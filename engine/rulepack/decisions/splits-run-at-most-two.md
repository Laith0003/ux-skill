---
id: splits-run-at-most-two
title: At most two media-and-text splits run in a row
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# At most two media-and-text splits run in a row

## Context

A picture beside text, then text beside a picture, then again: the zigzag is the layout a generator reaches for, and the third in a row loses the reader.

## Decision

split-sections-in-a-row finds sections that, past single wrappers, hold two parts, one with media and no heading, the other with a heading and no media. The third split in a row among sibling sections, and every one after it, are reported.

## Why

Two splits can pair two ideas. A third is the default pattern repeating; a full-width image, a grid, a quote or a band of figures between splits restores the rhythm.

## What it touches

engine/linter/taste.py (split_sections_in_a_row); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/split-sections-in-a-row and tests/lint_corpus/probes/taste.

## Consequences

Two splits, a grid and a split pass. Five splits in a row fail on the last three.
