# How to Ship a Case Study from Product Data

Generate a publishable case study in Wfrah editorial format — numbered (A)–(G) sections, ultra-clean editorial typography, two-tone body emphasis, pure monochrome — from your project facts using `/ux-case-study`. Outputs as Blade, HTML, or Markdown.

This page walks you through the format, the discovery, the discipline that separates a real case study from a case-study-shaped marketing brochure, and the publishing path.

---

## What a case study is for

A case study has three jobs. In order of priority:

### 1. Proof

The case study proves the product works for a real customer with real numbers. Not "we helped a leading enterprise improve efficiency." Specifically: "Bashiti Pharmacy went from 12-minute checkout reconciliation to 90 seconds. Their daily reconciliation now happens before they lock the door, not the next morning."

If your case study has no specific numbers or specific moments, it is not proof. It is testimonial-shaped marketing.

### 2. Positioning

The case study positions you in the market. The customer they chose to feature, the problem they chose to highlight, the outcome they chose to measure — each is an editorial decision that says "this is the kind of work we do."

A case study about a global enterprise positions you as enterprise-ready. A case study about a 3-person agency positions you as a daily-use tool for small teams. A case study about a hospital positions you as a serious system. The choice of who appears in the case study is itself part of the brand.

### 3. Brand recall

The case study should be memorable. Not "well-designed." Memorable. Something the reader can quote 90 days later when a colleague asks "have you seen X?"

The Wfrah format is built for all three. It rejects testimonial-carousel patterns, rejects round-number invented stats, and forces an editorial restraint that survives in memory.

---

## The Wfrah format: pure monochrome, numbered sections, editorial type

Wfrah is a published case-study format the plugin treats as the canonical reference. Six characteristics define it.

### 1. Pure monochrome

No chromatic accents. Black ink, white canvas, gray scale for the body. The brand mark may be colored on the landing page, in the docs, in the dashboard — but in the case study, color is removed.

Why: a case study is the most editorially serious surface the brand publishes. Removing color forces every choice to be about hierarchy and type. The reader's attention does not have anywhere to escape.

Exception: the customer's logo, rendered in their own brand color, in a single appearance at the top. That single use of color anchors the case study to the customer, not the brand.

### 2. Numbered (A)–(G) sections

Seven sections, fixed order, labeled with a letter prefix.

- (A) About
- (B) Mission
- (C) Outcomes
- (D) Impact
- (E) Market
- (F) Chance
- (G) Target Audience

The letters are visible. They appear in a margin, in an oversized display font, at the start of each section. The reader sees the structure of the document. The letters also act as anchor IDs for deep linking.

### 3. Editorial typography

- Display font: a real editorial face (PP Editorial New, Söhne, GT Sectra, Tiempos)
- Body font: a humanist sans or a literary serif
- Numerals: tabular, monospaced if the figure is read as data
- Line length: 50–65 characters for body, 30–45 for pull quotes
- Hanging punctuation on opening quotes
- Drop cap on the (A) section opener
- Negative tracking on headlines 30px+

### 4. Two-tone body emphasis

The body uses two tones: solid black for the key phrases that carry the argument, and gray-700 for the context around them.

The reader can skim the case study and pick up the argument from the black phrases alone. The gray context is for the second read.

This is not bold-on-emphasis. It is color contrast. The black phrases are not bold; they are the same weight as the gray. The contrast is hue only.

### 5. Hairline separators (no cards)

Sections are separated by 1px hairlines, not by cards, not by background tints, not by shadows. The document reads as a single editorial surface, not as a stack of components.

### 6. Bilingual support (RTL-safe)

For Dot's MENA market and any other RTL-required publishing, the format must mirror cleanly. Letter prefixes (A)–(G) become Arabic letters (أ)–(ز) or remain Latin with `dir="rtl"` on the body. Line lengths and margins mirror correctly.

---

## Required sections — (A) through (G) in detail

Each section has a specific job. The plugin enforces the job and rejects content that does not fit.

### (A) About

A single paragraph. Who is the customer? What do they do? Where do they operate? When did they start using the product?

This is the "establishing shot." The reader walks in cold; this section gets them oriented in 60 seconds.

Length: 80–120 words. No more.

Example:

> Bashiti Pharmacy operates 14 locations across Amman. Founded in 1982 by Dr. Khalid Bashiti, the chain has grown from a single counter in Jabal Amman to one of Jordan's largest independent pharmacy networks. Bashiti has run on Odoo since 2019. They began rolling out Dot at the flagship branch in February 2026.

