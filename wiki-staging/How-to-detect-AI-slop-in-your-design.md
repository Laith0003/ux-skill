# How to Detect AI Slop in Your Design

AI-generated UIs share measurable fingerprints. Inter font as the brand display. Purple-to-blue gradient on white. Three equal cards in a row. "John Doe" and "Acme" as placeholders. Centered hero over a dark image. The `/ux-polish` command catalogues 200+ of these patterns and detects them in any surface.

This page is the field guide. Learn to spot them, run the audit, and clear them before you ship.

---

## Why AI-slop exists

Large language models trained on the web have seen the same UI patterns hundreds of millions of times. When asked to generate a UI without explicit constraint, they sample the highest-probability pattern.

That sampling produces a recognizable aesthetic:

- The same fonts (Inter, Plus Jakarta Sans, Geist)
- The same colors (a few brand purples, a few accent blues, a single emerald success)
- The same layout (centered hero, three columns of features, a CTA band, a footer)
- The same placeholder content (John Doe, Acme Inc, lorem ipsum, "Increase efficiency by 47%")
- The same component library look (rounded-2xl cards, soft shadows, gradient buttons)

The output is not bad. It is generic. And generic, in a competitive market, is invisible.

`/ux-polish` exists to make the default visible so you can override it.

---

## The 8 categories of AI fingerprints

AI-slop falls into eight categories. Each has measurable tells.

1. **Typography** — fonts, sizes, weights, line lengths
2. **Color** — gradients, palette, contrast
3. **Layout** — grids, alignment, hero shapes
4. **Components** — cards, buttons, badges, shapes
5. **Content** — placeholder names, fake brands, filler verbs, round numbers
6. **Interaction** — hover, focus, motion, states
7. **Empty states** — illustrations, copy, calls to action
8. **Information architecture** — navigation, hierarchy, density

The next sections walk through each.

---

## Visual fingerprints

### Typography fingerprints

The single strongest tell that a UI was AI-generated is its typeface.

**The Inter epidemic.** Inter is a great font. It is also the single most-used font in AI-generated UIs because every starter template and every tutorial defaults to it. If you want your product not to look like every other AI-generated landing page on Twitter, do not use Inter as your display face.

**Acceptable substitutes for the AI default stack:**

- Display: a real editorial face (PP Editorial New, Söhne, Mona Sans, GT America, ABC Diatype, Founders Grotesk)
- Body: a humanist sans with character (Source Serif, IBM Plex Sans, Public Sans, Roboto Flex)
- Mono: tabular-numeral mono (JetBrains Mono, Berkeley Mono, IBM Plex Mono, Geist Mono)

**The size-stack fingerprint.** AI defaults to a font-size scale of 12/14/16/18/24/30/36/48/60/72. The numbers are tells. Real design systems use modular ratios (1.125, 1.2, 1.25, 1.333) producing scales like 14/16/18/20/22/26/32/40/52.

**Line-length collapse.** AI body text runs at 50–70 characters per line. That is acceptable for blog posts, not for hero copy. Hero copy at 30–45ch reads as editorial; at 70ch reads as a blog. Set `max-w-[28ch]` on hero headings.

**Weight inflation.** AI loves font-weight 600 (semibold) on body. Body is 400. Semibold is reserved for emphasis. If your body text is semibold, you're at AI default.

**Tracking neglect.** Headlines at 48px+ need negative tracking (`letter-spacing: -0.03em`). AI never adds it, so headlines feel loose and amateurish.

### Color fingerprints

**The purple-to-blue gradient.** The single most recognizable AI tell. `from-purple-600 to-blue-600` or `from-violet-500 to-indigo-600`. Once you see it, you cannot unsee it.

Adjacent tells:

- Pink-to-purple gradient on a "Get started" button
- Cyan-to-blue gradient on a feature illustration
- Orange-to-pink "accent" gradient on a stat card
- A radial gradient blob in the hero background

