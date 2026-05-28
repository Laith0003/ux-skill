# Design System Inspired by EA

## 1. Visual Theme & Atmosphere

EA's web presence is sports-and-blockbuster-gaming chrome — the EA wordmark in heavy display sans, a dark canvas (#0d0d0d) on franchise pages, and a master brand chrome that connects EA Sports FC (formerly FIFA), Madden NFL, Battlefield, The Sims, and Apex Legends under one umbrella. The atmosphere is sports-broadcast cinematic where the IP demands it and corporate-master-brand where the chrome takes over.

The franchise architecture is the brand's most important navigational decision. Each franchise — FC, Madden, Battlefield, Sims, Apex — has its own visual identity with a dedicated palette and tone. EA Sports FC leans football-green and stadium-photography; Madden leans NFL-navy and turf textures; Battlefield leans dusty-orange and war-photography; Sims leans Plumbob-green and cheerful character art; Apex Legends leans pure-black-and-red and esports-broadcast. The EA master brand is the connective tissue: the dark canvas, the wordmark, and the EA Play subscription chrome.

EA Play — the subscription product — has its own chrome treatment. Premium subscriber content is marked with a vertical accent bar on hover, an "EA Play" badge, and slightly elevated card styling. The chrome reads as "this content is part of your membership" rather than "this is a separately priced product."

**Key Characteristics:**
- Dark canvas (#0d0d0d) on franchise and game pages
- EA wordmark — heavy display sans, pinned top-left
- Franchise-specific IP palettes per game
- EA Play premium accent chrome — vertical accent bar on subscribed cards
- Rectilinear UI (0–8px radius) — console-game-store feel
- Trailer-grade hero motion with slow parallax cuts
- Platform-icon row (PS5, Xbox, PC, Switch) on every game page

## 2. Color Palette & Roles

### Primary (Master Brand)
- **EA Red** (`#ff4747`): Master brand CTA accent — used on the EA wordmark and on select primary CTAs
- **Pure Black** (`#0d0d0d`): The canvas anchor
- **Pure White** (`#ffffff`): The text on dark

### Surface & Background
- **Dark Canvas** (`#0d0d0d`): Page background on franchise pages
- **Surface 1** (`#1a1a1a`): Card backgrounds
- **Surface 2** (`#252525`): Hover state, elevated panels
- **Hairline Dark** (`#2e2e2e`): 1px borders in dark mode

### Light-mode (account, support)
- **Light Canvas** (`#ffffff`)
- **Light Surface** (`#f5f5f7`)

### Neutrals & Text (on dark)
- **Ink** (`#ffffff`): Primary text
- **Body** (`#d2d2d4`): Default body text
- **Muted** (`#8e8e93`): Captions
- **Muted Soft** (`#5a5a5e`): Fine-print

### Franchise IP Palettes
- **EA Sports FC** — Stadium Green `#1c8d4d`, Black, White
- **Madden NFL** — NFL Navy `#013369`, NFL Red `#d50a0a`, White
- **Battlefield** — Dust Orange `#d76332`, Olive `#5e6432`, Black
- **The Sims** — Plumbob Green `#7cd83e`, Soft Cream `#f6f0e4`
- **Apex Legends** — Apex Red `#da292a`, Pure Black

### Semantic
- **Success** (`#43c870`): Green status (also EA Sports FC palette)
- **Warning** (`#ffb84a`): Amber
- **Error** (`#ff4747`): EA Red doubles as error

## 3. Typography Rules

### Font Family
- **Display + Body**: `EA Spectrum, Helvetica Neue, Arial, sans-serif` — modern heavy display sans (open-source substitute: `Inter` at heavier weights)

### Hierarchy
- **Franchise hero h1** — 64–96px weight 800, line-height 1.05
- **Section h2** — 36–48px weight 700
- **Card title** — 20–24px weight 700
- **Body** — 16px weight 400, line-height 1.5
- **Caption** — 13–14px weight 500
- **Button label** — 14–16px weight 700, often uppercase

### Principles
- Weight 800 for hero h1 — heavy display
- Uppercase tracking on CTAs (1px) — sports-broadcast aesthetic
- Tabular numerals on player stat readouts (FIFA/FC, Madden)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440px. Section padding is 80–120px vertical. Game card grids run 3-up or 4-up at desktop. Franchise pages use full-bleed hero takeovers.

## 5. Componentry Feel

- **Trailer hero (dark)** — Full-viewport auto-playing video, muted default, audio toggle. Franchise wordmark logo overlaid, primary CTA below
- **Franchise card (rectilinear)** — Dark surface, 4–8px radius, key art top, title + sub-line + platform icons below, "Play Now" or "Learn More" link
- **Primary CTA** — Brand red or franchise color fill, white text, 4px radius (or pill for "Buy"), 44px height, weight-700 uppercase label
- **EA Play membership banner** — Subscription chrome with the EA Play wordmark, member benefit list, "Join EA Play" CTA
- **Live-service status card** — For games-as-a-service (Apex, FC Ultimate Team), shows current season, daily challenges, ranked tier badge
- **Platform icon row** — Small PS5, Xbox, PC, Switch icons on every game card indicating availability

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use sports-broadcast / blockbuster cinematic language ("Take the field", "Drop in to King's Canyon"). Reference franchise IP by name. Use uppercase for purchase CTAs ("PLAY NOW", "BUY"). Lead with the action.

**Don't.** Don't sanitize franchise-specific tone (Apex is competitive-esports, Sims is whimsical-cheerful). Don't use friendly enterprise-speak. Don't translate franchise names.

## 7. Motion Vocabulary

Trailer-grade hero motion with slow parallax and live-action gameplay cuts (4–6 seconds per cut). Card hover triggers a tight 150ms scale (1.03) + slight bloom on the key art. EA Play premium cards have a subtle vertical accent line that appears on hover. Carousel transitions run 500–700ms slide-fade. No spring overshoots.

## 8. Anti-patterns to Avoid

- **Don't replace the dark franchise canvas with light surfaces.** Game pages live on dark
- **Don't strip the franchise palettes.** Each game brings its own IP color identity
- **Don't soften card radii above 8px.** EA reads as a game store, not consumer SaaS
- **Don't blur EA Play premium chrome into free content.** The accent bar is part of the IA
- **Don't use weight 600 or below for franchise hero h1.** Heavy display is the brand
- **Don't add character mascot icons in master chrome.** The chrome is utilitarian; IP carries personality
- **Don't autoplay trailer audio.** Mute default, user-initiated toggle
