import json
import time
import tkinter as tk
from types import SimpleNamespace

import pytest

from gca import config as C
from gca import secrets
from gca.app import App, TAB_SPECS


@pytest.fixture(scope="module")
def app():
    try: instance = App()
    except tk.TclError: pytest.skip("No Windows display")
    instance.withdraw(); instance.update(); yield instance; instance.on_close()


def test_window_opens_and_all_tabs_build(app):
    assert len(app._tabs) == len(TAB_SPECS) == 18
    for key, _cls, _icon, _group in TAB_SPECS:
        app.select(key); app.update(); assert app.current_page().winfo_exists()


def test_language_switch_is_immediate_and_persistent(app):
    app.select("tab.study"); app.set_ui_language("en"); app.update()
    assert app.page_title.cget("text") == "Spaced Review" and app.language_var.get() == "English"
    assert C.load_settings()["ui_lang"] == "en"
    app.set_ui_language("de"); app.update()
    assert app.page_title.cget("text") == "Wiederholen" and app.language_var.get() == "Deutsch"


def test_card_session_can_complete(app):
    app.set_ui_language("tr"); app.select("tab.study"); tab = app.current_page(); tab.limit.set(5); tab.start("new")
    assert len(tab.session) == 5
    for _ in range(5): tab.reveal(); tab.grade(4); app.update()
    assert tab.session == []


def test_exam_can_generate_and_finish(app):
    app.select("tab.exam"); tab = app.current_page(); tab.count.set(5); tab.start(); assert len(tab.questions) == 5
    while tab.idx < len(tab.questions):
        tab.choice.set(tab.questions[tab.idx].answer); tab.submit(); app.update()
    row = app.repos.db.one("SELECT score FROM exams WHERE id=?", (tab.exam_id,)); assert row["score"] == 100.0


def test_ai_offline_page_does_not_crash(app):
    app.settings["ai_enabled"] = False; app.select("tab.ai"); tab = app.current_page(); tab.input.insert("1.0", "Test"); tab.send(); app.update()
    assert app.t("ai.status_off") in tab.output.get("1.0", "end")


