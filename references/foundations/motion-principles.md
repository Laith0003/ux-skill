# Motion principles

> Motion has measurable rules. The ones below come from shipping production UI at the highest bar — toast systems that compose without jank, drawer libraries that survive a real touch screen, modal stacks that don't make users wait. Every rule has a "do" and a "don't" pair and a code-level example where it helps. If a rule and a designer disagree, the rule wins until the designer can articulate which constraint shifts.

Motion is not decoration. It is a runtime property of the interface. Every animation costs frames, cycles, and attention; every animation that ships must earn those costs by communicating something the static interface cannot.

This file is the authority. When in doubt, default to less motion, shorter durations, and tighter curves than the brief asks for. Premium motion is felt, not seen.

---

## Principles (8 categories + polish)

The principles below are grouped: Decision, Easing, Duration, Spring physics, Component motion, Performance, Gesture motion, Accessibility, Polish. Read top to bottom for first-time intake; jump by section for reference.

---

## Decision — when to animate at all

### 1. Frequency gating

Animations happen on infrequent events. They never fire on every keystroke, every scroll tick, every mouse-move, every websocket message. The moment an animation runs on a high-frequency event, three things happen at once: the user can no longer perceive it as a discrete event, the main thread chokes, and the motion stops communicating because it never resolves.

**Rule of thumb:** if the event can fire more than ~3 times a second under normal use, the animation has to either be debounced, sampled, or replaced by an instant state change.

**Do:**
- Animate on commit (form submit, button click, modal open, tab switch).
- Animate on first appearance in viewport (one-shot, `{ once: true }`).
- Animate on hover-enter / hover-leave (low frequency).

**Don't:**
- Animate on every `onChange` of a text input.
- Animate on every scroll event (use `IntersectionObserver`, not scroll listeners).
- Animate on every websocket / streaming update — debounce to render once per ~250ms.

**Code-level example:**

```jsx
// Bad — animates on every keystroke
<input onChange={(e) => { setValue(e.target.value); triggerShake(); }} />

// Good — animates only on failed submit
<form onSubmit={handleSubmit /* triggers shake only on validation fail */}>
```

### 2. Never animate keyboard actions

Tab, Enter, arrow keys, Escape, Space — these are the user's accelerator pedal. They expect zero latency. Any animation in the path between keypress and visible state change reads as lag, not polish. Power users will be the first to notice and the loudest to complain.

The keyboard is the primary interface for accessibility users (screen reader + keyboard navigation), and reduced motion is more than a preference for them — it is a usability requirement.

**Do:**
- On Tab focus: snap the focus ring on instantly. The focus-visible outline can have an opacity transition under 80ms; the element itself moves zero.
- On Enter to submit: show loading state immediately, no enter animation on the spinner.
- On arrow-key navigation in a menu: highlight changes instantly.

**Don't:**
- Slide focus rings across the page with a 200ms transition.
- Animate the dropdown closing when the user presses Escape — close instantly, then optionally fade backdrop.
- Stagger menu items on arrow-key navigation; the user is already past the next item.

### 3. Every animation has a purpose

Every animation in shipped code falls into one of three buckets: cause-effect (the user did X, so this animates to confirm), state-change confirmation (the system transitioned, so the user sees it), or attention direction (something needs to be seen). Decorative motion — motion that exists because the surface "needed something" — is banned.

**The audit question:** if you remove this animation entirely and the user can still tell what happened from the static interface, the animation is decorative. Cut it or earn it by carrying meaning the static frame cannot.

**Do:**
- Modal scales in from `0.96` because it confirms the user's click opened it.
- Toast slides from edge because it draws attention to a transient surface.
- List item fades out on delete because the user needs to see the deletion register.

**Don't:**
- Hero text fade-up that fires every time the user scrolls back — there's no event being confirmed.
- Background ambient pulse on a CTA — the CTA is already visible; the pulse is anxiety.
- Particle systems behind a sign-up form — pure decoration, no cause-effect.

---

## Easing — the easing curves

### 4. Custom cubic-beziers required

The browser ships `ease`, `ease-in`, `ease-out`, `ease-in-out` as defaults. They are too weak for product UI — the curves are gentle parabolas that hit their target without conviction. Every shipped animation uses a custom cubic-bezier. The browser defaults are reserved for prototypes and disposable code.

**Reference set you can copy:**

```css
/* Entrance — overshoot-free decisive land */
--ease-out-quart: cubic-bezier(0.16, 1, 0.3, 1);
--ease-out-expo:  cubic-bezier(0.19, 1, 0.22, 1);

/* Exit — fast departure */
--ease-in-quart: cubic-bezier(0.5, 0, 0.75, 0);
--ease-in-expo:  cubic-bezier(0.7, 0, 0.84, 0);

/* In-place movement — accelerate then settle */
--ease-in-out-quart: cubic-bezier(0.76, 0, 0.24, 1);
--ease-in-out-expo:  cubic-bezier(0.87, 0, 0.13, 1);

/* Standard — for cases where the curve doesn't carry meaning */
--ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
```

