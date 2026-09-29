"""Typography foundation: three faces (display, text, mono) with their
Arabic partners, a size scale in rem, weights and letter spacing that vary
along the scale, line heights, text roles as DTCG typography composites,
icon sizes and stroke, and an Arabic variant under dir="rtl".

fonts.choose picks the faces from the axes. The contrast axis sets the
scale ratio (density tightens it); the display weight comes from contrast
and formality and eases toward the text face's heading weight down the
scale; letter spacing tightens toward the largest sizes by the contrast
and formality axes, and small labels open up. Under high contrast every
style set in the text or mono face is one weight heavier. Under dir="rtl"
every style but code switches to the Arabic face (the display
styles to the Arabic display face) at a size larger by the ratio the two
faces' metrics give (fonts.arabic_scale), with taller lines and no letter
spacing, which would break the joins between Arabic letters. Sizes are
rem so they follow the reader's default text size.

Checks: body and fine print keep minimum sizes in both directions;
running text keeps line height 1.5 or more (WCAG 1.4.8) and never
tightens its letters; the Arabic rules above; sizes in rem; falling sizes
from hero to body; high contrast never lightens a style; icon sizes rise
and the stroke stays readable. A role of another type than ROLE_TYPES
names is reported once by the build's role-types check and skipped here.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations import character, fonts
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.modes import compress
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.foundations.values import dimension_px
from engine.synthesizer.axes import AxisValues

STEPS = tuple(range(1, 11))
BODY_STEP = 3
# The landing display step: the headline of a landing page, above the hero
# by a size from expressiveness (character.landing_display_px), not by the
# ratio, so a landing page reads as one in a quiet system too.
DISPLAY_STEP = 10
BODY_PX = 16
# role -> (size step, face, weight kind, leading index, tracking kind).
# Faces: display, text, mono, label (the mono face for a technical system,
# else the text face). Weight kinds: display (eases along the scale),
# emphasis (the display weight less the emphasis gap), heading, regular,
# medium. Leading index 0 is the display leading at the style's own size
# (display_leading); 1 to 3 are fixed. Tracking kinds: scale (tightens
# with size), caps (0 or open, for capitals), label (opens up), none.
ROLES: Dict[str, Tuple[Any, str, str, int, str]] = {
    "type.text.display": (DISPLAY_STEP, "display", "display", 0, "scale"),
    # The display set in capitals: the same size, weight and leading, with
    # letter spacing at 0 or open, since capitals already sit close.
    "type.text.display-caps": (DISPLAY_STEP, "display", "display", 0, "caps"),
    # The emphasised words of a two-voice headline: the display at a
    # lighter weight (character.emphasis_contrast).
    "type.text.display-emphasis": (DISPLAY_STEP, "display", "emphasis", 0, "scale"),
    "type.text.hero": (9, "display", "display", 0, "scale"),
    "type.text.heading-1": (8, "display", "display", 0, "scale"),
    "type.text.section-title": (7, "display", "display", 1, "scale"),
    # A proof number reads at the page title's size, so a band of three or
    # four of them holds a section.
    "type.text.figure": (8, "display", "display", 0, "scale"),
    "type.text.heading-2": (5, "text", "heading", 1, "scale"),
    "type.text.heading-3": (4, "text", "heading", 2, "none"),
    "type.text.body": (3, "text", "regular", 3, "none"),
    "type.text.body-small": (2, "text", "regular", 3, "none"),
    "type.text.ui": ("ui", "text", "medium", 2, "none"),
    "type.text.ui-large": (3, "text", "medium", 2, "none"),
    "type.text.label": (2, "label", "medium", 2, "label"),
    "type.text.fine": (1, "text", "regular", 3, "none"),
    "type.text.code": (2, "mono", "regular", 3, "none"),
}
READING = ("type.text.body", "type.text.body-small", "type.text.fine")
# How each role's lines break: headlines and headings balance their lines,
# running text avoids a last line of one word. tokens.css writes it as
# --<role>-text-wrap in the root block of its viewport layer, beside the
# phone factors (responsive_lines), since it is derived from the role.
WRAP = {**{r: "balance" for r, spec in ROLES.items() if spec[1] == "display"},
        "type.text.heading-2": "balance", "type.text.heading-3": "balance",
        **{r: "pretty" for r in READING}}
# Roles that keep the reading line height: running text and code blocks.
LEADING_ROLES = READING + ("type.text.code",)
# Roles that never tighten their letters: running text and labels.
TRACKING_ROLES = READING + ("type.text.ui",)
HIERARCHY = ("type.text.display", "type.text.hero", "type.text.heading-1", "type.text.section-title",
             "type.text.heading-2", "type.text.heading-3", "type.text.body")
MIN_BODY_PX, MIN_FINE_PX, MIN_READING_LEADING = 16, 12, 1.5
# Display leading: DISPLAY_LEAD[0] at DISPLAY_LEAD_PX[0] and below, falling
# on a log scale of size to DISPLAY_LEAD[1] (contrast 0) or DISPLAY_LEAD[2]
# (contrast 1) at DISPLAY_LEAD_PX[1] and above, never below the face's ink
# clearance (clearance). Measured award headlines sit at 1.0 or tighter.
DISPLAY_LEAD = (1.12, 1.0, 0.92)
DISPLAY_LEAD_PX = (40.0, 160.0)
# Our gap between a descender and the ascender of the line below it, in em,
# so two display lines never touch.
INK_GAP = 0.02
# Our floor for any display-face style's line height; every other style
# keeps a line height above 1.
MIN_DISPLAY_LEADING = 0.88
# Arabic line heights sit this far above the Latin ones, and a display
# style's at least ARABIC_DISPLAY_GAP above, for the marks above and below.
ARABIC_LEAD_EXTRA = 0.2
ARABIC_DISPLAY_GAP = 0.15
# Our floor between neighbouring levels of HIERARCHY: a smaller step does
# not read as a new level. The generator holds every step from body up to
# it after rounding, in both scripts.
MIN_LEVEL_RATIO = 1.08
MONOSPACE = ("monospace", "ui-monospace")
# Under high contrast, bold words stay at least this far above body text.
STRONG_GAP = 200
# Face roles: the token each face is written to.
FACE_TOKENS = {"display": "type.face.display", "text": "type.face.text",
               "mono": "type.face.mono", "arabic": "type.face.arabic",
               "arabic-display": "type.face.arabic-display"}
ARABIC_FACE = "type.face.arabic"
ARABIC_DISPLAY_FACE = "type.face.arabic-display"
# The one style that keeps its Latin face under rtl: code, whose Arabic
# comments and strings still read in the mono face. A label set in the mono
# face switches to the Arabic face like any other text.
KEEP_FACE = ("type.text.code",)
# A technical system sets labels in the mono face.
MONO_LABEL_FROM = 0.5
# Icon sizes: inline follows body text, control sits in a control, feature
# grows with the contrast axis.
ICON_CONTROL_REM = 1.25
ICON_STROKE_RANGE = (1.0, 3.0)
# The styles that step down on a phone (every width below the tablet
# breakpoint): the four largest display styles. Each takes a factor on its
# size: the display's from character.phone_display_px, the others' from a
# phone scale whose ratio is PHONE_RATIO_SHARE of the way from 1 to the
# system's ratio, so a bold system still steps harder than a quiet one;
# each phone size stays at least 1px above the style below it, in the
# Latin and the Arabic sizes (hold_phone_order), and never above its own
# size. tokens.css multiplies the style's size and letter spacing by
# --<style>-scale, the factor on a phone and the tier's fit factor from
# the tablet breakpoint up, so a page reads one property.
PHONE_ROLES = ("type.text.display", "type.text.hero", "type.text.heading-1",
               "type.text.section-title")
PHONE_RATIO_SHARE = 0.6
PHONE_FLOOR_ROLE = "type.text.heading-2"
# Styles that share another's step take its factors at every width: the
# figure steps down with heading-1, so it never outranks the headline, and
# the capitals and emphasis voices of the display go with the display.
FOLLOWS = {"type.text.figure": "type.text.heading-1",
           "type.text.display-caps": "type.text.display",
           "type.text.display-emphasis": "type.text.display"}
# From the tablet breakpoint up each style in PHONE_ROLES takes a fit factor
# per tier: at most 1, and small enough that the page's longest headline
# word (FIT_WORD letters when the brief does not give it) fits the
# headline's column, measured with the face's own average advance (Latin
# and Arabic), each style still MIN_LEVEL_RATIO above the next, and never
# smaller on a wider tier. The column is the page's content width (its
# width less both landing margins, within the landing container), all of
# it on a phone and a tablet and, from the laptop up, the columns of
# twelve the composition sets the headline in (HEADLINE_COLUMNS).
FIT_TIERS = ("tablet", "laptop", "desktop")
FIT_WORD = {"latin": 13, "arabic": 10}
HEADLINE_COLUMNS = {"split": 7, "stacked": 12, "bento": 12, "editorial-column": 8,
                    "full-bleed-media": 12}
GRID_COLUMNS = 12
# Each tier's narrowest and widest width in px; the phone starts at the
# reflow width, and the desktop tier has no end.
TIER_WIDTHS: Dict[str, Tuple[int, Optional[int]]] = {
    "phone": (320, 639), "tablet": (640, 1023), "laptop": (1024, 1279), "desktop": (1280, None)}
# The display grows with the viewport: its size at REFERENCE_WIDTH is the
# size token, and below it the size follows the width in vw (the fluid
# roles, FLUID), never above the tier's fit factor and never below 1px
# over the hero, so the headline scales between the laptop and the
# reference width and a long word still fits a small phone.
REFERENCE_WIDTH = 1440
FLUID = ("type.text.display",)
# What rounding the fluid size to two places can take off the display at a
# tier's narrowest width, in px, kept spare under the hero.
ROUNDING_PX = 0.2
def phone_token(role: str) -> str:
    """The factor token of a style that steps down on a phone."""
    return "type.phone." + role.rsplit(".", 1)[1]


def fit_token(role: str, tier: str) -> str:
    """The fit factor token of a style that steps by tier."""
    return f"type.fit.{role.rsplit('.', 1)[1]}.{tier}"


def fluid_token(tier: str) -> str:
    """The token holding the display's fluid size at a tier, in vw."""
    return f"type.fluid.display.{tier}"


