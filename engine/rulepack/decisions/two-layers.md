---
id: two-layers
title: Tokens have two layers, primitives and semantic roles
status: active
areas: [color, space, radius, border, elevation, motion, layout, type]
supersedes: null
superseded_by: null
---

# Tokens have two layers, primitives and semantic roles

## Context

A token system can stack several layers between a raw number and the place it is used: a scale of steps, named sizes on that scale, roles that point at the names, and per-mode overrides on top. Each extra layer is one more hop to trace before a change is safe.

## Decision

Every foundation has exactly two layers. Primitives hold literal values and never vary by mode. Semantic roles alias primitives, and only semantic roles carry per-mode overrides. Components and contracts bind semantic roles, never primitives, and never a literal. The numbered scale is the primitive layer itself: space.4 is 16px, radius.3 is a multiple of the base corner.

## Why

Two layers are enough to separate what a value is from what it is for. A third layer of plain numbers adds nothing a generator needs, because the generator computes the steps; it only adds a place for values to drift. With modes confined to the semantic layer, a dark or compact value can never leak into a primitive that something else reads.

## What it touches

The validator: primitive-alias, primitive-modes, semantic-literal and semantic-to-semantic problems. Every generator writes primitives first, then roles. Contracts are checked by bind.py, which refuses a primitive or a literal.

## Consequences

To change a value everywhere, move the primitive a role points at, or point the role at another primitive. To change one use, change the role. A per-mode difference is always an override on a role. Nothing outside the token file names a primitive.
