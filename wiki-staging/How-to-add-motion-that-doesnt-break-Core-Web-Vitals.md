# How to Add Motion That Doesn't Break Core Web Vitals

Motion can hurt or help SEO. Core Web Vitals (LCP, INP, CLS) are ranking signals; a poorly-implemented animation can tank all three. The `/ux-motion` command applies motion discipline — 150–300ms durations, transform+opacity only, spring physics, reduced-motion compliance — to ship animations that respect performance.

This page is the full motion contract. Read it before you add a single animation to a production surface.

---

## The 3 Core Web Vitals — what motion does to each

Google's Core Web Vitals are three measured metrics that feed into search ranking. Every one of them can be ruined by a careless animation.

### LCP — Largest Contentful Paint

LCP measures the time from navigation to the moment the largest above-the-fold element is painted. Target: under 2.5 seconds.

How motion ruins it:

- **Hero entrance animations on the LCP element.** If your hero image fades in over 800ms after JS hydrates, LCP measures the start of that fade, not the final state — but more importantly, the perceived time is the full 800ms. Users feel a slow page.
- **JS-driven layout on first paint.** Any animation that runs JS to position the LCP element before showing it pushes LCP into the JS-execution time, not the network-paint time.
- **Above-the-fold loops that retrigger paint.** A looping gradient sweep on the hero forces the GPU to keep compositing during the LCP measurement window.

Rule: the LCP element renders in its final position on first paint. Any motion on it is purely decorative, starts AFTER paint, and uses transform/opacity only.

### INP — Interaction to Next Paint

INP measures the latency between a user input (click, tap, keypress) and the next visible frame. Target: under 200ms.

How motion ruins it:

- **Heavy JS in the click handler.** If a button click triggers a 50ms animation setup, INP measures that 50ms.
- **Layout-thrashing animations.** Animating `width` or `height` triggers layout on every frame, blocking the main thread.
- **Synchronous DOM reads + writes.** Reading `offsetTop` before a transform triggers a forced sync layout. Cap that and INP recovers.

Rule: input-triggered motion uses `requestAnimationFrame` and only mutates `transform` and `opacity` — both compositor-only properties that do not block the main thread.

### CLS — Cumulative Layout Shift

CLS measures visual stability. Any element that moves during the page's lifetime without a user input is counted. Target: under 0.1.

How motion ruins it:

- **Skeleton-to-content transitions.** When the skeleton is replaced with real content of a different height, the next element shifts. CLS event.
- **Above-the-fold fades that reflow.** An image that fades from `display: none` to `display: block` creates a layout shift.
- **Sticky reveals on scroll without `transform`.** Animating `top` or `margin` triggers layout.

Rule: every animation reserves its space. Use `aspect-ratio`, fixed heights, or `min-height` on placeholders. Animate `transform`, never the box model.

---

## The motion discipline (durations, easing, the transform-only rule)

The discipline is six rules. Memorize them.

### Rule 1: Duration

- Micro interactions (hover, focus, button press): **100–150ms**
- Component transitions (panel open, tooltip show): **150–250ms**
- Page-level transitions (route change, modal open): **250–400ms**
- Hero or feature reveal (one per page max): **400–600ms**

Anything over 600ms feels broken on desktop and is rejected on mobile. Anything under 100ms is invisible and wasted.

### Rule 2: Easing

- Default: `cubic-bezier(0.4, 0, 0.2, 1)` (Material standard) — most things
- Enter (something appearing): `cubic-bezier(0, 0, 0.2, 1)` (decelerate)
- Exit (something disappearing): `cubic-bezier(0.4, 0, 1, 1)` (accelerate)
- Spring (anything dragged or thrown): a spring curve, not a bezier

Never `ease-in-out` for entrances — it makes things feel slow at the start. Never `linear` for anything organic — linear is for progress bars only.

### Rule 3: Transform + opacity only

The only properties that can be animated at 60fps reliably on the compositor are `transform` and `opacity`. Anything else triggers layout or paint on every frame.

### Rule 4: Reduced motion

