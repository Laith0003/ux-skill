# Krug's Web Usability Principles

A working reference for the laws of web usability. Use this when reviewing a page, debating a navigation tree, simplifying copy, or arguing about whether something needs another menu, another modal, or another five seconds of the user's attention.

## How to read this file

Each section is a self-contained law. We give you the definition, the cause of failure, when to apply it, the violation patterns that ship in most production work, and a list of moves to take in a review. Treat it as a checklist. Lay it over a page and ask: "Did we make the user think? If yes, where, and can we stop?"

The cost of every cognitive demand is paid by the user, in attention. Attention is finite. Spend it where it produces value.

---

## The First Law: Don't Make Me Think

### Definition

Every page, every label, every interaction should be self-evident. The user should not have to read a sentence and then construct an interpretation. They should not have to guess. They should not have to ask themselves, "What does this do? Where do I click? What is this site for?"

When self-evident is not achievable, the design should be self-explanatory: a brief glance answers the question. The user might pause for half a second, but they should not pause for two seconds and then have to read.

Anything that makes the user pause longer than that — a confusing label, a non-obvious interactive element, a mysterious icon — is a small tax. Each tax alone is fine. Pile them up and the user leaves.

### What causes thinking-friction

- Clever names. ("Adventures" instead of "Trips." "My Stuff" instead of "Account.")
- Marketing-induced names. ("Solutions Discovery Center" instead of "Products.")
- Unfamiliar icons without labels.
- Links that do not look like links. Buttons that do not look like buttons.
- Walls of text where the user has to read before knowing where to click.
- Forms that demand information without explaining why.
- Multi-step flows where the user cannot tell which step they are on.
- Two paths that lead to the same place and the user has to choose.
- Hidden state ("Are my filters still applied?").
- Inconsistent vocabulary across the same product ("Cart," "Bag," "Basket" on the same site).

### How to eliminate it

- Use names users already know. "Sign in." "Search." "Buy."
- Pair icons with labels until you have evidence the icon alone is universally understood. Pair them anyway for any action that matters.
- Make links visibly different. Make buttons visibly like buttons. Make headings clearly hierarchical.
- Cut filler text. Replace prose with form fields, buttons, and headings the user can scan.
- For every required input, write a sentence in your head: "The user wants to do X. Why do we need this field?" If the answer is wobbly, the field is wrong.
- Show progress and state explicitly. "Step 2 of 4." "3 filters applied."

### Violation pattern

- A nav item labeled "Discover" that goes to a page of mixed editorial content and product recommendations. The user does not know if they should click it.
- A submit button labeled "Continue" that completes a purchase. The user clicked through expecting another confirmation step.
- An icon (e.g., a gear) that means "settings" on one page and "filters" on another in the same product.
- A primary CTA hidden among five tertiary buttons of the same visual weight.

### Fix example

```html
<!-- Bad: ambiguous, requires interpretation -->
<a href="/discover">Adventures</a>

<!-- Good: tells the user what they will see -->
<a href="/trips">Trip planning</a>
```

For destructive or irreversible actions, name the action specifically. Not "Continue" but "Place order." Not "OK" but "Delete account."

### How to spot it in review

- Walk through the page as a first-time user. Where do you pause? Where do you have to guess? That is friction.
- Read every label and ask, "Does the user have to interpret this?" If yes, rename.
- Cover the icons. Can you still navigate?

---

## The Second Law: The Number of Clicks Is Less Important Than the Quality of Each Click

### Definition

It does not matter how many clicks a task takes, as long as every click is a mindless, unambiguous choice. Users will happily click eight times through clear choices. They will resent two clicks if each one requires thought.

The cost of a task is not the number of steps. It is the cognitive load summed across the steps. A wizard with seven obvious steps beats a single screen with seven decisions clustered together.

### When it applies

- Wizards and multi-step flows.
- Settings hierarchies.
- Form flows for complex inputs (signups, checkouts, configuration).
- Any time a stakeholder demands "fewer clicks" without justifying why.

### How to apply it

