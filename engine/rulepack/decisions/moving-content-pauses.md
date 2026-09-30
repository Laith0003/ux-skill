---
id: moving-content-pauses
title: Anything that moves on its own stops under reduced motion and can be paused
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# Anything that moves on its own stops under reduced motion and can be paused

## Context

Marquees, beams and floating shapes loop forever. Many run with reduced motion set, and few offer a way to stop them, which 2.2.2 asks for when content moves on its own for more than five seconds beside other content.

## Decision

lint --render loads each page twice without freezing it. With reduced motion set, any animation that runs forever and is not a progress indicator is reported as infinite-animation-under-reduced-motion. With no motion preference, any animation that runs on its own for more than five seconds beside other content is reported as moving-content-without-pause unless the page has a control that pauses it: a button or toggle named pause, stop or play, or one whose aria-controls names the moving region.

## Why

A person who asked for less motion gets none that is decoration, and everyone can stop what moves while they read.

## What it touches

engine/render/taste.py (motion_checks); engine/render/core.py; commands/ux-lint.md; tests/test_render_taste.py.

## Consequences

A spinner or a progress bar keeps moving. The static rule infinite-animation-without-reduced-motion catches the same loop in the source before a page is rendered.
