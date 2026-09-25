"""Generative brand art: a hero composition, a pattern tile and a gradient
built from the axes and the built colors, so a page is never empty for
want of photos.

Every quantity is a continuous function of the axes, and the few counts
(how many accent dots, how many cells in the tile) are the nearest whole
number to one. Nothing is random, so the same axes always draw the same
art and two briefs a little apart draw art a little apart.

The hero is three layers. At the back a large neutral plane, in the
middle the focal shape in the brand color, in front a small group of
support accents. The group sits on the right third and leaves the left
open for a heading (mirror it under right to left), and the focal shape
always fits the right 9:16 of the canvas, the part a phone crop keeps.
Area follows the palette weights: the neutral takes about 60 percent of
the drawn area, the brand 30 and the support 10, and warmth moves area
from the neutral to the two accents. Geometry rounds every corner
(character.roundness: a square becomes a circle), and formality sets
regularity (character.regularity): formal art sits square on a grid with
more, smaller accents, playful art turns and offsets fewer, larger ones.

The tile is a lattice of evenly spaced shapes with a size rhythm and a
half drop that grows as formality falls; shapes that cross an edge are
drawn again on the far side, so the tile repeats without seams.

Every file is decoration: the root is aria-hidden, there is no title, and
the report says to place it with an empty alt. Colors are CSS custom
properties with the light values as fallbacks, so an inline SVG follows
the page's scheme and an <img> shows the light version. The one id (the
gradient's) carries a digest of the inputs, so it never meets an id on
the page or in another build's art.
"""
from __future__ import annotations

import hashlib
import math
from dataclasses import dataclass
from typing import Dict, List, Sequence, Tuple

from engine.foundations import character
from engine.foundations.tokens import TokenSet, css_property
from engine.synthesizer.axes import AxisValues

ART_DIR = "art"
FILES: Tuple[str, ...] = (f"{ART_DIR}/pattern.svg", f"{ART_DIR}/shapes.svg",
                          f"{ART_DIR}/gradient.svg")
PALETTE = ("color.decorative.brand", "color.decorative.support", "color.decorative.neutral")
HEAD = ("<!-- Decorative brand art generated with the design system. Place it with an empty "
        "alt; it carries no meaning. -->")
HERO = (1200, 800)
TILE = 240
# The hero's unit is 1/16 of its height; the margin is one and a half.
GRID_ROWS = 16
MARGIN_UNITS = 1.5
# The neutral's opacity over the page.
QUIET = 0.55
# The share of the hero the shapes cover; the rest is open space.
COVERAGE = 0.25


@dataclass(frozen=True)
class Shape:
    """A rectangle by center and size, rounded by `round_` (0 square, 1 a
    circle or a capsule), turned `turn` degrees about its center."""
    cx: float
    cy: float
    w: float
    h: float
    round_: float
    turn: float
    role: str  # one of PALETTE

    @property
    def area(self) -> float:
        r = self.round_ * min(self.w, self.h) / 2
        return self.w * self.h - (4 - math.pi) * r * r

    def moved(self, dx: float, dy: float) -> "Shape":
        return Shape(self.cx + dx, self.cy + dy, self.w, self.h, self.round_, self.turn, self.role)


def weights(axes: AxisValues) -> Tuple[float, float, float]:
    """The share of drawn area for each palette color: brand, support,
    neutral. 30, 10 and 60 percent at warmth 0.5; warmth moves area from
    the neutral to the brand and the support, continuously."""
    w = axes.warmth
    return (0.25 + 0.10 * w, 0.05 + 0.10 * w, 0.70 - 0.20 * w)


def digest(axes: AxisValues, brand: str) -> str:
    """Eight hex digits of the inputs: the brand in upper case and the axes
    at three decimals, so #3366ff and #3366FF share one digest."""
    text = f"{brand.upper()}|{','.join(f'{v:.3f}' for v in axes.as_tuple())}"
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _paint(ts: TokenSet, role: str) -> str:
    """A fill that follows the page's scheme inline and falls back to the
    light value in an <img>."""
    return f"var({css_property(role)}, {ts.resolve(role, 'scheme:light')})"


