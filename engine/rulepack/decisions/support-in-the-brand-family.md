---
id: support-in-the-brand-family
title: A cool brand's supporting accent moves with the axes inside its own family, and never forms a banned pairing
status: active
areas: [color, imagery]
supersedes: support-clear-of-banned-pairs
superseded_by: null
---

# A cool brand's supporting accent moves with the axes inside its own family, and never forms a banned pairing

## Context

Leaning a cool brand's accent all the way to its own hue at a fixed share of chroma kept it clear of the pairings anti-slop bans, but it gave every cool brand one support color whatever the axes: two blue clients got the same slate. With the button fixed by the brand, the accent is one of the few colors left to show character. The banned pairings were defined only in a test.

## Decision

character.banned_pair holds the rule as hue arcs, each from its start up to its end: blue 215 to 285 degrees, purple 285 to 330, pink 330 to 20. A blue brand with a purple or pink accent, a purple brand with a blue one, and a cool brand (coolness 0.75 and up) with a pink one are banned. A warm brand keeps its brand-led accent: 30 degrees from the brand for a muted brief up to 180 for a bold one, pulled warm or cool with warmth. A cool brand's accent moves in a straight line in the OKLab a/b plane to its family hue, as far as the brand is cool (in full from coolness 2/3) and its hue reads: the brand hue moved up to 30 degrees toward higher hues as warmth rises and lower as it falls, held closer by formality (character.family_hue), at 0.35 of the supporting chroma for a muted brief up to 0.80 for a bold one. Whatever results is slid out of any banned pairing with the brand to the edge of the arc it sits in, back toward the brand hue (clear_of_banned). The chroma is 0.9 of the brand's, between 0.06 and 0.16, times the share and times hue_weight (decisions/grey-support-is-neutral.md). art/gradient.svg runs from the page through the brand tint to the brand, in one hue, and never to the supporting accent.

## Why

An accent inside the brand's family never pairs the brand with a second hue anti-slop bans, and letting warmth, formality and contrast move it keeps two cool brands with opposite briefs apart. Sliding along the arc's edge instead of jumping keeps the accent continuous in the axes. The engine and its tests share one rule.

## What it touches

character.BLUE_ARC, PURPLE_ARC, PINK_ARC, BANNED_COOL, FAMILY_SPAN, SUPPORT_QUIET, SUPPORT_LOUD, QUIET_COOLNESS, banned_pair, clear_of_banned, family_hue, support_seed and support_hue; color._primitives (the support family); art.art_files and report_lines; guidance/color.md.

## Consequences

A blue brand's accent ranges from azure to the edge of violet with the axes; a teal's from green to cyan; a purple's stays violet to magenta. Measured over hues every three degrees, chroma 0.06 to 0.24 and every corner of warmth and contrast, no brand gets a banned pairing.
