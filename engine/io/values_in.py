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

An oklch() or oklab() color outside sRGB is never refused: it is mapped
into sRGB by CSS Color 4 gamut mapping, keeping its lightness and hue, and
reported as a GamutMapped with the OKLab distance it moved.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple

from engine.foundations.color_math import gamut_map_oklch, oklab_to_oklch, rgb_to_hex
from engine.foundations.values import GENERIC_FAMILIES, STROKE_STYLES


class NotRead(ValueError):
    """A value the reader cannot read for certain. The message says why and
    how to write it so it can."""


@dataclass(frozen=True)
class GamutMapped:
    """An oklch() or oklab() color outside sRGB, as written, the hex it was
    read as, and the OKLab distance between the two."""
    original: str
    hex: str
    distance: float


_NUMBER = r"[+-]?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?"
_NUM = re.compile(_NUMBER + r"$", re.I)
_UNIT = re.compile(r"(" + _NUMBER + r")([a-z%]+)$", re.I)
_HEX = re.compile(r"#([0-9a-f]{3,8})$", re.I)
_FUNC = re.compile(r"([a-z-]+)\((.*)\)$", re.I | re.S)
_VAR_HEAD = re.compile(r"var\(\s*--([A-Za-z0-9_-]+)\s*")

# The curves CSS defines for its easing keywords.
EASING_KEYWORDS = {
    "linear": [0, 0, 1, 1], "ease": [0.25, 0.1, 0.25, 1], "ease-in": [0.42, 0, 1, 1],
    "ease-out": [0, 0, 0.58, 1], "ease-in-out": [0.42, 0, 0.58, 1],
}
# CSS keywords that take a value from elsewhere: none of them is a value.
CSS_KEYWORDS = ("inherit", "initial", "unset", "revert", "revert-layer", "currentcolor", "auto",
                "none")
# The three color keywords read as colors; any other bare word is ambiguous.
COLOR_KEYWORDS = {"white": "#FFFFFF", "black": "#000000", "transparent": "#00000000"}
_RELATIVE = {"em": "the parent's font size", "%": "its container", "vw": "the viewport",
             "vh": "the viewport", "vmin": "the viewport", "vmax": "the viewport",
             "ch": "the font", "ex": "the font", "lh": "the line height",
             "svh": "the viewport", "dvh": "the viewport", "lvh": "the viewport"}
_COMPUTED = ("calc", "min", "max", "clamp", "color-mix", "light-dark", "env", "attr")
_OTHER_SPACES = ("lab", "lch", "hwb", "color")
# Each color function's channels, for the fix a refusal names.
_CHANNELS = {"rgb": "r g b", "hsl": "h s l", "oklch": "l c h", "oklab": "l a b"}
# CSS angle units, in degrees.
_HUE_UNITS = {"deg": 1.0, "turn": 360.0, "rad": 180 / math.pi, "grad": 0.9}


