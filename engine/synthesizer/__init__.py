"""Synthesizer — fresh design language synthesis from brief + brand exemplars.

The v2.1 intelligence layer. **Offline. Deterministic. No LLM.**

Three modes (dispatched automatically based on the Brief):

1. **strict_brand**  — Brief names one brand with strict=True. Output IS that
   brand's token set verbatim. Used for "make me a Stripe clone" speed paths.
   Fastest (no synthesis math, just emit the spec).

2. **brand_anchor** — Brief names brand(s) WITHOUT strict flag. ~70% weighted
   to the named brand(s), 30% adapted to the brief's axis values. Used for
   "Stripe-like but for healthcare" — looks Stripe-flavored, adapts to your
   domain. Fast.

3. **pure_synthesis** — Brief names no brand. Infinity space. 7-axis derivation
   from the brief → vocabulary distillation from N exemplars matching each
   axis → weighted-average synthesis → fresh tokens. Output is novel each call.

7 axes (all continuous 0.0–1.0):
- warmth          (cold ↔ warm)
- contrast        (flat ↔ dramatic)
- density         (airy ↔ dense)
- geometry        (sharp ↔ soft)
- formality       (playful ↔ corporate)
- motion          (still ↔ kinetic)
- type_personality (geometric ↔ humanist)

Public surface
--------------
``synthesize(brief: Brief) -> SynthesizedSystem``    main entry
``compute_axes(brief: Brief) -> AxisValues``         axis derivation
``distill_vocabulary(brands) -> Vocabulary``         vocabulary distillation
``MODES``                                            the 3 mode names
"""
from engine.synthesizer.core import (
    synthesize,
    SynthesizedSystem,
    SYNTHESIS_MODES,
)
from engine.synthesizer.axes import (
    compute_axes,
    AxisValues,
    AXIS_NAMES,
)
from engine.synthesizer.vocabulary import (
    distill_vocabulary,
    Vocabulary,
    pick_exemplars_by_axes,
)

__all__ = [
    "synthesize",
    "SynthesizedSystem",
    "SYNTHESIS_MODES",
    "compute_axes",
    "AxisValues",
    "AXIS_NAMES",
    "distill_vocabulary",
    "Vocabulary",
    "pick_exemplars_by_axes",
]
