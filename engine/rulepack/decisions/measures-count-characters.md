---
id: measures-count-characters
title: Measures count characters of the text face, landing copy runs shorter than reading, and every bound holds at every tier
status: active
areas: [layout]
supersedes: layout-bounds
superseded_by: null
---

# Measures count characters of the text face, landing copy runs shorter than reading, and every bound holds at every tier

## Context

The reading measure was 38rem, about 80 characters in the catalog's widest text face and 94 in its narrowest, and the floor was 30rem. On 35 measured award pages body copy ran 47 characters at the median and under 60 on 90 percent of pages, and formal, editorial pages ran longer. A rem is not a character: 30rem holds 66 characters of Noto Sans and 74 of Source Sans 3.

## Decision

layout.measure.text is character.reading_measure_ch characters (64 to 70 by formality, 4 fewer for long reading) and layout.measure.landing is character.landing_measure_ch characters (42 to 56, shorter as energy rises, longer as formality rises), each measured with the text face's average advance at the body size and rounded to whole rem. layout.measure.form stays 32rem. text-measure-floor: the reading and landing measures hold at least 40 characters of the set's text face at its body size (half an em per character when the face is not in the catalog), our floor, replacing 30rem. layout-grid-order and layout-gutter-floor now also hold the landing margins. form-measure is unchanged. container-bounds: the container, and the landing page's widest content, are at least 320px and at least the reading measure. Each floor and ceiling here is ours; WCAG sets none of them.

## Why

A measure in characters is what a reader sees; the same rem holds a fifth more characters in a narrow face. Landing copy is read in short bursts and measured pages keep it near 47 characters; long reading keeps a classic 60 to 66.

## What it touches

character.LANDING_MEASURE_CH, READING_MEASURE_CH, LONG_READ_FEWER_CH, landing_measure_ch, reading_measure_ch; layout.MEASURES, MIN_MEASURE_CH, DEFAULT_CH_EM, measure_rem, the text-measure-floor, layout-grid-order, layout-gutter-floor and container-bounds checks; audience effects; guidance/layout.md.

## Consequences

Long reading takes 4 characters fewer than other reading. An imported set with a 20rem reading column in a face of half an em fails, told the rem that holds 40 characters.
