"""Color foundation: primitives from OKLCH ramps, semantic roles per
context, the WCAG pairings every system must meet, and a deterministic
retune.

Contexts are scheme x contrast (light, dark; standard, high). Each role
starts where SEMANTIC (standard) or HIGH_CONTRAST puts it for the scheme.
Fill groups (a solid fill, its hover and pressed steps, the text on it)
are solved jointly by _solve_group; the primary group also picks the
focus ring, after its fill, so the ring can prefer a color other than the
fill without ever moving it. Every other role moves one ramp step at a
time away from its background until its pairings hold. Surfaces never
move.

generate_color never gates itself: it returns tokens and notes, and
build_system validates and gates them with PAIRINGS and CHECKS, then asks
seed_hint for advice on the failing pairings the brand seed controls."""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Tuple

from engine.foundations.color_math import contrast, hex_to_oklch, luminance, oklch_to_hex
from engine.foundations.foundation import BrandInputs, Foundation, Generated, typed
from engine.foundations.gate import Check, GateFinding, Pairing, cite, required
from engine.foundations.modes import compress, contexts, parse
from engine.foundations.ramp import STEPS, ramp
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

# Every context color tokens are generated for, base first.
COLOR_CONTEXTS = tuple(contexts(("scheme", "contrast")))

STATUS_HUES = {"danger": 25.0, "warning": 75.0, "success": 150.0, "info": 245.0}
STATUS_SEED = (0.58, 0.16)  # OKLCH lightness, chroma for status seeds
# Translucent overlays: black ("shade") and white ("tint") at these percents.
OVERLAY_STEPS = (10, 20, 40, 60, 80)

_SEMANTIC: Dict[str, Tuple[str, str]] = {
    "color.surface.page": ("color.neutral.50", "color.neutral.950"),
    "color.surface.card": ("color.base.white", "color.neutral.900"),
    "color.surface.sunken": ("color.neutral.100", "color.base.black"),
    "color.surface.raised": ("color.base.white", "color.neutral.800"),
    "color.surface.inverse": ("color.neutral.900", "color.neutral.100"),
    "color.surface.selected": ("color.brand.100", "color.brand.900"),
    "color.text.default": ("color.neutral.900", "color.neutral.50"),
    "color.text.muted": ("color.neutral.600", "color.neutral.400"),
    "color.text.inverse": ("color.neutral.50", "color.neutral.900"),
    "color.text.link": ("color.brand.600", "color.brand.300"),
    "color.text.disabled": ("color.neutral.400", "color.neutral.600"),
    "color.text.on-action": ("color.base.white", "color.base.white"),
    "color.text.on-danger": ("color.base.white", "color.base.white"),
    "color.action.primary": ("color.brand.500", "color.brand.400"),
    "color.action.primary-hover": ("color.brand.600", "color.brand.300"),
    "color.action.primary-pressed": ("color.brand.700", "color.brand.200"),
    "color.action.danger": ("color.danger.600", "color.danger.400"),
    "color.action.danger-hover": ("color.danger.700", "color.danger.300"),
    "color.action.danger-pressed": ("color.danger.800", "color.danger.200"),
    # One step off the surfaces a button sits on (card and raised are
    # white in light, neutral.900 and neutral.800 in dark).
    "color.action.disabled": ("color.neutral.200", "color.neutral.700"),
    # A separator sits on card and raised too, so it starts one step off
    # both (neutral.900 and neutral.800 in dark).
    "color.line.subtle": ("color.neutral.200", "color.neutral.700"),
    # A field border sits on every surface a control does. In dark, raised
    # is neutral.800, where neutral.500 falls under 3:1 for every seed, so
    # dark starts one step lighter.
    "color.line.input": ("color.neutral.500", "color.neutral.400"),
    "color.line.selected": ("color.brand.600", "color.brand.300"),
    "color.focus.ring": ("color.brand.700", "color.brand.200"),
    "color.focus.ring-inverse": ("color.brand.300", "color.brand.700"),
    "color.scrim": ("color.shade.40", "color.shade.60"),
}
for _s in STATUS_HUES:
    _SEMANTIC[f"color.status.{_s}.text"] = (f"color.{_s}.700", f"color.{_s}.300")
    _SEMANTIC[f"color.status.{_s}.soft"] = (f"color.{_s}.100", f"color.{_s}.900")
    _SEMANTIC[f"color.status.{_s}.strong"] = (f"color.{_s}.600", f"color.{_s}.400")
    _SEMANTIC[f"color.status.{_s}.on-strong"] = ("color.base.white", "color.base.black")
