---
id: spacing-within-group
title: Spacing inside a component never outgrows the gap between groups
status: active
areas: [space]
supersedes: null
superseded_by: null
---

# Spacing inside a component never outgrows the gap between groups

## Context

space-hierarchy holds the text gap, group gap and region gap in order, but the roles inside a component sat outside it. An imported set could pad a card or space a list wider than the gap between groups, so the parts of one thing read as separate things.

## Decision

The space-within-group check reads every density. The control gap, control inline and block padding, the large control's block padding, the field label and message gaps, the table cell padding, the list gap and the card padding are each at most space.group.gap, and the list gap is strictly below it. The large control's inline padding is left out: it sizes the one call to action of a hero, and a dense system gives it more room than the gap between groups. The failure names the role, its value, the group gap and the direction to move.

## Why

Proximity is how a person tells what belongs together. Space inside a group smaller than the space between groups keeps each group reading as one unit, and list rows, which sit side by side inside a group, must sit closer than the groups do.

## What it touches

space.WITHIN_GROUP, GROUP and the space-within-group check; guidance/space.md.

## Consequences

A generated set passes at both densities. An imported set with card padding above its group gap fails and is told to move the padding down the scale.
