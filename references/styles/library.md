# Style library — three distinct aesthetic systems

Three style systems for use as design directions. Each has its own typography, color, layout, motion, and component logic. When picking a style for a brief, choose ONE and commit. Don't blend.

Mixing two of these inside one interface is the most common failure mode. The brutalist substrate will fight the minimalist whitespace; the high-end gradients will read as decoration grafted onto editorial restraint. Pick the system that matches the brief, then stay inside it for every screen.

This file covers:
- Industrial / Brutalist
- Minimalist
- High-End Visual / Aesthetic-Maximalist
- A decision tree for picking between them
- Cross-style discipline (rules that apply regardless of the system chosen)
- Mixing rules — when and why blending is acceptable, and when it isn't

---

## Industrial / Brutalist

### When to use

Reach for this when the product wants to feel raw, mechanical, or anti-mainstream. Specifically:

- Developer tools, infrastructure dashboards, observability platforms, terminal-adjacent products.
- Indie creator products where the brand voice is contrarian, unfiltered, or technical.
- Editorial brands that want to read as declassified documents, field manuals, or zines.
- Data-heavy interfaces where dense tabular information is the product, not a side feature.
- Portfolios for designers, engineers, or studios that want to project precision without polish.
- Hacker, security, demoscene, or post-cyberpunk audiences who actively reject consumer UI conventions.

Avoid this style for: consumer wellness products, financial services targeting non-technical audiences, hospitality, family or child-oriented products, anything where "warm and welcoming" is a brand requirement.

### Typography

Typography carries almost all visual weight. Two compulsory voices: a structural heavy sans for headlines and a monospace for metadata. Optionally, a third high-contrast serif appears as textural disruption.

Macro-typography (headlines, section markers, viewport-bleeding numerals):

- Use neo-grotesque heavy or black-weight sans-serifs. Suitable choices include grotesks at black weight, extended industrial display faces, or extra-bold geometric sans-serifs with high x-height.
- Scale is aggressive. Use fluid clamps like `clamp(4rem, 10vw, 15rem)` so headlines visibly press against viewport edges.
- Letter-spacing is tight or negative: `-0.03em` to `-0.06em`. Glyphs should fuse into solid architectural blocks.
- Line-height is compressed: `0.85` to `0.95`.
- Casing is exclusively uppercase. No exceptions for headlines.

Micro-typography (metadata, navigation, unit IDs, telemetry, coordinates, status labels):

- Use technical monospaces. Modern programming monospaces, terminal-era bitmap faces, plex-style technical monos, or typewriter monospaces work well.
- Scale is fixed and small: `10px` to `14px` (roughly `0.7rem` to `0.875rem`).
- Letter-spacing is generous: `0.05em` to `0.1em`, simulating mechanical typewriter spacing or terminal grids.
- Line-height stays tight: `1.2` to `1.4`.
- Casing is exclusively uppercase.

Textural disruption (sparingly, often once per page):

- High-contrast serifs at display scale, immediately degraded through halftone, 1-bit dither, or scanline overlays. The point is friction against the clean sans-serifs, not legibility.

### Color

Uncompromising. Modern translucency, soft shadows, and full-spectrum gradients are banned. Pick ONE substrate per project — light industrial print or dark tactical telemetry — and stay there.

Light industrial print substrate:

- Background: warm matte off-white in the range of `#F4F4F0` to `#EAE8E3`. Suggests unbleached documentation paper, not the bright white of a SaaS dashboard.
- Foreground: near-black carbon ink, `#050505` to `#111111`. Never pure black.
- Accent: a single aviation or hazard red, `#E61919` or `#FF2A2A`. The only accent color. It appears as strike-throughs, thick structural dividers, warning stripes, or vital data highlights. Never decorative.

Dark tactical telemetry substrate:

- Background: deactivated CRT black, `#0A0A0A` to `#121212`. Avoid pure `#000000` — the slight lift reads as a real screen rather than an empty void.
- Foreground: white phosphor, `#EAEAEA`. The primary text color.
- Accent: the same hazard red, used under the same rules.
- An optional terminal green (`#4AF626`) may appear, but only on a single specific element such as one status indicator or one live readout. Never as a general body color. If it doesn't serve a clear purpose, omit it.

Rules that apply to both substrates:

- No gradients.
- No soft drop shadows. Shadows, if any, are hard offsets (e.g., `4px 4px 0 var(--ink)`) reading as printed registration marks.
- No translucency beyond simulated noise overlays.
- No secondary or tertiary accent. The hazard red carries all chromatic load.

### Layout

The layout must appear mathematically engineered. Reject conventional web padding in favor of visible compartmentalization.

Grid logic:

- Strict CSS Grid throughout. Elements anchor precisely to grid tracks; they never float.
- Use `display: grid; gap: 1px;` with contrasting parent/child background colors to generate razor-thin dividing lines without verbose border declarations.
- The grid is allowed to be visible. Faint baseline grids, registration marks, and ruler tick marks reinforce the "engineered drawing" feel.

Density:

- Bimodal. Dense clusters of monospaced metadata sit immediately next to vast expanses of negative space framing macro-typography. The eye is never given a comfortable midrange.
- Tabular data is genuinely tabular. Use semantic `<table>` markup, not stacks of styled divs.

Alignment:

- Asymmetric. Centered layouts contradict the system. Push macro-headlines to one rail; cluster telemetry tight against the opposite edge.
- Macro-typography is allowed and encouraged to bleed past viewport edges, cropping a numeral or letter to reinforce the "this is a printed plate" feeling.

Geometry:

- Absolute rejection of `border-radius`. Every corner is exactly 90 degrees.
- Solid borders, `1px` or `2px`, delineate operational zones.
- Full-width horizontal rules separate sections.

### Motion

Motion is restrained, mechanical, and information-dense. Avoid spring physics and graceful eases — they read as consumer-soft.

Appropriate motion:

