# Motion

> Motion expresses cause and effect. Every animation must communicate something the static interface cannot. If it does not communicate, cut it.

## Recommended engines (first-class in `/ux-motion`)

ux-skill's `/ux-motion` command accepts a `--engine` flag selecting one of three first-class implementations. Each one is fully supported in `data/motion-presets.json` — every preset has a snippet for all three.

| Engine | URL | Use when |
|---|---|---|
| **Framer Motion** (default) | https://www.framer.com/motion/ | React projects, declarative API, ~30 KB gzipped. Best balance of power and ergonomics for most apps. |
| **GSAP** | https://gsap.com | Cinematic scroll-pinned scenes, SVG path animation, complex timelines. The crown of web animation — every motion preset in our manifest ships with a GSAP snippet you can copy. Free for commercial use as of 2024-05 (Webflow acquisition). |
| **CSS keyframes** | https://developer.mozilla.org/en-US/docs/Web/CSS/@keyframes | Server-rendered or no-JS surfaces. Smallest cost. ux-skill outputs CSS-only when the picked style or brief requires it (e.g. <code>SSR-static</code>, <code>JS-disabled-allowed</code> must-have). |

**Invocation:**

```bash
ux motion --engine framer-motion    # default
ux motion --engine gsap             # cinematic scroll, complex timelines
ux motion --engine css              # SSR / no-JS surfaces
```

For motion principles beyond the engine choice (timing, easing, restraint), see [`motion-principles.md`](motion-principles.md) in the same folder.

## Principles

1. **Motion communicates, never decorates** — Every animation expresses a cause-effect relationship: a state change, a hierarchy shift, a confirmation, a spatial transition. Decoration-only motion is noise that drains attention and battery.

2. **Duration is calibrated to function** — 150 to 300ms for micro-interactions (button press, hover, focus). 250 to 400ms for entry transitions (modal open, page transition). 400 to 700ms for complex transitions (large content swap, multi-element orchestration). Never exceed 500ms for UI feedback, never exceed 900ms for major entries.

3. **Easing has direction and meaning** — `ease-out` (`cubic-bezier(0.16, 1, 0.3, 1)`) for entering. `ease-in` for exiting. `linear` never on UI transitions (linear motion reads mechanical and dated). Spring physics or custom cubic-beziers for natural feel.

4. **Exit is faster than enter** — Exit animations run at 60 to 70% of enter duration. The asymmetry feels more responsive. A modal that opens in 300ms closes in 200ms.

5. **Animate only `transform` and `opacity`** — These are the only two properties that hit the compositor without triggering layout. Animating `width`, `height`, `top`, or `left` causes layout shift, CLS, and frame drops.

6. **Respect reduced-motion at every level** — `prefers-reduced-motion: reduce` is a contract. Replace `translateY` reveals with opacity-only fades. Pause background ambient motion. Drop blur from scroll entries. Never opt the user back in by default.

7. **Interruptibility is mandatory** — User tap, scroll, or gesture cancels in-progress animation immediately. Animations never block input. UI stays interactive during motion.

8. **Stagger lists, not chrome** — List or grid items enter with a 30 to 50ms cascade between siblings. The wave is direction-aware (left-to-right LTR, mirrored RTL). All-at-once entries flatten composition; too-slow staggers (100ms+) feel theatrical.

9. **Spring physics for tactile UI gestures** — Drag handles, toggles, modal open/close use spring physics rather than cubic-bezier curves. Standard spring: `{ type: "spring", stiffness: 100, damping: 20 }`. The motion reads as having weight.

10. **Perpetual motion is isolated and memoized** — Any infinite loop or perpetual animation lives in its own microscopic memoized client component. A floating ambient pulse must not re-render the page it sits on.

## Do / Don't

