---
id: page-regions
title: Layout tokens cover the page grid and its regions; panes belong to page patterns
status: superseded
areas: [layout, space]
supersedes: layout-scope
superseded_by: page-regions-by-tier
---

# Layout tokens cover the page grid and its regions; panes belong to page patterns

## Context

A page needs space between its regions and around its header, hero and footer. One region gap for every width leaves a phone with a screen of empty space between sections, and without region tokens every page invents its own. Panes of an application shell (navigation widths, side panels) depend on what they hold.

## Decision

Layout tokens cover the page grid (three breakpoints, four tiers, columns, gutters, inline margins, the container, two measures, the minimum target) and the page regions: layout.region-gap and layout.hero.padding-block per tier, growing with the viewport, and layout.header.padding-block and layout.footer.padding-block. All alias the spacing scale and take a smaller step under compact density. Panes and how they collapse stay page patterns that compose these tokens.

## Why

Regions exist on every page, so their spacing belongs in the system; a gap per tier keeps a phone page short and a desktop page open. Pane widths depend on content and stay out.

## What it touches

layout.REGION_GAP, HERO_PADDING, HEADER_PADDING, FOOTER_PADDING and the layout-regions check; space.region.gap, now the widest tier's value.

## Consequences

A landing page steps its section gap by breakpoint with media queries on the breakpoint values. A side panel is still sized in columns or by layout.measure.form.