What the section is NOT:

- A history of the company beyond what's relevant
- An award list
- A description of the company's values
- A description of the problem (that goes in B)

### (B) Mission

What problem were they trying to solve? Not "they wanted to improve customer engagement." Specifically: "End-of-day reconciliation was taking 12 minutes per shift across 14 branches, blocking closing time and producing nightly errors that took the next morning to resolve."

The mission section names the pain in measurable terms. If the customer can't name the pain in measurable terms, the case study isn't ready yet — go back to the customer and ask for specifics.

Length: 120–180 words. Includes one or two specific numbers (the baseline).

### (C) Outcomes

What changed, measured. Not "they're happier." Specifically: "Reconciliation now takes 90 seconds. Closing happens at 11pm sharp, not midnight. The morning reconciliation desk has been eliminated; the headcount moved to customer service."

Outcomes is the proof section. Every claim is a number or a specific moment.

Length: 150–250 words. Includes 3–5 measured outcomes.

Sample structure:

> Before: 12-minute reconciliation per shift. After: 90 seconds.
>
> Before: ~3 reconciliation errors per branch per week, resolved next morning. After: 0.4 errors per branch per week, resolved before close.
>
> Before: 1 reconciliation analyst, full-time. After: 0. The role moved to customer service.
>
> Before: closing varied between 10:45pm and 11:30pm. After: closing at 11pm, +/- 4 minutes, 94% of nights.

### (D) Impact

What did the outcomes enable? This section is where the human story lives. The outcomes were measured; the impact is what those outcomes meant for the people involved.

> "We used to close, eat, then come back at 10am to fix the reconciliation. Now we close, lock the door, and the books are clean. My team gets their evenings back." — Yara Bashiti, Operations

Impact is allowed one direct quote per case study. No more. The quote must be from a named person with a named role at the customer, attributed correctly.

Length: 100–150 words including the quote.

### (E) Market

What does this customer's experience say about the broader market? This is where the case study generalizes — carefully, with the customer's permission.

> Bashiti's profile is typical of the MENA mid-market pharmacy: 5–25 branches, Odoo-based ERP, manual end-of-day workflows, deep loyalty to a regional brand. The reconciliation problem we solved at Bashiti is one of three universal pain points in this segment. The other two — voucher fraud and partner-portal latency — we expect to address in the next two case studies.

Length: 100–150 words. Names the segment, names the universal pain, gestures at the next chapter.

### (F) Chance

The risk and the conditions that made the outcome possible. Most case studies skip this section because it requires honesty. The Wfrah format requires it because honesty is what makes the case study credible.

> Bashiti was a willing first customer because Khalid Bashiti and our founder share a Friday backgammon table. They tolerated three weeks of integration bugs that no enterprise procurement team would have. Our second customer, a 6-branch chain without that relationship, signed only after we'd had Bashiti as a reference for 90 days. The relationship made the case study possible; the case study made the second customer possible.

Length: 100–150 words. Names the precondition, names the dependency, names what would not have worked without it.

### (G) Target Audience

Who else should read this case study and recognize themselves in it? This is the call to action, but not as "click here to start a trial." As "if you are in this situation, this story is yours."

> If you run 5–25 branches on Odoo with a manual reconciliation workflow, this is your story. If your closing time slips because of reconciliation, this is your story. If you've ever had a reconciliation analyst whose job felt like clerical archaeology, this is your story. Talk to us. layla@dot.com.

Length: 80–120 words. Ends with one specific way to act.

---

## Step 1: Gather your project facts

Before running the command, gather six things. Each is a specific question with a specific answer.

### 1. Customer permission

Have they agreed in writing to be named, to have their numbers published, and to have their quote attributed? If not, the case study cannot be published. The plugin will not generate a named case study without this.

If permission is limited (e.g., they agree to be named but not to publish specific numbers), the discovery captures the limit and the output respects it.

### 2. The baseline

What were the numbers before? "12-minute reconciliation per shift." "3 errors per branch per week." Real numbers, with units, with scope.

If you don't have a baseline, you don't have a case study. Go back and measure.

### 3. The outcome

What are the numbers now? "90 seconds." "0.4 errors per branch per week." Same units, same scope, comparable.

### 4. The timeline

When did this start? When did the outcomes land? "Rollout February 1, 2026. Outcomes measured at 60 days, again at 120 days." A case study without a timeline reads as marketing.

### 5. The quote

