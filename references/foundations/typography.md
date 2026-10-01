# Typography

> Disciplined type carries hierarchy without decoration. The scale, weight, and line-height system is what makes an interface read as composed instead of accidental.

## Principles

1. **The display is detached from the rest.** The display role sits well above the section headings: 60 to 240px at 1440 by the brand's expressiveness (character.landing_display_px), 36 to 90px on a phone, fluid in between. The ladder below it holds 6 to 10 sizes, one level at least 1.08 times the next.

2. **Weight follows size and formality.** The display sets at 400 to 650 in fifties, lighter for a formal brand and for a large display (character.display_weight); body at 400. Three or four weight steps cover an entire system. Five or more weights signal an undisciplined ramp.

3. **Line height falls as size rises.** Body sits at 1.5 to 1.7. The display runs 1.12 at 40px down to 1.0 for a muted brand or 0.92 for a bold one at 160px and up (the system's `type.leading` steps, floor 0.88); Arabic display stays at least 0.15 above.

4. **Tracking tightens as type grows, loosens as it shrinks.** The display tightens with contrast; capitals track at 0 or open, since they already sit close. Labels open up with formality. Body stays at default tracking.

5. **Sentence case is the default.** Reserve title case for proper nouns and trademarked product names. Capitals belong to short labels, and to the display of a loud brand whose system leans to capitals (character.capitals, emitted as `type.capitals`: under 0.5 the lint reports a capitals display; `type.text.display-caps`). Title-case headlines on every word read as enterprise from a previous decade.

6. **Line length is policed.** The measure counts characters of the text face: 42 to 56 on a landing page (`layout.measure.landing`), 60 to 70 for reading, 60 to 66 for a long read. Headlines wrap balanced (`text-wrap: balance`), paragraphs pretty (`text-wrap: pretty`).

7. **Numbers get the tabular treatment in data UI** — Tabular figures align decimals and prevent layout shift on count-up. Reserve proportional figures for prose. Mixed proportional and tabular on the same page reads as undisciplined.

8. **No serifs on dashboards or software UIs.** A dashboard is read at a glance, in dense rows; a serif headline there fights the data. Serifs belong to long reading and to display moments inside otherwise-sans pages.

9. **Pair two typefaces at most** — A display face plus a body face, or a sans plus a mono. Three faces only when a clear hierarchy demands it (sans, serif, mono for editorial-tech hybrids). Two display fonts together is banned.

10. **Optical contrast matters more than face novelty** — A well-cut neo-grotesque used across an entire system beats a flashy display face deployed once. Restraint in face selection magnifies the moves you do make.

## Do / Don't

| Do | Don't |
|---|---|
| Use a single workhorse sans-serif at varying weights for most surfaces | Mix five fonts across one page |
| Set body at 16 to 18px with line-height 1.5 to 1.7 | Set body below 12px or above 22px on web |
| Take display tracking from the system, tighter as contrast rises | Use the same tracking on display and body |
| Use sentence case for headlines | Use Title Case On Every Word |
| Set display line height from the system's steps, 1.12 down to 0.92 as the size rises | Run display headlines at body line-height (looks like a stack) |
| Use tabular figures in tables, dashboards, prices, timers | Use proportional figures for vertically aligned numeric columns |
| Pair sans with a mono for technical contexts | Pair two display faces together |
| Use weight changes (400 to 600) to signal hierarchy | Use color alone to signal hierarchy |
| Use capitals for short labels, and for a loud brand's display on its capitals role | Use capitals for body or subheads at any size |
| Standardize on one type ramp of 6 to 10 sizes with one detached display | Invent new sizes per component |
| Enable curly quotes in production copy; break sentences with a period, a comma or a colon | Ship straight quotes, em dashes or a double hyphen as punctuation |
| Reserve italic for genuine emphasis or titles | Use italic as decoration |
| Match optical size to rendered pixel size when the face supports it | Use a single optical variant across display and body |
| Wire `font-display: swap` so text remains visible during font load | Allow invisible text (FOIT) during font load |

## Examples

### Pattern: Display headline at hero scale
**Use when**: Hero or section opener carrying the page's primary claim.
**Anti-pattern**: 6-line wrapped headline crammed inside a narrow container, or a hero headline at 24px hoping weight will carry it.
**How**: Bind the H1 to `type.text.display`, a fluid clamp the system derives from the brand: 60 to 240px at 1440 by expressiveness, 36 to 90px on a phone. Line height from the system's display step, `text-wrap: balance` so the lines land on beats. The line limit lives in `references/surfaces/landing.md` (Hero composition); if the H1 overflows it, widen the container before the size shrinks.

### Pattern: Editorial body with measured column
**Use when**: Long-form marketing prose, documentation body, or any reading-intensive surface.
**Anti-pattern**: Body text running 100+ characters per line across a wide viewport.
**How**: Size body at 16 to 18px, regular weight, line-height 1.55 to 1.7. Clamp paragraph width to `max-w-[65ch]` or roughly 32 to 40em. On wide viewports, the canvas stays wide; the column stays narrow. This is the magazine effect.

### Pattern: Eyebrow + headline
**Use when**: A section needs a label its heading cannot carry: a step number, a category. Eyebrows never separate sections; space and a change of ground do, and the share of sections with one follows formality (character.eyebrow_share).
**Anti-pattern**: Naming sections as "SECTION 01" / "ABOUT US" / "OUR PROCESS 02" — these are amateur-tier signposting and banned.
**How**: A short label sits above the headline at 10 to 13px, weight 500 to 600, tracking +0.06em to +0.10em, in muted neutral or a paired accent. Sentence case or uppercase both work; pick one and apply consistently. The eyebrow is text only: no line, dash or dot before or after it.

### Pattern: Stat callout
**Use when**: A specific number is the persuasion — latency, accuracy, customer count, savings.
**Anti-pattern**: Stacking five identical stat tiles in a row, or surrounding the number with vague modifiers like "blazing fast."
**How**: Set the numeral at 48 to 144px, weight 700 to 800, in tabular figures. Drop the unit label ("ms", "%", "x", "K", "M") to 40 to 60% of the numeral size. Place a short qualifier label below at 14 to 16px regular. Two or three stats per row maximum; more dilutes.

### Pattern: Inline monospace for literal values
**Use when**: Version strings, region codes, identifiers, percentages, keyboard shortcuts, or any value that is more "literal data" than "prose."
**Anti-pattern**: Using mono for body paragraphs, or never using mono at all in technical contexts.
**How**: A geometric or programming mono one size step smaller than surrounding body. Inline values render in mono inside otherwise-sans copy. Keyboard shortcut chips render mono inside a low-radius pill with a 1px hairline border.

### Pattern: Three-weight hierarchy
**Use when**: Establishing typographic system for the entire product.
**Anti-pattern**: Five or six weights from the same family used in arbitrary roles.
**How**: Pick three weights — typically 400 (body), 500 (UI labels, secondary headlines), 600 or 700 (display headlines). Italic and light weights stay out of the system unless the brief specifically demands them. The intentional gap between 400 and 600 makes hierarchy unmissable.

### Pattern: Compressed type scale
**Use when**: Any page with a type system; the display's distance above the ladder grows with expressiveness.
**Anti-pattern**: A 12-step type scale with sizes at 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 28, 32px.
**How**: Define 6 to 10 sizes from one ladder: a detached display, section heading, subhead, body, small, label. Each size gets one weight and one line height. No size snuck in for a sidebar. The system is the constraint, and the constraint is the look.

### Pattern: Dark-mode weight compensation
**Use when**: Building a dark variant of the same typography system.
**Anti-pattern**: Reusing the same weight on light and dark and watching dark mode read as too thick.
**How**: Reduce font weight by roughly 50 units when going from light to dark for the same size (e.g., 600 in light becomes 550 in dark). This compensates for the apparent thickening of light type on dark background. Line-height stays the same across modes. Letter-spacing can loosen by 1 to 2% on body in dark mode.

### Pattern: Numerical specificity as typographic ornament
**Use when**: The page's persuasion is a measured figure the client gives, and the brand is formal.
**Anti-pattern**: "Big Stat" pattern with glowing 96pt numerals where the number is the only design move.
**How**: Concrete numbers (latency in ms, accuracy percentages, yield rates, fee figures) appear set at the same scale as the surrounding text but carry visual weight purely from their precision. The precision itself is the rhetoric. "75ms" inline at body scale persuades more than "Blazingly fast" at 96pt.

### Pattern: Long-form prose under a hero
**Use when**: The page argues a case at length and the reading context is long reading.
**Anti-pattern**: A trimmed-down tagline as the only body copy under an oversized hero.
**How**: Several premium surfaces allow paragraph-length body copy under the hero subhead — three or four sentences of substantive prose rather than a single tagline. Body sits at 15 to 17px, line-height 1.55 to 1.7. The willingness to use full sentences signals that the company has something to say.

### Pattern: Pull-quote treatment for testimonials
**Use when**: Customer testimonials in marketing surfaces.
**Anti-pattern**: Pull quote at body size with quote marks, no visual differentiation from surrounding paragraphs.
**How**: Pull quote sits at 28 to 40px, weight 500, line-height 1.3. Attribution beneath drops to body size with reduced contrast. The quote does not start with a quotation mark — instead, an oversized opening quote mark sits as a graphic element to the left or above. Set the quote at slightly larger size than body, regular weight, with the speaker's name and role beneath. No oversized quotation marks around the quote, no decorative card chrome, no logo overlay on the photograph.

### Pattern: Variable font weight animation
**Use when**: The face has a weight axis and the brand's motion is lively enough for one moving detail.
**Anti-pattern**: Variable axis animations on every label and headline — looks gimmicky.
**How**: A label tightens from 400 to 600 as the cursor approaches, or a number "settles" from 800 to 600 once a counter finishes animating. Cheap to ship if the font supports it; very expensive-looking on first encounter. Use sparingly — once or twice per page maximum. Disable under `prefers-reduced-motion: reduce`.

### Pattern: Mono for literal values (semantic role)
**Use when**: Version strings, region codes, percentage stats, build identifiers, inline data values.
**Anti-pattern**: Using a single sans family for everything and never signaling "this is a literal value."
**How**: Even outside code blocks, mono is doing semantic work: "this is a literal value, not prose." Inline values render in monospace inside otherwise-sans copy. Version strings, region codes, percentage stats, and build identifiers all render in mono. Keyboard shortcut chips render as compressed monospace inside a low-radius pill with a 1px hairline border.

### Pattern: Big stat with sized-down unit
**Use when**: Hero metric moments, KPI cards, headline numbers.
**Anti-pattern**: Stat numeral and unit at identical size, both shouting equally.
**How**: Big stat moments push to 96 to 144px, weight 700 to 800, sometimes in a contrast color or with a gradient fill (one word per page only). Decimal points and unit labels ("M", "K", "x") sized down by 40 to 60% from the numeral to create a marquee effect. The number itself does the persuading; the surrounding copy is just a label.

### Pattern: Single gradient word in a headline
**Use when**: High-end aesthetic that wants one moment of typographic personality.
**Anti-pattern**: Whole sentences in gradient text — reads as 2017 startup decoration.
**How**: One linear or conic gradient fills one carefully chosen word in the hero or a section headline. The rest stays plain. One word in gradient text in 2026 looks like craft; whole sentences look like decoration. The word chosen is the verb or the noun the page is selling.

### Pattern: Brutalist macro / micro contrast
**Use when**: High contrast, geometric type and low warmth: the loud, technical end of the axes.
**Anti-pattern**: Sans-serif at uniform scale across an entire brutalist surface.
**How**: Two compulsory voices — a structural heavy sans for headlines (`clamp(4rem, 10vw, 15rem)`, line-height 0.85 to 0.95, tracking -0.03em to -0.06em, uppercase) and a technical monospace for metadata (10 to 14px, `+0.05em` to `+0.10em` tracking, uppercase). The eye is never given a comfortable midrange — dense clusters of monospaced metadata sit immediately next to vast expanses of negative space framing macro-typography.

### Pattern: Single serif against an otherwise-sans page
**Use when**: Premium minimalist surfaces where a single editorial flourish carries personality.
**Anti-pattern**: Serifs scattered across the page in arbitrary roles.
**How**: One serif headline against an otherwise sans-serif page. Reserved for hero callouts, pull quotes, or occasional section openers. Maximum one per hero, maybe one per major section. Never a body face. Tracking tight (-0.02em to -0.04em). Line-height compressed (1.05 to 1.15 at large sizes). The serif appears surgically; the rest of the page commits to sans.

### Pattern: Three-weight system across the brand
**Use when**: Establishing the typographic system for an entire product.
**Anti-pattern**: A 6+ weight ladder where the differences between adjacent weights are imperceptible.
**How**: Collapse weight choices to three roles: bold or semibold for display (600 to 700), regular for body (400), light for support / metadata (300). The gap between 400 and 600 is intentional — it makes hierarchy unmissable. Italic and light weights stay out unless the brief explicitly demands them.

### Pattern: Numerals as editorial folios
**Use when**: Section numbering, step indicators, or chapter markers.
**Anti-pattern**: "SECTION 01," "CHAPTER 03": banned amateur-tier signposting.
**How**: Numbers and section markers in monospace, used like editorial folios. Small, tracked, set in a muted neutral. They function as orientation markers, not as decoration. The number itself is the marker; no surrounding meta-label.

## Tokens / values

### Scale (web, desktop default)
- Display: 60 to 240px at 1440 by expressiveness (`type.text.display`, a fluid clamp); capitals on `type.text.display-caps`
- Section heading (H2): 32 to 48px
- Subhead (H3): 20 to 24px
- Large body / lead: 18 to 22px
- Body: 16 to 18px
- Small / caption: 13 to 14px
- Eyebrow / small caps: 10 to 13px
- Code inline / shortcut chips: 13 to 14px

### Mobile floors
- Body: 16px minimum (prevents iOS auto-zoom on input focus)
- Display: 36 to 90px on a phone, from the desktop size (0.8 of it up to 72px, easing to 0.5 at 120px and up)

### Weight
- Display: 400 to 650 in fifties, lighter for a formal brand and a large display
- Subhead / UI label: 500 to 600
- Body: 400 to 450
- Caption / metadata / disabled: 400, sometimes paired with reduced opacity
- Reduce by ~50 units in dark mode for matching perceived weight

### Line-height
- Display: 1.12 at 40px down to 1.0 (muted) or 0.92 (bold) at 160px and up; floor 0.88
- Section heading: 1.15 to 1.3
- Subhead: 1.3 to 1.4
- Body: 1.5 to 1.7
- Small / caption: 1.3 to 1.4
- Brutalist display: 0.85 to 0.95 (intentionally cramped)

### Tracking (letter-spacing)
- Display: the system's step tracking, tighter as contrast rises
- Display in capitals: 0 or open (`type.tracking.caps`)
- Section heading: -0.01em to 0
- Body: 0 (default)
- Small / caption: 0 to +0.01em
- Eyebrow / small caps: +0.05em to +0.12em
- Brutalist macro display: -0.03em to -0.06em
- Brutalist mono micro: +0.05em to +0.10em

### Line length (measure)
- Mobile: 35 to 60 characters
- Landing paragraphs: 42 to 56 characters (`layout.measure.landing`); reading body: 60 to 70
- Long read: 60 to 66 characters
- Display H1: ultra-wide container (`max-w-5xl` to `max-w-7xl` or wider) — width prevents wraps, not narrowness

### Font loading
- `font-display: swap` for non-critical fonts
- `font-display: optional` for critical first paint
- Preload one or two weights of the primary family; do not preload every variant
- Variable fonts collapse multiple weights into a single file and are the default unless licensing forbids

### H1 line count
- 1 line: best
- 2 lines: acceptable
- 3 lines: tolerated only when the second clause is markedly shorter
- 4 lines: failure
- 5 lines: catastrophic
- 6 lines: disqualifying

### Font pairings by character

The engine picks faces from the axes (fonts.distance); these describe what each pairing does, never which business it belongs to.

**Elegant, high-contrast serifs:**
- Playfair Display + Source Sans 3: serif heading + clean sans body
- Cormorant + Inter: display serif + neutral sans
- Libre Caslon Display + Libre Franklin: classic editorial pairing
- Italiana + Inter: thin elegant serif + utilitarian sans
- Bodoni Moda + Inter: sharp contrast serif + clean sans
- Cardo + Roboto: refined book serif + standard sans
- EB Garamond + Inter: humanist serif + sans

**Playful / friendly:**
- Fraunces + Inter: quirky display serif + clean sans
- DM Serif Display + DM Sans: family pairing, modern playful
- Caveat + Inter: handwritten + sans
- Lobster + Open Sans: script + clean sans
- Pacifico + Open Sans: brush script + sans
- Quicksand + Quicksand: rounded sans across hierarchy
- Comic Neue + Open Sans: friendly + neutral

**Professional / trust:**
- Inter + Inter: single-family pairing, modern standard
- IBM Plex Sans + IBM Plex Mono: sans + mono for tech credibility
- Roboto + Roboto Mono: Material-aligned
- Source Sans 3 + Source Code Pro: open-source family
- Work Sans + Work Sans: single neutral family
- Manrope + Manrope: modern geometric sans
- Public Sans + Public Sans: plain, open and highly legible

**Modern / tech:**
- Geist + Geist Mono: modern minimal
- Satoshi + JetBrains Mono: geometric + dev mono
- Plus Jakarta Sans + Inter: modern + standard
- Onest + Inter: new geometric + standard
- General Sans + JetBrains Mono: versatile + mono
- Hanken Grotesk + Inter: grotesque + neutral
- Outfit + Inter: rounded geometric + sans

**Brutalist / editorial:**
- Space Grotesk + IBM Plex Mono: geometric quirky + mono
- Archivo Black + Inter: heavy display + clean body
- Anton + Open Sans: condensed display + sans
- Bebas Neue + Roboto: all-caps condensed + sans
- Druk + Inter: bold display + standard
- Monument Grotesk + Inter: neo-grotesque + standard
- NB International + IBM Plex Mono: tech-brutal pairing

**Display / statement:**
- Big Caslon + Inter: massive display serif + sans
- Recoleta + Inter: friendly contemporary serif + sans
- Migra + Inter: quirky display + sans
- PP Editorial New + Inter: modern serif + sans
- PP Neue Montreal + Inter: sharp grotesque + sans
- Tobias + Inter: refined display serif + sans

**Mono / technical:**
- JetBrains Mono: dev-focused mono
- Fira Code: mono with ligatures
- IBM Plex Mono: corporate mono
- Geist Mono: modern mono
- Berkeley Mono: premium mono
- Commit Mono: compact mono

Pick one mono and apply across code blocks, shortcut chips, metadata, and inline values.

### Banned typographic patterns
- Arial, Roboto, generic system stacks as primary display faces
- Serifs on dashboards or software UIs
- Inter used as the only reflex (acceptable as a body face but vary across projects
- Mixing two display faces together
- Title case on every word of every headline
- ALL CAPS body or subheads
- Oversized H1s that scream from scale alone (use weight and color for hierarchy)
- 6-line wrapped headings
- Decorative ligatures on body copy (standard ligatures are fine
- Straight quotes and double-hyphens in production copy
- Italic used as decoration
- Comic-Sans-adjacent humor in primary surfaces
- Variable font weight animations on headlines as a primary hook (use sparingly, on hover or once on load)
- Text-fill gradients on whole sentences (one-word gradient acceptable)
- Decorative serifs deployed for "premium feel": the premium feel comes from sans-serif at scale with editorial restraint, not from swapping in a serif
- All-caps headlines as a "powerful" device: reserve all-caps for 10 to 13px eyebrows
- Display headlines in 900-weight: reads as old-internet shouty
- Number-counter animations that overshoot and settle (must end exactly on target)
- Animated marketing copy that types itself letter-by-letter for the H1 (acceptable once for a code sample, never for the H1)
- Headline punctuation as faux-rhetorical setup ("Why so slow?"): only use questions when genuinely asking
- Headlines under 9 words that still feel padded with adjectives ("Powerful, modern, intelligent platform")
- Five fonts on one page with three weights in arbitrary roles

### Anti-AI-slop typography
The default LLM output reaches for typography that signals AI generation. Override these biases:
- Reach beyond Inter, Roboto, system-ui: pick a distinctive display face deliberately
- Vary across generations: never converge on Space Grotesk repeatedly
- Avoid 900-weight display headlines (the AI-shouty default)
- Avoid evenly-distributed weight ladders (400 / 500 / 600 / 700 / 800 in arbitrary roles): compress to 3 to 4 weights
- Reject the oversized-H1-as-its-own-justification pattern
- Reject the centered-headline-at-massive-scale default unless you genuinely chose it
- Recognize that a 4-line H1 means the container is too narrow, not that the font is too big
- Never reflexively reach for Inter when a more distinctive face would serve the brand

### Hierarchy rules
- Compress to four to six type scales
- Use weight changes more aggressively than size changes for adjacent levels
- Reserve italic for genuine emphasis or for titles
- Give an eyebrow more weight with its own size, weight or color, never with a line, dash or dot beside it
- Anchor numerals to the brand: stat moments at 96 to 144px in display weight

### Editorial column rhythm
- Body paragraphs clamp to 55 to 75 characters per line via `max-width`
- Roughly 32 to 40em for body text columns
- Outer canvas full-width
- "Magazine effect": wide canvas, narrow column
- Multiple columns rather than 100-character single-column wrap
- Long-line marketing copy is treated as a mistake

### Optical sizing
- Use display optical variant for hero moments
- Use text optical variant for body when variable fonts support `opsz`
- On non-variable faces, replace the display face entirely at the breakpoint where text-optical stops looking right
- Set `opsz` to match rendered pixel size: 20 / 24 / 40 / 48 axis values for typical icon sizes
- Display moments at hero scale use larger `opsz` values

### Tracking sub-tokens by scale
- 80px+ display: -0.02em to -0.03em
- 60 to 80px display: -0.015em to -0.02em
- 48 to 60px: -0.01em to -0.02em
- 32 to 48px: -0.01em to 0
- 24 to 32px: 0
- 16 to 24px body: 0 (default)
- 13 to 16px body: 0 (default)
- 10 to 13px eyebrow / small caps: +0.05em to +0.12em
- Brutalist micro mono: +0.05em to +0.10em (simulates mechanical typewriter spacing)

### Optical-detail tokens
- `font-smoothing: antialiased` on light-on-dark surfaces
- `text-rendering: optimizeLegibility` on prose-heavy surfaces
- Enable standard ligatures (fi, fl) on body
- Enable tabular figures via `font-variant-numeric: tabular-nums` for data tables, prices, timers, dashboards
- Use the display optical variant for hero moments and the text optical variant for body when variable fonts support `opsz`

## Checklist (severity-tagged)

- [ ] Display font is distinctive and chosen deliberately, not a default reflex (severity: High)
- [ ] H1 within the line limit in `references/surfaces/landing.md` (Hero composition) (severity: Critical)
- [ ] Body sits at 16px minimum on mobile (prevents iOS auto-zoom on input focus) (severity: Critical)
- [ ] Body line-height is 1.5 to 1.7 (severity: High)
- [ ] Display line-height is 1.0 to 1.15 (severity: High)
- [ ] Body paragraphs clamp to 55 to 75 characters per line (severity: High)
- [ ] Sentence case used for headlines (severity: Medium)
- [ ] No serifs used on dashboard or software UI surfaces (severity: High)
- [ ] At most two type families on one page (severity: Medium)
- [ ] Three to four weight steps cover the entire system (severity: Medium)
- [ ] Tracking tightens on display sizes (-0.01em to -0.03em at 48px+) (severity: Medium)
- [ ] Eyebrows use ALL CAPS or sentence case at 10 to 13px with positive tracking (severity: Cosmetic)
- [ ] ALL CAPS reserved for eyebrows only — never used for body or subheads above 14px (severity: High)
- [ ] Tabular figures enabled on data tables, dashboards, prices, timers (severity: Medium)
- [ ] Curly quotes used; no straight quotes, em dashes or double hyphens as punctuation (severity: Cosmetic)
- [ ] `font-display: swap` configured to avoid invisible text during load (severity: High)
- [ ] Variable font weight respected — reduce by ~50 units in dark mode (severity: Cosmetic)
- [ ] No more than two display fonts paired together (severity: High)
- [ ] Numbered "SECTION 01" / "CHAPTER 03" meta-labels removed (severity: High)
- [ ] No 6-line wrapped headings under any breakpoint (severity: Critical)
- [ ] Italic reserved for genuine emphasis or titles, not decoration (severity: Cosmetic)
- [ ] Type scale documented in tokens; no ad-hoc per-component sizes (severity: High)
- [ ] Optical sizing matched to rendered pixel size where variable fonts support `opsz` (severity: Cosmetic)
- [ ] Standard ligatures enabled on body; discretionary ligatures only in editorial contexts (severity: Cosmetic)
- [ ] Text-fill gradients on large headers avoided; one-word gradient acceptable (severity: High)
- [ ] No animated typewriter effects on the H1 (severity: High)
- [ ] Pull quotes set at 28 to 40px, weight 500, line-height 1.3 (severity: Cosmetic)
- [ ] Big stat numerals at 96 to 144px with sized-down unit labels (severity: Cosmetic)
- [ ] Editorial column width clamps body to 55 to 75 characters (severity: Medium)
- [ ] No 900-weight display headlines (cluster at 500 to 700) (severity: Medium)
- [ ] Display weight reduced by ~50 units in dark mode (severity: Cosmetic)
- [ ] No reflexive reach for Inter when a more distinctive face would serve the brand (severity: Medium)
- [ ] Display optical variant used for hero, text optical variant for body where variable fonts support `opsz` (severity: Cosmetic)
- [ ] Mono used for literal values (versions, regions, percentages) inside otherwise-sans copy (severity: Cosmetic)

### Sentence-case discipline
- Headlines: sentence case (only the first word and proper nouns capitalized)
- Subheads: sentence case
- Buttons: sentence case
- Nav items: sentence case
- Eyebrows: sentence case OR all-caps with positive tracking
- Title case is reserved for proper nouns and trademarked product names
- Title-Case-On-Every-Word reads as enterprise software from a previous decade

### Punctuation in typography
- Period at end of two-word headline acceptable as cadence move ("Make it.")
- Commas freely in conversational subheads
- Semicolons absent in marketing copy
- Question marks only when genuinely asking
- No exclamation marks in marketing copy
- No em dash or double hyphen for pauses and asides: a period, a comma or a colon
- Ranges in words ("3 to 5 minutes"), never an en dash
- Hyphen (-) for compound words
- Curly quotes ""; never straight quotes
- Apostrophes curly (') never straight (')
- Ellipsis character (…); never three periods

## Related

- See **color.md** for contrast pairs that govern text legibility.
- See **layout.md** for ultra-wide container widths that prevent H1 line-count failures.
- See **spacing.md** for vertical rhythm between type and surrounding sections.
- See `references/surfaces/dashboard.md` for tabular numeral discipline in data-dense surfaces.
- See **copy.md** for the words that fill the type system.
- See **accessibility.md** for dynamic-type scaling support and contrast minimums.
- See **components.md** for label, helper-text, and button typography contracts.
