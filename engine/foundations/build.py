"""Build pipeline: generate, validate, gate. One error type per stage.

generate raises ValueError (or GateFailure from the generator's own
re-check), validate raises ValidationError carrying every Problem, and the
gate raises GateFailure carrying its GateReport. On success the report is
returned with the tokens, not thrown away.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Tuple

from engine.foundations.color import PAIRINGS, generate_color
from engine.foundations.gate import GateReport, gate
from engine.foundations.tokens import TokenSet
from engine.foundations.validate import Problem, validate
from engine.synthesizer.axes import AxisValues


@dataclass(frozen=True)
class BuildResult:
    tokens: TokenSet
    notes: Tuple[str, ...]
    report: GateReport


class ValidationError(ValueError):
    """validate found problems; `problems` holds every one of them."""

    def __init__(self, problems: Iterable[Problem]):
        self.problems: Tuple[Problem, ...] = tuple(problems)
        super().__init__("\n".join(p.message for p in self.problems))


def build_color(axes: AxisValues, brand_hex: str) -> BuildResult:
    result = generate_color(axes, brand_hex)
    problems = validate(result.tokens)
    if problems:
        raise ValidationError(problems)
    report = gate(result.tokens, PAIRINGS)
    return BuildResult(tokens=result.tokens, notes=tuple(result.notes), report=report)
