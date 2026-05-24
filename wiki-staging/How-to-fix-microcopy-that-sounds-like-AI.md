# How to Fix Microcopy That Sounds Like AI

AI-generated copy fingerprints include marketing filler ("Elevate", "Seamless", "Unleash"), generic empty states ("No data yet"), unhelpful errors ("Form contains errors"), and "John Doe" placeholders. Here's how to detect and rewrite them using /ux-copy in Claude Code.

## What this page covers

You will learn the patterns that mark copy as AI-generated, run the audit on any surface, apply rewrites in place, and follow rules for error messages, empty states, loading states, success messages, and CTAs that read as written by a real person.

## Why AI-generated copy fails

Three reasons.

### Reason 1: it is generic by default

A language model trained on the internet writes the average of the internet. The average of the internet is bad marketing copy. Vague verbs. Abstract nouns. Promises with no substance.

Real copy says specific things. "Add a customer to a transaction." Not "Streamline customer engagement workflows."

### Reason 2: it pattern-matches to filler

The model has seen "Elevate your business" written so often it converges on it. Same for "Seamlessly integrate," "Unleash the power of," "Empower your team," "Transform your workflow." The phrases are dead. The model uses them anyway.

### Reason 3: it produces hostile error messages

When asked to write an error message, the model produces something like "An error occurred. Please try again." This says nothing. It tells the user nothing about what went wrong, nothing about what to do, nothing about whether to keep trying or call support. It is functionally adversarial.

A real error message names the field, names the problem, names the fix. "Email is missing the @ symbol. Add it to continue."

## The 10 most common AI copy fingerprints

### 1. Marketing filler verbs

The phrases "Elevate," "Unleash," "Empower," "Transform," "Revolutionize," "Streamline," "Enhance," "Optimize," "Maximize."

**Why it fails:** These verbs describe nothing. They promise improvement without specifying what improves or how.

**Fix:** Replace with the actual verb your product does. "Close your books" beats "Streamline your accounting workflow." "Reconcile six bank accounts" beats "Optimize your reconciliation process."

### 2. "Seamlessly" as a modifier

"Seamlessly integrate." "Seamlessly connect." "Seamlessly transition."

**Why it fails:** Adding "seamlessly" is a tell that the writer is hedging on the product's actual smoothness. Real seamless integration does not need to claim it is seamless.

**Fix:** Drop the adverb entirely. "Integrate with QuickBooks" beats "Seamlessly integrate with QuickBooks." If the integration is rough, fix the integration. Do not paper over it with "seamlessly."

### 3. "Powerful" as a feature descriptor

"Powerful analytics." "Powerful integrations." "Powerful automation."

**Why it fails:** "Powerful" describes nothing specific. Every product claims to be powerful.

**Fix:** Replace with a specific outcome. "Analytics that flag a 2 percent variance" beats "Powerful analytics." "Integrations with 14 banks and 6 ERPs" beats "Powerful integrations."

### 4. Marketing-cliche openings

"In today's fast-paced world..." "In the age of AI..." "In a world where customer expectations are higher than ever..."

**Why it fails:** Every reader has seen these openings hundreds of times. They signal the writer has nothing specific to say. They also signal AI generation almost universally.

**Fix:** Open with a specific scenario the reader recognizes. "Your CFO asks for the variance summary at 4:55 PM on Friday." beats "In today's fast-paced finance world..." 

### 5. Generic empty states

"No data yet." "Nothing to show." "Your list is empty." "No results found."

**Why it fails:** An empty state with no action is a dead end. The user gets there and has nowhere to go.

**Fix:** Sentence plus action. "No customers yet. Add your first one." beats "No data yet." "No transactions match your filter. Try broadening the date range." beats "No results found."

### 6. Unhelpful error messages

"An error occurred." "Form contains errors." "Invalid input." "Something went wrong."

**Why it fails:** These tell the user nothing about what is wrong or what to do. They are functionally adversarial.

**Fix:** Name the field, name the problem, name the fix. "Email is missing the @ symbol. Add it to continue." "Password must be at least 8 characters. Yours has 5."

### 7. "John Doe" and placeholder personas

"John Doe, CEO at Example Corp." "Jane Smith, Product Manager." Stock-looking avatars. Generic praise.

**Why it fails:** Every reader recognizes John Doe instantly. A landing page with John Doe testimonials reads as fake — because it is.

**Fix:** Real customers with permission and quoted attribution, or no testimonials at all. A page with no testimonials beats a page with fake ones.

