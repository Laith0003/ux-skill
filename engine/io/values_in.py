"""Read one value written as text (a CSS custom property, a Tailwind theme
value, a cell of a markdown table) into a token type and the engine's
internal literal (engine.foundations.values).

The reader decides a type from the text alone and only when the text
leaves one reading: #3366FF is a color, 16px a dimension, 200ms a
duration, a quoted name or a list ending in a generic family a font
family. Text with more than one reading (a bare word such as Inter), a
value the browser computes (calc(), color-mix()), a unit relative to
something outside the token (em, %, vw) and a color space it does not
convert raise NotRead with the reason and the fix. Nothing is guessed.
"""
from __future__ import annotations

import re
from typing import Any, List, Optional, Tuple

from engine.foundations.color_math import _oklch_to_linear, oklch_to_hex, rgb_to_hex
from engine.foundations.values import GENERIC_FAMILIES, STROKE_STYLES


class NotRead(ValueError):
    """A value the reader cannot read for certain. The message says why and
    how to write it so it can."""


_NUMBER = r"[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?"
_NUM = re.compile(_NUMBER + r"$", re.I)
_UNIT = re.compile(r"(" + _NUMBER + r")([a-z%]+)$", re.I)
_HEX = re.compile(r"#([0-9a-f]{3,8})$", re.I)
_FUNC = re.compile(r"([a-z-]+)\((.*)\)$", re.I | re.S)
_VAR = re.compile(r"var\(\s*--([A-Za-z0-9_-]+)\s*(?:,\s*(.*?))?\s*\)$", re.S)

# The curves CSS defines for its easing keywords.
EASING_KEYWORDS = {
    "linear": [0, 0, 1, 1], "ease": [0.25, 0.1, 0.25, 1], "ease-in": [0.42, 0, 1, 1],
    "ease-out": [0, 0, 0.58, 1], "ease-in-out": [0.42, 0, 0.58, 1],
}
# The three color keywords read as colors; any other bare word is ambiguous.
COLOR_KEYWORDS = {"white": "#FFFFFF", "black": "#000000", "transparent": "#00000000"}
_RELATIVE = {"em": "the parent's font size", "%": "its container", "vw": "the viewport",
             "vh": "the viewport", "vmin": "the viewport", "vmax": "the viewport",
             "ch": "the font", "ex": "the font", "lh": "the line height",
             "svh": "the viewport", "dvh": "the viewport", "lvh": "the viewport"}
_COMPUTED = ("calc", "min", "max", "clamp", "color-mix", "light-dark", "env", "attr")
_OTHER_SPACES = ("lab", "lch", "oklab", "hwb", "color")


def _number(text: str) -> float:
    value = float(text)
    return int(value) if value == int(value) and "." not in text and "e" not in text.lower() \
        else value


def split_top(text: str, sep: str = ",") -> List[str]:
    """Split on `sep` outside parentheses and quotes, trimming each part."""
    parts, depth, quote, start = [], 0, "", 0
    for i, ch in enumerate(text):
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and (ch == sep if sep != " " else ch.isspace()):
            parts.append(text[start:i].strip())
            start = i + 1
    parts.append(text[start:].strip())
    return [p for p in parts if p] if sep == " " else parts


def css_alias(text: str) -> Optional[Tuple[str, str]]:
    """(name, fallback) for a value that is one var(--name) reference, or
    None when it is not a reference. A value mixing a reference with
    anything else raises NotRead."""
    text = text.strip()
    m = _VAR.match(text)
    if m:
        return m.group(1), (m.group(2) or "").strip()
    if "var(" in text:
        raise NotRead(f"{text} joins several values with var(); split it into one token per "
                      "value")
    return None


def _hex(text: str) -> str:
    digits = _HEX.match(text).group(1)
    if len(digits) in (3, 4):
        digits = "".join(c * 2 for c in digits)
    if len(digits) not in (6, 8):
        raise NotRead(f"{text} is not a hex color; use #RGB, #RGBA, #RRGGBB or #RRGGBBAA")
    digits = digits.upper()
    return "#" + (digits[:6] if digits[6:] == "FF" else digits)


