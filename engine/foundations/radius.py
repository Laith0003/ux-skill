"""Radius foundation: a corner scale set by the geometry axis and the
roles that use it.

The base corner is 2px for a sharp brand (geometry 0) and 12px for a soft
one (geometry 1); the scale steps are fixed multiples of it. Rounded
brands move chips, then controls, to the pill shape. Containers nest, so
a dialog is never less rounded than a card inside it.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

# radius.<n> = base corner x multiple
MULTIPLES = (0, 0.5, 1, 1.5, 2, 3, 4)
PILL_PX = 9999
CHIP_PILL_FROM, CONTROL_PILL_FROM = 0.6, 0.85  # geometry thresholds


def base_corner(geometry: float) -> int:
    """2px at geometry 0 to 12px at geometry 1, in 2px steps."""
    return 2 * int(1 + 5 * geometry + 0.5)


def scale(geometry: float) -> List[int]:
    """Corner sizes for radius.0 .. radius.6, strictly increasing."""
    b = base_corner(geometry)
    out: List[int] = []
    for m in MULTIPLES:
        v = int(b * m + 0.5)
        out.append(max(v, out[-1] + 1) if out else v)
    return out


def roles(geometry: float) -> Dict[str, str]:
    """Semantic radius role -> primitive it aliases."""
    return {
        "radius.joined": "radius.0",
        "radius.chip": "radius.round" if geometry >= CHIP_PILL_FROM else "radius.1",
        "radius.control": "radius.round" if geometry >= CONTROL_PILL_FROM else "radius.2",
        "radius.card": "radius.3",
        "radius.dialog": "radius.4",
        "radius.pill": "radius.round",
    }


def generate_radius(axes: AxisValues) -> Generated:
    ts = TokenSet()
    for n, px in enumerate(scale(axes.geometry)):
        ts.add(Token(f"radius.{n}", "dimension", {"value": px, "unit": "px"}))
    ts.add(Token("radius.round", "dimension", {"value": PILL_PX, "unit": "px"}))
    notes: List[str] = []
    for role, prim in roles(axes.geometry).items():
        ts.add(Token(role, "dimension", "{" + prim + "}", layer="semantic"))
        if prim == "radius.round" and role != "radius.pill":
            notes.append(f"{role}: pill shape, geometry {axes.geometry:g} is soft")
    return Generated(tokens=ts, notes=notes)


def _px(ts: TokenSet, path: str) -> float:
    return ts.resolve(path)["value"]


def _nesting(ts: TokenSet, mode: str) -> List[str]:
    if not (ts.has("radius.card") and ts.has("radius.dialog")):
        return []
    card, dialog = _px(ts, "radius.card"), _px(ts, "radius.dialog")
    if card <= dialog:
        return []
    return [f"radius.card ({card:g}px) is rounder than radius.dialog ({dialog:g}px); a container "
            "is never rounder than the one it sits in, so point radius.dialog at a larger step"]


def _joined(ts: TokenSet, mode: str) -> List[str]:
    if ts.has("radius.joined") and _px(ts, "radius.joined") != 0:
        return [f"radius.joined is {_px(ts, 'radius.joined'):g}px; shared edges must be square, "
                "so point it at radius.0"]
    return []


def _pill(ts: TokenSet, mode: str) -> List[str]:
    if ts.has("radius.pill") and _px(ts, "radius.pill") < 999:
        return [f"radius.pill is {_px(ts, 'radius.pill'):g}px; a pill needs a radius larger than "
                "any control's height, so point it at radius.round"]
    return []


def _scale_order(ts: TokenSet, mode: str) -> List[str]:
    steps = [t.path for t in ts.tokens() if t.layer == "primitive"
             and t.path.startswith("radius.") and t.path.split(".")[1].isdigit()]
    return [f"{b} is not larger than {a}; keep the radius scale strictly increasing"
            for a, b in zip(steps, steps[1:]) if _px(ts, a) >= _px(ts, b)]


CHECKS: Tuple[Check, ...] = (
    Check("radius-nesting", "system", _nesting),
    Check("radius-joined", "system", _joined),
    Check("radius-pill", "system", _pill),
    Check("radius-scale-order", "system", _scale_order),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_radius(axes)


FOUNDATION = Foundation(name="radius", generate=_generate, checks=CHECKS)
