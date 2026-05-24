# Exemplar patterns — the world-class premium catalog

A distilled catalog of patterns observed across premium real-world surfaces. Each pattern is described in functional terms: when to use it, what it costs, what makes it distinctive.

Use this catalog to build surfaces that compete with the best in the world. Each pattern has been seen multiple times across high-end products; the convergence isn't accident — it's the shape of premium taste in this era. Pick patterns that match the brief, execute them with precision, ship them.

This file is organized by surface and intent:
- Premium SaaS catalog overview
- Hero treatments observed (~20 distinct patterns)
- Navigation patterns observed (~12 distinct patterns)
- Section-flow patterns
- Imagery treatments observed
- Content & copy voice patterns
- Color treatments by product category
- Motion language observed by tier
- Cross-cluster takeaways

---

## Premium SaaS catalog overview

The premium SaaS aesthetic in current marketing surfaces is built on a foundation of subtraction. Each premium product removes the things a less mature brand would add. No second typeface, no second accent color, no second CTA in the hero, no decorative AI iconography, no stock photo, no parallax, no scroll-jacking, no exclamation, no superlative. The negative space — visual, typographic, and rhetorical — is the personality.

What converges across the premium tier:

- Type carries almost all visual weight. Decoration is rare.
- One accent color, used like punctuation.
- Generous vertical rhythm. Sections breathe.
- One distinctive face (display + body), never two competing.
- Imagery is real product UI, not stock.
- Microcopy carries voice; primary surfaces stay calm.
- The page reads as a long, well-considered piece of prose, not as a billboard.

What absent from the premium tier:

- Purple-to-pink AI gradient.
- Brain / sparkle / neural-network iconography.
- 3D chrome, ray-traced spheres, metaverse-cube clusters.
- Stock photography of diverse teams laughing at laptops.
- Title Case headlines.
- ALL CAPS body or subhead copy.
- More than two CTAs in the hero.
- Logo walls in full color.
- Decorative serifs deployed for "premium feel" without intent.
- Exclamation marks in marketing copy.

The premium signal is composure. The hardest pattern to copy is the discipline to leave things out.

---

## Hero treatments observed

A catalog of distinct hero compositions across premium marketing surfaces. Each treatment carries a specific signal; pick based on what the product is selling.

### Centered thesis hero
Large centered display headline (1 line if possible, 2 max), 2-4 sentences of body-size prose under it, single primary CTA with at most one secondary text link. No multi-button toolbar.

- **When to use**: editorial / AI / research-positioning products where the brand voice is "we have something to say."
- **Distinctive marker**: the cliff between display scale and body scale. The willingness to use full sentences in the subhead.
- **Cost**: zero — typographic discipline.

### Asymmetric split hero
Text left, image right (or reversed), with massive negative space between. The split is intentionally uneven — 60/40 or 65/35, not 50/50.

- **When to use**: premium B2B SaaS, content-led products.
- **Distinctive marker**: the breathing room in the middle of the split. The hero feels composed, not stuffed.
- **Cost**: zero — layout discipline.

### Editorial column rhythm hero
Standard SaaS split, but the visual is treated as a real interface fragment, not a stock illustration. The fragment overflows the viewport intentionally (cropped right edge) to imply scale.

- **When to use**: developer tools, infrastructure marketing.
- **Distinctive marker**: the deliberate crop. The interface fragment isn't centered or framed — it bleeds out.
- **Cost**: zero — layout.

### Cinematic center hero
Text centered, massive width, ultra-wide H1 container. Two high-contrast CTAs below. Full-bleed background image with a dark radial wash. Buttons perfectly legible — dark background gets white text.

- **When to use**: marketing surfaces where a single statement carries the entire value proposition.
- **Distinctive marker**: when centered is the intentional choice (not the default), it functions as a declaration.
- **Cost**: low — careful contrast tuning, image processing.

### Artistic asymmetry hero
Text offset to the left. An artistic floating image overlapping the text from the bottom right. Generous negative space.

- **When to use**: brand-forward marketing, creative-tool landings.
- **Distinctive marker**: the floating image overlap. The image isn't behind the text — it's in front and overlapping.
- **Cost**: low — layout + image z-stacking.

### Email-capture hero
A single email input + a single button as the hero's primary CTA, replacing a "Sign Up" button. The hero copy implies the field IS the start.

- **When to use**: fintech, signup-led products.
- **Distinctive marker**: the absence of a multi-step funnel. The implied promise is "one field is enough."
- **Cost**: low — form + state.

### Interactive product demo hero
A real, manipulable instance of the product running inline. The user can drag, type, click — and the product responds with actual logic, not a video loop. Subtle pulsing dots, ghost hand-cursor hints, or a "try it" label on the first interactable element.

- **When to use**: creative tools, design platforms, design-led SaaS where the marketing site has to prove the tool's taste.
- **Distinctive marker**: the strongest "designed by designers" signal available. Converts the prospect into a user 5 seconds in.
- **Cost**: high — real product engine running in the browser. Worth the build cost when 60+ seconds of engagement justifies it.

### Auto-playing muted hero video
Hero video plays automatically, muted, looped, at reduced contrast or with a subtle dark gradient overlay to keep overlaid text legible. The video runs in the background of attention.

- **When to use**: products that are visual or temporal (AI-generated content, audio, motion).
- **Distinctive marker**: the video shows actual product output, not abstract motion graphics.
- **Cost**: medium — production + compression. Cap at 4MB for a 30-second loop.

### Large product mock hero
The canonical hero image is the actual UI — a dashboard, workflow, chat interface. Cropped close, with extreme detail visible. Real-looking data inside it. Soft drop shadow + subtle rounded corners. The screenshot floats above the page.

- **When to use**: B2B SaaS, analytics products, dashboard tools.
- **Distinctive marker**: the close crop. Not the whole app at 30% zoom — a tight crop on the specific feature.
- **Cost**: zero — screenshot + container styling.

### Stacked-card collage hero
2-4 UI fragments layered at varying z-depths — a panel, an overlay, a tooltip, a popup — creating dimensional composition. Suggests "here are several features at once."

- **When to use**: products with multiple distinct surfaces or capabilities to show.
- **Distinctive marker**: the choreographed overlap. Layers overlap intentionally to imply depth without obscuring meaning.
- **Cost**: medium — z-stacking + intentional crop + shadow management.

