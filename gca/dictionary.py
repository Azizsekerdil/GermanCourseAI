"""Bidirectional target-language <-> English dictionary engine.

Layers that are merged at runtime:
1. Built-in core dictionary (``dict_data.py``; ~900 A1-B1 entries).
2. User entries imported from CSV/TSV or added by hand (SQLite ``dict_entries``).

Search runs on both sides at once. The best-scoring side decides the direction
shown to the user; ranking is exact > prefix > word-start > substring.
"""
from __future__ import annotations

import csv
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

from . import config as C

SOURCE_BUILTIN = "builtin"
SOURCE_USER = "user"

POS_LABELS: dict[str, dict[str, str]] = {
    "n":    {"tr": "isim", "en": "noun", "de": "Substantiv", "fr": "nom"},
    "v":    {"tr": "fiil", "en": "verb", "de": "Verb", "fr": "verbe"},
    "adj":  {"tr": "sıfat", "en": "adjective", "de": "Adjektiv", "fr": "adjectif"},
    "adv":  {"tr": "zarf", "en": "adverb", "de": "Adverb", "fr": "adverbe"},
    "pron": {"tr": "zamir", "en": "pronoun", "de": "Pronomen", "fr": "pronom"},
    "prep": {"tr": "edat", "en": "preposition", "de": "Präposition", "fr": "préposition"},
    "conj": {"tr": "bağlaç", "en": "conjunction", "de": "Konjunktion", "fr": "conjonction"},
    "num":  {"tr": "sayı", "en": "numeral", "de": "Zahlwort", "fr": "numéral"},
    "art":  {"tr": "tanımlık", "en": "article", "de": "Artikel", "fr": "article"},
    "int":  {"tr": "ünlem", "en": "interjection", "de": "Interjektion", "fr": "interjection"},
    "part": {"tr": "parçacık", "en": "particle", "de": "Partikel", "fr": "particule"},
    "phr":  {"tr": "deyim", "en": "phrase", "de": "Wendung", "fr": "expression"},
}


@dataclass(frozen=True)
class Entry:
    headword: str
    pos: str
    extra: str            # article + plural (DE), gender/plural (FR), IPA or "" (EN)
    translation: str      # English (DE/FR apps) or Turkish (EN app); senses separated by ';'
    note: str = ""        # optional gloss / definition / usage hint
    source: str = SOURCE_BUILTIN

    def pos_label(self, lang: str) -> str:
        return POS_LABELS.get(self.pos, {}).get(lang, self.pos)

    @property
    def display(self) -> str:
        """Headword with article for German-style nouns (``das Haus``)."""
        art = self.extra.split()[0] if self.pos == "n" and self.extra.split() and self.extra.split()[0] in ARTICLES else ""
        return f"{art} {self.headword}".strip()

    @property
    def plural(self) -> str:
        toks = self.extra.split()
        if self.pos != "n":
            return ""
        toks = [t for t in toks if t not in ARTICLES and t not in GENDERS]
        return " ".join(toks)

    @property
    def gender(self) -> str:
        for t in self.extra.split():
            if t in ARTICLES:
                return ARTICLES[t]
            if t in GENDERS:
                return t
        return ""


ARTICLES = {"der": "m", "die": "f", "das": "n", "le": "m", "la": "f", "l'": "", "les": "pl"}
GENDERS = {"m", "f", "n", "pl", "mf"}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_line(line: str, source: str = SOURCE_BUILTIN) -> Entry | None:
    """``headword|pos extra…|translation[|note]``."""
    line = (line or "").strip()
    if not line or line.startswith("#"):
        return None
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 3:
        return None
    head, tag, tr = parts[0], parts[1], parts[2]
    note = parts[3] if len(parts) > 3 else ""
    toks = tag.split()
    pos = toks[0] if toks else ""
    extra = " ".join(toks[1:])
    if not head or not tr:
        return None
    return Entry(head, pos, extra, tr, note, source)


def parse_block(text: str, source: str = SOURCE_BUILTIN) -> list[Entry]:
    out = []
    for line in text.splitlines():
        e = parse_line(line, source)
        if e:
            out.append(e)
    return out


def _norm(text: str) -> str:
    return C.normalize_search(text)


def _senses(text: str) -> list[str]:
    """Split ';'-separated senses; also add each sense without its '(qualifier)'."""
    out: list[str] = []
    for raw in re.split(r"[;/]", text or ""):
        raw = raw.strip()
        if not raw:
            continue
        out.append(_norm(raw))
        bare = re.sub(r"\s*\([^)]*\)", "", raw).strip()
        if bare and bare != raw:
            out.append(_norm(bare))
    return [s for s in out if s]


