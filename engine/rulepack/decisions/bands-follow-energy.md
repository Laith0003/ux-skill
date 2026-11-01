---
id: bands-follow-energy
title: Section bands carry color by energy, a calm page none, and a page has a color budget
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Section bands carry color by energy, a calm page none, and a page has a color budget

## Context

Band chroma came from contrast alone and never reached zero, so a calm page still changed color from section to section, and nothing told a page how much color it may carry. On 35 measured award pages saturated color covered almost nothing on calm pages and about a fifth of the page on loud ones, and the background changed about every second screen, more often and harder the louder the page.

## Decision

character.band_level is 0 up to an energy of 0.2 and rises to 1 at energy 1. The light band's chroma cap is 0.12 times it and the dark band's 0.1 times it, so a calm system's band and tints are grey and a loud one's carry the brand's hue at the ramp's own chroma. color.budget.chromatic is character.chromatic_budget, 0.02 plus 0.18 times energy: the share of the page less its images a design may set in a chromatic color. color.budget.bands is character.band_share, half the band level: the share of a landing page's sections set on a band or the brand band, 0 for a calm page.

## Why

A calm page separates its sections by space, a loud one by color; one continuous level decides both, and the two budgets give a rendered-page check a number to read.

## What it touches

character.BAND_FROM, BAND_CHROMA, band_level, light_band_chroma, dark_band_chroma, band_share, chromatic_budget; color._add_ink_and_budget and the color.budget roles; guidance/color.md.

## Consequences

The band still stands 1.2:1 off the page, so a grey band reads as a band where a page uses one.
