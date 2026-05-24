# Wfrah-style case study format

The Wfrah editorial format for case studies — numbered (A) through (G) sections, ultra-wide editorial typography, two-tone body emphasis, pure monochrome, generous white space, RTL-safe. The `/ux-case-study` command produces it in Blade, HTML, or Markdown.

This page is the format reference. If you are documenting a project, an audit outcome, a redesign, a product launch, or a portfolio piece, this is the format. The format is opinionated. Follow it.

---

## Why a strong case study format matters

Case studies are how design work outlives the project. A good case study:

1. **Proves the work.** Shows the problem, the constraint, the solution, the outcome. Skeptical reader walks away convinced the work was real.
2. **Positions the team.** The format signals seriousness. A case study that looks like every Behance template signals nothing; a case study that has its own discipline signals taste.
3. **Earns recall.** Distinctive visual language is what people remember. Six months after reading the case study, the reader remembers the layout before they remember the project name.

Most case studies fail at all three. They are slide decks dressed up as web pages. They use stock photography for emphasis. They open with a hero shot of the product on a phone. They run 12 sections of "we wireframed, we prototyped, we shipped."

The Wfrah format is a counter. Pure monochrome. Editorial typography. Numbered sections. White space as a structural element. No decoration without purpose.

---

## The pure-monochrome rule

The case study uses only black, white, and grays. No chromatic accent.

This is non-negotiable. The reason: monochrome makes the work itself carry the visual load. If the case study has its own color scheme, that color competes with the screenshots and the product imagery. Monochrome surrenders to the work.

### Exception: the work itself

The product imagery, screenshots, brand marks, and reference photography may contain whatever colors the work contains. The case study chrome is monochrome; the work it documents is not.

If a screenshot has brand blue, that's fine — the blue is in the screenshot, not in the layout. If the case study uses a brand-blue accent in its own typography or dividers, that's a violation.

### Grays in use

The palette:

```
--mono-canvas: oklch(99% 0 0);  /* near-white background */
--mono-text: oklch(15% 0 0);    /* near-black body */
--mono-gray-1: oklch(85% 0 0);  /* hairline borders */
--mono-gray-2: oklch(60% 0 0);  /* secondary text */
--mono-gray-3: oklch(35% 0 0);  /* tertiary emphasis */
```

Five values, no more. The case study uses these and only these.

### Anti-patterns

- **Brand color overlays.** A brand teal as the accent in headings.
- **Gradient backgrounds.** Even subtle ones.
- **Color-coded sections.** Section A in blue, section B in green, etc. Use numbers instead.
- **Decorative photography.** Sunset photos, abstract patterns, "creative" backgrounds. Cut.
- **Emoji in any section.** Never.

---

## Numbered section codes (A)-(G)

The case study uses lettered section codes from (A) through (G). Each letter has a typical purpose, but the codes are flexible — you adapt to the project.

### Default section sequence

| Code | Section | Typical content |
|---|---|---|
| (A) | About | The project's identity. What it is, who it's for, when it shipped. |
| (B) | Mission | The problem the project addresses. The user's situation before the work. |
| (C) | Outcomes | What the project achieved. Measurable and qualitative. |
| (D) | Impact | The broader effect — users reached, hours saved, decisions enabled. |
| (E) | Market | The competitive landscape. What existed before this. |
| (F) | Chance | The opportunity the project bet on. The hypothesis. |
| (G) | Target Audience | Who the project is built for. Detailed user characterization. |

### Why letters not numbers

Numbered sections (1, 2, 3) imply sequence — the reader expects to read in order. Lettered sections suggest a glossary — the reader picks the section relevant to them.

A funder reads (E) Market and (F) Chance first. An engineer reads (C) Outcomes and (G) Target Audience. A portfolio reviewer reads (A) About and skims the rest. The lettered format respects this.

### Section count

