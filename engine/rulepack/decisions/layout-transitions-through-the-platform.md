---
id: layout-transitions-through-the-platform
title: A layout transition is flagged when it moves what sits beside it, and a disclosure may open its height through the platform
status: active
areas: [motion]
supersedes: layout-transitions-that-reflow
superseded_by: null
---

# A layout transition is flagged when it moves what sits beside it, and a disclosure may open its height through the platform

## Context

animating-layout-properties passed two moves that lay out nothing beside them: a moving indicator's inline size and a disclosure on grid-template-rows. The platform now opens a disclosure to its natural height directly: ::details-content is Baseline since 2025-09-16, and interpolate-size: allow-keywords or calc-size() let a height move to auto in Chromium, while other browsers open it at once with no move.

## Decision

The rule reports a transition on top, left, right, bottom, inset, margin, padding, height or block size, and on width or inline size in flow. It passes when the only layout property is width or inline size on a moving indicator: a selector that names an indicator, an underline, an ink bar, a highlight, a thumb or a selection, or an element taken out of flow with position absolute or fixed. It also passes when the only layout properties are height or block size and the move opens a disclosure through the platform: the selector styles ::details-content, or the selector names a disclosure (the details element, [open], aria-expanded, accordion, disclosure, collapse, expand) and either interpolate-size: allow-keywords reaches it (in its own block, on :root or html, or on an ancestor whose selector is a prefix of its own, since the property inherits) or a calc-size() open state styles the same element (the same first simple selector in the last compound). grid-template-rows is not one of the properties it reads, so a single disclosure opening on it passes.

## Why

The cost of a layout transition is the reflow of everything around it. An element out of flow and a single grid track change only themselves, and a platform disclosure is the same single track written the way the platform intends, with an instant open as its fallback.

## What it touches

engine/linter/taste.py (layout_transition_reflows, _platform_disclosure, _base, _opts_in_above); data/anti-patterns.json animating-layout-properties; commands/ux-lint.md; tests/lint_corpus/cases/animating-layout-properties.

## Consequences

`details::details-content { transition: block-size .24s }` passes, and so does `.accordion__panel { transition: height .24s }` on a page whose root sets interpolate-size. `.card { transition: height .3s }` fails even when the root or its own block sets interpolate-size, since a card is not a disclosure; `.product-details` is a class, not the details element; and `.sidebar.collapsed { transition: height .3s }` fails when only an unrelated element uses calc-size(). An indicator that also animates a margin fails, since the margin moves its neighbours.
