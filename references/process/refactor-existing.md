# Refactor Existing

How to redesign existing UIs without breaking what works. A redesign is not a rewrite. The job is to upgrade what is there, keep the lights on, and ship in slices the team can absorb.

Scope discipline is the difference between a redesign that ships and a redesign that stalls. Taste discipline is the difference between a redesign that modernizes and one that erases the things users actually loved.

---

## Scope without creep

Before opening any file, answer four questions. These four answers govern every decision the redesign will make.

### 1. What surface is in scope?

Marketing site, signed-in app, both, or a single page? Name it explicitly. The redesign covers exactly that and nothing else.

A surface is named when:
- The pages or routes are listed.
- The components shared with out-of-scope surfaces are identified (and ruled in or out).
- The data dependencies are noted (does the redesign change what is on the page, or only how it looks?).

A surface is not named when:
- The scope is "the design system" with no specific surfaces to apply it to.
- The scope is "the product" without a list of surfaces.
- The scope is "what looks bad" — a feeling, not a boundary.

### 2. What is the metric of success?

"Looks better" is not a metric. Choose one or two observable outcomes:

- **Conversion-side:** trial signups, time-to-task, signup completion rate, retention.
- **Performance-side:** page weight, CSS bundle size, Largest Contentful Paint, perceived performance on a real device.
- **Accessibility-side:** audit pass rate, keyboard navigation completion, screen reader successful task rate.
- **Adoption-side:** percentage of users who opt into the new surface, percentage who opt back to old, qualitative feedback rate.

The metric does two things: it tells you when the redesign is done, and it gives the team a way to evaluate trade-offs that emerge during the work. Without a metric, every choice is "I think it should be X" and there is no way to break ties.

### 3. What is explicitly out of scope?

Information architecture, content strategy, naming conventions, copy rewrites, framework migrations — name each one as out unless it is explicitly in. The default for any adjacent concern is "out, document for follow-up."

This list is what protects the redesign from scope creep. When something surfaces during the work that you want to fix, the question is: is it in the in-scope list? If not, it goes on the follow-up list and the work proceeds.

### 4. What is the ship pattern?

One big-bang launch, parallel pages with a toggle, dark-launch behind a flag, or rolling per-route. Pick before you start. The migration strategy section below covers when each applies.

---

## Audit first

Before deciding what to change, decide what is load-bearing. Walk the existing UI and produce four lists.

### Works

Components and patterns that are doing their job. The login flow that has a 92% completion rate. The dashboard widget that users specifically mention in support tickets. The microcopy on the empty state that nobody has ever complained about.

Touch these only when they conflict with the new direction. Even then, prefer to bend the new direction to fit, not the other way around. A redesign that breaks the working things is a regression in disguise.

### Load-bearing equity

Visual elements that are recognizable, trademarked-in-spirit, or carry user trust:
- The logo.
- The primary brand color.
- A signature curve, silhouette, or motion.
- The typeface family if it has equity (the team recognizes it; the audience recognizes it; replacing it would feel like a different product).
- The welcome microcopy that everyone has memorized.
- A signature interaction (the way save works, the way the menu opens, the way the toast feels).

These can evolve but not vanish. The modernization changes the surface around the equity; it does not delete the equity.

### Stale

Components that were good when they shipped and are now dated. The flat 2018 cards. The pure-black backgrounds. The default Material Design buttons. The illustrations that look like the era they came from.

These are the redesign's real targets. Stale does not mean broken — it means the component shipped against a different aesthetic baseline and the baseline has moved.

### Deprecated

Components nobody loves, nobody asked for, and that exist only because of historical accident. The page nobody visits. The setting nobody touches. The "share" button that has had a 0.2% click rate for three years.

Mark for removal; do not redesign what should be deleted. The redesign is also a deletion pass — every component you remove is one less component to maintain and one fewer surface to ship-quality.

### The audit checklist

Run these against the existing UI. Each item is a flag, not a verdict:

