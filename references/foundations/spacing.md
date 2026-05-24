# Spacing

> Whitespace is a design element, not a deficit. A consistent spacing rhythm is what makes a layout feel composed instead of cramped.

## Principles

1. **Pick a base unit and commit** — 4px or 8px. Build every gap, padding, and margin on multiples of that unit. The system is the look. Random spacing increments with no rhythm read as undisciplined.

2. **Section breathing room signals confidence** — Marketing sections at 96 to 160px vertical padding (often 120 to 200px on developer-tooling). Cramped sections (`py-12` on marketing) read as discount; breathing sections read as premium. Mobile halves the rhythm but keeps the principle.

3. **Density mode is a deliberate choice** — Art-gallery (low density), daily-app (comfortable), cockpit (packed). Pick one per surface based on product type. Mobile caps density at "daily-app" regardless of desktop choice.

4. **Adaptive gutters by breakpoint** — Increase horizontal insets on larger widths and in landscape. The same narrow gutter on phone and tablet reads as unconsidered.

5. **Vertical rhythm cascades by hierarchy** — Define tiers: 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128 / 160. Inside a component, gaps land on the smaller end (4 to 16). Between sections, gaps land on the larger end (64 to 160). Each tier signals a different level of separation.

6. **Safe areas are non-negotiable** — Fixed navbars, tab bars, and CTA bars must reserve space for notch, Dynamic Island, home indicator, and scroll content insets so lists do not hide behind sticky bars.

7. **Container max-widths cap reading distance** — 1200 to 1400px outer container, 640 to 1080px inner content depending on type of content (prose narrower, visuals wider). Beyond 1400px the eye loses anchor.

8. **Asymmetric whitespace is composition, not accident** — Generous one-sided whitespace (e.g., `padding-left: 20vw`) pushes content off-center deliberately. Symmetrical padding on every section produces the corporate-template look.

9. **Z-index is structural, not decorative** — Reserve high z-indexes for systemic layers: sticky nav, modals, overlays, tooltips. Document the scale. No arbitrary `z-50` spam.

10. **Inside cards, padding earns its keep** — Generous internal padding (24 to 40px) inside premium cards; tighter (8 to 16px) inside brutalist or cockpit-dense layouts. Mixed-padding cards on the same page break the rhythm.

## Do / Don't

| Do | Don't |
|---|---|
| Use a 4px or 8px base spacing unit | Use random px values like 7px, 13px, 19px |
| Apply 96 to 160px vertical padding to marketing sections | Cram marketing sections at 24 to 48px vertical padding |
| Halve section padding on mobile, keep the rhythm | Eliminate section padding on mobile |
| Use 24 to 40px internal padding inside premium cards | Use 8px tight padding inside premium cards |
| Increase horizontal gutters at wider breakpoints | Keep the same narrow gutter from phone to desktop |
| Cap content containers at 1200 to 1400px | Let content stretch edge-to-edge on 2560px monitors |
| Constrain prose columns to 640 to 720px | Run paragraphs at 100+ characters per line |
| Reserve z-indexes for nav, modal, overlay, tooltip | Spam `z-50` arbitrarily on every component |
| Respect safe areas for status bar, notch, home indicator | Place tappable controls under notch or gesture area |
| Use `min-h-[100dvh]` for full-height sections | Use `h-screen` (breaks on iOS Safari address bar collapse) |
| Document the spacing scale as design tokens | Re-invent gap values per component |
| Use CSS Grid for responsive structures | Use flexbox percentage math like `w-[calc(33%-1rem)]` |
| Use `grid-flow-dense` on bento layouts | Leave empty cells in bento grids |
| Use generous whitespace as the structural device | Reach for borders, rules, and dividers as separators |

## Examples

### Pattern: Marketing section padding
**Use when**: Any marketing landing section that needs to feel like a distinct cinematic chapter.
**Anti-pattern**: `py-12` (48px) — sections feel cramped, slabs of content with no breathing room.
**How**: Apply `py-32 md:py-48` minimum (128px mobile, 192px desktop). For premium and developer-tooling surfaces, push to `py-40` or `py-48` (160 to 192px). Sections breathe; the page reads as composed.

