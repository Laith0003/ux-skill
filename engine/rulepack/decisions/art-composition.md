---
id: art-composition
title: Generated art is a composition of three layers, placed by the axes and never at random
status: active
areas: [imagery, output]
supersedes: generated-art
superseded_by: null
---

# Generated art is a composition of three layers, placed by the axes and never at random

## Context

The first generated art kept each cell of a grid by a coin flip seeded from the inputs. A playful hero could be empty or one shape cropped by the canvas, a formal tile read as scattered noise, and a middle brief drew a pile of overlapping rounded squares. Two briefs a little apart drew unrelated art, and the gradient's bare id could meet an id on the page.

## Decision

Every build still writes art/pattern.svg, art/shapes.svg and art/gradient.svg, and every quantity is a continuous function of the axes; the two counts (accents per side, cells per tile side) are the nearest whole number to one. Nothing is random.

The hero is three layers, back to front: a neutral plane, the brand's focal shape and a group of support accents. The drawn area is about a quarter of the canvas, a little more when playful, and weights() splits it: 60, 30 and 10 percent for the neutral, the brand and the support at warmth 0.5, with warmth moving area from the neutral to the two accents. The neutral is drawn at 0.55 opacity, so it recedes. The focal shape sits on the right, whole, inside the right 9:16 of the canvas that a phone crop keeps (xMaxYMid slice); the left third stays open for a heading. When formal, the plane's upper corner meets the focal shape's center and the accents are an even 3 by 3 grid a gap below it, their outer edge in line with its edge; as formality falls the corner runs past the center, the accents become one capsule that overlaps the focal shape, and everything turns. Turns and offsets are zero over the formal part of the axis and grow slowly below it, so none is small enough to read as a mistake. Geometry rounds every layer, the plane least and the accents most, so the layers keep their own silhouettes.

The tile is a lattice of 2, 4 or 6 cells per side with one shape per cell at an even pitch, a large and small checker rhythm, a half drop on odd rows as formality falls, and colors dealt so each takes its weight of the cells. A shape that crosses an edge is drawn again on the far side, and the tile is 240px, so it repeats without seams. Contrast turns the gradient from left to right toward top to bottom. The gradient's id carries a digest of the brand and the axes (uxs-art-<digest>-wash); the other files have no id.

## Why

A composition reads as designed when it has one focal shape, open space on purpose, alignment it keeps or leaves on purpose, and a palette in proportion. Placing each layer against the others, instead of drawing it at random, makes every brief look composed, keeps the focal shape in every crop, and lets two close briefs draw close art. A digest in the id keeps an inlined gradient working next to any page's own ids and next to another build's art.

## What it touches

engine/foundations/art.py (weights, play, hero, tile, digest, report_lines); emit.ART_FILES, now art.FILES, and the report's Brand art section; guidance/imagery.md.

## Consequences

A build writes seven files, as before. Under right to left the hero is mirrored with transform: scaleX(-1); it has no text. A page with real photos drops the art.