Use as many or as few sections as the project warrants. Seven (A-G) is the typical range. A small project might use four (A, B, C, G). A large project might extend to (H) Process or (I) Learnings.

Never exceed nine sections. If you need more, the case study should be broken into multiple case studies.

---

## Editorial typography

The case study uses ultra-wide display typography for section headings and body type that respects scanning behavior.

### Display typography

Section headings and major callouts use:

```css
font-family: var(--display-font);   /* e.g., Inter, Söhne, Roobert, or system */
font-size: clamp(48px, 7vw, 96px);
line-height: 1.0;
letter-spacing: -0.04em;
font-weight: 600;
```

The display type is large. On a 1440px viewport, headings are 96px. On a 375px viewport, they are 48px. The `clamp` function scales between.

Tight tracking (`-0.04em`) compensates for the size. Loose tracking at 96px reads as bloated; tight tracking reads as deliberate.

Line height of 1.0 is acceptable because the headings are short — typically 2-5 words. Long headings need 1.1 to breathe.

### Body typography

Body type uses:

```css
font-family: var(--body-font);   /* e.g., Inter, system serif fallback */
font-size: 18px;
line-height: 1.6;
letter-spacing: 0;
font-weight: 400;
max-width: 65ch;
```

Body is 18px — slightly larger than the 16px default. This is editorial-scale, not interface-scale. The reader is here to read, not to scan a dashboard.

Line height of 1.6 gives breathing room. Max-width of 65 characters per line is the canonical readable measure.

### Caption typography

Captions, footnotes, and source citations use:

```css
font-size: 13px;
line-height: 1.5;
color: var(--mono-gray-2);
font-style: italic;
```

Italic for captions makes them register as voice-of-narrator, not voice-of-product. Small and gray, they don't compete with body text.

### Quote typography

Pull quotes and large quotes use:

```css
font-size: clamp(28px, 4vw, 48px);
line-height: 1.2;
letter-spacing: -0.02em;
font-weight: 500;
color: var(--mono-text);
max-width: 18ch;
```

Quotes are display-adjacent — large, distinct, but not heading-large. Max-width of 18 characters per line forces them to be short and punchy. If a quote needs more than 18 characters per line, it's not a quote, it's body text.

### The display/body contrast

The case study runs on the tension between display (huge, tight, opinionated) and body (calm, readable, generous). The contrast is the design.

Anti-pattern: making body type bigger to "balance" display. The display is supposed to dominate. Let it.

---

## Two-tone body emphasis

Within body paragraphs, use two tones — solid black for emphasis, gray for context.

```css
/* default body */
color: var(--mono-text);   /* oklch(15% 0 0) */

/* emphasis (key phrases) */
color: oklch(0% 0 0);   /* pure black */
font-weight: 500;

/* context (supporting details) */
color: var(--mono-gray-2);   /* oklch(60% 0 0) */
```

The technique: write the paragraph. Identify the 3-5 phrases that carry the meaning. Make those phrases solid black (and slightly heavier weight). Make the supporting context gray.

Reading the gray text alone is unintelligible. Reading the black phrases alone gives the essence. Reading both gives the full paragraph. The reader can choose their depth.

### Example

```
> The platform launched in <strong>March 2026</strong>, replacing
<span class="context">three months of paper coupon distribution and SMS-blast
campaigns</span> with a <strong>single phone-based identity</strong> that
worked across <span class="context">forty-seven partner storefronts in
Amman</span>. The first thousand users registered in <strong>under six
weeks</strong>.
```

Black phrases: "March 2026," "single phone-based identity," "under six weeks." The skim-reader gets the essence — when, what, how fast.

Gray context: the SMS-blast detail, the 47 storefronts. The deep-reader gets the texture.

### When not to use two-tone

- **Headings.** Headings are already display-emphasized; don't double-emphasize.
- **Lists.** The list structure is the emphasis.
- **Captions.** Captions are already secondary; don't sub-emphasize.
- **CTAs.** Buttons have their own visual hierarchy.

