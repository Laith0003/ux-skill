# Typography

> Disciplined type carries hierarchy without decoration. The scale, weight, and line-height system is what makes an interface read as composed instead of accidental.

## Principles

1. **Scale jumps are aggressive, mid-steps are removed** — Display sizes leap one to two orders of magnitude over body. There is no comfortable middle tier between body and hero. The cliff is the design; comfortable mid-sizes flatten hierarchy.

2. **Weight carries hierarchy more than size** — Use one bold or semibold for display, one regular for body, one medium for labels. Three or four weight steps cover an entire system. Five or more weights signal an undisciplined ramp.

3. **Line-height inverts with size** — Body sits at 1.5 to 1.7 for breathing room. Display tightens to 1.0 to 1.15 so headlines read as a single sculpted block. Missing this inversion is the most consistent amateur tell.

4. **Tracking tightens as type grows, loosens as it shrinks** — Display at -0.01em to -0.03em (sometimes -0.04em to -0.06em on brutalist headlines). Eyebrows and small caps at +0.05em to +0.12em. Body stays at default tracking; over-tracked body reads dated.

5. **Sentence case is the default** — Reserve title case for proper nouns and trademarked product names. ALL CAPS is reserved for eyebrows at 10 to 13px with positive tracking. Title-case headlines on every word read as enterprise from a previous decade.

6. **Line length is policed** — Body paragraphs clamp to 55 to 75 characters. Mobile floors at 35 to 60 per line. Long-line marketing copy is treated as a mistake; either break into columns or constrain measure.

7. **Numbers get the tabular treatment in data UI** — Tabular figures align decimals and prevent layout shift on count-up. Reserve proportional figures for prose. Mixed proportional and tabular on the same page reads as undisciplined.

8. **No serifs on dashboards or software UIs** — Serifs belong to editorial, marketing, and luxury contexts. A dashboard with serif headlines reads as a category error. Reserve serifs for surgical editorial moments inside otherwise-sans pages.

9. **Pair two typefaces at most** — A display face plus a body face, or a sans plus a mono. Three faces only when a clear hierarchy demands it (sans, serif, mono for editorial-tech hybrids). Two display fonts together is banned.

10. **Optical contrast matters more than face novelty** — A well-cut neo-grotesque used across an entire system beats a flashy display face deployed once. Restraint in face selection magnifies the moves you do make.

## Do / Don't

| Do | Don't |
|---|---|
| Use a single workhorse sans-serif at varying weights for most surfaces | Mix five fonts across one page |
| Set body at 16 to 18px with line-height 1.5 to 1.7 | Set body below 12px or above 22px on web |
| Tighten tracking to -0.02em on display sizes 48px and above | Use the same tracking on display and body |
| Use sentence case for headlines | Use Title Case On Every Word |
| Compress display line-height to 1.0 to 1.15 | Run display headlines at body line-height (looks like a stack) |
| Use tabular figures in tables, dashboards, prices, timers | Use proportional figures for vertically aligned numeric columns |
| Cap H1 at 2 to 3 lines maximum | Allow H1 to wrap to 4+ lines (catastrophic at 6) |
| Pair sans with a mono for technical contexts | Pair two display faces together |
| Use weight changes (400 to 600) to signal hierarchy | Use color alone to signal hierarchy |
| Use ALL CAPS only for eyebrows at 10 to 13px with +0.06em tracking | Use ALL CAPS for body or subheads at any size |
| Standardize on one type ramp with four to six steps | Invent new sizes per component |
| Enable curly quotes and em dashes in production copy | Ship straight quotes and double-hyphens |
| Reserve italic for genuine emphasis or titles | Use italic as decoration |
| Match optical size to rendered pixel size when the face supports it | Use a single optical variant across display and body |
| Wire `font-display: swap` so text remains visible during font load | Allow invisible text (FOIT) during font load |

## Examples