| Do | Don't |
|---|---|
| Animate `transform` and `opacity` only | Animate `width`, `height`, `top`, `left` |
| Use `ease-out` for entering, `ease-in` for exiting | Use `linear` for UI transitions |
| Use spring physics for tactile UI gestures | Use cubic-bezier for drag-and-toggle gestures (use springs) |
| Keep micro-interactions in the 150 to 300ms range | Ship 500ms+ animations on hover and tap |
| Stagger list entries at 30 to 50ms per item | Mount lists all-at-once or stagger at 100ms+ |
| Set exit duration to 60 to 70% of enter | Mirror exit to enter (feels sluggish) |
| Use `useMotionValue` / `useTransform` for magnetic hover | Use `useState` for continuous animations (kills performance) |
| Apply `backdrop-blur` only to fixed or sticky elements | Apply blur to scrolling containers (kills frame rate) |
| Isolate perpetual loops in memoized leaf components | Run perpetual loops in components that re-render with parent |
| Wrap animation `useEffect` with cleanup | Leave GSAP timelines and WebGL contexts uncleaned |
| Use `IntersectionObserver` for scroll triggers | Use `window.addEventListener('scroll')` |
| Honor `prefers-reduced-motion: reduce` | Force motion on users who opted out |
| Use `layoutId` for shared element transitions | Animate position changes with manual offsets |
| Apply grain / noise to fixed `pointer-events-none` layers | Apply grain to scrolling containers |
| Use `will-change: transform` sparingly, then remove | Apply `will-change` to every animated element forever |
| Keep loading states simple (skeleton, thin progress bar) | Block content with elaborate loading animations |
| Animate one or two key elements per view | Animate every element on entry |

## Examples

### Pattern: Hover lift on interactive cards
**Use when**: Clickable cards, primary CTAs, image tiles.
**Anti-pattern**: Cards that snap on hover with no transition, or cards that scale dramatically (1.2x or higher) and shift surrounding content.
**How**: `translateY(-2px)` to `translateY(-4px)` combined with a shadow elevation shift. Duration 200 to 300ms with `cubic-bezier(0.16, 1, 0.3, 1)`. The change is unmistakable but never showy. Never scale CTAs on hover — looks toy-like; use color or shadow shift only.

### Pattern: Tactile press feedback
**Use when**: Buttons, cards, any tappable surface.
**Anti-pattern**: No visual response on tap, or scaling so dramatic it shifts layout.
**How**: On `:active`, apply `-translate-y-[1px]` or `scale-[0.98]` to simulate a physical push. Duration 80 to 150ms. Restore on release. The combined effect feels tactile without breaking layout.

### Pattern: Scroll-triggered fade-up
**Use when**: Sections entering the viewport on first scroll.
**Anti-pattern**: 100px slide-ups with rotation that disorient, or repeated fade-ups every time the user scrolls back.
**How**: As a section enters viewport, fade `opacity 0 → 1` combined with `translateY(12 to 24px) → translateY(0)`. Duration 400 to 600ms with `cubic-bezier(0.16, 1, 0.3, 1)`. Implementation via `IntersectionObserver` with `{ once: true }`. Once is enough.

### Pattern: Cinematic scroll entry (premium)
**Use when**: High-end marketing surfaces where motion is part of the experience.
**Anti-pattern**: Same fade-up everywhere on every section, with no escalation.
**How**: Combine `translate-y-16`, `blur-md`, `opacity-0` resolving to `translate-y-0`, `blur-0`, `opacity-100` over 800ms or longer. Apply only to hero and feature deep-dives; reserve for moments that earn the runtime. Drop the blur portion under `prefers-reduced-motion: reduce`.

### Pattern: Staggered list orchestration
**Use when**: Lists, grids, bento cards entering the viewport.
**Anti-pattern**: All children mount instantly, or stagger feels glacial at 200ms per item.
**How**: Use `staggerChildren` or CSS cascade `animation-delay: calc(var(--index) * 100ms)`. Stagger at 30 to 50ms for short lists; 60 to 120ms for 4 to 6 sibling cards. The parent variants and children must reside in the same client component tree.

