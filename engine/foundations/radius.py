"""Radius foundation: a corner scale set by the roundness the geometry and
formality axes give, and the roles that use it.

The base corner runs from 0px for a sharp, formal brand to 14px for a
soft, playful one (character.roundness); the scale steps are fixed
multiples of it, so controls, cards and dialogs round together. Rounded
brands move chips, then controls, to the pill shape. A check box's box and
a field that runs to several lines never do: a round box reads as a radio
button, and a stadium clips a paragraph's first and last lines. Containers
nest, so a dialog is never less rounded than a card inside it.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations import character
from engine.foundations.foundation import (
    BrandInputs, Foundation, Generated, direct_alias, is_step, numbered_steps, typed)
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.values import dimension_px
from engine.synthesizer.axes import AxisValues

# radius.<n> = base corner x multiple
MULTIPLES = (0, 0.5, 1, 1.5, 2, 3, 4)
PILL_PX = 9999
# Our floor for a pill: at 999px a corner is larger than any control's
# height. radius-pill holds radius.pill to it, and radius-nesting sets any
# role at or above it aside as a pill.
PILL_FLOOR_PX = 999
CHIP_PILL_FROM, CONTROL_PILL_FROM = 0.6, 0.85  # roundness thresholds
MAX_BASE_PX = 14


def base_corner(roundness: float) -> int:
    """0px at roundness 0 to 14px at roundness 1, to the nearest pixel."""
    return int(MAX_BASE_PX * roundness + 0.5)


def scale(roundness: float) -> List[int]:
    """Corner sizes for radius.0 .. radius.6, strictly increasing."""
    b = base_corner(roundness)
    out: List[int] = []
    for m in MULTIPLES:
        v = int(b * m + 0.5)
        out.append(max(v, out[-1] + 1) if out else v)
    return out


def roles(roundness: float) -> Dict[str, str]:
    """Semantic radius role -> primitive it aliases."""
    return {
        "radius.joined": "radius.0",
        "radius.chip": "radius.round" if roundness >= CHIP_PILL_FROM else "radius.1",
        "radius.control": "radius.round" if roundness >= CONTROL_PILL_FROM else "radius.2",
        # A small square mark such as a check box: half the control corner,
        # never a pill.
        "radius.box": "radius.1",
        # A control that runs to several lines: the control corner, and the
        # card corner once controls are pills, never a pill itself.
        "radius.area": "radius.3" if roundness >= CONTROL_PILL_FROM else "radius.2",
        "radius.card": "radius.3",
        "radius.dialog": "radius.4",
        "radius.pill": "radius.round",
        # Photos and illustrations: sharper than a card in a sharp brand,
        # rounder in a soft one.
        "radius.media": f"radius.{2 + min(2, int(roundness * 3))}",
    }


def generate_radius(axes: AxisValues) -> Generated:
    r = character.roundness(axes)
    ts = TokenSet()
    for n, px in enumerate(scale(r)):
        ts.add(Token(f"radius.{n}", "dimension", {"value": px, "unit": "px"}))
    ts.add(Token("radius.round", "dimension", {"value": PILL_PX, "unit": "px"}))
    notes: List[str] = [f"radius: roundness {r:.2f} from geometry {axes.geometry:g} and formality "
                        f"{axes.formality:g}, base corner {base_corner(r)}px"]
    for role, prim in roles(r).items():
        ts.add(Token(role, "dimension", "{" + prim + "}", layer="semantic"))
        if prim == "radius.round" and role != "radius.pill":
            notes.append(f"{role}: pill shape, roundness {r:.2f} is soft")
    return Generated(tokens=ts, notes=notes)


# Every role is a dimension (the role names do not depend on geometry). The
# build's role-types check reports any other type once, and the checks
# below skip it.
ROLE_TYPES: Dict[str, str] = {role: "dimension" for role in roles(0.0)}


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _px(ts: TokenSet, path: str) -> float:
    return dimension_px(ts.resolve(path))


# Shapes from the innermost out: a chip sits in a control's row, a control
# in a card, a card in a dialog. Each is strictly less round than the next,
# unless both are square; a role at or above PILL_FLOOR_PX is a pill, a
# shape of its own, and sits outside the order.
NESTING = ("radius.chip", "radius.control", "radius.card", "radius.dialog")


def _nesting(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in NESTING if _typed(ts, r) and _px(ts, r) < PILL_FLOOR_PX]
    out = []
    for inner, outer in zip(present, present[1:]):
        a, b = _px(ts, inner), _px(ts, outer)
        if a > b:
            out.append(f"{inner} ({a:g}px) is rounder than {outer} ({b:g}px); a container is "
                       f"never rounder than the one it sits in, so point {outer} at a larger "
                       "step")
        elif a == b and a != 0:
            out.append(f"{inner} ({a:g}px) is as round as {outer} ({b:g}px); a shape inside "
                       f"another is less round than its container, so point {outer} at a "
                       "larger step")
    return out


def _joined(ts: TokenSet, mode: str) -> List[str]:
    if _typed(ts, "radius.joined") and _px(ts, "radius.joined") != 0:
        return [f"radius.joined is {_px(ts, 'radius.joined'):g}px; shared edges must be square, "
                "so point it at radius.0"]
    return []


def _pill(ts: TokenSet, mode: str) -> List[str]:
    if _typed(ts, "radius.pill") and _px(ts, "radius.pill") < PILL_FLOOR_PX:
        return [f"radius.pill is {_px(ts, 'radius.pill'):g}px; a pill needs a radius larger than "
                "any control's height, so point it at radius.round"]
    return []


def _scale_order(ts: TokenSet, mode: str) -> List[str]:
    steps = numbered_steps(ts, "radius.", others=False)
    return [f"{b} is not larger than {a}; keep the radius scale strictly increasing"
            for a, b in zip(steps, steps[1:]) if _px(ts, a) >= _px(ts, b)]


def _on_scale(ts: TokenSet, mode: str) -> List[str]:
    """Every role that aliases a primitive aliases radius.<n> or
    radius.round. A role holding its value directly is left to the value
    checks."""
    out = []
    for role in ROLE_TYPES:
        if not _typed(ts, role):
            continue
        target = direct_alias(ts, role, mode)
        if target is not None and target != "radius.round" and not is_step(target, "radius."):
            out.append(f"{role} points at {target}, which is not a step of the radius scale; "
                       "corners come from radius.<n> or radius.round, so point it at one of "
                       "those")
    return out


CHECKS: Tuple[Check, ...] = (
    Check("radius-nesting", "system", _nesting),
    Check("radius-joined", "system", _joined),
    Check("radius-pill", "system", _pill),
    Check("radius-scale-order", "system", _scale_order),
    Check("radius-on-scale", "system", _on_scale),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_radius(axes)


FOUNDATION = Foundation(name="radius", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
