---
id: warmth-through-grey
title: Warmth moves the neutrals and the duotone light through grey, never around the wheel
status: superseded
areas: [color, imagery]
supersedes: neutral-tint
superseded_by: neutrals-follow-the-brand
---

# Warmth moves the neutrals and the duotone light through grey, never around the wheel

## Context

Neutrals carry most of a screen, and grey with a trace of the brand hue looks the same for every brand, whatever the brief says about warmth. Turning the brand hue toward a warm or a cool hue along the wheel takes the short way round, and for the common pairs, a blue brand with a warm brief or a brown brand with a cool one, the short way runs through magenta: the neutrals come out mauve or rose instead of cream or blue grey, and two brands a few degrees apart either side of the anchor's opposite turn opposite ways.

## Decision

The neutral seed is a point in the OKLab a/b plane that moves in a straight line from the brand hue at chroma 0.008 (at warmth 0.5) to a warm hue (70 degrees) or a cool hue (250 degrees) at chroma 0.030, reaching the anchor at warmth 1 or 0. How far along it sits is the warmth's distance from 0.5, doubled. The brand's chroma weights its end of the line (decisions/grey-brands-steer-no-hue.md). The duotone highlight moves the same way, from the brand hue at chroma 0.04 toward the anchor at chroma 0.07, up to 60 percent of the way.

## Why

A straight line between two far hues passes near grey, where a hue has no name, instead of through a third hue, so a warm brief gets cream and sand and a cool one blue grey whatever the brand. At warmth 0.1 or 0.9 the neutral hue sits within a few degrees of its anchor for any brand. The point moves continuously with the warmth and with the brand color, so there is no seam where the brand sits opposite the anchor. The chroma stays low enough that text contrast is set by lightness, which the gate measures.

## What it touches

character.ab_mix, character.neutral_tint and NEUTRAL_C; color._neutral_seed; imagery.duotone and HIGHLIGHT_C; every role on the neutral ramp and imagery.duotone.highlight.

## Consequences

Every surface, text and line role shifts with warmth, and a brand whose hue sits far from the anchor gets neutrals near grey in the middle of the warmth range. The gate measures every role in every context, so a warm or cool tint never costs contrast.