### Pattern: Modal open with spring physics
**Use when**: Modal dialogs, sheets, side drawers.
**Anti-pattern**: Modal snaps in instantly, or fades over 800ms with no spatial cue.
**How**: Modal scales from `scale-0.95` to `scale-1` with `opacity 0 → 1`. Spring physics: `{ type: "spring", stiffness: 100, damping: 20 }`. Sheet slides from below with similar spring. Scrim fades behind. Modal animates from its trigger source where possible (use `layoutId`).

### Pattern: Page transition (forward / back)
**Use when**: Native-feeling navigation between screens.
**Anti-pattern**: Random direction on every transition.
**How**: Forward navigation slides left (or up); backward navigation slides right (or down). Direction expresses hierarchy. Crossfade is acceptable for content replacement within the same container. Duration 250 to 350ms.

### Pattern: Shared element transition (layoutId)
**Use when**: An item morphs into a detail view, or a list item expands into a card.
**Anti-pattern**: New view appears with no relationship to the trigger.
**How**: Use motion library's `layoutId` to morph the element across state changes. The element scales and translates from its source position to its destination. The user reads the spatial connection.

### Pattern: Tab cross-fade
**Use when**: Tabbed feature carousels swapping a single visual slot.
**Anti-pattern**: Tab content disappears and reappears with a flash.
**How**: 200 to 300ms crossfade combined with a 16 to 24px slide. The crossfade is short enough to feel quick; the slide gives directional context.

### Pattern: Animated number counter
**Use when**: Hero stats, dashboard metrics that benefit from the count-up effect.
**Anti-pattern**: Counter that ticks endlessly, or that overshoots and settles.
**How**: Tick from 0 to target over 800 to 1500ms with `ease-out`. Triggers once on enter view, not on every scroll. Ends exactly on the target number with no settling jitter. Use sparingly — 2 to 3 counters max per section.

### Pattern: Infinite logo marquee
**Use when**: Customer logo strips that need to feel alive without forcing attention.
**Anti-pattern**: 4-second loop that grabs attention every time it cycles.
**How**: 20 to 60 second full cycle, seamless via `x: ["0%", "-100%"]`. Duplicate the row 2 to 3x in the DOM to mask the seam. Pause on hover so users can read the logo they are focused on. Sub-conscious speed — the eye does not snap to it.

### Pattern: Magnetic button physics
**Use when**: Hero CTAs or signature interactive buttons in high-end aesthetic.
**Anti-pattern**: Button jumps wildly toward the cursor or lags behind it.
**How**: Use `useMotionValue` and `useTransform` (never `useState`) to track cursor position. Button translates 4 to 8px maximum toward the cursor. Spring physics damp the motion. On press, scale down to `0.98` to simulate the click.

### Pattern: Cursor glow follow
**Use when**: Hero canvases or interactive surfaces in premium aesthetic.
**Anti-pattern**: Cursor glow visible on every component, draining attention.
**How**: A subtle radial glow tied to mouse position via `useMotionValue`. Brand-colored. Fades within 200ms when cursor stops. Restrict to the hero or one specific surface; never global page-wide.

### Pattern: Skeleton with shimmer
**Use when**: Operations longer than 300ms (data fetch, image load, content render).
**Anti-pattern**: Generic circular spinner blocking content for 3 seconds with no progress indication.
**How**: Skeletal block matching the eventual layout shape. Shimmer is a horizontal light gradient sliding across the block at 1.5 to 2s loops. Reduce to opacity-only pulsing under `prefers-reduced-motion: reduce`.

### Pattern: Perpetual ambient pulse
**Use when**: Live status indicators, "online now" dots, breathing badges.
**Anti-pattern**: Every interactive element pulsing constantly.
**How**: Soft scale or opacity breathing — `scale: [1, 1.1, 1]` over 2 to 3 second loops. Use sparingly: maximum 2 per viewport, only on truly live elements. Isolate in a memoized leaf client component so the page does not re-render with each frame.

### Pattern: Brutalist step-function reveal
**Use when**: Industrial, mechanical, terminal-adjacent aesthetics.
**Anti-pattern**: Smooth eased springs on a brutalist surface read as consumer-soft.
**How**: Use `steps(N)` easing to simulate CRT redraw or mechanical advancement. Instant snap states for hover and focus (zero milliseconds). Slot-machine numeric counters tick through digits with discrete clicks rather than smooth lerps. Optional CRT flicker as a low-opacity scanline drifting slowly down a fixed overlay.