- Step-function reveals using `steps(N)` easing, simulating CRT redraw or mechanical advancement.
- Instant snap states for hover and focus. Outlines invert their fill in zero milliseconds.
- Slot-machine numeric counters that tick through digits with a discrete clack rather than a smooth lerp.
- Optional CRT flicker on key elements — a low-opacity scanline that drifts slowly down the viewport at very slow speeds.
- Glitch or RGB-split events on critical alerts, used once or twice per page maximum.

Inappropriate motion:

- Spring-physics card lifts.
- Soft fade-ups with blur radius.
- Parallax mouse-tilt on cards.
- Anything that reads as "premium consumer."

### Components

Buttons:

- Hard rectangular blocks with `1px` or `2px` solid borders. No radius.
- Uppercase monospace labels with generous tracking.
- Active state is a hard color inversion: foreground becomes background, background becomes foreground. No transition, no easing.
- Optional ASCII framing in the label (`[ EXECUTE ]`) or directional brackets (`<< BACK`).

Cards / panels:

- Bordered rectangles with visible header strips. The header strip contains an ID code, a revision number, and a status pill — all monospace, uppercase.
- Internal content sits flush against the border. Padding is minimal — often `8px` to `16px`. The crowded feel is intentional.
- Optional corner crosshairs (`+`) at each interior corner reinforce the technical-drawing aesthetic.

Forms:

- Inputs are bare. No background fill, single bottom border that becomes the accent red on focus.
- Labels sit above inputs in uppercase monospace, with field codes preceding them (e.g., `F-01 / NAME`).
- Errors appear inline as red monospace text with a leading directional marker (`>>>`) — never softened into a toast.

Navigation:

- Horizontal rail of uppercase monospace links separated by vertical bars (`|`) or directional markers.
- Active state inverts: link sits inside a solid block of foreground color with background-colored text.
- No hover lift, no underline animation. The inversion is the entire interaction.

Tables:

- True tabular layout. Rows alternate using a single-pixel border, not background tint.
- Column headers are uppercase monospace, top-aligned, with unit codes in parentheses where applicable (`VOLTAGE (V)`).
- Numeric cells right-align; their tabular figures sit flush against an invisible decimal column.

Charts and data visualization:

- Single-color line charts in foreground ink against the substrate. No fills, no smoothed splines.
- Axes appear as visible solid lines with tick marks. Gridlines, if present, are 1px hairlines at minimum opacity.
- Annotations use leader lines and monospace callouts, not floating tooltips.

### Visual moves (signature elements)

- ASCII syntax decoration framing structural elements: `[ DELIVERY SYSTEMS ]`, `< RE-IND >`, `>>>`, `///`, `\\\\`.
- Registration, copyright, and trademark symbols (`®`, `©`, `™`) used as structural ornaments — large, set apart, functioning geometrically rather than legally.
- Crosshairs (`+`) at grid intersections.
- Repeating vertical line patterns reading as barcodes or punch-card edges.
- Thick horizontal hazard stripes in red used as section dividers.
- Randomized-looking string data (`REV 2.6`, `UNIT / D-01`, `CH-0042-A`) as constant visual texture, simulating an active mechanical process.
- Halftone and 1-bit dithering applied to imagery and large serif elements, achieved via SVG dot-pattern masks or CSS `mix-blend-mode` overlays.
- CRT scanlines on dark substrates, implemented as a `repeating-linear-gradient` background or a fixed pseudo-element overlay.
- Global low-opacity SVG static noise filter applied to the document root, introducing a unified analog grain.
- Edge-of-viewport macro-typography that visibly crops on a numeral or letter.

### Banned in this style

- Rounded corners of any kind.
- Soft drop shadows.
- Gradients of any kind.
- Glassmorphism, backdrop blur, frosted panels.
- Default humanist sans-serifs (Inter at default weight, Roboto, Open Sans, Helvetica).
- Generic line-icon sets at standard weights.
- Pastel accent colors.
- Centered hero compositions.
- Smooth bezier eases that imply spring physics.
- Card hover-lift with elevated shadow.
- Emoji of any kind.
- Default web component aesthetics (date pickers, native dropdowns).

### Reference moods

- Declassified field manual photocopied three times.
- 1960s Swiss corporate identity manual cross-bred with a mainframe console.
- Warehouse safety poster after sun damage.
- Engineering drawing on dot-grid paper, scanned and uploaded.
- Early-2000s zine print run on a tired risograph.
- Aerospace heads-up display photographed off the glass.
- Newspaper print page with all the photography removed.
- A radar console at the moment before someone touches the controls.

---

## Minimalist

### When to use

Reach for this when the product wants to feel calm, premium, and editorial. Specifically:

- Premium SaaS workspace and productivity products.
- Fintech aimed at considered, deliberate users — wealth, accounting, treasury.
- Editorial publications and reader-first publishing platforms.
- High-end consumer hardware companion apps where the device, not the app, should feel like the hero.
- B2B platforms where the buyer is paying for restraint and clarity, not visual showmanship.
- Long-form content sites, documentation, knowledge bases that need to feel authoritative.
- Onboarding and account experiences where the perceived value of the brand is "we don't waste your attention."

Avoid this style for: consumer entertainment, products targeting youth or impulse audiences, anything where "wow" or "delight" is the headline emotion, anything that has to compete on density of feature surface.

### Typography

The system relies on extreme typographic contrast and deliberate font selection to establish an editorial feel.

Primary sans-serif (body, UI, buttons, navigation):

- Clean, geometric, character-bearing system or near-system sans-serifs. Modern display-and-text sans-serifs designed for screen, neo-grotesque humanist hybrids, or system-native premium faces.
- Body sits at `15px` to `17px` depending on container width.
- Line-height is generous: `1.55` to `1.7` for body, around `1.4` for shorter UI surfaces.

Editorial serif (hero headings, pull quotes, occasional section openers):

- High-quality contemporary text serifs or display serifs with character. Modern transitional serifs with subtle quirks, contemporary "magazine" serifs, or display serifs with optical contrast.
- Tracking is tight: `-0.02em` to `-0.04em`.
- Line-height is compressed: `1.05` to `1.15` at large sizes.
- Used surgically. One per hero, maybe one per major section. Not as a body face.

