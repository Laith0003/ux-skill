# Design System Inspired by Bose

## 1. Visual Theme & Atmosphere

Bose's web presence is the premium-audio brand's editorial chrome — black-and-white duotone product photography on a clean white canvas, restrained typography, and a single near-black CTA color. The atmosphere is hi-fi audio reverence. Where consumer-electronics peers (Sony, JBL, Beats) lean into bright color and lifestyle photography, Bose leans into the engineering: the QuietComfort headphones photographed against pure white, the SoundLink Revolve+ speaker rendered in monochromatic gradients, the soundbar in a styled-but-minimal living room with the brand wordmark holding the page.

The product photography is the system's primary atmospheric asset. Headphones, speakers, and soundbars are shot on pure-white seamless or on muted-tone neutral backgrounds, often in subtle high-key lighting that emphasizes the product's geometry rather than its lifestyle. The photography reads as "studio product shot for an audio engineering catalog" rather than "consumer marketing." The restraint is the prestige signal.

Typography is unfussy. Helvetica Neue (or close substitute) carries everything — display through body — at modest sizes. No proprietary face, no custom display, no editorial drop caps. The brand commits to neutrality. The signal is "the audio is the brand, the chrome stays out of the way."

**Key Characteristics:**
- Pure white canvas with premium black-and-white product photography
- Helvetica Neue across chrome — neutral, unobtrusive
- Rectilinear cards (0–8px radius) — hi-fi precision over consumer softness
- Single dark CTA color (#1f1f1f) — minimalist primary action
- Editorial product detail pages — long-scroll specs and audio-engineering callouts
- No bright accent colors — the chrome stays monochrome

## 2. Color Palette & Roles

### Primary
- **Bose Black** (`#1c1c1c`): The dark CTA fill and the ink color — a near-black with a slight warm undertone
- **Pure White** (`#ffffff`): The canvas anchor
- **Disabled** (`#a3a3a3`): Disabled button state

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f6f6f6`): Alternating section bands
- **Surface Card** (`#fafafa`): Hover state on cards
- **Hairline** (`#e0e0e0`): 1px borders

### Neutrals & Text
- **Ink** (`#1c1c1c`): Primary text
- **Body** (`#3d3d3d`): Default body text
- **Muted** (`#727272`): Captions
- **Muted Soft** (`#9d9d9d`): Fine-print

### Semantic
- **Success** (`#2e7d32`): Green confirmation
- **Warning** (`#d4a017`): Amber caution
- **Error** (`#c62828`): Red error

## 3. Typography Rules

### Font Family
- **Display + Body**: `Helvetica Neue, Helvetica, Arial, sans-serif`. No proprietary face

### Hierarchy
- **Hero h1** — 40–56px Helvetica Neue weight 600, line-height 1.15
- **Section h2** — 28–36px weight 600
- **Card title** — 18–22px weight 600
- **Body** — 16px weight 400, line-height 1.5
- **Caption** — 13–14px weight 400
- **Button label** — 14–16px weight 500

### Principles
- Weight 600 is the workhorse — never 700 or 800. The restraint is part of the prestige
- Body sits at 16px, tight to standard. No editorial 17–18px
- Tracking neutral (0)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Product card grids run 3-up or 4-up at desktop. Product detail pages use a 6-6 split with the product image on the left and specs on the right.

## 5. Componentry Feel

- **Primary CTA (dark)** — Bose Black fill, white text, 4px radius (or 0), 44px height, weight-500 label
- **Secondary CTA** — Transparent fill, 1px Bose Black border, dark text, same dimensions
- **Product card (rectilinear)** — White surface, 1px hairline border, 4–8px radius, internal padding 24px. Product image on white, name, price, "Learn more" link
- **Spec callout grid** — On product detail pages, 2-up or 3-up grid of small technical callouts (driver size, frequency response, weight)
- **Product detail hero** — Full-bleed product photo on white with the product name in 40–56px sans below
- **Audio tech explainer band** — Long-scroll section with paragraph explanations of acoustic engineering (Active Noise Cancellation, Voice4Video) accompanied by a simple line diagram

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use precise engineering language ("Active Noise Cancellation across 16 levels", "9-hour battery"). Lead with the technical specification, not the lifestyle promise. Treat product names as proper nouns (QuietComfort, SoundLink).

**Don't.** Don't write aspirational marketing copy. Don't use exclamation points. Don't add lifestyle taglines that aren't grounded in product capability. Don't anthropomorphize the audio ("immersive escape into your music" reads off-brand).

## 7. Motion Vocabulary

Editorial fade-ins on scroll (200ms ease). Slow crossfade carousels (1.2s). No spring, no scale, no bouncy interactions. Hover on product cards triggers a subtle background shift to #fafafa but no lift. The motion is restrained to match the prestige positioning.

## 8. Anti-patterns to Avoid

- **Don't add bright accent colors.** The brand is monochrome with dark CTAs
- **Don't soften card radii above 8px.** Bose reads as hi-fi precision, not soft consumer
- **Don't stylize product photography with color filters.** Pure-white seamless is the brand
- **Don't add motion to product cards.** Editorial restraint is the prestige signal
- **Don't use weight 700 for headlines.** Weight 600 is the brand standard
- **Don't crop product photography tightly.** Generous white space around the product is the brand
- **Don't pair Bose chrome with a chromatic CTA color.** Dark CTAs only
