# Landing page playbook

The surface playbook for marketing pages. `/ux-design` loads this file, and no other surface playbook, in page mode when the page explains, sells or converts. It holds every rule that is specific to landing pages: layout archetypes, the five compositions the engine chooses from, section flow, hero, header, proof, pricing, CTA, footer, and Arabic and RTL delivery. Cross-surface rules (color, type, spacing, motion, content, responsive mechanics, component contracts) stay in `references/styles/anti-slop.md`, `references/styles/arsenal.md` and `references/foundations/`; a landing page with a form or a comparison table also reads the contracts in `references/foundations/component-behaviors.md`.

---

## When it applies

Load this playbook when the brief asks for a page whose job is to explain, sell or convert:

- A product, SaaS or app landing page, a homepage, a launch page, a waitlist page.
- A service or local-business page whose conversion is a call, a quote or a booking.
- A campaign page, a pricing page, a "why us" page, a product tour page.

Do not load it for a dashboard, an admin tool, a signed-in app screen, a single component, documentation or a portfolio gallery. Those use `references/surfaces/dashboard.md`, `references/surfaces/component.md`, or no playbook.

Discovery asks landing briefs for their sections in order (`references/process/discovery-protocol.md`). When the answer is "trust the default", the archetype and the section flow below set the order.

---

## Layout archetypes

Pick one archetype per page and commit to it. Each one is a complete skeleton. Mixing two skeletons on one page produces the composition fingerprint: a page that could belong to any product.

### 1. Split-hero product page

**Structure.** Asymmetric 7/5 hero (copy on one side, real product UI on the other). A monochrome logo wall directly under the hero. Three to five marquee feature sections, each a 7/5 or 5/7 mosaic that alternates sides. One proof band with named, quantified quotes. A pricing teaser line. A final high-contrast CTA band. A sitemap footer.
**Pick it when.** The product has a real interface worth showing and the audience evaluates by looking at it: SaaS, productivity tools, fintech apps.
**It fails when.** It collapses into the default reach: centered or 50/50 hero, left-text-right-image repeated in every section, a row of three equal cards under the hero. The asymmetry is the whole point; a 6/6 split is a different, weaker page.

### 2. Thesis statement

**Structure.** A centered, single-line display headline. Two to four sentences of body-size prose under it. One CTA with at most one secondary link. Then long-form argument sections, a before and after panel, a short proof band, and a closing CTA that restates the thesis.
**Pick it when.** The brand voice is the product: editorial positioning, AI and research products, a company with a point of view to argue.
**It fails when.** The archetype is picked by default rather than deliberately, which breaks the centered-hero rule: Centered hero only when DESIGN_VARIANCE is 4 or below, or when the archetype is Thesis statement or Cinematic brand and was chosen deliberately. It also fails when the H1 wraps past three lines, or the hero grows a toolbar of buttons. A thesis page with no argument under the hero is a slogan, not a page.

### 3. Product demo led

**Structure.** The hero is the product itself: an interactive demo, a large product mock, a code block or a terminal. Under it, a scroll-pinned product walk through three or four states, a bento of five to eight capabilities, a monochrome logo wall, and a final CTA that repeats the command or the signup.
**Pick it when.** The product is visual or temporal and 60+ seconds of engagement justify the build cost. Developer tools, creative tools, AI products whose output is the proof.
**It fails when.** The "demo" is a video loop dressed as interactivity, the demo blocks first meaningful paint, or three premium effects stack on one screen (tilted window, parallax background, scrubbed video).

### 4. Editorial long form

**Structure.** Sections read as magazine spreads: text-left and image-right, then text-right and image-left, then an occasional full-bleed image. Cards inside sections are deliberately not identical. The grid is felt but not enforced. The alternation is the rhythm. A chapter narrative runs top to bottom and ends in one CTA.
**Pick it when.** The page is story-led or content-led: a product large enough to feel like a journey, a brand story, a manifesto, a long product explainer.
**It fails when.** Every section keeps the same orientation, sections carry decorative "SECTION 01" labels, or chapter framing is applied to a single-purpose tool with nothing to narrate.

### 5. Single-field conversion

**Structure.** The hero's primary CTA is one input and one button, replacing a "Sign up" button. The hero copy implies the field is the start. Under it: a short proof strip, three feature sections, a FAQ, and the same single field repeated in the final CTA band.
**Pick it when.** The conversion is one field: signup-led products, waitlists, fintech onboarding where the implied promise is "this is one field, not a multi-step funnel."
**It fails when.** The form asks for more than the one field, a separate hero button scrolls to the field that is already on screen, or the page has no proof and the field reads as a data grab.

### 6. Cinematic brand

