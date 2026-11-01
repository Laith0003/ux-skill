---
id: spacing-on-the-4px-grid
title: Every numbered spacing step is a whole multiple of 4px
status: active
areas: [space]
supersedes: null
superseded_by: null
---

# Every numbered spacing step is a whole multiple of 4px

## Context

The generator builds every space step on a 4px base, but nothing held an imported set to it, so a 10px or 14px step could enter the scale and every role that points at it would fall off the grid.

## Decision

The space-grid check reads every numbered space step in px and fails any that is not a whole multiple of space.BASE_UNIT, 4px. The failure names the step, its value and the two grid values either side of it. The 4px grid is our choice; no standard sets it.

## Why

A shared grid keeps spacing in proportion across components: two gaps that differ always differ by at least one unit, and sums of steps land back on the grid.

## What it touches

space.BASE_UNIT and the space-grid check; guidance/space.md.

## Consequences

A set with space.3 at 10px fails with "round it to 8px or 12px". The check reads primitives only, so it runs once, not per density.
