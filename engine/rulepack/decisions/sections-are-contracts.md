---
id: sections-are-contracts
title: A page's sections are contracts that compose component contracts
status: active
areas: [contracts, layout]
supersedes: null
superseded_by: null
---

# A page's sections are contracts that compose component contracts

## Context

The page sequences named their sections in prose, and the landing playbook restated each section's widths per composition. An agent building a page had a name and a paragraph, not a structure it could check, and the widths drifted from the system's roles.

## Decision

A contract of category section carries, besides the component fields, its job (one sentence saying what it must prove), slots that take component contracts (the seeds, or one beside the section in its own folder) or media (photograph, interface-fragment, logo, text), variants named by what differs (media, alignment, density), token-role bindings only, a proof requirement (none, or the proof kinds it needs and the reason it drops without them), and a phone recomposition in a fixed order: drop decorative layers, fold side columns into the text stack, pair small items two to a row, turn three or more plans into a plan switcher with the recommended plan preselected, and recrop interface fragments instead of shrinking them. A slot that takes an interface fragment needs a slot that takes a photograph, and a media variant value that shows a fragment names the photograph too (photograph-and-fragment). Fourteen seeds ship in engine/contracts/seed/sections/. Every page-sequence section names its contract or is marked prose-only; a section whose proof the client lacks keeps its place when its contract takes another kind the client has, and otherwise drops with its contract's reason; and the landing compositions name the contracts and their variants instead of restating widths. A section's container is a band of the page, set apart by space or its ground, so it needs no edge. engine/contracts/sections.py renders a section from its bindings, and a render test holds each at 1440 and 390 to no overflow, 24px targets (2.5.8) and one h2 (the two heroes carry the page's h1).

## Why

A section is where components meet the page's argument. Making it a contract gives the same guarantees the components have: every value is a role the system builds, the proof rule is checked, and the phone layout follows one order.

## What it touches

engine/contracts/schema.py (SECTION_KEYS, PHONE_ORDER, MEDIA_KINDS, SectionSpec); engine/contracts/library.py; engine/contracts/bind.py; engine/contracts/sections.py; engine/contracts/seed/sections/; data/page-sequences.json; engine/page_sequence/core.py; references/surfaces/landing.md; engine/foundations/distinct.py (GLANCE_FLOOR, features_shown).

## Consequences

The hero built under five corners of the axes stays above the glance floor on what it shows; a section of neutral text and space reads closer across briefs, by design. Split media-and-text rows stay prose-only, held to at most two in a row by the lint.
