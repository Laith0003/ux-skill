# The 30 Laws of UX

30 cognitive laws every UX designer applies — Fitts's Law, Hick's Law, Miller's Law, Jakob's Law, and 26 others. For each: the definition, when it applies, the violation pattern, and a fix example.

This is the canonical reference: how to spot a law in the wild, what breaks when you ignore it, and the specific correction that turns the screen around. Every law is grounded in cognitive psychology and behavioral research. Every fix is shippable.

The laws fall into four families:

- **Cognitive load and memory** — Miller's Law, Working Memory, Chunking, Cognitive Load, Selective Attention, Serial Position Effect
- **Decision and action** — Hick's Law, Choice Overload, Fitts's Law, Tesler's Law, Pareto Principle, Occam's Razor, Postel's Law, Doherty Threshold
- **Perception and Gestalt** — Law of Proximity, Law of Similarity, Law of Common Region, Law of Uniform Connectedness, Law of Prägnanz, Von Restorff Effect
- **Behavior and motivation** — Goal-Gradient Effect, Zeigarnik Effect, Peak-End Rule, Aesthetic-Usability Effect, Flow, Mental Model, Cognitive Bias, Paradox of the Active User, Parkinson's Law, Jakob's Law

Apply them in review, in critique, in audit. Apply them in generation, in handoff, in QA. They compound.

---

## 1. Aesthetic-Usability Effect

**Definition.** Users perceive aesthetically pleasing designs as more usable than less attractive ones, even when the underlying usability is identical. Beauty creates a halo that excuses minor friction.

**When it applies.** First-impression surfaces — landing pages, marketing sites, onboarding screens, hero sections, login flows. Anywhere trust is being earned in the first ten seconds.

**Violation pattern.** Engineers and analytical reviewers dismiss visual craft as "polish" or "the cherry on top," shipping functional-but-ugly interfaces and wondering why support tickets and bounce rates climb. The reverse violation: beautiful surfaces that hide real usability problems and never get fixed because users blame themselves.

**Fix example.** Treat aesthetic craft as a usability requirement, not a separate concern. Allocate time for spacing, typographic rhythm, color tone, and motion fidelity in every sprint. Then run usability tests anyway — beauty doesn't fix broken IA, but ugliness amplifies every other flaw.

**How to spot in review.** Look for screens that are technically correct but visually flat — equal spacing everywhere, default fonts, identical card sizes, no hierarchy beyond size. If the screen looks like a wireframe, it will test like a wireframe.

---

## 2. Choice Overload

**Definition.** Beyond a small set of options, additional choices reduce conversion, increase regret, and slow decisions. The cognitive cost of comparison rises faster than the value of the extra option.

**When it applies.** Pricing pages, plan selection, settings menus, filters, dropdown menus, navigation, product catalogs, payment methods.

**Violation pattern.** Five pricing tiers because "more options means more conversion." Seven payment methods at checkout because legal asked for them all. Thirty filter checkboxes because the data is there.

**Fix example.** Three pricing tiers with one pre-selected as recommended. Two payment methods visible by default with "more options" disclosure. Smart-default filters that pre-narrow the set before exposing the long tail.

**How to spot in review.** Count the choices on any decision surface. Above seven, redesign. Above twelve, the screen is broken regardless of how it tests in isolation — long-term conversion data will reveal the cost.

---

## 3. Chunking

**Definition.** The human mind groups related items into chunks; the chunk becomes the unit of cognition, not the individual item. Phone numbers as 3-3-4 chunks beat ten digits in a row. The chunk is what survives in working memory.

**When it applies.** Forms, phone numbers, credit card fields, OTP inputs, long lists, settings, dashboards, complex tables, legal documents, error messages.

**Violation pattern.** A 16-digit credit card field with no spacing. A 10-line address form rendered as one undifferentiated column. A settings page with forty toggles in a single list.

**Fix example.** Group the credit card field with visual gaps every four digits. Break the address form into "Street" / "City + State + Zip" / "Country" chunks with subtle dividers. Group settings into named sections with a maximum of seven items each. Dashboards: cluster related KPIs, separate clusters with whitespace, not lines.

**How to spot in review.** If you can describe a section out loud in one sentence ("the contact info chunk"), it's chunked. If you can't, regroup until you can.

---

## 4. Cognitive Bias

