"""Import a DTCG token file, ours or anyone's, in its own names.

A file this engine wrote (its root $extensions carry our axes) comes back
exactly: layers, modes and values as written, so export(import(file)) is
the same bytes. A foreign file is read by the DTCG 2025.10 rules: a group's
$type applies to the tokens below it, a token without a $type that
references another takes that token's type, `{a.b}` and `$ref` references
become aliases, and `$root` (a group's own token) is read as a segment
named root, which the report says. A token that references another is
semantic; any other is a primitive.

Values in the 2025.10 object forms are read as they are. Older string
forms ("16px", "#FFFFFF"), hsl, oklch and oklab colors, and a color with a
hex fallback are read with a note. An oklch or oklab color outside sRGB is
never refused: it is mapped into sRGB by CSS Color 4 gamut mapping, the
same one the value reader and `system detect` use, and the report lists it
under "Mapped into sRGB". An srgb color is its components: they are
checked, never clamped, and a hex fallback that disagrees with them is not
read. A value with more than one reading, a unit with no fixed size, a
color space the engine does not convert, a reference that loops back to
itself and the composite types it does not hold (border, transition,
gradient) are not read, each with the fix. Nothing is dropped without a
line: an older token form (`value` without `$value`), a bare value, a name
DTCG forbids and a property DTCG does not define are each listed.

A reference to a token the file does not define is not read, with the fix,
as the CSS reader does; it is never kept dangling.

A dark scheme is read wherever systems keep it, and paired by token path
into scheme:dark: a sibling file named for dark (tokens.dark.json,
x.dark.tokens.json beside x.tokens.json, x.dark-mode.json beside
x.light-mode.json, dark.json beside a file named for light, or the same
name in a dark/ folder), another tool's `dark` or `modes` entry in a
token's $extensions, or the themes of a Tokens Studio file. Mode and theme
names are placed by the importers' shared matcher: Dark Mode is
scheme:dark, High contrast is contrast:high, and Light or Default is the
base. A bare dark.json beside a file not named for light is not paired;
the report names it as a candidate, with the rename that pairs it. The
report names every pairing, and every semantic token with no value in a
paired file, folded into one line per file. A mode or theme whose name
places into no axis, and a value that could not be read, are listed under
Not read. Other tools' $extensions are otherwise left out and the report
says so.
"""
from __future__ import annotations

import json
import math
import re
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

from engine.foundations.color_math import gamut_map_oklch, hex_to_rgb, rgb_to_hex
from engine.foundations.errors import InputError
from engine.foundations.export import EXT, LEGACY_EXT
from engine.foundations.modes import AXES, ModeError, parse
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.foundations.validate import LAYERS
from engine.foundations.values import TYPES, TYPOGRAPHY_FIELDS
from engine.io.graph import cycles
from engine.io.mode_words import axis_of, is_base, mode_of, words
from engine.io.report import Imported, ImportReport, Item, Mapped, Source, read_source
from engine.io.values_in import GamutMapped, NotRead, read_value

# The weight names DTCG defines, and the number each one means.
WEIGHT_NAMES: Dict[str, int] = {
    "thin": 100, "hairline": 100, "extra-light": 200, "ultra-light": 200, "light": 300,
    "normal": 400, "regular": 400, "book": 400, "medium": 500, "semi-bold": 600,
    "demi-bold": 600, "bold": 700, "extra-bold": 800, "ultra-bold": 800, "black": 900,
    "heavy": 900, "extra-black": 950, "ultra-black": 950,
}
# DTCG composite types the engine holds no token for, with the fix.
UNHELD = {
    "border": "the engine holds no border composites, so write its width, style and color as "
              "three tokens",
    "transition": "the engine holds no transition composites, so write its duration and curve "
                  "as two tokens",
    "gradient": "the engine holds no gradients, so keep it in your own files",
}
# The properties DTCG 2025.10 defines on a group or a token. Any other $
# key is left out, and the report says so.
_DTCG_KEYS = ("$type", "$value", "$description", "$extensions", "$deprecated", "$schema",
              "$root", "$ref")
DARK = "scheme:dark"
_BAD_NAME = ".{}"
_HEX6 = re.compile(r"#[0-9A-Fa-f]{6}")
_LEGACY = "uses value, the form before DTCG 2025.10; write $value and $type"
_BARE = 'a bare value; write it as {"$value": ..., "$type": ...}'


