# Pitchfork — DESIGN.md

## Overview
Pitchfork is raw, loud, bold black-on-white music criticism. The Pitchfork wordmark is set in a heavy black slab (an industrial-feeling display), reviews open with a massive 0.0-10.0 score numeral, and album-art is treated as the visual anchor. Color is mostly black, white, with one signal red for "Best New Music" badges. The whole brand reads as a 90s zine that made the journey to the web without losing its edge.

## Color
- **Primary:** `#000000` — True Black
- **Canvas:** `#ffffff` — White
- **Surface alt:** `#f5f5f5` — Newsprint Gray (used on sidebar and footer)
- **Ink:** `#000000`
- **Body:** `#222222`
- **Hairlines:** `#e1e1e1` — visible 1px rules
- **Best-New-Music red:** `#ff0000` — Pitchfork Red (BNM badge only)
- **Score accent:** Score numerals use a slightly de-saturated dark — `#1c1c1c` — set in huge display
- **Section accent:** Black-on-white only — no section-color system

## Typography
- **Display:** Pitchfork Sans (custom industrial sans) / Founders Grotesk Condensed, weight 900, tracking -0.02em, sizes 96-160px for score numerals
- **Headline:** Same family at weight 700, 32-64px
- **Body:** Tiempos Text / Source Serif, weight 400, 17-18px base, 1.55 line-height — body is serif against the heavy sans headlines
- **Byline:** Söhne weight 500, 13px, tracking 0.4px caps

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/72). Hero album-review uses a vertical stack: massive score numeral, album art square, headline, byline. List pages use 3-up grids with strict 1:1 album-art tiles.

## Motion signature
None on hover beyond a 100ms color shift on links. Score reveal on review page has a slight scale-in (98%-100%, 300ms) — the only moment of brand-voiced motion. Otherwise the brand voice is "the writing is the motion."

## Components observed
- `score-numeral-display` (massive 0.0-10.0 score in heavy condensed sans)
- `album-art-square-tile` (1:1 album cover, no shadow, hairline border)
- `best-new-music-badge` (small red rectangle, "Best New Music" white caps)
- `review-headline-band` (album title in display, artist name below in smaller weight)
- `byline-block-mono` (reviewer name + date in Söhne caps)
- `list-page-grid-three-up` (review tiles in strict 3-column grid)

## Trademark signals
- The 0.0-10.0 score numeral set at 96-160px — Pitchfork's most-recognized visual element
- Heavy industrial sans display — anti-elegant, anti-magazine
- Album art treated as the visual anchor, never decorative
- Best New Music red badge — small, hot, reserved
- Serif body against heavy sans display — the contrast is the brand

## What they DON'T do
- No emoji in editorial content
- No saturated rainbow gradients
- No dark-mode hero
- No mascot characters
- No section-color system — the brand is monochrome plus one red

## Exemplar pages
- https://pitchfork.com/
- https://pitchfork.com/reviews/albums/
- https://pitchfork.com/best/
- https://pitchfork.com/features/

## When to reference
Reach for Pitchfork when the user wants a music / cultural-criticism / opinionated-review surface. The score-numeral + heavy-industrial-sans + serif-body-against-sans-display combination is canonical music-zine-on-the-web aesthetic. Appropriate for any review-driven product where the rating is the marketing.
