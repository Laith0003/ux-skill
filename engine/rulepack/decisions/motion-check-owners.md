---
id: motion-check-owners
title: Curves bend continuously, decoration leaves under reduced motion by our rule, and each motion property has one check
status: active
areas: [motion]
supersedes: expressive-motion
superseded_by: null
---

# Curves bend continuously, decoration leaves under reduced motion by our rule, and each motion property has one check

## Context

The expressive role came with a check, expressive-removed, that cited WCAG 2.3.3 for a 0ms rule. 2.3.3 asks that motion animation triggered by interaction can be turned off; it sets no duration, and a fade is outside it. The same check also reported the role's travel, which reduced-travel already reports, and reduced-length asked to cap the role at 100ms while expressive-removed asked for 0ms, so one broken role gave several findings whose fixes disagreed. A reduced duration past the cap and longer than standard gave two findings as well.

## Decision

Every curve is interpolated, control point by control point, between a plain and a springy curve by character.overshoot: the motion axis, held back by formality (motion times one minus 0.6 formality). motion.expressive is the role for decoration, a section that reveals on scroll: 300ms for a still brand to 800ms for a kinetic one, the expressive curve, and a travel of four travel units (motion.distance.3). Under reduced motion it lasts 0ms and does not travel.

Each motion property has one owner check. reduced-travel owns every distance under reduced motion, the expressive one included (WCAG 2.3.3). expressive-removed owns the expressive duration under reduced motion; removing decoration is our rule and the check cites no WCAG criterion. progress-keeps-pace owns the loop's duration. reduced-length owns every other one-shot duration past 100ms, and the cap it names is the lower of 100ms and the role's standard length in the same direction, so its one fix also keeps reduced motion from lengthening the move; reduced-not-longer and dismiss-faster do not repeat it.

## Why

A continuous curve lets two briefs one tenth apart feel slightly different. One owner per property gives a broken role one finding with one fix, and a check that cites WCAG only for what the criterion says keeps our own rules from reading as conformance requirements.

## What it touches

motion.PLAIN, SPRINGY, curves, ROLES (motion.expressive), EXPRESSIVE, OWN_REDUCED_DURATION and the reduced-length, reduced-not-longer, dismiss-faster and expressive-removed checks; character.overshoot; guidance/motion.md.

## Consequences

A lively playful brand's reveal overshoots; a formal brand at the same motion barely does. Pages use motion.expressive for decoration only, such as scroll reveals. A reduced-motion finding names the one change that clears it.
