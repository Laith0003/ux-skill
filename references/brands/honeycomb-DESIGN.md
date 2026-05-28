# Honeycomb — DESIGN.md

## Overview
Honeycomb (observability for distributed systems) leans into the literal honey-and-bee metaphor with a saturated honey-amber (`#ffc53d`) over a deep midnight teal (`#0d2330`). The brand voice is technical-but-warm — type pairs a geometric sans display with a humanist body, and the hexagon motif appears as both a literal logo and as a section-divider shape. It feels closer to a smart magazine than a typical observability tool.

## Color
- **Primary:** `#ffc53d` — Honey Amber
- **Primary deep:** `#e0a920` — Amber Pressed
- **Canvas:** `#0d2330` — Midnight Teal
- **Surface card:** `#163140` — Teal Card
- **Canvas alt (light bands):** `#fff8e8` — Honey Cream
- **Ink (on dark):** `#fbf6e9` — Cream Ink
- **Ink (on light):** `#0d2330`
- **Hairlines:** `rgba(255,255,255,0.10)` on dark, `rgba(13,35,48,0.08)` on light

## Typography
- **Display:** Söhne Breit / Geomanist, weight 600, tracking -0.01em, sizes 56-88px
- **Body:** Söhne / Inter, weight 400-500, 16-17px base, 1.55 line-height
- **Mono:** Söhne Mono / Berkeley Mono, weight 400, 14px

## Spacing & rhythm
8-base (8/16/24/32/48/64/96). Section padding 96-112px. Hex-shape decorative dividers between major bands. Card padding 24-32px.

## Motion signature
220ms ease-out on hover; signature is the honey-amber CTA hover-glow (soft outer ring at 30% alpha). Hex-section dividers slide in with a 600ms stagger on scroll.

## Components observed
- `hero-band-midnight-teal` (dark canvas with amber CTAs)
- `hex-divider` (literal hexagon shape as section separator)
- `code-block-dark` (teal-card surface, amber syntax highlights)
- `bubbleup-callout-card` (signature root-cause visual)
- `pricing-tier-three-column-dark`
- `customer-quote-card-honey`

## Trademark signals
- Honey-amber on midnight-teal — the dominant "wasp colors" pairing
- Literal hexagon shape used as section dividers and icon containers
- BubbleUp / Canvas product-feature visuals get full-bleed treatment
- Customer quotes set in larger type than body copy — testimonials get editorial weight
- Mono inline in body callouts for span names, attributes, query syntax

## What they DON'T do
- No purple/violet (the dominant dev-observability cliche)
- No mascot characters or illustrated creatures (the brand is the hexagon)
- No light-mode hero — the midnight teal is the entry point
- No flat-color rainbow data viz
- No emoji in product UI or marketing chrome

## Exemplar pages
- https://www.honeycomb.io/
- https://www.honeycomb.io/pricing
- https://www.honeycomb.io/blog
- https://www.honeycomb.io/product

## When to reference
Reach for Honeycomb when the user wants a developer-tools surface with both technical depth AND warm personality. The honey/hex metaphor is unusual in dev infra and gives the brand a strong identity without resorting to mascots. Especially appropriate for products that want to read as "for engineers who care about craft" rather than "for engineers who want speed."