**Definition.** Systematic patterns of deviation from rational judgment that affect every user, including designers. Confirmation bias, anchoring, availability heuristic, framing effects, sunk cost, and dozens more shape what users perceive and decide.

**When it applies.** Every persuasive surface — pricing, social proof, comparison tables, defaults, onboarding sequences, error states, recovery flows.

**Violation pattern.** Designing as if users are rational evaluators of feature lists. Comparing your product to competitors on dimensions users don't actually weigh. Burying the anchor (the highest price, the most-featured plan) when its presence is what makes the chosen tier feel reasonable.

**Fix example.** Use anchoring deliberately: show the higher tier first so the middle tier reads as the value pick. Use defaults intentionally — most users keep them. Use loss-framing on retention surfaces ("you'll lose your streak") and gain-framing on acquisition surfaces ("you'll get").

**How to spot in review.** Ask: which bias does this screen lean on, intentionally? If the answer is "none," the screen is leaving conversion on the table or, worse, working against itself.

---

## 5. Cognitive Load

**Definition.** The total mental effort required to use an interface, summed across perception, decision, and motor action. Working memory caps total cognitive load at roughly four chunks. Exceed that ceiling and performance collapses.

**When it applies.** Every screen. Especially: dashboards, forms, complex workflows, multi-step tasks, comparison surfaces, configuration UIs.

**Violation pattern.** Three competing primary CTAs. Seven different font sizes on one page. Information density that prides itself on "showing everything" instead of "showing what matters." Modal stacked on modal. Tooltip on a tooltip.

**Fix example.** Strip the screen until something breaks, then add back only what's essential. One primary CTA. Two typographic scales (heading, body). Information dense enough to be useful, sparse enough to be readable. Progressive disclosure for the rest.

**How to spot in review.** Squint at the screen for three seconds. If you cannot identify the primary action and the primary information, the cognitive load is too high. Squint test fails, design fails.

---

## 6. Doherty Threshold

**Definition.** Productivity soars and engagement compounds when system response time stays under 400 milliseconds. Above that threshold, users disengage, multitask, lose flow, and stop trusting the system.

**When it applies.** Every interactive surface — search, filters, navigation, form submission, image loading, autocomplete, chat, anywhere the user does a thing and waits for the system to react.

**Violation pattern.** Search that takes 2 seconds and shows no loading state. Form submission with no immediate feedback. Image-heavy pages that block on hero asset load. Autocomplete that lags one keystroke behind the input.

**Fix example.** Optimistic UI for everything user-initiated — show the new state immediately, reconcile in background. Skeleton screens during loads. Debounce autocomplete at 100-150ms, not 300. Lazy-load below the fold. If a server round-trip must take longer, show progress in real-time, not as a spinner.

**How to spot in review.** Use the network throttle in DevTools to simulate 3G. Click around. If anything takes longer than 400ms without visible feedback, fix it.

---

## 7. Fitts's Law

**Definition.** The time to acquire a target is a function of distance to it and size of it. Bigger targets, closer targets, are faster. Targets at screen edges have effectively infinite size in one dimension because the cursor stops at the edge.

**When it applies.** Every clickable element. Especially: primary CTAs, navigation, close buttons, mobile touch targets, drag handles, scroll bars, dropdowns.

**Violation pattern.** A 12px close button in the top corner. A primary CTA the same size as five other secondary buttons. Mobile tap targets smaller than 44x44 points. A submit button at the bottom of a long form on mobile, requiring a precise tap after a thumb stretch.

**Fix example.** Primary CTA 48-56px tall, padded for easy targeting, visually distinct from secondary actions. Close buttons 32px minimum with 8px padding for a 48px effective target. Mobile tap targets 44x44 minimum, 48x48 preferred, with 8px spacing between adjacent targets. Place destructive actions far from primary actions to prevent accidental clicks.

**How to spot in review.** Measure every interactive target. Under 44px on mobile, under 32px on desktop for non-text controls, fix. Adjacent targets touching, add spacing.

---

## 8. Flow

**Definition.** The state of complete absorption in an activity where time distorts, self-consciousness fades, and the activity becomes its own reward. Flow requires clear goals, immediate feedback, and a challenge balanced to skill.

**When it applies.** Repeat-use products, games, creative tools, dashboards, command interfaces, anything users spend hours in. Less directly applicable to one-shot transactional surfaces.