### Pattern: Display headline at hero scale
**Use when**: Hero or section opener carrying the page's primary claim.
**Anti-pattern**: 6-line wrapped headline crammed inside a narrow container, or a hero headline at 24px hoping weight will carry it.
**How**: Set the H1 in an ultra-wide container (`max-w-5xl` or wider). Size with clamp: `clamp(3rem, 5vw, 5.5rem)` so the line lands on conceptual beats, not on whitespace. Compress line-height to 1.0 to 1.15. Tighten tracking to -0.02em. Cap at 2 to 3 lines; if it overflows, widen the container before shrinking the font.

### Pattern: Editorial body with measured column
**Use when**: Long-form marketing prose, documentation body, or any reading-intensive surface.
**Anti-pattern**: Body text running 100+ characters per line across a wide viewport.
**How**: Size body at 16 to 18px, regular weight, line-height 1.55 to 1.7. Clamp paragraph width to `max-w-[65ch]` or roughly 32 to 40em. On wide viewports, the canvas stays wide; the column stays narrow. This is the magazine effect.

### Pattern: Eyebrow + headline
**Use when**: Sectioning a long page without numbered chapters or decorative dividers.
**Anti-pattern**: Naming sections as "SECTION 01" / "ABOUT US" / "OUR PROCESS 02" — these are amateur-tier signposting and banned.
**How**: A short label sits above the headline at 10 to 13px, weight 500 to 600, tracking +0.06em to +0.10em, in muted neutral or a paired accent. Sentence case or uppercase both work; pick one and apply consistently. Often paired with a 6 to 8px colored dot or geometric mark to the left.

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
**Use when**: Marketing landing pages, premium SaaS surfaces, editorial sites.
**Anti-pattern**: A 12-step type scale with sizes at 12, 13, 14, 15, 16, 17, 18, 20, 22, 24, 28, 32px.
**How**: Define four to six scales: hero display, section heading, subhead, body, small, eyebrow. Each scale gets one size, one weight, one line-height. No fifth scale snuck in for a sidebar. The system is the constraint, and the constraint is the look.

### Pattern: Dark-mode weight compensation
**Use when**: Building a dark variant of the same typography system.
**Anti-pattern**: Reusing the same weight on light and dark and watching dark mode read as too thick.
**How**: Reduce font weight by roughly 50 units when going from light to dark for the same size (e.g., 600 in light becomes 550 in dark). This compensates for the apparent thickening of light type on dark background. Line-height stays the same across modes. Letter-spacing can loosen by 1 to 2% on body in dark mode.

### Pattern: Numerical specificity as typographic ornament
**Use when**: Premium B2B and editorial surfaces where the persuasion is numerical.
**Anti-pattern**: "Big Stat" pattern with glowing 96pt numerals where the number is the only design move.
**How**: Concrete numbers (latency in ms, accuracy percentages, yield rates, fee figures) appear set at the same scale as the surrounding text but carry visual weight purely from their precision. The precision itself is the rhetoric. "75ms" inline at body scale persuades more than "Blazingly fast" at 96pt.

### Pattern: Long-form prose under a hero
**Use when**: AI, fintech, or research-led products where the company has something to say.
**Anti-pattern**: A trimmed-down tagline as the only body copy under an oversized hero.
**How**: Several premium surfaces allow paragraph-length body copy under the hero subhead — three or four sentences of substantive prose rather than a single tagline. Body sits at 15 to 17px, line-height 1.55 to 1.7. The willingness to use full sentences signals that the company has something to say.

### Pattern: Pull-quote treatment for testimonials
**Use when**: Customer testimonials in marketing surfaces.
**Anti-pattern**: Pull quote at body size with quote marks, no visual differentiation from surrounding paragraphs.
**How**: Pull quote sits at 28 to 40px, weight 500, line-height 1.3. Attribution beneath drops to body size with reduced contrast. The quote does not start with a quotation mark — instead, an oversized opening quote mark sits as a graphic element to the left or above. Set the quote at slightly larger size than body, regular weight, with the speaker's name and role beneath. No oversized quotation marks around the quote, no decorative card chrome, no logo overlay on the photograph.

