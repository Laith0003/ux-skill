# Premium SaaS Patterns (batch 1)

A synthesized pattern library distilled from studying current high-end SaaS marketing surfaces.
Patterns here are reusable building blocks: the language of "what premium B2B looks like in 2026."
Use as inspiration, not prescription — pick what fits the brand, leave what doesn't.

---

## Typography patterns observed

### Display headlines

- **Hero-scale display headlines in the 48-72px range, weight 700-800.**
  - The page's first impression carries the entire value proposition in one or two short lines.
  - Headlines are short enough to break across at most two lines on desktop (under ~50 characters per line).
  - Use this when the value-prop needs to land in under two seconds of scanning.
  - Sub-pattern: when the headline is two sentences ("Stop X. Start Y."), each sentence gets its own line.

- **Tight headline tracking (-0.01em to -0.02em) on large display sizes.**
  - At 48px and above, optical kerning needs a nudge inward.
  - This is one of the cheapest moves that separates polished from amateur.
  - Body text stays at default tracking — over-tracked body reads dated.

- **Headlines use a tight line-height (1.0-1.15).**
  - Pairs with looser body line-heights to create vertical contrast between display and reading text.
  - Each headline line should feel like a single "block" of weight, not a loose stack.

### Font stack choices

- **Sans-serif system stacks dominate.**
  - Inter, system-ui, -apple-system, Geist, or near-equivalents are the working palette.
  - Custom display typefaces are rare on this tier; discipline is in scale and rhythm, not in font novelty.
  - This works because the typography reads as competent and unforced — premium fluency, not premium decoration.
  - Serif typefaces are occasionally used for a single editorial flourish (testimonial pull-quotes) but never as the body or display family.

- **Monospaced numerals for metrics and step numbers.**
  - When a section uses "01 / 02 / 03" sequencing, or when stats appear inline ("280K documents/day," "60% reduction"), the numerals lock into a tabular or monospaced variant.
  - This signals data-fluency and adds a "platform engineering" edge.
  - Use a mono like JetBrains Mono, Geist Mono, or IBM Plex Mono for callouts; never as body text.

### Weight & hierarchy

- **A 3- to 4-step weight hierarchy.**
  - Typically a single bold display weight (700-800) for headlines.
  - A medium (500-600) for subheads and feature titles.
  - A regular (400) for body.
  - Italic and light weights are rare. Restraint is the move.

- **Numbered callouts rendered as a separate, heavier weight than the label below them.**
  - The digit dominates ("60%" in bold display).
  - The qualifier sits in lighter weight underneath ("fewer unqualified calls").
  - Use for stat-card components in trust strips and outcome sections.

### Spacing & rhythm

- **Generous line-height on body text (1.5-1.7).**
  - Never tight on paragraphs.
  - Pairs with tight headline line-heights (1.0-1.15) to create vertical contrast.

- **Slight letter-spacing on small caps and eyebrow labels (0.05em to 0.12em).**
  - Small-caps eyebrows ("PLATFORM," "VOICE AGENT," "USE CASE") get gentle tracking.
  - Body and headlines stay at default tracking — over-tracked headlines look 2015.

- **Eyebrow labels are 12-13px small caps in mid-gray.**
  - They orient the reader without taking visual weight.
  - Placed above the section headline, never below.

---

## Color & contrast patterns

### Canvas & ink