def _pump(app, predicate, timeout=10.0):
    """Run the Tk event loop until ``predicate()`` holds (background AI work lands via app.run_async)."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        app.update()
        if predicate(): return True
        time.sleep(0.05)
    return False


def _ai_rows(tab):
    return [i for i in tab.tree.get_children() if tab.tree.set(i, "src") == tab.t("dict.ai_source")]


def test_dictionary_falls_back_to_ai_and_caches_results(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    assert tab.policy.get() == app.t("dict.ai_local")
    tab.query.set("zzqqxxbrotzeit"); tab.search()
    assert app.t("dict.ai_asking") in tab.ai_out.get("1.0", "end")
    assert _pump(app, lambda: _ai_rows(tab)), "AI results did not arrive"
    entry = tab.current(); sample = mock_ai.sample[0]
    assert entry is not None and entry.source == "ai" and entry.headword == sample["headword"]
    assert sample["translation"].split("; ")[0] in tab.w_trans.cget("text") and sample["example"] in tab.w_example.cget("text")
    assert tab.w_note.cget("text") == sample["note"] and app.t("dict.ai_source") in tab.w_meta.cget("text")
    out = tab.ai_out.get("1.0", "end")
    assert app.t("dict.answered_by") in out and mock_ai.MODEL in out and app.t("dict.ai_local") in out and sample["headword"] in out
    assert mock_ai.count("/chat/completions") == 1 and mock_ai.chats[-1]["auth"] == ""
    assert not tab.save_btn.winfo_manager()                                          # autosaved -> no extra button
    # cached: persisted with source "ai", instantly found offline next time, no second request
    assert app.repos.dictionary.count("ai") >= 1 and any(r["source"] == "ai" and r["example"] == sample["example"] for r in app.repos.dictionary.all())
    tab.query.set(sample["headword"]); tab.search(); app.update()
    assert tab.current().source == "ai" and mock_ai.count("/chat/completions") == 1
    assert _pump(app, lambda: tab.ai_state.cget("text") == app.t("dict.state_local"), 5)
    # "Ask AI" merges AI entries on top of local hits and works for word-bank export with the example sentence
    tab.query.set({"de": "Haus", "fr": "maison", "en": "house"}[C.TARGET_LANG]); tab.search(); app.update()
    assert tab.current().source == "builtin"
    tab.ask_ai(); assert _pump(app, lambda: mock_ai.count("/chat/completions") == 2 and _ai_rows(tab))
    assert tab.tree.get_children()[0] in _ai_rows(tab) and len(tab.results) > len(mock_ai.sample)
    tab.add_to_bank(); word = app.repos.words.search(sample["headword"])[0]
    assert word["example_target"] == sample["example"]


def test_dictionary_policy_off_makes_no_ai_request(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "off"}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    assert tab.policy.get() == app.t("dict.ai_off") and tab.ai_state.cget("text") == app.t("dict.state_off")
    tab.query.set("qqzzxxnothing"); tab.search()
    _pump(app, lambda: False, 1.0)
    assert mock_ai.count("/chat/completions") == 0 and tab.tree.get_children() == ()
    assert app.t("dict.no_result") in tab.ai_out.get("1.0", "end")
    tab.ask_ai(); app.update()
    assert app.t("ai.status_off") in tab.ai_out.get("1.0", "end") and mock_ai.count() == 0
    # unreachable local provider: offline text, no crash, no hang
    app.settings.update({"dict_ai": "local", "ai_base": "http://127.0.0.1:9"}); app.refresh_ai_clients()
    tab.query.set("qqzzxxnothing"); tab.search()
    assert _pump(app, lambda: app.t("ai.status_off") in tab.ai_out.get("1.0", "end"), 5)
    tab.policy.set(app.t("dict.ai_auto")); tab._policy_changed()
    assert C.load_settings()["dict_ai"] == "auto"


def test_settings_alt_endpoint_keeps_key_out_of_settings_and_drives_dictionary(app, mock_ai):
    app.select("tab.settings"); tab = app.current_page(); app.update()
    assert tab.key_state.cget("text") == app.t("settings.alt_key_none")
    tab.alt_enabled.set(True); tab.alt_base.set(mock_ai.base); tab.alt_model.set(mock_ai.MODEL); tab.alt_key.set("nvapi-ui-secret")
    tab.dict_ai.set(app.t("dict.ai_alt")); tab.dict_autosave.set(False); tab.save(); app.update()
    assert "nvapi-ui-secret" not in C.SETTINGS_PATH.read_text(encoding="utf-8")
    assert secrets.get_secret("alt_api_key") == "nvapi-ui-secret" and tab.alt_key.get() == ""
    assert tab.key_state.cget("text") == app.t("settings.alt_key_saved")
    assert app.ai_alt.api_key == "nvapi-ui-secret" and app.ai_alt.base == mock_ai.base and app.ai_alt.model == mock_ai.MODEL
    assert C.load_settings()["dict_ai"] == "alt" and C.load_settings()["alt_enabled"] is True
    tab.test_alt(); assert _pump(app, lambda: app.t("settings.alt_ok") in tab.alt_result.cget("text"), 5)
    assert mock_ai.requests[-1]["auth"] == "Bearer nvapi-ui-secret"
    # dictionary now answers through the alternative client with the bearer key; autosave off -> "Save" button
    app.select("tab.dictionary"); dtab = app.current_page(); app.update()
    assert dtab.policy.get() == app.t("dict.ai_alt")
    mock_ai.content = '```json\n[{"headword": "Qqzzalt", "pos": "n", "extra": "", "translation": "alt-thing", "example": "Qqzzalt!", "note": ""}]\n```'
    dtab.query.set("qqzzalt"); dtab.search()
    assert _pump(app, lambda: _ai_rows(dtab))
    assert mock_ai.chats[-1]["auth"] == "Bearer nvapi-ui-secret" and mock_ai.chats[-1]["body"]["model"] == mock_ai.MODEL
    assert dtab.current().headword == "Qqzzalt" and dtab.current().source == "ai"
    assert app.t("dict.ai_alt") in dtab.ai_out.get("1.0", "end") and dtab.save_btn.winfo_manager()   # autosave off -> not stored yet
    before = app.repos.dictionary.count("ai"); dtab.save_ai_entry(); app.update()
    assert app.repos.dictionary.count("ai") == before + 1 and not dtab.save_btn.winfo_manager()
    assert any(r["headword"] == "Qqzzalt" and r["source"] == "ai" and r["example"] == "Qqzzalt!" for r in app.repos.dictionary.all())
    app.select("tab.settings"); tab = app.current_page(); tab.delete_key(); app.update()
    assert secrets.get_secret("alt_api_key") == "" and app.ai_alt.api_key == "" and tab.key_state.cget("text") == app.t("settings.alt_key_none")
    app.settings.update({"alt_enabled": False, "dict_ai": "auto", "dict_ai_autosave": True}); C.save_settings(app.settings)


def _entry_json(head, translation, pos="n"):
    return json.dumps([{"headword": head, "pos": pos, "extra": "", "translation": translation, "example": f"{head}!", "note": ""}])


def _word():
    return {"de": "Haus", "fr": "maison", "en": "house"}[C.TARGET_LANG]


def test_dictionary_pending_ai_answer_survives_key_releases_and_is_cached_when_superseded(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True, "alt_enabled": False}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    answer = {"text": ""}
    def slow(_body): time.sleep(0.5); return answer["text"]                       # slow enough to touch the keyboard meanwhile
    mock_ai.content = slow; asking = app.t("dict.ai_asking"); before = app.repos.dictionary.count("ai")
    # 1. modifier / cursor keys released while the answer is pending must not cancel it
    answer["text"] = _entry_json("Qqzzpending", "pending-thing")
    tab.query.set("qqzzpending"); tab.search()
    for keysym in ("Shift_L", "Control_L", "Left", "End", "Escape"): tab._on_key(SimpleNamespace(keysym=keysym))
    assert _pump(app, lambda: _ai_rows(tab)), "AI answer was discarded by a key release"
    assert tab.current().headword == "Qqzzpending" and mock_ai.count("/chat/completions") == 1
    assert app.repos.dictionary.count("ai") == before + 1 and asking not in tab.ai_out.get("1.0", "end") and app.status.get() != asking
    # 2. a newer explicit search supersedes the pending answer: still cached, the list stays with the new query, nothing stuck on "asking"
    answer["text"] = _entry_json("Qqzzstale", "stale-thing")
    tab.query.set("qqzzstale"); tab.search()
    tab.query.set(_word()); tab.search(); app.update()
    assert tab.current().source == "builtin" and asking in tab.ai_out.get("1.0", "end")
    assert _pump(app, lambda: app.repos.dictionary.count("ai") == before + 2), "superseded answer was not cached"
    assert tab.current().source == "builtin" and all(tab.tree.set(i, "head") != "Qqzzstale" for i in tab.tree.get_children())
    assert tab.dict.lookup("Qqzzstale")[1][0].source == "ai"
    assert _pump(app, lambda: "Qqzzstale" in tab.ai_out.get("1.0", "end"), 2) and app.status.get() != asking
    # 3. fixing a typo while the answer is pending: the freshly cached entry shows up for the corrected text
    answer["text"] = _entry_json("Qqzztypo", "typo-thing")
    tab.query.set("qqzztypoo"); tab.search()
    tab.query.set("qqzztypo"); tab._on_key(SimpleNamespace(keysym="BackSpace")); app.update()
    assert tab.tree.get_children() == ()
    assert _pump(app, lambda: _ai_rows(tab)) and tab.results[0].headword == "Qqzztypo" and asking not in tab.ai_out.get("1.0", "end")
    assert app.repos.dictionary.count("ai") == before + 3 and app.status.get() != asking


def test_settings_page_reflects_settings_changed_elsewhere_before_saving(app):
    app.settings.update({"dict_ai": "auto", "dict_ai_autosave": True}); C.save_settings(app.settings)
    app.select("tab.dictionary"); dtab = app.current_page(); app.update()
    dtab.policy.set(app.t("dict.ai_off")); dtab._policy_changed()                        # toolbar change, saved immediately
    assert app.settings["dict_ai"] == "off" and C.load_settings()["dict_ai"] == "off"
    app.settings.update({"dict_ai_autosave": False, "ai_base": "http://127.0.0.1:9"})      # changed elsewhere after the page was built
    app.select("tab.settings"); stab = app.current_page(); app.update()
    assert stab.dict_ai.get() == app.t("dict.ai_off") and stab.dict_autosave.get() is False and stab.base.get() == "http://127.0.0.1:9"
    stab.goal.set(33); stab.save(); app.update()                                           # saving something else keeps the toolbar's choice
    assert app.settings["dict_ai"] == "off" and app.settings["dict_ai_autosave"] is False and app.settings["daily_goal"] == 33
    assert C.load_settings()["dict_ai"] == "off" and app.ai.base == "http://127.0.0.1:9"
    app.select("tab.dictionary"); app.update(); assert dtab.policy.get() == app.t("dict.ai_off")
    app.settings.update({"dict_ai": "auto", "dict_ai_autosave": True, "daily_goal": 20}); C.save_settings(app.settings)


def test_ask_ai_on_a_known_word_lists_but_never_accumulates_ai_duplicates(app, mock_ai):
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True, "alt_enabled": False}); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    word = _word(); db_before, mem_before = app.repos.dictionary.count("ai"), len(tab.dict)
    tab.query.set(word); tab.search(); app.update(); local = len(tab.results)
    for i, translation in enumerate(("house; home", "house; home; building"), 1):          # the model rephrases on every call
        mock_ai.content = _entry_json(word, translation)
        tab.ask_ai(); assert _pump(app, lambda: mock_ai.count("/chat/completions") == i and tab.current() is not None and tab.current().translation == translation)
        assert tab.current().source == "ai" and tab.tree.get_children()[0] in _ai_rows(tab) and len(tab.results) == local + 1
        assert tab.save_btn.winfo_manager()                                                # listed with a "Save" button, not stored
    assert app.repos.dictionary.count("ai") == db_before and len(tab.dict) == mem_before
    tab.save_ai_entry(); app.update()                                                      # an explicit save still works
    assert app.repos.dictionary.count("ai") == db_before + 1 and tab.dict.contains(tab.current()) and not tab.save_btn.winfo_manager()
    # a fallback answer that merely restates a known headword is listed but not cached; genuinely new headwords are
    mock_ai.content = json.dumps(json.loads(_entry_json(word, "house; dwelling")) + json.loads(_entry_json("Qqzznovel", "novel-thing")))
    tab.query.set("qqzznovel"); tab.search(); assert _pump(app, lambda: len(_ai_rows(tab)) == 2)
    assert app.repos.dictionary.count("ai") == db_before + 2 and tab.dict.lookup("Qqzznovel")[1][0].source == "ai"
    assert not any(r["translation"] == "house; dwelling" for r in app.repos.dictionary.all())
    assert tab.current().translation == "house; dwelling" and tab.save_btn.winfo_manager()


def _cols(tab):
    value = tab.tree.cget("displaycolumns")
    return tuple(value) if isinstance(value, (tuple, list)) else tuple(str(value).split())


def test_dictionary_direction_selector_reruns_search_persists_and_fills_turkish(app, mock_ai):
    from gca import dictionary as D
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "off", "dict_ai_autosave": True, "alt_enabled": False, "dict_direction": "auto"})
    C.save_settings(app.settings); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    word, target, other = _word(), C.TARGET_LANG, D.OTHER_LANG
    t2o, o2t = f"{target}2{other}", f"{other}2{target}"
    assert tab.direction.get() == app.t("dict.dir_auto") and set(tab.direction_box.cget("values")) == set(tab._direction_labels.values())
    assert _cols(tab)[:2] == ("head", "trans") and ("tr" in _cols(tab)) is D.HAS_TR
    tab.query.set(word); tab.search(); app.update()
    assert tab.dir_label.cget("text") == f"{target.upper()} → {other.upper()}" and tab.current().headword == word
    assert tab.w_trans.cget("text").startswith(app.t("dict.translation") + ":") and (tab.w_tr.winfo_manager() != "") is D.HAS_TR
    # switching the combobox re-runs the query in the fixed direction, updates the label and persists the setting
    tab.direction.set(tab._direction_labels[o2t]); tab._direction_changed(); app.update()
    assert app.settings["dict_direction"] == o2t and C.load_settings()["dict_direction"] == o2t
    assert tab.dir_label.cget("text") == D.direction_text(o2t) == f"{other.upper()} → {target.upper()}"
    assert tab.tree.get_children() == () and app.t("dict.no_result") in tab.ai_out.get("1.0", "end") and mock_ai.count() == 0   # only the source side is searched; AI off
    tab.direction.set(tab._direction_labels[t2o]); tab._direction_changed(); app.update()
    assert C.load_settings()["dict_direction"] == t2o and tab.dir_label.cget("text") == D.direction_text(t2o) and tab.current().headword == word
    app.settings["dict_direction"] = "auto"; C.save_settings(app.settings); app.select("tab.settings"); app.select("tab.dictionary"); app.update()
    assert tab.direction.get() == app.t("dict.dir_auto")                                   # picked up on show, like the AI policy
    if not D.HAS_TR:
        return
    # a *2tr search that finds an entry without a Turkish gloss asks the AI and writes the gloss into that entry (no duplicate).
    # The query is always set before the direction is switched: switching re-runs whatever query is in the box.
    t2tr, tr2t = f"{target}2tr", f"tr2{target}"
    app.repos.dictionary.add("Qqzzhaus", "qqzz-house", "n", "", "", "user", ""); tab.dict.extend([D.Entry("Qqzzhaus", "n", "", "qqzz-house", "", D.SOURCE_USER)])
    app.settings["dict_ai"] = "local"; C.save_settings(app.settings); tab.on_show()
    mock_ai.content = json.dumps([{"headword": "Qqzzhaus", "pos": "n", "extra": "", "translation_en": "qqzz-house", "translation_tr": "qqzz-ev; qqzz-hane", "example": "", "note": ""}])
    tab.query.set("Qqzzhaus"); tab.direction.set(tab._direction_labels[t2tr]); tab._direction_changed()
    first = tab.tree.get_children()[0]                                                       # synchronous part: listed with "—", AI pending
    assert _cols(tab)[:3] == ("head", "tr", "trans") and tab.tree.set(first, "tr") == "—" and app.status.get() == app.t("dict.tr_missing")
    assert tab.w_tr.cget("text") == f"{app.t('dict.turkish')}: —" and tab.dir_label.cget("text") == D.direction_text(t2tr)
    assert _pump(app, lambda: tab.current() is not None and tab.current().tr == "qqzz-ev; qqzz-hane"), "Turkish gloss was not filled"
    assert mock_ai.count("/chat/completions") == 1 and tab.current().source == "user" and not _ai_rows(tab) and not tab.save_btn.winfo_manager()
    rows = [r for r in app.repos.dictionary.all() if r["headword"] == "Qqzzhaus"]
    assert [(r["source"], r["tr"]) for r in rows] == [("user", "qqzz-ev; qqzz-hane")]           # updated in place, not duplicated
    assert tab.tree.set(tab.tree.get_children()[0], "tr") == "qqzz-ev; qqzz-hane" and "qqzz-ev" in tab.w_tr.cget("text")
    assert app.t("dict.tr_filled") in app.status.get() and app.t("dict.turkish") in tab.ai_out.get("1.0", "end") and "qqzz-hane" in tab.ai_out.get("1.0", "end")
    tab.query.set("qqzz-hane"); tab.direction.set(tab._direction_labels[tr2t]); tab._direction_changed(); app.update()
    assert tab.dir_label.cget("text") == D.direction_text(tr2t) and tab.current().headword == "Qqzzhaus" and mock_ai.count("/chat/completions") == 1
    tab.add_to_bank(); bank = app.repos.words.search("Qqzzhaus")[0]
    assert bank["tr"] == "qqzz-ev" and bank["en"] == "qqzz-house"                                # first Turkish sense feeds the word bank
    # a *2tr search on an entry that already has its gloss never asks the AI
    tab.query.set("Qqzzhaus"); tab.direction.set(tab._direction_labels[t2tr]); tab._direction_changed(); _pump(app, lambda: False, 0.5)
    assert mock_ai.count("/chat/completions") == 1 and tab.current().tr == "qqzz-ev; qqzz-hane"
    # autosave off: nothing is written until "Save", which then merges the gloss into the existing entry
    app.settings.update({"dict_ai_autosave": False, "dict_direction": "auto"}); C.save_settings(app.settings); tab.on_show()
    app.repos.dictionary.add("Qqzzbaum", "qqzz-tree", "n", "", "", "user", ""); tab.dict.extend([D.Entry("Qqzzbaum", "n", "", "qqzz-tree", "", D.SOURCE_USER)])
    mock_ai.content = json.dumps([{"headword": "Qqzzbaum", "pos": "n", "extra": "", "translation_en": "qqzz-tree", "translation_tr": "qqzz-ağaç", "example": "", "note": ""}])
    tab.query.set("Qqzzbaum"); tab.search(); app.update()
    assert tab.current().source == "user" and mock_ai.count("/chat/completions") == 1                 # auto never targets Turkish: no request
    tab.ask_ai()
    assert _pump(app, lambda: _ai_rows(tab)) and tab.current().source == "ai" and tab.save_btn.winfo_manager()
    assert [r["tr"] for r in app.repos.dictionary.all() if r["headword"] == "Qqzzbaum"] == [""] and tab.dict.twin(tab.current()).tr == ""
    before = app.repos.dictionary.count(); tab.save_ai_entry(); app.update()
    assert app.repos.dictionary.count() == before and [r["tr"] for r in app.repos.dictionary.all() if r["headword"] == "Qqzzbaum"] == ["qqzz-ağaç"]
    assert tab.current().source == "user" and tab.current().tr == "qqzz-ağaç" and not tab.save_btn.winfo_manager() and not _ai_rows(tab)
    # a built-in entry without a gloss (if any is left) is completed through an "ai" twin row that merges on the next start
    bare = next((e for e in tab.dict.entries if e.source == D.SOURCE_BUILTIN and not e.tr and len(tab.dict.find(e.headword)) == 1), None)
    if bare is not None:
        app.settings.update({"dict_ai_autosave": True, "dict_direction": t2tr}); C.save_settings(app.settings); tab.on_show()
        mock_ai.content = json.dumps([{"headword": bare.headword, "pos": bare.pos, "extra": bare.extra, "translation_en": bare.translation, "translation_tr": "qqzz-gloss"}])
        tab.query.set(bare.headword); tab.search()
        assert tab.current().headword == bare.headword and not tab.current().tr and app.status.get() == app.t("dict.tr_missing")
        assert _pump(app, lambda: tab.dict.twin(bare) is not None and tab.dict.twin(bare).tr == "qqzz-gloss")
        assert tab.dict.twin(bare).source == D.SOURCE_BUILTIN and tab.current().tr == "qqzz-gloss" and tab.current().source == D.SOURCE_BUILTIN
        assert any(r["headword"] == bare.headword and r["translation"] == bare.translation and r["source"] == "ai" and r["tr"] == "qqzz-gloss" for r in app.repos.dictionary.all())
        rebuilt = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r["source"], r["example"], r["tr"]) for r in app.repos.dictionary.all()])
        assert rebuilt.twin(bare).tr == "qqzz-gloss" and rebuilt.twin(bare).source == D.SOURCE_BUILTIN
    app.settings.update({"dict_ai": "auto", "dict_ai_autosave": True, "dict_direction": "auto"}); C.save_settings(app.settings)


def test_dictionary_random_word_and_history_find_known_words_in_every_direction(app, mock_ai, monkeypatch):
    from gca import dictionary as D
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True, "alt_enabled": False, "dict_direction": "auto"})
    C.save_settings(app.settings); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    word, target, other = _word(), C.TARGET_LANG, D.OTHER_LANG
    known = tab.dict.find(word)[0]; monkeypatch.setattr(tab.dict, "random_entry", lambda rng=None: known)
    for code in D.DIRECTIONS:                                # a random headword is always looked up on the headword side, never on the other language
        tab.query.set(""); tab.direction.set(tab._direction_labels[code]); tab._direction_changed(); app.update()
        tab.random_word(); _pump(app, lambda: False, 0.2)
        src = D.split_direction(code)[0]
        expected = code if code == "auto" or src == target else D.direction_code(target, src)
        assert tab.query.get() == word and tab.current() is not None and tab.current().headword == word and tab.current().source == "builtin", code
        assert tab.history[0] == (word, expected) and mock_ai.count("/chat/completions") == 0, code
        if code != "auto": assert tab.dir_label.cget("text") == D.direction_text(expected) and tab.direction.get() == tab._direction_labels[code]
    # history keeps the direction of a lookup; a direction switch re-runs the box's text on the other side (nothing, the AI is asked) ...
    app.settings["dict_direction"] = "auto"; tab.on_show(); tab.query.set(word); tab.search(); app.update()
    assert tab.history[0] == (word, "auto") and tab.dir_label.cget("text") == D.direction_text(D.DEFAULT_DIRECTION)
    o2t = f"{other}2{target}"; tab.direction.set(tab._direction_labels[o2t]); tab._direction_changed(); app.update()
    assert tab.tree.get_children() == () and tab.history[0] == (word, o2t) and _pump(app, lambda: mock_ai.count("/chat/completions") == 1)
    # ... but a history pick never repeats that dead end: the side that finds nothing gives way to automatic detection, without an AI request
    tab.hist.selection_clear(0, "end"); tab.hist.selection_set(0); tab._pick_history(); _pump(app, lambda: False, 0.3)
    assert tab.current() is not None and tab.current().headword == word and tab.dir_label.cget("text") == D.direction_text(D.DEFAULT_DIRECTION)
    assert tab.history[0] == (word, "auto") and mock_ai.count("/chat/completions") == 1 and tab.direction.get() == tab._direction_labels[o2t]
    app.settings.update({"dict_ai": "auto", "dict_direction": "auto"}); C.save_settings(app.settings); tab.on_show()


def test_dictionary_turkish_fill_targets_the_right_sense_and_keeps_list_and_store_in_step(app, mock_ai, monkeypatch, tmp_path):
    import csv
    from tkinter import filedialog
    from gca import dictionary as D
    if not D.HAS_TR: pytest.skip("the English app has no separate Turkish field")
    app.settings.update({"ai_enabled": True, "ai_base": mock_ai.base, "dict_ai": "local", "dict_ai_autosave": True, "alt_enabled": False, "dict_direction": "auto"})
    C.save_settings(app.settings); app.refresh_ai_clients()
    app.select("tab.dictionary"); tab = app.current_page(); app.update()
    target = C.TARGET_LANG; t2tr, tr2t = f"{target}2tr", f"tr2{target}"
    def in_db(head): return sorted((r["translation"], r["tr"], r["source"]) for r in app.repos.dictionary.all() if r["headword"] == head)
    def answer(*items): return json.dumps([{"headword": h, "pos": "n", "extra": "", "translation_en": en, "translation_tr": tr} for h, en, tr in items])
    def add_user(head, en, tr=""):
        app.repos.dictionary.add(head, en, "n", "", "", "user", "", tr); tab.dict.extend([D.Entry(head, "n", "", en, "", D.SOURCE_USER, "", tr)])
    # 1. two senses of one headword without Turkish; the AI answers them in the other order and with a wider English gloss:
    #    each row gets its own gloss (castle never receives "kilit"), and the merged answers are not re-listed as AI rows
    add_user("Qqschloss", "qq-castle"); add_user("Qqschloss", "qq-lock")
    mock_ai.content = answer(("Qqschloss", "qq-lock", "qq-kilit"), ("Qqschloss", "qq-castle; qq-palace", "qq-sato; qq-saray"))
    tab.query.set("Qqschloss"); tab.direction.set(tab._direction_labels[t2tr]); tab._direction_changed()
    assert _pump(app, lambda: all(e.tr for e in tab.dict.find("Qqschloss")))
    assert in_db("Qqschloss") == [("qq-castle", "qq-sato; qq-saray", "user"), ("qq-lock", "qq-kilit", "user")]
    assert sorted((e.translation, e.tr) for e in tab.dict.find("Qqschloss")) == [("qq-castle", "qq-sato; qq-saray"), ("qq-lock", "qq-kilit")]
    assert sorted(tab.tree.set(i, "tr") for i in tab.tree.get_children()) == ["qq-kilit", "qq-sato; qq-saray"] and not _ai_rows(tab)
    # 2. a slow answer superseded by further typing: the stored gloss shows up in the list, the status moves on, the word bank gets Turkish
    add_user("Qqtisch", "qq-table"); text = answer(("Qqtisch", "qq-table", "qq-masa"))
    def slow(_body): time.sleep(0.5); return text
    mock_ai.content = slow; tab.query.set("Qqtisch"); tab.search()
    assert app.status.get() == app.t("dict.tr_missing") and tab.tree.set(tab.tree.get_children()[0], "tr") == "—"
    tab.query.set("Qqtis"); tab._on_key(SimpleNamespace(keysym="BackSpace")); app.update()                # quiet search supersedes the request
    assert _pump(app, lambda: tab.tree.set(tab.tree.get_children()[0], "tr") == "qq-masa"), "list not refreshed after the superseded fill"
    assert in_db("Qqtisch") == [("qq-table", "qq-masa", "user")] and tab.current().tr == "qq-masa" and tab.current().source == "user"
    assert app.status.get() not in (app.t("dict.tr_missing"), app.t("dict.ai_asking")) and app.t("dict.ai_asking") not in tab.ai_out.get("1.0", "end")
    tab.add_to_bank(); assert app.repos.words.search("Qqtisch")[0]["tr"] == "qq-masa"
    # 3. a Turkish synonym the stored gloss lacks: appended automatically (autosave) so the next search is local, offered via "Save" otherwise
    add_user("Qqstuhl", "qq-chair", "qq-sandalye"); mock_ai.content = answer(("Qqstuhl", "qq-chair", "qq-koltuk")); calls = mock_ai.count("/chat/completions")
    tab.query.set("qq-koltuk"); tab.direction.set(tab._direction_labels[tr2t]); tab._direction_changed()
    assert _pump(app, lambda: tab.current() is not None and tab.current().source == "user")
    assert tab.current().tr == "qq-sandalye; qq-koltuk" and in_db("Qqstuhl") == [("qq-chair", "qq-sandalye; qq-koltuk", "user")] and not _ai_rows(tab)
    tab.query.set("qq-koltuk"); tab.search(); _pump(app, lambda: False, 0.3)
    assert tab.current().headword == "Qqstuhl" and mock_ai.count("/chat/completions") == calls + 1               # found locally now: no second request
    app.settings["dict_ai_autosave"] = False; C.save_settings(app.settings); mock_ai.content = answer(("Qqstuhl", "qq-chair", "qq-iskemle"))
    tab.query.set("qq-iskemle"); tab.search(); assert _pump(app, lambda: _ai_rows(tab))
    assert tab.current().source == "ai" and tab.save_btn.winfo_manager() and in_db("Qqstuhl") == [("qq-chair", "qq-sandalye; qq-koltuk", "user")]
    tab.save_ai_entry(); app.update()
    assert in_db("Qqstuhl") == [("qq-chair", "qq-sandalye; qq-koltuk; qq-iskemle", "user")] and tab.current().source == "user" and not tab.save_btn.winfo_manager()
    app.settings["dict_ai_autosave"] = True; C.save_settings(app.settings)
    # 4. a user CSV row for a built-in word replaces its Turkish gloss: shown, searchable in TR -> DE without the AI, and kept across a restart
    base = tab.dict.find(_word())[0]; assert base.source == "builtin" and base.tr
    path = tmp_path / "own.csv"
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["headword", "translation", "pos", "extra", "tr"]); w.writerow([base.headword, base.translation, base.pos, base.extra, "qq-ev; qq-konut"])
    monkeypatch.setattr(filedialog, "askopenfilename", lambda **_kw: str(path))
    tab.direction.set(tab._direction_labels["auto"]); tab._direction_changed(); tab.import_file(); app.update()
    assert app.status.get().startswith("1 ") and tab.dict.twin(base).tr == "qq-ev; qq-konut" and tab.dict.twin(base).source == "builtin"
    calls = mock_ai.count("/chat/completions"); tab.query.set("qq-konut"); tab.direction.set(tab._direction_labels[tr2t]); tab._direction_changed(); _pump(app, lambda: False, 0.3)
    assert tab.current() is not None and tab.current().headword == base.headword and mock_ai.count("/chat/completions") == calls
    rebuilt = D.build_dictionary([(r["headword"], r["translation"], r["pos"], r["extra"], r["note"], r["source"], r["example"], r["tr"]) for r in app.repos.dictionary.all()])
    assert rebuilt.twin(base).tr == "qq-ev; qq-konut"
    app.repos.db.execute("DELETE FROM dict_entries WHERE headword=? AND translation=?", (base.headword, base.translation)); tab.dict.set_tr(base, base.tr)
    app.settings.update({"dict_ai": "auto", "dict_direction": "auto"}); C.save_settings(app.settings); tab.on_show()
