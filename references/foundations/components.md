# Components

> A component is a contract: a name, a set of states, a set of slots, a documented behavior. Every component ships with every state required by users — not just the happy path.

## Principles

1. **Every interactive component has a complete state cycle** — Default, hover, pressed/active, focus, disabled, loading, error, success, empty. Shipping only the happy path is a quality failure.

2. **Semantic native controls beat custom containers** — `<button>`, `<a href>`, `<input>`, `<label>`, `<table>`, `<dialog>`. Generic `<div>` used as a button breaks screen readers, keyboard navigation, and focus management.

3. **Compound components beat flat prop APIs** — `<Card><Card.Header><Card.Title>...</Card.Title></Card.Header></Card>` beats `<Card title="..." />`. Compound patterns compose cleanly; flat APIs leak abstractions.

4. **Semantic variants beat raw colors** — Buttons take `primary`, `secondary`, `tertiary`, `danger`, `ghost`, `outline`. Not `bg-blue-500`, `bg-red-500`. The variant adapts to themes; the raw color defeats the system.

5. **One primary action per context** — Each screen, section, or modal has exactly one primary CTA. Two primaries dilute the path. The rest are secondary, tertiary, or ghost.

6. **Cards earn their elevation** — Use cards only when elevation communicates hierarchy. Otherwise, alignment and spacing carry the structure. In dense data UI, replace cards with `border-t`, `divide-y`, or pure negative space.

7. **Forms validate on `blur`, not on every keystroke** — Show the error after the user finishes the input. Auto-focus the first invalid field on submit failure. Provide both inline errors and an aggregated summary.

8. **Modals and sheets offer a clear escape** — Escape key, visible close button, click-on-scrim. Confirm before dismissing with unsaved changes. Focus returns to the trigger after close.

9. **Tables use tabular numerals and consistent alignment** — Numbers right-aligned with `font-mono` and `font-variant-numeric: tabular-nums`. Action columns right-aligned. Sticky headers on long tables. Empty rows show an empty state across the full width.

10. **Toasts speak to screen readers** — `aria-live="polite"` for non-urgent updates. Auto-dismiss in 3 to 5 seconds. Never steal focus.

11. **Disabled states are programmatically disabled** — Reduced opacity, cursor change, AND the semantic `disabled` attribute. Looks disabled AND refuses input.

## Do / Don't

| Do | Don't |
|---|---|
| Use semantic HTML (`<button>`, `<a>`, `<input>`) | Use `<div onclick="...">` as a button |
| Define states explicitly for every component | Ship only the default state |
| Use compound subcomponents (`Card.Header`, `Table.Row`) | Flatten subcomponents into a single `<Card title="..." />` |
| One primary CTA per context | Two primary CTAs competing in the hero |
| `onPress` (accessibility-friendly) on touch and mouse | `onClick` only (skips touch and keyboard abstractions) |
| Cards earn their elevation | Wrap every block in a `<Card>` |
| Validate forms on `blur` | Validate on every keystroke |
| Provide Escape key, close button, scrim click on modals | Lock the user inside a modal |
| Right-align numeric columns in tables | Mix alignments in numeric data |
| Use sticky headers on long tables | Force users to scroll back to remember column meaning |
| Replace cards with `divide-y` in dense data UI | Use `<Card>` for every dashboard row |
| Use bottom tab bar ≤5 items on small screens | Cram 6+ items in bottom nav |
| Tooltip content keyboard-reachable | Tooltip only on hover (no keyboard, no mobile) |
| Toast uses `aria-live="polite"` | Toast steals focus from current control |
| Skeleton matching layout shape for loading | Generic centered spinner |
| Empty state with composed visual + next action | Blank screen or "No data" |
| Customize component library defaults (radii, colors, shadows) | Ship a component library with its default look untouched |

## Examples

