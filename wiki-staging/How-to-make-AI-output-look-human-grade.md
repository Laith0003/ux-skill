# How to Make AI Output Look Human-Grade

The difference between AI-generated and human-grade output is constraint and specificity. Discovery + anti-slop discipline + arsenal patterns + SEO foundation transform generic AI output into work that looks shipped, not generated. Here's the full pipeline.

This is the master walkthrough. Every command in the plugin contributes to one of the five stages. Run them in order and the output stops looking like AI.

---

## Why "looks like AI" is the rejection signal

When a screen looks AI-generated, the user does not think "this is AI." They think "this is generic," "this is template-y," "this is unfinished." The conscious read is taste; the unconscious read is fingerprint detection.

Three things produce the "looks like AI" perception:

1. **Default everything.** Default fonts, default colors, default layouts, default copy. Each is acceptable in isolation. Together they form a recognizable surface.

2. **No constraint.** A real designer says "no" 100 times before saying "yes." A model with no constraint says "yes" to everything — every feature on the screen, every gradient, every card with a shadow.

3. **No specificity.** Real products are specific to a user, a market, a moment. AI defaults are specific to nothing.

Human-grade output rejects defaults, applies constraint, and adds specificity. The pipeline below does each in order.

---

## Stage 1: The discovery protocol (10 questions before any code)

Discovery is the constraint stage. It refuses to generate anything until enough is known about the work.

The `/ux-discovery` command runs 10 questions. Every other command in the plugin runs discovery first unless you pass `--quick`.

The 10 questions:

### Q1. What is being built?

A landing page? A dashboard? A case study? A pricing page? A docs site? A product surface inside an app? The output structure changes completely based on the answer.

### Q2. Who is the audience?

A real audience. Not "everyone," not "users." Be specific: "Pharmacy operations managers at independent pharmacies in Jordan." "Senior frontend engineers at series-A startups." "VCs scouting MENA fintech."

The audience defines vocabulary, tone, density, references.

### Q3. What is the brand?

The brand identity. Existing tokens (`tokens.css`), existing voice samples, existing logo, existing references. If the brand exists, the output respects it. If the brand does not exist, the next question takes priority.

### Q4. What is the wow moment?

The single screen, motion, or interaction that users will remember. Without a wow moment, the output is uniformly competent and uniformly forgettable.

Examples of wow moments:

- A live counter that ticks up in real time on the hero
- A scroll-coupled video that frames the product narrative
- A magnetic hover on the primary CTA with a one-frame settle
- A bento dashboard where one cell pulses softly to show live data
- A case-study cover that types itself in over 1.2s

Pick one. Just one. The rest of the surface is restrained so the wow moment lands.

### Q5. What are the references?

Three references, minimum. Real URLs. Specific. "claude.com" is a reference; "modern SaaS landing pages" is not.

Strong reference sets pair contrasting examples:

- A monochrome editorial site + a high-energy product launch + a dense ops dashboard

The references set the bar. The output must reach it.

### Q6. What is the through-line?

The user-provided narrative thread. What is the page trying to say in one sentence? Without a through-line, the surface is a collection of sections with no argument.

For Dot: "Beyond likes. Beyond clicks. The internet of what people actually do."

That sentence shapes every choice downstream.

### Q7. What is the wow moment to avoid?

The trap. The pattern the audience has seen too often. For a fintech landing: no purple-to-blue gradient hero, no testimonial carousel, no "Trusted by [10 logos]" band.

Naming the trap explicitly is how the model avoids it.

### Q8. What are the constraints?

- Frontend stack? (Blade + Alpine? React + Tailwind? Plain HTML?)
- Browser support? (Evergreen only? IE11? Mobile-first?)
- RTL required?
- Locale list?
- Performance budget? (LCP under 2s? INP under 200ms?)
- Accessibility target? (WCAG AA? AAA?)
- File-size budget? (Hero under 200KB? Page under 1MB?)

