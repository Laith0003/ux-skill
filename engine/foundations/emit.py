"""From user inputs to the three files a builder keeps: tokens.json,
tokens.css and system-report.md.

The CLI (`uxskill system build`) and the MCP tool (`ux_system_build`) are
thin callers of this module, so both read inputs, word errors and gate the
same way. Every InputError names the input by the label its caller passes
("--brand" on the command line, "brand" over MCP) and says the fix.

Nothing here writes a file except write_files, and it never replaces a
file that differs unless the caller forces it.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.build import ValidationError, build_system
from engine.foundations.color_math import hex_to_rgb, rgb_to_hex
from engine.foundations.export import dump_dtcg, to_css
from engine.foundations.gate import GateFailure, GateReport
from engine.synthesizer.axes import AXIS_NAMES, AxisValues, compute_axes

# The files a build writes, in the order they are written and reported.
FILES: Tuple[str, ...] = ("tokens.json", "tokens.css", "system-report.md")

# Brief fields the synthesizer reads to place the axes.
BRIEF_FIELDS: Tuple[str, ...] = ("industry", "tone", "audience", "must_have", "forbidden")
_LIST_FIELDS = ("tone", "audience", "must_have", "forbidden")

NEUTRAL = AxisValues(*([0.5] * len(AXIS_NAMES)))
NEUTRAL_SOURCE = "neutral default: every axis at 0.5, since no brief or axes were given"

_AXES_EXAMPLE = ",".join(["0.5"] * len(AXIS_NAMES))


class InputError(ValueError):
    """A bad input. The message names the input and the fix."""


# ---------------------------------------------------------------- inputs


def parse_brand(value: Any, label: str = "brand") -> str:
    """The brand color as #RRGGBB (upper case). Accepts #RGB, #RRGGBB and
    the same without the leading #, since a shell drops an unquoted word
    that starts with #."""
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} is missing; pass the brand color as a hex string, "
                         "for example '#3366FF' (quote it in a shell) or 3366FF")
    try:
        return rgb_to_hex(hex_to_rgb(value.strip()))
    except ValueError:
        raise InputError(f"{label} is {value!r}, which is not a hex color; pass #RRGGBB or "
                         "#RGB, for example '#3366FF' (quote it in a shell) or 3366FF") from None


def parse_axes(value: Any, label: str = "axes") -> AxisValues:
    """Seven numbers from 0 to 1, in AXIS_NAMES order: a comma-separated
    string (the CLI) or a list (MCP)."""
    order = ",".join(AXIS_NAMES)
    if isinstance(value, str):
        items: List[Any] = [s.strip() for s in value.split(",")]
    elif isinstance(value, (list, tuple)):
        items = list(value)
    else:
        raise InputError(f"{label} is {value!r}; pass seven numbers from 0 to 1 in the order "
                         f"{order}, for example {_AXES_EXAMPLE}")
    if len(items) != len(AXIS_NAMES):
        raise InputError(f"{label} has {len(items)} value{'' if len(items) == 1 else 's'}; pass "
                         f"seven numbers from 0 to 1 in the order {order}, for example "
                         f"{_AXES_EXAMPLE}")
    numbers: List[float] = []
    for name, raw in zip(AXIS_NAMES, items):
        try:
            if isinstance(raw, bool):
                raise ValueError
            number = float(raw)
        except (TypeError, ValueError):
            raise InputError(f"{label} gives {name} as {raw!r}; set it to a number from 0 to 1"
                             ) from None
        if not (math.isfinite(number) and 0.0 <= number <= 1.0):
            raise InputError(f"{label} gives {name} as {raw!r}; set it to a number from 0 to 1")
        numbers.append(number)
    return AxisValues(*numbers)


