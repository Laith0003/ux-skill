"""Exporters for a TokenSet: W3C DTCG 2025.10 JSON (in and out) and CSS
custom properties.

Values travel through values.encode and values.decode, so a color leaves
as a 2025.10 color object and comes back as the same hex string. Our own
data (layer, per-mode values) sits under one reverse-domain $extensions
key, EXT, as the format recommends."""
from __future__ import annotations

import json
from typing import Any, Dict, List, Tuple

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
    """Nested DTCG groups. Raises ValueError when one path is a token and
    also a group of another, instead of dropping either."""
    doc: Dict[str, Any] = {}
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


def from_dtcg(doc: Dict[str, Any], mode_names: Tuple[str, ...] = ("light", "dark")) -> TokenSet:
    ts = TokenSet(mode_names)

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


def to_css(ts: TokenSet) -> str:
    base = [line for t in ts.tokens() for line in _lines(t, t.value)]
    # Every mode override is emitted whatever the token's layer, so the CSS
    # carries exactly the data the gate checked (validate already rejects
    # primitives with modes and unknown layers).
    dark = [line for t in ts.tokens() if "dark" in t.modes for line in _lines(t, t.modes["dark"])]
    # A light subtree inside a dark page sets back, at its base value,
    # every property the dark block re-points.
    light = [line for t in ts.tokens() if "dark" in t.modes for line in _lines(t, t.value)]
    out = [":root {", *base, "}", "", '[data-theme="light"] {', *light, "}", "",
           '[data-theme="dark"] {', *dark, "}", "",
           "@media (prefers-color-scheme: dark) {", '  :root:not([data-theme="light"]) {',
           *("  " + line for line in dark), "  }", "}", ""]
    return "\n".join(out)
