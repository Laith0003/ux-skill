# ux-skill 5.0: the measured edition

5.0 is the release that can be left alone for months and still be trusted. Every rule carries a measured precision. Every number in the guides traces to a source someone read. Every report names the ruleset that produced it. The engine leads a builder from users to structure to screens, in that order, and checks each step. Arabic and right to left are designed first, not mirrored. The project checks itself every week and opens an issue when something drifts.

5.0 ships everything on feat/4.1-stageshow (4.1 never ships on its own) plus the phases below. Each phase lands on that branch as one PR with one review. 5.0.0 ships by merging the branch into main with docs/launch/release-5.0.0.md present; the release workflow tags it, and the owner uploads to the registries.

## The release bar

5.0.0 ships when every row holds. No row can be cut. Only the items on the cut line below can move to 5.1, and none of them is a row here.

| Claim | Measured by | Bar | Today (2026-11-12, bench v1 on this branch) |
|---|---|---|---|
| A rule that blocks is right | Per-rule precision on ux-bench, person-confirmed label sample | Precision at least 0.95, Wilson 95 lower bound at least 0.90, findings on at least 5 pages; at least 20 rules hold the tier | No rule qualifies yet; labels are model-made |
| The whole ruleset is right | Micro precision, dev and holdout | At least 0.90 on dev, holdout within 0.05 of dev | 0.80 (0.78 to 0.82) on dev |
| The engine finds faults | Recall on the seeded-defect set; recall on a 60-page subsample annotated in full by three raters | At least 0.95 on seeded faults, every miss filed; real-page recall reported | 0.92 on seeded faults (49 of 53); real pages not annotated |
| Same input, same output | Two runs per page; two machines per score | 0 pages differ; identical score | 3 of 53 pages differ (wall-clock timing) |
| It does not fall over | Corpus run and a malformed-input set | 0 crashes, 0 silent skips | 0 crashes on 53 pages; no malformed set yet |
| It leads to a product people can use | Method benchmark on six briefs | Method modes beat the plain engine on route coverage and walk pass rate; the control brief gains no artifact | Not built |
| Arabic is first class | Right-to-left twins and Arabic pages on the bench | Twin pages get the same verdicts; at least 30 right-to-left pages, 20 of them written in Arabic | 7 right-to-left pages |
| An agent follows the skill | Scripted grading of fixed tasks in two tools | Process conformance at least 0.90 | Not built |
| Every figure is checkable | Source-id test over references/ and data/ | 0 unsourced figures that are not marked house practice | Every listed correction applied; the full audit is open |
| It stays light | Tokens loaded per command, lint time per page | Budgets set from the Phase 2 measurement and held in release_checks | Not measured |
| It runs unattended | CI and the weekly canary | Zero skipped render tests; canary green twice | No canary |

## Where it stands

| Phase | State |
|---|---|
| 4.0.1 | Live on GitHub, PyPI and npm; 3.2.0 removed from both registries |
| 1. Benchmark | v1 built and rerun on this branch: 53 pages, 2,024 findings, every measured rule with a tier, seeded set, diff, ablation hook. Open: corpus to 200, a clean AI-built set, the person-confirmed sample |
| 3. Corrections | Every listed correction applied (contradicted guidance, platform-outdated rules, dark text keeps its weight, the rows the curriculum added). Open: the full citation audit and its test |
| Curriculum | Merged: 742 links in a ledger, 323 lessons, 85 proposed checks, 76 guidance items, 14 corrections |
| Inputs | Landed: eval, landscape, stability, method, curriculum, book library with acknowledgements |
| Everything else | Not started |

## Inputs

| Input | Where | What it gives |
|---|---|---|
| Evaluation method | research/5.0/eval.md | Fixture standard, precision tiers, corpus, labelling, taste test, drift tracking |
| Landscape and standards | research/5.0/landscape.md | 2026 AI tells, modern CSS, platform changes that retire rules, compliance dates |
| Running unattended | research/5.0/stability.md | Dependency risks, CI gaps, release hardening, versioning policy |
| The owner's product method | research/5.0/method.md | Personas, goals, every route to each goal, conceptual model, IA, flows with failure paths, prototyping inside the design system, walking every goal by every route, the one-page case. Method only, no client facts |
| The owner's craft rules | research/5.0/craft.md (written in Phase 8) | The taste and working rules behind the owner's shipped work, normalized: ranked rules with a check for each, the Arabic rules, the design-file habits, the pre-flight list. The dated evidence stays private |
| Curriculum (742 links) | research/curriculum/ | Lessons, proposed checks ranked, guidance by target file, corrections, and a ledger row per link; the raw reports stay in raw/ |
| Book library (96 books) | research/library/ | Lessons by topic (merged, weighted, no quotations, no names in lesson text), conflicts, measurable checks, gaps against the engine, corrections applied, acknowledgements |
| Benchmark v1 | bench/report.md | Per-rule precision and recall today, and six filed engine faults |
| 4.1 backlog | PLAN-4.1.md "Next, ranked" | Twelve ranked items; each is placed in a phase below |

