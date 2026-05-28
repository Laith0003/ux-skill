# Render — DESIGN.md

## Overview
Render's marketing surface pairs a deep aubergine purple (`#5a2d8c`) with a warm cream (`#fdf4e7`) — a fintech-meets-developer-platform aesthetic that reads more like a magazine spread than a cloud console. The split-canvas rhythm (cream hero, purple feature bands, cream pricing) is the brand's pacing mechanism. Type is a humanist sans with a slight editorial weight.

## Color
- **Primary:** `#5a2d8c` — Deep Aubergine
- **Primary active:** `#46226d` — Aubergine Pressed
- **Canvas:** `#fdf4e7` — Warm Cream
- **Surface card:** `#ffffff` — White Card
- **Ink:** `#231f29` — Plum Near-Black
- **Body:** `#4a3f55` — Plum Muted
- **Hairlines/dividers:** `rgba(35,31,41,0.10)`
- **Accent (signals only):** `#ff6b35` — Burnt Orange (status / "live" indicators)

## Typography
- **Display:** Söhne / Inter Display, weight 500, tracking -0.015em, sizes 56-88px hero
- **Body:** Inter, weight 400-500, 16-17px base, 1.6 line-height
- **Mono:** IBM Plex Mono / Berkeley Mono, weight 400, 14px in code blocks

## Spacing & rhythm
4-base scale (4/8/16/24/32/48/64/96). Section padding 96-128px between bands. Card internal padding 32-40px. Hero band is generous — often 160px vertical breathing.

## Motion signature
200ms ease-in-out on hover; signature is the purple-to-aubergine darken on primary CTAs and a slow horizontal scroll-reveal on long feature scrollytells. No spring physics.

## Components observed
- `hero-band-cream` (cream canvas, large serif-feeling sans display)
- `feature-band-aubergine` (deep purple card with cream type)
- `pricing-table-three-tier` (cream rows with aubergine CTA cell)
- `code-snippet-card-dark` (inline aubergine-tinted dark code block)
- `service-card-grid` (3-up cream cards with hairline borders)
- `terminal-stream-block`

## Trademark signals
- Cream-and-aubergine pairing — instantly distinguishes Render from every blue/cyan cloud competitor
- Wordmark "Render" set in weight 500 italic — the italic detail is the personality
- Logos arranged in a horizontal "Trusted by" strip on cream, never on dark
- One-tier-highlighted pricing — the middle tier always sits on aubergine ground
- Bottom-of-hero gradient fade from cream to deeper cream (never to purple)

## What they DON'T do
- No cobalt/cyan accents — purple is the only brand voltage
- No 3D cloud illustrations or floating geometry
- No dark mode on the marketing site
- No emoji in product copy or chrome
- No bold-weight display headlines — weight 500 max

## Exemplar pages
- https://render.com/
- https://render.com/pricing
- https://render.com/docs
- https://render.com/blog

## When to reference
Reach for Render when the user wants a cloud / dev-infrastructure surface that intentionally rejects the "AWS-clone blue and white" default. The cream-and-purple atmosphere reads warmer and more editorial than typical cloud marketing — appropriate for products positioning themselves as the "thoughtful alternative" to the hyperscalers.
