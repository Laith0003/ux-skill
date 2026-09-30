---
id: ink-text-keeps-its-alpha
title: Text in the ink color keeps an alpha of 0.7 or more unless the system has its value
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Text in the ink color keeps an alpha of 0.7 or more unless the system has its value

## Context

Muted text written as the ink at an alpha (rgba at 0.5, text-black/50, color-mix with transparent) takes its contrast from whatever ground it lands on. On white it may pass; on an off-white card or a band it drops to about 3.7:1, under 1.4.3's 4.5:1.

## Decision

text-ink-at-low-alpha reports a text color in a near-neutral ink (channels within 24 of each other) at an alpha under 0.7, written as rgba, an eight- or four-digit hex, color-mix with transparent, or a Tailwind ink with an opacity modifier. It passes when the color over white (dark ink) or black (light ink) is a color the page's own tokens define. Accent colors, backgrounds and borders are not judged here; the render check measures accent text against every ground it lands on.

## Why

A muted text role is a color checked on every surface it sits on. An alpha is a guess that holds on one.

## What it touches

engine/linter/taste.py (text_ink_at_low_alpha); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/text-ink-at-low-alpha and tests/lint_corpus/probes/taste/t5-ink.css.

## Consequences

A hairline drawn in ink at 8 percent passes, since it is not text. A system that defines its muted text as the flattened value keeps its literal.
