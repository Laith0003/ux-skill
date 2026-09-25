"""From user inputs to the files a builder keeps: tokens.json, tokens.css,
fonts.css, fonts-self-host.css and system-report.md.

The CLI (`uxskill system build`) and the MCP tool (`ux_system_build`) are
thin callers of this module, so both read inputs, word errors and gate the
same way. Every InputError names the input by the label its caller passes
("--brand" on the command line, "brand" over MCP) and says the fix.

Nothing here writes a file except write_files, and it never replaces a
file that differs unless the caller forces it.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import tempfile
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.audience import (
    FIELDS as AUDIENCE_FIELDS, HOW_TO_PASS, Audience, AudienceError, effects, read_audience,
    writes_arabic)
from engine.foundations.build import FOUNDATIONS, ValidationError, build_system
from engine.foundations.composition import choose as choose_composition
from engine.foundations.color import brand_fidelity
from engine.foundations.color_math import hex_to_rgb, rgb_to_hex
from engine.foundations.export import dump_dtcg, to_css
from engine.foundations.art import FILES as ART_FILES  # noqa: F401 (re-exported)
from engine.foundations.art import art_files
from engine.foundations.art import report_lines as art_lines
from engine.foundations.fonts import fonts_css, link_tags, loading_lines, self_host_css
from engine.foundations.gate import GateFailure, GateReport
from engine.synthesizer.axes import (
    AXIS_NAMES, FORBIDDEN_CLAMPS, INDUSTRY_SEEDS, NUDGE_LIMIT, TONE_NUDGES, AxisValues,
    _apply_tone_nudges, _normalize_tag, _seed_from_industry, check_character, compute_axes,
)

# The files a build writes, in the order they are written and reported.
FILES: Tuple[str, ...] = ("tokens.json", "tokens.css", "fonts.css", "fonts-self-host.css",
                          "system-report.md")
# The generated art (engine.foundations.art.FILES as ART_FILES) is written after FILES.
# The folder the rule pack is written into, inside the out folder, when asked.
RULE_PACK_DIR = "rule-pack"
# The file in it that records the sha256 of the tokens.json it was built from.
RULE_PACK_MANIFEST = "built-from.json"

# Every status `uxskill system build` reports, with its exit code: the
# files were written, or were already identical (0); a file in the out
# folder differs, the gate or validation failed, or the folder could not
# be written, and nothing changed (1). The CLI exits by this table and the
# /ux-system doc test holds its status table to it.
STATUS_EXIT: Dict[str, int] = {
    "written": 0, "unchanged": 0, "refused": 1, "failed": 1, "error": 1,
}
STATUSES: Tuple[str, ...] = tuple(STATUS_EXIT)

# Brief fields the synthesizer reads to place the axes; the structured
# fields in audience.FIELDS are read beside them.
BRIEF_FIELDS: Tuple[str, ...] = ("industry", "tone", "audience", "must_have", "forbidden")
_LIST_FIELDS = ("tone", "audience", "must_have", "forbidden")
# The brief's object of axis nudges: what a word the engine does not read
# means, from -NUDGE_LIMIT to NUDGE_LIMIT per axis, applied after the words.
CHARACTER_FIELD = "character"
_NUDGE_EXAMPLE = '"character": {"contrast": 0.1, "geometry": -0.1}'


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
    # Only a flag is typed into a shell, where an unquoted # starts a comment.
    shell = " (quote it in a shell)" if label.startswith("--") else ""
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{label} is missing; pass the brand color as a hex string, "
                         f"for example '#3366FF'{shell} or 3366FF")
    try:
        return rgb_to_hex(hex_to_rgb(value.strip()))
    except ValueError:
        raise InputError(f"{label} is {value!r}, which is not a hex color; pass #RRGGBB or "
                         f"#RGB, for example '#3366FF'{shell} or 3366FF") from None


def parse_switch(value: Any, label: str, true_means: str, false_means: str) -> bool:
    """An optional true or false; missing means false. Only a real true or
    false is read, so a word such as "maybe" is named instead of being
    guessed at."""
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    raise InputError(f"{label} is {value!r}; pass true to {true_means}, or false (the default) "
                     f"to {false_means}")


def parse_latin_only(value: Any, label: str = "latin_only") -> bool:
    """True leaves out the Arabic face and scale; missing means false."""
    return parse_switch(value, label, "leave out the Arabic face and scale", "keep them")


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


def brief_character(brief: Mapping[str, Any], label: str = "brief") -> Dict[str, float]:
    """The brief's character nudges by axis, in AXIS_NAMES order; empty when
    it has none. A bad object is an InputError naming the entry and the fix
    (axes.check_character)."""
    try:
        return check_character(brief.get(CHARACTER_FIELD), label)
    except ValueError as exc:
        raise InputError(str(exc)) from None


def _signed(v: float) -> str:
    return f"{v:+g}"


def nudge_lines(brief: Optional[Mapping[str, Any]], label: str = "brief") -> List[str]:
    """One line per character nudge: the axis, the nudge, the value the
    words gave and the value the build used, and the foundations the axis
    moves. Empty without nudges."""
    if brief is None:
        return []
    if isinstance(brief.get("answers"), dict):
        brief = brief["answers"]
    nudges = brief_character(brief, label)
    if not nudges:
        return []
    from engine.foundations.character import INFLUENCE
    values = _brief_values(brief, label)
    before = compute_axes(values).to_dict()
    after = compute_axes({**values, CHARACTER_FIELD: nudges}).to_dict()
    out = []
    for axis, nudge in nudges.items():
        name = _AXIS_WORDS[axis][0]
        line = f"{name} {_signed(nudge)}: from {before[axis]:g} to {after[axis]:g}"
        if round(after[axis] - before[axis], 3) != round(nudge, 3):
            line += (" (held at the end of the axis)" if after[axis] in (0.0, 1.0)
                     else " (held by a forbidden word)")
        reach = _and([_FOUNDATION_WORDS.get(f, f) for f in INFLUENCE.get(axis, ())])
        out.append(f"{line}; {name} moves {reach}.")
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
    nudges = brief_character(brief, label)
    said = ("; character nudges: " + ", ".join(f"{k} {_signed(v)}" for k, v in nudges.items())
            if nudges else "")
    structured = [k for k in AUDIENCE_FIELDS if brief.get(k) not in (None, "", [])]
    if not values and nudges:
        return (compute_axes({CHARACTER_FIELD: nudges}),
                f"from the brief's character nudges, from 0.5 on every axis{said}")
    if not values and structured:
        return NEUTRAL, (f"from the brief's fields ({', '.join(structured)}), which leave every "
                         "axis at 0.5")
    if not values:
        raise InputError(f"{label} has none of {', '.join(BRIEF_FIELDS + AUDIENCE_FIELDS)}; add "
                         'at least one (for example "industry": "saas" or "age": '
                         f'"older-adults"), or pass {axes_label} instead')
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
    if not known and nudges:
        axes = compute_axes({**values, CHARACTER_FIELD: nudges})
        return axes, (f"from the brief's character nudges, from 0.5 on every axis{said}; not "
                      f"recognized and ignored: {ignored}")
    if not known and structured:
        return NEUTRAL, (f"from the brief's fields ({', '.join(structured)}), which leave every "
                         f"axis at 0.5; not recognized and ignored: {ignored}")
    if not known:
        fields = [k for k in BRIEF_FIELDS if any(k == key for key, _ in unknown)]
        raise InputError(" ".join([
            f"{label} has no word the engine recognizes, so it would build the same system as "
            f"no brief. Not recognized: {ignored}.",
            f"Use at least one accepted word, or pass {axes_label} instead.",
            *_accepted_lines(fields)]))
    axes = compute_axes({**values, CHARACTER_FIELD: nudges} if nudges else values)
    source = "from the brief (" + "; ".join(f"{k}: {', '.join(v)}" for k, v in known.items()) + ")"
    if axes == NEUTRAL:
        source += ", which leaves every axis at 0.5"
    source += said
    if unknown:
        source += f"; not recognized and ignored: {ignored}"
    return axes, source


def unread_lines(brief: Optional[Mapping[str, Any]], label: str = "brief") -> List[str]:
    """Every brief word the engine did not read, each with how to say it so
    it is read. Empty when every word was read."""
    if brief is None:
        return []
    if isinstance(brief.get("answers"), dict):
        brief = brief["answers"]
    try:
        values = _brief_values(brief, label)
    except InputError:
        return []
    out = []
    for key, value in values.items():
        for word in ([value] if isinstance(value, str) else value):
            if _reading(key, word) is not None:
                continue
            if key == "industry":
                out.append(f'industry "{word}" is not one the engine knows. Pass the nearest of '
                           f"{', '.join(_accepted(key))}, or leave industry out and describe "
                           "the character with tone words.")
            elif key == "audience":
                ways = {h.split(" ", 1)[0]: h for h in HOW_TO_PASS[:4]}
                held = [k for k in ways if brief.get(k) not in (None, "", [])]
                missing = [h for k, h in ways.items() if k not in held]
                out.append(f'audience "{word}" is plain text, which the engine does not parse. '
                           + (f"Say who the readers are with the brief's fields: "
                              f"{'; '.join(missing)}." if missing else
                              f"The brief's fields {', '.join(held[:-1])} and {held[-1]} "
                              "already say who the readers are."))
            elif key == "forbidden":
                out.append(f'forbidden "{word}" limits no axis. forbidden accepts: '
                           f"{', '.join(_accepted(key))}.")
            else:
                out.append(f'{key} "{word}" moves no axis. {key} accepts: '
                           f"{', '.join(_accepted(key))}. Or pass what it means as character "
                           f"nudges from -{NUDGE_LIMIT:g} to {NUDGE_LIMIT:g} on the axes, for "
                           f"example {_NUDGE_EXAMPLE}.")
    for key, value in sorted(brief.items()):
        if key in BRIEF_FIELDS or key in AUDIENCE_FIELDS or key == CHARACTER_FIELD \
                or value in (None, "", [], {}):
            continue
        out.append(f'{key} "{_as_words(value)}" is not read by the system build'
                   + (_UNREAD_HINTS[key] if key in _UNREAD_HINTS
                      else ", so it changed nothing here."))
    return out


# How to pass what a field the build does not read means for the system.
_UNREAD_HINTS: Mapping[str, str] = {
    "region": ". Say what it means for the system with " + HOW_TO_PASS[1] + ".",
    "project_type": ". Say what the product is with " + HOW_TO_PASS[5] + ".",
}


def _as_words(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(v, str) for v in value):
        return ", ".join(value)
    return json.dumps(value, sort_keys=True, ensure_ascii=False)


def resolve_arabic(latin_only: bool, audience: Audience, flag: str = "latin_only") -> bool:
    """Whether the build keeps Arabic: the brief's languages, or an Arabic
    primary script, decide when the brief gives them; the flag decides
    otherwise. A brief that names Arabic with the flag set is refused,
    since the two disagree."""
    if audience.arabic is None:
        return not latin_only
    if audience.arabic and latin_only and not any(
            writes_arabic(t) for t in audience.languages):
        raise InputError(f"{flag} leaves Arabic out, but the brief's primary_script is arabic; "
                         f"drop {flag}, or set primary_script to latin")
    if audience.arabic and latin_only:
        raise InputError(f"{flag} leaves Arabic out, but the brief's languages "
                         f"({', '.join(audience.languages)}) include one written in Arabic "
                         f"script; drop {flag}, or take the Arabic languages out of the brief")
    return audience.arabic


def brief_audience(brief: Optional[Mapping[str, Any]], label: str = "brief") -> Audience:
    """The structured fields of a brief, with a bad field as an InputError
    that names it and the choices."""
    try:
        return read_audience(brief, label)
    except AudienceError as exc:
        raise InputError(str(exc)) from None


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
    # The rule pack folder in the out folder that was not built from these
    # tokens, and why, when note_rule_pack found one.
    stale_rule_pack: Optional[str] = None
    stale_reason: str = ""
    audience: Audience = Audience()
    unread: Tuple[str, ...] = ()
    composition: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"passed": self.passed, "gate": self.gate, "brand": self.brand,
                "axes": self.axes.to_dict(), "axes_source": self.axes_source,
                "arabic": self.arabic, "audience": self.audience.to_dict(),
                "unread": list(self.unread), "composition": dict(self.composition),
                "findings": [f.to_dict() for f in self.findings]}


def _gate_findings(report: GateReport) -> List[SystemFinding]:
    out = [SystemFinding(f"{f.fg} on {f.bg}", f.mode, f.message()) for f in report.findings]
    out += [SystemFinding(c.check, c.mode, c.message) for c in report.failures]
    return out


# Report words. Each table is keyed by the engine's own names, and a test
# holds it to them, so a new foundation, mode or axis cannot go unworded.
_FOUNDATION_WORDS: Dict[str, str] = {
    "color": "color", "space": "spacing", "radius": "radius", "border": "borders",
    "elevation": "elevation", "motion": "motion", "layout": "layout", "type": "type",
    "imagery": "imagery"}

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
                "edge/page": "the edge on the page",
                "fill/surface": "the fill on the surfaces it sits on",
                "edge/surface": "the edge on the surfaces it sits on",
                "fill/band": "the fill on the brand band",
                "ring/surface": "the focus ring on the surface"}

_CONTEXT_KEY = re.compile(r"\((in )?([a-z]+:[a-z]+(?:,[a-z]+:[a-z]+)*)\)")
_PAIRING_NOTE = re.compile(
    r"^(?P<fg>\S+) \((?P<mode>[a-z:,]+)\): (?P<old>\S+) -> (?P<new>\S+), (?P=fg) on (?P<bg>\S+) "
    r"was (?P<was>[\d.]+:1), now (?P<now>[\d.]+:1), (?P<why>.+)$")
_GROUP_NOTE = re.compile(r"^(?P<fill>\S+) group \((?P<mode>[a-z:,]+)\): (?P<rest>.+)$")
_GROUP_MOVE = re.compile(r"^(\S+) (\S+) -> (\S+)$")
_GROUP_RATIO = re.compile(
    r"^(text/fill|fill/page|edge/page|fill/surface|edge/surface|fill/band|ring/surface) "
    r"([\d.]+:1)$")
_RAMP_NOTE = re.compile(
    r"^color\.(?P<family>[\w-]+): (?P<seed>#[0-9A-Fa-f]{6}) is too (?P<way>light|dark) to anchor "
    r"a ramp at 500; 500 retuned to (?P<anchor>#[0-9A-Fa-f]{6}), (?P<why>.+)\.$")
_MOVE_SENTENCE = re.compile(r"^(?P<head>.*?:1\)?)\. Move \S+ to a step with more contrast against "
                            r"\S+\.(?: .*)?$")
_VALIDATION = "Validation failed"
_RULE_PACK = "The rule pack could not be built"


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
    role = _ROLE_NOTE.match(note)
    if role:
        brand, _, scores = role["why"].partition("; ")
        head = f"Brand role {role['role']}: {_ROLE_WORDS[role['role']]}"
        if scores:
            return (f"{head}. The brand color's own case for a fill scored {brand.split()[-1]}, "
                    "where a saturated mid tone scores 1 and a very light, very dark or grey "
                    f"brand 0; with the axes the roles scored {scores}, and the highest wins.")
        why = ("the brief set it" if role["why"] == "set by the brief"
               else f"the axes scored {role['why']}, and the highest wins")
        return f"{head} ({why})."
    natural = _NATURAL_NOTE.match(note)
    if natural:
        return (f"In {natural['ctx']}, {natural['fill']} is {natural['step']} with white text "
                f"rather than {natural['was']} with black text: black text there weighs "
                f"{natural['cost']} in naturalness, more than the move of {natural['move']} "
                "from the brand.")
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
        elif _RULE_PACK in gate_line:
            why = (f"the tokens passed the WCAG gate, but the rule pack found {n} "
                   f"problem{'' if n == 1 else 's'}, so nothing was written")
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
_NOTES_LEAD = ("These are choices the engine made from the inputs: first the colors it moved "
               "off their default step so every pairing meets its contrast minimum, and why, then "
               "the other choices it made from the brand color and the axes. Modes are named in "
               "words; tokens.json keys the same modes, so dark mode, high contrast is "
               "scheme:dark,contrast:high there.")
_AUDIENCE_LEAD = ("What the brief's fields changed, and why. The same inputs give the same "
                  "changes every time.")
_NUDGE_LEAD = ("What the brief's character nudges did: each moved one axis after the words, "
               "and the axis moves the foundations named.")
_UNREAD_LEAD = ("The engine reads a fixed vocabulary and the brief's structured fields. These "
                "words changed nothing; say them as below and build again, or they stay unread.")
_CHANGE_GATE = ("Change the inputs and build again: a darker or more saturated brand "
                "color gives the engine more room to reach every contrast "
                "minimum, and different axes, or a different brief, change the steps it tries. "
                "The findings below name each pairing that fell short, for a design-system "
                "designer.")
_CHANGE_VALIDATION = ("No brand color or axes should cause this, so it is a problem in the "
                      "engine: build again with the same inputs, and if it fails "
                      "again, report it with the brand color, the axes and the findings below.")
_CHANGE_PACK = ("No brand color or axes should cause this: the rule pack's guidance, contracts "
                "or decision records do not fit the tokens this version builds. Build again "
                "without the rule pack to get the tokens, and report the findings below.")
_PACK_LINE = ("- rule-pack/: the rules for AI agents and people: per foundation an "
              "architecture, reference, audit and handoff file, the content and right-to-left "
              "rules, the component contracts and the decision records. Start at "
              "rule-pack/README.md.")
_FIDELITY_LEAD = ("Where the brand color appears, and whether it stays exact in each mode. A "
                  "brand fill keeps the exact color whenever its text reads naturally on it; "
                  "where black text would sit on a saturated mid tone, or a mode needs more "
                  "contrast, it moves to the nearest step of the brand's scale, and the line "
                  "says how far.")
_FONTS_LEAD = ("The tokens name these faces. fonts.css holds a metric-matched fallback for "
               "each, so text keeps its size and line breaks while a face loads; it does not "
               "load the faces. Load them one of two ways, each together with fonts.css, both "
               "linked before tokens.css, and edit neither file.")
_FONTS_SELF_HOST = ("Self-hosted: link fonts-self-host.css and put the WOFF2 files it names in "
                    "a fonts/ folder beside it. A static face looks for the reader's installed "
                    "copy of each weight first.")
_COMPOSITION_LEAD = ("The layout a landing page starts from, scored from the axes and the brief's "
                     "fields; the landing playbooks build on it, and the JSON result names it as "
                     "composition.")
_ART_LEAD = ("Generated from the axes and the colors above, so a page is never empty for want "
             "of photos. Three layers, a quiet neutral plane, the brand's focal shape and "
             "support accents, split the drawn area about 60, 30 and 10 percent; warmth moves "
             "area from the neutral to the accents, geometry rounds the shapes, and formality "
             "sets how many accents there are and how square to their lines they sit.")
_ROLE_NOTE = re.compile(r"^color: brand role (?P<role>\w+) \((?P<why>.+)\)$")
_NATURAL_NOTE = re.compile(
    r"^color: in (?P<ctx>[a-z ,]+), (?P<fill>\S+) takes white text on (?P<step>\S+) rather than "
    r"black text on (?P<was>\S+): black there weighs (?P<cost>[\d.]+) in naturalness, more than "
    r"the move of (?P<move>[\d.]+) from the brand$")
_ROLE_WORDS = {"fill": "the brand fills the main action",
               "accent": "the brand marks words and links, and the main action is ink",
               "edge": "the brand draws edges and rules, and actions and links are ink"}
_MODES_LINE = ("Switch a mode with an attribute on the html element: data-theme=\"dark\" for dark "
               "mode, data-contrast=\"high\" for high contrast, data-density=\"compact\" for "
               "compact spacing, dir=\"rtl\" for right to left, data-motion=\"reduced\" for "
               "reduced motion. With no attribute, dark mode, high contrast and reduced motion "
               "follow the operating system setting.")


def _change(gate_line: str) -> str:
    if gate_line.startswith(_VALIDATION):
        return _CHANGE_VALIDATION
    return _CHANGE_PACK if _RULE_PACK in gate_line else _CHANGE_GATE


def render_report(brand: str, axes: AxisValues, axes_source: str, arabic: bool,
                  gate_line: str, notes: Sequence[str],
                  findings: Sequence[SystemFinding], rule_pack: bool = False,
                  fidelity: Sequence[str] = (), fonts: Sequence[str] = (),
                  font_link: Sequence[str] = (), audience: Sequence[str] = (),
                  unread: Sequence[str] = (), art: bool = False,
                  composition: str = "", sentence: str = "",
                  nudges: Sequence[str] = ()) -> str:
    """system-report.md: one sentence on what was built, what it was built
    from, the gate result, every note or finding in plain words, and how to
    use the files, the rule pack among them when it was written. No time
    stamps, so the same inputs give the same bytes."""
    scripts = ("Latin and Arabic. Right to left (dir=\"rtl\") switches text to the Arabic face "
               "and type scale." if arabic else "Latin only (built with the Latin-only option).")
    lines = ["# Design system report", "", _opening(brand, gate_line, findings), "",
             *([sentence, ""] if sentence and not findings else []),
             "## Built from", "", f"- Brand color: {brand}", f"- Scripts: {scripts}",
             f"- Axes: {axes_source}.", "", *_axes_table(axes), "",
             "## WCAG gate", "", gate_line, "", _CHECKS_LINE, ""]
    if findings:
        lines += ["## What to change", "", _change(gate_line), "", "## Findings", ""]
        lines += [f"- {_finding_line(f)}" for f in findings]
        return "\n".join(lines) + "\n"
    lines += [_GATE_SCOPE, ""]
    if audience:
        lines += ["## Who it is for", "", _AUDIENCE_LEAD, "", *[f"- {a}" for a in audience], ""]
    if nudges:
        lines += ["## Character nudges", "", _NUDGE_LEAD, "", *[f"- {n}" for n in nudges], ""]
    if unread:
        lines += ["## What the engine did not read", "", _UNREAD_LEAD, "",
                  *[f"- {u}" for u in unread], ""]
    if fidelity:
        lines += ["## Brand color", "", _FIDELITY_LEAD, "", *[f"- {f}" for f in fidelity], ""]
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
    if fonts:
        lines += ["## Fonts", "", _FONTS_LEAD, "", *[f"- {f}" for f in fonts], "",
                  "From Google Fonts: add these tags to the page head, then link fonts.css.",
                  "", *[f"    {tag}" for tag in font_link], "", _FONTS_SELF_HOST, ""]
    if composition:
        lines += ["## Page composition", "", _COMPOSITION_LEAD, "", f"- {composition}", ""]
    if art:
        lines += ["## Brand art", "", _ART_LEAD, "", *[f"- {a}" for a in art_lines()], ""]
    lines += ["## Files", "",
              "- tokens.json: every token in the W3C design tokens format (DTCG 2025.10), with "
              "its values for each mode.",
              f"- tokens.css: CSS custom properties. {_MODES_LINE}",
              "- fonts.css: metric-matched fallback faces; link it before tokens.css, together "
              "with the Google Fonts link or fonts-self-host.css (see Fonts).",
              "- fonts-self-host.css: the faces from your own fonts/ folder, for pages that "
              "do not load them from Google Fonts.",
              "- system-report.md: this report."]
    if art:
        lines.append("- art/: generated brand art, decorative SVG (see Brand art).")
    if rule_pack:
        lines.append(_PACK_LINE)
    return "\n".join(lines) + "\n"


_ROLE_PHRASE = {"fill": "the brand fills the main action",
                "accent": "the brand marks links and accents beside ink actions",
                "edge": "the brand draws edges and rules around ink actions"}


def character_sentence(axes: AxisValues, ts: Any, composition: str,
                       audience: Optional[Audience] = None) -> str:
    """One sentence that says what the system is like: the axes that lean
    clearly one way, the brand's role, the display face and the page
    composition. Read from the built tokens, so it states what was built.
    When the primary script is Arabic and the set has an Arabic display
    face, the page's display type is set in it, so the sentence names it
    first and the Latin display face after it."""
    words = []
    for name, value in axes.to_dict().items():
        _, low, high = _AXIS_WORDS[name]
        if value <= 0.35:
            words.append(low)
        elif value >= 0.65:
            words.append(high)
    lead = _and(words) if words else "balanced on every axis"
    raw = ts.raw("color.action.primary", "scheme:light,contrast:standard")
    link = ts.raw("color.text.link", "scheme:light,contrast:standard")
    role = "fill" if "brand" in raw else ("edge" if "neutral" in link else "accent")
    display = ts.resolve("type.face.display")[0]
    faces = f"{display} sets the display type"
    if audience is not None and audience.primary_script == "arabic" \
            and ts.has("type.face.arabic-display"):
        faces = (f"{ts.resolve('type.face.arabic-display')[0]} sets the Arabic display type and "
                 f"{display} the Latin")
    return (f"Character: {lead}. In this system {_ROLE_PHRASE[role]}, {faces}, and a landing "
            f"page starts from the {composition} composition.")


def make_system(brand: str, axes: AxisValues, axes_source: str, *,
                arabic: bool = True, rule_pack: bool = False,
                audience: Optional[Audience] = None,
                unread: Sequence[str] = (), nudges: Sequence[str] = ()) -> SystemOutput:
    """Build, validate and gate. On success `files` holds every file in FILES
    and ART_FILES, and with rule_pack every rule pack file under
    RULE_PACK_DIR after them;
    on a validation, gate or rule pack failure `files` is empty and
    `findings` names every problem, so a caller can never write a failing
    system."""
    audience = audience or Audience()
    composition = choose_composition(axes, audience)
    notes: Sequence[str] = ()
    fidelity: Sequence[str] = ()
    fonts: Sequence[str] = ()
    font_link: Sequence[str] = ()
    tokens: Dict[str, str] = {}
    art: Dict[str, str] = {}
    pack: Dict[str, str] = {}
    try:
        built = build_system(axes, brand, arabic=arabic, audience=audience)
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
        fidelity = brand_fidelity(built.tokens)
        fonts, font_link = loading_lines(built.tokens), link_tags(built.tokens)
        art = art_files(built.tokens, axes, brand)
        tokens = {"tokens.json": dump_dtcg(built.tokens),
                  "tokens.css": to_css(built.tokens, audience.default_scheme),
                  "fonts.css": fonts_css(built.tokens),
                  "fonts-self-host.css": self_host_css(built.tokens)}
        if rule_pack:
            from engine.rulepack.generate import RulePackError, build_rule_pack
            try:
                pack = build_rule_pack(built.tokens)
            except RulePackError as exc:
                findings = tuple(SystemFinding(RULE_PACK_DIR, "", p) for p in exc.problems)
                n = len(findings)
                gate = (f"{gate} {_RULE_PACK}: {n} problem{'' if n == 1 else 's'} between its "
                        "guidance, contracts or records and these tokens.")
                notes, tokens, fidelity, fonts, art = (), {}, (), (), {}
    report = render_report(brand, axes, axes_source, arabic, gate, notes, findings,
                           rule_pack=bool(pack), fidelity=fidelity, fonts=fonts,
                           font_link=font_link,
                           audience=[e.line() for e in effects(audience, axes)], unread=unread,
                           art=bool(art), composition=composition.line() if tokens else "",
                           sentence=character_sentence(axes, built.tokens, composition.name,
                                                       audience)
                           if tokens else "", nudges=nudges)
    files = {**tokens, "system-report.md": report, **art, **pack} if tokens else {}
    return SystemOutput(passed=bool(tokens), files=files, report=report, gate=gate,
                        findings=findings, brand=brand, axes=axes, axes_source=axes_source,
                        arabic=arabic, audience=audience, unread=tuple(unread),
                        composition=composition.to_dict())


def failure_text(output: SystemOutput) -> str:
    """What a caller shows a person when nothing was built: the report's
    opening sentence, its guidance on what to change and every finding, in
    the report's own words. Empty for a system that passed."""
    if output.passed:
        return ""
    lines = [_opening(output.brand, output.gate, output.findings), "",
             "What to change", _change(output.gate), "", "Findings"]
    lines += [f"- {_finding_line(f)}" for f in output.findings]
    return "\n".join(lines) + "\n"


