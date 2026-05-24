# UI/UX Pattern Library

A comprehensive reference for designing professional, accessible, and performant interfaces across web and mobile. Rules are prioritized 1 (most critical) through 10. Follow categories 1-3 as non-negotiables; treat 4-9 as the difference between a working UI and a polished one; treat 10 as the discipline that distinguishes data products.

---

## 1. Accessibility (Critical)

Accessibility is a baseline, not a nice-to-have. These rules block release.

### Color & Contrast
- **Color contrast:** Minimum 4.5:1 ratio for normal text. Large text (18pt+ regular, or 14pt+ bold) may use 3:1.
- **AAA target:** Foreground/background pairs should meet 7:1 (AAA) where feasible; never less than 4.5:1 (AA).
- **Color not only:** Never convey information by color alone. Always pair a color signal with an icon, text, or pattern. Error states need a red color AND an icon AND a text message.
- **Functional color discipline:** Error red, success green, warning amber must always include icon or text — color carries reinforcement, not meaning.

### Focus & Keyboard
- **Focus states:** Visible focus rings on every interactive element. Width 2-4px, high-contrast against background. Never `outline: none` without a replacement.
- **Keyboard navigation:** Tab order must match visual order. Every interactive control reachable and operable by keyboard alone.
- **Skip links:** Provide a "Skip to main content" link as the first focusable element for keyboard users on every page with significant chrome.
- **Keyboard shortcuts:** Preserve system and assistive-technology shortcuts. If you offer drag-and-drop, also provide a keyboard alternative.
- **Focus management on route change:** After a page transition, move focus to the main content region so screen reader users know where they are.
- **Focus on error:** After form submit fails, auto-focus the first invalid field.

### Semantic Structure
- **Heading hierarchy:** Sequential h1 -> h2 -> h3 -> h4 -> h5 -> h6. Never skip levels.
- **Form labels:** Every input gets a visible `<label for="...">`. Placeholder text is not a label.
- **Aria labels:** Icon-only buttons need `aria-label`. Native apps need `accessibilityLabel`.
- **Alt text:** Every meaningful image gets descriptive alt text. Decorative images get `alt=""`.
- **VoiceOver / screen reader:** Provide meaningful `accessibilityLabel` and `accessibilityHint`. Reading order must be logical.

### Adaptive Behavior
- **Dynamic Type:** Support system text scaling. Layouts must not truncate or break as text grows. Test at the largest accessibility text size.
- **Reduced motion:** Respect `prefers-reduced-motion`. Reduce or disable animations on request. Never opt the user back in by default.
- **Escape routes:** Modals and multi-step flows must offer a clearly labeled cancel or back action.

### Anti-Patterns
- Removing focus rings without replacement.
- Icon-only buttons with no `aria-label`.
- Text below 12px in body content.
- Gray-on-gray, low-contrast text.
- Communicating state through color alone (no icon, no text).
- Disabling pinch-zoom via `user-scalable=no`.

---

## 2. Touch & Interaction (Critical)

These rules apply to every tappable, clickable, or gestural surface.

### Touch Target Standards
- **Minimum size:** 44x44pt on iOS, 48x48dp on Android, 44x44px on web. Extend the hit area beyond the visual bounds via `hitSlop` or padding if the icon is smaller.
- **Touch spacing:** Minimum 8px / 8dp gap between adjacent touch targets.
- **No precision required:** Never require pixel-perfect taps on small icons or thin edges.
- **Touch-friendly inputs:** Mobile input field height >=44px.
- **Safe-area awareness:** Keep primary touch targets clear of notch, Dynamic Island, home indicator, and screen edges.

### Feedback & Latency
- **Tap feedback speed:** Visible response within 100ms of tap.
- **Press feedback:** Ripple, opacity change, elevation change, or color flash on press — pick one and apply consistently. Material state layers are a solid baseline.
- **Input latency:** Keep tap/scroll latency under 100ms.
- **Loading buttons:** Disable button during async operations; show spinner or progress.
- **Error feedback:** Clear, specific error message near the problem field.
- **Cursor pointer (web):** Add `cursor: pointer` to clickable elements.

### Hover, Tap, and Gestures
- **Hover vs tap:** Primary interactions use click/tap. Never rely on hover alone — touch devices have no hover.
- **Gesture conflict prevention:** One primary gesture per region. Avoid nested tap/drag conflicts.
- **Gesture alternative:** Always provide a visible control for any critical action. Never gesture-only.
- **Standard gestures:** Use platform-standard gestures (swipe-back on iOS, pinch-zoom, predictive back on Android). Don't redefine them.
- **System gestures:** Don't block system gestures (Control Center swipe, back swipe, etc.).
- **Tap delay (web):** Use `touch-action: manipulation` to remove the 300ms double-tap-zoom delay.
- **Drag threshold:** Use a movement threshold (typically 8-12px) before starting a drag to prevent accidental drags.
- **Swipe clarity:** Swipe actions need a visible affordance (chevron, label, or onboarding hint).

### Haptics & Native Feel
- **Haptic feedback:** Use haptic on confirmations and important actions. Avoid overuse — haptic on every tap is exhausting.
- **Disabled state:** Disabled elements use reduced opacity (0.38-0.5) + cursor change + semantic `disabled` attribute.
- **Semantic native controls:** Use `Button`, `Pressable`, native equivalents. Generic containers used as buttons break a11y.

### Anti-Patterns
- Hover-only interactions.
- Instant state changes with 0ms animation.
- Tiny tap targets (<44pt) without expanded hit area.
- Overlapping gestures causing accidental actions.
- Controls that look tappable but do nothing (no disabled state).

---

## 3. Performance (High)

Perceived performance is design. Every blocked thread is a UX bug.

### Images & Media
- **Image optimization:** Use WebP or AVIF. Provide responsive sources via `srcset` / `sizes`.
- **Image dimensions:** Always declare `width`/`height` or use `aspect-ratio` to prevent layout shift (CLS < 0.1).
- **Lazy load below the fold:** Use `loading="lazy"` for below-fold images and heavy media.
- **Network fallback:** Offer degraded modes on slow networks — lower-res images, fewer animations.

### Fonts
- **Font loading:** Use `font-display: swap` or `font-display: optional`. Avoid invisible text (FOIT).
- **Font preload:** Preload only critical fonts. Don't preload every variant.

### CSS & JS Bundles
- **Critical CSS:** Prioritize above-the-fold CSS. Inline critical CSS or load it early.
- **Lazy loading:** Lazy load non-hero components via dynamic import or route-level code splitting.
- **Bundle splitting:** Split code by route or feature. Use React Suspense / dynamic imports.
- **Third-party scripts:** Load async or defer. Audit ruthlessly — remove what's not earning its weight.

### Rendering & Layout
- **Reduce reflows:** Avoid frequent layout reads/writes. Batch DOM reads, then writes.
- **Content jumping:** Reserve space for async content. Reduce Cumulative Layout Shift.
- **Layout shift avoidance:** Animate via `transform` and `opacity`. Never animate `width`, `height`, `top`, `left`.
- **Virtualize lists:** 50+ items must virtualize.
- **Main thread budget:** Keep per-frame work under 16ms for 60fps. Move heavy tasks to workers.

### Loading States
- **Progressive loading:** Use skeleton screens or shimmer for operations longer than 1 second. Avoid long blocking spinners.
- **Debounce and throttle:** Use for high-frequency events — scroll, resize, keystroke input.
- **Offline support:** Provide offline messaging and a basic fallback.

### Anti-Patterns
- Animating layout-affecting properties.
- Cumulative Layout Shift from unsized images.
- Blocking spinners that hide content for 3+ seconds with no progress indication.
- Loading 12 third-party scripts on page load.

---

## 4. Style Selection (High)

Pick one design language and commit to it across the product.

### Core Principles
- **Style match:** Match style to product type. Fintech needs trust signals; gaming needs energy.
- **Consistency:** Same style across all pages. Don't mix glassmorphism on one screen and brutalism on the next.
- **No emoji icons:** Use SVG icons (Heroicons, Lucide, Phosphor, Feather). Never emojis as structural icons.
- **Color palette from product:** Choose palette from product and industry, not personal taste.
- **Effects match style:** Shadows, blur, radius all aligned with chosen language. Don't slap heavy shadows on a flat design.