- Optimize each click for clarity, not for click-count reduction.
- Sequence steps so each step has one decision.
- If a step has more than one decision, split it.
- Save aggressively; the user should never lose progress by going back a step.
- Show the path: "Step 2 of 4: Address." The user knows where they are and what is left.

### Violation pattern

- A "single-page" checkout that demands shipping, billing, payment, and review in one massive screen. Looks like one click; feels like ten.
- A wizard that hides progress, so the user cannot tell how many more steps remain.
- A wizard that loses data when the user clicks back.

### Fix example

A 4-step checkout where each step has one focus: address, delivery, payment, review. Each transition is one click. At any point, the user can see "Step 2 of 4" and click back without losing data.

### How to spot it in review

- Time the task and count the decisions, not the clicks. Each decision is a moment of thinking-friction.
- Look at steps where multiple types of input live together. Split them.

---

## The Third Law: Get Rid of Half the Words on Each Page. Then Get Rid of Half of What's Left.

### Definition

Every word on a page is a tax on the user's attention. Most pages have at least twice as many words as they need. Trim aggressively until what remains is what users need to act.

This is not about losing meaning. It is about removing prose that explains things the design should already explain.

### When it applies

- Marketing pages. Landing pages. Onboarding. Empty states. Form help text. Error messages. Documentation index pages.

### How to apply it

- Replace prose with headings, lists, and labels the user can scan.
- Cut marketing language ("comprehensive," "powerful," "innovative," "industry-leading"). Replace with concrete claims.
- Cut throat-clearing ("Welcome! We're so excited to have you here. Let's get started by...").
- Cut redundant micro-instructions. If the button says "Save," do not also say "Click this button to save your work."
- For every paragraph, ask: "If this were gone, what would the user not know?" If the answer is "nothing important," cut it.

### Violation pattern

- A page that opens with two paragraphs of brand voice before any actionable content.
- A form where each field has a help string longer than the field label.
- An error message that explains the system's internal state in three sentences instead of telling the user what to do.
- Documentation that explains what the page is about in 200 words at the top before listing the topics.

### Fix example

Before:
> Welcome to your dashboard! This is the place where you can see all your important information at a glance. Below, you'll find a summary of your recent activity, alerts, and notifications. To get started, simply click on one of the cards.

After:
> Recent activity

That is the page. The cards below speak for themselves.

For an error:

Before:
> An error occurred while processing your request. The server returned an unexpected response. Please try again or contact support if the problem persists.

After:
> We could not save your changes. Check your connection and try again.

### How to spot it in review

- Read every paragraph aloud. If your tongue rolls past words without their absence changing the meaning, cut them.
- Look for adjectives. Most of them are puffery. Keep only the ones that carry specific meaning.
- Look at instruction text below a control. If the control's label and behavior are clear, the instruction is noise.

---

## How Users Really Use the Web

### Scanning, not reading

Users do not read pages. They scan them, looking for words that match their goal. They see headings, links, and visually distinct elements first. Body copy is mostly ignored until something signals "this is relevant."

Design for scanning:

- Strong heading hierarchy. The user can read only the headings and get the page.
- Distinct, descriptive link text. Not "click here" but "Pricing details."
- Front-loaded copy. Put the keyword and the conclusion in the first words.
- Bullet lists for parallel content.
- Visual weight matches importance. Bigger and bolder for what matters most.

### Satisficing, not optimizing

Users do not pick the best option. They pick the first reasonable option. If "Trip planning" is at the top of the nav and the user thinks it might lead to a trip planner, they click. They will not scroll the full nav to find "Trip optimizer," even if it is the better label.

Design for satisficing:

- Put the most likely match first.
- Make every reasonable label clearly distinct, so satisficing leads to the right place.
- Tolerate near-misses. If the user lands on the wrong page, give them a clear way to find the right one.

### Muddling through

Users do not figure out the system. They muddle through. They click things and see what happens. They are not building a mental model; they are looking for the next action.

Design for muddling:

- Make state visible at every step.
- Make the next action obvious.
- Tolerate wrong actions; offer undo and easy recovery.
- Do not assume the user knows what the previous step did.

