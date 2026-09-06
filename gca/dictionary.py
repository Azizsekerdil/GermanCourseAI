"""Three-language dictionary engine: target language <-> English <-> Turkish.

Layers that are merged at runtime:
1. Built-in core dictionary (``dict_data.py``; ~900 A1-B1 entries).
2. User entries imported from CSV/TSV or added by hand (SQLite ``dict_entries``).
3. AI entries produced by :func:`ai_lookup` and cached into the same table.

Every entry carries the headword (target language), an English translation and an optional
Turkish gloss (``Entry.tr``). :meth:`Dictionary.lookup` takes a direction code from
:data:`DIRECTIONS` (``auto`` | ``de2en`` | ``en2de`` | ``de2tr`` | ``tr2de`` for German; the
English app only has ``auto`` | ``en2tr`` | ``tr2en`` because its translation side already *is*
Turkish). A fixed direction searches only its source side; ``auto`` searches every side at once
and the best-scoring side decides the direction shown to the user. Ranking is
exact > prefix > word-start > substring.
"""
from __future__ import annotations

import csv
import json
import random
import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Iterable, Sequence

from . import config as C

SOURCE_BUILTIN = "builtin"
SOURCE_USER = "user"
SOURCE_AI = "ai"

POS_LABELS: dict[str, dict[str, str]] = {
    "n":    {"tr": "isim", "en": "noun", "de": "Substantiv", "fr": "nom"},
    "v":    {"tr": "fiil", "en": "verb", "de": "Verb", "fr": "verbe"},
    "adj":  {"tr": "sıfat", "en": "adjective", "de": "Adjektiv", "fr": "adjectif"},
    "adv":  {"tr": "zarf", "en": "adverb", "de": "Adverb", "fr": "adverbe"},
    "pron": {"tr": "zamir", "en": "pronoun", "de": "Pronomen", "fr": "pronom"},
    "prep": {"tr": "edat", "en": "preposition", "de": "Präposition", "fr": "préposition"},
    "conj": {"tr": "bağlaç", "en": "conjunction", "de": "Konjunktion", "fr": "conjonction"},
    "num":  {"tr": "sayı", "en": "numeral", "de": "Zahlwort", "fr": "numéral"},
    "art":  {"tr": "tanımlık", "en": "article", "de": "Artikel", "fr": "article"},
    "int":  {"tr": "ünlem", "en": "interjection", "de": "Interjektion", "fr": "interjection"},
    "part": {"tr": "parçacık", "en": "particle", "de": "Partikel", "fr": "particule"},
    "phr":  {"tr": "deyim", "en": "phrase", "de": "Wendung", "fr": "expression"},
}


@dataclass(frozen=True)
class Entry:
    headword: str
    pos: str
    extra: str            # article + plural (DE), gender/plural (FR), IPA or "" (EN)
    translation: str      # English (DE/FR apps) or Turkish (EN app); senses separated by ';'
    note: str = ""        # optional gloss / definition / usage hint
    source: str = SOURCE_BUILTIN
    example: str = ""     # optional short example sentence in the target language
    tr: str = ""          # Turkish gloss (DE/FR apps); senses separated by "; " - "" when not known yet

    def pos_label(self, lang: str) -> str:
        return POS_LABELS.get(self.pos, {}).get(lang, self.pos)

    @property
    def display(self) -> str:
        """Headword with article for German-style nouns (``das Haus``)."""
        art = self.extra.split()[0] if self.pos == "n" and self.extra.split() and self.extra.split()[0] in ARTICLES else ""
        return f"{art} {self.headword}".strip()

    @property
    def plural(self) -> str:
        toks = self.extra.split()
        if self.pos != "n":
            return ""
        toks = [t for t in toks if t not in ARTICLES and t not in GENDERS]
        return " ".join(toks)

    @property
    def gender(self) -> str:
        for t in self.extra.split():
            if t in ARTICLES:
                return ARTICLES[t]
            if t in GENDERS:
                return t
        return ""


ARTICLES = {"der": "m", "die": "f", "das": "n", "le": "m", "la": "f", "l'": "", "les": "pl"}
GENDERS = {"m", "f", "n", "pl", "mf"}


