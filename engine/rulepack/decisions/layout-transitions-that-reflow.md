---
id: layout-transitions-that-reflow
title: A layout transition is flagged when it moves what sits beside it
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# A layout transition is flagged when it moves what sits beside it

## Context

animating-layout-properties flagged every transition on a size or position. Two moves the interaction guidance asks for lay out nothing beside them: a shared indicator that slides and changes its inline size under the current tab or menu row, and a disclosure that opens by animating grid-template-rows from 0fr to 1fr.

## Decision

The rule still reports a transition on top, left, right, bottom, inset, margin, padding, height or block size, and on width or inline size in flow. It passes when the only layout property is width or inline size on a moving indicator: a selector that names an indicator, an underline, an ink bar, a highlight, a thumb or a selection, or an element taken out of flow with position absolute or fixed. grid-template-rows is not one of the properties it reads, so a single disclosure opening on it passes.

## Why

The cost of a layout transition is the reflow of everything around it. An element out of flow and a single grid track change only themselves.

## What it touches

engine/linter/taste.py (layout_transition_reflows); data/anti-patterns.json animating-layout-properties; commands/ux-lint.md; tests/lint_corpus/cases/animating-layout-properties.

## Consequences

`.answer { transition: grid-template-rows .3s }` passes and `.card { transition: height .3s }` fails. An indicator that also animates a margin fails, since the margin moves its neighbours.
