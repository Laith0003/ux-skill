# Visual Translation

How to translate a visual reference — a screenshot, mockup, photograph, sketch, or generated image — into working frontend code. The job is not to "be inspired by" the reference. The job is to translate it faithfully into real frontend, then resolve the gaps the reference leaves behind.

Drift kills more designs than ambition. This document codifies the discipline that prevents drift.

---

## The mandatory order

For any visually important task, the order is fixed:

1. **Visual reference is produced or sourced first.**
2. **The reference is deeply analyzed as a specification.**
3. **Implementation begins only after analysis is complete.**

If image generation is available and the task is visual ("a beautiful hero," "a premium landing," "a creative product page"), generate the reference yourself before writing any code. Do not start with freeform coding and try to discover the design in the IDE. The reference is the source of truth; the code is the translation layer.

Direct-code-first is acceptable only when the task is a bug fix, a structural refactor, or the brief is so precise that it already serves as a specification. In every other case, a reference comes first.

---

## Methodology phases

The work has six phases. They are sequential — each phase consumes the output of the prior phase. Skipping ahead produces drift.

### Phase 1: Extract structure

Before reading typography, color, or any surface detail, extract the bones.

- **Grid columns.** How many columns is the layout built on? Is it a strict 12-column grid, a looser 4-section flow, or asymmetric?
- **Section ordering.** What comes first, second, third? Does the reference have a clear top-to-bottom narrative?
- **Alignment logic.** Is content left-aligned with intent? Centered for standalone moments? Right-aligned for chrome or data?
- **Asymmetry.** Where does the reference deliberately break symmetry? Where does symmetry hold?
- **Overlap and bleed.** Do elements overlap intentionally? Does anything bleed to the edge of the viewport?
- **Container max-widths.** Does the content sit in a centered max-width container, or does it bleed full-width?
- **Gutter rhythm.** What is the visual rhythm of the gaps between elements?

Structure is the most load-bearing extraction. Everything else hangs on it. If the structure is wrong, no amount of typographic polish can save the translation.

### Phase 2: Extract typography scale

Count the steps, not the vibes.

- **Display size.** The biggest type on the page. Estimate the size; note the weight; note the alignment behavior.
- **Body size.** The default reading size. The body is where the type system lives, not the display.
- **Label size.** Microcopy, captions, metadata.
- **Line count per block.** How many lines does a typical headline run? A typical paragraph? A typical caption?
- **Line-height feel.** Tight, normal, or generous? Display type usually wants tight; body usually wants 1.4-1.6.
- **Tracking.** Loose, normal, or tight? Display headlines often use slightly negative tracking; small caps benefit from positive tracking.
- **Serif vs sans.** What family? Is it a single family in multiple weights, or a serif/sans pairing?
- **Display vs body contrast.** Are they the same family or different? Same weight or different?
- **Weight steps.** What weights are used? 400 and 700, or a fuller ramp with 500 and 600 for hierarchy?
- **Alignment behavior.** Left-aligned, centered, justified, or mixed?

If the body and labels disagree on tracking or weight, the reference is more polished than you thought. If they agree, the system is simpler than you thought. Either is valuable to know.

### Phase 3: Extract palette

Hex values where readable. Approximation where not.

- **Background.** The main canvas. Pure white, off-white, off-black, dark charcoal, or tinted?
- **Surface.** Card backgrounds, section backgrounds, panels. Often slightly different from the main background.
- **Primary text.** The default reading color. Rarely pure black even on white backgrounds.
- **Secondary text.** Metadata, captions, deemphasized content.
- **Accent.** The single brand color or the action color. Note where it appears — buttons, links, highlights, chrome.
- **Border.** The color of dividers, card borders, input borders.
- **Shadow tint.** Pure black shadows on white look harsh. Tinted shadows (slightly blue, slightly warm) match the background hue.
- **Image grade.** If photographs appear, what is the color grade? Cool, warm, desaturated, high-contrast?

