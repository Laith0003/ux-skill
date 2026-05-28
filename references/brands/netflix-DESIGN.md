# Netflix — DESIGN.md

## Overview
Netflix is the streaming entertainment brand whose visual language is the world's most-copied dark-canvas content grid. Canvas is true cinema-black (`#141414`) — the deepest dark in the streaming category. The signature is Netflix red (`#e50914`) — a pure red used only on the wordmark, on the play-button overlay, and on the primary 'Sign In' / 'Sign Up' CTA. Type runs the custom Netflix Sans (a precise grotesk with subtle aperture tweaks) at modest scale — the brand voice is 'content is the hero, chrome stays invisible'. The signature visual is the horizontal-scroll row of poster-art tiles: each row is a curated category ('Continue Watching', 'Top 10', 'Because you watched...') of poster-art rectangles, the brand-defining UI pattern in the streaming category.

## Color
- **Primary:** `#e50914` — Netflix red (wordmark + play-button + Sign In CTA)
- **Canvas:** `#141414` — True cinema-black
- **Canvas deep:** `#000000` — Full-bleed video underlays
- **Ink:** `#ffffff` — White type on dark
- **Muted:** `#777777` — Captions, metadata, time-since-upload
- **Body:** `#e5e5e5`
- **Hairlines:** `rgba(255,255,255,0.10)`

## Typography
- **Display:** Netflix Sans, weight 700, 36–56px hero
- **Sub-display:** Netflix Sans, weight 600, 20–28px row titles
- **Body:** Netflix Sans, weight 400, 15–16px, 1.5 line-height
- **Caption:** weight 500, 12–13px metadata
- **Mono:** none

## Spacing & rhythm
8-base (8/16/24/32/48). Section padding 48–64px between poster rows. Each horizontal-scroll row is a category title above a strip of 6–8 poster tiles at desktop. Hero auto-play video consumes 60–70vh.

## Motion signature
Hero auto-plays muted clip — typically 30 seconds of a featured show with slow camera moves and atmospheric music. Poster-art tiles on row-hover lift 1.08x scale with a 200ms ease-out and reveal hover-preview (auto-play 6-second clip). The signature 'TUDUM' sonic mnemonic — the brand's audio motif — plays on app cold-start.

## Components observed
- `hero-auto-play-video` — full-bleed muted video hero
- `poster-row-horizontal-scroll` — category-titled poster strip
- `poster-tile-rectangular` — 16:9 or portrait poster art tile
- `top-10-ranked-row` — Top 10 row with large rank-number overlay
- `billboard-card-feature` — featured-show billboard with logo + tagline
- `play-button-circular-red` — circular red play button
- `button-primary-netflix-red` — red-fill 'Sign In' CTA
- `footer-dark-multi-language` — black footer with language selector

## Trademark signals
- True cinema-black canvas (`#141414`) — the deepest dark in the streaming category — never a gray, never a navy
- Netflix red (`#e50914`) — pure red, used only on the wordmark, play-button overlays, 'Sign In' CTA — never a section background or category divider
- Horizontal-scroll poster-art rows — each row is a category title above a horizontal-scroll strip of poster-art rectangles — the brand-defining UI pattern
- Auto-playing hero clip — top-of-app or top-of-page video that runs muted with subtle volume-control affordance
- Custom Netflix Sans typography — grotesk with extremely subtle aperture variations that distinguish it from generic Inter / Helvetica

## What they DON'T do
- No lightening the canvas — `#141414` IS the brand-defining dark
- No tinting the red — pure `#e50914`
- No replacing horizontal-scroll rows with featured-cards — the row IS the brand
- No pausing the hero clip — auto-play muted video is the streaming-hero moment
- No secondary chromatic accent — black + white + red is the trinity
- No emoji, no playful illustration, no warm-cream surface

## Exemplar pages
- https://netflix.com/
- https://netflix.com/browse
- https://netflix.com/tudum
- https://about.netflix.com/

## When to reference
Reach for Netflix when the user wants the canonical streaming-platform UI — content-first dark-canvas products, video streaming, content libraries with category-curation. The "true cinema-black + Netflix red + horizontal-scroll category rows + auto-play hero" combination is the most-copyable Netflix move. Pairs well with any media product whose brand promise is 'we curate, you consume'.
