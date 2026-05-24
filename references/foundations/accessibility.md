# Accessibility

> Accessibility is a baseline, not a feature. These rules block release. Build it in from the start; do not bolt it on at the end.

## Principles

1. **Accessibility is non-negotiable, not a feature** — Every rule in this foundation is a release blocker. Color contrast, focus visibility, keyboard navigation, semantic markup, alt text, and reduced-motion support are preconditions for shipping, not nice-to-haves.

2. **Color is never the only signal** — Every color signal pairs with an icon, text, or pattern. Error states need red color AND an icon AND a text message. Color-blind users and screen reader users must get the same information.

3. **Keyboard must reach everything** — Every interactive control reachable and operable by keyboard alone. Tab order matches visual order. If you offer drag-and-drop, also offer a keyboard alternative.

4. **Focus must be visible** — 2 to 4px visible focus ring on every interactive element, high-contrast against background. Never `outline: none` without a replacement. After page transition, move focus to main content. After submit fails, auto-focus the first invalid field.

5. **Semantic HTML carries half the load** — Use `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`, `<button>`, `<label>`, `<table>`, headings in sequence. Generic `<div>` and `<span>` used as buttons break screen readers and keyboard nav.

6. **Sequential heading hierarchy** — `h1` → `h2` → `h3` → `h4` → `h5` → `h6`. Never skip levels. Each page has exactly one `h1`.

7. **Labels are explicit, never inferred** — Every input gets a visible `<label for="...">`. Placeholder text is not a label. Icon-only buttons get `aria-label`. Native apps use `accessibilityLabel`.

8. **Dynamic Type without breaking** — Support system text scaling. Layouts must not truncate or break as text grows. Test at the largest accessibility text size.

9. **Reduced motion is a contract** — Honor `prefers-reduced-motion: reduce`. Replace `translateY` reveals with opacity-only fades. Pause ambient motion. Drop blur from scroll entries. Never opt the user back in by default.

10. **Errors name the cause AND the fix** — Never "form contains errors" or "invalid input." Always specific: name the field, name the problem, name the fix. "Email needs an @ sign" not "Invalid email."

11. **Common courtesy in design** — Don't make users think. Make obvious things obvious. Don't ask for unnecessary effort. Provide visible affordances. Apologize for failures and explain the recovery path.

## Do / Don't

| Do | Don't |
|---|---|
| Verify foreground/background pairs at 4.5:1 minimum | Ship gray-on-gray text or `slate-500` on white body copy |
| Provide visible focus rings on every interactive element | Use `outline: none` without a replacement |
| Pair every color signal with an icon AND text | Convey state through color alone |
| Use semantic HTML (`<nav>`, `<main>`, `<button>`, `<label>`) | Use generic `<div>` as buttons |
| Provide sequential heading hierarchy (h1, h2, h3) | Skip from h1 directly to h4 |
| Provide visible `<label for>` on every input | Use placeholder text as the label |
| Add `aria-label` to icon-only buttons | Ship icon buttons with no accessible name |
| Provide skip-to-main-content link on every web page with significant chrome | Force keyboard users to tab through 20+ nav items |
| Test at largest Dynamic Type setting | Test only at default text size |
| Honor `prefers-reduced-motion: reduce` | Force motion on users who opted out |
| Provide alt text for every meaningful image | Leave alt text blank on content-bearing images |
| Mark decorative images with `alt=""` | Mark decorative images with `alt="image"` |
| Auto-focus first invalid field on submit failure | Drop user at top of form with no indication of what failed |
| Provide error summary at top with anchor links | List errors silently at the bottom |
| Use `aria-live` region for dynamic error announcements | Add errors silently to the DOM with no screen reader announcement |
| Use `role="alert"` for critical state announcements | Rely on visual color change alone for screen reader users |
| Reserve high contrast (7:1 AAA) for primary copy | Drift to 3:1 "stylish but unreadable" body text |
| Preserve pinch-zoom in viewport meta | Disable zoom via `user-scalable=no` |
| Use `touch-action: manipulation` to remove 300ms tap delay | Ignore tap delay on web |
| Provide keyboard shortcuts for power users (with documentation) | Override system shortcuts |