### Pattern: Scrub-controlled video
**Use when**: Demonstration-heavy product surfaces.
**Anti-pattern**: Autoplay video looping forever in the hero with sound.
**How**: Video frame advances with scroll position. User controls the pace. Loops back when scrolled past. The user reads it as control rather than spectacle. Implementation via `IntersectionObserver` mapping scroll progress to video currentTime.

### Pattern: First-paint motion budget
**Use when**: Critical above-the-fold render.
**Anti-pattern**: Hero waits for a 3D scene to load before showing text.
**How**: Hero text appears almost instantly. Heavier interactive demo or 3D render fades in 200 to 400ms behind it. A low-fidelity geometric brand-colored placeholder loads for ~150ms before the full-detail asset crossfades in. Never make users wait for first meaningful paint.

### Pattern: Sticky scroll-pinned section
**Use when**: A single feature needs to support 3 to 6 visual states without 3 to 6 separate sections.
**Anti-pattern**: Six near-identical feature sections, each with the same product screenshot in different states.
**How**: Pin the visual on one side while a stack of content states scrolls past on the other. Each scroll trigger swaps the visual state. Couples narrative with motion without requiring autoplay. Implementation via `IntersectionObserver` with multiple thresholds. Disabled below 768px and under `prefers-reduced-motion`.

### Pattern: Sticky scroll stack (cards stack as user scrolls)
**Use when**: A series of feature cards needs to demonstrate progression.
**Anti-pattern**: Cards rendered flat, with no spatial story of progression.
**How**: Cards stick to the top and physically stack on top of each other from the bottom as the user scrolls down. Each card has its own `position: sticky` offset. The stack creates spatial depth — newer cards layer over older. Disable under reduced-motion and below 768px.

### Pattern: Variable-axis weight on hover
**Use when**: Premium high-end aesthetic with variable fonts.
**Anti-pattern**: Animating font weight on every label across the page.
**How**: Use sparingly — one or two elements per page. A label tightens from `font-variation-settings: 'wght' 400` to `wght 600` as the cursor approaches. Animate via `transform`-compatible setup; respect `prefers-reduced-motion`.

### Pattern: Scroll progress in nav, not in side rail
**Use when**: Long-form pages where progress feedback is valuable.
**Anti-pattern**: Fixed-position SVG drawing lines down the left or right edge as the user scrolls — known stale pattern that signals AI generation.
**How**: Integrate progress feedback into the navigation bar (horizontal top progress bar) or into section anchors (active state on nav links as sections enter view). Never as a parasitic edge element.

### Pattern: Crossfade for content replacement
**Use when**: Tabbed content swapping within the same container.
**Anti-pattern**: Snap-cut between tab states with no transition.
**How**: Crossfade `opacity 1 → 0 → 1` combined with a 16 to 24px directional slide. Total duration 200 to 300ms. The crossfade is short enough to feel quick; the slide gives directional context.

### Pattern: Continuity in page transitions
**Use when**: Native-feeling navigation between screens, especially mobile.
**Anti-pattern**: Random direction or jarring snap between routes.
**How**: Forward navigation slides left (LTR) or up (modal); backward slides right or down. Direction expresses hierarchy. Spatial continuity via shared element transitions where possible (use `layoutId`). Duration 250 to 350ms with spring physics.

## Tokens / values

### Duration ladder
- Tap feedback: 80 to 150ms
- Hover: 150 to 250ms
- Micro-interaction: 150 to 300ms
- Modal / sheet entry: 250 to 400ms
- Page transition: 250 to 350ms
- Scroll-triggered reveal: 300 to 500ms (quiet) or 400 to 600ms (premium)
- Premium cinematic entry: 700 to 900ms
- Number counter: 800 to 1500ms
- Stat ticker on enter: 800 to 1500ms with ease-out
- Logo marquee full loop: 20 to 60 seconds
- Ambient background motion: 4 to 8 second loops
- Brand mark on first load: 600 to 1200ms (skip on return visits)
- Exit duration: 60 to 70% of enter duration