def _n(v: float) -> str:
    v = round(v, 1)
    return str(int(v)) if v == int(v) else f"{v:.1f}"


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def _inside(s: Shape, width: float, height: float, margin: float) -> Shape:
    """The shape moved the least distance that keeps it `margin` inside the
    canvas, by the box around it as turned."""
    box_w, box_h = _turned(s.w, s.h, s.turn)
    half_w, half_h = box_w / 2, box_h / 2
    lo_x, hi_x = half_w + margin, width - half_w - margin
    lo_y, hi_y = half_h + margin, height - half_h - margin
    cx = min(max(s.cx, lo_x), hi_x) if lo_x <= hi_x else width / 2
    cy = min(max(s.cy, lo_y), hi_y) if lo_y <= hi_y else height / 2
    return s.moved(cx - s.cx, cy - s.cy)


def play(axes: AxisValues) -> float:
    """How far art leaves its lines, 0 to 1: the turns, the half drop and
    the corner that runs past the focal center. None over the formal
    part of the axis (regularity 0.7 and up); below it the play grows
    slowly and then fully, so no brief shows a turn or an offset so small
    that it reads as a mistake. Continuous in the axes."""
    t = character.clamp(round((0.7 - character.regularity(axes)) / 0.5, 12))
    return t * t


def accent_side(axes: AxisValues) -> int:
    """Accents per side of the accent group: 1 when playful, 3 when formal."""
    return 1 + int(2 * axes.formality + 0.5)


def _accent_gap(reg: float, span: float, unit: float) -> float:
    """The accents' distance from the focal shape and the plane: a clear
    gap of up to 0.6 of a grid unit when formal, an overlap of up to 0.3
    of the group when playful. It crosses zero low on the formality axis,
    so a mid brief never shows two shapes that merely touch."""
    turn_at = 0.35
    if reg >= turn_at:
        return 0.6 * unit * (reg - turn_at) / (1 - turn_at)
    return -0.3 * span * (turn_at - reg) / (turn_at - 0.2)


def _side(area: float, aspect: float, round_: float) -> Tuple[float, float]:
    """(width, height) of a box of this aspect (width over height) whose
    rounded shape, corners `round_`, covers `area` exactly."""
    k = (4 - math.pi) / 4
    short = min(aspect, 1.0)
    h = math.sqrt(area / (aspect - k * round_ * round_ * short * short))
    return aspect * h, h


def _turned(w: float, h: float, turn: float) -> Tuple[float, float]:
    """Width and height of the box around a w by h shape turned `turn`."""
    c, si = abs(math.cos(math.radians(turn))), abs(math.sin(math.radians(turn)))
    return w * c + h * si, w * si + h * c


