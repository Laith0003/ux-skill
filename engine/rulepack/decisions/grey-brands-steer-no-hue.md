---
id: grey-brands-steer-no-hue
title: A brand's hue counts in proportion to its chroma, so a grey brand steers no hue
status: active
areas: [color, imagery]
supersedes: null
superseded_by: null
---

# A brand's hue counts in proportion to its chroma, so a grey brand steers no hue

## Context

A grey brand has no stable hue: #808080 reads 0 degrees, #7F8080 197 and #80807F 106. When the brand hue steers a color at a fixed chroma, a black, grey or white brand gets a maroon scrim and a pink photo highlight, and three greys that look the same get cream, cyan or magenta neutrals and status hues up to 24 degrees apart.

## Decision

Wherever the brand hue steers a color, its pull is weighted by the brand's chroma: in proportion up to OKLCH chroma 0.04, and in full from there (character.hue_weight). That weight scales the brand's end of the neutral seed, the brand lean of each status hue, the brand-led hue of the supporting accent, the chroma of the scrim base and the brand's end of the duotone highlight. The duotone shadow already takes no more chroma than the brand has.

## Why

Below a chroma of about 0.04 a hue is barely visible and, near grey, only noise in the last bit of the hex. Scaling by chroma keeps every color continuous in the brand color, so two brands that look alike get systems that look alike, and a monochrome brand gets grey neutrals, a grey scrim and a grey highlight at the middle warmth. The warmth axis still tints them warm or cool, because that pull comes from the brief, not from the brand.

## What it touches

character.HUE_CHROMA, hue_weight, neutral_tint, status_seed and support_hue; color._neutral_seed and _primitives; imagery.scrim_base, SCRIM_C and duotone.

## Consequences

A muted brand such as a slate keeps most of its hue in the neutrals, status colors and supporting accent; a grey brand keeps none. A grey brand's accent hue is set by the warmth axis alone (decisions/grey-brand-support-hue.md), so #808080, #7F8080, #80807F and #807F80 get the same accent.
