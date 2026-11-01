---
id: list-gap-and-control-gap
title: Stacked rows use the list gap, controls in a row use the control gap
status: active
areas: [space, contracts]
supersedes: null
superseded_by: null
---

# Stacked rows use the list gap, controls in a row use the control gap

## Context

Two spacing roles sit between repeated items: one between rows stacked in a list, one between controls placed side by side. They can look interchangeable, and in compact density the list gap is small.

## Decision

space.list.gap is the space between stacked rows. space.control.gap is the space between adjacent controls in a row, such as chips, toggle groups or a button pair, and it never falls below 8px. The gap between an icon and its label inside one control is space.control.gap too; there is no separate icon gap role.

## Why

A row that is itself a full-width target at the minimum target size needs no gap for WCAG 2.5.8, which sets 24 by 24 CSS px targets; its size already separates it. Small controls side by side are where a mistaken tap lands, so their gap carries our 8px floor. One gap inside a control keeps icon and label spacing consistent with the spacing between controls.

## What it touches

space.py ROLES and the control-gap check; the selectable-row contract (stack-gap) and the button contract (gap).

## Consequences

A list of small targets laid out in a row uses the control gap, not the list gap. The list gap can be small in compact density without harming anyone who taps.