### Pattern: AIDA section vertical rhythm
**Use when**: Landing pages structured around Attention → Interest → Desire → Action.
**Anti-pattern**: Identical padding on every section regardless of role.
**How**: Hero gets the deepest top padding (often `min-h-[100dvh]` with content centered or split). Interest sections (bento, features) get `py-32 md:py-48`. Desire sections (motion, media) get `py-40 md:py-56` to let scroll moments breathe. Action sections (final CTA) get `py-32 md:py-48` plus a tinted background band that visually separates from the footer.

### Pattern: Adaptive gutter scaling
**Use when**: Pages that span 375px mobile to 1440px+ desktop.
**Anti-pattern**: `px-4` everywhere from phone to desktop — wide screens look cramped against the chrome.
**How**: Mobile: `px-4` (16px). Tablet: `px-8` (32px). Desktop: `px-12` (48px) or use `max-w-7xl mx-auto` and let outer padding scale. Landscape phones get treated as tablets for gutter purposes — the wider canvas earns wider insets.

### Pattern: Component internal padding by density
**Use when**: Building cards, panels, and containers for a specific density mode.
**Anti-pattern**: Same padding (e.g., `p-4`) on every card regardless of role.
**How**:
- Art-gallery (premium SaaS): `p-8` to `p-10` (32 to 40px)
- Daily-app: `p-6` (24px)
- Cockpit / dense data: `p-2` to `p-4` (8 to 16px); rely on `border-t`, `divide-y` for separation rather than card padding
- Premium hero containers: `p-10` to `p-16` (40 to 64px), often with `rounded-[2.5rem]` for major bento containers

### Pattern: Bento grid with no empty cells
**Use when**: Asymmetric tile grids for "what's in the box" sections, dashboards, feature showcases.
**Anti-pattern**: A bento grid with 3 cards in row 1 and 2 cards in row 2 leaving a visible empty cell at the bottom-right.
**How**: Use `grid-flow-dense` to fill gaps. Aim for 3 to 5 cards (not 8) with varied sizes — one tall, one wide, one or two square. `gap-4` to `gap-6` between cards. Mobile collapses to a single column with `gap-4`.

### Pattern: Z-index scale
**Use when**: Layering sticky nav, modals, drawers, tooltips, toasts.
**Anti-pattern**: `z-50`, `z-[9999]`, `z-[99999]` spammed arbitrarily.
**How**: Document a scale and stick to it:
- 0: default flow
- 10: sticky elements (nav, sticky table headers)
- 20: dropdowns, popovers
- 40: drawers, side panels
- 100: modals
- 200: toasts and notifications above modals
- 1000: critical overlays (loading, fatal errors)

### Pattern: Asymmetric whitespace push
**Use when**: Layouts at DESIGN_VARIANCE 8 or above — asymmetric editorial, premium hero, brutalist.
**Anti-pattern**: Symmetrical padding on every section produces the corporate-template look.
**How**: Push content off-center with `padding-left: 20vw` or generous one-sided whitespace. Use fractional grid columns (`grid-template-columns: 2fr 1fr 1fr`) instead of equal `grid-cols-3`. Apply `margin-top: -2rem` for overlapping cards or images. Mobile aggressively falls back to single-column `w-full px-4`.

### Pattern: Safe area compliance
**Use when**: Mobile apps and PWAs with fixed headers, tab bars, or CTA bars.
**Anti-pattern**: Placing tappable controls under the notch, Dynamic Island, or home indicator.
**How**: Use `env(safe-area-inset-top)` and `env(safe-area-inset-bottom)` for fixed elements. Reserve content insets (`padding-bottom`) on scroll containers so lists are not hidden behind sticky bars. Test on devices with and without notches; test both portrait and landscape.

### Pattern: Container width caps
**Use when**: Marketing landing pages, product surfaces, documentation.
**Anti-pattern**: Content stretching full-width on 2560px ultrawide monitors — line lengths become punishing.
**How**:
- Outer container: `max-w-7xl mx-auto` (1280px) or `max-w-[1400px] mx-auto`
- Inside the container: prose columns at `max-w-prose` or `max-w-[65ch]` (roughly 640 to 720px)
- Visuals at `max-w-[1024px]` to `max-w-[1080px]`
- Full-bleed sections (backgrounds, hero imagery) extend to `w-screen`; constrained content inside still respects the container

