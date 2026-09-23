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
    #    of the others, away from its background's lightness (phase 1);
    #  - color.text.on-action is resolved once per mode against every
    #    background that uses it at once (phase 2): try white against all
    #    of them, then black against all of them, and if neither works
    #    everywhere, darken (never lighten) whichever backgrounds fail
    #    under white, then retry. That direction can never fight
    #    action.primary's own 3:1-vs-page pairing, which also only ever
    #    needs action.primary darker against a light page, so the two
    #    cannot cycle against each other the way flip-flopping the
    #    foreground did. This joint resolution is what gives the loop a
    #    fixed point at all: with max_passes forced to 1, every seed in
    #    the brief and in the wider sweep still passes every pairing, so
    #    it is phase 2's logic doing the real work, not the repetition.
    #  - action.primary-hover is then nudged off action.primary when the
    #    two have converged to the same color (phase 3, R16 item 3).
    # All three phases run inside the same outer loop, repeated (in the
    # same fixed order every time) until a full pass changes nothing. That
    # repetition is kept only as a defensive guard: phase 3 moving hover,
    # or phase 1 reacting to a phase-2 move, could in principle need a
    # second look, even though no seed found so far actually needs one.
    generic_pairings = [p for p in PAIRINGS if p.fg != "color.text.on-action"]
    on_action_bgs = [p.bg for p in PAIRINGS if p.fg == "color.text.on-action"]
    on_action_role = "color.text.on-action"
    primary_role = "color.action.primary"
    hover_role = "color.action.primary-hover"

    for mode in ("light", "dark"):
        max_passes = len(PAIRINGS) * len(STEPS) + 1
        for _pass in range(max_passes):
            changed = False

            # Phase 1: ordinary pairings, each moving its own foreground.
            for p in generic_pairings:
                for _ in range(len(STEPS)):
                    ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    if ratio >= p.minimum:
                        break
                    target = p.fg
                    old = pick[mode][target]
                    bg_light = hex_to_oklch(value(mode, p.bg))[0] > 0.5
                    nxt = _step_path(old, +1 if bg_light else -1)
                    if not nxt:
                        break
                    pick[mode][target] = nxt
                    new_ratio = contrast(value(mode, p.fg), value(mode, p.bg))
                    notes.append(f"{target} ({mode}): {old} -> {nxt}, "
                                 f"{p.fg} on {p.bg} was {ratio:.2f}:1, now {new_ratio:.2f}:1, "
                                 f"needs {p.minimum}:1 ({p.criterion})")
                    changed = True

            # Phase 2: color.text.on-action, resolved jointly (see above).
            for _ in range(len(STEPS)):
                white_ratios = {bg: contrast(prims["color.base.white"], value(mode, bg)) for bg in on_action_bgs}
                if all(r >= 4.5 for r in white_ratios.values()):
                    old = pick[mode][on_action_role]
                    if old != "color.base.white":
                        old_ratios = {bg: contrast(prims[old], value(mode, bg)) for bg in on_action_bgs}
                        worst_bg, worst_ratio = min(old_ratios.items(), key=lambda kv: kv[1])
                        new_ratio = min(white_ratios.values())
                        pick[mode][on_action_role] = "color.base.white"
                        notes.append(f"{on_action_role} ({mode}): {old} -> color.base.white, "
                                     f"{on_action_role} on {worst_bg} was {worst_ratio:.2f}:1, "
                                     f"now {new_ratio:.2f}:1 on every action background, "
                                     "needs 4.5:1 (1.4.3)")
                        changed = True
                    break
                black_ratios = {bg: contrast(prims["color.base.black"], value(mode, bg)) for bg in on_action_bgs}
                if all(r >= 4.5 for r in black_ratios.values()):
                    old = pick[mode][on_action_role]
                    if old != "color.base.black":
                        old_ratios = white_ratios if old == "color.base.white" else {
                            bg: contrast(prims[old], value(mode, bg)) for bg in on_action_bgs}
                        worst_bg, worst_ratio = min(old_ratios.items(), key=lambda kv: kv[1])
                        new_ratio = min(black_ratios.values())
                        pick[mode][on_action_role] = "color.base.black"
                        notes.append(f"{on_action_role} ({mode}): {old} -> color.base.black, "
                                     f"{on_action_role} on {worst_bg} was {worst_ratio:.2f}:1, "
                                     f"now {new_ratio:.2f}:1 on every action background, "
                                     "needs 4.5:1 (1.4.3)")
                        changed = True
                    break
                failing = [bg for bg, r in white_ratios.items() if r < 4.5] or on_action_bgs
                moved = False
                for bg in failing:
                    old = pick[mode][bg]
                    nxt = _step_path(old, +1)
                    if not nxt:
                        continue
                    pick[mode][bg] = nxt
                    new_ratio = contrast(prims["color.base.white"], value(mode, bg))
                    notes.append(f"{bg} ({mode}): {old} -> {nxt}, "
                                 f"{on_action_role} on {bg} was {white_ratios[bg]:.2f}:1, "
                                 f"now {new_ratio:.2f}:1, needs 4.5:1 (1.4.3)")
                    moved = True
                    changed = True
                if not moved:
                    break

            # Phase 3 (R16 item 3): action.primary-hover has no pairing of
            # its own against the page, only the shared on-action pairing,
            # so phases 1 and 2 can legitimately leave it resolving to the
            # exact same primitive as action.primary. A hover state that
            # is indistinguishable from the resting state is a real defect
            # even though nothing above treats it as a contrast failure.
            # Once hover reads the same color as primary, nudge it one
            # ramp step further out, preferring whichever direction primary
            # generally moves in this mode (darker in light mode, lighter
            # in dark mode) but only when that direction does not undo
            # phase 2's own work: if that step would fail text.on-action
            # against the new hover value while the other neighboring step
            # would not, take the one that keeps on-action passing instead
            # (otherwise phase 2 would just darken hover back on the next
            # pass, and this phase would push it back again, forever).
            # Phase 2 re-checks text.on-action against the new hover value
            # on the next pass regardless, applying the exact same
            # white/black/darken resolution it already applies to
            # action.primary.
            if value(mode, hover_role) == value(mode, primary_role):
                delta = +1 if mode == "light" else -1
                old = pick[mode][hover_role]
                candidates = [c for c in (_step_path(old, delta), _step_path(old, -delta))
                              if c and c != pick[mode][primary_role]]
                if candidates:
                    on_action_hex = prims[pick[mode][on_action_role]]
                    passing = [c for c in candidates if contrast(on_action_hex, prims[c]) >= 4.5]
                    nxt = passing[0] if passing else candidates[0]
                    pick[mode][hover_role] = nxt
                    new_ratio = contrast(on_action_hex, value(mode, hover_role))
                    notes.append(f"{hover_role} ({mode}): {old} -> {nxt}, "
                                 f"equaled {primary_role} at {old}, moved one step to stay "
                                 f"distinct, {on_action_role} on {hover_role} now {new_ratio:.2f}:1")
                    changed = True

            if not changed:
                break

    ts = TokenSet()
    for path, hx in prims.items():
        ts.add(Token(path, "color", hx))
    for role in SEMANTIC:
        light, dark = pick["light"][role], pick["dark"][role]
        ts.add(Token(role, "color", "{" + light + "}", layer="semantic",
                     modes={"dark": "{" + dark + "}"} if dark != light else {}))

    # R16 item 1 (CRITICAL): every move above is bounded by the ramp's own
    # ends, so any of them can legitimately do nothing (the "if not nxt"
    # and "if not moved" guards above) and leave a pairing still failing,
    # for example when a seed's ramp genuinely has no step that clears a
    # threshold. Re-verify every pairing, in both modes, against the
    # result actually being returned, and fail loudly rather than let a
    # design system that violates its own WCAG gate ship silently.
    for mode in ts.mode_names:
        for p in PAIRINGS:
            ratio = contrast(ts.resolve(p.fg, mode), ts.resolve(p.bg, mode))
            if ratio < p.minimum:
                raise ValueError(
                    f"{p.fg} on {p.bg} ({mode}) is {ratio:.2f}:1; WCAG {p.criterion} "
                    f"needs {p.minimum}:1. The seed cannot reach it within its ramp; "
                    "choose a darker or more saturated seed."
                )

    return ColorResult(tokens=ts, notes=notes)
