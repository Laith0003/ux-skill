---
id: type-steps-down-on-phones
title: Breakpoints are reference values, tokens.css switches the tiered roles, and the three largest type styles step down on phones
status: superseded
areas: [layout, type, output]
supersedes: layout-aliases
superseded_by: landing-display-step
---

# Breakpoints are reference values, tokens.css switches the tiered roles, and the three largest type styles step down on phones

## Context

With one size per style at every width, the site trials set a 54 to 67px hero on a 375px phone: a long word ran past its tile, and a five word Arabic headline took three lines. A page could shrink it only with media queries of its own, which copy the breakpoints and break the hierarchy when heading-1 shrinks below section-title.

## Decision

layout.breakpoint.tablet, laptop and desktop stay tokens for exporters and documentation, and tokens.css keeps one alias per tiered layout role (layout.RESPONSIVE) under @media (min-width) at the breakpoints' literal px. The hero, heading-1 and section-title also step down on a phone, every width below layout.breakpoint.tablet. Each has a factor token, type.phone.hero, type.phone.heading-1 and type.phone.section-title: its phone size over its own size. The phone size comes from a phone scale whose ratio is 0.6 of the way from 1 to the system's ratio, at the style's step, at least 1px above the style below it on the phone (heading-2, which keeps its size) and never above its own size. tokens.css writes each style's font-size and letter-spacing as calc(size * var(--<style>-scale)), and sets --<style>-scale to the factor at :root and to 1 from the tablet breakpoint up, in the same blocks as the layout aliases. The Arabic sizes take the same factor. Every other style keeps one size at every width, and sizes stay rem. The phone-hierarchy check keeps each factor above 0 and at most 1 and the phone sizes falling from hero to section-title, above heading-2, in both directions.

## Why

A phone has a quarter of a desktop's width, and the largest styles are the ones that run out of it. A gentler ratio from the same body size keeps the system's character (a bold system still steps harder than a quiet one) and is continuous in the axes. Section-title steps down with heading-1, since heading-1 would otherwise fall under it. Scaling letter spacing by the same factor keeps it in proportion to the size.

## What it touches

typography.PHONE_ROLES, phone_px, the type.phone roles and the phone-hierarchy check; export._lines and to_css; layout.responsive_css; guidance/type.md and layout.md.

## Consequences

A page reads --type-text-hero-font-size as before and gets the phone size below 640px without a query of its own. tokens.json carries the desktop sizes in each style and the factors beside them, so an exporter for another platform applies the factor below its own phone width. A media query of the page's own for anything else still copies the value of layout.breakpoint.tablet.
