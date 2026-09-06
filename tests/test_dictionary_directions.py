"""Dictionary directions and the Turkish side: data model, CSV, lookup per direction, AI keys, settings, DB migration."""
from __future__ import annotations

import json
import re
import sqlite3

import pytest

from gca import config as C
from gca import dictionary as D
from gca.db import Database, Repos

T = C.TARGET_LANG
# Sample entries per app: (headword, pos, extra, translation, tr). The English app has no separate Turkish field.
SAMPLE = {
    "de": [("Haus", "n", "das Häuser", "house; home", "ev; hane"), ("Baum", "n", "der Bäume", "tree", "ağaç"),
           ("Stuhl", "n", "der Stühle", "chair", ""), ("gehen", "v", "", "to go; to walk", "gitmek; yürümek")],
    "fr": [("maison", "n", "f", "house; home", "ev; hane"), ("arbre", "n", "m", "tree", "ağaç"),
           ("chaise", "n", "f", "chair", ""), ("aller", "v", "", "to go", "gitmek")],
    "en": [("house", "n", "/haʊs/", "ev; hane", ""), ("tree", "n", "", "ağaç", ""), ("chair", "n", "", "sandalye", ""),
           ("go", "v", "", "gitmek; yürümek", "")],
}[T]
HOUSE, TREE, CHAIR, GO = (row[0] for row in SAMPLE)


@pytest.fixture()
def dic():
    return D.Dictionary(D.Entry(h, p, x, t, "", D.SOURCE_USER, "", tr) for h, p, x, t, tr in SAMPLE)


# ---------------------------------------------------------------------------
# Direction codes and helpers
# ---------------------------------------------------------------------------
def test_direction_codes_follow_the_target_language():
    assert D.DIRECTIONS == C.DICT_DIRECTIONS and D.DIRECTIONS[0] == "auto"
    if T == "en":
        assert D.DIRECTIONS == ("auto", "en2tr", "tr2en") and not D.HAS_TR and D.OTHER_LANG == "tr"
        assert D.source_field("tr2en") == "translation" and D.target_field("en2tr") == "translation"
    else:
        assert D.DIRECTIONS == ("auto", f"{T}2en", f"en2{T}", f"{T}2tr", f"tr2{T}") and D.HAS_TR and D.OTHER_LANG == "en"
        assert D.target_field(f"{T}2tr") == "tr" and D.source_field(f"tr2{T}") == "tr"
        assert D.target_field(f"{T}2en") == "translation" and D.source_field(f"en2{T}") == "translation"
    assert D.DEFAULT_DIRECTION == D.DIRECTIONS[1] and D.target_field(f"{D.OTHER_LANG}2{T}") == "headword"
    assert D.split_direction(f"{T}2{D.OTHER_LANG}") == (T, D.OTHER_LANG) and D.split_direction("auto") == D.split_direction(D.DEFAULT_DIRECTION)
    assert D.direction_text(f"{T}2{D.OTHER_LANG}") == f"{T.upper()} → {D.OTHER_LANG.upper()}" and D.direction_text("auto") == "" and D.direction_text("bogus") == ""
    assert D.direction_code("tr", T) == f"tr2{T}"


def test_settings_dict_direction_default_and_validation():
    assert C.DEFAULT_SETTINGS["dict_direction"] == "auto"
    data = C.load_settings(); data["dict_direction"] = "bogus"; C.save_settings(data)
    assert C.load_settings()["dict_direction"] == "auto"
    data["dict_direction"] = D.DIRECTIONS[-1]; C.save_settings(data)
    assert C.load_settings()["dict_direction"] == D.DIRECTIONS[-1]
    data["dict_direction"] = "auto"; C.save_settings(data)


