---
id: support-clear-of-banned-pairs
title: A cool brand's supporting accent leans to its own hue, and the gradient stays in one hue
status: active
areas: [color, imagery]
supersedes: support-accent
superseded_by: null
---

# A cool brand's supporting accent leans to its own hue, and the gradient stays in one hue

## Context

The supporting accent sat 30 to 180 degrees from the brand hue by the contrast axis, pulled warm or cool. For a blue brand that landed on pink, magenta or purple, and gradient.svg ran from the brand to that accent: blue to pink, the pairing anti-slop bans. Every real landing page dropped the art for it.

## Decision

The supporting accent's seed sits at OKLCH lightness 0.6. Its brand-led hue sits 30 degrees from the brand for a muted brief up to 180 for a bold one, pulled warm or cool with warmth. That hue then moves in a straight line in the OKLab a/b plane toward the brand's own hue at 0.35 of the supporting chroma, as far as the brand is cool (character.coolness, in full from 2/3 up) and its hue reads (hue_weight). So a blue, violet or cyan brand gets an analogous, quiet accent of its own hue, and a warm brand keeps its complementary accent. The result counts by hue_weight against the grey brand's accent (decisions/grey-accent-clear-of-status.md). The chroma is 0.9 of the brand's, between 0.06 and 0.16, times the share the lean keeps. art/gradient.svg runs from the page through the brand tint to the brand, in one hue, and never to the supporting accent.

## Why

Anti-slop bans blue to pink or purple and a cool brand with a pink beside it, and allows a gradient inside a narrow hue window. A lean that is continuous in the brand color keeps near brands near each other, and a straight line in the a/b plane runs close to grey between far hues instead of through purple. Measured over hues every degree, chroma 0.04 to 0.24 and every corner of warmth and contrast, no brand gets a banned pairing.

## What it touches

character.SUPPORT_QUIET, QUIET_COOLNESS, coolness, support_seed and support_hue; color._primitives (the support family); art.art_files (the gradient's stops) and report_lines; guidance/color.md.

## Consequences

Blue and violet brands get a quiet accent in their own hue; tags and art in color.text.support and color.decorative.support read as the brand, softer. The supporting accent is still never an action or status color.
