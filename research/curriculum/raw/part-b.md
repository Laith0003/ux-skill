# Part B: User Research, Information Architecture and Interaction Design, Prototyping

Scope: hendurhance/ui-ux README.md lines 670 to 1135 (local clone), 158 links. Read only; nothing in the clone was run.

## How this was done

- Every link was extracted from the block (158, including 21 file-mirror links and 3 exact duplicate URLs) and probed for liveness.
- Articles and tool pages were read with WebFetch. YouTube links were checked through the oEmbed endpoint (title and channel) and are summarized from that metadata and the list description only; no video was watched.
- Books are summarized from publisher, Google Books, NN/g or Goodreads descriptions and tables of contents, plus well-known published content where marked. No book was read in full.
- Pages on Medium-hosted domains (uxplanet.org, uxdesign.cc, medium.com, blog.prototypr.io), toptal.com, indeed.com and the Harvard PDF return 403 to the fetcher. They are recorded as blocked and summarized from the list description; no workaround was used.
- Numbers were checked against primary sources fetched for this purpose: NN/g "Why you only need to test with 5 users", NN/g "How to rate the severity of usability problems", NN/g "How to conduct a heuristic evaluation", NN/g "Card sorting", NN/g "Tree testing", MeasuringU "SUS", lawsofux.com "Miller's law", and Maze's help-center scoring formula (via search result text).
- Coverage was set against PLAN-4.1-inventory.md (152 principles), references/, data/anti-patterns.json, engine/linter rule ids, the render `_RULES`/`RULES` in core.py, taste.py and interact.py, the complaint probe kinds in engine/complaints.py, and commands/ux-research.md, ux-audit.md, ux-discover.md.

## Counts

- Links in block: 158 (52 articles, 42 videos, 21 books plus 1 book chapter and 1 PDF question bank, 21 file-mirror links, 19 tool links, 1 course). Three URLs appear twice (rows 48/49, 20/80, 22/81).
- Read (page text fetched and read): 35.
- Summarized from description: 80 (40 videos from oEmbed metadata, 20 books from publisher or catalog descriptions, 20 pages blocked with HTTP 403).
- Tool noted: 18 (plus the Xtensio tool page, which was read and is counted under read).
- Dead: 4 (row 11 moved stub, row 12 host unreachable, rows 135 and 147 videos private or removed).
- Out of scope: 21 (unofficial file mirrors of paid books; not opened).
- Lessons: 86 written (2 are tool notes merged into other lessons, 1 sitemap note handled under IA8); 29 already COVERED, 3 already listed in PLAN-4.1-inventory.md, 11 new MISSING-CHECK, 43 new MISSING-GUIDE (IA3 and MI6 carry both a check and guidance).
- Number conflicts recorded: 8 (see Number checks and conflicts).

Status key: COVERED (file or rule named), MISSING-CHECK (lint rule, render measurement or complaints probe proposed, with a detection sketch), MISSING-GUIDE (target references/ or commands/ file named). "Already in inventory" means PLAN-4.1-inventory.md lists the gap; such lessons are not counted as new.

Source shorthand: numbers in brackets are ledger row numbers (Part 2). NNG-5 = nngroup.com/articles/why-you-only-need-to-test-with-5-users; NNG-SEV = nngroup.com/articles/how-to-rate-the-severity-of-usability-problems; NNG-HE = nngroup.com/articles/how-to-conduct-a-heuristic-evaluation; NNG-CS = nngroup.com/articles/card-sorting-definition; NNG-TT = nngroup.com/articles/tree-testing; MU-SUS = measuringu.com/sus.

---

# Part 1: Topic sections

## 1. Research planning and method choice

**R1. Start from the decision the study will change, then pick the method.** A study plan names the question, the design decision it informs, the participants, how data is evaluated and how it is shared.
Sources: [13] ixdf.org/literature/topics/user-research, [66] adamfard.com/blog/conduct-user-testing, [72] xd.adobe.com/ideas/process/user-testing.
Status: COVERED (commands/ux-research.md Input and step 1, "Design decision the research informs").

**R2. Place every method on two axes: what people say vs what they do, and why (qualitative) vs how many (quantitative). Mix them; weight behavior over stated intent.**
Sources: [13], [10] (description).
Status: COVERED for the behavior rule (commands/ux-research.md hard rule "Never ask 'would you use'"). MISSING-GUIDE (low): add a say/do column to the method table in commands/ux-research.md step 2 so a survey is never picked to answer a behavior question.

**R3. Pick methods by project stage: discover (field study, diary study, contextual inquiry), explore (card sort, journey map), test (usability test, accessibility evaluation), listen (analytics, surveys).**
Sources: [13].
Status: MISSING-GUIDE: commands/ux-research.md step 2 chooses by question type only; add the stage as a second key so `/ux-research` on a live product defaults to listen and test methods, and on a new idea to discover methods.

**R4. Analytics and session replays show what happened, never why; follow a surprising number with a moderated session before redesigning.**
Sources: [69] contentsquare.com/guides/usability-testing/methods, [13].
Status: COVERED (references/process/lean-ux-klein.md "Analytics and qualitative paired").

**R5. A research budget of zero still buys a discount study: about three days (day 1 plan, day 2 test five people, day 3 analyze and write fixes) and a few hundred dollars of incentives.**
Sources: [68] nngroup.com/articles/usability-testing-101.
Status: MISSING-GUIDE: commands/ux-research.md output block has a Timeline field with no default; make the 3-day discount plan the default when the user gives no budget, instead of asking first.

**R6. Pilot every study once before real participants: dry-run a paper prototype with teammates, pilot a card sort to check the card count and label clarity, pilot a survey for wording.**
Sources: [133] ixdf.org prototyping article, NNG-CS.
Status: MISSING-GUIDE: no file in ux-skill mentions a pilot. Add a "pilot one session" step to commands/ux-research.md step 3 and to references/process/lean-ux-klein.md (Usability testing on a tight budget).

## 2. Interviews and recruiting

**I1. Interview about the most recent real instance, then probe the pain and the workaround; never pitch, never ask about hypothetical use.**
Sources: [9] (description), [16], [13].
Status: COVERED (references/process/lean-ux-klein.md "Customer interview methodology"; commands/ux-research.md hard rules).

**I2. Recruit people who match the target behavior and do not know the product: exclude employees, their families and friends, and product professionals; ask sensitive screener questions in bands (income brackets), not exact values.**
Sources: [66], [68].
Status: COVERED (commands/ux-research.md "Screen out product professionals"; lean-ux-klein.md Recruitment, behavior screeners, Minimum data). Small gap: the screener rule does not name staff, family and friends; fold into the same hard rule.

**I3. When the audience has distinct groups, sample per group: 3 to 4 people per group for two groups, 3 per group for three or more groups.**
Sources: NNG-5 (primary), consistent with [66] segmentation advice.
Status: MISSING-GUIDE: commands/ux-research.md gives a flat n=5-8; lean-ux-klein.md warns against pooling segments but gives no per-group number. Add the per-group rule to the sample column.

**I4. Run every session from one verbatim script: same greeting, same task wording, same emphasis; read tasks aloud or hand over task cards, and have the participant read each task aloud.**
Sources: [66], [68].
Status: MISSING-GUIDE: commands/ux-research.md "Usability test plan" artifact lists tasks and success criteria but no facilitator script; require a word-for-word script section in the generated plan.

## 3. Usability testing

**T1. Five participants per round for one user group finds most common problems; spend a larger budget on more rounds of five, retesting each fix.**
Sources: [68], [66] (3 to 5, preferably 5), NNG-5 (formula N(1-(1-L)^n), L = 31%, five users find about 85%; "3 studies with 5 users each").
Status: COVERED (references/process/lean-ux-klein.md "Five users per round"; references/laws/krug.md; PLAN-4.1 H13).

**T2. Write tasks as goals inside a short scenario; never list the steps; never reuse words that appear in the interface labels (priming); define the correct answer and success criteria before the first session.**
Sources: [66] (bad example lists each click), [68] (priming), NNG-TT ("avoid using terms that give away the answers").
Status: COVERED for goal framing and success criteria (commands/ux-research.md usability test plan). MISSING-CHECK `task-primes-label`: a self-check `/ux-research` runs before delivering a test plan for a page it can snapshot. Detection: collect the visible text of links, buttons, tabs and headings from the DOM snapshot; lowercase; for each label of two or more words, or a single word of 6+ letters that is not a stopword, flag any task sentence that contains it verbatim; suggest a synonym rewrite.

**T3. Open with an easy warm-up task, then mix open exploration with goal-specific tasks; in unmoderated tests the warm-up also screens out careless participants.**
Sources: [66], NNG-TT.
Status: MISSING-GUIDE: commands/ux-research.md step 3 (usability test plan).

**T4. Measure task success, time on task and errors, plus one standard questionnaire. SUS: 10 items on a 5-point scale; odd items score response minus 1, even items 5 minus response; sum times 2.5 gives 0 to 100. The mean across 500 studies is 68; above 80.3 is the top 10% (A); below 51 is the bottom 15% (F). A SUS score is not a percentage or a percentile.**
Sources: [65] keepitusable.com, [72], MU-SUS (primary).
Status: MISSING-GUIDE: commands/ux-research.md names SUS but gives no scoring or benchmark; agents/research-synthesizer.md should score SUS this way and report it against 68 with a confidence interval.

**T5. Report quantitative results with confidence intervals; small-sample completion rates are wide, and "70% completed" from 10 people is a range, not a point.**
Sources: [5] (Sauro and Lewis TOC: "How precise are our estimates? Confidence intervals"), MU-SUS (compute a CI around small samples).
Status: COVERED (agents/research-synthesizer.md mentions confidence intervals).

