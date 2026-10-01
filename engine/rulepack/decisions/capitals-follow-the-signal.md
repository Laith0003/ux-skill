---
id: capitals-follow-the-signal
title: The system says how far it leans to capitals, and the lint reads it
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# The system says how far it leans to capitals, and the lint reads it

## Context

Every system emits a display-caps role, so a lint that passed capitals whenever the role existed passed them on every system, calm ones included. A calm, formal brand that sets its headline in capitals reads off its own character.

## Decision

The type foundation emits type.capitals (a primitive type.lean.capitals behind it): character.capitals, 0 up to an expressiveness of 0.5 and rising to 1 at 0.9, held back by formality, so it is continuous in energy and formality. all-caps-large reads --type-capitals when the page carries it: under character.CAPITALS_FROM (0.5) a capitals display is reported; at or above it the existing test holds (one of the system's two largest sizes, tracked at 0 or open). A system that does not emit the signal keeps the existing test.

## Why

The decision to set capitals belongs to the brand's character, not to whether a role exists. One number the page carries lets the lint follow that decision without guessing the axes back from other tokens.

## What it touches

engine/foundations/character.py (CAPITALS_FROM, capitals); engine/foundations/typography.py (type.lean.capitals, type.capitals); engine/foundations/composition.py; engine/linter/taste.py (capitals_outside_system); tests/foundations/golden; tests/test_capitals_signal.py.

## Consequences

The generated goldens gain two tokens per system and nothing else changes. A loud page keeps its capitals display; a calm page is told to set its headline in sentence case.