# Read-only view: role -> (light primitive, dark primitive).
SEMANTIC: Mapping[str, Tuple[str, str]] = MappingProxyType(_SEMANTIC)

# Starting points in contrast:high contexts, per scheme: extreme surfaces,
# text a step or two further out. The retune and the group solver then
# move roles until the raised minimums hold. Roles not listed start where
# the standard table puts them.
_HIGH: Dict[str, Tuple[str, str]] = {
    "color.surface.page": ("color.base.white", "color.base.black"),
    "color.surface.card": ("color.base.white", "color.neutral.950"),
    "color.surface.sunken": ("color.base.white", "color.base.black"),
    "color.surface.raised": ("color.base.white", "color.neutral.900"),
    "color.surface.inverse": ("color.base.black", "color.base.white"),
    "color.surface.selected": ("color.brand.50", "color.brand.950"),
    "color.text.default": ("color.neutral.950", "color.base.white"),
    "color.text.muted": ("color.neutral.800", "color.neutral.200"),
    "color.text.inverse": ("color.base.white", "color.base.black"),
    "color.text.link": ("color.brand.800", "color.brand.200"),
    "color.action.primary": ("color.brand.800", "color.brand.200"),
    "color.action.primary-hover": ("color.brand.900", "color.brand.100"),
    "color.action.primary-pressed": ("color.brand.950", "color.brand.50"),
    "color.action.danger": ("color.danger.800", "color.danger.200"),
    "color.action.danger-hover": ("color.danger.900", "color.danger.100"),
    "color.action.danger-pressed": ("color.danger.950", "color.danger.50"),
    "color.line.subtle": ("color.neutral.400", "color.neutral.600"),
    "color.line.input": ("color.neutral.700", "color.neutral.300"),
    "color.line.selected": ("color.brand.800", "color.brand.200"),
    "color.focus.ring": ("color.brand.600", "color.brand.400"),
    "color.focus.ring-inverse": ("color.brand.200", "color.brand.800"),
    "color.scrim": ("color.shade.60", "color.shade.80"),
}
for _s in STATUS_HUES:
    _HIGH[f"color.status.{_s}.text"] = (f"color.{_s}.800", f"color.{_s}.200")
    _HIGH[f"color.status.{_s}.soft"] = (f"color.{_s}.50", f"color.{_s}.950")
    _HIGH[f"color.status.{_s}.strong"] = (f"color.{_s}.800", f"color.{_s}.200")
HIGH_CONTRAST: Mapping[str, Tuple[str, str]] = MappingProxyType(_HIGH)

# Coverage by construction. Every role read as text pairs with every surface
# text can sit on, at the text minimum (WCAG 1.4.3 4.5:1; 1.4.6 7:1 in high
# contrast). Every line or ring that identifies a control or its state pairs
# with every surface a control sits on, at the non-text minimum (WCAG 1.4.11
# 3:1; our 4.5:1 floor in high contrast). A role or surface added to a table
# gets every pairing it needs; build_pairings writes them.
TEXT_ROLES: Tuple[str, ...] = ("color.text.default", "color.text.muted", "color.text.link") \
    + tuple(f"color.status.{s}.text" for s in STATUS_HUES)
TEXT_SURFACES: Tuple[str, ...] = ("color.surface.page", "color.surface.card",
                                  "color.surface.sunken", "color.surface.raised",
                                  "color.surface.selected")
LINE_ROLES: Tuple[str, ...] = ("color.line.input", "color.line.selected", "color.focus.ring")
LINE_SURFACES: Tuple[str, ...] = ("color.surface.page", "color.surface.card",
                                  "color.surface.sunken", "color.surface.raised")
# Roles in the four families the tables cover (text, surface, line,
# focus) that sit in no table, each with the reason it needs no row there.
# A role added to one of those families must join a table or this map, or
# uncovered_roles names it: a role in neither would get no pairing at all.
COVERAGE_EXEMPT: Mapping[str, str] = MappingProxyType({
    "color.text.inverse": "sits only on color.surface.inverse and is paired there",
    "color.text.disabled": "inactive text, which WCAG exempts from contrast minimums; "
                           "disabled-distinct keeps it apart from enabled text",
    "color.text.on-action": "sits only on the primary fill and its states and is paired there",
    "color.text.on-danger": "sits only on the danger fill and its states and is paired there",
    "color.surface.inverse": "a background whose text and ring are paired against it",
    "color.line.subtle": "a decorative separator with no contrast minimum; "
                         "line-subtle-visible keeps it apart from the surfaces it divides",
    "color.focus.ring-inverse": "the ring for color.surface.inverse and is paired there",
})
COVERAGE_FAMILIES: Tuple[str, ...] = ("color.text.", "color.surface.", "color.line.",
                                      "color.focus.")


