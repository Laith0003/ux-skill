---
id: layout-bounds
title: Gutters, margins, measures and the container stay inside our bounds at every tier
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# Gutters, margins, measures and the container stay inside our bounds at every tier

## Context

The layout checks held the order of breakpoints and regions and the widest reading line, but an imported set could still shrink its gutters as the screen widened, set a 2px margin, make the reading column a few words wide, set a form wider than any reading line, or cap the container below the width of its own text.

## Decision

Five checks read every density. layout-grid-order: gutters and inline margins never shrink as the tier widens. layout-gutter-floor: every gutter and inline margin is at least 8px (layout.MIN_GUTTER_PX, two 4px space units). text-measure-floor: the reading measure is at least 30rem (layout.MIN_TEXT_MEASURE_REM). form-measure: the form measure is at most 40rem, the ceiling text-measure holds reading text to. container-bounds: the container is at least 320px and at least as wide as the reading measure. Each floor and ceiling here is ours; WCAG sets none of them. Each failure names the role, its value and the step or width to point it at.

## Why

A wider screen with tighter gutters reads as a mistake. Below 8px, content touches the screen edge and its neighbours. Below 30rem, a reading column breaks every few words, and a form is read like a line of text, so it keeps the same ceiling. A container narrower than its reading measure cannot hold the column it exists for.

## What it touches

layout.MIN_GUTTER_PX, MIN_TEXT_MEASURE_REM, MAX_TEXT_MEASURE_REM and REFLOW_PX; the layout-grid-order, layout-gutter-floor, text-measure-floor, form-measure and container-bounds checks; guidance/layout.md.

## Consequences

A generated set passes at every density. An imported set that breaks a bound fails with the role named, and the gutter fix names the smallest space step at 8px or more that the set has.
