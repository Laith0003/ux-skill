# The Creative Arsenal — Pattern Library

60+ high-end UI patterns to reach for — the opposite of anti-slop. Asymmetric split heroes, bento grids, spotlight border cards, magnetic micro-physics, kinetic typography, the 5 dashboard archetypes. Each pattern: when to use, what it costs, how to ship at 60fps.

This is the affirmative library. The anti-slop ban list says what not to do; this document says what to reach for instead. Every pattern is named, scoped, costed, and explained. Use this on greenfield design, on redesigns, on review feedback ("this section needs a spotlight border treatment"). Combine patterns intentionally — not all of them at once.

The patterns are organized by surface: hero & landing, navigation, layout & grid, cards, scroll animation, typography, micro-interaction, imagery, dashboards. The last two sections cover combinations that work together and combinations that fight.

---

## How to Use This Library

**Pick 2-4 patterns per design.** A landing page using twelve patterns from this list looks busy and uncoordinated. The strongest designs pick a small number and execute them at high craft. The discipline is in the restraint.

**Match patterns to brief.** Editorial brands lean into asymmetric layouts and kinetic typography. Product-led brands lean into bento grids and spotlight border cards. Brutalist brands lean into broken grids and aggressive type. Don't mix tones without a reason.

**Verify 60fps before shipping.** Animation patterns that look great in a designer's tool drop frames in production. Test on a mid-range Android. If a pattern can't ship at 60fps, downgrade it or remove it.

**Cost matters.** Every pattern has implementation cost (engineering hours), runtime cost (rendering performance), and maintenance cost (ongoing complexity). The cost is annotated below. Cheap patterns can be everywhere; expensive patterns are accents.

**Combinations matter.** A bento grid plus spotlight border cards plus a magnetic primary CTA reinforces each other. A bento grid plus aggressive scroll hijack plus kinetic marquee fights itself. The final section covers what combines.

---

## Hero and Landing Patterns

### Asymmetric Split Hero

**Pattern.** The hero divides into two unequal columns — typically 60/40 or 70/30 — with copy on one side and imagery on the other. The asymmetry breaks the symmetric-centered default and reads as editorial.

**When to use.** Product launches, marketing pages, brand sites where you have one strong image (product, person, illustration) and one strong message. Works particularly well when the image has internal asymmetry that complements the layout.

**Cost.** Low. Single CSS grid with two unequal columns.

**Ship at 60fps.** Trivial — static layout.

**Anti-pattern to avoid.** 50/50 splits read as symmetric and lose the editorial quality.

---

### Editorial Column Rhythm

**Pattern.** Vary column widths and heights through the page to create a magazine-like rhythm. One section is 8+4. The next is 5+7. The next is full-bleed. The variation creates pace.

**When to use.** Long-scroll landing pages, brand stories, content-heavy marketing sites where the content varies in importance and shape.

**Cost.** Low to medium. Requires more layout iterations than a uniform grid.

**Ship at 60fps.** Trivial — static layout.

---

### Bento Grid

**Pattern.** A grid composed of cells with varied row and column spans, packed densely without visible gaps between cells (or with very narrow gaps). Each cell holds a self-contained piece of content — a feature, a stat, a screenshot, a quote.

**When to use.** Feature overviews, product summaries, dashboard composition, "everything you need to know" sections. Excellent for letting one large cell anchor and several smaller cells surround.

**Cost.** Medium. Requires careful content planning (each cell needs distinct content). CSS grid handles the structure.

**Ship at 60fps.** Trivial — static layout. Add hover interactions per cell for polish.

**Anti-pattern to avoid.** All cells the same size (becomes a regular grid). All content the same shape (loses the bento quality).

---

### Masonry Layout

**Pattern.** A grid where columns are fixed in width but rows are variable — each item fills its natural height, and shorter items pack tightly while taller items extend. Pinterest is the canonical example.

**When to use.** Image galleries, blog post previews, varied-content lists where uniform card heights would force cropping or padding.

