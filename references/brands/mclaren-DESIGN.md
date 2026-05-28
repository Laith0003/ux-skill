# Design System Inspired by McLaren

## 1. Visual Theme & Atmosphere

McLaren's web presence is hypercar-racing chrome — McLaren Orange (#ff8000) as the chromatic anchor, dark cinematic photography in racing-circuit lighting, and a layout grammar that reads as Formula 1 mission control. The atmosphere is racing-engineered. Where Ferrari plays "Italian luxury heritage" and Lamborghini plays "fighter-jet aggressive," McLaren plays "F1 engineering excellence translated into road cars." The chrome references aerodynamic precision, lap times, and engineering provenance at every section break.

McLaren Orange is the brand's chromatic voltage — drawn from the F1 racing program's papaya livery. The specific saturated hex (#ff8000) is non-negotiable; replacing with a tinted coral or a "modern" orange is a recognition failure. The orange appears on CTAs, on telemetry-style numerical readouts, on the wordmark accent, and as a signature accent on configurator surfaces.

The dark canvas (#0a0a0a) is the brand's atmosphere. Hypercars are photographed in racing-circuit lighting — pit-lane, garage, night-time circuit, paddock — and the dark backdrop makes the carbon-fiber bodywork and orange accents glow. The chrome's job is to recede so the car can perform.

**Key Characteristics:**
- McLaren Orange (#ff8000) — chromatic voltage drawn from F1 papaya livery
- Dark cinematic canvas (#0a0a0a) — racing-circuit lighting backdrop
- F1-mission-control aesthetic — telemetry readouts, tabular lap-time figures
- Rectilinear UI (0–4px radius) — engineering precision
- Auto-playing engineering-cinematic video heroes
- Carbon-fiber texture as occasional surface accent
- Configurator with livery picker (papaya, deep black, racing greens)

## 2. Color Palette & Roles

### Primary
- **McLaren Orange / Papaya** (`#ff8000`): The brand voltage — CTAs, wordmark accent, telemetry readouts
- **Orange Hover** (`#cc6600`): Press state
- **Pure Black** (`#0a0a0a`): The canvas anchor

### Surface & Background
- **Dark Canvas** (`#0a0a0a`): Page background
- **Surface 1** (`#1a1a1a`): Card backgrounds
- **Surface 2** (`#252525`): Hover state, elevated panels
- **Hairline Dark** (`#2e2e2e`): 1px borders

### Light-mode (rarely used, mostly account chrome)
- **Light Canvas** (`#ffffff`)
- **Light Surface** (`#f5f5f7`)

### Neutrals & Text (on dark)
- **Ink** (`#ffffff`): Primary text
- **Body** (`#dedede`): Default body text
- **Muted** (`#8e8e93`): Captions
- **Muted Soft** (`#5e6873`): Fine-print

### Texture Accents
- **Carbon Fiber Pattern**: Used as occasional surface fill on specs callouts
- **Racing Livery Stripes**: Used as section dividers on motorsport pages

### Semantic
- **Success** (`#3fb95e`): Green
- **Warning** (`#ff8000`): McLaren Orange doubles as warning
- **Error** (`#ff4747`): Red

## 3. Typography Rules

### Font Family
- **Display**: `McLaren Display, Helvetica Neue, sans-serif` — heavy modern display sans
- **Body**: `McLaren Sans, Helvetica Neue, sans-serif` — clean sans

### Hierarchy
- **Hero h1** — 64–96px McLaren Display weight 800, line-height 1.0, all caps optional
- **Section h2** — 36–48px weight 700
- **Card title** — 20–24px weight 700
- **Body** — 16px weight 400, line-height 1.5
- **Caption** — 13–14px weight 500
- **Telemetry readout** — Monospace tabular figures for lap times, 0-60 mph
- **Button label** — 14–16px weight 700, uppercase with 1.5px tracking

### Principles
- Weight 800 for hero h1 — heavy engineering display
- Uppercase tracking on CTAs and section labels
- Tabular monospace for technical readouts — F1-mission-control aesthetic

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1440–1600px. Section padding is 80–120px vertical. Hypercar hero sections use full-bleed cinematic photography or auto-playing video.

## 5. Componentry Feel

- **Hypercar hero video** — Full-viewport auto-playing video of the car on a circuit or in pit lane, muted default, audio toggle. Vehicle model name overlaid in display sans weight 800
- **Primary CTA (orange rect)** — McLaren Orange fill, white text, 0–4px radius, 48px height, weight-700 uppercase label
- **Vehicle card (dark rectilinear)** — Dark surface, 0–4px radius, vehicle render with subtle orange-edge highlight on hover, title + key spec (0-60 mph or power figure)
- **Spec telemetry readout** — Tabular monospace numerals presenting 0-60, top speed, power, weight in F1-mission-control format
- **Configurator livery picker** — Horizontal row of livery swatches (Papaya, Deep Black, Racing Green) for exterior color
- **Carbon-fiber surface accent** — Carbon-fiber texture used sparingly on spec callout backgrounds

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use racing-engineering language ("Engineered for the track", "0-60 in 2.8 seconds"). Quantify performance precisely. Reference F1 provenance.

**Don't.** Don't write consumer-aspirational softness. Don't use exclamation points. Don't sanitize the racing-engineering positioning.

## 7. Motion Vocabulary

Racing-grade motion. Auto-playing engineering-cinematic video heroes. Slow ken-burns pans on still imagery (10-second cycles). Hover lift on vehicle cards (1.04 scale + 200ms ease). Configurator changes use a hard cut at 150ms — racing-precision, no spring.

## 8. Anti-patterns to Avoid

- **Don't tint McLaren Orange.** The specific saturated #ff8000 is brand
- **Don't replace dark cinematic canvas with white.** Hypercar photography demands dark backdrop
- **Don't soften card radii above 4px.** Racing engineering precision
- **Don't sanitize the F1-mission-control aesthetic.** It is the brand
- **Don't pair the orange with a second saturated accent.** The orange is the voltage
- **Don't use weight 600 for hero h1.** Weight 800 is the brand standard
- **Don't autoplay engine audio.** Mute default, user-initiated toggle
