from __future__ import annotations

import base64
import ipaddress
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable

from . import config as C
from .i18n import SYSTEM_PROMPTS

REACH_TTL = 30.0            # seconds a reachability probe stays valid
_PRIVATE_SUFFIXES = (".local", ".localdomain", ".lan", ".home", ".home.arpa", ".internal")


def host_kind(base: str) -> str:
    """Classify the host of an endpoint URL without touching the network.

    ``loopback``: this machine; ``private``: a box on the local network (RFC 1918 / link-local / ULA
    addresses, ``.local``-style names, bare host names); ``public``: everything else.
    """
    base = (base or "").strip()
    try:
        host = (urllib.parse.urlsplit(base if "//" in base else f"//{base}").hostname or "").lower()
    except ValueError:
        return "public"
    if not host:
        return "public"
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        if host == "localhost" or host.endswith(".localhost"):
            return "loopback"
        return "private" if host.endswith(_PRIVATE_SUFFIXES) or "." not in host else "public"
    if ip.is_loopback or ip.is_unspecified:
        return "loopback"
    return "private" if ip.is_private or ip.is_link_local else "public"


class AIError(RuntimeError):
    pass


class AIClient:
    """Small OpenAI-compatible client (LM Studio, NVIDIA NIM, OpenRouter, Ollama, ...).

    It never persists message text. ``api_key`` is sent as ``Authorization: Bearer``
    on every request when set; local servers simply ignore it.
    """
    def __init__(self, base: str | None = None, token_logger: Callable | None = None,
                 api_key: str = "", model: str = ""):
        self.token_logger = token_logger
        self.api_key = ""
        self.model = ""
        self.last_model = ""
        self._reach: tuple[float, bool] | None = None
        self.configure(base or C.LMSTUDIO_BASE, api_key, model)

    # ------------------------------------------------------------------ setup
    def configure(self, base: str | None = None, api_key: str | None = None, model: str | None = None) -> None:
        """Update endpoint/key/model in place and forget the cached reachability."""
        if base is not None:
            self.base = (base or C.LMSTUDIO_BASE).strip().rstrip("/")
        if api_key is not None:
            self.api_key = (api_key or "").strip()
        if model is not None:
            self.model = (model or "").strip()
        self.invalidate()

    def invalidate(self) -> None:
        self._reach = None

    @property
    def is_local(self) -> bool:
        """Endpoint on this machine (loopback)."""
        return host_kind(self.base) == "loopback"

    @property
    def is_private(self) -> bool:
        """Endpoint on this machine or on the local network (LM Studio / Ollama on another LAN box): no API key expected."""
        return host_kind(self.base) in ("loopback", "private")

    @property
    def needs_key(self) -> bool:
        return not self.is_private

    def usable(self) -> bool:
        """True when a request can be attempted: a key is set or the endpoint needs none."""
        return bool(self.api_key) or not self.needs_key

    # --------------------------------------------------------------- requests
    def _url(self, path: str) -> str:
        base = self.base[:-3] if self.base.endswith("/v1") else self.base
        return f"{base}/v1/{path.lstrip('/')}"

    def _headers(self, json_body: bool = False) -> dict[str, str]:
        headers = {"Accept": "application/json", "User-Agent": f"{C.APP_SLUG}/{C.VERSION}"}
        if json_body:
            headers["Content-Type"] = "application/json"
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _open(self, path: str, data: bytes | None = None, timeout: float = 10.0):
        request = urllib.request.Request(self._url(path), data=data, headers=self._headers(data is not None),
                                         method="POST" if data is not None else "GET")
        return urllib.request.urlopen(request, timeout=timeout)

    def available(self, timeout: float = 0.8) -> bool:
        try:
            with self._open("models", timeout=timeout) as response:
                return response.status == 200
        except Exception:
            return False

    def models(self, timeout: float = 1.5) -> list[str]:
        try:
            with self._open("models", timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return [item["id"] for item in payload.get("data", []) if item.get("id")]
        except Exception:
            return []

    def reachable(self, ttl: float = REACH_TTL, timeout: float | None = None) -> bool:
        """``GET /v1/models`` succeeds; the answer is cached for ``ttl`` seconds."""
        now = time.monotonic()
        if self._reach and now - self._reach[0] < ttl:
            return self._reach[1]
        ok = self.available(timeout if timeout is not None else (1.5 if self.is_local else 4.0))
        self._reach = (now, ok)
        return ok

    def choose_model(self, task: str, configured: str = "") -> str:
        configured = configured or self.model
        if configured and self.needs_key:          # remote catalogues are huge/partial: trust the configured name
            return configured
        installed = self.models()
        if configured and (not installed or configured in installed):
            return configured
        for candidate in C.MODEL_PROFILES.get(task, C.MODEL_PROFILES["chat"]):
            if candidate in installed:
                return candidate
        return installed[0] if installed else (configured or C.MODEL_PROFILES["chat"][0])

    def chat(self, prompt: str, task: str, ui_lang: str, model: str = "",
             image_path: str = "", timeout: float = 90.0, system: str = "",
             temperature: float = 0.35, max_tokens: int = 900) -> str:
        chosen = self.choose_model(task, model)
        self.last_model = chosen
        content: str | list[dict] = prompt
        if image_path:
            path = Path(image_path)
            mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            content = [{"type": "text", "text": prompt},
                       {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{encoded}"}}]
        body = json.dumps({
            "model": chosen,
            "messages": [{"role": "system", "content": system or SYSTEM_PROMPTS.get(ui_lang, SYSTEM_PROMPTS["en"])},
                         {"role": "user", "content": content}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }, ensure_ascii=False).encode("utf-8")
        started = time.perf_counter()
        ok = False
        usage: dict[str, Any] = {}
        try:
            with self._open("chat/completions", data=body, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            usage = payload.get("usage") or {}
            ok = True
            return payload["choices"][0]["message"]["content"].strip()
        except (OSError, KeyError, IndexError, TypeError, ValueError, urllib.error.URLError) as exc:
            raise AIError(str(exc)) from exc
        finally:
            if self.token_logger:
                elapsed = int((time.perf_counter() - started) * 1000)
                self.token_logger(chosen, task, int(usage.get("prompt_tokens", 0) or 0),
                                  int(usage.get("completion_tokens", 0) or 0), elapsed, ok)


def resolve_provider(settings: dict, local: AIClient | None, alt: AIClient | None,
                     policy: str | None = None) -> AIClient | None:
    """Client the dictionary should use under ``settings["dict_ai"]`` (or ``policy``).

    off   -> None
    local -> local client when local AI is enabled and reachable
    alt   -> alternative client when enabled and a key is set (or none is needed: host on this machine / the LAN)
    auto  -> local if reachable, else alternative if enabled, else None
    """
    policy = policy or settings.get("dict_ai") or "auto"
    if policy not in C.DICT_AI_POLICIES:
        policy = "auto"

    def local_ok() -> bool:
        return bool(settings.get("ai_enabled", True)) and local is not None and local.reachable()

    def alt_ok() -> bool:
        return bool(settings.get("alt_enabled")) and alt is not None and alt.usable()

    if policy == "off":
        return None
    if policy == "local":
        return local if local_ok() else None
    if policy == "alt":
        return alt if alt_ok() else None
    if local_ok():
        return local
    return alt if alt_ok() else None


def approx_tokens(text: str) -> int:
    return max(1, len(text or "") // 4)
