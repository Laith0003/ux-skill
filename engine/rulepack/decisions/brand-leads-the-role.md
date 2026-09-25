---
id: brand-leads-the-role
title: The brand color leads its role, and the axes decide only where the brand cannot carry a fill
status: superseded
areas: [color]
supersedes: brand-roles
superseded_by: brand-leads-by-reach
---

# The brand color leads its role, and the axes decide only where the brand cannot carry a fill

## Context

The brand's role (fill, accent or edge) was scored from the axes alone, so the brief's words decided it. A formal or trustworthy brief put a saturated electric blue and a saturated mid blue on accent or edge, with ink buttons, although both brands fill their own buttons in the client's app and site. The brief field that could correct it, brand_role, was documented as for the user to name only, so the host AI could not set it from the client's own materials.

## Decision

The brand color is the identity, so its own evidence enters the score. character.brand_fill_evidence is its saturation (0 at OKLCH chroma 0.03 and below, 1 at 0.12 and above) times how far it is a mid tone (0 at lightness 0.30, 1 from 0.42 to 0.74, 0 again at 0.86), each in proportion between. brand_role_scores adds 1.0 times that evidence to the fill score and 0.25 times its absence to the accent and edge scores; the axes' own scores are unchanged. At full evidence fill scores at least 1.0, which no accent or edge score can pass, so a saturated mid-tone brand fills the action whatever the brief. Accent or edge wins only where the brand argues for it: very light, very dark or near grey, or a formal brief with a brand that cannot carry a fill. The text on the fill is not a factor: white or black text always reaches 4.58:1, the square root of 21, on any color, and the fidelity rule decides which (decisions/natural-text-on-the-brand.md). The brief's brand_role overrides, and the host AI fills it from the client's own materials: when the client's app, site or identity fills its buttons with the brand, fill; ink buttons with brand links, accent; brand rules and edges around ink, edge.

## Why

A client recognizes its product by its color on its buttons; demoting it for the brief's tone makes the system someone else's. Evidence that is continuous in lightness and chroma keeps two near brands on the same side, and letting the axes decide where the brand cannot carry a fill keeps the three roles for the brands that need them: a pale yellow, a navy and a grey.

## What it touches

character.SAT_CHROMA, FILL_L, BRAND_LEAD, BRAND_ARGUE, saturation, mid_lightness, brand_fill_evidence, brand_role_scores and brand_role; color.generate_color and its role note; the report's role line; commands/ux-system.md on brand_role; guidance/color.md.

## Consequences

Most saturated brands fill their main action, whatever the brief. The role note names the brand's evidence beside the scores. A system a brief built with an ink action for a saturated brand gets a brand-filled action when built again.
