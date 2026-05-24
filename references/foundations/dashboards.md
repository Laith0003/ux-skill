# Dashboards

> Data UI lives by different rules than marketing surfaces. Density is the product. Cards lose their job. Typography becomes data. Color carries semantic state. Restraint is the visual signature; density is the value proposition.

## Principles

1. **Density is the product, not a problem** — A dashboard's job is to surface signal per unit of screen. Generous spacing that fits 3 metrics on a 1440px monitor wastes the user's screen and their scan time. Pick a density mode and commit.

2. **Cards lose their job in dense data UI** — At VISUAL_DENSITY > 7, generic card containers are banned. Use logic-grouping via `border-t`, `divide-y`, or pure negative space. Data metrics breathe without being boxed unless elevation communicates hierarchy.

3. **Tabular numerals are mandatory** — `font-mono` + `font-variant-numeric: tabular-nums` on every numeric column, every stat callout, every ticker. Mixed proportional and tabular figures on the same page is undisciplined.

4. **No serifs on dashboards** — Serifs belong to editorial and marketing. Dashboard typography uses neo-grotesque sans pairings (`Geist + Geist Mono`, `Satoshi + JetBrains Mono`, `Inter + IBM Plex Mono`).

5. **Semantic color is reserved for meaning** — Green = up / live / success, red = down / regression / error, amber = warning, neutral or branded blue = informational. Never decorative. Never repurposed as brand color.

6. **Mono-color logo and chrome, accent only on action** — Dashboard chrome stays neutral. A single accent appears only on primary CTAs, focus rings, and the one or two highlights that earn it.

7. **Live indicators breathe sparingly** — Maximum 2 perpetual ambient pulses per viewport. Only on truly live elements. Anything more becomes screensaver noise that drains attention and battery.

8. **Charts are UI, not decoration** — Charts follow the same rules as the rest of the system: accessibility, contrast, clarity, color-not-only. Tooltips work on hover AND tap AND keyboard focus. Empty / loading / error states are designed.

9. **Restraint is the dashboard's signature** — The premium signal of a dashboard is composure under information density. The cluttered SaaS reflex (gradients, decorative icons, multiple accent colors) is what amateur dashboards do. The disciplined version uses typography, alignment, and negative space.

10. **Mobile collapse is a separate design** — Below 768px, cockpit-density rows collapse to scrollable card stacks, not 1px-divided rows. Mobile dashboards prioritize fewer metrics per viewport with deeper drill-down.

## Do / Don't

| Do | Don't |
|---|---|
| Use `font-mono` + tabular numerals on numeric columns | Mix proportional and tabular figures |
| Replace cards with `border-t` or `divide-y` in dense data | Wrap every metric in a `<Card>` |
| Use neo-grotesque sans (Geist, Satoshi, Inter) | Use serifs in dashboard typography |
| Use semantic color (green/red/amber) only for state | Use semantic colors as brand decoration |
| Right-align numeric columns in tables | Mix alignments in numeric data |
| Sticky headers on long tables (>10 rows) | Force users to scroll back to remember column meaning |
| Right-align action columns | Place action buttons in the leftmost column |
| Use sparklines inline for at-a-glance trends | Embed a full chart for every metric |
| Use compact stat tiles with monospaced numerals | Use 3D charts or rainbow gradients |
| Provide tooltip on hover AND tap AND keyboard focus | Tooltip only on hover (skips mobile and keyboard) |
| Show empty / loading / error states for every chart | Render an empty chart frame |
| Use sticky filter bars at the top of long lists | Force users to scroll up to refilter |
| Cap dashboard accent color use at CTA and focus only | Use accent for chrome decoration |
| Use breathing pulse on max 2 live indicators per viewport | Pulse every status dot on every row |
| Use diverging or qualitative colorblind-safe palettes | Use red-green as the only chart signals |
| Collapse cockpit-density to card stacks below 768px | Force 1px hairlines and 4px paddings on mobile |
| Use the 5 dashboard archetypes as bento card templates | Re-invent the same archetype for every card |
| Y-axis on bar charts starts at zero | Truncate Y-axis to amplify visual variance (misleading) |

