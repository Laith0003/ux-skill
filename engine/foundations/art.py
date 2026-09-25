"""Generative brand art: SVG patterns, shapes and a gradient built from the
axes and the built colors, so a page is never empty for want of photos.

Geometry sets the shape language (a square that rounds into a circle as
roundness grows), warmth the palette (warm systems lean on the brand and
support accents, cool ones on the neutral), formality the density and
regularity (formal art is many small shapes on a grid, playful art a few
large ones scattered and turned). Positions come from a generator seeded
by a digest of the inputs, so the same system always draws the same art.

Every file is decoration: the root is aria-hidden, there is no title, and
the report says to place it with an empty alt. Colors are written as CSS
custom properties with the light values as fallbacks, so an inline SVG
follows the page's scheme and an <img> shows the light version.
"""
from __future__ import annotations

import hashlib
from typing import Dict, List, Tuple

from engine.foundations import character
from engine.foundations.tokens import TokenSet, css_property
from engine.synthesizer.axes import AxisValues

ART_DIR = "art"
FILES: Tuple[str, ...] = (f"{ART_DIR}/pattern.svg", f"{ART_DIR}/shapes.svg",
                          f"{ART_DIR}/gradient.svg")
PALETTE = ("color.decorative.brand", "color.decorative.support", "color.decorative.neutral")
HEAD = ("<!-- Decorative brand art generated with the design system. Place it with an empty "
        "alt; it carries no meaning. -->")


class _Rand:
    """A small deterministic generator (a 64-bit LCG) seeded from text."""

    def __init__(self, seed: str):
        self.state = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16], 16)

    def next(self) -> float:
        self.state = (self.state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        return (self.state >> 11) / float(1 << 53)


def _paint(ts: TokenSet, role: str) -> str:
    """A fill that follows the page's scheme inline and falls back to the
    light value in an <img>."""
    return f"var({css_property(role)}, {ts.resolve(role, 'scheme:light')})"


def weights(axes: AxisValues) -> Tuple[float, float, float]:
    """How often each palette color is drawn: brand, support, neutral."""
    w = axes.warmth
    return (0.35 + 0.25 * w, 0.15 + 0.25 * w, 0.5 - 0.5 * w)


def _pick(r: _Rand, ws: Tuple[float, ...]) -> int:
    x, total = r.next() * sum(ws), 0.0
    for i, w in enumerate(ws):
        total += w
        if x < total:
            return i
    return len(ws) - 1


def _n(v: float) -> str:
    return f"{v:.1f}".rstrip("0").rstrip(".") if v != int(v) else str(int(v))


def _shape(x: float, y: float, size: float, roundness: float, turn: float, fill: str) -> str:
    rx = roundness * size / 2
    return (f'<rect x="{_n(x - size / 2)}" y="{_n(y - size / 2)}" width="{_n(size)}" '
            f'height="{_n(size)}" rx="{_n(rx)}" transform="rotate({_n(turn)} {_n(x)} {_n(y)})" '
            f'style="fill: {fill}"/>')


def _svg(width: int, height: int, body: List[str], defs: List[str] = ()) -> str:
    lines = [HEAD, f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
                   'width="100%" height="100%" preserveAspectRatio="xMidYMid slice" '
                   'aria-hidden="true" focusable="false">']
    if defs:
        lines += ["  <defs>", *[f"    {d}" for d in defs], "  </defs>"]
    lines += [f"  {b}" for b in body] + ["</svg>"]
    return "\n".join(lines) + "\n"


def _composition(ts: TokenSet, axes: AxisValues, seed: str, width: int, height: int,
                 scale: float) -> List[str]:
    """Shapes for one canvas: count and size by formality, jitter and turn
    by regularity, rounding by roundness, colors by warmth."""
    r = _Rand(seed)
    reg = character.regularity(axes)
    rnd = character.roundness(axes)
    cols = max(2, int(3 + 5 * axes.formality + 0.5))
    rows = max(2, int(cols * height / width + 0.5))
    cell_w, cell_h = width / cols, height / rows
    size = min(cell_w, cell_h) * (0.9 - 0.4 * axes.formality) * scale
    paints = [_paint(ts, role) for role in PALETTE]
    ws = weights(axes)
    out = []
    for row in range(rows):
        for col in range(cols):
            if r.next() > 0.35 + 0.55 * axes.formality:
                continue  # playful art leaves more of the canvas open
            jx = (r.next() - 0.5) * cell_w * (1 - reg)
            jy = (r.next() - 0.5) * cell_h * (1 - reg)
            x = (col + 0.5) * cell_w + jx
            y = (row + 0.5) * cell_h + jy
            grow = 1 + (r.next() - 0.5) * (1 - reg)
            turn = (r.next() - 0.5) * 90 * (1 - reg)
            out.append(_shape(x, y, size * grow, rnd, turn, paints[_pick(r, ws)]))
    return out


def art_files(ts: TokenSet, axes: AxisValues, brand: str) -> Dict[str, str]:
    """The three art files, by published name. Empty when the set lacks the
    decorative colors (a partial build)."""
    if not all(ts.has(role) for role in PALETTE):
        return {}
    seed = f"{brand}|{','.join(f'{v:.3f}' for v in axes.as_tuple())}"
    pattern = _svg(240, 240, _composition(ts, axes, seed + "|pattern", 240, 240, 0.8))
    shapes = _svg(1200, 800, _composition(ts, axes, seed + "|shapes", 1200, 800, 1.6))
    angle = int(90 + 90 * axes.contrast)
    stops = [f'<linearGradient id="brand" gradientTransform="rotate({angle} 0.5 0.5)">',
             f'  <stop offset="0" style="stop-color: {_paint(ts, "color.surface.tint")}"/>',
             f'  <stop offset="{_n(0.4 + 0.3 * axes.formality)}" style="stop-color: '
             f'{_paint(ts, "color.decorative.brand")}"/>',
             f'  <stop offset="1" style="stop-color: {_paint(ts, "color.decorative.support")}"/>',
             "</linearGradient>"]
    gradient = _svg(1200, 800, ['<rect width="1200" height="800" fill="url(#brand)"/>'], stops)
    return {FILES[0]: pattern, FILES[1]: shapes, FILES[2]: gradient}


def report_lines() -> List[str]:
    return [
        "art/pattern.svg: a tile to repeat behind a section, a card or an empty state.",
        "art/shapes.svg: a large composition for a hero or a band with no photo.",
        "art/gradient.svg: a wash from the brand tint to the supporting accent.",
        "Each is decoration: place it with an empty alt (alt=\"\") or as a CSS background, "
        "never as the only carrier of a message. Inline it to follow dark mode; as an image "
        "it shows the light colors.",
    ]