### Pattern: Vertical rhythm cascade
**Use when**: Stacking components with clear hierarchy — eyebrow → headline → body → CTA.
**Anti-pattern**: Identical 16px gap between every adjacent element.
**How**:
- 4 to 8px: between tightly related elements (icon + label, eyebrow + headline)
- 12 to 16px: between paragraph and next paragraph
- 24 to 32px: between component groups (headline block to CTA)
- 48 to 64px: between distinct content blocks within a section
- 96 to 160px: between major sections

### Pattern: Brutalist grid lines via gap
**Use when**: Industrial, technical, or engineered-document aesthetic.
**Anti-pattern**: Heavy `border` declarations on every cell.
**How**: Use `display: grid; gap: 1px;` with contrasting parent/child background colors to generate razor-thin dividing lines. The grid is allowed to be visible — faint baseline grids, registration marks, and ruler tick marks reinforce the engineered feel.

### Pattern: Safe area implementation
**Use when**: Mobile apps and PWAs with fixed headers, tab bars, or floating CTA bars.
**Anti-pattern**: Placing tappable controls under the notch, Dynamic Island, gesture home indicator, or curved corners.
**How**:
- Top: `padding-top: max(16px, env(safe-area-inset-top))` on fixed headers
- Bottom: `padding-bottom: max(16px, env(safe-area-inset-bottom))` on tab bars and floating CTAs
- Scroll containers: `padding-bottom` equal to fixed-element height + safe-area inset
- Test on devices with notches, Dynamic Island, and gesture indicators
- Test landscape orientation — safe areas shift to left and right edges
- Avoid hardcoding pixel values; respect the system's variable insets

### Pattern: Premium card padding scale
**Use when**: High-end aesthetic with major bento containers.
**Anti-pattern**: `p-4` on every card regardless of role.
**How**:
- Major bento containers: `p-10` to `p-16` (40 to 64px) — generous, gallery-presentation
- Standard premium cards: `p-8` (32px)
- Feature cards: `p-6` (24px)
- Compact tiles: `p-4` (16px)
- Cockpit rows: `p-2` to `p-3` (8 to 12px)
- Internal content gap: `space-y-4` to `space-y-6` (16 to 24px) inside card

### Pattern: AIDA section spacing escalation
**Use when**: Landing pages structured around Attention → Interest → Desire → Action.
**Anti-pattern**: Same `py-32` on every section.
**How**:
- Hero (Attention): `min-h-[100dvh]` with centered or split content; section padding minimal because the hero is its own block
- Interest (bento, features): `py-32 md:py-48` standard
- Desire (motion / proof / scrolly): `py-40 md:py-56` to let scroll moments breathe
- Action (final CTA): `py-32 md:py-48` plus tinted background band
- Footer: handled separately; minimum `py-16 md:py-24`

### Pattern: Magazine effect (wide canvas, narrow column)
**Use when**: Editorial, premium SaaS, long-form content surfaces.
**Anti-pattern**: Body text running 100+ characters per line across a wide viewport.
**How**: Outer canvas full-width (`max-w-7xl` or `max-w-[1400px]`). Body text columns inside clamp to 55 to 75 characters via `max-w-prose` or `max-w-[65ch]`. Inside premium card containers, internal padding stays at 24 to 40px. The eye reads short lines on a wide canvas; the magazine effect is the cumulative result.

### Pattern: Section background tonal shifts
**Use when**: Long pages need visual chunking without decorative dividers.
**Anti-pattern**: Bright color blocks alternating down the page (uncertain palette).
**How**: Three to four micro-shades of off-white (`#FFFFFF` → `#FAFAFA` → `#F4F6FA`) differentiate sections. The page feels structured without feeling segmented. Reserve one true-dark band per page (final CTA or one feature deep-dive) for maximum impact.

## Tokens / values

### Base unit
- 4px or 8px — pick one and commit
- All gaps, paddings, margins are multiples of the base unit

### Spacing scale (8px-rhythm aligned)
- 0 / 1 / 2 / 3 / 4 / 6 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128 / 160
- In px: 0 / 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128 / 192 / 256 / 384 / 512 / 640