def hero(axes: AxisValues, width: int = HERO[0], height: int = HERO[1]) -> List[Shape]:
    """The hero composition, back to front: the neutral plane, the brand
    focal shape, then the support accents. Each is placed against the
    others, never at random. When formal, the plane's upper corner meets
    the focal shape's center, and the accents hang a gap below the focal
    shape, their outer edge in line with its edge; as formality falls the
    corner runs past the center, the accents push out and overlap the
    focal shape, and everything turns. The drawn areas follow weights()
    exactly."""
    f = axes.formality
    loose = play(axes)
    rnd = character.roundness(axes)
    wb, ws, wn = weights(axes)
    unit = height / GRID_ROWS
    margin = MARGIN_UNITS * unit
    # Each layer has its own silhouette: the plane squarer than the
    # roundness, the focal shape and the accents rounder, so no hero is a
    # pile of like shapes. All three are square at roundness 0.
    r_back, r_focal, r_accent = rnd ** 2, rnd ** 0.5, rnd ** 0.35
    turns = (-12 * loose, 10 * loose, 20 * loose)
    n = accent_side(axes)
    stretch = 1 + loose

    def sizes(total: float):
        """The three layers' sizes for a drawn area of `total`. The focal
        shape is the largest saturated shape; the plane is wide when
        playful and a tall panel when formal; the accents are an n by n
        group, one when playful and an even grid of dots when formal, and
        playful accents stretch into capsules, a silhouette of their own."""
        side = _side(wb * total, 1.0, r_focal)[0]
        plane = _side(wn * total, _lerp(1.3, 0.85, f), r_back)
        aw, ah = _side(ws * total / (n * n), stretch, r_accent)
        pitch = ah * stretch * _lerp(1.9, 1.6, f)
        return side, plane, (aw, ah), pitch, aw + pitch * (n - 1)

    # The drawn area is a fixed share of the canvas, a little more when
    # playful, so the open space stays the same whatever the palette; the
    # weights split it. Where the focal shape and the accents under it
    # would not fit the height, everything shrinks together.
    total = COVERAGE * width * height * (1.1 - 0.2 * f)
    for _ in range(3):
        side, (bw, bh), (aw, ah), pitch, span = sizes(total)
        gap = _accent_gap(character.regularity(axes), span, unit)
        tall = (_turned(side, side, turns[1])[1] + side) / 2 + gap + pitch * (n - 1) \
            + _turned(aw, ah, turns[2])[1]
        room = height - 2 * margin
        if tall <= room:
            break
        total *= (room / tall) ** 2
    # The plane's corner runs past the focal center by this much.
    run_x, run_y = side * 0.18 * loose, side * 0.12 * loose

    # The focal center sits on the right, in the middle of the part of the
    # canvas a phone crop keeps, and high enough for the accents and the
    # plane to fit below it.
    fx = width - height * 9 / 32
    reach = _turned(aw, ah, turns[2])[1]
    fy = min(height * 0.42, height - margin - reach - pitch * (n - 1) - gap - side / 2,
             height - margin - _turned(bw, bh, turns[0])[1] / 2 - bh / 2 + run_y)
    fy = max(fy, margin + _turned(side, side, turns[1])[1] / 2)
    focal = Shape(fx, fy, side, side, r_focal, turns[1], "color.decorative.brand")
    corner_x, corner_y = fx + run_x, fy - run_y
    back = _inside(Shape(corner_x - bw / 2, corner_y + bh / 2, bw, bh, r_back, turns[0],
                         "color.decorative.neutral"), width, height, margin)
    # The accent group hangs under the focal shape, its edge toward the
    # canvas edge in line with the focal shape's (formal), or pushed past
    # it (playful); a wide group runs over the plane, in front of it.
    right = min(fx + side / 2 + 0.3 * span * loose, width - margin / 2)
    gx = right - span / 2
    gy = fy + side / 2 + gap + reach / 2 + pitch * (n - 1) / 2
    accents = [Shape(gx + (i - (n - 1) / 2) * pitch, gy + (j - (n - 1) / 2) * pitch,
                     aw, ah, r_accent, turns[2], "color.decorative.support")
               for j in range(n) for i in range(n)]
    return [back, focal, *accents]


def tile_side(axes: AxisValues) -> int:
    """Cells per side of the tile: 2 when playful, 4 at the middle, 6 when
    formal. Always even, so the half drop meets itself across the seam."""
    return 2 * (1 + int(2 * axes.formality + 0.5))


def tile(axes: AxisValues, size: int = TILE) -> List[Shape]:
    """The pattern tile: a lattice of n by n cells, one shape per cell at
    an even pitch. Sizes alternate large and small in a checker rhythm,
    odd rows drop by half a cell as formality falls, and the colors cycle
    so each takes its weight of the cells. Shapes crossing an edge are
    drawn again on the far side."""
    loose = play(axes)
    rnd = character.roundness(axes)
    n = tile_side(axes)
    pitch = size / n
    large = pitch * _lerp(0.62, 0.5, axes.formality)
    small = large * _lerp(0.55, 0.7, axes.formality)
    order = _color_cycle(weights(axes), n * n)
    shapes: List[Shape] = []
    for row in range(n):
        for col in range(n):
            big = (row + col) % 2 == 0
            s = large if big else small
            drop = (row % 2) * pitch / 2 * loose
            turn = loose * 16 * (1 if big else -1)
            shape = Shape((col + 0.5) * pitch + drop, (row + 0.5) * pitch, s, s, rnd, turn,
                          order[row * n + col])
            shapes += _wrapped(shape, size)
    return shapes


def _color_cycle(ws: Tuple[float, float, float], count: int) -> List[str]:
    """Each cell's color, so every color takes its share of the cells and
    they spread evenly: cell k takes the color whose running quota is
    furthest behind (ties by palette order)."""
    given = [0, 0, 0]
    out = []
    for k in range(count):
        lag = [ws[i] * (k + 1) - given[i] for i in range(3)]
        pick = max(range(3), key=lambda i: (round(lag[i], 9), -i))
        given[pick] += 1
        out.append(PALETTE[pick])
    return out


def _wrapped(s: Shape, size: float) -> List[Shape]:
    """The shape and its copies across every edge it crosses."""
    reach = math.hypot(s.w, s.h) / 2
    xs = [0.0] + ([size] if s.cx - reach < 0 else []) + ([-size] if s.cx + reach > size else [])
    ys = [0.0] + ([size] if s.cy - reach < 0 else []) + ([-size] if s.cy + reach > size else [])
    return [s.moved(dx, dy) for dy in ys for dx in xs]


