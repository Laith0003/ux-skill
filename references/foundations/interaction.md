# Interaction

> Tactile feedback within 100ms is what makes an interface feel alive. Every tap, hover, and gesture must respond visibly — or the user starts tapping twice.

## Principles

1. **Touch targets are 44pt iOS, 48dp Android, 44px web — minimum** — Extend hit areas beyond visual bounds via `hitSlop` or padding when icons are smaller. Never require pixel-perfect taps on small icons or thin edges.

2. **Tap feedback lands within 80 to 150ms** — Ripple, opacity change, elevation change, or color flash. Pick one and apply consistently. Material state layers are a solid baseline.

3. **Press states use tactile transforms** — `-translate-y-[1px]` or `scale-[0.98]` on `:active` to simulate a physical push. Duration 80 to 150ms. Restore on release.

4. **Hover never carries primary interaction** — Touch devices have no hover. Primary CTAs never live behind a hover state. Shape, location, and formatting must signal clickability before interaction.

5. **One primary gesture per region** — Avoid nested tap/drag conflicts. If a card supports both tap-to-open and swipe-to-delete, the swipe needs a visible affordance (chevron, label, onboarding hint).

6. **Platform-standard gestures are not redefined** — Swipe-back on iOS, pinch-zoom, predictive back on Android. Don't override them. Don't block system gestures (Control Center swipe, back swipe, edge gestures).

7. **Drag thresholds prevent accidents** — 8 to 12px movement threshold before drag starts. Below the threshold, the gesture is treated as a tap.

8. **Magnetic micro-physics use motion values, never state** — `useMotionValue` and `useTransform` for continuous hover and cursor-tracked motion. `useState` triggers re-renders that collapse performance on mobile.

9. **Tactile feedback is the difference between toy and tool** — Press states with translation, scale, or elevation shift. Hover states with shadow lift on cards. Color shift on links. The user feels the interface respond.

10. **System gestures are sacred** — Pinch-zoom is preserved (never `user-scalable=no`). Predictive back works. Tab Bar swipe doesn't block content scroll. Don't fight the OS.

11. **Visible affordances signal interactivity** — Buttons look like buttons. Links look like links. Don't rely on hover for discoverability. Mobile users see no hover; affordances must be visible at rest.

## Do / Don't

| Do | Don't |
|---|---|
| Use minimum 44x44pt touch targets (iOS) / 48x48dp (Android) / 44x44px (web) | Ship 16px tap targets without expanded hit area |
| Extend hit area beyond visual bounds via `hitSlop` or padding | Require pixel-perfect taps on small icons |
| Provide visible tap response within 80 to 150ms | Ship instant state changes with no animation |
| Use `-translate-y-[1px]` or `scale-[0.98]` on `:active` | Use dramatic transforms that shift surrounding layout |
| Provide both visible affordance AND aria-label on icon buttons | Rely on icon alone to signal interactivity |
| Use platform-standard gestures (swipe-back, pinch-zoom) | Redefine system gestures with custom behavior |
| Maintain 8 to 12px movement threshold before drag starts | Trigger drag immediately on touch (causes accidental drags) |
| Provide both gesture AND tappable control for critical actions | Make swipe the only path to a critical action |
| Use `useMotionValue` and `useTransform` for continuous animation | Use `useState` for continuous hover or magnetic effects |
| Provide hover lift on cards (200 to 300ms ease) | Apply scale animations to CTAs (looks toy-like) |
| Preserve pinch-zoom in viewport meta | Set `user-scalable=no` |
| Use `touch-action: manipulation` to remove 300ms tap delay | Ignore tap delay on web |
| Use haptic feedback on confirmations and important actions | Use haptic on every tap (exhausting) |
| Use cursor-driven parallax for visual effect | Use DeviceOrientation / DeviceMotion (requires sensor permissions) |
| Maintain `cursor: pointer` on every clickable element on web | Leave default cursor on interactive elements |
| Provide visible disabled state (0.38 to 0.5 opacity + cursor change + `disabled` attribute) | Style "disabled" buttons that still respond to clicks |
| Use semantic native controls (`<button>`, `<Pressable>`) | Use generic containers as buttons (breaks a11y) |

