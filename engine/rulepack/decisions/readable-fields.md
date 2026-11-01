---
id: readable-fields
title: A field's helper and error text are readable, and its label is never smaller than its value
status: active
areas: [contracts, type, space]
supersedes: null
superseded_by: null
---

# A field's helper and error text are readable, and its label is never smaller than its value

## Context

Helper and error text set in fine print, a 14px label over a 16px value, a placeholder in the helper's color, a measure on the input instead of the form, no hover state, and an error that appears on blur and pushes the submit button away from the pointer.

## Decision

The text field sets its helper text and error message in type.text.body-small (never fine print), its label in type.text.ui-large (body size at the ui weight), and its helper text in the default text color so a placeholder in the muted color never reads like a typed value or like the rule. Hover draws a heavier edge in the same color. space.field.label-gap and space.field.message-gap hold label, field and message together. The form, not the field, is capped at layout.measure.form. The contract reserves one line under every field before an error appears, so an error shown on blur never moves the submit button.

## Why

People must read helper and error text to act, so it cannot be fine print; a label smaller than the value inverts the hierarchy; a moving submit button loses the click.

## What it touches

engine/contracts/seed/text-field.yaml; type.text.ui-large; space.field.label-gap and message-gap.

## Consequences

Forms are taller by the reserved message line. The new select, textarea and date contracts follow the same rules.