### Pattern: Variable font weight animation
**Use when**: Premium SaaS surfaces where craftsmanship is part of the value proposition.
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
**Use when**: Industrial, technical, anti-mainstream products.
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
**Anti-pattern**: "SECTION 01," "QUESTION 05" — banned amateur-tier signposting.
**How**: Numbers and section markers in monospace, used like editorial folios. Small, tracked, set in a muted neutral. They function as orientation markers, not as decoration. The number itself is the marker; no surrounding meta-label.

## Tokens / values

### Scale (web, desktop default)
- Hero display: 48 to 96px (push to 64 to 96px or higher with clamp); brutalist headlines bleed to 120 to 240px with `clamp(4rem, 10vw, 15rem)`
- Section heading (H2): 32 to 48px
- Subhead (H3): 20 to 24px
- Large body / lead: 18 to 22px
- Body: 16 to 18px
- Small / caption: 13 to 14px
- Eyebrow / small caps: 10 to 13px
- Code inline / shortcut chips: 13 to 14px

### Mobile floors
- Body: 16px minimum (prevents iOS auto-zoom on input focus)
- Hero display: 36 to 48px minimum; never below 36px

### Weight
- Display: 600 to 800 (premium SaaS sits at 500 to 700; weight 900 reads as shouty)
- Subhead / UI label: 500 to 600
- Body: 400 to 450
- Caption / metadata / disabled: 400, sometimes paired with reduced opacity
- Reduce by ~50 units in dark mode for matching perceived weight

### Line-height
- Display (48px+): 1.0 to 1.15
- Section heading: 1.15 to 1.3
- Subhead: 1.3 to 1.4
- Body: 1.5 to 1.7
- Small / caption: 1.3 to 1.4
- Brutalist display: 0.85 to 0.95 (intentionally cramped)

### Tracking (letter-spacing)
- Display at 80px+: -0.02em to -0.03em
- Display at 48 to 80px: -0.01em to -0.02em
- Section heading: -0.01em to 0
- Body: 0 (default)
- Small / caption: 0 to +0.01em
- Eyebrow / small caps: +0.05em to +0.12em
- Brutalist macro display: -0.03em to -0.06em
- Brutalist mono micro: +0.05em to +0.10em

### Line length (measure)
- Mobile: 35 to 60 characters
- Desktop body: 55 to 75 characters
- Magazine-effect body: 60 to 65 characters (32 to 40em max-width)
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

### Font pairings — by mood

**Elegant / luxury:**
- Playfair Display + Source Sans 3 — serif heading + clean sans body; editorial, fashion, premium brands
- Cormorant + Inter — display serif + neutral sans; hospitality, beauty
- Libre Caslon Display + Libre Franklin — classic editorial pairing; media, longform
- Italiana + Inter — thin elegant serif + utilitarian sans; fashion, lookbook
- Bodoni Moda + Inter — sharp contrast serif + clean sans; luxury fashion
- Cardo + Roboto — refined book serif + standard sans; academic luxury
- EB Garamond + Inter — humanist serif + sans; editorial, longform

**Playful / friendly:**
- Fraunces + Inter — quirky display serif + clean sans; creative SaaS, lifestyle
- DM Serif Display + DM Sans — family pairing, modern playful; startups, consumer
- Caveat + Inter — handwritten + sans; education, kids
- Lobster + Open Sans — script + clean sans; food and beverage, casual brands
- Pacifico + Open Sans — brush script + sans; lifestyle, leisure
- Quicksand + Quicksand — rounded sans across hierarchy; kids, wellness
- Comic Neue + Open Sans — friendly + neutral; education, kids (sparingly)

