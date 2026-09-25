"""Layout foundation: breakpoints, grid columns and gutters, page margins,
the gap between regions and the padding of the header, hero and footer per
breakpoint, container and reading widths, and the minimum target size.

Gutters and margins alias the spacing scale (space.<n>), so layout and
spacing move together; the density axis places them and compact takes one
step less, never below 8px. Breakpoints are minimum viewport widths; a
phone is everything below the tablet breakpoint. CSS cannot read custom
properties inside a media query, so the breakpoint tokens are reference
values; responsive_css writes one alias per tiered role (RESPONSIVE),
--layout-<role>, that takes the phone value and switches to each tier's
value under a media query on the literal breakpoint, so a page reads one
property and gets the right tier at every width.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Sequence, Tuple

from engine.foundations import space
from engine.foundations.foundation import (
    BrandInputs, Foundation, Generated, direct_alias, is_step, typed)
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet, css_property
from engine.foundations.values import dimension_px
from engine.synthesizer.axes import AxisValues

TIERS = ("phone", "tablet", "laptop", "desktop")
VIEWPORTS = {"tablet": 640, "laptop": 1024, "desktop": 1280}
COLUMNS = {"phone": 4, "tablet": 8, "laptop": 12, "desktop": 12}
# tier -> (space units when the density axis is 0, when it is 1)
GUTTER = {"phone": (4, 3), "tablet": (6, 4), "laptop": (8, 5), "desktop": (8, 6)}
MARGIN = {"phone": (5, 4), "tablet": (8, 6), "laptop": (12, 8), "desktop": (16, 10)}
# Page regions per tier, in space units: the gap between regions and the
# block padding of the hero grow with the viewport, so a phone never shows
# a screen of empty space.
# The desktop gap is space.region.gap's pair, so the two tokens agree at
# every density.
REGION_GAP = {"phone": (12, 8), "tablet": (16, 12), "laptop": (24, 16), "desktop": (32, 16)}
HERO_PADDING = {"phone": (16, 10), "tablet": (20, 12), "laptop": (24, 16), "desktop": (32, 20)}
# The gap between the sections of a landing page, per tier: airier than an
# app's region gap, 128 to 192px at desktop by density, so a long page
# changes pace between sections. Never below the region gap at its tier.
LANDING_GAP = {"phone": (20, 16), "tablet": (24, 20), "laptop": (32, 24), "desktop": (48, 32)}
# Header and footer block padding, the same at every width.
HEADER_PADDING, FOOTER_PADDING = (4, 3), (16, 10)
# Tiered roles with a responsive alias in CSS (responsive_css).
RESPONSIVE = ("columns", "gutter", "margin-inline", "region-gap", "landing-gap",
              "hero.padding-block")
# Tiered roles that alias the spacing scale (layout-on-space).
ON_SPACE = ("gutter", "margin-inline", "region-gap", "landing-gap", "hero.padding-block")
COMPACT_FLOOR = 2  # space units, 8px
CONTAINERS = (1120, 1280, 1440)
MEASURE_REM = {"text": 38, "form": 32}
# Our approximation of the 80 characters WCAG 1.4.8 sets as the widest line.
MAX_TEXT_MEASURE_REM = 40
TARGET_PX = {"comfortable": 44, "compact": 32}
MIN_TARGET_PX, COMFORTABLE_TARGET_PX = 24, 44
# A large control (the call to action of a hero) stands this much taller.
LARGE_EXTRA_PX = 12


def _units(pair: Tuple[int, int], density: float) -> Tuple[int, int]:
    """Comfortable and compact space units on the spacing scale's own rules."""
    comfortable = space.snap(pair[0] + (pair[1] - pair[0]) * density)
    return comfortable, space.compact_step(comfortable, COMPACT_FLOOR)


def container_px(density: float) -> int:
    return space.snap(CONTAINERS[0] + (CONTAINERS[-1] - CONTAINERS[0]) * density, CONTAINERS)


