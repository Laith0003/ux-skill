# Porsche — DESIGN.md

## Overview
Porsche is the Stuttgart sports-car house whose visual discipline is the opposite of every other German luxury automaker. Canvas is pure white or dark race-track-black. Type runs the proprietary Porsche Next typeface — a precise, modernist grotesk with subtle aperture variations — at every text tier. The signature is Porsche red (`#d5001c`) — historically reserved for the 911 GT badging, used scarcely on configurator highlights, on the wordmark in select moments, and on the iconic horse-and-shield crest. Photography is cinematic motorsport: cars at speed on Alpine roads, paddock close-ups of the 911 chassis, design-team studio portraits. The voice is engineering-first — every page reads like a Le Mans technical manual translated into web layout.

## Color
- **Primary:** `#d5001c` — Porsche red (GT badging + crest + rare configurator highlights)
- **Canvas:** `#ffffff` — Pure white (default)
- **Canvas dark:** `#000000` — Race-track-black (motorsport pages and configurators)
- **Ink:** `#0a0e10` — Deep ink for type
- **Accent (gold):** `#c8b063` — Stuttgart crest gold
- **Body:** `#3a3a3a`
- **Muted:** `#7a7a7a`
- **Hairlines:** `rgba(10,14,16,0.10)`

## Typography
- **Display:** Porsche Next, weight 700, 48–80px hero
- **Sub-display:** Porsche Next, weight 600, 24–32px section heads
- **Body:** Porsche Next, weight 400, 16–17px, 1.6 line-height
- **Caption:** weight 500, 13–14px metadata
- **Mono:** Porsche Next Mono, 14px for spec tables and lap-time callouts

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Configurator pages widen to full viewport with vehicle 3D-spinner at center. Spec-sheet tables align in precise 12-column grids. Hero motorsport video consumes 80vh.

## Motion signature
Cinematic motorsport. Hero videos auto-play silent: 911s carving through Pyrenees passes, slow-motion engine-bay close-ups, paddock pit-stops. Cross-fades at 1.2s — fast enough to feel kinetic but slower than Tesla's quick cuts. Hover lifts product tiles 6px with a sharp shadow (engineering precision, not soft luxury). Configurator color-changes animate the car body via 800ms color-tween.

## Components observed
- `cinematic-car-hero-video` — full-bleed motorsport video
- `configurator-3d-spinner` — vehicle 3D viewer with color/wheel/spec controls
- `spec-sheet-engineering-table` — engineering data in mono
- `lap-time-callout-card` — Nürburgring lap-time hero card
- `model-comparison-grid-precise` — 911 / Cayman / Taycan / Macan hierarchy
- `horse-shield-crest-mark` — gold-and-red Stuttgart crest beneath wordmark
- `button-primary-thin-rule` — hairline-outlined CTA
- `footer-stuttgart-corporate` — multi-language corporate footer

## Trademark signals
- Porsche Next at every tier — proprietary grotesk that reads as engineering-document, not fashion-magazine — refusing the serif-luxury convention
- Porsche red (`#d5001c`) reserved for 911 GT badging, horse-and-shield crest, rare configurator highlights — never a section background, never a CTA fill on standard product pages
- Stuttgart horse-and-shield crest — gold-and-red coat-of-arms — appears as a sub-mark beneath the 'PORSCHE' wordmark
- Cinematic motorsport photography — 911s on Alpine roads, paddock close-ups, engine-bay portraits — refusing the polished-on-white showroom convention
- Engineering-document copy — lateral-G performance, lap times, kilowatt outputs, drag coefficients — Porsche-spec, never marketing-spec

## What they DON'T do
- No fashion-serif substitution for Porsche Next — the grotesk IS the engineering voice
- No luxury cream canvas — Porsche is white-or-black; cream reads as Ferrari off-brand
- No static showroom-on-white photography — in-motion, on-track, in-paddock only
- No dropping the lap-time / spec-sheet — engineering data IS the voltage
- No Porsche red on every accent moment — reserved for GT badging and crest
- No emoji, no warm-pastel palette, no friendly illustration

## Exemplar pages
- https://porsche.com/
- https://porsche.com/usa
- https://porsche.com/911
- https://porsche.com/motorsport

## When to reference
Reach for Porsche when the user wants engineering-first sports-car luxury — premium automotive marketing, motorsport brands, performance-product B2B, high-end engineering portfolio. The "Porsche Next at every tier + crest sub-mark + cinematic motorsport video + engineering-spec copy" combination is the most-copyable Porsche move. Pairs well with brands that want to project precision and speed without resorting to Ferrari romanticism or Tesla minimalism.
