"""Axis interaction matrix — explicit conflict resolution between competing axes.

The synthesizer's 7 axes can disagree about a single token. Without explicit
resolution, the FIRST axis a primitive consults wins implicitly. This module
documents and resolves the known conflicts so behaviour is predictable.

Each interaction returns a multiplier or override for a token category.

Documented conflicts:

1. **spacing**: density (push tight) vs formality (push spacious in luxury)
2. **radius**:  geometry (sharp ↔ soft) vs formality (corporate ↔ playful)
3. **accent**:  warmth × contrast — saturation register depends on both
4. **motion**:  motion (kinetic) vs formality (corporate — keep curve, dampen)

If you add a new conflict pair, add a function + register it below. Tests
guarantee each interaction is documented with a test case.
"""
from __future__ import annotations

from typing import Dict, Tuple

from engine.synthesizer.axes import AxisValues


def spacing_base_for(axes: AxisValues) -> int:
    """Pick spacing base px from density + formality conflict.

    - Dense + formal       (Bloomberg-school)     → 4 (density wins; both want fact-density)
    - Dense + casual                              → 4 (density wins outright)
    - Airy + formal        (luxury, hospitality)  → 12 (formality wins; breathing room)
    - Airy + casual        (consumer-lifestyle)   → 8
    - Balanced everywhere                         → 6
    """
    dense = axes.density > 0.65
    airy = axes.density < 0.4
    formal = axes.formality > 0.7
    if dense:
        return 4
    if airy and formal:
        return 12       # luxury / hospitality: formality overrides density toward more space
    if airy:
        return 8
    return 6


def radius_base_px_for(axes: AxisValues, vocab_mean: float = 0.5) -> int:
    """Pick base radius px from geometry × formality.

    geometry < 0.3 + formality > 0.7 → sharp (Bloomberg, NYT)
    geometry > 0.7 + formality < 0.3 → very soft (Glossier, Aesop)
    Otherwise weighted blend.

    The vocab_mean (from distilled brand exemplars) acts as a sanity floor.
    """
    g = axes.geometry
    f = axes.formality
    if g < 0.3 and f > 0.7:
        return 2        # sharp + corporate = essentially no radius
    if g > 0.7 and f < 0.4:
        return 18       # soft + playful = generous radius
    # Weighted blend: 50% axis target, 30% vocab mean, 20% formality dampener
    target = 0.5 * g + 0.3 * vocab_mean + 0.2 * (1.0 - f * 0.5)
    return max(2, int(round(target * 16)))


def accent_register_for(axes: AxisValues) -> Dict[str, float]:
    """Pick accent color register from warmth × contrast.

    Returns a dict with:
      - saturation_target (0.0–1.0)
      - lightness_target  (0.0–1.0)
      - warmth_register   (-1.0 cool ↔ 1.0 warm)
    """
    w = axes.warmth
    c = axes.contrast
    return {
        "saturation_target": min(1.0, 0.4 + 0.6 * c),
        "lightness_target": 0.55 - 0.10 * (c - 0.5),
        "warmth_register": (w - 0.5) * 2,
    }


def motion_timing_for(axes: AxisValues) -> Dict[str, int]:
    """Pick motion timings + dampen if formality high.

    High motion + high formality → keep curve, slower timing.
    High motion + low formality  → full snap (220→140ms range).
    """
    m = axes.motion
    f = axes.formality
    base_ms = int(220 - 80 * m)
    # Formality dampener: corporate brands slow motion even when axis is high
    if f > 0.7 and m > 0.5:
        base_ms = int(base_ms * 1.25)
    fast_ms = max(80, int(base_ms * 0.6))
    slow_ms = int(base_ms * 1.8)
    return {
        "base_ms": base_ms,
        "fast_ms": fast_ms,
        "slow_ms": slow_ms,
    }


# Public manifest — every documented interaction. Tests assert this list
# is closed (no silent additions).
DOCUMENTED_INTERACTIONS: Tuple[str, ...] = (
    "spacing_base_for",
    "radius_base_px_for",
    "accent_register_for",
    "motion_timing_for",
)
