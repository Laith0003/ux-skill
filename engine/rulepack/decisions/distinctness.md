---
id: distinctness
title: Opposite characters build measurably different systems
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# Opposite characters build measurably different systems

## Context

Four site trial briefs of very different character built systems a person could not tell apart: the same body size, corners, neutrals, status colors and face, with only the hue changed.

## Decision

engine/foundations/distinct.py reads the features a person sees at a glance from a built system (the button's color, the page tint, corners, faces, sizes, the display weight and tracking, shadow, the ring, motion, spacing and the hero ratio) and measures two systems apart as the mean scaled difference, 0 to 1. Our floors: every pair of opposite corners of the seven axes, with one brand, is at least 0.35 apart; moving any one axis from 0 to 1 moves the system at least 0.05; the four site trial briefs are at least 0.15 apart pairwise, with their own brands and with one shared brand, and choose four different display faces. character.INFLUENCE names which axes must move which foundations, and a test moves each.

## Why

A floor on a measured distance stops a later change from quietly collapsing the systems back together, which a review of one build cannot see.

## What it touches

engine/foundations/distinct.py and character.INFLUENCE; tests/foundations/test_distinct.py, test_character.py and the trial briefs in tests/foundations/briefs/.

## Consequences

A change that makes two characters converge fails the suite and names the pair. Raising a floor is a decision; lowering one needs a record.
