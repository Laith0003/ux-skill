---
id: neutrals-follow-the-brand
title: The neutrals take their temperature from the brand first, and warmth only leans them
status: active
areas: [color, imagery]
supersedes: warmth-through-grey
superseded_by: null
---

# The neutrals take their temperature from the brand first, and warmth only leans them

## Context

The neutral seed travelled from the brand hue all the way to a warm or a cool anchor at chroma 0.030 as warmth went to 1 or 0, so the brief's warmth overrode the brand's own temperature. A grey brand in a warm industry got sand greys, and a blue brand with a friendly tone got beige greys next to a cool blue.

## Decision

The neutral seed is the sum of two vectors in the OKLab a/b plane. The brand's own hue at chroma 0.008, weighted by the brand's chroma (decisions/grey-brands-steer-no-hue.md), sets the temperature. Warmth adds a lean toward the warm hue (70 degrees) or the cool hue (250 degrees) of up to 0.010 chroma at warmth 0 or 1, in proportion to the warmth's distance from 0.5, and a brand with a hue holds back half of it (character.LEAN_C, BRAND_HOLD). A grey brand gets true grey at the middle warmth and a trace of warm or cool toward the ends; a saturated brand keeps its own temperature and the lean only moves it a little. The duotone highlight moves from the brand hue at chroma 0.04 toward the anchor at chroma 0.07, up to 60 percent of the way, in a straight line through grey.

## Why

Neutrals carry most of a screen, so their temperature is part of the identity. Leaning instead of replacing keeps the brief's warmth visible without setting warm greys against a cool brand. The lean is zero where the anchor switches, so the seed is continuous in the axes and in the brand color.

## What it touches

character.neutral_tint, NEUTRAL_C, LEAN_C and BRAND_HOLD; color._neutral_seed; imagery.duotone and HIGHLIGHT_C; every role on the neutral ramp.

## Consequences

Neutrals move less with warmth, most for a saturated brand. The warmth axis still moves the neutral tint, the status hues and the imagery; the character test's least move for the neutral b is lowered to match.
