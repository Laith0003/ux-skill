"""Post checks that read the page's own design system, time motion by its
curve, and count the structure of a landing page.

A system is present when the page (its own styles, the local stylesheets it
links and, for a stylesheet, the pages that load it) defines custom
properties of the kind a rule judges: font weights, sizes, letter spacing,
durations and curves, colors. A value in that token set passes, because the
system decided it; a value outside it is judged. With no system the rules
keep their absolute thresholds.

Motion is judged by when it answers, not by its nominal length: a direct
response (hover, focus, press, a state change) reaches half its travel
within 70ms and nine tenths within 220ms, an entrance half within 140ms,
computed from the declared curve with ``motion.settle_ms``. An undeclared or
unreadable curve falls back to the rule's nominal cap. An accelerating exit
(an ease-in curve) is held to the nominal cap only.
"""
from __future__ import annotations

import math
import re
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

from engine.foundations import character
from engine.foundations.imagery import GRADE_SPREAD
from engine.foundations.motion import DIRECT_T50, DIRECT_T90, ENTRANCE_T50, settle_ms
from engine.linter.structure import (
    FileContext, _children, _class_list, _decl_map, _heads_a_heading, _linked_sheets,
    _matching_elements, _named_eyebrow, _split_top, _utility_eyebrow, attr_values, block_at,
    compounds, css_blocks, document_or_app_surface, pseudos, tokens,
)
from engine.linter.views import View

# ---------------------------------------------------------------------------
# The page's token set
# ---------------------------------------------------------------------------

_DEF = re.compile(r"(?<![\w-])(--[\w-]+)\s*:\s*([^;{}]*)")
_ONLY_VAR = re.compile(r"^var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)$", re.S)
_NUMBER = re.compile(r"^(-?\d*\.?\d+)\s*(px|rem|em|ms|s)?$", re.I)
_BEZIER = re.compile(r"^cubic-bezier\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)$", re.I)
KEYWORD_CURVES = {
    "ease": [0.25, 0.1, 0.25, 1.0], "linear": [0.0, 0.0, 1.0, 1.0],
    "ease-in": [0.42, 0.0, 1.0, 1.0], "ease-out": [0.0, 0.0, 0.58, 1.0],
    "ease-in-out": [0.42, 0.0, 0.58, 1.0],
}
# Tailwind's easing utilities and the curve its transition utilities default to.
TAILWIND_CURVES = {
    "ease-linear": [0.0, 0.0, 1.0, 1.0], "ease-in": [0.4, 0.0, 1.0, 1.0],
    "ease-out": [0.0, 0.0, 0.2, 1.0], "ease-in-out": [0.4, 0.0, 0.2, 1.0],
}
REM_PX = 16.0
# The curve CSS uses when a transition or animation names none, the one
# Tailwind's transition utilities use, and both spellings of each.
CSS_DEFAULT_CURVE = "ease"
TAILWIND_DEFAULT_CURVE = "cubic-bezier(%s)" % ", ".join(
    str(x) for x in TAILWIND_CURVES["ease-in-out"])
DEFAULT_CURVES = (CSS_DEFAULT_CURVE, TAILWIND_DEFAULT_CURVE)


def _css_texts(ctx: FileContext) -> List[str]:
    out: List[str] = []

    def add(c: FileContext) -> None:
        v = c.views.get("css")
        if v is not None and v.text:
            out.append(v.text)
        out.extend(css for _, css in _linked_sheets(c))
    add(ctx)
    for page in ctx.pages:
        add(page)
    return out


def custom_properties(ctx: FileContext) -> Dict[str, List[str]]:
    """Every custom property the page defines, name to each value written."""
    def build() -> Dict[str, List[str]]:
        out: Dict[str, List[str]] = {}
        for text in _css_texts(ctx):
            text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
            for m in _DEF.finditer(text):
                out.setdefault(m.group(1).lower(), []).append(m.group(2).strip())
        return out
    return ctx.cached("taste:props", build)  # type: ignore[return-value]


def literals(props: Dict[str, List[str]], name: str, seen: Tuple[str, ...] = ()) -> List[str]:
    """The literal values a custom property can take, a var() that is its
    whole value followed to the property it names."""
    out: List[str] = []
    for value in props.get(name, []):
        m = _ONLY_VAR.match(value.strip())
        if not m:
            out.append(value)
            continue
        target = m.group(1).lower()
        got = [] if target in seen or len(seen) > 10 else literals(props, target, seen + (name,))
        out.extend(got)
        if not got and m.group(2):
            out.append(m.group(2).strip())
    return out


def number(value: str) -> Optional[Tuple[float, str]]:
    m = _NUMBER.match(value.strip())
    return (float(m.group(1)), (m.group(2) or "").lower()) if m else None


def ms(value: str) -> Optional[float]:
    n = number(value)
    if n is None or n[1] not in ("ms", "s"):
        return None
    return n[0] * (1000.0 if n[1] == "s" else 1.0)


def curve(value: str) -> Optional[List[float]]:
    value = value.strip().lower()
    if value in KEYWORD_CURVES:
        return KEYWORD_CURVES[value]
    m = _BEZIER.match(value)
    return [float(x) for x in m.groups()] if m else None


def length_px(value: str, font_px: Optional[float] = None) -> Optional[float]:
    n = number(value)
    if n is None:
        return None
    v, unit = n
    if unit in ("px", ""):
        return v if unit or v == 0 else None
    if unit == "rem":
        return v * REM_PX
    if unit == "em" and font_px:
        return v * font_px
    return None


