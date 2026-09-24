---
id: dark-elevation-cue
title: In dark mode, surfaces lighten as they rise
status: active
areas: [color, elevation]
supersedes: null
superseded_by: null
---

# In dark mode, surfaces lighten as they rise

## Context

Shadows read poorly on dark backgrounds. A dark theme that keeps every surface the same color and relies on shadows for depth looks flat.

## Decision

In the dark scheme the surface roles step lighter as they rise: page is the darkest working surface, card is lighter and raised is lighter still, in standard and high contrast. Sunken is darker than the page at standard contrast; under high contrast both are black. Dark shadows are stronger than light ones. The lightness step, not the shadow, is the primary depth cue in dark.

## Why

Lightness is visible where a shadow is not. Putting the cue in color keeps it measurable, and the elevation checks keep the shadows as a second, weaker signal that still grows with each level.

## What it touches

color.SEMANTIC dark values for the surfaces; the elevation-dark and visible-shadow checks.

## Consequences

A dark theme that flattens its surfaces to one color loses depth even with shadows. Under dark high contrast the surfaces move toward black and the edges required by container-edge carry the separation.