**Cost.** Medium. CSS `column-count` is simple but limits interaction; CSS grid with `grid-auto-flow: dense` is more flexible.

**Ship at 60fps.** Trivial for static. Lazy-load images for long lists.

---

### Curtain Reveal Hero

**Pattern.** The hero begins with a solid color or simple state. As the user scrolls (or after a brief delay), a curtain — solid color, gradient, image — slides aside to reveal the content beneath.

**When to use.** Brand-led pages where the moment of reveal carries weight. Product launches. Campaign sites.

**Cost.** Medium. Requires careful animation timing and a fallback for users with reduced motion preferences.

**Ship at 60fps.** Animate `transform: translateY()` or `clip-path` only. Never animate width/height.

---

### Cinematic Center

**Pattern.** Hero is a single visual statement — usually a high-quality image or video — with a small amount of typography overlaid. The image dominates; the copy is restrained.

**When to use.** Brand-first pages. Sites where the imagery sells the story (luxury goods, hospitality, travel, fashion).

**Cost.** Medium for static, high for video. Imagery quality is paramount — a stock photo undoes the pattern.

**Ship at 60fps.** Trivial for image. Video: compress aggressively, lazy-load.

---

### Artistic Asymmetry

**Pattern.** Elements placed off-grid, at unusual angles, or with intentional misalignment. The composition reads as designed by a hand, not a system.

**When to use.** Brand sites for studios, designers, artists, or boutique products. Editorial features. Manifestos.

**Cost.** High. Every element is positioned manually; responsive breakpoints multiply the work.

**Ship at 60fps.** Trivial — static composition.

**Anti-pattern to avoid.** Random misalignment that reads as broken layout rather than intentional asymmetry. The composition must still feel composed.

---

### Editorial Split (60/40 Hero)

**Pattern.** A specific variant of asymmetric split: the dominant side (60%) carries the imagery or video; the secondary side (40%) carries the message, with small but confident typography.

**When to use.** Modern brand pages, product-led marketing, anywhere the image is the lead and copy supports.

**Cost.** Low.

**Ship at 60fps.** Trivial.

---

### Thesis-Statement Hero

**Pattern.** Hero is purely typography — a single thesis statement set in large, confident type, occupying most of the screen. No imagery, no decoration, just words. The Apple "Think Different" tradition.

**When to use.** Brand-led pages where the message is the product. Editorial sites. Manifestos. Conference sites.

**Cost.** Low to medium. The typography must be excellent. The statement must be excellent. Both bars are high.

**Ship at 60fps.** Trivial.

---

### AIDA Flow Landing

**Pattern.** Structured around the classic Attention-Interest-Desire-Action model. Hero grabs attention. Below hero, interest-building content (what the product does, how it works). Below that, desire-building content (testimonials, case studies, screenshots). Footer CTA captures action.

**When to use.** Conversion-focused landing pages. Sites where the funnel is the goal.

**Cost.** Medium. Each section needs distinct content and treatment.

**Ship at 60fps.** Trivial — static composition with scroll animations as polish.

---

## Navigation Patterns

### Floating Glass Pill Nav

**Pattern.** Top navigation as a pill-shaped element floating above the page, with frosted glass background (`backdrop-filter: blur`), rounded corners, and translucency. The pill detaches from the page edges and feels light.

**When to use.** Premium product sites. Brand pages. Anywhere the chrome should feel weightless.

**Cost.** Low.

**Ship at 60fps.** Trivial. `backdrop-filter` has a render cost; test on lower-end devices.

---

### Minimal Split Nav

**Pattern.** Navigation split into two halves — brand mark and primary nav on the left, user actions and CTAs on the right. Whitespace dominates the middle. Restraint is the signal.

**When to use.** Editorial sites. Premium products. Anywhere the goal is to recede.

**Cost.** Low.

**Ship at 60fps.** Trivial.

---

### Dock Magnification

**Pattern.** A dock of icons (like macOS dock) where the icon under the cursor magnifies, with neighbors smoothly tweening to lesser magnification. Pure macOS feel.

