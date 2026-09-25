---
id: landing-display-step
title: A landing display step sits above the hero, and the four largest type styles step down on phones
status: active
areas: [type, layout, output]
supersedes: type-steps-down-on-phones
superseded_by: null
---

# A landing display step sits above the hero, and the four largest type styles step down on phones

## Context

On real landing pages the hero came out at 45 to 53px at 1440 wide, so the page read as a product screen, and the guidance forbids resizing a token. With one size per style at every width a large style runs past a phone, and a page that shrinks it with its own media queries copies the breakpoints and breaks the hierarchy.

## Decision

typography.ROLES holds type.text.display at step 10, above the hero. Its size is character.landing_display_px at body 16px: 56px plus up to 48px, three fifths by the contrast axis and two fifths by playfulness (one minus formality), scaled with the body size and kept at least 1.08 times the hero. It uses the display face at the display weight, in both scripts, and the type-hierarchy check holds display, hero, heading-1, section-title, heading-2, heading-3 and body falling in size. layout.breakpoint.tablet, laptop and desktop stay tokens for exporters and documentation, and tokens.css keeps one alias per tiered layout role (layout.RESPONSIVE) under @media (min-width) at the breakpoints' literal px. The landing display, hero, heading-1 and section-title step down on a phone, every width below layout.breakpoint.tablet: each has a factor token (type.phone.display, hero, heading-1, section-title), its phone size over its own size, from a phone scale whose ratio is 0.6 of the way from 1 to the system's ratio, at least 1px above the style below it on the phone and never above its own size. From the tablet breakpoint up each of the four takes a fit factor per tier, type.fit.<style>.<tier>: at most 1, and small enough that a 13 letter Latin word and a 10 letter Arabic word at its size fit the tier's column (the breakpoint less both margins, within the container; all of it on a tablet and seven twelfths from the laptop up, where a split composition sets the headline), measured with the display and Arabic display faces' average advances, each style still 1.08 times the next, and never smaller on a wider tier. The figure takes heading-1's factors. tokens.css writes each style's font-size and letter-spacing as calc(size * var(--<style>-scale)), with the phone factor at :root and the tier's fit factor at each breakpoint. The display-fits check measures the word and the order at each tier. The phone-hierarchy check keeps each factor above 0 and at most 1 and the four phone sizes falling above heading-2, in both directions.

## Why

A landing page's headline has a job the hero of a product view does not: it carries the page from a distance. A size from contrast and formality is continuous in both, so a bold, playful system gets a large headline and a muted, formal one a smaller one that still reads as a landing page. A built step is checked; a size a page writes itself is not. The phone scale keeps the character of the system on a phone.

## What it touches

typography.DISPLAY_STEP, ROLES, HIERARCHY, PHONE_ROLES, FOLLOWS, FIT_TIERS, FIT_WORD, SPLIT_SHARE, tier_factors, fit_problems, latin_px, phone_px, the type.phone roles and the phone-hierarchy check; character.landing_display_px; export and layout.responsive_css; guidance/type.md and layout.md.

## Consequences

A landing page sets its headline in type.text.display and never enlarges the hero. tokens.json carries the desktop sizes in each style and the factors beside them, so an exporter for another platform applies the factor below its own phone width.