### Tilted product frame hero
Product shots tilted 6-12° on the Y-axis, given a subtle perspective shadow, floated against the section background. Creates the "design object" framing.

- **When to use**: high-end maximalist / creative-tool styles.
- **Distinctive marker**: the screenshot becomes an artifact, not documentation. The tilt is what reframes it.
- **Cost**: low — CSS transform + shadow.

### Animated metric callouts in hero
Numbers tick up from 0 on entry over 800-1500ms. Restricted to 2-3 stats max; more dilutes the effect. Counter triggers once per page entry, not on every scroll past.

- **When to use**: when the number is the proof. Skip when the number is incidental.
- **Distinctive marker**: the count animation is the demo. The number is doing the persuading.
- **Cost**: low — counter component.

### Kinetic headline reveal
Hero text appears almost instantly; the heavier interactive demo or 3D render fades in 200-400ms behind it. Never make users wait for first meaningful paint.

- **When to use**: any premium hero with substantial visual payload.
- **Distinctive marker**: the text never waits for the asset. First contentful paint is held under 400ms.
- **Cost**: zero — load order discipline.

### 3D marquee object hero
A single hero-render of the product as a physical thing — soft-clay device, glass orb, metallic monolith. Rotates on scroll. Matte (not glossy) PBR materials with strong rim light and soft floor shadow.

- **When to use**: premium consumer brands, hardware companion apps.
- **Distinctive marker**: anchors the brand in physical-design vocabulary. The product is positioned as an object.
- **Cost**: high — Blender or equivalent render. Subtle scroll-driven rotation.

### Pulsing globe / animated map hero
Recurring shorthand for "global infrastructure." The animation is slow (3-6s loop), low-saturation, never obstructs the headline. Labels only on the regions you actually have presence in.

- **When to use**: infrastructure products, CDN, edge networking, anything with genuine global presence.
- **Distinctive marker**: the restraint. Slow pulses, low saturation, no labels except real regions.
- **Cost**: medium — SVG or canvas animation.

### Slow ambient hero motion
A slow rotating gradient, a chart that gently animates, a token sliding across a connection. Subtle enough that you only notice it on a second look.

- **When to use**: pages that need to feel alive without demanding attention.
- **Distinctive marker**: the amplitude is so small you have to look directly at it.
- **Cost**: low — CSS keyframes.

### Two-column hero with metaphor image
Text does the heavy lifting; image carries metaphor. The image is atmospheric (water, light, fabric, sky) as metaphor for the feeling the product evokes.

- **When to use**: support and customer-experience categories.
- **Distinctive marker**: the image isn't product UI. It's mood.
- **Cost**: low — photography + layout.

### Synthetic screenshot composition
When the surface is too abstract to screenshot, the imagery becomes a stylized composition of UI fragments: a card, a notification, a chat bubble, a status pill, all floating against a soft background.

- **When to use**: workflow products, AI agent products, products that orchestrate other things.
- **Distinctive marker**: implies a product without committing to a literal frame.
- **Cost**: medium — design composition.

### Narrative chat thread hero
Multi-turn conversation between an agent and a person, shown inline on the marketing page.

- **When to use**: AI-assistant products, conversational interfaces, language-model tools.
- **Distinctive marker**: the reader absorbs the capability through the conversation, not through prose.
- **Cost**: zero — layout + content discipline.

### Code-as-design-content hero
Monospace, syntax-highlighted, with a window chrome (traffic-light dots, title bar with filename). The sample is short (6-14 lines), often runnable. Custom syntax theme matches the page accent — not a third-party scheme.

- **When to use**: developer-tooling marketing.
- **Distinctive marker**: code is treated like hero photography. Pixel-perfect HTML/CSS, not a screenshot.
- **Cost**: medium — custom syntax theme + window chrome.

### Terminal mockup hero
Near-black window with traffic-light chrome and a `$` or `>` prompt. Command is short, declarative, often runnable exactly as written.

- **When to use**: CLI products, infrastructure tools.
- **Distinctive marker**: the command shown is shippable. The CTA is "run this," not "sign up."
- **Cost**: low — CSS + content.

---

## Navigation patterns observed

A catalog of nav treatments across premium surfaces. Pick by the style system and the product's nav information density.

### Slim sticky transparent nav
60-72px tall, wordmark left, 5-7 nav items, two action buttons (Sign in + primary CTA) right edge. Transparent over hero, backdrop-blur or solid fill after ~100px scroll.

- **When to use**: most premium marketing surfaces.
- **Distinctive marker**: nav was always there but politely. The transition kicks in after first scroll, not before.
- **Cost**: low — CSS sticky + scroll listener.

### Floating glass pill nav
Detached from the viewport top with substantial top margin. Content includes brand mark, primary links, primary CTA. On scroll past hero, backdrop blur intensifies — but the pill never glues to the edge.

- **When to use**: high-end maximalist styles, premium product marketing.
- **Distinctive marker**: the detachment. The pill floats; it doesn't sit.
- **Cost**: low — CSS backdrop-filter + position fixed.

### Minimal split nav
Logo left, primary actions right, single accent on the active item. Thin horizontal rail, no background fill, sits on canvas. Optionally subtle backdrop blur after first scroll.

- **When to use**: minimalist styles, content-led SaaS.
- **Distinctive marker**: the nav sits on canvas. No rail background, no fill, just type.
- **Cost**: zero — pure layout.

### Mega menu on hover
Hover-revealed nav panels are not just link lists — they include preview thumbnails, feature highlights, and a "what's new" callout. Multi-column layout grouped by job-to-be-done.

- **When to use**: products with many sub-categories or audiences.
- **Distinctive marker**: the mega menu is treated as a micro-page.
- **Cost**: medium — staggered reveal + content composition.

### Status indicator in nav
A 6px green dot + 12px caps text saying "All systems operational" in the nav. Links to a status page.

- **When to use**: infrastructure products, developer tools, fintech.
- **Distinctive marker**: tiny but powerful trust signal.
- **Cost**: zero — small element with link.

### "What's new" badge in nav
A top-nav item ("What's new" or "Changelog") with a small dot or badge for recency.

- **When to use**: products with active development cadence.
- **Distinctive marker**: signals active development to engineers; gives returning visitors a destination.
- **Cost**: zero — badge UI.

### Dock-style magnification nav
Navbar at the edge with icons that scale fluidly on hover; neighbors grow proportionally less.