def read_brief(path: Any, label: str = "brief") -> Dict[str, Any]:
    """A brief file as a dict. A discovery file (answers nested under
    "answers") is flattened, as `uxskill recommend --brief-file` does."""
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"{label} {p} cannot be read ({exc.strerror or exc}); pass the path "
                         "of a JSON brief, for example .ux/last-discovery.json") from None
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise InputError(f"{label} {p} is not valid JSON ({exc}); fix the file, or pass a JSON "
                         'object such as {"industry": "saas", "tone": ["warm"]}') from None
    if isinstance(payload, dict) and isinstance(payload.get("answers"), dict):
        payload = payload["answers"]
    if not isinstance(payload, dict):
        raise InputError(f"{label} {p} holds a JSON {type(payload).__name__}, not an object; "
                         'pass an object such as {"industry": "saas", "tone": ["warm"]}')
    return payload


def _brief_values(brief: Mapping[str, Any], label: str) -> Dict[str, Any]:
    """The fields the synthesizer reads, with comma strings split into
    lists as `uxskill recommend` accepts them."""
    out: Dict[str, Any] = {}
    for key in BRIEF_FIELDS:
        value = brief.get(key)
        if value in (None, "", []):
            continue
        if key in _LIST_FIELDS:
            if isinstance(value, str):
                value = [s.strip() for s in value.split(",") if s.strip()]
            if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                raise InputError(f"{label} field {key} is {value!r}; give a list of words, "
                                 f'for example "{key}": ["warm", "calm"]')
        elif not isinstance(value, str):
            raise InputError(f"{label} field {key} is {value!r}; give a word, for example "
                             f'"{key}": "saas"')
        if value:
            out[key] = value
    return out


def brief_axes(brief: Mapping[str, Any], label: str = "brief") -> Tuple[AxisValues, str]:
    """Axes from a brief through the synthesizer, and a sentence saying so.
    A discovery brief (answers nested under "answers") is read the same as
    a flat one. A brief with none of BRIEF_FIELDS is refused rather than
    silently read as neutral."""
    if isinstance(brief.get("answers"), dict):
        brief = brief["answers"]
    values = _brief_values(brief, label)
    if not values:
        raise InputError(f"{label} has none of {', '.join(BRIEF_FIELDS)}; add at least one "
                         '(for example "industry": "saas"), or pass axes instead')
    parts = [f"{k}: {v if isinstance(v, str) else ', '.join(v)}" for k, v in values.items()]
    return compute_axes(values), "from the brief (" + "; ".join(parts) + ")"


def choose_axes(brief: Optional[Mapping[str, Any]], axes: Any, *,
                brief_label: str = "brief", axes_label: str = "axes"
                ) -> Tuple[AxisValues, str]:
    """The axes to build with and where they came from: the brief, the
    axes given, or the neutral default. Both given is an error, since the
    brief would decide the axes and silently override them."""
    if brief is not None and axes is not None:
        raise InputError(f"both {brief_label} and {axes_label} were given; pass one: the brief "
                         f"places the axes itself, and {axes_label} sets them by hand")
    if brief is not None:
        return brief_axes(brief, brief_label)
    if axes is not None:
        return parse_axes(axes, axes_label), f"set by hand ({axes_label})"
    return NEUTRAL, NEUTRAL_SOURCE


# ---------------------------------------------------------------- build


@dataclass(frozen=True)
class SystemFinding:
    """One reason the system was not emitted. `subject` is the pairing,
    the check or the token; `context` the mode it failed in ("" when it
    fails in every mode); `message` names the token and the fix."""
    subject: str
    context: str
    message: str

    def to_dict(self) -> Dict[str, str]:
        return {"subject": self.subject, "context": self.context, "message": self.message}

    def line(self) -> str:
        """The message, with the mode added when the message does not name it."""
        if self.context and self.context not in self.message:
            return f"{self.message} (in {self.context})"
        return self.message


@dataclass(frozen=True)
class SystemOutput:
    """A built system. `files` maps each name in FILES to its text and is
    empty when the build failed; `report` is written either way. `gate` is
    the one-line result: the gate summary, or why the gate did not run."""
    passed: bool
    files: Mapping[str, str]
    report: str
    gate: str
    findings: Tuple[SystemFinding, ...]
    brand: str
    axes: AxisValues
    axes_source: str
    arabic: bool

    def to_dict(self) -> Dict[str, Any]:
        return {"passed": self.passed, "gate": self.gate, "brand": self.brand,
                "axes": self.axes.to_dict(), "axes_source": self.axes_source,
                "arabic": self.arabic, "findings": [f.to_dict() for f in self.findings]}


