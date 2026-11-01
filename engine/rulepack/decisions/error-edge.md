---
id: error-edge
title: A field's error edge has its own role and keeps its red
status: active
areas: [color, contracts]
supersedes: null
superseded_by: null
---

# A field's error edge has its own role and keeps its red

## Context

The strong danger fill carries white text at 7:1 under high contrast, so it goes dark there. A field's error edge drawn in that fill turns near black in light high contrast and stops reading as an error.

## Decision

color.line.danger is the error edge of a field. It carries no text, so it is paired only as a non-text part, at 3:1 against every surface a control sits on: the page, card, sunken and raised surfaces, the tint, the band and the table stripe (our 4.5:1 floor under high contrast). The error-edge-hue check keeps its high contrast step within one ramp step of its standard step, and fails closed: a high contrast edge that is a literal color or a step of another ramp is a finding, since it can lose the red just as a far step does.

## Why

An edge with no text on it can stay at the middle of the danger ramp, where the hue is strongest, and still clear 4.5:1 on white. One step of movement is enough for high contrast; more turns the edge into a dark neutral that reads as no error at all.

## What it touches

color.SEMANTIC, HIGH_CONTRAST and LINE_ROLES; the error-edge-hue check; the text-field contract's error state.

## Consequences

The strong danger fill still colors icons and badges. An error still carries an icon and a message beside the edge (WCAG 1.4.1).
