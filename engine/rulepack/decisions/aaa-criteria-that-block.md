---
id: aaa-criteria-that-block
title: The gate blocks on the AAA criteria it applies
status: active
areas: [color, motion, layout, type]
supersedes: null
superseded_by: null
---

# The gate blocks on the AAA criteria it applies

## Context

Some of the rules the gate applies come from WCAG's AAA level: enhanced text contrast under high contrast (1.4.6), line spacing for reading text (1.4.8), turning off motion from interaction (2.3.3) and 44 by 44 targets (2.5.5). An audit can treat AAA as advice.

## Decision

Every check the gate runs blocks emission when it fails, AAA ones included, because each applies only where we chose to apply it: 1.4.6 under contrast:high, 2.3.3 under motion:reduced, 2.5.5 at comfortable density, 1.4.8 for reading styles and the text measure. Two failure messages name the level in their text: target-size-comfortable ("WCAG 2.5.5 (AAA) asks for targets of at least ...") and text-measure ("WCAG 1.4.8 (AAA) keeps lines to 80 ..."). The others name the criterion or the ratio without the level: the 7:1 raise prints "WCAG 1.4.6 needs 7:1", reading-leading prints "(1.4.8)", and reduced-travel names no criterion. Every check records its criterion on the check itself (Check.criterion), and each failure carries it in the gate report. There is no advisory tier in the gate.

## Why

A generated system can always meet these where they apply, so a failure is a defect, not a trade-off. Where a message names the level, a reader does not take an AAA rule for an AA obligation in their own work; where it does not, the criterion on the check leads to it.

## What it touches

gate.py; the layout target checks on layout.target.min, the size the button, text-field and selectable-row contracts bind, and the dialog's close and the banner's dismiss with them; typography reading-leading; motion reduced-travel; the audit files in the rule pack, which list each check's criterion.

## Consequences

An imported system that meets AA but not these checks fails the build until the owner meets them or the audit tier ships and reports them as advice.