## Examples

### Pattern: Cockpit density (VISUAL_DENSITY 8 to 10)
**Use when**: Trading dashboards, analytics, monitoring, ops, internal tools where information density is the value.
**Anti-pattern**: Generous card padding (24 to 40px), white surfaces between every metric, soft drop shadows.
**How**:
- Tiny paddings (4 to 12px)
- No card boxes — 1px lines (`border-t`, `divide-y`) separate data
- `font-mono` for all numbers
- Section grouping via spacing and typography, not container boxes
- Headers tight, columns dense, row heights compressed
- Tabular figures aligned to invisible decimal column

### Pattern: Replace cards with hairlines
**Use when**: Dashboard rows, settings panels, list views.
**Anti-pattern**: Every row wrapped in a `<Card>` with its own border, padding, and shadow — visual noise per row.
**How**:
- `divide-y divide-gray-200` separates rows with hairlines
- `border-t` to start a new section
- Internal padding 8 to 16px per row
- The structure carries from alignment and spacing, not container chrome

### Pattern: Tabular numeral discipline
**Use when**: Tables, stat callouts, prices, timers, dashboard metrics.
**Anti-pattern**: Proportional figures that drift visually when values change (count-up jitter, misaligned decimals).
**How**:
```css
font-feature-settings: "tnum";
font-variant-numeric: tabular-nums;
```
or use `font-mono`. Decimals align vertically. Count-ups don't shift layout. Mixed proportional and tabular figures on the same page is undisciplined.

### Pattern: Inline sparkline
**Use when**: At-a-glance trends inside a table cell, list row, or compact dashboard tile.
**Anti-pattern**: Embedding a full chart for every metric, blowing up vertical real estate.
**How**:
- 60 to 120px wide
- 16 to 24px tall
- Single line color matching semantic state (green up / red down)
- No axes, no labels, no tooltip
- Click expands to full chart in detail view

### Pattern: Compact stat tile
**Use when**: KPI cards in dashboard hero, summary metrics, top-of-page row.
**Anti-pattern**: Stat tile padding at 40px on each side, taking 4 rows of vertical space for one number.
**How**:
- Eyebrow label: 10 to 12px, tracked uppercase or sentence case
- Stat number: 32 to 64px, weight 600 to 700, tabular figures, `font-mono`
- Unit label: 50 to 60% of stat size, regular weight, baseline-aligned
- Delta indicator: small triangle or arrow + percentage in semantic green / red
- Optional sparkline below: 60 to 120px wide
- Internal padding: 16 to 24px (or less in cockpit mode)

### Pattern: 5 dashboard archetypes (bento cards)
**Use when**: Composing a feature-rich dashboard with varied card content.
**Anti-pattern**: 8 identical small cards with the same shape and metric type.
**How**: Mix archetypes across the bento grid:

1. **The Intelligent List** — Vertical stack of items with auto-sorting loop. Items swap positions using shared element transitions, simulating an AI prioritizing tasks in real-time. Best for queues, inboxes, priority lists.

2. **The Command Input** — Search / AI bar with multi-step typewriter effect. Cycles through complex prompts. Includes blinking cursor and "processing" state with shimmering loading gradient. Best for AI assistants, search-first UIs.

3. **The Live Status** — Scheduling interface with breathing status indicators. Pop-up notification badge emerges with overshoot spring, holds for 3 seconds, vanishes cleanly. Best for ops, calendars, live monitoring.

4. **The Wide Data Stream** — Horizontal infinite carousel of data cards or metrics. Loop is seamless via `x: ["0%", "-100%"]` at 15 to 25s speed. Best for ticker, leaderboards, recent events.

5. **The Contextual Focus** — Document view animating a staggered highlight of a text block, followed by float-in of a floating action toolbar. Best for note editors, document analysis, focused review.

