# Design System Inspired by Ubisoft

## 1. Visual Theme & Atmosphere

Ubisoft's web presence is cinematic gaming-publisher chrome — a dark canvas (#0e1318) carrying edge-to-edge game key art, the Ubisoft swirl logo as the brand mark, and trailer-grade hero treatments. The atmosphere is action-blockbuster: every page reads as the title screen of a major game franchise, with the chrome serving as the navigational scaffolding between franchises rather than as a designed surface in its own right.

The franchise architecture is the most important brand decision. Ubisoft publishes Assassin's Creed, Far Cry, Rainbow Six, The Division, Watch Dogs, Just Dance, and a dozen more — and each franchise has its own visual identity. Assassin's Creed leans cream-and-blood-red with Renaissance/Egyptian iconography; Far Cry leans dust-orange with first-person-shooter chrome; Rainbow Six leans tactical-gray with redacted-document typography. The Ubisoft master brand is the connective tissue — the dark canvas, the swirl logo, the unified account chrome (Ubisoft Connect) — but the franchise pages can lean hard into their own IP palette.

The hero treatment is cinematic. Most franchise pages open with a full-viewport auto-playing trailer (muted by default) with the franchise name overlaid in heavy display type. The trailer carries the atmosphere; the chrome stays minimal so the trailer can perform.

**Key Characteristics:**
- Dark canvas (#0e1318) — cinematic backdrop for game key art
- Ubisoft swirl logo as the brand mark
- Franchise-driven IP color treatments per game
- Cinematic auto-playing trailer heroes (muted default, audio toggle)
- Rectilinear game cards (0–8px radius)
- Heavy display typography (Ubisoft Sans 900) on franchise heroes
- Carousel transitions are weighty and deliberate, never bouncy

## 2. Color Palette & Roles

### Primary (Master Brand)
- **Ubisoft Blue** (`#0070f3`): The corporate brand accent — used on Ubisoft Connect chrome, account pages, and the master site. Not used on franchise pages
- **White** (`#ffffff`): The wordmark color and the primary text on dark canvases

### Surface & Background
- **Dark Canvas** (`#0e1318`): The dominant page background — near-black with a slight blue undertone
- **Surface 1** (`#1a2028`): Card backgrounds
- **Surface 2** (`#252d36`): Hover state, elevated panels
- **Hairline Dark** (`#2e3743`): 1px borders in dark mode

### Light-mode (rarely used, mostly for account chrome)
- **Light Canvas** (`#ffffff`): Account pages, support
- **Light Surface** (`#f6f7f9`): Section bands in light mode

### Neutrals & Text (on dark canvas)
- **Ink** (`#ffffff`): Primary text
- **Body** (`#dde2e8`): Default body text
- **Muted** (`#8c95a0`): Captions
- **Muted Soft** (`#5e6873`): Fine-print

### Franchise IP Palettes (contextual)
- **Assassin's Creed** — Cream `#e6dcc7`, Blood Red `#a01818`, Black
- **Far Cry** — Dust Orange `#d35831`, Olive `#6b6c3a`, Black
- **Rainbow Six** — Tactical Gray `#3e424a`, Hex Red `#c83d3d`, Black
- **The Division** — Toxic Orange `#ff4f1f`, Snow White, Black

### Semantic
- **Success** (`#3fb95e`): Green status
- **Warning** (`#f0a93a`): Amber warning
- **Error** (`#c83d3d`): Red error

## 3. Typography Rules

### Font Family
- **Display + Body**: `Ubisoft Sans, Helvetica Neue, Arial, sans-serif` — heavy modern sans with strong display weight axis

### Hierarchy
- **Franchise hero h1** — 80–120px Ubisoft Sans weight 900, line-height 1, all caps optional
- **Section h2** — 40–56px weight 800
- **Card title** — 20–28px weight 700
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 500
- **Button label** — 14–16px weight 700, often uppercase

### Principles
- Weight 900 (Black) for franchise hero h1 — the brand commits to heavy display
- Display headlines may use all-caps with slight tracking (1–2px)
- Body stays clean, no italic
- Numerals are tabular for stat readouts (achievement counts, kill counts on gaming achievements)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440–1600px (wider than most marketing sites). Section padding is 80–120px vertical. Game card grids run 4-up at desktop. Franchise pages use full-bleed hero takeovers.

## 5. Componentry Feel

- **Cinematic trailer hero** — Full-viewport (100vh) auto-playing video, muted by default, audio toggle bottom-right. Franchise name overlaid in display sans weight 900, "Play Now" or "Buy Now" pill CTA below
- **Primary CTA** — Brand blue or franchise-IP color fill, white text, 4px radius (or full pill for "Get the Game"), 44px height, weight-700 label, often uppercase
- **Game card (rectilinear)** — Dark surface, 0–8px radius, game key art top (16:9), title + franchise + platform icons below, "Learn More" link
- **Franchise page hero** — Full-bleed IP-treated hero with the franchise wordmark logo, sub-title, and primary CTA
- **Ubisoft Connect banner** — Membership chrome on logged-in pages, dark surface with the Ubisoft swirl, points balance, recent achievements
- **Carousel of key art** — Multi-game carousel on the master home page, slow auto-cycling, dot indicators

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use cinematic action-blockbuster language ("Live your story", "Take back the streets"). Reference franchise IP by name. Use uppercase for CTAs ("PLAY NOW", "BUY"). Lead with the action / drama.

**Don't.** Don't use friendly playful microcopy. Don't sanitize franchise-specific tone (Assassin's Creed is brooding, Just Dance is celebratory). Don't translate franchise names (Assassin's Creed stays as is).

## 7. Motion Vocabulary

Cinematic trailer-style motion. Hero trailers auto-play with parallax depth. Slow ken-burns pans on still key art (~6–8 seconds per pan). Card hover triggers a hard 200ms scale (1.04) + slight bloom on the key art. Carousel transitions are deliberately weighty — 600–800ms slide-and-fade. The motion never bounces or springs; the brand reads as cinematic, not animated.

## 8. Anti-patterns to Avoid

- **Don't replace the dark canvas with white.** Cinematic key art demands dark backdrop
- **Don't strip the franchise IP color treatments.** Each franchise has its own palette identity
- **Don't soften card radii above 8px.** The brand reads as console-game-store, not soft consumer SaaS
- **Don't autoplay video with sound.** Mute is default, audio toggle is user-initiated
- **Don't use weight 700 for franchise hero h1.** Weight 900 is the brand standard
- **Don't introduce a saturated brand-blue gradient on franchise pages.** Each franchise has its own palette
- **Don't add character mascot icons in the master chrome.** The chrome is utilitarian; the IP carries the personality
