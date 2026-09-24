"""Layout foundation: breakpoints, grid columns and gutters, page margins,
container and reading widths, and the minimum target size.

Gutters and margins alias the spacing scale (space.<n>), so layout and
spacing move together; the density axis places them and compact takes one
step less, never below 8px. Breakpoints are minimum viewport widths; a
phone is everything below the tablet breakpoint. CSS cannot read custom
properties inside a media query, so the breakpoint tokens are reference
values for exporters and docs.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Sequence, Tuple

from engine.foundations import space
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

TIERS = ("phone", "tablet", "laptop", "desktop")
VIEWPORTS = {"tablet": 640, "laptop": 1024, "desktop": 1280}
COLUMNS = {"phone": 4, "tablet": 8, "laptop": 12, "desktop": 12}
# tier -> (space units when the density axis is 0, when it is 1)
GUTTER = {"phone": (4, 3), "tablet": (6, 4), "laptop": (8, 5), "desktop": (8, 6)}
MARGIN = {"phone": (5, 4), "tablet": (8, 6), "laptop": (12, 8), "desktop": (16, 10)}
COMPACT_FLOOR = 2  # space units, 8px
CONTAINERS = (1120, 1280, 1440)
MEASURE_REM = {"text": 38, "form": 32}
MAX_TEXT_MEASURE_REM = 40  # about 80 characters of body text
TARGET_PX = {"comfortable": 44, "compact": 32}
MIN_TARGET_PX, COMFORTABLE_TARGET_PX = 24, 44


def _units(pair: Tuple[int, int], density: float) -> Tuple[int, int]:
    """Comfortable and compact space units on the spacing scale's own rules."""
    comfortable = space.snap(pair[0] + (pair[1] - pair[0]) * density)
    return comfortable, space.compact_step(comfortable, COMPACT_FLOOR)


def container_px(density: float) -> int:
    return space.snap(CONTAINERS[0] + (CONTAINERS[-1] - CONTAINERS[0]) * density, CONTAINERS)


def generate_layout(axes: AxisValues) -> Generated:
    d = axes.density
    ts = TokenSet()
    for px in VIEWPORTS.values():
        ts.add(Token(f"layout.viewport.{px}", "dimension", {"value": px, "unit": "px"}))
    for n in sorted(set(COLUMNS.values())):
        ts.add(Token(f"layout.column-count.{n}", "number", n))
    for px in sorted(set(CONTAINERS) | set(TARGET_PX.values())):
        ts.add(Token(f"layout.width.{px}", "dimension", {"value": px, "unit": "px"}))
    for rem in sorted(set(MEASURE_REM.values())):
        ts.add(Token(f"layout.rem.{rem}", "dimension", {"value": rem, "unit": "rem"}))

    for tier, px in VIEWPORTS.items():
        ts.add(Token(f"layout.breakpoint.{tier}", "dimension", "{layout.viewport.%d}" % px,
                     layer="semantic"))
    for tier in TIERS:
        ts.add(Token(f"layout.columns.{tier}", "number",
                     "{layout.column-count.%d}" % COLUMNS[tier], layer="semantic"))
    for group, table in (("gutter", GUTTER), ("margin-inline", MARGIN)):
        for tier in TIERS:
            comfortable, compact = _units(table[tier], d)
            modes = {"density:compact": "{space.%d}" % compact} if compact != comfortable else {}
            ts.add(Token(f"layout.{group}.{tier}", "dimension", "{space.%d}" % comfortable,
                         modes=modes, layer="semantic"))
    ts.add(Token("layout.container.max", "dimension", "{layout.width.%d}" % container_px(d),
                 layer="semantic"))
    for name, rem in MEASURE_REM.items():
        ts.add(Token(f"layout.measure.{name}", "dimension", "{layout.rem.%d}" % rem,
                     layer="semantic"))
    ts.add(Token("layout.target.min", "dimension", "{layout.width.%d}" % TARGET_PX["comfortable"],
                 modes={"density:compact": "{layout.width.%d}" % TARGET_PX["compact"]},
                 layer="semantic"))
    return Generated(tokens=ts, notes=[f"layout: container {container_px(d)}px"])


# Role path -> the token type the checks read; the build's role-types
# check reports any other type once, and the checks below skip it.
ROLE_TYPES: Dict[str, str] = {
    **{f"layout.breakpoint.{t}": "dimension" for t in VIEWPORTS},
    **{f"layout.columns.{t}": "number" for t in TIERS},
    **{f"layout.gutter.{t}": "dimension" for t in TIERS},
    **{f"layout.margin-inline.{t}": "dimension" for t in TIERS},
    "layout.container.max": "dimension",
    **{f"layout.measure.{name}": "dimension" for name in MEASURE_REM},
    "layout.target.min": "dimension",
}
COMPACT = "density:compact"


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _px(ts: TokenSet, path: str, mode: str = "") -> float:
    v = ts.resolve(path, mode)
    return v["value"] * (16 if v["unit"] == "rem" else 1)