Extract hex values where the reference allows. Where it does not, note "approximately" and proceed — the goal is a system close enough that a real implementation reads as faithful, not a pixel-perfect color-pick of an image that may not have rendered at full fidelity.

### Phase 4: Extract spacing rhythm

Spacing is what distinguishes a designed page from a default one. Count it.

- **Headline-to-subheadline gap.** Tight (display sits close to support text) or generous (display floats)?
- **Text-to-CTA gap.** How much breathing room before the call-to-action?
- **Card-to-card gap.** What is the rhythm between cards in a grid?
- **Section top/bottom padding.** How much vertical space between sections? Marketing pages often run 96-160px; product UIs run 32-64px.
- **Side gutters.** How much horizontal padding from the viewport edge?
- **Card padding.** Internal padding inside a card.
- **Image-to-text distance.** When images sit next to or above text, what is the gap?
- **Navbar internal spacing.** How dense or generous is the nav? What is the rhythm between nav items?

Spacing is the silent system. Two designs can use the same components and the same palette and read completely differently because their spacing rhythms disagree. Extract it explicitly.

### Phase 5: Component inventory

Before writing any code, list the components the reference contains.

- **Buttons.** Primary vs secondary. Fill or outline. Radius. Padding. Icon use. Font weight. Size variants visible.
- **Cards.** Border, fill, shadow, radius. Internal structure (header, body, footer). Hover affordance if implied.
- **Badges and pills.** Used decoratively or for status? What rounding?
- **Dividers.** Hairlines or thicker? What color?
- **Inputs.** If the reference contains forms — what is the input style? Underline, outlined, filled?
- **Navbar treatment.** Sticky, transparent, solid? Logo placement? Item spacing? Mobile collapse pattern?
- **Footer treatment.** Dense or sparse? Single column or multi-column?
- **Image system.** Aspect ratios, framing, crop logic. Are images square, 16:9, golden ratio? Cropped tight or generous?
- **Motion mood (implied).** Calm vs energetic. Scrubbing vs popping. Parallax-leaning vs static. Even when motion is not visible, the composition often implies it.

The inventory is the bill of materials. The build will assemble these components against the structure. Missing this step produces builds with ad-hoc components that disagree with each other.

### Phase 6: Code

Only after phases 1-5 is implementation acceptable. The order in the build:

1. Set up the type and color tokens (palette, type families, type scale).
2. Build the layout shell (grid, container widths, section structure).
3. Place the structural blocks (hero, sections, footer).
4. Build the components from the inventory.
5. Fill the content.
6. Add interaction states (hover, focus, active, disabled).
7. Add motion if the reference implies it.
8. Self-review the build against the reference.

If you find yourself building a component that was not in the inventory, stop. Either the inventory was incomplete (return to phase 5) or you are inventing something the reference did not have (this is drift — interrogate it).

---

## Handling ambiguity (low-fi vs high-fi sources)

The fidelity of the reference governs how much you invent.

### Photograph or polished mockup

Treat as a hard spec. Match layout, type scale, color, spacing within the limits of the medium. Invent only what is genuinely missing — hover states, focus rings, empty states, error states. The polished mockup is rarely the source of those states; you supply them, in the same visual language.

### High-fidelity screenshot

Treat as truth. Pixel-match where reasonable. Preserve the type ramp. Preserve the palette. Preserve the spacing language. If the screenshot is from a shipped product, you are translating production-quality work — the screenshot is the spec.

### Sketch or wireframe

The skeleton is binding; the surface is yours. Hold the structure, hierarchy, and content density that the wireframe specifies. Choose the typography, color, and motion to serve the implied product — not your default taste. A sketch implies a system; the system is your call within the sketch's bounds.

### Mood image or photo reference

Atmosphere is binding; structure is yours. Extract the palette, texture, and mood from the photograph. Translate into UI-shaped components. A photograph of a mountainside is not a layout, but its palette, light direction, and mood are. Build the UI that matches the mood.

