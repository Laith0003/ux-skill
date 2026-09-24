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
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.build import FOUNDATIONS, ValidationError, build_system
from engine.foundations.color_math import hex_to_rgb, rgb_to_hex
from engine.foundations.export import dump_dtcg, to_css
from engine.foundations.gate import GateFailure, GateReport
from engine.synthesizer.axes import (
    AXIS_NAMES, FORBIDDEN_CLAMPS, INDUSTRY_SEEDS, TONE_NUDGES, AxisValues, _apply_tone_nudges,
    _normalize_tag, _seed_from_industry, compute_axes,
)

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
        numbers.append(number + 0.0)  # -0 reads as 0
    return AxisValues(*numbers)


def _json_kind(payload: Any) -> str:
    """A JSON value's kind in JSON's own words, not Python's."""
    if payload is None:
        return "null"
    if isinstance(payload, bool):
        return "true or false"
    if isinstance(payload, str):
        return "string"
    if isinstance(payload, (int, float)):
        return "number"
    return "list"


def _brief_text(data: bytes) -> str:
    """The text of a brief file. UTF-8, with Notepad's leading mark
    dropped; a file that starts with the UTF-16 mark (Windows PowerShell 5.1
    writes one) is read as UTF-16. Raises UnicodeDecodeError otherwise."""
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16")
    return data.decode("utf-8-sig")


