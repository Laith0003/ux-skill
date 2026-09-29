---
id: photo-direction
title: A page uses photographs to a direction the axes set, and every photo on a page shares one grade
status: active
areas: [imagery]
supersedes: null
superseded_by: null
---

# A page uses photographs to a direction the axes set, and every photo on a page shares one grade

## Context

Pages without photographs read as templates, and a page whose photos come from different shoots, one warm and one cold, one bright and one moody, reads as stock. A study of a popular skill's output found its best pages carried by photographs that all share one light. The owner's rule: a page must use photographs, and when the client gives none the skill sources them.

## Decision

imagery.photo_direction gives the look from the axes and the brand color: mean lightness (38 plus 30 times a blend of muted contrast, playfulness and warmth), temperature as CIELAB b* (-6 plus 16 times warmth, leaned by the brand's warm or cool hue), chroma (6 plus 20 times energy held back by formality, plus 4 for a hued brand), contrast as the spread of L* (12 plus 14 times contrast), a black point, grain from type personality and geometry, and energy from energy and motion. The tokens imagery.photo.* hold them, with the grade lock's spreads (lightness 6 to 10, temperature 3 to 5, chroma 4 to 8, tighter for a formal brand). The subject comes from the brief's structured fields: product_type (what the product is), the audience's age and primary_action. The words for a search are read from the quantities by fixed cuts, never from an industry. imagery.grade_problems is the grade lock for lint --render: each photo sits within the spread of the page's own mean, and the page's mean within the direction's ranges. A brand's ban on a kind of photo narrows imagery.PHOTO_KINDS; only a client system that forbids photography removes it, and the report says so. The system report carries a Photography section.

## Why

One grade across photos is what makes a set of images read as one shoot; measuring it gives the render check a number. Continuous quantities keep a calm brand's photos soft and a loud one's vivid without a table of looks.

## What it touches

imagery.PHOTO_KINDS, GRADE_SPREAD, GRADE_TOLERANCE, SUBJECTS, PEOPLE, MOMENTS, PhotoDirection, photo_direction, grade_problems, photo_lines and the imagery.photo roles; emit.make_system and render_report; guidance/imagery.md.

## Consequences

Stock photos are allowed when they pass the direction and the grade lock. Generated art stays for pages the client asks to keep without photographs.
