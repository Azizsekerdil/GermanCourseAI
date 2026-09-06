import json
import os
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

TEST_HOME = Path(tempfile.mkdtemp(prefix="gca-tests-"))
os.environ["GCA_HOME"] = str(TEST_HOME)

from gca import config as C  # noqa: E402  (must come after the home override)

os.environ[C.SECRETS_FILE_ENV] = "1"          # tests never touch the real Credential Manager
os.environ.pop(C.API_KEY_ENV, None)


# ---------------------------------------------------------------------------
# Mock OpenAI-compatible server (LM Studio / NIM stand-in); no real network is ever used.
# ---------------------------------------------------------------------------
SAMPLE_ENTRIES = {
    "de": [
        {"headword": "Brotzeit", "pos": "n", "extra": "die Brotzeiten", "translation": "snack; light meal",
         "example": "Wir machen jetzt Brotzeit.", "note": "southern German, Bavarian"},
        {"headword": "der Feierabend", "pos": "noun", "extra": "Feierabende", "translation": "end of the working day",
         "example": "Schönen Feierabend!", "note": ""},
    ],
    "fr": [
        {"headword": "grignotage", "pos": "n", "extra": "m", "translation": "snacking; nibbling",
         "example": "Le grignotage entre les repas est fréquent.", "note": "familiar"},
        {"headword": "la pause", "pos": "noun", "extra": "", "translation": "break; pause",
         "example": "On fait une pause.", "note": ""},
    ],
    "en": [
        {"headword": "elevenses", "pos": "n", "extra": "/ɪˈlɛvənzɪz/", "translation": "kuşluk atıştırması; sabah ara öğünü",
         "example": "We stopped for elevenses.", "note": "a light mid-morning snack (British)"},
        {"headword": "snack", "pos": "noun", "extra": "", "translation": "atıştırmalık",
         "example": "I had a snack.", "note": "a small amount of food eaten between meals"},
    ],
}


def fenced(entries) -> str:
    return "```json\n" + json.dumps(entries, ensure_ascii=False, indent=1) + "\n```"


class MockOpenAI:
    """Minimal OpenAI-compatible server: ``GET /v1/models`` and ``POST /v1/chat/completions``.

    Every request is recorded (method, path, Authorization header, parsed JSON body).
    ``content`` is the assistant text to return; a callable receives the request body.
    """
    MODEL = "mock-model"

    def __init__(self, content=None):
        self.sample = SAMPLE_ENTRIES[C.TARGET_LANG]
        self.content = content if content is not None else fenced(self.sample)
        self.requests: list[dict] = []
        self._lock = threading.Lock()
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_args): pass

            def _send(self, payload, status=200):
                body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
                self.send_response(status); self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

            def do_GET(self):
                server._record("GET", self.path, self.headers.get("Authorization", ""), None)
                if self.path.rstrip("/").endswith("/models"):
                    self._send({"object": "list", "data": [{"id": MockOpenAI.MODEL, "object": "model"}]})
                else:
                    self._send({"error": "not found"}, 404)

            def do_POST(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                try: body = json.loads(raw.decode("utf-8"))
                except ValueError: body = {"raw": raw.decode("utf-8", "replace")}
                server._record("POST", self.path, self.headers.get("Authorization", ""), body)
                if not self.path.rstrip("/").endswith("/chat/completions"):
                    self._send({"error": "not found"}, 404); return
                content = server.content(body) if callable(server.content) else server.content
                self._send({"id": "chatcmpl-mock", "object": "chat.completion", "model": body.get("model", MockOpenAI.MODEL),
                            "choices": [{"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
                            "usage": {"prompt_tokens": 42, "completion_tokens": 17, "total_tokens": 59}})

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.httpd.daemon_threads = True
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def _record(self, method, path, auth, body):
        with self._lock:
            self.requests.append({"method": method, "path": path, "auth": auth, "body": body})

    def count(self, path_suffix: str | None = None) -> int:
        with self._lock:
            return len([r for r in self.requests if not path_suffix or r["path"].rstrip("/").endswith(path_suffix)])

    @property
    def chats(self) -> list[dict]:
        with self._lock:
            return [r for r in self.requests if r["path"].rstrip("/").endswith("/chat/completions")]

    def stop(self):
        self.httpd.shutdown(); self.httpd.server_close()


@pytest.fixture()
def mock_ai():
    server = MockOpenAI()
    yield server
    server.stop()
