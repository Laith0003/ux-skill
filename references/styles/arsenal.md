# Creative arsenal — the high-end pattern library

> The opposite of `anti-slop.md`. This is what to REACH for, not what to avoid. Patterns drawn from `design-taste-frontend` and the awwwards-grade frontend bar. Each pattern: when to use, what it costs, how to ship it without breaking 60fps.

## How to use this file

Don't ship everything. The arsenal is a menu — pick **2 to 4 patterns per design** and execute them well. More than 4 and the design becomes a showcase instead of a product.

The calling command (`/ux-design`) picks the patterns based on:
- The user's brief
- The `MOTION_INTENSITY` dial
- The `DESIGN_VARIANCE` dial
- The product type (landing, dashboard, component)

---

## Hero & landing patterns

### Asymmetric split hero
**Use when**: marketing pages, product landings, premium positioning.
**What it is**: Text aligned left (or right), media asset on the opposite side, no centering. Background fades subtly into the page background (lighter on light mode, darker on dark mode).
**Why it works**: Defeats the "centered hero over dark image" AI default.
**Cost**: zero — pure layout.

### Bento grid
**Use when**: feature sections, SaaS landings, dashboards, product overviews.
**What it is**: Asymmetric tile grouping like Apple Control Center. Different tile sizes; uses `grid-flow-dense` for tight packing. Each tile has its own micro-interaction.
**Why it works**: Implies depth + density without overwhelming. Lets each tile carry its own story.
**Cost**: design effort medium, code low (CSS Grid).
**Combine with**: Perpetual micro-interactions per tile.

### Masonry layout
**Use when**: galleries, portfolios, content-heavy pages.
**What it is**: Staggered grid with no fixed row heights (Pinterest-style).
**Cost**: low — use CSS columns or a masonry lib.

### Curtain reveal
**Use when**: brand statement at top of hero, theatrical entry.
**What it is**: Hero section that splits in the middle on scroll, revealing what's behind.
**Cost**: GSAP ScrollTrigger needed.

---

## Navigation patterns

### Mac OS dock magnification
**What it is**: Icons in the nav scale fluidly on hover, ripple-style.
**Cost**: low — CSS scale on hover with cubic-bezier easing.

### Dynamic Island
**What it is**: Pill-shaped UI component that morphs to show status/alerts (iOS-inspired).
**Cost**: medium — needs layout animation (`layout` + `layoutId` in Framer).

### Magnetic button
**What it is**: Buttons that physically pull toward the cursor.
**Cost**: medium — must use `useMotionValue` (NEVER `useState`).

### Mega menu reveal
**What it is**: Full-screen dropdown that stagger-fades complex content.
**Cost**: medium — Framer Motion `staggerChildren`.

### Floating speed dial
**What it is**: FAB that springs out into a curved line of secondary actions.
**Cost**: medium — spring physics + path math.

---

## Layout & grid patterns

### Split-screen scroll
**Use when**: storytelling, dual-narrative content.
**What it is**: Two halves slide in opposite directions on scroll.
**Cost**: GSAP, careful performance.

### Chroma grid
**Use when**: gallery surfaces, brand pages.
**What it is**: Grid borders or tiles with subtle continuously-animating color gradients.
**Cost**: low — CSS conic-gradient animation.

### Sticky scroll stack
**Use when**: storytelling, step-by-step product walkthrough.
**What it is**: Cards that stick to the top and physically stack over each other as you scroll.
**Cost**: medium — GSAP ScrollTrigger pinning.

---

## Card patterns

### Parallax tilt card
**What it is**: 3D-tilting card that tracks mouse position.
**Cost**: low — `useMotionValue` for x/y, transform with perspective.

### Spotlight border card
**What it is**: Card border illuminates dynamically under the cursor.
**Cost**: low — CSS radial gradient on a pseudo-element, mouse position tracked.

### Holographic foil card
**What it is**: Iridescent rainbow reflections shifting on hover (Pokémon card vibe).
**Cost**: medium — conic-gradient + mix-blend-mode.

### Tinder swipe stack
**Use when**: card-based decision UIs, onboarding flows.
**What it is**: Physical stack of cards user can swipe away.
**Cost**: medium — Framer Motion drag gestures + threshold detection.

### Morphing modal
**What it is**: Button that seamlessly expands into its own full-screen dialog container.
**Cost**: medium — Framer `layoutId` for shared element.

### Liquid glass panel
**What it is**: True frosted glass with inner refraction borders — `backdrop-blur` + 1px inner border + inner shadow.
**Cost**: low — pure CSS. Don't overuse; it's a moment, not a system.

---

## Scroll animation patterns

### Horizontal scroll hijack
**What it is**: Vertical scroll translates into smooth horizontal gallery pan.
**Cost**: high — GSAP ScrollTrigger pinning + horizontal translate.

### Locomotive scroll sequence
**What it is**: Video/3D sequence where framerate ties to scrollbar position.
**Cost**: very high — preloaded image sequence or canvas.