### Button (canonical)
**Use when**: Every clickable action — submit, save, cancel, navigate.
**Variants**: primary, secondary, tertiary, danger, ghost, outline, icon-only.
**Required states**:
- **Default**: visible at rest, clearly affords interaction
- **Hover**: background brightness shift (2 to 4% L), or shadow lift, or color change; 150 to 250ms
- **Active / pressed**: `-translate-y-[1px]` or `scale-[0.98]`; 80 to 150ms
- **Focus**: visible 2 to 4px focus ring; never `outline: none` without replacement
- **Disabled**: 0.38 to 0.5 opacity + `cursor: not-allowed` + `disabled` attribute
- **Loading**: spinner inside button, disable click, optional label swap ("Saving...")
- **Success / error feedback** (optional): brief color flash or icon on async completion

**Anti-patterns**:
- Two primary buttons competing for attention
- Hover-only interactions (touch has no hover)
- Tap target <44pt
- "Get Started" or "Learn More" CTA labels (use specific verbs)
- Scale animations on CTAs (looks toy-like)
- Naked trailing arrow on premium CTAs (wrap in its own circular container)
- Generic icon-only buttons without `aria-label`

**Specs**:
- Font: 14 to 16px, weight 500 to 600
- Padding: 12 to 16px vertical, 24 to 32px horizontal
- Radius: 4 to 12px (sharp), 16 to 24px (soft), 9999px (pill); commit to one and apply consistently
- Primary: filled brand-accent background, white text
- Secondary / ghost: transparent or light-tinted background, optional 1px mid-gray border
- Tertiary: text-only with inline underline on hover
- Touch target: ≥44x44pt

**Premium button-in-button pattern**:
For high-end aesthetic CTAs with a trailing icon, the icon lives inside its own circular wrapper, flush with the main button's right inner padding. Wrapper has its own subtle background and ring. On hover, the wrapper translates 1px up and 1px right, scales up to `scale-105`.

### Input (canonical)
**Use when**: Every form field — text, email, phone, number, date, password.
**Required states**:
- **Default**: visible label above, visible border, visible value (when present)
- **Focus**: focus ring + slight border emphasis
- **Filled / value-present**: label remains visible (no floating-label disappearance)
- **Error**: red color on border + inline error message below + icon
- **Disabled**: reduced opacity + cursor change + `disabled` attribute
- **Read-only**: visually distinct from disabled (often slightly muted background)
- **Loading** (for async validation): subtle spinner inside the input

**Anti-patterns**:
- Placeholder used as the label
- Validation on every keystroke (validation runs on `blur`)
- Floating labels that disappear when user types
- Errors only at top of form with no inline indication
- "Invalid input" without naming the field or fix
- No `<label for>` link

**Specs**:
- Label sits ABOVE the input — always
- Helper text: optional, below the input, even if empty (markup) to prevent layout shift on error
- Error text: below the input, paired with semantic red and an icon
- Padding: 12 to 16px vertical, 12 to 16px horizontal
- Border: 1px solid; `#EAEAEA` light mode, white at 8 to 12% alpha dark mode
- Radius: matches button radius
- Touch target: ≥44px height on mobile
- Required indicator: `*` inline or "(required)"
- `autocomplete` attribute for system autofill
- Semantic input types (`email`, `tel`, `number`, `url`, `date`) so mobile keyboards adapt

### Modal / Dialog (canonical)
**Use when**: Discrete actions requiring focused attention — confirmation, edit, view detail.
**Required states**:
- **Closed**: not rendered (or `display: none`)
- **Opening**: scale + fade entry from trigger source; 250 to 400ms with spring physics
- **Open**: focus trap, scrim, visible close button
- **Closing**: reverse the entry; 60 to 70% of entry duration
- **Loading inside modal**: skeleton matching modal content shape

