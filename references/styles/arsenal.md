# Creative arsenal — the high-end pattern library

The opposite of anti-slop. This is what to reach for, not what to avoid. Each pattern: when to use, what it costs, how to ship it without breaking 60fps. The arsenal is a menu — pick 2 to 4 patterns per design and execute them well. More than 4 and the design becomes a showcase instead of a product.

The calling command picks patterns based on:
- The user's brief
- The MOTION_INTENSITY dial
- The DESIGN_VARIANCE dial
- The product type (landing, dashboard, component)
- The committed style system (industrial, minimalist, high-end)

Patterns below are organized by purpose. Skim by section to find what fits the moment. Cost notes indicate implementation effort; performance notes indicate where these patterns break if applied carelessly.

---

## Hero & landing patterns

### Asymmetric split hero
**Use when**: marketing pages, product landings, premium positioning.
**What it is**: Text aligned left or right, media asset on the opposite side, no centering. Background fades subtly into the page background (lighter on light mode, darker on dark mode). The split is intentionally uneven — 7/5 or 5/7 columns, not 6/6.
**Why it works**: Defeats the "centered hero over dark image" default. The asymmetry creates hierarchy without typography variance.
**Cost**: zero — pure layout.

### Editorial column rhythm
**Use when**: longform marketing surfaces, story-led product pages.
**What it is**: Sections alternate text-left/image-right, then text-right/image-left, then occasionally full-bleed. Each section reads as a magazine spread. The grid is felt but not enforced; cards inside sections are deliberately not all identical.
**Why it works**: Creates visual zigzag with zero decorative cost. The alternation is the rhythm.
**Cost**: zero — pure layout discipline.

### Bento grid
**Use when**: feature sections, SaaS landings, dashboards, product overviews.
**What it is**: Asymmetric tile grouping. Different tile sizes; uses `grid-flow-dense` for tight packing. Each tile has its own micro-interaction. Tile size carries hierarchy instead of headline weight; larger tiles carry marquee features, smaller tiles carry supporting capabilities.
**Why it works**: Implies depth + density without overwhelming. Lets each tile carry its own story.
**Cost**: design effort medium, code low (CSS Grid).
**Combine with**: perpetual micro-interactions per tile; the 5 card archetypes for dashboards.

### Masonry layout
**Use when**: galleries, portfolios, content-heavy pages.
**What it is**: Staggered grid with no fixed row heights.
**Cost**: low — use CSS columns or a masonry library.

### Curtain reveal
**Use when**: brand statement at top of hero, theatrical entry, big-moment marketing.
**What it is**: Hero section that splits in the middle on scroll, revealing what's behind.
**Cost**: scroll-trigger library needed.

### Cinematic center hero
**Use when**: marketing surfaces where a single statement carries the entire value proposition.
**What it is**: Text perfectly centered, massive width, ultra-wide H1 container (`max-w-5xl` or wider). Exactly two high-contrast CTAs below. Behind everything, a stunning full-bleed background image with a dark radial wash. Buttons perfectly legible — dark background gets white text, light background gets dark text.
**Why it works**: When centered is the intentional choice (not the default), it functions as a declaration of confidence.
**Cost**: low — careful contrast tuning, image processing.

### Artistic asymmetry hero
**Use when**: brand-forward marketing, creative-tool landings.
**What it is**: Text offset to the left. An artistic floating image overlapping the text from the bottom right. Generous negative space.
**Cost**: low — layout + image z-stacking.

### Editorial split hero
**Use when**: premium SaaS, content-led products.
**What it is**: Text left, image right, but with massive negative space between. The split is not 50/50 — it's 60/40 or 65/35 with breathing room.
**Cost**: zero — layout discipline.

### Asymmetric hero with stylistic fade
**Use when**: brand-driven launch pages, premium consumer products.
**What it is**: High-quality relevant background image with a subtle stylistic fade (darkening or lightening into the page background depending on light or dark mode). Text aligned cleanly left or right.
**Cost**: low — image processing + CSS gradient mask.

### Email-capture hero
**Use when**: fintech, signup-led products where the implied promise is "this is one field, not a multi-step funnel."
**What it is**: A single email input + a single button as the hero's primary CTA, replacing a "Sign Up" button. The hero copy implies the field IS the start.
**Cost**: low — form + state.

### Thesis-statement hero
**Use when**: editorial / AI / research-positioning products where the brand voice is "we have something to say."
**What it is**: Large centered display headline (single line if possible), 2-4 sentences of body-size prose under it, single CTA with at most one secondary link. No multi-button toolbar.
**Why it works**: The cliff between display scale and body scale is the design. Confidence reads as willingness to use full sentences in the subhead.
**Cost**: zero — typographic discipline.

### AIDA section flow (mandatory framing for landings)
- **Attention (Hero)** — cinematic, clean, wide layout. One claim, one supporting line, one primary CTA + one secondary.
- **Interest (Features / Bento)** — high-density, mathematically intentional grid or interactive components.
- **Desire (Motion / Media)** — pinned sections, horizontal scroll, scroll-driven reveals, customer outcomes.
- **Action (Footer / Pricing)** — massive high-contrast CTA, clean footer.

---

## Navigation patterns

### Floating glass pill nav
**Use when**: high-end maximalist styles, premium product marketing.
**What it is**: Liquid glass treatment on a centered floating pill at the top, detached from the viewport edge with substantial margin above. On scroll past hero, backdrop blur intensifies but the pill never glues to the edge.
**Cost**: low — CSS backdrop-filter + position fixed.

