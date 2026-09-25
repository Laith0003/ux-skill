---
id: reflow-at-320
title: A 320px viewport gets the phone grid, and the phone grid leaves each column 44px there
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# A 320px viewport gets the phone grid, and the phone grid leaves each column 44px there

## Context

WCAG 1.4.10 asks that content reflow, without scrolling in two dimensions, at a width equivalent to 320 CSS px. A set whose tablet tier starts at or below 320px hands that viewport a multi-column grid, and a phone grid with wide margins and gutters can leave columns too narrow to hold a control.

## Decision

reflow-phone-tier cites WCAG 1.4.10: layout.breakpoint.tablet sits above 320px (layout.REFLOW_PX), so a 320px viewport gets the phone grid. phone-columns: at 320px, the width left after two phone inline margins and the phone gutters between the phone columns is at least 44px per column (layout.MIN_PHONE_COLUMN_PX). The 44px floor is ours, the size of our comfortable target, so a column can hold one; WCAG sets no column width. Both checks read every density.

## Why

Reflow is met by the grid a narrow viewport receives, so the tier boundary is where the build can hold it. A column narrower than a comfortable target cannot hold a control, which forces horizontal scrolling or overlap at exactly the width 1.4.10 names.

## What it touches

layout.REFLOW_PX and MIN_PHONE_COLUMN_PX; the reflow-phone-tier and phone-columns checks; guidance/layout.md.

## Consequences

A generated set passes. An imported set with its tablet breakpoint at 320px or below fails and is told to start the tablet tier above 320px; one with crowded phone columns is told to narrow the phone margins or gutters. Meeting 1.4.10 on a page still depends on the page's own content, which these checks do not see.