def _gate_findings(report: GateReport) -> List[SystemFinding]:
    out = [SystemFinding(f"{f.fg} on {f.bg}", f.mode, f.message()) for f in report.findings]
    out += [SystemFinding(c.check, c.mode, c.message) for c in report.failures]
    return out


def _axes_table(axes: AxisValues) -> List[str]:
    rows = ["| Axis | Value |", "|---|---|"]
    rows += [f"| {name} | {value:g} |" for name, value in axes.to_dict().items()]
    return rows


_GATE_SCOPE = ("Color pairings were measured in light and dark, at standard and high contrast. "
               "Standard contrast meets WCAG 1.4.3 (text 4.5:1) and 1.4.11 (non-text 3:1). High "
               "contrast raises text to WCAG 1.4.6 (7:1) and most non-text parts to a 4.5:1 floor "
               "of our own, since WCAG sets no enhanced non-text level.")

_MODES_LINE = ("Switch a mode on the html element: data-theme=\"dark\", data-contrast=\"high\", "
               "data-density=\"compact\", dir=\"rtl\", data-motion=\"reduced\". With no attribute, "
               "dark, high contrast and reduced motion follow the operating system setting.")


def render_report(brand: str, axes: AxisValues, axes_source: str, arabic: bool,
                  gate_line: str, notes: Sequence[str],
                  findings: Sequence[SystemFinding]) -> str:
    """system-report.md: what was built from what, the gate result, every
    note or finding, and how to use the files. No time stamps, so the same
    inputs give the same bytes."""
    scripts = ("Latin and Arabic. dir=\"rtl\" switches text to the Arabic face and scale."
               if arabic else "Latin only (built with the Latin-only option).")
    lines = ["# Design system report", "",
             f"Brand color: {brand}", f"Scripts: {scripts}", f"Axes: {axes_source}.", "",
             *_axes_table(axes), "", "## WCAG gate", "", gate_line, ""]
    if findings:
        lines += ["Nothing was written. Fix each finding below, then build again.", "",
                  "## Findings", ""]
        lines += [f"- {f.line()}" for f in findings]
    else:
        lines += [_GATE_SCOPE, ""]
        if notes:
            lines += ["## Notes", ""] + [f"- {n}" for n in notes]
        lines += ["", "## Files", "",
                  "- tokens.json: every token in the W3C design tokens format (DTCG 2025.10), "
                  "with its values for each mode.",
                  f"- tokens.css: CSS custom properties. {_MODES_LINE}",
                  "- system-report.md: this report."]
    return "\n".join(lines) + "\n"


def make_system(brand: str, axes: AxisValues, axes_source: str, *,
                arabic: bool = True) -> SystemOutput:
    """Build, validate and gate. On success `files` holds all three texts;
    on a validation or gate failure `files` is empty and `findings` names
    every problem, so a caller can never write a failing system."""
    notes: Sequence[str] = ()
    tokens: Dict[str, str] = {}
    try:
        built = build_system(axes, brand, arabic=arabic)
    except ValidationError as exc:
        findings = tuple(SystemFinding(p.token, "", p.message) for p in exc.problems)
        n = len(findings)
        gate = (f"Validation failed: {n} problem{'' if n == 1 else 's'} in the token set, "
                "so the WCAG gate did not run.")
    except GateFailure as exc:
        findings = tuple(_gate_findings(exc.report))
        gate = exc.report.summary().splitlines()[0]
    else:
        findings = ()
        gate = built.report.summary().splitlines()[0]
        notes = built.notes
        tokens = {"tokens.json": dump_dtcg(built.tokens), "tokens.css": to_css(built.tokens)}
    report = render_report(brand, axes, axes_source, arabic, gate, notes, findings)
    files = {**tokens, "system-report.md": report} if tokens else {}
    return SystemOutput(passed=not findings, files=files, report=report, gate=gate,
                        findings=findings, brand=brand, axes=axes, axes_source=axes_source,
                        arabic=arabic)