### Cross-Platform Fit
- **Platform adaptive:** Respect iOS HIG and Material Design idioms — navigation, controls, typography, motion. iOS uses Tab Bar; Android uses Top App Bar.
- **System controls:** Prefer native or system controls. Customize only when branding genuinely requires it.
- **Icon style consistent:** One icon set across the product. Same stroke width, same corner radius, same visual language.

### Visual Discipline
- **State clarity:** Hover, pressed, disabled — all visually distinct, all on-style.
- **Elevation consistent:** Use a consistent elevation scale. Cards = level 1, sheets = level 2, modals = level 3. No random shadow values.
- **Dark mode pairing:** Design light and dark variants together. Keep brand, contrast, and style consistent across both.
- **Blur purpose:** Use blur to indicate background dismissal (modals, sheets), not as decoration.
- **Primary action:** Each screen has exactly one primary CTA. Secondary actions are visually subordinate.

### Anti-Patterns
- Mixing flat icons with skeuomorphic icons in the same product.
- Emojis used as navigation icons.
- Random shadow values per component.
- Multiple primary buttons competing for attention on one screen.

---

## 5. Layout & Responsive (High)

Design mobile-first. Scale up. Never the reverse.

### Viewport & Breakpoints
- **Viewport meta:** `width=device-width, initial-scale=1`. Never `user-scalable=no`.
- **Mobile-first:** Design for 375px first. Layer up to tablet (768), laptop (1024), desktop (1440).
- **Breakpoint consistency:** Use a systematic scale — 375 / 768 / 1024 / 1440. Don't invent breakpoints per-component.
- **Container width:** Consistent max-width on desktop — typically `max-w-6xl` or `max-w-7xl`.
- **Adaptive gutters:** Increase horizontal insets on larger widths and in landscape. Don't keep the same narrow gutter everywhere.

### Text & Reading
- **Readable font size:** Minimum 16px body text on mobile (avoids iOS auto-zoom on input focus).
- **Line length control:** Mobile 35-60 characters per line; desktop 60-75.
- **Readable text measure on tablets:** Avoid edge-to-edge paragraphs on tablets — limit measure for readability.

### Spacing System
- **Spacing scale:** 4pt or 8dp incremental system. Stick to 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64.
- **Touch density:** Component spacing comfortable for touch — not cramped, not so loose it breaks rhythm.
- **8dp spacing rhythm:** Consistent 4/8dp system for padding, gaps, and section spacing.
- **Section spacing hierarchy:** Define clear vertical rhythm tiers — 16 / 24 / 32 / 48 — by hierarchy level.

### Layout Behavior
- **No horizontal scroll:** Content must fit viewport width on mobile.
- **Z-index management:** Defined scale — 0 / 10 / 20 / 40 / 100 / 1000.
- **Fixed element offset:** Fixed navbar or bottom bar must reserve safe padding for content beneath.
- **Scroll behavior:** Avoid nested scroll regions that fight the main scroll.
- **Viewport units:** Prefer `min-h-dvh` over `100vh` on mobile (handles dynamic browser chrome).
- **Orientation support:** Layout readable and operable in landscape.
- **Content priority:** Show core content first on mobile; fold or hide secondary content.
- **Visual hierarchy:** Use size, spacing, contrast — not color alone.

### Safe Areas (Mobile)
- **Safe-area compliance:** Respect top and bottom safe areas for fixed headers, tab bars, and CTA bars.
- **System bar clearance:** Add spacing for status, navigation bars, and gesture home indicator.
- **Scroll and fixed element coexistence:** Add content insets so lists aren't hidden behind sticky bars.

### Anti-Patterns
- Disabling zoom via viewport meta.
- Fixed pixel widths on container that don't reflow.
- Horizontal scroll on mobile body content.
- Same narrow gutter on phone and tablet.

---

## 6. Typography & Color (Medium)

Typography and color carry meaning. Build a system; reference it everywhere.

### Type Scale
- **Base size:** 16px body minimum.
- **Line height:** 1.5 to 1.75 for body text.
- **Line length:** 65-75 characters per line.
- **Font pairing:** Match heading and body personalities. Don't pair Playfair with Comic Sans.
- **Font scale:** Consistent ratio — 12 / 14 / 16 / 18 / 24 / 32 / 48 / 64.
- **Text styles system:** Use platform type system — iOS 11 Dynamic Type styles or Material 5 type roles (display, headline, title, body, label).
- **Weight hierarchy:** Bold headings (600-700), Regular body (400), Medium labels (500). Weight reinforces hierarchy.
- **Letter spacing:** Respect platform defaults. Avoid tight tracking on body text.
- **Number tabular:** Tabular/monospaced figures for data columns, prices, timers — prevents layout shift on count-up.
- **Truncation strategy:** Prefer wrapping. When truncating, use ellipsis and provide full text via tooltip or expand.

### Color System
- **Contrast readability:** Darker text on light backgrounds. `slate-900` on white, not `slate-500` on white.
- **Color semantic:** Define semantic tokens (`primary`, `secondary`, `error`, `surface`, `on-surface`) — not raw hex in components.
- **Color dark mode:** Dark mode uses desaturated tonal variants, not pure inversion. Test contrast separately for dark.
- **Color accessible pairs:** Foreground/background pairs verified at 4.5:1 (AA) or 7:1 (AAA).
- **Color not decorative only:** Error red and success green need icon or text alongside the color.
- **Token-driven theming:** Semantic color tokens mapped per theme across all surfaces, text, and icons. No hardcoded per-screen hex values.

### Whitespace
- **Whitespace balance:** Use whitespace intentionally to group related items and separate sections. Avoid visual clutter.

### Anti-Patterns
- Text smaller than 12px in body.
- Gray-on-gray combinations.
- Raw hex values in component code instead of semantic tokens.
- Inverted dark mode (white becomes pure black).
- Same letter-spacing on display type and body text.

---

## 7. Animation (Medium)

Motion expresses cause and effect. If it doesn't communicate, cut it.

### Timing
- **Duration timing:** 150-300ms for micro-interactions. Complex transitions <=400ms. Avoid >500ms.
- **Easing:** `ease-out` for entering, `ease-in` for exiting. Avoid linear for UI transitions.
- **Exit faster than enter:** Exit animations 60-70% of enter duration. Feels more responsive.
- **Spring physics:** Prefer spring or physics-based curves over cubic-bezier for natural feel.
- **Stagger sequence:** Stagger list/grid item entrance by 30-50ms per item. Avoid all-at-once or too-slow reveals.
- **Opacity threshold:** Fading elements shouldn't linger at opacity below 0.2. Fade fully or stay visible.

### Performance & Constraints
- **Transform performance:** Use `transform` and `opacity` only. Never animate `width`, `height`, `top`, `left`.
- **Layout shift avoid:** Animations must not cause layout reflow or CLS.
- **Excessive motion:** Animate 1-2 key elements per view max.
- **Motion meaning:** Every animation expresses a cause-effect relationship. Not decoration.
- **Interruptible:** Animations must be interruptible. User tap or gesture cancels in-progress animation immediately.
- **No blocking animation:** Never block user input during an animation. UI stays interactive.

### Specific Patterns
- **State transition:** Hover, active, expanded, collapsed, modal — animate smoothly, never snap.
- **Continuity:** Page/screen transitions maintain spatial continuity — shared element, directional slide.
- **Parallax subtle:** Use sparingly. Must respect reduced-motion. Don't disorient.
- **Shared element transition:** Use hero transitions between screens for visual continuity.
- **Modal motion:** Modals and sheets animate from their trigger source — scale+fade or slide-in.
- **Navigation direction:** Forward navigation animates left or up; backward animates right or down. Consistent.
- **Fade crossfade:** Use crossfade for content replacement within the same container.
- **Scale feedback:** Subtle scale (0.95-1.05) on press for tappable cards and buttons. Restore on release.
- **Gesture feedback:** Drag, swipe, pinch — real-time visual response tracking the finger.
- **Hierarchy motion:** Translate/scale direction expresses hierarchy — enter from below = deeper, exit upward = back.
- **Loading states:** Show skeleton or progress indicator when loading exceeds 300ms.

### System Consistency
- **Motion consistency:** Unify duration and easing tokens globally. All animations share one rhythm.