def _finite(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError(value)
    return value


def _number(text: str) -> float:
    value = float(text)
    if not math.isfinite(value):
        raise NotRead(f"{text} is not a finite number; write a plain number")
    return int(value) if value == int(value) and "." not in text and "e" not in text.lower() \
        else value


def _closing_paren(text: str, start: int) -> int:
    """The index of the paren that closes the one at `start`, skipping quoted
    text, or -1 when it never closes."""
    depth, quote = 0, ""
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            quote = "" if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i
    return -1


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
    m = _VAR_HEAD.match(text)
    # The reference is the whole value only when the paren that closes var(
    # is the last character.
    if m and _closing_paren(text, 3) == len(text) - 1:
        rest = text[m.end():-1]
        if not rest or rest.startswith(","):
            return m.group(1), rest[1:].strip()
    if "var(" in text and text.split("(", 1)[0].strip().lower() in _COMPUTED:
        raise NotRead(f"{text} is computed by the browser; write the value it computes to")
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
    if part.lower() == "none":  # CSS: a missing channel reads as zero
        return 0.0
    if part.endswith("%"):
        return _finite(float(part[:-1]) / 100 * scale)
    return _finite(float(part))


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
        names = _CHANNELS.get(name.rstrip("a") if name != "oklab" else name, "r g b")
        raise NotRead(f"{text} needs three channels; write it as {name}({names}) or "
                      f"{name}({names} / a)")
    return channels, alpha


def _alpha(text: Optional[str]) -> float:
    if text is None:
        return 1.0
    return _channel(text, 1)


def hsl_to_rgb(h: float, s: float, lightness: float) -> Tuple[float, float, float]:
    """An hsl color (hue in degrees, saturation and lightness from 0 to 1)
    as sRGB channels from 0 to 255."""
    c = (1 - abs(2 * lightness - 1)) * s
    hp = (h % 360) / 60
    x = c * (1 - abs(hp % 2 - 1))
    r, g, b = [(c, x, 0), (x, c, 0), (0, c, x), (0, x, c), (x, 0, c), (c, 0, x)][int(hp) % 6]
    m = lightness - c / 2
    return tuple((v + m) * 255 for v in (r, g, b))


def _hue(text: str, part: str) -> float:
    """A hue in degrees: a number, or an angle in deg, turn, rad or grad."""
    if part.lower() == "none":
        return 0.0
    m = _UNIT.match(part)
    if m:
        unit = m.group(2).lower()
        if unit not in _HUE_UNITS:
            raise NotRead(f"{text} writes its hue in {unit}, which this reader does not read; "
                          "write the hue in deg, turn, rad or grad")
        return _finite(float(m.group(1)) * _HUE_UNITS[unit])
    return _finite(float(part))


def hue_degrees(part: str) -> float:
    """A hue in degrees: a number, or an angle in deg, turn, rad or grad.
    Raises NotRead, naming the fix, for any other unit."""
    return _hue(part, part)


def _color_function(text: str, name: str, body: str,
                    mapped: Optional[List[GamutMapped]] = None) -> str:
    name = name.lower()
    if body.strip().lower().startswith("from "):
        raise NotRead(f"{text} is a relative color, computed by the browser; write the value "
                      "it computes to")
    try:
        channels, alpha_text = _args(text, name, body)
        alpha = _alpha(alpha_text)
        if name in ("rgb", "rgba"):
            rgb = tuple(_channel(c, 255) for c in channels)
        elif name in ("hsl", "hsla"):
            # CSS Color 4: a unitless saturation or lightness is a percentage.
            hue = _hue(text, channels[0])
            if "," in body and not all(c.endswith("%") for c in channels[1:]):
                raise NotRead(f"{text} writes saturation and lightness without %, which the "
                              f"comma syntax does not allow; write {name}({channels[0]}, "
                              f"{channels[1].rstrip('%')}%, {channels[2].rstrip('%')}%)")
            sat, light = (_channel(c.rstrip("%"), 1) / 100 for c in channels[1:])
            rgb = hsl_to_rgb(hue, sat, light)
        else:  # oklch, oklab
            lightness = _channel(channels[0], 1)
            if name == "oklch":
                chroma, hue = _channel(channels[1], 0.4), _hue(text, channels[2])
            else:
                _, chroma, hue = oklab_to_oklch(0, _channel(channels[1], 0.4),
                                                _channel(channels[2], 0.4))
            # CSS Color 4 gamut mapping, the one `system detect` uses too.
            hx, distance, was_mapped = gamut_map_oklch(lightness, chroma, hue)
            hx += _alpha_hex(alpha)
            if was_mapped and mapped is not None:
                mapped.append(GamutMapped(text, hx, distance))
            return hx
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


def _is_duration(word: str) -> bool:
    """True for a number in ms or s, the unit in any case."""
    m = _UNIT.match(word)
    return bool(m) and m.group(2).lower() in ("ms", "s")


def _is_length(word: str, any_unit: bool = False) -> bool:
    """True for a word a shadow layer reads as a length: 0, px or rem, or
    with `any_unit` any length unit, relative ones included."""
    m = _UNIT.match(word)
    units = ("px", "rem", *_RELATIVE) if any_unit else ("px", "rem")
    return word == "0" or bool(m and m.group(2).lower() in units)


def _shadow_layer(text: str, mapped: Optional[List[GamutMapped]]) -> dict:
    words = split_top(text, " ")
    inset = "inset" in (w.lower() for w in words)
    words = [w for w in words if w.lower() != "inset"]
    lengths, color = [], None
    for w in words:
        m = _UNIT.match(w)
        if _is_length(w):
            lengths.append({"value": _number(m.group(1)) if m else 0,
                            "unit": m.group(2).lower() if m else "px"})
        elif color is None:
            kind, value = read_value(w, mapped)
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


def read_value(text: Any, mapped: Optional[List[GamutMapped]] = None) -> Tuple[str, Any]:
    """(token type, internal literal) for a value written as text. Raises
    NotRead with the reason and the fix when the text has no single
    reading. A var() reference is not a value; read it with css_alias.
    Every oklch() or oklab() color mapped into sRGB is appended to `mapped`
    when it is given, so the importer can put it in its report."""
    if not isinstance(text, str):
        text = str(text)
    text = text.strip().rstrip(";").strip()
    if not text:
        raise NotRead("the value is empty; write a value or remove the entry")
    lower = text.lower()
    if lower == "currentcolor":
        raise NotRead(f"{text} has no fixed value; it takes the color of the element it sits "
                      "on, so write the color as hex")
    if lower in CSS_KEYWORDS:
        raise NotRead(f"{text} is a CSS keyword that takes its value from elsewhere, so it has no "
                      "value of its own; leave it out, or write the value it stands for as a "
                      "token")
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
        if name in ("rgb", "rgba", "hsl", "hsla", "oklch", "oklab"):
            return "color", _color_function(text, name, body, mapped)
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
    # A transition or animation shorthand, one member or a comma list of
    # them: a member of several words that holds a duration (in any case,
    # 200MS too). Checked before the font reading, which would take
    # `opacity 200ms ease` as a name; a list that ends in a generic family
    # (Font 2s, serif) is a font stack. A list of bare durations is named too.
    members = split_top(text)
    if not (len(members) > 1 and members[-1].lower() in GENERIC_FAMILIES):
        if any(len(split_top(p, " ")) > 1 and any(_is_duration(w) for w in split_top(p, " "))
               for p in members):
            # A capitalized word is a font name's more than a property's
            # (Font 2s, Inter): give a font author the way forward too.
            font = (", or, if it is a font list, quote each font name or end the list with a "
                    "generic family such as sans-serif") \
                if len(members) > 1 and re.search(r"(?<![\w-])[A-Z]", text) else ""
            raise NotRead(f"{text} is a transition or animation shorthand; write its duration "
                          f"and its curve as separate tokens{font}")
        if len(members) > 1 and all(_is_duration(p) for p in members):
            raise NotRead(f"{text} is a list of durations, one per transition or animation; "
                          "write each duration as its own token")
    names = _font_names(text)
    if names is not None:
        return "fontFamily", names
    words = split_top(text, " ")
    # inset is a border style and a shadow keyword; the shadow reading wins.
    if len(words) > 1 and any(w.lower() in STROKE_STYLES and w.lower() != "inset"
                              for w in words):
        raise NotRead(f"{text} is a border shorthand; write its width, style and color as "
                      "separate tokens")
    if re.fullmatch(_NUMBER + r"\s*/\s*" + _NUMBER, text):
        raise NotRead(f"{text} is a ratio, and the engine has no ratio token; keep it in the "
                      "component that uses it")
    if len(words) > 1 and any("/" in w and "(" not in w for w in words):
        raise NotRead(f"{text} is a font shorthand; write its family, size, weight and line "
                      "height as separate tokens")
    if re.fullmatch(_NUMBER + r"\s+" + _NUMBER + r"%\s+" + _NUMBER + "%", text):
        raise NotRead(f"{text} is hsl channels without hsl(); write hsl({text}) or hex")
    layers = split_top(text)
    # A shadow layer has two lengths at least; a length here is 0 or any
    # length unit, so a relative one gets its own refusal from the layer.
    if all(len(split_top(p, " ")) >= 3
           and sum(1 for w in split_top(p, " ") if w == "0" or _is_length(w, any_unit=True))
           >= 2 for p in layers):
        return "shadow", [_shadow_layer(p, mapped) for p in layers]
    if re.fullmatch(r"[A-Za-z][A-Za-z-]*", text):
        raise NotRead(f"{text} is a single word that could be a color name, a font name or a "
                      "keyword; write a color as hex, and quote a font name")
    raise NotRead(f"{text} is not a value this reader knows; write a hex color, a length in px "
                  "or rem, a duration in ms or s, a number, a curve or a quoted font list")