@dataclass(frozen=True)
class Frame:
    """What the headline sets in at each tier: the inline margin and the
    container in px, and the columns of twelve it spans from the laptop up."""
    margins: Mapping[str, float]
    container: float
    columns: int

    def content(self, tier: str, width: float) -> float:
        """The content width at `width` px inside `tier`."""
        return min(width - 2 * self.margins[tier], self.container)

    def column(self, tier: str, width: float) -> float:
        """The headline's column at `width` px inside `tier`: all of the
        content on a phone and a tablet, its columns of twelve from the
        laptop up."""
        share = 1.0 if tier in ("phone", "tablet") else self.columns / GRID_COLUMNS
        return self.content(tier, width) * share


def headline_columns(axes: AxisValues, audience: Any = None) -> int:
    """The columns of twelve the landing headline spans: its composition's
    (composition.choose)."""
    from engine.foundations import composition
    from engine.foundations.audience import Audience
    return HEADLINE_COLUMNS[composition.choose(axes, audience or Audience()).name]


def frame_of(axes: AxisValues, columns: int = GRID_COLUMNS) -> Frame:
    """The landing page's frame at these axes: the layout's landing margins
    and container (layout.landing_frame)."""
    from engine.foundations import layout
    margins, container = layout.landing_frame(axes)
    return Frame(margins, container, columns)


def word_em(face: fonts.Face, script: str, letters: float) -> float:
    """The width of a word of `letters` letters in `script` set in `face`,
    in em."""
    avg = face.metrics.arabic_avg if script == "arabic" else face.metrics.latin_avg
    return letters * (avg or 0) / face.metrics.upm


def word_px(face: fonts.Face, px: float, script: str, letters: Optional[float] = None) -> float:
    """The width of a word in `script` (FIT_WORD letters unless `letters`)
    set in `face` at `px`."""
    return word_em(face, script, FIT_WORD[script] if letters is None else letters) * px


def _fits(scripts: Sequence[Tuple[str, List[int], fonts.Face, float]], column: float,
          step: int) -> float:
    """The largest factor on step `step`'s size at which the word fits
    `column` px in every script, at most 1."""
    return min([1.0] + [column / (word_em(face, script, letters) * sizes[step - 1])
                        for script, sizes, face, letters in scripts])


def _floor4(f: float) -> float:
    return int(f * 10000) / 10000


def tier_factors(axes: AxisValues, choice: fonts.Choice, latin: List[int],
                 arabic: Optional[List[int]], frame: Optional[Frame] = None,
                 words: Optional[Mapping[str, float]] = None,
                 script: str = "latin") -> Dict[str, Dict[str, float]]:
    """{tier: {role: factor}} for PHONE_ROLES from the tablet up (FIT_TIERS)
    in one script, each rounded down to four places, so a wide Arabic face
    never shrinks the Latin headline. The hero, heading-1 and section-title
    fit the word at the tier's narrowest width, the hero with room for the
    display MIN_LEVEL_RATIO above it; each keeps MIN_LEVEL_RATIO over the
    next. The display's factor is its ceiling: the word fits at the tier's
    widest column, and the fluid size (fluid_vw) takes it below that."""
    frame = frame or frame_of(axes)
    one = [row for row in _scripts(choice, latin, arabic, words) if row[0] == script]
    sizes = one[0][1]
    out: Dict[str, Dict[str, float]] = {}
    for tier in FIT_TIERS:
        low, high = TIER_WIDTHS[tier]
        narrow = frame.column(tier, low)
        wide = frame.column(tier, high if high else 10 ** 6)
        row: Dict[str, float] = {}
        above = None
        for role in PHONE_ROLES[1:]:
            n = ROLES[role][0]
            f = _fits(one, narrow, n)
            if role == "type.text.hero":
                # room for the display MIN_LEVEL_RATIO above it, which must fit
                # too, with ROUNDING_PX spare for the fluid size's two places
                f = min(f, _hero_room(one, narrow, extra=ROUNDING_PX))
            if above is not None:
                f = min(f, above / (MIN_LEVEL_RATIO * sizes[n - 1]))
            row[role] = _floor4(min(1.0, f))
            above = sizes[n - 1] * row[role]
        hero = sizes[ROLES["type.text.hero"][0] - 1] * row["type.text.hero"]
        need = min(1.0, hero * MIN_LEVEL_RATIO / sizes[DISPLAY_STEP - 1])
        row["type.text.display"] = _floor4(max(_fits(one, wide, DISPLAY_STEP), need))
        out[tier] = {role: row[role] for role in PHONE_ROLES}
    for wide, narrow in zip(reversed(FIT_TIERS), list(reversed(FIT_TIERS))[1:]):
        for role in PHONE_ROLES:
            out[narrow][role] = min(out[narrow][role], out[wide][role])
    return out


def _hero_room(scripts: Sequence[Tuple[str, List[int], fonts.Face, float]],
               column: float, level: float = MIN_LEVEL_RATIO, extra: float = 0.0) -> float:
    """The largest factor on the hero at which a display `level` times it
    plus `extra` px still fits the word in `column` px, in every script."""
    n = ROLES["type.text.hero"][0]
    return min((column / word_em(face, script, letters) / level - extra) / sizes[n - 1]
               for script, sizes, face, letters in scripts)


Script = Tuple[str, List[int], fonts.Face, float]


def _scripts(choice: fonts.Choice, latin: List[int], arabic: Optional[List[int]],
             words: Optional[Mapping[str, float]]) -> List[Script]:
    """(script, sizes, display face, word letters) for every script the
    system sets."""
    words = dict(FIT_WORD, **(words or {}))
    out = [("latin", latin, choice.display, float(words["latin"]))]
    if arabic is not None:
        out.append(("arabic", arabic, choice.arabic_display, float(words["arabic"])))
    return out


def fluid_vw(axes: AxisValues, choice: fonts.Choice, latin: List[int],
             arabic: Optional[List[int]], factors: Mapping[str, Mapping[str, float]],
             frame: Optional[Frame] = None, words: Optional[Mapping[str, float]] = None,
             script: str = "latin") -> Dict[str, float]:
    """{tier: vw} the display's fluid size in one script: the largest share
    of the viewport at which the word still fits the column at the tier's
    narrowest width (the column grows at least as fast as the width up to
    the container), and from the laptop up no more than the display's size
    at REFERENCE_WIDTH (so the headline scales with the width up to there),
    nor less than MIN_LEVEL_RATIO over the hero at the tier's narrowest
    width, where the word allows. `factors` is {tier: {role: factor}} in the
    same script, the phone included."""
    frame = frame or frame_of(axes)
    _, sizes, face, letters = next(r for r in _scripts(choice, latin, arabic, words)
                                   if r[0] == script)
    hero_n = ROLES["type.text.hero"][0]
    out = {}
    for tier, (low, _) in TIER_WIDTHS.items():
        v = frame.column(tier, low) / word_em(face, script, letters) / low * 100
        if tier in ("laptop", "desktop"):
            reference = sizes[DISPLAY_STEP - 1] / REFERENCE_WIDTH * 100
            order = (sizes[hero_n - 1] * factors[tier]["type.text.hero"] * MIN_LEVEL_RATIO
                     + ROUNDING_PX) / low * 100
            v = min(v, max(reference, order))
        out[tier] = int(v * 100) / 100
    return out


def phone_px(axes: AxisValues, latin: List[int], body: int = BODY_PX) -> Dict[str, int]:
    """The phone size in px of each style in PHONE_ROLES: the display's from
    its desktop size (character.phone_display_for), the others the
    phone scale's size at their step; each at least 1px above the style
    below it on the phone (heading-2 at its own size for the lowest) and at
    most its own size."""
    r = 1 + (ratio(axes) - 1) * PHONE_RATIO_SHARE
    floor = latin[ROLES[PHONE_FLOOR_ROLE][0] - 1]
    out: Dict[str, int] = {}
    for role in reversed(PHONE_ROLES):
        n = ROLES[role][0]
        want = character.phone_display_for(latin[n - 1]) if n == DISPLAY_STEP \
            else body * r ** (n - BODY_STEP)
        px = min(latin[n - 1], max(int(want + 0.5), floor + 1))
        out[role] = floor = px
    return out


