---
id: moves-answer-at-once
title: Every move answers at once, a direct response half done in 70ms and an entrance in 140ms
status: active
areas: [motion]
supersedes: null
superseded_by: null
---

# Every move answers at once, a direct response half done in 70ms and an entrance in 140ms

## Context

A nominal duration says little about how a move feels: 620ms on a strong ease-out reaches half its travel in about 70ms, while 400ms on a symmetric curve takes 200ms. A study of an interaction-detail site measured its best moves by when they reach half and nine tenths of their travel.

## Decision

motion.settle_ms(duration, curve, fraction) is when a move on a cubic-bezier first reaches a share of its travel, searching the curve's parameter and bisecting, so an overshooting curve counts its first arrival. response-head, our rule: press, state, swap and indicator reach 50 percent within 70ms and 90 percent within 220ms, and reveal, expand, arrive, page and expressive reach 50 percent within 140ms, in standard motion; reduced motion keeps its own caps. A failure names the role, the time, the duration and curve, and the fix: a shorter duration or a stronger ease-out.

## Why

Longer, calmer durations from the measured pages only work when the head of the move is quick; the check keeps every generated role there at every corner of the axes and catches an edited curve that is not.

## What it touches

motion.settle_ms, DIRECT, ENTRANCES, DIRECT_T50, DIRECT_T90, ENTRANCE_T50 and the response-head check; guidance/motion.md.

## Consequences

An existing system's own durations and curves are read, reported and never replaced.
