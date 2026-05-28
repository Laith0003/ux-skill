# Design System Inspired by JBL

## 1. Visual Theme & Atmosphere

JBL's web presence is the high-energy youth-oriented audio brand — JBL Orange (#ff5500) as the chromatic voltage, a dark canvas (#0d0d0d) anchoring the chrome, and action-lifestyle photography (parties, outdoor adventures, gym workouts) carrying the atmosphere. Where Bose plays "premium studio quiet" and Sonos plays "considered home design," JBL plays "party speaker for the beach, gym headphones for the run, soundbar for the gaming setup." The brand is consumer audio at full volume.

JBL Orange is the chromatic voltage. The specific hex (#ff5500) is saturated and warm — not coral, not red, a true bright orange. It appears on CTAs, on the wordmark's exclamation accent (the "!" in JBL!), on the sound-wave ring animations on product pages, and as the primary action signal across the chrome. The orange is generous on the brand presence (the hero, the wordmark) and scarce on individual elements (a single primary CTA per viewport).

The signature interaction is the sound-wave ring animation. On speaker product pages, the speaker is centered and animated concentric rings emanate outward in JBL Orange, simulating the audio waves. The animation runs continuously as long as the user is on the page — it is the visual representation of the brand's product category.

**Key Characteristics:**
- JBL Orange (#ff5500) — chromatic voltage on CTAs, wordmark, sound-wave animations
- Dark canvas (#0d0d0d) — youth-energy backdrop
- Action-lifestyle photography — parties, gym, outdoor adventures
- Sound-wave ring animations on speaker product pages
- Pill-shaped (full-radius) CTAs in JBL Orange
- Auto-playing lifestyle video heroes (muted default, audio toggle)
- Card-based product grid with 8–16px radius on cards

## 2. Color Palette & Roles

### Primary
- **JBL Orange** (`#ff5500`): The chromatic voltage — CTAs, wordmark exclamation, sound-wave animations
- **Orange Hover** (`#cc4400`): Press state
- **Orange Glow** (`rgba(255, 85, 0, 0.4)`): The translucent orange used for sound-wave rings

### Surface & Background
- **Dark Canvas** (`#0d0d0d`): Page background
- **Surface 1** (`#1a1a1a`): Card backgrounds
- **Surface 2** (`#252525`): Hover state
- **Hairline Dark** (`#2e2e2e`): 1px borders

### Light-mode (account, support, checkout)
- **Light Canvas** (`#ffffff`)
- **Light Surface** (`#f6f6f6`)

### Neutrals & Text (on dark)
- **Ink** (`#ffffff`): Primary text on dark
- **Body** (`#dedede`): Default body text
- **Muted** (`#9d9d9d`): Captions
- **Muted Soft** (`#6e6e6e`): Fine-print

### Semantic
- **Success** (`#3fb95e`): Green status
- **Warning** (`#ffb84a`): Amber
- **Error** (`#ff4747`): Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `JBL Sans, Helvetica Neue, Arial, sans-serif` — modern geometric sans

### Hierarchy
- **Hero h1** — 56–80px JBL Sans weight 800, line-height 1.05
- **Section h2** — 36–48px weight 700
- **Card title** — 20–24px weight 700
- **Body** — 16px weight 400, line-height 1.5
- **Caption** — 13–14px weight 500
- **Button label** — 14–16px weight 700, often uppercase with tight tracking

### Principles
- Weight 800 for hero h1 — high-energy display
- CTA labels often uppercase with 1px tracking
- Tabular numerals on spec readouts (watts, hours, dB)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440px. Section padding is 80–120px vertical. Product card grids run 3-up or 4-up at desktop.

## 5. Componentry Feel

- **Lifestyle video hero** — Full-viewport auto-playing video of people using JBL products (beach party with portable speaker, gym workout with headphones), muted by default, audio toggle
- **Primary CTA (orange pill)** — JBL Orange fill, white text, full-pill radius, 44–48px height, weight-700 uppercase label
- **Speaker product card (dark)** — Dark surface, 8–16px radius, product image with subtle sound-wave ring animation on hover, title, price, "Shop now" link
- **Sound-wave ring animation** — Concentric JBL Orange rings emanating from a speaker product render, continuously animating as long as the page is visible
- **Action photography carousel** — Multi-image carousel showing lifestyle moments (party, gym, outdoor)
- **Product spec callout** — Battery hours, watts, IP rating callouts in 2–3-up grids

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use high-energy youth-oriented language ("Crank it up", "Sound that moves with you"). Reference activity contexts (party, run, ride, work). Use uppercase for CTAs ("SHOP NOW", "BUY"). Lead with the energy.

**Don't.** Don't write considered-prestige language (that's Bose/Sonos territory). Don't sanitize the action photography. Don't use exclamation points outside of the wordmark itself (the brand's name is JBL! with the exclamation — that's enough).

## 7. Motion Vocabulary

High-energy motion. Auto-playing lifestyle video heroes. Carousel transitions at 400–600ms with a slight ease. Hover lift on cards (1.04 scale + 200ms ease). Sound-wave ring animations on product pages run continuously. The motion budget is generous compared to Bose/Sonos — JBL leans into kinetic chrome.

## 8. Anti-patterns to Avoid

- **Don't tint the JBL Orange.** The specific saturated #ff5500 is brand
- **Don't replace dark canvas with white.** Youth-energy chrome lives on dark
- **Don't sanitize the lifestyle photography to clinical product-on-white.** The action context is the brand
- **Don't remove the sound-wave ring animations.** They are the brand's auditory-visual signature
- **Don't pair JBL Orange with a second saturated accent.** The orange is the brand voltage
- **Don't soften CTAs to rounded-rect.** Full-pill radius is the brand's CTA shape
- **Don't drop the uppercase tracking on CTAs.** The high-energy chrome leans on uppercase labels