def _number(ts: TokenSet, path: str, mode: str = "") -> Any:
    return ts.resolve(path, mode)


def _repeat(ts: TokenSet, paths: Sequence[str], mode: str,
            read: Callable[[TokenSet, str, str], Any]) -> bool:
    """In compact, a failure whose values all match comfortable is the
    comfortable context's finding and is not repeated."""
    return COMPACT in mode and all(read(ts, p, mode) == read(ts, p, "") for p in paths)


def _where(mode: str) -> str:
    return f" in {COMPACT}" if COMPACT in mode else ""


def _breakpoints(ts: TokenSet, mode: str) -> List[str]:
    present = [f"layout.breakpoint.{t}" for t in TIERS if _typed(ts, f"layout.breakpoint.{t}")]
    out = []
    for a, b in zip(present, present[1:]):
        va, vb, w = _px(ts, a, mode), _px(ts, b, mode), _where(mode)
        if vb <= va and not _repeat(ts, (a, b), mode, _px):
            out.append(f"{b} ({vb:g}px{w}) does not start above {a} ({va:g}px{w}); keep "
                       "breakpoints strictly increasing")
    return out


def _columns(ts: TokenSet, mode: str) -> List[str]:
    present = [f"layout.columns.{t}" for t in TIERS if _typed(ts, f"layout.columns.{t}")]
    out = []
    for a, b in zip(present, present[1:]):
        va, vb, w = _number(ts, a, mode), _number(ts, b, mode), _where(mode)
        if vb < va and not _repeat(ts, (a, b), mode, _number):
            out.append(f"{b} ({vb:g}{w}) has fewer columns than {a} ({va:g}{w}); a wider "
                       "viewport never loses columns")
    return out


def _step_at_least(ts: TokenSet, floor: float, mode: str) -> str:
    """The fix for a short target: the smallest width primitive the set has
    at `floor` px or more, else the smallest such space step, else the
    value itself. Only tokens the set has are named."""
    for family in ("layout.width.", "space."):
        steps = sorted((_px(ts, t.path, mode), t.path) for t in ts.tokens()
                       if t.layer == "primitive" and t.type == "dimension"
                       and t.path.startswith(family) and _px(ts, t.path, mode) >= floor)
        if steps:
            return f"point it at {steps[0][1]} ({steps[0][0]:g}px) or a larger step"
    return f"give it a value of {floor}px or more"


def _target(ts: TokenSet, mode: str, floor: int, criterion: str) -> List[str]:
    p = "layout.target.min"
    if not _typed(ts, p) or _px(ts, p, mode) >= floor:
        return []
    return [f"{p} ({mode}) is {_px(ts, p, mode):g}px; WCAG {criterion} asks for {floor}px "
            f"targets here, so {_step_at_least(ts, floor, mode)}"]


def _target_minimum(ts: TokenSet, mode: str) -> List[str]:
    return _target(ts, mode, MIN_TARGET_PX, "2.5.8")


def _target_comfortable(ts: TokenSet, mode: str) -> List[str]:
    if COMPACT in mode:
        return []
    return _target(ts, mode, COMFORTABLE_TARGET_PX, "2.5.5")


def _measure(ts: TokenSet, mode: str) -> List[str]:
    p = "layout.measure.text"
    if not _typed(ts, p) or _repeat(ts, (p,), mode, _px):
        return []
    rem = _px(ts, p, mode) / 16
    if rem > MAX_TEXT_MEASURE_REM:
        return [f"{p} is {rem:g}rem{_where(mode)}; lines past about 80 characters tire readers "
                f"(1.4.8), so keep it at {MAX_TEXT_MEASURE_REM}rem or less"]
    return []


# Every check reads the density axis, so a compact override is checked too.
CHECKS: Tuple[Check, ...] = (
    Check("layout-breakpoints", "system", _breakpoints, axes=("density",)),
    Check("layout-columns", "system", _columns, axes=("density",)),
    Check("target-size-minimum", "2.5.8", _target_minimum, axes=("density",)),
    Check("target-size-comfortable", "2.5.5", _target_comfortable, axes=("density",)),
    Check("text-measure", "1.4.8", _measure, axes=("density",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_layout(axes)


FOUNDATION = Foundation(name="layout", generate=_generate, checks=CHECKS, requires=("space",),
                        role_types=ROLE_TYPES)
