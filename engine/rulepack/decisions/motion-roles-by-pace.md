---
id: motion-roles-by-pace
title: Motion has ten interaction roles, formality slows them, energy speeds them, and curves are long-tail ease-outs
status: active
areas: [motion]
supersedes: motion-roles
superseded_by: null
---

# Motion has ten interaction roles, formality slows them, energy speeds them, and curves are long-tail ease-outs

## Context

Interaction moves ran 150 to 300ms by the motion axis alone, the plain out curve was CSS ease, and nothing covered a change of state in place, a sliding indicator or an entrance as the page is read. On 35 measured award pages the per-site median transition was 400ms (the middle half 300 to 444ms), 500ms or more on 43 percent; formal brands moved slower and loud ones snappier, on strong ease-out curves. A study of a popular skill's output found entrances of 500 to 900ms on long-tail curves, and a study of a component site found states at 150 to 240ms.

## Decision

Motion has ten interaction roles, each with a duration and a curve and, where something travels, a distance: press, state, reveal, dismiss, swap, expand, page, indicator, arrive and progress; emphasis and attention are not roles. character.motion_pace is 0.5 plus 0.6 times (formality minus 0.5) minus 0.6 times (energy minus 0.5): press (100 to 150ms), reveal (200 to 450ms), dismiss (150 to 350ms), swap (200 to 450ms), expand (250 to 500ms) and page (300 to 600ms) run between their ends by it. state runs 150 to 240ms by the motion axis held back by formality, indicator 200 to 280ms and progress 1200 to 800ms by the motion axis, and arrive 350 to 800ms by the motion axis and formality. Every one-shot role but dismiss takes the out curve, whose plain end is [0.2, 0.8, 0.2, 1], a long-tail ease-out that is nine tenths done at 40 percent of its time; the expressive curve's plain end is [0.16, 1, 0.3, 1]; character.overshoot still bends each toward its springy end. Durations snap to 0, 50, 100, 150, 200, 240, 250, 280, 300, 350, 400, 450, 500, 600, 700, 800 and 1200ms. Reduced motion is the motion axis: every role keeps its meaning with no travel, every one-shot role takes a gentle curve and at most 100ms, the indicator snaps (0ms), arrive is a brief fade, and the progress loop keeps its standard duration and linear curve.

## Why

A long duration on a strong ease-out answers at once and settles slowly, which reads calm, not slow. Tying the pace to formality and energy puts formal brands on unhurried moves and loud ones on quick, springy ones, continuously.

## What it touches

motion.ROLES, DURATIONS_MS, PLAIN, REMOVED, duration_ms; character.motion_pace; guidance/motion.md.

## Consequences

A page binds hover, selected and pressed transitions to motion.state, a sliding marker to motion.indicator and scroll entrances to motion.arrive; decoration stays on motion.expressive.