**Violation pattern.** Interrupting modals that break concentration. Forced tutorials that gate access. Slow response times. Confirmation dialogs for low-stakes actions. Notifications during focused work. Mode shifts the user didn't initiate.

**Fix example.** Reduce interruptions to the minimum legally required. Use inline hints, not modals. Make undo first-class so confirmation dialogs become unnecessary. Schedule notifications around the user's flow, not the system's clock. Keyboard shortcuts for power users. No mode shifts without explicit user action.

**How to spot in review.** Time a power user through a 10-minute task. Count interruptions — modals, confirmations, loading states, mode shifts. Above three, flow is broken.

---

## 9. Goal-Gradient Effect

**Definition.** Motivation increases as the goal nears. The closer to completion, the harder users push. Progress visibility accelerates engagement; perceived stalling kills it.

**When it applies.** Multi-step forms, onboarding, loyalty programs, checkout flows, profile completion, learning paths, gamification.

**Violation pattern.** A progress bar that starts at 0% on step one. A checkout that never communicates how many steps remain. An onboarding sequence with no end in sight. Loyalty tiers where progress to the next tier is invisible.

**Fix example.** Start the progress bar at 10-15% on step one — endowed progress accelerates completion. Show "Step 2 of 4" not just "Step 2." Surface tier progress prominently: "320 points to Silver." Pre-fill what you can; every pre-filled field counts as progress.

**How to spot in review.** On any multi-step flow, ask: can the user see how close they are to done at every step? If no, add the indicator. If the indicator demotivates (too far to go), redesign the flow into smaller flows.

---

## 10. Hick's Law

**Definition.** Decision time increases logarithmically with the number of choices. Doubling the options doesn't double the time — but more options always means slower decisions and more errors.

**When it applies.** Menus, navigation, dropdowns, settings, filters, action sets, any moment the user must choose.

**Violation pattern.** A primary navigation with 12 top-level items. A "More" menu with 30 entries. A dropdown with 50 options and no search. A toolbar with 20 icons of unclear function.

**Fix example.** Primary navigation: 5-7 items maximum, grouped by user task not by internal team. Dropdowns over 10 items: add search and recent items. Toolbars: group by function with visual separators; hide rarely-used actions in an overflow menu.

**How to spot in review.** Count primary navigation items. Above 7, redesign the IA. Count actions in any single action set. Above 5, redesign.

---

## 11. Jakob's Law

**Definition.** Users spend most of their time on other sites and products. They prefer your site to work the same way as all the others they already know. Convention is a usability feature.

**When it applies.** Universally. Especially: e-commerce checkout, navigation patterns, form layouts, login flows, password reset, search interfaces, sign-in flows.

**Violation pattern.** A creative reinterpretation of the shopping cart icon. A "novel" date picker. A login flow with the email below the password. Hamburger menu icon on desktop where users expect horizontal nav. Putting the search bar in an unexpected location to be "different."

**Fix example.** Use the magnifying glass icon for search. Put the cart in the top right. Email then password, top to bottom. Hamburger only on mobile-sized viewports. Logo top left, links to home. Save the creative interpretation for the brand work; the chrome should be invisible.

**How to spot in review.** For every UI pattern, ask: do the top three sites in this category do it this way? If not, what's the justification? "Differentiation" is not a justification for breaking convention on a transactional surface.

---

## 12. Law of Common Region

**Definition.** Elements within the same closed shape — a card, a panel, a bordered region — are perceived as belonging together, more strongly than spacing alone communicates. The border (or background tint) is the grouping signal.

**When it applies.** Dashboards, settings panels, multi-section forms, comparison tables, anywhere related information must visually cohere.

**Violation pattern.** Related fields sprinkled across a flat layout with only spacing to suggest grouping. A dashboard where five KPIs share the same canvas with no visual containment. Settings sections that bleed into one another.

**Fix example.** Wrap related fields in a card with consistent padding and a subtle border or tinted background. Give each dashboard KPI cluster its own panel. Use clear backgrounds (light tint, 1px border, soft shadow) to define a region — don't rely on whitespace alone when content is dense.

**How to spot in review.** Squint at the layout. Can you count discrete regions? If everything blurs together, you're underusing common region. If you count more than seven regions on one screen, you're overusing it.

---

## 13. Law of Proximity

