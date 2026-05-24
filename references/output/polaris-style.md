# Polaris Style — Review-Report Output

This is the house style for every review-report output the plugin produces. It governs `/ux-audit`, `/ux-critique`, `/ux-a11y`, `/ux-copy`, `/ux-motion`, and `/ux-polish`. A report that ignores this style is rejected and rewritten.

The style is foundation-first: principles, then do/don't, then examples, then tokens, then a checklist. No prose detours. No marketing. No trailing pleasantries.

---

## Report Opening

Every report opens with three lines, in this order:

1. **Verdict** — one sentence. "Ship-blocking." / "Ships with fixes." / "Ready to ship."
2. **Scope** — what was reviewed and what was excluded.
3. **Surface** — the route, screen, or component reviewed, with a single locator (file path, URL, or screen name).

Example:

```
Verdict: Ships with fixes.
Scope: Member-side stamp-card grid; partner dashboard excluded.
Surface: /member/cards (resources/views/member/cards/index.blade.php)
```

No banner. No table of contents. No "Hello, here is the audit." The reader sees the verdict in the first second.

---

## Severity Scale

Four levels. Use exactly these names.

### Critical

Definition: The product is broken, unsafe, illegal, or impossible to use for the affected segment. Ship blocks until fixed.

Decision rules:
- Accessibility regression below WCAG 2.1 AA threshold for a non-decorative element.
- Data loss, broken submit, broken navigation that traps the user.
- Misleading copy that creates legal or financial risk (wrong price, wrong amount, missing consent).
- Layout broken in RTL or on a supported viewport such that the primary task is impossible.

### High

Definition: The product works but the affected flow is materially degraded. Ship if there is a documented follow-up; otherwise fix first.

Decision rules:
- Primary CTA unclear, mislabeled, or competing with a secondary action.
- Form errors that say what is wrong but not what to do.
- Contrast at AA threshold for body text or important UI.
- Motion that runs longer than 400ms on a path the user takes more than once per session.
- Missing feedback after a user action (silent success, silent failure).

### Medium

Definition: The product works and the flow is usable, but the experience is noticeably worse than the standard the team has set elsewhere. Ship; fix in the next iteration.

Decision rules:
- Copy that is correct but verbose.
- Spacing inconsistent with adjacent components.
- Empty state present but generic.
- Icon-only control without an accessible name.
- Animation timing inconsistent across similar components.

### Cosmetic

Definition: Polish. The product is right; this is taste, alignment, or refinement. Ship; batch with the next polish pass.

Decision rules:
- A hairline that should be a token, not a hex.
- Letter-spacing on a headline that should be tighter at large sizes.
- A focus ring that is correct but not as crisp as the system's other focus rings.
- A loading state that is fine but could be faster-feeling.

If you cannot decide between two levels, choose the higher one. The audit should err toward fixing.

---

## Finding Format

Every finding uses this exact template. No deviations.

```
[SEVERITY] [LENS] Principle violated
Evidence: <one specific artifact>
Fix: <one prescriptive action>
```

Worked example:

```
[High] [READ] Form error names the problem but not the action
Evidence: resources/views/auth/login.blade.php:42 — "This field has an error."
Fix: Replace with "Phone number must be in international form. Add a country code, e.g. +962 79 786 8335."
```

Worked example, second:

```
[Critical] [ACT] Primary CTA contrast 3.1:1 fails WCAG 1.4.3
Evidence: Member dashboard "Redeem" button, white text #FFFFFF on tier-bronze #B58460.
Fix: Move to bronze L=0.50 token (#9C6B47), measured 5.96:1 on white text. Apply at theme layer.
```

Worked example, third:

```
[Medium] [SCAN] Visual hierarchy collapses below the hero
Evidence: /member/home — section headings and body copy both 16px, no weight differentiation, no rhythm.
Fix: Promote section headings to 20px / 600 weight. Add 32px margin above, 16px below. Match the spacing token used on /member/cards.
```

Rules:
- One finding per block. Never bundle "five things in one finding."
- The Evidence line names one artifact. A file path, a copy excerpt in quotes, a code snippet of three lines or fewer, a flow step, or a URL. Pick one type.
- The Fix line is prescriptive and copy-pasteable. The reader should not have to interpret the fix.
- No "consider," "perhaps," or "we might want to." The fix tells the reader what to do.

---

## Evidence Types

Five evidence types are allowed. Use exactly one per finding.

