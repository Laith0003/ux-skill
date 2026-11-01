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
so it wins over the kit's themes whatever the selector weights. It reads
the engine's role names, so a system the engine did not build is refused
with the roles it lacks.
"""
from __future__ import annotations

from typing import List, Tuple

from engine.foundations.errors import InputError
from engine.foundations.tokens import TokenSet
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


def _value(ts: TokenSet, role: str, mode: str) -> str:
    t = ts.get(role)
    entries = css_entries(role, t.type, ts.resolve(role, mode))
    return entries[0][1]


def _block(ts: TokenSet, selector: str, mode: str) -> List[str]:
    lines = [f"{selector} {{"]
    lines += [f"  {prop}: {_value(ts, role, mode)};" for prop, role in LOOK]
    return lines + ["}"]


def to_stageshow(ts: TokenSet) -> str:
    """The look stylesheet: a light block on the stage and a dark block on a
    stage whose theme is dark, each token resolved from its role."""
    missing = sorted({role for _, role in LOOK if not ts.has(role)})
    if missing:
        raise InputError(
            f"--to stageshow reads the engine's roles, and this system lacks {', '.join(missing)}; "
            "build the system with `uxskill system build`, or export this one with --to css "
            "and map it to the --ss-* tokens by hand")
    head = [
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
    body = _block(ts, f".{LOOK_CLASS} .ss-stage", "") + [""]
    body += _block(ts, f'.{LOOK_CLASS} .ss-stage[data-theme="dark"]', DARK)
    return "\n".join(head + body) + "\n"