Monospace (code, keystrokes, metadata, small status text):

- Modern, well-designed programming monospaces with humanist proportions rather than terminal-era faces.
- Always one size step smaller than surrounding body text.

Text colors:

- Body never uses absolute black (`#000000`). Off-black or charcoal — `#111111` or warm charcoal around `#2F3437` — paired with generous line-height for legibility.
- Secondary text is muted gray, around `#787774`.
- Tertiary text and metadata sit lighter still, around `#9B9A97`.

Casing:

- Title case for headlines (or sentence case — both work; commit to one).
- Sentence case for body and UI.
- Uppercase reserved for eyebrow labels and small status pills, always with wide tracking (`0.05em` to `0.1em`).

### Color

Color is a scarce resource. It carries semantic meaning or subtle accent — never decoration.

Canvas and surfaces:

- Background: pure white `#FFFFFF` or, preferably, warm bone / off-white in the range of `#FBFBFA` to `#F7F6F3`.
- Card and surface fills: `#FFFFFF` against a warm canvas, or `#F9F9F8` for layered surfaces against pure white.
- Structural borders and dividers: ultra-light gray `#EAEAEA` or `rgba(0,0,0,0.06)`.

Accent palette (used only where semantically meaningful):

- Highly desaturated, washed-out pastels. Each pastel has a paired darker text color so that pill-style tags and inline highlights remain legible.
- Pale red surface `#FDEBEC` with text `#9F2F2D` for destructive, urgent, or warning states.
- Pale blue surface `#E1F3FE` with text `#1F6C9F` for informational, neutral-system states.
- Pale green surface `#EDF3EC` with text `#346538` for success, completion states.
- Pale yellow surface `#FBF3DB` with text `#956400` for pending, caution states.

Restrictions:

- No primary-colored backgrounds for large elements or hero sections. No bright blue heroes, no green CTAs filling a viewport.
- No gradients, no neon, no full glassmorphism beyond perhaps a faint navbar blur.
- No saturated brand color used as a layout background. If the brand has a strong color, it appears as an accent dot, a single button fill, or a small mark — not as a wall.

### Layout

White space is the layout. Generous, deliberate, occasionally aggressive.

Macro-spacing:

- Section vertical padding is large: `py-24` to `py-32` (roughly `96px` to `128px`) for any meaningful section break.
- Content width is constrained. Main text columns sit at `max-w-4xl` or `max-w-5xl`. Even on wide viewports, the eye is not asked to track across the full screen.
- Inside cards, internal padding is generous: `24px` to `40px`. Never tight.

Grid logic:

- Asymmetric bento layouts are preferred over symmetrical three-column rows.
- Cards are bordered with exactly `1px solid #EAEAEA`. Not heavier, not softer.
- Border-radius is crisp: `8px` or `12px` maximum. Never pill-shaped containers.

Alignment:

- Left-aligned text is the default. Centered text is reserved for hero callouts and isolated lockups.
- Vertical rhythm is maintained through consistent line-height multiples rather than ad-hoc margins.

Density:

- Low. If a section feels crowded, remove an element rather than reduce spacing.
- A single screen often contains only two or three primary objects.

### Motion

Motion exists, but it should feel invisible — present but never demanding attention. The goal is quiet sophistication, not spectacle.

Scroll entry:

- Elements fade in gently as they enter the viewport. Use `translateY(12px)` combined with `opacity: 0`, resolving over `600ms` with a curve like `cubic-bezier(0.16, 1, 0.3, 1)`.
- Implementation via `IntersectionObserver`. Never `window.addEventListener('scroll')` — it kills frame rates.

Hover states:

- Cards lift with an ultra-subtle shadow shift: `box-shadow` transitions from `0 0 0` to `0 2px 8px rgba(0,0,0,0.04)` over `200ms`.
- Buttons respond on `:active` with a tiny `scale(0.98)`.

Staggered reveals:

- Lists and grid items enter with a cascade. Use `animation-delay: calc(var(--index) * 80ms)`. Never mount everything at once.

Background ambient motion:

- Optional. A single, very slow-moving radial gradient blob — `animation-duration: 20s` or longer — at very low opacity (`0.02` to `0.04`), drifting behind a hero. Applied to a `position: fixed; pointer-events: none` layer only. Never on a scrolling container.

Performance constraints:

- Animate exclusively via `transform` and `opacity`. No layout-triggering properties (`top`, `left`, `width`, `height`).
- `will-change: transform` used sparingly, only on elements actively animating.

### Components

Buttons:

- Primary CTA: solid `#111111` background, `#FFFFFF` text, `4px` to `6px` border-radius. No box-shadow. Hover shifts background to `#333333` or applies micro-scale `transform: scale(0.98)`.
- Secondary CTA: white background, `1px solid #EAEAEA`, charcoal text. Hover darkens the border to charcoal.
- Tertiary CTA: text-only with an inline underline that reveals or thickens on hover.

Cards (bento boxes):

- Asymmetrical CSS Grid layouts where cards have varying spans.
- Each card: white or layered surface fill, `1px solid #EAEAEA` border, `8px` to `12px` radius, generous internal padding.
- Cards contain a single concept each. If a card needs two things, it needs to be two cards.

Tags and status badges:

- Pill-shaped (`border-radius: 9999px`). The pill is the only place pills are permitted.
- Typography: monospace or small uppercase sans, wide tracking (`0.05em`).
- Background uses the muted pastel system; paired text color comes from the same pastel pair.

Accordions and FAQs:

- Strip all container boxes. Separate items only with `border-bottom: 1px solid #EAEAEA`.
- Toggle icon is a clean, sharp `+` and `-` — never a chevron arrow.

Keystroke and shortcut UI:

- Render shortcuts as physical keys using `<kbd>` markup: `border: 1px solid #EAEAEA`, `border-radius: 4px`, `background: #F7F6F3`, monospace font.

