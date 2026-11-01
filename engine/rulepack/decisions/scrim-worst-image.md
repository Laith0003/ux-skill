---
id: scrim-worst-image
title: The scrim is measured over the worst image for its text
status: active
areas: [imagery]
supersedes: null
superseded_by: null
---

# The scrim is measured over the worst image for its text

## Context

Text on a photo is only as readable as the photo under it allows, and the build cannot see the photo. A white image is the worst case for light text, but the best case for dark text on a light scrim: measured over white alone, dark text on a pale scrim passes at any strength and reads at about 1.3:1 over a black photo.

## Decision

The scrim-text check composites the scrim over a pure white and a pure black image in every context and holds the lower ratio of the text on it to 4.5:1 (WCAG 1.4.3), 7:1 under high contrast (WCAG 1.4.6); text whose luminance falls between the two composites measures 1:1, since a grey photo matches it. A finding names the image that failed. The scrim's alpha is the least that reaches the minimum over both.

## Why

Compositing is linear in each channel and luminance rises with every channel, so no photo's composite is lighter than the white image's or darker than the black image's: text lighter than both composites is weakest over white, text darker than both is weakest over black, and text between them meets a grey photo that matches it, which the check reports as 1:1. The generated text is white on a dark scrim, where the white image decides the alpha; the check guards a set whose text or scrim is changed.

## What it touches

imagery.IMAGES, imagery._worst, imagery.scrim_alpha and the scrim-text check; guidance/imagery.md.

## Consequences

A light scrim under dark text needs enough alpha to hold over a black image. The scrim has no headroom by design: it is the least alpha that reaches the minimum.
