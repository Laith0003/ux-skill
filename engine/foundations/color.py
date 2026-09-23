"""Color foundation: primitives from OKLCH ramps, semantic roles per mode,
the WCAG pairings every system must meet, and a deterministic retune."""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Dict, List, Tuple

from engine.foundations.color_math import contrast, hex_to_oklch, oklch_to_hex
from engine.foundations.gate import GateFailure, GateFinding, Pairing, gate
from engine.foundations.ramp import STEPS, ramp
from engine.foundations.tokens import Token, TokenSet, alias_target, is_alias
from engine.synthesizer.axes import AxisValues

STATUS_HUES = {"danger": 25.0, "warning": 75.0, "success": 150.0, "info": 245.0}
STATUS_SEED = (0.58, 0.16)  # OKLCH lightness, chroma for status seeds


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
    + [Pairing("color.action.primary-hover", "color.surface.page", 3.0, "1.4.11")]
    + [Pairing("color.focus.ring", bg, 3.0, "2.4.7") for bg in _TEXT_BGS]
)

# The three roles a single joint solver owns in generate_color (R17): the
# button fill, its hover step, and the text that sits on both. Every
# pairing above whose foreground is one of these is still enforced (the
# final re-check below walks all of PAIRINGS), but none of them is retuned
# by the ordinary one-pairing-at-a-time loop; see _solve_action_group.
_ACTION_GROUP_ROLES = frozenset(
    {"color.text.on-action", "color.action.primary", "color.action.primary-hover"})


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


