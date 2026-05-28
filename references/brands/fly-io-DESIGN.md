# Fly.io — DESIGN.md

## Overview
Fly.io is the edge-compute platform brand with a deeply contrarian voice — engineering blog as marketing, irreverent copy, dense long-form posts wrapped in a hot-pink-to-violet gradient identity. The canvas is a warm near-black (#0a0a0f), body type is a literary serif (Lora), and the chrome is mono-heavy with real shell snippets embedded throughout. The brand reads like an old-internet engineering newsletter that happens to sell global infrastructure.

## Color
- **Primary (gradient start):** `#ff007a` — Hot Pink (the voltage)
- **Primary (gradient end):** `#8957ff` — Violet (the voltage)
- **Accent (cream):** `#f5f5f0` — Warm Off-White (text on dark)
- **Canvas:** `#0a0a0f` — Warm Near-Black
- **Surface card:** `#161620` — Elevated near-black
- **Surface alt:** `#1f1f2c` — Selected band background
- **Surface code:** `#0a0a0f` — Code block background (slightly inset)
- **Ink:** `#f5f5f0` — Warm off-white text
- **Body:** `#c4c4be` — Secondary text
- **Muted:** `#8a8a82` — Captions, metadata
- **Hairlines:** `rgba(245,245,240,0.08)` — Low-alpha cream dividers
- **Inline-link:** `#ff007a` — Hot pink for body links

## Typography
- **Display:** Söhne, weight 500, tracking -0.02em, sizes 48–80px hero (rare — most pages don't have a display tier)
- **Body:** Lora (or PT Serif) serif, weight 400, 17–18px, 1.65 line-height — the long-form blog face
- **Sub-display:** Söhne weight 500, 24–28px section heads in blog posts
- **Caption:** Söhne weight 500, 14px
- **Mono:** JetBrains Mono, 14px for shell snippets and code blocks
- **Inline code:** JetBrains Mono 13px on a slightly elevated surface

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64/96). Section padding 64–96px. Body column width 680px (narrower than typical) — the brand wants you to read. Shell snippets are 100% width inside the body column, with ~20px internal padding.

## Motion signature
Almost no motion. 150ms ease-out on hover. The signature animation is the hot-pink-to-violet gradient slow-drift on the brand-mark fly balloon — ~8s cycle. No carousels, no parallax, no animated icons. The static-blog-post feel is deliberate.

## Components observed
- `blog-post-card-bordered` — card listing a blog post with title in Söhne, byline in serif
- `shell-snippet-card` — dark code block with `fly launch`, `fly deploy`, `fly logs` etc. in mono
- `fly-balloon-gradient-mark` — the brand mark with the hot-pink-to-violet gradient drifting
- `region-map-card` — world map showing Fly's 35+ edge regions
- `pricing-tier-card-dark` — dark tier card with mono pricing in JetBrains Mono
- `docs-codeblock-card` — extended code-block card for documentation
- `footer-multi-column-dark` — multi-column dark footer

## Trademark signals
- Hot-pink-to-violet gradient on the brand mark and selected CTAs
- Lora serif body face — the anti-SaaS literary voice
- Real shell snippets embedded everywhere — the brand earns trust through code proof
- Irreverent technical copy — refuses "enterprise-grade", "leverage", "unlock"
- Warm near-black canvas — refuses pure black, refuses navy

## What they DON'T do
- No serif-free pages — Lora carries every body paragraph
- No corporate trust signals above the fold
- No "leverage", "synergy", "enterprise-grade"
- No emoji (the brand mark balloon is illustration, not emoji)
- No gradient outside the pink-to-violet pair
- No drop shadows — surface contrast and hairlines carry elevation

## Exemplar pages
- https://fly.io/
- https://fly.io/blog
- https://fly.io/docs
- https://fly.io/pricing

## When to reference
Reach for Fly.io when the user wants an old-internet engineering-blog voice — irreverent, technical, long-form, anti-SaaS-cliché. Especially appropriate for infrastructure brands, technical content companies, developer-tool brands that compete on engineering culture rather than enterprise features. The serif-body-on-dark pattern is uniquely Fly.io's; downstream consumers should preserve the literary body face if they want the voice.
