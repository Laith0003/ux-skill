# Herman Miller — DESIGN.md

## Overview
Herman Miller is the American modernist furniture house responsible for the Eames Lounge, the Aeron chair, and a century of design-museum-permanent-collection objects. Canvas is warm gallery-white (`#faf9f6`) or a deep editorial near-black for hero immersion. Type runs a thoughtful serif (Söhne / proprietary modernist serif) at editorial scale paired with a precise grotesk for body. Photography is fine-art product-as-sculpture — single chair in a vast gallery space, side-light, no styling props. The voice is museum-curator: object name, year, designer, materials — written as exhibition wall labels, not e-commerce descriptions.

## Color
- **Primary / Ink:** `#000000` — Pure black (gallery-museum ink)
- **Canvas:** `#faf9f6` — Warm gallery-white
- **Ink:** `#1a1a1a` — Type running color
- **Accent:** `#a0532a` — Warm rust (for upholstery accent shots, hairline emphasis)
- **Body:** `#3a3a3a`
- **Muted:** `#7a7a7a` — Captions, designer-credit metadata
- **Hairlines:** `rgba(0,0,0,0.10)`

## Typography
- **Display:** Söhne / proprietary modernist serif, weight 400, 48–72px hero
- **Sub-display:** Söhne weight 500, 24–32px section heads
- **Body:** Söhne, weight 400, 16–17px essay body, 1.65 line-height
- **Caption (exhibition label):** Söhne Mono, 12–13px — designer + year + materials
- **Mono:** Söhne Mono, 13–14px for spec tables and exhibition labels

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128/160). Section padding 128–160px — the negative space IS the editorial. Product page hero typically shows the Aeron chair at 30% of the viewport with 70% empty floor. Product grid is 1-up or 2-up; 4-up reads as e-commerce.

## Motion signature
Gallery-pacing. Hero images cross-fade slowly (~2s) — never quick. Product detail pages reveal product specs (designer, year, materials) with a slow 600ms cascade. Hover on product tiles fades a thin hairline border in over 300ms — no scale, no shadow lift. The brand voice is museum, not e-commerce.

## Components observed
- `single-product-gallery-hero` — single chair on white floor in vast space
- `exhibition-label-caption` — designer + year + materials in mono
- `designer-credit-block` — bio block for chair designer
- `essay-long-form-text` — editorial essay on chair history
- `materials-science-spec-table` — engineering spec table
- `color-variant-swatch-row` — upholstery color picker
- `button-text-link-thin` — thin underlined text-link
- `footer-museum-style-monochrome` — gallery-style footer

## Trademark signals
- Gallery-white canvas with single product staged in vast negative space — Aeron chair at 30% viewport, 70% empty floor — the absence IS the editorial
- Exhibition-label captions — 'Aeron Chair, 1994, by Bill Stumpf and Don Chadwick' in monospaced type beneath the photograph — museum, not catalog
- Designer-credit type — every product page leads with the designer's name and the year of design, treating each chair as a historical artifact
- Editorial long-form essays about chair manufacturing, materials science, and ergonomic research — written as cultural-magazine features
- Single-image hero with low-saturation studio lighting — never multi-product collages, never lifestyle staging with people

## What they DON'T do
- No lifestyle staging — adding a person, coffee mug, rug breaks the gallery voice
- No dropping designer credit — the product IS the designer's signature
- No 4-up tile grids — 1-up or 2-up only
- No saturated colors — monochrome-on-gallery-white with rare warm-rust accent
- No marketing-bullet copy — descriptions are full editorial paragraphs
- No emoji, no urgency badges, no promotional pricing visible on hero

## Exemplar pages
- https://hermanmiller.com/
- https://hermanmiller.com/products
- https://hermanmiller.com/stories
- https://hermanmiller.com/designers

## When to reference
Reach for Herman Miller when the user wants museum-grade product-as-sculpture editorial — premium design objects, gallery-style e-commerce, architecture and design publications, art-book retailers. The "gallery-white canvas + single product in vast negative space + exhibition-label mono caption + editorial designer-credit prose" combination is the most-copyable Herman Miller move. Pairs well with any brand that wants to position product as artifact rather than commodity.
