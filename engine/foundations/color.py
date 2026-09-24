"""Color foundation: primitives from OKLCH ramps, semantic roles per mode,
the WCAG pairings every system must meet, and a deterministic retune.

generate_color never gates itself: it returns tokens and notes, and
build_system validates and gates them with PAIRINGS and CHECKS, then asks
seed_hint for advice on the failing pairings the brand seed controls."""
from __future__ import annotations

from types import MappingProxyType
from typing import Dict, List, Mapping, Tuple

from engine.foundations.color_math import contrast, hex_to_oklch, luminance, oklch_to_hex
from engine.foundations.foundation import BrandInputs, Foundation, Generated
from engine.foundations.gate import Check, GateFinding, Pairing
from engine.foundations.modes import compress, contexts, parse
from engine.foundations.ramp import STEPS, ramp
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

# Every context color tokens are generated for, base first.
COLOR_CONTEXTS = tuple(contexts(("scheme",)))

STATUS_HUES = {"danger": 25.0, "warning": 75.0, "success": 150.0, "info": 245.0}
STATUS_SEED = (0.58, 0.16)  # OKLCH lightness, chroma for status seeds


_SEMANTIC: Dict[str, Tuple[str, str]] = {
    "color.surface.page": ("color.neutral.50", "color.neutral.950"),
    "color.surface.card": ("color.base.white", "color.neutral.900"),
    "color.surface.sunken": ("color.neutral.100", "color.base.black"),
    "color.surface.inverse": ("color.neutral.900", "color.neutral.100"),
    "color.text.default": ("color.neutral.900", "color.neutral.50"),
    "color.text.muted": ("color.neutral.600", "color.neutral.400"),
    "color.text.inverse": ("color.neutral.50", "color.neutral.900"),
    "color.text.link": ("color.brand.600", "color.brand.300"),
    "color.text.on-action": ("color.base.white", "color.base.white"),
    "color.action.primary": ("color.brand.500", "color.brand.400"),
    "color.action.primary-hover": ("color.brand.600", "color.brand.300"),
    "color.line.subtle": ("color.neutral.200", "color.neutral.800"),
    "color.line.input": ("color.neutral.500", "color.neutral.500"),
    "color.focus.ring": ("color.brand.700", "color.brand.200"),
}
for _s in STATUS_HUES:
    _SEMANTIC[f"color.status.{_s}.text"] = (f"color.{_s}.700", f"color.{_s}.300")
    _SEMANTIC[f"color.status.{_s}.soft"] = (f"color.{_s}.100", f"color.{_s}.900")
# Read-only view: role -> (light primitive, dark primitive).
SEMANTIC: Mapping[str, Tuple[str, str]] = MappingProxyType(_SEMANTIC)

_TEXT_BGS = ("color.surface.page", "color.surface.card")
# Every surface text can sit on; surface.sunken is a text surface too.
_ALL_BGS = _TEXT_BGS + ("color.surface.sunken",)
PAIRINGS: Tuple[Pairing, ...] = tuple(
    [Pairing("color.text.default", bg, 4.5, "1.4.3") for bg in _ALL_BGS]
    + [Pairing("color.text.muted", bg, 4.5, "1.4.3") for bg in _ALL_BGS]
    + [Pairing("color.text.link", bg, 4.5, "1.4.3") for bg in _ALL_BGS]
    + [Pairing("color.text.inverse", "color.surface.inverse", 4.5, "1.4.3")]
    + [Pairing("color.text.on-action", bg, 4.5, "1.4.3")
       for bg in ("color.action.primary", "color.action.primary-hover")]
    + [Pairing(f"color.status.{s}.text", bg, 4.5, "1.4.3")
       for s in STATUS_HUES for bg in _ALL_BGS + (f"color.status.{s}.soft",)]
    + [Pairing("color.line.input", bg, 3.0, "1.4.11") for bg in _TEXT_BGS]
    + [Pairing("color.action.primary", "color.surface.page", 3.0, "1.4.11")]
    + [Pairing("color.action.primary-hover", "color.surface.page", 3.0, "1.4.11")]
    + [Pairing("color.focus.ring", bg, 3.0, "2.4.7") for bg in _ALL_BGS]
    # A ring drawn around the primary button touches its fill (1.4.11).
    + [Pairing("color.focus.ring", "color.action.primary", 3.0, "1.4.11")]
)

