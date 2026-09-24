---
id: color-roles
title: Color keeps one role per job, and interaction states belong to their fill
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Color keeps one role per job, and interaction states belong to their fill

## Context

Color systems grow families of near-duplicate roles: several text levels, several border weights, a generic hover overlay, a separate focus ring per intent, extra hue families. Each extra role is another pair the gate must measure and another choice a designer can get wrong.

## Decision

Color has six surfaces (page, card, sunken, raised, inverse, selected), text in default, muted, link, inverse, disabled and the on-fill roles, two filled actions (primary and danger) each with its own hover and pressed steps, three lines (subtle, input, selected), one focus ring plus a ring for the inverse surface, the scrim, and four statuses (danger, warning, success, info) with text, soft, strong and on-strong roles. There is no third text level, no generic hover or pressed overlay, no disabled line role, no destructive focus ring and no extra hue family. Translucent colors are 8-digit hex and are used for overlays only, never in a pairing.

## Why

Two text levels cover reading and supporting copy; a third level falls below the contrast minimum on some surfaces for some brands. Hover and pressed steps chosen per fill are measured against the text on them, which an overlay cannot promise across every surface it lands on. One ring with a guaranteed gap of page color is visible next to any fill, danger included. Contrast is defined for opaque colors only, so a translucent role is never paired.

## What it touches

color.py SEMANTIC and HIGH_CONTRAST, the fill-group solver, the coverage tables and COVERAGE_EXEMPT, the button contract's secondary and ghost bindings.

## Consequences

Secondary and ghost buttons reuse the link text, the selected line and the selected surface. De-emphasized copy uses muted text, never disabled text. There is no disabled line role, so each contract names its disabled edge: the secondary button's edge takes color.text.disabled, matching its disabled label; the check box in the selectable row takes color.text.disabled, matching the row's disabled text; the text field's edge takes color.line.subtle. A new role joins a coverage table or COVERAGE_EXEMPT with a reason, or the build refuses it.
