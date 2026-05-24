# Design Generation Methodology

This is the playbook for producing high-end frontend code that defeats AI-aesthetic biases. Default LLM output has measurable, predictable failure modes: narrow containers that force 6-line headings, gapless bento grids that ship with dead cells, generic typography (Inter everywhere), purple-on-white gradients, "Acme/Nexus" filler brand names, "John Doe" fake users, centered everything, three-equal-card feature rows, invisible button text. This document encodes the rules, dials, patterns, and bans that force the output up to a senior-designer baseline.

Read it before any UI work. Apply it during. Run the pre-flight checklist before shipping.

---

## Active baseline (the 3 dials)

Every generation runs against three dials. They are the global variables that drive every subsequent rule in this document. Default values below; respect any explicit user override in the current prompt.

### DESIGN_VARIANCE — default: 8
Controls layout regularity vs. asymmetric chaos.

| Level | Behavior |
|---|---|
| 1-3 (Predictable) | Flexbox `justify-center`, strict 12-column symmetrical grids, equal paddings, mirror-image sections. |
| 4-7 (Offset) | Use `margin-top: -2rem` overlapping. Varied image aspect ratios (4:3 next to 16:9). Left-aligned headers over center-aligned data. Asymmetric whitespace. |
| 8-10 (Asymmetric) | Masonry layouts. CSS Grid with fractional units (`grid-template-columns: 2fr 1fr 1fr`). Massive empty zones (`padding-left: 20vw`). Diagonal flow, overlap, grid-breaking elements. |

**Per product type defaults:**
- Marketing / landing: 8 (editorial energy)
- Dashboard / admin: 5 (predictable scanning beats clever)
- E-commerce / shop: 6 (browseable but distinctive)
- Mobile app shells: 5 (small viewports collapse anyway)
- Editorial / magazine: 9 (lean into chaos)
- Portfolio / agency: 9

**Mobile fallback rule (mandatory):** For VARIANCE 4-10, any asymmetric layout above `md:` MUST aggressively fall back to a strict single-column layout (`w-full`, `px-4`, `py-8`) on viewports `< 768px`. No exceptions. Horizontal scrollbars from off-screen animations are a critical failure.

### MOTION_INTENSITY — default: 6
Controls animation density and physics complexity.

| Level | Behavior |
|---|---|
| 1-3 (Static) | No automatic animations. CSS `:hover` and `:active` states only. Tactile feedback (translate, scale) is allowed and encouraged. |
| 4-7 (Fluid CSS) | `transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1)`. `animation-delay` cascades for load-ins. Focus exclusively on `transform` and `opacity`. Use `will-change: transform` sparingly. |
| 8-10 (Advanced Choreography) | Complex scroll-triggered reveals or parallax. Use motion library hooks. NEVER use `window.addEventListener('scroll')`. Pinning, scrubbing, stacked card transitions. |

**Per product type defaults:**
- Marketing / landing: 7-8 (motion sells)
- Dashboard / admin: 4 (motion is feedback, not show)
- E-commerce / product detail: 6
- Mobile app shells: 5
- Editorial / longform: 8
- Form-heavy SaaS: 4

**Mobile fallback rule:** Reduce by 2 levels below `md:`. Honor `prefers-reduced-motion: reduce` at every level.

### VISUAL_DENSITY — default: 4
Controls information packing per square inch.

| Level | Behavior |
|---|---|
| 1-3 (Art Gallery) | Generous whitespace. Huge section gaps. Sparse text. Everything feels expensive and quiet. |
| 4-7 (Daily App) | Normal spacing for standard web apps. Comfortable scanning. |
| 8-10 (Cockpit) | Tiny paddings. No card boxes — 1px lines separate data. Packed grids. **Mandatory:** Use `font-mono` for all numbers. |

**Per product type defaults:**
- Marketing / landing: 3
- Dashboard / admin: 7
- E-commerce / shop: 5
- Mobile app shells: 4
- Editorial / magazine: 3
- Trading / analytics / monitoring: 9
- Internal tools: 8

**Mobile fallback rule:** Cap density at 6 on mobile. Cockpit mode (8-10) becomes scrollable card stacks below `md:`, not 1px-divided rows.

---

## Default architecture & stack conventions

Unless the user explicitly specifies otherwise, these structural constraints maintain consistency across generations.

### Framework
React or Next.js. Default to Server Components (`RSC`).

**RSC safety:** Global state works ONLY in Client Components. In Next.js, wrap providers in a `"use client"` component.

**Interactivity isolation:** If motion or refractive effects are active, the specific interactive UI component MUST be extracted as an isolated leaf component with `'use client'` at the very top. Server Components must exclusively render static layouts. This prevents bundle bloat and hydration mismatch.

### Dependency verification (mandatory)
Before importing ANY third-party library (`framer-motion`, `lucide-react`, `zustand`, etc.), check `package.json`. If the package is missing, output the installation command (`npm install package-name`) before providing the code. Never assume a library exists.

