# Discovery protocol — ask first, never improvise

Every generation command (`/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-system`, `/ux-case-study`) **MUST** run the discovery protocol below before dispatching any sub-agent or writing any code. Improvisation is forbidden. The plugin's value is the discipline of the intake; the work is downstream of it.

A generation command that skips discovery is a bug.

---

## When to skip discovery (the only exceptions)

- The user explicitly passes `--skip-discovery` (they're an expert who knows what they want and accepts default-driven output).
- The user passes a fully-populated brief in a single message that already answers every required field. In that case, **verify the brief covers all required fields, then proceed.** If anything is missing, ask for the missing fields only.
- The user is iterating on an existing artifact (e.g., `/ux-fix --auto` on a prior audit). The earlier discovery is reused from `.ux/last-frame.json` or the relevant report.

In every other case, discovery is mandatory.

---

## The 10 required fields

Group these into 2–3 messages of 3–4 questions each. Don't dump all ten in a wall. Conversational delivery.

### 1. Brand identity
**Ask**: "Do you have a brand identity file, brand guidelines, design tokens, or a logo we should pull from? If yes, paste the path / URL / file. If no, say 'no brand' and I'll propose something restrained."

**Why**: Without brand identity, every design is a default. Worth one tight question.

### 2. Reference inspirations
**Ask**: "Drop 3–5 URLs or screenshots of designs you LIKE. Not for features — for the aesthetic feel. The bar for taste."

**Why**: References are the fastest way to align on intent. A picture is worth 100 paragraphs of style description.

**Read these references** before generating. Note the patterns they share and the patterns they avoid. The output should feel adjacent to the references, not adjacent to default-model output.

### 3. Product type & audience
**Ask**: "In one sentence: what is the product, and who is it for?"

**Why**: A SaaS landing for solo founders is not the same as a SaaS landing for enterprise procurement. The audience disambiguates dozens of downstream decisions (density, copy register, motion intensity).

### 4. Style direction
**Ask**: "Pick a style direction: **minimalist** (premium SaaS, fintech, editorial), **industrial / brutalist** (raw, hacker, indie), **high-end visual** (creator tools, design-heavy, premium consumer), **editorial** (case-study, content-led), **dev-tool dark** (developer tools, technical density), **playful** (consumer, creator, friendly), or **your call** if you want me to pick."

**Why**: Three of the four style libraries in `references/styles/library.md` are first-class citizens; the rest are subtypes. Picking one prevents blending later.

### 5. Voice
**Ask**: "What's the voice? Direct/warm/brief? Technical/dry? Friendly/witty? Editorial/restrained? Playful? Or pull voice from the brand brief you shared."

**Why**: Voice changes every CTA, every error message, every empty state, every section headline. Cannot be decided after generation.

### 6. Stack
**Ask**: "What stack? React + Tailwind, Next.js (App Router), Vue, Blade + Alpine + HTMX, vanilla HTML, Astro, Svelte? Or 'what we have' and I'll auto-detect from `package.json` / `composer.json`."

**Why**: Stack determines syntax, RSC boundaries, dependency verification rules, motion library defaults.

### 7. Imagery sources
**Ask**: "Imagery — real product screenshots, hero images, brand photos? Or use `picsum.photos` placeholders? Or describe specific images you want generated (e.g., 'a moody close-up of someone's hands on a laptop in a cafe')?"

**Why**: Imagery is mandatory (text-only walls are banned). Where the imagery comes from determines whether to call for assets, use placeholders, or describe an image-as-content plan.

### 8. Must-have patterns
**Ask**: "Any specific patterns you MUST have? Terminal mockup in hero, bento grid, interactive product demo, before/after slider, kinetic typography, animated data viz? Or pick freely from the arsenal?"

**Why**: Reading the brief tells you what the surface IS. Reading must-haves tells you what the user has already imagined.

### 9. Avoid list
**Ask**: "What do you specifically NOT want? Beyond the standard anti-slop bans — anything in YOUR taste that's a hard rule? (Example: 'no gradients anywhere', 'no dark mode', 'no hero video', 'no centered text', 'no testimonial sections')."

**Why**: Personal taste overrides the standard ban list. A user who hates gradients should not get the one "approved gradient" the arsenal allows.

### 10. The wow moment
**Ask**: "What's the ONE thing this design must do that lifts it above generic? Something a visitor would remember 24h later. A specific feature, motion, interaction, visual moment, or content beat."

**Why**: This is the most important question. Without an answer, the plugin produces a clean Apple-feel landing — competent and forgettable. With an answer, every other decision is in service of the wow moment.

---

## Optional follow-ups (ask if not covered)

- **Color preferences / accent color** — "Specific accent color or one we should pick from the brand?"
- **Dark/light/both** — "Light only, dark only, or both? If both, which is the primary?"
- **Mobile-first or desktop-first** — Default is mobile-first; ask if the audience is desktop-dominant (B2B admin, professional tools).
- **Sections / IA hint** — "Sections you know you want, in order? Or trust the AIDA default?"
- **Existing copy** — "Have copy already, or should I draft it?"
- **Animation appetite** — "Heavy motion, restrained, or static?"

---

## How to ask (delivery)

1. **Open with one tight framing sentence**: "Before I generate, I need to know a few things. The output is downstream of the inputs."
2. **Group into 2–3 messages.** First message: brand + references + audience (the highest-leverage trio). Second message: style + voice + stack. Third message: imagery + must-haves + avoid-list + wow.
3. **Never dump all 10 at once.** That's a form, not a conversation.
4. **Use multiple choice where natural** (style direction, stack), and free-form where it matters (wow moment, audience, avoid-list).
5. **Accept "your call" / "you decide" on any single field** but require the wow moment.

---

## What to do with the answers

1. **Save the discovery payload** to `.ux/last-frame.json` as the canonical brief for this generation session and downstream commands. Shape:
   ```json
   {
     "command": "ux-design",
     "timestamp": "<ISO8601>",
     "discovery": {
       "brand_identity": "<verbatim>",
       "references": ["<url-or-description>", ...],
       "audience": "<one-line>",
       "style": "<minimalist|industrial|high-end-visual|editorial|dev-tool-dark|playful|your-call>",
       "voice": "<verbatim>",
       "stack": "<verbatim>",
       "imagery": "<verbatim>",
       "must_have_patterns": [...],
       "avoid_list": [...],
       "wow_moment": "<verbatim>",
       "extras": {...}
     }
   }
   ```
2. **Read the brand identity file** if one was provided, and any reference URLs (via WebFetch). Synthesize what they share.
3. **Set the three dials** based on the style direction + audience + density signals from the references:
   - `DESIGN_VARIANCE` (1 perfect symmetry → 10 artsy chaos)
   - `MOTION_INTENSITY` (1 static → 10 cinematic)
   - `VISUAL_DENSITY` (1 art-gallery → 10 cockpit)
4. **Pick 2–4 arsenal patterns** that fit the brief + the wow moment.
5. **Dispatch the sub-agent** with the full discovery payload + the dials + the picked patterns + `references/styles/anti-slop.md` + the relevant arsenal entries embedded inline.
6. **Echo the discovery summary** in the output so the user can verify their intent landed.

---

## Hard rules for the discovery phase

- **Never assume.** If a field is ambiguous, ask. The cost of one clarification message is far lower than the cost of regenerating a misaligned design.
- **Never proceed without the wow moment.** Without it, you're producing default work. Push back if the user says "anything's fine" — ask for a concrete moment, even a tiny one ("the way the headline reveals on first scroll", "the brand-mark dot pulsing once on load").
- **Never substitute defaults for missing answers.** If the user skips a field, ask again or surface that you'll proceed with a default and what that default is, so they can intervene.
- **Always echo back the brief** before generating. Two sentences max: "Here's what I'm building. Stop me if any of this is wrong."

---

## Why this exists

The plugin's premise is that default model output has measurable, predictable failure modes. The biggest failure mode is **generating without enough constraint to make the output specific to the user's intent**. Asking 5–10 questions takes 2 minutes; it saves a generation that would have been 80% right and 100% rejected.

Apple-clean is not enough. Apple-clean is the floor, not the ceiling. The wow moment is what lifts a clean design into a memorable one — and the wow moment can only come from the user, not from the model.
