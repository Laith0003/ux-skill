# ux-skill 5.0: the measured edition

5.0 is the release that can be left alone for months. Every rule carries a measured precision, every number in the guides traces to a source someone read, every report names the ruleset that produced it, and the project checks itself every week and opens an issue when something drifts.

5.0 ships everything on feat/4.1-stageshow (4.1 never ships on its own) plus the phases below. The integration branch stays feat/4.1-stageshow; each phase lands there as one PR with one review; 5.0.0 ships by merging that branch into main with docs/launch/release-5.0.0.md present, and the release workflow tags and publishes it.

## Inputs

| Input | Where | What it gives |
|---|---|---|
| Evaluation method | research/5.0/eval.md | Fixture standard, precision tiers, corpus, labelling, taste test, drift tracking |
| Landscape and standards | research/5.0/landscape.md | 2026 AI tells, modern CSS, platform changes that retire rules, compliance dates |
| Running unattended | research/5.0/stability.md | Dependency risks, CI gaps, release hardening, versioning policy |
| Curriculum (742 links) | research/curriculum/ | Lessons, proposed checks, guidance by target file, corrections, ledger |
| Book library (96 books) | research/library/ | Per-book lessons with pages, cross-book topics, conflicts, measurable checks, gaps |
| 4.1 backlog | PLAN-4.1.md "Next, ranked" | Twelve ranked items, most of them render checks |

Where two inputs disagree, the primary source wins; the conflict and its resolution go in research/curriculum/corrections.md.

## Principles for every phase

- **Measure before claiming.** A new rule starts advisory. It moves to blocking only when the benchmark shows precision of at least 0.95 with a Wilson 95 percent lower bound of at least 0.90.
- **Prove on our own pages first.** Every render check runs over the site's pages before it ships, as in 4.1.
- **A rule change never silently changes a score.** Reports carry the ruleset version and digest; `--ruleset` scores with an earlier minor's rules.
- **The house rules hold:** looks are continuous functions of axes, brand and brief; pages use photographs; WCAG is cited only for what each criterion says; every error names the field and the fix; ASCII in new files; no client or vendor names in shipped docs.

## Phase 1. The benchmark (ux-bench)

Build the frozen corpus and the per-rule precision report. Spec: eval.md recommendations 1, 2, 5, 6, 9 and 10.

- bench/ with manifest, captured redistributable pages, expected findings, labels, briefs.
- 200 pages: 100 AI-built (50 generated from 10 fixed briefs, 50 found), 100 designer-built from openly licensed sources first. At least 60 percent redistributable; the rest stored as url, date, hash, findings and labels only. Split 140 dev and 60 holdout.
- `python -m bench run`, `python -m bench report` (precision, Wilson interval, tier per rule) and `bench/diff.py` (new and lost findings per rule between two engine versions).
- Labels: two independent passes and a tiebreak per finding; Krippendorff alpha per rule; a script that samples 50 findings for a human check. Labels are marked model-made until a human confirms the sample.
- A larger pool of 1,000 to 2,000 pages for rules that fire rarely, labelled up to 60 findings per rule.

**Exit:** report.md lists every rule with counts, precision and tier; every page renders identically twice; engine crashes found on the corpus are fixed or filed in the report.

## Phase 2. The finding contract and score honesty

Spec: eval.md 3 and 4; stability.md changes 5 to 7.

- `Finding` gains `outcome` (violation or review), `selector` and `viewport`. Render checks over images, gradients and video return review. Review findings never count toward the score.
- Render failures leave the score and go to an "unmeasured" list.
- Every lint report, MCP result and hook message carries `ruleset_version`, `ruleset_digest` and `score_formula`. `--ruleset <minor>` scores with that minor's rules.
- The render pass blocks network by default, uses Playwright's own Chromium, records browser and Playwright versions, and sets explicit timeouts.
- Rich output only on a terminal; piped output is valid JSON, with a test that pipes lint output through json.loads.
- Severity follows the measured tier from Phase 1: rules below their tier are demoted, with the reason in the rule's entry.

**Exit:** the same page and ruleset give the same score on two machines; no rule is blocking without a measured tier.

## Phase 3. Correct what the sources contradict

Spec: research/curriculum/corrections.md, research/library/gaps.md (rows marked contradicts), landscape.md recommendation 7.

