# Style library — twelve distinct aesthetic systems

Twelve style systems for use as design directions. Each has its own typography, color, layout, motion, and component logic. When picking a style for a brief, choose ONE and commit. Don't blend.

Mixing two of these inside one interface is the most common failure mode. A brutalist substrate will fight minimalist whitespace; high-end gradients will read as decoration grafted onto editorial restraint; the Swiss grid will smother organic illustration. Pick the system that matches the brief, then stay inside it for every screen.

This file covers, in order:
- Industrial / Brutalist
- Minimalist
- High-End Visual / Aesthetic-Maximalist
- Swiss Grid
- Editorial Magazine
- Quiet Emptiness
- Bold Maximalism
- Refined Minimalism
- Aurora Glass
- Retro-Futurist
- Organic Hand-drawn
- Anti-Design Web
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

## Additional design philosophies

The three systems above cover the largest share of premium product work. Nine additional schools are catalogued below. Each one solves a brief the first three cannot. Same rule applies: pick ONE per project and commit. Mixing across systems remains the most common failure mode regardless of how many systems exist.

---

## Swiss Grid

### When to use

Reach for Swiss Grid when the product must read as "authoritative system of record." The grid is the brand. Specifically:

- Editorial publications where typography carries credibility.
- Infosec, audit, compliance, or governance platforms where trust is the surface message.
- Civic, public-records, and government interfaces where neutrality is itself a posture.
- Financial reporting tools where decimals must read as exact and irreducible.
- Long-form documentation that wants to be cited rather than scanned.
- B2B platforms where the buyer is a finance, legal, or operations leader.
- Annual reports, regulatory disclosures, and any surface where the audience expects rigor.

Avoid this style for: consumer entertainment, products targeting teenagers or impulse audiences, anything where "warm" or "fun" is part of the brand promise, anything that has to compete on visual ambition or surprise.

### Typography

Grotesque sans-serif is the sole voice. Hierarchy comes from weight, scale, and position on the grid — never from face variance.

Display sans (headlines, section anchors):

- Use a neo-grotesque sans-serif at semibold or bold. Suitable choices include classical industrial grotesques and modern variable grotesques with neutral character.
- Display scales sit at `48px` to `96px` depending on viewport. Avoid going above `120px` — extreme scales contradict the system's restraint.
- Tracking is neutral at display scale: `0` to `-0.01em`. The Swiss aesthetic does not want tight or expanded display tracking.
- Line-height is compressed: `1.0` to `1.1` for display, `1.4` for body.

Body sans:

- Same family at regular weight, `16px` to `17px`.
- Generous leading: `1.5` to `1.65`.
- Color: a strong, but not pure, black. `#111` or `#1a1a1a`. The system rejects mid-grays for body — clarity is the discipline.

Eyebrow labels and section codes:

- Uppercase, tracked at `+0.08em` to `+0.12em`, at `10px` to `12px`.
- Used liberally — section numbers, category labels, navigation slots. They are the system's punctuation.

Numerals:

- Tabular figures wherever numbers appear in tables or aligned columns.
- Proportional figures only inside prose.

### Color

The palette is almost monochromatic. Color earns the right to appear by carrying semantic load.

Substrate options (pick one):

- **Pure white print substrate**: `#FFFFFF` or `#FDFDFC`. The default for editorial and publication surfaces.
- **Warm parchment**: `#FAFAF7` to `#F4F2EC`. The choice when the surface must read as "considered document."
- **Document gray**: `#F2F2F0`. Used when paired surfaces must distinguish without color shift.

Ink:

- Primary text: `#0F0F0F` or `#111111`. Strong, but lifted off pure black by 5-10 percent.
- Secondary text: `#444444`. Used for caption, footnote, support copy.
- Tertiary text: `#7A7A7A`. Used for metadata.

Accent (a single one, used sparingly):

- One restrained color, applied to category labels, links, and the single CTA per section. Suitable choices: a deep brand red around `#B61F1F`, a navy around `#0E2D5B`, an academic burgundy around `#5C1A1A`. The accent is small and exact — never used as a fill, never bled across a hero.

Rules across substrates:

- No gradients.
- No translucency.
- No glows. The system has no decorative shadow language.
- Backgrounds are flat color. Depth comes from layout structure, not from blur.

### Layout

The grid is visible discipline. Twelve columns at minimum on desktop, eight on tablet, four on mobile. Every element anchors to a column boundary; nothing floats.

Grid logic:

- Twelve-column grid with a `24px` gutter on desktop, `16px` on tablet, `12px` on mobile.
- Vertical rhythm via a `4px` baseline grid. Every line of body, every margin, every heading offset sits on a baseline multiple.
- Section divisions are hairline horizontal rules at `1px solid #DCDCDC` or a `48px` of pure whitespace — never both.

Alignment:

- Left-aligned text is the default. Right alignment is reserved for numerals, captions, or marginalia.
- Center alignment appears once per surface, at most — typically the masthead lockup or a final standalone callout.
- Margins are generous and asymmetric. A surface may carry a wide right-rail margin where notes, side metadata, or context live.

Density:

- Bimodal. Sections of dense reading sit next to sections of generous breathing room. The system does not believe in uniform density.

Margins:

- Body content sits inside a `max-w-3xl` to `max-w-4xl` column. Wider columns are reserved for tables and reference layouts where horizontal scanning is the user's task.

### Motion

Motion is restrained, almost absent. The grid does not move. Elements appear; they rarely interpolate.

Appropriate motion:

- Fade-in on initial section reveal at `300ms` `cubic-bezier(0.4, 0, 0.2, 1)`. No translation, no scale.
- Inline tooltip or footnote reveal at `200ms` fade.
- Page-level transitions when the surface is a multi-page document: a `400ms` crossfade with no movement.

Inappropriate motion:

- Scroll-tied animations. The grid does not perform.
- Spring physics. The aesthetic rejects bouncy.
- Hover lifts. Cards do not levitate.
- Page-load brand-mark animations. The mark is set, never animated.

### Components

Buttons:

- Rectangular. No radius, or `2px` to `4px` at most.
- Primary CTA is a solid ink block with white type, weight semibold, no shadow.
- Secondary CTA is text with an underline on hover.
- Tertiary is plain text with a small directional indicator (a right caret or a small arrow glyph).

Cards (when used):

- Hairline borders, `1px solid #DCDCDC`. No shadows.
- Internal padding generous: `32px` to `40px`.
- A small category label sits at the top corner, uppercase and tracked.

Tables:

- True semantic tables. Hairline rules separate rows; the header row carries a heavier rule below it.
- Column heads in uppercase tracked label style.
- Numeric cells right-aligned, with tabular figures.

Forms:

- Inputs sit on a hairline bottom border only. No filled box, no rounded corners, no shadow.
- Labels above inputs in sentence case, body size.
- Error text in the accent (deep red) below the input.

Navigation:

- A thin horizontal rail with text links, separated by either ample spacing or a vertical hairline.
- No icon nav, no mega-menus. The categories are listed plainly.
- Active link gets a subtle bottom hairline accent.

Charts:

- Single-color line charts with a hairline axis.
- Bar charts in ink only, no fill gradient.
- Data callouts use small marginalia, not floating tooltips.

### Visual moves (signature elements)

- Visible baseline grid hints — small registration marks at section openings.
- Marginal notes in a narrow right-rail at `12px` body type, used as scholarly footnotes.
- Section numerals set in large display weight, used as chapter signposting (but only when the surface genuinely is a journey — never decoratively).
- Pull quotes set inside a thin top and bottom hairline rule, never inside a tinted block.
- Captions set in uppercase tracked label style under every figure.
- Body type set with optical kerning and hung punctuation where the framework supports it.
- Footnote references rendered as small superscript numerals linked to the bottom of the section.

### Banned in this style

- Decorative gradients of any kind.
- Pill-shaped buttons.
- Drop shadows that lift surfaces.
- Glassmorphism, backdrop blur, frosted overlays.
- Saturated brand color across a large surface.
- Default humanist sans-serifs used as the display voice.
- Multi-color charts. Charts in this system are monochromatic.
- Hero photography with text overlaid. Image and text sit side by side, never stacked.
- Emoji of any kind.

### Reference moods

- A national newspaper of record on a slow news day.
- An academic journal's table of contents, set on heavy paper.
- A government white paper with marginal footnotes and tabular appendices.
- A modernist printed program for a museum retrospective.
- The opening pages of an annual report from a company that treats restraint as integrity.
- A specification document from an engineering standards body.
- An auction catalog set in a single neutral grotesque.

