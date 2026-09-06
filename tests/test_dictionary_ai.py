"""AI-driven dictionary lookup and provider resolution against a local mock OpenAI server (no real network)."""
from __future__ import annotations

import json
import time

import pytest

from gca import config as C
from gca import dictionary as D
from gca.ai_client import AIClient, AIError, host_kind, resolve_provider


def test_ai_lookup_parses_fenced_json_and_sends_bearer(mock_ai):
    client = AIClient(mock_ai.base, api_key="sk-test-123")
    entries = D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    assert len(entries) == len(mock_ai.sample) and all(e.source == D.SOURCE_AI for e in entries)
    first, sample = entries[0], mock_ai.sample[0]
    assert (first.headword, first.pos, first.extra, first.translation) == (sample["headword"], "n", sample["extra"], sample["translation"])
    assert first.example == sample["example"] and first.note == sample["note"]
    assert all(e.pos in D.POS_LABELS for e in entries)
    second = entries[1]
    assert second.pos == "n"                                             # "noun" normalised to the dictionary's code
    if C.TARGET_LANG == "de":
        assert (second.headword, second.extra, second.display, second.plural) == ("Feierabend", "der Feierabende", "der Feierabend", "Feierabende")
    elif C.TARGET_LANG == "fr":
        assert (second.headword, second.gender) == ("pause", "f")
    chat = mock_ai.chats[-1]
    assert chat["auth"] == "Bearer sk-test-123"
    assert chat["body"]["model"] == mock_ai.MODEL and client.last_model == mock_ai.MODEL
    user = chat["body"]["messages"][-1]["content"]
    assert sample["headword"] in user and "JSON" in user and C.TARGET_LANG_NAME in user
    assert all(r["auth"] == "Bearer sk-test-123" for r in mock_ai.requests)       # /models probe carries it too


def test_no_key_means_no_authorization_header(mock_ai):
    client = AIClient(mock_ai.base)
    assert D.ai_lookup(client, "x", "tr")
    assert all(r["auth"] == "" for r in mock_ai.requests)
    assert D.ai_lookup(client, "   ", "tr") == [] and mock_ai.count("/chat/completions") == 1   # blank query never hits the network


def test_garbage_output_yields_empty_list_without_raising(mock_ai):
    mock_ai.content = "Sorry, I cannot help with that."
    assert D.ai_lookup(AIClient(mock_ai.base), "x", "en") == []
    for garbage in ("", "null", "[]", "[1, 2]", '[{"headword": 5}]', "```\n[{broken\n```", '[{"headword": "a", "translation": null}]',
                    '{"headword": "a"}', "[[[", "]]]", '[{"headword": {"x": 1}, "translation": "y"}]', "[" * 5000):
        assert D.parse_ai_entries(garbage) == [], garbage


def test_parser_is_tolerant_and_bounded():
    rows = D.parse_ai_entries('Here you go:\n```json\n[{"headword": "x", "translation": ["y", "z"], "pos": "Verb"}]\n```\nHope it helps!')
    assert rows[0].translation == "y; z" and rows[0].pos == "v" and rows[0].source == D.SOURCE_AI
    assert D.parse_ai_entries('[{"headword": "x", "translation": "y"}]')[0].pos == "phr"          # missing pos
    long = "a" * 500
    e = D.parse_ai_entries(json.dumps([{"headword": long, "translation": long, "example": long, "note": long, "extra": long}]))[0]
    assert len(e.headword) <= 80 and len(e.translation) <= 200 and len(e.example) <= 240 and len(e.note) <= 240 and len(e.extra) <= 80
    many = D.parse_ai_entries(json.dumps([{"headword": f"w{i}", "translation": "t"} for i in range(12)]))
    assert len(many) == D.AI_MAX_ENTRIES
    mixed = D.parse_ai_entries(json.dumps([7, {"headword": "ok", "translation": "fine"}, {"headword": "", "translation": "x"}, "str"]))
    assert [e.headword for e in mixed] == ["ok"]
    if C.TARGET_LANG == "de":
        e = D.parse_ai_entries('[{"headword": "die Katze", "pos": "n", "extra": "die Katzen", "translation": "cat"}]')[0]
        assert (e.headword, e.extra, e.display) == ("Katze", "die Katzen", "die Katze")
        e = D.parse_ai_entries('[{"headword": "Tisch", "pos": "Substantiv", "extra": "der, Tische", "translation": "table"}]')[0]
        assert (e.pos, e.extra, e.plural) == ("n", "der Tische", "Tische")


