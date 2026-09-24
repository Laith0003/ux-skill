---
id: container-edge
title: A container whose fill measures below 1.2:1 against its surface draws an edge
status: active
areas: [contracts, color, border, elevation]
supersedes: null
superseded_by: null
---

# A container whose fill measures below 1.2:1 against its surface draws an edge

## Context

A container is told apart from what it sits on by its fill, its edge or its shadow. Fills can come very close to the surfaces: in light high contrast the page, card, sunken and raised surfaces are all white, and a soft status fill can measure close to 1:1 against a surface. WCAG sets no minimum for the edge of a container, and a shadow alone does not mark a boundary a person can rely on.

## Decision

For every fill a contract binds and every surface the contract lists, bind.py measures the fill against the surface in every scheme and contrast context. Where it measures below 1.2:1 in any of them, the contract binds border-width to border.outline (or a heavier edge role in EDGE_ROLES) and a border-color that apply to that fill's variant and state, or the contract is refused. The 1.2:1 floor is ours (EDGE_FLOOR), not a WCAG number. A shadow is never the only edge.

## Why

How close a fill is to its surface is a fact the built tokens can show, so the rule is measured, not remembered, and it covers tinted fills that come close without being equal. Below 1.2:1 the fill does not mark the container's shape. The surfaces converge most under high contrast, and the people who switch it on are the ones who most need the boundary.

## What it touches

bind.py's container-edge rule, EDGE_FLOOR and EDGE_ROLES. The card, dialog, text-field and status-banner contracts bind an edge in every state; the status banner's edge is color.line.input, paired with every surface it lists at 3:1 (4.5:1 under high contrast). The secondary button binds an edge in every state, with color.text.disabled when disabled. The ghost button and the selectable row bind an edge wherever they take a fill: on hover and press, and for the row a heavier active edge when selected.

## Consequences

A container may choose a quiet edge color such as color.line.subtle when its edge only marks the shape, as the card and dialog do; when the edge is what separates it, as on the status banner, the contract pairs the edge color at 3:1. A fill that clears 1.2:1 against every surface it sits on, in every context, needs no edge from this rule.
