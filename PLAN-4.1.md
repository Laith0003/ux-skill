# ux-skill 4.1: what is done and what is left

This file is the handoff for finishing 4.1 on `feat/4.1-stageshow`. A session that has only this repository can work from it. PLAN-4.1-inventory.md holds the research behind the checks. Delete both files in the release commit.

## The theme

4.0 builds the system. 4.1 makes the skill prove the page: everything a person complains about, and everything the canon says a page must do that a browser can measure, is measured on the rendered page, at every width, before the work is called done.

## Done on feat/4.1-stageshow

- **Stageshow absorbed** (MIT, credited in NOTICE). Three pieces:
  - `system export --to stageshow` writes the system's look;
  - `uxskill kit stageshow` drops the kit into a project with backups;
  - the product illustration guide and three illustration lint rules.
- **The complaint contract.** `uxskill complaints check --page <file or URL> [--before]` keeps the person's words as probes, and `complaints snapshot` keeps the page before it changes. The plugin's stop hook holds the session while a complaint is open or the check is stale. Record: complaints-close-by-measurement.
- **Render checks, measured at every width unless noted.**
  - `first-screen-covered` (record: first-screen-stays-clear)
  - `target-too-small` (record: targets-meet-the-floor)
  - `text-low-contrast`, read on the screen the visitor sees, at 1280px; accent text is now read the same way (record: all-text-measured-as-seen)
  - `input-text-zooms`
  - `image-broken`
  - `image-distorted`
- **Lint rules.** `title-is-a-framework-default`, `consent-prechecked`, `fake-urgency` and `confirmshaming`. Quoted mentions are read as mentions. An inline passive listener is no longer flagged. 178 rules in all.

## Waiting on the owner

- Create the v4.0.0 GitHub release from main (commit b8571f9) with the notes in docs/launch/release-4.0.0.md (they arrive with the release refresh PR), and set the repository's About text and topics.
- Publish 4.0.0 to PyPI and npm.
- Run a TypeScript check on the vendored kit (`engine/kits/stageshow`) in a project that has react, react-dom and lucide-react, before 4.1 ships.
- The figures for the investment section of the 4.0 launch post (marked in docs/blog/ux-skill-4-foundations.html).
- One existing post names a real client: docs/blog/redesign-existing-website-with-ux-skill.html. Decide whether to keep it.

## Next, ranked

Each item names where it lands. Build each with tests, one review, the full suite and a run over the site's own pages to prove zero false positives first.

1. **Render the running app.** `uxskill lint --render --url` reuses the complaints snapshot (styles inline, scripts removed after they ran), so frameworks are measured as served.
2. **Focus not obscured** (2.4.11). In engine/render/interact.py's tab pass, check that the focused box is not covered by fixed or sticky author content.
3. **Reflow and text spacing** (1.4.10, 1.4.12). Add a 320 by 640 viewport, and a pass with the WCAG text-spacing values forced that re-runs the overflow and clip checks.
4. **Control edges** (1.4.11). Input, checkbox and radio borders at 3:1 against the ground beside them; render, in taste.py beside the text contrast.
5. **Reading measure and leading.** Characters per rendered line of body text (house range from references/foundations/typography.md) and line height under 1.5 on body text. Render.
6. **Type-size drift.** Computed font sizes under 6% apart on one page, monospace and decorative text left out, measured against the system's type roles. Render, in taste.py.
7. **Near-miss alignment and off-scale spacing.** Left edges 1 to 6px apart within a section, and gaps off the page's base step. Render, in core.py.
8. **Hierarchy.** The largest text on the first screen is the h1, and one button group holds at most one filled button. Render.
9. **Dashboard numbers.** Tabular figures and right alignment in numeric table cells. Render, beside references/surfaces/dashboard.md.
10. **Input semantics.** Name, email, phone and card fields carry autocomplete tokens and the right type (1.3.5), and paste is never blocked. Lint.
11. **Complaint probes `task` and `reach`.** Steps to click, then a selector that must show; Tab presses to reach a selector. In engine/complaints.py, with the weak test against `--before`.
12. **Guidance the research found missing**, each as a reference file:
    - Nielsen's ten heuristics (references/laws/nielsen-heuristics.md, cited from commands/ux-audit.md);
    - AI interfaces: streaming, stop and regenerate, editable output, citations, uncertainty, disclosure, reversible agent actions (references/surfaces/ai-interface.md);
    - checkout (references/surfaces/checkout.md);
    - chart rules for dashboards: data ink, direct labels, no dual axes, sorted bars, small multiples (references/surfaces/dashboard.md);
    - toasts that hold an action wait for the person (references/foundations/components.md).
13. **Optional component tier in tokens.css** from the contracts (`--button-primary-bg: var(--color-action-primary)`), so one component can be restyled without touching a role.
14. **Router SKILL.md, manifest sync and a smaller MCP surface**; rule tiers and a hook that reports only new findings.

## What this round taught

- **Prove a render check on the site first.** Every check ran over the site's own pages before it shipped. That run found the false positives the fixtures missed:
  - root-relative images on pages opened from disk;
  - a page with smooth scrolling, which the scroll pass had to scroll instantly;
  - grounds a script swaps in on scroll;
  - drawers parked off screen by a transform, which the freeze would have measured open.
- **Measure what the visitor sees, not the page at rest.** Scroll-led pages change their ground as they move. A check that reads the page unscrolled measures colors no one sees.
- **A probe must fail on the original.** A check written after a fix tends to pass on the old page too. The `--before` run marks those weak.
- **A snapshot must stand alone.** Inline the styles, including rules added by script, and make the base absolute. Otherwise a later edit to a stylesheet reaches the old page.
- **A real fault on our own site is a result.** The new checks found contrast failures, 14px search fields and an inline listener bug on the project's own pages, and each was fixed.
- **One review per change, then fix with a test.** Every review in this round found real defects that tests had not covered: five in the occlusion check, seven in the complaints.
