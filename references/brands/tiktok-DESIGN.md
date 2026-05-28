# TikTok — DESIGN.md

## Overview
TikTok is the short-form-video platform brand — a pure black canvas, a signature cyan-and-magenta chromatic-aberration (Aqua #25F4EE + Magenta #FE2C55) reserved for the brand mark and selected moments, a vertical 9:16 video feed taking 100% of viewport, and a "content is the entire surface" approach where chrome floats over content. The brand reads as youthful, kinetic, slightly glitch-aesthetic.

## Color
- **Primary:** `#fe2c55` — TikTok Magenta (CTAs, heart-liked, brand-mark voltage)
- **Accent (aqua):** `#25f4ee` — Cyan (brand mark only, never as chrome)
- **Canvas:** `#000000` — Pure Black (the brand's structural canvas)
- **Surface card:** `#161616` — Elevated near-black for comment overlays
- **Surface alt:** `#1f1f1f` — Selected band background
- **Ink:** `#ffffff` — Pure white text on black
- **Body:** `#e5e5e5` — Slightly muted off-white for secondary text
- **Muted:** `#8a8a8a` — Captions, timestamps, follower counts
- **Hairlines:** `rgba(255,255,255,0.10)` — Low-alpha white dividers
- **Heart-liked:** `#fe2c55`

## Typography
- **Display:** Proxima Nova, weight 700, tracking -0.01em, sizes 32–56px (display rare — content carries the visual weight)
- **Username:** Proxima Nova, weight 700, 16px
- **Caption (video overlay):** Proxima Nova, weight 500, 14–16px, white with subtle 1px text-shadow for legibility on video
- **Body:** Proxima Nova, weight 400, 14–16px
- **Comment:** Proxima Nova, weight 400, 14px
- **Timestamp:** Proxima Nova, weight 400, 12px

## Spacing & rhythm
4-base (4/8/12/16/24/32). Vertical video feed: full viewport (no margins, no padding around video). Right-rail icon stack: icons spaced 24px vertically, anchored 16px from right edge. Comment overlay sheet: 70vh tall, slides up from bottom with 16px radius on top corners.

## Motion signature
Signature is the cyan-and-magenta chromatic-aberration on the brand mark — the two colors shift 4px apart at 600ms loops. Vertical feed videos use snap-scroll behavior. Heart pulse on double-tap scales to 1.4x at 300ms with a small red particle burst. Comment sheet slides up at 400ms cubic-bezier.

## Components observed
- `vertical-video-feed` — full-viewport 9:16 video player
- `right-rail-icon-stack` — floating column of circular icons (like, comment, share, follow, save)
- `chromatic-brand-mark` — d-glyph with cyan/magenta chromatic aberration
- `creator-avatar-floating` — circular profile photo floating above the icon stack
- `comment-overlay-sheet` — bottom-sheet comment list with rounded top corners
- `magenta-cta-pill` — large magenta-fill pill CTA, "Follow", "Sign up"
- `footer-tiktok-minimal` — minimal web footer (mobile has no footer)

## Trademark signals
- Cyan-and-magenta chromatic-aberration brand mark
- Pure black canvas — video is the only luminous element
- Vertical 9:16 video feed at full viewport
- Right-rail floating icon stack — chrome floats, doesn't anchor
- Magenta voltage for CTAs and heart-liked state

## What they DON'T do
- No backgrounds painted in the brand chromatic-aberration
- No landscape feed — vertical 9:16 only
- No third accent color
- No serif anywhere
- No drop shadows on chrome — text-shadow only for legibility on video
- No bottom-anchored action bars — right-rail floating only

## Exemplar pages
- https://tiktok.com/
- https://tiktok.com/foryou
- https://tiktok.com/explore
- https://newsroom.tiktok.com

## When to reference
Reach for TikTok when the user wants a short-form-vertical-video brand — youthful, kinetic, content-first, with floating chrome over video content. Especially appropriate for video apps, social-video platforms, mobile-first creative tools, and Gen-Z-leaning consumer products. The vertical-video-as-page + right-rail-icon-stack pattern is the brand's most structurally distinctive move; the cyan-magenta chromatic-aberration is the most copyable brand-mark treatment.
