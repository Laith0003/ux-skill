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

from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

from engine.foundations import character, space
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
# The gap between the sections of a landing page comes from how calm the
# brief is (character.landing_gap_px, 64 to 240px at desktop, falling with
# energy and rising with formality); the phone takes a share of it
# (character.phone_gap_share) and the tablet and laptop sit a third and two
# thirds of the way up. Never below the region gap at its tier.
LANDING_STEPS = {"phone": 0.0, "tablet": 1 / 3, "laptop": 2 / 3, "desktop": 1.0}
# Header and footer block padding, the same at every width.
HEADER_PADDING, FOOTER_PADDING = (4, 3), (16, 10)
# Tiered roles with a responsive alias in CSS (responsive_css).
RESPONSIVE = ("columns", "gutter", "margin-inline", "region-gap", "landing-gap",
              "hero.padding-block", "landing.margin-inline")
# Tiered roles that alias the spacing scale (layout-on-space).
ON_SPACE = ("gutter", "margin-inline", "region-gap", "landing-gap", "hero.padding-block",
            "landing.margin-inline")
# Untiered roles that alias the spacing scale: the full-width margin and
# how sections meet.
ON_SPACE_ONE = ("layout.margin-inline.full", "layout.seam.overlap", "layout.seam.fade")
COMPACT_FLOOR = 2  # space units, 8px
CONTAINERS = (1120, 1280, 1440)
# A full-width landing page stops growing here and centres beyond it.
FULL_CONTAINER = 1920
# The measures: text and landing from characters of the text face
# (character.reading_measure_ch, landing_measure_ch), form fixed.
MEASURE_REM = {"form": 32}
MEASURES = ("text", "landing", "form")
# Our approximation of the 80 characters WCAG 1.4.8 sets as the widest line.
MAX_TEXT_MEASURE_REM = 40
# Our floor for a reading or landing column, in characters of the text face
# (half an em each when the face is not one we know): narrower, lines
# break every few words.
MIN_MEASURE_CH = 40
# The width of a character when the set's text face is not in the catalog.
DEFAULT_CH_EM = 0.5
# WCAG 1.4.10: content reflows at a 320 CSS px wide viewport.
REFLOW_PX = 320
# Our floor per phone column at the reflow width: room for a 44px target.
MIN_PHONE_COLUMN_PX = 44
# Our floor for a gutter or inline margin, in every density.
MIN_GUTTER_PX = COMPACT_FLOOR * space.BASE_UNIT
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


def full_margin_units(axes: AxisValues) -> int:
    """The full-width landing margin in space units (character.full_margin_px),
    never under the tablet's margin, so margins never shrink as the tier
    widens."""
    return max(space.snap(character.full_margin_px(axes) / space.BASE_UNIT),
               _units(MARGIN["tablet"], axes.density)[0])


def uses_full_width(axes: AxisValues) -> bool:
    """Whether the landing page takes the full-width frame (character.full_width)."""
    return character.full_width(axes) >= 0.5


def landing_margin_units(axes: AxisValues, tier: str) -> int:
    """The landing page's inline margin at a tier, in space units: the page
    margin, or from the laptop up the full-width margin when the page takes
    the full-width frame."""
    if uses_full_width(axes) and tier in ("laptop", "desktop"):
        return full_margin_units(axes)
    return _units(MARGIN[tier], axes.density)[0]


def landing_frame(axes: AxisValues) -> Tuple[Dict[str, float], float]:
    """({tier: inline margin px}, container px) a landing page sets its
    content in: its margins per tier and its container, the full-width one
    when the page takes it."""
    margins = {tier: landing_margin_units(axes, tier) * space.BASE_UNIT for tier in TIERS}
    box = FULL_CONTAINER if uses_full_width(axes) else container_px(axes.density)
    return margins, float(box)


