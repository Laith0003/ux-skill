"""The page composition a landing page starts from, chosen by a score over
the axes and the brief's fields.

Five named compositions are the hooks the landing playbooks build on:
split, stacked, bento, editorial-column and full-bleed-media. Each has a
linear score over the axes plus the fields that bear on it (an older
audience favors stacked, long reading favors the editorial column,
glancing favors bento). The highest score wins, ties broken by name, and
the report says why: the winner, the runner-up and the terms that decided
it. No industry or keyword picks a composition.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Dict, List, Mapping, Tuple

from engine.foundations.audience import Audience
from engine.synthesizer.axes import AxisValues

Terms = List[Tuple[str, float]]
# What glance reading adds to bento's score, and long reading to the
# editorial column's.
GLANCE_BONUS = 0.2
LONG_READ_BONUS = 0.4

DESCRIPTIONS: Mapping[str, str] = MappingProxyType({
    "split": "the message on one side and one image or proof on the other, then alternating "
             "sections",
    "stacked": "one centered column of large, calm sections, one idea each, read top to "
               "bottom",
    "bento": "a grid of tiles of different sizes, each a feature or a number, scanned at a "
             "glance",
    "editorial-column": "a narrow reading column with a large display title, pull quotes and "
                        "images set into the text",
    "full-bleed-media": "edge-to-edge images or generated art with the headline on a scrim, "
                        "then bands of media and short copy",
})


def _terms_split(a: AxisValues, aud: Audience) -> Terms:
    return [("formality", 0.5 * a.formality),
            ("balanced contrast", 0.3 * (1 - abs(a.contrast - 0.5) * 2)),
            ("coolness", 0.2 * (1 - a.warmth))]


def _terms_stacked(a: AxisValues, aud: Audience) -> Terms:
    return [("the audience's age", 0.6 * aud.age_factor), ("airiness", 0.25 * (1 - a.density)),
            ("muted contrast", 0.15 * (1 - a.contrast))]


def _terms_bento(a: AxisValues, aud: Audience) -> Terms:
    return [("density", 0.4 * a.density), ("contrast", 0.35 * a.contrast),
            ("geometric type", 0.25 * (1 - a.type_personality)),
            ("glance reading", GLANCE_BONUS if aud.reading_context == "glance" else 0.0)]


def _terms_editorial(a: AxisValues, aud: Audience) -> Terms:
    return [("humanist type", 0.5 * a.type_personality), ("formality", 0.3 * a.formality),
            ("airiness", 0.2 * (1 - a.density)),
            ("long reading", LONG_READ_BONUS if aud.reading_context == "long-read" else 0.0)]


def _terms_media(a: AxisValues, aud: Audience) -> Terms:
    return [("warmth", 0.45 * a.warmth), ("playfulness", 0.35 * (1 - a.formality)),
            ("motion", 0.2 * a.motion)]


SCORES: Mapping[str, Callable[[AxisValues, Audience], Terms]] = MappingProxyType({
    "split": _terms_split, "stacked": _terms_stacked, "bento": _terms_bento,
    "editorial-column": _terms_editorial, "full-bleed-media": _terms_media,
})


@dataclass(frozen=True)
class Composition:
    name: str
    scores: Tuple[Tuple[str, float], ...]  # every composition, highest first
    reasons: Tuple[str, ...]               # the winner's two largest terms

    def line(self) -> str:
        (win, top), (second, next_score) = self.scores[0], self.scores[1]
        return (f"{win}: {DESCRIPTIONS[win]}. It scored {top:.2f}, ahead of {second} at "
                f"{next_score:.2f}, mostly for {' and '.join(self.reasons)}.")

    def to_dict(self) -> Dict[str, object]:
        return {"name": self.name, "scores": {k: round(v, 4) for k, v in self.scores},
                "reasons": list(self.reasons)}


def choose(axes: AxisValues, audience: Audience = Audience()) -> Composition:
    table = {name: fn(axes, audience) for name, fn in SCORES.items()}
    totals = sorted(((name, round(sum(v for _, v in terms), 6)) for name, terms in table.items()),
                    key=lambda item: (-item[1], item[0]))
    win = totals[0][0]
    top = sorted((t for t in table[win] if t[1] > 0), key=lambda t: (-t[1], t[0]))[:2]
    return Composition(win, tuple(totals), tuple(name for name, _ in top))
