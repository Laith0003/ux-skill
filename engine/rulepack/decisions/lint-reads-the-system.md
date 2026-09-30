---
id: lint-reads-the-system
title: The lint judges a type value against the page's own system before a fixed number
status: active
areas: [type, motion]
supersedes: null
superseded_by: null
---

# The lint judges a type value against the page's own system before a fixed number

## Context

A rule that flags a weight of 700, a size of 120px or tight tracking on a display was written for pages with no system. A brand the engine built can ask for exactly those values: a loud, informal brand gets a heavy display and a large headline on purpose. Flagging them tells the page to undo its own system.

## Decision

The rules display-bold-700, letterspacing-tracking-tight-display, hero-text-arbitrary-90px and all-caps-large read the page's own system first: the custom properties the file defines, the local stylesheets it links and, for a stylesheet, the pages that load it. A weight, size or tracking value the system has passes. Tracking in em is compared in pixels at the rule's font size, and the tracking rule needs both the tracking and the weight to be the system's. Capitals at a large size pass when the system has a capitals display role, the size is one of its two largest and the letters are tracked at 0 or open. With no system of that kind, the fixed thresholds hold.

## Why

The system is where the look was decided, from the brand and the axes. The lint checks that a page keeps to it; it has no second opinion about what the system chose.

## What it touches

engine/linter/taste.py (System, weight_outside_system, tracking_outside_system, size_outside_system, capitals_outside_system); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases for the four rules.

## Consequences

A page that writes the system's value as a literal passes, and so does one that binds the token. A value that is close but not equal fires: 112px beside a 120px display step is off the scale. Body and subhead capitals always fire.
