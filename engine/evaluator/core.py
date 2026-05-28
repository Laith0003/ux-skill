"""Evaluation engine — 7 deterministic axis scores.

Every score is a heuristic over the rendered output. No LLM. No external
service. Same input always gives the same score.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple


THRESHOLD = 65          # minimum auto-accept composite score
AXES: Tuple[str, ...] = (
    "linter_score",
    "hierarchy_clarity",
    "layout_coherence",
    "spacing_consistency",
    "usability_readability",
    "tone_match",
    "uniqueness",
)


@dataclass
class Evaluation:
    """7-axis evaluation result."""
    composite: int = 0
    linter_score: int = 0
    hierarchy_clarity: int = 0
    layout_coherence: int = 0
    spacing_consistency: int = 0
    usability_readability: int = 0
    tone_match: int = 0
    uniqueness: int = 0
    above_threshold: bool = False
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Per-axis scorers (each returns 0-100)
# ---------------------------------------------------------------------------

_H_TAG_RE = re.compile(r"<(h[1-6])\b", re.IGNORECASE)


def score_hierarchy(html: str) -> int:
    """Hierarchy clarity: H1 present, monotonic h-tag use, h-tag spread."""
    if not html:
        return 50
    tags = [t.lower() for t in _H_TAG_RE.findall(html)]
    if not tags:
        return 40  # no headings = low hierarchy
    has_h1 = any(t == "h1" for t in tags)
    has_h2 = any(t == "h2" for t in tags)
    # Penalize multiple H1s (should be exactly one per page)
    h1_count = tags.count("h1")
    score = 100
    if not has_h1:
        score -= 25
    if h1_count > 1:
        score -= 10 * (h1_count - 1)
    if not has_h2 and len(tags) > 1:
        score -= 10
    # Penalize skip from h1 → h3 without h2
    levels_seen = [int(t[1]) for t in tags]
    for prev, cur in zip(levels_seen, levels_seen[1:]):
        if cur - prev > 1:
            score -= 8
    return max(0, min(100, score))


def score_layout_coherence(html: str, css: str) -> int:
    """Layout coherence: primitive class use consistent, no fixed-px overflow risk."""
    score = 100
    notes = []
    # Penalize bare width: NNNpx over 1000 (likely overflow risk on mobile)
    big_widths = re.findall(r"width\s*:\s*([1-9]\d{3,})px", css or "")
    if big_widths:
        score -= min(40, 8 * len(big_widths))
    # Penalize !important spam (>5 = chaos)
    bangs = (css or "").count("!important")
    if bangs > 10:
        score -= min(20, bangs - 10)
    # Bonus for using ux-* primitive classes consistently
    if "ux-grid" in (html or "") or "ux-stack" in (html or ""):
        score += 0  # no bonus needed; just no penalty
    # Penalty for inline styles (chaos)
    inline_styles = len(re.findall(r"style\s*=\s*[\"']", html or ""))
    if inline_styles > 10:
        score -= min(20, inline_styles - 10)
    return max(0, min(100, score))


def score_spacing(css: str, spacing_scale: Optional[List[int]] = None) -> int:
    """Spacing consistency: rhythm values use the scale, not random magic numbers."""
    if not css:
        return 70
    # Find all px spacing values (margin, padding, gap)
    values = re.findall(r"(?:margin|padding|gap|inset)[^;:]*:\s*([^;]+);", css)
    scale = set(spacing_scale or [4, 8, 12, 16, 24, 32, 48, 64, 96])
    # Add common rems converted to px (1rem=16px)
    scale = {*scale, *(s for s in (8, 16, 24, 32, 48))}
    px_values: List[int] = []
    for v in values:
        for m in re.finditer(r"(\d+(?:\.\d+)?)px", v):
            px_values.append(int(float(m.group(1))))
    if not px_values:
        return 80
    on_scale = sum(1 for v in px_values if v in scale or v == 0)
    pct = on_scale / len(px_values)
    return max(0, min(100, int(round(40 + 60 * pct))))


def score_readability(css: str) -> int:
    """Usability/readability: font-size mins, line-length, contrast hints."""
    if not css:
        return 70
    score = 100
    # Penalize tiny font sizes (< 13px on body)
    small_fonts = re.findall(r"font-size\s*:\s*(\d{1,2})px", css)
    for s in small_fonts:
        sz = int(s)
        if sz < 12:
            score -= 8
        elif sz < 14:
            score -= 2
    # Penalize ultra-thin weights on body
    if re.search(r"body[^{]*\{[^}]*font-weight\s*:\s*[12]00", css):
        score -= 12
    # Penalize line-length absent max-width on body
    if re.search(r"\.body|\.prose", css) and "max-width" not in css:
        score -= 6
    return max(0, min(100, score))


def score_tone_match(synth_axes: Dict[str, float],
                     brief_axes: Dict[str, float]) -> int:
    """Tone match: cosine-like distance between synthesized axes and brief axes.

    Lower distance = higher score. Distance of 0 (identical) = 100.
    Distance of 1.0 (max in 7-D) = 0.
    """
    if not synth_axes or not brief_axes:
        return 70
    keys = set(synth_axes) & set(brief_axes)
    if not keys:
        return 70
    sq = sum((float(synth_axes[k]) - float(brief_axes[k])) ** 2 for k in keys)
    # Max distance for 7-D unit cube = sqrt(7) ≈ 2.646. Normalize to 0..1.
    max_dist = (len(keys)) ** 0.5
    dist = (sq ** 0.5) / max_dist if max_dist > 0 else 0
    return max(0, min(100, int(round(100 * (1 - dist)))))


def score_uniqueness(synth_axes: Dict[str, float],
                     palette: Optional[Dict[str, str]] = None,
                     prior_decisions: Optional[List[Dict[str, Any]]] = None) -> int:
    """Uniqueness: how different is this output from recent prior decisions.

    Distance = mean of pairwise differences in axes + palette hash distance.
    No prior decisions → default 80 (novel because nothing to compare).
    """
    if not prior_decisions:
        return 80
    # Compute axis distance against each prior decision; pick MIN (closest)
    min_axis_dist = 1.0
    for prior in prior_decisions:
        p_axes = prior.get("axes")
        if not isinstance(p_axes, dict):
            continue
        keys = set(synth_axes) & set(p_axes)
        if not keys:
            continue
        sq = sum((float(synth_axes.get(k, 0.5)) - float(p_axes.get(k, 0.5))) ** 2
                 for k in keys)
        d = (sq ** 0.5) / (len(keys) ** 0.5)
        if d < min_axis_dist:
            min_axis_dist = d
    # min_axis_dist near 0 = near-duplicate. We want score HIGH for unique.
    # Closer to 1 = more unique.
    return max(0, min(100, int(round(40 + 60 * min_axis_dist))))


# ---------------------------------------------------------------------------
# Composite
# ---------------------------------------------------------------------------

def evaluate(html: str = "", css: str = "",
             synth_system: Optional[Any] = None,
             brief_axes: Optional[Dict[str, float]] = None,
             linter_score: int = 100,
             spacing_scale: Optional[List[int]] = None,
             prior_decisions: Optional[List[Dict[str, Any]]] = None,
             ) -> Evaluation:
    """Run all 7 axis scorers, return an Evaluation."""
    synth_axes = {}
    palette = None
    if synth_system is not None:
        if hasattr(synth_system, "axes"):
            synth_axes = synth_system.axes
        elif isinstance(synth_system, dict):
            synth_axes = synth_system.get("axes", {})
        if hasattr(synth_system, "palette"):
            palette = synth_system.palette
        elif isinstance(synth_system, dict):
            palette = synth_system.get("palette")

    h_score = score_hierarchy(html)
    lc_score = score_layout_coherence(html, css)
    sp_score = score_spacing(css, spacing_scale)
    rd_score = score_readability(css)
    tm_score = score_tone_match(synth_axes, brief_axes or {})
    un_score = score_uniqueness(synth_axes, palette, prior_decisions)

    # Composite is the mean of the 7 axes
    composite = int(round(
        (linter_score + h_score + lc_score + sp_score + rd_score + tm_score + un_score) / 7
    ))

    notes: List[str] = []
    if linter_score < 70:
        notes.append("linter score low — multiple AI-slop fingerprints found")
    if h_score < 60:
        notes.append("hierarchy unclear — fix heading levels")
    if lc_score < 60:
        notes.append("layout coherence low — too many fixed-px widths or inline styles")
    if sp_score < 60:
        notes.append("spacing inconsistent — values off the scale")
    if rd_score < 60:
        notes.append("readability low — fix font-size mins or line-length")
    if tm_score < 60:
        notes.append("tone mismatch — output doesn't match the brief's axes")

    return Evaluation(
        composite=composite,
        linter_score=linter_score,
        hierarchy_clarity=h_score,
        layout_coherence=lc_score,
        spacing_consistency=sp_score,
        usability_readability=rd_score,
        tone_match=tm_score,
        uniqueness=un_score,
        above_threshold=composite >= THRESHOLD,
        notes=notes,
    )