Every animation respects `prefers-reduced-motion: reduce`. No exceptions. The reduced state is not "off" — it's "instant + opacity only, no movement."

### Rule 5: Stagger

Multiple items animating in sequence use a fixed stagger of 30–50ms per child. More than 50ms feels slow; less than 30ms reads as simultaneous.

### Rule 6: Origin

Motion has direction. An element appearing slides FROM the direction that explains its source. A dropdown slides down from its trigger. A toast slides in from the edge it lives on. Floating elements that "appear from nowhere" feel cheap.

---

## Banned animations (the box-model list)

Never animate these. They trigger layout on every frame and tank INP.

- `width`
- `height`
- `top`
- `left`
- `right`
- `bottom`
- `margin` (any side)
- `padding` (any side)
- `border-width`
- `font-size`

If you find yourself wanting to animate `height`, you actually want `transform: scaleY()` or `max-height` toggling with a duration (which is allowed but jumpy — prefer the scale).

Common AI-generated motion mistakes that hit this list:

```css
/* WRONG */
.menu {
  transition: height 300ms ease;
}
.menu.open {
  height: auto;
}

/* RIGHT */
.menu {
  transform: scaleY(0);
  transform-origin: top;
  opacity: 0;
  transition: transform 200ms cubic-bezier(0, 0, 0.2, 1), opacity 150ms ease;
}
.menu.open {
  transform: scaleY(1);
  opacity: 1;
}
```

---

## Approved animations (transform + opacity)

These are safe at 60fps because they are composited.

### Transform: translate

```css
.toast-enter {
  transform: translateY(100%);
  opacity: 0;
}
.toast-enter-active {
  transform: translateY(0);
  opacity: 1;
  transition: transform 250ms cubic-bezier(0, 0, 0.2, 1),
              opacity 200ms ease-out;
}
```

### Transform: scale

```css
.modal-enter {
  transform: scale(0.96);
  opacity: 0;
}
.modal-enter-active {
  transform: scale(1);
  opacity: 1;
  transition: transform 200ms cubic-bezier(0, 0, 0.2, 1),
              opacity 150ms ease-out;
}
```

### Transform: rotate

```css
.chevron {
  transform: rotate(0deg);
  transition: transform 150ms ease;
}
.chevron.open {
  transform: rotate(180deg);
}
```

### Opacity alone

```css
.fade {
  opacity: 0;
  transition: opacity 200ms ease;
}
.fade.in {
  opacity: 1;
}
```

These four primitives compose every interaction in a well-designed product.

---

## Spring physics vs cubic-bezier

Use bezier for predictable transitions: route changes, panel opens, tooltips. Use springs for anything that is dragged, thrown, or behaves like a physical object: drawer pulls, swipe-to-dismiss, magnetic hovers, scroll-coupled motion.

A bezier curve has a fixed duration. A spring is duration-less — it resolves when the physics says it's done, which makes it feel alive.

In Framer Motion:

```jsx
// Bezier — predictable, finite
<motion.div
  animate={{ x: 100 }}
  transition={{ duration: 0.25, ease: [0, 0, 0.2, 1] }}
/>

// Spring — physical, feels organic
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 400, damping: 30, mass: 1 }}
/>
```

Spring tuning:

- **Snappy UI (close to bezier, but with bounce):** stiffness 400, damping 30, mass 1
- **Friendly drawer / panel:** stiffness 260, damping 26, mass 1
- **Heavy / weighted feel (rare):** stiffness 150, damping 20, mass 1.2
- **Bouncy alert / celebration (use very rarely):** stiffness 300, damping 15, mass 1

Never use a spring on more than 3 things in a single viewport. Springs are expensive perceptually — they demand attention.

---

## Stagger rules (30–50ms per child)

Staggering a list of items in is one of the highest-leverage motion patterns. Done right, it feels intentional. Done wrong, it feels slow.

Rules:

1. Stagger is **30–50ms** per child. 40ms is the sweet spot.
2. Stagger only the first 8–12 children. After that, the rest enter without stagger to avoid making the page feel laggy.
3. Use stagger only on entrance. Never on exit (exits feel slow when staggered).
4. Stagger only on the first render or on a meaningful state change. Not on every re-render.

Framer Motion example:

```jsx
const list = {
  visible: {
    transition: { staggerChildren: 0.04, staggerDirection: 1 }
  }
};

const item = {
  hidden: { opacity: 0, y: 8 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.25, ease: [0, 0, 0.2, 1] }
  }
};

return (
  <motion.ul variants={list} initial="hidden" animate="visible">
    {items.map(i => <motion.li key={i.id} variants={item}>{i.text}</motion.li>)}
  </motion.ul>
);
```

CSS-only stagger using `animation-delay`:

```css
.list-item {
  opacity: 0;
  transform: translateY(8px);
  animation: enter 250ms cubic-bezier(0, 0, 0.2, 1) forwards;
}
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 40ms; }
.list-item:nth-child(3) { animation-delay: 80ms; }
.list-item:nth-child(4) { animation-delay: 120ms; }
.list-item:nth-child(5) { animation-delay: 160ms; }
.list-item:nth-child(6) { animation-delay: 200ms; }
.list-item:nth-child(n+7) { animation-delay: 240ms; }

@keyframes enter {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Note the clamp on `n+7` — every later item shares the same delay, so the total time does not balloon.

---

## The reduced-motion preference

`prefers-reduced-motion: reduce` is set by users with vestibular disorders, motion sensitivity, or simply a preference for less movement. Respecting it is an accessibility requirement, not optional.

The wrong implementation: setting all animations to `animation: none`. This breaks fade-ins and removes the affordance entirely.

The right implementation: keep opacity transitions, remove movement.

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Or, granular per-component:

```css
.item {
  transform: translateY(20px);
  opacity: 0;
  transition: transform 250ms ease, opacity 250ms ease;
}

@media (prefers-reduced-motion: reduce) {
  .item {
    transform: none;
    transition: opacity 250ms ease;
  }
}
```

Framer Motion has `useReducedMotion`:

```jsx
import { useReducedMotion, motion } from "framer-motion";

