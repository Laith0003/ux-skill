---
id: bottom-anchored-hero
title: A full-bleed hero anchors its headline at the bottom start or centres it, and the scrim covers that region
status: active
areas: [imagery, layout]
supersedes: null
superseded_by: null
---

# A full-bleed hero anchors its headline at the bottom start or centres it, and the scrim covers that region

## Context

The full-bleed composition set its headline on a scrim with nothing saying where. On 35 measured award pages 16 headlines sat in the lower half, usually start-aligned over video or a photo, and 9 were centred, mostly poster-style heroes on loud pages.

## Decision

composition.hero_anchor is center for a brand that leans to a capitals display (character.capitals at 0.5 and up) and bottom-start otherwise; the composition carries it, its line names it for a full-bleed winner, and its dictionary holds it as anchor. imagery.scrim-reach is imagery.scrim_reach: the share of the hero's height from its bottom edge that a two-line landing headline at the tallest display leading and what sits under it (250px: a lede, the action, the gaps and the padding) fill on a 1440 by 900 and a 390 by 844 hero, at least 0.4. imagery.scrim-fade, 0.15, is how far above that the scrim fades to clear. scrim-covers-text checks the reach against the display the set holds. The scrim's alpha is still measured over the worst image (scrim-text).

## Why

A headline anchored low leaves the image to carry the first screen; the scrim then needs only the region the words fill, measured, not a guessed gradient.

## What it touches

composition.ANCHORS, hero_anchor, Composition.anchor; imagery.HERO_VIEWS, TEXT_ALLOWANCE_PX, SCRIM_REACH_MIN, SCRIM_FADE, text_region, scrim_reach, the scrim-covers-text check; guidance/imagery.md.

## Consequences

A bottom-anchored hero draws its scrim as a gradient from the bottom edge: full strength up to imagery.scrim-reach, clear by scrim-reach plus scrim-fade.