- Apply every correction a primary source supports: the Miller's law nav cap, research sample sizes, card sorting and tree testing, the 60-30-10 credit, translation expansion by string length, color blindness as 8 percent of men, the scrim alpha inside color.md, the streaming-scroll rule in ai-interfaces.md, the case-study grayscale and section order for portfolios.
- Retire or rewrite rules the platform outdated: the 100vh fallback rule, glass-without-fallback, the AVIF date, the animation rules (accept `@starting-style`, `allow-discrete`, `interpolate-size`), the z-index rule (suggest the top layer), justified text (hyphens is widely available).
- Audit every number and citation in references/ and data/ against its source. A number with no source that a reader could check is removed or marked as house practice.

**Exit:** corrections.md has no open row marked verified; a test fails if a reference cites a source id that the ledger does not hold.

## Phase 4. Read modern CSS

Spec: landscape.md recommendations 5 and 6.

- The CSS reader and the contrast gate resolve `light-dark()`, relative color, `color-mix()`, `contrast-color()`, nesting, `@scope`, `@layer` and style queries, or report them as unmeasured. Nothing is skipped silently.
- A Baseline policy setting backed by a bundled, versioned copy of the web-features data. Suggestion-level "prefer the platform" rules: popover, invoker buttons, container queries, OKLCH, text-wrap balance, field-sizing, details-content, same-document view transitions. Anchor positioning is advised per property, not as one feature.

**Exit:** a fixture set written only in modern CSS gets the same contrast verdicts as its hex twin.

## Phase 5. New checks, each measured as it lands

Every check ships with the fixture standard (at least 3 fail, 3 near-miss pass, 1 inapplicable, 1 right-to-left pass), runs over the site's pages, runs on the benchmark, and starts advisory. Ranked by impact on how well the page works and how un-generic it looks; the full ranked list with sources lives in research/curriculum/checks.md and research/library/checks.md.

Core set for 5.0:

1. `dead-click` (interact): an element that looks clickable does nothing within 500 ms.
2. `form-submit-silent` (interact): submitting a form empty shows no error, alert or new text within 1 s.
3. `leaked-runtime-value` (render): visible "undefined", "NaN", "[object Object]", unrendered template tokens.
4. `font-synthesized` (render): a weight or style is shown that no loaded face provides.
5. `breaks-between-widths` (render): a cheap overflow and overlap sweep from 320 to 1440 px in 40 px steps.
6. Reflow at 320 px and text spacing (WCAG 1.4.10, 1.4.12), zoom to 200 percent (1.4.4).
7. Control edges at 3:1 against the ground beside them (1.4.11).
8. `disclosure-state-missing`: a button that shows or hides content without `aria-expanded` or `aria-pressed` (4.1.2).
9. The 2026 AI-default looks: cream with serif and terracotta, near-black with one acid accent, newspaper layout, uniform card kit, stock decoration (all-caps eyebrows, middle-dot meta lines, arrows appended to links). The purple-gradient rules are demoted so avoiding purple alone no longer scores well.
10. Hierarchy: the largest first-screen text is the h1; one filled button per group; `heading-size-inversion`; `emphasis-over-budget`.
11. Reading measure and leading on body text; type-size drift; near-miss alignment and off-scale spacing.
12. `button-style-sprawl`: more than three looks for filled buttons.
13. AI interfaces (opt-in pack): chat with no AI disclosure by first interaction, the "may make mistakes" note far from the input, more than one assistant launcher, generic progress text.
14. `permission-request-on-load`, `empty-state-dead-end`, `error-far-from-field`, `nav-wraps`, `mobile-columns-over-two`, `large-collection-no-finder`.
15. `internal-link-broken` (depth-one crawl) and `js-only-content` (render with scripts off).
16. Complaint probes `task` and `reach` (4.1 backlog item 9) and `lint --render --url` for running apps (item 1).

**Exit:** each core check has its fixtures, its site run with zero false positives, and a measured row in bench/report.md.

## Phase 6. Guidance that teaches

Spec: research/curriculum/guidance.md and research/library/topics.md and gaps.md (rows marked missing guide).

- New files: references/foundations/navigation-ia.md (the four IA systems, how people look for information, tree testing), references/process/journeys-and-flows.md (flow before screens, success and failure ends), references/foundations/voice-and-multimodal.md, references/surfaces/portfolio.md, references/surfaces/checkout.md, references/process/design-sprint.md.
- Additions: ai-interfaces.md (process versus result, agent control levels, repair moves, one AI marker, the error types), color.md (harmony models and the seven contrasts), dashboard.md (chart rules), components (toasts that hold an action wait), /ux-research numbers (sample sizes, SUS scoring, pilots, task wording), /ux-audit as independent passes with severity factors and stable finding ids.
- Every claim carries a source id from the curriculum ledger or the library; the book library's lessons are paraphrased with page references, never quoted at length.