### Violation pattern

- Long-form copy on a marketing page where the value prop is buried in paragraph three.
- Generic link text ("learn more," "click here," "read more") that gives the scanner no signal.
- A landing page where the primary CTA is below a fold the user does not reach.
- A complex flow that demands the user understand the entire flow before starting.

### Fix example

A landing page with three components above the fold: a heading that names the value, a sentence that explains the value, and a CTA. Everything below is for users who want more.

```html
<h1>Track your team's time without the meetings.</h1>
<p>One-click time tracking. Reports your team won't fake. No standups.</p>
<button>Start free trial</button>
```

A scanner gets the value in two seconds. A reader gets more if they scroll.

### How to spot violations in review

- Squint at the page. Can you tell what it is for from the shapes and headings alone?
- Read only the headings and links. Do you understand the page?
- Time how long it takes to see the primary action. Anything over five seconds is a problem.

---

## The Billboard Test

### Definition

A user should look at any page and, in five seconds — at highway speed, with one glance — be able to answer two questions: "What is this page?" and "What can I do on it?"

The billboard test is a thought experiment. Imagine your page on a billboard at the side of the road. A driver gets three seconds of glance time. Can they identify what is being advertised?

If not, the page is too cluttered, too generic, too cute, or too prose-heavy.

### When it applies

- Every page, especially landing pages, home pages, dashboards, and category pages.

### How to apply it

- A primary heading that names the page.
- A primary action that is the largest interactive element.
- Visual hierarchy that puts essential content above secondary content.
- Strip away anything that does not contribute to the two questions.

### Violation pattern

- Hero sections with five carousels and seven CTAs of equal weight.
- Dashboards where every metric is the same size and the user cannot tell what to look at first.
- A category page where the "category title" is smaller than the breadcrumb.

### Fix example

For a SaaS landing page:

- Heading: name the value in one line.
- Subheading: name the audience or use case in one line.
- Primary CTA: large, visually distinct, named for the action.
- Below: secondary content the user can find if they want.

For a dashboard:

- The most-needed metric, biggest. Other metrics, smaller. Drill-down on click.

### How to spot it in review

- Show the page to someone for five seconds. Take it away. Ask: "What is this page? What can you do on it?" If they cannot answer, the page fails the billboard test.

---

## Page Design Conventions and When to Deviate

### Definition

Users have learned conventions from years of using the web. They expect:

- Logo top-left links home.
- Search top-right.
- Account top-right.
- Navigation horizontal at the top, or vertical on the left.
- Footer at the bottom with secondary links.
- Underlined or otherwise visually distinct links.
- A shopping cart icon on the top right for e-commerce.
- Forms top-to-bottom, label-then-field.

Conventions are not laws. But every deviation costs the user a moment of thinking-friction.

### When to follow them

By default, follow conventions. The benefit of being unique is rarely worth the cost of being confusing.

### When to deviate

- When you have a measurable, tested reason. Not "we want to stand out." A specific user need that conventions do not solve.
- When your audience is so specific that the convention does not apply (e.g., interfaces for power users who use the product daily).
- When a new convention is clearly winning across multiple major products.

### Violation pattern

- Logo top-right because "the designer likes asymmetry." Users do not find it.
- Hamburger menu on desktop where horizontal nav fits easily. Users do not discover items hidden behind it.
- Search hidden in a settings menu instead of in the header.
- Cart in a non-standard location, costing the e-commerce site conversions.

### Fix example

Use the conventions. Save the design budget for the parts of the product where the convention does not exist — your specific product features, your novel interactions, your unique value.

### How to spot violations in review

- Check standard placements: logo, nav, search, account, cart, footer. Are they where users expect?
- For every deviation, ask: "What is the user benefit, and what is the cost?"

---

## Street Signs and Breadcrumbs

### Definition

Users need to know, at every moment, where they are in the site. Without orientation cues, they lose track and bail.

Orientation cues are the "street signs" of a site:

- The site name and logo, top-left, on every page.
- A persistent navigation that highlights the current section.
- A page title that names the page.
- Breadcrumbs that show the path from home to here.
- The URL, which power users use as a fallback.

### When it applies

- Every page below the home page.
- Especially sites with hierarchy: e-commerce, documentation, blogs, catalogs.

### How to apply it

- Highlight the current section in the nav. Users glance at the nav to confirm location.
- Title every page in the page itself (not just in the browser tab).
- Use breadcrumbs for sites three or more levels deep. Make them clickable.
- Keep URLs human-readable.

### Violation pattern

- A page deep in a hierarchy with no breadcrumbs and no nav highlight. The user has no idea where they are.
- A page title that says "Page" or repeats the site name. No information about this specific page.
- Breadcrumbs that are not clickable. Visual orientation only, no navigation use.

### Fix example

```
Home > Trips > Mediterranean > Greece > Athens 3-day itinerary
```

Each segment is clickable. The user can jump back to any level. The current segment ("Athens 3-day itinerary") is the page title, not a link.

### How to spot it in review

- Land on any page in the site. Within two seconds, can the user say where they are?
- Are breadcrumbs present and clickable on deep pages?
- Does the nav indicate the current section?

---

## The Big Bang Theory of Web Design (the Home Page Test)

### Definition

A home page's first job is to answer four questions:

1. **What is this site?** What is its name and its category?
2. **What can I do here?** What are the main actions?
3. **What do they have?** What is the content or product?
4. **Why should I be here?** Why this site and not a competitor?

A user landing on the home page should be able to answer all four questions in seconds, without scrolling and without reading prose.

### When it applies

- Home pages.
- Landing pages from external traffic.
- Marketing pages.
- App splash and first-run screens.

### How to apply it

- A heading that names the value or the product category.
- A subheading that explains who it is for.
- Visible navigation that names the main actions.
- A primary CTA that names the first thing to do.
- Secondary content that hints at the breadth of the offering.

### Violation pattern

- A home page that opens with a video and no text. The user must wait to see the heading.
- A heading that uses brand voice but does not say what the product is. ("Reimagine your day." — what is this?)
- No clear navigation. The user cannot tell what else exists.
- A primary CTA labeled "Get started" with no context. Started doing what?

### Fix example

Heading: "Track your team's time without the meetings."
Subheading: "One-click time tracking for distributed teams."
Nav: Features. Pricing. Customers. Docs.
CTA: "Start free trial."

In five seconds, the user knows the product, the audience, the navigation, and the first action.

### How to spot it in review

- Show the home page to a stranger. After three seconds, ask the four questions. If they cannot answer all four, the home page fails.

---

## Mobile Web Usability

### Definition

Mobile imposes constraints the desktop does not:

- Smaller screen. Less visible at once.
- Touch input. Larger targets, no hover, fat-finger errors.
- Slower connections, often. Larger pages take longer.
- Distracted users. Often glancing, often interrupted.
- Vertical orientation by default.

A mobile page that ports a desktop page directly will fail. Mobile design demands prioritization, simplification, and a different visual hierarchy.

### How to apply it

- One column. No multi-column layouts that demand horizontal scroll.
- One primary action per screen. A user should know what the main thing to do is.
- Large, finger-sized targets. Minimum touch target is generally accepted at 44 by 44 CSS pixels.
- Sticky access to critical actions (search, back, primary CTA).
- Cut secondary content. What was nice-to-have on desktop is dead weight on mobile.
- Avoid hover-only interactions. They do not exist on touch.
- Avoid modal stacks. A modal over a modal is a desktop pattern; on mobile, it is a trap.
- Forms: large fields, autocomplete, mobile keyboards (use `inputmode`).
- Test on actual devices, not browser emulators.

### Violation pattern

- A desktop nav crammed into a hamburger with no labels for the icons inside.
- A pricing table with five columns shrunk to fit. The text is unreadable.
- Tiny targets next to each other, prone to mis-taps.
- Forms with desktop-sized inputs and no `inputmode` so the user gets a generic keyboard for a phone-number field.

### Fix example

