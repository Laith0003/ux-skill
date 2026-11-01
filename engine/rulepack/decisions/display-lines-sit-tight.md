---
id: display-lines-sit-tight
title: Every type style keeps a size, leading and tracking floor, and display lines sit tight but never collide
status: active
areas: [type]
supersedes: the-full-type-ladder
superseded_by: null
---

# Every type style keeps a size, leading and tracking floor, and display lines sit tight but never collide

## Context

The line-height floor failed every style at a line height of 1 or less, and the display leading ran 1.05 to 1.15. On 35 measured award pages the headline's line height was 1.0 at the median and 1.0 or tighter on 77 percent, as low as 0.87, with no link to how loud the brand was. A study of a popular skill's output found confident heads at 0.90 to 0.95.

## Decision

type-sizes: body is at least 16px and every other style at least 12px, in both directions; both floors are ours. reading-leading holds body, body-small, fine and code at a line height of 1.5 or more (decisions/reading-line-height.md). A display style whose leading follows its size (the display, its two voices, the hero, heading-1 and the figure) reads typography.display_leading at its own size: 1.12 at 40px and below, falling on a log scale to 1.0 for a muted brand and 0.92 for a bold one at 160px and above, and never under its face's clearance: the measured ink of the tallest ascender and the deepest descender, in em, plus 0.02, rounded up. Each such step has its own leading token, type.leading.latin.step-<n>, and the Arabic one sits 0.2 above it. line-height-floor: such a display style keeps 0.88 or more, our floor; every other style a line height above 1. display-clearance: a display style under 1 keeps its face's clearance. arabic-text: an Arabic display style sits at least 0.15 above its Latin one. reading-tracking, type-tracking-order and code-face are unchanged.

## Why

Large type sits tighter than small type, and the measured pages set it at 1.0 or below. The ink of the face, not a fixed number, says when two lines touch: a serif with long descenders needs about 1.0, a compact sans can go to 0.92. Arabic marks above and below need the extra room.

## What it touches

typography.DISPLAY_LEAD, DISPLAY_LEAD_PX, INK_GAP, MIN_DISPLAY_LEADING, ARABIC_DISPLAY_GAP, clearance, display_leading, lead_token, the line-height-floor, display-clearance and arabic-text checks; fonts.Face.ink and INK_SOURCE; guidance/type.md.

## Consequences

A generated set passes in both directions. An imported set whose hero sits at 0.9 in a face that needs 0.98 is told the face's clearance.