def _alpha_hex(alpha: float) -> str:
    return "" if alpha >= 1 else f"{max(0, min(255, round(alpha * 255))):02X}"


def _channel(part: str, scale: float) -> float:
    """One channel: a number on `scale`, or a percentage of it."""
    if part.endswith("%"):
        return float(part[:-1]) / 100 * scale
    return float(part)


def _args(text: str, name: str, body: str) -> Tuple[List[str], Optional[str]]:
    """A color function's channels and its alpha (or None), in either the
    comma or the space syntax."""
    if "," in body:
        parts = [p.strip() for p in body.split(",")]
        alpha = parts[3] if len(parts) == 4 else None
        channels = parts[:3] if len(parts) in (3, 4) else parts
    else:
        main, _, alpha_text = body.partition("/")
        channels = main.split()
        alpha = alpha_text.strip() or None
    if len(channels) != 3:
        raise NotRead(f"{text} needs three channels; write it as {name}(r g b) or "
                      f"{name}(r g b / a)")
    return channels, alpha


def _alpha(text: Optional[str]) -> float:
    if text is None:
        return 1.0
    return float(text[:-1]) / 100 if text.endswith("%") else float(text)


def _hsl_to_rgb(h: float, s: float, lightness: float) -> Tuple[float, float, float]:
    c = (1 - abs(2 * lightness - 1)) * s
    hp = (h % 360) / 60
    x = c * (1 - abs(hp % 2 - 1))
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(hp) % 6]
    m = lightness - c / 2
    return tuple((v + m) * 255 for v in (r, g, b))


def _color_function(text: str, name: str, body: str) -> str:
    name = name.lower()
    try:
        channels, alpha_text = _args(text, name, body)
        alpha = _alpha(alpha_text)
        if name in ("rgb", "rgba"):
            rgb = tuple(_channel(c, 255) for c in channels)
        elif name in ("hsl", "hsla"):
            # CSS Color 4: a unitless saturation or lightness is a percentage.
            hue = float(channels[0].rstrip("deg"))
            sat, light = (float(c[:-1] if c.endswith("%") else c) / 100 for c in channels[1:])
            rgb = _hsl_to_rgb(hue, sat, light)
        else:  # oklch
            lightness = _channel(channels[0], 1)
            chroma = _channel(channels[1], 0.4)
            hue = float(channels[2].rstrip("deg")) if channels[2] != "none" else 0.0
            linear = _oklch_to_linear(lightness, chroma, hue)
            if any(c < -1e-4 or c > 1 + 1e-4 for c in linear):
                raise NotRead(f"{text} is outside the sRGB range this engine measures; write "
                              "the sRGB color you want as hex")
            # The one OKLCH conversion the engine has, which `system detect`
            # (engine.existing) uses too, so both read a color the same way.
            return oklch_to_hex(lightness, chroma, hue) + _alpha_hex(alpha)
    except ValueError as exc:
        if isinstance(exc, NotRead):
            raise
        raise NotRead(f"{text} has a channel that is not a number; write it as hex") from None
    return rgb_to_hex(rgb) + _alpha_hex(alpha)


def _font_names(text: str) -> Optional[List[str]]:
    """A font list when the text can only be one: quoted names, or a comma
    list, or a single generic family."""
    parts = split_top(text)
    quoted = any(p[:1] in "\"'" for p in parts)
    if len(parts) == 1 and not quoted and parts[0] not in GENERIC_FAMILIES:
        return None
    names = []
    for p in parts:
        if p[:1] in "\"'" and p[-1:] == p[:1]:
            names.append(p[1:-1])
        elif re.fullmatch(r"[A-Za-z][A-Za-z0-9 _-]*", p):
            names.append(p)
        else:
            return None
    return names


