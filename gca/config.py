from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

APP_NAME = "German Course AI"
APP_SLUG = "GermanCourseAI"
TARGET_LANG = "de"
TARGET_LANG_NAME = "Deutsch"
VERSION = "1.3.0"
HOME_ENV = "GCA_HOME"
API_KEY_ENV = f"{APP_SLUG.upper()}_API_KEY"              # overrides the stored alternative-endpoint key
SECRETS_FILE_ENV = f"{APP_SLUG.upper()}_SECRETS_FILE"    # "1" forces the JSON secret store (tests)
DB_FILENAME = "GermanCourseAI.db"
PACK_EXTENSION = ".gcapack"
UI_LANGS = ("tr", "en", "de")
CEFR_LEVELS = ("A1", "A2", "B1", "B2", "C1")

PACKAGE_DIR = Path(__file__).resolve().parent
PROGRAM_DIR = PACKAGE_DIR.parent


def _home() -> Path:
    override = os.environ.get(HOME_ENV)
    if override:
        return Path(override)
    if sys.platform.startswith("win"):
        return Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")) / APP_SLUG
    return Path.home() / f".{APP_SLUG.lower()}"


APP_HOME = _home()
DATA_DIR = APP_HOME / "data"
SETTINGS_DIR = APP_HOME / "settings"
EXPORT_DIR = APP_HOME / "exports"
DOWNLOAD_DIR = APP_HOME / "downloads"
DB_PATH = DATA_DIR / DB_FILENAME
SETTINGS_PATH = SETTINGS_DIR / "settings.json"
RESOURCES_DIR = PROGRAM_DIR / "Resources"


def ensure_dirs() -> None:
    for path in (APP_HOME, DATA_DIR, SETTINGS_DIR, EXPORT_DIR, DOWNLOAD_DIR):
        path.mkdir(parents=True, exist_ok=True)


LMSTUDIO_BASE = "http://127.0.0.1:1234"
NIM_BASE = "https://integrate.api.nvidia.com/v1"
ALT_MODEL_DEFAULT = "meta/llama-3.1-8b-instruct"
DICT_AI_POLICIES = ("auto", "local", "alt", "off")      # dictionary AI provider policy


def _dict_directions(target: str) -> tuple[str, ...]:
    """Dictionary direction codes: ``auto`` plus every fixed pair between the target language, English and Turkish.

    German: auto | de2en | en2de | de2tr | tr2de. For the English app the translation side already *is* Turkish,
    so only auto | en2tr | tr2en exist."""
    if target == "en":
        return ("auto", "en2tr", "tr2en")
    return ("auto", f"{target}2en", f"en2{target}", f"{target}2tr", f"tr2{target}")


DICT_DIRECTIONS = _dict_directions(TARGET_LANG)
MODEL_PROFILES = {
    "chat": ["qwen2.5-7b-instruct", "llama-3.1-8b-instruct"],
    "grammar": ["qwen2.5-7b-instruct", "qwen2.5-14b-instruct"],
    "translate": ["qwen2.5-7b-instruct", "gemma-2-9b-it"],
    "correct": ["qwen2.5-7b-instruct", "qwen2.5-14b-instruct"],
    "dialogue": ["qwen2.5-7b-instruct", "llama-3.1-8b-instruct"],
    "dictionary": ["qwen2.5-7b-instruct", "llama-3.1-8b-instruct"],
    "vision": ["qwen2-vl-7b-instruct", "llava-v1.6-mistral-7b"],
}

DEFAULT_SETTINGS: dict[str, Any] = {
    "ui_lang": "tr",
    "theme": "dark",
    "profile_id": None,
    "daily_goal": 20,
    "tts_enabled": True,
    "tts_rate": 155,
    "ai_enabled": True,
    "ai_base": LMSTUDIO_BASE,
    "ai_model": MODEL_PROFILES["chat"][0],
    "nim_enabled": False,               # legacy stub; migrated to alt_enabled on load
    "alt_enabled": False,
    "alt_base": NIM_BASE,
    "alt_model": ALT_MODEL_DEFAULT,
    "dict_ai": "auto",                  # auto | local | alt | off
    "dict_ai_autosave": True,
    "dict_direction": "auto",           # one of DICT_DIRECTIONS
    "cefr": "A1",
    "last_pdf": "",
}

PALETTES = {
    "dark": {
        "deep": "#11100d", "bg": "#171612", "panel": "#211f19", "card": "#29261e",
        "hover": "#343027", "fg": "#f8f4e8", "muted": "#aaa28f", "border": "#3a352a",
        "accent": "#e2ad3b", "accent2": "#c74b3f", "ok": "#61c48b", "warn": "#e3a94c",
    },
    "light": {
        "deep": "#eee9dc", "bg": "#f8f5ed", "panel": "#fffdf8", "card": "#f2ecde",
        "hover": "#e8dfcc", "fg": "#211e18", "muted": "#6d6659", "border": "#d6cbb5",
        "accent": "#a66b08", "accent2": "#ad392f", "ok": "#277a4d", "warn": "#94630c",
    },
}


def load_settings() -> dict[str, Any]:
    ensure_dirs()
    result = dict(DEFAULT_SETTINGS)
    try:
        raw = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            result.update({k: raw[k] for k in DEFAULT_SETTINGS if k in raw})
            if raw.get("nim_enabled") and "alt_enabled" not in raw:      # pre-alt settings file
                result["alt_enabled"] = True
    except (OSError, ValueError, TypeError):
        pass
    if result.get("ui_lang") not in UI_LANGS:
        result["ui_lang"] = "tr"
    if result.get("dict_ai") not in DICT_AI_POLICIES:
        result["dict_ai"] = "auto"
    if result.get("dict_direction") not in DICT_DIRECTIONS:
        result["dict_direction"] = "auto"
    if not str(result.get("alt_base") or "").strip():
        result["alt_base"] = NIM_BASE
    return result


def save_settings(settings: dict[str, Any]) -> None:
    """Persist known, non-secret settings with an atomic replace."""
    ensure_dirs()
    safe = {k: settings.get(k, v) for k, v in DEFAULT_SETTINGS.items()}
    temporary = SETTINGS_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(safe, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, SETTINGS_PATH)


_PUNCT = re.compile(r"[^\w\s\-']", re.UNICODE)


def normalize_exact(text: str) -> str:
    """Comparison form that deliberately preserves umlauts, ß and capitalization."""
    value = unicodedata.normalize("NFC", text or "").strip()
    value = value.replace("’", "'").replace("`", "'")
    return re.sub(r"\s+", " ", value)


def normalize_search(text: str) -> str:
    """Search-only equivalence: ä/ae, ö/oe, ü/ue and ß/ss.

    Turkish letters (ç ğ ş, and ö/ü through the same folding) match themselves. The dotted capital İ lowers to a plain
    ``i`` (``str.lower`` would leave a combining dot) and, because ``I`` also lowers to ``i``, dotless ı is folded to
    ``i`` too, so ``Işık``, ``ışık`` and ``isik``-style input all compare equal - search only, never spelling checks.
    The circumflex (``kâğıt``, ``dükkân``, ``resmî``) is folded as well, because most people type these words without it."""
    value = normalize_exact(text).replace("İ", "i").lower().replace("ı", "i")
    value = value.replace("â", "a").replace("î", "i").replace("û", "u")
    value = value.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    value = _PUNCT.sub(" ", value)
    return re.sub(r"\s+", " ", value).strip()


def answer_equal(given: str, expected: str) -> bool:
    return normalize_exact(given) == normalize_exact(expected)