### Mixed reference set

Pick one image as the structural anchor. Treat the rest as palette or atmosphere supporting evidence. Do not average across them. Averaging produces mush — the structure from A blended with the palette from B blended with the spacing from C is incoherent.

The structural anchor is whichever image is closest to the actual product surface. The others are critique, not parts.

### Missing states

For missing states (loading, empty, error, hover, focus), invent only after preserving everything else. The new state must inherit the reference's component family, radius logic, spacing rhythm, and mood. Do not let a missing state become an excuse to introduce a foreign visual language.

When you invent a state, document it: "Loading state inferred — used skeleton matching card structure, 600ms fade-in." This makes the invention reviewable and prevents the build from accumulating invented details that nobody can explain.

---

## What to ask vs make a sensible call

The reference is silent on many details. The question is which silences require clarification and which can be filled with a sensible default.

### Ask when:

- The choice affects the product's positioning or audience. "Is this a consumer-facing or B2B product?" governs voice, copy, and density.
- The choice has high cost to reverse. If the typography is the wrong call, the entire build needs reworking. If the radius is wrong, it is a quick swap.
- The reference is genuinely ambiguous on a load-bearing element. A reference that shows a hero but no nav cannot be interpreted as "no nav" — confirm.
- The brief implies constraints the reference does not respect. If the brief says "no JavaScript animations" and the reference clearly implies parallax, surface the conflict.

### Make a sensible call when:

- The choice is a leaf detail (the exact hex value of a hairline border, the precise weight of metadata text).
- The reference is silent on standard product surfaces (404 page, empty state, focus ring) and you can infer from the established system.
- A default exists that the reference does not contradict (e.g., 200ms transition on hovers, 8px corner radius if the system is "soft").
- Asking would slow the work and the call is low-cost to reverse.

### The standing rule

Make sensible calls fast; document them; flag them for review. The next pass either confirms or corrects. Do not paralyze the work on questions that can be cheaply reverted.

---

## Stack recommendations per reference type

The reference type strongly suggests the right stack. Match the stack to the surface.

### Marketing site, landing page, or hero-driven brand page

Static framework or server-side rendering with utility-first CSS for fast iteration. Plain HTML + utility-first CSS or vanilla CSS modules. Heavy component libraries are rarely needed — image quality, type discipline, and motion polish matter more than the framework.

### Product UI, dashboard, or data-dense app

Component library with strong primitives (Button, Modal, Form, Table, Card, Navbar) and accessibility-first foundations. Aria-foundation libraries on a v4-capable utility CSS layer are a strong default. Alternatives include Radix-based stacks. Build the design tokens into CSS variables so the library's theme system absorbs your visual customization.

### Editorial site, portfolio, or creative agency

Vanilla CSS modules or utility-first with a custom typography pipeline. Motion library only when it earns its weight. Heavy component frameworks fight editorial layouts more than they help — the layouts are unique per page and a card primitive made for SaaS feels wrong in a magazine.

### Internal tool or admin panel

Component library, conventions over creativity, dense data primitives. Optimize for "boring and obvious." The internal user wants speed and predictability, not delight.

### PWA, server-rendered, or existing template engine

Stay in the existing stack. Do not introduce a single-page React app for a single feature in a Blade + Alpine + HTMX project. Build with the project's primitives; design tokens still transfer.

### Mobile (native or hybrid)

Native platform primitives where possible. The platform's interaction patterns are evidence; do not fight them. Web-derived UI in a native shell reads as cheap; native primitives respected in a hybrid app read as professional.

---

## Common false reads

These patterns trick analysts into producing wrong implementations.

### Reading the sky for the system

A reference's atmosphere is real; its system is what you extract by counting things. Count columns. Count steps in the type scale. Count radius values. Atmosphere without count is vibes-only and produces drift. The atmospheric extraction tells you the mood; the system extraction tells you the build.

### Confusing decoration for structure

