---
id: high-contrast-non-text-floor
title: High contrast raises non-text parts to our own 4.5:1 floor
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# High contrast raises non-text parts to our own 4.5:1 floor

## Context

WCAG sets an enhanced level for text (1.4.6, 7:1) but none for non-text parts: 1.4.11 asks 3:1 at every level. A high-contrast mode that raises only text leaves borders, fills and rings where they were.

## Decision

Under contrast:high, text pairings rise to 7:1 (WCAG 1.4.6) and non-text pairings rise to 4.5:1. The 4.5:1 is our floor, not a WCAG number, and every message says so: "our high-contrast floor is 4.5:1 (WCAG 1.4.11 asks 3:1)". A pairing that cannot take the raise pins its own high-contrast minimum, and the pin is stated where it is declared.

## Why

People who switch on high contrast need the edges of controls to stand out as much as the words do. Borrowing the text ratio for parts gives a clear, round number. Calling it WCAG would misquote the standard, and a tool that misquotes WCAG loses the trust it sells.

## What it touches

gate.required, gate.cite and HIGH_NON_TEXT; the color generator's high-contrast starting points; the contracts' high field.

## Consequences

A focus ring on a tinted fill and on the selected surface pins 3:1 under high contrast (see ring-on-tinted-fills). The disabled label's 1.3:1 floor on its fill is pinned the same way (see disabled-contrast). Every other non-text pairing meets 4.5:1 there or the build stops.