Faux-OS window chrome (for software mockups):

- Wrap interface previews in a minimalist frame with a white top bar containing three small light gray circles, mimicking a desktop window header.

Navigation:

- Top navigation is typically a thin horizontal rail with text links. No background fill on the rail itself; let it sit on canvas.
- Optionally a very subtle backdrop blur appears when the user scrolls past the hero.

Forms:

- Inputs use `1px solid #EAEAEA` borders, generous internal padding, `4px` to `6px` radius.
- Labels sit above inputs in sentence case.
- Helper text sits below in muted gray.
- Errors appear inline below the affected field, using the pale red pair, never as a floating toast.

Charts and data visualization:

- Line charts use single charcoal lines with minimal styling. Axes are hairline `#EAEAEA`.
- Data point highlights use the pastel accent system.
- Number formatting is honest — no inflated decimals, no false precision.

### Visual moves (signature elements)

- Massive vertical whitespace around discrete content blocks.
- A single serif headline against an otherwise sans-serif page.
- Asymmetric bento grids with varying card heights but a single border treatment throughout.
- Pastel pills holding the only chromatic punch on the page.
- Faux-OS window frames around product screenshots, making them feel like artifacts rather than mockups.
- Inline keyboard shortcut keys rendered as miniature physical keycaps.
- A single low-opacity radial light drifting slowly behind a hero, almost imperceptible.
- Monochromatic line illustrations with a single offset pastel shape behind them.
- Numbers and section markers in monospace, used like editorial folios.

### Banned in this style

- Default heavy drop shadows. Any shadow used must be ultra-diffuse and below `0.05` opacity.
- Default web typography (the standard humanist sans-serifs most platforms ship).
- Generic line-icon libraries used at their default thin stroke.
- Primary-colored hero sections (bright blue, bright green, bright red).
- Gradients, neon colors, 3D glassmorphism beyond a subtle navbar blur.
- Pill-shaped containers used for non-tag elements (no pill cards, no pill primary buttons).
- Emojis anywhere — in code, markup, headings, alt text, microcopy. Replace with crisp icons or SVG primitives.
- Generic placeholder content. No "John Doe", no "Acme Corp", no "Lorem Ipsum". Use realistic, contextual content even in mockups.
- AI copywriting clichés: "elevate," "seamless," "unleash," "next-gen," "game-changer," "delve." Write plain, specific language.
- Flat empty backgrounds. Even quiet sections should have ambient depth via low-opacity imagery, soft radial light, or geometric line patterns.

### Reference moods

- A well-bound paperback, all interior pages, no cover photography.
- The reading room of a private library on a slow weekday afternoon.
- A high-end stationery store catalog photographed in soft window light.
- An architect's monograph — heavy paper, generous margins, careful captions.
- A boutique hotel printed brochure with one accent ink on cotton stock.
- A workspace tool that respects the work more than the workspace.
- A whitepaper that earns its margins.
- A long-form essay site that loads without anything moving.

---

## High-End Visual / Aesthetic-Maximalist

### When to use

Reach for this when "wow" is the headline emotion and the product has earned the right to be expensive on the surface. Specifically:

- Creator tools, design platforms, and visual editors where the marketing site has to prove the tool's taste before the user signs up.
- Premium consumer brands targeting an audience with eye fatigue for default SaaS aesthetics.
- AI products that want to feel like a leap, not an iteration.
- Hardware companion experiences where the visual fidelity must match the unboxing.
- Landing pages and marketing surfaces for products whose pricing is high enough that perceived craft is part of the value proposition.
- Award-pursuing portfolios, agency sites, and case study experiences.
- Conference, event, and brand activation microsites where the brief is "make it feel like an experience."

Avoid this style for: data-heavy production interfaces where users spend hours; accessibility-critical government or healthcare flows; products whose audience would read maximalist visuals as untrustworthy or expensive-to-run.

### Typography

The system runs on premium display faces, deliberate variance in weight, and obsessive control of optical detail.

Display headlines:

- Modern variable display sans-serifs with wide proportions, or contemporary display serifs with high optical contrast. Suitable choices include wide geometric grotesks, expressive editorial serifs with personality, or modern neo-grotesques with optical sizes.
- Scale is enormous on hero surfaces. Headlines occupy a meaningful percentage of the viewport height.
- Tracking is finely tuned per size — tight at display scale, neutral at section scale.
- Line-height at display scale is compressed: `0.95` to `1.05`.

Body and UI:

- Modern variable sans-serifs with humanist warmth. Suitable choices include contemporary screen-optimized sans-serifs designed for product use.
- Body sits at `15px` to `17px` with comfortable `1.5` to `1.6` line-height.

Eyebrow tags (precede major headlines):

- Microscopic pill-shaped badges. Roughly `10px` typography, uppercase, tracking `0.2em`, medium weight.
- Sit immediately above an H1 or H2 with a small offset.

Numerals and metadata:

- Tabular figures where columns of numbers appear together so digits align vertically.

### Color

Color is purposeful and theatrical, but never crass. Pick a vibe archetype and commit.

Vibe archetypes — pick ONE per project:

**Ethereal glass** (suited for technical, AI, SaaS surfaces):

- Substrate: the deepest OLED black, around `#050505`.
- Radial mesh gradients in the background — subtle glowing orbs in deep purple, emerald, indigo, or magenta, well outside saturation thresholds that would feel garish.
- Card surfaces: near-vantablack with heavy backdrop blur and hairline white borders at low opacity (e.g., `rgba(255,255,255,0.08)` to `rgba(255,255,255,0.12)`).
- Inner highlights on glass elements: a single 1px inset top highlight at low opacity to suggest a glass plate catching light.

**Editorial luxury** (suited for lifestyle, real estate, agency, hospitality):

- Substrate: warm cream, around `#FDFBF7`, or deep espresso for dark variants.
- Accent tones: muted sage, ochre, soft terracotta, dusty rose, or a single saturated jewel tone used surgically.
- High-contrast variable serif fonts at massive scale.
- Subtle film-grain overlay at very low opacity (`0.03`) for a physical paper feel.

