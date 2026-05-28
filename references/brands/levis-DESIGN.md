# Design System Inspired by Levi's

## 1. Visual Theme & Atmosphere

Levi's web presence is American-heritage denim chrome — the red tab as the chromatic anchor, monochrome editorial photography (often black-and-white denim shots), and a layout grammar that treats every jeans-fit page as a fit guide with measurements rather than a fashion lookbook. The atmosphere is workwear-heritage modern. The 501 is a heritage product with a 150-year history, and the chrome respects that lineage without being a costume.

Where contemporary fashion peers (Zara, H&M, ASOS) lean editorial-aspirational, Levi's leans documentary-honest. Photography is often black-and-white or muted-color, with models photographed against rough textured backdrops (raw plaster, concrete, weathered wood) that reference the brand's workwear origins. The styling is everyday — the photography says "this is what these jeans look like on real people in real settings" rather than "this is what these jeans look like on a runway."

The red tab — a small fabric tag stitched to the back pocket of every pair — is the brand mark. It appears in the chrome as a small graphic accent (a red rectangular tab with "LEVI'S" in white), used as a navigational anchor or as a section divider. The red tab is one of the most-recognized brand marks in apparel, and the chrome treats it as a small signature rather than as a chromatic explosion.

**Key Characteristics:**
- Pure white canvas with monochrome editorial denim photography
- Levi's red tab — chromatic anchor as small graphic accent
- Heritage serif for display + clean sans for body
- Workwear-honest photography against textured backdrops
- 501-specific fit guide chrome on heritage product pages
- Rectilinear product cards (0–4px radius)
- Levi's red (#cc1f3a) — scarce on individual elements, generous on brand-mark presence

## 2. Color Palette & Roles

### Primary
- **Levi's Red** (`#cc1f3a`): The red-tab accent and the primary CTA fill — a specific brick-red, not pure red, not coral
- **Pure Black** (`#1a1a1a`): The ink color
- **Pure White** (`#ffffff`): The canvas

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f7f5f0`): Slightly warm alternating sections — heritage-paper feel
- **Surface Card** (`#fafafa`): Hover state
- **Hairline** (`#e0e0e0`): 1px borders

### Neutrals & Text
- **Ink** (`#1a1a1a`): Primary text
- **Body** (`#3a3a3a`): Default body text
- **Muted** (`#6f6f6f`): Captions
- **Muted Soft** (`#a3a3a3`): Fine-print

### Denim Wash Swatches (product picker)
- **Rinse Wash** (`#1c2638`): Dark indigo
- **Medium Wash** (`#3a5573`): Mid-blue
- **Light Wash** (`#7993ad`): Light denim blue
- **Black Wash** (`#161616`): Black denim
- **White Wash** (`#e8e7e0`): Cream / ecru

### Semantic
- **Success** (`#2e7d32`): Green
- **Warning** (`#d4a017`): Amber
- **Error** (`#cc1f3a`): Levi's Red doubles as error

## 3. Typography Rules

### Font Family
- **Display**: `Levi's Heritage Serif` (proprietary) or `Playfair Display` / `Cormorant Garamond` as substitute — for hero headlines
- **Body**: `Levi's Sans, Helvetica Neue, Arial, sans-serif` — clean modern sans

### Hierarchy
- **Hero h1** — 48–72px Heritage Serif weight 600, line-height 1.1
- **Section h2** — 32–40px serif weight 500
- **Product title** — 16–18px Levi's Sans weight 600
- **Body** — 16px sans weight 400, line-height 1.5
- **Caption** — 13–14px sans weight 400
- **Button label** — 14–16px sans weight 600, often uppercase

### Principles
- Serif display + sans body — the split signals "heritage modern"
- Weight 600 for serif headlines (never 700+) — restrained editorial weight
- Tabular numerals on prices and inseam measurements
- Italic appears in inline emphasis only

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 96–120px vertical. Product card grids run 3-up or 4-up at desktop. Fit guide pages use a 7-5 split with the product render on the right and the fit information on the left.

## 5. Componentry Feel

- **Primary CTA (red rect)** — Levi's Red fill, white text, 0–4px radius, 44px height, weight-600 label
- **Fit guide stacked** — Long-scroll product page with fit information (rise, leg opening, inseam) presented as a measurement diagram, with model-on-fit photography
- **Product card (rectilinear)** — White surface, no border, 0–4px radius, product image, name + price below, denim wash swatch row
- **Red tab graphic accent** — Small red rectangular tab with "LEVI'S" in white, used as a navigational anchor or section divider
- **Heritage editorial band** — Long-scroll section telling the story of a Levi's product (501 history, fabric science) with black-and-white archival photography
- **Footer** — Soft warm surface, multi-column site-map

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use heritage-honest workwear language ("Originals since 1873", "The 501 jean"). Quantify product specs (inseam, rise, leg opening). Reference history and craft. Use sentence case for chrome.

**Don't.** Don't write fashion-aspirational copy ("Elevate your style"). Don't sanitize the workwear honesty. Don't translate "501" or product names — they are heritage IP.

## 7. Motion Vocabulary

Editorial slow motion. Hero carousels cross-fade at 4–5 seconds. Scroll-triggered fade-ins on heritage editorial bands (300ms ease-out). The brand commits to slow, considered motion that matches the heritage positioning.

## 8. Anti-patterns to Avoid

- **Don't replace heritage serif headlines with all-sans modern.** The serif is the heritage signal
- **Don't add bright fashion-brand chromatic accents.** The chrome is heritage-restrained
- **Don't sanitize the workwear-photography aesthetic.** Denim is the artifact
- **Don't lose the small red tab graphic.** It is the brand mark across the chrome
- **Don't tint Levi's Red to a "modern" pink or coral.** The specific brick-red is brand
- **Don't soften card radii above 4px.** Heritage workwear precision
- **Don't drop the fit-guide chrome on heritage product pages.** It is brand IA
