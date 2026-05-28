"""Evolve — auto-iterating lint→polish→re-lint refinement loop.

Takes a synthesized artifact, runs the linter + evaluator, attempts an
automatic polish pass, re-evaluates. Repeats until:

- Score crosses 90 (great), OR
- Score plateaus (delta < 5 between rounds), OR
- 5 rounds elapsed (safety cap).

If final score < 65 (quality gate), output is REFUSED with a force-regenerate
recommendation unless caller passes ``force=True``.

**Offline. Deterministic. No LLM.** Polish is heuristic-driven — strip
inline styles, replace generic CTAs, swap placeholder URLs, normalize
spacing to the scale.
"""
from engine.evolve.core import (
    evolve,
    EvolveResult,
    EvolveRound,
    MAX_ROUNDS,
    PLATEAU_DELTA,
    TARGET_SCORE,
    QUALITY_GATE,
)

__all__ = [
    "evolve",
    "EvolveResult",
    "EvolveRound",
    "MAX_ROUNDS",
    "PLATEAU_DELTA",
    "TARGET_SCORE",
    "QUALITY_GATE",
]
