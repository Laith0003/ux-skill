# Dezeen — DESIGN.md

## Overview
Dezeen is the world's most-read architecture-and-design magazine brand — confident, image-forward, anti-chrome. The canvas is a strict monochrome white-and-near-black duet, Dezeen Display serif carries every headline, and a 4-column masonry grid of beautifully-shot architecture photography carries ~80% of the visual surface area on every page. The brand reads as the design publication of record.

## Color
- **Primary:** `#000000` — Pure Black (every CTA, footer fill, brand mark)
- **Canvas:** `#ffffff` — Pure White
- **Surface card:** `#ffffff` — White card with hairline border
- **Surface alt:** `#f5f5f5` — Selected gray-tint band background (rare)
- **Ink:** `#1a1a1a` — Near-pure-black for headlines and primary text
- **Body:** `#3a3a3a` — Default running text
- **Muted:** `#7a7a7a` — Captions, photographer credits, dates
- **Hairlines:** `#e0e0e0` — 1px dividers between articles
- **Inline-link:** `#000000` (with thin underline)

## Typography
- **Display:** Dezeen Display (custom serif), weight 500, tracking -0.01em, sizes 24–48px headlines
- **Sub-display:** Dezeen Display, weight 500, 18–22px sub-heads
- **Body:** Helvetica Neue, weight 400, 15–16px, 1.55 line-height
- **Caption:** Helvetica Neue, weight 500, 12–13px (used for photographer credits and "Image courtesy of…")
- **Byline:** Helvetica Neue, weight 700, 11px, uppercase, +1px tracking
- **Category tag:** Helvetica Neue, weight 700, 11px, uppercase, +1px tracking

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64). Section padding 48–64px. Masonry grid: 4 columns at desktop, 16px gap. Image-tile aspect ratios vary (mostly 4:3 and 3:4) within the masonry. Article body column ~720px.

## Motion signature
Almost no motion. 150ms ease-out on hover. Signature is the 4-column masonry grid loading images on scroll with 200ms fade-in stagger. Image hover micro-zoom: images scale to 110% within a fixed crop frame over 300ms — the only motion device the brand uses.

## Components observed
- `masonry-grid-4col` — 4-column staggered grid of image tiles
- `story-card-with-image` — image tile with hover-zoom + serif title + byline below
- `image-hover-zoom-frame` — fixed-crop frame with image scaling to 110% on hover
- `category-tag-pill` — small uppercase category tag ("Architecture", "Design", "Interiors")
- `article-byline-row` — small uppercase byline row with author + date + photographer credit
- `designer-portrait-card` — featured designer card with portrait + name + studio
- `footer-dezeen-minimal` — black multi-column footer with white type

## Trademark signals
- Photograph-as-page — 4-column masonry grid carrying ~80% of visual area
- Dezeen Display custom serif at every headline tier
- Strict black-on-white monochrome — no chromatic accent
- Image hover micro-zoom within fixed crop frame
- Square/rectangular image tiles — no rounded corners

## What they DON'T do
- No chromatic brand accent
- No sans-only headline tier — Dezeen Display serif required
- No rounded image corners
- No drop shadows on tiles
- No decorative chrome — photography supplies all visual weight
- No emoji
- No animation beyond hover-zoom and fade-in stagger

## Exemplar pages
- https://dezeen.com/
- https://dezeen.com/architecture
- https://dezeen.com/design
- https://dezeen.com/interiors

## When to reference
Reach for Dezeen when the user wants an image-first design-publication brand — confident, anti-chrome, photograph-as-page. Especially appropriate for design magazines, architecture publications, portfolio sites, and any image-heavy editorial brand where photography should carry all visual weight. The 4-column masonry + image-hover-zoom + monochrome-chrome combo is the brand's most copyable formula; downstream consumers should resist adding any chromatic accent — the brand's discipline IS the design.