def read_brief(path: Any, label: str = "brief") -> Dict[str, Any]:
    """A brief file as a dict. A discovery file (answers nested under
    "answers") is flattened, as `uxskill recommend --brief-file` does."""
    p = Path(path).expanduser()
    try:
        data = p.read_bytes()
    except OSError as exc:
        raise InputError(f"{label} {p} cannot be read ({exc.strerror or exc}); pass the path "
                         "of a JSON brief, for example .ux/last-discovery.json") from None
    try:
        text = _brief_text(data)
    except UnicodeDecodeError:
        raise InputError(f"{label} {p} is not UTF-8 text; save the brief as UTF-8 and pass it "
                         "again") from None
    try:
        payload = json.loads(text)
    except ValueError as exc:
        raise InputError(f"{label} {p} is not valid JSON ({exc}); fix the file, or pass a JSON "
                         'object such as {"industry": "saas", "tone": ["warm"]}') from None
    if isinstance(payload, dict) and isinstance(payload.get("answers"), dict):
        payload = payload["answers"]
    if not isinstance(payload, dict):
        raise InputError(f"{label} {p} holds a JSON {_json_kind(payload)}, not an object; "
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


def _reading(key: str, word: str) -> Optional[str]:
    """How the synthesizer reads one brief word: the word, the industry it
    was matched to, or None when the word moves no axis. Asks the
    synthesizer's own lookups, so the two can never disagree."""
    if key == "industry":
        seed = _seed_from_industry(word)
        match = next((k for k, v in INDUSTRY_SEEDS.items() if v == seed), None)
        if match is None:
            return None
        return word if _normalize_tag(word) == match else f"{word}, read as {match}"
    if key == "forbidden":
        return word if _normalize_tag(word) in FORBIDDEN_CLAMPS else None
    neutral = dict(NEUTRAL.to_dict())
    return word if _apply_tone_nudges(dict(neutral), [word]) != neutral else None


def _accepted(key: str) -> Tuple[str, ...]:
    """The words the synthesizer knows for a brief field."""
    if key == "industry":
        return tuple(sorted(INDUSTRY_SEEDS))
    if key == "forbidden":
        return tuple(sorted(FORBIDDEN_CLAMPS))
    return tuple(sorted(TONE_NUDGES))


def _accepted_lines(keys: Sequence[str]) -> List[str]:
    """One sentence per vocabulary, naming every field that uses it."""
    groups: Dict[Tuple[str, ...], List[str]] = {}
    for key in keys:
        groups.setdefault(_accepted(key), []).append(key)
    lines = []
    for words, fields in groups.items():
        names = fields[0] if len(fields) == 1 else (", ".join(fields[:-1]) + " and " + fields[-1])
        lines.append(f"{names} {'accepts' if len(fields) == 1 else 'accept'}: "
                     f"{', '.join(words)}.")
    return lines


def brief_axes(brief: Mapping[str, Any], label: str = "brief", *,
               axes_label: str = "axes") -> Tuple[AxisValues, str]:
    """Axes from a brief through the synthesizer, and a sentence saying so.
    A discovery brief (answers nested under "answers") is read the same as
    a flat one. The sentence names the words that were read and the words
    that were ignored because the synthesizer does not know them. A brief
    with none of BRIEF_FIELDS, or with no word the synthesizer knows, is
    refused rather than silently read as neutral."""
    if isinstance(brief.get("answers"), dict):
        brief = brief["answers"]
    values = _brief_values(brief, label)
    if not values:
        raise InputError(f"{label} has none of {', '.join(BRIEF_FIELDS)}; add at least one "
                         f'(for example "industry": "saas"), or pass {axes_label} instead')
    known: Dict[str, List[str]] = {}
    unknown: List[Tuple[str, str]] = []
    for key, value in values.items():
        for word in ([value] if isinstance(value, str) else value):
            reading = _reading(key, word)
            if reading is None:
                unknown.append((key, word))
            else:
                known.setdefault(key, []).append(reading)
    ignored = ", ".join(f"{word} ({key})" for key, word in unknown)
    if not known:
        fields = [k for k in BRIEF_FIELDS if any(k == key for key, _ in unknown)]
        raise InputError(" ".join([
            f"{label} has no word the engine recognizes, so it would build the same system as "
            f"no brief. Not recognized: {ignored}.",
            f"Use at least one accepted word, or pass {axes_label} instead.",
            *_accepted_lines(fields)]))
    axes = compute_axes(values)
    source = "from the brief (" + "; ".join(f"{k}: {', '.join(v)}" for k, v in known.items()) + ")"
    if axes == NEUTRAL:
        source += ", which leaves every axis at 0.5"
    if unknown:
        source += f"; not recognized and ignored: {ignored}"
    return axes, source


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
        return brief_axes(brief, brief_label, axes_label=axes_label)
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


# Report words. Each table is keyed by the engine's own names, and a test
# holds it to them, so a new foundation, mode or axis cannot go unworded.
_FOUNDATION_WORDS: Dict[str, str] = {
    "color": "color", "space": "spacing", "radius": "radius", "border": "borders",
    "elevation": "elevation", "motion": "motion", "layout": "layout", "type": "type"}

# Each mode axis: both values together for the opening sentence, then each
# value alone, in the words a context key is read out in.
_MODE_WORDS: Dict[str, Tuple[str, Dict[str, str]]] = {
    "scheme": ("light and dark", {"light": "light mode", "dark": "dark mode"}),
    "contrast": ("standard and high contrast",
                 {"standard": "standard contrast", "high": "high contrast"}),
    "density": ("comfortable and compact spacing",
                {"comfortable": "comfortable spacing", "compact": "compact spacing"}),
    "direction": ("left to right and right to left",
                  {"ltr": "left to right", "rtl": "right to left"}),
    "motion": ("full and reduced motion", {"standard": "full motion", "reduced": "reduced motion"}),
}

# Each design axis: its name in words, and what 0 and 1 mean.
_AXIS_WORDS: Dict[str, Tuple[str, str, str]] = {
    "warmth": ("warmth", "cool", "warm"),
    "contrast": ("contrast", "muted", "bold"),
    "density": ("density", "airy", "packed"),
    "geometry": ("geometry", "sharp", "rounded"),
    "formality": ("formality", "playful", "formal"),
    "motion": ("motion", "still", "lively"),
    "type_personality": ("type personality", "geometric", "humanist"),
}

_RATIO_WORDS = {"text/fill": "text on the fill", "fill/page": "the fill on the page",
                "ring/surface": "the focus ring on the surface"}

_CONTEXT_KEY = re.compile(r"\((in )?([a-z]+:[a-z]+(?:,[a-z]+:[a-z]+)*)\)")
_PAIRING_NOTE = re.compile(
    r"^(?P<fg>\S+) \((?P<mode>[a-z:,]+)\): (?P<old>\S+) -> (?P<new>\S+), (?P=fg) on (?P<bg>\S+) "
    r"was (?P<was>[\d.]+:1), now (?P<now>[\d.]+:1), (?P<why>.+)$")
_GROUP_NOTE = re.compile(r"^(?P<fill>\S+) group \((?P<mode>[a-z:,]+)\): (?P<rest>.+)$")
_GROUP_MOVE = re.compile(r"^(\S+) (\S+) -> (\S+)$")
_GROUP_RATIO = re.compile(r"^(text/fill|fill/page|ring/surface) ([\d.]+:1)$")
_RAMP_NOTE = re.compile(
    r"^color\.(?P<family>[\w-]+): (?P<seed>#[0-9A-Fa-f]{6}) is too (?P<way>light|dark) to anchor "
    r"a ramp at 500; 500 retuned to (?P<anchor>#[0-9A-Fa-f]{6}), (?P<why>.+)\.$")
_MOVE_SENTENCE = re.compile(r"^(?P<head>.*?:1\)?)\. Move \S+ to a step with more contrast against "
                            r"\S+\.(?: .*)?$")
_VALIDATION = "Validation failed"


def _and(items: Sequence[str]) -> str:
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _context_words(key: str) -> str:
    """A context key in words: "scheme:dark,contrast:high" reads "dark mode,
    high contrast". A key with a part the table does not know is kept."""
    words = []
    for pair in key.split(","):
        axis, _, value = pair.partition(":")
        word = _MODE_WORDS.get(axis, ("", {}))[1].get(value)
        if not word:
            return key
        words.append(word)
    return ", ".join(words)


def _in_words(text: str) -> str:
    """Every "(key)" and "(in key)" context in a line, read out in words."""
    return _CONTEXT_KEY.sub(lambda m: f"({m.group(1) or ''}{_context_words(m.group(2))})", text)


def _contrast_note(note: str) -> Optional[str]:
    """A note about a color moved to meet contrast, in plain words, or None
    when the note is not one."""
    m = _PAIRING_NOTE.match(note)
    if m:
        return (f"In {_context_words(m['mode'])}, {m['fg']} moved from {m['old']} to {m['new']}: "
                f"on {m['bg']} it measured {m['was']}, now {m['now']}, and {m['why']}.")
    m = _GROUP_NOTE.match(note)
    if not m:
        return None
    moves, ratios = [], []
    for part in m["rest"].split(", "):
        move, ratio = _GROUP_MOVE.match(part), _GROUP_RATIO.match(part)
        if move:
            moves.append(f"{move[1]} from {move[2]} to {move[3]}")
        elif ratio:
            ratios.append(f"{ratio[2]} for {_RATIO_WORDS[ratio[1]]}")
        else:
            return _in_words(note)
    if not moves:
        return _in_words(note)
    text = (f"In {_context_words(m['mode'])}, for the {m['fill']} button the engine changed "
            f"{_and(moves)}.")
    return text + (f" It now measures {_and(ratios)}." if ratios else "")


def _other_note(note: str) -> str:
    m = _RAMP_NOTE.match(note)
    if not m:
        return _in_words(note)
    who = "The brand color" if m["family"] == "brand" else f"The {m['family']} color"
    return (f"{who} {m['seed']} is too {m['way']} to sit at step 500, the middle of its color "
            f"scale, so step 500 is {m['anchor']} ({m['why']}).")


def _finding_line(finding: SystemFinding) -> str:
    """A finding for the report: the measurement, modes in words. The
    engine's advice to move a token is left to the JSON findings, since no
    input moves a token; the report says which inputs to change instead."""
    line = finding.line()
    m = _MOVE_SENTENCE.match(line)
    return _in_words(f"{m['head']}." if m else line)


def _opening(brand: str, gate_line: str, findings: Sequence[SystemFinding]) -> str:
    if findings:
        n = len(findings)
        if gate_line.startswith(_VALIDATION):
            why = (f"the generated tokens broke {n} structural rule{'' if n == 1 else 's'}, so "
                   "the WCAG gate did not run and nothing was written")
        else:
            why = (f"the WCAG gate found {n} problem{'' if n == 1 else 's'} with these inputs, "
                   "so nothing was written")
        return f"No design system was built for {brand}: {why}."
    parts = _and([_FOUNDATION_WORDS.get(f.name, f.name) for f in FOUNDATIONS])
    modes = [pair for pair, _ in _MODE_WORDS.values()]
    return (f"A complete design system for {brand}: {parts}, in {', '.join(modes[:-1])}, and "
            f"{modes[-1]}. Every color pairing passed the WCAG contrast gate, so the files below "
            "are ready to use.")


def _axes_table(axes: AxisValues) -> List[str]:
    rows = ["Seven axes shape the look. Each runs from 0 to 1, and the scale says what each end "
            "means.", "", "| Axis | Value | Scale |", "|---|---|---|"]
    for name, value in axes.to_dict().items():
        words, low, high = _AXIS_WORDS[name]
        rows.append(f"| {words} | {value:g} | {low} 0 to {high} 1 |")
    return rows


_CHECKS_LINE = ("A check measures one color pairing, such as text on its background, in one mode; "
                "a rule check covers the rest, such as minimum sizes, widths and durations.")
_GATE_SCOPE = ("Color pairings were measured in light and dark, at standard and high contrast. "
               "Standard contrast meets WCAG 1.4.3 (text 4.5:1) and 1.4.11 (non-text 3:1). High "
               "contrast raises text to WCAG 1.4.6 (7:1) and most non-text parts to a 4.5:1 floor "
               "of our own, since WCAG sets no enhanced non-text level.")
_NOTES_LEAD = ("These are adjustments the engine made on its own, so nothing needs doing: first "
               "the colors it moved off their default step so every pairing meets its contrast "
               "minimum, and why, then the other choices it made from the brand color and the "
               "axes. Modes are named in words; tokens.json keys the same modes, so dark mode, "
               "high contrast is scheme:dark,contrast:high there.")
_CHANGE_GATE = ("Change the inputs and build again: a darker or more saturated brand "
                "color gives the engine more room to reach every contrast "
                "minimum, and different axes, or a different brief, change the steps it tries. "
                "The findings below name each pairing that fell short, for a design-system "
                "designer.")
_CHANGE_VALIDATION = ("No brand color or axes should cause this, so it is a problem in the "
                      "engine: build again with the same inputs, and if it fails "
                      "again, report it with the brand color, the axes and the findings below.")
_MODES_LINE = ("Switch a mode with an attribute on the html element: data-theme=\"dark\" for dark "
               "mode, data-contrast=\"high\" for high contrast, data-density=\"compact\" for "
               "compact spacing, dir=\"rtl\" for right to left, data-motion=\"reduced\" for "
               "reduced motion. With no attribute, dark mode, high contrast and reduced motion "
               "follow the operating system setting.")


def render_report(brand: str, axes: AxisValues, axes_source: str, arabic: bool,
                  gate_line: str, notes: Sequence[str],
                  findings: Sequence[SystemFinding]) -> str:
    """system-report.md: one sentence on what was built, what it was built
    from, the gate result, every note or finding in plain words, and how to
    use the files. No time stamps, so the same inputs give the same bytes."""
    scripts = ("Latin and Arabic. Right to left (dir=\"rtl\") switches text to the Arabic face "
               "and type scale." if arabic else "Latin only (built with the Latin-only option).")
    lines = ["# Design system report", "", _opening(brand, gate_line, findings), "",
             "## Built from", "", f"- Brand color: {brand}", f"- Scripts: {scripts}",
             f"- Axes: {axes_source}.", "", *_axes_table(axes), "",
             "## WCAG gate", "", gate_line, "", _CHECKS_LINE, ""]
    if findings:
        change = _CHANGE_VALIDATION if gate_line.startswith(_VALIDATION) else _CHANGE_GATE
        lines += ["## What to change", "", change, "", "## Findings", ""]
        lines += [f"- {_finding_line(f)}" for f in findings]
        return "\n".join(lines) + "\n"
    lines += [_GATE_SCOPE, ""]
    moved: List[str] = []
    other: List[str] = []
    for note in notes:
        plain = _contrast_note(note)
        if plain is None:
            other.append(_other_note(note))
        else:
            moved.append(plain)
    if notes:
        lines += ["## Notes", "", _NOTES_LEAD, ""]
        if moved:
            lines += ["### Colors moved to meet contrast", "", *[f"- {n}" for n in moved], ""]
        if other:
            lines += ["### Other choices", "", *[f"- {n}" for n in other], ""]
    lines += ["## Files", "",
              "- tokens.json: every token in the W3C design tokens format (DTCG 2025.10), with "
              "its values for each mode.",
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
    return SystemOutput(passed=bool(tokens), files=files, report=report, gate=gate,
                        findings=findings, brand=brand, axes=axes, axes_source=axes_source,
                        arabic=arabic)


# ---------------------------------------------------------------- write


@dataclass(frozen=True)
class WritePlan:
    """Where each file stands against the output folder. `conflicts` are
    files that exist with different content; they are replaced only when
    the caller forces it. `unchanged` files are identical and left alone."""
    write: Tuple[str, ...]
    unchanged: Tuple[str, ...]
    conflicts: Tuple[str, ...]


def _reason(exc: OSError) -> str:
    """The operating system's own words for a failure, such as "Permission
    denied"."""
    return exc.strerror or type(exc).__name__


def _broken_link(label: str, link: Path) -> InputError:
    return InputError(f"{label}{link} is a link to {os.readlink(str(link))}, which does not "
                      "exist; remove the link, or write the system into a different folder")


def check_out_dir(out_dir: Any, label: str = "out") -> Path:
    """The output folder as a Path. It may not exist yet; it may not be a
    file, a broken link, or sit inside a file."""
    if out_dir is None or not str(out_dir).strip():
        raise InputError(f"{label} is missing; pass the folder to write the system into, "
                         "for example design-system")
    p = Path(out_dir).expanduser()
    try:
        if p.is_symlink() and not p.exists():
            raise _broken_link(f"{label} ", p)
        if p.exists():
            if not p.is_dir():
                raise InputError(f"{label} {p} is a file, not a folder; pass a folder path, "
                                 f"for example {p.parent / 'design-system'}")
            return p
        for parent in p.parents:
            if parent.is_symlink() and not parent.exists():
                raise _broken_link(f"{label} {p} is inside ", parent)
            if parent.exists():
                if not parent.is_dir():
                    raise InputError(f"{label} {p} is inside {parent}, which is a file, so the "
                                     "folder cannot be made; pass a folder path that is not "
                                     f"inside a file, for example "
                                     f"{parent.parent / 'design-system'}")
                break
    except OSError as exc:
        raise InputError(f"{label} {p} cannot be checked ({_reason(exc)}); pass a folder you "
                         "can read and write") from None
    return p


def _same_as_disk(target: Path, name: str, data: bytes) -> bool:
    try:
        return target.read_bytes() == data
    except OSError as exc:
        raise InputError(f"{target} exists but cannot be read ({_reason(exc)}), so it cannot "
                         f"be compared with the new {name}; make it readable, move it away, or "
                         "write the system into a different folder") from None


def plan_writes(out_dir: Path, files: Mapping[str, str]) -> WritePlan:
    """Compare each file with what is on disk, without writing. A link in
    place of a file is never written through or replaced: an identical one
    is left alone, any other is refused."""
    write: List[str] = []
    unchanged: List[str] = []
    conflicts: List[str] = []
    for name, text in files.items():
        target = out_dir / name
        data = text.encode("utf-8")
        try:
            if target.is_dir():
                raise InputError(f"{target} is a folder, so {name} cannot be written there; "
                                 "rename that folder or write the system into a different "
                                 "folder")
            if target.is_symlink():
                if not target.exists():
                    raise _broken_link("", target)
                if not _same_as_disk(target, name, data):
                    raise InputError(f"{target} is a link to {os.readlink(str(target))}; the "
                                     "system is written only as plain files, so remove the "
                                     "link, or write the system into a different folder")
                unchanged.append(name)
            elif not target.exists():
                write.append(name)
            elif _same_as_disk(target, name, data):
                unchanged.append(name)
            else:
                conflicts.append(name)
        except OSError as exc:
            raise InputError(f"{target} cannot be checked ({_reason(exc)}); pass a folder you "
                             "can read and write") from None
    return WritePlan(tuple(write), tuple(unchanged), tuple(conflicts))


def conflict_message(out_dir: Path, plan: WritePlan, force_flag: str = "--force",
                     out_flag: str = "--out") -> str:
    """Why nothing was written: every file that differs, and the two fixes."""
    names = ", ".join(str(out_dir / n) for n in plan.conflicts)
    return (f"Nothing was written: {names} already "
            f"{'exists' if len(plan.conflicts) == 1 else 'exist'} with different content. "
            f"Pass {force_flag} to replace {'it' if len(plan.conflicts) == 1 else 'them'}, or "
            f"pass a different {out_flag} folder.")


def _stage(path: Path, data: bytes) -> None:
    """Write one file into the staging folder."""
    path.write_bytes(data)


def _place(staged: Path, target: Path) -> None:
    """Move one staged file into place. A rename within one folder, so a
    reader never sees half a file."""
    os.replace(str(staged), str(target))


def _missing_folders(folder: Path) -> List[Path]:
    """The folders a mkdir with parents would make, innermost first."""
    missing: List[Path] = []
    for q in (folder, *folder.parents):
        if q.exists():
            break
        missing.append(q)
    return missing


def _remove_folders(folders: Sequence[Path]) -> None:
    for q in folders:
        try:
            q.rmdir()
        except OSError:
            pass


def _restore(out_dir: Path, placed: Sequence[Tuple[str, Optional[Path]]]) -> bool:
    """Undo the moves so far: put each previous file back and remove each
    new one. False when a previous file could not be put back."""
    whole = True
    for name, previous in reversed(placed):
        target = out_dir / name
        try:
            if previous is not None:
                os.replace(str(previous), str(target))
            elif target.exists():
                target.unlink()
        except OSError:
            whole = whole and previous is None
    return whole


def write_files(out_dir: Path, files: Mapping[str, str], *, force: bool = False) -> WritePlan:
    """Write the files that are new or, when forced, different. Without
    force, one conflicting file stops every write. Identical files are
    never rewritten. All or nothing: every file is staged in a folder
    inside out_dir and then moved into place, and a failure at any step
    puts the folder back as it was, so it never holds a mix of two
    systems. Returns the plan it acted on; `conflicts` is non-empty only
    when nothing was written. Every filesystem error is an InputError
    naming the path and the fix."""
    if not files:
        return WritePlan((), (), ())
    plan = plan_writes(out_dir, files)
    if plan.conflicts and not force:
        return plan
    names = plan.write + plan.conflicts
    if not names:
        return WritePlan((), plan.unchanged, ())
    made = _missing_folders(out_dir)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        _remove_folders(made)
        raise InputError(f"{out_dir} cannot be made ({_reason(exc)}); pass a folder you can "
                         "write to") from None
    try:
        stage = Path(tempfile.mkdtemp(prefix=".uxskill-", dir=str(out_dir)))
    except OSError as exc:
        _remove_folders(made)
        raise InputError(f"{out_dir} cannot be written ({_reason(exc)}), so nothing in it was "
                         "changed; pass a folder you can write to") from None
    placed: List[Tuple[str, Optional[Path]]] = []
    name = names[0]
    try:
        for name in names:
            _stage(stage / name, files[name].encode("utf-8"))
        for name in names:
            previous = None
            if name in plan.conflicts:
                previous = stage / f"{name}.previous"
                os.replace(str(out_dir / name), str(previous))
            placed.append((name, previous))
            _place(stage / name, out_dir / name)
    except OSError as exc:
        if not _restore(out_dir, placed):
            raise InputError(f"{out_dir / name} could not be written ({_reason(exc)}), and the "
                             f"previous files could not all be put back; they are in {stage}. "
                             "Move them back into place, then pass a folder you can write "
                             "to") from None
        shutil.rmtree(str(stage), ignore_errors=True)
        _remove_folders(made)
        raise InputError(f"{out_dir / name} could not be written ({_reason(exc)}), so nothing "
                         f"in {out_dir} was changed; free some space or pass a folder you can "
                         "write to") from None
    shutil.rmtree(str(stage), ignore_errors=True)
    return WritePlan(names, plan.unchanged, ())
