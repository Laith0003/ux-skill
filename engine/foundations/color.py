"""Color foundation: primitives from OKLCH ramps, semantic roles per mode,
the WCAG pairings every system must meet, and a deterministic retune."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from engine.foundations.color_math import contrast, hex_to_oklch, oklch_to_hex
from engine.foundations.ramp import STEPS, ramp
from engine.foundations.tokens import Token, TokenSet
from engine.synthesizer.axes import AxisValues

STATUS_HUES = {"danger": 25.0, "warning": 75.0, "success": 150.0, "info": 245.0}
STATUS_SEED = (0.58, 0.16)  # OKLCH lightness, chroma for status seeds


@dataclass(frozen=True)
class Pairing:
    fg: str
    bg: str
    minimum: float
    criterion: str


SEMANTIC: Dict[str, Tuple[str, str]] = {
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
    "color.focus.ring": ("color.brand.500", "color.brand.300"),
}
for _s in STATUS_HUES:
    SEMANTIC[f"color.status.{_s}.text"] = (f"color.{_s}.700", f"color.{_s}.300")
    SEMANTIC[f"color.status.{_s}.soft"] = (f"color.{_s}.100", f"color.{_s}.900")

_TEXT_BGS = ("color.surface.page", "color.surface.card")
PAIRINGS: List[Pairing] = (
    [Pairing("color.text.default", bg, 4.5, "1.4.3") for bg in _TEXT_BGS + ("color.surface.sunken",)]
    + [Pairing("color.text.muted", bg, 4.5, "1.4.3") for bg in _TEXT_BGS]
    + [Pairing("color.text.link", bg, 4.5, "1.4.3") for bg in _TEXT_BGS]
    + [Pairing("color.text.inverse", "color.surface.inverse", 4.5, "1.4.3")]
    + [Pairing("color.text.on-action", bg, 4.5, "1.4.3")
       for bg in ("color.action.primary", "color.action.primary-hover")]
    + [Pairing(f"color.status.{s}.text", bg, 4.5, "1.4.3")
       for s in STATUS_HUES for bg in _TEXT_BGS + (f"color.status.{s}.soft",)]
    + [Pairing("color.line.input", bg, 3.0, "1.4.11") for bg in _TEXT_BGS]
    + [Pairing("color.action.primary", "color.surface.page", 3.0, "1.4.11")]
    + [Pairing("color.focus.ring", bg, 3.0, "2.4.7") for bg in _TEXT_BGS]
)


@dataclass
class ColorResult:
    tokens: TokenSet
    notes: List[str] = field(default_factory=list)


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


def generate_color(axes: AxisValues, brand_hex: str) -> ColorResult:
    notes: List[str] = []
    prims = _primitives(axes, brand_hex.upper(), notes)
    pick = {mode: {role: pair[i] for role, pair in SEMANTIC.items()}
            for i, mode in enumerate(("light", "dark"))}

    def value(mode: str, role: str) -> str:
        return prims[pick[mode][role]]

    # color.text.on-action is a single shared value checked against more
    # than one background (action.primary and action.primary-hover), and
    # action.primary itself separately has to hold 3:1 against the page
    # (Pairing 1.4.11 below). Retuning fg away from bg one pairing at a
    # time, in a single linear pass, does not have a fixed point here: for
    # a seed like a saturated yellow, black text passes against a light
    # action.primary while white does not, but action.primary's own 3:1
    # requirement against the page only clears once action.primary is
    # pushed dark enough that white (not black) is what clears 4.5:1 on it.
    # A pass that flips text.on-action back and forth between white and
    # black to chase whichever pairing it last checked never settles.
    # So the two kinds of pairing are resolved differently:
    #  - every ordinary pairing moves its own foreground role, independent
    #    of the others, away from its background's lightness;
    #  - color.text.on-action is resolved once per mode against every
    #    background that uses it at once: try white against all of them,
    #    then black against all of them, and if neither works everywhere,
    #    darken (never lighten) whichever backgrounds fail under white,
    #    then retry. That direction can never fight action.primary's own
    #    3:1-vs-page pairing, which also only ever needs action.primary
    #    darker against a light page, so the two cannot cycle against each
    #    other the way flip-flopping the foreground did.
    # The two phases still run inside the same outer fixed-point loop,
    # since darkening action.primary for text.on-action's sake cannot
    # break its own (also darker-seeking) page pairing, but could in
    # principle leave a later ordinary pairing to react; the outer loop
    # keeps re-running both phases, in the same fixed order every time,
    # until a full pass changes nothing, so the result is deterministic.
    generic_pairings = [p for p in PAIRINGS if p.fg != "color.text.on-action"]
    on_action_bgs = [p.bg for p in PAIRINGS if p.fg == "color.text.on-action"]
    on_action_role = "color.text.on-action"

    for mode in ("light", "dark"):
        max_passes = len(PAIRINGS) * len(STEPS) + 1
        for _pass in range(max_passes):
            changed = False

            for p in generic_pairings:
                for _ in range(len(STEPS)):
                    ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    if ratio >= p.minimum:
                        break
                    target = p.fg
                    bg_light = hex_to_oklch(value(mode, p.bg))[0] > 0.5
                    nxt = _step_path(pick[mode][target], +1 if bg_light else -1)
                    if not nxt:
                        break
                    notes.append(f"{target} ({mode}): {pick[mode][target]} -> {nxt}, "
                                 f"{p.fg} on {p.bg} was {ratio:.2f}:1, needs {p.minimum}:1 ({p.criterion})")
                    pick[mode][target] = nxt
                    changed = True

            for _ in range(len(STEPS)):
                white_ratios = {bg: contrast(prims["color.base.white"], value(mode, bg)) for bg in on_action_bgs}
                if all(r >= 4.5 for r in white_ratios.values()):
                    if pick[mode][on_action_role] != "color.base.white":
                        notes.append(f"{on_action_role} ({mode}): switched back to base.white, "
                                     "now clears 4.5:1 on every action background")
                        pick[mode][on_action_role] = "color.base.white"
                        changed = True
                    break
                black_ratios = {bg: contrast(prims["color.base.black"], value(mode, bg)) for bg in on_action_bgs}
                if all(r >= 4.5 for r in black_ratios.values()):
                    if pick[mode][on_action_role] != "color.base.black":
                        notes.append(f"{on_action_role} ({mode}): base.white fails at least one action "
                                     "background, switched to base.black")
                        pick[mode][on_action_role] = "color.base.black"
                        changed = True
                    break
                failing = [bg for bg, r in white_ratios.items() if r < 4.5] or on_action_bgs
                moved = False
                for bg in failing:
                    nxt = _step_path(pick[mode][bg], +1)
                    if not nxt:
                        continue
                    notes.append(f"{bg} ({mode}): {pick[mode][bg]} -> {nxt}, "
                                 f"{on_action_role} on {bg} was {white_ratios[bg]:.2f}:1, needs 4.5:1 (1.4.3)")
                    pick[mode][bg] = nxt
                    moved = True
                    changed = True
                if not moved:
                    break

            if not changed:
                break

    ts = TokenSet()
    for path, hx in prims.items():
        ts.add(Token(path, "color", hx))
    for role in SEMANTIC:
        light, dark = pick["light"][role], pick["dark"][role]
        ts.add(Token(role, "color", "{" + light + "}", layer="semantic",
                     modes={"dark": "{" + dark + "}"} if dark != light else {}))
    return ColorResult(tokens=ts, notes=notes)