def failure_message(output: SystemOutput) -> str:
    """One line for a caller's result: nothing was written, and which
    inputs to change. Empty for a system that passed."""
    if output.passed:
        return ""
    n = len(output.findings)
    if _RULE_PACK in output.gate:
        return (f"Nothing was written: the tokens passed the WCAG gate, but the rule pack found "
                f"{n} problem{'' if n == 1 else 's'}, which no brand color or axes should cause. "
                "Build again without the rule pack to get the tokens, and report the findings.")
    if output.gate.startswith(_VALIDATION):
        return (f"Nothing was written: the generated tokens broke {n} structural "
                f"rule{'' if n == 1 else 's'}, which no brand color or axes should cause. Build "
                "again with the same inputs, and if it fails again, report it with the brand "
                "color, the axes and the findings.")
    return (f"Nothing was written: the WCAG gate found {n} problem{'' if n == 1 else 's'} with "
            "these inputs. Change the brand color (a darker or more saturated one gives the "
            "engine more room to reach every contrast minimum), the axes or the brief, and "
            "build again. The findings name each pairing that fell short.")


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
    if out_dir is not None and not isinstance(out_dir, (str, os.PathLike)):
        raise InputError(f"{label} is {out_dir!r}; pass the folder to write the system into "
                         "as text, for example design-system")
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