def test_normalize_search_keeps_turkish_letters():
    assert C.normalize_search("çğışöü") == "çğişoeue" and C.normalize_search("Çiçek") == C.normalize_search("çiçek") == "çiçek"
    assert C.normalize_search("İyi") == C.normalize_search("iyi") == "iyi"
    assert C.normalize_search("Işık") == C.normalize_search("ışık") == C.normalize_search("IŞIK") == "işik"   # capital I lowers to i: ı/i are search-equivalent
    assert C.normalize_search("ağaç") == "ağaç" and C.normalize_search("Şeker") == "şeker" and C.normalize_search("gitmek") == "gitmek"
    assert not C.answer_equal("ışık", "işik")                                             # spelling checks stay strict
    # the circumflex is search-folded too: most people type kağıt / dükkan / resmi, the data spells them the TDK way
    assert C.normalize_search("kâğıt") == C.normalize_search("Kağıt") == "kağit" and C.normalize_search("dükkân") == "duekkan"
    assert C.normalize_search("resmî") == "resmi" and C.normalize_search("ÂŞIK") == "aşik" and C.normalize_search("sükûnet") == "suekunet"
    assert not C.answer_equal("kâğıt", "kağıt")


def test_senses_and_builtin_turkish_glosses_are_searchable():
    # a slash separates senses ("-de/-da") but never inside a "(qualifier)": "ona (erkek/nesne)" is one sense, "ona" its bare form
    assert D._senses("ona (erkek, nesne)") == ["ona erkek nesne", "ona"] == D._senses("ona (erkek/nesne)")
    assert D._senses("-de/-da; içinde") == ["-de", "-da", "içinde"] and D._senses("craze; fad") == ["craze", "fad"]
    if not D.HAS_TR:
        return
    d = D.Dictionary(D.builtin_entries()); tr2t = f"tr2{T}"
    glosses = [(e, e.tr) for e in d.entries if e.tr]
    assert glosses and not any(re.search(r"\([^)]*/[^)]*\)", tr) for _e, tr in glosses)           # qualifiers use commas, never slashes
    plain = str.maketrans("âîû", "aiu")
    for e, tr in glosses:                                                                        # every circumflex gloss is reachable both ways
        for sense in (s.strip() for s in tr.split(";")):
            if sense != sense.translate(plain):
                assert e in d.lookup(sense.translate(plain), tr2t)[1] and e in d.lookup(sense, tr2t)[1], (e.headword, sense)
    if T == "de":
        assert [e.headword for e in d.lookup("mekanisyen", tr2t)[1]] == ["Mechaniker"] and d.lookup("makinist", tr2t)[1] == []
        assert d.lookup("nesne", tr2t)[1][0].headword == "Ding" and d.lookup("ona", tr2t)[1][0].headword == "ihm"
        assert {e.headword for e in d.lookup("imkan", tr2t)[1]} >= {"Möglichkeit", "unmöglich"}
        assert d.lookup("şikayet etmek", tr2t)[1][0].headword == "sich beschweren" and d.lookup("dükkan", tr2t)[1][0].headword in ("Laden", "Geschäft")


# ---------------------------------------------------------------------------
# Data model: built-in line format and CSV
# ---------------------------------------------------------------------------
def test_parse_line_with_and_without_the_turkish_field():
    if D.HAS_TR:
        assert D.LINE_TAIL == ("note", "tr")
        e = D.parse_line("Haus|n das Häuser|house; home|a note|ev; hane")
        assert (e.headword, e.pos, e.extra, e.translation, e.note, e.tr) == ("Haus", "n", "das Häuser", "house; home", "a note", "ev; hane")
        assert D.parse_line("Haus|n das Häuser|house|a note").tr == "" and D.parse_line("Haus|n das Häuser|house||ev").note == ""
        assert D.parse_line("Haus|n das Häuser|house||ev").tr == "ev"
    else:
        assert D.LINE_TAIL == ("note",)
        e = D.parse_line("house|n /haʊs/|ev; hane|a building for living in")
        assert (e.translation, e.note, e.tr) == ("ev; hane", "a building for living in", "")
    plain = D.parse_line("x|n|y")
    assert plain.tr == "" and plain.note == "" and plain.source == D.SOURCE_BUILTIN
    assert D.Entry("x", "n", "", "y").tr == ""                                     # positional construction still works
    assert all(hasattr(e, "tr") for e in D.builtin_entries()[:5])


