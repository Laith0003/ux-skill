# Polaris-style audit reports

The Polaris-style audit report is the plugin's house style for review outputs. Every finding follows the same shape — severity, lens, principle, evidence, fix — and reports end with severity counts, top-3 must-fix, ship-readiness verdict, and a conductor block.

This page is the reference for the format. If you are writing a custom audit prompt or extending the `/ux-audit` command, follow this format. If you are reading an audit report, this page tells you exactly what every section means.

---

## Why a consistent report format matters

UX audits without a consistent format are noise. The reader has to learn the writer's structure before they can extract value. Findings cannot be compared across audits. Severity is impossible to weight when one auditor's "Critical" is another auditor's "needs attention."

The Polaris-style format solves three problems:

1. **Consistency across audits.** A team that runs five audits on five surfaces gets five reports that read the same way. They can compare apples to apples.
2. **Reader speed.** A reader who knows the format can skim a 30-finding audit in under five minutes and know which three to act on first.
3. **Action over commentary.** Every finding ends with a fix. The report is not an opinion piece; it is a work order.

The format draws its name from the "polar" structure: each finding has two poles — what is wrong, and what to do about it. No middle. No diagnosis without prescription. No prescription without evidence.

---

## The 4-tier severity scale

The plugin uses four severity tiers. Each tier has explicit decision rules. The rules are not subjective.

### Critical

A Critical finding has at least one of:

- **Blocks user from completing the primary task.** The user cannot accomplish what the surface exists to help them accomplish.
- **Violates accessibility law (WCAG 2.1 AA).** Missing labels, severe contrast failures, keyboard inaccessibility, missing focus indicators on interactive elements.
- **Loses user data.** Form submissions clear fields on validation failure; destructive actions without undo or confirmation; cascading deletes without preview.
- **Creates legal or compliance risk.** Missing privacy disclosures on data-collecting forms; deceptive UI patterns (dark patterns) that risk regulatory action.
- **Breaks the application loop.** Buttons that do nothing; flows that loop infinitely; "submit" actions that produce no perceivable response.

A surface with one Critical finding does not ship. There is no negotiation; the finding is in the way of users.

### High

A High finding has at least one of:

- **Significantly degrades the primary task without blocking it.** Users can complete the task, but with noticeable friction, confusion, or risk of error.
- **Violates a foundational principle (FRAME audience drift, DISCOVER gulf of execution, SCAN 5-second failure).** The surface works mechanically but does not respect the foundation of good interaction.
- **Causes likely abandonment.** Patterns that match known abandonment triggers (too many fields, unclear progress, surprise costs, forced account creation).
- **Creates support load.** Patterns that users will routinely contact support about (because the surface itself does not explain or recover).

A surface with one High finding can ship if the team accepts the cost. A surface with many Highs needs rework before shipping.

### Medium

A Medium finding has at least one of:

- **Friction without abandonment.** Users complete the task, but slower or less confidently than they should.
- **Convention drift.** The surface fights Jakob's Law in places that confuse but don't block.
- **Microcopy quality issues.** Vague error wording, generic empty states, system-speak CTAs.
- **Visual hierarchy weakness.** Secondary elements competing with primary; insufficient white space.
- **Partial accessibility.** Touch targets at 32-43px (below recommended but above legal floor); contrast at 4.0-4.4:1 (close to AA threshold but not compliant).

A surface with many Mediums needs a polish pass. A surface with few Mediums can ship.

### Cosmetic

A Cosmetic finding has at least one of:

- **Refinement opportunity.** The surface works well; this would make it better.
- **Style preference within acceptable range.** Type-size choice could be tighter; color choice could be more deliberate.
- **Microcopy tone could be sharper.** The wording is correct; a better version exists.
- **Performance polish.** Page works at 1.5s LCP; could work at 1.0s with optimization.

Cosmetic findings inform polish passes. They never block shipping.

### Decision rules at a glance

