"""Export a system as a Stageshow look, so a product illustration made with
the Stageshow kit wears the page's own system.

Stageshow (github.com/benjitaylor/skills, MIT) builds faux product UI from
a React kit whose parts read --ss-* custom properties. A look sets those
properties; to_stageshow() writes one from the system's roles: the
surfaces, the three text inks, the icons, the line, the accent, the status
colors, the faces and the radii, each resolved in light and in dark. The
light block sits on the stage and the dark block on a stage whose theme is
dark, so a dark product demo can sit on a light page and the other way
round.

The kit tunes some tokens to an illustration's scale rather than to a
product: its shadows carry the framing (a hero over its ground, a satellite
over the hero), its control and row heights are a miniature's, and its
placeholder inks draw filler. Those stay the kit's (KIT_OWNED): a page's
44px control would read as a chunky toy at illustration size.

The kit puts its own tokens in `@layer stageshow`; the look is unlayered,
so it wins over the kit's themes whatever the selector weights. A Stage
renders its className on the .ss-fit wrapper around .ss-stage, and its
theme is always explicit (light unless set), so the look selects the stage
inside the class and pins each theme's values rather than following the
page.

It reads the engine's roles, found by the CSS property each becomes, so a
tokens.json and a tokens.css ux-skill wrote (whose roles import with flat
names, color-surface-page) give the same look. A system without them is
refused with the roles it lacks.
"""
from __future__ import annotations

from typing import Dict, List, Mapping, Sequence, Tuple

from engine.foundations.errors import InputError
from engine.foundations.tokens import TokenSet, css_property
from engine.foundations.values import css_entries

# The class a stage's wrapper takes to wear the look: <Stage className="ux-look">.
LOOK_CLASS = "ux-look"
FILE_NAME = "stageshow-look.css"
DARK = "scheme:dark"

# (look token, the role it stands for), in the order the kit lists them.
LOOK: Tuple[Tuple[str, str], ...] = (
    ("--ss-canvas", "color.surface.page"),
    ("--ss-surface", "color.surface.card"),
    ("--ss-chrome", "color.surface.header"),
    ("--ss-well", "color.surface.sunken"),
    ("--ss-raised", "color.surface.raised"),
    ("--ss-line", "color.line.subtle"),
    ("--ss-text-strong", "color.text.default"),
    ("--ss-text", "color.text.muted"),
    ("--ss-text-faint", "color.text.disabled"),
    ("--ss-icon", "color.text.muted"),
    ("--ss-icon-faint", "color.text.disabled"),
    ("--ss-accent", "color.action.primary"),
    ("--ss-accent-2", "color.action.primary-pressed"),
    ("--ss-accent-soft", "color.surface.selected"),
    ("--ss-accent-text", "color.text.accent"),
    ("--ss-success", "color.status.success.strong"),
    ("--ss-success-soft", "color.status.success.soft"),
    ("--ss-success-text", "color.status.success.text"),
    ("--ss-danger", "color.status.danger.strong"),
    ("--ss-danger-soft", "color.status.danger.soft"),
    ("--ss-danger-text", "color.status.danger.text"),
    ("--ss-warning", "color.status.warning.strong"),
    ("--ss-warning-soft", "color.status.warning.soft"),
    ("--ss-warning-text", "color.status.warning.text"),
    ("--ss-font", "type.face.text"),
    ("--ss-mono", "type.face.mono"),
    ("--ss-radius-sm", "radius.chip"),
    ("--ss-radius-md", "radius.control"),
    ("--ss-radius-lg", "radius.card"),
    ("--ss-radius-window", "radius.dialog"),
    ("--ss-radius-pill", "radius.pill"),
)

# Tokens the kit tunes to an illustration's scale, which the look leaves alone.
KIT_OWNED: Tuple[str, ...] = (
    "--ss-shadow-window", "--ss-shadow-float", "--ss-shadow-card", "--ss-shadow-hero",
    "--ss-shadow-lift", "--ss-shadow-satellite", "--ss-shadow-ground",
    "--ss-control", "--ss-row", "--ss-line-faint", "--ss-fill",
    "--ss-ink-1", "--ss-ink-2", "--ss-ink-3", "--ss-ink-4", "--ss-ink-5",
)


# How the refusal names the caller's own fields; the MCP tools pass theirs.
LABELS: Mapping[str, str] = {"to": "--to", "build": "uxskill system build"}


def _paths(ts: TokenSet) -> Dict[str, str]:
    """Each role's path in this system, found by the CSS property it becomes."""
    by_property = {css_property(t.path): t.path for t in ts.tokens()}
    return {role: by_property[css_property(role)] for _, role in LOOK
            if css_property(role) in by_property}


def _value(ts: TokenSet, path: str, mode: str) -> str:
    t = ts.get(path)
    return css_entries(path, t.type, ts.resolve(path, mode))[0][1]


def _block(ts: TokenSet, paths: Mapping[str, str], selector: str, mode: str) -> List[str]:
    lines = [f"{selector} {{"]
    lines += [f"  {prop}: {_value(ts, paths[role], mode)};" for prop, role in LOOK]
    return lines + ["}"]


def to_stageshow(ts: TokenSet, *, labels: Mapping[str, str] = LABELS,
                 header: Sequence[str] = ()) -> str:
    """The look stylesheet: a light block on the stage and a dark block on a
    stage whose theme is dark, each token resolved from its role. `header`
    lines (what an import of a foreign system left out) open the file."""
    paths = _paths(ts)
    missing = sorted({role for _, role in LOOK if role not in paths})
    if missing:
        raise InputError(
            f"{labels['to']} stageshow reads ux-skill's roles, and this system lacks "
            f"{', '.join(missing)}; build the system with {labels['build']}, or map these "
            "roles to the --ss-* tokens by hand")
    lead = [f" * {line}".rstrip().replace("*/", "* /") for line in header]
    head = (["/*", *lead, " */", ""] if lead else []) + [
        "/* A Stageshow look from this design system: its surfaces, text, accent,",
        " * status colors, faces and radii, in light and in dark.",
        " *",
        " * Load it after the kit's stageshow.css, with the system's fonts.css for",
        f' * the faces, and give the stage the class: <Stage className="{LOOK_CLASS}">.',
        ' * theme="dark" on the stage takes the dark values. Shadows, control and row',
        " * heights and the placeholder inks stay the kit's: they are tuned to an",
        " * illustration's scale. Unlayered, so it wins over the kit's own themes. */",
        "",
    ]
    body = _block(ts, paths, f".{LOOK_CLASS} .ss-stage", "") + [""]
    body += _block(ts, paths, f'.{LOOK_CLASS} .ss-stage[data-theme="dark"]', DARK)
    return "\n".join(head + body) + "\n"