---

## Hairline section separators

Sections are separated by hairline rules, not by cards or shadows.

```css
.section-divider {
  border: none;
  border-top: 1px solid var(--mono-gray-1);
  margin: 0;
  padding: 0;
}
```

The hairline is `oklch(85% 0 0)` — a light gray. On a near-white canvas, it reads as a clear-but-quiet division. Stronger borders feel like UI; hairlines feel like editorial.

### Anti-patterns

- **Card containers.** Wrapping a section in a box with `border-radius: 12px` and `box-shadow`. The case study is not an app dashboard.
- **Full-bleed colored backgrounds.** Section A on white, Section B on light gray, Section C on a slightly different gray. Pick one canvas color and stick to it.
- **Decorative dividers.** Wavy lines, dotted lines, illustrated separators. Cut them.

### Section spacing

Use generous vertical white space:

```css
.section {
  padding: 8rem 0;   /* 128px top/bottom */
}

@media (min-width: 1024px) {
  .section {
    padding: 12rem 0;   /* 192px top/bottom on desktop */
  }
}
```

This is large. It is supposed to be. A case study is a slow, deliberate read. The white space is the design.

---

## Generous vertical white space

White space is treated as a structural element. The format budgets significant space:

- **Between sections**: 128-192px vertical padding (8-12rem).
- **Above section headings**: another 64-96px (4-6rem) above the heading.
- **Between paragraphs**: 1.5em (about 27px at 18px body).
- **Between heading and first paragraph**: 48-64px (3-4rem).

The reader should feel like they are reading something carefully designed, not skimming a wall of content. The white space carries the "this matters" signal.

### Why so much white space

Three reasons:

1. **Editorial gravity.** Magazines and books use white space to communicate value. Crowded layouts feel cheap.
2. **Reading rhythm.** White space gives the eye somewhere to rest between sections.
3. **Recall.** Spatial separation aids memory. The reader remembers "the part with X" partly because X had its own visual room.

### Anti-pattern: white space on mobile too

On mobile, the white space should reduce proportionally. 192px on desktop becomes 96px on mobile. Don't keep desktop spacing on small viewports — that's just empty screen.

```css
@media (max-width: 768px) {
  .section {
    padding: 6rem 0;   /* 96px */
  }
}
```

---

## Bilingual layout (RTL-safe)

The case study must work in both LTR and RTL. For MENA-market projects, Arabic is the primary language. For others, Arabic is the secondary.

### Logical properties

Use CSS logical properties everywhere directional:

```css
/* Wrong */
.callout {
  margin-left: 2rem;
  padding-right: 1rem;
  border-left: 1px solid var(--mono-gray-1);
}

/* Right */
.callout {
  margin-inline-start: 2rem;
  padding-inline-end: 1rem;
  border-inline-start: 1px solid var(--mono-gray-1);
}
```

Logical properties (`margin-inline-start` instead of `margin-left`) flip automatically under `dir="rtl"`.

### Bilingual content

If the case study contains both English and Arabic copy:

- Each language has its own typography (a sans-serif Arabic face paired with a sans-serif Latin face).
- Each language has its own paragraph, not mixed within a paragraph.
- Numbers stay in their native script (Western Arabic numerals in English; Eastern Arabic numerals in Arabic, if your audience expects them).
- Captions identify language: "(English)" or "(العربية)" if context is unclear.

### Reading direction

Section headings sit at the same logical position in both languages — `inline-start`. In LTR, that's left. In RTL, that's right. The page flips entirely; nothing is "in the same place" in absolute terms.

### Quotation marks

Use curly quotes appropriate to the language:

- English: "double" and 'single'
- Arabic: «guillemets» or "double" depending on style guide

Never use straight quotes in published case studies. Straight quotes signal "I forgot to render the typography."

### Hyphens and dashes

