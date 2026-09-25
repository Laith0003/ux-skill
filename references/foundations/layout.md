# Layout

> Layout is the architecture of attention. Reading order, visual rhythm, and asymmetry are what distinguish a designed page from a templated one.

## Principles

1. **Landing-page structure lives in its playbook.** AIDA is the default framing for landing pages, and it, the hero, the logo wall, the final CTA and the footer are specified in `references/surfaces/landing.md`. This file holds the layout mechanics every surface shares: containers, grids, bento, rhythm and collapse. Page hierarchy must announce itself without reading.

2. **Ultra-wide containers prevent H1 failure** — H1 containers at `max-w-5xl`, `max-w-6xl`, or `w-full`. Narrow containers cause 6-line wraps and reflexive failure. The width prevents the wrap, not the font size alone.

3. **H1 line limit.** The limit lives in `references/surfaces/landing.md` (Hero composition). Ultra-wide containers (principle 2) are how a page meets it.

4. **Center by choice, never by fallback.** When a hero may be centered is a landing rule (`references/surfaces/landing.md`, Hero bans). Elsewhere, center a block only when the composition calls for it; a centered-everything page is the fallback this rule bans.

5. **Asymmetric beats symmetric** — Use fractional grid columns (`2fr 1fr 1fr`) instead of `grid-cols-3`. Use 7/5 or 5/7 splits, not 6/6. Asymmetry creates hierarchy without needing different sizes of typography.

6. **Mobile-first, scale up** — Design for 375px first. Layer up through tablet (768), laptop (1024), desktop (1440). Never the reverse. High-variance desktop layouts collapse aggressively below 768px.

7. **Grid over flex-math** — Use CSS Grid for responsive structures, especially bento layouts. Flex percentage math (`w-[calc(33%-1rem)]`) is banned — Grid wins on responsive, gap consistency, and dense flow.

8. **`grid-flow-dense` on bento layouts.** Asymmetric bento grids fill empty cells. No missing corners, no dead space. The card count lives in `references/surfaces/landing.md` (When to include a section).

9. **Section spacing creates chapters** — Each section feels like a distinct cinematic chapter. Marketing sections at `py-32 md:py-48` minimum; premium at `py-40 md:py-56`. Cramming kills editorial energy.

10. **Conventions over cleverness for navigation** — Logo top-left. Nav top or left. Search = magnifying glass. Innovate when you have a better idea; otherwise honor convention so users can scan.

11. **No 3-column equal card layouts** — The generic 3-equal-cards feature row is banned. Use 2-column zig-zag, asymmetric grid, masonry, or horizontal scroll.

12. **Mobile collapse is aggressive** — Any asymmetric layout above `md:` must fall back to `w-full px-4 py-8` strict single-column below 768px. No `col-span` overrides survive. Horizontal scrollbars from off-screen animations are a critical failure.

## Do / Don't

| Do | Don't |
|---|---|
| Use `min-h-[100dvh]` for full-height sections | Use `h-screen` (breaks on iOS Safari address bar collapse) |
| Wrap `max-w-7xl` or `max-w-[1400px]` outer container | Let content stretch full-width on 2560px ultrawide |
| Use `max-w-5xl` or wider for H1 containers | Cram H1 inside `max-w-2xl` |
| Apply `py-32 md:py-48` to marketing sections | Apply `py-12` to marketing sections (looks cheap) |
| Use CSS Grid for layout | Use flex percentage math like `w-[calc(33%-1rem)]` |
| Use fractional grid columns (`2fr 1fr 1fr`) for asymmetry | Use `grid-cols-3` for every feature row |
| Use `grid-flow-dense` on bento | Leave empty cells in bento grids |
| Wrap page in `overflow-x-hidden w-full max-w-full` when motion is used | Allow horizontal scroll on mobile |
| Alternate image-left / image-right between feature sections | Use the same orientation for every feature row |
| Allow macro-typography to bleed past viewport edges (brutalist) | Force macro-headlines into rigid container widths |
| Use asymmetric two-column splits (7/5 or 5/7) | Default to 6/6 splits |
| Use bottom tab bar for top-level nav on small screens | Mix top, bottom, and side nav at the same hierarchy level |
| Cap bottom nav at 5 items with icon + text label | Cram 6+ items into bottom nav |
| Reserve drawer/sidebar for secondary nav, not primary actions | Hide primary actions in a drawer |
| Mobile fall back to single-column below 768px | Stack desktop column proportions on mobile |

## Examples

Landing-page patterns (AIDA structure, section order, hero composition and hero paradigms, the logo wall, the final CTA and the footer) live in `references/surfaces/landing.md`.

