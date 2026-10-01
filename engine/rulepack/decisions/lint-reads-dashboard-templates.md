---
id: lint-reads-dashboard-templates
title: Lint reads dashboards as admin templates build them
status: active
areas: [output, elevation]
supersedes: null
superseded_by: null
---

# Lint reads dashboards as admin templates build them

## Context

Run over fourteen public admin dashboards (Tailwind 4, Bootstrap and Material builds), five rules reported what the code does correctly. A Tailwind 4 build wraps its utilities in @layer, and a rule that matches a class name lands on the selector, before the rule's brace, so the unused utility check never saw which class it was; the shadcn dashboard example drew 87 findings on utilities no element uses. Tailwind composes every shadow and ring as box-shadow: var(--tw-inset-shadow), var(--tw-inset-ring-shadow), var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow), five custom properties read as five layers, so even shadow-none was reported. Every reset writes button:not(:disabled) { cursor: pointer }, the right way round, and the pointer rule read the :disabled inside :not() as styling disabled controls. A menu whose :focus-visible rule swaps the outline for a fill was reported as having no focus indicator, and a checkbox mark drawn on ::before at opacity 0 was reported as a hidden control.

## Decision

The unused utility check reads a match on a rule's selector as belonging to that rule, inside an @layer or @media too, and a brace inside a quoted attribute value does not end the selector (structure.rule_at). box-shadow-multilayer-default counts the layers a box-shadow paints (shadow-drawn-layers, five or more): a layer that is a lone var() is read through the page's custom properties, its most layered value counted, so var(--elev) holding five layers is five; a layer with no offset, blur or spread, or in a fully transparent color, paints nothing, which leaves Tailwind's composed shadows at the layers they draw. The rule also matches a box-shadow made of var() so that case is read at all. cursor-pointer-on-disabled reports a rule only when a :disabled sits outside every :not(...) argument (pointer-on-disabled), so button:not(*:disabled) and button:not(.x, :disabled) pass. In a focus rule, a fill, a text color or an underline in place of the outline counts as a visible indicator, as an outline, a box-shadow or a border already did, in the rule that removes the outline or in another focus rule covering it (fill_kind); a transparent color, a keyword that keeps the current color, and a var() the page does not define do not count. An opacity of 0 on a pseudo-element that draws a part of an element (::before, ::after, ::placeholder, ::marker and the like) is never a hidden control; ::part() and ::slotted() select real elements and are read as before.

## Why

A finding should point at something a person would change. Each of these fired on code that already does the right thing, on most of the dashboards an AI builder starts from, and buried the real problems (links that go nowhere, icons screen readers announce, images that shift the layout) under them.

## What it touches

engine/linter/structure.py (rule_at, unused_utility, resolved, fill_kind, outline_without_ring, _rings, drawn_layers, shadow_drawn_layers, pointer_on_disabled); engine/linter/components.py (focusable_hidden_by_opacity); data/anti-patterns.json (box-shadow-multilayer-default pattern and post, cursor-pointer-on-disabled post); tests/test_lint_dashboards.py; the corpus cases and probe misc/dash1.html.

## Consequences

166 fewer findings over the fourteen dashboards, 87 of them on the shadcn dashboard example. A focus rule that only removes the outline, a control at opacity 0, five drawn shadow layers and a pointer on a disabled control are reported as before. A fill counts as a focus indicator whatever its contrast; WCAG 2.4.7 asks for a visible indicator, and this check does not measure how visible.