Each constraint kills a class of defaults.

### Q9. What is the success metric?

How do you know if this worked? Conversion lift? Time-on-page? Demo bookings? Brand recall? Without a metric, every choice is taste-based. With a metric, choices are testable.

### Q10. What is out of scope?

What you are NOT building. Backend? Auth? Internationalization? Mobile app? Email templates? Listing this prevents scope creep mid-generation.

---

## Constraint as the source of taste

Every taste call is a "no." Saying yes to everything produces AI default output. Saying no produces tase.

Examples of taste-as-constraint:

- "No gradients." → forces solid colors, forces semantic palette
- "No more than 3 type sizes per surface." → forces hierarchy by weight, color, and space
- "No card unless it groups multiple fields." → forces flat layout, forces hairline separators
- "No emoji." → forces inline SVG with intent
- "No more than 2 live indicators per viewport." → forces a hierarchy of urgency
- "No banned animation properties (width, height, top, left, margin, padding)." → forces compositor-only motion
- "No round-number invented stats." → forces real data or no number

These constraints are the discipline encoded in the plugin commands. Together they reject 80% of the AI default surface.

You can also add constraints per project. A pricing page might add "no discount-percentage stickers." A landing page for a security product might add "no padlock icon." The more specific the constraints, the more specific the output.

---

## Stage 2: The anti-slop discipline

After discovery, run `/ux-polish` on the generated output (or on existing surfaces you want to harden). The command is the codified anti-slop checklist from [How to detect AI slop in your design](How-to-detect-AI-slop-in-your-design).

The anti-slop discipline is two parts: a list of bans and a positive checklist.

### Bans

These are unconditional. Any presence is a violation.

- Inter as the display font on a brand surface
- Purple-to-blue or pink-to-purple gradients
- "John Doe" / "Acme Inc" / lorem ipsum
- Round-number invented stats ("10x faster", "47% growth")
- Filler verbs ("streamline," "unlock," "supercharge")
- Decorative emoji
- Three equal feature cards in a row
- Icon-circle top-left of every feature card
- Chevron arrow on every CTA
- Shadow + border + background-tint combined on a single card
- Banned motion properties (width, height, top, left, margin, padding)
- `outline: none` without a `:focus-visible` replacement
- Missing empty / loading / error states

### Positive checklist

These must be present.

- Type uses negative tracking on headlines 30px+
- Body line length 50–75ch (30–45ch for hero)
- State palette is solid (no gradients on state)
- Live indicators capped at 2 per viewport
- Tabular numerals on every number in a column
- WCAG AA contrast on text
- Empty / loading / error states for every dynamic region
- Focus-visible ring on every interactive
- Reduced-motion handler
- RTL works (test by setting `dir="rtl"`)
- Cards use hairline borders OR shadows, not both

Run the audit. Fix critical and high. Ship.

---

## Stage 3: The arsenal (60+ high-end patterns)

The arsenal is the library of high-leverage patterns the plugin pulls from. These are patterns that human designers reach for to differentiate work from defaults.

### Layout arsenal

- Bento 2.0 (asymmetric grid with one anchor)
- Magazine spread (large hero image + offset copy)
- Split-screen with editorial hierarchy
- Sticky side-rail with scroll-coupled state
- Marquee sections (auto-scroll, pause on hover, reduced-motion-aware)
- Off-axis hero (copy offset from center, image extends out of frame)
- Hairline grid (1px borders define structure, no boxes)
- Number-led sections (large oversized stat as the anchor)
- Long-form "manual" layout (numbered sections, editorial type)

### Type arsenal

- Two-tone body emphasis (solid black for key phrases, gray for context)
- Editorial display + humanist body + tabular mono trio
- Negative tracking on headlines, positive on small caps
- Hanging quotes and pull-quote variants
- Variable-axis font tuning (weight, optical size, slant)
- Drop-cap openers
- Marquee headlines (oversized type that runs past container)