---

## Editorial Magazine

### When to use

Reach for Editorial Magazine when the product is about reading and the surface should feel like a publication. Specifically:

- Long-form publications, literary tools, essay platforms.
- Design-forward bookstores and reading apps.
- Premium content marketing platforms aimed at writers and editors.
- Newsletter products where the writer's voice is the brand.
- Indie magazine sites and serial publications.
- Book retailers, especially those curating taste rather than volume.
- Knowledge product surfaces where the article is the unit of value, not the feature list.

Avoid this style for: dashboards, admin surfaces, transactional flows, products optimized for skim-reading or short attention.

### Typography

Type is the system. Serif and sans pair across roles; weight contrast is liberal; long-form readability is non-negotiable.

Body serif (the primary reading face):

- A modern text serif designed for long-form reading. Wide proportion, modest contrast, optical sizing where available.
- Body size: `17px` to `19px` on desktop, `16px` to `17px` on mobile.
- Line-height: `1.6` to `1.75`. Editorial body breathes more than UI body.
- Tracking: `0` or slightly positive at small sizes for screen legibility.

Display serif (occasional, for major openings):

- A high-contrast display serif with optical clarity at large sizes.
- Used surgically — masthead, lead article opener, major section title.
- Tracking tightened: `-0.01em` to `-0.03em` at display scale.

Sans (for UI, captions, eyebrows, navigation):

- A neutral grotesque or geometric sans, used for everything that is not body or display headline.
- One weight family, three weights at most: regular, medium, bold.
- Used at small sizes — `12px` to `14px` for captions, `13px` to `15px` for nav.

Monospace (for code, statistics, citations):

- A modern programming monospace, used when numbers or code must align.

Drop caps and ornaments:

- Drop caps are allowed and encouraged on lead articles. Three-line minimum, six-line maximum.
- Section ornaments — small hairline dingbats, asterisks, fleurons — separate longform sections. Used sparingly.

### Color

Color is editorial. The substrate carries warmth; accents are restrained and meaningful.

Substrate:

- Warm cream or off-white: `#FAF8F3`, `#F7F3EB`, `#F5F0E6`. The page reads as printed paper.
- Dark mode option: a warm dark, `#1E1B17` or `#1A1814`. Avoid neutral grays — the publication should hold its warmth even at night.

Ink:

- Primary body: warm dark, around `#1F1A14` on light substrate, `#F3EFE6` on dark.
- Secondary text: a warm gray, `#6B645A`.
- Tertiary text: lighter still, `#94897A`.

Accent (used for links, pull quotes, callouts):

- A single editorial color. Suitable choices: a deep burgundy `#7A1E1E`, a forest green `#1F4A2A`, a navy `#0F2C5B`. Always desaturated, always single-tone.
- Hyperlinks carry the accent with an underline. No bare blue links.

### Layout

Multi-column reading layouts at desktop, single-column at mobile. The grid is rhythmic, never rigid.

Grid logic:

- Two-column or three-column body grids at desktop for newspaper-style layouts; single dense column for essay format.
- Marginalia rail: a narrow right-rail at `200px` to `280px` reserved for sidenotes, related links, pull-quote callouts.
- Vertical rhythm by line-height: section spacing is a multiple of body line-height, not arbitrary.

Mastheads:

- Large display headline anchored top-left or center-justified depending on publication voice.
- Date, issue, section name in small uppercase tracked sans below the masthead.

Article openers:

- Article header occupies a generous vertical space, often a third to a half of the viewport.
- Hero imagery is wide, occasionally full-bleed, with a thin caption below.
- Author byline, read time, publication date set in sans below the headline.

Margins:

- Body column is bounded — `max-w-prose` or `max-w-2xl`. Long line lengths kill reading.
- Generous outer margins on desktop; narrower but never absent on mobile.

### Motion

Motion is invisible. The page is a printed object. Reveals are slow fades; nothing should pull the eye from the prose.

Appropriate motion:

- Fade-in on scroll for figure embeds at `600ms` with no translation.
- A subtle parallax on hero imagery — `0.05` to `0.1` of scroll speed — used at most once per article.
- Highlighted text reveal on click for annotated passages.

Inappropriate motion:

- Animations on text. Words do not enter from the side.
- Scroll-tied transformations on body content.
- Bouncy springs.
- Anything that distracts from reading.

### Components

Article cards:

- Headline in display serif at section size.
- Eyebrow with kicker (section name in uppercase tracked sans).
- Optional thumbnail, sized to a fixed aspect ratio.
- Byline and read time in sans below the headline.
- No box, no card chrome. Articles are listed, not boxed.

Pull quotes:

- Large body serif at `28px` to `36px`, tightened tracking, generous left and right margins.
- Hairline rule above and below — or a single hairline rule on the left if the quote sits in a margin rail.

Inline callouts:

- A small bordered box with hairline top and bottom rules only. No left/right borders.
- Used for asides, related-reading lists, factual notes.

Bylines and metadata:

- Author name in sans, weight medium.
- Date and read time in sans regular at a smaller size.
- A small avatar where the writer's identity is part of the brand; absent where it isn't.

Tables and citations:

- Footnotes set inside a section at the bottom, numbered.
- Citations follow a consistent style throughout. The chosen citation format is the publication's signature.

Navigation:

- A masthead bar with the publication name and a thin horizontal nav.
- A persistent table-of-contents rail on long-form articles, scroll-anchored.

### Visual moves (signature elements)

- Generous drop caps on lead articles.
- Hairline section dividers replacing solid colored bands.
- A single warm accent color used in links, pull quotes, and the rare CTA.
- Marginal notes in a narrow right-rail, set in sans at small size.
- Numbered footnotes anchored to the section bottom.
- Section dingbats — small hairline ornaments — separating subsections.
- A cover image treatment that mimics a magazine plate: full bleed, large caption, single sentence subhead.

### Banned in this style

- Sans-serif as the body face. The body is serif.
- Pill-shaped CTAs. Editorial calls-to-action sit inline as underlined links.
- Bright primary-color buttons.
- Glassmorphism, gradients, neon.
- Card grids with shadows. Articles are listed in flat rows, not card lifts.
- Heavy drop shadows of any kind.
- Auto-playing video in body.
- Emoji of any kind.

### Reference moods

- A literary magazine printed on uncoated stock with one accent ink.
- A weekly cultural publication with hand-set drop caps.
- A small-press essay quarterly bound by hand.
- A long-form profile in a newspaper's weekend section, set across three columns.
- A book of essays with generous margins and footnotes that earn their space.
- A travelogue with one large photo plate per chapter and prose that fills the rest.
- A bibliophile's website where the typography itself is the reason to visit.

---

## Quiet Emptiness

### When to use

Reach for Quiet Emptiness when restraint is the message. The surface communicates by what it withholds. Specifically:

- Gallery, atelier, and museum sites where the work is the content.
- Conceptual retail brands targeting customers who recognize the discipline.
- Premium designer marketing for an audience of designers — peer-facing work.
- Wabi-sabi-adjacent product lines emphasizing simplicity and natural materials.
- Conceptual fashion drops where the absence of marketing language is the marketing.
- Architecture firms, interior studios, and craft-led brands.
- High-end consumer hardware companion sites where the product photography breathes.

Avoid this style for: anything that needs to convert quickly, data-dense interfaces, products competing on feature volume, anything that has to explain itself to a cold audience.

### Typography

Type is whisper-quiet. Single family throughout. The font choice is not the move — the negative space around it is.

Single typeface across the system:

- A quiet, well-proportioned sans-serif at light to regular weight. Suitable choices: a humanist sans with subtle character, a contemporary geometric sans at thin to regular weights.
- Body size: `14px` to `15px`. Small relative to the canvas size.
- Display headlines remain modest: `32px` to `48px`. The system does not shout.
- Line-height: `1.6` to `1.8`. Air around every line.
- Tracking: neutral or slightly positive at display, neutral at body.

Color of type:

- Primary text is muted: `#2A2A2A` against light substrate, never pure black. The reduction in contrast is intentional.
- Secondary text: a pale gray, `#9A9A9A`. Almost too quiet to be functional — that is the point.

No display drama:

- No display serif. No oversized hero type. No tight tracking for emphasis.
- The system rejects every move that would call attention to the typography itself.

