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

propose() maps a dimension token whose name says a text role's size to that role's fontSize field, by name, with the vocabulary "type size names" (adapter.TYPE_SIZES): size-display, size-hero, size-h1 to size-h3 and the heading words, size-title, size-body, size-base, size-text, size-small, size-ui, size-label, size-caption, size-fine and size-code, read after a type, font or size group word. Only fontSize is proposed; the other four fields wait for the owner, and the view's note names each one. A scale step (size-md, size-lg) and a word with no role of its own (size-lead) are left to the owner. A token of another type is never proposed.

## Why

A size name says one field and nothing more, so proposing the rest would be a guess the owner has to undo. Mapping the field it does say starts the role and tells the owner exactly what is left.

## What it touches

adapter.TYPE_SIZES, adapter.propose, adapter.VOCABULARY_EXAMPLES; commands/ux-system.md.

## Consequences

An import of a system with type.size-* tokens proposes its text roles field by field; enhance lists those roles as not checked until the owner maps the remaining fields.