**When to use.** Tool bars, action sets, anywhere the user has a fixed set of icons and needs to identify them at a glance.

**Cost.** Medium. Requires JS for the magnification curve.

**Ship at 60fps.** Animate `transform: scale()` only. Use `requestAnimationFrame`. Throttle pointer events.

---

### Morphing Status Pill

**Pattern.** A pill in the navigation that morphs to communicate state — search bar expands from a magnifying glass icon, login pill morphs to show user avatar after sign-in, notification pill expands when new notification arrives.

**When to use.** Apps where state changes are first-class. Productivity tools. Communication products.

**Cost.** Medium. Requires JS for state transitions and CSS for morph timing.

**Ship at 60fps.** Animate `width`, `padding`, `border-radius` only — and only on transitions. Don't keep them animating.

---

### Magnetic Button

**Pattern.** Button that subtly tracks the cursor as it approaches, "leaning" toward the cursor by a few pixels. The effect is barely perceptible but feels organic.

**When to use.** Primary CTAs in hero. Sparingly — once per page maximum.

**Cost.** Medium. Requires JS pointer tracking.

**Ship at 60fps.** Use `transform: translate()` and `requestAnimationFrame`. Limit to a 4-8px range; larger feels uncanny.

---

### Button-in-Button Bezel

**Pattern.** A button with an inner button or pill — primary CTA with a small icon-button inside it ("Get started → arrow icon" where the arrow is a clickable secondary affordance). The bezel effect adds depth without shadow.

**When to use.** Primary CTAs that bundle two actions (primary + reveal preview, primary + see pricing).

**Cost.** Low.

**Ship at 60fps.** Trivial.

---

## Layout and Grid Patterns

### Split-Screen Scroll

**Pattern.** Two columns side by side. One scrolls normally; the other is sticky and updates as the scrolling column passes key sections. The sticky column might show an image, a video, a code sample, a phone mockup — content that should anchor while the explanation scrolls.

**When to use.** Product walkthroughs where one side explains and the other side illustrates. Documentation. Step-by-step content.

**Cost.** Medium. Requires `position: sticky` and JS to update the sticky content on scroll.

**Ship at 60fps.** Use `IntersectionObserver` to detect scroll positions. Avoid scroll-tied animations on the sticky content.

---

### Chroma Grid

**Pattern.** A grid where each cell has a distinct accent color — pulled from a brand palette or a generated harmonious scheme. Cells with the same content type share the same color; the grid reads as both organized and vibrant.

**When to use.** Portfolios, product feature grids, category navigation, anywhere a varied grid benefits from color-coded grouping.

**Cost.** Low.

**Ship at 60fps.** Trivial — static color application.

---

### Sticky Scroll Stack

**Pattern.** Sections stack on scroll. As each new section enters the viewport, the previous section is pinned beneath it, creating a layered effect. Each section is fully visible at peak; transitions happen at the edges.

**When to use.** Storytelling pages, brand sites, immersive content. Particularly effective for product feature reveals where each feature gets its moment.

**Cost.** High. Requires careful scroll-position management and `position: sticky` choreography.

**Ship at 60fps.** Use `IntersectionObserver` for trigger points. Animate only `transform` and `opacity`. Avoid mixing with parallax (the combination fights itself).

---

### Mosaic Layout

**Pattern.** A grid of cells with varied sizes and shapes (rectangles, large squares, narrow strips). Each cell holds a self-contained piece of content. Similar to bento but with more shape variation and less density.

**When to use.** Gallery pages, portfolio overviews, magazine-style indexes.

**Cost.** Medium.

**Ship at 60fps.** Trivial.

---

### Broken Grid

**Pattern.** A grid that intentionally breaks — elements overlap, sit off-axis, extend beyond cell boundaries. The grid is implied, not strictly enforced.

**When to use.** Brutalist designs. Editorial features. Brand sites where convention-breaking is the brand.

**Cost.** High. Each breakage is hand-placed; responsive design is harder.

**Ship at 60fps.** Trivial — static.

---

## Card Patterns

