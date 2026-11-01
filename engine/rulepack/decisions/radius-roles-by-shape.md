---
id: radius-roles-by-shape
title: Eight radius roles follow structure, and a check box's box and a field of several lines never become pills
status: active
areas: [radius]
supersedes: radius-roles
superseded_by: null
---

# Eight radius roles follow structure, and a check box's box and a field of several lines never become pills

## Context

Soft brands move chips, then controls, to the pill shape. A check box bound to the chip corner became a circle and read as a radio button, and a textarea bound to the control corner became a stadium that clipped its first and last lines.

## Decision

Radius has eight roles that say what a shape is: radius.joined for shared edges, radius.chip, radius.control, radius.box, radius.area, radius.card, radius.dialog and radius.pill, plus radius.media for photos. radius.box is half the control corner at every roundness (radius.1), for a check box's box and other small square marks. radius.area is the control corner while controls are rounded rectangles and the card corner once they are pills, for a field that runs to several lines. The geometry axis sets the base corner and the scale is fixed multiples of it. There are no softer or sharper variants of a role.

## Why

A corner tells people what kind of thing they are looking at. A square box and a round dot are how a check box and a radio button differ at a glance, so the box never follows the chip to a pill; a paragraph needs a rectangle, so a field of several lines never follows the control to one.

## What it touches

radius.py roles(); guidance/radius.md; the checkbox, textarea and text-field contracts.

## Consequences

A component takes its radius from its structural role, and the radius never changes between states. A softer or sharper look is a change to the geometry axis, not a new role.
