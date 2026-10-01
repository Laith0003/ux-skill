---
id: score-weighs-repeats-past-the-knee
title: Past the knee the quality score counts a repeated rule lightly
status: active
areas: [output]
supersedes: score-tells-heavy-pages-apart
superseded_by: null
---

# Past the knee the quality score counts a repeated rule lightly

## Context

The score cost every finding its full severity weight and decayed past 50 points of penalty. Over 114 real pages (fourteen public admin dashboards and a hundred pages from AI builders), 35 scored 1 or 2, among them almost every admin template: Tabler's demo has 149 links to "#", one pattern repeated, and each copy cost as much as a new problem. A score that rates nearly every real dashboard the same cannot show a team which one is better or that a fix helped.

## Decision

Every finding costs its severity weight. Up to 50 points of penalty the score is 100 minus the penalty, so a clean file is 100, five mediums 80, five highs 50, and a page under 65 fails the gate. Past 50 points the score is 50 times e to the minus (excess over 100), where the excess is the penalty over 50 scaled by the repeated penalty over the full one. The repeated penalty counts the n-th finding of a rule in a file at 1/n of its weight, heaviest first; repeats are counted within a file, so the same page scanned twenty times scores as one page. A page whose findings are all different rules has a repeated penalty equal to its full one and scores as before.

## Why

A rule that fires 149 times is one pattern to fix, often in one template, not 149 problems; it should weigh more than one finding and less than 149 different ones. Keeping every score of 50 and up exactly as it was keeps the gate and every near-clean page where they were. Over the 114 pages, scores of 1 or 2 fell from 35 to 11 and distinct scores rose from 45 to 49, with no score of 50 or more changed.

## What it touches

engine/linter/core.py (compute_score, SCORE_KNEE, SCORE_TAIL); tests/test_lint_precision.py.

## Consequences

A heavy page with many repeats of a few rules scores above a heavy page of as many different problems. Removing any finding, a repeat included, never lowers the score.
