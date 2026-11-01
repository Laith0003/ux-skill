---
id: space-relationship-roles
title: Spacing roles name a relationship, and there are fourteen of them
status: active
areas: [space]
supersedes: space-roles
superseded_by: null
---

# Spacing roles name a relationship, and there are fourteen of them

## Context

The first record said spacing had eight roles. Fields, tables and large controls since gained their own inner spacing, and the gap between page regions now also lives in layout, one per tier, so the count and the region rule were out of date.

## Decision

Spacing has fourteen roles, each for one relationship: space.control.gap (between adjacent controls); space.control.padding-inline and space.control.padding-block (inside a control) and their -large forms (inside a large control); space.field.label-gap and space.field.message-gap (a label to its field, a field to its message); space.table.cell-padding-inline and space.table.cell-padding-block (inside a table cell); space.text.gap (between blocks of text); space.list.gap (between stacked rows); space.group.gap (between groups); space.card.padding (inside a container); and space.region.gap (between page regions). space.region.gap equals layout.region-gap.desktop at every density, and a page that spaces its regions by viewport reads the responsive alias --layout-region-gap (decisions/page-regions-by-tier.md). Page margins and gutters live in layout and alias the same scale. There is no size ladder per relationship.

## Why

One role per relationship makes the choice a question of what the space separates, which a reviewer can check. The density axis changes every role at once in one direction, so a second size per relationship is not needed to make a view tighter. Two tokens for one gap agree, so neither can mislead.

## What it touches

space.py ROLES and HIERARCHY, the control-gap, space-hierarchy and compact-not-larger checks; layout.py REGION_GAP, gutters and margins; guidance/space.md and guidance/border.md.

## Consequences

A design that needs a spacing the roles do not name uses the closest role by relationship, or proposes a new role with its relationship stated. Padding and gap are never swapped for each other because their values match.
