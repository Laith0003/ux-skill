# Krug's 3 Laws of Usability — With Examples

Steve Krug's 3 Laws of Usability for the web: (1) Don't make me think. (2) It doesn't matter how many clicks as long as each is a mindless unambiguous choice. (3) Get rid of half the words on each page, then half of what's left.

These three laws govern web usability with more practical leverage than most multi-hundred-page UX frameworks. They are tactical, brutal, and they ship. This reference walks through each law in full, with violation patterns from contemporary product work and the specific fix that turns the screen around. It then covers the deeper Krug canon: how users actually use the web, the Billboard Test, page conventions, the home page's job, mobile usability, low-budget usability testing, common courtesy in failure, and accessibility as the default.

The single sentence that summarizes the entire body of Krug's work: **a user should never have to wonder what something is, what it does, or how to do the thing they came to do.** Any wondering is a usability tax. The job of design is to eliminate the tax.

---

## Krug's First Law — Don't Make Me Think

**The law.** A web page should be self-evident. Obvious. Self-explanatory. When the user looks at a page, they should not have to think about: what this is, how to use it, what's clickable, where the navigation went, what each thing means, or whether they're in the right place.

If they have to think — even for a second — to figure out one of these basic questions, the page is failing the first law.

This is the master law. The other two are corollaries.

**Why it matters.** Users don't read pages. They scan them. They don't carefully consider their options. They satisfice — pick the first option that looks reasonable. They don't figure out how a site works; they muddle through. Every time the design forces the user to stop and think, the user pays a cognitive tax — and the tax compounds across a session. By the third or fourth tax, the user leaves.

**The violation patterns:**

- **Mystery meat navigation.** Icon-only navigation where the icons aren't standard. The user has to hover each one to learn what it is. Cute, expensive, and a first-law violation.
- **Clever names for ordinary things.** "Solutions" instead of "products." "Resources" instead of "help." "Insights" instead of "blog." The user has to translate before they can navigate.
- **Unstable layout.** Navigation that moves between pages. The same button in different positions on different screens. The user has to relocate familiar controls every time.
- **Hidden interactivity.** Things that look like decoration but are actually clickable. Things that look clickable but aren't. The user has to test by clicking, which is a tax.
- **Unclear primary action.** Three buttons of equal weight on one screen. The user has to decide which one is primary. The decision is a tax.
- **Mid-page jargon.** Error messages that say "validation error" instead of "your phone number is missing the country code." The user has to interpret before they can act.

**The fix:**

- Use the words your users use. If they call it a "phone," call it a phone. Internal vocabulary stays internal.
- Use conventions. Search bar in the top right with a magnifying glass icon. Logo top-left links to home. Cart icon for cart. Don't invent.
- Visual hierarchy. The most important thing on the page is the most visually prominent. Secondary things are clearly secondary. Tertiary things are clearly tertiary.
- Clickability is obvious. Buttons look like buttons. Links look like links. Hover states confirm interactivity.
- One primary action per screen. Secondary actions visibly demoted.
- Page name visible. The user always knows what page they're on.

**Example pair:**

- Violation: A landing hero with a headline like "Reimagine What's Possible." The user has no idea what the product does.
- Fix: A landing hero with a headline like "Loyalty for cafes — points, tiers, vouchers, no app required." The user knows what the product does in under three seconds.

**How to test the first law.** Show the page to someone for 3-5 seconds. Hide it. Ask: what is this? What can you do here? What would you click first? If they cannot answer any of those three questions with confidence, the page is failing the first law.

---

## Krug's Second Law — It Doesn't Matter How Many Clicks, as Long as Each Is a Mindless, Unambiguous Choice

**The law.** Click count is not the measure. Click quality is. A user will happily click ten times if each click is a confident, unambiguous choice. A user will quit after two clicks if each one made them stop and wonder which option was right.

The cost of a click isn't time — it's cognitive load. A mindless click costs nothing. An ambiguous click costs a decision.

**Why it matters.** "Reduce clicks" is a common but wrong prescription. Cramming all options onto one page so the user can "click less" produces overwhelming pages where every option is ambiguous. The user does click less, but each click is taxed harder, and total task time goes up.

