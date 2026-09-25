"""Exporters for a TokenSet: W3C DTCG 2025.10 JSON (in and out) and CSS
custom properties.

Values travel through values.encode and values.decode, so a color leaves
as a 2025.10 color object and comes back as the same hex string. Our own
data (layer, per-mode values) sits under one reverse-domain $extensions
key, EXT, as the format recommends."""
from __future__ import annotations

import itertools
import json
from typing import Any, Dict, List, Mapping, Optional, Tuple

from engine.foundations.layout import responsive_css
from engine.foundations.typography import phone_roles, responsive_lines, scale_property
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


def _lines(t: Token, value: Any, indent: str = "  ", phone: Tuple[str, ...] = ()) -> List[str]:
    """The declarations of one token value. A type style in `phone` scales
    its size and letter spacing by its --<style>-scale property, which
    tokens.css sets to the phone factor below the tablet breakpoint and to
    1 from it up."""
    entries = css_entries(t.path, t.type, value)
    if t.path in phone:
        scale = scale_property(t.path)
        entries = [(prop, f"calc({text} * var({scale}))"
                    if prop.endswith(("-font-size", "-letter-spacing")) else text)
                   for prop, text in entries]
    return [f"{indent}{prop}: {text};" for prop, text in entries]


# How the scheme axis reaches CSS for each default scheme: "system" follows
# the operating system unless data-theme pins it; "light" opens light and
# switches only on data-theme="dark"; "dark" opens dark unless
# data-theme="light".
SCHEME_DEFAULTS = ("system", "light", "dark")


# A right to left subtree: any element inside the root with dir="rtl" or
# an Arabic lang, so an Arabic block inside a left to right page gets the
# Arabic faces, sizes and travel sign too. The root keeps its own form.
NESTED_RTL = ':is([dir="rtl"], [lang|="ar"])'


def _rules(ts: TokenSet, key: str, scheme: str = "system",
           forms: Optional[Mapping[str, Tuple[str, str]]] = None) -> List[Tuple[str, str]]:
    """(media query, selector) pairs under which override `key` applies:
    each axis in the key is set either by its root attribute or, when the
    axis has a media feature, by that feature while the attribute does not
    pin the base value. A key over k media-backed axes gives 2**k rules.
    The scheme axis follows `scheme` (SCHEME_DEFAULTS). The direction axis
    at rtl has a second form, a subtree inside the root (NESTED_RTL), with
    every other axis still read from the root, so a combined override
    reaches the subtree with the same specificity it has on the root. An
    axis named in `forms` is set by the selector (and media query, when one
    is given) recorded there, as an imported stylesheet set it."""
    options = []
    for axis, value in parse(key, ts.axes).items():
        if forms and axis in forms:
            selector, media = forms[axis]
            options.append([("", selector, "")] + ([(media, "", "")] if media else []))
            continue
        attr, media = CSS_AXES.get(axis, (f"data-{axis}", ""))
        if axis == "scheme" and scheme == "dark":
            options.append([("", f':not([{attr}="{ts.axes[axis][0]}"])', "")])
            continue
        forms = [("", f'[{attr}="{value}"]', "")]
        if media and not (axis == "scheme" and scheme == "light"):
            forms.append((media, f':not([{attr}="{ts.axes[axis][0]}"])', ""))
        if axis == "direction" and value == "rtl":
            forms.append(("", "", NESTED_RTL))
        options.append(forms)
    out = []
    for combo in itertools.product(*options):
        media = " and ".join(m for m, _, _ in combo if m)
        nested = "".join(n for _, _, n in combo)
        out.append((media, ":root" + "".join(sel for _, sel, _ in combo)
                    + (f" {nested}" if nested else "")))
    return out


def to_css(ts: TokenSet, *, scheme: str = "system",
           forms: Optional[Mapping[str, Tuple[str, str]]] = None) -> str:
    """Custom properties on :root, then one rule per override key and form.
    Axes are set on the root element (data-theme, data-contrast,
    data-density, dir, data-motion) or by the matching media query when the
    attribute is absent; `scheme` sets which scheme opens (SCHEME_DEFAULTS).
    A set with a scheme axis in use writes color-scheme with each scheme,
    so native controls follow it. A rule over more axes has higher
    specificity, so a combined override wins over single-axis ones in every
    case. `forms` gives an imported system's own selector for an axis
    (css_in records it), so the system is written back the way it came.
    Last come the layout's responsive aliases (layout.responsive_css), one
    property per tiered role that follows the viewport."""
    if scheme not in SCHEME_DEFAULTS:
        raise ValueError(f"scheme is {scheme!r}; use one of {list(SCHEME_DEFAULTS)}")
    schemed = "scheme" in ts.axes and any(
        "scheme" in parse(k, ts.axes) for t in ts.tokens() for k in t.modes)
    base = [f"  color-scheme: {ts.axes['scheme'][0]};"] if schemed else []
    phone = tuple(phone_roles(ts))
    out = [":root {", *base, *(line for t in ts.tokens() for line in _lines(t, t.value,
                                                                             phone=phone)), "}"]
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
                 if join(parse(mk, ts.axes), ts.axes) == key
                 for line in _lines(t, v, phone=phone)]
        if schemed and parse(key, ts.axes).get("scheme") not in (None, ts.axes["scheme"][0]):
            lines = [f"  color-scheme: {parse(key, ts.axes)['scheme']};"] + lines
        for media, selector in _rules(ts, key, scheme, forms):
            if media:
                out += ["", f"@media {media} {{", f"  {selector} {{",
                        *("  " + line for line in lines), "  }", "}"]
            else:
                out += ["", f"{selector} {{", *lines, "}"]
    out += responsive_css(ts, responsive_lines(ts))
    return "\n".join(out) + "\n"