### State management
Use local `useState` / `useReducer` for isolated UI. Use global state strictly to avoid deep prop-drilling — not as a default. Resist Redux/Zustand unless three or more components share the same data three or more levels apart.

### Styling policy
Tailwind CSS for 90% of styling.

**Tailwind version lock:** Check `package.json` first. Do not use v4 syntax in v3 projects.

**Tailwind v4 config guard:** For v4, do NOT use the `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin.

### Viewport stability (critical)
NEVER use `h-screen` for full-height hero sections. ALWAYS use `min-h-[100dvh]` to prevent catastrophic layout jumping on mobile browsers (iOS Safari's address-bar collapse breaks `h-screen`).

### Grid over flex-math
NEVER use complex flexbox percentage math (`w-[calc(33%-1rem)]`). ALWAYS use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) for reliable structures. Grid wins on responsive, gap consistency, and gap-flow-dense.

### Responsiveness & spacing
- Standardize breakpoints: `sm`, `md`, `lg`, `xl`.
- Contain page layouts using `max-w-[1400px] mx-auto` or `max-w-7xl`.
- Section vertical padding: `py-32 md:py-48` on marketing pages. Sections must feel like distinct cinematic chapters, not cramped slabs.

### Icon system
Use Google Material Symbols as the primary icon set. Configure `font-variation-settings` to control fill, weight, grade, and optical size — that's the whole point of variable icon fonts.

```html
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;">
  search
</span>
```

Acceptable secondary fallbacks: Phosphor (`@phosphor-icons/react`), Radix Icons (`@radix-ui/react-icons`), Lucide. Standardize `strokeWidth` globally — pick `1.5` or `2.0` and stick with it across the entire output.

---

## Design engineering directives (bias correction)

LLMs have measurable statistical biases toward specific UI cliché patterns. The directives below proactively construct premium interfaces by overriding those biases at the generation step.

### Deterministic typography

**Display / headlines**
- Default: `text-4xl md:text-6xl tracking-tighter leading-none`.
- The H1 must NEVER exceed 2 to 3 lines. 4, 5, or 6 lines is a catastrophic failure. Make the font size smaller (`clamp(3rem, 5vw, 5.5rem)`) and the container wider to ensure this.
- Use ultra-wide containers for the H1: `max-w-5xl`, `max-w-6xl`, or `w-full`. Let words flow horizontally.

**Body / paragraphs**
- Default: `text-base text-gray-600 leading-relaxed max-w-[65ch]`.

**Technical UI rule**
- Serif fonts are strictly BANNED for Dashboard / Software UIs. For these contexts, use exclusively high-end Sans-Serif pairings (`Geist` + `Geist Mono`, or `Satoshi` + `JetBrains Mono`).
- All numbers in cockpit-density UIs use `font-mono` to lock tabular alignment.

**Banned font choices**
- Inter is acceptable per recent corrected direction (it was previously banned in legacy guidance, but Inter remains a legitimate choice today). Pair it carefully and avoid leaning on it as the only option.
- Arial, Roboto, generic system stacks are forbidden as primary display faces.
- Default to a distinctive display font (`Satoshi`, `Cabinet Grotesk`, `Outfit`, `Geist`) paired with a refined body face.
- Vary across generations. Never converge on `Space Grotesk` repeatedly. No two outputs should reach for the same stack reflexively.

### Color calibration

**Constraints**
- Max 1 accent color per design.
- Saturation < 80%.
- Use absolute neutral bases (Zinc, Slate, Stone) with high-contrast singular accents (Emerald, Electric Blue, Deep Rose, Amber).

**Banned aesthetics**
- The "AI Purple/Blue" gradient (purple-to-blue on white) is strictly BANNED. No purple button glows. No neon gradients.
- Pure black `#000000` is banned. Use Off-Black, Zinc-950, or Charcoal (`#0a0a0a`, `#111111`).
- Oversaturated accents are banned. Desaturate to blend elegantly with neutrals.
- Text-fill gradients on large headers are banned.

**Color consistency**
- Stick to one palette for the entire output. Do not fluctuate between warm and cool grays within the same project. Pick warm OR cool; commit.
- Dominant colors with sharp accents outperform timid, evenly-distributed palettes.

### Layout diversification

**Anti-center bias**
- Centered hero / H1 sections are strictly BANNED when `DESIGN_VARIANCE > 4`. Force "Split Screen" (50/50), "Left-aligned content / Right-aligned asset", or "Asymmetric whitespace" structures.
- When you do center, do it intentionally with massive width — not because you ran out of layout ideas.

**Asymmetric structures**
- Use `margin-top: -2rem` for overlapping cards or images.
- Fractional grid columns: `grid-template-columns: 2fr 1fr 1fr` instead of `grid-cols-3`.
- Generous one-sided whitespace: `padding-left: 20vw` to push content off-center.
- Diagonal flow: items aligned along an invisible diagonal across a section.
- Grid-breaking elements that bleed past the column boundary.

