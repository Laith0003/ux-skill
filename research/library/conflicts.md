# Conflicts between sources, and how each was resolved

Three clusters, each written separately: research and process, visual and system, interaction and content. Source codes (B01 to B96) refer to books listed in ACKNOWLEDGEMENTS.md.

<!-- cluster A: research and process -->

# Conflicts: cluster A (research and process)

Where books disagree, and how the rules in research/library/sources.md settle it. Rule numbers: 1 standard, 2 evidence, 3 authority, 4 newer on technology, 5 agreement, 6 newer edition. Ids are stable (A1, A2, ...). Duplicates found in more than one tag group were merged into one entry.


## Research methods, personas, journey mapping

### A1. Questionnaire item polarity

- Question: should questionnaire items alternate positive and negative wording?
- Side A (alternate polarity so people read carefully): B57 p.101 (t2).
- Side B (keep a consistent positive tone; mixing causes misreading and miscoding in about 11 percent of datasets without reducing bias): B94 p.223-227 (t1, measured).
- Resolution: keep item tone consistent. Side B is backed by measured data and a higher tier.
- Rule: 2

### A2. Rating scale points

- Question: how many response options should an agreement, satisfaction or task rating scale have, and should it keep a neutral midpoint?
- Side A (short scales, at most 5 options; most Likert use 3 or 5): B57 p.99, 101 (t2); B03 p.331, 355 (t1).
- Side B (7 points for satisfaction, difficulty and confidence; reliability rises to about 7 steps and levels off by 11; 7, 11 and 0 to 100 scales are about equally reliable): B94 p.205 (t1, measured); B02 p.324 (t1); B28 p.235-236 (t1); B14 p.164 (t1); B32 p.110-111 (t2); B58 p.506 (t2).
- Resolution: every side keeps an odd count with a neutral middle. Use 5 points as the floor for quick agreement items and task ratings, 7 where finer discrimination matters, up to 11 for fine judgments. Never change a standardized instrument's scale (SUS stays 5 points). Side B carries the measured reliability data.
- Rule: 2 (point count), 5 (odd scale with a midpoint, agreed by all).

### A3. Field research team size

- Question: how many researchers should attend a field interview or visit?
- Side A (two at most: one asks, one observes; three or more changes the dynamic): B64 p.140-143 (t1); B30 p.138-139 (t1, 2024); B40 p.38 (t3); B67 p.42-45 (t2); B58 p.270-271 (t2); B26 p.80 (t1).
- Side B (a field visit team of 2 to 8, most often 3 or 4): B20 p.135 (t1, 2012).
- Resolution: two researchers per session. Tiers are equal, so agreement decides and five books back Side A.
- Rule: 5

### A4. Interview length

- Question: how long should a research interview run?
- Side A (about one hour is enough; stakeholder interviews need no more): B26 p.69, 75, 80 (t1); B40 p.39 (t3).
- Side B (1.5 to 2 hours for contextual or on-site interviews): B02 p.452 (t1); B64 p.142 (t1); B58 p.242, 262 (t2); B20 p.136 (t1, a couple of hours maximum).
- Resolution: both stand by context. Desk or remote interviews about one hour; in-context visits up to 2 hours, never longer. Side B has more agreement for field visits.
- Rule: 5

### A5. Focus group size

- Question: how many participants per focus group?
- Side A (6 to 8, about 4 for depth, fewer than 8): B03 p.164, 169 (t1); B69 p.177 (t1); B55 p.90 (t1).
- Side B (8 to 12, or up to 12): B46 p.134 (t1); B06 p.100 (t2); B91 p.126 (t2, 3 to 12).
- Resolution: default 6 to 8; treat 12 as a hard ceiling. Tiers tie; three t1 books agree on Side A against one t1 on Side B.
- Rule: 5

### A6. Card sort deck size

- Question: how many cards should a card sort use?
- Side A (20 to 25 cards are usually sufficient): B93 p.365 (t1, 2015).
- Side B (about 50 topics, at most 100): B46 p.136-137 (t1, 2007).
- Resolution: no rule picks a winner (equal tier, no measured data on deck size, not technology dependent, no extra agreement). Use 20 to 50 cards by default and never exceed 100; size to the content being organized.
- Rule: 3 (tie, unresolved by authority; context decides)

### A7. Screener length

- Question: how many questions should a recruitment screener have?
- Side A (10 to 15 typical, about 20 maximum, under 5 if prescreened): B03 p.123 (t1).
- Side B (10 to 30 for interviews or tests): B17 p.51-52 (t3).
- Resolution: cap screeners at about 20 questions. The t1 source outranks the t3 source.
- Rule: 3

### A8. Where surveys sit in the sequence

- Question: do surveys come before or after qualitative work?
- Side A (start broad: surveys tell you whom to recruit before field visits): B03 p.73 (t1).
- Side B (surveys validate and size what qualitative work found; they do not discover needs): B27 p.72-75 (t2); B67 p.41-42 (t2); B30 p.47 (t1).
- Resolution: compatible once scoped. A survey may come first to size and locate an audience, but never to discover needs or motives; needs come from qualitative work, then a survey sizes them.
- Rule: 5

### A9. Over-recruitment buffer

- Question: how many extra participants should be booked for no-shows?
- Side A (book about 20 percent extra, for example 12 recruits to seat 10): B28 p.179 (t1, 2008).
- Side B (roughly one in four booked participants never arrives): B03 p.136-137 (t1, 2012, observed rate).
- Resolution: plan a buffer of 20 to 25 percent, leaning to 25 for cold recruits, or add floaters. The observed rate is the stronger evidence.
- Rule: 2

### A10. Typical, extreme or mainstream participants

- Question: whom should discovery research and design focus on?
- Side A (seek extreme, boundary and lead users; people with the most difficulty reveal needs that help everyone): B69 p.172, 213 (t1); B72 p.62, 302, 318 (t2); B30 p.53, 103 (t1).
- Side B (design for mainstream users, not experts or early adopters; edge cases must not drive design): B06 p.69-70 (t2); B01 p.6 (t3, 2003).
- Resolution: recruit extreme and boundary users for discovery and inclusive evaluation; let the primary persona set the design focus. The 2003 edge-case warning is superseded by the 4e position that the most constrained user is often the best primary (B26 p.117-119).
- Rule: 3 and 6

### A11. Edge cases in the persona model (edition conflict)

- Question: may constrained or edge users drive persona design?
- Side A (do not design around edge cases; handle them in code only): B01 p.6 (t3, 2003).
- Side B (the most constrained user often serves the bulk of the market and can be the primary): B26 p.117-119 (t1, 2014).
- Resolution: the 4th edition replaces the 2003 chapter. Rare operations still do not drive layout, but a constrained user can be the primary persona.
- Rule: 6

### A12. Secondary persona limit (edition conflict)

- Question: how many secondary personas before scope is too large?
- Side A (0 to 2 per interface): B01 p.20 (t3, 2003).
- Side B (more than 3 or 4 suggests the scope is too large): B26 p.119 (t1, 2014).
- Resolution: use the 4e threshold: warn above 3, fail above 4.
- Rule: 6

### A13. Primary personas: one or several

- Question: how many primary personas should there be?
- Side A (exactly one primary per interface): B26 p.117-119 (t1); B03 p.516 (t1).
- Side B (pick 2 or 3 primary personas; 1 or 2 priority user types): B17 p.164 (t3); B35 p.32, 70 (t3).
- Resolution: one primary per interface; a product with several interfaces may have one primary each, which reconciles Side B's product-level count.
- Rule: 3

### A14. Minimum cast size

- Question: can a cast have fewer than three personas?
- Side A (fewer than 3 is unrealistic; 3 to 8): B23 p.347 (t2); B38 p.86-87 (t3, 3 to 6).
- Side B (1 to 3 per project): B60 p.210-211 (t1); B50 p.19 (t2, casts of two to six).
- Resolution: no fixed floor. A focused product may need one to three; most casts land between 2 and 6. The t1 source outranks the t2 and t3 floor.
- Rule: 3

### A15. Demographics in personas

- Question: should personas be defined by age, gender, income and location?
- Side A (describe the audience through demographics such as age, gender, place, job, income and household, matching known population shares): B25 p.37-38 (t3); B38 p.87-88 (t3); B23 p.349 (t2).
- Side B (define by behavior, goals and needs; demographics do not predict skill and import stereotypes): B26 p.121 (t1); B03 p.498, 503 (t1); B34 p.61-62 (t1); B02 p.453-454 (t1); B09 p.76-77 (t2); B35 p.62-66 (t3).
- Resolution: behavior defines the persona; demographics are optional context and may reflect real distribution, but never the basis of segmentation.
- Rule: 3

### A16. Proto-personas

- Question: may a team start from assumption-based personas?
- Side A (yes: sketch proto-personas in hours, then validate in the field): B34 p.59-63 (t1); B64 p.111-113 (t1).
- Side B (do not invent personas without data; assumptive personas carry little authority and tend to stay unvalidated): B23 p.347-349 (t2); B58 p.262 (t2); B50 p.80, 125-126 (t2).
- Resolution: allowed only as a labeled hypothesis with a validation step. Side A is higher tier; Side B's warning becomes the labeling requirement.
- Rule: 3

### A17. Goals inside the persona description

- Question: do goals belong in the persona or in the scenarios?
- Side A (leave goals and present product use out of the persona text, so one persona can be placed in many scenarios): B50 p.92, 172 (t2).
- Side B (goals are what make a user model a persona; give each one 3 to 5 end goals): B26 p.116, 121 (t1); B03 p.498, 503 (t1).
- Resolution: keep product-independent goals on the persona; move product-specific tasks and usage into scenarios.
- Rule: 3

