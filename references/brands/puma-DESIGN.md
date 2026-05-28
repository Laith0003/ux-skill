# Design System Inspired by Puma

## 1. Visual Theme & Atmosphere

Puma's web presence is sport-and-culture chrome — the leaping cat logo, bright-energy chromatic identity, and a layout grammar that puts athlete-and-celebrity collaborations as the hero. The atmosphere is youth-energy more than premium-restraint. Where Nike plays "premium athletic" and Adidas plays "Germany-precision sportswear," Puma plays "faster, looser, more culture-forward." The brand has long leaned into entertainment-celebrity-as-athlete (Rihanna's Fenty Puma, Selena Gomez, Neymar, Antoine Griezmann), and the web chrome makes those collabs the hero.

The leaping cat logo is the brand mark — used pure black on white or pure white on black, never colored. The wordmark sometimes pairs with the cat (the cat sits beside the PUMA letterforms); sometimes the cat appears alone. Both treatments are brand-correct.

Puma Red (#e21e26) — the brand's "Forever Faster" red — is the seasonal voltage. It appears on campaign banners, on certain product CTAs, and as a signature accent on athletic product pages. The red is generous on campaign moments (a full-bleed red banner heralding a new drop) and scarce on individual elements.

**Key Characteristics:**
- Leaping cat logo — the brand mark, pure black or pure white
- "Forever Faster" Puma Red (#e21e26) — seasonal chromatic voltage
- Athlete-and-celebrity collaboration heroes
- Wide black-on-white chrome with bright campaign-driven accents
- Rectilinear product cards (0–8px radius)
- Kinetic motion vocabulary — quick carousel cuts, hover lift on cards

## 2. Color Palette & Roles

### Primary
- **Pure Black** (`#000000`): The CTA fill, the wordmark, the cat logo
- **Pure White** (`#ffffff`): The canvas, the inverted wordmark on dark
- **Puma Red** (`#e21e26`): "Forever Faster" seasonal voltage

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f5f5f5`): Alternating section bands
- **Hairline** (`#e0e0e0`): 1px borders

### Neutrals & Text
- **Ink** (`#000000`): Primary text
- **Body** (`#1d1d1d`): Default body text
- **Muted** (`#6e6e6e`): Captions
- **Muted Soft** (`#a8a8a8`): Fine-print

### Campaign Accents (rotate by collab)
- Fenty Puma collaborations tend toward soft pinks (`#f8c0d0`) and creams
- Athlete collabs lean toward team-specific palette accents
- Velocity drops use Puma Red `#e21e26` heavily

### Semantic
- **Success** (`#2e7d32`): Green
- **Warning** (`#d4a017`): Amber
- **Error** (`#e21e26`): Puma Red doubles as error

## 3. Typography Rules

### Font Family
- **Display + Body**: `Puma Sans, Helvetica Neue, Arial, sans-serif` — modern geometric sans (open-source substitute: `Inter` or `Söhne`)

### Hierarchy
- **Hero h1** — 56–80px Puma Sans weight 800, line-height 1.05, often uppercase
- **Section h2** — 32–48px weight 700
- **Product title** — 14–16px weight 600, uppercase tracking +0.5px
- **Body** — 14–16px weight 400, line-height 1.5
- **Caption** — 12px weight 400
- **Button label** — 14–16px weight 700, uppercase, 1.5px tracking

### Principles
- Weight 800 for hero h1 — kinetic display
- Uppercase tracking on CTAs and product titles
- Tabular numerals on prices

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440px. Section padding is 64–96px vertical. Product card grids run 4-up at desktop, 2-up at mobile.

## 5. Componentry Feel

- **Primary CTA (black rect)** — Pure black fill, white text, 0–4px radius, 44–48px height, weight-700 uppercase label
- **Secondary CTA** — Transparent fill, 2px black border, black text
- **Campaign hero photo** — Full-bleed athlete or celebrity photo with the season name in heavy display sans overlaid, often featuring Puma Red as the typography color or accent
- **Athlete collab card** — Featured athlete photo + name + collection name — used on collaboration product family pages
- **Product card (rectilinear)** — White surface, no border, 0–8px radius, product image on white or contextualized lifestyle backdrop, name + price below
- **Carousel hard cut** — Hero carousels cut hard at 3-second intervals (no slow cross-fade) — kinetic rhythm

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use kinetic athletic-streetwear language ("Forever Faster", "Run with the cat"). Reference collaboration partners by name. Use uppercase for CTAs ("SHOP", "ADD TO BAG"). Lead with the speed or the cultural moment.

**Don't.** Don't use considered-prestige softness. Don't sanitize collaboration personality (Rihanna's Fenty Puma has a different tone than Neymar's collection). Don't translate "PUMA" or the leaping cat.

## 7. Motion Vocabulary

Kinetic motion. Hero carousels with quick 3-second cuts. Slight ken-burns pans on still imagery (~5 seconds per pan). Hover lift on product cards (1.03 scale + 150ms ease). The leaping cat occasionally jumps on idle in mascot animations on certain promotional pages. The motion budget is kinetic-controlled — faster than Adidas, never bouncy.

## 8. Anti-patterns to Avoid

- **Don't replace the leaping cat with a stylized icon.** It is the brand mark
- **Don't sanitize collaboration photography.** The celebrity-as-athlete moments are the brand
- **Don't soften card radii above 8px.** Sportswear precision
- **Don't tint Puma Red to coral.** The saturated red is the seasonal voltage
- **Don't drop the uppercase tracking on CTAs.** It is brand convention
- **Don't add a saturated tech-blue accent to the chrome.** Black-on-white with campaign reds
- **Don't slow the carousel cuts below 3 seconds.** The kinetic rhythm is the brand