# ---------------------------------------------------------------------------
# Directions
# ---------------------------------------------------------------------------
OTHER_LANG = "tr" if C.TARGET_LANG == "en" else "en"     # language of ``Entry.translation``
HAS_TR = C.TARGET_LANG != "en"                            # a separate Turkish field exists (DE/FR apps)
DIRECTIONS: tuple[str, ...] = C.DICT_DIRECTIONS           # ("auto", "de2en", "en2de", "de2tr", "tr2de")
DEFAULT_DIRECTION = DIRECTIONS[1]                         # what an empty/undecidable "auto" query reports
# Entry field holding each language; for the English app "tr" is the translation column itself.
_FIELD_OF_LANG: dict[str, str] = {"tr": "tr"}
_FIELD_OF_LANG[OTHER_LANG] = "translation"
_FIELD_OF_LANG[C.TARGET_LANG] = "headword"
_LANG_OF_FIELD = {field: lang for lang, field in _FIELD_OF_LANG.items()}
_SIDES = tuple(f for f in ("headword", "translation", "tr") if f in _LANG_OF_FIELD)   # tie order in auto mode
# Optional script rules for auto mode: a query matching the pattern is only ever searched on that side
# (the Russian port appends a Cyrillic pattern mapped to "headword": Cyrillic input is always ru2*).
AUTO_SIDE_RULES: list[tuple[re.Pattern, str]] = []


def split_direction(direction: str) -> tuple[str, str]:
    """``"de2tr"`` -> ``("de", "tr")``; ``"auto"`` (or an unknown code) -> the default pair."""
    if direction not in DIRECTIONS or direction == "auto":
        direction = DEFAULT_DIRECTION
    src, dst = direction.split("2", 1)
    return src, dst


def direction_code(src_lang: str, dst_lang: str) -> str:
    return f"{src_lang}2{dst_lang}"


def source_field(direction: str) -> str:
    """Entry field that is searched for a fixed direction (``en2de`` -> ``translation``)."""
    return _FIELD_OF_LANG[split_direction(direction)[0]]


def target_field(direction: str) -> str:
    """Entry field shown as the "target" column for a direction (``de2tr`` -> ``tr``, ``en2de`` -> ``headword``)."""
    return _FIELD_OF_LANG[split_direction(direction)[1]]


def direction_text(direction: str) -> str:
    """Short label such as ``DE → TR``; ``""`` for ``auto`` or an unknown code."""
    if direction == "auto" or direction not in DIRECTIONS:
        return ""
    return " → ".join(code.upper() for code in split_direction(direction))


def _auto_direction(side: str) -> str:
    """Direction reported when ``side`` scored best in auto mode."""
    if side == "headword":
        return DEFAULT_DIRECTION
    return direction_code(_LANG_OF_FIELD[side], C.TARGET_LANG)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
# Optional fields after ``headword|pos extra|translation`` in built-in lines: DE/FR ``|note|turkish``,
# the English app ``|definition`` (its translation is Turkish already). A Russian port would use ``("tr",)``.
LINE_TAIL: tuple[str, ...] = ("note", "tr") if HAS_TR else ("note",)


def parse_line(line: str, source: str = SOURCE_BUILTIN) -> Entry | None:
    """``headword|pos extra…|translation[|note[|turkish]]`` (see :data:`LINE_TAIL`); the trailing fields are optional."""
    line = (line or "").strip()
    if not line or line.startswith("#"):
        return None
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 3:
        return None
    head, tag, translation = parts[0], parts[1], parts[2]
    tail = {name: (parts[3 + i] if len(parts) > 3 + i else "") for i, name in enumerate(LINE_TAIL)}
    toks = tag.split()
    pos = toks[0] if toks else ""
    extra = " ".join(toks[1:])
    if not head or not translation:
        return None
    return Entry(head, pos, extra, translation, tail.get("note", ""), source, "", tail.get("tr", ""))


def parse_block(text: str, source: str = SOURCE_BUILTIN) -> list[Entry]:
    out = []
    for line in text.splitlines():
        e = parse_line(line, source)
        if e:
            out.append(e)
    return out


def _norm(text: str) -> str:
    return C.normalize_search(text)


_SENSE_SPLIT = re.compile(r"[;/](?![^(]*\))")      # ";" or "/" outside a parenthesis: "ona (erkek/nesne)" is one sense


