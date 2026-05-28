# Cloudflare — DESIGN.md

## Overview
Cloudflare is the global-network infrastructure brand that operationalizes a single chromatic asset: orange. The orange (`#f48120`) is reserved with monastic discipline for the brand mark and primary CTAs. Canvas is white-to-near-white with cool blue-gray ink. Type runs a precise grotesk (Cloudflare Sans / Inter / IBM Plex) and the brand projects 'global, infrastructural, calm' — never SaaS-marketing kinetic. The mark — a stylized orange cloud — appears on the navigation; the rest of the page reads as quiet, dense, technical documentation.

## Color
- **Primary:** `#f48120` — Cloudflare orange (the single chromatic asset)
- **Canvas:** `#ffffff` — Pure white
- **Ink:** `#0d1620` — Cool blue-tinted near-black for type
- **Accent:** `#003682` — Cool blue, used on emphasized inline links and chart series
- **Body:** `#3a4451`
- **Muted:** `#6f7682`
- **Hairlines:** `#e6ebf0`
- **Code-block background:** `#1d2530` — Dark slate for code snippets

## Typography
- **Display:** Cloudflare Sans (or Inter substitute), weight 700, 40–64px hero
- **Sub-display:** weight 600, 24–32px section heads
- **Body:** Inter, weight 400, 16–17px, 1.6 line-height
- **Caption:** weight 500, 13–14px, uppercase tracking +1.5px for category eyebrows
- **Mono:** IBM Plex Mono, 14px for code excerpts and CLI commands

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px — generous breathing room projects 'infrastructure scale'. Body content max-width ~720px on essay pages; technical docs widen to ~960px to accommodate tables and code.

## Motion signature
Almost-no-motion. Section reveals fade in over 400ms with no translate. Global-network animations (the signature globe with arc-paths) move at slow 12s loop — calm, infrastructural, never twitchy. Hover states change opacity, never scale.

## Components observed
- `globe-network-hero` — globe with arc-paths between data centers
- `stat-counter-tile` — large numeric metric with grotesk display
- `product-feature-card` — flat card with icon + title + body + text-link
- `code-snippet-block` — dark slate well with IBM Plex Mono
- `button-primary-orange` — orange-fill CTA, 6–8px radius
- `button-secondary-outline` — ink-outline secondary
- `comparison-table-dense` — feature-by-tier table with hairlines
- `footer-multi-column-monochrome` — dark grey footer with 5+ link columns

## Trademark signals
- Single-asset orange (`#f48120`) — only on brand mark, primary CTAs, and rare inline highlight; never as a section background, never as a gradient stop
- Map-of-the-world hero — global network map with arc-paths between data centers, often as a watermark or full-bleed
- Dense technical content blocks with semantic hierarchy — sub-headers, mono code excerpts, tabular data — the brand reads as documentation more than marketing
- Cool blue secondary (`#003682`) for inline links and chart series — never replaces orange as primary CTA fill
- Generous white-space rhythm — the brand projects 'infrastructure scale' through breathing room, not visual density

## What they DON'T do
- No second saturated color — orange is the single chromatic asset; emphasis comes from weight and spacing
- No dark canvas on marketing — only the developer docs pivot to a dark code-block treatment
- No fast-spinning network animations — the slow 12s loop IS the 'we are infrastructure' voice
- No thin display weights — display tiers stay at 600+
- No stock vector blob illustrations — the brand favors the network globe, real data viz, and clean data-center photography

## Exemplar pages
- https://cloudflare.com/
- https://cloudflare.com/network
- https://blog.cloudflare.com/
- https://developers.cloudflare.com/

## When to reference
Reach for Cloudflare when the user wants infrastructural calm — global platforms, CDN/edge/network products, security infrastructure, developer-facing documentation portals. The "single-orange-asset + slow network globe + dense semantic typography" combination is the most-copyable Cloudflare move. Pairs well with B2B infrastructure brands that want to project scale and trust without resorting to gradient maximalism.