def uncovered_roles(roles: Iterable[str]) -> List[str]:
    """Every role in a covered family that no coverage table names and
    COVERAGE_EXEMPT does not excuse, in the order given."""
    tables = set(TEXT_ROLES + TEXT_SURFACES + LINE_ROLES + LINE_SURFACES)
    return [r for r in roles if r.startswith(COVERAGE_FAMILIES)
            and r not in tables and r not in COVERAGE_EXEMPT]

_FILL_STATES = {
    "color.action.primary": ("color.action.primary-hover", "color.action.primary-pressed"),
    "color.action.danger": ("color.action.danger-hover", "color.action.danger-pressed"),
}


def _extra_text_bgs(role: str) -> Tuple[str, ...]:
    """Fills a text role also sits on, beyond the surfaces: body and muted
    copy on every status soft fill (alert and banner copy), status text on
    its own soft fill."""
    if role in ("color.text.default", "color.text.muted"):
        return tuple(f"color.status.{s}.soft" for s in STATUS_HUES)
    if role.startswith("color.status.") and role.endswith(".text"):
        return (role[:-len("text")] + "soft",)
    return ()


def build_pairings(text_roles: Tuple[str, ...] = TEXT_ROLES,
                   text_surfaces: Tuple[str, ...] = TEXT_SURFACES,
                   line_roles: Tuple[str, ...] = LINE_ROLES,
                   line_surfaces: Tuple[str, ...] = LINE_SURFACES) -> Tuple[Pairing, ...]:
    """Every color pairing: the two coverage tables crossed, plus the
    pairings that belong to one fill or one surface."""
    return tuple(
        [Pairing(role, bg, 4.5, "1.4.3")
         for role in text_roles for bg in text_surfaces + _extra_text_bgs(role)]
        + [Pairing("color.text.inverse", "color.surface.inverse", 4.5, "1.4.3")]
        + [Pairing(on, state, 4.5, "1.4.3")
           for fill, on in (("color.action.primary", "color.text.on-action"),
                            ("color.action.danger", "color.text.on-danger"))
           for state in (fill,) + _FILL_STATES[fill]]
        + [Pairing(f"color.status.{s}.on-strong", f"color.status.{s}.strong", 4.5, "1.4.3")
           for s in STATUS_HUES]
        # A focus indicator is a non-text part: 1.4.11 sets its 3:1 against
        # the colors next to it (2.4.7 asks only that focus be visible). The
        # border foundation guarantees border.focus-ring.offset of at least
        # 1px, so the colors next to the ring are the surfaces, never the
        # fill it surrounds; the ring is not paired with the button fill.
        + [Pairing(role, bg, 3.0, "1.4.11") for role in line_roles for bg in line_surfaces]
        + [Pairing(state, "color.surface.page", 3.0, "1.4.11")
           for fill in _FILL_STATES for state in (fill,) + _FILL_STATES[fill]]
        + [Pairing(f"color.status.{s}.strong", "color.surface.page", 3.0, "1.4.11")
           for s in STATUS_HUES]
        # One ring cannot also stand out from the inverse surface, so that
        # surface gets its own.
        + [Pairing("color.focus.ring-inverse", "color.surface.inverse", 3.0, "1.4.11")]
    )


PAIRINGS: Tuple[Pairing, ...] = build_pairings()


def _paired_with(fg: str) -> Tuple[str, ...]:
    """Every background PAIRINGS pairs `fg` with, in declaration order."""
    return tuple(p.bg for p in PAIRINGS if p.fg == fg)


@dataclass(frozen=True)
class _Group:
    """Roles solved together: a fill, its interaction states, the text on
    it, and optionally the focus ring, picked after the fill so it can
    prefer a color other than the fill."""
    fill: str
    on: str
    states: Tuple[str, ...] = ()
    ring: str = ""