### Pattern: Live status indicator
**Use when**: Real-time element (online presence, live data, active operation).
**Anti-pattern**: Pulsing dot on every status icon on every row — screensaver effect.
**How**:
- Maximum 2 perpetual pulses per viewport
- Only on truly live elements
- Pulse loop: `scale: [1, 1.1, 1]` over 2 to 3 seconds, `opacity: [1, 0.6, 1]`
- Isolated in memoized leaf client component so page does not re-render with each frame
- Disabled under `prefers-reduced-motion: reduce`
- Pair with `aria-live="polite"` for screen reader updates

### Pattern: Chart with full state coverage
**Use when**: Every chart in the dashboard.
**Anti-pattern**: Chart renders blank or with "undefined" labels when data is loading or empty.
**How**:
- **Empty**: "No data yet" + guidance ("Connect your first source to see metrics")
- **Loading**: skeleton or shimmer placeholder matching chart shape
- **Error**: error message with retry action
- **Default**: chart renders with proper axes, legends, and tooltips

### Pattern: Chart accessibility
**Use when**: Every chart.
**Anti-pattern**: Color-only signals; tooltips only on hover; no data table alternative for screen readers.
**How**:
- Color supplemented by patterns, textures, or shapes
- Color contrast ≥3:1 for data lines/bars; ≥4.5:1 for text labels
- Tooltip works on hover (mouse), tap (touch), AND keyboard focus
- Legend visible near chart, clickable to toggle series visibility
- `aria-label` on chart summarizing key insight
- Parallel data table provided as accessible alternative

### Pattern: Sortable table with sticky header
**Use when**: Long tabular data with multiple columns.
**Anti-pattern**: Forcing users to scroll back to remember column meaning, or making them tap small chevrons to sort.
**How**:
- Sticky header pinned to top of scroll container
- `aria-sort="ascending"` / `aria-sort="descending"` on sorted column
- Click anywhere on header sorts; arrow indicator shows direction
- Active sort visually highlighted
- Keyboard navigable (Tab to header, Enter or Space to sort)
- Empty state across full width when no rows
- Pagination, page size, or infinite scroll for >50 rows

### Pattern: Filter bar
**Use when**: List or table with multiple filter dimensions.
**Anti-pattern**: Modal-only filtering that forces users out of the data view.
**How**:
- Sticky filter bar at top of list
- Active filters shown as removable pill chips
- "Clear all" link when ≥2 filters active
- Filter dropdowns close on outside click
- Filter state persists in URL (deep-linkable)
- Multi-select filters use checkbox lists

### Pattern: Drill-down with breadcrumb
**Use when**: Hierarchical data (region → country → city → store).
**Anti-pattern**: Silent navigation that drops user into a sub-view with no orientation.
**How**:
- Breadcrumb at top: `Region > Country > City`
- Each crumb is a link to that level
- Back button preserves scroll position and filter state
- "Up one level" gesture (Esc on web, swipe-right on mobile)
- Deep links to specific drill states

### Pattern: Real-time data update
**Use when**: Live metrics that update without user action.
**Anti-pattern**: Page reloads or auto-refreshes that disrupt the user's scroll position.
**How**:
- Numbers animate to new values with subtle fade or count-up (300 to 600ms)
- Lists insert new rows at top with `staggerChildren` (50 to 80ms) and slide-in
- Status pills change color with 200ms transition
- `aria-live="polite"` region announces critical updates to screen readers
- User scroll position preserved across updates

### Pattern: Brutalist data viz
**Use when**: Industrial, terminal-adjacent, or anti-mainstream products.
**Anti-pattern**: Smooth animated splines, soft drop shadows, brand-color charts.
**How**:
- Single-color line charts in foreground ink against substrate
- No fills, no smoothed splines
- Axes as visible solid lines with tick marks
- Gridlines as 1px hairlines at minimum opacity
- Annotations use leader lines and monospace callouts (not floating tooltips)
- Numeric counters tick through digits with `steps(N)` easing (slot-machine effect)