def landing_gap_units(axes: AxisValues) -> Dict[str, int]:
    """{tier: space units} for the gap between landing sections: the
    desktop gap (character.landing_gap_px, raised to the desktop region
    gap first), the phone's share of that (character.phone_gap_share), the
    tiers between at their steps; never below the region gap at its tier
    and never shrinking as the viewport grows."""
    region = _units(REGION_GAP["desktop"], axes.density)[0] * space.BASE_UNIT
    desktop = space.snap(max(character.landing_gap_px(axes), region) / space.BASE_UNIT) \
        * space.BASE_UNIT
    share = character.phone_gap_share(axes)
    lo, hi = character.PHONE_GAP_SHARE
    # the scale step nearest the phone's share that keeps the share in range
    inside = [u for u in space.UNITS if lo * desktop <= u * space.BASE_UNIT <= hi * desktop]
    phone = min(inside or space.UNITS,
                key=lambda u: (abs(u * space.BASE_UNIT - share * desktop), -u)) * space.BASE_UNIT
    out: Dict[str, int] = {}
    below = 0
    for tier in TIERS:
        px = phone + (desktop - phone) * LANDING_STEPS[tier]
        units = space.snap(px / space.BASE_UNIT)
        units = max(units, _units(REGION_GAP[tier], axes.density)[0], below)
        out[tier] = below = units
    return out


def measure_rem(chars: float, face: Any, body_px: int = 16) -> int:
    """A measure of `chars` characters of the text face at body size, in
    whole rem at a 16px root."""
    em = (face.metrics.latin_avg or 0) / face.metrics.upm if face else DEFAULT_CH_EM
    return max(1, int(chars * em * body_px / 16 + 0.5))


