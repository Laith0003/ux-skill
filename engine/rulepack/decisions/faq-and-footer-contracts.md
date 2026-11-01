---
id: faq-and-footer-contracts
title: An FAQ accordion and a site footer have contracts, and the footer binds the logo role
status: active
areas: [contracts, color, layout]
supersedes: null
superseded_by: null
---

# An FAQ accordion and a site footer have contracts, and the footer binds the logo role

## Context

Landing pages built on the system each drew an FAQ and a footer with no contract to follow, so each page chose its own question size, target, separators, logo color and legal line. The color foundation already holds color.logo, the exact brand color wherever it clears our 3:1 floor against the page (decisions/logo-and-decoration.md), but only the navigation bound it, so a footer logo took whatever color the page reached for.

## Decision

Two contracts join the seed set at experimental, making twenty. faq-accordion: each question is a button inside a heading, the whole row meets layout.target.min, set in type.text.heading-3, with an icon at the inline end that turns when the item opens; items are separated by one full-width border.separator line in color.line.subtle; the answer is type.text.body within layout.measure.text and opens with motion.expand. site-footer: layout.footer.padding-block, one full-width divider at its block start, the logo in color.logo paired at our 3:1 floor against the page, link columns under type.text.label titles with links at layout.target.min, hover in color.text.link with an underline, and a legal line in type.text.fine and color.text.muted. The footer binds the existing color.logo role; no new color role is added.

## Why

A contract is what keeps two pages built by two agents alike. The logo already has a measured role, and binding it where the logo appears is what makes the brand color survive every mode.

## What it touches

engine/contracts/seed/faq-accordion.yaml and site-footer.yaml; tests/contracts; commands/ux-system.md.

## Consequences

The footer sits on the page surface only: color.logo is held at 3:1 against the page, and on the sunken surface it falls below that for some brands, so the contract does not offer it. The FAQ binds no state for an open item: opening changes what is shown, not a color or an edge, so its cue is the answer itself, the turned icon and aria-expanded, and the state list keeps selected for things a person chooses. Both contracts ship at experimental with a null provenance until a design file holds them.
