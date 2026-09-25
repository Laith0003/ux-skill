---
id: imported-sets-pass
title: A set the engine did not generate passes the same gate, a role it lacks is skipped, and only strict fails it
status: active
areas: [color, space, radius, border, elevation, motion, layout, type, imagery]
supersedes: null
superseded_by: null
---

# A set the engine did not generate passes the same gate, a role it lacks is skipped, and only strict fails it

## Context

An edited tokens.json or an imported system has the core roles its authors needed and none of the character roles the engine adds: brand, tint, band, stripe, header and code surfaces, the buttons on a brand band, the primary edge, the landing gap, the landing display step and its fit factors, the phone scale, icons, page regions, field and table spacing. It may also lack one of our mode axes. A gate that failed every missing role would fail every real system, and one that raised on the first problem would show one fix at a time.

## Decision

check_system validates the set and gates it through gate_foundations, the same gate build_system uses, and returns the structural problems and the gate report together without raising. It checks the foundations whose root the set has, or the ones named. Each check runs over the axes the set has. A pairing on a role the set does not define is skipped and listed with the gate's skipped pairings, never failed. With strict, each skipped pairing is a skipped-pairing failure that names the missing token and says to define it or map the role to one of the system's tokens.

## Why

A migration is not a redesign: the gate judges what a system has, and a system gains the character roles by extending it, not by failing for their absence. One gate for generated and imported sets keeps the two from disagreeing about the same tokens. strict keeps a test of the complete engine contract in one argument.

## What it touches

build.gate_foundations, build.check_system, build.SystemCheck, build.foundations_in and build.SKIPPED_PAIRING; build_system gates through gate_foundations. typography's rem-sizes check reads right to left sizes only when the set has the direction axis.

## Consequences

A generated set passes check_system with the same counts as its build. A hand-written set with only the core roles passes, and its skipped pairings list every role it lacks. No command passes strict; a caller that wants every role enforced passes it.