## Examples

### Pattern: Standard tap feedback
**Use when**: Every tappable element — button, card, link, list row.
**Anti-pattern**: No visual response on tap; user taps twice thinking it didn't register.
**How**: Visible response within 80 to 150ms. Pick one feedback type and apply consistently:
- Ripple (Material): expanding circle from tap point
- Opacity change: 0.7 to 1 fade
- Elevation change: shadow lift
- Color flash: brief background tint

### Pattern: Tactile press transform
**Use when**: Buttons, primary CTAs, cards.
**Anti-pattern**: Press states that scale dramatically (1.2x) and shift surrounding layout.
**How**: On `:active`, apply `-translate-y-[1px]` or `scale-[0.98]`. Duration 80 to 150ms. Restore on release. The user feels a physical push. The transform stays subtle enough that surrounding content doesn't shift.

### Pattern: Hover lift on interactive cards
**Use when**: Clickable cards, image tiles, feature blocks.
**Anti-pattern**: Cards that snap on hover, or that scale dramatically (1.2x) and shift surrounding layout.
**How**: `translateY(-2px)` to `translateY(-4px)` combined with shadow elevation shift. Duration 200 to 300ms with `cubic-bezier(0.16, 1, 0.3, 1)`. Reserved for clickable cards and primary CTAs; not every element.

### Pattern: Magnetic button (high-end)
**Use when**: Hero CTAs in premium marketing surfaces.
**Anti-pattern**: Button jumps wildly toward cursor or lags behind it.
**How**: Use `useMotionValue` and `useTransform` (never `useState`) to track cursor position. Button translates 4 to 8px maximum toward cursor. Spring physics damp the motion. On press, scale down to `0.98`. NEVER use React `useState` for magnetic hover — performance collapses on mobile.

### Pattern: Button-in-button (high-end)
**Use when**: CTA with a trailing icon (arrow, chevron) in premium aesthetic.
**Anti-pattern**: Arrow sitting naked next to text inside the button.
**How**: The arrow lives inside its own circular wrapper, flush with the main button's right inner padding. The wrapper has its own subtle background and ring. On hover, the wrapper translates diagonally (1px up and 1px right) and scales up slightly (`scale-105`), creating internal kinetic tension.

### Pattern: Gesture with visible affordance
**Use when**: Swipe-to-delete, swipe-to-archive, swipe-to-reply.
**Anti-pattern**: Hidden gesture with no visible hint, user has no idea it exists.
**How**: Visible affordance (chevron, partial reveal of the action button, label, or onboarding hint) signals the gesture. First-time user sees the action; repeat users develop muscle memory. Always provide a tappable alternative — never gesture-only for critical actions.

### Pattern: Drag threshold
**Use when**: Drag-and-drop interfaces, draggable list items.
**Anti-pattern**: Touch immediately starts drag, accidentally moving items when user meant to tap.
**How**: 8 to 12px movement threshold before drag starts. Below the threshold, the gesture is treated as a tap. Above the threshold, drag activates and the cursor or pointer changes to indicate drag mode.

### Pattern: Pinch-zoom preservation
**Use when**: Every web page.
**Anti-pattern**: `<meta name="viewport" content="user-scalable=no">` disabling zoom.
**How**: Use `<meta name="viewport" content="width=device-width, initial-scale=1">`. Never `user-scalable=no`. Users with low vision rely on pinch-zoom; disabling it violates WCAG.

### Pattern: Removing 300ms tap delay (web)
**Use when**: Mobile web pages with interactive elements.
**Anti-pattern**: Buttons feel laggy because of legacy 300ms double-tap-zoom delay.
**How**: Apply `touch-action: manipulation` on tappable elements. Removes the 300ms wait while preserving pinch-zoom and double-tap behaviors elsewhere.

### Pattern: Haptic feedback discipline
**Use when**: Mobile native apps confirming important actions.
**Anti-pattern**: Haptic on every tap (exhausting; battery cost).
**How**: Haptic on confirmations, errors, and important state changes — not on every tap. Successful payment: heavy haptic. Failed validation: error haptic. Toggle switch: medium haptic. Tap on a list item: no haptic.

