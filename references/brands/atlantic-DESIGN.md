# The Atlantic — DESIGN.md

## Overview
The Atlantic is American long-form editorial — a paper-warm canvas (`#fcf9f4`) with a modern serif display (Atlantic Condensed / Domaine Display) and a deep editorial red (`#c8102e`) for the masthead and section accents. The site reads as a literary magazine: long single-column articles, full-bleed essay-cover photography, drop caps on feature openers, byline blocks treated as art.

## Color
- **Primary:** `#c8102e` — Atlantic Red (masthead, section heads, link hover)
- **Canvas:** `#fcf9f4` — Paper Cream
- **Surface alt:** `#f3ede2` — Aged Paper
- **Surface card:** `#ffffff`
- **Ink:** `#000000` — Newsprint Black
- **Body:** `#1a1a1a` (very dark, near-black for reading)
- **Hairlines:** `rgba(0,0,0,0.15)` — visible 1px rules
- **Section accent (Books):** `#3b5f3b` — Forest
- **Section accent (Politics):** `#c8102e` (the red)
- **Section accent (Science):** `#2c5d8f` — Steel Blue

## Typography
- **Masthead:** Atlantic Condensed (custom), weight 700, condensed sans, 96-128px masthead-only
- **Display:** Domaine Display / GT Sectra Display, weight 500-700 (serif), tracking 0, sizes 56-96px feature headlines
- **Body:** Domaine Text / Tiempos Text, weight 400, 19px base (large for reading), 1.6 line-height
- **Byline / caption:** Atlantic Sans / Söhne, weight 500, 12-14px, tracking 0.2px caps
- **Drop cap:** First letter of feature articles set 4-5 lines tall in display serif

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/72). Single-column reading width ~680px. Section padding 96-120px. Full-bleed essay openers run edge-to-edge with display headline overlaid on photography.

## Motion signature
Almost none. 150ms ease-out hover on link hover. Long-form article scrolls have a slow progress indicator at top (red line, 100% scroll-bound). Audio-narration controls fade in as the article loads.

## Components observed
- `essay-cover-fullbleed` (full-screen photo with overlay headline in serif)
- `drop-cap-article-opener` (large serif first letter, 4-5 lines tall)
- `single-column-reading-body` (680px wide, Domaine Text 19px)
- `section-masthead-red` (Atlantic Red section name in caps)
- `byline-block-with-bio` (author photo + name + bio caption)
- `pull-quote-band` (massive serif italic pull-quote, hairlines above and below)
- `audio-narration-player` (subtle play button, "Listen to this article")

## Trademark signals
- Atlantic Red as the brand's only voltage — used on masthead, section names, link hover
- Drop caps on feature article openers — magazine convention preserved
- Domaine Text body at 19px — larger than most digital pubs, signals "we expect you to read"
- Audio-narration option on most long-form articles — accessibility as editorial feature
- Full-bleed essay cover photography with type overlay

## What they DON'T do
- No emoji in editorial content
- No animated illustrations in body articles
- No saturated rainbow gradients
- No mascot characters
- No dark-mode hero on homepage (article view supports dark separately)

## Exemplar pages
- https://www.theatlantic.com/
- https://www.theatlantic.com/magazine/
- https://www.theatlantic.com/podcasts/
- https://www.theatlantic.com/projects/

## When to reference
Reach for The Atlantic when the user wants long-form literary editorial — the most reading-first surface in the catalog. The paper-cream + Domaine + drop-cap + 19px body combination is appropriate for any publication, newsletter, essay platform, or content product whose value proposition is "people will sit and read for 30 minutes."