### Anti-Patterns
- Decorative-only animation.
- Animating `width` or `height`.
- No reduced-motion respect.
- Linear easing on every transition.
- Snapping state changes.

---

## 8. Forms & Feedback (Medium)

Forms are where products win or lose users. Make every field forgiving.

### Labels & Inputs
- **Input labels:** Visible label per input. Placeholder text is not a label.
- **Input helper text:** Persistent helper text below complex inputs. Not just placeholder.
- **Required indicators:** Mark required fields — asterisk or "(required)" inline.
- **Input type keyboard:** Use semantic input types (`email`, `tel`, `number`, `url`, `date`) so mobile keyboards adapt.
- **Password toggle:** Show/hide toggle for password fields.
- **Autofill support:** Use `autocomplete` (web) and `textContentType` (iOS) so the system can autofill.
- **Field grouping:** Group related fields logically. Use `fieldset/legend` or visual grouping.
- **Read-only distinction:** Read-only state is visually and semantically different from disabled.

### Validation & Errors
- **Inline validation:** Validate on `blur`, not on every keystroke. Show error only after user finishes input.
- **Error placement:** Show error below the related field.
- **Error clarity:** Error messages state cause AND fix. Never "Invalid input." Say "Email needs an @ sign. Try again."
- **Error recovery:** Every error includes a clear recovery path — retry button, edit link, help link.
- **Focus management:** After submit fails, auto-focus the first invalid field.
- **Error summary:** For multiple errors, show summary at top with anchor links to each field.
- **Aria-live errors:** Form errors use `aria-live` region or `role="alert"` for screen readers.
- **Contrast feedback:** Error and success colors meet 4.5:1 contrast.

### Submission & Feedback
- **Submit feedback:** Loading state, then success or error state on submit.
- **Success feedback:** Confirm completed actions with checkmark, toast, or color flash.
- **Toast dismiss:** Auto-dismiss toasts in 3-5 seconds.
- **Toast accessibility:** Toasts must not steal focus. Use `aria-live="polite"`.
- **Timeout feedback:** Request timeout shows clear feedback with retry option.

### Flow Patterns
- **Empty states:** Helpful message and clear action when there's no content.
- **Confirmation dialogs:** Confirm before destructive actions.
- **Undo support:** Allow undo for destructive or bulk actions — "Undo delete" toast pattern.
- **Progressive disclosure:** Reveal complex options progressively. Don't overwhelm upfront.
- **Multi-step progress:** Show step indicator or progress bar. Allow back navigation.
- **Form autosave:** Long forms auto-save drafts to prevent data loss on accidental dismissal.
- **Sheet dismiss confirm:** Confirm before dismissing a sheet or modal with unsaved changes.

### Visual States
- **Disabled states:** Reduced opacity (0.38-0.5) + cursor change + semantic `disabled` attribute.
- **Destructive emphasis:** Destructive actions use semantic danger color (red), visually separated from primary actions.
- **Touch-friendly input:** Mobile input height >=44px.

### Anti-Patterns
- Placeholder-only labels.
- Errors only at the top with no inline indication.
- "Invalid input" with no fix suggested.
- Validation on every keystroke (user typing "j" sees "must be valid email").
- Toast that steals focus from the form.

---

## 9. Navigation Patterns (High)

Navigation is the contract between user and product. Break it and trust dies.

### Primary Navigation
- **Bottom nav limit:** Maximum 5 items. Use both icon and text label.
- **Tab bar iOS:** Use bottom Tab Bar for top-level navigation on iOS.
- **Top app bar Android:** Use Top App Bar with navigation icon for primary structure on Android.
- **Nav label icon:** Both icon AND text label. Icon-only nav harms discoverability.
- **Nav state active:** Current location visually highlighted — color, weight, indicator bar.
- **Nav hierarchy:** Primary nav (tabs/bottom bar) is separate from secondary nav (drawer/settings).
- **Bottom nav top-level:** Bottom nav is for top-level screens only. Never nest sub-navigation inside it.
- **Drawer usage:** Drawer/sidebar is for secondary navigation, not primary actions.
- **Adaptive navigation:** Screens >=1024px prefer sidebar; smaller screens use bottom or top nav.

### Back & State
- **Back behavior:** Predictable and consistent. Preserve scroll position and state.
- **State preservation:** Back navigation restores previous scroll position, filter state, and input.
- **Back stack integrity:** Never silently reset the navigation stack or unexpectedly jump to home.
- **Gesture nav support:** Support system gesture navigation — iOS swipe-back, Android predictive back — without conflict.
- **Deep linking:** All key screens reachable via deep link or URL for sharing and notifications.

### Modals & Sheets
- **Modal escape:** Modals and sheets offer clear close/dismiss affordance. Swipe-down to dismiss on mobile.
- **Modal vs navigation:** Modals are not for primary navigation flows. They break the user's path.

### Search & Hierarchy
- **Search accessible:** Search easily reachable from top bar or tab. Provide recent and suggested queries.
- **Breadcrumb web:** Use breadcrumbs for 3+ level deep hierarchies on web.

### Badges & Overflow
- **Tab badge:** Use badges sparingly to indicate unread/pending. Clear after user visits.
- **Overflow menu:** When actions exceed available space, use overflow/more menu instead of cramming.

### Cross-Cutting Rules
- **Navigation consistency:** Placement stays the same across all pages. Don't change by page type.
- **Avoid mixed patterns:** Don't mix Tab + Sidebar + Bottom Nav at the same hierarchy level.
- **Focus on route change:** After page transition, move focus to main content for screen readers.
- **Persistent nav:** Core navigation remains reachable from deep pages. Don't hide it entirely in sub-flows.
- **Destructive nav separation:** Dangerous actions (delete account, logout) visually and spatially separated from normal nav items.
- **Empty nav state:** When a destination is unavailable, explain why instead of silently hiding it.

### Anti-Patterns
- Overloaded bottom nav with 6+ items.
- Broken back behavior — back button takes user to wrong screen.
- No deep links — every share goes to home.
- Bottom nav changes location between pages.
- Modal blocks primary flow with no escape.

---

## 10. Charts & Data (Low)

Charts are UI. Data viz follows the same rules — accessibility, contrast, clarity.

### Chart Selection
- **Chart type:** Match chart type to data type.
  - Trend over time -> line chart
  - Comparison -> bar chart
  - Proportion -> pie or donut (but only for <=5 categories)
  - Distribution -> histogram
  - Correlation -> scatter plot
- **No pie overuse:** Avoid pie/donut for >5 categories. Switch to bar.

### Color & Accessibility
- **Color guidance:** Use accessible color palettes. Avoid red/green-only pairs for colorblind users.
- **Pattern texture:** Supplement color with patterns, textures, or shapes. Color-blind users need a fallback.
- **Contrast data:** Data lines and bars vs background >=3:1. Data text labels >=4.5:1.
- **Gridline subtle:** Grid lines low-contrast (gray-200) so they don't compete with data.
- **Trend emphasis:** Emphasize data trends over decoration. Avoid heavy gradients or shadows that obscure data.

### Labels & Legends
- **Legend visible:** Show legend near the chart, never detached below a scroll fold.
- **Legend interactive:** Legends clickable to toggle series visibility.
- **Direct labeling:** For small datasets, label values directly on the chart to reduce eye travel.
- **Axis labels:** Label axes with units and readable scale. Avoid truncated or rotated labels on mobile.
- **Axis readability:** Axis ticks not cramped. Maintain readable spacing. Auto-skip on small screens.
- **Number formatting:** Locale-aware formatting for numbers, dates, currencies.
- **Time scale clarity:** Time series charts clearly label time granularity (day/week/month). Allow switching.

### Interaction
- **Tooltip on interact:** Tooltips on hover (web) or tap (mobile) showing exact values.
- **Tooltip keyboard:** Tooltip content keyboard-reachable. Don't rely on hover alone.
- **Touch target chart:** Interactive chart elements >=44pt tap area or expand on touch.
- **Focusable elements:** Interactive chart elements (points, bars, slices) keyboard-navigable.
- **Drill-down consistency:** Drill-down interactions maintain a clear back-path and breadcrumb.

