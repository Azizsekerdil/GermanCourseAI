"""Bidirectional target-language <-> English dictionary engine.

Layers that are merged at runtime:
1. Built-in core dictionary (``dict_data.py``; ~900 A1-B1 entries).
2. User entries imported from CSV/TSV or added by hand (SQLite ``dict_entries``).
3. AI entries produced by :func:`ai_lookup` and cached into the same table.

Search runs on both sides at once. The best-scoring side decides the direction
shown to the user; ranking is exact > prefix > word-start > substring.
"""
from __future__ import annotations

import csv
import json
import random
import re
from dataclasses import dataclass
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
# Parsing
# ---------------------------------------------------------------------------
def parse_line(line: str, source: str = SOURCE_BUILTIN) -> Entry | None:
    """``headword|pos extra…|translation[|note]``."""
    line = (line or "").strip()
    if not line or line.startswith("#"):
        return None
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 3:
        return None
    head, tag, tr = parts[0], parts[1], parts[2]
    note = parts[3] if len(parts) > 3 else ""
    toks = tag.split()
    pos = toks[0] if toks else ""
    extra = " ".join(toks[1:])
    if not head or not tr:
        return None
    return Entry(head, pos, extra, tr, note, source)


def parse_block(text: str, source: str = SOURCE_BUILTIN) -> list[Entry]:
    out = []
    for line in text.splitlines():
        e = parse_line(line, source)
        if e:
            out.append(e)
    return out


def _norm(text: str) -> str:
    return C.normalize_search(text)


def _senses(text: str) -> list[str]:
    """Split ';'-separated senses; also add each sense without its '(qualifier)'."""
    out: list[str] = []
    for raw in re.split(r"[;/]", text or ""):
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
    """In-memory two-sided dictionary with de-duplication by (headword, pos, translation)."""

    def __init__(self, entries: Iterable[Entry] = ()):
        self._entries: list[Entry] = []
        self._seen: set[tuple[str, str, str]] = set()
        self.extend(entries)

    def extend(self, entries: Iterable[Entry]) -> int:
        added = 0
        for e in entries:
            key = (_norm(e.headword), e.pos, _norm(e.translation))
            if key in self._seen:
                continue
            self._seen.add(key)
            self._entries.append(e)
            added += 1
        return added

    def contains(self, entry: Entry) -> bool:
        return (_norm(entry.headword), entry.pos, _norm(entry.translation)) in self._seen

    def has_headword(self, headword: str, pos: str | None = None) -> bool:
        """True when an entry of any source already carries this headword (and part of speech, when given)."""
        key = _norm(headword)
        return any(_norm(e.headword) == key and (pos is None or e.pos == pos) for e in self._entries)

    def remove_source(self, source: str) -> None:
        keep = [e for e in self._entries if e.source != source]
        self._entries, self._seen = [], set()
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

    def lookup(self, query: str, limit: int = 200) -> tuple[str, list[Entry]]:
        """Return (direction, entries). direction is 'target' or 'translation'."""
        q = _norm(query)
        if not q:
            return "target", []
        q = re.sub(r"^(l|d|j|s|qu|n|m|t|c)' ?", "", q) or q      # l'école -> école
        scored: list[tuple[int, int, int, Entry]] = []
        best_side = {"target": 0, "translation": 0}
        for e in self._entries:
            head = _norm(e.headword)
            target_forms = [head] + [_norm(t) for t in e.headword.split(",") if t.strip()]
            if e.plural:
                target_forms.append(_norm(e.plural))
            s_t = _score(q, head, target_forms)
            s_x = _score(q, _norm(e.translation), _senses(e.translation))
            if not s_t and not s_x and e.note and len(q) >= 3:
                s_x = 8 if _score(q, _norm(e.note), []) >= 30 else 0
            if s_t or s_x:
                side = 0 if s_t >= s_x else 1
                best_side["target" if side == 0 else "translation"] = max(
                    best_side["target" if side == 0 else "translation"], max(s_t, s_x))
                scored.append((max(s_t, s_x), side, len(e.headword), e))
        direction = "target" if best_side["target"] >= best_side["translation"] else "translation"
        scored.sort(key=lambda t: (-t[0], t[1], t[2], t[3].headword.lower()))
        return direction, [e for _s, _side, _l, e in scored[:limit]]

    def random_entry(self, rng: random.Random | None = None) -> Entry | None:
        pool = [e for e in self._entries if e.source == SOURCE_BUILTIN] or self._entries
        return (rng or random).choice(pool) if pool else None