### Easing curves
- Standard ease-out (entering): `cubic-bezier(0.16, 1, 0.3, 1)`
- Premium entry: `cubic-bezier(0.32, 0.72, 0, 1)`
- State change: `cubic-bezier(0.4, 0, 0.2, 1)`
- Snap (brutalist): `steps(N)` for N discrete frames
- Spring physics: `{ type: "spring", stiffness: 100, damping: 20 }`
- Avoid: `linear`, `ease-in-out` default, browser-default `ease`

### Transform values
- Tap feedback: `-translate-y-[1px]` or `scale-[0.98]`
- Hover lift: `-translate-y-[2px]` to `-translate-y-[4px]`
- Card hover scale: `scale-[1.02]` to `scale-[1.05]` inside `overflow-hidden`
- Scroll fade-up: `translateY(12px)` to `translateY(24px)`
- Cinematic entry: `translateY(64px)` + `blur(12px)` + `opacity-0`
- Magnetic button: 4 to 8px translate maximum toward cursor
- Cursor-tracked tilt: 4 to 8 degrees rotation maximum
- Press: `scale-[0.98]`
- Modal open scale: `scale-[0.95]` → `scale-1`

### Stagger timings
- Tight list (4 to 6 items): 30 to 50ms per item
- Medium list (6 to 12 items): 50 to 80ms per item
- Wide grid (12+ items): 60 to 120ms per item
- Headline word-by-word: 80 to 120ms per word cascade
- Never exceed 150ms stagger between siblings — feels theatrical

### Hover state values (cards and links)
- Background brighten: 2 to 4% L shift
- Underline weight: 1px → 2px
- Border opacity: 8 to 12% → 16 to 24% alpha
- Shadow expansion: small → medium
- Opacity reveal: 0.7 → 1
- Trailing icon translate: 4 to 6px right

### Perpetual motion archetypes
- **Pulse** — `scale: [1, 1.1, 1]` over 2 to 3s loop; for status indicators and live elements
- **Typewriter** — multi-step text cycling with blinking cursor; for command and search inputs
- **Float** — `translateY: [0, -6px, 0]` over 4 to 6s; for hero badges and decorative elements
- **Shimmer** — horizontal light gradient sliding across; for skeletal placeholders and active cards
- **Carousel** — `x: ["0%", "-100%"]` seamless infinite at 15 to 25s for data streams

### Performance constraints
- Animate only `transform` and `opacity`
- Apply `backdrop-blur` only to fixed or sticky elements
- Apply `will-change: transform` only to actively animating elements; remove after animation
- Memoize perpetual motion in isolated leaf client components
- Wrap GSAP and WebGL contexts in `useEffect` with cleanup
- Never mix GSAP with motion library in the same component tree
- Use `IntersectionObserver`, not `window.addEventListener('scroll')`
- Cap per-frame work under 16ms for 60fps; move heavy tasks to workers

### Reduced-motion fallbacks
- `prefers-reduced-motion: reduce`:
  - Skip `translateY` reveals; use opacity-only fades
  - Pause background mesh animations
  - Drop blur from scroll entries
  - Shorten durations by 30 to 50%
  - Skip scanline drift, glitch effects, slot-machine counters in brutalist contexts
  - Skip magnetic button physics; keep instant hover state

### Mobile motion intensity
- Reduce desktop intensity by 2 levels below 768px
- Skip perpetual ambient motion on cards below 768px
- Honor `prefers-reduced-motion` at all levels regardless of platform