**Structure.** A full-bleed image or muted video with a dark radial wash. Centered statement, exactly two high-contrast CTAs. Image-led sections below: lifestyle photography at 4:5 or near-square, one product detail section, a short story, a closing CTA.
**Pick it when.** Imagery carries the value: premium consumer products, hospitality, hardware, brand-led launches with real photography.
**It fails when.** The archetype is picked by default rather than deliberately, which breaks the centered-hero rule: Centered hero only when DESIGN_VARIANCE is 4 or below, or when the archetype is Thesis statement or Cinematic brand and was chosen deliberately. It also fails when the text sits on the image without a legible scrim, or the imagery is generic stock that could advertise anything.

### 7. Service lead generation

**Structure.** The quote or contact form lives in the hero. A proof and stats bar under it. Trust signals (ratings, accreditations, years in business) and a visible phone affordance. Service or coverage cards with real backdrop images. A FAQ. A final CTA that points back to the form. This is the `lead-gen-service` page sequence in the engine.
**Pick it when.** The business sells a service and the conversion is a call, a quote or a booking: trades, clinics, local services, agencies.
**It fails when.** The ratings bar stacks into a tall sticky block, a hero button scrolls to the form that is already visible, or every service card carries the same icon.

### Pattern pairings by brief

| Brief | Archetype | Patterns |
|---|---|---|
| Modern SaaS landing | Split-hero product page | Asymmetric split hero + bento grid + spotlight border cards + perpetual micro-interactions |
| AI product landing | Thesis statement | Thesis-statement hero + before/after panels + command input demo + magnetic button + mesh gradient bg |
| Developer-tooling landing | Product demo led | Code-as-design hero + terminal mockup + monochrome logo wall + keyboard chips + status indicator |
| Fintech / wealth | Single-field conversion | Editorial split + email-capture hero + monochrome logo wall + research/timeline band |
| Creator-tool landing | Product demo led | Interactive demo hero + bento grid + per-section accent colors + tilted product frames + tinted shadows |
| Premium consumer brand | Cinematic brand | Cinematic center hero + double-bezel containers + mesh gradient + scroll-pinned product walks |
| Mobile app landing | Split-hero product page | Morphing status pill nav + dock-style magnification CTA + parallax tilt feature card |

---

## Compositions

Every system the engine builds names one of five compositions: the layout a landing page starts from. The Page composition section of `system-report.md` gives the winner, the runner-up and the two terms that decided it, and the JSON result carries all five scores (decisions/page-composition.md). Start from the winner. The client's own site, or a brief that says otherwise, can overrule it; the build notes say which and why. With an existing design system and no report, pick by the same terms below and say so.

The composition is the layout; the archetype above is the argument the page makes. They pair naturally: split with the Split-hero product page or Service lead generation, stacked with Thesis statement or Single-field conversion, bento with Product demo led, editorial-column with Editorial long form, full-bleed-media with Cinematic brand. Another pairing is allowed when the build notes give the reason.

What all five share. Widths are read at 1440 (the desktop tier: `layout.columns.desktop` columns inside `layout.container.max`) and at 375 (the phone tier: `layout.columns.phone` columns inside `layout.margin-inline.phone`). Regions sit the region gap apart (`layout.region-gap.<tier>`, or the system's landing region gap where it has one). The headline takes the hero style (`type.text.hero`, or the system's landing display step where it has one) and steps down on phones by `type.phone.hero`. Numbers take `type.text.figure`. The primary action is a filled button at `layout.target.large`. A proof section with no real proof behind it is dropped with its reason (/ux-design engine step 2.5); the layouts below close up around the gap rather than hold an empty band.

### split

**Structure.** The message on one side and one image or proof object on the other, then sections that alternate sides.
**The engine picks it** when the brief is formal, the contrast is balanced rather than extreme, and the temperature is cool: formality, balanced contrast and coolness are its three terms. It suits business software, finance, security, and a marketplace with a real product view.
**At 1440.** Hero: the copy spans 7 of the 12 columns and the media 5, or 5 and 7 when the media carries the value; headline, one lede, the primary action and at most one secondary link. Proof: one full-width band directly under the hero, either a logo row or three to five figures with their labels. Sections below alternate the media side, each 7 and 5. Call to action: a full-width closing band on `color.surface.brand` with one filled action.
**At 375.** One column: copy, then the action at full width, then the media at full width at `imagery.ratio.card` or the media's own ratio, cropped clear of any mark. The proof band becomes two figures per row, or a logo row that wraps to two rows. Every alternating section stacks the same way, media first. The closing band keeps one full-width action.
**Arabic.** Under `dir="rtl"` the copy column takes the start side, the right, and the media the left, through logical grid placement, not reordered markup. The alternation mirrors with it. Figures keep Western digits and the media itself never flips.
**It fails when.** The split drifts to an even 6 and 6, every section repeats copy on the same side, or the media is a generic illustration where the product should be.

### stacked