**Professional / trust:**
- Inter + Inter — single-family pairing, modern standard; tech, SaaS
- IBM Plex Sans + IBM Plex Mono — sans + mono for tech credibility; dev tools, fintech
- Roboto + Roboto Mono — Material-aligned; Android-first products
- Source Sans 3 + Source Code Pro — open-source family; government, healthcare
- Work Sans + Work Sans — single neutral family; B2B, agency
- Manrope + Manrope — modern geometric sans; tech
- Public Sans + Public Sans — government-aligned; civic tech

**Modern / tech:**
- Geist + Geist Mono — modern minimal; dev tools, AI products
- Satoshi + JetBrains Mono — geometric + dev mono; modern startups
- Plus Jakarta Sans + Inter — modern + standard; fintech, SaaS
- Onest + Inter — new geometric + standard; modern web
- General Sans + JetBrains Mono — versatile + mono; tech
- Hanken Grotesk + Inter — grotesque + neutral; editorial tech
- Outfit + Inter — rounded geometric + sans; modern consumer

**Brutalist / editorial:**
- Space Grotesk + IBM Plex Mono — geometric quirky + mono; indie tech, brutalism
- Archivo Black + Inter — heavy display + clean body; music, editorial
- Anton + Open Sans — condensed display + sans; sports, news
- Bebas Neue + Roboto — all-caps condensed + sans; cinema, sports
- Druk + Inter — bold display + standard; brutalism, editorial
- Monument Grotesk + Inter — neo-grotesque + standard; indie, design
- NB International + IBM Plex Mono — tech-brutal pairing; crypto, web3

**Display / statement:**
- Big Caslon + Inter — massive display serif + sans; luxury announcement
- Recoleta + Inter — friendly contemporary serif + sans; health, wellness
- Migra + Inter — quirky display + sans; creative brands
- PP Editorial New + Inter — modern serif + sans; editorial
- PP Neue Montreal + Inter — sharp grotesque + sans; modern luxury
- Tobias + Inter — refined display serif + sans; editorial luxury

**Mono / technical:**
- JetBrains Mono — dev-focused mono; code blocks
- Fira Code — mono with ligatures; dev tools
- IBM Plex Mono — corporate mono; fintech, enterprise
- Geist Mono — modern mono; AI products, modern dev tools
- Berkeley Mono — premium mono; creative tech
- Commit Mono — compact mono; terminal apps

Pick one mono and apply across code blocks, shortcut chips, metadata, and inline values.

### Banned typographic patterns
- Arial, Roboto, generic system stacks as primary display faces
- Serifs on dashboards or software UIs
- Inter used as the only reflex (acceptable as a body face but vary across projects; do not default to it)
- Mixing two display faces together
- Title case on every word of every headline
- ALL CAPS body or subheads
- Oversized H1s that scream from scale alone (use weight and color for hierarchy)
- 6-line wrapped headings
- Decorative ligatures on body copy (standard ligatures are fine; discretionary ligatures are editorial-only)
- Straight quotes and double-hyphens in production copy
- Italic used as decoration
- Comic-Sans-adjacent humor in primary surfaces
- Variable font weight animations on headlines as a primary hook (use sparingly, on hover or once on load)
- Text-fill gradients on whole sentences (one-word gradient acceptable)
- Decorative serifs deployed for "premium feel" — the premium feel comes from sans-serif at scale with editorial restraint, not from swapping in a serif
- All-caps headlines as a "powerful" device — reserve all-caps for 10 to 13px eyebrows
- Display headlines in 900-weight — reads as old-internet shouty; cluster at 500 to 700
- Number-counter animations that overshoot and settle (must end exactly on target)
- Animated marketing copy that types itself letter-by-letter for the H1 (acceptable once for a code sample, never for the H1)
- Headline punctuation as faux-rhetorical setup ("Why so slow?") — only use questions when genuinely asking
- Headlines under 9 words that still feel padded with adjectives ("Powerful, modern, intelligent platform")
- Five fonts on one page with three weights in arbitrary roles

