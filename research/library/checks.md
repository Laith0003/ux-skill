# Lessons that can become measured checks

Three clusters, each written separately: research and process, visual and system, interaction and content. Source codes (B01 to B96) refer to books listed in ACKNOWLEDGEMENTS.md.

<!-- cluster A: research and process -->

# Checks: cluster A (research and process)

Lessons that can become measurable automated checks, on a rendered page or on design artifacts (research plans, interview guides, test plans, personas, journey maps, findings, case studies, portfolio pages). Ordered by impact. Merged duplicates list both original ids under "Merged from". Methods: static = lint of HTML/CSS/JSX; render = load in a browser; interaction = drive the page; artifact = parse a design artifact or a `.ux/*.json` output.

Existing coverage: none of these exists in data/anti-patterns.json today. Where an existing rule partly overlaps, its id is named in the Existing column.

| # | id | impact | method | existing anti-pattern |
|-|-|-|-|-|
| 1 | interview-script-future-or-design-question | high | artifact | none |
| 2 | leading-or-double-question | high | artifact | none |
| 3 | research-plan-behavioral-method | high | artifact | none |
| 4 | persona-evidence-trace | high | artifact | none |
| 5 | persona-goals-present | high | artifact | none |
| 6 | screener-structure | high | artifact | none |
| 7 | journey-map-core-rows | high | artifact | none |
| 8 | qual-sample-per-segment | high | artifact | none |
| 9 | trunk-test-landmarks | high | static, render | none |
| 10 | prototype-dead-end-control | high | render, interaction | partial: href-empty-hash, link-without-href, href-javascript-void |
| 11 | test-task-names-ui-label | high | artifact | none |
| 12 | test-plan-sample-below-discovery | high | artifact | none |
| 13 | small-n-percentage | high | artifact | none |
| 14 | ab-winner-not-significant | high | artifact | none |
| 15 | hypothesis-without-signal | high | artifact | none |
| 16 | rate-without-interval | high | artifact | none |
| 17 | case-study-role-stated | high | artifact | none |
| 18 | case-study-metric-has-basis | high | artifact | partial: round-number-stats, before-after-100-percent, fake-line-of-code-count |
| 19 | finding-states-problem-not-fix | high | artifact | none |
| 20 | research-vague-quantifier | high | artifact | none |
| 21 | critique-comment-has-reason | high | artifact | none |
| 22 | worst-case-content-overflow | high | render | partial: lorem-ipsum-leak, fixed-height-text-block |
| 23 | persona-cast-size | medium | artifact | none |
| 24 | persona-demographic-ratio | medium | artifact | none |
| 25 | persona-distinctness | medium | artifact | none |
| 26 | recruit-buffer | medium | artifact | none |
| 27 | survey-overlapping-ranges | medium | static, artifact | none |
| 28 | rating-scale-points | medium | static, artifact | none |
| 29 | survey-length | medium | static, artifact | none |
| 30 | survey-other-option | medium | static, render, artifact | none |
| 31 | journey-map-size | medium | artifact | none |
| 32 | journey-map-state-label | medium | artifact | none |
| 33 | consent-form-items | medium | artifact | none |
| 34 | case-study-method-disclosure | medium | static, render | none |
| 35 | within-subjects-counterbalance | medium | artifact | none |
| 36 | test-task-step-instructions | medium | artifact | none |
| 37 | test-plan-thinkaloud-with-timing | medium | artifact | none |
| 38 | test-plan-session-overlong | medium | artifact | none |
| 39 | prototype-placeholder-data | medium | static | partial: lorem-ipsum-leak, placeholder-token-shipped, fake-name-john-doe |
| 40 | heuristic-review-single-evaluator | medium | artifact | none |
| 41 | survey-precision-mismatch | medium | artifact | none |
| 42 | task-time-arithmetic-mean | medium | artifact | none |
| 43 | sus-misreported | medium | artifact | none |
| 44 | nps-misbanded | medium | render, artifact | none |
| 45 | task-success-criteria-missing | medium | artifact | none |
| 46 | ab-plan-multiple-changes | medium | artifact | none |
| 47 | severity-without-frequency | medium | artifact | none |
| 48 | case-study-summary-first | medium | render, artifact | none |
| 49 | case-study-concept-labelled | medium | artifact | none |
| 50 | case-study-process-evidence | medium | artifact | none |
| 51 | report-conclusion-first | medium | artifact | none |
| 52 | report-has-positive-findings | medium | artifact | none |
| 53 | problem-statement-no-solution | medium | artifact | none |
| 54 | feature-traces-to-need | medium | artifact | none |
| 55 | design-handoff-a11y-annotations | medium | artifact | none |
| 56 | workshop-size-and-roles | medium | artifact | none |
| 57 | principle-too-generic | medium | artifact | none |
| 58 | portfolio-contact-reachable | medium | static, render | none |
| 59 | brief-expression-share | medium | artifact | none |
| 60 | persona-length | low | artifact | none |
| 61 | persona-review-date | low | artifact | none |
| 62 | journey-map-persona-count | low | artifact | none |
| 63 | task-tree-subgoal-count | low | artifact | none |
| 64 | scenario-has-obstacle | low | artifact | none |
| 65 | prototype-totals-do-not-add-up | low | render | none |
| 66 | wireframe-color-discipline | low | render, artifact | none |
| 67 | sticky-metric-as-success | low | artifact | none |
| 68 | sprint-plan-shape | low | artifact | none |
| 69 | accuracy-only-model-metric | low | artifact | none |
| 70 | portfolio-password-gate | low | static | none |
| 71 | portfolio-stock-imagery | low | static | partial: unsplash-photo-id-no-alt, picsum-photos-seed, placeholder-com-direct |
| 72 | resume-machine-readable | low | artifact | none |
| 73 | highlight-reel-length | low | artifact | none |
| 74 | team-user-exposure | low | artifact | none |


## High impact

### interview-script-future-or-design-question
- Measures: interview guides, test scripts, debriefs and survey drafts that ask participants to predict their own future behavior, to like or dislike, or to design the solution.
- Threshold: 0 question lines matching self-prediction and design patterns (would you use, would you pay, would you buy, how much would you pay, how likely are you to, do you like, what features would you, how would you design, what would solve). No closing section that asks the participant to propose the fix. Closed questions (opening with do, does, did, is, are, would, will, can, could) at most 20 percent of the probing and debrief questions, not counting a qualifying closed question that is followed by an open one.
- How measured: artifact check (regex over lines ending in a question mark, or list items under a questions heading).
- Fixtures: fail, a debrief with "Would you use this every day?" and a closing question asking what feature would fix it; near-miss pass, "When did you last try to do this, and what got in the way?" plus one qualifying closed question followed by an open follow-up.
- False-positive risk: medium. Pricing studies may legitimately ask willingness to pay; allow an explicit opt-out tag on the plan.
- Sources: B30 p.47; B03 p.148-149, 352; B27 p.41, 44-45, 64-65; B26 p.81-85; B20 p.148; B89 p.84-85; B81 p.217-219; B85 p.268-269; B17 p.115-117; B40 p.36
- Existing anti-pattern: none. commands/ux-research.md:57 currently ends its script with a reflection question that asks what would solve the problem (see gaps.md, contradicts).
- Merged from: interview-script-future-or-design-question, script-leading-question.

