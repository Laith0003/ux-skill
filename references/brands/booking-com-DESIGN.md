# Booking.com — DESIGN.md

## Overview
Booking.com is the Amsterdam-based travel-booking behemoth whose brand discipline is the opposite of luxury hospitality: dense, data-rich, urgency-driven, and unapologetically transactional. Canvas is pure white with crisp ink. The signature is the Booking.com blue (`#003580`) used at full saturation on the navigation, on the primary 'Search' CTA, and on the wordmark — a deep cobalt that reads as 'trustworthy financial institution' more than 'travel'. Type runs a precise grotesk (Booking Sans / system grotesk) at modest scale. The brand voltage is the urgency overlay: '5 people are looking at this property', 'Last booked 2 hours ago' — micro-copy interventions that turn search results into a high-pressure auction floor.

## Color
- **Primary:** `#003580` — Booking.com cobalt blue (nav + CTAs + wordmark)
- **Canvas:** `#ffffff` — Pure white
- **Ink:** `#1a1a1a` — Deep ink for headlines
- **Accent (loyalty):** `#febb02` — Yellow, reserved for Genius badges and review-value stickers
- **Urgency:** `#e21c3c` — Red, reserved for 'X rooms left' badges and limited-time overlays
- **Review-score green:** `#008009` — used on the iconic 10-out-of-10 lozenge
- **Body:** `#262626`
- **Muted:** `#6b6b6b`
- **Hairlines:** `#e6e6e6`

## Typography
- **Display:** Booking Sans / system grotesk, weight 700, 28–36px (modest hero — never 80px)
- **Sub-display:** weight 600, 20–24px section heads
- **Body:** weight 400, 14–15px running text, 1.5 line-height
- **Caption:** weight 500, 12–13px metadata, urgency micro-copy
- **Mono:** none — the brand is text + data, no code

## Spacing & rhythm
4-base (4/8/12/16/24/32/48). Section padding 24–48px — far tighter than luxury sites. The page packs 20+ property cards above the fold; 3-hero curation reads as off-brand. Sidebar filter rail (260–300px) + map split + result list is the canonical layout.

## Motion signature
Urgency-driven. 'Booked X hours ago' counters update in real-time via subtle 200ms cross-fade. 'Limited rooms' badges pulse red over a 1.2s ease-in-out loop. Hover on property tile fades a 1px blue border in over 150ms. The brand voice is 'transactional pressure', never 'leisurely browse'.

## Components observed
- `search-bar-hero-dense` — date-picker + destination + occupancy in a tight horizontal row
- `property-result-card-with-urgency` — image + name + price + review-score + urgency overlay
- `review-score-lozenge` — the iconic 10-out-of-10 badge with 'Excellent' label
- `urgency-banner-red` — '2 rooms left at this price' red banner
- `filter-sidebar-dense` — 200+ filter checkboxes in a scroll-rail
- `genius-loyalty-tier-badge` — yellow gem-shaped loyalty badge
- `map-and-list-split-view` — left map, right scrolling result list
- `button-primary-blue` — full-saturation cobalt CTA

## Trademark signals
- Booking.com cobalt (`#003580`) — full saturation on nav and primary CTAs — reads as banking, not travel
- Yellow secondary accent (`#febb02`) reserved for Genius loyalty and review-value stickers — never as a CTA fill
- Urgency overlay micro-copy ('Last booked 4 hours ago', '17 people are looking right now') on every property card
- 10-out-of-10 review-score lozenge with the 'Excellent' label and review count on every property hero
- Dense property-result grid — 4-up at desktop with map, list, filters, pagination all visible simultaneously

## What they DON'T do
- No dropping urgency micro-copy — the 'X people are looking' overlays ARE the brand voltage
- No softening the cobalt — lightening reads as 'travel boutique', off-brand
- No 3-hero curation — the dense result grid IS the brand
- No shrinking the review-score lozenge
- No yellow CTA fills — yellow is locked to loyalty and review-value
- No emoji, no luxury photography hero, no cinematic full-bleed video

## Exemplar pages
- https://booking.com/
- https://booking.com/searchresults.html
- https://booking.com/genius.html
- https://booking.com/help

## When to reference
Reach for Booking when the user wants transactional density with social-proof voltage — marketplace search, e-commerce result grids, ticket inventory pages, classified-listing platforms. The "deep cobalt + urgency micro-copy + dense grid" combination is the most-copyable Booking move and is the brand to study when the goal is conversion-optimized search-result UX rather than aspirational marketing.