The right framing: think about cognitive friction, not interaction count. Reduce friction per click. The user's patience for unambiguous clicks is high.

**The violation patterns:**

- **Optimizing for click count.** Cramming the menu, the form, the configuration into one page because "fewer clicks." The page becomes a cognitive jungle.
- **Ambiguous next steps.** A screen with three buttons of similar weight where the user has to decide which path to take with no clear guidance.
- **Options that overlap.** "Sign up" and "Get started" and "Create account" on the same page. The user has to figure out if these are different or the same.
- **Disclosed at the wrong moment.** A pricing page that requires the user to enter their email before showing the price. The decision the user needs to make (is this worth the price?) is gated behind a different decision (should I give them my email?).
- **Inconsistent paths.** "Settings" reachable from the main menu in some screens, from a footer in others, from a hamburger in others. The user has to relearn every time.

**The fix:**

- Identify the user's actual path. Map every step they take to accomplish the most common task. The path may be longer than you think, and that's fine.
- Each step should have one obvious next action. Secondary actions are visibly secondary.
- Use breadcrumbs and progress indicators so the user always knows where they are in the path.
- Use clear, distinct labels. "Sign up" and "Log in" are distinct. "Get started" and "Begin" are not. Pick one.
- Disclose information at the moment it's useful. Show price before asking for email.

**Example pair:**

- Violation: A single-page "configurator" with 30 options visible at once. Three primary CTAs. The user has to make 30 decisions in parallel, then choose which CTA matches their intent.
- Fix: A 4-step wizard. Step 1 surfaces three clearly-distinct paths. Each step has 3-5 options. Each step has one primary CTA. The user makes simple decisions in sequence and reaches the right outcome in 4 confident clicks instead of 1 paralyzed click.

**How to test the second law.** Time a user through a common task. Note every place they pause, hover over multiple options, or click and backtrack. Each pause is an ambiguous click. The fix is not to remove the click — it's to remove the ambiguity.

---

## Krug's Third Law — Get Rid of Half the Words on Each Page, Then Get Rid of Half of What's Left

**The law.** Most product copy is too long. Cut half. Then cut half of what remains. The result is usually clearer, shorter, and more confident than what the writer started with — and the reader gets to the meaning faster.

This is hyperbole, of course. You won't literally cut 75% from every page. But starting with that as the target reveals how much filler is in writing that felt tight when it was first written.

**Why it matters.** Users scan. They don't read. Long copy isn't read more thoroughly; it's skipped over more aggressively. Every extra word reduces the odds that the essential words get attention.

Filler comes in patterns:

- **Throat-clearing introductions.** "Welcome to our platform. We're excited to have you here. Our mission is to..." The user came for a task; the introduction delays it.
- **Hedging.** "It may be helpful to consider that you could potentially..." Replace with: "Try..."
- **Restating the obvious.** "Please enter your email in the email field below." Replace with: "Email."
- **Defensive copy.** Explanations the user didn't ask for, included to avoid imagined complaints. Cut them.
- **Marketing-speak in product surfaces.** "Empower your business" instead of "Add a product." The product surface is not the landing page.
- **Apologies.** "Sorry, but..." Just state the fact.

**The fix:**

- Read every page out loud. Anything that doesn't earn its place gets cut.
- Convert paragraphs to bullets where the structure is genuinely list-shaped. Convert bullets to short headers where the user is scanning for one of several options.
- Use the active voice. "Your message was sent" becomes "Sent." "Your profile has been saved" becomes "Saved."
- Cut the filler verbs: "in order to" becomes "to." "due to the fact that" becomes "because." "at this point in time" becomes "now."
- Cut the throat-clearing: nobody scrolls down to the third sentence to find the real content.

**Example pair:**

- Violation: An error message that reads "We apologize, but it looks like there might have been an issue with processing your request at this time. Please try again later, and if the issue persists, feel free to contact our support team for further assistance."
- Fix: "Something broke. Try again, or contact support if it keeps happening."

