---
id: character-nudges
title: The host AI passes what an unread word means as axis nudges
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# The host AI passes what an unread word means as axis nudges

## Context

The report named every word the engine did not read, and the host AI had no way to say what the word meant, so the only choices were a nearby word with another meaning or nothing.

## Decision

A brief may carry a character object: any of the seven axes (warmth, contrast, density, geometry, formality, motion, type_personality), each a nudge from -0.3 to 0.3 (axes.NUDGE_LIMIT). compute_axes applies the nudges after the industry seed and the words and before the forbidden clamps, holding each axis inside 0 to 1; a nudge never carries to another axis. emit.brief_character refuses anything else, naming the entry and the fix. The axes source line lists the nudges, and system-report.md gives each one a line under "Character nudges": the axis, the nudge, the value the words gave, the value the build used, whether the end of the axis or a forbidden word held it, and the foundations the axis moves (character.INFLUENCE). Every unread tone word's line in the report says how to pass it as a nudge.

## Why

A nudge is a number on the same axes the words already move, so the engine stays continuous and the host AI's reading of a word is stated in the report, where the user can see it and correct it. The limit keeps a nudge a nudge: an axis set by hand belongs in --axes.

## What it touches

axes.NUDGE_LIMIT, _apply_character, compute_axes; emit.CHARACTER_FIELD, brief_character, brief_axes, nudge_lines, unread_lines, render_report, make_system; the CLI and MCP brief descriptions (audience.FIELDS_HELP); commands/ux-system.md.

## Consequences

Two hosts that read one word differently build different systems, and each report says why. A brief of nudges alone builds from 0.5 on every axis.
