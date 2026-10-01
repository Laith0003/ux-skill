"""How different two built systems are, read from their tokens.

character_of(ts) reads two sets of features from a built system.

The glance set is what a person sees on a first look at a static screen:
the main button's color, the link color, the supporting accent, the tint
of the neutrals, the status colors' hues and chroma, the display and text
faces, corners, the hero's size, weight and tracking, the body size, the
card shadow, spacing and the hero image's ratio. distance(a, b) is their
weighted mean scaled difference, 0 for identical systems and 1 for systems
that differ in everything. The distinctness floors apply to it.

The behavior set is what shows only in use: the entrance duration, the
expressive curve's overshoot, the mono face and the focus ring's width.
behavior(a, b) measures it apart, and distance never counts it, so two
systems that differ only in how they move or in their focus ring are not
distinct at a glance.

Each numeric feature is scaled by SPAN, the widest the engine goes on it
over the 128 corners of the axes with any of REFERENCE_BRANDS, a mid grey
and four saturated brands (the body size by the audience's age bands,
since the axes do not move it), and a test pins every SPAN to that
measured range. A color is a point in OKLab, the
neutral tint a point in the OKLab a/b plane and the status hues a point in
the four hue turns; each compares by straight-line distance. A named
feature (a face) counts 0 when equal and 1 when not.
"""
from __future__ import annotations

import math
from types import MappingProxyType
from typing import Any, Dict, Mapping, Tuple

from engine.foundations.character import STATUS_HUES, hue_delta
from engine.foundations.color_math import hex_to_oklch
from engine.foundations.tokens import TokenSet
from engine.foundations.values import dimension_px

LIGHT = "scheme:light,contrast:standard"
# A mid grey leads nothing (decisions/brand-leads-the-role.md): its role
# and neutrals are the axes' alone. A saturated brand leads its button and
# link, and the axes show in its supporting accent and neutrals instead.
# The spans are the widest over all five, and the corner floors hold on
# each (decisions/distinctness-on-saturated-brands.md).
REFERENCE_BRAND = "#808080"
SATURATED_REFERENCES: Tuple[str, ...] = ("#3366FF", "#FF6A00", "#0D9488", "#7C3AED")
REFERENCE_BRANDS: Tuple[str, ...] = (REFERENCE_BRAND,) + SATURATED_REFERENCES

# How much each glance feature counts. 2 for what leads the first screen:
# the main action's color, the neutrals that tint the page and the grey
# text, and the face that sets the headline. 1 for each other thing a
# person sees. 0.5 for a detail inside another thing (the hero's tracking)
# and for each of the card shadow's two numbers, which make one shadow.
WEIGHTS: Mapping[str, float] = MappingProxyType({
    "button": 2.0, "neutral": 2.0, "face.display": 2.0,
    "link": 1.0, "support": 1.0, "status.hue": 1.0, "status.chroma": 1.0,
    "face.text": 1.0, "radius.control": 1.0, "radius.card": 1.0,
    "hero.px": 1.0, "hero.weight": 1.0, "body.px": 1.0,
    "card.padding": 1.0, "region.gap": 1.0, "hero.ratio": 1.0,
    "hero.tracking": 0.5, "shadow.alpha": 0.5, "shadow.blur": 0.5,
})
# What shows only in use; behavior() weighs these equally.
BEHAVIOR: Tuple[str, ...] = ("arrive.ms", "overshoot", "ring.px", "face.mono")
NAMED: Tuple[str, ...] = ("face.display", "face.text", "face.mono")
# The widest the engine goes on each numeric feature (see the docstring).
SPAN: Mapping[str, float] = MappingProxyType({
    "button": 0.37, "link": 0.13, "support": 0.25, "neutral": 0.021,
    "status.hue": 38.0, "status.chroma": 0.098,
    "radius.control": 58.0, "radius.card": 18.0,
    "hero.px": 71.0, "hero.weight": 250.0, "hero.tracking": 4.7, "body.px": 2.0,
    "shadow.alpha": 0.14, "shadow.blur": 2.0,
    "card.padding": 16.0, "region.gap": 64.0, "hero.ratio": 1.0,
    "arrive.ms": 450.0, "overshoot": 0.8, "ring.px": 1.0,
})
# Control corners past this read as a pill; any larger radius looks the same.
PILL_PX = 60.0
# Our floor on the glance distance between two systems built at different
# corners of the axes, read on what one section shows: below it a section
# looks the same whatever the brand and brief.
GLANCE_FLOOR = 0.20
# The glance features a bound role shows, by role prefix.
FEATURE_ROLES: Mapping[str, Tuple[str, ...]] = MappingProxyType({
    "button": ("color.action.primary",), "link": ("color.text.link",),
    "support": ("color.text.support", "color.surface.band", "color.text.accent"),
    "neutral": ("color.surface.", "color.text.muted", "color.text.default", "color.line."),
    "face.display": ("type.text.display", "type.text.hero", "type.text.heading-1",
                     "type.text.section-title", "type.text.figure"),
    "face.text": ("type.text.body", "type.text.ui", "type.text.fine", "type.text.label",
                  "type.text.heading-2", "type.text.heading-3"),
    "radius.control": ("radius.control",), "radius.card": ("radius.card", "radius.media"),
    "hero.px": ("type.text.display", "type.text.hero"),
    "hero.weight": ("type.text.display", "type.text.hero"),
    "hero.tracking": ("type.text.display", "type.text.hero"),
    "body.px": ("type.text.body",), "shadow.alpha": ("elevation.",), "shadow.blur": ("elevation.",),
    "card.padding": ("space.card.padding",), "region.gap": ("layout.region-gap", "layout.landing-gap"),
    "hero.ratio": ("imagery.ratio",),
})


