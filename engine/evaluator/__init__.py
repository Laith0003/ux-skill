"""Evaluation engine — deterministic 7-axis scoring of synthesized output.

Every UI output gets scored 0-100 on 7 dimensions. **All deterministic. No LLM.**

The 7 axes:

1. **linter_score** — existing 0-100 anti-pattern linter score
2. **hierarchy_clarity** — H1/H2/H3 distribution + size ratios
3. **layout_coherence** — primitives used consistently, no fixed-px overflow
4. **spacing_consistency** — adherence to the spacing scale
5. **usability_readability** — contrast ratios, line-length, font-size mins
6. **tone_match** — cosine distance from synthesized axes vs brief-intended axes
7. **uniqueness** — distance from prior decisions (hash-based novelty)

Composite score is the mean of the 7 axes. Below 65 trips the quality gate.

Public surface
--------------
``evaluate(html, css, synth_system, brief, axes) -> Evaluation``
``Evaluation``                    — dataclass with the 7 axis scores
``THRESHOLD``                     — 65, the minimum auto-accept score
``AXES``                          — list of the 7 axis names
"""
from engine.evaluator.core import (
    evaluate,
    Evaluation,
    THRESHOLD,
    AXES,
    score_hierarchy,
    score_layout_coherence,
    score_spacing,
    score_readability,
    score_tone_match,
    score_uniqueness,
)

__all__ = [
    "evaluate",
    "Evaluation",
    "THRESHOLD",
    "AXES",
    "score_hierarchy",
    "score_layout_coherence",
    "score_spacing",
    "score_readability",
    "score_tone_match",
    "score_uniqueness",
]
