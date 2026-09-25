"""Token values per type: what a literal must look like, how it travels
to DTCG 2025.10 and back, and how it prints as CSS.

Internal representation, one rule for every type: a literal is plain JSON
data (dict, list, str, int, float, bool) equal to the token's DTCG 2025.10
$value, except color. A color is held as its sRGB hex string, #RRGGBB or
#RRGGBBAA when translucent, because color math, the contrast gate and CSS
all read sRGB hex; the codec below turns it into the 2025.10 color object
(colorSpace srgb, components 0 to 1, alpha only when below 1, hex
fallback) and back without loss. An opaque color is never held with an
alpha: #RRGGBBFF and an alpha of 1 both become #RRGGBB. Inside a composite (a shadow layer's
color, a typography field) the same rule applies field by field, and any
field may instead be an alias such as "{color.base.black}".
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Callable, Dict, List, Mapping, Tuple

from engine.foundations.tokens import alias_target, css_property, is_alias, opaque_hex

_HEX = re.compile(r"#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}|[0-9A-Fa-f]{8})")
_FONT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9 _-]*")
GENERIC_FAMILIES = ("serif", "sans-serif", "monospace", "cursive", "fantasy", "system-ui",
                    "ui-serif", "ui-sans-serif", "ui-monospace", "ui-rounded", "math", "emoji")
STROKE_STYLES = ("solid", "dashed", "dotted", "double", "groove", "ridge", "outset", "inset")
SHADOW_KEYS = ("color", "offsetX", "offsetY", "blur", "spread")
# DTCG typography field -> (the token type that field holds, its CSS property)
TYPOGRAPHY_FIELDS: Mapping[str, Tuple[str, str]] = MappingProxyType({
    "fontFamily": ("fontFamily", "font-family"),
    "fontSize": ("dimension", "font-size"),
    "fontWeight": ("fontWeight", "font-weight"),
    "letterSpacing": ("dimension", "letter-spacing"),
    "lineHeight": ("number", "line-height"),
})


def _is_number(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def _num(v: float) -> str:
    """A number as CSS writes it, to four decimals: 16, 0.5, -0.25. Never
    16.0, 1e-05, a trailing dot or a signed zero."""
    if isinstance(v, int):
        return str(v)
    r = round(float(v), 4)
    if r == 0:
        return "0"
    return f"{r:.4f}".rstrip("0").rstrip(".")


def _alias_css(value: str) -> str:
    return f"var({css_property(alias_target(value))})"


# color

def _color_ok(v: Any) -> bool:
    return isinstance(v, str) and _HEX.fullmatch(v) is not None


def _color_encode(v: str) -> Dict[str, Any]:
    s = v[1:]
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    rgb = [int(s[i:i + 2], 16) for i in (0, 2, 4)]
    out: Dict[str, Any] = {"colorSpace": "srgb",
                           "components": [round(c / 255, 6) for c in rgb]}
    if len(s) == 8 and s[6:8].upper() != "FF":
        out["alpha"] = round(int(s[6:8], 16) / 255, 6)
    out["hex"] = "#" + s[:6].upper()
    return out


def _color_decode(v: Any) -> Any:
    if isinstance(v, str) and _HEX.fullmatch(v):
        return opaque_hex(v.upper())  # a pre-2025.10 hex string, accepted on import
    if not (isinstance(v, dict) and v.get("colorSpace") == "srgb"):
        return v  # left as is; validate reports it as a bad value
    comps = v.get("components")
    if isinstance(v.get("hex"), str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", v["hex"]):
        base = v["hex"].upper()
    elif isinstance(comps, list) and len(comps) == 3 and all(_is_number(c) for c in comps):
        base = "#" + "".join(f"{max(0, min(255, round(c * 255))):02X}" for c in comps)
    else:
        return v
    if "alpha" in v:
        if not _is_number(v["alpha"]):
            return v
        alpha = max(0, min(255, round(v["alpha"] * 255)))
        return base if alpha == 255 else base + f"{alpha:02X}"
    return base


# dimension and duration

def _unit_ok(units: Tuple[str, ...]) -> Callable[[Any], bool]:
    def ok(v: Any) -> bool:
        return (isinstance(v, dict) and set(v) == {"value", "unit"}
                and _is_number(v["value"]) and v["unit"] in units)
    return ok


def _unit_css(v: Dict[str, Any]) -> str:
    return f"{_num(v['value'])}{v['unit']}"


# Checks compare dimensions in px and durations in ms, whatever unit a set
# writes them in: a rem is read at the browser default of 16px.
REM_PX = 16


def dimension_px(v: Dict[str, Any]) -> float:
    """A dimension literal in px."""
    return v["value"] * (REM_PX if v["unit"] == "rem" else 1)


def duration_ms(v: Dict[str, Any]) -> float:
    """A duration literal in ms."""
    return v["value"] * (1000 if v["unit"] == "s" else 1)


# cubicBezier, fontFamily, fontWeight, number, strokeStyle

def _bezier_ok(v: Any) -> bool:
    return (isinstance(v, list) and len(v) == 4 and all(_is_number(c) for c in v)
            and 0 <= v[0] <= 1 and 0 <= v[2] <= 1)


def _family_ok(v: Any) -> bool:
    names = v if isinstance(v, list) else [v]
    return bool(names) and all(isinstance(n, str) and _FONT_NAME.fullmatch(n) for n in names)


def _family_css(v: Any) -> str:
    names = v if isinstance(v, list) else [v]
    return ", ".join(n if n in GENERIC_FAMILIES else f'"{n}"' for n in names)


def _weight_ok(v: Any) -> bool:
    return _is_number(v) and 1 <= v <= 1000


def _stroke_ok(v: Any) -> bool:
    return isinstance(v, str) and v in STROKE_STYLES


# shadow

def _layers(v: Any) -> List[Any]:
    return v if isinstance(v, list) else [v]


def _shadow_ok(v: Any) -> bool:
    layers = _layers(v)
    if not layers:
        return False
    dim = _unit_ok(("px", "rem"))
    for layer in layers:
        if not isinstance(layer, dict) or not set(SHADOW_KEYS) <= set(layer) \
                or not set(layer) <= set(SHADOW_KEYS) | {"inset"}:
            return False
        if not (is_alias(layer["color"]) or _color_ok(layer["color"])):
            return False
        if any(not (is_alias(layer[k]) or dim(layer[k])) for k in SHADOW_KEYS[1:]):
            return False
        if not isinstance(layer.get("inset", False), bool):
            return False
    return True


def _map_layer_colors(v: Any, fn: Callable[[Any], Any]) -> Any:
    out = []
    for layer in _layers(v):
        layer = dict(layer) if isinstance(layer, dict) else layer
        if isinstance(layer, dict) and "color" in layer and not is_alias(layer["color"]):
            layer["color"] = fn(layer["color"])
        out.append(layer)
    return out if isinstance(v, list) else out[0]


def _shadow_css(v: Any) -> str:
    def part(x: Any) -> str:
        return _alias_css(x) if is_alias(x) else (_unit_css(x) if isinstance(x, dict) else x)
    return ", ".join(
        ("inset " if layer.get("inset") else "")
        + " ".join(part(layer[k]) for k in ("offsetX", "offsetY", "blur", "spread"))
        + " " + part(layer["color"])
        for layer in _layers(v))


# typography

def _typography_ok(v: Any) -> bool:
    if not isinstance(v, dict) or set(v) != set(TYPOGRAPHY_FIELDS):
        return False
    return all(is_alias(v[k]) or TYPES[t].check(v[k]) for k, (t, _) in TYPOGRAPHY_FIELDS.items())


@dataclass(frozen=True)
class TypeSpec:
    """One token type: `check` accepts a literal, `expected` is the fix
    quoted when it does not, `encode` and `decode` convert to and from the
    DTCG 2025.10 $value, `css` prints a literal (aliases print as var())."""
    check: Callable[[Any], bool]
    expected: str
    encode: Callable[[Any], Any]
    decode: Callable[[Any], Any]
    css: Callable[[Any], str]


def _same(v: Any) -> Any:
    return v


TYPES: Mapping[str, TypeSpec] = MappingProxyType({
    "color": TypeSpec(_color_ok, "use #RRGGBB or #RGB, or #RRGGBBAA when translucent, "
                      "for example #3366FF",
                      _color_encode, _color_decode, str),
    "dimension": TypeSpec(_unit_ok(("px", "rem")),
                          'use {"value": <number>, "unit": "px" or "rem"}, for example '
                          '{"value": 16, "unit": "px"}', _same, _same, _unit_css),
    "duration": TypeSpec(_unit_ok(("ms", "s")),
                         'use {"value": <number>, "unit": "ms" or "s"}, for example '
                         '{"value": 200, "unit": "ms"}', _same, _same, _unit_css),
    "cubicBezier": TypeSpec(_bezier_ok, "use four numbers [x1, y1, x2, y2] with x1 and x2 "
                            "from 0 to 1, for example [0.2, 0, 0, 1]", _same, _same,
                            lambda v: "cubic-bezier(" + ", ".join(_num(c) for c in v) + ")"),
    "fontFamily": TypeSpec(_family_ok, "use a font name or a list of names made of letters, "
                           "digits, spaces, '_' and '-', for example [\"Source Sans 3\", "
                           "\"sans-serif\"]", _same, _same, _family_css),
    "fontWeight": TypeSpec(_weight_ok, "use a number from 1 to 1000, for example 600",
                           _same, _same, _num),
    "number": TypeSpec(_is_number, "use a finite number, for example 1.5", _same, _same, _num),
    "strokeStyle": TypeSpec(_stroke_ok, f"use one of {list(STROKE_STYLES)}", _same, _same, str),
    "shadow": TypeSpec(_shadow_ok, "use a list of layers, each with color, offsetX, offsetY, "
                       "blur and spread (dimensions or aliases) and an optional boolean inset",
                       lambda v: _map_layer_colors(v, _color_encode),
                       lambda v: _map_layer_colors(v, _color_decode), _shadow_css),
    "typography": TypeSpec(_typography_ok, "use an object with exactly fontFamily, fontSize, "
                           "fontWeight, letterSpacing and lineHeight, each a literal of its "
                           "type or an alias", _same, _same,
                           lambda v: ""),  # expanded field by field, see css_entries
})


class EncodeError(ValueError):
    """A value that fails its type check reached encode. The message names
    the token, the value and the fix, as validate's bad-value does."""


