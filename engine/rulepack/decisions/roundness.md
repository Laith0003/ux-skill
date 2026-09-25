---
id: roundness
title: Geometry and formality set one roundness, and every corner follows it
status: active
areas: [radius]
supersedes: null
superseded_by: null
---

# Geometry and formality set one roundness, and every corner follows it

## Context

A corner scale set by geometry alone gives a playful brand at middle geometry the same 8px buttons and 12px cards as a formal one, and a scale in 2px steps from 2px to 12px never reaches a truly sharp or a truly soft look.

## Decision

character.roundness is geometry plus 0.4 times (0.5 minus formality), clamped to 0 to 1. The base corner is that roundness times 14px, to the nearest pixel, from 0px to 14px; the scale is fixed multiples of it. Chips turn into pills from roundness 0.6, controls from 0.85.

## Why

Playful brands read softer and formal ones squarer at any geometry, so formality shows in the shape. One number drives every role, so a control, a card and a dialog always round in proportion.

## What it touches

character.roundness; radius.base_corner, scale, roles, MAX_BASE_PX, CHIP_PILL_FROM and CONTROL_PILL_FROM.

## Consequences

At the sharp end the base corner is 0px, but the scale keeps each step at least 1px above the one below, so controls are 2px, cards 3px and dialogs 4px, and only radius.joined is square. Roundness from 0 to about 0.1 therefore gives the same corners. The nesting rule still holds.
