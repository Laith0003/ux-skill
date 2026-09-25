---
id: fills-on-every-control-surface
title: A control's fill, or its edge, clears every surface a control sits on, and a placement allows only what it binds
status: active
areas: [color, contracts]
supersedes: fills-on-every-placement
superseded_by: null
---

# A control's fill, or its edge, clears every surface a control sits on, and a placement allows only what it binds

## Context

The primary edge and the danger fill were measured against page, card, sunken and raised, while the guidance puts controls on the tint, the section band and the table stripe too, and the landing playbook puts a call to action on the band. A steel blue brand's primary edge measured 2.73:1 on the section band, under WCAG 1.4.11, and teal brands fell under our 4.5:1 floor on the stripe and header in high contrast. The brand band's surface variant also allowed secondary, ghost and danger buttons on the band that nothing bound or measured.

## Decision

color.CONTROL_SURFACES is every surface a control sits on: page, card, sunken, raised, tint, band, stripe and header. The primary edge, the danger fill with its hover and pressed steps and the danger edge (color.status.danger.strong) are paired with each at 3:1 (WCAG 1.4.11) and our 4.5:1 floor under high contrast, and the button contract lists them all as its surfaces. The edge is the fill when the fill clears all of them, else the nearest step of its ramp that does. The disabled primary button draws an edge in color.text.disabled, since its fill can match a tinted surface. On the brand band (surface set to brand) the primary button takes its own group: color.action.on-brand, a neutral end on the side of the band's own text, with hover and pressed steps and a label in the brand step nearest the band that reads on it; its rest fill clears the band at 3:1 and is drawn as its edge in every state. Secondary and ghost buttons there take color.text.on-brand for the label, edge and ring, and under hover and press turn to that color as a fill with the band's color as the label. A placement allows only the combinations a binding under it names (Contract.combinations), so the button has no danger combination on the band, and the component set counts only what it binds. The contract check measures every action fill of an interactive contract, and every fill bound under a placement, or the edge drawn around it, against every surface the contract places it on, in every scheme and contrast context.

## Why

A control is identified by its boundary wherever it sits, so every surface a control is allowed on is measured, and a combination no binding covers cannot ship unmeasured.

## What it touches

color.CONTROL_SURFACES, PAIRINGS, GROUPS; schema.PLACEMENT and Contract.combinations and variant_product; bind._placement_problems; the button contract; guidance/color.md and border.md.

## Consequences

Some brands take an edge a step from the fill on the band, the stripe or the header. The button's component set holds 18 combinations: 12 on surfaces and 6 on the brand band.