### Color arsenal

- Pure monochrome with a single chromatic accent
- Brand-color reserved for one surface (CTA only, or logo only)
- State palette tuned to brand hue (not default emerald/red)
- Dark mode as a separate design (not an inversion)
- Soft warm-neutral as the canvas (off-white, not pure white)
- Hairline borders in low-saturation cool gray
- Selection color tuned to brand

### Motion arsenal

- Magnetic micro-physics on the primary CTA
- Scroll-coupled progress on long-form pages
- Stagger reveal on first paint (30–50ms per child)
- Live pulse (capped 2 per viewport)
- Number counter (count up on first paint, 600ms decelerate)
- Page-level transition (250–400ms decelerate)
- Sparkline draw on data update
- Hover-to-reveal actions on table rows
- Spring-physics drawer pulls
- Reduced-motion-aware everywhere

### Component arsenal

- Hairline-bordered cards (1px, no shadow)
- Hero CTA: solid black on white, no gradient, no chevron
- Quiet primary action + loud destructive confirmation
- Live data pill (status dot + value + timestamp)
- Sparkline-inline metrics (data IN the cell, not next to it)
- Empty states with a primary action, not just an illustration
- Error states that name the failure AND the next action
- Loading states that match the final element's shape (skeleton)
- Confirmation dialogs with a 5-word title and a 2-button choice

### Interaction arsenal

- Command-K palette (quick action search)
- Slash filters in dense tables
- Keyboard navigation (arrow keys for rows, j/k for vim users)
- Sticky filter chips above tables
- Hover-revealed row actions
- Click-and-drag selection
- Toast notifications (top-right, auto-dismiss, max 3 stacked)
- Floating action button (mobile only, single primary action)

### Editorial arsenal

- Numbered (A)–(G) sections in long-form
- Hairline separators between numbered sections (no cards)
- Pull-quote variant for key claims
- Sidebar callouts for tangential info
- Footnote-style references for citations
- TOC with active-section highlighting

The arsenal expands per command. `/ux-dashboard` pulls from dashboard arsenal. `/ux-case-study` pulls from editorial. `/ux-landing` pulls from layout + motion + color.

Each pattern is opinionated. Each rejects an AI default.

---

## Stage 4: The 3 dials (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY)

The dials let you tune the output without rewriting the prompt. Each dial has three settings.

### DESIGN_VARIANCE

Controls how far from the brand baseline the design ranges.

