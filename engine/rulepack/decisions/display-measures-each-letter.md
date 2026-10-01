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

The display fit sized a headline word as its letter count times the face's average advance, and that advance was measured for running text: English letter frequencies with the space counted in. A headline word has no space, so every proportional face came out 9 to 19 percent narrower than it sets. A landing page built for a short brief headline then ran sideways at 768px wide, the fit having allowed a size the word did not fit. Letters also differ: an m or a W sets near twice a face's letter advance and an i or an l near half, capitals are wider still and differ most between faces, and a face with an optical size axis draws a wider cut at a display size than at a large test size.

## Decision

Each Latin face carries latin_letters and latin_capitals, its frequency-weighted advance over a to z and over A to Z with the space left out, measured in Chromium from the face's own file at 40px (so an optical size axis draws its display cut) and at weight 650, the heaviest a display takes (scripts/measure_face_letters.py, which waits for every face to load and refuses to write if one did not). word_em sets a Latin word at latin_letters (latin_avg when a face has none); layout measures keep latin_avg, since a line of text does carry its spaces. typography.LETTER_WIDTHS holds each letter's share of its face's lowercase advance over the proportional Latin faces, rounded up: the average share for a lowercase letter and the widest for a capital. The brief's headline counts its longest Latin word in average letters: the shares summed, accents read as their base letter, times WORD_SLACK (1.08), rounded up to a tenth (fit_letters). An Arabic word counts its letters times ARABIC_SLACK (1.06) at arabic_avg, since joined letters take other forms than isolated ones. The default word is 13 average Latin letters and 10 Arabic letters with the same slack (FIT_WORD 14.1 and 10.6). When the brand leans to a display in capitals (character.capitals at CAPITALS_FROM and above), the Latin word is measured in them: its count times the face's capital advance over its lowercase one, plus the capitals tracking (capitals_letters), recorded in type.fit-word.latin. build_system words take fractional counts, and a word wider than 40 average letters is refused naming the field and the fix.

## Why

A fit that measures less than the page sets is the overflow it exists to prevent. Measuring each letter costs nothing at build time and keeps the display as large as the page's own word allows: a headline of narrow letters is not held to the size of a wide one. The committed fixture (tests/foundations/data/face_word_widths.json) holds every face's letters and headline words; the metrics and the letter table are recomputed from it, the slack is chosen on one set of words, and a second set the slack was not chosen on (wide letters, short words and capitals) and the Arabic words check it. No measured word comes in over its estimate, and on the chosen words the estimate sits within 25 percent of the measured width.

## What it touches

fonts.Metrics.latin_letters and latin_capitals and the Latin faces' metrics; typography.LETTER_FREQ, LETTER_WIDTHS, WORD_SLACK, ARABIC_SLACK, FIT_LETTERS, FIT_WORD, letter_count, fit_letters, arabic_fit_letters, capitals_letters, word_em, generate_type and the display-fits message; emit.brief_words; build._check_words; scripts/measure_face_letters.py; tests/foundations/data/face_word_widths.json; guidance/type.md.

## Consequences

Where the default word binds, the display fit and its fluid size come down: by up to about 20 percent for a sentence-case display, and further for a brand that sets its display in capitals, whose default word is measured in capitals (a loud brand's display at 1440 wide sits near 70 percent of its size until the brief gives its headline). A brief that gives its headline gets a display sized to its real letters, so a short headline stands at full size. A new face needs its letters measured with the script before it ships.
