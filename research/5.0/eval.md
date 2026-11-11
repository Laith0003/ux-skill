# ux-skill 5.0: how to evaluate the linter and the generator

Research notes for the 5.0 plan. Written 2026-11-02. Scope: measuring precision and recall
for each of the roughly 180 lint and render rules, building a benchmark corpus of about 200
pages, a labelling protocol, a blind taste evaluation of generated pages, and regression
protection.

What ux-skill has today (read from the repo, not changed):

- `data/anti-patterns.json`: 171 entries. Severities: 6 critical, 56 high, 79 medium,
  30 low. Categories: A11y 45, Content 35, Layout 18, Typography 16, Motion 14, Visual 14,
  Quality 12, Color 10, Performance 5, Depth 2. Plus the render checks in
  `engine/render/core.py`, `interact.py` and `taste.py`.
- `tests/test_lint_corpus.py`: one dirty fixture per rule (`tests/lint_corpus/dirty/<rule-id>.<ext>`)
  that must fire, plus a shared `clean/` set on which nothing at medium or above may fire.
  `tests/lint_corpus/cases/` has pass/fail pairs for 42 rules. `tests/test_lint_precision.py`
  holds hand-written false positive regressions.
- `engine.linter.core.Finding` has a rule, severity, file, line and excerpt. There is no
  "needs review" outcome, no selector or viewport field, and no confidence.
- No precision or recall has been measured on real pages, and no generated page has been
  judged blind.

So the gap is not unit tests. It is (a) element level fixtures with near-miss negatives
for every rule, (b) a labelled corpus of real pages, (c) per-rule numbers with intervals,
(d) a gate that ties a rule's severity to its measured precision, and (e) a blind human
judgement of the generator.

* * *

## Part A. Recommendations for 5.0

### A1. A per-rule fixture standard (ACT style), enforced by a meta-test

Every rule, static or render, gets a folder `tests/rules/<rule-id>/` holding:

- `rule.md`: plain-language applicability (which elements are tested), expectation (what
  must be true), assumptions, and the WCAG or design source it maps to. This is the ACT
  Rules Format structure, and it doubles as the labelling guide in A4.
- `examples.html` (or `.css`, `.tsx`): elements carrying ids `fail1..n`, `pass1..n`,
  `inapplicable1..n`, `canttell1..n`.
- `expected.json`: `{"rule": "...", "violations": [["#fail1"], ...], "passes": [...],
  "inapplicable": [...], "incomplete": [...], "viewports": [390, 1280]}`. This is the axe-core
  integration fixture shape (`test/integration/rules/<rule>/<rule>.html` plus `.json`).
- For source-only rules where ids are awkward, Semgrep style inline annotations instead:
  a comment `ruleid: <id>` before a line that must fire, `ok: <id>` before a line that must
  not, and `todoruleid` / `todook` for known misses and known false positives, which are
  reported but do not fail the build.

Minimums, checked by a meta-test that fails CI if any rule is short:

| Example type   | Minimum | Purpose                                                          |
|----------------|---------|------------------------------------------------------------------|
| fail           | 3       | different syntaxes: inline style, stylesheet, utility class, JSX |
| pass           | 3       | near misses that look like the pattern but are fine              |
| inapplicable   | 1       | content the rule must not even consider                          |
| canttell       | 0, or 1 if the rule can return "needs review"                     |
| RTL / Arabic   | 1 pass  | the repo's existing promise                                      |

Each `todook` counts as a known false positive and must link an issue. A rule with an open
`todook` cannot be in the blocking tier (A2).

### A2. Tie severity to measured precision (three tiers plus "needs review")

Adopt the Google Tricorder model, which is the clearest published policy: checks that break
the build must have no effective false positives; checks shown in review may have up to
10%, and an analyzer whose "not useful" rate goes above 10% is switched off until fixed.
Adopt axe-core's split between a violation and "incomplete" (needs review): when the rule
cannot be sure, it says so and the finding does not count.

| Tier      | Maps to ux-skill        | Counts in score / CI exit | Gate on the labelled corpus                                                       |
|-----------|-------------------------|---------------------------|-----------------------------------------------------------------------------------|
| blocking  | critical, high          | yes                       | precision >= 0.95 and Wilson 95% lower bound >= 0.90; no open `todook`            |
| advisory  | medium                  | yes, lower weight         | precision >= 0.90 and Wilson lower bound >= 0.75                                  |
| info      | low                     | no                        | precision >= 0.75, or not yet measured                                            |
| review    | new outcome             | no                        | the rule ran but could not decide (gradient behind text, image ground, etc.)      |

What the bounds mean in counts (Wilson, 95%):

| Labelled findings | False positives | Precision | Wilson 95% interval | Enough for blocking? |
|-------------------|-----------------|-----------|---------------------|----------------------|
| 10                | 0               | 1.00      | 0.72 to 1.00        | no                   |
| 20                | 0               | 1.00      | 0.84 to 1.00        | no                   |
| 35                | 0               | 1.00      | 0.90 to 1.00        | yes (minimum)        |
| 53                | 1               | 0.98      | 0.90 to 1.00        | yes (minimum)        |
| 69                | 2               | 0.97      | 0.90 to 0.99        | yes (minimum)        |
| 50                | 5               | 0.90      | 0.79 to 0.96        | advisory only        |
| 20                | 2               | 0.90      | 0.70 to 0.97        | info until more data |

So a rule needs at least 35 labelled true findings with zero false positives (or 53 with
one) before it can block. Rules that cannot reach that count on the corpus stay advisory
and are marked "unmeasured" in the report, not silently promoted.