function Card() {
  const shouldReduce = useReducedMotion();
  return (
    <motion.div
      initial={{ y: shouldReduce ? 0 : 20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
    />
  );
}
```

Test it. macOS: System Settings → Accessibility → Display → "Reduce motion." Chrome DevTools: Rendering pane → "Emulate CSS media feature prefers-reduced-motion."

---

## Run `/ux-motion` to audit existing motion

If you have an existing surface with motion, run:

```
/ux-motion --audit ./resources/views/landing.blade.php
```

The audit reports:

- Every animation property used (with a violation flag for banned ones)
- Every duration (with a flag for under 100ms or over 600ms)
- Every easing (with a flag for `linear` or `ease-in-out` on entrances)
- Missing `prefers-reduced-motion` handlers
- Layout-shifting animations (CLS risk)
- Compositor-blocking properties (INP risk)
- LCP-blocking animations on above-the-fold elements

Sample output:

```
MOTION AUDIT — landing.blade.php
================================

CRITICAL (3)
  L48  height transition (200ms) — banned property. Triggers layout.
  L72  width transition (300ms) — banned property. Triggers layout.
  L94  Hero image fade-in (800ms) — LCP risk. Element is largest above fold.

HIGH (5)
  L31  No prefers-reduced-motion handler on .hero-enter
  L31  No prefers-reduced-motion handler on .nav-slide
  L66  duration 800ms on a hover — too long for micro-interaction
  L102 ease-in-out on .toast-enter — should be cubic-bezier(0, 0, 0.2, 1)
  L118 staggerChildren 0.12s — should be 0.03–0.05s

MEDIUM (2)
  L55  scroll-behavior smooth — verify it does not break anchor navigation in iOS
  L142 No exit animation defined — abrupt removal

Pass rate: 12 / 22 animations clean
```

---

## `/ux-motion --fix` to apply corrections

The fix mode rewrites the violations. It preserves your authored animations where they pass discipline; it patches the rest.

```
/ux-motion --fix ./resources/views/landing.blade.php
```

What it changes:

- Banned properties get rewritten to transform equivalents
- Over-long durations get clamped to the right tier
- Easing gets corrected per direction (enter / exit)
- A `prefers-reduced-motion` block is added at the top of the file's `<style>` block (or in the linked stylesheet)
- LCP-blocking animations get either removed or rescheduled to start after first paint

It does not change motion intent — only its implementation. If a fade is meant to be a fade, it stays a fade; the duration and easing get fixed.

After the fix, re-run the audit. Pass rate should be 100%.

---

## The 5 dashboard motion archetypes (perpetual but performant)

Dashboards have specific motion needs because they run for hours. The motion has to live in the screen without becoming visual noise.

### 1. The live pulse

Used by live status indicators. A slow opacity pulse, 2 per viewport maximum.

```css
@keyframes live-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}
.live-dot {
  animation: live-pulse 2s ease-in-out infinite;
  will-change: opacity, transform;
}
```

### 2. The sparkline draw

When new data arrives, the sparkline extends with a 150ms transform. The path itself is drawn once; the visible portion grows via a clip-path or stroke-dashoffset.

```css
@keyframes sparkline-grow {
  from { stroke-dashoffset: 1000; }
  to { stroke-dashoffset: 0; }
}
.sparkline path {
  stroke-dasharray: 1000;
  animation: sparkline-grow 400ms cubic-bezier(0, 0, 0.2, 1) forwards;
}
```

### 3. The metric counter

Numbers count up to their final value on first paint. 600ms maximum, eased out.

```jsx
import { motion, useMotionValue, useTransform, animate } from "framer-motion";

function Metric({ value }) {
  const count = useMotionValue(0);
  const rounded = useTransform(count, latest => Math.round(latest));
  useEffect(() => {
    const controls = animate(count, value, { duration: 0.6, ease: [0, 0, 0.2, 1] });
    return controls.stop;
  }, [value]);
  return <motion.span>{rounded}</motion.span>;
}
```

### 4. The row highlight

When a row updates in real time, a 600ms background flash signals the change.

```css
@keyframes row-flash {
  0% { background-color: var(--accent-soft); }
  100% { background-color: transparent; }
}
.row[data-updated] {
  animation: row-flash 600ms ease-out;
}
```

### 5. The bento entry

On first paint, bento cells stagger in over 200ms with a 30ms stagger.

Already covered in the stagger section. Use it.

---

## Magnetic micro-physics (useMotionValue, not useState)

Magnetic hovers — where an element drifts toward the cursor — are a high-leverage detail when used sparingly. The wrong way is `useState` + re-render on every mousemove. The right way is `useMotionValue` and direct GPU compositing.

```jsx
import { useRef } from "react";
import { motion, useMotionValue, useSpring, useTransform } from "framer-motion";

function MagneticButton({ children }) {
  const ref = useRef(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const springX = useSpring(x, { stiffness: 300, damping: 25 });
  const springY = useSpring(y, { stiffness: 300, damping: 25 });

  const handleMove = (e) => {
    const rect = ref.current.getBoundingClientRect();
    const cx = rect.left + rect.width / 2;
    const cy = rect.top + rect.height / 2;
    x.set((e.clientX - cx) * 0.3);
    y.set((e.clientY - cy) * 0.3);
  };

  const handleLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      ref={ref}
      onMouseMove={handleMove}
      onMouseLeave={handleLeave}
      style={{ x: springX, y: springY }}
    >
      {children}
    </motion.button>
  );
}
```

Why this is fast: `useMotionValue` writes directly to the DOM's transform property without triggering a React re-render. The spring lives on the compositor.

Why this is restrained: the multiplier is 0.3, not 1.0. The element drifts a fraction of the cursor distance. Anything more reads as gimmicky.

Cap magnetic effects at 1–2 per screen. The hero CTA. Maybe a feature card. Never every button.

---

## Performance reminders

### Memoize the components that animate

A component that animates and also re-renders on parent state is double-paying. Wrap it in `React.memo` if the props are stable.

### Isolate animations with `will-change`

`will-change: transform` tells the browser to promote the element to its own compositor layer. Use sparingly — too many layers hurt memory.

```css
.animated {
  will-change: transform, opacity;
}
```

Only apply `will-change` while the animation is active or imminent. Setting it on every element is worse than not setting it at all.

### Use `AnimatePresence` for exit animations

In Framer Motion, an element removed from the DOM cannot animate out unless `AnimatePresence` wraps it.

```jsx
<AnimatePresence>
  {open && (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.96 }}
      transition={{ duration: 0.2, ease: [0, 0, 0.2, 1] }}
    />
  )}
