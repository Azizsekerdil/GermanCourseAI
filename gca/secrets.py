"""Tiny secret store for API keys.

Windows: Credential Manager through ``advapi32`` (generic credential named
``<APP_SLUG>/<name>``, blob stored as UTF-16-LE).  Elsewhere, or whenever the
Windows API is unavailable or fails: a JSON file ``<SETTINGS_DIR>/secrets.json``
(mode 0o600 where the platform supports it).

Secrets never go through ``settings.json``.  Tests force the file backend with
``FORCE_FILE_BACKEND = True`` or the ``<APP_SLUG_UPPER>_SECRETS_FILE=1`` env var so
they never touch the real Credential Manager.
"""
from __future__ import annotations

import ctypes
import json
import os
import sys
from pathlib import Path

from . import config as C

FORCE_FILE_BACKEND = False
ENV_OVERRIDES = {"alt_api_key": C.API_KEY_ENV}

CRED_TYPE_GENERIC = 1
CRED_PERSIST_LOCAL_MACHINE = 2
_ERROR_NOT_FOUND = 1168


# ---------------------------------------------------------------------------
# Backend selection
# ---------------------------------------------------------------------------
def _use_file_backend() -> bool:
    if FORCE_FILE_BACKEND or os.environ.get(C.SECRETS_FILE_ENV) == "1":
        return True
    return not sys.platform.startswith("win")


def _target(name: str) -> str:
    return f"{C.APP_SLUG}/{name}"


# ---------------------------------------------------------------------------
# File backend
# ---------------------------------------------------------------------------
def secrets_path() -> Path:
    return C.SETTINGS_DIR / "secrets.json"


def _file_read_all() -> dict[str, str]:
    try:
        raw = json.loads(secrets_path().read_text(encoding="utf-8"))
        return {str(k): str(v) for k, v in raw.items()} if isinstance(raw, dict) else {}
    except (OSError, ValueError, TypeError, AttributeError):
        return {}


def _file_write_all(data: dict[str, str]) -> None:
    C.ensure_dirs()
    path = secrets_path()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(temporary, 0o600)
    except OSError:
        pass
    os.replace(temporary, path)


def _file_get(name: str) -> str:
    return _file_read_all().get(name, "")


def _file_set(name: str, value: str) -> None:
    data = _file_read_all()
    data[name] = value
    _file_write_all(data)


def _file_delete(name: str) -> None:
    data = _file_read_all()
    if name in data:
        del data[name]
        _file_write_all(data)


# ---------------------------------------------------------------------------
# Windows Credential Manager backend (ctypes)
# ---------------------------------------------------------------------------
if sys.platform.startswith("win"):
    from ctypes import wintypes

    class _CREDENTIAL(ctypes.Structure):
        _fields_ = [
            ("Flags", wintypes.DWORD), ("Type", wintypes.DWORD),
            ("TargetName", wintypes.LPWSTR), ("Comment", wintypes.LPWSTR),
            ("LastWritten", wintypes.FILETIME), ("CredentialBlobSize", wintypes.DWORD),
            ("CredentialBlob", ctypes.POINTER(ctypes.c_char)), ("Persist", wintypes.DWORD),
            ("AttributeCount", wintypes.DWORD), ("Attributes", ctypes.c_void_p),
            ("TargetAlias", wintypes.LPWSTR), ("UserName", wintypes.LPWSTR),
        ]

    def _advapi():
        lib = ctypes.WinDLL("advapi32", use_last_error=True)
        lib.CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(_CREDENTIAL))]
        lib.CredReadW.restype = wintypes.BOOL
        lib.CredWriteW.argtypes = [ctypes.POINTER(_CREDENTIAL), wintypes.DWORD]
        lib.CredWriteW.restype = wintypes.BOOL
        lib.CredDeleteW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD]
        lib.CredDeleteW.restype = wintypes.BOOL
        lib.CredFree.argtypes = [ctypes.c_void_p]
        lib.CredFree.restype = None
        return lib

    def _cred_get(name: str) -> str:
        lib = _advapi()
        pointer = ctypes.POINTER(_CREDENTIAL)()
        if not lib.CredReadW(_target(name), CRED_TYPE_GENERIC, 0, ctypes.byref(pointer)):
            if ctypes.get_last_error() == _ERROR_NOT_FOUND:
                return ""
            raise OSError(ctypes.get_last_error(), "CredReadW failed")
        try:
            cred = pointer.contents
            blob = ctypes.string_at(cred.CredentialBlob, cred.CredentialBlobSize) if cred.CredentialBlobSize else b""
            return blob.decode("utf-16-le")
        finally:
            lib.CredFree(pointer)

    def _cred_set(name: str, value: str) -> None:
        lib = _advapi()
        blob = value.encode("utf-16-le")
        buffer = ctypes.create_string_buffer(blob, max(len(blob), 1))
        cred = _CREDENTIAL()
        cred.Type = CRED_TYPE_GENERIC
        cred.TargetName = _target(name)
        cred.Comment = C.APP_NAME
        cred.CredentialBlobSize = len(blob)
        cred.CredentialBlob = ctypes.cast(buffer, ctypes.POINTER(ctypes.c_char))
        cred.Persist = CRED_PERSIST_LOCAL_MACHINE
        cred.UserName = C.APP_SLUG
        if not lib.CredWriteW(ctypes.byref(cred), 0):
            raise OSError(ctypes.get_last_error(), "CredWriteW failed")

    def _cred_delete(name: str) -> None:
        lib = _advapi()
        if not lib.CredDeleteW(_target(name), CRED_TYPE_GENERIC, 0):
            if ctypes.get_last_error() != _ERROR_NOT_FOUND:
                raise OSError(ctypes.get_last_error(), "CredDeleteW failed")
else:  # pragma: no cover - non-Windows platforms use the file store only
    def _cred_get(name: str) -> str: raise OSError("Credential Manager unavailable")
    def _cred_set(name: str, value: str) -> None: raise OSError("Credential Manager unavailable")
    def _cred_delete(name: str) -> None: raise OSError("Credential Manager unavailable")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def get_secret(name: str) -> str:
    """Stored secret or ``""``. The environment override (if any) always wins."""
    env = ENV_OVERRIDES.get(name)
    if env and os.environ.get(env):
        return os.environ[env].strip()
    if not _use_file_backend():
        try:
            value = _cred_get(name)
            if value:
                return value
        except Exception:
            pass
    return _file_get(name)


def set_secret(name: str, value: str) -> None:
    value = (value or "").strip()
    if not value:
        delete_secret(name); return
    if not _use_file_backend():
        try:
            _cred_set(name, value)
            _file_delete(name)          # no stale copy in the fallback file
            return
        except Exception:
            pass
    _file_set(name, value)


def delete_secret(name: str) -> None:
    if not _use_file_backend():
        try:
            _cred_delete(name)
        except Exception:
            pass
    _file_delete(name)


def has_secret(name: str) -> bool:
    return bool(get_secret(name))
