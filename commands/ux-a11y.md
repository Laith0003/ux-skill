---
description: WCAG 2.1 AA accessibility audit plus common-courtesy checks beyond the spec. Produces findings grouped by WCAG criterion with severity, evidence, and fix. Triggers on "accessibility check", "WCAG audit", "is this accessible", or "a11y review".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(curl:*), Bash(date:*), Glob, Grep, Task, WebFetch
disable-model-invocation: false
---

# /ux-a11y

You are running the `/ux-a11y` command from the `ux` plugin. The job is a structured WCAG 2.1 AA audit of a surface, plus the common-courtesy checks that pass automated tools but still hurt real users.

## When to use

Triggers: "accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check", "color contrast", "ARIA review", "make this accessible".

Use whenever a surface is touched by users beyond the team, especially before shipping any production change. Also use proactively after a redesign — accessibility regressions are the most common silent failure.

## Input

One of: a URL, an absolute file path (Blade view, JSX, HTML), a screenshot, a code snippet. If a live URL is available, prefer it — automated tools and keyboard testing only work on live surfaces. If only static markup is available, the audit will be partial and you must flag what could not be verified.

## Process

### 1. Identify the surface mode

- **Live URL** → can verify contrast computationally, keyboard tab order, focus visibility, ARIA in DOM, dynamic states.
- **Code/file** → can verify semantic HTML, ARIA attributes, alt text presence, contrast against declared colors, focus management code paths.
- **Screenshot only** → can verify visual contrast (sampled), focus visibility if shown, color-not-only, dynamic-type tolerance. Cannot verify keyboard, screen reader, or dynamic states.

Surface the mode at the top of the report so the user knows what could not be verified.

### 2. Run the 11-point checklist

For each item, check the relevant WCAG success criterion (cite the SC number) and decide pass / fail / partial / not-verifiable.

#### 1. Color contrast (WCAG 1.4.3, 1.4.11)

- Body text: ≥ 4.5:1 against its background.
- Large text (18pt regular or 14pt bold): ≥ 3:1.
- Non-text UI (focus rings, icons, form borders): ≥ 3:1.
- Compute ratios; do not eyeball.

#### 2. Keyboard navigation (WCAG 2.1.1, 2.1.2)

- Every interactive element reachable via Tab in a sensible order.
- No keyboard traps (modals, custom widgets).
- Custom widgets respond to expected keys (Esc closes, arrows navigate menus).

#### 3. Focus indicators (WCAG 2.4.7)

- Every focusable element has a visible focus indicator.
- Contrast of focus ring ≥ 3:1 against adjacent colors.
- No `outline: none` without a replacement.

#### 4. Screen reader compatibility (WCAG 1.3.1, 4.1.2)

- Semantic HTML used (`<button>`, `<nav>`, `<main>`, `<header>`, not all `<div>`).
- Form fields have associated `<label>` (explicit `for` or wrapping).
- Custom widgets use ARIA roles, states, properties correctly.
- Decorative images have `alt=""`, meaningful images have descriptive alt.

#### 5. ARIA usage (WCAG 4.1.2)