def _rect(s: Shape, fill: str) -> str:
    rx = s.round_ * min(s.w, s.h) / 2
    return (f'<rect x="{_n(s.cx - s.w / 2)}" y="{_n(s.cy - s.h / 2)}" width="{_n(s.w)}" '
            f'height="{_n(s.h)}" rx="{_n(rx)}" transform="rotate({_n(s.turn)} {_n(s.cx)} '
            f'{_n(s.cy)})" style="fill: {fill}{_quiet(s.role)}"/>')


def _quiet(role: str) -> str:
    """The neutral is the quiet 60 percent: drawn at QUIET opacity over the
    page, so it recedes behind the brand and the support in both schemes."""
    return f"; fill-opacity: {QUIET}" if role == "color.decorative.neutral" else ""


def _svg(width: int, height: int, body: Sequence[str], defs: Sequence[str] = (),
         size: str = 'width="100%" height="100%" preserveAspectRatio="xMaxYMid slice"') -> str:
    lines = [HEAD, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
                   f'{size} aria-hidden="true" focusable="false">']
    if defs:
        lines += ["  <defs>", *[f"    {d}" for d in defs], "  </defs>"]
    lines += [f"  {b}" for b in body] + ["</svg>"]
    return "\n".join(lines) + "\n"


def gradient_angle(axes: AxisValues) -> int:
    """The wash's angle: 90 degrees (left to right) at contrast 0, turning
    to 180 (top to bottom) at contrast 1."""
    return int(90 + 90 * axes.contrast)


def art_files(ts: TokenSet, axes: AxisValues, brand: str) -> Dict[str, str]:
    """The three art files, by published name. Empty when the set lacks the
    decorative colors (a partial build)."""
    if not all(ts.has(role) for role in PALETTE):
        return {}
    paints = {role: _paint(ts, role) for role in PALETTE}
    pattern = _svg(TILE, TILE, [_rect(s, paints[s.role]) for s in tile(axes)],
                   size=f'width="{TILE}" height="{TILE}"')
    shapes = _svg(HERO[0], HERO[1], [_rect(s, paints[s.role]) for s in hero(axes)])
    wash = f"uxs-art-{digest(axes, brand)}-wash"
    stops = [f'<linearGradient id="{wash}" gradientTransform="rotate({gradient_angle(axes)} '
             '0.5 0.5)">',
             f'  <stop offset="0" style="stop-color: {_paint(ts, "color.surface.tint")}"/>',
             f'  <stop offset="{_n(0.4 + 0.3 * axes.formality)}" style="stop-color: '
             f'{paints["color.decorative.brand"]}"/>',
             f'  <stop offset="1" style="stop-color: {paints["color.decorative.support"]}"/>',
             "</linearGradient>"]
    gradient = _svg(HERO[0], HERO[1], [f'<rect width="{HERO[0]}" height="{HERO[1]}" '
                                       f'fill="url(#{wash})"/>'], stops)
    return {FILES[0]: pattern, FILES[1]: shapes, FILES[2]: gradient}


def report_lines() -> List[str]:
    return [
        "art/shapes.svg: a hero composition, a neutral plane, the brand's focal shape and "
        "support accents on the right third, with the left open for a heading. It keeps the "
        "focal shape in a phone crop; under dir=\"rtl\" mirror it with transform: scaleX(-1).",
        "art/pattern.svg: a 240px tile that repeats without seams behind a section, a card or "
        "an empty state; as a CSS background it repeats at 240px, and background-size scales it.",
        "art/gradient.svg: a wash from the brand tint to the supporting accent; contrast turns "
        "it from left to right toward top to bottom.",
        "Each is decoration: place it with an empty alt (alt=\"\") or as a CSS background, "
        "never as the only carrier of a message. Inline it to follow dark mode; as an image "
        "it shows the light colors. Colors sit in style attributes, so a policy that blocks "
        "inline styles needs the image form.",
        "Text over the art, such as a headline across a full-bleed hero, sits on a layer of "
        "color.media.veil in color.text.on-media, and so do the label, edge and focus ring of "
        "a control there; the veil is measured over the art's own colors, so light art keeps "
        "its colors. Keep the photo scrim (imagery.scrim) for photos.",
    ]