Use em dashes (—) not hyphens (-) for parenthetical breaks. Use en dashes (–) for numeric ranges (2024–2026). Reserve hyphens for hyphenated words.

---

## Image treatment

Images are full-bleed, no frames, no shadows.

### Full-bleed images

```css
.case-study-image {
  display: block;
  width: 100%;
  margin: 4rem 0;
  border: none;
  border-radius: 0;
  box-shadow: none;
}
```

The image is the image. No "device mockup" frames around screenshots. No "polaroid" effects. No drop shadows.

### Why no frames

Frames around product screenshots add nothing. They signal "this is a screenshot" which is already obvious from context. They add visual noise. They constrain the image to a device aspect ratio that may not be the right one.

If you must show a product in context, do so with a real photo of the product in use — not a Photoshop mockup.

### Aspect ratios

Use ratios that suit the content:

- **Hero images**: 16:9 or 21:9 (cinematic).
- **Screenshots**: native aspect of the source.
- **Portrait imagery**: 4:5 or 3:4.
- **Detail shots**: square (1:1).

Don't crop to a uniform ratio across all images. Variation is the design.

### Captions

Captions sit below the image, gray, italic, small.

```html
<figure>
  <img src="..." alt="...">
  <figcaption>
    The dashboard at first load — three days after launch, before any
    optimization. Forty-seven active partners in the partner directory.
  </figcaption>
</figure>
```

The caption adds context that the image alone doesn't carry. It is not a label ("Dashboard screenshot"); it is a sentence.

### Black-and-white photography

If using photography, it must also be monochrome. Convert color photography to grayscale to match the format's discipline.

The exception: if a photograph contains the product itself (e.g., a partner using the app), the product imagery may retain its native colors. Treat the photo as you would a screenshot.

---

## Default section sequence

The default order of sections — adapt to project type:

### (A) About

The project's identity card.

- What is the project?
- Who is it for?
- When did it ship (or when did this phase ship)?
- Where can it be seen (URL, app store, etc.)?

Length: short. 50-100 words plus an image. The reader should know what they're reading about by the end of (A).

### (B) Mission

The problem the project addresses.

- What was the user's situation before this work existed?
- What was broken, missing, or inadequate?
- What was the cost of that brokenness — to users, to the market, to time?

Length: 200-400 words. This is where you make the problem feel real. Use specific examples. Quote a user if you have one. Avoid abstractions like "users were frustrated."

### (C) Outcomes

What the project achieved.

- Measurable: numbers, time saved, conversion rates, retention, etc.
- Qualitative: testimonials, observed behavior changes, decisions enabled.
- What you set out to achieve vs what you actually achieved.

Length: 150-300 words. Be specific. "47 partners in 6 weeks" is better than "rapid partner adoption." If you have charts, embed them — but the charts must also be monochrome.

### (D) Impact

The broader effect of the project.

- How many users were reached?
- What hours of work or cost were saved?
- What new behaviors became possible?
- What did the project enable downstream?

Length: 150-300 words. Impact is bigger than outcomes — outcomes are what you measured, impact is what those measurements mean.

### (E) Market

The competitive landscape.

- Who else was solving (or trying to solve) this problem?
- What did they get right? What did they get wrong?
- Where does this project sit in the landscape?

Length: 200-400 words. This is where you position. Be honest about competitors. Don't strawman.

### (F) Chance

The opportunity the project bet on.

- What was the hypothesis?
- What evidence supported the hypothesis at the time of the bet?
- What was the risk if the hypothesis was wrong?

Length: 150-300 words. This is where Lean UX thinking shows. The case study reads better when the hypothesis is named and the bet is honest.

### (G) Target Audience

Detailed characterization of the user.

- Who exactly is the primary user?
- What is their day like?
- What problem are they solving when they use this?
- What constraints do they operate under?