Where two inputs disagree, the primary source wins; the conflict and its resolution go in research/curriculum/corrections.md. Where the owner's craft rules disagree with a source, both are kept: the source sets the default, the craft rule ships as a named house preference that a project can turn off.

## Principles for every phase

- **Measure before claiming.** A new rule starts advisory. It blocks only at precision of at least 0.95 with a Wilson 95 percent lower bound of at least 0.90, on a person-confirmed sample.
- **Users before screens.** Product work starts from personas, goals and every route to each goal. Screens mirror the site map and the flows. The engine teaches this order and checks it.
- **Judge by outcomes, not only by rules.** Every phase reports its effect on the benchmark: per-rule precision, recall on seeded faults, the method outcome scores and agent conformance. A guide or rule that moves none of them in two releases is trimmed or merged.
- **Prove on our own pages first.** Every render check runs over the site's pages before it ships.
- **A rule change never silently changes a score.** Reports carry the ruleset version and digest; `--ruleset` scores with an earlier minor's rules.
- **Arabic first, not mirrored.** Every check has a right-to-left fixture, every render check runs on a mirrored twin, and the generator writes Arabic as its own design.
- **Approved is locked.** Once a structure is approved, polish improves execution only. Structure changes are proposals, never silent edits.
- **A correction fixes the class.** One correction is recorded with before, after and why, then every other instance is found and fixed.
- **Real things only.** No drawn stand-in for a product, device, logo, photo or face. A missing asset is reported as a gap.
- **Rendered and looked at.** No command says done without a render at real size, in both themes and both directions, and a list of what was not looked at.
- **Nothing skipped silently.** What the engine cannot measure goes on an unmeasured list with the reason.
- **Light by default.** A single-role, single-goal project gets no extra artifacts. Each command loads only the guidance it needs.
- **The house rules hold:** looks are continuous functions of axes, brand and brief; pages use photographs; WCAG is cited only for what each criterion says; every error names the field and the fix; ASCII in new files; no client or vendor names in shipped docs.

## Order of work

Four stages. Each ends in a gate the benchmark can show, and a pre-release tag on GitHub if the owner agrees (registries carry only 5.0.0).

| Stage | Phases | Gate |
|---|---|---|
| A. Measure | 3 (the audit), 1 (to v2), 2, 4, and the CI items of 14 that every later phase leans on | Scores repeat across runs and machines; no rule blocks without a measured tier; modern CSS reads true |
| B. See and walk | 5, 6, 7 | Each new check has a measured row; the six method briefs run end to end; right-to-left twins agree |
| C. Craft and conduct | 8, 9, 10 | Pre-flight runs on our own pages; every missing-guide row is written or parked; agent conformance at least 0.90 |
| D. Prove and ship | 11, 12, 13, rest of 14, 15 | The release bar |

What depends on what: 2 before 5 (checks need the finding contract). 5 item 16 before 6 (the walk harness drives a running URL). 7 runs beside 5. 8 needs 2 and 6. 10 needs 6 and 8. 13 needs 5 to 8 landed, so the build it judges is the build that ships.

**The cut line.** If 5.0 is late, these move to 5.1 by name and nothing else does: the 1,000-page pool, the human taste round, the EN 301 549 and ADA Title II report formats, the DTCG resolver document, the AI interfaces pack (Phase 5 item 15, and with it the Article 50 heading in Phase 11), the design-files guide. Everything else in every phase is fixed.

## Phase 1. The benchmark (ux-bench)

Spec: eval.md A1, A2, A3, A4, A7 and A8. v1 is built; this phase now means v2.

Built in v1: bench/ with manifest, capture, run, report (precision, Wilson interval, tier per rule), diff between two engine versions, the seeded-defect set with near-miss twins, the ablation hook, two-pass labels with a tiebreak and Krippendorff alpha, the 50-finding sample script. 53 redistributable pages, every script stripped.

Left for v2:

- Recall on real pages: a 60-page subsample annotated in full by three raters, marked model-made where a model rated.
- Corpus to 200 pages: 50 generated from 10 fixed briefs by at least three tools that have never read this repository, 50 found AI-built, 100 designer-built from openly licensed sources. At least 60 percent redistributable; the rest stored as url, date, hash, findings and labels only. Split 140 dev and 60 holdout, page families kept together.
- At least 30 right-to-left pages, 20 written in Arabic (Phase 7).
- The owner confirms the 50-finding sample; until then every label is marked model-made and gates only demote.
- Usefulness labelled beside correctness: a true finding nobody would act on does not count toward a blocking tier.
- A larger pool of 1,000 to 2,000 pages for rules that fire rarely, labelled up to 60 findings per rule (cuttable).
- Each new check adds its fault and a near-miss twin to the seeded set.
- The ablation run: the engine with and without each guidance pack on the fixed briefs, so the report shows which guidance changes the output and which only adds weight.