- **Browser-default fonts or Inter everywhere.** Replace with a font that has character (Geist, Outfit, Cabinet Grotesk, Satoshi, or a distinctive serif like Fraunces).
- **Headlines lacking presence.** Increase display size, tighten letter-spacing, reduce line-height. Headlines should feel intentional.
- **Body text wider than 65 characters.** Clamp paragraph width.
- **Only 400/700 in the font weight set.** Introduce 500 and 600 for subtle hierarchy.
- **Proportional figures in a data UI.** Switch to tabular figures.
- **Pure black backgrounds.** Replace with off-black, dark charcoal, or a tinted dark.
- **Oversaturated accents.** Drop saturation below 80%. Desaturate so they blend with neutrals.
- **More than one accent.** Pick one. Remove the rest.
- **Mixed warm and cool grays.** Pick one gray family, tint consistently.
- **Purple-blue gradient fingerprint.** Replace with neutral bases and one considered accent.
- **Generic black box-shadow.** Tint shadows to match the background hue.
- **Flat sections with no depth.** Add subtle noise, ambient gradient, or a low-opacity background image.
- **Everything centered and symmetrical.** Break symmetry with offset margins, mixed aspect ratios, left-aligned headers over centered content.
- **Three equal feature columns.** Replace with a 2-column zig-zag, asymmetric grid, masonry, or horizontal scroll.
- **`100vh` on full-screen sections.** Switch to `min-height: 100dvh` to fix the mobile viewport jump.
- **Cards locked to equal heights by flexbox.** Allow variable heights or use masonry when content varies.
- **Uniform radius on everything.** Vary: tighter on inner elements, softer on containers.
- **Missing hover, active, focus states.** Add them. Transitions 200-300ms. Visible focus rings are required, not optional.
- **Generic loading spinners.** Replace with skeleton loaders that match the layout shape.
- **No empty states or error states.** Design composed empty states. Inline error messages with the field and the fix. Never use the browser's native alert dialog.
- **Dead anchor links.** Link to real destinations or visually disable.
- **Placeholder content.** "John Doe," "Acme Corp," round numbers (50%, $100.00). Use diverse realistic names, contextual brand names, organic numbers (47.2%, $99.00).
- **Copywriting clichés.** "Elevate," "Seamless," "Unleash," "Next-Gen," "Game-changer." Write plain, specific language.
- **Exclamation marks in success messages.** "Oops!" errors. Be confident, direct.
- **Lorem Ipsum, identical avatars, identical blog dates.** Fill with real-shaped placeholder content.
- **Title Case On Every Header.** Switch to sentence case.
- **Div soup.** Use semantic HTML — `<nav>`, `<main>`, `<article>`, `<aside>`, `<section>`.
- **Missing alt text, missing meta tags, arbitrary z-index values.** Clean up.
- **No skip-to-content link.** Add one.
- **No 404.** Design a helpful, branded page.

The audit is the redesign's prioritization tool. Fix in this order: font swap, color cleanup, interaction states, layout and spacing, component replacements, missing states, typography scale polish.

---

## Taste invariants vs expression layer

A redesign distinguishes two layers.

### Taste invariants (things that must stay)

The things that, if removed, would change what the product *is* — not how it looks. These survive the redesign without negotiation.

- **The product's voice.** The way it greets, confirms, apologizes. If the existing voice is "direct, warm, specific," the redesign keeps "direct, warm, specific." If the voice is broken (shouty, condescending, overly cheerful), that is a separate decision and lives on the in-scope or follow-up list.
- **The decision architecture.** What the user can and cannot do. The redesign restyles the surface; it does not silently remove a capability.
- **The brand mark.** The logo, the primary brand color (which can desaturate or tighten its usage, but does not disappear), the trademarked elements.
- **The signature moments.** The save animation that the team is known for. The empty state that users have screenshot for friends. The error message that turned a frustrating moment into a memorable one.
- **The data integrity.** A redesign does not change what data appears on the page, only how it is presented.

The taste invariants are the equity. They are what makes a returning user feel "yes, this is still my product, but it looks better."

### Expression layer (things that can change)

Everything else. The chrome, the surface, the choreography:

- The exact typeface (within the family — and the family itself if it carries no equity).
- The radius scale.
- The shadow style.
- The spacing rhythm.
- The interaction state details (specific hover behavior, transition timing, focus ring style).
- The illustration style.
- The micro-animation library.
- The color tokens beyond the brand primary.

The expression layer is what the redesign actually moves. Modernizing the expression layer while preserving the invariants is the move that makes a redesign feel like "the same product, but better" instead of "a different product."

### The test for invariant vs expression

