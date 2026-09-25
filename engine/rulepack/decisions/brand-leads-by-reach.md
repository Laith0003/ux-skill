---
id: brand-leads-by-reach
title: The brand leads its role when it is saturated and stands apart from the page and from ink
status: active
areas: [color]
supersedes: brand-leads-the-role
superseded_by: null
---

# The brand leads its role when it is saturated and stands apart from the page and from ink

## Context

The brand's evidence for filling the action was its saturation times how far it was a mid tone in absolute OKLCH lightness. That scored a saturated yellow such as #FFD400 at 0 and a navy such as #003366 low, so a yellow brand that fills its buttons with black text at 14.7:1 got an ink action, and the navies of banks, universities and government lost their buttons to a formal brief. Absolute lightness is not why a brand cannot carry a fill; a fill that cannot be told from the page or from ink is.

## Decision

character.brand_fill_evidence is the brand's saturation (0 at OKLCH chroma 0.03 and below, 1 at 0.12 and above) times its reach: its OKLab distance from the nearer of white and black, 0 at 0.04 and below, 1 at 0.12 and above, in proportion between (character.REACH). brand_role_scores adds 1.0 times the evidence to the fill score and 0.25 times its absence to the accent and edge scores, and the axes' own scores are unchanged. At full evidence fill scores at least 1.0, which no accent or edge score can pass, so a saturated brand fills the action whatever the brief: yellows, ambers, navies, teals and greens included. Accent or edge wins only where the brand argues for it: near grey, a near white tint or a near black, or a formal brief with a brand that cannot carry a fill. The text on the fill is not a factor: white or black always reaches 4.58:1, the square root of 21, on any color, and the fidelity rule decides which (decisions/natural-fill-for-white-text.md). The brief's brand_role overrides, and the host AI fills it from the client's own materials: when the client's app, site or identity fills its buttons with the brand, fill; ink buttons with brand links, accent; brand rules and edges around ink, edge.

## Why

A client recognizes its product by its color on its buttons. Reach measures what stops a color from working as a fill, its closeness to the page or to the ink beside it, so it is continuous in the brand color and keeps the three roles for the brands that need them.

## What it touches

character.SAT_CHROMA, REACH, BRAND_LEAD, BRAND_ARGUE, saturation, reach, brand_fill_evidence, brand_role_scores and brand_role; color.generate_color and its role note; the report's role line; commands/ux-system.md on brand_role; guidance/color.md.

## Consequences

Saturated brands fill their main action at every lightness. A pastel tint gets part of the evidence, in proportion to its chroma and reach, and the axes decide it.
