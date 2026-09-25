---
id: brief-fields-checked
title: Languages are tags, an Arabic primary script ships Arabic, and every field gets a line
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# Languages are tags, an Arabic primary script ships Arabic, and every field gets a line

## Context

Three gaps let a brief lose what mattered to it. A language name such as "Arabic" passed as a tag, matched no Arabic language and shipped a Latin only system. A primary script of arabic with no languages left the Latin-only flag unchallenged while the report told the reader to set dir="rtl". Discovery fields the build does not read, such as region and project_type, vanished with no line, and glance reading claimed a change it did not state.

## Decision

A language must be a tag: two or three letters, then optional subtags of up to eight letters or digits. A known language name is refused with its tag ("Arabic" gives "ar"). An explicit primary_script of arabic names Arabic, as an Arabic language does: the build ships Arabic, and the Latin-only flag with it is refused. The right to left line appears only when the build ships Arabic. Every brief field the build does not read gets its own line in "What the engine did not read"; region says to pass what it means as languages and primary_script. Glance reading states the score it adds to the bento composition and whether the page starts from it.

## Why

A report that names every field and every effect is the only way a reader can trust that the brief was read. Names for languages are easy for a host AI to write, so the error gives the fix instead of a silent Latin build.

## What it touches

audience.TAG, NAME_TAGS, read_audience, Audience.arabic and effects; composition.GLANCE_BONUS; emit.resolve_arabic and unread_lines; commands/ux-system.md.

## Consequences

A brief with a language name is refused until it gives tags. A discovery file's region, project_type, reference brands, stack and other answers each get one line in the report.
