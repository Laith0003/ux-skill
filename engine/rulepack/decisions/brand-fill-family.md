---
id: brand-fill-family
title: The primary fill keeps the exact brand whenever text reads on it, and otherwise the nearest brand step, weighing the ring in dark high contrast
status: active
areas: [color]
supersedes: brand-fidelity
superseded_by: null
---

# The primary fill keeps the exact brand whenever text reads on it, and otherwise the nearest brand step, weighing the ring in dark high contrast

## Context

Under high contrast the restaurant trial's orange became a pale peach with black text in both schemes: in light because black text on the nearest bright step counted as muddy, and in dark because the nearest passing step was the peach, where no focus ring could stand 3:1 off the fill (it measured 1.57:1).

## Decision

The primary fill's first candidate in every context is the exact brand color, and it stays whenever its text meets the minimum: white or black text in light, at standard and high contrast; in dark, white text, or black text on a fill at OKLCH lightness 0.72 or more, since black text on a mid tone reads muddy only on a dark page. Otherwise the fill moves to the nearest brand step whose text passes, in OKLab order from the brand color. In dark high contrast, where the 7:1 minimum moves the fill furthest, the order after the exact brand is OKLab distance plus 0.3 times the ring's shortfall: how far the best focus ring that clears every surface falls short of standing 3:1 off that step, 0 when it stands off and 1 at the most. So a step a ring can stand off wins over a slightly nearer one no ring can, and a far step never wins for the ring alone. Black text on a mid tone in dark comes last, as before. The system report states, per context, the fill, its text and whether it is the brand color; when the fill sits more than 0.12 from the brand in OKLab it says the button does not carry the brand's identity there.

## Why

Black text on a bright brand reads as the brand's own look on any light page, so light high contrast keeps a bright brand in its family (0.07 from the restaurant orange instead of 0.14). A ring that stands off the fill it surrounds is the ring's own rule, and in dark high contrast the nearest passing step was often a pale one no light ring could stand off. Over 107 brands at a fill role the weighed order doubles the dark high contrast fills a ring stands 3:1 off (35 to 71) and moves the mean distance from the brand from 0.062 to 0.070; standard contrast keeps its order, where the fill stays near the brand and the ring already stands off it in most cases. In dark the ring is light, so the step it favors is a deeper one, and the ramp's dark steps keep most of the brand's chroma; in light high contrast the ring is dark and would favor a paler step, which bleeds chroma faster (a vivid blue would turn periwinkle), so light keeps the nearest step. The exact brand is never passed over for the ring.

## What it touches

color._muddy, _solve_group (its order under high contrast), MUDDY_L, RING_ON_FILL, RING_WEIGHT and IDENTITY_DISTANCE; brand_fidelity and the Brand color section of system-report.md; guidance/color.md.

## Consequences

A bright brand in light high contrast keeps a near brand step with black text. In dark high contrast a brand that cannot keep its color takes a deeper step of its hue with white text and a light ring, rather than a pale step the ring cannot stand off. Hover and pressed steps still step away from the fill from where it sits (decisions/exact-fill-states.md).
