---
id: ring-never-weaker
title: The focus ring never weakens under high contrast, and is measured against the fill
status: active
areas: [color, border]
supersedes: null
superseded_by: null
---

# The focus ring never weakens under high contrast, and is measured against the fill

## Context

The ring is chosen per context. Chosen alone, the high contrast ring can measure less against a surface than the standard ring does, and next to the primary fill a ring close to the fill's color reads as part of the button.

## Decision

Under high contrast the ring must measure at least what the standard ring of the same scheme measures against each surface it is paired with (the ring-not-weaker check). In every context the solver prefers a ring that stands 3:1 off the primary fill, then one that differs from it; where no ring can clear the surfaces and the fill at once, the ring keeps at least 2px of page color between itself and the fill (the ring-on-fill check). The border foundation widens the ring under high contrast.

## Why

High contrast exists for people who need more, so no part of it may give less. WCAG 1.4.11 measures the ring against the colors next to it, which the offset makes the page; measuring it against the fill as well keeps it from blending into the button for people who see the two together.

## What it touches

color._ring_floor, _choose_ring, RING_ON_FILL; the ring-not-weaker and ring-on-fill checks; border.focus-ring.offset and width.

## Consequences

The ring can move away from the brand ramp to a neutral or black and white step under high contrast. The report lists the ring against the fill in every context.
