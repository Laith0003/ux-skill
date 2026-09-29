---
id: landing-rhythm-follows-the-brand
title: A landing page spaces its sections by how calm and formal the brand is, and a phone keeps most of the gap
status: active
areas: [layout, space]
supersedes: landing-gap
superseded_by: null
---

# A landing page spaces its sections by how calm and formal the brand is, and a phone keeps most of the gap

## Context

The landing gap came from density alone, 128 to 192px at desktop and 64 to 80px on a phone. On 35 measured award pages the gap between sections fell as the brand grew louder (about 233, 162 and 68px at expressiveness 0.2, 0.5 and 0.9) and the bands of empty space grew with formality, and phone gaps barely shrank (the phone gap was 1.04 times the desktop one at the median, about 100px).

## Decision

character.calm_space is 0.6 times one minus energy plus 0.4 times formality. character.landing_gap_px is 64px times 3.75 to the power of calm_space: 64 to 240px at desktop. The phone takes character.phone_gap_share of it, 0.6 for a loud brief to 0.9 for a calm one, and the tablet and laptop sit a third and two thirds of the way from the phone to the desktop. Each tier snaps to the spacing scale, which gains space.56 and space.60, never below the region gap at its tier and never shrinking as the viewport grows; compact takes one step less, never below the region gap's compact step. The layout-regions check is unchanged.

## Why

Loud pages separate sections with color and hard cuts and pack them tight; calm and formal ones separate them with space. A phone that shrinks the gap to a third reads cramped next to its own desktop page.

## What it touches

character.calm_space, LANDING_GAP_PX, PHONE_GAP_SHARE, landing_gap_px, phone_gap_share; layout.LANDING_STEPS, landing_gap_units; space.UNITS; guidance/layout.md.

## Consequences

Density moves the region gap, not the landing gap. A page reads var(--layout-landing-gap) between its sections; the report names the desktop and phone gap.
