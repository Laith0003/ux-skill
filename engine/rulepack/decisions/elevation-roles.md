---
id: elevation-roles
title: Elevation is four shadows and a stacking order; surfaces are color
status: active
areas: [elevation, color]
supersedes: null
superseded_by: null
---

# Elevation is four shadows and a stacking order; surfaces are color

## Context

An elevation system can bundle depth, background color and shadow into one role per plane. That couples two foundations: changing a surface color means changing an elevation token.

## Decision

Elevation holds four shadow roles (elevation.card, elevation.lifted, elevation.popover, elevation.dialog) and the stacking order (elevation.order.base, sticky, dropdown, overlay, dialog, toast). The surface under a shadow is a color role: page, sunken, card, raised. The dimming behind a dialog is color.scrim, which casts no shadow. A drag lifts an element to elevation.lifted for as long as it is held.

## Why

Keeping the fill in color and the depth in elevation lets each foundation gate what it owns: color measures contrast, elevation checks that each level rises above the one below and that dark shadows are stronger. A component contract joins them explicitly by binding a fill, a shadow and a layer.

## What it touches

elevation.py ROLES and ORDER, the elevation-order, elevation-dark, visible-shadow and stacking-order checks, the card and dialog contracts.

## Consequences

A raised card binds color.surface.raised and elevation.lifted together; neither implies the other. The scrim and the dialog above it are two bindings that appear and leave together.
