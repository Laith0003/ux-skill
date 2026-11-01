---
id: media-veil
title: Text on generated art sits on a veil of the page color, measured over the art's own colors
status: active
areas: [color, imagery, contracts]
supersedes: null
superseded_by: null
---

# Text on generated art sits on a veil of the page color, measured over the art's own colors

## Context

The full-bleed hero of the restaurant trial put its headline over the generated art with the photo scrim, black at 0.56 alpha, which the build sizes for the worst photo, a white one. Over light pastel art it turned the page into grey-brown mud, and with no role for a control on media the secondary button took the link color and could not be read on it.

## Decision

The build knows every color its art draws (color.decorative.brand, support and neutral over the page), so text over the art gets its own pair of roles. color.text.on-media is the page's text color. color.media.veil is the page's own color at the least alpha, in 1/255 steps, at which color.text.on-media reaches 4.5:1 over every art color laid under the veil, 7:1 under high contrast; in each of the four color contexts, so it follows the scheme like the art does. The media-veil check measures it. A control on media draws its label, edge and focus ring in color.text.on-media over the art, and in imagery.on-scrim over a photo under imagery.scrim; the button contract says so. The photo scrim is unchanged.

## Why

The veil is weighted by the art's lightness: light art under dark text needs little or no veil and keeps its colors, and dark art in dark mode takes just enough. A veil of the page color reads as part of the page, never as fog, and text that already reads on the page reads on it. The text minimum is above the 3:1 a control's edge and ring need, so one role serves the text and the control.

## What it touches

color.ART_ROLES, over, veil_alpha, the veil primitives, SEMANTIC and HIGH_CONTRAST for color.media.veil and color.text.on-media, COVERAGE_EXEMPT and the media-veil check; contracts/seed/button.yaml; guidance/color.md and imagery.md.

## Consequences

A hero over the generated art needs no scrim; its veil can be fully transparent. A page that swaps the art for a photo switches to imagery.scrim and imagery.on-scrim.
