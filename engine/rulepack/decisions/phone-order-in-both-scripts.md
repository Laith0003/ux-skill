---
id: phone-order-in-both-scripts
title: Each phone factor keeps the phone order in every script the system carries
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# Each phone factor keeps the phone order in every script the system carries

## Context

The phone factors of the landing display, hero, heading-1 and section-title were set from the Latin sizes alone: each Latin phone size at least 1px above the style below it, the factor its phone size over its own size, rounded to four places. Under dir="rtl" the same factor applies to the Arabic size, and the Arabic sizes are the Latin sizes times the faces' ratio, rounded per step, so the steps do not keep the Latin proportions. In a muted, dense system for children the Arabic hero came out at 28.0px on a phone and the landing display at 27.8px, and the phone-hierarchy check refused the system. In about one Arabic system in a hundred a phone style fell under the one below it, and in about three in ten it sat less than 1px above it.

## Decision

The Latin phone size of each style is set as before. Then, from section-title up, each factor is raised to the smallest value that keeps the style at least 1px above the phone size of the style below it (heading-2 at its own size for section-title) in every script the system carries: Latin, and Arabic when the system carries Arabic. A factor is never below the one the Latin rule gives and never above 1. The factors are computed exactly and rounded to four places at the end. If a style at its own size still could not clear the style below it in a script, it keeps factor 1 and the styles below it come down instead, each to 1px under the one above.

## Why

The rule is continuous in the sizes, so no system, face pair or script needs a case of its own, and it only raises a factor where a script needs it: a Latin-only system keeps its factors, and so does an Arabic system whose rounded sizes already keep the step. The fallback is never reached by a generated system: every step from body up rises by whole pixels in both scripts (the 1.08 floor between levels), so a style at its own size is at least 1px above the next style's size, and so above that style's phone size. Rounding a factor to four places moves a phone size by at most half of 1e-4 of the size, under 0.01px below 200px, so two neighbours 1px apart can never tie.

## What it touches

typography.hold_phone_order, phone_factors, generate_type and the type.phone-scale tokens; the phone-hierarchy check is unchanged.

## Consequences

In an Arabic system whose rounded sizes would break the step, one or more of the largest styles is a little larger on a phone, in both scripts, since the factor is shared. In the brown, muted golden system the hero's factor moves from 0.75 to 0.7579, and its Latin phone size from 24px to 24.25px, so the Arabic hero sits 1px above heading-1 on a phone instead of 0.7px.