### Parallax Tilt Card

**Pattern.** Card that tilts in 3D in response to cursor position. As the cursor moves across the card, the card rotates subtly along X and Y axes, creating a sense of depth.

**When to use.** Feature cards in heroes. Product cards. Anywhere a single card deserves attention.

**Cost.** Medium. Requires JS pointer tracking and CSS 3D transforms.

**Ship at 60fps.** Use `transform: perspective() rotateX() rotateY()`. Throttle pointer events with `requestAnimationFrame`. Disable on touch devices.

**Caveat.** Never use DeviceOrientation/DeviceMotion APIs to drive this on mobile. Cursor only. The pattern degrades gracefully to static on touch.

---

### Spotlight Border Card

**Pattern.** Card with a subtle border that reveals a gradient highlight following the cursor as it moves across the card. The card's body stays still; only the border lights up.

**When to use.** Feature card grids. Pricing tiers. Bento grid cells where you want to add interactive polish without busying the layout.

**Cost.** Medium. CSS-only implementation possible with conic gradients and CSS variables tied to pointer position.

**Ship at 60fps.** Update CSS variables via pointer events with `requestAnimationFrame`. The render path stays on the GPU.

---

### Glassmorphism Card

**Pattern.** Card with frosted glass background — translucent fill, backdrop blur, subtle border. The card layers over a colorful or busy background and lets some of it through.

**When to use.** One element per page maximum. Premium product surfaces. Hero overlays.

**Cost.** Low.

**Ship at 60fps.** `backdrop-filter` is GPU-accelerated but has a render cost. Test on lower-end hardware. Limit to one or two glass elements simultaneously.

---

### Holographic Foil Card

**Pattern.** Card with an iridescent foil effect — a conic or linear gradient with multiple stops creating a holographic shimmer that shifts as the user tilts (cursor-driven on desktop).

**When to use.** Premium product pages, collectible products, special editions. Sparingly.

**Cost.** Medium.

**Ship at 60fps.** Use CSS conic gradients and `transform`. No image dependencies; pure CSS.

---

### Tinder Swipe Card

**Pattern.** Card that can be swiped left or right to dismiss or accept. The card rotates as it leaves the stack; the next card scales up underneath. Originally Tinder, now everywhere.

**When to use.** Mobile-first decision flows. Onboarding card stacks. Quick triage.

**Cost.** Medium to high. Requires gesture handling, animation choreography, and accessible alternatives (keyboard, buttons).

**Ship at 60fps.** Use `transform` for movement and rotation. Use `pointermove` events. Test on touch devices.

---

### Morphing Modal

**Pattern.** When a card is clicked, the card itself expands and morphs into a modal — instead of the modal appearing from nowhere and the card staying behind. The user's eye follows the transformation.

**When to use.** Cards that link to detailed views. Photo galleries. Product detail expansions.

**Cost.** Medium. Requires layout coordination between the card and modal states.

**Ship at 60fps.** Animate `transform`, `position`, and `opacity`. Use the FLIP technique (First, Last, Invert, Play).

---

### Liquid Glass Card

**Pattern.** Card whose background subtly distorts the content behind it — a refractive glass effect simulating real glass thickness. Uses CSS `filter` or WebGL for the distortion.

**When to use.** Premium product surfaces. Hero feature cards. Sparingly.

**Cost.** High. CSS-only is limited; WebGL is heavier but more flexible.

**Ship at 60fps.** Use GPU-accelerated filters. Limit to one or two elements simultaneously.

---

## Scroll Animation Patterns

### Horizontal Scroll Hijack

**Pattern.** A section that, when entered, converts vertical scroll into horizontal scroll. The user keeps scrolling down (or using arrow keys) but the section moves sideways, revealing horizontal content. Once the section is exhausted, vertical scroll resumes.

**When to use.** Storytelling sections. Portfolio walkthroughs. Timeline reveals.

**Cost.** High. Requires scroll-position management, accessibility considerations, and careful UX (some users find scroll hijacking disorienting).