Add an `outcome` field to `Finding` (`violation` or `review`) and a `selector` and
`viewport` field so findings can be matched to labels and to `expected.json`. Render rules
that sample colors over images, gradients or video (contrast as seen, occlusion) should
return `review` when the ground is not uniform, as axe-core's color-contrast does with its
`incomplete` list.

Report two precisions per rule, because ux-skill mixes objective rules with taste rules:

- detection precision: the condition the rule describes is really present (objective;
  applies to every rule);
- usefulness precision: a competent designer would change it (Tricorder's "effective false
  positive"; matters most for the Content, Visual and Typography rules such as
  `inter-as-display`).

Blocking requires both to pass.

### A3. Benchmark corpus "ux-bench": 200 pages, frozen, licence-aware

Composition (200 pages, stratified):

| Half           | Source                                                                     | Pages | Storage class |
|----------------|----------------------------------------------------------------------------|-------|---------------|
| AI-built       | Generated by us: 5 AI coding tools or builders x 10 fixed briefs, without ux-skill | 50 | A (full)  |
| AI-built       | Generated by us: same 10 briefs with ux-skill (also feeds A5)              | 0 to 20, kept apart from the lint test set | A |
| AI-built       | Found in the wild (public "made with X" galleries, Show HN launches)       | 50    | B (derived only) |
| Designer-built | Openly licensed: GOV.UK and other OGL sites, US federal sites (public domain), CC BY templates (HTML5 UP), MIT-licensed open source project sites and design-system docs | 40 | A |
| Designer-built | Commissioned or donated by designers under CC BY 4.0, with written consent | 20 to 40 | A |
| Designer-built | Notable live sites sampled from the Tranco top list by category            | 20 to 40 | B |

Aim for at least 60% of pages in class A so the benchmark can be re-run by anyone. Cover
landing, dashboard, docs, e-commerce, form-heavy and article pages, and at least 15 RTL
pages (Arabic), because the engine promises RTL.

Storage classes:

- Class A (redistributable): keep the full snapshot (WARC or single-file HTML with inlined
  assets), screenshots, and labels in a separate dataset repo, with a `LICENSE` and
  attribution per page. Strip logos and crests where the licence excludes them (OGL v3
  excludes departmental logos and third-party rights).
- Class B (not redistributable): publish only the URL, capture timestamp, a public archive
  link (Wayback) if one exists, SHA-256 of the private snapshot, the extracted measurements,
  findings and labels. Keep the snapshot private for re-runs; do not ship it in the repo or
  the PyPI package. Rely on text-and-data-mining exceptions only where they apply (EU DSM
  Directive art. 3 and 4, with machine-readable opt-outs respected) and get legal advice
  before any commercial use.
- Never publish personal data seen on pages; blur faces and names in screenshots that are
  published.

Freezing and reproducibility:

- Capture with a browser crawler that writes WARC (ISO 28500), such as
  `webrecorder/browsertrix-crawler`, or SingleFile for single pages; replay offline (pywb, or
  Playwright routing from a HAR) with the network blocked.
- Pin the Chromium build, the font set, the device scale factor, timezone, locale and
  `Math.random`/`Date` seeds; render each page twice and require identical findings before
  a page enters the golden set (Playwright's own docs warn that rendering varies by host OS,
  version, settings and hardware).
- One `manifest.json` row per page: id, half, source, storage class, licence, attribution,
  URL, capture date, sha256, framework, page type, direction, and for AI pages the tool,
  model, version, date and the exact prompt.
- Split 140 dev / 60 held out. Rule authors only look at the dev split. The held-out split
  is scored once per release. Refresh about a third of the AI-built half every year,
  because AI output styles move quickly.

Extend precision with a cheap larger pool: precision only needs findings labelled, not whole
pages, so for rules that fire rarely, run the linter over 1,000 to 2,000 extra class B pages
(Tranco or HTTP Archive URLs) and label a random sample of up to 60 findings per rule. Recall
needs exhaustive annotation and stays on the 200-page core (A4).

### A4. Labelling protocol

Two tasks, run by different people where possible.

Task 1, precision (finding adjudication):

- Every finding from every rule on the corpus (and the sampled pool) is shown to 2 raters
  independently: page screenshot at the finding's viewport, highlighted element, the
  `rule.md` text, and the excerpt. Raters do not see the severity.
- Labels: `TP` (condition present), `FP` (not present), `cantTell`; and for TPs a usefulness
  label (`would fix` / `would not fix`) and a Nielsen severity 0 to 4.
- Disagreements go to a third rater (adjudicator). Keep both original labels in the data.
- Rough cost: 200 pages x about 15 findings = 3,000 findings; at about 30 seconds per
  finding per rater, 2 raters is about 50 hours.

Task 2, recall (exhaustive problem annotation):

- A stratified 60-page subsample (30 AI, 30 designer). 3 raters each annotate every problem
  they see, before seeing any tool output, by drawing a box and choosing a category from the
  rule taxonomy or "other". Nielsen recommends 3 to 5 independent evaluators because any one
  evaluator misses problems, and the mean of 3 severity ratings as good enough.
- A problem counts as ground truth when 2 of 3 raters mark it, or the adjudicator confirms
  it. Single-rater problems are kept as a separate "possible" set.
- Rough cost: 60 pages x 3 raters x 30 minutes = 90 hours.

Raters: at least one with accessibility auditing experience (for A11y rules) and two
working product designers (for taste rules). Run a calibration round on 10 dev pages, revise
`rule.md` wording where raters split, then start.

Agreement, reported per rule and per category:

- Krippendorff's alpha (nominal for TP/FP, ordinal for severity), with a bootstrap interval.
  alpha >= 0.80: use the labels. 0.667 to 0.80: report as tentative. Below 0.667: the rule's
  definition is ambiguous; rewrite `rule.md` and relabel before trusting its precision.
- Also report positive specific agreement, because kappa and alpha drop sharply when
  positives are rare ("high agreement but low kappa"), which is exactly the case for most
  rules on most pages. Cohen's kappa is fine for the 2-rater precision task but alpha
  handles 3 raters and missing labels.
- Expect low raw agreement on the recall task: across usability studies, any-two evaluator
  agreement has a median around 27%. That is why recall uses 2-of-3 consensus.

Metrics:

- Precision per rule = TP / (TP + FP) at the element level, `cantTell` excluded and counted
  separately. Wilson 95% interval (recommended by Brown, Cai and DasGupta for small n;
  Jeffreys is an acceptable alternative). With zero events, quote the interval, not "100%".
- Recall per rule = consensus problems of that rule's category that the rule found /
  all consensus problems of that category on the 60 pages. Most rules will have small
  counts; report recall per category and per rule only when n >= 10.
- Aggregate precision and recall: micro and macro over rules, with intervals from a
  bootstrap that resamples pages (findings on one page are correlated).
- Also report "problems no rule covers" from the "other" bucket; that is the roadmap for
  new rules.

### A5. Blind taste evaluation of the generator

Design:

- 30 briefs spanning industries, page types, LTR and RTL. Fix the copy for each brief (one
  shared copy deck) so raters judge design, not writing.
- Conditions: (A) the same AI coding tool with ux-skill, (B) the same tool without it.
  Optional: (C) a competing design plugin, (D) a human designer's page for 10 of the
  briefs as a ceiling.
- Render all pages through the same frozen pipeline at 1280 and 390 widths; strip anything
  that names the tool (comments, meta generator, class prefixes do not show in screenshots,
  but visible watermarks and favicons must go).
- Task: side by side, "Which page is better designed for this brief?" with a "no
  preference" option, plus three secondary questions (fits the brief, clear hierarchy,
  trustworthy). Optionally an interactive variant where raters scroll both pages.

Bias controls:

- Randomise left/right per trial and counterbalance so every pair is shown in both orders
  across raters; randomise trial order; cap at about 40 trials per rater per session.
- Hide condition identity everywhere; check after the session whether raters could guess
  the condition (if they can, blinding failed; report it).
- Quality checks: 10% repeated pairs (consistency), 5% gold pairs where one page has an
  injected defect (overflow, broken image), and a minimum time per trial.

Raters and sample size:

- Two panels, analysed separately: 12 to 20 professional designers (screened by portfolio,
  paid), and 60 to 100 crowd raters (Prolific or similar, with approval rate and attention
  screens; Design2Code used Prolific with more than 2,500 completed studies and a 98% pass
  rate, 5 raters per pair, and got Fleiss' kappa 0.46).
- Non-tied judgments needed for a win rate:

| Goal                                              | Non-tied judgments |
|---------------------------------------------------|--------------------|
| win rate within +/- 10 points (95%)               | 96                 |
| win rate within +/- 7 points                      | 196                |
| win rate within +/- 5 points                      | 384                |
| detect 60% vs 50% (two-sided 0.05, 80% power)     | 194                |
| detect 65% vs 50%                                 | 85                 |
| detect 55% vs 50%                                 | 783                |

  Judgments are clustered by rater and brief, so inflate by a design effect (plan about
  1.5x to 2x): target 400 to 600 judgments per comparison per panel, e.g. 30 briefs x 2
  widths x 5 to 8 raters per pair.
- Analysis: preregister (hypothesis, primary question, exclusion rules, analysis) before
  data collection. Primary metric: win rate of A over B with ties excluded, Wilson interval,
  and a mixed-effects logistic model with random intercepts for rater and brief. For more
  than two conditions, fit Bradley-Terry with bootstrap intervals resampled by brief (the
  Chatbot Arena method; Design Arena uses Bradley-Terry with Wilson intervals on win rates).
  Do not rank conditions whose intervals overlap.
- 5.0 claim threshold: among designers, A beats B in at least 60% of non-tied judgments with
  the 95% lower bound above 50%, on both widths. Publish raw votes, screenshots (class A),
  briefs and the analysis script.

### A6. LLM-as-judge: pre-filter only, never the reported number

ux-skill is offline and LLM-free, so this only concerns the research harness.

- Allowed: triage (flag broken renders, empty pages, obvious layout breaks) before human
  rounds; a cheap nightly alarm that compares generator output against the last release.
- Required if used: run both orders and keep only order-consistent verdicts; never let the
  same model family judge its own output; validate against a human-labelled gold set of at
  least 100 pairs from A5, and use the judge only if order-consistent agreement with the
  human majority is at least 75% and the order-flip rate is below 10%.
- Why: on 300 real A/B-tested UI pairs (WiserUI-Bench), order-consistent accuracy of current
  MLLMs was 15% to 35% against a 25% random baseline, with strong second-position bias (o1
  picked the winner 98% of the time when it was second and 17% when it was first). On 30 UIs
  rated by 500 people, MLLM pairwise agreement with humans was about 60%, near chance when
  the human difference was small, and near chance on "ease of use". UIClip's authors report
  GPT-4V preferring a screenshot with overflowing text over the original. Model-level ranking
  agreement can be high (ArtifactsBench reports 94.4% ranking consistency with WebDev Arena)
  but that is an aggregate over many tasks, not a per-page verdict.

### A7. Regression protection

1. Golden findings on the corpus: `bench/expected/<page-id>.json` holds every finding as
   (rule, selector, viewport, outcome). CI runs the engine over the frozen corpus on every
   PR, diffs against the base branch, and posts "new findings / disappeared findings by rule"
   as a PR comment. This is how Ruff (ecosystem check), mypy and typeshed (mypy_primer) and
   Clippy (lintcheck) protect their rules: run old and new versions over a fixed corpus of
   real code and review the diff. Accepted changes update the goldens with an explicit
   command, never automatically.
2. Unlabelled findings block blocking-tier rules: if a PR makes a blocking rule emit a
   finding that has no label, the PR needs a label (TP/FP) for it before merge. New FP on a
   blocking rule fails CI.
3. Drift tracking: append per-rule TP, FP, cantTell, precision and interval to
   `bench/history.jsonl` at each release. Demote a rule automatically to advisory if its
   Wilson lower bound falls below the tier threshold, or if it gains 3 or more FPs since the
   last release. Publish the history as a page.
4. Mutation testing of rule code: run mutmut over `engine/linter` and `engine/render` against
   the per-rule fixtures. Target a mutation score of at least 80% on rule modules; a
   surviving mutant in a blocking rule means a missing fixture.
5. Metamorphic tests of fixtures (Statfier style): apply transforms that must not change
   findings (reorder attributes, minify, rename classes, hex to rgb, inline to external CSS,
   add a wrapper div, swap LTR for RTL where direction is irrelevant) and transforms that must
   (drop alt text, lower contrast, shrink a target below 24px). Statfier found 79 bugs (46
   confirmed) in five popular static analyzers this way.
6. Render determinism: render each corpus page twice per CI run; any difference is a flake,
   reported separately and excluded from the diff until fixed. Pin the browser and fonts;
   upgrade them only in a dedicated PR that reviews the full diff.

### A8. Publish a per-rule precision report

A generated page per release, modelled on W3C ACT implementation reports (which list each
rule's examples and the tool's outcome, and label each tool's rule as consistent or
partially consistent). Columns:

| Rule | Tier | Fixtures fail/pass/inapp | Corpus findings | TP | FP | cantTell | Precision | Wilson 95% | Usefulness | Recall (n) | alpha | Measured in |
|------|------|--------------------------|-----------------|----|----|----------|-----------|------------|------------|------------|-------|-------------|
| `color-contrast-as-seen` (example) | blocking | 6/8/2 | 212 | 201 | 3 | 8 | 0.985 | 0.96 to 1.00 | 0.97 | 0.81 (42) | 0.86 | 5.0.0 |
| `inter-as-display` (example) | advisory | 3/4/1 | 41 | 38 | 3 | 0 | 0.93 | 0.80 to 0.97 | 0.71 | n/a | 0.72 | 5.0.0 |

(Numbers in these rows are placeholders to show the shape.)

Summary of numbers to adopt:

- per-rule fixtures: >= 3 fail, >= 3 near-miss pass, >= 1 inapplicable;
- blocking tier: precision >= 0.95 and Wilson lower bound >= 0.90 (>= 35 TP with 0 FP);
- advisory: >= 0.90 and lower bound >= 0.75; otherwise info or review;
- corpus: 200 pages, 100 AI / 100 designer, >= 60% redistributable, 140 dev / 60 held out;
- labelling: 2 raters plus adjudicator for findings; 3 raters on a 60-page recall subsample;
  alpha >= 0.80 to trust, 0.667 to 0.80 tentative;
- taste: 30 briefs, 400 to 600 judgments per comparison per panel, claim at >= 60% win with
  lower bound > 50%;
- LLM judge: both orders, >= 75% agreement with humans on >= 100 gold pairs, pre-filter only;
- regression: corpus diff on every PR, history per release, mutation score >= 80%.

* * *

## Part B. Evidence by question

### B1. How mature rule engines measure and protect precision

axe-core (Deque)

- The README states a manifesto point that axe "returns zero false positives (bugs
  notwithstanding)" and claims it finds "on average 57% of WCAG issues automatically";
  results that need a human are returned as "incomplete".
  https://github.com/dequelabs/axe-core
- The rule proposal guide: a new rule "must have no false positives", and must follow Deque's
  interpretation of WCAG. https://github.com/dequelabs/axe-core/blob/develop/doc/rule-proposal.md
