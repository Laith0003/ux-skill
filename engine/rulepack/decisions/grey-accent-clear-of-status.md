---
id: grey-accent-clear-of-status
title: A grey brand's supporting accent runs from violet to rose, clear of every status hue
status: superseded
areas: [color]
supersedes: grey-brand-support-hue
superseded_by: grey-support-is-neutral
---

# A grey brand's supporting accent runs from violet to rose, clear of every status hue

## Context

A grey brand has no stable hue, so its supporting accent takes its hue from warmth (decisions/grey-brands-steer-no-hue.md). A path from the cool hue (250 degrees) to the warm hue (70 degrees) lands on the info hue at warmth 0 and on the warning hue at warmth 1, 5 degrees from each, and passes the danger hue near warmth 0.75, also 5 degrees away. An accent tag beside a danger or info message then reads as the same status.

## Decision

With no brand hue the accent's hue moves in proportion to warmth from 285 degrees (violet) at warmth 0 to 355 degrees (rose) at warmth 1, 320 degrees (orchid) at warmth 0.5 (character.axes_support_hue, GREY_ACCENT). At every warmth it sits at least 30 degrees from each of the four status hues the same system gets (character.STATUS_CLEARANCE), 39 degrees at the least. The brand-led hue and this one are mixed in a straight line in the OKLab a/b plane, weighted by the brand's chroma: in full from OKLCH chroma 0.04 up, where the brand-led hue is kept exactly, and none at grey. The accent's chroma and lightness are unchanged.

## Why

The status hues sit at 25, 75, 150 and 245 degrees and lean up to 12 degrees with warmth. Around those four hues the arcs that keep 30 degrees from all of them are 80 degrees wide from violet to rose, 35 in the cyans, 15 in the yellow greens and none between danger and warning, and the leans narrow them further, so a hue that moves continuously has to stay inside one arc, and only the first has room to follow warmth. Violet reads cool and rose reads warm, so the accent still follows warmth, and it never crosses a status hue on the way. Mixing in the a/b plane keeps the accent continuous in the brand color, so brands that look alike get accents that look alike.

## What it touches

character.axes_support_hue, support_hue, GREY_ACCENT and STATUS_CLEARANCE; color._primitives (the support family); color.text.support, color.decorative.support and the generated art.

## Consequences

Every brand at or above chroma 0.04 keeps its accent. A grey brand gets a violet accent toward cool, orchid at the middle warmth and rose toward warm, whatever its hex rounding, and none of them reads as a status color. A brand between grey and chroma 0.04 gets an accent between its brand-led hue and the axes' hue; the clearance is held for the grey end of that mix only.