### Pattern: Disabled state
**Use when**: Buttons or inputs that should not respond.
**Anti-pattern**: Styled "disabled" button that still responds to clicks or has no visible difference from enabled.
**How**: Reduce opacity to 0.38 to 0.5. Change cursor to `not-allowed` on web. Apply the semantic `disabled` attribute (HTML) or `disabled` prop. The element must visibly look inactive AND programmatically refuse input. Optional: tooltip or inline message explaining why the action is disabled.

### Pattern: Semantic native controls
**Use when**: Building interactive elements.
**Anti-pattern**: `<div onclick="...">` used as a button — breaks screen readers, keyboard nav, focus management.
**How**: Use `<button>`, `<a href>`, `<input>`, native equivalents (`<Pressable>` in React Native). They come with built-in keyboard handling, focus management, screen reader support, and platform conventions. If you must use a `<div>` for styling reasons, add `role="button"`, `tabindex="0"`, and keyboard event handlers — but you almost never should.

### Pattern: Cursor-driven parallax
**Use when**: Subtle depth effect on hero illustrations or hero canvas.
**Anti-pattern**: DeviceOrientation / DeviceMotion APIs that require sensor permission prompts.
**How**: Pointer events only. Track mouse position via `useMotionValue`. Elements translate 4 to 8px maximum based on cursor position. Capped at 4 to 8 degrees of rotation. The shift is slow (200 to 400ms ease) and feels like depth, not jitter. Disabled on touch devices (no mouse).

### Pattern: Gesture conflict prevention
**Use when**: Card lists with both tap and swipe gestures.
**Anti-pattern**: Tap on card opens detail, swipe on card deletes, but the touch handler can't distinguish between them — both fire.
**How**: One primary gesture per region. If a card supports both:
- Tap = open detail (primary)
- Swipe-left = delete (secondary, with visible affordance)
Threshold disambiguates: short tap with no movement = tap; sustained movement past threshold = swipe. Cancel the tap if movement crosses the threshold.

### Pattern: System gesture respect
**Use when**: Building any mobile UI.
**Anti-pattern**: Blocking edge-swipe-back on iOS, blocking pull-down for Control Center.
**How**: Don't override system gestures. iOS edge-swipe goes back. Pull-down from the top corner opens Control Center. Predictive back on Android works. If your app intercepts these, document why and provide a clear alternative.

### Pattern: Loading button state
**Use when**: Async actions on a button (submit, save, send).
**Anti-pattern**: Button stays clickable during submit; user clicks twice and submits twice.
**How**: Disable the button during async operation. Show a spinner or progress indicator inside the button. Optionally swap label to "Submitting..." or "Saving...". Restore on completion. If the operation takes >3 seconds, show progress (percentage, step indicator) rather than indefinite spinner.

### Pattern: Tap feedback latency budget
**Use when**: Any tappable surface.
**Anti-pattern**: Heavy JavaScript handlers blocking the main thread, delaying tap response past 100ms.
**How**: Keep tap response under 100ms. Use CSS-only state changes where possible (`:active`, `:focus`). Defer heavy work to `requestIdleCallback` or workers. The visual response must lead the action; the action follows the response.

### Pattern: Press feedback selection by aesthetic
**Use when**: Defining the active state for an entire design system.
**Anti-pattern**: Inconsistent press feedback — translate on some, scale on others, color on others.
**How**: Pick one and apply consistently:
- Brutalist: full color inversion (zero milliseconds, instant snap)
- Minimalist: micro-scale `0.98` and slight darken (80 to 150ms)
- High-end: micro-scale `0.98` combined with magnetic physics shift (80 to 150ms)

### Pattern: Hover state selection by aesthetic
**Use when**: Defining the hover state for an entire design system.
**Anti-pattern**: Different hover behavior on every component.
**How**:
- Brutalist: instant inversion or instant border-color shift to accent
- Minimalist: subtle shadow lift, micro-scale, or quiet color shift over 150 to 250ms
- High-end: magnetic button physics with nested icon translation, scale, and color shift over 300 to 500ms with custom cubic-bezier

