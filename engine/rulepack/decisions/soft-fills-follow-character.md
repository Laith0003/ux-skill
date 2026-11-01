---
id: soft-fills-follow-character
title: Status soft fills take their chroma from the character
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Status soft fills take their chroma from the character

## Context

The info fill of a calm clinic and of a trustworthy fintech was the same saturated sky blue as a loud brand's, because every soft fill was a fixed ramp step. The status seeds already followed the contrast axis, but the light steps kept enough chroma to shout on a quiet page.

## Decision

Each status soft fill is its ramp step (100 and 900, 50 and 950 under high contrast) at the same lightness and hue with a share of its chroma: character.status_soft, 0.3 plus 0.7 times the energy, where energy is 0.6 times the contrast axis plus 0.4 times the motion axis. A calm, muted brief keeps about a third of the chroma, a loud, lively one all of it. The motion axis therefore reaches color, through this share.

## Why

A soft fill says "this is a note" by its hue; how loudly it says it is character, the same as the brand's own loudness and pace. A continuous share keeps two close briefs close, and the text on each fill is still measured at 4.5:1, 7:1 under high contrast.

## What it touches

character.energy, status_soft and INFLUENCE; color._primitives (the soft primitives), SEMANTIC and HIGH_CONTRAST for color.status.<name>.soft; guidance/color.md.

## Consequences

Calm systems show near grey status banners with a tinted edge of hue; the icon and the words still carry the status (WCAG 1.4.1). Status text and strong fills keep their chroma.