**Structure.** One centered column of large, calm sections, one idea each, read top to bottom.
**The engine picks it** when the audience is older or of mixed age (the age field weighs most), the density is airy and the contrast is muted: the audience's age, airiness and muted contrast are its terms. It suits patient-facing healthcare, public services and local businesses whose visitors read on a phone.
**At 1440.** Hero: headline, lede and one action centered within `layout.measure.text`, with the image below the action across the container, never beside it. Pair it with the Thesis statement archetype so the centered hero is deliberate; otherwise align the hero to the start of the same column. Proof: one row of figures or one named quote, inside the measure. Each later section is one idea in the measure, its media across the container, and every second region sits on `color.surface.band` so the column has a rhythm. Call to action: a centered closing band that repeats the hero's action.
**At 375.** Almost nothing moves, since the column already fits: the headline steps down, actions go full width, and the region gap takes its phone value.
**Arabic.** Centered lines stay centered. Lists, forms and captions inside the column align to the start, the right.
**It fails when.** Every region is the same centered block at the same weight and the page reads as a slide deck, or it is kept for a product people have to compare side by side.

### bento

**Structure.** A grid of tiles of different sizes, each a feature or a number, scanned at a glance.
**The engine picks it** for a dense, high-contrast brief with geometric type, and more strongly when the brief's reading context is glance: density, contrast, geometric type and glance reading are its terms. It suits developer tools, status and monitoring products, and apps whose value is several capabilities at once.
**At 1440.** Hero: a start-aligned or split hero above the grid; the grid is never the hero. Grid: five to eight tiles on the 12 columns, spanning 3, 4, 6 or 8 columns and one or two rows, with one lead tile (6 or 8 columns, two rows) holding the real product view. Tiles sit `layout.gutter.desktop` apart, not the region gap. Proof: figures live inside tiles with their labels, and one tile may hold a named quote. Call to action: a closing band after the grid, never a tile.
**At 375.** One column in reading order, lead tile first, each tile at full width with its height set by its content. Two figure tiles may share a row when each is a number and a short label.
**Arabic.** Grid placement mirrors, so the lead tile starts at the right edge. Tile content aligns to the start; digits keep their order.
**It fails when.** The tiles are equal, a three by three of identical cards, there are fewer than five, or a tile holds a decorative shape instead of a feature or a number.

### editorial-column

**Structure.** A narrow reading column with a large display title, pull quotes and images set into the text.
**The engine picks it** for humanist type, a formal tone and an airy density, and more strongly when the reading context is long reading: humanist type, formality, airiness and long reading are its terms. It suits research, editorial products, consultancies that sell judgment and long product explainers.
**At 1440.** Hero: the display title start-aligned across up to 8 columns, a standfirst in the body style within `layout.measure.text`, a line of metadata in `type.text.label`, then one image at `imagery.ratio.hero` across the container. Body: the text column at `layout.measure.text`, offset from the start by one or two columns; images break out to the container; pull quotes sit in the wide margin beside the paragraph they come from. Proof: the pull quotes, each attributed with name, role and company. Call to action: an inline action where the argument ends, then a closing band.
**When the client has no pull quotes:** use one of the client's own sentences as a callout, set large with no quotation marks and no attribution, since it is the page's own claim; or a real figure with its source in a caption; or a captioned image of the real product or place. Never an invented quote, and never quotation marks around words nobody said.
**At 375.** The column takes the full width inside the margins, the title steps down, images run the full width, and margin callouts become blocks between paragraphs.
**Arabic.** The column starts at the right, so margin callouts move to the left margin. The display title takes the Arabic display face with no letter spacing, and body text keeps the system's reading line height.
**It fails when.** The column runs wider than the measure, the page has little to read (a tool with three features), or a quote is made up to fill the margin.

### full-bleed-media

**Structure.** Edge-to-edge images or generated art with the headline on a scrim, then bands of media and short copy.
**The engine picks it** for a warm, playful brief with lively motion: warmth, playfulness and motion are its terms. It suits hospitality, food, consumer products, events and lifestyle brands with real photography.
**At 1440.** Hero: the image runs to both viewport edges at `imagery.ratio.hero`, with the headline and action inside the container on `imagery.scrim` in `imagery.on-scrim`, the scrim measured on the worst part of the image (decisions/scrim-worst-image.md). Proof: a band of short attributed lines or a rating between the media bands, on the page surface, never on a photo. Below, full-bleed image bands alternate with contained text bands. Call to action: a closing band over an image on the scrim, or on `color.surface.brand`.
**At 375.** The hero takes an art-directed portrait crop at `imagery.ratio.portrait` (a separate source through `<picture>`), subject clear of the text; the headline sits on the scrim in the lower third and the action runs full width. Each band stacks image then text.
**Arabic.** The text block moves to the start side, the right, and the crop keeps the subject away from it, so the right-to-left crop may differ from the left-to-right one. Photos never flip.
**It fails when.** The images are stock, text sits on a photo without the scrim, or the client has no real imagery; then start from the runner-up the report names instead.

