# Discovery Protocol — the 10-field design brief intake every ux plugin generation runs

The discovery protocol is the design discovery questions every generation command in the ux plugin runs before producing anything. Ten required fields. Two to three messages of conversational intake. Refuses to proceed without the wow moment. The protocol is the plugin's value — improvisation is banned, because the output is downstream of the inputs, and the inputs decide whether the work is generic or specific.

A generation command that skips discovery is a bug.

---

## Why discovery exists

Default model output has measurable, predictable failure modes. The biggest failure mode is generating without enough constraint to make the output specific to the user's intent. Asking 5-10 questions takes two minutes. It saves a generation that would have been 80% right and 100% rejected.

Apple-clean is not enough. Apple-clean is the floor, not the ceiling. The wow moment is what lifts a clean design into a memorable one — and the wow moment can only come from the user, not from the model. The model can produce a competent landing page from a vague brief. It cannot produce a landing page that someone remembers 24 hours later. That requires a specific intent, and the only place that intent exists is in the user's head.

Discovery extracts the intent into a structured payload that every downstream decision points back to. The brand identity decides the palette. The references decide the aesthetic. The audience decides the density and the register. The style direction picks the library. The voice writes every CTA and every error message. The stack determines syntax and dependency rules. The imagery decides whether to call for real assets, generate placeholders, or describe the image-as-content plan. The must-have patterns surface what the user has already imagined. The avoid-list locks in personal taste. The wow moment names what makes this specific build worth remembering.

Run discovery once, properly, and the next 90 minutes of generation is on rails. Skip discovery, and you spend three hours regenerating something that was always going to land 80% short.

---

## The 10 fields

The protocol asks 10 fields. Group them into 2-3 messages of 3-4 questions each. Do not dump all ten in a wall — that's a form, not a conversation.

### 1. Brand identity

**Ask**: "Do you have a brand identity file, brand guidelines, design tokens, or a logo we should pull from? If yes, paste the path / URL / file. If no, say 'no brand' and I'll propose something restrained."

**Why**: Without brand identity, every design is a default. The palette becomes Tailwind defaults. The type becomes Inter on Inter. The accent becomes the AI purple-blue. With brand identity — even minimal brand identity, even just a logo and a primary color — every downstream decision has an anchor.

**How to handle "no brand"**: Propose a restrained system. Not no system. Pick a monochrome base (off-black, off-white, a single mid-gray for borders) and one accent that fits the audience and style direction. Surface the choice explicitly so the user can override before generation. Never proceed with "I'll figure out the brand as I go" — that produces drift.

**What to extract**: Logo (link or pasted). Primary palette (hex values or a brand-guidelines page). Type pairing if specified. Voice file if pasted. Any specific motifs the brand uses (a dot, a stroke, a specific geometry).

### 2. Reference inspirations

**Ask**: "Drop 3-5 URLs or screenshots of designs you LIKE. Not for features — for the aesthetic feel. The bar for taste."

**Why**: References are the fastest way to align on intent. A picture is worth 100 paragraphs of style description. A user who says "make it minimalist" and points at Linear means something different than a user who says "make it minimalist" and points at Stripe. The references disambiguate.

**How to read references**: Pull each URL. Look at what they share, not what they each have. If all five references use a serif headline over a sans body, that's a pattern. If only one does, that's a one-off. The output should feel adjacent to the shared patterns, not adjacent to default-model output.

**What to extract**: Shared typography choices. Shared spacing rhythm (tight or loose?). Shared color discipline (monochrome with one accent? full palette?). Shared motion appetite (static, restrained, expressive?). Shared imagery treatment (photography, illustration, abstract, no imagery?). Shared layout patterns (asymmetric? grid? bento? full-bleed hero?).

### 3. Product type & audience

**Ask**: "In one sentence: what is the product, and who is it for?"

**Why**: A SaaS landing for solo founders is not the same as a SaaS landing for enterprise procurement. The audience disambiguates dozens of downstream decisions — density (operator dashboards are dense, marketing pages are airy), copy register (developer tools are dry, consumer apps are warm), motion intensity (B2B is restrained, creator tools are expressive), trust signals (enterprise needs logos and case studies, indie products need code samples and screenshots).

