---
id: display-contracts-measured
title: Chips, badges, links, navigation, progress and tables are measured where they sit, and the table binds its phone layout
status: active
areas: [contracts, border, motion, direction]
supersedes: display-and-navigation-contracts
superseded_by: null
---

# Chips, badges, links, navigation, progress and tables are measured where they sit, and the table binds its phone layout

## Context

The six display contracts passed every pairing they declared, but some of what they drew was not declared. The empty progress track was visible only because color.line.subtle happened to sit far enough from the surfaces; nothing measured it, and in a third of the light builds it did not. The progress value was a fixed left to right run, which puts an Arabic value's number after its words. Stripes matched the raised surface exactly in dark high contrast, and a hovered striped row did not change. The table's phone layout was one sentence with nothing bound, the chip's remove button and the table's rows had no focus, and the open navigation menu had no surface of its own.

## Decision

Six contracts ship at experimental: chip, badge, link, nav, progress and table. What each draws is paired where it sits:

- progress: the empty track's edge is color.line.input, paired at 3:1 with every surface; the value keeps the page's direction; the bar grows with motion.expand; a spinner that can run longer than 5 seconds sits beside a control that pauses or cancels the work.
- table: it names one surface, the card. Plain rows take border.separator in color.line.subtle; a striped row takes border.outline, since its fill can match the card. A hovered row takes the sunken fill and a color.line.input edge, so a striped row changes too. A layout variant (grid, scroll, stacked) binds the phone layout: in scroll the region takes focus and the first column sticks at the inline start with elevation.order.sticky, its row's fill in every state and a divider at its end; in stacked each value has a label in type.text.label and color.text.muted. Below the tablet breakpoint a table of four columns or fewer keeps the grid. Rows take focus.
- chip: an input chip's remove button shows its own ring, and its icon is paired with the hover and chosen fills. A chip holds a value a person added; a read-only tag, which type.md sets in type.text.label, is a badge.
- nav: the collapsed layout binds a menu on the raised surface with its edge, shadow and layer, and the items, underline and rings are paired with raised as well as the page. The button states aria-expanded and aria-controls, and Escape closes the menu.
- link: the underline is drawn under the words with text-decoration, never at the edge of a standalone link's 44px target, where it floats a line away from them. A link has no disabled state; it is present or absent.
- badge: unchanged.
- Every contract with more than one part that can hold focus says that only the part holding focus draws its ring.

## Why

What a person needs to see has to be measured in every context on every surface it sits on, or it holds by luck and a later color change can break it without a test failing. A number wrapped in a fixed run reorders a sentence in Arabic. A phone layout that is only a sentence leaves every build to invent the sticky cell, which then shows the cells scrolling under it.

## What it touches

engine/contracts/seed/chip.yaml, link.yaml, nav.yaml, progress.yaml and table.yaml, and the one-ring line in status-banner.yaml; guidance/border.md; commands/ux-system.md lists the contracts; tests/contracts/test_contract_findings.py.

## Consequences

There are eighteen seed contracts. A table placed straight on the raised surface loses its stripes in dark high contrast; the contract says to put it in a card.
