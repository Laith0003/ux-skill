---
id: strong-weight
title: Emphasis inside text uses the text face's heading weight
status: active
areas: [type]
supersedes: strong-equals-heading-weight
superseded_by: null
---

# Emphasis inside text uses the text face's heading weight

## Context

A system can give emphasis inside body text its own weight between regular and the heading weight, or reuse the heading weight.

## Decision

type.strong aliases the text face's heading weight: 500, 600 or 700 as the contrast axis rises (character.heading_weight), within what the face ships. It does not change under high contrast. There is no separate emphasis weight.

## Why

Two weights (regular and strong) are what a reader can tell apart in running text; a third weight between them is lost at body sizes. Reusing the heading weight also means one fewer weight for the page to load.

## What it touches

character.heading_weight; typography.weights and type.strong.

## Consequences

Bold words in a paragraph match the heading weight. A heading that needs to stand out from bold body text does so by size, which the type-hierarchy check keeps falling from hero to body.
