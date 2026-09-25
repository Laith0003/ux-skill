---
id: breakpoints-are-reference-values
title: Breakpoints are reference values, and type does not change by breakpoint
status: active
areas: [layout, type, output]
supersedes: null
superseded_by: null
---

# Breakpoints are reference values, and type does not change by breakpoint

## Context

CSS custom properties cannot be read inside a media query, so a breakpoint token cannot drive the query that uses it. Type scales are often remapped per breakpoint as well.

## Decision

layout.breakpoint.tablet, laptop and desktop are tokens for exporters and documentation; stylesheets copy their values into media queries. Columns, gutters and margins are named per tier so a stylesheet picks the right one inside each query. Type sizes are in rem and do not change by breakpoint. There is no phone breakpoint: the phone tier is every width below layout.breakpoint.tablet, and the layout audit checks reflow at 320 CSS px wide (WCAG 1.4.10).

## Why

Stating the limit honestly beats a token that looks usable in a query and silently is not. Rem sizes follow the reader's own default text size, which matters more than the viewport, and one size per style keeps the hierarchy checks exact.

## What it touches

layout.py, export.to_css, the handoff files for layout and type in the rule pack.

## Consequences

A stylesheet writes @media (min-width: 640px) with the value of layout.breakpoint.tablet and sets the tablet gutter inside it. A hero that should shrink on phones uses a smaller style on phones, not a responsive token.
