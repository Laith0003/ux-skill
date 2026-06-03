# Anti-slop — the forbidden patterns

Default model output has measurable, predictable failure modes. This file catalogues them. Every entry here exists because the unconstrained generator reaches for it reflexively, and the result reads as machine-made.

Treat each ban as a hard rule unless a brief explicitly overrides it. The goal is not stylistic preference — it is the elimination of fingerprints that mark output as generated.

---

## Principles

1. **Specificity beats genericity.** A generic three-card row is the strongest AI tell. Asymmetry, named brands that fit the product's market, organic numbers — these signal a human (or a careful machine). The fastest way to ship slop is to use the safest defaults the model offers.

2. **Restraint beats decoration.** Single accent color, neutral base, intentional whitespace. Don't add a gradient because the model defaults to one. Don't add a glow because the surface needs "polish." A surface needs a job, not ornament.

3. **Type carries weight, not just size.** Hierarchy comes from weight + color + spacing — not from `text-9xl`. Oversize H1s that scream just because they're H1s are amateur. Premium type whispers at scale.

4. **Motion has meaning or it doesn't ship.** Decorative animation is slop. Every motion expresses cause and effect, confirms a state change, or invites engagement. Bouncing for the sake of bouncing dates the work in six months.

5. **Content is a design surface.** "John Doe" + "Acme Corp" + `99.99%` is content slop and ruins the design regardless of layout quality. Treat placeholder content with the same care as the layout that holds it.

6. **Imagery is mandatory and real.** A text-only wall reads as a memo, not a product. Every layout accommodates imagery — never avoids it. Use the client's own assets first; fill the gaps with curated Unsplash/Pexels chosen to match the brand and the 7-axis temperature, then treat them so they read as deliberate. An abstract SVG is NOT a substitute for a real product or site image. Only *random/generic* stock (and the auto-rotating placeholder services) is banned — real photography, chosen on purpose, is the goal.

7. **Convention over cleverness on navigation.** Logo top-left. Nav top or left. Search is a magnifying glass. Innovate when you know you have a better idea; otherwise honor convention so the user can scan.

8. **Clarity over consistency.** When making something significantly clearer requires slight inconsistency, choose clarity every time.

---

## Responsive / mobile-first (non-negotiable)

Mobile is not the small version of the desktop — it is where most of the traffic lives and where the defects ship. The failures below recur on every unconstrained build because the generator designs at desktop width and never re-checks the phone. They are not taste calls; they are correctness.

1. **Mobile-first, and verify it.** Every layout MUST work at 360–390px with ZERO horizontal scroll. Horizontal scroll on mobile is a CRITICAL fail — the single most common shipped defect. ALWAYS verify it before declaring done: render the output at 390px and assert `document.documentElement.scrollWidth <= window.innerWidth`. If it overflows, it is not finished, no matter how good the desktop view looks.

2. **Every multi-column block collapses to one column at ≤640px.** Hero text + form, image + text, card rows, stat bars — all of them. A fixed multi-column grid that overflows on a phone is never acceptable. Set the single-column breakpoint explicitly; never let a `1.05fr 0.95fr` (or any `Nfr Mfr`) survive to mobile, and never define the columns in an inline `style` you cannot media-query.

3. **Nothing escapes its container.** No absolutely-positioned element may bleed outside its parent or "pop out" on small screens. Decorative glows, off-canvas art, and oversized media are all clipped or contained — a `width: 100vw` block overflows by the scrollbar width and is banned; size to `100%`/the container, not the viewport.

4. **Never ship a literal placeholder token.** `{TODO_FILL...}`, `{{ var }}` mustache left in markup, "lorem ipsum" — none of these reach the rendered UI. If a value is genuinely absent (no phone number, no OG image), OMIT that element gracefully — drop the affordance, don't print the token. A visible `{TODO_FILL: phone}` in a sticky header is the rawest draft-state leak there is.

5. **Imagery as backdrop, not just an icon.** Where it adds depth — hero, location/coverage cards, feature tiles — use a REAL image as the section or card background with text overlaid and a readable scrim, not a flat card with one lone icon. A single centered icon on a bare card is a slop tell precisely where a backdrop image would have carried the surface. (The icon-per-item rule for lists still holds; this is about sections and feature/coverage cards that read as empty without imagery.)

