---
id: neutrals-lean-along-the-brand
title: The neutrals take their temperature from the brand, and warmth leans them along the brand's own hue
status: active
areas: [color, imagery]
supersedes: neutrals-follow-the-brand
superseded_by: null
---

# The neutrals take their temperature from the brand, and warmth leans them along the brand's own hue

## Context

The brand's whisper plus a warmth lean toward a warm or cool anchor kept a blue brand's greys cool under a warm brief, but for a warm brand under a cool brief the sum of two vectors turned through red and magenta: an orange brand at warmth 0 got a faint rose grey, the direction the owner objected to.

## Decision

The neutral seed is the brand's own hue at chroma 0.008, weighted by the brand's chroma (decisions/grey-brands-steer-no-hue.md), plus a warmth lean of up to 0.010 chroma toward the warm hue (70 degrees) or the cool hue (250 degrees), in proportion to the warmth's distance from 0.5 (character.LEAN_C). For a brand with a hue the lean is its projection on the brand's own hue axis, at half its size (BRAND_HOLD), so warmth deepens or thins the whisper toward grey and never turns it; hue_weight blends the free lean of a grey brand into the projected one. The duotone highlight moves from the brand hue at chroma 0.04 toward the anchor at chroma 0.07, up to 60 percent of the way, in a straight line through grey.

## Why

Neutrals carry most of a screen, so their temperature is part of the identity. A lean along the brand's own axis keeps the brief's warmth visible as more or less of the brand's tint, and it cannot pass through a third hue.

## What it touches

character.neutral_tint, NEUTRAL_C, LEAN_C and BRAND_HOLD; color._neutral_seed; imagery.duotone and HIGHLIGHT_C; every role on the neutral ramp.

## Consequences

A saturated brand's neutrals keep its hue at every warmth, thinner or fuller. A grey brand's neutrals lean sand or slate. The character test reads the neutrals' warmth on a grey brand.
