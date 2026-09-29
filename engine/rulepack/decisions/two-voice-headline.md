---
id: two-voice-headline
title: A two-voice headline takes its gap in weight, style and tone from the axes
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# A two-voice headline takes its gap in weight, style and tone from the axes

## Context

Confident headlines often speak in two voices: the main words, then an emphasised phrase lighter, in italic or in a quieter tone. A page that invents the second voice by hand picks a second face or a color that fails contrast.

## Decision

type.text.display-emphasis is the display at its size, face and leading, lighter by typography.emphasis_gap: 100 plus 200 times character.emphasis_contrast (0.55 type personality plus 0.45 contrast), snapped to hundreds, never under 300 so it holds at a phone size, and within what the face ships. type.emphasis.italic is 1 when the emphasis contrast is 0.5 or more and the display face ships a true italic, else 0, and always 0 under right to left; the faces link and self-host file then load that italic. type.emphasis.tone is the emphasis contrast, the share to mix from color.text.default toward color.text.muted, so the words stay at the text minimum wherever both already meet it. The voice takes the display's phone and tier factors.

## Why

The same family keeps one headline; a gap from the axes keeps it continuous, so a geometric, muted brand gets a quiet gap and a humanist, bold one a wide one.

## What it touches

typography.ROLES, EMPHASIS_GAP, ITALIC_FROM, emphasis_gap, emphasis_italic, FOLLOWS and the type.emphasis tokens; character.emphasis_contrast; fonts.Face.italic, css2_family, italic_families, cdn_url, self_host_css; guidance/type.md.

## Consequences

A page sets the emphasised words in type.text.display-emphasis and mixes their color by type.emphasis.tone; it never adds a second display face for them.
