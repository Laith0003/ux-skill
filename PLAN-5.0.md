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
| Book library (96 books) | research/library/ | Lessons normalized by topic (merged across books, weighted, no quotations, no names in lesson text), conflicts, measurable checks, gaps against the engine, and ACKNOWLEDGEMENTS.md thanking every author and book |
| The owner's product method | research/5.0/method.md | How real multi-role back offices were designed: personas, goals, every route to each goal, conceptual model, IA, flows with failure paths, prototyping inside the design system, walking every goal by every route, the one-page case. Method only, no client facts |
| 4.1 backlog | PLAN-4.1.md "Next, ranked" | Twelve ranked items, most of them render checks |

Where two inputs disagree, the primary source wins; the conflict and its resolution go in research/curriculum/corrections.md.

## Principles for every phase

- **Measure before claiming.** A new rule starts advisory. It moves to blocking only when the benchmark shows precision of at least 0.95 with a Wilson 95 percent lower bound of at least 0.90.
- **Prove on our own pages first.** Every render check runs over the site's pages before it ships, as in 4.1.
- **A rule change never silently changes a score.** Reports carry the ruleset version and digest; `--ruleset` scores with an earlier minor's rules.
- **Users before screens.** Product work starts from personas, goals and every route to each goal; screens mirror the site map and the flows. The engine teaches this order and checks it (Phase 6).
- **Judge the engine by outcomes, not only by rules.** Every phase reports its effect on the benchmark: per-rule precision, recall on seeded defects, and the method outcome scores (goal recall, route coverage, walk pass rate, dead ends, role leakage). A guide or rule that moves none of them in two releases is trimmed or merged.
- **The house rules hold:** looks are continuous functions of axes, brand and brief; pages use photographs; WCAG is cited only for what each criterion says; every error names the field and the fix; ASCII in new files; no client or vendor names in shipped docs.

## Phase 1. The benchmark (ux-bench)

Build the frozen corpus and the per-rule precision report. Spec: eval.md recommendations 1, 2, 5, 6, 9 and 10.

- bench/ with manifest, captured redistributable pages, expected findings, labels, briefs.
- 200 pages: 100 AI-built (50 generated from 10 fixed briefs, 50 found), 100 designer-built from openly licensed sources first. At least 60 percent redistributable; the rest stored as url, date, hash, findings and labels only. Split 140 dev and 60 holdout.
- `python -m bench run`, `python -m bench report` (precision, Wilson interval, tier per rule) and `bench/diff.py` (new and lost findings per rule between two engine versions).
- Labels: two independent passes and a tiebreak per finding; Krippendorff alpha per rule; a script that samples 50 findings for a human check. Labels are marked model-made until a human confirms the sample.
- A larger pool of 1,000 to 2,000 pages for rules that fire rarely, labelled up to 60 findings per rule.
- Recall, not only precision: a seeded-defect set where each planted fault is known, so the report also says what the engine misses. Each new check adds its fault to the set.
- An ablation run: the engine with and without each guidance pack on the fixed briefs, so the report shows which guidance changes the output and which only adds weight.

**Exit:** report.md lists every rule with counts, precision, recall on the seeded set and tier; every page renders identically twice; engine crashes found on the corpus are fixed or filed in the report.

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

## Phase 6. Method: users before screens

Spec: research/5.0/method.md. The engine learns the order that real product work follows and checks each artifact, so a builder gets a product people can use, not only a page that lints clean. Runs after Phase 5 (it needs `lint --render --url` and the `task` and `reach` probes) and absorbs navigation-ia.md and journeys-and-flows.md from Phase 7, so they are written once, with their checks.

The method, in order:

1. **Check what exists.** Audit the current build against how its shipped pages compose the kit, not only the component files. Reduce the spec to actors, jobs, objects, states, gaps and contradictions.
2. **Research mature tools for the same jobs.** How each leads a person to each kind of data; evidence strength recorded.
3. **Personas.** Who, the job, what they fear, what each may not see or do.
4. **Goals per persona,** every one of them.
5. **The route matrix.** Every goal against every entry point (navigation, home, search, filters, tabs, links between records, report drill-down, deep link, notification), each marked must, should or not needed with a reason.
6. **Conceptual model, IA and site map.** Objects, relations, states and who acts next, what can be undone; page structure decisions with the rejected options; the site map and its indexes.
7. **Flows.** One shared rule set (undo, reasons, denied, stale, focus, keyboard), then every flow with its click count, decision points, failure paths and exits.
8. **Prototype inside the design system.** Compose the way the shipped pages compose; a missing piece widens the kit, never forks it.
9. **Walk every goal by every route as each persona.** Rough recordings, one per route; each route reached, trouble, blocked or missing.
10. **The one-page case,** decided by the standard where the standard answers, then build, then walk the whole matrix again and list what was not walked.

No new command. `/ux-discover` gains a `method` mode (the router picks it for briefs with more than one role, or for admin, back office, portal and console projects); `/ux-design` gains a `structure` mode; `/ux-audit` gains a `walk` mode. CLI `uxskill method check|walk` and MCP `ux_method_check`, `ux_method_walk` mirror them. A single-role dashboard keeps its one-audience rule; several roles route to method mode.