# ---------------------------------------------------------------------------
# Files
# ---------------------------------------------------------------------------
def read_table(path: Path) -> list[Entry]:
    """CSV/TSV with columns ``headword, translation[, pos[, extra[, note]]]``; header optional."""
    path = Path(path)
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    delim = "\t" if path.suffix.lower() in (".tsv", ".txt") or raw.count("\t") > raw.count(",") else ","
    out: list[Entry] = []
    for i, row in enumerate(csv.reader(raw.splitlines(), delimiter=delim)):
        if len(row) < 2:
            continue
        head, tr = row[0].strip(), row[1].strip()
        if not head or not tr:
            continue
        if i == 0 and head.lower() in ("headword", "word", C.TARGET_LANG, "target") and tr.lower() in ("translation", "en", "tr", "meaning", "english", "turkish"):
            continue
        pos = row[2].strip() if len(row) > 2 else ""
        extra = row[3].strip() if len(row) > 3 else ""
        note = row[4].strip() if len(row) > 4 else ""
        example = row[6].strip() if len(row) > 6 else ""
        out.append(Entry(head, pos, extra, tr, note, SOURCE_USER, example))
    return out


def write_table(path: Path, entries: Iterable[Entry]) -> int:
    n = 0
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["headword", "translation", "pos", "extra", "note", "source", "example"])
        for e in entries:
            w.writerow([e.headword, e.translation, e.pos, e.extra, e.note, e.source, e.example])
            n += 1
    return n


def builtin_entries() -> list[Entry]:
    from .dict_data import DATA
    return parse_block(DATA, SOURCE_BUILTIN)


def build_dictionary(user_rows: Iterable[Sequence[Any]] = ()) -> Dictionary:
    """``user_rows``: ``(headword, translation[, pos[, extra[, note[, source[, example]]]]])`` as stored in SQLite."""
    d = Dictionary(builtin_entries())
    def cell(r, i): return str((r[i] if len(r) > i else "") or "")
    d.extend(Entry(str(r[0]), cell(r, 2), cell(r, 3), str(r[1]), cell(r, 4),
                   cell(r, 5) if cell(r, 5) in (SOURCE_USER, SOURCE_AI) else SOURCE_USER, cell(r, 6)) for r in user_rows)
    return d


# ---------------------------------------------------------------------------
# AI lookup (structured)
# ---------------------------------------------------------------------------
AI_MAX_ENTRIES = 5
AI_MAX_TOKENS = 1200
_AI_LIMITS = {"headword": 80, "pos": 12, "extra": 80, "translation": 200, "example": 240, "note": 240}
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
    """Strict instruction: answer ONLY with a JSON array of dictionary entries."""
    target, other = C.TARGET_LANG_NAME, _OTHER_LANG_NAME.get(C.TARGET_LANG, "English")
    codes = " ".join(POS_LABELS)
    return (
        f"You are a bilingual {target} <-> {other} dictionary engine.\n"
        f'Look up: "{query}"\n'
        f"The query may be in {target} or in {other}. Detect the direction yourself. "
        f"Every returned entry must have its headword in {target}; if the query is in {other}, return the best {target} "
        f"equivalents. If the query is misspelled, return the most likely intended {target} word.\n"
        f"Answer ONLY with a JSON array of 1 to {AI_MAX_ENTRIES} objects and nothing else - no prose, no markdown, no code fence.\n"
        "Each object has exactly these keys:\n"
        f'  "headword": the {target} word or phrase (lemma / dictionary form),\n'
        f'  "pos": one of: {codes},\n'
        '  "extra": see the convention below,\n'
        f'  "translation": the {other} side; several senses separated by "; ",\n'
        f'  "example": one short natural example sentence in {target} using the headword,\n'
        f'  "note": a short usage note ({other}), or "".\n'
        f"Convention: {_CONVENTIONS.get(C.TARGET_LANG, '')}\n"
        f'Example of the required shape: [{{"headword": "...", "pos": "n", "extra": "...", "translation": "...", "example": "...", "note": "..."}}]\n'
        f"Return [] only if the query is not a real word or phrase in either language."
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
        translation = _clean(item.get("translation"), _AI_LIMITS["translation"])
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
            out.append(Entry(head, pos, extra, translation, note, SOURCE_AI, example))
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