### 8. Generic CTAs

"Get Started." "Learn More." "Click Here." "Submit."

**Why it fails:** These describe the action but not the outcome. They give the user no reason to click.

**Fix:** Verb plus outcome. "Book a 15-minute demo" beats "Get Started." "See the variance report on your own data" beats "Learn More." "Add my first customer" beats "Submit."

### 9. Success messages that celebrate too hard

"Congratulations! You have successfully completed your action!" "Awesome! Your changes have been saved!" "Great job! Welcome aboard!"

**Why it fails:** Real users do not need celebration for routine actions. The exclamation point and the enthusiasm read as condescending and AI-generated.

**Fix:** Calm confirmation. "Changes saved." beats "Awesome! Your changes have been saved!" "50 points added." beats "Congratulations! You have successfully earned 50 points!"

### 10. Loading states that say nothing

A spinner with no copy. "Loading..." with no context. "Please wait..."

**Why it fails:** A user staring at a spinner does not know what is happening or how long it will take. They cannot tell if it is stuck.

**Fix:** Tell the user what is happening. "Closing the books for May..." beats "Loading..." "Calculating variance across 6 accounts..." beats a bare spinner. If the action is under 300 milliseconds, skip the loading state entirely.

## Voice principles

The plugin enforces four voice principles. These apply to most products. Override them in discovery if your brand voice is different.

### Direct

Say what the thing is. Skip the throat-clearing.

Wrong: "We are excited to announce that we have just launched..."
Right: "Voucher redemption is live."

### Warm

Speak to a real person. Skip the corporate tone.

Wrong: "User authentication requires a valid OTP code."
Right: "Check your phone for the code."

### Brief

One sentence is usually enough. Two if the first does not land.

Wrong: "This dashboard provides you with a comprehensive overview of your customer engagement metrics across all touchpoints in your loyalty program."
Right: "Your loyalty program, on one screen."

### Unpretentious

Skip the jargon. Skip the enterprise vocabulary.

Wrong: "Leverage data-driven insights to optimize stakeholder engagement."
Right: "See who is coming back and who is not."

The voice can be different. A children's product is playful. A medical product is calm and precise. A finance product is sober and confident. The principles still apply — the voice is just oriented differently.

## Run /ux-copy on any surface

The command works against deployed URLs, local files, or directories.

```bash
# Audit a live page
/ux-copy https://your-site.com/landing

# Audit a local file
/ux-copy ./resources/views/landing.blade.php

# Audit a directory
/ux-copy ./src/components/

# Audit specific categories
/ux-copy ./landing.blade.php --only=cta
/ux-copy ./landing.blade.php --only=errors
/ux-copy ./landing.blade.php --only=empty-states
/ux-copy ./landing.blade.php --only=success
/ux-copy ./landing.blade.php --only=loading
/ux-copy ./landing.blade.php --only=marketing
```

The audit returns a structured report identifying filler words, marketing cliches, generic CTAs, hostile errors, and dead empty states.

## Apply fixes with /ux-copy --fix

The same command with `--fix` applies rewrites in place.

```bash
/ux-copy ./resources/views/landing.blade.php --fix
```

The plugin will:

1. Show each finding with the proposed rewrite
2. Ask for confirmation on judgment-level rewrites (taglines, hero copy, value propositions)
3. Apply mechanical fixes automatically (filler verbs, placeholder names, generic CTAs)
4. Generate a diff summary

For tighter control:

```bash
# Apply only mechanical fixes (no judgment calls)
/ux-copy ./landing.blade.php --fix --mechanical-only

# Apply only a specific category
/ux-copy ./landing.blade.php --fix --only=cta
/ux-copy ./landing.blade.php --fix --only=errors
```

The judgment-level rewrites (hero headlines, taglines) need your input. The plugin suggests but does not commit them without confirmation.

## Error message rules

Three rules. Apply them every time.

### Rule 1: name the field

A user with multiple form fields needs to know which field has the error.

Wrong: "Invalid input."
Right: "Email is invalid."

### Rule 2: name the problem

Tell the user what the system thinks is wrong.

Wrong: "Email is invalid."
Right: "Email is missing the @ symbol."

### Rule 3: name the fix

Tell the user what to do.

Wrong: "Email is missing the @ symbol."
Right: "Email is missing the @ symbol. Add it to continue."

### Real examples

