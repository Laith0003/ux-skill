---
id: states-name-themselves
title: A state names itself in words a screen reader and a voice user can use
status: active
areas: [contracts, content]
supersedes: null
superseded_by: null
---

# A state names itself in words a screen reader and a voice user can use

## Context

Actions inside repeated items were named by their verb alone, so a list of controls read Save, Save, Save. Disabled menu rows were removed or disabled with the attribute, and a person never learned why. A visited mark leaned on color, and lists that load after the page said nothing while loading or failing.

## Decision

repeated-action-same-name reports buttons or links that share one accessible name across the items of a list, table or feed, once, on the first. menu-row-disabled-without-reason reports a menu row disabled with the disabled attribute, or with aria-disabled and no aria-describedby. The contracts say the rest: a disabled menu row stays visible with aria-disabled and a reason (menu), a visited mark is a glyph with a name, since :visited may change color only (link), and a list that loads after it shows puts loading in an aria-live="polite" region and a failure in a role="alert" region (select, table, menu).

## Why

The accessible name is how a screen reader lists controls and how a voice user picks one; a name shared by every item picks none. A reason in words is the difference between a control that is off and one that is broken.

## What it touches

engine/linter/components.py; data/anti-patterns.json; commands/ux-lint.md; engine/contracts/seed/menu.yaml, link.yaml, select.yaml, table.yaml.

## Consequences

A table of rows with an Edit button each is reported until each button carries its row, for example with a visually hidden span.
