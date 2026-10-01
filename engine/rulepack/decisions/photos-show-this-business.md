---
id: photos-show-this-business
title: Photos show what only this business has
status: active
areas: [imagery]
supersedes: null
superseded_by: null
---

# Photos show what only this business has

## Context

The photo direction described a subject by the kind of product ("people at work with the product, the screen implied"). Followed literally, that sentence is a stock search, and it returned the photos that make a page read as generated: a laptop showing charts, a high-five, a stethoscope on white, a glowing lock.

## Decision

The direction asks for the client's own photos first: this place, these people, these goods and this work as they are. Where there are none, the report asks for each shot by what it shows (this counter, this front desk, this crew on this site), and stand-ins are sourced to the direction only until those arrive, listed for replacement. The subject sentences for software and apps name the people who use the product, mid-task, in their own place. The report names the stock cliches to avoid (STOCK_CLICHES), and the search words leave them out.

## Why

A photograph earns its place by showing something true about the business; the subjects every stock search returns first say nothing about anyone. Naming them keeps the direction's words from leading back to them.

## What it touches

engine/foundations/imagery.py (SUBJECTS, STOCK_CLICHES, SEARCH_EXCLUDES, PhotoDirection.query, photo_lines); engine/rulepack/guidance/imagery.md; tests/foundations/test_photo_direction.py.

## Consequences

Every system report gains Source and Avoid lines under Photography, and its search words carry exclusions. Pages still use photographs; this changes which ones.