### Pattern: Cursor on web
**Use when**: Every web interactive element.
**Anti-pattern**: Default cursor on a `<div onclick="...">` — looks not clickable.
**How**: Apply `cursor: pointer` to all clickable elements (buttons, links, clickable cards, custom controls). Apply `cursor: not-allowed` to disabled elements. Apply `cursor: text` only on text inputs (browser default). Never use custom cursor images — accessibility hostile and performance hit.

## Tokens / values

### Touch target sizes
- iOS: 44x44pt minimum
- Android: 48x48dp minimum
- Web: 44x44px minimum
- Mobile input field height: ≥44px
- Touch spacing: ≥8px gap between adjacent targets
- Extend hit area beyond visual bounds via `hitSlop` (RN) or padding (web) for smaller icons
- Test at largest Dynamic Type setting — targets must remain 44pt+

### Feedback timings
- Tap visual response: 80 to 150ms
- Hover transition: 150 to 250ms
- Card hover lift duration: 200 to 300ms
- Active press transform: 80 to 150ms
- Disabled state transition: 200ms
- Disabled to enabled state change: 200ms ease

### Tactile transform values
- Press feedback: `-translate-y-[1px]` or `scale-[0.98]`
- Card hover lift: `translateY(-2px)` to `translateY(-4px)`
- Card image hover scale: `scale-[1.02]` to `scale-[1.05]` inside `overflow-hidden`
- Magnetic button maximum translate: 4 to 8px
- Cursor parallax rotation cap: 4 to 8 degrees
- Trailing icon translate on hover: 4 to 6px

### Drag thresholds
- Drag activation threshold: 8 to 12px movement
- Swipe activation threshold: 30 to 50px movement combined with velocity check
- Tap window after touchstart: <300ms (cancel if movement exceeds threshold)

### Hover state values
- Background brightness shift: 2 to 4% L
- Underline weight shift: 1px → 2px
- Border opacity shift: 8 to 12% → 16 to 24% alpha
- Shadow expansion: small → medium
- Opacity reveal: 0.7 → 1

### Disabled state
- Opacity: 0.38 to 0.5
- Cursor: `not-allowed` (web)
- Semantic `disabled` attribute on form controls
- Optional tooltip explaining why disabled

### Cursor styles (web)
- Clickable: `cursor: pointer`
- Disabled: `cursor: not-allowed`
- Text input: `cursor: text` (browser default)
- Loading: `cursor: progress`
- Move: `cursor: move`
- Resize: `cursor: ew-resize`, `ns-resize`, etc.
- Never custom cursor images (accessibility hostile, performance hit)

### Gesture vocabulary
- Tap = primary selection
- Long-press = secondary actions, context menu
- Double-tap = often "like" or "zoom" depending on context; reserve carefully
- Swipe-left / swipe-right = secondary actions (delete, archive, reveal)
- Swipe-down = dismiss modal or refresh
- Swipe-up = open detail or expand
- Pinch = zoom (preserve always)
- Drag = move or sort (with 8 to 12px threshold)

### Haptic patterns (mobile native)
- Light tap (selection): subtle haptic on tab switch, picker change
- Medium tap (confirmation): toggle, button activation
- Heavy tap (success): payment confirmation, action completion
- Error: distinct error pattern (double pulse)
- Avoid haptic on every interaction — reserve for moments

### Loading patterns
- Button loading: spinner inside button, disable click
- Inline loading: skeleton matching layout shape
- Page loading: thin progress bar at top of viewport
- Long operation (>3s): show progress percentage or step indicator
- Show skeleton when load exceeds 300ms

### Cursor parallax (premium)
- Use `useMotionValue` to track cursor position
- Apply spring damping (`stiffness: 100, damping: 20`)
- Maximum 4 to 8px translation or 4 to 8 degrees rotation
- Slow ease (200 to 400ms)
- Disabled on touch devices
- Disabled under `prefers-reduced-motion: reduce`