# The four roles one joint solver owns: the button fill, its hover step,
# the text on both, and the focus ring that must stand out from the fill
# and from every surface. The gate still checks every pairing whose
# foreground is one of these; the one-pairing-at-a-time retune never moves
# them. See _solve_action_group.
_ACTION_GROUP_ROLES = frozenset({"color.text.on-action", "color.action.primary",
                                 "color.action.primary-hover", "color.focus.ring"})


# M1 name for the generator's result; every foundation now returns Generated.
ColorResult = Generated


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


def _solve_action_group(mode: str, prims: Dict[str, str], pick: Dict[str, Dict[str, str]],
                         notes: List[str]) -> None:
    """Choose action.primary, action.primary-hover, text.on-action and
    focus.ring together for one mode.

    Search order (deterministic):
      1. action.primary at 0, 1, 2, ... ramp steps from its default; at equal
         distance the conventional direction (darker in light, lighter in
         dark) first.
      2. For each primary, the hover one step conventional, one step
         against, then two steps each way.
      3. For each pair, text.on-action as base.white, then base.black.
      4. For each triple, the first ring from _ring_candidates.
    The first candidate that clears every constraint wins:
      on-action on primary and on hover  >= 4.5 (1.4.3)
      primary and hover on the page      >= 3.0 (1.4.11)
      hover's hex differs from primary's
      ring on page, card and sunken      >= 3.0 (2.4.7)
      ring against the primary fill      >= 3.0 (1.4.11)
    When nothing clears, the closest candidate is kept and noted; the gate
    then reports the failing pairings. The generator never raises here.
    """
    primary_role = "color.action.primary"
    hover_role = "color.action.primary-hover"
    on_action_role = "color.text.on-action"
    ring_role = "color.focus.ring"
    defaults = {r: pick[mode][r] for r in (primary_role, hover_role, on_action_role, ring_role)}
    page_hex = prims[pick[mode]["color.surface.page"]]
    ring_bgs = [prims[pick[mode][bg]] for bg in _ALL_BGS]
    rings = _ring_candidates(mode, defaults[ring_role])

    family, default_step = defaults[primary_role].rsplit(".", 1)
    conv = +1 if _scheme(mode) == "light" else -1

    def path_at(idx: int) -> str:
        return f"{family}.{STEPS[idx]}"

    def ring_fit(ring: str, primary_hex: str) -> float:
        hx = prims[ring]
        return min([contrast(hx, bg) / 3.0 for bg in ring_bgs] + [contrast(hx, primary_hex) / 3.0])

    best = None  # (score, ratios, choice) kept when nothing clears
    for primary_idx in _order_from(STEPS.index(int(default_step)), conv):
        primary_hex = prims[path_at(primary_idx)]
        r_pp = contrast(primary_hex, page_hex)
        best_ring = max(rings, key=lambda r: ring_fit(r, primary_hex))
        ring_ok = [r for r in rings if ring_fit(r, primary_hex) >= 1.0]
        for hd in (conv, -conv, 2 * conv, -2 * conv):
            hover_idx = primary_idx + hd
            if not 0 <= hover_idx < len(STEPS):
                continue
            hover_hex = prims[path_at(hover_idx)]
            if hover_hex == primary_hex:
                continue
            r_hp = contrast(hover_hex, page_hex)
            for on_path in ("color.base.white", "color.base.black"):
                r_op = contrast(prims[on_path], primary_hex)
                r_oh = contrast(prims[on_path], hover_hex)
                ring = ring_ok[0] if ring_ok else best_ring
                r_rp = contrast(prims[ring], primary_hex)
                score = min(r_op / 4.5, r_oh / 4.5, r_pp / 3.0, r_hp / 3.0,
                            ring_fit(ring, primary_hex))
                choice = (path_at(primary_idx), path_at(hover_idx), on_path, ring)
                ratios = (r_op, r_oh, r_pp, r_hp, r_rp)
                if best is None or score > best[0]:
                    best = (score, ratios, choice)
                if score >= 1.0:
                    _apply_action_choice(mode, pick, defaults, choice, ratios, notes, solved=True)
                    return

    if best is None:
        # Every hover candidate resolved to the same hex as its primary (a
        # ramp flat end to end). Keep the defaults; the hover-distinct
        # check fails in the gate and names the fix.
        notes.append(
            f"action group ({mode}): every brand step resolves to the same color, so "
            f"{hover_role} cannot differ from {primary_role}; kept the defaults")
        return
    _apply_action_choice(mode, pick, defaults, best[2], best[1], notes, solved=False)


