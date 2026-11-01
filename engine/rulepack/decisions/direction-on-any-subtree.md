---
id: direction-on-any-subtree
title: Mode axes switch on the root element, and right to left also on any subtree
status: active
areas: [output, direction, space]
supersedes: axes-on-the-root
superseded_by: null
---

# Mode axes switch on the root element, and right to left also on any subtree

## Context

A bilingual page often carries an Arabic block inside an English page, or the reverse. With every axis switched only on the html element, an Arabic block inside a left to right page got only the Arabic run face; its sizes, line heights and display face had to be copied by hand from the style's Arabic values, and the site trial clinic page did exactly that.

## Decision

data-theme, data-contrast, data-density and data-motion switch on the html element, or the matching media query when the attribute is absent. Direction switches there too, and also on any element inside the page with dir="rtl" or a lang that starts with ar: tokens.css writes each override that holds under right to left a second time for the selector :root :is([dir="rtl"], [lang|="ar"]), with every other axis in the override still read from the root (:root[data-contrast="high"] :is(...), and the same under the media query). So the element and everything in it take the Arabic faces, sizes, line heights, weights and travel sign. Density stays whole page.

## Why

A subtree rule restores a combined value correctly when every other axis is known on the root: each subtree rule carries the same attributes and the same specificity order as its root form, so dark high contrast right to left still beats right to left alone inside the block. Direction is the one axis a page mixes by content, so it is the one that follows the content.

## What it touches

export._rules and NESTED_RTL, to_css; guidance/direction.md, type.md and space.md; commands/ux-system.md.

## Consequences

An Arabic block inside a Latin page needs only dir="rtl" and lang="ar" on its element. A Latin block inside an Arabic page keeps the Arabic values it inherits and sets its Latin runs with type.run.latin. A dense region inside a comfortable page still binds compact values through different roles, not by switching the axis.