| Tier | Blocks shipping? | Blocks task? | Legal/data risk? |
|---|---|---|---|
| Critical | Yes | Yes | Possible |
| High | Sometimes | Significantly degrades | No |
| Medium | No | Friction only | No |
| Cosmetic | No | No | No |

When the tier is ambiguous, prefer the higher tier. Under-reporting severity is worse than over-reporting.

---

## The 6 audit lenses

Every finding is attributed to exactly one primary lens. The lenses are:

| Lens | Reference | Question |
|---|---|---|
| FRAME | Lean UX | Who is this for, what outcome, what hypothesis? |
| DISCOVER | Norman | Can a first-timer figure out what to do? |
| SCAN | Krug | In 5 seconds, what does a user understand? |
| ACT | Laws of UX + Norman action cycle | Does the action loop respect cognitive constraints? |
| READ | microcopy rubric | Does the language treat the user like an adult? |
| RECOVER | Norman error design + WCAG 2.1 AA | When things go wrong, does the system catch the user? |

See [The 6 Audit Lenses](The-6-Audit-Lenses) for what each lens checks. The Polaris format requires the lens name in every finding so the reader can trace which discipline a finding violates.

A finding may also note **secondary lenses** in its body. This is normal — a vague error message that also fails contrast is primary RECOVER (accessibility), secondary READ (microcopy).

---

## Finding format

Every finding follows this exact template:

```
### F[number] · [SEVERITY] · [LENS] · [Short title]

Principle: [Named principle violated]
Evidence: [Specific evidence — copy excerpt, screenshot region, code snippet, flow step, URL]
Why this fails: [One sentence connecting evidence to principle]
Fix: [Specific change to make]
Effort: [Small / Medium / Large]
```

Each part is non-optional.

### F[number]

A sequential finding number across the whole report. F01, F02, F03. This lets the reader cite findings unambiguously ("F12 still needs work").

### Severity

CRITICAL, HIGH, MEDIUM, or COSMETIC. All uppercase. No qualifiers ("borderline high"); pick a tier and commit.

### Lens

FRAME, DISCOVER, SCAN, ACT, READ, RECOVER. All uppercase. Exactly one primary lens.

### Short title

Five-to-seven-word summary of the finding. Action-oriented when possible. Examples:

- "Primary CTA hidden below fold"
- "Submit button gives no feedback"
- "Error 'Invalid input' blocks recovery"
- "Touch targets below 44px on mobile"

Bad titles:

- "Issue with button" (too vague)
- "The submit button is hidden below the fold and the user might not see it" (too long)
- "UX problem" (not a description)

### Principle

The named principle violated. Use the exact name. Examples:

- "Hick's Law"
- "Norman gulf of evaluation"
- "Fitts's Law"
- "Jakob's Law"
- "WCAG 1.4.3 (contrast)"
- "WCAG 2.4.7 (focus visible)"
- "Krug 5-second billboard test"

Never:

- "the law about choices"
- "the accessibility thing"
- "user expectations"

If you don't know the exact principle name, the audit is not ready. Look it up.

### Evidence

The evidence is the proof. It must be:

- **Specific.** "The primary CTA on the homepage" — not "the CTA."
- **Quotable.** Copy text exactly as it appears; quote selectors exactly; cite URL with the path; reference screenshot region.
- **Re-findable.** A reader looking at the surface can locate the evidence in seconds.

Evidence types:

1. **Screenshot region.** "Top-right of hero section, /pricing page, 1440px viewport." If multiple findings cite the same region, link them.
2. **Copy excerpt.** Quote the exact text. Include surrounding context if needed for clarity.
3. **Code snippet.** For source-file audits, include the relevant 3-10 lines with file path and line number.
4. **Flow step.** "Step 3 of signup, after entering OTP, before tier selection."
5. **URL.** Include path, viewport size if relevant, and any query parameters.

### Why this fails

One sentence. Connects the evidence to the principle. Example:

- "The Submit button has no aria-label and no visible text — screen reader users hear 'button' with no further context, violating WCAG 4.1.2."

### Fix

The fix must be:

- **Specific.** Not "improve clarity" — describe the actual change.
- **Implementable.** A developer or designer should be able to act on it without further interpretation.
- **Scoped.** If the fix has dependencies, name them.

Bad fixes:

- "Improve the error message."
- "Make the button more discoverable."
- "Add accessibility."

Good fixes:

- "Replace 'Submit' with 'Save changes'. Add aria-label='Save changes' redundantly to button element."
- "Move primary CTA above fold. Reduce hero text to two lines. Maintain 16px button padding."
- "Add explicit error message above the field: 'Phone number must start with +962. Tap field to fix.' Border-color change alone is insufficient for accessibility."

### Effort

A rough estimate of fix size:

- **Small.** Single component, single field, copy change. Under 1 hour of dev work.
- **Medium.** Multi-component, requires design + dev, may touch state. 1 hour to 1 day.
- **Large.** Architecture-level, multi-file, requires re-design. 1 day or more.

Effort is the auditor's best estimate. The implementing team will re-estimate.

---

## Evidence types in detail

### Screenshot region

When auditing live surfaces, screenshot regions are usually the strongest evidence. They are unambiguous and quotable in followup conversations.

Format:

```
Evidence: Screenshot — homepage /, 1440x900 viewport, hero section bottom-right.
The "Get started" button overlaps the trust-badge row, with the bottom of the button
clipped at the fold (832px scroll line).
```

When citing screenshots, name:

- The page (path).
- The viewport size you observed it at.
- The region of the screenshot.
- What about it you are pointing to.

### Copy excerpt

When the issue is copy, quote it verbatim. Use quotation marks. Include surrounding text if the context matters.

```
Evidence: Copy excerpt — error state on /signup, after invalid phone submission.
> "Please correct the errors and try again."

The error does not name which field, what is wrong, or how to fix it.
```

### Code snippet

For source-file audits (when the audit target is a directory of source files, not a live surface), include 3-10 lines with file path and line number.

```
Evidence: Code — resources/views/components/forms/phone-input.blade.php, lines 14-22.

<input
  type="tel"
  name="phone"
  class="border @error('phone') border-red-500 @enderror"
  required
/>
@error('phone')
  <p class="text-sm text-red-600">{{ $message }}</p>
@enderror

The validation error is rendered correctly. But there is no aria-describedby
linking the error message to the input — screen readers do not associate the
error text with the input.
```

### Flow step

When the issue is in a multi-step flow, name the step precisely.

```
Evidence: Flow — signup, step 3 of 5 (OTP verification), after submitting code.
On submission, the page navigates to step 4 without any confirmation that
step 3 succeeded. The user is left to infer success from the step counter.
```

### URL

Always include the path. Include viewport if relevant. Include query parameters if they change the surface.

```
Evidence: URL — /partner/dashboard?tab=members, 1440x900.
The active tab indicator is invisible — the active tab and inactive tabs
have the same border-bottom color.
```

---

## Citation rules

The Polaris format requires naming the principle exactly. This is non-negotiable. The reasons:

1. **Reproducibility.** A reader can look up the principle and verify the audit's reasoning.
2. **Education.** Naming forces the auditor to know what they're citing.
3. **Argumentation.** When defending an audit's findings, "Hick's Law" is a defensible citation. "The law about choices" is not.

### Correct citations

