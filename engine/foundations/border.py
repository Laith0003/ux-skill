"""Border foundation: stroke widths, stroke styles, and the roles that use
them. Border colors live in the color foundation (color.line.*).

Widths are whole pixels; a sub-pixel stroke vanishes on 1x screens. The
focus ring is the heaviest stroke and a dramatic brand (contrast axis at
0.66 or more) gets a 3px ring. The ring's offset leaves a gap of page
color between the element and the ring.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

WIDTHS = (0, 1, 2, 3, 4)
STYLES = ("solid", "dashed", "dotted")
BOLD_RING_FROM = 0.66  # contrast axis
MIN_RING_PX = 2


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
        ts.add(Token(role, _role_type(prim), "{" + prim + "}", layer="semantic"))
    notes = [] if axes.contrast < BOLD_RING_FROM else [
        f"border.focus-ring.width: 3px, contrast axis {axes.contrast:g} is dramatic"]
    return Generated(tokens=ts, notes=notes)


def _role_type(prim: str) -> str:
    return "strokeStyle" if prim.startswith("border.line.") else "dimension"


# Role path -> token type (role names and types do not depend on the axes).
# The build's role-types check reports any other type once, and the checks
# below skip it.
ROLE_TYPES: Dict[str, str] = {role: _role_type(prim)
                              for role, prim in roles(AxisValues(*[0.0] * 7)).items()}


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _px(ts: TokenSet, path: str) -> float:
    return ts.resolve(path)["value"]


def _ring(ts: TokenSet, mode: str) -> List[str]:
    out = []
    if _typed(ts, "border.focus-ring.width"):
        ring = _px(ts, "border.focus-ring.width")
        if ring < MIN_RING_PX:
            out.append(f"border.focus-ring.width is {ring:g}px; a focus ring needs at least "
                       f"{MIN_RING_PX}px to be seen, so point it at border.width.2 or wider")
        if _typed(ts, "border.outline") and ring <= _px(ts, "border.outline"):
            out.append("border.focus-ring.width is not wider than border.outline; a ring must "
                       "stand out from resting borders, so point it at a wider step")
    if _typed(ts, "border.focus-ring.width") and not ts.has("border.focus-ring.offset"):
        out.append("border.focus-ring.width is set but border.focus-ring.offset is missing; "
                   "leave at least 1px of page color between the element and its ring, so "
                   "add border.focus-ring.offset pointing at border.width.1 or wider")
    elif _typed(ts, "border.focus-ring.offset") and _px(ts, "border.focus-ring.offset") < 1:
        offset = _px(ts, "border.focus-ring.offset")
        out.append(f"border.focus-ring.offset is {offset:g}px; leave at least 1px of page color "
                   "between the element and its ring, so point it at border.width.1 or wider")
    return out


def _active(ts: TokenSet, mode: str) -> List[str]:
    """A selected edge must be wider than a resting one; one as thin as
    border.outline tells the states apart by color alone."""
    if not _typed(ts, "border.active"):
        return []
    active = _px(ts, "border.active")
    if _typed(ts, "border.outline") and active <= _px(ts, "border.outline"):
        return [f"border.active ({active:g}px) is not wider than border.outline "
                f"({_px(ts, 'border.outline'):g}px), so a selected edge differs from a resting "
                "edge by color alone; WCAG 1.4.1 asks that color not be the only visual means of "
                "conveying information, so point border.active at a wider step than "
                "border.outline"]
    if active <= 0:
        return ["border.active is 0px; a selected state must show more than a color change, "
                "so point it at border.width.1 or wider"]
    return []


def _weight_order(ts: TokenSet, mode: str) -> List[str]:
    """border.emphasis is heavier than border.outline, and border.separator
    may match border.outline but never outweigh it. Without an outline,
    emphasis is heavier than the separator."""
    sep, outline, emph = "border.separator", "border.outline", "border.emphasis"
    out = []
    if _typed(ts, outline):
        o = _px(ts, outline)
        if _typed(ts, sep) and _px(ts, sep) > o:
            out.append(f"{sep} ({_px(ts, sep):g}px) is heavier than {outline} ({o:g}px); a "
                       "separator may match a resting edge but never outweigh it, so point "
                       f"{sep} at the step {outline} uses or a lighter one")
        if _typed(ts, emph) and _px(ts, emph) <= o:
            out.append(f"{emph} ({_px(ts, emph):g}px) is not heavier than {outline} ({o:g}px), "
                       "so an emphasized edge differs from a resting edge by color alone; point "
                       f"{emph} at a wider step than {outline}")
    elif _typed(ts, sep) and _typed(ts, emph) and _px(ts, emph) <= _px(ts, sep):
        out.append(f"{emph} ({_px(ts, emph):g}px) is not heavier than {sep} "
                   f"({_px(ts, sep):g}px); point {emph} at a wider step than {sep}")
    return out


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


FOUNDATION = Foundation(name="border", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