If you cannot decide whether something is invariant or expression, ask: **would a returning user notice if it disappeared?**

If yes, it is equity. Preserve it.
If no, it is expression. Modernize it.

If you genuinely cannot tell, ask the team. The team's institutional memory is the source of truth on what carries equity. Do not guess — guessing wrong on equity creates the worst outcome: a returning user opens the product and feels lost.

---

## Preserving brand equity while modernizing

Brand equity lives in two places: marks (logo, brand color, type personality) and rituals (the way the product greets, confirms, apologizes). The modernization changes the surface around those marks and rituals; it does not delete them.

### Concrete moves

- **Keep the logo.** Replace its container, not its form. If the logo lived in a colored circle in the old chrome, the redesign can change the circle but not the logo inside it.

- **Keep the brand color.** Reduce saturation. Tighten its usage rules. Give it more breathing room. The old design might have used the brand color on twelve elements; the new design uses it on three — that is modernization, not removal.

- **Keep the type family if it carries equity.** Refresh the scale, weights, and tracking. Do not replace the family unless it is genuinely a problem — licensing, accessibility, or it never had equity to begin with.

- **Keep the voice.** Modernize tone where the current voice is shouty, exclamation-heavy, or condescending. The personality stays. The "we'll be right with you, hold tight" stays; the "OMG SO EXCITED YOU'RE HERE!!!" goes.

- **Keep the moments.** A signature animation on save. A particular empty-state illustration style. A specific welcome flow. Modernize the execution. Preserve the moment.

### When equity is actually legacy

Sometimes the team treats something as equity when it is actually legacy. The brand color is "ours" because nobody has questioned it in five years — but nobody actually liked it, the audience does not remember it, and replacing it would not feel like a loss.

The test:
- Ask three returning users what color the brand is. If they cannot answer, the color is not equity.
- Ask the team what the signature ritual is. If they have to think about it, it is not a ritual.
- Look at user research. If the equity is real, it shows up in interviews unprompted.

When something is genuinely legacy and not equity, the modernization can replace it. Document the decision. Defend the call. Move on.

---

## Migration strategy

Pick one per surface. Do not mix without intent.

### 1. Big-bang

Cut over the entire surface in one release. Reserved for:
- Small surfaces (a single internal tool, a single utility page).
- Surfaces where the existing UI is so broken that gradual rollout is worse.
- Greenfield within a redesign (a brand new page being added as part of the redesign).

Requires a tight blast radius and a rollback path. The rollback is what makes big-bang safe — if the launch shows a problem in the first hour, the team can revert and diagnose.

### 2. Parallel pages

Ship the redesigned page at a sibling URL (`/v2/...`, `/new/...`) and link both. Let users opt in. Useful for:
- Marketing surfaces where the team wants to see conversion data before fully committing.
- Surfaces where the existing page has bookmark equity (returning users have it saved).
- Surfaces where the redesign is genuinely an experiment.

Decommission the old page once metrics confirm the new one wins. Keep a redirect from the old URL to the new one for at least six months to preserve bookmark equity.

### 3. Feature-flagged rollout

Same templates, same routes, gated by a flag. Start at 1% to dogfood, 10% for early signal, 50% for confidence, 100% to commit. The flag is removable once the rollout settles.

Use when:
- The surface is high-traffic and the team wants graduated risk.
- The redesign touches load-bearing flows where a regression would be expensive.
- The team has a feature flag system in production already (do not add one just for the redesign).

### 4. Dark launch

Ship the new design rendered but not visible — behind a query param the team uses, or a header check, or an internal-only flag. Validate in production with real data before exposing to users.

Use when:
- The redesign has heavy computation or new data dependencies that need real-world validation.
- The redesign touches load-bearing flows and even a small percentage of users hitting a regression would be costly.
- The team wants to verify performance and behavior before committing to a rollout pattern.

### 5. Per-route rolling

Migrate one route at a time. The site looks inconsistent during the rollout; budget for visible "in transition" weeks. Works best when:
- Routes are independent (marketing pages, settings pages, standalone tools).
- The team can ship continuously and update routes one at a time.
- Users tolerate or expect the iterative rollout.

### Standing rule

Whichever you pick, keep the old code in the tree until the new is proven. Cleanup happens after the redesign lands, not during. Premature deletion makes rollback expensive; deferred deletion costs little.

---

