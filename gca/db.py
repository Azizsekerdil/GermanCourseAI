from __future__ import annotations

import sqlite3
from dataclasses import asdict
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable

from . import config as C
from .seed_words import WORDS
from .srs import SRSState

SCHEMA_VERSION = 4

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS profiles(
 id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS words(
 id INTEGER PRIMARY KEY, target TEXT NOT NULL, target_search TEXT NOT NULL,
 tr TEXT NOT NULL, en TEXT NOT NULL DEFAULT '', article TEXT NOT NULL DEFAULT '',
 gender TEXT NOT NULL DEFAULT '', plural TEXT NOT NULL DEFAULT '', pos TEXT NOT NULL DEFAULT '',
 example_target TEXT NOT NULL DEFAULT '', example_tr TEXT NOT NULL DEFAULT '', example_en TEXT NOT NULL DEFAULT '',
 frequency_rank INTEGER NOT NULL DEFAULT 9999, deck TEXT NOT NULL DEFAULT 'A1', audio TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(target_search, deck));
CREATE INDEX IF NOT EXISTS idx_words_search ON words(target_search);
CREATE TABLE IF NOT EXISTS word_progress(
 profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
 word_id INTEGER NOT NULL REFERENCES words(id) ON DELETE CASCADE,
 repetitions INTEGER NOT NULL DEFAULT 0, interval_days INTEGER NOT NULL DEFAULT 0,
 ease REAL NOT NULL DEFAULT 2.5, due TEXT NOT NULL, box INTEGER NOT NULL DEFAULT 1,
 correct INTEGER NOT NULL DEFAULT 0, wrong INTEGER NOT NULL DEFAULT 0,
 starred INTEGER NOT NULL DEFAULT 0, last_seen TEXT,
 PRIMARY KEY(profile_id, word_id));
CREATE TABLE IF NOT EXISTS study_log(
 id INTEGER PRIMARY KEY, profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
 day TEXT NOT NULL, activity TEXT NOT NULL, correct INTEGER NOT NULL DEFAULT 0,
 wrong INTEGER NOT NULL DEFAULT 0, seconds INTEGER NOT NULL DEFAULT 0);
CREATE INDEX IF NOT EXISTS idx_study_day ON study_log(profile_id, day);
CREATE TABLE IF NOT EXISTS exams(
 id INTEGER PRIMARY KEY, profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
 started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, finished_at TEXT, kinds TEXT NOT NULL,
 cefr TEXT NOT NULL DEFAULT 'A1', total INTEGER NOT NULL DEFAULT 0,
 correct INTEGER NOT NULL DEFAULT 0, score REAL NOT NULL DEFAULT 0);
CREATE TABLE IF NOT EXISTS exam_answers(
 id INTEGER PRIMARY KEY, exam_id INTEGER NOT NULL REFERENCES exams(id) ON DELETE CASCADE,
 word_id INTEGER, kind TEXT NOT NULL, prompt TEXT NOT NULL, given_answer TEXT NOT NULL,
 correct_answer TEXT NOT NULL, is_correct INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS token_log(
 id INTEGER PRIMARY KEY, ts TEXT NOT NULL, day TEXT NOT NULL, model TEXT NOT NULL,
 task TEXT NOT NULL, prompt_tokens INTEGER NOT NULL DEFAULT 0,
 completion_tokens INTEGER NOT NULL DEFAULT 0, total_tokens INTEGER NOT NULL DEFAULT 0,
 ms INTEGER NOT NULL DEFAULT 0, ok INTEGER NOT NULL DEFAULT 1);
CREATE INDEX IF NOT EXISTS idx_token_day ON token_log(day);
CREATE TABLE IF NOT EXISTS pdf_notes(
 id INTEGER PRIMARY KEY, profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
 pdf_path TEXT NOT NULL, page INTEGER NOT NULL, note TEXT NOT NULL, updated_at TEXT NOT NULL,
 UNIQUE(profile_id, pdf_path, page));
CREATE TABLE IF NOT EXISTS resource_state(
 profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
 resource_id TEXT NOT NULL, completed INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(profile_id, resource_id));
CREATE TABLE IF NOT EXISTS grammar_progress(
 profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
 topic TEXT NOT NULL, correct INTEGER NOT NULL DEFAULT 0, wrong INTEGER NOT NULL DEFAULT 0,
 PRIMARY KEY(profile_id, topic));
CREATE TABLE IF NOT EXISTS dict_entries(
 id INTEGER PRIMARY KEY, headword TEXT NOT NULL, translation TEXT NOT NULL,
 pos TEXT NOT NULL DEFAULT '', extra TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '',
 source TEXT NOT NULL DEFAULT 'user', example TEXT NOT NULL DEFAULT '', tr TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(headword, translation));
"""


class Database:
    def __init__(self, path: str | Path | None = None):
        C.ensure_dirs()
        self.path = Path(path or C.DB_PATH)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path, timeout=15, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self._migrate()

    def _migrate(self) -> None:
        """Forward-only, additive migration safe for older local databases."""
        columns = {r[1] for r in self.conn.execute("PRAGMA table_info(words)")}
        additions = {
            "gender": "TEXT NOT NULL DEFAULT ''", "audio": "TEXT NOT NULL DEFAULT ''",
            "example_en": "TEXT NOT NULL DEFAULT ''",
        }
        for name, sql_type in additions.items():
            if name not in columns:
                self.conn.execute(f"ALTER TABLE words ADD COLUMN {name} {sql_type}")
        dict_columns = {r[1] for r in self.conn.execute("PRAGMA table_info(dict_entries)")}
        for name, sql_type in {"source": "TEXT NOT NULL DEFAULT 'user'", "example": "TEXT NOT NULL DEFAULT ''",
                               "tr": "TEXT NOT NULL DEFAULT ''"}.items():
            if name not in dict_columns:
                self.conn.execute(f"ALTER TABLE dict_entries ADD COLUMN {name} {sql_type}")
        self.conn.execute("INSERT INTO meta(key,value) VALUES('schema_version',?) "
                          "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(SCHEMA_VERSION),))
        self.conn.commit()

    def execute(self, sql: str, args: Iterable[Any] = ()) -> sqlite3.Cursor:
        cur = self.conn.execute(sql, tuple(args))
        self.conn.commit()
        return cur

    def query(self, sql: str, args: Iterable[Any] = ()) -> list[sqlite3.Row]:
        return list(self.conn.execute(sql, tuple(args)))

    def one(self, sql: str, args: Iterable[Any] = ()) -> sqlite3.Row | None:
        return self.conn.execute(sql, tuple(args)).fetchone()

    def close(self) -> None:
        self.conn.close()


class ProfileRepo:
    def __init__(self, db: Database): self.db = db
    def ensure_default(self) -> int:
        row = self.db.one("SELECT id FROM profiles ORDER BY id LIMIT 1")
        return int(row["id"]) if row else self.create("Alex")
    def create(self, name: str) -> int:
        return int(self.db.execute("INSERT INTO profiles(name) VALUES(?)", (name.strip(),)).lastrowid)
    def all(self): return [dict(r) for r in self.db.query("SELECT * FROM profiles ORDER BY id")]
    def delete(self, profile_id: int) -> None: self.db.execute("DELETE FROM profiles WHERE id=?", (profile_id,))


class WordRepo:
    def __init__(self, db: Database):
        self.db = db
        self.seed()

    def seed(self) -> None:
        if self.count() >= len(WORDS):
            return
        sql = ("INSERT OR IGNORE INTO words(target,target_search,tr,en,article,gender,plural,pos,"
               "example_target,example_tr,example_en,frequency_rank,deck,audio) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)")
        rows = []
        for word in WORDS:
            term = word[C.TARGET_LANG]
            rows.append((term, C.normalize_search(term), word["tr"], word["en"], word.get("article", ""),
                         word.get("gender", ""), word.get("plural", ""), word.get("part_of_speech", ""),
                         word.get(f"example_{C.TARGET_LANG}", ""), word.get("example_tr", ""),
                         word.get("example_en", ""), int(word.get("frequency_rank", 9999)),
                         word.get("deck", "A1"), word.get("audio", "")))
        self.db.conn.executemany(sql, rows)
        self.db.conn.commit()

    def count(self) -> int: return int(self.db.one("SELECT COUNT(*) n FROM words")["n"])
    def all(self, limit: int | None = None) -> list[dict[str, Any]]:
        sql = "SELECT * FROM words ORDER BY frequency_rank,target" + (" LIMIT ?" if limit else "")
        rows = self.db.query(sql, (limit,)) if limit else self.db.query(sql)
        return [dict(r) for r in rows]
    def get(self, word_id: int):
        row = self.db.one("SELECT * FROM words WHERE id=?", (word_id,))
        return dict(row) if row else None
    def decks(self) -> list[str]:
        return [r["deck"] for r in self.db.query("SELECT DISTINCT deck FROM words ORDER BY deck")]
    def search(self, query: str, limit: int = 200) -> list[dict[str, Any]]:
        q = (query or "").strip()
        if not q: return self.all(limit)
        search = f"%{C.normalize_search(q)}%"
        loose = f"%{q.lower()}%"
        rows = self.db.query("SELECT * FROM words WHERE target_search LIKE ? OR lower(tr) LIKE ? "
                             "OR lower(en) LIKE ? ORDER BY frequency_rank LIMIT ?",
                             (search, loose, loose, limit))
        return [dict(r) for r in rows]
    def add(self, target: str, tr: str, en: str = "", **fields) -> int:
        deck = fields.get("deck", "Kişisel")
        search = C.normalize_search(target)
        row = self.db.one("SELECT id FROM words WHERE target_search=? AND deck=?", (search, deck))
        if row: return int(row["id"])
        cur = self.db.execute("INSERT INTO words(target,target_search,tr,en,article,gender,plural,pos,"
                              "example_target,example_tr,example_en,frequency_rank,deck,audio) "
                              "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                              (target, search, tr, en, fields.get("article", ""), fields.get("gender", ""),
                               fields.get("plural", ""), fields.get("pos", ""), fields.get("example_target", ""),
                               fields.get("example_tr", ""), fields.get("example_en", ""),
                               int(fields.get("frequency_rank", 9999)), deck, fields.get("audio", "")))
        return int(cur.lastrowid)
    def delete(self, word_id: int) -> None: self.db.execute("DELETE FROM words WHERE id=?", (word_id,))


class ProgressRepo:
    def __init__(self, db: Database): self.db = db
    def state(self, profile_id: int, word_id: int) -> SRSState:
        row = self.db.one("SELECT * FROM word_progress WHERE profile_id=? AND word_id=?", (profile_id, word_id))
        if not row: return SRSState()
        return SRSState(int(row["repetitions"]), int(row["interval_days"]), float(row["ease"]),
                        date.fromisoformat(row["due"]), int(row["box"]))
    def save(self, profile_id: int, word_id: int, state: SRSState,
             correct_inc: int = 0, wrong_inc: int = 0) -> None:
        self.db.execute("INSERT INTO word_progress(profile_id,word_id,repetitions,interval_days,ease,due,box,correct,wrong,last_seen) "
                        "VALUES(?,?,?,?,?,?,?,?,?,?) ON CONFLICT(profile_id,word_id) DO UPDATE SET "
                        "repetitions=excluded.repetitions,interval_days=excluded.interval_days,ease=excluded.ease,"
                        "due=excluded.due,box=excluded.box,correct=word_progress.correct+excluded.correct,"
                        "wrong=word_progress.wrong+excluded.wrong,last_seen=excluded.last_seen",
                        (profile_id, word_id, state.repetitions, state.interval, state.ease, state.due.isoformat(),
                         state.box, correct_inc, wrong_inc, date.today().isoformat()))
    def due_words(self, profile_id: int, limit: int = 20):
        rows = self.db.query("SELECT w.* FROM words w JOIN word_progress p ON p.word_id=w.id "
                             "WHERE p.profile_id=? AND p.due<=? ORDER BY p.due LIMIT ?",
                             (profile_id, date.today().isoformat(), limit))
        return [dict(r) for r in rows]
    def new_words(self, profile_id: int, limit: int = 20):
        rows = self.db.query("SELECT w.* FROM words w LEFT JOIN word_progress p ON p.word_id=w.id AND p.profile_id=? "
                             "WHERE p.word_id IS NULL ORDER BY w.frequency_rank LIMIT ?", (profile_id, limit))
        return [dict(r) for r in rows]
    def wrong_words(self, profile_id: int, limit: int = 100):
        rows = self.db.query("SELECT w.* FROM words w JOIN word_progress p ON p.word_id=w.id "
                             "WHERE p.profile_id=? AND p.wrong>p.correct ORDER BY p.wrong-p.correct DESC LIMIT ?",
                             (profile_id, limit))
        return [dict(r) for r in rows]
    def starred(self, profile_id: int):
        return [dict(r) for r in self.db.query("SELECT w.* FROM words w JOIN word_progress p ON p.word_id=w.id "
                                                "WHERE p.profile_id=? AND p.starred=1 ORDER BY w.target", (profile_id,))]
    def toggle_star(self, profile_id: int, word_id: int) -> bool:
        row = self.db.one("SELECT starred FROM word_progress WHERE profile_id=? AND word_id=?", (profile_id, word_id))
        value = 0 if row and row["starred"] else 1
        self.db.execute("INSERT INTO word_progress(profile_id,word_id,due,starred) VALUES(?,?,?,?) "
                        "ON CONFLICT(profile_id,word_id) DO UPDATE SET starred=excluded.starred",
                        (profile_id, word_id, date.today().isoformat(), value))
        return bool(value)
    def dashboard(self, profile_id: int) -> dict[str, int]:
        total = int(self.db.one("SELECT COUNT(*) n FROM words")["n"])
        row = self.db.one("SELECT COUNT(*) seen, COALESCE(SUM(CASE WHEN box>=4 THEN 1 ELSE 0 END),0) learned "
                          "FROM word_progress WHERE profile_id=? AND (correct+wrong)>0", (profile_id,))
        due = int(self.db.one("SELECT COUNT(*) n FROM word_progress WHERE profile_id=? AND due<=?",
                              (profile_id, date.today().isoformat()))["n"])
        return {"total": total, "seen": int(row["seen"]), "learned": int(row["learned"]),
                "new": total - int(row["seen"]), "due": due}


class StudyRepo:
    def __init__(self, db: Database): self.db = db
    def log(self, profile_id: int, activity: str, correct: int, wrong: int, seconds: int = 0) -> None:
        self.db.execute("INSERT INTO study_log(profile_id,day,activity,correct,wrong,seconds) VALUES(?,?,?,?,?,?)",
                        (profile_id, date.today().isoformat(), activity, correct, wrong, seconds))
    def streak(self, profile_id: int) -> int:
        days = {r["day"] for r in self.db.query("SELECT DISTINCT day FROM study_log WHERE profile_id=?", (profile_id,))}
        streak = 0
        cursor = date.today()
        while cursor.isoformat() in days:
            streak += 1; cursor -= timedelta(days=1)
        return streak
    def daily(self, profile_id: int, days: int = 7):
        start = date.today() - timedelta(days=days - 1)
        raw = {r["day"]: dict(r) for r in self.db.query("SELECT day,SUM(correct) correct,SUM(wrong) wrong,SUM(seconds) seconds "
                                                          "FROM study_log WHERE profile_id=? AND day>=? GROUP BY day",
                                                          (profile_id, start.isoformat()))}
        return [raw.get((start + timedelta(days=i)).isoformat(), {"day": (start + timedelta(days=i)).isoformat(), "correct": 0, "wrong": 0, "seconds": 0}) for i in range(days)]


class ExamRepo:
    def __init__(self, db: Database): self.db = db
    def start(self, profile_id: int, kinds: str, cefr: str = "A1") -> int:
        return int(self.db.execute("INSERT INTO exams(profile_id,kinds,cefr) VALUES(?,?,?)", (profile_id, kinds, cefr)).lastrowid)
    def answer(self, exam_id: int, word_id: int | None, kind: str, prompt: str, given: str, correct: str, ok: bool) -> None:
        self.db.execute("INSERT INTO exam_answers(exam_id,word_id,kind,prompt,given_answer,correct_answer,is_correct) VALUES(?,?,?,?,?,?,?)",
                        (exam_id, word_id, kind, prompt, given, correct, int(ok)))
    def finish(self, exam_id: int):
        row = self.db.one("SELECT COUNT(*) total, COALESCE(SUM(is_correct),0) correct FROM exam_answers WHERE exam_id=?", (exam_id,))
        total, correct = int(row["total"]), int(row["correct"])
        score = round(correct * 100 / total, 1) if total else 0.0
        self.db.execute("UPDATE exams SET finished_at=?,total=?,correct=?,score=? WHERE id=?",
                        (datetime.now().isoformat(timespec="seconds"), total, correct, score, exam_id))
        return {"total": total, "correct": correct, "score": score}


class TokenRepo:
    def __init__(self, db: Database): self.db = db
    def log(self, model: str, task: str, prompt_tokens: int, completion_tokens: int, ms: int, ok: bool = True) -> None:
        now = datetime.now()
        self.db.execute("INSERT INTO token_log(ts,day,model,task,prompt_tokens,completion_tokens,total_tokens,ms,ok) VALUES(?,?,?,?,?,?,?,?,?)",
                        (now.isoformat(timespec="seconds"), now.date().isoformat(), model, task,
                         prompt_tokens, completion_tokens, prompt_tokens + completion_tokens, ms, int(ok)))
    def summary(self):
        row = self.db.one("SELECT COUNT(*) calls,COALESCE(SUM(total_tokens),0) tokens FROM token_log")
        return {"calls": int(row["calls"]), "tokens": int(row["tokens"])}
    def rows(self): return [dict(r) for r in self.db.query("SELECT * FROM token_log ORDER BY id DESC LIMIT 500")]


class NoteRepo:
    def __init__(self, db: Database): self.db = db
    def save(self, profile_id: int, pdf_path: str, page: int, note: str) -> None:
        self.db.execute("INSERT INTO pdf_notes(profile_id,pdf_path,page,note,updated_at) VALUES(?,?,?,?,?) "
                        "ON CONFLICT(profile_id,pdf_path,page) DO UPDATE SET note=excluded.note,updated_at=excluded.updated_at",
                        (profile_id, pdf_path, page, note, datetime.now().isoformat(timespec="seconds")))
    def get(self, profile_id: int, pdf_path: str, page: int) -> str:
        row = self.db.one("SELECT note FROM pdf_notes WHERE profile_id=? AND pdf_path=? AND page=?", (profile_id, pdf_path, page))
        return row["note"] if row else ""


class ResourceRepo:
    def __init__(self, db: Database): self.db = db
    def toggle(self, profile_id: int, resource_id: str) -> bool:
        row = self.db.one("SELECT completed FROM resource_state WHERE profile_id=? AND resource_id=?", (profile_id, resource_id))
        value = 0 if row and row["completed"] else 1
        self.db.execute("INSERT INTO resource_state(profile_id,resource_id,completed) VALUES(?,?,?) "
                        "ON CONFLICT(profile_id,resource_id) DO UPDATE SET completed=excluded.completed", (profile_id, resource_id, value))
        return bool(value)


class GrammarRepo:
    def __init__(self, db: Database): self.db = db
    def record(self, profile_id: int, topic: str, correct: int, wrong: int) -> None:
        self.db.execute("INSERT INTO grammar_progress(profile_id,topic,correct,wrong) VALUES(?,?,?,?) "
                        "ON CONFLICT(profile_id,topic) DO UPDATE SET correct=grammar_progress.correct+excluded.correct,wrong=grammar_progress.wrong+excluded.wrong",
                        (profile_id, topic, correct, wrong))


class DictRepo:
    """User-added and AI-cached dictionary entries layered on top of the built-in dictionary."""
    SOURCE_USER, SOURCE_AI = "user", "ai"
    def __init__(self, db: Database): self.db = db
    def all(self): return [dict(r) for r in self.db.query("SELECT * FROM dict_entries ORDER BY headword")]
    def count(self, source: str | None = None) -> int:
        if source: return int(self.db.one("SELECT COUNT(*) n FROM dict_entries WHERE source=?", (source,))["n"])
        return int(self.db.one("SELECT COUNT(*) n FROM dict_entries")["n"])
    def count_by_source(self) -> dict[str, int]:
        return {r["source"]: int(r["n"]) for r in self.db.query("SELECT source, COUNT(*) n FROM dict_entries GROUP BY source")}
    def add_many(self, rows, source: str = SOURCE_USER) -> int:
        """rows: (headword, translation[, pos[, extra[, note[, example[, tr]]]]]). Returns the number actually inserted.

        A row whose (headword, translation) is already stored is never duplicated; a *user* row's non-empty Turkish gloss
        replaces the stored one (the user curates the Turkish side, mirroring ``Dictionary.merge_tr``), other sources leave it."""
        before = self.count(); source = source or self.SOURCE_USER
        def cell(r, i): return (r[i] if len(r) > i else "") or ""
        sql = "INSERT OR IGNORE INTO dict_entries(headword,translation,pos,extra,note,source,example,tr) VALUES(?,?,?,?,?,?,?,?)"
        if source == self.SOURCE_USER: sql += " ON CONFLICT(headword, translation) DO UPDATE SET tr=excluded.tr WHERE excluded.tr != ''"
        self.db.conn.executemany(sql, [(r[0].strip(), r[1].strip(), cell(r, 2), cell(r, 3), cell(r, 4), source, cell(r, 5), cell(r, 6).strip())
                                       for r in rows if r and r[0].strip() and r[1].strip()])
        self.db.conn.commit(); return self.count() - before
    def add(self, headword: str, translation: str, pos: str = "", extra: str = "", note: str = "",
            source: str = SOURCE_USER, example: str = "", tr: str = "") -> int:
        return self.add_many([(headword, translation, pos, extra, note, example, tr)], source)
    def set_tr(self, headword: str, translation: str, tr: str) -> bool:
        """Give the stored row (headword, translation) its Turkish gloss; False when no such row exists (built-in entries)."""
        cur = self.db.execute("UPDATE dict_entries SET tr=? WHERE headword=? AND translation=?", (tr.strip(), headword.strip(), translation.strip()))
        return cur.rowcount > 0
    def clear(self, source: str | None = None) -> None:
        if source: self.db.execute("DELETE FROM dict_entries WHERE source=?", (source,))
        else: self.db.execute("DELETE FROM dict_entries")


class Repos:
    def __init__(self, db: Database):
        self.db = db; self.profiles = ProfileRepo(db); self.words = WordRepo(db)
        self.progress = ProgressRepo(db); self.study = StudyRepo(db); self.exams = ExamRepo(db)
        self.tokens = TokenRepo(db); self.notes = NoteRepo(db); self.resources = ResourceRepo(db)
        self.grammar = GrammarRepo(db); self.dictionary = DictRepo(db)