def encode(type_: str, value: Any, path: str = "") -> Any:
    """Internal literal or alias to its DTCG 2025.10 $value. A literal that
    fails its type check raises EncodeError naming `path`, never a value
    the codec half read (so a bad color cannot leave as another color).
    An unknown type passes through; validate names it."""
    if is_alias(value) or type_ not in TYPES:
        return value
    spec = TYPES[type_]
    if not spec.check(value):
        raise EncodeError(f"{path or 'a token'} is type {type_} but holds {value!r}; "
                          f"{spec.expected}")
    return spec.encode(value)


def decode(type_: str, value: Any) -> Any:
    """DTCG 2025.10 $value to the internal literal. A value the codec cannot
    read comes back unchanged, so validate can name it."""
    if is_alias(value) or type_ not in TYPES:
        return value
    return TYPES[type_].decode(value)


def css_entries(path: str, type_: str, value: Any) -> List[Tuple[str, str]]:
    """The CSS custom properties one token value becomes. A typography
    composite expands into one property per field; everything else is one
    property. Aliases, whole or per field, print as var()."""
    prop = css_property(path)
    if is_alias(value):
        if type_ == "typography":
            return [(f"{prop}-{css}", f"var({css_property(alias_target(value))}-{css})")
                    for _, css in TYPOGRAPHY_FIELDS.values()]
        return [(prop, _alias_css(value))]
    if type_ == "typography":
        return [(f"{prop}-{css}", _alias_css(value[k]) if is_alias(value[k]) else TYPES[t].css(value[k]))
                for k, (t, css) in TYPOGRAPHY_FIELDS.items()]
    return [(prop, TYPES[type_].css(value))]


def css_names(path: str, type_: str) -> List[str]:
    """The property names css_entries gives a token of this type."""
    prop = css_property(path)
    if type_ == "typography":
        return [f"{prop}-{css}" for _, css in TYPOGRAPHY_FIELDS.values()]
    return [prop]
