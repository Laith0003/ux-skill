---
id: distinctness-on-a-grey-reference
title: Distinctness scales are measured on a grey reference brand, which leaves every color feature to the axes
status: active
areas: [output]
supersedes: distinctness-at-a-glance
superseded_by: null
---

# Distinctness scales are measured on a grey reference brand, which leaves every color feature to the axes

## Context

The glance distance scales each feature by the widest the engine goes over the 128 corners of the axes with one reference brand, #3366FF. The brand leads (decisions/brand-leads-the-role.md): a saturated blue fills its action at every corner, keeps its own temperature in the neutrals and leans its supporting accent to its own hue (decisions/neutrals-follow-the-brand.md, decisions/support-clear-of-banned-pairs.md). Over its corners the button, the link and the supporting accent do not move at all, so their scales would be zero and the distance could not compare two brands' buttons.

## Decision

Everything in decisions/distinctness-at-a-glance.md stands (the glance and behavior features, their weights, the floors and the named quantity per axis and foundation) except the reference brand: the scales are measured over the 128 corners with #808080, a mid grey. A grey brand leads nothing, so its role, its neutrals and its supporting accent are the axes' alone, and each scale is what the axes can do. The scales measured there, each pinned to within 5 percent: the button 0.37, the link 0.11, the supporting accent 0.07, the neutral tint 0.021, the status hues 38 degrees and the status chroma 0.082; the rest are unchanged. The trials built on one shared brand use the grey too. The named quantity for warmth and the neutrals is read on the same grey, since a saturated brand holds back half of warmth's lean.

## Why

A scale is the range the axes can move a feature over; a brand that leads a feature leaves no range to measure. With the grey reference the engine sits at 0.67 on opposite corners (floor 0.55), 0.42 on the four trials with their own brands and 0.22 on one shared brand (floor 0.20), 0.13 for the weakest single axis (floor 0.10) and 0.40 on the motion axis's behavior score (floor 0.30).

## What it touches

distinct.REFERENCE_BRAND and SPAN; tests/foundations/test_distinct.py; tests/foundations/test_character.py (the warmth and color quantity).

## Consequences

The floors are unchanged. Two saturated brands built from opposite briefs differ less in color than two grey brands would, by design: the brand is their identity. Lowering a floor needs a record.
