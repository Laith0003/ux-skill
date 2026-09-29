---
id: press-scale-and-glide
title: A press scales a little and scrolling may glide, both by the motion axis, and neither runs under reduced motion
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# A press scales a little and scrolling may glide, both by the motion axis, and neither runs under reduced motion

## Context

A press confirmed a tap only through color. On measured award pages 79 percent ran inertial scroll, and only 35 percent shipped any reduced-motion rule.

## Decision

motion.press.scale is character.press_scale: 0.985 for a still, formal brand to 0.96 for a kinetic one (the motion axis held back by half the formality), and 1 under reduced motion. press-in-place holds it between 0.95 and 1, exactly 1 under reduced motion. motion.scroll is character.scroll_strength: 0 up to 0.6 on the motion axis, rising to 1 at motion 1, held back by half the formality, and 0 under reduced motion; reduced-scroll holds that 0 (WCAG 2.3.3 asks that motion from interaction can be turned off).

## Why

A small scale says the press landed without moving anything. Inertial scroll suits kinetic brands only, and it is motion from interaction, so reduced motion turns it off.

## What it touches

character.press_scale, SCROLL_FROM, scroll_strength; motion.PRESS_SCALE, the motion.press.scale and motion.scroll tokens, the press-in-place and reduced-scroll checks; guidance/motion.md.

## Consequences

A page scales a pressed control by var(--motion-press-scale) and runs inertial scroll only when var(--motion-scroll) is above 0.