def generate_layout(axes: AxisValues, target_px: int = TARGET_PX["comfortable"],
                    long_read: bool = False, refuse_compact: bool = False,
                    body_px: int = 16, book_depth: Optional[float] = None) -> Generated:
    """The page grid and regions. `target_px`, `long_read` and `body_px`
    come from the audience (larger targets for older readers, a few fewer
    characters for long reading, a larger body); the measures are
    characters of the text face at body size (fonts.choose with
    `book_depth`); with `refuse_compact` the compact mode keeps every
    comfortable value."""
    from engine.foundations import fonts
    d = axes.density
    face = fonts.choose(axes, book_depth).text
    measures = {"text": measure_rem(character.reading_measure_ch(axes, long_read), face, body_px),
                "landing": measure_rem(character.landing_measure_ch(axes), face, body_px),
                **MEASURE_REM}
    targets = {"comfortable": target_px,
               "compact": target_px if refuse_compact else TARGET_PX["compact"]}
    ts = TokenSet()
    for px in VIEWPORTS.values():
        ts.add(Token(f"layout.viewport.{px}", "dimension", {"value": px, "unit": "px"}))
    for n in sorted(set(COLUMNS.values())):
        ts.add(Token(f"layout.column-count.{n}", "number", n))
    line = int(character.seam_line(axes) * 2 + 0.5)
    for px in sorted(set(CONTAINERS) | set(TARGET_PX.values()) | set(targets.values())
                     | {targets["comfortable"] + LARGE_EXTRA_PX, FULL_CONTAINER, line}):
        ts.add(Token(f"layout.width.{px}", "dimension", {"value": px, "unit": "px"}))
    for rem in sorted(set(measures.values())):
        ts.add(Token(f"layout.rem.{rem}", "dimension", {"value": rem, "unit": "rem"}))
    # The character the measures count, so a set without type still reads it.
    ts.add(Token("layout.ch-em", "number",
                 round((face.metrics.latin_avg or 0) / face.metrics.upm * body_px / 16, 4)))

    for tier, px in VIEWPORTS.items():
        ts.add(Token(f"layout.breakpoint.{tier}", "dimension", "{layout.viewport.%d}" % px,
                     layer="semantic"))
    for tier in TIERS:
        ts.add(Token(f"layout.columns.{tier}", "number",
                     "{layout.column-count.%d}" % COLUMNS[tier], layer="semantic"))
    landing = landing_gap_units(axes)
    full = full_margin_units(axes)
    for group, table in (("gutter", GUTTER), ("margin-inline", MARGIN),
                         ("region-gap", REGION_GAP), ("landing-gap", None),
                         ("hero.padding-block", HERO_PADDING), ("landing.margin-inline", MARGIN)):
        for tier in TIERS:
            if group == "landing-gap":
                comfortable = landing[tier]
                compact = max(space.compact_step(comfortable, COMPACT_FLOOR),
                              _units(REGION_GAP[tier], d)[1])
            elif group == "landing.margin-inline" and uses_full_width(axes) \
                    and tier in ("laptop", "desktop"):
                comfortable = compact = full
            else:
                comfortable, compact = _units(table[tier], d)
            compact = comfortable if refuse_compact else compact
            modes = {"density:compact": "{space.%d}" % compact} if compact != comfortable else {}
            ts.add(Token(f"layout.{group}.{tier}", "dimension", "{space.%d}" % comfortable,
                         modes=modes, layer="semantic"))
        if group == "margin-inline":
            ts.add(Token("layout.margin-inline.full", "dimension", "{space.%d}" % full,
                         layer="semantic"))
    ts.add(Token("layout.landing.max-width", "dimension", "{layout.width.%d}" % (
        FULL_CONTAINER if uses_full_width(axes) else container_px(d)), layer="semantic"))
    for name, pair in (("header", HEADER_PADDING), ("footer", FOOTER_PADDING)):
        comfortable, compact = _units(pair, d)
        compact = comfortable if refuse_compact else compact
        modes = {"density:compact": "{space.%d}" % compact} if compact != comfortable else {}
        ts.add(Token(f"layout.{name}.padding-block", "dimension", "{space.%d}" % comfortable,
                     modes=modes, layer="semantic"))
    ts.add(Token("layout.container.max", "dimension", "{layout.width.%d}" % container_px(d),
                 layer="semantic"))
    ts.add(Token("layout.container.full", "dimension", "{layout.width.%d}" % FULL_CONTAINER,
                 layer="semantic"))
    for name, px in (("overlap", character.seam_overlap_px(axes)),
                     ("fade", character.seam_fade_px(axes))):
        ts.add(Token(f"layout.seam.{name}", "dimension",
                     "{space.%d}" % space.snap(px / space.BASE_UNIT), layer="semantic"))
    ts.add(Token("layout.seam.line", "dimension", "{layout.width.%d}" % line, layer="semantic"))
    for name in MEASURES:
        ts.add(Token(f"layout.measure.{name}", "dimension", "{layout.rem.%d}" % measures[name],
                     layer="semantic"))
    ts.add(Token("layout.target.min", "dimension", "{layout.width.%d}" % targets["comfortable"],
                 modes={} if targets["compact"] == targets["comfortable"] else
                 {"density:compact": "{layout.width.%d}" % targets["compact"]},
                 layer="semantic"))
    ts.add(Token("layout.target.large", "dimension",
                 "{layout.width.%d}" % (targets["comfortable"] + LARGE_EXTRA_PX),
                 layer="semantic"))
    frame = ("full width, " + str(full * space.BASE_UNIT) + "px margins"
             if uses_full_width(axes) else f"{container_px(d)}px container")
    return Generated(tokens=ts, notes=[
        f"layout: container {container_px(d)}px, landing page {frame}, landing gap "
        f"{landing['desktop'] * space.BASE_UNIT}px at desktop and "
        f"{landing['phone'] * space.BASE_UNIT}px on a phone, measures "
        f"{measures['landing']}rem for landing copy and {measures['text']}rem for reading"])


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
    **{f"layout.landing.margin-inline.{t}": "dimension" for t in TIERS},
    "layout.margin-inline.full": "dimension", "layout.container.full": "dimension",
    "layout.landing.max-width": "dimension", "layout.seam.overlap": "dimension",
    "layout.seam.fade": "dimension", "layout.seam.line": "dimension",
    **{f"layout.hero.padding-block.{t}": "dimension" for t in TIERS},
    "layout.header.padding-block": "dimension", "layout.footer.padding-block": "dimension",
    "layout.container.max": "dimension",
    **{f"layout.measure.{name}": "dimension" for name in MEASURES},
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