**Soft structuralism** (suited for consumer, health, portfolio, premium hardware):

- Substrate: silver-gray, warm white, or completely white.
- Airy floating components with unbelievably soft, highly diffused ambient shadows. The shadow is large in spread but extremely low in opacity.
- Massive bold display sans-serifs.
- Occasional precision color accents — a single saturated color reserved for a CTA or single brand mark.

Universal rules:

- No banned defaults. No bright primary shadows, no harsh `rgba(0,0,0,0.3)` shadows.
- No flat solid color hero blocks; every section has texture, ambient light, or depth.
- When using saturated color, restrict it to a small surface area — never a full-bleed hero wall.

### Layout

Layouts must feel composed, not laid out. The eye should travel through a designed space, not scan a content list.

Macro-whitespace:

- Section padding is at least `py-24`, often `py-32` to `py-40`. The design breathes heavily.
- Inside premium containers, padding is similarly generous.

Layout archetypes — pick ONE per project:

**Asymmetrical bento:**

- A masonry-like grid where card sizes vary intentionally. Some cards span more columns and rows than others, breaking visual monotony.
- Mobile collapse: all cards reset to single-column with generous vertical gaps. No `col-span` overrides survive below `768px`.

**Z-axis cascade:**

- Elements stack like physical cards, slightly overlapping with varying depths. Some cards carry a subtle `-2deg` or `3deg` rotation to break the digital grid.
- Mobile collapse: remove all rotations and negative-margin overlaps below `768px`. Stack vertically with standard spacing.

**Editorial split:**

- Massive typography on one half of the viewport, interactive cards or horizontal-scroll image rails on the other half.
- Mobile collapse: full-width vertical stack. Typography block sits on top; interactive content flows below, with horizontal scroll preserved if essential to the experience.

Universal mobile rules:

- Any asymmetric layout that uses fractional widths above the `md:` breakpoint must aggressively fall back to `w-full` with `px-4` and `py-8` padding below `768px`.
- Never use `h-screen` for full-height sections — always `min-h-[100dvh]` to prevent mobile viewport jumping when the address bar collapses.

Eyebrow rhythm:

- Major H1s and H2s are preceded by an eyebrow tag.
- Eyebrow → headline → supporting body → action. This four-beat rhythm repeats per major section.

### Motion

Motion is cinematic, premium, controlled. Every transition must simulate real-world mass and spring physics — never default eases.

Easing:

- All transitions use custom cubic-beziers. A reliable workhorse is `cubic-bezier(0.32, 0.72, 0, 1)` for entries and `cubic-bezier(0.4, 0, 0.2, 1)` for state changes.
- No `linear`, no `ease-in-out`, no instant state changes.
- Durations are longer than defaults. `700ms` to `900ms` for major entries; `300ms` to `500ms` for interaction states.

Fluid island navigation:

- Closed state: a floating glass pill detached from the top edge, with margin above and centered horizontally. Width is content-bounded, not full-bleed.
- Hamburger morph: on click, the hamburger lines fluidly rotate and translate to form an `X`. Lines don't disappear; they transform.
- Modal expansion: the menu opens as a screen-filling overlay with heavy backdrop blur and a darkened glass background.
- Staggered mask reveal: nav links inside the expanded overlay fade and slide up from `translate-y-12 opacity-0` to `translate-y-0 opacity-100`, with a staggered delay (`80ms` to `150ms` between items).

Magnetic button hover physics:

- Use a `group` wrapper on the button so children can respond to hover state.
- On hover, scale the entire button slightly down on press (`active:scale-[0.98]`) to simulate physical pressing.
- The nested trailing icon circle translates diagonally (e.g., one pixel up and one pixel right) and scales up slightly (`scale-105`), creating internal kinetic tension.

Scroll interpolation:

- Elements enter the viewport with a heavy fade-up combining `translate-y-16`, `blur-md`, `opacity-0` resolving to `translate-y-0`, `blur-0`, `opacity-100` over `800ms` or longer.
- Implementation via `IntersectionObserver` or framework-equivalent intersection-driven motion. Never `window.addEventListener('scroll')`.

Performance constraints:

- Animate via `transform` and `opacity` only.
- Apply `backdrop-blur` only to fixed or sticky elements (navbars, overlays, modals). Never apply blur filters to scrolling content or large always-on areas — this causes continuous GPU repaints and severe mobile frame drops.
- Grain and noise overlays attach exclusively to fixed, `pointer-events-none` pseudo-elements. Never to scrolling containers.
- Reserve high `z-index` values for systemic layers (sticky nav, modals, overlays, tooltips). No arbitrary `z-50` or `z-[9999]`.

### Components

Buttons:

- Primary CTAs are fully rounded pills with generous padding (`px-6 py-3`).
- The button-in-button pattern is mandatory for any CTA with a trailing icon. The arrow (or other glyph) never sits naked next to the text — it lives inside its own circular wrapper, flush with the main button's right inner padding. The wrapper has its own subtle background and ring, distinct from the parent button.
- Secondary buttons echo the same pill shape with reduced fill (`bg-black/5`, `bg-white/10`) and a hairline ring.

Cards and feature containers — the double-bezel pattern:

- Never place a premium card flatly on the background. Cards must look like physical, machined hardware — a glass plate sitting in an aluminum tray.
- Outer shell: a wrapper element with a subtle background (`bg-black/5` or `bg-white/5`), a hairline outer border (`ring-1 ring-black/5` or `border border-white/10`), specific padding (`p-1.5` or `p-2`), and a large outer radius (`rounded-[2rem]`).
- Inner core: the actual content container inside the shell. It has its own distinct background color, an inner highlight (`shadow-[inset_0_1px_1px_rgba(255,255,255,0.15)]`), and a mathematically calculated smaller radius (e.g., `rounded-[calc(2rem-0.375rem)]`) so the inner and outer radii are visibly concentric.

Navigation:

- Floating glass pill detached from the viewport top with substantial top margin.
- Pill content includes the brand mark, a small set of primary links, and a primary CTA.
- On scroll past the hero, the pill darkens or its backdrop blur intensifies — but it never glues to the edge.

Forms:

- Inputs sit inside their own bezel treatment. The outer container provides the radius and outer ring; the inner input has its own subtler ring and inner highlight.
- Focus state intensifies the inner ring and adds a soft outer glow keyed to the brand or vibe accent.

Hero imagery and product mockups:

- Imagery is wrapped in the double-bezel pattern at hero scale. The mockup feels like a framed artifact, not a screenshot dumped onto canvas.
- Optional subtle perspective tilt (`rotateX(8deg)` paired with `rotateY(-4deg)`) to suggest a physical object held at an angle.

Modals and overlays:

- Full-screen takeovers, never narrow centered dialogs. The overlay carries a heavy backdrop blur and a dim layer.
- Content inside the modal uses the double-bezel pattern.

Eyebrow tags:

- Microscopic pill-shaped badges, `rounded-full px-3 py-1`, text at `10px` uppercase tracking `0.2em` medium weight.
- Sit immediately above hero or section H1s/H2s.

### Visual moves (signature elements)

- Mesh gradients in the background — radial orbs of color that bleed and overlap softly behind hero text.
- Liquid glass cards with backdrop blur, hairline borders, and inset highlights, suggesting machined hardware on glass.
- Holographic or iridescent micro-accents — small reflective elements on otherwise restrained surfaces.
- Cinematic scroll entries: text and imagery rising from below with motion blur dissolving as they settle.
- The button-in-button pattern with magnetic hover physics.
- The double-bezel concentric radius pattern, applied consistently to every premium container.
- Floating glass pill navigation that detaches from the viewport edge.
- Eyebrow tags preceding every major headline.
- Subtle film-grain overlays at very low opacity providing physical paper or sensor texture.
- Hero imagery rendered as if it's a physical artifact — framed, tilted, lit, never bare.
- Massive display typography at scales that border on the editorial-architectural.

### Banned in this style

- Default humanist sans-serifs that ship as web defaults.
- Generic thick-stroke icon libraries. Use only ultra-light, precise lines with consistent stroke weight.
- Generic 1px solid gray borders without surrounding structure. Every border lives inside a bezel or ring system.
- Harsh dark drop shadows. Specifically `shadow-md` defaults and any shadow with `rgba(0,0,0,0.3)` or heavier opacity.
- Edge-to-edge sticky navbars glued to the viewport top. The nav must float, breathe, and detach.
- Symmetrical three-column grids without massive whitespace gaps.
- Standard `linear` or `ease-in-out` transitions.
- Instant state changes without interpolation.
- Backdrop blur applied to scrolling containers.
- Flat empty hero sections without ambient depth.
- Cards placed bare on background without bezel treatment.
- CTAs with naked trailing arrows that aren't wrapped in their own circle.
- Z-index sprawl with arbitrary high values.

### Reference moods

- A flagship product unveiling shot in slow-motion, lit from above.
- A late-evening boutique window display, internally lit, viewed through misted glass.
- A high-end watch movement photographed under macro light, every facet considered.
- A film title sequence where each character types itself into an atmospheric backdrop.
- A perfume campaign whose hero is the glass bottle, not the model.
- A piece of premium hardware photographed in studio with two soft sources.
- A gallery installation lit so each object floats away from its plinth.
- The opening seconds of a luxury car commercial, when only ambient light is moving.

---

## Style selection decision tree

For any brief, ask these three questions in order. Combine the answers to land on a style.

1. **What is the product type?**
   - Developer tool, infrastructure dashboard, observability product, data-heavy interface, anti-mainstream editorial → start considering brutalist.
   - Productivity tool, document workspace, fintech, B2B platform, knowledge base, long-form publishing → start considering minimalist.
   - Creator tool, design platform, premium consumer brand, AI product with broad appeal, agency portfolio, marketing surface for an expensive product → start considering high-end.

2. **What is the brand tone?**
   - Raw, contrarian, technical, "we don't apologize" → brutalist.
   - Calm, considered, deliberate, "we don't waste your attention" → minimalist.
   - Luxe, cinematic, theatrical, "we've earned the right to be seen" → high-end.

3. **What does the audience expect?**
   - Audience that actively rejects consumer polish, reads it as "watered down" → brutalist.
   - Audience that has eye fatigue for over-designed SaaS and pays for restraint → minimalist.
   - Audience that judges the product partly on the surface and will reward visual ambition → high-end.

### Recommendation table

| Product type | Brand tone | Audience expectation | Style |
|---|---|---|---|
| Developer tool / infra dashboard | Raw or technical | Rejects consumer polish | Brutalist |
| Indie creator product | Raw or contrarian | Hacker / anti-mainstream | Brutalist |
| Editorial brand / zine / studio site | Raw or editorial | Print-literate audience | Brutalist |
| Data-heavy interface | Technical | Information density required | Brutalist |
| Premium SaaS / productivity tool | Calm | Eye fatigue for SaaS defaults | Minimalist |
| Fintech / wealth / treasury | Calm and deliberate | Considered audience | Minimalist |
| Long-form publishing / documentation | Editorial and calm | Reads carefully | Minimalist |
| B2B platform / knowledge product | Calm and restrained | Wants signal not spectacle | Minimalist |
| High-end hardware companion app | Calm; device is hero | Premium consumer | Minimalist |
| AI product targeting researchers / engineers | Calm, restrained | Reads gradients as cliché | Minimalist |
| Creator tool / design platform | Luxe and cinematic | Judges by surface taste | High-end |
| AI product targeting broad consumer | Luxe and ambitious | Wants to feel a leap | High-end |
| Premium consumer brand | Theatrical | Audience rewards ambition | High-end |
| Agency portfolio / award-targeting site | Cinematic | Peers as audience | High-end |
| Marketing site for expensive product | Luxe | Surface is part of value | High-end |

