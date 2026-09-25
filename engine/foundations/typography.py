"""Typography foundation: three faces (display, text, mono) with their
Arabic partners, a size scale in rem, weights and letter spacing that vary
along the scale, line heights, text roles as DTCG typography composites,
icon sizes and stroke, and an Arabic variant under dir="rtl".

fonts.choose picks the faces from the axes. The contrast axis sets the
scale ratio (density tightens it); the display weight comes from contrast
and formality and eases toward the text face's heading weight down the
scale; letter spacing tightens toward the largest sizes by the contrast
and formality axes, and small labels open up. Under high contrast every
style set in the text or mono face is one weight heavier. Under dir="rtl"
every style but code switches to the Arabic face (the display
styles to the Arabic display face) at a size larger by the ratio the two
faces' metrics give (fonts.arabic_scale), with taller lines and no letter
spacing, which would break the joins between Arabic letters. Sizes are
rem so they follow the reader's default text size.

Checks: body and fine print keep minimum sizes in both directions;
running text keeps line height 1.5 or more (WCAG 1.4.8) and never
tightens its letters; the Arabic rules above; sizes in rem; falling sizes
from hero to body; high contrast never lightens a style; icon sizes rise
and the stroke stays readable. A role of another type than ROLE_TYPES
names is reported once by the build's role-types check and skipped here.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from engine.foundations import character, fonts
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check
from engine.foundations.modes import compress
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

STEPS = tuple(range(1, 10))
BODY_STEP = 3
BODY_PX = 16
# role -> (size step, face, weight kind, leading index, tracking kind).
# Faces: display, text, mono, label (the mono face for a technical system,
# else the text face). Weight kinds: display (eases along the scale),
# heading, regular, medium. Tracking kinds: scale (tightens with size),
# label (opens up), none.
ROLES: Dict[str, Tuple[Any, str, str, int, str]] = {
    "type.text.hero": (9, "display", "display", 0, "scale"),
    "type.text.heading-1": (8, "display", "display", 0, "scale"),
    "type.text.section-title": (7, "display", "display", 1, "scale"),
    "type.text.figure": (6, "display", "display", 1, "scale"),
    "type.text.heading-2": (5, "text", "heading", 1, "scale"),
    "type.text.heading-3": (4, "text", "heading", 2, "none"),
    "type.text.body": (3, "text", "regular", 3, "none"),
    "type.text.body-small": (2, "text", "regular", 3, "none"),
    "type.text.ui": ("ui", "text", "medium", 2, "none"),
    "type.text.ui-large": (3, "text", "medium", 2, "none"),
    "type.text.label": (2, "label", "medium", 2, "label"),
    "type.text.fine": (1, "text", "regular", 3, "none"),
    "type.text.code": (2, "mono", "regular", 3, "none"),
}
READING = ("type.text.body", "type.text.body-small", "type.text.fine")
HIERARCHY = ("type.text.hero", "type.text.heading-1", "type.text.section-title",
             "type.text.heading-2", "type.text.heading-3", "type.text.body")
MIN_BODY_PX, MIN_FINE_PX, MIN_READING_LEADING = 16, 12, 1.5
# Our floor between neighbouring levels of HIERARCHY: a smaller step does
# not read as a new level. The generator holds every step from body up to
# it after rounding, in both scripts.
MIN_LEVEL_RATIO = 1.08
# Under high contrast, bold words stay at least this far above body text.
STRONG_GAP = 200
# Face roles: the token each face is written to.
FACE_TOKENS = {"display": "type.face.display", "text": "type.face.text",
               "mono": "type.face.mono", "arabic": "type.face.arabic",
               "arabic-display": "type.face.arabic-display"}
ARABIC_FACE = "type.face.arabic"
ARABIC_DISPLAY_FACE = "type.face.arabic-display"
# The one style that keeps its Latin face under rtl: code, whose Arabic
# comments and strings still read in the mono face. A label set in the mono
# face switches to the Arabic face like any other text.
KEEP_FACE = ("type.text.code",)
# A technical system sets labels in the mono face.
MONO_LABEL_FROM = 0.5
# Icon sizes: inline follows body text, control sits in a control, feature
# grows with the contrast axis.
ICON_CONTROL_REM = 1.25
ICON_STROKE_RANGE = (1.0, 3.0)
# The styles that step down on a phone (every width below the tablet
# breakpoint): the three largest display styles. Each takes a factor on its
# size from a phone scale whose ratio is PHONE_RATIO_SHARE of the way from
# 1 to the system's ratio, so a bold system still steps harder than a
# quiet one; each phone size stays at least 1px above the style below it,
# and never above its own size. tokens.css multiplies the style's size and
# letter spacing by --<style>-scale, the factor on a phone and 1 from the
# tablet breakpoint up, so a page reads one property.
PHONE_ROLES = ("type.text.hero", "type.text.heading-1", "type.text.section-title")
PHONE_RATIO_SHARE = 0.6
PHONE_FLOOR_ROLE = "type.text.heading-2"


def phone_token(role: str) -> str:
    """The factor token of a style that steps down on a phone."""
    return "type.phone." + role.rsplit(".", 1)[1]


def phone_px(axes: AxisValues, latin: List[int], body: int = BODY_PX) -> Dict[str, int]:
    """The phone size in px of each style in PHONE_ROLES: the phone scale's
    size at its step, at least 1px above the style below it on the phone
    (heading-2 at its own size for the lowest) and at most its own size."""
    r = 1 + (ratio(axes) - 1) * PHONE_RATIO_SHARE
    floor = latin[ROLES[PHONE_FLOOR_ROLE][0] - 1]
    out: Dict[str, int] = {}
    for role in reversed(PHONE_ROLES):
        n = ROLES[role][0]
        px = min(latin[n - 1], max(int(body * r ** (n - BODY_STEP) + 0.5), floor + 1))
        out[role] = floor = px
    return out


# Run roles: the face a run in the other script takes inside a paragraph.
RUNS = {"type.run.latin": "type.face.text", "type.run.arabic": ARABIC_FACE}
ROLE_TYPES: Dict[str, str] = {
    **{token: "fontFamily" for token in FACE_TOKENS.values()},
    **{role: "typography" for role in ROLES},
    "type.strong": "fontWeight",
    **{run: "fontFamily" for run in RUNS},
    "type.icon.size.inline": "dimension", "type.icon.size.control": "dimension",
    "type.icon.size.feature": "dimension", "type.icon.stroke": "number",
    **{phone_token(role): "number" for role in PHONE_ROLES},
}


def ratio(axes: AxisValues) -> float:
    return character.scale_ratio(axes)


def _clear_level(px: int, below: int) -> int:
    """px raised by whole pixels until it sits MIN_LEVEL_RATIO above the
    step below it."""
    while px / below < MIN_LEVEL_RATIO:
        px += 1
    return px


def latin_px(axes: AxisValues, body: int = BODY_PX) -> List[int]:
    """Sizes in px for steps 1..9: body minus 4, body minus 2, body, then
    the ratio upward, each step at least MIN_LEVEL_RATIO above the one
    below after rounding."""
    r = ratio(axes)
    out = [body - 4, body - 2, body]
    for n in STEPS[3:]:
        out.append(_clear_level(int(body * r ** (n - BODY_STEP) + 0.5), out[-1]))
    return out


def arabic_px(latin: List[int], scale: float) -> List[int]:
    """The Arabic size at each step: the Latin size times the scale the
    two faces' metrics give, at least one pixel larger, and from body up
    at least MIN_LEVEL_RATIO above the step below."""
    out: List[int] = []
    for i, px in enumerate(latin):
        size = max(px + 1, int(px * scale + 0.5))
        out.append(_clear_level(size, out[-1]) if i >= BODY_STEP else size)
    return out


def leading(axes: AxisValues, extra: float = 0.0) -> Dict[int, float]:
    """Line heights: display lines tighten with contrast, reading lines
    open as density falls, and more for long reading (`extra`)."""
    return {0: round(1.05 + 0.1 * (1 - axes.contrast), 2), 1: 1.2, 2: 1.3,
            3: round(1.5 + 0.1 * (1 - axes.density) + extra, 2)}


def _rem(px: float) -> Dict[str, Any]:
    return {"value": round(px / 16, 4), "unit": "rem"}


def _step(role: str, axes: AxisValues) -> int:
    step = ROLES[role][0]
    return (BODY_STEP if axes.density < 0.5 else 2) if step == "ui" else step


def _snap(w: float) -> int:
    return int(round(w / 100.0)) * 100


def weights(axes: AxisValues, choice: fonts.Choice, sizes: List[int]) -> Dict[str, int]:
    """The weight of every style at standard contrast. Display styles ease
    from the display weight at the hero to the heading weight at heading-3
    along a log scale of size; the rest take their kind's weight."""
    display = choice.display.clamp(character.display_weight(axes))
    heading = choice.text.clamp(character.heading_weight(axes))
    hero_px = sizes[ROLES["type.text.hero"][0] - 1]
    h3_px = sizes[ROLES["type.text.heading-3"][0] - 1]
    out = {}
    for role, (_, face, kind, _, _) in ROLES.items():
        if kind == "display":
            px = sizes[_step(role, axes) - 1]
            t = character.log_position(px, h3_px, hero_px)
            out[role] = choice.display.clamp(_snap(heading + (display - heading) * t))
        else:
            out[role] = {"heading": heading, "regular": 400, "medium": 500}[kind]
    return out


