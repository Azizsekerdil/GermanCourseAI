# German Course AI

German Course AI is an independent Windows desktop learning app built around local-first student data. Its Turkish, English and German interfaces expose the same feature set and German-specific content.

> Core learning features and student data are local. Opening resource links and using optional remote services requires the internet, so the app does not make a misleading “100% offline” claim.

## Features

- SM-2/Leitner spaced review, daily goal and streak
- 160 built-in A1 words with noun article, gender and plural
- German-Turkish-English dictionary, favorites and mistake drills
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

Prompt and response text is not persisted. The token ledger stores only model, task, token counts, duration and success status. NVIDIA NIM is disabled by default, and API keys are never written to the settings file.

## Privacy and optional internet use

- Profiles, progress, exams, PDF notes and counters live in a separate local SQLite database.
- SRS, exams, dictionary, grammar and packs work without internet access.
- Resource links open only on user action and use the internet.
- Remote AI services are optional and off by default.

## Tests

```powershell
python -m pytest -q
```

The suite covers the window and all 17 pages, immediate/persistent language switching, complete i18n catalogs, migrations, 150+ seed words, SRS, study/exam flows, German search equivalence, strict spelling, Unicode CSV, offline AI behavior, token privacy and pack round-trips.

## Structure

```text
German_Course_AI.pyw    entry point
gca/                    independent Python package
  tabs/                 modular learning, lab, reading and system pages
  db.py                 SQLite schema, migrations and repositories
  srs.py                SM-2 / Leitner scheduling
  content.py            German-specific learning content
  seed_words.py         original A1 starter vocabulary
  ai_client.py          LM Studio client
tests/                  automated tests
grammar/                offline grammar notes
Resources/              learner-owned course files
docs/presentation/      editable PPTX, PDF and screenshots
```
