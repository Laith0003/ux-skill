"""Export a system as a Tailwind 4 theme stylesheet, and write one beside
a Tailwind source.

For a system in the engine's roles (to_tailwind with roles=True: a built
system, or a tokens file whose ownership record says the engine wrote it),
every semantic role gets a name in Tailwind's theme namespaces
(color.surface.page is --color-surface-page, space.control.gap
--spacing-control-gap, radius.card --radius-card, a shadow level
--shadow-card, a curve --ease-reveal, a breakpoint --breakpoint-tablet, a
text style --text-body with its --line-height, --letter-spacing and
--font-weight), holding its resolved value inside @theme. Primitives are
left out, so a utility can only name a role; the faces are the one
exception, since each is named for the role it plays (display, text, mono
and the Arabic faces) and Tailwind sets a family only through --font-*,
which is not reset, so Tailwind's own families stay. Tailwind cannot read
a custom property inside a media query, so the breakpoints come from the
tokens as values, not as var() references. The namespaces the system
fills are reset first (RESETS), so Tailwind's own palette and scales do
not sit beside it as a second source. Each mode is an override block of
the same variables, switched the way tokens.css switches it (data-theme,
dir and the rest, or the preference media query).

Tailwind switches by breakpoint variant, not by a property that follows
the viewport, so the viewport layer of tokens.css becomes theme values:
each tier of a layout role is its own variable (--spacing-gutter-phone to
--spacing-gutter-desktop), and each text style that steps down on a phone
has a phone style beside it (--text-hero-phone, its size and letter
spacing times the phone factor), so a page writes text-hero-phone
tablet:text-hero.

Any other system is written in its own names (roles=False, the default):
a system imported from a Tailwind stylesheet comes back with its own
selectors, resets, scheme and `@custom-variant dark` line, so imported and
written again the text is the same. Whether a system is the engine's is
read from the source's ownership record (Imported.owned), never from its
token names: a foreign file that happens to use a role's name stays
foreign.

write_tailwind() writes to a Tailwind source through the intake step. A
stylesheet the engine wrote (it carries the engine's digest and still
matches it) is rewritten in place. A stylesheet the engine did not write
is never rewritten: the additions go in an extension stylesheet beside it
(theme-ext.css beside theme.css), in the source's own names, with its own
@theme block and override blocks in the source's own selectors, stamped
with the engine's digest so a forced write can replace it later, and the
outcome says to load it after the source.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.existing import stamp_digest
from engine.foundations.errors import InputError
from engine.foundations.export import to_css
from engine.foundations.modes import FOUNDATION_AXES, compress, contexts
from engine.foundations.tokens import Token, TokenSet, css_property
from engine.foundations.typography import FACE_TOKENS, phone_roles, phone_token
from engine.foundations.values import REM_PX, css_entries, dimension_px
from engine.io.adapter import ROLE_TYPES
from engine.io.intake import write_with_intake
from engine.io.report import Imported

# Tailwind namespaces the exporter fills and clears first.
RESETS: Tuple[str, ...] = ("--color-*", "--radius-*", "--shadow-*", "--ease-*",
                           "--breakpoint-*", "--text-*")
# What an extension file adds to its source's name: theme.css, theme-ext.css.
EXTENSION_SUFFIX = "-ext"
_TEXT_FIELDS = (("fontSize", "", "dimension"), ("lineHeight", "--line-height", "number"),
                ("letterSpacing", "--letter-spacing", "dimension"),
                ("fontWeight", "--font-weight", "fontWeight"))


def tailwind_name(role: str) -> Optional[str]:
    """The Tailwind theme variable (without --) a role takes, or None for a
    token that is not written (a phone factor, which becomes phone styles)."""
    parts = role.split(".")
    root, rest = parts[0], parts[1:]
    dashed = "-".join(rest)
    if root == "color":
        return f"color-{dashed}"
    if root == "space":
        return f"spacing-{dashed}"
    if root == "radius":
        return f"radius-{dashed}"
    if root == "border":
        return f"border-{dashed}"
    if root == "elevation":
        return f"z-{'-'.join(rest[1:])}" if rest[0] == "order" else f"shadow-{dashed}"
    if root == "motion":
        if rest[-1] == "curve":
            return f"ease-{'-'.join(rest[:-1])}"
        if rest[-1] == "duration":
            return f"duration-{'-'.join(rest[:-1])}"
        return f"motion-{dashed}"
    if root == "layout":
        kind, tail = rest[0], "-".join(rest[1:])
        return {"breakpoint": f"breakpoint-{tail}", "container": f"container-{tail}",
                "measure": f"container-measure-{tail}", "columns": f"columns-{tail}"}.get(
            kind, f"spacing-{dashed}")
    if root == "type":
        if rest[0] == "run":
            return f"font-{dashed}"
        if rest[0] == "face":
            return f"font-{'-'.join(rest[1:])}"
        if rest[0] == "text":
            return f"text-{'-'.join(rest[1:])}"
        if rest[:2] == ["icon", "size"]:
            return f"spacing-icon-{'-'.join(rest[2:])}"
        if rest == ["strong"]:
            return "font-weight-strong"
    if root == "imagery":
        return f"aspect-{'-'.join(rest[1:])}" if rest[0] == "ratio" else f"color-imagery-{dashed}"
    return None


def _is_role(t: Token) -> bool:
    """A semantic role, or a face (named for the role it plays)."""
    return (t.layer == "semantic" and t.path in ROLE_TYPES) or t.path in FACE_TOKENS.values()


def _times(dim: Mapping[str, Any], factor: float) -> Dict[str, Any]:
    """A dimension times a factor, to a hundredth of a pixel, in its own
    unit."""
    per_px = REM_PX if dim["unit"] == "rem" else 1
    px = round(dimension_px(dim) * factor, 2)
    return {"value": round(px / per_px, 4) + 0, "unit": dim["unit"]}


def _phone(values: Mapping[str, Any], factors: Mapping[str, float]) -> Dict[str, Any]:
    """A text style's values per context with its size and letter spacing
    times the phone factor in that context, as tokens.css computes them
    below the tablet breakpoint."""
    return {ctx: {**v, "fontSize": _times(v["fontSize"], factors[ctx]),
                  "letterSpacing": _times(v["letterSpacing"], factors[ctx])}
            for ctx, v in values.items()}


def _roles_set(ts: TokenSet) -> TokenSet:
    """The roles as Tailwind variables with resolved values per mode."""
    out = TokenSet(ts.axes)
    phone = phone_roles(ts)
    for t in ts.tokens():
        if not _is_role(t):
            continue
        name = tailwind_name(t.path)
        if name is None:
            continue
        axes = [a for a in FOUNDATION_AXES.get(t.path.split(".", 1)[0], tuple(ts.axes))
                if a in ts.axes]
        values = {ctx: ts.resolve(t.path, ctx) for ctx in contexts(axes, ts.axes)}
        if t.type != "typography":
            base, modes = compress(values, ts.axes)
            out.add(Token(name, t.type, base, modes=modes))
            continue
        styles = [(name, values)]
        if t.path in phone:
            factors = {ctx: ts.resolve(phone_token(t.path), ctx) for ctx in values}
            styles.append((name + "-phone", _phone(values, factors)))
        for style, per in styles:
            for field, suffix, kind in _TEXT_FIELDS:
                base, modes = compress({c: v[field] for c, v in per.items()}, ts.axes)
                out.add(Token(style + suffix, kind, base, modes=modes))
    return out


def _parts(ts: TokenSet, forms: Optional[Mapping[str, Tuple[str, str]]], scheme: str,
           roles: bool) -> Tuple[List[str], List[str], str, List[str]]:
    """to_css's text cut into (the comment that opens it, the base
    declarations, the base color-scheme line or "", everything after the
    base block)."""
    body = to_css(_roles_set(ts) if roles else ts, scheme=scheme, forms=forms)
    lines = body.split("\n")
    start = lines.index(":root {")
    end = lines.index("}", start)
    theme = lines[start + 1:end]
    scheme_line = theme.pop(0) if theme and theme[0].startswith("  color-scheme:") else ""
    return lines[:start], theme, scheme_line, lines[end + 1:]


def to_tailwind(ts: TokenSet, forms: Optional[Mapping[str, Tuple[str, str]]] = None,
                resets: Optional[Sequence[str]] = None, *, scheme: str = "system",
                roles: bool = False, variant: str = "") -> str:
    """A Tailwind 4 theme stylesheet for `ts` (see the module docstring).
    `roles` is True for a system in the engine's roles, which takes RESETS
    unless `resets` is given; any other system is written in its own names
    with the resets given. `forms`, `resets`, `scheme` and `variant` (the
    `@custom-variant dark` declaration, written back before @theme) come
    from an imported stylesheet; `scheme` says which scheme it opens, as
    tokens.css does. Opens with @theme unless the system needs a note (a
    number held from 0 to 100) or a variant first."""
    note, theme, scheme_line, after = _parts(ts, forms, scheme, roles)
    if resets is None:
        resets = RESETS if roles else ()
    head = [*note, *([variant, ""] if variant else []), "@theme {",
            *(f"  {r}: initial;" for r in resets), *theme, "}"]
    # @theme holds custom properties only: the base color-scheme goes in a
    # :root block of its own, after the theme and before the overrides.
    own = f"\n:root {{\n{scheme_line}\n}}\n" if scheme_line else ""
    return "\n".join(head) + "\n" + own + "\n".join(after)


def in_roles(imported: Imported) -> bool:
    """True when an imported system is in the engine's roles: a tokens file
    whose ownership record says the engine wrote it. A stylesheet the
    engine wrote is already in Tailwind's names and is written back in
    them."""
    return imported.owned and imported.report.source.format == "dtcg"


def export_tailwind(imported: Imported) -> str:
    """An imported system as a Tailwind 4 stylesheet: in the engine's roles
    when in_roles() says so, else in its own names, forms, resets, scheme
    and dark variant."""
    return to_tailwind(imported.tokens, imported.forms, imported.resets or None,
                       scheme=imported.scheme, roles=in_roles(imported),
                       variant=imported.variant)


def extension_name(source: Any) -> str:
    """The extension file written beside a source: theme.css gives
    theme-ext.css."""
    p = Path(source)
    return f"{p.stem}{EXTENSION_SUFFIX}{p.suffix or '.css'}"


def _shown(t: Token) -> str:
    """A token's value as the stylesheet writes it, with each mode."""
    def text(value: Any) -> str:
        return "; ".join(v for _, v in css_entries(t.path, t.type, value))
    modes = ", ".join(f"{k}: {text(v)}" for k, v in t.modes.items())
    return f"{text(t.value)} ({modes})" if modes else text(t.value)


