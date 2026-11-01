---
id: border-roles
title: Border roles are widths for four jobs plus the focus ring
status: active
areas: [border]
supersedes: null
superseded_by: null
---

# Border roles are widths for four jobs plus the focus ring

## Context

Border systems can name a width for every structural level and every state, several of them resolving to the same pixel value.

## Decision

Border has four width roles: border.separator between siblings, border.outline for a resting edge, border.emphasis for an edge that must outrank its neighbors, and border.active for a selected edge. The focus ring has its own width and offset roles, and two style roles cover solid and placeholder strokes. Border colors live in color: an edge at rest or selected takes a color.line role (subtle, input, selected), a danger or error edge takes color.status.danger.strong, and a disabled edge, in error or not, takes the role its contract names. A border role never carries a color.

## Why

Four jobs cover every structural edge a product draws. Separator and outline may share a value but not a meaning: a separator divides siblings inside one parent, an outline encloses a group. Emphasis and active are heavier than an outline, so state and priority never rest on color alone.

## What it touches

border.py roles(), the focus-ring, active-border, border-weight-order and border-whole-pixels checks, the contracts' border-width and border-color bindings.

## Consequences

Two roles with equal values are never swapped on the strength of their value. A new structural level is a new role with its job stated, not a new value on an existing role.
