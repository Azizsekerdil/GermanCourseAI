"""Secret store (file backend forced by conftest), env override and the settings-file invariant."""
from __future__ import annotations

import json

from gca import config as C
from gca import secrets as S

KEY = "alt_api_key"


def test_file_backend_is_forced_in_tests():
    assert S._use_file_backend()
    assert S.secrets_path().parent == C.SETTINGS_DIR and S.secrets_path().name == "secrets.json"


def test_roundtrip_and_delete(monkeypatch):
    monkeypatch.delenv(C.API_KEY_ENV, raising=False)
    S.delete_secret(KEY)
    assert S.get_secret(KEY) == "" and not S.has_secret(KEY)
    S.set_secret(KEY, "  nvapi-test-123  ")
    assert S.get_secret(KEY) == "nvapi-test-123" and S.has_secret(KEY)
    assert json.loads(S.secrets_path().read_text(encoding="utf-8"))[KEY] == "nvapi-test-123"
    S.set_secret("other", "x")
    assert S.get_secret("other") == "x" and S.get_secret(KEY) == "nvapi-test-123"
    S.delete_secret(KEY)
    assert S.get_secret(KEY) == "" and S.get_secret("other") == "x"
    S.set_secret("other", "")                       # empty value == delete
    assert not S.has_secret("other")
    S.delete_secret("missing")                      # never raises
    assert not S.secrets_path().with_suffix(".tmp").exists()


def test_env_override_wins_for_api_key(monkeypatch):
    S.set_secret(KEY, "stored")
    monkeypatch.setenv(C.API_KEY_ENV, "from-env")
    assert S.get_secret(KEY) == "from-env"
    monkeypatch.delenv(C.API_KEY_ENV)
    assert S.get_secret(KEY) == "stored"
    S.delete_secret(KEY)


def test_settings_file_never_contains_the_key(monkeypatch):
    monkeypatch.delenv(C.API_KEY_ENV, raising=False)
    S.set_secret(KEY, "nvapi-super-secret")
    original = C.load_settings(); settings = dict(original)
    settings.update({"alt_enabled": True, "alt_api_key": "nvapi-super-secret", "api_key": "nvapi-super-secret"})
    try:
        C.save_settings(settings)
        text = C.SETTINGS_PATH.read_text(encoding="utf-8")
        assert "nvapi-super-secret" not in text and "api_key" not in text
        assert C.load_settings()["alt_enabled"] is True and S.get_secret(KEY) == "nvapi-super-secret"
    finally:
        S.delete_secret(KEY); C.save_settings(original)


def test_defaults_and_legacy_nim_flag_migration():
    original = C.load_settings()
    try:
        for key, value in (("alt_enabled", False), ("alt_base", C.NIM_BASE), ("alt_model", "meta/llama-3.1-8b-instruct"),
                           ("dict_ai", "auto"), ("dict_ai_autosave", True), ("nim_enabled", False)):
            assert C.DEFAULT_SETTINGS[key] == value
        C.SETTINGS_PATH.write_text(json.dumps({"ui_lang": "en", "nim_enabled": True}), encoding="utf-8")
        loaded = C.load_settings()
        assert loaded["alt_enabled"] is True and loaded["dict_ai"] == "auto" and loaded["alt_base"] == C.NIM_BASE
        C.SETTINGS_PATH.write_text(json.dumps({"nim_enabled": True, "alt_enabled": False, "dict_ai": "bogus", "alt_base": ""}), encoding="utf-8")
        loaded = C.load_settings()
        assert loaded["alt_enabled"] is False and loaded["dict_ai"] == "auto" and loaded["alt_base"] == C.NIM_BASE
    finally:
        C.save_settings(original)
