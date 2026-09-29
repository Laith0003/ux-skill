---
id: weights-stay-light
title: Display weights stay regular to medium, lighter for formal brands, and change along the scale
status: active
areas: [type]
supersedes: type-along-the-scale
superseded_by: null
---

# Display weights stay regular to medium, lighter for formal brands, and change along the scale

## Context

The display weight ran 300 to 800 and sat at 600 in the middle of the axes. On 35 measured award pages the headline weight was 400 at the median, 400 or lighter on 54 percent and 700 or heavier on 11 percent; formal brands were lighter.

## Decision

character.display_weight is 300 plus 350 times (0.6 energy plus 0.4 playfulness) plus 100 times how small the landing display is on its log range (1 at 60px, 0 at 240px), snapped to fifties, since every display face in the catalog is variable: 400 to 650, 500 in the middle of the axes, lighter as formality rises and heavier only for a small display or a loud, informal brand. It sets the hero and the display and eases toward the text face's heading weight (500 to 700 from contrast) at heading-3 on a log scale of size, within what each face ships. The icon stroke follows it, 1.5 to 2.25 in quarters. Letter spacing is 0 at 20px and below and tightens toward the hero to character.display_tracking em; labels open up by character.label_tracking em. Reading styles keep 0.

## Why

Large type needs less weight to look even, and the measured pages set it regular. A small display needs weight to hold the page. Driving the weight from energy, playfulness and the display's own size keeps it continuous.

## What it touches

character.display_weight, icon_stroke, heading_weight, display_tracking, label_tracking; typography.weights and tracking_em.

## Consequences

At standard contrast type.strong equals the heading weight (decisions/strong-under-high-contrast.md). The distinctness span for the hero weight is 250 (decisions/distinctness-on-saturated-brands.md reads it).
