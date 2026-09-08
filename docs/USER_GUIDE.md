# German Course AI - User Guide

## Table of contents

- [1. About this guide](#1-about-this-guide)
- [2. Installation](#2-installation)
- [3. First launch](#3-first-launch)
- [4. Screens](#4-screens)
- [5. Dictionary (in detail)](#5-dictionary-in-detail)
- [6. Artificial intelligence](#6-artificial-intelligence)
- [7. Data management](#7-data-management)
- [8. Shortcuts and tips](#8-shortcuts-and-tips)
- [9. Troubleshooting](#9-troubleshooting)
- [10. Release notes summary](#10-release-notes-summary)
- [11. Frequently asked questions](#11-frequently-asked-questions)
- [12. License](#12-license)

---

## 1. About this guide

This document covers **German Course AI** version **1.3.0**. The application is a standalone desktop program for learning German: it runs on Windows and macOS, keeps your data on your own computer, and performs every feature except the AI ones without an internet connection.

You do not have to read the guide end to end: see [2](#2-installation) and [3](#3-first-launch) for the first setup, [4](#4-screens) for what a screen does, and [5](#5-dictionary-in-detail) for the details of the dictionary.

Every button and field name is quoted as it appears with the interface language set to **English**. The interface language can be **Türkçe**, **English** or **Deutsch**.

---

## 2. Installation

### Windows (zip archive)

1. Download `GermanCourseAI-Windows.zip`.
2. Right-click the archive and use **Extract All** to unpack it into a folder.
3. Double-click **`GermanCourseAI.exe`** in that folder.

There is no setup wizard, no administrator rights are needed and nothing is written to the registry. To remove the program, delete the folder; your data lives in a separate folder and is not deleted.

The archive also contains `LICENSE` (MIT) and `THIRD_PARTY_NOTICES.md` (third-party component notices) next to the executable.

### macOS (zip archive)

The macOS package is distributed as `GermanCourseAI-macOS.zip` for Apple Silicon Macs.

1. Open the archive; `GermanCourseAI.app` appears. Move the app to your **Applications** folder.
2. The app is **not notarized** by Apple. On the first launch, instead of double-clicking, **right-click the icon → Open** and confirm with **Open** in the warning. This confirmation is needed only once.

### Running from source

Python 3.11 or newer is required. The only runtime dependency is `pypdf`, which reads PDF text.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python .\German_Course_AI.pyw
```

To build your own executable run `python -m pip install -r requirements-dev.txt` and then `.\build.bat`; the output is `dist\GermanCourseAI.exe`. The macOS package is built on a Mac with `./build_macos.sh`, which produces `dist/GermanCourseAI.app` and `dist/GermanCourseAI-macOS.zip`.

### Where the data is kept

Learner data is not stored in the program folder but in a separate user folder.

| System | Default data folder |
| --- | --- |
| Windows | `%APPDATA%\GermanCourseAI` |
| macOS / Linux | `~/.germancourseai` |

It contains `data\` (the SQLite database `GermanCourseAI.db`), `settings\`, `exports\` and `downloads\`. For portable use, define the **`GCA_HOME`** environment variable; the program writes all of its data into that folder:

```powershell
$env:GCA_HOME = "E:\GermanCourseAI-Data"
.\GermanCourseAI.exe
```

---

## 3. First launch

The window opens at 1360 × 860 (minimum 1080 × 700): a grouped navigation bar on the left, a toolbar strip on top, a status line at the bottom.

On the first run the data folder and the SQLite database are created, the default profile named **Alex** is opened, the built-in **161 A1 words** are written into the word bank, and the built-in **1267-entry German-English-Turkish dictionary** is loaded; the dictionary ships inside the program and needs no download.

You are then advised to set the following:

- **Interface language:** pick **Türkçe**, **English** or **Deutsch** from the list next to the 🌐 icon in the top strip. The change is applied immediately and saved.
- **Profile:** the list to the right of the language list shows the active learner; the **+** button between them creates a new profile. Progress, exams and PDF notes are per profile; the word bank and the dictionary are shared.
- **Theme:** in **Settings → Theme** choose `dark` (default) or `light` and press **Save**.
- **Daily goal:** **Settings → Daily goal** defaults to 20; you may pick any value from 5 to 200.

The **AI:** label at the right of the top strip shows the state of the local AI server (**Available** / **Unavailable**). This is not an error; the whole program works without AI.

---

## 4. Screens

The left navigation bar splits 18 pages into five groups.

| Group | Icon | Page | In short |
| --- | --- | --- | --- |
| LEARN | ↻ | Spaced Review | SM-2 / Leitner card practice |
| LEARN | Aa | Word Bank | Word list and CSV |
| LEARN | 📖 | Dictionary DE-EN-TR | Trilingual dictionary, AI lookup |
| LEARN | ✓ | Exam | Scored multiple-choice exam |
| LABS | Äß | Spelling & Sound | Alphabet, umlauts, ß, dictation |
| LABS | ◖ | Pronunciation | Speech and sound rules |
| LABS | § | Grammar | 24 topics and exercises |
| READ & EXPLORE | ◇ | Resource Center | Openly licensed external sources |
| READ & EXPLORE | ▤ | PDF Reader | PDF text and page notes |
| READ & EXPLORE | ▣ | Course Library | Your own course files |
| PRACTICE | ✦ | AI Tutor | Explain, translate, correct, OCR |
| PRACTICE | ◌ | Speaking | Scenario-based dialogue |
| PRACTICE | ✎ | Writing & Handwriting | Writing, AI correction, canvas |
| PROGRESS & SYSTEM | ↗ | Progress | Goal, streak, weekly chart |
| PROGRESS & SYSTEM | ⬡ | Packs | `.gcapack` transfer |
| PROGRESS & SYSTEM | # | Token Ledger | AI usage summary |
| PROGRESS & SYSTEM | ? | Offline Guide | In-app guide |
| PROGRESS & SYSTEM | ⚙ | Settings | Theme, goal, speech, AI |

**LEARN group**

### Spaced Review

**What it does.** Uses the SM-2 algorithm and Leitner boxes to work out which word to review when. The four boxes on top show **Due today**, **New**, **Mistakes** and **Favorites**.

**How to use it.** Pick the queue (`new`, `due`, `wrong`, `favorites`) and the mode (**Cards**, **Multiple choice**, **Typing**, **Listening**, **Matching**), set the card count (5-50, default 10) and press **Start**. **Show answer** reveals the Turkish and English gloss plus the example sentence; then rate yourself with **Again**, **Hard**, **Good** or **Easy**. The next date is calculated from that; when the queue is empty **Session complete** appears.

**Tip.** In this version all five modes use the same card flow; only in **Listening** mode is the word also read aloud as the card opens.

### Word Bank

**What it does.** Keeps your German-Turkish-English word list with article and plural information; Spaced Review and Exam draw their cards from here.

**How to use it.** Type in the search box and press **Search** or `Enter`; the search runs across all three languages at once. The columns are **German**, **Turkish**, **English**, **Article**, **Plural** and **Deck**; selecting a row shows the example sentences underneath. **★ Favorite** toggles the favorite flag; **↑ Export** and **↓ Import** work with UTF-8 CSV.

**Tip.** Imported words with no deck given land in a deck named `İçe Aktarılan` - a fixed label that does not follow the interface language.

### Dictionary DE-EN-TR

**What it does.** A trilingual dictionary made of 1267 built-in entries, your own entries and the entries the AI has cached. See [5. Dictionary](#5-dictionary-in-detail) for the details.

**How to use it.** Type a word; from two characters on the list filters itself, and `Enter` or **Search** runs the full lookup. The panel on the right shows the headword, part of speech, article/plural, the English and Turkish gloss, the example sentence and the note.

**Tip.** **🎲 Random word** opens a random built-in entry - ideal as a daily warm-up.

### Exam

**What it does.** Generates multiple-choice questions from the word bank, records the answers and scores them as a percentage.

**How to use it.** Choose a value between 5 and 50 with **Question count** and press **Start**. Each question shows a German word; pick the correct Turkish gloss out of four options and press **Check**. At the end the **Exam complete** screen and the **Score** percentage appear; the result feeds the weekly report.

**Tip.** Every exam record is stored together with the CEFR level from the settings (default `A1`).

**LABS group**

### Spelling & Sound

**What it does.** Lists 15 spelling rules - the German alphabet, `Ä/Ö/Ü`, `ß`, capitalised nouns and so on - with examples, and includes a short dictation exercise.

**How to use it.** Select a symbol in the table on the left; its rule appears on the right. In the **Dictation exercise** section press **▶ Speak**, type the word you heard and press **Check**; a `✓` confirms it, otherwise the correct spelling is shown.

**Tip.** The comparison is sensitive to case and umlauts: type `Strasse` and you get `Straße` back as the correction.

### Pronunciation

**What it does.** Presents nine German-specific sound rules (`ch` twice - after `i/e` and after `a/o/u` - plus `r`, `z`, `sch`, `sp/st`, `ei/ie`, `eu/äu`, `w/j`) with IPA notation and examples.

**How to use it.** Type a word into the box on top and press **▶ Speak**. The **◉ Compare with microphone** button is not active in this version; it answers **Unavailable**.

**Tip.** The box starts with `Mädchen`, a good example for hearing both an umlaut and the `ch` sound.

### Grammar

**What it does.** Presents 24 German topics, from Nominativ to compound nouns, as rule, example and exercise.

**How to use it.** Pick a topic in the list on the left; the title, the rule and an example sentence appear on the right. An exercise follows underneath: choose an option and press **Check** to see the correct answer and the explanation. **Next** brings a new exercise; results are recorded per topic.

**Tip.** Exercises come from a shared pool of 18 questions, so you can keep pressing **Next** without changing the topic.

**READ & EXPLORE group**

### Resource Center

**What it does.** Lists four external sources that are public domain or Creative Commons only (Wikibooks, Tatoeba, LibriVox, Project Gutenberg) with level, **License** and **Attribution**.

**How to use it.** The **Open ↗** button on a card opens the link in your default browser. The notice on top reminds you that opening links uses the internet.

**Tip.** No content is copied into the program; public-domain status varies by country, so read the licence line.

### PDF Reader

**What it does.** Shows the text of a PDF on your computer page by page and lets you keep a separate note for each page.

**How to use it.** Open a file with **Choose PDF** and move through it with the **Page** spinner; the text appears in the left pane. Write into the **Page note** field on the right and press **Save**. The last PDF you opened is remembered and loaded again when you reopen the page.

**Tip.** Notes are tied to the triple of profile, file path and page.

### Course Library

**What it does.** Collects the course files (PDF, audio, text) you put into the `Resources` folder next to the program in a single list.

**How to use it.** **Open course folder** opens the folder in Explorer (Windows only) so you can copy your files there; **Refresh** reloads the list. The table shows name, type and size in MB; **double-clicking** a row opens the file in its default program (Windows only as well).

**Tip.** The `BURAYA_DERS_KOYUN.txt` placeholder in the folder is not shown in the list.

**PRACTICE group**

### AI Tutor

**What it does.** Uses the local AI for grammar explanations, translation, correction and reading text from an image (OCR).

**How to use it.** Pick **Explain**, **Translate**, **Correct** or **Image / OCR** from the **Task** list, type your text and press **Send**; the answer appears in the box below. For an image, choose a PNG/JPG/WEBP file with the **Image / OCR** button; if the text box is empty the program uses a built-in instruction.

**Tip.** The 🔒 line at the bottom repeats the privacy promise: prompt and response text is never saved, only token counts are logged.

### Speaking

**What it does.** Gives you German role-play practice in five everyday scenarios (`Im Café`, `Am Bahnhof`, `Im Hotel`, `Beim Einkaufen`, `Beim Arzt`).

**How to use it.** Pick a **Scenario** and press **Start conversation**; the AI takes the other role and asks one short question. Type your German reply and press **Send**; you are gently corrected where needed and the conversation continues with a new question.

**Tip.** The dialogue is kept short at A1 level; raising the number of turns helps more than long sentences.

### Writing & Handwriting

**What it does.** Offers free-writing practice, AI correction and an area where you can practise writing with the mouse.

**How to use it.** Write your German text into the left box (the default prompt asks what you did today) and press **Correct with AI**; the corrected text, the name of the rule and a short explanation appear below. Draw into the **Handwriting area** on the right with the mouse; **Clear** wipes it.

**Tip.** The handwriting area is not saved, and your text is sent only when you press **Correct with AI**.

**PROGRESS & SYSTEM group**

### Progress

**What it does.** Shows the **Daily goal**, the **Day streak**, the number of words **Studied** and **Learned**, and a bar chart of the **Last 7 days**.

**How to use it.** The metrics and the chart are calculated as soon as the page opens. The **Weekly report** line under the chart gives the correct, wrong and percentage score of the last seven days.

**Tip.** "Learned" counts the words that have reached Leitner box 4 or above.

### Packs

**What it does.** Writes your word list - optionally together with your progress - into a portable `.gcapack` file and reads it back.

**How to use it.** Tick **Include progress** as you wish and save the file with **↑ Export**; read it on another computer with **↓ Import**. The number of words taken over is shown on screen.

**Tip.** A pack checks the target language; a pack made for another language is not imported.

### Token Ledger

**What it does.** Keeps a local summary of the AI calls: **Calls**, **Total tokens** and a breakdown of the last 500 calls.

**How to use it.** Just open the page. The columns are timestamp, model, task, prompt tokens, completion tokens, total tokens, duration (ms) and success flag.

**Tip.** The ledger holds no request or response text at all; the 🔒 note at the bottom says so.

### Offline Guide

**What it does.** Summarises inside the app which features work without the internet, how the dictionary directions work, what the AI options are and where the data is kept.

**How to use it.** Open the page and read the text. The full path of your data folder is printed at the bottom.

**Tip.** The text follows the interface language.

### Settings

**What it does.** Gathers the theme, daily goal, speech, local AI and alternative endpoint options.

**How to use it.** Fill in the fields and press **Save**. The page re-reads the settings every time it is opened, so an AI policy you changed from the dictionary toolbar shows up here as well.

| Field | Meaning | Default |
| --- | --- | --- |
| Theme | `dark` / `light` | `dark` |
| Daily goal | Card goal between 5 and 200 | `20` |
| Text to speech | Speech on/off | On |
| Local AI | Use of LM Studio on/off | On |
| LM Studio address | Local server address | `http://127.0.0.1:1234` |
| Default model | Local model name | `qwen2.5-7b-instruct` |
| Dictionary AI provider | Auto / LM Studio / Alternative / Off | Auto |
| Save AI dictionary results into the dictionary | Cache found entries and complete missing Turkish glosses | On |
| Use the alternative endpoint | Second provider on/off | Off |
| Base URL | OpenAI-compatible address | `https://integrate.api.nvidia.com/v1` |
| Model | Alternative endpoint model | `meta/llama-3.1-8b-instruct` |
| API key | Secret key (masked) | empty |

**Tip.** The **Default model** list shows the profiles the app knows, not the models you have installed: `gemma-2-9b-it`, `llama-3.1-8b-instruct`, `llava-v1.6-mistral-7b`, `qwen2-vl-7b-instruct`, `qwen2.5-14b-instruct`, `qwen2.5-7b-instruct`. You may also type another name by hand.

---

## 5. Dictionary (in detail)

The dictionary keeps three languages side by side: the headword in **German**, the glosses in **English** and **Turkish**. Three sources are merged: the built-in core dictionary, your own entries and the entries the AI has cached.

### Direction selector

The **Direction:** list on the second toolbar row offers five options.

| Code | Label | What it does | When to choose it |
| --- | --- | --- | --- |
| `auto` | Auto | Searches all three sides at once, the best-matching side wins | When you do not want to think about the language you typed |
| `de2en` | DE → EN | Searches German headwords only | For the English of a German word |
| `en2de` | EN → DE | Searches English glosses only | Going from English into German |
| `de2tr` | DE → TR | Searches German headwords, moves the Turkish column to the front | For the Turkish of a German word |
| `tr2de` | TR → DE | Searches Turkish glosses only | Going from Turkish into German |

A fixed direction scans the source language only: in `de2tr` typing `ev` returns nothing, because there is no German headword `ev`. Your choice is saved and still applies after a restart; when you change the direction, a query already in the box is searched again. The small label to the right of the search box says which direction the result was found in (`DE → TR` and so on) - in **Auto** mode it shows the direction the program actually detected.

### The Turkish column and the detail panel

The result table has the columns **German**, **English**, **Turkish**, **Part of speech**, **Article / Plural** and **Source**. In the `*2tr` directions the Turkish column moves right next to the headword; entries whose Turkish gloss is unknown show `—` in that cell.

The panel on the right shows the selected entry in a large font: the headword with its article (`das Haus`), part of speech and gender, plural, the **English:** and **Turkish:** lines, the example sentence and the note. If the word is already in the word bank, a `★ Word Bank: …` line appears.

### Search rules

Ranking is strict: **exact match > prefix > word start > substring**. In addition:

- Leading words such as `to`, `the`, `a`, `an`, `sich` are ignored; `to learn` finds the same entry as `learn`.
- Umlauts and `ß` are flexible (`ae = ä`, `oe = ö`, `ue = ü`, `ss = ß`): typing `Strasse` reaches the `Straße` entry.
- On the Turkish side the Turkish letters also fold onto their ASCII counterparts (`ı/İ → i`, `ş → s`, `ğ → g`, `ç → c`, `ö → o`, `ü → u`) and the circumflex (`kâğıt`) is ignored: `cok` finds `çok`, `ogrenmek` finds `öğrenmek`, and `isik` or `ISIK` finds `ışık`. A direct match still ranks above a folded one.
- Plural forms are searched too: typing `Häuser` finds `Haus`.
- Glosses are split into senses at `;` or `/`; a parenthesised qualifier (`ona (erkek/nesne)`) is not split.
- If nothing matches, the English note/definition field is scanned as a last resort (in **Auto** and `EN → DE` only).
- From two characters on, the list filters as you type; this "quiet" search never asks the AI. The AI only steps in for the full lookup started with `Enter` or **Search**.

### Source labels

| Label | Meaning |
| --- | --- |
| built-in | The core dictionary shipped with the program |
| user | An entry you imported by CSV or added by hand |
| AI | An entry the AI found and that was cached |

The counter at the bottom of the page adds these up separately, for example `1267 entries  ·  built-in 1267  ·  user 0  ·  AI 0`.

### Filling a missing Turkish gloss with the AI

If an entry found in the `DE → TR` direction has no Turkish gloss and the AI policy is not **Off**, the program asks the AI in the background; the status line reads **Turkish gloss missing, asking the AI…**. While **Settings → Save AI dictionary results into the dictionary** is on, the gloss that comes back is written into **that same entry** - no duplicate is created - and when it is done the message **Turkish gloss added by the AI** appears. With that box unticked the question is still asked, but nothing is stored and the message never appears.

If the AI returns a further Turkish sense for an entry that already has a gloss, that sense is appended to the existing gloss rather than overwriting it. A user row, on the other hand - imported by CSV or entered with **Add entry** - **replaces** the Turkish gloss of a built-in entry.

The **✦ Ask AI** button is an explicit request: it puts AI entries on top of the list even when local results exist. Those entries are not saved automatically; select the one you like and store it with **💾 Save to dictionary**. The **Answered by:** line under the answer names the provider and the model that replied.

### Adding to the word bank

**★ Add to word bank** writes the selected entry into the word bank. The Turkish field gets the first Turkish sense, or the first English sense when there is none; for nouns the article, gender and plural are carried over too. The deck is named **Dictionary DE-EN-TR**, so you can filter these words out later.

### CSV import and export

**↑ Export CSV** writes the results currently listed, or the whole dictionary when the list is empty. The file is suggested in the `exports` subfolder of your data folder as `dictionary_de.csv`. The column order is fixed:

| Column | Content |
| --- | --- |
| `headword` | German headword (without article) |
| `translation` | English gloss(es), separated by `;` |
| `pos` | Part-of-speech code: `n`, `v`, `adj`, `adv`, `pron`, `prep`, `conj`, `num`, `art`, `int`, `part`, `phr` |
| `extra` | For nouns the article + plural (`das Häuser`), otherwise empty |
| `note` | Note / definition / usage hint |
| `source` | `builtin`, `user` or `ai` |
| `example` | German example sentence |
| `tr` | Turkish gloss(es), separated by `;` |

```csv
headword,translation,pos,extra,note,source,example,tr
Haus,house,n,das Häuser,,builtin,,ev
Buch,book,n,das Bücher,,builtin,,kitap
lernen,to learn; to study,v,,,builtin,,öğrenmek; ders çalışmak
schnell,fast,adj,,,builtin,,hızlı
Fenster,window,n,das Fenster,,user,Das Fenster ist offen.,pencere
```

Built-in entries carry no example sentence, so the `example` column of a `builtin` row is always empty. Example sentences appear only on the entries you added yourself (`user`) and on the ones the AI found (`ai`).

**↓ Import CSV/TSV** reads `.csv`, `.tsv` and `.txt` files; the delimiter is chosen from the file type and the content. With a header row the columns may come in any order (the names `headword`, `word`, `de`, `Deutsch`, `translation`, `meaning`, `en`, `english`, `tr`, `turkish`, `türkçe` are recognised); without one the order above is expected. Older files without a `tr` column are read as well, empty rows are skipped, and everything imported is marked with the `user` source.

### Adding an entry

**+ Add entry** opens a dialog. The fields are **German**, **English**, **Turkish**, **Part of speech (n/v/adj/…)**, **Article / Plural**, **Note / definition** and **Example sentence**. If there is text in the search box, the program puts it into the field of the language it detected in **Auto** mode, and into that direction's source-language field when a fixed direction is selected, so check the fields before saving. **German** and **English** are required; leaving them empty raises **German and English fields are required.** `Enter` saves, `Esc` closes.

---

## 6. Artificial intelligence

The AI is optional. With it switched off, the dictionary, review, exam, grammar, PDF and progress features work in full.

### Installing LM Studio and the local server

1. Install LM Studio.
2. Download a chat model (recommended: `qwen2.5-7b-instruct`).
3. Start the OpenAI-compatible server in the **Local Server** section.
4. The program uses `http://127.0.0.1:1234` by default; if yours differs, correct **Settings → LM Studio address** and press **Save**.

Once connected, the **AI:** label in the top strip turns to **Available**.

### Model selection

The program keeps a model profile per task:

| Task | Preferred models |
| --- | --- |
| `chat` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `grammar` | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `translate` | `qwen2.5-7b-instruct`, `gemma-2-9b-it` |
| `correct` | `qwen2.5-7b-instruct`, `qwen2.5-14b-instruct` |
| `dialogue` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `dictionary` | `qwen2.5-7b-instruct`, `llama-3.1-8b-instruct` |
| `vision` | `qwen2-vl-7b-instruct`, `llava-v1.6-mistral-7b` |

The order of selection: the model named in the settings if it is installed; otherwise the names in the task profile; otherwise the installed models are ranked. Ranking **skips specialist models** - names containing `embed`, `rerank`, `math`, `coder`, `code-`, `moondream`, `llava`, `-vl`, `vision`, `bio`, `medic`, `whisper`, `tts`, `audio`, `clip`, `sd-` or `stable-diffusion` are meant for embeddings, maths, code, images or audio and answer dictionary tasks badly; they are still used if nothing else is left. Ties prefer models of 4-16 billion parameters and names containing `instruct`, `-it`, `chat` or `assistant`.

For dictionary calls, `reasoning_effort: none` is sent to local servers; it stops "thinking" models from spending the whole budget on reasoning and returning an empty answer. A server that rejects the field is retried without it; an answer cut short because the budget ran out is retried once with three times the budget.

### Alternative endpoint

The second provider can be any **OpenAI-compatible** service: NVIDIA NIM by default (`https://integrate.api.nvidia.com/v1`, model `meta/llama-3.1-8b-instruct`), or OpenRouter, Groq, Ollama or another server on your local network.

1. Under **Settings → Alternative endpoint** tick **Use the alternative endpoint**.
2. Fill in **Base URL** and **Model**, and paste your key into **API key** (it is masked as you type).
3. Press **Test connection**: **Connection OK · N models** appears. If the model is not listed you also get **selected model not listed**, and if no key was entered for a public host, **public host: the dictionary needs an API key to use it**.
4. Press **Save**.

A server on your local network (`http://192.168.1.10:11434` or names ending in `.local`) needs no API key; the program tells apart addresses on this machine, on the local network and on the internet, and only asks for a key on public ones.

### How the key is stored

The API key is **never** written into `settings.json`. On Windows it is kept in the **Credential Manager** as a generic credential named `GermanCourseAI/alt_api_key`; outside Windows, or if that API fails, `settings\secrets.json` is used. **Delete key** removes the record and reports **Key deleted**. If the environment variable `GERMANCOURSEAI_API_KEY` is set, it overrides the stored key.

### AI policy

The dictionary learns which provider to use from the **Dictionary AI provider** setting. The same list also sits on the dictionary toolbar behind the **AI:** label; the choice is shared.

| Policy | Behaviour |
| --- | --- |
| Auto | LM Studio if reachable; otherwise the alternative endpoint if enabled; otherwise off |
| LM Studio | Local server only (Local AI must be on and reachable) |
| Alternative | Alternative endpoint only (must be enabled and satisfy the key requirement) |
| Off | The dictionary sends no AI request (AI Tutor, Speaking and Writing still follow the **Local AI** setting) |

Depending on the choice, the status label reads **LM Studio: connected**, **Alternative: ready**, **AI unreachable** or **AI off**. The reachability answer is cached for 30 seconds.

### Token ledger

Every call adds a row to the **Token Ledger** page: timestamp, model, task, prompt tokens, completion tokens, total, duration (ms) and success flag. The two boxes on top give the total number of **Calls** and **Total tokens**; the ledger shows the last 500 calls.

### Privacy

- Request and response text is **never stored anywhere**; only the numeric token data is kept.
- The alternative endpoint is off by default; nothing goes to the internet until you enable it explicitly.
- When you use a local model, your text never leaves your computer.
- Entries found by the AI are written into the local dictionary, so the same word comes back offline next time.

---

## 7. Data management

### Profiles

The profile list in the top strip decides the active learner; the **+** button asks for a name and creates a new profile. Word progress, the study log, exams, PDF notes and grammar statistics are per profile; the word bank, the dictionary and the token ledger are shared.

### Backups

| Method | What it covers | Where |
| --- | --- | --- |
| Word CSV | The entire word bank (13 columns, UTF-8) | Word Bank → **↑ Export** |
| Dictionary CSV | Dictionary entries (8 columns) | Dictionary → **↑ Export CSV** |
| `.gcapack` pack | Words + optional progress | Packs → **↑ Export** |

The most complete backup is a copy of the data folder itself: with the program closed, copy `%APPDATA%\GermanCourseAI`, in particular `data\GermanCourseAI.db`.

### The data folder

```text
%APPDATA%\GermanCourseAI\
  data\GermanCourseAI.db      SQLite database (profiles, words, progress, dictionary, notes, token log)
  settings\settings.json      Non-secret settings
  settings\secrets.json       Only created when the Credential Manager cannot be used
  exports\                    Suggested folder for exports
  downloads\                  Folder reserved for downloads
```

The `Resources` folder holding your course files sits next to the program, not here.

### Resetting

There is no "delete everything" button inside the program; resetting is done at file level.

- **Reset progress only:** create a new profile and use it; the old profile stays untouched.
- **Reset everything:** with the program closed, delete `data\GermanCourseAI.db`. On the next launch the program rebuilds the database, the default profile and the built-in word deck.
- **Reset the settings:** delete `settings\settings.json`.
- **Remove the API key:** use **Settings → Delete key**.

---

## 8. Shortcuts and tips

The program defines no global hotkeys; the following work while the relevant field has focus.

| Shortcut | Where | What it does |
| --- | --- | --- |
| `Enter` | Dictionary search box | Runs the full lookup (asking the AI when needed) |
| `Enter` | Word Bank search box | Filters the list |
| `Enter` | Add entry dialog | Saves the entry |
| `Esc` | Add entry dialog | Closes the dialog |
| Double-click | Dictionary result row | Reads the headword aloud |
| Double-click | Course Library row | Opens the file in its default program (Windows) |

Practical tips:

- In the dictionary the list filters itself from two characters on; do not press `Enter` if you do not want a question to go to the AI.
- **Recent lookups** keeps the last 12 queries **together with their direction**; clicking one repeats the lookup in that direction, and falls back to **Auto** when that side no longer finds anything.
- **🎲 Random word** looks the word up on the headword side whatever the chosen direction, so a known German word is not needlessly sent to the AI while `TR → DE` is selected.
- **Copy** puts the entry on the clipboard as `das Haus — house — ev`.
- Changing the interface language rebuilds the pages and resets an open card session, so choose the language at the start of a session.
- A theme change is applied as soon as you press **Save**.

---

## 9. Troubleshooting

### LM Studio does not connect

**Symptom.** The top strip says **AI: Unavailable**, the dictionary says **AI unreachable**.
**Cause and fix.** The program probes the server with `GET /v1/models`. LM Studio must be running with its **Local Server** started, **Settings → LM Studio address** must match the address LM Studio shows (default `http://127.0.0.1:1234`), and **Settings → Local AI** must be ticked; a firewall may also be blocking it. The reachability answer is cached for 30 seconds, so the result may lag by half a minute; **Settings → Save** clears that cache at once. The **AI:** label in the top strip is measured only at startup - for the current state look at the status label on the dictionary page, which re-probes every time that page is opened.

### The AI returns an empty answer

**Symptom.** The dictionary says **The AI returned no entry for this query.**
**Cause and fix.** The most common cause is an unsuitable model: embedding, code, maths or vision models cannot produce structured JSON. Put a general chat model such as `qwen2.5-7b-instruct` into **Settings → Default model**. The second cause is a "thinking" model consuming the budget; the program counters that with `reasoning_effort: none` and a retry at three times the budget, but a very small model can still emit invalid JSON. If you looked up a word that does not exist, an empty answer is the correct behaviour.

### No Turkish gloss

**Symptom.** The Turkish column shows `—`.
**Cause and fix.** That entry does not carry a Turkish gloss yet. Choose **DE → TR** from the **Direction** list and repeat the search; the program asks the AI in the background and writes the gloss into the same entry. If you would rather not use the AI, fill the field yourself with **+ Add entry** or import a CSV with a `tr` column. With the **AI:** policy set to **Off**, no request is sent.

### The macOS "cannot be opened" warning

**Symptom.** A warning like "from an unidentified developer" appears.
**Cause and fix.** The app is not notarized. Instead of double-clicking, **right-click the icon → Open** and press **Open** again in the dialog. This confirmation is only needed on the first launch.

### No sound

**Symptom.** The **▶ Speak** button does nothing.
**Cause and fix.** Speech calls the Windows `System.Speech` synthesizer through PowerShell. Make sure **Settings → Text to speech** is ticked, install a **German (de-DE) voice package** from the Windows settings (without one the system default voice is used) and check the volume. This path does not exist on macOS and Linux, so speech stays silent there.

### The exe does not start

**Symptom.** Double-clicking `GermanCourseAI.exe` opens no window.
**Cause and fix.** Make sure you actually **extracted** the zip archive; running from inside the archive fails. On a SmartScreen warning choose **More info → Run anyway**. Antivirus software may quarantine PyInstaller-packed files; add the folder to its allow list. If you have no write access to `%APPDATA%`, point `GCA_HOME` at another folder. If the problem persists, run from source to see the error: `python German_Course_AI.pyw`.

### Where is my data

**Symptom.** You want to back the data up or move it to another computer.
**Cause and fix.** The full path is printed at the bottom of the **Offline Guide** page: `%APPDATA%\GermanCourseAI` on Windows, `~/.germancourseai` elsewhere. If `GCA_HOME` is set, the program uses that folder.

---

## 10. Release notes summary

| Version | Highlights |
| --- | --- |
| **v1.0.0** | An 18-page shell; SM-2 / Leitner review; 161 built-in A1 words; the exam engine; spelling, pronunciation and 24-topic grammar labs; the PDF reader; the Course Library; the Resource Center; AI Tutor, Speaking and Writing with LM Studio; the progress chart; `.gcapack` packs; the token ledger; dark/light themes; a tr/en/de interface. |
| **v1.1.0** | A separate **Dictionary** tab: built-in dictionary, source labels, search ranking, umlaut/ß tolerance, CSV/TSV import and export, adding entries, transfer to the word bank, lookup history, speech. An **AI connection** for words the dictionary does not know: structured JSON entry generation, caching of the results, an alternative OpenAI-compatible endpoint, the key stored in the Credential Manager, and the dictionary AI policy. |
| **v1.2.0** | The **direction selector** (`Auto`, `DE → EN`, `EN → DE`, `DE → TR`, `TR → DE`); a fixed direction searches only the source language and the choice is saved. The **Turkish column** and a Turkish line in the detail panel; in `*2tr` directions the Turkish column moves to the front. Completion of a missing Turkish gloss by the AI **without creating a duplicate**; extra senses appended to the existing gloss, user rows replacing it. The CSV layout with a `tr` column (the old layout is still read). The built-in dictionary grew to 1267 entries, each with a Turkish gloss. |
| **v1.2.1** | **ASCII and upper-case support for Turkish searches**: "sinav" = "SINAV" = "sınav", "cok" = "çok", "ogrenci" = "öğrenci". Turkish folding is applied before the German ö→oe folding; a match found only through folding is ranked below the direct matches, so a user typing "ask" still gets the English gloss. The displayed spelling never changes. **User guide**: `docs/KULLANIM_KILAVUZU.md` (Turkish) and `docs/USER_GUIDE.md` (English) were added to the repository, covering installation, the 18 screens, the dictionary and its direction selector, the AI setup, data management, troubleshooting and the FAQ; the PDF version is attached to the release. |
| **v1.3.0** | **MIT License**: the project is released under the MIT License; `LICENSE` and `THIRD_PARTY_NOTICES.md` were added to the repository and both files ship inside every distribution archive next to the executable. **Clean virtual-environment build**: the Windows package is now produced in a dedicated virtual environment that holds only the `requirements.txt` dependencies, so libraries the application never imports (pandas, SQLAlchemy, lxml, NumPy and the like) no longer enter the package, the file size drops noticeably, and the third-party notice travels with the package. |

---

## 11. Frequently asked questions

**Does the program work without the internet?**
Yes. The word bank, review, exams, dictionary, grammar, spelling, PDF notes, progress and packs are local. The internet is needed only for the Resource Center links and the alternative endpoint.

**Is the AI mandatory?**
No. The program runs even with LM Studio never installed; the AI buttons then answer "AI is disabled or LM Studio cannot be reached." Setting **Dictionary AI provider** to **Off** stops only the dictionary's requests; to silence every page - AI Tutor, Speaking and Writing included - untick **Settings → Local AI** and leave **Use the alternative endpoint** off.

**Does my data go to the cloud?**
No. All data lives in a SQLite file on your computer. Only if you enable the alternative endpoint does the query text go to the provider you chose; no text is stored.

**Where is my API key kept?**
On Windows in the Credential Manager as `GermanCourseAI/alt_api_key`, elsewhere in `settings\secrets.json`. It is never written into `settings.json`.

**Can two people work on the same computer?**
Yes. Create a second profile with the **+** button; progress, exams and PDF notes are separate.

**How do I import my own word list?**
Choose your UTF-8 CSV file with **↓ Import** in the Word Bank. For dictionary entries use **↓ Import CSV/TSV** on the Dictionary page; with a header row the column order does not matter.

**How many words are in the dictionary?**
The built-in dictionary holds 1267 entries, all of them with a Turkish gloss; your own entries and the cached AI entries add to that. The total is printed at the bottom of the page.

**Are entries found by the AI permanent?**
Results of lookups that were asked because the dictionary found nothing are saved automatically while **Save AI dictionary results into the dictionary** is on. Entries you requested with **✦ Ask AI** are not saved; press **💾 Save to dictionary** to keep one.

**When does the "Auto" direction get it wrong?**
When the same form is both an English and a Turkish sense - and is not itself a German headword - the English side wins. A German headword always beats the other sides: a query such as `park`, which is also a German headword, therefore comes back as `DE → EN`. Choose the direction by hand if you do not get the result you expected.

**Will an update delete my data?**
No. Replace the program folder with the new one; the data lives in a separate folder and the database schema is updated additively.

---

## 12. License

German Course AI is released under the **MIT License**. The full text lives in the `LICENSE` file
of the source repository: you may use, copy, modify and redistribute the program, the single
condition being that the copyright and licence notice travels with the copies. The program comes
with no warranty.

The third-party components the program carries inside itself - pypdf behind the PDF Reader, and
the pieces PyInstaller embeds in the frozen application such as Python, Tcl/Tk, SQLite and
OpenSSL, plus the build tools - keep their own licences. Every one of them, with its real licence
and what it is used for, is listed in `THIRD_PARTY_NOTICES.md`, which is published in the source
repository and also ships in the archive you downloaded, next to `GermanCourseAI.exe` (inside
`GermanCourseAI.app` on macOS).

No copyleft library imposes copyleft obligations on the distributed binaries. The only GPL-licensed
code present is the libgfortran runtime statically linked into NumPy's OpenBLAS library in the
Windows build; the **GCC Runtime Library Exception 3.1** it carries permits the program to be
redistributed under any licence and places no source-disclosure requirement on you. No LGPL or
AGPL library is bundled.

The external sources listed on the **Resource Center** page (Wikibooks, Tatoeba, LibriVox, Project
Gutenberg) are not copied into the program; each keeps its own licence, and that licence is shown
on the card. Course files you drop into `Resources/` stay on your computer and are never
redistributed.