**Do:**
- Define the cubic-bezier set as CSS custom properties at the design-system root.
- Pick a curve based on direction (in / out / both) before picking duration.
- Keep the set small — five to seven curves total across the entire surface.

**Don't:**
- Use `transition-timing-function: ease` in any shipped component.
- Define a new cubic-bezier per component — that fragments the motion vocabulary.
- Mix and match cubic-bezier and spring inside the same component.

### 5. ease-out for entrances

When something enters the screen, it should land decisively. Ease-out curves accelerate at the start, decelerate to a confident stop. The motion reads as the element "arriving" rather than drifting.

**Why:** human perception forgives a fast start better than a fast finish. Things that decelerate feel deliberate; things that overshoot feel fidgety.

**Reference:** `cubic-bezier(0.16, 1, 0.3, 1)` for most entrances. `cubic-bezier(0.19, 1, 0.22, 1)` for the few moments that need extra punch.

**Do:**
- Modal entry: ease-out, duration 250-350ms.
- Toast entry: ease-out, duration 180-220ms.
- Dropdown entry: ease-out, duration 150-200ms.
- Hero element fade-up: ease-out, duration 400-600ms.

**Don't:**
- Use ease-in on entry — the element accelerates into existence and lands hard.
- Use ease-in-out on entry — the element drifts in without conviction.

### 6. ease-in for exits

When something leaves the screen, it should depart quickly. Ease-in starts slow, accelerates to the end. The motion reads as "getting out of the way."

**Why:** the user has already decided this surface is done. Holding their attention on its departure punishes them for closing it.

**Reference:** `cubic-bezier(0.5, 0, 0.75, 0)` for most exits. `cubic-bezier(0.7, 0, 0.84, 0)` for snappy exits like tooltip dismissal.

**Do:**
- Modal exit: ease-in, duration 180-250ms (60-70% of entry).
- Toast exit: ease-in, duration 120-180ms.
- Tooltip exit: ease-in, duration 80-120ms.

**Don't:**
- Use ease-out on exit — the element decelerates into nothing and the user waits.
- Match exit duration to entry duration — the asymmetry is the polish.

### 7. ease-in-out for on-screen movement

When an element moves from one position to another on a surface where it already exists (a card reordering, a stepper advancing, a tab indicator sliding), the curve is ease-in-out. The motion accelerates from rest and decelerates back to rest.

**Why:** the element wasn't entering or leaving — it was relocating. Both endpoints carry meaning.

**Reference:** `cubic-bezier(0.76, 0, 0.24, 1)`.

**Do:**
- Tab indicator slide: ease-in-out, duration 200-280ms.
- Stepper progress fill: ease-in-out, duration 250-350ms.
- Card reorder (sortable lists): ease-in-out, duration 200-300ms with `layoutId` shared-element transitions.

**Don't:**
- Use ease-out for in-place movement — it reads as "arriving" when nothing arrived.
- Mix ease-out and ease-in across the same logical motion path.

### 8. linear for constant motion only

Linear curves are reserved for motion that should not accelerate or decelerate — loading bars filling, infinite scroll skeletons, marquee tickers, progress indicators with a known mechanical pacing.

**Why:** linear is the only curve that communicates "this is happening at a constant rate." For any motion that has a beginning and an end, linear feels mechanical and dated.

**Do:**
- Loading bar fill from 0 to 100%: linear, duration matched to actual load time.
- Skeleton shimmer cycle: linear, 1200-1800ms loop.
- Marquee scroll: linear, duration calculated from content length and target velocity.

**Don't:**
- Use linear on any UI transition with a start and end state (modal open, hover lift, focus ring).
- Animate position changes with linear — reads as a robot move.

---

## Duration — per-element timing

Durations are measured in milliseconds and tuned per component type. The values below are not guidelines; they are the band you ship within unless you can defend a specific exception in writing.

### Per-element ranges

| Element | Enter duration | Exit duration | Notes |
|---|---|---|---|
| Button feedback (`:active`, hover) | 100-160ms | 80-120ms | Press feedback below 100ms reads as glitchy; above 200ms reads as laggy |
| Dropdown menu / popover | 150-250ms | 100-180ms | Smaller surface = shorter duration |
| Modal / dialog | 250-400ms | 180-280ms | Up to 500ms for full-screen sheets |
| Sheet / drawer (mobile) | 280-450ms | 200-320ms | Larger surface deserves more time |
| Tooltip | 150ms (enter, with 400ms delay) | 80-120ms (exit, 0ms delay) | Skip delay on sustained hover |
| Toast notification | 180-260ms (slide-in) | 200-300ms (slide-out or fade) | Exit can be longer if dismissed automatically |
| Tab indicator slide | 200-280ms | n/a (no exit) | ease-in-out |
| Hero fade-up on scroll | 400-600ms | n/a (one-shot) | Up to 800ms with blur reveal on premium |
| Page transition | 300-500ms | 200-350ms | Coordinate with exit of outgoing route |
| List item entry (per child) | 200-300ms | 150-220ms | With stagger of 30-80ms between siblings |

