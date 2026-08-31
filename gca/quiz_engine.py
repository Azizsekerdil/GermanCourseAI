from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any, Sequence

from .config import answer_equal, normalize_search

MCQ = "mcq"
TYPE_IN = "type_in"
LISTEN = "listen"


@dataclass
class Question:
    kind: str
    prompt: str
    answer: str
    options: list[str]
    word_id: int | None = None
    hint: str = ""
    meta: dict[str, Any] | None = None


def distractors(correct: str, pool: Sequence[str], n: int = 3,
                rng: random.Random | None = None) -> list[str]:
    rng = rng or random.Random()
    seen = {normalize_search(correct)}
    candidates = []
    for value in pool:
        key = normalize_search(value)
        if value and key not in seen:
            seen.add(key)
            candidates.append(value)
    rng.shuffle(candidates)
    return candidates[:n]


def make_mcq(prompt: str, correct: str, pool: Sequence[str],
             rng: random.Random | None = None) -> Question:
    rng = rng or random.Random()
    options = [correct, *distractors(correct, pool, 3, rng)]
    rng.shuffle(options)
    return Question(MCQ, prompt, correct, options)


def check_answer(question: Question, given: str) -> bool:
    return answer_equal(given, question.answer)


def accuracy(results: Sequence[bool]) -> float:
    return round(100.0 * sum(bool(v) for v in results) / len(results), 1) if results else 0.0


def build_session(words: Sequence[dict[str, Any]], count: int = 10,
                  rng: random.Random | None = None) -> list[Question]:
    rng = rng or random.Random()
    selected = list(words)
    rng.shuffle(selected)
    selected = selected[:count]
    translations = [w["tr"] for w in words]
    return [make_mcq(w["target"], w["tr"], translations, rng) for w in selected]
