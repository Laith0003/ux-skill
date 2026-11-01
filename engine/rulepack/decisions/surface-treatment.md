---
id: surface-treatment
title: The surface treatment runs from flat hairlines to deep shadows
status: active
areas: [elevation, color]
supersedes: null
superseded_by: null
---

# The surface treatment runs from flat hairlines to deep shadows

## Context

One shadow strength for every brand makes a quiet formal product and a bold playful one read the same, and a sunken surface with no cue but its color reads as a disabled block.

## Decision

character.depth is contrast plus 0.3 times (0.5 minus formality), clamped to 0 to 1. The key shadow's alpha runs from 0.03 (flat) to 0.17 (deep) at level 1 and its blur from 0.7 to 1.3 times the base; color.line.subtle is neutral 300, 200 or 100 in light (600 or 700 in dark) as the treatment deepens, so a flat system carries its shapes with hairlines and a deep one with shadows. elevation.inset gives a sunken surface an inner shadow at the same depth.

## Why

Flat, soft and deep are the three surface treatments designers name; driving them from one continuous number keeps shadows, edges and wells in step.

## What it touches

character.depth; elevation.key_alpha, softness, inset and elevation.inset; color._subtle_steps.

## Consequences

The elevation checks still hold every level above the one below and every shadow visible in both schemes.
