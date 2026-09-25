"""WCAG gate: every declared pairing, in every mode, meets its minimum or
the system is not emitted.

The gate knows no foundation. Callers pass the contrast pairings and the
other checks their foundations declare (build_system collects them from
every Foundation), so gate.py never imports a generator.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Callable, Iterable, List, Mapping, Optional, Tuple

from engine.foundations.color_math import contrast, hex_to_rgb
from engine.foundations.modes import AXES, FOUNDATION_AXES, contexts, parse
from engine.foundations.tokens import TokenSet, opaque_hex


@dataclass(frozen=True)
class Pairing:
    """A foreground role that must reach `minimum` contrast against a
    background role, per WCAG success criterion `criterion`. In a
    contrast:high context the minimum rises (see required); `high` pins a
    different high-contrast minimum for a pairing that cannot take the
    standard raise."""
    fg: str
    bg: str
    minimum: float
    criterion: str
    high: Optional[float] = None


# High-contrast minimums: text meets the enhanced 7:1 of WCAG 1.4.6.
# Non-text parts (borders, fills, focus rings) rise from 3:1 to 4.5:1;
# that floor is ours, since WCAG 1.4.11 has no enhanced level.
HIGH_TEXT = 7.0
HIGH_NON_TEXT = 4.5

# The ratio each success criterion the gate cites actually sets.
WCAG_RATIOS: Mapping[str, float] = MappingProxyType({"1.4.3": 4.5, "1.4.6": 7.0, "1.4.11": 3.0})

# Criterion prefix for a minimum WCAG does not set: our high-contrast
# floor, raised over the criterion that follows.
HIGH_FLOOR = "high-contrast floor over "


def required(p: Pairing, mode: str,
             axes: Mapping[str, Tuple[str, ...]] = AXES) -> Tuple[float, str]:
    """The minimum and criterion a pairing must meet in one context of
    `axes` (the token set's own axes when the gate calls it)."""
    if parse(mode, axes).get("contrast") != "high":
        return p.minimum, p.criterion
    if p.high is not None:
        return p.high, p.criterion
    if p.minimum >= 4.5:
        return HIGH_TEXT, "1.4.6"
    return HIGH_NON_TEXT, HIGH_FLOOR + p.criterion


def cite(minimum: float, criterion: str) -> str:
    """How a message states a minimum. WCAG is named as the source only
    when the criterion sets exactly that ratio; any other floor is stated
    as a floor, with what WCAG asks beside it. Minimums print as WCAG
    writes them ("3:1", "4.5:1", "7:1"); measured ratios are printed by
    the caller, floored to two decimals."""
    if criterion.startswith(HIGH_FLOOR):
        base = criterion[len(HIGH_FLOOR):]
        asks = (f"WCAG {base} asks {WCAG_RATIOS[base]:g}:1" if base in WCAG_RATIOS
                else f"raised over {base}")
        return f"our high-contrast floor is {minimum:g}:1 ({asks})"
    if criterion in WCAG_RATIOS:
        if WCAG_RATIOS[criterion] == minimum:
            return f"WCAG {criterion} needs {minimum:g}:1"
        return (f"the declared floor is {minimum:g}:1 "
                f"(WCAG {criterion} asks {WCAG_RATIOS[criterion]:g}:1)")
    if criterion == "system":
        return f"our floor is {minimum:g}:1"
    return f"the declared floor for {criterion} is {minimum:g}:1"


@dataclass(frozen=True)
class GateFinding:
    fg: str
    bg: str
    mode: str
    ratio: float
    minimum: float
    criterion: str
    # Extra fix advice from whoever owns the pairing (for example the color
    # generator naming the seed direction); appended to message() when set.
    hint: str = ""

    def message(self) -> str:
        # Floor, never round: a ratio just under the minimum (e.g. 4.496
        # against a 4.5 minimum) must never print as meeting it. Rounding
        # would show "4.50:1"; floor to 2 decimals shows "4.49:1".
        truncated = math.floor(self.ratio * 100) / 100
        text = (f"{self.fg} on {self.bg} ({self.mode}) is {truncated:.2f}:1; "
                f"{cite(self.minimum, self.criterion)}. Move {self.fg} to a "
                f"step with more contrast against {self.bg}.")
        return f"{text} {self.hint}" if self.hint else text


@dataclass(frozen=True)
class Check:
    """A requirement that is not a contrast pairing (a minimum size, a
    width, a duration). `run(ts, mode)` returns one message per failure in
    that context; every message names the token and the fix. The gate runs
    it in every context over `axes`. A run that raises becomes a failure of
    this check in that context, and the gate goes on.

    A check walks every axis its foundation's tokens vary on. An axis it
    deliberately leaves out goes in `exempt_axes` as (axis, reason), so the
    gap is stated where the check is declared and a test can hold it."""
    id: str
    criterion: str
    run: Callable[[TokenSet, str], List[str]]
    axes: Tuple[str, ...] = ()
    exempt_axes: Tuple[Tuple[str, str], ...] = ()


@dataclass(frozen=True)
class CheckFailure:
    check: str
    criterion: str
    mode: str
    message: str


@dataclass
class GateReport:
    findings: List[GateFinding] = field(default_factory=list)
    checked: int = 0
    failures: List[CheckFailure] = field(default_factory=list)
    rules_checked: int = 0
    # Pairings not checked because the set lacks one of their tokens. A set
    # with none of the roles would otherwise pass with checked == 0 unseen.
    skipped_pairings: List[Pairing] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.findings and not self.failures

    @property
    def skipped(self) -> int:
        return len(self.skipped_pairings)

    def skipped_message(self) -> str:
        """One line naming every skipped pairing, or "" when none were."""
        if not self.skipped_pairings:
            return ""
        n = len(self.skipped_pairings)
        names = ", ".join(f"{p.fg} on {p.bg}" for p in self.skipped_pairings)
        return (f"Skipped {n} pairing{'' if n == 1 else 's'} because a token is not "
                f"defined: {names}; define those tokens or leave those pairings out.")

    def summary(self) -> str:
        head = (f"WCAG gate {'passed' if self.passed else 'failed'}: {self.checked} checks, "
                f"{len(self.findings)} failing, {self.skipped} "
                f"pairing{'' if self.skipped == 1 else 's'} skipped; {self.rules_checked} "
                f"rule checks, {len(self.failures)} failing.")
        lines = [head] + [f.message() for f in self.findings] + [f.message for f in self.failures]
        if self.skipped_pairings:
            lines.append(self.skipped_message())
        return "\n".join(lines)


class GateFailure(Exception):
    def __init__(self, report: GateReport):
        self.report = report
        lines = [f.message() for f in report.findings] + [f.message for f in report.failures]
        if report.skipped_pairings:
            lines.append(report.skipped_message())
        super().__init__("\n".join(lines))


class _Translucent(ValueError):
    """A paired role resolves to a translucent color: the gate reports it
    as a failure instead of measuring it."""

    def __init__(self, path: str, mode: str, value: str):
        self.path, self.mode, self.value = path, mode, value
        super().__init__(f"{path} ({mode}) resolves to the translucent {value}")


def _hex(ts: TokenSet, path: str, mode: str) -> str:
    value = opaque_hex(ts.resolve(path, mode))
    if isinstance(value, str) and len(value) == 9 and value.startswith("#"):
        raise _Translucent(path, mode, value)
    try:
        hex_to_rgb(value)
    except ValueError:
        raise ValueError(
            f"{path} ({mode}) resolves to {value!r}, which is not a hex color; "
            "use #RRGGBB or #RGB, and run validate() first to see every such problem"
        ) from None
    return value


# Check id for a pairing the gate cannot measure because a side is translucent.
OPAQUE_PAIRING = "opaque-pairing"


def _pairing_contexts(ts: TokenSet, p: Pairing) -> List[str]:
    """Every context over the axes the pairing's foundation varies on."""
    names = FOUNDATION_AXES.get(p.fg.split(".", 1)[0], tuple(ts.axes))
    return contexts([a for a in names if a in ts.axes], ts.axes)


def gate(ts: TokenSet, pairings: Iterable[Pairing], checks: Iterable[Check] = (),
         raise_on_fail: bool = True) -> GateReport:
    report = GateReport()
    for p in pairings:
        if not (ts.has(p.fg) and ts.has(p.bg)):
            report.skipped_pairings.append(p)
            continue
        for mode in _pairing_contexts(ts, p):
            report.checked += 1
            try:
                ratio = contrast(_hex(ts, p.fg, mode), _hex(ts, p.bg, mode))
            except _Translucent as t:
                # Contrast is defined for opaque colors only; compositing
                # over the surface beneath is the caller's step.
                report.failures.append(CheckFailure(
                    OPAQUE_PAIRING, "system", mode,
                    f"{t}, so {p.fg} on {p.bg} cannot be measured; contrast needs opaque "
                    f"colors, so point {t.path} at an opaque color, or composite it over the "
                    "surface beneath it first and pair the result"))
                continue
            minimum, criterion = required(p, mode, ts.axes)
            if ratio < minimum:
                report.findings.append(
                    GateFinding(p.fg, p.bg, mode, ratio, minimum, criterion))
    for c in checks:
        unknown = [a for a in c.axes if a not in ts.axes]
        if unknown:
            raise ValueError(
                f"check {c.id} names the axes {unknown}, which this token set does not "
                f"have; use one of {list(ts.axes)}")
        for mode in contexts(list(c.axes), ts.axes):
            report.rules_checked += 1
            try:
                messages = c.run(ts, mode)
            except Exception as exc:  # a check must never take the gate down
                messages = [f"check {c.id} could not read the token set "
                            f"({type(exc).__name__}: {exc}); a token it reads has an "
                            "unexpected shape; run validate and fix the named token"]
            for message in messages:
                report.failures.append(CheckFailure(c.id, c.criterion, mode, message))
    if raise_on_fail and not report.passed:
        raise GateFailure(report)
    return report