def test_normalize_pos_covers_codes_names_and_localised_labels():
    assert D.normalize_pos("noun") == "n" and D.normalize_pos("Substantiv") == "n" and D.normalize_pos("isim") == "n"
    assert D.normalize_pos("verb.") == "v" and D.normalize_pos("ADJ") == "adj" and D.normalize_pos("n.") == "n"
    assert D.normalize_pos("noun (m)") == "n" and D.normalize_pos("Wendung") == "phr" and D.normalize_pos("interjection") == "int"
    assert D.normalize_pos("whatever") == "phr" and D.normalize_pos(None) == "phr" and D.normalize_pos(3) == "phr"


def test_ai_prompt_explains_convention_and_direction():
    prompt = D.ai_prompt("Haus", "tr")
    assert "Haus" in prompt and "headword" in prompt and "translation" in prompt and "example" in prompt
    assert all(code in prompt for code in D.POS_LABELS) and str(D.AI_MAX_ENTRIES) in prompt
    assert "Detect the direction" in prompt and C.TARGET_LANG_NAME in prompt
    if C.TARGET_LANG == "de": assert "der Tische" in prompt
    if C.TARGET_LANG == "fr": assert '"m"' in prompt
    if C.TARGET_LANG == "en": assert "Turkish" in prompt


def test_closed_port_raises_aierror_quickly():
    client = AIClient("http://127.0.0.1:9")
    started = time.monotonic()
    with pytest.raises(AIError):
        D.ai_lookup(client, "Haus", "en")
    assert time.monotonic() - started < 5
    assert client.available(timeout=0.2) is False and client.reachable(timeout=0.2) is False


def test_client_url_headers_and_key_requirements():
    remote = AIClient(C.NIM_BASE + "/", api_key="k", model="meta/llama-3.1-8b-instruct")
    assert remote._url("models") == "https://integrate.api.nvidia.com/v1/models"
    assert remote._headers()["Authorization"] == "Bearer k" and remote.needs_key and not remote.is_local and remote.usable()
    assert remote.choose_model("dictionary") == "meta/llama-3.1-8b-instruct"        # remote: trusts the configured model, no probe
    assert not AIClient(C.NIM_BASE).usable()                                          # remote without key
    local = AIClient("http://localhost:11434")
    assert local._url("chat/completions") == "http://localhost:11434/v1/chat/completions"
    assert local.usable() and local.is_local and "Authorization" not in local._headers()
    local.configure(api_key="abc", model="m")
    assert local.api_key == "abc" and local.model == "m" and local.base == "http://localhost:11434"


def test_private_network_endpoints_need_no_key():
    """Ollama / LM Studio on another LAN box is usable without a key; public hosts still need one. No network is touched."""
    for base in ("http://192.168.1.3:11434", "http://10.0.0.5:8000/v1", "http://172.20.1.9:1234", "http://169.254.1.1:1",
                 "http://[fd00::5]:1", "http://gpubox:11434", "http://nas.local:11434", "http://host.docker.internal:1234"):
        client = AIClient(base)
        assert host_kind(base) == "private" and client.is_private and not client.is_local, base
        assert not client.needs_key and client.usable() and "Authorization" not in client._headers(), base
    for base in ("http://127.0.0.1:1234", "http://localhost:11434", "http://[::1]:8080", "http://0.0.0.0:1", "localhost:1234"):
        assert host_kind(base) == "loopback" and AIClient(base).is_local and AIClient(base).usable(), base
    for base in ("https://integrate.api.nvidia.com/v1", "https://openrouter.ai/api/v1", "http://172.32.1.9:1", "http://8.8.8.8:1",
                 "integrate.api.nvidia.com/v1", "http://[::1"):
        client = AIClient(base)
        assert host_kind(base) == "public" and client.needs_key and not client.is_private and not client.usable(), base
        client.configure(api_key="k"); assert client.usable(), base
    assert host_kind("") == "public" and AIClient("").is_local                     # empty base falls back to the LM Studio default