---

## Section flow

### AIDA (the default framing for landings)

- **Attention (hero).** Cinematic, clean, wide layout. One claim, one supporting line, one primary CTA plus one secondary.
- **Interest (features, bento).** High-density, mathematically intentional grid or interactive components.
- **Desire (motion, media).** Pinned sections, horizontal scroll, scroll-driven reveals, customer outcomes.
- **Action (pricing, footer).** Massive high-contrast CTA, clean footer.

The section order comes from the archetype above and from the engine's page sequence for the brief's goal. Section orders observed by cohort (B2B, editorial, developer tooling, creative) are catalogued in `references/styles/exemplars.md` (Section-flow patterns).

### When to include a section

- **Animated counters**: when the metric is the proof. Skip when the number is incidental.
- **Numbered "how it works"**: when the product has a clear onboarding arc. Skip if it's a single tool with no sequence.
- **"Before / after" comparison**: when there's a clear status-quo competitor to displace. Skip in greenfield categories.
- **Logo strip**: when 6+ recognizable customers can be named. Skip with 3 logos, it looks thin.
- **Bento grids**: when 5-8 distinct capabilities need showcasing. Skip for 3, it looks underbuilt.
- **Chapter-framework narrative**: when the product is large enough to feel like a journey. Skip on single-purpose tools.
- **Ambient hero motion**: when the page is otherwise quiet. Don't stack motion on motion.
- **Compliance badges**: when procurement teams will ask. Skip on consumer-facing surfaces.
- **Mid-page "still have questions" deflector**: on long pages. Skip on short pages; the final CTA does the job.
- **Interactive product demo**: when the product is visual or temporal and 60+ seconds of engagement justifies the build cost.
- **Pulsing globe**: when the product has genuine global infrastructure to surface; skip when it's vibes.

### Feature sections and rhythm

| Don't | Do instead |
|---|---|
| 5-column or 9-tile feature grids cramming every capability into one screen | 3-5 marquee feature sections, each with a deep visual. Width breeds shallowness; depth wins memory |
| Cramped feature cards with 9-12 tiny tiles in a 3x3 or 4x3 grid | 3-5 themed sections with one feature focus each. The dense grid reads as a single visual unit and the reader remembers nothing |
| Long bare bullet lists of features | Features get marquee treatment with visuals, not bare bullets |
| Marketing sections at `py-12` or less | `py-32 md:py-48` minimum on desktop, 64-96px on tablet, 48-72px on mobile. Sections must feel like distinct chapters |

**Feature split on mobile.** Alternating image and text rows stack on mobile: the image goes full-width above the text (use `order`), not a squeezed half-width thumbnail. Rows alternate sides on desktop; on mobile they all stack the same way, image on top.

---

## Hero

### Hero composition

- One headline, one supporting line, one primary CTA (filled) and at most one secondary (ghost button or text link), one product image or short motion. The CTA section below holds the button rules.
- Above the fold, nothing else fights for attention. No carousel, no slideshow, no rotating taglines.
- **H1 line limit.** The H1 runs 3 lines at most at every breakpoint from 375px to 1440px; a 4-line H1 fails. Meet the limit by widening the container (`max-w-5xl`, `max-w-6xl` or `w-full`) and scaling with `clamp()`, not by cutting the claim.
- A "Built for X" line ("Built for finance", "Built for sales teams") under or beside the H1 pre-qualifies the visitor in one breath. It never sits above the H1; the eyebrow owns that slot.

### Hero patterns

**Asymmetric split hero.** Text aligned left or right, media asset on the opposite side, no centering. The background fades subtly into the page background (lighter on light mode, darker on dark mode). The split is intentionally uneven, 7/5 or 5/7 columns, not 6/6. It defeats the "centered hero over dark image" default: the asymmetry creates hierarchy without typography variance. Cost: zero, pure layout.

**Editorial split hero.** For premium SaaS and content-led products. Text left, image right, with massive negative space between. The split is 60/40 or 65/35 with breathing room, not 50/50. Cost: zero, layout discipline.

**Artistic asymmetry hero.** For brand-forward marketing and creative-tool landings. Text offset to the left, an artistic floating image overlapping the text from the bottom right, generous negative space. Cost: low, layout plus image z-stacking.

**Asymmetric hero with stylistic fade.** For brand-driven launch pages and premium consumer products. A high-quality relevant background image with a subtle stylistic fade (darkening or lightening into the page background depending on mode). Text aligned cleanly left or right. Cost: low, image processing plus a CSS gradient mask.

