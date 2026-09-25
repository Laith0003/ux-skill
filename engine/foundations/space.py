"""Spacing foundation: a 4px-unit scale and the spacing roles that use it.

Primitives are space.<n>, n units of BASE_UNIT pixels. Each role has an
airy and a dense position on that scale; the density axis interpolates
between them for the comfortable mode, and compact sits one step lower,
never below the role's floor. Directional roles use logical names
(padding-inline, padding-block), so they read the same in both
directions.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations.foundation import (
    BrandInputs, Foundation, Generated, direct_alias, is_step, numbered_steps, typed)
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.values import dimension_px
from engine.synthesizer.axes import AxisValues

BASE_UNIT = 4  # px; every step lands on a 4px grid
UNITS = (0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48)

# role -> (units when the density axis is 0, units when it is 1, compact floor)
ROLES: Dict[str, Tuple[int, int, int]] = {
    "space.control.gap": (3, 2, 2),
    "space.control.padding-inline": (5, 3, 2),
    "space.control.padding-block": (3, 2, 1),
    "space.control.padding-inline-large": (8, 6, 4),
    "space.control.padding-block-large": (4, 3, 2),
    "space.field.label-gap": (2, 1, 1),
    "space.field.message-gap": (2, 1, 1),
    "space.table.cell-padding-inline": (4, 3, 2),
    "space.table.cell-padding-block": (3, 2, 1),
    "space.text.gap": (4, 2, 1),
    "space.list.gap": (4, 2, 1),
    "space.group.gap": (8, 4, 2),
    "space.card.padding": (8, 4, 3),
    "space.region.gap": (32, 16, 12),
}
# Roles whose values must grow in this order (a gap inside a group never
# exceeds the gap between groups, and so on).
HIERARCHY = ("space.text.gap", "space.group.gap", "space.region.gap")
MIN_CONTROL_GAP_PX = 8  # our floor between adjacent controls


def _px(units: int) -> Dict[str, int]:
    return {"value": units * BASE_UNIT, "unit": "px"}


def snap(units: float, steps: Tuple[int, ...] = UNITS) -> int:
    """The step nearest `units`; a tie goes to the larger step. Layout
    snaps on these same rules, so the two move together."""
    return min(steps, key=lambda u: (abs(u - units), -u))


def compact_step(comfortable: int, floor: int) -> int:
    """The compact step for a comfortable step: one step lower on the
    scale, never below `floor`."""
    below = [u for u in UNITS if u < comfortable]
    return max(floor, below[-1]) if below else comfortable


def comfortable_units(role: str, density: float) -> int:
    airy, dense, _ = ROLES[role]
    return snap(airy + (dense - airy) * density)


def compact_units(role: str, density: float) -> int:
    return compact_step(comfortable_units(role, density), ROLES[role][2])


def generate_space(axes: AxisValues, refuse_compact: bool = False) -> Generated:
    """Every spacing role; with `refuse_compact` (older or mixed-age
    readers) the compact mode keeps the comfortable values."""
    ts = TokenSet()
    for n in UNITS:
        ts.add(Token(f"space.{n}", "dimension", _px(n)))
    notes: List[str] = []
    for role in ROLES:
        comfortable = comfortable_units(role, axes.density)
        compact = comfortable if refuse_compact else compact_units(role, axes.density)
        modes = {"density:compact": "{space.%d}" % compact} if compact != comfortable else {}
        ts.add(Token(role, "dimension", "{space.%d}" % comfortable, modes=modes, layer="semantic"))
        if compact == comfortable and not refuse_compact:
            notes.append(f"{role}: compact keeps {comfortable * BASE_UNIT}px, its floor")
    return Generated(tokens=ts, notes=notes)


# Every role is a dimension. The build's role-types check reports any other
# type once, and the checks below skip it.
ROLE_TYPES: Dict[str, str] = {role: "dimension" for role in ROLES}


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _value(ts: TokenSet, path: str, mode: str) -> float:
    return dimension_px(ts.resolve(path, mode))


def _control_gap(ts: TokenSet, mode: str) -> List[str]:
    if not _typed(ts, "space.control.gap"):
        return []
    px = _value(ts, "space.control.gap", mode)
    if px >= MIN_CONTROL_GAP_PX:
        return []
    return [f"space.control.gap ({mode}) is {px:g}px; our floor between adjacent controls is "
            f"{MIN_CONTROL_GAP_PX}px, so point it at space.2 or larger. WCAG 2.5.8 sets a "
            "minimum target of 24 by 24 CSS px, not a gap; this floor keeps smaller controls "
            "apart."]


def _scale_order(ts: TokenSet, mode: str) -> List[str]:
    steps = numbered_steps(ts, "space.")
    return [f"{b} is not larger than {a}; keep the scale strictly increasing"
            for a, b in zip(steps, steps[1:]) if _value(ts, a, mode) >= _value(ts, b, mode)]


def _on_scale(ts: TokenSet, mode: str) -> List[str]:
    """Every role that aliases a primitive aliases space.<n>. A role holding
    its value directly is left to the value checks."""
    out = []
    for role in ROLES:
        if not _typed(ts, role):
            continue
        target = direct_alias(ts, role, mode)
        if target is not None and not is_step(target, "space."):
            out.append(f"{role} ({mode}) points at {target}, which is not a step of the spacing "
                       "scale; spacing values come from space.<n>, so point it at a space step")
    return out


def _grid(ts: TokenSet, mode: str) -> List[str]:
    """Every numbered spacing step is a whole multiple of BASE_UNIT."""
    out = []
    for path in numbered_steps(ts, "space.", others=False):
        if ts.get(path).type != "dimension":
            continue
        px = _value(ts, path, mode)
        if px % BASE_UNIT:
            low = int(px // BASE_UNIT) * BASE_UNIT
            out.append(f"{path} is {px:g}px, which is not a multiple of {BASE_UNIT}px; every "
                       f"spacing step sits on the {BASE_UNIT}px grid, so round it to {low}px or "
                       f"{low + BASE_UNIT}px")
    return out


def _hierarchy(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in HIERARCHY if _typed(ts, r)]
    out = []
    for a, b in zip(present, present[1:]):
        if _value(ts, a, mode) >= _value(ts, b, mode):
            out.append(f"{a} ({mode}) is not smaller than {b}; a gap inside a level must stay "
                       f"below the gap between levels, so move {a} down the scale")
    return out


def _compact_not_larger(ts: TokenSet, mode: str) -> List[str]:
    if mode != "density:compact":
        return []
    return [f"{r} is larger in compact than in comfortable; point its compact override at a "
            "smaller step" for r in ROLES
            if _typed(ts, r) and _value(ts, r, "density:compact") > _value(ts, r, "")]


CHECKS: Tuple[Check, ...] = (
    Check("control-gap", "system", _control_gap, axes=("density",)),
    Check("space-scale-order", "system", _scale_order,
          exempt_axes=(("density", "it reads only primitives, which never carry modes"),)),
    Check("space-on-scale", "system", _on_scale, axes=("density",)),
    Check("space-grid", "system", _grid,
          exempt_axes=(("density", "it reads only primitives, which never carry modes"),)),
    Check("space-hierarchy", "system", _hierarchy, axes=("density",)),
    Check("compact-not-larger", "system", _compact_not_larger, axes=("density",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_space(axes, refuse_compact=inputs.audience.refuse_compact)


FOUNDATION = Foundation(name="space", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
