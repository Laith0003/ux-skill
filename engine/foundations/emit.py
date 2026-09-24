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
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple

from engine.foundations.color_math import hex_to_rgb, rgb_to_hex
from engine.synthesizer.axes import AXIS_NAMES, AxisValues, compute_axes

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