### Minimal split nav
**Use when**: minimalist styles, content-led SaaS.
**What it is**: Logo left, primary actions right, single accent on the active item. Thin horizontal rail, no background fill, sits on canvas. Optionally a subtle backdrop blur appears after first scroll.
**Cost**: zero — pure layout.

### Dock-style magnification nav
**Use when**: creative tools, design-forward portfolios.
**What it is**: Navbar at the edge with icons that scale fluidly on hover; neighbors grow proportionally less.
**Cost**: low — CSS scale + cubic-bezier easing.

### Morphing status pill
**Use when**: products with live data, status surfaces, in-app notifications.
**What it is**: Pill-shaped UI component that morphs to show status / alerts. Pop-up notification badge that emerges with overshoot spring, stays 3 seconds, vanishes.
**Cost**: medium — needs layout animation (`layout` + `layoutId` in motion library).

### Magnetic button
**Use when**: high-end maximalist styles, hero CTAs that need cinematic feedback.
**What it is**: Buttons that physically pull toward the cursor as it approaches.
**Cost**: medium — must use `useMotionValue` / `useTransform`. Never `useState` for continuous tracking.

### Button-in-button (the trailing icon bezel)
**Use when**: high-end CTAs with directional icons.
**What it is**: Primary CTA with a trailing arrow that lives inside its own circular wrapper, flush with the parent button's right inner padding. The wrapper has its own background and ring distinct from the parent. On hover, the nested icon translates diagonally (1px up, 1px right) and scales slightly (1.05).
**Why it works**: Naked arrows next to text are a generator default; the bezel reads as machined hardware.
**Cost**: low — nested elements + hover transform.

### Mega menu reveal
**Use when**: content-heavy nav, products with many sub-categories.
**What it is**: Full-screen dropdown that stagger-fades complex content. Multi-column layout grouped by job-to-be-done, not by alphabetical product name. Often includes preview thumbnails, feature highlights, and a "what's new" callout — treated as a micro-page.
**Cost**: medium — `staggerChildren` orchestration.

### Floating speed dial
**Use when**: mobile-first surfaces, action-heavy dashboards.
**What it is**: FAB that springs out into a curved line of secondary actions.
**Cost**: medium — spring physics + path math.

### Contextual radial menu
**Use when**: editing surfaces, creative tools.
**What it is**: Circular menu expanding exactly at the click coordinates.
**Cost**: medium — pointer coords + radial layout.

### Status indicator in nav
**Use when**: infrastructure products, developer tools, fintech.
**What it is**: A 6px green dot + 12px caps text saying "All systems operational" in the nav or footer. Links to a status page.
**Why it works**: Sells reliability without saying "reliable."
**Cost**: zero — tiny but powerful trust signal.

### "What's new" badge in nav
**Use when**: products with active development cadence.
**What it is**: A top-nav item ("What's new" or "Changelog") with a small dot or badge for recency. Signals active development to engineers; gives returning visitors a destination.
**Cost**: zero.

---

## Layout & grid patterns

### Split-screen scroll
**Use when**: storytelling, dual-narrative content.
**What it is**: Two screen halves sliding in opposite directions on scroll.
**Cost**: scroll-trigger library, careful performance.

### Chroma grid
**Use when**: gallery surfaces, brand pages.
**What it is**: Grid borders or tiles with subtle continuously-animating color gradients.
**Cost**: low — CSS conic-gradient animation.

### Sticky scroll stack
**Use when**: storytelling, step-by-step product walkthrough.
**What it is**: Cards that stick to the top and physically stack over each other as you scroll downward.
**Cost**: medium — scroll-trigger library + pinning.

### Mosaic / asymmetric two-column
**Use when**: feature sections, capability deep-dives.
**What it is**: 7/5 or 5/7 split that alternates side section to section. Produces visual zigzag with zero decorative cost. Where a section has text + visual, the visual gets 7-8 columns and the text gets 4-5, not 6/6. The visual is the proof; the text is the caption.
**Cost**: zero — pure layout.

### Broken-grid layout
**Use when**: editorial brand surfaces, magazine-style product pages.
**What it is**: Strict grid backbone, but elements deliberately bleed past column boundaries. Some cards span more columns and rows than others. Fractional grid columns (`grid-template-columns: 2fr 1fr 1fr`).
**Cost**: low — CSS grid with intentional breaks.

### Z-axis cascade
**Use when**: high-end maximalist styles, hardware showcases.
**What it is**: Elements stack like physical cards, slightly overlapping with varying depths. Some cards carry a subtle -2° or 3° rotation to break the digital grid. Mobile collapse: remove all rotations and negative-margin overlaps; stack vertically.
**Cost**: low — CSS transform + z-index.

### Editorial split section
**Use when**: high-end marketing, hero variants.
**What it is**: Massive typography on one half of the viewport, interactive cards or horizontal-scroll image rails on the other half. Mobile collapse: full-width vertical stack.
**Cost**: low — layout discipline + responsive collapse.

### Visible grid as ornament
**Use when**: industrial / brutalist styles, technical surfaces.
**What it is**: `display: grid; gap: 1px;` with contrasting parent/child background colors to generate razor-thin dividing lines. Faint baseline grids, registration marks, ruler ticks reinforce the "engineered drawing" feel.
**Cost**: zero — pure CSS.

---

## Card patterns

### Parallax tilt card
**Use when**: hero showcase cards, premium feature cards.
**What it is**: 3D-tilting card that tracks mouse position within its bounding box.
**Cost**: low — `useMotionValue` for x/y, transform with perspective.
**Mobile note**: disable below `md:` — pointer events don't apply on touch.

### Spotlight border card
**Use when**: feature sections, premium card grids.
**What it is**: Card border illuminates dynamically under the cursor's proximity.
**Cost**: low — CSS radial gradient on a pseudo-element, mouse position tracked via CSS variable.