### Color

Color is severely limited. Most surfaces are a single off-white. Color enters only as a single muted tone, used once per page at most.

Substrate:

- Warm off-white: `#F8F6F2`, `#F5F3EE`. Never pure white.
- Optional dark variant: deep warm gray, `#1F1D1A`.

Ink:

- Primary text muted: `#2A2A2A` to `#363432`.
- Secondary text: a pale gray, `#9A9A9A`.
- Tertiary text disappears into the substrate: `#C2C0BC`.

Accent (if any):

- A single soft tone — pale terracotta, dusty sage, warm ochre — used surgically, often in a brand mark or a single rule line. Saturation low (`30-40%`), value high.
- Most surfaces should ship without any accent at all.

### Layout

Negative space is the layout. Content occupies a small fraction of the canvas; the rest is empty by design.

Macro-spacing:

- Sections separated by `200px` to `400px` of pure whitespace. The reader is asked to scroll through emptiness.
- Content blocks occupy at most 40 percent of viewport area on desktop. The remaining 60 percent is empty.

Asymmetry:

- Elements sit off-center, anchored to a single rail. A heading might float at the top-left while its supporting paragraph sits in a small column on the right.
- No balanced columns. The composition is intentionally lopsided.

Grid logic:

- A loose grid. Twelve columns, but most content spans three to five — never the full width.
- Images sit on the grid but at small fractional widths, sometimes a single column wide, sometimes spanning seven.

Mobile:

- Single column with the same generous emptiness preserved. Sections still have `120px` to `200px` of vertical breathing room.

### Motion

Motion is barely present. When it appears, it is slow and almost imperceptible.

Appropriate motion:

- Slow fade-in on scroll: `1200ms` with `cubic-bezier(0.25, 1, 0.5, 1)`. No translation.
- Hover state on links: a soft underline reveal at `400ms`.
- Page transitions: a `600ms` opacity crossfade.

Inappropriate motion:

- Any scroll-driven animation. The page is a still object.
- Spring physics. The system does not perform.
- Looping background motion. The page rests.
- Cursor-following effects. The visitor's cursor is not an event.

### Components

Buttons:

- Almost absent. When present, a single hairline border around small sans text — `1px solid #E0DDD7`, `8px` padding, no fill.
- Hover state: a subtle border darken at `400ms`. No background change.
- Primary CTA is the only filled button on the entire surface, and even then, the fill is the ink color at low contrast.

Navigation:

- A single horizontal rail at the top with three or four links. No logo if the brand mark is the page itself.
- Inactive links sit at tertiary gray. Active link in primary ink.

Cards:

- Not used. Content sits flat on the canvas. Hairlines separate sections at most.

Forms:

- Inputs are a single hairline at the bottom only. Labels above in sans at small size.
- Errors are a single line of muted ink. No color, no icon, no urgency.

Images:

- Photographs sit at small fractional widths, often centered within a much larger empty column.
- Aspect ratios vary intentionally — square, portrait, occasional wide landscape — but never random.

Galleries:

- Vertical scroll with one image per viewport. The image occupies 30-40 percent of the screen; the rest is empty.

### Visual moves (signature elements)

- Massive negative space, 60-70 percent of the visible viewport at all times.
- A single small detail — a hairline, a small caption, a single photograph — placed in vast emptiness.
- Asymmetric anchoring. Content never centers.
- Type set at small sizes against vast canvases. Whisper, never shout.
- A single muted accent used once, if at all.
- Hairline section separators replacing every other section divider convention.
- Photography that breathes, set at intentionally small fractional widths.

### Banned in this style

- Decorative anything. No ornament can justify itself.
- Cards or boxes of any kind.
- Drop shadows.
- Gradients.
- Saturated accents.
- Glassmorphism, backdrop blur.
- Animated state changes beyond opacity.
- Display type at oversized scale.
- Pill buttons, filled buttons in saturated color.
- Auto-playing video.
- Emoji of any kind.

### Reference moods

- A gallery on opening day before the crowd arrives.
- A high-end stationery showroom with one product on each shelf.
- An atelier where the work is laid on a single cotton drape.
- A printed photo book with one image per spread and no captions.
- A craft retailer's website where each product gets its own page and no surrounding noise.
- A monograph that takes ten pages to introduce its subject.
- A wabi-sabi tea ceremony website where the smallest detail is meant to be noticed.
- An interior studio's portfolio where the rooms photographed are mostly empty.

---

## Bold Maximalism

### When to use

Reach for Bold Maximalism when the product earns its volume. The surface celebrates rather than restrains. Specifically:

- Creator-economy tools where the user is themselves a brand.
- Indie game studios, music labels, and entertainment products.
- Brand drops, capsule collections, and limited-run merchandise.
- Conferences, festivals, and event microsites where the page is the experience.
- Cultural and arts platforms with strong editorial voice.
- Youth-targeted products where reading "loud" is a feature, not a bug.
- Marketing surfaces for products whose voice is the differentiator.

Avoid this style for: enterprise platforms, regulated industries, products targeting calm or considered audiences, anything where "trust through restraint" is the brand promise.

### Typography

Type is loud and varied. Multiple display faces appear in a single layout. Weight, scale, and color contrast carry the energy.

Display stack:

- Pick two display faces — one expressive (a stylized display sans, an extreme grotesque, a decorative serif) and one workhorse (a clean geometric sans).
- Display scales are aggressive: `120px` to `280px`. Headlines occupy half the viewport.
- Tracking: tight at display scale, `-0.02em` to `-0.05em`.
- Weight contrast: ultra-bold paired with light. Both extremes carry weight in a single section.

Body:

- A geometric sans at `16px` to `18px`. The body remains readable while the display goes wild.
- Line-height: `1.4` to `1.6`. Tighter than editorial; the body keeps up with the energy above.

Eyebrows and microcopy:

- Uppercase tracked at sizes that match the energy: `14px` to `18px`, not the conventional `10px`.
- Used as section signposts but loud — high contrast against the body.

Decorative type:

- A third decorative face — a stylized serif, a script, an extreme display — may appear once per surface as an accent moment. Used surgically.

### Color

Saturated, layered, fearless. Multiple colors per surface. Backgrounds carry chromatic weight.

Palette:

- A primary palette of three to five saturated colors — a hot red, a cobalt, a chartreuse, a deep purple, a sunny yellow. Saturation `70-90%`.
- Each color carries semantic or section meaning. Sections shift palette as the page progresses.
- Background colors are bold. A section may sit on a full-bleed cobalt. The next sits on chartreuse. The next on cream.

Type color:

- Type adapts to the substrate. White on dark sections, dark on light. Never mid-gray — the contrast is the point.

Accents:

- Full-bleed color blocks separate sections.
- Color is used as personality, not just as functional accent.

### Layout

Layered, kinetic, willingness to break the grid. Elements overlap, rotate, escape their containers.

Grid logic:

- A grid exists, but breakage is intentional. Elements that span two grid cells, elements offset by a quarter-column.
- Overlapping content: an oversized headline that bleeds across a photographic background.
- Rotated elements at `-2deg` to `5deg` — a card askew, a label tilted.

Composition:

- Layered illustrations stacked with depth.
- Type interacting with imagery: words wrapping around photographs, type behind objects.
- Full-bleed photographic sections alternating with full-bleed color blocks.

Density:

- High. The page is loaded with content, but content is composed, not crammed. Every layer earns its place.

Mobile:

- Layouts reflow but the energy preserves. Overlaps remain; rotations may flatten; colors stay.

### Motion

Motion is expressive and abundant. The surface moves continuously, but every motion has a beat.

Appropriate motion:

- Aggressive scroll entries: type rises from `translate-y-32` with rotation snapping to neutral over `800ms`.
- Marquee scrolls with bold type that loops without pause.
- Gestural hover effects: cards that lift, rotate, and reveal additional content on hover.
- Color flips on tap: backgrounds change color at the press of a CTA.
- Sound on intentional interaction (with a clearly-marked mute toggle).

Inappropriate motion:

- Quiet fades. The system does not whisper.
- Slow easing. Motion is snappy.
- Static states for elements that the page treats as kinetic centerpieces.

### Components

Buttons:

- Bold, oversized, saturated fill. Padding generous: `20px 32px` minimum.
- Type is bold uppercase at `16px` to `18px`, tracked moderately.
- Hover: a scale-up to `1.05` with a snappy spring.
- Active: scale to `0.95` with a satisfying physical feel.

