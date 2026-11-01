---
id: disabled-contrast
title: Disabled colors stay distinct and visible, not readable at 4.5:1
status: active
areas: [color, contracts]
supersedes: null
superseded_by: null
---

# Disabled colors stay distinct and visible, not readable at 4.5:1

## Context

WCAG exempts inactive controls from contrast minimums. A disabled control that vanishes into its surface, or a disabled label that disappears on its own fill, still costs people the knowledge that the control exists.

## Decision

Disabled roles are not held to 4.5:1 or 3:1. color.text.disabled differs from default and muted text, color.action.disabled differs from the primary fill and from the card and raised surfaces in every context. The button contract holds the disabled label on the disabled fill to 1.3:1, a floor of its own, so the label never disappears. Disabled edges are held to no ratio, and each contract names its own: the secondary button's edge takes color.text.disabled, matching its disabled label; the check box in the selectable row takes color.text.disabled, matching the row's disabled text; the text field's edge takes color.line.subtle.

## Why

Inactive means not available, not invisible. The distinctness checks keep a disabled control recognizable as present without making it compete with active ones, and the label floor is measured, not hoped for.

## What it touches

color.py's disabled-distinct and disabled-visible checks; COVERAGE_EXEMPT; the button, selectable-row and text-field contracts.

## Consequences

Disabled styling is never used to de-emphasize an active control; muted text does that. When a disabled control needs its reason read, the reason is written next to it in readable text.