### Pattern: Bento grid (modern SaaS)
**Use when**: Feature showcases, dashboards, "what's in the box" sections.
**Anti-pattern**: 3-column equal cards row (banned).
**How**: Cards in varying sizes (one tall, one wide, the rest square), in the count `references/surfaces/landing.md` (When to include a section) sets. Use CSS Grid with `grid-flow-dense` and fractional spans. Common arrangement: Row 1 with 3 columns, Row 2 with 2 columns split 70/30. Premium versions use `rounded-[2rem]` to `rounded-[2.5rem]` for major containers with diffusion shadows.

### Pattern: Z-axis cascade (high-end aesthetic)
**Use when**: Premium marketing surfaces where depth communicates craftsmanship.
**Anti-pattern**: Cards in flat grid with no depth.
**How**: Elements stack like physical cards, slightly overlapping with varying depths. Some cards carry subtle `-2deg` or `3deg` rotation to break the digital grid. Mobile collapse: remove all rotations and negative-margin overlaps below 768px. Stack vertically with standard spacing.

### Pattern: Editorial split (premium)
**Use when**: Marketing pages targeting design-literate audiences.
**Anti-pattern**: Symmetrical text-left, image-right that never alternates.
**How**: Massive typography on one half of the viewport, interactive cards or horizontal-scroll image rails on the other half. Mobile collapse: full-width vertical stack. Typography block sits on top; interactive content flows below, with horizontal scroll preserved if essential to the experience.

### Pattern: Asymmetric two-column zigzag
**Use when**: Long-form landing pages with 3 to 6 feature sections.
**Anti-pattern**: Same image-left, text-right orientation for every feature row.
**How**: Alternate text-left/image-right then text-right/image-left section to section. Use 7/5 or 5/7 splits, not 6/6. Don't repeat the same orientation more than twice in a row. The alternation is the rhythm.

### Pattern: Three product pillars
**Use when**: Compressing a wide surface area into a memorable triad.
**Anti-pattern**: 8 thin feature tiles competing for attention.
**How**: Group products into three pillars, each presented as an equally weighted card or column. If the company has more than three core capabilities, find the meta-categorisation that compresses them into three. Three pillars is the memorability number.

### Pattern: Sticky scroll-pinned product walk
**Use when**: A single feature needs to support 3 to 6 visual states without 3 to 6 separate sections.
**Anti-pattern**: Six near-identical feature sections, each with the same product screenshot in different states.
**How**: A short headline + bullet list pins on the left while a stack of product screenshots scrolls past on the right, swapping in at scroll triggers. Frame 1: empty state. Frame 2: user types. Frame 3: result appears. Frame 4: AI responds. Couples narrative with motion without requiring autoplay.

### Pattern: Brutalist edge-bleed macro-typography
**Use when**: Industrial, technical, anti-mainstream aesthetic.
**Anti-pattern**: Containing brutalist headlines inside a polite SaaS max-width.
**How**: Macro-typography is allowed and encouraged to bleed past viewport edges, cropping a numeral or letter. Reinforces the "this is a printed plate" feeling. Use fluid clamps like `clamp(4rem, 10vw, 15rem)` so headlines visibly press against viewport edges. Push macro-headlines to one rail; cluster telemetry tight against the opposite edge.

### Pattern: Adaptive navigation
**Use when**: Cross-platform products needing both mobile and desktop nav.
**Anti-pattern**: Tab bar on desktop or sidebar on mobile.
**How**:
- ≥1024px: prefer sidebar for primary nav
- 768 to 1023px: top app bar with hamburger or condensed nav
- <768px: bottom tab bar (≤5 items) for top-level navigation; top app bar acceptable for non-app marketing surfaces
- Persistent core nav reachable from deep pages
- Current location visually highlighted (color, weight, indicator bar)

### Pattern: Sticky transparent-to-opaque nav
**Use when**: Long-scroll marketing pages.
**Anti-pattern**: Sticky nav with solid background fighting the hero on first paint.
**How**: On page load, nav has no fill — hero gradient bleeds through. After ~100px scroll, a backdrop-blur or solid fill kicks in (slight transition over 150 to 200ms). The effect is "the nav was always there, but politely." A hairline bottom border appears with the scroll state.

### Pattern: Floating glass pill nav (premium)
**Use when**: High-end premium marketing surfaces.
**Anti-pattern**: Edge-to-edge sticky navbar glued to viewport top.
**How**: Floating glass pill detached from the viewport top with substantial top margin. Pill content includes the brand mark, a small set of primary links, and a primary CTA. On scroll past the hero, the pill darkens or its backdrop blur intensifies — but it never glues to the edge.

### Pattern: Adaptive container insets
**Use when**: Layouts that span 375px to 1440px+.
**Anti-pattern**: Same `px-4` from phone to desktop — wide screens cramped.
**How**:
- Mobile: `px-4` (16px outer)
- Tablet: `px-8` (32px)
- Desktop: `px-12` (48px), or rely on `max-w-7xl mx-auto` to center
- Landscape phones treated as tablets for gutter purposes