def _senses(text: str) -> list[str]:
    """Split ';'/'/'-separated senses; also add each sense without its '(qualifier)'.

    A slash inside a qualifier (``ona (erkek/nesne)``) is not a separator, so the qualifier never becomes a sense of its own."""
    out: list[str] = []
    for raw in _SENSE_SPLIT.split(text or ""):
        raw = raw.strip()
        if not raw:
            continue
        out.append(_norm(raw))
        bare = re.sub(r"\s*\([^)]*\)", "", raw).strip()
        if bare and bare != raw:
            out.append(_norm(bare))
    return [s for s in out if s]


def _score(q: str, field: str, senses: list[str]) -> int:
    if not field:
        return 0
    if q == field or q in senses:
        return 100
    for s in senses:
        if re.sub(r"^(to|the|a|an|sich|se|s') ", "", s) == q:
            return 95
    if field.startswith(q) or any(s.startswith(q) for s in senses):
        return 60
    if re.search(r"(^|[\s\-(])" + re.escape(q), field):
        return 30
    if len(q) >= 3 and q in field:
        return 10
    return 0


# ---------------------------------------------------------------------------
# Dictionary
# ---------------------------------------------------------------------------
class Dictionary:
    """In-memory three-sided dictionary with de-duplication by (headword, pos, translation).

    A duplicate only ever contributes its Turkish gloss to the stored entry, which keeps its own source (see
    :meth:`merge_tr`): a cached AI row adds Turkish senses to a built-in entry across restarts, a user row replaces them."""

    def __init__(self, entries: Iterable[Entry] = ()):
        self._entries: list[Entry] = []
        self._index: dict[tuple[str, str, str], int] = {}
        self.extend(entries)

    @staticmethod
    def _key(e: Entry) -> tuple[str, str, str]:
        return (_norm(e.headword), e.pos, _norm(e.translation))

    @staticmethod
    def merge_tr(stored: Entry, incoming: Entry) -> str:
        """Turkish gloss ``stored`` carries once ``incoming`` (same key) is merged into it.

        A *user* entry's gloss replaces the stored one - the user curates the Turkish side, also of built-in entries -
        while any other source (AI, built-in) only appends the senses the stored gloss lacks, so an extra Turkish
        synonym from the AI is kept without ever overwriting what is there. An entry without a gloss changes nothing."""
        if not incoming.tr:
            return stored.tr
        if incoming.source == SOURCE_USER:
            return incoming.tr
        return _dedupe_senses(f"{stored.tr}; {incoming.tr}")

    def extend(self, entries: Iterable[Entry]) -> int:
        added = 0
        for e in entries:
            key = self._key(e)
            at = self._index.get(key)
            if at is not None:
                tr = self.merge_tr(self._entries[at], e)
                if tr != self._entries[at].tr:
                    self._entries[at] = replace(self._entries[at], tr=tr)
                continue
            self._index[key] = len(self._entries)
            self._entries.append(e)
            added += 1
        return added

    def twin(self, entry: Entry) -> Entry | None:
        """The stored entry with the same (headword, pos, translation) key, any source; None when unknown."""
        at = self._index.get(self._key(entry))
        return None if at is None else self._entries[at]

    def would_change(self, entry: Entry) -> bool:
        """True when storing ``entry`` changes the dictionary: unknown key, or a known twin whose Turkish gloss would
        change (an AI entry carrying senses the twin lacks, a user entry with a different gloss)."""
        twin = self.twin(entry)
        return twin is None or self.merge_tr(twin, entry) != twin.tr

    def set_tr(self, entry: Entry, tr: str) -> Entry | None:
        """Give the stored twin of ``entry`` the Turkish gloss ``tr``; returns the updated entry (None when unknown)."""
        at = self._index.get(self._key(entry))
        if at is None:
            return None
        self._entries[at] = replace(self._entries[at], tr=tr.strip())
        return self._entries[at]

    def find(self, headword: str, pos: str | None = None) -> list[Entry]:
        """Every stored entry with this headword (and part of speech, when given), any source."""
        key = _norm(headword)
        return [e for e in self._entries if _norm(e.headword) == key and (pos is None or e.pos == pos)]

    def contains(self, entry: Entry) -> bool:
        return self._key(entry) in self._index

    def has_headword(self, headword: str, pos: str | None = None) -> bool:
        """True when an entry of any source already carries this headword (and part of speech, when given)."""
        return bool(self.find(headword, pos))

    def remove_source(self, source: str) -> None:
        keep = [e for e in self._entries if e.source != source]
        self._entries, self._index = [], {}
        self.extend(keep)

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def entries(self) -> Sequence[Entry]:
        return self._entries

    def count_by_source(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for e in self._entries:
            out[e.source] = out.get(e.source, 0) + 1
        return out

    def lookup(self, query: str, direction: str = "auto", limit: int = 200) -> tuple[str, list[Entry]]:
        """Return ``(direction, entries)``.

        ``direction`` is a code from :data:`DIRECTIONS`. A fixed code searches only its source side (headword for
        ``de2*``, English senses for ``en2*``, Turkish senses for ``tr2*``) and is returned unchanged. ``auto``
        searches every side and returns the code of the best-scoring side (ties: headword > English > Turkish),
        so a Turkish query comes back as ``tr2de`` and an English one as ``en2de``."""
        if isinstance(direction, int):                       # pre-direction callers: lookup(query, limit)
            direction, limit = "auto", direction
        if direction not in DIRECTIONS:
            direction = "auto"
        q = _norm(query)
        if not q:
            return (DEFAULT_DIRECTION if direction == "auto" else direction), []
        q = re.sub(r"^(l|d|j|s|qu|n|m|t|c)' ?", "", q) or q      # l'école -> école
        if direction == "auto":
            forced = next((side for pattern, side in AUTO_SIDE_RULES if pattern.search(query or "")), None)
            sides = (forced,) if forced else _SIDES
        else:
            sides = (source_field(direction),)
        scored: list[tuple[int, int, int, Entry]] = []
        best = {side: 0 for side in _SIDES}
        for e in self._entries:
            scores: dict[str, int] = {}
            if "headword" in sides:
                head = _norm(e.headword)
                forms = [head] + [_norm(t) for t in e.headword.split(",") if t.strip()]
                if e.plural:
                    forms.append(_norm(e.plural))
                scores["headword"] = _score(q, head, forms)
            if "translation" in sides:
                s = _score(q, _norm(e.translation), _senses(e.translation))
                if not s and not scores.get("headword") and e.note and len(q) >= 3:
                    s = 8 if _score(q, _norm(e.note), []) >= 30 else 0      # definition / usage note as a last resort
                scores["translation"] = s
            if "tr" in sides and e.tr:
                scores["tr"] = _score(q, _norm(e.tr), _senses(e.tr))
            top = max(scores.values(), default=0)
            if not top:
                continue
            side = next(f for f in _SIDES if scores.get(f) == top)
            best[side] = max(best[side], top)
            scored.append((top, _SIDES.index(side), len(e.headword), e))
        if direction == "auto":
            winner = max(_SIDES, key=lambda f: (best[f], -_SIDES.index(f)))
            direction = _auto_direction(winner)
        scored.sort(key=lambda t: (-t[0], t[1], t[2], t[3].headword.lower()))
        return direction, [e for _s, _side, _l, e in scored[:limit]]

    def random_entry(self, rng: random.Random | None = None) -> Entry | None:
        pool = [e for e in self._entries if e.source == SOURCE_BUILTIN] or self._entries
        return (rng or random).choice(pool) if pool else None


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------
# CSV layout. The Turkish column comes last so that files written before it existed (and header-less files in
# the old layout) still read positionally; a header row may also put the columns in any order.
CSV_COLUMNS: tuple[str, ...] = ("headword", "translation", "pos", "extra", "note", "source", "example") + (("tr",) if HAS_TR else ())
_HEADER_ALIASES: dict[str, str] = {
    "headword": "headword", "word": "headword", "target": "headword", C.TARGET_LANG: "headword", C.TARGET_LANG_NAME.lower(): "headword",
    "translation": "translation", "meaning": "translation", OTHER_LANG: "translation",
    {"en": "english", "tr": "turkish"}[OTHER_LANG]: "translation",
    "pos": "pos", "extra": "extra", "note": "note", "definition": "note", "source": "source", "example": "example",
}
if HAS_TR:
    _HEADER_ALIASES.update({"tr": "tr", "turkish": "tr", "türkçe": "tr", "turkce": "tr"})
else:
    _HEADER_ALIASES.update({"türkçe": "translation", "turkce": "translation"})


def _header_columns(row: list[str]) -> dict[str, int] | None:
    """Column index per field when ``row`` is a header row (headword + translation recognised), else None."""
    columns: dict[str, int] = {}
    for i, cell in enumerate(row):
        field = _HEADER_ALIASES.get(cell.strip().lower())
        if field and field not in columns:
            columns[field] = i
    return columns if {"headword", "translation"} <= set(columns) else None


def read_table(path: Path) -> list[Entry]:
    """CSV/TSV import. With a header row the columns may come in any order (``headword, translation, tr, pos, …``);
    without one the layout is :data:`CSV_COLUMNS` (``headword, translation[, pos[, extra[, note[, source[, example[, tr]]]]]]``)."""
    path = Path(path)
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    delim = "\t" if path.suffix.lower() in (".tsv", ".txt") or raw.count("\t") > raw.count(",") else ","
    columns = {name: i for i, name in enumerate(CSV_COLUMNS)}
    out: list[Entry] = []
    for i, row in enumerate(csv.reader(raw.splitlines(), delimiter=delim)):
        if i == 0:
            header = _header_columns(row)
            if header:
                columns = header
                continue
        def cell(name: str) -> str:
            at = columns.get(name)
            return row[at].strip() if at is not None and len(row) > at else ""
        head, translation = cell("headword"), cell("translation")
        if not head or not translation:
            continue
        out.append(Entry(head, cell("pos"), cell("extra"), translation, cell("note"), SOURCE_USER, cell("example"), cell("tr")))
    return out


def write_table(path: Path, entries: Iterable[Entry]) -> int:
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLUMNS)
        for e in entries:
            w.writerow([getattr(e, name) for name in CSV_COLUMNS])
            n += 1
    return n


