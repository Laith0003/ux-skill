# Datadog — DESIGN.md

## Overview
Datadog's marketing surface is built around the brand's signature deep purple (`#632ca6`) and the dog-mascot illustration system. The canvas is white, the purple is generous on hero bands and CTAs, and an editorial geometric serif (Tiempos / Domaine) carries display headlines — the type choice is what makes the brand feel like an institution, not a startup. Body sits in a humanist sans (Söhne / Inter).

## Color
- **Primary:** `#632ca6` — Datadog Purple
- **Primary dark:** `#4a1d82` — Active Purple
- **Canvas:** `#ffffff` — White
- **Surface alt:** `#f7f5fc` — Lavender Wash
- **Ink:** `#1c1d26` — Indigo Near-Black
- **Body:** `#4d4f60`
- **Hairlines/dividers:** `rgba(28,29,38,0.10)`
- **Accent secondary:** `#ff7300` — Bark Orange (used on dog-mascot, status indicators, "live" badges)

## Typography
- **Display:** Tiempos Headline / Domaine Display, weight 400 (regular), tracking -0.01em, sizes 56-96px on hero
- **Body:** Söhne / Inter, weight 400-500, 16-18px base, 1.55 line-height
- **Mono:** Söhne Mono / IBM Plex Mono, 14px

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96px desktop. Hero band carries 120-160px vertical breathing. Card padding generous at 32-40px.

## Motion signature
180ms ease-out on hover; signature is the dog-mascot blink/wag micro-animation in hero illustrations. Dashboard mockups have a slow scroll-reveal with chart-line draw-on.

## Components observed
- `hero-band-with-mascot` (purple gradient with bark-orange dog character)
- `dashboard-screenshot-card` (real product chrome as marketing hero)
- `pricing-table-five-tier` (Pro / Enterprise / etc., five tiers wide)
- `category-tab-purple-active`
- `cta-band-purple-fill`
- `customer-logo-strip-mono`

## Trademark signals
- Bark, the dog mascot — appears in nearly every hero band, the only place in dev-observability where a literal mascot survives
- Purple-on-white with a single bark-orange accent — never any other secondary
- Serif display headlines in an industry of geometric sans — the editorial weight is the brand differentiator
- Five-tier pricing tables (rare; most products show 3) signaling enterprise depth
- Dashboard mockups carry actual product chrome, never abstract data viz

## What they DON'T do
- No dark-mode hero on the marketing site
- No emoji or playful UI illustrations beyond the Bark mascot
- No geometric-sans display headlines — the serif is the brand voice
- No saturated rainbow data viz in marketing screenshots — Datadog dashboards skew muted
- No second mascot or sibling characters — Bark stands alone

## Exemplar pages
- https://www.datadoghq.com/
- https://www.datadoghq.com/pricing/
- https://www.datadoghq.com/dash/
- https://www.datadoghq.com/product/

## When to reference
Reach for Datadog when the user wants enterprise-credibility-with-personality. The serif-display-over-purple combination is unusual in observability/devtools and works for products that want to read as institutional but warm. Especially relevant when the brand needs a strong mascot system and dense dashboard mockups as the marketing hero.
