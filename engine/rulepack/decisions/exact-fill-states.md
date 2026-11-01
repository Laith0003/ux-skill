---
id: exact-fill-states
title: Hover and pressed step away from the fill from where the fill sits in its ramp
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Hover and pressed step away from the fill from where the fill sits in its ramp

## Context

The primary fill is the exact brand color, which sits wherever the brand sits: a light brand is lighter than its ramp's step 500, which the ramp retunes into its band. Stepping hover and pressed from step 500 put them on the wrong side of such a fill or out of order: #FFD400 at lightness 0.88 got a hover at 0.83 and a pressed step at 0.87, so pressing moved back toward the resting color, and some states sat less than a just visible step from the fill.

## Decision

Hover and pressed step from the fill's own lightness. On each side of the fill, darker and lighter, the ramp's steps are taken nearest first, and a step is kept only when it sits at least 0.02 from the step before it in OKLab (the fill first) and further from the fill than that step. Hover and pressed are the first two kept steps in the conventional direction (darker in light, lighter in dark), then against it when the text on them needs it, then with a gap of two. Every fill group steps this way; for a fill that is a ramp step it gives the neighboring steps as before.

## Why

Hover and pressed tell a person the control is responding; a state that moves back toward the fill, or by less than a visible step, reads as no response. Walking from the fill's own lightness keeps the order true for every brand, and the distance rule makes each state visibly further from the fill than the one before.

## What it touches

color.JUST_VISIBLE, _side, _state_paths and _solve_group.

## Consequences

A light or dark brand whose exact color is off its ramp's step 500 gets states that start from the nearest step past it, so they can skip a step that sits too close. Across 504 brands and four contexts every state moves away from the fill in order, each at least 0.02 from it.
