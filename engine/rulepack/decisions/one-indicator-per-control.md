---
id: one-indicator-per-control
title: Navigation, tabs, segmented controls and menus move one shared indicator
status: active
areas: [motion, contracts]
supersedes: null
superseded_by: null
---

# Navigation, tabs, segmented controls and menus move one shared indicator

## Context

A selected tab or the current page in a header was marked by an underline drawn on each item, so a change of selection made one mark vanish and another appear. Measured interfaces move one mark between items, which shows where the selection went.

## Decision

nav, tabs, segmented-control and menu each have an indicator part bound to motion.indicator: it fades in the first time it appears (enter-duration and enter-curve), slides to the new item after that (transition-duration and transition-curve, on its inline position and size only), and snaps under reduced motion, where motion.indicator resolves to 0ms. Selection is still carried by aria-current, aria-selected or aria-checked and a non-color cue (weight or the indicator's edge), never by color alone. A disabled tab, segment or menu row stays visible with aria-disabled and its reason.

## Why

One mark that moves reads as one selection changing place. Fading in the first time avoids a slide from nowhere, and the snap under reduced motion keeps the meaning without the movement.

## What it touches

engine/contracts/seed/nav.yaml, tabs.yaml, segmented-control.yaml, menu.yaml; tests/contracts/test_state_motion.py.

## Consequences

Three new seed contracts ship. The indicator animates only its inline position and size, which the lint already allows on an indicator (layout-transitions-that-reflow).