### Pattern: Monochrome-leaning palette
**Use when**: Any premium SaaS dashboard.
**Anti-pattern**: 5+ accent colors decorating chrome and data simultaneously.
**How**:
- Background: off-white or near-black (depending on mode)
- Text: charcoal or off-white
- Borders / dividers: hairlines (`#EAEAEA` light; white at 8 to 12% alpha dark)
- One brand accent: CTAs and focus rings only
- Semantic colors (green/red/amber): inside product data and pills only
- Chart colors: diverging or sequential, never decorative

## Tokens / values

### Density modes
- **Art-gallery (1 to 3)**: huge section gaps, sparse text, expensive and quiet
- **Daily-app (4 to 7)**: normal spacing, comfortable scanning
- **Cockpit (8 to 10)**: tiny paddings, no card boxes, 1px lines separating data, mandatory `font-mono` on numbers

### Cockpit-specific tokens
- Internal padding: 4 to 12px
- Row height: 28 to 36px
- Header height: 24 to 32px
- Numbers: `font-mono` + tabular numerals
- Section separators: `border-t`, `divide-y`, 1px hairlines
- No card boxes (replace with logic-grouping via hairlines)
- Mobile collapse: cockpit becomes scrollable card stacks below 768px

### Typography (dashboard-specific)
- Display headlines: neo-grotesque sans only (Geist, Satoshi, Inter, Manrope)
- Body: 14 to 16px on dashboard surfaces (smaller than marketing)
- Stat numerals: 32 to 64px (compact tile), 48 to 144px (hero metric)
- Stat numeral unit label: 40 to 60% of stat size
- Eyebrow labels: 10 to 12px, weight 500, tracking +0.06em
- Inline code / values: 13 to 14px in `font-mono`
- Banned: serifs anywhere in dashboard chrome

### Tabular numeral configuration
```css
font-feature-settings: "tnum";
font-variant-numeric: tabular-nums;
```
Or use a true monospace family (`font-mono`).

### Sparkline specs
- Width: 60 to 120px
- Height: 16 to 24px
- Stroke: 1.5 to 2px
- Color: matches semantic state (green up, red down, neutral mid)
- No axes, no labels, no gridlines, no tooltips inline
- Click expands to full chart

### Compact stat tile specs
- Padding: 16 to 24px (daily-app); 8 to 12px (cockpit)
- Stat numeral: 32 to 64px, weight 600 to 700, `font-mono`, tabular figures
- Unit label: 50 to 60% of numeral size, regular weight, baseline-aligned
- Eyebrow: 10 to 12px, tracked uppercase or sentence case
- Delta indicator: triangle or arrow + percentage in semantic color
- Optional sparkline: 60 to 120px below stat

### Bento 2.0 (premium dashboard)
- Background: `#f9fafb`
- Cards: pure white `#ffffff` with `border-slate-200/50` (1px)
- Surfaces: `rounded-[2.5rem]` for major containers
- Shadows: diffusion `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`
- Typography: `Geist`, `Satoshi`, or `Cabinet Grotesk`; subtle `tracking-tight` on headers
- Labels: titles and descriptions OUTSIDE and BELOW cards for gallery presentation
- Padding inside cards: 32 to 40px (`p-8` to `p-10`)
- Animation engine: spring physics (`stiffness: 100, damping: 20`), heavy use of `layout` and `layoutId`, every card with an "active state" that loops infinitely

### 5 dashboard archetypes
1. **The Intelligent List** — auto-sorting items with shared-element morph; for queues, inboxes
2. **The Command Input** — typewriter + cursor + processing shimmer; for AI search, prompts
3. **The Live Status** — breathing indicators, popup notifications with spring + 3s hold; for ops, calendars
4. **The Wide Data Stream** — horizontal infinite carousel at 15-25s loop; for tickers, leaderboards
5. **The Contextual Focus** — staggered highlight + floating action toolbar; for editors, document review

### Live indicator rules
- Maximum 2 perpetual pulses per viewport
- Only on truly live elements
- Pulse spec: `scale: [1, 1.1, 1]` over 2 to 3 seconds
- Isolated in memoized leaf client component
- Disabled under `prefers-reduced-motion: reduce`
- Pair with `aria-live="polite"`

