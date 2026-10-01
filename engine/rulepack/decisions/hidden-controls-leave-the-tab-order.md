---
id: hidden-controls-leave-the-tab-order
title: A hidden control leaves the tab order, an exit runs to its end, and a theme switch does not animate the page
status: active
areas: [motion, contracts]
supersedes: null
superseded_by: null
---

# A hidden control leaves the tab order, an exit runs to its end, and a theme switch does not animate the page

## Context

Three ways a component's exit goes wrong were left to review. A closed menu faded to opacity 0 keeps its links in the tab order. A popover that sets display: none in its closed state loses its exit at the first frame. A transition on every element's colors turns a theme switch into a slow wash across the page.

## Decision

Three lint rules. focusable-at-opacity-zero reports opacity 0 on a control, or a panel holding one, with no visibility: hidden, display: none, inert or hidden companion; a reveal on hover is left to hover-only-card-actions and a reveal on its own focus (a skip link) passes. exit-cut-by-display-none reports a closed state that sets display: none while the open state moves on a transition, unless display waits (allow-discrete). theme-switch-animates-everything reports a transition on every element's colors on a page with a theme switch, unless a switching hook sets transition none for that frame. hover-only-card-actions now passes only when the revealed control also shows on focus inside its container, shows with no hover, and stays while a menu it opens is open.

## Why

Opacity hides from sight only; keyboard and screen reader users still reach what is hidden, and 2.4.7 asks for a visible focus indicator. An exit the system defines (motion.dismiss) should be seen. A theme switch is one decision, not an animation.

## What it touches

engine/linter/components.py; engine/linter/structure.py (hover_only_reveal); data/anti-patterns.json; commands/ux-lint.md; the cases and probes for each rule.

## Consequences

A hover reveal hidden only inside @media (hover: hover) now also needs a focus reveal. A stylesheet with no markup to read judges the selector: a control or a panel name.