| Concept | Correct citation | Wrong citation |
|---|---|---|
| Choice complexity | Hick's Law | "the law about choices" |
| Target acquisition | Fitts's Law | "buttons should be big" |
| Convention | Jakob's Law | "users expect things" |
| Working memory | Miller's Law | "people forget" |
| Complexity conservation | Tesler's Law | "make it simple" |
| Input forgiveness | Postel's Law | "be flexible" |
| Response time | Doherty Threshold | "should be fast" |
| Halo effect | Aesthetic-Usability Effect | "pretty is usable" |
| Gulf of execution | Norman gulf of execution | "user can't find action" |
| Gulf of evaluation | Norman gulf of evaluation | "user can't tell what happened" |
| Affordance/signifier/feedback | Norman affordances (or signifiers, or feedback) | "design language" |
| Scannability | Krug "Don't Make Me Think" 5-second test | "scan-friendly" |
| Conventions | Krug conventions principle | "follows patterns" |
| Lean | Lean UX hypothesis-driven design | "lean methodology" |
| Contrast | WCAG 1.4.3 (contrast minimum) | "color contrast" |
| Focus visible | WCAG 2.4.7 (focus visible) | "focus state" |
| Keyboard accessible | WCAG 2.1.1 (keyboard) | "keyboard navigation" |
| Labels | WCAG 3.3.2 (labels or instructions) | "form labels" |
| Errors | WCAG 3.3.1 (error identification) + 3.3.3 (error suggestion) | "error messages" |
| Touch targets | WCAG 2.5.5 (target size, AAA) | "tap targets" |

### Multi-principle findings

If a finding violates multiple principles, name all of them in the Principle line, separated by " + ".

```
Principle: Hick's Law + Norman gulf of execution
```

Order the principles by relevance — the most violated principle first.

### Custom principles

If the finding relates to a project-specific design system rule (e.g., "Dot DS Bronze tier color L=0.62 fails WCAG AA"), name it explicitly:

```
Principle: WCAG 1.4.3 (contrast minimum) — Dot DS Bronze tier at L=0.62 (4.21:1) on #FFFFFF
```

The reader needs to know both the foundational principle and the specific manifestation.

---

## Fix specificity

The fix line is the work order. Vague fixes mean nothing happens. Specific fixes mean the team can act.

### Test for fix specificity

Read the fix. Ask: "Can a developer who has never seen this surface implement this change without asking another question?"

If yes, the fix is specific enough. If no, rewrite.

### Examples

**Bad:**
```
Fix: Improve the error message.
```

**Good:**
```
Fix: Replace error text "Form contains errors" with field-specific messages.
For the phone field, use: "Phone number must start with country code, e.g.,
+962 79 786 8335." Render below the field via aria-describedby. Maintain
red color but also include the message text — color alone fails WCAG.
```

**Bad:**
```
Fix: Make the CTA more prominent.
```

**Good:**
```
Fix: Increase primary CTA size from 38px height to 48px height. Move from
bottom-right of hero to center-bottom, aligned with headline. Increase
contrast from current #2D2D2D-on-#F4F4F4 (8.2:1) — wait, that's fine.
The contrast is not the issue. The issue is position. Reposition only.
```

The second example shows the auditor catching themselves and prescribing what actually matters.

### When the fix is "we don't know yet"

Sometimes a finding identifies a problem with no clear solution. The fix line should still be specific — about the next step.

```
Fix: The first-run state shows zero data and zero suggestion of what to do.
This is a design problem, not a copy problem. Schedule a 30-minute design
session to specify the first-run experience: what the user sees, what they
can do, what example content (if any) appears. Until that's specified, fix
the symptom by adding the placeholder text "No transactions yet — link your
first POS to begin" — but the real fix is the design session.
```

---

## Report opening block

Every report starts with the same block:

```
# UX Audit · [Surface name]

Date: [YYYY-MM-DD]
Surface: [URL / path / Figma node / etc.]
Viewport(s) audited: [1440x900, 375x667, etc.]
Scope: [What was in scope — and what was out]
Method: [/ux-audit, manual review, etc.]

Primary user: [As inferred or stated]
Primary outcome: [As inferred or stated]
```

This block tells the reader what they are about to read. If "primary user" or "primary outcome" were inferred (not stated), say so — that itself is a FRAME finding to follow.

---

## Report ending block

Every report ends with the same block:

```
## Severity counts

- Critical: [N]
- High: [N]
- Medium: [N]
- Cosmetic: [N]

Total findings: [N]

## Top 3 must-fix-now

1. F[number] — [short title]
2. F[number] — [short title]
3. F[number] — [short title]

## Ship-readiness verdict

[Pass / Pass with fixes / Hold / Rework]

[1-3 sentence reasoning]

## Conductor

Suggested next prompts:
- [Specific next prompt]
- [Specific next prompt]
```

