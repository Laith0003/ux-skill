---
id: eyebrows-follow-formality
title: How many sections carry an eyebrow follows the brand's formality
status: active
areas: [type, layout]
supersedes: null
superseded_by: null
---

# How many sections carry an eyebrow follows the brand's formality

## Context

A small uppercase label above every section heading is the most common tell of a generated landing page. The guidance recommended one per section, and nothing counted them.

## Decision

character.eyebrow_share gives the share of a landing page's sections that may carry an eyebrow: a sixth for a playful brand to a half for a formal one, continuous in formality. The lint rule eyebrows-over-budget counts the sections (every section element not inside another) and the eyebrows (read as decorative-accent-ruler reads them) and reports each eyebrow past the allowance, the share of the sections rounded up and at least one. The formality is read back from the system's photo grade spread, the one token that follows formality alone; with no system the share is a third. A page with fewer than three sections, a docs page or an app surface is not counted.

## Why

An eyebrow earns its place where the heading cannot carry a label, a step number or a category. A formal page labels its parts more; a playful one lets its headlines stand. Eyebrows are never how sections are told apart: space and a change of ground do that.

## What it touches

engine/foundations/character.py (eyebrow_share); engine/linter/taste.py (eyebrows_over_budget, eyebrow_allowance); data/anti-patterns.json; commands/ux-lint.md; tests/lint_corpus/cases/eyebrows-over-budget and tests/lint_corpus/probes/taste.

## Consequences

Six sections with six eyebrows fire on four of them at mid formality. A client's own system that labels every section keeps its pattern: its files are reported apart.
