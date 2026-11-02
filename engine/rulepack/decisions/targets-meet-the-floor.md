---
id: targets-meet-the-floor
title: Every target meets the 24px floor, and 44px is the touch default
status: active
areas: [layout, contracts]
supersedes: null
superseded_by: null
---

# Every target meets the 24px floor, and 44px is the touch default

## Context

Toolbars of small icons and stacked footer links are where generated pages put controls a thumb cannot hit. The guides disagree on the number: 2.5.8 sets 24 CSS pixels with a spacing exception, 2.5.5 names 44, and platform guides ask 44pt or 48dp.

## Decision

The floor is 2.5.8: a target is at least 24 by 24 CSS pixels, or a 24px circle centred on it meets no other target and no other small target's circle. lint --render reports target-too-small at every width, naming each control; a link inside a sentence, a checkbox or radio the browser draws unstyled, and a disabled, inert or hidden control pass. The default the system designs to for touch is 44px, the size 2.5.5 names.

## Why

A floor the page is held to must be one the criterion sets; the larger size is the target worth designing to, not a failure to report.

## What it touches

engine/render/core.py (the target block); references/foundations/accessibility.md; commands/ux-lint.md; tests/test_render_targets.py.

## Consequences

A 32px icon button with 8px between neighbours passes the floor and still reads as small against the touch default.