**Cinematic center hero.** For marketing surfaces where a single statement carries the entire value proposition. Text perfectly centered, ultra-wide H1 container (`max-w-5xl` or wider), exactly two high-contrast CTAs below. Behind everything, a full-bleed background image with a dark radial wash. Buttons stay legible: a dark background gets white text, a light background gets dark text. When centered is the intentional choice (not the default), it functions as a declaration of confidence; the centered-hero rule in Hero bans decides when it is allowed. Cost: low, careful contrast tuning and image processing.

**Thesis-statement hero.** For editorial, AI and research-positioning products. Large centered display headline (single line if possible), 2-4 sentences of body-size prose under it, single CTA with at most one secondary link. No multi-button toolbar. The cliff between display scale and body scale is the design. Confidence reads as willingness to use full sentences in the subhead. Cost: zero, typographic discipline.

**Email-capture hero.** A single email input plus a single button as the hero's primary CTA. See archetype 5. Cost: low, form plus state.

**Curtain reveal.** For a brand statement at the top of the hero or a theatrical entry. The hero splits in the middle on scroll, revealing what is behind. Cost: needs a scroll-trigger library.

### Hero media

**Large product mock.** The canonical hero image is the actual UI: a dashboard, a workflow, a chat interface. Cropped close, with extreme detail visible and real-looking data inside it. Soft drop shadow and subtle rounded corners (12-24px). Box-shadow at low opacity and high blur (for example `0 24px 64px rgba(0,0,0,0.08)`). The screenshot floats above the page without harsh edges.

**Cropped dashboard preview.** For B2B marketing that shows dashboards or admin interfaces. Cropped, never full-page. The reader sees one card, one chart, a sliver of nav: enough to read "this is software," not enough to parse the dashboard. Real data shapes (sparklines, log lines, plausible numbers) instead of stock chart shapes. Cost: zero, design discipline.

**Code as hero content.** For developer-tooling and infrastructure marketing. Treat a code block like hero photography. Short (6-14 lines), syntax-highlighted with a custom theme that matches the page accent, inside window chrome (traffic-light dots, a title bar with the filename). Built in HTML and CSS, not a screenshot, so it scales crisply. Cost: medium, a custom syntax theme plus window chrome styling.

**Terminal mockup.** For infrastructure, CLI and dev-tool marketing. Near-black window with traffic-light chrome and a `$` or `>` prompt. The command is short, declarative, and runnable exactly as written. Multi-line terminals fade older lines with reduced opacity. Output is monospace and color-coded (green success, gray chatter, bright neutral for user input). Cost: low, CSS plus content.

**Interactive product demo.** A real, manipulable instance of the product running inline. The user can drag, type and click, and the product responds with actual logic, not a video loop. The strongest "designed by designers" signal available. Affordances: subtle pulsing dots, ghost hand-cursor hints, a "try it" label on the first interactable element.

**Animated metric callouts.** Numbers tick up from 0 on entry over 800-1500ms. Restricted to 2-3 stats; more dilutes the effect. The counter triggers once per page entry, then stays static. Numbers use tabular figures, so the layout does not shift during the count, and an eyebrow above each stat names what it counts.

**Kinetic headline reveal.** Hero text appears almost instantly; the heavier interactive demo or 3D render fades in 200-400ms behind it. Never make users wait for first meaningful paint.

**Slow ambient motion.** A slow rotating gradient, a chart that gently animates, a token sliding across a connection. Subtle enough that it is only noticed on a second look.

**Auto-playing muted video.** Plays automatically, muted and looped, often at reduced contrast or under a subtle dark gradient overlay that keeps overlaid text legible. Ships a still poster image as the fallback for slow connections. The file stays under 4MB for a 30-second loop.

**Pulsing globe or animated map.** Shorthand for global infrastructure. The animation is slow (3-6s loop), low-saturation, and never obstructs the headline. Labels appear only on the regions with real presence.

**3D marquee object.** A single render of the product as a physical thing: soft-clay device, glass orb, metallic monolith. Rotates on scroll. Matte (not glossy) PBR materials with a strong rim light and a soft floor shadow.

**Two-column hero with metaphor image.** The text does the heavy lifting; the image carries a metaphor. Works for support and customer-experience categories. The image is atmospheric, not literal product UI: water, light, fabric or sky as a metaphor for the feeling the product evokes.

**Synthetic screenshot composition.** When the product is too abstract to screenshot (a workflow, an agent conversation, a queue of work), the hero becomes a stylized composition of UI fragments: a card, a notification, a chat bubble, a status pill, floating against a soft background.

**Narrative chat thread.** A multi-turn conversation between an agent and a person, shown inline. The reader absorbs the capability through the conversation instead of prose explaining it. Replaces older "feature screenshot" treatments for AI-adjacent capabilities.

**Cropped interface fragment.** A standard split where the visual is a real interface fragment, not a stock illustration, and it overflows the viewport on purpose (a cropped right edge) to imply scale. The deliberate crop is the signal. Cost: zero, layout.