**Ship at 60fps.** Use `transform: translateX()`. Avoid animating the actual scroll position.

**Caveat.** Always provide a non-hijacked alternative path. Hijacking is friction; use it for storytelling, not for primary navigation.

---

### Locomotive Sequence

**Pattern.** Smooth scroll with momentum, plus elements that animate based on scroll position. Inspired by Locomotive Scroll library work. Elements drift, fade, scale based on scroll velocity and position.

**When to use.** Premium brand sites. Editorial features. Atmosphere over function.

**Cost.** High. Requires a custom scroll system and careful tuning.

**Ship at 60fps.** Use a virtual scroll system that animates `transform` on a container. Avoid animating each element separately.

---

### Zoom Parallax

**Pattern.** As the user scrolls past a hero image or section, the image zooms in (or out) subtly, creating depth without horizontal movement.

**When to use.** Hero sections. Feature reveals. Brand pages where the image is the lead.

**Cost.** Low. CSS `transform: scale()` tied to scroll position.

**Ship at 60fps.** Use `IntersectionObserver` and `requestAnimationFrame`. Animate `transform: scale()` only.

---

### Liquid Swipe

**Pattern.** Section transitions via a liquid wipe — one section blends into the next via a fluid mask, not a hard cut.

**When to use.** Onboarding flows. Carousel transitions. Story-driven content.

**Cost.** Medium. SVG mask or WebGL.

**Ship at 60fps.** SVG mask animation can stay on GPU with care. WebGL is more flexible but heavier.

**Anti-pattern.** Do not use scroll-progress paths (snake-like SVG drawn alongside scroll). They are visually busy, semantically empty, and have been overused to the point of cliché.

---

## Typography Patterns

### Kinetic Marquee

**Pattern.** A horizontal marquee of large text, scrolling slowly. Words pass through the viewport with confidence. Different from old marquee tags — modern kinetic marquees use SVG, transform, and proper rendering for smooth scrolling.

**When to use.** Brand statements. Manifestos. Section breaks. Anywhere a single line of text deserves attention.

**Cost.** Low.

**Ship at 60fps.** Animate `transform: translateX()` on the marquee container. Duplicate the content so the loop is seamless.

---

### Text Mask Reveal

**Pattern.** Text appears to be revealed by a mask — characters or words emerge one by one (or in groups) as if being uncovered. The reveal is tied to scroll position or to entry into the viewport.

**When to use.** Hero headlines. Section openers. Story moments.

**Cost.** Medium. Requires per-character or per-word DOM splitting.

**Ship at 60fps.** Animate `clip-path` or `opacity` per element. Use `requestAnimationFrame`. For large strings, consider canvas rendering.

---

### Scramble Text

**Pattern.** Text that scrambles into its final form. Initial state shows random characters that animate (frame by frame) into the target string.

**When to use.** Hero opens. Brand reveals. Tech-aesthetic surfaces.

**Cost.** Medium. JS animation.

**Ship at 60fps.** Use `requestAnimationFrame` with throttled updates. Avoid animating the DOM more than ~30fps for character changes — the eye doesn't need 60fps for character scramble.

---

### Circular Path Text

**Pattern.** Text laid out along a circular or curved path using SVG `<textPath>`. The text follows the curve, sometimes rotating around it as the user scrolls.

**When to use.** Decorative section breaks. Brand badges. Editorial features.

**Cost.** Medium. SVG knowledge required.

**Ship at 60fps.** SVG renders on the GPU. Animate the rotation, not the text generation.

---

### Gradient Stroke Text

**Pattern.** Text with a gradient applied to the stroke (outline) rather than the fill. The fill stays transparent or matches background.

**When to use.** Display text in heroes. Decorative section openers.

**Cost.** Low.

**Ship at 60fps.** Trivial — static CSS.

---

### Two-Tone Editorial Type

**Pattern.** A headline split into two visual treatments — half in one color or weight, half in another. The visual break creates emphasis on one phrase within the headline.

**When to use.** Brand-led headlines. Editorial features. Headlines where one phrase carries the punch.

