---
id: dark-recess-and-bands
title: In dark the sunken surface sits between the page and the card, a band stays a quiet tint, and a table header is a band off the card
status: active
areas: [color, contracts]
supersedes: recessed-sunken
superseded_by: null
---

# In dark the sunken surface sits between the page and the card, a band stays a quiet tint, and a table header is a band off the card

## Context

In the site trial specimens every dark band was a deep saturated slab (a navy, a purple, a brown), louder than the rest of the page, and the dark sunken surface sat below the page, so a table header on it read as a black strip; under high contrast in dark the sunken surface and the page were both black.

## Decision

color.surface.sunken is color.neutral.recess-light in light, 0.035 OKLCH lightness below the page's step, and color.neutral.recess-dark in dark, the color halfway between the page's step (neutral.950) and the card's (neutral.900) in OKLab, at standard and high contrast. In dark the section band, color.surface.band, is color.brand.band-dark: brand.900's lightness and hue at no more chroma than character.dark_band_chroma allows, 0.02 plus 0.06 times the contrast axis, so a muted system gets a near grey band and a bold one a deeper tint, lifted to 1.2:1 off the page where it sits closer (decisions/surfaces-stand-apart.md). A table's header row fills with a new role, color.surface.header: the stripe's step in light (neutral.50, neutral.100 under high contrast) and the raised surface's in dark (neutral.800); the table contract binds its header to it, and every text, line and ring role is measured on it.

## Why

In dark the page is the floor: anything below it reads as a hole, and a well inside a card only needs to sit below the card. A band marks a section by its tint; at full ramp chroma a dark step of a saturated brand becomes the loudest thing on the page. A header needs to read as a band on the card in both schemes, which the stripe does in light and the raised step does in dark.

## What it touches

color._primitives (recess-dark, band-dark), _midpoint, _with_chroma, SEMANTIC and HIGH_CONTRAST for color.surface.sunken, band and header, TEXT_SURFACES and LINE_SURFACES; character.dark_band_chroma; contracts/seed/table.yaml; guidance/color.md.

## Consequences

Dark sunken areas, code blocks included, are a half step lighter than the page. Text on the sunken surface and the band is measured as before and moves if it must. A table placed straight on the raised surface still shows its header only by its edge in dark.