**The one-sentence pitch**: It must name the product, the audience, AND the wedge. "A loyalty platform for MENA partners" is fine. "A loyalty platform for partners" is too vague. "A loyalty platform for restaurant owners in Amman who run on Odoo" is sharp — the audience implies the integration, the locale, the partner-side ERP, the cultural-fit requirements.

**What to extract**: Audience density (operator / consumer / developer / mixed). Audience sophistication (technical / non-technical). Audience desperation (curious browsing / urgent need / contract-signed). Audience scale (solo / small team / enterprise).

### 4. Style direction

**Ask**: "Pick a style direction: **minimalist** (premium SaaS, fintech, editorial), **industrial / brutalist** (raw, hacker, indie), **high-end visual** (creator tools, design-heavy, premium consumer), **editorial** (case-study, content-led), **dev-tool dark** (developer tools, technical density), **playful** (consumer, creator, friendly), or **your call** if you want me to pick."

**Why**: Three of the four style libraries in `references/styles/library.md` are first-class citizens — minimalist, industrial, high-end visual. The rest are subtypes. Picking one prevents blending later, which produces incoherent output. A minimalist landing with brutalist details and high-end-visual photography looks like the model couldn't decide. Picking one means every reference, every token, every layout decision points the same direction.

**How to handle "your call"**: Acceptable on this field. Pick based on the audience + the references. If the references skew Linear / Stripe / Vercel, pick minimalist. If they skew Render / Fly / indie SaaS, pick dev-tool dark. If they skew Apple / Vercel marketing pages, pick high-end visual. Surface the pick explicitly before proceeding so the user can override.

**What to extract**: One named style direction. Any modifiers (e.g., "minimalist but with a single bold color block per section"). Confirmation that the direction matches the references.

### 5. Voice

**Ask**: "What's the voice? Direct/warm/brief? Technical/dry? Friendly/witty? Editorial/restrained? Playful? Or pull voice from the brand brief you shared."

**Why**: Voice changes every CTA, every error message, every empty state, every section headline. It cannot be decided after generation — the model commits to a voice on the first H1 and the entire surface has to harmonize. A direct voice on the headline with a marketing-filler voice on the CTA reads as confused. A warm voice on the welcome state with a cold voice on the error state reads as broken.

**The voice rubric**: direct / warm / brief / technical / dry / friendly / witty / editorial / restrained / playful. Combine 2-4 adjectives. Examples: "direct, warm, brief, unpretentious" (Dot voice). "Dry, technical, no exclamation marks" (developer tool). "Warm, witty, occasionally cheeky" (consumer app). "Editorial, restrained, third-person" (case-study site).

**What to extract**: 2-4 voice adjectives. Any explicit banned words ("never say 'just'", "no exclamation marks"). Any required terminology (specific product names, brand-specific verbs). The locale-specific voice tweaks if multi-locale.

### 6. Stack

**Ask**: "What stack? React + Tailwind, Next.js (App Router), Vue, Blade + Alpine + HTMX, vanilla HTML, Astro, Svelte? Or 'what we have' and I'll auto-detect from `package.json` / `composer.json`."

**Why**: Stack determines syntax, RSC boundaries (for Next.js App Router), dependency verification rules, motion library defaults, accessibility patterns. A component that works in React might not translate cleanly to Blade. A motion pattern that uses Framer Motion needs to be rewritten for Vue. The agent picks the right library defaults per stack — Framer Motion for React, GSAP for Vue, CSS transitions + Alpine `x-transition` for Blade.

**How to handle "what we have"**: Auto-detect. Read `package.json` for Node-based stacks. Read `composer.json` for PHP. Look for `tailwind.config.js`, `next.config.js`, `vite.config.js`, `nuxt.config.js`, `astro.config.mjs`. Surface what was detected before generation so the user can correct.

