# Robinhood — DESIGN.md

## Overview
Robinhood is the retail-investing platform brand for the millennial investor — confident, dark-first, data-dense. The canvas is a warm near-black (#0a0c0d), the signature voltage is an electric Robinhood Green (#00C805) reserved exclusively for market-up indicators and primary CTAs, Capsule sans carries every text tier, and large tabular-figure mono numerals carry every portfolio value. The brand reads as a serious trading platform that happens to look modern.

## Color
- **Primary:** `#00c805` — Robinhood Green (market-up, primary CTAs, brand mark)
- **Primary deep:** `#00a004` — Green Hover/Press
- **Accent (market-down):** `#ff5052` — Red (negative percent change, sell-state)
- **Canvas:** `#0a0c0d` — Warm Near-Black (the brand's trading-platform chrome)
- **Canvas (light pages):** `#ffffff` — Pure White (the recent 2026 light marketing variant)
- **Surface card:** `#15181a` — Elevated near-black
- **Surface alt:** `#1f2326` — Selected band background
- **Ink (on dark):** `#ffffff` — Pure white for portfolio values
- **Ink (on light):** `#0a0c0d` — Near-black for headlines on light marketing pages
- **Body:** `#a8aab2` — Secondary text on dark
- **Muted:** `#6e7178` — Captions, timestamps
- **Hairlines:** `rgba(255,255,255,0.08)` — Low-alpha white dividers
- **Chart fill green:** `rgba(0,200,5,0.15)` — Gradient fill below positive chart line
- **Chart fill red:** `rgba(255,80,82,0.15)` — Gradient fill below negative chart line

## Typography
- **Display:** Capsule Sans, weight 700, tracking -0.02em, sizes 48–72px hero
- **Sub-display:** Capsule Sans, weight 600, 28–32px section heads
- **Body:** Capsule Sans, weight 400, 16px, 1.5 line-height
- **Caption:** Capsule Sans, weight 500, 13px
- **Portfolio value:** Capsule Sans Mono (tabular), weight 600, 48–72px on portfolio overview, 24–32px in tiles
- **Price (small):** Capsule Sans Mono (tabular), weight 500, 14px
- **Percent change:** Capsule Sans Mono (tabular), weight 600, 14px (green or red)

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64/96). Section padding 64–96px. Portfolio chart hero consumes 60% of viewport with the chart line dominating. Stock-detail cards use 16px internal padding for tight density. Ticker rows: 12px vertical padding, 16px horizontal.

## Motion signature
Signature is the portfolio chart line drawing in at 800ms cubic-bezier on first paint. Price ticks animate at 200ms with a green or red flash on direction change. Tabular-figure number transitions use slot-machine ticks for portfolio value updates (~150ms per digit). Buy/sell pill CTAs have a 100ms press-down with a slight scale-down.

## Components observed
- `portfolio-chart-hero` — large chart with green or red line + gradient fill below
- `ticker-row-with-mono` — table row with ticker + name + tabular-figure price + percent change
- `feature-card-dark` — near-black card with hairline border
- `buy-sell-pill-cta` — large green or red pill button for buy/sell
- `stock-detail-card` — card with stock chart + key metrics in mono
- `crypto-portfolio-tile` — square tile showing crypto symbol + mono balance + percent change
- `footer-robinhood-dark` — dark multi-column footer with green section heads

## Trademark signals
- Robinhood Green (#00C805) — the electric green voltage
- Warm near-black canvas (#0a0c0d) — not pure black
- Tabular-figure mono numerals on every portfolio value
- Capsule sans at every tier — refuses Inter substitution
- Portfolio chart line flips color (green/red) based on day's performance

## What they DON'T do
- No emerald or lime substitution for Robinhood Green
- No pure black canvas — the warm tint is required
- No proportional figures for portfolio values
- No third chromatic accent — green + red + white only
- No drop shadows — hairlines and surface contrast carry elevation
- No emoji
- No serif anywhere

## Exemplar pages
- https://robinhood.com/
- https://robinhood.com/us/en/about
- https://robinhood.com/us/en/our-products
- https://robinhood.com/us/en/legend

## When to reference
Reach for Robinhood when the user wants a modern retail-investing or trading-platform brand — dark-first, data-dense, with green/red financial-data voltage. Especially appropriate for trading apps, investing platforms, crypto exchanges (consumer-facing), and any fintech where portfolio values must read as serious. The "Robinhood Green + warm near-black + tabular-figure mono" trio is the most copyable formula; preserve the strict color discipline (no third accent) to avoid drift into generic-fintech.
