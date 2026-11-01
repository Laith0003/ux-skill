---
id: accent-text-on-every-ground
title: Accent text is measured against every ground it lands on
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Accent text is measured against every ground it lands on

## Context

An accent checked on white can fail on the off-white card, the tinted band or the sunken panel where the same link also sits: a blue that is 5.2:1 on white is about 3.5:1 on a light grey.

## Decision

lint --render finds every text in a color (OKLCH chroma 0.04 and up) at 1280px and measures it against the ground under it, the backgrounds of its ancestors composited on white. Under 4.5:1 is reported as accent-text-low-contrast, once per color and ground, naming both. Normal text under 4.5:1 cites 1.4.3. Large text (24px, or 18.66px bold) that reaches 3:1 meets 1.4.3, so the finding names 4.5:1 as the system's own floor for all text (no-large-text-relaxation); under 3:1 it cites 1.4.3 for large text. Text over a picture, a gradient or an overlay beside media is left to the scrim check.

## Why

Every text role is held to 4.5:1 on every surface it can sit on; the page is where the surfaces an accent meets are known.

## What it touches

engine/render/taste.py (page_checks, accent-text-low-contrast); commands/ux-lint.md; tests/test_render_taste.py.

## Consequences

A link color that fails on one card surface fails the page until the card's link role is used. Neutral text is left to the system's own contrast gate.