### Severity counts

Counts of findings by tier. No interpretation here, just numbers.

### Top 3 must-fix-now

The auditor's recommendation for highest-leverage fixes. As discussed under severity decision rules — these are not always the three Criticals. They are the three that, if fixed, would resolve the most user pain.

If there are fewer than 3 findings, show "Top N must-fix-now" with N = total findings.

### Ship-readiness verdict

One of four states:

- **Pass.** All counts at zero or near-zero. Ship.
- **Pass with fixes.** Mediums and below remain. Ship now if context permits; address in next iteration.
- **Hold.** Highs remain. Don't ship the headline use case; fix Highs first.
- **Rework.** Criticals remain. The design needs revisiting at a foundational level.

The verdict comes with one to three sentences of reasoning. The reasoning is what makes the verdict actionable.

### Conductor block

The conductor block suggests the next prompts the user might run. Examples:

```
Conductor:

Suggested next prompts:
- /ux-fix F01,F02,F03 — fix top 3 findings
- /ux-motion — audit animation layer (no motion in this audit)
- /ux-polish after critical fixes land
- /ux-case-study to document this audit's outcome
```

The conductor turns the audit into a workflow. It assumes the user wants to act, and tells them how.

---

## Foundation-style structure

When the audit is for a design system or foundation review (not a single surface), the format extends with foundation-style structure: principles → do/don't → examples → tokens → checklist.

This applies to commands like `/ux-foundation-review`.

### Principles

Name the foundation's principles. Example:

```
## Principles

1. Black is chrome, white is canvas.
2. Color carries meaning, never decoration.
3. Phone is primary identity.
```

### Do / Don't

For each principle, show examples of doing it and not doing it.

```
### Color carries meaning

Do:
- Red for destructive actions.
- Amber for warnings.
- Green for confirmation.

Don't:
- Red for decoration in the hero illustration.
- Amber for branded background color.
- Green for non-success states like "ready to start."
```

### Examples

Show concrete uses. Code, screenshots, copy excerpts.

```
### Examples

> "50 points added to your balance."

Green (#1B7F3A) used for the points delta. Background remains white.
The green is meaning-bearing — confirms the increment.

> "Voucher expires Dec 31, 2026."

Black (#000000) used for the text. Not red. Expiration is information,
not warning. Save red for actions that would lose value.
```

### Tokens

Show the actual design tokens — the variable names, the values.

```
### Tokens

--color-success: oklch(50% 0.12 145);
--color-warning: oklch(75% 0.15 75);
--color-danger: oklch(55% 0.20 25);
--color-text: oklch(15% 0 0);
--color-canvas: oklch(99% 0 0);
```

### Checklist

End with a usable checklist for new work.

```
### Checklist for new screens

- [ ] Every color used carries meaning OR is brand-mark dot.
- [ ] Black, white, gray are the structural palette.
- [ ] Semantic colors used only for state (success/warning/danger).
- [ ] No decorative gradients.
- [ ] Tenant content (logos, photos) carries the chromatic load.
```

---

## Length discipline

A 5-finding audit reads in 90 seconds. This is the bar.

If your audit takes longer to read than that, one of three things is happening:

1. **Findings are too verbose.** Each finding should be 5-10 lines. Trim.
2. **There are too many findings.** Combine related findings; demote Mediums to a single "Polish opportunities" section.
3. **The surface needs rework, not an audit.** If you have 30 Critical findings, stop auditing. Recommend rework. A 30-Critical report is not a useful artifact.

### Word budgets

- **Short title**: 5-7 words.
- **Principle**: 1-3 words (the named principle).
- **Evidence**: 1-3 sentences, plus quoted material as needed.
- **Why this fails**: 1 sentence.
- **Fix**: 1-3 sentences.
- **Effort**: 1 word.

Each finding totals around 50-100 words. A 10-finding audit is around 800 words plus the opening and ending blocks. Reads in 4-5 minutes.