### Sub-300ms rule for micro-interactions

Anything the user triggers and expects to see resolve immediately — button presses, hover states, focus rings, dropdown menus — must complete in under 300ms. The user's attention budget for a "did anything happen?" question is roughly 300ms; past that, they look elsewhere or click again.

**Do:**
- Button press feedback: 120ms.
- Hover lift: 200ms.
- Dropdown menu entry: 180ms.

**Don't:**
- Ship a 400ms hover transition because "it looks smoother."
- Stretch micro-interactions to make the surface feel "premium" — premium is faster, not slower.

### Asymmetric enter / exit

Exit duration is 60-70% of entry duration. When the user dismisses something, they have already decided it's done. The element should get out of the way faster than it arrived.

**Reference math:**
- Modal enter 300ms → exit 200ms.
- Toast enter 240ms → exit 160ms.
- Tooltip enter 150ms → exit 100ms.

**Do:**
- Calculate exit duration as `0.65 * enterDuration`, round to nearest 10ms.
- Pair ease-out (entry) with ease-in (exit) so curves match direction.

**Don't:**
- Mirror exit duration to entry duration — feels sluggish on dismissal.
- Use the same curve for both directions.

---

## Spring physics — when springs vs tweens

Springs and tweens (cubic-bezier curves) are different motion paradigms. Tweens describe a fixed path from A to B over fixed time. Springs describe a physical system reaching equilibrium — the motion is shaped by stiffness, damping, mass, and initial velocity.

### When to use tweens (cubic-bezier)

Use tweens for predictable, controlled motion where the start, end, and duration are known and matter. Most product motion is tween motion.

**Cases:**
- Modal slide-in (start and end positions are known).
- Drawer open (slides from edge to fixed position).
- Tab indicator slide.
- Fade in / out.
- Stagger reveals.

### When to use springs

Use springs for organic, weighty motion where the system responds to user input or where mass is part of the meaning. Springs shine on drag-release and tactile gestures.

**Cases:**
- Drag handle release (the element settles into place with weight).
- Toggle switch flip.
- Press feedback that should feel tactile (button push).
- Magnetic hover (cursor pulls toward element).
- Card flick / dismiss in card stacks.
- Modal opening on a click (a moment of weight is appropriate).

### Spring config style

Use the modern `{ duration, bounce }` config (the Apple-style API), not the older stiffness/damping/mass triplet. The duration/bounce model is easier to reason about, easier to tune, and matches how iOS / macOS feel.

```js
// Modern config
{ duration: 0.4, bounce: 0.2 }

// Old config (avoid)
{ stiffness: 300, damping: 26, mass: 1 }
```

**Mapping:**
- `duration` is the perceived time (in seconds) from start to settle.
- `bounce` is from `-1` (overdamped, no overshoot) to `1` (heavily underdamped, lots of bounce). For product UI, stay between `0` and `0.2`.

### Bounce budget for product UI

Subtle bounce only. `bounce <= 0.2` for any motion the user sees more than once a day.

Aggressive bounce (`bounce > 0.3`) is reserved for celebration moments — the confetti drop on a checkout success, the trophy reveal on a milestone, the rare flourish that the user is meant to remember. Use it twice per surface. Three times and it becomes noise.

**Do:**
- Toggle flip: `{ duration: 0.3, bounce: 0.15 }`.
- Drag-release of a card back into its slot: `{ duration: 0.5, bounce: 0.2 }`.
- Celebration confetti scatter: `{ duration: 0.8, bounce: 0.4 }` (rare moment).

**Don't:**
- Use bounce > 0.2 on routine UI (every button, every menu).
- Apply spring physics to every page-load reveal — page loads need predictable timing, not weight.

---

## Component motion — per-component rules

### `:active` uses scale, never displacement

When the user presses a button or tappable surface, the press feedback is `scale(0.97)` or `-translate-y-[1px]`. Never use `translate-x` (horizontal displacement) for press feedback — it reads as a swipe, not a push.

```css
.btn {
  transition: transform 100ms cubic-bezier(0.4, 0, 0.2, 1);
}
.btn:active {
  transform: scale(0.97);
  /* OR */
  transform: translateY(-1px);
}
```

