# MUJI — DESIGN.md

## Overview
MUJI (無印良品 — 'no-brand quality goods') is the Japanese lifestyle retailer whose brand strategy is to have no brand. Canvas is pure white or kraft-paper beige (`#f0ebe1`). Type runs a mixed Japanese-Latin grotesk (Yu Gothic / Hiragino Kaku Gothic / Helvetica Neue) at modest 11–13px sizes — never large display. Product photography is shot on shadowless white with the object floating in negative space. Color is reserved for the deep MUJI red (`#8a1538`) used only on the brand mark and on price tags. Everything else is the kraft-and-cotton palette of un-bleached materials. The page reads as a department-store catalog from 1985 — quiet, dense, anti-marketing.

## Color
- **Primary:** `#8a1538` — Deep MUJI red (wordmark + price tags only)
- **Canvas:** `#ffffff` — Pure white
- **Canvas kraft:** `#f0ebe1` — Kraft-paper beige (gift-wrap and stationery bands)
- **Ink:** `#1a1a1a` — Type running color
- **Muted:** `#878787` — Captions, secondary metadata
- **Body:** `#3a3a3a`
- **Hairlines:** `rgba(26,26,26,0.10)` — barely-visible tile borders

## Typography
- **Display:** Yu Gothic / Hiragino / Helvetica Neue, weight 500, 14–16px (the brand's modest hero)
- **Sub-display:** weight 500, 12–14px section heads
- **Body:** Yu Gothic / Helvetica Neue, weight 400, 11–13px running text, 1.5 line-height
- **Caption:** weight 400, 10–11px
- **Mono:** none

## Spacing & rhythm
4-base (4/8/12/16/24/32/48). Section padding 32–48px — far tighter than luxury. Product grids stack 4-up or 5-up at desktop with shadowless product photography. Catalog pages stack 10+ products per scroll-screen.

## Motion signature
Almost-zero motion. Image hover changes opacity only — no scale, no shadow lift. Page transitions use a 200ms cross-fade. Product carousel uses a slow ~600ms ease-in-out between frames. The brand voice is 'the object is the point' — motion would distract.

## Components observed
- `product-floating-white-tile` — shadowless product on pure white, generous negative space
- `kraft-canvas-band` — kraft-paper textured section for stationery
- `price-tag-red` — small red tag with price (the only chromatic moment)
- `dense-product-row` — vertical thumbnail + price + spec
- `category-tab-minimal` — thin underlined category tabs
- `footer-store-locator` — store list in tiny type
- `button-text-link-underlined` — thin underlined text-link
- `magazine-spread-editorial` — long-form magazine essay layout

## Trademark signals
- Product-floating-in-white photography — every product shot on a shadowless pure-white background with the object centered in generous negative space, no styling, no props
- Tiny type at every tier — 11–13px body, 14–16px display — refusing the SaaS-marketing 48px hero convention
- Kraft-paper texture (`#f0ebe1`) as secondary canvas — an actual paper-fiber surface, not a flat fill
- Deep MUJI red (`#8a1538`) reserved for the wordmark and red price tags — never a CTA fill, never a section background
- Dense vertical product lists — the page reads like a 1985 mail-order catalog, not a 2026 e-commerce hero

## What they DON'T do
- No SaaS-marketing display sizes — 48px headlines read as off-brand shouting
- No MUJI red on CTAs or section backgrounds — reserved for wordmark and price tag
- No product-photography styling — shadowless on white, no props, no model
- No shadows on product cards — flat hairline tiles only
- No chromatic accent palette — kraft + white + ink + red price tag
- No emoji, no animation flourishes, no urgency badges

## Exemplar pages
- https://muji.com/
- https://muji.com/jp
- https://muji.us
- https://muji.eu

## When to reference
Reach for MUJI when the user wants Japanese-minimalist retail with anti-marketing voice — no-frills consumer goods, sustainable lifestyle brands, stationery and home essentials, paper goods retailers. The "tiny type + shadowless product photography + kraft secondary canvas + red-only-on-price-tag" combination is the most-copyable MUJI move. Pairs well with brands that want to project quality through restraint rather than maximalism.
