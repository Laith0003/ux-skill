# The 6 Audit Lenses

The `/ux-audit` command walks every surface through six lenses: FRAME, DISCOVER, SCAN, ACT, READ, RECOVER. Each lens is grounded in a specific reference — Lean UX, Norman, Krug, Laws of UX, microcopy rubric, error design + WCAG. The lenses are not categories. They are sequential interrogations: each one builds on the previous, and together they cover the full arc from "should this exist" to "does it fail well."

This page is the reference for what each lens checks, how findings are produced, and how the lenses interact. Read it before running `/ux-audit` on a serious surface — the audit is only as good as your understanding of what it's measuring.

---

## Why six lenses, not one checklist

A flat checklist treats every issue as equal. It is not. A surface can pass forty visual-polish checks and still be unusable, because the foundational question — what is this for, and who is it for — was never answered. A surface can have perfect microcopy and still confuse a first-timer because the affordances are invisible. A surface can be perfectly accessible at the WCAG level and still hide its primary action.

The six lenses are ordered by what fails first. If FRAME is wrong, nothing downstream matters. If DISCOVER is broken, scan-readability is irrelevant. If SCAN fails, action-loop integrity will not save it. The lenses are a triage order, not a coverage matrix.

You run them in order. You stop reporting downstream lenses only when an upstream lens is so broken that fixing downstream would be wasted work — but you do not skip them. The audit always names every lens, even if a lens is "Pass" with no findings.

---

## Lens 1: FRAME — Lean UX

**Question**: Who is this for, what outcome are they trying to reach, and what hypothesis does this design test?

FRAME is the first lens because every other lens depends on knowing the target. You cannot evaluate cognitive load without knowing who the user is. You cannot evaluate scan-readability without knowing what they are scanning for. You cannot evaluate error recovery without knowing what they are trying to do.

### What FRAME asks

- **Audience**: Is the primary user explicit? Is there a single primary user, or is the surface trying to serve multiple primary users at once (almost always a mistake)?
- **Outcome**: Is the user's desired outcome explicit? Not "engage with the platform" — what specific thing do they want to accomplish?
- **Hypothesis**: What does this design assume about user behavior? Is the assumption testable? Is there evidence the assumption holds?
- **Scope**: Is the surface trying to do one job well, or several jobs poorly?

### How to read existing framing

If you are auditing a live surface, framing is rarely written down. You infer it from the surface itself: who is the headline talking to, who is the primary CTA designed for, what does the page demonstrate the user can do? If those three don't agree, the surface has a framing problem before anything else.

Inferred framing is a finding. If you cannot tell from looking at the surface who it is for or what it wants the user to do, that is a Critical FRAME finding even if every other lens passes.

### Anti-patterns in FRAME

- **Audience drift**: The headline talks to engineers, the CTA is designed for executives, the demo content shows consumer users. Three primary users in one surface.
- **Outcome ambiguity**: The page demonstrates ten features and never says what problem any of them solves. The user has to assemble the framing.
- **Untested hypothesis**: The whole surface is built around an assumption that has not been validated with even five user conversations.
- **Scope sprawl**: A landing page that tries to be a feature tour, a documentation portal, a pricing page, and a signup flow simultaneously.
- **Self-referential framing**: "We are a company that does X" instead of "If you have problem Y, here is how X solves it." The framing is about the company, not the user.

### When FRAME passes

FRAME passes when:

1. A first-time viewer can articulate in one sentence who the surface is for.
2. A first-time viewer can articulate in one sentence what outcome the surface helps the user reach.
3. The primary CTA, the primary headline, and the primary visual all serve the same outcome for the same audience.
4. The hypothesis the design tests is at least implicit (e.g., "we believe loyalty managers will sign up for a phone-based wallet if they see it works with their POS in 60 seconds").

### Severity defaults for FRAME