### A18. Narrative prose versus explicit short lists

- Question: should a persona be written as narrative or as explicit behaviors?
- Side A (third-person narrative is remembered better than bullets): B50 p.75, 110 (t2); B26 p.120 (t1, narrative of 1 to 2 pages).
- Side B (half-page personas stating behaviors directly beat narratives with irrelevant detail): B09 p.76 (t2); B38 p.87-88 (t3).
- Resolution: a short third-person narrative is allowed, capped at about one page, with every sentence tied to data; explicit keys sit beside it in the template.
- Rule: 3

### A19. Photos, sketches and posters

- Question: how should a persona be visualized?
- Side A (use a photo that signals context and attitude; print as A3 posters): B01 p.19 (t3); B38 p.87 (t3); B17 p.164 (t3).
- Side B (realistic photos aid recall, but stock images feel fake and single images or quotes measurably skew readings; keep personas as editable sketches, not glossy posters): B50 p.76-77, 155-160 (t2, studies); B30 p.204-209 (t1).
- Resolution: prefer editable sketches or carefully chosen realistic photos; avoid stock imagery and polished posters that freeze the persona.
- Rule: 2 and 3

### A20. Related or unrelated personas

- Question: should personas in a cast be socially linked?
- Side A (keep them unrelated unless research shows the link or a shared workflow must be shown): B01 p.17-18 (t3).
- Side B (a persona family across generations and abilities sparks concrete inclusive ideas): B69 p.62, 163 (t1).
- Resolution: design personas stay unrelated by default; a persona family is a valid ideation device in inclusive workshops.
- Rule: 3

### A21. Persona refresh cadence

- Question: how often should personas be revised?
- Side A (revisit after every conversation or study; living documents): B34 p.61, 64 (t1).
- Side B (revise about every second year; check every 1 to 2 years): B50 p.22, 166 (t2).
- Resolution: update continuously as research arrives, with a full review at least every two years as the floor.
- Rule: 3

### A22. Preference questions

- Question: should research ask people which option they prefer?
- Side A (ask preference questions to learn trade-offs experts cannot weigh): B89 p.283-284, 293-294 (t1, 1994).
- Side B (people confabulate reasons for choices; observe behavior instead of asking preferences): B30 p.19-21 (t1, 2024, measured position effect).
- Resolution: use preference questions only to rank trade-offs and never trust stated reasons; pair with behavioral evidence. Side B carries measured evidence.
- Rule: 2

### A23. Affinity group size

- Question: how many notes may sit in one affinity group?
- Side A (at most 5 notes per group): B06 p.106-107 (t2).
- Side B (start groups at 4 to 5 and let them grow to 12 to 15 before splitting): B20 p.180-188 (t1).
- Resolution: groups may grow to 12 to 15 notes; split larger ones and add a label level.
- Rule: 3


## Usability testing, prototyping, wireframing

### A24. Does a five-person round find about 85 percent of usability problems?

- Side A: five users find about 85 percent (75 to 85) of problems, so five is enough. Sources: B81 p.202, 256; B74 p.106; B46 p.828-829; B29 p.68; B06 p.50; B49 p.23
- Side B: the 85 percent figure holds only when each problem affects about 31 percent of users; measured problem rates run 0.03 to 0.46 and averaged 0.04 on websites, where five users found about a third. Five users reliably find problems that hit one user in three, not 85 percent of all problems. Sources: B94 p.163-167, 179-184; B30 p.103-108; B20 p.565-571
- Resolution: Side B. It is backed by measured discovery rates across many studies and by the binomial model itself, while Side A repeats the headline figure without the condition. Keep "about five per round" as a planning default for iterative formative work, but state the condition (common problems only) and size studies aimed at rare or critical problems with the discovery formula.
- Rule: 2

### A25. Round size for formative usability tests: fewer than five, five, or eight?

- Question: how many participants should one round of a formative usability test have?
- Side A (never four or fewer, start at five): B81 p.202, 256 (t1); B46 p.828-829 (t1); B06 p.212, 218 (t2); B87 p.19 (t3); B17 p.39 (t3); B89 p.58-59 (t1, discovery-rate data).
- Side B (2 to 4 per round is fine when rounds repeat on a fixed schedule, including RITE rounds of 1 to 4 with fixes between): B34 p.123-124 (t1); B77 p.125-130 (t1); B02 p.577 (t1); B20 p.520 (t1); B12 p.388-398 (t2); B57 p.98 (t2).
- Side C (four or five per cell find about 80 percent, but eight is the preferred minimum): B28 p.110, 164 (t1).
- Resolution: the discovery formula decides; the answer depends on the per-user problem rate and on whether rounds repeat. A standalone single round: 5 or more per distinct user group, about 8 when only one round will ever run or the problem rate is low. A recurring or RITE series: 2 to 4 per round is acceptable while the series continues and its cumulative total reaches the discovery goal. Side B has the most tier 1 agreement.
- Rule: 2 (discovery math), 5 (agreement).

### A26. How many participants does quantitative or comparative work need?

- Question: is there a fixed minimum sample (20 per group, 30, 40 in total) for statistics, or does the number come from a calculation?
- Side A (fixed floors): about 20 per group for statistics or A/B comparisons: B87 p.19 (t3); B06 p.211-212, 218 (t2); B49 p.23 (t2); B14 p.161 (t1). Inferential comparisons need 10 to 12 per condition and 40 or more in total: B28 p.62, 110, 305 (t1). Picking a conversion winner needs thousands: B74 p.33 (t3); B57 p.110-111 (t2). Scores on 25 to 30 data points are noise: B56 p.13, 115-116 (t2).
- Side B (computed): small samples support valid intervals and tests, the 30-user rule has no basis, and 2 to 10 users can give usable results with small-sample methods; within-subjects designs need far fewer participants than between-subjects (15 versus 52 in one worked example); SUS comparisons were fully correct at 12 users; the right n comes from the margin of error or the effect size and power. Sources: B94 p.27, 80, 133-134, 228-229, 263-265 (t1, coverage simulations); B02 p.599-600 (t1, at least 15 per condition); B11 p.61, 66 (t2).
- Resolution: Side B. No fixed head count is correct. Compute n from the design (within or between subjects), the metric and the precision needed. Side A is right that small samples only detect large effects, so state what the chosen n can detect. When no calculation is done, about 20 per group is a labeled default, never a floor that blocks a study.
- Rule: 2.

### A27. Concurrent think-aloud: always, or chosen per study?

- Side A: ask every participant to think aloud and keep them narrating; prompt a silent participant within seconds. Sources: B77 p.133, 137-139; B03 p.32-33; B81 p.206-214; B57 p.118-119; B06 p.222, 225
- Side B: concurrent think-aloud adds load and slows people, so drop it for timed tasks, very short tasks and eye tracking; use retrospective review, silent completion, post-task interviews or co-discovery pairs when narration is unreliable (fatigue, disability, cultures where criticism of the facilitator is avoided). Sources: B28 p.92, 118, 243; B17 p.75-76; B06 p.224; B32 p.155-156; B49 p.281-282; B08 p.141, 230-231; B79 p.228-229
- Resolution: concurrent think-aloud is the default for formative, untimed tests; it must not be combined with time-on-task or eye tracking, and an alternative protocol is chosen for the cases in Side B. Both sides are tier 1; Side B carries the specific, observed effect on time and attention and more independent books.
- Rule: 5 (tier 1 on both sides, so rule 3 does not decide; Side B has wider agreement)

### A28. When a participant goes quiet or gets stuck, prompt fast or wait?

- Side A: prompt a silent think-aloud participant after about 3 to 5 seconds. Sources: B06 p.222, 225
- Side B: when someone stalls, count silently to 20 or 30 before prompting or moving on, and let frustration run while they still try. Sources: B28 p.93-94, 244, 249; B27 p.65
- Resolution: the two address different moments. A participant who is working but has stopped narrating gets a quick neutral nudge to keep talking; a participant who has stopped making progress gets 20 to 30 seconds of silence before any hint. Where they truly overlap, the tier 1 source governs: do not rescue early.
- Rule: 3

### A29. Are friends, family and loose recruits acceptable participants?

- Side A: loose recruiting, judged with some allowance, is fine because the worst problems trip up nearly everyone, so never hold a test back waiting for ideal recruits; a friends-and-family round of 5 or 6 people resembling the audience is a valid quick test. Sources: B77 p.131-132; B03 p.31
- Side B: never test with friends or family; acquaintances soften feedback; recruit screened strangers, ideally people about to do the real job. Sources: B81 p.255-256; B96 p.114-116; B40 p.46-47; B87 p.19-20
- Resolution: Side B as the default, Side A as a narrow exception. Authority ties (tier 1 on both sides) and neither side has a study, so rules 2 and 3 do not separate them and agreement decides. More independent books require representative, screened recruits; a loose round is acceptable only as a fast check for problems that would hit almost anyone, never as the evidence for a decision about the target audience, and never with people who work in design, UX or marketing.
- Rule: 5

### A30. One participant at a time, or pairs and groups?

- Side A: one participant per session; never focus groups. Sources: B96 p.126; B81 p.255-256
- Side B: pairs thinking aloud surface reasoning; pairing two people of the same social standing helps in cultures where a single participant avoids open criticism. Sources: B79 p.228-229; B08 p.230-231
- Resolution: individual sessions by default; deliberate pairs (co-discovery) are a valid variant, focus groups are not a usability test. Both sides agree groups of several people distort behavior.
- Rule: 3 (the tier 1 sources on both sides agree on rejecting groups; the pair variant comes from a tier 1 source)