GROUPS: Tuple[_Group, ...] = (
    _Group("color.action.primary", "color.text.on-action",
           _FILL_STATES["color.action.primary"], "color.focus.ring"),
    _Group("color.action.danger", "color.text.on-danger", _FILL_STATES["color.action.danger"]),
) + tuple(_Group(f"color.status.{s}.strong", f"color.status.{s}.on-strong") for s in STATUS_HUES)
_GROUP_ROLES = frozenset(r for g in GROUPS for r in (g.fill, g.on, g.ring) + g.states if r)

# M1 name for the generator's result; every foundation now returns Generated.
ColorResult = Generated


def _scheme(mode: str) -> str:
    return parse(mode).get("scheme", "light")


def _default(role: str, mode: str) -> str:
    """Where a role starts in one context, before any retune."""
    table = HIGH_CONTRAST if parse(mode).get("contrast") == "high" and role in HIGH_CONTRAST \
        else SEMANTIC
    return table[role][0 if _scheme(mode) == "light" else 1]


def _need(fg: str, bg: str, mode: str) -> float:
    """The minimum PAIRINGS asks of fg on bg in this context."""
    return next(required(p, mode)[0] for p in PAIRINGS if (p.fg, p.bg) == (fg, bg))


def _neutral_seed(brand_hex: str, axes: AxisValues) -> str:
    _, _, hue = hex_to_oklch(brand_hex)
    return oklch_to_hex(0.55, 0.004 + 0.018 * axes.warmth, hue)


def _primitives(axes: AxisValues, brand_hex: str, notes: List[str]) -> Dict[str, str]:
    prims = {"color.base.white": "#FFFFFF", "color.base.black": "#000000"}
    seeds = {"brand": brand_hex, "neutral": _neutral_seed(brand_hex, axes)}
    seeds.update({s: oklch_to_hex(STATUS_SEED[0], STATUS_SEED[1], h) for s, h in STATUS_HUES.items()})
    for family, seed in seeds.items():
        r = ramp(seed)
        if r.retuned:
            notes.append(f"color.{family}: {r.note}")
        for step, hx in r.stops.items():
            prims[f"color.{family}.{step}"] = hx
    for family, rgb in (("shade", "#000000"), ("tint", "#FFFFFF")):
        for pct in OVERLAY_STEPS:
            prims[f"color.{family}.{pct}"] = rgb + f"{round(pct * 255 / 100):02X}"
    return prims


def _step_path(path: str, delta: int) -> str:
    family, step = path.rsplit(".", 1)
    if not step.isdigit():
        return ""
    i = STEPS.index(int(step)) + delta
    return f"{family}.{STEPS[i]}" if 0 <= i < len(STEPS) else ""


def _order_from(idx: int, conv: int) -> List[int]:
    """Ramp indices from idx outward: idx, then one step in the
    conventional direction, one step against it, two steps, and so on."""
    out = [idx]
    for d in range(1, len(STEPS)):
        for delta in (conv * d, -conv * d):
            if 0 <= idx + delta < len(STEPS) and idx + delta not in out:
                out.append(idx + delta)
    return out


def _ring_candidates(mode: str, default_ring: str) -> List[str]:
    """Where the focus ring may land, in preference order: brand steps
    nearest its default, then neutral steps from the extreme that contrasts
    with the surfaces, then black and white."""
    conv = +1 if _scheme(mode) == "light" else -1
    family, step = default_ring.rsplit(".", 1)
    brand = [f"{family}.{STEPS[i]}" for i in _order_from(STEPS.index(int(step)), conv)]
    light = _scheme(mode) == "light"
    neutral_steps = list(reversed(STEPS)) if light else list(STEPS)
    base = ["color.base.black", "color.base.white"]
    return brand + [f"color.neutral.{s}" for s in neutral_steps] + (
        base if light else list(reversed(base)))


def _state_offsets(conv: int, n: int) -> List[Tuple[int, ...]]:
    """Ramp offsets from the fill for n interaction states, in preference
    order: each state one step further in the conventional direction, then
    against it, then with a gap of two."""
    if n == 0:
        return [()]
    out: List[Tuple[int, ...]] = []
    for d in (conv, -conv, 2 * conv, -2 * conv):
        out.append(tuple(d * (k + 1) for k in range(n)))
    return out


