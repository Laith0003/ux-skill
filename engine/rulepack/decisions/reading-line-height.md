---
id: reading-line-height
title: Reading styles and code have a line height of 1.5 or more by default
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# Reading styles and code have a line height of 1.5 or more by default

## Context

Some systems set body line heights below 1.5 by default and leave meeting WCAG 1.4.8 to whoever customizes them.

## Decision

body, body-small, fine and code have a line height of 1.5 or more in every system (1.5 to 1.6 by density, taller under right to left), and the reading-leading check blocks a system where they fall below 1.5. Headings and interface labels may be tighter, never 1 or less (decisions/the-full-type-ladder.md).

## Why

Reading comfort is the default, not an option. The check cites 1.4.8, which asks for line spacing of at least 1.5 within paragraphs, and applies it to the styles used for paragraphs. A code block is read line by line like a paragraph, so the check holds code to the same floor; applying 1.4.8 to code is our choice.

## What it touches

typography.leading, READING and LEADING_ROLES, and the reading-leading check.

## Consequences

A dense data view keeps its compact line heights in its ui and heading styles, not by tightening body text or code.
