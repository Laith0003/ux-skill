# Anti-slop — the forbidden patterns

Default model output has measurable, predictable failure modes. This file catalogues them. Every entry here exists because the unconstrained generator reaches for it reflexively, and the result reads as machine-made.

Treat each ban as a hard rule unless a brief explicitly overrides it, or the client's own system or identity does otherwise (principles 9 to 11). The goal is not stylistic preference: it is the elimination of fingerprints that mark output as generated.

---

## Principles

1. **Specificity beats genericity.** A generic three-card row is the strongest AI tell. Asymmetry, names that fit the product's market, and the client's own figures with what they count: these signal a human (or a careful machine). The fastest way to ship slop is to use the safest defaults the model offers.

2. **Restraint beats decoration.** Single accent color, neutral base, intentional whitespace. Don't add a gradient because the model defaults to one. Don't add a glow because the surface needs "polish." A surface needs a job, not ornament.

3. **Type size follows the brand.** Hierarchy comes from size, weight and color together, and the headline's size is the system's display role: 60 to 240px at 1440 by the brand's expressiveness (character.landing_display_px), near 60 to 90px for a calm brand and 180 to 240px for a loud one. A size of your own, larger or smaller, is the tell.

4. **Motion has meaning or it doesn't ship.** Decorative animation is slop. Every motion expresses cause and effect, confirms a state change, or invites engagement. Bouncing for the sake of bouncing dates the work in six months.

5. **Content is a design surface.** "John Doe" + "Acme Corp" + `99.99%` is content slop and ruins the design regardless of layout quality. Treat placeholder content with the same care as the layout that holds it.

6. **Imagery is mandatory and real.** A text-only wall reads as a memo, not a product. Every layout accommodates imagery and never avoids it. Use the client's own assets first; fill the gaps with curated Unsplash/Pexels chosen to match the brand and the 7-axis temperature, then treat them so they read as deliberate. An abstract SVG is NOT a substitute for a real product or site image, and neither is the logo. Only *random/generic* stock (and the auto-rotating placeholder services) is banned: real photography, chosen on purpose, is the goal. A page always carries photographs: with none from the client, sourced ones (stock included) fill the gap. A brand book's ban on a kind of photo (staged lifestyle stock, airbrushed people) narrows which photos qualify and never removes photography; only a client system that forbids photography outright ships without it, and says so.

7. **Convention over cleverness on navigation.** Logo top-left. Nav top or left. Search is a magnifying glass. Innovate when you know you have a better idea; otherwise honor convention so the user can scan.

8. **Clarity over consistency.** When making something significantly clearer requires slight inconsistency, choose clarity every time.

9. **A client's existing design system wins.** When the project already has its own system (tokens, foundation CSS, a hand-written MASTER.md or DESIGN.md), every generic rule in this file yields to it: its colors, saturation, gradients, type, label tracking and case stand as they are. These bans guard against model defaults, never against a client's deliberate identity; a mark beside a label still needs the recorded waiver (decisions/eyebrow-is-text.md). Find it with `ux system detect` before applying any rule below.

10. **A client's own identity wins, even with no full system.** When there are no token files but the client has a logo, a site, an app or a brand book, the same holds for what that material shows: its saturated brand, its brand gradient, its pure white or pure black canvas, its blue or violet hue stay as the client uses them (decisions/client-identity-wins.md, which extends decisions/existing-system-wins.md to identities with no full system). The evidence is client material that predates the build, named with its exact value (the hex, the gradient stops), and the page uses that exact value; the engine's generated art, anything made in this session and a word in the brief are not evidence. The contrast gate still holds: keep the color and solve the text on it.

11. **The system font stack and pure white bans apply to generated systems only.** They stop a generator from shipping its defaults. A client's own system that sets a system font stack (`-apple-system`, `system-ui`, `Segoe UI`) or a pure white canvas keeps it exactly, like every other value it owns.

---

## Responsive / mobile-first (non-negotiable)

Mobile is not the small version of the desktop — it is where most of the traffic lives and where the defects ship. The failures below recur on every unconstrained build because the generator designs at desktop width and never re-checks the phone. They are not taste calls; they are correctness.

1. **Mobile-first, and verify it.** Every layout MUST work at 360–390px with ZERO horizontal scroll. Horizontal scroll on mobile is a CRITICAL fail — the single most common shipped defect. ALWAYS verify it before declaring done: render the output at 390px and assert `document.documentElement.scrollWidth <= window.innerWidth`. If it overflows, it is not finished, no matter how good the desktop view looks.

2. **Every multi-column block collapses to one column at ≤640px.** Hero text + form, image + text, card rows, stat bars — all of them. A fixed multi-column grid that overflows on a phone is never acceptable. Set the single-column breakpoint explicitly; never let a `1.05fr 0.95fr` (or any `Nfr Mfr`) survive to mobile, and never define the columns in an inline `style` you cannot media-query.