**What to extract**: Named stack with version if specified (Next.js 14 App Router, Vue 3 Composition API, Laravel 11 Blade). Existing component libraries (HeroUI, Radix, shadcn, Vuetify, Element). Existing motion libraries already in `package.json`. Existing token systems already in place (Tailwind config, CSS variables, design system folder).

### 7. Imagery sources

**Ask**: "Imagery — real product screenshots, hero images, brand photos? Or use `picsum.photos` placeholders? Or describe specific images you want generated (e.g., 'a moody close-up of someone's hands on a laptop in a cafe')?"

**Why**: Imagery is mandatory — text-only walls are banned. Where the imagery comes from determines whether the agent calls for real assets (and where to put them), uses placeholders (and which placeholder URLs), or describes an image-as-content plan (so the user can generate the images via Midjourney/Stable Diffusion/DALL-E and drop them in).

**The three modes**:

- **Real assets** — the user has files or URLs ready. The agent references the file paths in the output (with width/height, descriptive alt, lazy loading, AVIF/WebP with fallback).
- **Placeholders** — the user wants to ship the build with `picsum.photos` or `placehold.co` URLs. The agent picks dimensions and surfaces the placeholder pattern. The output ships with a clear "REPLACE BEFORE DEPLOY" comment block.
- **Described generations** — the user wants specific images that don't exist yet. The agent writes the prompts inline as comments alongside the image references, so the user can paste them into their image generator. The output ships with `{TODO_FILL}` placeholders for the file paths.

**What to extract**: Mode. File paths or URLs if real. Generation prompts if described. Dimensions per image slot.

### 8. Must-have patterns

**Ask**: "Any specific patterns you MUST have? Terminal mockup in hero, bento grid, interactive product demo, before/after slider, kinetic typography, animated data viz? Or pick freely from the arsenal?"

**Why**: Reading the brief tells the agent what the surface IS. Reading must-haves tells the agent what the user has already imagined. A user who says "terminal mockup in hero" has visualized the hero already — the agent's job is to deliver that vision, not invent a different hero.

**The arsenal**: 60+ patterns documented in `references/styles/arsenal.md` — terminal-mockup, bento-grid, kinetic-headline, magnetic-cta, asymmetric-bento, scroll-tied-3d, before-after-slider, interactive-demo, animated-data-viz, sticky-feature-scrollytell, intelligent-list, command-input, live-status, wide-stream, contextual-focus (dashboard-specific), and dozens more. The agent picks 2-4 patterns that fit the brief + style direction + audience.

**What to extract**: Named patterns the user must have. Any patterns the user has seen and wants to adapt (point at the reference). Permission to pick freely vs. constraint to specific patterns.

### 9. Avoid list

**Ask**: "What do you specifically NOT want? Beyond the standard anti-slop bans — anything in YOUR taste that's a hard rule? (Example: 'no gradients anywhere', 'no dark mode', 'no hero video', 'no centered text', 'no testimonial sections')."

**Why**: Personal taste overrides the standard ban list. A user who hates gradients should not get the one "approved gradient" the arsenal allows. A user who hates testimonial sections should not get one even if the audience is "trust-sensitive enterprise." The avoid-list is the user's veto, and the agent respects it without arguing.

**Standard bans vs. personal bans**: Standard bans are in `references/styles/anti-slop.md` — Inter on brand surfaces, purple-blue gradients, three equal cards, "John Doe", marketing filler verbs. These apply always. Personal bans are additive — they go ON TOP of the standard bans. A user who says "no hero video" gets no hero video, even though hero video is allowed by the standard.

**What to extract**: Specific items the user does not want. Where the bans apply (everywhere, or just specific surfaces). Any nuance ("gradients OK in icons, never in backgrounds").

### 10. The wow moment

**Ask**: "What's the ONE thing this design must do that lifts it above generic? Something a visitor would remember 24h later. A specific feature, motion, interaction, visual moment, or content beat."

**Why**: This is the most important question. Without an answer, the plugin produces a clean Apple-feel landing — competent and forgettable. With an answer, every other decision is in service of the wow moment. The arsenal pattern picks fit the wow moment. The motion intensity tunes to it. The imagery serves it. The headline anchors it.

