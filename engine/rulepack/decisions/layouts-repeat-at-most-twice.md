---
id: layouts-repeat-at-most-twice
title: A landing page uses one layout for at most two sections
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# A landing page uses one layout for at most two sections

## Context

A page built from the same section three times (a heading over three cards, again and again) reads as one section repeated. Nothing in the lint saw it.

## Decision

layout-family-repeated reads each section's tree of elements four levels deep, with headings, media, links and paragraphs as kinds, a run of the same item counted once, and words ignored. The third section with the same tree and every one after it are reported. A section of fewer than two levels is not compared, and docs pages and app surfaces are skipped.

## Why

Each section's layout should follow what it holds. Two sections may share a layout; a third makes the rhythm a loop.

## What it touches

engine/linter/taste.py (layout_family_repeated); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/layout-family-repeated and tests/lint_corpus/probes/taste.

## Consequences

Two card grids and a split pass; three card grids fail on the third. The count reads structure only, so two sections with the same tree and different words are the same family.
