# The New York Times — DESIGN.md

## Overview
The canonical American newspaper online. The masthead serif (NYT Cheltenham) and the news-headline serif (NYT Imperial) carry every editorial moment; body runs in Imperial Text. The canvas is a paper-warm off-white (`#fffffe` with slight cream tint in real CSS — read as pure white at glance). The brand voltage is the masthead itself, set in display-size Cheltenham. Color is functional, never decorative — link blue, breaking-news red, byline gray.

## Color
- **Primary:** `#000000` — Newsprint Black (used for type)
- **Canvas:** `#ffffff` — Paper White (with subtle cream warmth)
- **Surface alt:** `#f7f7f5` — Off-White (used for opinion section, special-feature backgrounds)
- **Ink:** `#000000`
- **Body:** `#363636`
- **Hairlines:** `#dfdfdf` — newsprint divider gray
- **Link blue:** `#326891` — Times Link
- **Breaking-news red:** `#d0021b` — Times Red (used only on breaking-news banners and Live indicators)
- **Section accent (Opinion):** `#326891` (the same blue)
- **Section accent (Cooking):** `#236a51` — Recipe Green

## Typography
- **Masthead:** NYT Cheltenham, weight 700, tracking -0.01em, sizes up to 96px (masthead-only)
- **Display:** NYT Imperial / NYT Cheltenham (mixed), weight 500-700, tracking 0, sizes 36-72px headline
- **Body:** NYT Imperial Text, weight 400, 18px base, 1.55 line-height
- **Byline / kicker:** NYT Franklin Gothic, weight 500-700, 12-13px, tracking 0.4px caps
- **Eyebrow:** Franklin Gothic small caps with 1px tracking

## Spacing & rhythm
4-base (4/8/12/16/24/32/48/72). Newspaper-column rhythm — front page uses a heavy grid with 3-4 column sections at desktop. Hero headlines often span 2-3 columns; body wraps tight at 18px / 1.55.

## Motion signature
Almost none. 120ms ease-out hover on link hover (color shift). Breaking news ribbon at the top of homepage pulses subtly when live. The brand voice is "the news is the motion" — animation that draws attention is anti-brand.

## Components observed
- `masthead-cheltenham` (giant Cheltenham wordmark, centered, hairline below)
- `headline-imperial-bold` (Imperial weight 700 for above-the-fold news)
- `subhead-franklin-caps` (Franklin small caps eyebrow)
- `byline-block` (author name + role, hairline-separated)
- `breaking-news-ribbon-red` (full-width red ribbon, white type, pulsing)
- `section-front-grid` (multi-column newspaper grid)
- `recipe-card` (Cooking section — green accent, photo-led)
- `opinion-essay-card` (Opinion section — blue accent, byline-prominent)

## Trademark signals
- The Cheltenham masthead — the most recognized newspaper wordmark online
- Imperial body text at 18px — the brand's text size is the brand
- Franklin Gothic small caps for bylines and section labels — newspaper-page cadence
- Section-specific accent colors (recipe green, opinion blue) — color carries section identity, not decoration
- Hairline 1px dividers between every section/story — newspaper rule-line aesthetic

## What they DON'T do
- No emoji in news content
- No saturated rainbow gradients
- No animated illustrations in editorial articles (special-feature scrollytells are an exception, separately art-directed)
- No mascot characters
- No dark-mode hero on the homepage (article view supports dark mode separately)

## Exemplar pages
- https://www.nytimes.com/
- https://www.nytimes.com/section/opinion
- https://cooking.nytimes.com/
- https://www.nytimes.com/section/technology

## When to reference
Reach for The New York Times when the user needs the most editorially-rooted, newspaper-traditional surface possible. The Cheltenham-masthead + Imperial-body + hairline-grid combination is canonical newspaper typography online. Appropriate for any long-form publication, newsroom product, serious journalism brand, or product wanting to read with institutional gravity.
