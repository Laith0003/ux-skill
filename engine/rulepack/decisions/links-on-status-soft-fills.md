---
id: links-on-status-soft-fills
title: Links read on every status soft fill
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Links read on every status soft fill

## Context

A status banner carries an action link on its soft fill, and its contract pairs color.text.link there, but the color gate paired links with the surfaces only. For amber, orange and yellow brands the link measured 4.0 to 4.2:1 on the soft fills in light standard contrast, and the build shipped it.

## Decision

color.text.link joins body and muted text among the roles paired with every status soft fill at the text minimum, 4.5:1 (WCAG 1.4.3) and 7:1 under high contrast (WCAG 1.4.6), so the retune moves the link until it reads there too.

## Why

A link inside an alert is still text people must read; measuring it where the banner puts it closes the gap between the contract and the gate.

## What it touches

color._extra_text_bgs and the pairings build_pairings writes from it.

## Consequences

Warm brands may take a link one step deeper.
