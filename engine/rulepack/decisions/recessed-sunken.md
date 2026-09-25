---
id: recessed-sunken
title: A sunken surface sits a small step below the page
status: superseded
areas: [color]
supersedes: null
superseded_by: dark-recess-and-bands
---

# A sunken surface sits a small step below the page

## Context

A well, a hovered row or a disabled field needs a surface below the page. One full ramp step below the page reads as a heavy grey slab in light, which people take for disabled, and pure black in dark reads as a hole in the page.

## Decision

color.surface.sunken is its own neutral primitive per scheme, 0.035 OKLCH lightness below the page's step: color.neutral.recess-light in light and color.neutral.recess-dark in dark. Under high contrast it keeps color.neutral.recess-light in light, so a well stays visible on a white page, and is black in dark.

## Why

A small step reads as recessed and keeps text on it at the page's contrast. The primitive is derived from the page's own step, so it follows the neutral tint the warmth axis sets.

## What it touches

color._primitives (the recess primitives), SEMANTIC and HIGH_CONTRAST for color.surface.sunken; every text pairing on the sunken surface.

## Consequences

A sunken area needs its edge or its content to show where it ends; the step alone is quiet by design. Disabled fields may still use the sunken surface, and they carry their disabled text and edge as well.
