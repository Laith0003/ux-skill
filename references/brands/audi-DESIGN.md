# Design System Inspired by Audi

## 1. Visual Theme & Atmosphere

Audi's web presence is German-engineering luxury — the Four Rings logo, a near-monochrome chrome with pure-white canvas and dark gray ink, and cinematic vehicle photography in muted automotive-grade lighting. The atmosphere is precision-luxury. Every CTA, every section break, every photograph reads as "designed by engineers, finished by designers." Where Mercedes-Benz plays "classical luxury heritage" and BMW plays "ultimate driving machine kinetic," Audi plays "Vorsprung durch Technik" — progress through technology — and the chrome follows that positioning.

The Four Rings logo is the brand mark, used pure black on white or pure white on black. It is one of the most-recognized automotive marks in the world, and the chrome treats it with reverence — the rings appear at the top-left of every page in modest size, never animated, never tinted. The wordmark "AUDI" sometimes accompanies the rings but more often the rings stand alone.

Audi Type — the proprietary humanist sans — runs display through body. Its slightly wider proportions and rounded terminals give the chrome a precision-engineered feel that matches the brand. The display variant has a heavier optical mastering for hero headlines; the body variant has tighter spacing for legibility at small sizes.

**Key Characteristics:**
- Four Rings logo as brand mark — pure black or white, never tinted
- Audi Type — proprietary humanist sans across chrome
- Pure white canvas with dark gray ink — engineered precision
- Audi Red (#bb0a30) — scarce CTA accent, heritage racing red
- Cinematic vehicle photography in automotive-grade lighting
- Configurator-style product pages with exterior color, interior trim, wheel selection
- Rectilinear cards (0–8px radius)

## 2. Color Palette & Roles

### Primary
- **Audi Red** (`#bb0a30`): The brand's racing heritage red — used scarcely on primary CTAs
- **Pure Black** (`#000000`): The wordmark and ink color
- **Pure White** (`#ffffff`): The canvas

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f4f4f4`): Alternating section bands
- **Surface Dark** (`#1a1a1a`): Dark sections (model showcases, configurator)
- **Hairline** (`#dadada`): 1px borders

### Neutrals & Text
- **Ink** (`#000000`): Primary text
- **Body** (`#1f1f1f`): Default body text
- **Muted** (`#6e6e6e`): Captions
- **Muted Soft** (`#999999`): Fine-print

### Semantic
- **Success** (`#2e7d32`): Green
- **Warning** (`#d4a017`): Amber
- **Error** (`#bb0a30`): Audi Red doubles as error

## 3. Typography Rules

### Font Family
- **Display + Body**: `Audi Type, Helvetica Neue, Arial, sans-serif` — proprietary humanist sans (open-source substitute: `Inter` with slightly wider tracking)

### Hierarchy
- **Hero h1** — 48–72px Audi Type weight 700, line-height 1.1
- **Section h2** — 32–48px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 13–14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for hero h1 — heavy editorial display
- Audi Type's slightly wider proportions are signature
- Body sits at 16–18px for considered reading
- Tabular numerals on vehicle specs (horsepower, range, MPG)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440–1600px. Section padding is 96–120px vertical. Vehicle hero sections use a full-bleed photograph with the model name overlaid in heavy display sans.

## 5. Componentry Feel

- **Vehicle hero photography** — Full-bleed cinematic photo of the car in motion or at rest in styled location, model name overlaid in Audi Type display weight 700
- **Configurator color picker** — Horizontal row of color swatches for exterior paint; clicking changes the vehicle render in real-time with a 200ms crossfade
- **Primary CTA (red rect)** — Audi Red fill, white text, 0–4px radius, 48px height, weight-600 label
- **Secondary CTA** — Transparent fill, 2px black border, black text
- **Model comparison row** — Horizontal row of vehicle thumbnails with name, starting price, primary spec (horsepower, range)
- **Footer (multi-column dark)** — Dark surface footer with white links, multi-column site-map, country/region switcher

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use precision-engineering language ("Vorsprung durch Technik", "Progress through technology"). Quantify vehicle specs precisely. Reference engineering achievement.

**Don't.** Don't write consumer-aspirational softness. Don't use exclamation points. Don't anthropomorphize the vehicle.

## 7. Motion Vocabulary

Cinematic editorial fade-ins (300ms ease-out). Hero photography uses slow ken-burns pans (8-second cycles). Configurator color changes use a hard 200ms crossfade rather than spring transitions. The brand reads as engineered-precision.

## 8. Anti-patterns to Avoid

- **Don't replace Audi Type with Helvetica or Inter.** The German-precision humanist proportions are signature
- **Don't add saturated brand-blue accents.** Audi chrome is monochrome + red
- **Don't sanitize the cinematic photography.** Automotive-grade lighting is the brand
- **Don't soften card radii above 8px.** German precision
- **Don't paint the chrome in any color other than monochrome.** The Audi Red is scarce on CTAs only
- **Don't animate the Four Rings logo.** It stays static
- **Don't drop the configurator chrome on vehicle pages.** It is brand IA
