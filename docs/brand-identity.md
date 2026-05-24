# Brand identity — for the ux-skill landing page

Source: user-provided Claude.com / Anthropic brand spec. This file is the load-bearing input for the landing-page sub-agent dispatch.

## Overview

Claude.com is the warmest, most editorial interface in the AI-product category. The base atmosphere is a **tinted cream canvas** (`{colors.canvas}` — #faf9f5) — distinctly warm, deliberately not the cool gray-white that every other AI brand uses. Headlines run a **slab-serif display** ("Copernicus" / Tiempos Headline) at weight 400 with negative letter-spacing, paired with **StyreneB / Inter** body sans. The combination feels like a literary publication, not a SaaS marketing page.

Brand voltage comes from the **cream + coral pairing** — coral (`{colors.primary}` — #cc785c) is the signature Anthropic accent, used on every primary CTA, on the brand wordmark, and on full-bleed callout cards. The coral is warm, slightly muted, never cyan/blue — a deliberate counter-positioning against OpenAI's cool slate, Google's saturated blue, and Microsoft's corporate cyan.

The system has three surface modes that alternate page-by-page:
1. **Cream canvas** (`{colors.canvas}`) — default body floor
2. **Light cream cards** (`{colors.surface-card}`) — feature card backgrounds
3. **Dark navy product surfaces** (`{colors.surface-dark}`) — code editor mockups, model showcase cards, pre-footer CTAs, footer itself

The dark surfaces are where Claude shows its product chrome — code blocks, terminal output, model comparison tables, agentic-flow diagrams. The cream-to-dark contrast is the page's pacing rhythm.

**Key Characteristics:**
- Warm cream canvas (`{colors.canvas}` — #faf9f5) with dark warm-ink text (`{colors.ink}` — #141413). The brand's defining color choice.
- Coral primary CTA (`{colors.primary}` — #cc785c). Used scarcely on individual buttons, generously on full-bleed coral callout cards.
- Slab-serif display headlines via Copernicus / Tiempos Headline at weight 400 with negative letter-spacing. Pairs with humanist sans body for a literary editorial voice.
- Dark navy product mockup cards (`{colors.surface-dark}` — #181715) carrying code blocks, terminal panels, model comparison data — the brand shows the product chrome at scale rather than abstract marketing illustrations.
- Light cream feature cards (`{colors.surface-card}` — #efe9de) — slightly darker than canvas, used for content-driven feature explanations.
- Anthropic radial-spike mark — a small black asterisk-like glyph (4-spoke radial) — appears as the brand wordmark prefix and as a content marker.
- Border radius is hierarchical: `{rounded.md}` (8px) for buttons + inputs, `{rounded.lg}` (12px) for content + product cards, `{rounded.xl}` (16px) for the hero illustration container, `{rounded.pill}` for badges.
- Section rhythm `{spacing.section}` (96px) — modern-SaaS standard. Internal card padding stays generous at `{spacing.xl}` (32px).

## Colors

### Brand & Accent
- **Coral / Primary** (`{colors.primary}` — #cc785c): The signature warm coral. Used on every primary CTA background, on full-bleed coral callout cards, on the brand wordmark accent.
- **Coral Active** (`{colors.primary-active}` — #a9583e): The press / hover-darker variant.
- **Coral Disabled** (`{colors.primary-disabled}` — #e6dfd8): A desaturated cream-tinted disabled state.
- **Accent Teal** (`{colors.accent-teal}` — #5db8a6): Used sparingly on secondary product surfaces.
- **Accent Amber** (`{colors.accent-amber}` — #e8a55a): A small companion warm-tone used on category badges and inline highlights.

### Surface
- **Canvas** (`{colors.canvas}` — #faf9f5): The default page floor. Tinted cream — warm, deliberately not pure white.
- **Surface Soft** (`{colors.surface-soft}` — #f5f0e8): Section dividers, very-soft band backgrounds.
- **Surface Card** (`{colors.surface-card}` — #efe9de): Feature cards, content cards. One step darker than canvas.
- **Surface Cream Strong** (`{colors.surface-cream-strong}` — #e8e0d2): A strongest-cream variant used on selected category tabs and emphasized section bands.
- **Surface Dark** (`{colors.surface-dark}` — #181715): Code editor mockups, model showcase cards, footer. The dominant dark surface.
- **Surface Dark Elevated** (`{colors.surface-dark-elevated}` — #252320): Elevated cards inside dark bands.
- **Surface Dark Soft** (`{colors.surface-dark-soft}` — #1f1e1b): Slightly lighter dark, used for code block backgrounds inside larger dark cards.
- **Hairline** (`{colors.hairline}` — #e6dfd8): The 1px border tone on cream surfaces.
- **Hairline Soft** (`{colors.hairline-soft}` — #ebe6df): Barely-visible divider used inside the same band.

### Text
- **Ink** (`{colors.ink}` — #141413): All headlines and primary text. Warm dark, slightly off-pure-black.
- **Body Strong** (`{colors.body-strong}` — #252523): Emphasized paragraphs, lead text.
- **Body** (`{colors.body}` — #3d3d3a): Default running-text color.
- **Muted** (`{colors.muted}` — #6c6a64): Sub-headings, breadcrumbs, footer-adjacent secondary text.
- **Muted Soft** (`{colors.muted-soft}` — #8e8b82): Captions, fine-print, copyright lines.
- **On Primary** (`{colors.on-primary}` — #ffffff): Text on coral buttons.
- **On Dark** (`{colors.on-dark}` — #faf9f5): Cream-tinted white used on dark surfaces (echoes the canvas tone).
- **On Dark Soft** (`{colors.on-dark-soft}` — #a09d96): Footer body text, secondary labels in dark mockups.

### Semantic
- **Success** (`{colors.success}` — #5db872): Green status dots, "available" indicators.
- **Warning** (`{colors.warning}` — #d4a017): Warning callouts (rare on marketing surfaces).
- **Error** (`{colors.error}` — #c64545): Validation errors.

## Typography

**Display**: Copernicus / Tiempos Headline → Cormorant Garamond at weight 500 with -0.02em letter-spacing is the closest open-source approximation. EB Garamond is a fallback.
**Body**: StyreneB → Inter (humanist sans).
**Code**: JetBrains Mono.

Display sizes use weight 400 (regular), never bold. Negative letter-spacing (-0.3 to -1.5px) is essential — serif without it reads as off-brand.

### Hierarchy

| Token | Size | Weight | Line Height | Letter Spacing |
|---|---|---|---|---|
| display-xl | 64px | 400 | 1.05 | -1.5px |
| display-lg | 48px | 400 | 1.1 | -1px |
| display-md | 36px | 400 | 1.15 | -0.5px |
| display-sm | 28px | 400 | 1.2 | -0.3px |
| title-lg | 22px | 500 | 1.3 | 0 |
| title-md | 18px | 500 | 1.4 | 0 |
| title-sm | 16px | 500 | 1.4 | 0 |
| body-md | 16px | 400 | 1.55 | 0 |
| body-sm | 14px | 400 | 1.55 | 0 |
| caption | 13px | 500 | 1.4 | 0 |
| caption-uppercase | 12px | 500 | 1.4 | 1.5px |
| code | 14px | 400 | 1.6 | 0 |
| button | 14px | 500 | 1.0 | 0 |
| nav-link | 14px | 500 | 1.4 | 0 |

## Layout

- Spacing base: 4px. Tokens: xxs(4) xs(8) sm(12) md(16) lg(24) xl(32) xxl(48) section(96).
- Section padding: 96px.
- Card padding: 32px for feature/pricing/model-comparison cards; 24px for code-window cards.
- Max content width: 1200px centered.
- Hero: 6/6 split (h1 left, illustration/mockup right).
- Feature card grids: 3-up desktop / 2-up tablet / 1-up mobile.

## Elevation & Depth

| Level | Treatment | Use |
|---|---|---|
| Flat | No shadow, no border | Body sections, top nav, hero bands |
| Soft hairline | 1px hairline border | Inputs, sub-nav, occasionally cards |
| Cream card | surface-card background, no shadow | Feature cards, content cards |
| Dark surface | surface-dark background, no shadow | Code mockups, model cards, footer |
| Subtle drop | `0 1px 3px rgba(20,20,19,0.08)` | Rare hover-elevated states |

**Color-block first, shadow rare.** Depth from surface contrast.

## Shapes

| Token | Value | Use |
|---|---|---|
| rounded.xs | 4px | Badge accents, tiny dropdowns |
| rounded.sm | 6px | Small inline buttons, dropdown items |
| rounded.md | 8px | Standard CTAs, text inputs, category tabs |
| rounded.lg | 12px | Content cards (feature, pricing, code-window, model-comparison) |
| rounded.xl | 16px | Hero illustration container, larger marquee components |
| rounded.pill | 9999px | Badge pills, NEW tags |
| rounded.full | 50% | Avatars, icon buttons |

## Components (key ones for the landing)

- **top-nav** — cream nav bar, 64px tall, spike-mark + "ux" wordmark at left, primary menu center, "Sign in" + coral primary CTA right
- **button-primary** — coral background (#cc785c), white text, 14px/500, 40px tall, rounded 8px
- **button-secondary** — cream background, ink text, 1px hairline border
- **button-secondary-on-dark** — surface-dark-elevated background, on-dark text. Stays dark; never inverts.
- **text-link** — inline coral underlined-on-press
- **hero-band** — cream canvas, 6/6 grid: h1 + sub + buttons left, illustration/mockup card right, 96px vertical padding
- **hero-illustration-card** — rounded 16px, cream-canvas OR surface-dark depending on context
- **feature-card** — surface-card background (#efe9de), rounded 12px, 32px padding
- **product-mockup-card-dark** — surface-dark (#181715), rounded 12px, 32px padding — actual product chrome
- **code-window-card** — surface-dark with surface-dark-soft inner code block, JetBrains Mono, line numbers
- **model-comparison-card** — canvas with hairline border, rounded 12px, 32px padding
- **pricing-tier-card** — canvas with hairline; featured tier flips to surface-dark
- **callout-card-coral** — full-bleed coral, white text, rounded 12px, 48px padding — voltage moment
- **badge-coral** — coral fill, white caption-uppercase, rounded pill
- **cta-band-coral** — pre-footer coral fill, 64px padding, white type, cream button
- **cta-band-dark** — alternative pre-footer surface-dark, 64px padding
- **footer** — surface-dark, on-dark-soft text, 4-column links, never inverts

## Pacing & Rhythm

Section sequence: cream → cream-card → dark-mockup → cream → coral-callout → dark-footer. Don't repeat the same surface mode in consecutive bands.

## Do / Don't

### Do
- Anchor every page on cream canvas. Pure white reads as generic.
- Use serif for every display headline. Body in humanist sans.
- Reserve coral for primary CTAs + full-bleed callout cards. Scarce elsewhere.
- Show actual product chrome in dark mockup cards, not abstract illustrations.
- Alternate cream → dark → cream pacing.
- Use Anthropic spike-mark glyph as the wordmark prefix (we'll adapt to a "ux" wordmark + spike-style accent).

### Don't
- No cool grays. No pure white.
- No bold serif display weight — stay at 400.
- No blue/cyan accent — coral is the voltage.
- No serif body. No Inter as the display face.
- No consecutive same-surface bands. Pacing alternates.
- No hover state styling beyond what's encoded — primary darkens on press, nothing else.

## Notes for the landing

- The ux-skill plugin is open-source and is NOT Anthropic's product. The Claude.com aesthetic is a STYLE direction (warm cream + coral + dark editorial). The landing must clearly attribute the plugin to its author (Laith Aljunaidy), not Anthropic.
- Substitute fonts: Cormorant Garamond (weight 500, -0.02em tracking) for serif display + Inter for body + JetBrains Mono for code. Loaded via Google Fonts.
- The radial spike-mark is an Anthropic brand glyph — we don't use it directly. We design our own brand-mark that complements the cream-and-coral palette without copying Anthropic's logo.
