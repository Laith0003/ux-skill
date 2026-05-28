# N26 — DESIGN.md

## Overview
N26 is the European mobile-bank brand — Berlin-clean, slightly architectural, with a serif display tier that lifts it out of the all-sans neobank default. The canvas is a strict white-on-white with Tiempos Headline (or similar literary serif) carrying every hero, the floating physical credit card photograph on a soft pastel gradient as the recurring hero device, and a single N26 cyan-mint (#2DCFA5) for CTA voltage. The brand reads as European premium neobank.

## Color
- **Primary:** `#2dcfa5` — N26 Cyan-Mint (the single CTA voltage)
- **Primary deep:** `#20a584` — Mint Hover/Press
- **Canvas:** `#ffffff` — Pure White
- **Surface card:** `#ffffff` — White card with hairline border
- **Surface alt:** `#f5f5f5` — Off-white selected band background
- **Surface card-pastel-mint:** `#a8e6d6` — Pastel mint (behind floating card only)
- **Surface card-pastel-coral:** `#ff8d6e` — Pastel coral (behind floating card only)
- **Surface card-pastel-graphite:** `#3a3d44` — Graphite (behind premium-tier floating card)
- **Ink:** `#191919` — Near-black headlines and primary text
- **Body:** `#4a4a4a` — Default running text
- **Muted:** `#7a7a7a` — Captions, metadata
- **Hairlines:** `#e5e5e5` — 1px borders and dividers
- **Inline-link:** `#2dcfa5`

## Typography
- **Display:** Tiempos Headline, weight 500, tracking -0.02em, sizes 48–80px hero
- **Sub-display:** Inter weight 600, 28–32px section heads
- **Body:** Inter, weight 400, 16–17px, 1.55 line-height
- **Caption:** Inter, weight 500, 13–14px
- **Eyebrow:** Inter, weight 600, 12px, uppercase, +1.5px tracking
- **Card balance:** Inter, weight 600, 24–32px tabular figures (in phone mockup)

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Hero band uses 6/6 split: serif headline + sub + button on left, floating card photograph on pastel gradient on right. Card photographs typically 400–600px wide with subtle drop shadow only on the card itself, never on the gradient background.

## Motion signature
Signature is the floating card mockup with a subtle 4s breathing rotation (~3° yaw, ~2% scale variation). CTAs have a 100ms press-down with a slight darken to deep mint. Phone mockup screenshots fade in at 500ms with an 8px translate on scroll. No carousels, no parallax.

## Components observed
- `floating-card-hero` — physical N26 credit card photograph floating on pastel gradient
- `pastel-gradient-background` — soft mint/coral/graphite gradient (behind cards only)
- `phone-mockup-with-app` — iPhone mockup with N26 app screenshot
- `feature-card-bordered` — white card with hairline border, mint CTA on hover
- `pricing-tier-card` — tier card with floating card photograph + tier name + features
- `trust-badge-row` — row of regulatory/security badges (BaFin, ECB, FDIC equivalent)
- `footer-n26-clean` — light multi-column footer with mint section heads

## Trademark signals
- Floating physical card photograph on pastel gradient as recurring hero
- Tiempos Headline serif at hero scale
- N26 cyan-mint (#2DCFA5) as single CTA voltage
- Pastel gradient backgrounds reserved for card photography areas only
- Phone mockup with serif balance numbers as product proof

## What they DON'T do
- No body backgrounds in pastel colors
- No second voltage accent
- No sans-only display tier — Tiempos serif required at hero
- No flat-on-white card visuals — card always floats on pastel gradient
- No emoji
- No drop shadows on body cards — hairlines only

## Exemplar pages
- https://n26.com/
- https://n26.com/en-eu
- https://n26.com/en-eu/pricing
- https://n26.com/en-eu/premium

## When to reference
Reach for N26 when the user wants a European-premium-neobank brand — Berlin-clean, slightly architectural, with editorial serif voice. Especially appropriate for consumer fintech, digital banks, premium financial products, and any product where the physical artifact (card, device) should be the hero. The "floating-card-on-pastel-gradient + Tiempos-serif-hero + mint-CTA" combo is the brand's most copyable formula; the pastel-gradient discipline (reserved for card area only, never on body) is the most critical anti-slop guardrail.
