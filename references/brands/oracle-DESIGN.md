# Design System Inspired by Oracle

## 1. Visual Theme & Atmosphere

Oracle's web presence is the database-as-institution brand. The chrome is white, the chromatic anchor is Oracle Red (#c74634) — a specific saturated tomato-brick-red used on the wordmark and CTAs — and the typography is a Roboto-family humanist sans. Where consumer SaaS competitors lean on illustration, motion, and editorial photography, Oracle leans on dense taxonomy navigation, documentation-style chrome, and rectilinear cards with sharp corners. The brand reads as serious enterprise IT — for the customer who is comparing TCO, support tiers, and feature matrices, not for the customer hunting aspiration.

The Oracle Red is the brand's most recognized asset. It is not pure red and it is not coral — it is a saturated brick-tomato hex that, paired with the corporate sans wordmark, instantly reads as Oracle. The CTAs use the red as a solid fill with white text; the wordmark uses it as a solid letter color. Replacing the red with a warmer coral or a "modern" pink is a recognition failure.

The information architecture is dense. The top mega-menu spans Cloud, Database, Java, Applications, Industries, Customers, Resources, Support. Each opens to a multi-level dropdown with 20–40 child items. The density is intentional — Oracle's customers know exactly which product family they want and the chrome serves the experienced enterprise buyer, not the curious first-time visitor.

**Key Characteristics:**
- Oracle Red (#c74634) — the specific brick-tomato chromatic anchor
- Pure white canvas with rectilinear (0–4px radius) cards
- Roboto-family humanist sans across chrome — wide proportions for documentation legibility
- Multi-level mega-menu navigation with dense product taxonomy
- Documentation-style chrome — breadcrumbs, sidebar TOCs, version selectors on most product pages
- No character illustrations, no playful motion, no scroll-triggered reveals

## 2. Color Palette & Roles

### Primary
- **Oracle Red** (`#c74634`): The wordmark color and primary CTA fill. Specific saturated tomato-brick — not pure red, not coral
- **Red Hover** (`#a73e2e`): Slightly darker press state

### Surface & Background
- **Pure White** (`#ffffff`): Page canvas
- **Surface Soft** (`#f7f6f4`): Alternating section bands
- **Hairline** (`#dcdcdc`): 1px card and input borders

### Neutrals & Text
- **Ink** (`#161513`): Primary text — near-black with a slight warm undertone
- **Body** (`#312d2a`): Default body text
- **Muted** (`#5c5c5c`): Captions, breadcrumbs
- **Link** (`#0572ce`): Inline body links — a blue, not red

### Semantic
- **Success** (`#3a8c5f`): Confirmation banners
- **Warning** (`#d4a017`): Caution banners
- **Error** (`#c74634`): Same as brand red — semantic overlap is acceptable

## 3. Typography Rules

### Font Family
- **Display + Body**: `Oracle Sans, Roboto, system-ui, sans-serif` — wide humanist sans, optimized for documentation legibility

### Hierarchy
- **Hero h1** — 42–56px Oracle Sans weight 700, line-height 1.15
- **Section h2** — 32–36px weight 700
- **Card title** — 20–24px weight 600
- **Body** — 16–17px weight 400, line-height 1.5
- **Caption** — 14px weight 400
- **Button label** — 14–16px weight 600

### Principles
- Weight 700 for headlines — the brand's editorial weight
- Body sits at 16–17px for documentation legibility
- Tracking is neutral (0) — no negative tracking at display sizes

## 4. Layout & Spacing

The site uses a 12-column grid with a max content width of 1280–1440px. Section padding is 64–96px vertical. Product card grids run 3-up or 4-up at desktop. Documentation pages use a 3-column layout: left sidebar TOC, center body, right sidebar links.

## 5. Componentry Feel

- **Primary CTA** — Oracle Red fill, white text, 4px radius, 40px height
- **Secondary CTA** — Transparent fill, 1px Oracle Red border, red text, 4px radius
- **Product card (rectilinear)** — White surface, 1px hairline border, 4px radius, internal padding 24px. Title, sub-line, "Learn more" link. Minimal styling
- **Mega-menu** — Multi-column dropdown with 3-tier child lists per category. Background white, 1px border, 4px radius
- **Documentation sidebar** — Hierarchical TOC with expand/collapse rows, current-page indicator (a 2px red bar on the left)
- **Breadcrumb trail** — Slashed-separated path at the top of documentation pages
- **Footer** — Dense multi-column site-map, country/region switcher, copyright row

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use enterprise-formal language ("Optimize your database infrastructure"). Quantify benefit precisely ("Reduce TCO by 35%"). Lead with the technical specification, not the lifestyle promise. Maintain consistency between product family names and acronyms.

**Don't.** Don't write consumer-aspirational copy. Don't use exclamation points. Don't anthropomorphize the database. Don't add playful microcopy in error states.

## 7. Motion Vocabulary

Minimal motion. Hover triggers a 150ms ease on link underlines and a slight 5% darken on CTA fills. Mega-menu drops with a 200ms ease-out. No scroll-triggered reveals on enterprise product pages. The brand reads as serious documentation, not marketing performance.

## 8. Anti-patterns to Avoid

- **Don't soften the rectilinear card radii.** Oracle reads as documentation, not consumer SaaS
- **Don't replace Oracle Red with a "warmer" coral.** The specific brick-red is part of corporate recognition
- **Don't add character illustrations or playful mascots.** Oracle's brand voice is enterprise-formal
- **Don't reduce the mega-menu density.** The multi-level taxonomy is part of the brand's enterprise IA
- **Don't increase radii above 4–8px.** Oracle's rectilinear surfaces are part of the documentation feel
- **Don't add saturated brand-accent gradients.** The chrome stays monochrome + red
- **Don't translate the wordmark.** "Oracle" stays as is across all locales
