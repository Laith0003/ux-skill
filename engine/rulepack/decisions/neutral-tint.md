---
id: neutral-tint
title: Warmth sets the hue and chroma of the neutrals
status: superseded
areas: [color]
supersedes: null
superseded_by: warmth-through-grey
---

# Warmth sets the hue and chroma of the neutrals

## Context

Neutrals carry most of a screen. Grey with a trace of the brand hue looks the same for every brand, whatever the brief says about warmth.

## Decision

The neutral seed takes the brand hue at warmth 0.5 and moves toward a warm hue (70 degrees) or a cool hue (250 degrees) as warmth moves toward 1 or 0, up to 80 percent of the way. Its chroma runs from 0.008 at warmth 0.5 to 0.030 at either end.

## Why

Warm systems get cream and sand, cool systems blue grey, and a middle brief keeps a whisper of its own hue. The change is continuous, so two briefs one tenth apart in warmth differ a little and two at opposite ends differ plainly. The chroma stays low enough that text contrast is set by lightness, which the gate measures.

## What it touches

character.neutral_tint; color._neutral_seed; every role on the neutral ramp.

## Consequences

Every surface, text and line role shifts with warmth. The gate measures them in every context, so a warm or cool tint never costs contrast.