def _blocked_folder(out_dir: Path, name: str) -> Optional[Path]:
    """For a name inside subfolders (rule-pack/color/audit.md), the first
    of those subfolders that exists as something other than a folder."""
    folder = out_dir
    for part in Path(name).parts[:-1]:
        folder = folder / part
        if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
            return folder
    return None


def plan_writes(out_dir: Path, files: Mapping[str, str]) -> WritePlan:
    """Compare each file with what is on disk, without writing. A link in
    place of a file is never written through or replaced: an identical one
    is left alone, any other is refused. A name may sit in subfolders; a
    file or link where one of them should be is named."""
    write: List[str] = []
    unchanged: List[str] = []
    conflicts: List[str] = []
    for name, text in files.items():
        target = out_dir / name
        data = text.encode("utf-8")
        try:
            blocked = _blocked_folder(out_dir, name)
            if blocked is not None:
                raise InputError(f"{blocked} is a file or a link where a folder should be, so "
                                 f"{name} cannot be written; move it away or write the system "
                                 "into a different folder")
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
    """Write one file into the staging folder, making its subfolders."""
    path.parent.mkdir(parents=True, exist_ok=True)
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


def _restore(out_dir: Path, placed: Sequence[Tuple[str, Optional[Path]]]) -> List[str]:
    """Undo the moves so far: put each previous file back and remove each
    new one. A name is recorded before its old copy is set aside, so an old
    copy that is missing was never moved and its file is still in place.
    Returns what could not be undone, one phrase per file."""
    left: List[str] = []
    for name, previous in reversed(placed):
        target = out_dir / name
        try:
            if previous is not None:
                if previous.exists():
                    os.replace(str(previous), str(target))
            elif target.exists():
                target.unlink()
        except OSError:
            left.append(f"the old {name} is at {previous}" if previous is not None
                        else f"the new {target} could not be removed")
    return left


