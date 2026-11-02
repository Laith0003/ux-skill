---
id: all-text-measured-as-seen
title: Every text on the rendered page is measured against the ground the visitor sees
status: active
areas: [color]
supersedes: accent-text-on-every-ground
superseded_by: null
---

# Every text on the rendered page is measured against the ground the visitor sees

## Context

A page assembled by hand or by a model can set any text in any color, outside the roles the gate checked. Scroll-led pages also paint their grounds with script: a section is transparent at rest and a dark ground arrives only when it scrolls into view, so text measured at rest is measured on a ground no one sees.

## Decision

lint --render reads every visible text at 1280px. The page is scrolled instantly a step at a time; each text block is read once it has risen into the upper half of the screen and again one step later, and is reported only when it fails both readings, so a ground caught mid fade is not. Text in a color (OKLCH chroma 0.04 and up) is held to 4.5:1 as accent-text-low-contrast, the system's own floor for all text (no-large-text-relaxation). Neutral text is held to what 1.4.3 asks, 4.5:1 or 3:1 at 24px or 18.66px bold, as text-low-contrast; an inactive control and text hidden from assistive technology are left out, as 1.4.3 leaves them out. Each color and ground pair is reported once. Text over a picture, a gradient or an overlay beside media is left to the scrim check.

## Why

The gate proves the roles; only the page shows which colors were used and on which ground. Reading the screen the visitor sees keeps the check honest on pages that change their ground as they scroll.

## What it touches

engine/render/taste.py (page_checks, the scroll pass); commands/ux-lint.md; tests/test_render_text_contrast.py and tests/test_render_taste.py.

## Consequences

A muted grey that clears 4.5:1 on the page ground but not on a card fails on the card. A page whose ground fades between sections is measured at its settled colors.