- `LOW` — sticks to the brand baseline. Use for products with strong existing identity (Dot's monochrome system).
- `MEDIUM` — explores adjacent territory. Use for new features in an existing product.
- `HIGH` — explores unexpected territory. Use for a launch moment that needs to be distinctive.

Higher variance increases the risk of off-brand output. Lower variance increases the risk of generic output.

### MOTION_INTENSITY

Controls how much motion is in the output.

- `LOW` — micro interactions only. Hover, focus, page-transition. No scroll-coupled motion. No magnetic effects.
- `MEDIUM` — adds stagger reveal on first paint, one magnetic CTA, scroll-coupled progress.
- `HIGH` — adds scroll-coupled video, parallax (pointer-only), section pinning, multiple magnetic elements.

For dashboards: LOW always. For landings: MEDIUM. For one-off launch pages: HIGH if and only if the audience expects spectacle.

### VISUAL_DENSITY

Controls how much information is on the screen.

- `LOW` — editorial. Lots of negative space. Slow vertical rhythm. Few elements per viewport.
- `MEDIUM` — standard product surface. Balanced.
- `HIGH` — operator dashboard or data-dense table. Tight rhythm. Many elements per viewport.

For an executive dashboard: LOW. For a marketing landing: MEDIUM. For a payments ops console: HIGH.

### Setting the dials

In the discovery, the questions implicitly set the dials. You can also override explicitly:

```
/ux-landing --variance HIGH --motion MEDIUM --density LOW
```

The output respects the dials.

---

## Stage 5: Brand identity input (asking for it before generating)

The plugin will not generate without a brand identity. If no brand exists, the discovery prompts for one.

The minimum brand input:

### A name and a one-line description

"Dot — beyond likes, beyond clicks. The internet of what people actually do."

### A type stack

- Display font: PP Editorial New
- Body font: Roboto Flex
- Mono font: JetBrains Mono

If no fonts chosen, the plugin proposes 3 candidate stacks tuned to the audience and lets you pick one.

### A palette

- Canvas: `#FAFAF7` (warm off-white)
- Ink: `#0E0E0E` (near-black, never pure black)
- Brand accent: a single hue, used sparingly
- State palette: success / warning / danger / info, tuned to brand

If no palette chosen, the plugin proposes 3 candidates and lets you pick one.

### A voice sample

A paragraph of existing brand voice. If none exists, the plugin proposes 3 voice candidates (warm/direct/literary, sharp/technical/precise, calm/editorial/literary).

### A reference set

Three URLs minimum.

Once the brand identity exists, every command in the plugin respects it. Tokens are referenced from `tokens.css`. Voice is checked against the sample. Layouts honor the density.

---

## References as the bar (claude.com-style, awwwards-style)

References serve a single function: they set the quality bar.

The plugin asks for three references. Each reference is interpreted to extract:

- Type hierarchy patterns
- Color and palette discipline
- Layout patterns
- Motion patterns
- Density choices
- Editorial decisions

The output then aims at the bar set by the references. Without references, the bar is the AI default.

Strong reference combinations:

### For a landing page

- A current-best product launch (sets layout + motion bar)
- An editorial publication (sets type bar)
- A dense product surface in the same category (sets information-density bar)

### For a dashboard

- A live ops console (sets density + state-color bar)
- A trading interface (sets numeral + sparkline bar)
- An editorial product page (sets restraint bar)

### For a case study

- A magazine feature (sets editorial bar)
- A studio case study (sets section-organization bar)
- A peer's published case study (sets the comparative bar)

You can also negative-reference: "Do NOT look like [URL]." This is high-leverage when the audience has seen the trap pattern too often.

---

## The wow moment (the user-provided through-line)

The wow moment was set in discovery Q4. It is the one screen or interaction that users will remember.

The plugin treats the wow moment as a budget. The rest of the surface is restrained so the wow moment can land. If everything is loud, nothing is.

Examples:

### Wow: live counter ticking up on the hero

- Hero is otherwise quiet: solid type, solid color, no other motion
- The counter is the focal point: oversized tabular numerals, smooth count-up on first paint, then live ticks every 5s
- Below the hero: standard restraint

### Wow: scroll-coupled video

- Above the fold: simple type, no decoration
- The video is the second viewport: pinned, scroll-coupled, no other motion competing
- After the video: standard restraint

### Wow: magnetic CTA with one-frame settle

- The CTA sits in a clean field of negative space
- On hover, the magnetic pull is restrained (0.3 multiplier, see motion patterns)
- The settle is a single overshoot frame
- No other magnetic elements on the page

The plugin enforces the budget. If you have a wow on the hero, the feature section is quiet. If the wow is in the feature section, the hero is quiet. Never two wows competing.

---

## SEO baked in (the head surface, OG, Twitter, JSON-LD)

A human-grade landing page does not stop at visual design. The metadata is part of the surface. Search and social previews are the first impression for users who never visit the page.

`/ux-seo` generates the metadata block alongside any landing or case study output. It produces:

### The `<head>` block

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Beyond likes. Beyond clicks. — Dot</title>
  <meta name="description" content="The internet of what people actually do. A loyalty platform that rewards real behavior across the MENA market." />

  <link rel="canonical" href="https://thedotwallet.com/" />
  <link rel="alternate" hreflang="en" href="https://thedotwallet.com/" />
  <link rel="alternate" hreflang="ar" href="https://thedotwallet.com/ar" />
  <link rel="alternate" hreflang="x-default" href="https://thedotwallet.com/" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="Beyond likes. Beyond clicks. — Dot" />
  <meta property="og:description" content="The internet of what people actually do." />
  <meta property="og:image" content="https://thedotwallet.com/og.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="og:url" content="https://thedotwallet.com/" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:locale:alternate" content="ar_JO" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Beyond likes. Beyond clicks. — Dot" />
  <meta name="twitter:description" content="The internet of what people actually do." />
  <meta name="twitter:image" content="https://thedotwallet.com/og.jpg" />

  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "Dot",
    "url": "https://thedotwallet.com/",
    "logo": "https://thedotwallet.com/logo.svg",
    "sameAs": []
  }
  </script>
