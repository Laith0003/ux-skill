---
id: logo-and-decoration
title: The logo keeps the brand color, and decoration has a visibility floor of ours
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# The logo keeps the brand color, and decoration has a visibility floor of ours

## Context

WCAG exempts logotypes and pure decoration from contrast minimums, so without a floor of our own a logo or a background shape can vanish into the page in one mode.

## Decision

color.logo starts at the exact brand color and keeps it wherever it measures our 3:1 floor against the page, moving to the nearest brand step otherwise. The decorative roles hold our 1.5:1 floor against the page and the card in every context. color.illustration.line, for lines that carry meaning, is paired at 3:1 (WCAG 1.4.11) with the page, card and raised surfaces.

## Why

A logo that keeps its color in most modes and stays visible in all of them is what a brand owner expects. Decoration that is barely visible is still decoration; one that disappears in dark mode is a bug.

## What it touches

color.LOGO_FLOOR, DECORATIVE_FLOOR, DECORATIVE_ROLES; the logo, decorative and illustration pairings; gate.cite for our floors.

## Consequences

Meaningful graphics use color.illustration.line or a status role with a second cue, never a decorative role.
