---
id: expressive-motion
title: Curves bend continuously, and decoration has one role that reduced motion removes
status: superseded
areas: [motion]
supersedes: null
superseded_by: motion-check-owners
---

# Curves bend continuously, and decoration has one role that reduced motion removes

## Context

Three bands of curves give every brief one of three feels, and with no role for decoration a lively brand either animates nothing or borrows an interaction role for a reveal on scroll.

## Decision

Every curve is interpolated, control point by control point, between a plain and a springy curve by character.overshoot: the motion axis, held back by formality (motion times one minus 0.6 formality). motion.expressive is the role for decoration (a section that reveals on scroll, a celebration): 300ms for a still brand to 800ms for a kinetic one, the expressive curve, and a travel of four steps. Under reduced motion it lasts 0ms and does not travel, which the expressive-removed check holds (WCAG 2.3.3).

## Why

A continuous curve lets two briefs one tenth apart feel slightly different instead of identical or a band apart. Giving decoration its own role keeps interaction roles honest and makes decoration the first thing reduced motion removes.

## What it touches

motion.PLAIN, SPRINGY, curves, ROLES (motion.expressive), EXPRESSIVE and the expressive-removed check; character.overshoot.

## Consequences

A lively playful brand's reveal overshoots; a formal brand at the same motion barely does. Pages use motion.expressive for scroll reveals and nothing else.