</head>
```

### Why each piece matters

- **`<title>`** — the primary SEO surface. 50–60 characters. Includes the brand and the through-line.
- **`<meta description>`** — the snippet under the title in search results. 150–160 characters. Should be a complete sentence.
- **`canonical`** — prevents duplicate-content penalties when the page is reachable at multiple URLs.
- **`hreflang`** — tells search engines which language version to show. Critical for MENA products with Arabic + English.
- **OG (Open Graph)** — controls the preview when the page is shared on Facebook, LinkedIn, iMessage, Slack, etc.
- **Twitter Card** — controls the preview on Twitter / X.
- **JSON-LD** — structured data for search. Tells Google what kind of entity this is (Organization, Product, Article, etc.).

### The OG image

The OG image is the single most-shared visual representation of your product. The plugin generates one alongside the landing page:

- 1200x630 pixels
- The display headline rendered in the brand display font
- The brand mark in the corner
- Solid background, no gradient, no decoration
- Compressed under 200KB

A custom OG image converts 3–10x better than the default page-screenshot OG. Do not skip it.

### Sitemap and robots

The plugin also generates:

- `sitemap.xml` (list of all canonical URLs)
- `robots.txt` (allow / disallow rules)

For a multilingual site, the sitemap includes `xhtml:link` annotations for each language alternate.

---

## A real before / after walkthrough

A landing page for a fictional product, "Quill — invoicing for solo designers."

### Stage 0: AI default output (no plugin)

```
Hero:
- Headline: "Streamline your invoicing workflow"
- Subhead: "Quill helps designers invoice clients faster and get paid on time."
- CTA: "Get started →" with from-purple-600 to-blue-600 gradient
- Centered hero, single CTA below, gradient blob behind

Features section:
- "10x faster invoicing" | "Trusted by 5,000+ designers" | "Get paid 3 days sooner"
- Three equal cards, each with a Lucide icon in a colored circle

Testimonial:
- "Quill is the best invoicing tool I've ever used." — John Doe, Designer at Acme Inc

