---
id: fills-on-every-placement
title: A control's fill, or its edge, clears every surface its contract places it on, the brand band included
status: superseded
areas: [color, contracts]
supersedes: primary-edge
superseded_by: fills-on-every-control-surface
---

# A control's fill, or its edge, clears every surface its contract places it on, the brand band included

## Context

The primary edge and the danger fill were paired with the page only. A page put the primary button on the brand band, as the guidance's closing call to action suggests, and in dark mode an ink button on a grey band measured about 1.3:1; with the brand role fill the button on the band is the band's own color. Nothing measured either.

## Decision

The color gate pairs color.action.primary-edge, and the danger fill with its hover and pressed steps, with every surface the button contract places a button on: page, card, sunken and raised, at 3:1 (WCAG 1.4.11) and our 4.5:1 floor under high contrast. The edge is the fill when the fill clears all four, else the nearest step of its ramp that does. The button on the brand band has its own group: color.action.on-brand, a neutral end on the side of the band's own text, with its hover and pressed steps and a label, color.text.on-brand-action, in the brand step nearest the band that reads on it at the text minimum. Its rest fill clears the band at 3:1 and is drawn as its edge in every state, so the states need only their text. The button contract has a surface variant: surface=brand places the primary button on color.surface.brand with those roles and color.text.on-brand as its focus ring. The contract check measures every action fill of an interactive contract, or the edge drawn around it, against every surface the contract places it on (its surfaces, or the one a surface variant names), in every scheme and contrast context, and names the fill, the surface and the context that falls short.

## Why

A control is identified by its boundary wherever it sits; a pairing that stops at the page leaves every other placement to luck. Measuring by placement, not by a list of pairings someone remembered, catches a new surface as soon as a contract names it. The band gets its own button because a brand-filled button on the brand band cannot be told from it.

## What it touches

color.CONTROL_SURFACES, PAIRINGS, GROUPS (grounds, brand_text, states_on_grounds), _choose_edge and _start_on_band; the four color.action.on-brand roles; schema.PLACEMENT; bind._placement_problems; the button contract; guidance/color.md.

## Consequences

A few brands take an edge a step away from the fill on dark card or raised surfaces. A contract that places a control on another surface names it with a surface variant and is measured there. Secondary, ghost and danger buttons stay off the brand band.
