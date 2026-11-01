---
id: faces-by-product-type
title: The axes choose each face by distance, and the product type adds how bookish a face should be
status: active
areas: [type]
supersedes: face-choice
superseded_by: null
---

# The axes choose each face by distance, and the product type adds how bookish a face should be

## Context

A face picked by a keyword table repeats across every brief that shares the word. The distance over the axes alone gave a care brief that is trustworthy and friendly a serif display face and a Naskh Arabic face even for an app, since both axes that sit high there (type personality and formality) also describe a book face; nothing said what the product is.

## Decision

engine/foundations/fonts.py holds a small catalog of faces under the SIL Open Font License, each with metrics measured from its files, the weights it ships, its Arabic partner and a place on formality, warmth, roundness, type personality and contrast. For each role the build takes the face nearest the brief's place by weighted distance, ties broken by name; the display face is never the text face. The brief's product_type is the product the page sells, never the page (a landing page for an app is app; the page kind is project_type). It is one closed vocabulary the engine and the page-sequence picker share, in audience.py: PRODUCT_TYPES (app, software, marketing-site, editorial, commerce, marketplace, local-service), PRODUCT_ALIASES (saas and web-app as software, mobile-app as app, shop and store as commerce, b2b-marketplace and b2c-marketplace as marketplace, service as local-service, each reported in one line) and product_type_of, which refuses any other value with the field, the values and the fix. It sets a book depth, audience.BOOK_DEPTH, a per-type scalar like AGES and never a table of faces: 0 for a product people use (app, software, commerce, marketplace, local-service), 0.5 for a marketing site with no product of its own, 1 for editorial. book_target is that depth times the mean of type personality and formality. With a product type, each face adds BOOK_WEIGHT times the squared gap between how bookish it is (1 for a serif, 0 for an interface face) and the target, and each Arabic face costs its book gap, its place's distance from the Latin face's, PARTNER_GAP unless it is the face drawn beside it, and BOOK_WEIGHT times the squared gap between its bookishness and the Latin face's, so a sans Latin face never pairs with a book Arabic face. Without a product type the book gap counts for nothing and every Arabic face is the Latin face's partner. The "Who it is for" section states the target and the faces it gave.

## Why

The product type is what the axes cannot say: the same trustworthy, friendly brief is an app used in short tasks or a journal read at length. A target continuous in type personality and formality keeps the face a nearest choice, never a table: an editorial product with a humanist, formal brief takes a serif, and one with a geometric, playful brief still may not.

## What it touches

fonts.FACES, WEIGHTS, BOOK_WEIGHT, PARTNER_GAP, bookish, book_target, book_cost, arabic_cost, arabic_for, nearest, choose; audience.PRODUCT_TYPES, PRODUCT_ALIASES, product_type_of, BOOK_DEPTH, Audience.book_depth, effects; typography.generate_type.

## Consequences

A brief with a product type may get an Arabic face that is not its Latin face's drawn partner; the size ratio still comes from the two faces' metrics. Adding a face means adding its measured metrics and its place; a serif counts as bookish by its generic family.