def _choose_ring(rings: List[str], fit: Callable[[str], float], fill_hex: str,
                 prims: Dict[str, str]) -> str:
    """The ring for a fill already chosen: the first candidate that clears
    every surface and differs from the fill, else the first that clears
    every surface (it equals the fill, which the offset makes visible),
    else the closest. Only the ring moves here, never the fill."""
    clear = [r for r in rings if fit(r) >= 1.0]
    if clear:
        return next((r for r in clear if prims[r] != fill_hex), clear[0])
    return max(rings, key=fit)


def _solve_group(g: _Group, mode: str, prims: Dict[str, str],
                 pick: Dict[str, Dict[str, str]], notes: List[str]) -> None:
    """Choose one fill group for one context.

    Search order (deterministic):
      1. the fill at 0, 1, 2, ... ramp steps from its default; at equal
         distance the conventional direction (darker in light, lighter in
         dark) first;
      2. its states (hover, then pressed) one and two steps on in the
         conventional direction, then against it, then with gaps of two;
      3. the text on it as base.white, then base.black;
      4. for the primary group, the ring, after the rest is fixed: brand
         steps nearest its default, then neutral steps, then black and
         white (_ring_candidates), preferring a ring whose color differs
         from the fill. That preference only reorders ring candidates;
         the fill never moves for it.
    The first fill, states and text that clear every constraint win. The
    minimums are PAIRINGS' own in this context, so they rise under
    contrast:high:
      text on the fill and on every state   >= 4.5 (WCAG 1.4.3), 7.0 high (WCAG 1.4.6)
      fill and every state on the page      >= 3.0 (WCAG 1.4.11), 4.5 high (our floor)
      every state's hex differs from the fill's and from each other's
      ring on every surface PAIRINGS names  >= 3.0 (WCAG 1.4.11), 4.5 high (our floor)
    The ring has no minimum against the fill: the border foundation keeps
    page color between an element and its ring.
    When nothing clears, the closest candidate is kept and noted; the gate
    then reports the failing pairings. The generator never raises here.
    """
    roles = (g.fill,) + g.states + (g.on,) + ((g.ring,) if g.ring else ())
    defaults = {r: pick[mode][r] for r in roles}
    page_hex = prims[pick[mode]["color.surface.page"]]
    family, default_step = defaults[g.fill].rsplit(".", 1)
    conv = +1 if _scheme(mode) == "light" else -1
    need_text = _need(g.on, g.fill, mode)
    need_fill = _need(g.fill, "color.surface.page", mode)
    rings = _ring_candidates(mode, defaults[g.ring]) if g.ring else []
    ring_bgs = [(prims[pick[mode][bg]], _need(g.ring, bg, mode)) for bg in _paired_with(g.ring)] \
        if g.ring else []

    def ring_low(ring: str) -> float:
        return min(contrast(prims[ring], hx) for hx, _ in ring_bgs)

    def ring_fit(ring: str) -> float:
        return min(contrast(prims[ring], hx) / need for hx, need in ring_bgs)

    def finish(choice: Tuple[str, ...], hexes: List[str], on: str, solved: bool) -> None:
        summary = (f"text/fill {contrast(prims[on], hexes[0]):.2f}:1, "
                   f"fill/page {contrast(hexes[0], page_hex):.2f}:1")
        if g.ring:
            ring = _choose_ring(rings, ring_fit, hexes[0], prims)
            choice += (ring,)
            solved = solved and ring_fit(ring) >= 1.0
            summary += f", ring/surface {ring_low(ring):.2f}:1"
        _apply(g, mode, pick, defaults, roles, choice, summary, notes, solved=solved)

    best: Optional[Tuple[float, Tuple[str, ...], List[str], str]] = None
    for fill_idx in _order_from(STEPS.index(int(default_step)), conv):
        for offsets in _state_offsets(conv, len(g.states)):
            idxs = [fill_idx] + [fill_idx + o for o in offsets]
            if not all(0 <= i < len(STEPS) for i in idxs):
                continue
            hexes = [prims[f"{family}.{STEPS[i]}"] for i in idxs]
            if len(set(hexes)) != len(hexes):
                continue
            for on in ("color.base.white", "color.base.black"):
                score = min([contrast(prims[on], h) / need_text for h in hexes]
                            + [contrast(h, page_hex) / need_fill for h in hexes])
                choice = tuple(f"{family}.{STEPS[i]}" for i in idxs) + (on,)
                if best is None or score > best[0]:
                    best = (score, choice, hexes, on)
                if score >= 1.0:
                    finish(choice, hexes, on, solved=True)
                    return
    if best is None:
        notes.append(f"{g.fill} group ({mode}): every step of the {family.split('.')[-1]} ramp "
                     "resolves to the same color, so the states cannot differ from the fill; "
                     "kept the defaults")
        return
    finish(best[1], best[2], best[3], solved=False)