def test_csv_roundtrip_with_turkish_and_old_layouts(tmp_path):
    entries = [D.Entry(HOUSE, "n", SAMPLE[0][2], SAMPLE[0][3], "note", D.SOURCE_AI, "Example.", SAMPLE[0][4]),
               D.Entry(CHAIR, "n", SAMPLE[2][2], SAMPLE[2][3])]
    out = tmp_path / "out.csv"
    assert D.write_table(out, entries) == 2
    header = out.read_text(encoding="utf-8").splitlines()[0]
    assert ("tr" in header.split(",")) is D.HAS_TR and header.startswith("headword,translation,pos,extra,note,source,example")
    back = D.read_table(out)
    assert [(e.headword, e.translation, e.tr, e.example, e.note) for e in back] == [(e.headword, e.translation, e.tr, e.example, e.note) for e in entries]
    assert all(e.source == D.SOURCE_USER for e in back)
    # old layout with header (no tr column) and without header
    old = tmp_path / "old.csv"
    old.write_text("headword,translation,pos,extra,note,source,example\nalpha,first,n,x,a note,ai,Alpha!\nbeta,second\n", encoding="utf-8")
    rows = D.read_table(old)
    assert [(e.headword, e.translation, e.pos, e.extra, e.note, e.example, e.tr) for e in rows] == [("alpha", "first", "n", "x", "a note", "Alpha!", ""), ("beta", "second", "", "", "", "", "")]
    bare = tmp_path / "bare.tsv"; bare.write_text("gamma\tthird\tv\n", encoding="utf-8")
    assert [(e.headword, e.translation, e.pos, e.tr) for e in D.read_table(bare)] == [("gamma", "third", "v", "")]
    if D.HAS_TR:
        # header-aware: columns in any order, localised names accepted, headerless new layout reads tr as the last column
        mixed = tmp_path / "mixed.csv"
        mixed.write_text(f"Türkçe,{C.TARGET_LANG_NAME},English,pos\nev,Haus,house,n\n,Baum,tree,n\n", encoding="utf-8")
        assert [(e.headword, e.translation, e.tr, e.pos) for e in D.read_table(mixed)] == [("Haus", "house", "ev", "n"), ("Baum", "tree", "", "n")]
        nohead = tmp_path / "nohead.csv"; nohead.write_text("Haus,house,n,das Häuser,,user,,ev\n", encoding="utf-8")
        assert D.read_table(nohead)[0].tr == "ev"


