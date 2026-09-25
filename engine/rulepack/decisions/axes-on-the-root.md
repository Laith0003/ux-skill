---
id: axes-on-the-root
title: Mode axes switch on the root element only
status: superseded
areas: [output, direction, space]
supersedes: null
superseded_by: direction-on-any-subtree
---

# Mode axes switch on the root element only

## Context

CSS can switch a mode on any element: a dark sidebar, a compact table, an Arabic quote inside an English page. Tokens that vary on two axes at once, such as dark high contrast, can only be restored correctly where both axes are known.

## Decision

Every axis switches on the root element: data-theme, data-contrast, data-density, dir and data-motion on html, or the matching media query when the attribute is absent. Tokens.css writes no rules for a subtree. A dir="rtl" subtree inside a left-to-right page keeps the Latin type; density cannot be scoped to one section.

## Why

A combined override (dark and high contrast) beats single-axis ones on the root by construction. A subtree block could not restore a value that depends on two axes set at different levels, and a page would read one mode's color with another mode's edges.

## What it touches

export.to_css and modes.CSS_AXES; the handoff files in the rule pack, which say where to put the attributes.

## Consequences

A bilingual page sets dir on the root for its main language. Arabic text inside a Latin page sets its font and letter spacing on that element by hand from the type tokens. A dense region inside a comfortable page uses compact values by binding different roles, not by switching the axis.