**Exit:** every missing-guide row in both gap lists is either written or marked park with a reason.

## Phase 7. Compliance evidence

Spec: landscape.md recommendations 2, 3 and 10.

- `uxskill audit --standard wcag22-aa | en301549-4.1.1 | ada-title-ii` writes a dated, reproducible report: ruleset and data versions, the criteria measured, the findings per criterion, and the criteria that still need a person, listed by name.
- The AI Act Article 50 pack from Phase 5 reports under its own heading with the dates it rests on.

**Exit:** the report for the site's own pages lists every WCAG 2.2 AA criterion as measured, needs a person, or not applicable, and nothing is claimed beyond what each criterion says.

## Phase 8. Interop

Spec: landscape.md recommendation 8.

- Read and write DESIGN.md; the 160 brand specs validate as DESIGN.md files.
- Emit the DTCG resolver document (2025.10) for the five mode axes.
- SARIF output and GitHub annotations from lint; stable exit codes documented.

**Exit:** round trips through DESIGN.md and DTCG with no mismatch, in release_checks.

## Phase 9. The taste test

Spec: eval.md recommendations 7 and 8.

- 30 briefs with fixed copy; each built with and without ux-skill by the same tool; screenshots at 1280 and 390.
- The harness randomises sides, repeats pairs and seeds gold pairs, and computes a Bradley-Terry estimate with bootstrap intervals.
- A model judge runs only as a pre-filter: both orders, consistent verdicts only, agreement with humans checked on gold pairs before any use. Its result is published as model-judged and never as the headline.
- The human round kit (rater instructions, the pair set, the analysis script) ships in bench/taste/ so a designer panel can run it.

**Exit:** the harness, the pair set and the model-judged pre-filter result are in the repo; the release notes say plainly that the human round is pending if it has not run.

## Phase 10. Running unattended

Spec: stability.md sections 1 to 5.

- release.yml runs only after tests pass on the same commit; builds once; attaches an SBOM; publishes the GitHub release from a draft; every step is safe to re-run.
- Registry publishing to PyPI and npm through trusted publishing (no stored tokens) is written but switched off until the owner turns it on; the owner's standing rule is that nothing is published there without an explicit yes.
- test.yml: Python 3.11 to 3.15 on a pinned runner image; a Playwright job that installs Chromium and fails if any render test is skipped; an MCP stdio test; a Windows job for the hook and the npm wrapper.
- pyproject: SPDX license, capped build backend, `requires-python >=3.11`, `playwright>=1.63,<2`, the missing image extra.
- dependabot: ignore majors for mcp and playwright, cooldowns, grouped updates.
- A weekly canary against the latest dependencies and the frozen corpus; it opens or updates one issue on drift and closes it when green.
- The hook launcher tries `UXSKILL_PYTHON`, python3, python and `py -3`; drop MultiEdit from the matcher; rate-limit the Stop hook.
- The MCP server checks its SDK and names the installed version and the right pin when it cannot start.
- Versioning policy in CONTRIBUTING.md: what semver covers (CLI flags, MCP tool names and shapes, token names, exit codes, rule ids), deprecation windows, rule and score versioning.

**Exit:** a fresh clone passes CI with zero skipped render tests; the canary has run green once; the policy is written.

## Phase 11. Release 5.0.0

- Remove the seven 4.0 command aliases (they were due in 4.1).
- Migration guide docs/migrating-to-5.md; release notes docs/launch/release-5.0.0.md; CHANGELOG; README and the 16 translations; site figures regenerated; compare page refreshed with current facts; the precision report published as a page.
- Full suite clean, release_checks clean, the benchmark report attached.
- Merge feat/4.1-stageshow into main; the release workflow tags v5.0.0 and publishes the release.

**Exit:** v5.0.0 exists on GitHub with notes, the benchmark report and the SBOM; main is green; the canary is scheduled.

## Who does what

- Phases 1, 5 and 9 are the heavy ones and run in a separate session on the owner's API credit, one phase per PR into feat/4.1-stageshow.
- The cloud session reviews each PR, runs the full suite, merges, and does Phases 2, 3, 4, 6, 7, 8, 10 and 11 between them.
- Owner decisions, the only ones left: turn on registry publishing; run the human taste round; confirm the 50-finding label sample.
