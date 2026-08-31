from pathlib import Path

from gca import config as C
from gca.i18n import LANG_NAMES, LOCALES, SYSTEM_PROMPTS


def test_identity_and_isolated_paths():
    assert (C.APP_NAME, C.APP_SLUG, C.TARGET_LANG, C.TARGET_LANG_NAME) == ("German Course AI", "GermanCourseAI", "de", "Deutsch")
    assert C.DB_PATH.name == "GermanCourseAI.db"
    assert C.APP_SLUG.lower() not in "frenchcourseai"


def test_settings_roundtrip_is_filtered_and_atomic():
    data = C.load_settings(); data["ui_lang"] = "de"; data["daily_goal"] = 37; data["api_key"] = "must-not-persist"
    C.save_settings(data); back = C.load_settings()
    assert back["ui_lang"] == "de" and back["daily_goal"] == 37
    assert "api_key" not in C.SETTINGS_PATH.read_text(encoding="utf-8")
    assert not C.SETTINGS_PATH.with_suffix(".tmp").exists()


def test_all_i18n_keys_exist_in_three_languages():
    assert tuple(LANG_NAMES) == C.UI_LANGS
    keys = set(LOCALES["tr"])
    assert len(keys) >= 140
    assert all(set(LOCALES[lang]) == keys for lang in C.UI_LANGS)
    assert all(value.strip() for lang in C.UI_LANGS for value in LOCALES[lang].values())


def test_system_prompts_follow_interface_language():
    assert set(SYSTEM_PROMPTS) == set(C.UI_LANGS)
    assert "Türkçe" in SYSTEM_PROMPTS["tr"] and "article" in SYSTEM_PROMPTS["en"]
    assert "einfachem Deutsch" in SYSTEM_PROMPTS["de"] and "Plural" in SYSTEM_PROMPTS["de"]


def test_german_search_and_spelling_forms_are_separate():
    assert C.normalize_search("Mädchen") == "maedchen"
    assert C.normalize_search("Mädchen") == C.normalize_search("Maedchen")
    assert C.normalize_search("Straße") == C.normalize_search("Strasse")
    assert C.answer_equal("Straße", "Straße")
    assert not C.answer_equal("Strasse", "Straße")
    assert not C.answer_equal("straße", "Straße")