def test_provider_resolution_follows_policy(mock_ai):
    local_ok, local_down = AIClient(mock_ai.base), AIClient("http://127.0.0.1:9")
    alt, alt_nokey = AIClient(C.NIM_BASE, api_key="k"), AIClient(C.NIM_BASE)      # remote: never contacted by the resolver
    base = {"ai_enabled": True, "alt_enabled": True}
    assert resolve_provider({**base, "dict_ai": "off"}, local_ok, alt) is None
    assert resolve_provider({**base, "dict_ai": "local"}, local_ok, alt) is local_ok
    assert resolve_provider({**base, "dict_ai": "local"}, local_down, alt) is None
    assert resolve_provider({**base, "dict_ai": "alt"}, local_ok, alt) is alt
    assert resolve_provider({**base, "dict_ai": "alt"}, local_ok, alt_nokey) is None
    assert resolve_provider({**base, "alt_enabled": False, "dict_ai": "alt"}, local_ok, alt) is None
    assert resolve_provider({**base, "dict_ai": "auto"}, local_ok, alt) is local_ok
    assert resolve_provider({**base, "dict_ai": "auto"}, local_down, alt) is alt
    assert resolve_provider({**base, "dict_ai": "auto"}, local_down, alt_nokey) is None
    assert resolve_provider({**base, "alt_enabled": False, "dict_ai": "auto"}, local_down, alt) is None
    assert resolve_provider({**base, "ai_enabled": False, "dict_ai": "auto"}, local_ok, alt) is alt
    assert resolve_provider({**base, "ai_enabled": False, "dict_ai": "local"}, local_ok, alt) is None
    assert resolve_provider({**base, "dict_ai": "bogus"}, local_ok, alt) is local_ok                # unknown -> auto
    assert resolve_provider({}, local_ok, alt) is local_ok                                          # defaults: auto, local enabled
    lan = AIClient("http://192.168.1.3:1")                                                          # keyless LAN box: usable, never probed here
    assert resolve_provider({**base, "dict_ai": "alt"}, local_ok, lan) is lan
    assert resolve_provider({**base, "dict_ai": "auto"}, local_down, lan) is lan
    assert resolve_provider({**base, "alt_enabled": False, "dict_ai": "alt"}, local_ok, lan) is None
    assert mock_ai.count("/models") == 1                                                            # reachability is cached


def test_reachability_cache_expires_and_can_be_invalidated(mock_ai):
    client = AIClient(mock_ai.base)
    assert client.reachable() and client.reachable() and mock_ai.count("/models") == 1
    assert client.reachable(ttl=0) and mock_ai.count("/models") == 2
    client.invalidate(); assert client.reachable() and mock_ai.count("/models") == 3
    client.configure(base=mock_ai.base); assert client.reachable() and mock_ai.count("/models") == 4


def test_token_logger_and_alt_model_are_used(mock_ai):
    log = []
    AIClient(mock_ai.base, lambda *a: log.append(a)).chat("hi", "chat", "en")
    alt = AIClient(mock_ai.base, lambda *a: log.append(a), api_key="k", model=mock_ai.MODEL)
    assert D.ai_lookup(alt, "x", "de") and mock_ai.chats[-1]["body"]["model"] == mock_ai.MODEL
    assert mock_ai.chats[-1]["body"]["temperature"] <= 0.2 and mock_ai.chats[-1]["body"]["messages"][0]["role"] == "system"
    assert [(row[0], row[1], row[2], row[3], row[5]) for row in log] == [(mock_ai.MODEL, "chat", 42, 17, True), (mock_ai.MODEL, "dictionary", 42, 17, True)]


def test_entry_defaults_and_table_roundtrip_keep_example(tmp_path):
    e = D.Entry("Haus", "n", "das Häuser", "house")
    assert e.example == "" and e.source == D.SOURCE_BUILTIN
    ai = D.Entry("Zzqqxx", "n", "das Zzqqxxe", "zzq-thing", "n", D.SOURCE_AI, "Das Zzqqxx ist alt.")
    out = tmp_path / "ai.csv"
    assert D.write_table(out, [ai]) == 1
    back = D.read_table(out)[0]
    assert back.example == "Das Zzqqxx ist alt." and back.source == D.SOURCE_USER
    d = D.build_dictionary([("Zzqqxx", "zzq-thing", "n", "das Zzqqxxe", "", "ai", "Das Zzqqxx ist alt."), ("Qqzz", "qqz-fence", "n", "der Qqzze", "", "bogus", "")])
    by = d.count_by_source()
    assert by.get(D.SOURCE_AI, 0) == 1 and d.lookup("Qqzz")[1][0].source == D.SOURCE_USER
    assert d.lookup("Zzqqxx")[1][0].example == "Das Zzqqxx ist alt."
    assert d.contains(ai) and not d.contains(D.Entry("nope", "n", "", "nothing"))
    assert d.contains(D.Entry("Haus", "n", "das Häuser", "house", "", D.SOURCE_AI))      # duplicates of built-in entries are recognised


# ---------------------------------------------------------------------------
# Thinking models (gemma-4 / qwen3): reasoning_effort field, truncated-answer retry, model ranking
# ---------------------------------------------------------------------------
def test_local_client_sends_reasoning_off_and_records_finish_reason(mock_ai):
    mock_ai.reasoning_tokens = 3
    client = AIClient(mock_ai.base)
    assert client.is_local
    entries = D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    assert entries and entries[0].source == D.SOURCE_AI
    body = mock_ai.chats[-1]["body"]
    assert body.get("reasoning_effort") == "none" and body["max_tokens"] == D.AI_MAX_TOKENS
    assert client.last_finish_reason == "stop" and client.last_reasoning_tokens == 3