- **Critical**: No identifiable primary user OR no identifiable primary outcome.
- **High**: Audience drift across major elements (headline vs CTA vs demo).
- **Medium**: Outcome is implicit and requires more than 5 seconds of inference.
- **Cosmetic**: Outcome is clear but framing copy is dry/uncompelling.

---

## Lens 2: DISCOVER — Norman

**Question**: Can a first-timer figure out what to do, where they are, and what is possible?

DISCOVER applies Norman's gulfs of execution and evaluation. The gulf of execution is the distance between what the user wants to do and what the system lets them do. The gulf of evaluation is the distance between what the system did and what the user can perceive about that.

A surface bridges both gulfs through three Norman concepts: **affordances**, **signifiers**, and **feedback**.

### Affordances

An affordance is what an object lets you do. A button affords pressing. A link affords following. A handle affords pulling. Affordances are properties of the object, not signals about it.

DISCOVER checks: do interactive elements have the affordances they should? A button-shaped div that is not clickable has the wrong affordance. A clickable area styled like static text has no affordance.

### Signifiers

A signifier is the visible signal that an affordance exists. Underlined text signifies a link. A shadow signifies clickability. A hover state signifies interactivity. Signifiers are how the user perceives the affordance.

DISCOVER checks: are signifiers present for every interactive element, and absent for non-interactive ones? Non-interactive elements that look interactive (cards that are not clickable) are as bad as interactive elements that don't look it.

### Feedback

Feedback is the system's response to user action. A button press should look pressed. A form submit should show progress. A delete should show what was deleted and offer undo.

DISCOVER checks: does every action produce immediate, perceivable feedback? Silent actions break the action loop and force the user to guess.

### The gulf of execution

The user wants to do X. They look at the surface. Can they find the control that does X? Is the control labeled in a way they will recognize? Is the control where they expect it to be?

DISCOVER walks this for the top three user actions on the surface. For each:

1. What is the action the user wants to take?
2. What control performs that action?
3. Is the control visible without scrolling, hovering, or searching?
4. Is the control labeled in the user's language (not the system's language)?
5. Is the control where Jakob's-Law-trained users expect it to be?

If any answer is "no," there is a gulf of execution finding.

### The gulf of evaluation

The user performed an action. Can they tell what happened? Can they tell if it succeeded? Can they tell what state the system is in now?

DISCOVER walks this for the same top three actions. For each:

1. After the action, what changes on the surface?
2. Is the change perceivable (not just a state change in the URL)?
3. Is the change interpretable (the user knows what it means)?
4. If the action could have failed, does success vs failure look different?

If any answer is "no," there is a gulf of evaluation finding.

### Anti-patterns in DISCOVER