def builtin_entries() -> list[Entry]:
    from .dict_data import DATA
    return parse_block(DATA, SOURCE_BUILTIN)


def build_dictionary(user_rows: Iterable[Sequence[Any]] = ()) -> Dictionary:
    """``user_rows``: ``(headword, translation[, pos[, extra[, note[, source[, example[, tr]]]]]])`` as stored in SQLite."""
    d = Dictionary(builtin_entries())
    def cell(r, i): return str((r[i] if len(r) > i else "") or "")
    d.extend(Entry(str(r[0]), cell(r, 2), cell(r, 3), str(r[1]), cell(r, 4),
                   cell(r, 5) if cell(r, 5) in (SOURCE_USER, SOURCE_AI) else SOURCE_USER, cell(r, 6), cell(r, 7)) for r in user_rows)
    return d


# ---------------------------------------------------------------------------
# AI lookup (structured)
# ---------------------------------------------------------------------------
AI_MAX_ENTRIES = 5
AI_MAX_TOKENS = 1200
_AI_LIMITS = {"headword": 80, "pos": 12, "extra": 80, "translation": 200, "tr": 200, "example": 240, "note": 240}
_OTHER_LANG_NAME = {"de": "English", "fr": "English", "en": "Turkish", "ru": "English"}

_CONVENTIONS = {
    "de": ('"extra": for nouns the singular definite article followed by the plural form, exactly like '
           '"der Tische" for Tisch, "das Häuser" for Haus, "die Katzen" for Katze (use "die -" when there is no plural); '
           'for all other parts of speech "extra" is "". Give the headword without article, with correct capitalization and umlauts/ß. '
           'Irregular verb forms go into "note" like "ging, ist gegangen".'),
    "fr": ('"extra": for nouns the gender code "m", "f", "mf" or "pl", followed by the plural only when it is irregular, e.g. '
           '"m yeux" for œil, "f" for maison; for all other parts of speech "extra" is "". '
           'Give the headword without article, with correct accents. Irregular verb forms go into "note".'),
    "en": ('"extra": the IPA transcription in slashes like "/haʊs/" or "". The translation must be Turkish. '
           '"note" must be a short plain-English definition.'),
    "ru": ('Mark the stress in the headword with an apostrophe right after the stressed vowel, like "приве\'т". '
           '"extra": for nouns the gender "m", "f", "n" or "pl"; for verbs the aspect "ipf" or "pf"; otherwise "".'),
}