**Cost.** Low.

**Ship at 60fps.** Trivial.

---

## Micro-Interaction Patterns

### Particle Explosion

**Pattern.** On a key event (form submit success, button click, milestone reached), a burst of particles emanates from the trigger point. Sparingly used for celebration moments.

**When to use.** Successful form submissions. Achievement unlocks. Milestone reveals.

**Cost.** Medium. Canvas or DOM-based particles.

**Ship at 60fps.** Canvas with a simple particle system (50-100 particles) runs smoothly. DOM-based particles drop frames above ~20 elements.

---

### Liquid Pull-to-Refresh

**Pattern.** Pull-to-refresh that distorts the top of the content as the user pulls — like pulling fabric or liquid. The distortion releases when the user lets go.

**When to use.** Mobile feeds. App-like products on web.

**Cost.** Medium to high. SVG mask or WebGL.

**Ship at 60fps.** Use `requestAnimationFrame`. Stay on the GPU.

---

### Skeleton Shimmer

**Pattern.** Skeleton loading state with a subtle shimmer — a gradient that sweeps across the skeleton blocks, indicating loading is in progress.

**When to use.** Any loading state that takes >400ms.

**Cost.** Low.

**Ship at 60fps.** Animate `background-position` of a gradient. Pure CSS.

---

### Directional Hover

**Pattern.** When the cursor enters a card, the card's hover effect comes from the direction the cursor entered. Cursor enters from the left, hover slides in from the left.

**When to use.** Feature card grids. Product galleries.

**Cost.** Medium. Requires JS to detect entry direction.

**Ship at 60fps.** Use `transform: translateX/Y()` for the hover slide. Detect entry direction by comparing cursor position to card center.

---

### Ripple Effect

**Pattern.** Click ripple — when the user clicks a button or surface, a circular ripple emanates from the click point. Material Design canonical.

**When to use.** Buttons. Touch surfaces. List items.

**Cost.** Low.

**Ship at 60fps.** Animate `transform: scale()` and `opacity` on a circle element positioned at the click coordinates.

---

### SVG Line Drawing

**Pattern.** An SVG path that animates as if being drawn by a pen — `stroke-dasharray` and `stroke-dashoffset` tied to scroll or to entry into the viewport.

**When to use.** Decorative section dividers. Illustration reveals. Stat callouts.

**Cost.** Medium. SVG knowledge required.

**Ship at 60fps.** Animate `stroke-dashoffset` only. Use `requestAnimationFrame` for scroll-tied animations.

---

### Mesh Gradient

**Pattern.** A multi-color gradient that interpolates between several color points placed in a 2D mesh. The result is organic, with colors flowing into each other in non-linear ways.

**When to use.** Backgrounds. Hero atmospherics. Brand surfaces.

**Cost.** Medium. Pure CSS is possible with multiple `radial-gradient` layered; WebGL is more flexible.

**Ship at 60fps.** Static is trivial. Animated mesh gradients should animate the radial-gradient positions, not regenerate.

---

### Lens Blur Depth

**Pattern.** Background content blurs based on depth — foreground sharp, midground slightly blurred, background heavily blurred — simulating camera depth of field.

**When to use.** Hero overlays. Modal overlays. Anywhere a layer hierarchy benefits from depth cues.

**Cost.** Medium.

**Ship at 60fps.** `filter: blur()` on the background layers. Stays on the GPU.

---

## Imagery Patterns

### Full-Bleed Product

**Pattern.** Product image fills the viewport edge-to-edge. The product is the entire visual statement. Copy overlays or sits beside the image.

**When to use.** Brand-led product launches. Premium products. Editorial features.

**Cost.** Medium. The image must be high quality. Crop and composition matter.

**Ship at 60fps.** Trivial. Use `srcset` and `loading="lazy"` for performance.

---

### Inline Contextual Imagery

**Pattern.** Images embedded within text content — not in a sidebar, not in a gallery, but inline with paragraphs and headings. The image is part of the reading flow.