- **When to use**: creative tools, design-forward portfolios.
- **Distinctive marker**: the fluid magnification. The hover state is the entire interaction.
- **Cost**: low — CSS scale + cubic-bezier easing.

### Morphing status pill
Pill-shaped component that morphs to show status / alerts. Pop-up notification badge that emerges with overshoot spring, stays 3 seconds, vanishes.

- **When to use**: products with live data, status surfaces.
- **Distinctive marker**: the overshoot spring. The badge has weight.
- **Cost**: medium — layout animation + shared element IDs.

### Floating speed dial
FAB that springs out into a curved line of secondary actions.

- **When to use**: mobile-first surfaces, action-heavy dashboards.
- **Distinctive marker**: the radial expansion. Actions arc out, not stack.
- **Cost**: medium — spring physics + path math.

### Sticky in-page secondary nav
Once the user scrolls past the hero, a thin secondary nav often pins to the top with section anchors (Overview, Features, Pricing, FAQ).

- **When to use**: long marketing pages, product pages with deep content.
- **Distinctive marker**: quietly provides a table of contents without forcing it.
- **Cost**: low — sticky position + scroll-spy.

### Persona-led nav dropdown
"Solutions" or "Use cases" as a dropdown, with entries oriented to user roles (startups, agencies, finance teams, creators) rather than to features.

- **When to use**: products serving multiple verticals or personas.
- **Distinctive marker**: the orientation is "who you are" not "what we do."
- **Cost**: low — content discipline + dropdown.

### Brutalist horizontal rail
Uppercase monospace links separated by vertical bars (`|`) or directional markers. Active state inverts: link sits inside a solid block of foreground color with background-colored text.

- **When to use**: industrial / brutalist styles.
- **Distinctive marker**: the inversion. No hover lift, no underline animation — the inversion is the entire interaction.
- **Cost**: zero — CSS.

---

## Section-flow patterns

The structural spine of a premium marketing page. Different cohorts converge on different IA, but the variations are predictable.

### Canonical premium B2B flow

1. **Hero** — value-prop + sub + 1-2 CTAs + product image or short motion. Above-the-fold on a 1440×900 viewport with room to spare.
2. **Social proof strip** — logo marquee of customers, single row, monochrome. Immediately after hero.
3. **Problem framing / "old way vs. new way"** — short section naming the friction users experience today. Sometimes a side-by-side comparison.
4. **Core feature pillars (3-4)** — each pillar is a row with screenshot + headline + 2-3 bullet outcomes. Alternating image-left, image-right.
5. **"How it works" — numbered step sequence (3-5 steps)** — each step with number, title, short description, small visual.
6. **Use-case / industry / persona section** — platform applied to different contexts.
7. **Outcome / ROI section** — customer quote + headline metric ("21x faster", "$3M saved").
8. **Trust & security section** — compliance badges + short paragraph on posture.
9. **FAQ section (optional)** — 5-8 questions, accordion-collapsed.
10. **Final CTA section** — restated value-prop, single filled CTA, tinted background.
11. **Footer** — navigation + secondary links + small print.

### Editorial / AI / fintech flow (pyramid descent)

1. **Hero / thesis** — one big statement of what we are.
2. **Product pillars** — small number (often three) of named product modules, each with its own card.
3. **Feature deep-dives** — alternating column rhythm walking through the most important capabilities.
4. **Evidence layer** — customer logos, then a testimonial or two, then a stat strip.
5. **Trust/safety/security band** — relevant especially to fintech and AI, framed in calm UI rather than dramatic icons.
6. **Press / external validation** — headline-style mentions, treated like newspaper clippings.
7. **Final CTA** — repeat of the hero CTA.
8. **Footer sitemap** — dense, navigable.

### Developer-tooling flow

1. **Hero** — headline + subhead + primary/secondary CTA + product fragment (code sample, terminal, dashboard fragment).
2. **Trust strip** — 6-12 customer logos, monochrome, evenly weighted.
3. **Three-up value props** — what the product gives you, in 3 cards or 3 columns.
4. **Deep-feature section #1** — a single feature blown out, often with a real code sample or terminal as the visual.
5. **Deep-feature section #2** — a different angle — integrations, scale, security, pricing — visualized with a diagram or a dashboard fragment.
6. **Quotes / testimonials** — 2-4 quotes from named engineers at known companies. Photo, name, title, company. Often with a measurable result attached.
7. **Tertiary content** — blog/changelog teaser, docs callout, community card.
8. **Footer CTA** — large display headline restating the value prop, primary CTA, secondary "talk to us" link.
9. **Site footer** — 4-8 column link map, status indicator, locale switcher.

### Creative / productivity flow

1. **Hero** — short headline + 1-line subhead + 2 CTAs sits in the top 40% of the fold; the bottom 60% is an interactive demo, an animated product cluster, or a hero canvas with the product in motion.
2. **Logo wall** — customer trust within the first 800-1000px of scroll. The logo wall is a permission slip for the deep-scroll.
3. **Three to five major feature sections** — deep visuals, not 8-12 thin tiles.
4. **Templates and community gallery** — horizontal-scroll carousel of templates or example projects.
5. **Pricing teaser** — single line + link to full pricing.
6. **Final CTA section** — full-bleed accent color, 100+ pixel display headline, single CTA.
7. **Footer** — 4-6 columns sprawling but disciplined.

### AIDA mapping (cross-cohort)

- **Attention**: hero.
- **Interest**: problem framing + core feature pillars.
- **Desire**: how it works + ROI + customer outcomes.
- **Action**: final CTA.
- **Trust/security pre-empts Desire-to-Action objections** — placed deliberately just before the close.

### Section flow rules

- **Trust signals stack progressively through the page.** Logos (hero proximity) → quantified outcomes (mid-page) → security/compliance (pre-CTA).
- **Pricing is teased on the homepage, not detailed.** Full pricing tables on the homepage feel sales-y. A single "starts at $X" or "free to start" line plus a link to the full pricing page is the typical move.
- **Testimonials appear after the buyer has seen what the product does.** Testimonials shown too early feel like deflection.
- **One CTA goal, repeated.** Hero CTA, mid-page CTAs, pre-footer CTA all push toward the same action.
- **Final CTA gets the heaviest typography.** The closer earns the visual weight the hero held back from.
- **Footer is sitemap, not filler.** 4-6 columns by audience (Product, Solutions, Resources, Company, Legal).

---

## Imagery treatments observed

A catalog of how premium products use imagery. Premium surfaces refuse to substitute stock photography for actual product.