### Tiebreakers

When two styles seem plausible, default to whichever one the audience would reward more for restraint. A brutalist developer tool that happens to have premium-product positioning should still lean brutalist — the audience reads polish as a tell.

When the brief says "modern, clean, premium" without further specifics, default to minimalist. It is the safest direction across audiences and the least likely to misfire.

When the brief says "wow, agency, design-led, ambitious" without further specifics, default to high-end. The brief is signaling that surface ambition is the explicit requirement.

When the brief is for a product whose audience overlaps two of these styles, pick one and commit. Blending will produce a generic SaaS look that none of the three styles intends.

When the brief mentions "AI" but the target audience is technical (researchers, engineers, infrastructure buyers), lean minimalist or brutalist. The technical AI cohort reads gradient maximalism as low-craft. Restraint signals competence.

When the brief mentions "AI" but the target audience is consumer or creator, lean high-end. The consumer AI cohort rewards visual ambition.

---

## Cross-style discipline

These rules apply regardless of the style chosen. They are non-negotiable.

### Accessibility

- Body text contrast must meet WCAG AA at minimum: `4.5:1` against its background for normal text, `3:1` for large text. Verify in both light and dark variants if both exist.
- Focus states must be visible on every interactive element. Brutalist uses hard inversion; minimalist uses a 2px solid focus ring in the brand accent; high-end uses a soft outer glow combined with a ring. Never rely on color alone.
- All interactive controls reachable by keyboard and operable without a mouse. Tab order matches visual order.
- All images have descriptive alt text or are explicitly marked decorative.
- Form fields have programmatically associated labels — not just visual proximity.
- Error messages are announced to screen readers via appropriate ARIA roles, not just visually styled.
- Touch targets are at least `44px` by `44px` on mobile, regardless of how the design renders them visually.
- Color is never the only signal. Status pills include a text label, error fields include an icon or prefix, success states include a check or word.

### Performance

- Animate exclusively via `transform` and `opacity`. Never animate `top`, `left`, `width`, `height`, or any property that triggers layout.
- `will-change` is applied only to actively animating elements, then removed when animation completes.
- `backdrop-filter` is reserved for fixed or sticky elements. Never apply blur to a scrolling container or to a wide always-on region.
- Noise, grain, and texture overlays attach to fixed `pointer-events-none` layers. Not to scrolling content.
- Heavy assets (background video, mesh gradient canvases, large decorative SVGs) load lazily and have skeleton or fallback states.
- Font loading uses `font-display: swap` or equivalent to avoid invisible text during font load.
- Critical-path CSS for above-the-fold content is inlined where possible.
- Reserve high `z-index` values for systemic layers only. Document them so they don't sprawl.

### Motion and user preferences

- Respect `prefers-reduced-motion: reduce` universally. When active:
  - Brutalist: skip scanline drift, glitch effects, slot-machine counters. Keep instant state changes.
  - Minimalist: replace `translateY` scroll entries with simple `opacity` fades, shorten durations.
  - High-end: drop the blur portion of scroll entries; replace cinematic interpolations with simple fades; pause background mesh animations.
- Never auto-play sound. Any video that auto-plays must be muted, looped if short, and accompanied by a pause control.
- Avoid flashing or rapidly-strobing effects above three flashes per second.
- Avoid motion parallax that depends on device orientation sensors. Cursor-driven parallax is acceptable; phone-tilt parallax is not — it requires sensor permissions that erode trust.

### Mandatory imagery

Every style requires deliberate imagery — none of them can rest on a blank substrate alone.

- Brutalist: imagery is degraded into halftones, dithers, or scanline overlays. Photographs are processed into 1-bit or low-bit visual artifacts. Diagrams, schematics, and technical drawings are welcome at full fidelity.
- Minimalist: imagery is high-quality, desaturated, warm-toned. Subtle warm grain overlay at very low opacity blends photos into the monochrome canvas. Stock photography that reads as oversaturated is banned.
- High-end: imagery is wrapped in the bezel system at hero scale, presented as if it's a physical artifact. Mesh gradients, ambient light, and texture overlays accompany every major section so nothing reads as flat.

Hero and section backgrounds:

- A section that contains content must have visual depth. Empty flat backgrounds are a tell of unfinished design.
- Acceptable depth treatments:
  - Brutalist: visible grid, registration marks, halftone field, scanline overlay, large macro-typographic background numerals.
  - Minimalist: subtle radial light at `opacity: 0.03`, faint warm grain, single offset pastel geometric shape, soft full-width photograph at low opacity.
  - High-end: radial mesh gradient orbs, film-grain overlay, ambient lighting that suggests an off-screen source.

### Mandatory interaction states

Every interactive element ships with the full set of states. Missing states are a quality failure.

**Default state:**
- Visible, legible, clear in its affordance. The user can tell it's interactive at rest.

**Hover state:**
- Brutalist: instant inversion or instant border-color shift to accent.
- Minimalist: subtle shadow lift, micro-scale shift, or quiet color shift over `150ms` to `250ms`.
- High-end: magnetic button physics with nested icon translation, scale, and color shift over `300ms` to `500ms` with custom cubic-bezier.

**Focus state:**
- Visible on keyboard navigation. Not just `:focus-visible` — actually visible.
- Brutalist: hard 2px solid accent outline with zero offset.
- Minimalist: 2px solid focus ring in a paired accent pastel, offset by `2px`.
- High-end: combined ring and soft outer glow keyed to the active vibe accent.

**Active / pressed state:**
- Brutalist: full color inversion.
- Minimalist: micro-scale `0.98` and slight darken.
- High-end: micro-scale `0.98` combined with the magnetic physics shift.

**Disabled state:**
- Visibly inactive. Reduced opacity (`0.4` to `0.6`), `cursor: not-allowed`.
- Tooltip or inline message explaining why the action is disabled, where appropriate.

