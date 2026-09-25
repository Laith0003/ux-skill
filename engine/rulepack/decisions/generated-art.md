---
id: generated-art
title: Every build draws decorative brand art from the axes
status: active
areas: [imagery, output]
supersedes: null
superseded_by: null
---

# Every build draws decorative brand art from the axes

## Context

A page with no photos yet is a page of flat surfaces, and stock art picked by hand drifts from the system's character.

## Decision

Every build writes art/pattern.svg, art/shapes.svg and art/gradient.svg. Shapes are squares whose corners round toward circles as roundness grows; warmth weighs the palette toward the brand and support accents over the neutral; formality sets how many shapes there are, how small, and how regularly they sit (formal art is a dense grid, playful art a few large shapes scattered and turned). Positions come from a generator seeded by a digest of the brand and the axes, so the same inputs draw the same art. Colors are CSS custom properties with the light values as fallbacks. Each file is aria-hidden with no title, and the report says to place it with an empty alt.

## Why

Art drawn from the same numbers as the rest of the system belongs to it, and a deterministic seed keeps builds reproducible. Decoration marked as decoration never reaches a screen reader as noise.

## What it touches

engine/foundations/art.py; emit.ART_FILES and the report's Brand art section; guidance/imagery.md.

## Consequences

A build writes seven files. Art is replaceable: a page with real photos drops it.
