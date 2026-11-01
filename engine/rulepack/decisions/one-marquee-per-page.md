---
id: one-marquee-per-page
title: A page carries at most one marquee
status: active
areas: [motion, layout]
supersedes: null
superseded_by: null
---

# A page carries at most one marquee

## Context

A scrolling strip of logos or news moves on its own. Two of them compete with each other and with the text around them, and each needs a way to pause.

## Decision

marquee-more-than-one counts marquee elements, data-marquee and elements whose class names a marquee or ticker, a part of one (marquee__track) counted with it, and reports every one after the first.

## Why

One strip can carry a row of proof. More turn the page into motion the reader has to read around.

## What it touches

engine/linter/taste.py (marquee_more_than_one); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/marquee-more-than-one and tests/lint_corpus/probes/taste.

## Consequences

The marquee that stays still needs a pause control and a reduced-motion stop; the render check and infinite-animation-without-reduced-motion hold those.
