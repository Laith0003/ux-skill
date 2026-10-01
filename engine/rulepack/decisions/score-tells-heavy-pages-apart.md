---
id: score-tells-heavy-pages-apart
title: The quality score tells heavy pages apart
status: superseded
areas: [output]
supersedes: null
superseded_by: score-weighs-repeats-past-the-knee
---

# The quality score tells heavy pages apart

## Context

The score subtracted every finding's weight from 100 and stopped at 0. Over a hundred pages from AI builders, 85 scored exactly 0, so the score could not say which page was closer to done.

## Decision

Every finding costs its severity weight. Up to 50 points of penalty the score is 100 minus the penalty, so a clean file is 100, five mediums 80, five highs 50, and a page under 65 fails the gate. Past 50 points the score is 50 times e to the minus (penalty minus 50) over 100: it falls toward 0 and never reaches it.

## Why

A score is useful when it moves as a page gets better. Every page that is already close keeps its number; heavy pages now differ instead of sharing 0.

## What it touches

engine/linter/core.py (compute_score, SCORE_KNEE, SCORE_TAIL); tests/test_lint_precision.py.

## Consequences

Every score of 50 and up is what it was; a heavy page scores above 0 and below every lighter one. A repeated problem costs every time it appears, so the gate still trips on it.
