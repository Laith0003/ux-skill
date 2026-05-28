# Modal — DESIGN.md

## Overview
Modal is the serverless-Python-for-AI platform brand — a stark white canvas, a signature warm mustard (#FFB949) as primary accent, a 12-column grid that exposes its own vertical dividers, and a hero that IS a live Python code block running real Modal functions. The brand reads as "look, here is the actual primitive" — anti-marketing, command-line-confident, geometric.

## Color
- **Primary:** `#ffb949` — Modal Mustard (the brand voltage — CTAs, link underlines, highlights)
- **Accent (ember):** `#ff7a30` — Ember Orange (sub-accent on the largest CTAs and pricing emphasis)
- **Canvas:** `#ffffff` — Pure White
- **Surface card:** `#fafafa` — Off-White card backgrounds
- **Surface alt:** `#f2f2ed` — Buttery cream for callout bands
- **Surface dark:** `#0a0a0a` — Near-black for code block backgrounds
- **Ink:** `#000000` — Pure black for headlines and primary text
- **Body:** `#3d3d3d` — Default running text
- **Muted:** `#737373` — Secondary metadata
- **Hairlines:** `#e5e5e0` — 1px borders and the exposed grid dividers
- **Mono comment:** `#737373` on dark; code identifiers in mustard

## Typography
- **Display:** Inter, weight 700, tracking -0.02em, sizes 48–80px hero
- **Sub-display:** Inter weight 600, 28–32px section heads
- **Body:** Inter, weight 400, 16–17px, 1.5 line-height
- **Caption:** Inter weight 500, 13–14px
- **Mono:** IBM Plex Mono, 14px for code blocks, 12px for inline code

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64/96). Section padding 96–128px. The 12-column grid runs from header to footer with visible vertical hairline dividers (this is the brand's most distinctive layout decision — most sites hide their grid; Modal shows it). Code-block-hero consumes ~60% of viewport width on desktop.

## Motion signature
Almost no motion. 150ms ease-out on hover. The signature is the live-running code block on the homepage: real Python characters appear in IBM Plex Mono at ~30 chars/sec, then the result (a tensor, an image, a transcript) renders below. No carousels, no parallax, no scroll-jacking.

## Components observed
- `code-hero-live` — the homepage's live Python code block in IBM Plex Mono
- `exposed-grid-divider` — vertical 1px hairlines running full-height from nav to footer
- `feature-card-bordered` — white card with 1px hairline border, no shadow, no radius
- `pricing-tier-card` — square white card with mustard CTA at bottom
- `gpu-pricing-table` — the dense table showing per-GPU per-second pricing
- `docs-codeblock-card` — dark code block with syntax-highlighted Python
- `footer-grid-light` — multi-column white footer with exposed grid dividers visible

## Trademark signals
- Mustard (#FFB949) as the single primary accent
- Exposed 12-column grid dividers running full-page-height
- Live-running Python code as hero — not a faux mockup
- Square geometry — 0px or 4px corners
- Inter + IBM Plex Mono — refuses serifs

## What they DON'T do
- No saturated orange, no brand yellow — the specific mustard is the brand
- No pill CTAs — square geometry only
- No faux-code marketing mockups — the code is real
- No second accent color
- No gradient hero, no illustration hero
- No emoji
- No animation beyond the live code typewriter

## Exemplar pages
- https://modal.com/
- https://modal.com/pricing
- https://modal.com/use-cases
- https://modal.com/docs

## When to reference
Reach for Modal when the user wants a serverless / GPU / Python-first infrastructure brand — anti-marketing, command-line-confident, comfortable showing the grid. Especially appropriate for compute platforms, inference services, AI infrastructure, and any developer tool where the value prop is "run this code, see this result." The exposed-grid layout and live-code-hero replace the standard SaaS hero pattern.
