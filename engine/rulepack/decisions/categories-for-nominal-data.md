---
id: categories-for-nominal-data
title: Nominal data takes six category hues that start on the brand
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Nominal data takes six category hues that start on the brand

## Context

A system carried four status families (danger, warning, success, info) and the brand, so a product had no color for a state that is neither good nor bad. An order that is shipped, preparing or scheduled, a second chart series and a segment of a breakdown all borrowed a status color, which told the reader the state was an outcome, or fell back to gray.

## Decision

The color foundation builds six category families, color.category.1 to color.category.6. The first sits on the brand's hue as far as the brand has one, a grey brand starting from the supporting accent's hue, so warmth still moves it; within 15 degrees of that hue's opposite the pull fades, so the start has no seam. The others step round the wheel by 60 degrees from there. Neighbors alternate between two lightnesses, and chroma follows the contrast axis as the status seeds do. Each category has a soft fill for a pill or a tile (step 200 in light, 900 in dark, at the step's full chroma), a strong tone for a chart mark (700 in light, 800 under high contrast, 400 and 300 in dark), text for the fill and the page, and text on the strong tone. Category text is a text role: the gate holds it to 4.5:1 on every text surface and on its own fill. The strong tone holds 3:1 on every surface a chart or a control sits on (1.4.11 for a chart mark), the text on it 4.5:1, every two strong tones stand at least 0.06 apart in OKLab and every two soft fills 0.04, in every context. Six hues cannot all keep clear of the four status hues, so a category always shows its word, a contract that binds one names a second cue, and the render budget counts category colors as meaning, as it counts status colors.

## Why

A dashboard reads states and series by color before it reads their words. Spacing the hues from the brand keeps the set the product's own, a continuous function of the brand and the axes rather than a fixed palette, and the alternating lightness keeps neighbors apart for readers who do not see the hue difference.

## What it touches

engine/foundations/character.py (CATEGORY_COUNT, CATEGORY_L, category_seed); engine/foundations/color.py (the category primitives, roles, pairings, fill groups and the categories-distinct check); engine/rulepack/guidance/color.md; tests/foundations/test_categories.py.

## Consequences

Every system gains six ramps and twenty-four roles, so tokens.json, tokens.css and the exports grow, and the gate measures the new pairings in every context. Status colors report outcomes; a category marks a state or a series that is neither good nor bad, and is never used to report an outcome. A shadcn theme's chart-1 to chart-5 import as the category marks.