### Glassmorphism panel (true liquid glass)
**Use when**: high-end maximalist styles, modal overlays, navigation pills.
**What it is**: True frosted glass with inner refraction borders. Beyond `backdrop-blur`, add a 1px inner border (`border-white/10`) and a subtle inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`). These two layers simulate physical edge refraction; without them, "glass" reads as "blurred div."
**Cost**: low — pure CSS. Don't overuse; it's a moment, not a system. Reserve for fixed/sticky surfaces only — backdrop-blur on scrolling content kills mobile frame rates.

### Holographic foil card
**Use when**: premium / collectible / unboxing contexts.
**What it is**: Iridescent rainbow light reflections shifting on hover.
**Cost**: medium — conic-gradient + mix-blend-mode.

### Swipe-card stack
**Use when**: card-based decision UIs, onboarding flows, mobile-first surfaces.
**What it is**: Physical stack of cards the user can swipe away horizontally; the next card animates forward.
**Cost**: medium — motion library drag gestures + threshold detection.

### Morphing modal
**Use when**: detail views from card grids, expandable feature cards.
**What it is**: Button or card that seamlessly expands into its own full-screen dialog container using shared element transitions.
**Cost**: medium — `layoutId` for shared element.

### Double-bezel container (high-end signature)
**Use when**: hero product mockups, premium feature containers, form fields in maximalist styles.
**What it is**: Never place a premium card flatly on the background. Outer shell: wrapper element with subtle background (`bg-black/5` or `bg-white/5`), hairline outer border (`ring-1 ring-black/5` or `border border-white/10`), specific padding (`p-1.5` or `p-2`), large outer radius (`rounded-[2rem]`). Inner core: actual content container with distinct background, inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and mathematically calculated smaller radius (e.g., `rounded-[calc(2rem-0.375rem)]`) so inner and outer radii are visibly concentric.
**Why it works**: Cards read as physical, machined hardware — a glass plate sitting in an aluminum tray.
**Cost**: medium — radius math + nested structure.

### Hairline-border card (minimalist signature)
**Use when**: minimalist styles, editorial product surfaces, content cards.
**What it is**: White or layered surface fill, `1px solid #EAEAEA` border (or `rgba(0,0,0,0.06-0.10)` for warmer surfaces), `8px` to `12px` radius, generous internal padding (24-40px). On hover, border darkens to 0.16-0.24 alpha; add a near-invisible shadow (`box-shadow: 0 2px 8px rgba(0,0,0,0.04)`).
**Why it works**: Border is permission, not partition — present enough to confirm boundaries, faint enough to disappear.
**Cost**: zero — pure CSS.

### Bordered industrial card
**Use when**: industrial / brutalist styles, technical dashboards.
**What it is**: Bordered rectangle with visible header strip. Header contains ID code, revision number, status pill — all monospace uppercase. Internal content sits flush against the border; padding is minimal (8-16px). Optional corner crosshairs (+) at each interior corner.
**Cost**: zero — CSS.

### Tinted-shadow card (creative-cohort signature)
**Use when**: creative tools, brand-led marketing.
**What it is**: Drop shadow colored in the section accent rather than gray. A teal section gets teal-mist shadows. Default values: `0 8px 32px` with 8-14% alpha in the brand hue, often paired with a tighter `0 1px 2px` black at 6% for grounding.
**Why it works**: Reads as "lit from inside the brand."
**Cost**: zero — CSS tint.

### Hover-revealed color card
**Use when**: feature grids where chromatic energy is reserved for engagement.
**What it is**: Card sits in neutral chrome at rest; on hover, lights up in its category color. Transition is slow (400-700ms) so the lit state has time to register.
**Cost**: zero — CSS transition.

---

## Scroll animation patterns

### Horizontal scroll hijack
**Use when**: galleries, sequential storytelling.
**What it is**: Vertical scroll input translates into smooth horizontal gallery pan.
**Cost**: high — scroll-trigger library, pinning, careful performance.

### Locomotive sequence
**Use when**: hero showcase reveals, premium product launches.
**What it is**: Video / 3D sequence where framerate ties directly to scrollbar position.
**Cost**: very high — preloaded image sequence or canvas.

### Zoom parallax
**Use when**: long-form storytelling pages, photo-led marketing.
**What it is**: Central background image zooming in / out seamlessly as the user scrolls.
**Cost**: medium — scroll-trigger + transform.

### Liquid swipe transition
**Use when**: between-page transitions in editorial sites, between hero variants in tabbed flows.
**What it is**: Page transitions that wipe the screen like viscous liquid.
**Cost**: high — SVG path morphing.

### Scroll-pinned product walk
**Use when**: feature deep-dives, complex multi-step features.
**What it is**: A feature block pins the product visual and scrubs through a sequence of states as the user scrolls — frame 1: empty state, frame 2: user types, frame 3: result appears, frame 4: AI responds. Narrative coupled with motion without autoplay.
**Cost**: medium — scroll-trigger library + state sequencing.

### Sticky-text scroll columns
**Use when**: feature deep-dives where a single capability needs 3-6 visual states.
**What it is**: Short headline + bullet list pins on the left while a stack of product screenshots scrolls past on the right, swapping in at scroll triggers.
**Cost**: medium — sticky positioning + scroll observers.

### Scroll-scrubbed video
**Use when**: motion-heavy demo content; replaces autoplay video.
**What it is**: Video frame advances with scroll position, giving the user manual control over the demonstration. Loops back when scrolled past.
**Cost**: medium — video element + scroll position math.

