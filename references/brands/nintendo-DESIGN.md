# Design System Inspired by Nintendo

## 1. Visual Theme & Atmosphere

Nintendo's web presence is the brand's signature "family-friendly fun" translated into a card-rich, character-led UI. The atmosphere is playful, IP-driven, and unmistakably joyful where the property demands it. Where peer gaming brands (PlayStation, Xbox) lean into dark canvases, cinematic photography, and edgy minimalism, Nintendo leans into white canvas, generous radii, bright IP-driven secondary palettes, and hero illustrations of Mario, Link, Pikachu, Donkey Kong, and the rest of the cast. The brand commits to "fun for everyone" and the design language follows.

Nintendo Red (#e60012) is the chromatic anchor — used on the wordmark, on primary CTAs, and as the brand mark on the Switch console silhouette. It is a specific saturated red — not coral, not crimson, a true #e60012. The red is scarce on individual elements (it shows up on the "Buy Now" CTA and the wordmark) and generous on the brand presence (the home page hero often features a red banner).

The signature interaction is the IP-led hero card. Every product page opens with the relevant character — Mario waves on Mario pages, Pikachu blinks on Pokemon pages, Link draws his sword on Zelda pages. The character is the hero. The design system is built around making those characters look right at every scale, and the chrome around them stays restrained so the IP can perform.

**Key Characteristics:**
- Nintendo Red (#e60012) — wordmark, primary CTAs, brand mark
- White canvas with generous character-driven hero illustrations
- 16–24px radii on character cards — softness as friendliness signal
- IP-driven secondary palette per franchise — Mario red, Zelda gold, Pokemon yellow, Splatoon pink/lime
- Switch-shaped product cards when the product is a console or game
- Friendly humanist sans display + body (Nintendo proprietary or open-source substitute)
- Idle animations on character heroes — Mario waves, Pikachu blinks

## 2. Color Palette & Roles

### Primary
- **Nintendo Red** (`#e60012`): Wordmark, primary CTA fill, brand mark
- **Red Hover** (`#b8000e`): Press state
- **Red Soft** (`#fce4e6`): Subtle red tint for promotional banners

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f5f5f5`): Alternating section bands
- **Surface Warm** (`#fafafa`): Hover state on cards
- **Hairline** (`#e0e0e0`): 1px borders

### Neutrals & Text
- **Ink** (`#1f1f1f`): Primary text
- **Body** (`#3a3a3a`): Default body text
- **Muted** (`#5e5e5e`): Captions
- **Muted Soft** (`#8a8a8a`): Fine-print

### IP-Driven Secondary (used contextually per franchise)
- **Mario Red** (`#ed1e24`)
- **Luigi Green** (`#43b047`)
- **Zelda Gold** (`#d4a017`)
- **Pokemon Yellow** (`#ffcb05`)
- **Splatoon Pink** (`#ff3380`) + **Lime** (`#a4f100`)
- **Animal Crossing Green** (`#82be39`)

### Semantic
- **Success** (`#43b047`): Green confirmation (also Luigi Green)
- **Warning** (`#d4a017`): Caution
- **Error** (`#e60012`): Brand red doubles as error semantic

## 3. Typography Rules

### Font Family
- **Display + Body**: `Nintendo Display, Nintendo Body, sans-serif` (proprietary). Open-source substitute: `Inter` or `Noto Sans` with slightly wider tracking. Display variant has rounded terminals to match the friendly brand voice

### Hierarchy
- **Hero h1** — 48–72px display, weight 700, line-height 1.1
- **Section h2** — 32–42px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 700

### Principles
- Weight 700 for hero h1 — the brand commits to bold display
- Display headlines often feature drop shadow or outline for character cards (game-poster style)
- Body stays clean — no decorative type below 24px

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Character cards run 3-up or 4-up at desktop. Hero sections use a 7-5 split with the character illustration on the right (or left, depending on the franchise's directionality).

## 5. Componentry Feel

- **Primary CTA (pill)** — Nintendo Red fill, white text, full-pill radius (or 16px rounded-rect), 44–48px height, weight-700 label
- **Character hero card** — Soft-radius surface (16–24px), character illustration filling 60% of the card, game/title name on the other 40%, "Learn more" pill CTA
- **Game card (soft radius)** — White surface, 16px radius, 1px hairline border, game cover image at top (cropped to fit), title + price + "Add to cart" below
- **Switch-shaped frame** — When showing a game on the Switch console, the screenshot is masked into the Switch's hardware silhouette
- **IP-driven section background** — Sections on franchise pages can use the IP's secondary color as a band background (Mario red band, Zelda gold band) — used sparingly
- **Footer** — Soft surface, multi-column site-map, region switcher, Nintendo Account link

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use friendly inclusive language ("Play together", "Bring the family"). Reference characters by name (Mario, Link, Princess Zelda). Use sentence case for chrome. Lead with the joy ("Save Hyrule once more").

**Don't.** Don't write edgy or competitive copy. Don't sanitize the character personality — the brand voice is character-led. Don't use exclamation points outside of moments of genuine celebration. Don't translate character names (Mario stays Mario across locales).

## 7. Motion Vocabulary

Character heroes have idle animations — Mario waves on hover, Pikachu blinks at random intervals, Link draws his sword. Card hover triggers a soft 200ms scale-up (1.03). Scroll-triggered reveals on character cards as the section comes into view. The motion is gentle and joyful — no chaotic spring, no aggressive scale.

## 8. Anti-patterns to Avoid

- **Don't replace the character illustrations with generic 3D renders.** The IP cast is the brand voice
- **Don't strip the IP-driven secondary colors when the IP demands them.** Mario pages get Mario red; Pokemon pages get Pokemon yellow
- **Don't sharpen card radii to 0–4px.** Nintendo's soft radii are the friendliness signal
- **Don't add edgy or aggressive motion.** The brand is family-friendly even on Bowser pages
- **Don't use a saturated tech-blue accent.** Nintendo's chrome stays red + white + IP color
- **Don't add gradient overlays to character illustrations.** Characters are crisp flat art (or character-rendered 3D with clean lighting)
- **Don't blur the line between Nintendo brand chrome and IP-specific chrome.** A Mario page can lean into Mario; the home page stays the master brand
