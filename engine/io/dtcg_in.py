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
never refused (ruling M4-R5): it is mapped into sRGB by CSS Color 4 gamut
mapping, the one the value reader and `system detect` use, and the report
lists it under "Mapped into sRGB". A value with more than one reading, a unit
with no fixed size, a color space the engine does not convert and the
composite types it does not hold (border, transition, gradient) are not
read, each with the fix. Other tools' $extensions are left out and the
report says so.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from engine.foundations.color_math import gamut_map_oklch
from engine.foundations.emit import InputError
from engine.foundations.export import EXT, LEGACY_EXT
from engine.foundations.modes import AXES
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.foundations.values import TYPES, TYPOGRAPHY_FIELDS, decode
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
_GROUP_KEYS = ("$type", "$description", "$extensions", "$deprecated", "$schema")


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
    """The reference a raw value makes, as {path}, or None."""
    if is_alias(raw):
        return "{" + _rewrite(alias_target(raw)) + "}"
    if isinstance(raw, dict) and set(raw) == {"$ref"} and isinstance(raw["$ref"], str) \
            and raw["$ref"].startswith("#/"):
        parts = [p for p in raw["$ref"][2:].split("/") if p != "$value"]
        return "{" + ".".join(_segment(p) for p in parts) + "}"
    return None


class _Reader:
    """Decodes one token's value, collecting notes for the report."""

    def __init__(self) -> None:
        self.notes: List[str] = []
        self.mapped: List[GamutMapped] = []

    def take_mapped(self) -> List[GamutMapped]:
        """The colors mapped into sRGB since the last call."""
        out, self.mapped = self.mapped, []
        return out

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
        comps = raw.get("components")
        alpha = raw.get("alpha", 1)
        if space == "srgb":
            value = decode("color", raw)
            if not TYPES["color"].check(value):
                raise NotRead("an srgb color without three components from 0 to 1; write them, "
                              "or a hex fallback")
            return value
        if not (_number(alpha) and 0 <= alpha <= 1):
            raise NotRead(f"its alpha {alpha!r} is not a number from 0 to 1; write one")
        comps = _components(comps)
        suffix = "" if alpha >= 1 else f"{max(0, min(255, round(alpha * 255))):02X}"
        if space == "hsl" and comps is not None:
            _, value = read_value(f"hsl({comps[0]} {comps[1]}% {comps[2]}%)")
            value += suffix
            self.notes.append(f"an hsl color, converted to sRGB {value}")
            return value
        if space in ("oklch", "oklab") and comps is not None:
            # CSS Color 4 gamut mapping (M4-R5), the one read_value uses for
            # oklch() text: outside sRGB is mapped and reported, not refused.
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
        alias = _alias(raw)
        if alias is not None:
            return alias
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
        alias = _alias(raw)
        if alias is not None:
            return alias
        if kind == "shadow":
            value = self.shadow(raw)
        elif kind == "typography":
            value = self.typography(raw)
        else:
            value = self.field(kind, raw)
        if not TYPES[kind].check(value):
            raise NotRead(f"{raw!r} is not a {kind}; {TYPES[kind].expected}")
        return value


def _extensions_note(others: List[str]) -> str:
    return (f"carries $extensions from {', '.join(others)}, which the engine does not read; "
            "they are left out of what it writes")


def _leaves(value: Any) -> List[Any]:
    if isinstance(value, dict):
        return [x for v in value.values() for x in _leaves(v)]
    if isinstance(value, list):
        return [x for v in value for x in _leaves(v)]
    return [value]


def _axes(doc: Dict[str, Any], name: str) -> Optional[Dict[str, Tuple[str, str]]]:
    ext = (doc.get("$extensions") or {}).get(EXT) or {}
    axes = ext.get("axes")
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


