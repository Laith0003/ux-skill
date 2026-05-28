# Design System Inspired by Bentley

## 1. Visual Theme & Atmosphere

Bentley's web presence is British luxury automotive — the winged 'B' wordmark, a near-monochrome dark chrome with a deep racing-green secondary accent, and editorial photography that treats the vehicle as a coachbuilt artifact rather than a transportation product. The atmosphere is heritage-bespoke. Every page references handcrafted leather, marquetry, polished wood veneers, and 100+ years of British coachbuilding. Where McLaren plays "F1 engineering precision" and Rolls-Royce plays "ultimate prestige formality," Bentley plays "British coachbuilt heritage with continental grand-touring soul."

The signature visual decision is the artisan-detail photography. Hero pages don't just show the car — they intercut close-ups of leather grain, hand-stitched seams, marquetry diamond patterns, wood veneer joinery, and polished chrome detailing. The chrome treats every artisan craft moment as worthy of the same reverence as the vehicle itself. The brand is selling craftsmanship, and the photography proves the craftsmanship.

The winged 'B' wordmark is the brand mark, often rendered in gold leaf or polished chrome on hero treatments. The wordmark carries the weight of a luxury heritage badge — never animated, never flat-colored, always rendered with the polished-metal sheen that references the physical badge on the car's grille.

**Key Characteristics:**
- Winged 'B' wordmark — rendered in gold leaf or polished chrome
- Bentley Racing Green (#093624) — deep racing-heritage secondary
- Dark cinematic canvas (#0e0e0e) with editorial coachbuilding photography
- Artisan-detail photography — leather grain, marquetry, wood veneer close-ups
- Bespoke material picker on configurator pages
- Rectilinear cards (0–8px radius) — heritage precision
- Bentley Sans — proprietary modern sans with heritage proportions

## 2. Color Palette & Roles

### Primary
- **Bentley Racing Green** (`#093624`): The brand's deep heritage green — secondary accent and select CTA fills
- **Polished Gold** (`#c8a35c`): The wordmark gold-leaf rendering
- **Pure White** (`#ffffff`): The primary text on dark
- **Pure Black** (`#0e0e0e`): The canvas anchor

### Surface & Background
- **Dark Canvas** (`#0e0e0e`): Page background
- **Surface 1** (`#1a1a1a`): Card backgrounds
- **Surface 2** (`#252525`): Hover state, elevated panels
- **Hairline Dark** (`#2e2e2e`): 1px borders

### Light-mode (account, support, configurator)
- **Light Canvas** (`#ffffff`)
- **Light Surface** (`#f7f5f0`): Warm cream-tinted alternate

### Neutrals & Text (on dark)
- **Ink** (`#ffffff`): Primary text
- **Body** (`#dedede`): Default body text
- **Muted** (`#9d9d9d`): Captions
- **Muted Soft** (`#6e6e6e`): Fine-print

### Bespoke Material Swatches (configurator)
- **Leather Browns** — Saddle `#7a4f2e`, Beluga Black `#1a1a1a`, Linen `#d8c5a8`
- **Wood Veneers** — Burr Walnut, Piano Black, Dark Stain
- **Embroidery Threads** — multiple bespoke options

### Semantic
- **Success** (`#3fb95e`): Green status
- **Warning** (`#d4a017`): Amber
- **Error** (`#c83d3d`): Red error

## 3. Typography Rules

### Font Family
- **Display + Body**: `Bentley Sans, Helvetica Neue, Arial, sans-serif` — proprietary modern sans with heritage proportions

### Hierarchy
- **Hero h1** — 48–72px Bentley Sans weight 500, line-height 1.1
- **Section h2** — 32–48px weight 500
- **Card title** — 20–24px weight 500
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 500, often uppercase with tight tracking

### Principles
- Weight 500 is the workhorse — the brand commits to medium weight, never bold
- Display headlines lean on generous size and considered tracking, not heavy weight
- Body sits at 16–18px for editorial reading pace

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 96–120px vertical — generous to give the editorial photography room. Vehicle hero sections use full-bleed cinematic photography.

## 5. Componentry Feel

- **Coachbuilt hero photography** — Full-bleed cinematic photo of the car in a heritage location (English countryside, Mediterranean coast, Mayfair street) with the model name overlaid
- **Bespoke material picker** — Interactive picker for leather color, wood veneer, embroidery thread on configurator pages
- **Primary CTA (green rect)** — Racing Green fill, white text, 0–4px radius, 48px height, weight-500 label
- **Marquetry detail card** — Close-up photography of an artisan craft moment (stitched seam, diamond marquetry, polished chrome detail) with a short explanatory paragraph
- **Heritage narrative band** — Long-scroll section telling Bentley brand story (founded 1919, racing heritage, modern grand touring)

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use British heritage luxury language ("Crafted in Crewe", "Hand-stitched, hand-marquetried"). Reference craft heritage. Treat models as proper nouns (Continental GT, Mulsanne, Flying Spur).

**Don't.** Don't write performance-machine copy. Don't use exclamation points. Don't sanitize the craft-detail focus.

## 7. Motion Vocabulary

Editorial cinematic motion. Slow ken-burns pans on hero photography (10-second cycles). Considered fade-ins on scroll (400ms ease-out). Configurator changes use a soft 300ms crossfade with the wheel rim slowly rotating between selections. The motion budget matches the heritage prestige positioning.

## 8. Anti-patterns to Avoid

- **Don't sanitize the coachbuilding photography.** The artisan detail shots are the brand
- **Don't replace Bentley Racing Green with a brighter forest.** The specific deep green is heritage
- **Don't soften card radii above 8px.** Heritage precision
- **Don't strip the winged 'B' wordmark of its gold-leaf rendering on hero treatments.** The polished-metal sheen is brand
- **Don't pair the chrome with a saturated tech-blue accent.** The cream/green/gold tonal palette is brand
- **Don't add kinetic motion.** Bentley reads as considered, never kinetic
- **Don't drop the bespoke material picker on configurator pages.** It is brand IA