**Exit:** report.md lists every rule with counts, precision, recall on the seeded set and tier, on 200 pages; every page gives the same findings twice; the sample is confirmed by a person; engine faults found on the corpus are fixed or filed in the report.

## Phase 2. The finding contract and score honesty

Spec: eval.md A2; stability.md changes 5 to 7; the faults filed in bench/report.md.

- `Finding` gains `outcome` (violation or review), `selector`, `viewport` and `page_type`. Render checks over images, gradients and video return review. Review findings never count toward the score.
- Excerpts show the match, not the first 200 characters of the line.
- Render timing runs on a virtual clock, so a control near a threshold gives the same answer on every run.
- The render pass blocks the network by default, uses Playwright's own Chromium, records browser and Playwright versions, and sets explicit timeouts. An image or font it blocked itself is unmeasured, not broken.
- Render failures leave the score and go to an "unmeasured" list.
- Rules apply by page type: a rule written for landing pages does not fire on a sign-in, settings, dashboard or article page.
- Two rules never count one fault twice; overlapping rules are merged or one defers to the other.
- Every lint report, MCP result and hook message carries `ruleset_version`, `ruleset_digest` and `score_formula`. `--ruleset <minor>` scores with that minor's rules.
- Rich output only on a terminal; piped output is valid JSON, with a test that pipes lint output through json.loads.
- Severity follows the measured tier from Phase 1. The rules with the highest false-positive rates are fixed first or demoted, with the reason in the rule's entry.
- A malformed-input set (broken HTML, half a stylesheet, a 5 MB line, mixed encodings) runs in CI; each case ends in a finding or a named error, never a traceback.
- The four seeded misses are closed in the rules that should have caught them: an image with a width and no height, a textarea named only by its placeholder, a transition with no property, an SVG image stretched out of shape.

**Exit:** the same page and ruleset give the same score on two machines; two runs of the corpus differ on 0 pages; no rule is blocking without a measured tier; lint and render time per page are in the report, and the budgets are set from them.

## Phase 3. Correct what the sources contradict

Spec: research/library/corrections-applied.md, research/curriculum/corrections.md, landscape.md recommendation 7. The corrections are applied and the curriculum is merged.

Left:

- Audit every number and citation in references/ and data/ against its source. A number with no source a reader could check is removed or marked as house practice.
- A test fails if a reference cites a source id that the ledger does not hold.

**Exit:** corrections.md and corrections-applied.md have no open or parked row (met); the source-id test is in CI.

## Phase 4. Read modern CSS

Spec: landscape.md recommendations 5 and 6.

- The CSS reader and the contrast gate resolve `light-dark()`, relative color, `color-mix()`, `contrast-color()`, nesting, `@scope`, `@layer` and style queries, or report them as unmeasured.
- A Baseline policy setting backed by a bundled, versioned copy of the web-features data. Suggestion-level "prefer the platform" rules: popover, invoker buttons, container queries, OKLCH, text-wrap balance, field-sizing, details-content, same-document view transitions. Anchor positioning is advised per property, not as one feature.
- Logical properties are read as their physical result in each direction, so every spacing and alignment check works on right-to-left pages.

**Exit:** a fixture set written only in modern CSS gets the same contrast verdicts as its hex twin, in both directions.

## Phase 5. New checks, each measured as it lands

Every check ships with the fixture standard (at least 3 fail, 3 near-miss pass, 1 inapplicable, 1 right-to-left pass), runs over the site's pages, runs on the benchmark, adds its fault to the seeded set, and starts advisory. Before a check is written, the existing rules and render checks are searched; where one already covers the fault it is tuned on the benchmark, not duplicated. Known overlaps to tune, not rebuild: template tokens (`placeholder-token-shipped`), eyebrows, capitals, equal card grids and link arrows (`eyebrows-over-budget`, `capitals-outside-system`, `three-equal-card-grid`, `cta-arrow-rightward-bouncing`), type-size drift (`size-outside-system`). The stored corpus pages carry no scripts, so the interact checks and `js-only-content` are measured on the seeded-defect apps and running-app fixtures, and the report says so. Ranked by impact on how well the page works and how un-generic it looks; the full ranked list with sources lives in research/curriculum/checks.md and research/library/checks.md.

Core set for 5.0:

1. `dead-click` (interact): an element that looks clickable does nothing within 500 ms. Covers cards and figures.
2. `form-submit-silent` (interact): submitting a form empty shows no error, alert or new text within 1 s.
3. `leaked-runtime-value` (render): visible "undefined", "NaN", "[object Object]", unrendered template tokens.
4. `font-synthesized` (render): a weight or style is shown that no loaded face provides.
5. `breaks-between-widths` (render): a cheap overflow and overlap sweep from 320 to 1440 px in 40 px steps.
6. Reflow at 320 px and text spacing (WCAG 1.4.10, 1.4.12), zoom to 200 percent (1.4.4).
7. Control edges at 3:1 against the ground beside them (1.4.11).
8. `disclosure-state-missing`: a button that shows or hides content without `aria-expanded` or `aria-pressed` (4.1.2).
9. The 2026 AI-default looks: cream with serif and terracotta, near-black with one acid accent, newspaper layout, uniform card kit, stock decoration (all-caps eyebrows, middle-dot meta lines, arrows appended to links). Each look is a combination of signals; no single trait (one accent, a serif, a dark ground) fires alone. The purple-gradient rules are demoted so avoiding purple alone no longer scores well.
10. Hierarchy: the largest first-screen text is the h1; one filled button per group; `heading-size-inversion`; `emphasis-over-budget`.
11. Reading measure and leading on body text; type-size drift; near-miss alignment and off-scale spacing.
12. `button-style-sprawl`: more than three looks for filled buttons. Tabular figures and right alignment in numeric table cells.
13. `permission-request-on-load`, `empty-state-dead-end`, `error-far-from-field`, `nav-wraps`, `mobile-columns-over-two`, `large-collection-no-finder`.
14. `internal-link-broken` (depth-one crawl) and `js-only-content` (render with scripts off).
15. AI interfaces (opt-in pack, cuttable): chat with no AI disclosure by first interaction, the "may make mistakes" note far from the input, more than one assistant launcher, generic progress text.
16. `lint --render --url` for running apps, and the complaint probes `task` and `reach`.

**Exit:** each core check that ships has its fixtures, its site run with zero false positives, and a measured row in bench/report.md or the seeded-app report.

## Phase 6. Method: users before screens

Spec: research/5.0/method.md. The engine learns the order real product work follows and checks each artifact, so a builder gets a product people can use, not only a page that lints clean. Runs after Phase 5 item 16.

The method, in order:

1. **Check what exists.** Audit the current build against how its shipped pages compose the kit, not only the component files. Reduce the spec to actors, jobs, objects, states, gaps and contradictions.
2. **Research mature tools for the same jobs.** How each leads a person to each kind of data; evidence strength recorded.
3. **Personas.** Who, the job, what they fear, what each may not see or do.
4. **Goals per persona,** every one of them, written as the job the person is trying to get done.
5. **The route matrix.** Every goal against every entry point (navigation, home, search, filters, tabs, links between records, report drill-down, deep link, notification), each marked must, should or not needed with a reason.
6. **Conceptual model, IA and site map.** Objects, relations, states and who acts next, what can be undone; page structure decisions with the rejected options; the site map and its indexes. The interface mirrors the model: one name per object, everywhere.
7. **Flows.** One shared rule set (undo, reasons, denied, stale, focus, keyboard), then every flow with its click count, decision points, failure paths and exits. Access is designed here: keyboard path, focus order, step count and recovery are part of the flow, not an audit on finished screens.
8. **Prototype inside the design system.** Compose the way the shipped pages compose; a missing piece widens the kit, never forks it.
9. **Walk every goal by every route as each persona.** At each step the walk asks what a first-time user would ask: will they try this, do they see the control, do they connect it to the goal, do they see progress after. Rough recordings, one per route; each route reached, trouble, blocked or missing. Rough is wanted; polish is waste.
10. **The one-page case,** decided by the standard where the standard answers, reviewed by the owner of the product before any screen is built. Then build, then walk the whole matrix again and list what was not walked.

No new command. `/ux-discover` gains a `method` mode (the router picks it for briefs with more than one role, or for admin, back office, portal and console projects); `/ux-design` gains a `structure` mode; `/ux-audit` gains a `walk` mode. CLI `uxskill method check|walk` and MCP `ux_method_check`, `ux_method_walk` mirror them. In a multi-role project, the page and dashboard modes stop with one line naming the missing site map and the mode that writes it. A single-role dashboard keeps its one-audience rule.