**When to use.** Editorial articles. Product documentation. Storytelling pages.

**Cost.** Low.

**Ship at 60fps.** Trivial. Lazy-load.

---

### Editorial Juxtaposition

**Pattern.** Two contrasting images placed side by side — before/after, problem/solution, old/new — creating tension and meaning through comparison.

**When to use.** Case studies. Product evolution stories. Brand narratives.

**Cost.** Low.

**Ship at 60fps.** Trivial.

---

### Soft-Edge Lifestyle

**Pattern.** Lifestyle imagery with soft, faded edges — vignetted toward the background, blending into the surrounding layout. The image feels integrated, not bolted on.

**When to use.** Brand pages. Editorial features. Anywhere lifestyle imagery supports rather than dominates.

**Cost.** Low.

**Ship at 60fps.** Trivial. Use a CSS mask or pre-processed image with alpha edges.

---

### Image Grid

**Pattern.** A grid of images — varied sizes, often a hero image plus several supporting images. A visual story told through composition.

**When to use.** Galleries. Portfolios. Product photography.

**Cost.** Low.

**Ship at 60fps.** Trivial. Lazy-load images below the fold.

---

## The 5 Dashboard Archetypes

Dashboards are their own design problem. Five archetypes cover most cases. Pick the archetype that matches the user's job-to-be-done; don't blend archetypes within one dashboard.

### 1. Intelligent List

**Pattern.** Dashboard organized as a smart list — emails, tasks, deals, support tickets. Each row carries the essential information; clicking opens detail. Filters, search, sort, and bulk actions are the primary controls.

**When to use.** Inbox-like products. Task managers. CRM. Support systems.

**Composition.** Top: filter and search bar. Middle: list (denser than typical, 4-6 fields per row). Right: optional detail pane or expand-in-place.

**Cost.** Medium. Performance matters as the list grows.

---

### 2. Command Input

**Pattern.** Dashboard organized around a command input — a chat-like or terminal-like interface where the user types queries or commands and the system responds. The history of commands and responses scrolls.

**When to use.** AI products. Power-user tools. Developer products.

**Composition.** Bottom: command input. Above: scrolling history of inputs and outputs. Right: optional context pane.

**Cost.** Medium. Requires careful state management for the history.

---

### 3. Live Status

**Pattern.** Dashboard showing real-time status of a system — uptime, deployment, sensor readings, server health. Information updates in real time; the user is monitoring, not editing.

**When to use.** Ops dashboards. Monitoring. IoT. Live event tracking.

**Composition.** Top: high-level status (green/amber/red, key KPIs). Middle: detailed panels updating live. Bottom: alerts and event log.

**Cost.** Medium. Real-time updates need careful throttling to avoid jank.

---

### 4. Wide Data Stream

**Pattern.** Dashboard showing wide-format data — tables, time series, large grids. The user is analyzing, not monitoring.

**When to use.** Analytics. Reporting. Data exploration.

**Composition.** Top: time range and dimension controls. Middle: chart or table. Right or below: secondary panels (legends, drill-downs).

**Cost.** Medium to high. Performance with large datasets is the key challenge.

---

### 5. Contextual Focus

**Pattern.** Dashboard organized around a single context — a customer, a deal, a project. Everything on screen relates to that one thing. The user dives in, sees everything, takes action.

**When to use.** CRM detail pages. Project management. Account dashboards.

**Composition.** Top: identity (the customer name, the project name, key status). Middle: tabs or sections grouping related information. Side: actions and relationships.

**Cost.** Medium.

---

## Combinations That Work

