# Design System Inspired by Zara

## 1. Visual Theme & Atmosphere

Zara's web presence is a deliberate provocation: it refuses every convention of e-commerce UX in favor of editorial fashion-magazine aesthetics. Where peers fill product pages with reviews, recommendations, and trust badges, Zara strips everything to the bone — full-bleed model photography, the smallest possible navigation chrome, near-invisible Add to Cart, and headlines set in a high-contrast didone serif that announces the page as a fashion editorial rather than a retail catalog.

The atmosphere is monochrome and severe. Canvas is pure white, ink is pure black, and the only chromatic note is whatever color happens to appear in the season's photography. There is no brand accent color in the UI sense — no red CTA, no blue link, no amber sale tag. The brand confidence is in refusing those affordances entirely. A first-time visitor often spends 5–10 seconds finding the Add to Cart button, which is set in 12px black-on-white near the bottom of the product page — and that friction is intentional. Zara is a brand that asks customers to come to it.

The product photography is the system's atmosphere. Editorial-quality, model-driven, often shot at extreme angles or with deliberate negative space, the photos are 9:16 or 4:5 portrait crops that bleed to the page edges. Models are styled and composed like fashion magazine spreads, not like e-commerce product shots. The garment is on a body, in motion, in a styled environment — never on a hanger or mannequin.