### Banned interaction patterns
- Hover-only primary actions (touch has no hover)
- Instant state changes with no animation (looks broken)
- Tap targets <44pt without expanded hit area
- Pixel-perfect tap requirements on small icons
- Custom mouse cursors (accessibility hostile)
- Disabling pinch-zoom via `user-scalable=no`
- DeviceOrientation / DeviceMotion for visual effects (requires sensor permission)
- `useState` for continuous animations (use `useMotionValue` / `useTransform`)
- Overlapping gestures with no disambiguation
- Custom gestures that override system gestures (swipe-back, pinch-zoom, predictive back)
- Controls that look tappable but do nothing (no disabled state)
- Toast that steals focus from current control
- Haptic on every tap (exhausting)
- Generic `<div>` used as `<button>` (use semantic controls)
- Drag triggered immediately on touch without movement threshold

### System gesture protection
- iOS edge-swipe = back navigation (never override)
- iOS top-edge pull = Control Center (never block)
- Android predictive back (never override)
- Pinch-zoom = always preserved
- Two-finger scroll = browser default
- System keyboard shortcuts (Cmd+S, Cmd+Z, browser back) = preserved

## Checklist (severity-tagged)

- [ ] Touch targets ≥44x44pt (iOS) / ≥48x48dp (Android) / ≥44x44px (web) (severity: Critical)
- [ ] 8px minimum gap between adjacent touch targets (severity: Critical)
- [ ] Tap feedback lands within 80 to 150ms (severity: High)
- [ ] Press states use `-translate-y-[1px]` or `scale-[0.98]` (severity: Medium)
- [ ] Hover lift on cards uses 200 to 300ms ease (severity: Medium)
- [ ] No hover-only primary interactions — primary CTAs work without hover (severity: Critical)
- [ ] `cursor: pointer` on all clickable elements (web) (severity: High)
- [ ] `touch-action: manipulation` removes 300ms tap delay (web) (severity: Medium)
- [ ] Pinch-zoom preserved — viewport meta does not set `user-scalable=no` (severity: Critical)
- [ ] Drag threshold of 8 to 12px before drag starts (severity: High)
- [ ] One primary gesture per region; gesture conflicts disambiguated (severity: High)
- [ ] Critical actions have both gesture AND tappable control (severity: Critical)
- [ ] System gestures (swipe-back, pinch-zoom, predictive back) preserved (severity: Critical)
- [ ] Semantic native controls (`<button>`, `<a>`, `<Pressable>`) used (severity: Critical)
- [ ] `useMotionValue` / `useTransform` used for magnetic hover (not `useState`) (severity: High)
- [ ] Cursor parallax disabled on touch devices and under reduced-motion (severity: High)
- [ ] No DeviceOrientation / DeviceMotion APIs for visual effects (severity: Critical)
- [ ] No custom mouse cursor images (severity: High)
- [ ] Disabled state uses 0.38 to 0.5 opacity + cursor change + `disabled` attribute (severity: High)
- [ ] Loading buttons disable click during async operation (severity: High)
- [ ] Show progress or step indicator if operation exceeds 3 seconds (severity: Medium)
- [ ] Skeleton placeholders for operations exceeding 300ms (severity: High)
- [ ] Gesture affordances visible (chevron, label, or onboarding hint) (severity: Medium)
- [ ] Haptic feedback reserved for confirmations and errors (not every tap) (severity: Cosmetic)
- [ ] Predictive back works on Android; iOS edge-swipe works (severity: Critical)
- [ ] No CTAs scale on hover (color or shadow shift only) (severity: Medium)
- [ ] Drag-and-drop has keyboard alternative (severity: High)
- [ ] Reduced-motion fallback on magnetic and parallax effects (severity: Critical)

## Related

- See **motion.md** for animation timing and easing curves on interactive feedback.
- See **accessibility.md** for keyboard navigation, focus management, and gesture alternatives.
- See **components.md** for state-by-state interaction contracts on buttons, inputs, and cards.
- See **layout.md** for navigation patterns and bottom tab discipline.
- See **spacing.md** for touch target spacing and density modes.
- See **dashboards.md** for interactive chart and table behaviors.