def test_remote_client_does_not_send_reasoning_field(mock_ai):
    class RemoteClient(AIClient):                     # hosted endpoint stand-in
        is_local = property(lambda self: False)

    client = RemoteClient(mock_ai.base, api_key="k")
    assert D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    assert "reasoning_effort" not in mock_ai.chats[-1]["body"]
    assert AIClient(mock_ai.base).is_local                       # class property untouched


def test_server_rejecting_extra_fields_gets_a_retry_without_them(mock_ai):
    mock_ai.reject_fields = {"reasoning_effort"}
    client = AIClient(mock_ai.base)
    assert D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    chats = mock_ai.chats
    assert len(chats) == 2
    assert "reasoning_effort" in chats[0]["body"] and "reasoning_effort" not in chats[1]["body"]


def test_truncated_empty_answer_is_retried_with_a_bigger_budget(mock_ai):
    mock_ai.queue = [("", "length"), (mock_ai.content, "stop")]
    client = AIClient(mock_ai.base)
    assert D.ai_lookup(client, mock_ai.sample[0]["headword"], "en")
    chats = mock_ai.chats
    assert len(chats) == 2 and chats[1]["body"]["max_tokens"] == D.AI_MAX_TOKENS * 3
    mock_ai.queue = [("Sorry, I cannot help with that.", "stop")]          # not truncated: no retry
    assert D.ai_lookup(client, "zzqqxx", "en") == [] and len(mock_ai.chats) == 3


def test_rank_models_skips_specialist_models_and_prefers_fitting_general_models():
    from gca import ai_client as A
    installed = ["qwen/qwen3.6-35b-a3b", "google/gemma-4-12b-qat", "qwen/qwen3-vl-8b", "biomistral-7b",
                 "qwen2.5-math-7b-instruct", "moondream-2b-2025-04-14", "text-embedding-nomic-embed-text-v1.5"]
    ranked = A.rank_models(installed, "dictionary")
    assert ranked[0] == "google/gemma-4-12b-qat"
    assert "qwen2.5-math-7b-instruct" not in ranked and "text-embedding-nomic-embed-text-v1.5" not in ranked
    assert A.rank_models(["text-embedding-x"], "chat") == ["text-embedding-x"]
    assert A.rank_models(["gemma-4-12b-qat", "qwen2.5-7b-instruct"], "chat")[0] == "qwen2.5-7b-instruct"
    assert A.model_size_b("qwen/qwen3.6-35b-a3b") == 35.0 and A.is_specialist("qwen/qwen3-vl-8b")


def test_choose_model_avoids_specialist_models(monkeypatch, mock_ai):
    client = AIClient(mock_ai.base)
    monkeypatch.setattr(client, "models", lambda timeout=1.5: ["qwen2.5-math-7b-instruct", "google/gemma-4-12b-qat"])
    assert client.choose_model("dictionary") == "google/gemma-4-12b-qat"


def test_ai_noun_extra_drops_repeated_headword_and_dash_plural():
    if C.TARGET_LANG not in ("de", "fr"):
        return
    if C.TARGET_LANG == "de":
        rows = ('[{"headword": "das Fernweh", "pos": "n", "extra": "das Fernweh", "translation": "wanderlust"},'
                ' {"headword": "Haus", "pos": "n", "extra": "das Haus Häuser", "translation": "house"},'
                ' {"headword": "die Prokrastination", "pos": "n", "extra": "die -", "translation": "procrastination"}]')
        entries = D.parse_ai_entries(rows)
        assert [(e.headword, e.extra, e.plural) for e in entries] == [
            ("Fernweh", "das", ""), ("Haus", "das Häuser", "Häuser"), ("Prokrastination", "die", "")]
        assert entries[0].display == "das Fernweh"
        extra = D.parse_ai_entries('[{"headword": "der Ohrwurm", "pos": "n", "extra": "die Ohrwürmer", "translation": "earworm"}]')[0]
        assert (extra.extra, extra.plural, extra.display) == ("der Ohrwürmer", "Ohrwürmer", "der Ohrwurm")
    else:
        rows = ('[{"headword": "le cafard", "pos": "n", "extra": "m cafard", "translation": "blues"},'
                ' {"headword": "la nostalgie", "pos": "n", "extra": "f -", "translation": "nostalgia"}]')
        entries = D.parse_ai_entries(rows)
        assert [(e.headword, e.extra, e.plural) for e in entries] == [("cafard", "m", ""), ("nostalgie", "f", "")]