**AIDA reading order on landings**
Every landing-style page MUST follow the AIDA framework:
- **Attention (Hero)** — Cinematic, clean, wide layout.
- **Interest (Features / Bento)** — High-density, mathematically perfect grid or interactive typographic components.
- **Desire (Motion / Media)** — Pinned sections, horizontal scroll, or text-reveals.
- **Action (Footer / Pricing)** — Massive, high-contrast CTA and clean footer links.

Every page begins with a highly creative, premium navigation bar (floating glass pill, minimal split nav, etc.).

### Materiality, shadows, anti-card-overuse (dashboard hardening)

**Dashboard hardening (when `VISUAL_DENSITY > 7`)**
- Generic card containers are strictly BANNED.
- Use logic-grouping via `border-t`, `divide-y`, or purely negative space.
- Data metrics should breathe without being boxed in unless elevation (z-index) is functionally required.

**Card discipline (everywhere)**
- Use cards ONLY when elevation communicates hierarchy.
- When a shadow is used, tint it to the background hue (a card on `#f9fafb` gets a shadow tinted slightly cool, not pure gray-900).
- Use `rounded-[2.5rem]` for major containers in the high-end Bento style.
- Apply diffusion shadows: `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]` — wide-spreading, low-opacity, depth without clutter.

**Card restraint in bento grids**
- 3 to 5 highly intentional, beautifully styled cards beat 8 messy ones every time.
- Fill cards with a mix of large imagery, dense typography, or CSS effects — not three lines of body copy and a button.

### Interactive UI states (mandatory)

LLMs naturally generate "static" successful states. You MUST implement full interaction cycles for every interactive surface:

**Loading**
- Skeletal loaders matching layout sizes. Avoid generic circular spinners.

**Empty states**
- Beautifully composed empty states that indicate HOW to populate data, not just "No items yet."

**Error states**
- Clear, inline error reporting (forms especially). Tell the user what's wrong AND what to do — never "form contains errors."

**Tactile feedback**
- On `:active`, use `-translate-y-[1px]` or `scale-[0.98]` to simulate a physical push indicating success / action.
- On hover, every clickable card and image must react. Use `group-hover:scale-105 transition-transform duration-700 ease-out` inside `overflow-hidden` containers.

### Data & form patterns

**Forms**
- Label sits ABOVE input. Always.
- Helper text is optional but should exist in the markup (even if empty) so error states don't cause layout shift.
- Error text sits BELOW input.
- Use standard `gap-2` for input blocks.
- Buttons in forms get tactile feedback on press.

**Tables**
- Numbers right-aligned in `font-mono`.
- Action columns right-aligned.
- Sticky headers on long tables.
- Empty rows are not collapsed — they show an empty state across the full width.

---

## Creative proactivity (anti-slop implementation)

To actively combat generic AI designs, systematically implement these high-end coding concepts as baseline behaviors, not exotic exceptions.

### Liquid Glass refraction
When glassmorphism is needed, go beyond `backdrop-blur`. Add:
- A 1px inner border: `border-white/10`
- A subtle inner shadow: `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`
- These two layers simulate physical edge refraction. Without them, "glass" reads as "blurred div."

### Magnetic micro-physics (when MOTION_INTENSITY > 5)
Implement buttons that pull slightly toward the mouse cursor.

**Critical:** NEVER use React `useState` for magnetic hover or continuous animations. Use EXCLUSIVELY motion library's `useMotionValue` and `useTransform` outside the React render cycle to prevent performance collapse on mobile.

### Perpetual micro-interactions (when MOTION_INTENSITY > 5)

Embed continuous, infinite micro-animations in standard components (avatars, status dots, backgrounds, hero badges). Apply premium spring physics — no linear easing.

**The five perpetual archetypes:**
- **Pulse** — soft scale or opacity breathing on status indicators and live elements.
- **Typewriter** — multi-step text cycling through complex prompts with a blinking cursor and shimmering "processing" state.
- **Float** — gentle Y-axis drift on hero badges, decorative elements.
- **Shimmer** — horizontal light gradient sliding across skeletal placeholders and active cards.
- **Carousel** — seamless infinite horizontal loop using `x: ["0%", "-100%"]`.

### Spring physics specs
Standard spring for premium feel:
```
{ type: "spring", stiffness: 100, damping: 20 }
```
No linear easing on interactive elements. For UI feedback, use `cubic-bezier(0.16, 1, 0.3, 1)`.

### Layout transitions with layoutId
Always utilize motion library's `layout` and `layoutId` props for smooth re-ordering, resizing, and shared element transitions across state changes. This is the difference between "things move" and "things morph."

### Staggered orchestration
Do not mount lists or grids instantly. Use `staggerChildren` (motion library) or CSS cascade (`animation-delay: calc(var(--index) * 100ms)`) for sequential waterfall reveals.

**Critical:** For `staggerChildren`, the Parent (`variants`) and Children MUST reside in the identical Client Component tree. If data is fetched asynchronously, pass the data as props into a centralized Parent motion wrapper.

### Hover physics
Every clickable card or image reacts on hover:
- Image scale with eased duration inside `overflow-hidden`: `group-hover:scale-105 transition-transform duration-700 ease-out`
- Border or backdrop transitions
- Subtle shadow lift

