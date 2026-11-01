---
id: layout-aliases
title: Breakpoints are reference values, tokens.css switches the tiered roles, and type does not change by breakpoint
status: superseded
areas: [layout, output]
supersedes: breakpoints-are-reference-values
superseded_by: type-steps-down-on-phones
---

# Breakpoints are reference values, tokens.css switches the tiered roles, and type does not change by breakpoint

## Context

CSS custom properties cannot be read inside a media query, so a breakpoint token cannot drive the query that uses it. With the tiers named per role and nothing to switch between them, every page had to copy the breakpoints into its own media queries, and a page that did not got one tier at every width.

## Decision

layout.breakpoint.tablet, laptop and desktop stay tokens for exporters and documentation. tokens.css ends with one alias per tiered role in layout.RESPONSIVE: --layout-columns, --layout-gutter, --layout-margin-inline, --layout-region-gap and --layout-hero-padding-block. Each takes the phone value at :root and the tablet, laptop and desktop values under @media (min-width) with the breakpoints' literal px (640, 1024 and 1280), so a page reads one property. A density override reaches the alias through var(). Type sizes are in rem and do not change by breakpoint. There is no phone breakpoint: the phone tier is every width below layout.breakpoint.tablet, and the layout audit checks reflow at 320 CSS px wide (WCAG 1.4.10).

## Why

The engine knows the breakpoints, so it writes the queries once instead of every page copying them. Rem sizes follow the reader's own default text size, which matters more than the viewport, and one size per style keeps the hierarchy checks exact.

## What it touches

layout.RESPONSIVE and responsive_css, export.to_css, the handoff files for layout and type in the rule pack.

## Consequences

A stylesheet writes grid-template-columns: repeat(var(--layout-columns), 1fr) and gap: var(--layout-region-gap) and never copies a breakpoint for these roles; a query of its own for anything else still copies the value of layout.breakpoint.tablet. A hero that should shrink on phones uses a smaller style on phones, not a responsive type token.
