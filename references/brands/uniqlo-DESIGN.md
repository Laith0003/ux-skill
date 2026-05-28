# Design System Inspired by UNIQLO

## 1. Visual Theme & Atmosphere

UNIQLO's web presence is the Japanese basics retailer translated into pixels: pure-white canvas, flat-light fashion photography, dense category grids, and a single chromatic note — UNIQLO red (#ff0000) — used as the brand's wordmark, on price-cut callouts, and on the rare hero CTA. The atmosphere is hyper-functional. Where its luxury-fashion peers stage their pages as moodboards, UNIQLO stages its pages as catalogs — model after model on pure-white seamlessly tiled, garment name and price stacked underneath, 4-up at desktop, 2-up at mobile. The philosophy "LifeWear" — clothing as everyday infrastructure — translates into a UI that treats abundance as a feature rather than a weakness.

The signature visual decision is the kana-and-Latin co-typesetting. On Japanese-locale and many global pages, the brand wordmark and headlines lock Japanese characters next to Helvetica Neue Latin at matched scale, announcing the Tokyo origin without ever needing to say "Japanese brand." On U.S. and European locales the kana is reduced but still present in the wordmark and certain editorial features.

Photography is the most disciplined element in the system. Every model is shot on pure-white or pure-black under flat soft light — no cinematic grading, no styling theatrics, no environmental props. The garment is the only signal. The "LifeWear" editorial spreads (long-scroll magazine-format features documenting fabric science, designer collaborations, seasonal collections) break the catalog rhythm with full-bleed photography and serif drop caps, but even there the lighting stays flat and journalistic.