### Scroll motion patterns (when MOTION_INTENSITY > 7)
- **Scroll pinning** — pin a section title on the left while a gallery scrolls upward on the right.
- **Image scale & fade scroll** — images start at `scale: 0.8`, grow to `scale: 1.0` as they enter view, fade to `opacity: 0.2` as they exit.
- **Scrubbing text reveals** — opacity of central paragraph words starts at `0.1` and scrubs to `1.0` sequentially as the user scrolls.
- **Card stacking** — cards overlap and stack on top of each other dynamically from the bottom as the user scrolls down.

---

## Performance guardrails

These are not optimizations. They are correctness rules. Violating them produces frame drops, dropped touches, and battery drain on real devices.

### DOM cost
Apply grain / noise filters EXCLUSIVELY to fixed, pointer-event-none pseudo-elements (`fixed inset-0 z-50 pointer-events-none`). NEVER apply grain to scrolling containers — it triggers continuous GPU repaints and craters mobile performance.

### Hardware acceleration
Never animate `top`, `left`, `width`, or `height`. Animate exclusively via `transform` and `opacity`. These are the only two properties that hit the compositor without triggering layout.

### Z-index restraint
NEVER spam arbitrary `z-50` or `z-10` unprompted. Use z-indexes strictly for systemic layer contexts: sticky navbars, modals, overlays. A flat document with z-0 is correct most of the time.

### Perpetual motion isolation (critical)
Any perpetual motion or infinite loop MUST be memoized (`React.memo`) and completely isolated in its own microscopic Client Component. Never trigger re-renders in the parent layout. A floating ambient pulse should not re-render the page it lives on.

### Cleanup discipline
Every `useEffect` animation contains strict cleanup. GSAP / WebGL contexts are wrapped in `useEffect` cleanup blocks that kill timelines and dispose contexts.

### Mixing motion libraries
Never mix GSAP / ThreeJS with motion library in the same component tree. Default to motion library for UI / Bento interactions. Use GSAP / ThreeJS EXCLUSIVELY for isolated full-page scrolltelling or canvas backgrounds.

### Horizontal scroll prevention
Wrap the entire page in `<main className="overflow-x-hidden w-full max-w-full">` to absolutely prevent horizontal scrollbars caused by off-screen animations.

---

## AI Tells (forbidden patterns)

Everything in this section is a known generator failure mode. Treat every item as a hard ban unless the user explicitly requests it.

### Visual & CSS
- **No neon / outer glows.** Default `box-shadow` glows and auto-glows are banned. Use inner borders or subtle tinted shadows.
- **No pure black.** `#000000` is banned. Use Off-Black, Zinc-950, or Charcoal.
- **No oversaturated accents.** Desaturate to blend with neutrals.
- **No excessive gradient text.** No text-fill gradients on large headers.
- **No custom mouse cursors.** Outdated, accessibility hostile, performance hit.
- **No `h-screen` for hero.** Use `min-h-[100dvh]`.
- **No flex percentage math.** Use CSS Grid.

### Typography
- **No oversized H1s** that scream just because they're H1s. Control hierarchy with weight and color, not just scale.
- **No serifs on dashboards / software UIs.** Serifs are for editorial / creative contexts.
- **No 6-line wrapped headings.** 2-3 lines maximum. Widen the container.

### Layout & spacing
- **No 3-column equal card layouts.** The generic "3 equal cards horizontally" feature row is BANNED. Use 2-column zig-zag, asymmetric grid, or horizontal scroll.
- **No floating elements with awkward gaps.** Padding and margins are mathematically perfect.
- **No cramped sections.** Marketing sections use `py-32 md:py-48` minimum.
- **No center-everything layouts** with no visual hierarchy.
- **No cookie-cutter hero** with left-text right-image as a default reach.

### Content & data ("The Jane Doe Effect")
- **No generic names.** "John Doe", "Sarah Chan", "Jack Su", "Jane Smith" — banned. Use creative, realistic-sounding names that fit the product's market.
- **No generic avatars.** No standard SVG "egg" silhouettes. No default Lucide user icons. Use creative, believable photo placeholders or specific styling.
- **No fake numbers.** "99.99%", "50%", "1234567" — banned. Use organic, messy data: `47.2%`, `+1 (312) 847-1928`, `$8,247.30`.
- **No startup slop names.** "Acme", "Nexus", "SmartFlow", "Vertex", "Apex" — banned. Invent premium, contextual brand names that match the project's industry.
- **No filler verbs.** "Elevate", "Seamless", "Unleash", "Next-Gen", "Empower", "Revolutionize" — banned. Use concrete verbs that describe what the product actually does.
- **No "Lorem ipsum"** or "Your text here" or placeholder content. When a mockup exists, extract text from it. Otherwise, generate realistic content based on the brief.

### External resources
- **No broken Unsplash links.** Use absolute, reliable placeholders: `https://picsum.photos/seed/{keyword}/1920/1080` (match keyword to vibe). Apply sophisticated CSS filters: `grayscale`, `mix-blend-luminosity`, `opacity-90`, `contrast-125` so they read as deliberate, not stock.
- **No emoji as visual elements.** Anywhere. Code, comments, markup, alt text, UI strings. Use SVG icons or text.