def _additions(imported: Imported, ts: TokenSet) -> TokenSet:
    """The tokens of `ts` the source does not hold, matched by the custom
    property each becomes. Raises InputError naming the property and the
    fix when `ts` changes one the source holds: an extension only adds."""
    source = imported.report.source.path
    held = {css_property(t.path): t for t in imported.tokens.tokens()}
    out = TokenSet(ts.axes)
    for t in ts.tokens():
        name = css_property(t.path)
        old = held.get(name)
        if old is None:
            out.add(t)
        elif (old.type, old.value, old.modes) != (t.type, t.value, t.modes):
            raise InputError(f"{name} is {_shown(old)} in {source} and {_shown(t)} in the system "
                             "to write; an extension file only adds tokens, so change "
                             f"{name} in {source} itself, or add a token under a new name")
    return out


def tailwind_extension(imported: Imported, ts: TokenSet) -> str:
    """The extension stylesheet beside a Tailwind source the engine did not
    write: the tokens of `ts` the source does not hold, in the source's own
    names, in an @theme block of its own, each mode in the source's own
    selectors, opened by a comment that says to load it after the source
    and carries the engine's digest. "" when there is nothing to add.
    Raises InputError when `ts` changes a token the source holds."""
    added = _additions(imported, ts)
    if not added.tokens():
        return ""
    name = Path(imported.report.source.path).name
    note, theme, _, after = _parts(added, imported.forms, imported.scheme, False)
    # The source sets color-scheme with each scheme; the extension adds
    # tokens only.
    after = [line for line in after if not line.strip().startswith("color-scheme:")]
    head = ["/*", f" * Written by ux-skill beside {name}, which it never rewrites: each",
            " * token below is an addition in the source's own names.",
            f" * Load it after {name}.", " */", *note, "@theme {", *theme, "}"]
    return stamp_digest("\n".join(head) + "\n" + "\n".join(after), css=True)