Footer:
- Standard 4-column grid, weight 600 body, Inter throughout
```

Slop score: 92/100. Looks like every AI landing on Twitter.

### Stage 1: Discovery

Q1. Landing page.
Q2. Solo designers (freelancers, not agencies) charging $5K-$50K projects.
Q3. Brand exists: monochrome with a single warm-orange accent on actions. Display: PP Editorial New. Body: Söhne. Voice: warm, direct, brief.
Q4. Wow moment: a live counter on the hero showing the total invoiced through Quill in the last 30 days, ticking up in real time.
Q5. References: stripe.com, linear.app, lattice.com.
Q6. Through-line: "Send the invoice. Get the money."
Q7. Avoid: testimonial carousels, gradient hero, "10x" claims, trusted-by logo strip.
Q8. Stack: Next.js + Tailwind. Mobile-first. WCAG AA. LCP under 2s.
Q9. Success: paid signups from solo designers.
Q10. Out of scope: in-app product surface (separate from landing).

### Stage 2: Constraints applied

- No gradients on hero or CTA (Q7 implicit)
- No testimonial carousel (Q7)
- No "10x" or "trusted by" stats (Q7)
- No Inter (brand uses PP Editorial New + Söhne)
- One wow moment: the live counter (Q4)
- The rest of the surface is restrained
- RTL not required for v1 (Q2 implies English-only)

### Stage 3: Arsenal applied

- Layout: off-axis hero (copy offset left, live counter offset right). No center alignment.
- Type: PP Editorial New 72px display with -0.04em tracking. Söhne 16px body.
- Color: warm canvas (#FAFAF7), near-black ink (#0E0E0E), warm-orange accent (#E5613A) reserved for the CTA only.
- Motion: live counter ticks up on first paint over 800ms, then live increments every 5s. Hero copy fades in over 300ms. CTA has magnetic micro-hover (0.3 multiplier).
- Components: hairline-bordered cards (1px, no shadow). CTA: solid black on warm-canvas, no gradient, no chevron, single label "Start invoicing."

### Stage 4: Dials

- DESIGN_VARIANCE: LOW (existing brand)
- MOTION_INTENSITY: MEDIUM (one magnetic CTA, the live counter)
- VISUAL_DENSITY: LOW (editorial restraint)

### Stage 5: Generated output

```
Hero:
- Headline (PP Editorial New 72px, -0.04em tracking, ink):
  "Send the invoice. Get the money."
- Subhead (Söhne 18px, gray-700):
  "Quill is invoicing for solo designers who'd rather be designing."
- CTA (solid black on warm canvas, magnetic micro-hover):
  "Start invoicing"
- Live counter (Söhne tabular nums, 48px):
  "$2,847,392 invoiced through Quill in the last 30 days"
- Off-axis layout: copy left, counter right, no center alignment

Below the fold:
- Section 1: "What it does." (one feature, one anchor metric, hairline separator)
- Section 2: "What it doesn't do." (the restraint statement — sets it apart)
- Section 3: "What customers say." (one real quote from a real beta customer, attributed correctly)
- Section 4: "How much." ($12/mo, single tier, no annual-discount theater)

Footer:
- Single line, left aligned: "Quill, made by Layla Aljunaidy. quill.so/manifesto."
```

Slop score: 8/100. Looks like a shipped indie product.

### Metadata

```html
<title>Quill — Invoicing for solo designers</title>
<meta name="description" content="Send the invoice. Get the money. Quill is invoicing for solo designers who'd rather be designing." />
<meta property="og:image" content="https://quill.so/og.jpg" />
```

OG image: a single quote ("Send the invoice. Get the money.") rendered in PP Editorial New on the warm canvas with the Quill mark in the corner. Solid background. Sub-200KB.

### Final pipeline command

```
/ux-landing --variance LOW --motion MEDIUM --density LOW \
  --brand ./brand.json \
  --refs stripe.com,linear.app,lattice.com \
  --through-line "Send the invoice. Get the money." \
  --avoid "testimonial carousel, gradient hero, 10x claims, trusted-by logos"
```

Output: a single Next.js component file, with the metadata block, the OG image script, and the live counter wired to a stubbed API.

---

## Next steps

- Run [`/ux-polish`](How-to-detect-AI-slop-in-your-design) on every output before shipping
- For dashboards, see [How to design a dashboard with Claude Code](How-to-design-a-dashboard-with-Claude-Code)
- For motion that respects performance, see [How to add motion that doesn't break Core Web Vitals](How-to-add-motion-that-doesnt-break-Core-Web-Vitals)
- For case-study format output, see [How to ship a case study from product data](How-to-ship-a-case-study-from-product-data)

---

**Plugin repo:** https://github.com/Laith0003/ux-skill
**Author:** Laith Aljunaidy — https://www.linkedin.com/in/laith-aljunaidy/
**License:** MIT