def tracking_em(axes: AxisValues, px: float, hero_px: float) -> float:
    """Letter spacing in em for a heading size: 0 at 20px and below, the
    full display tracking at the hero size."""
    return character.display_tracking(axes) * character.log_position(px, 20, hero_px)


def _face_list(face: fonts.Face, *rest: str) -> List[str]:
    return [face.family, fonts.fallback_name(face), *rest]


def generate_type(axes: AxisValues, arabic: bool = True, body_px: int = BODY_PX,
                  leading_extra: float = 0.0) -> Generated:
    choice = fonts.choose(axes)
    ts = TokenSet()
    faces = {
        "display": _face_list(choice.display, choice.display.generic),
        "text": _face_list(choice.text, "system-ui", "sans-serif"),
        "mono": _face_list(choice.mono, "ui-monospace", "monospace"),
        "arabic": _face_list(choice.arabic, choice.text.family, "Tahoma", "sans-serif"),
        "arabic-display": _face_list(choice.arabic_display, choice.arabic.family, "sans-serif"),
    }
    for role, token in FACE_TOKENS.items():
        if arabic or not role.startswith("arabic"):
            ts.add(Token(token, "fontFamily", faces[role]))
    latin = latin_px(axes, body_px)
    scale = fonts.arabic_scale(choice.text, choice.arabic)
    std = weights(axes, choice, latin)
    high = {role: _heavier(role, w, choice) for role, w in std.items()}

    def in_arabic(role: str, w: int) -> int:
        face = choice.arabic_display if ROLES[role][1] == "display" else choice.arabic
        return face.clamp(w)

    strong = _strong(std, high, choice, in_arabic if arabic else None)
    used = sorted(set(std.values()) | set(high.values()) | set(strong.values())
                  | ({in_arabic(r, w) for r, w in list(std.items()) + list(high.items())}
                     if arabic else set()))
    for w in used:
        ts.add(Token(f"type.weight.{w}", "fontWeight", w))
    for n, px in zip(STEPS, latin):
        ts.add(Token(f"type.size.latin.{n}", "dimension", _rem(px)))
    if arabic:
        for n, px in zip(STEPS, arabic_px(latin, scale)):
            ts.add(Token(f"type.size.arabic.{n}", "dimension", _rem(px)))
    lead = leading(axes, leading_extra)
    for i, v in lead.items():
        ts.add(Token(f"type.leading.latin.{i}", "number", v))
    if arabic:
        for i, v in lead.items():
            ts.add(Token(f"type.leading.arabic.{i}", "number", round(v + 0.2, 2)))
    hero_px = latin[ROLES["type.text.hero"][0] - 1]
    ts.add(Token("type.tracking.0", "dimension", {"value": 0, "unit": "px"}))
    scale_steps = sorted({_step(r, axes) for r, spec in ROLES.items() if spec[4] == "scale"})
    for n in scale_steps:
        px = latin[n - 1]
        ts.add(Token(f"type.tracking.step-{n}", "dimension",
                     {"value": round(tracking_em(axes, px, hero_px) * px, 2), "unit": "px"}))
    label_px = latin[_step("type.text.label", axes) - 1]
    ts.add(Token("type.tracking.label", "dimension",
                 {"value": round(character.label_tracking(axes) * label_px, 2), "unit": "px"}))

    label_face = "mono" if character.technical(axes) >= MONO_LABEL_FROM else "text"
    for role, (_, face, _, lead_i, track) in ROLES.items():
        face = label_face if face == "label" else face
        step = _step(role, axes)
        tracking = {"scale": "{type.tracking.step-%d}" % step, "label": "{type.tracking.label}",
                    "none": "{type.tracking.0}"}[track]
        value = {"fontFamily": "{%s}" % FACE_TOKENS[face],
                 "fontSize": "{type.size.latin.%d}" % step,
                 "fontWeight": "{type.weight.%d}" % std[role],
                 "letterSpacing": tracking,
                 "lineHeight": "{type.leading.latin.%d}" % lead_i}
        rtl = value
        arabic_rtl = arabic and role not in KEEP_FACE
        if arabic_rtl:
            arabic_face = ARABIC_DISPLAY_FACE if face == "display" else ARABIC_FACE
            rtl = {"fontFamily": "{%s}" % arabic_face,
                   "fontSize": "{type.size.arabic.%d}" % step,
                   "fontWeight": "{type.weight.%d}" % in_arabic(role, std[role]),
                   "letterSpacing": "{type.tracking.0}",
                   "lineHeight": "{type.leading.arabic.%d}" % lead_i}
        elif arabic:
            # Code keeps its face, size and leading, but drops letter
            # spacing for the Arabic strings it can hold.
            rtl = dict(value, letterSpacing="{type.tracking.0}")
        heavy = "{type.weight.%d}" % high[role]
        heavy_rtl = "{type.weight.%d}" % (in_arabic(role, high[role]) if arabic_rtl
                                          else high[role])
        per_context = {
            "contrast:standard,direction:ltr": value,
            "contrast:high,direction:ltr": dict(value, fontWeight=heavy),
            "contrast:standard,direction:rtl": rtl,
            "contrast:high,direction:rtl": dict(rtl, fontWeight=heavy_rtl),
        }
        if not arabic:
            per_context = {k: v for k, v in per_context.items() if "rtl" not in k}
            per_context = {k.split(",")[0]: v for k, v in per_context.items()}
        base, modes = compress(per_context)
        ts.add(Token(role, "typography", base, modes=modes, layer="semantic"))
    per_strong = {k: "{type.weight.%d}" % w for k, w in strong.items()}
    if not arabic:
        per_strong = {k.split(",")[0]: v for k, v in per_strong.items() if "rtl" not in k}
    base, modes = compress(per_strong)
    ts.add(Token("type.strong", "fontWeight", base, modes=modes, layer="semantic"))
    for run, face in RUNS.items():
        if arabic or run == "type.run.latin":
            ts.add(Token(run, "fontFamily", "{%s}" % face, layer="semantic"))
    feature = round(2.0 + 1.0 * axes.contrast, 4)
    for name, rem in (("inline", body_px / 16), ("control", ICON_CONTROL_REM),
                      ("feature", feature)):
        ts.add(Token(f"type.icon.{name}", "dimension", {"value": round(rem, 4), "unit": "rem"}))
    ts.add(Token("type.icon.stroke-width", "number", character.icon_stroke(axes)))
    for name in ("inline", "control", "feature"):
        ts.add(Token(f"type.icon.size.{name}", "dimension", "{type.icon.%s}" % name,
                     layer="semantic"))
    ts.add(Token("type.icon.stroke", "number", "{type.icon.stroke-width}", layer="semantic"))
    phone = phone_px(axes, latin, body_px)
    for role in reversed(PHONE_ROLES):
        n = ROLES[role][0]
        ts.add(Token(f"type.phone-scale.{n}", "number", round(phone[role] / latin[n - 1], 4)))
    for role in PHONE_ROLES:
        ts.add(Token(phone_token(role), "number", "{type.phone-scale.%d}" % ROLES[role][0],
                     layer="semantic"))
    notes = [f"type: display {choice.display.family}, text {choice.text.family}, mono "
             f"{choice.mono.family}" + (f", Arabic {choice.arabic.family} and "
                                        f"{choice.arabic_display.family} at {scale:g} times the "
                                        "Latin size" if arabic else "")
             + f", ratio {ratio(axes):g}, display weight {std['type.text.hero']}, hero "
             f"{latin[ROLES['type.text.hero'][0] - 1]}px ({phone['type.text.hero']}px on a phone)"]
    return Generated(tokens=ts, notes=notes)