## When to refactor vs rewrite vs replace

### Refactor

The existing code is roughly sound; the visual treatment is the problem. Keep the structure, swap tokens, restyle components, add missing states. This is the default and the right move for 80% of redesigns.

When refactor applies:
- The components map to what the new design needs.
- The data flow is correct.
- The accessibility foundation is present (semantic HTML, ARIA where needed, keyboard handling).
- The issue is surface — colors, spacing, typography, interaction states.

Refactor is fast and reversible. Most redesigns end here.

### Rewrite

The existing code is fighting the new design — wrong primitives, wrong stack, wrong layering. Rewrite the component or the page in place; keep the route and the URL stable.

When rewrite applies:
- The existing component was built for a different aesthetic and is structurally incompatible.
- The existing code has accumulated debt that makes refactor cost more than rewrite.
- The new design implies primitives the old code does not have.

Rewrite is more expensive than refactor but less expensive than replace. Keep the URL and the data contract; rewrite the implementation.

### Replace

The existing surface is so far from the new direction that rewriting it costs more than rebuilding. Reserved for:
- Legacy surfaces with low usage that the redesign explicitly retires.
- Surfaces where the existing code is on a different stack and migrating is part of the redesign.
- Surfaces where the existing implementation has security or accessibility issues that warrant a fresh build.

Replace is the most expensive option. Use it only when the alternatives are clearly worse.

### The default

If you cannot tell which mode applies, refactor first. The cost of refactor-then-rewrite is low; the cost of rewrite-when-refactor-would-have-worked is high. Refactor reveals what is actually broken vs what is just dated.

---

## Coordination with users

A redesign is a change. Users do not always welcome change, even when the change is an improvement. The communication strategy is part of the redesign.

### Announcement

Tell users what is happening before they discover it. The announcement says:
- What is changing.
- Why (in terms the user cares about — speed, clarity, new capabilities).
- When (date or rollout window).
- What stays the same (the equity — the things they will still recognize).
- How to provide feedback if something goes wrong.

A surprise redesign — users open the product one morning and find it different — generates more support tickets than a redesign announced a week in advance. The cost of the announcement is low; the benefit is high.

### Opt-in

When the migration strategy supports it (parallel pages, feature flag), let users opt in. The opt-in is the friendliest rollout because it converts complaints into curiosity — users who do not want change can stay; users who want to try the new version can.

Opt-in surfaces the strongest signal: the percentage of users who opt back to the old version is the clearest measure of whether the redesign is actually better. If 30% opt back, something is wrong. If 2% opt back, the redesign is succeeding.

### Full rollout

Once metrics support it, commit to the new version and remove the old. The full rollout removes the toggle, removes the alternate URL, removes the feature flag — the new design becomes the only design.

Time the full rollout against:
- Stability of the new design (no open critical issues).
- Adoption (most users have used the new version at least once).
- Feedback (the loud minority of "I hate the new version" has settled).

Premature full rollout (forcing users off the old version before the new one is stable) generates more complaints than a delayed rollout (keeping the old around longer than needed). When in doubt, wait.

### Sunset

The old version is deprecated, the toggle is removed, the alternate URL redirects. The redesign is complete.

The sunset includes a final communication: "We've removed the old version. The new design is now the default. Thanks for testing it with us."

---

## Failure modes

Redesigns fail in predictable ways. Naming the failures helps prevent them.

### Scope creep

The redesign starts as "the marketing site" and becomes "the marketing site plus the dashboard plus a copy refresh plus a content strategy review." The original scope was achievable in six weeks; the expanded scope will take six months.

Prevention: the out-of-scope list, written before the work starts, is the boundary. Every "while I'm here" goes on the follow-up list, not into the current sprint.

Recovery: when scope creep is detected mid-redesign, do not "finish what's started." Cut back to the original scope. Ship that. The expanded items become a second redesign.

### Regressions

The new design is prettier but slower. Or prettier but less accessible. Or prettier but harder to use. The metric the team chose (in the scope phase) is the canary — when the metric moves the wrong way, the redesign has regressed.

Prevention: track the metric continuously during the rollout. Define a regression threshold before the launch ("if conversion drops more than 5%, we pause the rollout").

Recovery: roll back the surface where the regression appeared. Diagnose. Fix. Re-launch. Do not push through a known regression hoping it will resolve.

