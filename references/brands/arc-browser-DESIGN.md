# Arc Browser — DESIGN.md

## Overview
Arc is The Browser Company's post-Chrome browser that treats the address bar as the enemy. The brand canvas is a soft warm off-white (`#f5f3ed`) with deep ink, or alternatively a watercolor-gradient hero band sweeping pastel coral, peach, and lavender across a hand-drawn marketing page. The voice is wide-eyed earnest tech-utopianism — sentence-case headlines, generous serif accents (Söhne or Inter for body, with proprietary curvilinear display nameplates), and animation that feels closer to children's illustration than browser-chrome. Arc is the brand where motion IS the marketing.

## Color
- **Primary:** `#ff7a5c` — Arc coral (the brand's coral-peach voltage)
- **Canvas:** `#f5f3ed` — Warm off-white (deliberately not pure white)
- **Ink:** `#1a1a1a` — Deep warm-ink for type
- **Accent:** `#bca7e8` — Lavender pastel (secondary in hero gradients)
- **Watercolor gradient stops:** coral `#ff7a5c` → peach `#ffb89e` → lavender `#bca7e8` (full-bleed hero backgrounds)
- **Body:** `#3a3a3a`
- **Muted:** `#7a7a7a`
- **Hairlines:** `rgba(26,26,26,0.10)`

## Typography
- **Display:** ABC Diatype Mono / proprietary curvilinear face, weight 500, sentence-case only, 48–72px
- **Sub-display:** Söhne weight 500, 28–32px section heads
- **Body:** Söhne, weight 400, 17px essay body, 1.6 line-height
- **Caption:** Söhne weight 500, 14px
- **Mono:** ABC Diatype Mono, 14px for inline UI references

## Spacing & rhythm
8-base (8/16/24/32/48/64/96). Section padding 96–128px. Marketing pages are long-scroll narrative — each section reveals a new product feature with a custom animated UI mockup. Body content runs ~720px max-width.

## Motion signature
Constant gentle motion is the brand. Hero gradients drift slowly with watercolor-bleed transitions (~12s loop). UI mockups float with subtle 4px vertical bobs over 3s ease-in-out. Hover states scale 1.02x with a 200ms cubic-bezier. Page transitions use slow 600ms fade-with-translate, never abrupt cuts.

## Components observed
- `watercolor-gradient-hero` — full-bleed pastel coral/peach/lavender bleed
- `sidebar-tab-organic` — sidebar tab UI with rounded organic edges
- `feature-animation-card` — custom-animated UI mockup per feature
- `split-view-mockup` — illustrated split-view browser composition
- `color-palette-picker` — user-color personalization tile
- `command-bar-floating` — floating central command bar
- `button-primary-coral` — coral-fill CTA, rounded 12px
- `manifesto-paragraph-block` — earnest sentence-case manifesto prose

## Trademark signals
- Watercolor-gradient hero with painterly soft-bleed transitions — coral + peach + lavender
- Sentence-case display headlines ("Browse the web like a person") — never Title Case, never ALL CAPS
- Curvilinear hand-drawn UI mockups — sidebar tabs render with rounded organic edges, not chrome-rectangular grids
- Color-personalization theme: every Arc screenshot shows a different user's chosen palette — chrome is meant to be expressive
- Long-scroll narrative marketing — each section reveals a feature with a custom animated mockup

## What they DON'T do
- No Title Case or ALL CAPS headlines — sentence-case is the manifesto voice
- No hard linear gradient stops — the watercolor-bleed signature requires painterly transitions
- No flat rectangular Material/Fluent UI mockups — Arc UI renders with organic curves
- No single corporate color theme across screenshots — variety IS the personalization message
- No emoji, no decorative stock illustrations
- No static screenshot grids — the long-scroll narrative tour is the format

## Exemplar pages
- https://arc.net/
- https://thebrowser.company/
- https://arc.net/browse

## When to reference
Reach for Arc when the user wants playful tech-utopianism — earnest, hand-drawn, motion-as-marketing. Especially appropriate for consumer software with a "delight" voice, AI tools that want to feel friendly rather than industrial, and onboarding flows that benefit from narrative pacing. The watercolor-gradient hero and the sentence-case manifesto headline are the most-copyable Arc moves.
