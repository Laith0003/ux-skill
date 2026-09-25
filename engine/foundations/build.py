"""Build pipeline: generate every foundation, validate, gate. One error
type per stage.

build_system is the single entry point for a generated system.
Generators return tokens and notes and never gate themselves; the build
validates the merged set once (raises ValidationError carrying every
Problem), gates it once through gate_foundations with every foundation's
pairings and checks plus one role-types check over every declared role (a
pairing on a mistyped role is left to that check), attaches each
foundation's hints to the findings it owns, and raises GateFailure
carrying the report. On success the report is returned with the tokens.

check_system is the entry point for a set the engine did not generate (an
edited tokens.json, an import): the same validate and the same
gate_foundations, returned together and never raised.
"""
from __future__ import annotations

import dataclasses
import math
import numbers
from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Sequence, Tuple

from engine.foundations import (
    border, color, elevation, imagery, layout, motion, radius, space, typography)
from engine.foundations.audience import Audience
from engine.foundations.color_math import hex_to_rgb
from engine.foundations.foundation import BrandInputs, Foundation, mistyped, role_types_check
from engine.foundations.gate import Check, CheckFailure, GateFailure, GateReport, gate
from engine.foundations.tokens import TokenSet
from engine.foundations.validate import Problem, validate
from engine.synthesizer.axes import AxisValues

# Build order. Each foundation task appends its FOUNDATION here.
FOUNDATIONS: Tuple[Foundation, ...] = (color.FOUNDATION, space.FOUNDATION, radius.FOUNDATION,
                                      border.FOUNDATION, elevation.FOUNDATION,
                                      motion.FOUNDATION, layout.FOUNDATION,
                                      typography.FOUNDATION, imagery.FOUNDATION)

# The color gate measures the focus ring against surfaces only. That is
# enough because the border foundation guarantees a ring offset; a build
# without border has to say so.
RING_WITHOUT_BORDER = ("color.focus.ring is checked against surfaces only and relies on "
                       "border.focus-ring.offset of at least 1px, which the border foundation "
                       "guarantees; build border too, or keep a gap between the element and "
                       "its ring")


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
    chosen = tuple(f for f in FOUNDATIONS if f.name in foundations)
    for f in chosen:
        for need in f.requires:
            if need not in foundations:
                raise ValueError(f"foundations includes {f.name!r}, which aliases {need!r} tokens; "
                                 f"add {need!r} to foundations")
    return chosen


def _attach_hints(ts: TokenSet, report: GateReport, chosen: Sequence[Foundation]) -> None:
    """Each finding gets advice from the foundation that owns its
    foreground. A hint runs under the same guard as a check: one that
    raises becomes a failure naming the hint, and the finding keeps its
    own fix."""
    hinted = []
    for finding in report.findings:
        root = finding.fg.split(".", 1)[0]
        owner = next((f for f in chosen if f.name == root and f.hint), None)
        advice = ""
        if owner:
            try:
                advice = owner.hint(ts, finding)
            except Exception as exc:  # a hint must never take the build down
                report.failures.append(CheckFailure(
                    f"{owner.name}-hint", "system", finding.mode,
                    f"the {owner.name} hint could not advise on {finding.fg} on {finding.bg} "
                    f"({finding.mode}) ({type(exc).__name__}: {exc}); that finding keeps its "
                    f"own fix, so move {finding.fg} as it says"))
        hinted.append(dataclasses.replace(finding, hint=advice) if advice else finding)
    report.findings[:] = hinted


# Check id for a pairing strict mode fails because a token is not defined.
SKIPPED_PAIRING = "skipped-pairing"


def _narrow(check: Check, ts: TokenSet) -> Check:
    """The check over the axes the set has: an imported set may lack one of
    ours, and a check reads only the contexts the set can be in."""
    axes = tuple(a for a in check.axes if a in ts.axes)
    return check if axes == check.axes else dataclasses.replace(check, axes=axes)