**Required affordances**:
- Visible close button (44px+ touch target), clearly labeled
- Escape key dismisses
- Click on scrim dismisses (unless work in progress)
- Swipe-down dismisses on mobile sheets
- Focus traps inside modal — Tab cycles through interactive elements
- Focus returns to trigger element on close
- If unsaved changes exist, confirm before dismissing
- Scrim opacity: 40 to 60% black (light mode); page background at 60 to 80% alpha (dark mode)

**Anti-patterns**:
- No close button or escape key handler
- Modal blocks primary flow with no escape
- Stacking modals more than two deep
- Modal used for primary navigation flows (breaks the user's path)
- Heavy entry animations exceeding 500ms
- Modal that doesn't trap focus (Tab leaves the modal)

**Specs**:
- Background: surface color (off-white or near-black depending on mode)
- Border / shadow: tinted shadow matching surface
- Radius: matches card radius (8 to 24px for premium; 0 for brutalist)
- Padding: `p-6` to `p-8` (24 to 32px)
- Max width: 480 to 720px depending on content; full-bleed for high-end modals
- Modal scrim: `bg-black/40` to `bg-black/60`
- Header: title + close button
- Footer: secondary action (cancel) + primary action (confirm)

### Sheet (mobile alternative to modal)
**Use when**: Mobile-specific modal that slides up from below.
**Required affordances**:
- Slide up from bottom with spring physics
- Swipe-down handle visible at top of sheet
- Swipe-down to dismiss (with momentum threshold)
- Visible close button as alternative
- Backdrop fades in behind sheet
- Focus traps inside sheet

**Anti-patterns**:
- Sheet without swipe-down handle (users don't discover the gesture)
- Sheet covering content with no way to peek at what's behind
- Sheet with content that scrolls but body also scrolls behind (locks body scroll)

### Card (canonical)
**Use when**: Elevation communicates hierarchy or grouping. NOT for every block.
**When to ban cards**:
- Dense data UI — use `border-t`, `divide-y`, or negative space instead
- Cockpit-density dashboards — replace cards with hairlines
- Brutalist surfaces — borders only, no shadows

**Required states**:
- **Default**: visible at rest with subtle elevation or border
- **Hover** (if clickable): `translateY(-2px)` to `translateY(-4px)` + shadow elevation shift; 200 to 300ms
- **Pressed** (if clickable): `scale-[0.98]` press feedback
- **Focused** (if clickable): visible focus ring
- **Loading**: skeleton matching card layout
- **Empty**: composed empty state matching card position

**Specs**:
- Padding: 24 to 40px (`p-6` to `p-10`) for premium; 8 to 16px for cockpit
- Border: 1px hairline (`#EAEAEA` light; white at 8 to 12% alpha dark)
- Radius: 8 to 24px (premium soft), 32 to 40px (`rounded-[2rem]` to `rounded-[2.5rem]` for major containers)
- Shadow: tinted to background hue, low opacity (8 to 14% alpha)
- Premium diffuse shadow: `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`

**Premium double-bezel pattern**:
For high-end product surfaces, cards use the double-bezel pattern — outer shell with subtle background and hairline outer border, inner core with distinct background color, inner highlight, and a mathematically calculated smaller radius (e.g., `rounded-[calc(2rem-0.375rem)]`) so inner and outer are visibly concentric.

### Table (canonical)
**Use when**: Tabular data with rows and columns.
**Required affordances**:
- Sortable columns with `aria-sort` indicating current sort
- Sticky headers on long tables (>10 rows)
- Empty state across full width (not a collapsed empty row)
- Loading state: skeleton rows matching layout
- Error state: row-level error with retry
- Responsive collapse on mobile (cards or horizontal scroll, depending on data shape)

**Specs**:
- Numbers right-aligned in `font-mono` with `font-variant-numeric: tabular-nums`
- Action columns right-aligned
- Row hover: subtle background shift (`bg-muted/50`)
- Row height: 40 to 56px (`py-3` to `py-4`)
- Selected row: brand accent background at low opacity + checkbox
- Column headers: 12 to 14px, weight 500 to 600, uppercase or sentence case
- Pagination, page size selector, or infinite scroll for large datasets

**Anti-patterns**:
- Mixing proportional and tabular figures
- Action buttons in the leftmost column (right-align actions)
- Same row height for `<th>` and `<td>` (headers can be tighter)
- Horizontal scroll on mobile without explicit affordance
- Cramming 8+ columns on mobile

### Navbar / Top Nav (canonical)
**Use when**: Persistent navigation on web and mobile.
**Required affordances**:
- Logo top-left, links centered or right-aligned, primary CTA right
- Active state visually highlighted on current page
- Hover state on links (underline, weight, color shift)
- Focus rings on every interactive element
- Mobile collapse: hamburger menu under 768px
- Mega-menu hover-revealed with multi-column groupings (organized by job-to-be-done, not alphabetical)

**Sticky behavior**:
- Sticky from start, OR
- Transparent over hero, opaque on scroll (~100px scroll triggers backdrop-blur + hairline border with 150 to 200ms transition)

**Anti-patterns**:
- Bottom nav with 6+ items
- Bottom nav location changing between pages
- Mystery-meat icon-only nav with no labels
- Mega-menu requiring 3 levels of hover
- Sticky chatbot bubble overlapping primary CTA
- Persistent nav breaking on deep pages (must remain reachable)
- Hide-on-scroll nav that fights user scroll direction

**Specs**:
- Height: 60 to 72px (slim) for marketing; 48 to 64px for product
- Padding: matches outer container insets
- Items: 4 to 7 links + 1 to 2 action buttons (Sign in + primary CTA)
- Mobile: hamburger left or right; full-screen overlay on tap with staggered nav reveal

### Bottom Nav (mobile native)
**Use when**: Mobile native or PWA top-level navigation.
**Required affordances**:
- ≤5 items
- Both icon AND text label per item
- Active state with color + indicator bar or weight change
- Safe area inset at bottom (above home indicator)
- Persists across all top-level screens
- Top-level only — never nest sub-navigation inside

### Form Field (canonical contract)
**Use when**: Composing an input with its label, helper, and error.
**Structure**:
```
<label>...</label>            (above input)
<input />                     (44px+ tall on mobile)
<helper>...</helper>          (below input; markup present even if empty to prevent layout shift)
<error role="alert">...</error>  (below input; appears on validation failure)
```

**Behavior**:
- Validation on `blur` (not on every keystroke)
- Required indicator inline (`*` or "(required)")
- Auto-focus first invalid field on submit failure
- Multi-error summary at top of form with anchor links
- Each anchor link scrolls to and focuses the corresponding field

**Anti-patterns**:
- Placeholder as label
- Errors only at top with no inline marker
- Errors only inline with no aggregated summary
- "Form contains errors" or "Invalid input" copy
- Validation messages that disappear when user starts typing

### Toast / Notification (canonical)
**Use when**: System feedback that does not require user action — success confirmation, info, non-blocking errors.
**Required affordances**:
- `aria-live="polite"` for non-urgent (most cases)
- `aria-live="assertive"` or `role="alert"` for urgent errors only
- Auto-dismiss in 3 to 5 seconds
- Visible dismiss button for users who need more time
- Stacks if multiple toasts queued; oldest at top
- Never steals focus from current control
- Slide in from top, top-right, or bottom; 250 to 400ms with spring physics

**Anti-patterns**:
- Toast covers primary CTA
- Toast persists indefinitely (use a banner or alert instead)
- Toast steals keyboard focus
- Toast with destructive action — destructive needs confirmation, not a transient

**Specs**:
- Width: 320 to 480px
- Padding: 16 to 24px
- Background: surface color with shadow
- Icon: matches semantic state (success / error / warning / info)
- Text: 14 to 16px, weight 500
- Action button (optional): "Undo" or "Retry" inline

### Chart (canonical)
**Use when**: Data visualization with quantitative content.
**Required affordances**:
- Tooltip on hover (web) AND tap (mobile) AND keyboard focus
- Legend visible near the chart, never detached below a scroll fold
- Legend clickable to toggle series visibility
- Empty state: "No data yet" + guidance (not a blank chart frame)
- Loading state: skeleton or shimmer placeholder
- Error state: error message with retry action
- Responsive reflow on mobile (horizontal bar instead of vertical, fewer ticks)
- Screen reader summary: `aria-label` describing the chart's key insight
- Data table alternative for accessibility — every chart has a parallel table

**Chart type selection**:
- Trend over time → line chart
- Comparison → bar chart (vertical for 5-15 categories, horizontal for many or long labels)
- Proportion → pie or donut (≤5 categories; never more)
- Distribution → histogram
- Correlation → scatter plot

**Color rules**:
- Colorblind-safe palettes (Viridis, Cividis, Magma — perceptually uniform)
- Diverging: blue → gray → red (never red → green)
- Sequential: single-hue gradient
- Qualitative: max 7 to 8 distinct hues
- Pattern/texture supplements color
- Data lines: 3:1 contrast minimum; text labels 4.5:1

**Anti-patterns**:
- Color as the only signal
- Pie charts with >5 wedges
- 3D charts (distort perception)
- Tooltips only on hover (no keyboard, no mobile)
- Y-axis that doesn't start at zero on bar charts (misleading)
- Charts without empty/loading/error states
- Charts that don't reflow on mobile

### Accordion / FAQ (canonical)
**Use when**: Hiding secondary information until user requests it.
**Required affordances**:
- Visible expand affordance — sharp `+` and `-` icons preferred over chevrons in minimalist aesthetic
- Click anywhere on the row toggles
- `aria-expanded` attribute tracks state
- Smooth height transition (250 to 400ms)
- Keyboard accessible (Enter and Space toggle)

**Specs (minimalist)**:
- Strip container boxes — separate items with `border-bottom: 1px solid #EAEAEA`
- Toggle icon: clean `+` and `-`
- Item title: 16 to 18px, weight 500
- Item body: 14 to 16px, weight 400, line-height 1.55 to 1.7

### Tabs (canonical)
**Use when**: Switching between related views within the same context.
**Required affordances**:
- `role="tablist"` on container; `role="tab"` and `aria-controls` on each tab; `role="tabpanel"` on each panel
- `aria-selected="true"` on active tab; only one selected at a time
- Keyboard navigation: arrow keys to move between tabs, Home / End for first / last
- Visible active indicator (color, weight, underline bar)
- Tabs reflow or scroll on mobile (no truncation)

**Anti-patterns**:
- Tabs that auto-rotate without manual control
- Tabs as a substitute for primary navigation
- Tabs that hide critical content (use cards or sections instead)

### Dropdown / Select (canonical)
**Use when**: User picks one value from a known set.
**Required affordances**:
- Visible label above
- Click toggles open
- Escape closes
- Arrow keys navigate options
- Selected option visible in trigger
- For long lists, use Combobox (search-as-you-type)
- Focus traps in open dropdown

### Combobox (canonical, for long lists)
**Use when**: User picks from a list too long to scan visually.
**Required affordances**:
- Search-as-you-type
- Filtered results render below input
- Arrow keys navigate filtered results
- Enter selects, Escape closes
- Empty state: "No matches" with guidance
- `aria-activedescendant` tracks focused option

### Skeleton (canonical loading state)
**Use when**: Operations longer than 300ms.
**Required affordances**:
- Match the eventual layout shape (not generic rectangles)
- Shimmer animation across the block at 1.5 to 2s loops
- Honor `prefers-reduced-motion: reduce` — replace shimmer with opacity pulsing
- Block click and interaction until loaded

**Anti-patterns**:
- Generic centered spinner blocking content for 3+ seconds with no progress
- Skeleton that doesn't match the eventual layout (layout shift on resolve)
- Shimmer that runs forever (cap at 5 seconds, then show error state)

### Avatar (canonical)
**Use when**: Representing users or entities.
**Specs**:
- Circle or rounded-square
- 24px / 32px / 48px / 64px / 96px size scale
- Initials fallback (first letter of name) when no photo
- Background color derived from name hash for variation
- Decorative status indicator (online dot) at bottom-right corner; 8 to 12px diameter

**Anti-patterns**:
- Generic egg silhouette or default user icon
- Lorem Ipsum names ("John Doe")

### Badge / Chip / Pill (canonical)
**Use when**: Status, category, count, or selection.
**Specs**:
- Background: pastel pair (light + paired text color) for semantic states
- Padding: 4 to 8px vertical, 8 to 12px horizontal
- Radius: 9999px (pill) — the pill shape is reserved for this component
- Typography: 12 to 13px, weight 500 to 600, optional uppercase with +0.06em tracking
- Maximum width before truncation: 200px

**Pastel pair system**:
- Pale red `#FDEBEC` with text `#9F2F2D` — destructive / warning
- Pale blue `#E1F3FE` with text `#1F6C9F` — informational
- Pale green `#EDF3EC` with text `#346538` — success
- Pale yellow `#FBF3DB` with text `#956400` — pending / caution

## Tokens / values

### Component sizing scale
- Small: 32px (button height, input height)
- Default: 40 to 44px
- Large: 48 to 56px
- Mobile touch: 44px minimum

### Component radii
- Sharp (brutalist): 0
- Crisp (minimalist): 4 to 12px
- Default (most products): 8 to 12px
- Soft (premium): 16 to 24px
- Major bento containers (high-end): 32 to 40px (`rounded-[2rem]` to `rounded-[2.5rem]`)
- Pills and badges: 9999px (`rounded-full`)

### Component padding
- Tight (cockpit): 4 to 8px
- Default: 12 to 16px
- Comfortable (premium): 24 to 40px (`p-6` to `p-10`)
- Major bento: 40 to 64px (`p-10` to `p-16`)

### Button specs
- Font: 14 to 16px, weight 500 to 600
- Padding: 12 to 16px vertical, 24 to 32px horizontal
- Radius: matches component radii
- Touch target: ≥44x44pt
- Variants: primary (filled), secondary (outline or ghost), tertiary (text-only), danger, ghost
- Loading state: spinner inside; disable click

### Form field specs
- Label: above input, 14 to 16px, weight 500
- Input height: 40 to 48px (mobile ≥44px)
- Input padding: 12 to 16px
- Helper text: 13 to 14px, weight 400, mid-gray
- Error text: 13 to 14px, weight 500, semantic red
- Error placement: below input
- Validation timing: on `blur`
- Auto-focus first invalid on submit failure

### Modal specs
- Max width: 480 to 720px (standard); full-bleed for high-end
- Padding: 24 to 32px (`p-6` to `p-8`)
- Scrim opacity: 40 to 60% black (light); page background at 60 to 80% alpha (dark)
- Entry: 250 to 400ms with spring physics
- Exit: 60 to 70% of entry duration
- Focus trap required
- Escape key handler required
- Maximum 2 modals deep — never more

### Card specs
- Padding: 24 to 40px (premium); 8 to 16px (cockpit)
- Border: 1px hairline (`#EAEAEA` light; white at 8 to 12% alpha dark)
- Radius: 8 to 12px (default); 16 to 24px (premium); 32 to 40px (major bento)
- Shadow: tinted to background hue, 8 to 14% alpha; or pure hairline border
- Hover (clickable): `translateY(-2px)` to `translateY(-4px)` + shadow lift; 200 to 300ms
- Press (clickable): `scale-[0.98]`

### Table specs
- Row height: 40 to 56px
- Header height: 36 to 48px (slightly tighter than rows)
- Numbers: right-aligned, `font-mono`, tabular figures
- Action columns: right-aligned
- Sticky headers on >10 rows
- Selected row: brand accent at low opacity + checkbox
- Empty state: full-width row with composed empty state
- Mobile: collapse to cards or enable horizontal scroll (with visible affordance)

### Toast specs
- Width: 320 to 480px
- Padding: 16 to 24px
- Background: surface color with shadow
- Auto-dismiss: 3 to 5 seconds
- `aria-live="polite"` default; `aria-live="assertive"` for urgent only
- Position: top, top-right, or bottom (consistent within product)
- Never overlaps primary CTA

### Navbar specs
- Height: 60 to 72px (marketing); 48 to 64px (product)
- Items: 4 to 7 links + 1 to 2 action buttons
- Mobile collapse threshold: ≤768px → hamburger
- Sticky behavior: from-start OR transparent-to-opaque on scroll (150 to 200ms transition)

### Bottom nav specs (mobile native)
- Max 5 items
- Icon + text label per item
- Safe area inset at bottom
- Active state: color + indicator bar or weight
- Persists on all top-level screens

### Tab specs
- `role="tablist"`, `role="tab"`, `role="tabpanel"` on respective elements
- `aria-selected` tracks state
- Arrow key navigation
- Active indicator: color + weight + underline bar
- Mobile: scroll or reflow (no truncation)

### Chart specs
- Color: diverging (blue-gray-red), sequential, or colorblind-safe qualitative
- Max 7 to 8 distinct hues
- Pattern / texture supplement
- Tooltip: hover + tap + keyboard accessible
- Legend: visible near chart, clickable to toggle series
- Empty / loading / error states required
- Screen reader: `aria-label` summary + data table alternative
- Responsive: reflow on mobile (horizontal bar, fewer ticks)
- Y-axis on bar charts: starts at zero (mandatory)

### Skeleton specs
- Match eventual layout shape (not generic rectangles)
- Shimmer at 1.5 to 2s loops
- Opacity pulse fallback under `prefers-reduced-motion`
- Cap at 5 seconds, then error state

### Avatar specs
- Sizes: 24 / 32 / 48 / 64 / 96px
- Shape: circle or rounded-square
- Initials fallback
- Background color derived from name hash
- Status indicator: 8 to 12px bottom-right corner

### Banned component patterns
- Default component library look shipped without customization (a known generic tell)
- Generic `<div>` used as `<button>`
- Placeholder-only labels
- Floating labels that disappear when user types
- Validation on every keystroke
- "Get Started" / "Learn More" as primary CTA labels
- Two primary buttons in the same view
- Modal without Escape key or close button
- Stacking modals more than two deep
- Modal used for primary navigation flows
- Bottom nav with 6+ items
- Bottom nav location changing between pages
- Mystery-meat icon-only nav with no labels
- Tooltip only on hover (no keyboard, no mobile)
- Toast that steals focus
- Pie charts with >5 wedges
- 3D charts
- Charts without empty / loading / error states
- Skeleton that doesn't match eventual layout
- Card overuse — wrapping every block in a `<Card>`
- Cards in cockpit-density UIs (use `divide-y` instead)
- Generic centered spinner blocking content
- Hover-only interactions on primary actions
- Tap targets <44pt without expanded hit area
- Custom containers used as buttons without semantic role and keyboard support
- Generic "egg" avatar silhouettes or default user icons
- Sticky chatbot bubble overlapping primary CTA

### Component documentation requirements
Every component documents:
- Purpose and use cases
- All available variants
- All required states (default, hover, pressed, focus, disabled, loading, error, empty)
- Accessibility behavior (keyboard, screen reader, ARIA)
- Anti-patterns and when not to use
- Code example with compound subcomponents

## Checklist (severity-tagged)

- [ ] Every interactive component ships with all required states (severity: High)
- [ ] Semantic native controls used (`<button>`, `<a>`, `<input>`, `<table>`) (severity: Critical)
- [ ] Compound component pattern used for multi-part components (severity: Medium)
- [ ] One primary CTA per context — no competing primaries (severity: High)
- [ ] All buttons have visible focus ring (severity: Critical)
- [ ] All buttons have hover and active states (severity: High)
- [ ] All buttons meet 44pt touch target minimum (severity: Critical)
- [ ] Form inputs have visible `<label for>` (severity: Critical)
- [ ] Placeholder is never used as the label (severity: Critical)
- [ ] Validation runs on `blur`, not on every keystroke (severity: High)
- [ ] First invalid field auto-focuses on submit failure (severity: High)
- [ ] Multi-error summary at top of form with anchor links (severity: Medium)
- [ ] Error messages name the cause AND the fix (severity: Critical)
- [ ] Modal has Escape key, visible close button, scrim click (severity: Critical)
- [ ] Modal traps focus while open (severity: Critical)
- [ ] Focus returns to trigger element on modal close (severity: High)
- [ ] Maximum 2 modals deep — never more (severity: High)
- [ ] Cards used only when elevation communicates hierarchy (severity: Medium)
- [ ] Dense data UI uses `divide-y` or `border-t`, not `<Card>` wrapping (severity: Medium)
- [ ] Table numbers right-aligned in tabular figures (severity: Medium)
- [ ] Table action columns right-aligned (severity: Medium)
- [ ] Sticky table headers on tables >10 rows (severity: Medium)
- [ ] Table sortable columns include `aria-sort` (severity: High)
- [ ] Bottom nav ≤5 items with icon + text label (severity: High)
- [ ] Bottom nav location consistent across pages (severity: High)
- [ ] Navbar persistent and reachable from deep pages (severity: Medium)
- [ ] Active nav state visually highlighted (severity: Medium)
- [ ] Toast uses `aria-live="polite"`, does not steal focus (severity: High)
- [ ] Toast auto-dismisses in 3 to 5 seconds (severity: Medium)
- [ ] Chart tooltip works on hover, tap, AND keyboard focus (severity: Critical)
- [ ] Chart has empty / loading / error states (severity: High)
- [ ] Chart has `aria-label` summary AND data table alternative (severity: Critical)
- [ ] Chart palettes survive color-blindness (severity: Critical)
- [ ] Skeleton matches eventual layout shape (severity: High)
- [ ] Skeleton honors `prefers-reduced-motion` (severity: High)
- [ ] Disabled states use opacity + cursor + `disabled` attribute (severity: High)
- [ ] Component library defaults customized — radii, colors, shadows tuned to brand (severity: Medium)
- [ ] No generic egg avatar silhouettes (severity: High)
- [ ] Avatar initials fallback when no photo (severity: Medium)
- [ ] Pill / chip pastel pairs hold 4.5:1 contrast (severity: Critical)
- [ ] Accordion uses sharp `+` / `-` icons in minimalist aesthetic (severity: Cosmetic)
- [ ] Tabs are keyboard navigable (arrow keys, Home/End) (severity: High)
- [ ] Combobox for long lists (>10 items typically) (severity: Medium)
- [ ] Every component documents its states and anti-patterns (severity: Medium)

## Related

- See **accessibility.md** for ARIA roles, focus management, and keyboard navigation contracts.
- See **interaction.md** for tap feedback, hover states, and touch target sizes.
- See **motion.md** for state transition timing and spring physics on modals.
- See **typography.md** for label, helper text, and button typography.
- See **color.md** for state tokens (default, hover, active, focus, disabled).
- See **spacing.md** for component padding by density mode.
- See **dashboards.md** for table, chart, and data-dense component patterns.
- See **copy.md** for button labels, error messages, and toast copy.
