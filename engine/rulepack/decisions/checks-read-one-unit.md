---
id: checks-read-one-unit
title: Checks compare dimensions in px and durations in ms, and read scale steps by their number
status: active
areas: [space, radius, layout, border, elevation, motion, type]
supersedes: null
superseded_by: null
---

# Checks compare dimensions in px and durations in ms, and read scale steps by their number

## Context

An imported token set writes its values in the units its authors chose: a radius in rem, a border width of 0.0625rem, a duration in seconds, and a scale listed in any order. A check that reads the number beside the unit, or reads steps in file order, passes a broken set and fails a sound one.

## Decision

Every check converts a dimension with values.dimension_px and a duration with values.duration_ms before it compares anything. A rem reads at 16px (values.REM_PX), the browser default, and a second reads as 1000ms. The border whole-pixel check rounds the px value to four places before it tests for a whole number, so 0.0625rem reads as 1px. Scale checks read the numbered steps of a family (space.<n>, radius.<n>) sorted by the number, through foundation.numbered_steps, so space.10 sits after space.8 whatever order the file lists them in. A set with no direction axis reads as left to right in the motion checks.

## Why

A rule is about the size or the time a person meets, not about the unit a file writes it in. One conversion for every foundation keeps two checks from disagreeing about the same value. The step number says where a step sits; the file order says only where someone typed it.

## What it touches

values.REM_PX, dimension_px and duration_ms; foundation.is_step and numbered_steps; the _px and _ms readers in border, elevation, layout, motion, radius, space and typography; the border-whole-pixels, space-scale-order and radius-scale-order checks.

## Consequences

An imported set in rem passes or fails exactly as the same set in px. A check added later reads its values through dimension_px or duration_ms and never multiplies by 16 or 1000 itself.
