---
id: high-contrast-surfaces
title: High contrast keeps every surface level apart
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# High contrast keeps every surface level apart

## Context

High contrast pushes surfaces toward the ends of the ramp. Taken to the end, every light surface is white and every dark one black, so cards and wells vanish and lean on a 1px edge.

## Decision

Under high contrast in light, the page, card and raised surfaces are white and the sunken surface is neutral.100. In dark, the page and the sunken surface are black, the card is neutral.900 and the raised surface neutral.800. Text on every surface still meets 7:1.

## Why

A card one full step above a black page measures about 1.3:1 instead of 1.08:1, so the level reads without its edge, and the heavier high-contrast edges the border foundation draws add to it. A light well stays visible on white. Text roles move to keep 7:1, which the gate measures.

## What it touches

color.HIGH_CONTRAST for color.surface.card, raised and sunken; the surface order the rule pack reports.

## Consequences

Light cards and raised surfaces still equal the page under high contrast and keep their edge (decisions/container-edge.md).