## Examples

### Pattern: Visible focus ring
**Use when**: Every interactive element — button, link, input, card, tab.
**Anti-pattern**: `outline: none` with no replacement, or 1px gray ring invisible on the surface.
**How**: 2 to 4px solid outline in the brand accent color, offset 2 to 4px. Style varies by aesthetic:
- Brutalist: hard 2px solid accent outline with zero offset
- Minimalist: 2px solid focus ring in paired accent pastel, 2px offset
- High-end: combined ring and soft outer glow keyed to active vibe accent

The focus state is not just `:focus-visible` — actually visible. `:focus-visible` should style the focus, but never rely on it without ensuring the style is genuinely perceivable.

### Pattern: Error summary with anchor links
**Use when**: Forms with multiple potential errors.
**Anti-pattern**: Errors scattered inline only, with no aggregated summary at the top.
**How**: After submit failure:
1. Auto-focus the first invalid field
2. Render an error summary at the top of the form with anchor links to each invalid field
3. Each field shows its own inline error below the input
4. Wrap the summary in `<div role="alert" aria-live="polite">` so screen readers announce
5. Error messages name the cause AND the fix: "Phone number needs a country code" not "Invalid input"

### Pattern: Inline error with cause + fix
**Use when**: Field validation on a form.
**Anti-pattern**: "Invalid email," "Please check your input," "Form contains errors."
**How**: State the cause AND the fix in one sentence. Examples:
- "Email needs an @ sign. Try again."
- "Phone number must include the country code. Add +1 or your country prefix."
- "Password needs at least 8 characters and one number."
- "Date can't be in the past. Pick today or later."

Validation on `blur`, not on every keystroke. The user finishes typing, then sees the error. Never "must be valid email" after the first letter.

### Pattern: Skip link
**Use when**: Every web page with significant chrome (nav, sidebar, mega-menu).
**Anti-pattern**: Forcing keyboard users to tab through 20+ nav items to reach content.
**How**: First focusable element on the page is a "Skip to main content" link. Hidden visually until focused; on focus, jumps to visible. Pressing Enter moves focus to `<main>` or the page's content region. Implementation:

```html
<a href="#main" class="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4">Skip to main content</a>
<main id="main" tabindex="-1">...</main>
```

### Pattern: Sequential heading hierarchy
**Use when**: Every page.
**Anti-pattern**: Skipping from `h1` directly to `h3` because the design wanted smaller text, or using `h2` for "Header" and `h2` again for "Footer" (only one h1 per page; never two).
**How**: Each page has exactly one `<h1>` carrying the page's primary topic. `<h2>` for major sections. `<h3>` for subsections. Never skip a level for visual reasons — use CSS to style. Screen reader users navigate by heading; broken hierarchy reads as chaos.

### Pattern: Touch target with hitSlop
**Use when**: Small icons or thin edges that need to be tappable.
**Anti-pattern**: 16px icon with no padding — impossible to tap accurately.
**How**: Minimum 44x44pt (iOS), 48x48dp (Android), 44x44px (web). For small visual elements, extend the hit area beyond visual bounds via `hitSlop` (React Native) or padding (web). 8px minimum gap between adjacent touch targets.

### Pattern: Aria-label on icon-only buttons
**Use when**: Icon buttons with no visible text label.
**Anti-pattern**: `<button><Icon /></button>` with no accessible name.
**How**: Add `aria-label="Close dialog"` (or whatever the action is). Native equivalents: `accessibilityLabel` and `accessibilityHint` in React Native, `contentDescription` in Android. Screen reader users hear the label; sighted users see the icon.

### Pattern: Form labels
**Use when**: Every input field.
**Anti-pattern**: Placeholder-only labels that disappear when the user starts typing.
**How**: Every input has a visible `<label for="email">Email</label>` linked by `for` and `id`. Required fields marked with an asterisk or "(required)" inline. Helper text below the input via `aria-describedby`. Error text below the field, also referenced via `aria-describedby`. Floating labels are tolerated but the label must remain visible after the user types.