def _apply_action_choice(mode: str, pick: Dict[str, Dict[str, str]], defaults: Dict[str, str],
                         choice: Tuple[str, str, str, str], ratios: Tuple[float, ...],
                         notes: List[str], solved: bool) -> None:
    roles = ("color.action.primary", "color.action.primary-hover", "color.text.on-action",
             "color.focus.ring")
    r_op, r_oh, r_pp, r_hp, r_rp = ratios
    for role, path in zip(roles, choice):
        pick[mode][role] = path
    moves = ", ".join(f"{role} {defaults[role]} -> {path}"
                      for role, path in zip(roles, choice) if defaults[role] != path)
    measured = (f"on-action/primary {r_op:.2f}:1, on-action/hover {r_oh:.2f}:1, "
                f"primary/page {r_pp:.2f}:1, hover/page {r_hp:.2f}:1, ring/primary {r_rp:.2f}:1")
    if not solved:
        notes.append(
            f"action group ({mode}): no combination of the button fill, its hover, the text on "
            f"it and the focus ring within the ramps clears every requirement; kept the closest"
            f"{': ' + moves if moves else ''}, {measured}")
    elif moves:
        notes.append(f"action group ({mode}): {moves}, {measured}")


def seed_hint(ts: TokenSet, finding: GateFinding) -> str:
    """Advice for a failing pairing the brand seed controls: one side
    aliases a brand step in that mode. The direction comes from the other
    side: when it is lighter than the brand color, a darker seed gains
    contrast, otherwise a lighter one does. Pairings the seed does not
    control get no advice ("") and keep the gate's own fix."""
    for side, other in ((finding.fg, finding.bg), (finding.bg, finding.fg)):
        raw = ts.raw(side, finding.mode)
        if is_alias(raw) and alias_target(raw).startswith("color.brand."):
            brand_lum = luminance(ts.resolve(side, finding.mode))
            other_lum = luminance(ts.resolve(other, finding.mode))
            direction = "a darker" if other_lum > brand_lum else "a lighter"
            return ("The brand seed cannot reach it within its ramp; "
                    f"choose {direction} or more saturated seed.")
    return ""


def _hover_distinct(ts: TokenSet, mode: str) -> List[str]:
    primary, hover = "color.action.primary", "color.action.primary-hover"
    if not (ts.has(primary) and ts.has(hover)):
        return []
    p, h = ts.resolve(primary, mode), ts.resolve(hover, mode)
    if p != h:
        return []
    return [f"{hover} equals {primary} ({mode}) at {p}; point {hover} at a neighboring "
            "brand step so the hover state reads as a different color"]


CHECKS: Tuple[Check, ...] = (
    Check("hover-distinct", "system", _hover_distinct, axes=("scheme", "contrast")),)


def _scheme(mode: str) -> str:
    return parse(mode).get("scheme", "light")


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
    pick = {mode: {role: pair[0 if _scheme(mode) == "light" else 1]
                   for role, pair in SEMANTIC.items()}
            for mode in COLOR_CONTEXTS}

    def value(mode: str, role: str) -> str:
        return prims[pick[mode][role]]

    # The action group (fill, hover, text on it, focus ring) is solved
    # jointly by _solve_action_group; every other pairing moves its own
    # foreground away from its background, one step at a time, until all of
    # them hold or the ramp ends. Surfaces never move.
    generic_pairings = [p for p in PAIRINGS if p.fg not in _ACTION_GROUP_ROLES]

    for mode in COLOR_CONTEXTS:
        max_passes = len(generic_pairings) * len(STEPS) + 1
        for _pass in range(max_passes):
            changed = False
            for p in generic_pairings:
                for _ in range(len(STEPS)):
                    ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    if ratio >= p.minimum:
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
                                 f"needs {p.minimum}:1 ({p.criterion})")
                    changed = True
            if not changed:
                break
        # No generic pairing reads an action-group role as its background,
        # so solving the group once, after the loop settles, is enough.
        _solve_action_group(mode, prims, pick, notes)

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
                        checks=CHECKS, hint=seed_hint)