def write_tailwind(ts: TokenSet, imported: Imported, *, force: bool = False,
                   replace_client: bool = False, force_label: str = "--force",
                   replace_label: str = "--replace-client-files",
                   out_label: str = "--out") -> Dict[str, Any]:
    """Write `ts`, a system in the names of the Tailwind stylesheet
    `imported` was read from, to that source through the intake step (see
    the module docstring): in place when the engine wrote the source,
    else as an extension file beside it. Returns write_with_intake's
    outcome with `file` (the file written to) and `load` (how to load an
    extension file, else ""). Raises InputError when `imported` is not a
    Tailwind stylesheet, or when `ts` changes a token a foreign source
    holds."""
    source = imported.report.source
    path = Path(source.path).expanduser()
    if source.format != "tailwind":
        raise InputError(f"{source.path} is a {source.format} source, not a Tailwind "
                         "stylesheet, so no Tailwind file is written beside it; pass the "
                         "Tailwind stylesheet (.css) the system lives in, or export the system "
                         "to a new folder")
    load = ""
    if imported.owned:
        name = path.name
        text = stamp_digest(to_tailwind(ts, imported.forms, imported.resets,
                                        scheme=imported.scheme, variant=imported.variant),
                            css=True)
    else:
        name = extension_name(path)
        text = tailwind_extension(imported, ts)
        if not text:
            return {"status": "unchanged", "written": [], "unchanged": [], "conflicts": [],
                    "message": f"{source.path} already holds every token of the system to "
                               "write, so no extension file was written.",
                    "backup": "", "replaced": {}, "file": "", "load": ""}
        count = len(_additions(imported, ts).tokens())
        load = (f"Load {path.parent / name} after {source.path}: it adds {count} "
                f"token{'' if count == 1 else 's'} to that theme and changes nothing in it. "
                f"Where the source is imported, import {name} on the line after it, for "
                f'example @import "./{name}";')
    outcome = write_with_intake(path.parent, {name: text}, imported.report, force=force,
                                replace_client=replace_client, force_label=force_label,
                                replace_label=replace_label, out_label=out_label)
    outcome["file"] = str(path.parent / name)
    outcome["load"] = load
    if load and outcome["status"] in ("written", "unchanged"):
        outcome["message"] += " " + load
    return outcome