### Pattern: Scroll-pinned product walk
**Use when**: A single feature supporting 3 to 6 visual states without 3 to 6 separate sections.
**Anti-pattern**: Six near-identical sections with the same screenshot in different states.
**How**: A short headline + bullet list pins on the left while a stack of product screenshots scrolls past on the right, swapping in at scroll triggers. Frame 1: empty state. Frame 2: user types. Frame 3: result appears. Frame 4: AI responds. Mobile collapse: vertical stack with one image per frame, no pinning.

### Pattern: Templates and gallery section
**Use when**: Creative tools, design platforms, or any product with user-generated artifacts.
**Anti-pattern**: Burying templates and example projects in a separate page.
**How**: A "see what people made" or template-grid section roughly 70% down the page. Horizontal-scroll carousel of starting points lets users see "what I could make" before committing. Hover-reveals creator names. Refreshed regularly as a living asset.

### Pattern: Integrations / ecosystem section
**Use when**: Products with rich third-party ecosystem.
**Anti-pattern**: Listing 50 integrations as identical small tiles.
**How**: A grid of partner logos with one-line use cases ("Sync with X", "Export to Y") in the lower third of the page, after features, before pricing. Demonstrates ecosystem without being the centerpiece. Logos rendered in monochrome treatment matching the rest of the chrome.

### Pattern: Sticky in-page nav (long pages)
**Use when**: Long marketing pages with multiple major sections.
**Anti-pattern**: Forcing users to scroll up to reorient.
**How**: Once the user scrolls past the hero, a thin secondary nav pins to the top with section anchors (Overview, Features, Pricing, FAQ). Quietly providing a TOC without forcing it. Closes when user scrolls back into hero.

### Pattern: What's-new badge in nav
**Use when**: Products with active development and returning visitors.
**Anti-pattern**: Recent changes buried in a blog the user never visits.
**How**: Top-nav includes a "What's new" item with a small dot or badge for recency. Signals active development and gives returning visitors a destination. The badge clears when the user clicks. Pair with a brief release note or changelog.

### Pattern: Status indicator in footer
**Use when**: Any operationally-mature product.
**Anti-pattern**: Burying uptime data on a separate status site.
**How**: A small green dot + "all systems operational" link to the status page, in the footer or quietly in nav. Tiny but powerful trust signal. Performed transparency.

## Tokens / values

### Container widths
- Outer container: `max-w-7xl mx-auto` (1280px) or `max-w-[1400px] mx-auto`
- Cap above which the page just centers: 1400px
- Prose / text columns: `max-w-prose` or `max-w-[65ch]` (~640 to 720px)
- Hero H1 container: `max-w-5xl` to `max-w-7xl` (1024 to 1280px) or wider
- Visual containers: `max-w-5xl` to `max-w-7xl` (1024 to 1280px)
- Full-bleed sections: `w-screen` for backgrounds; content inside still respects max-width

### Breakpoints
- 375px: small phone
- 414px: large phone
- 768px: tablet (`md:`)
- 1024px: laptop (`lg:`)
- 1280px: desktop (`xl:`)
- 1440px: wide desktop (`2xl:`)
- Cap layouts at 1400px

### Section padding (marketing)
- Default: `py-32 md:py-48` (128px / 192px)
- Premium: `py-40 md:py-56` (160px / 224px)
- Editorial: `py-32 md:py-48`
- Final CTA: `py-32 md:py-48` with tinted background band
- Mobile minimum: `py-16` (64px)

### Grid systems
- Default symmetrical: `grid grid-cols-1 md:grid-cols-3 gap-6`
- Asymmetric fractional: `grid-template-columns: 2fr 1fr 1fr`
- Bento dense: `grid-flow-dense` with mixed `col-span` and `row-span`
- 12-column underlying grid for editorial layouts
- Inside the grid, content modules at 8 of 12 columns is common; outer columns provide breathing room

### Section vertical rhythm
- Hero: `min-h-[100dvh]` with centered or split content
- Feature pillars: `py-32 md:py-48`
- Logo strip: `py-12 md:py-16` (sparser)
- FAQ: `py-24 md:py-32`
- Final CTA: `py-32 md:py-48` with band background

### Bento layout
- Card count: see `references/surfaces/landing.md` (When to include a section)
- Card sizes: vary — one tall, one wide, one or two square
- Common arrangement: Row 1 with 3 columns, Row 2 with 2 columns split 70/30
- Card radii: `rounded-[2rem]` to `rounded-[2.5rem]` for premium
- Card padding: `p-6` to `p-10` depending on density
- Gap: `gap-4` to `gap-6`