### Components
- **No generic 3-column feature grids.** See layout bans above.
- **No generic testimonial sections.** Testimonials get specific, named, real-feeling people with portrait composition and minimalist typography quotes, controlled by subtle arrows or a carousel.
- **No rounded-corner cards with drop shadows as default.** Cards earn their elevation.
- **No "Get Started" / "Learn More" CTAs** unless they're in the mockup. Specific verbs: "Run the demo", "See the dashboard", "Try a sample partner."
- **No decorative blobs / waves / geometric patterns** not in the mockup.
- **No stock photo placeholder divs.**
- **No arbitrary floating stamp / badge icons on hero text.**
- **No pill-tags under the hero.**
- **No raw data / stats dumped in the hero.**

### Meta-labels
- **No "SECTION 01" / "SECTION 04" / "QUESTION 05" / "ABOUT US"** as label decoration. Banned forever. Remove them entirely. They are amateur-tier signposting that signals AI generation.

### shadcn / ui
- You may use `shadcn/ui`, but NEVER in its generic default state. Customize the radii, colors, shadows to match the high-end project aesthetic. Default shadcn is a known AI tell.

### Banned default behaviors
- **No purple gradients on white as default.**
- **No center-everything fallback.**
- **No three equal cards as the feature row default.**
- **No left-text right-image as the default hero.**

---

## The Creative Arsenal

Pull from this library of advanced concepts to ensure output is visually striking and memorable. Use the dials and product type to select; don't reach for the same patterns reflexively.

### Hero paradigms

Stop defaulting to centered text over a dark image. Force one of these:

- **Cinematic Center (preferred default)** — Text perfectly centered, massive width, ultra-wide H1 container. Exactly two high-contrast CTAs below the text. Behind everything, a stunning full-bleed background image with a dark radial wash. Buttons perfectly legible — dark background gets white text, light background gets dark text.
- **Artistic Asymmetry** — Text offset to the left. An artistic floating image overlapping the text from the bottom right. Generous negative space.
- **Editorial Split** — Text left, image right, but with massive negative space between. The split is not 50/50 — it's 60/40 or 65/35 with breathing room.
- **Asymmetric Hero with Stylistic Fade** — High-quality relevant background image with a subtle stylistic fade (darkening or lightening into the page background depending on light or dark mode). Text aligned cleanly left or right.

### Navigation & menus
- **Mac OS Dock Magnification** — Navbar at the edge with icons that scale fluidly on hover, neighbors growing proportionally less.
- **Magnetic Button** — Buttons that physically pull toward the cursor as it approaches.
- **Gooey Menu** — Sub-items that detach from the main button like viscous liquid.
- **Dynamic Island** — Pill-shaped UI component that morphs to show status / alerts. Pop-up notification badge that emerges with overshoot spring, stays 3 seconds, vanishes.
- **Contextual Radial Menu** — Circular menu expanding exactly at the click coordinates.
- **Floating Speed Dial** — FAB that springs out into a curved line of secondary actions.
- **Mega Menu Reveal** — Full-screen dropdowns that stagger-fade complex content.
- **Floating Glass Pill Nav** — Liquid Glass treatment on a centered floating pill at the top.
- **Minimal Split Nav** — Logo left, primary actions right, single accent on the active item.

### Layout & grids
- **Bento Grid** — Asymmetric, tile-based grouping. Apple Control Center as the reference. Cards earn their span by content density.
- **Masonry Layout** — Staggered grid without fixed row heights.
- **Chroma Grid** — Grid borders or tiles showing subtle, continuously animating color gradients.
- **Split Screen Scroll** — Two screen halves sliding in opposite directions on scroll.
- **Curtain Reveal** — Hero section parting in the middle like a curtain on scroll.

### Cards & containers
- **Parallax Tilt Card** — 3D-tilting card tracking the mouse coordinates within its bounding box.
- **Spotlight Border Card** — Card borders illuminate dynamically under the cursor's proximity.
- **Glassmorphism Panel** — True frosted glass with inner refraction borders (the Liquid Glass spec above).
- **Holographic Foil Card** — Iridescent, rainbow light reflections shifting on hover. Use for premium / collectible contexts.
- **Tinder Swipe Stack** — Physical stack of cards the user can swipe away horizontally.
- **Morphing Modal** — Button that seamlessly expands into its own full-screen dialog container using `layoutId`.

### Scroll animations
- **Sticky Scroll Stack** — Cards that stick to the top and physically stack over each other as the user scrolls.
- **Horizontal Scroll Hijack** — Vertical scroll input translates into smooth horizontal gallery pan.
- **Locomotive Sequence** — Video / 3D sequences where framerate is tied directly to the scrollbar position.
- **Zoom Parallax** — Central background image zooming in / out seamlessly as you scroll.
- **Liquid Swipe Transition** — Page transitions that wipe the screen like viscous liquid.

