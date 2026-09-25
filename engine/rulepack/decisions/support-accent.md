---
id: support-accent
title: A supporting accent takes a second hue placed by the axes
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# A supporting accent takes a second hue placed by the axes

## Context

A single hue gives generated art, tags and highlights nothing to set against the brand, and a second hue picked by hand drifts from the brand's character.

## Decision

The support ramp's seed sits at OKLCH lightness 0.6 and the brand's chroma (0.06 to 0.16), at a hue 30 degrees from the brand for a muted brand up to 180 degrees for a bold one, pulled toward warm or cool with the warmth axis. That hue counts by the brand's chroma (decisions/grey-brands-steer-no-hue.md), and a grey brand's accent takes its hue from warmth alone, clear of every status hue (decisions/grey-accent-clear-of-status.md). It feeds color.text.support, color.decorative.support and the generated art.

## Why

Analogous hues suit quiet systems and near complements suit loud ones; placing the hue by the contrast axis gives each its own without a palette table.

## What it touches

character.support_hue; color._primitives (the support family); the support roles.

## Consequences

The supporting accent is never an action or status color. A brief that wants no second hue simply leaves those roles unused.
