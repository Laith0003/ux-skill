---
id: type-size-names
title: A size named for a text role is proposed as that role's font size alone
status: active
areas: [type, contracts]
supersedes: null
superseded_by: null
---

# A size named for a text role is proposed as that role's font size alone

## Context

Many systems keep type as separate tokens per field: type.size-body, font-size-display, fontSize.h1, with families, weights and line heights elsewhere or nowhere. The engine's text roles (type.text.body and the rest) are composites of five fields, and the mapping can map them one field at a time.

## Decision

propose() maps a dimension token whose name says type, font or text, then size, then a text role's own name (type.size-body, font-size-display, text-size-label, fontSize.h1) to that role's fontSize field, by name, with the vocabulary "type size names" (adapter.TYPE_SIZES). The role names are the engine's own: display, hero, h1 to h3 and heading-1 to heading-3, section-title, figure, body, body-small, ui, ui-large, label, fine and code. Only fontSize is proposed; the other four fields wait for the owner, and the view's note names each one. A bare size name (size-display, sizes.label) does not say it is type, so it is not proposed; enhance names each one with the role it names and how to map it (adapter.unclaimed_sizes). A scale step or a word that is no role's own name (size-md, size-base, size-small, size-lead) is left to the owner. A token of another type is never proposed.

## Why

A size name says one field and nothing more, so proposing the rest would be a guess the owner has to undo. Mapping the field it does say starts the role and tells the owner exactly what is left.

## What it touches

adapter.TYPE_SIZES, adapter.propose, adapter.unclaimed_sizes, adapter.VOCABULARY_EXAMPLES, enhance's decisions; commands/ux-system.md.

## Consequences

An import of a system with type.size-* tokens proposes its text roles field by field; enhance lists those roles as not checked until the owner maps the remaining fields.
