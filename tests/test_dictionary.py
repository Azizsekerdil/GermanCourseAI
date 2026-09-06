"""Dictionary engine: built-in data integrity, two-way lookup, import/export and the DB layer."""
from __future__ import annotations

import pytest

from gca import config as C
from gca import dictionary as D
from gca.db import Database, Repos


@pytest.fixture(scope="module")
def dic():
    return D.Dictionary(D.builtin_entries())


def test_builtin_data_is_large_and_well_formed(dic):
    entries = D.builtin_entries()
    assert len(entries) >= 1100
    assert len(dic) == len(entries), "duplicate entries in built-in data"
    seen = set()
    for e in entries:
        assert e.headword and e.translation and e.pos, e
        assert e.pos in D.POS_LABELS, e
        assert (e.headword, e.pos, e.extra) not in seen, e
        seen.add((e.headword, e.pos, e.extra))
        assert e.source == D.SOURCE_BUILTIN
        if C.TARGET_LANG == "de" and e.pos == "n":
            assert e.extra.split()[0] in ("der", "die", "das"), e
            assert e.display.startswith(e.extra.split()[0] + " ")
        if C.TARGET_LANG == "fr" and e.pos == "n":
            assert e.gender in ("m", "f", "mf", "pl"), e
        if C.TARGET_LANG == "en":
            assert e.note, e          # every English entry carries a definition


def test_lookup_both_directions(dic):
    target, other = {
        "de": ("Haus", "house"), "fr": ("maison", "house"), "en": ("house", "ev")}[C.TARGET_LANG]
    direction, rows = dic.lookup(target)
    assert direction == "target" and rows[0].headword == target
    direction, rows = dic.lookup(other)
    assert direction == "translation" and target in [r.headword for r in rows[:2]]
    assert dic.lookup("")[1] == [] and dic.lookup("zzqqxx")[1] == []
    assert dic.lookup(target.upper())[1][0].headword == target      # case-insensitive


def test_language_specific_search_forms(dic):
    if C.TARGET_LANG == "de":
        assert dic.lookup("Häuser")[1][0].headword == "Haus"        # plural
        assert dic.lookup("haeuser")[1][0].headword == "Haus"       # umlaut fallback
        assert dic.lookup("Strasse")[1][0].headword == "Straße"     # ß fallback
        assert dic.lookup("the")[1][0].pos == "art"
    elif C.TARGET_LANG == "fr":
        assert dic.lookup("yeux")[1][0].headword == "œil"           # irregular plural
        assert dic.lookup("oeil")[1][0].headword == "œil"           # ligature fallback
        assert dic.lookup("ecole")[1][0].headword == "école"        # accent fallback
        assert dic.lookup("l'école")[1][0].headword == "école"      # elision
    else:
        assert dic.lookup("teeth")[1][0].headword == "tooth"        # irregular plural in definition
        assert dic.lookup("gitmek")[1][0].headword == "go"
        assert dic.lookup("go")[1][0].headword == "go"


def test_ranking_prefers_exact_then_prefix(dic):
    word = {"de": "gehen", "fr": "aller", "en": "go"}[C.TARGET_LANG]
    _d, rows = dic.lookup(word)
    assert rows[0].headword == word
    _d, rows = dic.lookup("to go" if C.TARGET_LANG != "en" else "gitmek")
    assert rows[0].headword == word


def test_parse_line_and_fields():
    e = D.parse_line("Haus|n das Häuser|house|note here")
    assert (e.headword, e.pos, e.extra, e.translation, e.note) == ("Haus", "n", "das Häuser", "house", "note here")
    assert e.plural == "Häuser" and e.gender == "n" and e.display == "das Haus"
    assert D.parse_line("# comment") is None and D.parse_line("") is None and D.parse_line("one|two") is None
    f = D.parse_line("œil|n m yeux|eye")
    assert f.gender == "m" and f.plural == "yeux" and f.display == "œil"


def test_table_roundtrip(tmp_path):
    src = tmp_path / "in.csv"
    src.write_text("headword,translation,pos,extra,note\nalpha,first,n,,x\nbeta,second\n,empty\n", encoding="utf-8")
    rows = D.read_table(src)
    assert [(r.headword, r.translation) for r in rows] == [("alpha", "first"), ("beta", "second")]
    assert rows[0].source == D.SOURCE_USER and rows[0].note == "x"
    out = tmp_path / "out.csv"
    assert D.write_table(out, rows) == 2 and "alpha" in out.read_text(encoding="utf-8")
    tsv = tmp_path / "in.tsv"; tsv.write_text("gamma\tthird\n", encoding="utf-8")
    assert D.read_table(tsv)[0].headword == "gamma"


def test_dictionary_merges_sources_and_dedupes(dic):
    d = D.Dictionary(dic.entries)
    n = len(d)
    assert d.extend([D.Entry("zzz", "n", "", "test", "", D.SOURCE_USER), D.Entry("zzz", "n", "", "test", "", D.SOURCE_USER)]) == 1
    assert len(d) == n + 1 and d.count_by_source()[D.SOURCE_USER] == 1
    assert d.lookup("zzz")[1][0].source == D.SOURCE_USER
    d.remove_source(D.SOURCE_USER)
    assert len(d) == n and d.random_entry() is not None


def test_dict_repo_persists_user_entries(tmp_path):
    db = Database(tmp_path / "t.db"); repos = Repos(db)
    assert repos.dictionary.count() == 0
    assert repos.dictionary.add_many([("qqq", "www", "n", "", ""), ("qqq", "www"), ("", "x")]) == 1
    assert repos.dictionary.add("rrr", "sss") == 1
    rows = repos.dictionary.all()
    assert {r["headword"] for r in rows} == {"qqq", "rrr"}
    d = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"]) for r in rows])
    assert d.lookup("qqq")[1][0].source == D.SOURCE_USER and d.lookup("sss")[1][0].headword == "rrr"
    repos.dictionary.clear(); assert repos.dictionary.count() == 0
    db.close()
