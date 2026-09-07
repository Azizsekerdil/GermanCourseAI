# German Course AI

German Course AI is an independent Windows desktop learning app built around local-first student data. Its Turkish, English and German interfaces expose the same feature set and German-specific content.

> Core learning features and student data are local. Opening resource links and using optional remote services requires the internet, so the app does not make a misleading “100% offline” claim.

User guide: [docs/USER_GUIDE.md](docs/USER_GUIDE.md) — installation, the 18 screens, the dictionary, the AI setup and troubleshooting.

## Features

- SM-2/Leitner spaced review, daily goal and streak
- 160 built-in A1 words with noun article, gender and plural
- German-Turkish-English dictionary, favorites and mistake drills
- Trilingual **German ↔ English ↔ Turkish dictionary** tab: 1,260+ built-in entries with article and plural, direction selector (`Auto`, `DE → EN`, `EN → DE`, `DE → TR`, `TR → DE`; a fixed direction searches only the source language and the choice is saved), Turkish column and detail line, plural/umlaut/ß-tolerant search, TTS, add-to-word-bank (the Turkish gloss becomes the word's `tr` field when present), CSV/TSV import/export (`tr` column; header row recognised, old layout accepted; a user row for a built-in word replaces its Turkish gloss)
- **AI-assisted dictionary**: words missing from the dictionary are looked up as structured JSON through LM Studio or an alternative OpenAI-compatible endpoint (NVIDIA NIM or any URL + API key); results (article/plural, English and Turkish translation, example sentence, note) are cached in the local dictionary and work offline afterwards; when a `DE → TR` search finds an entry without a Turkish gloss the AI is asked in the background and the gloss is added to that same entry (no duplicate)
- Cards, multiple choice, typing, listening and matching study modes
- CEFR A1-C1 profiles and a scored exam engine
- German spelling and sound lab for umlauts, ß, capitalization, vowel length, major consonant patterns, compounds and stress
- Grammar labs for four cases, articles, adjectives, pronouns, verb systems, word order, past tenses, prepositions, comparison, numbers, time and dates
- Pronunciation, speaking, free writing and handwriting tools
- Local PDF text reading and page notes
- Open-license Resource Center with visible license and attribution
- Local AI tutor through LM Studio for explanation, translation, correction, conversation and vision/OCR tasks
- Per-task model profiles and a text-free token ledger
- Weekly progress report, light/dark themes and learner profiles
- Unicode CSV and `.gcapack` import/export

## Install and run from source

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\German_Course_AI.pyw
```

User data is stored under `%APPDATA%\GermanCourseAI`. Set `GCA_HOME` to an isolated folder for testing or portable evaluation.

## Build the Windows EXE

```powershell
python -m pip install -r requirements-dev.txt
.\build.bat
```

Output: `dist\GermanCourseAI.exe`. Build output and user data are excluded from Git.

## Local AI

Install LM Studio, download a chat model, and start its OpenAI-compatible Local Server. The default endpoint is `http://127.0.0.1:1234`. If the server is unavailable, only AI functions are disabled; the app keeps running.

Prompt and response text is not persisted. The token ledger stores only model, task, token counts, duration and success status.

### Dictionary AI provider

The dictionary tab can use two providers:

- **LM Studio** (local, no key) — `app.ai`, the address above.
- **Alternative endpoint** — any OpenAI-compatible API: the default is `https://integrate.api.nvidia.com/v1` (NVIDIA NIM, model `meta/llama-3.1-8b-instruct`), but another base URL such as OpenRouter, Groq or Ollama, a model name and an API key can be entered. Enable it on the Settings page and check it with "Test connection". A server on the local network (e.g. `http://192.168.1.10:11434`, `.local` names) needs no API key; public hosts do.

The **Dictionary AI provider** policy (Settings page and the dictionary toolbar) is `Auto` (LM Studio if reachable, otherwise the alternative endpoint if enabled), `LM Studio`, `Alternative` or `Off`. When a search finds nothing locally the AI is asked in the background; the entries it returns are listed with source `AI` and, by default, stored in the `dict_entries` table; answers that merely restate a headword the dictionary already knows are not stored (use "Save to dictionary" if wanted). "Ask AI" merges AI entries on top of the list even when local results exist; those are never autosaved. The AI is asked for both `translation_en` and `translation_tr`; when a `DE → TR` search finds an entry without a Turkish gloss the AI is asked automatically and the returned gloss is written into the existing entry (for built-in entries an `ai`-sourced twin row lands in `dict_entries`; no new entry is created). A further Turkish sense the AI returns for an entry that already has a gloss is appended to it, never overwritten; "Random word" and the lookup history always find their word on the headword side, whatever direction is selected.

The API key is stored in the Windows Credential Manager (`GermanCourseAI/alt_api_key`); off Windows, or if the API fails, it falls back to `settings/secrets.json`. The key is never written to `settings.json`. The `GERMANCOURSEAI_API_KEY` environment variable overrides the stored key.

## Privacy and optional internet use

- Profiles, progress, exams, PDF notes and counters live in a separate local SQLite database.
- SRS, exams, dictionary, grammar and packs work without internet access.
- Resource links open only on user action and use the internet.
- Remote AI services are optional and off by default; the API key lives in the Credential Manager, never in the settings file.

## Tests

```powershell
python -m pytest -q
```

The suite covers the window and all 18 pages, immediate/persistent language switching, complete i18n catalogs, migrations, 150+ seed words, the 1,260+-entry dictionary engine (fixed and automatic directions, Turkish field, import/export, SQLite user entries), AI dictionary lookup against a local mock OpenAI server (JSON parsing, Bearer header, provider resolution, the dictionary-tab flow), the secret store (file backend), the `dict_entries` schema migration, SRS, study/exam flows, German search equivalence, strict spelling, Unicode CSV, offline AI behavior, token privacy and pack round-trips. Tests never touch the real network or the Credential Manager.

## Structure

```text
German_Course_AI.pyw    entry point
gca/                    independent Python package
  tabs/                 modular learning, lab, reading and system pages
  db.py                 SQLite schema, migrations and repositories
  srs.py                SM-2 / Leitner scheduling
  content.py            German-specific learning content
  seed_words.py         original A1 starter vocabulary
  dictionary.py         dictionary engine and structured AI lookup
  dict_data.py          built-in DE-EN-TR dictionary data
  ai_client.py          OpenAI-compatible client (LM Studio, NIM, ...) and provider resolution
  secrets.py            API-key store (Credential Manager / file fallback)
tests/                  automated tests
grammar/                offline grammar notes
Resources/              learner-owned course files
docs/presentation/      editable PPTX, PDF and screenshots
```