For a mobile e-commerce product page:

- Single column.
- Product image full width at top.
- Title and price below.
- Add-to-cart as a sticky button at the bottom of the screen.
- Description, reviews, and recommendations below the fold.

For form inputs:

```html
<input type="tel" inputmode="numeric" name="phone">
<input type="email" inputmode="email" name="email">
<input type="text" inputmode="decimal" name="amount">
```

### How to spot violations in review

- Open the site on a real phone. Try every action with a thumb.
- Look for any text smaller than 16px or any touch target smaller than 44px.
- Look for hover behaviors that are not also tap-accessible.

---

## Usability Testing on a Budget

### Definition

Usability testing does not require a lab, a research panel, or six-week studies. Frequent, cheap tests with three to five users catch the majority of issues. The cost of one professional study is the cost of twenty informal ones; the informal ones catch more, because you can iterate between them.

### How to do it

- Recruit five users per round. Friends, colleagues from other teams, contractors, your audience by intercept.
- Define one or two tasks. ("Find a product you would buy. Add it to the cart. Check out.")
- Watch them attempt the task without help.
- Note where they get stuck, what they say aloud, what they expected versus what happened.
- Iterate before the next round.

### When it applies

- Any time you have a design more concrete than a sketch.
- Especially before code is shipped.

### Violation pattern

- Skipping testing because "we know our users."
- Testing with internal users who already know the product.
- Testing late, after the design is locked in and feedback is expensive to act on.
- Asking testers questions instead of giving them tasks. ("Do you like this?" is useless. "Show me how you would book a trip" is gold.)

### Fix example

A tester is asked: "Imagine you want to buy running shoes. Show me how you would do it on this site." Watch. Do not prompt. Do not explain. Note every pause, every wrong click, every backtrack.

After five testers, you will see the same three problems. Fix them. Test again.

### How to spot violations in review

- Has this design been tested? If not, why is it being shipped?
- Were the testers representative? If everyone was internal, the test does not count.
- What was learned? What was changed?

---

## Common Courtesy (Failing Gracefully)

### Definition

When the system fails, the user should not be punished. They should be told what happened, told what to do, and given a path back to where they were going.

Common courtesy is the difference between a frustrating error and a forgivable one.

### When it applies

- 404s, 500s, network errors, validation errors, denied actions, expired sessions, rate limits.

### How to apply it

- Tell the user what failed. In plain language. Near the source.
- Tell the user what to do. A retry button. A way to contact support. A link to the closest available page.
- Avoid blaming the user. Avoid blaming the system in a way that sounds like blame ("Your request could not be processed").
- Avoid jargon. No HTTP status codes in the user-facing message. No "ECONNRESET." No "unexpected state."
- Preserve work. Do not lose what the user typed. Do not log them out unless required.
- Match the tone of the rest of the product. Errors should not feel like a different system wrote them.

### Violation pattern

- A 404 that says "Page not found" with no further help. The user has no idea what to do next.
- An error message at the top of a form that says "form contains errors." Which field? What error?
- A timeout that says "An unexpected error has occurred. Please try again." What error? Try what again? Will I lose my work?
- Validation that strips all the user's input on submit failure. They retype it and try again.

### Fix example

For a 404:

> We can't find that page.
> Maybe it was moved or deleted.
> Try the home page or search for what you need.

For a form validation:

```html
<!-- Bad: generic, away from the source -->
<div class="error">Form contains errors.</div>

<!-- Good: specific, at the source, actionable -->
<div class="field">
  <label for="phone">Phone</label>
  <input id="phone" type="tel" name="phone" value="555-12">
  <div class="field-error">
    This number is too short. Phone numbers must be at least 10 digits.
  </div>
</div>
```

For a system error during save:

> We couldn't save your changes.
> Your text is still here on the screen.
> Check your connection and try again, or copy your text to a safe place.

### How to spot it in review

- Trigger every error path. Read every error message. Is the user told what failed and what to do?
- Trigger a network failure. Does the system handle it gracefully or crash?
- Trigger a validation error. Is it near the field? Does it say what is wrong and what to fix?