**Definition.** Objects near each other are perceived as related. Proximity is the strongest of the Gestalt grouping principles; it overrides similarity, color, and shape.

**When it applies.** Forms (label-input pairing), navigation (groupings), card layouts, lists, captions to images, button groups.

**Violation pattern.** A form label 24px above its input but 8px from the input above it — the label visually pairs with the wrong field. A button group where buttons sit 16px apart and 8px from adjacent unrelated content. An image with its caption 32px below, equidistant from the next image.

**Fix example.** Form: label-to-its-own-input gap should be tighter than input-to-next-label gap (typical: 4-8px to its input, 16-24px to the next field). Buttons in a group: 4-8px spacing within the group, 24px+ between groups. Image-caption: 8px tight pairing, 32px to the next item.

**How to spot in review.** Measure vertical gaps in any form or grouped content. The gap inside a group should be ~half the gap between groups. If gaps are uniform, regroup.

---

## 14. Law of Prägnanz

**Definition.** The mind perceives ambiguous or complex images in their simplest possible form. Simplicity is the cognitive default; the user's brain will impose order even on noisy layouts, often in ways the designer didn't intend.

**When it applies.** Information design, logos, icons, data visualization, illustrations, complex layouts.

**Violation pattern.** Illustrations with too many competing elements that read as visual noise instead of as the intended subject. Logos with eight distinct shapes. Data visualizations where the user has to work to extract the comparison.

**Fix example.** Reduce illustrations to their essential silhouette. Test every icon at 16x16 — if it's not recognizable, simplify. Data viz: one chart, one comparison, one takeaway. If the user has to read the legend to understand the chart, redesign.

**How to spot in review.** Show any visual asset to someone for 3 seconds, then ask what it represents. If the answer doesn't match your intent, the form isn't pregnant — the meaning isn't springing out — and you need to simplify.

---

## 15. Law of Similarity

**Definition.** Elements that share visual properties (color, shape, size, orientation) are perceived as related. Similarity creates groups across distance; dissimilarity breaks groups even when items are close.

**When it applies.** Tagged content, status indicators, navigation states, button hierarchies, link styles, repeated patterns.

**Violation pattern.** All buttons styled identically — primary, secondary, destructive all look the same. Different statuses in a table styled with the same neutral pill. Active and inactive navigation items rendered identically.

**Fix example.** Primary CTA solid filled, secondary CTA outlined, tertiary CTA text-only — three clearly differentiated treatments. Statuses use semantic color (success green, warning amber, danger red) consistently across every table and surface. Active nav state has a clear visual difference (bold, color, indicator bar) from inactive.

**How to spot in review.** Pick any visual treatment and trace it across the product. Does it mean the same thing in every instance? If a green pill means "active" in one table and "approved" in another, the similarity law is leaking meaning.

---

## 16. Law of Uniform Connectedness

**Definition.** Visually connected elements are perceived as more related than unconnected ones, even when proximity and similarity say otherwise. A line, a border, or a connecting shape is the strongest grouping signal of all.

**When it applies.** Process diagrams, hierarchies, related-item indicators, timelines, step-flows, org charts, mind maps.

**Violation pattern.** A multi-step process where the steps sit isolated in their cards with no connecting line. A hierarchy rendered as nested indents without indicators of the parent-child relationship. A timeline without an axis.

**Fix example.** Multi-step process: connect steps with a horizontal line and dots, or a directional chevron. Hierarchy: tree lines, indent-with-line, or expand/collapse indicators. Timeline: a clear axis with consistent tick marks; events on the axis are related to each other through their shared connection.

**How to spot in review.** Look for sequences or hierarchies. If the relationship is meant to be read as a connection (step 1 leads to step 2), there should be a visual connector, not just adjacency.

---

## 17. Mental Model

**Definition.** A user's internal representation of how a system works, built from prior experience with similar systems and refined as they interact with this one. The closer the interface matches the user's mental model, the more usable the product.

**When it applies.** Universally. Especially: terminology, IA, navigation, workflows, error messages, status indicators, anywhere the user must predict what will happen.

**Violation pattern.** Internal product team's mental model leaks into the UI — using engineering terms in user-facing copy, organizing menus by team org chart, exposing database states as user states. The product's mental model fights the user's.