def hold_phone_order(start: Dict[str, float], scripts: List[List[float]]) -> Dict[str, float]:
    """The phone factor of each style in PHONE_ROLES, rounded to four
    places: from the lowest up, the smallest factor at or above `start`
    that keeps the style at least 1px above the phone size of the style
    below it (heading-2 at its own size for the lowest) in every script in
    `scripts` (one size list per script, steps 1..10), at most 1.

    A style at its own size that still cannot clear the style below in a
    script keeps factor 1, and the styles below it come down instead, each
    to 1px under the one above. That fallback does not check heading-2
    again, so on a scale too compressed to hold the order a style can end
    at heading-2's size; the phone-hierarchy gate check then names that
    order, and the build refuses it. Scales whose steps rise by whole pixels
    never get there, since a style's size is then at least 1px above the
    next style's size, and so above its phone size. Rounding to four
    places moves a phone size by at most half of 1e-4 of the size, so two
    neighbours 1px apart stay more than 0.98px apart under 200px."""
    below = [s[ROLES[PHONE_FLOOR_ROLE][0] - 1] for s in scripts]
    exact: Dict[str, float] = {}
    capped = False
    for role in reversed(PHONE_ROLES):
        sizes = [s[ROLES[role][0] - 1] for s in scripts]
        need = max((b + 1) / size for b, size in zip(below, sizes))
        capped = capped or need > 1
        exact[role] = min(1.0, max(start[role], need))
        below = [size * exact[role] for size in sizes]
    if capped:
        for role, lower in zip(PHONE_ROLES, PHONE_ROLES[1:]):
            n, m = ROLES[role][0], ROLES[lower][0]
            exact[lower] = min(exact[lower], min((s[n - 1] * exact[role] - 1) / s[m - 1]
                                                 for s in scripts))
    return {role: round(f, 4) for role, f in exact.items()}


def phone_factors(axes: AxisValues, latin: List[int], body: int = BODY_PX,
                  arabic: Optional[List[int]] = None, choice: Optional[fonts.Choice] = None,
                  frame: Optional[Frame] = None,
                  words: Optional[Mapping[str, float]] = None) -> Dict[str, float]:
    """The phone factor of each style in PHONE_ROLES: the Latin phone size
    (phone_px) over the style's size, raised where the Arabic sizes, which
    round per step, would otherwise leave a style less than 1px above the
    one below it on a phone (hold_phone_order). With the faces, the hero
    then comes down, and the styles under it with it, until a display 1px
    above it still fits the word at the reflow width in every script, since
    the fluid display (fluid_vw) never falls below that."""
    px = phone_px(axes, latin, body)
    start = {role: px[role] / latin[ROLES[role][0] - 1] for role in PHONE_ROLES}
    scripts_sizes = [latin] + ([arabic] if arabic is not None else [])
    held = hold_phone_order(start, scripts_sizes)
    if choice is None:
        return held
    frame = frame or frame_of(axes)
    col = frame.column("phone", TIER_WIDTHS["phone"][0])
    room = _hero_room(_scripts(choice, latin, arabic, words), col, level=1.0, extra=1.0)
    if held["type.text.hero"] <= room:
        return held
    # The least factors that keep the phone order: a scale too tight for the
    # word at 320px keeps its order, and the display may then run past a
    # 320px screen by the rest (fit_problems measures only the fluid size).
    least = hold_phone_order({role: 0.0 for role in PHONE_ROLES}, scripts_sizes)
    capped = dict(held)
    prev = None
    for role in PHONE_ROLES[1:]:
        n = ROLES[role][0]
        if prev is None:
            cap = room
        else:
            pn = ROLES[prev][0]
            cap = min((sz[pn - 1] * capped[prev] - 1) / sz[n - 1] for sz in scripts_sizes)
        capped[role] = min(capped[role], max(least[role], int(cap * 10000) / 10000))
        prev = role
    return capped


# Run roles: the face a run in the other script takes inside a paragraph.
RUNS = {"type.run.latin": "type.face.text", "type.run.arabic": ARABIC_FACE}
ROLE_TYPES: Dict[str, str] = {
    **{token: "fontFamily" for token in FACE_TOKENS.values()},
    **{role: "typography" for role in ROLES},
    "type.strong": "fontWeight",
    **{run: "fontFamily" for run in RUNS},
    "type.icon.size.inline": "dimension", "type.icon.size.control": "dimension",
    "type.icon.size.feature": "dimension", "type.icon.stroke": "number",
    **{phone_token(role): "number" for role in PHONE_ROLES + tuple(FOLLOWS)},
    **{fit_token(role, tier): "number" for role in PHONE_ROLES for tier in FIT_TIERS},
    **{fluid_token(tier): "number" for tier in TIER_WIDTHS},
    "type.emphasis.tone": "number", "type.emphasis.italic": "number",
}


def ratio(axes: AxisValues) -> float:
    return character.scale_ratio(axes)


def _clear_level(px: int, below: int) -> int:
    """px raised by whole pixels until it sits MIN_LEVEL_RATIO above the
    step below it."""
    while px / below < MIN_LEVEL_RATIO:
        px += 1
    return px


def latin_px(axes: AxisValues, body: int = BODY_PX) -> List[int]:
    """Sizes in px for steps 1..10: body minus 4, body minus 2, body, then
    the ratio upward to the hero at step 9, and the landing display at step
    10 (character.landing_display_px, scaled with the body size), each step
    at least MIN_LEVEL_RATIO above the one below after rounding."""
    r = ratio(axes)
    out = [body - 4, body - 2, body]
    for n in STEPS[3:]:
        if n == DISPLAY_STEP:
            want = int(character.landing_display_px(axes) * body / BODY_PX + 0.5)
        else:
            want = int(body * r ** (n - BODY_STEP) + 0.5)
        out.append(_clear_level(want, out[-1]))
    return out


def arabic_px(latin: List[int], scale: float) -> List[int]:
    """The Arabic size at each step: the Latin size times the scale the
    two faces' metrics give, at least one pixel larger, and from body up
    at least MIN_LEVEL_RATIO above the step below."""
    out: List[int] = []
    for i, px in enumerate(latin):
        size = max(px + 1, int(px * scale + 0.5))
        out.append(_clear_level(size, out[-1]) if i >= BODY_STEP else size)
    return out


def leading(axes: AxisValues, extra: float = 0.0) -> Dict[int, float]:
    """The fixed line heights, 1 to 3: reading lines open as density
    falls, and more for long reading (`extra`). The display leading (0)
    depends on each style's size (display_leading)."""
    return {1: 1.2, 2: 1.3, 3: round(1.5 + 0.1 * (1 - axes.density) + extra, 2)}


def clearance(face: Optional[fonts.Face]) -> float:
    """The least line height at which a descender and the ascender of the
    line below it keep INK_GAP apart in `face` (its measured Latin ink),
    rounded up to two places; 1 for a face with no measured ink."""
    if face is None or face.ink is None:
        return 1.0
    return math.ceil(((face.ink[0] + face.ink[1]) / 1000 + INK_GAP) * 100 - 1e-9) / 100


def display_leading(axes: AxisValues, px: float, face: Optional[fonts.Face] = None) -> float:
    """The line height of a display style at `px`: DISPLAY_LEAD[0] at
    DISPLAY_LEAD_PX[0] and below, falling on a log scale of size to 1.0 for
    a muted brand or 0.92 for a bold one at DISPLAY_LEAD_PX[1] and above,
    and never below the face's clearance (MIN_DISPLAY_LEADING without a
    face). Continuous in size and contrast."""
    top, calm, bold = DISPLAY_LEAD
    large = calm + (bold - calm) * axes.contrast
    t = character.log_position(max(px, 1.0), *DISPLAY_LEAD_PX)
    floor = clearance(face) if face is not None else MIN_DISPLAY_LEADING
    return max(round(top + (large - top) * t, 2), floor)


def lead_token(role: str, script: str) -> str:
    """The leading token a role reads in `script`: its step's display
    leading for index 0, else the fixed index."""
    step, _, _, index, _ = ROLES[role]
    return f"type.leading.{script}.step-{step}" if index == 0 else f"type.leading.{script}.{index}"


def _rem(px: float) -> Dict[str, Any]:
    return {"value": round(px / 16, 4), "unit": "rem"}


def _step(role: str, axes: AxisValues) -> int:
    step = ROLES[role][0]
    return (BODY_STEP if axes.density < 0.5 else 2) if step == "ui" else step


def _snap(w: float, step: int = 100) -> int:
    return int(round(w / step)) * step


def weights(axes: AxisValues, choice: fonts.Choice, sizes: List[int]) -> Dict[str, int]:
    """The weight of every style at standard contrast. Display styles ease
    from the display weight at the hero to the heading weight at heading-3
    along a log scale of size; the rest take their kind's weight."""
    display = choice.display.clamp(character.display_weight(axes))
    heading = choice.text.clamp(character.heading_weight(axes))
    hero_px = sizes[ROLES["type.text.hero"][0] - 1]
    h3_px = sizes[ROLES["type.text.heading-3"][0] - 1]
    out = {}
    for role, (_, _, kind, _, _) in ROLES.items():
        if kind in ("display", "emphasis"):
            px = sizes[_step(role, axes) - 1]
            t = character.log_position(px, h3_px, hero_px)
            out[role] = choice.display.clamp(_snap(heading + (display - heading) * t, 50))
            if kind == "emphasis":
                out[role] = choice.display.clamp(out[role] - emphasis_gap(axes))
        else:
            out[role] = {"heading": heading, "regular": 400, "medium": 500}[kind]
    return out


