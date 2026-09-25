---
id: default-scheme
title: A brief can open the page dark, and color-scheme follows every scheme
status: active
areas: [color, output]
supersedes: null
superseded_by: null
---

# A brief can open the page dark, and color-scheme follows every scheme

## Context

A dark-first product had no way to say so, and without color-scheme native date and select controls stayed light on a dark page.

## Decision

tokens.css writes color-scheme on the root and in every rule that switches the scheme. The default_scheme field decides which scheme opens: system (the default) follows the operating system unless data-theme pins it; dark applies the dark values unless data-theme set to light; light applies them only on data-theme set to dark. Light stays the base value in tokens.json.

## Why

color-scheme is the one property the browser reads to draw its own controls. A dark default that still honors an explicit light choice serves a dark-first product without taking the choice from the reader.

## What it touches

export.to_css (the scheme argument and SCHEME_DEFAULTS); audience.default_scheme; emit.make_system.

## Consequences

A page that opens dark and wants a light toggle sets data-theme set to light on the html element.