3. **Nothing escapes its container.** No absolutely-positioned element may bleed outside its parent or "pop out" on small screens. Decorative glows, off-canvas art, and oversized media are all clipped or contained — a `width: 100vw` block overflows by the scrollbar width and is banned; size to `100%`/the container, not the viewport.

4. **Never ship a literal placeholder token.** `{TODO_FILL...}`, `{{ var }}` mustache left in markup, "lorem ipsum" — none of these reach the rendered UI. If a value is genuinely absent (no phone number, no OG image), OMIT that element gracefully — drop the affordance, don't print the token. A visible `{TODO_FILL: phone}` in a sticky header is the rawest draft-state leak there is.

5. **Imagery as backdrop, not just an icon.** Where it adds depth (hero, location or coverage cards, feature tiles), use a REAL image as the section or card background with text overlaid and a readable scrim, not a flat card with one lone icon. A single centered icon on a bare card is a slop tell precisely where a backdrop image would have carried the surface. (Icons on list items follow the one icon rule in `commands/ux-design.md`; this is about sections and feature/coverage cards that read as empty without imagery.)

6. **Never repeat one icon across differentiated items.** Every skip size, every plan, every sector rendered with the same box/grid/check icon reads as the generator giving up. If you cannot source a DISTINCT, meaningful icon per item, drop the icons there entirely and differentiate with TYPOGRAPHY (scale, weight, the number itself), color, or layout. A repeated icon is worse than no icon — it actively says "these are the same" about things you are claiming are different.

7. **Short labels never wrap to a second line.** The brand wordmark, every button/CTA label, and nav links are short, fixed phrases — they must stay on ONE line at 360px. Wrapping a 2-3 word label ("Instant Skip / Hire", "Get a / quote") is the textbook *break-by-accident*: the box got too narrow and the browser improvised, and it reads as broken. `white-space: nowrap` them and size them to fit (shrink the wordmark font on mobile, tighten gaps); if the full wordmark still cannot fit beside the logo + the primary CTA, drop to the **logomark alone** (hide the words, keep the icon) — never two lines. This is invisible to a horizontal-scroll check: a nav that wraps to two rows still reports `scrollWidth == innerWidth`, so it must be verified directly (the wordmark's and each label's rendered height stays at one line: `scrollHeight <= 1.4 * lineHeight`). Note `nowrap` alone can trade the wrap for horizontal scroll — pair it with a size-to-fit and confirm both.

---

## Forbidden — visual & CSS

| Don't | Do instead |
|---|---|
| Default `box-shadow` glows, neon outer glows | Inner border (`border-white/10`) + tinted inner shadow (`box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.08)`) |
| Pure black (`#000000`) | Zinc-950, charcoal, off-black: `#0a0a0a`, `#111111` are correct. A client whose identity is set in pure black keeps it (decisions/client-identity-wins.md) |
| Pure white (`#FFFFFF`) on premium marketing, in a generated system | Warm off-white in the `#FAFAF8` to `#F7F6F3` range; pure white reads as default. A client whose identity is set on pure white keeps it (decisions/client-identity-wins.md, principle 11) |
| Oversaturated accents (>80% saturation) | Desaturate. High contrast comes from value, not saturation. A client's own saturated brand stays exact (decisions/client-identity-wins.md) |
| Text-fill gradients on large headers | Solid color + weight hierarchy. One word in gradient per page is the absolute maximum |
| The "AI" purple-to-blue gradient on white | A single restrained accent (Emerald, Electric Blue, Deep Rose, Amber) against neutrals. A gradient from the client's own identity is not this default and stays (decisions/client-identity-wins.md) |
| Full-bleed gradient hero backgrounds covering large surfaces | Gradients sit inside narrow 30 to 60 degree hue windows at low saturation, used as accents not as canvas. The client's own gradient band may run full-bleed, as their material shows it (decisions/client-identity-wins.md) |
| Multi-stop rainbow gradients | 2-3 stops, axis-aligned, narrow hue spread |
| More than one gradient section per page | One gradient feature, max |
| Custom mouse cursors | Native cursors only — performance + a11y + outdated. Exception: a custom cursor inside an interactive product demo surface |
| Mixing warm gray + cool gray in same project | Pick one (Zinc OR Slate) and commit across the whole surface |
| Default shadcn/ui look | Customize radii, colors, shadows — the default look is a known fingerprint |
| Skeuomorphic shadows, 1990s bevels | Tinted ambient shadows or hairline borders |
| Heavy drop shadows at >24px blur with >15% alpha | Hairline 1px borders, or near-invisible shadows (4-8% alpha, long blur) |
| Heavy drop shadows on dark surfaces | Elevation via lightness ladder, not shadows — dark mode shadows smudge or vanish |
| Hard, dark, gray drop shadows | Tinted shadows keyed to the surface or brand: a teal section gets teal-mist shadows |
| Glassmorphism applied to scrolling content | Reserve `backdrop-blur` for fixed or sticky surfaces only (nav, modal, overlay) |
| Excessive z-index spam (arbitrary `z-50`, `z-[9999]`) | Z-index reserved for systemic layers: sticky nav, modal, overlay, tooltip. Document them so they don't sprawl |
| Grain or noise on scrolling containers | Grain attaches exclusively to fixed `pointer-events-none` pseudo-elements |
| Decorative blobs, waves, geometric patterns not in the spec | If decoration doesn't carry a job, delete it |
| 3D chrome, ray-traced spheres, metaverse-cluster renders | Restrained matte 3D when needed; or skip entirely |
| Iridescent rainbow overlays as primary visual | Used surgically on a single foil card or premium accent — not as a section theme |
| Flex math like `flex-basis: calc(33.3% - 24px)` | CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) |
| `border-radius: 9999px` on non-tag elements (pill cards, pill primary buttons) | Pill shape is reserved for tags, status badges, sometimes primary CTAs in maximalist styles |
| Inconsistent corner radii across components | Pick 2-3 radii and commit. Mixing 4, 8, 12, 16, 24px across a single page reads as undisciplined |
| Color bands switched on and off down the page with no content reason (the same idea on alternating slabs) | Bands carry the section rhythm by the brand's energy: `color.budget.bands` of the sections sit on a band, none on a calm page and up to half on a loud one. Otherwise space and a change of ground separate sections; an eyebrow never separates sections |