def _apply(g: _Group, mode: str, pick: Dict[str, Dict[str, str]], defaults: Dict[str, str],
           roles: Tuple[str, ...], choice: Tuple[str, ...], summary: str, notes: List[str],
           solved: bool) -> None:
    for role, path in zip(roles, choice):
        pick[mode][role] = path
    moves = ", ".join(f"{role} {defaults[role]} -> {path}"
                      for role, path in zip(roles, choice) if defaults[role] != path)
    if not solved:
        notes.append(f"{g.fill} group ({mode}): no combination within the ramps clears every "
                     f"requirement; kept the closest{': ' + moves if moves else ''}, {summary}")
    elif moves:
        notes.append(f"{g.fill} group ({mode}): {moves}, {summary}")


def seed_hint(ts: TokenSet, finding: GateFinding) -> str:
    """Advice for a failing pairing the brand seed controls: one side
    aliases a brand step in that context. The direction comes from the
    other side: when it is lighter than the brand color, a darker seed
    gains contrast, otherwise a lighter one does. Pairings the seed does
    not control get no advice ("") and keep the gate's own fix."""
    for side, other in ((finding.fg, finding.bg), (finding.bg, finding.fg)):
        raw = ts.raw(side, finding.mode)
        if is_alias(raw) and alias_target(raw).startswith("color.brand."):
            brand_lum = luminance(ts.resolve(side, finding.mode))
            other_lum = luminance(ts.resolve(other, finding.mode))
            direction = "a darker" if other_lum > brand_lum else "a lighter"
            return ("The brand seed cannot reach it within its ramp; "
                    f"choose {direction} or more saturated seed.")
    return ""


# Every semantic role is a color. The build's role-types check reports any
# other type once, and the checks below skip it.
ROLE_TYPES: Mapping[str, str] = MappingProxyType({role: "color" for role in SEMANTIC})


def _typed(ts: TokenSet, path: str) -> bool:
    return typed(ts, path, ROLE_TYPES)