def _step_at_least(ts: TokenSet, floor: float, mode: str,
                   families: Sequence[str] = ("layout.width.", "space.")) -> str:
    """The fix for a value under `floor`: the smallest primitive of the
    first family that has one at `floor` px or more, else the value itself.
    Only tokens the set has are named."""
    for family in families:
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


def _grid_order(ts: TokenSet, mode: str) -> List[str]:
    """Gutters and inline margins never shrink as the tier widens."""
    out = []
    for group in ("gutter", "margin-inline", "landing.margin-inline"):
        present = [f"layout.{group}.{t}" for t in TIERS if _typed(ts, f"layout.{group}.{t}")]
        for a, b in zip(present, present[1:]):
            va, vb, w = _px(ts, a, mode), _px(ts, b, mode), _where(mode)
            if vb < va and not _repeat(ts, (a, b), mode, _px):
                out.append(f"{b} ({vb:g}px{w}) is narrower than {a} ({va:g}px{w}); a wider "
                           "viewport never gets a smaller gutter or inline margin, so point "
                           f"{b} at a step of {va:g}px or more")
    return out


def _gutter_floor(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for group in ("gutter", "margin-inline", "landing.margin-inline"):
        for tier in TIERS:
            p = f"layout.{group}.{tier}"
            if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
                continue
            v = _px(ts, p, mode)
            if v < MIN_GUTTER_PX:
                out.append(f"{p} ({mode}) is {v:g}px; our floor for a gutter or inline margin "
                           f"is {MIN_GUTTER_PX}px in every density, so "
                           f"{_step_at_least(ts, MIN_GUTTER_PX, mode, ('space.',))}")
    return out


def _reflow(ts: TokenSet, mode: str) -> List[str]:
    """The first breakpoint sits above the reflow width, so a 320px
    viewport gets the phone grid."""
    p = "layout.breakpoint.tablet"
    if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
        return []
    v = _px(ts, p, mode)
    if v > REFLOW_PX:
        return []
    return [f"{p} is {v:g}px{_where(mode)}, so a {REFLOW_PX}px viewport gets the tablet grid; "
            f"WCAG 1.4.10 asks that content reflow at {REFLOW_PX} CSS px, so start the tablet "
            f"tier above {REFLOW_PX}px"]


def _phone_columns(ts: TokenSet, mode: str) -> List[str]:
    """At the reflow width, the phone margins and gutters leave each column
    room for a comfortable target."""
    m, g, c = "layout.margin-inline.phone", "layout.gutter.phone", "layout.columns.phone"
    if not all(_typed(ts, p) for p in (m, g, c)) or _repeat(ts, (m, g), mode, _px):
        return []
    margin, gutter, cols = _px(ts, m, mode), _px(ts, g, mode), _number(ts, c, mode)
    if cols < 1:
        return []
    each = (REFLOW_PX - 2 * margin - (cols - 1) * gutter) / cols
    if each >= MIN_PHONE_COLUMN_PX:
        return []
    return [f"at {REFLOW_PX}px the phone grid leaves {each:g}px per column (two {m} of "
            f"{margin:g}px and {cols - 1:g} {g} of {gutter:g}px beside {cols:g} columns"
            f"{_where(mode)}); our floor is {MIN_PHONE_COLUMN_PX}px per column so a column can "
            "hold a comfortable target, so narrow the phone margins or gutters"]


def _ch_px(ts: TokenSet) -> Tuple[float, str]:
    """(the width of one character of body text in px, how it was read):
    the text face's average advance at the body size when the set names a
    face in the catalog, else layout.ch-em (the character the build
    counted, in rem) when the set has it, else DEFAULT_CH_EM at 16px."""
    from engine.foundations import fonts
    body = 16.0
    if not ts.has("type.face.text") and ts.has("layout.ch-em") \
            and ts.get("layout.ch-em").type == "number":
        return float(ts.resolve("layout.ch-em")) * 16, "the text face the build counted"
    if ts.has("type.text.body") and ts.get("type.text.body").type == "typography":
        body = dimension_px(ts.resolve("type.text.body")["fontSize"])
    face = None
    if ts.has("type.face.text") and ts.get("type.face.text").type == "fontFamily":
        family = ts.resolve("type.face.text")
        face = fonts.BY_FAMILY.get(family[0] if isinstance(family, list) else family)
    if face is None or not face.metrics.latin_avg:
        return DEFAULT_CH_EM * body, f"half an em at {body:g}px"
    return face.metrics.latin_avg / face.metrics.upm * body, f"{face.family} at {body:g}px"


def _measure_floor(ts: TokenSet, mode: str) -> List[str]:
    """The reading and landing measures hold at least MIN_MEASURE_CH
    characters of the text face."""
    out = []
    for p in ("layout.measure.text", "layout.measure.landing"):
        if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
            continue
        ch, how = _ch_px(ts)
        chars = _px(ts, p, mode) / ch
        if chars + 1e-9 >= MIN_MEASURE_CH:
            continue
        need = int(MIN_MEASURE_CH * ch / 16 + 0.999)
        out.append(f"{p} is {_px(ts, p, mode) / 16:g}rem{_where(mode)}, {chars:.0f} characters "
                   f"of {how}; below our floor of {MIN_MEASURE_CH} characters a column breaks "
                   f"lines every few words, so keep it at {need}rem or more")
    return out


def _form_measure(ts: TokenSet, mode: str) -> List[str]:
    p = "layout.measure.form"
    if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
        return []
    rem = _px(ts, p, mode) / 16
    if rem <= MAX_TEXT_MEASURE_REM:
        return []
    return [f"{p} is {rem:g}rem{_where(mode)}; a form wider than the reading measure is read "
            f"like a long line, so keep it at {MAX_TEXT_MEASURE_REM}rem or less, our ceiling "
            "for a reading width"]


def _container(ts: TokenSet, mode: str) -> List[str]:
    p = "layout.container.max"
    if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
        return []
    v, out = _px(ts, p, mode), []
    if v < REFLOW_PX:
        out.append(f"{p} is {v:g}px{_where(mode)}, narrower than the {REFLOW_PX}px reflow "
                   f"width; point it at a width of {REFLOW_PX}px or more")
    text = "layout.measure.text"
    for box in (p, "layout.landing.max-width"):
        if box != p and (not _typed(ts, box) or _repeat(ts, (box,), mode, _px)):
            continue
        v = _px(ts, box, mode)
        if _typed(ts, text) and v < _px(ts, text, mode):
            need = _px(ts, text, mode)
            out.append(f"{box} is {v:g}px{_where(mode)}, narrower than {text} ({need:g}px), so "
                       f"a reading column would not fit; point it at a width of {need:g}px or "
                       "more")
    return out


def _on_space(ts: TokenSet, mode: str) -> List[str]:
    """Layout roles that take a spacing value (gutters, inline margins,
    region and landing gaps, the hero, header and footer padding) alias
    space.<n> when they alias a primitive, so layout and spacing move
    together."""
    roles = [f"layout.{group}.{tier}" for group in ON_SPACE for tier in TIERS]
    roles += [f"layout.{name}.padding-block" for name in ("header", "footer")]
    roles += list(ON_SPACE_ONE)
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
    Check("layout-grid-order", "system", _grid_order, axes=("density",)),
    Check("layout-gutter-floor", "system", _gutter_floor, axes=("density",)),
    Check("reflow-phone-tier", "1.4.10", _reflow, axes=("density",)),
    Check("phone-columns", "system", _phone_columns, axes=("density",)),
    Check("text-measure-floor", "system", _measure_floor, axes=("density",)),
    Check("form-measure", "system", _form_measure, axes=("density",)),
    Check("container-bounds", "system", _container, axes=("density",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    a = inputs.audience
    return generate_layout(axes, target_px=a.target_px,
                           long_read=a.reading_context == "long-read",
                           refuse_compact=a.refuse_compact, body_px=a.body_px,
                           book_depth=a.book_depth)


FOUNDATION = Foundation(name="layout", generate=_generate, checks=CHECKS, requires=("space",),
                        role_types=ROLE_TYPES)
