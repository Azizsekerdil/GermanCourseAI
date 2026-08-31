from __future__ import annotations

import base64
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable

from . import config as C
from .i18n import SYSTEM_PROMPTS


class AIError(RuntimeError):
    pass


class AIClient:
    """Small OpenAI-compatible client for LM Studio; it never persists message text."""
    def __init__(self, base: str | None = None, token_logger: Callable | None = None):
        self.base = (base or C.LMSTUDIO_BASE).rstrip("/")
        self.token_logger = token_logger

    def _url(self, path: str) -> str:
        return f"{self.base}/v1/{path.lstrip('/')}"

    def available(self, timeout: float = 0.8) -> bool:
        try:
            with urllib.request.urlopen(self._url("models"), timeout=timeout) as response:
                return response.status == 200
        except Exception:
            return False

    def models(self, timeout: float = 1.5) -> list[str]:
        try:
            with urllib.request.urlopen(self._url("models"), timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            return [item["id"] for item in payload.get("data", []) if item.get("id")]
        except Exception:
            return []

    def choose_model(self, task: str, configured: str = "") -> str:
        installed = self.models()
        if configured and (not installed or configured in installed):
            return configured
        for candidate in C.MODEL_PROFILES.get(task, C.MODEL_PROFILES["chat"]):
            if candidate in installed:
                return candidate
        return installed[0] if installed else (configured or C.MODEL_PROFILES["chat"][0])

    def chat(self, prompt: str, task: str, ui_lang: str, model: str = "",
             image_path: str = "", timeout: float = 90.0) -> str:
        chosen = self.choose_model(task, model)
        content: str | list[dict] = prompt
        if image_path:
            path = Path(image_path)
            mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
            encoded = base64.b64encode(path.read_bytes()).decode("ascii")
            content = [{"type": "text", "text": prompt},
                       {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{encoded}"}}]
        body = json.dumps({
            "model": chosen,
            "messages": [{"role": "system", "content": SYSTEM_PROMPTS[ui_lang]},
                         {"role": "user", "content": content}],
            "temperature": 0.35,
            "max_tokens": 900,
        }, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(self._url("chat/completions"), data=body,
                                         headers={"Content-Type": "application/json"}, method="POST")
        started = time.perf_counter()
        ok = False
        usage = {}
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
            usage = payload.get("usage") or {}
            ok = True
            return payload["choices"][0]["message"]["content"].strip()
        except (OSError, KeyError, IndexError, ValueError, urllib.error.URLError) as exc:
            raise AIError(str(exc)) from exc
        finally:
            if self.token_logger:
                elapsed = int((time.perf_counter() - started) * 1000)
                self.token_logger(chosen, task, int(usage.get("prompt_tokens", 0)),
                                  int(usage.get("completion_tokens", 0)), elapsed, ok)


def approx_tokens(text: str) -> int:
    return max(1, len(text or "") // 4)
