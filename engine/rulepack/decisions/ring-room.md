---
id: ring-room
title: The standard focus ring stops one step below the widest, so high contrast can widen it
status: active
areas: [border]
supersedes: null
superseded_by: null
---

# The standard focus ring stops one step below the widest, so high contrast can widen it

## Context

Two things widen the standard focus ring: a dramatic contrast axis (0.66 or more) takes it from 2px to 3px, and older or mixed-age readers add a pixel. Together they reached 4px, the widest border width, so the high contrast ring could not go one step heavier, the high-contrast-borders check failed, and every such brief built nothing.

## Decision

The standard ring is 2px, 3px on a dramatic contrast axis, plus the audience's extra pixel, and never more than the second widest width (3px). Under high contrast it is one step wider. When the contrast axis has already taken the ring to 3px, the age adds nothing at standard contrast, and the report says the ring stays 3px and is 4px under high contrast.

## Why

The high contrast ring must stay heavier than the standard one for the readers who turn high contrast on, and a build must never fail for an age and an axis that are both valid. A 3px ring is already the heaviest standard stroke, so the cap costs an older reader nothing they could find.

## What it touches

border.ring_px and roles; audience.effects, whose age line states the ring the build made at the axes.

## Consequences

Every age band builds at every contrast axis. An older reader on a dramatic brand gets the same 3px standard ring as any reader of it, and the 4px ring under high contrast.