### Real product UI as primary visual
Hero, features, and proof sections lean overwhelmingly on real (or realistic-looking composite) product UI. Stock photography is nearly absent.

- **Distinctive marker**: the product is the product. Marketing illustration is rare.
- **Source**: real screenshots, or pixel-perfect HTML/CSS rebuilds for scalability.

### Annotated UI screenshots
Product UI shown with subtle callouts, inline labels, or small badges pointing to specific features. Annotations are restrained — a thin line and a short label, never a giant numbered circle.

- **Distinctive marker**: the screenshot becomes a small editorial diagram.
- **Source**: overlay markup on the screenshot.

### Close-cropped feature shots
Not the whole app at 30% zoom — a tight crop on the specific feature being discussed. Real-looking data inside (real-sounding company names, plausible numbers, realistic timestamps).

- **Distinctive marker**: the crop. Premium screenshots show ONE thing well.
- **Source**: design discipline.

### Floating screenshot with soft drop shadow
Subtle 12-24px corner radius. Box-shadow at low opacity, high blur (e.g., `0 24px 64px rgba(0,0,0,0.08)`). The screenshot floats above the page without harsh edges.

- **Distinctive marker**: the shadow is barely there. Heavy shadows read as 2018-era card-elevation aesthetic.
- **Source**: CSS treatment on `<img>`.

### Tilted product frame
Subtle Y-axis tilt + perspective shadow turns a screenshot from "documentation" into "object."

- **Distinctive marker**: the framing. The screenshot is no longer documentation; it's an artifact.
- **Source**: CSS transform.

### Stacked-card collage
2-4 UI fragments layered at varying z-depths — a panel, an overlay, a tooltip, a popup. Creates dimensional composition.

- **Distinctive marker**: choreographed overlap. Implies "several features at once" without overwhelming.
- **Source**: z-stacking + intentional crop.

### Ghost-cursor screenshots
Static screenshots show fake collaborator cursors with name labels, simulated typing indicators, or active selection states. Plausible names (not "User1") that suggest a team is actually working.

- **Distinctive marker**: proves multiplayer without motion.
- **Source**: overlay markup with cursor positioning.

### Before/after transformation panel
Two-panel comparison: messy input left, clean output right, often with an arrow or wand glyph between. Demonstrates value without explanation.

- **When to use**: AI products, transformation features, magic-trick demos.
- **Distinctive marker**: the transformation is the demo.
- **Source**: layout discipline.

### Generated-output portfolio grid
For AI products: sample images, audio waveforms with transcript captions, sample text in an editor, placed in the layout AS IF they were portfolio pieces. The output is the proof.

- **When to use**: generative AI products.
- **Distinctive marker**: the output is invited to be evaluated as work, not described as a capability.
- **Source**: curated assets + grid layout.

### Monochrome customer logo wall
6-10 customer logos in a single row, all desaturated to the page's neutral text color, at uniform optical weight. Spaced with generous gutters. Introduced by a short label ("Working with", "Trusted by teams at").

- **Distinctive marker**: the harmony. Removes visual chaos; the wall reads as a single block.
- **Source**: CSS filter or pre-rendered greyscale assets.

### Auto-scrolling logo marquee
Customer logo rows infinite-scroll horizontally at 20-40 seconds per loop — slow enough that the eye doesn't snap to motion, fast enough that the row never feels static.

- **Distinctive marker**: sub-conscious speed. Pauses on hover so users can read.
- **Source**: CSS keyframe animation.

### Editorial-framed customer portrait
Photography of founders or customers shot in real environments (offices, studios) and treated with editorial restraint — natural lighting, no heavy retouching, no stock-photo gloss. Portraits at 4:5 or near-square with generous negative space.

- **When to use**: testimonials, customer proof, founder stories.
- **Distinctive marker**: real environments. Stock-photo gloss is absent.
- **Source**: real photography production. Multiple aspect-ratio crops for responsive art direction.

### OS chrome preserved
Real macOS / Windows / iOS chrome around product screenshots — the menubar, traffic lights, status bar — grounds the product as software you actually run.

- **Distinctive marker**: stripping OS chrome makes screenshots look like prototypes. Keeping it grounds them.
- **Source**: design discipline.

### Mesh gradient hero background
3-5 large, blurred radial gradients in brand colors, drifting slowly (4-8s ease loops, 3-6px translation). Positioned out of the safe text area so contrast on copy stays consistent.

- **When to use**: high-end maximalist styles.
- **Distinctive marker**: cheap to implement, expensive-looking. The hero feels alive without distracting.
- **Source**: CSS radial gradients + slow animation.

### Per-section accent color in product UI
The product itself often shows interface chrome tinted to match the section accent — a "color match" between marketing surface and product surface. The screenshot is a styled render where the accent is tuned to the surrounding context.

- **Distinctive marker**: coherence signal almost no enterprise site bothers with.
- **Source**: per-section asset variants.

### Custom illustration (restrained)
Flat-vector or low-poly 3D in the site's accent palette. Geometric blobs, abstract isomorphic objects, stylized "tools in space" compositions. Monochrome or near-monochrome.

- **When to use**: a concept is too abstract for a screenshot.
- **Distinctive marker**: never stock illustration. Never generic isometric people.
- **Source**: custom illustration work.

### Diagrams matching the visual system
Flowchart-style explainer diagrams (boxes with arrows, layered stacks, network meshes) appear for architecture or workflow features where a screenshot would mislead. Styled to match the rest of the visual system — same corner radii, same accent colors, same line weights.

- **Distinctive marker**: the diagrams feel like part of the system, not a Visio export.
- **Source**: design discipline.

### Hand-drawn annotation overlays
Underlines, circles, arrows in a sketchy aesthetic atop hero copy. One per page maximum.

- **When to use**: brand voice that wants warmth without slipping into cute.
- **Distinctive marker**: used sparingly. More than one per page reads as decorative chaos.
- **Source**: hand-drawn SVG overlays.

### Decorative dot-grid or fine-line pattern background
Visible only on inspection, but gives the page a "plotted on a working grid" feel.

- **When to use**: subtle spatial-feel backgrounds on calm sections.
- **Distinctive marker**: visible only on close inspection. Adds rhythm without competing.
- **Source**: CSS background or SVG pattern.

### Lifestyle photography (rare in B2B premium)
Real photography, when present, is atmospheric and abstract rather than literal. Soft-focus natural elements (water, light, fabric, sky) as metaphor for feelings the product is meant to evoke.

