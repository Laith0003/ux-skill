---
id: whole-pixel-borders
title: Border widths are whole pixels
status: active
areas: [border]
supersedes: null
superseded_by: null
---

# Border widths are whole pixels

## Context

A half-pixel stroke looks fine on dense screens and disappears or blurs on standard ones.

## Decision

Border widths are 0, 1, 2, 3 and 4px. There is no hairline width. A lighter separation uses a quieter color (color.line.subtle), not a thinner stroke.

## Why

A stroke that vanishes on some screens is not a structural edge. Color can be lightened without that risk, and the color foundation keeps the quiet line distinct from the surfaces it divides.

## What it touches

border.WIDTHS and the border-whole-pixels check.

## Consequences

An imported system with a 0.5px role fails the build with a message naming the role; the fix is a 1px width and a quieter color.