def _solve_action_group(mode: str, prims: Dict[str, str], pick: Dict[str, Dict[str, str]],
                         notes: List[str]) -> None:
    """R17: choose action.primary, action.primary-hover and text.on-action
    together for one mode, instead of retuning each pairing in isolation.

    A prior version resolved text.on-action jointly against both
    backgrounds (R16), then nudged hover off primary when they collided
    (R16 item 3). That nudge had no notion of hover's own 3:1 requirement
    against the page (PAIRINGS had no such entry), so it could satisfy
    on-action while dropping hover below 3:1 against a light or dark page,
    an invisible button on hover. Solving all three together, against all
    four constraints at once, is the only way to guarantee a candidate
    that is never picked unless it already clears everything.

    Search order (deterministic, matches the R17 ruling exactly):
      1. action.primary at distance 0, then 1, then 2, ... ramp steps from
         its SEMANTIC default; at equal distance, the conventional
         direction (darker in light mode, lighter in dark mode) before the
         opposite one.
      2. For each primary candidate, action.primary-hover at primary + 1
         step conventional, then primary - 1 step (the opposite), then +2,
         then -2.
      3. For each (primary, hover) pair, text.on-action as base.white
         (the default for both modes), then base.black.
    The first candidate that clears every constraint below wins:
      contrast(on_action, primary)  >= 4.5   (1.4.3, text.on-action)
      contrast(on_action, hover)    >= 4.5   (1.4.3, text.on-action)
      contrast(primary, page)       >= 3.0   (1.4.11, action.primary)
      contrast(hover, page)         >= 3.0   (1.4.11, action.primary-hover)
      hover's hex != primary's hex             (a hover state must be visible)
    """
    primary_role = "color.action.primary"
    hover_role = "color.action.primary-hover"
    on_action_role = "color.text.on-action"

    default_primary_path = pick[mode][primary_role]
    default_hover_path = pick[mode][hover_role]
    default_onaction_path = pick[mode][on_action_role]
    page_hex = prims[pick[mode]["color.surface.page"]]

    family, default_step = default_primary_path.rsplit(".", 1)
    default_idx = STEPS.index(int(default_step))
    conv = +1 if mode == "light" else -1

    def path_at(idx: int) -> str:
        return f"{family}.{STEPS[idx]}"

    primary_indices = [default_idx]
    for d in range(1, len(STEPS)):
        for delta in (conv * d, -conv * d):
            idx = default_idx + delta
            if 0 <= idx < len(STEPS) and idx not in primary_indices:
                primary_indices.append(idx)

    best = None  # (score, ratios) for the exhaustion error, if it comes to that

    for primary_idx in primary_indices:
        primary_hex = prims[path_at(primary_idx)]
        r_pp = contrast(primary_hex, page_hex)

        hover_indices = []
        for hd in (conv * 1, -conv * 1, conv * 2, -conv * 2):
            hidx = primary_idx + hd
            if 0 <= hidx < len(STEPS) and hidx != primary_idx and hidx not in hover_indices:
                hover_indices.append(hidx)

        for hover_idx in hover_indices:
            hover_hex = prims[path_at(hover_idx)]
            if hover_hex == primary_hex:
                continue
            r_hp = contrast(hover_hex, page_hex)

            for on_action_path in ("color.base.white", "color.base.black"):
                on_action_hex = prims[on_action_path]
                r_op = contrast(on_action_hex, primary_hex)
                r_oh = contrast(on_action_hex, hover_hex)

                score = min(r_op / 4.5, r_oh / 4.5, r_pp / 3.0, r_hp / 3.0)
                if best is None or score > best[0]:
                    best = (score, (r_op, r_oh, r_pp, r_hp))

                if r_op >= 4.5 and r_oh >= 4.5 and r_pp >= 3.0 and r_hp >= 3.0:
                    chosen_primary = path_at(primary_idx)
                    chosen_hover = path_at(hover_idx)
                    if (chosen_primary, chosen_hover, on_action_path) != (
                            default_primary_path, default_hover_path, default_onaction_path):
                        notes.append(
                            f"action group ({mode}): "
                            f"{primary_role} {default_primary_path} -> {chosen_primary}, "
                            f"{hover_role} {default_hover_path} -> {chosen_hover}, "
                            f"{on_action_role} {default_onaction_path} -> {on_action_path}, "
                            f"on-action/primary {r_op:.2f}:1, on-action/hover {r_oh:.2f}:1, "
                            f"primary/page {r_pp:.2f}:1, hover/page {r_hp:.2f}:1"
                        )
                    pick[mode][primary_role] = chosen_primary
                    pick[mode][hover_role] = chosen_hover
                    pick[mode][on_action_role] = on_action_path
                    return

    if best is None:
        # Every hover candidate tried resolved to the exact same hex as its
        # primary candidate (e.g. a ramp flattened to one color end to
        # end), so the hover != primary requirement alone ruled out every
        # combination before any ratio was even worth scoring.
        raise ValueError(
            f"action group ({mode}): every ramp step this seed's brand family reaches "
            f"resolves to the same color as {primary_role}, so {hover_role} can never "
            "read as a different color from it. Choose a brand seed whose ramp actually "
            "varies from step to step."
        )

    r_op, r_oh, r_pp, r_hp = best[1]
    raise ValueError(
        f"action group ({mode}): no combination of {primary_role}, {hover_role} and "
        f"{on_action_role} within the brand ramp clears every requirement; the closest "
        f"reached on-action/primary {r_op:.2f}:1, on-action/hover {r_oh:.2f}:1 (both need "
        f"4.5:1), primary/page {r_pp:.2f}:1, hover/page {r_hp:.2f}:1 (both need 3.0:1). "
        "Choose a brand seed with more contrast range in its ramp."
    )


def _with_seed_hint(ts: TokenSet, finding: GateFinding) -> GateFinding:
    """Add the seed direction to a finding whose pairing the brand seed
    controls (either side aliases a brand step in that mode). A darker brand
    only ever helps a light-mode pairing gain contrast against a light
    page, and only a lighter brand helps the dark-mode equivalent (R17
    minor), so the hint never suggests the direction that makes it worse.
    Pairings the seed does not control keep the gate's own fix."""
    for path in (finding.fg, finding.bg):
        raw = ts.raw(path, finding.mode)
        if is_alias(raw) and alias_target(raw).startswith("color.brand."):
            direction = "a darker" if finding.mode == "light" else "a lighter"
            return replace(finding, hint=(
                "The brand seed cannot reach it within its ramp; "
                f"choose {direction} or more saturated seed."))
    return finding


