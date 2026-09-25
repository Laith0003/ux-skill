---
id: grey-support-is-neutral
title: A grey brand's supporting accent is a neutral step, since an identity with no hue gains none
status: active
areas: [color]
supersedes: grey-accent-clear-of-status
superseded_by: null
---

# A grey brand's supporting accent is a neutral step, since an identity with no hue gains none

## Context

A grey brand's supporting accent took a hue from warmth alone, violet to rose, at the 0.06 chroma floor. A grey stone brand got a mauve accent in its tags and in 13 shapes of its generated art, a hue its identity never had.

## Decision

The supporting accent's chroma is multiplied by hue_weight of the brand's chroma: in full from OKLCH chroma 0.04 up, in proportion below, none at grey. So an achromatic brand's accent is a neutral step, a tint of ink, and a nearly grey brand's is nearly neutral. The accent's hue is still placed as before (decisions/support-in-the-brand-family.md), from warmth alone for a grey brand, so it moves continuously as the chroma rises from zero.

## Why

A grey identity is a choice; adding a hue to it is the engine speaking over the brand. With no chroma the accent cannot read as a status color either, so it needs no hue arc to keep clear of them.

## What it touches

character.support_seed; color._primitives (the support family); color.text.support, color.decorative.support and the generated art.

## Consequences

A grey brand's tags and art accents are neutral greys. A brand between grey and chroma 0.04 gets a quiet accent in proportion.
