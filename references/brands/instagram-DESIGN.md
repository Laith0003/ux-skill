# Instagram — DESIGN.md

## Overview
Instagram is the photo-and-video social platform brand — a white canvas (light mode) or near-black canvas (dark mode), a signature multi-stop gradient reserved for the brand mark and the Stories unread-ring, a strict grotesk sans (Instagram Sans / Helvetica Neue) carrying every text tier, and a 3-column square photo grid that IS the brand's entire visual system. The chrome stays invisible so the content can carry every visual moment.

## Color
- **Primary (gradient stop 1):** `#fcb045` — Yellow
- **Primary (gradient stop 2):** `#fd1d1d` — Orange-Red
- **Primary (gradient stop 3):** `#833ab4` — Magenta-Purple
- **Accent (heart-liked):** `#ed1c84` — Heart Pink (the only single-color accent in the system, used on liked-state heart icons)
- **Canvas (light):** `#ffffff` — Pure White
- **Canvas (dark):** `#000000` — Pure Black
- **Surface card (light):** `#ffffff` with hairline border
- **Surface card (dark):** `#1a1a1a` — Elevated near-black
- **Ink (light):** `#262626` — Near-black for body text
- **Ink (dark):** `#fafafa` — Off-white text on dark
- **Muted:** `#8e8e8e` — Captions, timestamps, secondary metadata
- **Hairlines (light):** `#dbdbdb` — 1px borders and dividers
- **Hairlines (dark):** `#262626` — 1px borders on dark
- **Inline-link:** `#00376b` — The body-link blue (subtle, deep navy-blue)

## Typography
- **Display:** Instagram Sans / Helvetica Neue, weight 600, tracking -0.01em, sizes 24–48px (Instagram doesn't have a true display tier — the content is the display)
- **Body:** Instagram Sans / Helvetica Neue, weight 400, 14–16px, 1.4 line-height
- **Username:** Instagram Sans, weight 600, 14px
- **Caption:** Instagram Sans, weight 400, 14px
- **Timestamp:** Instagram Sans, weight 400, 12px, uppercase letter-spacing +0.5px

## Spacing & rhythm
4-base (4/8/12/16/24/32). Feed posts use a fixed ~470px column at desktop with 16px padding. Profile grid: 3-column square grid with 4px gap. Stories tray: horizontal-scroll row of 70px circular avatars. Bottom nav: 5 evenly-spaced icons.

## Motion signature
Signature is the Stories ring rotating gradient — ~2s loop animation on unread stories. Double-tap heart pulses to 1.3x scale at 300ms cubic-bezier with a small particle burst. Image-grid items have no hover transform on desktop — content carries all visual weight. Feed-scroll uses native momentum scrolling.

## Components observed
- `feed-post-card` — single post with avatar header + image + actions row + caption
- `stories-tray-ring` — horizontal-scroll row of avatars with rotating gradient ring on unread
- `story-circle-avatar` — circular profile photo with the gradient unread ring
- `profile-grid-square` — 3-column square grid of profile posts (the brand's structural signature)
- `bottom-nav-icon-row` — 5 outlined icons (Home, Search, Reels, Shop, Profile)
- `heart-icon-liked` — outlined heart that fills pink (#ed1c84) on liked state
- `create-button-gradient` — the "+ Create" button with the brand gradient fill
- `footer-instagram-minimal` — minimal footer on web only (mobile has no footer)

## Trademark signals
- Multi-stop gradient (yellow → orange-red → magenta-purple) on brand mark and Stories ring only
- 3-column square photo grid as the entire visual system
- Monochrome chrome — white/near-black duet with gradient mark
- Circular profile avatars at every scale with gradient unread-ring
- Four-icon action row (heart, comment, share, save) beneath every post

## What they DON'T do
- No backgrounds painted in the brand gradient — gradient is reserved
- No chromatic accent colors beyond the heart pink
- No serif anywhere — Instagram Sans / Helvetica Neue only
- No drop shadows — hairlines carry elevation
- No emoji as UI affordances
- No display headlines — content is the display

## Exemplar pages
- https://instagram.com/
- https://instagram.com/about
- https://about.instagram.com

## When to reference
Reach for Instagram when the user wants a content-first social-platform brand — square photo grid, gradient brand mark, invisible chrome. Especially appropriate for photo apps, social feeds, content-creator platforms, and any product where user-generated visual content should carry every visual moment. The "monochrome chrome + gradient mark + 3-up square grid" pattern is the brand's most copyable formula; preserve the strict gradient discipline (mark only, never backgrounds) to avoid AI-slop drift toward gradient-everywhere.
