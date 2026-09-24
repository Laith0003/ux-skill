"""Typography foundation: faces, weights, a size scale in rem, line
heights, letter spacing, and text roles as DTCG typography composites,
with an Arabic variant under dir="rtl".

The type_personality axis picks the face pairing (geometric, neutral,
humanist), each a Latin face with an Arabic face designed to sit beside
it. The contrast axis sets the scale ratio and heading weight; the density
axis sets how open body text is. Under dir="rtl" every role but code
switches to the Arabic face at a size 1 to 2px larger than the Latin one
at the same step, with taller lines and no letter spacing, which would
break the joins between Arabic letters. Code keeps its monospace face and
its Latin size and leading in both directions: Arabic sizing is for Arabic
glyphs. Sizes are rem so they follow the reader's default text size.

Checks: body and fine print keep minimum sizes in both directions;
running text keeps line height 1.5 or more (WCAG 1.4.8) and never
tightens its letters; the Arabic rules above; sizes in rem; and falling
sizes from hero to body. A role of another type than ROLE_TYPES names is
reported once by the build's role-types check and skipped here.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

# type_personality band -> (Latin face, Arabic face)
PAIRINGS = {
    "geometric": ("Manrope", "Readex Pro"),
    "neutral": ("IBM Plex Sans", "IBM Plex Sans Arabic"),
    "humanist": ("Source Sans 3", "Noto Naskh Arabic"),
}
CODE_FACE = ["IBM Plex Mono", "ui-monospace", "monospace"]
WEIGHTS = (400, 500, 600, 700)
STEPS = tuple(range(1, 10))
BODY_STEP = 3
# role -> (size step, weight key, leading index, tracking index, face)
ROLES: Dict[str, Tuple[Any, str, int, int, str]] = {
    "type.text.hero": (9, "heading", 1, 3, "latin"),
    "type.text.heading-1": (7, "heading", 1, 2, "latin"),
    "type.text.heading-2": (5, "heading", 2, 1, "latin"),
    "type.text.heading-3": (4, "heading", 2, 0, "latin"),
    "type.text.body": (3, "regular", 3, 0, "latin"),
    "type.text.body-small": (2, "regular", 3, 0, "latin"),
    "type.text.ui": ("ui", "medium", 2, 0, "latin"),
    "type.text.fine": (1, "regular", 3, 0, "latin"),
    "type.text.code": (2, "regular", 3, 0, "code"),
}
READING = ("type.text.body", "type.text.body-small", "type.text.fine")
HIERARCHY = ("type.text.hero", "type.text.heading-1", "type.text.heading-2",
             "type.text.heading-3", "type.text.body")
MIN_BODY_PX, MIN_FINE_PX, MIN_READING_LEADING = 16, 12, 1.5
FACES = ("latin", "arabic", "code")
ARABIC_FACE = "type.face.arabic"
# Role path -> the token type the checks read; the build's role-types
# check reports any other type once, and the checks below skip it.
ROLE_TYPES: Dict[str, str] = {
    **{f"type.face.{face}": "fontFamily" for face in FACES},
    **{role: "typography" for role in ROLES},
    "type.strong": "fontWeight",
}


def band(type_personality: float) -> str:
    if type_personality < 0.34:
        return "geometric"
    return "humanist" if type_personality >= 0.66 else "neutral"


def ratio(contrast: float) -> float:
    return round(1.125 + 0.2 * contrast, 4)


def latin_px(contrast: float) -> List[int]:
    """Sizes in px for steps 1..9: 12, 14, 16, then the ratio upward."""
    r = ratio(contrast)
    out = [12, 14, 16]
    for n in STEPS[3:]:
        out.append(max(int(16 * r ** (n - BODY_STEP) + 0.5), out[-1] + 1))
    return out


def arabic_px(latin: List[int]) -> List[int]:
    """The Arabic size at each step: 2px larger up to 23px, 1px above."""
    return [px + (2 if px < 24 else 1) for px in latin]


def leading(density: float) -> Dict[int, float]:
    return {1: 1.1, 2: 1.25, 3: round(1.5 + 0.1 * (1 - density), 2)}


def tracking(contrast: float) -> Dict[int, float]:
    t = round((0.5 + 0.5 * contrast) * 20) / 20
    return {0: 0.0, 1: round(-0.25 * t, 3), 2: round(-0.5 * t, 3), 3: round(-1.0 * t, 3)}


def _rem(px: float) -> Dict[str, Any]:
    return {"value": round(px / 16, 4), "unit": "rem"}


def _step(role: str, axes: AxisValues) -> int:
    step = ROLES[role][0]
    return (BODY_STEP if axes.density < 0.5 else 2) if step == "ui" else step


def _weight(key: str, axes: AxisValues) -> int:
    return {"regular": 400, "medium": 500,
            "heading": 700 if axes.contrast >= 0.66 else 600}[key]


def generate_type(axes: AxisValues, arabic: bool = True) -> Generated:
    latin_face, arabic_face = PAIRINGS[band(axes.type_personality)]
    ts = TokenSet()
    ts.add(Token("type.face.latin", "fontFamily", [latin_face, "system-ui", "sans-serif"]))
    if arabic:
        ts.add(Token("type.face.arabic", "fontFamily",
                     [arabic_face, latin_face, "Noto Sans Arabic", "Tahoma", "sans-serif"]))
    ts.add(Token("type.face.code", "fontFamily", list(CODE_FACE)))
    for w in WEIGHTS:
        ts.add(Token(f"type.weight.{w}", "fontWeight", w))
    latin = latin_px(axes.contrast)
    for n, px in zip(STEPS, latin):
        ts.add(Token(f"type.size.latin.{n}", "dimension", _rem(px)))
    if arabic:
        for n, px in zip(STEPS, arabic_px(latin)):
            ts.add(Token(f"type.size.arabic.{n}", "dimension", _rem(px)))
    lead = leading(axes.density)
    for i, v in lead.items():
        ts.add(Token(f"type.leading.latin.{i}", "number", v))
    if arabic:
        for i, v in lead.items():
            ts.add(Token(f"type.leading.arabic.{i}", "number", round(v + 0.2, 2)))
    for i, v in tracking(axes.contrast).items():
        ts.add(Token(f"type.tracking.{i}", "dimension", {"value": v, "unit": "px"}))

    for role, (_, weight, lead_i, track_i, face) in ROLES.items():
        step = _step(role, axes)
        w = "{type.weight.%d}" % _weight(weight, axes)
        value = {"fontFamily": "{type.face.%s}" % face,
                 "fontSize": "{type.size.latin.%d}" % step, "fontWeight": w,
                 "letterSpacing": "{type.tracking.%d}" % track_i,
                 "lineHeight": "{type.leading.latin.%d}" % lead_i}
        modes = {}
        if arabic and face != "code":
            modes["direction:rtl"] = {
                "fontFamily": "{type.face.arabic}",
                "fontSize": "{type.size.arabic.%d}" % step, "fontWeight": w,
                "letterSpacing": "{type.tracking.0}",
                "lineHeight": "{type.leading.arabic.%d}" % lead_i}
        ts.add(Token(role, "typography", value, modes=modes, layer="semantic"))
    ts.add(Token("type.strong", "fontWeight", "{type.weight.%d}" % _weight("heading", axes),
                 layer="semantic"))
    notes = [f"type: {band(axes.type_personality)} pairing, {latin_face}"
             + (f" with {arabic_face}" if arabic else "") + f", ratio {ratio(axes.contrast)}"]
    return Generated(tokens=ts, notes=notes)


def _px(dim: Dict[str, Any]) -> float:
    return dim["value"] * (16 if dim["unit"] == "rem" else 1)


def _typed(ts: TokenSet, path: str) -> bool:
    """The typed accessor every check reads through: a role is read only
    when it exists with the type its role expects."""
    return typed(ts, path, ROLE_TYPES)


def _roles(ts: TokenSet, names) -> List[str]:
    return [r for r in names if _typed(ts, r)]


def _sizes(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for role, floor in (("type.text.body", MIN_BODY_PX), ("type.text.fine", MIN_FINE_PX)):
        if _typed(ts, role):
            px = _px(ts.resolve(role, mode)["fontSize"])
            if px < floor:
                out.append(f"{role} ({mode}) is {px:g}px; it needs at least {floor}px to stay "
                           "readable, so point its fontSize at a larger step")
    return out


def _leading(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for role in _roles(ts, READING):
        v = ts.resolve(role, mode)
        if v["lineHeight"] < MIN_READING_LEADING:
            out.append(f"{role} ({mode}) has line height {v['lineHeight']:g}; running text needs "
                       f"{MIN_READING_LEADING} or more (1.4.8), so point it at a taller leading")
    return out


def _tracking(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for role in _roles(ts, READING):
        v = ts.resolve(role, mode)
        if v["letterSpacing"]["value"] < 0:
            out.append(f"{role} ({mode}) tightens letters to {v['letterSpacing']['value']:g}px; "
                       "running text keeps 0 or more, so point it at type.tracking.0")
    return out


def _first(family: Any) -> str:
    return family if isinstance(family, str) else family[0]


def _arabic(ts: TokenSet, mode: str) -> List[str]:
    """Under rtl every text role but code reads the Arabic face, at the
    Arabic size, with taller lines, and every role, code included, drops
    letter spacing (Arabic comments and strings sit in code too). Code
    keeps its monospace face and its Latin size and leading. A set without
    type.face.arabic is Latin-only and has nothing to check."""
    if "direction:rtl" not in mode or not _typed(ts, ARABIC_FACE):
        return []
    arabic_face = ts.resolve(ARABIC_FACE, mode)
    out = []
    for role in _roles(ts, ROLES):
        code = ROLES[role][4] == "code"
        rtl, ltr = ts.resolve(role, mode), ts.resolve(role, "direction:ltr")
        if not code and rtl["fontFamily"] != arabic_face:
            out.append(f"{role} (direction:rtl) is set in {_first(rtl['fontFamily'])}, not "
                       f"{ARABIC_FACE}; Arabic text needs its own face, so point its "
                       f"direction:rtl fontFamily at {ARABIC_FACE}")
        if rtl["letterSpacing"]["value"] != 0:
            out.append(f"{role} (direction:rtl) spaces letters by "
                       f"{rtl['letterSpacing']['value']:g}px; letter spacing breaks Arabic "
                       "joins, so point it at type.tracking.0")
        if code:
            continue
        grow = _px(rtl["fontSize"]) - _px(ltr["fontSize"])
        if not 1 <= grow <= 2:
            out.append(f"{role} (direction:rtl) is {grow:+g}px against its Latin size; Arabic "
                       "reads at 1 to 2px larger at the same step, so point it at the Arabic "
                       "size for that step")
        if rtl["lineHeight"] <= ltr["lineHeight"]:
            out.append(f"{role} (direction:rtl) has line height {rtl['lineHeight']:g}, not taller "
                       f"than its Latin {ltr['lineHeight']:g}; Arabic needs room for its marks, "
                       "so point it at the Arabic leading")
    return out


def _size_source(ts: TokenSet, role: str, mode: str) -> Optional[str]:
    """The token holding the literal a role's fontSize resolves to in one
    context, following aliases through the role and the field; None when
    the role writes the size inline."""
    raw, path = ts.raw(role, mode), role
    while is_alias(raw):
        path = alias_target(raw)
        raw = ts.raw(path, mode)
    field = raw["fontSize"]
    source = None
    while is_alias(field):
        source = alias_target(field)
        field = ts.raw(source, mode)
    return source


def _rem_sizes(ts: TokenSet, mode: str) -> List[str]:
    """Every text role's fontSize in rem in each direction, wherever it
    points; then, once, any px step in the size tree no role reaches."""
    out, named = [], set()
    for role in _roles(ts, ROLES):
        size = ts.resolve(role, mode)["fontSize"]
        if size["unit"] == "rem":
            continue
        source = _size_source(ts, role, mode)
        named.add(source)
        where = f" through {source}" if source else ""
        fix = f"express {source} in rem" if source else "write it in rem"
        out.append(f"{role} ({mode}) is {size['value']:g}{size['unit']}{where}; sizes in rem "
                   "follow the reader's default text size, so point its fontSize at a size in "
                   f"rem or {fix}")
    if "direction:rtl" in mode:
        return out
    for role in _roles(ts, ROLES):
        named.add(_size_source(ts, role, "direction:rtl"))
    return out + [f"{t.path} is in {t.value['unit']}; sizes in rem follow the reader's default "
                  "text size, so express it in rem"
                  for t in ts.tokens() if t.path.startswith("type.size.")
                  and t.type == "dimension" and t.path not in named
                  and isinstance(t.value, dict) and t.value.get("unit") != "rem"]


def _hierarchy(ts: TokenSet, mode: str) -> List[str]:
    present = _roles(ts, HIERARCHY)
    out = []
    for a, b in zip(present, present[1:]):
        pa, pb = _px(ts.resolve(a, mode)["fontSize"]), _px(ts.resolve(b, mode)["fontSize"])
        if pa <= pb:
            out.append(f"{a} ({mode}, {pa:g}px) is not larger than {b} ({pb:g}px); keep "
                       f"{', '.join(r.rsplit('.', 1)[1] for r in HIERARCHY)} in falling size")
    return out


CHECKS: Tuple[Check, ...] = (
    Check("type-sizes", "system", _sizes, axes=("direction",)),
    Check("reading-leading", "1.4.8", _leading, axes=("direction",)),
    Check("reading-tracking", "system", _tracking, axes=("direction",)),
    Check("arabic-text", "system", _arabic, axes=("direction",)),
    Check("rem-sizes", "system", _rem_sizes, axes=("direction",)),
    Check("type-hierarchy", "system", _hierarchy, axes=("direction",)),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_type(axes, arabic=inputs.arabic)


FOUNDATION = Foundation(name="type", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
