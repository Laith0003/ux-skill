---
id: lint-reads-dashboard-templates
title: Lint reads dashboards as admin templates build them
status: active
areas: [output, motion]
supersedes: null
superseded_by: null
---

# Lint reads dashboards as admin templates build them

## Context

Run over fourteen public admin dashboards (Tailwind 4, Bootstrap and Material builds), five rules reported what the code does correctly. A Tailwind 4 build wraps its utilities in @layer, and a rule that matches a class name lands on the selector, before the rule's brace, so the unused utility check never saw which class it was; the shadcn dashboard example drew 87 findings on utilities no element uses. Tailwind composes every shadow and ring as box-shadow: var(--tw-inset-shadow), var(--tw-inset-ring-shadow), var(--tw-ring-offset-shadow), var(--tw-ring-shadow), var(--tw-shadow), five custom properties read as five layers, so even shadow-none was reported. Every reset writes button:not(:disabled) { cursor: pointer }, the right way round, and the pointer rule read the :disabled inside :not() as styling disabled controls. A menu whose :focus-visible rule swaps the outline for a fill was reported as having no focus indicator, and a checkbox mark drawn on ::before at opacity 0 was reported as a hidden control.

## Decision

The unused utility check reads a match on a rule's selector as belonging to that rule, inside an @layer or @media too (structure.rule_at). box-shadow-multilayer-default counts only the layers a box-shadow draws itself: a layer that is only a custom property draws nothing there, and its value is judged where it is defined (shadow-drawn-layers, five layers or more). cursor-pointer-on-disabled reports :disabled only outside :not(). In a focus rule, a fill, a text color or an underline in place of the outline counts as a visible indicator, as an outline, a box-shadow or a border already did. An opacity of 0 on a pseudo-element is never a hidden control, since a pseudo-element takes no focus.

## Why

A finding should point at something a person would change. Each of these fired on code that already does the right thing, on most of the dashboards an AI builder starts from, and buried the real problems (links that go nowhere, icons screen readers announce, images that shift the layout) under them.

## What it touches

engine/linter/structure.py (rule_at, unused_utility, outline_without_ring, shadow_drawn_layers); engine/linter/components.py (focusable_hidden_by_opacity); data/anti-patterns.json (box-shadow-multilayer-default post, cursor-pointer-on-disabled pattern); tests/test_lint_dashboards.py; the corpus cases and probe misc/dash1.html.

## Consequences

175 fewer findings over the fourteen dashboards, 87 of them on the shadcn dashboard example. A focus rule that only removes the outline, a control at opacity 0, five drawn shadow layers and a pointer on a disabled control are reported as before. A fill counts as a focus indicator whatever its contrast; WCAG 2.4.7 asks for a visible indicator, and this check does not measure how visible.
