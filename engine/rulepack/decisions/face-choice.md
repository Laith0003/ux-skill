---
id: face-choice
title: The axes choose each face from a catalog by distance, never by keyword
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# The axes choose each face from a catalog by distance, never by keyword

## Context

A face picked by a keyword table (an industry, a tone word) repeats across every brief that shares the word, and three bands of type personality give every brief one of three looks.

## Decision

engine/foundations/fonts.py holds a small catalog of faces under the SIL Open Font License, each with metrics measured from its files, the weights it ships, its Arabic partner and a place on formality, warmth, roundness, type personality and contrast. For each role the build takes the face nearest the brief's place by weighted distance (type personality counts most for text and mono, formality for display), ties broken by name; the display face is never the text face.

## Why

A distance over the axes changes the face whenever the brief's character changes enough, with no table to maintain per industry. Measured metrics let the page load a matched fallback, so the choice costs no layout shift.

## What it touches

fonts.FACES, WEIGHTS, choose, nearest; typography.generate_type.

## Consequences

Adding a face means adding its measured metrics and its place; the catalog stays small so each face is distinct.