_POS_ALIASES = {
    "noun": "n", "substantive": "n", "nomen": "n", "verb": "v", "adjective": "adj", "adverb": "adv",
    "pronoun": "pron", "preposition": "prep", "conjunction": "conj", "numeral": "num", "number": "num",
    "article": "art", "determiner": "art", "particle": "part", "interjection": "int", "phrase": "phr",
    "expression": "phr", "idiom": "phr", "collocation": "phr", "abbreviation": "phr", "prefix": "part",
}
for _code, _names in POS_LABELS.items():
    for _name in _names.values():
        _POS_ALIASES.setdefault(_name.lower(), _code)
_FENCE = re.compile(r"^\s*```[\w-]*\s*|\s*```\s*$", re.MULTILINE)


def ai_prompt(query: str, ui_lang: str = "en") -> str:
    """Strict instruction: answer ONLY with a JSON array of dictionary entries.

    DE/FR apps ask for both ``translation_en`` and ``translation_tr``; the English app keeps the single
    ``translation`` key (Turkish). :func:`parse_ai_entries` accepts every variant."""
    target, other = C.TARGET_LANG_NAME, _OTHER_LANG_NAME.get(C.TARGET_LANG, "English")
    codes = " ".join(POS_LABELS)
    if HAS_TR:
        languages = f"{target}, {other} or Turkish"
        engine = f"trilingual {target} <-> {other} <-> Turkish"
        translation_keys = (f'  "translation_en": the English side; several senses separated by "; ",\n'
                            f'  "translation_tr": the Turkish side (Türkçe); several senses separated by "; ",\n')
        shape = '"translation_en": "...", "translation_tr": "..."'
    else:
        languages = f"{target} or {other}"
        engine = f"bilingual {target} <-> {other}"
        translation_keys = f'  "translation": the {other} side; several senses separated by "; ",\n'
        shape = '"translation": "..."'
    return (
        f"You are a {engine} dictionary engine.\n"
        f'Look up: "{query}"\n'
        f"The query may be in {languages}. Detect the direction yourself. "
        f"Every returned entry must have its headword in {target}; if the query is not in {target}, return the best {target} "
        f"equivalents. If the query is misspelled, return the most likely intended {target} word.\n"
        f"Answer ONLY with a JSON array of 1 to {AI_MAX_ENTRIES} objects and nothing else - no prose, no markdown, no code fence.\n"
        "Each object has exactly these keys:\n"
        f'  "headword": the {target} word or phrase (lemma / dictionary form),\n'
        f'  "pos": one of: {codes},\n'
        '  "extra": see the convention below,\n'
        f"{translation_keys}"
        f'  "example": one short natural example sentence in {target} using the headword,\n'
        f'  "note": a short usage note ({other}), or "".\n'
        f"Convention: {_CONVENTIONS.get(C.TARGET_LANG, '')}\n"
        f'Example of the required shape: [{{"headword": "...", "pos": "n", "extra": "...", {shape}, "example": "...", "note": "..."}}]\n'
        f"Return [] only if the query is not a real word or phrase in any of these languages."
    )


