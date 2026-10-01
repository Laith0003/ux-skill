---
id: display-measures-each-letter
title: The display fit measures a headline word by its letters, the space left out
status: active
areas: [type, output]
supersedes: null
superseded_by: null
---

# The display fit measures a headline word by its letters, the space left out

## Context

The display fit sized a headline word as its letter count times the face's average advance, and that advance was measured for running text: English letter frequencies with the space counted in. A headline word has no space, so every proportional face came out 9 to 19 percent narrower than it sets. A landing page built for a short brief headline then ran sideways at 768px wide, the fit having allowed a size the word did not fit. Letters also differ: an m or a W sets near twice a face's letter advance and an i or an l near half, so a word of wide letters overran even a correct average.

## Decision

Each Latin face carries latin_letters, its frequency-weighted advance over a to z with the space left out, measured in Chromium from the face's own file at weight 400 (scripts/measure_face_letters.py). word_em sets a Latin word at latin_letters (latin_avg when a face has none); layout measures keep latin_avg, since a line of text does carry its spaces. typography.LETTER_WIDTHS holds each letter's share of its face's letter advance, averaged over the proportional Latin faces and rounded up, and the brief's headline counts its longest Latin word in average letters: the shares summed, accents read as their base letter, times WORD_SLACK (1.08), rounded up to a tenth (fit_letters). build_system words take that count, fractional for Latin and whole for Arabic, and a word wider than 40 average letters is refused naming the field and the fix. The default word stays 13 average Latin letters.

## Why

A fit that measures less than the page sets is the overflow it exists to prevent. Measuring each letter costs nothing at build time and keeps the display as large as the page's own word allows: a headline of narrow letters is not held to the size of a wide one. The slack is the measured spread between faces, so no word in the committed fixture (sixteen headline words in every Latin face) comes in over its estimate, and the estimate sits about 9 percent over the median word.

## What it touches

fonts.Metrics.latin_letters and the Latin faces' metrics; typography.LETTER_WIDTHS, WORD_SLACK, letter_count, fit_letters and word_em; emit.brief_words; build._check_words; scripts/measure_face_letters.py; tests/foundations/data/face_word_widths.json; guidance/type.md.

## Consequences

Where the default 13 letter word binds, the display fit and its fluid size come down by up to about 9 percent, so a loud brand's display reaches its full size a little past 1440 wide and a middle one sits about 1 percent under it there. A brief that gives its headline gets a display sized to its real letters. A new Latin face needs its letters measured with the script before it ships.
