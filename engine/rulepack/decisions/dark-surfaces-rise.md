---
id: dark-surfaces-rise
title: In dark mode, surfaces lighten as they rise, and a well sits between the page and the card
status: active
areas: [color, elevation]
supersedes: dark-elevation-cue
superseded_by: null
---

# In dark mode, surfaces lighten as they rise, and a well sits between the page and the card

## Context

Shadows read poorly on dark backgrounds. A dark theme that keeps every surface the same color and relies on shadows for depth looks flat. A sunken surface below a dark page reads as a hole: in the site trials a table header on it was a black strip across the card.

## Decision

In the dark scheme the surface roles step lighter as they rise: page is the darkest working surface, card is lighter and raised is lighter still, in standard and high contrast. The sunken surface sits between the page and the card, at standard and high contrast. Dark shadows are stronger than light ones. The lightness step, not the shadow, is the primary depth cue in dark. The surface order the rule pack writes for dark reads page, sunken, card, raised.

## Why

Lightness is visible where a shadow is not. Putting the cue in color keeps it measurable, and the elevation checks keep the shadows as a second, weaker signal that still grows with each level. In dark the page is the floor; a well is cut into the card it sits on, so it only needs to sit below that card.

## What it touches

color.SEMANTIC and HIGH_CONTRAST dark values for the surfaces; the elevation-dark and visible-shadow checks; rulepack.generate DARK_LEVELS.

## Consequences

A dark theme that flattens its surfaces to one color loses depth even with shadows. Under dark high contrast the page is black and the edges required by container-edge carry the separation of the card and raised surfaces.
