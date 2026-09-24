---
id: radius-roles
title: Six radius roles follow structure, and geometry sets the scale
status: active
areas: [radius]
supersedes: null
superseded_by: null
---

# Six radius roles follow structure, and geometry sets the scale

## Context

A radius system can grow a role for every shade of softness per shape category, which turns a structural signal into a matter of taste per screen.

## Decision

Radius has six roles: radius.joined for shared edges, radius.chip, radius.control, radius.card, radius.dialog and radius.pill. The geometry axis sets the base corner and the scale is fixed multiples of it; soft brands move chips, then controls, to the pill shape. There are no softer or sharper variants of a role.

## Why

A corner tells people what kind of thing they are looking at: a joined seam, a control, a container, a floating layer. Six roles carry that signal. The brand's softness belongs to the scale, set once by the geometry axis, so every role moves together and the structure stays readable.

## What it touches

radius.py roles(), the radius-nesting, radius-joined, radius-pill and radius-scale-order checks.

## Consequences

A component takes its radius from its structural role, and the radius never changes between states. A softer or sharper look is a change to the geometry axis, not a new role.