### Anti-AI-slop typography
The default LLM output reaches for typography that signals AI generation. Override these biases:
- Reach beyond Inter, Roboto, system-ui — pick a distinctive display face deliberately
- Vary across generations — never converge on Space Grotesk repeatedly; no two outputs reach for the same stack reflexively
- Avoid 900-weight display headlines (the AI-shouty default)
- Avoid evenly-distributed weight ladders (400 / 500 / 600 / 700 / 800 in arbitrary roles) — compress to 3 to 4 weights
- Reject the oversized-H1-as-its-own-justification pattern; control hierarchy with weight and color
- Reject the centered-headline-at-massive-scale default unless you genuinely chose it
- Recognize that a 4-line H1 means the container is too narrow, not that the font is too big
- Never reflexively reach for Inter when a more distinctive face would serve the brand

### Hierarchy rules
- Compress to four to six type scales; no fifth scale snuck in
- Use weight changes more aggressively than size changes for adjacent levels
- Reserve italic for genuine emphasis or for titles
- Use a 6 to 8px colored dot or geometric mark before eyebrows when more visual weight is needed
- Anchor numerals to the brand: stat moments at 96 to 144px in display weight; unit labels at 40 to 60% of the numeral size

### Editorial column rhythm
- Body paragraphs clamp to 55 to 75 characters per line via `max-width`
- Roughly 32 to 40em for body text columns
- Outer canvas full-width; text column narrow
- "Magazine effect" — wide canvas, narrow column
- Multiple columns rather than 100-character single-column wrap
- Long-line marketing copy is treated as a mistake; break into columns

### Optical sizing
- Use display optical variant for hero moments
- Use text optical variant for body when variable fonts support `opsz`
- On non-variable faces, replace the display face entirely at the breakpoint where text-optical stops looking right
- Set `opsz` to match rendered pixel size: 20 / 24 / 40 / 48 axis values for typical icon sizes
- Display moments at hero scale use larger `opsz` values; body uses smaller

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
- Enable standard ligatures (fi, fl) on body; reserve discretionary ligatures (ct, st, sp) for editorial moments
- Enable tabular figures via `font-variant-numeric: tabular-nums` for data tables, prices, timers, dashboards
- Use the display optical variant for hero moments and the text optical variant for body when variable fonts support `opsz`

## Checklist (severity-tagged)

- [ ] Display font is distinctive and chosen deliberately, not a default reflex (severity: High)
- [ ] H1 never exceeds 2 to 3 lines at any breakpoint from 375px to 1440px (severity: Critical)
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
- [ ] Curly quotes and em dashes used; no straight quotes or double-hyphens (severity: Cosmetic)
- [ ] `font-display: swap` configured to avoid invisible text during load (severity: High)
- [ ] Variable font weight respected — reduce by ~50 units in dark mode (severity: Cosmetic)
- [ ] No more than two display fonts paired together (severity: High)
- [ ] Numbered "SECTION 01" / "QUESTION 05" meta-labels removed (severity: High)
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
- Em dash (—) for pauses and asides; no spaces around it
- En dash (–) for ranges ("3–5 minutes")
- Hyphen (-) for compound words
- Curly quotes ""; never straight quotes
- Apostrophes curly (') never straight (')
- Ellipsis character (…); never three periods

## Related

- See **color.md** for contrast pairs that govern text legibility.
- See **layout.md** for ultra-wide container widths that prevent H1 line-count failures.
- See **spacing.md** for vertical rhythm between type and surrounding sections.
- See **dashboards.md** for tabular numeral discipline in data-dense surfaces.
- See **copy.md** for the words that fill the type system.
- See **accessibility.md** for dynamic-type scaling support and contrast minimums.
- See **components.md** for label, helper-text, and button typography contracts.
