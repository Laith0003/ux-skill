---
id: clean-code-surface
title: Code blocks and tables have their own surfaces, and the light code surface is a clean well
status: active
areas: [color]
supersedes: code-and-table-colors
superseded_by: null
---

# Code blocks and tables have their own surfaces, and the light code surface is a clean well

## Context

Syntax colors drawn from the text roles are measured against the page, not against the block they sit on, and a table stripe borrowed from the sunken surface reads as recessed. On real pages the light code surface, the neutral step 100 at about 0.89 lightness, read as a muddy grey slab.

## Decision

color.surface.code is the code block's background. In light it is the neutral seed's step 50 hue and chroma at the lightest lightness that stands 1.2:1 off the light card, read from the card's own step (color.stand_off, CODE_EDGE, the container-edge floor), and the surfaces-stand-apart check measures it; in dark it is the recess between the page and the card; under high contrast it keeps neutral.100 in light and black in dark. Six syntax roles (plain, keyword, string, number, function, comment) are paired with it at 4.5:1 (WCAG 1.4.3), 7:1 under high contrast. color.surface.stripe marks alternate table rows one step off the card, and every text role is paired with it.

## Why

A code block needs to read as a block on the card and the page, and the container-edge floor is the step at which a fill reads without an edge; any darker only greys it. Measuring syntax colors on the surface they sit on is the only measurement that means anything.

## What it touches

color.SEMANTIC, CODE_EDGE, stand_off, _primitives (code-light), HIGH_CONTRAST, SYNTAX_ROLES, TEXT_SURFACES; the table contract.

## Consequences

Syntax colors reuse the status hues and the brand, so a code block reads as part of the system, and on the lighter surface they keep more room above 4.5:1.