# The weight the emphasised words of a two-voice headline drop by, from a
# quiet gap to a wide one (character.emphasis_contrast), in hundreds; and
# the emphasis contrast at which they turn italic, in a display face that
# ships one.
EMPHASIS_GAP = (100, 300)
ITALIC_FROM = 0.5


def emphasis_gap(axes: AxisValues) -> int:
    """How much lighter the emphasised words are than the display, 100 to
    300 in steps of 100."""
    lo, hi = EMPHASIS_GAP
    return _snap(lo + (hi - lo) * character.emphasis_contrast(axes))


def emphasis_italic(axes: AxisValues, face: fonts.Face) -> bool:
    """Whether the emphasised words turn italic: a wide enough emphasis
    contrast in a display face that ships a true italic."""
    return face.italic and character.emphasis_contrast(axes) >= ITALIC_FROM


# In dark mode light text on a dark page reads heavier, so a variable face
# sets it lighter: by DARK_LIGHTER[0] at body size, falling on a log scale
# to DARK_LIGHTER[1] at DARK_LIGHTER_PX and above, never under the face's
# lightest weight or DARK_FLOOR. A static face keeps its weights; high
# contrast keeps its own, heavier weights.
DARK_LIGHTER = (40.0, 10.0)
DARK_LIGHTER_PX = 96.0
DARK_FLOOR = 300


def dark_weight(weight: int, px: float, face: fonts.Face, body_px: float = BODY_PX) -> int:
    """The weight a style takes in dark mode at standard contrast: lighter
    by DARK_LIGHTER in a variable face, in tens, never heavier and never
    under the face's lightest weight or DARK_FLOOR."""
    if not face.variable:
        return weight
    t = character.log_position(max(px, body_px), body_px, DARK_LIGHTER_PX)
    less = DARK_LIGHTER[0] + (DARK_LIGHTER[1] - DARK_LIGHTER[0]) * t
    return min(weight, max(round((weight - less) / 10) * 10, face.weights[0], DARK_FLOOR))


def tracking_em(axes: AxisValues, px: float, hero_px: float) -> float:
    """Letter spacing in em for a heading size: 0 at 20px and below, the
    full display tracking at the hero size."""
    return character.display_tracking(axes) * character.log_position(px, 20, hero_px)


def _tier_scale(step: int, tier: str, script: str) -> str:
    """The primitive holding a step's fit factor at a tier in a script."""
    return f"type.tier-scale.{step}.{tier}" if script == "latin" \
        else f"type.tier-scale.arabic.{step}.{tier}"


def _vw(tier: str, script: str) -> str:
    """The primitive holding the display's fluid size at a tier in a
    script, in vw."""
    return f"type.vw.{tier}" if script == "latin" else f"type.vw.arabic.{tier}"


def _add_scripted(ts: TokenSet, path: str, latin: str, arabic: Optional[str]) -> None:
    """A number role that reads `latin`, and `arabic` under right to left
    when the system has Arabic and the two differ in value."""
    modes = {}
    if arabic is not None and ts.resolve(arabic) != ts.resolve(latin):
        modes = {"direction:rtl": "{%s}" % arabic}
    ts.add(Token(path, "number", "{%s}" % latin, modes=modes, layer="semantic"))


def _face_list(face: fonts.Face, *rest: str) -> List[str]:
    return [face.family, fonts.fallback_name(face), *rest]


