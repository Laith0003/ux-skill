---
id: loops-stop-under-reduced-motion
title: Every infinite animation stops under reduced motion
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# Every infinite animation stops under reduced motion

## Context

A loop that never ends (a marquee, a glow, a floating shape) keeps moving for a person who asked their system for less motion. Most measured award pages ship no reduced-motion rule at all.

## Decision

infinite-animation-without-reduced-motion reports an infinite animation unless it runs only under prefers-reduced-motion: no-preference (or not reduce), a reduced-motion query stops it (animation none, paused, one iteration or a duration of 10ms or less on its selector, a selector it matches, or every element), or it is a progress indicator. A loop declared inside a reduce query is reported: it runs only for people who asked for less motion. The render check confirms it on the rendered page and asks for a pause control on anything that moves on its own for more than five seconds beside other content, as 2.2.2 says.

## Why

Decoration that moves is optional; a person's setting is not.

## What it touches

engine/linter/taste.py (infinite_animation_unguarded); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/infinite-animation-without-reduced-motion and tests/lint_corpus/probes/taste/t6-loops.css.

## Consequences

A spinner keeps turning, since it reports progress. A global reduced-motion reset on every element covers every loop in the file.
