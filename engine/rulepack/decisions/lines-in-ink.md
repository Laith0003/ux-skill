---
id: lines-in-ink
title: Decorative lines and a card's ring are the ink at a low alpha, and control edges stay opaque
status: active
areas: [color, elevation]
supersedes: null
superseded_by: null
---

# Decorative lines and a card's ring are the ink at a low alpha, and control edges stay opaque

## Context

Separators and card edges were opaque neutral steps chosen per surface, so one line looked different on the page, a card and a band. A study of a component kit drew them in the text color at a low alpha, which reads the same on every surface, and ringed cards with a 1px spread shadow.

## Decision

color.hairline is the text color of each context at character.ink_alpha (0.05 for a muted system to 0.12 for a bold one, by contrast), 1.5 times that under high contrast; it has no contrast minimum and is for decorative lines only. elevation.card adds a third layer, a 1px spread ring at that alpha, black in light and white in dark, to its key and ambient shadows. A control's edge stays color.line.input, measured at 3:1 against every surface it sits on.

## Why

A translucent line takes the surface under it, so one role serves every surface; a control's edge is how people find it, so it keeps an opaque, measured color.

## What it touches

character.ink_alpha; color.INK_LINE_HIGH, _add_ink_and_budget and the color.hairline role; elevation.shadow; guidance/color.md and elevation.md.

## Consequences

A page draws separators and a card's outline from color.hairline and never from the input edge.
