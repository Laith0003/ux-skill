# Perplexity — DESIGN.md

## Overview
Perplexity is the answer-engine brand — built on a near-black graphite canvas (with a 2026 cream marketing surface), a signature peacock-teal (#20B8CD) as the single accent, the FK Grotesk Neue family at every tier, and a search input that IS the hero. The brand reads as a technical answer engine, not a chat product: dense, sourced, slightly serious, with the source-cite ribbon as a recurring visual signature.

## Color
- **Primary:** `#20b8cd` — Peacock Teal (the single brand accent, used for CTAs, links, focus rings)
- **Canvas (app):** `#0f1416` — Graphite Near-Black (the app surface)
- **Canvas (marketing):** `#fbfaf4` — Cream (2026 marketing-only surface)
- **Surface card (dark):** `#1a1f22` — Elevated graphite for answer cards
- **Surface card (light):** `#ffffff` — White card on cream marketing surface
- **Surface alt:** `#091114` — Deeper graphite for footer and modals
- **Ink (on dark):** `#f7f7f5` — Off-white text on graphite
- **Ink (on light):** `#0f1416` — Near-black on cream
- **Body (on dark):** `#b8bdc1` — Secondary text on graphite
- **Body (on light):** `#52555c`
- **Muted:** `#737880` — Captions, source-cite metadata
- **Hairlines:** `rgba(255,255,255,0.08)` on dark; `rgba(15,20,22,0.10)` on light

## Typography
- **Display:** FK Grotesk Neue, weight 500, tracking -0.02em, sizes 48–80px hero
- **Sub-display:** FK Grotesk Neue weight 500, 28–32px section heads
- **Body:** FK Grotesk Neue, weight 400, 16–17px, 1.55 line-height
- **Search placeholder:** FK Grotesk Neue, weight 400, 18px
- **Source-cite caption:** FK Grotesk Neue, weight 500, 12px, +0.5px tracking
- **Mono:** JetBrains Mono, 14px for code answers

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64/96). Section padding 96px. Search-pill is the hero element — typically 720px wide × 64px tall, centered, with the teal CTA on the right edge. Answer cards use 24–32px internal padding with a 12px gap between the answer body and the source-cite ribbon.

## Motion signature
200ms ease-out on hover for all interactive elements. Signature is the typewriter-rate answer reveal — ~25ms per token streaming into the answer card. Source-cite ribbons fade in at 300ms with a 50ms stagger between favicons. Follow-up question pills slide up 8px and fade in over 250ms after answer completion.

## Components observed
- `search-pill-hero` — the centerpiece input on every primary surface
- `answer-card-with-cites` — answer body + source-cite ribbon stacked
- `source-favicon-row` — row of small favicon thumbnails (16px) of cited domains
- `follow-up-pill` — small pill buttons under answers ("Ask a follow-up…")
- `discover-feed-card` — Discover-page card with thumbnail + question + source ribbon
- `spaces-card` — Spaces feature card with collection metadata
- `pro-upgrade-card-teal` — the rare full-teal-fill card promoting Pro
- `footer-graphite` — multi-column deep-graphite footer

## Trademark signals
- Peacock teal #20B8CD as the single accent — never blue, never aqua
- FK Grotesk Neue at every tier — refuses Inter substitution
- Search field IS the hero — replaces traditional headline + CTA hero
- Source-cite favicon ribbon under every answer — the brand's trust signal
- Dual-canvas system: graphite app + cream marketing

## What they DON'T do
- No second accent color — the brand is teal-on-graphite or teal-on-cream
- No gradient hero, no illustration hero, no photograph hero — search input is hero
- No emoji
- No drop shadows on answer cards — elevation is hairline + surface contrast
- No animation beyond the typewriter answer reveal and quiet fades
- No bold display weight beyond 500

## Exemplar pages
- https://perplexity.ai/
- https://perplexity.ai/discover
- https://perplexity.ai/pro
- https://perplexity.ai/enterprise

## When to reference
Reach for Perplexity when the user wants a search/answer-engine brand — sourced, technical, slightly serious, anti-chat-product. Especially appropriate for research tools, knowledge platforms, vertical search engines, and any product where the primary interaction is "ask a question, get a sourced answer." The search-pill-as-hero replaces the standard SaaS hero pattern entirely; downstream consumers should preserve this inversion.
