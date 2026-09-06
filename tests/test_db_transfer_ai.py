import csv
import json
import sqlite3
import zipfile
from datetime import date, timedelta

import pytest

from gca import config as C
from gca.ai_client import AIClient
from gca.db import Database, Repos, SCHEMA_VERSION
from gca.dictionary import build_dictionary
from gca.srs import SRSState
from gca.transfer import CSV_FIELDS, export_csv, export_pack, import_csv, import_pack


@pytest.fixture()
def repos(tmp_path):
    db = Database(tmp_path / "course.db"); result = Repos(db); yield result; db.close()


def test_database_schema_migration_and_seed(repos):
    assert repos.words.count() >= 150
    assert int(repos.db.one("SELECT value FROM meta WHERE key='schema_version'")["value"]) == SCHEMA_VERSION
    assert {"article", "gender", "plural", "audio"} <= {r[1] for r in repos.db.query("PRAGMA table_info(words)")}


def test_search_uses_controlled_umlaut_and_eszett_equivalence(repos):
    assert any(w["target"] == "Mädchen" for w in repos.words.search("maedchen"))
    assert any(w["target"] == "Straße" for w in repos.words.search("strasse"))
    assert any(w["target"] == "Milch" for w in repos.words.search("süt"))


def test_profiles_progress_favorites_and_streak(repos):
    pid = repos.profiles.ensure_default(); word = repos.words.all()[0]
    repos.progress.save(pid, word["id"], SRSState(due=date.today()-timedelta(days=1), box=4), 1, 0)
    assert word["id"] in {w["id"] for w in repos.progress.due_words(pid)}
    assert repos.progress.toggle_star(pid, word["id"]) and repos.progress.starred(pid)
    repos.study.log(pid, "srs", 1, 0); assert repos.study.streak(pid) == 1


def test_exam_can_be_scored(repos):
    pid = repos.profiles.ensure_default(); eid = repos.exams.start(pid, "mcq")
    repos.exams.answer(eid, None, "mcq", "a", "x", "x", True); repos.exams.answer(eid, None, "mcq", "b", "x", "y", False)
    assert repos.exams.finish(eid) == {"total": 2, "correct": 1, "score": 50.0}


def test_csv_roundtrip_preserves_unicode(repos, tmp_path):
    path = tmp_path / "wörter.csv"; export_csv(repos.words.search("Straße"), path)
    text = path.read_text(encoding="utf-8-sig"); assert "Straße" in text and "straße" not in text
    other = Repos(Database(tmp_path / "import.db")); before = other.words.count(); import_csv(other.words, path)
    assert any(w["target"] == "Straße" for w in other.words.search("straße")); other.db.close()


def test_pack_roundtrip_and_language_guard(repos, tmp_path):
    pid = repos.profiles.ensure_default(); path = tmp_path / ("test" + C.PACK_EXTENSION)
    export_pack(repos, pid, path, True); assert zipfile.is_zipfile(path)
    target = Repos(Database(tmp_path / "target.db")); count = import_pack(target, target.profiles.ensure_default(), path)
    assert count >= 150; target.db.close()


def test_token_ledger_has_no_prompt_or_response_columns(repos):
    repos.tokens.log("model", "grammar", 12, 8, 50)
    cols = {r[1] for r in repos.db.query("PRAGMA table_info(token_log)")}
    assert not ({"prompt", "response", "text", "content"} & cols)
    assert repos.tokens.summary() == {"calls": 1, "tokens": 20}


def test_ai_unavailable_is_safe_and_non_throwing():
    client = AIClient("http://127.0.0.1:9")
    assert client.available(timeout=0.05) is False and client.models(timeout=0.05) == []


OLD_DICT_SCHEMA = """
CREATE TABLE dict_entries(
 id INTEGER PRIMARY KEY, headword TEXT NOT NULL, translation TEXT NOT NULL,
 pos TEXT NOT NULL DEFAULT '', extra TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(headword, translation));
"""


def test_dict_entries_gets_source_and_example_columns_on_old_databases(tmp_path):
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.executescript(OLD_DICT_SCHEMA)
    old.execute("INSERT INTO dict_entries(headword,translation,pos,extra,note) VALUES('Brezel','pretzel','n','die Brezeln','')")
    old.commit(); old.close()
    db = Database(path); repos = Repos(db)
    assert {"source", "example"} <= {r[1] for r in db.query("PRAGMA table_info(dict_entries)")}
    rows = repos.dictionary.all()
    assert [(r["headword"], r["source"], r["example"]) for r in rows] == [("Brezel", "user", "")]
    assert repos.dictionary.add("Semmel", "bread roll", "n", "die Semmeln", "", "ai", "Eine Semmel, bitte.") == 1
    assert repos.dictionary.add_many([("Brezel", "pretzel")], "ai") == 0            # UNIQUE(headword, translation) still holds
    assert repos.dictionary.count_by_source() == {"user": 1, "ai": 1} and repos.dictionary.count("ai") == 1
    d = build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r["source"], r["example"]) for r in repos.dictionary.all()])
    semmel, brezel = d.lookup("Semmel")[1][0], d.lookup("Brezel")[1][0]
    assert (semmel.source, semmel.example, brezel.source) == ("ai", "Eine Semmel, bitte.", "user")
    repos.dictionary.clear("ai")
    assert repos.dictionary.count() == 1 and repos.dictionary.count_by_source() == {"user": 1}
    assert Database(path).query("PRAGMA table_info(dict_entries)")                   # reopening is idempotent
    db.close()
