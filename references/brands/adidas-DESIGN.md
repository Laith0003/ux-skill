# Design System Inspired by Adidas

## 1. Visual Theme & Atmosphere

Adidas's web presence is sports-and-streetwear editorial — the three-stripes wordmark holds the page, the chrome is unapologetically black-on-white, athletic-action photography blends with high-fashion lookbook crops, and a single chromatic accent (the season's signature color: lime, electric blue, solar red) appears scarcely. The atmosphere is performance-meets-runway. Track athletes shot under stadium lighting and street-style models shot in deconstructed urban contexts share the same chrome — that consistency is the brand telling you "we're both performance and culture."

The three-stripes wordmark is the brand mark, used pure black on white. The brand's Performance and Originals sub-brands have distinct visual treatments — Performance leans more athletic-action and white-heavy; Originals leans more lookbook-editorial and color-rich — but both live in the same chrome system. The wordmark is invariant.

The typography is Adihaus DIN — the proprietary modern industrial sans, descendant of the German DIN standard and shaped to read as athletic-precision. The letterforms are tighter and more rectilinear than Helvetica; they carry a precision-engineered feel that matches the sportswear positioning. The brand commits to Adihaus across display through body; replacing with Inter or Helvetica flattens the German-industrial feel.

**Key Characteristics:**
- Three-stripes wordmark — pure black on white
- Adihaus DIN typography — modern industrial sans across chrome
- Black-on-white chrome with single-season chromatic accent
- Rectilinear product cards (0–4px radius) — sportswear precision
- Athletic-action photography blended with lookbook editorial crops
- Performance and Originals as sub-brands sharing the master chrome
- Athlete-roster cards on collaboration product pages

## 2. Color Palette & Roles

### Primary
- **Pure Black** (`#000000`): The CTA fill and the wordmark
- **Pure White** (`#ffffff`): The canvas

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f4f4f4`): Alternating section bands
- **Surface Card** (`#fafafa`): Hover state
- **Hairline** (`#dedede`): 1px borders

### Neutrals & Text
- **Ink** (`#000000`): Primary text
- **Body** (`#1d1d1d`): Default body text
- **Muted** (`#767677`): Captions
- **Muted Soft** (`#a8a8a8`): Fine-print

### Season Accents (rotate by collection)
- **Lime** (`#c0ff00`): Spring/summer signature
- **Electric Blue** (`#0066ff`): Stadium accent
- **Solar Red** (`#ff3030`): Heritage colorway
- **Sunset Orange** (`#ff5733`): Limited drop

### Semantic
- **Success** (`#2e7d32`): Green confirmation
- **Warning** (`#d4a017`): Amber
- **Error** (`#c62828`): Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `Adihaus DIN, DIN Next, Helvetica Neue, sans-serif` — proprietary modern industrial sans (open-source substitute: `Inter` with tightened tracking)

### Hierarchy
- **Hero h1** — 56–80px Adihaus DIN weight 800, line-height 1.05, often uppercase
- **Section h2** — 36–48px weight 700, optional uppercase
- **Product title** — 16–18px weight 600, uppercase tracking +1px
- **Body** — 14–16px weight 400, line-height 1.5
- **Caption** — 12–13px weight 400
- **Button label** — 14–16px weight 700, uppercase with 1.5px tracking

### Principles
- Weight 800 for hero h1 — heavy industrial display
- Uppercase tracking on CTAs and product titles — sportswear convention
- Tabular numerals on prices and sport stat readouts

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440–1600px. Section padding is 64–96px vertical. Product card grids run 4-up at desktop, 2-up at mobile (the dense 2-up mobile is a sportswear-e-commerce convention).

## 5. Componentry Feel

- **Primary CTA (black rect)** — Pure black fill, white text, 0–4px radius, 48px height, weight-700 uppercase label, 1.5px tracking
- **Secondary CTA** — Transparent fill, 2px black border, black text, same dimensions
- **Product card (rectilinear)** — White surface, no border, 0–4px radius, product image on white, name (uppercase tracked) + price below
- **Lookbook editorial hero** — Full-bleed editorial photograph (athletic-action or street-style) with the season name in heavy display sans overlaid
- **Three-stripes pattern band** — Decorative band using the three-stripes motif as a section divider
- **Athlete roster card** — Featured athlete photo + name + sport — used on collaboration product pages (Beckham, Messi, Anthony Edwards)

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use direct athletic-streetwear language ("Lighter. Faster. Stronger."). Reference sport-specific contexts. Use uppercase for CTAs ("SHOP NOW", "ADD TO BAG"). Lead with the performance benefit or the cultural moment.

**Don't.** Don't use considered-prestige softness (that's Aesop / Aman territory). Don't sanitize the athletic intensity. Don't translate "Three Stripes" — the wordmark stays.

## 7. Motion Vocabulary

Athletic-grade motion. Hero carousels with hard cuts at ~4-second intervals (no slow cross-fades). Scroll-triggered headline reveals with a slight directional translate (50–80px). Hover on product cards triggers an alternate angle crossfade (200ms). The motion budget is kinetic-controlled — never bouncy, never overshooting.

## 8. Anti-patterns to Avoid

- **Don't introduce ornate brand-blue accents.** Adidas chrome is black-on-white with season accents
- **Don't soften card radii above 4px.** Sportswear precision
- **Don't replace Adihaus DIN with Helvetica or Inter.** Modern industrial proportions are signature
- **Don't stylize action photography with color filters.** Natural lighting is the brand
- **Don't drop the uppercase tracking on CTAs and product titles.** It is brand convention
- **Don't make the three-stripes wordmark colored.** It stays pure black on white
- **Don't pair the chrome with a saturated tech-blue accent.** Season accents rotate; the chrome stays monochrome
