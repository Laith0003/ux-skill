---
id: fill-edge-page-only
title: A filled control's fill clears 3:1 against the page only
status: active
areas: [color, contracts]
supersedes: null
superseded_by: null
---

# A filled control's fill clears 3:1 against the page only

## Context

A primary or danger fill can sit on the page, a card or a raised dialog. Holding the fill to 3:1 against every surface would push the brand fill away from the brand for many brands, mostly in dark mode on the raised surface.

## Decision

The action fills and their hover and pressed steps, and the strong status fills, are paired with the page at 3:1 (4.5:1 under high contrast). As fills they are not paired with card, sunken or raised. On those surfaces the component is identified by its label, which clears 4.5:1 on the fill, and by its focus ring, which clears every surface.

## Why

WCAG asks for 3:1 on the visual information needed to identify a component; a button whose label names it does not need its fill edge for that. The page pairing is our rule, applied where most filled controls sit, and keeps the brand color recognizable.

## What it touches

color.PAIRINGS for action and status strong fills; the button contract, which pairs the fills with the page only.

## Consequences

Where a contract draws a strong status color as an edge or an icon rather than a fill, such as the danger secondary button's edge or the text field's error edge, it pairs that color with every surface it lists. A design that places a filled button where its label is not visible, such as an icon-only button on a raised surface, pairs that fill with the raised surface in its own contract.
