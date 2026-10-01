---
id: text-stays-in-its-box
title: The render check reports text that runs past its own box
status: active
areas: [layout, type]
supersedes: null
superseded_by: null
---

# The render check reports text that runs past its own box

## Context

A display headline in a narrow column can hold a word wider than the column. The word lies over the photo or the form beside it, yet the page does not scroll sideways, so the overflow check stayed silent.

## Decision

The render check measures every block of text (headings, paragraphs, list items, labels, cells and the rest, inline-block ones included) at each width it renders, by the line boxes of its own text: text in a descendant that is hidden, absolute, fixed or that clips or scrolls is left out. When that text runs more than 2px past the box's padding edge, the box's overflow is visible and no ancestor scrolls or clips it, text-overflows-its-box names the deepest such element, up to three per page, and not one the page-overflow check already named.

## Why

Text over other content cannot be read, and neither can the content under it. Measuring the rendered box is the only way to see it, since the width depends on the font, the column and the viewport together.

## What it touches

engine/render/core.py (the measure script and the rule); tests/test_lint_precision.py.

## Consequences

Pages with oversized display type in grid columns gain a high finding at the widths where the word does not fit.
