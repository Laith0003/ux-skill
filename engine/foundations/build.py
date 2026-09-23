"""Build pipeline: generate, validate, gate. One error type per stage.

generate raises ValueError (or GateFailure from the generator's own
re-check), validate raises ValidationError carrying every Problem, and the
gate raises GateFailure carrying its GateReport. On success the report is
returned with the tokens, not thrown away.
"""
from __future__ import annotations

import dataclasses
import math
import numbers
from dataclasses import dataclass
from typing import Any, Iterable, Tuple

from engine.foundations.color import PAIRINGS, generate_color
from engine.foundations.color_math import hex_to_rgb
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


def _check_inputs(axes: Any, brand_hex: Any) -> None:
    """Reject bad inputs before generating, naming the input and the fix."""
    if not isinstance(axes, AxisValues):
        raise TypeError(f"axes is {type(axes).__name__}; pass an AxisValues, "
                        "for example AxisValues(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5)")
    for f in dataclasses.fields(axes):
        v = getattr(axes, f.name)
        if isinstance(v, bool) or not isinstance(v, numbers.Real):
            raise TypeError(f"axes.{f.name} is {v!r}; set it to a number from 0 to 1")
        if not (math.isfinite(v) and 0.0 <= v <= 1.0):
            raise ValueError(f"axes.{f.name} is {v!r}; set it to a number from 0 to 1")
    if not isinstance(brand_hex, str):
        raise TypeError(f"brand_hex is {brand_hex!r}; pass the brand color as a hex string, "
                        "for example '#3366FF'")
    try:
        hex_to_rgb(brand_hex)
    except ValueError:
        raise ValueError(f"brand_hex is {brand_hex!r}, which is not a hex color; "
                         "use #RRGGBB or #RGB, for example #3366FF") from None


def build_color(axes: AxisValues, brand_hex: str) -> BuildResult:
    """Generate the color foundation, validate it and gate it.

    Raises TypeError or ValueError for bad inputs, ValidationError when the
    generated set breaks a structural rule, and GateFailure when a pairing
    fails; otherwise returns the tokens, the retune notes and the gate report.
    """
    _check_inputs(axes, brand_hex)
    result = generate_color(axes, brand_hex)
    problems = validate(result.tokens)
    if problems:
        raise ValidationError(problems)
    report = gate(result.tokens, PAIRINGS)
    return BuildResult(tokens=result.tokens, notes=tuple(result.notes), report=report)