**T6. Quantitative benchmarks need far more people than problem-finding: NN/g recommends 20 users for usability metrics; Sauro and Lewis size the sample from the margin of error you need.**
Sources: NNG-5 (20 for quantitative), [5] chapters 6 and 7.
Status: MISSING-GUIDE: commands/ux-research.md hard rule says "never recommend n<30 for quant". Keep the floor but state where it comes from and that the real number follows from the target margin of error (see Number checks).

**T7. Use cheap unmoderated micro-studies for narrow questions: a five-second test for first impressions, a first-click test for where people expect a function, a preference test between two options; guerrilla tests take 5 to 10 minutes per stranger; lab comparison studies run 8 to 10 people per round.**
Sources: [69], [23] Lyssna, [18] UXtweak.
Status: COVERED for first impressions (references/laws/krug.md Billboard Test; ux-audit stranger test). MISSING-GUIDE: add five-second, first-click and preference tests as named rows in the commands/ux-research.md method table with what each can and cannot answer.

**T8. The whole team watches sessions live, and the debrief happens minutes after each session, not in a later report.**
Sources: [68], [66] (observers take notes).
Status: COVERED (references/process/lean-ux-klein.md "Run the team in the room", "Debrief immediately").

**T9. Unmoderated tests rely only on written tasks and cannot follow up; pair a quantitative unmoderated run with a few moderated sessions to learn the reasons.**
Sources: [68], [69], NNG-CS.
Status: COVERED in part (commands/ux-research.md alternative "Unmoderated remote (n=15+)"). Fold the pairing rule into T3's guidance; not counted separately as new.

**T10. Users skip instruction overlays and coach marks; help that depends on being read first goes unseen.**
Sources: [65].
Status: COVERED (render `first-screen-covered`; references/laws/nielsen-heuristics.md heuristic 10 "Help is there when it is needed").

## 4. Expert review (heuristic evaluation) and severity

**H1. Three to five evaluators inspect the interface independently, about 1 to 2 hours each, and only then merge findings by clustering duplicates.**
Sources: NNG-HE (primary), [70] uxmatters.com, [67] and [71] (descriptions), [63] (Nielsen and Mack TOC).
Status: MISSING-GUIDE: commands/ux-audit.md runs the six lenses as one continuous pass. Add: run lenses as independent passes (or parallel subagents) that do not see each other's findings, then merge and de-duplicate, keeping a count of how many passes found each issue as a confidence signal.

**H2. Make two passes: the first walks the main task end to end to learn the flow, the second inspects each screen and element against the heuristics.**
Sources: NNG-HE.
Status: MISSING-GUIDE: commands/ux-audit.md step 3; flow-level problems (dead ends, missing states) are found on pass one, element problems on pass two.

**H3. Severity is argued from three factors: frequency (how many people hit it), impact (how hard it is to overcome) and persistence (once or every time), with market impact as a modifier. Nielsen's scale: 0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 catastrophe. Rate after the evaluation, each rater alone; one rater is unreliable, the mean of three is usable.**
Sources: NNG-SEV (primary), [70] (traffic-light variant: green, yellow, orange, red).
Status: MISSING-GUIDE: commands/ux-audit.md step 4 defines Critical/High/Medium/Cosmetic by effect on the success signal only. Add the three factors and store them per finding in `.ux/last-audit.json` (`frequency`, `impact`, `persistence`) so severity is reproducible. The four ux-skill levels map cleanly to Nielsen 4 to 1.

**H4. Give every issue a stable unique id, a screenshot or measured evidence, and a recommended fix; state which heuristic set was used.**
Sources: [70].
Status: COVERED for evidence, principle and fix (commands/ux-audit.md finding fields). MISSING-GUIDE: add an `id` field (for example lens initial plus counter, or a hash of rule plus selector) so `/ux-fix`, re-audits and complaint probes can track the same finding across runs.

**H5. Other heuristic sets exist and suit some domains: Shneiderman's eight golden rules, Tognazzini's first principles, Nielsen's top web mistakes; custom heuristics are legitimate when stated.**
Sources: [70].
Status: MISSING-GUIDE (low): a "related sets" paragraph in references/laws/nielsen-heuristics.md.

**H6. Expert review predicts problems; it does not prove them. People fail tasks that look easy and finish ones that look hard, so triangulate with testing.**
Sources: [70], [63] (chapter "Are usability inspection methods as effective as empirical testing?").
Status: COVERED (commands/ux-audit.md `evidence_kind` values `heuristic` and `hypothesis`).

## 5. Personas

**P1. A persona must come from research with real people. One built from team assumptions is a provisional or fictional persona: label it as such and do not let it drive decisions.**
Sources: [27] ixdf.org personas, [28] xd.adobe.com personas, [30] miro.com, [38] xtensio.com.
Status: MISSING-GUIDE: references/process/discovery-protocol.md field 3 records the audience as a one-line string with no evidence. Add an `audience_evidence` value (research, analytics, support logs, sales calls, or assumption) and treat an assumption as provisional in later commands, matching ux-audit's `evidence_kind` vocabulary.

**P2. Derive personas from behavior, not demographics: list about 6 to 8 behavioral variables, place each interviewee on every variable, and look for people who cluster together.**
Sources: [28] (credited to Kim Goodwin), [26] Cooper (About Face; scanned PDF, summarized from known content).
Status: MISSING-GUIDE: commands/ux-research.md synthesis mode and agents/research-synthesizer.md produce themes, not personas; add behavioral-variable clustering as the persona method.

**P3. Keep the set small and name one primary persona per interface: about 3 to 4 (Adobe), 3 to 5 at most (Xtensio); merge personas that would lead to the same design decisions.**
Sources: [27] (more than one, one primary), [28], [38], [26].
Status: MISSING-GUIDE: references/process/discovery-protocol.md (audience) and research-synthesizer output.