def _clean(value: Any, limit: int) -> str:
    if value is None or isinstance(value, bool):
        return ""
    if isinstance(value, (list, tuple)):
        value = "; ".join(str(v) for v in value if v is not None and not isinstance(v, (dict, list, tuple)))
    elif isinstance(value, dict):
        return ""
    text = re.sub(r"\s+", " ", str(value)).strip()
    return text[:limit].strip()


def normalize_pos(value: Any) -> str:
    """Map anything the model says to one of the POS codes used by this dictionary (unknown -> ``phr``)."""
    text = _clean(value, 40).lower().strip(" .:;,")
    if not text:
        return "phr"
    if text in POS_LABELS:
        return text
    token = re.split(r"[\s/(,]", text)[0]
    if token in POS_LABELS:
        return token
    return _POS_ALIASES.get(text, _POS_ALIASES.get(token, "phr"))


_ARTICLE_SETS = {"de": ("der", "die", "das"), "fr": ("le", "la", "les", "un", "une")}


def _fix_article(head: str, extra: str) -> tuple[str, str]:
    """Normalise noun headwords the model wrote with an article (``der Tisch`` -> ``Tisch`` / ``der Tische``)."""
    arts = _ARTICLE_SETS.get(C.TARGET_LANG, ())
    toks = head.split()
    article = toks[0].lower() if len(toks) > 1 and toks[0].lower() in arts else ""
    if article:
        head = " ".join(toks[1:])
    elif C.TARGET_LANG == "fr" and re.match(r"^l['’]\s*\S", head, re.IGNORECASE):
        head = re.sub(r"^l['’]\s*", "", head, flags=re.IGNORECASE)
    etoks = extra.split()
    if C.TARGET_LANG == "de":
        if etoks and etoks[0].lower() in arts:
            etoks[0] = article or etoks[0].lower()
        elif article:
            etoks.insert(0, article)
    elif C.TARGET_LANG == "fr":
        gender = {"le": "m", "un": "m", "la": "f", "une": "f", "les": "pl"}.get(article, "")
        etoks = [t for t in etoks if t.lower() not in arts]
        if etoks and etoks[0].lower() in GENDERS:
            etoks[0] = etoks[0].lower()
        elif gender:
            etoks.insert(0, gender)
    # The model sometimes repeats the headword in ``extra`` ("das Fernweh") or writes a dash for
    # "no plural" ("die -"); neither is a plural form.
    head_norm = C.normalize_search(head)
    etoks = [t for t in etoks
             if C.normalize_search(t) != head_norm and t.strip("-–—()") != ""]
    if C.TARGET_LANG == "de" and etoks:
        etoks = etoks[:1] + [t for t in etoks[1:] if t.lower() not in arts]   # "der die Ohrwürmer" -> "der Ohrwürmer"
    return head, " ".join(etoks)


