# Laws of UX

A reference catalog of thirty cognitive laws that govern how users perceive, decide, and act inside interfaces. Use this when you need to name what is wrong with a screen — or what is right — in language that survives stakeholder challenge.

## Primary source

This catalog is synthesized from production design work. The canonical reference for the named laws is **[lawsofux.com](https://lawsofux.com)** by Jon Yablonski — each law there has an illustrated card, the original research citation, and worked examples. When ux-skill's `/ux-critique` cites a named law, link to the corresponding lawsofux.com page so readers reach the canonical card in one click.

Other foundational sources cited throughout:

- Don Norman — *The Design of Everyday Things* (see `references/laws/norman.md`)
- Steve Krug — *Don't Make Me Think* (see `references/laws/krug.md`)
- Susan Weinschenk — *100 Things Every Designer Needs to Know About People*
- Daniel Kahneman — *Thinking, Fast and Slow* (cognitive bias laws)

### Source link index — by canonical name

| Law | Primary source |
|---|---|
| Aesthetic-Usability Effect | https://lawsofux.com/aesthetic-usability-effect/ |
| Choice Overload | https://lawsofux.com/choice-overload/ |
| Chunking | https://lawsofux.com/chunking/ |
| Cognitive Bias | https://lawsofux.com/cognitive-bias/ |
| Cognitive Load | https://lawsofux.com/cognitive-load/ |
| Doherty Threshold | https://lawsofux.com/doherty-threshold/ |
| Fitts's Law | https://lawsofux.com/fittss-law/ |
| Flow | https://lawsofux.com/flow/ |
| Goal-Gradient Effect | https://lawsofux.com/goal-gradient-effect/ |
| Hick's Law | https://lawsofux.com/hicks-law/ |
| Jakob's Law | https://lawsofux.com/jakobs-law/ |
| Law of Common Region | https://lawsofux.com/law-of-common-region/ |
| Law of Proximity | https://lawsofux.com/law-of-proximity/ |
| Law of Prägnanz | https://lawsofux.com/law-of-pragnanz/ |
| Law of Similarity | https://lawsofux.com/law-of-similarity/ |
| Law of Uniform Connectedness | https://lawsofux.com/law-of-uniform-connectedness/ |
| Mental Model | https://lawsofux.com/mental-model/ |
| Miller's Law | https://lawsofux.com/millers-law/ |
| Occam's Razor | https://lawsofux.com/occams-razor/ |
| Paradox of the Active User | https://lawsofux.com/paradox-of-the-active-user/ |
| Pareto Principle | https://lawsofux.com/pareto-principle/ |
| Parkinson's Law | https://lawsofux.com/parkinsons-law/ |
| Peak-End Rule | https://lawsofux.com/peak-end-rule/ |
| Postel's Law | https://lawsofux.com/postels-law/ |
| Selective Attention | https://lawsofux.com/selective-attention/ |
| Serial Position Effect | https://lawsofux.com/serial-position-effect/ |
| Tesler's Law | https://lawsofux.com/teslers-law/ |
| Von Restorff Effect | https://lawsofux.com/von-restorff-effect/ |
| Working Memory | https://lawsofux.com/working-memory/ |
| Zeigarnik Effect | https://lawsofux.com/zeigarnik-effect/ |

## How to read this file

Each law has the same shape: a one-line definition, when it applies, how to use it in design, the violation pattern that ships in default AI-slop output, and a fix example you can copy. The laws compound. A screen that violates one is uncomfortable. A screen that violates four is unusable. A screen that obeys all thirty is rare — design is the practice of choosing which ones matter most for this surface, this user, this moment.

Treat the catalog as a vocabulary. The job is not to memorize all thirty. The job is to recognize the pattern fast enough that you can name it during a review, debate it without hedging, and fix it without breaking the next law.

---

## 1. Aesthetic-Usability Effect

### Definition

Users perceive aesthetically pleasing designs as more usable, even when actual usability is identical.

### When it applies

- First impressions, especially on landing pages, marketing surfaces, and onboarding.
- User-reported satisfaction in surveys and reviews.
- Friction tolerance: users forgive more bugs in beautiful products than in ugly ones.

### How to use it in design

- Invest in visual polish on the user's first three screens. The aesthetic credit carries them through later friction.
- Use the aesthetic-usability effect as a buffer, not a substitute. The product still has to work.
- Be honest with yourself: a beautiful prototype tested informally will overstate its real usability. Test more strictly.

### Violation pattern

- Bland, generic interfaces with no visual identity. Users assume the product is also generic.
- Overdesigned interfaces where decoration competes with content. Aesthetic-usability flips at the point where decoration impedes use.

### Fix example

Take any working interface and improve the type system: a defined hierarchy, deliberate spacing, considered color, calm rhythm. The functionality is unchanged. User-perceived usability rises. The same product feels easier.

---

## 2. Choice Overload

### Definition

Too many options cause decision paralysis, longer decision time, and lower satisfaction with the option finally chosen.

### When it applies

- Pricing pages with more than three plans.
- Menus with more than seven items.
- Search results with no default sort or filter.
- Onboarding flows that offer "configure your dashboard" before the user has used the product.

### How to use it in design

- Default to fewer choices. Add only when the user demonstrates need.
- Group related choices and surface the group, not every item.
- Recommend a default. Reduce the user's decision to "accept default or pick something else."
- Hide power-user options behind progressive disclosure.

### Violation pattern

- A pricing page with seven tiers, each differing in three dimensions. The user cannot tell which to pick.
- A signup wizard that asks for ten preferences before letting the user in.
- A toolbar with thirty icons of equal weight.

### Fix example

Replace seven plans with three: a starter, a recommended (marked "Most popular"), and a premium. Move the configuration options out of the chooser and into account settings, where the user goes when they have a specific need.

```html
<div class="pricing">
  <div class="plan">Starter — for solo use</div>
  <div class="plan recommended">Team — most popular</div>
  <div class="plan">Enterprise — call us</div>
</div>
```

Three options, one recommendation. The user can pick in seconds.

---

## 3. Chunking

### Definition

Working memory holds information more reliably when items are grouped into meaningful chunks. Roughly four chunks at a time.

### When it applies

- Phone numbers, credit card numbers, dates, account IDs, tracking numbers.
- Long forms.
- Settings pages with many controls.
- Lists that present unrelated items at the same visual weight.

### How to use it in design

- Group related controls visually. Use spacing, dividers, and headings.
- Break long numbers into chunks (e.g., 0797 868 335, not 0797868335).
- Limit each form section to four to seven fields. Break longer forms across sections.
- Name each group. A heading is the chunk's label.

### Violation pattern

- A 16-digit credit card number rendered as one long string of digits.
- A 24-field signup form on one screen, no sections.
- A settings page where notification, billing, security, and integrations are interleaved with no headings.

### Fix example

Render a card number with chunks: `4242 4242 4242 4242`, not `4242424242424242`. Use `inputmode="numeric"` and auto-insert spaces. The user can read and verify each chunk independently.

For a settings page, group into named sections: Profile, Notifications, Billing, Security, Integrations. Each section has a heading and a defined boundary.

---

## 4. Cognitive Bias

### Definition

Users do not make rational decisions. They are biased — by anchoring, by loss aversion, by social proof, by framing, by recency. Design either accounts for biases or stumbles over them.

### When it applies

- Pricing. Anchoring sets reference points; the user compares to the anchor.
- Defaults. Users keep the default even when they would prefer something else.
- Loss framing. "You'll lose access" is more motivating than "You'll gain access."
- Social proof. Users follow what others did.

### How to use it in design

- Choose defaults consciously. The default is a choice the user is unlikely to override.
- Use anchoring to position a recommended choice. The expensive plan makes the medium plan feel reasonable.
- Frame consequences in the direction that matches the user's interest. Be honest about the framing.
- Use social proof when it is real. ("Used by 12,000 teams.") Never fabricate.

### Violation pattern

- Defaults that benefit the company at the user's expense. Pre-checked subscription boxes. Auto-renewal opt-in without consent.
- False urgency ("Only 2 left!") that has no grounding in fact.
- Social proof with anonymous numbers ("Trusted by thousands") that the user cannot verify.

### Fix example

Use defaults that benefit the user. Opt-in to marketing emails (unchecked). Auto-renewal off by default; offer it as an opt-in with clear pricing.

Anchor honestly. Show the highest plan first; the user reads down and finds the recommended plan affordable by comparison. Do not invent fake anchors.

---

## 5. Cognitive Load

### Definition

Cognitive load is the mental effort required to use an interface. It includes intrinsic load (the difficulty of the task itself), extraneous load (the effort created by the design), and germane load (the effort that builds understanding).

The interface should minimize extraneous load. Intrinsic and germane load are part of the task.

### When it applies

- Every interaction. Every screen. Especially complex tools (analytics, configuration, admin panels).

### How to use it in design

- Reduce extraneous load: cut clutter, simplify labels, externalize state, use familiar patterns.
- Preserve germane load: do not infantilize. The user is learning your product; teach them.
- Match the cognitive budget of the user. A novice has less budget than a power user. Design for the audience you actually have.

### Violation pattern

- A dashboard where every metric, button, and label has the same visual weight. The user has to scan and re-scan to find anything.
- A form that asks for information the system could compute. The user does mental work the system should be doing.
- Inconsistent vocabulary across the same product. The user maintains a translation table in their head.

### Fix example

Cut every visual element that does not contribute to a user task. Group related controls. Use heading hierarchy. Default to one primary action per screen.

If the system can compute a field (full name from first + last, total from line items), compute it. Do not ask.

---

## 6. Doherty Threshold

### Definition

Productivity rises sharply when system response time falls below 400ms. Above that, users wait. Below that, users flow.

### When it applies

- Any interaction with a perceptible delay: clicks, taps, form submits, searches, autocomplete, page loads.

### How to use it in design

- Target sub-400ms for the perceived response to every action.
- For actions that cannot complete that fast: show immediate visual feedback within 100ms, even if the result takes longer.
- Use skeleton screens, optimistic UI, and instant transitions to keep the perceived response inside the threshold.
- For background operations, do not block the user. Let them continue.

### Violation pattern

- A button that does nothing for 1500ms after click. The user clicks again.
- A search bar where results take 2s to update. The user types faster than the system responds; they see stale results.
- A "Save" button that locks the entire UI while saving.

### Fix example

For an async save:

```js
async function save() {
  // Immediate feedback inside 100ms
  setSaving(true)
  setOptimisticState(newState)

  try {
    await api.save(newState)
    // Reconcile when the response lands
    setSaving(false)
  } catch (err) {
    // Roll back optimistic state
    setOptimisticState(prevState)
    setSaving(false)
    showError(err.message)
  }
}
```

The user sees the change at once. The server reconciles in the background. If something fails, the system rolls back and tells the user.

---

## 7. Fitts's Law

### Definition

The time to acquire a target is a function of the distance to the target and the size of the target. Bigger targets and closer targets are faster to hit.

### When it applies

- Buttons, links, taps, drags — every interactive element.
- Especially: primary CTAs, mobile controls, controls used in sequence.

### How to use it in design

- Make primary actions large.
- Place frequent actions near the user's natural pointer position. On desktop, near the current cursor. On mobile, in the thumb zone.
- Group sequential actions so the next one is close to the last.
- Edges and corners are "infinite" targets — the cursor stops there. Use them for high-frequency controls (menu bars at the top, close button at the corner).

### Violation pattern

- Tiny "x" buttons in modal corners that mobile users mis-tap.
- Primary CTAs the same size as secondary actions.
- Tap targets smaller than 44 by 44 pixels.
- Important buttons placed far from the user's hands on mobile (top-right on a phone held in the left hand).

### Fix example

For a mobile modal:

```css
.modal-close {
  min-width: 44px;
  min-height: 44px;
  /* Place in a thumb-reachable area, not the top corner alone */
}
.modal-primary-action {
  min-height: 56px;
  width: 100%;
  /* Sticky to the bottom of the modal, in the thumb zone */
}
```

Primary action is large, near the user's thumb. Close button has a generous target.

---

## 8. Flow

### Definition

Flow is a state of complete focused engagement, where time disappears and the user is fully absorbed in the task. It happens when the task's difficulty matches the user's skill, with no extraneous friction.

### When it applies

- Any task the user performs repeatedly or for extended periods: writing, coding, designing, gaming, browsing, configuring.

### How to use it in design

- Remove all friction from the path of the primary task.
- Minimize interruptions. Notifications, popups, and confirmations break flow.
- Match the user's pace. A system that lags or interrupts cannot host flow.
- Provide feedback that confirms the user is on the right track without requiring them to stop.

### Violation pattern

- An editor that pauses to save, blocking input.
- A notification panel that pops over the active task.
- A confirmation dialog for every small action.
- A "tips" tooltip that interrupts the user mid-task.

### Fix example

Auto-save in the background. Defer non-critical notifications until the user pauses. Reserve confirmations for destructive actions. Replace prescriptive tips with optional, dismissible discovery.

A good writing app: the cursor blinks, the words appear, nothing else moves. The save indicator pulses for half a second, then fades. The user remains in flow.

---

## 9. Goal-Gradient Effect

### Definition

Motivation intensifies as the user nears the goal. Showing progress accelerates completion.

### When it applies

- Multi-step flows: signup, checkout, onboarding, configuration.
- Loyalty programs: progress toward rewards.
- Learning paths: progress toward a credential.
- Task lists: progress toward completion.

### How to use it in design

- Show progress explicitly. "Step 3 of 5." A progress bar. Checkmarks on completed items.
- Front-load early wins. Make the first step easy so the user gets a "done" feeling and momentum.
- Reinforce as the user nears the end. "One more step." "Almost done."

### Violation pattern

- Multi-step flows with no progress indicator. The user does not know how much is left.
- Onboarding that hides the first reward behind a long form. The user gives up before tasting the value.
- A loyalty program that hides how close the user is to the next reward.

### Fix example

A 5-step onboarding:

```html
<div class="onboarding-progress">
  <span class="step done">1. Account</span>
  <span class="step done">2. Profile</span>
  <span class="step current">3. Invite team</span>
  <span class="step">4. Choose plan</span>
  <span class="step">5. Done</span>
</div>
```

The user sees how far they have come and how little is left. Motivation rises near the end.

---

## 10. Hick's Law

### Definition

Decision time grows logarithmically with the number and complexity of choices. More choices, more time, more abandonment.

### When it applies

- Menus, navigation, dropdowns, settings panels.
- Pricing pages.
- Any moment the user has to choose between options.

### How to use it in design

- Cap the number of visible choices. Aim for under seven; ideally under five.
- Categorize and progressively disclose. Group related options under a parent.
- Sort by frequency or recommendation. The most likely choice is first.
- Use defaults to remove the choice when possible.

### Violation pattern

- A nav bar with twelve top-level items.
- A dropdown with fifty unsorted options.
- A "configure your account" wizard with fifteen toggles, none recommended.

### Fix example

A nav bar:

```html
<nav>
  <a href="/products">Products</a>
  <a href="/pricing">Pricing</a>
  <a href="/customers">Customers</a>
  <a href="/docs">Docs</a>
  <a href="/account">Account</a>
</nav>
```

Five items, each clearly distinct. Sub-navigation lives one level deeper.

---

## 11. Jakob's Law

### Definition

Users spend most of their time on sites other than yours. They expect your site to work like the sites they already know.

### When it applies

- Page layout. Navigation placement. Iconography. Interaction patterns.
- Anywhere a user has a strong prior expectation from other products.

### How to use it in design

- Follow conventions by default. Search top-right, account top-right, logo top-left, footer at the bottom.
- Adopt patterns that have won across major products. A hamburger on mobile, a sticky CTA at the bottom, a tab bar for primary navigation.
- Deviate only when you have a tested reason and the benefit clearly exceeds the cost.

### Violation pattern

- Custom navigation patterns that look novel but force users to learn from scratch.
- Icons that mean something different from the cross-product norm. (A gear that opens search, for example.)
- Unique interaction patterns for common tasks (sign in, search, checkout).

### Fix example

Use the cart icon for the cart. The hamburger for the menu. The gear for settings. The magnifying glass for search. Save your inventiveness for features that have no convention yet.

---

## 12. Law of Common Region

### Definition

Elements perceived as sharing a defined boundary (a card, a box, a background fill) are grouped, regardless of their other properties.

### When it applies

- Card-based layouts.
- Form sections.
- Lists with sub-groups.
- Any time you need the user to perceive a group at a glance.

### How to use it in design

- Use a defined boundary (a card, a tinted background, a border) to group related elements.
- Make boundaries match the grouping you want the user to perceive. Do not box random items.
- Strip boundaries from elements that should not be perceived as grouped.

### Violation pattern

- Items in the same card that do not belong together. The boundary lies.
- Items that belong together but live in separate cards. The boundary divides them.
- Boundaries used decoratively, with no semantic intent. The user infers grouping that is not real.

### Fix example

```html
<!-- A card groups title, body, and action — all related -->
<article class="card">
  <h3>Mediterranean trip</h3>
  <p>Greek islands, 7 days.</p>
  <button>View itinerary</button>
</article>
```

Three elements, one boundary, one perceived group. The user reads the card as a unit.

---

## 13. Law of Proximity

### Definition

Objects near each other are perceived as related. Objects far from each other are not.

### When it applies

- Form fields and their labels.
- Buttons and their captions.
- Cards in a grid.
- Headings and their content.

### How to use it in design

- Place a label close to its field. The visual distance signals the relationship.
- Group items that belong together; separate items that do not.
- Use spacing intentionally — every gap communicates "these are not the same group."

### Violation pattern

- Form labels far from their fields. The user has to mentally connect.
- Buttons with two equal-distance neighbors. The user does not know which button this caption belongs to.
- Cards in a grid with uneven spacing, suggesting accidental grouping.

### Fix example

```html
<!-- Label and field are close; the field-error is closer to the field than to the next field -->
<div class="field">
  <label for="email">Email</label>
  <input id="email" type="email">
  <p class="field-error">Required.</p>
</div>

<div class="field">
  <label for="phone">Phone</label>
  <input id="phone" type="tel">
</div>
```

The user sees email and phone as separate, the error as belonging to email.

---

## 14. Law of Prägnanz

### Definition

When the user sees something ambiguous, they interpret it as the simplest possible form. The brain seeks regularity and order.

### When it applies

- Logos, icons, illustrations.
- Complex layouts.
- Charts and data visualizations.
- Anywhere the user must perceive structure from visual input.

### How to use it in design

- Reduce visual complexity. Strip detail that does not add meaning.
- Use simple shapes for icons. Users perceive them faster and more accurately.
- Align elements to a grid. Regularity reduces interpretation cost.

### Violation pattern

- Overdrawn icons with detail at icon scale that disappears at icon scale.
- Layouts that mix two grids. The user cannot construct a coherent layout in their head.
- Charts with too many series, too many colors, too many annotations. The user cannot pull a story from the noise.

### Fix example

```css
/* Use a consistent stroke weight for icons, simple geometry */
.icon {
  width: 24px;
  height: 24px;
  stroke: currentColor;
  stroke-width: 1.5;
  fill: none;
}
```

Simple, consistent icons. The user reads them at a glance.

For charts, strip every line, gridline, and label that is not necessary. The story should be visible without effort.

---

## 15. Law of Similarity

### Definition

Elements that look similar are perceived as related. Style is a grouping signal.

### When it applies

- Repeating elements (cards, list items, table rows).
- Action buttons.
- Status indicators.
- Categorical color and shape.

### How to use it in design

- Style similar things the same. All primary buttons look the same. All cards in a grid match. All headings at the same level share their styling.
- Differentiate dissimilar things. Primary buttons look different from secondary buttons. Warnings look different from confirmations.
- Use color, shape, and weight as grouping signals.

### Violation pattern

- A page with three primary buttons in three different styles. The user reads them as three different kinds of action.
- Status indicators where the same color means different things in different parts of the product.
- Headings that vary in style across the same page, suggesting different hierarchical levels.

### Fix example

Define a small palette of components and use them consistently. Every primary action button looks the same. Every error indicator uses the same red. Every card in a grid shares its styling.

---

## 16. Law of Uniform Connectedness

### Definition

Elements visually connected (by a line, a shape, a shared container) are perceived as more related than elements merely close together.

### When it applies

- Diagrams, flowcharts, network graphs.
- Forms with conditional fields connected to a parent.
- Tab groups, list items with shared backgrounds.
- Any time you need a stronger grouping signal than proximity alone.

### How to use it in design

- Use connecting lines to show flow or hierarchy.
- Use shared containers for stronger grouping than spacing alone provides.
- Reserve uniform connectedness for stronger relationships; proximity for weaker ones.

### Violation pattern

- Flowcharts where the arrows are missing or unclear. The user cannot follow the flow.
- Forms where a "follow-up" field appears far from its trigger. The user does not connect them.

### Fix example

For a tabbed interface, the active tab is visually connected to the content below by a shared background or by extending the tab into the content area. The user perceives "this tab owns this content."

For conditional fields, indent and connect with a vertical line:

```
[ ] Notify me by email
    └── How often?
        [Daily ▾]
```

The user sees that "How often?" only applies when the parent is checked.

---

## 17. Mental Model

### Definition

A mental model is the user's compressed, working understanding of how a system behaves. It is built from the system image — everything the user sees, hears, reads, and remembers about the product.

The user's mental model does not have to be accurate. It has to be useful enough that the user can predict what will happen next.

### When it applies

- New product adoption.
- Recovery from error.
- Migration from competing products.
- Any feature that introduces a new concept.

### How to use it in design

- Pick a clear, consistent metaphor and use it everywhere — UI, docs, marketing, error messages.
- Surface hidden state. If the system is doing something, show it.
- Avoid magic. Magic looks great until it breaks; when it breaks, the user has no model to recover.
- Match the model to the user's prior expectations when possible. Diverge only when the divergence has a clear benefit.

### Violation pattern

- Inconsistent vocabulary across the product. The dashboard says "Members," the settings say "Users," the API says "Accounts." Three models for the same thing.
- Hidden async behavior. A field saves when the user moves on, but no indicator says so. The user does not know whether their change took.
- Magic features the user cannot explain. "It just works" until it does not.

### Fix example

Pick a vocabulary and enforce it. If your unit is "team," every screen, label, doc, and email says "team." Not "group," not "workspace," not "org."

Externalize state. A sync indicator, a saved indicator, a "last updated" timestamp. The user reads the system image to construct the model.

---

## 18. Miller's Law

### Definition

The average person can hold about seven items (plus or minus two) in working memory at one time. Beyond that, performance degrades.

### When it applies

- Navigation menus.
- Lists of options the user must compare.
- Tabs.
- Items in a single field's autocomplete.

### How to use it in design

- Cap visible items at five to nine. Above that, group or paginate.
- For navigation, prefer five to seven top-level items.
- For comparing options, group attributes so the user can hold the groups in memory rather than each item.
- For autocomplete, show no more than seven results at a time.

### Violation pattern

- A nav bar with twelve top-level items. The user has to scan.
- A comparison table with ten rows and seven columns. The user cannot hold any of it.
- An autocomplete that lists thirty results. The user picks from the first three.

### Fix example

Group a nav with twelve items into five categories of two to three each. The user reads the categories at a glance and dives in.

For a comparison table, group attributes into "Features," "Pricing," "Support." The user reads the groups, then the rows within each group.

---

## 19. Occam's Razor

### Definition

When choosing between two solutions, prefer the one with fewer assumptions, fewer parts, fewer steps. The simplest viable solution is usually the right one.

### When it applies

- Feature design: which approach to take.
- UI design: which controls to use.
- Information architecture: which structure fits.
- Any time the team is debating two equally valid designs.

### How to use it in design

- Default to the simplest design that meets the requirement.
- For every element, ask: "What would happen if this were gone?" If the answer is "nothing important," cut it.
- Add complexity only when a specific user need demands it.

### Violation pattern

- Custom date pickers when a native input would work.
- Carousels with five panels when a single hero would communicate the message.
- Animation that performs no functional purpose, only delay.

### Fix example

Replace a custom dropdown with a native `<select>` when the styling is not critical. Less code, fewer bugs, better accessibility, the same user task.

Replace a carousel with the single most important message. The user does not see the message that was on slide 4. They see the one you chose.

---

## 20. Paradox of the Active User

### Definition

Users start using a product before they read any instructions. They skip onboarding. They ignore tooltips. They learn by doing, by failing, and by recovering.

### When it applies

- Onboarding flows. (They will be skipped.)
- Help documentation. (It will not be read.)
- Tooltips. (They will not be hovered.)
- Empty states. (The user will not read the prose.)

### How to use it in design

- Design for action, not for reading. Every screen should support the user's first attempt.
- Use defaults so the user can do something useful before learning anything.
- Reserve help for the moment the user fails. Embed help near the source of confusion.
- Make undo cheap. The user is going to do the wrong thing. Let them get back.

### Violation pattern

- A 10-step onboarding tour the user must complete before using the product. Users will exit the app rather than finish.
- Help that lives on an external site, accessed via a "?" icon in the corner.
- Empty states with three paragraphs of explanation. The user wants to act.

### Fix example

Empty state for a project list:

```html
<div class="empty-state">
  <h2>No projects yet</h2>
  <p>Start with a template or from scratch.</p>
  <button>Use template</button>
  <button>Start blank</button>
</div>
```

The user can act in one click. No prose to read.

For onboarding, replace the tour with sensible defaults and a sample dataset. The user explores by doing.

---

## 21. Pareto Principle

### Definition

Roughly 80% of effects come from 20% of causes. In product, 80% of usage comes from 20% of features. Identify the 20% and prioritize it.

### When it applies

- Feature prioritization.
- UI prominence (which features get top-level real estate).
- Performance optimization (which paths to fast-path).
- Support content (which problems generate the most tickets).

### How to use it in design

- Identify the high-frequency 20% by usage data, not intuition.
- Give the 20% the most prominent real estate.
- Push the other 80% into menus, settings, and progressive disclosure.
- For optimization: profile, find the 20% of code or routes that account for 80% of latency, fix those first.

### Violation pattern

- A toolbar where every feature gets equal real estate. The 20% is buried.
- A help center organized by feature rather than by problem frequency. Common problems are no easier to find than rare ones.
- Performance work spread across every component equally, with no path optimized.

### Fix example

In a writing app, the 20% is open, type, save. Those three get the most prominent UI. Spell-check, formatting, sharing, collaboration are one click in. Statistics, plugins, integrations are two clicks in.

---

## 22. Parkinson's Law

### Definition

Work expands to fill the time available for its completion. Without constraint, a task will take longer than it needs to.

### When it applies

- User-facing time limits (sessions, sales, holds).
- Internal estimates and deadlines.
- Forms with no implicit pace.

### How to use it in design

- Use time constraints where they fit the user's interest (a 10-minute checkout hold, a 24-hour delivery slot, an expiring discount that is real).
- Avoid arbitrary time constraints that pressure the user without benefit.
- For tasks the user controls, default to fast paths. Auto-fill, smart defaults, one-click flows.

### Violation pattern

- Manufactured urgency ("Only 5 hours left!") with no real deadline. Users learn to distrust.
- Checkout flows that take five minutes when one minute is plenty.
- Forms that demand twelve fields when four would suffice.

### Fix example

For a real session timeout: show a clear countdown a minute before expiry, with a one-click "Stay signed in" option. Honest urgency, no surprise.

For a checkout: prefill what you know. Default the shipping address to the saved one. Default the payment method. The user reviews and confirms in seconds.

---

## 23. Peak-End Rule

### Definition

Experiences are remembered by their peak and their ending, not by their average. The user's recollection is dominated by the most intense moment and the final moment.

### When it applies

- Onboarding (first impression is the peak).
- Checkout (last impression is the ending).
- Error recovery (the ending defines whether the user came back).
- Any user journey with a beginning and an end.

### How to use it in design

- Identify the peak moment. Make it intentional. Make it memorable for the right reason.
- Design the ending. The last screen the user sees is what they remember.
- For long journeys, end with a clear, satisfying state. "Done." "Sent." "Welcome."
- Avoid ending on bureaucracy. A "thank you for your purchase" page that is just a receipt feels flatter than one that confirms the value.

### Violation pattern

- A signup that ends with a "verify your email" screen and no further direction. The user leaves on a chore.
- A purchase confirmation that lists prices and SKUs but does not name what the user just bought.
- An error that ends with "An error occurred." The user remembers the failure, not your recovery.

### Fix example

End a signup with: "Welcome, Alice. Here is your first project." The user lands on something real, with their name on it. Memorable for the right reason.

End a purchase with: "On its way. Estimated delivery: Tuesday." A concrete next event the user can hold onto.

---

## 24. Postel's Law

### Definition

Be liberal in what you accept; be conservative in what you send. Accept input in many forms; produce output in one consistent form.

### When it applies

- Form input parsing.
- API contracts.
- File imports.
- Any boundary where the user's format may not match the system's.

### How to use it in design

- For phone numbers, accept any reasonable format. Strip spaces, dashes, parentheses. Normalize internally.
- For dates, accept multiple formats. Show clearly which one the user is in.
- For emails, accept case-insensitively. Normalize to lowercase for storage.
- For currency, accept "1,000.00" and "1000" and "1k" if appropriate.
- For output, always show one consistent format.

### Violation pattern

- A phone field that rejects "0797-868-335" because of the dash.
- A date field that rejects "2026-05-24" because it expected "05/24/2026."
- An email field that fails on "Alice@Team.com" because of the capital A.

### Fix example

```js
function normalizePhone(input) {
  // Strip everything that is not a digit or a leading +
  const cleaned = input.replace(/[^\d+]/g, '')
  return cleaned
}
```

The user types whatever feels natural. The system normalizes. The user sees the normalized version (so they can verify), but the system accepts more than it shows.

---

## 25. Selective Attention

### Definition

Users focus on goal-related stimuli. Everything else is ignored, even when visually prominent. If it does not match the goal, it does not exist for the user.

### When it applies

- Marketing pages where the user is hunting for one specific piece of information.
- Forms where the user wants to finish, not browse.
- Search results where the user is looking for one specific result.

### How to use it in design

- Identify the user's goal on each screen. Place goal-related content where attention falls.
- Reduce competing stimuli. Cut promotional banners, distracting animations, irrelevant recommendations on goal-focused screens.
- Use visual hierarchy to put the goal-related action where the user's eye naturally lands.

### Violation pattern

- A checkout page with a banner advertising other products. The user is hunting for the "Confirm" button.
- A pricing page where the recommended plan is not visually distinct. The user has to scan to figure out what is recommended.
- A search result page with promotional cards interleaved with results. The user ignores everything that is not a result, or worse, becomes irritated.

### Fix example

On a checkout page, the only non-goal content is a small "Need help?" link. The order summary, the payment fields, and the "Place order" button take all the focus. No upsell banners.

---

## 26. Serial Position Effect

### Definition

In a list, the first and last items are remembered best. Items in the middle are forgotten.

### When it applies

- Navigation menus.
- Pricing tiers.
- Carousels.
- Lists of features.
- Search results.

### How to use it in design

- Put the most important items at the start and the end of any list.
- For pricing, place the recommended plan first or last (or use Von Restorff to distinguish it).
- For navigation, place the most-used items at the ends.

### Violation pattern

- A navigation menu where the most important item is fourth out of seven, buried in the middle.
- A pricing table where the recommended plan is in the middle, with no other visual distinction.
- A list of features where the most compelling one is item six out of ten.

### Fix example

In a nav: Home, Products, Pricing, Customers, Docs, Account. The two ends are anchors. Place the most important sections at the start or end.

In a pricing table of three plans, the middle plan is often used because it is the recommended one — and to defeat the serial position effect, it is also visually distinguished (a different background, a "Most popular" badge).

---

## 27. Tesler's Law (The Law of Conservation of Complexity)

### Definition

Every system has an irreducible minimum of complexity. The question is not whether complexity exists; the question is who pays the cost — the system or the user.

### When it applies

- Configuration screens.
- Forms with conditional logic.
- Anywhere a sensible default would relieve the user of a choice.

### How to use it in design

- For every decision the user must make, ask: "Could the system make this decision instead?"
- Push as much complexity as possible into the system. Defaults, computed values, smart routing, inference from context.
- When complexity must surface to the user, surface it where the user is best equipped to handle it.

### Violation pattern

- A signup that asks for time zone when the browser knows it.
- A form that asks the user to enter their company size into three different forms, when one would suffice.
- A configuration screen that exposes every option, including those 99% of users will never touch.

### Fix example

For a new account: infer time zone from the browser. Infer country from IP. Default currency to the locale's currency. The user can override if needed; the system has done the work.

```js
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone
const userLocale = navigator.language
```

The user does not see the question; the system has answered it.

---

## 28. Von Restorff Effect (the Isolation Effect)

### Definition

An item that visually stands out from its neighbors is more likely to be noticed and remembered.

### When it applies

- Primary CTAs in a row of buttons.
- The recommended option in a list of options.
- The current step in a multi-step flow.
- An alert in a calm interface.

### How to use it in design

- Use isolation purposefully. The standout element is the one you want noticed.
- Limit standout to one element per visual frame. Two standouts cancel each other.
- Strip standouts from anything that is not action-critical. Decorative isolation is noise.

### Violation pattern

- A page with three primary buttons in three different bright colors. None stands out; all compete.
- A pricing table where every plan has a "Most popular" badge. The signal is meaningless.
- A dashboard with five red badges. The user does not know which is urgent.

### Fix example

A pricing table: two plans in neutral cards; the recommended plan in a card with a colored border, a slight elevation, and a "Most popular" badge. One standout, one signal.

A button row: the primary action is filled and saturated; secondary actions are outline-only. One standout.

---

## 29. Working Memory

### Definition

Working memory is the temporary, limited cognitive holding area where the user keeps the information they are currently using. It is small, easily disrupted, and discharges quickly.

### When it applies

- Forms with many fields.
- Multi-step flows where each step requires remembering the previous step's input.
- Dashboards with many numbers.
- Comparison tables.

### How to use it in design

- Externalize state. Show what the user has already done so they do not have to remember.
- Show what the user has chosen on multi-step flows. Echo it back.
- Limit the number of new pieces of information per screen.
- Avoid making the user hold a number, code, or detail in memory across screens.

### Violation pattern

- A wizard where step 4 asks the user to confirm a number they entered in step 1. The user has to remember.
- A comparison table where the user must look at one plan, scroll to the next plan, and compare from memory.
- A code shown briefly before a screen change, with no easy way to retrieve it.

### Fix example

A multi-step wizard:

```html
<aside class="wizard-summary">
  <h3>Your trip</h3>
  <p>Destination: Athens</p>
  <p>Dates: Jun 12 — Jun 19</p>
  <p>Travelers: 2 adults</p>
</aside>
```

The user sees their own choices on every step. They do not hold them in memory.

For a confirmation code, show it on the screen until the user explicitly continues. Do not flash it for two seconds and move on.

---

## 30. Zeigarnik Effect

### Definition

Uncompleted or interrupted tasks are remembered more vividly than completed ones. The brain hangs on to the unfinished.

### When it applies

- Onboarding (incomplete steps stay on the user's mind).
- Multi-step flows.
- Saved drafts and partial submissions.
- Notifications about pending actions.

### How to use it in design

- Surface incomplete tasks intentionally. A progress bar, a "complete your profile" checklist, a "draft saved" indicator.
- Use the effect to bring users back: a notification about an unfinished task is more compelling than one about a completed one.
- Do not abuse it. A perpetual "complete your profile" nag with no end becomes noise.

### Violation pattern

- An onboarding checklist with no end. The user is permanently 60% complete.
- An "unfinished task" notification for a task that does not exist (e.g., a draft that was already submitted).
- A wizard that hides its progress, denying the user the closure of completion.

### Fix example

An onboarding checklist:

```
[x] Create account
[x] Set up profile
[ ] Invite team (skip if solo)
[ ] Start first project
```

The user sees what is done, what remains, and is gently pulled back to finish. When everything is done, the checklist disappears or transforms into a completion state.

---

## Putting it together: review checklist

For any screen or flow, run through these in order. The first failure is rarely the last.

### Perception

- **Aesthetic-Usability**: does the design feel considered, calm, on-brand?
- **Common Region, Proximity, Similarity, Uniform Connectedness**: are visual groupings intentional?
- **Prägnanz**: is the visual structure simple and regular?
- **Von Restorff**: is the standout element the one you want noticed?

### Cognition

- **Cognitive Load**: where is the user paying attention they should not have to?
- **Chunking, Miller's Law, Working Memory**: are you respecting the user's limits?
- **Mental Model**: is the model consistent across the product?
- **Selective Attention**: is goal-related content where the user looks?

### Decision

- **Choice Overload, Hick's Law**: too many options?
- **Cognitive Bias**: are defaults set in the user's interest?
- **Occam's Razor**: is this the simplest solution that meets the requirement?

### Action

- **Doherty Threshold**: does every action feel fast?
- **Fitts's Law**: are targets large, reachable, well-placed?
- **Postel's Law**: does the system accept what the user types and normalize?
- **Tesler's Law**: are you pushing complexity onto the user that the system could absorb?

### Journey

- **Goal-Gradient, Zeigarnik**: do users see progress and pull toward completion?
- **Paradox of the Active User**: does the design assume the user reads instructions? They do not.
- **Parkinson's Law**: are time and step counts in the user's interest?

### Memory

- **Serial Position**: are key items at the start and end?
- **Peak-End**: is the peak intentional? Is the ending memorable for the right reason?

### Flow

- **Flow**: are interruptions minimized for the primary task?
- **Jakob's Law**: do conventions match the user's prior expectations?

### Pattern

- **Pareto Principle**: is the 20% getting the prominence and the optimization?

A design that scores well on all thirty is rare and admirable. A design that scores poorly on more than five is sloppy. The job is to find the violations, name them, and fix them.