### Subtle scroll-entry fade-up
**Use when**: section entries on all premium surfaces — the default reveal motion.
**What it is**: Elements fade in as they enter the viewport with `translateY(12px)` + `opacity: 0`, resolving over 280-600ms with `cubic-bezier(0.16, 1, 0.3, 1)`. Implementation via `IntersectionObserver`, never `window.addEventListener('scroll')`.
**Cost**: zero — Intersection Observer + CSS transition.

### Subtle background parallax
**Use when**: decorative backgrounds, subtle depth on hero ornaments.
**What it is**: 5-15% scroll-speed offset between foreground and background. The intent is depth, not spectacle.
**Cost**: low — transform on scroll.

(Note: side-of-page scroll progress paths — fixed vertical SVG lines tracking scroll position on the viewport edge — are deliberately excluded from this arsenal. They read as stale, add visual noise, and signal generated output. If progress feedback is needed, integrate it into the navigation as a thin top bar or use active-state on nav links as sections enter view.)

---

## Typography patterns

### Kinetic marquee
**Use when**: brand statements, "trusted by" sections, editorial energy.
**What it is**: Endless text bands that reverse direction or speed up on scroll. Authentic typography or icons, never lorem placeholders.
**Cost**: low — CSS keyframes + scroll-triggered speed multiplier.

### Text mask reveal
**Use when**: brand hero moments, editorial transitions.
**What it is**: Massive typography acting as a transparent window to a video background.
**Cost**: low — `background-clip: text` + a `<video>` behind.

### Text scramble effect
**Use when**: technical surfaces, command interfaces, infrastructure products.
**What it is**: Character-decoding effect on load or hover — random characters cycle then settle into the final string.
**Cost**: low — JS interval cycling random chars then settling.

### Circular text path
**Use when**: brand marks, decorative section labels.
**What it is**: Text curved along a spinning circular path.
**Cost**: low — SVG `<textPath>` + CSS rotate animation.

### Gradient stroke animation
**Use when**: outlined display headlines on premium maximalist surfaces.
**What it is**: Outlined text with a gradient continuously running along the stroke.
**Cost**: low — `-webkit-text-stroke` + `background-clip: text` + animation.

### Kinetic typography grid
**Use when**: brand statements, interactive typographic showcases.
**What it is**: Grid of letters dodging or rotating away from the cursor.
**Cost**: medium — pointer position + per-letter transform.

### Inline typography images
**Use when**: editorial headlines, brand-led marketing.
**What it is**: Small pill-shaped images embedded directly inside massive headings. The text breaks around a tiny image; the image is treated as a glyph within the typographic flow.
**Cost**: low — inline-block image elements with vertical alignment math.

### Horizontal accordions
**Use when**: portfolio surfaces, content-led navigation.
**What it is**: Vertical slices that expand horizontally on hover to reveal content and imagery.
**Cost**: medium — flex with width transitions.