**What counts as a wow moment**: A specific feature ("the brand dot pulses once on first load, then settles"). A specific motion ("the hero terminal types out the actual product CLI output as the user scrolls"). A specific interaction ("hovering the pricing card reveals a personalized cost calculator"). A specific visual moment ("the page transitions from light to dark as the user scrolls into the technical section"). A specific content beat ("a one-sentence manifesto centered between empty fields above and below — the only centered text on the page").

**Push back on "anything's fine"**: The user is not done with the protocol until they have a wow moment. The agent asks again with a more specific prompt — "Even something small. The way the headline reveals on first scroll. The brand-mark dot pulsing once on load. The transition between sections. What's the one thing?" If the user genuinely has nothing, the agent surfaces what it would pick and asks the user to confirm or override before proceeding.

**What to extract**: One sentence describing the wow moment. The dimension it lives in (motion, interaction, visual, content). The arsenal patterns that support it.

---

## Optional follow-ups

Ask if not covered by the 10 fields:

- **Color preferences / accent color** — "Specific accent color or one we should pick from the brand?"
- **Dark / light / both** — "Light only, dark only, or both? If both, which is the primary?"
- **Mobile-first or desktop-first** — Default is mobile-first; ask if the audience is desktop-dominant (B2B admin, professional tools).
- **Sections / IA hint** — "Sections you know you want, in order? Or trust the AIDA default?"
- **Existing copy** — "Have copy already, or should I draft it?"
- **Animation appetite** — "Heavy motion, restrained, or static?"

These are not required. They are nice-to-have signals that further refine the dials.

---

## When to skip discovery

Three conditions. The only three conditions.

- **`--skip-discovery` flag.** The user explicitly opted out. They're an expert who knows what they want and accepts default-driven output. The agent proceeds with sensible defaults and surfaces what they were before generation.
- **Complete spec in one message.** The user pasted a fully-populated brief that already answers every required field. The agent verifies the brief covers all 10 fields, then proceeds. If anything is missing, the agent asks for the missing fields only — not the whole protocol.
- **Iteration on a prior artifact.** The user is running `/ux-fix --auto` against a prior audit, or rerunning `/ux-design` against an existing `.ux/last-frame.json`. The earlier discovery is reused.

In every other case, discovery is mandatory.

---

## How to ask (delivery rules)

The protocol is a conversation, not a form. Five rules.

1. **Open with one tight framing sentence.** "Before I generate, I need to know a few things. The output is downstream of the inputs." One line. Sets expectation.
2. **Group into 2-3 messages.** First message: brand + references + audience (the highest-leverage trio). Second message: style + voice + stack. Third message: imagery + must-haves + avoid-list + wow moment.
3. **Never dump all 10 at once.** A wall of 10 questions is a form. The user disengages, gives one-word answers, and the protocol fails.
4. **Use multiple choice where natural.** Style direction, stack — these have a small set of valid answers. List them. Free-form where it matters — wow moment, audience, avoid-list. Don't constrain the answers that need range.
5. **Accept "your call" / "you decide" on any single field, except the wow moment.** "Your call" on style direction is fine — the agent picks based on audience + references. "Your call" on the wow moment is not fine. Push back until the user names one.

---

## What to do with the answers

Six steps after the user finishes the protocol.

1. **Save the discovery payload to `.ux/last-frame.json`.** This is the canonical brief for this generation session and every downstream command. The shape is:
   ```json
   {
     "command": "ux-design",
     "timestamp": "<ISO8601>",
     "discovery": {
       "brand_identity": "<verbatim>",
       "references": ["<url-or-description>", "..."],
       "audience": "<one-line>",
       "style": "<minimalist|industrial|high-end-visual|editorial|dev-tool-dark|playful|your-call>",
       "voice": "<verbatim>",
       "stack": "<verbatim>",
       "imagery": "<verbatim>",
       "must_have_patterns": ["..."],
       "avoid_list": ["..."],
       "wow_moment": "<verbatim>",
       "extras": {}
     }
   }
   ```