- **Mystery meat navigation**: Icons with no labels, requiring hover to discover what they do.
- **Phantom affordances**: Cards or rows that look clickable but are not, or vice versa.
- **Silent submission**: Form submits with no visible feedback for >300ms.
- **State changes in the URL only**: Tab changes, filter changes, or step advances that don't update visible chrome.
- **Hidden primary actions**: The primary CTA is below the fold or obscured by overlapping elements on common viewport sizes.
- **Iconography without grounding**: Custom icons that don't follow Jakob's Law expectations (a custom "trash" icon that doesn't look like a trash can).

### When DISCOVER passes

DISCOVER passes when:

1. The top three user actions are visible, signified, and labeled in user language above the fold on a common viewport.
2. Every interactive element has a visible signifier (cursor change, hover state, or styling treatment).
3. Every action produces feedback within 300ms.
4. The current state of the surface (which tab, which filter, which step) is perceivable from chrome alone, not just from URL.

### Severity defaults for DISCOVER

- **Critical**: Primary CTA is hidden, mislabeled, or has no signifier.
- **High**: Top 3 actions cannot be discovered in 5 seconds by a first-timer; OR major affordance mismatches.
- **Medium**: Secondary actions have weak signifiers; feedback delays under 1s.
- **Cosmetic**: Hover states could be more distinct; cursor changes inconsistent.

---

## Lens 3: SCAN — Krug

**Question**: In 5 seconds, what does a user understand about this page?

SCAN applies Krug's "Don't Make Me Think" and the 5-second billboard test. People do not read pages. They scan. The surface must communicate its purpose, identity, and primary action in the time it takes to read a billboard at 60 miles per hour.

### The 5-second test

You show the surface to a user for exactly 5 seconds. Then you ask:

1. What is this page about?
2. Who is it for?
3. What can you do here?
4. What was the most prominent thing?

If the answers do not match the framing the surface intended, SCAN failed.

### What SCAN measures

- **Visual hierarchy**: Is there a clear primary element, secondary elements, tertiary elements? Or is everything competing for attention?
- **Scan-not-read structure**: Are headings, bullets, and short paragraphs used? Or are there walls of text?
- **F-pattern compatibility**: Does the layout work with how Western users scan (left-to-right, top-to-bottom, F-shape)?
- **Information density**: Is the surface trying to communicate too much in the first viewport?
- **The 5-second billboard**: If the user only saw the top 600 pixels, could they answer "what is this and what can I do?"

### Scan-not-read patterns

Krug's principles for scannability:

- **Clear visual hierarchy**: Bigger, bolder, higher = more important.
- **Conventions over novelty**: Users have learned where to look for what. Don't fight learned patterns.
- **Pages divided into clear areas**: White space, dividers, color blocks that group related content.
- **Obvious clickability**: Buttons look like buttons, links look like links, no guessing.
- **Reduced noise**: Every element earns its place. Decoration without purpose is noise.

### Anti-patterns in SCAN

- **Equal weight**: Every section is the same size, same emphasis. No primary, no secondary.
- **Wall of text**: Paragraphs longer than 4 lines without subheadings or breaks.
- **Decoration drift**: Background patterns, illustrations, animations that compete with content for attention.
- **Hero overload**: Hero section trying to be a tagline + value prop + features + social proof + CTA simultaneously.
- **Below-fold burial**: The actual purpose of the page is revealed below the fold; above the fold is brand and decoration.
- **Layout instability**: Elements shift as the page loads, so the user cannot trust what they're scanning.

### When SCAN passes

SCAN passes when:

1. A 5-second view of the surface produces correct answers to all four questions.
2. There is exactly one element that draws the eye first (and it is the intended primary).
3. Secondary and tertiary information layers are clearly subordinate.
4. Headings, bullets, and white space are used to support scanning.
5. The first viewport answers the user's "what and why" without requiring scroll.

### Severity defaults for SCAN

- **Critical**: 5-second test fails — user cannot identify page purpose or primary action.
- **High**: Visual hierarchy is unclear; multiple elements compete for primary attention.
- **Medium**: Walls of text; below-fold burial of important context.
- **Cosmetic**: Hierarchy works but could be sharper; minor decoration drift.

---

## Lens 4: ACT — Laws of UX + Norman's action cycle

**Question**: When the user takes action, does the system respect their cognitive constraints and complete the action loop?

ACT is the densest lens because it cross-references Norman's seven stages of action with the Laws of UX (Fitts, Hick, Miller, Jakob, Tesler, Postel, Doherty, Aesthetic-Usability, and others). Where DISCOVER asks whether the user can find the action, ACT asks whether the action itself is well-designed.

### Norman's action cycle

Seven stages, two gulfs:

1. **Goal** — what the user wants.
2. **Plan** — how they intend to do it.
3. **Specify** — the specific sequence of operations.
4. **Perform** — executing the operations.
5. **Perceive** — observing the system response.
6. **Interpret** — understanding what the response means.
7. **Compare** — checking the response against the goal.

Stages 1-4 cross the gulf of execution. Stages 5-7 cross the gulf of evaluation. ACT walks each stage for the surface's top three actions.

### The Laws applied

**Fitts's Law**: Time to acquire a target is a function of distance and size. Primary CTAs should be large and reachable. Touch targets should be at least 44x44px (Apple HIG) or 48x48px (Material). Distance from natural finger or cursor position matters.

ACT checks: are primary actions large enough, and within reach? Are destructive actions intentionally far from primary actions?

**Hick's Law**: Decision time grows with the log of the number of choices. Limit choices. Group related options. Use progressive disclosure.

ACT checks: how many choices is the surface presenting at once? Are choices grouped meaningfully? Are advanced options hidden by default?

**Miller's Law**: Working memory holds ~7 (±2) chunks. Don't ask users to hold more than that across steps.

ACT checks: do multi-step flows leak working-memory dependencies (e.g., requiring the user to remember a code from step 1 to enter at step 3)?

**Jakob's Law**: Users spend most of their time on other sites. They expect your site to work like the sites they already know.

ACT checks: do common patterns (cart icon top-right, hamburger menu, search top-bar, primary CTA in hero) follow convention? Or does the surface ask users to relearn conventions?

**Tesler's Law (conservation of complexity)**: Every system has a minimum amount of complexity that cannot be removed, only moved. Move complexity from the user to the system whenever possible.

ACT checks: is the surface pushing complexity onto the user (e.g., requiring them to format input, calculate values, choose between technical options) that the system could handle?

**Postel's Law**: Be conservative in what you do, liberal in what you accept. Validate input forgivingly; respond predictably.

ACT checks: do input fields accept multiple valid formats (phone number with or without spaces, dates in multiple formats)? Or do they reject anything that doesn't match exact format?

**Doherty Threshold**: Productivity soars when system response is under 400ms. Above that, users disengage.

ACT checks: do interactions feel within 400ms? Are slow operations indicated with skeleton/spinner immediately?

**Aesthetic-Usability Effect**: Users perceive aesthetic designs as more usable. But this is a halo effect — usability problems are still usability problems.

ACT checks: does the surface lean on aesthetic polish to mask usability problems? Conversely, is a functional but ugly surface being criticized for things that are actually aesthetic?

### Cognitive load across the action

For each top action, ACT calculates rough cognitive load:

- How many decisions does the user make?
- How many things do they have to remember?
- How many fields do they fill?
- How many steps does the action take?

A "buy" action that requires 12 fields and 4 steps has high cognitive load. A "buy" action that requires 2 fields and 1 step has low cognitive load. The lower the better, within reason.

### Anti-patterns in ACT

- **Tiny touch targets**: Buttons under 32px on mobile.
- **Choice paralysis**: 15+ options in a single menu or grid.
- **Working memory leaks**: Multi-step flows where step N depends on remembering data from step N-2.
- **Convention fighting**: Hamburger menu on top-left (instead of top-right RTL or convention-dependent), search at bottom of page, cart icon in footer.
- **Input rigidity**: Forms that reject "+962 79 786 8335" because they expected "00962797868335" (or vice versa).
- **Silent slowness**: Operations that take 1500ms with no visual indicator.
- **Polish-as-cover**: Visually beautiful surface with primary action 60px square and below the fold.

### When ACT passes

ACT passes when:

1. Top three actions have large, reachable, conventional controls.
2. Cognitive load is appropriate to the task (a critical action can ask more; a routine action should ask very little).
3. No working-memory leaks across multi-step flows.
4. Input is liberal (accepts multiple valid formats).
5. Response is under 400ms or has immediate progress indication.

### Severity defaults for ACT

- **Critical**: Action is impossible to complete (broken loop, missing feedback, blocked by error).
- **High**: Action requires excessive cognitive load (working-memory leak, 10+ choices, 5+ steps for routine task) OR primary control violates Fitts/Jakob severely.
- **Medium**: Action works but is harder than it should be (rigid input formats, minor convention fights, missing progress indicators).
- **Cosmetic**: Action is fine but a Law of UX could be applied more tightly.

---

## Lens 5: READ — microcopy rubric

**Question**: Does the language treat the user like an adult, in their voice, at the right moment?

READ audits the writing. It is the lens that is almost always done last in conventional reviews and almost always too late. Writing is design. Microcopy is the surface most users actually experience.

### What READ measures

- **Voice consistency**: Does the surface sound like one author across all copy, or does it shift tone between sections?
- **User language**: Are technical terms ("authentication token," "GUID," "E.164") used when user language ("login code," "your ID," "phone number") would do?
- **Specificity**: Are errors specific ("Phone number must include country code, e.g., +962 79 786 8335") or vague ("Invalid input")?
- **Empty/loading/success patterns**: Do empty states explain what to do, not just that there's nothing? Do loading states tell the user what's happening? Do success states confirm specifically?
- **CTA wording**: Do CTAs describe the action ("Save changes") or the outcome ("Get my report") rather than the system ("Submit," "OK," "Confirm")?
- **Tone calibration**: Does the celebration match the moment? (A signup might warrant warmth; an account deletion does not.)
- **Bilingual integrity**: If RTL, does the Arabic read naturally — not translated-from-English?

### The microcopy patterns

**Empty states**: Tell the user what they're seeing (or not seeing), why, and what to do.
- Bad: "No data."
- Better: "No transactions yet. Add your first payment method to start earning."

**Loading states**: Tell the user what's happening, especially if it's slow.
- Bad: spinner with no text.
- Better: "Connecting to your POS..."

**Success states**: Confirm what specifically happened.
- Bad: "Success!"
- Better: "50 points added to your balance."

**Error states**: Name the field. Name the problem. Name the fix.
- Bad: "Form contains errors."
- Better: "Phone number must start with +962. Tap the field to fix."

**CTAs**: Describe what the button does for the user.
- Bad: "Submit"
- Better: "Save changes" or "Confirm payment" or "Send code to my phone"

**Confirmation dialogs**: Don't ask "Are you sure?" Tell them what will happen.
- Bad: "Are you sure?"
- Better: "Delete 3 vouchers? This can't be undone."

### Voice characteristics by product type

The voice depends on the product. The rubric checks consistency, not a specific voice. A loyalty platform aimed at MENA partners might want: direct, warm, brief, unpretentious. A children's product might want: playful, encouraging. A medical product might want: calm, precise, never alarming.

What the rubric flags:

- **Voice inconsistency**: Different sections written by different unstated authors.
- **Tone whiplash**: Light/celebratory in error states; clinical in success states.
- **Over-formal**: "Please be advised that your account..."  when "Your account..." is what humans say.
- **Under-formal**: "Oops! Something went sideways :("  in a context where calm and specific is needed.
- **Corporate hedge**: "Please note that data may take up to..."  when "This usually takes about..." is what humans say.

### Anti-patterns in READ

- **System-speak**: "Authentication failed" instead of "We couldn't sign you in. Check your code and try again."
- **Vague errors**: "Something went wrong." "Form contains errors." "Invalid input."
- **Decoration words**: "Welcome to our amazing platform!" — words that add length without information.
- **Inappropriate hype**: "Congratulations on your purchase!" for a routine transaction.
- **Voice drift**: First-person plural ("we") in some sections, first-person singular ("I") in others, second-person ("you") in others — without intent.
- **Translation tells**: Arabic that reads like English in Arabic letters; English that reads like Arabic in English letters.

### When READ passes

READ passes when:

1. Voice is consistent across the surface.
2. Errors name the field, the problem, and the fix.
3. Empty/loading/success states tell the user something specific.
4. CTAs describe the action, not the system.
5. Tone calibrates to the moment.
6. Bilingual copy reads natively in both languages.

### Severity defaults for READ

- **Critical**: Errors are vague enough to block recovery; CTAs are ambiguous enough to mislead.
- **High**: Voice drift across major sections; empty/loading/success states are generic.
- **Medium**: System-speak in user-facing copy; CTAs that say "Submit."
- **Cosmetic**: Voice is right but could be tighter; minor formality drift.

---

## Lens 6: RECOVER — error design + a11y

**Question**: When things go wrong, does the system catch the user gracefully and offer a path forward? Does it meet WCAG 2.1 AA?

RECOVER is the last lens because errors and edge cases are the last thing teams get to. They are also the surfaces users remember most. A product is judged by its failure modes.

### Norman's error design principles

Norman's principles for error handling:

- **Errors should be prevented, not just handled.** Constraints, defaults, and confirmations reduce error occurrence.
- **When errors happen, they should be caught early.** Validate as the user types, not on submit, when possible.
- **Errors should not lose user work.** Form data should survive validation failure.
- **Error messages should be helpful.** Specific. In context. Suggesting a fix.
- **Destructive actions should require confirmation.** And the confirmation should describe the consequence.
- **Undo should be available.** For anything reversible.

### WCAG 2.1 AA — the floor

WCAG 2.1 AA is the legal and ethical floor for digital surfaces in most jurisdictions. The audit checks:

**Perceivable**:
- Text contrast at least 4.5:1 for normal text, 3:1 for large text.
- Non-text content (icons, charts) has text alternative.
- Information is not conveyed by color alone.

**Operable**:
- All functionality is available from keyboard.
- Visible focus indicator on all interactive elements.
- No keyboard trap.
- Touch targets at least 44x44 CSS pixels (WCAG 2.5.5 AAA — recommended).
- No content that flashes more than 3 times per second.

**Understandable**:
- Language of page is declared.
- Inputs have labels.
- Errors are identified, described, and (where applicable) suggested fixes.
- Consistent navigation.

**Robust**:
- Semantic HTML for assistive technology.
- ARIA used only where semantic HTML cannot express intent.
- Form fields have programmatically associated labels.

### Common courtesy

Beyond Norman and WCAG, the lens applies "common courtesy" — what a thoughtful designer does that no checklist requires:

- **Loading states for slow operations**: even if WCAG doesn't demand it, users do.
- **Confirmations for destructive actions**: even single-click delete with no undo is technically WCAG-compliant; it is not courteous.
- **Save drafts for long forms**: WCAG doesn't require it; respect for the user does.
- **Helpful 404s and 500s**: error pages that are blank or generic are technically compliant; helpful ones link back to common destinations.
- **Honoring user preferences**: prefers-reduced-motion, prefers-color-scheme, prefers-contrast.

### Recovery patterns

For the audit, RECOVER walks the top three error scenarios and the top three success scenarios:

**Error scenarios** — what happens when:
1. The user enters something invalid?
2. The system fails (timeout, server error, network)?
3. The user takes a destructive action?

For each:
- Is the error caught before submission where possible?
- Is the user's work preserved?
- Is the error message specific, helpful, and in the user's voice?
- Is there a clear path forward (retry, edit, contact support)?
- Is undo available where the action is reversible?

**Edge case scenarios** — what happens when:
1. The user has empty data (first-run, after deletion)?
2. The user has very large data (long lists, long text)?
3. The user is offline or slow network?

For each:
- Does the surface degrade gracefully?
- Is the user informed?
- Can they still do something useful?

### Anti-patterns in RECOVER

- **Validate-on-submit**: All errors revealed at once after the user thought they were done.
- **Generic 500s**: "Something went wrong" with no recovery path.
- **Destructive without confirm**: Single-click delete with no undo.
- **Lost work**: Form failure clears all fields.
- **Color-only error indication**: Red border with no text label.
- **Contrast failures**: Body text below 4.5:1 on background; error text below 4.5:1 on its background.
- **Keyboard traps**: Modal that traps focus and cannot be closed with Esc.
- **Missing focus indicators**: `:focus` styles removed or replaced with the default browser ring being suppressed without a replacement.
- **Auto-play motion**: Motion that does not respect prefers-reduced-motion.
- **Inaccessible custom controls**: Divs with `role="button"` that don't handle space/enter keyboard.

### When RECOVER passes

RECOVER passes when:

1. All top three error scenarios produce specific, helpful, contextual error messages.
2. User work is never lost to validation failure.
3. Destructive actions confirm with consequence-naming language.
4. Undo is available for reversible actions.
5. WCAG 2.1 AA is met across contrast, keyboard, focus, labels, and semantic HTML.
6. prefers-reduced-motion is honored.

### Severity defaults for RECOVER

- **Critical**: WCAG failures that block users (no keyboard access, missing labels, severe contrast failures); destructive actions without confirmation or undo; lost work on validation failure.
- **High**: Vague errors that block recovery; missing focus indicators; color-only error indication.
- **Medium**: Validate-on-submit when inline would work; generic 500 pages; missing prefers-reduced-motion.
- **Cosmetic**: Could-be-better error wording; minor contrast issues just under threshold.

---

## How the lenses interact

A single finding often violates multiple lenses. The audit reports against the **primary** lens (the one most diagnostic of the problem) but notes the secondary lenses in the finding body.

Common multi-lens findings:

- **Mystery icon CTA** — primary lens DISCOVER (no signifier), secondary READ (no label), tertiary ACT (Jakob's Law).
- **Form with vague error** — primary RECOVER (poor error design), secondary READ (vague microcopy), tertiary DISCOVER (gulf of evaluation).
- **Decorative below-fold hero** — primary SCAN (5-second test fails), secondary FRAME (outcome unclear), tertiary ACT (primary CTA out of reach).
- **Hidden destructive action** — primary RECOVER (no confirmation pattern), secondary DISCOVER (silent), tertiary ACT (Fitts — too easy to hit accidentally).

The lens hierarchy matters: when in doubt, attribute to the highest (most foundational) lens. If FRAME fails, that's where you report it, even if it manifests as a SCAN problem.

### When lenses contradict

Sometimes lenses pull in opposite directions. Examples:

- **DISCOVER vs ACT**: DISCOVER wants signifiers everywhere; ACT wants minimal cognitive load. Resolution: signifiers should be present but quiet.
- **SCAN vs READ**: SCAN wants brevity; READ wants specificity. Resolution: short sentences, specific words.
- **ACT vs RECOVER**: ACT wants frictionless action; RECOVER wants confirmation for destructive ones. Resolution: confirm only the destructive; flow the rest.

These tensions are not bugs in the framework. They are the actual design problem. The audit names the tension, then prescribes the resolution that respects the more critical lens.

---

## How /ux-audit produces structured reports

The `/ux-audit` command walks the six lenses against a target surface. The target is one of:

- A URL (live or staging).
- A Figma node or frame.
- A screenshot pasted into the conversation.
- A directory of source files (React, Vue, Blade, etc.).
- A description of the surface, if no artifact is available.

For each lens, the command:

1. Identifies relevant evidence from the target.
2. Tests against the lens's principles.
3. Produces zero or more findings.
4. Assigns severity per the defaults above (with override reasoning if the default is changed).
5. Names the principle violated (e.g., "Hick's Law," "Norman gulf of evaluation").
6. Quotes the evidence (copy excerpt, screenshot region, code snippet).
7. Prescribes a specific fix.

The report ends with:

- **Severity counts**: total Critical / High / Medium / Cosmetic.
- **Top 3 must-fix-now**: the highest-leverage three fixes.
- **Ship-readiness verdict**: pass / pass-with-fixes / hold / rework.
- **Conductor block**: suggested next prompts (e.g., "/ux-fix the top 3," "/ux-polish after critical fixes land").

The format is consistent across audits, which makes them comparable over time. See [Polaris-style audit reports](Polaris-style-audit-reports) for the full report format reference.

---

## How to read the severity counts

The severity counts tell you what kind of work the surface needs:

- **Critical > 0**: Do not ship. The surface has at least one issue that blocks users or violates accessibility law.
- **High > 5**: Major rework needed. The surface has multiple foundational problems; fixing them piecemeal will take longer than addressing the design pass.
- **High 1-5 + Medium > 10**: Targeted fix pass. Specific, scoped issues that can be addressed in a sprint.
- **High 0 + Medium > 0 + Cosmetic > 0**: Polish pass. The surface works; refinement remains.
- **All counts 0**: Ship-ready.

These thresholds are heuristic. Adjust to your context (e.g., a healthcare surface with one High in RECOVER may need rework; a prototype with three Highs may ship for user testing).

---

## How to read the top-3 must-fix-now

The top-3 is the audit's recommendation for highest-leverage fixes. It is not always the three Criticals. It might be one Critical plus two Highs that, if fixed, would also resolve five Mediums.

Read the top-3 as: "If you fix only these three things and ship, you will have addressed more user pain than any other three-item combination." Then audit the audit — does the top-3 make sense given your knowledge of users and constraints?

If the top-3 includes a Critical, that Critical is non-negotiable. If the top-3 is all Highs, you have judgment about scope.

---

## How to read the ship-readiness verdict

- **Pass**: All counts 0 or near-zero. Ship.
- **Pass with fixes**: Mediums and below remain. Fix in next iteration; ship now is acceptable if context permits.
- **Hold**: Highs remain. Don't ship the headline use case; fix first.
- **Rework**: Criticals remain. The design needs revisiting at a foundational level, not surface fixes.

The verdict is a recommendation. Override it with reasoning. A surface might be verdict "Hold" but be acceptable to ship for an internal beta; a surface might be verdict "Pass with fixes" but unacceptable to ship because the remaining Mediums are concentrated in the primary user flow.

---

## When to extend with MOTION lens

The six lenses do not include motion. Motion is its own lens, run via `/ux-motion`. Motion lens checks:

- prefers-reduced-motion respect.
- Animation purpose (does the motion serve communication or decoration?).
- Easing and duration appropriateness.
- Performance (no motion that drops frames).
- RTL-mirroring for directional motion.

Run `/ux-motion` after the six-lens audit if the surface has significant animation, transitions, or scroll-driven effects.

---

## When to extend with STYLE lens

Visual polish — typography refinement, spacing rhythm, color application, brand consistency — is run via `/ux-polish`. Style lens checks:

- Type ramp consistency.
- Spacing system adherence.
- Color application (semantic vs decorative).
- Brand voice in visual treatment.
- Photography/illustration treatment consistency.

Run `/ux-polish` after RECOVER findings are addressed. Polish before fixing fundamentals is wasted work.

---

## Reference summary

| Lens | Reference | Question |
|---|---|---|
| FRAME | Lean UX | Who is this for, what outcome, what hypothesis? |
| DISCOVER | Norman | Can a first-timer figure out what to do? |
| SCAN | Krug | In 5 seconds, what does a user understand? |
| ACT | Laws of UX + Norman action cycle | Does the action loop respect cognitive constraints? |
| READ | microcopy rubric | Does the language treat the user like an adult? |
| RECOVER | Norman error design + WCAG 2.1 AA | When things go wrong, does the system catch the user? |

Extensions:

| Lens | Command | Purpose |
|---|---|---|
| MOTION | `/ux-motion` | Animation, transitions, scroll-driven effects. |
| STYLE | `/ux-polish` | Typography, spacing, color, brand consistency. |

---

## Related pages

- [Polaris-style audit reports](Polaris-style-audit-reports) — the report format the lenses produce.
- [Wfrah-style case study format](Wfrah-style-case-study-format) — for documenting audit outcomes as case studies.
- [Frontend stacks compared](Frontend-stacks-compared) — for fix-implementation in different stacks.
- [Real-life UX consulting](Real-life-UX-consulting) — when you need a human review beyond the audit.

---

## Footer

Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
Author: Laith Aljunaidy — [LinkedIn](https://www.linkedin.com/in/laithaljunaidy/) — +962 79 786 8335