One quote from a named person at the customer, attributed correctly. Verbatim. Approved by the customer for publication.

### 6. The honest precondition

What would not have worked without a specific condition? The first customer was a personal contact? The product had a feature that was custom-built? The customer's IT team did half the integration?

Naming the precondition makes the case study credible. Hiding it makes it suspect.

---

## Step 2: Run `/ux-case-study`

In Claude Code:

```
/ux-case-study
```

Discovery runs. The plugin asks:

- Q1. Customer name and the customer's permission status
- Q2. Customer's industry and size
- Q3. The baseline (numbers before)
- Q4. The outcome (numbers after)
- Q5. The timeline
- Q6. The quote and the named attribution
- Q7. The precondition (the chance)
- Q8. The target audience (who else this is for)
- Q9. The output format (Blade / HTML / Markdown)
- Q10. The language (English, Arabic, bilingual)

After discovery, the plugin generates the seven sections.

For an existing case study you want reformatted:

```
/ux-case-study --reformat ./existing-case-study.md
```

The reformat mode imports the existing content, fits it into the Wfrah structure, and flags missing sections.

---

## Step 3: Pick output format (Blade / HTML / Markdown)

Three formats. Pick one based on where the case study will live.

### Blade

For a Laravel + Blade product (Dot). The output is a Blade view that uses the design system tokens.

```
/ux-case-study --format blade --output ./resources/views/case-studies/bashiti.blade.php
```

Output structure:

```blade
@extends('layouts.case-study')

@section('content')
  <article class="case-study">
    <section id="A" class="case-section">
      <span class="case-section__label">(A)</span>
      <h2 class="case-section__title">About</h2>
      <div class="case-section__body">
        {{-- generated content --}}
      </div>
    </section>
    {{-- (B) through (G) --}}
  </article>
@endsection
```

The Blade template uses real DS classes (`.case-section`, `.case-section__title`, etc.) — not generic Tailwind utility soup.

### HTML

For a static site or a marketing CMS that takes raw HTML. The output is a single self-contained HTML file with inline CSS.

```
/ux-case-study --format html --output ./case-studies/bashiti.html
```

Output uses semantic markup with hairline separators and the editorial type stack inlined.

### Markdown

For a docs site, a blog, a GitHub README, or any markdown-rendering surface. The output uses the section letter prefix in the heading text.

```
/ux-case-study --format markdown --output ./case-studies/bashiti.md
```

Sample markdown output:

```markdown
# Bashiti Pharmacy

## (A) About

Bashiti Pharmacy operates 14 locations across Amman...

## (B) Mission

End-of-day reconciliation was taking 12 minutes per shift...

## (C) Outcomes

Before: 12-minute reconciliation per shift. After: 90 seconds...
```

---

## The pure-monochrome rule

The case study is monochrome. No exceptions inside the seven sections.

- Black ink on warm canvas (or pure white if the brand uses pure white)
- Gray-700 for context body
- Hairline gray-200 for separators
- No chromatic accents inside the seven sections

The only color allowed is:

1. The customer's logo at the top, in their own brand color
2. The hyperlinks in section (G) — but rendered in solid ink with an underline, not in a brand color

Why the rule is absolute: the case study earns gravity by removing decoration. Color reintroduces decoration. The rule is the discipline.

For a brand whose other surfaces use the brand color heavily (Dot uses warm-orange on actions), the case study deliberately departs from that surface. The reader notices the departure. The departure signals "this is a different kind of document."

---

## Two-tone body emphasis

In every paragraph, the key phrases that carry the argument are rendered in solid ink (`#0E0E0E`). The context is rendered in gray-700 (`#3F3F46`).

Both are the same weight. The contrast is color, not weight.

In Blade:

```blade
<p>
  <span class="ink">Bashiti's profile is typical of the MENA mid-market pharmacy:</span>
  <span class="gray">5–25 branches, Odoo-based ERP, manual end-of-day workflows,
  deep loyalty to a regional brand.</span>
  <span class="ink">The reconciliation problem we solved at Bashiti is one
  of three universal pain points in this segment.</span>
</p>
```

In CSS:

```css
.case-section__body .ink { color: #0E0E0E; }
.case-section__body .gray { color: #3F3F46; }
.case-section__body {
  font-family: "Söhne", -apple-system, sans-serif;
  font-size: 17px;
  line-height: 1.6;
  max-width: 62ch;
}
```

