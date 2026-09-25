---
id: roles-on-their-scale
title: Spacing, radius and layout spacing roles point at a step of their own scale
status: active
areas: [space, radius, layout]
supersedes: null
superseded_by: null
---

# Spacing, radius and layout spacing roles point at a step of their own scale

## Context

An imported set can point space.card.padding at a radius step, or a gutter at a border width, and every value check still passes because the number happens to fit. The set then moves wrongly the moment either scale changes.

## Decision

Three checks hold each role to its scale when the role aliases a primitive. space-on-scale: every spacing role points at a numbered space step. radius-on-scale: every radius role points at a numbered radius step or radius.round. layout-on-space: every gutter, inline margin, region gap, landing gap and hero padding at every tier, and the header and footer padding, points at a numbered space step. The spacing and layout checks read every density. A role that holds its value directly is left to the value checks. The failure names the role, the token it points at and the scale to point it at instead.

## Why

A role takes its value from the scale that owns its kind of value, so a change to the spacing scale moves every spacing role and nothing else. Layout gaps are spacing, so layout and spacing move together.

## What it touches

space.ROLES and the space-on-scale check; radius.ROLE_TYPES and the radius-on-scale check; layout.ON_SPACE and the layout-on-space check; foundation.direct_alias and is_step; guidance/space.md, radius.md and layout.md.

## Consequences

A generated set passes, because every role it builds aliases its own scale. An imported set with a cross-scale alias fails with the role named; the fix is to point it at a step of its own scale.