class System:
    """What the page's own custom properties decide, per kind."""

    def __init__(self, props: Dict[str, List[str]]):
        self.props = props
        self.weights: Set[float] = set()
        self.sizes: List[float] = []
        self.tracking: List[Tuple[float, str]] = []
        self.durations: Set[float] = set()
        self.curves: List[List[float]] = []
        self.colors: List[Tuple[int, int, int]] = []
        self.leadings: Set[float] = set()
        # type.capitals: how far the system leans to a capitals display.
        self.capitals: Optional[float] = None
        self.caps = any("caps" in name for name in props)
        self.formality: Optional[float] = None
        for name in props:
            for value in literals(props, name):
                self._read(name, value)

    def _read(self, name: str, value: str) -> None:
        low = value.strip().lower()
        n = number(low)
        if "weight" in name and n is not None and n[1] == "":
            self.weights.add(n[0])
        if "size" in name and "line" not in name:
            px = length_px(low)
            if px is not None and px > 0:
                self.sizes.append(px)
        if ("tracking" in name or "letter-spacing" in name) and n is not None:
            self.tracking.append(n)
        if name == "--type-capitals" and n is not None and n[1] == "":
            self.capitals = n[0]
        if ("leading" in name or "line-height" in name) and n is not None and n[1] == "":
            self.leadings.add(n[0])
        t = ms(low)
        if t is not None:
            self.durations.add(t)
        c = curve(low)
        if c is not None and ("curve" in name or "ease" in name or "timing" in name):
            self.curves.append(c)
        rgb = parse_color(low)
        if rgb is not None and rgb[3] >= 0.999:
            self.colors.append(rgb[:3])
        if name in ("--imagery-grade-spread-lightness", "--imagery-photo-spread-lightness") and n:
            lo, hi = GRADE_SPREAD["lightness"]
            self.formality = character.clamp(1.0 - (n[0] - lo) / (hi - lo))

    def has_duration(self, value: float) -> bool:
        return any(abs(value - d) <= 0.5 for d in self.durations)

    def has_curve(self, c: Sequence[float]) -> bool:
        return any(all(abs(a - b) <= 0.005 for a, b in zip(c, s)) for s in self.curves)

    def has_size(self, px: float) -> bool:
        return any(abs(px - s) <= 0.5 for s in self.sizes)


def system(ctx: FileContext) -> System:
    return ctx.cached("taste:system", lambda: System(custom_properties(ctx)))  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

_HEX = re.compile(r"^#([0-9a-f]{3,8})$")
_RGB = re.compile(r"^rgba?\(\s*([\d.]+%?)[\s,]+([\d.]+%?)[\s,]+([\d.]+%?)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$")


def _channel(v: str) -> float:
    return float(v[:-1]) * 2.55 if v.endswith("%") else float(v)


def _alpha(v: Optional[str]) -> float:
    if v is None:
        return 1.0
    return float(v[:-1]) / 100.0 if v.endswith("%") else float(v)


def parse_color(value: str) -> Optional[Tuple[int, int, int, float]]:
    """(r, g, b, alpha) of a hex or rgb() color, None for anything else."""
    value = value.strip().lower()
    m = _HEX.match(value)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) not in (6, 8):
            return None
        a = int(h[6:8], 16) / 255.0 if len(h) == 8 else 1.0
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a
    m = _RGB.match(value)
    if m:
        try:
            r, g, b = (round(_channel(x)) for x in m.groups()[:3])
            return r, g, b, _alpha(m.group(4))
        except ValueError:
            return None
    return None


# ---------------------------------------------------------------------------
# Rules that judge a type value against a fixed number
# ---------------------------------------------------------------------------

_WEIGHT = re.compile(r"font-weight\s*:\s*(\d+|bolder|bold)", re.I)
_TW_WEIGHT = {"font-bold": 700.0, "font-extrabold": 800.0, "font-black": 900.0}


def _weight(text: str) -> Optional[float]:
    m = _WEIGHT.search(text)
    if m:
        w = m.group(1).lower()
        return 700.0 if w in ("bold", "bolder") else float(w)
    for cls, w in _TW_WEIGHT.items():
        if re.search(r"(?<![\w-])" + cls + r"(?![\w-])", text):
            return w
    return None


