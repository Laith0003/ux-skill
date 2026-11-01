---
id: eyebrow-is-text
title: An eyebrow is text only, with no line, dash or dot before or after it
status: active
areas: [type, color, content]
supersedes: null
superseded_by: null
---

# An eyebrow is text only, with no line, dash or dot before or after it

## Context

type.text.label and color.text.accent name the eyebrow above a heading and say how it is set, but not what may sit beside it. Pages built on the system drew a short line before the label with a ::before of a spacing token's width and a border token's height, and the lint rule for decorative rulers read only pixel widths and heights, so those pages scored 99 while the owner read the mark as generated. The same ornament is built many ways: a pseudo-element with a size or a border, an empty span or i, an edge on the label, a background line, an SVG line or dot, or a dash typed into the text.

## Decision

An eyebrow is text only: type.text.label in color.text.accent or the text color the section uses, and nothing drawn before or after it, whether a line, a dash or a dot. The lint rule decorative-accent-ruler fires on every build of that mark: a ::before or ::after on an eyebrow class that draws a box, a border or a dash character; a short thin pseudo-element line on any selector that is not a control or an icon; a border-inline-start, border-left or background line on the label; an empty span or i, or an SVG that draws one line or one dot, as the label's first or last child or its next sibling; and a dash or bullet typed at the start or end of the label's text. Real separators stay clean: an hr, table rules, a card's own edge, a full-width underline, list markers and icon glyphs.

## Why

The short line before a label is one of the most repeated marks in generated pages, and it adds no structure: the label's size, weight, spacing and color already mark it. A rule that reads only pixel values misses a page built on tokens, which is the page this system produces.

## What it touches

guidance/type.md and color.md (the eyebrow roles and common mistakes); data/anti-patterns.json decorative-accent-ruler; engine/linter/structure.py accent_ruler; references/foundations/typography.md; tests/lint_corpus/probes/ruler and cases/decorative-accent-ruler.

## Consequences

An existing system's label style wins on tracking and case; a mark beside its labels is kept only with the recorded waiver. A brand whose own identity puts a mark beside its labels records that as a waiver on the line (ux-lint-disable-next-line decorative-accent-ruler) with the reason. The rule reads an eyebrow by its class (eyebrow, kicker, overline, pretitle, section-label and their compounds) or by an uppercase, tracked utility list on an element that a heading follows (never a table cell, link, button, label or list item); an eyebrow with neither is judged only by the pseudo-element line check.