def _and(items: List[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def _number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _components(comps: Any) -> Optional[List[float]]:
    """Three color components as numbers ("none" read as 0), or None."""
    if not (isinstance(comps, list) and len(comps) == 3):
        return None
    out: List[float] = []
    for c in comps:
        if c == "none":
            out.append(0.0)
        elif _number(c):
            out.append(c)
        else:
            return None
    return out


def _segment(key: str) -> str:
    return "root" if key == "$root" else key


def _rewrite(ref: str) -> str:
    """A reference with every $root segment read as root."""
    return ".".join(_segment(s) for s in ref.split("."))


def _alias(raw: Any) -> Optional[str]:
    """The reference a raw value makes, as {path}, or None. A `$ref` into
    another file or into part of a value is not an alias (_ref_problem
    names it)."""
    if is_alias(raw):
        return "{" + _rewrite(alias_target(raw)) + "}"
    if isinstance(raw, dict) and set(raw) == {"$ref"} and isinstance(raw["$ref"], str) \
            and raw["$ref"].startswith("#/"):
        # JSON Pointer: ~1 is "/" and ~0 is "~".
        parts = [p.replace("~1", "/").replace("~0", "~") for p in raw["$ref"][2:].split("/")]
        if "$value" in parts:
            at = parts.index("$value")
            if parts[at + 1:]:
                return None
            parts = parts[:at]
        return "{" + ".".join(_segment(p) for p in parts) + "}"
    return None


def _ref_problem(raw: Any) -> Optional[str]:
    """Why a `$ref` value cannot be followed, or None."""
    if not (isinstance(raw, dict) and "$ref" in raw) or _alias(raw) is not None:
        return None
    ref = raw["$ref"]
    if not isinstance(ref, str) or set(raw) != {"$ref"}:
        return f'has a $ref it cannot follow ({ref!r}); write it as {{"$ref": "#/group/token"}}'
    if not ref.startswith("#"):
        return f"references another file ({ref}); import both together or write the value"
    return f"references part of a value ({ref}); reference the whole token"


def _extensions_note(others: Iterable[str]) -> str:
    return (f"carries $extensions from {', '.join(others)}, which the engine does not read; "
            "they are left out of what it writes")


def _leaves(value: Any) -> List[Any]:
    if isinstance(value, dict):
        return [x for v in value.values() for x in _leaves(v)]
    if isinstance(value, list):
        return [x for v in value for x in _leaves(v)]
    return [value]


def _refs(value: Any) -> List[str]:
    return [alias_target(x) for x in _leaves(value) if is_alias(x)]


def _literal_text(value: Any) -> str:
    """A field's literal value as a person writes it: 16px, 400, Inter."""
    if isinstance(value, dict) and set(value) == {"value", "unit"} and _number(value["value"]):
        return f"{value['value']:g}{value['unit']}"
    if _number(value):
        return f"{value:g}"
    if isinstance(value, list) and all(isinstance(x, str) for x in value):
        return ", ".join(value)
    return value if isinstance(value, str) else json.dumps(value)


def _literals_inside(value: Any, context: str = "") -> List[str]:
    """A note for each literal field of a composite (a typography, a shadow
    and its layers) whose other fields are aliases: the token references
    others, so it is semantic, and a literal inside it is a primitive
    value that belongs in a token of its own."""
    layers = value if isinstance(value, list) else [value]
    if not layers or not all(isinstance(x, dict) for x in layers):
        return []
    fields = [(n, k, v) for n, layer in enumerate(layers, 1) for k, v in layer.items()]
    aliased = list(dict.fromkeys(k for _, k, v in fields if _refs(v)))
    if not aliased:
        return []
    at = f" in {context}" if context else ""
    held = aliased[0] if len(aliased) == 1 else ", ".join(aliased[:-1]) + " and " + aliased[-1]
    verb = "is" if len(aliased) == 1 else "are"
    return [f"its field {k}{f' of layer {n}' if len(layers) > 1 else ''}{at} "
            f"({_literal_text(v)}) is a literal inside a semantic token; extract it to a "
            f"primitive token and alias it, as {held} {verb}"
            for n, k, v in fields if not _refs(v)]


class _Reader:
    """Decodes one token's value, collecting notes for the report. `types`
    holds each token's declared type and `groups` every group path, so an
    alias to a group or to a token of another type is named, not kept."""

    def __init__(self, types: Dict[str, str], groups: Set[str]) -> None:
        self.types, self.groups = types, groups
        self.notes: List[str] = []
        self.mapped: List[GamutMapped] = []

    def take_mapped(self) -> List[GamutMapped]:
        """The colors mapped into sRGB since the last call."""
        out, self.mapped = self.mapped, []
        return out

    def checked(self, alias: str, kind: str) -> str:
        target = alias_target(alias)
        if target in self.groups and target not in self.types:
            raise NotRead(f"references {target}, which names a group, not a token; reference "
                          "one of its tokens")
        declared = self.types.get(target)
        if declared and declared != kind:
            raise NotRead(f"references {target}, a {declared}, where a {kind} belongs; point it "
                          f"at a {kind}")
        return alias

    def srgb(self, raw: Dict[str, Any], comps: Optional[List[float]]) -> str:
        if comps is None:
            raise NotRead("an srgb color without three numeric components; write them from 0 "
                          "to 1")
        if not all(0 <= c <= 1 for c in comps):
            if all(0 <= c <= 255 and c == int(c) for c in comps):
                raise NotRead(f"its srgb components {raw['components']} look like 0 to 255; "
                              "divide each by 255")
            raise NotRead(f"its srgb components {raw['components']} run outside 0 to 1; write "
                          "each from 0 to 1")
        rgb = [round(c * 255) for c in comps]
        value = rgb_to_hex(rgb)
        fallback = raw.get("hex")
        if fallback is None:
            return value
        if not (isinstance(fallback, str) and _HEX6.fullmatch(fallback)):
            raise NotRead(f"its hex fallback {fallback!r} is not #RRGGBB; write it that way or "
                          "leave it out")
        # The components are the color; a fallback within one 8-bit step of
        # them is the same color rounded, and is kept as written.
        if any(abs(a - b) > 1 for a, b in zip(rgb, hex_to_rgb(fallback))):
            raise NotRead(f"its components read as {value} but its hex fallback is "
                          f"{fallback.upper()}; fix one")
        return fallback.upper()

    def color(self, raw: Any) -> str:
        if isinstance(raw, str):
            kind, value = read_value(raw, self.mapped)
            if kind != "color":
                raise NotRead(f"{raw} is not a color; write a color object or a hex string")
            form = "a hex string" if raw.strip().startswith("#") else "a CSS color string"
            self.notes.append(f"{form}, the form before DTCG 2025.10; read as {value}")
            return value
        if not isinstance(raw, dict):
            raise NotRead(f"{raw!r} is not a color; write a color object")
        space = raw.get("colorSpace")
        if not isinstance(space, str):
            raise NotRead("a color object without a colorSpace; write srgb, hsl, oklch or oklab")
        alpha = raw.get("alpha", 1)
        if not (_number(alpha) and 0 <= alpha <= 1):
            raise NotRead(f"its alpha {alpha!r} is not a number from 0 to 1; write one")
        comps = _components(raw.get("components"))
        suffix = "" if alpha >= 1 else f"{max(0, min(255, round(alpha * 255))):02X}"
        if space == "srgb":
            return self.srgb(raw, comps) + suffix
        if space == "hsl" and comps is not None:
            if not all(0 <= c <= 100 for c in comps[1:]):
                raise NotRead("its hsl saturation and lightness run from 0 to 100; write them in "
                              "that range")
            _, value = read_value(f"hsl({comps[0]} {comps[1]}% {comps[2]}%)")
            value += suffix
            self.notes.append(f"an hsl color, converted to sRGB {value}")
            return value
        if space in ("oklch", "oklab") and comps is not None:
            # CSS Color 4 gamut mapping, the same one the value reader uses:
            # a color outside sRGB is mapped and reported, never refused.
            lightness, x, y = comps
            chroma, hue = (x, y) if space == "oklch" else \
                (math.hypot(x, y), math.degrees(math.atan2(y, x)) % 360)
            hx, distance, was_mapped = gamut_map_oklch(lightness, chroma, hue)
            value = hx + suffix
            if was_mapped:
                alpha_text = "" if alpha >= 1 else f" / {alpha:g}"
                original = f"{space}({' '.join(f'{c:g}' for c in comps)}{alpha_text})"
                self.mapped.append(GamutMapped(original, value, distance))
            else:
                self.notes.append(f"an {space} color, converted to sRGB {value}")
            return value
        hex_ = raw.get("hex")
        if isinstance(hex_, str):
            try:
                kind, value = read_value(hex_)
            except NotRead:
                kind, value = "", ""
            if kind != "color" or not value.startswith("#"):
                raise NotRead(f"a {space} color whose hex fallback {hex_} is not a hex color; "
                              "write it as #RRGGBB")
            value += suffix if len(value) == 7 else ""
            self.notes.append(f"a {space} color, read from its hex fallback {value}; the engine "
                              "measures sRGB only")
            return value
        raise NotRead(f"a {space} color with no hex fallback; the engine measures sRGB only, so "
                      "write it as srgb or add a hex fallback")

    def unit(self, kind: str, raw: Any) -> Dict[str, Any]:
        if isinstance(raw, dict) and set(raw) == {"value", "unit"}:
            if TYPES[kind].check(raw):
                return dict(raw)
            text = f"{raw['value']}{raw['unit']}"
        elif isinstance(raw, str):
            text = raw
        else:
            raise NotRead(f"{raw!r} is not a {kind}; {TYPES[kind].expected}")
        got, value = read_value(text)
        if got != kind:
            raise NotRead(f"{text} is not a {kind}; {TYPES[kind].expected}")
        if isinstance(raw, str):
            self.notes.append(f"a string, the form before DTCG 2025.10; read as {text}")
        elif isinstance(raw["value"], str):
            self.notes.append(f"its value is text inside the object; read as {text}")
        return value

    def weight(self, raw: Any) -> Any:
        if isinstance(raw, str) and raw in WEIGHT_NAMES:
            self.notes.append(f"the weight name {raw}, read as {WEIGHT_NAMES[raw]}")
            return WEIGHT_NAMES[raw]
        return self.string("fontWeight", raw)

    def string(self, kind: str, raw: Any) -> Any:
        """The older string form a build script writes ("700", "cubic-bezier(...)",
        "Inter, sans-serif") read through the shared value reader, with a
        note; anything else comes back as it is, for the type check to name."""
        if not isinstance(raw, str) or (kind == "fontFamily" and "," not in raw):
            return raw  # a single font name is the 2025.10 form
        try:
            got, value = read_value(raw)
        except NotRead:
            return raw
        if got != kind and not (kind == "fontWeight" and got == "number"):
            return raw
        self.notes.append("a string, the form before DTCG 2025.10; read as "
                          f"{json.dumps(value, ensure_ascii=False)}")
        return value

    def field(self, kind: str, raw: Any) -> Any:
        """One value of `kind`, or an alias."""
        problem = _ref_problem(raw)
        if problem:
            raise NotRead(problem)
        alias = _alias(raw)
        if alias is not None:
            return self.checked(alias, kind)
        if kind == "color":
            return self.color(raw)
        if kind in ("dimension", "duration"):
            return self.unit(kind, raw)
        if kind == "fontWeight":
            return self.weight(raw)
        if kind in ("cubicBezier", "fontFamily", "number"):
            return self.string(kind, raw)
        if kind == "strokeStyle" and isinstance(raw, dict):
            raise NotRead("a stroke style object (a dash pattern); the engine holds the keyword "
                          "form only, so write solid, dashed or dotted")
        return raw

    def shadow(self, raw: Any) -> Any:
        layers = raw if isinstance(raw, list) else [raw]
        out = []
        for layer in layers:
            if not isinstance(layer, dict):
                raise NotRead(f"{layer!r} is not a shadow layer; write an object with color, "
                              "offsetX, offsetY, blur and spread")
            new = {"color": self.field("color", layer.get("color"))}
            for key in ("offsetX", "offsetY", "blur", "spread"):
                if key not in layer:
                    raise NotRead(f"a shadow layer without {key}; add it")
                new[key] = self.field("dimension", layer[key])
            if "inset" in layer:
                new["inset"] = layer["inset"]
            out.append(new)
        return out if isinstance(raw, list) else out[0]

    def typography(self, raw: Any) -> Dict[str, Any]:
        if not isinstance(raw, dict):
            raise NotRead(f"{raw!r} is not a typography object")
        missing = [k for k in TYPOGRAPHY_FIELDS if k not in raw]
        if missing:
            raise NotRead(f"a typography value without {', '.join(missing)}; the engine reads "
                          "fontFamily, fontSize, fontWeight, letterSpacing and lineHeight, so "
                          "add them")
        extra = [k for k in raw if k not in TYPOGRAPHY_FIELDS]
        if extra:
            self.notes.append(f"its typography fields {', '.join(extra)} were left out; the "
                              "engine reads fontFamily, fontSize, fontWeight, letterSpacing "
                              "and lineHeight")
        return {k: self.field(t, raw[k]) for k, (t, _) in TYPOGRAPHY_FIELDS.items()}

    def value(self, kind: str, raw: Any) -> Any:
        if kind in UNHELD:
            raise NotRead(f"a {kind} token; {UNHELD[kind]}")
        if kind not in TYPES:
            raise NotRead(f"its type {kind} is not one the engine reads; use one of "
                          f"{sorted(TYPES)}")
        problem = _ref_problem(raw)
        if problem:
            raise NotRead(problem)
        alias = _alias(raw)
        if alias is not None:
            return self.checked(alias, kind)
        if kind == "shadow":
            value = self.shadow(raw)
        elif kind == "typography":
            value = self.typography(raw)
        else:
            value = self.field(kind, raw)
        if not TYPES[kind].check(value):
            raise NotRead(f"{raw!r} is not a {kind}; {TYPES[kind].expected}")
        return value


@dataclass
class _Entry:
    """A token as a file writes it: its path there (`src`), its path as read
    (`dst`), the node, its declared or inherited $type, the file's name and
    its place in the documents read."""
    src: str
    dst: str
    node: Dict[str, Any]
    kind: Any
    file: str
    pos: int

    @property
    def where(self) -> str:
        """The file; the report names the token by its path beside it."""
        return self.file


class _Log:
    """Report lines, each kept with its place in the documents and the token
    it belongs to (so a token dropped later takes its lines with it), and
    sorted into document order at the end."""

    def __init__(self) -> None:
        self.pos = 0
        self.renamed: List[Tuple[int, Optional[str], Item]] = []
        self.notes: List[Tuple[int, Optional[str], Item]] = []
        self.not_read: List[Tuple[int, Optional[str], Item]] = []
        self.mapped: List[Tuple[int, Optional[str], Mapped]] = []
        self.first: List[Item] = []  # pairings, ahead of everything else

    def next(self) -> int:
        self.pos += 1
        return self.pos

    @staticmethod
    def done(rows: List[Tuple[int, Optional[str], Any]], dropped: Set[str]) -> List[Any]:
        return [i for _, owner, i in sorted(rows, key=lambda r: r[0]) if owner not in dropped]


class _DuplicateKey(Exception):
    pass


def _pairs(pairs: List[Tuple[str, Any]]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise _DuplicateKey(key)
        out[key] = value
    return out


def _parse(text: str, name: str) -> Dict[str, Any]:
    try:
        doc = json.loads(text, object_pairs_hook=_pairs)
    except _DuplicateKey as exc:
        raise InputError(f"{name} holds the key {exc.args[0]!r} twice in one object; keep one "
                         "and import it again") from None
    except ValueError as exc:
        fix = "fix the file and import it again"
        if isinstance(exc, json.JSONDecodeError):
            at, ahead = text[exc.pos:exc.pos + 1], text[exc.pos + 1:].lstrip()[:1]
            behind = text[:exc.pos].rstrip()[-1:]
            if at == "/" or (at == "," and ahead in ("}", "]")) \
                    or (behind == "," and at in ("}", "]")):
                fix = "JSON holds no comments or trailing commas; remove them and import it again"
        raise InputError(f"{name} is not valid JSON ({exc}); {fix}") from None
    if not isinstance(doc, dict):
        kind = "list" if isinstance(doc, list) else type(doc).__name__
        raise InputError(f"{name} holds a JSON {kind}, not an object; a DTCG file is an object "
                         "of groups and tokens")
    return doc


def _axes(doc: Dict[str, Any], name: str) -> Optional[Dict[str, Tuple[str, str]]]:
    exts = doc.get("$extensions")
    ours = exts.get(EXT) if isinstance(exts, dict) else None
    axes = ours.get("axes") if isinstance(ours, dict) else None
    if axes is None:
        return None
    if not isinstance(axes, dict):
        raise InputError(f"{name} has an axes block that is not an object; write it as "
                         '{"scheme": ["light", "dark"]}')
    for axis, values in axes.items():
        if not (isinstance(values, list) and len(values) == 2
                and all(isinstance(v, str) for v in values)):
            raise InputError(f"{name} names the mode axis {axis} with {values!r}; a mode axis has "
                             "exactly two values, the base first, for example "
                             '"scheme": ["light", "dark"]')
    return {a: tuple(v) for a, v in axes.items()}


def _walk(log: _Log, root: Dict[str, Any], file: str, src0: List[str],
          skip: Tuple[str, ...] = ()) -> Tuple[List[_Entry], Set[str]]:
    """Every token under `root` in document order, and every group path.
    What is not a token or a group is listed in the log with the fix."""
    entries: List[_Entry] = []
    groups: Set[str] = set()
    seen: Dict[str, str] = {}

    def walk(node: Dict[str, Any], src: List[str], dst: List[str], group_type: Any) -> None:
        pos, gname = log.next(), ".".join(src)
        where = file
        if "$type" in node:
            if isinstance(node["$type"], str):
                group_type = node["$type"]
            else:
                log.not_read.append((pos, None, Item(
                    where, gname, f"its $type {node['$type']!r} is not a string; write one of "
                                  f"{sorted(TYPES)}; the tokens below take no type from it")))
        exts = node.get("$extensions")
        if "$extensions" in node and not isinstance(exts, dict):
            log.notes.append((pos, None, Item(where, gname, "its $extensions is not an object; "
                                                            "it was left out")))
        elif isinstance(exts, dict) and any(k != EXT for k in exts):
            log.notes.append((pos, None, Item(where, gname, _extensions_note(
                sorted(k for k in exts if k != EXT)))))
        if node.get("$deprecated"):
            log.notes.append((pos, None, Item(where, gname, "is marked deprecated; the engine "
                                                            "has no deprecated tokens, so the "
                                                            "tokens below were read as live "
                                                            "ones")))
        for key, val in node.items():
            s, d = src + [key], dst + [_segment(key)]
            path, at = ".".join(s), file
            if key.startswith("$") and key != "$root":
                if key not in _DTCG_KEYS and not (not src and key in skip):
                    log.notes.append((log.next(), None, Item(at, path, "is not a DTCG property; "
                                                                       "it was left out")))
                continue
            kpos = log.next()
            if any(c in key for c in _BAD_NAME):
                log.not_read.append((kpos, None, Item(at, path, "a name cannot contain '.', "
                                                                "'{' or '}'; rename it")))
            elif not isinstance(val, dict):
                log.not_read.append((kpos, None, Item(at, path, _BARE)))
            elif "$value" in val:
                read_as = ".".join(d)
                if read_as in seen:
                    log.not_read.append((kpos, None, Item(at, path, f"is read as {read_as}, "
                                                                    f"which {seen[read_as]} "
                                                                    "already names; rename "
                                                                    "one")))
                    continue
                seen[read_as] = path
                if key == "$root":
                    log.renamed.append((kpos, None, Item(
                        at, path, f"read as {read_as}, since a token path segment cannot start "
                                  f"with $; references to it now read {read_as}")))
                entries.append(_Entry(path, read_as, val, val.get("$type", group_type), file,
                                      kpos))
            elif "value" in val and not (isinstance(val["value"], dict)
                                         and "$value" in val["value"]):
                log.not_read.append((kpos, None, Item(at, path, _LEGACY)))
            else:
                groups.add(".".join(d))
                walk(val, s, d, group_type)

    walk(root, list(src0), [], "")
    # A token whose path also names a group ("root" beside "$root") cannot
    # be written back; the group's tokens are kept.
    clash = [e for e in entries if e.dst in groups]
    for e in clash:
        log.not_read.append((e.pos, None, Item(e.where, e.src, f"is read as {e.dst}, which also "
                                                               "names a group; rename one")))
    return [e for e in entries if e.dst not in groups], groups


def _ctx(axis: str) -> str:
    """The context of an axis's non-base value: scheme:dark."""
    return f"{axis}:{AXES[axis][1]}"


def _word(ctx: str) -> str:
    """How a message names a context's value: dark for scheme:dark."""
    return "dark" if ctx == DARK else ctx


def _both(ctx: str) -> str:
    axis = ctx.split(":")[0]
    return "both schemes" if axis == "scheme" else f"both {axis} modes"


def _base_word(ctx: str) -> str:
    axis = ctx.split(":")[0]
    return AXES[axis][0] if axis in AXES else "base"


@dataclass
class _Side:
    """The other mode of a pairing: its context, its tokens by path, how a
    message names it and where the pairing note sits."""
    ctx: str
    entries: List[_Entry]
    label: str
    where: str

    def __post_init__(self) -> None:
        self.index = {e.dst: e for e in self.entries}


def _studio(doc: Dict[str, Any], name: str, log: _Log) \
        -> Optional[Tuple[List[str], str, List[Tuple[str, List[str], str]]]]:
    """A Tokens Studio file's themes, placed by the importers' shared
    matcher: (the base theme's sets, its name, and for each theme that
    names a mode (Dark, Dark Mode, High contrast) its context, its sets and
    its name), the sets in the file's set order. None when no theme names
    a mode opposite a base. A theme or a set that is not read is listed."""
    themes = doc.get("$themes")
    if themes is None:
        return None
    pos = log.next()
    valid = [t for t in (themes if isinstance(themes, list) else [])
             if isinstance(t, dict) and isinstance(t.get("name"), str)
             and isinstance(t.get("selectedTokenSets"), dict)]
    placed = [(t, mode_of(t["name"])) for t in valid]
    unplaced = [t for t, axis in placed if axis is None]
    base = next((t for t in unplaced if is_base(t["name"])),
                unplaced[0] if len(unplaced) == 1 else None)
    if base is None or len(unplaced) == len(placed):
        log.notes.append((pos, None, Item(name, "$themes", (
            "names no base theme and mode theme, such as Light and Dark, so its sets were read "
            "as groups"))))
        return None
    sets = [k for k, v in doc.items() if not k.startswith("$") and isinstance(v, dict)]
    meta = doc.get("$metadata")
    order = meta.get("tokenSetOrder") if isinstance(meta, dict) else None
    if isinstance(order, list):
        sets = [s for s in order if s in sets] + [s for s in sets if s not in order]

    def chosen(theme: Dict[str, Any]) -> List[str]:
        picked = theme["selectedTokenSets"]
        return [s for s in sets if picked.get(s) in ("enabled", "source")]

    held: Dict[str, str] = {}
    sides: List[Tuple[str, List[str], str]] = []
    for theme, axis in placed:
        tname = theme["name"]
        if axis is None:
            if theme is not base:
                log.not_read.append((log.next(), None, Item(name, tname, (
                    f"is a theme whose name places into no mode axis beside {base['name']}, so "
                    "it was not read; name it for a mode, such as Dark or High contrast"))))
        elif axis in held:
            log.not_read.append((log.next(), None, Item(name, tname, (
                f"is a second theme for the {axis} axis, which {held[axis]} holds, so it was "
                "not read; keep one theme per axis"))))
        else:
            held[axis] = tname
            sides.append((_ctx(axis), chosen(theme), tname))
    base_sets = chosen(base)
    read = set(base_sets).union(*[set(s) for _, s, _ in sides])
    names = [base["name"]] + [t for _, _, t in sides]
    for s in sets:
        if s not in read:
            log.not_read.append((log.next(), None, Item(name, s, (
                f"is a set in none of the themes read ({_and(names)}), so it was not read; "
                "enable it in one of them"))))
    return base_sets, base["name"], sides


def _merge(log: _Log, sets: List[str],
           cache: Dict[str, Tuple[List[_Entry], Set[str]]]) -> Tuple[List[_Entry], Set[str]]:
    """One theme's tokens: its sets in order, a later set overriding."""
    out: Dict[str, _Entry] = {}
    groups: Set[str] = set()
    for s in sets:
        entries, found = cache[s]
        groups |= found
        for e in entries:
            if e.dst in out and out[e.dst] is not e:
                log.notes.append((e.pos, None, Item(e.where, e.src,
                                                    f"overrides {out[e.dst].src}, from an "
                                                    "earlier set")))
            out[e.dst] = e
    return list(out.values()), groups


def _tool_modes(value: Any) -> Tuple[Optional[str], Dict[str, Any], List[Tuple[str, str]]]:
    """(the key that holds modes, context -> raw value, [(mode name, why it
    was not read)]) for one tool's $extensions entry: a `dark` key, or a
    `modes` object whose names the importers' shared matcher places (Dark
    Mode is scheme:dark, high-contrast is contrast:high; a base name such
    as Light is the token's own value)."""
    if not isinstance(value, dict):
        return None, {}, []
    if "dark" in value:
        return "dark", {DARK: value["dark"]}, []
    modes = value.get("modes")
    if not (isinstance(modes, dict) and modes):
        return None, {}, []
    placed: Dict[str, Any] = {}
    left: List[Tuple[str, str]] = []
    held: Dict[str, str] = {}
    for raw_name, raw in modes.items():
        mode = str(raw_name)
        axis = mode_of(mode)
        if axis is None:
            if not is_base(mode):
                left.append((mode, "its name places into no mode axis; name it for a mode, such "
                                   "as Dark or High contrast"))
        elif axis in held:
            left.append((mode, f"it is a second mode for the {axis} axis, which {held[axis]} "
                               "holds; keep one"))
        else:
            held[axis] = mode
            placed[_ctx(axis)] = raw
    return "modes", placed, left


@dataclass(frozen=True)
class _Folded(Item):
    """Report lines of one kind folded into one: the line says how many and
    names a few; to_dict() keeps every one under items."""
    items: Tuple[Item, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = dict(super().to_dict())
        out["items"] = [i.to_dict() for i in self.items]
        return out


_OLDER = "the form before DTCG 2025.10; read as "
_FEW = 3


def _few(names: List[str]) -> str:
    shown = names if len(names) <= _FEW + 1 else names[:_FEW] + [f"{len(names) - _FEW} more"]
    return _and(shown)


def _fold_key(item: Item) -> Optional[Tuple[str, ...]]:
    if _OLDER in item.message:
        return ("older", item.where)
    if item.message.startswith("has no ") and "; it keeps this value in " in item.message:
        return ("missing", item.where, item.message)
    return None


def _fold(items: List[Item]) -> List[Item]:
    """The notes with each repeated per-token kind folded into one line at
    the place of its first: the older value forms of one file, and the
    tokens one paired file gives no value."""
    groups: Dict[Tuple[str, ...], List[Item]] = {}
    for i in items:
        key = _fold_key(i)
        if key is not None:
            groups.setdefault(key, []).append(i)
    out: List[Item] = []
    for i in items:
        key = _fold_key(i)
        group = groups.get(key) if key is not None else None
        if group is None or len(group) < 2:
            out.append(i)
            continue
        if group[0] is not i:
            continue
        n = len(group)
        if key[0] == "older":
            sample = _few([f"{g.name} ({g.message.rsplit(_OLDER, 1)[1]})" for g in group])
            message = (f"{n} tokens are written in forms before DTCG 2025.10 (strings where "
                       f"2025.10 writes objects) and were read as those values: {sample}; "
                       "write each as a 2025.10 $value object to drop this note")
        else:
            said = i.message.removeprefix("has no ").split("; it keeps this value in ")
            message = (f"{n} semantic tokens have no {said[0]} and keep their value in "
                       f"{said[1]}: {_few([g.name for g in group])}; give each its value there "
                       "to change it")
        out.append(_Folded(i.where, "", message, tuple(group)))
    return out


def import_dtcg(text: str, source: Source,
                dark: Optional[Tuple[str, Source]] = None) -> Imported:
    """The tokens a DTCG document holds, in its own names, and the report.
    `dark` is (text, source) of a file that holds the same tokens' dark
    values, paired by token path into scheme:dark."""
    name = Path(source.path).name
    doc = _parse(text, name)
    axes = _axes(doc, name)
    log = _Log()
    also: List[Source] = []
    if dark is not None and axes is not None:
        log.not_read.append((0, None, Item(Path(dark[1].path).name, "", (
            f"is named as the dark half of {name}, which carries its own modes, so it was not "
            f"read; import it on its own, or write its values as {DARK} modes in {name}"))))
        dark = None

    # Pass 1: the tokens in document order, the base ones and those of each
    # other mode, with their declared or group type.
    sides: List[_Side] = []
    light_label = name
    studio = _studio(doc, name, log) if axes is None and dark is None else None
    if studio is not None:
        base_sets, base_name, theme_sides = studio
        cache = {s: _walk(log, doc[s], name, [s])
                 for s in dict.fromkeys(base_sets + [s for _, sets, _ in theme_sides
                                                     for s in sets])}
        base, groups = _merge(log, base_sets, cache)
        for ctx, sets, tname in theme_sides:
            entries, found = _merge(log, sets, cache)
            groups |= found
            sides.append(_Side(ctx, entries, f"the theme {tname}", f"{name} $themes"))
        light_label = f"the theme {base_name}"
    else:
        base, groups = _walk(log, doc, name, [], ("$themes",))
        if dark is not None:
            dark_text, dark_source = dark
            dark_label = Path(dark_source.path).name
            entries, found = _walk(log, _parse(dark_text, dark_label), dark_label, [])
            groups |= found
            sides.append(_Side(DARK, entries, dark_label, dark_label))
            also.append(dark_source)

    index = {e.dst: e for e in base}
    union: Dict[str, _Entry] = {}
    for side in reversed(sides):
        union.update(side.index)
    union.update(index)
    types = {d: e.kind for d, e in union.items() if isinstance(e.kind, str) and e.kind}
    mode_axes = axes if axes is not None else AXES
    memo: Dict[str, Tuple[str, Optional[List[str]]]] = {}

    def type_of(path: str) -> Tuple[str, Optional[List[str]]]:
        """A token's type, following references for an untyped one, or ""
        with the loop when its references lead back to it."""
        chain: List[str] = []
        cur = path
        while cur not in memo:
            if cur in chain:
                loop = chain[chain.index(cur):]
                for i, n in enumerate(loop):
                    memo[n] = ("", loop[i:] + loop[:i] + [n])
                break
            e = union.get(cur)
            if e is not None and isinstance(e.kind, str) and e.kind:
                memo[cur] = (e.kind, None)
                break
            target = _alias(e.node.get("$value")) if e is not None else None
            if target is None:
                memo[cur] = ("", None)
                break
            chain.append(cur)
            cur = alias_target(target)
        found = memo[cur] if cur in memo else ("", None)
        for n in chain:
            memo.setdefault(n, (found[0], None))
        return memo[path]

    # Pass 2: decode each token, and its value in each other mode.
    tokens: List[Token] = []
    uses_our_modes = False
    # (the note's where, context, token path, whether the value is the same)
    events: List[Tuple[str, str, str, bool]] = []

    for e in base:
        where = e.where
        raw_exts = e.node.get("$extensions")
        exts = raw_exts if isinstance(raw_exts, dict) else {}
        legacy = [k for k in LEGACY_EXT if k in exts]
        if legacy:
            raise InputError(f"{e.file} {e.src} carries the extension keys {legacy}; this file "
                             "was written by an older build; build it again with the current "
                             "version and import that")
        reader = _Reader(types, groups)
        kind = e.kind
        if not isinstance(kind, str):
            log.not_read.append((e.pos, None, Item(where, e.src, f"its $type {kind!r} is not a "
                                                                 "string; write one of "
                                                                 f"{sorted(TYPES)}")))
            continue
        if not kind:
            target = _alias(e.node["$value"])
            kind, loop = type_of(e.dst)
            if not kind:
                ref = alias_target(target) if target is not None else ""
                if loop:
                    msg = (f"has no $type, and its references lead back to it "
                           f"({' -> '.join(loop)}); point one of them at a value")
                elif ref and ref in groups and ref not in union:
                    msg = (f"references {ref}, which names a group, not a token; reference one "
                           "of its tokens")
                elif ref and ref not in union:
                    msg = f"has no $type, and {ref}, which it references, is not in this file; " \
                          "add a $type"
                else:
                    msg = "has no $type and its groups set none; add a $type"
                log.not_read.append((e.pos, None, Item(where, e.src, msg)))
                continue
            reader.notes.append(f"has no $type, so it takes the type of {alias_target(target)}, "
                                "which it references")
        raw_ours = exts.get(EXT)
        ours = raw_ours if isinstance(raw_ours, dict) else {}
        if EXT in exts and not isinstance(raw_ours, dict):
            reader.notes.append(f"its {EXT} extension is not an object; it was left out")
        own_modes = ours.get("modes", {})
        if not isinstance(own_modes, dict):
            log.not_read.append((e.pos, None, Item(where, e.src, "its modes are not an object; "
                                                                 'write them as {"scheme:dark": '
                                                                 "<value>}")))
            continue
        bad = None
        for m in own_modes:
            try:
                parse(m, mode_axes)
            except ModeError as exc:
                bad = f"its mode {m} does not parse: {exc}"
                break
        if bad:
            log.not_read.append((e.pos, None, Item(where, e.src, bad)))
            continue
        try:
            value = reader.value(kind, e.node["$value"])
            gamut = [Mapped.of(where, e.src, g) for g in reader.take_mapped()]
            modes = {}
            for m, v in own_modes.items():
                modes[m] = reader.value(kind, v)
                gamut += [Mapped.of(f"{where} ({m})", e.src, g) for g in reader.take_mapped()]
        except NotRead as exc:
            log.not_read.append((e.pos, None, Item(where, e.src, str(exc))))
            continue
        uses_our_modes = uses_our_modes or bool(modes)

        # The other modes: the paired files or themes first, then another
        # tool's modes; our own modes win over both.
        tools = sorted(k for k in exts if k != EXT)
        left_out: List[str] = []
        # context -> (raw value, the note's where, where it sits, its name there, position)
        taken: Dict[str, Tuple[Any, str, str, str, int]] = {}
        missing: List[_Side] = []
        side_notes: List[Tuple[int, Optional[str], Item]] = []
        for side in sides:
            if side.ctx in modes:
                continue
            paired = side.index.get(e.dst)
            if paired is None:
                missing.append(side)
                continue
            clash = paired.kind if isinstance(paired.kind, str) and paired.kind else ""
            if paired is e:
                events.append((side.where, side.ctx, e.dst, True))
            elif clash and clash != kind:
                log.not_read.append((paired.pos, None, Item(
                    paired.where, paired.src, f"is a {clash} in {side.label} but a {kind} in "
                                              f"{light_label}; give both one type")))
            else:
                taken[side.ctx] = (paired.node.get("$value"), side.where, paired.where,
                                   paired.src, paired.pos)
        sided = {side.ctx for side in sides if side.index.get(e.dst) is not None}
        for tool in tools:
            held, placed, left = _tool_modes(exts[tool])
            for mode, why in left:
                log.not_read.append((e.pos, None, Item(where, e.src, (
                    f"its mode {mode} under {tool} was not read, since {why}"))))
            fresh = [c for c in placed if c not in taken and c not in modes and c not in sided]
            for c in fresh:
                taken[c] = (placed[c], f"{name} $extensions {tool}", where, e.src, e.pos)
            if held is None or (placed and not fresh) or set(exts[tool]) - {held}:
                left_out.append(tool)
        for c, (raw, label, at, src, pos) in taken.items():
            other = _Reader(types, groups)
            try:
                got = other.value(kind, raw)
            except NotRead as exc:
                log.not_read.append((pos, None, Item(at, src, (
                    f"its {_word(c)} value was not read: {exc}; it keeps its {_base_word(c)} "
                    f"value in {_both(c)}"))))
                continue
            events.append((label, c, e.dst, got == value))
            if got != value:
                modes[c] = got
                gamut += [Mapped.of(f"{at} ({c})", e.src, g) for g in other.take_mapped()]
            side_notes += [(pos, e.dst, Item(at, src, n)) for n in other.notes]

        deprecated = e.node.get("$deprecated")
        if deprecated:
            why = f" ({deprecated})" if isinstance(deprecated, str) else ""
            reader.notes.append(f"is marked deprecated{why}; the engine has no deprecated "
                                "tokens, so it was read as a live one")
        if left_out:
            reader.notes.append(_extensions_note(left_out))
        refs = [r for v in [value, *modes.values()] for r in _refs(v)]
        for context, v in [("", value), *modes.items()]:
            reader.notes += _literals_inside(v, context)
        description = e.node.get("$description", "")
        if not isinstance(description, str):
            reader.notes.append("its $description is not text; it was left out")
            description = ""
        inferred = "semantic" if refs else "primitive"
        layer = ours.get("layer")
        if layer not in LAYERS:
            if layer:
                reader.notes.append(f"its layer {layer!r} is not one of {list(LAYERS)}; it was "
                                    f"read as {inferred} by its references")
            layer = inferred
        # A primitive with one value in every mode is the usual case; only a
        # semantic token without a value in a paired mode is named.
        if layer == "semantic":
            reader.notes += [f"has no {_word(s.ctx)} value in {s.label}; it keeps this value in "
                             f"{_both(s.ctx)}" for s in missing]
        tokens.append(Token(e.dst, kind, value, modes=modes, layer=layer,
                            description=description))
        log.notes += [(e.pos, e.dst, Item(where, e.src, n)) for n in reader.notes] + side_notes
        log.mapped += [(e.pos, e.dst, g) for g in gamut]

    # A token in another mode with no base one is not read.
    reported: Set[int] = set()
    for side in sides:
        for d in side.entries:
            if d.dst not in index and id(d) not in reported:
                reported.add(id(d))
                log.not_read.append((d.pos, None, Item(d.where, d.src, (
                    f"is only in {side.label}, with no {_base_word(side.ctx)} value in "
                    f"{light_label}, so it was not read; add it to {light_label}"))))

    # Pass 3: a token that references one this file does not define, or one
    # that was not read, is not read, and neither is a token on a reference
    # loop. One pass over reverse references, so a long chain costs its
    # length.
    kept = {t.path: t for t in tokens}
    sources = {e.dst: e for e in base}
    refs_of = {p: [r for v in [t.value, *t.modes.values()] for r in _refs(v)]
               for p, t in kept.items()}
    users: Dict[str, List[str]] = {}
    for p, refs in refs_of.items():
        for r in dict.fromkeys(refs):
            users.setdefault(r, []).append(p)
    dropped: Set[str] = set()

    def drop(path: str, message: str) -> None:
        dropped.add(path)
        del kept[path]
        e = sources[path]
        log.not_read.append((e.pos, None, Item(e.where, e.src, message)))

    def spread(start: Iterable[str]) -> None:
        queue = deque(start)
        while queue:
            gone = queue.popleft()
            for p in users.get(gone, []):
                if p in kept:
                    drop(p, f"references {gone}, which was not read; fix {gone} and import again")
                    queue.append(p)

    for p in list(kept):
        outside = next((r for r in refs_of[p] if r not in union), None)
        if outside is not None:
            drop(p, f"references {outside}, which this file does not define; import it together "
                    "with the file that defines it, or write the value")
    for p in list(kept):
        gone = next((r for r in refs_of[p] if r in union and r not in kept), None)
        if gone is not None and p in kept:
            drop(p, f"references {gone}, which was not read; fix {gone} and import again")
    spread(sorted(dropped, key=lambda p: sources[p].pos))

    contexts = [""] + sorted({m for t in kept.values() for m in t.modes})
    looped: Dict[str, Tuple[List[str], str]] = {}
    for context in contexts:
        def succ(p: str, context: str = context) -> List[str]:
            t = kept[p]
            value = t.modes.get(context, t.value) if context else t.value
            return [r for r in dict.fromkeys(_refs(value)) if r in kept]
        for p, loop in cycles(list(kept), succ).items():
            looped.setdefault(p, (loop, context))
    for p in [p for p in list(kept) if p in looped]:
        loop, context = looped[p]
        where = f", in {context}" if context else ""
        drop(p, f"references {loop[1]}, which leads back to it ({' -> '.join(loop)}{where}); "
                "point one of them at a value")
    spread([p for p in looped])

    used = {c for _, c, _, _ in events} | {s.ctx for s in sides}
    if used:
        axes = dict(axes or {})
        for axis in AXES:
            if _ctx(axis) in used:
                axes.setdefault(axis, AXES[axis])
    elif axes is None:
        axes = dict(AXES) if uses_our_modes else {}
    try:
        ts = TokenSet(axes)
    except ValueError as exc:
        raise InputError(f"{name}: {exc}") from None
    for t in tokens:
        if t.path in kept:
            ts.add(t)
    report = ImportReport.of(source, ts, entries=len(base) + len({
        d.dst for side in sides for d in side.entries if d.dst not in index}))
    # One line per pairing, counting the tokens that were read.
    counts: Dict[Tuple[str, str], List[int]] = {}
    for label, c, path, same in events:
        if path in kept:
            counts.setdefault((label, c), [0, 0])[1 if same else 0] += 1
    for (label, c), (taken_n, same_n) in counts.items():
        takes = "token takes its" if taken_n == 1 else "tokens take their"
        log.first.append(Item(label, "", f"paired with {light_label} by token path into {c}; "
                                         f"{taken_n} {takes} {_word(c)} value from here and "
                                         f"{same_n} {'is' if same_n == 1 else 'are'} the same "
                                         f"in {_both(c)}"))
    report.renamed = _Log.done(log.renamed, dropped)
    report.notes = log.first + _fold(_Log.done(log.notes, dropped))
    report.not_read = _Log.done(log.not_read, dropped)
    report.mapped = _Log.done(log.mapped, dropped)
    report.also_read = also
    return Imported(ts, report)


# Words a file or folder name may hold beside the scheme word.
_NAME_WORDS = frozenset(("mode", "theme", "scheme", "tokens"))


def _dark_word(part: str) -> bool:
    """True when a part of a file name, or a folder name, names the dark
    scheme by the shared matcher and says nothing else: dark, dark-mode,
    darkMode; not darkness, and not a folder that only mentions dark."""
    return axis_of([part]) == ("scheme", -1) and words(part) - _NAME_WORDS == {"dark"}


def _light_word(part: str) -> bool:
    return words(part) - _NAME_WORDS == {"light"}


def _dark_named(path: Path) -> bool:
    return any(_dark_word(w) for w in path.name.split(".")[:-1]) or _dark_word(path.parent.name)


def _to_dark(part: str) -> str:
    """A light-named part with its light word turned to dark, case kept:
    light-mode to dark-mode, Light to Dark, lightMode to darkMode."""
    if not _light_word(part):
        return part
    return re.sub(r"light", lambda m: "Dark" if m.group(0)[0] == "L" else "dark", part,
                  flags=re.I)


def _dark_sibling(path: Path) -> Optional[Path]:
    """The file beside `path` that holds its dark scheme, by name: the
    light file's name with light turned to dark (tokens.light-mode.json,
    tokens.dark-mode.json), the name with .dark after its first part
    (tokens.json, tokens.dark.json), dark.json when `path` is named for
    light (light.json, theme.light.json) or sits in a light/ folder, or
    the same name in a dark/ folder. None when `path` itself is the dark
    one. A bare dark.json beside a file not named for light is only a
    candidate (see _bare_dark)."""
    parts = path.name.split(".")
    if _dark_named(path):
        return None
    first, _, rest = path.name.partition(".")
    options = []
    lit = any(_light_word(w) for w in parts[:-1])
    if lit:
        options.append(path.with_name(".".join([_to_dark(w) for w in parts[:-1]] + parts[-1:])))
    if rest:
        options.append(path.with_name(f"{first}.dark.{rest}"))
    if lit or _light_word(path.parent.name):
        options.append(path.with_name("dark.json"))
    options.append(path.parent / "dark" / path.name)
    if _light_word(path.parent.name):
        options.append(path.parent.parent / _to_dark(path.parent.name) / path.name)
    return next((o for o in options if o != path and o.is_file()), None)


def _bare_dark(path: Path) -> Optional[Item]:
    """A note on a bare dark.json beside `path` that was not paired with
    it: it belongs to a light.json beside it, or nothing names the pair."""
    bare = path.with_name("dark.json")
    if bare == path or _dark_named(path) or not bare.is_file():
        return None
    light = path.with_name("light.json")
    if light != path and light.is_file():
        return Item("dark.json", "", f"sits beside light.json, so it is read as the dark half "
                                     f"of light.json, not of {path.name}; import light.json to "
                                     "read the two schemes together")
    first, _, rest = path.name.partition(".")
    return Item("dark.json", "", f"sits beside {path.name} and may hold its dark scheme, but "
                                 "was not paired, since neither file is named for light; rename "
                                 f"{path.name} to light.json, or dark.json to "
                                 f"{first}.dark.{rest or 'json'}, and import again to read it as "
                                 "scheme:dark")


def read_dtcg(path: Any, label: str = "--from", pair: bool = True) -> Imported:
    """Read and import a DTCG file, with its dark sibling when one sits
    beside it (see _dark_sibling) and `pair` is true."""
    source, text = read_source(path, "dtcg", label)
    sibling = _dark_sibling(Path(source.path)) if pair else None
    if sibling is None:
        imported = import_dtcg(text, source)
        candidate = _bare_dark(Path(source.path)) if pair else None
        if candidate is not None:
            imported.report.notes.insert(0, candidate)
        return imported
    dark_source, dark_text = read_source(sibling, "dtcg", label)
    return import_dtcg(text, source, (dark_text, dark_source))
