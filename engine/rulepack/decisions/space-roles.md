---
id: space-roles
title: Spacing roles name a relationship, and there are eight of them
status: active
areas: [space]
supersedes: null
superseded_by: null
---

# Spacing roles name a relationship, and there are eight of them

## Context

Spacing systems often offer every relationship in five sizes, which multiplies into dozens of roles and invites picking a size by eye instead of by relationship.

## Decision

Spacing has eight roles, each for one relationship: space.control.gap (between adjacent controls), space.control.padding-inline and space.control.padding-block (inside a control), space.text.gap (between blocks of text), space.list.gap (between stacked rows), space.group.gap (between groups), space.card.padding (inside a container) and space.region.gap (between page regions). Page margins and gutters live in layout and alias the same scale. There is no size ladder per relationship.

## Why

One role per relationship makes the choice a question of what the space separates, which a reviewer can check. The density axis changes every role at once in one direction, so a second size per relationship is not needed to make a view tighter.

## What it touches

space.py ROLES and HIERARCHY, the control-gap, space-hierarchy and compact-not-larger checks, layout.py gutters and margins.

## Consequences

A design that needs a spacing the roles do not name uses the closest role by relationship, or proposes a new role with its relationship stated. Padding and gap are never swapped for each other because their values match.