### Section padding by surface type
- Marketing landing: `py-32 md:py-48` (128 to 192px desktop)
- Marketing premium / developer-tooling: `py-40 md:py-56` (160 to 224px desktop)
- Marketing brutalist / editorial: `py-32 md:py-48`, often paired with full-width macro-typography
- Product / dashboard: `py-12 md:py-16` (48 to 64px)
- Modal / sheet: `p-6` (24px) to `p-8` (32px)
- Mobile: halve the desktop values; floor at `py-16` (64px) for marketing

### Container widths
- Outermost: `max-w-7xl` (1280px) or `max-w-[1400px]`
- Prose / text columns: `max-w-prose` or `max-w-[65ch]` (~640 to 720px)
- Hero containers (constrains H1 to prevent 6-line wraps): `max-w-5xl` to `max-w-6xl` (1024 to 1152px)
- Visual / imagery containers: `max-w-5xl` to `max-w-7xl` (1024 to 1280px)
- Mobile: respect the container but use `px-4` outer padding

### Card internal padding by density
- Art-gallery: 32 to 40px (`p-8` to `p-10`)
- Daily-app: 24px (`p-6`)
- Cockpit / dense: 8 to 16px (`p-2` to `p-4`)
- Premium hero / bento: 40 to 64px (`p-10` to `p-16`)
- Tight bento with imagery: 12 to 16px (`p-3` to `p-4`)

### Card radii
- Sharp / brutalist: 0 (90-degree corners only)
- Crisp minimalist: 4 to 12px (`rounded` to `rounded-xl`)
- Premium soft: 16 to 24px (`rounded-2xl` to `rounded-3xl`)
- High-end bento: `rounded-[2rem]` to `rounded-[2.5rem]` (32 to 40px)
- Pills and badges: `rounded-full` (9999px)
- Mathematically concentric: outer radius `rounded-[2rem]`, inner core radius `rounded-[calc(2rem-0.375rem)]` so inner and outer are visibly concentric

### Z-index scale (documented)
- 0: default flow
- 10: sticky nav, sticky table headers
- 20: dropdowns, popovers
- 40: side drawers, off-canvas panels
- 100: modals, dialogs
- 200: toasts, notifications above modals
- 1000: critical overlays (full-screen loading, fatal errors)

### Safe area variables
- Top: `env(safe-area-inset-top)` for status bar and notch
- Bottom: `env(safe-area-inset-bottom)` for home indicator and gesture area
- Add content insets to scroll containers so lists are not hidden behind fixed bars
- Test at 375px (small phone), 414px (large phone), 768px (tablet), 1024px (laptop), 1440px (desktop)

### Breakpoints
- Mobile: 375px (small), 414px (large)
- Tablet: 768px
- Laptop: 1024px
- Desktop: 1280px
- Wide desktop: 1440px+
- Cap at 1400px; above that, center and pad

### Mobile collapse rules (VARIANCE 4-10)
- Below 768px (`md:`): any asymmetric layout falls back to `w-full px-4 py-8` single-column
- Below 768px: cap density at "daily-app" — cockpit mode becomes scrollable card stacks, not 1px-divided rows
- Below 768px: motion intensity drops by 2 levels
- Below 768px: bento grids collapse to single column with `gap-4` and standard vertical spacing; no `col-span` overrides survive
- Below 768px: remove rotations and negative-margin overlaps from z-axis cascades

### Banned spacing patterns
- `h-screen` for full-height sections (use `min-h-[100dvh]`)
- Flex percentage math like `w-[calc(33%-1rem)]` (use CSS Grid)
- Same narrow gutter from phone to desktop (adapt by breakpoint)
- Section padding under `py-32` on marketing surfaces
- Empty cells in bento grids (use `grid-flow-dense`)
- Symmetrical padding on every section as a fallback
- Arbitrary `z-50` or `z-[9999]` without documented purpose
- Horizontal scroll on mobile body content (wrap page in `overflow-x-hidden w-full max-w-full`)
- Tap targets crammed without 8px gap between (minimum 8 to 8dp between adjacent touch targets)
- Identical card padding across density modes