# ---------------------------------------------------------------------------
# Lookup per direction
# ---------------------------------------------------------------------------
def test_fixed_directions_search_only_their_source_side(dic):
    other = D.OTHER_LANG
    t2o, o2t = f"{T}2{other}", f"{other}2{T}"
    assert dic.lookup(HOUSE, t2o) == (t2o, [dic.entries[0]]) and dic.lookup("house" if other == "en" else "ev", t2o)[1] == []
    assert dic.lookup("house" if other == "en" else "ev", o2t)[0] == o2t and dic.lookup("house" if other == "en" else "ev", o2t)[1][0].headword == HOUSE
    assert dic.lookup(HOUSE, o2t) == (o2t, [])                                        # a headword is not searched in the other language
    assert dic.lookup("", o2t) == (o2t, []) and dic.lookup("zzz", t2o) == (t2o, [])   # a fixed code is echoed even without results
    assert len(dic.lookup(HOUSE[0].lower(), 1)[1]) == 1 == len(dic.lookup(HOUSE[0].lower(), "auto", 1)[1])   # old positional limit still works
    assert dic.lookup(HOUSE.upper(), t2o)[1][0].headword == HOUSE                     # case-insensitive
    assert dic.lookup(HOUSE, "bogus")[0] == D.DEFAULT_DIRECTION                       # unknown code -> auto
    if not D.HAS_TR:
        assert dic.lookup("gitmek", "tr2en")[1][0].headword == GO and dic.lookup("go", "tr2en")[1] == []
        return
    t2tr, tr2t = f"{T}2tr", f"tr2{T}"
    direction, rows = dic.lookup(HOUSE, t2tr)
    assert direction == t2tr and rows[0].headword == HOUSE and rows[0].tr == "ev; hane"
    assert dic.lookup(CHAIR, t2tr)[1][0].tr == ""                                     # entries without a gloss are still found (the AI fills them)
    assert dic.lookup("ev", t2tr)[1] == [] and dic.lookup("house", t2tr)[1] == []
    assert dic.lookup("ev", tr2t) == (tr2t, [dic.entries[0]]) and dic.lookup("hane", tr2t)[1][0].headword == HOUSE
    assert dic.lookup("ağaç", tr2t)[1][0].headword == TREE and dic.lookup("AĞAÇ", tr2t)[1][0].headword == TREE
    assert dic.lookup("gitmek", tr2t)[1][0].headword == GO and dic.lookup("yürümek", tr2t)[1][0].headword == GO
    assert dic.lookup("house", tr2t)[1] == [] and dic.lookup(HOUSE, tr2t)[1] == [] and dic.lookup("chair", tr2t)[1] == []
    assert dic.lookup("gitmek", "en2" + T)[1] == []


def test_auto_direction_detects_the_query_language(dic):
    other = D.OTHER_LANG
    assert dic.lookup(HOUSE)[0] == f"{T}2{other}" and dic.lookup(HOUSE, "auto")[1][0].headword == HOUSE
    assert dic.lookup("house" if other == "en" else "ev")[0] == f"{other}2{T}"
    assert dic.lookup("")[0] == D.DEFAULT_DIRECTION and dic.lookup("zzqq")[0] == D.DEFAULT_DIRECTION
    if not D.HAS_TR:
        assert dic.lookup("gitmek")[0] == "tr2en" and dic.lookup("gitmek")[1][0].headword == GO
        return
    direction, rows = dic.lookup("ev")
    assert direction == f"tr2{T}" and rows[0].headword == HOUSE
    assert dic.lookup("ağaç")[0] == f"tr2{T}" and dic.lookup("ağaç")[1][0].headword == TREE
    assert dic.lookup("gitmek")[0] == f"tr2{T}" and dic.lookup("gitmek")[1][0].headword == GO
    assert dic.lookup("to go")[0] == f"en2{T}"
    # a form that is both an English and a Turkish sense: English wins the tie, the entry is listed once
    dic.extend([D.Entry("Zzqqxx", "n", "", "park", "", D.SOURCE_USER, "", "park")])
    direction, rows = dic.lookup("park")
    assert direction == f"en2{T}" and [e.headword for e in rows] == ["Zzqqxx"]
    # a headword hit always beats the other sides (ties go to the headword)
    dic.extend([D.Entry("Park", "n", "der Parks", "park", "", D.SOURCE_USER, "", "park")])
    direction, rows = dic.lookup("park")
    assert direction == f"{T}2{other}" and rows[0].headword == "Park"