### Two-tone editorial body emphasis
**Use when**: longform body copy with semantic emphasis.
**What it is**: Body text in charcoal (#171717-#1F1F1F); emphasized words in a slightly muted secondary color or full-saturation accent. The shift between weight + color carries emphasis without italic or bold.
**Cost**: zero — CSS color tokens.

### Variable-axis hover animation
**Use when**: premium creative-tool surfaces, brand-led marketing.
**What it is**: Font weight tightens from 400 to 600 as the cursor approaches a label; a number "settles" from 800 to 600 once a counter finishes animating. Cheap to ship if the font supports it; very expensive-looking on first encounter.
**Cost**: low — `font-variation-settings` animation on a variable font.

### Single-word gradient
**Use when**: hero headlines on creative-cohort surfaces.
**What it is**: A linear or conic gradient fills one carefully chosen word in the hero or a section headline. The rest stays plain.
**Why it works**: Whole sentences in gradient text date the work; one word in gradient reads as craft.
**Cost**: low — `background-clip: text` on a single span.

### Headline + deflating qualifier
**Use when**: ambitious-but-honest brand voice (creative tools, AI products).
**What it is**: Big claim + small honest constraint. "Make anything possible — in one tool." "Build better sites, faster." The qualifier is what makes the claim believable.
**Cost**: zero — copy structure.

---

## Micro-interactions

### Particle explosion button
**Use when**: success-state moments, celebratory micro-confirmations (sparingly).
**What it is**: CTA that shatters into particles upon success state confirmation.
**Cost**: medium — canvas or many small absolute-positioned elements.

### Liquid pull-to-refresh
**Use when**: mobile-native feeling lists, refreshable feeds.
**What it is**: Mobile reload indicators that act like detaching water droplets.
**Cost**: medium — SVG morph + drag gesture.

### Skeleton shimmer
**Use when**: any loading state, especially product UI.
**What it is**: Shifting light reflection moving across placeholder boxes during load. Skeleton blocks mirror the eventual layout so the page does not jump on resolve.
**Cost**: low — CSS keyframe animating a linear-gradient position.

### Directional hover-aware button
**Use when**: card hovers, button-prominence moments.
**What it is**: Hover fill enters from the exact side the mouse entered from.
**Cost**: low — JS detects entry direction, CSS variable drives fill direction.

### Ripple click effect
**Use when**: tactile feedback on press, system-feel surfaces.
**What it is**: Visual waves rippling precisely from click coordinates.
**Cost**: low — absolute-positioned span on click, scale + fade.

### Animated SVG line drawing
**Use when**: diagram explainers, technical surfaces, custom icon reveals.
**What it is**: Vectors that draw their own contours in real-time.
**Cost**: low — `stroke-dasharray` trick.

### Mesh gradient background
**Use when**: hero backgrounds in high-end maximalist styles.
**What it is**: Organic lava-lamp-like animated color blobs. 3-5 large blurred radial gradients in brand colors, drifting slowly (4-8s ease loops, 3-6px translation). Positioned out of the safe text area so contrast on copy stays consistent.
**Why it works**: Cheap to implement, expensive-looking. The hero feels alive without distracting.
**Cost**: medium — large blurred radial gradients, CSS animations driving position.

### Lens blur depth
**Use when**: focus modes, modal overlays, action-isolated moments.
**What it is**: Dynamic focus blurring background UI layers to highlight a foreground action.
**Cost**: low — backdrop-filter on a sibling layer.

### Magnetic micro-physics
**Use when**: hero CTAs in high-end styles when MOTION_INTENSITY > 5.
**What it is**: Button pulls slightly toward the cursor. Implemented via `useMotionValue` + `useTransform`, never `useState`.
**Cost**: low — motion library.

### Cursor-following glow
**Use when**: hero canvases, interactive demo surfaces.
**What it is**: A subtle radial glow follows the cursor through the hero canvas. Brand-colored, fades within 200ms of cursor stop.
**Cost**: low — pointer position + radial gradient on a pseudo-element.

### Custom cursor inside demo surface
**Use when**: interactive product demos in maximalist styles.
**What it is**: Cursor changes to a labeled name-badge, a brush, a pointer, or a product-specific shape only when the user mouses into the demo surface. Reinforces "you're in the product now."
**Cost**: low — `cursor: url(...)` scoped to the surface.

### Perpetual archetypes (when MOTION_INTENSITY > 5)
Continuous, infinite micro-animations embedded in standard components. Premium spring physics — never linear easing.
- **Pulse** — soft scale or opacity breathing on status indicators and live elements.
- **Typewriter** — multi-step text cycling through complex prompts with a blinking cursor and shimmering "processing" state.
- **Float** — gentle Y-axis drift on hero badges, decorative elements.
- **Shimmer** — horizontal light gradient sliding across skeletal placeholders and active cards.
- **Carousel** — seamless infinite horizontal loop using `x: ["0%", "-100%"]`.

Each perpetual loop MUST be memoized (`React.memo`) and isolated in its own microscopic Client Component. Never trigger re-renders in the parent layout.

### Spring physics specs
Standard spring for premium feel:
```
{ type: "spring", stiffness: 100, damping: 20 }
```
No linear easing on interactive elements. For UI feedback, use `cubic-bezier(0.16, 1, 0.3, 1)`. For cinematic entries, `cubic-bezier(0.32, 0.72, 0, 1)`.

### Layout transitions with shared element IDs
Always utilize motion library's `layout` and `layoutId` props for smooth re-ordering, resizing, and shared element transitions across state changes. This is the difference between "things move" and "things morph."

### Staggered orchestration
Do not mount lists or grids instantly. Use `staggerChildren` (motion library) or CSS cascade (`animation-delay: calc(var(--index) * 80ms)`) for sequential waterfall reveals. The cascade is direction-aware — left-to-right on LTR locales, mirrored on RTL.

**Critical:** For `staggerChildren`, the Parent (`variants`) and Children MUST reside in the identical Client Component tree. If data is fetched asynchronously, pass the data as props into a centralized Parent motion wrapper.

### Hover physics
Every clickable card or image reacts on hover:
- Image scale with eased duration inside `overflow-hidden`: `group-hover:scale-105 transition-transform duration-700 ease-out`
- Border or backdrop transitions
- Subtle shadow lift
- Multiple effects in concert (border brightens + inner icon rotates 10° + arrow slides 4px right) read as one composite motion, not five separate animations

### Choreographed micro-events on cards
**Use when**: feature cards, premium grid surfaces.
**What it is**: A card hover does multiple things in concert: background lifts (translate -2px), shadow expands, border brightens, an inner icon rotates 10°, an arrow slides 4px right. The composite effect reads as one motion, not five separate animations.
**Cost**: zero — CSS transitions with consistent timing.

---

## Dashboard-specific patterns

The 5 card archetypes for modern SaaS dashboards. A common arrangement: Row 1 with 3 columns, Row 2 with 2 columns split 70/30.

### The Intelligent List
Vertical stack of items with an infinite auto-sorting loop. Items swap positions using shared layout IDs, simulating an AI prioritizing tasks in real-time.
**Use for**: "this is a smart product" surfaces.

### The Command Input
Search / AI bar with a multi-step typewriter effect. Cycles through complex prompts. Includes a blinking cursor and a "processing" state with a shimmering loading gradient.
**Use for**: hero placement on AI products, search-first surfaces.

### The Live Status
Scheduling interface with "breathing" status indicators. Pop-up notification badge that emerges with overshoot spring, holds for 3 seconds, vanishes cleanly.
**Use for**: live-data products, monitoring surfaces.

### The Wide Data Stream
Horizontal infinite carousel of data cards or metrics. Loop is seamless via `x: ["0%", "-100%"]` at a speed that feels effortless (15-25s typical).
**Use for**: telemetry surfaces, observability, real-time feeds.

### The Contextual Focus Mode
Document view that animates a staggered highlight of a text block, followed by a float-in of a floating action toolbar with micro-icons.
**Use for**: editing surfaces, AI-assisted document tools.

### Dashboard hardening rules (when VISUAL_DENSITY > 7)
- Generic card containers are out. Use logic-grouping via `border-t`, `divide-y`, or pure negative space.
- Numbers right-aligned in `font-mono` (tabular figures).
- Sticky headers on long tables.
- Empty rows show empty states across the full width, never collapse silently.
- Action columns right-aligned.
- 1px hairline borders for surface elevation in dark mode rather than drop shadows.
- 4-5 step surface lightness ladder (page → card → raised → popover → overlay).

### Tiered surface elevation (dark mode)
**Use when**: dark-mode dashboards, premium dev tools.
**What it is**: 4-5 step lightness ladder for page/card/raised/popover/overlay. Each step is small in absolute lightness (~3-5% L lift) but the cumulative effect creates real depth. No drop shadows; elevation lives in lightness.
**Cost**: zero — token discipline.

### Code-as-design-content
**Use when**: developer-tooling surfaces, infrastructure marketing.
**What it is**: Treat a code block like hero photography. Short (6-14 lines), syntax-highlighted with a custom theme that matches the page accent (not a third-party scheme), inside window chrome (traffic-light dots, title bar with filename). Pixel-perfect HTML/CSS, not a screenshot — scales crisply.
**Cost**: medium — custom syntax theme + window chrome styling.

### Terminal mockup
**Use when**: infrastructure / CLI / dev-tool marketing.
**What it is**: Near-black window with traffic-light chrome and a `$` or `>` prompt. Command is short, declarative, often runnable exactly as written. Multi-line terminals fade older lines via opacity reduction. Output is monospace and color-coded (green success, gray chatter, bright neutral for user input).
**Cost**: low — CSS + content.

### Cropped dashboard preview
**Use when**: B2B product marketing showing dashboards or admin interfaces.
**What it is**: Cropped, never full-page. The reader sees one card, one chart, a sliver of nav — enough to read "this is software," not enough to actually parse the dashboard. Real data shapes (sparklines, log lines, plausible numbers) instead of stock chart shapes.
**Cost**: zero — design discipline.

### Keyboard shortcut chip
**Use when**: products that have been designed by people who care about keyboard speed.
**What it is**: Compressed monospace inside a low-radius pill with a 1px hairline border. Appears in nav, body text, hero illustrations. `<kbd>` markup: `border: 1px solid #EAEAEA`, `border-radius: 4px`, `background: #F7F6F3`, monospace font.
**Cost**: zero — markup discipline.

---

## Imagery patterns (mandatory — never ship text-only walls)

Imagery is part of the design, not a nice-to-have. Every layout must accommodate it.

### Full-bleed product image
**Use when**: showcasing the actual product / app screen. Anchor every major section with one.
**What it is**: A single edge-to-edge image (or container-width) running full bleed between text blocks. No frame, no shadow, no caption chrome — let the image speak.
**Source**: real product screenshots when available, or a custom inline-SVG placeholder. (Seeded `picsum.photos` for local prototyping only — the linter flags shipped picsum.)

### Inline contextual image
**Use when**: illustrating a feature, a moment, a person.
**What it is**: 1:1 or 4:5 image embedded in the text flow, sized to match a body-text column. Caption optional, italic small type.

### Editorial image-headline juxtaposition
**Use when**: a hero or section-opener needs visual + verbal weight together.
**What it is**: A large image to one side, a large headline to the other, deliberately uneven gutters. The image is NOT decoration behind the text — it stands as its own element.

### Soft-edge lifestyle image
**Use when**: hero or brand sections that need warmth.
**What it is**: Lifestyle photo with a subtle fade-to-canvas edge (radial gradient mask) so the image grounds the page without a hard boundary.

### Image grid (sparingly)
**Use when**: showing a portfolio, a gallery, multi-product proof.
**What it is**: 2-column or 3-column image grid, irregular aspect ratios, generous gaps. NOT cards — just images.

### Annotated UI screenshot
**Use when**: explaining a feature, surfacing a specific capability inside the interface.
**What it is**: Crop the product UI tightly. Add thin connector lines (1px in the brand color) from labels to specific features. Labels are short pills (2-4 words) with no heavy background. The annotation language is "architectural diagram," not "marker on a photo."
**Cost**: low — overlay markup on the screenshot.

### Tilted product frame
**Use when**: high-end maximalist / creative-tool styles, hero product mockups.
**What it is**: Product shots tilted 6-12° on the Y-axis, given a subtle perspective shadow, floated against the section background. Creates the "design object" framing — screenshot becomes an artifact, not documentation.
**Cost**: low — CSS transform + shadow.

### Stacked-card collage
**Use when**: hero compositions when a single screenshot doesn't convey breadth.
**What it is**: 2-4 UI fragments layered at varying z-depths — a panel, an overlay, a tooltip, a popup — creating dimensional composition. Suggests "here are several features at once." Choreographed; layers overlap intentionally to imply depth without obscuring meaning.
**Cost**: medium — z-stacking + intentional crop.

### Ghost-cursor screenshot
**Use when**: products with multiplayer or collaborative features.
**What it is**: Static screenshots show fake collaborator cursors with name labels mid-action, simulated typing indicators, active selection states. Proves multiplayer without motion.
**Cost**: zero — overlay markup on the screenshot. Names must be plausible (not "User1").

### Before / after panel
**Use when**: AI products, transformation features, magic-trick demos.
**What it is**: Two-panel comparison: messy input left, clean output right, often with an arrow or wand glyph between. Demonstrates value without verbal explanation.
**Cost**: zero — layout.

### Monochrome logo wall
**Use when**: trust strips, customer-proof sections.
**What it is**: 6-10 customer logos in a single row, all desaturated to the page's neutral text color, at uniform optical weight (not pixel size — adjusted per logo so they read evenly). Spaced with generous gutters. Often introduced by a short label ("Working with", "Trusted by teams at").
**Why it works**: Removes visual chaos; the wall reads as a single block of social proof.
**Cost**: zero — CSS filter or pre-rendered greyscale assets.

### Generative-art output as portfolio
**Use when**: AI products where the output IS the product.
**What it is**: Sample images, audio waveforms with transcript captions, sample text in an editor, placed in the layout AS IF they were portfolio pieces. The output is the proof; description is supplementary.
**Cost**: low — curated assets + grid layout.

### OS chrome preserved
**Use when**: product showcase imagery for desktop or mobile apps.
**What it is**: Keep real OS chrome (macOS traffic lights, Windows title bar, mobile status bar) in screenshots. Grounds the product as real software, not a prototype.
**Cost**: zero — design discipline.

### Lifestyle hero with editorial framing
**Use when**: brand-led products, hospitality, premium consumer hardware.
**What it is**: Real photography (rare in B2B premium), shot in real environments, with editorial restraint — natural lighting, no heavy retouching. Portraits at 4:5 or near-square with generous negative space.
**Cost**: high — real production. Multiple aspect-ratio crops for responsive art direction.

### Decorative dot-grid / line-pattern background
**Use when**: subtle spatial-feel backgrounds on calm sections.
**What it is**: A fine dot-grid or line-pattern visible only on inspection. Gives the page a "plotted on a working grid" feel.
**Cost**: zero — CSS background or SVG pattern.

### Custom illustration (restrained)
**Use when**: a concept is too abstract for a screenshot.
**What it is**: Flat-vector or low-poly 3D in the site's accent palette. Geometric blobs, abstract isomorphic objects, stylized "tools in space" compositions. Monochrome or near-monochrome.
**Cost**: medium-high — custom illustration work. Never stock illustration. Never generic isometric people.

---

## Hero treatments observed across premium sites

### Large product mock as hero
The canonical hero image is the actual UI — a dashboard, workflow, chat interface. Cropped close, with extreme detail visible. Real-looking data inside it. Soft drop shadow + subtle rounded corners (12-24px). Box-shadow at low opacity, high blur (e.g., `0 24px 64px rgba(0,0,0,0.08)`). The screenshot floats above the page without harsh edges.

### Animated metric callouts in hero
Numbers tick up from 0 on entry over 800-1500ms. Restricted to 2-3 stats max; more dilutes the effect. Counter triggers once per page entry, not on every scroll past.

### Interactive product demo in hero
A real, manipulable instance of the product running inline. The user can drag, type, click — and the product responds with actual logic, not a video loop. The strongest "designed by designers" signal available. Affordances: subtle pulsing dots, ghost hand-cursor hints, a "try it" label on the first interactable element.

### Kinetic headline reveal
Hero text appears almost instantly; the heavier interactive demo or 3D render fades in 200-400ms behind it. Never make users wait for first meaningful paint.

### Slow ambient hero motion
A slow rotating gradient, a chart that gently animates, a token sliding across a connection. Subtle enough that you only notice it on a second look.

### Auto-playing muted hero video
Hero video plays automatically, muted, looped, often at reduced contrast or with a subtle dark gradient overlay to keep overlaid text legible. The video runs in the background of attention. Provides a still poster image as a fallback. Compresses aggressively (under 4MB for a 30-second loop).

### Pulsing globe / animated map
Recurring shorthand for "global infrastructure." The animation is slow (3-6s loop), low-saturation, never obstructs the headline. Labels only on the regions you actually have presence in.

### 3D marquee object
A single hero-render of the product as a physical thing — soft-clay device, glass orb, metallic monolith. Rotates on scroll. Matte (not glossy) PBR materials with strong rim light and soft floor shadow. Anchors the brand in physical-design vocabulary.

### Two-column hero with metaphor image
Text the heavy lifting; image carries metaphor. Works for support and customer-experience categories. The image is atmospheric (not literal product UI) — water, light, fabric, sky as metaphor for the feeling the product evokes.

### Synthetic screenshot composition
When the surface is too abstract to screenshot (a workflow, an AI agent conversation, a queue of work), the imagery becomes a stylized composition of UI fragments: a card, a notification, a chat bubble, a status pill, all floating against a soft background. Implies a product without committing to a literal frame.

### Narrative chat thread
Multi-turn conversation between an agent and a person, shown inline on the marketing page. The reader absorbs the capability through the conversation, not through prose explaining it. Replaces older "feature screenshot" treatments for AI-adjacent capabilities.

---

## Combinations that work

| Brief | Patterns |
|---|---|
| Modern SaaS landing | Asymmetric split hero + bento grid + spotlight border cards + perpetual micro-interactions |
| AI product landing | Thesis-statement hero + before/after panels + command input demo + magnetic button + mesh gradient bg |
| Developer-tooling landing | Code-as-design hero + terminal mockup + monochrome logo wall + keyboard chips + status indicator |
| Fintech / wealth | Editorial split + email-capture hero + monochrome logo wall + research/timeline band |
| Creator-tool landing | Interactive demo hero + bento grid + per-section accent colors + tilted product frames + tinted shadows |
| Premium consumer brand | Cinematic center hero + double-bezel containers + mesh gradient + scroll-pinned product walks |
| Portfolio | Masonry + parallax tilt cards + horizontal scroll hijack on featured pieces |
| Editorial / brand | Curtain reveal + kinetic marquee + text mask reveal + circular text path |
| Dashboard (cockpit density) | Tiered surface elevation + intelligent list + wide data stream + cropped dashboard preview |
| Mobile app landing | Morphing status pill nav + dock-style magnification CTA + parallax tilt feature card |
| Long-form content / docs | Editorial column rhythm + hairline-border cards + subtle fade-up + monochrome logo wall |
| Brutalist editorial | Visible grid + bordered industrial cards + step-function reveals + terminal mockup |

---

## Hard combinations to avoid

| Don't combine | Why |
|---|---|
| GSAP + motion library in same component tree | Conflicting animation control; pick one |
| 3+ scroll-triggered effects on the same page | Performance collapse — frame drops on mobile |
| Magnetic button + parallax tilt + spotlight border on the SAME card | Visual noise; the moment dies |
| Every section with perpetual motion | Eye-fatigue; the user can't focus on content |
| Glassmorphism + heavy drop shadow on the same card | Conflicting depth language |
| Variable-font weight animation + scramble + typewriter on the same headline | Three motion languages applied to one surface; pick one |
| Mesh gradient + heavy texture overlay on hero | Visual noise; the gradient loses depth |
| 3D-tilted product window + parallax background + scroll-scrubbed video | Three "premium effect" patterns layered; the page reads as showcase, not product |
| Brutalist visible grid + soft drop shadow + glassmorphism | Style collision — pick one system and commit |
| Title Case + decorative serif + center alignment on a software dashboard | Three "premium feel" reflexes on a surface that doesn't want them |
| Customer logo wall repeated 3+ times | Overcompensation; the trust signal collapses |

---

## Performance reminders

- **Hardware acceleration** — never animate `top`, `left`, `width`, `height`. Animate exclusively via `transform` and `opacity`. These are the only two properties that hit the compositor without triggering layout.
- **Perpetual motion isolation** — any perpetual animation memoized (`React.memo`) and isolated in its own microscopic Client Component. Never trigger re-renders in the parent layout.
- **`<AnimatePresence>` wrap** — wrap dynamic lists in `<AnimatePresence>` to handle enter/exit cleanly.
- **Lazy load below the fold** — `loading="lazy"` on images, declare `width`/`height` attributes to prevent CLS.
- **Grain / noise overlays** — apply only to `fixed pointer-events-none` pseudo-elements, never to scrolling containers. Continuous GPU repaints craters mobile performance.
- **Cleanup discipline** — every `useEffect` animation contains strict cleanup. GSAP / WebGL contexts wrapped in `useEffect` cleanup blocks that kill timelines and dispose contexts.
- **No GSAP + motion library mix** — default to motion library for UI / Bento interactions. Use GSAP / WebGL exclusively for isolated full-page scrolltelling or canvas backgrounds.
- **Horizontal scroll prevention** — wrap the entire page in `<main className="overflow-x-hidden w-full max-w-full">` to prevent horizontal scrollbars from off-screen animations.
- **`backdrop-filter` discipline** — reserve for fixed or sticky elements (navbars, overlays, modals). Never apply blur filters to scrolling content or large always-on areas.
- **Z-index restraint** — reserve high `z-index` values for systemic layers (sticky nav, modal, overlay, tooltip). Document them so they don't sprawl.
- **`will-change` sparingly** — only on elements actively animating. Remove after animation completes.
- **Font loading** — `font-display: swap` or equivalent to avoid invisible text during font load.
- **Critical-path CSS** — inline for above-the-fold content where possible.
- **`prefers-reduced-motion`** — respected universally. Replace transforms with simple opacity fades, shorten durations, drop blur components, pause background mesh animations.
- **Reduce motion intensity by 2 levels on mobile** — what reads as ambient on desktop reads as distracting on mobile.
- **Cap hero video size** — under 4MB for a 30-second loop. Provide poster image for slow connections.
- **Mount animations once** — number counters animate on enter-view, not on every scroll past.

---

## When to apply each pattern

- **Animated counters**: when the metric is the proof. Skip when the number is incidental.
- **Numbered "how it works"**: when the product has a clear onboarding arc. Skip if it's a single tool with no sequence.
- **"Before / after" comparison**: when there's a clear status-quo competitor to displace. Skip in greenfield categories.
- **Logo strip**: when 6+ recognizable customers can be named. Skip with 3 logos — looks thin.
- **Bento grids**: when 5-8 distinct capabilities need showcasing. Skip for 3 — looks underbuilt.
- **Chapter-framework narrative**: when the product is large enough to feel like a journey. Skip on single-purpose tools.
- **Ambient hero motion**: when the page is otherwise quiet. Don't stack motion on motion.
- **Compliance badges**: when procurement teams will ask. Skip on consumer-facing surfaces.
- **Gradient background section**: once per page, at the section that matters most.
- **Mid-page "still have questions" deflector**: on long pages. Skip on short pages — the final CTA does the job.
- **Interactive product demo**: when the product is visual or temporal and 60+ seconds of engagement justifies the build cost.
- **Mesh gradient background**: on hero surfaces in maximalist styles; skip on minimalist or industrial.
- **Pulsing globe**: when the product has genuine global infrastructure to surface; skip when it's vibes.
- **Variable-axis hover animation**: when the brand voice is "we notice details"; skip when the audience won't.
- **Tinted shadow**: in creative-cohort styles; skip in industrial or minimalist.
- **Liquid glass / double bezel**: in high-end maximalist styles; skip elsewhere — it reads as decorative grafting.
- **Visible grid as ornament**: in industrial / brutalist styles; skip elsewhere.

---

## Closing principle

The arsenal exists to defeat reflex. The default generator output picks the safest, most-frequent neighbor for every slot in a layout. Each pattern here is a way to refuse that reflex with intention.

The patterns are not stylistic preferences — they are deliberate moves with measurable costs and clear use cases. Pick the moves that match the brief. Execute them with precision. Cut everything else.

Match implementation complexity to aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well — not from picking the most elaborate vision available.

Pick a clear conceptual direction. Bold maximalism and refined minimalism both work. Intentionality is the differentiator, not intensity.
