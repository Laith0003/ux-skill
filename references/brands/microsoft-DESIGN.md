# Design System Inspired by Microsoft

## 1. Visual Theme & Atmosphere

Microsoft's web presence is the rare design system that has to serve five wildly different product surfaces — consumer Windows, professional Microsoft 365, enterprise Azure, Surface hardware, and gaming Xbox — and stitch them into a single coherent brand. The answer is Fluent 2, the design language that ladders from Windows desktop to web to mobile to mixed reality. On microsoft.com that language reads as institutional, utilitarian, and quietly warm: white canvas, near-monochrome ink ladder, a single chromatic accent (Microsoft Blue, #0067c0), and product photography that brings the color.

The atmosphere is corporate without feeling cold. Surface device renders, Windows desktop screenshots, Teams collaboration photos, and Xbox controllers carry the chromatic warmth — the chrome stays quiet. Cards are rounded at 4–8px (a deliberate softening from the harsher rectilinear surfaces of pre-Fluent Microsoft), and the brand's signature material — acrylic backdrop blur — appears on flyouts, command bars, and sticky navigation. The acrylic gives Microsoft surfaces a recognizable translucent depth that distinguishes them from competitor's flat-card UIs.

The four-square logo (red/green/blue/yellow) is the only multi-chromatic asset in the system. It appears as the brand mark and nothing else — never as a decorative pattern, never as a section divider, never as a background motif. The chromatic restraint is what lets the four-square mark carry real semantic weight when it does appear.

