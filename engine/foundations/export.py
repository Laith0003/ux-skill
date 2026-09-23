"""Exporters for a TokenSet: W3C DTCG JSON (in and out) and CSS custom properties."""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from engine.foundations.color import generate_color
from engine.foundations.gate import gate
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.foundations.validate import validate
from engine.synthesizer.axes import AxisValues


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

    def walk(node: Dict[str, Any], path: List[str]) -> None:
        for key, val in node.items():
            if key.startswith("$") or not isinstance(val, dict):
                continue
            if "$value" in val:
                ext = val.get("$extensions", {})
                ts.add(Token(".".join(path + [key]), val.get("$type", ""), val["$value"],
                             modes=dict(ext.get("ux.modes", {})),
                             layer=ext.get("ux.layer", "primitive"),
                             description=val.get("$description", "")))
            else:
                walk(val, path + [key])

    walk(doc, [])
    return ts


def _prop(path: str) -> str:
    return "--" + path.replace(".", "-")


def _css_value(value: str) -> str:
    return f"var({_prop(alias_target(value))})" if is_alias(value) else value


def to_css(ts: TokenSet) -> str:
    base = [f"  {_prop(t.path)}: {_css_value(t.value)};" for t in ts.tokens()]
    dark = [f"  {_prop(t.path)}: {_css_value(t.modes['dark'])};"
            for t in ts.tokens() if t.layer == "semantic" and "dark" in t.modes]
    out = [":root {", *base, "}", "", '[data-theme="dark"] {', *dark, "}", "",
           "@media (prefers-color-scheme: dark) {", '  :root:not([data-theme="light"]) {',
           *("  " + line for line in dark), "  }", "}", ""]
    return "\n".join(out)


def build_color(axes: AxisValues, brand_hex: str) -> Tuple[TokenSet, List[str]]:
    result = generate_color(axes, brand_hex)
    problems = validate(result.tokens)
    if problems:
        raise ValueError("\n".join(p.message for p in problems))
    gate(result.tokens)
    return result.tokens, result.notes
