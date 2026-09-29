---
id: capitals-track-open
title: A display set in capitals tracks at 0 or open, and loud, informal brands lean to it
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# A display set in capitals tracks at 0 or open, and loud, informal brands lean to it

## Context

On 35 measured award pages, 12 of 32 hero headlines were set in capitals, all from the louder half, and capitals and condensed faces tracked at 0 or slightly open while other display type tracked tighter.

## Decision

type.text.display-caps is the display at its size, weight and leading with letter spacing type.tracking.caps: character.capitals_tracking em, 0.005 plus 0.02 times formality, never negative. character.capitals is 0 up to an expressiveness of 0.5 and rises to 1 at 0.9, held back by formality; at 0.5 and above the report calls for capitals. The role takes the display's phone and tier factors.

## Why

Capitals already sit close, so tightening them closes the counters. Tying the lean to expressiveness keeps capitals for the brands the measured pages use them for.

## What it touches

typography.ROLES and the type.tracking.caps primitive; character.capitals_tracking and capitals; guidance/type.md.

## Consequences

A calm brand never gets a capitals display by default; a page that sets capitals uses this role, not the display with its tight tracking.