**Do:**
- Scale 0.97 for press feedback (small, perceptible, not toy-like).
- TranslateY(-1px) for surfaces that should feel "lifted off" the page.

**Don't:**
- Scale below 0.95 — looks like the button is collapsing.
- Use translateX on press — reads as drag.

### Never animate from `scale(0)`

Starting an entrance animation from `scale(0)` reads as the element materializing from a single pixel. The eye doesn't track that; it just sees a sudden pop. Start from `scale(0.96)` minimum.

```jsx
// Bad
initial={{ scale: 0, opacity: 0 }}

// Good
initial={{ scale: 0.96, opacity: 0 }}
```

**Do:**
- Modal entry: `scale(0.96) → scale(1)`.
- Card entry: `scale(0.98) → scale(1)`.
- Avatar reveal: `scale(0.9) → scale(1)` (maximum stretch for routine entry).

**Don't:**
- `scale(0)` for routine entries.
- `scale(1.5) → scale(1)` overshoots that fight the user's eye.

### Popover transform-origin anchors to the trigger

When a popover, tooltip, or context menu opens, its `transform-origin` should point at the trigger that opened it — not at the popover's own center. The user's eye is on the trigger; the popover should appear to grow out of that point.

```css
.popover {
  /* Trigger is below the popover, so anchor at the bottom-center */
  transform-origin: bottom center;
}
```

**The exception:** modals and dialogs anchor at center because they exist independent of a spatial trigger (a click anywhere can open them).

**Do:**
- Dropdown menu under a button: `transform-origin: top` (grows down from button).
- Tooltip above an icon: `transform-origin: bottom` (grows up to icon).
- Context menu on right-click: `transform-origin: top left` (grows from click point).

**Don't:**
- Default `transform-origin: center` on all popovers — feels disconnected from trigger.

### Tooltip enter delay only on first hover

Tooltips have a delay before they appear — typically 400ms — so they don't flash on every cursor passthrough. But on sustained interaction (the user hovered one tooltip, moved to a sibling within ~1 second), the delay should be skipped. The user is now actively reading; making them wait 400ms per item is hostile.

```js
// Pseudocode pattern
const lastTooltipHidden = useRef(0);
const SKIP_DELAY_WINDOW = 1000; // ms

const handleEnter = () => {
  const skipDelay = Date.now() - lastTooltipHidden.current < SKIP_DELAY_WINDOW;
  setTimeout(showTooltip, skipDelay ? 0 : 400);
};
```

**Do:**
- 400ms first-hover delay.
- 0ms delay if previous tooltip was shown within last 1000ms.

**Don't:**
- 400ms delay on every tooltip in a list — punishes scanning.
- Zero delay on every tooltip — they flash on cursor passthrough.

### Blur during crossfade hides imperfect alignment

When two elements crossfade — one fading out, another fading in, occupying the same screen position — even pixel-perfect alignment looks off because the two elements briefly co-exist at 50% opacity. A blur on both during the crossfade hides that artifact.

```css
.crossfade-out, .crossfade-in {
  transition: opacity 250ms ease, filter 250ms ease;
}
.crossfade-out {
  opacity: 0;
  filter: blur(8px);
}
```

**Use case:** image swaps in a gallery, avatar updates in a list, hero image swaps on tab change.

**Do:**
- Apply `filter: blur(8-12px)` during the crossfade.
- Resolve the blur to `blur(0)` on the incoming element.

**Don't:**
- Apply blur to text crossfades — too heavy, looks broken.
- Apply blur outside the crossfade window — it lingers.

### `@starting-style` for entry-only styles

For pure-CSS entry transitions with no JS state, use `@starting-style`. It lets you declare a "starting" CSS rule that applies only on the first frame after the element appears — perfect for one-shot entries without React mount logic.

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 200ms ease-out, transform 200ms ease-out;
}

@starting-style {
  .toast {
    opacity: 0;
    transform: translateY(-12px);
  }
}
```

**Do:**
- Use `@starting-style` for components that mount once and never re-enter (toasts, notifications, modal first-mount).
- Pair with `transition-behavior: allow-discrete` for entries that include `display` property changes.

**Don't:**
- Use `@starting-style` for components that toggle visibility — JS-controlled state is more reliable across browsers.

---

## Performance — the hardware-acceleration trap

### Animate `transform` and `opacity` ONLY

These are the only two CSS properties that the browser compositor can animate without triggering layout or paint. Every other property — `width`, `height`, `top`, `left`, `margin`, `padding`, `color`, `background-color`, `filter`, `box-shadow`, `border-radius` — triggers either layout (which cascades through the entire DOM tree) or paint (which forces a re-rasterize). Either drops frames on mid-range hardware.

**The compositor-only path:**

```css
/* Hardware-accelerated */
transform: translateX(20px);
transform: scale(0.98);
transform: rotate(8deg);
opacity: 0.6;
```

**The slow path:**

```css
/* Forces layout — avoid */
width: 200px;
height: 100px;
top: 20px;
left: 10px;
margin-left: 16px;

