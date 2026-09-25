"""How different two built systems are, read from their tokens.

character_of(ts) reads a fixed set of features that a person sees at a
glance: the main button's color, the page tint, corners, faces, sizes,
weights, letter spacing, shadow, the ring, motion, spacing and the hero
ratio. Each numeric feature is scaled to 0 to 1 over the range the engine
can produce; each named feature (a face, the brand's role) counts 0 when
equal and 1 when not. distance(a, b) is the mean absolute difference over
every feature, 0 for identical systems and 1 for systems that differ in
everything. The distinctness tests hold opposite corners of the axes and
the four site trial briefs apart by it.
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from engine.foundations.color_math import hex_to_oklch
from engine.foundations.tokens import TokenSet

LIGHT = "scheme:light,contrast:standard"
# The most two systems can differ on each feature, for scaling to 0..1.
SPAN: Dict[str, float] = {
    "button.L": 1.0, "button.a": 0.5, "button.b": 0.5,
    "page.a": 0.1, "page.b": 0.1,
    "radius.control": 60.0, "radius.card": 21.0,
    "body.px": 4.0, "hero.px": 70.0, "hero.weight": 500.0, "hero.tracking": 4.0,
    "shadow.alpha": 0.3, "shadow.blur": 30.0, "ring.px": 3.0,
    "reveal.ms": 150.0, "reveal.overshoot": 1.5,
    "card.padding": 24.0, "region.gap": 64.0, "hero.ratio": 1.0,
}
NAMED: Tuple[str, ...] = ("face.display", "face.text", "face.mono", "brand.role")


def _px(v: Dict[str, Any]) -> float:
    return v["value"] * (16 if v.get("unit") == "rem" else 1)


def _lab(hx: str) -> Tuple[float, float, float]:
    L, C, H = hex_to_oklch(hx[:7])
    return L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))


def character_of(ts: TokenSet) -> Dict[str, Any]:
    """The features distance compares, from a built token set."""
    button = _lab(ts.resolve("color.action.primary", LIGHT))
    page = _lab(ts.resolve("color.surface.page", LIGHT))
    hero = ts.resolve("type.text.hero")
    shadow = ts.resolve("elevation.card")[0]
    raw = ts.raw("color.action.primary", LIGHT)
    role = "ink" if "neutral" in raw else "brand"
    if role == "ink":
        role = "edge" if "neutral" in ts.raw("color.text.link", LIGHT) else "accent"
    return {
        "button.L": button[0], "button.a": button[1], "button.b": button[2],
        "page.a": page[1], "page.b": page[2],
        "radius.control": min(_px(ts.resolve("radius.control")), 60.0),
        "radius.card": _px(ts.resolve("radius.card")),
        "body.px": _px(ts.resolve("type.text.body")["fontSize"]),
        "hero.px": _px(hero["fontSize"]), "hero.weight": float(hero["fontWeight"]),
        "hero.tracking": hero["letterSpacing"]["value"],
        "shadow.alpha": int(shadow["color"][7:9], 16) / 255 if len(shadow["color"]) == 9 else 1,
        "shadow.blur": _px(shadow["blur"]),
        "ring.px": _px(ts.resolve("border.focus-ring.width")),
        "reveal.ms": _px(ts.resolve("motion.reveal.duration")),
        "reveal.overshoot": ts.resolve("motion.reveal.curve")[1],
        "card.padding": _px(ts.resolve("space.card.padding")),
        "region.gap": _px(ts.resolve("layout.region-gap.desktop")),
        "hero.ratio": ts.resolve("imagery.ratio.hero"),
        "face.display": ts.resolve("type.face.display")[0],
        "face.text": ts.resolve("type.face.text")[0],
        "face.mono": ts.resolve("type.face.mono")[0],
        "brand.role": role if role != "brand" else "fill",
    }


def distance(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    """Mean absolute difference over every feature, scaled to 0..1."""
    parts = [min(1.0, abs(a[k] - b[k]) / span) for k, span in SPAN.items()]
    parts += [0.0 if a[k] == b[k] else 1.0 for k in NAMED]
    return round(sum(parts) / len(parts), 4)
