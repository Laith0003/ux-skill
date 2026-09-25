---
id: code-and-table-colors
title: Code blocks and tables have their own surfaces
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Code blocks and tables have their own surfaces

## Context

Syntax colors drawn from the text roles are measured against the page, not against the block they sit on, and a table stripe borrowed from the sunken surface reads as recessed.

## Decision

color.surface.code is the code block's background, one step off the page in light and a recess in dark. Six syntax roles (plain, keyword, string, number, function, comment) are paired with it at 4.5:1 (WCAG 1.4.3), 7:1 under high contrast. color.surface.stripe marks alternate table rows one step off the card, and every text role is paired with it.

## Why

Measuring syntax colors on the surface they sit on is the only measurement that means anything. A stripe that is its own role can stay light without implying depth.

## What it touches

color.SEMANTIC, HIGH_CONTRAST, SYNTAX_ROLES, TEXT_SURFACES; the table contract.

## Consequences

Syntax colors reuse the status hues and the brand, so a code block reads as part of the system.