def write_files(out_dir: Path, files: Mapping[str, str], *, force: bool = False) -> WritePlan:
    """Write the files that are new or, when forced, different. Without
    force, one conflicting file stops every write. Identical files are
    never rewritten. All or nothing: every file is staged in a folder
    inside out_dir and then moved into place, and a failure at any step,
    an interrupt included, puts the folder back as it was before it goes
    on, so the folder never holds a mix of two systems. Returns the plan
    it acted on; `conflicts` is non-empty only when nothing was written.
    Every filesystem error is an InputError naming the path and the fix;
    any other exception is raised as it was, once the folder is back."""
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
    except BaseException as exc:
        _remove_folders(made)
        if not isinstance(exc, OSError):
            raise
        raise InputError(f"{out_dir} cannot be written ({_reason(exc)}), so nothing in it was "
                         "changed; pass a folder you can write to") from None
    placed: List[Tuple[str, Optional[Path]]] = []
    inner: List[Path] = []
    name = names[0]
    try:
        for name in names:
            _stage(stage / name, files[name].encode("utf-8"))
        for name in names:
            previous = stage / f"{name}.previous" if name in plan.conflicts else None
            placed.append((name, previous))
            if previous is not None:
                os.replace(str(out_dir / name), str(previous))
            folder = (out_dir / name).parent
            if not folder.exists():
                inner[:0] = _missing_folders(folder)
                folder.mkdir(parents=True)
            _place(stage / name, out_dir / name)
    except BaseException as exc:
        # Any failure, an interrupt included, puts the folder back first.
        reason = _reason(exc) if isinstance(exc, OSError) else (
            "interrupted" if isinstance(exc, KeyboardInterrupt) else type(exc).__name__)
        left = _restore(out_dir, placed)
        _remove_folders(inner)
        if left:
            # The staging folder holds the old copies, so it stays; the
            # person needs each path whatever stopped the write.
            steps = []
            if any(p.startswith("the old ") for p in left):
                steps.append(f"move each old copy back into {out_dir}")
            if any(p.startswith("the new ") for p in left):
                steps.append("remove each new file named")
            undo = _and(steps)
            raise InputError(f"{out_dir / name} could not be written ({reason}), and "
                             f"{len(left)} file{'' if len(left) == 1 else 's'} could not be put "
                             f"back: {'; '.join(left)}. To undo the write, {undo}, then pass a "
                             "folder you can write to") from exc
        shutil.rmtree(str(stage), ignore_errors=True)
        _remove_folders(made)
        if not isinstance(exc, OSError):
            raise
        raise InputError(f"{out_dir / name} could not be written ({reason}), so nothing "
                         f"in {out_dir} was changed; free some space or pass a folder you can "
                         "write to") from None
    shutil.rmtree(str(stage), ignore_errors=True)
    return WritePlan(names, plan.unchanged, ())