**P4. Watch for the elastic user (each stakeholder stretches "the user" to fit an argument) and for self-referential design (designing for yourself). Edge cases inform, they do not drive, the main design.**
Sources: [28], [30], [26].
Status: MISSING-CHECK `audience-is-elastic`, a discovery-time check. Detection: when `/ux-discover` writes `.ux/last-discovery.json`, if `answers.audience` matches `\b(everyone|anyone|all users|users|people|customers|businesses of all sizes|teams of all sizes|anybody)\b` and carries no qualifier (role, context, or task), ask one follow-up for a primary user and their main goal before generating. Optional lint `copy-for-everyone` (low): hero or h1 text matching "for everyone", "for anyone", "for teams of all sizes" (fails ux-audit's swap test).

**P5. Persona content that changes design: end goals (not tasks), evidence-backed frustrations, context (device, setting, skill, interruptions) and behaviors. Leave out details that would not change a decision (age ranges, hobbies, stock photos); use specific values, not ranges.**
Sources: [29] careerfoundry.com persona guide, [30], [38], [28].
Status: MISSING-GUIDE: references/process/discovery-protocol.md field 3 should ask for the primary user's goal, context and main frustration; ux-skill already turns audience into density, mobile-first and register choices, so context is the field that pays off.

**P6. A persona is useless until it appears in a scenario: write when, where and how the primary persona reaches the goal.**
Sources: [27] (Nielsen steps 6 and 9), [29], [30], [28].
Status: COVERED in part (commands/ux-research.md Brief carries `primary_goal`). MISSING-GUIDE: add a one-paragraph "top scenario" optional follow-up to references/process/discovery-protocol.md; it feeds the wow moment and the first-screen content.

**P7. Name a negative persona: who the product is deliberately not for.**
Sources: [38], [26].
Status: MISSING-GUIDE: references/process/discovery-protocol.md, next to field 9 (Avoid list).

**P8. Split buyer and user when they are different people (common in B2B): landing pages argue to the buyer, the app and dashboard serve the user.**
Sources: [38].
Status: MISSING-GUIDE: references/process/discovery-protocol.md field 3; references/surfaces/landing.md vs surfaces/dashboard.md would read different audience fields.

**P9. Personas go stale: light refresh each quarter or major release, structural review yearly, retire the ones nobody matches.**
Sources: [30], [38], [27] (step 10).
Status: MISSING-GUIDE (low): references/process/lean-ux-klein.md "Research operations".

## 6. Journeys, user flows and sitemaps

**J1. A journey map has one actor, one scenario with the actor's expectations, phases, and for each phase the actions, thoughts and a single emotion line, ending in opportunities that each carry an owner and a metric. Separate user types get separate maps; actions are a narrative per phase, not a click log.**
Sources: [44] nngroup.com journey mapping 101, [43] optimizely.com, [45] marvelapp.com, [48] (video, same NN/g topic).
Status: MISSING-GUIDE: ux-skill mentions journey maps only in passing (references/process/lean-ux-gothelf.md). New file references/process/journeys-and-flows.md.

**J2. Choose the map by purpose: experience map (a general human activity, no product), journey map (one product and scenario), service blueprint (adds the internal processes behind each touchpoint), user story map (planning and release slicing).**
Sources: [44], [39] Kalbach (description), [52] (story mapping video).
Status: COVERED for story maps (references/process/lean-ux-gothelf.md "Story mapping"). MISSING-GUIDE for the rest: references/process/journeys-and-flows.md.

**J3. A map is a hypothesis until checked against usability tests, analytics and feedback.**
Sources: [45], [43].
Status: MISSING-GUIDE: references/process/journeys-and-flows.md; tag the map with ux-audit's `evidence_kind`.

**J4. The lowest point on the emotion line is where design effort, reassurance copy and support go.**
Sources: [44], [45], [50] (workshop video, description).
Status: MISSING-GUIDE: commands/ux-design.md should, when a journey exists, name the low-point step and the screen that serves it, and treat that screen as the priority surface.

**J5. Draft the user flow before screens: entry points (not only the home page), each action as a box, each decision as a branch with both exits, and explicit success and failure end states. The flow fixes how many screens there are and in what order; a wireflow puts screen thumbnails in the flow and suits mobile.**
Sources: [46] careerfoundry.com user flows, [53], [54] (videos, description), [148] (course syllabus: user flows before wireframes).
Status: MISSING-GUIDE: references/process/journeys-and-flows.md, invoked by `/ux-design` for any multi-screen app or checkout before generation.

**J6. Every form and decision ends in a visible outcome: submitting with missing input produces a message, not silence.**
Sources: [46] (every decision has two exits), [119] (feedback for every trigger), [106] checklist (design error states).
Status: MISSING-CHECK, render `form-submit-silent` in engine/render/interact.py. Detection: for each visible form with a submit control, clear its fields and submit; within 1000 ms flag when there is no navigation, no element matching `:invalid` that the browser would report, no new or changed visible text, no `[aria-invalid="true"]`, and no `role=alert`/`aria-live` update. Complements `state-answers-late` (timing) and PLAN-4.1 A20/B3 (error wording).

**J7. Many visitors enter on an inner page, not the home page (Dan Brown's "front doors"; at least half by his estimate), so every page must say where it is and offer a way to the rest: global nav, logo linked home, page title, current-location marker.**
Sources: [90] careerfoundry.com IA guide.
Status: Already in inventory (PLAN-4.1 F8 logo home link B-LINT, F9 aria-current PARTIAL; references/laws/krug.md "Street Signs and Breadcrumbs"). Not counted as new.

**J8. A sitemap is the hierarchy drawn from a content inventory and card-sort results; each node is a page with its label.**
Sources: [47] (blocked; description), [91] xd.adobe.com IA guide, [90].
Status: COVERED in part (references/process/brand-extraction.md "Navigation / sitemap" maps the whole nav for redesigns). The remaining gap is handled under IA8 (refactor-existing.md).

## 7. Information architecture and navigation

**IA1. IA has four systems: organization (how content is grouped), labeling (what groups are called), navigation (how people move) and search (how they find by query).**
Sources: [90], [86] and [88] Rosenfeld, Morville, Arango (descriptions), [91].
Status: MISSING-GUIDE: ux-skill has no IA reference (IA appears only in passing in laws-of-ux.md and refactor-existing.md). New file references/foundations/navigation-ia.md.

**IA2. Dan Brown's eight principles: treat content as objects with lifecycles; minimize choices; disclose enough to preview what lies deeper; show exemplars inside category descriptions; design front doors for inner-page entry; offer multiple classifications; keep each navigation focused on one kind of thing; plan for growth.**
Sources: [90].
Status: MISSING-GUIDE: references/foundations/navigation-ia.md.

**IA3. People look for information four ways: known-item, exploratory, exhaustive research and re-finding. Known-item seeking needs search; exploring needs browsable categories; re-finding needs history, saved items or stable URLs. A long collection with neither search nor filters serves none of them.**
Sources: [90] (Morville and Rosenfeld's four needs), [86].
Status: MISSING-CHECK, render `large-collection-no-finder`. Detection: at 1280px, find a container with 24 or more visible sibling items sharing the same tag and class signature (cards, rows, list items); flag when the page has no `input[type=search]`, no `[role=search]`, no `select` or button group within 600px above the collection, and no pagination or "load more" control. MISSING-GUIDE: references/foundations/navigation-ia.md.

**IA4. Labels are specific and familiar ("About", not "General Information"); catch-all labels hide content.**
Sources: [91], [90].
Status: MISSING-CHECK, lint `nav-label-vague`. Detection: link or button text inside `nav`, `header` or `[role=navigation]` that, trimmed and lowercased, equals one of more, misc, miscellaneous, other, others, stuff, things, general, general information, info, information, links, click here. Advisory tier; "Resources" and "Solutions" are left out because they are conventional.

**IA5. Do not size menus by Miller's "seven plus or minus two". Miller describes short-term memory; a visible menu is recognition, not recall. Keep top-level navigation short because scanning and choosing cost time (Hick), and group long sets.**
Sources: [91] (claims Miller means "never more than seven" options), lawsofux.com/millers-law (primary takeaway: do not use the magical number seven to justify unnecessary design limits).
Status: MISSING-GUIDE (conflict fix): references/laws/laws-of-ux.md section 18 says "For navigation, prefer five to seven top-level items" under Miller's law and lists navigation menus as where it applies; reattribute the nav cap to Hick's law and scanning cost, and add the lawsofux.com caveat.

**IA6. Card sorting: 30 to 50 cards (above 50 people dump cards into a miscellaneous pile); at least 15 participants for a qualitative sort, 30 to 50 for a quantitative one; open sorts generate groupings, closed sorts and tree tests validate them; ask for group names only after grouping; never repeat the same word across cards, or people group by keyword match.**
Sources: NNG-CS (primary), [69], [66], [90], [91].
Status: COVERED in part (commands/ux-research.md "Card sort + cluster analysis (n=15-25)"). MISSING-GUIDE: add card count, the label-after-grouping order and the keyword-match rule to the card-sort artifact in commands/ux-research.md; raise the quantitative range to 30 to 50.

**IA7. Tree testing checks a hierarchy using only its labels: measure success, directness, time and first choice; tasks must not reuse label words; always tree-test the hierarchy a card sort produced; compare alternative trees between subjects.**
Sources: NNG-TT (primary), [90], [18], [23].
Status: MISSING-GUIDE: tree testing appears nowhere in ux-skill (grep of references, commands, agents). Add a row to the commands/ux-research.md method table and a short section to references/foundations/navigation-ia.md.

**IA8. Before restructuring, take a content inventory (full, or partial for the top levels) and audit each item for usefulness, accuracy and effectiveness.**
Sources: [90], [91].
Status: MISSING-GUIDE: references/process/refactor-existing.md "Audit first" covers UX equity, not content; add an inventory and audit step with a sitemap output.

**IA9. Keep each navigation focused: separate utility links (sign in, cart, language) from content sections.**
Sources: [90] (focused navigation).
Status: COVERED (references/surfaces/landing.md "Utility and announcement topbar").

**IA10. Plan navigation for growth: a nav designed for five items breaks at twelve, and the first sign is items wrapping onto a second line.**
Sources: [90] (growth), [91] (scalable taxonomy).
Status: MISSING-CHECK, render `nav-wraps`. Detection: at 1280 and 1024px, take the link boxes of the first `header nav` (or first `[role=navigation]`) that is not a hamburger state; flag when their top coordinates fall into two or more rows more than half a line height apart, or when the nav's scrollWidth exceeds its clientWidth.

## 8. Interaction design principles

**IX1. Interaction design works in five dimensions: words, visual representations, physical objects and space (device, setting), time (motion, sound, progress) and behavior.**
Sources: [105] ixdf.org what is interaction design, [108] (video, description).
Status: COVERED (references/foundations/interaction.md, motion.md, copy.md).

**IX2. Norman's principles carry the field: visibility, feedback, constraints, mapping, consistency and affordance, plus the cognitive laws (Hick, Fitts, serial position).**
Sources: [106] uxpin.com, [103] (companion site chapter list), [109] to [111] (videos, description).
Status: COVERED (references/laws/norman.md, references/laws/laws-of-ux.md).

**IX3. Every action yields a perceivable response, and that response also reaches assistive technology.**
Sources: [106], [105].
Status: COVERED (render `state-answers-late`; lint `aria-live-polite-on-error`, `aria-busy-without-aria-live`).

**IX4. Decide the input methods per surface (tap, swipe, long press, keyboard, voice) and give every gesture a visible alternative.**
Sources: [106].
Status: COVERED (references/foundations/interaction.md "Gesture with visible affordance", "Gesture vocabulary"; PLAN-4.1 A15).

**IX5. Physical context sets the target size and density: one hand on a crowded train is not a desk with a mouse.**
Sources: [105].
Status: COVERED (render `target-too-small`; references/foundations/interaction.md Touch target sizes).

**IX6. Goal-directed design: design for the person's end goal, not the task list or the feature list (Cooper's experience, end and life goals).**
Sources: [99] About Face (description), [26] (Cooper chapter, summarized from known content), [112] (task analysis, description).
Status: MISSING-GUIDE: belongs in the references/laws/cooper.md file PLAN-4.1 already proposes for posture, excise and perpetual intermediates (H4 to H6); goal types are not in that list, so this is counted as new.

**IX7. Gradual engagement: let people use the product before asking for an account, break big requests into small steps, use sensible defaults and fewer choices. Anderson also lists scarcity and unpredictable rewards; ux-skill's honesty rules keep those out.**
Sources: [101] Seductive Interaction Design (publisher TOC).
Status: Already in inventory for checkout (PLAN-4.1 B14, defer account creation, C). MISSING-GUIDE for product onboarding: references/conditional/habit-design.md (try before sign-up), with a pointer to lint `fake-urgency`.

**IX8. Let people track progress through a long task and resume it later; time is a design material.**
Sources: [105].
Status: Already in inventory (PLAN-4.1 B16 progress and back keeps data; A17 re-entered data). Not counted as new.

## 9. Microinteractions and interface animation

**MI1. A microinteraction has a trigger (user or system), rules, feedback, and loops and modes.**
Sources: [119] nngroup.com microinteractions, [118] vev.design, [113] Saffer (description).
Status: COVERED (PLAN-4.1 F16; references/foundations/motion-principles.md).

**MI2. Feedback appears where the person is looking, next to the trigger; a confirmation the person cannot see is no confirmation.**
Sources: [119].
Status: MISSING-CHECK, render `feedback-out-of-view` in engine/render/interact.py. Detection: at 390x844, click each primary button and submit control; record DOM mutations for 1000 ms; flag when every visible mutated node lies outside the current viewport and focus did not move into the changed region (for example a success message rendered at the top of a long form while the person is at the bottom).

**MI3. A changed state looks different from the prior state, and the control exposes its state: a disclosure button reports expanded or collapsed, a toggle reports pressed.**
Sources: [119] (distinct states; Gap heart example).
Status: MISSING-CHECK, render `disclosure-state-missing` in engine/render/interact.py. Detection: click each `button` (and `[role=button]`) that is not a submit; if another element changes between hidden and visible and the clicked control has neither `aria-expanded` nor `aria-pressed` nor `role=tab` with `aria-selected`, flag. Basis: WCAG 4.1.2 Name, Role, Value requires that states of user interface components can be programmatically determined. Existing structure.py logic only covers menus and hamburgers.

**MI4. Microinteraction feedback is brief and ends; it never becomes a permanent loop.**
Sources: [119].
Status: COVERED (lint `infinite-animation-without-reduced-motion`; render `moving-content-without-pause`).

**MI5. Every microinteraction has a job (show status, prevent an error, invite engagement, carry the brand); decorative ones stay subtle and few, because many of them complicate a design.**
Sources: [119], [118], [117], [120] to [122] (descriptions).
Status: COVERED (references/foundations/motion-principles.md "Every animation has a purpose", "Frequency gating").

**MI6. Prevent errors while typing: show password rules up front and tick each as it is met, instead of rejecting after submit.**
Sources: [119] (eBay password requirements).
Status: MISSING-CHECK, lint `password-rules-hidden` (low). Detection: `input[type=password]` with `minlength`, `pattern` or a `name`/`autocomplete="new-password"` and no `aria-describedby`, and no text within its field container mentioning "character", "letter", "number" or "symbol". MISSING-GUIDE: references/foundations/component-behaviors.md (Form).

**MI7. Celebration flourishes (confetti, mascots) are rare rewards and match the brand; a professional product avoids comic touches.**
Sources: [119] (Asana unicorn appears only sporadically).
Status: COVERED (references/foundations/motion-principles.md "Frequency gating"; brand voice in references/foundations/copy.md).

**MI8. Do not start from zero: use what the system already knows (last value, locale, device) to prefill and default.**
Sources: [113] (Saffer, known content).
Status: COVERED (PLAN-4.1 A17, WCAG 3.3.7 Redundant Entry, in references/foundations/accessibility.md).

**MI9. Interface animation earns its place by aiding feedback, orientation (where things come from and go) and attention, and stays short.**
Sources: [115] Val Head (description), [123] to [126] (videos, description).
Status: COVERED (references/foundations/motion-principles.md durations and purpose rules).

## 10. Prototyping and fidelity

**PR1. Fidelity is three separate dials: visual polish, content realism and interactivity. Set each to the question being asked, and prototype only what that question needs.**
Sources: [154] netsolutions.com, [133], [129] (UXPin: "prototype only what you need, then stop").
Status: MISSING-GUIDE: references/process/generation-modes.md has variant axes (style, layout, density, motion) but no fidelity axis.

**PR2. Low fidelity answers concept and flow questions early and cheaply; high fidelity comes after flows are validated, to test microcopy, animation, color, complex interactions or many-screen apps.**
Sources: [154], [153] locofy.ai, [133], [140], [142], [152].
Status: COVERED for testing (references/process/lean-ux-klein.md "Low-fi over high-fi early"). MISSING-GUIDE for generation: references/process/generation-modes.md should offer a structure-first wireframe pass (grayscale, one typeface, real copy, boxes for media) when the brief's flow is unvalidated, before the styled build.

**PR3. Polish suppresses honest feedback: people critique structure on rough work and hesitate to suggest changes to finished-looking work.**
Sources: [140], [152], [133] (paper is obviously unfinished, so critique is candid).
Status: MISSING-GUIDE: references/process/generation-modes.md (Shotgun Exploration) and references/process/creative-selection.md; when asking a client to choose a structure, show structure-only variants.

**PR4. Wireframe rules: grayscale, one typeface with size steps for hierarchy, boxes for media, as few layouts as possible, and real headlines and calls to action instead of lorem ipsum.**
Sources: [133], [142] balsamiq.com, [140], [143].
Status: COVERED (lint `lorem-ipsum-leak`, `placeholder-token-shipped`; references/process/visual-translation.md "Sketch or wireframe" keeps the skeleton binding).

**PR5. On phones, layouts hold one or two columns at most.**
Sources: [140].
Status: MISSING-CHECK, render `mobile-columns-over-two`. Detection: at 390px, find rows where three or more sibling boxes sit side by side (same top within 8px), each narrower than 34% of the viewport and each holding more than 12 characters of text; exclude nav, tab bars, toolbars, icon rows and chip lists. references/foundations/responsive.md already says phones default to one column but nothing measures it.

**PR6. Wizard of Oz prototypes fake the hard back end with a person; they suit AI, chat and voice ideas, and the wizard needs a written behavior script so responses stay consistent across sessions.**
Sources: [133].
Status: COVERED (references/process/lean-ux-gothelf.md and lean-ux-klein.md "Wizard of Oz"). The wizard-script detail is small; fold it into those sections.

**PR7. A high-fidelity prototype that omits core features and states leaves developers to guess, which causes rework; design the edge, empty and error states too.**
Sources: [153], [106] (checklist: edge cases and error states).
Status: COVERED (references/foundations/components.md state specs; references/surfaces/dashboard.md "Chart with full state coverage").

**PR8. Coded, live responsive prototypes show real behavior at every breakpoint, unlike static frames drawn per screen size.**
Sources: [153].
Status: COVERED (ux-skill builds code and renders at 390, 430, 768 and 1280).

**PR9. Frame the context with storyboards (a big-picture board for the situation, a close-up board for the screen moment) before wireframing.**
Sources: [148] (Google course syllabus).
Status: MISSING-GUIDE (low): references/process/journeys-and-flows.md.

**PR10. Wireframes are where global and secondary navigation terms get settled and tested, and where design and copy discover that real content does not fit the layout.**
Sources: [141] experienceux.co.uk.
Status: COVERED (render `text-overflows-its-box`; references/foundations/copy.md). The navigation-terms part is covered by IA4 and IA7.

## 11. Tools: what ux-skill can learn from their approach

**TL1. Maze scores each prototype screen deterministically: start at 100, subtract 0.5 points per percentage point of misclicks and a duration penalty (none up to 5 s, then 1 point per 2 s, capped at 10); bands are 80 to 100 high, 50 to 80 medium, 0 to 50 low.**
Sources: [79] maze.co, Maze help center formula (search result text; the help page's own worked example does not fully match its formula).
Status: COVERED in spirit (ux-skill already has deterministic scored dimensions). Lesson for ux-skill: publish the penalty per finding as Maze does, so a score change can be explained line by line. Not counted as new guidance.

**TL2. Analytics tools flag rage clicks and dead clicks: elements that look clickable but do nothing.**
Sources: [19] Hotjar (Contentsquare).
Status: MISSING-CHECK, render `dead-click` in engine/render/interact.py. Detection: for each visible `button`, `[role=button]`, `a[href]` and element with computed `cursor: pointer`, click it in a fresh page state; flag when within 500 ms there is no navigation, no DOM mutation, no focus change, no dialog and no network request. Static rules `href-empty-hash`, `link-onclick-no-href` and `cursor-pointer-non-interactive` cover only some anchors; a button wired to nothing (common in AI-built pages: "Get started" with no handler) is not caught today.

**TL3. Lyssna, UXtweak and Optimal Workshop package five-second, first-click, preference, card-sort and tree tests as small unmoderated studies with panels.**
Sources: [18], [23], [12] (dead).
Status: Merged into T7 and IA7 (the guidance gap is recorded there).

**TL4. UserTesting, Userbrain, Userlytics and Userfeel run panel-based think-aloud tests; Userbrain sells them as a recurring subscription.**
Sources: [20], [21], [82], [83].
Status: COVERED (references/process/lean-ux-klein.md "The fast cycles", continuous small rounds).

**TL5. Persona tools (User Forge, Xtensio) offer templates and AI persona generators; a generated persona without research is a fictional persona.**
Sources: [37], [38].
Status: Merged into P1.

**TL6. Flows and sitemaps live in diagram tools (Whimsical, Miro, FigJam, Lucidchart, Cacoo, draw.io). ux-skill can emit flows and sitemaps as Mermaid text that pastes into most of them.**
Sources: [55] to [60].
Status: MISSING-GUIDE: references/process/journeys-and-flows.md output format (Mermaid flowchart for flows, indented tree or Mermaid graph for sitemaps).

---

## Number checks and conflicts

- Five users: NN/g's formula is N(1-(1-L)^n) with L = 31% averaged across projects; five users find about 84%, which NN/g rounds to 85%; 15 users find nearly all. Three rounds of five beat one of fifteen. ux-skill (lean-ux-klein.md, krug.md) matches.
- Lab rounds: Hotjar/Contentsquare [69] says lab tests "typically" run 8 to 10 people per round; NN/g says 5 for a qualitative round. Not a real conflict: the larger number is for controlled comparison studies.
- Per-group samples: NN/g says 3 to 4 per group for two groups and 3 per group for three or more. ux-skill gives a flat 5 to 8 (gap, I3).
- Quantitative studies: NN/g recommends 20 users; commands/ux-research.md sets a floor of 30. Sauro and Lewis derive n from the target margin of error. ux-skill's 30 is stricter than NN/g's 20; keep it but explain (T6).
- Card sorting: NN/g says at least 15 participants for qualitative and 30 to 50 for quantitative, with 30 to 50 cards. ux-skill's "n=15-25" fits qualitative only (IA6).
- Heuristic evaluators: NN/g's current page says 3 to 5 evaluators, 1 to 2 hours each, and gives no percentages. UXmatters [70] attributes to Nielsen and Landauer that three experts find about 60% and ten about 85%. The figures often quoted elsewhere (one evaluator about 35%, five about 75%) were not found on any page fetched here; treat all such percentages as unverified until checked against Nielsen and Landauer 1993.
- Severity: NN/g's 0 to 4 scale; a single rater is unreliable and the mean of three is usable for practical purposes; each rater spends about 30 minutes.
- SUS: 10 items, 5 options, x2.5 scoring; mean 68 across 500 studies; A above 80.3 (top 10%); F below 51 (bottom 15%); usable with very small samples if a confidence interval is reported.
- Persona counts: 3 to 4 (Adobe [28]), 3 to 5 at most (Xtensio [38]), "more than one, one primary" (IxDF [27]). Consistent on one primary persona.
- Interview saturation: Xtensio [38] claims 5 interviews surface 80% of recurring themes, with no source. This is a different phenomenon from NN/g's usability-problem curve; do not reuse the 85% figure for interview themes.
- Miller's law: Adobe [91] says options "should never be more than seven"; lawsofux.com's own takeaway warns against using the magical number seven to justify design limits. ux-skill's references/laws/laws-of-ux.md section 18 repeats the menu cap under Miller (IA5).
- Front doors: CareerFoundry [90] cites Dan Brown for "at least 50%" of visitors entering through a page other than the home page. Brown's 2010 paper was not fetched here; recorded as cited, not verified.
- Microinteraction timing: NN/g [119] gives no durations; Figma prototypes accept 1 to 10000 ms. No conflict with ux-skill's motion ranges.
- Maze score: the help-center formula and its worked example disagree on how success rate enters the mission score; the screen-level penalties (0.5 per misclick point; duration penalty capped at 10) are consistent.
- UXPin [129] claims prototypes improve estimate accuracy by 50% and cut clarification requests by 80%; no source is given. Do not cite.
- List attribution errors found while checking: row 34 and row 108 are IxDF videos credited to CareerFoundry; row 95 is a CareerFoundry video credited to Toptal; row 144's title promises a prototyping vs wireframing comparison the page does not contain; UsabilityHub is now Lyssna, UserZoom is part of UserTesting, Hotjar is part of Contentsquare.

---

## Summary of proposals

### New checks (MISSING-CHECK)

| Id | Kind | Where | Lesson | One-line detection |
|---|---|---|---|---|
| `dead-click` | render | interact.py | TL2 | click each clickable-looking element; no navigation, mutation, focus change, dialog or request within 500 ms |
| `form-submit-silent` | render | interact.py | J6 | submit each form empty; no invalid state, alert, aria-invalid or new visible text within 1000 ms |
| `disclosure-state-missing` | render | interact.py | MI3 | a button toggles another element's visibility but has no aria-expanded, aria-pressed or tab selection state |
| `feedback-out-of-view` | render | interact.py | MI2 | after clicking a primary action at 390x844, every visible change is outside the viewport and focus stays put |
| `mobile-columns-over-two` | render | core.py | PR5 | at 390px, 3+ side-by-side text boxes each under 34% width, excluding nav and toolbars |
| `nav-wraps` | render | core.py | IA10 | at 1280 and 1024px, header nav links fall on 2+ rows or the nav overflows |
| `large-collection-no-finder` | render | core.py | IA3 | 24+ same-signature siblings and no search, filter, sort or pagination control |
| `nav-label-vague` | lint | data/anti-patterns.json | IA4 | nav link text equals more, misc, other, stuff, things, general, info, links, click here |
| `password-rules-hidden` | lint | data/anti-patterns.json | MI6 | password input with minlength/pattern/new-password and no describedby or rule text |
| `task-primes-label` | command self-check | commands/ux-research.md | T2 | task sentences containing an exact UI label from the page snapshot |
| `audience-is-elastic` | discovery check | commands/ux-discover.md | P4 | audience answer is a generic noun (everyone, users, people) with no role, context or task |

Every render rule above becomes a `rule-clear` complaint probe target once its id is in `_RULES` (no new probe kind needed). Low-priority extra: lint `copy-for-everyone` (P4).

### New guidance (MISSING-GUIDE), by target file

- New references/process/journeys-and-flows.md: J1, J2, J3, J5, PR9, TL6.
- New references/foundations/navigation-ia.md: IA1, IA2, IA3, IA7.
- commands/ux-research.md: R2, R3, R5, R6, I3, I4, T3, T4, T6, T7, IA6, IA7, P2.
- commands/ux-audit.md: H1, H2, H3, H4.
- commands/ux-design.md: J4.
- references/process/discovery-protocol.md: P1, P3, P5, P6, P7, P8.
- references/process/generation-modes.md: PR1, PR2, PR3.
- references/process/refactor-existing.md: IA8 (with J8).
- references/process/lean-ux-klein.md: R6, P9.
- references/laws/laws-of-ux.md: IA5 (conflict fix).
- references/laws/nielsen-heuristics.md: H5.
- references/laws/cooper.md (already proposed by PLAN-4.1): IX6.
- references/conditional/habit-design.md: IX7.
- references/foundations/component-behaviors.md: MI6.

---

# Part 2: Ledger of every link

Status values: read; summarized from description; blocked (403), summarized from description; tool noted; dead; out of scope. Lesson ids in the takeaway column point to Part 1.

| # | Title | URL | Type | Status | Takeaway |
|---|---|---|---|---|---|
| 1 | Think Like a UX Researcher: How to Observe Users, Influence Design, and Shape Business Str | https://www.goodreads.com/book/show/123871628-think-like-a-ux-researcher | book | summarized from description | Research as a practice: plan studies, observe behavior, and tie findings to business strategy (publisher blurb; not read in full). |
| 2 | Think Like a UX Researcher: How to Observe Users, Influence Design, and Shape Business Str | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 3 | Researching UX: User Research | https://www.goodreads.com/book/show/34497740-researching-ux | book | summarized from description | Short practitioner guide to planning and running user research (description only). |
| 4 | Researching UX: User Research | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 5 | Quantifying the User Experience. Practical Statistics for User Research | https://shop.elsevier.com/books/quantifying-the-user-experience/sauro/978-0-12-802308-2 | book | summarized from description | Sauro and Lewis, 2nd ed. 2016: confidence intervals, sample sizes for formative and summative studies, standard questionnaires (TOC and blurb). |
| 6 | Quantifying the User Experience. Practical Statistics for User Research | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 7 | Observing the User Experience, Second Edition: A Practitioner's Guide to User Research | https://shop.elsevier.com/books/observing-the-user-experience/goodman/978-0-12-384869-7 | book | summarized from description | Goodman and Kuniavsky, 2nd ed. 2012: interviews, field visits, diary studies, card sorts, surveys, personas and scenarios as deliverables (TOC). |
| 8 | Observing the User Experience, Second Edition: A Practitioner's Guide to User Research | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 9 | Starter questions for User research interviews | https://projects.iq.harvard.edu/files/harvarduxgroup/files/ux-research-guide-sample-questions-for-user-interviews.pdf | other (PDF question bank) | blocked (403); summarized from description | Starter interview questions by Sarah Doody; lesson merged into recent-behavior interviewing (I1). |
| 10 | Introduction To UX Research ( User Research) | https://uxplanet.org/introduction-to-ux-research-user-research-a2f27a6413ff | article | blocked (403); summarized from description | Intro to UX research; no specific lesson beyond the method overview covered by I1 and R2. |
| 11 | The UX Research Methods You Need To Know | https://careerfoundry.com/en/tutorials/ux-research-for-beginners/an-introduction-to-ux-research-methods/ | article | dead | Page is a 'page has moved' stub; CareerFoundry banner says the company is ceasing operations. |
| 12 | Intro to UX research | https://blog.optimalworkshop.com/intro-to-ux-research/ | article | dead | blog.optimalworkshop.com no longer answers (connection fails); the new-site path returns 404. |
| 13 | What is User Research? | https://ixdf.org/literature/topics/user-research | article | read | Qual vs quant, say vs do, discover/explore/test/listen stages, six-step study plan (R2, R3). |
| 14 | User Research Introduction | https://medium.com/user-research/user-research-introduction-126ce1e4e546 | article | blocked (403); summarized from description | Medium intro to user research; nothing beyond R1 and R2. |
| 15 | What is UX Research? | https://www.youtube.com/watch?v=kQ_6faxhyIw | video | summarized from description | Google UX certificate intro to research (oEmbed metadata only). |
| 16 | UX Research: Get Started With Qualitative User Research (2023) | https://www.youtube.com/watch?v=bAARmsv1tms | video | summarized from description | CareerFoundry intro to qualitative research (metadata only). |
| 17 | Great Design With User Research: Design a Mobile App Using Figma | https://www.youtube.com/watch?v=YD0egXpd-Y0 | video | summarized from description | freeCodeCamp: research-led mobile app design in Figma (metadata only). |
| 18 | UXtweaks | https://www.uxtweak.com/ | tool | tool noted | UXtweak: tree tests, card sorts, first-click, five-second, session recording; supports IA7 and T7. |
| 19 | Hotjar | https://contentsquare.com/hotjar/ | tool | tool noted | Hotjar, now under Contentsquare: heatmaps, recordings, rage and dead clicks; inspires the dead-click render check (TL2). |
| 20 | UserTesting | https://www.usertesting.com/ | tool | tool noted | UserTesting: panel-based unmoderated think-aloud video tests. |
| 21 | Userbrain | https://www.userbrain.com/en/ | tool | tool noted | Userbrain: subscription unmoderated tests on a schedule; supports continuous small rounds (T1). |
| 22 | UserZoom | https://www.usertesting.com/platform/userzoom | tool | tool noted | UserZoom, now part of UserTesting: quantitative benchmarking and unmoderated studies. |
| 23 | UsabilityHub | https://www.lyssna.com/ | tool | tool noted | UsabilityHub renamed Lyssna: five-second, first-click, preference, card sort, tree test, surveys (page read). |
| 24 | Personas: User Focused Design | https://books.google.com/books/about/Personas_User_Focused_Design.html?id=NoBgC0NEInEC | book | summarized from description | Lene Nielsen, Springer 2012: engaging personas and her 10 steps to personas (Google Books description and TOC). |
| 25 | Personas: User Focused Design | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 26 | Modeling Users: Personas and Goals | http://www.cs.cmu.edu/~jhm/Readings/cooper_personas.pdf | book chapter (scanned PDF) | summarized from description | Cooper's personas and goals chapter; scanned image PDF with no text layer, so summarized from the known About Face content (P2, P3, P4, IX8). |
| 27 | Personas: A Simple Introduction | https://ixdf.org/literature/article/personas-why-and-how-you-should-use-them | article | read | Four persona types; Nielsen's 10 steps; one primary persona; 1 to 2 pages each; fictional personas must not drive decisions (P1, P3, P6). |
| 28 | What Are User Personas and Why Are They Important? | https://xd.adobe.com/ideas/process/user-research/putting-personas-to-work-in-ux-design/ | article | read | Provisional personas, 6 to 8 behavioral variables, 3 to 4 personas, elastic user and self-referential design (P1 to P4). |
| 29 | How to Define a User Persona | https://careerfoundry.com/en/blog/ux-design/how-to-define-a-user-persona/ | article | read | Persona = header, profile, end goals, scenario; one page; omit details that change no decision (P5, P6). |
| 30 | Introduction to Developing User Personas | https://miro.com/blog/introduction-user-personas/ | article | read | Persona research mix, revisit each major release, throw-away personas, scenario required (P6, P9). |
| 31 | What Are User Personas? How to Create Personas in 4 Steps | https://uxplanet.org/how-to-create-user-personas-2f9d5e3a0e2b | article | blocked (403); summarized from description | Four-step persona creation; merged into P1 to P5. |
| 32 | An Overview of User Personas | https://uxplanet.org/an-overview-of-user-personas-b26e9c543be5 | article | blocked (403); summarized from description | Persona overview; merged into P1 to P5. |
| 33 | Intro to Personas in UX Design | https://www.youtube.com/watch?v=An2qbKbyY6g | video | summarized from description | Intro to personas (metadata only). |
| 34 | What are Personas? | https://www.youtube.com/watch?v=XnG4c4gXaQY | video | summarized from description | README credits CareerFoundry but the video is IxDF's 'All About User Personas' (metadata only). |
| 35 | How To Create A User Persona (Video Guide) | https://www.youtube.com/watch?v=DvV7ZcRVQ4g | video | summarized from description | CareerFoundry persona video guide (metadata only). |
| 36 | Creating Personas for User Experience Research | https://www.youtube.com/watch?v=u44pBnAn7cM | video | summarized from description | PlaybookUX: personas for UX research (metadata only). |
| 37 | User Forge | https://userforge.com/ | tool | tool noted | User Forge: persona and user story cards; template sections match P5. |
| 38 | Xtensio | https://xtensio.com/how-to-create-a-persona/ | tool | read | Xtensio persona template; 5 to 8 interviews per segment, 3 to 5 personas max, buyer vs user, negative personas, refresh cadence (P3, P7, P8, P9). |
| 39 | Mapping Experiences: A Complete Guide to Creating Value through Journeys, Blueprints, and  | https://www.goodreads.com/work/editions/46787723-mapping-experiences-a-complete-guide-to-creating-value-through-journeys | book | summarized from description | Kalbach, Mapping Experiences (O'Reilly 2016, 2nd ed. 2020): alignment diagrams, journeys, blueprints (description). |
| 40 | Mapping Experiences: A Complete Guide to Creating Value through Journeys, Blueprints, and  | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 41 | User Journey Mapping | https://www.goodreads.com/book/show/61051829-user-journey-mapping | book | summarized from description | User Journey Mapping (Goodreads blurb): using maps to understand how people use products. |
| 42 | User Journey Mapping | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 43 | User journey map | https://www.optimizely.com/optimization-glossary/user-journey-map | article | read | Journey map components, one map per primary persona and use case, share beyond product team (J1, J2). |
| 44 | Journey Mapping 101 | https://www.nngroup.com/articles/journey-mapping-101/ | article | read | NN/g: actor, scenario and expectations, phases, actions/mindsets/emotions, opportunities; map type differences (J1 to J3). |
| 45 | A Beginner's Guide To User Journey Mapping | https://marvelapp.com/blog/beginners-guide-user-journey-mapping/ | article | read | Eight-step journey mapping process ending in validation against tests and analytics (J4, J5). |
| 46 | What are User Flows in User Experience (UX) Design? | https://careerfoundry.com/en/blog/ux-design/what-are-user-flows/ | article | read | Task flow vs user flow vs wireflow; rectangles for actions, diamonds for decisions; flows set screen count and order (J6). |
| 47 | How to create a UX Sitemap: a simple guideline | https://uxdesign.cc/how-to-create-a-ux-sitemap-a-simple-guideline-8786c16f85c1 | article | blocked (403); summarized from description | How to build a UX sitemap; merged into J9. |
| 48 | Customer Journey Mapping 101 | https://www.youtube.com/watch?v=2W13ext26kQ | video | summarized from description | NN/g journey mapping 101 (metadata only). |
| 49 | Customer Journey Mapping 101 | https://www.youtube.com/watch?v=2W13ext26kQ | video | summarized from description | Duplicate of the previous row (same URL). |
| 50 | Customer Journey Map Workshop | https://www.youtube.com/watch?v=X7iXcP-wIkk | video | summarized from description | PlaybookUX journey map workshop (metadata only). |
| 51 | Customer Journey Mapping Tutorial | https://www.youtube.com/watch?v=3iwL2OEeWiw | video | summarized from description | Journey mapping tutorial (metadata only). |
| 52 | How to do User Story Mapping | https://www.youtube.com/watch?v=k_4SchJgAI4 | video | summarized from description | User story mapping (metadata only); story maps already in lean-ux-gothelf.md. |
| 53 | UX Design: Why you NEED to know User Flows! | https://www.youtube.com/watch?v=4uHxJMCzeGg | video | summarized from description | Why user flows matter (metadata only). |
| 54 | Create User Flow Diagrams From Customer Journey Maps | https://www.youtube.com/watch?v=pcCUP23X9g8 | video | summarized from description | Deriving user flow diagrams from journey maps in FigJam (metadata only); supports J6. |
| 55 | Whimsical | https://whimsical.com/ | tool | tool noted | Whimsical: flowcharts, wireframes, mind maps (TL6). |
| 56 | Miro | https://miro.com/ | tool | tool noted | Miro: whiteboard for maps and workshops (TL6). |
| 57 | Figjam | https://www.figma.com/figjam/ | tool | tool noted | FigJam: whiteboard inside Figma (TL6). |
| 58 | Lucidchart | https://lucid.co/lucidchart | tool | tool noted | Lucidchart: diagramming with data import and automation (TL6). |
| 59 | Cacoo | https://nulab.com/cacoo/ | tool | tool noted | Cacoo: collaborative diagrams (TL6). |
| 60 | Drawio | https://app.diagrams.net/ | tool | tool noted | draw.io / diagrams.net: free diagram editor (TL6). |
| 61 | Handbook of Usability Testing: Howto Plan, Design, and Conduct Effective Tests | https://www.goodreads.com/book/show/2203883 | book | summarized from description | Rubin and Chisnell: planning, running and reporting usability tests (blurb). |
| 62 | Handbook of Usability Testing: Howto Plan, Design, and Conduct Effective Tests | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 63 | Usability Inspection Methods | https://www.nngroup.com/books/usability-inspection-methods/ | book | summarized from description | Nielsen and Mack 1994: heuristic evaluation, cognitive and pluralistic walkthroughs, inspections vs testing (TOC from NN/g page). |
| 64 | Usability Inspection Methods | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 65 | What is User Testing?: Learn UX: Keep It Usable | https://www.keepitusable.com/blog/what-is-user-testing/ | article | read | User testing basics; SUS as the satisfaction score; users skip instructions and overlays (T4, T11). |
| 66 | 6 Simple Steps to Conduct User Testing Successfully | https://adamfard.com/blog/conduct-user-testing | article | read | Six steps; 3 to 5 users, preferably 5; exclude staff, family and friends; vague goal scenarios; scripted consistency (I2, I4, T2). |
| 67 | How to Conduct a Heuristic Evaluation | https://uxplanet.org/how-to-conduct-heuristic-evaluation-85548a355dca | article | blocked (403); summarized from description | How to run a heuristic evaluation; merged into H1 to H4. |
| 68 | Usability Testing 101 | https://www.nngroup.com/articles/usability-testing-101/ | article | read | NN/g: facilitator, tasks, participant; 5 users; 3-day discount study; priming risk in task wording (T1, T2, R5). |
| 69 | 8 Usability Testing Methods That Work | https://contentsquare.com/guides/usability-testing/methods/ | article | read | Eight methods: lab 8 to 10 per round, guerrilla 5 to 10 min, five-second and first-click tests, session replay shows what not why (T7, R4). |
| 70 | An Overview of Expert Heuristic Evaluations | https://www.uxmatters.com/mt/archives/2014/06/an-overview-of-expert-heuristic-evaluations.php | article | read | Expert review steps, traffic-light severity, unique issue ids, alternate heuristic sets; not a substitute for testing (H4 to H6). |
| 71 | The A to Z of UX: H is for Heuristics: 9 steps to carry out a heuristic evaluation | https://uxdesign.cc/the-a-to-z-of-ux-h-is-for-heuristics-9-steps-to-carry-out-a-heuristic-evaluation-a1f5225c4e83 | article | blocked (403); summarized from description | Nine-step heuristic evaluation; merged into H1 to H4. |
| 72 | User & Usability Testing: Methods & Tips | https://xd.adobe.com/ideas/process/user-testing/ | article | read | Adobe testing hub: success rate and time on task as core metrics; plan analysis time (T4). |
| 73 | Heuristic Evaluation: GoodReads, LibraryThing, Litsy | https://uxplanet.org/heuristic-evaluation-goodreads-librarything-litsy-a3a4d8373255 | article | blocked (403); summarized from description | Worked heuristic evaluation of three reading apps; example only. |
| 74 | Uncovering Secrets of User Testing in 5 Minutes! | https://www.youtube.com/watch?v=CU_tfEGwit8 | video | summarized from description | Five-minute user testing primer (metadata only). |
| 75 | You need to know Usability Testing (with Maze) | https://www.youtube.com/watch?v=ID0fwi2q028 | video | summarized from description | Usability testing with Maze (metadata only). |
| 76 | Intro to Usability Testing and Heuristic Evaluations | https://www.youtube.com/watch?v=-PxgUK9u3Rk | video | summarized from description | University lecture on usability testing and heuristic evaluation (metadata only). |
| 77 | Usability Testing Tips & Tools: Powerful UX Research Method | https://www.youtube.com/watch?v=RyGFEmimwoM | video | summarized from description | Usability testing tips and tools (metadata only). |
| 78 | The 10 Usability Heuristics | https://www.youtube.com/playlist?list=PLJOFJ3Ok_idtb2YeifXlG1-TYoMBLoG6I | video | summarized from description | NN/g playlist on the 10 heuristics; covered by references/laws/nielsen-heuristics.md. |
| 79 | Maze | https://maze.co/ | tool | tool noted | Maze: unmoderated prototype tests with a usability score built from success, misclicks and duration (TL1). |
| 80 | UserTesting | https://www.usertesting.com/ | tool | tool noted | Duplicate of row 20 (UserTesting). |
| 81 | UserZoom | https://www.usertesting.com/platform/userzoom | tool | tool noted | Duplicate of row 22 (UserZoom). |
| 82 | Userlytics | https://www.userlytics.com/ | tool | tool noted | Userlytics: remote moderated and unmoderated testing with a panel. |
| 83 | Userfeel | https://www.userfeel.com/ | tool | tool noted | Userfeel: pay-per-test think-aloud videos. |
| 84 | Information Architecture and UX Design: The Integration of Information Spaces | https://link.springer.com/book/10.1007/978-3-031-72138-0 | book | summarized from description | Ding, Lin and Zarro, Springer 2025 edition (title from list); page redirects to a login, so summarized from the list description. |
| 85 | Information Architecture and UX Design: The Integration of Information Spaces | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 86 | Information Architecture: For the Web and Beyond | https://www.goodreads.com/book/show/25908623-information-architecture | book | summarized from description | Rosenfeld, Morville, Arango 4th ed.: organization, labeling, navigation, search systems (blurb) (IA1). |
| 87 | Information Architecture: For the Web and Beyond | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 88 | Information Architecture for the World Wide Web | https://www.goodreads.com/book/show/70132.Information_Architecture_for_the_World_Wide_Web | book | summarized from description | Earlier Morville/Rosenfeld edition; same four systems (blurb). |
| 89 | Information Architecture for the World Wide Web | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 90 | A Beginner's Guide To Information Architecture in UX [2023] | https://careerfoundry.com/en/blog/ux-design/a-beginners-guide-to-information-architecture/ | article | read | IA components, content inventory and audit, card sort, tree and click tests, Dan Brown's eight principles, four information needs (IA1 to IA3, IA8). |
| 91 | Information Architecture Guide for UX Architects & Designers | https://xd.adobe.com/ideas/process/information-architecture/information-ux-architect/ | article | read | IA process activities; specific labels ('About' not 'General Information'); cites Miller as a hard cap of seven, which misreads Miller (IA4, IA5). |
| 92 | The UX Process for Information Architecture | https://www.toptal.com/designers/ia/guide-to-information-architecture | article | blocked (403); summarized from description | Toptal IA process guide; merged into IA1, IA8. |
| 93 | Information Architecture. Basics for Designers. | https://uxplanet.org/information-architecture-basics-for-designers-b5d43df62e20 | article | blocked (403); summarized from description | Tubik IA basics; merged into IA1. |
| 94 | Information Architecture Design: A Step-By-Step Guide | https://uxplanet.org/information-architecture-design-a-step-by-step-guide-41dcd4405ee3 | article | blocked (403); summarized from description | Step-by-step IA design; merged into IA1, IA6, IA7. |
| 95 | A Beginner's Guide To Information Architecture | https://www.youtube.com/watch?v=Ij4WquJaRTc | video | summarized from description | README credits Toptal but the video is CareerFoundry's IA beginner guide (metadata only). |
| 96 | What Is Information Architecture? (UX Design Guide) | https://www.youtube.com/watch?v=OJLfjgVlwDo | video | summarized from description | CareerFoundry: what IA is (metadata only). |
| 97 | Information Architecture (IA) | https://www.youtube.com/playlist?list=PLJOFJ3Ok_idv3UGVmUktgRrVbl0X45RTY | video | summarized from description | NN/g IA playlist (metadata only); grounded via NN/g card sorting and tree testing articles. |
| 98 | Information Architecture & Sketching for UI/UX Projects | https://www.youtube.com/watch?v=CkQ3q0gewrQ | video | summarized from description | IA and sketching in a real project (metadata only). |
| 99 | About Face: The Essentials of Interaction Design | https://www.goodreads.com/book/show/18737922 | book | summarized from description | About Face: goal-directed design, personas, posture, excise (blurb; overlaps PLAN-4.1 H4 to H6). |
| 100 | About Face: The Essentials of Interaction Design | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 101 | Seductive Interaction Design: Creating Playful, Fun, and Effective User Experiences (Voice | https://www.peachpit.com/store/seductive-interaction-design-creating-playful-fun-and-9780321725523 | book | summarized from description | Anderson 2011: gradual engagement, defaults, playfulness, game mechanics (publisher TOC) (IX9). |
| 102 | Seductive Interaction Design: Creating Playful, Fun, and Effective User Experiences (Voice | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 103 | Interaction Design: Beyond Human-Computer Interaction | https://www.id-book.com/ | book | read (companion site) | Preece, Sharp, Rogers 6th ed.: 16 chapters from conceptual models to evaluation (site read). |
| 104 | Interaction Design: Beyond Human-Computer Interaction | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 105 | What is Interaction Design? | https://ixdf.org/literature/article/what-is-interaction-design | article | read | Five dimensions of interaction design and the questions designers ask (IX1, IX5). |
| 106 | What is Interaction Design? | https://www.uxpin.com/studio/blog/interaction-design-its-origin-and-principles/ | article | read | Norman-derived IxD principles and a checklist covering inputs, errors, feedback timing, target spacing (IX2 to IX4). |
| 107 | What Is Interaction Design in UX Development? | https://www.indeed.com/career-advice/career-development/what-is-interaction-design | article | blocked (403); summarized from description | Career-site explainer of interaction design; no unique lesson. |
| 108 | Basics of Interaction Design | https://www.youtube.com/watch?v=U7rS_2ch_Ps | video | summarized from description | README credits CareerFoundry but the video is IxDF's interaction design basics (metadata only). |
| 109 | What is Interaction Design | https://www.youtube.com/watch?v=KWtWqbJSP5E | video | summarized from description | What is interaction design (metadata only). |
| 110 | User Experience Design vs Interaction Design | https://www.youtube.com/watch?v=UsV_UBkiKSk | video | summarized from description | UX design vs interaction design (metadata only). |
| 111 | What is Interaction Design? Learn Interaction Design in Product Design like a Pro! | https://www.youtube.com/watch?v=DlQ75eTM_AM | video | summarized from description | Interaction design in product design (metadata only). |
| 112 | Interaction Design and Tasks | https://www.youtube.com/watch?v=_vsbkvm1w4w | video | summarized from description | Udacity: interaction design and task analysis (metadata only) (IX10). |
| 113 | Microinteractions: Full Color Edition: Designing with Details | https://www.goodreads.com/book/show/17239285-microinteractions | book | summarized from description | Saffer 2013: trigger, rules, feedback, loops and modes; 'don't start from zero' (blurb and known content) (MI1, MI8). |
| 114 | Microinteractions: Full Color Edition: Designing with Details | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 115 | Designing Interface Animation: Improving the User Experience | https://www.goodreads.com/book/show/30826231-designing-interface-animation | book | summarized from description | Val Head: purposeful interface animation for feedback, orientation and attention (blurb) (MI9). |
| 116 | Designing Interface Animation: Improving the User Experience | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 117 | Better UX Through Microinteractions | https://www.toptal.com/designers/product-design/microinteractions-better-ux | article | blocked (403); summarized from description | Microinteractions for better UX; merged into MI1 to MI5. |
| 118 | 10 Micro-interactions Examples and How They Boost UX | https://www.vev.design/blog/micro-interaction-examples/ | article | read | Ten showcase sites; four-part microinteraction model; purpose over decoration (MI1, MI5). |
| 119 | Microinteractions in User Experience | https://www.nngroup.com/articles/microinteractions/ | article | read | NN/g: trigger and feedback, feedback near the trigger, short-lived, distinct states, brand tone (MI2 to MI7). |
| 120 | How Micro Interactions have become an essential part of great products. | https://uxplanet.org/how-micro-interactions-have-become-an-essential-part-of-great-products-2ac8e02b5f2 | article | blocked (403); summarized from description | Why microinteractions matter; merged into MI5. |
| 121 | Micro-interactions: why, when and how to use them to improve the user experience | https://uxdesign.cc/micro-interactions-why-when-and-how-to-use-them-to-boost-the-ux-17094b3baaa0 | article | blocked (403); summarized from description | When and how to use microinteractions; merged into MI5. |
| 122 | Creating meaningful micro-interactions | https://uxplanet.org/creating-meaningful-micro-interactions-99cbde1fbee7 | article | blocked (403); summarized from description | Meaningful microinteractions; merged into MI5. |
| 123 | Micro-interactions in Figma under 9 mins-UI Animation Series: 09 | https://www.youtube.com/watch?v=l0EkLsZiWUg | video | summarized from description | Figma microinteraction tutorial (metadata only). |
| 124 | Awesome Micro Animations With Figma Tutorial | https://www.youtube.com/watch?v=0YIovQXnwBY | video | summarized from description | Video exists but has embedding disabled; title not retrievable; Figma micro-animation tutorial per list. |
| 125 | How to create complex micro interactions in Figma! | https://www.youtube.com/watch?v=moLF7t3HwYk | video | summarized from description | Complex Figma microinteractions (metadata only). |
| 126 | UI Animation Series in Figma | https://www.youtube.com/playlist?list=PLtU8M9giqjPuObPhJrS6z54hMEZRZfws3 | video | summarized from description | Figma UI animation playlist (metadata only). |
| 127 | Designing UX: Prototyping: Because Modern Design is Never Static | https://www.goodreads.com/book/show/43077265-designing-ux | book | summarized from description | Designing UX: Prototyping (SitePoint): prototyping as a continuous practice (list description). |
| 128 | Designing UX: Prototyping: Because Modern Design is Never Static | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 129 | How to Prototype: The Rapid Prototyping Process | https://www.uxpin.com/studio/ebooks/guide-to-prototyping/ | book (vendor ebook) | read (landing page) | UXPin ebook landing page: 'prototype only what you need'; 50% and 80% efficiency claims are unsourced (PR6, PR14). |
| 130 | How to Prototype: The Rapid Prototyping Process | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 131 | An Introduction to Prototyping in UX Design | https://medium.com/design-bootcamp/an-introduction-to-prototyping-in-ux-design-e19455eccb5e | article | blocked (403); summarized from description | Intro to prototyping; merged into PR1, PR2. |
| 132 | Guide to prototyping in Figma | https://help.figma.com/hc/en-us/articles/360040314193-Guide-to-prototyping-in-Figma | article | read | Figma prototyping model: flows, starting points, connections, overlays, durations 1 to 10000 ms. |
| 133 | 5 Common Low-Fidelity Prototypes and Their Best Practices | https://ixdf.org/literature/article/prototyping-learn-eight-common-methods-and-best-practices | article | read | Low-fi methods: sketch, paper, Lego, wireframe, Wizard of Oz; wireframe rules; dry-run before testing (PR2, PR4, R6). |
| 134 | Perfect Your UX Design Process: A Guide to Prototype Design | https://www.toptal.com/designers/prototype/guide-to-prototype-design | article | blocked (403); summarized from description | Prototype design guide; merged into PR1, PR2. |
| 135 | Figma Tutorial: Prototyping in Figma | https://www.youtube.com/watch?v=iBkXf6u8htI | video | dead | Unavailable: oEmbed 403 and no thumbnail (private or removed). |
| 136 | What is prototyping? | https://www.youtube.com/watch?v=_1bOaNSy5XY | video | summarized from description | Nesta: what prototyping is (metadata only). |
| 137 | Figma Tutorial: Prototyping & Transitions | https://www.youtube.com/watch?v=-d6zNGeF59M | video | summarized from description | Figma official: prototyping and transitions (metadata only). |
| 138 | Wireframing essentials : An Introduction to User Experience Design | https://www.goodreads.com/book/show/20718118-wireframing-essentials | book | summarized from description | Hamm, Wireframing Essentials (Packt 2014) (blurb). |
| 139 | Wireframing essentials : An Introduction to User Experience Design | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 140 | What Is A Wireframe? Your Best Guide | https://careerfoundry.com/en/blog/ux-design/what-is-a-wireframe-guide/ | article | read | Low, mid, high fidelity; grayscale; mobile one to two columns; polish suppresses honest feedback (PR3, PR5). |
| 141 | What is wireframing | https://www.experienceux.co.uk/faqs/what-is-wireframing/ | article | read | Wireframes settle global and secondary navigation terms and get tested before visual design (PR13). |
| 142 | What Are Wireframes? | https://balsamiq.com/blog/what-are-wireframes/ | article | read | Balsamiq: five wireframing steps; real headlines and CTAs instead of lorem ipsum (PR4). |
| 143 | Low-Fidelity Prototypes | https://tillerdigital.com/glossary/low-fidelity/ | article | read | Thin glossary entry: low-fi formats and benefits, no drawbacks or data. |
| 144 | Prototyping vs Wireframing: What's The Difference? | https://tillerdigital.com/glossary/wireframing/ | article | read | Thin glossary entry on wireframing only; title promises a comparison the page does not make. |
| 145 | Wireframing: Low Fidelity vs. High Fidelity | https://www.youtube.com/watch?v=J3FXDVe-6ws | video | summarized from description | Low vs high fidelity wireframes (metadata only). |
| 146 | Build Wireframes and Low-Fidelity Prototypes | https://www.youtube.com/watch?v=wJ3vof9Er5c | video | summarized from description | Re-upload of the Google course 3 content (metadata only). |
| 147 | Free Figma Tutorial: Designing Wireframes with Figma | https://www.youtube.com/watch?v=6t_dYhXyYjI | video | dead | Unavailable: oEmbed 403 and no thumbnail (private or removed). |
| 148 | Build Wireframes and Low-Fidelity Prototypes | https://www.coursera.org/learn/wireframes-low-fidelity-prototypes | course | read (syllabus page) | Google UX certificate course 3: storyboards, paper and Figma wireframes, low-fi prototypes, deceptive patterns (PR12). |
| 149 | Prototyping for Designers: Developing the Best Digital and Physical Products | https://www.goodreads.com/book/show/30014108-prototyping-for-designers | book | summarized from description | McElroy, Prototyping for Designers (O'Reilly 2017) (blurb). |
| 150 | Prototyping for Designers: Developing the Best Digital and Physical Products | (unofficial mirror, link withheld) | book (file mirror) | out of scope | Unofficial download mirror of a paid book; not opened (see the book's own row). |
| 151 | High-fidelity prototyping: What, When, Why and How? | https://blog.prototypr.io/high-fidelity-prototyping-what-when-why-and-how-f5bbde6a7fd4 | article | blocked (403); summarized from description | Hi-fi prototyping what/when/why; merged into PR2. |
| 152 | What is a high-fidelity prototype? | https://www.educative.io/answers/what-is-a-high-fidelity-prototype | article | read | Hi-fi prototype traits; users hesitate to suggest changes to polished work (PR3). |
| 153 | High-Fidelity Prototype: Why & When to Create Them | https://www.locofy.ai/blog/high-fidelity-prototype | article | read | When to go hi-fi; poor hi-fi leaves developers guessing; live coded prototypes cover all breakpoints (PR2, PR10, PR11). |
| 154 | Low-fidelity vs. High-fidelity Design Prototypes (and when to use which) | https://www.netsolutions.com/insights/low-fidelity-vs-high-fidelity-prototypes/ | article | read | Fidelity as three dimensions (visual, content, interactivity); decision rules for low vs high (PR1, PR2). |
| 155 | What are High Fidelity Prototypes?Types and Examples. | https://www.youtube.com/watch?v=O3FyvQq068U | video | summarized from description | Types of hi-fi prototypes (metadata only). |
| 156 | High-Fidelity Prototyping Demand is GROWING! (Don't Miss Out) | https://www.youtube.com/watch?v=cbhxy4OOReU | video | summarized from description | Market-demand video on hi-fi prototyping; no method content expected (metadata only). |
| 157 | Food App Design: UX/UI ( Wireframe, Prototype, Export) | https://www.youtube.com/watch?v=195RY7jCuZg | video | summarized from description | Food app wireframe-to-prototype walkthrough (metadata only). |
| 158 | Figma Mobile App Design Tutorial | https://www.youtube.com/watch?v=PeGfX7W1mJk | video | summarized from description | Figma mobile app design tutorial (metadata only). |
