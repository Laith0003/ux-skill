# Design System Inspired by Loom

## 1. Visual Theme & Atmosphere

Loom's web presence is async-video-for-work chrome — a deep purple primary (#625df5) as the brand voltage, soft rounded cards, illustration-driven heroes featuring people in the act of recording a video. The atmosphere is friendly workplace SaaS: approachable, animated, and confident that async video is the future of work communication. Where peer collaboration tools (Slack, Teams, Notion) lean into productivity-card density, Loom leans into the video-message as the primary content unit — every page features the signature video-thumbnail with a circular recorder avatar overlaid.

The Loom Purple (#625df5) is the brand voltage. It is a specific lavender-leaning purple — neither blue, nor magenta. The color appears on CTAs, on the wordmark, and as accent moments inside illustrations (the recorder avatar's border, the play button color). The purple is generous on the brand presence and scarce on individual chrome elements.

The video-message thumbnail is the brand's signature visual unit. Every screenshot mockup on the marketing site shows a video frame with a circular recorder avatar overlaid in the bottom-left corner — that's the Loom convention: the recorder's face is part of the message. Replacing this thumbnail style with a generic video player thumbnail flattens the brand.

**Key Characteristics:**
- Loom Purple (#625df5) — chromatic voltage on CTAs, wordmark, accents
- White canvas with soft-rounded cards (12–16px radius)
- Illustration-driven heroes — people recording or watching video
- Video-message thumbnail signature — circular recorder avatar overlaid on video frame
- Inter typography across chrome
- Friendly micro-animations on cards and buttons

## 2. Color Palette & Roles

### Primary
- **Loom Purple** (`#625df5`): The brand voltage — CTAs, wordmark, accents
- **Purple Hover** (`#4f4cc6`): Press state
- **Purple Soft** (`#e6e5fd`): Subtle background tint on featured content

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#fafafb`): Alternating section bands
- **Surface Card** (`#f5f5f7`): Card hover state
- **Hairline** (`#e8e8eb`): 1px borders

### Neutrals & Text
- **Ink** (`#13141c`): Primary text
- **Body** (`#3a3c47`): Default body text
- **Muted** (`#6c6e7e`): Captions
- **Muted Soft** (`#9da0ad`): Fine-print

### Illustration Accent Tints
- **Coral** (`#ff8b76`): Used in illustrations for skin/clothing warmth
- **Sky Blue** (`#6cc4f5`): Background illustration accent
- **Mint** (`#7cd3a7`): Accent in workflow diagrams

### Semantic
- **Success** (`#22c55e`): Green
- **Warning** (`#f59e0b`): Amber
- **Error** (`#ef4444`): Red

## 3. Typography Rules

### Font Family
- **Display + Body**: `Inter, system-ui, sans-serif` — modern humanist sans

### Hierarchy
- **Hero h1** — 48–64px Inter weight 700, line-height 1.1
- **Section h2** — 32–40px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–18px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for hero h1, weight 600 for card titles
- Body sits at 16–18px for friendly reading
- Tracking slightly negative at display sizes (-0.5px)

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 80–120px vertical. Feature card grids run 3-up at desktop.

## 5. Componentry Feel

- **Video-message thumbnail** — Video frame mockup with a circular recorder avatar overlaid in the bottom-left, play button centered, duration top-right
- **Primary CTA (purple pill)** — Loom Purple fill, white text, full-pill radius, 44px height, weight-600 label
- **Secondary CTA** — Transparent fill, 2px Loom Purple border, purple text
- **Hero illustration (recording)** — Illustrated person at a desk, headset on, gesturing while recording — with the Loom video-message thumbnail mocked-up in their viewport
- **Feature card (soft radius)** — White surface, 12–16px radius, hairline border, internal padding 24px. Icon top, headline, description, optional CTA
- **Playback controls** — Inline video player controls with the signature purple progress bar

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use friendly workplace-async language ("Send a quick Loom instead", "Async, but human"). Reference workflow contexts (standup, design review, customer demo). Use sentence case for chrome.

**Don't.** Don't write corporate-enterprise speak. Don't use exclamation points in chrome. Don't sanitize the playful illustration personality.

## 7. Motion Vocabulary

Friendly micro-animations — hover lift on cards (1.02 scale + 200ms ease). Playful idle animations on hero illustrations (the recording person occasionally blinks or gestures). Soft spring on button press (50ms scale-down + 100ms back). Video player previews auto-play silently on hover.

## 8. Anti-patterns to Avoid

- **Don't replace Loom Purple with a saturated tech-blue.** The specific lavender-purple is brand
- **Don't sharpen card radii below 8px.** Friendly SaaS softness
- **Don't sanitize the recording-people illustrations to generic 3D renders.** The hand-drawn personality is brand
- **Don't strip the video-message thumbnail style.** Circular recorder avatar overlay is brand signature
- **Don't pair the purple with a second saturated brand accent.** The purple is the voltage
- **Don't use weight 600 for hero h1.** Weight 700 is the brand standard
- **Don't disable the video preview hover animations.** They demonstrate the product
