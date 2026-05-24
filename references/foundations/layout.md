# Layout

> Layout is the architecture of attention. Reading order, visual rhythm, and asymmetry are what distinguish a designed page from a templated one.

## Principles

1. **AIDA is the spine of landing pages** — Attention (hero) → Interest (features) → Desire (motion / proof / outcomes) → Action (final CTA). Every landing page follows this sequence. Page hierarchy must announce itself without reading.

2. **Ultra-wide containers prevent H1 failure** — H1 containers at `max-w-5xl`, `max-w-6xl`, or `w-full`. Narrow containers cause 6-line wraps and reflexive failure. The width prevents the wrap, not the font size alone.

3. **2-line H1 rule** — H1 never exceeds 2 to 3 lines at any breakpoint from 375px to 1440px. 4 lines is failure; 5 is catastrophic; 6 is disqualifying.

4. **Anti-center bias** — Centered hero sections used as a fallback are banned at DESIGN_VARIANCE > 4. Force split-screen, left-aligned-content-with-right-asset, or asymmetric whitespace. Center only intentionally with massive width.

5. **Asymmetric beats symmetric** — Use fractional grid columns (`2fr 1fr 1fr`) instead of `grid-cols-3`. Use 7/5 or 5/7 splits, not 6/6. Asymmetry creates hierarchy without needing different sizes of typography.

6. **Mobile-first, scale up** — Design for 375px first. Layer up through tablet (768), laptop (1024), desktop (1440). Never the reverse. High-variance desktop layouts collapse aggressively below 768px.

7. **Grid over flex-math** — Use CSS Grid for responsive structures, especially bento layouts. Flex percentage math (`w-[calc(33%-1rem)]`) is banned — Grid wins on responsive, gap consistency, and dense flow.

8. **`grid-flow-dense` on bento layouts** — Asymmetric bento grids fill empty cells. No missing corners, no dead space. 3 to 5 intentional cards beat 8 messy ones every time.

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
| Build 3 to 5 intentional bento cards | Cram 8+ cards into one bento section |
| Wrap page in `overflow-x-hidden w-full max-w-full` when motion is used | Allow horizontal scroll on mobile |
| Alternate image-left / image-right between feature sections | Use the same orientation for every feature row |
| Allow macro-typography to bleed past viewport edges (brutalist) | Force macro-headlines into rigid container widths |
| Use asymmetric two-column splits (7/5 or 5/7) | Default to 6/6 splits |
| Use bottom tab bar for top-level nav on small screens | Mix top, bottom, and side nav at the same hierarchy level |
| Cap bottom nav at 5 items with icon + text label | Cram 6+ items into bottom nav |
| Reserve drawer/sidebar for secondary nav, not primary actions | Hide primary actions in a drawer |
| Mobile fall back to single-column below 768px | Stack desktop column proportions on mobile |

## Examples

### Pattern: AIDA landing structure
**Use when**: Any marketing landing page.
**Anti-pattern**: 12 unstructured sections, no clear hero, multiple competing CTAs.
**How**:
1. Premium navigation bar (floating glass pill, minimal split nav) — first paint.
2. **Attention** — hero with ultra-wide H1, 2 to 3 lines max, 2 high-contrast CTAs.
3. **Interest** — bento grid or interactive typographic component density.
4. **Desire** — motion / scroll-driven section (pinned, scrubbed, stacked).
5. **Action** — high-contrast CTA + clean footer.

### Pattern: Canonical premium SaaS section flow
**Use when**: B2B marketing pages, enterprise tools, developer surfaces.
**Anti-pattern**: 20 sections with random order, no narrative arc.
**How**:
1. Hero (one-line value-prop + one-line sub + 1 or 2 CTAs + product image or motion)
2. Social proof strip (logo marquee, single row, monochrome)
3. Problem framing or "old way vs new way"
4. Core feature pillars (3 to 4, alternating image-left, image-right)
5. "How it works" — numbered step sequence (3 to 5 steps)
6. Use-case or persona section (tabbed switcher or carousel)
7. Outcome / ROI (customer quote + headline metric)
8. Trust & security (compliance badges + paragraph)
9. FAQ (5 to 8 questions, accordion-collapsed) — optional, above final CTA
10. Final CTA section (restated value-prop, single filled CTA, tinted band)
11. Footer (navigation + secondary links + small print)