**The single emerald success.** AI picks the same green: `#10B981` (Tailwind's emerald-500). Real design systems have a state palette tuned to the brand — green that lives in the brand's hue family, not the default.

**Soft-shadow + low-saturation neutrals.** A flat off-white background, low-saturation gray text, and a soft drop shadow on every card. This combination reads as "AI starter."

**Brand-color overuse on chrome.** The brand color appears in the nav, the buttons, the link, the borders, the badges, the focus ring. Real brands restrict the brand color to one or two surfaces — the logo and the primary CTA.

**Dark-mode by inversion.** AI builds light mode and then inverts colors for dark mode. Real dark mode is not an inversion; it is a separate design with different contrast targets, different shadow strategy (often glow instead of shadow), and different accent intensities.

### Layout fingerprints

**The centered hero.** Logo top-left, nav top-right, hero copy centered, single CTA below. This is the highest-frequency layout in the training set and the most AI-recognizable.

**Three equal columns.** Three feature cards in a row, each with an icon, a title, two lines of body. If you have three features that warrant the same treatment, ask whether one of them is actually the primary feature and deserves more space.

**The 80-character body line.** AI lays body copy out to fill the container width. Real editorial work caps at 60–75ch. Long-form at 50–65ch.

**Equal vertical rhythm between sections.** Every section the same height, the same padding, the same heading size. Real designs have a few anchor sections and many supporting sections.

**Centered everything.** Every element centered horizontally. Real layouts use directional alignment for narrative — left-aligned for primary, right-aligned for response, center reserved for true equilibrium moments.

**No asymmetric grids.** AI does not generate asymmetric layouts unless explicitly asked. A bento grid, a magazine layout, an off-axis hero — these never appear in defaults.

### Component fingerprints

**Rounded-2xl on everything.** A consistent 16–24px border radius on every card, every button, every input, every modal. Real design systems use radius as a semantic — small radius for inline elements, medium for cards, large for containers, none for utility surfaces.

**Soft shadow + soft border + soft background.** A card with `shadow-sm`, `border-gray-200`, and `bg-white` on `bg-gray-50` is the canonical AI card. Pick one: shadow, border, or background contrast. Not all three.

**The icon-circle-on-feature-card.** A small icon inside a colored circle, top-left of every feature card. Universal AI pattern.

**Gradient borders.** A 1px gradient border around a card or button to imply "premium." Used so widely it has lost meaning.

**The all-icons icon set.** Every icon from Lucide, every icon at the same size, every icon the same weight. Real products use icons sparingly and from a custom set or a consistent subset.

**Round CTA pills with chevron arrows.** "Get started →" with an arrow on the right of every button.

---

## Content fingerprints

The content is often a louder tell than the visual design.

### The "Jane Doe" effect

Every AI-generated UI has the same set of placeholder names:

- John Doe
- Jane Doe
- Jane Smith
- John Smith
- Sarah Johnson
- Michael Chen
- Maria Garcia

If your product copy ships with any of these, it announces "AI-generated" before the user reads the first sentence.

Replace with names that fit your actual audience. For a MENA product: Ahmad, Layla, Yara, Khalid, Nour. For a US product, use real-feeling combinations that are not on the AI top-20 list.

### Fake brand names

- Acme Inc
- Acme Corp
- Acme
- Globex
- Initech
- TechCorp
- SaaS Co

Replace with real brand names if you have customer permission, or with bespoke fake names that fit your space (a fintech might use "Northwind Financial" instead of "Acme Inc").

### Round-number stats

AI gravitates toward round numbers:

- "Increase efficiency by 47%"
- "Save 10 hours per week"
- "Grow revenue by 3x"
- "Used by 10,000+ teams"
- "99.9% uptime"

These read as fake because they are. Real metrics are weird: "Increased reply rate from 14.7% to 22.3%." "Saved an average of 6h 40m per week across 47 ops engineers." If you can name a real number, use it. If you cannot, do not invent one.

### Filler verbs

- "Streamline your workflow"
- "Unlock your potential"
- "Supercharge your team"
- "Take control of your data"
- "Empower your business"
- "Transform the way you work"

These verbs say nothing. Replace with concrete actions: "Cut ticket triage from 12 minutes to 2." "Stop checking three dashboards. The number that matters is on the home screen."

### Lorem ipsum

If your shipped UI contains "Lorem ipsum dolor sit amet," it is not shipped. Replace every instance. Do not let a single one survive.

### Emoji as decoration

AI loves rainbow flags, sparkles, rockets, lightning bolts, and party poppers. Brand-grade products do not decorate with emoji. Replace with inline SVG icons or remove entirely.

(For the Dot product, no emojis ever, anywhere. This is a hard standing rule.)

---

## Interaction fingerprints

### Decorative motion with no information value

A floating gradient blob behind the hero, slowly drifting. A subtle pulse on every card. A "shimmer" on every button on hover. These do not communicate state; they signal "AI tried to make it feel premium."

Motion should answer a question: "Did the click register?" "Is something loading?" "Is this card hoverable?" If the motion is not answering a question, cut it.

### Missing states

The shipped UI shows the happy path. There is no:

- Empty state (what does a new user see?)
- Loading state (skeleton, spinner, or progress?)
- Error state (what did the user see when the API failed?)
- Disabled state (why is the button gray?)
- Zero-data state (what if the table has no rows?)

The first real-world hit on any of these reveals a broken UI. `/ux-polish` checks for the presence of all five.

### Hover-only affordances

Critical actions revealed only on hover do not work on mobile or for keyboard users. AI often hides "Edit" and "Delete" behind a hover. They should be either always visible or accessed through a clear "More" menu.

### Single hover effect on all interactive elements

Every link, button, card uses the same `hover:opacity-80` or `hover:scale-105`. Real products have distinct hover states tuned to the element: a button changes background, a link underlines, a card lifts.

### No focus-visible

Focus rings missing or set to `outline: none`. Keyboard users cannot tell where they are. This is both a slop tell and an accessibility failure.

```css
/* WRONG */
button:focus { outline: none; }

/* RIGHT */
button:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}
```

---

## The full anti-slop checklist

Run through this list before shipping. Anything yes is a violation.

### Typography
- [ ] Does the display font default to Inter, Plus Jakarta Sans, or Geist?
- [ ] Does body text use weight 600 anywhere?
- [ ] Are headlines under 30px without negative letter-spacing?
- [ ] Is hero copy longer than 45 characters per line?
- [ ] Does the size scale follow the 12/14/16/18/24/30/36/48 default?

### Color
- [ ] Is there a purple-to-blue gradient anywhere?
- [ ] Is success colored emerald-500 (`#10B981`)?
- [ ] Do cards have both a shadow AND a border AND a background tint?
- [ ] Does the brand color appear in more than 3 distinct surfaces?
- [ ] Is dark mode an inversion of light mode rather than a separate design?

### Layout
- [ ] Is the hero centered with a single CTA below?
- [ ] Are there exactly 3 equal feature cards in a row?
- [ ] Is the body copy line length over 75 characters?
- [ ] Are all sections the same height?
- [ ] Is the entire page centered with no left-aligned sections?

### Components
- [ ] Is every container `rounded-2xl` regardless of role?
- [ ] Does every feature card have a colored icon-circle top-left?
- [ ] Does every CTA have a chevron arrow appended?
- [ ] Is there a gradient border anywhere?
- [ ] Are icons from Lucide / Heroicons at default size, default weight?

### Content
- [ ] Does any placeholder name match the AI top-20 list (John Doe, Jane Smith, Sarah Johnson, etc.)?
- [ ] Does any fake brand match the AI list (Acme, Globex, TechCorp)?
- [ ] Does any stat use a round invented number (10x, 47%, 99.9%)?
- [ ] Does any headline use filler verbs (streamline, unlock, supercharge)?
- [ ] Is there any lorem ipsum left?
- [ ] Are there decorative emoji?

### Interaction
- [ ] Are there animations with no information value?
- [ ] Is there a missing empty / loading / error / disabled / zero-data state?
- [ ] Are critical actions revealed only on hover?
- [ ] Is `outline: none` set anywhere without a `:focus-visible` replacement?
- [ ] Is every hover the same effect?

### Accessibility
- [ ] Is text contrast below WCAG AA?
- [ ] Are touch targets under 44x44px?
- [ ] Are form errors color-only (no text)?
- [ ] Are charts color-only with no text summary?
- [ ] Is there no `prefers-reduced-motion` handling?

Any yes is a violation. The audit catches them all.

---

## How to run `/ux-polish` to detect them

The command runs against any file or directory.

```
/ux-polish ./resources/views/landing.blade.php
```

For a directory:

```
/ux-polish ./resources/views/
```

For a remote URL:

```
/ux-polish --url https://example.com/landing
```

The audit produces a structured report with severity tagged per finding.

```
ANTI-SLOP AUDIT — landing.blade.php
====================================

CRITICAL (4)
  L23   Display font is "Inter" — universal AI default
  L48   Purple-to-blue gradient on hero CTA (from-purple-600 to-blue-600)
  L102  Three equal columns with icon-circle pattern
  L156  "Increase your conversion by 47%" — round-number invented stat

HIGH (7)
  L31   Body weight 600 (should be 400)
  L72   Headline 36px without negative letter-spacing
  L94   Card has shadow + border + background tint
  L118  CTA copy ends in arrow chevron ("Get started →")
  L142  "John Doe" placeholder name
  L168  No focus-visible state on .cta
  L182  No prefers-reduced-motion handler

MEDIUM (4)
  L55   Hero copy 78ch (should be 30-45ch)
  L66   Single hover effect across all interactive elements
  L88   No loading state defined
  L201  Brand color used in 5 different surfaces

COSMETIC (3)
  L14   Default size scale (12/14/16/18/24/30)
  L177  Lucide icons at default 24px
  L210  Decorative gradient blob in hero background

Total: 18 findings
Severity: 4 critical, 7 high, 4 medium, 3 cosmetic
Slop score: 67/100 (HIGH — major rewrite recommended)
```

---

## Severity scale

The audit ranks findings on a four-tier scale.

### Critical

Will be recognized as AI-generated within 3 seconds of a user landing on the page. Must be fixed before shipping. Examples:

- Purple-to-blue gradient on primary action
- Inter as the display font on a brand surface
- "John Doe" + "Acme Inc" + lorem ipsum visible on the page
- Round-number invented stats in the marketing copy
- Three equal feature cards above the fold

### High

Recognized as AI-generated by anyone who has built a UI in the last 2 years. Should be fixed. Examples:

- Icon-circle on every feature card
- Chevron arrow on every CTA
- Soft shadow + soft border + soft background combined
- Missing empty / loading / error states
- Body weight 600

### Medium

Not strong tells, but combine with other findings to create a slop impression. Address opportunistically.

- Generic color palette
- Default font size scale
- Decorative drop shadows
- Standard 80ch line length

### Cosmetic

Detected but not high-leverage. Worth fixing if you have time.

- Default icon library at default settings
- Subtle blob backgrounds
- Default font features (no tnum, no ss01)

---

## Common false positives

The audit is aggressive. A few patterns get flagged that may be intentional. Override them with care.

### "Inter is fine for body, just not display."

Inter as body is acceptable. Inter as the display font is the slop tell. If the audit flags Inter on body and you're using a distinct display face, override with the `--allow-inter-body` flag.

```
/ux-polish ./landing.html --allow-inter-body
```

### "Three columns are sometimes correct."

If your product genuinely has three equal pillars (e.g., a marketplace with Buyers / Sellers / Admins), three equal columns is the right layout. The audit flags it because most uses are decorative. Override with `--allow-equal-columns` after confirming.

### "I used emerald on purpose."

If `#10B981` is your brand green, the audit flagging it is wrong. Annotate the file with `<!-- design-system: emerald-500 is brand -->` and the audit will skip the finding.

### "The purple gradient is the brand."

If your brand IS a purple-to-blue gradient (a few real ones exist), confirm with the audit:

```
/ux-polish ./landing.html --brand-gradient "from-purple-600 to-blue-600"
```

The audit will skip that exact gradient but still flag others.

---

## Manual detection — what to look for without the plugin

You won't always run the command. Train your eye.

When a screen comes up:

1. **Look at the type.** Is it Inter? Plus Jakarta? Is the headline loose (no tight tracking)? Is the body in semibold?
2. **Look at the gradients.** Purple-to-blue? Pink-to-purple? Cyan-to-blue?
3. **Look at the hero.** Centered? Single button? Is there a chevron on the button?
4. **Look at the feature section.** Three equal cards? Icon-circle top-left of each?
5. **Look at the copy.** Any "streamline," "unlock," "supercharge"? Any round-number stat? Any "John Doe"?
6. **Look at the states.** Is there an empty state visible? Click a button — does it have a focus ring?
7. **Look at the motion.** Is there decorative motion that adds no information?
8. **Look at the dark mode.** Is it just an inversion?

Six minutes of inspection catches 80% of the slop. The audit catches the remaining 20% and quantifies the score.

---

## Real before / after

A landing page submitted to audit:

**Before:**
- Font: Inter for everything
- Hero CTA: gradient `from-purple-600 to-blue-600` with "Get started →"
- Three equal feature cards, each with a Lucide icon in a colored circle
- Body: weight 600, line length 80ch
- Stat: "Trusted by 10,000+ teams"
- Testimonial: "Jane Doe, CEO of Acme Inc"
- No empty / loading state
- Slop score: 78/100

**After (post `/ux-polish --fix`):**
- Display font: PP Editorial New. Body: Roboto Flex. Mono: JetBrains Mono.
- Hero CTA: solid black on white, no gradient, no chevron, label "Start"
- Asymmetric layout: one anchor feature with a large surface, two supporting features at 40% width each
- Body: weight 400, line length 60ch
- Stat: removed entirely (no real data to back it)
- Testimonial: removed pending real customer quote
- Empty state added: "Nothing here yet. Create your first record."
- Loading state added: skeleton matching the hero height
- Slop score: 12/100

The audit's job is to make the default visible. Your job is to override it with constraint and specificity.

---

## Next steps

- For dashboards specifically, see [How to design a dashboard with Claude Code](How-to-design-a-dashboard-with-Claude-Code)
- For motion that does not become its own slop tell, see [How to add motion that doesn't break Core Web Vitals](How-to-add-motion-that-doesnt-break-Core-Web-Vitals)
- For the full pipeline from default to human-grade, see [How to make AI output look human-grade](How-to-make-AI-output-look-human-grade)
- For case-study output, see [How to ship a case study from product data](How-to-ship-a-case-study-from-product-data)

---

**Plugin repo:** https://github.com/Laith0003/ux-skill
**Author:** Laith Aljunaidy — https://www.linkedin.com/in/laith-aljunaidy/
**License:** MIT
