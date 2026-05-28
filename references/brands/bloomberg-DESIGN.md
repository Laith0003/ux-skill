# Bloomberg — DESIGN.md

## Overview
Bloomberg's marketing/news surface borrows from the terminal — black canvas (`#0a0a0a`) with the signature Bloomberg orange (`#fb8b1e`) for "live" indicators, tickers, and CTA voltage. Display uses a geometric serif (Bloomberg Cousine / Tiempos) with an editorial weight; body uses Bloomberg Inc — a custom humanist sans. The brand reads as a financial-news institution that uses its terminal heritage as design language. Dense data, generous editorial typography, hairline-rule rhythm.

## Color
- **Primary:** `#fb8b1e` — Bloomberg Orange
- **Primary deep:** `#d9700f`
- **Canvas:** `#0a0a0a` — Terminal Black (news/marketing dark mode)
- **Canvas alt (long-form articles):** `#ffffff` — Reading White
- **Surface card (on dark):** `#1a1a1a`
- **Surface card (on light):** `#f7f7f7` — Newsprint Gray
- **Ink (on dark):** `#ffffff`
- **Ink (on light):** `#000000`
- **Body (on dark):** `#cccccc`
- **Body (on light):** `#222222`
- **Hairlines:** `rgba(255,255,255,0.15)` on dark, `rgba(0,0,0,0.15)` on light
- **Ticker red (negative):** `#d04545`
- **Ticker green (positive):** `#1cb585`

## Typography
- **Display:** Bloomberg Cousine / Tiempos Display, weight 500-700 (serif), tracking -0.01em, sizes 48-96px headlines
- **Body:** Bloomberg Inc / Söhne, weight 400-500, 16-18px base, 1.55 line-height
- **Mono (data / ticker):** Bloomberg Mono / IBM Plex Mono, weight 500, 13-14px tabular figures
- **Section caps:** Bloomberg Inc weight 700, 11px, 1.5px tracking caps

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64/96). Section padding 64-96px. Article reading column ~720px. Homepage uses dense multi-column grid with hairline dividers everywhere — terminal data-grid lineage.

## Motion signature
180ms ease-out on hover; signature is the ticker-style horizontal scroll of stock data at the top of the page (continuous linear loop, 60s). Live-indicator pulses orange. Chart data lines draw on with 800ms ease on viewport entry.

## Components observed
- `live-ticker-strip-orange` (orange-text scrolling ticker at top of page)
- `headline-serif-large` (Tiempos serif, 48-96px, editorial weight)
- `data-table-tabular-figures` (mono numerals, hairline rows, ticker-color positive/negative)
- `chart-card-dark` (full data viz with orange accent line)
- `article-byline-block-caps` (Bloomberg Inc caps, hairline below)
- `subscribe-cta-orange-fill`
- `section-grid-multi-column` (dense terminal-inspired grid)

## Trademark signals
- Bloomberg Orange (`#fb8b1e`) — one of the most-recognized accent colors in financial media
- Ticker scrolling at top of every page — terminal-heritage UX preserved
- Hairline-rule rhythm — every section, table row, byline separated by 1px lines
- Tabular figures EVERYWHERE numbers appear — the brand respects financial data
- Serif headlines against sans body — editorial weight in a data-heavy product

## What they DON'T do
- No emoji in news content
- No saturated rainbow gradients
- No mascot characters
- No flat-cartoon illustrations in finance content
- No "cooling" the orange — it stays at full saturation

## Exemplar pages
- https://www.bloomberg.com/
- https://www.bloomberg.com/markets
- https://www.bloomberg.com/businessweek
- https://www.bloomberg.com/opinion

## When to reference
Reach for Bloomberg when the user wants a financial-news / data-dense / institutional editorial surface. The terminal-black + orange + ticker + tabular-figure combination is canonical "we own the financial data conversation" aesthetic. Especially appropriate for any product where the data itself is the marketing — financial media, market-intelligence, stock-tracking, analytics platforms.
