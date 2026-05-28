# Fivetran — DESIGN.md

## Overview
Fivetran is the managed-data-pipeline brand — a clean white canvas, a single deep cobalt (#0073e6) for CTAs, and a connector-logo wall that runs across every product page (200+ source logos: Salesforce, Stripe, NetSuite, Workday, BigQuery, Snowflake). The brand reads as "mature data platform" — enterprise-clean, logo-density forward, slightly serif-tinged with Tiempos Headline for moments of voice.

## Color
- **Primary:** `#0073e6` — Cobalt Blue (CTAs, link underlines, focus rings)
- **Accent (deep):** `#0058b3` — Cobalt Deep (hover / press)
- **Canvas:** `#ffffff` — Pure White
- **Surface card:** `#ffffff` — White card with hairline border
- **Surface alt:** `#f5f8fb` — Light blue-tinted off-white for selected bands
- **Surface dark:** `#0d1219` — Near-black cobalt for footer and pre-footer CTA
- **Ink:** `#0d1219` — Near-black with blue undertone
- **Body:** `#3a4252` — Default running text
- **Muted:** `#6b7280` — Captions, metadata
- **Hairlines:** `#dfe5ec` — 1px borders with subtle blue tint
- **Inline-link:** `#0073e6`

## Typography
- **Display:** Tiempos Headline, weight 500, tracking -0.02em, sizes 48–72px hero
- **Sub-display:** Inter weight 600, 28–32px section heads
- **Body:** Inter, weight 400, 16px, 1.55 line-height
- **Caption:** Inter weight 500, 13–14px
- **Mono:** JetBrains Mono, 14px for connector names in technical contexts

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Connector-logo grid lives in a band consuming 40% of viewport height — 8 columns × 4 rows of small connector tiles. Pipeline diagram bands use a 3-section horizontal flow (source — Fivetran — destination).

## Motion signature
200ms ease-out on hover. The connector logo grid drifts subtly on scroll — a 4-row carousel where each row drifts at 30px/s in alternating directions. CTA buttons have a subtle 100ms press-down. No parallax, no scroll-jacking.

## Components observed
- `connector-logo-grid-hero` — 8×4 grid of small connector logo tiles, the brand's most-recognized hero
- `pipeline-flow-diagram` — horizontal source → Fivetran → destination flow with hairlines
- `feature-card-bordered` — white card with hairline border, 1px cobalt accent on hover
- `destination-card` — card showing destination logo (Snowflake, BigQuery, Databricks) + description
- `pricing-tier-card-enterprise` — tier card with "Contact us" CTA on the highest tier
- `customer-logo-row` — single horizontal row of enterprise customer logos
- `footer-dark-cobalt` — near-black multi-column footer with cobalt accent links

## Trademark signals
- 200+ connector-logo grid as recurring hero device
- Tiempos Headline serif at hero scale — refuses all-sans default
- Cobalt blue (#0073e6) as single CTA voltage — enterprise-trust blue
- Pipeline-flow diagram showing source → Fivetran → destination
- Light blue-tinted off-white (#f5f8fb) for selected bands

## What they DON'T do
- No pages without the connector logo wall on at least one section
- No saturated rainbow colors — the brand is cobalt + white + serif voice
- No hero gradient or hero illustration
- No emoji
- No consumer-bright voltage — the cobalt is enterprise-deep
- No drop shadows on cards — hairlines carry elevation

## Exemplar pages
- https://fivetran.com/
- https://fivetran.com/connectors
- https://fivetran.com/pricing
- https://fivetran.com/customers

## When to reference
Reach for Fivetran when the user wants an enterprise-data-platform brand — connector-logo-wall trust signal, cobalt CTA voltage, slightly editorial via Tiempos serif moments. Especially appropriate for ETL, reverse-ETL, data integration, data warehouse, and any B2B platform whose value prop is "we connect to everything." The 200-logo-grid hero pattern is uniquely Fivetran's and is the brand's most copyable move.
