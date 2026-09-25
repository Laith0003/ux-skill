---
id: status-harmony
title: Status colors lean toward the brand and the warmth axis, inside a fixed band
status: active
areas: [color]
supersedes: status-hues
superseded_by: null
---

# Status colors lean toward the brand and the warmth axis, inside a fixed band

## Context

A status palette at fixed hues and a fixed chroma reads the same on every brand: a loud sky blue info tint on a calm clinic, a saturated green beside a muted brand. Fixed hues keep danger red; a free hue would let a red brand pull warning into orange.

## Decision

Each status family keeps its own hue (danger 25, warning 75, success 150, info 245, in OKLCH degrees) and leans a quarter of the way toward the brand hue and a fifth of the way toward a warm or a cool hue with the warmth axis, never more than 12 degrees from its own hue. Its chroma follows the contrast axis, from 0.07 for a muted brand to 0.18 for a bold one; its lightness stays at 0.58. The soft, text and strong steps come from that ramp as before.

## Why

A 12 degree band keeps each status in its own color name, so danger never reads as orange and info never as purple, while the palette shares the brand's temperature. Chroma from the contrast axis makes a calm system's status tints calm without a second table. Status never relies on hue alone: every status carries an icon and words, and the contracts refuse a status color without a second cue.

## What it touches

character.status_seed, character.STATUS_HUES and STATUS_BAND; color._primitives; the status-banner contract.

## Consequences

Two brands with different hues get status palettes that differ by a few degrees. A brand close to a status hue should not use its brand fill for anything that could read as that status; the owner decides, and the generator does not move the status past its band.
