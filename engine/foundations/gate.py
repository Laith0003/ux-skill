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
    skipped: int = 0

    @property
    def passed(self) -> bool:
        return not self.findings


class GateFailure(Exception):
    def __init__(self, report: GateReport):
        self.report = report
        super().__init__("\n".join(f.message() for f in report.findings))


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
            report.skipped += 1
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
