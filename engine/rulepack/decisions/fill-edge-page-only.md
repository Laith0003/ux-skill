---
id: fill-edge-page-only
title: A filled control's fill clears 3:1 against the page only
status: superseded
areas: [color, contracts]
supersedes: null
superseded_by: primary-edge
---

# A filled control's fill clears 3:1 against the page only

## Context

A primary or danger fill can sit on the page, a card or a raised dialog. Holding the fill to 3:1 against every surface would move the brand fill for some brands. Measured over 90 brands (the brands the color and contract tests use) in 3 axis sets, 270 builds in every scheme and contrast context: 2 brands, in 6 builds, have an action or strong status fill, or one of its hover and pressed steps, below its floor against card, sunken or raised. Every one is color.action.primary on the raised surface in dark standard contrast, worst 2.85:1 in that sample; over a wider sample of 152 brands in 456 builds the same pair reaches 2.79:1 (#2D0679).

## Decision

The action fills and their hover and pressed steps, and the strong status fills, are paired with the page at 3:1 (4.5:1 under high contrast). As fills they are not paired with card, sunken or raised. On those surfaces the component is identified by its label, which clears 4.5:1 on the fill, and by its focus ring, which clears every surface.

## Why

WCAG asks for 3:1 on the visual information needed to identify a component; a button whose label names it does not need its fill edge for that. The page pairing is our rule, applied where most filled controls sit, and keeps the brand color recognizable.

## What it touches

color.PAIRINGS for action and status strong fills; the button contract, which pairs the fills with the page only.

## Consequences

Where a contract draws a strong status color as an edge or an icon, it pairs that color with what the edge or icon sits on, per contract: the button pairs color.status.danger.strong, the danger edge of its secondary and ghost buttons, with page, card, raised and sunken at 3:1; the text field pairs it, its error edge and icon, with page, card, raised and sunken at 3:1; the status banner pairs each strong status color, its icon, with that status's soft fill only, at 3:1. A design that places a filled button where its label is not visible, such as an icon-only button on a raised surface, pairs that fill with the raised surface in its own contract.