### Pattern: Hero composition
**Use when**: Any hero landing.
**Anti-pattern**: Carousel hero with 4 rotating slides, or 5+ CTAs in the hero.
**How**: One headline, one sub-paragraph, one or two CTAs, one product image or short motion. No carousel, no slideshow, no rotating taglines. Premium pages do not hedge. Asymmetric hero with product image right-aligned, copy left-aligned (or reversed). A "headline / sub / two CTAs" stack: primary action filled, secondary action ghost or text-link.

### Pattern: Hero paradigms — choose one
**Use when**: Picking the structural variant for the hero.
**Anti-pattern**: Reflexive left-text-right-image default with no variant chosen.
**How**:
- **Cinematic Center (preferred default)** — text perfectly centered, massive width, ultra-wide H1 container, two high-contrast CTAs below, stunning full-bleed background with dark radial wash.
- **Artistic Asymmetry** — text offset left, artistic floating image overlapping from bottom right, generous negative space.
- **Editorial Split** — text left, image right, massive negative space between (60/40 or 65/35, not 50/50).
- **Asymmetric Hero with Stylistic Fade** — high-quality background image with subtle stylistic fade (darkening or lightening into the page background), text aligned cleanly left or right.

### Pattern: Bento grid (modern SaaS)
**Use when**: Feature showcases, dashboards, "what's in the box" sections.
**Anti-pattern**: 3-column equal cards row (banned).
**How**: 3 to 5 intentional cards in varying sizes — one tall, one wide, one or two square. Use CSS Grid with `grid-flow-dense` and fractional spans. Common arrangement: Row 1 with 3 columns, Row 2 with 2 columns split 70/30. Premium versions use `rounded-[2rem]` to `rounded-[2.5rem]` for major containers with diffusion shadows.

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

### Pattern: Logo marquee under hero
**Use when**: Social proof immediately after the hero.
**Anti-pattern**: A row of full-color logos at native pixel heights.
**How**: 6 to 10 customer logos in a single grayscale or monotone treatment. Single horizontal row, evenly weighted (adjusted per logo so they read evenly, not at native pixel heights). Often with a small eyebrow ("Trusted by teams at," "Used by"). Auto-scrolling marquees cycle 20 to 60 seconds; pause on hover.

### Pattern: Brutalist edge-bleed macro-typography
**Use when**: Industrial, technical, anti-mainstream aesthetic.
**Anti-pattern**: Containing brutalist headlines inside a polite SaaS max-width.
**How**: Macro-typography is allowed and encouraged to bleed past viewport edges, cropping a numeral or letter. Reinforces the "this is a printed plate" feeling. Use fluid clamps like `clamp(4rem, 10vw, 15rem)` so headlines visibly press against viewport edges. Push macro-headlines to one rail; cluster telemetry tight against the opposite edge.

### Pattern: Final CTA section
**Use when**: Closing the page after objections are resolved.
**Anti-pattern**: FAQ noise after the final CTA, or email capture wall before the close.
**How**: The page ends with a quiet, restated value-prop in one line and a single filled CTA, centered. On a slightly tinted background or full-dark band. FAQs (when present) live ABOVE the final CTA, not below. The footer follows the CTA but is a separate visual concern.

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

### Pattern: Pre-footer full-bleed CTA
**Use when**: Creative-tool and premium SaaS marketing surfaces.
**Anti-pattern**: A small CTA buried at the bottom of the page.
**How**: Before the footer, a horizontal band in the brand's strongest color carries one headline, one CTA. Full-bleed background, centered content. The hero held back; the closer doesn't. This is the page's loudest moment and earns it by being last.

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