- **When to use**: support and customer-experience categories.
- **Distinctive marker**: not literal. Mood, not subject.
- **Source**: photo production or curated stock that doesn't read as stock.

---

## Content & copy voice patterns

A catalog of voice moves observed across premium surfaces. Voice converges across cohorts: calm, direct, specific, short.

### Headline construction patterns

**Imperative verb + concrete outcome**
"Stop reading documents. Start making decisions."
"Build better sites, faster."
"Replace manual work with automated workflows."

- Verb does the heavy lifting; noun phrase grounds it.
- Sentence case throughout. Title Case reads as advertising copy from a previous decade.

**Problem-then-solution two-line construction**
"Old approach is broken. New approach is here."
- Many headlines are two short sentences.
- One names the friction, one names the resolution.

**Thesis statement**
"Building [X] to do [ambitious thing]."
"[Category] designed for [specific human problem]."
- Confident statement of position. Reads like the opening line of an essay.

**Headline + deflating qualifier**
"Make anything possible — in one tool."
"Build better sites, faster."
- Big claim + small honest constraint. The constraint is what makes the claim believable.

**Subhead specificity**
The line under the headline names a measurable outcome.
"21x faster", "60% reduction in unqualified calls", "from days to minutes".
- Numbers do more persuasion than adjectives.

**Subhead clarification, never echo**
Common rookie mistake: subhead restates the headline in different words. Premium surfaces use the subhead to give one specific clarifying detail (what audience, what context, what unique angle).

### CTA copy patterns

**Action-verb CTAs naming the next concrete step**
"Book a demo", "Start free", "See it in action", "Open account", "Run the demo".
- Avoid "Learn more" — verb of inaction.
- The CTA verb matches the product verb. If the product deploys, the CTA is "Deploy." If it queries, "Run a query."

**Single primary action per section**
Exactly one filled button per section, with all other interactivity demoted to text or ghost buttons.
- The visitor never has to choose between two equal options.

**No "Get Started" reflex**
When a more specific verb is available, use it. "Get Started" appears only as a fallback.

### Testimonial framing patterns

**Quotes lead with the result, not the praise**
"We cut review time by 40%" beats "The team loves it."
"We cut p99 from 380ms to 90ms" beats "Great product."
- Premium testimonials are case-study fragments, not vibes.

**Attribution required**
Name + role + company at minimum. Quotes with no attribution read as fabricated.

**Customer voice unornamented**
Set the quote at body-plus size, regular weight, with name + role beneath. No oversized quotation marks, no decorative quote-card chrome.

**Customers carry the superlatives**
Where bragging happens ("the best CRM I've used", "next generation"), it comes from named customers, not from the brand itself.

### Specificity patterns

**Numerical specificity replaces adjectives**
"75ms latency" beats "blazingly fast".
"1.5% cashback" beats "industry-leading rates".
"3-day onboarding" beats "fast onboarding".
"98% of category leaders" beats "trusted by leaders".

**Use numbers where they exist; write around them where they don't**
The cohort never lets a vague modifier sit alone. If the real number isn't available, restructure the sentence.

**Power language used sparingly**
Words like "everywhere", "every team", "always", "the only" appear at most once per page. Overusing them flattens their impact.

### Microcopy patterns

**Calm celebration in success copy**
"50 points added" beats "Hooray! You earned 50 points!"
"Account ready" beats "Congratulations! Account created!"
- Tone stays level.

**Empty states are invitations**
"Connect your first integration to start" beats "No data yet."
"Nothing here yet — start with a template, or build from scratch" beats "Empty."
- Premium products assume the user is smart and just needs the next move named.

**Errors are specific and helpful**
"Phone number missing — add a number to continue" beats "Form contains errors."
"Couldn't reach the server. Try again, or check status" beats "Something went wrong."
- Errors name the field and the action.

**Confirmations narrate state changes**
"Phone verified." "Profile saved." "Connection paused."
- Short, declarative, no enthusiasm.

### Tone calibration patterns

**Calm confidence is the default register**
Premium B2B doesn't shout. It states. Two sentences usually finish the thought. One if you can land it.

**Direct without arrogant**
The voice reads like a senior engineer or designer describing their own work to a peer, not a sales deck.

**Light wit, used sparingly**
One joke per page, max. Sparingly used wit signals confidence; constant cleverness signals insecurity.

**Empathy beats hype**
"Skip the blank canvas", "Stop pasting between tools", "Keep work moving 24/7".
- Naming the user's existing pain in plain language, then showing the relief. Tends to convert better than aspirational copy.

**The user is the subject**
Second-person address ("you ship, you plan, you decide") appears often.
First-person plural ("we help you...", "we believe...", "our mission") rare in headlines.
Third-person abstraction ("users can...", "the platform provides...") treated as a failure of intimacy.

**Honest about AI limits**
Where AI features are described, premium products tend to use "drafts", "suggests", "tries" — not "writes", "creates", "knows".
The user remains the protagonist; the AI is the tool.

### Voice avoidances

- Exclamation marks in marketing copy. Confidence is performed by restraint.
- ALL-CAPS body or subhead copy. Reserved for eyebrow labels at 10-13px.
- Hyperbolic adjective stacks ("amazing", "world-class", "revolutionary"). Signal of weakness.
- Buzzword stacking ("AI-powered next-gen platform").
- Vague verbs (empower, unlock, accelerate, transform, leverage).
- Corporate hedging ("we believe", "we think", "our mission").
- "Trusted by 10,000+ developers" with no logos shown.
- Industry jargon used unless it's been earned.
- Filler verbs (Elevate, Seamless, Unleash, Next-Gen, Empower, Revolutionize).
- Question-form headlines as faux-rhetorical setup.

### Eyebrow / kicker label patterns

**Tracked uppercase microtype above section heads**
10-13px small caps in muted gray. Letter-spacing 0.05em-0.10em. Sits above the section headline, never below.
- Tiny labels that orient the reader without taking visual weight.
- Often preceded by a 6-8px colored dot or geometric mark.

### Feature-naming patterns

**Feature names that are nouns or noun-phrases**
"Workflows", "Agents", "Connectors", "Spaces", "Boosts".
- Not "Powerful Workflows", "Smart Agents".
- Naming a thing makes it real; describing a thing makes it brochure.