### Banned motion patterns
- Side scroll progress paths (fixed-position SVG drawing lines down the viewport edge)
- Animating `width`, `height`, `top`, `left`
- `linear` easing on UI transitions
- Snapping state changes (instant 0ms with no transition) outside brutalist contexts
- Scroll-jacking that forces horizontal narrative
- Autoplay video with sound
- Hijacking pinch-zoom or scroll-wheel
- Decorative-only animation with no cause-effect
- `useState` for continuous animations (use `useMotionValue` and `useTransform`)
- Mixing GSAP with motion library in the same tree
- `window.addEventListener('scroll')` (use `IntersectionObserver`)
- Grain or noise filters on scrolling containers
- DeviceOrientation / DeviceMotion APIs for tilt or parallax (cursor-only via pointer events)
- Custom mouse cursors (accessibility hostile, performance hit)
- Looping animations on brand wordmark in nav (once on load, then static)
- Carousels under 4 seconds per slide
- Auto-rotating carousels with manual pagination dots
- Animation durations under 100ms or over 1500ms (other than ambient loops)

### Motion library defaults (when present)
- Spring physics: `stiffness: 100, damping: 20`
- Stagger children: `staggerChildren: 0.05` (50ms)
- Layout transitions: use `layout` and `layoutId` props for smooth re-ordering
- Variants: parent variants and children must reside in identical client component tree
- Wrap dynamic lists in `AnimatePresence` for exit animations

## Checklist (severity-tagged)

- [ ] Animations use `transform` and `opacity` only (severity: Critical)
- [ ] `prefers-reduced-motion: reduce` respected at every level (severity: Critical)
- [ ] User input (tap, scroll, gesture) cancels in-progress animation immediately (severity: High)
- [ ] Spring physics on interactive elements, not linear easing (severity: Medium)
- [ ] Micro-interactions sit in 150 to 300ms range (severity: High)
- [ ] Complex transitions cap at 400 to 500ms (severity: High)
- [ ] Exit duration is 60 to 70% of enter (severity: Medium)
- [ ] Staggered orchestration on list and grid mounts at 30 to 80ms per item (severity: Medium)
- [ ] `useEffect` animations have cleanup functions (severity: Critical)
- [ ] Perpetual motion isolated in memoized leaf client components (severity: High)
- [ ] No `window.addEventListener('scroll')` — `IntersectionObserver` used instead (severity: High)
- [ ] No `useState` for continuous animations — `useMotionValue` and `useTransform` used instead (severity: High)
- [ ] `backdrop-blur` applied only to fixed or sticky elements (severity: High)
- [ ] Grain or noise filters on fixed `pointer-events-none` pseudo-elements (severity: High)
- [ ] No GSAP mixed with motion library in the same component tree (severity: High)
- [ ] No side scroll progress paths (severity: High)
- [ ] No animating `width`, `height`, `top`, `left` (severity: Critical)
- [ ] No DeviceOrientation / DeviceMotion APIs for visual effects (severity: Critical)
- [ ] No custom mouse cursors (severity: High)
- [ ] No scroll-jacking that forces user direction (severity: High)
- [ ] No autoplay video with sound (severity: Critical)
- [ ] Skeletal loaders match layout sizes for operations >300ms (severity: High)
- [ ] Animated counters trigger once on enter, end exactly on target (severity: Medium)
- [ ] Logo marquees cycle at 20 to 60 seconds and pause on hover (severity: Cosmetic)
- [ ] Maximum 2 perpetual loops per viewport (severity: Medium)
- [ ] Mobile reduces motion intensity by 2 levels below 768px (severity: Medium)
- [ ] Layout transitions use `layoutId` for shared element morphs (severity: Medium)
- [ ] Cursor-tracked tilt capped at 4 to 8 degrees rotation (severity: Cosmetic)
- [ ] First-paint motion budget under 400ms — text appears before heavy assets (severity: High)
- [ ] Brand wordmark animations play once on load, not on loop (severity: Cosmetic)

## Related

- See **accessibility.md** for the `prefers-reduced-motion` contract and accommodations.
- See **interaction.md** for tap feedback timing and tactile press patterns.
- See **components.md** for state-by-state animation specs (hover, active, focus, loading).
- See **layout.md** for layout-shift avoidance during motion.
- See **typography.md** for variable-axis weight animations.
- See **dashboards.md** for breathing live indicators and number-counter rules.
