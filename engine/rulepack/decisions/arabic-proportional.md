---
id: arabic-proportional
title: Arabic is set larger by a ratio the two faces' metrics give
status: active
areas: [direction]
supersedes: null
superseded_by: null
---

# Arabic is set larger by a ratio the two faces' metrics give

## Context

A fixed 1 to 2px step makes Arabic larger at body size and meaningless at display sizes, where a 64px Latin heading beside a 66px Arabic one reads smaller.

## Decision

Under right to left each style's Arabic size is its Latin size times fonts.arabic_scale: one plus half the gap between the Latin face's x-height and the Arabic face's letter body, both per em, within 1.05 to 1.15, and at least 1px larger. The arabic-text check holds every Arabic size between 1px and a fifth above its Latin size.

## Why

The Arabic letter body and the Latin x-height are what the eye compares; a ratio keeps the two scripts matched at every size, and measuring it from the faces keeps it right when the faces change.

## What it touches

fonts.arabic_scale and ARABIC_SCALE; typography.arabic_px and the arabic-text check.

## Consequences

Arabic headings grow with the scale. Layouts reserve the extra height at display sizes.