The information is the same. The second version respects the reader's time, communicates the same intent, and feels human.

**How to test the third law.** Print the page. Read it aloud. Mark every sentence you read with a sigh. Cut the sighs. Repeat.

---

## How We Really Use the Web

Krug's deeper insight, underpinning all three laws: users don't behave the way designers imagine. The mental model in most designers' heads (the user considers each option carefully, weighs alternatives, reads the page) is wrong. The actual user behavior is:

**1. We don't read pages. We scan them.**

Users skim the page looking for trigger words — words that match what they came to do. They scan headlines, links, button labels, and short bursts of text. They mostly ignore paragraphs unless they have to read them.

Design implication: visual hierarchy is paramount. The trigger words for common tasks must be visible at scan speed. Hide them in a paragraph and they may as well not exist.

**2. We satisfice. We don't optimize.**

Users pick the first option that looks reasonable — not the best option. Once they find something that might work, they click it. If they're wrong, they backtrack. They don't compare all options.

Design implication: the first option matters disproportionately. If your most important link is listed sixth, most users will never see it. Order is hierarchy.

**3. We muddle through. We don't figure out how things work.**

Users don't read instructions. They guess at how the system works and learn by trying. They have no idea what most icons mean. They click around until something happens. If it's the wrong thing, they undo and try again.

Design implication: design for muddling. Make undo first-class. Make consequences reversible where possible. Use universally-understood icons; label everything else. Don't rely on the user to read help text.

---

## The Billboard Test (5-Second Scan)

**The test.** A web page should communicate its purpose, its primary action, and how to find what the user came for — all in the time it takes to glance at a billboard from a moving car. Five seconds.

If you stop at the home page for five seconds, can you answer:
1. What is this site?
2. What can I do here?
3. Why am I here (and not somewhere else)?
4. What should I click first?

If the answer to any of those is "I'm not sure," the page is failing the billboard test.

**How to run the test.** Show the page to someone who has never seen it. Hold for 5 seconds. Hide. Ask the four questions. Note what they got right, what they got wrong, what they couldn't answer.

**Common failures:**

- Vague headline that doesn't say what the product does ("Reimagining the future")
- Multiple primary CTAs of equal weight
- Hero image with no text explaining context
- Logo with no tagline
- Navigation labels that don't say what's behind them
- A featured product or article with no context

**Fix:**

- Headline says what the product does, plainly. Subhead adds the reason to care.
- One primary CTA, visually dominant.
- Tagline directly under the logo if the company name doesn't communicate the product.
- Navigation labels in user vocabulary.
- Above-the-fold content makes the value proposition obvious.

---

## Page Conventions and When to Break Them

Web conventions exist because they reduce cognitive load. The user has seen the magnifying glass for search a thousand times; using it costs them nothing. Invent a new icon and you've spent the user's attention on learning.

**The conventions that almost always hold:**

- Logo top-left, links to home
- Primary nav across the top (desktop) or hamburger (mobile)
- Search top-right with magnifying glass icon
- Cart top-right with cart icon (e-commerce)
- Sign in / Profile top-right
- Footer with secondary links and legal
- Breadcrumbs above page title for deep navigation
- "X" in top-right of modals for close
- Hamburger icon for menu on mobile
- Underlined or colored text for links in running copy
- Primary CTA bottom-right of forms, secondary CTA to its left

**When to break a convention.** Only when you have a strong reason and a clear signal that the user will discover the alternative. "We wanted to be different" is not a strong reason. "Our user research showed users couldn't find X in the conventional position" might be.

When you do break a convention, double down on signifiers. Hover states. Tooltips. Onboarding hints. The user will not figure out a non-conventional layout on their own.

**Example pair:**

- Violation: A site puts its search bar in the footer because the designer thought search "wasn't part of the brand story." Users who want to search bounce.
- Fix: Search bar top-right with magnifying glass. The brand story is told through content; the chrome is invisible.

---

## Street Signs and Breadcrumbs

Users get lost. The web is a maze of pages, and at any moment a user may need to answer: where am I? How did I get here? Where can I go next?

**Street signs:**

