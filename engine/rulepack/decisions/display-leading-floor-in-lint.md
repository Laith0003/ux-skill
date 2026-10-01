---
id: display-leading-floor-in-lint
title: The lint holds a display line height to the least the engine builds for its size
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# The lint holds a display line height to the least the engine builds for its size

## Context

The engine sets a display style's line height from its size and the contrast axis: 1.12 at 40px, falling on a log scale to 1.0 for a muted brand or 0.92 for a bold one at 160px and above, with Arabic higher for the marks above and below the letters. A page written by hand, or by a generator with no system, can set a 120px headline at 0.85 and nothing reported it.

## Decision

display-line-height-under-floor reads a line height on a style of 40px and up (a declaration, the font shorthand, or Tailwind text and leading classes on one element) and reports it when it sits under typography.display_leading_floor for the size: the engine's leading at full contrast, never under MIN_DISPLAY_LEADING. A style in an Arabic context (a selector for lang ar, fa, ur or he, or dir rtl, an Arabic face, or a page whose html element says so) is held ARABIC_DISPLAY_GAP (0.15) higher. When the page carries its own system, a line height its tokens define passes, and a var() into the system is never judged. The rule is low severity: a tighter setting reads cramped well before lines collide.

## Why

No contrast setting of the engine builds a display under this floor, so a value under it was not chosen by any system the engine would make. The full-contrast end is the most lenient, which keeps the rule quiet on any value a loud brand could get. A foreign system decides its own leading; the lint keeps a page to it rather than to ours.

## What it touches

engine/foundations/typography.py (display_leading_floor); engine/linter/taste.py (display_leading_outside_floor, System.leadings); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/display-line-height-under-floor; tests/test_lint_display_leading.py.

## Consequences

Tailwind's leading-none on text-6xl (60px at 1.0, under 1.06) is reported; on text-9xl it passes. A display set in px line height is compared as a ratio of its size. Text under 40px is left to the reading line-height check.
