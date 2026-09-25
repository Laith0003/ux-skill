---
id: arabic-market-content
title: Arabic copy follows the market for currency, months and fixed runs
status: active
areas: [content, direction]
supersedes: null
superseded_by: null
---

# Arabic copy follows the market for currency, months and fixed runs

## Context

One Arabic page that serves Jordan and Egypt had no rule for writing the currency in Arabic or for naming the month, and a phone number wrapped across two lines with its plus sign at the wrong end.

## Decision

Arabic copy writes the currency as its Arabic abbreviation after the amount, joined by a no-break space (content.md lists them). Months follow the market: the Levant and Iraq use the Syriac names, Egypt and the Gulf the names from the Latin calendar, and a page that serves both writes the Levantine name with the other after it. Every fixed run (a phone number, a code, an amount with its currency) is wrapped with dir set to ltr and white-space nowrap. Arabic letters may appear in content.md and direction.md, the two files that must show them; everything else in the pack stays ASCII.

## Why

A reader in Amman and a reader in Cairo read the same month under different names, and both read a broken phone number as wrong. The rule pack cannot teach Arabic words without writing them.

## What it touches

guidance/content.md, guidance/direction.md; the ASCII tests for guidance and the pack.

## Consequences

A Latin-only build reads none of these lines.
