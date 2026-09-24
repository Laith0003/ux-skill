---
id: nested-radius
title: A dialog is never less rounded than a card, and inner corners follow the padding
status: active
areas: [radius]
supersedes: null
superseded_by: null
---

# A dialog is never less rounded than a card, and inner corners follow the padding

## Context

A container inside another container can take the same radius as its parent, a smaller one, or one computed from the padding between them. A rule that forbids equal radii outright clashes with cards placed in dialogs at the same step.

## Decision

radius.dialog is at least radius.card; the check allows them equal and the generator makes the dialog one step rounder. An element inset inside a container by padding takes the container radius minus the padding, never the container radius itself. Shared edges between joined shapes are square (radius.joined is 0), and only the exposed outer corners are rounded.

## Why

The inset rule is what keeps nested corners concentric; equal radii at different insets are what look wrong, not equal roles. A dialog that were less rounded than a card inside it would invert the hierarchy the corners express.

## What it touches

radius.py's radius-nesting and radius-joined checks; the card contract's rule for inner media.

## Consequences

An imported system with radius.card equal to radius.dialog passes. Code computes inner corners as calc(outer radius minus padding) rather than reusing a role.