def generate_type(axes: AxisValues, arabic: bool = True, body_px: int = BODY_PX,
                  leading_extra: float = 0.0, book_depth: Optional[float] = None,
                  columns: Optional[int] = None,
                  words: Optional[Mapping[str, float]] = None,
                  dark_scheme: bool = False) -> Generated:
    """The type tokens. `book_depth` is the product's book depth from the
    brief's product_type (fonts.choose), None when the brief does not say.
    `columns` is the columns of twelve the landing headline spans (its
    composition's, HEADLINE_COLUMNS; 12 when not given) and `words` the
    letters of the page's longest headline word per script, when known
    (FIT_WORD otherwise). With `dark_scheme` (the system builds color, so
    it has a dark scheme) the styles take lighter weights there
    (dark_weight)."""
    choice = fonts.choose(axes, book_depth)
    columns = GRID_COLUMNS if columns is None else columns
    fit_words = dict(FIT_WORD, **(words or {}))
    frame = frame_of(axes, columns)
    ts = TokenSet()
    faces = {
        "display": _face_list(choice.display, choice.display.generic),
        "text": _face_list(choice.text, "system-ui", "sans-serif"),
        "mono": _face_list(choice.mono, "ui-monospace", "monospace"),
        "arabic": _face_list(choice.arabic, choice.text.family, "Tahoma", "sans-serif"),
        "arabic-display": _face_list(choice.arabic_display, choice.arabic.family, "sans-serif"),
    }
    for role, token in FACE_TOKENS.items():
        if arabic or not role.startswith("arabic"):
            ts.add(Token(token, "fontFamily", faces[role]))
    latin = latin_px(axes, body_px)
    scale = fonts.arabic_scale(choice.text, choice.arabic)
    std = weights(axes, choice, latin)
    high = {role: _heavier(role, w, choice) for role, w in std.items()}

    def in_arabic(role: str, w: int) -> int:
        face = choice.arabic_display if ROLES[role][1] == "display" else choice.arabic
        return face.clamp(w)

    strong = _strong(std, high, choice, in_arabic if arabic else None)
    arabic_sizes_all = arabic_px(latin, scale) if arabic else None
    label_kind = "mono" if character.technical(axes) >= MONO_LABEL_FROM else "text"

    def face_of(role: str, rtl: bool) -> fonts.Face:
        kind = ROLES[role][1]
        kind = label_kind if kind == "label" else kind
        if rtl and role not in KEEP_FACE:
            return choice.arabic_display if kind == "display" else choice.arabic
        return {"display": choice.display, "text": choice.text, "mono": choice.mono}[kind]

    def dark(role: str, weight: int, rtl: bool) -> int:
        sizes = arabic_sizes_all if rtl and role not in KEEP_FACE else latin
        return dark_weight(weight, sizes[_step(role, axes) - 1], face_of(role, rtl), body_px)

    std_dark = {r: dark(r, w, False) if dark_scheme else w for r, w in std.items()}
    rtl_dark = {r: dark(r, in_arabic(r, w) if r not in KEEP_FACE else w, True)
                if dark_scheme else (in_arabic(r, w) if r not in KEEP_FACE else w)
                for r, w in std.items()} if arabic else {}
    strong_dark = {k.replace("contrast:standard", "contrast:dark-standard"):
                   dark_weight(w, body_px, choice.arabic if "rtl" in k else choice.text,
                               body_px) if dark_scheme else w
                   for k, w in strong.items() if "contrast:standard" in k}
    used = sorted(set(std.values()) | set(high.values()) | set(strong.values())
                  | ({in_arabic(r, w) for r, w in list(std.items()) + list(high.items())}
                     if arabic else set())
                  | set(std_dark.values()) | set(rtl_dark.values()) | set(strong_dark.values()))
    for w in used:
        ts.add(Token(f"type.weight.{w}", "fontWeight", w))
    for n, px in zip(STEPS, latin):
        ts.add(Token(f"type.size.latin.{n}", "dimension", _rem(px)))
    if arabic:
        for n, px in zip(STEPS, arabic_px(latin, scale)):
            ts.add(Token(f"type.size.arabic.{n}", "dimension", _rem(px)))
    lead = leading(axes, leading_extra)
    display_steps = sorted({spec[0] for spec in ROLES.values() if spec[3] == 0},
                           reverse=True)
    lead_latin = {f"step-{n}": display_leading(axes, latin[n - 1], choice.display)
                  for n in display_steps}
    lead_latin.update({str(i): v for i, v in lead.items()})
    for name, v in lead_latin.items():
        ts.add(Token(f"type.leading.latin.{name}", "number", v))
    if arabic:
        for name, v in lead_latin.items():
            ts.add(Token(f"type.leading.arabic.{name}", "number",
                         round(v + ARABIC_LEAD_EXTRA, 2)))
    hero_px = latin[ROLES["type.text.hero"][0] - 1]
    ts.add(Token("type.tracking.0", "dimension", {"value": 0, "unit": "px"}))
    ts.add(Token("type.tracking.caps", "dimension",
                 {"value": round(character.capitals_tracking(axes) * latin[DISPLAY_STEP - 1], 2),
                  "unit": "px"}))
    scale_steps = sorted({_step(r, axes) for r, spec in ROLES.items() if spec[4] == "scale"})
    for n in scale_steps:
        px = latin[n - 1]
        ts.add(Token(f"type.tracking.step-{n}", "dimension",
                     {"value": round(tracking_em(axes, px, hero_px) * px, 2), "unit": "px"}))
    label_px = latin[_step("type.text.label", axes) - 1]
    ts.add(Token("type.tracking.label", "dimension",
                 {"value": round(character.label_tracking(axes) * label_px, 2), "unit": "px"}))

    label_face = "mono" if character.technical(axes) >= MONO_LABEL_FROM else "text"
    for role, (_, face, _, _, track) in ROLES.items():
        face = label_face if face == "label" else face
        step = _step(role, axes)
        tracking = {"scale": "{type.tracking.step-%d}" % step, "label": "{type.tracking.label}",
                    "caps": "{type.tracking.caps}", "none": "{type.tracking.0}"}[track]
        value = {"fontFamily": "{%s}" % FACE_TOKENS[face],
                 "fontSize": "{type.size.latin.%d}" % step,
                 "fontWeight": "{type.weight.%d}" % std[role],
                 "letterSpacing": tracking,
                 "lineHeight": "{%s}" % lead_token(role, "latin")}
        rtl = value
        arabic_rtl = arabic and role not in KEEP_FACE
        if arabic_rtl:
            arabic_face = ARABIC_DISPLAY_FACE if face == "display" else ARABIC_FACE
            rtl = {"fontFamily": "{%s}" % arabic_face,
                   "fontSize": "{type.size.arabic.%d}" % step,
                   "fontWeight": "{type.weight.%d}" % in_arabic(role, std[role]),
                   "letterSpacing": "{type.tracking.0}",
                   "lineHeight": "{%s}" % lead_token(role, "arabic")}
        elif arabic:
            # Code keeps its face, size and leading, but drops letter
            # spacing for the Arabic strings it can hold.
            rtl = dict(value, letterSpacing="{type.tracking.0}")
        heavy = "{type.weight.%d}" % high[role]
        heavy_rtl = "{type.weight.%d}" % (in_arabic(role, high[role]) if arabic_rtl
                                          else high[role])
        per_context = {
            "scheme:light,contrast:standard,direction:ltr": value,
            "scheme:light,contrast:high,direction:ltr": dict(value, fontWeight=heavy),
            "scheme:light,contrast:standard,direction:rtl": rtl,
            "scheme:light,contrast:high,direction:rtl": dict(rtl, fontWeight=heavy_rtl),
            "scheme:dark,contrast:standard,direction:ltr":
                dict(value, fontWeight="{type.weight.%d}" % std_dark[role]),
            "scheme:dark,contrast:high,direction:ltr": dict(value, fontWeight=heavy),
            "scheme:dark,contrast:standard,direction:rtl": dict(
                rtl, fontWeight="{type.weight.%d}" % rtl_dark[role]) if arabic_rtl else
            dict(rtl, fontWeight="{type.weight.%d}" % std_dark[role]),
            "scheme:dark,contrast:high,direction:rtl": dict(rtl, fontWeight=heavy_rtl),
        }
        if not arabic:
            per_context = {k.replace(",direction:ltr", ""): v for k, v in per_context.items()
                           if "rtl" not in k}
        base, modes = compress(per_context)
        ts.add(Token(role, "typography", base, modes=modes, layer="semantic"))
    per_strong = {}
    for k, w in strong.items():
        per_strong["scheme:light," + k] = "{type.weight.%d}" % w
        dark_w = strong_dark.get(k.replace("contrast:standard", "contrast:dark-standard"), w)
        per_strong["scheme:dark," + k] = "{type.weight.%d}" % dark_w
    if not arabic:
        per_strong = {k.replace(",direction:ltr", ""): v for k, v in per_strong.items()
                      if "rtl" not in k}
    base, modes = compress(per_strong)
    ts.add(Token("type.strong", "fontWeight", base, modes=modes, layer="semantic"))
    for run, face in RUNS.items():
        if arabic or run == "type.run.latin":
            ts.add(Token(run, "fontFamily", "{%s}" % face, layer="semantic"))
    feature = round(2.0 + 1.0 * axes.contrast, 4)
    for name, rem in (("inline", body_px / 16), ("control", ICON_CONTROL_REM),
                      ("feature", feature)):
        ts.add(Token(f"type.icon.{name}", "dimension", {"value": round(rem, 4), "unit": "rem"}))
    ts.add(Token("type.icon.stroke-width", "number", character.icon_stroke(axes)))
    for name in ("inline", "control", "feature"):
        ts.add(Token(f"type.icon.size.{name}", "dimension", "{type.icon.%s}" % name,
                     layer="semantic"))
    ts.add(Token("type.icon.stroke", "number", "{type.icon.stroke-width}", layer="semantic"))
    arabic_sizes = arabic_px(latin, scale) if arabic else None
    phone = phone_factors(axes, latin, body_px, arabic_sizes, choice, frame, fit_words)
    for role in reversed(PHONE_ROLES):
        ts.add(Token(f"type.phone-scale.{ROLES[role][0]}", "number", phone[role]))
    for role in PHONE_ROLES + tuple(FOLLOWS):
        ts.add(Token(phone_token(role), "number", "{type.phone-scale.%d}" % ROLES[role][0],
                     layer="semantic"))
    scripts = {"latin": latin, **({"arabic": arabic_sizes} if arabic_sizes else {})}
    fits = {sc: tier_factors(axes, choice, latin, arabic_sizes, frame, fit_words, sc)
            for sc in scripts}
    fluid = {sc: fluid_vw(axes, choice, latin, arabic_sizes, dict(fits[sc], phone=phone),
                          frame, fit_words, sc) for sc in scripts}
    for sc in scripts:
        for role in PHONE_ROLES:
            for tier in FIT_TIERS:
                ts.add(Token(_tier_scale(ROLES[role][0], tier, sc), "number",
                             fits[sc][tier][role]))
    for role in PHONE_ROLES:
        for tier in FIT_TIERS:
            _add_scripted(ts, fit_token(role, tier), _tier_scale(ROLES[role][0], tier, "latin"),
                          _tier_scale(ROLES[role][0], tier, "arabic") if arabic_sizes else None)
    for sc in scripts:
        for tier in TIER_WIDTHS:
            ts.add(Token(_vw(tier, sc), "number", fluid[sc][tier]))
    for tier in TIER_WIDTHS:
        _add_scripted(ts, fluid_token(tier), _vw(tier, "latin"),
                      _vw(tier, "arabic") if arabic_sizes else None)
    for script, letters in fit_words.items():
        if arabic or script == "latin":
            ts.add(Token(f"type.fit-word.{script}", "number", letters))
    ts.add(Token("type.fit-columns", "number", columns))
    gap_tone = round(character.emphasis_contrast(axes), 2)
    tone = round(gap_tone * 100)
    ts.add(Token(f"type.tone.{tone}", "number", gap_tone))
    ts.add(Token("type.switch.off", "number", 0))
    ts.add(Token("type.switch.on", "number", 1))
    ts.add(Token("type.emphasis.tone", "number", "{type.tone.%d}" % tone, layer="semantic"))
    italic = emphasis_italic(axes, choice.display)
    ts.add(Token("type.emphasis.italic", "number",
                 "{type.switch.%s}" % ("on" if italic else "off"),
                 modes={"direction:rtl": "{type.switch.off}"} if arabic and italic else {},
                 layer="semantic"))
    hero_n = ROLES["type.text.hero"][0]
    notes = [f"type: display {choice.display.family}, text {choice.text.family}, mono "
             f"{choice.mono.family}" + (f", Arabic {choice.arabic.family} and "
                                        f"{choice.arabic_display.family} at {scale:g} times the "
                                        "Latin size" if arabic else "")
             + f", ratio {ratio(axes):g}, display weight {std['type.text.hero']}, hero "
             f"{latin[hero_n - 1]}px ({latin[hero_n - 1] * phone['type.text.hero']:.0f}px on a "
             f"phone), landing display {latin[DISPLAY_STEP - 1]}px at {REFERENCE_WIDTH}px wide "
             f"({latin[DISPLAY_STEP - 1] * phone['type.text.display']:.0f}px on a phone at most, "
             f"{fluid['latin']['phone']:g}vw), line height "
             f"{lead_latin['step-%d' % DISPLAY_STEP]:g}"]
    return Generated(tokens=ts, notes=notes)


def _strong(std: Dict[str, int], high: Dict[str, int], choice: fonts.Choice,
            in_arabic: Optional[Any]) -> Dict[str, int]:
    """type.strong per context: the text face's heading weight, and under
    high contrast at least STRONG_GAP above body text, which gets heavier
    there too. Under rtl each weight is one the Arabic face ships."""
    h3, body = "type.text.heading-3", "type.text.body"
    out = {"contrast:standard,direction:ltr": std[h3],
           "contrast:high,direction:ltr": choice.text.clamp(
               max(high[h3], high[body] + STRONG_GAP))}
    arabic = in_arabic or (lambda role, w: w)
    out["contrast:standard,direction:rtl"] = arabic(body, std[h3])
    out["contrast:high,direction:rtl"] = arabic(
        body, max(high[h3], arabic(body, high[body]) + STRONG_GAP))
    return out