def generate_layout(axes: AxisValues, target_px: int = TARGET_PX["comfortable"],
                    measure_rem: int = MEASURE_REM["text"],
                    refuse_compact: bool = False) -> Generated:
    """The page grid and regions. `target_px` and `measure_rem` come from
    the audience (larger targets for older readers, a narrower measure for
    long reading); with `refuse_compact` the compact mode keeps every
    comfortable value."""
    d = axes.density
    measures = dict(MEASURE_REM, text=measure_rem)
    targets = {"comfortable": target_px,
               "compact": target_px if refuse_compact else TARGET_PX["compact"]}
    ts = TokenSet()
    for px in VIEWPORTS.values():
        ts.add(Token(f"layout.viewport.{px}", "dimension", {"value": px, "unit": "px"}))
    for n in sorted(set(COLUMNS.values())):
        ts.add(Token(f"layout.column-count.{n}", "number", n))
    for px in sorted(set(CONTAINERS) | set(TARGET_PX.values()) | set(targets.values())
                     | {targets["comfortable"] + LARGE_EXTRA_PX}):
        ts.add(Token(f"layout.width.{px}", "dimension", {"value": px, "unit": "px"}))
    for rem in sorted(set(MEASURE_REM.values()) | set(measures.values())):
        ts.add(Token(f"layout.rem.{rem}", "dimension", {"value": rem, "unit": "rem"}))

    for tier, px in VIEWPORTS.items():
        ts.add(Token(f"layout.breakpoint.{tier}", "dimension", "{layout.viewport.%d}" % px,
                     layer="semantic"))
    for tier in TIERS:
        ts.add(Token(f"layout.columns.{tier}", "number",
                     "{layout.column-count.%d}" % COLUMNS[tier], layer="semantic"))
    for group, table in (("gutter", GUTTER), ("margin-inline", MARGIN),
                         ("region-gap", REGION_GAP), ("landing-gap", LANDING_GAP),
                         ("hero.padding-block", HERO_PADDING)):
        for tier in TIERS:
            comfortable, compact = _units(table[tier], d)
            compact = comfortable if refuse_compact else compact
            modes = {"density:compact": "{space.%d}" % compact} if compact != comfortable else {}
            ts.add(Token(f"layout.{group}.{tier}", "dimension", "{space.%d}" % comfortable,
                         modes=modes, layer="semantic"))
    for name, pair in (("header", HEADER_PADDING), ("footer", FOOTER_PADDING)):
        comfortable, compact = _units(pair, d)
        compact = comfortable if refuse_compact else compact
        modes = {"density:compact": "{space.%d}" % compact} if compact != comfortable else {}
        ts.add(Token(f"layout.{name}.padding-block", "dimension", "{space.%d}" % comfortable,
                     modes=modes, layer="semantic"))
    ts.add(Token("layout.container.max", "dimension", "{layout.width.%d}" % container_px(d),
                 layer="semantic"))
    for name, rem in measures.items():
        ts.add(Token(f"layout.measure.{name}", "dimension", "{layout.rem.%d}" % rem,
                     layer="semantic"))
    ts.add(Token("layout.target.min", "dimension", "{layout.width.%d}" % targets["comfortable"],
                 modes={} if targets["compact"] == targets["comfortable"] else
                 {"density:compact": "{layout.width.%d}" % targets["compact"]},
                 layer="semantic"))
    ts.add(Token("layout.target.large", "dimension",
                 "{layout.width.%d}" % (targets["comfortable"] + LARGE_EXTRA_PX),
                 layer="semantic"))
    return Generated(tokens=ts, notes=[f"layout: container {container_px(d)}px"])


def responsive_css(ts: TokenSet, extra: Dict[str, List[str]] = None) -> List[str]:
    """CSS lines that give each tiered role in RESPONSIVE one alias,
    --layout-<role>: the phone value at :root, then each tier's value from
    its breakpoint up, under @media (min-width) with the breakpoint's
    literal px (CSS cannot read a custom property in a media query). A
    density override reaches the alias through var(). `extra` adds
    declarations per tier to the same blocks (the type styles that step
    down on a phone). Empty when the set lacks a breakpoint, or when it
    lacks every tier of a role and `extra` is empty."""
    extra = extra or {}
    groups = [g for g in RESPONSIVE if all(ts.has(f"layout.{g}.{t}") for t in TIERS)]
    tiers = [t for t in TIERS[1:] if ts.has(f"layout.breakpoint.{t}")]
    if not (groups or any(extra.values())) or len(tiers) != len(TIERS) - 1:
        return []

    def lines(tier: str, indent: str) -> List[str]:
        return [f"{indent}{css_property(f'layout.{g}')}: var({css_property(f'layout.{g}.{tier}')});"
                for g in groups] + [indent + line for line in extra.get(tier, [])]

    out = ["", ":root {", *lines(TIERS[0], "  "), "}"]
    for tier in tiers:
        body = lines(tier, "    ")
        if not body:
            continue
        px = _px(ts, f"layout.breakpoint.{tier}")
        out += ["", f"@media (min-width: {px:g}px) {{", "  :root {", *body, "  }", "}"]
    return out


