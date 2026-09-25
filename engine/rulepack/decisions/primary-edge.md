---
id: primary-edge
title: The primary button's edge carries its contrast against the page
status: superseded
areas: [color, contracts]
supersedes: fill-edge-page-only
superseded_by: fills-on-every-placement
---

# The primary button's edge carries its contrast against the page

## Context

Holding the primary fill and its hover and pressed steps to 3:1 against the page moves the brand fill for every bright brand, and a move for the page alone costs the brand everywhere the button appears.

## Decision

color.action.primary-edge is the primary button's edge: the fill itself when the fill measures 3:1 against the page (our 4.5:1 floor under high contrast), otherwise the step of the fill's ramp nearest the fill that does. It is paired with the page only (WCAG 1.4.11). The fill and its states carry only the text on them. The danger fill and the strong status fills keep their own pairing against the page. On card, sunken and raised a filled control is found by its label, its edge and its focus ring.

## Why

The edge identifies the control, which is what WCAG 1.4.11 asks of a boundary; the fill is free to stay the brand color. Where the fill already clears the page the edge is invisible, so the button looks the same as a borderless one.

## What it touches

color.PAIRINGS, GROUPS (the edge field), _choose_edge; the button contract's primary edge binding.

## Consequences

The button contract binds border-width and border-color on every primary neutral button. A primary button on card, sunken or raised is identified by its label, edge and ring, as before; its fill is still not paired there.