6. **Never repeat one icon across differentiated items.** Every skip size, every plan, every sector rendered with the same box/grid/check icon reads as the generator giving up. If you cannot source a DISTINCT, meaningful icon per item, drop the icons there entirely and differentiate with TYPOGRAPHY (scale, weight, the number itself), color, or layout. A repeated icon is worse than no icon — it actively says "these are the same" about things you are claiming are different.

7. **Short labels never wrap to a second line.** The brand wordmark, every button/CTA label, and nav links are short, fixed phrases — they must stay on ONE line at 360px. Wrapping a 2-3 word label ("Instant Skip / Hire", "Get a / quote") is the textbook *break-by-accident*: the box got too narrow and the browser improvised, and it reads as broken. `white-space: nowrap` them and size them to fit (shrink the wordmark font on mobile, tighten gaps); if the full wordmark still cannot fit beside the logo + the primary CTA, drop to the **logomark alone** (hide the words, keep the icon) — never two lines. This is invisible to a horizontal-scroll check: a nav that wraps to two rows still reports `scrollWidth == innerWidth`, so it must be verified directly (the wordmark's and each label's rendered height stays at one line: `scrollHeight <= 1.4 * lineHeight`). Note `nowrap` alone can trade the wrap for horizontal scroll — pair it with a size-to-fit and confirm both.

---

## Forbidden — visual & CSS

| Don't | Do instead |
|---|---|
| Default `box-shadow` glows, neon outer glows | Inner border (`border-white/10`) + tinted inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) |
| Pure black (`#000000`) | Zinc-950, charcoal, off-black — `#0a0a0a`, `#111111` are correct |
| Pure white (`#FFFFFF`) on premium marketing | Warm off-white in the `#FAFAF8` to `#F7F6F3` range; pure white reads as default |
| Oversaturated accents (>80% saturation) | Desaturate. High contrast comes from value, not saturation |
| Text-fill gradients on large headers | Solid color + weight hierarchy. One word in gradient per page is the absolute maximum |
| The "AI" purple-to-blue gradient on white | A single restrained accent (Emerald, Electric Blue, Deep Rose, Amber) against neutrals |
| Full-bleed gradient hero backgrounds covering large surfaces | Gradients sit inside narrow 30–60° hue windows at low saturation, used as accents not as canvas |
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
| `h-screen` on hero | `min-h-[100dvh]` — iOS Safari's address-bar collapse breaks `h-screen` |
| Flex math like `w-[calc(33%-1rem)]` | CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) |
| `border-radius: 9999px` on non-tag elements (pill cards, pill primary buttons) | Pill shape is reserved for tags, status badges, sometimes primary CTAs in maximalist styles |
| Inconsistent corner radii across components | Pick 2-3 radii and commit. Mixing 4, 8, 12, 16, 24px across a single page reads as undisciplined |
| Hard-edged dark slabs alternating with white slabs as section dividers | Use eyebrow tags and whitespace rhythm to separate sections; reserve full-color bands for one or two moments per page |

---

## Forbidden — typography