def test_extend_merges_a_turkish_gloss_into_an_existing_twin():
    base = D.Entry(HOUSE, "n", SAMPLE[0][2], SAMPLE[0][3])
    dic = D.Dictionary([base])
    ai = D.Entry(HOUSE, "n", "", SAMPLE[0][3], "", D.SOURCE_AI, "", "ev")
    assert dic.would_change(ai) is D.HAS_TR and dic.contains(ai) and dic.twin(ai) is base
    assert dic.extend([ai]) == 0 and len(dic) == 1
    twin = dic.twin(ai)
    assert twin.source == D.SOURCE_BUILTIN and twin.tr == ("ev" if D.HAS_TR else "")   # source kept, gloss merged
    assert dic.would_change(ai) is False and dic.would_change(D.Entry("new", "n", "", "x")) is True
    # an AI entry with an extra Turkish sense appends it - never overwrites - and a repeated sense changes nothing
    more = D.Entry(HOUSE, "n", "", SAMPLE[0][3], "", D.SOURCE_AI, "", "hane; ev")
    assert dic.would_change(more) is D.HAS_TR and dic.extend([more]) == 0 and len(dic) == 1
    assert dic.twin(ai).tr == ("ev; hane" if D.HAS_TR else "") and dic.would_change(more) is False and dic.merge_tr(dic.twin(ai), ai) == dic.twin(ai).tr
    # a user entry's gloss replaces the stored one, also for a built-in entry (the source is kept); an empty user gloss leaves it
    mine = D.Entry(HOUSE, "n", "", SAMPLE[0][3], "", D.SOURCE_USER, "", "konut")
    assert dic.would_change(mine) is D.HAS_TR and dic.extend([mine]) == 0 and dic.twin(ai).tr == ("konut" if D.HAS_TR else "")
    assert dic.twin(ai).source == D.SOURCE_BUILTIN and dic.would_change(mine) is False
    assert dic.extend([D.Entry(HOUSE, "n", "", SAMPLE[0][3], "", D.SOURCE_USER)]) == 0 and dic.twin(ai).tr == ("konut" if D.HAS_TR else "")
    assert dic.set_tr(base, "ev") and dic.twin(ai).tr == "ev"
    updated = dic.set_tr(base, "konut")
    assert updated.tr == "konut" and dic.entries[0].tr == "konut" and dic.set_tr(D.Entry("nope", "n", "", "x"), "y") is None
    assert dic.find(HOUSE, "n") == [dic.entries[0]] and dic.find(HOUSE, "v") == [] and dic.has_headword(HOUSE)
    dic.remove_source(D.SOURCE_USER); assert len(dic) == 1 and dic.entries[0].tr == "konut"


def test_build_dictionary_maps_the_tr_column():
    d = D.build_dictionary([("Zzqqxx", "zzq-thing", "n", "", "", "ai", "", "zzq-şey"), ("Qqzz", "qqz-fence", "n", "", "", "user", "")])
    assert d.lookup("Zzqqxx")[1][0].tr == "zzq-şey" and d.lookup("Qqzz")[1][0].tr == ""
    if D.HAS_TR:
        direction, rows = d.lookup("zzq-şey", f"tr2{T}")
        assert direction == f"tr2{T}" and rows[0].headword == "Zzqqxx"


# ---------------------------------------------------------------------------
# AI: prompt keys and parser
# ---------------------------------------------------------------------------
def test_ai_prompt_asks_for_english_and_turkish():
    prompt = D.ai_prompt("x", "tr")
    if D.HAS_TR:
        assert "translation_en" in prompt and "translation_tr" in prompt and "Turkish" in prompt
    else:
        assert '"translation"' in prompt and "translation_en" not in prompt and "Turkish" in prompt


