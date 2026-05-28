# Sourcegraph — DESIGN.md

## Overview
Sourcegraph's marketing surface pairs a deep slate near-black (`#0f111a`) with an electric blue (`#00cbec`) and a violet secondary (`#a112ff`) — a triad that reads as the inside of a compiler. Type is geometric sans (PolySans / IBM Plex Sans) tightened to a developer-tool cadence. Code lives at marketing scale: half of the homepage is real syntax-highlighted code mockups.

## Color
- **Primary:** `#00cbec` — Electric Cyan-Blue
- **Secondary:** `#a112ff` — Violet
- **Tertiary signal:** `#ff5543` — Coral Alert (used for code-error highlights, status only)
- **Canvas:** `#0f111a` — Slate Near-Black
- **Surface card:** `#1a1d29` — Elevated Slate
- **Ink (on dark):** `#f5f6fa` — Cool Cream
- **Body muted:** `#8a8fa3`
- **Hairlines:** `rgba(255,255,255,0.08)`
- **Code-string accent:** `#9ee493`
- **Code-keyword accent:** `#bf9eee`

## Typography
- **Display:** PolySans / Geist, weight 500-600, tracking -0.015em, sizes 56-96px
- **Body:** Inter, weight 400-500, 16-17px base, 1.55 line-height
- **Mono:** IBM Plex Mono / JetBrains Mono, weight 400, 14px

## Spacing & rhythm
8-base (8/16/24/32/48/64/96). Section padding 96px. Code blocks consume more vertical real estate than text — the rhythm is text band → big code mockup → text band.

## Motion signature
180ms ease-out on hover; signature is the cyan-blue gradient-line that traces under the Sourcegraph wordmark on load. Code-mockup screenshots have a slow scroll-reveal with a syntax-highlight pulse.

## Components observed
- `code-search-mockup-card` (full IDE chrome inside a card)
- `cody-chat-panel` (AI assistant panel mockup, signature treatment)
- `pricing-table-three-tier-dark`
- `category-tab-cyan-active`
- `cta-button-cyan-fill`
- `repository-graph-visual`

## Trademark signals
- Cyan-blue (`#00cbec`) is the brand voltage — never desaturated, never traded for purple
- Violet (`#a112ff`) reserved for Cody (AI assistant) feature pages only — a sub-brand color
- Code-search mockup as homepage hero — actual product UI as the marketing artifact
- Wordmark uses a custom-drawn `S` with a search-magnifier dot accent
- Logos arranged in a dark-canvas customer strip with subtle 1px hairlines between

## What they DON'T do
- No light-mode marketing surface
- No emoji or playful UI illustrations
- No 3D rendered code visualizations or floating geometry
- No mascot characters (Cody is a text-chat product, never anthropomorphized)
- No saturated rainbow gradients on code highlights — syntax theme is restrained

## Exemplar pages
- https://sourcegraph.com/
- https://sourcegraph.com/cody
- https://sourcegraph.com/pricing
- https://sourcegraph.com/code-search

## When to reference
Reach for Sourcegraph when the user wants a developer-tools surface that takes code seriously as marketing content. The slate + cyan + violet triad and the full-IDE-chrome mockups make it ideal for any product whose differentiator is the code experience itself — code search, AI coding assistants, refactoring tools, repo intelligence.
