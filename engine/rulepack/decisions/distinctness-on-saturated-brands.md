---
id: distinctness-on-saturated-brands
title: Distinctness is measured on a grey and on four saturated reference brands, each with its corner floor
status: active
areas: [output]
supersedes: distinctness-on-a-grey-reference
superseded_by: null
---

# Distinctness is measured on a grey and on four saturated reference brands, each with its corner floor

## Context

The brand leads its button and link (decisions/brand-leads-by-reach.md), so a saturated brand's opposite corners differ in less of what a person sees. Measured on a grey reference only, the corner floor held, while saturated blues sat at 0.50 against a floor of 0.55: a floor lowered for the common case without saying so.

## Decision

Everything in decisions/distinctness-at-a-glance.md stands, the features, weights, the trial, axis and motion floors and the named quantity per axis and foundation, with these changes. The scales are the widest the engine goes over the 128 corners of the axes with any of five reference brands: #808080, and the saturated #3366FF, #FF6A00, #0D9488 and #7C3AED (distinct.REFERENCE_BRANDS); pinned within 5 percent, the button is 0.37, the link 0.13, the supporting accent 0.25, the neutral tint 0.021, the status hues 38 degrees and the status chroma 0.098. On the grey reference opposite corners are held to 0.55. On each saturated reference they are held to 0.46, since the brand leads 3 of the 19.5 glance weight. A test freezes the features each collapse leaves unchanged (one face set; a color foundation that ignores warmth; the collapse the site trials showed) and requires every reference to fall under its floor. The trials on one shared brand, and every single axis, hold their floors on all five.

## Why

A floor that holds only for a grey brand says nothing about the brands people bring. Measured: opposite corners at 0.60 on grey and 0.47 to 0.54 on the saturated four; the trials on one shared brand at 0.21 to 0.22; the weakest single axis at 0.13; the four trials with their own brands at 0.41. Under the collapses the saturated references fall to 0.33 to 0.40 (one face set), 0.42 to 0.43 (color ignores warmth) and about 0.21 (the trial collapse), all under 0.46, so the floor still catches them.

## What it touches

distinct.REFERENCE_BRAND, SATURATED_REFERENCES, REFERENCE_BRANDS and SPAN; tests/foundations/test_distinct.py.

## Consequences

Two saturated brands built from opposite briefs differ less in color than two grey ones, by design: the brand is their identity. Their accent, neutrals, faces, shape and space carry the character. Lowering either floor needs a record.