def _heavier(role: str, weight: int, choice: fonts.Choice) -> int:
    """High contrast adds one weight to every style set in the text or
    mono face, within what the face (and its Arabic partner) ships."""
    face = ROLES[role][1]
    if face == "display":
        return weight
    top = min(choice.text.weights[1], choice.arabic.weights[1], choice.mono.weights[1], 700)
    return max(weight, min(weight + 100, top))


def _px(dim: Dict[str, Any]) -> float:
    return dimension_px(dim)


def _typed(ts: TokenSet, path: str) -> bool:
    """The typed accessor every check reads through: a role is read only
    when it exists with the type its role expects."""
    return typed(ts, path, ROLE_TYPES)


def _roles(ts: TokenSet, names) -> List[str]:
    return [r for r in names if _typed(ts, r)]


def _sizes(ts: TokenSet, mode: str) -> List[str]:
    """Body keeps 16px; every other role keeps the 12px fine-print floor."""
    out = []
    for role in ROLES:
        floor = MIN_BODY_PX if role == "type.text.body" else MIN_FINE_PX
        if _typed(ts, role):
            px = _px(ts.resolve(role, mode)["fontSize"])
            if px < floor:
                out.append(f"{role} ({mode}) is {px:g}px; it needs at least {floor}px to stay "
                           "readable, so point its fontSize at a larger step")
    return out