| Evidence type | When to use it | Format |
|---|---|---|
| Screenshot region | Visual hierarchy, spacing, alignment, color, motion stills | A clipped image of the relevant region, captioned with route and viewport. |
| Copy excerpt | Microcopy, errors, empty states, button labels, headings | Verbatim text in quotes, with file path or screen location after the quote. |
| Code snippet | A specific implementation defect (token mis-use, missing aria attribute, wrong color value) | Three lines or fewer, in a fenced block, with file:line prefix. |
| Flow step | Multi-step issues (the user did X, then Y, then Z, and Z failed) | A numbered list of steps with the failure point flagged. |
| URL | Live surface, deployed bug, third-party component | A single URL line. No screenshot if the URL is the artifact. |

If a finding needs two evidence types, split it into two findings.

---

## Citation Rules

When a finding rests on a principle, name the principle. Be specific.

Acceptable:
- "Hick's Law" (decision time grows with options)
- "Fitts's Law" (target size and distance govern selection time)
- "WCAG 1.4.3 — contrast minimum 4.5:1 for body text"
- "WCAG 2.5.5 — target size minimum 44px"
- "Omit needless words" (microcopy and label compression)
- "Missing feedback after user action" (the system silently succeeded or failed)
- "Recognition over recall" (the user should not have to remember what was on the previous screen)

Unacceptable:
- "best practice"
- "we always do it this way"
- "industry standard"
- "research shows"

If you cannot name the principle, the finding is not yet earned. Either find the principle or downgrade the finding to "taste call" under the Cosmetic tier.

---

## Fix Specificity Rule

The Fix line is the most important line in the finding. It must be specific.

Bad fixes:
- "Improve clarity."
- "Make this more accessible."
- "Use a better CTA."
- "Reduce cognitive load."

Good fixes:
- "Rename 'Submit' to 'Pay $24.99'."
- "Change body color from #6B7280 to #4B5563 (token: text-secondary). Measured contrast 7.1:1."
- "Replace 'Submit' button with two buttons: 'Save draft' (secondary) and 'Publish' (primary). Publish stays on the right under RTL too."
- "Cap modal animation at 200ms; remove the easing on the backdrop fade."

The fix names the change, the value, and the location. The reader applies it without interpretation.

---

## The 6 Audit Lenses

The plugin reviews every surface through six lenses. Each lens has a job. Use them in this order; flag findings under exactly one lens.

### FRAME

What the surface is and who it is for. Audience clarity, scope, promise, expectation-setting.

Invoke when: opening a new surface, reviewing a landing page, evaluating onboarding, judging whether the surface honors the brand voice.

Covers: page title, hero promise, audience assumptions, "what is this," scope mismatch.

### DISCOVER

How the user finds what they need. Navigation, search, information architecture, findability.

Invoke when: reviewing a dashboard, a settings surface, a multi-section product, a catalog, any surface where the user starts not knowing what is there.

Covers: nav labels, search behavior, IA depth, breadcrumbs, empty state guidance, find-vs-recall friction.

### SCAN

How the eye reads the page before the user commits. Visual hierarchy, typography, spacing, contrast, density.

Invoke when: reviewing any text-heavy or component-dense surface; reviewing a card, list, table, or dashboard.

Covers: heading hierarchy, weight contrast, line-height, spacing rhythm, density, color hierarchy, alignment.

### ACT

How the user takes action. CTAs, forms, buttons, controls, primary/secondary distinctions.

Invoke when: reviewing any surface with a primary action; reviewing forms, checkout, sign-up, redeem, settings.

Covers: CTA labels, button hierarchy, form layout, input affordances, target size, action confirmation, undo, motion timing on action.

### READ

How the user understands what just happened or what they must do. Microcopy, errors, empty states, success states, system feedback.

Invoke when: reviewing forms, errors, transactional flows, status feedback, any surface that talks back to the user.

Covers: error wording, empty state copy, success messages, inline help, tooltips, labels, the line of voice consistency.

### RECOVER

How the user fixes mistakes and undoes harm. Undo, back, cancel, recovery, destructive-action confirmation.

Invoke when: reviewing any flow with a destructive or hard-to-reverse action; reviewing forms, deletions, sign-up, sign-out, payment.

Covers: undo affordances, cancel flows, destructive-action confirmation, error recovery, browser back behavior, state restoration.

If a finding fits two lenses, choose the one that names the user's job at that moment. The lens is for organizing the report, not for showing breadth.

---

## Report Ending

Every report ends with four elements, in this order.

### 1. Severity counts

```
Critical: 1
High: 3
Medium: 4
Cosmetic: 6
```