/* Forces paint — avoid */
background-color: red;
filter: blur(8px);
box-shadow: 0 10px 20px black;
border-radius: 12px;
```

**Workarounds for properties that look like they need to animate:**

| You want to animate | Use instead |
|---|---|
| `width` / `height` | `scaleX` / `scaleY` with `transform-origin` |
| `top` / `left` | `translateX` / `translateY` |
| `margin` | `transform: translate()` on the affected element |
| `background-color` | Two stacked layers; cross-fade `opacity` between them |
| `box-shadow` | Two stacked shadows on parent / pseudo; cross-fade `opacity` |
| `border-radius` (rare) | Pre-render two shapes; cross-fade |
| `filter: blur()` (animated) | Acceptable for one-shot entries; never animate continuously |

### The CSS-vars-on-parent recalc trap

When you animate a CSS custom property on a parent element, every child that reads that variable re-evaluates on every animation frame. If the parent has 50 children and the variable is in a `background`, `color`, or `border` rule, you've just paid for 50 paints per frame.

**Bad:**

```css
.parent {
  --x: 0px;
  animation: move 1s linear infinite;
}
@keyframes move { to { --x: 100px; } }

.child {
  transform: translateX(var(--x));
  background: hsl(var(--hue) 50% 50%);  /* if --hue also animates, paint storm */
}
```

**Fix:** isolate animated CSS variables to leaf elements. If you need a parent-level variable to drive multiple children, accept the cost or restructure so the animation runs on a single element with siblings positioned via `transform`.

**Do:**
- Animate CSS vars on the element that directly reads them.
- Use `@property` registration to give the variable a type, which lets the compositor handle it more efficiently for some property types.

**Don't:**
- Animate a CSS variable on `:root` that's read in 200 places.
- Combine animated CSS vars with `filter` or `background` (paint-heavy properties).

### Framer Motion shorthand isn't always compositor-only

When you write `animate={{ x: 100 }}` in Framer Motion, the library typically translates that to a transform — but React re-renders are involved, and edge cases (interrupted animations, layout shifts, hybrid animations mixing transform and non-transform properties) can fall off the compositor-only path.

For animations that must hit the compositor every frame (drag handles, scrub animations, anything tied to a continuous input), use `useMotionValue` paired with `style={{ transform }}` directly. This bypasses React's render loop entirely and writes to the DOM on every frame via the motion value subscription.

**Bad — falls back to React updates under contention:**

```jsx
<motion.div animate={{ x: dragX }} />
```

**Good — pure compositor path:**

```jsx
const x = useMotionValue(0);
const transformX = useTransform(x, (val) => `translateX(${val}px)`);