A grain overlay, a noise texture, or a subtle gradient is not the design system. Strip the surface treatment, see the bones, then add the texture back as a final layer. A grainy reference and a clean reference can share the same bones — start with the bones.

### Conflating display and body

Display type is loud and lies about the scale. Find the body and the labels — that is where the system lives. A reference with a 96px hero headline and 16px body has a body system of 16px; the 96px is one specific moment, not the system.

### Hero clean-up bias

When a hero looks crowded in the reference, the temptation is to "clean it up." Don't. The crowd is the design. Either reduce the words in the headline (a copy decision, surfaced separately) or regenerate the reference cleaner — do not silently drop elements during translation.

### Centering everything because some things are centered

Asymmetry in the reference is intentional. Preserve it. If the hero is left-aligned and the testimonials are centered, both alignments are deliberate. Do not center the hero "for consistency" — the inconsistency is the design.

### Replacing distinctive components with generic equivalents

A "card" in the reference might be a one-off layered frame, not a re-usable card primitive. Read the actual structure before reaching for a `<Card>` component. The generic component is faster; the specific structure is right.

### Mistaking pseudo-system labels for real UI

Decorative micro-text — "00 orchestration layer," "system marker 03," "intelligence vector 7.2" — often appears in moodier references. It is rarely real UI and almost never adds value in the build. It is set dressing. Reduce or remove during translation. A real product does not ship with "00 orchestration layer" stamped on its header.

### Pulling proportions from cropped zooms

Cropping out a tiny zone of a larger composition destroys spacing, proportion, and type-scale accuracy. A crop tells you what an element looks like up close; it does not tell you how that element relates to its neighbors. For zone-level analysis, regenerate the section as a fresh standalone image.

---

## Translation pitfalls

Failure modes that occur during the translation pass itself.

### Compressing multi-section analysis into one pass

If the reference has a hero, three feature sections, a testimonials block, a pricing section, and a footer, do not run one analysis on the whole thing. Treat each section as its own analysis unit, with its own optional detail pass. A unified analysis loses the per-section nuances and produces a build that drifts as it moves down the page.

### Skipping analysis because the reference "looks easy"

Easy references are the ones that get translated into generic defaults. The simpler the reference, the more its quality depends on the small choices — the exact tracking, the precise hex, the deliberate spacing rhythm. Skip the analysis on an "easy" reference and you will produce something that looks like the reference at a glance but reads as generic on inspection.

### Inventing details before regenerating the reference

When a region of the reference is unclear, generate one more clean image of that region first. Inventing without regenerating is gambling; the gamble loses more often than it wins. The cost of one extra reference image is far less than the cost of building something that the stakeholder rejects because it does not match.

### Substituting "good defaults" for the reference's specific choices

The defaults are exactly what the reference was built to escape. Inter is the default; the reference probably uses something with character. 8px radius is the default; the reference probably uses 4px or 16px. White is the default; the reference probably uses off-white. Match the reference's choices, not the defaults — defaults are what produce convergence to a generic look.

### Section-by-section drift

The implementation drifts so that section 1 looks like the reference and section 6 looks like a different website. The fix: after each section is built, hold the build next to the reference and check for drift. Catch it early or it compounds — section 6 disagrees with section 5 which disagrees with section 4 which disagrees with the reference.

### Inventing components mid-build

The inventory was complete. You start the build. You realize you need a "stats counter" component that was not in the inventory. Either you missed it (return to phase 5 and update the inventory) or it is drift (interrogate why it appeared). Either way, the inventory should match the build; if it does not, one of them is wrong.

---

## The output: code + self-review

A faithful translation produces two artifacts.

### The code

A working frontend file (or files) that implements the reference. The code uses the tokens extracted in phases 2-4. The code uses the components inventoried in phase 5. The code respects the structure extracted in phase 1.

The code should be reviewable in isolation — a teammate should be able to read the code without seeing the reference and understand the design choices.

### The self-review