### Pattern: Dense multi-column footer
**Use when**: Compensating for narrative-led upper sections.
**Anti-pattern**: A thin one-row footer with a single copyright line.
**How**: 4 to 6 columns of links organized by audience (Product, Solutions, Resources, Company, Legal). Each column 4 to 8 links. Includes language picker, social icons, wordmark, status indicator. The dense footer is the page's apology for being narrative-led above. The newsletter signup, if present, goes above the sitemap.

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

### Hero structures
- Cinematic Center: ultra-wide H1, two high-contrast CTAs, full-bleed background
- Artistic Asymmetry: text offset left, image overlapping from bottom right
- Editorial Split: text left, image right, 60/40 or 65/35 split
- Asymmetric with Stylistic Fade: high-quality background image with subtle fade
- Above-the-fold density: low — nothing else fights for attention

### Hero composition rules
- Single CTA pair: primary filled + secondary ghost or text-link
- Two filled CTAs of equal weight is banned (dilutes primary path)
- No more than 2 CTAs above the fold
- No floating stamp / badge icons on hero text
- No pill-tags under the hero
- No raw stats in the hero (move to dedicated stat section)
- One claim, one supporting line, one call to action

### Section vertical rhythm
- Hero: `min-h-[100dvh]` with centered or split content
- Feature pillars: `py-32 md:py-48`
- Logo strip: `py-12 md:py-16` (sparser)
- FAQ: `py-24 md:py-32`
- Final CTA: `py-32 md:py-48` with band background

### Bento layout
- Card count: 3 to 5 (not 8)
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

### Footer structure
- Multi-column: 4 to 8 columns of links organized by audience (Product, Solutions, Resources, Company, Legal)
- Language picker, social icons, wordmark
- Status indicator: small green dot + "all systems operational" link to status page
- Address and a single legal line; no more
- Newsletter signup (if present): above the sitemap, not at the absolute foot
- Footer takes a slightly darker or lighter band than the page

### Banned layout patterns
- `h-screen` (use `min-h-[100dvh]`)
- Flex percentage math (use Grid)
- 3-column equal card feature rows
- Center-everything fallback at VARIANCE > 4
- Reflexive left-text-right-image default hero
- Bento grids with empty cells (use `grid-flow-dense`)
- 8+ cards in a single bento grid
- Cramped sections (`py-12` on marketing)
- Horizontal scroll on mobile body content
- Floating stamp / badge icons on hero text
- Pill-tags directly under the hero
- Raw stats / data dumped in the hero
- Tab bar + sidebar + bottom nav at the same hierarchy level
- Bottom nav with 6+ items
- Bottom nav locations changing between pages
- Mega-menus that require hovering through 3 levels
- Mystery-meat icon-only navigation
- Footer thin (one row) — must be sitemap-dense

### Anti-AI defaults
- No centered-everything as fallback
- No "purple gradient AI" hero backgrounds
- No "Acme / Nexus" filler brand names
- No 3-equal-card feature grids
- No reflexive left-text-right-image hero
- No edge-to-edge floating elements with awkward gaps (mathematics must be perfect)

### Hero metric callouts
- Used when a single number is part of the proof
- Animated counter ticks up from 0 on entry (once, then static)
- 2 to 3 stats max per section; more dilutes the effect
- Tabular figures so layout does not shift during count-up
- Numbers in mono variant for engineering credibility
- Eyebrow above the stat ("Customers," "Documents/day," "Users")

### "Built for X" sub-positioning
- A small line under the hero ("Built for finance," "Built for sales teams")
- Pre-qualifies the visitor in one breath
- Reduces bounce — visitor immediately knows whether they're in the right place
- Appears beneath or to the side of the H1, never above (eyebrow has that slot)

### Section flow primitives (premium SaaS canonical)
1. Hero — one-line value-prop + one-line sub + 1 or 2 CTAs + product image or motion
2. Logo strip — monochrome, single row, after hero
3. Problem framing / "old way vs new way" — short comparison
4. Core feature pillars — 3 to 4, alternating image-left, image-right
5. "How it works" — numbered 3 to 5 step sequence
6. Use-case / persona section — tabbed switcher or carousel
7. Outcome / ROI — customer quote + headline metric
8. Trust & security — compliance badges + paragraph
9. FAQ — 5 to 8 questions, accordion-collapsed (optional)
10. Final CTA — restated value-prop, single filled CTA, tinted band
11. Footer — dense multi-column sitemap