def tokens_digest(tokens_json: str) -> str:
    """The sha256 of tokens.json as the writer puts it on disk."""
    return hashlib.sha256(tokens_json.encode("utf-8")).hexdigest()


def _pack_mismatch(folder: Path, tokens_json: str) -> Optional[str]:
    """Why the rule pack in `folder` cannot be matched to this tokens.json,
    or None when its manifest names exactly this file."""
    manifest = folder / RULE_PACK_MANIFEST
    if not manifest.is_file():
        return f"it has no {RULE_PACK_MANIFEST}"
    try:
        recorded = json.loads(manifest.read_text(encoding="utf-8"))["tokens.json"]["sha256"]
    except (OSError, ValueError, KeyError, TypeError):
        return f"its {RULE_PACK_MANIFEST} cannot be read"
    if recorded != tokens_digest(tokens_json):
        return f"its {RULE_PACK_MANIFEST} names another tokens.json"
    return None


def note_rule_pack(system: SystemOutput, out_dir: Path, *,
                    force: bool = False) -> SystemOutput:
    """For a build that does not write the rule pack into an out_dir that
    holds one: a pack built from this tokens.json is listed in the report
    as if it had been written, so the report describes the folder and a
    rebuild without the flag leaves it unchanged. A pack built from other
    tokens (or with no readable digest) is named as stale in the report,
    when the write will go ahead. The pack itself is never touched. Any
    other system is returned as it is."""
    if not system.passed or f"{RULE_PACK_DIR}/README.md" in system.files:
        return system
    folder = out_dir / RULE_PACK_DIR
    if not folder.is_dir():
        return system
    reason = _pack_mismatch(folder, system.files["tokens.json"])
    if reason is None:
        report = system.report + _PACK_LINE + "\n"
        return replace(system, files={**system.files, "system-report.md": report},
                       report=report)
    report = system.report + "\n".join([
        "", "## Rule pack", "",
        f"The {RULE_PACK_DIR}/ folder beside these files cannot be matched to this tokens.json "
        f"({reason}), so its values, pairings and rules may describe another system. It was "
        f"left as it is. Build again with uxskill system build --rule-pack --force to write a "
        f"pack for these tokens, or remove {RULE_PACK_DIR}/."]) + "\n"
    noted = replace(system, files={**system.files, "system-report.md": report}, report=report,
                    stale_rule_pack=str(folder), stale_reason=reason)
    # A refused write changes nothing, so the pack still matches the files
    # on disk; name it only when these files will be written or are there.
    try:
        plan = plan_writes(out_dir, noted.files)
    except InputError:
        return system
    return system if plan.conflicts and not force else noted