### Galleries & media
- **Dome Gallery** — 3D gallery feeling like a panoramic dome surrounding the viewer.
- **Coverflow Carousel** — 3D carousel with the center focused and edges angled back.
- **Drag-to-Pan Grid** — Boundless grid the user can freely drag in any compass direction.
- **Accordion Image Slider** — Narrow vertical or horizontal image strips that expand fully on hover.
- **Hover Image Trail** — Mouse leaves a trail of popping / fading images behind it.
- **Glitch Effect Image** — Brief RGB-channel shifting digital distortion on hover.

### Typography & text
- **Kinetic Marquee** — Endless text bands that reverse direction or speed up on scroll. Use authentic typography or icons, not lorem placeholders.
- **Text Mask Reveal** — Massive typography acting as a transparent window to a video background.
- **Text Scramble Effect** — Matrix-style character decoding on load or hover.
- **Circular Text Path** — Text curved along a spinning circular path.
- **Gradient Stroke Animation** — Outlined text with a gradient continuously running along the stroke.
- **Kinetic Typography Grid** — Grid of letters dodging or rotating away from the cursor.
- **Inline Typography Images** — Embed small, pill-shaped images directly INSIDE massive headings: `I shape <span class="inline-block w-24 h-10 rounded-full align-middle bg-cover bg-center mx-2" style="background-image: url(...)"></span> digital spaces.`
- **Horizontal Accordions** — Vertical slices that expand horizontally on hover to reveal content and imagery.
- **Infinite Marquee (Trusted Partners)** — Smooth continuously scrolling rows of authentic icons or large typography.
- **Feedback / Testimonial Carousel** — Overlapping portrait images next to minimalist typography quotes, controlled by subtle arrows.

### Micro-interactions & effects
- **Particle Explosion Button** — CTAs that shatter into particles upon success state confirmation.
- **Liquid Pull-to-Refresh** — Mobile reload indicators that act like detaching water droplets.
- **Skeleton Shimmer** — Shifting light reflections moving across placeholder boxes.
- **Directional Hover Aware Button** — Hover fill that enters from the exact side the mouse entered from.
- **Ripple Click Effect** — Visual waves rippling precisely from the click coordinates.
- **Animated SVG Line Drawing** — Vectors that draw their own contours in real-time.
- **Mesh Gradient Background** — Organic, lava-lamp-like animated color blobs.
- **Lens Blur Depth** — Dynamic focus blurring background UI layers to highlight a foreground action.

### Bento 2.0 — the Motion-Engine paradigm

When generating modern SaaS dashboards or feature sections, use this architecture. It enforces a "minimalist-with-soul" aesthetic heavily reliant on perpetual physics.

**Core philosophy**
- Aesthetic: high-end, minimal, functional.
- Palette: background `#f9fafb`. Cards pure white `#ffffff` with `border-slate-200/50` (1px).
- Surfaces: `rounded-[2.5rem]` for major containers.
- Shadows: diffusion shadow `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`.
- Typography: strict `Geist`, `Satoshi`, or `Cabinet Grotesk`. Subtle tracking (`tracking-tight`) for headers.
- Labels: titles and descriptions placed OUTSIDE and BELOW cards for clean gallery presentation.
- Padding: generous `p-8` or `p-10` inside cards.

**Animation engine**
- Spring physics: `{ type: "spring", stiffness: 100, damping: 20 }`.
- Layout transitions: heavy use of `layout` and `layoutId` props.
- Infinite loops: every card has an "Active State" that loops infinitely.
- Performance: wrap dynamic lists in `<AnimatePresence>`. Memoize. Isolate to leaf Client Components.

### The 5 card archetypes

Use these specific micro-animations when constructing Bento grids. A common arrangement: Row 1 with 3 columns, Row 2 with 2 columns split 70/30.

1. **The Intelligent List** — Vertical stack of items with an infinite auto-sorting loop. Items swap positions using `layoutId`, simulating an AI prioritizing tasks in real-time.
2. **The Command Input** — Search / AI bar with a multi-step typewriter effect. Cycles through complex prompts. Includes a blinking cursor and a "processing" state with a shimmering loading gradient.
3. **The Live Status** — Scheduling interface with "breathing" status indicators. Pop-up notification badge that emerges with overshoot spring, holds for 3 seconds, vanishes cleanly.
4. **The Wide Data Stream** — Horizontal infinite carousel of data cards or metrics. Loop is seamless via `x: ["0%", "-100%"]` at a speed that feels effortless (15-25s typical).
5. **The Contextual UI (Focus Mode)** — Document view that animates a staggered highlight of a text block, followed by a float-in of a floating action toolbar with micro-icons.

---

## Pre-flight checklist

Run this matrix before outputting any code. Last filter before ship.

**Architecture**
- [ ] Framework matches the project (RSC where applicable, Client Component isolation for interactive surfaces).
- [ ] Dependency verification done — `package.json` checked, install commands provided for missing libraries.
- [ ] Tailwind version matches `package.json`. No v4 syntax in v3 projects.
- [ ] Global state is justified — used to avoid deep prop-drilling, not arbitrarily.

