---
id: high-contrast-weights
title: High contrast sets text one weight heavier
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# High contrast sets text one weight heavier

## Context

High contrast that changes colors only leaves thin strokes at small sizes, which is where low vision readers lose letters first.

## Decision

Type varies on the contrast axis. Under high contrast every style set in the text or mono face is one weight heavier (regular 400 to 500, medium 500 to 600, headings up to 700), never past what the face and its Arabic partner ship. Display styles keep their weight. The high-contrast-weights check refuses a style that is lighter under high contrast.

## Why

A heavier stroke raises the contrast of each letter against its ground without changing the size or the layout.

## What it touches

typography._heavier, the contrast:high overrides of the text styles; modes.FOUNDATION_AXES for type.

## Consequences

tokens.css carries type weight overrides under the high contrast attribute and media query. The page loads the heavier weights too.