**Key Characteristics:**
- Pure-white canvas (#ffffff), pure-black ink (#000000) — no brand accent color in the UI
- Editorial fashion-magazine layout — full-bleed photography, oversized portrait crops
- Didone-style serif for headlines (very high contrast, hairline thin strokes)
- Geometric sans (Helvetica or similar) for body and UI labels
- Add to Cart is deliberately tiny — 12px text, often unstyled, located out of immediate sight
- Navigation chrome is minimal — hamburger top-left, basket count top-right, brand wordmark center
- Product page is photo-first; product name + price stack appear after multiple viewport scrolls
- Asymmetric layouts — single product, edge-to-edge, with the next product's preview peeking from the margin

## 2. Color Palette & Roles

### Primary
- The brand intentionally has no chromatic primary. The "brand color" is the photography itself — whatever colors the season's editorial happens to contain

### Surface & Background
- **Pure White** (`#ffffff`): The dominant canvas. Every page starts and ends in white
- **Pure Black** (`#000000`): The alternate canvas, used for editorial campaign hero takeovers and the mobile navigation drawer
- **Off-White** (`#fafafa`): A barely-perceptible section divider, used to break up consecutive white sections

### Neutrals & Text
- **Pure Black** (`#000000`): All text on light surfaces, all wordmark instances
- **Charcoal** (`#1a1a1a`): Used very rarely; the brand commits hard to pure black
- **Muted Gray** (`#999999`): Size labels, sold-out indicators, fine-print legal copy
- **Hairline** (`#e8e8e8`): 1px borders on size pickers, dropdowns, form inputs

### Semantic
- "Sold out" — muted gray text, never a saturated red
- Validation errors render as plain black with an asterisk; the brand refuses to color-code errors
- "Sale" — sometimes rendered as a small black-on-white pill, sometimes as struck-through black text. Never red

## 3. Typography Rules

### Font Family
- **Display**: A custom Didone-style serif (the brand uses a proprietary face with extreme thick-thin contrast and hairline thin strokes — `Bodoni Moda` or `Playfair Display` are open-source substitutes)
- **Body / UI**: Helvetica or a geometric sans — used for body, navigation, product names, prices

### Hierarchy
- **Editorial campaign headline** — 80–120px, Didone serif, weight 400, line-height 0.9, tight tracking (-2px)
- **Product name** — 14–16px, geometric sans, all caps, 1.5px tracking
- **Product price** — 14–16px, geometric sans, normal-case, no special treatment
- **Body** — 13–14px, geometric sans, 1.5 line-height
- **Navigation label** — 12px, geometric sans, all caps, 1px tracking
- **Fine print** — 11px, geometric sans, muted gray

### Principles
- The didone serif is the brand's voice — committing to its extreme contrast (hairline thin strokes against thick stems) is part of what reads as "Zara" rather than "fast fashion peer"
- All-caps + tracked sans labels for chrome — never sentence case for navigation
- Pricing is never bold, never highlighted. It is the same weight as the product name
- Headlines lean on size and tracking, not weight. Weight 700 didone reads as off-brand; weight 400 at 100px is correct

## 4. Layout & Spacing

The product grid breaks the 4-up convention — Zara often uses asymmetric 2-up or even 1-up grids where products bleed edge to edge. A category page might open with a single full-viewport editorial photo, then a 2-up grid, then a single full-bleed product, then back to a 4-up. The unpredictability is the rhythm.

Section padding is generous (60–120px vertical between major bands). Internal product page padding is asymmetric — a product photo might bleed to the left edge while leaving a 200px right gutter that holds nothing but white space. The white space is the design.

Whitespace philosophy: Zara treats whitespace as an aesthetic asset, not a usability convention. Pages can scroll for 8+ viewports before reaching the footer. The friction is the brand.

## 5. Componentry Feel

- **Product tile (editorial)** — Full-bleed portrait photo, name + price below in 14px sans caps. No add-to-cart button on the tile
- **Product page hero** — Full-viewport editorial photo, often with two crops side-by-side. No headline, no UI overlay
- **Product page chrome** — Below the hero, a single column with name, price, size picker, color swatch row, and the unstyled "ADD" button (12–14px black-on-white, no border, no fill)
- **Size picker** — Flat row of size chips with 1px hairline borders, active state inverts to black fill + white text
- **Navigation drawer** — Slides in from the left as a full-height pure-black panel with white labels in all-caps. Closing X is in the top-right
- **Basket (cart)** — Counter top-right in plain numbers, no badge color
- **Footer** — Pure-white, links in 12px black caps, country/language switcher dominates
- **Search** — Full-page overlay that takes over the viewport, with the input centered and the rest of the page dimmed to white

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use spare product names ("OVERSIZED COTTON SHIRT"). Treat seasonal collections as proper nouns (SS25, AW24). Quote price plainly without currency-symbol gymnastics. Use directional verbs sparingly ("ADD", "REMOVE") rather than friendly ones ("Add to my bag").

**Don't.** Don't use exclamation points. Don't write copy that sells ("Elevate your wardrobe with…"). Don't add ratings, reviews, or "customers also bought" — the brand refuses social proof. Don't translate "ZARA" — the wordmark is locale-invariant.

## 7. Motion Vocabulary

Motion is editorial and slow. Image carousels cross-fade at 1.5–2 seconds — far slower than e-commerce convention. The navigation drawer slides in over 400ms with a slight ease-out. Product images have no hover transform; the only on-image motion is a slight ken-burns pan on certain campaign-landing crops. Add-to-Cart triggers a minimal "added" confirmation in 12px text near the button — no toast, no modal, no overlay.

## 8. Anti-patterns to Avoid

- **Don't introduce a chromatic CTA color.** Zara's Add to Cart is unstyled black-on-white. Adding a red, blue, or green CTA breaks the brand
- **Don't add reviews, ratings, or social proof.** The brand deliberately refuses these e-commerce conventions
- **Don't bold the didone display face.** It reads as off-brand. The 400-weight at large sizes is the brand
- **Don't reduce the photography crop ratios.** Editorial 9:16 or 4:5 portraits are signature; landscape product shots flatten the brand
- **Don't grid-align the asymmetric layouts.** Zara's intentional misalignment (a product peeking from the margin) is part of the editorial feel
- **Don't add an "added to cart" modal.** The minimal in-place confirmation is part of the friction-as-luxury aesthetic
- **Don't use a friendly sans like Inter for chrome.** Helvetica's neutrality is part of the cold-editorial feel — Inter reads as too humanist
