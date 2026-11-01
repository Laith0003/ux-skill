---
id: phone-accepts-local-input
title: A phone field accepts the number as people type it
status: active
areas: [contracts, content]
supersedes: null
superseded_by: null
---

# A phone field accepts the number as people type it

## Context

Phone is the customer's identity in the products this system serves, so the phone field is often the only field on the page. Generated forms give it a pattern that demands a plus and a country code, and a visitor who types their number the way they always do (a leading zero, spaces, no country code) is told it is wrong at the last step, after they decided to act.

## Decision

A phone field accepts the local form the visitor types: spaces, brackets, a leading zero and no country code. The server turns it into the full international number. A field is checked when the visitor leaves it, the error sits at the field and names the field and the fix, and a failed submit moves focus to the first field in error. The lint rule phone-field-requires-country-code fires on a type="tel" input whose pattern accepts none of a set of common local numbers and does accept an international one; a field with no pattern, an optional plus, a computed pattern or one that accepts a local number passes.

## Why

Everyone who reaches the field meant to finish. A pattern that refuses a correct number turns a decision into a failure, and the page never learns why the visitor left. The number is the same number with or without its country code, so the server can add it.

## What it touches

data/anti-patterns.json phone-field-requires-country-code; engine/linter/structure.py phone_rejects_local; references/foundations/component-behaviors.md (Form); tests/lint_corpus/cases/phone-field-requires-country-code, tests/lint_corpus/probes/phone and tests/lint_corpus/dirty.

## Consequences

A product that serves one country may keep a pattern for that country's local form. A product that needs the country picks it with a control beside the field, never by refusing the number. A pattern the rule cannot compile is read by its first token, so a pattern that opens with a required plus is still found.