---

## Accessibility Is the Default

### Definition

Accessibility is not a feature. It is not an add-on. It is not a checklist a team runs at the end of the project. It is the baseline state of a usable web page.

A page that is not accessible is a page that excludes users. The exclusion is rarely intentional, but the cost is real.

Accessibility includes:

- Visible focus states for keyboard users.
- Sufficient color contrast for users with low vision.
- Semantic HTML so screen readers can understand structure.
- Alt text on meaningful images.
- Labels associated with form fields.
- Captions on video, transcripts on audio.
- Targets large enough for users with motor impairments.
- Animation users can pause or disable.
- Time limits users can extend.

### When it applies

- Every page. Every component. Every release.

### How to apply it

- Use semantic HTML by default. `<button>`, `<a>`, `<input>`, `<label>`, `<nav>`, `<main>`, `<section>`.
- Test keyboard navigation. Tab through every interactive element. Can you reach everything? Can you tell where you are?
- Run an accessibility scanner (axe, Lighthouse) on every page. Treat findings as bugs.
- Test with a screen reader at least once per major flow.
- Verify contrast for every text on every background. Use a contrast checker.

### Violation pattern

- Buttons made of `<div>` with click handlers. Invisible to assistive technology.
- Form inputs without labels, just placeholder text. Screen readers do not announce them.
- Custom focus styles that look prettier but are less visible than the default.
- Color as the only signal of state. Color-blind users cannot perceive it.
- Hover-only interactions, with no keyboard or touch equivalent.

### Fix example

```html
<!-- Bad: not a button, not focusable, no label, no role -->
<div class="btn" onclick="submit()">Submit</div>

<!-- Good: real button, keyboard-accessible, semantically labeled -->
<button type="submit">Submit</button>
```

```html
<!-- Bad: placeholder used as label -->
<input type="text" placeholder="Email">

<!-- Good: associated label, still visually present -->
<label for="email">Email</label>
<input id="email" type="email" name="email">
```

### How to spot it in review

- Tab through the page. Can you reach every interactive element? Is focus visible?
- Run Lighthouse or axe. Treat every finding as a bug to fix.
- Spot-check contrast. Every text on every background.
- Spot-check with a screen reader for one critical flow.

---

## Design review checklist

Use this for every web page or screen.

### Thinking-friction
- Walk the page. Where did you pause? Why?
- Read every label. Are any of them clever, marketing-induced, or unfamiliar?
- Cover the icons. Can you still navigate?

### Clicks
- For multi-step flows: is every step a single mindless decision?
- Is progress visible? "Step 2 of 4"?
- Does going back lose progress?

### Words
- Read the page aloud. Where can you cut without losing meaning?
- Are there adjectives doing no work?
- Are there micro-instructions repeating what the labels already say?

### Scanning
- Squint. Can you tell what the page is?
- Read only headings and links. Does the page communicate its purpose?
- Time to first action. Under five seconds?

### Billboard test
- Show the page for five seconds. Ask: "What is this? What can you do here?" Does the user answer correctly?

### Conventions
- Logo top-left? Search top-right? Nav clearly marked? Account where users expect?
- Deviations: are they justified?

### Orientation
- Page title in the page?
- Current section highlighted in nav?
- Breadcrumbs present for deep pages? Clickable?

### Home page test
- Can a stranger answer the four questions (what is it, what can I do, what do they have, why should I be here) in three seconds?

### Mobile
- Tested on a real phone with a thumb?
- One column? Primary action obvious?
- Targets at least 44 by 44? Text at least 16px?

### Testing
- Has this been tested with real users?
- Were they representative?
- What was learned and changed?

### Failing gracefully
- Every error message: names the failure, names the fix?
- Every form validation: at the source, specific to the field?
- Network failures handled, data preserved?

### Accessibility
- Tab through the page. Can you reach everything? Is focus visible?
- Lighthouse or axe clean?
- Contrast verified for all text?
- Screen-reader spot-check on critical flow?

A page that fails three or more of these is not ready to ship.