- Page title visible and clear (what page is this?)
- Section heading visible (what part of the site?)
- Logo / home link (how do I get back to home?)
- Navigation showing current location (which top-level section am I in?)

**Breadcrumbs:**

- "Home > Products > Laptops > MacBook Pro 14"
- Each crumb clickable, last crumb non-clickable (current page)
- Used in deep hierarchies (3+ levels)
- Not used as primary navigation; used as orientation

**Violation patterns:**

- Pages without titles
- Section headings styled identical to body text
- No clear current-location indicator in nav
- Breadcrumbs that lie (showing a path that wasn't actually taken)
- Breadcrumbs as the only way back up

**Fix:**

- Every page has a title in a clearly-headline style.
- Section headings have their own scale, distinct from body and from page titles.
- Active nav state has a clear visual difference (color, weight, underline, indicator bar).
- Breadcrumbs reflect IA structure, not browsing history.
- Browser back, breadcrumbs, and the site's own nav all work to move up the tree.

---

## The Big Bang Theory of Web Design — The Home Page's 4 Questions

The home page does a disproportionate share of the orienting work. In the first moments, the user is forming an answer to four questions. If the home page doesn't answer them, the user leaves.

**The four questions:**

1. **What is this?**
   Answer: a clear product name and a one-line description of what the product does. Not a slogan. A description.

2. **What can I do here?**
   Answer: visible primary actions. Sign up. Browse the catalog. Read the docs. Start the demo.

3. **What do they have?**
   Answer: a sense of the product's scope. Categories of features, types of content, kinds of services. The user wants to know if you have what they came for.

4. **Why should I be here? (Why not somewhere else?)**
   Answer: a value proposition that differentiates. Why this product over the alternatives. Specific, not generic.

**Violation patterns:**

- Vague hero copy that fails question 1
- Decorative hero that fails question 2
- No clear path to product breadth that fails question 3
- Generic value claims ("the best platform") that fail question 4

**Fix:**

- Hero: product name + 1-line description ("Loyalty for cafes — points, tiers, vouchers, no app required").
- Below hero: one primary CTA, one secondary CTA. The CTAs answer question 2.
- Below CTAs: a feature grid, a product gallery, or a use-case list that answers question 3.
- Throughout: specific differentiators (concrete capabilities, integrations, customer names) that answer question 4.

**Example.** A SaaS home page that scores well on all four questions in under five seconds: hero says "Schedule social media posts to 12 platforms from one calendar." CTA: "Try free for 14 days." Below: a screenshot of the calendar with examples of the supported platforms (Twitter, LinkedIn, Instagram, Facebook, Threads, Bluesky, etc.). Below that: testimonials from named companies.

---

## Mobile Web Usability

Mobile is not desktop in a narrower frame. Mobile has different constraints (touch targets, viewport, attention) and different contexts (on the go, one-handed, interrupted). Krug's laws apply equally on mobile but the violations are different.

**Mobile-specific concerns:**

- **Touch targets.** 44x44 minimum, 48x48 preferred. Anything smaller is unreliable.
- **Thumb reach.** Bottom of screen is easier to reach with thumbs than the top. Primary actions in the bottom-third where possible.
- **One-handed use.** Most mobile use is one-handed. Don't require two hands for common actions.
- **Tap targets adjacent.** Adjacent targets must have spacing. Two buttons sharing an edge are unreliable.
- **No hover.** All interactivity must be visible without hover. Tooltips that depend on hover don't work.
- **Viewport scale.** Set `viewport` meta tag. Don't disable zoom.
- **Forms.** Use mobile-native input types (`type="tel"`, `type="email"`) to trigger the right keyboard. Use `autocomplete` to surface saved data.

**Violation patterns:**

- Desktop site shrunk to mobile width with no rework
- Tap targets smaller than 44px
- Important actions at the top of screen (unreachable with thumb on large devices)
- Hover-only interactivity ported to mobile
- Forms without correct input types
- Modals that don't scale to mobile viewport
- Horizontal scrolling

**Fix:**

- Mobile-first design where possible. Constrain on small viewports, expand on large.
- All tap targets 44x44+ with 8px+ spacing.
- Primary actions reachable with thumb on the largest target devices.
- All interactivity signified without hover (visible affordances, persistent labels).
- Mobile-native form input types.
- Modal designs that use the full viewport on mobile (sheet UI, not centered modal).

---

## Usability Testing on a Budget — 5 Users Per Round

The Krug doctrine on testing: you don't need 50 users to find usability problems. You need 5. Run them. Find problems. Fix them. Test again with 5 more. Repeat.

**Why 5 users.** Diminishing returns. The first user finds many problems. The second finds many of the same plus new ones. By the fifth user, you've found ~80% of the most serious usability problems. The sixth user mostly confirms what you've already learned. More users = better statistical confidence but slower iteration.

**The testing protocol:**

1. **Pick a goal.** What flow are you testing? Be specific.
2. **Recruit 5 users.** They don't have to be perfect demographic matches. Available, willing humans who aren't on the team are fine.
3. **Run 1-hour sessions.** Half-hour at minimum.
4. **Use a script.** Same tasks for every user. Standard introduction.
5. **Watch, don't help.** Resist the urge to explain. If they get stuck, ask "what would you try next?"
6. **Take notes on what surprised you.** Where they hesitated. What they said out loud. What they clicked that you didn't expect.
7. **Debrief between sessions.** Note patterns across users.
8. **Fix the most serious problems.** Don't try to fix everything. Pick the 3-5 biggest issues. Ship the fixes. Test again.

**Violation patterns:**

- "We can't test until the design is done." Wrong. Test wireframes. Test prototypes. Test paper sketches.
- "We don't have time to test." Test once a sprint with 5 users. Two hours total. The cost of not testing is shipping the wrong thing.
- "Our users are too special to test with random users." Probably wrong. Most usability problems are universal — affordance, signifier, mapping, feedback. Specialist problems come up in specialist testing.
- "We tested with 5 users and they liked it." Wrong measure. Users always say they like it. Watch where they hesitated, where they did the wrong thing, where they had to ask. That's the data.

**Fix.** Adopt the 5-user protocol as a sprint ritual. Calendar two hours a week for testing. Iterate against findings. Compound over time.

---

## Common Courtesy — When Failures Happen, Fail Gracefully

Things break. Servers go down. Validations fail. The user clicks a stale link. Connections drop. The question is not whether failures will happen — it's how the system behaves when they do.

**Common courtesy in failure:**

- **Specific error messages.** Never "form contains errors." Always "Phone number is missing the country code. Add +962 for Jordan, +971 for UAE."
- **Recovery options.** Always offer a path forward. "Sign in again," "Retry," "Contact support," "Go back."
- **Preserve user data.** Form submission failed? Keep the entered data so the user doesn't re-type. Connection dropped during a long task? Save state and let them resume.
- **Acknowledge the cost.** A 404 page shouldn't just say "Not found." It should help the user find what they were looking for — search bar, popular pages, link back to home.
- **No blame on the user.** The user didn't fail; the system did. Phrase errors as system events, not user mistakes. "Couldn't reach the server" beats "You sent an invalid request."
- **Maintain trust.** When something goes wrong, the user is wondering if the system is broken or if they made a mistake. The error message must clarify which.

**Violation patterns:**

- Cryptic codes ("Error 0x80004005")
- Blaming the user ("Invalid input")
- Generic messages ("Something went wrong")
- Lost form data on failed submit
- 404 pages with no recovery path
- Errors with no recovery action

**Fix:**

- Error messages: specific, in user language, with the fix.
- Recovery action visible.
- Form state preserved across errors.
- 404 page is a navigation surface, not a dead end.

---

## Accessibility as Default

Accessibility is not a special-needs concern. It's a usability concern. Designs that work well for users with disabilities work better for all users. Designs that fail accessibility usually fail Krug's three laws too.

**The minimum:**

- **Color contrast.** WCAG AA: 4.5:1 for normal text, 3:1 for large text and UI components. Most accessibility failures are contrast failures.
- **Keyboard navigation.** Every interactive element reachable and operable via keyboard. Tab order logical. Focus indicators visible.
- **Screen reader support.** Semantic HTML (`<button>`, `<nav>`, `<main>`, etc.). Alt text on images. Form labels properly associated with inputs.
- **Touch target size.** 44x44 minimum.
- **Text scaling.** Layout doesn't break at 200% zoom.
- **No information by color alone.** Status indicated by color AND icon AND label.
- **Captions on video.** Transcripts where possible.

**Violation patterns:**

- Light grey text on white ("aesthetic minimalism" that fails contrast)
- Icon-only buttons with no accessible label
- Forms where the label and input aren't associated (clicking the label doesn't focus the input)
- Custom controls (carousels, modals, dropdowns) that don't work with keyboard
- Status communicated only by color (red = error, green = success)
- Click targets that fail size requirements

