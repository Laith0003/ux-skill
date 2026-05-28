# Apple Music — DESIGN.md

## Overview
Apple Music's marketing and browse surfaces sit at an interesting intersection: Apple's clean SF Pro chrome and a white canvas paired with full-bleed album-cover-driven hero bands. The brand is a chameleon dressed in SF Pro — every page derives its chromatic system from the featured album or artist artwork. The one fixed accent is Apple Music's signature red (#fa233b) for the brand mark and "Try free" CTAs.

## Color
- **Primary:** `#fa233b` — Apple Music Red (the brand mark + "Try free" CTAs)
- **Primary deep:** `#cc1c30` — Red Hover/Press
- **Canvas:** `#ffffff` — Pure White
- **Surface card:** `#ffffff` — White card with subtle elevation
- **Surface alt:** `#f5f5f7` — Apple Off-White (between bands and selected card backgrounds)
- **Surface dark:** `#1d1d1f` — Near-black for the desktop player chrome and selected dark bands
- **Ink:** `#1d1d1f` — Near-black for headlines and primary text
- **Body:** `#424245` — Default running text
- **Muted:** `#86868b` — Captions, metadata, track durations
- **Hairlines:** `#d2d2d7` — 1px borders and divider lines
- **Dynamic:** the album artwork supplies the page's chromatic accents — gradient backgrounds, hover glow color, and pull-quote tint are derived from the featured artwork

## Typography
- **Display (hero):** SF Pro Display, weight 700, tracking -0.02em, sizes 48–80px hero
- **Display (track):** SF Pro Display, weight 600, 32–40px track and artist names
- **Sub-display:** SF Pro Display weight 600, 22–28px section heads
- **Body:** SF Pro Text, weight 400, 15–17px, 1.5 line-height
- **Caption:** SF Pro Text, weight 500, 13px
- **Mono:** SF Mono, 13px for rare timestamp displays

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/64). Section padding 64–96px. Album-cover hero often consumes 800–1200px of vertical real estate. "For You" grid: 2-up large featured tiles, 4-up secondary tiles, horizontal-scroll rails of playlist cards below. Track-list rows use 12px vertical padding for tight density.

## Motion signature
Signature is the album-cover parallax — featured artwork shifts at 30% of scroll velocity creating a depth effect. Play-button hover scales to 1.05 at 200ms ease-out. The persistent desktop player floats up at 400ms cubic-bezier on first paint. Horizontal-scroll rails snap to playlist card boundaries.

## Components observed
- `album-cover-hero-fullbleed` — giant featured artwork at 800–1200px tall
- `play-button-circular-red` — circular red-fill button with white triangle, appears on hover
- `track-row-with-artwork` — track list row with 60×60 artwork, track + artist, duration, controls
- `playlist-rail-scroll` — horizontal-scroll rail of playlist tiles, snap-aligned
- `artist-portrait-card` — featured artist card with full-bleed portrait
- `lyrics-overlay-band` — lyrics display overlay with color-derived background
- `footer-light-apple` — light Apple-standard footer with hairline-divided columns

## Trademark signals
- Album cover as hero and as the page's chromatic system
- Apple Music red (#fa233b) as the only fixed brand accent
- SF Pro Display weight 700 for hero titles, weight 600 for artist names
- Floating circular red play-button with white triangle
- Editorial "For You" grid + horizontal-scroll playlist rails

## What they DON'T do
- No brand-color hero backgrounds (the album cover IS the color)
- No SF Pro substitution
- No emoji (the play triangle is the only glyph)
- No album-cover overlays or gradients — artwork shown as-is
- No saturated CTAs outside the Apple Music red
- No drop shadows on cards — hairlines and surface contrast carry elevation

## Exemplar pages
- https://music.apple.com/
- https://music.apple.com/browse
- https://apple.com/apple-music
- https://music.apple.com/us/new

## When to reference
Reach for Apple Music when the user wants a media-streaming brand where the content artwork IS the design system — film posters, album covers, magazine covers driving page chrome. Especially appropriate for music apps, podcast platforms, video streaming, and any product where featured artwork should drive page color. The "fixed-red-accent + artwork-derived-canvas" pattern is the brand's most distinctive move; the floating circular play-button is the most copyable interaction primitive.