| Wrong | Right |
|---|---|
| "Form contains errors." | "Email is missing the @ symbol. Add it to continue." |
| "Invalid input." | "Phone number must be 10 digits. Yours has 7." |
| "An error occurred." | "We could not save your changes. The server timed out. Try again in 10 seconds, or contact support if it keeps happening." |
| "Password is invalid." | "Password must be at least 8 characters with a number. Yours has 6 characters and no numbers." |
| "Email already exists." | "An account with this email already exists. Try logging in instead, or reset your password if you forgot it." |
| "Network error." | "We could not reach the server. Check your connection and try again." |
| "Unauthorized." | "Your session expired. Log in to continue." |
| "Not found." | "We could not find a customer with that phone number. Try searching by email, or add the customer as new." |
| "Rate limit exceeded." | "Too many attempts. Wait 60 seconds and try again." |
| "Server error 500." | "Something broke on our end. We are on it — try again in a minute." |

The right column says what is wrong, in what field, and what to do. Every time.

## Empty state rules

Three rules.

### Rule 1: a sentence

Acknowledge the empty state in one sentence.

Wrong: "No data."
Right: "No customers yet."

### Rule 2: an action

Tell the user what to do next.

Wrong: "No customers yet."
Right: "No customers yet. Add your first one."

### Rule 3: optional context

If the empty state needs explanation (filtered results, first run, etc.), add one more sentence.

Right: "No customers yet. Add your first one to start tracking visits."

### Real examples

| Wrong | Right |
|---|---|
| "No data yet." | "No transactions yet. Process your first sale and they will appear here." |
| "Nothing to show." | "No customers match this filter. Try broadening the date range or clearing filters." |
| "Your list is empty." | "No vouchers yet. Send your first one from the Customers page." |
| "No results found." | "No customers found matching 'Sarah'. Check spelling or search by phone." |
| "No tasks." | "No tasks today. Add one or wait until tomorrow." |
| "Inbox empty." | "Inbox empty. Nothing to read." |

The right column is honest about the empty state and gives the user a way forward.

## Loading state rules

Three rules.

### Rule 1: tell them what is happening

A spinner alone says nothing. Pair it with a description.

Wrong: A bare spinner.
Right: "Closing the books for May..."

### Rule 2: be specific

If the system is doing one of several things, say which.

Wrong: "Loading..."
Right: "Calculating variance across 6 accounts..."

### Rule 3: under 300 milliseconds, no loading state

If the action completes in under 300ms, the loading state flashes and disappears. Skip it entirely. A successful state appears instantly.

### Real examples

| Wrong | Right |
|---|---|
| "Loading..." | "Loading your dashboard..." |
| Bare spinner | "Generating the variance report..." |
| "Please wait..." | "Reconciling 6 accounts..." |
| "Processing..." | "Charging $1,200 to card ending 4232..." |
| "Saving..." | "Saving changes to customer Sarah Chen..." |

### When the action might fail or take a long time

Add a status update after a few seconds.

```
"Closing the books for May..."   [appears immediately]
"Still working — this can take 30 seconds on large datasets."   [appears after 5s]
"Almost done — finalizing the variance summary."   [appears after 20s]
```

The user knows the system is alive. They know roughly how long. They are not tempted to refresh.

## Success message rules

Three rules.

### Rule 1: brief

A single phrase. Sometimes a single word.

Wrong: "Congratulations! Your customer has been successfully added to the system!"
Right: "Customer added."

### Rule 2: no celebration

Skip the exclamation points. Skip the "great job" tone. Routine actions deserve routine confirmations.

Wrong: "Awesome! Your changes have been saved!"
Right: "Changes saved."

### Rule 3: include the specific thing

If the action affected a specific record, name it.

Wrong: "Customer added."
Right: "Sarah Chen added."

### Real examples

| Wrong | Right |
|---|---|
| "Congratulations! You earned 50 points!" | "50 points added." |
| "Awesome! Your changes have been saved!" | "Changes saved." |
| "Great job! Welcome aboard!" | "Account created. Welcome." |
| "Your voucher has been successfully redeemed!" | "Voucher redeemed. 200 points off your next visit." |
| "Successfully sent!" | "Message sent to Sarah Chen." |
| "Saved!" | "Customer Sarah Chen saved." |
| "Done!" | "Report exported to /Downloads/treasury-may.pdf." |

The right column is calm. It confirms the action. It names what was affected. It does not celebrate.

### Exception: meaningful milestones

