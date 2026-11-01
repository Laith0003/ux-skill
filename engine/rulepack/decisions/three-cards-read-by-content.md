---
id: three-cards-read-by-content
title: Three equal cards fire only when every card holds just an icon, a title and a line
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# Three equal cards fire only when every card holds just an icon, a title and a line

## Context

three-equal-card-grid and grid-cols-3-1fr-default fired on any three equal columns. Equal columns whose cards each carry their own photograph or product fragment are a fair layout; what reads as generated is three cards with nothing in them but an icon and words.

## Decision

three-equal-card-grid reports a grid only when every card holds just an icon, a title and a line or two of text; a card with its own image, video, figure or large SVG, or a list, table, form or quote, passes. A small SVG icon or an icon image under 100px is not media. grid-cols-3-1fr-default finds the markup its rule styles, in the same file or a page that loads the stylesheet, and passes when each cell carries its own media or richer content; a stylesheet with no markup to read still fires.

## Why

The fingerprint is empty sameness, not the number of columns.

## What it touches

engine/linter/taste.py (cards_hold_only_icon_title_line, grid_holds_plain_cards); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases for both rules.

## Consequences

Three cards each with a different photograph pass. Three icon cards still fail, whatever their words.