**Loading state:**
- Replace the label or content with a quiet indicator. Never freeze the entire UI; never block other input.
- Brutalist: monospace dots or a step-frame ASCII spinner.
- Minimalist: a small spinner or a low-opacity skeleton block.
- High-end: a soft pulsing indicator with the active vibe accent and a quiet entry animation.

**Error state:**
- Inline, specific, actionable. Tell the user what's wrong and what to do.
- Never use a vague catch-all like "form contains errors." Name the field. Name the fix.
- All three styles use red sparingly and specifically — never a tidal wave of error color across a form.

**Success state:**
- Quietly confirmed. A success isn't a celebration unless it's an exceptional moment. Toasts, pills, and inline confirmations are sufficient for most flows.

**Empty state:**
- Every list, table, and grid has a deliberate empty state. No bare zero-row screens.
- Empty states explain what the surface is for, what will fill it, and how to add the first item.

### Universal banned defaults

These are banned in every style:

- Emojis anywhere — code, markup, microcopy, alt text, headings, error messages. Use SVG icons or plain text.
- Generic placeholder names: "John Doe", "Acme Corp", "Lorem Ipsum", "Test User", "example@example.com". Use contextual content even in mockups.
- AI copywriting clichés: "elevate," "seamless," "unleash," "next-gen," "game-changer," "delve," "leverage" used as a verb, "robust" applied to anything.
- Default font fallback chains (the standard humanist sans-serifs most platforms ship). Even if the brief doesn't specify fonts, choose intentionally.
- Standard line-icon sets at default stroke weight. Either choose a deliberate icon system or design glyphs to match the style.
- Centered hero compositions used as a fallback when a layout decision isn't made. Center alignment is a deliberate choice, not a default.
- Bootstrap-style symmetrical grids without massive whitespace. Three equal columns separated by `24px` gutters is a tell of unfinished design.
- Auto-play audio anywhere.
- Sensor-based motion effects that require phone tilt or orientation permissions.

### Style discipline reminders

- If the brief is unclear, ask before committing to a style. Switching halfway through a project is more expensive than asking on day one.
- If two styles seem to fit, pick the one whose audience would reward restraint more.
- Once a style is chosen, every screen on the same product carries the same style. There is no "this one screen is brutalist for fun." Consistency is the point.
- Build a token system early. Colors, typography scales, radii, shadow definitions, spacing units — all live in tokens. No magic numbers scattered across components.
- Document why the style was chosen. The next person on the project should be able to read the decision and stay inside it without asking.

---

## Mixing and combining rules

Three rules govern when blending elements across styles is acceptable.

### Rule 1: Mixing is the default failure mode. Pure styles are the default goal.

The most common failure when reading these three systems is the temptation to take "the best of each." It produces inconsistent, templated, generic-feeling output. The minimalist whitespace neutralizes the brutalist density. The high-end gradients undercut the minimalist restraint. The brutalist hazard red clashes with the high-end vibe accent.

Pick one. Commit. Every screen on the same product reads in the same voice.

### Rule 2: Cross-style imports are allowed surgically and only in specific cases.

- **Brutalist eyebrow labels in a minimalist surface.** A small tracked uppercase label above a section heading is one of the most portable patterns. It works across all three systems because the typographic move is universal.

- **Minimalist hairline cards in a high-end surface.** When the high-end maximalist style needs a denser feature section, hairline-border cards (1px gray borders, generous padding) work as a quieter alternative to the double-bezel pattern. The card structure imports cleanly; the surrounding chrome stays high-end.

- **High-end backdrop blur on a minimalist navbar.** A subtle backdrop blur on the sticky nav after scroll is acceptable across styles. The minimalist version uses lighter opacity and a thinner blur than the high-end version.

- **Brutalist monospace numerals in any data-heavy surface.** When numbers matter, monospace numerals lock alignment regardless of style. This is the universal exception.

- **Minimalist generous whitespace in any style.** Padding generosity is universally premium. A brutalist page that crams every pixel can still afford breathing room between sections.

These imports work because they are single moves carried across, not entire pattern systems imported wholesale. Each imported move serves a specific clarity or hierarchy job.

### Rule 3: When in doubt, retreat to the chosen style.

If a pattern is borderline — a magnetic button in a minimalist surface, a glassmorphism panel in a brutalist surface, a hazard-red accent in a high-end surface — retreat to the chosen style. The retreat costs nothing; the import risks coherence. The audience's eye will sense the dissonance even if they can't name it.

The only time to violate Rule 3 is when the import is doing measurable clarity work that no native pattern would. If the magnetic button is the only way to communicate "this is a hero CTA" with sufficient signal weight on an otherwise quiet minimalist page, the import is justified. If the magnetic button is being added because it looks cool, retreat.

### Reading the page for style discipline

Before shipping, ask:

- Is every typographic decision native to the chosen style? (No serifs sneaking into a brutalist page; no monospace numerals sneaking into a minimalist page that doesn't otherwise use monospace.)
- Is every color choice native to the chosen style? (No hazard red in a high-end page; no muted pastel pills in a brutalist page; no purple-mesh gradient in a minimalist page.)
- Is every motion choice native? (No spring physics in a brutalist page; no step-function reveals in a high-end page; no scanline drift in a minimalist page.)
- Is every imagery treatment native? (No halftone dither in a high-end page; no bezel-wrapped product mock in a brutalist page; no mesh-gradient background in a minimalist page.)

When any one of these answers is "no," check Rule 2 — is this a single surgical import, or am I drifting between systems? If it's drift, retreat. If it's a justified single import, document why.

---

## Closing reflection

The three style systems exist not because there are only three ways to design — but because most successful premium products converge on one of them. Each system has a discipline: what to include, what to exclude, what to commit to. The discipline is what produces coherence.

Output that reads as "premium" is rarely doing something unusual. It is committing fully to one of these systems and refusing the templated defaults that would dilute it. The brutalist developer tool that ships in a templated SaaS aesthetic loses its audience. The minimalist fintech that ships with mesh gradients loses its audience. The high-end creator tool that ships with hairline borders loses its audience.

Pick the style. Commit to the style. Ship the style. The rest is execution.