| Brief | Pattern Combination |
|---|---|
| **Premium product launch** | Cinematic center hero + bento grid features + spotlight border cards + magnetic primary CTA |
| **Editorial brand site** | Asymmetric split hero + editorial column rhythm + kinetic marquee + soft-edge lifestyle imagery |
| **Conversion-focused SaaS** | AIDA flow landing + minimal split nav + parallax tilt feature cards + scroll-revealed testimonials |
| **Developer product** | Thesis-statement hero + split-screen scroll for code/explanation + dock magnification for tool icons |
| **App-like product** | Floating glass pill nav + morphing status pill + skeleton shimmer + liquid pull-to-refresh |
| **Brutalist brand** | Broken grid + chroma grid sections + gradient stroke text + scramble text on entry |
| **Storytelling page** | Curtain reveal hero + sticky scroll stack + zoom parallax + SVG line drawing on key stats |
| **Portfolio site** | Mosaic layout + horizontal scroll hijack for projects + editorial juxtaposition imagery |
| **AI product** | Command input dashboard + holographic foil cards for features + mesh gradient backgrounds |
| **Premium e-commerce** | Full-bleed product hero + bento grid for collections + glassmorphism card for cart + magnetic CTA |

Pattern combinations reinforce when they share a tonal direction — editorial, premium, brutalist, technical, organic. Mixing tones produces incoherent design.

---

## Hard Combinations to Avoid

| Combination | Why it fails |
|---|---|
| **Bento grid + broken grid** | The bento needs visual order to read as bento; the broken grid breaks the order. They cancel each other out. |
| **Horizontal scroll hijack + sticky scroll stack** | Both compete for the user's scroll interpretation. The user can't tell which axis they're navigating. |
| **Kinetic marquee + scramble text + text mask reveal** | All three are kinetic typography patterns on a single page. The eye has nowhere to rest. |
| **Magnetic button + parallax tilt card + directional hover + dock magnification** | All four track the cursor. The cursor becomes a busy commanding influence; the page feels nervous. |
| **Glassmorphism card + holographic foil + liquid glass card + mesh gradient** | All four are translucent / refractive treatments. The visual hierarchy collapses; nothing stands out. |
| **Brutalist broken grid + premium spotlight border cards** | Tonal mismatch. Brutalism is unrefined by design; spotlight border is premium polish. They fight. |
| **Cinematic center hero + thesis-statement hero** | Both are full-screen hero treatments. They can't coexist on the same page; pick one. |
| **Particle explosion + ripple effect + skeleton shimmer on every action** | Every micro-interaction is a celebration. The celebration loses meaning. Reserve big micro-interactions for big moments. |
| **Curtain reveal hero + locomotive sequence + zoom parallax** | All three are scroll-driven entry animations. The user enters the page, the page animates aggressively, the user can't read anything. |
| **All five dashboard archetypes in one dashboard** | Each archetype solves a different problem. Mixing creates a tool that does many jobs poorly. Choose one. |

When in doubt, simplify. Cut the second-most-impressive pattern. The result is more confident than the additive version.

---

## Verification Before Ship

For every design that uses patterns from this library, verify before shipping:

- **60fps test.** Open Chrome DevTools, Performance tab. Record an interaction. Check frame rate. Below 60fps in any sustained interaction, fix.
- **Reduced motion.** Test with `prefers-reduced-motion: reduce`. All decorative motion should be disabled or significantly reduced.
- **Touch test.** Test on a mid-range Android. Cursor-driven patterns should degrade gracefully. Tap targets must be 44x44+.
- **Keyboard test.** Tab through every interactive element. Focus indicators visible. Logical tab order.
- **Screen reader test.** Run a screen reader on the page. Critical content readable.
- **Low-bandwidth test.** Throttle the network in DevTools to 3G. The page should load reasonably; heavy animations should not block content.
- **Aging hardware test.** Test on a 3-year-old laptop. Patterns that drop frames there will drop frames in production for many users.

A pattern that fails any of these tests is downgraded or removed.

---

## Related references

- [The 30 Laws of UX](The-30-Laws-of-UX.md)
- [Don Normans design principles applied](Don-Normans-design-principles-applied.md)
- [Krug 3 Laws of Usability with examples](Krug-3-Laws-of-Usability-with-examples.md)
- [Anti-AI slop ban list](Anti-AI-slop-ban-list.md)

---

Repository: github.com/Laith0003/ux-skill | Maintainer: linkedin.com/in/laithaljunaidy