### Zoom parallax
**What it is**: Central background image zooming in/out seamlessly as user scrolls.
**Cost**: medium — GSAP + transform.

### Scroll progress path
**What it is**: SVG vector lines that draw themselves as user scrolls.
**Cost**: medium — `stroke-dasharray` + `stroke-dashoffset` tied to scroll.

### Liquid swipe transition
**What it is**: Page transitions that wipe like viscous liquid.
**Cost**: high — SVG path morphing.

---

## Typography patterns

### Kinetic marquee
**What it is**: Endless text bands reversing direction or speeding up on scroll.
**Cost**: low — CSS keyframes + scroll-triggered speed multiplier.

### Text mask reveal
**What it is**: Massive typography acting as a transparent window to a video background.
**Cost**: low — `background-clip: text` + a `<video>` behind.

### Text scramble effect
**What it is**: Matrix-style character decoding on load or hover.
**Cost**: low — JS interval cycling random chars then settling.

### Circular text path
**What it is**: Text curved along a spinning circular path.
**Cost**: low — SVG `<textPath>` + CSS rotate animation.

### Gradient stroke animation
**What it is**: Outlined text with a gradient continuously running along the stroke.
**Cost**: low — `-webkit-text-stroke` + `background-clip: text` + animation.

---

## Micro-interactions

### Particle explosion button
**What it is**: CTA that shatters into particles on success.
**Cost**: medium — canvas or many small absolute-positioned elements.

### Skeleton shimmer
**What it is**: Shifting light reflection moving across placeholder boxes during load.
**Cost**: low — CSS keyframe animating a linear-gradient position.

### Directional hover-aware button
**What it is**: Hover fill enters from the exact side the mouse entered from.
**Cost**: low — JS detects entry direction, CSS variable drives fill direction.

### Ripple click effect
**What it is**: Visual waves rippling from click coordinates (Material Design).
**Cost**: low — absolute-positioned span on click, scale + fade.

### Animated SVG line drawing
**What it is**: Vectors drawing their own contours in real-time.
**Cost**: low — `stroke-dasharray` trick.

### Mesh gradient background
**What it is**: Organic lava-lamp-like animated color blobs.
**Cost**: medium — large blurred radial gradients, CSS animations driving position.

---

## Dashboard-specific patterns

### Intelligent list
Vertical stack of items with infinite auto-sorting loop. Items swap positions using `layoutId`, simulating AI prioritizing tasks in real-time. Use for "this is a smart product" surfaces.

### Command input
Search/AI bar with multi-step typewriter effect cycling through complex prompts, blinking cursor, shimmering "processing" state. Hero placement on AI products.

### Live status with overshoot badge
Scheduling interface with "breathing" status indicators + a pop-up notification badge that emerges with an overshoot spring effect, stays 3 seconds, vanishes.

### Wide data stream
Horizontal "infinite carousel" of data cards or metrics. Seamless loop using `x: ["0%", "-100%"]`. Used for live data displays.

### Contextual focus mode
Document view that animates staggered highlight on a text block, followed by a "float-in" of a floating action toolbar with micro-icons.

---

## Combinations that work

| Brief | Patterns |
|---|---|
| Modern SaaS landing | Asymmetric split hero + bento grid + spotlight border cards + perpetual micro-interactions |
| AI product landing | Asymmetric hero + command input + live status + magnetic button + mesh gradient bg |
| Portfolio | Masonry + parallax tilt cards + horizontal scroll hijack on featured |
| Editorial / brand | Curtain reveal + kinetic marquee + text mask reveal + circular text path |
| Dashboard | Bento + intelligent list + wide data stream + contextual focus mode |
| Mobile app landing | Dynamic island nav + dock magnification CTA + parallax tilt feature card |

---

## Hard combinations to avoid

| Don't combine | Why |
|---|---|
| GSAP + Framer Motion in same component tree | Conflicts in animation control |
| 3+ scroll-triggered effects on the same page | Performance collapse |
| Magnetic button + parallax tilt + spotlight border on the SAME card | Visual noise; the moment dies |
| Every section with perpetual motion | Eye-fatigue; user can't focus on content |

---

## Performance reminders

- Any perpetual animation → memoize + isolate in its own micro-Client-Component
- Never trigger re-renders in the parent layout from a child animation
- Wrap dynamic lists in `<AnimatePresence>`
- Lazy-load below-the-fold pattern code
- Apply grain/noise filters only to `fixed pointer-events-none` pseudo-elements, never to scrolling containers
- Always memo (`React.memo`) components with continuous motion

## Sources

- `design-taste-frontend` SKILL — Section 8 "THE CREATIVE ARSENAL", Section 9 "THE MOTION-ENGINE BENTO PARADIGM"
- `gpt-taste` SKILL — component arsenal references
- awwwards.com — patterns that consistently win SOTD