| # | Task | Done when |
|---|---|---|
| M1 | JSON Schemas for personas, goals, routes, model, sitemap, flows, walks and decisions under `engine/method/schemas/`; loader errors name the file, the path and the fix | a broken fixture per artifact gives one error per fault, each naming field and fix |
| M2 | Guidance: references/process/users-before-screens.md (the method, with its failure modes), references/foundations/navigation-ia.md, references/process/journeys-and-flows.md; dashboard.md gains a back-office section (home as role-scoped queues, numbers that open their rows, saved views named by the work left) | every IA and flow row marked missing guide in the gap lists is written or parked with a reason |
| M3 | `/ux-discover` method mode and router rule | the router picks method mode on the multi-role briefs and not on the single-role ones |
| M4 | `/ux-design` structure mode, with the compose-from-the-shipped-kit step: per pattern, the kit piece and its call site in the project's own pages, or a proposal to widen the kit | on the back-office brief every page in the site map lists its patterns with a call site or a widen proposal |
| M5 | Static checks, advisory, with the fixture standard: every must route lands on a site-map page and no page is orphaned; every flow has a failure path, a cancel exit, a success exit and a focus target; every goal has at least one must route; undo in flows matches the model | each check has fixtures and a measured row in the method report |
| M6 | Walk harness on a running URL: scripted and generated walks per persona, goal and route, recordings, statuses, and a weak-walk guard (a walk that also passes on the old build counts as weak) | two runs on one build give the same statuses; a seeded missing route is reported missing |
| M7 | Live checks on the harness, advisory: each number on home equals the rows its link opens; each role sees only its own navigation; a disabled action says who can do it; deep links round-trip; focus lands on a named target after an action | each runs on the seeded-defect apps with precision and recall measured |
| M8 | Case page generated from the artifacts and walks, every finding linked to its recording | renders at 390 and 1280, light and dark |
| M9 | Method outcome benchmark in bench/method/: six fixed briefs (a back office with at least four staff roles and deadline-bound queues, a field team's role-switching mobile app, SaaS settings and billing, a two-role case-management tool, a single-owner shop dashboard as the control, a support desk), gold sets, three seeded-defect apps, a scoring script; each brief built with and without the method modes | bench/method/report.md gives goal recall, route coverage, flow completeness, walk pass rate, dead ends, role leakage, number-to-list parity, click cost against gold, and the added cost on the control brief |

**Exit:** the six briefs run end to end through method, structure, build and walk modes and produce a case page; the method modes beat the plain engine on route coverage and walk pass rate without adding weight to the control brief; every check is advisory with a measured row; gold sets are marked model-made until the owner confirms them; no client, vendor or person names in shipped files.

## Phase 7. Guidance that teaches

Spec: research/curriculum/guidance.md and research/library/topics.md and gaps.md (rows marked missing guide).

- New files: references/foundations/voice-and-multimodal.md, references/surfaces/portfolio.md, references/surfaces/checkout.md, references/process/design-sprint.md.
- Additions: ai-interfaces.md (process versus result, agent control levels, repair moves, one AI marker, the error types), color.md (harmony models and the seven contrasts), dashboard.md (chart rules), components (toasts that hold an action wait), /ux-research numbers (sample sizes, SUS scoring, pilots, task wording), /ux-audit as independent passes with severity factors and stable finding ids.
- Every claim carries a source id from the curriculum ledger or the library. Book lessons ship normalized: rewritten, merged across books, no quotations and no person names in the text; research/library/ACKNOWLEDGEMENTS.md thanks every author and book.
- Navigation and IA, and journeys and flows, are written in Phase 6 with their checks.

**Exit:** every missing-guide row in both gap lists is either written or marked park with a reason.

## Phase 8. Compliance evidence

Spec: landscape.md recommendations 2, 3 and 10.

- `uxskill audit --standard wcag22-aa | en301549-4.1.1 | ada-title-ii` writes a dated, reproducible report: ruleset and data versions, the criteria measured, the findings per criterion, and the criteria that still need a person, listed by name.
- The AI Act Article 50 pack from Phase 5 reports under its own heading with the dates it rests on.

**Exit:** the report for the site's own pages lists every WCAG 2.2 AA criterion as measured, needs a person, or not applicable, and nothing is claimed beyond what each criterion says.

## Phase 9. Interop

Spec: landscape.md recommendation 8.

- Read and write DESIGN.md; the 160 brand specs validate as DESIGN.md files.
- Emit the DTCG resolver document (2025.10) for the five mode axes.
- SARIF output and GitHub annotations from lint; stable exit codes documented.

**Exit:** round trips through DESIGN.md and DTCG with no mismatch, in release_checks.

## Phase 10. The taste test

Spec: eval.md recommendations 7 and 8.

- 30 briefs with fixed copy; each built with and without ux-skill by the same tool; screenshots at 1280 and 390.
- The harness randomises sides, repeats pairs and seeds gold pairs, and computes a Bradley-Terry estimate with bootstrap intervals.
- A model judge runs only as a pre-filter: both orders, consistent verdicts only, agreement with humans checked on gold pairs before any use. Its result is published as model-judged and never as the headline.
- The human round kit (rater instructions, the pair set, the analysis script) ships in bench/taste/ so a designer panel can run it.

**Exit:** the harness, the pair set and the model-judged pre-filter result are in the repo; the release notes say plainly that the human round is pending if it has not run.

## Phase 11. Running unattended

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

## Phase 12. Release 5.0.0

- Remove the seven 4.0 command aliases (they were due in 4.1).
- Migration guide docs/migrating-to-5.md; release notes docs/launch/release-5.0.0.md; CHANGELOG; README and the 16 translations; site figures regenerated; compare page refreshed with current facts; the precision report published as a page.
- Full suite clean, release_checks clean, the benchmark report attached.
- Merge feat/4.1-stageshow into main; the release workflow tags v5.0.0 and publishes the release.

**Exit:** v5.0.0 exists on GitHub with notes, the benchmark report and the SBOM; main is green; the canary is scheduled.

## Who does what

- Phases 1, 5, 6 and 10 are the heavy ones and run in a separate session on the owner's API credit, one phase per PR into feat/4.1-stageshow.
- The cloud session reviews each PR, runs the full suite, merges, and does Phases 2, 3, 4, 7, 8, 9, 11 and 12 between them.
- Owner decisions, the only ones left: turn on registry publishing; run the human taste round; confirm the 50-finding label sample; confirm the gold sets for the six method briefs.
- Every push, release and registry upload passes the release gate first: a leak and confidentiality scan of the source and of the unpacked artifacts. Nothing private, no client facts, no book text.
