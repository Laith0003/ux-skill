---
id: high-contrast-levels
title: High contrast keeps every surface level apart, and the dark recess is never the page
status: active
areas: [color]
supersedes: high-contrast-surfaces
superseded_by: null
---

# High contrast keeps every surface level apart, and the dark recess is never the page

## Context

High contrast pushes surfaces toward the ends of the ramp. Taken to the end, every light surface is white and every dark one black, so cards and wells vanish and lean on a 1px edge; with a black sunken surface on a black page, a table header in dark high contrast read as nothing but a strip of page.

## Decision

Under high contrast in light, the page, card and raised surfaces are white and the sunken surface keeps its recess step, color.neutral.recess-light. In dark the page is black, the sunken surface keeps its recess between the page's step and the card's (decisions/dark-recess-and-bands.md), the card is neutral.900 and the raised surface neutral.800. Text on every surface still meets 7:1.

## Why

A card one full step above a black page measures about 1.3:1 instead of 1.08:1, so the level reads without its edge, and the heavier high-contrast edges the border foundation draws add to it. A well sits below the card it is cut into and above the page, in both contrasts. Every high contrast surface is at least as far out as its standard surface, so the focus ring can always hold its standard contrast.

## What it touches

color.HIGH_CONTRAST for color.surface.card, raised and sunken; the surface order the rule pack reports.

## Consequences

Light cards and raised surfaces still equal the page under high contrast and keep their edge (decisions/container-edge.md). Text on the dark sunken surface moves a step further out if it must, which the gate measures.