A short written note, alongside the code, that distinguishes literal from inferred. The format:

```
Literal from reference:
- 3-column grid at 1280px viewport
- Display: 72px, weight 600, tracking -2%
- Body: 16px, weight 400, line-height 1.55
- Accent: oklch(0.62 0.18 254) — pulled from CTA buttons
- Card: 8px radius, hairline border (1px, oklch(0.92 0 0)), 24px padding

Inferred (not literal):
- Hover state: 200ms cubic-bezier easing, opacity 0.9
- Focus ring: 2px solid accent, 4px offset
- Empty state: composed inline; reference had no empty state
- Mobile breakpoint at 768px; reference was desktop-only
- Dark mode tokens: derived by inversion; reference was light-mode only

Flagged for confirmation:
- The "stats counter" component is inferred from copy patterns; reference may have shown a simpler block
- The footer was partially cropped; assumed two-column layout with social on the right
```

The self-review is what makes the translation reviewable. Without it, the next reader cannot tell which decisions were the reference's and which were yours. With it, every inferred decision is auditable — the stakeholder can confirm or correct, and the next pass either accepts or revises.

---

## The translation discipline

When implementing from a reference, follow it. Preserve layout logic, spacing rhythm, section order, text-image balance, typography mood, component style. The goal is not "inspired by" — the goal is "visually faithful, translated into real frontend."

Do not "improve" the reference by replacing it with a generic coded layout. Improve it by executing it well. The reference is what the stakeholder agreed to; the build is the translation of that agreement into code. Drift is the silent failure mode that takes a faithful translation and turns it into a different design.

The discipline:

1. **Reference first. Always.**
2. **Analyze before you code.**
3. **Extract tokens before you compose.**
4. **Inventory components before you build.**
5. **Match what the reference shows; invent only what it omits.**
6. **Document literal vs inferred in writing.**
7. **Hold the build next to the reference at each section.**

Hold these and the translation reads as faithful. Skip any and drift sneaks in. The discipline is the difference between a build that lands and a build that almost-lands but feels wrong.

---

## When the reference is generated, not sourced

When you produce the reference yourself (e.g., via image generation), the translation pipeline is the same — but the production of the reference is itself a phase.

### Generating the reference

- **Specify the brief in the prompt.** The image generation needs the same information the build needs: product, audience, aesthetic, palette, mood.
- **Generate at the surface's actual size.** A landing page is wide; a mobile screen is narrow. Match the aspect ratio to the build.
- **Regenerate for sections.** A single image cannot represent the hero, the features, and the footer at high fidelity. Generate the hero separately, the features separately, the footer separately. Stitch the system across them in the build.
- **Generate detail passes for unclear regions.** If a generated reference has an unclear card structure, generate a closer image of just the card. The detail pass clarifies what the wide shot blurred.

### The fidelity ceiling

A generated reference is not pixel-canonical truth — it is a high-fidelity sketch. The build interprets it; the build does not enslave to it. If the generated reference shows a font you cannot license, the build picks the nearest licensed equivalent. If the generated reference shows a layout that does not respond well at mobile widths, the build adapts.

The generated reference is a strong reference, but its purpose is to anchor the system, not to dictate every pixel.

---

## Closing rules

1. **Reference first, code second.** Always. No exceptions for visually important tasks.
2. **Analyze as a checklist, not a vibe-read.** Six phases. Sequential.
3. **Extract by counting.** Columns, steps in the type scale, radius values, accent uses. The system is what you can count.
4. **Distinguish literal from inferred in writing.** The self-review is non-negotiable.
5. **Hold the build next to the reference per section.** Catch drift early.
6. **When unclear, regenerate the reference for that region.** Do not invent.
7. **Improve the reference by executing it well, not by replacing it with defaults.** Defaults are the convergence trap.

Hold these and the translation is faithful. The faithful translation lands the design; the unfaithful translation lands a near-miss that nobody can quite name. The discipline is the difference.
