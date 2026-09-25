---
id: strict-radius-nesting
title: Chip, control, card and dialog grow strictly rounder, and inner corners follow the padding
status: active
areas: [radius]
supersedes: nested-radius
superseded_by: null
---

# Chip, control, card and dialog grow strictly rounder, and inner corners follow the padding

## Context

Shapes nest: a chip sits in a control's row, a control in a card, a card in a dialog. Holding only the card and the dialog let an imported set give a chip rounder corners than the control around it, and a card and a dialog the same rounded corner, which reads as one shape pasted on another.

## Decision

The radius-nesting check reads radius.chip, radius.control, radius.card and radius.dialog from the innermost out: each is strictly less round than the next one the set has. Two square corners may match, since 0 cannot step down. A role at or above 999px (radius.PILL_FLOOR_PX, our pill floor, the same one radius-pill holds radius.pill to) is a pill, a shape of its own, and sits outside the order. An element inset inside a container by padding takes the container radius minus the padding, never the container radius itself. Shared edges between joined shapes are square (radius.joined is 0), and only the exposed outer corners are rounded.

## Why

Each nesting level reads as a level when its corner is visibly tighter than its container's. The inset rule keeps nested corners concentric; equal radii at different insets are what look wrong.

## What it touches

radius.NESTING, PILL_FLOOR_PX and the radius-nesting, radius-joined and radius-pill checks; the card contract's rule for inner media; guidance/radius.md.

## Consequences

An imported system with radius.card equal to a rounded radius.dialog fails and is told to point radius.dialog at a larger step. A square system passes, and so does a control at a 999px pill. Code computes inner corners as calc(outer radius minus padding) rather than reusing a role.
