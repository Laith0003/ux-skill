---
id: brief-fields
title: Who the product is for arrives as structured fields, and every effect is reported
status: active
areas: [output, type, layout, border, space]
supersedes: null
superseded_by: null
---

# Who the product is for arrives as structured fields, and every effect is reported

## Context

Words such as over 60, Arabic-speaking or dark by default sat in free text the engine ignored, and the report then said nothing needed doing. Guessing from free text would be a keyword table by another name.

## Decision

The brief carries six structured fields beside the seven axes: age, languages, primary_script, default_scheme, reading_context and brand_role, each from a fixed list. The host AI fills them from the user's words; the engine never parses free text for them. Older and mixed-age readers get body text 17 or 18px, targets 46 or 48px, a focus ring 1px wider, up to 3px at standard contrast (decisions/ring-room.md), and compact density refused; on-the-go use adds 4px to targets; long reading adds 0.1 to body line height and narrows the measure to 34rem; languages decide whether Arabic ships, and a language in Arabic script with the Latin-only flag is refused. The report lists each change with its reason, and names every brief word that changed nothing with how to pass it.

## Why

Structured fields keep the mapping exact and testable, and the host AI is good at turning plain language into them. Reporting unread words stops a brief from silently losing what matters to it.

## What it touches

engine/foundations/audience.py (FIELDS, AGES, effects, HOW_TO_PASS); emit.read_brief, brief_audience, resolve_arabic, unread_lines and the report sections Who it is for and What the engine did not read; the type, layout, border and space generators.

## Consequences

The /ux-system command tells the host AI how to fill each field. A field with a value outside its list is refused, naming the field and the choices.