Cards:

- Filled, high-contrast, often rotated slightly.
- Internal padding is moderate to allow content to breathe within the loud frame.
- Hover: a lift with a hard shadow offset (e.g., `8px 8px 0 currentColor`).

Navigation:

- Heavy. The brand mark is large; the navigation items are typographically bold.
- Mobile nav opens full-screen with massive type and bold color blocks per item.

Forms:

- Inputs are filled with a saturated low-opacity tint of the brand color.
- Labels in bold uppercase tracked sans.
- Errors in a contrasting saturated red with a small icon or character marker.

Imagery:

- Photography is high-contrast, saturated, occasionally cut-out with hard edges.
- Custom illustration is welcome — bold, flat, oversized.
- Photo treatments include duotones in brand palette pairs.

Headlines:

- Frequently span multiple lines with intentional line-breaks for rhythm.
- Mix faces within a single headline — display sans for the noun, decorative serif for the verb.

### Visual moves (signature elements)

- Oversized typography that crops at the viewport edge.
- Multiple display faces in a single layout — two minimum, three in headlines that combine moods.
- Saturated full-bleed color blocks as section dividers.
- Layered illustration with depth and overlap.
- Rotated cards and labels at small angles (`-3deg` to `3deg`).
- Marquee scrolls of bold type running across the viewport.
- Sound cues on intentional events (with an obvious mute control).
- Decorative emoji-style illustrated icons (custom illustration, never literal emoji) at oversized scale.

### Banned in this style

- Pure neutrals only. The system requires color.
- Tiny typography. Display sizes must commit.
- Restrained motion. Everything moves with intent.
- Generic stock photography. Imagery is custom or curated.
- Hairline borders. Borders, when present, are heavy and saturated.
- Glassmorphism in the high-end manner — Bold Maximalism uses solid color, not translucency.
- Centered, balanced compositions as a default — asymmetric overlap is the move.
- Emoji as icons. Use custom illustrated marks instead.

### Reference moods

- A festival poster wall stapled in layers, the bottom poster still visible behind the top.
- A late-2000s indie record label site with hand-lettered logo and saturated color blocks.
- A teen magazine cover with three competing headlines all set at full scale.
- A music streaming app's editorial playlist banner where the artwork shouts.
- A gallery opening invitation set on construction paper with stamped type.
- A toy store window display with primary colors against painted wood.
- A skateboard graphic where the deck design is louder than the brand mark.

---

## Refined Minimalism

### When to use

Refined Minimalism shares restraint with the broader Minimalist system but adds a deliberate signature touch. Reach for it when the brief asks for "considered" — calm but distinctive — rather than "quiet." Specifically:

- Premium fintech and treasury products targeting deliberate audiences.
- Design-tool marketing pages aimed at designers and developers.
- Indie products that aim for "considered" and want to read as taste-led rather than minimal-by-default.
- Small-team SaaS where the marketing is the proof of craft.
- Premium hardware companion apps where the device is the hero but the app has personality.
- Single-purpose tools whose marketing should outshine its enterprise competitors.

Avoid this style for: any context where the basic Minimalist system serves better — long-form publishing, dashboards, documentation. Reach for it specifically when the brief calls for restraint with a signature.

### Typography

Sans-only system. One distinctive display face, one workhorse body face. The display face is the signature.