Some milestones deserve celebration. A customer's tier upgrade. A first sale. A goal reached. The plugin allows celebration in these cases — but it still avoids exclamation point overload.

Right: "You hit Silver. Lifetime discount is now 8 percent."
Right: "First sale closed. The next ones get easier."

Calm milestones. Not exclamation point storms.

## CTA microcopy rules

Three rules.

### Rule 1: verb plus outcome

The CTA says what the action is and what the user gets.

Wrong: "Get Started."
Right: "Start a free trial."

### Rule 2: specific over generic

Specific actions beat generic ones.

Wrong: "Learn More."
Right: "See the workflow in 60 seconds."

### Rule 3: the user's words, not yours

Frame the CTA from the user's perspective.

Wrong: "Submit your inquiry."
Right: "Send my question."

### Real examples

| Wrong | Right |
|---|---|
| "Get Started" | "Start a 14-day free trial" |
| "Learn More" | "See the variance report on your own data" |
| "Click Here" | "Book a 15-minute demo" |
| "Submit" | "Add my customer" |
| "Sign Up" | "Create my account" |
| "Subscribe" | "Subscribe — one email per week" |
| "Buy Now" | "Order — ships in 2 days" |
| "Download" | "Download the white paper (PDF, 4 pages)" |
| "Continue" | "Continue to payment" |
| "Cancel" | "Keep editing" |

The right column tells the user what happens when they click. It uses verbs they would use themselves.

### Cancel and back button copy

The "cancel" or "back" button needs special attention. The wrong copy makes users hesitate.

| Wrong | Right |
|---|---|
| "Cancel" | "Keep editing" (in a modal asking if they want to discard changes) |
| "No" | "Stay here" (in a confirmation to leave a page) |
| "Cancel" | "Discard changes" (when canceling means destruction) |
| "Back" | "Back to customers" (when the destination is known) |

The right column tells the user what happens. It removes ambiguity about which button is destructive.

## The filler-word ban list

Words and phrases the plugin flags. Each has a replacement category.

### Verbs to avoid

- **Elevate** — replace with the actual verb (raise, increase, improve in a specific way)
- **Unleash** — replace with the actual verb (start, activate, enable)
- **Empower** — replace with the actual capability (give, allow, let)
- **Transform** — replace with the actual change (change, replace, rebuild)
- **Revolutionize** — replace with the actual change (change, redo)
- **Streamline** — replace with the actual outcome (simplify by removing X, shorten by Y)
- **Enhance** — replace with the actual improvement (improve in a specific way)
- **Optimize** — replace with the actual change (improve speed, reduce errors, cut steps)
- **Maximize** — replace with the actual goal (increase, raise)
- **Leverage** — replace with "use"

### Adverbs to avoid

- **Seamlessly** — drop entirely
- **Effortlessly** — drop entirely
- **Intuitively** — drop entirely
- **Powerfully** — drop entirely
- **Smartly** — drop entirely
- **Automatically** — keep only if literally true

### Adjectives to avoid

- **Powerful** — replace with specific capability
- **Robust** — replace with specific capability
- **Comprehensive** — replace with specific scope
- **Cutting-edge** — drop entirely
- **State-of-the-art** — drop entirely
- **Best-in-class** — drop entirely
- **World-class** — drop entirely
- **Industry-leading** — drop entirely
- **Game-changing** — drop entirely
- **Next-generation** — drop entirely
- **Innovative** — drop entirely

### Phrases to avoid

- **In today's fast-paced world** — drop entirely
- **In the age of AI** — drop entirely
- **Now more than ever** — drop entirely
- **In a world where** — drop entirely
- **Take your X to the next level** — replace with specific improvement
- **Unlock the power of** — drop entirely
- **At the heart of** — drop entirely
- **Reimagine your X** — drop entirely
- **The future of X is here** — drop entirely
- **X has never been easier** — drop entirely

## The marketing-cliche ban list

Sentences the plugin flags as cliche.

- "We are excited to announce..."
- "We are thrilled to share..."
- "Our team has been working hard to..."
- "Welcome to the future of..."
- "Designed with you in mind..."
- "Built for the modern X..."
- "Trusted by thousands of customers..."
- "Join the X revolution..."
- "Get the most out of your..."
- "Take your X to the next level..."
- "The only X you will ever need..."
- "Everything you need to X, all in one place..."

These read as filler. They signal nothing specific about the product.

### Replacement strategy