The discipline: every paragraph has at most 1–2 ink phrases. Over-using the ink class flattens the contrast and the page reads as bold-everywhere, which means bold-nowhere.

---

## Bilingual support (RTL-safe)

For Dot, every case study can ship in Arabic and English. The Wfrah format mirrors cleanly under `dir="rtl"`.

What changes in Arabic:

- Section labels: (أ) (ب) (ج) (د) (ه) (و) (ز) — or keep Latin (A) through (G) with `dir="rtl"` on the body
- Type stack: an Arabic display face (IBM Plex Sans Arabic, GE SS, Tajawal) + the same English fallback for any English terms
- Line length: 50–65ch still applies (Arabic is dense, so the visual line is similar)
- Direction: right-to-left throughout; hairlines mirror; section letter labels mirror to the right margin

What stays the same:

- Pure monochrome
- Hairline separators
- Two-tone body emphasis
- Sections (A) through (G) in fixed order
- The quote, the numbers, the precondition

For a single bilingual page (English and Arabic side by side), the layout splits vertically with a hairline running down the middle. English left, Arabic right. The reader can read either side independently or scan across.

```
/ux-case-study --format html --language bilingual --output ./bashiti-en-ar.html
```

---

## Hairline separators (no cards)

The case study uses 1px hairline borders to separate sections. Never:

- A card around each section
- A background tint to separate sections
- A drop shadow to separate sections
- A pill or badge to mark the section label

The section label (A)–(G) is rendered in oversized display font in the margin (or above the title), not in a colored circle or badge. The label IS the visual marker. No additional decoration is added.

```css
.case-section {
  border-top: 1px solid #E5E5E5;
  padding-top: 64px;
  margin-top: 64px;
}
.case-section:first-child {
  border-top: none;
  padding-top: 0;
  margin-top: 0;
}
.case-section__label {
  display: block;
  font-family: "PP Editorial New", serif;
  font-size: 48px;
  letter-spacing: -0.04em;
  color: #0E0E0E;
  margin-bottom: 8px;
}
.case-section__title {
  font-family: "PP Editorial New", serif;
  font-size: 32px;
  letter-spacing: -0.03em;
  margin-bottom: 24px;
}
```

---

## Real example walkthrough

A case study for Bashiti Pharmacy, generated end to end.

### Discovery answers

- Q1. Customer: Bashiti Pharmacy. Permission: yes, signed agreement to publish.
- Q2. Industry: independent pharmacy chain, MENA mid-market.
- Q3. Baseline: 12-minute reconciliation per shift, 3 errors per branch per week, 1 dedicated analyst, closing time 11:15pm average.
- Q4. Outcome: 90 seconds, 0.4 errors per branch per week, 0 analysts, closing time 11:00pm +/- 4 min.
- Q5. Timeline: February 1 rollout, measured at 60 days, again at 120 days.
- Q6. Quote: "We used to close, eat, then come back at 10am to fix the reconciliation. Now we close, lock the door, and the books are clean." — Yara Bashiti, Operations Manager.
- Q7. Precondition: founder's personal relationship with Khalid Bashiti enabled the three-week integration tolerance.
- Q8. Target audience: 5–25 branch pharmacy chains on Odoo with manual reconciliation.
- Q9. Format: Blade.
- Q10. Language: English first, Arabic to follow.

### Output

A single Blade file: `resources/views/case-studies/bashiti.blade.php`.

The file extends a `layouts.case-study` template and contains seven sections, each with the letter label, the title, and the body. The body uses the two-tone ink/gray emphasis.

Section (A):

> (A) About
>
> **Bashiti Pharmacy operates 14 locations across Amman.** Founded in 1982 by Dr. Khalid Bashiti, the chain has grown from a single counter in Jabal Amman to one of Jordan's largest independent pharmacy networks. **Bashiti has run on Odoo since 2019.** They began rolling out Dot at the flagship branch in February 2026.

(Where bold above represents ink-rendered phrases, not bold weight.)

Section (C):

> (C) Outcomes
>
> **Before: 12-minute reconciliation per shift. After: 90 seconds.** This was measured across all 14 branches over the first 60 days post-rollout.
>
> **Before: ~3 reconciliation errors per branch per week, resolved the next morning. After: 0.4 errors per branch per week, resolved before close.**
>
> **Before: 1 dedicated reconciliation analyst. After: 0.** The role moved to customer service after a 90-day transition period.
>
> **Before: closing varied between 10:45pm and 11:30pm. After: closing at 11:00pm, +/- 4 minutes, 94% of nights.**