| Don't | Do instead |
|---|---|
| Serif faces on dashboards, admin, data UIs, software UIs | Sans only. Geist + Geist Mono, Satoshi + JetBrains Mono, IBM Plex Sans + IBM Plex Mono, or similar disciplined pairings |
| H1 that screams (`text-9xl`) just because it's an H1 | Hierarchy from weight + color + spacing; cap display at `text-4xl md:text-6xl tracking-tighter leading-none` unless the brief is maximalist |
| H1 wrapping to 4, 5, or 6 lines | 2–3 lines maximum. Widen the container (`max-w-5xl`, `max-w-6xl`, `w-full`) and use `clamp()` to scale the font down |
| Mismatched font families per section | One display + one body across the entire project. If a serif appears, it appears surgically — once or twice per page maximum |
| Body text > 75 characters per line | `max-w-[65ch]` on paragraphs. Roughly 55-72 characters per line is the editorial sweet spot |
| Body type below 16px on marketing surfaces | 16-18px minimum. Compressed body type reads as a startup template |
| Arial, Roboto, generic system stacks as primary display | Distinctive display face (Geist, Satoshi, Cabinet Grotesk, Outfit) — or a deliberately chosen variable sans. Note: Inter is a legitimate, modern choice; pair it carefully and don't reach for it reflexively as the only option |
| Default font-fallback chains (the standard humanist sans most platforms ship) | Choose the type intentionally even when the brief doesn't specify |
| Same display family across every output | Vary across generations. Never converge on one stack repeatedly |
| Title Case Across Every Word In Headlines | Sentence case. Title case reads as advertising copy from a previous decade |
| ALL CAPS headlines at >14px | All-caps reserved for eyebrow labels at 10-13px with tracked spacing (0.05em-0.1em) |
| All-caps for body copy, subheads, or anything readable | Breaks legibility. Reserved for eyebrow labels only |
| Italic used as decoration | Italic means "this is a title" or "I am emphasizing this word" — not "this is a fancy moment" |
| Tracking left at 0 on display sizes (>48px) | Tighten display tracking by -1% to -3% (-0.01em to -0.03em). The fix that separates polished from amateur |
| Tabular figures mixed with proportional figures on the same page | Pick one. Stat blocks, prices, version strings get tabular; prose gets proportional |
| Straight quotes (' "), double-hyphen (--) | Curly quotes ('') and em dashes (—) where appropriate. Get these right |
| Decorative or handwritten display faces on premium surfaces | Personality comes from scale, weight contrast, and whitespace — not face selection |
| 5+ weights from the same family | Three-weight system at most: bold/semibold for display, regular for body, lighter for support |
| Variable font weight animated for decoration only | When variable axes animate, the motion expresses state change — not "look at this font" |
| Eyebrows that aren't tracked (`+0.05em` to `+0.10em`) | All eyebrows are tracked. The wide tracking is the whole point |

---

## Forbidden — layout & spacing

| Don't | Do instead |
|---|---|
| 3-equal-cards horizontal feature row | 2-column zig-zag, asymmetric grid, horizontal scroll, or bento. The 3-equal pattern is the strongest AI tell |
| 5-column or 9-tile feature grids cramming every capability into one screen | 3-5 marquee feature sections, each with a deep visual. Width breeds shallowness; depth wins memory |
| Centered hero with text over dark image | Asymmetric hero — text left or right, image with subtle stylistic fade |
| Center alignment as a fallback when no layout decision is made | Center alignment is a deliberate choice for hero callouts, isolated lockups, or final CTAs — not a default |
| Center alignment when DESIGN_VARIANCE > 4 | Split screen (60/40 or 65/35, not 50/50), left-aligned over right-aligned, asymmetric whitespace |
| `h-screen` on mobile hero | `min-h-[100dvh]` — never `h-screen` |
| Horizontal scroll on mobile from off-screen animations | Wrap the page in `overflow-x-hidden w-full max-w-full` |
| Marketing sections at `py-12` or less | `py-32 md:py-48` minimum on desktop, 64-96px on tablet, 48-72px on mobile. Sections must feel like distinct chapters |
| Symmetric 50/50 split-screen heroes | 7/5 or 5/7 split. The asymmetry creates hierarchy without typography variance |
| Symmetric three-column grids without massive whitespace gaps | Asymmetric bento, or split with one column dominant |
| Random spacing increments (5px, 11px, 23px) | 4/8 rhythm — every gap, padding, margin in multiples of 4 |
| Content max-width >1400px | Cap at 1200-1400px. Beyond that, line-length becomes punishing and the eye loses anchor |
| Bootstrap-style symmetric grids with 24px gutters | The grid exists to allow alignment, not to enforce density. Most marketing sections only need 1, 2, or 8 columns |
| Meta-labels like "SECTION 01", "QUESTION 05", "OUR PROCESS 02", "ABOUT US" as decoration | Strip them entirely. If the section needs a label, use a small eyebrow naming the category — not numbered chapter signposting |
| "Section X of Y" indicators | Eyebrow tags replace decorative section dividers. Numbered chapter framing only when the product genuinely is a journey |
| Cramped feature cards with 9-12 tiny tiles in a 3×3 or 4×3 grid | 3-5 themed sections with one feature focus each. The dense grid reads as a single visual unit and the reader remembers nothing |
| Floating elements with awkward gaps | Padding and margins are mathematically intentional |
| Cookie-cutter left-text-right-image hero as the default reach | Editorial split (massive whitespace between halves), curtain reveal, asymmetric float, or full-bleed background |
| Cards bare on background without any structure | Bordered (1px hairline), bezel-wrapped (in maximalist styles), or grouped by spacing — but never floating without context |
| Cards mixing structure within the same row | Inside a row, all cards share one anatomy — same icon position, same heading scale, same internal padding |
| Card paddings mixed across the page (16px here, 32px there) | Choose 24-32px or 32-40px and commit. Mixed-padding cards on the same page break rhythm |
| Pricing tables on the homepage | Tease pricing with a "starts at $X" line + link out. Full pricing tables on the homepage feel sales-y |
| Long bare bullet lists of features | Features get marquee treatment with visuals, not bare bullets |
| Multi-row navigation with mega-categories crammed across two rows | Slim nav (60-72px tall), 5-7 items, two action buttons right edge. Mega-menus open on hover |
| Footer treated as filler | Footer is a sitemap: 4-6 columns by audience (Product, Solutions, Resources, Company, Legal) |
| Thin one-row footer with three social icons | The footer is generosity after the page's restraint |

---

## Forbidden — content & data (the "Jane Doe" effect)

The single fastest way to mark output as AI-generated. The design can be perfect; if the placeholder content is generic, the whole surface reads as slop.

| Don't | Do instead |
|---|---|
| "John Doe", "Jane Smith", "Sarah Chan", "Jack Su", "Test User" | Creative and plausible names that fit the product's market |
| "example@example.com", "user@email.com" | Realistic, contextual emails |
| "Acme", "Nexus", "SmartFlow", "Zenith", "Stellar", "Vertex", "Apex" | Contextual brand names. A fintech is "Ledgerine" or "Tash"; a CRM is "Patio" or "Greta" |
| Round / suspicious numbers: "99.99%", "50%", "1234567", "$10,000" | Organic, messy data: "47.2%", "63%", "$8,247.30", "+1 (312) 847-1928" |
| Default Lucide / Heroicons egg avatars | Real/licensed photos, or distinct SVG initials with intentional styling. When you need a stand-in face, source a curated, on-brand portrait (Unsplash/Pexels) rather than an auto-rotating placeholder; the linter flags *random/unseeded* services HIGH. |
| Lorem ipsum, "Your text here", "Placeholder content" | Generate realistic content based on the brief. If a mockup exists, extract text from it |
| Filler verbs: "Elevate", "Seamless", "Unleash", "Next-Gen", "Empower", "Revolutionize", "Transform", "Leverage", "Robust" | Concrete verbs naming what the product actually does: "Send", "Settle", "Track", "Decide", "Ship", "Deploy", "Query" |
| AI copywriting clichés: "delve", "blazingly fast", "game-changer", "world-class", "industry-leading", "innovative" | Specific numbers and named outcomes. "75ms latency" beats "blazing fast"; "98% of category leaders" beats "trusted by leaders" |
| Generic "Get Started" / "Learn More" as the only CTA | Specific verbs naming what happens next: "Run the demo", "See the dashboard", "Open account", "Start free", "Deploy", "Run a query" |
| Random/generic stock (teams laughing at laptops, the first Unsplash hit) | Client assets first, then curated Unsplash/Pexels chosen to match the brand + 7-axis temperature — pick the best per slot, don't paste the first credible photo. Treat them (grayscale, mix-blend-luminosity, opacity-90, contrast-125) so they read as deliberate. A real, chosen photo beats an abstract SVG, which is not a substitute for a product/site image. |
| Generic/clichéd stock (teams laughing at laptops, businessmen pointing at charts, isometric workers) | Custom imagery, real product UI, or real editorial photography curated to the brand. The cliché is the ban — not photography itself; every surface still carries real imagery |
| Generic testimonial copy ("This product changed my life", "Amazing tool!") | Quantified, named testimonials: "We cut p99 from 380ms to 90ms. — Name, role, company" |
| Customer quotes without a name, role, or company | Name + role + company at minimum. Quotes with no attribution read as fabricated |
| Compliance badge logos in original full color | Single-color or grayscale, all logos at uniform optical weight |
| Fabricated / hand-drawn / abstract brand logos (an invented glyph standing in for Cursor, Stripe, Claude, etc.) | The REAL single-path SVG from `references/logos/` (or fetched from `cdn.simpleicons.org/<slug>` / the brand's own kit), `fill="currentColor"`. An approximated brand mark is an instant credibility leak |
| Stat callouts that are visibly invented ("99.99% uptime!") | Real numbers or organic-looking ones (47.2%, 280K, $8,247.30). Round numbers in stats read as marketing |
| Hyperbolic adjective stacks ("powerful, intelligent, transformative, seamless") | Signal of weakness in the underlying claim. Replace adjectives with specifics |
| Vague benefit copy ("faster", "easier", "smarter") | Specific numbers and named outcomes |
| "Trusted by 10,000+ developers" with no logos | Show logos or show nothing |
| "As seen in" press logos at radically different sizes | If the press logos lift the brand, render them uniformly at optical heights. If they don't, skip them |
| Customer logos in full color | Single mono treatment (all 70% black, all white, all neutral ink). Mixed-color logo walls read busy |
| Logo walls repeated 3+ times down a single page as filler | Once near the hero, optionally once before the final CTA. Repeating it more reads as overcompensation |
| Mentioning the product's own name in every sentence | "The platform", "your team", "the workflow" — constant self-naming reads insecure |
| First-person plural in headlines ("We help you...", "We believe...", "Our mission") | Address the reader directly or describe the outcome. "We" comes later, in trust copy and about pages |
| Exclamation marks in marketing copy | Confidence is performed by restraint. Reserved for in-product micro-celebrations and even then sparingly |
| Question-form headlines as faux-rhetorical setup ("Tired of slow workflows?") | Declarative statements. Question headlines are reserved for genuine questions |
| Multiple primary CTAs above the fold | One primary, optionally one secondary. Two filled CTAs of equal weight dilute the primary path |
| Form fields asking for too much in the first interaction | 3-4 fields ceiling for "book a demo" or signup flows |
| Brain icons, sparkle icons, neural-network nodes, glowing dots as "AI" iconography | Restrained generic icons — a small star, a triangle, an arrow. No "AI" visual vocabulary |
| Confetti, sparkle emojis, or celebration explosion on success states | Calm success: "50 points added", "Account ready", "Invite sent" |
| Numbered version badges in marketing headlines ("Now with v3.7!") | Say "new" or "now", or name the new feature directly |
| Pop-culture references and casual handwritten fonts on primary surfaces | Wit lives in copy cadence, not in typeface choice |
| Industry-vertical names where they don't apply ("Built for fintech, healthcare, retail") | Horizontal positioning by role ("For designers", "For builders", "For teams") |
| Buzzword stacking ("AI-powered next-gen platform") | Plain verb-noun honesty: "Build sites", "Take notes", "Run queries" |

---

## Forbidden — interaction & motion

| Don't | Do instead |
|---|---|
| Static "success" state with no loading / empty / error variants | Always ship all four states. Missing states are a quality failure |
| Generic circular spinners | Skeletal loaders matching the eventual layout shape |
| Vague empty states ("No items yet", "No data") | Empty states explain what should be there and how to make it appear: "Connect your first source to start" |
| Vague errors ("Form contains errors", "Something went wrong") | Name the field and the action. "Phone number missing — add a number to continue" |
| Linear easing on UI motion | `ease-out` on enter, `ease-in` on exit, custom cubic-bezier, or spring physics. `linear` and `ease-in-out` read as unconsidered |
| Instant state changes (0ms) | 150-300ms for micro-interactions. Below 100ms is invisible |
| Slow motion (>500ms on micro, >1000ms on hover) | Cap micro at 300ms, complex at 400-800ms, never >1500ms |
| Continuous animations driven by `useState` | `useMotionValue` + `useTransform` only. `useState` causes re-render storms |
| Perpetual motion components that re-render the parent | Wrap perpetual loops in `React.memo` and isolate to leaf Client Components |
| Hover-only critical interactions | Tap/click for primary; hover is enhancement only. Mobile has no hover |
| Animating `width`, `height`, `top`, `left` | `transform` + `opacity` only — hardware acceleration |
| Ignoring `prefers-reduced-motion` | Wrap motion in a reduced-motion check. Replace transforms with simple opacity fades, shorten durations, drop blur components |
| Scroll-jacking, scroll-snap that forces a sequence | The page scrolls naturally; reveals happen as the user reaches them |
| Horizontal scroll hijack as a default | Reserved for galleries or storytelling sequences with a real reason; never the default flow |
| Pinned-3d-element scroll-controlled video scrubbing as decoration | When scrub motion appears, it carries a real demo or sequence |
| Auto-playing background video with sound | Muted, looped, with a pause control. Sound is opt-in |
| Auto-playing testimonial videos on page load | Opt-in. Auto-play is intrusive |
| Auto-rotating carousels under 4 seconds per slide | Either continuous marquees (no pagination dots, sub-conscious speed 20-40s loop) or scroll-snap horizontal lists with visible affordance |
| Hero carousels with auto-advancing slides | Single confident hero. If multiple stories must coexist, use tabs with manual control |
| Number counters that animate on every scroll past | Once per page entry. Settling jitter on the final number is a tell |
| Animated typewriter on the H1 | Reserved for content that is genuinely input (a search bar, a chat). Typewriter on a headline reads as gimmick |
| Bouncy spring animations on type | Spring physics on draggable UI elements (toggles, modals, drag handles), not on headline reveals |
| Page-load animations that loop endlessly on the wordmark | Once-on-load is the rule. Looping brand-mark animation in nav reads as distracting |
| Device orientation / motion permission prompts for parallax | Pointer events only. Phone-tilt parallax requires sensor permissions that erode trust |
| Cursor-following effects on every clickable element across the page | Cursor effects are scoped — to a hero canvas, to one demo surface. Global cursor effects are noise |
| Big animated number sequences as decoration | Counters anchored to a real metric. Decorative counters feel like a gimmick |
| Modal popups for newsletter signup on a timer | Newsletter signup goes in the footer or a sidebar component, not as a time-triggered interstitial |
| Cookie banners blocking first paint | Slim, monochrome, bottom-bar or sidebar treatment that respects the page |
| Floating chat widgets overlapping the primary CTA | Position chat where it can't compete, or hide it on hero |
| Sticky chatbot bubbles in the corner on first load | None of the premium cohort does this. Wait for engagement |

---

## Forbidden — components

| Don't | Do instead |
|---|---|
| Generic card containers everywhere | Cards only when elevation communicates hierarchy. Otherwise use `border-t`, `divide-y`, or pure negative space |
| Dashboard cockpit-density UIs wrapped in card boxes | When `VISUAL_DENSITY > 7`, use logic-grouping via hairlines and negative space. Data metrics breathe without boxing |
| Generic 3-column feature grids | See layout bans. Bento, masonry, asymmetric, zig-zag |
| Generic testimonial sections of 15+ unattributed quotes | 2-3 strong, named, quantified quotes beat 15 vibes-only |
| Cards with default rounded corners and drop shadows as the page baseline | Cards earn their elevation. Most surfaces don't need card chrome |
| Emoji as visual elements anywhere | Anywhere. Code, comments, markup, alt text, UI strings, microcopy. Use SVG icons or text |
| Mixed icon styles (filled + outline at the same hierarchy level) | One icon family, one stroke weight, one fill state at any given level |
| Mixing icon families (Lucide + Heroicons + Phosphor in the same project) | One family, committed |
| Stroke-width inconsistency (mixing 1.5 + 2.0 in the same surface) | Pick one stroke and stick with it |
| No imagery anywhere (text walls of cards) | Imagery is mandatory and real. Real product UI when available; otherwise curated, on-brand stock (Unsplash/Pexels) chosen by temperature. A descriptive inline-SVG illustration can support a section but is NOT a substitute for the real product/site image. Random/unseeded placeholder services never ship |
| Stock-photo placeholder divs as "image here" markers | Real imagery or hand-styled SVG/CSS placeholders. Stock-placeholder divs ship as the final shippable mistake |
| Random radius values across components (4, 8, 12, 16, 24px on the same page) | Token: `rounded-sm` / `md` / `lg` / `2xl` / `[2.5rem]` — pick a scale, commit |
| Toasts that steal focus | `aria-live="polite"` toasts. Never grab focus |
| Placeholder-only form labels | Visible label above input, helper below input, error below input |
| Form fields with no helper text markup at all | Helper text slot exists in the markup even when empty, so error states don't cause layout shift |
| Default `shadcn/ui` styling | Customize radii, colors, shadows to match the project aesthetic. Default `shadcn` is a recognized AI tell |
| Floating stamp / badge icons on hero text | If the hero needs a label, use a small eyebrow tag above the H1 |
| Pill tags scattered under the hero as decoration | Pills work as status indicators or single-eyebrow taxonomy, not as decorative confetti |
| Raw data / stats dumped in the hero ("100k users", "99.99% uptime" in the hero subhead) | Stats earn their place lower on the page with context. Hero subhead clarifies, doesn't quantify |
| Naked trailing arrows on CTA text | In high-end styles, wrap the arrow in its own circular bezel inside the button (button-in-button pattern). In minimalist styles, the arrow sits naked inline — but tracked properly |
| Default heavy drop shadows on cards | Hairline 1px borders, near-invisible shadows (4-8% alpha), or rely on background contrast |
| Generic line-icon clichés (lightbulb, rocket, lock) | Purposeful, often custom icons. The lightbulb cliché is absent from every premium cohort |
| The "hero with a giant fake browser window tilted in 3D space" as decoration | Product screenshots presented flat or with subtle 6-12° tilt where it serves a "design object" framing — not as default flair |
| OS chrome stripped from product screenshots | Real OS chrome (traffic lights, menubar, status bar) grounds the screenshot as real software. Stripping it makes it read as prototype |
| Generic font-fallback chains (the standard humanist sans most platforms ship) | Choose intentionally even when the brief is silent |

---

## Tokens / numeric guardrails

- **Color saturation**: < 80% for any accent in restrained styles; saturated jewel tones acceptable in maximalist styles but reserved for small surface areas, never full-bleed
- **Contrast**: ≥ 4.5:1 for body text, ≥ 3:1 for large/UI text. AAA where possible on primary copy
- **Spacing**: multiples of 4 (4, 8, 12, 16, 24, 32, 48, 64, 96, 128, 160)
- **Touch targets**: ≥ 44×44 pt (iOS), ≥ 48×48 dp (Android) regardless of visual render
- **Animation duration**: 150-300ms micro, ≤ 400ms complex hover, 400-800ms major reveals, 600-1200ms cinematic transitions, never > 1500ms
- **Body line length**: 35-60 chars mobile, 55-72 desktop (`max-w-[65ch]`)
- **Max H1 lines**: 2-3 (4 is failure, 5 is catastrophic, 6 is disqualifying)
- **Container max-width**: 1200-1400px or `max-w-7xl`
- **Marketing section padding**: `py-32 md:py-48` minimum on desktop
- **Card internal padding**: 24-40px
- **Font scale**: 12 / 14 / 16 / 18 / 24 / 32 / 48 / 64 / 96 / 144 — pick a 4-step subset and commit
- **Body font size minimum**: 16px on marketing, 15-16px on dashboards
- **Display line-height**: 1.0-1.15
- **Body line-height**: 1.5-1.7
- **Display tracking**: -0.01em to -0.03em at >48px
- **Eyebrow tracking**: +0.05em to +0.10em uppercase
- **Image aspect ratios**: 16:9, 4:3, 1:1, 4:5 — vary intentionally, never random

---

## Severity-tagged checklist

Run before shipping any UI output. Severity tags indicate the failure mode if violated.

### Critical (blocker — ship is not possible)
- [ ] No purple-to-blue "AI" gradient on white
- [ ] No generic names ("John Doe", "Jane Smith")
- [ ] No "Acme / Nexus / SmartFlow" filler brand placeholders
- [ ] No Lorem ipsum, no "Your text here" placeholder content
- [ ] No emojis anywhere (code, markup, UI, alt text, microcopy)
- [ ] All four interaction states present (loading, empty, error, success/default)
- [ ] No `h-screen` on mobile hero
- [ ] No horizontal scroll at 360–390px (`scrollWidth <= innerWidth`) — verified, not assumed
- [ ] Nav stays ONE row at 360px and NO short label wraps — brand wordmark, button/CTA labels, nav links each on one line (`scrollHeight <= 1.4 * lineHeight`); verified directly, since `scrollWidth` alone misses a wrapped nav
- [ ] No literal placeholder token shipped (`{TODO_FILL...}`, `{{ var }}`, "lorem ipsum")
- [ ] No pure `#000` text or background
- [ ] No 3-equal-cards feature row
- [ ] No "SECTION 01" / "QUESTION 05" / decorative meta-labels
- [ ] No exclamation marks in marketing copy

### High (must fix before review)
- [ ] H1 ≤ 2-3 lines max
- [ ] Every multi-column block (hero, image+text, card rows, stat bars) collapses to one column at ≤640px
- [ ] Sections/feature/coverage cards use a real backdrop image where depth is needed, not a lone icon on a bare card
- [ ] No single icon repeated across differentiated items (distinct icon per item, or none + typographic differentiation)
- [ ] No serif on dashboards or software UIs
- [ ] Centered hero only when DESIGN_VARIANCE ≤ 4 or by intentional choice
- [ ] All animations on `transform` + `opacity` only
- [ ] `prefers-reduced-motion` respected
- [ ] No GSAP + motion library in the same component tree
- [ ] No scroll-jacking
- [ ] Imagery is present, real, and intentional (no text-only walls; no abstract SVG as a stand-in for a real product/site image)
- [ ] Icons are one consistent family at consistent stroke width
- [ ] No customer logos in original full color
- [ ] No hover-only critical interactions
- [ ] No oversaturated accents (> 80% in restrained styles)
- [ ] No multiple gradient sections
- [ ] No filler verbs ("Elevate", "Unleash", "Next-Gen")
- [ ] Specific CTAs, not "Get Started" / "Learn More" reflexively
- [ ] Footer is a sitemap, not a one-row strip

### Medium (polish — fix before final)
- [ ] H1 in sentence case (not Title Case)
- [ ] Display tracking tightened (-0.01 to -0.03em)
- [ ] Body line-length capped at ≤ 65ch
- [ ] Body type at 16-18px minimum on marketing
- [ ] Single accent color, < 80% saturation in restrained styles
- [ ] Spacing on 4/8 rhythm
- [ ] Imagery is real and chosen: client assets first, then curated Unsplash/Pexels by temperature — no random/generic stock, no abstract SVG standing in for a real product image
- [ ] One icon family at consistent stroke width
- [ ] Eyebrow labels tracked (+0.05em to +0.10em)
- [ ] Corner radii consistent (2-3 values max across the page)
- [ ] Numbers organic, not round (47.2%, not 99.99%)
- [ ] Color saturation tuned separately for light and dark modes
- [ ] No press logos with publications nobody recognizes
- [ ] No "Trusted by 10,000+ developers" with no logos shown
- [ ] No naked trailing arrows on CTAs in high-end styles (button-in-button pattern instead)

### Low (taste calls — flag but don't block)
- [ ] No mention of the product's own name in every sentence
- [ ] No first-person plural in headlines ("We help you...")
- [ ] Testimonials have name + role + company minimum
- [ ] Press logos quieter than customer logos
- [ ] Number formatting honest (no false precision)

---

## AI Tells by category — the meta-fingerprints

These are the combinations that, when they co-occur, mark the output as machine-made within seconds of viewing. Each one alone is a signal; together they are a confession.

### The composition fingerprint
- Centered hero + left-text-right-image as default reach + 3-equal cards below + decorative meta-label numbering = generated.
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
- Fix: names that fit the market, brands that fit the category, numbers that read as organic, verbs that name what the product does.

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