**Single-word feature names treated as proper nouns**
"Agents", "Spaces", "Boosts" — short, memorable, consistently capitalized.
- Becomes brand asset that gets reused across blog, docs, product.

---

## Color treatments observed by category

Color discipline converges by cohort. The category signals the palette.

### Dev tools / infrastructure (dark mode dominant)

**Background**: very-dark-neutral with a faint cool cast (L = 4-8% in OKLCH). Reads black at a glance but lets surfaces sit on top with visible-but-quiet elevation.

**Text**: rarely pure white. Primary text at L = 92-96% with a slight desaturated cast. Pure white reserved for strongest highlight or active focus.

**Accent**: single hue (saturated blue-cyan, sometimes violet, sometimes neutral-warm) carries CTA, link, and focus. Saturation high but lightness balanced for legibility. Separate tokens for light/dark modes, not a single hex.

**Semantic color**: reserved for semantics (green success, red error, amber warning). Shows up in product mockups, status pills, log lines — never as decoration.

**Surface elevation**: 4-5 step lightness ladder (page → card → raised → popover → overlay). Each step ~3-5% L lift.

**Borders**: hairline white at 8-12% alpha. Almost invisible but defines geometry crisply.

### Fintech / editorial (light mode dominant, restrained)

**Background**: off-white in the `#FAFAFA` to `#F7F6F3` range. Pure white reads as default; warm tints read as paper.

**Text**: deep charcoal in the `#171717` to `#1F1F1F` range. Brand mark and emphasized UI controls can drop to true black for contrast.

**Accent**: single restrained accent — often a saturated blue, muted teal, or warm tone. Appears exclusively on primary CTAs, key icons, small marker dots.

**Semantic color**: surgically used in product screenshots, not in marketing chrome.

**Borders**: 1px hairline at low contrast. `#EAEAEA` or `rgba(0,0,0,0.06)`.

### AI / research (restrained, no purple-gradient cliché)

**Background**: near-monochrome foundation. True white or off-white canvas. Near-black text.

**Accent**: at most one accent applied surgically. Often a desaturated tan, ochre, sand, or calibrated grey-blue — explicitly NOT purple-to-pink.

**Notable absence**: brain icons, sparkle icons, neural-network nodes, glowing dots, mesh gradients in the purple-pink window. The semantic vocabulary of AI iconography is absent.

**Substitute**: editorial language about research and direction. Numbers around accuracy, latency, model capability. Calm interface chrome around AI features — the same restrained neutral palette as the rest of the design.

### Creative tools (more permissive of color)

**Background**: pure neutrals form the chassis (white or near-white canvas with deep ink text).

**Accent**: bright, saturated, confident — not pastel. Electric teal, hot coral, vivid violet, acid green, deep magenta.

**Color use rules**:
- Accent used as full-bleed feature backgrounds, never as text color over white.
- Pastels appear only in soft-gradient backgrounds, never as primary accents.
- Two-color accent pairings rotated across sections rather than splattered both at once.

**Mesh and orb gradients** sit behind hero moments — soft blurred radial gradients (60-80% noise opacity, gaussian blur ~120px) in 2-4 colors. Animated subtly.

**Per-feature color codes** as a navigational device: a feature stack of 4-6 items will assign each a distinct color, then preserve that color in subnav, icon, and product UI screenshot tinting.

**Tinted shadows**: brand-colored shadows (violet glow under a violet card, teal mist behind a teal screenshot) replace neutral drop shadows.

**Dark mode** is a first-class surface, not an inversion. Separately art-directed gradients, separately calibrated accents.

### Brutalist / industrial (uncompromising)

**Light substrate**: warm matte off-white (`#F4F4F0` to `#EAE8E3`). Suggests unbleached documentation paper.

**Dark substrate**: deactivated CRT black (`#0A0A0A` to `#121212`). Slight lift reads as a real screen.

**Text**: near-black carbon ink (light substrate) or white phosphor (dark substrate). Never pure `#000` or pure `#FFF`.

**Accent**: a single aviation or hazard red (`#E61919`, `#FF2A2A`). Strike-throughs, structural dividers, warning stripes, vital data highlights. Never decorative.

**Optional terminal green** (`#4AF626`) on dark substrate — but only on a single specific element. Never as a general body color.

### Cross-category color rules

- Pure black (`#000000`) is uncommon. The "black" used for body text is typically a near-black with a slight blue or warm undertone.
- White is rarely `#FFFFFF` either. Off-whites in the `#FAFAFA` — `#F7F7F5` range give a paper-like warmth.
- Customer logos go monochrome. Never in their native brand colors.
- Section anchors via subtle background-color shifts (off-white → slightly-darker-off-white → near-black for one moment).
- One gradient feature per page, max.
- Semantic color stays consistent across the system. Green is success, red is destructive, amber is warning.

---

## Motion language observed by tier

Motion is restrained in premium cohorts. The premium ones tend to be slower and spring-physics-based. AI products are conspicuously avoiding the gradient cliché.

### Premium motion vocabulary

**Easing**: almost always a soft out-ease (`cubic-bezier(0.2, 0.8, 0.2, 1)` or similar). No bouncy spring. No linear motion outside loops.

**Durations**: cluster predictably:
- 150-200ms for hover state changes
- 250-350ms for entry reveals
- 600-900ms for major reveals
- 600-1200ms for cinematic transitions

**Scroll-triggered reveals**: small. A 4-8px translate combined with an opacity fade from 0.8 to 1. No 100px slide-ups, no rotation, no staggered cascades.

**Parallax**: 5-15% offset between foreground and background scroll speeds. Subtle.

**Hover on CTA**: background brightens 2-4% L, sometimes a subtle inner glow for dark-mode primary buttons. No translate-on-hover for premium-feel buttons.

**Hover on cards**: lift -2 to -4px with shadow elevation. 200-300ms ease. Reserved for clickable cards.

**Number counters**: animate on enter-view (800-1500ms ease-out). Once, not on every scroll past.

**Code/terminal types itself**: a code block or terminal cursors a single line into existence on entry, then holds still. Once, not on loop.

**Spring physics on UI gestures**: drag handles, toggles, modal open/close use spring physics rather than cubic-bezier — the motion feels like the user moved something with weight.

### Creative-cohort motion variations

**Color transitions**: long, eased curves. Background-color and gradient transitions run 600-1200ms with custom cubic-bezier curves. Slowness reads as confidence.

