"""Border foundation: stroke widths, stroke styles, and the roles that use
them. Border colors live in the color foundation (color.line.*).

Widths are whole pixels; a sub-pixel stroke vanishes on 1x screens. The
focus ring is the heaviest stroke and a dramatic brand (contrast axis at
0.66 or more) gets a 3px ring. The ring's offset leaves a gap of page
color between the element and the ring. Under high contrast the outline,
emphasis, active edge and ring are each one pixel heavier.
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


def roles(axes: AxisValues, ring_extra: int = 0) -> Dict[str, str]:
    ring = f"border.width.{(3 if axes.contrast >= BOLD_RING_FROM else 2) + ring_extra}"
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


# Roles one step heavier under high contrast.
HIGH_STEP = ("border.outline", "border.emphasis", "border.active", "border.focus-ring.width")


def _heavier(prim: str) -> str:
    return f"border.width.{min(WIDTHS[-1], int(prim.rsplit('.', 1)[1]) + 1)}"


def generate_border(axes: AxisValues, ring_extra: int = 0) -> Generated:
    ts = TokenSet()
    for px in WIDTHS:
        ts.add(Token(f"border.width.{px}", "dimension", {"value": px, "unit": "px"}))
    for style in STYLES:
        ts.add(Token(f"border.line.{style}", "strokeStyle", style))
    for role, prim in roles(axes, ring_extra).items():
        modes = {"contrast:high": "{" + _heavier(prim) + "}"} if role in HIGH_STEP else {}
        ts.add(Token(role, _role_type(prim), "{" + prim + "}", modes=modes, layer="semantic"))
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


def _px(ts: TokenSet, path: str, mode: str = "") -> float:
    return ts.resolve(path, mode)["value"]


def _where(mode: str) -> str:
    return " under high contrast" if "contrast:high" in mode else ""


def _repeat(ts: TokenSet, mode: str) -> bool:
    """Under high contrast, True when every width role reads as at standard
    contrast: a finding there is the standard context's and is not
    repeated (high-contrast-borders names the missing step)."""
    if "contrast:high" not in mode:
        return False
    roles = [r for r in ROLE_TYPES if _typed(ts, r) and ROLE_TYPES[r] == "dimension"]
    return all(_px(ts, r, mode) == _px(ts, r, "") for r in roles)


def _high_not_thinner(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast no edge is thinner than at standard contrast,
    and the ring and the outline are heavier."""
    if "contrast:high" not in mode:
        return []
    out = []
    for role in ROLE_TYPES:
        if not _typed(ts, role) or ROLE_TYPES[role] != "dimension":
            continue
        high, std = _px(ts, role, mode), _px(ts, role, "")
        if high < std or (role in ("border.focus-ring.width", "border.outline") and high <= std):
            out.append(f"{role} is {high:g}px under high contrast and {std:g}px at standard; "
                       "high contrast makes the ring and the outline heavier and never thins an "
                       f"edge, so point its contrast:high override at a wider step than {std:g}px")
    return out


def _ring(ts: TokenSet, mode: str) -> List[str]:
    if _repeat(ts, mode):
        return []
    out = []
    if _typed(ts, "border.focus-ring.width"):
        ring = _px(ts, "border.focus-ring.width", mode)
        if ring < MIN_RING_PX:
            out.append(f"border.focus-ring.width is {ring:g}px{_where(mode)}; a focus ring needs "
                       f"at least {MIN_RING_PX}px to be seen, so point it at border.width.2 or "
                       "wider")
        if _typed(ts, "border.outline") and ring <= _px(ts, "border.outline", mode):
            out.append(f"border.focus-ring.width is not wider than border.outline{_where(mode)}; "
                       "a ring must stand out from resting borders, so point it at a wider step")
    if _typed(ts, "border.focus-ring.width") and not ts.has("border.focus-ring.offset"):
        out.append("border.focus-ring.width is set but border.focus-ring.offset is missing; "
                   "leave at least 1px of page color between the element and its ring, so "
                   "add border.focus-ring.offset pointing at border.width.1 or wider")
    elif _typed(ts, "border.focus-ring.offset") and _px(ts, "border.focus-ring.offset", mode) < 1:
        offset = _px(ts, "border.focus-ring.offset", mode)
        out.append(f"border.focus-ring.offset is {offset:g}px; leave at least 1px of page color "
                   "between the element and its ring, so point it at border.width.1 or wider")
    return out


def _active(ts: TokenSet, mode: str) -> List[str]:
    """A selected edge must be wider than a resting one; one as thin as
    border.outline tells the states apart by color alone."""
    if not _typed(ts, "border.active") or _repeat(ts, mode):
        return []
    active = _px(ts, "border.active", mode)
    if _typed(ts, "border.outline") and active <= _px(ts, "border.outline", mode):
        return [f"border.active ({active:g}px) is not wider than border.outline "
                f"({_px(ts, 'border.outline', mode):g}px){_where(mode)}, so a selected edge "
                "differs from a resting "
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
    out: List[str] = []
    if _repeat(ts, mode):
        return out

    def px(path: str) -> float:
        return _px(ts, path, mode)

    if _typed(ts, outline):
        o = px(outline)
        if _typed(ts, sep) and px(sep) > o:
            out.append(f"{sep} ({px(sep):g}px) is heavier than {outline} ({o:g}px){_where(mode)}; "
                       "a separator may match a resting edge but never outweigh it, so point "
                       f"{sep} at the step {outline} uses or a lighter one")
        if _typed(ts, emph) and px(emph) <= o:
            out.append(f"{emph} ({px(emph):g}px) is not heavier than {outline} ({o:g}px)"
                       f"{_where(mode)}, so an emphasized edge differs from a resting edge by "
                       f"color alone; point {emph} at a wider step than {outline}")
    elif _typed(ts, sep) and _typed(ts, emph) and px(emph) <= px(sep):
        out.append(f"{emph} ({px(emph):g}px) is not heavier than {sep} "
                   f"({px(sep):g}px){_where(mode)}; point {emph} at a wider step than {sep}")
    return out


def _whole_pixels(ts: TokenSet, mode: str) -> List[str]:
    return [f"{t.path} is {t.value['value']:g}px; a sub-pixel stroke vanishes on 1x screens, so "
            "use a whole number of pixels"
            for t in ts.tokens() if t.path.startswith("border.width.")
            and isinstance(t.value, dict) and float(t.value["value"]) != int(t.value["value"])]


CHECKS: Tuple[Check, ...] = (
    Check("focus-ring", "system", _ring, axes=("contrast",)),
    Check("active-border", "1.4.1", _active, axes=("contrast",)),
    Check("border-weight-order", "system", _weight_order, axes=("contrast",)),
    Check("border-whole-pixels", "system", _whole_pixels,
          exempt_axes=(("contrast", "it reads only primitives, which never carry modes"),)),
    Check("high-contrast-borders", "system", _high_not_thinner, axes=("contrast",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_border(axes, ring_extra=inputs.audience.ring_extra)


FOUNDATION = Foundation(name="border", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
