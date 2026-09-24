---
id: unsigned-distances
title: Travel distances are unsigned, and one sign follows the reading direction
status: active
areas: [motion, direction]
supersedes: null
superseded_by: null
---

# Travel distances are unsigned, and one sign follows the reading direction

## Context

A panel that slides in from the start edge moves right in a left-to-right page and left in a right-to-left one. Signed distances per direction would double every travel token.

## Decision

motion.<role>.distance values are positive lengths with no direction. motion.inline-sign is 1 under dir="ltr" and -1 under dir="rtl"; horizontal travel multiplies the distance by it. Vertical travel does not use the sign.

## Why

One sign token mirrors every horizontal move at once, and a check holds it to the reading direction in every motion mode. Distances stay comparable across roles because none is negative.

## What it touches

motion.py distance and sign primitives, the mirrored-motion check, the handoff file for motion in the rule pack.

## Consequences

Code writes translateX(calc(var(--motion-reveal-distance) * var(--motion-inline-sign))). A move that must not mirror, such as a progress indicator tied to a timeline, leaves the sign out.