**Fix example.** Use the user's words, not yours. If they call it a "phone," call it a phone, not an "MSISDN" or "phone_e164." If they think of their work as "projects," don't expose the underlying "workspaces" abstraction. Run a card sort to discover the user's natural categories before designing IA.

**How to spot in review.** Read every label, every error, every empty state out loud to a non-team user. If they need explanation, the model has leaked.

---

## 18. Miller's Law

**Definition.** The average person can hold about 7±2 items in working memory. This is the famous "magical number seven," and it's the upper bound — practical UI design assumes far less.

**When it applies.** Menus, lists, navigation, options in any decision moment, items in a single comparison.

**Violation pattern.** Twelve primary navigation items. A pricing comparison with 25 features down the side. A dropdown with no visual chunking past item five.

**Fix example.** Cap any single grouping at 7 items, target 5. Chunk long lists into named sub-groups so the user holds the chunk name, not the items. Use search and filtering when the natural set exceeds the cap.

**How to spot in review.** Count items at every level of every grouping. Above 7, regroup. Above 9, redesign.

---

## 19. Occam's Razor

**Definition.** Among competing designs that achieve the same outcome, the simplest is best. Every added element must justify its cost in attention, cognitive load, and maintenance.

**When it applies.** Every design decision. Especially: feature additions, UI element additions, copy length, visual decoration, animation, settings, options.

**Violation pattern.** Decorative gradients that add no information. Three illustration styles fighting on one page. Verbose error messages that say in 40 words what 8 would carry. Feature flags exposed to users as toggles.

**Fix example.** Strip the page. Remove one element at a time and ask if the page got worse. If not, the element was unnecessary. Repeat until removal hurts. The remaining design is the answer.

**How to spot in review.** Point at every element on a screen and ask "what would happen if this were gone?" If the answer is "nothing important," remove it.

---

## 20. Paradox of the Active User

**Definition.** Users want to start using a product immediately, not read documentation first. Even when reading would save them time, they won't. They learn by doing, fail by doing, and only consult help when stuck.

**When it applies.** Onboarding, complex features, first-run experiences, settings, error recovery.

**Violation pattern.** A mandatory tutorial gating product access. A long onboarding sequence the user can't skip. Documentation that assumes the user has read previous documentation. Empty states with no clear first action.

**Fix example.** Skip the tutorial — let the user touch the product. Use just-in-time hints triggered by what the user is trying to do. Empty states with a single, obvious first action ("Add your first item"). Pre-fill examples so the user can edit, not start from blank. Make documentation contextual and findable from inside the action.

**How to spot in review.** First-run a new account. How many clicks before you can do the core thing? Above three, redesign. If a tutorial appears, can it be dismissed? If not, the paradox is being ignored.

---

## 21. Pareto Principle

**Definition.** Roughly 80% of effects come from 20% of causes. In UX: 80% of usage comes from 20% of features. 20% of users generate 80% of revenue. 20% of UI affordances handle 80% of tasks.

**When it applies.** Feature prioritization, UI hierarchy, navigation, default views, settings exposure, analytics decisions.

**Violation pattern.** Treating every feature as primary. Surfacing rarely-used settings alongside daily-use settings. Navigation that gives equal weight to "Settings" and "Search." Roadmaps that allocate equal effort to features used by 5% and features used by 80%.

**Fix example.** Identify the top 20% of features by usage. Make them one click. Hide the long tail behind progressive disclosure. Default views show the 80% case; the 20% case has a clear path but isn't in the way.

**How to spot in review.** Look at usage data. If the UI hierarchy doesn't match the usage distribution, redesign the hierarchy.

---

## 22. Parkinson's Law

**Definition.** Work expands to fill the time available. Users will take as long as you give them to complete a task. Defaults, constraints, and time-pressure cues change behavior.

**When it applies.** Forms, sessions, time-bounded actions, deadlines, free trials, expiry windows.

**Violation pattern.** A free trial with no end-date reminder until the last day. A form with no indication of expected completion time. A session that times out silently mid-task. A "save draft" feature so robust that users never complete the actual submission.

**Fix example.** Show trial countdown clearly from day 3 onward. Indicate "about 2 minutes" on forms. Warn before session timeout with extend-session option. Limit auto-save indefinite drafts; surface staleness ("Last edited 3 weeks ago").

**How to spot in review.** Any flow where time is meaningful — does the UI tell the user that? If not, behavior will drift toward indefinite postponement.

---

