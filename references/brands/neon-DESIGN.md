# Neon — DESIGN.md

## Overview
Neon is a serverless Postgres platform whose marketing canvas is a near-black graphite (`#0c0d0d`) lit with electric green (`#00e599`). The brand voltage is the green wordmark and the green-on-graphite code mockups; everything else recedes to inter-frame quiet. Type is a tightened modern grotesque (Inter Display / proprietary "Esbuild Mono" pairing) — the brand reads like a developer console that someone took the trouble to design.

## Color
- **Primary:** `#00e599` — Neon Green
- **Canvas:** `#0c0d0d` — Graphite Near-Black
- **Surface card:** `#16191a` — Elevated Graphite
- **Ink (on dark):** `#f5f7f4` — Cream-tinted white
- **Hairlines/dividers:** `rgba(255,255,255,0.08)`
- **Secondary surface (light bands):** `#fafaf7` — Warm white (used on docs/pricing only)
- **Code-string accent:** `#a78bfa` — Soft violet (syntax highlighting)
- **Body muted:** `#8d918e`

## Typography
- **Display:** Inter Display, weight 600, tracking -0.02em, sizes 48-96px on hero
- **Body:** Inter, weight 400-500, 16-18px base, 1.55 line-height
- **Mono:** JetBrains Mono / Esbuild Mono, weight 400, 14px in code blocks

## Spacing & rhythm
8-base scale (8/16/24/32/48/64/96). Section padding 96px desktop, 64px mobile. Card padding 24-32px. Generous vertical breathing between code mockups.

## Motion signature
Sub-300ms ease-out fades on hover and section enter; signature is the green branch-arrow that animates from the wordmark when a CTA is engaged. No bounce, no parallax.

## Components observed
- `code-block-graphite` (dark mock with violet/green syntax)
- `branch-diagram` (database branching visual — green arrows on graphite)
- `pricing-table-three-tier-dark`
- `nav-pill-bar` (translucent on graphite)
- `cta-button-green-fill`
- `terminal-output-card`

## Trademark signals
- Green-on-graphite is the entire brand voltage — no second accent on marketing surfaces
- Branch-diagram visuals (Postgres branching) used as actual product chrome, never as illustration
- Mono in body callouts mid-paragraph — code lives at sentence level, not just in blocks
- Pricing rows render hover-glow with a 1px green underline, never a full row fill
- Logo wordmark uses lowercase `neon` with a single green dot accent

## What they DON'T do
- No purple/blue gradients (the dominant fintech-dev cliche)
- No 3D illustrations or rendered geometry
- No drop shadows on cards — depth is surface tone, not shadow
- No light-mode hero on the homepage
- No emoji in product chrome or marketing

## Exemplar pages
- https://neon.com/
- https://neon.com/docs/introduction
- https://neon.com/pricing
- https://neon.com/branching

## When to reference
Reach for Neon when the user needs a serverless / developer-infrastructure surface that wants to feel both performant and considered. Especially appropriate for any product whose differentiator is database/branching/storage — Neon shows how to render that as the hero artifact rather than describe it as marketing copy.
