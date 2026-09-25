---
id: type-along-the-scale
title: Weight and letter spacing change along the type scale
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# Weight and letter spacing change along the type scale

## Context

One heading weight and one tracking step for every size gives a 64px hero and a 24px heading the same weight and the hero the same tightness in every brand.

## Decision

The display weight (character.display_weight, 300 to 800 from contrast and formality) sets the hero and eases toward the text face's heading weight (500 to 700 from contrast) at heading-3, on a log scale of size, within what each face ships. Letter spacing is 0 at 20px and below and tightens toward the hero to character.display_tracking em (tighter for bold brands, more open for formal ones); labels open up by character.label_tracking em. Reading styles keep 0.

## Why

Large type needs less weight and tighter spacing to look even; small labels need more space. Driving both from the axes gives a formal system light, open display type and a playful one heavy, tight display type.

## What it touches

typography.weights, tracking_em and the tracking primitives; character.display_weight, heading_weight, display_tracking, label_tracking.

## Consequences

At standard contrast type.strong equals the heading weight (decisions/strong-under-high-contrast.md). The reading-tracking check still refuses negative spacing on reading styles.
