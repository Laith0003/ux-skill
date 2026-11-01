---
id: divider-edge
title: A part inside a group draws one divider where it meets the rest, and the group draws the edge
status: active
areas: [contracts, border]
supersedes: null
superseded_by: null
---

# A part inside a group draws one divider where it meets the rest, and the group draws the edge

## Context

The container edge rule is per part: a fill below 1.2:1 against a surface needs border-width and border-color on the same part. A field's prefix and a table's sticky first column sit inside a group whose own edge draws their outer sides, so a full border on the part doubled the seam, and in a field in error it put a grey inner edge against a red outer one. border-width draws every side, so there was no way to bind the one line the part does need.

## Decision

Two binding properties draw one side of a part: divider-width and divider-color. The divider sits where the part meets the rest of its group: the inline end of a part at the start, the inline start of a part at the end, the end edge of a sticky column. For the container edge rule, a fill whose part binds both a divider width and a divider color for its variant and state has its edge: the divider draws the side it shares with the group, and the group's own edge draws the rest. A divider takes border.separator and a color.line role.

## Why

One shape with one edge reads as one control, and every state then changes that one edge. The rule stays measured: the part still needs a line where it meets the value or the scrolling cells, and a contract that relies on the line pairs its color.

## What it touches

schema.py PROPERTY_TYPES; bind.py's container edge rule; the input-prefix and table contracts; guidance/border.md.

## Consequences

A divider never stands in for the edge of a part that sits straight on a surface; a group with dividers binds its own border-width and border-color. The rule does not check that the group has one; the contract's usage says so.
