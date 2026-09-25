---
id: brand-fidelity
title: The primary fill keeps the exact brand color whenever text reads on it
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# The primary fill keeps the exact brand color whenever text reads on it

## Context

A fill that moves a ramp step whenever white text falls short costs a bright brand its own color, even when black text reads on it. In dark mode a mid tone with black text reads muddy, and under high contrast the 7:1 text minimum can move the fill far enough to read as another color.

## Decision

The primary fill's first candidate in every context is the exact brand color. In light at standard contrast it stays whenever white or black text meets 4.5:1 on it. In dark and under high contrast it stays whenever white text meets the minimum, or black text does on a fill at OKLCH lightness 0.72 or more; otherwise the fill moves to the brand step nearest the brand color in OKLab that meets the minimum under the same rule, and takes black text on a darker step only when no step passes without it. The system report states, per context, the fill, its text and whether it is the brand color; when the fill sits more than 0.15 from the brand in OKLab it says the brand's identity is not carried by the button there.

## Why

The brand is what people recognize; a button one step off it reads as a near miss. Black text on a bright fill looks intentional, black text on a mid tone in the dark looks dirty. Ordering candidates by distance from the brand keeps as much of it as the text minimum allows, and naming an identity loss lets the owner carry the brand elsewhere, in the logo or an accent.

## What it touches

color.EXACT (the color.brand.exact primitive), _fill_candidates, _muddy, MUDDY_L and IDENTITY_DISTANCE; brand_fidelity and the Brand color section of system-report.md.

## Consequences

A brand that needs black text keeps black text in light. Hover and pressed steps move away from the text color, so a black text brand gets lighter hover and pressed steps. Under high contrast many brands move; the report names the move and the distance.
