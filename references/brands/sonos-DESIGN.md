# Design System Inspired by Sonos

## 1. Visual Theme & Atmosphere

Sonos's web presence is premium-home-audio editorial — black-and-white product photography on white seamless, generous lifestyle imagery in muted Scandi-modern interiors, and a clean chrome with a single near-pure-black CTA. The atmosphere is design-magazine considered. Where Bose stays purely product-on-white and JBL leans bright-lifestyle-colorful, Sonos splits the difference: product imagery is studio-clean, lifestyle imagery is styled-room — a Sonos Era 300 on a walnut sideboard in a sunlit minimalist living room, a Sonos Arc beneath a wall-mounted television in a styled space, a Sonos Roam on a kitchen counter beside a ceramic vase.

The lifestyle photography is where Sonos differentiates from peers. The interiors are deliberately Scandi-modern: walnut, oak, white walls, indoor plants, ceramic objects, natural light. The styling reads as Architectural Digest more than Best Buy. The speakers are objects of design intent placed in spaces that aspire to taste. This is the brand selling itself to customers who value the look of audio gear as much as the sound.

The chrome around the photography stays restrained. Headlines are set in Saans (the brand's geometric humanist sans) at modest sizes. CTAs are pure-black rectangles or pills. Cards are rectilinear (0–8px radius). The chrome's job is to recede.

**Key Characteristics:**
- Pure white canvas with premium product-on-white and styled-room lifestyle photography
- Saans typography — modern geometric sans with humanist warmth
- Pure black CTA (#000000) — minimalist primary action
- Rectilinear cards (0–8px radius)
- Scandi-modern interior lifestyle imagery in muted earth tones
- Color-swatch picker on speaker product pages (white / black / soft / shadow palette)
- Room-by-room product recommender as a brand IA pattern

## 2. Color Palette & Roles

### Primary
- **Pure Black** (`#000000`): The CTA fill and the wordmark
- **Pure White** (`#ffffff`): The canvas anchor

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f7f7f5`): Alternating section bands — slight warmth
- **Surface Card** (`#fafaf8`): Hover state
- **Hairline** (`#dedede`): 1px borders

### Neutrals & Text
- **Ink** (`#000000`): Primary text
- **Body** (`#2a2a2a`): Default body text
- **Muted** (`#6b6b6b`): Captions
- **Muted Soft** (`#9d9d9d`): Fine-print

### Product Color Swatches (speakers come in)
- **Bright White** (`#fafafa`): White speaker finish
- **Shadow Black** (`#0e0e0e`): Black speaker finish
- **Soft White** (`#e0ddd5`): Off-white limited edition
- **Sunset Coral** (`#c87b6a`): Limited edition warm coral
- **Wave Blue** (`#3d5a7d`): Limited edition muted blue

### Semantic
- **Success** (`#2e7d32`): Green confirmation
- **Warning** (`#d4a017`): Amber
- **Error** (`#c62828`): Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `Saans` (proprietary) or `Inter` / `Söhne` as substitute — geometric humanist sans

### Hierarchy
- **Hero h1** — 48–64px Saans weight 500, line-height 1.1
- **Section h2** — 32–40px weight 500
- **Card title** — 20–24px weight 500
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 13–14px weight 400
- **Button label** — 14–16px weight 500

### Principles
- Weight 500 is the workhorse — the brand commits to medium weight, never bold
- Display headlines lean on generous size, not heavy weight
- Body sits at 16–18px for editorial reading pace
- Tracking neutral (0)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 96–120px vertical — generous to give the lifestyle photography room. Product card grids run 3-up at desktop.

## 5. Componentry Feel

- **Lifestyle photo hero** — Full-bleed styled-room photograph with the brand wordmark + headline overlaid in white or black depending on photo tone
- **Primary CTA (dark rect)** — Pure black fill, white text, 0–4px radius, 48px height, weight-500 label
- **Color swatch picker** — Horizontal row of round color swatches on speaker product pages, active swatch shows a thin ring outline
- **Product detail stacked** — Long-scroll product page with hero (product on white), spec callouts, lifestyle photography mid-page, technical details
- **Room-by-room recommender** — Quiz-style flow ("How big is the room? How do you listen?") returning recommended Sonos configurations
- **Footer** — Minimal soft surface footer, multi-column site-map, region switcher

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use considered lifestyle-language ("Built for the way you listen at home"). Reference room contexts (living room, kitchen, bedroom). Treat product names as proper nouns (Era 300, Sub, Arc, Beam, Roam). Lead with the listening moment.

**Don't.** Don't write tech-spec-first copy in the chrome (specs come on the product detail page). Don't use exclamation points. Don't add aspirational lifestyle vagueness ("Transform your home" reads off-brand).

## 7. Motion Vocabulary

Editorial fade-in reveals on scroll (250ms ease-out). Carousel cross-fade at 1.2–1.5s — deliberately slow. Hover lifts on product cards are minimal — a slight 100ms opacity dip on the price line. The motion philosophy matches the prestige restraint.

## 8. Anti-patterns to Avoid

- **Don't add bright brand-accent colors.** Sonos is monochrome chrome on muted lifestyle
- **Don't sharpen lifestyle photography into clinical product shots.** The styled-room context is the brand
- **Don't soften card radii above 8px**
- **Don't add scroll-driven motion that competes with the lifestyle photography**
- **Don't replace Saans with a heavy display sans.** The medium-weight humanist proportions are part of the brand
- **Don't use a saturated CTA color.** Pure black is the brand
- **Don't crop product photography tightly without context.** The generous white space and lifestyle context are signatures
