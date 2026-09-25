"""Elevation foundation: shadow composites per level and scheme, and the
stacking order of floating layers.

Each level's shadow has two layers, a key light that grows with the level
and a tight ambient one. The surface treatment (character.depth, from the
contrast and formality axes) sets how strong and how soft they are: a
flat system keeps a whisper of shadow, a deep one casts a clear one. Dark
schemes need stronger shadows to read at all, so their alpha is 2.5 times
the light alpha, capped. elevation.inset gives a sunken surface an inner
shadow, so it reads as recessed. The surfaces these shadows sit on are color roles
(color.surface.card, color.surface.raised) and the dimming behind a dialog
is color.scrim.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple

from engine.foundations import character
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.modes import compress, contexts
from engine.foundations.tokens import Token, TokenSet
from engine.foundations.values import dimension_px
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


def key_alpha(depth: float, level: int, scheme: str) -> float:
    """The key light's alpha: 0.03 for a flat system to 0.17 for a deep one
    at level 1, stronger per level and in dark."""
    a = (0.03 + 0.14 * depth) * STRENGTH[level - 1]
    if scheme == "dark":
        a *= DARK_FACTOR
    return round(min(a, ALPHA_CAP), 3)


def softness(depth: float) -> float:
    """How far a shadow spreads its blur: 0.7 flat to 1.3 deep."""
    return 0.7 + 0.6 * depth


def _black(alpha: float) -> str:
    return f"#000000{round(alpha * 255):02X}"


def _dim(px: int) -> Dict[str, Any]:
    return {"value": px, "unit": "px"}


def shadow(depth: float, level: int, scheme: str) -> List[Dict[str, Any]]:
    y, blur, spread = KEY[level - 1]
    ay, ablur = AMBIENT[level - 1]
    a = key_alpha(depth, level, scheme)
    return [
        {"color": _black(a), "offsetX": _dim(0), "offsetY": _dim(y),
         "blur": _dim(max(y + 1, int(blur * softness(depth) + 0.5))), "spread": _dim(spread)},
        {"color": _black(round(a / 2, 3)), "offsetX": _dim(0), "offsetY": _dim(ay),
         "blur": _dim(ablur), "spread": _dim(0)},
    ]


def inset(depth: float, scheme: str) -> List[Dict[str, Any]]:
    """An inner shadow along the top edge of a sunken surface."""
    a = round(min((0.04 + 0.08 * depth) * (DARK_FACTOR if scheme == "dark" else 1), ALPHA_CAP), 3)
    return [{"color": _black(a), "offsetX": _dim(0), "offsetY": _dim(1),
             "blur": _dim(2 + int(2 * depth + 0.5)), "spread": _dim(0), "inset": True}]


def generate_elevation(axes: AxisValues) -> Generated:
    d = character.depth(axes)
    ts = TokenSet()
    for scheme in ("light", "dark"):
        for level in range(1, 5):
            ts.add(Token(f"elevation.shadow.{scheme}.{level}", "shadow",
                         shadow(d, level, scheme)))
        ts.add(Token(f"elevation.shadow.{scheme}.inset", "shadow", inset(d, scheme)))
    for z in sorted(set(ORDER.values())):
        ts.add(Token(f"elevation.z.{z}", "number", z))
    for level, role in enumerate(ROLES, 1):
        base, modes = compress({ctx: "{elevation.shadow.%s.%d}" % (ctx.split(":")[1], level)
                                for ctx in contexts(("scheme",))})
        ts.add(Token(role, "shadow", base, modes=modes, layer="semantic"))
    base, modes = compress({ctx: "{elevation.shadow.%s.inset}" % ctx.split(":")[1]
                            for ctx in contexts(("scheme",))})
    ts.add(Token("elevation.inset", "shadow", base, modes=modes, layer="semantic"))
    for role, z in ORDER.items():
        ts.add(Token(role, "number", "{elevation.z.%d}" % z, layer="semantic"))
    return Generated(tokens=ts, notes=[f"elevation: depth {d:.2f} from contrast "
                                       f"{axes.contrast:g} and formality {axes.formality:g}"])


# Role path -> token type: levels are shadows, the stacking order numbers.
# The build's role-types check reports any other type once, and the checks
# below skip it.
ROLE_TYPES: Dict[str, str] = {**{r: "shadow" for r in ROLES}, "elevation.inset": "shadow",
                              **{r: "number" for r in ORDER}}


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _alpha(hex8: str) -> int:
    return int(hex8[7:9], 16) if len(hex8) == 9 else 255


def _key(ts: TokenSet, role: str, mode: str) -> dict:
    """The first (key) layer of a role's shadow; a shadow may be one layer
    object or a list of layers."""
    value = ts.resolve(role, mode)
    return value[0] if isinstance(value, list) else value


def _order(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in ROLES if _typed(ts, r)]
    out = []
    for a, b in zip(present, present[1:]):
        ka, kb = _key(ts, a, mode), _key(ts, b, mode)
        if not (dimension_px(kb["offsetY"]) > dimension_px(ka["offsetY"])
                and dimension_px(kb["blur"]) > dimension_px(ka["blur"])
                and _alpha(kb["color"]) >= _alpha(ka["color"])):
            out.append(f"{b} ({mode}) does not rise above {a}; a higher level needs a larger "
                       "offset and blur and at least the same strength, so point it at a "
                       "higher shadow step")
    return out


LIGHT, DARK = "scheme:light", "scheme:dark"


def _layers(ts: TokenSet, role: str, mode: str) -> List[dict]:
    value = ts.resolve(role, mode)
    return value if isinstance(value, list) else [value]


def _dark_only(ts: TokenSet, paths: List[str], mode: str) -> bool:
    """In scheme:dark, whether every path reads as in light; a finding then
    belongs to the light context and is not repeated."""
    return mode == DARK and all(ts.resolve(p, DARK) == ts.resolve(p, LIGHT) for p in paths)


def _dark_strength(ts: TokenSet, mode: str) -> List[str]:
    if mode != DARK:
        return []
    return [f"{r} is no stronger in dark than in light; dark surfaces need a stronger shadow "
            "than light to read, so point its scheme:dark override at a stronger shadow"
            for r in ROLES if _typed(ts, r)
            and _alpha(_key(ts, r, DARK)["color"]) <= _alpha(_key(ts, r, LIGHT)["color"])]


def _visible(ts: TokenSet, mode: str) -> List[str]:
    return [f"{r} ({mode}) casts no visible shadow; every layer is fully transparent, so "
            "point it at a shadow step with a layer above alpha 0"
            for r in ROLES if _typed(ts, r) and not _dark_only(ts, [r], mode)
            and not any(_alpha(layer["color"]) > 0 for layer in _layers(ts, r, mode))]


def _stacking(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in ORDER if _typed(ts, r)]
    where = f" under {mode}" if mode == DARK else ""
    return [f"{b} ({ts.resolve(b, mode):g}) does not stack above {a} ({ts.resolve(a, mode):g})"
            f"{where}; keep the order {', '.join(r.rsplit('.', 1)[1] for r in ORDER)}"
            for a, b in zip(present, present[1:])
            if ts.resolve(b, mode) <= ts.resolve(a, mode) and not _dark_only(ts, [a, b], mode)]


CHECKS: Tuple[Check, ...] = (
    Check("elevation-order", "system", _order, axes=("scheme",)),
    Check("elevation-dark", "system", _dark_strength, axes=("scheme",)),
    Check("visible-shadow", "system", _visible, axes=("scheme",)),
    Check("stacking-order", "system", _stacking, axes=("scheme",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_elevation(axes)


FOUNDATION = Foundation(name="elevation", generate=_generate, checks=CHECKS,
                        role_types=ROLE_TYPES)
