---
id: form-contracts
title: Every form control has a contract, and they share the field rules
status: superseded
areas: [contracts]
supersedes: null
superseded_by: form-contracts-per-control
---

# Every form control has a contract, and they share the field rules

## Context

Pages built from the system hand-rolled selects, checkboxes, radio buttons, text areas, date fields and a phone field with a dialing code, each with its own label size, edge and error treatment.

## Decision

Six contracts cover the form controls: select, checkbox, radio, textarea, date and input-prefix. Each ships at experimental with a null provenance, binds semantic roles only, and follows the text field's rules: a label in type.text.ui-large, helper and error text in type.text.body-small, a heavier edge on hover, an error edge in color.line.danger with a message and an icon, a reserved message line, and 44px targets. Choices show state with a mark or an edge as well as a fill. An input-prefix joins a fixed part (a dialing code, a currency) with radius.joined on the shared edge and keeps it left to right in a right to left form.

## Why

One set of field rules across every control is what makes a form read as one thing; contracts make the rules checkable against every build.

## What it touches

engine/contracts/seed/select.yaml, checkbox.yaml, radio.yaml, textarea.yaml, date.yaml, input-prefix.yaml.

## Consequences

A person promotes a contract to ready only against a design file, by the thresholds in the schema.
