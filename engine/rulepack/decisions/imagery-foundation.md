---
id: imagery-foundation
title: Imagery is a foundation of ratios, a measured scrim, a duotone and a tint
status: active
areas: [imagery, radius]
supersedes: null
superseded_by: null
---

# Imagery is a foundation of ratios, a measured scrim, a duotone and a tint

## Context

The site trials had no images at all: nothing in the system said how to crop a photo, how to keep text on it readable, or how to bring mixed photos into the brand.

## Decision

A ninth foundation, imagery, holds the media ratios (hero from the contrast, density and formality axes; card from geometry and formality; portrait 4:5), a scrim whose alpha is the least that lets its text reach 4.5:1 over the worst image for that text and 7:1 under high contrast (decisions/scrim-worst-image.md), a duotone pair in the brand hue with a highlight pulled warm or cool, and a brand tint whose strength grows with warmth. radius.media gives media its corner. The scrim-text check measures the scrim over a white and a black image in every context and counts the lower ratio; the duotone pair holds our 7:1 floor.

## Why

Measuring the scrim over the worst image makes text on photos safe for any photo, which a ratio against one sample cannot promise. A treatment derived from the brand keeps photos from different sources looking like one set.

## What it touches

engine/foundations/imagery.py; build.FOUNDATIONS; modes.FOUNDATION_AXES; radius.media; guidance/imagery.md with the art direction.

## Consequences

Photos themselves stay the owner's choice; the rule pack gives the art direction in our words. The report's opening names nine foundations.
