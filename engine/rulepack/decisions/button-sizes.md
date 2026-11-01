---
id: button-sizes
title: Buttons come in two sizes, and a view is one screen
status: active
areas: [contracts, type, space, layout]
supersedes: null
superseded_by: null
---

# Buttons come in two sizes, and a view is one screen

## Context

One button size made the call to action of a hero a 14px toolbar button, and one primary per view had no meaning on a long scrolling page.

## Decision

The button has a size variant: medium (every button by default) and large (the one call to action of a hero or a band), which takes type.text.ui-large, space.control.padding-inline-large and padding-block-large, and a min-size of layout.target.large, 12px above the minimum target. A view is what one screen shows without scrolling: a long page may have a primary button in each section, as long as two never share one screen.

## Why

A hero's call to action needs the weight of the hero without a new color; a view defined by the screen keeps the one-primary rule meaningful on landing pages.

## What it touches

engine/contracts/seed/button.yaml; the large control roles in space, type and layout.

## Consequences

The button contract has twelve variant combinations.