Render as a table or a four-line block. No prose.

### 2. Top-3 must-fix-now

Three bullet points. Each names one finding by ID or by Lens + Principle. These are the items that block ship.

```
Top fixes:
- [Critical][ACT] CTA contrast 3.1:1, breaks WCAG.
- [High][READ] Login error names problem, not action.
- [High][SCAN] Section headings same weight as body — page reads as a wall.
```

### 3. Ship-readiness verdict

One sentence. Matches the opening verdict or supersedes it with new context from the body of the report.

```
Ships after the three top fixes land.
```

### 4. Conductor block

Three suggested next prompts, formatted as a fenced code block. The reader copies one of them.

```
Next:
/ux-audit /member/cards   # re-run after fixes
/ux-copy /auth/login      # tighten the login error pass-through
/ux-a11y /member          # AA sweep across all member surfaces
```

No closing pleasantry. No "I hope this helps." No summary paragraph. The conductor block is the last thing the reader sees.

---

## Voice Rules

The report's voice is direct, prescriptive, and dry.

Never use:
- "elevate," "unleash," "seamless," "robust," "leverage," "synergy," "delightful"
- "we believe," "we feel," "in our opinion"
- "best-in-class," "world-class," "next-generation"
- "Just a quick note," "Hope this helps," "Let me know if you have questions"
- exclamation marks
- emoji

Always use:
- The active voice ("The button breaks at 320px" not "The button is broken at 320px")
- Specific names ("the Redeem button" not "the CTA")
- Specific numbers (44px, 3.1:1, 200ms) not adjectives ("small," "low," "fast")
- Imperatives in fixes ("Change," "Replace," "Add," "Remove," "Move")

The report reads like a checklist a senior engineer would write to a peer. No selling. No softening.

---

## Foundation-Style Structure

Every report follows this structure. The reader can skim it in one pass.

1. **Opening** — Verdict, scope, surface. (Three lines.)
2. **Findings** — Grouped by severity, then by lens within each severity. Critical first.
3. **Patterns** — If three or more findings share a root cause, name the pattern in one paragraph. ("Spacing rhythm is inconsistent across the member section because no spacing token is enforced at the layout layer.")
4. **Tokens** — When findings cite design tokens, list the affected tokens once at the end. ("Tokens referenced: text-secondary, surface-2, motion-fast, border-hairline.")
5. **Checklist** — A copy-pasteable checklist of every Fix line, in priority order, with checkboxes.
6. **Ending** — Severity counts, top-3, verdict, conductor block.

No "introduction." No "conclusion." No sources, no further reading.

---

## Tables vs Prose

Default to tables and bullet lists. Use prose only when a relationship between findings needs to be explained.

Use a table when:
- Listing severity counts.
- Comparing tokens before and after.
- Showing measured values (contrast, timing, target size).
- Mapping findings to lenses.

Use bullets when:
- Listing top fixes.
- Naming files touched.
- Naming next-prompt suggestions.

Use prose when:
- Explaining a pattern that ties three or more findings to one root cause.
- Naming a taste call where the principle is contested.

Prose paragraphs in this style are two sentences. Three at most.

---

## Length Discipline

A 5-finding audit must be readable in 90 seconds.

Targets:
- 5 findings: 80 to 130 lines of output.
- 10 findings: 150 to 220 lines.
- 20 findings: 280 to 380 lines.

If the report exceeds these targets, the report is bloated. Cut adjectives, merge near-duplicate findings, move the third evidence type to a follow-up.

The reader does not have time to read a long report. The plugin's job is to compress the audit to the smallest set of high-leverage findings, each with one fix.

---

## Pre-Send Checklist

Before the report is returned, verify every item.

- [ ] Opening is exactly three lines (Verdict, Scope, Surface).
- [ ] Every finding uses the `[SEVERITY] [LENS] Principle\nEvidence: ...\nFix: ...` template.
- [ ] Every Fix line is prescriptive and copy-pasteable.
- [ ] Every principle is named (Hick's Law, Fitts's Law, WCAG section, named UX principle — be specific).
- [ ] No "consider," "perhaps," "might want to."
- [ ] No marketing words (elevate, unleash, seamless, robust).
- [ ] No emoji.
- [ ] No source URLs in the body of the report.
- [ ] Severity counts present.
- [ ] Top-3 must-fix-now present.
- [ ] Ship-readiness verdict present.
- [ ] Conductor block present with three next prompts.
- [ ] Report fits the length target for its finding count.

A report that fails any item is rewritten before send.