def generate_color(axes: AxisValues, brand_hex: str) -> ColorResult:
    """Low-level call: build_color wraps it with input checks, validate and
    the gate report, so prefer build_color unless you need the raw generator.

    Returns the color TokenSet and the retune notes. Raises GateFailure when
    the generated system fails a pairing in PAIRINGS, and ValueError when
    the action group cannot be solved within the brand ramp.
    """
    notes: List[str] = []
    prims = _primitives(axes, brand_hex.upper(), notes)
    pick = {mode: {role: pair[i] for role, pair in SEMANTIC.items()}
            for i, mode in enumerate(("light", "dark"))}

    def value(mode: str, role: str) -> str:
        return prims[pick[mode][role]]

    # R17: action.primary, action.primary-hover and text.on-action are
    # resolved together by _solve_action_group, not by the one-pairing-
    # at-a-time loop below. A prior version (R16) retuned text.on-action
    # jointly against both backgrounds and then nudged hover away from
    # primary on collision, but neither step had any notion of hover's own
    # 3:1-vs-page requirement (PAIRINGS had no such entry), so the nudge
    # could satisfy on-action while quietly dropping the hover fill below
    # 3:1 against the page, an invisible button on hover that nothing
    # caught. Solving all three roles against all four constraints at once
    # is the only way to guarantee a result that is never picked unless it
    # already clears everything; see _solve_action_group's own docstring
    # for the exact search order.
    generic_pairings = [p for p in PAIRINGS if p.fg not in _ACTION_GROUP_ROLES]

    for mode in ("light", "dark"):
        max_passes = len(generic_pairings) * len(STEPS) + 1
        for _pass in range(max_passes):
            changed = False

            # Every ordinary pairing moves its own foreground, independent
            # of the others, away from its background's lightness. None of
            # these ever targets action.primary, action.primary-hover or
            # text.on-action (see _ACTION_GROUP_ROLES above); those are the
            # solver's alone, run once below, after this has converged.
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

            if not changed:
                break

        # The solver runs last, once per mode: nothing in the ordinary loop
        # above ever reads action.primary, action.primary-hover or
        # text.on-action (no other pairing's bg is one of them), so there
        # is no order dependency to resolve by repeating it.
        _solve_action_group(mode, prims, pick, notes)

    ts = TokenSet()
    for path, hx in prims.items():
        ts.add(Token(path, "color", hx))
    for role in SEMANTIC:
        light, dark = pick["light"][role], pick["dark"][role]
        ts.add(Token(role, "color", "{" + light + "}", layer="semantic",
                     modes={"dark": "{" + dark + "}"} if dark != light else {}))

    # R16 item 1 (CRITICAL): every move above is bounded by the ramp's own
    # ends, so any of them can legitimately do nothing (the "if not nxt"
    # guard above, and _solve_action_group's own exhaustion raise) and
    # leave a pairing still failing, for example when a seed's ramp
    # genuinely has no step that clears a threshold. Re-verify every
    # pairing, in both modes, against the result actually being returned,
    # through the same gate build_color uses (R27 I3), and fail loudly with
    # GateFailure rather than let a design system that violates its own
    # WCAG gate ship silently.
    report = gate(ts, PAIRINGS, raise_on_fail=False)
    if not report.passed:
        report.findings[:] = [_with_seed_hint(ts, f) for f in report.findings]
        raise GateFailure(report)

    # R17 item (c): action.primary-hover must never resolve to the exact
    # same color as action.primary. _solve_action_group already refuses
    # any candidate where the two hexes match, so this should be
    # unreachable; it stays as the same kind of fail-loud backstop as the
    # pairing check above, in case a future change to the solver reopens
    # the gap R16 item 3 first found.
    for mode in ts.mode_names:
        primary_hex = ts.resolve("color.action.primary", mode)
        hover_hex = ts.resolve("color.action.primary-hover", mode)
        if primary_hex == hover_hex:
            raise ValueError(
                f"color.action.primary-hover equals color.action.primary ({mode}) at "
                f"{primary_hex}; the hover state must read as a different color from "
                "the resting state."
            )

    return ColorResult(tokens=ts, notes=notes)