2. **Read the brand identity file** if one was provided. Read the reference URLs via WebFetch. Synthesize what they share.

3. **Set the three dials** based on the style direction + audience + density signals from the references:
   - `DESIGN_VARIANCE` (1 perfect symmetry → 10 artsy chaos)
   - `MOTION_INTENSITY` (1 static → 10 cinematic)
   - `VISUAL_DENSITY` (1 art-gallery → 10 cockpit)

4. **Pick 2-4 arsenal patterns** that fit the brief + the wow moment.

5. **Dispatch the sub-agent** with the full discovery payload + the dials + the picked patterns + `references/styles/anti-slop.md` + the relevant arsenal entries embedded inline.

6. **Echo the discovery summary** in the output so the user can verify their intent landed. Two sentences max: "Here's what I'm building. Stop me if any of this is wrong."

---

## Hard rules for the discovery phase

Four rules. Non-negotiable.

- **Never assume.** If a field is ambiguous, ask. The cost of one clarification message is far lower than the cost of regenerating a misaligned design. A user who says "minimalist" and lists references that include both Linear and Apple needs a follow-up — those are different minimalisms.
- **Never proceed without the wow moment.** Without it, the output is default work. Push back when the user says "anything's fine." Ask for a concrete moment, even a tiny one. The brand-mark dot pulsing once on load is a wow moment. The headline reveal on first scroll is a wow moment. The transition between sections is a wow moment. Something specific. Always.
- **Never substitute defaults for missing answers silently.** If the user skips a field, ask again. If they skip again, surface that the agent will proceed with a default and what that default is, so they can intervene. Never let a default sneak in unannounced.
- **Always echo back the brief before generating.** Two sentences max: "Here's what I'm building. Stop me if any of this is wrong." This is the last opportunity to catch a misaligned brief before generation burns minutes.

---

## What the protocol prevents

Three specific failure modes the protocol prevents, listed for clarity on what the discipline is buying:

- **Generic output.** Without discovery, the model produces the average of its training data — Inter on Inter, purple-blue gradient hero, three equal cards, marketing-filler CTAs. With discovery, the output is specific to the user's intent — their brand, their audience, their wow moment.
- **Misaligned output.** Without discovery, the model guesses at the audience and the voice. Sometimes it guesses right. More often, it guesses "consumer-friendly with light marketing energy" because that's the modal training example, and then the user — who is shipping a developer tool — has to throw the whole generation away. With discovery, the audience is named upfront and the voice is calibrated to it.
- **Half-finished output.** Without discovery, the model picks a few arsenal patterns at random and produces a surface that has some good moments and some generic moments. The user spends an hour patching the generic parts. With discovery, the wow moment is named and every pattern pick serves it. The surface is coherent on first generation.

The protocol takes two minutes. It saves two hours. The math is not subtle.

---

## What the user gets back

After the protocol completes and generation runs, the user receives:

1. The generated artifact in the target stack (code blocks with filename headers).
2. An echo-back of the discovery payload so the user can verify the intent landed (one sentence summarizing audience + style + wow moment).
3. A self-review naming which 3+ anti-slop bans were consciously avoided, which arsenal patterns were used and where in the code, and specifically how the design delivers the wow moment from discovery.
4. For public-web outputs: confirmation that the full SEO surface ships (title, description, canonical, OG, Twitter, JSON-LD, semantic HTML, image discipline, CWV-friendly patterns).
5. `.ux/last-frame.json` written so every subsequent command — `/ux-audit`, `/ux-polish`, `/ux-fix`, `/ux-case-study`, `/ux-next` — has the canonical brief to anchor to.

That last point matters. Discovery isn't just for the current generation. It's the foundation for every audit, every polish pass, every case study, every "what should I do next" conversation that follows. Run it once, properly. Everything downstream benefits.

---

**See also**: [Installation](Installation) · [All 17 Commands](All-17-Commands) · [All 5 Sub-Agents](All-5-Sub-Agents)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
