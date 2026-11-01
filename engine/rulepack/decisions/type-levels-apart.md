---
id: type-levels-apart
title: Neighbouring type levels stay at least 1.08 times apart after rounding
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# Neighbouring type levels stay at least 1.08 times apart after rounding

## Context

The scale ratio runs from 1.095 for a muted, dense system to 1.355 for a bold one. Sizes are whole pixels, and rounding at the muted, dense corner set heading-3 at 18px and heading-2 at 19px, 1.056 times apart. The type-hierarchy check asked only for falling sizes, so it passed a pair a reader cannot tell apart. The Arabic sizes, the Latin size times the faces' ratio, rounded the same way.

## Decision

Every size from body up, in the Latin and the Arabic scale, is at least 1.08 times the size below it after rounding: the generator raises a size by whole pixels until it clears. The type-hierarchy check holds hero, heading-1, section-title, heading-2, heading-3 and body to the same floor, in both directions, and names the style to move up the scale. 1.08 is our floor, not a WCAG number.

## Why

A heading reads as a new level only when its size differs at a glance. The generated ratio never falls below 1.095, so the floor moves a size only where rounding pulled two steps together; a larger floor such as 1.125 would push every muted system off its own ratio.

## What it touches

typography.MIN_LEVEL_RATIO, latin_px, arabic_px and the type-hierarchy check; guidance/type.md.

## Consequences

At the muted, dense corner one size rises by a pixel. An imported or edited set with two levels closer than 1.08 fails the gate with the style to move.
