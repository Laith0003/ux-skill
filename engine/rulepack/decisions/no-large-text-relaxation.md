---
id: no-large-text-relaxation
title: Every text style is held to the body text minimum
status: active
areas: [color, type]
supersedes: null
superseded_by: null
---

# Every text style is held to the body text minimum

## Context

WCAG lets large text (24px and up, or about 18.7px bold and up) meet 3:1 instead of 4.5:1. Using it means classifying every style at every size, in both scripts, and pairing each class with its own minimum.

## Decision

Every text role is held to 4.5:1 (7:1 under high contrast) on every surface it can sit on, whatever size it is set in. There is no large-text class.

## Why

Sizes change with the reader's default text size, with direction (the Arabic face is larger) and with the breakpoint a page chooses; a classification made on the tokens can be wrong on the page. One minimum for all text is simpler to check and never lets a heading fall short on a page where it renders smaller than planned.

## What it touches

color.TEXT_ROLES and build_pairings; typography sizes in rem.

## Consequences

Headings get no contrast discount. A contract whose text is always large may declare a lower floor for it as a system floor with its own high value, and say why; it never cites 1.4.3 for a ratio other than 4.5:1.