### Empty, Loading, Error
- **Empty data state:** Show "No data yet" + guidance. Never a blank chart frame.
- **Loading chart:** Skeleton or shimmer placeholder while data loads. Don't show empty axes.
- **Error state chart:** Data load failure shows error message with retry action. Never a broken chart.

### Responsiveness & Density
- **Responsive chart:** Charts reflow or simplify on small screens — horizontal bar instead of vertical, fewer ticks.
- **Animation optional:** Entrance animations respect `prefers-reduced-motion`. Data must be readable immediately.
- **Large dataset:** 1000+ data points — aggregate or sample. Provide drill-down for detail instead of rendering all.
- **Data density:** Limit information density per chart. Split into multiple charts if needed.

### Data Tables
- **Data table:** Provide table alternative for accessibility — charts alone aren't screen-reader friendly.
- **Sortable table:** Data tables support sorting with `aria-sort` indicating current sort state.

### Screen Reader & Export
- **Screen reader summary:** Provide text summary or `aria-label` describing the chart's key insight.
- **Export option:** Data-heavy products offer CSV or image export.

### Anti-Patterns
- Relying on color alone to convey data meaning.
- Pie charts with 8 wedges.
- Tooltips only on hover (no keyboard, no mobile).
- Charts that don't reflow on mobile.

---

## Design System Methodology

The systematic workflow for moving from a product idea to a coherent visual system.

### Step 1: Analyze Product Requirements

Extract these from any design request:

- **Product type:** Entertainment (social, video, music, gaming), Tool (scanner, editor, converter, AI), Productivity (task, notes, calendar), Service (booking, marketplace), Commerce (e-com, fintech, SaaS), or hybrid.
- **Target audience:** Consumer vs business. Age range. Usage context (commute, leisure, work, in-store).
- **Style keywords:** Playful, vibrant, minimal, dark, content-first, immersive, premium, brutalist, etc. Multiple keywords combined work better than one.
- **Stack:** Web (React, Next.js, Vue, Svelte, HTML/CSS, Tailwind, shadcn/ui), Mobile (React Native, Flutter, SwiftUI), or both.

Use multi-dimensional keywords: `"entertainment social vibrant content-dense"` outperforms `"app"`.

### Step 2: Generate the Design System (Required)

Start every project with a complete design system. The output covers:

1. **Pattern** — which page architecture fits (hero-centric, content-grid, dashboard, dual-pane).
2. **Style** — visual language (glassmorphism, minimalism, brutalism, etc.).
3. **Colors** — palette aligned with industry psychology.
4. **Typography** — font pairing matched to product personality.
5. **Effects** — shadows, blur, radius scale.
6. **Anti-patterns** — what to avoid for this product type.

### Step 3: Persist as MASTER.md + Page Overrides

For multi-page projects, save the design system hierarchically:

```
design-system/
  MASTER.md           # Global Source of Truth (all rules)
  pages/
    dashboard.md      # Page-specific deviations from Master
    checkout.md       # Page-specific deviations from Master
    settings.md
```

**Retrieval rule:**
1. When building a specific page, first check `design-system/pages/{page-name}.md`.
2. If the page file exists, its rules **override** the Master.
3. If not, use `design-system/MASTER.md` exclusively.

Context-aware retrieval prompt template:

```
I am building the [Page Name] page. Read design-system/MASTER.md.
Also check if design-system/pages/[page-name].md exists.
If the page file exists, prioritize its rules.
If not, use the Master rules exclusively.
Now generate the code.
```

### Step 4: Supplement with Detailed Searches

After the system is generated, deep-dive specific dimensions when needed:

| Need | Domain | Example Keywords |
|------|--------|------------------|
| Product type patterns | `product` | `entertainment social`, `saas dashboard` |
| More style options | `style` | `glassmorphism dark`, `brutalism editorial` |
| Color palettes | `color` | `entertainment vibrant`, `fintech trust` |
| Font pairings | `typography` | `playful modern`, `elegant luxury` |
| Chart recommendations | `chart` | `real-time dashboard`, `comparison sales` |
| UX best practices | `ux` | `animation accessibility`, `form validation` |
| Landing page structure | `landing` | `hero social-proof`, `pricing testimonial` |
| Web framework performance | `react` | `waterfall bundle`, `suspense memo` |
| Native interface patterns | `web` | `accessibilityLabel safe-areas` |
| AI / CSS keyword recipes | `prompt` | style name |

### Step 5: Validate Before Implementation

Run UX validation across the rule categories above:
- §1-3 (CRITICAL + HIGH): Accessibility, Touch, Performance.
- Verify on 375px and landscape.
- Test reduced-motion and Dynamic Type at largest size.
- Check dark mode contrast independently from light mode.
- Confirm all touch targets >=44pt and content respects safe areas.

---

## Style Catalog

50+ visual styles. Pick one. Stick with it.

### Glassmorphism
Frosted glass surfaces with backdrop blur, subtle borders, translucent layers. Best for SaaS, modern apps, dashboards over photographic backgrounds. Avoid when high text density or low-end devices matter (blur is expensive).

### Claymorphism
Soft 3D extruded shapes, pillow-like surfaces, soft shadows. Best for kids' apps, learning products, friendly consumer tools. Avoid in dense data products.

### Minimalism
Generous whitespace, restrained color, one or two type sizes per screen, clean alignment. Best for tech, productivity, premium brands, B2B SaaS. Default safe choice.

### Brutalism
Raw structure, exposed grid, monospace, harsh contrast, aggressive type. Best for editorial, music, art, indie products. Avoid where trust signals matter (banking, healthcare).

### Neumorphism
Soft inner and outer shadows creating extruded controls in low-contrast scenes. Best for music players, niche interfaces. Avoid in primary UIs — fails contrast accessibility.

### Bento Grid
Modular grid with cards of varying sizes, tight spacing, content-first composition. Best for portfolios, landing pages, dashboards, feature showcases.