**Viewport & responsiveness**
- [ ] Hero sections use `min-h-[100dvh]`, not `h-screen`.
- [ ] Page is wrapped in `overflow-x-hidden w-full max-w-full` if motion is used.
- [ ] Mobile collapse is enforced for high-variance layouts: `w-full`, `px-4`, `max-w-7xl mx-auto`.
- [ ] Breakpoint behavior at 375px, 768px, 1024px, 1440px is intentional.

**Hero math**
- [ ] H1 uses an ultra-wide container (`max-w-5xl` or wider).
- [ ] H1 is 2-3 lines max. Verified mentally with the actual copy.
- [ ] No floating stamp / badge icons on hero text.
- [ ] No pill tags under the hero.
- [ ] No raw stats in the hero.
- [ ] Button text contrast is perfect (dark bg = white text, light bg = dark text).

**Layout**
- [ ] Bento grids use `grid-flow-dense`. No empty cells, no missing corners.
- [ ] Bento card count is 3-5, not 8.
- [ ] No center-everything fallback unless intentional.
- [ ] Section padding is `py-32 md:py-48` on marketing.
- [ ] Sections feel like distinct cinematic chapters, not cramped slabs.
- [ ] No 3-equal-card feature rows.

**Typography**
- [ ] Display font is distinctive (not the default reflex).
- [ ] Dashboard / software UI uses Sans pairings, no serifs.
- [ ] Numbers in cockpit-density contexts use `font-mono`.
- [ ] Body line length capped at `max-w-[65ch]`.

**Color**
- [ ] Max 1 accent color. Saturation < 80%.
- [ ] No pure `#000000`.
- [ ] No purple-to-blue gradients on white.
- [ ] Warm OR cool grays — not both.

**Motion**
- [ ] Perpetual loops are isolated to their own memoized Client Components.
- [ ] Animations use `transform` and `opacity` only.
- [ ] Spring physics on interactive elements, not linear easing.
- [ ] Staggered orchestration on list / grid mounts.
- [ ] `useEffect` animations have cleanup functions.
- [ ] Grain / noise is on fixed pointer-event-none pseudo-elements.
- [ ] `prefers-reduced-motion` respected.
- [ ] Mobile reduces motion intensity by 2 levels.

**States**
- [ ] Loading states use skeletal loaders matching layout.
- [ ] Empty states explain how to populate, not just "nothing here."
- [ ] Error states are inline, specific, with a fix.
- [ ] Tactile feedback on `:active` (translate or scale).
- [ ] Hover physics on every clickable card / image.

**Content**
- [ ] No generic names ("John Doe").
- [ ] No "Acme / Nexus" filler brand names.
- [ ] No "Elevate / Seamless / Unleash" filler verbs.
- [ ] No fake numbers ("99.99%", "50%").
- [ ] No Lorem ipsum or placeholder text.
- [ ] No emojis anywhere.
- [ ] No "SECTION 01" meta-labels.
- [ ] CTAs are specific verbs, not "Get Started" reflexively.

**External resources**
- [ ] Images use `picsum.photos/seed/{keyword}/W/H` or equivalent reliable source.
- [ ] No Unsplash URLs.
- [ ] Image filters applied so they don't read as stock (grayscale, mix-blend, contrast).

**Performance**
- [ ] No `top` / `left` / `width` / `height` animations.
- [ ] No arbitrary `z-50` spam.
- [ ] Z-indexes only for systemic layers (nav, modal, overlay).
- [ ] GSAP / WebGL cleanup blocks in place.
- [ ] No GSAP + motion library in the same component tree.

**Component cleanliness**
- [ ] No default shadcn / ui — radii, colors, shadows customized.
- [ ] Code is clean, visually striking, memorable, refined in every detail.
- [ ] Cards omitted in favor of spacing where possible.

---

## Strict bans by category

A consolidated reference for the hard bans. Violation = blocker.

### Meta-labels
- "SECTION 01", "SECTION 04", "QUESTION 05", "ABOUT US", "OUR PROCESS 02" — banned forever. Strip them entirely.

### Typography
- Inter is acceptable as a corrected position. Earlier guidance banned it; current direction permits it. Use it deliberately, not reflexively. Vary across generations.
- Arial, Roboto, generic system fonts as primary display — banned.
- Serif on dashboards / software UIs — banned.
- Oversized H1s that scream just because — banned. Use weight and color.

### Naming
- "John Doe", "Sarah Chan", "Jack Su", "Jane Smith" — banned. Use realistic names that fit the product's market.
- "Acme", "Nexus", "SmartFlow", "Vertex", "Apex" — banned. Invent contextual brand names.
- "Elevate", "Seamless", "Unleash", "Next-Gen", "Empower", "Revolutionize" — banned verbs. Use concrete language.

### Numbers
- "99.99%", "50%", "1234567" — banned. Use organic values: `47.2%`, `+1 (312) 847-1928`, `$8,247.30`.

### External
- Unsplash URLs — banned. Use `picsum.photos/seed/{keyword}/W/H`.
- Custom mouse cursors — banned.

