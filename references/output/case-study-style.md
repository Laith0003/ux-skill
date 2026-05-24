# Case Study Style — Editorial Long-Form Output

This is the house style for `/ux-case-study` and any long-form report the plugin produces. It is editorial, monochrome, and restrained. The aesthetic is the wide-margin design book: black ink, white paper, generous breath, evidence over claim.

This style applies only to case-study outputs. HTML deliverables produced by `/ux-design` are not subject to it; they may use the project's full token system. The pure-monochrome rule below is unique to case studies.

---

## Visual Rules

### Pure Monochrome Only

The entire document is rendered in black, white, and grayscale. No chromatic accent. No brand color. No semantic color (success green, danger red). Nothing.

Allowed colors:
- `#000000` for primary type, primary fills, hairlines.
- `#FFFFFF` for canvas.
- Tailwind `zinc-100` through `zinc-900` for the gray scale.

Forbidden:
- Any hue with saturation greater than zero.
- Any token that resolves to a brand color, including the Dot dot.
- Any photo or chart with chromatic content unless converted to grayscale.

If the case study describes a chromatic system (a brand book, a token chart), render the description in monochrome and describe the color in prose. The case study is the document, not the product.

### Numbered Section Codes

Every primary section is prefixed with a one-letter alphabetic code, set in the margin or above the headline. The codes run alphabetically: (A), (B), (C), (D), (E), (F), (G). If a case study has fewer than seven sections, codes still start at (A) and proceed alphabetically without gaps. If a case study uses a different section set, the codes still march alphabetically.

Render rules:
- Code is the size of body type, weight 500.
- Code sits in the left margin (LTR) or the right margin (RTL) when the layout allows.
- When the layout does not have a margin, the code sits above the headline with 16px of space.
- Codes never sit inline with the headline.

### Ultra-Wide Editorial Headlines

Headlines are display-scale and tight.

- Section headlines: `text-7xl` to `text-8xl`, `font-medium`, `tracking-tighter` or `letter-spacing: -0.04em`.
- Document title: `text-8xl` to `text-9xl`, `font-medium`, `letter-spacing: -0.045em`.
- Subheadings under a section: `text-3xl` to `text-4xl`, `font-medium`, `tracking-tight`.

Headlines wrap. Long headlines wrap deliberately — do not shrink them to fit. Two-line and three-line headlines are correct.

### Two-Tone Body Emphasis

Body type is set in two tones, not two weights. Important phrases sit in solid black (`text-zinc-900`). Context phrases sit in gray (`text-zinc-500` or `text-zinc-400`).

The effect is literary: a paragraph reads like prose where the structurally important words are slightly louder than the surrounding context, without bolding, italicizing, or color-coding.

Rules:
- The black is `text-zinc-900`. The gray is `text-zinc-500` (preferred) or `text-zinc-400` (lower contrast paragraphs).
- Use the gray for: parenthetical context, dates, place names, instrument names, second-tier facts.
- Use the black for: the subject of the sentence, the verb that carries the action, the named outcome.
- Never use both colors on the same word.
- Never use bold or italic to do the work of the gray. The gray is the system.

Example (rendered as plain text here; the actual styling is `<span class="text-zinc-500">`):

> The Bashiti pilot launched in Q4 2026 (across three branches in Amman). Redemption rose 41% in the first six weeks, with no observed change in fraud attempts.

The black words carry the claim. The gray words frame it.

### Hairline Separators

Sections are separated by a single hairline: `border-t border-zinc-200`, full width or column-width. The hairline is 1px. It is not a card border. It is not a divider with shadow. It is a single line that says "the next section starts here."

Forbidden:
- Boxes, cards, panels, containers with visible borders or shadows.
- Dotted or dashed lines.
- Hairlines thicker than 1px.
- Color on the hairline.

### Generous Vertical White Space

The page breathes.

- Between sections: `py-32 lg:py-48`.
- Between a headline and its body copy: `mt-8` to `mt-12`.
- Between paragraphs: `mt-6` to `mt-8`.
- Between a body paragraph and a full-bleed image: `my-24`.

