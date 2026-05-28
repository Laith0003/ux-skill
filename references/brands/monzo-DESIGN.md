# Monzo — DESIGN.md

## Overview
Monzo is hot coral on white — the brand's signature card color (`#ff4f40`) is one of the most-recognized hues in consumer fintech. The marketing surface pairs the coral with a friendly geometric sans (FK Display / ABC Diatype) and a deliberately illustrated UI style (rounded characters, simplified objects). It feels closer to a children's book illustration system than a traditional bank.

## Color
- **Primary:** `#ff4f40` — Hot Coral (the card)
- **Primary deep:** `#e3382a`
- **Canvas:** `#ffffff` — White
- **Surface alt:** `#fff5f1` — Coral Wash
- **Ink:** `#091723` — Deep Navy
- **Body:** `#4d5560`
- **Hairlines:** `rgba(9,23,35,0.10)`
- **Accent palette:** `#ffd166` (sunshine yellow), `#06aed5` (cyan), `#2d6a4f` (forest green) — used in illustration only
- **Semantic success:** `#2d6a4f`
- **Semantic warning:** `#ffd166`

## Typography
- **Display:** FK Display / ABC Diatype Variable, weight 500-700, tracking -0.02em, sizes 56-96px hero
- **Body:** ABC Diatype, weight 400-500, 16-17px base, 1.55 line-height
- **Mono (numbers / account):** Söhne Mono, 14-16px for figures

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/72). Section padding 72-96px. Hero band uses 6/6 grid with type left, large hot-coral card render right. Card padding 24-32px.

## Motion signature
220ms ease-out on hover; signature is the gentle tilt-and-shadow of the coral card mockup on scroll-reveal (slight 3D rotation, never aggressive). Coin/icon illustrations have subtle bounce on hover.

## Components observed
- `hero-band-coral-card-render` (large hot-coral card render as the hero artifact)
- `feature-illustration-card` (rounded character illustration, friendly object)
- `product-comparison-three-tier`
- `pill-cta-coral-fill` (full radius pill, coral fill)
- `industry-first-badge` (small coral circle marker)
- `app-screenshot-card-rounded` (real app UI in a rounded device frame)

## Trademark signals
- Hot coral card render — the card IS the brand, rendered photorealistically in nearly every hero
- Pill-shape CTAs at full radius — never square, never less than full pill
- Illustrated objects with simplified geometry — coins, plants, characters, all hand-drawn-feeling
- Industry-first coral circle badges — small, restrained, distinctive
- Cyan/yellow/green accents used in illustration, never as buttons

## What they DON'T do
- No dark-mode hero on marketing site
- No emoji — illustrated objects fill that role with brand consistency
- No square buttons
- No 3D rendered hyper-realistic finance geometry — illustration style is deliberately flat-friendly
- No coral type on white — coral is reserved for surfaces and the card

## Exemplar pages
- https://monzo.com/
- https://monzo.com/features/
- https://monzo.com/business/
- https://monzo.com/help/

## When to reference
Reach for Monzo when the user wants a consumer-fintech brand surface with maximum personality and approachability. The hot-coral + illustrated-objects + pill-CTA combination is appropriate for any consumer financial product targeting a younger or design-aware audience — neobanks, budgeting apps, paying-friends apps. Especially useful when the user wants warmth without losing trust.
