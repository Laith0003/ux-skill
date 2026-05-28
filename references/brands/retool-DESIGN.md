# Retool — DESIGN.md

## Overview
Retool is the internal-tool builder brand — but it reads as a literary technology magazine, not a developer tool. The canvas is a warm cream (#fbf6ea), display headlines run GT Sectra serif at magazine-cover scale (72–96px weight 500), and the voltage is a single signal-orange (#ff5d00) reserved for CTAs and selected underlines. Every solutions page leads with a real Retool-built dashboard screenshot, paired with a logo wall of operator brands. The brand reads as "serious software for serious operators."

## Color
- **Primary:** `#ff5d00` — Signal Orange (CTAs, link underlines, selected display word accents)
- **Accent (amber):** `#ff9533` — Soft Amber (sub-accent on the largest moments, never on chrome)
- **Canvas:** `#fbf6ea` — Retool Cream (the brand's editorial chrome)
- **Surface card:** `#ffffff` — White card on cream
- **Surface alt:** `#f3ecd9` — Selected band background
- **Surface dark:** `#171413` — Near-black for code blocks and pre-footer CTAs
- **Ink:** `#171413` — Warm dark for headlines and primary text
- **Body:** `#3f3a36` — Default running text
- **Muted:** `#736b66` — Captions, metadata
- **Hairlines:** `rgba(23,20,19,0.10)` — 1px borders on cream
- **Inline-link:** `#ff5d00` (with thin underline)

## Typography
- **Display:** GT Sectra, weight 500, tracking -0.02em, sizes 56–96px hero
- **Sub-display:** GT Sectra weight 500, 28–40px section heads
- **Body:** Inter, weight 400, 17px essay body, 1.55 line-height
- **Caption:** Inter weight 500, 13–14px
- **Eyebrow:** Inter 12px / 500 / uppercase / +1.5px tracking
- **Mono:** GT Pressura Mono, 14px for code blocks and inline code

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Hero band consumes upper third with display headline on left, dashboard mockup card on right (5/7 split at desktop). Logo wall band immediately below hero with 6–8 customer logos in a single horizontal row.

## Motion signature
200ms ease-out on hover. Signature is the dashboard-mockup scroll-reveal — built-internal-tool screenshots fade in at 500ms with a 12px upward translate. Orange CTAs have a subtle 80ms press-down (1px translateY, slight darken to #e54f00). No carousels, no parallax.

## Components observed
- `hero-dashboard-mockup` — real Retool-built admin panel / ops dashboard screenshot
- `feature-card-cream` — white card on cream with serif title + sans body
- `logo-wall-cream` — single row of operator-brand customer logos
- `customer-story-card` — pull-quote + logo + named operator role
- `pricing-tier-card` — white tier card with serif price and orange CTA
- `code-extension-card` — dark code-block card showing Retool extension code
- `footer-cream-dense` — multi-column cream footer with serif column heads

## Trademark signals
- GT Sectra serif at magazine-cover scale headlines
- Warm cream canvas (#fbf6ea) — editorial chrome for a developer product
- Signal orange (#ff5d00) reserved for CTAs and selected display underlines
- Dashboard mockup screenshots as hero — real product chrome
- Logo wall of operator brands directly below hero — operator-name credibility

## What they DON'T do
- No sans-only display tier — GT Sectra carries every display headline
- No pure white canvas — the cream is non-negotiable
- No saturated orange backgrounds — the orange is scarce
- No abstract illustration hero — real dashboard screenshots only
- No "10x productivity" hyperbole — the voice is operator-serious
- No emoji

## Exemplar pages
- https://retool.com/
- https://retool.com/solutions
- https://retool.com/customers
- https://retool.com/pricing

## When to reference
Reach for Retool when the user wants a developer-tool brand that feels editorial and operator-serious — magazine-cover headlines, real product screenshots, operator-name credibility. Especially appropriate for B2B tools targeting Heads of Operations, Heads of Engineering, or any technical buyer who reads The Economist. The GT-Sectra-on-cream pattern is replicable for any developer brand that wants to feel premium without leaning enterprise.