### A31. How long can a session run?

- Side A: 60 minutes or less; value drops quickly after an hour; some participants degrade after about 30 minutes. Sources: B23 p.171; B85 p.275; B06 p.214; B34 p.123-124
- Side B: 90 minutes to 2 hours is workable; users stay effective about 90 minutes; older or disabled participants can go 1.5 to 2 hours with breaks. Sources: B03 p.295-296; B58 p.285; B20 p.554; B69 p.182; B32 p.165
- Resolution: default to 60 minutes with about 40 to 45 minutes of tasks; extend to 90 only with a break and a reason; never exceed 2 hours. Immersive (VR) sessions stay near 30 minutes. Agreement is wide on the 60-minute default and on the 2-hour ceiling.
- Rule: 5

### A32. What fidelity should a test prototype have?

- Side A: low fidelity (paper, grayscale wireframes) for testing; polish draws comments on looks, makes testers polite and the team reluctant to change. Sources: B20 p.431, 441-442; B27 p.159-160, 182-183; B57 p.107-108; B02 p.477, 480; B26 p.133, 150, 156-157; B72 p.115, 120; B35 p.278-281
- Side B: a realistic facade ("just enough" quality, built in a day) gets genuine reactions; flimsy paper breaks the illusion and invites feedback; high-fidelity versions are what go in front of users and stakeholders. Sources: B81 p.172-177; B75 p.213-214; B95 p.102-103
- Resolution: a measured comparison found fidelity did not change the problems found (B46 p.806), so low fidelity is sufficient for finding problems and cheaper to change. Raise realism in content and interaction (real copy, realistic data, working links) before raising visual polish; keep visual polish low until structure is settled, except for sign-off comps and visual-design questions.
- Rule: 2

### A33. Paper prototypes or interactive wireframes for user tests?

- Side A: paper works for tests; it lowers participant anxiety, reveals mental models when users relabel or add elements, and finds severe problems. Sources: B06 p.185-187, 206-207; B38 p.100-101; B28 p.337-339; B20 p.441-442; B87 p.22-23
- Side B: prefer interactive wireframes; paper changes how people read, cannot show states or animation, makes inspectors miss "something missing" problems, and should be used for tests only when the product is paper. Sources: B27 p.161-165; B81 p.183-184; B89 p.82; B87 p.24-25
- Resolution: the fidelity study (B46 p.806) found equal problem counts, but paper sessions took about 30 percent longer and most participants preferred the computer version. Use paper for concept and mental-model exploration early; switch to linked digital wireframes for flows, states, mobile gestures and anything timed.
- Rule: 2

### A34. Are dead-end links acceptable in a prototype?

- Side A: dead-end buttons are acceptable in a one-day prototype. Sources: B81 p.156-163
- Side B: decide how out-of-scope links behave and avoid jarring dead ends; give a "not yet implemented" response, which also captures what the user expected; add decoy controls so tasks are not artificially easy. Sources: B74 p.48-49; B28 p.68-69; B20 p.450-451
- Resolution: Side B. Two tier 1 sources and one more agree; every out-of-scope control should respond with a labeled placeholder rather than doing nothing.
- Rule: 3

### A35. Sketch only the happy path, or every state?

- Side A: early wireframes cover only the most probable main path, with edge and error states deferred. Sources: B96 p.94
- Side B: sketch every state of every interactive element, including errors and misuse; annotate error messages, popups and defaults; prototypes hide states, so document them. Sources: B27 p.105-106; B78 p.103-105; B62 p.69
- Resolution: sequence, not contradiction. Happy path only during divergent sketching; every state documented before a wireframe is tested in detail or handed to engineering. Side B has more agreeing sources for the hand-off point.
- Rule: 5

### A36. Should moderators rotate the order of tasks and designs?

- Side A: order tasks from easiest to hardest so participants settle in, and run the main task early. Sources: B03 p.31; B17 p.67-68
- Side B: rotate or counterbalance task and design order to cancel learning effects. Sources: B17 p.69; B27 p.61, 77, 157; B94 p.80, 133-134; B41 p.187; B85 p.181-182; B12 p.396
- Resolution: fix a short easy warm-up task first, then counterbalance the remaining tasks and always counterbalance compared designs. The learning effect behind Side B is measured in the within-subjects literature.
- Rule: 2


## Metrics and statistics, design sprints, lean and agile

### A37. Mean, median or geometric mean for task time?

- Side A: report the median when outliers exist; median for skewed data. Sources: B28 p.289-292; B02 p.357; B03 p.378-380 (all t1).
- Side B: below about 25 users the geometric mean estimates typical time better than the median or mean; median above 25. Sources: B94 p.46-49, 53 (t1, measured comparison); B14 p.163 (t1).
- Resolution: geometric mean under n = 25, median at 25 or more; never the arithmetic mean alone for raw task times. Side B carries measured evidence; Side A's core point (do not trust the mean on skewed data) is kept.
- Rule: 2.

### A38. Top-box scores or raw rating means?

- Side A: report top-box (most favorable answer over all respondents) or top-two-box to counter acquiescence. Sources: B57 p.100 (t2); B58 p.506, 511 (t2).
- Side B: collapsing ratings loses information and sensitivity; one comparison lost significance. Sources: B94 p.69-70, 117 (t1, worked data).
- Resolution: compare designs on raw ratings; top-box may be shown as an extra reporting view only.
- Rule: 2 (and 3).

### A39. Survey sample size for a population of one million

- Side A: about 2,000 responses from a population of one million for a 5 point margin at 95 percent confidence. Sources: B03 p.368 (t1).
- Side B: about 384 to 385 for the same precision; the requirement barely grows above about 10,000. Sources: B94 p.139 (t1); B30 p.232, 271 (t1, 2024); B44 p.336-337 (t3).
- Resolution: Side B. It follows from the standard formula and three books agree; the larger figure only makes sense if it covers several analyzed subgroups, which Side A states separately (each subgroup needs a full sample).
- Rule: 2, then 5.

### A40. What survey response rate is normal?

- Side A: online surveys typically get 20 to 40 percent; under 20 percent is doubtful and 1 percent worthless. Sources: B03 p.372-373 (t1, 2012).
- Side B: web survey response is typically 1 percent or 0.1 percent; draw a random sample of about 1,500 and aim for 70 percent. Sources: B30 p.234 (t1, 2024).
- Resolution: both treat low response as bias. Response rates depend on the channel and era, so the newer figure describes open web surveys today; the shared rule is to invite a random sample and work for a high response rather than accept volume from a 1 percent return.
- Rule: 4.

### A41. Which alpha level for decisions?

- Side A: p < 0.05 is the convention, p < 0.01 stronger. Sources: B02 p.593 (t1).
- Side B: for product decisions alpha 0.10 or 0.20 (80 percent confidence) is defensible if overlooking a genuine gain hurts as much as shipping a false positive. Sources: B94 p.137, 268-270 (t1).
- Resolution: both stand in their context. Use 0.05 for publishable or high-stakes claims; for reversible product decisions choose alpha from the relative cost of Type I and Type II errors and declare it before collecting data.
- Rule: 2 (Side B argues from error costs; the convention is not evidence).

### A42. How to split A/B traffic?

- Side A: split 50/50 for a controlled test. Sources: B27 p.196, 201, 224 (t2).
- Side B: expose 1 to 10 percent of visitors, or the smallest share of traffic that still yields reliable numbers. Sources: B04 p.37-38 (t2); B79 p.225 (t1); B03 p.481-482 (t1).
- Resolution: different goals. 50/50 maximizes power for a given traffic level; small exposure limits harm from a risky change. Pick by risk and required sample, and compute duration from the sample-size formula.
- Rule: 3 (t1 sources favor limiting exposure when risk is unknown).

### A43. Satisfaction cut points on a 0 to 10 scale

- Side A: 1 to 4 bad, 5 to 7 neutral, 8 to 10 good. Sources: B61 p.149 (t2).
- Side B: on the recommend question 9 to 10 are promoters, 7 to 8 passives, 0 to 6 detractors. Sources: B94 p.33 (t1).
- Resolution: use each instrument's defined bands. The NPS bands apply only to the NPS question; a generic satisfaction scale may use meaning-based buckets.
- Rule: 3.

### A44. Severity scale design

- Side A: one 0 to 4 rating combining frequency, impact, persistence and market effect. Sources: B89 p.72, 74 (t1).
- Side B: separate severity 1 to 4 and frequency 1 to 4, added together. Sources: B28 p.299-301 (t1). A 0 to 3 scale by share of users affected. Sources: B89 p.294-295.
- Resolution: both require frequency as well as impact. Prefer the additive form (separate severity and frequency) because it keeps the two inputs auditable; average ratings across 3 or 4 raters either way.
- Rule: 2 (inter-rater data shows single combined judgments are unreliable).

### A45. Design sprint length and day length

- Side A: five days; shorter was exhausting and longer gave no more; 6 working hours a day, breaks every 60 to 90 minutes. Sources: B81 p.45-48, 96 (t1).
- Side B: can compress to three days (or a 3-hour ultra-compact version); 7-hour days with breaks every 80 to 120 minutes. Sources: B96 p.35-37, 41, 49 (t2).
- Resolution: default to five days of about six focused hours with breaks every 60 to 90 minutes; treat three days as the compressed floor and shorter formats as workshops, not sprints.
- Rule: 3.

### A46. Sprint team size

