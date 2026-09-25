---
id: sentence-names-the-shown-face
title: The character sentence names the display face the page shows
status: active
areas: [type, output]
supersedes: null
superseded_by: null
---

# The character sentence names the display face the page shows

## Context

The report opens with one character sentence that names the display face. On an Arabic-first system the page opens right to left, and every display style there is set in the Arabic display face, so a sentence naming only the Latin display face described a face the page barely shows.

## Decision

When the primary script is Arabic and the set has an Arabic display face, the sentence reads "<Arabic display face> sets the Arabic display type and <Latin display face> the Latin". Otherwise it names the Latin display face alone, as before. The faces are read from the built tokens.

## Why

The sentence exists so a person can check what was built at a glance; it must name what they will see first on the page.

## What it touches

emit.character_sentence and make_system; commands/ux-system.md.

## Consequences

An Arabic-first report names two faces in its first line. A Latin-first system with Arabic support still names the Latin face alone, since its pages open left to right.