### Dark Mode
Dark surfaces with desaturated accents, lifted backgrounds (#0a0a0a, #18181b), low-glow type. Best for media, gaming, dev tools, late-night use. Always test contrast independently.

### Skeuomorphism
Real-world textures (paper, leather, wood) mimicking physical objects. Best for note apps, audio interfaces, simulators. Avoid in modern productivity UIs.

### Flat Design
No depth, solid colors, no shadows, geometric icons. Best for Material-style products, government, education. Reliable, dated unless paired with strong type.

### Responsive (Adaptive)
Not a style itself — a constraint. Layouts reflow from 375px to 1440px+. Every style above must be responsive.

### Gradient
Mesh gradients, chromatic blends, smooth color transitions. Best for modern brands, fintech, creative tools.

### Bold Typography
Oversized type as the hero element, minimal imagery. Best for announcements, editorial, brand statements.

### Photo-Based
Full-bleed photography with text overlay. Best for lifestyle, e-commerce, travel, hospitality.

### Geometric
Shapes, abstract patterns, structured grids. Best for tech, fintech, B2B.

### Retro / Vintage
Distressed textures, muted color palettes, period-typography. Best for food & beverage, craft, lifestyle brands.

### Neon / Cyberpunk
Dark background with glowing neon accents, high saturation. Best for gaming, music events, late-night entertainment.

### Editorial
Magazine-style grid layouts, pull quotes, strong type hierarchy. Best for media, luxury, longform.

### 3D / Sculptural
Rendered objects, depth, complex shadows. Best for product, tech, immersive launches.

### Duotone
Two-color treatment over imagery. Best for editorial, music, branding.

### Illustrated
Custom illustration as primary visual. Best for SaaS marketing pages, education, healthcare consumer apps.

### Collage
Layered cutouts, mixed media, organic composition. Best for art, creative tools, fashion.

### Style Selection Rules
- Match style to product type. Fintech wants trust (minimal, geometric); gaming wants energy (neon, 3D).
- Consistency over novelty. Pick one and apply it everywhere.
- Effects align with style. Heavy shadows on flat design = noise.
- Light and dark variants designed together, not as an afterthought.

---

## Color Palettes by Product Type

Color choice is industry-coded. Use palettes proven by the category.

### SaaS / Dev Tools
- **Primary:** Cool blues (#2563EB, #4F46E5, #0EA5E9), deep purples (#7C3AED, #6366F1).
- **Neutrals:** Slate or zinc scale (slate-50 -> slate-900).
- **Accents:** Limited — one accent (teal, amber) for CTA differentiation.
- **Mood:** Trust, capability, professional, focused.

### E-commerce / Retail
- **Primary:** Brand-led (varies). Common defaults: black, deep red, navy.
- **Accents:** Sale red (#DC2626), trust green (#16A34A).
- **Neutrals:** Warm grays for product backgrounds.
- **Mood:** Desire, urgency, clarity.

### Healthcare / Medical
- **Primary:** Calming blues (#0284C7), soft greens (#10B981), warm whites.
- **Accents:** Trust-signal blues, never alarming reds for primary CTAs.
- **Neutrals:** Soft warm grays.
- **Mood:** Trust, care, calm, clinical clarity.

### Beauty / Wellness / Spa
- **Primary:** Soft pinks (#FCE7F3, #F9A8D4), nude tones (#FBCFE8, #E5C7B7), sage (#A7C4A0).
- **Accents:** Gold (#D4A574), terracotta (#C97B5C).
- **Neutrals:** Cream, off-white, warm beige.
- **Mood:** Serenity, indulgence, premium.

### Fintech / Banking / Crypto
- **Primary:** Deep blues (#1E40AF, #0F172A), black, electric green for growth.
- **Accents:** Sharp green (gains), red (losses), gold (premium tier).
- **Neutrals:** Cool grays, charcoal.
- **Mood:** Trust, precision, authority, alertness.

### Service (Booking, Marketplace)
- **Primary:** Friendly brand colors — coral (#FF6B6B), warm blue (#3B82F6), teal (#14B8A6).
- **Accents:** Booking-success green, premium gold.
- **Neutrals:** Warm grays.
- **Mood:** Approachable, reliable, energetic.

### Gaming / Entertainment
- **Primary:** Saturated, high-contrast — neon pink (#EC4899), electric purple (#8B5CF6), acid green (#84CC16), cyan (#06B6D4).
- **Accents:** Glow effects, gradient blends.
- **Neutrals:** Deep black, near-black surfaces.
- **Mood:** Energy, immersion, hype.

### Food & Beverage
- **Primary:** Warm earth tones — terracotta (#C2410C), olive (#65A30D), mustard (#CA8A04), deep burgundy.
- **Accents:** Cream, butter yellow.
- **Neutrals:** Warm beige, parchment.
- **Mood:** Appetite, craft, warmth.

### Education / Learning
- **Primary:** Optimistic blues (#3B82F6), encouraging greens (#22C55E), playful yellows (#FACC15).
- **Accents:** Achievement gold, growth purple.
- **Neutrals:** Soft warm whites.
- **Mood:** Optimism, growth, achievement.

### Travel / Hospitality
- **Primary:** Sky blues, sunset oranges, lush greens, sand neutrals.
- **Accents:** Brand-specific (airline branding tends bold red or navy).
- **Neutrals:** Warm sandy beige.
- **Mood:** Escape, wonder, comfort.

### Productivity / Notes / Calendar
- **Primary:** Restrained — single accent color (#3B82F6 or #18181B) over near-monochrome neutrals.
- **Accents:** Subtle category colors (limited palette).
- **Neutrals:** Warm or cool gray scale.
- **Mood:** Focus, clarity, calm.

### Real Estate / Luxury
- **Primary:** Deep charcoal, navy, cream, gold accents.
- **Accents:** Brass, deep emerald.
- **Neutrals:** Warm ivory, soft taupe.
- **Mood:** Premium, established, trusted.

### Kids / Family
- **Primary:** Saturated primary colors — bright blue (#3B82F6), pure red, sunshine yellow.
- **Accents:** Playful pastels.
- **Neutrals:** Pure white, soft cream.
- **Mood:** Joy, safety, play.

### Crypto / Web3
- **Primary:** Black, electric purple (#A855F7), neon green (#22D3EE), white.
- **Accents:** Holographic gradients.
- **Neutrals:** Deep black, charcoal.
- **Mood:** Future, decentralized, premium-tech.

### Color Palette Rules
- Define semantic tokens (`primary`, `secondary`, `error`, `success`, `warning`, `surface`, `on-surface`).
- Build a tonal scale (50, 100, 200, 300, 400, 500, 600, 700, 800, 900) per color.
- Test all foreground/background pairs at 4.5:1.
- Design dark mode variants alongside light mode, not after.
- Avoid pure black (#000) in dark mode — use #0a0a0a or #18181b for softer rendering.

---

## Font Pairings

Pair headings with body fonts that complement, don't compete.

### Elegant / Luxury
- **Playfair Display + Source Sans 3:** Serif heading + clean sans body. Editorial, fashion, premium brands.
- **Cormorant + Inter:** Display serif + neutral sans. Hospitality, beauty.
- **Libre Caslon Display + Libre Franklin:** Classic editorial pairing. Media, longform.
- **Italiana + Inter:** Thin elegant serif + utilitarian sans. Fashion, lookbook.
- **Bodoni Moda + Inter:** Sharp contrast serif + clean sans. Luxury fashion.
- **Cardo + Roboto:** Refined book serif + standard sans. Academic luxury.
- **EB Garamond + Inter:** Humanist serif + sans. Editorial, longform.

### Playful / Friendly
- **Fraunces + Inter:** Quirky display serif + clean sans. Creative SaaS, lifestyle.
- **DM Serif Display + DM Sans:** Family pairing, modern playful. Startups, consumer.
- **Caveat + Inter:** Handwritten + sans. Education, kids.
- **Lobster + Open Sans:** Script + clean sans. F&B, casual brands.
- **Pacifico + Open Sans:** Brush script + sans. Lifestyle, leisure.
- **Quicksand + Quicksand:** Rounded sans across hierarchy. Kids, wellness.
- **Comic Neue + Open Sans:** Friendly + neutral. Education, kids (sparingly).

### Professional / Trust
- **Inter + Inter:** Single-family pairing, modern standard. Tech, SaaS.
- **IBM Plex Sans + IBM Plex Mono:** Sans + mono for tech credibility. Dev tools, fintech.
- **Roboto + Roboto Mono:** Material-aligned. Android-first products.
- **Source Sans 3 + Source Code Pro:** Open-source family. Government, healthcare.
- **Work Sans + Work Sans:** Single neutral family. B2B, agency.
- **Manrope + Manrope:** Modern geometric sans. Tech.
- **Public Sans + Public Sans:** Government-aligned. Civic tech.

### Modern / Tech
- **Geist + Geist Mono:** Modern minimal. Dev tools, AI products.
- **Satoshi + JetBrains Mono:** Geometric + dev mono. Modern startups.
- **Plus Jakarta Sans + Inter:** Modern + standard. Fintech, SaaS.
- **Onest + Inter:** New geometric + standard. Modern web.
- **General Sans + JetBrains Mono:** Versatile + mono. Tech.
- **Hanken Grotesk + Inter:** Grotesque + neutral. Editorial tech.
- **Outfit + Inter:** Rounded geometric + sans. Modern consumer.

### Brutalist / Editorial
- **Space Grotesk + IBM Plex Mono:** Geometric quirky + mono. Indie tech, brutalism.
- **Archivo Black + Inter:** Heavy display + clean body. Music, editorial.
- **Anton + Open Sans:** Condensed display + sans. Sports, news.
- **Bebas Neue + Roboto:** All-caps condensed + sans. Cinema, sports.
- **Druk + Inter:** Bold display + standard. Brutalism, editorial.
- **Monument Grotesk + Inter:** Neo-grotesque + standard. Indie, design.
- **NB International + IBM Plex Mono:** Tech-brutal pairing. Crypto, web3.

### Display / Statement
- **Big Caslon + Inter:** Massive display serif + sans. Luxury announcement.
- **Recoleta + Inter:** Friendly contemporary serif + sans. Health, wellness.
- **Migra + Inter:** Quirky display + sans. Creative brands.
- **PP Editorial New + Inter:** Modern serif + sans. Editorial.
- **PP Neue Montreal + Inter:** Sharp grotesque + sans. Modern luxury.
- **Tobias + Inter:** Refined display serif + sans. Editorial luxury.

### Mono / Technical
- **JetBrains Mono:** Dev-focused mono. Code blocks.
- **Fira Code:** Mono with ligatures. Dev tools.
- **IBM Plex Mono:** Corporate mono. Fintech, enterprise.
- **Geist Mono:** Modern mono. AI products, modern dev tools.
- **Berkeley Mono:** Premium mono. Creative tech.
- **Commit Mono:** Compact mono. Terminal apps.

### Font Pairing Rules
- Maximum 2 typefaces per design unless a clear hierarchy demands a third.
- Pair contrast: serif heading + sans body, or display + neutral body.
- Avoid pairing two display fonts together.
- Single-family pairings (Inter + Inter, weights vary) work for modern minimal products.
- Test at 16px minimum to confirm body readability.
- Variable fonts reduce bundle weight and provide weight/width flexibility.

---

## Product Type Patterns

161 product types group into broad patterns. Each implies a default layout, density, and interaction model.

### Landing Pages
- **Hero-centric:** Single statement, single CTA, full-bleed visual. Best for product announcements, single-purpose tools.
- **Hero + social proof:** Hero, testimonials, logo strip, feature grid, pricing. Best for SaaS marketing pages.
- **Story-driven:** Long scrolling narrative with parallax sections. Best for brand storytelling.
- **Content-first:** Editorial layout, photography-led. Best for media, lifestyle, hospitality.
- **Conversion-focused:** Above-the-fold CTA, minimal navigation, trust badges. Best for SaaS trial signup, lead generation.

### Dashboards
- **Metrics-first:** Top row of KPI cards, chart grid below, table at bottom. Best for analytics tools.
- **Workspace dashboard:** Sidebar navigation, content canvas, contextual right panel. Best for productivity tools.
- **Operations dashboard:** Real-time feed + status grid + alerts. Best for ops, monitoring.
- **Reporting dashboard:** Filter bar, chart grid, drill-down tables. Best for BI tools.

### Admin Panels
- **CRUD-heavy:** Sidebar nav, table list, drawer/modal detail view. Best for content management.
- **Settings-heavy:** Tabbed settings, form-dense panels. Best for configuration tools.
- **Multi-tenant admin:** Org switcher, scoped navigation, audit logs. Best for B2B platforms.

### E-commerce
- **Storefront:** Hero + featured collections + product grid + footer. Best for product-first stores.
- **Marketplace:** Search-first, filter sidebar, infinite product grid. Best for multi-vendor marketplaces.
- **Product detail:** Gallery + price + CTA + variant selector + description + reviews. Best for product depth.
- **Checkout:** Single-step or multi-step. Address, shipping, payment, review.

### SaaS Apps
- **Workspace:** Persistent nav, tabbed workspace, contextual panels. Best for project management, design tools.
- **Document-centric:** Document grid + nested folders + collaborative canvas. Best for docs, design files.
- **Feed-centric:** Activity stream + composer + filters. Best for team comms.
- **Pipeline-centric:** Kanban or pipeline view + cards + detail drawer. Best for CRM, sales.

### Mobile Apps
- **Tab-based:** Bottom tabs (3-5), stack navigation per tab. Best for consumer apps.
- **Drawer-based:** Side drawer for navigation, focused screens. Best for utility apps.
- **Modal-flow:** Linear flow with modal sheets, dismiss-to-cancel. Best for booking, onboarding.
- **Camera-first:** Camera as primary interaction. Best for scanners, AR, photo apps.
- **Map-first:** Map as primary canvas, overlaid cards. Best for travel, location services.

### Content / Media
- **Article-focused:** Headline + lead + body + sidebar. Best for editorial, news.
- **Video-focused:** Full-bleed player + controls + recommendations. Best for streaming.
- **Audio-focused:** Player at top/bottom + library grid + queue. Best for music, podcasts.
- **Social feed:** Composer + scroll feed + reactions + share. Best for social platforms.

### Portfolios
- **Project-grid:** Bento or masonry grid of project tiles. Best for designer portfolios.
- **Long-form case study:** Per-project scroll narrative. Best for agency, freelancer portfolios.
- **Index + detail:** Minimal list + on-click detail expansion. Best for editorial portfolios.

### Blogs
- **Editorial blog:** Featured post + grid below + sidebar. Best for media-style blogs.
- **Tech blog:** Plain reverse-chronological list + post detail. Best for developer blogs.
- **Newsletter blog:** Sign-up first, archive secondary. Best for newsletter-driven publications.

### Service / Booking
- **Service marketplace:** Search-first, provider cards, availability calendar. Best for booking platforms.
- **Booking flow:** Step-by-step (service -> time -> contact -> confirm). Best for appointment booking.
- **Service detail:** Provider profile, services list, reviews, book CTA. Best for individual service providers.

### Healthcare / Wellness
- **Patient portal:** Appointments, records, messaging, billing. Best for healthcare consumer apps.
- **Wellness tracker:** Dashboard of daily metrics + trends + actions. Best for fitness, sleep, nutrition.
- **Telehealth:** Booking + video call + post-visit notes. Best for telemedicine.

### Fintech / Banking
- **Banking dashboard:** Balance prominent, transactions list, transfer CTA. Best for retail banking.
- **Investment tracker:** Portfolio chart + holdings table + transaction history. Best for brokerage.
- **Crypto wallet:** Holdings + send/receive + swap + history. Best for crypto wallets.
- **Budgeting:** Category breakdown + transaction categorization + goals. Best for personal finance.

### Gaming
- **Game lobby:** Hero + game tiles + leaderboard + chat. Best for gaming platforms.
- **In-game UI:** HUD overlay + menus + inventory. Best for game interfaces.
- **Esports / streaming:** Live tile + chat + standings. Best for esports portals.

### Beauty / Spa
- **Service catalog:** Photography-led service tiles + booking CTA + therapist profiles.
- **Treatment detail:** Photo + description + duration + price + book.
- **Spa landing:** Atmospheric hero + service overview + booking + location.

### Education / Learning
- **Course catalog:** Filterable course grid + course detail + enrollment CTA.
- **Course player:** Video + transcript + notes + progress + quiz.
- **Student dashboard:** Enrolled courses + progress + upcoming + community.

### Travel / Hospitality
- **Hotel landing:** Hero + rooms + amenities + booking CTA + location.
- **Travel search:** Search bar + filterable results + map view toggle.
- **Trip planning:** Itinerary builder + bookings + map + chat.

### AI Tools
- **AI search / chat:** Centered input + result stream + history sidebar. Best for AI assistants.
- **AI generator:** Prompt input + result gallery + iteration controls. Best for image/text generation.
- **AI dashboard:** Models, runs, usage, billing. Best for AI infrastructure tools.

### Crypto / Web3
- **DEX / swap:** Token selector + amount + swap CTA + price impact + slippage.
- **NFT marketplace:** Grid of NFTs + filters + bidding + auction history.
- **DAO governance:** Proposals list + voting + delegation + treasury.

### Real Estate
- **Listing grid:** Map + filterable property grid + saved searches.
- **Property detail:** Photo gallery + price + specs + agent contact + map.

### Pattern Selection Rules
- Match pattern to product type, not personal preference.
- Mobile-first patterns differ from desktop — bottom tabs vs sidebar, sheet vs modal, drawer vs flyout.
- Consistency across the product is more important than perfection per screen.

---

## Chart Types & Data Viz

25 chart types. Each has a right and wrong moment.

### Trend Over Time
- **Line chart:** Continuous time series. Stock prices, signups, revenue. Best library: Chart.js, Recharts.
- **Area chart:** Line + filled area. Emphasizes magnitude. Best for cumulative trends.
- **Stacked area:** Multiple series, cumulative. Best for composition over time.
- **Stream graph:** Centered stacked area. Best for editorial data viz, narrative.
- **Sparkline:** Tiny line in a table cell or inline. Best for at-a-glance trends in tables.

### Comparison
- **Vertical bar chart:** Categorical comparison. Best for 5-15 categories.
- **Horizontal bar chart:** Categorical with long labels or many items. Best for ranking.
- **Grouped bar chart:** Multiple series across categories. Best for comparing 2-4 dimensions.
- **Stacked bar chart:** Composition within categories. Best for breakdown by category + dimension.
- **Bullet chart:** Single value vs target with ranges. Best for KPI dashboards.

### Proportion
- **Pie chart:** Whole-to-part. Best for <=5 categories.
- **Donut chart:** Same as pie with center label. Best for <=5 categories + summary metric.
- **Treemap:** Hierarchical proportion. Best for budgets, portfolios, disk usage.
- **Sunburst:** Multi-level hierarchical proportion. Best for nested categorical data.

### Distribution
- **Histogram:** Frequency distribution. Best for understanding spread.
- **Box plot:** Quartiles, outliers, median. Best for statistical summaries.
- **Violin plot:** Density + distribution. Best for scientific data viz.

### Correlation / Relationship
- **Scatter plot:** Two-variable relationship. Best for correlation studies.
- **Bubble chart:** Three-variable relationship (x, y, size). Best for risk/return analysis.
- **Heatmap:** Two-axis intensity. Best for correlation matrices, time-of-day patterns.

### Flow / Process
- **Funnel chart:** Drop-off through stages. Best for conversion analysis.
- **Sankey diagram:** Flow between nodes. Best for energy flow, conversion paths.
- **Waterfall chart:** Sequential additions/subtractions to a total. Best for financial bridge analysis.

### Geographic
- **Choropleth map:** Regional shading by value. Best for geographic statistics.
- **Pin/marker map:** Discrete location points. Best for store finders, travel routes.

### Network
- **Force-directed graph:** Connected nodes. Best for relationships, org charts, network analysis.
- **Chord diagram:** Cross-category relationships. Best for trade flows, migration data.

### Time Specific
- **Gantt chart:** Tasks across time. Best for project planning.
- **Calendar heatmap:** Daily intensity over a year. Best for activity patterns, contribution graphs.
- **Radar chart:** Multi-variable comparison. Best for product feature comparison, athlete profiles.

### Library Recommendations
- **Chart.js:** Standard library for web. Good defaults, light footprint, accessible.
- **Recharts:** React-native chart library. Composable, declarative.
- **D3.js:** Full custom control. Steep curve, best for unique visualizations.
- **Apache ECharts:** Powerful Chinese-origin library, dense feature set, performant for large datasets.
- **Visx:** D3 primitives wrapped for React. Best for custom React charts.
- **Plotly:** Scientific charts, 3D, interactive. Best for data analysis tools.
- **Victory:** React-native and web. Cross-platform charts.

### Accessible Color Palettes
- **Diverging:** Blue -> Gray -> Red (for negative-positive scales). Avoid red-green.
- **Sequential:** Single-hue gradient (light to dark). Best for ordered data.
- **Qualitative:** Distinct hues for categories. Maximum 7-8 categories before recall fails.
- **Colorblind-safe palettes:** Viridis, Cividis, Magma — perceptually uniform and colorblind-friendly.

### Chart Anti-Patterns
- Pie charts with >5 categories.
- Red and green as the only signals.
- 3D charts that distort perception.
- Tooltips that only work on hover.
- Charts without empty/loading/error states.
- Y-axis that doesn't start at zero on bar charts (misleading).

---

## Common Rules for Professional UI

The details that separate "looks fine" from "looks shipped."

### Icons & Visual Elements

| Rule | Standard | Avoid | Why |
|------|----------|--------|-----|
| **No emoji as structural icons** | Use vector icon sets (Lucide, Heroicons, Phosphor, react-native-vector-icons). | Using emojis (palette, rocket, gear) for navigation, settings, or system controls. | Emojis are font-dependent, inconsistent across platforms, cannot be themed. |
| **Vector-only assets** | Use SVG or platform vector icons that scale cleanly and theme. | Raster PNG icons that blur or pixelate. | Crisp at any size; light/dark adaptable. |
| **Stable interaction states** | Use color, opacity, or elevation for press states. | Layout-shifting transforms that move surrounding content. | Prevents jitter and preserves smoothness. |
| **Correct brand logos** | Use official brand assets; follow usage guidelines (spacing, color, clear space). | Guessing logo paths, recoloring unofficially, modifying proportions. | Prevents brand misuse and legal exposure. |
| **Consistent icon sizing** | Define icon sizes as design tokens — `icon-sm` (16), `icon-md` (24), `icon-lg` (32). | Mixing arbitrary values like 20 / 24 / 28 randomly. | Maintains rhythm and hierarchy. |
| **Stroke consistency** | Same stroke width within a visual layer (1.5px or 2px). | Mixing thick and thin strokes arbitrarily. | Inconsistent strokes reduce polish. |
| **Filled vs outline discipline** | One icon style per hierarchy level. | Mixing filled and outline at the same level. | Maintains semantic clarity. |
| **Touch target minimum** | 44x44pt interactive area. Use `hitSlop` for smaller icons. | Small icons without expanded hit area. | Accessibility and platform usability standards. |
| **Icon alignment** | Align icons to text baseline. Consistent padding around. | Misaligned icons or inconsistent spacing. | Subtle imbalance reduces perceived quality. |
| **Icon contrast** | WCAG: 4.5:1 for small elements, 3:1 minimum for larger glyphs. | Low-contrast icons blending into background. | Accessibility in both light and dark modes. |

### Interaction

| Rule | Do | Don't |
|------|-----|--------|
| **Tap feedback** | Provide pressed feedback (ripple/opacity/elevation) within 80-150ms. | No visual response on tap. |
| **Animation timing** | Micro-interactions 150-300ms with platform-native easing. | Instant transitions or >500ms animations. |
| **Accessibility focus** | Screen reader focus order matches visual order; labels descriptive. | Unlabeled controls or confused focus traversal. |
| **Disabled state clarity** | Disabled semantics, reduced emphasis, no tap action. | Controls that look tappable but do nothing. |
| **Touch target minimum** | >=44x44pt (iOS) or >=48x48dp (Android). Expand hit area when icon smaller. | Tiny tap targets with no padding. |
| **Gesture conflict prevention** | One primary gesture per region. | Overlapping gestures causing accidental actions. |
| **Semantic native controls** | Use `Button`, `Pressable`, native equivalents with proper roles. | Generic containers used as primary controls without semantics. |

### Light/Dark Mode Contrast

| Rule | Do | Don't |
|------|-----|--------|
| **Surface readability (light)** | Clear separation of cards/surfaces from background via opacity/elevation. | Overly transparent surfaces that blur hierarchy. |
| **Text contrast (light)** | Body text >=4.5:1 against light surfaces. | Low-contrast gray body text. |
| **Text contrast (dark)** | Primary text >=4.5:1; secondary >=3:1 on dark surfaces. | Dark mode text that blends into background. |
| **Border and divider visibility** | Separators visible in both themes. | Theme-specific borders disappearing in one mode. |
| **State contrast parity** | Pressed/focused/disabled states distinguishable in both modes. | Defining interaction states for one theme only. |
| **Token-driven theming** | Semantic color tokens mapped per theme. | Hardcoded per-screen hex values. |
| **Scrim and modal legibility** | Modal scrim 40-60% black to isolate foreground. | Weak scrim that leaves background competing. |

### Layout & Spacing

| Rule | Do | Don't |
|------|-----|--------|
| **Safe-area compliance** | Respect top/bottom safe areas for headers, tab bars, CTA bars. | Placing fixed UI under notch or gesture area. |
| **System bar clearance** | Spacing for status, nav bar, gesture home indicator. | Tappable content colliding with OS chrome. |
| **Consistent content width** | Predictable content width per device class. | Mixing arbitrary widths between screens. |
| **8dp spacing rhythm** | Consistent 4/8dp system for padding, gaps, section spacing. | Random spacing increments with no rhythm. |
| **Readable text measure** | Limit long-form text on tablets. | Full-width long paragraphs that hurt readability. |
| **Section spacing hierarchy** | Vertical rhythm tiers — 16/24/32/48 — by hierarchy level. | Similar UI levels with inconsistent spacing. |
| **Adaptive gutters by breakpoint** | Increase horizontal insets on larger widths and landscape. | Same narrow gutter on all device sizes. |
| **Scroll and fixed element coexistence** | Bottom/top content insets so lists aren't hidden behind fixed bars. | Scroll content obscured by sticky headers/footers. |

### Token Architecture (Design System Layer)

Build tokens in three layers:

```
Primitive (raw values: --color-blue-600: #2563EB)
    -> Semantic (purpose aliases: --color-primary: var(--color-blue-600))
        -> Component (component-specific: --button-bg: var(--color-primary))
```

- **Never use raw hex in components.** Always reference semantic tokens.
- **Semantic layer enables theme switching** (light/dark).
- **Component tokens enable per-component customization** without touching globals.
- **Use HSL format** for opacity control: `hsl(var(--color-primary) / 0.5)`.
- **Document every token's purpose.** Token files are public API.

### Component Spec Pattern

For each component, define states explicitly:

| Property | Default | Hover | Active | Focus | Disabled |
|----------|---------|-------|--------|-------|----------|
| Background | primary | primary-dark | primary-darker | primary | muted |
| Text | white | white | white | white | muted-fg |
| Border | none | none | none | focus-ring | muted-border |
| Shadow | sm | md | none | focus-shadow | none |

### Banner / Hero Design Rules

- **Safe zones:** Critical content in central 70-80% of canvas.
- **One CTA per banner:** Bottom-right, minimum 44px height, action verb.
- **Typography:** Maximum 2 fonts, minimum 16px body, >=32px headline.
- **Text ratio:** Under 20% of canvas for ads (Meta penalizes heavy text).
- **Print specs:** 300 DPI, CMYK, 3-5mm bleed.

### Standard Banner Sizes

| Platform | Type | Size (px) | Aspect |
|----------|------|-----------|--------|
| Facebook | Cover | 820 x 312 | ~2.6:1 |
| Twitter/X | Header | 1500 x 500 | 3:1 |
| LinkedIn | Personal | 1584 x 396 | 4:1 |
| LinkedIn | Company | 1192 x 220 | ~5.4:1 |
| YouTube | Channel art | 2560 x 1440 | 16:9 |
| Instagram | Story | 1080 x 1920 | 9:16 |
| Instagram | Post | 1080 x 1080 | 1:1 |
| Instagram | Carousel | 1080 x 1350 | 4:5 |
| Google Ads | Med Rectangle | 300 x 250 | 6:5 |
| Google Ads | Leaderboard | 728 x 90 | 8:1 |
| Pinterest | Pin | 1000 x 1500 | 2:3 |
| TikTok | Video | 1080 x 1920 | 9:16 |
| Website | Hero | 1920 x 600-1080 | ~3:1 to 16:9 |

### Social Photo Sizes

| Platform | Asset | Size (px) |
|----------|-------|-----------|
| Instagram | Post | 1080 x 1080 |
| Instagram | Story | 1080 x 1920 |
| Instagram | Carousel | 1080 x 1350 |
| Facebook | Post | 1200 x 630 |
| Twitter/X | Post | 1200 x 675 |
| LinkedIn | Post | 1200 x 627 |
| YouTube | Thumbnail | 1280 x 720 |
| Pinterest | Pin | 1000 x 1500 |

### Slide / Presentation Rules

- Use CSS variables for colors, never hardcoded hex.
- Use Chart.js for charts, not CSS-only bar graphs.
- Include navigation: keyboard arrows, click, progress bar.
- Center-align content for focus.
- Optimize for persuasion and conversion, not information dump.
- One key message per slide.
- Pattern-break between slides — alternate "What Is" (frustration) with "What Could Be" (hope) at 1/3 and 2/3 of deck.

### Standard Copywriting Formulas
- **PAS:** Problem -> Agitation -> Solution.
- **AIDA:** Attention -> Interest -> Desire -> Action.
- **FAB:** Features -> Advantages -> Benefits.
- **BAB:** Before -> After -> Bridge.
- **4Ps:** Promise -> Picture -> Proof -> Push.

---

## Pre-Delivery Checklist

Verify before shipping. Every item is a release-blocker if it fails.

### Visual Quality
- [ ] No emojis used as icons (use SVG instead).
- [ ] All icons from a consistent icon family — same stroke width, same corner radius.
- [ ] Official brand assets used with correct proportions and clear space.
- [ ] Pressed-state visuals do not shift layout bounds or cause jitter.
- [ ] Semantic theme tokens used consistently — no ad-hoc per-screen hardcoded colors.
- [ ] Icon contrast meets WCAG 4.5:1 (small) / 3:1 (larger glyphs).

### Interaction
- [ ] All tappable elements provide clear pressed feedback (ripple/opacity/elevation) within 100ms.
- [ ] Touch targets meet minimum size — >=44x44pt iOS, >=48x48dp Android, >=44x44px web.
- [ ] Micro-interaction timing in 150-300ms range with native-feeling easing.
- [ ] Disabled states visually clear and non-interactive.
- [ ] Screen reader focus order matches visual order; labels descriptive.
- [ ] Gesture regions avoid nested/conflicting interactions (tap/drag/back-swipe conflicts).
- [ ] Each screen has one primary CTA.

### Light/Dark Mode
- [ ] Primary text contrast >=4.5:1 in both light and dark mode.
- [ ] Secondary text contrast >=3:1 in both light and dark mode.
- [ ] Dividers, borders, interaction states distinguishable in both modes.
- [ ] Modal/drawer scrim opacity strong enough to preserve foreground legibility (40-60% black).
- [ ] Both themes tested before delivery — not inferred from one theme.
- [ ] Dark mode uses desaturated tonal variants, not pure inversion.

### Layout
- [ ] Safe areas respected for headers, tab bars, bottom CTA bars.
- [ ] Scroll content not hidden behind fixed/sticky bars.
- [ ] Verified on small phone (375px), large phone (414px), tablet (768px), portrait + landscape.
- [ ] Horizontal insets/gutters adapt by device size and orientation.
- [ ] 4/8dp spacing rhythm maintained across component, section, and page levels.
- [ ] Long-form text measure remains readable on larger devices — no edge-to-edge paragraphs.
- [ ] No horizontal scroll on mobile body content.
- [ ] Viewport meta tag set correctly. Zoom not disabled.

### Accessibility
- [ ] All meaningful images and icons have accessibility labels.
- [ ] Form fields have labels, hints, and clear error messages stating cause + fix.
- [ ] Color is not the only indicator (icon or text accompanies every color signal).
- [ ] Reduced motion supported — animations reduce or stop on user preference.
- [ ] Dynamic text size supported without layout breakage at largest setting.
- [ ] Accessibility traits/roles/states (selected, disabled, expanded) announced correctly.
- [ ] Skip links present for keyboard users on web.
- [ ] Sequential heading hierarchy (h1 -> h2 -> h3, no skipping).
- [ ] Focus rings visible on all interactive elements.

### Performance
- [ ] Images use WebP or AVIF.
- [ ] Image dimensions or `aspect-ratio` declared to prevent layout shift.
- [ ] CLS < 0.1.
- [ ] Below-fold images use `loading="lazy"`.
- [ ] Critical CSS inlined or loaded early.
- [ ] Third-party scripts async or deferred.
- [ ] Lists with 50+ items are virtualized.
- [ ] Skeleton screens for operations >300ms.
- [ ] No animations on `width`, `height`, `top`, `left` — only `transform` and `opacity`.

### Navigation
- [ ] Back button preserves scroll position and state.
- [ ] All key screens reachable via deep link.
- [ ] Bottom nav <=5 items with icon + label.
- [ ] Current location visually highlighted in nav.
- [ ] Persistent core nav reachable from deep pages.
- [ ] Destructive actions visually separated from normal nav items.

### Forms
- [ ] Visible label per input (not placeholder-only).
- [ ] Errors below related field with cause + fix.
- [ ] First invalid field auto-focused on submit failure.
- [ ] Multi-error summary at top with anchor links to fields.
- [ ] Aria-live region for screen reader error announcement.
- [ ] Submit shows loading -> success/error.
- [ ] Confirmation dialog before destructive actions.
- [ ] Undo available for destructive or bulk operations.

### Charts
- [ ] Color not the only signal — icons/patterns/text supplement.
- [ ] Legends visible and near the chart.
- [ ] Tooltips work on hover, tap, and keyboard focus.
- [ ] Empty, loading, and error states designed.
- [ ] Chart reflows or simplifies on mobile.
- [ ] Screen reader summary describes key insight.
- [ ] Data table alternative for accessibility.

### Final Pass
- [ ] Test on 375px and landscape orientation.
- [ ] Verify with `prefers-reduced-motion` enabled.
- [ ] Test with Dynamic Type at largest size.
- [ ] Dark mode contrast checked independently from light.
- [ ] All touch targets >=44pt; no content behind safe areas.
- [ ] No emojis anywhere in production UI.