Section (F):

> (F) Chance
>
> Bashiti was a willing first customer because **Khalid Bashiti and our founder share a Friday backgammon table.** They tolerated three weeks of integration bugs that no enterprise procurement team would have. **Our second customer, a 6-branch chain without that relationship, signed only after we'd had Bashiti as a reference for 90 days.** The relationship made the case study possible; the case study made the second customer possible.

The full Blade file is rendered, the metadata block is generated, and the file is ready to commit.

### Visual result

- Warm off-white canvas, near-black ink, gray-700 context
- Section letters (A)–(G) in 48px PP Editorial New, left margin
- Section titles in 32px PP Editorial New
- Body in 17px Söhne, max-width 62ch
- 1px hairline separators
- The single Bashiti logo at the top, in the Bashiti brand green (the only color)
- Drop cap on the (A) opener
- No motion, no decoration, no card

The result reads as an editorial published document, not as a SaaS marketing page.

---

## Publishing the case study

Three publishing paths.

### Where to host

For Dot, case studies live at `thedotwallet.com/case-studies/{slug}` — a route in the Laravel app. The Blade template inherits from a `case-study` layout that loads the editorial type stack and the monochrome stylesheet.

For a static site, host as a folder of HTML files. The OG image generated by `/ux-seo` is shared via the metadata.

For Notion / a CMS, paste the markdown output directly. The CMS strips the section letter labels from the visual rendering if it doesn't support custom headings; that's acceptable.

### How to PDF it

A case study is often shared as a PDF for sales conversations, partner introductions, or investor decks. The plugin can output a print-ready version:

```
/ux-case-study --format pdf --output ./bashiti.pdf
```

The PDF uses:

- A4 portrait, 1-inch margins on all sides
- The same editorial type stack
- Page numbers in the footer (right margin)
- The customer logo at the top of page 1
- Section letter labels rendered in the left margin
- Hairline separators
- The same two-tone ink/gray emphasis

PDF settings:

- Embedded fonts (no missing-glyph risk on the recipient's machine)
- 300 DPI for any raster image
- Hyperlinks preserved (the email in section G is clickable)

For a bilingual PDF, the file is two-up: English on the left page, Arabic on the right.

### Distribution

After publishing:

- Add the case study to your homepage "case studies" section (one card, hairline border, title + customer name + read time)
- Add the OG image to your social posts when announcing
- Submit to relevant aggregators (industry newsletters, MENA fintech roundups)
- Include the PDF in sales outreach
- Pin the announcement on your LinkedIn

Track engagement: time-on-page, scroll depth, PDF downloads. A case study that gets read end-to-end converts; one that gets read only halfway needs a shorter (A) section.

---

## Common mistakes the format prevents

The Wfrah discipline rejects these by structure:

1. **Testimonial-shaped marketing.** The case study cannot ship without specific numbers in (C). Without numbers, there is no (C). Without (C), the format refuses to generate.

2. **Round-number invented stats.** "10x faster" gets flagged by `/ux-polish` if anyone tries to add it. The format expects real measurements.

3. **Logo soup.** No "trusted by [10 logos]" band. The case study features ONE customer, deeply. The reader doesn't need 10 logos to believe in 1 customer's story.

4. **The trusted-by carousel.** No carousel of quotes. One quote, one customer, one story.

5. **The marketing pull quote.** No "Quill helped us 10x our productivity." Only verbatim, named, attributed quotes.

6. **Hidden preconditions.** Section (F) is required. The case study cannot hide the "chance" — the relationship, the custom feature, the tolerance.

7. **Vague call to action.** Section (G) names a specific audience and a specific way to act. Not "learn more." "If you run 5–25 branches on Odoo, email layla@dot.com."

---

## Next steps

- Run [`/ux-polish`](How-to-detect-AI-slop-in-your-design) on the case study output to catch any anti-patterns
- For the landing page that links to the case study, see [How to make AI output look human-grade](How-to-make-AI-output-look-human-grade)
- For dashboards that the case study might reference, see [How to design a dashboard with Claude Code](How-to-design-a-dashboard-with-Claude-Code)
- For any motion in the case-study landing surface, see [How to add motion that doesn't break Core Web Vitals](How-to-add-motion-that-doesnt-break-Core-Web-Vitals)

---

**Plugin repo:** https://github.com/Laith0003/ux-skill
**Author:** Laith Aljunaidy — https://www.linkedin.com/in/laith-aljunaidy/
**License:** MIT