### Touch density
- Minimum 8px gap between adjacent touch targets
- Comfortable spacing reads as professional, cramped reads as junior
- Tabs and segmented controls: 4 to 8px between items
- Toolbars: 8 to 12px between buttons
- List rows: 8 to 16px vertical padding per row (cockpit drops to 4 to 6px)

## Checklist (severity-tagged)

- [ ] Base spacing unit (4 or 8) chosen and documented (severity: High)
- [ ] All gaps, paddings, margins land on multiples of the base unit (severity: High)
- [ ] Marketing sections use `py-32 md:py-48` minimum (severity: High)
- [ ] Hero uses `min-h-[100dvh]`, not `h-screen` (severity: Critical)
- [ ] Page wrapped in `overflow-x-hidden w-full max-w-full` when motion is used (severity: High)
- [ ] Outer container caps at `max-w-7xl` (1280px) or `max-w-[1400px]` (severity: Medium)
- [ ] Prose columns clamp to `max-w-prose` (~65ch / 640 to 720px) (severity: Medium)
- [ ] Hero H1 container is `max-w-5xl` or wider to prevent 6-line wraps (severity: Critical)
- [ ] Horizontal gutters adapt by breakpoint (mobile `px-4`, desktop `px-12`+) (severity: Medium)
- [ ] Safe areas respected for status bar, notch, home indicator (severity: Critical for mobile)
- [ ] Scroll containers have content insets so lists are not hidden behind fixed bars (severity: High)
- [ ] Mobile aggressive collapse: any asymmetric layout above `md:` falls back to single-column below 768px (severity: Critical)
- [ ] No `h-screen` anywhere — `min-h-[100dvh]` used consistently (severity: Critical)
- [ ] CSS Grid used for responsive structures; no flex percentage math (severity: High)
- [ ] Bento grids use `grid-flow-dense`; no empty cells (severity: High)
- [ ] Bento card count is 3 to 5, not 8 (severity: Medium)
- [ ] Z-index scale documented; no `z-50` or `z-[9999]` spam (severity: Medium)
- [ ] No horizontal scroll on mobile body content (severity: Critical)
- [ ] Verified on 375px, 414px, 768px, 1024px, 1440px (severity: Critical)
- [ ] Density mode (art-gallery / daily-app / cockpit) chosen and consistent (severity: Medium)
- [ ] Cockpit mode (density > 7) caps at "daily-app" below 768px (severity: High)
- [ ] Card internal padding consistent across the system; not mixed (24px / 32px) on one page (severity: Medium)
- [ ] Section spacing hierarchy uses defined tiers (16/24/32/48/96/160), not ad-hoc values (severity: Medium)
- [ ] No section padding under `py-12` on marketing surfaces (severity: High)
- [ ] Minimum 8px gap between adjacent touch targets (severity: Critical)
- [ ] Major bento containers use generous `p-10` to `p-16` (40 to 64px) padding (severity: Cosmetic)
- [ ] Section background shifts use 3 to 4 micro-shades of off-white, not bright color blocks (severity: Medium)
- [ ] Magazine effect: wide canvas, narrow text column (55 to 75 characters) (severity: Medium)
- [ ] AIDA spacing escalates: Desire sections get more vertical room than Interest sections (severity: Cosmetic)
- [ ] Safe area insets respected with `env(safe-area-inset-top)` and `env(safe-area-inset-bottom)` (severity: Critical for mobile)
- [ ] No `p-4` applied uniformly to cards of different roles (severity: Medium)
- [ ] Asymmetric whitespace pushes used intentionally at VARIANCE > 7 (severity: Medium)
- [ ] One true-dark band per page reserved for maximum impact (severity: Cosmetic)
- [ ] Grain / noise overlays on fixed `pointer-events-none` layers only (severity: Critical)
- [ ] `backdrop-blur` applied only to fixed or sticky elements (severity: Critical)
- [ ] Mobile breakpoints have bespoke layouts, not stacked desktop columns (severity: Medium)

## Related

- See **layout.md** for AIDA section structure that drives section padding decisions.
- See **interaction.md** for touch target sizes and spacing between tappable elements.
- See **accessibility.md** for safe-area compliance and zoom behavior.
- See **components.md** for card-specific padding contracts.
- See **dashboards.md** for cockpit-density spacing rules.
- See **motion.md** for layout shift avoidance during animations.
