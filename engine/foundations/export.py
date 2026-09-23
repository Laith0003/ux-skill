"""Exporters for a TokenSet: W3C DTCG JSON (in and out) and CSS custom properties."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from engine.foundations.tokens import Token, TokenSet, alias_target, css_property, is_alias


def to_dtcg(ts: TokenSet) -> Dict[str, Any]:
    doc: Dict[str, Any] = {}
    for t in ts.tokens():
        node = doc
        *groups, leaf = t.path.split(".")
        for g in groups:
            node = node.setdefault(g, {})
        ext: Dict[str, Any] = {"ux.layer": t.layer}
        if t.modes:
            ext["ux.modes"] = dict(t.modes)
        entry: Dict[str, Any] = {"$type": t.type, "$value": t.value, "$extensions": ext}
        if t.description:
            entry["$description"] = t.description
        node[leaf] = entry
    return doc


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
                ext = val.get("$extensions") or {}
                ts.add(Token(".".join(path + [key]), val.get("$type", group_type), val["$value"],
                             modes=dict(ext.get("ux.modes") or {}),
                             layer=ext.get("ux.layer", "primitive"),
                             description=val.get("$description", "")))
            else:
                walk(val, path + [key], group_type)

    walk(doc, [], "")
    return ts


def _css_value(value: str) -> str:
    return f"var({css_property(alias_target(value))})" if is_alias(value) else value


def to_css(ts: TokenSet) -> str:
    base = [f"  {css_property(t.path)}: {_css_value(t.value)};" for t in ts.tokens()]
    # Every mode override is emitted whatever the token's layer, so the CSS
    # carries exactly the data the gate checked (validate already rejects
    # primitives with modes and unknown layers).
    dark = [f"  {css_property(t.path)}: {_css_value(t.modes['dark'])};"
            for t in ts.tokens() if "dark" in t.modes]
    # A light subtree inside a dark page sets back, at its base value,
    # every property the dark block re-points.
    light = [f"  {css_property(t.path)}: {_css_value(t.value)};"
             for t in ts.tokens() if "dark" in t.modes]
    out = [":root {", *base, "}", "", '[data-theme="light"] {', *light, "}", "",
           '[data-theme="dark"] {', *dark, "}", "",
           "@media (prefers-color-scheme: dark) {", '  :root:not([data-theme="light"]) {',
           *("  " + line for line in dark), "  }", "}", ""]
    return "\n".join(out)
