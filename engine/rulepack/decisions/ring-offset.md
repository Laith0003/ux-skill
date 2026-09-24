---
id: ring-offset
title: The focus ring clears the surfaces, and an offset keeps it off the fill
status: active
areas: [color, border]
supersedes: null
superseded_by: null
---

# The focus ring clears the surfaces, and an offset keeps it off the fill

## Context

A focus ring drawn flush against a filled button touches two colors: the fill and the surface around it. Making one ring clear both the brand fill and every surface at 3:1 forces the fill away from the brand color for many brands.

## Decision

The ring is drawn with an offset of at least 1px (border.focus-ring.offset, 2px as generated), so the color next to it is always the surface, never the fill. color.focus.ring is paired with the page, card, sunken and raised surfaces at 3:1 (WCAG 1.4.11) and is not paired with the fill. The inverse surface has its own ring, color.focus.ring-inverse. The ring is at least 2px wide and wider than a resting outline.

## Why

WCAG 1.4.11 asks that the indicator contrast with the colors adjacent to it; with an offset those colors are surfaces. Dropping the ring-to-fill pairing keeps the brand fill where the brand put it. 2.4.7 asks only that focus be visible and sets no ratio.

## What it touches

color.PAIRINGS and the ring choice in the fill-group solver; border.py's focus-ring check; every interactive contract, which binds focus-ring, focus-ring-width and focus-ring-offset together.

## Consequences

Code that draws the ring keeps the offset: outline-offset set from border.focus-ring.offset, never 0. A build without the border foundation notes that it relies on the offset.