### Pattern: Alt text discipline
**Use when**: Every `<img>` or meaningful visual.
**Anti-pattern**: `alt="image"`, `alt="photo.jpg"`, blank `alt` on a content image.
**How**:
- Meaningful image: `alt="A team reviewing a wireframe on a wall"` (describes the image's content and intent)
- Decorative image: `alt=""` (empty, signals to screen readers to skip)
- Icon paired with visible text label: `alt=""` (label carries the meaning)
- Icon-only: use `aria-label` on the parent button, or `<img alt="Close dialog">`

### Pattern: Dynamic Type support
**Use when**: Any text-containing layout, especially mobile.
**Anti-pattern**: Fixed pixel sizes that truncate or overflow at largest accessibility text size.
**How**:
- Mobile body: 16px minimum (also prevents iOS auto-zoom on input focus)
- Use relative units (`rem`, `em`) for type scale
- Test at iOS Dynamic Type at largest accessibility setting
- Layouts must reflow, not truncate, as text grows
- Touch targets remain 44pt+ at largest text size

### Pattern: Reduced-motion fallback
**Use when**: Building any animation system.
**Anti-pattern**: Single switch that disables all motion, leaving the page feeling broken with sudden snaps.
**How**: Define a reduced variant of each animation:
- Scroll fade-up with `translateY(24px)` → opacity-only fade
- Modal scale + fade → quick opacity fade (200ms)
- Background mesh drift → static
- Logo marquee → static row
- Cinematic blur + translate entry → simple opacity fade
- Brutalist scanline drift, glitch effects, slot-machine counters → static; keep instant state changes
- Magnetic button physics → static hover state

Honor at every level. Never assume the user "will be fine."

### Pattern: Color-blind safe palette
**Use when**: Charts, data viz, status indicators.
**Anti-pattern**: Red and green as the only signals (red = bad, green = good) — fails ~8% of male users.
**How**:
- Diverging scales: blue → gray → red (not red → green)
- Sequential: single-hue gradient (light to dark)
- Qualitative: max 7 to 8 distinct hues; use perceptually uniform palettes
- Always supplement with patterns, textures, shapes, or icons
- Always supplement with text labels
- Validate using a color-blindness simulator (deuteranopia, protanopia, tritanopia)

### Pattern: Focus management on route change
**Use when**: SPA route transitions or modal open.
**Anti-pattern**: Focus stays at the previous page's position; screen reader user has no idea where they are.
**How**: After page transition, programmatically move focus to the main content region. Use `tabIndex={-1}` on `<main>` and `.focus()` after route mount. After modal open, focus the modal heading or first interactive element. After modal close, return focus to the trigger.

### Pattern: Aria-live for dynamic updates
**Use when**: Toast notifications, async error messages, status updates.
**Anti-pattern**: Toast appears visually but is silent to screen readers.
**How**:
- `aria-live="polite"` for non-urgent updates (toasts, status changes)
- `aria-live="assertive"` for urgent errors only
- `role="alert"` for critical state announcements (form submission failures)
- Auto-dismiss toasts in 3 to 5 seconds; never steal focus
- Provide a manual dismiss control for screen reader users who need more time

### Pattern: Keyboard shortcut documentation
**Use when**: Power-user products with custom shortcuts.
**Anti-pattern**: Hidden shortcuts that override system shortcuts (Ctrl+S blocked, browser back broken).
**How**: Document all shortcuts in an accessible help dialog (often Cmd+/ or "?"). Preserve system and assistive-technology shortcuts. Custom shortcuts use `Alt+Letter` or `Cmd+Shift+Letter` to avoid collisions with browser/OS. Provide a visible UI control for every shortcut so non-keyboard users have the same affordance.

### Pattern: Escape route on modal
**Use when**: Every modal, sheet, drawer.
**Anti-pattern**: Modal with no close button, no Escape key handler, no clickable scrim.
**How**:
- Visible close button (44px+ touch target) clearly labeled
- Escape key dismisses (always)
- Click on scrim dismisses (unless work is in progress)
- Swipe-down dismisses on mobile sheets
- If unsaved changes exist, confirm before dismissing
- Focus returns to the trigger element after close

### Pattern: Common courtesy in design
**Use when**: Designing any user-facing surface.
**Anti-pattern**: Asking the user to do unnecessary work — re-entering their phone number, re-finding their place after a route change, parsing a vague error message.
**How**: Apply these principles:
- Don't make me think — make obvious things obvious
- Don't ask for unnecessary effort — autofill, pre-fill, save drafts
- Provide visible affordances — clickable things must look clickable
- Apologize for failures and explain the recovery path
- Honor convention — search is a magnifying glass, logo is top-left, primary CTA is filled
- Provide error tolerance — undo for destructive actions, confirmation for irreversible ones

### Pattern: Aria-busy during loading
**Use when**: A component or section loads dynamically.
**Anti-pattern**: Component changes visually without screen reader awareness.
**How**: Set `aria-busy="true"` on the loading region. Screen readers announce the loading state. Set `aria-busy="false"` on completion; consider pairing with `aria-live="polite"` to announce completion.

### Pattern: Live regions for transient content
**Use when**: Toast notifications, status updates, validation errors after user action.
**Anti-pattern**: Toast appears visually only; screen reader user misses critical state.
**How**:
- `aria-live="polite"` for non-urgent updates (most cases) — screen reader waits until current speech finishes
- `aria-live="assertive"` for urgent errors only — interrupts current speech (use sparingly)
- `role="alert"` is equivalent to `aria-live="assertive"`
- `role="status"` is equivalent to `aria-live="polite"`
- Wrap toasts and dynamic messages in a persistent live region — adding/removing the region itself does not trigger announcement

### Pattern: Drag-and-drop alternative
**Use when**: Sortable lists, kanban boards, reorderable items.
**Anti-pattern**: Drag is the only path to reorder; keyboard users cannot use the feature.
**How**: Provide keyboard alternatives:
- "Move up" / "Move down" buttons on each item
- Up/Down arrow keys when item is focused
- Cut/paste via Ctrl+X / Ctrl+V on items
- A reorder dialog with explicit numeric position input
- `aria-grabbed` and `aria-dropeffect` for screen readers during drag

### Pattern: Multi-language and RTL support
**Use when**: Building for international audiences.
**Anti-pattern**: Hardcoded LTR layouts that break under Arabic, Hebrew, Persian.
**How**:
- Use `dir="rtl"` and ensure every layout works mirrored
- Use logical properties (`margin-inline-start`, `padding-inline-end`) rather than `margin-left` / `padding-right`
- Stagger animations are direction-aware — mirror on RTL
- Number formatting locale-aware
- Date formatting locale-aware
- Text expansion: translations may be 30 to 50% longer; layouts must flex
- Test in RTL languages and large-text mode in the same pass

### Pattern: Focus outline with high contrast
**Use when**: Every interactive element.
**Anti-pattern**: 1px gray focus ring on a gray background — technically present, practically invisible.
**How**: Focus outline must clear 3:1 contrast against ALL adjacent colors. On gradients or photo backgrounds, use double-layer outlines (white + accent, or accent + black) to ensure visibility everywhere. 2 to 4px width. Offset 0 to 4px from element edge.

## Tokens / values

### Contrast minimums
- Normal text (body): 4.5:1 (AA)
- Large text (18pt+ regular, 14pt+ bold): 3:1 (AA)
- AAA target: 7:1 for body
- UI components and graphic objects: 3:1 minimum
- Disabled states: contrast not required, but visibly muted (0.38 to 0.5 opacity)
- Data lines, bars vs background: 3:1; text labels 4.5:1
- Focus ring: 3:1 against adjacent colors

### Touch target sizes
- iOS minimum: 44x44pt
- Android minimum: 48x48dp
- Web minimum: 44x44px
- Mobile input field height: ≥44px
- Touch spacing: ≥8px gap between adjacent targets
- Extend hit area beyond visual bounds via `hitSlop` or padding for smaller icons

### Focus indicators
- Width: 2 to 4px
- Style: solid (brutalist), or paired focus ring with offset (minimalist), or ring + soft glow (premium)
- Offset: 0 to 4px from element edge
- Color: brand accent, high-contrast against background
- Must clear 3:1 contrast against adjacent colors

### Heading hierarchy rules
- One `<h1>` per page
- Sequential: h1 → h2 → h3 → h4 → h5 → h6
- Never skip levels for visual reasons
- Use CSS to style if visual size differs from hierarchical level
- Section headings inside `<section>` start at `<h2>`

### ARIA usage
- Roles: `role="alert"`, `role="status"`, `role="dialog"`, `role="navigation"` only when semantic HTML cannot express it
- `aria-label` for icon-only buttons and unlabeled controls
- `aria-labelledby` to associate a visible label with a control
- `aria-describedby` for helper text and error messages
- `aria-live="polite"` for non-urgent dynamic updates
- `aria-live="assertive"` for urgent errors only (use sparingly)
- `aria-expanded` for accordions, dropdowns, expandable sections
- `aria-selected` for tabs, lists with selection
- `aria-current="page"` on active nav item
- `aria-hidden="true"` on decorative elements
- `aria-busy="true"` during loading states

### Form patterns
- Visible `<label for>` on every input — never placeholder-only
- Required indicators inline (`*` or "(required)")
- Helper text via `aria-describedby`
- Error text below field via `aria-describedby`
- Validation on `blur`, not on every keystroke
- Auto-focus first invalid field on submit failure
- Multi-error summary at top with anchor links
- `role="alert"` or `aria-live="polite"` on the error region
- `autocomplete` attribute on form inputs for system autofill
- Semantic input types (`email`, `tel`, `number`, `url`, `date`) so mobile keyboards adapt

### Reduced-motion fallbacks
- `prefers-reduced-motion: reduce` honored at every level
- Replace `translateY` reveals with opacity-only fades
- Pause background ambient motion
- Drop blur from scroll entries
- Skip scanline drift, glitch effects, slot-machine counters
- Skip magnetic button physics; keep instant hover state
- Shorten durations by 30 to 50% where motion remains

### Dynamic Type
- Mobile body: 16px minimum
- Use relative units (`rem`, `em`)
- Test at largest accessibility setting
- Layouts must reflow, not truncate

### Keyboard navigation
- Tab order matches visual order
- Every interactive control reachable by keyboard alone
- Drag-and-drop has keyboard alternative
- System and assistive-technology shortcuts preserved
- Skip-to-main-content link as first focusable element
- Focus management on route change (move focus to main)

### Banned accessibility anti-patterns
- `outline: none` without replacement
- Icon-only buttons with no `aria-label`
- Placeholder-only labels
- Text below 12px in body content
- Gray-on-gray, low-contrast text
- Color-only state signals (no icon, no text)
- `user-scalable=no` in viewport meta (disabled pinch-zoom)
- "Form contains errors" or "Invalid input" with no specifics
- Toast steals focus from current control
- Validation on every keystroke (user typing "j" sees "must be valid email")
- Skipping heading levels for visual reasons (h1 → h4)
- Errors only at top of form with no inline indication
- Errors only inline with no aggregated summary
- Modal with no Escape key handler
- Modal blocks primary flow with no escape
- Auto-play audio without consent
- Flashing or rapidly-strobing effects above 3 flashes per second
- DeviceOrientation / DeviceMotion APIs for visual effects (requires sensor permissions, erodes trust)
- Custom mouse cursors (accessibility hostile)
- 300ms double-tap-zoom delay on web (use `touch-action: manipulation`)
- Mystery-meat icon-only navigation
- Long-pressed or right-click as the only path to an action

### Common courtesy principles
- Don't make the user think — make obvious things obvious
- Don't ask for unnecessary effort (autofill, pre-fill, save drafts)
- Make clickable things obviously clickable
- Apologize for failures and explain the recovery path
- Honor convention (logo top-left, nav top, search = magnifying glass)
- Provide error tolerance (undo for destructive, confirm for irreversible)
- Three sources of noise to eliminate: shouting, disorganization, clutter — fix by removal, not addition
- Clarity over consistency — when making something significantly clearer requires slight inconsistency, choose clarity every time

### Web Content Accessibility Guidelines (WCAG) baseline
- 2.1 AA at minimum across all surfaces
- AAA targeted where feasible for body copy and primary controls
- Verify with automated tooling (axe, Lighthouse) and manual screen reader testing
- Test with VoiceOver (iOS), TalkBack (Android), NVDA or JAWS (Windows)

## Checklist (severity-tagged)

- [ ] All foreground/background pairs verified at 4.5:1 minimum (severity: Critical)
- [ ] Color is never the only signal — icon or text accompanies every color signal (severity: Critical)
- [ ] Visible focus ring on every interactive element, 2 to 4px high-contrast (severity: Critical)
- [ ] `outline: none` never used without a replacement (severity: Critical)
- [ ] Tab order matches visual order (severity: Critical)
- [ ] Every interactive control reachable by keyboard alone (severity: Critical)
- [ ] Skip-to-main-content link as first focusable element on web pages with significant chrome (severity: High)
- [ ] Sequential heading hierarchy (h1 → h2 → h3, no skipping) (severity: High)
- [ ] Exactly one `<h1>` per page (severity: High)
- [ ] Visible `<label for>` on every input (placeholder is not a label) (severity: Critical)
- [ ] Icon-only buttons have `aria-label` (severity: Critical)
- [ ] Every meaningful image has descriptive alt text (severity: Critical)
- [ ] Decorative images marked `alt=""` (severity: Medium)
- [ ] Touch targets ≥44x44pt iOS, ≥48x48dp Android, ≥44x44px web (severity: Critical)
- [ ] 8px minimum gap between adjacent touch targets (severity: Critical)
- [ ] Dynamic Type tested at largest accessibility setting (severity: High)
- [ ] Mobile body text ≥16px (severity: Critical)
- [ ] `prefers-reduced-motion: reduce` honored at every level (severity: Critical)
- [ ] Error messages state cause AND fix (severity: High)
- [ ] No "form contains errors" or "invalid input" copy (severity: High)
- [ ] Auto-focus first invalid field on submit failure (severity: High)
- [ ] Error summary at top of form with anchor links to each field (severity: Medium)
- [ ] `aria-live` region or `role="alert"` on form error region (severity: High)
- [ ] Validation runs on `blur`, not on every keystroke (severity: High)
- [ ] Modals offer Escape key dismissal, visible close button, scrim click (severity: Critical)
- [ ] Focus returns to trigger after modal close (severity: High)
- [ ] Focus moves to main content after route change (severity: High)
- [ ] Toasts use `aria-live="polite"`, do not steal focus (severity: High)
- [ ] Toasts auto-dismiss in 3 to 5 seconds (severity: Medium)
- [ ] Pinch-zoom preserved in viewport meta (severity: Critical)
- [ ] `touch-action: manipulation` removes 300ms tap delay on web (severity: Medium)
- [ ] Color-blind safe palettes in charts and status indicators (severity: Critical)
- [ ] Red-green as the only chart signals avoided (severity: Critical)
- [ ] Disabled states use reduced opacity + cursor change + semantic `disabled` attribute (severity: High)
- [ ] Drag-and-drop has keyboard alternative (severity: High)
- [ ] No DeviceOrientation / DeviceMotion APIs for visual effects (severity: Critical)
- [ ] No custom mouse cursors (severity: High)
- [ ] No auto-play audio without consent (severity: Critical)
- [ ] No flashing above 3 flashes per second (severity: Critical)
- [ ] Tested with screen reader (VoiceOver, TalkBack, NVDA) (severity: Critical)
- [ ] WCAG 2.1 AA cleared on automated tools (axe, Lighthouse) (severity: Critical)
- [ ] Persistent core nav reachable from deep pages (severity: Medium)
- [ ] System and assistive-technology shortcuts preserved (severity: High)

## Related

- See **color.md** for contrast pairs and color-not-only rules.
- See **motion.md** for `prefers-reduced-motion` accommodations.
- See **interaction.md** for touch target sizes and gesture alternatives.
- See **copy.md** for error message specificity (cause + fix).
- See **components.md** for form field, modal, and toast accessibility contracts.
- See **typography.md** for Dynamic Type support and sizing minimums.
- See **layout.md** for skip-link placement and heading hierarchy across page structure.
- See **dashboards.md** for chart accessibility (legends, tooltips, table alternatives).