def _strong(std: Dict[str, int], high: Dict[str, int], choice: fonts.Choice,
            in_arabic: Optional[Any]) -> Dict[str, int]:
    """type.strong per context: the text face's heading weight, and under
    high contrast at least STRONG_GAP above body text, which gets heavier
    there too. Under rtl each weight is one the Arabic face ships."""
    h3, body = "type.text.heading-3", "type.text.body"
    out = {"contrast:standard,direction:ltr": std[h3],
           "contrast:high,direction:ltr": choice.text.clamp(
               max(high[h3], high[body] + STRONG_GAP))}
    arabic = in_arabic or (lambda role, w: w)
    out["contrast:standard,direction:rtl"] = arabic(body, std[h3])
    out["contrast:high,direction:rtl"] = arabic(
        body, max(high[h3], arabic(body, high[body]) + STRONG_GAP))
    return out


def _heavier(role: str, weight: int, choice: fonts.Choice) -> int:
    """High contrast adds one weight to every style set in the text or
    mono face, within what the face (and its Arabic partner) ships."""
    face = ROLES[role][1]
    if face == "display":
        return weight
    top = min(choice.text.weights[1], choice.arabic.weights[1], choice.mono.weights[1], 700)
    return max(weight, min(weight + 100, top))


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


# Arabic sits at least a pixel and at most a fifth above the Latin size.
ARABIC_GROW_MAX = 1.2