For each cliche, the plugin asks what specific thing the cliche was trying to say, and replaces it with that.

Wrong: "We are excited to announce that we have just launched our new dashboard."
What it was trying to say: The dashboard is live.
Right: "The dashboard is live."

Wrong: "Trusted by thousands of customers in the finance industry."
What it was trying to say: They have many customers.
Right: "1,200 finance teams use it weekly." (with a real number)

Wrong: "Take your treasury workflow to the next level."
What it was trying to say: It helps with treasury work.
Right: "Close your weekly treasury report in 14 minutes."

## Real before/after examples

### Example 1: a SaaS hero

Before (AI-generated):
```
Unleash the Power of Your Data

Elevate your business with our innovative platform that seamlessly
integrates with your existing tools to empower your team and
transform your workflow.

[Get Started]   [Learn More]
```

After (`/ux-copy --fix` plus brand voice):
```
Close your weekly treasury report in 14 minutes, not 4 hours.

Reconciliation across 6 bank accounts, FX positions, and intercompany
loans — done before your 9 AM standup.

[Book a 15-minute demo]   [See it on your own data]
```

Specific. Concrete. Verb-driven. CTAs that say what happens.

### Example 2: a form error

Before (AI-generated):
```
Error: Form contains errors. Please correct and try again.
```

After:
```
Email is missing the @ symbol. Add it to continue.
```

Specific. Names the field. Names the fix.

### Example 3: an empty state

Before (AI-generated):
```
No data yet.
```

After:
```
No customers yet. Add your first one to start tracking visits.

[Add a customer]
```

Sentence plus action plus optional context.

### Example 4: a loading state

Before (AI-generated):
```
Loading...
```

After:
```
Closing the books for May...
```

(After 5 seconds, if still loading:)
```
Closing the books for May...
Still working — this can take 30 seconds on large datasets.
```

Specific. Honest. Calm.

### Example 5: a success message

Before (AI-generated):
```
Congratulations! Your customer has been successfully added to your account!
```

After:
```
Sarah Chen added.
```

Brief. Calm. Names the specific thing.

### Example 6: a CTA

Before (AI-generated):
```
[Get Started]
```

After:
```
[Add my first customer]
```

Verb plus outcome. User's frame.

### Example 7: a feature card

Before (AI-generated):
```
Powerful Analytics

Get powerful insights into your business with our cutting-edge analytics
platform that helps you make data-driven decisions and optimize your
performance.
```

After:
```
Variance alerts under 2 percent

Get a Slack ping the moment a bank account drifts more than 2 percent
from forecast. Stops surprises before your CFO sees them.
```

Specific capability. Concrete outcome. Real user benefit.

### Example 8: an onboarding step

Before (AI-generated):
```
Welcome! Let's get you started on your journey to success.
```

After:
```
Add your first bank account.

We support 14 major banks via Plaid. Takes 2 minutes.

[Connect a bank]
```

Action-led. Practical. Tells the user what is next.

## When the copy is right

Signals that copy passes the test.

- A user could read it aloud without sounding like a robot
- It says something specific that no other product could say verbatim
- It names the user's situation, not generic "users"
- Errors tell the user what is wrong and what to do
- Empty states give the user a way forward
- CTAs say what happens when clicked
- No filler verbs, no marketing cliches, no John Doe placeholders

When the copy passes all of these, the surface no longer reads as AI-generated.

## Beyond the audit: voice as system

The audit catches violations of universal rules. A real product voice goes further — it has a specific personality, references, sense of humor, and tone.

Use `/ux-design` with brand voice samples in the discovery questions to bake voice into new surfaces. Use the design system's `voice.md` foundation document to keep the voice consistent across writers.

Voice is a system. The plugin enforces the system at write time and audit time.

## Linked next steps

- The visual fingerprints of AI are a related problem class. See [How to fix AI-generated UI](How-to-fix-AI-generated-UI).
- A real design system bakes voice into the foundations. See [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code).
- The landing page is where voice gets tested first. See [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code).
- Error messages are part of the accessibility surface too. See [How to audit accessibility with Claude Code](How-to-audit-accessibility-with-Claude-Code).

---

**See also**: [How to fix AI-generated UI](How-to-fix-AI-generated-UI) | [How to generate a design system with Claude Code](How-to-generate-a-design-system-with-Claude-Code) | [How to build a SaaS landing page with Claude Code](How-to-build-a-SaaS-landing-page-with-Claude-Code)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
