---
id: surfaces-stand-apart
title: The brand reaches surfaces as a tint, a band or one brand band, and each stands apart from the page
status: active
areas: [color]
supersedes: brand-surfaces
superseded_by: null
---

# The brand reaches surfaces as a tint, a band or one brand band, and each stands apart from the page

## Context

Rules that keep saturated color off large surfaces, with no brand-tinted surface to use instead, push people to paint a surface with the button color. On real landing pages the light tint, the brand's step 50, measured 1.0:1 against the page and could not be seen, and the light band, step 100 at full ramp chroma, read as a loud periwinkle slab in a muted system.

## Decision

Three surface roles carry the brand. color.surface.tint, for a quiet group, is the brand's 50 hue and chroma in light (950 in dark) at the lightness nearest the page that stands 1.1:1 off it (color.stand_off, TINT_FLOOR, our floor for a filled area). color.surface.band, for a section band, is the brand's 100 lightness and hue in light at no more chroma than character.light_band_chroma, 0.015 plus 0.045 times the contrast axis, moved to 1.2:1 off the page (BAND_FLOOR, the container-edge floor) when it sits closer; in dark it is brand.900's lightness and hue at no more chroma than character.dark_band_chroma. color.surface.brand, the brand color, is for one band per view with color.text.on-brand on it, solved like the primary fill (decisions/natural-fill-for-white-text.md). Every text role is paired with the tint and the band, and every line role and the focus ring with the tint, the band and the table stripe; a control on the brand band takes color.text.on-brand for its focus ring and edges (decisions/controls-on-brand-surfaces.md).

## Why

A tint that measures 1.0:1 is no surface. A filled area is seen at a smaller step than a hairline edge, so the tint's floor sits below the container-edge floor, and the band sits beyond it, so the two read as two levels. A band spans a whole section, so its chroma follows the contrast axis: a muted system gets a pale band, a bold one a deeper tint.

## What it touches

color.SEMANTIC for the three surfaces, TINT_FLOOR, BAND_FLOOR, stand_off, _primitives (tint-light, tint-dark, band-light, band-dark); character.light_band_chroma, dark_band_chroma; TEXT_SURFACES and LINE_SURFACES; the brand band's group in GROUPS.

## Consequences

Status tints and the selected surface keep their meanings; a tinted surface is decoration, never state. Text and lines on the tint and the band are measured as before and move if they must.
