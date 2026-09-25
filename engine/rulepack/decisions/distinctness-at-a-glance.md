---
id: distinctness-at-a-glance
title: Distinctness is measured on what a person sees at a glance, and each axis moves a named quantity
status: superseded
areas: [output]
supersedes: distinctness
superseded_by: distinctness-on-a-grey-reference
---

# Distinctness is measured on what a person sees at a glance, and each axis moves a named quantity

## Context

Four site trial briefs of very different character built systems a person could not tell apart: the same body size, corners, neutrals, status colors and face, with only the hue changed. A distance that averages every feature equally, with scales guessed rather than measured, can be met by features nobody sees on a first look (motion, the mono face, the focus ring's width) and cannot see the neutrals and the status colors at all when their scale is ten times their real range. A check that an axis changes some token under a foundation passes as long as any one token moves, so an axis can stop reaching the neutrals while it still flips the brand's role.

## Decision

engine/foundations/distinct.py reads two sets of features from a built system. The glance set, weighted: 2 each for the main button's color, the neutral tint (the neutral ramp's middle step in the OKLab a/b plane) and the display face; 1 each for the link color, the supporting accent, the four status hues, the status chroma, the text face, the control and card corners, the hero's size and weight, the body size, the card padding, the desktop region gap and the hero image's ratio; 0.5 each for the hero's tracking and for the card shadow's alpha and blur. The behavior set, equal weights: the reveal duration, the expressive curve's overshoot, the mono face and the focus ring's width. `distance` is the weighted mean scaled difference of the glance set, 0 to 1, and never counts the behavior set; `behavior` measures that set apart. Each scale is the widest the engine goes over the 128 corners of the axes with the brand #3366FF (the body size by the audience's age bands), pinned by a test to within 5 percent of that measured range. Our floors on the glance distance: every pair of opposite corners at least 0.55 apart; the four site trial briefs at least 0.20 apart pairwise (two different faces alone score 0.146, and trials with only their faces apart score 0.166, so the floor sits above both), with their own brands and with one shared brand, and on four different display faces; any one axis but motion, moved from 0 to 1, at least 0.10. The motion axis shows only in use, so it is held to 0.30 on the behavior score. For every axis-to-foundation pair in character.INFLUENCE a test names a visible quantity (for warmth and color, the neutrals' b and the info hue; for density and layout, the desktop region gap; for motion, the overshoot and the reveal duration) and requires it to move one way only along an 11 step sweep, by at least a stated amount of about two thirds of what the engine moves it.

## Why

What makes two systems look alike is what fills the first screen, so that is what the floors hold. A scale taken from the engine's real range makes a whole swing of the neutrals from cool to warm count in full, where a guessed scale made it worth under 0.01. Keeping motion and the ring out of the glance distance stops a pair that differs only in use from clearing the trial floor. The floors are set where the collapses they guard against fail them: one face set for every system brings the trials to 0.08 and the corners to 0.52; a color foundation that ignores warmth brings the corners to 0.52; the collapse the site trials showed (one face set, the neutrals and status colors at the middle warmth, one roundness) brings the trials to 0.07 and the corners to 0.33; a layout that ignores density brings that axis to 0.08; curves that ignore the motion axis bring its behavior to 0.25. The engine sits at 0.23, 0.66, 0.13 and 0.40 on the same measures. A named quantity per pair catches a single dropped path, such as status colors that stop following warmth, that no distance floor can see without being set so close to the engine that any change would trip it.

## What it touches

engine/foundations/distinct.py; character.INFLUENCE; tests/foundations/test_distinct.py, test_character.py (QUANTITIES), trials.py and the trial briefs in tests/foundations/briefs/.

## Consequences

A change that makes two characters converge, or that stops an axis reaching a quantity it names, fails the suite and names the pair or the quantity. A change that widens or narrows what the engine produces on a feature fails the scale test until the scale is measured again. Raising a floor is a decision; lowering one needs a record.
