# The Economist — DESIGN.md

## Overview
The Economist is the British weekly newspaper-of-record brand — a 200-year-old global authority with strict editorial discipline. The brand is anchored by Economist Red (#E3120B) in a 1.5cm top-bar strip running the full page width, Milo Serif slab-serif for every headline, Officina Sans humanist body, no bylines (articles are unsigned), and drop caps opening feature articles. The visual system is conservative, dense, and unmistakably print-magazine ported to the web.

## Color
- **Primary:** `#e3120b` — Economist Red (masthead bar, section eyebrows, dividers, drop caps)
- **Primary deep:** `#b80c08` — Red Hover/Press
- **Canvas:** `#ffffff` — Pure White
- **Surface card:** `#ffffff` — White card with hairline border
- **Surface alt:** `#f9f4eb` — Cream (sub-band backgrounds, podcast row, archive index)
- **Ink:** `#121212` — Near-black headlines and body
- **Body:** `#3a3a3a` — Default running text
- **Muted:** `#6b6b6b` — Captions, metadata, dates
- **Hairlines:** `#d2d2d2` — 1px dividers between articles
- **Inline-link:** `#e3120b` (with thin underline)

## Typography
- **Display:** Milo Serif (slab), weight 700, tracking -0.02em, sizes 28–56px headlines
- **Sub-display:** Milo Serif weight 700, 22–28px section heads
- **Body:** EconomistMilo (a Milo variant tuned for body) or fallback serif, weight 400, 16–17px, 1.55 line-height
- **Sans (ledes/metadata):** Officina Sans, weight 400–600, 14–16px
- **Caption:** Officina Sans, weight 500, 12–13px
- **Section eyebrow:** Officina Sans, weight 600, 12px, uppercase, +1.5px tracking, red color
- **Drop cap:** Milo Serif, weight 700, 80px, red, 3-line-deep float

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64). Section padding 48–64px (denser than typical SaaS). Article column width ~640px (narrow editorial reading column). Hero band shows masthead red bar + week's cover image + lead story headline + 3-story-stack secondary.

## Motion signature
Almost no motion. 200ms ease-out on hover. The masthead red bar never animates. Article-list entries have no scroll-fade. The brand stays static and print-like — refusing the animated chrome of modern publishers.

## Components observed
- `masthead-red-bar` — 1.5cm red strip running full page width as the brand masthead
- `article-card-with-eyebrow` — story card with red section eyebrow + Milo headline + serif lede
- `drop-cap-paragraph` — opening paragraph of feature articles with 3-line-deep red drop cap
- `section-eyebrow-red-caps` — uppercase red small-caps section label ("Britain", "Finance & economics")
- `issue-cover-card` — weekly cover image card with issue date and main story title
- `podcast-row-card` — podcast episode row with title + serif description + listen button
- `footer-economist-dense` — multi-column footer with red section heads + serif link lists

## Trademark signals
- Economist Red 1.5cm masthead bar
- Milo Serif slab at every headline tier
- No bylines — every article unsigned
- Drop caps on feature article opens
- Red small-caps section eyebrows

## What they DON'T do
- No bylines
- No serif substitution — Milo Serif is mandatory
- No second chromatic color
- No rounded corners on cards or images
- No animation, no parallax, no scroll-jacking
- No emoji
- No casual / conversational microcopy — the voice is formal-British-weekly

## Exemplar pages
- https://economist.com/
- https://economist.com/leaders
- https://economist.com/britain
- https://economist.com/finance-and-economics

## When to reference
Reach for The Economist when the user wants a heritage-editorial-newspaper brand — formal, authoritative, dense, anti-marketing. Especially appropriate for premium publications, research institutions, policy think tanks, and any media brand that wants to feel 100+ years old. The masthead-red-bar + drop-cap + no-byline combination is the brand's most distinctive editorial discipline; downstream consumers should preserve all three to capture the voice.
