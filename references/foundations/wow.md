# The wow layer

A page that is on-brand, responsive, and richly built is the **floor** -- correct and
forgettable. The wow layer is the **ceiling**: the 2-3 coordinated moments that make a
visitor remember the page. This file is how the model produces wow itself, every time,
without the user having to hand it one.

## Doctrine: the model derives wow (it is not outsourced to the user)

In the common flow, someone hands us a URL or a project and wants the page leveled up: there
is no rich brief and no hand-specified moment, yet the output must still be memorable. So
the model **derives a wow layer** from three things: the brand's own page style (what its
pages already do: scheme, rhythm, imagery, how color is used), the brief's structured fields
(`product_type`, `page`, `platforms`, `stage`) and the page goal. A user-supplied wow moment
wins when present. When the brand's pages or brand book already show a signature move, the
wow layer extends that move instead of inventing another. Absent all of these, the model
still composes its own and never settles for clean and forgettable.

## What a wow layer is: 2-3 coordinated moments, one dominant

A wow layer is not "more effects." It is a small, **coherent** set drawn from three tiers:

1. **The hero moment** (the entrance -- always present). The first thing seen does
   something a static image can't: a kinetic headline reveal, a real-photo hero with depth
   + scrim, an interactive demo, a slow ambient motion, a 3D/clay object, a mesh-gradient
   field. This is the dominant moment.
2. **The motion signature** (one recurring micro-behavior). ONE small thing that repeats
   and gives the page a pulse: proof-stat counters that tick up on entry, choreographed
   card hover (border + icon + arrow moving as one), staggered section reveals. Recurring,
   restrained, the same language each time.
3. **The section moment** (one mid-page surprise -- optional, for longer pages). ONE
   place the page does something theatrical: a scroll-pinned product walk, a before/after,
   a kinetic marquee, a distinctive card treatment. Exactly one.

Pick the hero moment + the motion signature always; add the section moment only if the page
is long enough to earn it. **Two to three total. One dominant, the rest supporting.** Never
three co-equal spectacles competing for the eye.

## Derive the set from this brand, never from its industry (the anti-uniformity rule)

**Wow is the one thing that must NOT be a recipe.** A fixed map (`lead-gen -> always these
three moves`, or an industry to an effect) produces formulaic wow: a new generic centroid,
the exact reflex the arsenal exists to defeat. Two products in one industry can share
nothing but the word, so no table here names an industry. Treat the arsenal as a *palette*:
derive a coherent set from what this brand is and does, then **vary it to this brand**.

**1. What carries the value decides the hero moment.** The brand's own product screens make
the hero the product doing its job (a real screen in motion, a live input that answers).
Real photography makes it depth and a measured scrim. A claim with nothing to show makes it
type: a kinetic or masked headline reveal. A terminal or code moment belongs only to a
product that itself runs in a terminal or ships code.

**2. The brand's page style sets how loud the layer is.** A quiet brand (color held back,
one idea per screen, little motion on its own pages) gets one slow reveal and no section
moment. A loud one (color flooded across bands, dense sections) may carry a kinetic
headline or a marquee. The layer never runs louder than the brand's own pages.

**3. The 7-axis temperature picks the language within that volume:**
- **warm / human / friendly** -> real photography with depth, gentle counters, soft
  staggered reveals.
- **bold / energetic / high-contrast** -> kinetic type reveal, marquee, magnetic CTA,
  single-word gradient.
- **technical / precise / cool** -> data shown as it is (real figures, live status
  indicators), scramble text, the product's own interface cropped close.
- **editorial / calm / spacious** -> column rhythm, text-mask reveal, slow ambient motion,
  curtain reveal.
- **formal / restrained** -> cinematic restraint: one slow camera-like reveal, generous
  negative space, a single tilted product frame. Motion is rare and expensive-looking.

**4. The brief's fields and the goal point it.** A page whose conversion is a form pulls the
hero moment toward the form, never away from it. A feature page (`page: feature`) shows that
feature at work. A web app that signs in by phone makes the phone field itself the first
thing that moves. A product page's hero moment is the product; a portfolio's is the work. A
pre-launch page shows nothing that fakes usage.

## The discipline (this is the build, not an afterthought)

The richer layer is the higher-risk path. These keep it from becoming slop:

- **Coherence over count.** The 2-3 moments must read as ONE design language. Check the
  arsenal's "hard combinations to avoid" -- never stack glassmorphism + heavy shadow, three
  scroll-triggers, or three motion languages on one headline.
- **Cap at the arsenal's limit.** More than ~4 distinct effects and the page reads as a
  showcase, not a product. When in doubt, cut to the dominant moment + one support.
- **Mobile tones down two levels.** What is ambient on desktop is distracting on a phone.
  Reduce intensity, drop the section moment if it costs scroll/perf, keep the hero moment
  simple. Mobile-first wow is harder than desktop wow -- and it must never reintroduce
  horizontal scroll, a tall sticky header, or wrapping (the responsive gates still rule).
- **`prefers-reduced-motion` always.** Every moment has an opacity-only / instant fallback.
  No exceptions.
- **Performance non-negotiable.** Transform + opacity only; `IntersectionObserver` not
  scroll listeners; counters/reveals fire ONCE on entry; perpetual loops memoized + isolated;
  no `backdrop-filter` on scrolling content. See arsenal.md "Performance reminders."
- **The CTA/affordance is sacred.** A wow moment never buries or delays the primary action.

## How wow is validated

Wow **cannot be gated**. A check that fails a build unless it detects "2 motion moments"
just rewards shipping motion to pass -- which manufactures the over-animated slop this file
exists to prevent, and fights the responsive gates. So:

- The engine may surface candidate moments and an **advisory** floor ("did this ship any
  hero device beyond a static image?"), never a quality bar.
- The real validator is the **eye, on a real phone.** Deploy the iteration and look. Wow is
  a taste judgment; the human stays in the loop for it, by design.

## Worked examples (illustrations of RANGE, not recipes to stamp)

- **A form converts, real photos, warm brand:** hero = a real on-site photo with a scrim in
  the brand's ink and the headline + quote form composed over it; motion signature =
  proof-stat counters ticking up on entry; (long page) section moment = choreographed hover
  on the service cards.
- **A product with a command input, bold brand:** hero = the live input answering a real
  query with a typewriter cycle; motion signature = staggered reveals; section moment = a
  before/after panel.
- **A product that runs in a terminal, cool brand:** hero = the real command and its real
  output; motion signature = scramble-on-load for the headline; section moment = a
  code-as-design block.
- **A quiet brand with one product object, formal:** hero = one slow cinematic reveal of the
  product on the brand's dark canvas; motion signature = a single tilted product frame with
  a soft float; no section moment.

Same three tiers, four different languages. That difference IS the wow -- not the tier list.