def features_shown(roles) -> Tuple[str, ...]:
    """The glance features a set of bound roles shows, in WEIGHTS order."""
    return tuple(k for k in WEIGHTS
                 if any(r.startswith(p) for r in roles for p in FEATURE_ROLES.get(k, ())))


def _px(v: Dict[str, Any]) -> float:
    return dimension_px(v)


def _lab(hx: str) -> Tuple[float, float, float]:
    L, C, H = hex_to_oklch(hx[:7])
    return L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))


def character_of(ts: TokenSet) -> Dict[str, Any]:
    """The glance and behavior features, from a built token set."""
    hero = ts.resolve("type.text.hero")
    shadow = ts.resolve("elevation.card")[0]
    curve = ts.resolve("motion.expressive.curve")
    status = {s: hex_to_oklch(ts.resolve(f"color.{s}.500")) for s in STATUS_HUES}
    return {
        "button": _lab(ts.resolve("color.action.primary", LIGHT)),
        "link": _lab(ts.resolve("color.text.link", LIGHT)),
        "support": _lab(ts.resolve("color.support.500")),
        "neutral": _lab(ts.resolve("color.neutral.500"))[1:],
        "status.hue": tuple(hue_delta(base, status[s][2]) for s, base in STATUS_HUES.items()),
        "status.chroma": sum(c for _, c, _ in status.values()) / len(status),
        "radius.control": min(_px(ts.resolve("radius.control")), PILL_PX),
        "radius.card": _px(ts.resolve("radius.card")),
        "body.px": _px(ts.resolve("type.text.body")["fontSize"]),
        "hero.px": _px(hero["fontSize"]), "hero.weight": float(hero["fontWeight"]),
        "hero.tracking": hero["letterSpacing"]["value"],
        "shadow.alpha": int(shadow["color"][7:9], 16) / 255 if len(shadow["color"]) == 9 else 1,
        "shadow.blur": _px(shadow["blur"]),
        "card.padding": _px(ts.resolve("space.card.padding")),
        "region.gap": _px(ts.resolve("layout.region-gap.desktop")),
        "hero.ratio": ts.resolve("imagery.ratio.hero"),
        "face.display": ts.resolve("type.face.display")[0],
        "face.text": ts.resolve("type.face.text")[0],
        "arrive.ms": float(ts.resolve("motion.arrive.duration")["value"]),
        "overshoot": max(0.0, curve[1] - 1.0, curve[3] - 1.0),
        "ring.px": _px(ts.resolve("border.focus-ring.width")),
        "face.mono": ts.resolve("type.face.mono")[0],
    }


def apart(key: str, a: Any, b: Any) -> float:
    """How far apart two values of one feature are, 0 to 1."""
    if key in NAMED:
        return 0.0 if a == b else 1.0
    raw = math.dist(a, b) if isinstance(a, tuple) else abs(a - b)
    return min(1.0, raw / SPAN[key])


def distance(a: Dict[str, Any], b: Dict[str, Any], keys=None) -> float:
    """The weighted mean of the glance features apart, 0 to 1; with
    ``keys``, of those features only (what one section shows)."""
    weights = {k: w for k, w in WEIGHTS.items() if keys is None or k in keys}
    if not weights:
        raise ValueError("keys: name at least one glance feature, from "
                         + ", ".join(WEIGHTS))
    total = sum(w * apart(k, a[k], b[k]) for k, w in weights.items())
    return round(total / sum(weights.values()), 4)


def behavior(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    """The mean of the behavior features apart, 0 to 1."""
    return round(sum(apart(k, a[k], b[k]) for k in BEHAVIOR) / len(BEHAVIOR), 4)
