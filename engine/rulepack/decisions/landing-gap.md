---
id: landing-gap
title: A landing page spaces its sections with its own gap, 128 to 192px at desktop by density
status: active
areas: [layout, space]
supersedes: null
superseded_by: null
---

# A landing page spaces its sections with its own gap, 128 to 192px at desktop by density

## Context

The landing playbook asks for 128 to 192px between sections at desktop, and the region gap, built for the regions of a product page, is 96px at a mid density, so real landing pages either broke the token or looked cramped. The evidence (three real landing pages, each spacing its sections past the token) supports a role for landing pages over lowering the playbook.

## Decision

layout.landing-gap.<tier> holds the gap between a landing page's sections per tier, on the spacing scale, by density: 80 to 64px on a phone, 96 to 80px on a tablet, 128 to 96px on a laptop and 192 to 128px at desktop, compact one step less. The spacing scale gains space.40 and space.48 for it. tokens.css gives it one alias, --layout-landing-gap, that follows the tier. The layout-regions check keeps it growing with the viewport and never below the region gap at its tier.

## Why

A landing page changes pace between sections; a product page keeps its regions close. Two roles let each keep its rhythm, and the density axis moves both, so an airy brief gets the playbook's top value and a dense one its bottom.

## What it touches

layout.LANDING_GAP, RESPONSIVE, ROLE_TYPES, _regions; space.UNITS; guidance/layout.md and space.md.

## Consequences

The landing playbook's section gap is this token; a page reads var(--layout-landing-gap) instead of a number of its own.