Length: 200-400 words. This is where you show user understanding. Avoid persona-as-cliche ("Sarah is 32, lives in a city, loves coffee"). Show specific behaviors, specific decisions, specific moments.

---

## Adapting section codes for different project types

The default sequence works for most product cases. Adapt for project type:

### Service design case study

- (A) About — service name, scope.
- (B) Mission — service problem.
- (C) Outcomes — KPIs.
- (D) Impact — broader effect.
- (E) Journey — service blueprint, key touchpoints.
- (F) Roles — staff, partners, vendors.
- (G) Audience.

### Brand identity case study

- (A) About — brand name, sector.
- (B) Mission — brand problem (positioning, recognition).
- (C) System — visual system overview.
- (D) Application — how it shows up.
- (E) Market — competitive identity landscape.
- (F) Voice — verbal identity.
- (G) Audience.

### Internal tool case study

- (A) About — tool name, internal user count.
- (B) Mission — workflow problem.
- (C) Outcomes — time saved, errors reduced, satisfaction.
- (D) Adoption — how usage grew.
- (E) Build — technical approach.
- (F) Decisions — key product decisions.
- (G) Team — internal user characterization.

### Audit-as-case-study

When a case study documents an audit outcome (not a build):

- (A) About — what was audited, when.
- (B) Findings — the headline severity counts and top issues.
- (C) Fixes — what was addressed.
- (D) Outcomes — what changed after fixes.
- (E) Lenses — which lenses surfaced the most findings.
- (F) Method — how the audit was conducted.
- (G) Audience — the surface's intended users.

### Single-section case study

For very small projects or quick wins, the format may collapse to a single section with no codes — a 200-400 word piece with one or two images. Don't force the (A)-(G) structure where it doesn't fit.

---

## Output formats

The `/ux-case-study` command produces output in three formats. Use the one that matches your stack.

### Blade for Laravel

For projects using the Laravel + Blade stack:

```php
<x-layout title="Case Study — {{ $project }}">
  <section class="case-section case-about">
    <span class="case-code">(A)</span>
    <h2 class="case-heading">About</h2>
    <div class="case-body">
      <p>{!! $about !!}</p>
    </div>
  </section>

  {{-- ...more sections... --}}
</x-layout>
```

The Blade output uses the project's existing layout component and component primitives. It is RTL-safe via the project's existing `dir="rtl"` handling.

### HTML for static sites

For static portfolios or one-off published pages:

```html
<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Case Study — Project Name</title>
  <style>/* embedded monochrome tokens + typography */</style>
</head>
<body>
  <main>
    <section class="case-section">
      <span class="case-code">(A)</span>
      <h2 class="case-heading">About</h2>
      <p>...</p>
    </section>
    <!-- ... -->
  </main>
</body>
</html>
```

The HTML output is self-contained — embedded CSS, no external dependencies. It can be hosted anywhere, emailed, exported to PDF.

### Markdown for portability

For docs sites, README files, or portfolio platforms that accept markdown:

```markdown
# Case Study — Project Name

## (A) About

[Body paragraph with **black emphasis** and supporting context...]

---

## (B) Mission

[Body paragraph...]
```

Markdown loses the typographic precision of the other formats but gains portability. Use it for archival or when the host platform handles its own styling.

---

## Publishing the case study

The case study is a deliverable. Treat it as one.

### PDF generation

For a publication-quality PDF:

1. Render the HTML output in a headless browser at A4 size.
2. Use print-specific CSS:

```css
@media print {
  .case-section {
    page-break-inside: avoid;
    padding: 4rem 0;
  }
  .case-image {
    page-break-inside: avoid;
  }
  @page {
    margin: 1in;
  }
}
```

3. Output to PDF with embedded fonts.

The PDF should look like an editorial publication, not a screenshot of a webpage.

### Host suggestions