def write_outcome(system: SystemOutput, out_dir: Path, *, force: bool = False,
                  force_label: str = "--force", out_label: str = "--out") -> Dict[str, Any]:
    """Write a built system into out_dir and say what happened, in the
    fields both callers report: status (a key of STATUS_EXIT), written,
    unchanged, conflicts and message. A failed system writes nothing. The
    labels name the force and out inputs the way the caller's person types
    them, in the refusal message."""
    stale, reason = system.stale_rule_pack, system.stale_reason

    def outcome(status: str, written: Sequence[str] = (), unchanged: Sequence[str] = (),
                conflicts: Sequence[str] = (), message: str = "") -> Dict[str, Any]:
        named = stale if status in ("written", "unchanged") else None
        if named:
            message += (f" {named} holds a rule pack that cannot be matched to this tokens.json "
                        f"({reason}); it was left as it is. Build again with uxskill system "
                        f"build --rule-pack --force to replace it, or remove {named}.")
        return {"status": status, "written": list(written), "unchanged": list(unchanged),
                "conflicts": list(conflicts), "message": message, "stale_rule_pack": named}

    if not system.passed:
        return outcome("failed", message=failure_message(system))
    try:
        plan = write_files(out_dir, system.files, force=force)
    except InputError as exc:
        # The inputs were fine; the folder could not be written. Nothing in
        # it changed, so this is a run that wrote nothing.
        return outcome("error", message=str(exc))
    if plan.conflicts:
        # Refused: the plan's would-be writes did not happen.
        return outcome("refused", unchanged=plan.unchanged, conflicts=plan.conflicts,
                       message=conflict_message(out_dir, plan, force_label, out_label))
    if plan.write:
        return outcome("written", written=plan.write, unchanged=plan.unchanged,
                       message=f"Wrote {', '.join(plan.write)} to {out_dir}.")
    return outcome("unchanged", unchanged=plan.unchanged,
                   message=f"{out_dir} already holds this system; nothing changed.")
