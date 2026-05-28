# dbt Labs — DESIGN.md

## Overview
dbt Labs is the analytics-engineering platform brand — a dual-canvas system pairing a soft cream (#fefcf7) marketing surface with a deep navy-violet (#262a38) product surface, a signature dbt-orange (#ff694a) accent, and a recurring isometric pixel-cube glyph assembled from small orange-and-violet pixels. The brand reads as half data-warehouse-serious, half developer-tool-friendly, with a real SQL editor as the brand's most consistent hero device.

## Color
- **Primary:** `#ff694a` — dbt Orange (CTAs, key display words, pixel-cube highlights)
- **Accent (violet):** `#7a5af8` — Pixel Violet (sub-accent on the pixel-cube mark, hover states on dark)
- **Canvas (light):** `#fefcf7` — Cream (marketing surface)
- **Canvas (dark):** `#262a38` — Navy Violet (product surface, pre-footer CTAs, footer)
- **Surface card (light):** `#ffffff` — White card on cream
- **Surface card (dark):** `#1e2230` — Elevated navy-violet for cards
- **Surface code:** `#161928` — Deeper navy for code blocks
- **Ink (on light):** `#0d1226` — Deep navy-ink for headlines
- **Ink (on dark):** `#fefcf7` — Cream text on navy
- **Body (light):** `#3a405a`
- **Body (dark):** `#a8accc`
- **Muted:** `#6b7080`
- **Hairlines:** `rgba(13,18,38,0.10)` light; `rgba(255,255,255,0.08)` dark

## Typography
- **Display:** Söhne, weight 500, tracking -0.02em, sizes 48–80px hero
- **Sub-display:** Söhne weight 500, 28–32px section heads
- **Body:** Söhne, weight 400, 16px, 1.55 line-height
- **Caption:** Söhne weight 500, 13–14px
- **Mono:** Söhne Mono, 14px for SQL editor and code blocks
- **SQL keyword:** Söhne Mono 14px in dbt-orange
- **SQL macro:** Söhne Mono 14px in pixel-violet
- **SQL identifier:** Söhne Mono 14px in cream

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Hero band uses 6/6 split — headline + sub + buttons on left, SQL editor card or pixel-cube illustration on right. Cards use 24–32px internal padding.

## Motion signature
300ms ease-out on hover. Signature is the dbt-pixel-cube mark with a subtle 4s rotation cycle (very slow, ambient). SQL editor hero types in syntax-highlighted SQL at ~30 chars/sec on first paint. Lineage DAG diagrams animate edges drawing in at 600ms per edge on scroll.

## Components observed
- `sql-editor-hero` — real dbt SQL/Jinja code block with syntax highlighting
- `pixel-cube-illustration` — isometric 3D cube assembled from small pixels
- `feature-card-cream` — white card on cream with serif accent
- `feature-card-dark` — navy-violet card with cream text and orange highlights
- `pricing-tier-card` — tier card with orange CTA on the featured tier
- `dag-lineage-diagram-card` — DAG diagram showing dbt model lineage with hairline edges
- `footer-navy-dense` — multi-column navy-violet footer with cream type

## Trademark signals
- dbt-orange (#ff694a) as the warm-coral accent unique to dbt
- Pixel-cube glyph — isometric 3D cube of small pixels
- Dual-canvas: cream marketing + navy-violet product
- SQL editor with syntax highlighting as recurring hero
- Secondary pixel-violet (#7a5af8) on the cube mark only

## What they DON'T do
- No third accent color
- No saturated red or amber substituting for dbt-orange
- No abstract gradient hero — pixel cube or SQL editor only
- No emoji
- No serif anywhere — Söhne + Söhne Mono carry the entire system
- No gradient on the brand orange — solid fill only

## Exemplar pages
- https://getdbt.com/
- https://getdbt.com/product
- https://getdbt.com/pricing
- https://getdbt.com/customers

## When to reference
Reach for dbt Labs when the user wants an analytics-engineering brand — half data-platform-serious, half developer-tool-friendly. Especially appropriate for data tools, analytics platforms, and any product whose primary buyer is an analytics engineer or data engineer. The pixel-cube glyph + SQL-editor-hero combo is the brand's most copyable move; the dual-canvas marketing/product split is the second most distinctive.
