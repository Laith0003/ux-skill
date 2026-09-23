"""WCAG gate: every declared pairing, in every mode, meets its minimum or
the system is not emitted.

The gate knows no foundation. Each caller passes the pairings it owns
(color passes color.PAIRINGS), so gate.py never imports a generator.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Iterable, List

from engine.foundations.color_math import contrast, hex_to_rgb
from engine.foundations.tokens import TokenSet


@dataclass(frozen=True)
class Pairing:
    """A foreground role that must reach `minimum` contrast against a
    background role, per WCAG success criterion `criterion`."""
    fg: str
    bg: str
    minimum: float
    criterion: str


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
                f"WCAG {self.criterion} needs {self.minimum}:1. Move {self.fg} to a "
                f"step with more contrast against {self.bg}.")
        return f"{text} {self.hint}" if self.hint else text


@dataclass
class GateReport:
    findings: List[GateFinding] = field(default_factory=list)
    checked: int = 0
    # Pairings not checked because the set lacks one of their tokens. A set
    # with none of the roles would otherwise pass with checked == 0 unseen.
    skipped_pairings: List[Pairing] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.findings

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
                f"pairing{'' if self.skipped == 1 else 's'} skipped.")
        lines = [head] + [f.message() for f in self.findings]
        if self.skipped_pairings:
            lines.append(self.skipped_message())
        return "\n".join(lines)


class GateFailure(Exception):
    def __init__(self, report: GateReport):
        self.report = report
        lines = [f.message() for f in report.findings]
        if report.skipped_pairings:
            lines.append(report.skipped_message())
        super().__init__("\n".join(lines))


def _hex(ts: TokenSet, path: str, mode: str) -> str:
    value = ts.resolve(path, mode)
    try:
        hex_to_rgb(value)
    except ValueError:
        raise ValueError(
            f"{path} ({mode}) resolves to {value!r}, which is not a hex color; "
            "use #RRGGBB or #RGB, and run validate() first to see every such problem"
        ) from None
    return value


def gate(ts: TokenSet, pairings: Iterable[Pairing],
         raise_on_fail: bool = True) -> GateReport:
    report = GateReport()
    for p in pairings:
        if not (ts.has(p.fg) and ts.has(p.bg)):
            report.skipped_pairings.append(p)
            continue
        for mode in ts.mode_names:
            report.checked += 1
            ratio = contrast(_hex(ts, p.fg, mode), _hex(ts, p.bg, mode))
            if ratio < p.minimum:
                report.findings.append(
                    GateFinding(p.fg, p.bg, mode, ratio, p.minimum, p.criterion))
    if raise_on_fail and not report.passed:
        raise GateFailure(report)
    return report
