---
id: bare-sizes-read-as-px
title: A bare number whose name says it is a size is read as px, with a note
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# A bare number whose name says it is a size is read as px, with a note

## Context

Systems write sizes without a unit: --radius-md: 8 in a stylesheet that multiplies by 1px in calc(), borderRadius: {md: 8} in a resolved Tailwind theme, or a markdown row of radius.card and 12. The importers read such a value as a plain number with no word in the report, so a radius or a container width reached the checks as a number and the person was never told.

## Decision

The CSS, Tailwind theme and markdown importers read a bare number as px when a word of its name says it is a size: space, spacing, gap, padding, margin, inset, radius, rounded, corner, size, width, height, gutter, offset, blur, spread, indent, breakpoint, container or elevation, first in the name's order. A word that says the number is plain wins over them: line, leading, weight, opacity, z, index, ratio, scale, factor, alpha, order, count, flex, columns, level, layer, multiplier, stroke and the color quantities lightness, chroma, hue, saturation and temperature. Each such value gets one note that names the value, the word and the fix: write the unit, or the unit it has if it is not px. A name that holds letter or tracking never gets the px default: a bare letter spacing is as often em as px, so it is listed under Not read with the fix, write -0.02em or the unit it has. A bare 0 is 0px with no note. A unit a markdown column header or heading names still wins, and a bare duration with no unit anywhere is still not read, since a time has no default unit.

## Why

A length with no unit has one reading a browser or a design tool gives it, px, and the name says it is a length. Reading it with a note keeps the value in the checks and tells the owner exactly what was assumed and how to say otherwise, where a plain number would have been checked as nothing.

## What it touches

engine/io/values_in.py (SIZE_WORDS, UNITLESS_WORDS, size_word, bare_size_note); engine/io/css_in.py; engine/io/tailwind_in.py; engine/io/markdown_in.py; tests/io/test_css_in.py; tests/io/test_tailwind_in.py; tests/io/test_markdown_in.py.

## Consequences

A markdown row whose bare number names a size is read with a note instead of listed under Not read. A z-index kept under a name such as elevation-modal is read as px, and its note names that assumption so the owner can see it; a name that says level or layer keeps it a number. The engine's own stylesheets carry no bare number under a size name, so they read back exactly.
