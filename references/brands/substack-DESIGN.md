# Substack — DESIGN.md

## Overview
Substack is writer-first warmth — a cream canvas (`#f9f7f1`) with the signature Substack orange (`#ff6719`) for the "Subscribe" CTA and brand accents. Display runs a slab serif (Spectral / Vollkorn) and body uses Inter at a generous 17-18px reading size. The brand reads like a small-press literary magazine that grew up — every page reinforces "this is for writers."

## Color
- **Primary:** `#ff6719` — Substack Orange
- **Primary deep:** `#e6571a`
- **Canvas:** `#f9f7f1` — Cream Paper
- **Surface alt:** `#ffffff` — White (used inside subscriber-only article frames)
- **Surface card:** `#ffffff`
- **Ink:** `#1a1a1a` — Ink
- **Body:** `#363636`
- **Hairlines:** `rgba(26,26,26,0.10)`
- **Accent (subscriber green):** `#1a936f` — Subscriber Status
- **Accent (paid-tier gold):** `#c9a227` — Premium Tier Marker

## Typography
- **Display:** Spectral / Vollkorn (slab serif), weight 600-700, tracking -0.005em, sizes 48-72px hero
- **Body:** Inter / Source Serif Pro (writer's choice), weight 400, 17-18px base, 1.6 line-height
- **Newsletter masthead:** Often customizable per writer — Spectral is the default
- **Subscribe CTA:** Inter weight 600, 16px

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/72). Reading column ~700px. Section padding 64-96px on marketing pages. Newsletter articles have minimal chrome — the writing is the marketing.

## Motion signature
180ms ease-out on hover; signature is the Subscribe button glow (soft orange outer ring) when entering viewport mid-article. New-post notifications slide in from the right with 300ms ease.

## Components observed
- `newsletter-masthead-card` (writer's avatar, name in display serif, subscribe CTA)
- `subscribe-cta-orange-fill` (full-width orange button, white type)
- `article-card-with-byline` (cream surface, serif headline, writer avatar + name)
- `paywall-card-soft` (gentle gradient fade with subscribe CTA below)
- `comment-thread-nested` (lightly indented, hairline-separated)
- `discover-grid-three-up` (newsletter discovery grid, photo + serif name + subscriber count)

## Trademark signals
- Substack Orange (`#ff6719`) — the most-recognized "Subscribe" button color on the writer-platform internet
- Slab-serif display (Spectral) — literary-magazine cadence, distinguishes from Medium's geometric sans
- 17-18px body reading size — accessible reading-first commitment
- Subscriber count displayed openly on every newsletter — social proof as content
- Writer-customizable masthead colors and fonts — the platform bends to the writer's brand

## What they DON'T do
- No emoji in marketing chrome (writers can use them in posts; the platform itself doesn't)
- No dark-mode hero on marketing
- No saturated rainbow gradients
- No mascot characters
- No "limited time" or scarcity marketing — the brand is the slow read

## Exemplar pages
- https://substack.com/
- https://substack.com/browse
- https://substack.com/about
- https://on.substack.com/

## When to reference
Reach for Substack when the user wants a writer-platform / newsletter / content-creator product surface. The cream-canvas + slab-serif + orange-subscribe-CTA combination is the canonical "writer-first" aesthetic. Especially appropriate for any content product where individual creators are the brand and the platform's job is to recede.