# Role path -> the token type the checks read; the build's role-types
# check reports any other type once, and the checks below skip it.
ROLE_TYPES: Dict[str, str] = {
    **{f"layout.breakpoint.{t}": "dimension" for t in VIEWPORTS},
    **{f"layout.columns.{t}": "number" for t in TIERS},
    **{f"layout.gutter.{t}": "dimension" for t in TIERS},
    **{f"layout.margin-inline.{t}": "dimension" for t in TIERS},
    **{f"layout.region-gap.{t}": "dimension" for t in TIERS},
    **{f"layout.landing-gap.{t}": "dimension" for t in TIERS},
    **{f"layout.hero.padding-block.{t}": "dimension" for t in TIERS},
    "layout.header.padding-block": "dimension", "layout.footer.padding-block": "dimension",
    "layout.container.max": "dimension",
    **{f"layout.measure.{name}": "dimension" for name in MEASURE_REM},
    "layout.target.min": "dimension",
    "layout.target.large": "dimension",
}
COMPACT = "density:compact"


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _px(ts: TokenSet, path: str, mode: str = "") -> float:
    return dimension_px(ts.resolve(path, mode))


def _number(ts: TokenSet, path: str, mode: str = "") -> Any:
    return ts.resolve(path, mode)


def _repeat(ts: TokenSet, paths: Sequence[str], mode: str,
            read: Callable[[TokenSet, str, str], Any]) -> bool:
    """In compact, a failure whose values all match comfortable is the
    comfortable context's finding and is not repeated."""
    return COMPACT in mode and all(read(ts, p, mode) == read(ts, p, "") for p in paths)


def _where(mode: str) -> str:
    return f" in {COMPACT}" if COMPACT in mode else ""


def _breakpoints(ts: TokenSet, mode: str) -> List[str]:
    present = [f"layout.breakpoint.{t}" for t in TIERS if _typed(ts, f"layout.breakpoint.{t}")]
    out = []
    for a, b in zip(present, present[1:]):
        va, vb, w = _px(ts, a, mode), _px(ts, b, mode), _where(mode)
        if vb <= va and not _repeat(ts, (a, b), mode, _px):
            out.append(f"{b} ({vb:g}px{w}) does not start above {a} ({va:g}px{w}); keep "
                       "breakpoints strictly increasing")
    return out


def _columns(ts: TokenSet, mode: str) -> List[str]:
    present = [f"layout.columns.{t}" for t in TIERS if _typed(ts, f"layout.columns.{t}")]
    out = []
    for a, b in zip(present, present[1:]):
        va, vb, w = _number(ts, a, mode), _number(ts, b, mode), _where(mode)
        if vb < va and not _repeat(ts, (a, b), mode, _number):
            out.append(f"{b} ({vb:g}{w}) has fewer columns than {a} ({va:g}{w}); a wider "
                       "viewport never loses columns")
    return out


def _step_at_least(ts: TokenSet, floor: float, mode: str) -> str:
    """The fix for a short target: the smallest width primitive the set has
    at `floor` px or more, else the smallest such space step, else the
    value itself. Only tokens the set has are named."""
    for family in ("layout.width.", "space."):
        steps = sorted((_px(ts, t.path, mode), t.path) for t in ts.tokens()
                       if t.layer == "primitive" and t.type == "dimension"
                       and t.path.startswith(family) and _px(ts, t.path, mode) >= floor)
        if steps:
            return f"point it at {steps[0][1]} ({steps[0][0]:g}px) or a larger step"
    return f"give it a value of {floor}px or more"


def _target(ts: TokenSet, mode: str, floor: int, asks: str) -> List[str]:
    p = "layout.target.min"
    if not _typed(ts, p) or _px(ts, p, mode) >= floor:
        return []
    return [f"{p} ({mode}) is {_px(ts, p, mode):g}px; {asks}, so "
            f"{_step_at_least(ts, floor, mode)}"]