def import_dtcg(text: str, source: Source) -> Imported:
    """The tokens a DTCG document holds, in its own names, and the report."""
    name = Path(source.path).name
    try:
        doc = json.loads(text)
    except ValueError as exc:
        raise InputError(f"{source.path} is not valid JSON ({exc}); fix the file and import it "
                         "again") from None
    if not isinstance(doc, dict):
        kind = "list" if isinstance(doc, list) else type(doc).__name__
        raise InputError(f"{source.path} holds a JSON {kind}, not an object; a DTCG file is an "
                         "object of groups and tokens")
    axes = _axes(doc, source.path)

    # Pass 1: every token in document order, with its declared or group type.
    entries: List[Tuple[str, str, Dict[str, Any], str]] = []
    renamed: List[Item] = []
    # Other tools' $extensions on a group or the root, by the index of the
    # first token after them, so the report keeps document order.
    group_notes: List[Tuple[int, Item]] = []

    def walk(node: Dict[str, Any], src: List[str], dst: List[str], group_type: str) -> None:
        group_type = node.get("$type", group_type)
        exts = node.get("$extensions")
        others = sorted(k for k in exts if k != EXT) if isinstance(exts, dict) else []
        if others:
            path = ".".join(src)
            group_notes.append((len(entries), Item(f"{name} {path or '(root)'}", path,
                                                   _extensions_note(others))))
        for key, val in node.items():
            if (key.startswith("$") and key != "$root") or not isinstance(val, dict):
                continue
            s, d = src + [key], dst + [_segment(key)]
            if "$value" in val:
                if key == "$root":
                    renamed.append(Item(f"{name} {'.'.join(s)}", ".".join(s),
                                        f"read as {'.'.join(d)}, since a token path segment "
                                        "cannot start with $; references to it now read "
                                        f"{'.'.join(d)}"))
                entries.append((".".join(s), ".".join(d), val, val.get("$type", group_type)))
            else:
                walk(val, s, d, group_type)

    walk(doc, [], [], "")
    declared = {d: t for _, d, _, t in entries}

    def type_of(path: str, seen: Tuple[str, ...] = ()) -> str:
        """A token's type, following references for an untyped one."""
        if declared.get(path):
            return declared[path]
        node = next((v for _, d, v, _ in entries if d == path), None)
        target = _alias(node["$value"]) if node is not None else None
        if target is None or path in seen:
            return ""
        return type_of(alias_target(target), seen + (path,))

    # Pass 2: decode each token.
    tokens: List[Token] = []
    notes: List[Item] = []
    not_read: List[Item] = []
    mapped: List[Mapped] = []
    uses_our_modes = False
    for index, (src, dst, node, kind) in enumerate(entries):
        notes += [item for i, item in group_notes if i == index]
        where = f"{name} {src}"
        legacy = [k for k in LEGACY_EXT if k in (node.get("$extensions") or {})]
        if legacy:
            raise InputError(f"{name} {src} carries the extension keys {legacy}; this file was "
                             "written by an older build; build it again with the current "
                             "version and import that")
        reader = _Reader()
        if not kind:
            target = _alias(node["$value"])
            kind = type_of(dst)
            if not kind and target is not None and alias_target(target) not in declared:
                not_read.append(Item(where, src, f"has no $type, and {alias_target(target)}, "
                                                 "which it references, is not in this file; "
                                                 "add a $type"))
                continue
            if not kind:
                not_read.append(Item(where, src, "has no $type and its groups set none; add a "
                                                 "$type"))
                continue
            reader.notes.append(f"has no $type, so it takes the type of "
                                f"{alias_target(target)}, which it references")
        exts = node.get("$extensions") if isinstance(node.get("$extensions"), dict) else {}
        ours = exts.get(EXT) or {}
        others = sorted(k for k in exts if k != EXT)
        try:
            value = reader.value(kind, node["$value"])
            gamut = [Mapped.of(where, src, g) for g in reader.take_mapped()]
            modes = {}
            for m, v in (ours.get("modes") or {}).items():
                modes[m] = reader.value(kind, v)
                gamut += [Mapped.of(f"{where} ({m})", src, g) for g in reader.take_mapped()]
        except NotRead as exc:
            not_read.append(Item(where, src, str(exc)))
            continue
        uses_our_modes = uses_our_modes or bool(modes)
        deprecated = node.get("$deprecated")
        if deprecated:
            why = f" ({deprecated})" if isinstance(deprecated, str) else ""
            reader.notes.append(f"is marked deprecated{why}; the engine has no deprecated "
                                "tokens, so it was read as a live one")
        if others:
            reader.notes.append(_extensions_note(others))
        refs = [alias_target(x) for v in [value, *modes.values()] for x in _leaves(v)
                if is_alias(x)]
        outside = sorted({r for r in refs if r not in declared})
        if outside:
            reader.notes.append(f"references {', '.join(outside)}, which this file does not "
                                "hold; the reference is kept as written and resolves only "
                                "where the file that defines it is read too")
        aliased = bool(refs)
        layer = ours.get("layer") or ("semantic" if aliased else "primitive")
        tokens.append(Token(dst, kind, value, modes=modes, layer=layer,
                            description=node.get("$description", "")
                            if isinstance(node.get("$description", ""), str) else ""))
        notes += [Item(where, src, n) for n in reader.notes]
        mapped += gamut

    notes += [item for i, item in group_notes if i == len(entries)]

    # Pass 3: a token that references one that was not read is not read.
    kept = {t.path: t for t in tokens}
    sources = {d: s for s, d, _, _ in entries}
    changed = True
    while changed:
        changed = False
        for t in list(kept.values()):
            refs = [alias_target(x) for v in [t.value, *t.modes.values()] for x in _leaves(v)
                    if is_alias(x)]
            gone = next((r for r in refs if r not in kept and r in declared), None)
            if gone is not None:
                del kept[t.path]
                not_read.append(Item(f"{name} {sources[t.path]}", sources[t.path],
                                     f"references {gone}, which was not read; fix {gone} and "
                                     "import again"))
                notes = [i for i in notes if i.name != sources[t.path]]
                mapped = [i for i in mapped if i.name != sources[t.path]]
                changed = True

    if axes is None:
        axes = dict(AXES) if uses_our_modes else {}
    try:
        ts = TokenSet(axes)
    except ValueError as exc:
        raise InputError(f"{source.path}: {exc}") from None
    for t in tokens:
        if t.path in kept:
            ts.add(t)
    report = ImportReport.of(source, ts, entries=len(entries))
    report.renamed, report.notes, report.not_read = renamed, notes, not_read
    report.mapped = mapped
    return Imported(ts, report)


def read_dtcg(path: Any, label: str = "--from") -> Imported:
    """Read and import a DTCG file."""
    source, text = read_source(path, "dtcg", label)
    return import_dtcg(text, source)