## 23. Peak-End Rule

**Definition.** People judge an experience largely on how they felt at its peak (most intense moment) and at its end, not on the sum or average of the experience. A flow with one delightful peak and a graceful end will be remembered as positive even if most of it was mundane.

**When it applies.** Onboarding completion, purchase confirmation, error recovery, checkout, support resolution, end-of-session screens, account closure.

**Violation pattern.** A great onboarding flow that ends with a flat "Done" screen. A purchase confirmation that simply lists order details with no acknowledgement of the milestone. An error recovery that returns the user to a blank slate with no resolution moment.

**Fix example.** Design the peak and end deliberately. Onboarding ends with a moment of accomplishment — animation, summary of what's now possible, single clear next action. Confirmation pages thank the user and confirm what just happened in human language. Error recovery includes a brief "Fixed. Here's where you were." moment.

**How to spot in review.** Walk through any flow end-to-end. What's the peak emotional moment? What's the last thing the user sees or feels? If either is flat, design it.

---

## 24. Postel's Law

**Definition.** Be conservative in what you do, be liberal in what you accept from others. In UX: be strict about what your system produces and outputs; be forgiving about what users input.

**When it applies.** Forms, search, command interfaces, date pickers, address fields, phone fields, payment fields.

**Violation pattern.** A phone field that rejects spaces, dashes, or parentheses. An email field that rejects valid edge-case addresses. A search that requires exact spelling. A date field that demands a specific format. A coupon code that's case-sensitive.

**Fix example.** Strip non-digit characters from phone input before validating. Accept any reasonable email format and normalize. Search uses fuzzy matching and corrects common typos. Date pickers accept multiple input formats and normalize. Coupon codes are case-insensitive and tolerate extra whitespace.

**How to spot in review.** Try entering the user-natural format for every field. Phone with spaces, date with slashes vs dashes, name with accents. If any rejects valid intent, it's violating Postel's Law.

---

## 25. Selective Attention

**Definition.** The brain filters perception, focusing on what seems relevant and ignoring the rest. Users will miss anything that doesn't match their current goal — including, often, the thing you most want them to see.

**When it applies.** Notifications, error messages, important state changes, banners, primary CTAs in busy contexts.

**Violation pattern.** Banner blindness — important notices placed in banner-shaped slots that users have trained themselves to ignore. Error messages styled to blend with the page. Critical state changes that don't visually demand attention. Multiple primary CTAs competing — none wins attention.

**Fix example.** Important messages: position in user's natural reading path, use motion sparingly to draw attention, contrast strongly against surroundings. Errors: inline at the field, in user language, with a fix. Critical state changes: animate the transition; static visual change is invisible to selective attention. One primary CTA per surface.

**How to spot in review.** Run a 5-second test: show the screen, hide it, ask what they saw. If they missed the thing you most wanted them to see, your visual hierarchy fails.

---

## 26. Serial Position Effect

**Definition.** Items at the beginning and end of a list are remembered best. Items in the middle are most likely to be forgotten. Primacy and recency dominate; the middle is the dead zone.

**When it applies.** Navigation, menus, settings, feature lists, onboarding sequences, marketing copy, anywhere order communicates priority.

**Violation pattern.** Critical navigation items buried in the middle of the menu. The most important feature listed third in a list of seven. Burying the call to action in the middle of marketing copy.

**Fix example.** Put the most important item first. Put the second-most-important item last. Use the middle for important-but-not-critical content. In navigation: home, then key task surfaces, with settings/profile at the far right. In a feature list: lead with the killer feature, end with the runner-up, middle for the rest.

**How to spot in review.** For any ordered list, ask: would a user, asked to recall this list later, remember the right things? If the most important item is in position 4 of 7, reorder.

---

## 27. Tesler's Law

**Definition.** Every application has an inherent amount of irreducible complexity. The only question is who bears it: the user, the developer, or the designer. Hiding complexity from one actor pushes it to another.

**When it applies.** Forms, configuration, edge cases, defaults, advanced features, integrations.

**Violation pattern.** Exposing all the underlying configuration complexity to the user, in the name of flexibility. The opposite: hiding so much complexity that users can't accomplish legitimate goals and feel boxed in.

**Fix example.** Take the complexity onto the designer's side. Smart defaults that handle 80% of cases. Progressive disclosure for the 20%. The complexity exists — the question is who pays the cognitive cost. Make the system pay it where possible.

