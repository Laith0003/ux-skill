---
id: arabic-by-script
title: A language tag is Arabic by its script subtag, else by its language or macrolanguage
status: active
areas: [output, direction]
supersedes: null
superseded_by: null
---

# A language tag is Arabic by its script subtag, else by its language or macrolanguage

## Context

The brief's languages decided Arabic from the primary subtag alone, against seven codes (ar, fa, ur, ps, ckb, sd, ug). Tags a host AI writes for this product's own markets, such as arz (Egyptian), apc and ajp (Levantine), ary, aeb and acm, and any tag with the Arab script subtag (pa-Arab), passed the tag check and built a Latin only system with no error, while the report said none was written in Arabic script. tokens.css switches Arabic subtrees on [lang|="ar"], which never matches lang="arz".

## Decision

A tag with a script subtag is Arabic when that subtag is Arab or Aran (ISO 15924), and not otherwise, so ar-Latn is Latin and pa-Arab is Arabic. A tag without one is Arabic when its language is one of the seven codes or a member of the Arabic, Persian or Pashto macrolanguage as the IANA language subtag registry lists them. The first language decides the primary script by the same rule. For every Arabic tag outside ar and its subtags, the report's "Who it is for" says to mark that text with dir="rtl", since the [lang|="ar"] selector does not reach it.

## Why

The registry and the script subtag already say which tags are written in Arabic script; reading them by that rule covers every variety without a list of dialects to keep up. Refusing a valid variety tag would push the host to rewrite a correct tag; building Arabic and naming the one attribute the page needs keeps the tag and the CSS both true.

## What it touches

audience.MACROLANGUAGE_MEMBERS, ARABIC_SCRIPTS, script_subtag, writes_arabic, Audience.arabic, read_audience and effects; emit.resolve_arabic; guidance/type.md; commands/ux-system.md.

## Consequences

A brief with arz, apc or pa-Arab ships the Arabic faces, sizes and right to left styles, and refuses the Latin-only flag as ar does. A brief with ar-Latn builds Latin only.