def _shadow_layer(text: str) -> dict:
    words = split_top(text, " ")
    inset = "inset" in (w.lower() for w in words)
    words = [w for w in words if w.lower() != "inset"]
    lengths, color = [], None
    for w in words:
        m = _UNIT.match(w)
        if w == "0" or (m and m.group(2).lower() in ("px", "rem")):
            lengths.append({"value": _number(m.group(1)) if m else 0,
                            "unit": m.group(2).lower() if m else "px"})
        elif color is None:
            kind, value = read_value(w)
            if kind != "color":
                raise NotRead(f"{text} is not a shadow layer; write x, y, blur, spread and a "
                              "color")
            color = value
        else:
            raise NotRead(f"{text} is not a shadow layer; write x, y, blur, spread and a color")
    if color is None or not 2 <= len(lengths) <= 4:
        raise NotRead(f"{text} is not a shadow layer; write x, y, blur, spread and a color")
    zero = {"value": 0, "unit": "px"}
    lengths += [zero] * (4 - len(lengths))
    layer = {"color": color, "offsetX": lengths[0], "offsetY": lengths[1], "blur": lengths[2],
             "spread": lengths[3]}
    if inset:
        layer["inset"] = True
    return layer


def read_value(text: Any) -> Tuple[str, Any]:
    """(token type, internal literal) for a value written as text. Raises
    NotRead with the reason and the fix when the text has no single
    reading. A var() reference is not a value; read it with css_alias."""
    if not isinstance(text, str):
        text = str(text)
    text = text.strip().rstrip(";").strip()
    if not text:
        raise NotRead("the value is empty")
    lower = text.lower()
    if _HEX.match(text):
        return "color", _hex(text)
    if lower in COLOR_KEYWORDS:
        return "color", COLOR_KEYWORDS[lower]
    if lower in EASING_KEYWORDS:
        return "cubicBezier", list(EASING_KEYWORDS[lower])
    if lower in STROKE_STYLES:
        return "strokeStyle", lower
    if _NUM.match(text):
        return "number", _number(text)
    m = _UNIT.match(text)
    if m:
        value, unit = _number(m.group(1)), m.group(2).lower()
        if unit in ("px", "rem"):
            return "dimension", {"value": value, "unit": unit}
        if unit in ("ms", "s"):
            return "duration", {"value": value, "unit": unit}
        if unit in _RELATIVE:
            raise NotRead(f"{text} is relative to {_RELATIVE[unit]}, so it has no fixed value; "
                          "write it in px or rem")
        raise NotRead(f"{text} has the unit {unit}, which this reader does not convert; write "
                      "it in px, rem, ms or s")
    f = _FUNC.match(text)
    if f and "," not in text.split("(", 1)[0] and len(split_top(text)) == 1 \
            and len(split_top(text, " ")) == 1:
        name, body = f.group(1).lower(), f.group(2)
        if name in _COMPUTED:
            raise NotRead(f"{text} is computed by the browser; write the value it computes to")
        if name in ("rgb", "rgba", "hsl", "hsla", "oklch"):
            return "color", _color_function(text, name, body)
        if name in _OTHER_SPACES:
            raise NotRead(f"{text} is in a color space this reader does not convert; write it "
                          "as hex or oklch()")
        if name == "cubic-bezier":
            try:
                curve = [_number(p.strip()) for p in body.split(",")]
            except ValueError:
                curve = []
            if len(curve) != 4:
                raise NotRead(f"{text} needs four numbers; write cubic-bezier(x1, y1, x2, y2)")
            if not (0 <= curve[0] <= 1 and 0 <= curve[2] <= 1):
                raise NotRead(f"{text} has an x outside 0 to 1; x1 and x2 must sit from 0 to 1")
            return "cubicBezier", curve
        raise NotRead(f"{text} uses {name}(), which this reader does not read; write a plain "
                      "value")
    names = _font_names(text)
    if names is not None:
        return "fontFamily", names
    layers = split_top(text)
    if any(ch.isdigit() for ch in text) and all(len(split_top(p, " ")) >= 3 for p in layers):
        return "shadow", [_shadow_layer(p) for p in layers]
    if re.fullmatch(r"[A-Za-z][A-Za-z-]*", text):
        raise NotRead(f"{text} is a single word that could be a color name, a font name or a "
                      "keyword; write a color as hex, and quote a font name")
    raise NotRead(f"{text} is not a value this reader knows; write a hex color, a length in px "
                  "or rem, a duration in ms or s, a number, a curve or a quoted font list")