White space is the layout's primary spacing system. Do not compress to fit content; let the document run long.

### Bilingual Support

The layout works under both `dir="ltr"` and `dir="rtl"`.

- Margins flip. Section codes move to the right margin under RTL.
- Headlines remain tight in both languages.
- For Arabic, use `font-family: "SF Arabic", "IBM Plex Sans Arabic", system-ui, -apple-system, sans-serif;`. Latin numerals are acceptable; if Eastern Arabic numerals are used, they are used consistently.
- Line-height under Arabic increases by 4%–8% to accommodate diacritics.
- Test the document under RTL before delivery. Mirrored layout that reads incorrectly is a Critical ship-block under the polaris style.

---

## Required Sections

The default case study has seven sections, in this order:

- (A) About — what the product is and who it is for.
- (B) Mission — the principle that drives the work.
- (C) Outcomes — what was achieved, in numbers where possible.
- (D) Impact — what changed for the user and the business.
- (E) Market — where the product sits and what it competes with.
- (F) Chance — the bet the team made and the constraint it accepted.
- (G) Target Audience — who the product is built for, precisely.

A case study may use a different section set, but the alphabetic codes still march. If a case study has five sections — say About, Process, Outcomes, Lessons, Future — it codes them (A) through (E).

Section titles are noun phrases, set in title case. "About," not "About the product." "Outcomes," not "Our Outcomes." The title is the system; the body is the content.

---

## Voice

The voice is editorial, evidence-led, restrained.

- Third-person where appropriate. First-person plural is acceptable when describing internal process; first-person singular is rare and reserved for the case study's author.
- The verbs are concrete: "shipped," "rebuilt," "measured," "deprecated." Not "leveraged," "drove," "enabled."
- Claims carry evidence. "Redemption rose 41%" not "Redemption rose significantly."
- The voice does not sell. The case study is a report, not a brochure.

Forbidden phrasing:
- "We are proud to announce."
- "Best-in-class."
- "World-class."
- "Game-changing."
- "Disruptive."
- Anything that would read as marketing copy.

Required phrasing:
- Verbs in the past tense for what happened.
- Verbs in the present tense for the product as it exists today.
- Verbs in the conditional for future work.

---

## Image Handling

Photos and screenshots are full-bleed.

- Width: `w-full`, edge-to-edge of the content column at minimum, edge-to-edge of the viewport for hero images.
- No frame, no border, no shadow, no rounded corners. The image sits flat on the page.
- Captions: small italic gray (`text-sm italic text-zinc-500`), set below the image with `mt-4`.
- Captions are short: route, viewport, date. "Member dashboard, mobile, December 2026." That is enough.

If a screenshot has chromatic content, convert to grayscale before placement. This is the case-study rule and only the case-study rule.

Product photos are unframed. Lifestyle photos are unframed. No "device frame" mockups (no laptop chrome, no phone bezel). The image is the artifact.

---

## Typography Stack

Default stack:

```css
font-family: -apple-system, BlinkMacSystemFont, "Inter", "Helvetica Neue", Helvetica, Arial, sans-serif;
```

Inter is acceptable. Serifs are allowed for case studies — unlike dashboards, a case study may set body type in a serif if the design calls for it. Acceptable serifs:

- IBM Plex Serif
- Source Serif Pro
- A locally-licensed editorial serif

If the case study uses a serif for body, headlines remain sans-serif. The contrast is intentional. Mixing serif body with sans-serif display reads as editorial; mixing the reverse reads as a website.

For Arabic, use SF Arabic, IBM Plex Sans Arabic, or a locally-licensed Arabic editorial face. Do not auto-fall-back from a Latin font to a system Arabic; specify the Arabic face explicitly in the stack.

---

## Output Format

The case study is delivered as one of:

- A complete Blade file (`.blade.php`) that renders inside the project's layout.
- A complete HTML file (`.html`) that renders standalone.
- A Markdown document (`.md`) with Tailwind class hints in HTML span tags where the two-tone emphasis is required.