### Visual
- Pure `#000000` — banned. Use Off-Black / Zinc-950 / Charcoal.
- Purple-blue gradients on white — banned.
- Default `shadcn/ui` without customization — banned.

### Layout
- 3-equal-card feature rows — banned.
- Center-everything as a fallback — banned.
- Cramped sections (`py-12` on marketing) — banned. Use `py-32 md:py-48`.
- `h-screen` for hero — banned. Use `min-h-[100dvh]`.
- Flex percentage math (`w-[calc(33%-1rem)]`) — banned. Use Grid.

---

## Page structure rules

### AIDA reading order on landings
Every landing-style page MUST follow this sequence:
1. Premium navigation bar (floating glass pill, minimal split nav, etc.) — first paint.
2. **Attention** — hero with ultra-wide H1, 2-3 lines max, 2 high-contrast CTAs.
3. **Interest** — bento grid or interactive typographic component density.
4. **Desire** — motion / scroll-driven section (pinned, scrubbed, stacked).
5. **Action** — high-contrast CTA + clean footer.

### Ultra-wide containers
H1s use `max-w-5xl`, `max-w-6xl`, or `w-full`. Section containers use `max-w-7xl mx-auto` or `max-w-[1400px] mx-auto`. The H1 container width is what prevents 6-line wraps — narrower containers reflexively cause failure.

### The 2-line H1 rule
H1 must NEVER exceed 2 to 3 lines. 4 lines is failure. 5 is catastrophic. 6 is disqualifying.

To enforce:
- Widen the container first (`max-w-6xl` over `max-w-2xl`).
- Reduce the font with clamp: `clamp(3rem, 5vw, 5.5rem)`.
- Re-check at 375px, 768px, 1024px, 1440px.

### Section spacing
Marketing sections: `py-32 md:py-48` minimum. Sections must feel like distinct cinematic chapters. Cramming kills the editorial energy that distinguishes premium work from AI slop.

### The billboard test
Every page is a billboard going by at 60 mph. Cover everything except navigation — can you still identify the site, the page, and the major sections? If not, navigation has failed. Visual hierarchy must announce itself without reading.

### Conventions over cleverness
Logo top-left. Nav top or left. Search = magnifying glass. Don't innovate on navigation patterns to be clever. Innovate when you KNOW you have a better idea; otherwise honor convention so users can scan.

### Make clickable things obviously clickable
No relying on hover states for discoverability, especially on mobile where hover doesn't exist. Shape, location, and formatting (color, underline) must signal clickability without interaction.

### Eliminate noise
Three sources of noise: shouting (too many things demanding attention), disorganization (things not grouped logically), clutter (too much stuff). Fix noise by removal, not addition. Start with the assumption every element is visual noise — guilty until proven innocent.

### Clarity over consistency
If making something significantly clearer requires making it slightly inconsistent, choose clarity every time.

---

## Side scroll progress paths — forbidden

NEVER use scroll progress paths on the side of the page. No fixed-position SVG drawing lines down the left or right edge as the user scrolls. No vertical progress indicators glued to the viewport edge. This is a known stale pattern that signals AI generation and adds visual noise without information value.

If progress feedback is needed, integrate it into the navigation bar (horizontal top progress bar) or into section anchors (active state on nav links as sections enter view), not as a parasitic edge element.

---

## Icons

Primary icon system: Google Material Symbols. Use the variable font with `font-variation-settings` to control fill, weight, grade, and optical size.

```html
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;">
  search
</span>
```

```html
<span class="material-symbols-rounded" style="font-variation-settings: 'FILL' 1, 'wght' 500, 'GRAD' 0, 'opsz' 40;">
  notifications
</span>
```

Variation axes:
- `FILL` — 0 (outlined) or 1 (filled). Use filled for active / selected states, outlined for resting states.
- `wght` — 100 to 700. Match the surrounding type weight.
- `GRAD` — -25, 0, or 200. Subtle thickness adjustment.
- `opsz` — 20, 24, 40, 48. Optical size; match the rendered pixel size.

Secondary fallbacks (use only when Material Symbols isn't appropriate for the brand):
- **Phosphor** — `@phosphor-icons/react`. Six weights, friendly geometric.
- **Radix Icons** — `@radix-ui/react-icons`. Minimal, neutral, system-friendly.
- **Lucide** — `lucide-react`. Crisp, technical, 1.5-2px stroke.

Standardize stroke width across the entire output. Pick `1.5` or `2.0` and commit — mixing weights is a visible AI tell.

Never replace symbols with emojis. Ever.

---

## Closing principle

The output you generate should be indistinguishable from work by a senior frontend designer who has spent a decade getting paid to defeat their own biases. Every directive in this document exists because the default generator behavior fails in a specific, measurable way. The rules are not stylistic — they are corrections for known failure modes.

Match implementation complexity to aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well — not from picking the most elaborate vision available.

Pick a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work. Intentionality is the differentiator, not intensity.

Don't hold back. Show what's possible when you commit fully to a distinctive vision.