Hero rules, including the hero height, live in `references/surfaces/landing.md`.

---

## Forbidden — typography

| Don't | Do instead |
|---|---|
| Serif faces on dashboards, admin, data UIs, software UIs | Sans only. Geist + Geist Mono, Satoshi + JetBrains Mono, IBM Plex Sans + IBM Plex Mono, or similar disciplined pairings |
| A headline size of your own (`text-9xl`, `text-[112px]`), larger or smaller than the system's | The display role: `type.text.display`, a fluid clamp from character.landing_display_px, 60 to 240px at 1440 and 36 to 90px on a phone. Widen the container before the size shrinks |
| H1 wrapping past the line limit in `references/surfaces/landing.md` (Hero composition) | Widen the container (`max-w-5xl`, `max-w-6xl`, `w-full`) and use `clamp()` to scale the font down |
| Mismatched font families per section | One display + one body across the entire project. If a serif appears, it appears surgically — once or twice per page maximum |
| Paragraphs wider than the system's measure | `layout.measure.landing`, 42 to 56 characters of the text face on a landing page, and `layout.measure.text`, 60 to 70 for reading |
| Body type below 16px on marketing surfaces | 16-18px minimum. Compressed body type reads as a startup template |
| Arial, Roboto, generic system stacks as primary display, in a generated system | Distinctive display face (Geist, Satoshi, Cabinet Grotesk, Outfit), or a deliberately chosen variable sans. Note: Inter is a legitimate, modern choice; pair it carefully and don't reach for it reflexively as the only option |
| Default font-fallback chains (the standard humanist sans most platforms ship), in a generated system | Choose the type intentionally even when the brief doesn't specify. A client's own system stack stays (principle 11) |
| Same display family across every output | Vary across generations. Never converge on one stack repeatedly |
| Title Case Across Every Word In Headlines | Sentence case. Title case reads as advertising copy from a previous decade |
| A headline in capitals when the system does not lean to capitals | Sentence case. A loud brand's system leans to capitals (character.capitals at 0.5 and up) and sets them on `type.text.display-caps`, tracked at 0 or open; a calm brand keeps its headlines in sentence case |
| Capitals on body copy, subheads, or anything read at length | Breaks legibility. Capitals belong to short labels and to a loud brand's display |
| Italic used as decoration | Italic means "this is a title" or "I am emphasizing this word" — not "this is a fancy moment" |
| Display tracking of your own | The system's tracking per step, tighter as contrast rises; capitals track at 0 or open (`type.tracking.caps`) |
| Tabular figures mixed with proportional figures on the same page | Pick one. Stat blocks, prices, version strings get tabular; prose gets proportional |
| Straight quotes (' ") in copy, and a double hyphen or a long dash as punctuation | Curly quotes and apostrophes in copy. No em dashes and no double hyphen: a period, a comma or a colon does the job |
| A display face picked for novelty with nothing in the brand behind it | The display face is the system's (fonts.distance over the axes). A loud, informal brand can carry a display face; a calm one keeps to its text family |
| 5+ weights from the same family | Three-weight system at most: bold/semibold for display, regular for body, lighter for support |
| Variable font weight animated for decoration only | When variable axes animate, the motion expresses state change — not "look at this font" |
| Eyebrows that aren't tracked (`+0.05em` to `+0.10em`) | All eyebrows are tracked. The wide tracking is the whole point. An existing design system wins: when the client's system sets label letter-spacing to 0 or sentence case, keep it (decisions/existing-system-wins.md) |
| A short line, dash or dot before or after an eyebrow (a `::before` bar, an empty span, a left border, an SVG line, a typed dash) | The eyebrow is text only. Its size, weight, tracking and color carry it; lint flags every build as `decorative-accent-ruler` |

---

## Forbidden — layout & spacing

| Don't | Do instead |
|---|---|
| 3-equal-cards horizontal feature row | 2-column zig-zag, asymmetric grid, horizontal scroll, or bento. The 3-equal pattern is the strongest AI tell |
| Center alignment as a fallback when no layout decision is made | Center alignment is a deliberate choice for hero callouts, isolated lockups, or final CTAs — not a default |
| Centring a page to make it calm | Centring is a composition, not the calm option: measured award pages centre more when the brand is loud and poster-like. A centred hero fits a capitals display or the Thesis statement and Cinematic brand archetypes; a calm brief with a centred hero over three equal cards reads as generated |
| Horizontal scroll on mobile from off-screen animations | Wrap the page in `overflow-x-hidden w-full max-w-full` |
| Symmetric three-column grids without massive whitespace gaps | Asymmetric bento, or split with one column dominant |
| Random spacing increments (5px, 11px, 23px) | 4/8 rhythm — every gap, padding, margin in multiples of 4 |
| A reading column wider than the measure | Text keeps `layout.measure.*`. The frame follows the brand: an expressive brand page runs a full-width grid (`layout.landing.full`, a 1920px container with a 24 to 48px margin) and a calm one keeps `layout.container.max` |
| Bootstrap-style symmetric grids with 24px gutters | The grid exists to allow alignment, not to enforce density. Most marketing sections only need 1, 2, or 8 columns |
| Meta-labels like "SECTION 01", "CHAPTER 03", "OUR PROCESS 02", "ABOUT US" as decoration | Strip them entirely. If the section needs a label, use a small eyebrow naming the category: not numbered chapter signposting |
| "Section X of Y" indicators | Space and a change of ground separate sections; an eyebrow never separates sections. Numbered chapter framing only when the product genuinely is a journey |
| Floating elements with awkward gaps | Padding and margins are mathematically intentional |
| Cards bare on background without any structure | Bordered (1px hairline), bezel-wrapped (in maximalist styles), or grouped by spacing — but never floating without context |
| Cards mixing structure within the same row | Inside a row, all cards share one anatomy — same icon position, same heading scale, same internal padding |
| Card paddings mixed across the page (16px here, 32px there) | Choose 24-32px or 32-40px and commit. Mixed-padding cards on the same page break rhythm |

Landing-page layout rules (hero, section rhythm, feature sections, pricing, navigation, footer) live in `references/surfaces/landing.md`.

---

## Forbidden: content and data (the placeholder-name effect)

The single fastest way to mark output as AI-generated. The design can be perfect; if the placeholder content is generic, the whole surface reads as slop.

| Don't | Do instead |
|---|---|
| "John Doe", "Jane Smith", "Sarah Chan", "Jack Su", "Test User" | Creative and plausible names that fit the product's market |
| "example@example.com", "user@email.com" | Realistic, contextual emails |
| "Acme", "Nexus", "SmartFlow", "Zenith", "Stellar", "Vertex", "Apex" | Contextual brand names. A fintech is "Ledgerine" or "Tash"; a CRM is "Patio" or "Greta" |
| Round numbers inside a product mock (a dashboard, a table, a chart): "99.99%", "50%", "1234567", "$10,000" | Plausible, irregular stand-in data that fits the screen: "47.2%", "63%", "$8,247.30". This is for data inside a UI mock only |
| A figure the page claims, reshaped to look precise or given with nothing about what it counts | The client's own figure, as the client states it, with what it counts and as of when. With no source, the slot holds a labeled draft placeholder for the client, not a made-up figure. A round real figure stays round; one the client cannot define or date follows the Proof bans in `references/surfaces/landing.md` |
| Default Lucide / Heroicons egg avatars | Real/licensed photos, or distinct SVG initials with intentional styling. When you need a stand-in face, source a curated, on-brand portrait (Unsplash/Pexels) rather than an auto-rotating placeholder; the linter flags *random/unseeded* services HIGH. |
| Lorem ipsum, "Your text here", "Placeholder content" | Generate realistic content based on the brief. If a mockup exists, extract text from it |
| Filler verbs: "Elevate", "Seamless", "Unleash", "Next-Gen", "Empower", "Revolutionize", "Transform", "Leverage", "Robust" | Concrete verbs naming what the product actually does: "Send", "Settle", "Track", "Decide", "Ship", "Deploy", "Query" |
| AI copywriting clichés: "delve", "blazingly fast", "game-changer", "world-class", "industry-leading", "innovative" | Specific numbers and named outcomes. "75ms latency" beats "blazing fast"; a named customer with the result they measured beats "trusted by leaders" |
| Random/generic stock (teams laughing at laptops, the first Unsplash hit) | Client assets first, then curated Unsplash/Pexels chosen to match the brand + 7-axis temperature — pick the best per slot, don't paste the first credible photo. Treat them (grayscale, mix-blend-luminosity, opacity-90, contrast-125) so they read as deliberate. A real, chosen photo beats an abstract SVG, which is not a substitute for a product/site image. |
| Generic/clichéd stock (teams laughing at laptops, businessmen pointing at charts, isometric workers) | Custom imagery, real product UI, or real editorial photography curated to the brand. The cliché is the ban — not photography itself; every surface still carries real imagery |
| Fabricated / hand-drawn / abstract brand logos (an invented glyph standing in for Cursor, Stripe, Claude, etc.) | The REAL single-path SVG from `references/logos/` (or fetched from `cdn.simpleicons.org/<slug>` / the brand's own kit), `fill="currentColor"`. An approximated brand mark is an instant credibility leak |
| Hyperbolic adjective stacks ("powerful, intelligent, transformative, seamless") | Signal of weakness in the underlying claim. Replace adjectives with specifics |
| Vague benefit copy ("faster", "easier", "smarter") | Specific numbers and named outcomes |
| Mentioning the product's own name in every sentence | "The platform", "your team", "the workflow" — constant self-naming reads insecure |
| First-person plural in headlines ("We help you...", "We believe...", "Our mission") | Address the reader directly or describe the outcome. "We" comes later, in trust copy and about pages |
| Exclamation marks in marketing copy | Confidence is performed by restraint. Reserved for in-product micro-celebrations and even then sparingly |
| Question-form headlines as faux-rhetorical setup ("Tired of slow workflows?") | Declarative statements. Question headlines are reserved for genuine questions |
| Brain icons, sparkle icons, neural-network nodes, glowing dots as "AI" iconography | Restrained generic icons — a small star, a triangle, an arrow. No "AI" visual vocabulary |
| Confetti, sparkle emojis, or celebration explosion on success states | Calm success: "50 points added", "Account ready", "Invite sent" |
| Numbered version badges in marketing headlines ("Now with v3.7!") | Say "new" or "now", or name the new feature directly |
| Pop-culture references and casual handwritten fonts on primary surfaces | Wit lives in copy cadence, not in typeface choice |
| Industry-vertical names where they don't apply ("Built for fintech, healthcare, retail") | Horizontal positioning by role ("For designers", "For builders", "For teams") |
| Buzzword stacking ("AI-powered next-gen platform") | Plain verb-noun honesty: "Build sites", "Take notes", "Run queries" |

Landing-page proof and CTA rules (testimonials, logo walls, press logos, stat callouts, CTA wording, lead forms) live in `references/surfaces/landing.md`.

---

## Forbidden — interaction & motion

| Don't | Do instead |
|---|---|
| Static "success" state with no loading / empty / error variants | Always ship all four states. Missing states are a quality failure |
| Generic circular spinners | Skeletal loaders matching the eventual layout shape |
| Vague empty states ("No items yet", "No data") | Empty states explain what should be there and how to make it appear: "Connect your first source to start" |
| Vague errors ("Form contains errors", "Something went wrong") | Name the field and the action. "Phone number missing — add a number to continue" |
| Linear easing on UI motion | `ease-out` on enter, `ease-in` on exit, custom cubic-bezier, or spring physics. `linear` and `ease-in-out` read as unconsidered |
| Instant state changes (0ms) | The system's `motion.state` role, 150 to 240ms by the brand's motion; under reduced motion it stays at 100ms or less |
| Motion that answers late: a hover or press not half done by 70ms, an entrance not half done by 140ms | The system's roles (`motion.state`, `motion.press`, `motion.reveal`, `motion.arrive`), whose curves answer in time at any length (motion.settle_ms). A long move on a strong out curve is fine; a short one on ease-in-out is not |
| Continuous animations driven by `useState` | `useMotionValue` + `useTransform` only. `useState` causes re-render storms |
| Perpetual motion components that re-render the parent | Wrap perpetual loops in `React.memo` and isolate to leaf Client Components |
| Hover-only critical interactions | Tap/click for primary; hover is enhancement only. Mobile has no hover |
| Animating `width`, `height`, `top`, `left` | `transform` + `opacity` only — hardware acceleration |
| Ignoring `prefers-reduced-motion` | Wrap motion in a reduced-motion check. Replace transforms with simple opacity fades, shorten durations, drop blur components |
| Scroll-jacking, scroll-snap that forces a sequence | The page scrolls in the reader's direction. Inertial scroll is an opt-in treatment on `motion.scroll` (0 below a motion of 0.6, 0 under reduced motion), never a hijack |
| Horizontal scroll hijack as a default | Reserved for galleries or storytelling sequences with a real reason; never the default flow |
| Pinned-3d-element scroll-controlled video scrubbing as decoration | When scrub motion appears, it carries a real demo or sequence |
| Auto-playing background video with sound | Muted, looped, with a pause control. Sound is opt-in |
| Auto-rotating carousels under 4 seconds per slide | Either one continuous marquee (no pagination dots, a slow loop, a pause control, stopped under reduced motion) or scroll-snap horizontal lists with visible affordance |
| Number counters that animate on every scroll past | Once per page entry. Settling jitter on the final number is a tell |
| Bouncy spring animations on type | Spring physics on draggable UI elements (toggles, modals, drag handles), not on headline reveals |
| Page-load animations that loop endlessly on the wordmark | Once-on-load is the rule. Looping brand-mark animation in nav reads as distracting |
| Device orientation / motion permission prompts for parallax | Pointer events only. Phone-tilt parallax requires sensor permissions that erode trust |
| Cursor-following effects on every clickable element across the page | Cursor effects are scoped — to a hero canvas, to one demo surface. Global cursor effects are noise |
| Big animated number sequences as decoration | Counters anchored to a real metric. Decorative counters feel like a gimmick |

Landing-page interaction rules (hero carousels, headline typewriters, testimonial video, newsletter modals, cookie banners, chat widgets) live in `references/surfaces/landing.md`.

---

## Forbidden — components

| Don't | Do instead |
|---|---|
| Generic card containers everywhere | Cards only when elevation communicates hierarchy. Otherwise use `border-t`, `divide-y`, or pure negative space |
| Generic 3-column feature grids | See layout bans. Bento, masonry, asymmetric, zig-zag |
| Cards with default rounded corners and drop shadows as the page baseline | Cards earn their elevation. Most surfaces don't need card chrome |
| Emoji as visual elements anywhere | Anywhere. Code, comments, markup, alt text, UI strings, microcopy. Use SVG icons or text |
| Mixed icon styles (filled + outline at the same hierarchy level) | One icon family, one stroke weight, one fill state at any given level |
| Mixing icon families (Lucide + Heroicons + Phosphor in the same project) | One family, committed |
| Stroke-width inconsistency (mixing 1.5 + 2.0 in the same surface) | Pick one stroke and stick with it |
| No imagery anywhere (text walls of cards) | Photographs are required: the client's own first, else sourced ones (stock included) that follow the system's photo direction (the `imagery.photo.*` grade, the report's subject and kinds). A brand's ban on a kind of photo narrows the kinds; only a brand that forbids photography outright ships without one. Drawn art and product fragments add to photographs, never replace them. Random placeholder services never ship |
| Stock-photo placeholder divs as "image here" markers | Real imagery or hand-styled SVG/CSS placeholders. Stock-placeholder divs ship as the final shippable mistake |
| Random radius values across components (4, 8, 12, 16, 24px on the same page) | Token: `rounded-sm` / `md` / `lg` / `2xl` / `[2.5rem]` — pick a scale, commit |
| Toasts that steal focus | `aria-live="polite"` toasts. Never grab focus |
| Placeholder-only form labels | Visible label above input, helper below input, error below input |
| Form fields with no helper text markup at all | Helper text slot exists in the markup even when empty, so error states don't cause layout shift |
| Default `shadcn/ui` styling | Customize radii, colors, shadows to match the project aesthetic. Default `shadcn` is a recognized AI tell |
| Naked trailing arrows on CTA text | In high-end styles, wrap the arrow in its own circular bezel inside the button (a nested icon chip). In minimalist styles, the arrow sits naked inline: but tracked properly |
| Default heavy drop shadows on cards | Hairline 1px borders, near-invisible shadows (4-8% alpha), or rely on background contrast |
| Generic line-icon clichés (lightbulb, rocket, lock) | Purposeful, often custom icons. The lightbulb cliché is absent from every premium cohort |
| OS chrome stripped from product screenshots | Real OS chrome (traffic lights, menubar, status bar) grounds the screenshot as real software. Stripping it makes it read as prototype |
| Generic font-fallback chains (the standard humanist sans most platforms ship) | Choose intentionally even when the brief is silent |

Hero component rules live in `references/surfaces/landing.md`. Dashboard card-density rules live in `references/surfaces/dashboard.md`.

---

## Tokens / numeric guardrails

- **Color**: within the system's budget, `color.budget.chromatic` (2 to 20 percent of the interface by energy) plus `color.budget.bands` for bands; lint --render measures it. A client's own brand keeps its saturation (decisions/client-identity-wins.md)
- **Contrast**: 4.5:1 for text and 3:1 for large text (1.4.3); the system holds every text role to 4.5:1 at any size, as its own floor. 3:1 for UI components and graphics (1.4.11)
- **Spacing**: multiples of 4 (4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160)
- **Touch targets**: ≥ 44×44 pt (iOS), ≥ 48×48 dp (Android) regardless of visual render
- **Motion**: the system's roles. A direct response is half done within 70ms and nine tenths within 220ms, an entrance half within 140ms (motion.settle_ms); reduced motion keeps 100ms or less
- **Measure**: 42 to 56 characters on a landing page (`layout.measure.landing`), 60 to 70 for reading (`layout.measure.text`)
- **Max H1 lines**: the limit in `references/surfaces/landing.md` (Hero composition)
- **Frame**: `layout.container.max`, or a full-width grid for an expressive brand page (`layout.landing.full`)
- **Card internal padding**: 24-40px
- **Font scale**: 6 to 10 sizes from the system's ladder, with one detached display
- **Body font size minimum**: 16px on marketing, 15-16px on dashboards
- **Display line height**: the system's `type.leading` steps, 1.12 at 40px down to 1.0 (muted) or 0.92 (bold) at 160px and up; Arabic at least 0.15 above
- **Body line-height**: 1.5-1.7
- **Display tracking**: the system's step tracking, tighter as contrast rises; capitals at 0 or open
- **Eyebrow tracking**: +0.05em to +0.10em uppercase, unless an existing design system sets its own
- **Image aspect ratios**: 16:9, 4:3, 1:1, 4:5 — vary intentionally, never random

Marketing section padding lives in `references/surfaces/landing.md`.

---

## Severity-tagged checklist

Run before shipping any UI output. Severity tags indicate the failure mode if violated.

### Critical (blocker — ship is not possible)
- [ ] No purple-to-blue "AI" gradient on white, unless it is the client's own identity
- [ ] No generic names ("John Doe", "Jane Smith")
- [ ] No "Acme / Nexus / SmartFlow" filler brand placeholders
- [ ] No Lorem ipsum, no "Your text here" placeholder content
- [ ] No emojis anywhere (code, markup, UI, alt text, microcopy)
- [ ] All four interaction states present (loading, empty, error, success/default)
- [ ] No horizontal scroll at 360–390px (`scrollWidth <= innerWidth`) — verified, not assumed
- [ ] Nav stays ONE row at 360px and NO short label wraps — brand wordmark, button/CTA labels, nav links each on one line (`scrollHeight <= 1.4 * lineHeight`); verified directly, since `scrollWidth` alone misses a wrapped nav
- [ ] No literal placeholder token shipped (`{TODO_FILL...}`, `{{ var }}`, "lorem ipsum")
- [ ] No pure `#000` text or background
- [ ] No row of three equal cards that each hold just an icon, a title and a line
- [ ] No "SECTION 01" / "CHAPTER 03" / decorative meta-labels
- [ ] No exclamation marks in marketing copy
- Landing-page critical checks live in the checklist of `references/surfaces/landing.md`.

### High (must fix before review)
- [ ] H1 within the line limit in `references/surfaces/landing.md` (Hero composition)
- [ ] Every multi-column block (hero, image+text, card rows, stat bars) collapses to one column at ≤640px
- [ ] Sections/feature/coverage cards use a real backdrop image where depth is needed, not a lone icon on a bare card
- [ ] No single icon repeated across differentiated items (distinct icon per item, or none + typographic differentiation)
- [ ] No serif on dashboards or software UIs
- [ ] All animations on `transform` + `opacity` only
- [ ] `prefers-reduced-motion` respected
- [ ] No GSAP + motion library in the same component tree
- [ ] No scroll-jacking; inertial scroll only on `motion.scroll`, off under reduced motion
- [ ] Photographs are present and follow the photo direction (no text-only walls; no illustration standing in for a photograph)
- [ ] Icons are one consistent family at consistent stroke width
- [ ] No hover-only critical interactions
- [ ] Chromatic color within the system's budget (lint --render `color-over-budget`), except the client's own brand
- [ ] No multiple gradient sections
- [ ] No filler verbs ("Elevate", "Unleash", "Next-Gen")
- Landing-page high checks (centered hero, logo color, CTA wording, footer) live in the checklist of `references/surfaces/landing.md`.

### Medium (polish — fix before final)
- [ ] H1 in sentence case (not Title Case)
- [ ] Display tracking from the system (tight for a bold display, 0 or open for capitals)
- [ ] Paragraphs within the system's measure (42 to 56 characters on a landing page)
- [ ] Body type at 16-18px minimum on marketing
- [ ] One accent, within the system's color budget
- [ ] Spacing on 4/8 rhythm
- [ ] Photographs are real and chosen: client assets first, then sourced ones by the photo direction, all within one grade (lint --render `photo-grade-off`)
- [ ] One icon family at consistent stroke width
- [ ] Eyebrow labels tracked (+0.05em to +0.10em), or as the existing design system sets them
- [ ] Corner radii consistent (2-3 values max across the page)
- [ ] Mock data inside a product UI is irregular; every figure the page claims is the client's own, with what it counts and as of when, or a labeled draft placeholder; never an invented number
- [ ] Color saturation tuned separately for light and dark modes
- [ ] No naked trailing arrows on CTAs in high-end styles (a nested icon chip instead)
- Landing-page medium checks (press logos, unsupported trust claims) live in the checklist of `references/surfaces/landing.md`.

### Low (taste calls — flag but don't block)
- [ ] No mention of the product's own name in every sentence
- [ ] No first-person plural in headlines ("We help you...")
- [ ] Number formatting honest (no false precision)
- Landing-page low checks (testimonial attribution, press logo weight) live in the checklist of `references/surfaces/landing.md`.

---

## AI Tells by category — the meta-fingerprints

These are the combinations that, when they co-occur, mark the output as machine-made within seconds of viewing. Each one alone is a signal; together they are a confession.

### The composition fingerprint
- A centred hero chosen to look calm + left-text-right-image as default reach + 3-equal cards below + decorative meta-label numbering = generated.
- The page tells you nothing about the product because it could be any product. Every section is a slot the model filled with the safest possible option.
- Fix: pick one organizing principle (editorial column rhythm, bento, asymmetric split) and commit. Vary section orientation. Earn each layout decision.

### The typography fingerprint
- Default font fallback + Title Case headlines + 6-line wrapping H1 + body type at 14px + serif on a dashboard = generated.
- The face wasn't chosen; it landed. The scale wasn't designed; it defaulted. The hierarchy wasn't built; it scaled monotonically.
- Fix: pick one distinctive face. Set sentence case. Widen the H1 container. Raise body to 16-18px. Drop serifs from software contexts.

### The color fingerprint
- Purple-to-blue gradient + pure `#000` text + pure `#FFF` background + saturated accents on every surface + customer logos in original colors = generated.
- Every color decision was the most obvious one. There is no palette discipline because there was no palette intent.
- Fix: warm off-white canvas, charcoal text, one restrained accent. Logos go monochrome. Accents are scarce.

### The content fingerprint
- "John Doe" + "Acme Corp" + "99.99% uptime" + "Elevate your workflow" + "Get Started" CTA = generated.
- Every placeholder was filled with the model's most-frequent neighbor for that slot. The result reads as no product because it reads as every product.
- Fix: names that fit the market, brands that fit the category, figures the client can define and date, verbs that name what the product does.
- The swap test for vague benefit copy: put a competitor's name in the headline. If the line still holds, it says nothing about this product; rewrite it until it would be false for the competitor.

### The motion fingerprint
- Linear easing + 0ms instant state changes + `useState`-driven perpetual hover + autoplay video with sound + scroll-jacking on a marketing landing = generated.
- The motion was added because motion is expected, not because it serves the surface.
- Fix: spring physics on gestures, cubic-bezier on transitions, motion only where it earns its place. Drop scroll-jacking. Mute autoplay.

### The component fingerprint
- Default `shadcn/ui` chrome + emoji icons + Lucide user-egg avatars + naked trailing arrows on every CTA + 24px-blur drop shadows on every card = generated.
- The component library wasn't customized. Every default the framework offered shipped to production.
- Fix: customize radii, shadows, colors. Pick one icon system. Style avatars deliberately. Wrap trailing arrows in bezels (high-end) or drop them entirely (minimalist).

### The voice fingerprint
- Exclamation marks in headlines + "Elevate" / "Seamless" / "Unleash" + question-form rhetorical headlines + 15 unattributed testimonials + multiple primary CTAs above the fold = generated.
- The voice was performed, not earned. Every hedge was filled with hype.
- Fix: declarative statements, specific numbers, named testimonials with outcomes, one primary CTA, calm microcopy.

### The composition test
Run any output against the test below. If three or more apply, the surface is generated:

- A centered hero with three equal cards below
- "Elevate / Seamless / Next-Gen" copywriting
- Purple-blue gradient anywhere
- Pure `#000` and pure `#FFF`
- "John Doe" or "Acme Corp" placeholders
- Default `shadcn/ui` rounded corners and shadow tokens
- Lucide user-egg avatars
- Generic 24px-blur drop shadows on every card
- Customer logos in original brand colors
- Animated number counter on a stat that isn't real proof
- "Get Started" as the only CTA
- Section labels like "SECTION 01" or "OUR PROCESS"
- Title Case headlines
- Inter at default weight with no tracking adjustment
- Auto-rotating carousel under 4 seconds
- Floating chatbot bubble blocking the CTA
- 6-line wrapped H1
- Body type at 14px
- Stock photography of teams laughing at laptops
- Brain / sparkle / neural-network icon as the "AI" mark
- Confetti or sparkle on a success message
- Email-capture modal popup on a timer

The further any output drifts from these fingerprints, the closer it lands to senior-designer baseline. The fingerprints exist because the generator reaches for them reflexively. Knowing them is half the fix; refusing them is the other half.

---

## The closing principle

Output that defeats AI bias is indistinguishable from work by a senior frontend designer who has spent a decade unlearning their own defaults. Every directive here exists because the default behavior fails in a specific, measurable way. The rules are not stylistic preferences — they are corrections for known failure modes.

Match implementation complexity to aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details.

Pick a clear conceptual direction and execute with precision. Bold maximalism and refined minimalism both work. Intentionality is the differentiator, not intensity.

Don't hold back. Show what's possible when you commit fully to a distinctive vision — then strip everything that doesn't serve it.