### Mobile collapse rules (VARIANCE > 4)
- Below 768px: any asymmetric layout collapses to `w-full px-4 py-8` single-column
- Below 768px: bento `col-span` overrides do not survive
- Below 768px: z-axis cascades flatten (no rotations, no negative-margin overlaps)
- Below 768px: density caps at "daily-app"
- Below 768px: motion intensity reduces by 2 levels
- Below 768px: horizontal scrollbars from off-screen animations are critical failure

### Navigation rules
- Bottom nav (mobile): ≤5 items, icon + text label
- Top app bar (Android-style or marketing): full-width, persistent
- Sidebar: secondary nav, not primary actions
- Breadcrumb: 3+ level deep hierarchies on web
- Mega-menu: hover-revealed nav panels with multi-column groupings by job-to-be-done
- Nav state active: color, weight, or indicator bar highlight
- Persistent core nav reachable from deep pages
- Destructive actions (delete account, logout) visually and spatially separated from normal nav items
- Skip-to-main-content link as first focusable element on web pages with significant chrome

### Banned layout patterns
- `h-screen` (use `min-h-[100dvh]`)
- Flex percentage math (use Grid)
- 3-column equal card feature rows
- Center-everything fallback at VARIANCE > 4
- Bento grids with empty cells (use `grid-flow-dense`)
- Cramped sections (`py-12` on marketing)
- Horizontal scroll on mobile body content
- Tab bar + sidebar + bottom nav at the same hierarchy level
- Bottom nav with 6+ items
- Bottom nav locations changing between pages
- Mega-menus that require hovering through 3 levels
- Mystery-meat icon-only navigation

### Anti-AI defaults
- No centered-everything as fallback
- No "purple gradient AI" hero backgrounds
- No "Acme / Nexus" filler brand names
- No 3-equal-card feature grids
- No edge-to-edge floating elements with awkward gaps (mathematics must be perfect)

## Checklist (severity-tagged)

- [ ] Hero uses `min-h-[100dvh]`, never `h-screen` (severity: Critical)
- [ ] H1 container is `max-w-5xl` or wider (severity: Critical)
- [ ] H1 within the line limit in `references/surfaces/landing.md` (Hero composition) (severity: Critical)
- [ ] Outer container caps at `max-w-7xl` or `max-w-[1400px]` (severity: Medium)
- [ ] Page wrapped in `overflow-x-hidden w-full max-w-full` if motion is used (severity: Critical)
- [ ] No horizontal scroll on mobile body content (severity: Critical)
- [ ] CSS Grid used for layout; no flex percentage math (severity: High)
- [ ] Bento grids use `grid-flow-dense`; no empty cells (severity: High)
- [ ] Bento card count follows `references/surfaces/landing.md` (When to include a section) (severity: Medium)
- [ ] No 3-equal-card feature rows (severity: High)
- [ ] Marketing sections use `py-32 md:py-48` minimum (severity: High)
- [ ] Sections feel like distinct cinematic chapters, not cramped slabs (severity: Medium)
- [ ] Asymmetric layouts collapse to single-column below 768px (severity: Critical)
- [ ] Verified at 375px, 768px, 1024px, 1440px (severity: Critical)
- [ ] Center-everything fallback used intentionally, not by default (severity: High)
- [ ] Landing pages pass the checklist in `references/surfaces/landing.md` (hero, logo wall, final CTA, footer) (severity: High)
- [ ] Alternating image-left / image-right on feature sections (severity: Medium)
- [ ] Bottom nav (mobile) capped at 5 items with icon + text label (severity: High)
- [ ] Persistent core nav reachable from deep pages (severity: Medium)
- [ ] Status indicator in footer (green dot + status page link) (severity: Cosmetic)
- [ ] Adaptive horizontal gutters by breakpoint (severity: Medium)
- [ ] Safe areas respected for status bar, notch, home indicator (severity: Critical for mobile)
- [ ] No `z-50` or `z-[9999]` spam; z-index documented for systemic layers only (severity: Medium)
- [ ] Skip-to-main-content link as first focusable element on web pages (severity: High)
- [ ] No multiple gradient sections on a single page (severity: Medium)
- [ ] No "SECTION 01" / "QUESTION 05" meta-labels (severity: High)

## Related

- See **typography.md** for ultra-wide containers that prevent H1 line failure.
- See **spacing.md** for section padding tokens and density modes.
- See **interaction.md** for navigation touch targets and tap feedback.
- See **accessibility.md** for skip-links, heading hierarchy, and orientation support.
- See **motion.md** for scroll-triggered reveals and pinned-section choreography.
- See `references/surfaces/landing.md` for landing-page structure: AIDA, hero, logo wall, final CTA and footer.
- See `references/surfaces/dashboard.md` for data-dense layout density and how the live-product archetypes in `references/styles/arsenal.md` combine on a dashboard.
- See **components.md** for navbar, modal, and bento card contracts.