def _leading(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for role in _roles(ts, LEADING_ROLES):
        v = ts.resolve(role, mode)
        if v["lineHeight"] < MIN_READING_LEADING:
            out.append(f"{role} ({mode}) has line height {v['lineHeight']:g}; running text needs "
                       f"{MIN_READING_LEADING} or more (1.4.8), so point it at a taller leading")
    return out


def _tracking(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for role in _roles(ts, TRACKING_ROLES):
        v = ts.resolve(role, mode)
        if v["letterSpacing"]["value"] < 0:
            out.append(f"{role} ({mode}) tightens letters to {v['letterSpacing']['value']:g}px; "
                       "running text keeps 0 or more, so point it at type.tracking.0")
    return out


def _first(family: Any) -> str:
    return family if isinstance(family, str) else family[0]


# Arabic sits at least a pixel and at most a fifth above the Latin size.
ARABIC_GROW_MAX = 1.2


def _arabic(ts: TokenSet, mode: str) -> List[str]:
    """Under rtl every style set in the text or display face reads the
    Arabic face (or the Arabic display face) at a size 4 to 20 percent
    larger than its Latin size, with taller lines, and every style drops
    letter spacing. Code keeps its face, size and leading. A set without
    type.face.arabic is Latin-only."""
    if "direction:rtl" not in mode or not _typed(ts, ARABIC_FACE):
        return []
    ltr_mode = mode.replace("direction:rtl", "direction:ltr")
    out = []
    mono = _first(ts.resolve("type.face.mono")) if ts.has("type.face.mono") else ""
    for role in _roles(ts, ROLES):
        rtl, ltr = ts.resolve(role, mode), ts.resolve(role, ltr_mode)
        kept = role in KEEP_FACE and rtl["fontFamily"] == ltr["fontFamily"] \
            and _first(ltr["fontFamily"]) == mono
        face = ARABIC_DISPLAY_FACE if ROLES[role][1] == "display" and \
            _typed(ts, ARABIC_DISPLAY_FACE) else ARABIC_FACE
        if not kept and rtl["fontFamily"] != ts.resolve(face, mode):
            out.append(f"{role} (direction:rtl) is set in {_first(rtl['fontFamily'])}, not "
                       f"{face}; Arabic text needs its own face, so point its direction:rtl "
                       f"fontFamily at {face}")
        if rtl["letterSpacing"]["value"] != 0:
            out.append(f"{role} (direction:rtl) spaces letters by "
                       f"{rtl['letterSpacing']['value']:g}px; letter spacing breaks Arabic "
                       "joins, so point it at type.tracking.0")
        if kept:
            continue
        rtl_px, ltr_px = _px(rtl["fontSize"]), _px(ltr["fontSize"])
        if not ltr_px + 1 <= rtl_px <= ltr_px * ARABIC_GROW_MAX:
            out.append(f"{role} (direction:rtl) is {rtl_px:g}px against its Latin {ltr_px:g}px; "
                       "Arabic reads at least 1px and at most a fifth larger than the Latin size "
                       "at the same step, so point it at the Arabic size for that step")
        if rtl["lineHeight"] <= ltr["lineHeight"]:
            out.append(f"{role} (direction:rtl) has line height {rtl['lineHeight']:g}, not taller "
                       f"than its Latin {ltr['lineHeight']:g}; Arabic needs room for its marks, "
                       "so point it at the Arabic leading")
        elif _display_kind(role) and rtl["lineHeight"] < ltr["lineHeight"] \
                + ARABIC_DISPLAY_GAP - 1e-9:
            out.append(f"{role} (direction:rtl) has line height {rtl['lineHeight']:g}, less than "
                       f"{ARABIC_DISPLAY_GAP:g} above its Latin {ltr['lineHeight']:g}; Arabic "
                       "display lines need room for the marks above and below, so point it at "
                       "the Arabic leading")
    return out


def _size_source(ts: TokenSet, role: str, mode: str) -> Optional[str]:
    """The token holding the literal a role's fontSize resolves to in one
    context, following aliases through the role and the field; None when
    the role writes the size inline."""
    raw, path = ts.raw(role, mode), role
    while is_alias(raw):
        path = alias_target(raw)
        raw = ts.raw(path, mode)
    field = raw["fontSize"]
    source = None
    while is_alias(field):
        source = alias_target(field)
        field = ts.raw(source, mode)
    return source


def _rem_sizes(ts: TokenSet, mode: str) -> List[str]:
    """Every text role's fontSize in rem in each direction, wherever it
    points; then, once, any px step in the size tree no role reaches."""
    out, named = [], set()
    for role in _roles(ts, ROLES):
        size = ts.resolve(role, mode)["fontSize"]
        if size["unit"] == "rem":
            continue
        source = _size_source(ts, role, mode)
        named.add(source)
        where = f" through {source}" if source else ""
        fix = f"express {source} in rem" if source else "write it in rem"
        out.append(f"{role} ({mode}) is {size['value']:g}{size['unit']}{where}; sizes in rem "
                   "follow the reader's default text size, so point its fontSize at a size in "
                   f"rem or {fix}")
    if "direction:rtl" in mode:
        return out
    # A set without the direction axis has no right to left sizes to name.
    for role in _roles(ts, ROLES) if "direction" in ts.axes else ():
        named.add(_size_source(ts, role, "direction:rtl"))
    return out + [f"{t.path} is in {t.value['unit']}; sizes in rem follow the reader's default "
                  "text size, so express it in rem"
                  for t in ts.tokens() if t.path.startswith("type.size.")
                  and t.type == "dimension" and t.path not in named
                  and isinstance(t.value, dict) and t.value.get("unit") != "rem"]


def _hierarchy(ts: TokenSet, mode: str) -> List[str]:
    present = _roles(ts, HIERARCHY)
    out = []
    for a, b in zip(present, present[1:]):
        pa, pb = _px(ts.resolve(a, mode)["fontSize"]), _px(ts.resolve(b, mode)["fontSize"])
        if pa <= pb:
            out.append(f"{a} ({mode}, {pa:g}px) is not larger than {b} ({pb:g}px); keep "
                       f"{', '.join(r.rsplit('.', 1)[1] for r in HIERARCHY)} in falling size")
        elif pa / pb < MIN_LEVEL_RATIO:
            times = int(pa / pb * 100) / 100
            out.append(f"{a} ({mode}, {pa:g}px) is only {times:.2f} times {b} ({pb:g}px); our "
                       f"floor between neighbouring levels is {MIN_LEVEL_RATIO:g} times, since a "
                       f"smaller step does not read as a new level, so move {a} up the scale")
    return out


def _tracking_order(ts: TokenSet, mode: str) -> List[str]:
    """Down the ladder, tracking loosens or stays: a smaller role never
    tracks tighter than the larger role above it. Under rtl in a set with
    an Arabic face, arabic-text holds every role at 0, so it owns tracking
    there."""
    if "direction:rtl" in mode and _typed(ts, ARABIC_FACE):
        return []
    present = _roles(ts, HIERARCHY)
    out = []
    for a, b in zip(present, present[1:]):
        ta = _px(ts.resolve(a, mode)["letterSpacing"])
        tb = _px(ts.resolve(b, mode)["letterSpacing"])
        if tb < ta:
            out.append(f"{b} ({mode}) tracks at {tb:g}px, tighter than {a} ({ta:g}px) above "
                       f"it; tracking loosens as size falls, so point {b} at a looser tracking")
    return out


def _display_kind(role: str) -> bool:
    """A style set in the display face whose leading follows its size."""
    return ROLES[role][1] == "display" and ROLES[role][3] == 0


def _line_height_floor(ts: TokenSet, mode: str) -> List[str]:
    """A display style keeps a line height of MIN_DISPLAY_LEADING or more;
    every other style a line height above 1."""
    out = []
    for role in _roles(ts, ROLES):
        lh = ts.resolve(role, mode)["lineHeight"]
        if _display_kind(role):
            if lh < MIN_DISPLAY_LEADING:
                out.append(f"{role} ({mode}) has line height {lh:g}; below "
                           f"{MIN_DISPLAY_LEADING:g}, our floor for a display style, its lines "
                           f"collide, so point it at a leading of {MIN_DISPLAY_LEADING:g} or more")
        elif lh <= 1:
            out.append(f"{role} ({mode}) has line height {lh:g}; at 1 or less its lines touch, "
                       "so point it at a leading above 1")
    return out


def _clearance(ts: TokenSet, mode: str) -> List[str]:
    """A display style set below a line height of 1 leaves room between a
    descender and the ascender of the line below it: at least the face's
    measured clearance (clearance). Arabic has its own rule (arabic-text)."""
    if "direction:rtl" in mode:
        return []
    out = []
    for role in _roles(ts, ROLES):
        if not _display_kind(role):
            continue
        v = ts.resolve(role, mode)
        face = fonts.BY_FAMILY.get(_first(v["fontFamily"]))
        need = clearance(face)
        if v["lineHeight"] < 1 and v["lineHeight"] < need - 1e-9:
            out.append(f"{role} ({mode}) has line height {v['lineHeight']:g}, under the "
                       f"{need:g} {face.family if face else 'its face'} needs for a descender "
                       "to clear the ascender of the next line, so point it at a leading of "
                       f"{need:g} or more")
    return out


def _code_face(ts: TokenSet, mode: str) -> List[str]:
    p = FACE_TOKENS["mono"]
    if not _typed(ts, p):
        return []
    family = ts.resolve(p, mode)
    last = family if isinstance(family, str) else family[-1]
    if last in MONOSPACE:
        return []
    return [f"{p} ends in {last}; code needs a fixed width, so end its list with ui-monospace "
            "or monospace"]


def _phone_hierarchy(ts: TokenSet, mode: str) -> List[str]:
    """On a phone the styles in PHONE_ROLES take their size times their
    factor: each factor sits above 0 and at most 1, and the phone sizes
    keep falling from hero to section-title and stay above heading-2."""
    present = [r for r in PHONE_ROLES if _typed(ts, r) and _typed(ts, phone_token(r))]
    if not present:
        return []
    out = []
    sizes = []
    for role in present:
        factor = ts.resolve(phone_token(role), mode)
        if not 0 < factor <= 1:
            out.append(f"{phone_token(role)} ({mode}) is {factor:g}; a phone factor sits above 0 "
                       "and at most 1, so point it at a factor in that range")
        sizes.append((phone_token(role), _px(ts.resolve(role, mode)["fontSize"]) * factor))
    if _typed(ts, PHONE_FLOOR_ROLE):
        sizes.append((PHONE_FLOOR_ROLE, _px(ts.resolve(PHONE_FLOOR_ROLE, mode)["fontSize"])))
    for role, leader in FOLLOWS.items():
        if all(_typed(ts, r) and _typed(ts, phone_token(r)) for r in (role, leader)):
            mine, theirs = (_px(ts.resolve(r, mode)["fontSize"]) * ts.resolve(phone_token(r), mode)
                            for r in (role, leader))
            if mine > theirs + 0.01:
                out.append(f"{role} ({mode}) gives {mine:.1f}px on a phone, above {leader} at "
                           f"{theirs:.1f}px; a figure never outranks the headline there, so point "
                           f"{phone_token(role)} at {leader}'s factor")
    for (a, pa), (b, pb) in zip(sizes, sizes[1:]):
        if pa <= pb:
            out.append(f"{b} ({mode}) gives {pb:.1f}px on a phone, not smaller than {a} at "
                       f"{pa:.1f}px; keep hero, heading-1, section-title and heading-2 in falling "
                       f"size on a phone, so point {b if b != PHONE_FLOOR_ROLE else a} at a "
                       "factor that restores the order")
    return out


def phone_roles(ts: TokenSet) -> List[str]:
    """The styles tokens.css scales on a phone: those with a factor token,
    in a set that has the tablet breakpoint to switch it off at."""
    if not ts.has("layout.breakpoint.tablet"):
        return []
    return [r for r in PHONE_ROLES + tuple(FOLLOWS) if ts.has(r) and ts.has(phone_token(r))]


def _fit_of(ts: TokenSet, role: str, tier: str) -> Optional[str]:
    """The fit token a style reads at a tier (its own, or the one of the
    style it follows), None when the set has none."""
    token = fit_token(FOLLOWS.get(role, role), tier)
    return token if ts.has(token) else None


def tier_factor(ts: TokenSet, role: str, tier: str, mode: str = "") -> float:
    """The factor a style takes at a tier in a context: its fit factor, or 1."""
    token = _fit_of(ts, role, tier)
    return float(ts.resolve(token, mode)) if token else 1.0


# The column a set without type.fit-columns is measured in from the laptop
# up: seven of twelve, where a split composition sets its headline.
DEFAULT_COLUMNS = 7


def fluid_roles(ts: TokenSet) -> List[str]:
    """The styles tokens.css sets fluid: the display and the styles that
    follow it, in a set that has a fluid size for every tier."""
    if not all(ts.has(fluid_token(t)) for t in TIER_WIDTHS) or not phone_roles(ts):
        return []
    return [r for r in phone_roles(ts) if FOLLOWS.get(r, r) in FLUID]


def _frame_in(ts: TokenSet, mode: str) -> Optional[Frame]:
    """The frame a set declares: its landing margins and container when it
    has them, else its page margins and container; None when a tier's
    margin is missing."""
    margins = {}
    for tier in TIER_WIDTHS:
        for path in (f"layout.landing.margin-inline.{tier}", f"layout.margin-inline.{tier}"):
            if ts.has(path):
                margins[tier] = _px(ts.resolve(path, mode))
                break
    if set(margins) != set(TIER_WIDTHS):
        return None
    box = "layout.landing.max-width" if ts.has("layout.landing.max-width") \
        else "layout.container.max"
    columns = int(ts.resolve("type.fit-columns")) if ts.has("type.fit-columns") \
        else DEFAULT_COLUMNS
    return Frame(margins, _px(ts.resolve(box, mode)), columns)


def _letters(ts: TokenSet, script: str) -> float:
    path = f"type.fit-word.{script}"
    return float(ts.resolve(path)) if ts.has(path) else float(FIT_WORD[script])


def fit_problems(ts: TokenSet, mode: str = "") -> List[str]:
    """At each tier, in each script the set ships, the display style's
    longest headline word (type.fit-word, else FIT_WORD) fits the headline's
    column (Frame) at the tier's narrowest and widest widths, the display
    taking its fluid size where the set has one; and at each tier from the
    tablet up the scaled display, hero, heading-1 and section-title keep
    falling in size, MIN_LEVEL_RATIO apart, above heading-2."""
    need = ("layout.breakpoint.tablet", "layout.container.max", "type.face.display")
    if not all(ts.has(p) for p in need) or not _typed(ts, "type.text.display"):
        return []
    face = fonts.BY_FAMILY.get(_first(ts.resolve("type.face.display")))
    arabic = fonts.BY_FAMILY.get(_first(ts.resolve(ARABIC_DISPLAY_FACE))) \
        if _typed(ts, ARABIC_DISPLAY_FACE) else None
    if face is None:
        return []
    # The standard contrast context in each direction, over the axes the set has.
    std = ["contrast:standard"] if "contrast" in ts.axes else []
    ltr = ",".join(std + (["direction:ltr"] if "direction" in ts.axes else []))
    rtl = ",".join(std + ["direction:rtl"])
    frame = _frame_in(ts, mode)
    fluid = all(_typed(ts, fluid_token(t)) for t in TIER_WIDTHS)
    hero_ok = _typed(ts, "type.text.hero")
    scripts = [("latin", ltr, face)]
    if arabic is not None and "direction" in ts.axes:
        scripts.append(("arabic", rtl, arabic))
    out = []
    phone = fluid and all(_typed(ts, phone_token(r))
                          for r in ("type.text.display", "type.text.hero"))
    tiers = (("phone",) if phone else ()) + FIT_TIERS
    for tier in tiers:
        low, high = TIER_WIDTHS[tier]
        widths = [low] if not fluid else [low, high or REFERENCE_WIDTH] + (
            [1920] if high is None else [])
        for script, ctx, fc in scripts if frame is not None else ():
            f = ts.resolve(phone_token("type.text.display"), ctx) if tier == "phone" \
                else tier_factor(ts, "type.text.display", tier, ctx)
            ceiling = _px(ts.resolve("type.text.display", ctx)["fontSize"]) * f
            hero = 0.0
            if hero_ok and tier != "phone":
                hf = ts.resolve(phone_token("type.text.hero"), ctx) if tier == "phone" \
                    else tier_factor(ts, "type.text.hero", tier, ctx)
                hero = _px(ts.resolve("type.text.hero", ctx)["fontSize"]) * hf
            for w in widths:
                size = ceiling
                if fluid:
                    size = min(float(ts.resolve(fluid_token(tier), ctx)) * w / 100, ceiling)
                    if tier != "phone":
                        size = max(hero + 1, size)
                col = frame.column(tier, w)
                width = word_em(fc, script, _letters(ts, script)) * size
                if width > col + 0.5:
                    factor = phone_token("type.text.display") if tier == "phone" \
                        else fit_token("type.text.display", tier)
                    out.append(f"type.text.display at {w}px wide ({tier}) sets a "
                               f"{_letters(ts, script):g} letter {script} word {width:.0f}px "
                               f"wide in a {col:.0f}px column; point {factor}"
                               + (f" or {fluid_token(tier)}" if fluid else "")
                               + " at a smaller value that fits it")
                    break
        if tier == "phone":
            continue
        for script, ctx, _ in scripts:
            chain = []
            for r in PHONE_ROLES:
                if not _typed(ts, r):
                    continue
                size = _px(ts.resolve(r, ctx)["fontSize"]) * tier_factor(ts, r, tier, ctx)
                if r == "type.text.display" and fluid:
                    size = min(float(ts.resolve(fluid_token(tier), ctx)) * low / 100, size)
                chain.append((r, size))
            if _typed(ts, PHONE_FLOOR_ROLE):
                chain.append((PHONE_FLOOR_ROLE,
                              _px(ts.resolve(PHONE_FLOOR_ROLE, ctx)["fontSize"])))
            where = "" if script == "latin" else f" in {script}"
            for (a, pa), (b, pb) in zip(chain, chain[1:]):
                if pa < pb * MIN_LEVEL_RATIO - 0.01:
                    fix = fit_token(a, tier) + (f" or {fluid_token(tier)}"
                                                if a == "type.text.display" and fluid else "")
                    out.append(f"{a} at the {tier} tier{where} is {pa:.1f}px, less than "
                               f"{MIN_LEVEL_RATIO:g} times {b} at {pb:.1f}px; point {fix} at a "
                               "factor that keeps the order")
    return out


def scale_property(role: str) -> str:
    """The CSS property that holds a style's phone factor or 1."""
    from engine.foundations.tokens import css_property
    return f"{css_property(role)}-scale"


def fluid_property(role: str) -> str:
    """The CSS property that holds a fluid style's size in vw, a number, at
    the tier the viewport is in (the style it follows, for a follower). It
    is set on the root, so a right to left block inside a left to right
    page reads the root's."""
    from engine.foundations.tokens import css_property
    return f"{css_property(FOLLOWS.get(role, role))}-fluid"


def fluid_size(role: str, size: str) -> str:
    """The font-size a fluid style writes: its fluid size, never above
    `size` (its size times its scale) and never below 1px over the hero."""
    from engine.foundations.tokens import css_property
    hero = css_property("type.text.hero") + "-font-size"
    return f"clamp(calc(var({hero}) + 1px), calc(var({fluid_property(role)}) * 1vw), {size})"


def responsive_lines(ts: TokenSet) -> Dict[str, List[str]]:
    """The declarations for the phone (:root) and from each breakpoint up
    that set each scaled style's factor: the phone factor, then the tier's
    fit factor (or 1 where the set has none); the display's fluid size per
    tier; and, at the root, each type role's line breaking (WRAP)."""
    from engine.foundations.tokens import css_property
    roles = phone_roles(ts)
    leaders = [r for r in fluid_roles(ts) if r not in FOLLOWS]

    def fluid(tier: str) -> List[str]:
        return [f"{fluid_property(r)}: var({css_property(fluid_token(tier))});"
                for r in leaders]

    wrap = [f"{css_property(r)}-text-wrap: {WRAP[r]};" for r in ROLES
            if r in WRAP and _typed(ts, r)] if roles else []
    out = {"phone": [f"{scale_property(r)}: var({css_property(phone_token(r))});"
                     for r in roles] + fluid("phone") + wrap}
    for tier in FIT_TIERS:
        lines = []
        for r in roles:
            token = _fit_of(ts, r, tier)
            if token:
                lines.append(f"{scale_property(r)}: var({css_property(token)});")
            elif tier == FIT_TIERS[0]:
                lines.append(f"{scale_property(r)}: 1;")
        out[tier] = lines + fluid(tier)
    return out


def _high_weights(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast no style is lighter than at standard contrast."""
    if "contrast:high" not in mode:
        return []
    std = mode.replace("contrast:high", "contrast:standard")
    return [f"{role} ({mode}) is weight {ts.resolve(role, mode)['fontWeight']:g}, lighter than "
            f"its {ts.resolve(role, std)['fontWeight']:g} at standard contrast; high contrast "
            "never lightens text, so point its contrast:high fontWeight at a heavier step"
            for role in _roles(ts, ROLES)
            if ts.resolve(role, mode)["fontWeight"] < ts.resolve(role, std)["fontWeight"]]


def _dark_weights(ts: TokenSet, mode: str) -> List[str]:
    """In dark mode at standard contrast no style is heavier than in light
    mode, in the same direction."""
    if "scheme:dark" not in mode:
        return []
    light = mode.replace("scheme:dark", "scheme:light")
    return [f"{role} ({mode}) is weight {ts.resolve(role, mode)['fontWeight']:g}, heavier than "
            f"its {ts.resolve(role, light)['fontWeight']:g} in light mode; light text on a dark "
            "page already reads heavier, so point its scheme:dark fontWeight at a step no "
            "heavier"
            for role in _roles(ts, ROLES)
            if ts.resolve(role, mode)["fontWeight"] > ts.resolve(role, light)["fontWeight"]]


def _strong_gap(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast, bold words stay STRONG_GAP above body text, so
    emphasis survives the heavier body the mode gives."""
    if "contrast:high" not in mode or not (_typed(ts, "type.strong")
                                           and _typed(ts, "type.text.body")):
        return []
    strong = ts.resolve("type.strong", mode)
    body = ts.resolve("type.text.body", mode)["fontWeight"]
    if strong - body >= STRONG_GAP:
        return []
    want = int(body + STRONG_GAP)
    return [f"type.strong ({mode}) is weight {strong:g}, only {strong - body:g} above "
            f"type.text.body at {body:g}; bold words must stay at least {STRONG_GAP} above body "
            "text under high contrast, so point its contrast:high value at "
            f"type.weight.{want} or heavier"]


def _icons(ts: TokenSet, mode: str) -> List[str]:
    sizes = [r for r in ("type.icon.size.inline", "type.icon.size.control",
                         "type.icon.size.feature") if _typed(ts, r)]
    out = []
    for a, b in zip(sizes, sizes[1:]):
        pa, pb = _px(ts.resolve(a, mode)), _px(ts.resolve(b, mode))
        if pa >= pb:
            out.append(f"{b} ({pb:g}px) is not larger than {a} ({pa:g}px); keep inline, control "
                       "and feature icons in rising size")
    if _typed(ts, "type.icon.stroke"):
        stroke = ts.resolve("type.icon.stroke", mode)
        lo, hi = ICON_STROKE_RANGE
        if not lo <= stroke <= hi:
            out.append(f"type.icon.stroke is {stroke:g}; on a 24 unit icon a stroke outside {lo:g} "
                       f"to {hi:g} breaks up or fills in, so point it inside that range")
    return out


def _fits_check(ts: TokenSet, mode: str) -> List[str]:
    return fit_problems(ts)


# High contrast and dark mode change only weights; every other check reads
# direction.
_WEIGHT_ONLY = (("contrast", "high contrast changes only weights, which high-contrast-weights "
                 "reads"),
                ("scheme", "dark mode changes only weights, which dark-weights reads"))
CHECKS: Tuple[Check, ...] = (
    Check("type-sizes", "system", _sizes, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("reading-leading", "1.4.8", _leading, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("reading-tracking", "system", _tracking, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("arabic-text", "system", _arabic, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("rem-sizes", "system", _rem_sizes, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("type-hierarchy", "system", _hierarchy, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("phone-hierarchy", "system", _phone_hierarchy, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("display-fits", "system", _fits_check,
          exempt_axes=(("direction", "it reads both directions itself"),
                       ("contrast", "fit factors never carry modes"),
                       ("scheme", "fit factors never carry modes"))),
    Check("type-tracking-order", "system", _tracking_order, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("line-height-floor", "system", _line_height_floor, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("display-clearance", "system", _clearance, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("code-face", "system", _code_face,
          exempt_axes=(("direction", "the mono face is a primitive, the same in both "
                                     "directions"),
                       ("contrast", "the mono face is a primitive, the same in both "
                                    "contrasts"),
                       ("scheme", "the mono face is a primitive, the same in both schemes"))),
    Check("high-contrast-weights", "system", _high_weights,
          axes=("scheme", "contrast", "direction")),
    Check("strong-weight", "system", _strong_gap, axes=("scheme", "contrast", "direction")),
    Check("dark-weights", "system", _dark_weights, axes=("scheme", "direction"),
          exempt_axes=(("contrast", "high contrast keeps its own weights, which "
                                    "high-contrast-weights reads"),)),
    Check("icon-sizes", "system", _icons,
          exempt_axes=(("direction", "icon sizes and the stroke never carry modes"),
                       ("contrast", "icon sizes and the stroke never carry modes"),
                       ("scheme", "icon sizes and the stroke never carry modes"))),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    a = inputs.audience
    return generate_type(axes, arabic=inputs.arabic, body_px=a.body_px,
                         leading_extra=a.leading_extra, book_depth=a.book_depth,
                         columns=headline_columns(axes, a), words=inputs.words,
                         dark_scheme=inputs.dark_scheme)


FOUNDATION = Foundation(name="type", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
