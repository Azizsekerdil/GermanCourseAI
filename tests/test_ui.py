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
