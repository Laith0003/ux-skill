---
id: color-budget-on-the-page
title: The rendered page keeps chromatic color within the system's budget
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# The rendered page keeps chromatic color within the system's budget

## Context

The system gives every brand a color budget, color.budget.chromatic (0.02 for a calm brand to 0.2 for a loud one, by energy) and color.budget.bands (0 to 0.5). A page built from it can still set every heading in the brand color or flood a calm page with bands, and nothing checked the page against the budget it was given.

## Decision

On a page that carries --color-budget-chromatic, lint --render measures two shares at 1280px: text characters in a chromatic color (OKLCH chroma 0.08 and up), and the interface area filled in one, painted on a 16px grid in document order, with images, video, canvas, SVG and background pictures left out. Text over color.budget.chromatic, or fill over it plus color.budget.bands, is reported as color-over-budget, with two points of slack. Colors of custom properties named for a status are left out, since they carry meaning.

## Why

A calm brand reads calm because almost nothing on it is saturated; a loud one spends a fifth of the page on color. The budget comes from the brand's energy, so the check follows the brand, and bands are how a loud page carries its rhythm.

## What it touches

engine/render/taste.py (page_checks, color-over-budget); engine/render/core.py; commands/ux-lint.md; tests/test_render_taste.py.

## Consequences

A page without the engine's tokens is not judged. A client's own flooded brand bands are allowed as far as the system's band share says.