### leading-or-double-question
- Measures: leading, loaded or double-barreled questions in interview guides, surveys and screeners.
- Threshold: 0 matches. Flag questions that open with a negative tag (don't you, wouldn't you, isn't it), contain evaluative adjectives about the product (great, easy, excellent, love), or join two asks with and / or around two verbs.
- How measured: artifact check (regex plus a simple clause count per question).
- Fixtures: fail, a survey item asking how much people love the new easy checkout; near-miss pass, an item asking people to describe their last checkout.
- False-positive risk: medium. Legitimate compound nouns (terms and conditions) and quoted product names can trip the and/or rule; restrict it to two verb phrases.
- Sources: B03 p.149-151; B40 p.39; B44 p.276-279; B23 p.239, 248-249; B69 p.180; B02 p.321-325
- Existing anti-pattern: none.

### research-plan-behavioral-method
- Measures: whether a research plan includes at least one method that captures behavior rather than only self-report.
- Threshold: at least 1 method from the behavioral set (field visit, contextual inquiry, observation, usability test, diary or experience sampling, analytics or logs, A/B test). Fail when every method is interview, survey, focus group or preference test. Warn when fewer than 2 method types are listed.
- How measured: artifact check (parse the methods field of the plan, for example the method line in the ux-research output or .ux/last-research.json).
- Fixtures: fail, a plan with 8 interviews plus a survey; near-miss pass, 6 interviews plus 5 moderated task sessions.
- False-positive risk: low. A pure attitudinal study (brand perception) may opt out with a stated reason.
- Sources: B06 p.79, 87; B30 p.21-22, 198-202; B02 p.310-311; B27 p.82, 88; B17 p.31-33
- Existing anti-pattern: none.

### persona-evidence-trace
- Measures: whether each persona states its evidence base.
- Threshold: every persona carries a source block naming method, number of participants (n of at least 4 for the segment) and date; a persona without it must carry a proto or assumption label. Fail when neither is present.
- How measured: artifact check (persona markdown, JSON or design-file text layer).
- Fixtures: fail, a persona card with name, photo, age, hobbies and a quote but no source; near-miss pass, a card labeled proto-persona, assumption, to validate by a date.
- False-positive risk: low.
- Sources: B50 p.56, 83-84, 171; B26 p.99; B03 p.498; B34 p.59-63; B58 p.239, 262; B23 p.347-349
- Existing anti-pattern: none.

### persona-goals-present
- Measures: presence and count of goals on each persona.
- Threshold: at least 1 goal, target 3 to 5 outcome goals; at most 1 life goal and at most 2 experience goals. Fail at 0 goals; warn above 5 outcome goals.
- How measured: artifact check (count list items under a goals heading or goals field).
- Fixtures: fail, a persona with needs and frustrations but no goals section; near-miss pass, three outcome goals and one experience goal.
- False-positive risk: low.
- Sources: B26 p.116, 121; B03 p.498, 503; B50 p.64
- Existing anti-pattern: none.

### screener-structure
- Measures: screener order, form and length.
- Threshold: the first question that can disqualify appears before any qualifying or profile question; behavior questions use an explicit time window or count; a recent-participation exclusion (6 months) is present; total questions 5 to 20. Fail if any rule is missed.
- How measured: artifact check (ordered question list with a disqualify flag; regex for time windows such as in the last N days, weeks or months).
- Fixtures: fail, a screener opening with age and income then asking whether the person often shops online; near-miss pass, opening with an exclusion for recent study participation and asking how many orders they placed in the last month.
- False-positive risk: medium. Very short guerrilla screeners may only need 3 to 5 questions; allow a guerrilla mode.
- Sources: B03 p.122-124, 128-129; B17 p.48, 50-52; B28 p.167-169; B30 p.94-96, 177
- Existing anti-pattern: none.

### journey-map-core-rows
- Measures: whether a journey map artifact has the core structure and evidence.
- Threshold: has a scope or persona header, a goal, ordered phases, actions, pain points and opportunities, plus at least 1 evidence item (quote, observation or data reference). Fail on any missing core row; fail when no evidence and no hypothesis label.
- How measured: artifact check (row headers in a table, FigJam or markdown export).
- Fixtures: fail, a map with phases and an emotion curve but no pain points, opportunities or evidence; near-miss pass, all six rows plus two participant quotes.
- False-positive risk: low to medium. Service blueprints use different row names; detect the diagram type first.
- Sources: B67 p.10-12, 16, 20-22; B11 p.73-75; B17 p.159-160; B30 p.241-256
- Existing anti-pattern: none.

### qual-sample-per-segment
- Measures: planned participants per named segment or user type, when the plan says segments will be compared.
- Threshold: qualitative rounds need at least 3 per compared segment (4 to 6 for enterprise roles, 8 to 12 for consumer types is the target) and at least 5 overall; surveys analyzed per segment need at least 100 per segment, and about 385 per segment for plus or minus 5 percent claims. Warn when a plan lists segments but only a study-level n.
- How measured: artifact check on the `/ux-research` plan: count compared segments, divide the stated n (or read per-segment n), compare.
- Fixtures: fail, interviews n=6 across 3 segments and 2 regions (1 per cell); near-miss pass, n=9 with 3 owners, 3 staff, 3 customers.
- False-positive risk: medium. Segments listed only for context get flagged; require the plan to state which segments are compared.
- Sources: B26 p.75, 79; B30 p.138; B64 p.142-143; B17 p.39-40; B03 p.368; B28 p.110; B58 p.239, 501-502
- Existing anti-pattern: none.
- Merged from: qual-sample-per-segment, subgroup-sample-too-small.

### trunk-test-landmarks
- Measures: whether a deep (non-home) page answers the six orientation questions: site identity, page name, major sections, local navigation, current location, search.
- Threshold: all six present on every page below the home page: (1) a logo or site name linking to the root, (2) exactly one h1, (3) a nav landmark with at least 3 links, (4) a second-level nav or breadcrumb (nav with aria-label containing "breadcrumb", or ol inside nav) when the page depth is 2 or more, (5) one link with aria-current="page" or an equivalent active class, (6) a search input or role="search" when the site has more than about 20 pages. Fail when 2 or more are missing; warn on 1.
- How measured: static lint of rendered HTML, run on a sample of deep URLs (not the home page).
- Fixtures: fail, a product detail page with a logo image that is not a link, no h1 and no nav landmark. Near-miss pass, a page with a logo link to "/", one h1, a top nav of 5 links, a breadcrumb nav, aria-current on the active section, and a search form, but no local sidebar (breadcrumb satisfies item 4).
- False-positive risk: medium. Single-page apps, campaign landing pages and small sites without search will trip it; scope to multi-page sites and pages at depth 2 or more, and make search conditional on page count.
- Sources: B77 p.93-94
- Existing anti-pattern: none (heading-skip-h1-h3 covers heading order only)

### prototype-dead-end-control
- Measures: interactive controls in an HTML prototype or built page that do nothing when activated.
- Threshold: 0 controls (a, button, [role=button], [onclick]) that, when clicked, cause no navigation, no DOM change, no focus change and no dialog. Out-of-scope controls must lead to a labeled placeholder ("not in this prototype" or similar).
- How measured: interaction check in a headless browser: snapshot DOM and URL, click each visible control, diff, restore.
- Fixtures: fail, a prototype nav where "Settings" is a button with no handler. Near-miss pass, the same nav where "Settings" opens a page reading "Settings is not part of this prototype. What did you expect to find here?".
- False-positive risk: medium. Controls whose effect is off-DOM (download, clipboard, analytics only) or delayed (debounced) read as dead; allow a 500 ms wait and whitelist download and copy actions.
- Sources: B74 p.48-49; B28 p.68-69; B20 p.450-451; B35 p.27-28
- Existing anti-pattern: partial. href-empty-hash, link-without-href and href-javascript-void catch the static markup cases; none catches a handler that does nothing.

### test-task-names-ui-label
- Measures: usability test tasks that contain the visible label of the control or menu the task is meant to test.
- Threshold: 0 tasks containing a visible UI label of 4 or more characters (excluding stop words and the product name) taken from the screens under test, matched case-insensitively as a whole word or phrase.
- How measured: artifact check. Extract button, link, menu and heading text from the prototype or page; extract task lines from the test plan; report overlaps.
- Fixtures: fail, task "Use Quick Transfer to send money to Sara" when a button reads "Quick Transfer". Near-miss pass, task "Send 20 dinars to your sister as fast as you can" with the same button present.
- False-positive risk: medium. Common words that are both labels and natural language ("Search", "Save") will match; limit to multi-word labels or labels the plan marks as under test.
- Sources: B20 p.405-408; B28 p.121-123, 222; B63 p.255; B41 p.183, 186-187
- Existing anti-pattern: none

### test-plan-sample-below-discovery
- Measures: whether a formative test plan's sample can plausibly reach its discovery goal.
- Threshold: compute discovery as 1 - (1 - p)^n, with n the cumulative count across planned rounds, with p from the plan or 0.31 by default (0.10 when the plan targets rare or critical problems). Fail when a standalone single round has n under 5; warn when the computed discovery is under the plan's stated goal or under 0.80 when no goal is stated; warn when the plan claims "5 users find 85 percent" without stating that it applies only to problems affecting about a third of users.
- How measured: artifact check of the research plan (n per round, number of rounds, stated goal, stated p).
- Fixtures: fail, one round of 3 users with no later rounds. Near-miss pass, a weekly series of 3 users for 4 weeks with fixes between rounds (cumulative 12, discovery about 0.99 at p 0.31).
- False-positive risk: low. Plans that are explicitly summative or quantitative should route to a sample-size calculation instead.
- Sources: B94 p.160-167; B20 p.565-569; B30 p.103-108; B34 p.123-124; B77 p.125-130
- Existing anti-pattern: none

### small-n-percentage
- Measures: a percentage reported from a sample smaller than 10 (stated n, or an "x of y" count with y < 10 next to it) in research reports, synthesis output, case studies and portfolio pages.
- Threshold: any percent figure whose denominator is under 10 must also show the raw count ("4 of 6"), or be replaced by it.
- How measured: artifact check. Parse "n = N", "N participants/users", "x of y" and percent tokens in the same paragraph or table row; flag a percent whose nearest n is under 10 with no "x of y" form beside it.
- Fixture: fail "83% of participants (n=6) failed checkout". Near-miss pass "5 of 6 participants (83%) failed checkout" or "62% drop-off (n=4,247)".
- False-positive risk: medium. Percentages unrelated to the sample (a conversion rate quoted from analytics in the same paragraph) can be misattributed; scope to the sentence or table row.
- Sources: B02 p.354, 392; B28 p.296, 304-305; B94 p.42
- Existing anti-pattern: none

### ab-winner-not-significant
- Measures: an A/B or variant result declared a winner (or shipped) when the reported counts do not support a significant difference.
- Threshold: two-proportion test (N-1 chi-square, or Fisher exact when any expected cell is under 1) gives p >= 0.05, or the 95 percent interval on the difference includes 0, while the text says "winner", "won", "lift", "ship" or "better".
- How measured: artifact check. Extract conversions and visitors per arm from the result table; compute the test; flag claims. Flag also when counts are missing entirely but a lift is claimed.
- Fixture: fail "Variant B wins: 6 vs 3 conversions out of 600 each". Near-miss pass "Variant B: 60 vs 30 of 6,000 each (p < 0.01), shipping B".
- False-positive risk: low when counts are present; medium when the artifact declares a different alpha in advance (read a declared alpha if present and use it).
- Sources: B27 p.211; B94 p.82-83, 95-98; B02 p.634-635
- Existing anti-pattern: none

### hypothesis-without-signal
- Measures: hypotheses, goals and success signals in a discovery brief, framing, lean canvas or sprint plan that name no measurable outcome.
- Threshold: each hypothesis and each goal contains a named metric or observable behavior, a direction or number, and ideally a time window; it does not begin with a feature verb (add, build, launch, ship, create, redesign).
- How measured: artifact check over `.ux/last-frame.json` and `.ux/last-discovery.json` hypothesis, goal and success_signal fields, and markdown sections titled Hypothesis or Goals.
- Fixtures: fail, "We believe partners will love the new dashboard" or "Launch the new dashboard"; near-miss pass, "new partners set up rules faster: median setup time under 5 minutes within 60 days of release".
- False-positive risk: medium. Discovery-stage problem hypotheses may use a count-based qualitative signal such as "5 of 8 interviewees describe X unprompted"; accept it, and allow a list of observable behavior verbs.
- Sources: B34 p.36-37, 54-55, 58-59; B27 p.19-21, 97-98; B64 p.216; B94 p.60-61; B09 p.81, 183; B96 p.61; B54 p.160-161; B35 p.29, 38
- Existing anti-pattern: none. commands/ux-discover.md:166-170 asks the model to push back in prose; nothing checks it.
- Merged from: hypothesis-without-signal, success-signal-measurable.

### rate-without-interval
- Measures: completion, success or conversion rates from samples under 100 reported as a bare point estimate.
- Threshold: n < 100 and no confidence interval, margin of error or "x of y" count attached.
- How measured: artifact check on research reports and benchmark summaries: find rate statements with an n below 100 and look for "CI", "interval", "+/-", "margin" or a bracketed range in the same row or sentence.
- Fixture: fail "Task 3 success rate: 70% (n=10)". Near-miss pass "Task 3: 7 of 10 succeeded (adjusted-Wald 95% CI 39 to 90%)".
- False-positive risk: low to medium. Qualitative reports that already use counts pass; analytics rates with very large n are out of scope by threshold.
- Sources: B94 p.36-42, 59-60; B30 p.285-286
- Existing anti-pattern: none

### case-study-role-stated
- Measures: whether a case study or portfolio project page states the author's own role and the team around them.
- Threshold: at least one role marker (for example "My role", "Role:", "I led", "I was responsible for", or a structured role field) plus a team or solo statement within the first 25 percent of body text.
- How measured: artifact check on case-study HTML or Markdown, and on `.ux/last-case-study.json` (a `role` fact field).
- Fixture: fail = a case study told entirely in "we" with no role line; near-miss pass = "Role: lead product designer, team of 4 (PM, 2 engineers)" in the overview paragraph.
- False-positive risk: low to medium; solo work needs an accepted "solo project" phrase; translated pages need localized markers.
- Sources: B05 p.200, 278; B84 p.49, 98; B29 p.210-213.
- Existing anti-pattern: none.

### case-study-metric-has-basis
- Measures: every number in Outcomes or Impact sections carries a basis: a baseline ("from X to Y"), a time window, a sample size, or a named measurement source.
- Threshold: 100 percent of percentage or multiplier claims in those sections have one of: "from", "to", "over N weeks/months", "n=", "N of M", "measured by", "baseline".
- How measured: artifact check (regex over the section text of the case study).
- Fixture: fail = "Engagement up 47%."; near-miss pass = "Redemption rose from 12% to 17% over six weeks (analytics, n=2,400 members)."
- False-positive risk: medium; prose may state the basis in an adjacent sentence, so scan the paragraph, not the sentence.
- Sources: B29 p.210-213; B05 p.151-152, 182; engine hard rule in commands/ux-case-study.md:153.
- Existing anti-pattern: partial overlap with round-number-stats, before-after-100-percent and fake-line-of-code-count (those catch suspicious round claims on marketing pages, not unsupported metrics in case studies).

### finding-states-problem-not-fix
- Measures: whether each audit or review finding states a user-facing problem before, and separately from, the fix.
- Threshold: finding `title` does not begin with an imperative fix verb (Add, Make, Change, Use, Move, Increase, Remove) and the `fix` field is non-empty and not identical to the title.
- How measured: artifact check on `.ux/last-audit.json` findings and on research-synthesizer output.
- Fixture: fail = title "Make the CTA red"; near-miss pass = title "Primary action loses to secondary nav on first read (same weight)", fix "Double the CTA weight".
- False-positive risk: low; some legitimate titles start with "Use of" (exclude noun phrases).
- Sources: B89 p.174, 176, 309; B20 p.634, 641-644; B09 p.43, 131-132.
- Existing anti-pattern: none.

### research-vague-quantifier
- Measures: vague quantity words in research findings where a count should be.
- Threshold: zero occurrences of "most users", "many users", "some participants", "a lot of users", "few people" (and equivalents) in a finding unless an "N of M" or percentage with n appears in the same paragraph.
- How measured: artifact check on research reports and synthesis output.
- Fixture: fail = "Most users struggled with checkout."; near-miss pass = "Most users (5 of 8) abandoned checkout at the address step."
- False-positive risk: low to medium; quoted participant speech should be excluded.
- Sources: B03 p.553. The engine already asks for this in prose at agents/research-synthesizer.md:43.
- Existing anti-pattern: none.

### critique-comment-has-reason
- Measures: whether each critique win or miss names a specific element and a reason, not a bare verdict.
- Threshold: each item contains a causal connector (because, so, which, since, so that) or a cited principle or goal, and contains none of a banned vague list ("make it pop", "looks good", "I don't like", "needs polish", "feels off", "could be tighter").
- How measured: artifact check on `.ux/last-critique.json` wins and misses.
- Fixture: fail = "The hero feels off."; near-miss pass = "The hero CTA has the same weight as the nav links, so the primary action loses the first read."
- False-positive risk: medium; a reason can be implied by a colon or dash construction, so accept "X: Y" structures with a mechanism noun.
- Sources: B09 p.27-28, 42; B78 p.95-96; B34 p.79; B89 p.56; B95 p.117.
- Existing anti-pattern: none.

### worst-case-content-overflow
- Measures: whether a layout survives real worst-case content (longest titles, long names, long translations).
- Threshold: after injecting a content variant at 2x the longest current string length per text node (and the longest localized string where available), no text node overflows its box (scrollWidth > clientWidth or clipped by overflow hidden) and no line truncates without an ellipsis affordance.
- How measured: render in a browser, swap text, measure overflow.
- Fixture: fail = a card title in a fixed-height box that clips the third line; near-miss pass = the same card with line-clamp and a visible ellipsis plus a title attribute or expansion.
- False-positive risk: medium; intentionally clamped teasers are valid if an ellipsis and full text access exist.
- Sources: B35 p.268-269; B05 p.247; B33 p.119-120.
- Existing anti-pattern: partial: lorem-ipsum-leak (catches filler text) and fixed-height-text-block (catches a risky CSS pattern), neither tests worst-case content.


## Medium impact

### persona-cast-size
- Measures: number of personas in a cast and primary or secondary counts.
- Threshold: warn above 6 personas, fail above 10; exactly 1 primary per interface; warn above 3 secondary, fail above 4.
- How measured: artifact check (count persona entries and their role tags).
- Fixtures: fail, 12 personas, three tagged primary for one app; near-miss pass, 5 personas, one primary, two secondary.
- False-positive risk: low. Multi-interface products need a primary per interface; read an interface field.
- Sources: B50 p.19, 58, 170; B26 p.117-119; B69 p.162-164; B23 p.347; B72 p.57, 66
- Existing anti-pattern: none.

### persona-demographic-ratio
- Measures: balance of demographic fields against behavioral fields in a persona.
- Threshold: fail when demographic fields (age, gender, income, marital status, hobbies, car) outnumber behavior, goal, need, frustration and context fields; warn when a persona has no behavior field at all.
- How measured: artifact check (classify field labels against two keyword lists).
- Fixtures: fail, a card with eight demographic lines and one goal; near-miss pass, age and location plus goals, frequency of use, tools and frustrations.
- False-positive risk: medium. Free-text narratives need field extraction; skip narrative-only personas.
- Sources: B26 p.121; B34 p.61-62; B03 p.503, 509; B09 p.76-77; B35 p.62-66
- Existing anti-pattern: none.

### persona-distinctness
- Measures: whether any two personas differ only in demographics.
- Threshold: every pair differs on at least 1 behavioral variable or goal. Fail when two personas share all behavior and goal values.
- How measured: artifact check (pairwise comparison of normalized behavior and goal fields).
- Fixtures: fail, two personas with identical goals and usage frequency, one aged 25 and one aged 45; near-miss pass, same age band but different usage frequency and goals.
- False-positive risk: medium (free-text paraphrase can hide sameness or difference).
- Sources: B35 p.72-75; B64 p.111; B50 p.81-82; B01 p.18
- Existing anti-pattern: none.

### recruit-buffer
- Measures: over-recruitment against the target sample, so no-shows do not shrink a round.
- Threshold: recruited count at least 1.2 times the target (1.25 for cold or unpaid recruits), and at least one spare or floater per testing day. Warn at target plus 10 percent; fail at no buffer.
- How measured: artifact check of the plan's target and recruited fields.
- Fixtures: fail, target 5 and recruited 5; near-miss pass, target 8 and recruited 10 over two days with one floater each day.
- False-positive risk: low. Panels with guaranteed attendance may justify no buffer; allow a stated reason.
- Sources: B28 p.179; B03 p.136-137, 294-295; B30 p.98; B46 p.828-829; B91 p.185; B27 p.67-68; B96 p.127, 130
- Existing anti-pattern: none. commands/ux-research.md:67 asks for a 30 percent buffer in prose; nothing checks it.
- Merged from: recruit-buffer, test-plan-recruit-buffer.

### survey-overlapping-ranges
- Measures: numeric answer ranges that overlap or leave gaps, in survey drafts and in rendered forms (radio or select options).
- Threshold: 0 overlaps and 0 gaps between consecutive numeric range options.
- How measured: static lint of HTML or JSX option labels and artifact check of survey text (parse a-b ranges, sort, compare bounds).
- Fixtures: fail, options 15-20, 20-25, 25-30; near-miss pass, 15-19, 20-24, 25-29.
- False-positive risk: low. Continuous decimal ranges (0-1.5, 1.5-3) need an inclusive or exclusive convention; skip when one is stated.
- Sources: B02 p.321-322
- Existing anti-pattern: none.

### rating-scale-points
- Measures: agreement and satisfaction scales, in survey drafts and in rendered feedback widgets.
- Threshold: an agreement or satisfaction scale has an odd count with a neutral midpoint: 5 or 7 points (3 allowed for very short pulses, 11 allowed for 0 to 10 recommend scales). All items in one block share one scale. Item tone does not alternate unless the instrument is a named standard (SUS alternates on purpose).
- How measured: static lint of HTML/JSX (fieldset or role="radiogroup" whose legend or name matches rating, likert, agree, satisfied, satisfaction, scale; count options) plus an artifact check on survey drafts.
- Fixtures: fail, a 4-option strongly disagree to strongly agree group with every other item reversed; near-miss pass, the same group with a neither agree nor disagree option in the middle (5 options), all items positively worded.
- False-positive risk: medium. Yes or no and frequency questions are legitimately even; restrict to agreement and satisfaction wording, and whitelist named instruments.
- Sources: B94 p.205, 223-227; B03 p.331, 355; B28 p.235-236; B20 p.482-483; B02 p.324
- Existing anti-pattern: none. Note references/process/lean-ux-klein.md:139 currently advises removing the midpoint (see gaps.md).
- Merged from: survey-scale-points, rating-scale-point-count.

### survey-length
- Measures: estimated survey completion load, on a page or in a survey artifact.
- Threshold: warn above 10 items or an estimated 10 minutes (split anything longer on mobile); fail above 30 items or an estimated 20 minutes. Estimate about 30 seconds per closed item, 90 seconds per open item, plus instructions.
- How measured: static lint of a survey form (count question fieldsets across all pages) or artifact check of a generated survey.
- Fixtures: fail, a 36-question single-page mobile survey; near-miss pass, 10 closed items in two short sections.
- False-positive risk: low. Multi-page surveys need every page counted.
- Sources: B03 p.357; B46 p.138; B66 p.79-80; B58 p.506, 665-666; B11 p.69
- Existing anti-pattern: none.
- Merged from: survey-length, survey-too-long.

### survey-other-option
- Measures: closed multiple-choice items that lack an escape option.
- Threshold: every single or multi-select item includes other, none, or not applicable unless the options are provably exhaustive (for example yes or no).
- How measured: artifact check of survey drafts; static lint of rendered option groups.
- Fixtures: fail, a which-tool-do-you-use item listing four products only; near-miss pass, the same list plus other with a text field.
- False-positive risk: medium (exhaustive numeric ranges need no other option).
- Sources: B23 p.248-249; B69 p.180; B02 p.325
- Existing anti-pattern: none.

### journey-map-size
- Measures: phase and step counts on chronological maps.
- Threshold: 4 to 12 phases; warn above 15 steps, fail above 20.
- How measured: artifact check (count phase columns and step cards).
- Fixtures: fail, a map with 3 phases and 34 steps; near-miss pass, 5 phases and 14 steps.
- False-positive risk: low to medium (detailed task-analysis layers beneath a map are allowed more steps).
- Sources: B64 p.164; B81 p.71-72; B34 p.181
- Existing anti-pattern: none.

### journey-map-state-label
- Measures: whether a map declares current versus future state and verified versus hypothesis.
- Threshold: both labels present.
- How measured: artifact check (title or metadata fields).
- Fixtures: fail, an unlabeled map built in a stakeholder workshop; near-miss pass, a map titled current state, hypothesis, to be verified with 6 interviews.
- False-positive risk: low.
- Sources: B67 p.20-24; B06 p.114-117
- Existing anti-pattern: none.

### consent-form-items
- Measures: consent form completeness and length.
- Threshold: covers recording, who sees data, right to withdraw and retention as separate items; fits on one page (about 400 words); not merged with an NDA or incentive receipt.
- How measured: artifact check (keyword presence per item and word count).
- Fixtures: fail, a two-page legal release that bundles NDA, payment and consent; near-miss pass, a one-page form with four checkbox items.
- False-positive risk: low to medium (jurisdictions may require extra clauses that lengthen it).
- Sources: B17 p.60-61; B30 p.127-131; B03 p.144
- Existing anti-pattern: none.

### case-study-method-disclosure
- Measures: whether a case study or portfolio page states how its research evidence was gathered.
- Threshold: names at least one method, a participant count and one limit or caveat whenever the page claims research findings.
- How measured: render or static check of the case study page text (regex for method terms near a number of participants).
- Fixtures: fail, a case study claiming users loved the redesign with no method or n; near-miss pass, a line stating 8 interviews and 5 moderated tests, small sample, directional.
- False-positive risk: medium (pages that make no research claim should be skipped).
- Sources: B50 p.56, 96; B30 p.62; B29 p.180
- Existing anti-pattern: none.

### within-subjects-counterbalance
- Measures: test plans where each participant sees two or more designs or a fixed set of tasks in sequence.
- Threshold: any within-subjects comparison states an order rotation (alternating, Latin square or random). 0 fixed-order comparisons.
- How measured: artifact check of the plan's comparison section (detect several variants per participant, then look for order or rotation text).
- Fixtures: fail, each participant sees design A, then design B; near-miss pass, odd-numbered participants see A first and even-numbered see B first.
- False-positive risk: low.
- Sources: B28 p.113-115; B94 p.72, 80; B27 p.61, 77, 157; B85 p.181-182; B58 p.149; B12 p.396; B41 p.187
- Existing anti-pattern: none.
- Merged from: within-subjects-counterbalance, test-plan-no-counterbalance.

### test-task-step-instructions
- Measures: tasks written as instructions rather than goals.
- Threshold: 0 tasks containing navigation verbs aimed at the interface ("click", "tap", "press", "select the", "go to the", "scroll to", "open the menu").
- How measured: artifact check; regex over task lines of the test plan.
- Fixtures: fail, "Click Accounts, then tap Add card". Near-miss pass, "Add your new debit card so you can pay with it tomorrow".
- False-positive risk: low. Troubleshooting tasks that recreate a fault may need a setup step; allow a marked setup line before the task.
- Sources: B85 p.270; B81 p.213-214; B20 p.405-408; B27 p.46, 64
- Existing anti-pattern: none

### test-plan-thinkaloud-with-timing
- Measures: plans that ask for concurrent think-aloud on the same tasks whose time-on-task is reported as a metric, or that combine think-aloud with eye tracking.
- Threshold: 0 tasks tagged both "think-aloud" (concurrent) and "time-on-task" or "eye tracking".
- How measured: artifact check of the test plan's protocol and metrics sections.
- Fixtures: fail, a plan with "participants think aloud throughout" and "report mean time on task per task". Near-miss pass, think-aloud for tasks 1 to 4 and silent, timed tasks 5 to 6 with a retrospective review afterwards.
- False-positive risk: low. Plans may report time as a rough note rather than a metric; only flag when time is a stated metric or target.
- Sources: B28 p.92, 118, 243; B06 p.224; B17 p.75-76
- Existing anti-pattern: none

### test-plan-session-overlong
- Measures: session length and task load in a moderated test plan.
- Threshold: warn when planned session time exceeds 60 minutes without a stated reason or break; fail above 120 minutes; warn when task time exceeds 45 minutes or there are more than 7 tasks in a 60-minute session.
- How measured: artifact check summing the plan's timed blocks and counting tasks.
- Fixtures: fail, a 150-minute session with 12 tasks. Near-miss pass, a 75-minute session with a 10-minute break, 6 tasks and 40 minutes of task time.
- False-positive risk: low to medium. Contextual inquiries and diary debriefs follow different norms; scope to task-based usability tests.
- Sources: B23 p.171; B06 p.214; B77 p.146; B03 p.296, 300-301; B58 p.285; B20 p.554
- Existing anti-pattern: none

### prototype-placeholder-data
- Measures: placeholder content in prototypes and wireframes meant for user testing: lorem ipsum, labeled field placeholders ("[First Name]", "Name Surname"), masks ("$###.##", "MM/DD/YYYY", "XXX"), repeated identical values.
- Threshold: 0 such strings in a prototype marked for testing; labeled placeholders allowed only in spec documents.
- How measured: static lint of prototype HTML or exported frames' text.
- Fixtures: fail, a test prototype account list showing "[Account Name]" and "$###.##" on every row. Near-miss pass, plausible names and amounts, with one row deliberately empty to show the empty state.
- False-positive risk: medium. Legitimate input masks inside form placeholders, and code samples, may match; skip input placeholder attributes and code blocks.
- Sources: B27 p.152-153; B62 p.238-240; B12 p.420-421; B74 p.27-28, 56
- Existing anti-pattern: partial. lorem-ipsum-leak, placeholder-token-shipped and fake-name-john-doe cover shipped code; none covers bracketed field placeholders or masks in prototypes.

### heuristic-review-single-evaluator
- Measures: expert review reports that present a single evaluator's pass as a complete usability evaluation.
- Threshold: report must state the number of independent evaluators; when it is 1, the report must carry a limitation note (expected coverage about a third of problems) and recommend user testing. Fail when neither the count nor the note is present.
- How measured: artifact check of the audit report metadata and summary.
- Fixtures: fail, an audit summary claiming "the interface has no major usability issues" from one reviewer. Near-miss pass, the same audit stating "single evaluator, expect roughly 35 percent coverage; validate the top five findings with a five-person test".
- False-positive risk: low.
- Sources: B89 p.51, 57-58, 199, 210-211; B46 p.809-814; B02 p.612-617; B30 p.153-156
- Existing anti-pattern: none

### survey-precision-mismatch
- Measures: survey plans or results that claim prevalence ("X percent of users") at a precision the sample cannot support. Replaces a fixed n floor with the margin of error.
- Threshold: margin of error = 1.96 x sqrt(0.25 / n) above 10 percentage points (n under about 96) while the artifact states a percent as a finding without a caveat.
- How measured: artifact check; compute the margin from n and flag uncaveated percent claims.
- Fixture: fail "Survey (n=40): 55% prefer weekly billing". Near-miss pass "Survey (n=400): 55% prefer weekly billing (+/- 5 points)".
- False-positive risk: low.
- Sources: B94 p.36-37, 139; B30 p.232; B03 p.368, 385-386
- Existing anti-pattern: none

### task-time-arithmetic-mean
- Measures: task times summarized only by an arithmetic mean.
- Threshold: a reported "average time" or "mean time" with no median or geometric mean beside it; when n < 25 expect the geometric mean, otherwise the median.
- How measured: artifact check on usability reports: find time-on-task statistics and look for "median" or "geometric".
- Fixture: fail "Average time on task: 4.4 min (n=9)". Near-miss pass "Median 3.0 min, geometric mean 3.2 min, range 2.1 to 16 (n=9)".
- False-positive risk: low; analytics session averages over huge samples should be excluded by requiring an n under 1,000.
- Sources: B94 p.46-49, 53; B28 p.289-292; B14 p.163; B02 p.357
- Existing anti-pattern: none

### sus-misreported
- Measures: SUS scores that are impossible or misinterpreted.
- Threshold: score within 0 to 100; an individual score is a multiple of 2.5; SUS is never called a percentage; any verbal grade or percentile matches the curved scale (68 is average, the 50th percentile; below about 51.7 is an F); no claim that a score above 50 is above average; a reported mean references the 68 average, a grade or a percentile.
- How measured: artifact check on research reports and case studies that mention SUS.
- Fixtures: fail, "SUS 72 percent satisfaction" or "SUS of 62, comfortably above average"; near-miss pass, "mean SUS 72.5 (n=12), above the 68 average".
- False-positive risk: low.
- Sources: B94 p.213, 215-222; B20 p.482-483; B11 p.69
- Existing anti-pattern: none.
- Merged from: sus-misreported, sus-score-misread.

### nps-misbanded
- Measures: NPS computed with wrong bands or as a mean.
- Threshold: promoters must be 9 to 10, detractors 0 to 6; NPS must be percent promoters minus percent detractors within -100 to 100; flag "average NPS of 7.8", bands like "promoters 8 to 10", or values outside the range.
- How measured: artifact check on research output and dashboards specs; in rendered pages, check any NPS gauge widget's min and max are -100 and 100.
- Fixture: fail "NPS 8.1 (average of responses)". Near-miss pass "NPS +21 (45% promoters, 24% detractors, n=310)".
- False-positive risk: low.
- Sources: B94 p.33, 71
- Existing anti-pattern: none (data/components.json:4950 mentions an NPS gauge without range rules)

### task-success-criteria-missing
- Measures: usability test tasks without a defined end state, pass rule or target.
- Threshold: every task names its observable end point and pass rule (for example whether one wrong turn still counts), and a target success rate (70 percent default for first rounds; 100 percent only for harm or data-loss tasks). Assisted and unassisted success are recorded separately.
- How measured: artifact check that each task block has a non-empty success or done-when field and a target.
- Fixtures: fail, "Task 2: find the refund policy" with nothing else; near-miss pass, "Task 2: reach the refund policy page unaided within 90 s; target 70 percent".
- False-positive risk: low. Exploratory concept sessions may skip it with an explicit exploratory flag.
- Sources: B28 p.81, 118, 123, 126-127, 296-297; B30 p.168-170, 222-225; B20 p.397-424
- Existing anti-pattern: none. commands/ux-research.md asks for success criteria in prose.
- Merged from: task-success-criteria-missing, test-plan-missing-success-criteria.

### ab-plan-multiple-changes
- Measures: A/B test plans whose variant changes more than one element without a multivariate design, or that lack a pre-declared primary metric and sample size.
- Threshold: variant description lists 2 or more changed elements while the design is labelled A/B; or primary metric or target n is missing.
- How measured: artifact check of experiment plans.
- Fixture: fail "Variant B: new headline, green button, shorter form". Near-miss pass "Variant B: shorter form only; primary metric sign-up completion; n = 2 x 1,900".
- False-positive risk: medium; a deliberate bundle test ("does the whole redesign beat control") is valid if labelled as such.
- Sources: B34 p.135-136; B27 p.82-83, 199, 212-213; B02 p.634-635
- Existing anti-pattern: none

### severity-without-frequency
- Measures: findings from user testing that carry a severity but no count of affected participants.
- Threshold: every finding from a session with participants lists "n of N participants" (or an estimated share). 0 findings without it. Inspection-only findings may carry "frequency unknown".
- How measured: artifact check of `.ux/last-audit.json`, findings lists and test reports.
- Fixtures: fail, a High finding that users could not find the transfer button with no count; near-miss pass, the same finding with 4 of 5 participants.
- False-positive risk: low once inspection-only findings are exempt (evidence kind heuristic).
- Sources: B28 p.299-301; B94 p.30, 43; B30 p.210-212; B89 p.72-80; B81 p.226-227; B17 p.159
- Existing anti-pattern: none.
- Merged from: severity-without-frequency, test-findings-severity-without-frequency.

### case-study-summary-first
- Measures: whether a portfolio case study can be judged in the first minute.
- Threshold: problem, role and result all appear within the first 150 words (or the first viewport of a rendered page); total core narrative at or under about 1,200 words for portfolio pieces.
- How measured: artifact check (word positions of problem, role and outcome markers) or render and read the first viewport.
- Fixture: fail = 400 words of company background before the problem; near-miss pass = a three-line overview block "Problem / Role / Result" under the title.
- False-positive risk: medium; long-form retrospectives that are not portfolio pieces should be exempt by mode.
- Sources: B30 p.326-327; B29 p.210, 231; B95 p.247-248.
- Existing anti-pattern: none.

### case-study-concept-labelled
- Measures: whether unshipped or self-initiated work is labeled as concept.
- Threshold: if a case study has no launch date, no shipped artifact and no measured outcome, it must contain a label such as "concept", "speculative", "self-initiated" or "unshipped".
- How measured: artifact check on case-study text and `.ux/last-case-study.json` facts.
- Fixture: fail = a redesign of a well-known app with invented impact and no label; near-miss pass = "Self-initiated concept, not affiliated with the company" in the overview.
- False-positive risk: medium; shipped internal tools may lack public dates.
- Sources: B29 p.211, 220-221.
- Existing anti-pattern: none.

### case-study-process-evidence
- Measures: whether a case study shows intermediate thinking, not only final screens.
- Threshold: at least one figure whose caption or alt text names a process artifact (sketch, wireframe, research, map, flow, test, prototype).
- How measured: artifact check over figures, captions and alt text.
- Fixture: fail = five polished screenshots captioned only with route names; near-miss pass = one early wireframe captioned "First wireframe, tested with 5 members".
- False-positive risk: medium; process may be described in prose rather than shown.
- Sources: B84 p.18, 49, 97; B29 p.284-285; B25 p.7-10.
- Existing anti-pattern: none.

### report-conclusion-first
- Measures: whether a research or audit report leads with a conclusion and a short theme list.
- Threshold: the first 300 words contain a one-sentence overall conclusion and the report has 8 or fewer top-level themes (debrief focus on the 5 most severe problems).
- How measured: artifact check on report Markdown or HTML (heading count, first-section length).
- Fixture: fail = a report opening with methodology and 14 themes; near-miss pass = a one-line conclusion, then 6 themes, then method.
- False-positive risk: low to medium.
- Sources: B03 p.553, 560-561; B17 p.148-150; B28 p.307-309, 311-312; B30 p.276-281.
- Existing anti-pattern: none.

### report-has-positive-findings
- Measures: whether an audit or usability report records what works.
- Threshold: at least one positive finding or strengths entry per report.
- How measured: artifact check on `.ux/last-audit.json` (a non-empty strengths array) or report sections.
- Fixture: fail = 18 problems and no strengths; near-miss pass = 18 problems and 2 named strengths to keep.
- False-positive risk: low.
- Sources: B28 p.307-309, 313-317; B89 p.109, 111; B58 p.455-456; B09 p.47-48.
- Existing anti-pattern: none.

### problem-statement-no-solution
- Measures: whether a problem statement is single and solution-free.
- Threshold: no solution phrasing ("build a", "add a", "launch", "app by", platform or feature names) and no compound joining two problems with "and" or "or" at clause level.
- How measured: artifact check on brief or framing text.
- Fixture: fail = "We need to launch an iOS app and redesign onboarding by Q2"; near-miss pass = "New partners in their first 14 days cannot tell which rules apply to them, so 40 percent never configure one."
- False-positive risk: medium; "and" inside a noun phrase is legitimate.
- Sources: B34 p.49-51; B96 p.55, 66; B72 p.25.
- Existing anti-pattern: none.

### feature-traces-to-need
- Measures: whether every listed feature or functional requirement references a user need or outcome.
- Threshold: 100 percent of feature rows have a non-empty need or outcome reference.
- How measured: artifact check on feature lists, requirement tables or hypothesis backlogs.
- Fixture: fail = a features table with a "Social sharing" row and no linked need; near-miss pass = the same row citing "N3: members want to show status to friends".
- False-positive risk: low.
- Sources: B57 p.51-53; B34 p.65-66; B06 p.141, 169-175; B67 p.70-71.
- Existing anti-pattern: none.

### design-handoff-a11y-annotations
- Measures: whether a handoff spec carries accessibility annotations.
- Threshold: handoff includes heading levels, landmarks, focus or reading order, and alt text or decorative flags for every image in scope.
- How measured: artifact check on handoff JSON or Markdown.
- Fixture: fail = a spec with spacing and colors only; near-miss pass = a spec with headings, landmarks and focus order but one decorative image flagged as such.
- False-positive risk: low.
- Sources: B80 p.35-36; B32 p.62-63; B18 p.219-224.
- Existing anti-pattern: none (code-level checks exist, for example img-no-alt and heading-skip-h1-h3, but not spec-level).

### workshop-size-and-roles
- Measures: whether a workshop plan fits its activity and names a decider and a neutral facilitator.
- Threshold: ideation or convergence sessions have 8 or fewer participants (mapping up to 12 in breakouts); when users attend, stakeholders do not outnumber users; plan names a decider and a facilitator who is not the product owner.
- How measured: artifact check on `.ux/last-workshop.json` participants and roles.
- Fixture: fail = 14 participants in one ideation room, no decider; near-miss pass = 8 participants, a named decider, and a facilitator separate from the PM.
- False-positive risk: low to medium; role names vary.
- Sources: B23 p.281, 300; B35 p.91; B34 p.76-81; B64 p.212-213; B67 p.52; B81 p.147; B96 p.42-45.
- Existing anti-pattern: none.

### principle-too-generic
- Measures: whether design principles are specific enough to reject options.
- Threshold: no principle consists only of a generic adjective or two-word phrase from a list (simple, clean, modern, intuitive, fun, delightful, user-friendly, seamless).
- How measured: artifact check on principles lists in briefs or design-system docs.
- Fixture: fail = "Simple."; near-miss pass = "Simple: one primary action per screen, secondary actions behind a menu."
- False-positive risk: low.
- Sources: B09 p.36, 82, 183; B26 p.161.
- Existing anti-pattern: none (filler-marketing-verbs covers page copy, not principles).

### portfolio-contact-reachable
- Measures: whether contact is one step away on every portfolio page.
- Threshold: every page in a portfolio site has a mailto link or a link to a contact route in header or footer.
- How measured: static lint across the site's pages, or render and query.
- Fixture: fail = contact only on the About page; near-miss pass = footer mailto on every page.
- False-positive risk: low.
- Sources: B05 p.199-200.
- Existing anti-pattern: none.

### brief-expression-share
- Measures: balance of a design brief's content.
- Threshold: 500 to 1,500 words; sections on look and feel (expression) at least 25 percent of words; process sections at most 55 percent.
- How measured: artifact check by heading classification and word counts.
- Fixture: fail = 900 words, 70 percent schedule and process; near-miss pass = 700 words with 26 percent on expression.
- False-positive risk: medium; needs reliable section headings.
- Sources: B72 p.40-43.
- Existing anti-pattern: none.


## Low impact

### persona-length
- Measures: persona description length.
- Threshold: warn above about 1,000 words (two pages); fail above 2,000.
- How measured: artifact check (word count per persona, excluding the linked foundation document).
- Fixtures: fail, a 3-page biography; near-miss pass, a 600-word narrative with a key-facts sidebar.
- False-positive risk: low.
- Sources: B26 p.120; B64 p.111; B50 p.82
- Existing anti-pattern: none.

### persona-review-date
- Measures: persona freshness.
- Threshold: a last-validated date within 24 months.
- How measured: artifact check (date field).
- Fixtures: fail, a persona last validated three years ago; near-miss pass, validated 20 months ago.
- False-positive risk: low.
- Sources: B50 p.22, 166; B34 p.61, 64
- Existing anti-pattern: none.

### journey-map-persona-count
- Measures: personas per journey map.
- Threshold: at most 2 personas on one map.
- How measured: artifact check (persona header count).
- Fixtures: fail, one map covering four personas; near-miss pass, one primary and one secondary persona.
- False-positive risk: low.
- Sources: B67 p.16, 34
- Existing anti-pattern: none.

### task-tree-subgoal-count
- Measures: breadth of hierarchical task analyses and task flowcharts.
- Threshold: warn when a goal node has more than 4 direct subgoals.
- How measured: artifact check (tree depth and fan-out from an outline or diagram export).
- Fixtures: fail, a goal with 7 children; near-miss pass, a goal with 4 children.
- False-positive risk: medium (some menus or checklists are legitimately flat).
- Sources: B03 p.530-533
- Existing anti-pattern: none.

### scenario-has-obstacle
- Measures: whether written scenarios include an obstacle or failure path.
- Threshold: each scenario includes at least 1 obstacle, error or negative branch, and an ending stating whether the goal was reached.
- How measured: artifact check (section or keyword presence).
- Fixtures: fail, a scenario where every step succeeds; near-miss pass, a scenario where a payment fails and the persona retries.
- False-positive risk: medium (keyword detection is crude).
- Sources: B50 p.105-110, 119-120
- Existing anti-pattern: none.

### prototype-totals-do-not-add-up
- Measures: tables and summaries in a prototype whose stated totals differ from the sum of their line items.
- Threshold: 0 mismatches beyond rounding (difference greater than 0.5 percent of the total).
- How measured: render in a browser, parse tables or lists with numeric cells and a row labeled total or sum, compare.
- Fixtures: fail, a cart with items 12.00, 8.50 and a total of 25.00. Near-miss pass, the same cart with a separate delivery line of 4.50 and a total of 25.00.
- False-positive risk: medium to high. Hidden fees, taxes or discounts outside the table cause false alarms; only check when every contributing line is inside the same table.
- Sources: B12 p.420-421; B81 p.193-196
- Existing anti-pattern: none

### wireframe-color-discipline
- Measures: wireframes that carry decorative color.
- Threshold: in an artifact marked as a wireframe, saturated colors (HSL saturation above 30 percent) appear only on links and buttons (one interactive hue) and error text (one red); 0 other saturated fills or text.
- How measured: render in a browser and sample computed colors per element class; artifact must be flagged as a wireframe (file name or data attribute).
- Fixtures: fail, a wireframe with a purple gradient hero and green cards. Near-miss pass, a gray wireframe with blue buttons and one red error message.
- False-positive risk: medium; teams that deliberately test color in mid-fidelity frames will trip it, so only run on artifacts flagged as wireframes.
- Sources: B62 p.231-237; B38 p.28, 46; B47 p.12-13; B06 p.191-192
- Existing anti-pattern: none

### sticky-metric-as-success
- Measures: success metrics that reward users staying longer.
- Threshold: "time on site", "session length", "time spent" or "pages per session" listed as the primary success metric for a task-oriented surface.
- How measured: artifact check of frames, case studies and metric plans.
- Fixture: fail "Success: increase time on site by 20%" for a checkout flow. Near-miss pass "Success: checkout completion up 5 points; guard: time to complete does not rise".
- False-positive risk: medium for content and media products where dwell can be a valid goal.
- Sources: B23 p.231; B63 p.281-283
- Existing anti-pattern: none

### sprint-plan-shape
- Measures: design sprint or workshop plans that break the sprint shape.
- Threshold: core team over 7 people; no named Decider; no user-test block; a working day over 7 hours; or a stretch longer than 120 minutes without a break.
- How measured: artifact check of a workshop or sprint agenda (participants list and timed blocks).
- Fixture: fail a 5-day agenda with 12 participants and 3-hour blocks. Near-miss pass 7 participants with a named Decider, 90-minute blocks, test day on day 5.
- False-positive risk: medium; short design-thinking workshops (not sprints) should only be checked for breaks and group size.
- Sources: B81 p.12, 35-48, 96; B96 p.24, 35, 41, 49; B09 p.116
- Existing anti-pattern: none

### accuracy-only-model-metric
- Measures: AI feature specs or case studies that report a model only by accuracy when the positive class is rare.
- Threshold: accuracy stated with no precision, recall, F-measure or confusion matrix, where the spec mentions detection, fraud, alerts, flags or anomalies.
- How measured: artifact check.
- Fixture: fail "Fraud model: 95% accurate". Near-miss pass "Fraud model: precision 42%, recall 30% at 5% base rate; accuracy 94.5%".
- False-positive risk: medium for balanced classification tasks.
- Sources: B61 p.151-154; B43 p.215-216, 225-226; B51 p.365-367
- Existing anti-pattern: none

### portfolio-password-gate
- Measures: password-gated case studies on a public portfolio.
- Threshold: no `input[type=password]` on portfolio case-study routes without a visible public alternative.
- How measured: static lint of portfolio pages.
- Fixture: fail = case study behind a password form with no request path; near-miss pass = public summary with an optional gated appendix.
- False-positive risk: medium; client portals legitimately need passwords, so scope to portfolio sequences only.
- Sources: B29 p.210-212.
- Existing anti-pattern: none.

### portfolio-stock-imagery
- Measures: stock photography or untouched template mockups in case studies.
- Threshold: no case-study image sourced from common stock hosts or named with template markers (mockup-template, stock, unsplash) without a caption crediting real project use.
- How measured: static lint of image src and filenames.
- Fixture: fail = a sticky-note stock photo in the research section; near-miss pass = a photo of the real workshop wall with caption.
- False-positive risk: medium.
- Sources: B29 p.210-212; B05 p.214-215.
- Existing anti-pattern: partial: unsplash-photo-id-no-alt, picsum-photos-seed, placeholder-com-direct (they flag placeholder sources, not portfolio context).

### resume-machine-readable
- Measures: whether a resume is parseable and free of skill bars.
- Threshold: extracted text of at least 300 characters (not image-only), and no progress bars or percentage meters next to skill names.
- How measured: artifact check (PDF text extraction; HTML query for progress elements or width-percent bars in a skills section).
- Fixture: fail = image-only PDF with skill bars; near-miss pass = text PDF that lists skill levels in words.
- False-positive risk: low.
- Sources: B29 p.254-256; B05 p.285, 292.
- Existing anti-pattern: none.

### highlight-reel-length
- Measures: length of findings videos for stakeholders.
- Threshold: total at most 5 minutes; each clip at most 3 minutes (prefer under 1).
- How measured: artifact check on video metadata.
- Fixture: fail = a 14-minute reel; near-miss pass = 4 minutes 40 seconds with clips under a minute.
- False-positive risk: low; team-internal compilations can be exempt.
- Sources: B77 p.197; B17 p.166; B03 p.561-564.
- Existing anti-pattern: none.

### team-user-exposure
- Measures: whether each team member gets direct exposure to users.
- Threshold: at least 2 hours of observed sessions per person every 6 weeks.
- How measured: artifact check on a research log or dashboard listing observers per session.
- Fixture: fail = engineers absent from all sessions in a quarter; near-miss pass = every member at 2 hours in the window.
- False-positive risk: medium; depends on a maintained log.
- Sources: B30 p.23, 240-241.
- Existing anti-pattern: none.


<!-- cluster B: visual, system and platform -->

# checks: cluster B (visual, system and platform)

Lessons that can become a measurable check on a page. Methods: static (lint of HTML, CSS, JSX or token files), render (headless browser, computed styles and geometry), interaction (scripted input and timing). "Existing" names the rule in data/anti-patterns.json or the render rule id in engine/render when one already covers it, fully or in part.

Checks are ordered by impact: standard-backed and high-confidence first, advisory heuristics last.

## Priority 1: standard-backed or high confidence, not yet covered

### text-measure-too-long
- Measures: characters per line of rendered running text (p and li inside main or article): the rendered width divided by the average glyph advance of the computed font.
- Threshold: fail above 80 characters (WCAG 1.4.8). Warn above 75. Warn below 35 in a single-column body.
- How: render.
- Fixture: fail is an 18px paragraph in a 1200px container (about 130 characters). Near-miss pass is the same paragraph at max-width 70ch.
- False-positive risk: medium. Exclude pre, td, figcaption, pull quotes and blocks under 3 lines.
- Sources: B88 p.126-127; B18 p.141; B92 p.55; B47 p.114-116
- Existing: none. references/foundations/typography.md:353 is a manual checklist item.

### reflow-at-320-and-text-zoom
- Measures: horizontal overflow and clipped text at a 320px viewport, and at 1280px with text at 200 percent.
- Threshold: fail when document scrollWidth exceeds the viewport, or text overflows its box, in either pass.
- How: render.
- Fixture: fail is a card with min-width 400px. Near-miss pass is the same card with width min(100%, 400px).
- False-positive risk: low. Data tables, maps and toolbars are exempt under WCAG 1.4.10.
- Sources: B91 p.115, 245, 263; B18 p.129-131; B59 p.11
- Existing: horizontal-overflow and text-overflows-its-box, but the render VIEWPORTS start at 390px (engine/render/core.py:25) and there is no text-zoom pass. Extend the existing rules rather than add a new one.

### link-distinguishable-without-color
- Measures: inline links inside a paragraph of body text. Checks for an underline or border-bottom (or a weight change), and the contrast between the link color and the surrounding text color.
- Threshold: fail when the link has no underline or other non-color cue AND its color is under 3:1 against the surrounding text (WCAG 1.4.1, technique G183).
- How: render.
- Fixture: fail is a link in the brand accent with text-decoration none inside charcoal body text at 2.1:1. Near-miss pass is the same link with an underline at 1px offset.
- False-positive risk: low. Exclude nav, buttons and cards that are whole-block links.
- Sources: B77 p.48-49; B80 p.116, 121; B86 p.279
- Existing: none. references/foundations/color.md:204 puts the accent on inline links with no non-color cue.

### chart-series-color-only
- Measures: charts (svg, canvas with data attributes, or known chart library configs) with two or more series or categories. Looks for at least one non-color cue per series: a direct label, legend text, marker shape, stroke-dasharray or fill pattern.
- Threshold: fail when series differ only in fill or stroke color.
- How: static lint of chart configs (Recharts, Chart.js, Vega-Lite, ECharts) plus render of inline svg.
- Fixture: fail is a three-line chart with no legend and solid strokes in three hues. Near-miss pass is the same chart with end-of-line labels.
- False-positive risk: medium. A legend counts as a cue only when it is visible and near the chart.
- Sources: B18 p.154-155; B91 p.33, 59; B86 p.436-438; B46 p.726, 732-733
- Existing: none. The rule is stated in references/foundations/accessibility.md:150-156 only.

### motion-without-reduced-motion-query
- Measures: CSS or JS that animates transform, scroll-linked motion or parallax, in a project that has no prefers-reduced-motion branch anywhere.
- Threshold: one or more non-trivial transform animations or transitions, and zero reduced-motion media queries or matchMedia checks.
- How: static lint across CSS and JS.
- Fixture: fail is .reveal { transition: transform 600ms } with no media query. Near-miss pass is the same rule plus a reduced-motion override to a 200ms opacity fade.
- False-positive risk: low. Exclude color-only transitions.
- Sources: B26 p.570; B91 p.240; B36 p.272-273
- Existing: infinite-animation-without-reduced-motion covers infinite loops only. The render rule press-moves-under-reduced-motion covers press scale only.

### flash-rate-over-three-per-second
- Measures: repeating animations that change opacity, visibility, background or a luminance-bearing color with a full cycle shorter than 333ms.
- Threshold: more than 3 flashes in any 1 second over an area larger than WCAG's small-area exemption (WCAG 2.3.1).
- How: static lint of keyframes and iteration counts, with a render sampling pass to confirm.
- Fixture: fail is .alert { animation: blink 0.2s infinite } on opacity. Near-miss pass is a spinner rotating at 0.6s infinite (transform only).
- False-positive risk: medium. Small dot loaders flash fast over tiny areas, so gate the check on element area.
- Sources: B91 p.264; B18 p.187, 259; B20 p.832-834
- Existing: blink-tag covers the blink element only.

### carousel-auto-advance
- Measures: a slider or carousel that changes slides with no input during 7 seconds of observation, and whether a pause or stop control exists.
- Threshold: advisory on any auto-advance. Fail when motion runs past 5 seconds with no visible pause, or keeps running under reduced motion.
- How: render plus interaction.
- Fixture: fail is a carousel with autoplay every 4 seconds and no pause. Near-miss pass is the same carousel with a labeled Pause button and autoplay off under reduced motion.
- False-positive risk: low to medium. Overlaps marquee rules.
- Sources: B18 p.99, 183, 259; B91 p.240, 264
- Existing: the render rule moving-content-without-pause covers the hard fail. Add the advisory tier, and remove the 4-second carve-out at references/foundations/motion.md:288.

### body-line-height-too-tight
- Measures: computed line-height divided by font-size on multi-line running text.
- Threshold: fail below 1.4 for text under 20px. Warn below 1.5 (WCAG 1.4.8 and 1.4.12).
- How: render. Static lint also works for unitless values.
- Fixture: fail is a 16px paragraph at line-height 1.2. Near-miss pass is line-height 1.45.
- False-positive risk: low.
- Sources: B88 p.140; B18 p.137-138, 141; B59 p.7; B46 p.201-202
- Existing: display-line-height-under-floor covers display sizes only.

### body-text-too-small
- Measures: computed font-size of rendered running text (p, li, td, label) at phone widths.
- Threshold: fail below 16px for body paragraphs at 390px. Fail below 12px for any reading text except legal small print.
- How: render.
- Fixture: fail is a 14px paragraph at 390px. Near-miss pass is a 16px paragraph with a 12px footer copyright line.
- False-positive risk: low to medium. Badges and tabular metadata at 13px may be intentional, so apply the 16px floor to paragraphs over 2 lines.
- Sources: B86 p.290; B80 p.137; B46 p.201-202; B85 p.131
- Existing: input-text-zooms covers form fields only. MIN_BODY_PX (engine/foundations/typography.py:93) governs generated tokens, not shipped pages.

### button-used-for-navigation
- Measures: a button element whose handler only changes location (router push, location assignment, window.open).
- Threshold: any occurrence.
- How: static lint of JSX, HTML and Vue.
- Fixture: fail is a button whose click only pushes the /pricing route. Near-miss pass is a button that saves, then redirects.
- False-positive risk: medium. Save-then-redirect handlers are fine.
- Sources: B26 p.622-623; B80 p.42-45; B91 p.72, 81; B23 p.465; B22 p.260
- Existing: link-onclick-no-href, anchor-no-href-as-button and role-button-on-anchor-without-href cover the inverse case only.

### dialog-without-name
- Measures: role dialog or alertdialog, or a dialog element, with no aria-labelledby or aria-label.
- Threshold: any.
- How: static lint.
- Fixture: fail is a div with role dialog and no name. Near-miss pass is the same div with aria-labelledby pointing at its h2.
- False-positive risk: low.
- Sources: B80 p.86-87; B91 p.70-71, 264
- Existing: none.

### dialog-not-dismissable
- Measures: whether an open dialog closes on Escape and has a visible close or cancel control.
- Threshold: fail when a dialog lacks either one.
- How: interaction.
- Fixture: fail is an email gate with no close button that ignores Escape. Near-miss pass is a confirm dialog with a Cancel button that also closes on Escape.
- False-positive risk: low.
- Sources: B91 p.70-71; B20 p.208-210; B80 p.82-85; B78 p.16
- Existing: the render rule focus-lost-after-escape covers focus return only.

### hover-only-disclosure
- Measures: menus or content shown only by :hover, with no :focus-within, :focus-visible or click path.
- Threshold: any :hover rule that changes display, visibility or opacity of a descendant menu without a matching focus or tap path.
- How: static lint of selectors, confirmed by tabbing.
- Fixture: fail is a nav menu (.nav li:hover > ul) that opens on hover only. Near-miss pass adds a :focus-within rule and a toggle button.
- False-positive risk: medium. Exclude purely decorative hover effects.
- Sources: B77 p.163; B14 p.54-55, 93; B52 p.142-143; B23 p.568, 620
- Existing: hover-only-card-actions covers actions set to opacity 0. Extend it to menus.

### layout-shift-over-budget
- Measures: cumulative layout shift during load and the first interactions.
- Threshold: CLS over 0.1 (Core Web Vitals).
- How: render with a PerformanceObserver for layout-shift entries at 390px and 1280px.
- Fixture: fail is a hero image with no dimensions that pushes text down 300px after load. Near-miss pass is the same image with width and height set.
- False-positive risk: low.
- Sources: B52 p.222, 282; B44 p.72-74
- Existing: img-no-dimensions covers the main static cause. There is no measured render rule (the guide is at references/foundations/seo.md:374).

## Priority 2: color and data checks (high value, need calibration)

### equal-lightness-adjacent-fills
- Measures: pairs of adjacent painted regions (bands, cards on bands, pills on fills, text on chromatic fills) whose hues differ strongly while their lightness is nearly equal.
- Threshold (starting point to calibrate): both colors have OKLCH chroma above 0.08, hue difference above 60 degrees, and WCAG contrast below 1.5:1 between them. Flag as a vibrating or vanishing boundary.
- How: render. Sample the computed backgrounds of neighboring boxes and of text on fills.
- Fixture: fail is saturated red text on a saturated green band of equal lightness. Near-miss pass is the same hues with the band darkened to 3:1.
- False-positive risk: medium. Photos and gradients need sampling at the boundary, not the computed style.
- Sources: B90 p.88-90; B76 p.182, 186, 188, 191; B70 p.41-42; B20 p.832-834
- Existing: text-low-contrast catches text cases below 4.5:1. Nothing checks non-text adjacent fills.

### chromostereopsis-pair
- Measures: saturated red directly on saturated blue (or the reverse), saturated yellow on purple, and pure blue small text or hairlines.
- Threshold: both colors with OKLCH chroma above 0.15 and hues in the red band (about 20 to 40 degrees) and blue band (about 250 to 270 degrees) touching. Or text under 14px whose color has a hue near 265 degrees, chroma above 0.2, on a dark ground.
- How: render.
- Fixture: fail is #FF0000 text on #0000FF. Near-miss pass is a red badge on a near-white card next to a blue link.
- False-positive risk: medium.
- Sources: B20 p.832-834; B46 p.737-738, 752-754
- Existing: none.

### chart-category-count
- Measures: distinct series or slice colors in one chart, line count in a line chart, bar count in a bar chart and slice count in a pie or donut.
- Threshold: fail above 6 categorical colors. Warn above 5 lines, above 12 bars and above 5 pie slices. Warn on any slice under 5 percent.
- How: static lint of chart configs and data arrays, plus render of inline svg.
- Fixture: fail is a pie with 8 slices. Near-miss pass is a pie with 5 slices, the smallest at 6 percent.
- False-positive risk: low to medium. Small multiples and grouped Other slices are fine.
- Sources: B46 p.302, 306-307, 310-311, 733-734, 746-747; B91 p.33; B76 p.116-118
- Existing: none. The guide is at references/surfaces/dashboard.md:309, 320, 358, 410.

### bar-axis-not-zero
- Measures: bar or column charts whose value axis does not start at zero and shows no break marker.
- Threshold: any. Line charts are exempt.
- How: static lint of chart configs (beginAtZero false, a domain not starting at 0, a scale zero false).
- Fixture: fail is a bar chart with a y domain of 90 to 100. Near-miss pass is a line chart with the same domain.
- False-positive risk: low.
- Sources: B02 p.416, 422-423; B46 p.297-298
- Existing: none. The guide is at references/foundations/components.md:341 and references/surfaces/dashboard.md:62.

### chart-3d-or-gauge
- Measures: 3D chart options, perspective transforms on chart containers, and gauge or dial components on dashboards.
- Threshold: fail on 3D. Warn on a gauge whose value could be a labeled number or a bullet chart.
- How: static lint.
- Fixture: fail is a Highcharts options3d enabled. Near-miss pass is a bullet chart with a target marker.
- False-positive risk: low.
- Sources: B86 p.99; B02 p.422-423; B24 p.211, 369-372
- Existing: none.

### numbers-not-tabular
- Measures: table cells and stat tiles whose content is numeric. Checks the computed font-variant-numeric and text-align.
- Threshold: fail when a numeric column lacks tabular-nums or is not right-aligned (end-aligned in RTL).
- How: render.
- Fixture: fail is a price column in proportional figures, left-aligned. Near-miss pass is the same column in tabular-nums, end-aligned.
- False-positive risk: low. Identifier columns such as order numbers may stay start-aligned.
- Sources: B88 p.74-75; B24 p.119
- Existing: none. The guide is a Critical checklist item at references/surfaces/dashboard.md:388.

### too-many-hues-on-screen
- Measures: distinct chromatic hues (OKLCH chroma above 0.05, binned into 30-degree hue sectors) across non-image UI chrome in the first two screens, charts excluded.
- Threshold: warn above 4 hue sectors in chrome.
- How: render.
- Fixture: fail is a page with blue links, a purple CTA, an orange badge, green tags and a teal header. Near-miss pass is one accent plus the status colors in pills.
- False-positive risk: medium. Status pills and illustrations add hues by design, so count them separately.
- Sources: B46 p.193-194, 733-734; B26 p.432, 453; B86 p.283; B59 p.8
- Existing: the render rule color-over-budget measures the chromatic share of area, not the hue count. This would sit beside it.

### contrast-worst-point-on-gradient-or-image
- Measures: text placed over a gradient or background image. Samples the screenshot pixels under the text box and computes contrast at the lightest and darkest points.
- Threshold: fail when the worst point is under 4.5:1 (3:1 for large text).
- How: render with pixel sampling.
- Fixture: fail is white text over a photo with a bright sky behind half the headline. Near-miss pass adds a 60 percent scrim.
- False-positive risk: medium. Anti-aliasing and text shadows complicate sampling.
- Sources: B80 p.113-117, 121; B83 p.582-583
- Existing: text-low-contrast reads gradient stops (engine/render/taste.py:116) but not image pixels.

### ramp-step-evenness
- Measures: in token files, the OKLab L gaps between adjacent steps of each color ramp.
- Threshold: warn when the largest gap is more than 2 times the smallest within one ramp, or when the gap between steps that are assigned different roles is under 0.02 (the engine's JUST_VISIBLE).
- How: static lint of tokens.
- Fixture: fail is a ramp whose 50 to 400 steps sit within 0.18 L and whose 600 to 950 steps spread over 0.6. Near-miss pass is a ramp with gaps of 0.06 to 0.1.
- False-positive risk: low.
- Sources: B90 p.80-81; B68 p.81-82, 97; B46 p.741
- Existing: engine/foundations/ramp.py:42 enforces a MIN_STEP floor only.

### scheme-lightness-intervals
- Measures: in token files, the L difference between paired roles (text default to text muted, page to card, card to raised) in the light scheme against the dark scheme.
- Threshold: warn when a pair's L gap in one scheme is under half its gap in the other.
- How: static lint of tokens.
- Fixture: fail is muted text 0.25 L from default in light but 0.08 in dark. Near-miss pass is 0.25 and 0.18.
- False-positive risk: low to medium. Dark surfaces are intentionally compressed.
- Sources: B90 p.60
- Existing: none.

### near-duplicate-colors
- Measures: pairs of distinct color literals in use whose OKLab distance falls below a just-visible floor.
- Threshold: OKLab distance under about 0.02.
- How: static scan of CSS and JSX color literals.
- Fixture: fail is #1F6FEB and #1E6FEA both used for links. Near-miss pass is #1F6FEB as the base with #1858C4 as hover.
- False-positive risk: low to medium. Gradients and image-matched colors.
- Sources: B22 p.128-131; B07 p.14; B47 p.29-32
- Existing: partial. commands/ux-system.md:236 reports values written several ways, and tailwind-color-named-vague flags raw palette classes.

### link-color-on-non-link
- Measures: headings or non-interactive text rendered in the same color as inline links, with no link role.
- Threshold: any heading or span whose color equals the computed link color and that is not inside an a or button.
- How: render.
- Fixture: fail is an h3 in the link blue with no link. Near-miss pass is an h3 in the text color with a link-blue eyebrow that is itself a link.
- False-positive risk: medium. Brands that use the accent for both need a separate link cue.
- Sources: B77 p.48-49
- Existing: none.

## Priority 3: typography, layout, components (useful, mostly advisory)

### thin-weight-small-text
- Measures: font-weight under 400 on text under 18px.
- Threshold: fail at weight 300 or lighter below 18px.
- How: static lint plus render.
- Fixture: fail is .meta at 13px, weight 300. Near-miss pass is weight 300 on a 48px heading.
- False-positive risk: low.
- Sources: B47 p.40-41; B31 p.92, 180
- Existing: font-weight-numeric-100-or-900-on-body catches 100 on body selectors only.

### all-caps-running-text
- Measures: uppercase text (by transform or in the source) in blocks longer than about 40 characters.
- Threshold: fail above 40 uppercase characters in one block, at any size.
- How: render.
- Fixture: fail is a two-sentence uppercase paragraph at 14px. Near-miss pass is a three-word uppercase eyebrow with +0.08em tracking.
- False-positive risk: low.
- Sources: B46 p.203-205; B26 p.440; B19 p.22, 29
- Existing: all-caps-large keys on font-size, so small uppercase paragraphs slip through.

### caps-without-tracking
- Measures: letter-spacing on uppercase text under 20px.
- Threshold: warn when letter-spacing is 0 or less.
- How: static lint.
- Fixture: fail is an uppercase eyebrow at letter-spacing 0. Near-miss pass is letter-spacing 0.06em.
- False-positive risk: medium. Some faces ship with caps spacing built in.
- Sources: B88 p.136-137; B47 p.132-134; B10 p.171
- Existing: none.

### reversed-small-text-weight
- Measures: light text on a dark ground under 16px with weight under 400 or negative letter-spacing.
- Threshold: fail when either condition holds.
- How: render.
- Fixture: fail is 13px text at weight 300 in #EEE on #111. Near-miss pass is weight 400 with +0.01em tracking.
- False-positive risk: low.
- Sources: B88 p.139; B19 p.29; B18 p.135-136
- Existing: none. Note that references/foundations/typography.md:86 pushes the other way (see gaps.md).

### centered-long-text
- Measures: text-align center on a block of 4 or more rendered lines of body-size text.
- Threshold: fail at 4 lines or more.
- How: render.
- Fixture: fail is a centered 6-line paragraph. Near-miss pass is a centered 2-line hero subhead.
- False-positive risk: low.
- Sources: B47 p.129; B86 p.272-274; B10 p.170
- Existing: centered-everything-hero is static and limited to heroes.

### heading-spacing-inverted
- Measures: the space above a heading against the space below it.
- Threshold: fail when the space below is equal to or greater than the space above.
- How: render.
- Fixture: fail is an h2 with 16px above and 32px below. Near-miss pass is 40px above and 12px below.
- False-positive risk: medium. The first heading in a card has no space above it.
- Sources: B77 p.51, 202; B88 p.141, 226; B10 p.175
- Existing: none.

### proximity-label-ambiguous
- Measures: a form label's distance to its own control against its distance to the previous control.
- Threshold: fail unless the label is at least 1.5 times closer to its own control.
- How: render.
- Fixture: fail is a label 16px above its input with 16px to the previous input. Near-miss pass is 4px to its own input and 24px to the previous one.
- False-positive risk: medium.
- Sources: B47 p.96-99; B46 p.176, 183; B52 p.208-210; B88 p.224-227
- Existing: none. engine/foundations/space.py:175 checks within-group gaps on generated tokens only.

### too-many-type-sizes
- Measures: distinct rounded computed font-size values on rendered text, and pairs that differ by 1px.
- Threshold: warn above about 8 distinct sizes, and on any two sizes within 1px.
- How: render.
- Fixture: fail is a page using every size from 13 to 20px. Near-miss pass is a page using 12, 14, 16, 20, 28 and 40px.
- False-positive risk: medium. Fluid clamp sizes give fractional values, so round them first.
- Sources: B22 p.218; B88 p.158, 167; B46 p.199-203
- Existing: none.

### too-many-font-families
- Measures: distinct primary font families actually rendered.
- Threshold: warn above 2, fail above 3.
- How: render.
- Fixture: fail is 4 families on one page. Near-miss pass is a display face, a text face and a mono face.
- False-positive risk: low.
- Sources: B46 p.199-203; B26 p.453; B64 p.171
- Existing: none.

### faux-styles
- Measures: synthesized bold or italic (font-synthesis allowed while the loaded face lacks the style), and scaleX on text.
- Threshold: any.
- How: render (document.fonts) plus static lint.
- Fixture: fail is italic text with only the roman file loaded. Near-miss pass loads the true italic.
- False-positive risk: medium.
- Sources: B88 p.48, 71, 72; B19 p.29; B10 p.19
- Existing: none.

### primary-actions-over-budget
- Measures: elements styled as the primary action, per section and per viewport.
- Threshold: more than 2 per section or viewport, or more than 1 inside a dialog.
- How: render.
- Fixture: fail is a hero with three filled brand buttons. Near-miss pass is one filled button and one outline button.
- False-positive risk: medium. Pricing cards carry one primary each.
- Sources: B47 p.60-61; B22 p.260; B24 p.190-191; B54 p.122-124
- Existing: cta-buttons-clustered-in-hero is a hero-only regex proxy.

### selected-state-color-only
- Measures: the selected item in a tablist, segmented control or toggle group, compared with its siblings for any non-color change (weight, underline, border, icon, fill shape).
- Threshold: fail when only the color changes.
- How: render.
- Fixture: fail is tabs whose active tab only changes text color. Near-miss pass adds a 2px underline.
- False-positive risk: medium.
- Sources: B91 p.204; B86 p.242-243; B77 p.92
- Existing: none.

### destructive-styled-as-primary
- Measures: delete, remove and similar actions carrying the filled primary or danger style outside a confirmation, or styled the same as a frequent neighboring action.
- Threshold: any.
- How: render.
- Fixture: fail is a toolbar of Download, Delete and Rename as identical buttons. Near-miss pass is Delete as a tertiary text button with a red Confirm inside the dialog.
- False-positive risk: medium.
- Sources: B47 p.62; B26 p.35, 213, 294-295; B44 p.98-99
- Existing: none.

### accordion-without-expanded-state
- Measures: a control that toggles a sibling panel without aria-expanded. Native details and summary are exempt.
- Threshold: any.
- How: static lint, confirmed by interaction.
- Fixture: fail is a div that toggles an FAQ answer on click. Near-miss pass is a button with aria-expanded and aria-controls.
- False-positive risk: medium.
- Sources: B91 p.242; B18 p.92, 197-198
- Existing: none.

### pagination-current-unmarked
- Measures: a pagination nav whose current page lacks aria-current="page" or is still a live link.
- Threshold: any.
- How: static lint.
- Fixture: fail is the current page as a link with class active. Near-miss pass is a span with aria-current="page".
- False-positive risk: low.
- Sources: B91 p.248, 250; B86 p.366
- Existing: none.

### select-change-triggers-action
- Measures: a select whose change handler navigates or submits.
- Threshold: any.
- How: static lint.
- Fixture: fail is a select that sets location on change. Near-miss pass is an in-place sort that keeps focus.
- False-positive risk: medium.
- Sources: B18 p.96; B86 p.378
- Existing: none.

### tabs-overflow
- Measures: a tablist with 10 or more tabs, or one that wraps to a second row.
- Threshold: more than 9 tabs, or any wrap.
- How: render at each viewport.
- Fixture: fail is 12 tabs wrapping at 768px. Near-miss pass is 6 tabs in one scrolling row.
- False-positive risk: low.
- Sources: B86 p.242-243; B26 p.638-639
- Existing: none.

### menu-too-deep
- Measures: depth of nested menus or submenus.
- Threshold: more than 2 cascade levels.
- How: static lint.
- Fixture: fail is three nested flyouts. Near-miss pass is one flyout level.
- False-positive risk: low.
- Sources: B46 p.405-408
- Existing: none.

### single-and-double-tap-on-one-element
- Measures: one element with both a click and a double-click handler.
- Threshold: any.
- How: static lint.
- Fixture: fail is a card that opens on click and likes on double-click. Near-miss pass uses a separate like button.
- False-positive risk: low.
- Sources: B52 p.136
- Existing: none.

### mixed-corner-families
- Measures: square (0 to 2px) and rounded (6px or more) radii on the same control type.
- Threshold: two corner families on one control type.
- How: render or a static CSS scan.
- Fixture: fail is square inputs next to 12px-radius buttons in one form. Near-miss pass is 8px buttons and inputs with round avatars.
- False-positive risk: medium. Pills and avatars are deliberate.
- Sources: B47 p.20-25
- Existing: pill-rounded-full-everywhere and border-radius-2xl-default flag overuse, not mixing.

### off-scale-values
- Measures: the share of spacing, font-size and radius literals that fall off the system scale.
- Threshold: more than about 10 percent off the scale.
- How: static scan against tokens.
- Fixture: fail is padding of 7, 13 and 19px. Near-miss pass is 8, 12 and 16px on a 4px base.
- False-positive risk: medium. Optical tweaks and 1px borders.
- Sources: B47 p.29-32, 71-73; B22 p.15-16, 193; B26 p.444-445
- Existing: partial, through class-multiple-utility-than-token and inline-style-attribute.

### icon-only-primary-control
- Measures: primary navigation items or primary actions whose visible content is only an icon.
- Threshold: any outside a small set of learnable icons (close, search, menu).
- How: render.
- Fixture: fail is a bottom nav of five unlabeled icons. Near-miss pass is a toolbar of familiar icons with labeled primary actions.
- False-positive risk: medium.
- Sources: B93 p.174-175; B28 p.274-276; B08 p.327-332
- Existing: inline-svg-no-aria checks the accessible name only.

### icon-stroke-mixed
- Measures: distinct stroke-width values across inline svg icons of the same size.
- Threshold: more than one.
- How: static scan.
- Fixture: fail is icons at stroke 1.5 and 2 side by side. Near-miss pass is all icons at 2.
- False-positive risk: low.
- Sources: B86 p.279, 378
- Existing: none. The rule is a checklist item at references/foundations/color.md:275, 326.

### modal-on-entry-blocking
- Measures: a dialog or overlay covering the page within 3 seconds of load.
- Threshold: fail with no close control. Flag any on-load overlay for review.
- How: render.
- Fixture: fail is an email gate on load with no close. Near-miss pass is a non-blocking cookie bar.
- False-positive risk: low.
- Sources: B78 p.16; B07 p.214-216
- Existing: overlaps the render rule first-screen-covered. Confirm its scope.

## Priority 4: motion, touch and feedback timing

### ui-transition-over-one-second
- Measures: non-infinite, non-ambient transition or animation durations on UI elements.
- Threshold: fail above 1000ms. Advisory from 600 to 1000ms on interactive elements.
- How: static lint.
- Fixture: fail is a modal transition of 1200ms. Near-miss pass is a single 900ms hero entrance.
- False-positive risk: low. Exclude loops, marquees and progress.
- Sources: B26 p.297; B42 p.73-76; B14 p.119
- Existing: transition-duration-500ms-or-longer and animation-duration-too-long cover part of this. Extend them to entrances, and drop the 1500ms ceiling at references/foundations/motion.md:290.

### linear-easing-on-spatial-transition
- Measures: linear timing on transitions that move or scale elements.
- Threshold: linear combined with transform or position changes. Progress bars, spinners, marquees and shimmer are excluded.
- How: static lint.
- Fixture: fail is a drawer sliding with linear timing over 300ms. Near-miss pass is a progress fill with a linear width transition.
- False-positive risk: medium.
- Sources: B42 p.39-41, 54-55; B85 p.139
- Existing: none. The guide is at references/foundations/motion.md:214, 275.

### touch-target-below-platform-size
- Measures: hit areas of interactive elements at phone width.
- Threshold: advisory under 44 by 44 CSS px at 390px (WCAG 2.5.5 AAA and platform guidance). The existing 24px hard fail stays.
- How: render at 390 by 844. Exclude inline links inside sentences.
- Fixture: fail is a 32px icon button in a toolbar. Near-miss pass is a 24px icon padded to a 44px box.
- False-positive risk: medium.
- Sources: B02 p.255-256; B86 p.297, 326; B52 p.132-133; B91 p.202; B80 p.32
- Existing: target-too-small (24px, WCAG 2.5.8). This adds a new tier only.

### too-many-touch-controls-in-a-row
- Measures: distinct targets sharing one horizontal band at phone width.
- Threshold: more than 5 targets whose centers align within 8px in one 390px row.
- How: render.
- Fixture: fail is a bottom bar of 6 icon buttons. Near-miss pass is 5 labeled tabs.
- False-positive risk: medium.
- Sources: B04 p.287-288, 294; B26 p.530, 533
- Existing: none.

### loading-indicator-flicker
- Measures: how long a spinner, progress bar or aria-busy region stays visible after a fast response.
- Threshold: fail when visible for under 200ms.
- How: interaction with a mocked fast response.
- Fixture: fail is a spinner shown at once and removed at 80ms. Near-miss pass gates the spinner behind a 200ms delay.
- False-positive risk: medium.
- Sources: B52 p.264; B86 p.409-410
- Existing: none.

### progress-bar-goes-backward
- Measures: progress values over one operation.
- Threshold: any decrease, or reaching 100 before the work ends.
- How: interaction.
- Fixture: fail is aria-valuenow going from 60 to 40. Near-miss pass is 10, 30, 30, 70, 100 and then removed.
- False-positive risk: low.
- Sources: B52 p.262-263; B82 p.116-117
- Existing: none.

### long-operation-without-cancel
- Measures: progress visible past 2 seconds with no cancel or stop control nearby.
- Threshold: any.
- How: interaction with a slow mocked response.
- Fixture: fail is a 5-second upload with no Cancel. Near-miss pass is the same upload with Cancel.
- False-positive risk: medium. Page loads cannot always be cancelled.
- Sources: B86 p.409, 415; B26 p.295-296, 452; B24 p.312-314
- Existing: none.

### mobile-content-starts-too-low
- Measures: the top of the first content block inside main at phone width.
- Threshold: advisory when stacked chrome pushes content below about 25 percent of an 844px viewport.
- How: render at 390 by 844, scoped to app and results pages.
- Fixture: fail is a logo bar, promo strip, tabs and sticky search stacking 320px. Near-miss pass is a 64px header with content at 96px.
- False-positive risk: high. Landing heroes do this on purpose.
- Sources: B86 p.299, 307; B04 p.299-300
- Existing: first-screen-covered covers overlays only.

### alignment-points-count
- Measures: distinct left edges of visible blocks in the first screen.
- Threshold: advisory above about 6 at desktop (calibrate on reference pages).
- How: render.
- Fixture: fail is a form with labels and fields at 9 x offsets. Near-miss pass is the same form on 2 columns.
- False-positive risk: high. Advisory only.
- Sources: B46 p.178-182; B26 p.444-447
- Existing: none.

### long-table-unchunked
- Measures: tables of more than 7 rows read across, with no zebra striping, row grouping or row dividers.
- Threshold: advisory.
- How: render.
- Fixture: fail is 30 rows with no stripes, rules or group gaps. Near-miss pass is the same table with hairline dividers or zebra rows.
- False-positive risk: medium.
- Sources: B46 p.182-183, 245-246; B23 p.576, 583
- Existing: none.

### print-stylesheet-missing
- Measures: a content page (article, docs, receipt) with no @media print rules while nav or sticky chrome is present.
- Threshold: advisory.
- How: static lint.
- Fixture: fail is an article page with a sticky header and no print rules. Near-miss pass hides the nav under @media print.
- False-positive risk: medium. Most app screens are never printed.
- Sources: B59 p.16
- Existing: none.

## Already covered (no new rule needed)

| Lesson | Existing rule | Sources |
|---|---|---|
| Never block pinch zoom | viewport-no-zoom (data/anti-patterns.json) | B77 p.161; B91 p.115, 197, 202; B80 p.26, 32 |
| No justified web body text | text-align-justify-web | B46 p.607-608; B88 p.118-119 |
| No gray or white at reduced opacity for text | text-ink-at-low-alpha | B47 p.42-44 |
| Text contrast floors | text-low-contrast, accent-text-low-contrast (render) | B91 p.59, 243; B18 p.140 |
| Web target floor 24px | target-too-small (render) | B91 p.202 |
| Images reserve their space | img-no-dimensions | B52 p.222, 282 |
| Animate transform and opacity only | animating-layout-properties | B42 p.77-79 |
| No autoplay video with sound | autoplay-without-muted (extend to the audio element) | B91 p.74; B18 p.185, 187 |
| Chromatic share follows energy | color-over-budget (render) | B86 p.283; B76 p.14 |


<!-- cluster C: interaction, content, access and AI -->

# Cluster C checks: interaction, content, access and AI

Lessons from cluster C that can become measurable automated checks. Methods: static (lint of HTML, CSS, JSX, locale files), render (headless browser, computed styles and geometry), interaction (scripted input in a browser), artifact (design artifacts: flow files, site maps, goal-by-route matrices, intent lists, agent specs, research plans).

"Existing" names the matching rule in data/anti-patterns.json, or a render rule in commands/ux-lint.md, or "none". Impact runs 1 (minor) to 5 (prevents serious harm or a broken core flow). 71 checks.

## Top 10 by impact

| rank | id | method | impact | existing |
|---|---|---|---|---|
| 1 | flow-failure-paths | artifact | 5 | none |
| 2 | goal-multiple-routes | artifact, crawl | 5 | none |
| 3 | error-not-linked-to-field | static, render | 5 | none |
| 4 | agent-consequential-action-gate | artifact, static | 5 | none |
| 5 | rtl-html-dir | static | 5 | lang-attribute-missing (lang only) |
| 6 | rtl-physical-properties | static | 5 | none |
| 7 | permission-request-on-load | static, render | 5 | none |
| 8 | generic-error-copy | static | 4 | none (prose only, copy.md:91) |
| 9 | nav-primary-hidden-mobile | render | 4 | nav-equal-hamburger-desktop (desktop only) |
| 10 | submit-not-guarded | interaction | 4 | none |

Next in line: ai-run-stop-control, i18n-concatenated-strings, i18n-expansion-overflow, bidi-isolation, drip-pricing, flow-late-constraint.

## Flows and structure (artifact checks)

### flow-failure-paths (impact 5)
- Measures: whether every step in a flow artifact that takes input, calls the network, pays, uploads or deletes has a failure branch, and whether every error node leads back to a recoverable state.
- Threshold: 100 percent of such nodes carry at least one of error, empty, timeout, cancel, offline; every terminal error node has an edge back (retry, edit, alternative); every destructive node has an undo or confirm node.
- How measured: artifact check on flow JSON or Mermaid using node type tags.
- Fixture: fail, a sign-in flow with only the success path, or checkout with pay then success. Near-miss pass, sign-in with wrong password, unknown account, forgot password and no account branches, each returning to the form with the email kept.
- False-positive risk: medium; depends on node tagging. Purely informational nodes are exempt.
- Sources: B27 p.144-147; B38 p.24, 27-28; B29 p.60; B63 p.46-47; B67 p.24-27; B20 p.812-813; B79 p.204-207.
- Existing: none.

### goal-multiple-routes (impact 5)
- Measures: whether each top task or key page in a goal-by-route matrix (or a crawl of a built site) is reachable by independent routes.
- Threshold: at least 2 of global navigation, site search, site map or index, contextual link. Mirrors WCAG 2.4.5 Multiple Ways.
- How measured: artifact check on the goal-by-route matrix; link-graph crawl for built sites.
- Fixture: fail, a pricing page reachable only from one footer link. Near-miss pass, reachable from the top navigation and site search, nothing else.
- False-positive risk: low; steps inside a process (checkout step 3) are exempt under WCAG and must be excluded.
- Sources: B93 p.215-218; B18 p.113, 115; B91 p.264; B40 p.30.
- Existing: none.

### flow-late-constraint (impact 4)
- Measures: eligibility checks, permission walls or price-changing options that appear only after the user has entered data.
- Threshold: no blocking check or price-changing option placed after a data-entry node when it could precede it.
- How measured: artifact check on flows (node order).
- Fixture: fail, a rental flow collecting personal details before showing an add-on that changes the price. Near-miss pass, add-ons and the total shown first, then details.
- False-positive risk: medium; some checks genuinely need the data first (credit decisions).
- Sources: B20 p.812-813; B94 p.109; B23 p.517, 525.
- Existing: none.

### exit-friction-asymmetry (impact 4)
- Measures: steps to cancel, unsubscribe or delete an account versus steps to sign up.
- Threshold: exit path no longer than the entry path; no shaming copy on it.
- How measured: artifact check (count nodes on both paths) or interaction.
- Fixture: fail, sign-up in 2 steps and cancellation in 5 with a retention loop. Near-miss pass, cancellation in 2 steps with one optional offer screen that keeps a plain cancel button.
- False-positive risk: low on artifacts.
- Sources: B02 p.51-53; B07 p.203-206; B56 p.70.
- Existing: confirmshaming covers the wording only.

### sitemap-depth (impact 3)
- Measures: depth and grouping in a site map artifact.
- Threshold: primary content within 3 levels; any level with more than about 8 children is split into labeled groups.
- How measured: artifact check on the site map tree.
- Fixture: fail, product detail at level 5. Near-miss pass, level 3 with a 20-item level split into 4 labeled groups.
- False-positive risk: medium; searchable documentation and archives may run deeper.
- Sources: B93 p.141-143; B46 p.167, 347-349; B26 p.604-605.
- Existing: none.

### agent-plan-review-gate (impact 4)
- Measures: whether agent tasks tagged costly, irreversible or long-running show an editable plan before they run.
- Threshold: 100 percent of such tasks; plans longer than about 15 steps grouped into phases.
- How measured: artifact check on agent or flow specs.
- Fixture: fail, a migrate_database task that runs straight after the request. Near-miss pass, a quick reversible rename with no review next to a migration that shows a three-phase plan.
- False-positive risk: low.
- Sources: B82 p.176, 184, 192-193; B16 p.252-253.
- Existing: none.

### conversation-core-intents (impact 4)
- Measures: whether a bot's intent inventory covers repair and navigation.
- Threshold: intents present for help or capabilities, repeat, clarify, go back or start over, cancel, talk to a person, goodbye; the handoff intent routes to a node that passes a summary to the person.
- How measured: artifact check on the intent list or training file.
- Fixture: fail, only domain intents (order_status, refund). Near-miss pass, the same plus all seven, with handoff passing context.
- False-positive risk: low.
- Sources: B60 p.100-102; B63 p.140; B41 p.75-77; B02 p.259-260; B51 p.165-166.
- Existing: none.

### voice-prompt-structure (impact 3)
- Measures: spoken prompt scripts.
- Threshold: at most 3 options (4 for very short familiar items); nothing after the final question or cue; under about 20 s, roughly 50 words at 150 words per minute.
- How measured: artifact check on prompt scripts or SSML (count list items, find trailing text after the cue, count words).
- Fixture: fail, five sizes listed then a help hint after the question. Near-miss pass, three sizes ending on the question.
- False-positive risk: medium.
- Sources: B63 p.96, 102, 114-117; B41 p.60, 131-132; B73 p.40-41; B02 p.148.
- Existing: none.

### card-sort-plan (impact 2)
- Measures: card sort and tree test plans.
- Threshold: 30 to 60 cards; at least 6 participants (up to about 15); open sort, then closed sort, then tree test.
- How measured: artifact check on the research plan.
- Fixture: fail, 120 cards with 3 participants. Near-miss pass, 45 cards, 12 participants, tree test planned.
- False-positive risk: low; small internal tools may skip it.
- Sources: B35 p.290-292; B03 p.219-220; B58 p.173; B06 p.120.
- Existing: none.

## Forms and errors

### error-not-linked-to-field (impact 5)
- Measures: invalid fields whose message is not tied to the input in code.
- Threshold: any input with aria-invalid true (or an error class) lacking aria-describedby or aria-errormessage that resolves to non-empty text placed after the input in DOM order.
- How measured: static lint of HTML or JSX; render to resolve ids set at runtime.
- Fixture: fail, red border on the input and the error paragraph at the top of the form, no link. Near-miss pass, aria-describedby pointing to a span right after the input.
- False-positive risk: medium in static mode, low in render mode.
- Sources: B18 p.92-93; B52 p.176-177; B27 p.148-150; B86 p.525-526.
- Existing: none (accessibility.md describes it in prose).

### generic-error-copy (impact 4)
- Measures: error strings that name neither cause nor fix.
- Threshold: any rendered string, locale entry or toast call matching something went wrong, an error occurred, invalid input, invalid value, illegal, fatal, oops, a lone Error, or a bare code (Error 404) with no sentence after it.
- How measured: static lint of markup, JSX and locale JSON.
- Fixture: fail, an error toast reading only that something went wrong. Near-miss pass, could not save, check your connection and try again.
- False-positive risk: medium; scope to rendered strings, not logs or docs about errors.
- Sources: B51 p.267-268; B82 p.128-129; B58 p.306-307; B46 p.594-599; B20 p.817, 828-831.
- Existing: none (copy.md:91 lists the strings in prose).

### submit-not-guarded (impact 4)
- Measures: whether a fast double click on submit sends two requests.
- Threshold: more than one identical POST within 1 s of two clicks, or a button that stays enabled with no busy state while the request runs.
- How measured: interaction with network interception.
- Fixture: fail, a handler that posts with no pending state. Near-miss pass, button disabled and relabeled while the request is in flight.
- False-positive risk: low in interaction mode; high if attempted statically.
- Sources: B27 p.121-122; B44 p.132-133; B82 p.125.
- Existing: none (interaction.md:135-138 describes the pattern).

### required-indicator-mismatch (impact 3)
- Measures: visual required markers without required state in code, the reverse, or an asterisk never explained on the page.
- Threshold: a label with an asterisk or the word required whose input lacks required or aria-required; or a form using asterisks with no explanatory text.
- How measured: static lint.
- Fixture: fail, label with an asterisk, input without required, no legend. Near-miss pass, same label, input required, a line explaining the asterisk.
- False-positive risk: medium; the explanation may sit in a shared layout.
- Sources: B86 p.494-495; B23 p.564; B59 p.13; B91 p.240. Standard: WCAG 3.3.2, 1.3.1.
- Existing: none.

### duplicate-confirm-field (impact 3)
- Measures: confirm-email and confirm-password fields.
- Threshold: any input whose name, id or label pairs confirm, repeat or retype with email or password.
- How measured: static lint.
- Fixture: fail, email plus confirm_email. Near-miss pass, one password field with a show-password toggle; current-password plus new-password in a change flow.
- False-positive risk: low; exempt current or old password.
- Sources: B52 p.157; B24 p.77, 83-85. Standard: WCAG 3.3.7.
- Existing: none.

### autocomplete-off-personal-field (impact 3)
- Measures: autofill disabled on personal or credential fields.
- Threshold: autocomplete off on fields named email, name, phone, address, username or current password.
- How measured: static lint.
- Fixture: fail, email input with autocomplete off. Near-miss pass, a one-time code input with autocomplete one-time-code.
- False-positive risk: low.
- Sources: B07 p.45-46; B52 p.171-172. Standard: WCAG 1.3.5, 3.3.8.
- Existing: input-purpose-missing flags a missing value; extend it to flag off.

### input-type-mismatch (impact 3)
- Measures: semantic input type versus field purpose.
- Threshold: a field named or labeled email, phone, url or numeric code using type text without inputmode.
- How measured: static lint.
- Fixture: fail, email field with type text. Near-miss pass, phone field with type tel.
- False-positive risk: low; accept inputmode for formatted IDs.
- Sources: B07 p.45-46; B52 p.168.
- Existing: none (components.md mentions it in prose).

### button-label-generic-verb (impact 3)
- Measures: buttons whose whole label is Submit, OK, Yes, No, Send, Done or Go.
- Threshold: exact match on trimmed text; exempt OK in an alert with a single action.
- How measured: static lint.
- Fixture: fail, a submit button reading Submit. Near-miss pass, Submit application.
- False-positive risk: low to medium.
- Sources: B20 p.754-755, 757; B23 p.564; B07 p.45-46, 211; B54 p.153; B33 p.107-108.
- Existing: partial; cta-text-tap-continue-go and generic-cta-text miss bare Submit and OK. Extend cta-text-tap-continue-go.

### confirm-dialog-vague (impact 3)
- Measures: confirmation dialogs that do not name the action and the object.
- Threshold: a dialog or alertdialog whose text is only a are-you-sure question, or whose buttons are only OK and Cancel or Yes and No; any window.confirm call.
- How measured: static lint.
- Fixture: fail, window.confirm asking whether the user is sure. Near-miss pass, dialog titled Delete 12 invoices with buttons Delete invoices and Keep.
- False-positive risk: low.
- Sources: B79 p.205-207; B26 p.641-642; B07 p.211.
- Existing: none (copy.md in prose).

### error-toast-auto-dismiss (impact 3)
- Measures: error toasts or toasts carrying Undo or Retry that close on a timer.
- Threshold: a toast call or component with an error or destructive variant, or an action, that sets a finite duration.
- How measured: static lint of common toast APIs (duration, autoClose, timeout).
- Fixture: fail, an error toast with a 3000 ms duration. Near-miss pass, a success toast with no action and a 4000 ms duration.
- False-positive risk: medium; libraries that pause on hover or focus.
- Sources: B26 p.291, 666, 680; B20 p.780, 816. Standard: WCAG 2.2.1.
- Existing: none. Note: the engine guide itself advises 3 to 5 s auto-dismiss (see gaps.md).

### time-limit-without-warning (impact 3)
- Measures: session or step timeouts with no warning and no extension.
- Threshold: a timer that ends a session or clears input with under 20 s warning and no extend control.
- How measured: artifact (flow states include a timeout warning) plus interaction with fake timers.
- Fixture: fail, checkout redirects after 8 idle minutes with no dialog. Near-miss pass, a dialog at 2 minutes left with an extend button that keeps the input.
- False-positive risk: medium.
- Sources: B18 p.101, 251; B91 p.72, 77, 99; B32 p.173. Standard: WCAG 2.2.1.
- Existing: none.

### radio-group-without-fieldset (impact 3)
- Measures: radios sharing a name with no grouping.
- Threshold: two or more radios with one name not inside a fieldset with legend or a named radiogroup.
- How measured: static lint.
- Fixture: fail, three plan radios in plain divs. Near-miss pass, the same inside a fieldset with legend Plan.
- False-positive risk: low.
- Sources: B80 p.16-17; B91 p.242.
- Existing: fieldset-without-legend covers a fieldset missing its legend only.

### input-visible-boundary (impact 3)
- Measures: text inputs with no visible edge in flat styles.
- Threshold: border, underline or fill with at least 3:1 contrast against the adjacent background (WCAG 1.4.11).
- How measured: render, computed border and background contrast.
- Fixture: fail, a borderless input on white with only a placeholder. Near-miss pass, a 1 px border at 3:1.
- False-positive risk: medium; inline-edit fields that show a border on focus by design.
- Sources: B77 p.162-165; B24 p.316-317.
- Existing: none.

### disabled-submit-without-reason (impact 2)
- Measures: a disabled primary button with no visible explanation.
- Threshold: no aria-describedby, adjacent hint or tooltip naming what enables it.
- How measured: static plus render.
- Fixture: fail, a disabled Continue with no hint. Near-miss pass, a hint under it naming the missing field.
- False-positive risk: medium.
- Sources: B20 p.689-690, 782-783.
- Existing: menu-row-disabled-without-reason covers menu rows only; extend.

### form-without-form-element (impact 2)
- Measures: inputs and a submit control outside a form element, so Enter does nothing.
- Threshold: a text input and an onClick submit button with no form ancestor.
- How measured: static lint.
- Fixture: fail, a div with an input and a save button. Near-miss pass, a form with onSubmit and a type submit button.
- False-positive risk: medium; single filters that apply on change.
- Sources: B80 p.52-53; B52 p.153-154.
- Existing: none (button-no-type is related).

### form-reset-button (impact 2)
- Measures: reset or clear-all buttons that wipe a form.
- Threshold: any input or button of type reset, or a button labeled reset or clear form.
- How measured: static lint.
- Fixture: fail, a reset button beside submit. Near-miss pass, a clear control on one search field.
- False-positive risk: low.
- Sources: B23 p.564; B52 p.157-158.
- Existing: none.

## Accessibility

### label-not-in-name (impact 3)
- Measures: an accessible name that does not contain the visible label (WCAG 2.5.3).
- Threshold: visible text not contained, case-insensitive, in the element's aria-label.
- How measured: static lint.
- Fixture: fail, visible Done with an aria-label of Close dialog. Near-miss pass, aria-label Done, close dialog.
- False-positive risk: low.
- Sources: B91 p.96.
- Existing: none.

### live-region-mounted-late (impact 3)
- Measures: live regions created at the moment the message appears.
- Threshold: role status or aria-live inside a conditional that is false on first render (lower severity for role alert, which most readers announce on insertion).
- How measured: static lint of JSX conditionals, confirmed by render.
- Fixture: fail, a status region rendered only when an error exists. Near-miss pass, a region always present whose text fills in.
- False-positive risk: medium.
- Sources: B80 p.98-100; B91 p.68; B07 p.127.
- Existing: aria-busy-without-aria-live and aria-live-polite-on-error are related, not the same.

### drag-without-pointer-alternative (impact 3)
- Measures: drag interactions with no single-pointer or keyboard alternative (WCAG 2.5.7).
- Threshold: draggable elements or a drag library in a component with no move buttons, menu or input that does the same.
- How measured: static heuristic plus interaction (try to reorder by clicks only).
- Fixture: fail, a sortable list with handles only. Near-miss pass, the same list with move up and move down buttons.
- False-positive risk: medium.
- Sources: B18 p.94-97; B46 p.667-669.
- Existing: none.

### skip-link-first-focusable (impact 4)
- Measures: the first Tab stop is a working skip link that shows on focus (WCAG 2.4.1).
- Threshold: first focusable element links to an existing id and has a visible box when focused.
- How measured: interaction, one Tab press, read the active element and its rect.
- Fixture: fail, skip link to a missing id. Near-miss pass, skip link to an existing content id that appears on focus.
- False-positive risk: low; apps with no repeated header blocks are exempt.
- Sources: B91 p.82, 117, 244; B18 p.113.
- Existing: screen-reader-only-without-class checks the hiding class only.

### in-text-link-distinguishable (impact 4)
- Measures: links inside prose that rely on color alone (WCAG 1.4.1).
- Threshold: underlined, or at least 3:1 contrast with surrounding text plus underline or outline on hover and focus.
- How measured: render (computed decoration and contrast against sibling text) plus interaction for hover and focus.
- Fixture: fail, a link at 1.6:1 against body text with no underline. Near-miss pass, the same link underlined.
- False-positive risk: low; navigation and button-styled links excluded.
- Sources: B46 p.378, 387-389; B77 p.72; B47 p.126-127.
- Existing: none.

### duplicate-adjacent-links (impact 2)
- Measures: two adjacent links to the same URL (image link plus title link).
- Threshold: same href twice in one card or list item.
- How measured: static lint.
- Fixture: fail, a card with an image link and a heading link to one product. Near-miss pass, one wrapping link, or the image link removed from the tab order and hidden from assistive tech.
- False-positive risk: low.
- Sources: B91 p.191, 202, 204; B80 p.20-21, 32.
- Existing: none.

### flashing-content (impact 2)
- Measures: luminance flashes (WCAG 2.3.1).
- Threshold: more than 3 general or red flashes in any 1 s over an area above the small-area limit.
- How measured: render and sample frames.
- Fixture: fail, a large panel toggling black and white at 5 Hz. Near-miss pass, a 2 Hz pulse on a small dot.
- False-positive risk: low with the area threshold.
- Sources: B42 p.237, 239; B26 p.402.
- Existing: blink-tag and marquee-tag catch old tags only.

### new-window-internal-link (impact 2)
- Measures: same-origin links forced into a new window.
- Threshold: target blank on an internal link with no stated reason in the link text.
- How measured: static lint.
- Fixture: fail, an internal pricing link opening a new tab. Near-miss pass, an external PDF link whose text says it opens in a new tab.
- False-positive risk: medium; in-app help panels where losing state is worse.
- Sources: B18 p.99.
- Existing: target-blank-no-noopener covers security only.

### reading-level (impact 3)
- Measures: grade level of body copy for a general audience.
- Threshold: warn above grade 9 (reading age about 14); formulas carry about 1.5 grades of error, so warn, do not fail; offer a summary per WCAG 3.1.5.
- How measured: static text analysis of prose blocks.
- Fixture: fail, a help article at grade 14. Near-miss pass, grade 8 with a key-points summary.
- False-positive risk: medium; technical and legal audiences need a per-audience setting.
- Sources: B46 p.120, 593-594; B23 p.269, 536; B18 p.160-164.
- Existing: none.

## Navigation, search and affordance

### nav-primary-hidden-mobile (impact 4)
- Measures: top-level destinations hidden behind a toggle at phone width.
- Threshold: at 375 px wide, if the site has 5 or fewer top-level destinations and none is visible without opening a menu, fail.
- How measured: render at phone width.
- Fixture: fail, 4 links inside a closed drawer behind an icon. Near-miss pass, 4 links in a bottom tab bar with secondary items behind a labeled Menu button.
- False-positive risk: medium; large content sites with 8 or more sections may use a menu, which the threshold avoids.
- Sources: B02 p.534-535; B07 p.198-201; B24 p.25, 37.
- Existing: nav-equal-hamburger-desktop covers desktop only.

### nav-current-location (impact 4)
- Measures: whether the active navigation item is marked for assistive tech and for the eye.
- Threshold: the link matching the current URL carries aria-current page and differs from its siblings in at least 2 computed properties (color, weight, background, border, underline).
- How measured: static for aria-current; render to compare computed styles.
- Fixture: fail, active link differs by color only and lacks aria-current. Near-miss pass, aria-current plus color and a bottom bar.
- False-positive risk: low; pages outside the navigation are skipped.
- Sources: B77 p.89; B18 p.112; B93 p.202.
- Existing: none.

### menu-ungrouped-count (impact 3)
- Measures: how many ungrouped choices a menu level shows. Replaces a fixed 7-item cap.
- Threshold: warn above 10 items with no group headings or separators; grouped levels pass up to about 24.
- How measured: render, count items per level.
- Fixture: fail, 14 flat links in one dropdown. Near-miss pass, 18 links in 3 labeled groups.
- False-positive risk: low; alphabetical indexes (countries, A to Z) exempt.
- Sources: B46 p.347-349, 352-353; B93 p.141-143.
- Existing: none.

### tab-bar-count (impact 2)
- Measures: items in a mobile bottom tab bar.
- Threshold: 5 or fewer, each with a text label.
- How measured: static or render.
- Fixture: fail, 6 icon-only tabs. Near-miss pass, 5 labeled tabs.
- False-positive risk: low.
- Sources: B24 p.38, 43-44.
- Existing: none in anti-patterns.json; guide only (components.md:620, layout.md:254).

### dead-end-screen (impact 3)
- Measures: screens with no route to a known place.
- Threshold: every page, modal and 404 offers at least one of a home-linked logo, navigation, a close control, a back link.
- How measured: render each route and modal; static for the 404 template.
- Fixture: fail, a 404 page with only an apology. Near-miss pass, a 404 with a home link and search.
- False-positive risk: low; kiosk and embedded contexts exempt.
- Sources: B86 p.171-173; B46 p.373-383.
- Existing: none.

### breadcrumb-structure (impact 2)
- Measures: breadcrumb semantics.
- Threshold: a labeled nav landmark; last crumb is not a link and carries aria-current page; crumbs follow the hierarchy, not history.
- How measured: static lint.
- Fixture: fail, last crumb links to itself. Near-miss pass, last crumb plain text with aria-current.
- False-positive risk: low.
- Sources: B77 p.91; B86 p.194-195; B04 p.227-231.
- Existing: none.

### zero-results-dead-end (impact 4)
- Measures: what a search with no matches offers.
- Threshold: results area echoes the query and offers at least one suggestion, correction, popular link or contact route; no sort or filter controls acting on the empty set.
- How measured: interaction, submit a nonsense query.
- Fixture: fail, a blank page saying no results with a sort dropdown. Near-miss pass, the query echoed with a spelling suggestion and popular categories.
- False-positive risk: low; sites without search skipped.
- Sources: B93 p.287-288; B04 p.38-40; B23 p.490, 498.
- Existing: none.

### search-query-echo-count (impact 3)
- Measures: whether a results page keeps the query and shows a count.
- Threshold: the input keeps the submitted value and a result count shows above the results.
- How measured: interaction.
- Fixture: fail, empty box above the results and no count. Near-miss pass, box holding the query and a count of 42 results.
- False-positive risk: low.
- Sources: B93 p.260, 282-284; B23 p.491, 495.
- Existing: none.

### active-filters-visible (impact 3)
- Measures: whether applied filters stay visible once the filter panel closes.
- Threshold: at 375 px, applied values show as removable chips or a summary, plus a clear-all control.
- How measured: interaction at phone width.
- Fixture: fail, the drawer closes and nothing shows a filter is on. Near-miss pass, a removable Size M chip and Clear all.
- False-positive risk: low.
- Sources: B07 p.105-106, 111; B24 p.161-176.
- Existing: none.

### filter-option-counts (impact 3)
- Measures: whether facet options prevent zero-result states.
- Threshold: each option shows a count; options with zero matches are disabled or hidden.
- How measured: interaction.
- Fixture: fail, selecting a color returns nothing with no warning. Near-miss pass, the color shown disabled with a zero count.
- False-positive risk: medium; counts may lag on huge catalogs.
- Sources: B07 p.111, 247-248; B23 p.491-497; B24 p.173-175.
- Existing: none.

### search-box-width (impact 2)
- Measures: rendered width of the global search input on desktop.
- Threshold: at least about 20 characters (20ch), measured expanded.
- How measured: render.
- Fixture: fail, a 120 px box. Near-miss pass, a 22ch box.
- False-positive risk: low.
- Sources: B46 p.281-282; B04 p.54.
- Existing: none.

### hover-only-affordance (impact 3)
- Measures: controls whose signifier exists only on hover.
- Threshold: interactive elements at opacity 0, hidden, or without a border until hover, with no equivalent on focus-visible or touch.
- How measured: static CSS lint plus render with touch emulation.
- Fixture: fail, card action buttons invisible until hover. Near-miss pass, buttons visible at rest with a stronger hover state.
- False-positive risk: medium.
- Sources: B79 p.33-35.
- Existing: hover-only-card-actions and focusable-at-opacity-zero cover part; generalize.

### false-affordance-pointer (impact 3)
- Measures: non-interactive elements styled as interactive.
- Threshold: pointer cursor, underline or link color on elements with no href, role, tabindex or handler (checking ancestors).
- How measured: static lint plus render.
- Fixture: fail, a blue underlined span with no link. Near-miss pass, the same span in body color, no underline.
- False-positive risk: medium; clicks delegated to a parent.
- Sources: B20 p.690-692; B14 p.48, 50; B11 p.112.
- Existing: none (onclick-on-non-button is the reverse case).

### permission-request-on-load (impact 5)
- Measures: browser permission prompts (notifications, location, camera, microphone, push) fired before any user gesture.
- Threshold: zero permission requests before the first user interaction.
- How measured: static lint for the permission APIs at module top level, in load handlers or in mount-only effects; render check recording permission calls before any input.
- Fixture: fail, a notification permission request in a mount-only effect. Near-miss pass, the same call in the click handler of a button that names the benefit.
- False-positive risk: medium; location-first apps opened from an explicit link may ask on load.
- Sources: B44 p.36-37; B07 p.67; B52 p.190-191; B51 p.181-184; B24 p.366.
- Existing: none.

### first-run-empty-state (impact 3)
- Measures: a view rendered with no data.
- Threshold: at least one primary action and one sentence naming the surface; no filters, sorts or tabs acting on zero items.
- How measured: render with an empty-data fixture.
- Fixture: fail, an empty table with sort controls and a no-data line. Near-miss pass, a sentence, a primary button to connect a first source, filters hidden.
- False-positive risk: low.
- Sources: B52 p.278; B47 p.234-236; B07 p.43.
- Existing: none (checklist in copy.md).

### onboarding-tour-length-and-skip (impact 3)
- Measures: first-run tours.
- Threshold: at most 7 steps; skip or close on every step; a replay entry outside the tour.
- How measured: static lint of tour library configs; render of step indicators.
- Fixture: fail, a 10-step tour with skip disabled. Near-miss pass, 5 steps, skip on each, Replay tour in the help menu.
- False-positive risk: low.
- Sources: B26 p.415-417; B24 p.267, 273-281; B07 p.32; B77 p.168-169.
- Existing: none.

### badge-count-cap (impact 2)
- Measures: notification badges showing large exact counts.
- Threshold: badge text at most two digits or capped with a plus (99+).
- How measured: render on badge-like elements.
- Fixture: fail, a bell badge reading 1284. Near-miss pass, 99+.
- False-positive risk: low.
- Sources: B52 p.243.
- Existing: none.

## Commerce and persuasion

### drip-pricing (impact 4)
- Measures: mandatory fees first appearing at the last checkout step.
- Threshold: the final total for the same item and quantity equals the first shown price plus only taxes or shipping shown earlier as estimates.
- How measured: interaction through checkout capturing prices at each step, or artifact check of fee nodes.
- Fixture: fail, 40 on the product page and cart, a 6 service fee added at payment. Near-miss pass, 46 including the fee from the product page on.
- False-positive risk: medium; address-dependent tax and shipping must be whitelisted.
- Sources: B02 p.61; B56 p.139; B23 p.517, 525.
- Existing: none (guidance in landing.md).

### prechecked-add-on (impact 4)
- Measures: pre-checked boxes for paid add-ons, donations, insurance, warranties or data sharing.
- Threshold: zero checked boxes whose label mentions add, insurance, protection, warranty, donate, round up, share data or partners in purchase or sign-up forms.
- How measured: static regex, same shape as consent-prechecked with wider keywords.
- Fixture: fail, a checked trip protection box with a price. Near-miss pass, the same unchecked, or a checked remember-this-device box.
- False-positive risk: low to medium.
- Sources: B02 p.51-53; B77 p.199-200; B23 p.521; B54 p.136-137.
- Existing: consent-prechecked covers marketing keywords only; extend or add a sibling.

## AI interfaces

### agent-consequential-action-gate (impact 5)
- Measures: every agent step that spends, sends, deletes, books or changes permissions is preceded by a confirmation naming action, target and consequence, and followed by undo or a stated irreversibility.
- Threshold: 100 percent of tagged steps; the confirm button label holds a verb and an object, never OK, Yes, Confirm or Continue alone.
- How measured: artifact check on flow or agent specs; static lint of dialog markup for bare labels.
- Fixture: fail, a send_email node with no preceding confirm, or a dialog with a bare OK. Near-miss pass, a confirm reading Send to 14 people and a 10 s undo node.
- False-positive risk: low on artifacts; medium on markup (a single-button informational alert may say OK).
- Sources: B16 p.276-278; B12 p.182-183; B66 p.22-23; B60 p.194-195.
- Existing: none (generic-cta-text covers other labels).

### ai-run-stop-control (impact 4)
- Measures: a Stop control (and Pause for agents) while an answer streams or an agent runs.
- Threshold: a visible, keyboard-reachable control named stop or pause within 500 ms of the run starting, present until completion.
- How measured: interaction against a mocked slow stream.
- Fixture: fail, send disabled during streaming and nothing else offered. Near-miss pass, send swaps to a square icon named Stop generating.
- False-positive risk: low.
- Sources: B16 p.257-258; B82 p.190-191; B12 p.330-337; B21 p.59-60.
- Existing: none (guidance at ai-interfaces.md:19).

### ai-content-label (impact 4)
- Measures: generated content and bot replies carry an AI label.
- Threshold: every element marked as AI output has a visible label or accessible description naming AI, generated, assistant or bot; component specs declare a provenance slot.
- How measured: render plus artifact check of component specs.
- Fixture: fail, a generated product description shown as plain copy. Near-miss pass, the same with a small AI-drafted tag and edit history.
- False-positive risk: medium; needs the codebase to mark AI output.
- Sources: B16 p.195-196, 224; B82 p.147-148; B65 p.74-77; B73 p.57-58.
- Existing: none.

### ai-confidence-percentage (impact 4)
- Measures: uncalibrated percentage confidence beside model output.
- Threshold: zero percentages within six words of confident, confidence, sure, certain or accuracy inside an AI output region unless marked calibrated.
- How measured: static regex plus render, scoped to AI regions.
- Fixture: fail, an answer card reading 93% confident. Near-miss pass, an answer saying the figures are likely and should be checked, or a weather widget with a rain chance outside any AI region.
- False-positive risk: medium.
- Sources: B51 p.150-155; B82 p.142; B61 p.251-252.
- Existing: none (guidance at ai-interfaces.md:33).

### ai-generic-prompt-placeholder (impact 3)
- Measures: prompt inputs that promise unlimited scope.
- Threshold: zero placeholders or opening messages like ask me anything, how can I help you, type anything.
- How measured: static regex on placeholders and the first assistant message.
- Fixture: fail, a placeholder inviting anything. Near-miss pass, a placeholder naming invoices with one example question.
- False-positive risk: low.
- Sources: B16 p.164-167; B41 p.15-16; B63 p.118-120; B33 p.81.
- Existing: none (guidance at ai-interfaces.md:12).

### ai-icon-only-entry (impact 3)
- Measures: AI entry points that are a sparkle or wand icon with no visible name.
- Threshold: zero buttons whose only child is a sparkle, wand or magic icon.
- How measured: static lint of icon components inside text-less buttons.
- Fixture: fail, a sparkles-only button labeled AI for screen readers. Near-miss pass, the same icon with visible text Summarize thread.
- False-positive risk: low to medium.
- Sources: B82 p.57; B51 p.181-184.
- Existing: none.

### ai-data-use-disclosure-near-input (impact 3)
- Measures: whether a prompt or upload input states storage and training use nearby.
- Threshold: text or a link about storage, history, training or privacy within the input container or 200 px of it.
- How measured: render.
- Fixture: fail, a bare chat box and send button. Near-miss pass, a muted line under the box giving retention and training use, with a link.
- False-positive risk: medium.
- Sources: B12 p.168-169; B16 p.193-194; B75 p.69-70.
- Existing: none (guidance at ai-interfaces.md:47).

### feedback-prompt-every-turn (impact 2)
- Measures: modal or input-blocking feedback requests after assistant turns.
- Threshold: feedback stays inline and optional; at most one modal request per session.
- How measured: interaction, send three prompts and count blocking requests.
- Fixture: fail, a rating modal after each answer. Near-miss pass, thumbs controls under each answer that never take focus.
- False-positive risk: low.
- Sources: B60 p.33, 162-163; B52 p.76.
- Existing: none.

## Internationalization and right-to-left

### rtl-html-dir (impact 5)
- Measures: document direction for right-to-left languages.
- Threshold: when the html lang is ar, he, fa, ur, ps, ckb or yi, the html element carries dir rtl (not only body or a wrapper).
- How measured: static lint of HTML and JSX.
- Fixture: fail, an Arabic page with no dir. Near-miss pass, dir rtl on html with an inner ltr code block.
- False-positive risk: low.
- Sources: B08 p.48, 52-53; B88 p.119, 176-177.
- Existing: lang-attribute-missing checks that lang exists only.

### rtl-physical-properties (impact 5)
- Measures: physical left and right CSS in a codebase that ships a right-to-left locale.
- Threshold: no margin, padding, border or inset using left or right, no float or text-align left or right, no Tailwind ml, mr, pl, pr, left, right, text-left or text-right without an rtl variant.
- How measured: static lint, enabled when an RTL locale is detected.
- Fixture: fail, a card with a left margin. Near-miss pass, the same with margin-inline-start.
- False-positive risk: medium; maps and media timelines are physical by design; allow an ignore comment.
- Sources: B49 p.261; B08 p.52-53.
- Existing: none (negative-margin-pull-left-right is a different rule).

### rtl-directional-icon-mirror (impact 4)
- Measures: directional icons under RTL.
- Threshold: chevrons, arrows, back, forward, send, reply, undo, redo and progress icons mirror; media play, clocks, checkmarks and logos do not.
- How measured: static lint plus render in dir rtl, with an allow-list by icon name.
- Fixture: fail, a back chevron pointing left in an Arabic header. Near-miss pass, the chevron pointing right while a play icon stays unmirrored.
- False-positive risk: medium; needs the allow-list.
- Sources: B49 p.261; B79 p.125-127.
- Existing: none.

### bidi-isolation (impact 4)
- Measures: numbers with punctuation, phone numbers, Latin names and URLs inside right-to-left text.
- Threshold: such runs are wrapped in bdi, dir ltr or unicode-bidi isolate.
- How measured: static regex on text nodes in RTL documents; render to spot misplaced punctuation.
- Fixture: fail, an Arabic sentence ending in an international phone number whose plus sign lands at the wrong end. Near-miss pass, the same number inside bdi.
- False-positive risk: medium; plain digits without punctuation render correctly and are skipped.
- Sources: B08 p.48, 52-53; B88 p.119.
- Existing: none.

### arabic-latin-only-emphasis (impact 3)
- Measures: Latin-only emphasis applied to Arabic text.
- Threshold: no italic, uppercase transform or positive letter-spacing on Arabic content.
- How measured: static lint plus render on lang ar or RTL Arabic blocks.
- Fixture: fail, an Arabic headline with 0.1em letter-spacing. Near-miss pass, the headline emphasized by weight and color.
- False-positive risk: low.
- Sources: B88 p.109, 176-178.
- Existing: none (all-caps-large is not language-aware).

### inline-lang-mismatch (impact 3)
- Measures: passages in another script with no lang of their own (WCAG 3.1.2).
- Threshold: runs of Arabic or Hebrew script inside an element whose resolved lang is a Latin-script language, and the reverse, without a lang attribute.
- How measured: static scan of text nodes.
- Fixture: fail, an Arabic tagline in an English page without lang. Near-miss pass, the tagline in a span with lang ar and dir rtl; a single proper noun is exempt.
- False-positive risk: low.
- Sources: B18 p.50.
- Existing: lang-attribute-missing is document level only.

### i18n-concatenated-strings (impact 4)
- Measures: UI sentences assembled from fragments.
- Threshold: no concatenation or template joining of two or more translation calls, or a variable spliced mid-sentence.
- How measured: static lint of JS, TS and JSX, limited to rendered children and accessible labels.
- Fixture: fail, two translated fragments joined around a count. Near-miss pass, one message key with a plural-aware count argument.
- False-positive risk: low to medium.
- Sources: B08 p.155, 166; B49 p.264, 345-346; B52 p.85-91.
- Existing: none.

### i18n-expansion-overflow (impact 4)
- Measures: whether text containers survive translation growth.
- Threshold: under a pseudo-locale that lengthens strings by the length table (100 percent at 10 characters or fewer, falling to about 30 percent for long text), no button, tab, nav item or label clips, ellipsizes or overflows.
- How measured: render with pseudo-localized strings, compare scrollWidth with clientWidth.
- Fixture: fail, a fixed-width 6-character button that clips when doubled. Near-miss pass, the same button with min-width and padding that grows.
- False-positive risk: low; intentional truncation with a tooltip in data tables is exempt.
- Sources: B46 p.657-662; B23 p.603-604; B49 p.74, 274, 275.
- Existing: fixed-height-text-block covers height only.

### locale-format-hardcoded (impact 3)
- Measures: hand-built date, number, currency or week-start formats.
- Threshold: no manual date assembly, literal currency symbols glued to numbers, locale-less toLocaleString, or calendars with a fixed first weekday.
- How measured: static lint of JS and TS.
- Fixture: fail, month, day and year joined with slashes on a receipt. Near-miss pass, Intl.DateTimeFormat with the user's locale and locale week data.
- False-positive risk: low; ISO strings in transport and logs are fine.
- Sources: B08 p.59-69; B58 p.424-425, 433-436; B61 p.51; B22 p.64-67.
- Existing: none.

### language-picker-flags (impact 3)
- Measures: language switchers using flags or English language names.
- Threshold: no flag icons inside language switch links; each language named in its own language.
- How measured: static lint of elements linking to hreflang alternates.
- Fixture: fail, a UK flag to switch to English. Near-miss pass, English and Arabic each written in their own script; a shipping-country picker with flags is exempt.
- False-positive risk: low.
- Sources: B08 p.21; B11 p.166-167; B46 p.657-662.
- Existing: none (icon-emoji-stamp is generic).
