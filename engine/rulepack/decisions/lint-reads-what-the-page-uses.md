---
id: lint-reads-what-the-page-uses
title: Lint reports what the page uses, not what its bundle carries
status: active
areas: [output, layout]
supersedes: null
superseded_by: null
---

# Lint reports what the page uses, not what its bundle carries

## Context

A page an AI builder ships carries one compiled stylesheet for every route: utilities no element on the page uses, and library rules for toasts and dialogs that are not there. Run over a hundred such pages, about a quarter of the findings sat on rules that matched nothing. The opacity check read a selector made only of attribute tests as matching every element, and guessed from a class name when nothing matched. A dashboard whose header paired its title with a button counted as a landing page and was asked for a photograph.

## Decision

In a file with markup of its own, a finding inside a block whose every selector is one class with its states (a utility such as .h-screen or .md\:grid-cols-3) is dropped when no element carries that class, unescaped, and nothing outside the styles names it, so a class a script adds still counts. A stylesheet with no markup of its own is read whole. The opacity check matches attribute tests and opens one-argument :where() and :is(), and on a page with markup it does not guess for a selector that matches nothing, unless a script names its class or id. A sidebar beside the content marks an app shell before a title and an action can mark a hero.

## Why

A finding should point at something a person sees. Reporting the bundle buried the real problems of each page under the utilities of every other route, and every page scored the same.

## What it touches

engine/linter/structure.py (unused_utility, document_or_app_surface); engine/linter/core.py; engine/linter/components.py (focusable_hidden_by_opacity); tests/test_lint_precision.py; the corpus cases and probes.

## Consequences

Fewer findings on compiled pages: 25 percent fewer over a hundred captured pages, none of them on an element the page has. A utility added only by a script outside the page is not reported in that page.
