---
id: dark-text-sets-lighter
title: In dark mode a variable face sets text a little lighter, and high contrast keeps its own weights
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# In dark mode a variable face sets text a little lighter, and high contrast keeps its own weights

## Context

Light text on a dark page spreads and reads heavier than the same weight dark on light, most at small sizes. Type did not vary on the scheme, so dark mode showed every style at its light-mode weight. A study of an interaction-detail site found its variable faces set lighter in dark mode.

## Decision

Type varies on scheme as well as direction and contrast, in a system that has a dark scheme: one that builds color (BrandInputs.dark_scheme); a set built without color, such as type added to another system alone, gains no dark mode. In dark mode at standard contrast, every style set in a variable face takes typography.dark_weight: lighter by 40 at body size, falling on a log scale of size to 10 at 96px and above, in tens, never heavier and never under 300 or the lightest weight the face ships. Emphasis (type.strong) follows at body size. A static face keeps its weights, and so does every style under high contrast, in both schemes. dark-weights: in dark mode at standard contrast no style is heavier than in light mode. high-contrast-weights and strong-weight now read both schemes.

## Why

The lighter weight evens how heavy text reads across the two schemes, and it matters most where strokes are thin. Only a variable face has the weights between its steps; a static face would jump a whole step. High contrast asks for heavier text, so it wins over the dark adjustment.

## What it touches

typography.DARK_LIGHTER, DARK_LIGHTER_PX, DARK_FLOOR, dark_weight, generate_type, the dark-weights, high-contrast-weights and strong-weight checks; foundation.BrandInputs.dark_scheme; build_system; modes.FOUNDATION_AXES; guidance/type.md.

## Consequences

tokens.css writes each style's dark font-weight in the dark blocks, so a page reads the same property in both schemes. A static Arabic face keeps its weights under right to left in dark mode.