**Hover states**: choreographed micro-events. A card hover does multiple things in concert: background lifts (translate -2px), shadow expands, border brightens, an inner icon rotates 10°, an arrow slides 4px right. The hover is a small show.

**Scroll-pinned product walks**: pin the visual, scrub through 4-6 states as the user scrolls. Storytelling without autoplay.

**Cursor-following glow**: subtle radial brand-color glow follows the cursor through hero canvases. Fades within 200ms of cursor stop.

**Magnetic micro-physics**: hero CTAs pull slightly toward the cursor. Implemented via motion library values, never `useState`.

**3D objects rotate on scroll, not autoplay**: marquee 3D renders rotate as the user scrolls, mapping scroll position to rotation. Couples motion with intent.

### Editorial / AI / research motion (most restrained)

**Motion is content-driven, not chrome-driven**. The largest motion surface is video — full-bleed product or generated output looping silently in the hero.

**Quiet entrance animations**: sections fade or rise into view as the user scrolls, but the distance is small (8-16px) and the duration is short (240-320ms).

**No parallax tricks, no scroll-jacking**. Refuses dramatic scroll hijacking — no horizontal-snap section, no pinned-3d-element, no scroll-controlled video scrubbing. The page scrolls like a magazine.

**Hover states are subtle and immediate**: links shift color or underline weight on hover without any decorative micro-animation.

**Reduced-motion is respected implicitly**: the motion vocabulary is so restrained that even users with `prefers-reduced-motion` lose almost nothing.

### Motion avoidances (across cohorts)

- Page-scroll-hijacking. Hijacking the scroll wheel reads dated and accessibility-hostile.
- Full-screen video autoplay with sound. Violates user expectation.
- Big animated number sequences as decoration. Counters not anchored to a real metric feel like a gimmick.
- Heavy drop shadows on dark surfaces. Shadows get swallowed or look smudgy.
- Bouncy spring animations on headline reveals. Spring physics belongs on gestures, not on type.
- Looping animations on the wordmark in the nav. Read as distracting.
- Device orientation / motion permission prompts for parallax. Pointer events only.
- Custom mouse cursors on the page (acceptable inside a scoped interactive demo surface).
- Auto-rotating carousels under 4 seconds per slide. Either continuous marquees or scroll-snap with visible affordance.
- Animation durations under 100ms or over 1500ms. Too fast = invisible; too slow = stuck.

### Reduced-motion behavior

**Brutalist**: skip scanline drift, glitch effects, slot-machine counters. Keep instant state changes.

**Minimalist**: replace translateY scroll entries with simple opacity fades, shorten durations.

**High-end**: drop the blur portion of scroll entries; replace cinematic interpolations with simple fades; pause background mesh animations.

---

## Distinctive techniques worth stealing across cohorts

A consolidated list of the cross-cohort moves that consistently signal premium taste.

### The mono-color logo wall
Force all customer logos to the page's text color. Removes visual chaos; the wall reads as a single block of social proof.

### Code as design content
Treat a code block like hero photography. Short, beautiful, cropped, with custom syntax theming that matches the page.

### Cropped real interfaces
Show a sliver of dashboard, not the whole thing. The crop implies "there's more here, and what you see is real."

### Eyebrow tag instead of section divider
Replaces decorative rules and icons with a tiny piece of semantic typography. Cheap and highly effective.

### Quantified subheads
Every subhead pulls in a number or a name. The reader is convinced by specifics before they've read the body.

### Type-anchored CTAs
The primary CTA is sometimes just type with an underline-on-hover, not a filled button. When the headline is doing the work, a filled button can compete; a text-link CTA defers.

### Tiered surface elevation in dark mode
A 4-5 step lightness ladder gives real depth without ever using a drop shadow that would look out of place on dark.

### Status pill in the nav
A 6px green dot + 12px caps text saying "all systems operational." Sells reliability without saying "reliable."

### Pulsing globe / animated map
Subdued, slow, low-saturation. Don't over-design it.

### "What's new" / changelog teaser
A small, dated, monospaced strip showing the most recent shipped change. Tells engineers "this thing is alive and being worked on."

### Per-section accent color in product UI
Color match between marketing surface and product surface signals the team controls both ends.

### Stacked-card collages instead of single screenshots
2-4 UI fragments at varying z-depths and tilts create depth and suggest "multiple features visible at once."

### Custom cursor inside demo surfaces
Cursor changes when the user mouses into the demo. Tiny touch, big "you're in the product now" moment.

### Fake collaborator cursors in screenshots
Static screenshots show ghost cursors with name labels mid-action. Proves multiplayer without motion.

### Tilted product frames at 6-12 degrees
Subtle Y-axis tilt + perspective shadow turns a screenshot from "documentation" into "object."

### Tinted shadows in brand colors
Drop shadows colored in the section accent rather than gray. Reads as expensive.

### Scrollytelling for feature deep-dives
Pin the visual, scrub through 4-6 states as the user scrolls. Storytelling without autoplay.

### Customer work galleries as social proof
A grid of actual user projects. Doubles as inspiration content for SEO.

### Headline + deflating qualifier structure
"Make anything possible — in one tool." Big claim + small honest constraint.

### A savings or ROI calculator on the homepage
Interactive input that estimates value. Converts abstract value into a personal number.

### Auto-scrolling logo marquees at sub-conscious speed
20-40 second loops on customer logos.

### Dark mode as a first-class surface
Not just inverted — separately art-directed gradients, separately calibrated accents.

### Templates and example projects as a section
Horizontal scroll carousel of starting points. Lets the user see "what I could make" before committing.

### Operational transparency in the footer
Green-dot status link to the status page. Performed trust signal.

### Single-word feature names as proper nouns
Short, memorable, capitalized consistently. Becomes brand asset.

### Bento-grid for "what's in the box"
Asymmetric tile grid with mixed aspect ratios. Tile size carries hierarchy.

### OS chrome preserved in screenshots
Grounds the product as real software.

### Variable-axis hover animation
Font weight tightening as cursor approaches. Almost imperceptible, deeply premium.

### Single-word gradient text
One word per page in a brand gradient. The rest stays plain.

### Magic-trick before/after panels for AI features
Messy input left, clean output right, glyph between.

### Tabular numerals for stats and pricing
Aligned columns. Subtle but signals discipline.

### Pre-footer full-bleed CTA strip
A loud band of brand color carrying the closing call. Earns its loudness by being last.

