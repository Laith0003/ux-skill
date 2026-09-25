---
id: edge-weight-inside
title: A field's heavier hover and error edge is drawn inside its border
status: active
areas: [border, contracts]
supersedes: null
superseded_by: null
---

# A field's heavier hover and error edge is drawn inside its border

## Context

The field contracts bound border-width to border.emphasis on hover and in error, 2px against a resting 1px. A border that widens moves the field's content and everything after it by a pixel, so a pointer passing over a form made the page shift, and an error shown on blur did the same.

## Decision

A part's heavier edge in a state is edge-weight, a dimension property: the full weight of the edge in that state. The border keeps its resting border-width in every state, and the difference is drawn inside it, as an inset box-shadow in the state's border color, never as an outline, which the focus ring owns. The text field, textarea, date, select and field-with-prefix contracts bind edge-weight to border.emphasis for hover and error, and their border-width stays border.outline.

## Why

The edge still reads heavier, which is the non-color cue the error needs (WCAG 1.4.1), and nothing on the page moves. The focus ring already follows the same rule with outline.

## What it touches

schema.py PROPERTY_TYPES; engine/contracts/seed/text-field.yaml, textarea.yaml, date.yaml, select.yaml and input-prefix.yaml; guidance/border.md; tests/contracts/test_contract_findings.py.

## Consequences

A contract that needs a heavier edge on a control binds edge-weight, never a second border-width in a state. A selected row or tab still binds border.active as its border-width, since selection is a resting state that does not change under the pointer.