- **Personal site**: best for portfolio reach. Set up at a stable URL.
- **Medium/Substack**: limited typographic control — the format will degrade. Don't host there.
- **Behance/Dribbble**: design-community discovery. The format will partially survive.
- **Direct PDF**: best for client-facing deliverables. No format degradation.
- **Notion/Coda**: limited typographic control; the white space will compress.

The first and last are usually best. Personal site for discovery; PDF for delivery.

### Sharing the case study

- Include a one-line summary in the link preview (Open Graph meta tags).
- Tag with the project's name, the role you played, and the year.
- For client work, include the client's name only with permission.
- Cite tools, frameworks, and collaborators in a small footer section if relevant.

---

## Real example walkthrough

A hypothetical case study for a loyalty platform, in shortened form.

### Opening

```
# The Dot — phone is the customer.

A monochrome editorial typeface dominates the page. Below the title,
a single hairline rule. Below that, white space — about 96px — then
the first section.
```

### (A) About

```
(A) About

The Dot is a phone-first customer loyalty platform for MENA partners.
Launched in March 2026 in Amman, Jordan. Live at thedotwallet.com.
Forty-seven partner storefronts in the first six weeks.

[Full-bleed image: a phone showing the wallet, in a real cafe context,
photographed in monochrome.]
```

### (B) Mission

```
(B) Mission

Loyalty in MENA, before The Dot, ran on paper. Stamp cards in wallets,
SMS broadcasts to phone numbers nobody updated, plastic cards that
expired before they were used. Partners paid for printing. Customers
forgot the cards. The data never came back.

The mission: a single phone number, used everywhere. A customer earns
at the cafe in Sweifieh, redeems at the gym in Abdoun, sees their
balance in any partner storefront — all from one identity they
already have.

[Image: stamp card chaos in a real wallet, monochrome.]
```

### (C) Outcomes

```
(C) Outcomes

Six weeks after launch: 1,047 users registered. 47 partner storefronts
active. 2,300 transactions processed. The average user touched 2.4
partners. Zero customers asked for a plastic card.

The outcome that mattered most: a partner in Sweifieh ran a tier promotion
on a Tuesday that drove 60 visits to a partner gym in Abdoun on Wednesday.
Cross-partner traffic. That had not existed before.
```

### (D) Impact

```
(D) Impact

The partners stopped printing stamp cards. They saved an estimated
$11,000 in printing across the first six weeks. More importantly,
they started seeing each other's customer activity. The platform
became, accidentally, a competitive intelligence tool — a partner
could see whether their tier-up promotion drove visits at a competitor.

This was not the original feature. It was the original consequence.
```

### (E) Market

```
(E) Market

The MENA loyalty space, before The Dot, was three things: paper,
SMS, and plastic. Two regional players had built app-based loyalty
but with single-brand wallets — the customer needed one app per
partner. Adoption was low because customers don't install one app
per coffee shop.

The Dot's bet: phone is already in every customer's hand, every
hour. Make the wallet phone-native, no app install, no email,
no password. Subdomain on the partner's existing storefront.
```

### (F) Chance

```
(F) Chance

The hypothesis: if loyalty was as easy as showing a phone, partners
would adopt and customers would actually use it. The evidence:
informal interviews with 23 partners over four weeks; pilot with
Bashiti Cafe in Sweifieh which showed an 11% redemption rate vs
the previous 3% on plastic cards.

The risk: if customers didn't share their phone number freely,
the system was dead. We bet they would, because they were already
giving phone numbers to mall WiFi, parking apps, food delivery,
and every grocery checkout.
```

### (G) Target Audience

```
(G) Target Audience

The primary user is the MENA-region customer who already gives their
phone number to four different apps before noon. They are 22-45.
They use Instagram, WhatsApp, and one food delivery app daily.
They have a paper stamp card in their wallet right now from a cafe
they last visited three months ago. They cannot remember which cafe.

They will not install another app. They will not sign up with email.
They will not remember a password. They will give you their phone
number if your storefront, in front of them, in their hand, asks
for it once.

The secondary user is the partner — the storefront operator who
prints stamp cards once a quarter and wonders, every quarter, what
that printing cost achieved.
```