### Noise/grain overlay on flat color
3-6% opacity high-frequency noise on top of solid color blocks. Breaks the digital flatness.

### Hover-to-reveal animations on screenshots
A static product image plays a small loop only on hover. Engagement-gated motion.

### Scroll-scrubbed video instead of autoplay
Video frame advances with scroll position. User controls the pace.

### Spring-physics gestures on toggles and drag handles
Real weight in UI motion.

### Cursor-following glow on hero canvas
A radial brand-color glow tails the cursor through interactive surfaces.

### Annotated UI screenshots
Crop the product interface tightly, add a single thin line + label callout for each notable feature.

### Generated content as portfolio (for AI products)
Show generated outputs in the layout as if they were portfolio pieces. The output is the proof.

### Research / timeline band in the main scroll
For AI products and category-defining companies, a chronological band — model releases, milestones, papers.

### Greyscale logo strips with consistent vertical alignment
Make the partner logo band a band of muted neutrals at identical heights.

### Big display sentence with quiet paragraph beneath
Pair an oversized declarative headline with a 2-4 sentence calm paragraph beneath.

### Sentence-case display throughout
Every headline in sentence case. The page reads as essay rather than billboard.

### Dense footer as IA insurance
Compensate for an aggressively minimal scroll by giving the footer a dense, multi-column sitemap.

---

## Cross-cluster takeaways

What emerges when patterns are looked at across all premium clusters at once.

### Restraint is the strongest signal of competence

The most counter-intuitive lesson: the more confident the company, the quieter the design. Sites that lean hardest on glowing gradients, neon accents, and 3D chrome read as the LEAST technically credible. The premium signal is composure.

### Subtraction over addition

Premium pages are built on what they refuse to include. No second typeface. No second accent. No second CTA in the hero. No decorative AI iconography. No stock photo. No parallax. No scroll-jacking. No exclamation. No superlative.

Every removed element creates room for the remaining ones to land. The discipline to leave things out is the hardest pattern to copy.

### Specificity beats hyperbole everywhere

"75ms latency" beats "blazingly fast."
"1.5% cashback" beats "industry-leading rates."
"98% of category leaders" beats "trusted by leaders."
"We cut p99 from 380ms to 90ms" beats "great product."

Where a real number exists, it appears. Where it doesn't, the cohort restructures the sentence rather than reaching for an adjective.

### Imagery is real product, not stock

Premium surfaces refuse stock photography. The product is the product. Where humans appear, it's named customers in real environments, shot with editorial restraint.

### Motion is purposeful and short

Restraint dominates. Scroll-triggered reveals are tiny. Hover transitions are quick. Spring physics belongs on draggable UI elements, not on type. Scroll-jacking is rejected. Reduced-motion is honored implicitly because the motion vocabulary is small enough that reduced-motion users lose almost nothing.

### The one-CTA-per-section rule

Exactly one filled button per section, with all other interactivity demoted to text or ghost buttons. The visitor never has to choose between two equal options. This is the most reliable conversion move available.

### Trust signals stack progressively

Logos near the hero. Quantified outcomes mid-page. Security and compliance pre-CTA. By the time the user reaches the final CTA, every objection should be at least lightly addressed.

### One voice across surfaces

Marketing copy, in-product empty states, error messages, blog posts, docs — all sound like they were written by the same person. This is the discipline most companies break at the marketing/product seam; premium companies hold it tight.

### Sentence-case display is the modern default

Title Case Across Every Word In Headlines is an enterprise-software-circa-2014 tell. Sentence case prevails across all premium cohorts.

### Off-white over pure white, charcoal over pure black

The "premium" foundation is paper-feeling off-white and ink-feeling charcoal. Pure white reads as default; pure black reads as raw HTML.

### Dark mode is first-class, not inversion

Premium dark mode has its own gradient stops, its own accent calibrations, its own product screenshots. Not a CSS invert of the light version.

### Customer logos go monochrome

The harmony of the strip becomes the testimonial. Multi-color logo walls read as visually busy and uncurated.

### Numbers are visual punctuation

Every section has at least one number. A latency target, a pricing detail, a customer count, a region count, an uptime percentage. Numbers render large and monospaced. They function as the page's punctuation.

### Generic AI iconography is conspicuously absent

The premium AI cohort refuses purple-to-pink gradients, brain icons, sparkle icons, neural-network nodes. The colour assigned to "AI-ness" is more likely to be a desaturated tan, an ochre, or a calibrated grey-blue than a synthetic gradient. The intelligence is implied by the artefact, not by the chrome.

### The page is allowed to scroll

Premium pages don't try to cram every capability into one screen. The page scrolls. Each feature gets room. 3-5 marquee feature sections, not 8-12 thin tiles.

### Footer is generosity

Dense, multi-column, navigable. The footer compensates for an aggressively minimal scroll by restoring discoverability.

### One accent, used like punctuation

Premium pages have a single accent color used surgically — primary CTA, link state, focus ring, occasionally a small marker dot. Anything beyond this gets justified. The accent does not appear in section backgrounds, card chrome, illustration fills, or decorative dividers.

### The brief is the spec

Premium pages are short. If a section can be cut without losing the value-prop, cut it. The discipline isn't what to include — it's what to leave out.

### Whitespace is a design element, not a deficit

Sections with 96-160px of vertical padding tell the reader "this section matters." Cramming sections together flattens hierarchy.

### Conventions over cleverness

Logo top-left. Nav top or left. Search is a magnifying glass. Innovate when you know you have a better idea; otherwise honor convention so users can scan.

### Clarity over consistency

When making something significantly clearer requires slight inconsistency, choose clarity.

### Eliminate noise

Three sources of noise: shouting (too many things demanding attention), disorganization (things not grouped logically), clutter (too much stuff). Fix noise by removal, not addition. Start with the assumption every element is visual noise — guilty until proven innocent.

---

## Closing principle

The exemplar catalog is descriptive, not prescriptive. Every pattern here has been observed multiple times in premium real-world surfaces because the pattern works. The convergence isn't accident — it's the shape of taste in the current era.

Build with these patterns, not from a void. Pick the ones that fit the brief. Execute them with precision. Refuse the templated defaults that would dilute them.

The hardest pattern to copy is the discipline to leave things out. That is what every premium surface in every cohort shares — the restraint to refuse what doesn't serve the work.

Output that competes with the best in the world is built on subtraction more than addition. Read these patterns as a kit of moves and a longer list of things not to do. The taste is in the negative space.
