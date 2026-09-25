---
id: unresolved-pairing
title: A contrast pairing the gate cannot resolve is a failure it reports, and contracts report it too
status: active
areas: [color, contracts]
supersedes: null
superseded_by: null
---

# A contrast pairing the gate cannot resolve is a failure it reports, and contracts report it too

## Context

A set nobody validated can alias a color role at a token that does not exist, or carry overrides that tie in one context. When the gate stopped on the first such pairing, every other pairing went unmeasured and the person saw one error at a time.

## Decision

When a side of a pairing cannot be resolved in a context, the gate records an unresolved-pairing failure for that context, with the alias error's own text naming the token, the alias and the fix, and goes on with every other pairing. A contract bound to a token set reports each unresolved pairing as an unresolved problem: one per pairing and cause, naming the pairing, the alias and its fix, the first context it fails in and how many others, and telling the person to run validate on the token set.

## Why

One pass shows every pairing that cannot be measured beside every pairing that fails, so the fixes come in one round. A contract bound to an edited set is the case where a broken alias is most likely, so it must never pass silently there.

## What it touches

gate.UNRESOLVED_PAIRING and gate.gate; contracts.bind._contrast_problems and _unresolved_problems.

## Consequences

A generated set never reaches this path, because the build runs validate before the gate. An imported or edited set with a broken color alias fails with each affected pairing named once in a contract report.