def test_parse_ai_entries_accepts_translation_en_tr_and_legacy_translation():
    rows = D.parse_ai_entries(json.dumps([
        {"headword": "Aaa", "pos": "n", "extra": "", "translation_en": "house; home", "translation_tr": "ev; hane; ev"},
        {"headword": "Bbb", "pos": "n", "extra": "", "translation": "tree"},
        {"headword": "Ccc", "pos": "n", "extra": "", "translation": "old", "translation_en": "new", "translation_tr": ["ağaç", "ağac"]},
        {"headword": "Ddd", "pos": "n", "extra": "", "translation_tr": "only turkish"},
    ]))
    by = {e.headword: e for e in rows}
    assert by["Bbb"].translation == "tree" and by["Bbb"].tr == ""
    assert by["Ccc"].translation == "new"                                            # translation_en beats the legacy key
    if D.HAS_TR:
        assert by["Aaa"].translation == "house; home" and by["Aaa"].tr == "ev; hane"     # Turkish senses deduplicated too
        assert by["Ccc"].tr == "ağaç; ağac" and "Ddd" not in by                         # English is required
        long = D.parse_ai_entries(json.dumps([{"headword": "x", "translation_en": "y", "translation_tr": "z" * 500}]))[0]
        assert len(long.tr) <= 200
    else:
        assert by["Aaa"].translation == "house; home" and by["Aaa"].tr == ""
        assert by["Ddd"].translation == "only turkish"                                  # the English app's translation is Turkish anyway


# ---------------------------------------------------------------------------
# SQLite: tr column migration and repo
# ---------------------------------------------------------------------------
V112_DICT_SCHEMA = """
CREATE TABLE dict_entries(
 id INTEGER PRIMARY KEY, headword TEXT NOT NULL, translation TEXT NOT NULL,
 pos TEXT NOT NULL DEFAULT '', extra TEXT NOT NULL DEFAULT '', note TEXT NOT NULL DEFAULT '',
 source TEXT NOT NULL DEFAULT 'user', example TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, UNIQUE(headword, translation));
"""


def test_dict_entries_gets_a_tr_column_on_old_databases(tmp_path):
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.executescript(V112_DICT_SCHEMA)
    old.execute("INSERT INTO dict_entries(headword,translation,pos,extra,note,source,example) VALUES('Brezel','pretzel','n','die Brezeln','','ai','Eine Brezel.')")
    old.execute("INSERT INTO dict_entries(headword,translation,pos) VALUES('Semmel','bread roll','n')")
    old.commit(); old.close()
    db = Database(path); repos = Repos(db)
    assert "tr" in {r[1] for r in db.query("PRAGMA table_info(dict_entries)")}
    rows = repos.dictionary.all()
    assert [(r["headword"], r["source"], r["example"], r["tr"]) for r in rows] == [("Brezel", "ai", "Eine Brezel.", ""), ("Semmel", "user", "", "")]
    assert repos.dictionary.set_tr("Brezel", "pretzel", " simit ") is True and repos.dictionary.set_tr("Brezel", "other", "x") is False
    assert repos.dictionary.add("Kipferl", "croissant", "n", "das Kipferl", "", "ai", "", "ay çöreği") == 1
    assert repos.dictionary.add_many([("Semmel", "bread roll", "n", "", "", "", "sandviç ekmeği")]) == 0     # UNIQUE(headword, translation): no second row …
    assert repos.dictionary.count() == 3
    by = {r["headword"]: r["tr"] for r in repos.dictionary.all()}
    assert by == {"Brezel": "simit", "Kipferl": "ay çöreği", "Semmel": "sandviç ekmeği"}                       # … but the user's gloss replaces the stored one
    assert repos.dictionary.add_many([("Semmel", "bread roll", "n")]) == 0 and repos.dictionary.add_many([("Semmel", "bread roll", "n", "", "", "", "x")], "ai") == 0
    assert {r["headword"]: (r["tr"], r["source"]) for r in repos.dictionary.all()}["Semmel"] == ("sandviç ekmeği", "user")   # an empty user gloss or an AI duplicate leaves it
    d = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r["source"], r["example"], r["tr"]) for r in repos.dictionary.all()])
    assert d.lookup("Brezel")[1][0].tr == "simit" and d.lookup("Kipferl")[1][0].source == D.SOURCE_AI
    assert Database(path).query("PRAGMA table_info(dict_entries)")                    # reopening is idempotent
    db.close()
