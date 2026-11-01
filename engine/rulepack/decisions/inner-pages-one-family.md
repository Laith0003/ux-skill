---
id: inner-pages-one-family
title: Inner pages have their own sequences and share one header, closing band and footer
status: active
areas: [layout, content]
supersedes: null
superseded_by: null
---

# Inner pages have their own sequences and share one header, closing band and footer

## Context

The page picker built home pages, feature pages and campaign pages. A site also needs its pricing, about, contact, customers, customer story and legal pages, and generated inner pages restate the home page's hero and invent their own headers and footers, so the site reads as several templates.

## Decision

The brief's page field takes pricing, about, contact, customers, customer-story and legal, and each picks its own sequence (page_sequence.INNER_PAGES), before the stage is read, so a legal page stays a legal page before launch. Every inner sequence opens on a secondary hero that names the page, says in one line what it holds and offers one action, and ends on the site's own closing band and sitemap footer. Pages built in one run are one page family: one header, one closing band and one footer instance shared by all of them. The pricing page turns a comparison of three or more plans into a plan switcher on a phone that keeps the row labels and preselects the recommended plan. Proof sections on the customers and customer story pages drop, with their reason, when the client has no proof of that kind, and every proof section drops with the pre-launch reason when the stage is pre-launch. A section that needs a contact route (the contact page's Where to find us needs an address) drops with its reason when the brief's contact list lacks it.

## Why

A structured field picks the page, never a word of the brief or an industry. The frame repeated across pages is what makes several pages one site.

## What it touches

engine/page_sequence/core.py (PAGES, INNER_PAGES, select_for_brief); data/page-sequences.json (six sequences); references/surfaces/landing.md (Pages of one site); commands/ux-design.md (the page field); tests/test_page_sequence_inner.py.

engine/page_sequence/family.py builds a family's skeleton pages in one run: the header, closing band and footer are written once and placed on every page, the header marking its own page with aria-current; tests/test_page_family_render.py renders three of them at 1440 and 390.

## Consequences

An inner page never repeats the home page's hero claim. A page family built across two runs has to reuse the first run's header and footer by hand.
