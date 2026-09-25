---
id: the-full-type-ladder
title: Every type style keeps a size, leading and tracking floor, and code keeps a fixed width
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# Every type style keeps a size, leading and tracking floor, and code keeps a fixed width

## Context

The type checks held body, body-small and fine, and left the rest of the ladder open: an imported set could set a label at 10px, a heading at a line height of 0.9, a small heading tracked tighter than the one above it, code at a line height meant for headings, or a mono face list that falls back to a proportional font.

## Decision

type-sizes: body is at least 16px and every other style at least 12px, in both directions; both floors are ours, since WCAG sets no minimum text size. reading-leading holds body, body-small, fine and code at a line height of 1.5 or more (decisions/reading-line-height.md). line-height-floor: every style's line height is above 1. reading-tracking: the reading styles and type.text.ui never tighten letter spacing. type-tracking-order: from display down to body, no style tracks tighter than the larger style above it; under right to left in a set with an Arabic face, arabic-text holds every style at 0 and owns tracking there. code-face: the mono face list ends in ui-monospace or monospace. Headings and interface labels may be tighter than 1.5 but never 1 or less.

## Why

At a line height of 1 or less, ascenders and descenders of neighbouring lines touch. Tracking tightens with size, so a smaller style tighter than a larger one inverts the ladder. Code aligns by column, which needs a fixed width even when the named face fails to load.

## What it touches

typography.ROLES, READING, TRACKING_ROLES, HIERARCHY and MONOSPACE; the type-sizes, reading-tracking, type-tracking-order, line-height-floor and code-face checks; guidance/type.md.

## Consequences

A generated set passes in both directions. An imported mono stack that ends in a named face fails and is told to end it with ui-monospace or monospace.
