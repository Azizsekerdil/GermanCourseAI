from __future__ import annotations

import csv
import json
import zipfile
from datetime import datetime
from pathlib import Path

from . import config as C

CSV_FIELDS = [C.TARGET_LANG, "tr", "en", "article", "gender", "plural", "part_of_speech",
              f"example_{C.TARGET_LANG}", "example_tr", "example_en", "frequency_rank", "deck", "audio"]


def export_csv(words: list[dict], path: str | Path) -> Path:
    path = Path(path)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for word in words:
            writer.writerow({
                C.TARGET_LANG: word.get("target", word.get(C.TARGET_LANG, "")), "tr": word.get("tr", ""),
                "en": word.get("en", ""), "article": word.get("article", ""), "gender": word.get("gender", ""),
                "plural": word.get("plural", ""), "part_of_speech": word.get("pos", word.get("part_of_speech", "")),
                f"example_{C.TARGET_LANG}": word.get("example_target", word.get(f"example_{C.TARGET_LANG}", "")),
                "example_tr": word.get("example_tr", ""), "example_en": word.get("example_en", ""),
                "frequency_rank": word.get("frequency_rank", 9999), "deck": word.get("deck", "A1"),
                "audio": word.get("audio", ""),
            })
    return path


def import_csv(repo, path: str | Path) -> int:
    count = 0
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            target, tr = (row.get(C.TARGET_LANG) or "").strip(), (row.get("tr") or "").strip()
            if not target or not tr:
                continue
            repo.add(target, tr, row.get("en", ""), article=row.get("article", ""), gender=row.get("gender", ""),
                     plural=row.get("plural", ""), pos=row.get("part_of_speech", ""),
                     example_target=row.get(f"example_{C.TARGET_LANG}", ""), example_tr=row.get("example_tr", ""),
                     example_en=row.get("example_en", ""), frequency_rank=int(row.get("frequency_rank") or 9999),
                     deck=row.get("deck") or "İçe Aktarılan", audio=row.get("audio", ""))
            count += 1
    return count


def export_pack(repos, profile_id: int, path: str | Path, include_progress: bool = False) -> Path:
    path = Path(path)
    words = repos.words.all()
    manifest = {"format": "courseai-pack", "version": 1, "app": C.APP_SLUG, "target_lang": C.TARGET_LANG,
                "created_at": datetime.now().isoformat(timespec="seconds"), "word_count": len(words)}
    payload = {"manifest": manifest, "words": words}
    if include_progress:
        payload["progress"] = [dict(r) for r in repos.db.query("SELECT * FROM word_progress WHERE profile_id=?", (profile_id,))]
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        archive.writestr("data.json", json.dumps(payload, ensure_ascii=False, indent=2))
    return path


def import_pack(repos, profile_id: int, path: str | Path) -> int:
    with zipfile.ZipFile(path) as archive:
        payload = json.loads(archive.read("data.json").decode("utf-8"))
    manifest = payload.get("manifest") or {}
    if manifest.get("format") != "courseai-pack" or manifest.get("target_lang") != C.TARGET_LANG:
        raise ValueError("Incompatible course pack")
    count = 0
    old_to_new = {}
    for word in payload.get("words", []):
        new_id = repos.words.add(word["target"], word["tr"], word.get("en", ""), article=word.get("article", ""),
                                 gender=word.get("gender", ""), plural=word.get("plural", ""), pos=word.get("pos", ""),
                                 example_target=word.get("example_target", ""), example_tr=word.get("example_tr", ""),
                                 example_en=word.get("example_en", ""), frequency_rank=word.get("frequency_rank", 9999),
                                 deck=word.get("deck", "Paket"), audio=word.get("audio", ""))
        old_to_new[int(word.get("id", 0))] = new_id; count += 1
    for progress in payload.get("progress", []):
        new_word = old_to_new.get(int(progress.get("word_id", 0)))
        if new_word:
            repos.db.execute("INSERT OR REPLACE INTO word_progress(profile_id,word_id,repetitions,interval_days,ease,due,box,correct,wrong,starred,last_seen) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                              (profile_id, new_word, progress.get("repetitions", 0), progress.get("interval_days", 0),
                               progress.get("ease", 2.5), progress.get("due"), progress.get("box", 1),
                               progress.get("correct", 0), progress.get("wrong", 0), progress.get("starred", 0),
                               progress.get("last_seen")))
    return count
