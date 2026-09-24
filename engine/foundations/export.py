"""Exporters for a TokenSet: W3C DTCG 2025.10 JSON (in and out) and CSS
custom properties.

Values travel through values.encode and values.decode, so a color leaves
as a 2025.10 color object and comes back as the same hex string. Our own
data (layer, per-mode values) sits under one reverse-domain $extensions
key, EXT, as the format recommends."""
from __future__ import annotations

import itertools
import json
from typing import Any, Dict, List, Tuple

from engine.foundations.modes import AXES, CSS_AXES, join, parse
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.values import css_entries, decode, encode

EXT = "io.github.laith0003.ux-skill"
# The extension keys earlier builds wrote; a document that still carries
# them is refused, since reading it would drop its layers and modes.
LEGACY_EXT = ("ux.layer", "ux.modes")


def _conflict(prefix: str, path: str) -> ValueError:
    return ValueError(f"{prefix} is a token and also a group holding {path}; DTCG cannot "
                      "hold both, so rename one")


def to_dtcg(ts: TokenSet) -> Dict[str, Any]:
    """Nested DTCG groups. The mode axes go on the root's $extensions so
    from_dtcg rebuilds the same TokenSet. Raises ValueError when one path
    is a token and also a group of another, instead of dropping either."""
    doc: Dict[str, Any] = {"$extensions": {EXT: {"axes": {a: list(v) for a, v in ts.axes.items()}}}}
    for t in ts.tokens():
        node = doc
        *groups, leaf = t.path.split(".")
        for i, g in enumerate(groups):
            node = node.setdefault(g, {})
            if "$value" in node:
                raise _conflict(".".join(groups[:i + 1]), t.path)
        if leaf in node:
            below = next(p.path for p in ts.tokens() if p.path.startswith(t.path + "."))
            raise _conflict(t.path, below)
        ext: Dict[str, Any] = {"layer": t.layer}
        if t.modes:
            ext["modes"] = {m: encode(t.type, v, f"{t.path} ({m})") for m, v in t.modes.items()}
        entry: Dict[str, Any] = {"$type": t.type, "$value": encode(t.type, t.value, t.path),
                                 "$extensions": {EXT: ext}}
        if t.description:
            entry["$description"] = t.description
        node[leaf] = entry
    return doc


def dump_dtcg(ts: TokenSet) -> str:
    """The DTCG document as text with fixed settings (two space indent,
    non-ASCII kept as is, trailing newline), so equal sets give equal bytes
    whoever writes the file."""
    return json.dumps(to_dtcg(ts), indent=2, ensure_ascii=False) + "\n"


def from_dtcg(doc: Dict[str, Any]) -> TokenSet:
    """The inverse of to_dtcg. The axes come from the root's $extensions;
    a document without them gets the default AXES."""
    root_ext = (doc.get("$extensions") or {}).get(EXT) or {}
    axes = root_ext.get("axes")
    ts = TokenSet({a: tuple(v) for a, v in axes.items()} if axes else AXES)

    def walk(node: Dict[str, Any], path: List[str], inherited_type: str) -> None:
        # DTCG: a group's $type applies to every token below it that does
        # not declare its own; the nearest group wins.
        group_type = node.get("$type", inherited_type)
        for key, val in node.items():
            if key.startswith("$") or not isinstance(val, dict):
                continue
            if "$value" in val:
                type_ = val.get("$type", group_type)
                exts = val.get("$extensions") or {}
                legacy = [k for k in LEGACY_EXT if k in exts]
                if legacy:
                    raise ValueError(
                        f"{'.'.join(path + [key])} carries the extension keys {legacy}; "
                        "this file was written by an older build; re-export it with the "
                        "current version")
                ext = exts.get(EXT) or {}
                ts.add(Token(".".join(path + [key]), type_, decode(type_, val["$value"]),
                             modes={m: decode(type_, v) for m, v in (ext.get("modes") or {}).items()},
                             layer=ext.get("layer", "primitive"),
                             description=val.get("$description", "")))
            else:
                walk(val, path + [key], group_type)

    walk(doc, [], "")
    return ts


def _lines(t: Token, value: Any, indent: str = "  ") -> List[str]:
    return [f"{indent}{prop}: {text};" for prop, text in css_entries(t.path, t.type, value)]


def _rules(ts: TokenSet, key: str) -> List[Tuple[str, str]]:
    """(media query, selector) pairs under which override `key` applies:
    each axis in the key is set either by its root attribute or, when the
    axis has a media feature, by that feature while the attribute does not
    pin the base value. A key over k media-backed axes gives 2**k rules."""
    options = []
    for axis, value in parse(key, ts.axes).items():
        attr, media = CSS_AXES.get(axis, (f"data-{axis}", ""))
        forms = [("", f'[{attr}="{value}"]')]
        if media:
            forms.append((media, f':not([{attr}="{ts.axes[axis][0]}"])'))
        options.append(forms)
    out = []
    for combo in itertools.product(*options):
        media = " and ".join(m for m, _ in combo if m)
        out.append((media, ":root" + "".join(sel for _, sel in combo)))
    return out


def to_css(ts: TokenSet) -> str:
    """Custom properties on :root, then one rule per override key and form.
    Axes are set on the root element (data-theme, data-contrast,
    data-density, dir, data-motion) or by the matching media query when the
    attribute is absent. A rule over more axes has higher specificity, so
    a combined override wins over single-axis ones in every case."""
    out = [":root {", *(line for t in ts.tokens() for line in _lines(t, t.value)), "}"]
    keys: List[str] = []
    for t in ts.tokens():
        for key in t.modes:
            canonical = join(parse(key, ts.axes), ts.axes)
            if canonical not in keys:
                keys.append(canonical)
    order = list(ts.axes)
    keys.sort(key=lambda k: (len(parse(k, ts.axes)), [order.index(a) for a in parse(k, ts.axes)]))
    for key in keys:
        lines = [line for t in ts.tokens() for mk, v in t.modes.items()
                 if join(parse(mk, ts.axes), ts.axes) == key for line in _lines(t, v)]
        for media, selector in _rules(ts, key):
            if media:
                out += ["", f"@media {media} {{", f"  {selector} {{",
                        *("  " + line for line in lines), "  }", "}"]
            else:
                out += ["", f"{selector} {{", *lines, "}"]
    return "\n".join(out) + "\n"
