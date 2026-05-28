# Railway — DESIGN.md

## Overview
Railway is the infrastructure-deployment brand for the "make-cloud-feel-magical" generation — built on a deep midnight-violet canvas (#13111c, deliberately not black), a single lavender-purple voltage (#9c7dff) for CTAs, and Berkeley Mono everywhere service names, env vars, and URLs appear. The hero IS a node graph of services — database, API, cron, worker — connected with hairlines and pulsing with deploy activity. The brand reads as "the magical version of cloud."

## Color
- **Primary:** `#9c7dff` — Railway Lavender (the only voltage accent, glow on hover)
- **Accent (soft):** `#c4b5fd` — Lavender Soft (secondary highlights, hover states)
- **Canvas:** `#13111c` — Midnight Violet (the brand chrome)
- **Surface card:** `#1d1a2b` — Elevated violet for cards
- **Surface alt:** `#0d0b15` — Deeper violet for footer and modals
- **Surface code:** `#08070d` — Near-black violet for code blocks
- **Ink:** `#fdfaff` — Off-white text on violet
- **Body:** `#b4afc9` — Secondary text
- **Muted:** `#807994` — Captions, metadata, env var values
- **Hairlines:** `rgba(196,181,253,0.12)` — low-alpha lavender dividers (the brand decision)
- **Success:** `#5dd49f` — Deploy success status
- **Warning:** `#ffb849` — Deploy warning status
- **Error:** `#ff5d6c` — Deploy failure status

## Typography
- **Display:** Söhne, weight 500, tracking -0.02em, sizes 48–72px hero
- **Sub-display:** Söhne weight 500, 28–32px section heads
- **Body:** Söhne, weight 400, 16px, 1.55 line-height
- **Caption:** Söhne weight 500, 13–14px
- **Mono:** Berkeley Mono, 14px for service names + env vars + URLs + code (this carries 40%+ of all text on the page)

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64/96). Section padding 96px. Service graph hero typically consumes 60% of viewport. Cards use 24px internal padding. Env-var tables use 12px row height with monospace alignment.

## Motion signature
Signature is the service-graph nodes pulsing on deploy — ~1.5s breathing cycle with an 8% scale variation. Link hovers fade at 200ms. Deploy-progress bars sweep at 400ms ease-out. The lavender CTA has a subtle 16px outer glow that intensifies on hover (200ms ease-out). Deploy logs stream in at ~50ms per line with a slight fade.

## Components observed
- `service-graph-hero` — node graph of services connected with hairlines
- `service-node-card` — circular or square node with service name in mono, pulsing on activity
- `deploy-log-stream-card` — terminal-styled card with streaming deploy logs
- `env-var-table-mono` — dense table of NAME=value rows in Berkeley Mono
- `pricing-tier-card-dark` — violet tier card with lavender CTA
- `metrics-chart-card` — dark chart card with lavender stroke lines
- `footer-violet-dense` — deep-violet multi-column footer

## Trademark signals
- Midnight-violet canvas — not black, not navy
- Lavender purple accent with subtle outer glow on CTAs
- Berkeley Mono everywhere for service names, env vars, URLs
- Service graph as hero — interactive, pulsing
- Hairlines drawn in low-alpha lavender — color-tinted dividers

## What they DON'T do
- No pure black canvas — the violet tint is the brand
- No second voltage color
- No serif anywhere — the brand is grotesk + mono only
- No static product screenshot hero — the service graph is the hero
- No emoji
- No gradient mesh — single-color glow only

## Exemplar pages
- https://railway.com/
- https://railway.com/pricing
- https://railway.com/templates
- https://railway.com/docs

## When to reference
Reach for Railway when the user wants a developer-infrastructure brand that feels magical without being cute — node-graph product visualization, mono-heavy chrome, single lavender voltage. Especially appropriate for PaaS / IaaS / deployment tools / DevOps platforms. The service-graph-as-hero pattern is the brand's most copyable move; downstream consumers should preserve the node-and-edge visualization and the mono-text density.