**Fix:**

- Run a contrast checker on every text/background combination. Fix anything below 4.5:1.
- Keyboard-test every screen. Tab through. Can you reach everything? Can you activate it?
- Use semantic HTML by default. `<button>` not `<div onclick>`. `<nav>` not `<div class="nav">`.
- Status: color + icon + label. Never color alone.
- Run a screen reader through critical flows. NVDA on Windows, VoiceOver on Mac, both free.

Accessibility done right is invisible. Done wrong, it excludes users and degrades the product for everyone else.

---

## Real Examples and Fixes

Five before/after pairs that show Krug's laws in action.

### Example 1: Cryptic Empty State

- **Before:** A new dashboard with no data shows the message "No data available."
- **After:** A new dashboard with no data shows: "Nothing here yet. Add your first product to see sales come through." With a single button: "Add product."

Krug's First Law: the user is told what's missing, why, and what to do.

### Example 2: Ambiguous Confirmation

- **Before:** "Are you sure?"
- **After:** "Delete this voucher? Customers who already received it can still redeem it." With buttons "Delete" and "Cancel."

Krug's First Law: the user knows what they're confirming and what the consequence is.

### Example 3: Bloated Form Copy

- **Before:** "Please enter your phone number in the field below, including the country code, and ensure that the format matches international standards."
- **After:** "Phone (with country code)."