def weight_outside_system(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A heavy display weight passes when the page's system has that weight."""
    sys_ = system(ctx)
    w = _weight(match.group(0))
    return not (sys_.weights and w is not None and w in sys_.weights)


def _block_font_px(ctx: FileContext, view: View, pos: int) -> Optional[float]:
    block = block_at(ctx, view, pos)
    if block is None:
        return None
    size = _decl_map(block.body).get("font-size")
    if size is None:
        return None
    m = _ONLY_VAR.match(size.strip())
    if m:
        for v in literals(system(ctx).props, m.group(1).lower()):
            px = length_px(v)
            if px:
                return px
        return None
    return length_px(size)


def _tracking_in_system(sys_: System, value: Tuple[float, str], font_px: Optional[float]) -> bool:
    v, unit = value
    px = v if unit == "px" else v * REM_PX if unit == "rem" else v * font_px if font_px else None
    for t, tu in sys_.tracking:
        if tu == unit and abs(t - v) <= 0.002:
            return True
        tpx = t if tu == "px" else t * REM_PX if tu == "rem" else t * font_px if (tu == "em" and font_px) else None
        if px is not None and tpx is not None and abs(px - tpx) <= 0.05:
            return True
    return False


_TRACK = re.compile(r"letter-spacing\s*:\s*(-?\d*\.?\d+)\s*(em|px|rem)?", re.I)
_TW_TRACK = {"tracking-tighter": (-0.05, "em"), "tracking-tight": (-0.025, "em")}


def tracking_outside_system(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Tight tracking on a heavy display passes when the page's system has
    both the tracking and the weight."""
    sys_ = system(ctx)
    if not sys_.tracking:
        return True
    text = match.group(0)
    m = _TRACK.search(text)
    if m:
        value: Optional[Tuple[float, str]] = (float(m.group(1)), (m.group(2) or "px").lower())
    else:
        value = next((v for cls, v in _TW_TRACK.items()
                      if re.search(r"(?<![\w-])" + cls + r"(?![\w-])", text)), None)
    if value is None:
        return True
    font_px = _block_font_px(ctx, view, match.start()) if m else None
    w = _weight(text)
    weight_ok = not sys_.weights or (w is not None and w in sys_.weights)
    return not (_tracking_in_system(sys_, value, font_px) and weight_ok)


_SIZE = re.compile(r"(?:text-\[|font-size\s*:\s*)(\d+(?:\.\d+)?)px", re.I)


def size_outside_system(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An arbitrary display size passes when the page's system has it."""
    sys_ = system(ctx)
    m = _SIZE.search(match.group(0))
    return not (sys_.sizes and m and sys_.has_size(float(m.group(1))))


_CAPS_SIZE = re.compile(r"font-size\s*:\s*(\d+(?:\.\d+)?)\s*(px|rem)?", re.I)


def capitals_outside_system(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Capitals at a large size pass when the page's system has a capitals
    display role, leans to capitals (type.capitals at CAPITALS_FROM or
    more, when the system emits it), the size is one of the system's two
    largest and the letters are not tracked tight."""
    sys_ = system(ctx)
    if not (sys_.caps and sys_.sizes):
        return True
    if sys_.capitals is not None and sys_.capitals < character.CAPITALS_FROM:
        return True
    m = _CAPS_SIZE.search(match.group(0))
    if not m:
        return True
    px = float(m.group(1)) * (REM_PX if (m.group(2) or "").lower() == "rem" else 1.0)
    top = sorted(set(round(s, 2) for s in sys_.sizes))[-2:]
    if not any(abs(px - t) <= 0.5 for t in top):
        return True
    block = block_at(ctx, view, match.start())
    spacing = _decl_map(block.body).get("letter-spacing", "") if block else ""
    n = number(spacing) if spacing else None
    return bool(n and n[0] < 0)


# ---------------------------------------------------------------------------
# Motion: time to half and nine tenths of the travel
# ---------------------------------------------------------------------------

_STATE_PSEUDOS = {"hover", "focus", "focus-visible", "focus-within", "active", "checked"}
_STATE_ATTR = re.compile(r"\[(?:aria-(?:pressed|selected|expanded|checked|current)|data-state|open)\b", re.I)
_STATE_STRIP = re.compile(r":(?:hover|focus-visible|focus-within|focus|active|checked)\b|"
                          r"\[(?:aria-(?:pressed|selected|expanded|checked|current)|data-state|open)[^\]]*\]",
                          re.I)
# Tailwind variants that apply a class on a person's action or a state.
_TW_STATE = re.compile(r"(?:^|:)(?:hover|focus|focus-visible|focus-within|active|group-hover|peer-hover"
                       r"|peer-focus|aria-[\w-]+|data-\[[^\]]*\])$")


def _has_state(selector: str) -> bool:
    return any(name.lower() in _STATE_PSEUDOS for c in compounds(selector)
               for name, _ in pseudos(c)) or bool(_STATE_ATTR.search(selector))


def _state_subjects(ctx: FileContext, view: View) -> Set[str]:
    def build() -> Set[str]:
        out: Set[str] = set()
        for b in css_blocks(view.text):
            for sel in b.selectors:
                if _has_state(sel):
                    out.add(" ".join(_STATE_STRIP.sub("", sel).split()))
        return out
    return ctx.cached("taste:states:%d" % id(view), build)  # type: ignore[return-value]


def _direct_css(ctx: FileContext, view: View, pos: int) -> bool:
    """A transition answers a person's action when its rule, or another rule
    for the same element, is a hover, focus, press or state."""
    block = block_at(ctx, view, pos)
    if block is None:
        return True
    subjects = _state_subjects(ctx, view)
    return any(_has_state(s) or " ".join(s.split()) in subjects for s in block.selectors)


def _is_exit(c: Sequence[float]) -> bool:
    """An accelerating curve (ease-in): an exit, held to the nominal cap."""
    return c[1] <= 0.05 and c[0] >= 0.3 and c[2] >= 0.6


def answers(duration: float, c: Sequence[float], direct: bool) -> bool:
    """True when a move of ``duration`` on curve ``c`` answers in time."""
    if settle_ms(duration, list(c), 0.5) > (DIRECT_T50 if direct else ENTRANCE_T50):
        return False
    return not direct or settle_ms(duration, list(c), 0.9) <= DIRECT_T90


def _resolve_curve(ctx: FileContext, token: Optional[str]) -> Tuple[str, Optional[List[float]]]:
    """("known", curve), ("system", curve) for a var() the system resolves,
    or ("unknown", None) for an undeclared or unreadable curve."""
    if not token:
        return "unknown", None
    m = _ONLY_VAR.match(token.strip())
    if m:
        for v in literals(system(ctx).props, m.group(1).lower()):
            c = curve(v)
            if c is not None:
                return "system", c
        return "unknown", None
    c = curve(token)
    return ("known", c) if c is not None else ("unknown", None)


def _fires(ctx: FileContext, duration: float, token: Optional[str], direct: bool, cap: float,
           default_fires: bool = False) -> bool:
    """True when the move answers late. An unwritten curve is the default
    one (CSS_DEFAULT_CURVE, or Tailwind's for its utilities) and is judged
    the same as the default written out; with ``default_fires`` (the 300ms
    rule) a move on the default curve outside the system is a finding."""
    sys_ = system(ctx)
    state, c = _resolve_curve(ctx, token)
    if sys_.durations and sys_.has_duration(duration) and (
            state in ("system", "unknown") or (c is not None and sys_.has_curve(c))):
        return False
    if default_fires and token is not None and token.strip().lower() in DEFAULT_CURVES:
        return True
    if c is None or _is_exit(c):
        return duration >= cap
    return not answers(duration, c, direct)


_TIME_TOKEN = re.compile(r"^-?\d*\.?\d+m?s$", re.I)


def _items(value: str) -> List[Tuple[Optional[float], Optional[str]]]:
    """(duration, curve token) of each comma-separated transition or
    animation in a shorthand value."""
    out: List[Tuple[Optional[float], Optional[str]]] = []
    for item in _split_top(value):
        parts = _split_top(item, " ")
        times = [ms(p) for p in parts if _TIME_TOKEN.match(p)]
        token = next((p for p in parts if curve(p) is not None or p.lower().startswith(
            ("cubic-bezier(", "steps(", "linear(", "var(")) or p.lower() in ("step-start", "step-end")),
            None)
        out.append((times[0] if times else None, token))
    return out


def _declaration(view: View, pos: int) -> Tuple[str, str]:
    """(property, value) of the declaration the match at ``pos`` sits in."""
    text = view.text
    begin = max(text.rfind(";", 0, pos), text.rfind("{", 0, pos), text.rfind("}", 0, pos)) + 1
    ends = [i for i in (text.find(";", pos), text.find("}", pos)) if i != -1]
    decl = text[begin:min(ends) if ends else len(text)]
    prop, _, value = decl.partition(":")
    return prop.strip().lower(), value.strip()


def _longhand_curves(ctx: FileContext, view: View, pos: int, prop: str) -> List[str]:
    block = block_at(ctx, view, pos)
    if block is None:
        return []
    value = _decl_map(block.body).get(prop)
    return _split_top(value) if value else []


def _motion_fires(ctx: FileContext, view: View, match: re.Match, start: int,
                  floor: float, cap: float, animation: bool, exact: bool = False,
                  default_fires: bool = False) -> bool:
    """Judge every duration in the declaration at or above ``floor`` (equal
    to it when ``exact``); True when one of them answers late."""
    if view is ctx.views.get("classes"):
        return _classes_fire(ctx, view, match, start, cap, default_fires)
    prop, value = _declaration(view, match.start())
    if prop.startswith("--"):
        return False  # a token definition: the system's own value
    direct = False if animation else _direct_css(ctx, view, match.start())
    if prop.endswith("-duration"):
        durations = [ms(v) for v in _split_top(value)]
        curves = _longhand_curves(ctx, view, match.start(),
                                  prop.replace("-duration", "-timing-function"))
        items = [(d, curves[i % len(curves)] if curves else CSS_DEFAULT_CURVE)
                 for i, d in enumerate(durations)]
    elif prop in ("transition", "animation"):
        curves = _longhand_curves(ctx, view, match.start(), prop + "-timing-function")
        items = [(d, t or (curves[i % len(curves)] if curves else CSS_DEFAULT_CURVE))
                 for i, (d, t) in enumerate(_items(value))]
    else:
        return True
    judged = [(d, t) for d, t in items
              if d is not None and (abs(d - floor) <= 0.5 if exact else d >= floor)]
    if not judged:
        return False
    return any(_fires(ctx, d, t, direct, cap, default_fires) for d, t in judged)


def _classes_fire(ctx: FileContext, view: View, match: re.Match, start: int, cap: float,
                  default_fires: bool = False) -> bool:
    tag = ctx.tag_at(start)
    if tag is not None:
        classes = _class_list(ctx, tag)
    else:
        text = view.text
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.end())
        classes = text[line_start:line_end if line_end != -1 else len(text)].split()
    m = re.search(r"duration-(\d+)", match.group(0))
    duration = float(m.group(1)) if m else 300.0
    direct = any(_TW_STATE.search(c.rsplit(":", 1)[0]) for c in classes if ":" in c)
    # Tailwind's transition utilities default to its ease-in-out curve.
    token: Optional[str] = TAILWIND_DEFAULT_CURVE
    for c in classes:
        bare = c.rsplit(":", 1)[-1]
        if bare in TAILWIND_CURVES:
            token = "cubic-bezier(%s)" % ", ".join(str(x) for x in TAILWIND_CURVES[bare])
        elif bare.startswith("ease-[") and bare.endswith("]"):
            token = bare[6:-1].replace("_", " ")
    return _fires(ctx, duration, token, direct, cap, default_fires)


def transition_answers_late(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    return _motion_fires(ctx, view, match, start, floor=400.0, cap=500.0, animation=False)


def animation_answers_late(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    return _motion_fires(ctx, view, match, start, floor=800.0, cap=800.0, animation=True)


def default_300_answers_late(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    animation = "animation" in match.group(0).lower()
    return _motion_fires(ctx, view, match, start, floor=300.0, cap=300.0, animation=animation,
                         exact=True, default_fires=True)


# ---------------------------------------------------------------------------
# imagery-mandatory-missing: a photograph, unless the brand forbids them
# ---------------------------------------------------------------------------

_PROJECT_MARKERS = (".git", "package.json", "pyproject.toml", "composer.json")
# A layout template: its main holds a slot the pages fill, not content.
_SLOT = re.compile(r"@yield\(|\{\{\s*\$slot\s*\}\}|<slot\b|<router-view\b|<Outlet\b"
                   r"|\{\s*children\s*\}|<%=\s*yield|\{%\s*block\b", re.I)
_UNREADABLE_MEDIA = re.compile(
    r"<iframe\b|<(?!svg\b)[a-z][\w-]*\b[^>]*\brole\s*=\s*[\"']img[\"']"
    r"|<image\b[^>]*\bhref\s*=\s*[\"'][^\"']+\.(?:png|jpe?g|webp|avif|gif)", re.I)


@lru_cache(maxsize=256)
def _forbidden_in(folder: str) -> bool:
    from engine.brand import parse_brand_md, photography_forbidden
    here = Path(folder)
    for level, f in enumerate([here, *here.parents]):
        brand = f / "brand.md"
        if brand.is_file():
            try:
                return photography_forbidden(parse_brand_md(brand.read_text(encoding="utf-8")))
            except (OSError, ValueError):
                return False
        if level >= 4 or any((f / m).exists() for m in _PROJECT_MARKERS):
            return False
    return False


def page_needs_photograph(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A landing page carries a photograph: a raster image, a picture, a
    video or a raster background that is not the logo. An illustration or
    icons alone do not count. A page passes with none only when the brand's
    rules (a brand.md beside it or above it) forbid photography."""
    from engine.brand.fidelity import score_imagery
    if document_or_app_surface(ctx):
        return False
    if _SLOT.search(ctx.text) and "<h1" not in ctx.low:
        return False
    if ctx.path.parent and _forbidden_in(str(ctx.path.resolve().parent)):
        return False
    if score_imagery(ctx.text)["ok"]:
        return False
    return not _UNREADABLE_MEDIA.search(ctx.text)


# ---------------------------------------------------------------------------
# Structure of a landing page
# ---------------------------------------------------------------------------

_MEDIA_TAGS = {"img", "picture", "video", "canvas", "iframe", "figure"}
_HEADING = re.compile(r"^h[1-6]$")


def _big_svg(ctx: FileContext, tag) -> bool:
    a = attr_values(ctx.text, tag)
    for k in ("width", "height"):
        n = number(a.get(k, ("", ""))[1].replace("px", "") or "x")
        if n and n[0] >= 100:
            return True
    vb = a.get("viewbox", ("", ""))[1].split()
    try:
        return len(vb) == 4 and (float(vb[2]) >= 100 or float(vb[3]) >= 100)
    except ValueError:
        return False


def _subtree(ctx: FileContext, i: int) -> List[int]:
    tags, ends, _ = ctx.tree()
    out = []
    j = i + 1
    while j < len(tags) and tags[j].start < ends[i]:
        out.append(j)
        j += 1
    return out


def _has_media(ctx: FileContext, i: int) -> bool:
    tags, _, _ = ctx.tree()
    for j in [i] + _subtree(ctx, i):
        name = tags[j].name.lower()
        if name in _MEDIA_TAGS or (name == "svg" and _big_svg(ctx, tags[j])):
            return True
    return False


def _has_heading(ctx: FileContext, i: int) -> bool:
    tags, _, _ = ctx.tree()
    return any(_HEADING.match(tags[j].name.lower()) for j in [i] + _subtree(ctx, i))


def _sections(ctx: FileContext) -> List[int]:
    """Indexes of the page's sections: every <section> not inside another."""
    def build() -> List[int]:
        tags, ends, parents = ctx.tree()
        out: List[int] = []
        for i, t in enumerate(tags):
            if t.name.lower() != "section":
                continue
            k = parents[i]
            while k >= 0 and tags[k].name.lower() != "section":
                k = parents[k]
            if k < 0:
                out.append(i)
        return out
    return ctx.cached("taste:sections", build)  # type: ignore[return-value]


def _landing(ctx: FileContext) -> bool:
    return not ctx.cached("taste:document", lambda: document_or_app_surface(ctx))


def eyebrow_allowance(sections: int, formality: Optional[float]) -> int:
    """How many sections may carry an eyebrow: the brand's share
    (character.eyebrow_share, from its formality; mid formality when the
    page's system does not say) of the sections, rounded up, at least one."""
    share = character.eyebrow_share(0.5 if formality is None else formality)
    return max(1, math.ceil(sections * share - 1e-9))


def _over_budget_eyebrows(ctx: FileContext) -> Set[int]:
    def build() -> Set[int]:
        sections = _sections(ctx)
        if len(sections) < 3 or not _landing(ctx):
            return set()
        tags, _, _ = ctx.tree()
        found = []
        for i, tag in enumerate(tags):
            classes = _class_list(ctx, tag)
            if classes and (_named_eyebrow(classes)
                            or (_utility_eyebrow(classes) and _heads_a_heading(ctx, i))):
                found.append(tag.start)
        allowed = eyebrow_allowance(len(sections), system(ctx).formality)
        return set(found[allowed:])
    return ctx.cached("taste:eyebrows", build)  # type: ignore[return-value]


def eyebrows_over_budget(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An eyebrow is a finding when more sections carry one than the brand's
    formality allows; the ones past the allowance are reported."""
    return start in _over_budget_eyebrows(ctx)


_CANON = {"h1": "h", "h2": "h", "h3": "h", "h4": "h", "h5": "h", "h6": "h", "img": "m",
          "picture": "m", "video": "m", "canvas": "m", "iframe": "m", "ol": "ul", "button": "a",
          "b": "", "strong": "", "em": "", "i": "", "span": "", "br": "", "source": ""}


def _shape(ctx: FileContext, i: int, depth: int) -> str:
    tags, _, _ = ctx.tree()
    name = tags[i].name.lower()
    canon = _CANON.get(name, name)
    if name == "svg":
        return "m" if _big_svg(ctx, tags[i]) else ""
    if depth == 0 or canon in ("m", "h", "a", "p"):
        return canon
    kids = [s for s in (_shape(ctx, k, depth - 1) for k in _children(ctx).get(i, [])) if s]
    runs: List[str] = []
    for s in kids:
        if runs and runs[-1].rstrip("*") == s:
            if not runs[-1].endswith("*"):
                runs[-1] += "*"
            continue
        runs.append(s)
    return canon + ("(" + ",".join(runs) + ")" if runs else "")


def _repeated_families(ctx: FileContext) -> Set[int]:
    def build() -> Set[int]:
        if not _landing(ctx):
            return set()
        tags, _, _ = ctx.tree()
        seen: Dict[str, int] = {}
        out: Set[int] = set()
        for i in _sections(ctx):
            shape = _shape(ctx, i, 4)
            if shape.count("(") < 2:
                continue
            seen[shape] = seen.get(shape, 0) + 1
            if seen[shape] > 2:
                out.add(tags[i].start)
        return out
    return ctx.cached("taste:families", build)  # type: ignore[return-value]


def layout_family_repeated(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A section is a finding when two earlier sections share its layout:
    the same tree of elements, repeated items counted once, text ignored."""
    return start in _repeated_families(ctx)


def _is_split(ctx: FileContext, i: int) -> bool:
    kids = _children(ctx)
    k = i
    for _ in range(4):
        own = kids.get(k, [])
        if len(own) == 1:
            k = own[0]
            continue
        if len(own) != 2:
            return False
        a, b = own
        media_a, media_b = _has_media(ctx, a), _has_media(ctx, b)
        head_a, head_b = _has_heading(ctx, a), _has_heading(ctx, b)
        return (media_a and not head_a and head_b and not media_b) or \
               (media_b and not head_b and head_a and not media_a)
    return False


def _long_split_runs(ctx: FileContext) -> Set[int]:
    def build() -> Set[int]:
        if not _landing(ctx):
            return set()
        tags, _, parents = ctx.tree()
        out: Set[int] = set()
        run = 0
        last_parent = None
        for i in _sections(ctx):
            if parents[i] != last_parent:
                run = 0
                last_parent = parents[i]
            run = run + 1 if _is_split(ctx, i) else 0
            if run > 2:
                out.add(tags[i].start)
        return out
    return ctx.cached("taste:splits", build)  # type: ignore[return-value]


def split_sections_in_a_row(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A section is a finding when it is the third media-and-text split in
    a row: one side holds the media, the other the heading and text."""
    return start in _long_split_runs(ctx)


_MARQUEE_CLASS = re.compile(r"(?:^|[_-])(?:marquee|ticker)(?:$|[_-])", re.I)


def _extra_marquees(ctx: FileContext) -> Set[int]:
    def build() -> Set[int]:
        tags, ends, parents = ctx.tree()
        found: List[int] = []
        for i, tag in enumerate(tags):
            name = tag.name.lower()
            classes = _class_list(ctx, tag)
            if not (name == "marquee" or "data-marquee" in {a.name.lower() for a in tag.attrs}
                    or any(_MARQUEE_CLASS.search(c) and "__" not in c for c in classes)):
                continue
            k = parents[i]
            nested = False
            while k >= 0:
                if tags[k].start in found:
                    nested = True
                    break
                k = parents[k]
            if not nested:
                found.append(tag.start)
        return set(found[1:])
    return ctx.cached("taste:marquees", build)  # type: ignore[return-value]


def marquee_more_than_one(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Every marquee after the first on a page is a finding."""
    return start in _extra_marquees(ctx)


_ICON_CLASS = re.compile(r"(?:^|[_-])(?:icon|ico|glyph|symbol)(?:$|[_-])", re.I)


def _plain_card(ctx: FileContext, i: int) -> bool:
    """A card that holds just an icon, a title and a line or two of text."""
    tags, _, _ = ctx.tree()
    texts = 0
    for j in _subtree(ctx, i):
        name = tags[j].name.lower()
        if name in _MEDIA_TAGS or (name == "svg" and _big_svg(ctx, tags[j])):
            if name == "img":
                a = attr_values(ctx.text, tags[j])
                src = a.get("src", ("", ""))[1].lower()
                w = number(a.get("width", ("", ""))[1] or "x")
                if src.endswith(".svg") and (w is None or w[0] < 100):
                    continue
            return False
        if name in ("ul", "ol", "table", "form", "dl", "blockquote"):
            return False
        if _HEADING.match(name) or name == "p":
            texts += 1
    return texts <= 3


def _plain_grid(ctx: FileContext, i: int) -> bool:
    kids = _children(ctx).get(i, [])
    return len(kids) >= 3 and all(_plain_card(ctx, k) for k in kids)


def cards_hold_only_icon_title_line(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Three equal cards are a finding only when every card holds just an
    icon, a title and a line; cards that each carry their own image or
    richer content pass."""
    tag = ctx.tag_at(start)
    if tag is None:
        return True
    tags, _, _ = ctx.tree()
    try:
        i = next(k for k, t in enumerate(tags) if t.start == tag.start)
    except StopIteration:
        return True
    return _plain_grid(ctx, i)


def grid_holds_plain_cards(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A repeat(3, 1fr) grid is a finding unless the markup it styles, when
    the file or the pages that load it hold it, gives each cell its own
    media or richer content."""
    block = block_at(ctx, view, match.start())
    if block is None:
        return True
    grids: List[Tuple[FileContext, int]] = []
    for c in [ctx, *ctx.pages]:
        if not c.views.scan.tags:
            continue
        for sel in block.selectors:
            removal = [tokens(x) for x in compounds(sel)]
            grids.extend((c, i) for i in _matching_elements(c, removal))
    if not grids:
        return True
    return any(_plain_grid(c, i) for c, i in grids)


# ---------------------------------------------------------------------------
# text-ink-at-low-alpha
# ---------------------------------------------------------------------------

_TW_INK = re.compile(r"(?<![\w-])text-(black|white|foreground|ink|(?:gray|slate|zinc|neutral|stone)-(\d{2,3}))"
                     r"/(\d{1,2}|\[0?\.\d+\])(?![\w-])")
_MIX = re.compile(r"color-mix\(\s*in\s+[\w-]+\s*,\s*([^,]+?)\s+(\d+(?:\.\d+)?)%\s*,\s*transparent\s*\)", re.I)
INK_ALPHA_FLOOR = 0.7
# The Tailwind inks whose value is fixed; the gray scales and theme names
# follow the project's config, which the lint does not read.
_TW_INK_RGB = {"black": (0, 0, 0), "white": (255, 255, 255)}


def _ink(rgb: Tuple[int, int, int]) -> bool:
    """Near-neutral: the text color, not an accent."""
    return max(rgb) - min(rgb) <= 24


def _composited(rgb: Tuple[int, int, int], alpha: float) -> Tuple[int, int, int]:
    dark = sum(rgb) / 3 < 128
    ground = 255 if dark else 0
    return tuple(round(c * alpha + ground * (1 - alpha)) for c in rgb)  # type: ignore[return-value]


def text_ink_at_low_alpha(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Text set in the ink color at an alpha under 0.7 is a finding unless
    its composited value (over white for dark ink, black for light) is a
    color in the page's own token set."""
    text = match.group(0)
    m = _TW_INK.search(text)
    if m:
        raw = m.group(3)
        alpha = float(raw.strip("[]")) if raw.startswith("[") else int(raw) / 100.0
        if alpha >= INK_ALPHA_FLOOR:
            return False
        rgb = _TW_INK_RGB.get(m.group(1))
        if rgb is None:
            return True  # a theme color with no value the lint can read
        flat = _composited(rgb, alpha)
        return not any(all(abs(a - b) <= 3 for a, b in zip(flat, col))
                       for col in system(ctx).colors)
    value = text.split(":", 1)[1].strip() if ":" in text else text
    mix = _MIX.search(value)
    if mix:
        c = parse_color(mix.group(1))
        if c is None and mix.group(1).strip().lower().startswith("var("):
            return float(mix.group(2)) / 100.0 < INK_ALPHA_FLOOR
        rgb, alpha = (c[:3], float(mix.group(2)) / 100.0) if c else (None, 1.0)
    else:
        c = parse_color(value.rstrip(";").split("!")[0])
        rgb, alpha = (c[:3], c[3]) if c else (None, 1.0)
    if rgb is None or alpha >= INK_ALPHA_FLOOR or not _ink(rgb):
        return False
    flat = _composited(rgb, alpha)
    return not any(all(abs(a - b) <= 3 for a, b in zip(flat, col)) for col in system(ctx).colors)


# ---------------------------------------------------------------------------
# infinite-animation-without-reduced-motion
# ---------------------------------------------------------------------------

_PROGRESS = re.compile(r"spin|loader|loading|progress|busy", re.I)
_REDUCE = re.compile(r"prefers-reduced-motion\s*(?::\s*reduce)?\s*\)", re.I)
_NO_PREF = re.compile(r"prefers-reduced-motion\s*:\s*no-preference", re.I)
_STOPS = re.compile(r"animation(?:-name)?\s*:\s*none|animation-play-state\s*:\s*paused"
                    r"|animation-iteration-count\s*:\s*1\b", re.I)
_ANIMATION_DECL = re.compile(r"(?<![\w-])animation(-duration)?\s*:\s*([^;{}]*)", re.I)
# Our ceiling for a duration that stops a loop in effect: 10ms.
STOP_MS = 10.0


def _stops(body: str) -> bool:
    """The declarations stop an animation: none, paused, one iteration, or
    a duration of STOP_MS or less (the first time in a shorthand)."""
    if _STOPS.search(body):
        return True
    for m in _ANIMATION_DECL.finditer(body):
        for item in _split_top(m.group(2)):
            times = [ms(p) for p in _split_top(item, " ") if _TIME_TOKEN.match(p)]
            if times and times[0] is not None and times[0] <= STOP_MS:
                return True
    return False


# A query that applies only when the person has not asked for less motion.
_NOT_REDUCE = re.compile(r"\bnot\s*\(?\s*prefers-reduced-motion\s*:\s*reduce", re.I)


def _reduce_query(atrule: str) -> bool:
    """An @media rule that applies when reduced motion is asked for."""
    return (atrule.startswith("@media") and bool(_REDUCE.search(atrule))
            and not _NOT_REDUCE.search(atrule) and not _NO_PREF.search(atrule))


def _motion_ok_query(atrule: str) -> bool:
    """An @media rule that applies only when no reduced motion is asked for."""
    return bool(_NO_PREF.search(atrule) or _NOT_REDUCE.search(atrule))


def _guards(ctx: FileContext) -> List[List[str]]:
    """Selectors (as compounds' token sets per selector) that a reduced
    motion query stops."""
    def build() -> List[List[str]]:
        out: List[List[str]] = []
        for text in _css_texts(ctx):
            for b in css_blocks(re.sub(r"/\*.*?\*/", " ", text, flags=re.S)):
                if any(_reduce_query(a) for a in b.atrules) and _stops(b.body):
                    out.extend(b.selectors)
        return out
    return ctx.cached("taste:guards", build)  # type: ignore[return-value]


def _guarded(selector: str, guards: List[str]) -> bool:
    subject = compounds(selector)[-1] if compounds(selector) else ""
    have = tokens(subject)
    for g in guards:
        parts = compounds(g)
        if not parts:
            continue
        want = tokens(parts[-1])
        if not want or want <= {"*"} or parts[-1].strip().startswith("*"):
            return True
        if want <= have:
            return True
    return False


def infinite_animation_unguarded(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An infinite animation is a finding unless it runs only under
    prefers-reduced-motion: no-preference (or not reduce), a reduced-motion
    query stops it (animation none, paused, one iteration or a duration of
    STOP_MS or less, on its selector or on every element), or it is a
    progress indicator. A loop declared inside a reduce query is a finding."""
    block = block_at(ctx, view, match.start())
    if block is None:
        return True
    if any(_motion_ok_query(a) for a in block.atrules):
        return False
    if any(_PROGRESS.search(s) for s in block.selectors):
        return False
    guards = _guards(ctx)
    return not all(_guarded(s, guards) for s in block.selectors)


# ---------------------------------------------------------------------------
# animating-layout-properties: an indicator may change its inline size
# ---------------------------------------------------------------------------

_LAYOUT_PROP = re.compile(r"(?<![\w-])((?:min|max)-(?:width|height|inline-size|block-size)|width|height"
                          r"|top|left|right|bottom|inline-size|block-size|inset(?:-[a-z]+)*"
                          r"|margin(?:-[a-z]+)*|padding(?:-[a-z]+)*)(?![\w-])", re.I)
_INDICATOR = re.compile(r"indicator|underline|ink-?bar|highlight|thumb|selection", re.I)
_SIZE_ONLY = {"width", "inline-size"}


def layout_transition_reflows(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A transition on a layout property is a finding unless its only
    layout property is the inline size of a moving indicator (a selector
    naming an indicator, or an element taken out of flow with position
    absolute or fixed), which reflows nothing beside it."""
    props = {m.group(1).lower() for m in _LAYOUT_PROP.finditer(match.group(0).split(":", 1)[-1])}
    if not props or not props <= _SIZE_ONLY:
        return True
    block = block_at(ctx, view, match.start())
    if block is None:
        return True
    position = _decl_map(block.body).get("position", "").strip().lower()
    return not (any(_INDICATOR.search(s) for s in block.selectors)
                or position in ("absolute", "fixed"))


TASTE_CHECKS = {
    "weight-outside-system": weight_outside_system,
    "tracking-outside-system": tracking_outside_system,
    "size-outside-system": size_outside_system,
    "capitals-outside-system": capitals_outside_system,
    "transition-answers-late": transition_answers_late,
    "animation-answers-late": animation_answers_late,
    "default-300-answers-late": default_300_answers_late,
    "page-needs-photograph": page_needs_photograph,
    "eyebrows-over-budget": eyebrows_over_budget,
    "layout-family-repeated": layout_family_repeated,
    "split-sections-in-a-row": split_sections_in_a_row,
    "marquee-more-than-one": marquee_more_than_one,
    "cards-hold-only-icon-title-line": cards_hold_only_icon_title_line,
    "grid-holds-plain-cards": grid_holds_plain_cards,
    "text-ink-at-low-alpha": text_ink_at_low_alpha,
    "infinite-animation-unguarded": infinite_animation_unguarded,
    "layout-transition-reflows": layout_transition_reflows,
}


# ---------------------------------------------------------------------------
# display-line-height-under-floor
# ---------------------------------------------------------------------------

_RTL_SELECTOR = re.compile(r":lang\(\s*['\"]?(?:ar|fa|ur|he)\b|\[lang\s*[|^*~]?=\s*['\"]?(?:ar|fa|ur|he)\b"
                           r"|\[dir\s*=\s*['\"]?rtl|:dir\(\s*rtl", re.I)
_RTL_PAGE = re.compile(r"<html\b[^>]*\b(?:dir\s*=\s*['\"]?rtl|lang\s*=\s*['\"]?(?:ar|fa|ur|he)\b)", re.I)
_ARABIC_FACE = re.compile(r"arabic|naskh|kufi|thuluth|nastaliq", re.I)
_SHORT_FONT = re.compile(r"(\d*\.?\d+)\s*(px|rem)\s*/\s*(\d*\.?\d+)\s*(px|rem|%)?", re.I)
# Tailwind's display sizes and line-height utilities.
_TW_TEXT = {"5xl": 48.0, "6xl": 60.0, "7xl": 72.0, "8xl": 96.0, "9xl": 128.0}
_TW_LEADING = {"none": 1.0, "tight": 1.25, "snug": 1.375}
_TW_TEXT_CLASS = re.compile(r"(?<![\w:/-])text-(?:([5-9]xl)|\[(\d*\.?\d+)(px|rem)\])(?![\w-])", re.I)
_TW_LEAD_CLASS = re.compile(r"(?<![\w:/-])leading-(?:(none|tight|snug)|\[(\d*\.?\d+)\])(?![\w-])", re.I)


def _font_size_px(ctx: FileContext, value: str) -> Optional[float]:
    """A font size in px: a length, a var() into the page's system, or the
    largest length inside clamp(), min() or max()."""
    value = value.strip()
    m = _ONLY_VAR.match(value)
    if m:
        for v in literals(system(ctx).props, m.group(1).lower()):
            px = _font_size_px(ctx, v)
            if px:
                return px
        return None
    if "(" in value:
        found = [length_px(x) for x in re.findall(r"\d*\.?\d+(?:px|rem)", value, re.I)]
        found = [x for x in found if x]
        return max(found) if found else None
    return length_px(value)


def _ratio(value: str, font_px: float) -> Optional[float]:
    """A line height as a multiple of the font size; None for a var(),
    normal or anything unreadable."""
    n = number(value.strip())
    if n is None:
        m = re.match(r"^(\d*\.?\d+)%$", value.strip())
        return float(m.group(1)) / 100.0 if m else None
    v, unit = n
    if unit == "":
        return v
    px = length_px(value.strip(), font_px)
    return px / font_px if px is not None else None


def _rtl_block(ctx: FileContext, block) -> bool:
    if any(_RTL_SELECTOR.search(s) for s in block.selectors):
        return True
    family = _decl_map(block.body).get("font-family", "")
    if _ARABIC_FACE.search(family):
        return True
    raw = ctx.views.get("raw")
    return bool(raw is not None and _RTL_PAGE.search(raw.text))


def _leading_in_system(sys_: System, ratio: float) -> bool:
    return any(abs(ratio - v) <= 0.005 for v in sys_.leadings)


def display_leading_outside_floor(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A display line height (40px and up) under the engine's floor for its
    size (typography.display_leading_floor, 0.15 higher for Arabic) is a
    finding unless the page's system has that line height."""
    from engine.foundations.typography import DISPLAY_LEAD_PX, display_leading_floor
    text = match.group(0)
    sys_ = system(ctx)
    if text.lower().startswith("class="):
        size = _TW_TEXT_CLASS.search(text)
        lead = _TW_LEAD_CLASS.search(text)
        if not (size and lead):
            return False
        px = _TW_TEXT[size.group(1).lower()] if size.group(1) else (
            float(size.group(2)) * (REM_PX if size.group(3).lower() == "rem" else 1.0))
        ratio = _TW_LEADING[lead.group(1).lower()] if lead.group(1) else float(lead.group(2))
        raw = ctx.views.get("raw")
        rtl = bool(raw is not None and _RTL_PAGE.search(raw.text))
    else:
        block = block_at(ctx, view, match.start())
        if block is None:
            return False
        decls = _decl_map(block.body)
        short = _SHORT_FONT.search(decls.get("font", "")) if "font" in decls else None
        if text.lower().lstrip().startswith("font") and not text.lower().lstrip().startswith("font-"):
            if not short:
                return False
            px = float(short.group(1)) * (REM_PX if short.group(2).lower() == "rem" else 1.0)
            ratio = _ratio(short.group(3) + (short.group(4) or ""), px)
        else:
            if "font-size" not in decls:
                return False
            px = _font_size_px(ctx, decls["font-size"])
            if px is None:
                return False
            ratio = _ratio(decls.get("line-height", text.split(":", 1)[-1]), px)
        rtl = _rtl_block(ctx, block)
    if ratio is None or px is None or px < DISPLAY_LEAD_PX[0]:
        return False
    if ratio >= display_leading_floor(px, arabic=rtl) - 0.005:
        return False
    return not _leading_in_system(sys_, ratio)


TASTE_CHECKS["display-leading-outside-floor"] = display_leading_outside_floor