### Logo wall repetition
- A single mid-page logo strip is more credible than three
- Optional: repeat the wall 2 to 3x at strategic points (after hero, mid-page, before close) to compound trust without overloading any one section
- Each appearance uses identical treatment (monochrome, uniform optical height, generous gutters)
- Mark the wall with an eyebrow ("Trusted by," "Used by teams at") for one of the appearances; subsequent appearances are unframed

## Checklist (severity-tagged)

- [ ] Hero uses `min-h-[100dvh]`, never `h-screen` (severity: Critical)
- [ ] H1 container is `max-w-5xl` or wider (severity: Critical)
- [ ] H1 never exceeds 2 to 3 lines at any breakpoint (375px to 1440px) (severity: Critical)
- [ ] Outer container caps at `max-w-7xl` or `max-w-[1400px]` (severity: Medium)
- [ ] Page wrapped in `overflow-x-hidden w-full max-w-full` if motion is used (severity: Critical)
- [ ] No horizontal scroll on mobile body content (severity: Critical)
- [ ] AIDA structure followed on landing pages (Attention → Interest → Desire → Action) (severity: High)
- [ ] CSS Grid used for layout; no flex percentage math (severity: High)
- [ ] Bento grids use `grid-flow-dense`; no empty cells (severity: High)
- [ ] Bento card count is 3 to 5, not 8 (severity: Medium)
- [ ] No 3-equal-card feature rows (severity: High)
- [ ] Marketing sections use `py-32 md:py-48` minimum (severity: High)
- [ ] Sections feel like distinct cinematic chapters, not cramped slabs (severity: Medium)
- [ ] Asymmetric layouts collapse to single-column below 768px (severity: Critical)
- [ ] Verified at 375px, 768px, 1024px, 1440px (severity: Critical)
- [ ] One primary CTA per section, one filled + one ghost in hero (severity: High)
- [ ] No floating stamp / badge icons on hero text (severity: Medium)
- [ ] No pill-tags under the hero (severity: Medium)
- [ ] No raw stats in the hero (severity: Medium)
- [ ] Center-everything fallback used intentionally, not by default (severity: High)
- [ ] Alternating image-left / image-right on feature sections (severity: Medium)
- [ ] Bottom nav (mobile) capped at 5 items with icon + text label (severity: High)
- [ ] Persistent core nav reachable from deep pages (severity: Medium)
- [ ] Logo marquee under hero is monochrome at uniform optical height (severity: Medium)
- [ ] Final CTA section on tinted band, single filled CTA (severity: Medium)
- [ ] FAQs sit above the final CTA, never below (severity: Cosmetic)
- [ ] Footer is dense multi-column sitemap, not a thin one-row strip (severity: Medium)
- [ ] Status indicator in footer (green dot + status page link) (severity: Cosmetic)
- [ ] Adaptive horizontal gutters by breakpoint (severity: Medium)
- [ ] Safe areas respected for status bar, notch, home indicator (severity: Critical for mobile)
- [ ] No `z-50` or `z-[9999]` spam; z-index documented for systemic layers only (severity: Medium)
- [ ] Skip-to-main-content link as first focusable element on web pages (severity: High)
- [ ] No carousel hero with auto-advancing slides (severity: High)
- [ ] No multiple gradient sections on a single page (severity: Medium)
- [ ] No "SECTION 01" / "QUESTION 05" meta-labels (severity: High)

## Related

- See **typography.md** for ultra-wide containers that prevent H1 line failure.
- See **spacing.md** for section padding tokens and density modes.
- See **interaction.md** for navigation touch targets and tap feedback.
- See **accessibility.md** for skip-links, heading hierarchy, and orientation support.
- See **motion.md** for scroll-triggered reveals and pinned-section choreography.
- See **dashboards.md** for data-dense layout density and the 5 dashboard archetypes.
- See **components.md** for navbar, modal, and bento card contracts.