| # | Task | Done when |
|---|---|---|
| M1 | JSON Schemas for personas, goals, routes, model, sitemap, flows, walks and decisions under `engine/method/schemas/`; loader errors name the file, the path and the fix | a broken fixture per artifact gives one error per fault, each naming field and fix |
| M2 | Guidance: references/process/users-before-screens.md (the method, with its failure modes), references/foundations/navigation-ia.md, references/process/journeys-and-flows.md; dashboard.md gains a back-office section (home as role-scoped queues, numbers that open their rows, one sheet per pending item, saved views named by the work left, dense status-at-a-glance layouts for people who use the tool all day) | every IA and flow row marked missing guide in the gap lists is written or parked with a reason |
| M3 | `/ux-discover` method mode and router rule | the router picks method mode on the multi-role briefs and not on the single-role ones |
| M4 | `/ux-design` structure mode, with the compose-from-the-shipped-kit step: per pattern, the kit piece and its call site in the project's own pages, or a proposal to widen the kit | on the back-office brief every page in the site map lists its patterns with a call site or a widen proposal |
| M5 | Static checks, advisory, with the fixture standard: every must route lands on a site-map page and no page is orphaned; every flow has a failure path, a cancel exit, a success exit and a focus target; every goal has at least one must route; every waiting state shows in a queue; undo in flows matches the model | each check has fixtures and a measured row in the method report |
| M6 | Walk harness on a running URL: scripted and generated walks per persona, goal and route, recordings, statuses, and a weak-walk guard (a walk that also passes on the old build counts as weak) | two runs on one build give the same statuses; a seeded missing route is reported missing |
| M7 | Live checks on the harness, advisory: each number on home equals the rows its link opens; each role sees only its own navigation; a disabled action says who can do it; deep links round-trip; focus lands on a named target after an action; a confirm button names the action; a later build that adds clicks to a flow is flagged | each runs on the seeded-defect apps with precision and recall measured |
| M8 | Case page generated from the artifacts and walks, every finding linked to its recording and its screen by name | renders at 390 and 1280, light and dark, both directions |
| M9 | Method outcome benchmark in bench/method/: six fixed briefs (a back office with at least four staff roles and deadline-bound queues, a field team's role-switching mobile app, SaaS settings and billing, a two-role case-management tool, a single-owner shop dashboard as the control, a support desk), two of them bilingual; gold sets, three seeded-defect apps, a scoring script; each brief built with and without the method modes | bench/method/report.md gives goal recall, route coverage, flow completeness, walk pass rate, dead ends, role leakage, number-to-list parity, click cost against gold, and the added cost on the control brief |

**Exit:** the six briefs run end to end through method, structure, build and walk modes and produce a case page; the method modes beat the plain engine on route coverage and walk pass rate without adding weight to the control brief; every check is advisory with a measured row; gold sets are marked model-made until the owner confirms them; no client, vendor or person names in shipped files.

## Phase 7. Arabic and right to left, first class

Spec: the Arabic section of research/5.0/craft.md, written first in this phase and passed through the release gate before it is pushed; references/foundations/typography.md. Today four rules and thirteen lines in the foundation guides touch right to left. Most tools build Arabic as a mirrored afterthought; this phase makes it a design of its own. Runs beside Phase 5.

- **Guide:** references/foundations/arabic-rtl.md. Arabic is designed first and leads the layout. Mirror the glyph, not the container: direction arrows and progress swap; logos, media controls, clocks, digits and charts on a time axis do not. Never letter-space Arabic. Arabic sets a step larger than Latin at the same role, with more leading; display and body faces are separate roles; diacritics and descenders are checked at the real line height. Mixed-direction runs are isolated. An Arabic word is never split for a per-letter or per-word reveal. Copy is written in Arabic in the product's register, not translated line by line.
- **Brief and tokens:** the brief gains `languages`, `primary_language`, `digits` (one digit system per product) and `register`. The generator emits `dir` and `lang`, logical properties only, and a paired Arabic face per type role with its size and leading offsets as tokens.
- **Checks,** advisory, each with the fixture standard:
  1. `arabic-letter-spacing`: computed letter spacing other than zero on Arabic text. Extends the existing tracking rules to read the script.
  2. `arabic-face-fallback` (render): Arabic text drawn in a fallback face because the declared face did not load or lacks the glyphs. The check reads the rendered face, never the declaration.
  3. `physical-property-in-rtl`: left and right margins, padding, positions or text alignment on a page that serves a right-to-left language.
  4. `directional-icon-not-mirrored` and `mirrored-what-must-not`.
  5. `bidi-run-unisolated`: a phone number, address, code or user-entered string inside right-to-left text with no isolation.
  6. `mixed-digit-systems`: two digit systems on one page.
  7. `arabic-line-clipped` (render): body leading under the Arabic floor, or marks cut by the line box.
  8. `arabic-word-split`: an Arabic word wrapped in per-letter or per-word elements.
  9. `arabic-size-parity`: on a bilingual pair, Arabic body smaller than the Latin body role.
  10. `input-dir-missing`: a free-text input in a bilingual product with no automatic direction.
- **Parity:** every render check runs on a page and its mirrored twin and must give the same findings; a difference is a fault in the check.
- **Benchmark:** 30 right-to-left pages, 20 written in Arabic; three of the ten generator briefs and two of the six method briefs are Arabic or bilingual.

**Exit:** the guide is written with a source id or a house mark on every rule; each check has a measured row; the twin parity test is in CI; the generator's Arabic output for the three briefs passes all ten checks.

## Phase 8. Craft: the house taste, measured

Spec: research/5.0/craft.md, completed first in this phase from the owner's recorded rules (its Arabic section lands in Phase 7). It is normalized the way the book library was: rules and checks only, no client, project or person, no dated incidents. It passes the release gate before it is pushed. Where a craft rule is a preference and not a standard, it ships as a house rule a project can turn off, and it is labelled so in every finding.

**Checks,** advisory, measured like any other. Where a rule already exists it is tuned on the benchmark, not duplicated:

1. One accent: tune the existing `color-over-budget` so more than one accent hue outside the status colors is reported. Greys carry hierarchy.
2. `theme-role-unchanged`: a role that keeps one value in light and dark where its ground changes. Every render check runs in both themes.
3. `proximity-inverted`: items inside a group sit further apart than the group sits from its neighbour.
4. `badge-acts` and `action-looks-like-badge`: a state chip that is clickable, or a control drawn as a chip. Target size stays with the existing `target-too-small` (24 px, WCAG 2.5.8); 44 px is reported as the house target for touch.
5. `effect-clipped`: a shadow, glow, chip or badge cut by an ancestor's overflow. Built on the existing `focus-ring-clipped`.
6. `logo-as-text`: the brand is typed while the brief supplies a mark.
7. `drawn-stand-in`: a device frame built from styled boxes, or an image the asset manifest does not hold. Runs only when the project has an asset manifest.
8. `figure-not-in-facts`: a statistic, customer count, rating or testimonial name in marketing copy that the brief's facts file does not hold. Runs only when the brief has a facts file; dates, prices and contact details are out of scope.
9. `reveal-delays-reading`: a blanket fade on every section, or text that is not readable within its budget after it enters the view.
10. `state-snaps`: an interactive state that changes instantly while the same component's other states transition.
11. Repeated sections: tune the existing `layout-family-repeated` and `split-sections-in-a-row`.

**Working practices,** built into the commands:

- **Approved is locked.** `uxskill baseline lock` records the approved structure: section order, headings, navigation, flow steps and tokens. `baseline diff` reports drift. `/ux-polish` and `/ux-fix` change execution only; a structure change comes back as a proposal.
- **A correction fixes the class.** A correction is recorded in the existing decision ledger (`.ux/decisions.jsonl`) with before, after, why and scope. Every later command reads it. `uxskill decisions audit` finds the remaining instances. A rejected option never returns.
- **Open questions are asked.** When two recorded decisions conflict, the command stops, shows both, and records the answer. It does not guess.
- **References first.** `/ux-design` gathers references before generating and records which style, layout, motion and interaction choices come from references and which belong to the product. It shows a few reference-backed directions before converging.
- **Real things only.** An asset manifest holds the source and licence of every logo, photo, device frame and screen. A missing asset is named in the output as a gap.
- **Meaning before geometry.** `/ux-critique` opens with a cold read: a reader with no context states the takeaway in one sentence, and the command compares it with the brief's. Each image is judged with its real title on it.
- **Computed, then checked by eye.** Proportions are shown with their maths, then rendered at real size and compared for optical weight. The report says which one decided.
- **Platform conventions first.** The system keyboard, navigation and sheets before a kit; a proven kit before bespoke. Locked at intake.
- **The deliverable is a page.** Audits, cases and findings render as a designed page with a link and a name for every screen, never a raw file or a bare id.
- **Pre-flight.** `uxskill preflight` runs the craft checklist before anything is shown. Each line comes back pass, fail or not checked, with its evidence.

**Design files** (cuttable): references/process/design-files.md. Auto layout everywhere; layer names that match the code components; radius and color bound to variables; spacing as named objects; numbered pages behind a cover; light and dark as one collection; both languages as pages; archive, never delete. Applied design outranks the document: `uxskill system drift` compares the tokens in code, DESIGN.md and exported design-file variables, reports the drift and never overwrites the applied one.

**Exit:** craft.md is public and passed the gate; each check has a measured row; pre-flight runs clean on the site's pages; `baseline diff` catches a seeded structure change; `decisions audit` finds a seeded repeat.

## Phase 9. Guidance that teaches

Spec: research/curriculum/guidance.md, research/library/topics/ and gaps.md (rows marked missing guide: 48 in the research cluster alone).

- New files: references/foundations/voice-and-multimodal.md, references/surfaces/portfolio.md, references/surfaces/checkout.md, references/process/design-sprint.md, references/process/personas-and-journeys.md (personas from clustered research, one primary per interface, proto-personas labelled as hypotheses, journey maps and service blueprints).
- Additions: ai-interfaces.md (process versus result, agent control levels, repair moves, one AI marker, the error types), color.md (harmony models and the seven contrasts), dashboard.md (chart rules: data ink, direct labels, no dual axes, sorted bars, small multiples), components (toasts that hold an action wait; view modes, selection, mass actions, filters and search for collections; loading states by wait length), /ux-research (sample sizes computed, SUS scoring, pilots, task wording, survey hygiene, inclusive recruitment, no synthetic users in place of participants), /ux-audit as independent passes with severity factors and stable finding ids.
- An optional component tier in tokens.css from the contracts, so one component can be restyled without touching a role.
- Every claim carries a source id from the curriculum ledger or the library, or a house mark. Book lessons ship normalized: rewritten, merged across books, no quotations and no person names in the text.
- Navigation, IA and flows are written in Phase 6; Arabic in Phase 7; craft in Phase 8.

**Exit:** every missing-guide row in both gap lists is written or parked with a reason; the ablation run shows each new guide changes the output on at least one brief.

## Phase 10. The skill an agent follows

A guide nobody loads and a rule the agent skips are worth nothing. This phase measures whether an agent using ux-skill does the right things in the right order.

- **Router and surface.** One router SKILL.md, manifests generated from one source, a smaller MCP surface with each tool's shape documented.
- **Context budget.** Tokens loaded per command are measured and capped in release_checks. References are split so a command loads the sections it needs.
- **Instructions that verify.** Every "must" in a command maps to a tool call that checks it, or it is removed.
- **Hooks.** The hook reports only findings that are new since the baseline, and is rate-limited.
- **Errors.** A test walks every error the engine can raise and fails on one that does not name the field and the fix.
- **Conformance benchmark** in bench/agent/: twelve fixed tasks (a landing page from a brief, an Arabic landing page, a multi-role back office, a single-role dashboard, fix a failing lint report, polish against a locked baseline, audit a running app, a component in an existing system, a copy pass, a system from a brand, a correction that must fix its class, a brief with a missing asset). Each runs headless in at least two agent tools. A script grades the transcript and the output on process: the right mode was chosen; no screen before the site map on multi-role work; the render check ran before the done claim; findings carry sources; no figure outside the facts file; the baseline held in polish; the missing asset was reported, not drawn. A model judge is a pre-filter only.

**Exit:** conformance at least 0.90 across both tools, with every failed step filed; the context budget holds; the engine still never calls a model and never touches the network unless asked, with a test for each.

## Phase 11. Compliance evidence

Spec: landscape.md recommendations 2, 3 and 10.

- `uxskill audit --standard wcag22-aa` writes a dated, reproducible report: ruleset and data versions, the criteria measured, the findings per criterion, and the criteria that still need a person, listed by name. `en301549-4.1.1` and `ada-title-ii` are the same report under their own clause maps (cuttable).
- If the AI interfaces pack ships, its AI Act Article 50 findings report under their own heading with the dates they rest on.

**Exit:** the report for the site's own pages lists every WCAG 2.2 AA criterion as measured, needs a person, or not applicable, and nothing is claimed beyond what each criterion says.

## Phase 12. Interop

Spec: landscape.md recommendation 8.

- Read and write DESIGN.md; the 160 brand specs validate as DESIGN.md files.
- SARIF output and GitHub annotations from lint; stable exit codes documented.
- Emit the DTCG resolver document (2025.10) for the five mode axes (cuttable).

**Exit:** round trips through DESIGN.md with no mismatch, in release_checks.

## Phase 13. The taste test

Spec: eval.md A5 and A6. Runs last among the build phases, so it judges the build that ships.

- 30 briefs with fixed copy, six of them Arabic; each built with and without ux-skill by the same tool; screenshots at 1280 and 390.
- The harness randomises sides, repeats pairs and seeds gold pairs, and computes a Bradley-Terry estimate with bootstrap intervals.
- A model judge runs only as a pre-filter: both orders, consistent verdicts only, agreement with humans checked on gold pairs before any use. Its result is published as model-judged and never as the headline.
- The human round kit (rater instructions, the pair set, the analysis script) ships in bench/taste/ so a designer panel can run it. The round itself is cuttable.

**Exit:** the harness, the pair set and the model-judged pre-filter result are in the repo; the release notes say plainly that the human round is pending if it has not run.

## Phase 14. Running unattended

Spec: stability.md sections 1 to 5. The CI items land in stage A.

- **CI (stage A).** test.yml on Python 3.11 to 3.15 on a pinned runner image; a Playwright job that installs Chromium and fails if any render test is skipped; an MCP stdio test; a Windows job for the hook and the npm wrapper; the malformed-input set; a tested constraints file used by every leg; actions pinned by commit with least privilege per job. The twin parity test joins in stage B.
- **Release.** release.yml runs only after tests pass on the same commit; builds once; attaches an SBOM; publishes the GitHub release from a draft; every step is safe to re-run. After a release, a job compares the version on GitHub, PyPI and npm and opens an issue when they differ.
- **Registries.** Trusted publishing to PyPI and npm (no stored tokens) is written but switched off until the owner turns it on. Until then the owner uploads by hand and nothing is published without an explicit yes.
- **Packaging.** SPDX license, capped build backend, `requires-python >=3.11`, `playwright>=1.63,<2`, the missing image extra. The package summary and every README figure are generated from `uxskill stats`, with a test.
- **Dependencies.** dependabot ignores majors for mcp and playwright, with cooldowns and grouped updates.
- **Canary.** Weekly, against the latest dependencies, the frozen corpus, the method benchmark and the twin parity test. It opens or updates one issue on drift and closes it when green.
- **Hooks, wrapper and MCP.** The hook launcher tries `UXSKILL_PYTHON`, python3, python and `py -3`; MultiEdit leaves the matcher. The npm wrapper finds the right Python and says why an install failed. Install hints fit the environment that runs the check. The MCP server checks its SDK and names the installed version and the right pin when it cannot start. The installer stops writing a stub plugin file into user projects.
- **Plugin and repository.** The plugin manifest is validated strictly in the canary and its stale descriptions are fixed. Immutable releases, branch protection on main and private vulnerability reporting are switched on by the owner.
- **Breaking layout changes, possible only in a major** (owner decision in stage A, stability.md changes 16 and 17): move the plugin to a subdirectory, and rename the import package from `engine` to `uxskill` with `data/` inside it. If declined, both are recorded as declined for the 5.x line.
- **Policy** in CONTRIBUTING.md: what semver covers (CLI flags, MCP tool names and shapes, token names, exit codes, rule ids, method schemas), deprecation windows, rule and score versioning.
- **The release gate in CI.** A leak scan of the source and of the unpacked wheel, sdist and npm tarball runs on every PR and before every release.

**Exit:** a fresh clone passes CI with zero skipped render tests; the canary has run green twice; the policy is written.

## Phase 15. Release 5.0.0

- Remove the seven 4.0 command aliases (they were due in 4.1).
- Migration guide docs/migrating-to-5.md; release notes docs/launch/release-5.0.0.md; CHANGELOG; README and the 16 translations, the Arabic one written, not translated; site figures regenerated; compare page refreshed with current facts; the precision report, the method report and the conformance report published as pages.
- Full suite clean, release_checks clean, every row of the release bar filled with its measured value.
- Merge feat/4.1-stageshow into main; the release workflow tags v5.0.0 and publishes the GitHub release; the owner uploads to PyPI and npm.
- Seen, not assumed: the GitHub release, the PyPI page, the npm page and the site are each opened and read after the upload.

**Exit:** v5.0.0 exists on GitHub, PyPI and npm with the same version, notes, the three reports and the SBOM; main is green; the canary is scheduled.

## Risks

| Risk | Likelihood | Answer |
|---|---|---|
| The plan never closes: fifteen phases, one maintainer | high | Four stage gates with a pre-release each; the cut line is fixed above; a phase's PR is the unit of done |
| Model-made labels flatter the engine | high | Labels marked model-made; gates only demote until the owner confirms the sample; usefulness labelled beside correctness |
| The AI-built pages were made by a tool that had read this repository | certain in v1 | v2 generates with tools that never read it, three tools per brief |
| House taste shipped as if it were a standard | medium | Every craft finding is labelled house rule and can be turned off; standards cite their criterion |
| The method adds weight to small projects | medium | The control brief measures added artifacts; method mode triggers only on multi-role or back-office briefs |
| Generated walks guess selectors and report noise | medium | Scripted walks decide gates; generated walks are advisory; the weak-walk guard |
| Arabic checks tuned on mirrored English | medium | 20 pages written in Arabic; twin parity is a test of the check, not of the page |
| Private material reaches the public repo | medium | The release gate on every push and upload; craft.md and method.md carry rules only |
| Agent runs cost more than they return | medium | At most two agents at a time; one review per PR; conformance and taste runs are capped batches the owner approves |
| Dependency or browser drift breaks a release nobody is watching | medium | Pinned ranges, the canary, the version-compare job |

## Who does what

- One working session at a time carries a phase from plan to PR, with at most two agents and one fresh review per PR. Opus-class models for anything with judgment.
- Every push, release and registry upload passes the release gate first: a leak and confidentiality scan of the source and of the unpacked artifacts. Nothing private, no client facts, no book text.
- Owner decisions, the only ones left: confirm the 50-finding label sample; confirm the gold sets for the six method briefs; read craft.md before it goes public; agree or decline the pre-release tags; decide the two breaking layout changes; approve each capped batch of agent runs; run or skip the human taste round; turn on registry publishing; say yes to 5.0.0.