def _arabic(ts: TokenSet, mode: str) -> List[str]:
    """Under rtl every style set in the text or display face reads the
    Arabic face (or the Arabic display face) at a size 4 to 20 percent
    larger than its Latin size, with taller lines, and every style drops
    letter spacing. Code keeps its face, size and leading. A set without
    type.face.arabic is Latin-only."""
    if "direction:rtl" not in mode or not _typed(ts, ARABIC_FACE):
        return []
    ltr_mode = mode.replace("direction:rtl", "direction:ltr")
    out = []
    mono = _first(ts.resolve("type.face.mono")) if ts.has("type.face.mono") else ""
    for role in _roles(ts, ROLES):
        rtl, ltr = ts.resolve(role, mode), ts.resolve(role, ltr_mode)
        kept = role in KEEP_FACE and rtl["fontFamily"] == ltr["fontFamily"] \
            and _first(ltr["fontFamily"]) == mono
        face = ARABIC_DISPLAY_FACE if ROLES[role][1] == "display" and \
            _typed(ts, ARABIC_DISPLAY_FACE) else ARABIC_FACE
        if not kept and rtl["fontFamily"] != ts.resolve(face, mode):
            out.append(f"{role} (direction:rtl) is set in {_first(rtl['fontFamily'])}, not "
                       f"{face}; Arabic text needs its own face, so point its direction:rtl "
                       f"fontFamily at {face}")
        if rtl["letterSpacing"]["value"] != 0:
            out.append(f"{role} (direction:rtl) spaces letters by "
                       f"{rtl['letterSpacing']['value']:g}px; letter spacing breaks Arabic "
                       "joins, so point it at type.tracking.0")
        if kept:
            continue
        rtl_px, ltr_px = _px(rtl["fontSize"]), _px(ltr["fontSize"])
        if not ltr_px + 1 <= rtl_px <= ltr_px * ARABIC_GROW_MAX:
            out.append(f"{role} (direction:rtl) is {rtl_px:g}px against its Latin {ltr_px:g}px; "
                       "Arabic reads at least 1px and at most a fifth larger than the Latin size "
                       "at the same step, so point it at the Arabic size for that step")
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
        elif pa / pb < MIN_LEVEL_RATIO:
            times = int(pa / pb * 100) / 100
            out.append(f"{a} ({mode}, {pa:g}px) is only {times:.2f} times {b} ({pb:g}px); our "
                       f"floor between neighbouring levels is {MIN_LEVEL_RATIO:g} times, since a "
                       f"smaller step does not read as a new level, so move {a} up the scale")
    return out