### Chart type selection
- **Trend over time**: line chart, area chart, sparkline
- **Comparison**: vertical bar (5-15 categories), horizontal bar (long labels or many items)
- **Proportion**: pie or donut (≤5 categories; never more), treemap (hierarchical)
- **Distribution**: histogram, box plot, violin plot
- **Correlation**: scatter plot, bubble chart, heatmap
- **Flow / process**: funnel, Sankey, waterfall
- **Geographic**: choropleth map, pin/marker map
- **Network**: force-directed graph, chord diagram
- **Time-specific**: Gantt chart, calendar heatmap, radar chart

### Chart color palettes (accessible)
- **Diverging**: blue → gray → red (for negative-positive scales); avoid red-green
- **Sequential**: single-hue gradient (light to dark) for ordered data
- **Qualitative**: maximum 7 to 8 distinct hues for categories
- **Colorblind-safe**: perceptually uniform (Viridis, Cividis, Magma)

### Chart specs
- Tooltip: works on hover (web), tap (mobile), keyboard focus
- Legend: near chart, clickable to toggle series
- Axis labels: locale-aware number formatting, readable scale
- Auto-skip ticks on small screens
- Empty / loading / error states designed
- `aria-label` summary describing key insight
- Data table alternative (parallel `<table>` for screen readers)
- Reduced-motion: skip entrance animations; data readable immediately
- 1000+ data points: aggregate or sample; drill-down for detail
- Y-axis on bar charts: starts at zero (mandatory)
- Direct labeling for small datasets (label values directly on chart)

### Semantic state colors (dashboard data)
- Success / up / live / healthy: green family
- Error / down / regression / destructive: red family
- Warning / pending: amber family
- Informational / neutral: branded blue
- Disabled / muted: gray
- These NEVER appear as chrome decoration

### Table specs (dashboard)
- Row height: 32 to 48px (default); 28 to 36px (cockpit); 48 to 56px (comfortable)
- Header height: tighter than rows by 4 to 8px
- Numbers: right-aligned, `font-mono`, tabular figures
- Action columns: right-aligned
- Sticky headers on >10 rows
- Selected row: brand accent at low opacity + checkbox
- Empty state: full-width row with composed message
- Mobile: collapse to cards or enable horizontal scroll
- Pagination, page size, or infinite scroll for >50 rows

### Filter bar specs
- Sticky at top of list
- Active filters as removable pill chips
- "Clear all" when ≥2 filters active
- Filter dropdowns close on outside click
- Filter state persists in URL
- Multi-select filters use checkbox lists

### Mobile collapse rules (dashboards)
- Below 768px: cockpit density caps at "daily-app"
- Below 768px: 1px-divided rows become card stacks
- Below 768px: fewer metrics per viewport with deeper drill-down
- Below 768px: tables collapse to cards or enable horizontal scroll
- Below 768px: motion intensity reduces by 2 levels

### Banned dashboard patterns
- Serif typography on dashboards
- Mixed proportional and tabular figures on the same page
- Generic 3D charts (distort perception)
- Pie charts with >5 wedges
- Red-green as the only color signals in charts
- Color-only data signals (no pattern, no text)
- Tooltips only on hover (no keyboard, no mobile)
- Chart Y-axis that doesn't start at zero on bar charts (misleading)
- Charts without empty / loading / error states
- Cards wrapping every metric in dense data UI (use hairlines instead)
- Semantic state colors used as brand decoration
- Multiple accent colors in dashboard chrome
- Decorative gradients on dashboard surfaces
- Glowing brain / neural-net / spark icons for AI features
- Auto-refreshing pages that lose user scroll position
- Modal-only filtering (use inline filter bar)
- Pulsing live indicators on every row
- Sticky chatbot bubble overlapping primary actions
- Floating UI windows with drop shadows and tilted-perspective screenshots
- Stock photography in dashboard surfaces

### Restraint signals (premium dashboards)
- Off-white or near-black background; never pure
- Charcoal or off-white text; never pure black or pure white
- One accent color, CTA / focus only
- Hairline borders or near-absent shadows
- Sentence-case headlines
- Tabular numerals everywhere data appears
- Mono-color logo and chrome
- Mono-color customer logos in any visible band

