---
id: high-contrast-borders
title: High contrast makes edges and the focus ring heavier
status: active
areas: [border]
supersedes: null
superseded_by: null
---

# High contrast makes edges and the focus ring heavier

## Context

High contrast that changes only colors leaves a 1px card edge and a 2px ring, which are hard to see for the people who turn it on.

## Decision

Border varies on the contrast axis. Under high contrast border.outline, border.emphasis, border.active and border.focus-ring.width alias the next wider step; border.separator and border.focus-ring.offset keep their width. The high-contrast-borders check keeps every edge at least as wide as at standard contrast, and the ring and outline wider.

## Why

Weight is as much a contrast cue as color. One pixel more keeps the hierarchy (outline, emphasis, ring) while making every edge easier to find.

## What it touches

border.HIGH_STEP and _heavier; modes.FOUNDATION_AXES for border; the border checks, which read the contrast axis.

## Consequences

tokens.css carries border overrides under the high contrast attribute and media query. A layout that depends on exact border widths reserves one more pixel.
