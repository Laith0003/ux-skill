---
id: dark-text-keeps-its-weight
title: In dark mode text keeps its weight, only heavy display styles set lighter, and high contrast keeps its own weights
status: active
areas: [type]
supersedes: dark-text-sets-lighter
superseded_by: null
---

# In dark mode text keeps its weight, only heavy display styles set lighter, and high contrast keeps its own weights

## Context

Type varies on scheme in a system that has a dark scheme. Light text on a dark ground loses contrast and breaks up when its strokes thin, most at body and small sizes. Two tier 1 and two tier 2 books agree that reversed text needs equal or more weight (B88 p.139; B18 p.135-136; B19 p.29; B31 p.92). Large display type set heavy can read heavier on a dark ground.

## Decision

In dark mode at standard contrast every body, text, label and mono style keeps its light-mode weight. A display style (a role of the display kind) at weight 600 or more, set in a variable face, takes typography.dark_weight: lighter by 40 at body size, falling on a log scale of size to 10 at 96px and above, in tens, never heavier and never under 600 or the lightest weight the face ships. Emphasis (type.strong) keeps its weight. A static face keeps its weights, and so does every style under high contrast, in both schemes. dark-weights: in dark mode at standard contrast no style is heavier than in light mode. high-contrast-weights and strong-weight read both schemes.

## Why

Thinning reversed text costs legibility where strokes are already thin, and the weighted sources in research/library/gaps.md (row Reversed text weight) overrule a lighter dark weight for text. Only heavy display type has stroke to spare, so only it may set a little lighter.

## What it touches

typography.DARK_LIGHTER, DARK_LIGHTER_PX, DARK_DISPLAY_FROM, dark_weight, generate_type, the dark-weights, high-contrast-weights and strong-weight checks; foundation.BrandInputs.dark_scheme; build_system; modes.FOUNDATION_AXES; guidance/type.md; references/foundations/typography.md.

## Consequences

tokens.css writes a dark font-weight only for the display styles that set lighter, so body text reads the same weight in both schemes. A static Arabic face keeps its weights under right to left in dark mode.