**Key Characteristics:**
- White canvas (#ffffff), near-black ink (#242424), Microsoft Blue (#0067c0) as the single chromatic accent
- Segoe UI Variable as the display + body face — the proprietary system font with a continuous weight axis
- Fluent 2 acrylic backdrop-blur material on flyouts, command bars, sticky chrome
- 4–8px rounded cards with 1px hairline borders — the Fluent surface unit
- Four-square logo as the brand mark; no other multi-color elements anywhere
- Product card grids in 3-up or 4-up — Surface, Microsoft 365, Windows, Xbox feature grids
- Tab "pivot" navigation pattern — flat tabs with a thin colored underline indicator

## 2. Color Palette & Roles

### Primary
- **Microsoft Blue** (`#0067c0`): The single chromatic CTA. Used on primary buttons, on focus rings, and inside the four-square logo. Slightly deeper than peer-tech blues (Google's #4285f4, Facebook's #1877f2) — a deliberate institutional weight

### Surface & Background
- **Pure White** (`#ffffff`): The dominant canvas
- **Surface Soft** (`#faf9f8`): Section divider bands, alternate surfaces
- **Surface Card** (`#f5f5f5`): Hover state on cards, secondary tile backgrounds
- **Hairline** (`#edebe9`): 1px borders on cards and inputs
- **Acrylic Tint** (`rgba(255, 255, 255, 0.7)`): Backdrop-blur material applied to flyouts and sticky chrome

### Neutrals & Text
- **Ink** (`#242424`): Primary text and headlines — a warm near-black
- **Body** (`#424242`): Default body text
- **Muted** (`#616161`): Sub-headings, breadcrumbs
- **Muted Soft** (`#8a8886`): Caption, fine-print, disabled states
- **On Primary** (`#ffffff`): Text on Microsoft Blue CTAs

### Brand Mark
- **Logo Red** (`#f25022`), **Logo Green** (`#7fba00`), **Logo Blue** (`#00a4ef`), **Logo Yellow** (`#ffb900`) — the four-square logo. Appears only on the wordmark, never as decoration

### Semantic
- **Success** (`#107c10`): Status indicators, confirmation banners
- **Warning** (`#ffb900`): Same hex as Logo Yellow — semantic warning
- **Error** (`#c50f1f`): Validation, error banners

## 3. Typography Rules

### Font Family
- **Display + Body**: `Segoe UI Variable, system-ui, -apple-system, sans-serif` — proprietary Microsoft system font with a continuous weight + optical-size axis. Display sizes pull from the heavier optical variant
- **Mono**: `Cascadia Code` — Microsoft's open-source monospace, used in code snippets and terminal mockups

### Hierarchy
- **Hero h1** — 52–64px, Segoe UI Variable Display, weight 600, line-height 1.1, slight negative tracking (-0.5px)
- **Section h2** — 36–42px, Segoe UI Variable Display, weight 600
- **Card title** — 20–22px, Segoe UI Variable Text, weight 600
- **Body** — 16px, Segoe UI Variable Text, weight 400, line-height 1.5
- **Caption** — 14px, Segoe UI Variable Text, weight 400, muted color
- **Button label** — 14–16px, weight 600

### Principles
- Segoe UI's humanist proportions (slight character widening at large sizes, true italics rather than slanted romans) are part of the brand voice — replacing with Inter or a geometric sans flattens the feel
- Weight 600 is the workhorse for headlines and CTAs; weight 700 is reserved for emphasis within body copy
- Display sizes pull from the heavier optical-size variants of the variable face — same family, different optical mastering

## 4. Layout & Spacing

The site runs a 12-column grid with a max content width of 1440px. Hero sections often use a 6-6 split (h1 + sub + CTA on the left, product render on the right) or a 12-col centered headline above a 3- or 4-up product card grid below.

Section padding is 80–96px vertical between major bands — modern-SaaS rhythm but slightly tighter than peers. Card internal padding is 24–32px. The Fluent acrylic material adds a sense of layered depth without using shadows.

## 5. Componentry Feel

- **Product card (Fluent)** — White surface, 1px hairline border, 4–8px radius, internal padding 24px. Title, sub-line, product render, "Learn more" link. No shadow at rest; hover lifts surface to `#f5f5f5`
- **Primary CTA** — Solid Microsoft Blue fill, white text, 4px radius (or 16px for the pill variant), 40px height, weight-600 label
- **Secondary button** — Transparent fill, 1px Microsoft Blue border, blue text, same dimensions
- **Acrylic flyout** — Floating panel with `backdrop-filter: blur(40px) saturate(180%)` over `rgba(255,255,255,0.7)`. Signature Fluent material
- **Command bar** — Top utility bar with grouped action buttons (download, share, edit) — flat, no border, slight separator hairlines
- **Tab pivot** — Flat tab labels with a 2px Microsoft Blue underline on the active tab. No card-style tabs
- **Hero product render** — Surface device or Windows screenshot, rendered with a soft shadow, often offset slightly off-axis for editorial feel
- **Footer** — Dark gray (#242424 or near) with white links in a multi-column site-map layout. The Microsoft wordmark + four-square logo top-left

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use direct corporate-but-friendly language ("Get started", "Learn more", "Compare plans"). Quantify product capability ("AI-powered insights across 200+ data sources"). Treat Microsoft 365, Azure, Windows as proper nouns. Lead with the customer's job, not the product's features.

**Don't.** Don't write corporate-speak ("Empower your organization to leverage…"). Don't abbreviate Microsoft to "MSFT" outside of finance contexts. Don't use exclamation points in chrome. Don't market gaming with the same voice as enterprise.

## 7. Motion Vocabulary

Fluent 2 motion is gentle and functional. Transitions run 200–250ms with a cubic-bezier ease-in-out. Card hover triggers a 1.02 scale-up over 150ms. Flyouts open with a slight slide-down + fade-in (200ms). The acrylic-blur material has its own implicit motion — the blurred content behind the panel scrolls slightly out of focus as the flyout opens.

## 8. Anti-patterns to Avoid

- **Don't replace Segoe UI with Inter or geometric sans.** The humanist proportions are core to the Fluent feel
- **Don't make the four-square logo decorative.** It is the mark, not a pattern. Painting cards in red/green/blue/yellow breaks the brand
- **Don't add a second brand accent color.** Microsoft Blue is the only chromatic CTA color in the chrome
- **Don't ignore the acrylic-blur material.** Flat translucent overlays read as off-brand; the saturated blur is signature
- **Don't sharpen card corners to 0px.** Fluent's 4–8px radius is a deliberate softening of pre-Fluent rectilinear surfaces
- **Don't use deep drop shadows.** Depth comes from acrylic blur and surface tint, not from heavy elevation
- **Don't run hero h1 at weight 700.** Weight 600 is the brand standard; 700 reads as bombastic
