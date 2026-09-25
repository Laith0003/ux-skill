---
id: display-and-navigation-contracts
title: Chips, badges, links, navigation, progress and tables have contracts
status: active
areas: [contracts]
supersedes: null
superseded_by: null
---

# Chips, badges, links, navigation, progress and tables have contracts

## Context

Pages built from the system hand-rolled tags, status badges, links, the header, progress bars and tables, and a table had no phone behavior, no header fill and no stripe.

## Decision

Six contracts ship at experimental: chip (filter and input chips, chosen with a check and a heavier edge), badge (read-only status, brand or neutral labels with an icon per status), link (always underlined in color.line.accent, standalone links meet the target size), nav (the header with the logo in color.logo, the current page marked with aria-current and the selected underline, collapsing to a menu button below the tablet breakpoint), progress (a bar in the selected line color on a sunken track, a spinner when the share is unknown, the value in words), and table (a sunken header, optional stripes in color.surface.stripe, a highlighted column in the brand tint with its accent edge, cell padding from the table spacing roles, and a phone layout that scrolls sideways with a fixed first column or shows rows as cards).

## Why

Contracts for the parts every landing and product page has keep the whole page on the system, not only its buttons and fields.

## What it touches

engine/contracts/seed/chip.yaml, badge.yaml, link.yaml, nav.yaml, progress.yaml, table.yaml.

## Consequences

There are eighteen seed contracts. A link has no disabled state; it is present or absent.
