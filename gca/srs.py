from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, timedelta


@dataclass(frozen=True)
class SRSState:
    repetitions: int = 0
    interval: int = 0
    ease: float = 2.5
    due: date = date.today()
    box: int = 1


def review(state: SRSState, quality: int, today: date | None = None) -> SRSState:
    """SM-2 scheduling with a Leitner box used for the dashboard."""
    today = today or date.today()
    q = max(0, min(5, int(quality)))
    ease = max(1.3, state.ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)))
    if q < 3:
        return replace(state, repetitions=0, interval=1, ease=ease,
                       due=today + timedelta(days=1), box=max(1, state.box - 1))
    reps = state.repetitions + 1
    interval = 1 if reps == 1 else 6 if reps == 2 else max(1, round(state.interval * ease))
    return SRSState(reps, interval, ease, today + timedelta(days=interval), min(5, state.box + 1))


def is_due(state: SRSState, today: date | None = None) -> bool:
    return state.due <= (today or date.today())


def mastery(correct: int, wrong: int, box: int) -> float:
    attempts = correct + wrong
    accuracy = correct / attempts if attempts else 0.0
    return round(min(100.0, accuracy * 65.0 + max(0, min(5, box)) * 7.0), 1)


def leitner_due(box: int, last_seen: date, today: date | None = None) -> bool:
    gaps = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
    return (today or date.today()) >= last_seen + timedelta(days=gaps.get(box, 1))