The case study ends. Footer with project credits, year, link to the live product.

---

## Anti-patterns in case studies

### The hero deck

The case study opens with a "hero deck" of mockups on different devices — a phone, a tablet, a laptop, all showing the product. The reader has not yet been told what the product is. Cut all device mockups. Open with the product in context.

### The process timeline

The case study includes a long "process" section: "We started with research, then ideation, then wireframes, then prototypes, then user testing, then..." This is the design student's case study. The reader doesn't need your process; they need to know what you made and what it did. Cut the process section unless the process itself is the story.

### The features tour

The case study walks through every screen in the product. This is a documentation site, not a case study. Show the screens that demonstrate the (B) Mission and (C) Outcomes. Cut the rest.

### The chrome creep

The case study slowly adopts the brand's colors as accents — "just this one heading in brand teal." Hold the monochrome discipline. The work brings the color.

### The emoji-as-section-marker

Section headings with decorative emoji. Never. Use the lettered codes.

### The personality voice

The case study is written in a chatty, first-person voice: "We were SO excited when..." Direct narration without theater. The work is the show.

### The unverifiable claim

The case study claims numbers without evidence: "Adoption grew by 400%." From what baseline? Over what period? In what segment? If you cite numbers, cite the baseline and period.

---

## Variations and extensions

### Bilingual case studies (English + Arabic)

Lay out two columns at desktop, stacked at mobile. Each section has both languages, side by side. Hairline divider between them.

```
[ABOUT (English)]      |     [حول (العربية)]
                       |
Body in English        |     Body in Arabic
                       |
```

For RTL primary, swap the order — Arabic first, English second.

### Time-series case studies

For projects that evolved over time, add a sub-axis: each section has phases.

```
(C) Outcomes

- Phase 1 (March-April 2026): 247 users, 12 partners.
- Phase 2 (May-June 2026): 1,047 users, 47 partners.
- Phase 3 (Pending): TBD.
```

### Multi-project case studies

When documenting a body of work (not a single project), use the lettered codes for project meta-information and add a Projects section listing each one.

### Inverse case studies (failure stories)

The format works for projects that didn't succeed. (C) Outcomes becomes (C) What Happened. (F) Chance becomes (F) Bet. (E) Market becomes (E) Why It Failed. The discipline of the format makes failure tellable.

---

## Quality checklist

Before publishing:

- [ ] Pure monochrome — no brand color in chrome.
- [ ] Lettered sections (A)-(G) or appropriate variation.
- [ ] Display typography at clamp(48px, 7vw, 96px) for headings.
- [ ] Body typography at 18px, 65ch max-width.
- [ ] Two-tone emphasis used purposefully — not on every word.
- [ ] Hairline section dividers, no cards or shadows.
- [ ] Generous vertical white space (8-12rem between sections).
- [ ] RTL-safe (logical properties used throughout).
- [ ] Images full-bleed, no frames.
- [ ] Captions below images, gray italic.
- [ ] No emojis.
- [ ] Specific claims with baselines and periods.
- [ ] One primary user characterized in (G).
- [ ] One named hypothesis in (F).
- [ ] Length appropriate to project scope.

---

## Related pages

- [The 6 Audit Lenses](The-6-Audit-Lenses) — for case studies documenting audit work.
- [Polaris-style audit reports](Polaris-style-audit-reports) — when the case study includes an audit summary.
- [Frontend stacks compared](Frontend-stacks-compared) — for implementing the case study in your stack.
- [Real-life UX consulting](Real-life-UX-consulting) — for a human review of your case study draft.

---

## Footer

Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
Author: Laith Aljunaidy — [LinkedIn](https://www.linkedin.com/in/laithaljunaidy/) — +962 79 786 8335
