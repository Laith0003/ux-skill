---
id: ring-on-tinted-fills
title: A focus ring on a tinted fill keeps 3:1 in high contrast
status: active
areas: [color, contracts]
supersedes: null
superseded_by: null
---

# A focus ring on a tinted fill keeps 3:1 in high contrast

## Context

Controls inside a status banner sit on a soft status fill, and a selected row is tinted with the selected surface. Their focus ring is adjacent to that tint. Measured across brands, one ring cannot clear the soft fills, the page and the other surfaces at the 4.5:1 high-contrast floor at once.

## Decision

The status-banner and selectable-row contracts pair color.focus.ring with each soft status fill and with color.surface.selected at 3:1 (WCAG 1.4.11) and pin that 3:1 under high contrast with high: 3. Every other ring pairing keeps the 4.5:1 floor.

## Why

3:1 is what WCAG asks of a focus indicator at every level, and it holds in every context for every brand. The raised floor is ours; where it cannot hold, the pairing says so in the contract instead of failing some brands or retuning the brand color.

## What it touches

The status-banner and selectable-row contracts, the contract schema's high field, the gate's required().

## Consequences

The pin is visible in the contract and in the rule pack. A product that needs 4.5:1 there binds, in its own contract, a ring color it has paired with those fills at 4.5:1, and the gate measures it.
