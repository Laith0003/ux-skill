"""Border foundation: stroke widths, stroke styles, and the roles that use
them. Border colors live in the color foundation (color.line.*).

Widths are whole pixels; a sub-pixel stroke vanishes on 1x screens. The
focus ring is the heaviest stroke and a dramatic brand (contrast axis at
0.66 or more) gets a 3px ring. The ring's offset leaves a gap of page
color between the element and the ring.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

WIDTHS = (0, 1, 2, 3, 4)
STYLES = ("solid", "dashed", "dotted")
BOLD_RING_FROM = 0.66  # contrast axis
MIN_RING_PX = 2
# roles whose widths must not decrease in this order
WEIGHT_ORDER = ("border.separator", "border.outline", "border.emphasis")


def roles(axes: AxisValues) -> Dict[str, str]:
    ring = "border.width.3" if axes.contrast >= BOLD_RING_FROM else "border.width.2"
    return {
        "border.separator": "border.width.1",
        "border.outline": "border.width.1",
        "border.emphasis": "border.width.2",
        "border.active": "border.width.2",
        "border.focus-ring.width": ring,
        "border.focus-ring.offset": "border.width.2",
        "border.style.default": "border.line.solid",
        "border.style.placeholder": "border.line.dashed",
    }


def generate_border(axes: AxisValues) -> Generated:
    ts = TokenSet()
    for px in WIDTHS:
        ts.add(Token(f"border.width.{px}", "dimension", {"value": px, "unit": "px"}))
    for style in STYLES:
        ts.add(Token(f"border.line.{style}", "strokeStyle", style))
    for role, prim in roles(axes).items():
        type_ = "strokeStyle" if prim.startswith("border.line.") else "dimension"
        ts.add(Token(role, type_, "{" + prim + "}", layer="semantic"))
    notes = [] if axes.contrast < BOLD_RING_FROM else [
        f"border.focus-ring.width: 3px, contrast axis {axes.contrast:g} is dramatic"]
    return Generated(tokens=ts, notes=notes)


def _px(ts: TokenSet, path: str) -> float:
    return ts.resolve(path)["value"]


def _ring(ts: TokenSet, mode: str) -> List[str]:
    out = []
    if ts.has("border.focus-ring.width"):
        ring = _px(ts, "border.focus-ring.width")
        if ring < MIN_RING_PX:
            out.append(f"border.focus-ring.width is {ring:g}px; a focus ring needs at least "
                       f"{MIN_RING_PX}px to be seen, so point it at border.width.2 or wider")
        if ts.has("border.outline") and ring <= _px(ts, "border.outline"):
            out.append("border.focus-ring.width is not wider than border.outline; a ring must "
                       "stand out from resting borders, so point it at a wider step")
    if ts.has("border.focus-ring.width") and not ts.has("border.focus-ring.offset"):
        out.append("border.focus-ring.width is set but border.focus-ring.offset is missing; "
                   "leave at least 1px of page color between the element and its ring, so "
                   "add border.focus-ring.offset pointing at border.width.1 or wider")
    elif ts.has("border.focus-ring.offset") and _px(ts, "border.focus-ring.offset") < 1:
        offset = _px(ts, "border.focus-ring.offset")
        out.append(f"border.focus-ring.offset is {offset:g}px; leave at least 1px of page color "
                   "between the element and its ring, so point it at border.width.1 or wider")
    return out


def _active(ts: TokenSet, mode: str) -> List[str]:
    if ts.has("border.active") and _px(ts, "border.active") <= 0:
        return ["border.active is 0px; a selected state must show more than a color change, so "
                "point it at border.width.1 or wider"]
    return []


def _weight_order(ts: TokenSet, mode: str) -> List[str]:
    present = [r for r in WEIGHT_ORDER if ts.has(r)]
    return [f"{b} ({_px(ts, b):g}px) is lighter than {a} ({_px(ts, a):g}px); keep border "
            f"weights in the order {', '.join(WEIGHT_ORDER)}"
            for a, b in zip(present, present[1:]) if _px(ts, b) < _px(ts, a)]


def _whole_pixels(ts: TokenSet, mode: str) -> List[str]:
    return [f"{t.path} is {t.value['value']:g}px; a sub-pixel stroke vanishes on 1x screens, so "
            "use a whole number of pixels"
            for t in ts.tokens() if t.path.startswith("border.width.")
            and isinstance(t.value, dict) and float(t.value["value"]) != int(t.value["value"])]


CHECKS: Tuple[Check, ...] = (
    Check("focus-ring", "system", _ring),
    Check("active-border", "1.4.1", _active),
    Check("border-weight-order", "system", _weight_order),
    Check("border-whole-pixels", "system", _whole_pixels),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_border(axes)


FOUNDATION = Foundation(name="border", generate=_generate, checks=CHECKS)
