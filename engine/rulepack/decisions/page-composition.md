---
id: page-composition
title: A landing page starts from one of five compositions, scored from the axes
status: active
areas: [layout, output]
supersedes: null
superseded_by: null
---

# A landing page starts from one of five compositions, scored from the axes

## Context

Every site trial page had one layout shape, a stack of centered sections, whatever the brief.

## Decision

The build scores five named compositions (split, stacked, bento, editorial-column, full-bleed-media) with linear terms over the axes and the brief's fields: an older audience favors stacked, long reading the editorial column, glancing bento, formality split, warmth and playfulness full-bleed media. The highest score wins, ties by name. The report names the winner, the runner-up and the two terms that decided it, and the JSON result carries the name and every score. The compositions are hooks: the landing playbooks in 4.2 lay out each one.

## Why

A score over the same numbers as the rest of the system gives two briefs of different character different starting layouts without a table per industry, and naming the reason lets a person overrule it knowingly.

## What it touches

engine/foundations/composition.py (SCORES, DESCRIPTIONS, choose); emit.make_system and the report's Page composition section.

## Consequences

This version chooses a composition and names it; it does not lay out the page. A playbook that disagrees states why.
