---
id: strong-under-high-contrast
title: Emphasis uses the heading weight, and stays 200 above body text under high contrast
status: active
areas: [type]
supersedes: strong-weight
superseded_by: null
---

# Emphasis uses the heading weight, and stays 200 above body text under high contrast

## Context

type.strong took the text face's heading weight in every mode. High contrast makes body text one weight heavier, so for a brand whose heading weight is 500 (contrast axis below 0.25) bold words sat at the same weight as body text in exactly the mode meant for low vision readers, and for every other brand the gap shrank from 200 to 100.

## Decision

At standard contrast type.strong is the text face's heading weight, 500, 600 or 700 as the contrast axis rises (character.heading_weight), as before. Under high contrast it is the heavier of the high contrast heading weight and body text's high contrast weight plus 200, within what the face ships. Under right to left each value is a weight the Arabic text face ships. The strong-weight check refuses a type.strong less than 200 above type.text.body in any high contrast context.

## Why

Two weights are what a reader tells apart in running text, and 200 is the smallest gap that stays visible at body sizes once body text is heavier. Emphasis must survive the mode that exists to make text easier to read.

## What it touches

typography._strong, STRONG_GAP and the strong-weight check; the contrast:high and direction:rtl modes of type.strong.

## Consequences

tokens.css carries a type.strong override under the high contrast attribute and media query. A system whose heading weight is 500 or 600 loads weight 700 too.