def _phone_hierarchy(ts: TokenSet, mode: str) -> List[str]:
    """On a phone the styles in PHONE_ROLES take their size times their
    factor: each factor sits above 0 and at most 1, and the phone sizes
    keep falling from hero to section-title and stay above heading-2."""
    present = [r for r in PHONE_ROLES if _typed(ts, r) and _typed(ts, phone_token(r))]
    if not present:
        return []
    out = []
    sizes = []
    for role in present:
        factor = ts.resolve(phone_token(role), mode)
        if not 0 < factor <= 1:
            out.append(f"{phone_token(role)} ({mode}) is {factor:g}; a phone factor sits above 0 "
                       "and at most 1, so point it at a factor in that range")
        sizes.append((phone_token(role), _px(ts.resolve(role, mode)["fontSize"]) * factor))
    if _typed(ts, PHONE_FLOOR_ROLE):
        sizes.append((PHONE_FLOOR_ROLE, _px(ts.resolve(PHONE_FLOOR_ROLE, mode)["fontSize"])))
    for (a, pa), (b, pb) in zip(sizes, sizes[1:]):
        if pa <= pb:
            out.append(f"{b} ({mode}) gives {pb:.1f}px on a phone, not smaller than {a} at "
                       f"{pa:.1f}px; keep hero, heading-1, section-title and heading-2 in falling "
                       f"size on a phone, so point {b if b != PHONE_FLOOR_ROLE else a} at a "
                       "factor that restores the order")
    return out


