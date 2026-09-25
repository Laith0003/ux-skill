---
id: field-and-table-spacing
title: Fields and tables have their own inner spacing
status: active
areas: [space]
supersedes: null
superseded_by: null
---

# Fields and tables have their own inner spacing

## Context

A label to field gap borrowed from the text gap and table cells padded like controls give forms and tables no rhythm of their own.

## Decision

space.field.label-gap and space.field.message-gap hold a field's label, input and message together, from 8px (airy) to 4px (dense). space.table.cell-padding-inline and space.table.cell-padding-block pad a table cell, from 16px and 12px (airy) to 12px and 8px (dense). Each takes one step less under compact density, never below its floor.

## Why

A field reads as one unit when its parts sit closer to each other than to the next field; a table reads when its cells are padded less than a card.

## What it touches

space.ROLES; the text-field, select, textarea, date and table contracts.

## Consequences

A message that appears under a field on blur reserves its space, so the submit button never moves.
