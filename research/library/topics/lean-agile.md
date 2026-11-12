# lean-agile

Input rows: 46. Merged rows: 16.

## Cadence

- **Plan around one to four week iterations, with two weeks as the common default.** Most Scrum teams (the majority framework in agile surveys) run two-week sprints, with teams of roughly 8 to 10; match any design sprint to that cycle (one or two weeks). Confidence: high. Sources: B50 p.123; B02 p.436, 520; B34 p.142; B11 p.155; B96 p.25, 37; B85 p.45, 310; B21 p.167-168
- **Run design and research one step ahead of the development sprint.** When a story is picked up, its tested design should already exist: work on sprint n+1 designs while assessing what shipped in sprint n-1, and as a minimum raise at planning that the designer needs two to three days of lead time. Do a light analysis up front, maintain a single integrated prototype and one style guide that all teams share, and have every release add capability without altering how features already shipped behave. Confidence: medium. Sources: B20 p.662-677; B85 p.38-39; B38 p.23; B11 p.155; B34 p.153
- **Fit each research round inside the sprint rhythm.** A lean usability cycle (recruit, test, analyze) can finish in under two weeks instead of the three or more that is common; a fixed weekly rhythm such as build early in the week, test on one set day and plan at the end keeps learning continuous. Confidence: medium. Sources: B03 p.73; B34 p.178-179
- **Iterate rough and fast before adding fidelity.** Sketch the interactions first as a rough clickable prototype rather than walking the wireframe, mockup, prototype sequence; three or four design iterations a day are possible with 10 to 15 minutes to a few hours of work between critiques. Confidence: low. Sources: B87 p.11; B09 p.32

## Outcomes and hypotheses

- **Give teams outcomes to move, not features to ship.** Ask a team to change a measurable customer behavior; a feature list is output whose value stays unknown until it meets real use. Confidence: medium. Sources: B34 p.36-37, 45-46; B27 p.19-21; B64 p.216
- **Frame each feature idea as a falsifiable hypothesis tied to a named signal.** State that a [change] for a [user] is expected to produce an [outcome], and name the [metric] whose movement will confirm it; then build the cheapest test able to disprove it, since a hypothesis with no metric cannot be tested. After launch, keep validating with interviews, usability tests and A/B tests: agile provides the rhythm and lean provides the purpose. Confidence: medium. Sources: B64 p.216; B27 p.19-21; B25 p.53; B87 p.57-61
- **Write the problem, the audience, the solution attributes and the solution as distinct statements.** Teams often mistake a desired attribute for a solution; a point-of-view statement (user, need, insight) converts facts into a direction you can act on. Confidence: low. Sources: B72 p.310, 317

## Minimum viable experiments

- **Fake the hard part before building it.** Deliver the service by hand for a few customers (Wizard of Oz or concierge), or put up a preorder button that takes minutes to wire, before automating anything; a limited release with one or two working features plus a three-question survey after sign-up is another cheap probe. Confidence: medium. Sources: B27 p.120-121, 221; B64 p.216
- **Define an MVP as the least work that answers the riskiest question.** It need not be a cut-down product at all; field data gathered with rented equipment can be the real MVP. Track how fast the team completes each learning loop. Confidence: low. Sources: B72 p.303-304; B25 p.53
- **Ship a limited product, never a broken one.** An MVP may do little but must do it well; a broken release returns a false negative on the whole idea. Design the smallest shippable version and do not hint at functionality that is not built (a comment box without attachments beats no comment box). Confidence: low. Sources: B27 p.175-176; B47 p.18-19
- **Release risky changes in stages and track how many people switch back.** Begin opt-in, move to opt-out with a route back, and then roll out to a percentage of users or to a cohort of new users (starting at 1 to 10 percent). A loud one percent opting out is acceptable; if half the base reverts, the change has failed. Confidence: low. Sources: B27 p.222-225

## Backlog and artifacts

- **Log UX debt on the backlog exactly as tech debt is logged.** A single pass is not iteration: lay out the present journey next to the ideal one and write a debt story for every gap. Confidence: low. Sources: B34 p.172
- **Keep the big picture with a story map.** Lay a backbone of user activities across the top, stories beneath each, and slice releases from the minimum needed to reach the outcome, so increments do not become a patchwork. Confidence: low. Sources: B64 p.236-238
- **Name the persona in user stories and write each epic for two contrasting personas.** "As [persona, role] I want ... so that ..." written for two different personas shows that one solution rarely fits all; walking past decisions through a persona later explains why they were made, and knowing whom you are not designing for speeds decisions. Confidence: low. Sources: B50 p.124-126

## Team and adoption

- **Staff design to the team's iteration load.** Product and UX roles can be combined on teams under about seven or eight engineers, but a lean team with a single designer saw design stagnate after about 12 weekly iterations until a second designer joined. Confidence: low. Sources: B27 p.220; B09 p.106-107
- **Pilot a new process small, then standardize from what the pilot shows.** Keep pilot groups limited; a pilot that ballooned into a two-day lecture for 40 people damaged adoption. Confidence: low. Sources: B62 p.304-305