def phone_roles(ts: TokenSet) -> List[str]:
    """The styles tokens.css scales on a phone: those with a factor token,
    in a set that has the tablet breakpoint to switch it off at."""
    if not ts.has("layout.breakpoint.tablet"):
        return []
    return [r for r in PHONE_ROLES if ts.has(r) and ts.has(phone_token(r))]


def scale_property(role: str) -> str:
    """The CSS property that holds a style's phone factor or 1."""
    from engine.foundations.tokens import css_property
    return f"{css_property(role)}-scale"


def responsive_lines(ts: TokenSet) -> Dict[str, List[str]]:
    """The declarations for the phone (:root) and from the tablet breakpoint
    up that set each scaled style's factor."""
    from engine.foundations.tokens import css_property
    roles = phone_roles(ts)
    return {"phone": [f"{scale_property(r)}: var({css_property(phone_token(r))});"
                      for r in roles],
            "tablet": [f"{scale_property(r)}: 1;" for r in roles]}


def _high_weights(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast no style is lighter than at standard contrast."""
    if "contrast:high" not in mode:
        return []
    std = mode.replace("contrast:high", "contrast:standard")
    return [f"{role} ({mode}) is weight {ts.resolve(role, mode)['fontWeight']:g}, lighter than "
            f"its {ts.resolve(role, std)['fontWeight']:g} at standard contrast; high contrast "
            "never lightens text, so point its contrast:high fontWeight at a heavier step"
            for role in _roles(ts, ROLES)
            if ts.resolve(role, mode)["fontWeight"] < ts.resolve(role, std)["fontWeight"]]


def _strong_gap(ts: TokenSet, mode: str) -> List[str]:
    """Under high contrast, bold words stay STRONG_GAP above body text, so
    emphasis survives the heavier body the mode gives."""
    if "contrast:high" not in mode or not (_typed(ts, "type.strong")
                                           and _typed(ts, "type.text.body")):
        return []
    strong = ts.resolve("type.strong", mode)
    body = ts.resolve("type.text.body", mode)["fontWeight"]
    if strong - body >= STRONG_GAP:
        return []
    want = int(body + STRONG_GAP)
    return [f"type.strong ({mode}) is weight {strong:g}, only {strong - body:g} above "
            f"type.text.body at {body:g}; bold words must stay at least {STRONG_GAP} above body "
            "text under high contrast, so point its contrast:high value at "
            f"type.weight.{want} or heavier"]


def _icons(ts: TokenSet, mode: str) -> List[str]:
    sizes = [r for r in ("type.icon.size.inline", "type.icon.size.control",
                         "type.icon.size.feature") if _typed(ts, r)]
    out = []
    for a, b in zip(sizes, sizes[1:]):
        pa, pb = _px(ts.resolve(a, mode)), _px(ts.resolve(b, mode))
        if pa >= pb:
            out.append(f"{b} ({pb:g}px) is not larger than {a} ({pa:g}px); keep inline, control "
                       "and feature icons in rising size")
    if _typed(ts, "type.icon.stroke"):
        stroke = ts.resolve("type.icon.stroke", mode)
        lo, hi = ICON_STROKE_RANGE
        if not lo <= stroke <= hi:
            out.append(f"type.icon.stroke is {stroke:g}; on a 24 unit icon a stroke outside {lo:g} "
                       f"to {hi:g} breaks up or fills in, so point it inside that range")
    return out


# High contrast changes only weights; every other check reads direction.
_WEIGHT_ONLY = (("contrast", "high contrast changes only weights, which high-contrast-weights "
                 "reads"),)
CHECKS: Tuple[Check, ...] = (
    Check("type-sizes", "system", _sizes, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("reading-leading", "1.4.8", _leading, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("reading-tracking", "system", _tracking, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("arabic-text", "system", _arabic, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("rem-sizes", "system", _rem_sizes, axes=("direction",), exempt_axes=_WEIGHT_ONLY),
    Check("type-hierarchy", "system", _hierarchy, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("phone-hierarchy", "system", _phone_hierarchy, axes=("direction",),
          exempt_axes=_WEIGHT_ONLY),
    Check("high-contrast-weights", "system", _high_weights, axes=("contrast", "direction")),
    Check("strong-weight", "system", _strong_gap, axes=("contrast", "direction")),
    Check("icon-sizes", "system", _icons,
          exempt_axes=(("direction", "icon sizes and the stroke never carry modes"),
                       ("contrast", "icon sizes and the stroke never carry modes"))),
)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    a = inputs.audience
    return generate_type(axes, arabic=inputs.arabic, body_px=a.body_px,
                         leading_extra=a.leading_extra)


FOUNDATION = Foundation(name="type", generate=_generate, checks=CHECKS, role_types=ROLE_TYPES)
