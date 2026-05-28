# Anthropic — DESIGN.md

## Overview
Anthropic is the corporate-research brand sister to the Claude product — same parent company, very different surface. Where Claude reads as a warm consumer chat product, Anthropic reads as a literary technology publisher: warm putty canvas, Tiempos serif at every display tier, narrow editorial body columns, and a thin red-clay accent kept almost entirely in reserve. The page IS the essay; there are almost no marketing devices.

## Color
- **Primary:** `#191919` — Anthropic Ink (used for type and rare CTAs)
- **Canvas:** `#f0eee6` — Putty (the most-recognized brand cue)
- **Surface card:** `#ffffff` — White cards on putty
- **Surface alt:** `#e8e4d6` — Putty Deep (selected band backgrounds)
- **Accent (clay):** `#cc785c` — Red-Clay (inline article links + radial-spike glyph only)
- **Accent (signal):** `#5db8a6` — Quiet teal (rare status dots)
- **Ink:** `#191919`
- **Body:** `#4d4d4d`
- **Muted:** `#737373` — captions, dates, secondary metadata
- **Hairlines:** `rgba(25,25,25,0.12)` — visible 1px borders on cards

## Typography
- **Display:** Tiempos Headline, weight 400, tracking -0.02em, sizes 40–88px hero
- **Sub-display:** Tiempos Headline weight 400, 28–32px section heads
- **Body:** Styrene B / Inter, weight 400, 17px essay body, 1.6 line-height
- **Caption:** Styrene B weight 500, 13–14px, uppercase tracking +1.5px for category eyebrows
- **Mono:** JetBrains Mono, 14px, for any code or numeric callouts in research posts

## Spacing & rhythm
8-base (8/16/24/32/48/64/96/128). Section padding 96–128px. Essay column max-width ~640px (narrower than typical SaaS) — the brand is comfortable being a column of running serif text. Hero band uses no grid; just headline + dek + byline stacked center-left.

## Motion signature
Quiet to the point of nearly absent. 200ms ease-out on link hovers; research-list entries reveal at a 600ms scroll-fade with no translate. No carousels, no parallax, no autoplay video.

## Components observed
- `research-card-bordered` — white card on putty, 1px hairline, Tiempos title + Styrene byline
- `essay-byline-row` — author name + role + date, Styrene 14px / 500
- `radial-spike-glyph` — the Anthropic 4-spoke asterisk, used as content marker
- `inline-link-clay` — body links in red-clay with thin underline
- `narrow-essay-column` — 640px max-width long-form body
- `policy-pdf-row` — file-list row with title + author + date + download icon
- `footer-multi-column-dark` — dark putty-ink footer with 4 link columns

## Trademark signals
- Putty canvas across every page — deliberately not Claude's cream and deliberately not OpenAI's white
- Tiempos at all display tiers, weight 400 only — research-paper voice
- Narrow editorial body column (~640px) — reads as essay, not landing page
- Red-clay accent kept to inline links and the radial spike — never a CTA fill
- Square buttons (0px or 4px radius) — refuses the AI-category pill geometry

## What they DON'T do
- No hero illustrations, no hero photography, no hero gradient — the headline IS the hero
- No saturated brand colors — clay is the only accent and it is muted
- No Tiempos at weight 700
- No autoplay video, no parallax, no scroll-jacking
- No emoji
- No urgency / scarcity marketing

## Exemplar pages
- https://anthropic.com/
- https://anthropic.com/research
- https://anthropic.com/news
- https://anthropic.com/company

## When to reference
Reach for Anthropic when the user wants a research-publisher voice — long-form essays, policy briefs, technical disclosures, careers-as-content, lab-and-product company sites. The brand is appropriate for any technology brand that wants to feel earnest, literary, and considered rather than salesy. Pairs well as the corporate-parent surface above a brighter product brand (the same way Anthropic itself sits above Claude).
