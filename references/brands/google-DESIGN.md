# Design System Inspired by Google

## 1. Visual Theme & Atmosphere

Google's web presence is the canonical Material You / Material 3 expression: a paper-bright canvas, friendly geometric type (Google Sans), saturated four-color brand palette used semantically, and a card-based layout grammar that treats every product feature as a small bento tile. The atmosphere is approachable, optimistic, and consumer-grade — even on enterprise Google Cloud pages. Where Microsoft reads as institutional and Apple reads as reverent-product-photography, Google reads as soft-bright-bento-tile.

The defining visual decisions are the four-color brand palette — Blue #4285f4, Red #ea4335, Yellow #fbbc04, Green #34a853 — and the generous radii on every surface. Cards round at 16–28px (the Material 3 "extra-large" radius), buttons round at 20–28px pill or 8–12px rounded-rect. The soft radii read as friendly rather than precise; this is the brand telling you the technology is approachable.

Google Sans (the proprietary display + body family) carries the typographic voice. Its rounded terminals, humanist proportions, and slightly wider apertures make headlines feel like they're inviting you in rather than declaring at you. The brand commits to weight 500 (Medium) for headlines — never 700 — to keep the friendliness consistent.

**Key Characteristics:**
- White canvas, near-black ink, four-color brand palette used semantically (Blue = primary action, Red = destructive, Green = success, Yellow = caution)
- Google Sans Display + Text — proprietary geometric humanist sans
- Generous radii: cards 16–28px, buttons 20–28px pill or 8–12px rect
- Material 3 surface tonal elevation — surfaces shift hue with elevation, not shadow
- Bento-tile feature grids — 3-up or 4-up small cards with illustration + headline + short description
- Filled tonal buttons — primary action style with a low-saturation tinted fill
- Spring-emphasized motion easing — Material's signature `cubic-bezier(0.2, 0, 0, 1)`

## 2. Color Palette & Roles

### Brand Four
- **Google Blue** (`#4285f4`): Primary CTA, links, focus rings, brand "G" first letter
- **Google Red** (`#ea4335`): Destructive actions, "stop" semantics, brand "G" o (second letter)
- **Google Yellow** (`#fbbc04`): Caution, neutral attention, brand "G" o (third letter)
- **Google Green** (`#34a853`): Success, "go" semantics, brand "G" e (final letter)

### Surface & Background
- **Pure White** (`#ffffff`): The default canvas
- **Surface Container Low** (`#f8f9fa`): First elevation tier — alternate section backgrounds
- **Surface Container** (`#f1f3f4`): Second tier — card hover, drawer surfaces
- **Surface Container High** (`#e8eaed`): Third tier — emphasized cards, selection states
- **Outline** (`#dadce0`): 1px hairline border
- **Outline Variant** (`#e8eaed`): Subtle inner-card divider

### Neutrals & Text
- **Ink** (`#202124`): Primary text and headlines
- **Body** (`#3c4043`): Default body text
- **Muted** (`#5f6368`): Sub-headings, captions, breadcrumbs
- **Muted Soft** (`#80868b`): Fine-print, disabled states
- **On Primary** (`#ffffff`): Text on Google Blue CTAs

### Brand Accent Tints (Material 3 tonal)
- **Blue Container** (`#d2e3fc`): Tonal-button fill — lighter blue surface with dark blue text
- **Green Container** (`#ceead6`): Success surface fill
- **Yellow Container** (`#feefc3`): Caution surface fill
- **Red Container** (`#fad2cf`): Error surface fill

## 3. Typography Rules

### Font Family
- **Display**: `Google Sans Display, system-ui, sans-serif` — the proprietary display optical variant
- **Body**: `Google Sans Text, system-ui, sans-serif` — the proprietary text optical variant
- **Mono**: `Google Sans Code` or `Roboto Mono` — for code snippets