Krug's Third Law: half the words, then half again. The essential information remains.

### Example 4: Mystery Meat Navigation

- **Before:** A row of icons — magnifying glass (search), house (home), cog (settings), envelope (messages), bell (notifications), person (profile). All identical size, no labels.
- **After:** Same icons, with labels on hover (desktop) and labels persistently visible on mobile.

Krug's First Law: the user doesn't have to think about what each icon means.

### Example 5: Hidden Primary Action

- **Before:** A checkout page with three buttons of equal weight: "Apply Coupon," "Continue," "Calculate Tax."
- **After:** "Continue" rendered as a solid filled primary button. "Apply Coupon" rendered as a text link. "Calculate Tax" automated, no button needed.

Krug's Second Law: the next action is unambiguous.

---

## Applying Krug in review

Run any screen through these checks:

**First Law — Don't Make Me Think**
- Can the user identify the page and its purpose in 3 seconds?
- Is every label in user language?
- Is the primary action visually dominant?
- Does every interactive element look interactive?

**Second Law — Mindless, Unambiguous Choices**
- At every decision point, is one path clearly the right one?
- Are competing actions visually differentiated?
- Are click paths consistent across screens?

**Third Law — Cut the Words**
- Read every line of copy aloud. Can each sentence be shorter?
- Are there any sentences that could be cut entirely without losing meaning?
- Is the active voice used?

These three checks compound. Apply them on every review and the design improves predictably.

---

## Related references

- [The 30 Laws of UX](The-30-Laws-of-UX.md)
- [Don Normans design principles applied](Don-Normans-design-principles-applied.md)
- [Anti-AI slop ban list](Anti-AI-slop-ban-list.md)
- [The creative arsenal pattern library](The-creative-arsenal-pattern-library.md)

---

Repository: github.com/Laith0003/ux-skill | Maintainer: linkedin.com/in/laithaljunaidy