### When to break the budget

Break the word budget only for Criticals that need full explanation, or for findings that include code snippets. Never break it for Cosmetics — if a Cosmetic needs more than 50 words, it is probably not a Cosmetic.

---

## Real example

Here is an example finding in full Polaris format:

```
### F03 · CRITICAL · DISCOVER · Submit button has no visible feedback

Principle: Norman gulf of evaluation + WCAG 4.1.3 (status messages)
Evidence: Flow — /signup, after clicking "Create account" button.
The button is clicked. The page does not visibly change for 1.2 seconds.
No spinner, no progress indicator, no button state change. The user has
no signal that the action was received.
Why this fails: The gulf of evaluation is unbridged — the user cannot
perceive that the system received their action.
Fix: On click, immediately (within 100ms): change button text to
"Creating account..." and add a disabled state with reduced opacity (0.6).
Add aria-live="polite" announcement: "Creating your account." Restore
button state on response. Keep total interaction under 400ms or show
progress text "Still working..." after 400ms.
Effort: Small
```

The finding takes about 100 words. A reader knows exactly what is wrong, why it's wrong, what to do about it, and how big the change is.

---

## Anti-patterns in audit reports

### The thesis paper

The auditor writes 3 pages about UX philosophy before getting to a finding. Cut all of it. The report is a work order, not an essay.

### The lecture

The auditor cites a principle and explains it at length. The reader doesn't need education in the report; they need to act. Cite the principle by name. If they want education, they can look it up.

### The hedge

The auditor writes "this might be an issue" or "consider whether this could perhaps be improved." Either it's a finding or it isn't. If you're not sure, it's not a finding yet — investigate more or drop it.

### The compliment sandwich

The auditor wraps every finding in praise. The report is not a feedback session; it's a work order. Praise once at the top if warranted ("The surface is structurally sound with a few targeted issues") and then get to work.

### The wall of Cosmetics

The auditor reports 30 Cosmetic findings to look thorough. The result is unreadable. Group Cosmetics by theme into a single section: "Polish opportunities." Spend the audit's word budget on Criticals and Highs.

### The vague Critical

The auditor labels something Critical without explicit Critical evidence (blocking task, violating WCAG, losing data, etc.). Either find the Critical evidence or downgrade.

### The missing fix

The auditor reports the problem without prescribing a fix. Send the report back — every finding needs a fix.

---

## Customizing the format

The Polaris-style format is the default. Customize it for specific needs:

### Adding fields

You may add:

- **Owner** (which team or person should own the fix)
- **Linked PR/issue** (link to the tracking artifact)
- **Verification** (how to verify the fix works)
- **Related findings** (cross-reference to other findings)

Never add:

- **Subjective rating** ("design quality: 7/10")
- **Author opinion** ("I don't love this")
- **Unscoped commentary** ("this might affect other parts of the app")

### Removing fields

You may remove:

- **Effort** if your team estimates separately.
- **Lens** if your team uses a different framework.

Never remove:

- Severity.
- Evidence.
- Fix.

These three are the minimum viable finding.

### Adjusting severity rules

You may add stricter rules for your context. Examples:

- For healthcare surfaces: anything that could lead to wrong medication dosage is Critical regardless of WCAG.
- For e-commerce: anything that could affect price display is Critical regardless of WCAG.
- For internal tools: lower the Critical bar — minor friction may be acceptable.

Document your customizations in your team's audit playbook. Don't reinvent severity per audit.

---

## Related pages

- [The 6 Audit Lenses](The-6-Audit-Lenses) — what the lenses check.
- [Wfrah-style case study format](Wfrah-style-case-study-format) — how to write up audit outcomes for portfolio or case study.
- [Frontend stacks compared](Frontend-stacks-compared) — for implementing audit fixes.
- [Real-life UX consulting](Real-life-UX-consulting) — when an audit needs human follow-up.

---

## Footer

Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
Author: Laith Aljunaidy — [LinkedIn](https://www.linkedin.com/in/laithaljunaidy/) — +962 79 786 8335