**Stacked-card collage.** Two to four UI fragments (a panel, an overlay, a tooltip, a popup) layered at varying depths. The overlap is choreographed so layers imply depth without hiding meaning. Use it when the product has several distinct surfaces to show at once. Cost: medium, z-stacking, crop and shadow management.

**Tilted product frame.** Product shots tilted 6-12 degrees on the Y axis with a subtle perspective shadow, floating against the section background, so the screenshot reads as a design object. For high-end maximalist and creative-tool styles. Cost: low, a CSS transform plus a shadow.

### Hero bans

| Don't | Do instead |
|---|---|
| Centered hero with text over dark image as the default | Asymmetric hero: text left or right, image with a subtle stylistic fade. Centered hero only when DESIGN_VARIANCE is 4 or below, or when the archetype is Thesis statement or Cinematic brand and was chosen deliberately. |
| Symmetric 50/50 split-screen heroes | 7/5 or 5/7 split. The asymmetry creates hierarchy without typography variance |
| Cookie-cutter left-text-right-image hero as the default reach | Editorial split (massive whitespace between halves), curtain reveal, asymmetric float, or full-bleed background |
| `h-screen` on the hero | `min-h-[100dvh]`. The iOS Safari address-bar collapse breaks `h-screen` |
| Floating stamp or badge icons on hero text | If the hero needs a label, use a small eyebrow tag above the H1 |
| Pill tags scattered under the hero as decoration | Pills work as status indicators or single-eyebrow taxonomy, not as decorative confetti |
| Raw data or stats dumped in the hero subhead ("100k users", "99.99% uptime") | Stats earn their place lower on the page with context. The hero subhead clarifies, it does not quantify |
| A giant fake browser window tilted in 3D space as decoration | Product screenshots presented flat, or with a subtle 6-12 degree tilt where it serves a "design object" framing |
| Hero carousels with auto-advancing slides | A single confident hero. If multiple stories must coexist, use tabs with manual control |
| Animated typewriter on the H1 | Reserved for content that is genuinely input (a search bar, a chat). A typewriter on a headline reads as a gimmick |

### Hero on mobile

Stack to one column: copy and CTA first, media below. Or put the media behind the copy as a full-bleed background with a legibility scrim (dark overlay) so the headline and accent stay readable. The headline clamps down; a 56px headline does not fit a 360px screen. A hero form goes full-width below the copy. The failure to prevent: a fixed 2-column hero where the text and the form sit side by side and overflow the viewport.

### Form in the hero

When the quote or contact form lives in the hero, the form is the primary CTA. Do not add a separate hero button that scrolls to that same form. A CTA points to an action that is not already on the screen, so a button targeting the visible in-hero form is a dead, redundant control. Let the headline and lede lead into the form. A CTA in the nav or in a later section that points back to the hero form is correct, because there the form is off-screen. A button beside an in-hero form needs a real job (focus the first field), never a scroll to itself.

---

## Header and navigation

### Nav bar

**Desktop.** Logo left, links center or right, primary CTA right. Slim: 60-72px tall, 5-7 items, at most two action buttons on the right edge. Mega-menus open on hover; never cram mega-categories into two rows of nav.

**Mobile contract.** The bar stays one row. Only the logo and the single primary CTA persist; every nav link collapses behind a menu button that opens a drawer or a full-screen overlay. The collapse breakpoint sits between 768px and 1024px, so the desktop nav never gets squeezed into a narrow viewport. The bar stays at or under 64-72px.

- The brand wordmark never splits mid-name. Give it `white-space: nowrap`; if the full wordmark does not fit beside the menu button and the CTA, drop to the logomark alone (keep the icon, hide the words).
- Utility actions (phone, search, account) become icon-only below the breakpoint: a labeled icon button with `aria-label`, not a text and icon pair that overflows. A phone shows the handset glyph, not the number.
- The drawer is a real overlay: focus-trapped, closed by `Esc` and by the backdrop, body scroll locked, links at least 44px tall.

Breaks to prevent: links wrapping to a second row, the wordmark stacking mid-name, a phone number plus label plus CTA crammed until the bar is two or three rows tall.

### Sticky-header budget on mobile

Total sticky or fixed top chrome is about one row: target 72px or less, hard ceiling about 96px. Only the primary nav and its single CTA persist on scroll. A decorative or utility bar (ratings, announcement) is not sticky; it sits at the top and scrolls away. If the summed height of everything pinned exceeds the ceiling, cut what sticks until only the nav row remains. The sticky element wraps the nav alone: a sticky element is bounded by its containing block, so a utility bar left inside the sticky `<header>` both inflates the budget and lets the nav unstick once that box scrolls past.

### Utility and announcement topbar

**Desktop.** Claims inline, divider-separated ("Rated Excellent | Same Day | UK Wide").