- Result types: violations, passes, inapplicable, and incomplete ("Also known as 'needs
  review'"). Experimental rules are tagged `experimental` and disabled by default, which is a
  staging tier for unproven rules. https://github.com/dequelabs/axe-core/blob/develop/doc/API.md
- A check returns true, false or undefined; undefined lands in `incomplete`.
  https://github.com/dequelabs/axe-core/blob/develop/doc/developer-guide.md
- Fixture shape: `test/integration/rules/color-contrast/color-contrast.html` holds elements
  with ids `pass1..`, `fail1..`, `canttell1..`; the sibling `.json` lists the expected
  selectors under `violations`, `passes` and `incomplete`.
  https://github.com/dequelabs/axe-core/tree/develop/test/integration/rules/color-contrast
- Rules that walk the DOM must have shadow DOM pass and fail cases; rules with an `after`
  function must have iframe cases. https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md
- Contributing guide: "We expect all code to be 100% covered by tests", but reviewers judge
  adequacy rather than coverage metrics. https://github.com/dequelabs/axe-core/blob/develop/CONTRIBUTING.md
- Policy: axe-core 4.1 (Wilco Fiers, Nov 2020) treats false positives as bugs ("If you find
  one and tell us about it, we will fix it") and aimed to bring known false positives to zero.
  https://www.deque.com/blog/deque-releases-axe-core-4-1/
- Deque docs: "needs review" and "incomplete" mean the same thing; only violations it is sure
  of are reported. https://docs.deque.com/devtools-for-web/4/en/needs-review-incomplete
- Deque's 57% figure comes from its own study of more than 2,000 audits, 13,000 pages and
  nearly 300,000 issues, measured by issue volume rather than success criteria (vendor
  study, not independently replicated).
  https://www.deque.com/blog/automated-testing-study-identifies-57-percent-of-digital-accessibility-issues

Lighthouse

- The accessibility score is a weighted average of pass/fail audits (weights 3, 7, 10, based
  on axe impact); manual audits are listed but not scored, the same split as violation vs
  needs review. https://developer.chrome.com/docs/lighthouse/accessibility/scoring
- Smokehouse: end-to-end tests run Lighthouse against purpose-built fixture sites and assert
  expectations on the result with subset matching, numeric ranges (`'>0'`, `'100+/-10'`),
  regexes, and `_includes` / `_excludes` for lists. This is the model for asserting render
  findings on fixture pages. https://github.com/GoogleChrome/lighthouse/blob/main/cli/test/smokehouse/readme.md

WAVE (WebAIM)

- Red icons are errors to fix, yellow alerts are things a human should look at, green
  features "should be verified"; "Only a human can determine true accessibility."
  https://wave.webaim.org/help
- WebAIM Million counts only WAVE "errors", defined as having "a very high likelihood of
  being WCAG 2.2 Level A/AA conformance failures", and states that absence of detected errors
  does not mean a page is accessible. https://webaim.org/projects/million/

ESLint and stylelint

- ESLint `RuleTester`: `valid` and `invalid` arrays; invalid cases need `errors` (count or
  objects with `message` or `messageId`, `line`, `column`, `endLine`, `endColumn`), `output`
  is required if the rule fixes code, `suggestions` if it suggests; `assertionOptions` can
  force message and location on every error.
  https://eslint.org/docs/latest/integrate/nodejs-api#ruletester
- stylelint `jest-preset-stylelint` `testRule`: `accept` and `reject` arrays, each with
  `code`, `description`, and for reject `message`, location fields, `fixed`, or `warnings`
  for several. https://github.com/stylelint/jest-preset-stylelint

Semgrep

- Inline annotations: `ruleid:` (must match, guards against false negatives), `ok:` (must not
  match, guards against false positives), `todoruleid:` and `todook:` (known gaps, reported
  but not failing); the Semgrep test command pairs rule and test files by name; autofix tests via a
  `.fixed` file. https://docs.semgrep.dev/writing-rules/testing-rules

W3C ACT Rules

- ACT Rules Format: each rule has applicability, expectations, assumptions, accessibility
  support notes, and must have at least one passed, one failed and one inapplicable example.
  Outcomes: passed, failed, inapplicable, cantTell, untested. An implementation is
  "consistent" when it has no false results on the examples and reports at least one failed
  example as failed; "partially consistent" when it has no false positives but does not cover
  everything. https://www.w3.org/TR/act-rules-format/
- Implementation reports: vendors run their tool on every rule's examples and submit EARL
  reports; the W3C page lists, per tool, consistent rules (e.g. axe-core 4.14.0: 30 WCAG rules
  consistent, 5 proposed). https://www.w3.org/WAI/standards-guidelines/act/implementations/
  and the axe-core report https://www.w3.org/WAI/standards-guidelines/act/implementations/axe-core/
  Test cases: https://www.w3.org/WAI/standards-guidelines/act/report/testcases/ ; EARL format:
  https://act-rules.github.io/pages/implementations/earl-reports/

Measured accuracy of automated checkers (why per-rule numbers matter)

- Vigo, Brown and Conway (W4A 2013), six tools against WCAG 2.0: coverage at most 50% of
  success criteria, completeness 14% to 38%, and the tools with higher completeness had lower
  correctness (66% to 71%). https://doi.org/10.1145/2461121.2461124
- UK GDS (2017): a page with 142 deliberate barriers run through 13 tools; tools found only a
  minority, and 42 to 43 barriers were missed by all (secondary figure).
  https://accessibility.blog.gov.uk/2017/02/24/what-we-found-when-we-tested-tools-on-the-worlds-least-accessible-webpage/
  and https://alphagov.github.io/accessibility-tool-audit/
- Google, "Lessons from Building Static Analysis Tools at Google" (CACM 61(4), 2018): an
  "effective false positive" is a result developers take no action on; compiler checks must
  produce no effective false positives; code review checks must produce "less than 10%
  effective false positives"; Tricorder disables an analyzer when its "Not useful" ratio
  goes above 10%. https://research.google/pubs/lessons-from-building-static-analysis-tools-at-google/
  (PDF https://6826.csail.mit.edu/2020/papers/google-analysis-cacm.pdf) and Tricorder (ICSE 2015)
  https://research.google/pubs/tricorder-building-a-program-analysis-ecosystem/

What a per-rule fixture and a per-rule report look like in practice: the axe-core
`color-contrast` html plus json pair (element ids and expected selector lists per outcome),
the Semgrep annotated test file, and the W3C ACT implementation table (one row per example,
expected vs reported outcome, then a consistent / partially consistent verdict per rule).
None of these publish a precision number on real pages; the closest public practice is
Google's 10% effective false positive bar backed by live feedback. ux-skill can go further
by publishing Wilson intervals from a labelled corpus.

### B2. Public datasets of real pages and UIs, and building the corpus

| Dataset | What it is | Licence / terms | Use for ux-skill |
|---------|------------|-----------------|------------------|
| WebAIM Million | WAVE run on the top 1,000,000 home pages from Tranco, rendered DOM; Feb 2026: 95.9% of home pages with detected WCAG failures, 56.1 errors per page, low contrast text on 83.9% | Report only; no page data released | Methodology model (exclusions: under 10 elements, error pages); comparison numbers |
| HTTP Archive / Web Almanac | Monthly crawl of about 17 million sites from the CrUX URL list, desktop and emulated mobile, Lighthouse, response bodies, custom metrics, in BigQuery | Site code Apache 2.0; no formal data licence (maintainers say use freely, attribution appreciated); page content stays the owners' | URL sampling frame; prevalence of patterns via custom metrics; not a source of redistributable pages |
| Rico (Deka et al., UIST 2017) | 72k screens from 9.7k Android apps | Researcher agreement: screenshots "may contain copyrighted work", user indemnifies the university | Mobile only; not web; reference only |
| WebUI (Wu et al., CHI 2023) | 400k web pages, screenshots at several devices, accessibility trees, box models, computed styles | Same style of researcher agreement as Rico (CMU), "may contain copyrighted work"; HF licence "other" | Large pool for precision sampling of render rules (research use); not redistributable |
| UICrit (Duan et al., UIST 2024) | 1,000 Rico screens, 3 annotators each, 11,344 critiques with boxes, ratings for aesthetics (1 to 10), usability, design quality | Annotations CC BY 4.0; screenshots inherit Rico terms | Labelling protocol model; taste rubric |
| UIClip (Wu et al., UIST 2024) | JitterWeb (2.3M synthetic jittered pairs) and BetterApp (about 1,200 designer-rated pairs, 12 designers) | See HF collection | Defect-injection idea for gold pairs; quality model baseline |
| Reinecke and Gajos (CHI 2013, 2014) | 430 to 450 website screenshots rated for visual appeal by about 40,000 people, with demographics | Released for research | Shows taste varies with country, age and education; rater pool design |
| Design2Code (Si et al., 2024) | 484 real pages curated from the C4 validation set | ODC-By (inherits C4) | A redistributable set of real pages for class A |
| WebGen-Bench (Lu et al., NeurIPS 2025) | 101 website instructions, 647 functional tests | See repo | Brief source for generator evaluation |
| Tranco | Research top-sites list, hardened against manipulation | Free for research | Sampling frame for class B designer and wild pages |
| Common Crawl | Petabyte web crawl | ToU: content stays subject to the owners' rights; user must respect third-party copyright; indemnity for AI use | URL discovery only |

Sources:
- WebAIM Million: https://webaim.org/projects/million/
- HTTP Archive: https://httparchive.org/docs/guides/getting-started/ ; FAQ https://httparchive.org/faq ;
  data rights thread https://discuss.httparchive.org/t/what-are-the-rights-licensing-for-data-in-http-archive/1924 ;
  Web Almanac methodology https://almanac.httparchive.org/en/2024/methodology
- Rico copyright notice: https://www.interactionmining.org/archive/rico/copyright.txt ; paper
  https://experts.illinois.edu/en/publications/rico-a-mobile-app-dataset-for-building-data-driven-design-applica/
- WebUI: https://uimodeling.github.io/ ; https://huggingface.co/datasets/biglab/webui-all ;
  terms https://github.com/js0nwu/webui/blob/main/COPYRIGHT.txt
- UICrit: https://arxiv.org/abs/2407.08850 ; https://github.com/google-research-datasets/uicrit
- UIClip: https://arxiv.org/abs/2404.12500 ; https://huggingface.co/collections/biglab/uiclip-uist-2024
- Reinecke and Gajos 2014: https://iis.seas.harvard.edu/papers/reinecke14visual.pdf ; 2013:
  https://www.eecs.harvard.edu/~kgajos/papers/2013/reinecke13predicting.shtml
- Design2Code: https://arxiv.org/abs/2403.03163 (HTML version with method details https://arxiv.org/html/2403.03163)
- WebGen-Bench: https://arxiv.org/abs/2505.03733 ; https://github.com/mnluzimu/WebGen-Bench
- Tranco: https://arxiv.org/abs/1806.01156 ; https://tranco-list.eu/
- Common Crawl terms: https://commoncrawl.org/terms-of-use

Licences for the redistributable designer half:
- HTML5 UP templates: CC BY 3.0. https://html5up.net/license
- UK Open Government Licence v3: copy, adapt and redistribute with attribution; excludes
  personal data, departmental logos and crests, and third-party rights.
  https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/
- US federal government works are not protected by copyright (17 U.S.C. 105), but third-party
  content on federal sites may be. https://www.law.cornell.edu/uscode/text/17/105
- EU text-and-data-mining exceptions (Directive 2019/790, art. 3 for research organisations,
  art. 4 for others unless the rights holder opts out in machine-readable form).
  https://eur-lex.europa.eu/eli/dir/2019/790/oj

Snapshot tooling: WARC format (ISO 28500) https://iipc.github.io/warc-specifications/ ;
browsertrix-crawler https://github.com/webrecorder/browsertrix-crawler ; pywb replay
https://github.com/webrecorder/pywb ; Playwright screenshots vary by host OS, version,
settings and hardware, so baselines must come from the same environment
https://playwright.dev/docs/test-snapshots

No public dataset combines (a) real web pages, (b) element-level design or accessibility
problem labels, and (c) a licence that allows redistribution. That is the main reason to
build ux-bench, and also a contribution worth publishing.

### B3. Labelling protocol

- A five-step severity scale from 0 (no problem) through cosmetic, minor and major to 4
  (catastrophic), weighing how often, how hard and how persistently a problem bites; one
  evaluator's ratings are unreliable on their own, and the mean of three evaluators is
  satisfactory for most purposes; rate independently.
  https://www.nngroup.com/articles/how-to-rate-the-severity-of-usability-problems/
- Heuristic evaluation: three to five people should evaluate independently, then
  aggregate. https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
- Evaluator effect: in the original study only 20% of 93 problems were found by all four
  evaluators and 46% by only one (Jacobsen, Hertzum and John 1998); Hertzum and Jacobsen
  (2001) report any-two agreement from 5% to 65%; a review of 33 studies gives a median
  any-two agreement of 27%. https://measuringu.com/evaluator-effect/
- Krippendorff's alpha conventions: rely on alpha >= 0.800, tentative conclusions for 0.667
  to 0.800, discard below 0.667; alpha handles any number of raters, missing data and
  ordinal scales. https://en.wikipedia.org/wiki/Krippendorff%27s_alpha (summarising
  Krippendorff, "Computing Krippendorff's Alpha-Reliability", 2011,
  https://repository.upenn.edu/asc_papers/43/)
- Kappa paradoxes: with imbalanced marginals (rare positives) kappa can be low despite high
  agreement; report positive and negative agreement separately (Feinstein and Cicchetti
  1990; Cicchetti and Feinstein 1990, J Clin Epidemiol 43:543 and 551).
  https://pubmed.ncbi.nlm.nih.gov/2348207/
- Sample sizes for kappa studies: Sim and Wright 2005, Physical Therapy 85(3):257.
  https://doi.org/10.1093/ptj/85.3.257
- Binomial intervals: Brown, Cai and DasGupta (Statistical Science 16(2), 2001) show the Wald
  interval is unreliable and recommend Wilson or Jeffreys for n <= 40 and Agresti-Coull for
  larger n. https://doi.org/10.1214/ss/1009213286
- Crowd vs expert critique: aggregated feedback from 10 to 14 crowd workers covered roughly
  40% to 60% of issues experts found (CrowdCrit, CSCW 2015), which argues for experts on the
  recall task. https://vis.berkeley.edu/papers/crowdcrit/luther-crowdcrit-cscw2015.pdf
- UICrit used 7 experienced designers, later 3 annotators per screen, with critiques tied to
  bounding boxes: a working template for box-level problem labels.
  https://arxiv.org/abs/2407.08850

Wilson formula used in Part A: for k successes in n, with z = 1.96,
centre = (p + z^2/2n) / (1 + z^2/n), half-width = z * sqrt(p(1-p)/n + z^2/4n^2) / (1 + z^2/n).
All tables in Part A were computed with it.

### B4. Blind taste evaluation of generated designs

- Chatbot Arena (Chiang et al., 2024): Bradley-Terry fitted by (reweighted) maximum
  likelihood; intervals by pivot bootstrap or sandwich standard errors; active sampling of
  pairs that shrink intervals most; anomalous-voter detection; crowd vs expert agreement 73%
  to 83%, expert vs expert 79% to 90%. https://arxiv.org/abs/2403.04132
- WebDev Arena (LMArena): two anonymous models build an app from the user's prompt, users
  vote; 26% ties, more often "both bad"; ranking now via the open Arena-Rank package.
  https://news.lmarena.ai/webdev-arena ; https://news.lmarena.ai/arena-rank
- Design Arena: four anonymous models per session, pairwise votes, Bradley-Terry by
  iterative fitting, Wilson 95% intervals on win rates, models under 15 comparisons hidden and
  under 50 flagged "new". https://notes.designarena.ai/methodology/
- The Leaderboard Illusion (Singh et al., 2025): private testing and selective disclosure
  bias arena rankings; lesson for ux-skill: preregister and publish every run.
  https://arxiv.org/abs/2504.20879
- Design2Code: 484 real pages; human evaluation on Prolific ($16/hour, US, more than 2,500
  studies, >= 98% approval), 5 annotators per pair, majority of 3 decides, Fleiss' kappa 0.46
  for pairwise, 0.32 for "can it replace the original"; automatic metrics (position,
  block-match, CLIP, color) predicted human pairwise preference at 79.9% accuracy.
  https://arxiv.org/html/2403.03163
- Sketch2Code (NAACL 2025): 731 sketches of the 484 Design2Code pages, user study with UI/UX
  experts. https://arxiv.org/abs/2410.16232
- WebGen-Bench (NeurIPS 2025): 101 instructions, 647 functional test cases run by a
  web-navigation agent; best agent combination 27.8%. Functional, not aesthetic.
  https://arxiv.org/abs/2505.03733
- ArtifactsBench (Tencent, 2025): 1,825 tasks, MLLM judge with per-task checklists over
  interaction screenshots; 94.4% ranking consistency with WebDev Arena and over 90% pairwise
  agreement with experts; judge model changes break comparability across time.
  https://arxiv.org/abs/2507.04952 ; https://github.com/Tencent-Hunyuan/ArtifactsBenchmark
- UIClip: designer-rated pairs and synthetic jitter; GPT-4V judged a jittered screenshot with
  overflowing text as better than the original. https://arxiv.org/abs/2404.12500

LLM-as-judge pitfalls:

- Zheng et al. (2023), "Judging LLM-as-a-Judge": position, verbosity and self-enhancement
  biases; strong judges reach over 80% agreement with humans on text.
  https://arxiv.org/abs/2306.05685
- Wang et al. (2023), "Large Language Models are not Fair Evaluators": rankings can be
  flipped by swapping order; fixes are multiple evidence, balanced position calibration
  (aggregate over both orders) and human-in-the-loop for hard cases.
  https://arxiv.org/abs/2305.17926
- MLLM as a UI Judge (2025): 30 UIs, about 9,300 human ratings on 9 factors; MLLM pairwise
  accuracy about 60%, near 50% when human differences are small, near chance on ease of use;
  authors call MLLMs "UI testing approximators, not replacements".
  https://arxiv.org/abs/2510.08783
- WiserUI-Bench (2025): 300 real A/B-tested UI pairs; order-consistent accuracy 15% to 35%
  against a 25% baseline; strong second-position bias. https://arxiv.org/abs/2505.05026
- MLLM-as-a-Judge benchmark (2024): general multimodal judging, pairwise and scoring.
  https://arxiv.org/abs/2402.04788

When an LLM judge is acceptable: as a pre-filter for defects that are visible and binary
(broken layout, overflow, missing images), run in both orders, checked against a human gold
set, and never as the score reported for a release.

Sample-size arithmetic (normal approximation, z = 1.96, p = 0.5): n = z^2 * 0.25 / E^2,
giving 96, 196 and 384 non-tied judgments for margins of 10, 7 and 5 points. Power for a
one-sample test of p1 against 0.5 at two-sided 0.05 and 80% power:
n = ((1.96 * 0.5 + 0.8416 * sqrt(p1 (1 - p1))) / (p1 - 0.5))^2, giving 783, 194, 85 and 47
for p1 = 0.55, 0.60, 0.65 and 0.70. Bradley-Terry: Bradley and Terry (1952), Biometrika
39:324. https://doi.org/10.2307/2334029

### B5. Regression protection

- Ruff ecosystem check: runs the old and new binaries over a corpus of open source projects
  on every PR and posts the diff as a PR comment (began as `scripts/check_ecosystem.py`, now
  the `ruff-ecosystem` package). https://github.com/astral-sh/ruff/tree/main/python/ruff-ecosystem
  and origin https://github.com/astral-sh/ruff/issues/2677
- mypy_primer: "a tool for regression testing Python static type checkers", runs two
  revisions over a fixed list of projects and diffs; used in the CI of mypy, typeshed and
  pyright. https://github.com/hauntsaninja/mypy_primer
- Clippy lintcheck: runs Clippy over a fixed, pinned set of crates and diffs logs to "spot new
  or disappearing warnings". https://github.com/rust-lang/rust-clippy/blob/master/lintcheck/README.md
- Lighthouse smokehouse: expectations on fixture sites with ranges and include/exclude
  matchers, run in CI. https://github.com/GoogleChrome/lighthouse/blob/main/cli/test/smokehouse/readme.md
- Mutation testing: mutmut for Python, incremental, can limit to changed functions and
  covered lines, reports a mutation score for CI. https://mutmut.readthedocs.io/
- Metamorphic testing of static analyzers: Statfier (ESEC/FSE 2023) applies
  semantic-preserving transformations to analyzers' own test programs and flags inconsistent
  results; 79 bugs, 46 confirmed, in five analyzers.
  https://2023.esec-fse.org/details/fse-2023-research-papers/31/Statfier-Automated-Testing-of-Static-Analyzers-via-Semantic-preserving-Program-Trans
- Visual goldens need a fixed environment and thresholds (`threshold`, `maxDiffPixels`).
  https://playwright.dev/docs/test-snapshots
- Feedback-driven drift control: Tricorder's "Not useful" button files a bug and the analyzer
  is disabled above a 10% ratio (CACM 2018, above). For ux-skill, the equivalent is a
  false-positive report command or an issue template that records rule, excerpt and
  version, feeding `bench/history.jsonl`.

* * *

## Part C. Open risks

1. Too few findings per rule. With 200 pages, many of the 180 rules will fire fewer than 35
   times, so they cannot qualify for blocking. Mitigation: the larger unlabelled pool for
   precision (A3), and accept that some rules stay advisory. Do not lower the bar to fit.
2. Labelling cost and rater supply. About 50 hours for precision and 90 for recall per full
   pass, plus adjudication. Arabic and RTL pages need raters who read Arabic.
3. Taste rules have no objective truth. Precision for `inter-as-display` style rules is a
   designer opinion; alpha may stay below 0.667. Then the honest outcome is to keep such rules
   advisory or info and say so, not to pick friendlier raters.
4. Legal exposure. Third-party pages and screenshots are copyrighted; WebUI and Rico push the
   risk onto the user by contract. Keep class B private, publish derived data only, get
   advice before using class B in anything commercial.
5. Overfitting to the corpus. Rule authors tuning against the dev split will inflate dev
   precision. The held-out split, scored once per release, and yearly refresh are the guard.
6. Goodhart between linter and generator. If the generator is tuned to pass the linter, a
   good lint score on generated pages says nothing about quality. Judge the generator with
   blind humans (A5), never by its own linter.
7. Blinding can fail. Designers may recognise a house style (ux-skill's or a known AI look).
   Ask raters to guess the condition and report the guess rate.
8. Moving targets. AI tools change monthly, Chromium changes rendering, and LLM judges get
   deprecated (ArtifactsBench had to switch judge models). Record every version in the
   manifest and re-baseline only in dedicated PRs.
9. Rater population effects. Visual preference differs by country, age and education
   (Reinecke and Gajos 2014). Report the panel's makeup and do not generalise beyond it.
10. Vendor numbers. Deque's 57% and the zero-false-positive claim are self-reported; ACT
    reports cover only the rules' example sets, not real pages. ux-skill should not cite them
    as proof of its own accuracy, only as practice to copy.
