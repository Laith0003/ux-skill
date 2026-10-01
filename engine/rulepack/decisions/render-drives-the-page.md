---
id: render-drives-the-page
title: The render check drives the page with its motion running
status: active
areas: [motion, contracts]
supersedes: null
superseded_by: null
---

# The render check drives the page with its motion running

## Context

The render check froze motion to measure layout, so it could not see a focus ring cut off by a scroller, a hover that answers late on a slow curve, focus lost after Escape, or a press that still scales with reduced motion set.

## Decision

lint --render adds a pass that does not freeze motion, at 1280 and 390. It tabs through the first 30 focusables and reports one whose focused style does not differ from its resting style (focus-ring-missing, as 2.4.7 asks) or whose ring an ancestor that clips its overflow cuts off (focus-ring-clipped). At 1280 it hovers and presses the first six distinct buttons, chips and cards and samples transform, background color and opacity each frame; half the change later than 70ms plus one frame is state-answers-late. It opens each button with aria-haspopup, presses Escape and reports focus that does not return to it (focus-lost-after-escape). With reduced motion set it presses again and reports any transform (press-moves-under-reduced-motion); loops under reduced motion stay with the existing check.

## Why

These are things a person meets only by using the page. Driving it the way a keyboard or pointer user would finds them where reading the source cannot.

## What it touches

engine/render/interact.py; engine/render/core.py; tests/test_lint_probes.py.

## Consequences

A render run takes longer: about two seconds more per page. Controls the page covers or moves away while driven are skipped, not reported.
