---
id: brand-surfaces
title: The brand reaches surfaces as a tint, a band or one brand band
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# The brand reaches surfaces as a tint, a band or one brand band

## Context

Rules that keep saturated color off large surfaces, with no brand-tinted surface to use instead, leave every section of a page on the same neutral and push people to paint a surface with the button color.

## Decision

Three surface roles carry the brand: color.surface.tint (step 50 in light, 950 in dark) for a quiet group, color.surface.band (step 100 in light, 900 in dark) for a section band, and color.surface.brand, the exact brand color, for one band per view with color.text.on-brand on it. Every text role is paired with the tint and the band, and every line role and the focus ring with the tint, the band and the table stripe; a control on the brand band takes color.text.on-brand for its focus ring and edges (decisions/controls-on-brand-surfaces.md). The brand band is solved like a fill: the exact brand first, then the nearest brand step whose text reads, with no pairing against the page.

## Why

A tint or a band keeps text at full contrast and lets a long page change pace without inventing colors. The brand band gives a closing call to action the brand color without stretching a button.

## What it touches

color.SEMANTIC and HIGH_CONTRAST for the three surfaces; TEXT_SURFACES and LINE_SURFACES; the brand band's group in GROUPS.

## Consequences

Status tints and the selected surface keep their meanings; a tinted surface is decoration, never state.
