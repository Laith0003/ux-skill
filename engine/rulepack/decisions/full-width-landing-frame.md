---
id: full-width-landing-frame
title: An expressive brand's landing page runs nearly edge to edge with a tight margin
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# An expressive brand's landing page runs nearly edge to edge with a tight margin

## Context

The container ran 1120 to 1440px with a 40 to 64px margin. On 35 measured award pages the desktop gutter was 32px at the median, 48px or less on 66 percent and 24px or less on 31 percent: layouts run nearly edge to edge.

## Decision

character.full_width is 0 up to an expressiveness of 0.45 and 1 from 0.75; at 0.5 and above the landing page takes the full-width frame. layout.container.full is 1920px, where a full-width page stops growing, and layout.margin-inline.full is character.full_margin_px (48px for a calm brand to 24px for a loud one, by energy) on the spacing scale, never under the tablet margin. layout.landing.max-width points at the full container or at layout.container.max, and layout.landing.margin-inline.<tier> at the page margin, or at the full margin from the laptop up; tokens.css gives the landing margin one alias, --layout-landing-margin-inline. The landing display fits its word in this frame (decisions/display-follows-expressiveness.md). Reading columns keep their measure.

## Why

A loud brand's first screen reads as a poster; a calm one's as a page. Both keep 1340px or more of content at 1440 when they take the full frame.

## What it touches

character.full_width, FULL_MARGIN_PX, full_margin_px; layout.FULL_CONTAINER, full_margin_units, uses_full_width, landing_margin_units, landing_frame, RESPONSIVE, ON_SPACE and the layout.container.full, layout.margin-inline.full, layout.landing roles; guidance/layout.md.

## Consequences

A landing page reads --layout-landing-margin-inline and layout.landing.max-width; product pages keep the container.
