---
id: layout-scope
title: Layout tokens cover the page grid; regions and panes belong to page patterns
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# Layout tokens cover the page grid; regions and panes belong to page patterns

## Context

A layout system can carry tokens for every pane of an application shell: navigation widths, side panels, work areas, their minimums and maximums per breakpoint.

## Decision

Layout tokens cover the page: three breakpoints and four tiers (phone, tablet, laptop, desktop), columns, gutters and inline margins per tier, the container width, two reading measures (text and form) and the minimum target size. Regions, panes and how they collapse are patterns that compose these tokens on a given kind of page, not tokens of their own.

## Why

Every product has a page grid, but only some have panes, and their widths depend on what the panes hold. Pane widths as tokens would ship numbers most systems never use and some would use wrongly. The grid tokens are enough for a pane pattern to state its widths in columns and measures.

## What it touches

layout.py, its breakpoint, column, target and measure checks, and the page patterns for dashboards and application shells.

## Consequences

A side panel is sized in columns or by layout.measure.form, not by a pane token. The main content keeps priority: secondary panes collapse, move below or overlay before it narrows.