**Mobile contract.** This bar is secondary chrome; on a phone it stays about one line tall. In priority order:

1. One condensed centered line: the stars, then the claims in small text separated by middots, with the `|` dividers swapped for middots. This is the default.
2. Show fewer: if one line is still cramped at 360px, keep the stars and the single strongest claim and drop the rest on mobile. Bring them back at a wider breakpoint.
3. Horizontal scroller: the claims in a single `overflow-x: auto` row.

Stacking claims onto their own lines is acceptable only for one or two short items, and never when it makes the header tall. Four centered lines of stars and claims produce a 150px+ block, the exact failure this contract prevents. The bar is not sticky (see the budget above).

Breaks to prevent: claims wrapping mid-phrase into ragged lines with dangling `|` dividers, or claims stacked into a tall block that bloats the header.

---

## Proof

Proof is what makes the claims above it believable. It is specific, attributed and quiet.

### Monochrome logo wall

For trust strips and customer-proof sections. 6-10 customer logos in a single row, all desaturated to the page's neutral text color, at uniform optical weight (not pixel size: each logo is adjusted so they read evenly). Generous gutters. Often introduced by a short label ("Working with", "Trusted by teams at"). The wall reads as a single block of social proof. Cost: zero, a CSS filter or pre-rendered greyscale assets. Place it once near the hero and optionally once before the final CTA; never more. A second appearance uses the identical treatment, and only one appearance carries the eyebrow label.

### Proof bans

| Don't | Do instead |
|---|---|
| Generic testimonial copy ("This product changed my life", "Amazing tool!") | Quantified, named testimonials: "We cut p99 from 380ms to 90ms." Name, role, company |
| Customer quotes without a name, role, or company | Name plus role plus company at minimum. Quotes with no attribution read as fabricated |
| Generic testimonial sections of 15+ unattributed quotes | 2-3 strong, named, quantified quotes beat 15 vibes-only |
| Auto-playing testimonial videos on page load | Opt-in. Auto-play is intrusive |
| Stat callouts that are visibly invented ("99.99% uptime!") | Real numbers or organic-looking ones (47.2%, 280K, $8,247.30). Round numbers in stats read as marketing |
| "Trusted by 10,000+ developers" with no logos | Show logos or show nothing |
| Customer logos in full color | Single mono treatment (all 70% black, all white, or all neutral ink). Mixed-color logo walls read busy |
| Logo walls repeated 3+ times down a single page as filler | Once near the hero, optionally once before the final CTA. More reads as overcompensation and the trust signal collapses |
| "As seen in" press logos at radically different sizes | If the press logos lift the brand, render them uniformly at optical heights. If they don't, skip them |
| Press logos from publications nobody recognizes | Skip them. Press logos sit quieter than customer logos |
| Compliance badge logos in original full color | Single-color or grayscale, all badges at uniform optical weight |

---

## Pricing

- **Homepage pricing is a teaser.** Full pricing tables on the homepage feel sales-driven. Tease with a "starts at" line and a link to the pricing page.
- **Two to four plans.** One plan is marked as the recommended choice with one visual device (a border, a label, or a tint), not three.
- **Every plan states who it is for** in one line before it lists features.
- **Prices use tabular figures** and one consistent format across plans (same decimals, same billing period label).
- **A billing toggle states the saving as an amount** ("Save $48 a year"), not only a percentage, and the default toggle state matches what most customers buy.
- **Feature comparison lives in a table below the plan cards**, with the plan names repeated in a sticky header on long tables. Plan cards carry at most 5-7 differentiating lines each.
- **The enterprise or custom plan names what changes** (limits, support, contract terms) next to its "Talk to sales" action. A bare "Contact us" card is not a plan.
- **Each plan has one CTA with a specific verb** ("Start free", "Start 14-day trial", "Talk to sales"). The recommended plan carries the only filled button.
- **On mobile, plans stack in the order of recommendation**, the recommended plan first, and the comparison table scrolls horizontally inside its own container.

---

## CTA

| Don't | Do instead |
|---|---|
| Generic "Get Started" / "Learn More" as the only CTA | Specific verbs naming what happens next: "Run the demo", "See the dashboard", "Open account", "Start free", "Deploy", "Run a query" |
| Multiple primary CTAs above the fold | One primary, optionally one secondary. Two filled CTAs of equal weight dilute the primary path |
| Form fields asking for too much in the first interaction | 3-4 fields ceiling for "book a demo" or signup flows |
| Modal popups for newsletter signup on a timer | Newsletter signup goes in the footer or a sidebar component, not in a time-triggered interstitial |
| Floating chat widgets overlapping the primary CTA | Position chat where it can't compete, or hide it on the hero |
| Sticky chatbot bubbles in the corner on first load | None. Wait for engagement |
| Cookie banners blocking first paint | Slim, monochrome, bottom-bar or sidebar treatment that respects the page |

