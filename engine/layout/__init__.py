"""Layout synthesizer — responsive-by-construction layout composition.

Given a Brief + axis values, picks a section sequence and emits a layout
spec that is GUARANTEED responsive across 360/768/1024/1440 px breakpoints.

The guarantee comes from two layers of defense:

1. **Construction**: every primitive (grid, stack, cluster, frame) uses
   modern CSS that's responsive-by-construction:
     - CSS Grid with ``auto-fit minmax(min(N, 100%), 1fr)``
     - Container queries instead of media queries
     - Intrinsic sizing (``min-width: 0``, ``flex: 1 1 auto``)
     - No fixed widths over 100% of viewport
   This means broken layouts CAN'T be emitted in the first place.

2. **Validation**: optional ``validate()`` runs a headless Playwright check
   at 360/768/1024/1440 px and refuses any output with overflow, clipping,
   or hidden content. Heavy dep, opt-in via ``uxskill validate --playwright``.

Public surface
--------------
``synthesize_layout(brief, axes) -> LayoutSpec``     — section sequence + tokens
``LayoutSpec``                                       — dataclass with sections
``validate(html, breakpoints=DEFAULT_BREAKPOINTS)``  — Playwright validator (opt-in)
``PRIMITIVES``                                       — registry of layout primitives
``DEFAULT_BREAKPOINTS``                              — (360, 768, 1024, 1440)
"""
from engine.layout.core import (
    synthesize_layout,
    LayoutSpec,
    Section,
    PRIMITIVES,
    DEFAULT_BREAKPOINTS,
)

__all__ = [
    "synthesize_layout",
    "LayoutSpec",
    "Section",
    "PRIMITIVES",
    "DEFAULT_BREAKPOINTS",
]
