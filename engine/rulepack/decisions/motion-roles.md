---
id: motion-roles
title: Motion has seven interaction roles and reduced motion is a mode
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# Motion has seven interaction roles and reduced motion is a mode

## Context

Motion systems often name an intent for every kind of change, including separate roles for emphasis and for pulling attention, and keep reduced-motion values in a parallel set of tokens.

## Decision

Motion has seven roles, each with a duration and a curve and, where something travels, a distance: press, reveal, dismiss, swap, expand, page and progress. Emphasis and attention are not roles; a change that must be noticed uses reveal or swap, and one that must interrupt uses a status banner or a dialog. Reduced motion is the motion axis: every role keeps its meaning with no travel, a gentle curve and at most 100ms, and the progress loop keeps its pace.

## Why

Seven roles cover arriving, leaving, replacing, growing, moving between pages, confirming a press and showing progress. A separate attention role invites motion that loops or pulses for its own sake. Modeling reduced motion as a mode gives it the same override, gate and CSS switch as dark mode, instead of a second token tree to keep in step.

## What it touches

motion.py ROLES and the reduced-travel, reduced-length, reduced-curve, dismiss-faster, press-in-place and progress checks; modes.AXES; CSS data-motion and prefers-reduced-motion.

## Consequences

A highlight is a swap. A notice that must be seen is a status banner, which does not move to be noticed. Code reads the same role in every mode; the mode switch does the rest.
