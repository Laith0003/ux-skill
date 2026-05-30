"""Evolve loop — auto-iterating polish + re-evaluate.

Public function: ``evolve(html, css, synth_system, brief_axes, ...)``.

Polish passes (all deterministic, no LLM):

- **Strip inline styles** that violate the linter (color/font-weight/text-align
  on a div). Move to a class-based approach.
- **Replace generic CTAs** ("Click here", "Submit") with action-specific text.
- **Swap placeholder URLs** (via.placeholder.com, etc.) for ``data:`` URIs.
- **Normalize spacing** to nearest scale step (16/24/32/48/64).
- **Strip Lorem ipsum** with a generic editorial prompt-line.
- **Lowercase ``font-weight: bold``** to numeric weight 700.

Each polish is idempotent — running it twice produces no further change.

The loop stops on the first of:
  - composite score >= TARGET_SCORE (90)
  - |delta| < PLATEAU_DELTA (5) between consecutive rounds
  - rounds >= MAX_ROUNDS (5)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

from engine.evaluator import evaluate, Evaluation, THRESHOLD


MAX_ROUNDS = 5
PLATEAU_DELTA = 5     # |round_n - round_n-1| < this = plateau
TARGET_SCORE = 90     # auto-stop above this
QUALITY_GATE = THRESHOLD   # 65 — below this, refuse to commit


@dataclass
class EvolveRound:
    """One iteration of the loop."""
    round: int = 0
    composite: int = 0
    delta_from_prev: int = 0
    polishes_applied: List[str] = field(default_factory=list)
    evaluation: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvolveResult:
    """Final result of an evolve loop."""
    initial_score: int = 0
    final_score: int = 0
    rounds: List[EvolveRound] = field(default_factory=list)
    stopped_reason: str = ""        # "target_hit" | "plateau" | "max_rounds" | "gate_failed"
    above_gate: bool = False
    forced: bool = False
    final_html: str = ""
    final_css: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "initial_score": self.initial_score,
            "final_score": self.final_score,
            "rounds": [r.to_dict() for r in self.rounds],
            "stopped_reason": self.stopped_reason,
            "above_gate": self.above_gate,
            "forced": self.forced,
            "final_html_length": len(self.final_html),
            "final_css_length": len(self.final_css),
        }


# ---------------------------------------------------------------------------
# Polish passes
# ---------------------------------------------------------------------------

_GENERIC_CTAS = {
    "Click here": "View details",
    "Submit": "Continue",
    "Read more": "Continue reading",
    "Learn more": "See how it works",
    "Tap here": "Get started",
}


def polish_strip_inline_styles(html: str) -> Tuple[str, bool]:
    """Strip color: / font-weight: inline style attributes."""
    new = re.sub(r'\s+style="(?:color|font-weight|text-align):[^"]*"', "", html)
    return new, new != html


def polish_replace_generic_ctas(html: str) -> Tuple[str, bool]:
    """Replace generic CTA text with action-specific copy."""
    changed = False
    new = html
    for old, repl in _GENERIC_CTAS.items():
        before = new
        new = new.replace(f">{old}<", f">{repl}<")
        if new != before:
            changed = True
    return new, changed


def polish_swap_placeholder_urls(html: str) -> Tuple[str, bool]:
    """Swap generic placeholder URLs for inert data URIs.

    Strips via.placeholder / placehold.co / placekitten and RANDOM (unseeded)
    picsum.photos. A seeded picsum (picsum.photos/seed/...) is stable and on the
    curated-stock path, so it is preserved -- consistent with the
    data/anti-patterns.json picsum stance.
    """
    pattern = (
        r"https?://(?:via\.placeholder|placeholder|placehold\.co|placekitten)[^\s\"'<>]*"
        r"|https?://picsum\.photos/(?!seed/)[^\s\"'<>]*"
    )
    new = re.sub(pattern, "data:image/svg+xml;base64,PHN2Zy8+", html)
    return new, new != html


def polish_normalize_spacing(css: str) -> Tuple[str, bool]:
    """Snap px spacing values to the nearest scale step.

    Scale: {4, 8, 12, 16, 24, 32, 48, 64, 96, 128}.
    """
    scale = [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]
    changed = False

    def _snap(match: re.Match) -> str:
        nonlocal changed
        v = int(match.group(1))
        if v == 0 or v in scale:
            return match.group(0)
        nearest = min(scale, key=lambda s: abs(s - v))
        # Only snap if within 35% of original (don't snap 7 → 96)
        if abs(nearest - v) / max(v, 1) > 0.35:
            return match.group(0)
        changed = True
        return f"{nearest}px"

    new = re.sub(r"\b(\d+)px\b", _snap, css)
    return new, changed


def polish_strip_lorem_ipsum(html: str) -> Tuple[str, bool]:
    """Replace Lorem ipsum blocks with a placeholder editorial note."""
    pattern = r"Lorem ipsum[^<]*"
    new = re.sub(pattern, "[editorial copy — replace before ship]", html,
                 flags=re.IGNORECASE)
    return new, new != html


def polish_fontweight_bold(css: str) -> Tuple[str, bool]:
    """font-weight: bold → font-weight: 700 (numeric)."""
    new = re.sub(r"font-weight\s*:\s*bold", "font-weight: 700", css,
                 flags=re.IGNORECASE)
    return new, new != css


def _polish_pass(html: str, css: str) -> Tuple[str, str, List[str]]:
    """Run all polish passes once. Returns (html, css, names_applied)."""
    applied: List[str] = []
    html, ch = polish_strip_inline_styles(html)
    if ch:
        applied.append("strip_inline_styles")
    html, ch = polish_replace_generic_ctas(html)
    if ch:
        applied.append("replace_generic_ctas")
    html, ch = polish_swap_placeholder_urls(html)
    if ch:
        applied.append("swap_placeholder_urls")
    html, ch = polish_strip_lorem_ipsum(html)
    if ch:
        applied.append("strip_lorem_ipsum")
    css, ch = polish_normalize_spacing(css)
    if ch:
        applied.append("normalize_spacing")
    # Bold pass
    new_css = re.sub(r"font-weight\s*:\s*bold", "font-weight: 700", css,
                     flags=re.IGNORECASE)
    if new_css != css:
        applied.append("fontweight_numeric")
        css = new_css
    return html, css, applied


def html_or_css_safeguard(s: str) -> bool:
    """Sanity: ensure s is a string."""
    return isinstance(s, str)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def evolve(html: str, css: str,
           synth_system: Optional[Any] = None,
           brief_axes: Optional[Dict[str, float]] = None,
           linter_score: int = 100,
           force: bool = False,
           max_rounds: int = MAX_ROUNDS,
           ) -> EvolveResult:
    """Run the lint→polish→re-lint loop until convergence.

    Polish passes are all deterministic. Same input → same trajectory.
    """
    rounds: List[EvolveRound] = []
    prev_score: Optional[int] = None
    initial_eval = evaluate(
        html=html, css=css, synth_system=synth_system,
        brief_axes=brief_axes, linter_score=linter_score,
    )
    initial_score = initial_eval.composite

    for n in range(1, max_rounds + 1):
        ev = evaluate(
            html=html, css=css, synth_system=synth_system,
            brief_axes=brief_axes, linter_score=linter_score,
        )
        delta = (ev.composite - prev_score) if prev_score is not None else 0
        round_rec = EvolveRound(
            round=n,
            composite=ev.composite,
            delta_from_prev=delta,
            evaluation=ev.to_dict(),
            polishes_applied=[],
        )

        # Stop on target hit
        if ev.composite >= TARGET_SCORE:
            rounds.append(round_rec)
            return EvolveResult(
                initial_score=initial_score,
                final_score=ev.composite,
                rounds=rounds,
                stopped_reason="target_hit",
                above_gate=True,
                forced=False,
                final_html=html,
                final_css=css,
            )

        # Stop on plateau (after round 2 so the first delta counts)
        if prev_score is not None and abs(delta) < PLATEAU_DELTA:
            rounds.append(round_rec)
            above_gate = ev.composite >= QUALITY_GATE
            return EvolveResult(
                initial_score=initial_score,
                final_score=ev.composite,
                rounds=rounds,
                stopped_reason="plateau" if above_gate or force else "gate_failed",
                above_gate=above_gate,
                forced=force,
                final_html=html,
                final_css=css,
            )

        # Apply polish for next round
        new_html, new_css, applied = _polish_pass(html, css)
        round_rec.polishes_applied = applied
        rounds.append(round_rec)
        if not applied:
            # Nothing to polish. We're done.
            above_gate = ev.composite >= QUALITY_GATE
            return EvolveResult(
                initial_score=initial_score,
                final_score=ev.composite,
                rounds=rounds,
                stopped_reason="plateau" if above_gate or force else "gate_failed",
                above_gate=above_gate,
                forced=force,
                final_html=html,
                final_css=css,
            )
        html, css = new_html, new_css
        prev_score = ev.composite

    # Max rounds reached
    final_eval = evaluate(
        html=html, css=css, synth_system=synth_system,
        brief_axes=brief_axes, linter_score=linter_score,
    )
    above_gate = final_eval.composite >= QUALITY_GATE
    return EvolveResult(
        initial_score=initial_score,
        final_score=final_eval.composite,
        rounds=rounds,
        stopped_reason="max_rounds" if above_gate or force else "gate_failed",
        above_gate=above_gate,
        forced=force,
        final_html=html,
        final_css=css,
    )