### Hierarchy
- **Display Large** — 57px, Google Sans Display, weight 400, line-height 1.12, tracking -0.25px
- **Display Medium** — 45px, weight 400, line-height 1.15
- **Headline Large** — 32px, Google Sans Display, weight 500
- **Headline Medium** — 28px, weight 500
- **Title Large** — 22px, Google Sans Text, weight 500
- **Body Large** — 16px, weight 400, line-height 1.5
- **Body Medium** — 14px, weight 400
- **Label Large** — 14px, weight 500 — used for button labels and category chips

### Principles
- Weight 500 (Medium) is the workhorse for headlines and labels — never 700
- Display sizes can drop to weight 400 (Regular) for the largest h1s — the friendliness comes from generous size, not from weight
- Google Sans's rounded terminals are part of the brand voice — substituting Inter or Roboto loses the warmth
- Tracking adjusts at display sizes (-0.25px at 57px); body tracking stays at 0

## 4. Layout & Spacing

The site uses a 12-column grid with an 8-base spacing system. Section padding is 80–120px vertical between major bands. Bento-tile grids run 3-up or 4-up at desktop, 2-up at tablet, 1-up at mobile. Tile internal padding is 24–32px.

Hero sections often use a single-column centered layout — display headline (45–57px), short sub-line, primary CTA, illustration below. Product pages use a 6-6 split with the product render on the right.

## 5. Componentry Feel

- **Bento feature tile** — Soft-radius card (16–28px), illustration or icon top, headline (h3), short body, optional "Learn more" link. White surface with `#dadce0` hairline border, or a soft `#f8f9fa` fill for emphasis
- **Primary CTA (filled)** — Solid Google Blue fill, white text, pill radius (20–28px) or rounded-rect (8–12px), 40px height, label in 14px Google Sans weight 500
- **Filled tonal button** — Material 3 signature — soft tinted fill (e.g., Blue Container `#d2e3fc`), dark blue text. Reads as a friendlier-than-primary secondary
- **Text button** — Transparent fill, blue text, no border. Used for tertiary actions
- **Material text field** — Filled or outlined variants. The filled variant has a soft tint background and a 2px Blue underline on focus. The outlined variant uses a 1px hairline border that thickens and turns blue on focus
- **Navigation rail** — Left-side icon column (60px wide) with vertical icon stack. Used on app-shell pages like Gmail or Drive
- **FAB (floating action button)** — Circular or extended pill, brand blue or yellow fill, 56px diameter. Floats bottom-right on app surfaces
- **App bar** — Horizontal top nav, sticky, with a slight tonal-elevation shift when scrolled

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Write friendly direct copy ("Get started in seconds"). Use sentence case for everything — buttons, headers, navigation. Quantify capability ("3.5 billion searches a day"). Lead with the customer outcome.

**Don't.** Don't use title case for chrome (this isn't Apple). Don't write corporate-speak ("Leverage Google's enterprise-grade…"). Don't use exclamation points in chrome. Don't translate brand product names (Gmail, Drive, Workspace stay as is).

## 7. Motion Vocabulary

Material motion is the system's signature. Transitions use Material's "emphasized" easing `cubic-bezier(0.2, 0, 0, 1)` — a spring-like curve that grounds motion. Container-transforms morph cards between states (collapsed bento → expanded detail page) rather than fading or sliding. FAB extends with a 250ms morph from circular to pill. The friendliness of the easing is part of the brand voice — replacing with linear or ease-in-out flattens the feel.

## 8. Anti-patterns to Avoid

- **Don't use the four brand colors as decorative gradients.** They are semantic + brand-mark only. Painting a hero in a four-color gradient breaks the brand
- **Don't replace Google Sans with Roboto for display sizes.** Display optical variant is part of the brand
- **Don't sharpen card corners below 8px.** Soft radii are the brand's friendliness signal
- **Don't add deep drop shadows.** Material 3 uses tonal surface elevation — depth comes from surface hue shift, not from shadow
- **Don't use weight 700 for headlines.** Weight 500 (sometimes 400 for large h1s) is the brand standard
- **Don't paint the entire chrome in Google Blue.** The blue is scarce on individual CTAs and generous only on the wordmark "G"
- **Don't ignore the Material easing.** Linear transitions and 100ms hovers feel un-Google