- **The final CTA band repeats the primary action**, with the same verb as the hero CTA, on a full-width band with the page's strongest contrast: a tinted band, a full-dark band, or the brand's strongest color. One line restates the value proposition above a single filled CTA. The hero held back; the closer does not.
- **A FAQ, when present, sits above the final CTA**, never below it.
- **A CTA never points at itself.** A button that scrolls to a form already on screen is redundant (see Form in the hero).
- **On long pages, the primary CTA is reachable at every scroll depth** through the sticky nav's single CTA, not through a floating button that covers content.

---

## Footer

| Don't | Do instead |
|---|---|
| Footer treated as filler | The footer is a sitemap: 4-6 columns by audience (Product, Solutions, Resources, Company, Legal) |
| Thin one-row footer with three social icons | The footer is generosity after the page's restraint |

- **The footer carries** the legal links, the contact route, the language switcher on multilingual sites, the wordmark, social links, a status indicator for operational products, and the newsletter field if the page has one. The newsletter field sits above the sitemap columns, not at the absolute foot.
- **Each column holds 4 to 8 links.** The footer takes a slightly darker or lighter band than the page.
- **Footer on mobile.** Link columns stack to a single column, or collapse into accordion sections. Legible spacing, never a cramped 4-column grid squeezed into 360px.

---

## Arabic and RTL

A landing page that ships in Arabic is designed in Arabic, not mirrored after the fact.

- **Set direction on the document.** `<html lang="ar" dir="rtl">`. Every layout rule then flows from logical properties.
- **Use logical properties everywhere.** `margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `border-inline-start`, `text-align: start`. Physical `left` and `right` in layout CSS break the mirror. In Tailwind, use `ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`.
- **Mirror directional glyphs, not containers.** The grid mirrors itself through `dir="rtl"`. Arrows, chevrons, back and forward icons, progress direction and carousel order flip. Logos, media playback controls, checkmarks, clocks and photographs do not flip. A chart's time axis is a product choice: mirror it or keep it left to right, and keep the choice the same on every chart. Never apply `transform: scaleX(-1)` to a whole section.
- **Letter-spacing is 0 under `dir="rtl"`.** Arabic is a connected script; any tracking breaks the joins between letters. Reset the tracked eyebrow and display styles: `[dir="rtl"] * { letter-spacing: 0; }` or an equivalent per-style override. All-caps and uppercase transforms do not apply to Arabic either.
- **Set the Arabic face 1 to 2px larger than the Latin face at the same step.** Arabic glyphs sit smaller on the same em. Keep one scale and add the offset per step, and raise line-height for body text so diacritics clear.
- **Name the Arabic face explicitly** in the font stack. Never let a Latin stack fall back to a system Arabic face.
- **Budget for copy 10 to 25 percent longer** than the English source. Headlines, buttons and nav labels need that room at 360px without wrapping; test with the real Arabic copy, not with English placeholders.
- **Use Western numerals** (0-9) for prices, stats, phone numbers and dates, and keep them consistent across the page.
- **Put the currency after the amount** ("250 ر.س", "49 د.إ", "1,200 ج.م"). Keep the number and the currency together with a no-break space (U+00A0, as in these examples) so they never split across lines.
- **Mixed-direction strings stay intact.** Wrap Latin brand names, emails and URLs inside Arabic sentences in `<bdi>` or `dir="auto"` so punctuation lands on the correct side.
- **Stagger and slide motion mirrors.** A left-to-right cascade in LTR runs right to left in RTL.

---

## Checklist

### Critical
- [ ] No `h-screen` on the hero; `min-h-[100dvh]` instead
- [ ] Nav stays one row at 360px and the sticky top chrome is 96px or less
- [ ] Under `dir="rtl"`, letter-spacing is 0 and layout uses logical properties

### High
- [ ] One archetype chosen and committed; the page does not mix skeletons
- [ ] Centered hero only when DESIGN_VARIANCE is 4 or below, or when the archetype is Thesis statement or Cinematic brand and was chosen deliberately.
- [ ] No hero button that scrolls to a form already visible in the hero
- [ ] No customer logos in original full color
- [ ] Specific CTAs, not "Get Started" / "Learn More" reflexively
- [ ] Footer is a sitemap, not a one-row strip
- [ ] Arabic copy tested at real length; numerals Western; currency after the amount

### Medium
- [ ] No press logos from publications nobody recognizes
- [ ] No "Trusted by 10,000+ developers" with no logos shown
- [ ] Logo wall appears at most twice
- [ ] A FAQ, when present, sits above the final CTA
- [ ] Pricing on the homepage is a teaser line, not a full table

### Low
- [ ] Testimonials have name, role and company at minimum
- [ ] Press logos quieter than customer logos
