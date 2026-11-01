---
id: grey-brand-support-hue
title: A grey brand's supporting accent takes its hue from warmth alone
status: superseded
areas: [color]
supersedes: null
superseded_by: grey-accent-clear-of-status
---

# A grey brand's supporting accent takes its hue from warmth alone

## Context

The supporting accent keeps a chroma of at least 0.06, so it always shows a hue, and that hue is placed from the brand hue. A grey brand has no stable hue: at the middle axes #808080, #7F8080, #80807F and #807F80 look the same and get olive, violet, teal and brown accents. Weighting the brand's hue by its chroma removes that noise, but then the accent needs a hue that owes nothing to the brand.

## Decision

With no brand hue the accent's hue comes from warmth: the cool hue (250 degrees) at warmth 0, the warm hue (70 degrees) at warmth 1, and between them it walks through violet and rose, 340 degrees at warmth 0.5 (character.axes_support_hue). The brand-led hue and this one are mixed in a straight line in the OKLab a/b plane, weighted by the brand's chroma: in full from OKLCH chroma 0.04 up, where the brand-led hue is kept exactly, and none at grey. The accent's chroma and lightness are unchanged.

## Why

The warm and cool hues sit opposite each other, so a hue that moves continuously with warmth from one to the other has to pass a third hue on the way. Through violet and rose it stays off the green side, where the success color sits, at the middle warmth where most briefs sit. Toward warm it passes the danger hue near warmth 0.75, at 0.06 chroma against the danger color's 0.07 to 0.18. Mixing in the a/b plane keeps the accent continuous in the brand color, so brands that look alike get accents that look alike. Where the two hues sit opposite each other at equal weight, at one or two brand colors per set of axes, the mix has no hue and the brand-led hue is used.

## What it touches

character.axes_support_hue and support_hue; color._primitives (the support family); color.text.support, color.decorative.support and the generated art.

## Consequences

Every brand at or above chroma 0.04 keeps its accent. A grey brand gets a dusty rose accent at the middle warmth, violet toward cool and terracotta toward warm, whatever its hex rounding. A brand between grey and chroma 0.04 gets an accent between its brand-led hue and the axes' hue.
