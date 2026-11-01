---
id: photograph-required-in-lint
title: The lint requires a photograph on a landing page unless the brand forbids photography
status: active
areas: [imagery]
supersedes: null
superseded_by: null
---

# The lint requires a photograph on a landing page unless the brand forbids photography

## Context

imagery-mandatory-missing passed a page whose only picture was a large SVG illustration, while the brand gate and the photo direction require a photograph. The two checks disagreed on the same page.

## Decision

The rule reads the page the way the brand gate does (brand.fidelity.score_imagery): a raster image, a picture, a video or a raster background that is not the logo is a photograph. An illustration, icons or the logo alone fire. An iframe, an element with role="img" that is not an SVG and an SVG image of a raster file pass, since their content cannot be read. A page passes with none only when a brand.md beside it or above it forbids photography. Pages that are not landing pages are skipped as before, and so is a layout template whose main is a slot the pages fill.

## Why

Photographs carry the brand's world; drawn art and product fragments add to them and never replace them. A ban on a kind of photo narrows the kinds and never removes photography.

## What it touches

engine/linter/taste.py (page_needs_photograph); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/imagery-mandatory-missing; tests/test_linter.py.

## Consequences

A page that ships only a hero illustration fails until a photograph joins it. A client whose brand rules forbid photography records it in brand.md and passes.
