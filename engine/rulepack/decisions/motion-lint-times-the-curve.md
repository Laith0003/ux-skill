---
id: motion-lint-times-the-curve
title: The lint times a transition by when it answers, from its curve
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# The lint times a transition by when it answers, from its curve

## Context

A cap on nominal duration (500ms for a transition, 800ms for an animation, 300ms as a default) judges the wrong thing. A long move on a strong out curve is half done in 70ms and feels immediate; a 400ms ease-in-out is only half done at 200ms and feels slow. The engine's own roles are checked by when they answer (moves-answer-at-once), and the lint said otherwise.

## Decision

transition-duration-500ms-or-longer, animation-duration-too-long and timing-300ms-default compute the time to half and nine tenths of the travel with motion.settle_ms from the declared curve. A transition whose rule, or another rule for the same element, is a hover, focus, press or state is a response: half within 70ms and nine tenths within 220ms. Any other transition, and every animation, is an entrance: half within 140ms. A curve that is not declared, a var() the page does not define, steps() or linear() falls back to the nominal cap; an ease-in exit is held to the cap only, since it accelerates by design. A duration the page's system defines passes with the system's curve or with none. The transition rule reads 400ms and up; the 300ms rule reads exactly 300ms and never a delay. Tailwind duration classes read the curve from ease classes on the same element.

## Why

What a person feels is how soon the screen answers, and the curve decides that more than the length.

## What it touches

engine/linter/taste.py (answers, transition_answers_late, animation_answers_late, default_300_answers_late); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases for the three rules and tests/lint_corpus/probes/taste/t4-motion.css.

## Consequences

`transition: transform .62s cubic-bezier(.2, 1, .25, 1)` on a hover passes and `transition: background-color .4s ease-in-out` fails. An undeclared curve is read as undecided, even though the browser plays ease.
