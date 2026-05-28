# Aesop — DESIGN.md

## Overview
Aesop's surface is the deepest apothecary in beauty — a sepia canvas (`#dccfb6`) with chocolate-ink type (`#241f17`) and a Walbaum-feel serif display. Every page reads like a 19th-century botanical pharmacopeia translated to the screen. Photography is sparse, restrained, often product-only on warm gradient floors. The brand's UI vocabulary intentionally feels handset rather than designed-in-Figma.

## Color
- **Primary:** `#241f17` — Chocolate Ink (used for type and CTAs)
- **Canvas:** `#dccfb6` — Sepia Cream
- **Surface alt:** `#c8b598` — Sepia Deep
- **Surface card (rare):** `#f0e6d2` — Pale Tan
- **Accent (botanical):** `#5a4a2e` — Dried Herb (used in apothecary illustrations)
- **Ink:** `#241f17`
- **Body:** `#3d342a`
- **Hairlines:** `rgba(36,31,23,0.20)` — visible 1px hairlines, never subtle

## Typography
- **Display:** Walbaum / Suisse Works (transitional serif), weight 400, tracking 0, sizes 36-56px hero — small for an industry that loves giant type
- **Body:** Walbaum / Suisse Works, weight 400, 15-16px base, 1.6 line-height
- **Eyebrow:** Same serif at 11px small-caps with 1.2px tracking

## Spacing & rhythm
8-base (8/16/24/32/48/72). Section padding 96-120px. Long-form essays use single 640px reading column. Product grids 3-up max, with generous 40-60px gutters.

## Motion signature
None on hover. The brand voice is "stillness" — animation is anti-aesthetic. Add-to-cart triggers a quiet slide-down acknowledgment, no toast, no modal, no celebration.

## Components observed
- `apothecary-product-card` (single product photo on sepia, serif name, mL volume, price)
- `essay-band-single-column` (640px reading column, serif body, drop-cap optional)
- `ingredient-list-band` (Latin botanical names in italic, alphabetized)
- `category-nav-text-only` (text links in serif, no icons, no chips)
- `cta-link-underlined` (no buttons — text links with hairline underline)
- `instructional-band` (numbered serif steps, hairline-divided)

## Trademark signals
- Sepia canvas — the entire industry runs white; Aesop refuses
- Walbaum serif EVERYWHERE — display, body, navigation, captions, buttons (when buttons exist)
- Text-link CTAs instead of button-fill — the absence of buttons is the brand
- Latin botanical names italicized in ingredient lists — scientific cadence
- Numbered instructional steps with serif numerals, not symbols

## What they DON'T do
- No emoji anywhere — the brand voice is 19th-century
- No filled-button CTAs except in checkout — the rest is hairline-underlined text
- No saturated colors — sepia is the entire palette
- No animation beyond quiet 200ms link fades
- No promotional banners, no sale messaging, no scarcity chrome ever

## Exemplar pages
- https://www.aesop.com/us/
- https://www.aesop.com/us/r/online-magazine/
- https://www.aesop.com/us/c/skin/
- https://www.aesop.com/us/p/products/

## When to reference
Reach for Aesop when the user wants the most editorial, restrained, apothecary-feeling surface in the catalog. The sepia + serif-everywhere + text-link-CTA atmosphere is appropriate for the most considered beauty/wellness/heritage brands — and as a forcing function when the user's brand is trying too hard ("can we be more Aesop" = less ornament, more confidence).
