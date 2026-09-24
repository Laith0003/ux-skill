---
id: type-roles
title: Nine text styles as composites, faces chosen per script
status: active
areas: [type, direction]
supersedes: null
superseded_by: null
---

# Nine text styles as composites, faces chosen per script

## Context

Type systems can expand every role into several sizes and emphasis levels, each split into separate tokens for family, size, weight, line height and letter spacing, and assign families by category of use.

## Decision

Type has nine text styles, each one composite token holding family, size, weight, line height and letter spacing: hero, heading-1, heading-2, heading-3, body, body-small, ui, fine and code. Faces are chosen per script: one Latin face, one Arabic face drawn to sit beside it, and one monospace face for code. Emphasis inside a style is type.strong, a weight, not another style.

## Why

A composite keeps the five properties of a style together, so no one sets a size without its line height. Nine styles span a page from its hero to its fine print. Choosing faces per script, not per use, is what keeps Arabic readable: under right to left every style except code switches to the Arabic face at its own size and leading.

## What it touches

typography.py ROLES, PAIRINGS and generate_type, the type-sizes, reading-leading, arabic-text, rem-sizes and type-hierarchy checks.

## Consequences

A heading that needs more weight uses type.strong, not a new style. A product that needs a second Latin face for display adds a face and a style that uses it, and the Arabic face beside it.
