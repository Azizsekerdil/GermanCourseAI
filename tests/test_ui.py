import tkinter as tk

import pytest

from gca import config as C
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