def _dedupe_senses(text: str) -> str:
    """"craze; fad; craze" -> "craze; fad": models sometimes repeat a sense."""
    seen: set[str] = set(); out: list[str] = []
    for sense in (s.strip() for s in (text or "").split(";")):
        key = C.normalize_search(sense)
        if sense and key not in seen:
            seen.add(key); out.append(sense)
    return "; ".join(out)


def parse_ai_entries(text: str) -> list[Entry]:
    """Tolerant parser for the model output; never raises, returns ``[]`` on garbage."""
    raw = _FENCE.sub("", text or "")
    start, end = raw.find("["), raw.rfind("]")
    if start < 0 or end <= start:
        return []
    try:
        data = json.loads(raw[start:end + 1])
    except (ValueError, TypeError, RecursionError):
        return []
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []
    out: list[Entry] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        head = _clean(item.get("headword"), _AI_LIMITS["headword"])
        # "translation_en" is the current key; "translation" the legacy one (English for DE/FR, Turkish for the English app).
        translation = _dedupe_senses(_clean(item.get("translation_en") or item.get("translation"), _AI_LIMITS["translation"]))
        if not HAS_TR and not translation:
            translation = _dedupe_senses(_clean(item.get("translation_tr"), _AI_LIMITS["translation"]))
        tr = _dedupe_senses(_clean(item.get("translation_tr"), _AI_LIMITS["tr"])) if HAS_TR else ""
        if not head or not translation:
            continue
        pos = normalize_pos(item.get("pos"))
        extra = re.sub(r"[,;]", " ", _clean(item.get("extra"), _AI_LIMITS["extra"]))
        extra = re.sub(r"\s+", " ", extra).strip()
        if pos == "n" and C.TARGET_LANG in ("de", "fr"):
            head, extra = _fix_article(head, extra)
        example = _clean(item.get("example"), _AI_LIMITS["example"])
        note = _clean(item.get("note"), _AI_LIMITS["note"])
        if head:
            out.append(Entry(head, pos, extra, translation, note, SOURCE_AI, example, tr))
        if len(out) >= AI_MAX_ENTRIES:
            break
    return out


def ai_lookup(client, query: str, ui_lang: str = "en", model: str = "") -> list[Entry]:
    """Ask an OpenAI-compatible client for structured entries. Network errors (``AIError``) propagate."""
    query = C.normalize_exact(query)
    if not query:
        return []
    system = (f"You are a precise bilingual {C.TARGET_LANG_NAME} dictionary. "
              "You output strictly valid JSON and nothing else.")
    # Thinking models (gemma-4, qwen3...) can spend the whole budget on reasoning and return an
    # empty content; local servers get reasoning_effort=none (a server that rejects the field
    # with 400 is retried without it). An empty, truncated answer is retried once with 3x budget.
    extra = {"reasoning_effort": "none"} if getattr(client, "is_local", False) else None
    text = client.chat(ai_prompt(query, ui_lang), "dictionary", ui_lang, model, timeout=90.0,
                       system=system, temperature=0.1, max_tokens=AI_MAX_TOKENS, extra=extra)
    entries = parse_ai_entries(text)
    if not entries and getattr(client, "last_finish_reason", "") == "length":
        text = client.chat(ai_prompt(query, ui_lang), "dictionary", ui_lang, model, timeout=180.0,
                           system=system, temperature=0.1, max_tokens=AI_MAX_TOKENS * 3, extra=extra)
        entries = parse_ai_entries(text)
    return entries
