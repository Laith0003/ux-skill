---
id: type-three-faces
title: Twelve text styles in three faces, display, text and mono
status: active
areas: [type]
supersedes: type-roles
superseded_by: null
---

# Twelve text styles in three faces, display, text and mono

## Context

One face for headings and body in every system makes the hero of a playful restaurant and of a formal bank the same shape, and a scale that jumps from a 54px hero to a 24px heading-2 has nothing for a section title or a price.

## Decision

Type has twelve composite styles: hero, heading-1, section-title and figure in the display face; heading-2, heading-3, body, body-small, ui and fine in the text face; label in the mono face when the system reads technical (character.technical at 0.5 or more) and in the text face otherwise; code in the mono face. Each Latin face has an Arabic partner, and the display styles take the Arabic display partner under right to left. type.run.latin and type.run.arabic name the face for a run in the other script. Emphasis inside a style is type.strong.

## Why

A display face gives the largest statements character without costing reading; a section title and a figure style fill the two gaps the site trials hit. A label in the mono face is the metadata voice a technical product expects, and a warm one keeps it in the text face.

## What it touches

typography.ROLES, FACE_TOKENS, RUNS, generate_type; fonts.choose.

## Consequences

A page that ships Arabic loads up to five faces. The face table in /ux-system and the report name the faces chosen.