- **Light-mode default, near-white background, near-black text.**
  - The dominant palette is a neutral light canvas (#FFFFFF to #FAFAFA).
  - Primary text in a near-black (#0A0A0A to #1A1A1A), not pure black.
  - The slight desaturation softens the contrast and reads less like a 1995 document.

- **Mid-grays carry the supporting load.**
  - Secondary text in the #6B7280 to #71717A range.
  - Tertiary labels in #9CA3AF.
  - Dividers at ~#E5E7EB hold structure without shouting.
  - Use the gray ramp as a vertical depth ladder: darker = more important.

### Accent strategy

- **Single restrained accent color.**
  - A single brand chromatic — often a saturated blue, green, teal, or violet.
  - Appears exclusively on primary CTAs, key icons, and small marker dots.
  - Accent never becomes a wash; it's a needle in a haystack.
  - If a second accent is needed (for data-viz), it lives only inside product imagery, not in marketing chrome.

- **Multi-stop gradients used sparingly as section dividers or background washes.**
  - A soft horizontal gradient on a single hero or feature section can read as premium when the rest of the page is flat.
  - More than two gradient sections in a single page reads cheap.
  - Gradients use 2-3 stops max; rainbow gradients are out.

### Data & semantic color

- **Semantic color for data, not decoration.**
  - Green for "up / positive / completion."
  - Red or amber for "down / risk / requires attention."
  - When a dashboard or product screenshot appears, the green-up / red-down convention is preserved even in the marketing imagery.
  - This signals fluency with the actual product surface.

- **Compliance and trust badges in mono-color.**
  - SOC 2, ISO, GDPR, CASA badges appear in single-color (grayscale or accent-tinted) treatments rather than their official rainbow logos.
  - This keeps the trust signals from competing with the brand.
  - Cluster them in a tight row, low in the page, before the final CTA.

### Section background shifts

- **Section anchors via subtle background-color shifts.**
  - Three to four micro-shades of off-white (#FFFFFF → #FAFAFA → #F4F6FA) differentiate sections without harsh borders.
  - The page feels structured without feeling segmented.
  - Reserve true-black or true-dark sections for one moment per page (often the final CTA or a single bold feature).

---

## Layout & hero patterns

### Hero composition

- **Hero is a single composition: headline + one sub-paragraph + one or two CTAs + one product image or motion.**
  - No carousel, no slideshow, no rotating taglines.
  - One claim, one supporting line, one call to action.
  - Premium pages don't hedge.

- **Asymmetric hero with product image right-aligned, copy left-aligned (or reversed).**
  - The product screenshot or animated GIF anchors one half of the hero.
  - The text the other.
  - The image is a real screen, not an abstract illustration.

- **A "headline / sub / two CTAs" stack: primary action filled, secondary action ghost or text-link.**
  - "Book a demo" (filled) + "See how it works" (ghost) is the canonical pair.
  - Two filled CTAs of equal weight is an anti-pattern — it dilutes the primary path.

### Section padding & breathing room

- **Generous vertical section padding (96-160px on desktop).**
  - Sections breathe.
  - Anything under 64px between major sections reads as a wall of content.
  - The whitespace is the design.

- **Horizontal max-width of 1200-1280px for content, edge-to-edge for backgrounds.**
  - Backgrounds (gradients, color washes) stretch full viewport width.
  - Text and imagery stay constrained inside a max-width.
  - This creates the "framed inside infinite canvas" feel.

### Social proof & feature grids

- **A logo strip immediately after the hero, single row, monochromatic.**
  - 6-10 customer logos in a single grayscale or monotone treatment.
  - Often with a small eyebrow ("Trusted by teams at," "Used by").
  - The logos themselves are the credibility — no copy needed.

- **3-column or 2x3 feature grids with consistent card structure.**
  - Icon (or numeral) + short title (4-6 words) + 1-2 sentence description.
  - Cards inside a section never vary in structure within the same row.

- **Bento-style asymmetric grids for "platform / capabilities" sections.**
  - One tall card, one wide card, two square cards.
  - Varied sizes with consistent treatment.
  - Use when a single grid needs to show feature breadth without visual monotony.

### How-it-works sequences

- **A "how it works" section as a 3-5 step numbered sequence.**
  - Each step gets its own row or column with a number, a title, and a screenshot or icon.
  - The sequence implies inevitability: do step 1, get step 5.
  - This is one of the most consistently-used moves across premium B2B pages.
  - Numbers use the monospaced/tabular figure variant for engineering feel.

### Page close

- **The page ends with a quiet, final CTA section.**
  - Usually a one-line restated value-prop and a single filled CTA, centered.
  - On a slightly tinted background or full-dark band.
  - No FAQ noise after it, no email capture wall.

- **FAQs (when present) live above the final CTA, not below it.**
  - Questions are the last-objection handler.
  - The final CTA closes after objections are addressed.

---

## Imagery patterns

### Product-first imagery

- **Real product screenshots dominate over decorative illustration.**
  - The canonical hero image is the actual UI — a dashboard, a workflow, a chat interface.
  - Marketing illustration is rare and almost never primary.
  - The product is the product.

- **Screenshots are cropped close, with extreme detail visible.**
  - Not the whole app at 30% zoom — a tight crop on the specific feature being discussed.
  - With real-looking data inside it (real-sounding company names, plausible numbers, realistic timestamps).
  - Lorem ipsum inside a product shot is amateur.

- **Soft drop shadow + subtle rounded corners on product images.**
  - 12-24px corner radius.
  - Shadow at low opacity and high blur (e.g., box-shadow: 0 24px 64px rgba(0,0,0,0.08)).
  - The screenshot floats above the page without harsh edges.

### Motion in imagery

- **Animated GIFs or short looping MP4s in the hero.**
  - 2-4 second loops showing a single interaction.
  - A button being clicked, a chart updating, a workflow advancing.
  - Looping motion outperforms static screenshots for time-on-page.
  - Loop seamlessly — visible cut-and-restart is amateur.

- **Continuous, slow ambient motion on hero illustrations.**
  - A slow rotating gradient, a chart that gently animates, a token sliding across a connection.
  - Subtle enough that you only notice it on a second look.

### Decorative imagery

- **Decorative geometric assets (dots, gradients, abstract shapes) as background ornament.**
  - Not foreground content.
  - Low contrast, low opacity, often anchored to corners.
  - They add visual rhythm without competing for attention.

- **A subtle dot-grid or fine-line pattern as the background of one or two sections.**
  - Visible only on inspection, but it gives the page a "spatial" feel.
  - Like the design is plotted on a working grid.

- **Decorative hand-drawn or geometric corner ornaments.**
  - Low-key, asymmetric, anchored to one or two corners of a section.
  - Adds personality without compromising premium feel.

### People & testimonials

- **Headshot circles for testimonials, square or rounded-square cards for the testimonial body.**
  - Face + name + title + one-line affiliation.
  - Photos are professional but not corporate-stiff.
  - If a real photo isn't available, omit the photo — never substitute a generic avatar.

- **No stock photography of laptops, lightbulbs, or handshakes.**
  - Premium B2B has retired the stock-photo lifestyle shot.
  - If a human appears at all, it's a real customer headshot, not a model.

---

## Motion language

### Page-level motion

- **Auto-scrolling logo marquees that loop seamlessly.**
  - Client logo strips scroll horizontally on infinite loop.
  - Often duplicated 2-3x in the DOM to mask the loop seam.
  - Speed is slow (30-60 second full cycle).

- **Scroll-triggered fade-and-rise on section entry.**
  - As a section enters the viewport, its contents fade in and translate up 12-24px over 400-600ms.
  - Once is enough — repeating on every scroll back up is annoying.

- **Subtle parallax on background ornaments, never on text.**
  - Decorative shapes can drift at 0.5-0.7x scroll speed.
  - Text never moves independently of its container.

### Interactive motion

- **Hover lifts on cards (translateY -2 to -4px) with shadow elevation.**
  - Cards rise slightly on hover, shadow deepens.
  - 200-300ms ease.
  - Never on every element — reserved for clickable cards and primary CTAs.

- **CTA buttons get a subtle background-color or background-gradient shift on hover.**
  - No scale animations on CTAs (looks toy-like).
  - Color or shadow shift only.
  - Active/pressed state: slight darken or inset shadow.

### Numerical motion

- **Animated counters for hero metrics.**
  - "0 → 280,000" counting up over 1.5 seconds on entry.
  - Use sparingly, and only when the number is the proof.
  - Two or three counters max per section; more becomes noise.

### Motion don'ts

- **Avoid page-scroll-hijacking.**
  - Hijacking the scroll wheel to force a horizontal narrative reads dated and accessibility-hostile.

- **Avoid full-screen video autoplay with sound.**
  - Violates user expectation.
  - If video is used, it loops silently as background ambience and never demands the user.

- **Avoid big animated number sequences as decoration.**
  - Counters that aren't anchored to a real metric feel like a gimmick.

- **Reduced-motion respect.**
  - Every motion above should honor `prefers-reduced-motion`.
  - Premium signals fluency with accessibility, not flashy disregard for it.

---

## Content voice patterns

### Headline construction

- **Headline structure: imperative verb + concrete outcome.**
  - "Stop reading documents. Start making decisions."
  - "Run an entire company with agents."
  - "Replace manual work with automated workflows."
  - The verb does the heavy lifting; the noun phrase grounds it.

- **Problem-then-solution two-line construction.**
  - Many headlines are two short sentences.
  - One names the friction, one names the resolution.
  - "Old approach is broken. New approach is here."
  - Cadence over completeness.

- **Subhead immediately quantifies or specifies.**
  - The line under the headline names a measurable outcome.
  - "21x faster," "60% reduction in unqualified calls," "from days to minutes."
  - Numbers do more persuasion than adjectives.

### CTA copy

- **Action-verb CTAs that name the next concrete step.**
  - "Book a demo," "Start free," "See it in action," "Get started."
  - Avoid "Learn more" — it's a verb of inaction.
  - "See how" is acceptable when paired with a specific concrete noun ("See how teams ship in days").

### Testimonial framing

- **Customer quotes lead with the result, not the praise.**
  - "We cut review time by 40%" beats "The team loves it."
  - Premium testimonials are case-study fragments, not vibes.
  - Quote attribution: name, title, company. No "Software Engineer" without a company.

### Feature naming

- **Feature names that are nouns or noun-phrases, not adjectives.**
  - "Workflows," "Agents," "Connectors," "Hidden Profile."
  - Not "Powerful Workflows," "Smart Agents."
  - Naming a thing makes it real; describing a thing makes it brochure.

### Specificity over hyperbole

- **Avoid hyperbolic adjectives ("amazing," "world-class," "revolutionary").**
  - They signal weakness in the underlying claim.
  - The strongest premium copy is the most matter-of-fact ("Zero compromises." "Built for finance.").

- **Use specificity as the credibility lever.**
  - Name a customer, a metric, an integration, a date, a regulation.
  - Concrete proof beats abstract benefit.

### Microcopy conventions

- **Microcopy is calm, never celebratory.**
  - Success states say what happened ("50 points added").
  - Not how the user should feel ("Congratulations! You earned 50 points!").

- **Empty states explain the path forward, not the absence of content.**
  - "Connect your first integration to start" beats "No data yet."
  - Premium products assume the user is smart and just needs the next move named.

- **Error messages name the field and the action to take.**
  - "Phone number missing — add a number to continue" beats "Form contains errors."
  - Always specific. Always actionable.

- **Confirmations narrate state changes.**
  - "Phone verified." "Profile saved." "Connection paused."
  - Short, declarative, no enthusiasm.

---

## Section flow / IA patterns

The canonical premium B2B page IA, in observed order:

1. **Hero.**
   - One-line value-prop + one-line sub + one or two CTAs + product image or short motion.
   - Above the fold on a 1440x900 viewport with room to spare.

2. **Social proof strip.**
   - Logo marquee of customers, single row, monochrome.
   - Immediately after hero.
   - No copy, just logos. (Optional eyebrow: "Trusted by teams at.")

3. **Problem framing / "the old way vs. the new way."**
   - A short section that names the friction users experience today.
   - Sometimes a side-by-side comparison table.
   - Sometimes a single block of "Before" text and "After" text.

4. **Core feature pillars (3-4 of them).**
   - Each pillar is a row with screenshot + headline + 2-3 bullet outcomes.
   - Alternating image-left, image-right for visual rhythm.

5. **"How it works" — numbered step sequence (3-5 steps).**
   - Each step has a number, title, short description, and a small visual.
   - Steps imply inevitability and reduce perceived complexity.

6. **Use-case / industry / persona section.**
   - Shows the platform applied to different contexts.
   - Often as a tabbed switcher or a carousel of persona cards.

7. **Outcome / ROI section.**
   - Customer quote + headline metric (e.g., "21x faster" or "$3M saved").
   - One or two anchor case studies, not a wall of quotes.

8. **Trust & security section.**
   - Compliance badges (SOC 2, ISO, GDPR, etc.) + a short paragraph on security posture.
   - Usually before the final CTA, after objections are otherwise resolved.

9. **FAQ section (optional).**
   - 5-8 questions, accordion-collapsed by default.
   - Lives above the final CTA.

10. **Final CTA section.**
    - Restated value-prop in one line.
    - Single filled CTA.
    - Lives on a tinted-background band that visually separates it from the footer.

11. **Footer.**
    - Navigation + secondary links + small print.
    - No marketing, no surprises.

### AIDA mapping

- **Attention**: hero.
- **Interest**: problem framing + core feature pillars.
- **Desire**: how it works + ROI + customer outcomes.
- **Action**: final CTA.
- **Trust/security pre-empts Desire-to-Action objections** — placed deliberately just before the close.

---

## Distinctive techniques worth stealing

### Structural moves

- **The "before / after" feature comparison table.**
  - Two-column comparison that names the old way on the left and the new way on the right.
  - Each row is a single dimension.
  - Reads as honest and quantifiable.

- **The mid-page "still have questions?" deflector.**
  - A small CTA block in the middle of the page.
  - Catches users who've already decided to dig deeper before the final close.
  - Pairs well with FAQ links.

- **Numbered chapter framework as a learning ladder.**
  - Framing the product surface as "Chapter 1: Start. Chapter 2: Build. Chapter 3: Sell. Chapter 4: Scale."
  - Positions the product as a journey, not a feature pile.
  - Implies the user grows with the product.

- **Repeating the customer logo strip 2-3x within a single page.**
  - Appears once after the hero, once mid-page, once before the close.
  - Compounds the trust signal without overloading any one section.

### Inside the hero

- **Hero metric callouts that quantify scale.**
  - "$3.6T AUM," "280K documents/day," "15K agents."
  - These are credibility punches placed inside or just below the hero.
  - They imply that the platform has been tested at scale.

- **The "Built for [vertical]" subhead.**
  - A small line under the hero ("Built for finance," "Built for sales teams").
  - Immediately tells the reader whether they're in the right place.
  - Reduces bounce; pre-qualifies.

- **Animated metric counters in hero stats.**
  - Numbers tick up from 0 on entry.
  - Restrict to 2-3 stats max; more dilutes the effect.

### Inside the product imagery

- **Approval-state UI in product screenshots.**
  - Showing "Agent requires approval" or "User task" badges inside the product imagery.
  - Communicates "human-in-the-loop" visually rather than verbally.
  - Cheaper than a paragraph of trust copy.

### Demonstrating breadth

- **The "industries carousel" small-caps marquee.**
  - A fast-scrolling row of category labels ("PLATFORM. VOICE AGENT. CRM. PAYMENTS. INVENTORY.").
  - Demonstrates platform breadth in 2 seconds.
  - Pairs with a static hero.

- **A single anchor case study with a real customer name and number.**
  - One customer, one outcome, one screenshot.
  - More memorable than 12 unattributed quotes.

### Surface decoration

- **Custom illustrations that share the brand accent color.**
  - When illustration is used at all, it picks up the single brand accent.
  - Page palette stays disciplined.

- **The "we build alongside you" service line.**
  - Positioning the company as a hands-on partner rather than a self-serve tool.
  - Works when the price point justifies it.
  - Avoid when the product is genuinely self-serve.

---

## Anti-patterns observed

- **Pure prose hero (no visual).**
  - Text-only heroes feel like blog posts, not product pages.
  - Always pair the headline with a visual anchor — a screenshot, a motion, a diagram.

- **Static screenshots that show too much.**
  - A full-app screenshot at 30% zoom is unreadable.
  - Signals "we don't know what's important."
  - Crop to the feature being discussed.

- **Generic stock photography of meetings, laptops, charts.**
  - Instantly downgrades premium perception.
  - Replace with real product UI or remove entirely.

- **Five+ CTAs in the hero.**
  - "Book demo," "Start free," "Watch video," "Read docs," "Talk to sales" — a paralysis cluster.
  - One primary, one secondary, no more.

- **Auto-playing hero video with sound.**
  - Violates user expectation.
  - If video is used, it loops silently as background ambience.

- **Long testimonial walls (15+ quotes).**
  - Noise.
  - 2-3 strong, named, quantified quotes beat 15 vibes-only ones.

- **Animated scroll-jacking.**
  - Hijacking the scroll wheel to force a horizontal narrative reads dated.
  - Accessibility-hostile.

- **CTA copy that says "Learn more."**
  - Tells the reader they should expect to read more, not act.
  - Replace with a verb of intent.

- **Inconsistent card structure within a single feature grid.**
  - Some cards have icons, some don't; some have buttons, some don't.
  - The grid breaks visually.
  - Inside a row, all cards must share one anatomy.

- **Compliance badge logos in full color.**
  - Forces the eye to break from the brand palette.
  - Render in single-color or grayscale.

- **Multiple gradient sections in a single page.**
  - Makes the page feel uncertain about its own palette.
  - One gradient feature, max.

- **Emojis in headlines, microcopy, or product UI.**
  - Reads as casual / Web2 / startup-stage.
  - Premium B2B uses inline SVG icons (Lucide, Feather, Phosphor) or text only.

- **Hyperbolic adjective stacks ("powerful, intelligent, transformative").**
  - Signals weakness in the underlying claim.
  - Replace adjectives with specifics.

- **Form fields that ask for too much in the first interaction.**
  - A "Book a demo" form with 10 fields scares off serious prospects.
  - 3-4 fields is the ceiling.

---

## Voice + tone takeaways

### Register

- **Calm confidence is the default register.**
  - Premium B2B doesn't shout. It states.
  - Two sentences usually finish the thought. One if you can land it.

- **Avoid first-person plural marketing copy in headlines ("We help you...," "We believe...").**
  - Address the reader directly or describe the outcome.
  - "We" comes later, in trust copy and the about section.

- **The product's name shows up in copy sparingly.**
  - Premium copy refers to "the platform," "your team," "the workflow."
  - Constant self-naming reads insecure.

### Value-prop framing

- **Outcome > capability > feature.**
  - "Decisions faster" (outcome) beats "AI reads documents" (capability) beats "OCR engine" (feature).
  - Push every line up the abstraction ladder.

- **Numbers carry more weight than adjectives in headlines.**
  - "21x faster" persuades; "blazingly fast" doesn't.

### Headline patterns

- **The "Stop X. Start Y." headline pattern is durable.**
  - Useful when there's a clear behavioral shift the product enables.
  - Don't overuse — once per page.

- **The "Run an entire [thing] with [novel approach]" headline.**
  - Implies scale and novelty in one breath.
  - Works for category-defining products.

- **The "Replace [old way] with [new way]" headline.**
  - Direct, oppositional, frames the product as inevitable.

### Microcopy conventions

- **Microcopy is operational, not emotional.**
  - "50 points added" not "Awesome — you earned 50 points!"
  - The system stays calm even when the user is celebrating.

- **One-line empty states.**
  - "Connect your first source to start."
  - Premium products assume the user is smart and just needs the next move named.

### Punctuation discipline

- **No exclamation points outside of UI delight micro-moments.**
  - Even then, sparingly.
  - Exclamation marks in marketing copy now read as small-startup energy.

- **Active voice across all surfaces.**
  - "Agents handle the call" beats "The call is handled by agents."

### Eyebrow labels

- **Eyebrow labels in small caps name the conceptual category.**
  - "PLATFORM" "USE CASE" "INTEGRATION."
  - Tiny labels above headlines that orient the reader without taking visual weight.

- **CTAs are imperatives on the user's behalf, not commands at the user.**
  - "See the platform" beats "Click here."
  - The user gets to do something, not is told to do something.

---

## Composition principles to internalize

- **The brief is the spec.**
  - Premium pages are short.
  - If a section can be cut without losing the value-prop, cut it.
  - The discipline isn't what to include — it's what to leave out.

- **One claim per section, one section per claim.**
  - Don't make a single feature section try to do three things.
  - Spawn another section.

- **Visual rhythm via alternation.**
  - Image-left, image-right, full-width, image-left.
  - Keeps the eye moving.
  - Prevents the page from reading as a single slab.

- **Whitespace is a design element, not a deficit.**
  - A section with 160px of vertical padding above and below tells the reader "this section matters."
  - Cramming sections together flattens hierarchy.

- **Premium is the absence of decoration that doesn't carry weight.**
  - Every shape, color, animation, and word should be doing a job.
  - If something is just there to fill space, delete it.

- **Trust signals stack progressively through the page.**
  - Logos (hero proximity) → quantified outcomes (mid-page) → security/compliance (pre-CTA).
  - By the time the user reaches the final CTA, every objection should be at least lightly addressed.

- **The product image is the product.**
  - The most persuasive thing on a B2B page is a screenshot of a thing that obviously works.
  - Treat product imagery as the headline's twin, not as decoration.

- **Consistency across surfaces signals fluency.**
  - The homepage, pricing page, product page, and docs should share typography, spacing, color, and voice.
  - Inconsistency reads as immaturity.

---

## When to apply each pattern

- **Animated counters**: when the metric is the proof. Skip when the number is incidental.
- **Numbered "how it works"**: when the product has a clear onboarding arc. Skip if it's a single tool with no sequence.
- **"Before / after" comparison**: when there's a clear status-quo competitor to displace. Skip in greenfield categories.
- **Logo strip**: when 6+ recognizable customers can be named. Skip with 3 logos — looks thin.
- **Bento grids**: when 5-8 distinct capabilities need showcasing. Skip for 3 — looks underbuilt.
- **Chapter-framework narrative**: when the product is large enough to feel like a journey. Skip on single-purpose tools.
- **Ambient hero motion**: when the page is otherwise quiet. Don't stack motion on motion.
- **Compliance badges**: when procurement teams will ask. Skip on consumer-facing surfaces — reads as enterprise-cosplay.
- **Gradient background section**: once per page, at the section that matters most.
- **Mid-page "still have questions" deflector**: on long pages. Skip on short pages — the final CTA does the job.

---

## Component anatomy notes

- **Primary CTA button**: filled brand-accent background, 14-16px font at weight 500-600, 12-16px vertical / 24-32px horizontal padding, 8-12px corner radius. No icon by default; small right-arrow acceptable when the action implies "go to new context." Hover darkens background ~10% or adds shadow. Active: slight inset or 1-2px translateY.
- **Secondary CTA / ghost button**: transparent or light-tinted background, optional 1px mid-gray border. Same dimensions as primary. Hover fills with low-opacity tint of brand accent or light gray.
- **Feature card**: 24-32px internal padding, 12-16px corner radius, subtle border or low-opacity shadow. Icon at top (24-32px), title below (18-20px, weight 600), description (14-16px, regular). Hover lifts -2 to -4px with shadow elevation.
- **Testimonial card**: pull-quote at 18-22px in slightly muted weight. Attribution line: name (semibold) + title (regular, mid-gray) + company (regular, mid-gray). Optional headshot circle 48-64px diameter to the left.
- **Stat callout**: display-weight number (48-64px, bold, monospaced or tabular figures), qualifier label below (14-16px, regular, mid-gray). Three or four per row, equal spacing.

---

## Sites that didn't return

One source out of five failed to fetch (connection error). Patterns above are synthesized from the four successful fetches; the missing source's specific moves are not represented but the pattern library is broad enough to stand without it.
