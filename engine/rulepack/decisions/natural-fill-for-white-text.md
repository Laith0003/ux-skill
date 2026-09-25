---
id: natural-fill-for-white-text
title: The primary fill weighs black text on a saturated mid tone against the least move that carries white, in light and dark alike
status: active
areas: [color]
supersedes: natural-text-on-the-brand
superseded_by: null
---

# The primary fill weighs black text on a saturated mid tone against the least move that carries white, in light and dark alike

## Context

Weighing black text on a saturated mid tone against a move to a brand ramp step snapped the move to the grid. A mid blue that carries white text at 4.17:1 moved to brand.600, 0.09 from the brand, where 0.02 would do; a crimson at 4.48:1 moved 0.10 and read as another red; and where the nearest step sat too far, the rule did not fire. Dark mode kept its own threshold, black text never on a fill darker than OKLCH lightness 0.72, so light and dark disagreed on the same button.

## Decision

The build writes the brand's natural fill for white text, per text minimum: color.brand.fill for 4.5:1 and color.brand.fill-high for 7:1, the brand's own hue and chroma at the highest OKLCH lightness, no lighter than the brand, where white text reaches that minimum, found by bisection (color.natural_fill). Its hover and pressed steps sit 0.05 and 0.10 darker in the same hue and chroma. The primary fill and the brand band start at the exact brand, and the natural fill joins the ramp steps as a candidate by its OKLab distance from the brand. Each fill and text that passes is weighed by a cost: the fill's distance from the brand (plus 0.3 times the ring's shortfall after the exact brand in dark high contrast) plus what the text costs in naturalness. White text costs nothing; black text costs character.black_text_cost, up to 0.12, the identity distance, on a fill of chroma 0.12 or more at lightness 0.60 or darker, nothing on a grey fill or one at 0.72 or lighter, in proportion between. The lowest cost wins, the search order breaking ties, and the same cost decides light and dark. The build notes the move, the system report says why, and the gate's on-color-natural check, our rule, finds black text on a primary fill where the natural fill sits nearer the brand than the fill plus that cost. The check reads the natural fill the engine wrote, so a token set the engine did not build is not checked, and dark high contrast, where the solver also weighs the ring, is left to the solver.

## Why

The least move that carries white keeps the button as close to the brand as the text allows, and it moves continuously with the brand color. The fill jumps only where the text turns from white to black, by about what black text costs there. One cost for both schemes means one judgment for one button.

## What it touches

character.BLACK_TEXT_COST, NATURAL_L and black_text_cost; color.NATURAL_FILLS, STATE_L, natural_fill, _natural_path, _fill_candidates, natural_cost, _solve_group, _on_color_natural, brand_fidelity; the color.brand.fill primitives; guidance/color.md.

## Consequences

A saturated mid tone takes a fill just darker than the brand with white text, on the button and on the brand band. A bright brand at lightness 0.72 or more keeps black text on its exact color in both schemes.
