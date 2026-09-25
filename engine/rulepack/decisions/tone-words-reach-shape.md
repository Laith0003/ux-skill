---
id: tone-words-reach-shape
title: A tone word's formality weight also moves the corners and the type
status: active
areas: [radius, type]
supersedes: null
superseded_by: null
---

# A tone word's formality weight also moves the corners and the type

## Context

The synthesizer turns each tone word into weights on the seven axes. Playful and casual moved formality, warmth and motion but left geometry and type personality at their seed, so a warm and playful brief with no known industry built the same 9px control and 14px card corners as a calm, formal clinic brief, and a text face picked for the middle of the type personality axis.

## Decision

A word's formality weight reaches two more axes in proportion to it: geometry moves by -0.6 times the formality weight, and on the playful side only, type personality moves by 0.5 times its size. A playful word (formality -0.30) rounds the corners by 0.18 and humanizes the type by 0.15; a formal word such as corporate (+0.25) sharpens the corners by 0.15 and leaves the type alone. Words without a formality weight move neither.

## Why

Playfulness shows in shape and letterform as much as in color and motion, and formality shows in crisp corners. Carrying the formality weight through one proportion keeps the reading continuous: two words with close weights move the shape by close amounts, and no word gets its own shape table. Formal type can be a serif or a grotesque, so formality alone does not pick a side of the type axis.

## What it touches

engine/synthesizer/axes.py (word_weights, GEOMETRY_PER_FORMALITY, TYPE_PER_PLAYFULNESS); character.roundness and the face choice read the moved axes; guidance/radius.md.

## Consequences

Briefs with playful or formal words build rounder or sharper corners and, when playful, more humanist faces than before. A brief can still set geometry directly with shape words (rounded, sharp), which add to the same axis.