- Side A: seven or fewer. Sources: B81 p.12, 38 (t1). Studio teams 3 to 6. Sources: B09 p.116 (t2).
- Side B: a five-day sprint with about ten participants. Sources: B34 p.145-146 (t1).
- Resolution: cap the deciding core at seven and bring others in as expert interviews or split them into sketch groups of three to six. Two independent books agree on small groups.
- Rule: 5.

### A47. Should design work a sprint ahead of development?

- Side A: yes. Design sprint n+1 while evaluating n-1; tested designs must be ready when developers need them. Sources: B20 p.662-677 (t1); B85 p.38-39 (t2); B38 p.23 (t3); B11 p.155 (t2, 2025, one to two sprints ahead is common).
- Side B: a short lead (two to three days of design time raised at planning) rather than a separate track. Sources: B34 p.153 (t1).
- Resolution: keep design ahead of the story being built; the size of the lead (days or a sprint) depends on the team, but zero lead is not supported by any book. Four books agree on working ahead.
- Rule: 5.


## Critique and collaboration, design process, career and portfolio

### A48. Should critique include the fix?

- Question: does a critique or review propose solutions, or only analyze problems?
- Side A (keep fixes out): critique is analysis, and a group cannot evaluate and invent at the same moment, so park proposed solutions and extract the problem. Sources: B09 p.43, 131-132; B78 p.95-96.
- Side B (attach a fix): written reviews need concrete, reasoned "change X in Y" recommendations, and designers ignore problem reports with no redesign proposal. Sources: B89 p.109, 111; B20 p.634, 641-644; B58 p.455-456; B28 p.307-309.
- Resolution: both sides agree the problem must be stated in user terms on its own, which side B's tier 1 inspection source also requires. Live group critique sessions keep solutioning out; written findings carry a recommendation in a separate field after the problem statement. Side B wins for written reports because it has the tier 1 sources.
- Rule: 3.

### A49. Decide in the room, or after the session?

- Question: should a group session end with a decision?
- Side A (no decisions in critique): leave decisions for after the session so analysis is not rushed. Sources: B09 p.129-134.
- Side B (decide in the room): a named decider makes the call before people leave, using silent votes and supervotes; deferring invites reversal. Sources: B81 p.136-148; B96 p.92-93, 102.
- Resolution: these are different activities. Critique sessions analyze; a separate decision step (which may follow on the same day) decides with a named decider. For the decision step, side B wins.
- Rule: 3.

### A50. Equal voices versus extra votes for the boss

- Question: should senior people have more weight?
- Side A: neutralize the highest paid person's opinion; equality is a ground rule. Sources: B09 p.129-134; B96 p.56-58.
- Side B: give deciders visible extra votes or supervotes, because that reflects how decisions are really made. Sources: B96 p.92-93; B81 p.138-148.
- Resolution: equality applies while generating and critiquing ideas; open, explicit authority applies at the final decision. Both coexist in the same tier 1 sprint method.
- Rule: 3.

### A51. Merge the best parts, or pick one bet?

- Question: when two strong alternatives exist, combine them?
- Side A (expect a hybrid): test radically different alternatives; the winning design tends to combine the strongest elements of several. Sources: B28 p.76, 302-303.
- Side B (pick a bet): do not average rival ideas into a middle ground or make ideas vaguer to agree; choose one and keep the other in reserve. Sources: B96 p.102-103; B34 p.80-81.
- Resolution: side A's hybrid comes out of test evidence; side B warns against compromise made before evidence to avoid conflict. Before testing, pick a bet; after testing, merge parts the evidence supports.
- Rule: 2.

### A52. Group brainstorming or solo generation?

