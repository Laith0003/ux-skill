---
id: aaa-criteria-that-block
title: The gate blocks on the AAA criteria it applies and names their level
status: active
areas: [color, motion, layout, type]
supersedes: null
superseded_by: null
---

# The gate blocks on the AAA criteria it applies and names their level

## Context

Some of the rules the gate applies come from WCAG's AAA level: enhanced text contrast under high contrast (1.4.6), line spacing for reading text (1.4.8), turning off motion from interaction (2.3.3) and 44 by 44 targets (2.5.5). An audit can treat AAA as advice.

## Decision

Every check the gate runs blocks emission when it fails, AAA ones included, because each applies only where we chose to apply it: 1.4.6 under contrast:high, 2.3.3 under motion:reduced, 2.5.5 at comfortable density, 1.4.8 for reading styles. Messages name the level where it matters, for example "WCAG 2.5.5 (AAA)". There is no advisory tier in the gate.

## Why

A generated system can always meet these where they apply, so a failure is a defect, not a trade-off. Naming the level keeps a reader from taking an AAA rule for an AA obligation in their own work.

## What it touches

gate.py; the layout target checks on layout.target.min, the size the button, text-field and selectable-row contracts bind, and the dialog's close and the banner's dismiss with them; typography reading-leading; motion reduced-travel; the audit files in the rule pack, which explain the level of each check.

## Consequences

An imported system that meets AA but not these checks fails the build until the owner meets them or the audit tier ships and reports them as advice.
