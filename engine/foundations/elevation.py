"""Elevation foundation: shadow composites per level and scheme, and the
stacking order of floating layers.

Each level's shadow has two layers, a key light that grows with the level
and a tight ambient one. The contrast axis sets how strong they are; dark
schemes need stronger shadows to read at all, so their alpha is 2.5 times
the light alpha, capped. The surfaces these shadows sit on are color roles
(color.surface.card, color.surface.raised) and the dimming behind a dialog
is color.scrim.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated
from engine.foundations.gate import Check
from engine.foundations.modes import compress, contexts
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

# per level 1..4: key (y, blur, spread), ambient (y, blur), strength multiple
KEY = ((1, 3, 0), (2, 6, -1), (6, 16, -3), (12, 32, -6))
AMBIENT = ((0, 1), (1, 2), (2, 4), (4, 8))
STRENGTH = (1.0, 1.25, 1.5, 2.0)
DARK_FACTOR, ALPHA_CAP = 2.5, 0.8
ROLES = ("elevation.card", "elevation.lifted", "elevation.popover", "elevation.dialog")
# stacking order: role -> z-index
ORDER = {"elevation.order.base": 0, "elevation.order.sticky": 100,
         "elevation.order.dropdown": 1000, "elevation.order.overlay": 2000,
         "elevation.order.dialog": 2100, "elevation.order.toast": 3000}


def key_alpha(contrast: float, level: int, scheme: str) -> float:
    a = (0.06 + 0.06 * contrast) * STRENGTH[level - 1]
    if scheme == "dark":
        a *= DARK_FACTOR
    return round(min(a, ALPHA_CAP), 3)


def _black(alpha: float) -> str:
    return f"#000000{round(alpha * 255):02X}"


def _dim(px: int) -> Dict[str, Any]:
    return {"value": px, "unit": "px"}


def shadow(contrast: float, level: int, scheme: str) -> List[Dict[str, Any]]:
    y, blur, spread = KEY[level - 1]
    ay, ablur = AMBIENT[level - 1]
    a = key_alpha(contrast, level, scheme)
    return [
        {"color": _black(a), "offsetX": _dim(0), "offsetY": _dim(y), "blur": _dim(blur),
         "spread": _dim(spread)},
        {"color": _black(round(a / 2, 3)), "offsetX": _dim(0), "offsetY": _dim(ay),
         "blur": _dim(ablur), "spread": _dim(0)},
    ]


def generate_elevation(axes: AxisValues) -> Generated:
    ts = TokenSet()
    for scheme in ("light", "dark"):
        for level in range(1, 5):
            ts.add(Token(f"elevation.shadow.{scheme}.{level}", "shadow",
                         shadow(axes.contrast, level, scheme)))
    for z in sorted(set(ORDER.values())):
        ts.add(Token(f"elevation.z.{z}", "number", z))
    for level, role in enumerate(ROLES, 1):
        base, modes = compress({ctx: "{elevation.shadow.%s.%d}" % (ctx.split(":")[1], level)
                                for ctx in contexts(("scheme",))})
        ts.add(Token(role, "shadow", base, modes=modes, layer="semantic"))
    for role, z in ORDER.items():
        ts.add(Token(role, "number", "{elevation.z.%d}" % z, layer="semantic"))
    return Generated(tokens=ts)


def _alpha(hex8: str) -> int:
    return int(hex8[7:9], 16) if len(hex8) == 9 else 255


def _order(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in ROLES if ts.has(r)]
    out = []
    for a, b in zip(present, present[1:]):
        ka, kb = ts.resolve(a, mode)[0], ts.resolve(b, mode)[0]
        if not (kb["offsetY"]["value"] > ka["offsetY"]["value"]
                and kb["blur"]["value"] > ka["blur"]["value"]
                and _alpha(kb["color"]) >= _alpha(ka["color"])):
            out.append(f"{b} ({mode}) does not rise above {a}; a higher level needs a larger "
                       "offset and blur and at least the same strength, so point it at a "
                       "higher shadow step")
    return out


def _dark_strength(ts: TokenSet, mode: str) -> List[str]:
    if mode != "scheme:dark":
        return []
    return [f"{r} is weaker in dark than in light; dark surfaces need at least the light "
            "shadow strength to read, so point its dark override at a stronger shadow"
            for r in ROLES if ts.has(r)
            and _alpha(ts.resolve(r, "scheme:dark")[0]["color"])
            < _alpha(ts.resolve(r, "scheme:light")[0]["color"])]


def _stacking(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in ORDER if ts.has(r)]
    return [f"{b} ({ts.resolve(b):g}) does not stack above {a} ({ts.resolve(a):g}); keep the "
            f"order {', '.join(r.rsplit('.', 1)[1] for r in ORDER)}"
            for a, b in zip(present, present[1:]) if ts.resolve(b) <= ts.resolve(a)]


CHECKS: Tuple[Check, ...] = (
    Check("elevation-order", "system", _order, axes=("scheme",)),
    Check("elevation-dark", "system", _dark_strength, axes=("scheme",)),
    Check("stacking-order", "system", _stacking),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_elevation(axes)


FOUNDATION = Foundation(name="elevation", generate=_generate, checks=CHECKS)
