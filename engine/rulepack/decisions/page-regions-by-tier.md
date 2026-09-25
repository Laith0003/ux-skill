---
id: page-regions-by-tier
title: Page regions are spaced per tier, and one alias follows the viewport
status: active
areas: [layout, space]
supersedes: page-regions
superseded_by: null
---

# Page regions are spaced per tier, and one alias follows the viewport

## Context

The region gap and the hero padding came as four flat properties per tier with nothing that picked the tier by width, so a page that read space.region.gap showed the desktop gap on a phone, and above mid density space.region.gap and layout.region-gap.desktop disagreed.

## Decision

Layout tokens cover the page grid (three breakpoints, four tiers, columns, gutters, inline margins, the container, two measures, the minimum target) and the page regions: layout.region-gap and layout.hero.padding-block per tier, growing with the viewport, and layout.header.padding-block and layout.footer.padding-block. All alias the spacing scale and take a smaller step under compact density. tokens.css gives each tiered role one alias, --layout-region-gap and --layout-hero-padding-block among them, that follows the viewport (decisions/layout-aliases.md). The desktop region gap takes space.region.gap's pair (32 units airy, 16 dense), so the two agree at every density. Panes and how they collapse stay page patterns that compose these tokens.

## Why

Regions exist on every page, so their spacing belongs in the system; a gap per tier keeps a phone page short and a desktop page open, and one property that follows the viewport means a page cannot pick the wrong tier by accident.

## What it touches

layout.REGION_GAP, HERO_PADDING, HEADER_PADDING, FOOTER_PADDING, RESPONSIVE, responsive_css and the layout-regions check; export.to_css; space.region.gap.

## Consequences

A landing page sets its section gap with var(--layout-region-gap) and its hero padding with var(--layout-hero-padding-block): 40px apart at mid density on a phone, the desktop value from 1280px. A side panel is still sized in columns or by layout.measure.form.