**Key Characteristics:**
- Pure-white canvas (#ffffff) with pure-black ink (#000000); UNIQLO red (#ff0000) as the single chromatic accent
- Helvetica Neue Bold Latin paired with the proprietary UNIQLO Japanese face — kana-and-Latin lockup is signature
- Dense category-grid pages (4-up product tiles with image + name + price, 40-50 tiles per page)
- Flat-light fashion photography — pure-white or pure-black backgrounds, no cinematic grading
- Price-cut red callouts in 100% saturation red — never tinted
- Long-scroll "LifeWear" editorial spreads documenting fabric science and designer collabs
- Hard 200ms slide-down on mega-menu dropdowns — minimal motion vocabulary
- 0-to-4px border radius on cards; the brand reads as architectural, not decorative

## 2. Color Palette & Roles

### Primary
- **UNIQLO Red** (`#ff0000`): The single chromatic asset. Pure red — not warmed, not desaturated. Used on the wordmark, on price-cut callouts, on the rare hero CTA. Never as a section background; never tinted

### Surface & Background
- **Pure White** (`#ffffff`): The dominant canvas — every product page, every category grid, every editorial spread starts here
- **Pure Black** (`#000000`): The text color and the alternate photography backdrop. Used edge-to-edge as a contrasting band in fall/winter campaigns
- **Ash Gray** (`#f7f7f7`): Section dividers and subtle alternate band backgrounds

### Neutrals & Text
- **Pure Black** (`#000000`): All body text, all headlines, all product names. The high-contrast pairing with pure-white is non-negotiable
- **Charcoal** (`#7a7a7a`): Secondary copy — size labels, color labels, breadcrumbs
- **Silver Border** (`#e5e5e5`): 1px borders on size pickers and quantity steppers
- **Cream Sale Highlight** (`#fff5f0`): Background tint on price-cut tile callouts — barely-perceptible warmth as a pricing signal

### Semantic
- The brand avoids decorative semantics — the price-cut red doubles as both "savings" and "primary CTA"
- Validation errors render as plain dark red text, not branded

## 3. Typography Rules

### Font Family
- **Latin Display + Body**: `Helvetica Neue Bold` for display lockups, `Helvetica Neue` for body. The brand commits hard to Helvetica — no custom Latin face
- **Japanese**: The proprietary UNIQLO Japanese face — used in the wordmark and in Japanese-locale headlines. Matched in scale to the Latin lockup

### Hierarchy
- **Wordmark** — Helvetica Neue Bold, all caps, tight tracking, UNIQLO red on white
- **Hero headline** — 56–72px, Helvetica Neue Bold, slight negative letter-spacing (-0.5px)
- **Category headline** — 32–40px, Helvetica Neue Bold
- **Product name** — 14–16px, Helvetica Neue Regular
- **Price** — 14–18px, Helvetica Neue Bold; price-cut variant in UNIQLO red
- **Body** — 14–15px, Helvetica Neue Regular, 1.5 line-height
- **Caption / size label** — 12px, Helvetica Neue Regular, 0.04em tracking

### Principles
- Type stays at weights 400 and 700 — no light, no medium. The binary is the brand
- Tracking tightens at display sizes (-0.5px); body tracking sits at 0
- Headline alignment is left-aligned everywhere except editorial spreads (which can center)
- The kana-and-Latin lockup retains both scripts at equal weight — never reduce Japanese to a subtitle

## 4. Layout & Spacing

The base grid is 4-up at desktop, 2-up at tablet, 2-up at small tablet, and 2-up at mobile (the rare grid that stays 2-column on phones rather than collapsing to 1). Product tiles are perfect squares with photography filling the full square, name + price stacked below in a 56–72px strip.

Section padding is 80–96px vertical between major bands. Category-grid pages stack section after section without decorative breaks — the photography itself is the rhythm. Editorial "LifeWear" pages widen to 1200–1440px content max for full-bleed photography moments.

Whitespace philosophy: UNIQLO refuses the "curated 6-product hero" convention of luxury fashion. The category grid embraces abundance — 40–50 tiles per page — and trusts the customer to scan. Whitespace lives at the margins, not between products.

## 5. Componentry Feel

- **Product tile** — Square image (1:1), name + price below, no border, no shadow. Hover reveals an alternate angle (slight crossfade). 0-radius corners
- **Category grid** — 4-up dense grid, no gaps between tiles (or 4px gaps for visual rhythm)
- **Price-cut callout** — UNIQLO red strip above the price, white type at 12–14px, often paired with a `from $X` syntax
- **LifeWear editorial spread** — long-scroll magazine layout, drop-cap leads, full-bleed photography, serif accents
- **Designer collab hero** — full-bleed black or white photo with the designer name in Helvetica Neue Bold lockup
- **Size/color picker** — flat unstyled chips (radius 0–4px), 1px Silver Border, active chip flips to pure-black fill
- **Mega-menu dropdown** — opens with a hard 200ms slide-down (no spring, no overshoot), reveals a 4-column category list on white
- **Footer** — pure-white background, pure-black links, store-locator dominant, 11-locale switcher

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use plain product names ("Heattech Crew Neck T-Shirt"). State the price first, the fabric science second. Reference Japanese origin without performing it. Treat technical features (UV protection, anti-bacterial, heat retention) as bullet-point facts, not marketing hyperbole.

**Don't.** Don't write copy that sounds aspirational ("Elevate your everyday with…"). Don't use exclamation points outside of price-cut callouts. Don't translate "LifeWear" — it stays as a proper noun. Don't tag products with mood adjectives ("cozy", "effortless") — let the photography do that work.

## 7. Motion Vocabulary

Flat-light still photography is the visual anchor — motion is rare and minimal. Hero image carousels cross-fade slowly (~1.2s). Product tiles have zero hover transform. The only signature motion is the red-block dropdown animation in the mega-menu — a hard 200ms slide-down, no easing flourish, no spring overshoot. Add-to-cart triggers a small basket-count tick without any toast or modal.

## 8. Anti-patterns to Avoid

- **Don't tint the UNIQLO red.** It is pure #ff0000 — any pinkening, muting, or warmth shifts off-brand
- **Don't style fashion photography with mood lighting or color grading.** The brand is flat-light, hyper-real, no styling — the garment is the only signal
- **Don't drop the Japanese characters on global pages.** The kana presence is part of the brand's Tokyo authenticity
- **Don't curate-down the product grid to 6 tiles.** UNIQLO category pages are dense, catalog-style, and embrace abundance
- **Don't introduce a chromatic accent.** Black + white + red is the trinity; teal/blue/green accents read as off-brand
- **Don't replace Helvetica Neue with a "modern" geometric sans.** The brand's Helvetica commitment is part of its functional, no-styling identity