The file is complete and self-rendering. No "fill in the assets later." No "add a header here." The reader opens the file and reads the case study.

When delivering Blade or HTML, include the full document scaffold: `<!doctype html>`, `<html>`, `<head>` with meta tags and Tailwind, `<body>` with `dir="ltr"` set explicitly. For RTL, deliver a sibling file with `dir="rtl"`.

When delivering Markdown, the file renders cleanly in any Markdown previewer. Tailwind class hints are present but degrade gracefully if not interpreted.

---

## Pre-Publish Checklist

Before the case study is delivered, verify every item.

- [ ] Monochrome verified — no chromatic content, no hue with non-zero saturation.
- [ ] Section codes present — alphabetic, in order, no gaps.
- [ ] Hairline separators only — no boxes, no cards, no shadows.
- [ ] Two-tone body emphasis used — black for important phrases, gray for context.
- [ ] No marketing language — no "elevate," "unleash," "seamless," "robust."
- [ ] No source attributions inside the content — no name-checked authorities, no inline citations.
- [ ] RTL tested — document renders correctly under `dir="rtl"` with mirrored margins and section codes.
- [ ] Typography stack specified — Latin and Arabic faces both named.
- [ ] Images are full-bleed, unframed, grayscale.
- [ ] Captions are short, italic, gray.
- [ ] Length is honest — the case study runs as long as it needs to and no longer.
- [ ] No emoji.

A case study that fails any item is rewritten before send.

---

## Length Discipline

A case study is as long as it needs to be. The discipline is not "be short"; the discipline is "no filler."

Targets:
- A product overview case study: 600 to 1,200 words.
- A flow-deep case study: 1,200 to 2,400 words.
- A retrospective or year-in-review: 2,000 to 4,000 words.

If the case study exceeds the upper bound, cut the section that is the most general. The case study earns its length with specificity.

---

## Section Patterns

Each section has a default structure that the writer can override.

### (A) About

One paragraph. Names the product, the market, the launch date, the team size. Two sentences if the product is well-known; three if it needs setup.

### (B) Mission

One paragraph. Names the principle. Not a slogan — the operating principle behind the product. "Phone is the only customer identity." That is a mission. "Empowering merchants" is not.

### (C) Outcomes

A list or a table. Numbers where possible. Each outcome is a single line. No prose around the outcomes — the outcomes are the prose.

### (D) Impact

One or two paragraphs. What changed for the user. What changed for the business. Specific examples, not generalizations.

### (E) Market

One paragraph or a short table. Where the product sits and what it competes with. Honest comparison, not aspirational positioning.

### (F) Chance

One paragraph. The bet the team made — the constraint it accepted in exchange for a specific advantage. "We accepted that we would not support Western markets in year one so we could ship Arabic-first." That is a chance.

### (G) Target Audience

One paragraph. Who the product is for, precisely. Not "small businesses" but "single-location retail merchants in Amman, Riyadh, and Dubai with 1–5 staff and no POS integration prior to onboarding."

A case study that follows these section patterns reads as a system, not a one-off document.

---

## Document Title Block

The title sits alone on the opening view. The reader sees:

- Document title — `text-8xl` to `text-9xl`, `font-medium`, `letter-spacing: -0.045em`.
- One-line subtitle — `text-xl` `text-zinc-500`, set below the title with `mt-8`.
- Date and author — small caps, `text-xs uppercase tracking-widest text-zinc-400`, set below the subtitle with `mt-12`.

Below the title block is `py-48` of breath, then the (A) section begins.

The title block is the only place where the document title appears. It is not repeated in headers, footers, or running heads.

---

## End-of-Document Block

The case study ends with a single hairline followed by a small block:

- A one-sentence colophon naming the production stack ("Set in Inter and IBM Plex Sans Arabic. Built with Tailwind and Blade.")
- The publication date.
- A revision tag if the document has been updated ("Revised 2026-05-24.")

No "thank you for reading." No call to action. No sign-off. The hairline and the colophon are the close.