def gate_foundations(ts: TokenSet, chosen: Sequence[Foundation],
                     strict: bool = False) -> GateReport:
    """Gate `ts` with the chosen foundations' pairings and checks and one
    role-types check over their roles. Checks run over the axes the set
    has. With strict, each pairing that could not be checked because a
    token is not defined is a failure. Failing findings get their
    foundation's hints. Never raises for what it finds."""
    checks = ([role_types_check(chosen)] if chosen else []) \
        + [_narrow(c, ts) for f in chosen for c in f.checks]
    # A pairing on a mistyped role cannot be measured; role-types names the
    # role, so the pairing waits until it is fixed.
    skip = set(mistyped(ts, chosen))
    pairings = [p for f in chosen for p in f.pairings if p.fg not in skip and p.bg not in skip]
    report = gate(ts, pairings, checks, raise_on_fail=False)
    if strict:
        for p in report.skipped_pairings:
            missing = p.fg if not ts.has(p.fg) else p.bg
            report.failures.append(CheckFailure(
                SKIPPED_PAIRING, "system", "",
                f"{p.fg} on {p.bg} was not checked because {missing} is not defined; define "
                "it, or for an imported system map the role to one of its tokens"))
    if not report.passed:
        _attach_hints(ts, report, chosen)
    return report


@dataclass(frozen=True)
class SystemCheck:
    """What check_system found: every structural problem, the gate report
    and the foundations it checked, in build order."""
    problems: Tuple[Problem, ...]
    report: GateReport
    foundations: Tuple[str, ...]

    @property
    def passed(self) -> bool:
        return not self.problems and self.report.passed


def foundations_in(ts: TokenSet) -> Tuple[str, ...]:
    """The foundations whose root the set has, in build order."""
    roots = {t.path.split(".", 1)[0] for t in ts.tokens()}
    return tuple(f.name for f in FOUNDATIONS if f.name in roots)


def check_system(ts: TokenSet, foundations: Optional[Sequence[str]] = None, *,
                 strict: bool = False) -> SystemCheck:
    """Validate and gate a token set the engine did not generate, without
    raising for what it finds. Checks the named foundations, or every
    foundation whose root the set has. A foundation named that requires
    another is checked on its own; an alias into a foundation the set lacks
    is a validate problem."""
    if foundations is None:
        chosen = tuple(f for f in FOUNDATIONS if f.name in foundations_in(ts))
    else:
        known = [f.name for f in FOUNDATIONS]
        for name in foundations:
            if name not in known:
                raise ValueError(f"foundations names {name!r}, which is not one of {known}; "
                                 "use those names or leave foundations out to check every "
                                 "foundation the set has")
        chosen = tuple(f for f in FOUNDATIONS if f.name in foundations)
    return SystemCheck(problems=tuple(validate(ts)),
                       report=gate_foundations(ts, chosen, strict),
                       foundations=tuple(f.name for f in chosen))


def build_system(axes: AxisValues, brand_hex: str, *, arabic: bool = True,
                 foundations: Optional[Sequence[str]] = None,
                 audience: Optional[Audience] = None) -> BuildResult:
    """Generate every foundation (or the named ones, in build order),
    validate the merged set and gate it.

    Raises TypeError or ValueError for bad inputs, ValidationError when the
    set breaks a structural rule, and GateFailure when a pairing or check
    fails (a paired role that resolves to a translucent color is such a
    failure, named by token); otherwise returns the tokens, every
    generator's notes and the gate report.
    """
    _check_inputs(axes, brand_hex, arabic)
    chosen = _select(foundations)
    audience = audience or Audience()
    inputs = BrandInputs(brand_hex=brand_hex, arabic=arabic, brand_role=audience.brand_role,
                         audience=audience)
    ts = TokenSet()
    notes: List[str] = []
    for f in chosen:
        generated = f.generate(axes, inputs)
        for token in generated.tokens.tokens():
            ts.add(token)
        notes.extend(generated.notes)
    names = {f.name for f in chosen}
    if "color" in names and "border" not in names:
        notes.append(RING_WITHOUT_BORDER)
    problems = validate(ts)
    if problems:
        raise ValidationError(problems)
    report = gate_foundations(ts, chosen)
    if not report.passed:
        raise GateFailure(report)
    return BuildResult(tokens=ts, notes=tuple(notes), report=report)


def build_color(axes: AxisValues, brand_hex: str) -> BuildResult:
    """Color only: the same pipeline as build_system, one foundation. Its
    notes end with RING_WITHOUT_BORDER, since border is not built."""
    return build_system(axes, brand_hex, foundations=("color",))