Display sans (the brand's voice):

- A distinctive contemporary display sans. Suitable choices include modern variable sans-serifs with character — clean, considered, slightly idiosyncratic in proportion or detail.
- Display size: `48px` to `96px`. Restrained relative to maximalist styles but confident.
- Tracking: tight at display, `-0.02em` to `-0.04em`.
- Weight: medium to semibold. Not heavy.
- Line-height: `1.05` to `1.15`.

Body sans:

- A workhorse sans paired with the display. Should be visually quieter — neutral grotesque, clean geometric.
- Body size: `16px` to `17px`. Generous for screen.
- Line-height: `1.55` to `1.65`.

Eyebrows:

- Uppercase tracked at `+0.08em`, sized `11px` to `13px`. Used at major section openings.

Numerals:

- Tabular for stats and prices. Proportional for prose.

### Color

A warm off-white canvas, a single high-contrast accent, generous use of neutral grays for hierarchy. The system uses one chromatic note across the entire surface.

Substrate:

- Warm off-white: `#FAFAF8`, `#F7F6F3`. Never pure white.
- Surface fills: `#FFFFFF` against the warm canvas for layered cards.

Ink:

- Primary text: `#0F0F0F` or `#111111`. Strong, not pure black.
- Secondary text: a warm gray, `#666666` to `#787878`.
- Tertiary text: lighter, `#A0A0A0`.

Accent (the single chromatic note):

- One high-contrast, restrained color. Suitable choices: a deep emerald `#006D5B`, an electric blue `#1E4BFF`, a deep rose `#C5395E`, a warm amber `#C77F00`.
- Used in: the primary CTA fill, link color, an occasional underline, the brand mark.
- Saturation: `60-75%`. Lower than maximalist; higher than the minimalist pastel system.

### Layout

Generous whitespace with deliberate composition. Asymmetric splits, intentional alignment shifts, considered scale variation.

Grid logic:

- A twelve-column grid with deliberate column-span variance. Hero sits at `7/12` on the left or right, with whitespace filling the rest.
- Bento layouts where each card has a defined column span — `4/12`, `8/12`, `5/12`, `7/12`. Mathematical, not random.
- Section breaks: `96px` to `160px` of vertical whitespace.

Alignment:

- Left-aligned by default. Center alignment is a deliberate choice for one or two surfaces — a final CTA, a major lockup.
- Right-aligned for numerals and small captions only.

Cards:

- `1px` hairline borders in `rgba(0,0,0,0.06)`. Subtle but present.
- Border radius: `8px` to `12px`. Modest but present.
- Internal padding: `28px` to `36px`.

Density:

- Low. Each card carries one concept. Each section communicates one idea.

### Motion

Motion is present, intentional, and quiet. Every transition is custom-eased; nothing reads as default.

Easing:

- All transitions use custom cubic-beziers. A reliable set: `cubic-bezier(0.16, 1, 0.3, 1)` for entries, `cubic-bezier(0.4, 0, 0.2, 1)` for state changes.
- Durations: `250ms` to `400ms` for micro, `500ms` to `700ms` for entry reveals.

Scroll entry:

- Subtle `translateY(8px)` with `opacity` from `0` to `1` over `500ms` to `700ms`.
- Stagger via `animation-delay` proportional to element index.

Hover states:

- Buttons darken slightly and scale to `0.98` on active.
- Cards lift by `2px` with a subtle shadow shift.
- Links underline reveal at `200ms`.

### Components

Buttons:

- Primary: solid ink fill or accent fill, white text, `8px` to `12px` radius, generous padding.
- Secondary: hairline border, ink text, hover darkens the border.
- Tertiary: text-only with underline on hover.

Cards:

- Hairline border, modest radius, white surface on warm canvas.
- Internal hierarchy: small uppercase eyebrow, mid-size headline in display sans, body paragraph in body sans, optional CTA below.

Navigation:

- Thin horizontal rail with text links in body sans at moderate weight.
- A single primary CTA at the right edge in the accent.
- Optional subtle blur on scroll (the only place blur appears in this system).

Forms:

- Inputs: hairline border, modest radius, generous padding, focus ring in the accent.
- Labels above inputs in sentence case.
- Helper text below, errors below in a darkened version of the accent.

Charts:

- Single-line charts in the accent color against a subtle background gradient (very subtle — `2%` opacity).
- Data points highlighted with small filled dots in the accent.
- Tooltips rendered as small white cards with a hairline border.

Tables:

- Subtle row separation via hairline rules.
- Numeric cells right-aligned with tabular figures.
- Header row in slightly heavier weight, uppercase optional.

### Visual moves (signature elements)

- A single accent color, used surgically across the whole surface.
- The distinctive display sans as the signature voice.
- Asymmetric bento with mathematically intentional spans.
- Hairline borders in `rgba(0,0,0,0.06)`.
- A small detail — an offset shape, a single inline keystroke key, a subtle highlight — that reads as the craft signature.
- Generous whitespace but never the severity of the quiet-emptiness system.
- A single eyebrow per major section, tracked and consistent.
- Subtle scroll-entry motion that never calls attention to itself.

### Banned in this style

- Multiple accent colors. One chromatic note, period.
- Heavy drop shadows.
- Gradients beyond very subtle background washes.
- Default humanist sans as the display face. The display face must be deliberate.
- Pill cards. Pills reserved for tags and the occasional CTA.
- Cluttered hero sections.
- Bouncy spring motion.
- Decorative emoji.
- Generic stock photography.

### Reference moods

- A small-team SaaS marketing site where every line reads as authored.
- A premium accounting tool's landing page that feels nothing like the enterprise category.
- A boutique fintech's homepage that signals taste before it signals competence.
- A design-tool's brand site where the marketing proves the product's eye.
- An indie hardware companion app whose marketing matches the unboxing.
- A founder-led product's homepage that reads as one person's craft.

---

## Aurora Glass

### When to use

Reach for Aurora Glass when the brief asks for "magic" — atmospheric, generative, cinematic. The surface communicates leap and possibility. Specifically:

- AI products targeting broad consumer or creator audiences.
- Creator tools and generative-art platforms where the surface should match the tool's output.
- Premium consumer brands where atmosphere is the offering.
- Music streaming and entertainment surfaces where mood matters.
- Hospitality and luxury brands targeting design-literate audiences.
- Awards-targeting agency portfolios.
- Conference microsites for events with high production value.

Avoid this style for: data interfaces, regulated industries, products where "magic" reads as untrustworthy, accessibility-critical flows, or audiences that read gradient maximalism as the AI category default.

### Typography

Display-led system. Modern variable sans paired with optional editorial serif for moments. Tracking and weight contrast carry hierarchy.

Display (the centerpiece):

- A modern variable display sans with wide proportions, or a contemporary editorial serif with optical contrast.
- Display sizes are enormous: `96px` to `200px` on hero sections. Headlines occupy meaningful viewport area.
- Tracking: tight at display, `-0.02em` to `-0.04em`.
- Weight: variable, leaning lighter at larger sizes. The system favors elegant, never heavy.

Body:

- A clean variable sans at `15px` to `17px`. Line-height `1.5` to `1.6`.
- White or near-white text on the typical dark substrate.

Eyebrows:

- Microscopic pill-shaped tags at `10px` to `11px`, uppercase tracked `+0.15em` to `+0.2em`.
- Sit immediately above headlines as preamble.

### Color

Atmospheric. The substrate is deep dark; gradients sit behind everything, narrowly hue-spread, slowly drifting.

Substrate:

- Deep OLED black: `#050505` to `#0A0A0A`. Avoid pure black.
- Surface fills: near-vantablack with hairline white borders at low opacity.

Mesh gradient backgrounds:

- Radial orbs of color bleed and overlap softly behind hero text.
- Hue palettes (pick one per project):
  - Deep purple to indigo to magenta — for AI, creator tools.
  - Emerald to teal to deep blue — for technical premium.
  - Warm amber to deep rose to violet — for hospitality, luxury.
  - Cool cyan to electric blue to midnight — for data and music.
- Saturation moderate (`60-70%`); never crass. Brightness modest so type stays legible.

Surfaces (glass cards):

- Background: near-vantablack with heavy backdrop blur.
- Border: hairline white at `rgba(255,255,255,0.08)` to `rgba(255,255,255,0.12)`.
- Inner highlight: a single `1px` inset top highlight at low opacity, suggesting glass catching light.

Accents:

- One vibrant accent per project — a single saturated color used for CTA fills, primary glyphs, and the brand mark.

### Layout

Composed, atmospheric, generous. The page is a sequence of cinematic stages.

Macro-spacing:

- Section padding: `py-32` to `py-48` minimum.
- Hero sections occupy at least `100dvh`. The first impression is meant to land.

Layout archetypes:

- Asymmetric splits with the hero anchored to one side, a generative visual on the other.
- Z-axis cascade where elements stack with subtle rotation and overlap.
- Full-bleed hero with the headline at the lower third, the upper two thirds carrying the mesh gradient.

Card system (double-bezel):

- Every premium container uses an outer shell and an inner core with concentric radii.
- Outer shell: subtle background, hairline ring, large radius (`rounded-[2rem]`).
- Inner core: distinct surface, inner highlight, mathematically smaller radius.

Eyebrow rhythm:

- Eyebrow → headline → body → action repeats per major section.

Mobile:

- All asymmetric layouts collapse to single column with generous vertical spacing preserved. Glass treatments simplify but remain.

### Motion

Cinematic, premium, every transition simulating real-world physics.

Easing:

- Custom cubic-beziers throughout. `cubic-bezier(0.32, 0.72, 0, 1)` for entries; `cubic-bezier(0.4, 0, 0.2, 1)` for state changes.
- Durations: `700ms` to `900ms` for major entries, `300ms` to `500ms` for state changes.

Scroll entries:

- Combined `translate-y-16` with `blur-md` resolving to neutral over `800ms`.
- The blur element is critical — it gives the surface its "settling into focus" quality.

Background animation:

- Mesh gradient orbs drift slowly. `40s` to `60s` per orbit. Almost imperceptible.
- Animation attached to a `position: fixed; pointer-events: none` layer. Never to scrolling content.

Magnetic hover physics:

- Buttons with nested icon circles translate diagonally and scale up on hover. The parent button scales down on press.

Page transitions:

- Crossfades over `400ms` with a slight blur in/out for premium framing.

### Components

Buttons:

- Primary: pill-shaped, fully rounded, accent fill, white text.
- The button-in-button pattern for any CTA with a trailing icon — the arrow lives inside its own circular wrapper.
- Secondary: pill shape with `bg-white/5` fill and a hairline ring.

Cards:

- Double-bezel pattern mandatory.
- Glass treatment: backdrop blur, hairline border, inset highlight.
- Internal padding generous: `32px` to `48px`.

Navigation:

- Floating glass pill detached from the viewport top with `24px` to `32px` of margin.
- Content: brand mark, three to five primary links, one primary CTA.
- Pill darkens or intensifies blur on scroll past hero.

Forms:

- Inputs sit inside the bezel pattern. Outer ring, inner highlight.
- Focus state intensifies the inner ring and adds a soft outer glow keyed to the vibe accent.

Modals:

- Full-screen takeover. Heavy backdrop blur. Dim layer. Content inside uses double-bezel.

Imagery:

- Product mockups wrapped in the double-bezel at hero scale. Subtle perspective tilt — `rotateX(8deg)` paired with `rotateY(-4deg)`.

Eyebrow tags:

- Microscopic pill-shaped badges with the same glass treatment as cards.

### Visual moves (signature elements)

- Slow-drifting mesh gradient backgrounds with narrow hue spread.
- Liquid glass cards with backdrop blur and hairline borders.
- The double-bezel concentric radius pattern across every premium container.
- Floating glass pill navigation detached from the viewport edge.
- Holographic or iridescent micro-accents used surgically.
- Cinematic scroll entries with motion blur dissolving into focus.
- Magnetic button hover physics with the button-in-button pattern.
- Subtle film-grain overlay at very low opacity (`0.03`) on fixed layers.
- Hero imagery rendered as a physical artifact — framed, tilted, lit.

### Banned in this style

- Backdrop blur on scrolling content (kills performance on mobile).
- Bright primary-color hero sections.
- Default humanist sans-serifs.
- Generic thick-stroke icon libraries.
- Standard `linear` or `ease-in-out` transitions.
- Cards placed bare on the background without bezel treatment.
- CTAs with naked trailing arrows.
- Z-index sprawl.
- Auto-playing audio.
- Phone-tilt parallax — pointer events only.
- Emoji of any kind.

### Reference moods

- A late-evening boutique window display lit from within, seen through misted glass.
- A flagship product unveiling shot in slow motion under controlled light.
- A premium hardware studio shot, two soft sources, every facet of the object considered.
- A film title sequence dissolving from atmospheric backdrop into clean type.
- A music streaming app's landing page where the playlist artwork sets the mood.
- A creator tool's marketing site where the tool's output is the brand argument.
- A perfume campaign whose hero is the glass bottle.
- A gallery installation lit so each object floats away from its plinth.

---

## Retro-Futurist

### When to use

Reach for Retro-Futurist when the audience rewards energy and nostalgia. Chrome, holographic accents, blobby shapes, pixel marks. Specifically:

- Indie games and game studios targeting Gen-Z and millennial gamers.
- Music streaming brands aimed at younger audiences.
- Fashion drops, capsule collections, and limited-edition merchandise.
- Festival microsites for music and culture events.
- Web3 and crypto products where the aesthetic doubles as positioning.
- Skateboard, surf, and youth-culture brands.
- Marketing surfaces for products whose primary differentiator is mood.

Avoid this style for: enterprise platforms, regulated industries, products targeting older or more conservative audiences, anything where serious-and-trustworthy is the brand promise.

### Typography

Pixel marks paired with workhorse sans. Decorative type is the signature; body type remains functional.

Display:

- A pixel face or a stylized bitmap face for accent moments. Used surgically — page header, key callouts, button labels.
- A modern geometric sans for primary display headlines. Scale `64px` to `144px`.
- Tracking: tight at display, `-0.02em` to `-0.04em`.

Body:

- A clean geometric sans at `15px` to `17px`. Line-height `1.5` to `1.6`.
- Body remains readable; the pixel face is decoration, not utility.

Eyebrows:

- Pixel face at small size (`10px` to `12px`) for system labels and category tags.
- Uppercase tracked sans for conventional eyebrows.

### Color

Saturated and reflective. Chrome silvers, holographic blends, candy-bright primaries paired with deep purples and electric blues.

Palette options:

- **Chrome holographic**: silver `#C0C0C0` with iridescent gradients (pink-to-cyan, gold-to-violet) on highlights. Deep navy substrate.
- **Y2K candy**: hot pink `#FF1B6B`, electric blue `#1AC8F0`, silver, lavender `#C7A6FF`. White or pale-pink substrate.
- **Vapor**: pastel purple, cyan, magenta with soft gradients. Deep purple substrate.

Type color:

- White on dark substrate, deep navy on light. Pixel-face accents in saturated brand color.

Gradients:

- Holographic blends — pink to cyan, gold to violet — used on small surfaces (a button hover state, a single header glyph, a logo treatment). Never as full-page substrate.

### Layout

Layered, playful, organic. Blobby SVG shapes, overlapping elements, intentional asymmetry.

Grid logic:

- A loose grid with intentional escape. Elements overlap, rotate, sit on blobby SVG backgrounds.
- Section breaks: blobby SVG dividers, not hairline rules.

Composition:

- Layered illustration with depth — chrome 3D objects, holographic stickers, pixel-art icons.
- Type interacting with imagery: words wrapping blobby shapes, type set inside chrome plates.

Density:

- Moderate. The page feels full but composed. Every layer earns its place.

Mobile:

- Layouts reflow; overlaps soften but remain. Blob shapes scale down; chrome accents stay.

### Motion

Kinetic and playful. The system embraces movement.

Appropriate motion:

- Hover effects with bouncy springs on chrome and pixel elements.
- Cursor-following holographic highlights on small interactive surfaces.
- Looping marquee scrolls with retro-futurist type.
- Glitch effects on critical moments (page entry, CTA hover).
- Subtle chrome shimmer animations on key brand elements.

Inappropriate motion:

- Quiet restraint. The system rejects subtlety.
- Pure linear easing. Motion bounces, glitches, or shimmers — never just slides.

### Components

Buttons:

- Chrome-finished pills with a metallic gradient and `2px` hairline highlight at the top.
- Hover: pixel-face label glitches briefly, then resettles.
- Active: chrome scales to `0.95` with a satisfying snap.

Cards:

- Layered, often with holographic stickers attached at corners.
- Background: pale pearl or candy color with subtle chrome border treatment.
- Hover: an iridescent gradient sweeps across the card.

Navigation:

- A floating chrome bar with the brand mark in pixel face.
- Items in geometric sans with hover effect that glitches the label briefly.

Forms:

- Inputs with chrome-bezel borders and subtle gradient fills.
- Labels in pixel face at small size for retro signal.
- Errors as glitch effects on the input field.

Imagery:

- Chrome 3D renders, holographic stickers, pixel-art accents.
- Layered illustration with depth.
- Custom illustration only — stock imagery breaks the aesthetic instantly.

Stickers and ornaments:

- Holographic decals attached to cards and hero sections.
- Pixel-art rosettes and stars used as bullet markers and dividers.

### Visual moves (signature elements)

- Chrome bezels on every primary CTA.
- Holographic gradients on highlights and brand marks.
- Pixel-face type as decorative accent.
- Blobby SVG shapes as section dividers and backgrounds.
- Layered illustration with depth — chrome objects, holographic stickers, pixel icons.
- Glitch motion on key interactions.
- Cursor-following holographic highlights on small surfaces.
- Saturated candy palette with deep substrate anchoring.

### Banned in this style

- Pure neutrals only. The system requires color and chrome.
- Modern flat illustrations. Illustration must carry depth and reflectivity.
- Restrained motion. Everything bounces, glitches, or shimmers.
- Default humanist sans alone — the pixel face must appear somewhere.
- Generic stock photography.
- Hairline-only borders. Borders are chromatic or chrome.
- Glassmorphism in the aurora manner — this system uses chrome reflection, not translucent blur.

### Reference moods

- A late-90s arcade cabinet with chrome trim and pixel marquee.
- A Y2K teen-magazine cover with holographic foil stamps.
- A vaporwave album cover with chrome 3D objects floating on gradient.
- An early-2000s music channel bumper with glitching pixel logos.
- A skateboard graphic with chrome plating and pixel rosette.
- A capsule fashion drop's lookbook with metallic foiling on the cover.
- A retro-gaming console's web showcase where chrome and pixel mix.

---

## Organic Hand-drawn

### When to use

Reach for Organic Hand-drawn when warmth is the primary brand requirement. The surface communicates "made by a person." Specifically:

- Consumer wellness products targeting calm and care.
- Family and kids' education tools where friendliness is the contract.
- Indie creator newsletters and personal brands where the writer is the product.
- Boutique consumer goods — soap, candles, ceramics, niche apparel.
- Plant, garden, and craft platforms.
- Community-led platforms where personality is the differentiator from enterprise alternatives.
- Holiday and gift-giving microsites.

Avoid this style for: enterprise platforms, technical products, regulated industries, anything where "professional polish" reads as a brand requirement.

### Typography

Sans with personality paired with optional hand-lettered accents. Body is calm; display has warmth.

Body sans:

- A friendly humanist sans with rounded forms. Body size `16px` to `17px`.
- Line-height: `1.55` to `1.7` for generous reading.
- Letter-spacing neutral.

Display sans:

- A geometric sans with character — rounded geometric, friendly grotesque. Display size `40px` to `72px`.
- Weight: medium to semibold. Never heavy.
- Tracking: tight to neutral.

Hand-lettered accents:

- A single hand-lettered face used surgically — for a brand mark, a single headline emphasis, a callout label. Never for body or general headlines.
- Suitable choices: a casual script, a hand-drawn marker face. Used sparingly so it remains charming.

### Color

Warm, soft, earthy. Cream substrates, coral and sage accents, occasional terracotta.

Substrate:

- Warm cream: `#FAF6EE`, `#F8F2E8`. Never pure white.
- Optional warm earth tones: `#F0E8D8` (parchment), `#EFE5D0` (oat).

Ink:

- Primary text: warm dark, around `#3A2E25` or `#2C2419`. Never pure black.
- Secondary text: warm gray, `#7C6F60`.
- Tertiary text: lighter, `#A39A8B`.

Accents (the warm palette):

- Coral: `#E8745C`. Used for primary CTAs and key callouts.
- Sage: `#A8B89A`. Used for category labels, secondary actions.
- Terracotta: `#C76A3E`. Used for warm accents.
- Mustard: `#D9A93B`. Used surgically for highlights.
- Soft blue: `#9ABBC9`. Used as quiet support.

### Layout

Rounded, soft, generous. Hard edges and grid rigidity give way to organic shapes and intuitive spacing.

Grid logic:

- A loose grid. Twelve columns at desktop but heavy reliance on uneven spans and floated layouts.
- Cards have generous rounded radii — `16px` to `24px`.
- Section dividers are often custom illustrations or soft gradient washes, not hairlines.

Composition:

- Custom illustration paired with type. Illustrations are warm, hand-feel, occasionally watercolor.
- Type often offset by small illustrated elements — a sprig, a leaf, a small drawn flourish.

Margins:

- Generous. The page breathes.
- Asymmetric padding allowed — a section may have wider padding on one side, narrower on the other.

Mobile:

- Layouts collapse gracefully. Rounded radii preserve at scale; illustrations scale down without losing texture.

### Motion

Soft and warm. Bouncy springs on small interactions; gentle reveals.

Appropriate motion:

- Spring physics on small elements (badges, illustration accents).
- Gentle scroll entries with `translate-y-6` and `opacity` over `500ms` with `cubic-bezier(0.16, 1, 0.3, 1)`.
- Hover effects with subtle rotation (`-2deg` to `2deg`) on illustrated elements.
- Smooth color shifts on hover for buttons.

Inappropriate motion:

- Aggressive bounces. The system is warm, not playful.
- Glitch effects.
- Scroll-jacking.
- Cursor-following effects on every clickable element.

### Components

Buttons:

- Primary: rounded radius (`12px` to `16px`), warm accent fill (coral or sage), warm dark text.
- Hover: subtle scale-up to `1.02` with a soft spring.
- Active: scale to `0.98`.
- Secondary: outlined with the accent color, transparent fill.

Cards:

- Generous rounded radii (`20px` to `24px`).
- Cream or layered surface fill with a subtle warm shadow (`0 8px 24px rgba(58, 46, 37, 0.06)`).
- Internal padding: `24px` to `32px`.
- Optional illustrated accent — a small drawn element in a corner.

Navigation:

- A thin horizontal rail with rounded illustrated brand mark on the left.
- Items in body sans at medium weight.
- A single warm CTA at the right edge.

Forms:

- Inputs with generous rounded radii (`12px`), warm border (`1.5px solid #E8E0D0`), focus state with a coral or sage glow.
- Labels above inputs in friendly sentence case.
- Errors in coral with a soft icon (a drawn outline).

Illustration:

- Custom illustration sets are mandatory — Lucide and Heroicons stand out and break the aesthetic.
- Suitable styles: hand-drawn outline, soft watercolor, simple flat illustration with subtle texture.
- Illustrations carry warm color and have visible "made by hand" qualities.

Imagery:

- Photography is warm-toned, naturally lit, slightly soft. Candid over staged.
- Treatments: gentle warm overlay, no high-contrast filters.

### Visual moves (signature elements)

- Custom hand-drawn illustration paired with type throughout.
- Generous rounded radii on every interactive element.
- Warm cream substrate with one to two accent tones (coral, sage, terracotta).
- A single hand-lettered face used surgically for a brand mark or single callout.
- Soft drawn flourishes — sprigs, leaves, small organic shapes — between sections.
- Photography with warm overlays and natural light.
- A small illustrated mascot or recurring motif that signals the brand's personality.
- Section dividers made from soft watercolor washes or hand-drawn elements.

### Banned in this style

- Sharp `90°` corners on interactive elements.
- Default Lucide / Heroicons icon sets — they stand out as machine.
- Lorem ipsum or generic stock photography.
- Cool, technical color palettes.
- Heavy drop shadows. Shadows here are warm and diffuse.
- Bold maximalist gestures — the system is warm, not loud.
- Multiple hand-lettered faces in one layout. One, used surgically.
- Emoji as substitutes for illustrated marks. Custom illustration only.

### Reference moods

- A neighborhood ceramics studio's website with hand-glazed mugs and warm photography.
- A small herb farm's online shop where each product card is illustrated by hand.
- A children's bookstore site with a recurring illustrated cat as the brand mascot.
- A small-batch soap maker's product pages where the illustrations match the bottles.
- A wellness retreat's booking page with watercolor washes between sections.
- A personal newsletter where the writer's hand-drawn logo appears at the top of every issue.
- A community garden's seasonal calendar with illustrated months and warm typography.
- An indie maker's shop page where the photography matches the kitchen-table aesthetic of the work.

---

## Anti-Design Web

### When to use

Reach for Anti-Design Web when the brief is a deliberate statement. The aesthetic rejects design polish on purpose. Specifically:

- Anti-corporate brand statements where polish reads as deceit.
- Designer portfolios making a conceptual point about the design industry.
- Art installations and conceptual web pieces.
- Indie publications whose voice is contrarian to mainstream tech.
- Underground music labels, zines, and counterculture brands.
- Provocative campaigns where the medium is the message.
- Personal sites whose author is explicitly rejecting the SaaS aesthetic.

Avoid this style for: any commercial product whose audience expects professionalism, anything regulated, anything where readability and trust are non-negotiable, anything where the audience does not share the in-joke.

### Typography

System defaults intentionally. The page wears the browser's font stack as a badge. Decoration appears via misuse of conventional roles.

Body type:

- System default sans or system default serif. The fallback chain that ships with the browser is THE choice.
- Times New Roman as headline. Arial or Helvetica as body. The defaults the corporate web spent two decades replacing.
- Size: `16px` or `18px`. Generous on purpose, undecorated.

Display type:

- Same system fonts at larger sizes. No display face brought in.
- Optional appropriation: a casual face used as if by mistake — for an inappropriate context. The juxtaposition is the move.

Casing and weight:

- Mix freely. UPPERCASE PARAGRAPHS appear. Bold and italic combine in single phrases. The system rejects typographic discipline.

Underlines:

- Hyperlinks are blue and underlined. Visited links are purple and underlined.
- The browser default link styles are preserved.

### Color

Web-native primaries. Harsh blue, harsh red, harsh yellow. White or institutional gray substrate.

Substrate:

- Pure white `#FFFFFF` or a default institutional gray `#C0C0C0`.
- Dark variant: pure black `#000000` — the only place pure black is permitted in this library, and it's permitted because the system is making a point.

Type:

- Black on white substrate.
- White on black substrate.
- Bright blue, bright red, bright yellow used as accents. Always saturated, always primary, never adjusted.

Hyperlinks:

- Blue underlined. Visited purple. Browser defaults preserved.

### Layout

Tables and float layouts. Intentional misalignment. Page widths set to `780px` because someone hand-coded an HTML page in 2001 and never updated it.

Layout logic:

- Use `<table>` for layout (yes, intentionally).
- Or use plain block elements with no grid, no flexbox.
- Page width: fixed `780px` to `980px` centered on the canvas. The empty whitespace on either side is the gesture.

Alignment:

- Left-aligned by default. Center-aligned occasionally for nostalgic effect.
- Misalignments are kept. A heading offset by `3px` because that's how the text node rendered.

Spacing:

- Random spacing increments. `7px`, `13px`, `21px`. The system rejects `4/8` rhythm.

Images:

- Inline images interrupt body text. No aspect ratio discipline. Sometimes pixelated, sometimes JPEG-degraded.

Section dividers:

- `<hr>` horizontal rules. The browser default. Or `*  *  *` typed as text.

### Motion

None. Or specifically, motion that contradicts modern best practice.

Appropriate motion:

- Nothing. The page is static.
- Optional: a `<marquee>` element (yes, the deprecated one) for a single rebellious moment.
- Optional: GIF animations embedded inline.

Inappropriate motion:

- Modern scroll-driven animations. The system rejects them.
- Spring physics. Rejected.
- Anything from the past decade of motion design.

### Components

Buttons:

- Default `<button>` styling. The native browser render — boxy, gray, beveled where the OS still bevels.
- No CSS reset. No customization.
- Hover state: the browser's default.

Links:

- Blue, underlined. Visited purple, underlined.

Forms:

- Default `<input>` and `<textarea>` styling. No CSS applied.
- Labels appear inline or above with no special treatment.
- Submit button is a default `<button>` with the word "Submit."

Tables:

- Used freely. Borders are `1px` default solid black. Data sits inside default cells.

Navigation:

- Plain text links separated by `|` characters. Like a personal homepage from the mid-90s.

Images:

- Inline, sized to their natural dimensions. Optionally surrounded by a `1px` solid border.

### Visual moves (signature elements)

- Default browser fonts as the brand voice.
- Default blue underlined hyperlinks.
- Fixed-width centered layouts at `780px`.
- `<table>` layouts where modern CSS would do the job.
- Random spacing increments.
- Inline GIFs.
- A single deprecated HTML element (a `<marquee>`, a `<blink>`) for rebellious effect.
- Misaligned elements left where they fell.
- Pure black substrate or institutional gray.
- Default button styling.
- "Last updated" timestamps in plain text at the bottom of the page.
- A guestbook (yes, an actual guestbook).
- An animated mailbox GIF as the email-contact affordance.

### Banned in this style

- Modern type systems. The defaults are the point.
- Custom CSS resets. Browser defaults must show through.
- Modern grid frameworks. Tables and floats only.
- Brand color systems. The system rejects taste.
- Sophisticated motion design.
- Glassmorphism, blur, gradient anything.
- Drop shadows beyond the browser's defaults.
- Rounded radii (browsers default to square corners — keep them).
- Modern icon systems. Use default emoji-like character glyphs, or no icons at all.

### Reference moods

- A personal homepage from a university CS department in the late 1990s.
- A zine's web archive maintained by someone who hand-codes every page.
- An artist's portfolio site that refuses to use a CMS.
- A conceptual project where the design is the protest.
- A counter-cultural music label's pre-2005 web page preserved without update.
- A personal blog from a writer who treats the web as a notebook.
- An indie developer's portfolio that signals "I make tools, not marketing pages."
- A statement piece by a designer making a point about the SaaS sameness.

---



For any brief, ask these three questions in order. Combine the answers to land on a style.

1. **What is the product type?**
   - Developer tool, infrastructure dashboard, observability product, data-heavy interface, anti-mainstream editorial → start considering brutalist or Swiss Grid.
   - Productivity tool, document workspace, fintech, B2B platform, knowledge base, long-form publishing → start considering minimalist, refined minimalism, or editorial magazine.
   - Creator tool, design platform, premium consumer brand, AI product with broad appeal, agency portfolio, marketing surface for an expensive product → start considering high-end, aurora glass, or bold maximalism.
   - Wellness, kids, indie creator product with personality → start considering organic hand-drawn or retro-futurist.
   - Gallery, atelier, museum, conceptual brand → start considering quiet emptiness.
   - Anti-corporate, art statement, intentional rebellion → start considering anti-design web.

2. **What is the brand tone?**
   - Raw, contrarian, technical, "we don't apologize" → brutalist or anti-design web.
   - Calm, considered, deliberate, "we don't waste your attention" → minimalist, refined minimalism, or quiet emptiness.
   - Luxe, cinematic, theatrical, "we've earned the right to be seen" → high-end or aurora glass.
   - Loud, expressive, "we want you to feel this" → bold maximalism or retro-futurist.
   - Trust, authority, "we are the system of record" → Swiss Grid or editorial magazine.
   - Warm, soft, friendly, "we are here to help" → organic hand-drawn.

3. **What does the audience expect?**
   - Audience that actively rejects consumer polish, reads it as "watered down" → brutalist or anti-design web.
   - Audience that has eye fatigue for over-designed SaaS and pays for restraint → minimalist, refined minimalism, or quiet emptiness.
   - Audience that judges the product partly on the surface and will reward visual ambition → high-end, aurora glass, or bold maximalism.
   - Audience that reads typography as the brand → Swiss Grid or editorial magazine.
   - Audience that wants to feel celebrated, warm, hand-held → organic hand-drawn or retro-futurist.

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
| Editorial publication / infosec / trust surface | Authoritative, system-of-record | Reads typography as brand | Swiss Grid |
| Government, civic, public-records platform | Neutral, durable, exact | Wants signal of permanence | Swiss Grid |
| Magazine, literary tool, design-forward bookstore | Editorial, narrative | Reads long-form happily | Editorial Magazine |
| Long-form essayist platform / serial publication | Literate, paced | Trusts a writer's voice | Editorial Magazine |
| Gallery, atelier, conceptual retailer, museum | Restraint as content | Reads empty space as intent | Quiet Emptiness |
| Premium designer marketing for the design-literate | Restraint pushed to severity | Recognizes the discipline | Quiet Emptiness |
| Creator-economy tool with personality | Loud, expressive, generous | Wants to be celebrated | Bold Maximalism |
| Indie game studio / music label / brand drop | Bold, kinetic, declarative | Pays for the show | Bold Maximalism |
| Premium fintech / design-tool marketing | Restrained but warm | Wants signal of considered choice | Refined Minimalism |
| Indie product aiming at "considered" | Calm, premium, deliberate | Pays for restraint with a signature | Refined Minimalism |
| AI product wanting "magic" feel | Luxe, generative, atmospheric | Reads gradients as differentiator | Aurora Glass |
| Creator tool / generative-art platform | Cinematic, atmospheric | Expects to feel transported | Aurora Glass |
| Indie game, music streaming for younger audience | Playful, retro, kinetic | Reads chrome as identity | Retro-Futurist |
| Fashion drop, capsule release, kit launch | Bold, ephemeral, fun | Buys the energy | Retro-Futurist |
| Consumer wellness / family / kids product | Warm, soft, friendly | Wants to be hand-held | Organic Hand-drawn |
| Indie creator newsletter / personal brand | Personable, illustrative | Reads "made by a person" as the differentiator | Organic Hand-drawn |
| Anti-corporate, conceptual art, intentional rebellion | Provocative, oppositional | Reads polish as deceit | Anti-Design Web |
| Designer statement / portfolio art piece | Raw, intentional, declarative | Recognizes the meta-move | Anti-Design Web |

### Tiebreakers

When two styles seem plausible, default to whichever one the audience would reward more for restraint. A brutalist developer tool that happens to have premium-product positioning should still lean brutalist — the audience reads polish as a tell.

When the brief says "modern, clean, premium" without further specifics, default to minimalist. It is the safest direction across audiences and the least likely to misfire.

When the brief says "wow, agency, design-led, ambitious" without further specifics, default to high-end. The brief is signaling that surface ambition is the explicit requirement.

When the brief is for a product whose audience overlaps two of these styles, pick one and commit. Blending will produce a generic SaaS look that none of the three styles intends.

When the brief mentions "AI" but the target audience is technical (researchers, engineers, infrastructure buyers), lean minimalist or brutalist. The technical AI cohort reads gradient maximalism as low-craft. Restraint signals competence.

When the brief mentions "AI" but the target audience is consumer or creator, lean high-end. The consumer AI cohort rewards visual ambition.

---

## Cross-style discipline

These rules apply regardless of the style chosen — Brutalist, Minimalist, High-End, Swiss Grid, Editorial Magazine, Quiet Emptiness, Bold Maximalism, Refined Minimalism, Aurora Glass, Retro-Futurist, Organic Hand-drawn, or Anti-Design Web. All twelve systems share the same floor on the items below. They are non-negotiable.

The cross-style floor exists because brand identity is a separate decision from professional baseline. Anti-slop discipline, SEO foundations, accessibility, intentional imagery, and the full set of interaction states must ship regardless of which aesthetic was chosen. The Bold Maximalist landing page that ships without alt text is still broken. The Anti-Design Web statement piece that animates `width` instead of `transform` is still broken. The Quiet Emptiness gallery site with placeholder names is still broken. Style is brand voice; cross-style discipline is craft baseline.

### Accessibility

- Body text contrast must meet WCAG AA at minimum: `4.5:1` against its background for normal text, `3:1` for large text. Verify in both light and dark variants if both exist.
- Focus states must be visible on every interactive element. Each style handles them differently — brutalist uses hard inversion, minimalist uses a 2px solid focus ring in the brand accent, high-end uses a soft outer glow combined with a ring, Swiss Grid uses a hairline outline, Editorial Magazine uses an underlined word, Quiet Emptiness uses a muted color shift, Bold Maximalism uses a saturated ring, Refined Minimalism uses an accent-color outline, Aurora Glass uses a tinted glow keyed to the vibe, Retro-Futurist uses a chrome highlight, Organic Hand-drawn uses a warm-tinted ring, Anti-Design Web uses the browser's default outline. Never rely on color alone in any style.
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

The twelve style systems exist not because there are only twelve ways to design — but because most successful premium products converge on one of them. Each system has a discipline: what to include, what to exclude, what to commit to. The discipline is what produces coherence.

Output that reads as "premium" is rarely doing something unusual. It is committing fully to one of these systems and refusing the templated defaults that would dilute it. The brutalist developer tool that ships in a templated SaaS aesthetic loses its audience. The minimalist fintech that ships with mesh gradients loses its audience. The high-end creator tool that ships with hairline borders loses its audience. The Swiss Grid editorial site that adds spring physics loses its authority. The Aurora Glass AI product that adds chrome retro accents loses its leap. The Organic Hand-drawn wellness brand that ships with Lucide icons loses its warmth. The Anti-Design Web statement piece that adds a design system loses its joke.

Pick the style. Commit to the style. Ship the style. The rest is execution.