</AnimatePresence>
```

### Avoid layout-thrashing patterns

```jsx
// WRONG — synchronous read + write in a loop
items.forEach(el => {
  const top = el.offsetTop;       // read (forces layout)
  el.style.transform = `translateY(${top}px)`; // write
});

// RIGHT — read all, then write all
const tops = items.map(el => el.offsetTop);    // reads
items.forEach((el, i) => {
  el.style.transform = `translateY(${tops[i]}px)`; // writes
});
```

### Profile with the Performance panel

In Chrome DevTools:

1. Open the Performance tab
2. Click Record
3. Trigger your animation
4. Stop the recording
5. Look for long tasks (red triangles), forced reflows (purple), and layer counts

Anything over 16ms per frame drops below 60fps. Anything over 50ms is jank.

### Lighthouse + Web Vitals extension

Run Lighthouse on the surface. INP and CLS report inline. If either is in the red, the audit will tell you which animation caused it.

---

## Real example

A landing-page hero with restrained motion:

```jsx
"use client";

import { motion, useReducedMotion } from "framer-motion";

const fadeUp = (shouldReduce) => ({
  hidden: { opacity: 0, y: shouldReduce ? 0 : 16 },
  visible: { opacity: 1, y: 0 }
});

const list = {
  visible: { transition: { staggerChildren: 0.04 } }
};

export default function Hero() {
  const shouldReduce = useReducedMotion();
  const variant = fadeUp(shouldReduce);

  return (
    <motion.section
      className="hero"
      initial="hidden"
      animate="visible"
      variants={list}
    >
      <motion.h1 variants={variant} transition={{ duration: 0.4, ease: [0, 0, 0.2, 1] }}>
        Beyond likes. Beyond clicks.
      </motion.h1>
      <motion.p variants={variant} transition={{ duration: 0.4, ease: [0, 0, 0.2, 1] }}>
        The internet of what people actually do.
      </motion.p>
      <motion.div variants={variant} transition={{ duration: 0.4, ease: [0, 0, 0.2, 1] }}>
        <a href="/start" className="cta">Start</a>
      </motion.div>
    </motion.section>
  );
}
```

What this gets right:

- LCP element (`<h1>`) renders in its final position; the y-offset of 16px is small enough not to delay perceived paint
- Total animation duration: 0.4s + (3 children × 0.04s stagger) = ~520ms
- Reduced motion: opacity only, no translate
- Easing: decelerate (entrance)
- No banned properties
- No layout shift (h1 has reserved space)

What it would get wrong if you let the model default:

- 800ms duration with `ease-in-out`
- Translate of 80px (large enough to feel slow)
- Stagger of 0.15s per child
- No reduced-motion handling
- `width` or `scale` on the hero card causing CLS

---

## Next steps

- Run [`/ux-polish`](How-to-detect-AI-slop-in-your-design) to detect decorative motion that adds no information
- For dashboards specifically, see [How to design a dashboard with Claude Code](How-to-design-a-dashboard-with-Claude-Code)
- For the full pipeline from AI default to human-grade, see [How to make AI output look human-grade](How-to-make-AI-output-look-human-grade)

---

**Plugin repo:** https://github.com/Laith0003/ux-skill
**Author:** Laith Aljunaidy — https://www.linkedin.com/in/laith-aljunaidy/
**License:** MIT
