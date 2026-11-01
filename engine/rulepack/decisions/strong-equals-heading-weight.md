---
id: strong-equals-heading-weight
title: Emphasis inside text uses the heading weight
status: superseded
areas: [type]
supersedes: null
superseded_by: strong-weight
---

# Emphasis inside text uses the heading weight

## Context

A system can give emphasis inside body text its own weight between regular and the heading weight, or reuse the heading weight.

## Decision

type.strong aliases the same weight as the headings: 600, or 700 when the brand's contrast axis is 0.66 or more; it does not change under contrast:high. There is no separate emphasis weight.

## Why

Two weights (regular and strong) are what a reader can tell apart in running text; a third weight between them is lost at body sizes. Reusing the heading weight also means one fewer face file for the page to load.

## What it touches

typography.py _weight and type.strong.

## Consequences

Bold words in a paragraph match the heading weight. A heading that needs to stand out from bold body text does so by size, which the type-hierarchy check keeps falling from hero to body.
