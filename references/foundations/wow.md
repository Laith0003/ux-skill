# The wow layer

A page that is on-brand, responsive, and richly built is the **floor** -- correct and
forgettable. The wow layer is the **ceiling**: the 2-3 coordinated moments that make a
visitor remember the page. This file is how the model produces wow itself, every time,
without the user having to hand it one.

## Doctrine: the model derives wow (it is not outsourced to the user)

Older guidance said "the wow moment can only come from the user." That is overturned. In
the common flow -- someone hands us a URL and wants their page leveled up -- there is no
rich brief and no hand-specified moment, yet the output must still be memorable. So the
engine **derives a wow layer** from `brand temperature + industry + page goal`. A
user-supplied wow moment still wins when present; absent one, the model does not fall back
to "clean and forgettable" -- it composes its own.

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

## Derive the set from brand temperature (the anti-uniformity rule)

**Wow is the one thing that must NOT be a recipe.** A fixed map (`lead-gen -> always these
three moves`) produces formulaic wow -- a new generic centroid, the exact reflex the arsenal
exists to defeat. Treat the arsenal as a *palette*: derive a coherent set from this brand's
temperature, then **vary it to this brand**. Two skip-hire pages and two law-firm pages
should not get the same three moves.

Map the synthesized 7-axis temperature to a moment family:
- **warm / human / friendly** -> real photography with depth, gentle counters, soft
  staggered reveals. (Skip-hire, hospitality, local services.)
- **bold / energetic / high-contrast** -> kinetic type reveal, marquee, magnetic CTA,
  single-word gradient. (Consumer, sport, creator tools.)
- **technical / precise / cool** -> terminal mockup, code-as-content, scramble text, data
  viz, status indicators. (Dev tools, infra, fintech.)
- **editorial / calm / spacious** -> column rhythm, text-mask reveal, slow ambient motion,
  curtain reveal. (Publications, brand-led, research.)
- **luxury / formal** -> cinematic restraint: one slow camera-like reveal, generous
  negative space, a single tilted product frame. Motion is rare and expensive-looking.

Goal also shapes it: a lead-gen page's hero moment should pull toward the form, not away
from it; a product page's hero moment is the product; a portfolio's is the work.

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

- **Lead-gen local service (warm):** hero = real on-site photo with a green->ink scrim and
  the headline + quote form composed over it; motion signature = proof-stat counters ticking
  up on entry; (long page) section moment = choreographed hover on the service cards.
- **AI product (technical/bold):** hero = a live command-input demo with a typewriter cycle;
  motion signature = staggered reveals; section moment = a before/after panel.
- **Dev tool (technical/cool):** hero = terminal mockup running a real command; motion
  signature = scramble-on-load for the headline; section moment = code-as-design block.
- **Luxury consumer (formal):** hero = one slow cinematic reveal of the product on near-black;
  motion signature = a single tilted product frame with a soft float; no section moment.

Same three tiers, four different languages. That difference IS the wow -- not the tier list.