- Question: should teams brainstorm aloud together?
- Side A (group brainstorm with rules): brainstorm together without criticism, with a numeric target and time limit; brainstorm for hours to days. Sources: B71 p.70-72; B26 p.141-142.
- Side B (work alone together): individuals generating in parallel outperform shout-out group sessions, as a classic study found. Sources: B81 p.113, 129; B34 p.76-81.
- Resolution: side B is study-backed. Generate individually first (side A's sticky notes already lean this way), then share and build.
- Rule: 2.

### A53. Praise sandwich and positive ratios

- Question: should criticism be cushioned with praise?
- Side A: skip the feedback sandwich; token praise is forgotten and signals bad news. Sources: B09 p.171-172.
- Side B: frame feedback positively ("what went well, even better if"); strong teams were observed giving over 5 positive remarks for each critical one. Sources: B13 p.192-193, 200.
- Resolution: side B cites a single team-meeting ratio, not a design critique study, so rule 2 does not settle it; the tier 2 critique source outranks the tier 3 career source. Name genuine strengths as separate items and never use praise as a wrapper.
- Rule: 3.

### A54. How long should a research report be?

- Question: what length should findings take?
- Side A: a formal written report runs about 20 to 25 pages with a 1-page executive summary. Sources: B28 p.311-312.
- Side B: if readers must turn the page it is too long; nobody reads 35 pages; use one-page radiators, a summary email or 3-slide deck. Sources: B30 p.25; B06 p.254; B17 p.22; B03 p.553.
- Resolution: tier 1 sources sit on both sides, so agreement decides: lead with a one-page summary; any long report is optional reference behind it.
- Rule: 5.

### A55. Total length of highlight videos

- Question: how long should a findings video be?
- Side A: under 20 minutes total, clips 30 seconds to 3 minutes. Sources: B28 p.322-324.
- Side B: under 3 minutes for executives, or a showreel under 5 minutes with clips under 1 minute. Sources: B77 p.197; B17 p.166; B03 p.561-564.
- Resolution: for stakeholder viewing keep the reel under 3 to 5 minutes; longer compilations are working material for the team.
- Rule: 5.

### A56. Problem time versus solution time

- Question: how should time split between defining the problem and solving it?
- Side A: up to two-thirds of the time on the problem; one framing spends 55 of 60 minutes defining it; you cannot iterate your way to innovation. Sources: B29 p.29; B72 p.309; B30 p.50-52.
- Side B: give the solution step half or more of the available time. Sources: B25 p.26, 46, 54.
- Resolution: side B is scoped to timed interview exercises where the problem is handed over. For real projects side A holds, backed by the tier 1 source.
- Rule: 3.

### A57. Throwaway prototypes or production code?

- Question: should prototypes be discarded or built in production code?
- Side A: prototypes are disposable; make the least artifact that answers the question and throw it away. Sources: B85 p.57, 110; B34 p.170-171.
- Side B: designers writing production front-end code instead of throwaway prototypes gained over 50 percent efficiency; front-end prototypes on a shared grid became the app. Sources: B58 p.84; B87 p.37-38.
- Resolution: side B's figure is a single team's estimate, not a study. Throw away prototypes built to answer a question; move to production-grade code once the direction is settled.
- Rule: 3.

### A58. Fidelity for collaboration

- Question: rough or polished artifacts with stakeholders?
- Side A: keep collaborative artifacts low fidelity so non-designers contribute and feedback stays on flow. Sources: B34 p.72-73; B74 p.106, 128.
- Side B: stakeholders read mid or mixed fidelity best, clients expect to see their own brand, and developers need full fidelity with motion and specs. Sources: B85 p.51-52, 102.
- Resolution: low fidelity for working sessions and flow questions; raise fidelity for sign-off and handoff audiences.
- Rule: 3.

### A59. Brief length

- Question: one page or a substantial document?
- Side A: a creative brief fits one page. Sources: B05 p.48, 168-169; B09 p.82-83.
- Side B: briefs that worked were 500 to 1,500 words long, and writing one raised concept quality by about 20 percent. Sources: B72 p.40-43.
- Resolution: side B is backed by measured data. Write the full brief, then derive the one-page summary from it for meetings.
- Rule: 2.

### A60. Workshop size

- Question: how many people per workshop?
- Side A: 8 or fewer; Design Studio 5 to 8; sprint teams 4 to 5. Sources: B23 p.281, 300; B35 p.91; B34 p.76-81; B96 p.43-45.
- Side B: 6 to 12 participants, about 12 stakeholders in breakouts; innovation jams hold 20 to 30. Sources: B64 p.61, 212-213; B72 p.139.
- Resolution: size depends on the activity. Ideation and convergence stay at 8 or fewer; alignment and mapping can reach 12 by splitting into breakout groups.
- Rule: 3.

### A61. Weight of non-designer taste

- Question: how much should non-designer opinions on look and feel count?
- Side A: value non-designers' opinions because they see work as consumers do. Sources: B95 p.67-68.
- Side B: weigh stakeholders for domain knowledge, not taste, and ignore test color comments unless about 3 of 4 participants are strongly negative. Sources: B77 p.180; B74 p.201.
- Resolution: the tier 1 source wins. Treat taste remarks as signals to verify with users, not as direction.
- Rule: 3.

### A62. Pitching research to stakeholders

- Question: frame research around the stakeholder's solution or the problem?
- Side A: pitch research as validating the stakeholder's idea, then let the evidence shift opinion. Sources: B29 p.69.
- Side B: move stakeholders off their solution and onto the problem, how they know it exists, and how it is measured. Sources: B30 p.82-87.
- Resolution: the tier 1 source governs how research is scoped and run. Side A survives only as a way to open the conversation.
- Rule: 3.

### A63. Portfolio size

- Question: how many pieces?
- Side A: 15 to 20 pieces; 4 or 5 campaigns of 4 or 5 pieces. Sources: B05 p.146, 159.
- Side B: 1 to 3 relevant case studies for juniors, 1 to 2 pages per project, minutes of reviewer time. Sources: B29 p.210, 244; B30 p.326-327.
- Resolution: side A describes graphic and advertising books; for UX and product roles the tier 1 source sides with B.
- Rule: 3.

### A64. Portfolio format

- Question: website, PDF or physical book?
- Side A: host the portfolio on your own domain rather than sending attachments. Sources: B95 p.247-248.
- Side B: a modular PDF tailored per application. Sources: B29 p.233-240.
- Side C: a portable physical book plus a leave-behind. Sources: B84 p.49, 53-55, 82, 101.
- Resolution: hiring channels depend on technology, so newer sources win. Keep a site and a tailored PDF; a physical book is optional.
- Rule: 4.


<!-- cluster B: visual, system and platform -->

# conflicts: cluster B (visual, system and platform)

Each conflict names the question, both sides with their sources, the resolution, and the sources.md rule that settles it. Rule numbers: 1 standard beats books on compliance; 2 evidence beats authority; 3 authority beats count; 4 newer beats older on technology; 5 agreement raises confidence; 6 newer edition replaces older.

## Color

### 1. Does warm color always advance and cool color recede?
- Side A: yes, warm and saturated hues come forward, cool and dark ones recede; use it to order depth and attention. Sources: B70 p.46, 78; B92 p.79, 174; B76 p.186, 189; B53 p.312, 449
- Side B: warm and cool are relative and the advance and recede theory is contradictory in practice; the split is a convention. Sources: B90 p.85-87; B37 p.31; B70 p.45-46, 77-78 (background lightness reverses the order)
- Resolution: both sides include tier 1 sources, so authority ties. The one point every source agrees on is that the ground's lightness decides which colors come forward: on black the light hues advance, on white the dark ones do. Treat depth from color as relative and control it with lightness against the ground. A warm or cool label alone is a weak cue. Rules 3 and 5.

### 2. Are red, yellow and green acceptable for threshold coloring?
- Side A: red, yellow and green is the common threshold palette; keep the order consistent across charts. Sources: B24 p.238, 241; B35 p.264
- Side B: never separate states by red against green alone, because red-green deficiency is the most common kind. Sources: B46 p.726-727; B86 p.279, 284; B91 p.34-40; B80 p.111, 117; B58 p.111, 137, 299; B20 p.832-834
- Resolution: WCAG 1.4.1 decides. Threshold colors are acceptable only with a second cue, such as a label, icon, position or pattern. For diverging scales, prefer a hue pair that color-deficient readers can tell apart, such as blue against orange or red. Rules 1 and 5.

### 3. How many categorical colors may a chart use?
- Side A: up to six colors on statistical graphics, with four or five for reliable absolute identification. Sources: B46 p.193-194, 733-734, 746-747
- Side B: more than three colors in a chart is already a warning sign. Sources: B91 p.33
- Resolution: side A cites identification research. Side B rests on one reader's experience. Both sides agree that color must be redundant. The ceiling is six categories, with direct labels or patterns. Plan for four or five where readers must name a color without a legend. Rules 2 and 3.

### 4. Should light-on-dark text get a higher contrast target than dark-on-light?
- Side A: reported research gives different luminance ratios by polarity, about 10:1 for light on dark against about 6.5:1 for dark on light. Sources: B46 p.745
- Side B: one symmetric floor of 4.5:1 for body text and 3:1 for large text, whatever the polarity. Sources: B91 p.59, 243; B18 p.140, 254; B80 p.55, 123
- Resolution: WCAG decides compliance, so the floor is 4.5:1 and 3:1 in both polarities. The asymmetry stays as advice above the floor. Reversed text should get more contrast, weight or size, which matches the reversed-text rows in color and typography. Rules 1 and 2.

### 5. How many steps should a color ramp have?
- Side A: about seven, because that is how many lightness levels people hold in visual memory. Sources: B68 p.23, 48; B22 p.170-172
- Side B: eight to ten predefined shades per color, ideally nine from 100 to 900. Sources: B47 p.29, 147, 150
- Resolution: the two sides answer different questions. A ramp may hold nine to eleven primitives for state and surface needs. No role, legend or comparison should depend on telling apart more than about seven of them. Rule 5.

### 6. Flat color fields or subtle texture?
- Side A: keep flat color and avoid textures, borders and decorative shadows. Sources: B59 p.8
- Side B: perfectly flat, uniform color can read as one-dimensional, and subtle variation adds depth. Sources: B37 p.92, 186-187; B53 p.207
- Resolution: all three sources are tier 3 and none is study-backed. Rule 4 does not apply, since this is taste, not technology. Default to flat. Texture is allowed only as a deliberate brand material: very subtle, never under running text, and never on scrolling layers. The engine contradicts itself on this point (see gaps.md). Rule 3 ties, rule 5.

### 7. How many brand colors?
- Side A: three or fewer for most identities. Sources: B76 p.146-148
- Side B: one or two primaries plus two to four secondaries, or at most four hues in a web palette. Sources: B05 p.60-61; B59 p.8
- Resolution: all sources agree on one or two primaries. The tier 2 source sets the core identity at three colors or fewer. A UI palette may add neutrals and status colors on top of that. Rule 3.

## Data visualization and dashboards

### 8. Are pie charts and gauges acceptable on dashboards?
- Side A: pies are fine with at most five slices, each at least 5 percent, the largest starting at twelve o'clock. Sources: B46 p.310-311
- Side B: use lines and bars on dashboards. Gauges, dials, pies and 3D bars look attractive but compare poorly. Sources: B86 p.99; B02 p.422-423
- Resolution: both sides have tier 1 sources. Side B is newer and has two sources that agree. Default to bars and lines. A pie is acceptable only for one part-to-whole view of five or fewer parts with values labeled, and never for comparing across charts. Replace gauges with a labeled number or a bullet chart. Rules 3 and 5.

## Typography and layout

### 9. What is the ideal body measure?
- Side A: about 45 to 75 characters, with roughly 66 ideal for one column. Sources: B88 p.126-127; B92 p.55; B47 p.114-116; B78 p.81
- Side B: 75 to 100 characters for reading speed, or a hard maximum of about 60. Sources: B46 p.607-609; B10 p.52, 83, 89
- Resolution: WCAG 1.4.8 caps lines at 80 characters. Measured findings show readers prefer 50 to 60 characters even though they read slightly faster on long lines. Target 60 to 70 characters inside a 45 to 75 band, never past 80. Rules 1, 2 and 5.

### 10. Ratio-derived type scale or a hand-tuned one?
- Side A: derive every size from one ratio or modular scale. Sources: B92 p.60; B10 p.18-35
- Side B: hand-tune the scale, because modular ratios give fractional sizes and too few UI steps. Sources: B47 p.102-107
- Resolution: no study on either side, and both sides are tier 2. For screen UI, the newer, UI-specific source wins. Start from a ratio, round to whole pixels or rem, and add hand-tuned steps where the UI needs them. Rule 4.

### 11. Should reversed (light on dark) text be lighter or heavier?
- Side A: give reversed text equal or more weight, a slightly larger size and a little positive tracking. Keep hairline faces out of reversed settings. Sources: B88 p.139; B18 p.135-136; B19 p.29; B31 p.92
- Side B: the engine drops weight by about 50 units in dark mode, because light type looks thicker on dark. It cites no book.
- Resolution: two tier 1 and two tier 2 sources agree on side A. On screens, irradiation does thicken light type at display sizes. Limit any weight reduction to display weights of 600 and up, never take body text below 400, and add +0.01 to +0.02em tracking to small reversed text. Rules 3 and 5.

### 12. Strict regularity or asymmetry as the layout default?
- Side A: make near-equal values exactly equal, snap to halves and thirds, and keep the number of distinct alignment points low. Measured search was faster. Sources: B26 p.444-447; B46 p.178-182
- Side B: symmetric, centered layouts are static, and asymmetric columns create movement and give captions a home. Sources: B10 p.97, 131, 148; B92 p.26, 77
- Resolution: the evidence supports few alignment points and exact equality. An asymmetric split is fine when it reuses the same column lines. Rule 2.

## Components and patterns

### 13. Should visible menus be capped at about seven items?
- Side A: seven plus or minus two is the working limit, and menus should hold 5 to 10 items, ideally 8 or fewer. Sources: B20 p.289, 732-733; B46 p.402, 405-408
- Side B: there is no fixed cap. The seven-item limit is about recall of transient items, while a visible menu is scanned by recognition, so long grouped menus work. Sources: B02 p.141-142; B11 p.100
- Resolution: the seven-item finding measures short-term recall, which a visible menu does not load. Group long menus. Keep the soft default of about 8 for drop-down menus only, and limit cascades to two levels. Rules 2 and 4.

### 14. How long should a tooltip wait before showing?
- Side A: about two thirds to three quarters of a second. Sources: B46 p.565, 693
- Side B: about 1 second, or 1 to 2 seconds. Sources: B02 p.242; B86 p.132; B26 p.487
- Resolution: no standard sets the delay. Take the overlap of the tier 1 sources, about 0.5 to 1 second, with no delay for the next tip within about a second. WCAG 1.4.13 still requires the tip to be dismissible, hoverable and persistent. Rule 1 for the behavior, rules 3 and 4 for the number.

### 15. Should a destructive action look dangerous?
- Side A: give destructive actions a distinct, dangerous look so their weight is felt. Sources: B54 p.52; B44 p.98-99; B26 p.35, 213
- Side B: destructive does not mean big and red. Style it secondary or tertiary unless it is the main task, and save the strong red for the confirmation. Sources: B47 p.62
- Resolution: always separate destructive actions and set them apart from frequent ones. Do not give them primary weight on a page where they are not the main task. The strong danger fill goes on the confirm step. Rules 3 and 5.

### 16. May secondary controls appear only on hover?
- Side A: hover reveals and collapsed menus save space. Sources: B78 p.53-54
- Side B: never hide a high-priority action behind an invisible trigger, and give hidden menus a visible equivalent. Sources: B14 p.54-55, 93; B16 p.123; B52 p.142-143; B77 p.163
- Resolution: keyboard and touch users must reach every control (WCAG 2.1.1). Hover reveal is allowed only as an enhancement over a control that focus and touch can also reach. Rules 1 and 3.

### 17. Radio buttons or a drop-down for picking one value?
- Side A: a drop-down for any single choice from a known set. This is the engine's convention and has no book source.
- Side B: visible radio or check box sets were faster, more accurate and preferred, even up to about 30 options. Use a drop-down only when space is short and the default is usually right. Sources: B46 p.497-500, 571-576; B14 p.47-48
- Resolution: measured performance outranks an uncited convention. Rule 2.

### 18. Consistency or clarity first?
- Side A: stay consistent unless the new way is far better. Sources: B79 p.156, 159; B27 p.133-134
- Side B: clarity beats consistency when a small inconsistency makes something much clearer, and behavior that differs should look different. Sources: B77 p.44; B07 p.267-268
- Resolution: the two sides set compatible thresholds. Default to consistency, and break it only for a significant clarity gain or a real difference in behavior. Rules 3 and 5.

### 19. Are tabs safe for content?
- Side A: users repeatedly miss content hidden behind tabs. Sources: B23 p.466
- Side B: tabs work when the active tab comes forward and joins its panel, for fewer than ten short-labeled views. Sources: B77 p.92; B86 p.242-243; B26 p.638-639
- Resolution: use tabs for parallel views of similar size with a clear active state. Never use them for content every user must see. Rule 3, with side A kept as the scope limit.

### 20. One progressive form or a wizard for multi-step tasks?
- Side A: prefer state changes and progressive disclosure in one view, and keep wizards for rare, discrete steps. Sources: B14 p.80
- Side B: for infrequent tasks, a wizard with preview, save and exit, a step indicator and a summary hub outperformed a progressive form. Incomplete applications fell from 19 to 5 percent. Sources: B58 p.319-326, 373, 613-619; B11 p.117-118
- Resolution: decide by frequency and dependency. Frequent expert tasks get one view with disclosure. Rare or strictly ordered tasks get a wizard with a summary. Rule 2 for the rare-task case.

## Branding

### 21. Should a brand color follow its sector or stand apart?
- Side A: map the rivals' colors and pick a hue they do not own. Sources: B76 p.38, 41, 88; B05 p.60-61
- Side B: sectors signal trust through conventional, restrained treatments, so deviate only sympathetically. The palette should fit the product. Sources: B19 p.60-61, 94; B70 p.26-28
- Resolution: differentiate the signature hue, and keep sector trust cues in type restraint and tone where trust matters. Rule 5 for side A, rule 3 for side B's product-fit point.

## Motion, mobile, performance, XR

### 22. What minimum touch target size applies?
- Side A: 44 pt on iOS, 48 dp on Android, about 7 to 10 mm. Sources: B02 p.255-256; B86 p.297, 326; B52 p.132; B91 p.202; B80 p.32
- Side B: smaller or different values: 30 by 30 px, 20 to 30 mm finger areas, or three-quarter-inch squares. Sources: B40 p.60; B46 p.367-368, 457-458; B18 p.249
- Resolution: platform guidelines and WCAG decide. Use 44 pt or 48 dp on native platforms. On the web, 24 px is the hard floor (2.5.8 AA) and 44 px the target (2.5.5 AAA). The 30 px figure is out of date. The 20 mm figures apply to kiosks and public terminals, not phones. Rules 1 and 3.

### 23. May a carousel or ticker auto-advance?
- Side A: no. Load the first slide with controls and wait for the user, and anything that moves for more than 5 seconds needs pause, stop or hide. Sources: B18 p.99, 183; B91 p.240, 264
- Side B: the engine bans only slides shorter than 4 seconds, which implies slower auto-rotation is fine. No book source.
- Resolution: WCAG 2.2.2 and the tier 1 source win. Default to no auto-advance. Any carousel that keeps it needs a visible pause control and stops under reduced motion. Rules 1 and 3.

### 24. How long may an entrance animation run?
- Side A: 200 to 500 ms is the practical range, about 600 ms only when tested, and always under 1 second. Sources: B42 p.73-76; B26 p.297; B14 p.119
- Side B: the engine allows a hero reveal of 800 ms or longer and bans only durations past 1500 ms. No book source.
- Resolution: the tier 1 sources agree on under a second. Cap any non-ambient animation at 1000 ms. Rules 3 and 5.

### 25. How far must a pointer move before a press becomes a drag?
- Side A: about 3 px for a mouse, with axis-dependent values of 4 and 8 px. Sources: B26 p.520, 522
- Side B: the engine uses 8 to 12 px for every drag.
- Resolution: both values are right for their input. Use a few pixels for fine pointers and about 8 to 12 px of slop for touch, split by the pointer media query. Rules 1 and 4.

### 26. What should a short wait show?
- Side A: skeletons and content-first placeholders beat spinners, which make apps feel slower. Sources: B24 p.312-314; B42 p.152-156; B52 p.276-277
- Side B: skeletons only when the incoming structure is predictable, and spinners for short waits of unknown shape. Sources: B82 p.116-117
- Resolution: the newer source refines the older ones rather than overturning them. Use a skeleton when the structure is known, a spinner when it is not, and nothing under about 200 ms. Rules 4 and 5.

### 27. When must a progress indicator appear?
- Side A: any process over about 1 second needs a busy cue. Sources: B26 p.662; B86 p.409-410
- Side B: show nothing under 200 ms, an indicator after 200 ms, and progress with the expected length after 2 seconds. An older source keeps a plain busy cue up to 10 seconds and shows a percentage only beyond that. Sources: B52 p.264; B46 p.627-629
- Resolution: the bands fit one ladder. Nothing under 200 ms, an indeterminate cue from 200 ms to 2 s, determinate progress with cancel past 2 s, and background work past 10 s. The ten-second percentage threshold in B46 is superseded. Rules 2 and 4.

### 28. What page load time is acceptable?
- Side A: 8 to 10 seconds is acceptable and up to 5 seconds is good. Sources: B46 p.319-320, 625
- Side B: about half of mobile visitors leave after 3 seconds, and a second of lag loses customers. Sources: B44 p.72; B07 p.162
- Resolution: the newer sources and the current Core Web Vitals thresholds win: LCP at or under 2.5 s, INP at or under 200 ms, CLS at or under 0.1. Rule 4.

### 29. What frame rate does VR need?
- Side A: 60 fps minimum. Sources: B48 p.151, 162; B15 p.12
- Side B: 75 to 120 fps, matched to the display's native refresh. Sources: B15 p.79, 109; B36 p.157-159
- Resolution: match the device's native refresh, which is 72 to 120 Hz on current headsets. 60 fps is only a floor for older or phone-based headsets. Rules 4 and 1, where a platform publishes a required rate.

### 30. How should a VR user be moved?
- Side A: teleport to a visible, cancelable target, or fade to black and back. Sources: B48 p.148-149; B36 p.231, 250
- Side B: instant teleport disorients, so prefer a brief high-speed transition when orientation matters. Sources: B83 p.513-514, 550
- Resolution: both sides reject slow automated motion. Where spatial orientation matters, the tier 1 source wins and the move is a fast dash. For comfort-first casual use, a teleport with a target preview and a short fade is acceptable. Rule 3.

### 31. One design across mobile web and native apps?
- Side A: design a distinct native UI per platform, because porting breaks conventions. Sources: B24 p.15, 360-361
- Side B: keep behavior consistent across web, responsive and native apps. Sources: B11 p.123
- Resolution: keep the product behavior and content model consistent, and use platform-native controls and navigation. Rule 1.

### 32. Should mobile strip content?
- Side A: do not strip functionality, reprioritize it. Sources: B23 p.616-618
- Side B: reduce content and marketing on small screens. Sources: B06 p.300-301; B38 p.77
- Resolution: cut secondary and marketing content, never tasks or structure. Rule 5.


<!-- cluster C: interaction, content, access and AI -->

# Cluster C conflicts: interaction, content, access and AI

Where the books disagree, and how the sources.md rules settle it. Rule numbers refer to "The rules, in order": 1 standard beats books, 2 evidence beats authority, 3 authority beats count, 4 newer beats older on technology, 5 agreement raises confidence, 6 newer edition replaces older. Conflicts between a book and the engine itself are in gaps.md as contradicts rows.

## Navigation and information architecture

### C-01. Does the 7 plus or minus 2 memory span cap how many items a menu may show?
- Side A, yes: menus and lists should stay inside the short-term memory span. Sources: B49 p.107, 142; B06 p.45. Both restate the capacity figure; neither measures menus.
- Side B, no: the span describes unaided recall, while a visible menu is read by recognition and bounded by scanning; current estimates put working memory nearer 3 to 4 chunks anyway; measured menus of 18 to 24 items in labeled groups stayed fast, and broad shallow menus beat deep ones. Sources: B93 p.141; B02 p.141-142; B46 p.107, 347-349; B79 p.102-103; B11 p.100.
- Resolution: Side B. No fixed cap on a visible menu. Keep a level to roughly 4 to 8 ungrouped items and group beyond that (up to about 24 grouped, at most 10 per group). Use the 3 to 5 chunk limit only for things people must hold in their head across screens (codes, earlier choices).
- Rules: 2 (measured menu studies beat a restated capacity number), 3 (two tier 1 sources reject the cap explicitly), 5.

### C-02. Should every level of a menu be trimmed to the fewest choices (Hick's law), or is breadth fine?
- Side A, trim: each added choice slows the decision, so show the fewest options first. Sources: B57 p.92-93; B33 p.61-62.
- Side B, broad and shallow: two or three levels with grouped breadth were fastest; adding depth to keep each level short costs more than a wider level. Sources: B46 p.347-349, 376; B93 p.141-143; B86 p.134-135; B26 p.323-324, 604-605.
- Resolution: Side B for structure. Side A still applies inside a level: remove items nobody needs and order the rest naturally, then by frequency, then alphabetically. Hick's law is logarithmic and assumes unordered, unfamiliar options, so it argues for ordering and grouping, not a hard cap. Do not flatten so far that one level becomes an unsorted wall (B87 p.49-50).
- Rules: 2, 3.

### C-03. Do click counts matter?
- Side A: keep critical content within 2 to 3 steps of home; people abandon past two or three hierarchy levels. Sources: B46 p.167; B93 p.143; B35 p.240-241.
- Side B: the three-click rule has no support; what costs people is the doubt each click carries, and several effortless clicks beat one hard one. Sources: B77 p.54; B87 p.46-50.
- Resolution: compatible. Keep hierarchy depth to about 3 levels because scent decays with each level, but judge a path by how ambiguous each step is, not by the raw count. Wizard steps and obvious clicks do not count against it.
- Rules: 3 (tier 1 on both sides, so reconcile), 5.

### C-04. Hamburger menu or visible navigation on mobile?
- Side A, hamburger: a menu button hiding navigation is the accepted mobile web convention. Sources: B93 p.214 (2015); B59 p.11.
- Side B, visible: hidden navigation roughly halves discoverability, makes options seem less important and costs taps; large tests found a tab bar beating a drawer; a labeled Menu outperformed the bare icon for some users. Sources: B02 p.534-535 (2023); B07 p.198-201; B85 p.42-43; B24 p.37; B26 p.604.
- Resolution: Side B for primary destinations: 3 to 5 top-level sections sit in a visible bottom bar or inline. A labeled Menu button is acceptable for secondary items and for large content sites on mobile web; never hide navigation on desktop where it fits.
- Rules: 2 (measured discoverability and A/B results), 4 (newer source on a technology-dependent pattern).

### C-05. Alphabetical or task-based ordering for large menus?
- Side A, by task or topic: group by what people want to do. Sources: B93 p.127-131 (ambiguous schemes for exploration).
- Side B, alphabetical where people know the name: an 18-item alphabetical list was searched about four times faster than a random one; exact schemes serve known-item seekers. Sources: B46 p.350-352; B93 p.127-131, 152; B86 p.52-53.
- Resolution: both, by seeking mode. Use task or topic groups for exploration, alphabetical order inside groups and as an alternate index for known items. Never forbid alphabetical order outright.
- Rules: 2, 3.

### C-06. How visible must links be?
- Side A: underline links, reserve link styling for links, keep visited distinct. Sources: B46 p.378, 387-389; B77 p.72, 201; B59 p.14.
- Side B: in link-dense interfaces, style secondary links quietly and underline on hover. Sources: B47 p.126-127.
- Resolution: WCAG 2.2 SC 1.4.1 decides links inside prose: distinguishable by more than color, or 3:1 contrast with surrounding text plus a non-color cue on hover and focus. Quiet styling is fine in navigation and UI chrome where position signals a link.
- Rule: 1.

### C-07. Infinite scroll, load more or pagination?
- Side A: people scroll long single pages happily; offer View all or load on scroll. Sources: B23 p.499; B24 p.157.
- Side B: avoid infinite scroll when people need to find, compare, bookmark or reach the footer. Sources: B07 p.124-126.
- Resolution: by task. Casual feeds may scroll endlessly; search and product results that get compared or revisited use pagination or a load-more button, keep a stable URL and keep the footer reachable.
- Rule: 4 (newer, technology-dependent source for the compare case); Side A kept for browsing.

### C-08. When do breadcrumbs start?
- Side A: from two levels down. Sources: B86 p.194-195.
- Side B: they pay off mostly on large, deep sites. Sources: B77 p.91.
- Resolution: compatible. Add breadcrumbs when content sits two or more levels below a section landing page and people arrive from outside (search, shared links).
- Rule: 3 (tier 1 both sides, reconcile).

### C-09. Is the logo enough as a home link?
- Side A: the logo linking home is the convention and the escape hatch. Sources: B86 p.171-173; B46 p.790.
- Side B: mobile test users did not use the logo to go home; add an explicit Home item. Sources: B23 p.196.
- Resolution: both. The logo links home everywhere, and mobile navigation also carries an explicit Home item.
- Rules: 3, then 2 for the mobile observation.

### C-10. Browse first or search first?
- Side A: where labels are clear, browsing far outnumbers searching. Sources: B46 p.275-277 (2007).
- Side B: query volume and length grow fast with conversational and model-backed search, and heavy search use can signal weak navigation. Sources: B11 p.70-71, 106-107 (2025); B12 p.255.
- Resolution: provide both and make each feed the other. Behavior trends favor stronger search, but navigation stays the fix for findability failures.
- Rule: 4.

## Forms, errors and feedback

### C-11. Error summary at the top, or inline errors only?
- Side A, inline only: a top summary scrolls away, gets missed by sighted and screen reader users, and makes people remember the fix. Sources: B52 p.176-177; B27 p.148-150; B18 p.92-93; B14 p.117.
- Side B, summary plus inline: on submit, list the problems at the top with links to each field, especially on long forms. Sources: B23 p.566-567, 570; B86 p.525-526.
- Resolution: the inline message beside the field is mandatory on both sides. A linked summary is an optional supplement for long or multi-section forms, never a replacement. No WCAG criterion requires a summary.
- Rules: 3 (tier 1 on both sides), 5 (agreement on inline).

### C-12. Validate while typing, or when the field is left?
- Side A, live: check and coach input as it is typed. Sources: B54 p.140-142; B24 p.87-88.
- Side B, on blur or after a pause: validate when focus leaves or about half a second after typing stops; never flag an entry as wrong while the person is still typing something valid. Sources: B86 p.493-494, 526; B26 p.646-648; B52 p.175-176; B23 p.566-567.
- Resolution: Side B for errors. Positive live coaching (a strength meter, a rule list that ticks as rules are met) fits Side B because it never shows an error mid-entry.
- Rules: 3, 5.

### C-13. Confirmation dialog or undo for destructive actions?
- Side A, confirm first. Sources: B20 p.784, 810; B46 p.633-635; B89 p.117; B57 p.91-92; B83 p.172.
- Side B, act and offer undo: routine confirmations train reflex clicks. Sources: B26 p.216, 681-683; B79 p.204-207; B86 p.38-39.
- Resolution: compatible once scoped. Undo for anything reversible; a confirmation only when undo is impossible or the cost is high, and it names the action and the object.
- Rule: 5.

### C-14. May messages dismiss themselves on a timer?
- Side A: a brief toast (up to about five seconds) that offers undo is an acceptable light confirmation. Sources: B24 p.303-311.
- Side B: errors and confirmations stay until acknowledged. Sources: B26 p.291, 666, 680; B20 p.780, 816, 819.
- Resolution: WCAG 2.2.1 Timing Adjustable treats a timed message as a time limit the user must be able to turn off, adjust or extend unless it is non-essential. Errors and any toast that carries an action (undo, retry) persist or are adjustable; a purely informational success toast may fade.
- Rules: 1, then 3.

### C-15. How should required fields be marked?
- Side A, explained asterisk: an asterisk after the label with a note explaining it. Sources: B59 p.13; B46 p.236-237.
- Side B, the word optional: an asterisk is insider knowledge; mark the optional fields in words. Sources: B23 p.564; B86 p.494-495.
- Resolution: either convention, applied consistently; never an unexplained symbol. WCAG 3.3.2 and 1.3.1 require the requirement in text and in code (required or aria-required).
- Rules: 1, then 3.

### C-16. Can a placeholder stand in for a label?
- Side A: acceptable on very simple forms if it returns when the field is empty. Sources: B77 p.201.
- Side B: never. Sources: B86 p.493, 495; B52 p.164-165; B24 p.86-87; B14 p.97; B18 p.89, 93; B88 p.171.
- Resolution: Side B. WCAG 3.3.2 needs labels or instructions that stay available; a placeholder vanishes on input.
- Rules: 1, 5.

### C-17. One long page or several steps?
- Side A, one page: long forms work better as one scrolling page on mobile. Sources: B24 p.114-115.
- Side B, steps: break complex or high-stakes decisions into steps with a way back; a chunked form felt shorter. Sources: B21 p.181; B34 p.183-185; B78 p.66-67.
- Resolution: by task. Moderate forms stay on one page; complex, branching or high-stakes tasks are chunked with progress and back.
- Rules: 3, with 2 for the measured case.

### C-18. Is the shortest form always best?
- Side A: every extra field lowers completion; cut to the minimum. Sources: B52 p.152-153; B23 p.569-570; B44 p.45; B54 p.128.
- Side B: a minimal loan form left people unsure they had been approved; a longer, chunked form built confidence. Sources: B34 p.183-185.
- Resolution: both hold. Cut fields that give the user nothing back; on high-stakes forms add structure and reassurance, not extra questions.
- Rules: 2 bounds 5.

### C-19. Should error messages apologize?
- Side A: apologize briefly and take the blame. Sources: B02 p.209; B33 p.79; B44 p.66-67.
- Side B: no first-person, cute system voice; state the condition. Sources: B20 p.828-831; B46 p.594-599.
- Resolution: a short apology when the system is at fault is fine; persona, first-person I and jokes are not.
- Rules: 5, then 4 (the newer tier 1 on tone).

### C-20. Preselect defaults or leave fields blank?
- Side A: preselect the likely answer and do what the system can for the user. Sources: B44 p.46; B20 p.771-773.
- Side B: never assume a value for missing data; skip defaults where a wrong value is costly or sensitive. Sources: B52 p.173; B07 p.68-69; B86 p.520; B78 p.63-64.
- Resolution: default only when most people keep the value and an overlooked default is harmless; never for consent, sensitive data or cost.
- Rules: 3, 5.

## Accessibility and inclusion (book versus standard)

### C-21. Flash threshold
- Side A: nothing faster than 2 Hz; avoid 2 to 55 Hz. Sources: B26 p.402; B46 p.670-672.
- Side B: three flashes per second. Sources: B42 p.237, 239.
- Resolution: WCAG 2.3.1, at most three flashes in any one second (or below the general and red flash thresholds).
- Rule: 1.

### C-22. Minimum target size
- Side A: 16 by 16 px. Sources: B59 p.15.
- Side B: about 9.6 mm (about 44 CSS px) for touch and spacing for older users; targets big and spaced from unrelated ones. Sources: B80 p.138-139; B20 p.715-717; B58 p.622-623.
- Resolution: WCAG 2.2 SC 2.5.8 sets 24 by 24 CSS px (or the spacing exception) at AA; 44 by 44 is AAA and the iOS target, 48 dp on Android. For older audiences treat 44 px plus spacing as the floor. The 16 px figure is out of date.
- Rule: 1.

### C-23. Text contrast
- Side A: aim for about 80 percent contrast. Sources: B26 p.401, 440.
- Side B: 4.5:1 for normal text, 3:1 for large. Sources: B59 p.6; B47 p.162.
- Resolution: WCAG 1.4.3 ratios.
- Rule: 1.

### C-24. Type size for older readers
- Side A: body text in a 12 to 14 pt sans serif, headings at 14 to 16 pt, and no pull-down menus. Sources: B46 p.678 (2007).
- Side B: at least 16 pt in an inclusive checklist. Sources: B32 p.116 (2007).
- Resolution: WCAG 1.4.4 (resize to 200 percent) and 1.4.10 (reflow) govern; set at least 16 px body on the web and let it scale. The advice against pull-down menus is dated and has no basis in the standard.
- Rules: 1, then 4.

### C-25. How to depict people across cultures
- Side A: simple line figures without skin tone, modest clothing, right hand doing the task. Sources: B08 p.191-193, 210 (2005).
- Side B: show a range of skin tones, genders, ages and builds, never call one tone nude or flesh, and let people describe their own identity. Sources: B37 p.114-115; B36 p.279-280; B65 p.140-153.
- Resolution: Side B for representation; keep Side A's warning about gestures, bare feet and religious symbols that carry local meaning.
- Rule: 5.

## Internationalization

### C-26. How much room to leave for translated text?
- Side A, a flat allowance: about 30 to 50 percent. Sources: B11 p.166; B52 p.87-88; B06 p.267.
- Side B, by string length: 10 characters or fewer grow 100 to 200 percent, 11 to 20 about 80 to 100, 21 to 30 about 60 to 80, 31 to 50 about 40 to 60, 51 to 70 about 31 to 40, longer text about 30 percent; very short menu items up to 300 percent. Sources: B46 p.659-660; B23 p.603-604.
- Resolution: Side B. The flat figures describe running text and match the long-string rows; buttons, tabs, nav items and labels need the larger allowance. Verify with pseudo-localization.
- Rules: 2 (measured length table), 3.

### C-27. Do high-context audiences, Arab users included, want denser pages?
- Side A: high-context cultures, Arab countries named, accept more animation, varied layouts and denser pages; relationship-oriented users preferred more information units. Sources: B11 p.164, 166; B49 p.198-199.
- Side B: similarities across countries often outweigh differences; avoid stereotyped per-country design. Sources: B50 p.128-133.
- Resolution: the measured evidence compares Chinese and German users only; extending it to Arab users is an unmeasured generalization. Treat density as a variable to test with local users, not a regional default.
- Rule: 2.

## AI, conversation and engagement

### C-28. Show model confidence as numbers or as words?
- Side A, numbers: convert scores to probabilities, show estimates in natural units and let people set thresholds. Sources: B61 p.251-252, 259-260, 379; B21 p.180.
- Side B, words or bands: raw percentages mislead or invite blind trust; a language model's percentage is a token likelihood, not an accuracy rate. Sources: B51 p.150-155; B82 p.142.
- Resolution: Side B for model self-confidence; Side A only for calibrated estimates in natural units (minutes of delay, a price range).
- Rule: 4, with a scope split.

### C-29. Free conversation or structured choices?
- Side A: a conversation-first style that keeps context, uses short turns and mixed initiative. Sources: B60 p.27-36.
- Side B: a set of structured options can feel more natural than open chat because its value is plain; use chat only where exploring beats efficiency; offer 2 or 3 contextual options. Sources: B33 p.37-38, 82-83; B16 p.144-145; B21 p.42, 145-146; B63 p.194-195.
- Resolution: Side B decides whether to use chat at all and when to offer chips; Side A governs how to build the dialog once chat is chosen (context, repair, mixed initiative).
- Rules: 5, then 4.

### C-30. Show the recognized speech text?
- Side A, hide it in conversation: showing misheard words undermines trust even when the answer itself is correct. Sources: B41 p.166-168.
- Side B, show and read back: show recognized commands and read captured answers back before saving. Sources: B48 p.170-171; B60 p.131-132, 160.
- Resolution: scope split. Show or read back whenever the words become data or a query (search, commands, form values); do not echo the transcript in free conversation.
- Rule: 3, per scope.

### C-31. How humanlike should an assistant be?
- Side A: define a persona because people infer one anyway; small human cues help; an animated virtual human raised disclosure in a study. Sources: B41 p.93-101, 121; B73 p.14, 54; B63 p.70-71.
- Side B: minimal personification; no avatars for task tools, no claimed feelings, humanlike framing inflates trust and oversharing. Sources: B21 p.41, 132, 148, 181; B43 p.151, 207; B16 p.155-157; B51 p.195-198, 313-314; B33 p.81.
- Resolution: Side B. Define voice traits for consistency, but no faces, no claimed emotion and no first person in recommendations for task tools. The disclosure study measures the very effect Side B calls a harm, so it does not justify avatars.
- Rules: 4, 5 (rule 2 considered; it does not favor Side A).

### C-32. Product tours: allowed up to a length, or avoided?
- Side A: first-run tours of up to five to seven screens with skip and relaunch; walkthroughs suit counterintuitive concepts. Sources: B26 p.415-417; B07 p.32-37.
- Side B: people skip tours, overlays and demos; a single tip pointing at the first action was the only concept that tested well; after a ten-screen tour no participant could finish the task. Sources: B24 p.245-246, 273-281; B77 p.168-169.
- Resolution: Side B by default (teach by doing, one contextual tip). Side A sets the ceiling when a tour is justified: at most five to seven screens, skippable, re-openable.
- Rule: 2.

### C-33. Create an account early?
- Side A: default to creating an account so continuing costs one click and builds a small commitment. Sources: B54 p.114-115.
- Side B: no registration wall before the first success; ask only at the commit step. Sources: B86 p.33; B44 p.126; B78 p.12; B33 p.55-57.
- Resolution: Side B. Side A survives only after value is shown, as a one-click default that serves the user.
- Rules: 3, 5.

### C-34. Is a fake button for an unbuilt feature acceptable?
- Side A: a stub or fake buy button measures demand before building, if it then tells people the feature is not ready. Sources: B27 p.86, 88, 103-104, 119.
- Side B: decoy buttons are manipulation. Sources: B77 p.199-200.
- Resolution: compatible only when the stub discloses itself on click and collects nothing (no payment details, no personal data). A stub that takes payment or misleads about availability is a dark pattern.
- Rule: 3.

### C-35. How many options in a spoken prompt?
- Side A: three by default, four only for short intuitive items. Sources: B63 p.114-115.
- Side B: three or four at most; phone menus up to four per level. Sources: B73 p.40-41; B02 p.148; B46 p.714-715.
- Resolution: three by default, four as a hard ceiling.
- Rule: 5.

### C-36. What response latency feels natural?
- Side A, voice: human turn gaps run about 200 ms and rarely pass 400 ms; a reply that needs thought gets a short marker first. Sources: B73 p.43-44, 62-63; B63 p.41; B41 p.249.
- Side B, chat agents: about 2 to 3 seconds feels natural. Sources: B82 p.125.
- Resolution: different modalities. Voice acknowledges within a few hundred milliseconds (a marker counts); a text answer may take 2 to 3 seconds if the send is acknowledged at once.
- Rule: 4, scope split.

### C-37. End every turn with a follow-up, or leave the floor open?
- Side A: end each turn with a useful continuation (go deeper, refine, act, wrap up). Sources: B16 p.172-173.
- Side B: do not fill the user's closing turn with a feedback or anything-else question; wait 2 to 3 s in voice or 20 to 30 s in text, and ask only if the agent helped. Sources: B60 p.33, 162-163.
- Resolution: offer continuations as optional, non-blocking affordances (chips, one suggestion); never a feedback question after every turn.
- Rules: 3, with 4 keeping Side A's non-blocking form.