<motion.div style={{ transform: transformX }} />
```

### CSS animations beat JS animations under load

CSS animations and transitions run on the compositor thread. JS-driven animations run on the main thread by default — even when they animate transform / opacity. Under load (during a network request, when other JS is parsing, when the user is scrolling), JS animations drop frames first.

**Rule of thumb:** if you can express the animation in CSS (keyframes, transitions), do it in CSS. Reach for JS only when you need:
- Coordination across many elements with shared state.
- User-driven inputs (drag, scrub, gesture).
- Conditional logic mid-animation.

**Do:**
- CSS keyframes for skeleton shimmer.
- CSS transitions for hover / focus.
- CSS `@starting-style` for one-shot entries.

**Don't:**
- Build a hover lift in JS when a one-liner CSS transition does the job.
- Trigger CSS class toggles from JS just to "feel modern" — `:hover`, `:focus`, `:active` exist.

### Web Animations API for programmatic-CSS use cases

The Web Animations API (`element.animate()`) gives you JS-level programmability while the animation runs on the compositor. It's the right tool for animations that need to be triggered or coordinated from JS but should perform like CSS.

```js
element.animate(
  [
    { transform: 'translateY(20px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 },
  ],
  { duration: 300, easing: 'cubic-bezier(0.16, 1, 0.3, 1)', fill: 'forwards' }
);
```

**Use cases:**
- Triggering an entry animation from a React effect without setting state on the parent.
- Animating an element that doesn't yet exist in React state (imperative DOM manipulation).
- Pausing / reversing / scrubbing animations programmatically.

**Do:**
- Use WAAPI for animations triggered from one-shot user actions where React state is overkill.
- Combine with `getAnimations()` to coordinate or cancel running animations.

**Don't:**
- Reach for WAAPI when a CSS `transition` does the job.
- Use WAAPI for continuous, frame-driven inputs (use `useMotionValue` instead).

---

## Gesture motion — drag, swipe, pull

### Velocity-based dismissal

A drag dismissal is not "did the user pull past 50% of the screen?" It's "is the user still moving with intent?" Velocity-based dismissal measures the pointer's velocity at release and dismisses if it exceeds a threshold; otherwise the surface snaps back.

**Threshold:** velocity > 0.11 px/ms dismisses. Below that, snap back.

**Why velocity wins over distance:**
- A user can fling 30% of the way and clearly intend to dismiss.
- A user can hesitantly drag 70% and reconsider — distance-only would dismiss against intent.

```js
const VELOCITY_THRESHOLD = 0.11; // px/ms

const handleDragEnd = (e, info) => {
  const velocity = info.velocity.y; // or .x for horizontal
  const shouldDismiss = Math.abs(velocity) > VELOCITY_THRESHOLD;
  if (shouldDismiss) dismiss();
  else snapBack();
};
```

**Do:**
- Sample velocity over the last ~100ms of the drag.
- Combine velocity with a minimum-distance fallback (in case velocity reads near-zero on a slow drag past a clear threshold).

**Don't:**
- Use only distance — feels rigid and ignores intent.
- Use only velocity without a distance fallback — slow deliberate drags break.

### Boundary damping

When a user drags past a natural boundary (a sheet pulled below its fully-open position, a scrollable list at its top), the surface should resist. The resistance is nonlinear: the further past the boundary, the more it pushes back. This is rubber-band physics.

```js
const damp = (overshoot) => {
  // Nonlinear damping: every additional pixel past boundary
  // contributes diminishingly to actual movement
  const RESISTANCE = 2.5;
  return overshoot / (1 + Math.abs(overshoot) / RESISTANCE * 0.1);
};
```

**Do:**
- Resist past natural boundaries with diminishing-returns damping.
- Snap back to boundary on release with spring physics (`bounce: 0.15`).

**Don't:**
- Hard-stop drag at the boundary (feels broken).
- Let drag continue indefinitely past the boundary (loses sense of where the surface ends).

### Pointer capture on drag-start

When a drag begins, immediately call `element.setPointerCapture(pointerId)`. This tells the browser to keep delivering pointer events to that element even if the user's finger drifts outside its bounds. Without pointer capture, fast drags lose the pointer when fingers leave the element and the surface jumps or stops mid-motion.

```js
const handlePointerDown = (e) => {
  e.currentTarget.setPointerCapture(e.pointerId);
  // start drag tracking
};

const handlePointerUp = (e) => {
  e.currentTarget.releasePointerCapture(e.pointerId);
  // end drag tracking
};
```

**Do:**
- Call `setPointerCapture` on `pointerdown` for any draggable element.
- Release capture on `pointerup` / `pointercancel`.

**Don't:**
- Track drags with `mousemove` / `touchmove` listeners on `document` — pointer events are unified, simpler, and more reliable.
- Forget to release capture — leaks pointer ownership and breaks subsequent interactions.

### Multi-touch protection

A drag is a single-pointer interaction. If a second pointer enters the element while a drag is in progress, cancel the drag — don't try to track two fingers as one drag, and don't ignore the second pointer (which leads to ghost drags when the first pointer lifts).

```js
const activePointerId = useRef(null);

const handlePointerDown = (e) => {
  if (activePointerId.current !== null) return; // ignore second pointer
  activePointerId.current = e.pointerId;
  // start drag
};

const handlePointerDown2 = (e) => {
  // If a second pointer enters during a drag, cancel
  if (activePointerId.current !== null && activePointerId.current !== e.pointerId) {
    cancelDrag();
    activePointerId.current = null;
  }
};
```

**Do:**
- Track the active pointer ID and ignore subsequent `pointerdown`s.
- Cancel the drag if the active pointer is cancelled.

**Don't:**
- Try to track two fingers as one drag (use a dedicated multi-touch pattern for pinch / zoom instead).
- Track multiple drags simultaneously on the same element.

---

## Accessibility — respecting preferences

### `prefers-reduced-motion: reduce` does NOT mean zero motion

Reduced motion is the user telling you "I get motion-sick or distracted by animation." It does not mean "remove all visual feedback." Removing animation entirely strips signal — users still need to perceive state changes. The fix is shorter, gentler, no-bounce versions of the same animations.

**Reduced-motion rules:**
- Duration: <= 100ms.
- No spring physics (use linear or simple ease).
- No overshoot, no bounce.
- No blur reveals.
- No directional slides over 8px.
- Cross-fades become instant opacity changes or shortened opacity transitions (~100ms).

```css
.toast {
  transition: transform 240ms cubic-bezier(0.16, 1, 0.3, 1),
              opacity 240ms cubic-bezier(0.16, 1, 0.3, 1);
}

@media (prefers-reduced-motion: reduce) {
  .toast {
    transition: opacity 100ms linear;
    transform: none;
  }
}
```

**Do:**
- Keep state-change feedback visible (color change, opacity transition).
- Replace `translateY` reveals with opacity-only fades.
- Remove blur, scale overshoot, and bounce.

**Don't:**
- Set `animation: none` globally under reduced motion — kills state feedback.
- Skip the feature entirely for reduced-motion users.

### Hover gating with `(hover: hover) and (pointer: fine)`

Touch devices don't have hover. Applying `:hover` styles on a touch device causes the "sticky hover" bug: the user taps an element, the hover state activates, and stays activated until they tap somewhere else. Cards remain visually "lifted," buttons remain "tinted," the surface looks broken.

The fix is to gate hover effects behind a media query that only matches true hover-capable devices:

```css
@media (hover: hover) and (pointer: fine) {
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  }
}
```

**Do:**
- Wrap every hover effect in the media query.
- Define mobile-specific tactile feedback (active state, ripple) separately.

**Don't:**
- Use bare `:hover` on interactive elements.
- Rely on `:hover` to communicate state — touch users won't see it.

### Don't disable animations entirely for reduced-motion users

This is worth saying twice because it's a common mistake. The naive implementation of reduced-motion support is `* { animation: none; transition: none; }` — which kills state-change feedback and makes the interface read as broken to the very users you're trying to help.

The correct approach is graceful reduction: shorter, gentler, no-spring versions of every animation, not removed animations.

**Do:**
- Audit every animation under reduced-motion settings.
- Verify state changes are still perceptible (color shift, opacity transition, focus ring).

**Don't:**
- Blanket-disable animations.
- Treat reduced-motion as an excuse to not design the reduced state.

---

## Polish — the things that separate amateur from premium

### Stagger lists 30-80ms per child

List entries and grid reveals get a stagger between children. The right window is 30-80ms per child.

- Below 30ms: reads as flashing — too fast for the eye to track each child as discrete.
- Above 80ms: reads as slow — the user starts looking elsewhere before the last child arrives.

**Reference math:**
- Short list (3-5 items): 50ms per child.
- Medium list (6-12 items): 40ms per child.
- Long list (12+ items): 30ms per child or skip stagger (use a single wave).

```jsx
{items.map((item, i) => (
  <motion.li
    key={item.id}
    initial={{ opacity: 0, y: 12 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.3, delay: i * 0.04, ease: [0.16, 1, 0.3, 1] }}
  >
    {item.label}
  </motion.li>
))}
```

**Do:**
- Stagger 30-80ms per child.
- Cap total stagger time at 600ms — past that, the last child arrives after the user has moved on.

**Don't:**
- Mount all children at once (composition flattens).
- Stagger at 100ms+ per child (theatrical).

### Motion cohesion — motion personality matches component personality

A heavy modal should feel heavy. A snappy tooltip should feel snappy. The curves and durations you pick should encode the same personality the static design does.

**Examples of cohesion:**

| Component | Personality | Curve | Duration |
|---|---|---|---|
| Tooltip | Lightweight, snappy | ease-out-quart | 150ms |
| Dropdown | Functional, swift | ease-out-quart | 180ms |
| Modal | Weighty, deliberate | ease-out-expo + slight spring | 320ms |
| Full-screen sheet | Substantial, considered | ease-out-quart | 450ms |
| Hero section reveal | Cinematic | ease-out-expo | 600-800ms |

**Do:**
- Pick durations and curves that match the visual weight of the component.
- Treat motion as a property of the component's identity, not an applied effect.

**Don't:**
- Use the same 250ms ease-out on every component (flattens the motion vocabulary).

### Next-day review

Motion looks good immediately because of novelty — the eye is excited to see something move and forgives flaws. The next day, with fresh eyes, the same motion can read as showy, slow, or wrong. Review motion the day after you ship it, when the novelty has worn off.

**Process:**
1. Ship the animation on Tuesday.
2. Don't look at it again that day.
3. Wednesday morning, load the surface and watch the animation play once. Is it still good?
4. If it now feels too long, too dramatic, or too frequent — cut it.

**Do:**
- Build a "motion review" pass into your sprint at +24h.
- Test on a colleague who hasn't seen it — first-impression honesty.

**Don't:**
- Ship motion that you've watched 200 times in dev — you've gone motion-blind.

### Real-device gesture testing

Trackpads, mouse wheels, and desktop touchscreens all lie about how the gesture feels on a phone. The acceleration curves are different, the friction is different, the pointer precision is different.

For any gesture-driven motion (drag-to-dismiss, swipe-to-delete, pull-to-refresh, sheet drag), test on:
- iOS Safari (real iPhone, not simulator).
- Android Chrome (real Android, not emulator).
- A desktop trackpad (for accessibility users navigating via trackpad).

**What you'll find:**
- Velocity thresholds tuned on desktop are too low on phone (fingers move faster than expected).
- Damping feels too aggressive on phone (touchscreens have more friction).
- Hover-triggered animations don't fire on touch — silent regressions.

**Do:**
- Maintain a small device shelf: one iOS, one Android, both refreshed yearly.
- Block ship until the gesture is verified on real device.

**Don't:**
- Trust the desktop dev tools touch emulator for gesture work — it's directionally correct but not feel-accurate.

---

## Tokens / values cheatsheet

Quick-reference numbers. These are the values you use unless you can defend a specific exception in writing.

| Concern | Value |
|---|---|
| Button feedback | 100-160ms |
| Dropdown / popover | 150-250ms |
| Modal / dialog | 250-400ms |
| Sheet / drawer | 280-450ms |
| Tooltip enter (with delay) | 150ms after 400ms delay |
| Tooltip exit | 80-120ms (0ms delay) |
| Toast | 180-260ms in, 200-300ms out |
| Tab indicator slide | 200-280ms |
| Hero fade-up | 400-600ms |
| Page transition | 300-500ms |
| Stagger between children | 30-80ms |
| Velocity dismiss threshold | 0.11 px/ms |
| Sustained-hover skip-delay window | 1000ms |
| Reduced-motion max duration | 100ms |
| Active state scale | 0.97 |
| Active state lift | translateY(-1px) |
| Minimum scale for entries | 0.96 |
| Spring bounce in product UI | <= 0.2 |
| Celebration spring bounce | 0.3-0.4 (rare) |
| Exit duration vs entry | 60-70% |
| Compositor-safe properties | transform, opacity |

### Curve presets (copy these)

```css
--ease-out-quart:    cubic-bezier(0.16, 1, 0.3, 1);
--ease-out-expo:     cubic-bezier(0.19, 1, 0.22, 1);
--ease-in-quart:     cubic-bezier(0.5, 0, 0.75, 0);
--ease-in-expo:      cubic-bezier(0.7, 0, 0.84, 0);
--ease-in-out-quart: cubic-bezier(0.76, 0, 0.24, 1);
--ease-in-out-expo:  cubic-bezier(0.87, 0, 0.13, 1);
--ease-standard:     cubic-bezier(0.4, 0, 0.2, 1);
```

---

## Checklist (severity-tagged)

Run this before shipping any surface with motion.

- [ ] All animations on `transform` and `opacity` only (**Critical**)
- [ ] `prefers-reduced-motion: reduce` respected with graceful reduction, not removal (**Critical**)
- [ ] No animations on keyboard-only actions (Tab, Enter, arrows) (**High**)
- [ ] Custom cubic-bezier curves, not browser defaults (**High**)
- [ ] Duration within per-element ranges from the cheatsheet (**High**)
- [ ] Exit duration 60-70% of entry duration (**High**)
- [ ] Pointer capture on every draggable element (**High**)
- [ ] Hover effects gated behind `(hover: hover) and (pointer: fine)` (**High**)
- [ ] `:active` uses `scale(0.97)` or `translateY(-1px)` (**Medium**)
- [ ] No animations starting from `scale(0)` (**Medium**)
- [ ] Popover transform-origin anchors to the trigger (**Medium**)
- [ ] Stagger 30-80ms per child on list reveals (**Medium**)
- [ ] Spring bounce <= 0.2 in routine product UI (**Medium**)
- [ ] Velocity threshold of 0.11 px/ms on drag-dismiss (**Medium**)
- [ ] CSS-vars-on-parent-recalc trap audited (**Medium**)
- [ ] CSS animations preferred over JS where equivalent (**Medium**)
- [ ] Tooltip skip-delay on sustained hover (**Cosmetic**)
- [ ] Blur during crossfades for swap animations (**Cosmetic**)
- [ ] Motion cohesion: curve / duration matches component personality (**Cosmetic**)
- [ ] Next-day review done, blind to novelty bias (**Cosmetic**)
- [ ] Real-device gesture test on iOS + Android (**Cosmetic**, blocking for gesture-heavy surfaces)

---

## Related

- see `foundations/accessibility.md` for the full reduced-motion + hover handling specification, including screen reader announcements that pair with motion
- see `foundations/interaction.md` for touch targets, tactile feedback, and the static-interface contract motion supplements
- see `foundations/motion.md` for the higher-level motion philosophy this file operationalizes
- see `styles/anti-slop.md` for the decorative-animation ban and the broader catalogue of motion fingerprints to avoid
- see `foundations/anti-patterns.md` for the lintable subset of motion violations (`outline:none` without focus-visible replacement, animating width/height, missing `prefers-reduced-motion` media queries)