def _target_minimum(ts: TokenSet, mode: str) -> List[str]:
    return _target(ts, mode, MIN_TARGET_PX, "WCAG 2.5.8 asks for targets of at least "
                   f"{MIN_TARGET_PX} by {MIN_TARGET_PX} CSS px")


def _target_comfortable(ts: TokenSet, mode: str) -> List[str]:
    """2.5.5 does not vary by density; applying it at comfortable density
    only is our choice, and the message says so."""
    if COMPACT in mode:
        return []
    return _target(ts, mode, COMFORTABLE_TARGET_PX, "WCAG 2.5.5 (AAA) asks for targets of at "
                   f"least {COMFORTABLE_TARGET_PX} by {COMFORTABLE_TARGET_PX} CSS px, and we "
                   "apply it at comfortable density")


def _measure(ts: TokenSet, mode: str) -> List[str]:
    p = "layout.measure.text"
    if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
        return []
    rem = _px(ts, p, mode) / 16
    if rem > MAX_TEXT_MEASURE_REM:
        return [f"{p} is {rem:g}rem{_where(mode)}; WCAG 1.4.8 (AAA) keeps lines to 80 "
                f"characters or fewer, and {MAX_TEXT_MEASURE_REM}rem is our approximation of "
                f"that width for body text, so keep it at {MAX_TEXT_MEASURE_REM}rem or less"]
    return []


def _regions(ts: TokenSet, mode: str) -> List[str]:
    """The region gap, the landing gap and the hero padding never shrink as
    the viewport grows, and the landing gap never falls below the region
    gap at its tier."""
    out = []
    for t in TIERS:
        a, b = f"layout.region-gap.{t}", f"layout.landing-gap.{t}"
        if _typed(ts, a) and _typed(ts, b) and _px(ts, b, mode) < _px(ts, a, mode) \
                and not _repeat(ts, (a, b), mode, _px):
            w = _where(mode)
            out.append(f"{b} ({_px(ts, b, mode):g}px{w}) is smaller than {a} "
                       f"({_px(ts, a, mode):g}px{w}); a landing page spaces its sections at "
                       "least as far apart as an app, so point it at a larger space step")
    for group in ("region-gap", "landing-gap", "hero.padding-block"):
        present = [f"layout.{group}.{t}" for t in TIERS if _typed(ts, f"layout.{group}.{t}")]
        for a, b in zip(present, present[1:]):
            va, vb, w = _px(ts, a, mode), _px(ts, b, mode), _where(mode)
            if vb < va and not _repeat(ts, (a, b), mode, _px):
                out.append(f"{b} ({vb:g}px{w}) is smaller than {a} ({va:g}px{w}); a wider "
                           "viewport never tightens the page, so point it at a larger space step")
    return out


def _on_space(ts: TokenSet, mode: str) -> List[str]:
    """Layout roles that take a spacing value (gutters, inline margins,
    region and landing gaps, the hero, header and footer padding) alias
    space.<n> when they alias a primitive, so layout and spacing move
    together."""
    roles = [f"layout.{group}.{tier}" for group in ON_SPACE for tier in TIERS]
    roles += [f"layout.{name}.padding-block" for name in ("header", "footer")]
    out = []
    for role in roles:
        if not _typed(ts, role):
            continue
        target = direct_alias(ts, role, mode)
        if target is not None and not is_step(target, "space."):
            out.append(f"{role} ({mode}) points at {target}, which is not a step of the "
                       "spacing scale; layout spacing comes from space.<n>, so point it at a "
                       "space step")
    return out


# Every check reads the density axis, so a compact override is checked too.
CHECKS: Tuple[Check, ...] = (
    Check("layout-breakpoints", "system", _breakpoints, axes=("density",)),
    Check("layout-columns", "system", _columns, axes=("density",)),
    Check("target-size-minimum", "2.5.8", _target_minimum, axes=("density",)),
    Check("target-size-comfortable", "2.5.5", _target_comfortable, axes=("density",)),
    Check("text-measure", "1.4.8", _measure, axes=("density",)),
    Check("layout-regions", "system", _regions, axes=("density",)),
    Check("layout-on-space", "system", _on_space, axes=("density",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    a = inputs.audience
    return generate_layout(axes, target_px=a.target_px, measure_rem=a.measure_rem,
                           refuse_compact=a.refuse_compact)


FOUNDATION = Foundation(name="layout", generate=_generate, checks=CHECKS, requires=("space",),
                        role_types=ROLE_TYPES)
