---
id: first-screen-stays-clear
title: Nothing fixed covers the first screen at rest
status: active
areas: [layout]
supersedes: null
superseded_by: null
---

# Nothing fixed covers the first screen at rest

## Context

A cookie card left floating over the content, a consent wall or a promo bar over the form is the first thing a visitor meets, and it hides the heading and the action the page was built around. It is also the one fault a person names first when they see the page.

## Decision

lint --render measures every fixed panel at rest at every width and reports first-screen-covered when it lies on top of the page's h1 or a form's first control, covers 30% or more of the viewport over text or images, or is a panel at least half the viewport wide floating clear of both edges over them. A transparent fixed wrapper is measured by the painted boxes inside it. A thin bar docked to an edge, a narrow widget, a sidebar beside the content, a layer painted under the page, a drawer its transform parks off screen and an overlay that paints nothing or takes no pointer pass.

## Why

A notice docked to an edge informs; a panel over the content blocks. Measuring what lies on top, where, keeps the rule on what a visitor actually cannot see.

## What it touches

engine/render/core.py (_PARK_JS, the first-screen block); commands/ux-lint.md and commands/ux-design.md check (f); tests/test_render_occlusion.py.

## Consequences

A consent notice is a thin bar on an edge or a dialog the visitor opens. The primary action itself is still checked by its selector in check (f), which this rule does not know.