def _score(q: str, field: str, senses: list[str]) -> int:
    if not field:
        return 0
    if q == field or q in senses:
        return 100
    for s in senses:
        if re.sub(r"^(to|the|a|an|sich|se|s') ", "", s) == q:
            return 95
    if field.startswith(q) or any(s.startswith(q) for s in senses):
        return 60
    if re.search(r"(^|[\s\-(])" + re.escape(q), field):
        return 30
    if len(q) >= 3 and q in field:
        return 10
    return 0


# ---------------------------------------------------------------------------
# Dictionary
# ---------------------------------------------------------------------------
class Dictionary:
    """In-memory two-sided dictionary with de-duplication by (headword, pos, translation)."""

    def __init__(self, entries: Iterable[Entry] = ()):
        self._entries: list[Entry] = []
        self._seen: set[tuple[str, str, str]] = set()
        self.extend(entries)

    def extend(self, entries: Iterable[Entry]) -> int:
        added = 0
        for e in entries:
            key = (_norm(e.headword), e.pos, _norm(e.translation))
            if key in self._seen:
                continue
            self._seen.add(key)
            self._entries.append(e)
            added += 1
        return added

    def remove_source(self, source: str) -> None:
        keep = [e for e in self._entries if e.source != source]
        self._entries, self._seen = [], set()
        self.extend(keep)

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def entries(self) -> Sequence[Entry]:
        return self._entries

    def count_by_source(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for e in self._entries:
            out[e.source] = out.get(e.source, 0) + 1
        return out

    def lookup(self, query: str, limit: int = 200) -> tuple[str, list[Entry]]:
        """Return (direction, entries). direction is 'target' or 'translation'."""
        q = _norm(query)
        if not q:
            return "target", []
        q = re.sub(r"^(l|d|j|s|qu|n|m|t|c)' ?", "", q) or q      # l'école -> école
        scored: list[tuple[int, int, int, Entry]] = []
        best_side = {"target": 0, "translation": 0}
        for e in self._entries:
            head = _norm(e.headword)
            target_forms = [head] + [_norm(t) for t in e.headword.split(",") if t.strip()]
            if e.plural:
                target_forms.append(_norm(e.plural))
            s_t = _score(q, head, target_forms)
            s_x = _score(q, _norm(e.translation), _senses(e.translation))
            if not s_t and not s_x and e.note and len(q) >= 3:
                s_x = 8 if _score(q, _norm(e.note), []) >= 30 else 0
            if s_t or s_x:
                side = 0 if s_t >= s_x else 1
                best_side["target" if side == 0 else "translation"] = max(
                    best_side["target" if side == 0 else "translation"], max(s_t, s_x))
                scored.append((max(s_t, s_x), side, len(e.headword), e))
        direction = "target" if best_side["target"] >= best_side["translation"] else "translation"
        scored.sort(key=lambda t: (-t[0], t[1], t[2], t[3].headword.lower()))
        return direction, [e for _s, _side, _l, e in scored[:limit]]

    def random_entry(self, rng: random.Random | None = None) -> Entry | None:
        pool = [e for e in self._entries if e.source == SOURCE_BUILTIN] or self._entries
        return (rng or random).choice(pool) if pool else None


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------
def read_table(path: Path) -> list[Entry]:
    """CSV/TSV with columns ``headword, translation[, pos[, extra[, note]]]``; header optional."""
    path = Path(path)
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    delim = "\t" if path.suffix.lower() in (".tsv", ".txt") or raw.count("\t") > raw.count(",") else ","
    out: list[Entry] = []
    for i, row in enumerate(csv.reader(raw.splitlines(), delimiter=delim)):
        if len(row) < 2:
            continue
        head, tr = row[0].strip(), row[1].strip()
        if not head or not tr:
            continue
        if i == 0 and head.lower() in ("headword", "word", C.TARGET_LANG, "target") and tr.lower() in ("translation", "en", "tr", "meaning", "english", "turkish"):
            continue
        pos = row[2].strip() if len(row) > 2 else ""
        extra = row[3].strip() if len(row) > 3 else ""
        note = row[4].strip() if len(row) > 4 else ""
        out.append(Entry(head, pos, extra, tr, note, SOURCE_USER))
    return out


def write_table(path: Path, entries: Iterable[Entry]) -> int:
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["headword", "translation", "pos", "extra", "note", "source"])
        for e in entries:
            w.writerow([e.headword, e.translation, e.pos, e.extra, e.note, e.source])
            n += 1
    return n


def builtin_entries() -> list[Entry]:
    from .dict_data import DATA
    return parse_block(DATA, SOURCE_BUILTIN)


def build_dictionary(user_rows: Iterable[Sequence[Any]] = ()) -> Dictionary:
    d = Dictionary(builtin_entries())
    d.extend(Entry(str(r[0]), str(r[2] if len(r) > 2 else "") or "", str(r[3] if len(r) > 3 else "") or "",
                   str(r[1]), str(r[4] if len(r) > 4 else "") or "", SOURCE_USER) for r in user_rows)
    return d
