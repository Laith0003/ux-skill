---
id: grade-lock-on-the-page
title: Every photograph on a rendered page sits within one grade
status: active
areas: [imagery]
supersedes: null
superseded_by: null
---

# Every photograph on a rendered page sits within one grade

## Context

The photo direction gives each system a grade (mean lightness, temperature and chroma) and a grade lock: how far any photo may sit from the page's own mean. A warm stock photo beside a cool studio shot breaks the page's look, and only the rendered page shows which photos it uses.

## Decision

On a page that carries the imagery.photo tokens, lint --render measures every raster image and background at least 120px on each side that is not a logo: its mean L*, b* and C*, drawn from the image file itself, so text and scrims over it do not count. imagery.grade_problems then reports each photo out of the spread of the page's mean, and a page mean outside the direction's ranges, as photo-grade-off, naming the photo and the fix.

## Why

One grade is what makes photos from different sources read as one set. The spread follows formality: a formal brand keeps them tighter.

## What it touches

engine/render/taste.py (page_checks, photo-grade-off); engine/foundations/imagery.py (grade_problems); commands/ux-lint.md; tests/test_render_taste.py.

## Consequences

Screenshots count as photographs, as they do in the brand gate; a product screen beside warm photographs may need a matching frame or tone. An image the check cannot read is not graded.
