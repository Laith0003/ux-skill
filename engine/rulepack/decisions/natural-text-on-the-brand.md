---
id: natural-text-on-the-brand
title: The primary fill weighs black text on a saturated mid tone against a move to a step that carries white
status: superseded
areas: [color]
supersedes: brand-fill-family
superseded_by: natural-fill-for-white-text
---

# The primary fill weighs black text on a saturated mid tone against a move to a step that carries white

## Context

The primary fill kept the exact brand whenever white or black text met the minimum. A saturated mid blue such as #2279EE carries white text at 4.17:1 and black at 5.04:1, so it kept the exact hex with black text, which reads muddy on a saturated mid tone; the client's own app uses white on that blue. Every text style is held to 4.5:1 (decisions/no-large-text-relaxation.md), so white could not stay on the exact hex.

## Decision

The primary fill's first candidate in every context is the exact brand color, and the brand band is solved the same way. Each fill and text that passes is weighed by a cost: the fill's OKLab distance from the brand (plus 0.3 times the ring's shortfall after the exact brand in dark high contrast) plus what the text costs in naturalness. White text costs nothing. Black text costs character.black_text_cost: up to 0.12, the identity distance, on a fill of OKLCH chroma 0.12 or more at lightness 0.60 or darker, nothing on a grey fill or one at lightness 0.72 or lighter, in proportion between. The lowest cost wins, the search order breaking ties. So white text on the nearest brand step that carries it beats black text on the exact brand whenever that step is nearer than black costs, which is never beyond the identity distance. In dark, black text on a fill darker than 0.72 is taken only when nothing else passes. The build notes the move, the system report says why in the Brand color section, and the gate's on-color-natural check, our rule, finds black text on a primary fill where a brand step nearer to the brand than the fill plus that cost carries white text on it and on the two steps its states take.

## Why

On a bright color black text reads as the color's own look; on a saturated mid tone it reads dirty, and a step a little darker with white text reads as the brand. Weighing both in one continuous cost keeps each choice explainable, changes it gradually as a brand gets lighter or greyer, and caps the move at the distance past which the button would stop reading as the brand. The rest of the brand-fill-family rule is kept: light high contrast keeps a bright brand in its family, and dark high contrast weighs the ring.

## What it touches

character.BLACK_TEXT_COST, NATURAL_L and black_text_cost; color.natural_cost, _solve_group (the weighed choice), _on_color_natural and CHECKS, brand_fidelity; RING_WEIGHT, MUDDY_L and IDENTITY_DISTANCE; guidance/color.md.

## Consequences

A saturated mid-tone brand takes a step just darker with white text on the button and the brand band; #E85D04 keeps black on the exact orange, where black costs 0.07 and the nearest white step is 0.10 away. Hover and pressed still step away from the fill from where it sits (decisions/exact-fill-states.md).