- ARIA only where semantic HTML is insufficient (first rule of ARIA: don't use ARIA).
- `aria-label` / `aria-labelledby` on every unlabeled control.
- `aria-live` regions for async updates.
- No conflicting or stale ARIA (`aria-expanded` not updated, `aria-hidden` on focusable elements).

#### 6. Color is not the only signal (WCAG 1.4.1)

- Errors use icon or text in addition to red.
- Status badges have shape or text in addition to color.
- Charts have patterns or labels in addition to color.

#### 7. Dynamic type tolerance (WCAG 1.4.4, 1.4.10)

- Text scales to 200% without loss of content or function.
- No fixed pixel sizes that break at large type.
- Reflows correctly at 320px width.

#### 8. Reduced-motion preference (WCAG 2.3.3)

- `prefers-reduced-motion` media query respected.
- Auto-playing animations stop, loop or simplify under reduced motion.
- Parallax, tilt, large translations disabled or reduced.

#### 9. Form-error patterns (WCAG 3.3.1, 3.3.3)

- Errors announced to screen readers (`aria-live` or `aria-describedby`).
- Errors associated with the offending field.
- Error messages specific (name the field, name the fix).
- Errors do not rely on color alone.

#### 10. Semantic HTML (WCAG 1.3.1)

- Headings in correct hierarchical order (no skipped levels).
- Lists use `<ul>` / `<ol>` / `<li>`.
- Tables use `<table>` with `<th>` and proper scope.
- Buttons are `<button>`, links are `<a>` with `href`.

#### 11. Image alt text (WCAG 1.1.1)

- Every `<img>` has an `alt` attribute (even if empty).
- Decorative images: `alt=""`.
- Meaningful images: short, descriptive, not "image of."
- Complex images (charts, diagrams): long description nearby or linked.

### 3. Score and group findings

For each failing or partial item, assign severity:

- **Critical** — blocks an assistive-tech user from completing the task. Examples: unlabeled form fields, keyboard trap, missing focus indicator on a CTA.
- **High** — degrades the experience significantly. Examples: contrast slightly under threshold, heading hierarchy broken, error not announced.
- **Medium** — friction the user can work around. Examples: alt text present but generic, focus order suboptimal.
- **Cosmetic** — best-practice but not a barrier. Examples: ARIA where semantic HTML would do, redundant labels.

### 4. Format the output

```
─── a11y audit ───
Surface:      <URL / path / description>
Mode:         <live URL | code | screenshot>
Verified:     <list of points fully verified>
Partial:      <list of points partially verified — explain why>
Not verified: <list of points that could not be verified in this mode>

Severity counts:  Critical <n> | High <n> | Medium <n> | Cosmetic <n>

─── findings ───

WCAG <SC number> — <SC name>
  [<severity>] <finding title>
    Evidence:  <what you saw — include selector or line number if code>
    Fix:       <what to do — be specific>

WCAG ...
  ...

─── beyond WCAG ───
<common-courtesy findings that pass spec but still hurt users — e.g., autoplay video, tiny tap targets, time-limited dialogs>
```

### 5. Persist state

Write `.ux/last-a11y.json`:

```json
{
  "command": "ux-a11y",
  "timestamp": "<ISO8601>",
  "surface": "<URL / path / description>",
  "mode": "live | code | screenshot",
  "verified_points": ["<list of point names>"],
  "partial_points": ["<list>"],
  "not_verified": ["<list>"],
  "findings": [
    {
      "wcag_sc": "1.4.3",
      "sc_name": "Contrast (Minimum)",
      "severity": "Critical | High | Medium | Cosmetic",
      "title": "<short>",
      "evidence": "<what you saw>",
      "fix": "<what to do>",
      "category": "code | copy | motion | other"
    }
  ],
  "beyond_wcag": [
    { "title": "<short>", "evidence": "<>", "fix": "<>" }
  ],
  "severity_counts": { "critical": <n>, "high": <n>, "medium": <n>, "cosmetic": <n> }
}
```

The `category` field tells `/ux-fix` which sub-agent to dispatch.

### 6. Optional fix flag

If the user passed `--fix`, after writing the report:

1. Validate clean working tree.
2. For each finding sorted Critical → Cosmetic (skip Cosmetic unless `--include-cosmetic`):
   - `category: code` → dispatch `frontend-engineer`.
   - `category: copy` → dispatch `copy-writer`.
   - `category: motion` → dispatch `motion-engineer`.
3. Where independent, dispatch in parallel in a single message.
4. Each agent commits atomically with a message naming the WCAG SC and the fix.
5. After fixes, re-run the audit on a live URL if available and report deltas.

## Output

The audit report and (if `--fix`) the fix-loop results.

## State persisted

- `.ux/last-a11y.json` — keys: `command`, `timestamp`, `surface`, `mode`, `verified_points`, `partial_points`, `not_verified`, `findings` (array of `{wcag_sc, sc_name, severity, title, evidence, fix, category}`), `beyond_wcag` (array), `severity_counts`.

## Next prompt

```
─── next ───
Recommended: /ux-a11y --fix     (apply the fixes)
Other moves: /ux-copy            (form-error wording deep-dive)
             /ux-motion          (reduced-motion compliance deep-dive)
             /ux-audit           (broader structural review)
             /ux-next            (let me decide)
```

If `not_verified` is non-empty and a live URL is feasible, recommend re-running on the live URL before fixing — partial audits produce regressions.

## Hard rules

- Never claim a point passes without verifying it. If you cannot verify in the current mode, mark it `not_verified` and explain.
- Never recommend ARIA where semantic HTML would do. The first rule of ARIA is don't use ARIA.
- Never compute contrast by eye — sample colors and calculate.
- Never auto-fix accessibility without re-verifying. Silent fixes create new regressions.
- Never skip the `beyond_wcag` section — passing WCAG is the floor, not the ceiling.
- Never dispatch fixes for `not_verified` items. Verify first, then fix.

## Failure modes

- **False clean reports**: marking everything pass in screenshot mode. Many WCAG criteria are not verifiable from a screenshot — say so.
- **Severity flattening**: every finding marked Critical. Only assistive-tech blockers are Critical.
- **ARIA over-reach**: suggesting `aria-label` on a `<button>` that already has visible text. The text IS the label. Adding ARIA duplicates it.
- **Contrast eyeballing**: declaring "this looks fine" instead of computing. Always compute.
- **Color-only-signal blindness**: missing that a red error border is the only error indicator. Look for the redundancy in every status communication.
- **Reduced-motion oversight**: not checking `prefers-reduced-motion` because the animation "looks fine." That is the wrong test — the test is whether motion-sensitive users can use the surface.