**How to spot in review.** For every screen, ask: which choices does the user have to make that the system could have made for them? Defaulting reasonably is not removing flexibility — it's pricing the flexibility correctly.

---

## 28. Von Restorff Effect

**Definition.** When multiple similar objects are present, the one that differs from the rest is more likely to be remembered and noticed. Also called the "isolation effect."

**When it applies.** Pricing tiers (the "recommended" one), nav active states, primary CTAs in a row of secondaries, the featured item in a list, the new badge on a list item.

**Violation pattern.** All pricing tiers styled identically — none stands out. All buttons in a footer styled the same — no clear primary action. Featured content that doesn't visually differ from surrounding content. New-feature announcements buried among existing features.

**Fix example.** Make the recommended pricing tier visually distinct — different color border, "Most popular" tag, slight size increase. Primary CTA: solid filled in the brand accent; secondary: outlined; tertiary: text. The featured item gets a different background tint or border. New features get a clearly-styled "New" badge.

**How to spot in review.** In any set of similar items, is the priority item visually isolated from the rest? If not, the effect isn't being used.

---

## 29. Working Memory

**Definition.** The cognitive system that holds and manipulates information for current tasks. Limited to roughly four chunks for most adults, decaying rapidly without rehearsal. The bottleneck for every complex task.

**When it applies.** Multi-step flows, complex forms, comparison tasks, decision-making, data entry, configuration.

**Violation pattern.** A checkout flow that asks the user to remember a discount code from the cart screen. A comparison page that requires the user to remember features from page 1 to compare with page 2. A multi-step form that doesn't show what's been entered before.

**Fix example.** Show the discount code as applied, not as a number to remember. Comparison: show all options on one screen, no remembering required. Multi-step forms: a summary panel showing entered data; or, on the final step, a review screen with edit links for every prior step.

**How to spot in review.** For any flow, ask: what does the user need to hold in mind from one step to the next? Anything that fits in working memory will be forgotten. Externalize it onto the screen.

---

## 30. Zeigarnik Effect

**Definition.** People remember uncompleted or interrupted tasks better than completed ones. Open loops create cognitive tension that motivates closure.

**When it applies.** Onboarding completion percentages, profile completion bars, multi-step processes, saved-for-later items, draft states.

**Violation pattern.** No visible indicator of incomplete work. Once a user abandons a flow, they have no easy re-entry point. Drafts that don't surface themselves. Profile completeness that hides at 70%.

**Fix example.** Persistent "complete your profile (70%)" prompt with one click to the next step. Saved cart items surface on next visit. Drafts appear in a prominent "Continue where you left off" slot. Onboarding completion meter on the home screen until 100%.

**How to spot in review.** Are there incomplete states the user might forget about? Surface them. The user's mind wants to close the loop; help it find the loop.

---

## Using the laws in practice

These 30 laws are not equal. In any given review or generation pass, weight them by surface:

- **Transactional surfaces** (checkout, signup, payment) — Hick's Law, Fitts's Law, Postel's Law, Choice Overload, Jakob's Law, Doherty Threshold
- **Information-dense surfaces** (dashboards, reports, tables) — Miller's Law, Working Memory, Chunking, Cognitive Load, Common Region, Proximity
- **Persuasive surfaces** (pricing, landing pages, marketing) — Von Restorff Effect, Aesthetic-Usability Effect, Cognitive Bias, Serial Position Effect, Peak-End Rule
- **Onboarding and engagement** — Goal-Gradient Effect, Zeigarnik Effect, Paradox of the Active User, Peak-End Rule, Flow
- **System-level decisions** — Tesler's Law, Occam's Razor, Mental Model, Jakob's Law, Pareto Principle

When a screen feels wrong but the brief was met, run it against this list. One of the 30 laws is being violated. Find which, name it, fix it.

---

## Related references

- [Don Normans design principles applied](Don-Normans-design-principles-applied.md)
- [Krug 3 Laws of Usability with examples](Krug-3-Laws-of-Usability-with-examples.md)
- [The creative arsenal pattern library](The-creative-arsenal-pattern-library.md)
- [Anti-AI slop ban list](Anti-AI-slop-ban-list.md)

---

Repository: github.com/Laith0003/ux-skill | Maintainer: linkedin.com/in/laithaljunaidy