### Regression of taste

The redesign is technically modernized — better colors, better type, better spacing — but the soul of the product is gone. The signature warmth, the specific voice, the moments that users loved — they are not in the new design.

Prevention: the taste invariants list, written before the work starts, names what must survive. The work is reviewable against the list — does the new design preserve each invariant?

Recovery: the invariants that were lost are diagnosed and restored. The redesign does not roll back; the redesign incorporates the missing equity. The new save animation now matches the warmth of the old one; the new empty state has the personality of the old one.

### Drift during rollout

The team starts redesigning surface 1 with a clear vision. By surface 6, the vision has drifted — surface 6 disagrees with surface 5 which disagrees with surface 4 which disagrees with surface 1. The redesign ships, but the result is incoherent across surfaces.

Prevention: the design system document, written during or before the work, is the source of truth. Every surface is built against the system, not against the surface before it.

Recovery: when drift is detected, pause new surface work. Align the drifted surfaces to the system. Then resume.

### Over-personalization to the loud minority

A small but vocal group of users hates the new design. They send angry emails. They threaten to leave. The team panics and starts reverting changes piecemeal to placate them.

Prevention: the metric is the source of truth, not the loudest voice. A 2% complaint rate against a 30% conversion improvement is a win, even if the 2% are loud.

Recovery: when the team is reverting based on noise, return to the metric. Ask: what does the data show? Decide based on the data. Acknowledge the loud minority's feedback without letting it dictate the rollout.

### Premature cleanup

The team deletes the old code before the new is proven. Six weeks in, a regression appears that requires reverting to the old version — and the old code is gone.

Prevention: keep the old code in the tree until the new is proven. "Cleanup" is a phase after the redesign lands, not during.

Recovery: if the old code is already gone, the team commits to fixing the new version rather than reverting. This makes regressions more expensive but is sometimes the only option.

---

## Rules of conduct during a redesign

1. **Work with the existing tech stack.** Do not migrate frameworks under cover of a redesign. If the framework needs to change, that is its own project.

2. **Check the project's dependency file before importing anything new.** A new font, a new motion library, a new component primitive — each one needs justification, and the justification belongs in the design system document, not hidden in the build.

3. **Do not break existing functionality.** Test after every visible change. The redesign restyles; it does not silently remove capabilities.

4. **Keep changes reviewable and focused.** Small, targeted improvements over big rewrites. Twenty small PRs that each preserve reviewability beat one giant PR that nobody can review properly.

5. **Document behavioral changes separately from visual ones.** Reviewers should be able to see "we restyled the button" and "we changed when the button is enabled" independently. Conflating the two hides bugs.

6. **Preserve the working things.** The audit's "works" list is the constraint. Do not modernize what does not need modernization.

7. **Commit to the migration strategy.** If you picked feature-flag rollout, follow the percentage steps. If you picked parallel pages, do not silently change the old page.

8. **Track the metric.** The success metric is the canary. Track it continuously. Decide based on data, not based on the loud minority's emails.

9. **Sunset deliberately.** The old version comes down when metrics support it, not when the team is impatient. The sunset is announced; bookmark equity is preserved with redirects.

10. **Defer cleanup until after the redesign lands.** The old code stays in the tree until the new is proven.

---

## Closing rules

A redesign is an act of preservation as much as it is an act of modernization. The redesign keeps:
- What works.
- What carries equity.
- What users have memorized.

The redesign changes:
- The chrome around what works.
- The expression around the equity.
- The execution of the moments users have memorized.

The redesign deletes:
- What is deprecated.
- What nobody loves.
- What exists only because of historical accident.

Hold this distinction and the redesign lands as "the same product, but better." Lose it and the redesign becomes a different product, which is rarely what was asked for.

The discipline:

1. **Scope before opening any file.**
2. **Audit before deciding what to change.**
3. **Distinguish taste invariants from expression layer.**
4. **Preserve equity while modernizing chrome.**
5. **Pick the migration strategy explicitly.**
6. **Refactor by default; rewrite when forced; replace when justified.**
7. **Communicate the change before users discover it.**
8. **Track the metric.**
9. **Keep the old code until the new is proven.**
10. **Sunset deliberately.**

Hold these and the redesign ships. Skip any and the redesign stalls or regresses. The discipline is the difference.
