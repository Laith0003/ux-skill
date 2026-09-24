"""Build pipeline: generate every foundation, validate, gate. One error
type per stage.

build_system is the single entry point. Generators return tokens and notes
and never gate themselves; the build validates the merged set once (raises
ValidationError carrying every Problem), gates it once with every
foundation's pairings and checks, attaches each foundation's hints to the
findings it owns, and raises GateFailure carrying the report. On success
the report is returned with the tokens.
"""
from __future__ import annotations

import dataclasses
import math
import numbers
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Sequence, Tuple

from engine.foundations import color, space
from engine.foundations.color_math import hex_to_rgb
from engine.foundations.foundation import BrandInputs, Foundation
from engine.foundations.gate import GateFailure, GateReport, gate
from engine.foundations.tokens import TokenSet
from engine.foundations.validate import Problem, validate
from engine.synthesizer.axes import AxisValues

# Build order. Each foundation task appends its FOUNDATION here.
FOUNDATIONS: Tuple[Foundation, ...] = (color.FOUNDATION, space.FOUNDATION)


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


def _check_inputs(axes: Any, brand_hex: Any, arabic: Any) -> None:
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
    if not isinstance(arabic, bool):
        raise TypeError(f"arabic is {arabic!r}; pass True or False")


def _select(foundations: Optional[Sequence[str]]) -> Tuple[Foundation, ...]:
    if foundations is None:
        return FOUNDATIONS
    known = [f.name for f in FOUNDATIONS]
    if isinstance(foundations, str):
        raise TypeError(f"foundations is the string {foundations!r}; pass a tuple of names, "
                        f"for example ({foundations!r},)")
    for name in foundations:
        if name not in known:
            raise ValueError(f"foundations names {name!r}, which is not one of {known}; "
                             "use those names or leave foundations out to build all")
    return tuple(f for f in FOUNDATIONS if f.name in foundations)


def _attach_hints(ts: TokenSet, report: GateReport, chosen: Sequence[Foundation]) -> None:
    hinted = []
    for finding in report.findings:
        root = finding.fg.split(".", 1)[0]
        owner = next((f for f in chosen if f.name == root and f.hint), None)
        advice = owner.hint(ts, finding) if owner else ""
        hinted.append(dataclasses.replace(finding, hint=advice) if advice else finding)
    report.findings[:] = hinted


def build_system(axes: AxisValues, brand_hex: str, *, arabic: bool = True,
                 foundations: Optional[Sequence[str]] = None) -> BuildResult:
    """Generate every foundation (or the named ones, in build order),
    validate the merged set and gate it.

    Raises TypeError or ValueError for bad inputs, ValidationError when the
    set breaks a structural rule, and GateFailure when a pairing or check
    fails; otherwise returns the tokens, every generator's notes and the
    gate report.
    """
    _check_inputs(axes, brand_hex, arabic)
    chosen = _select(foundations)
    inputs = BrandInputs(brand_hex=brand_hex, arabic=arabic)
    ts = TokenSet()
    notes: List[str] = []
    for f in chosen:
        generated = f.generate(axes, inputs)
        for token in generated.tokens.tokens():
            ts.add(token)
        notes.extend(generated.notes)
    problems = validate(ts)
    if problems:
        raise ValidationError(problems)
    report = gate(ts, [p for f in chosen for p in f.pairings],
                  [c for f in chosen for c in f.checks], raise_on_fail=False)
    if not report.passed:
        _attach_hints(ts, report, chosen)
        raise GateFailure(report)
    return BuildResult(tokens=ts, notes=tuple(notes), report=report)


def build_color(axes: AxisValues, brand_hex: str) -> BuildResult:
    """Color only: the same pipeline as build_system, one foundation."""
    return build_system(axes, brand_hex, foundations=("color",))