## Checklist (severity-tagged)

- [ ] Density mode (art-gallery / daily-app / cockpit) chosen and consistent (severity: High)
- [ ] Cockpit-density mode caps at "daily-app" below 768px (severity: High)
- [ ] Tabular numerals (`font-mono` + `tabular-nums`) on numeric columns and stat callouts (severity: Critical)
- [ ] No mixed proportional and tabular figures on the same page (severity: High)
- [ ] No serifs in dashboard typography (severity: High)
- [ ] Cards replaced with `border-t` / `divide-y` in cockpit-density UIs (severity: Medium)
- [ ] Semantic state colors (green/red/amber) used only for state, not chrome (severity: Critical)
- [ ] One accent color in chrome, applied only on CTAs and focus rings (severity: High)
- [ ] Chrome stays monochrome; chromatic load carried by data (severity: Medium)
- [ ] Numbers right-aligned in tables (severity: Medium)
- [ ] Action columns right-aligned (severity: Medium)
- [ ] Sticky table headers on tables >10 rows (severity: Medium)
- [ ] Sortable columns include `aria-sort` attribute (severity: High)
- [ ] Maximum 2 perpetual pulses per viewport (severity: Medium)
- [ ] Live indicators only on truly live elements (severity: Medium)
- [ ] Live indicators isolated in memoized leaf client components (severity: High)
- [ ] All charts have empty / loading / error states designed (severity: High)
- [ ] Chart tooltips work on hover, tap, AND keyboard focus (severity: Critical)
- [ ] Chart legends visible and clickable to toggle series (severity: High)
- [ ] Chart color contrast ≥3:1 for data lines, ≥4.5:1 for text labels (severity: Critical)
- [ ] Chart palettes survive color-blindness (no red-green only) (severity: Critical)
- [ ] Chart `aria-label` summary describes key insight (severity: Critical)
- [ ] Data table alternative provided for every chart (severity: Critical)
- [ ] Y-axis on bar charts starts at zero (severity: High)
- [ ] No pie charts with >5 wedges (severity: High)
- [ ] No 3D charts (severity: High)
- [ ] Chart reflows or simplifies on mobile (severity: High)
- [ ] Filter bar sticky at top of long lists (severity: Medium)
- [ ] Active filters shown as removable pill chips (severity: Medium)
- [ ] Filter state persists in URL (severity: Cosmetic)
- [ ] Drill-down maintains breadcrumb and back-path (severity: Medium)
- [ ] Real-time updates preserve user scroll position (severity: High)
- [ ] Sparklines used for at-a-glance trends (no full chart for every metric) (severity: Cosmetic)
- [ ] Mobile dashboards prioritize fewer metrics per viewport with drill-down (severity: Medium)
- [ ] Number animations use `font-mono` with tabular figures to prevent layout shift (severity: High)
- [ ] No decorative gradients on dashboard surfaces (severity: Medium)
- [ ] No glowing AI / neural icons (use restrained generic symbols) (severity: Medium)
- [ ] Reduced-motion respected on chart entrance animations (severity: Critical)
- [ ] Charts honor `prefers-reduced-motion: reduce` (severity: Critical)
- [ ] 1000+ data points aggregated or sampled with drill-down (severity: High)
- [ ] Sticky chatbot bubbles do not overlap primary CTAs (severity: Medium)
- [ ] Cockpit-density rows collapse to card stacks below 768px (severity: High)

## Related

- See **components.md** for canonical contracts on table, chart, modal, toast.
- See **color.md** for semantic state colors and dark-mode dashboard palettes.
- See **typography.md** for tabular numeral configuration and mono pairings.
- See **spacing.md** for cockpit-density padding and section grouping rules.
- See **motion.md** for live indicator pulse specs and chart entry animations.
- See **accessibility.md** for chart tooltip accessibility and data table alternatives.
- See **layout.md** for dashboard archetype patterns and bento layout rules.
- See **interaction.md** for sortable column behavior and filter bar interactions.
