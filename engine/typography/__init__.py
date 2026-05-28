"""Typography computation — size ladder + weight curve from axes.

Given axis values, derive a complete type scale (caption→display) using a
modular ratio. The 70-entry type-pairs manifest acts as the EXEMPLAR pool
for which font families to use, but the actual size ladder + weight curve
is COMPUTED per brief, not picked from a fixed table.

Three derived outputs:

1. **Size ladder** — 9-step scale from caption to display.
   Ratio derived from axes:
     - contrast high  → 1.333 (perfect fourth) — bigger ratio = louder
     - contrast mid   → 1.250 (major third) — balanced
     - contrast low   → 1.200 (minor third) — quieter

2. **Weight curve** — display, h1, h2, h3, body, caption weights.
   Bias from axes.type_personality:
     - geometric (low)  → display 800, body 400, mono 500
     - humanist (high)  → display 600, body 400, mono 400

3. **Tracking (letter-spacing) curve** — derived from axes.formality + size.
   Display tighter; body neutral; caption wider.

Public surface
--------------
``compute_type_scale(axes) -> TypeScale``     — full ladder + weights + tracking
``TypeScale``                                 — dataclass
``modular_ratio_for(axes)``                   — picks the type ratio
"""
from engine.typography.core import (
    compute_type_scale,
    TypeScale,
    modular_ratio_for,
    SIZE_NAMES,
    WEIGHT_NAMES,
)

__all__ = [
    "compute_type_scale",
    "TypeScale",
    "modular_ratio_for",
    "SIZE_NAMES",
    "WEIGHT_NAMES",
]
