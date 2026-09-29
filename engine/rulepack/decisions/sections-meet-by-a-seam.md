---
id: sections-meet-by-a-seam
title: How sections meet comes from depth and contrast, and a formal, calm brand joins them with a hairline
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# How sections meet comes from depth and contrast, and a formal, calm brand joins them with a hairline

## Context

With no default for how sections meet, every page cut from one section to the next the same way. Popular generated pages let hero media reach into the next section and fade between tones; measured award pages cut hard about half the time, more often the louder they are; a calm, formal page often separates sections by space and a single line.

## Decision

layout.seam.overlap is character.seam_overlap_px, 128px times depth, on the spacing scale: how far hero media reaches into the next section. layout.seam.fade is character.seam_fade_px, 192px times depth times one minus contrast: how long a tonal seam runs, 0 for a bold brand, which cuts hard. layout.seam.line is character.seam_line mapped to 0, 1 or 2px: a formal (0.6 and up) and calm (energy under 0.35) brand draws a hairline where sections meet, heavier with formality, the calm end of the same seam. A flat brand gets hard edges.

## Why

Depth says how much a surface floats, so it sets how far media floats past its section; contrast says how hard edges are. A hairline is how a formal page separates sections without color.

## What it touches

character.SEAM_OVERLAP_PX, SEAM_FADE_PX, seam_overlap_px, seam_fade_px, seam_line; layout.ON_SPACE_ONE and the layout.seam roles; guidance/layout.md.

## Consequences

A brand's own recorded rhythm still wins over these defaults.
