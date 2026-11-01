---
id: faces-cost-their-ubiquity
title: Each display face carries a ubiquity cost, so no face wins more than a set share of the axis space
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# Each display face carries a ubiquity cost, so no face wins more than a set share of the axis space

## Context

Picked by distance alone, one display face won a fifth of all axis vectors and another nearly as much, so generated pages leaned on the same faces while others almost never appeared.

## Decision

Each display face in fonts.FACES carries ubiquity, a cost added to fonts.distance. The values were set on fonts.UBIQUITY_SAMPLE (warmth, contrast, geometry, formality and type personality each at 0, 1/8 and so on to 1, density and motion at 0.5) so no display face wins more than fonts.UBIQUITY_CAP, 0.16, and each wins at least UBIQUITY_FLOOR, 0.06. It is a property of the face, never of the brief; text and mono faces carry none.

## Why

A face that already appears everywhere reads generic; a cost on the face spreads the choice without a ban and without looking at any brief.

## What it touches

fonts.Face.ubiquity, UBIQUITY_SAMPLE, UBIQUITY_CAP, UBIQUITY_FLOOR, distance; guidance/type.md.

## Consequences

A test recounts the shares on the sample, so a new face or a moved place resets the costs.
