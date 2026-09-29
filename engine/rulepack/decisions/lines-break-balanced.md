---
id: lines-break-balanced
title: Headlines balance their lines and running text avoids a last word alone
status: active
areas: [type, output]
supersedes: null
superseded_by: null
---

# Headlines balance their lines and running text avoids a last word alone

## Context

Headlines that break by the browser's default leave one long line and one short one, and paragraphs often end on a single word.

## Decision

tokens.css writes --<role>-text-wrap beside each type role in typography.WRAP: balance for every style in the display face, heading-2 and heading-3, pretty for body, body-small and fine. A page sets text-wrap from it.

## Why

Balanced lines read as one shape at display sizes; a pretty break keeps the last line of a paragraph from standing alone. Both only change where lines break.

## What it touches

typography.WRAP; export._lines; guidance/type.md.

## Consequences

The one-line and three-line headline limits are measured with balance on.