def _states_distinct(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for fill, states in _FILL_STATES.items():
        chain = (fill,) + states
        if not all(_typed(ts, r) for r in chain):
            continue
        hexes = [ts.resolve(r, mode) for r in chain]
        for i, role in enumerate(chain[1:], 1):
            if hexes[i] in hexes[:i]:
                other = chain[hexes.index(hexes[i])]
                out.append(f"{role} equals {other} ({mode}) at {hexes[i]}; point {role} at a "
                           "neighboring step so each state reads as a different color")
    return out


def _disabled_visible(ts: TokenSet, mode: str) -> List[str]:
    """A disabled button must not vanish into the surface it sits on.
    Inactive controls are exempt from the WCAG contrast minimums, so this
    asks only that the colors differ."""
    disabled = "color.action.disabled"
    if not _typed(ts, disabled):
        return []
    hx = ts.resolve(disabled, mode)
    return [f"{disabled} equals {bg} ({mode}) at {hx}, so a disabled button vanishes on that "
            "surface. WCAG exempts inactive controls from contrast minimums, so this is a "
            f"distinctness rule, not a ratio: point {disabled} at a step that differs from "
            "color.surface.card and color.surface.raised"
            for bg in ("color.surface.card", "color.surface.raised")
            if _typed(ts, bg) and ts.resolve(bg, mode) == hx]


def _line_subtle_visible(ts: TokenSet, mode: str) -> List[str]:
    """A separator must not vanish into the surface it divides. It is
    decorative, so no contrast ratio applies; this asks only that the
    colors differ."""
    subtle = "color.line.subtle"
    if not _typed(ts, subtle):
        return []
    hx = ts.resolve(subtle, mode)
    return [f"{subtle} equals {bg} ({mode}) at {hx}, so a separator vanishes on that surface. "
            "A decorative line needs no contrast ratio, but it must differ from the surface it "
            f"divides: point {subtle} at a step that differs from color.surface.card and "
            "color.surface.raised"
            for bg in ("color.surface.card", "color.surface.raised")
            if _typed(ts, bg) and ts.resolve(bg, mode) == hx]


def _disabled_distinct(ts: TokenSet, mode: str) -> List[str]:
    out = []
    for disabled, enabled in (("color.text.disabled", ("color.text.default", "color.text.muted")),
                              ("color.action.disabled", ("color.action.primary",))):
        if not _typed(ts, disabled):
            continue
        hx = ts.resolve(disabled, mode)
        for role in enabled:
            if _typed(ts, role) and ts.resolve(role, mode) == hx:
                out.append(f"{disabled} equals {role} ({mode}) at {hx}; point {disabled} at a "
                           "step that reads as inactive next to it")
    return out


def _scheme_polarity(ts: TokenSet, mode: str) -> List[str]:
    """A light scheme has a page lighter than its text, a dark scheme the
    reverse; a set that says dark but ships a light palette is caught here."""
    page, text = "color.surface.page", "color.text.default"
    if not (_typed(ts, page) and _typed(ts, text)):
        return []
    light = _scheme(mode) == "light"
    if (luminance(ts.resolve(page, mode)) > luminance(ts.resolve(text, mode))) == light:
        return []
    want = "lighter" if light else "darker"
    return [f"{page} is not {want} than {text} ({mode}); a {_scheme(mode)} scheme needs a "
            f"{want} page, so point {page} and {text} at the other ends of the neutral ramp"]


CHECKS: Tuple[Check, ...] = (
    Check("states-distinct", "system", _states_distinct, axes=("scheme", "contrast")),
    Check("disabled-distinct", "system", _disabled_distinct, axes=("scheme", "contrast")),
    Check("disabled-visible", "system", _disabled_visible, axes=("scheme", "contrast")),
    Check("line-subtle-visible", "system", _line_subtle_visible, axes=("scheme", "contrast")),
    Check("scheme-polarity", "system", _scheme_polarity, axes=("scheme", "contrast")),
)


def generate_color(axes: AxisValues, brand_hex: str) -> Generated:
    """Low-level call: build_system (and build_color, its color-only
    shortcut) wraps it with input checks, validate and the gate, so prefer
    those unless you need the raw generator.

    Returns the color TokenSet and the retune notes. It never raises for a
    failing pairing: when the ramp cannot reach a minimum it keeps the
    closest step, notes it, and leaves the failure to the gate.
    """
    notes: List[str] = []
    prims = _primitives(axes, brand_hex.upper(), notes)
    pick = {mode: {role: _default(role, mode) for role in SEMANTIC} for mode in COLOR_CONTEXTS}

    def value(mode: str, role: str) -> str:
        return prims[pick[mode][role]]

    generic_pairings = [p for p in PAIRINGS if p.fg not in _GROUP_ROLES]
    for mode in COLOR_CONTEXTS:
        for _pass in range(len(generic_pairings) * len(STEPS) + 1):
            changed = False
            for p in generic_pairings:
                for _ in range(len(STEPS)):
                    ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    minimum, criterion = required(p, mode)
                    if ratio >= minimum:
                        break
                    old = pick[mode][p.fg]
                    bg_light = hex_to_oklch(value(mode, p.bg))[0] > 0.5
                    nxt = _step_path(old, +1 if bg_light else -1)
                    if not nxt:
                        break
                    pick[mode][p.fg] = nxt
                    new_ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    notes.append(f"{p.fg} ({mode}): {old} -> {nxt}, "
                                 f"{p.fg} on {p.bg} was {ratio:.2f}:1, now {new_ratio:.2f}:1, "
                                 f"{cite(minimum, criterion)}")
                    changed = True
            if not changed:
                break
        # No generic pairing reads a group role as its background, so each
        # group is solved once, after the loop settles.
        for g in GROUPS:
            _solve_group(g, mode, prims, pick, notes)

    ts = TokenSet()
    for path, hx in prims.items():
        ts.add(Token(path, "color", hx))
    for role in SEMANTIC:
        base, modes = compress({mode: "{" + pick[mode][role] + "}" for mode in COLOR_CONTEXTS})
        ts.add(Token(role, "color", base, modes=modes, layer="semantic"))
    return Generated(tokens=ts, notes=notes)


def _generate(axes: AxisValues, inputs: BrandInputs) -> Generated:
    return generate_color(axes, inputs.brand_hex)


FOUNDATION = Foundation(name="color", generate=_generate, pairings=PAIRINGS,
                        checks=CHECKS, hint=seed_hint, role_types=ROLE_TYPES)
