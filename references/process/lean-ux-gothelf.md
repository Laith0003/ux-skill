# Lean UX — Team-Oriented, Hypothesis-Driven Design

## What this is for

Lean UX is how you run product design when the work matters, the team is small, and shipping a 200-page spec into a six-month build is a way to lose. It is a synthesis of three disciplines into a single working method: design thinking gives you the user-centered framing, agile gives you the cadence and feedback, lean startup gives you the validated-learning posture. You take all three and run them as one loop.

Use this when you are building software with a real team, against real users, under real uncertainty. Skip it when the answer is already known and the work is execution-only.

---

## Three foundations

You inherit three intellectual traditions. Each one fixes a failure mode in the others.

**Design thinking** is your defense against building the wrong thing well. It forces you to start with the human, not the technology or the org chart. Empathy is a step, not a slogan. You go and watch real people in their actual context. You stop confusing your stakeholders' opinions with your users' problems.

**Agile development** is your defense against burning a year on a plan that the market has already moved past. You ship small. You inspect. You adapt. The unit of progress is "what worked in production," not "what we planned in January."

**Lean startup** is your defense against confusing motion for progress. Every meaningful piece of work begins as a hypothesis and earns its place by surviving contact with users. You measure outcomes, not effort.

When you only run design thinking, you over-explore and never ship. When you only run agile, you ship things nobody wanted. When you only run lean startup, you optimize a flow that nobody loves and never invest in craft. The synthesis is the point.

---

## The shift from deliverables to outcomes

The old design model rewarded artifacts. You wrote a 90-page wireframe document, signed it off, threw it over the wall, and the wall threw the build back six months later — by which point the document was wrong and the team had stopped reading it.

You are leaving that model behind. The new question is not "what artifact did you produce" but "what outcome did you create for users that changed a business metric."

This has practical consequences. You stop sizing UX work in document pages. You stop measuring designers by how thick their Figma file is. You stop treating handoff as a phase. Designers stay with the team across the whole loop — research, sketch, build, measure, learn, sketch again — and the artifacts they make are throwaway scaffolding for a conversation, not contracts.

The artifacts shrink. The conversations grow. The decisions get faster.

Mistake to avoid: do not let "lean" become an excuse to skip artifacts entirely. You still write down decisions. You still leave a trail. The point is that the artifact serves the team's working memory, not the team's compliance theater.

---

## Assumptions, made visible

Before you can write a hypothesis, you need to know what you are assuming. Teams that skip this step write hypotheses on top of unspoken assumptions, and when the hypothesis fails they cannot trace why.

An assumption is anything the team believes about the world that is not yet validated. They come in categories.

**Business assumptions.** What we believe about the market, the customer, the partner, the channel, the price point. "Partners will pay X per month for this." "The total addressable market is large enough to support a 10x business." "Existing partners want a loyalty program but cannot get one because the alternatives are too complex."

**User assumptions.** What we believe about the user's problem, context, capability, and motivation. "Customers want to track loyalty points across multiple merchants in one place." "Partners can configure rules without help if the interface is good enough." "Users will adopt this if it is faster than the current method."

**Behavior assumptions.** What we believe users will do once we ship. "New users who see the wizard will complete signup at 80%." "Partners who configure rules in the first session will return weekly." "Customers who earn their first reward within 7 days will become repeat users."

**Feature assumptions.** What we believe about our solution. "A wizard is the right interaction pattern for this." "The default rules cover 80% of real-world use cases." "The dashboard provides enough information to debug edge cases."

For each category, the team writes down everything it currently believes. Many of the items will feel obvious; write them anyway. The act of writing makes them visible. Some will be controversial; write those too, even if the team is split.

The output is a board with 30 to 100 assumptions, organized by category. The board is alive — the team adds to it as new assumptions surface, and crosses off assumptions as evidence validates or refutes them.

**Risk ranking.** Not all assumptions are equally important. The team ranks them on two axes: how risky is this assumption (how badly would the work suffer if it turned out to be wrong) and how unknown is it (how much evidence do we currently have). The assumptions that are high-risk and high-unknown are the ones that become hypotheses; the assumptions that are low-risk or already well-evidenced are noted but not tested.

The riskiest unknown assumption is the next thing the team should test. This is the discipline. Many teams test their easiest assumptions first because they are easy to test, and they avoid the hardest unknowns because testing them is uncomfortable. The result is months of "validation" that confirms the easy parts of the work while the hard part remains a guess. Test the hard part first.

---

## Hypothesis-driven design

Every meaningful design decision in this model starts as a falsifiable statement.

The template you commit to memory:

> We believe **[this outcome]** will be achieved if **[these users]** attain **[this benefit]** with **[this feature]**.

Read each clause carefully — they all do work.

- **This outcome** is the business or user behavior you want to change. "Repeat purchases go up," "support tickets about onboarding drop," "weekly active partners increases." It is measurable. It is not "users will like the new design."
- **These users** is a specific, narrow segment. Not "users." Not "everyone." A particular cohort with a particular problem in a particular context. "New partners in their first 14 days who joined via the self-serve path." Specificity is what makes the hypothesis testable.
- **This benefit** is the user-perceived value you believe the feature delivers. Not the feature itself — the thing the feature gives them. "Confidence that they set the loyalty rules up correctly" is a benefit. "A wizard" is not a benefit.
- **This feature** is the smallest version of the thing you will build to test the hypothesis. If you cannot describe the feature in one sentence, the hypothesis is not ready.

The point of writing it this way is that you can be wrong. A hypothesis you cannot fail is not a hypothesis — it is a plan in disguise. The moment you write "we believe weekly active partners will go up if we make the UI more beautiful," you have written nothing. Force the specificity.

You also write hypotheses at multiple altitudes. There are program hypotheses (the bet behind a quarter of work), feature hypotheses (the bet behind one sprint), and design hypotheses (the bet behind a single screen). They nest. The lower ones inform the higher ones.

---

## Outcome over output

The trap is measuring what you shipped instead of what changed. "Output" is the thing you did. "Outcome" is the thing your users now do differently because of what you did.

You ship 12 features in a quarter. That is output. Of those 12, four moved a metric, three were neutral, five made things slightly worse. That is the outcome conversation. Output is easy to count and useless to optimize. Outcome is harder to count and the only thing that matters.

In practice you do three things.

You name the outcome for every initiative before work starts. "Increase weekly active partners by 15% within 60 days of feature ship" is an outcome. "Build the new partner dashboard" is an output.

You instrument the outcome before you ship. If you cannot measure whether the outcome happened, you cannot learn. The instrumentation is part of the feature, not a follow-up ticket.

You retire features that did not produce the outcome. This is the hardest discipline. Teams get attached to what they built. Lean UX gives you permission, and the obligation, to delete code that did not earn its keep.

---

## The hypothesis backlog

Hypotheses are not one-off artifacts. They accumulate. The team maintains a backlog of hypotheses the same way it maintains a backlog of stories. The hypothesis backlog is the team's queue of bets it wants to run, ordered by priority.

Each hypothesis in the backlog has a state: not yet started, in flight, decided. The "in flight" set is what the team is currently testing. The "decided" set is what the team has resolved, with a brief note on the outcome and the change it produced.

The backlog is reviewed weekly. New hypotheses get added as assumptions surface. Existing hypotheses get reprioritized as new information arrives. Stale hypotheses — ones that were urgent six weeks ago but no longer matter — get archived rather than executed.

Why a backlog and not a single hypothesis at a time? Because the team's bandwidth is enough to run two or three hypotheses in parallel without losing focus, and the backlog ensures that as soon as one hypothesis resolves, the team has the next one queued. Idle time between hypotheses is wasted learning capacity.

How big should the backlog be? Smaller than you think. Twenty live hypotheses is too many — the team will not finish them, and the prioritization debate consumes more time than the execution. Five to eight active hypotheses, with a reserve of another ten that the team has scoped but not started, is a healthy size.

---

## Vision and framing — the upfront work

You do not just sprint blind from day one. There is a short, intense framing exercise before any iteration loop begins. It is days, not weeks, and it produces five artifacts.

**Problem statement.** One paragraph. The current state, the gap, and the specific change you want to drive. Avoid solutions in the problem statement. Solutions come later.

**Assumptions.** Everything you currently believe about the user, the problem, and the solution that is not yet validated. Write them down. There will be more than you expect. The act of writing surfaces the ones you didn't know you were carrying.

**Hypotheses.** Convert the riskiest assumptions into the hypothesis template. Rank them by risk — what would hurt the most if it turned out to be wrong.

**MVPs.** For each top-ranked hypothesis, design the smallest possible experiment that would tell you whether the hypothesis holds. An MVP in this method is a learning instrument, not a product launch. It may be a clickable prototype, a landing page, a Wizard-of-Oz demo, a five-user concierge test.

**Learning loops.** The mechanism by which the team will run, observe, decide. Cadence, who participates, what counts as a result, who has the authority to kill the bet.

These five artifacts fit on one wall. Not in one binder. The wall is the contract. Anyone who walks into the room can see what the team is trying to do, what they are guessing about, and what they are testing this week.

---

## Collaborative design

The lone designer who emerges from a cave with a perfect comp is finished. Not because design is unimportant — because the cave is wrong. The work is better when the team makes it together.

The core technique is the **design studio**. It is a time-boxed working session, usually two to three hours, with a mixed group — designers, engineers, product, sometimes a partner-facing voice. Everyone sketches. Engineers sketch. Product managers sketch. The sketches are bad and that is fine. The point is to get every idea into the open before anyone commits to one.

The studio runs in rounds. First round: each person, alone, sketches three to six ideas for the problem on paper. Second round: each person presents their sketches to the group in three minutes, no defending. Third round: the group critiques, picks elements, recombines. Fourth round: each person sketches one refined concept. Fifth round: the group converges on one direction to prototype.

This works because it kills two enemies of good design. The first enemy is groupthink — the loudest voice wins, the quiet voice never gets the idea out, the team converges before it has explored. Sketching alone, first, fixes this. The second enemy is design-by-committee — every stakeholder injecting their preference into a single artifact until the artifact has no spine. The studio gives each idea a fair hearing and then commits to one direction.

You still need a single point of authority on the final visual and interaction direction. The studio is convergence with input, not democracy.

A few rules to enforce: no laptops, no slides, no rehearsed pitches. Pen on paper or markers on whiteboard. Time-box every round to the minute. The facilitator is not a participant — they run the clock.

---

## MVPs and experiments

The MVP in this method is the smallest test that produces learning. It is not the first slice of the eventual product. Those are different things, and conflating them is the most common failure.

A few MVP archetypes you will use repeatedly.

**The clickable prototype.** Static screens linked together. Five users walk through a task. You watch. You learn whether the flow makes sense, where they get stuck, what language confuses them. Cheap, fast, and the highest learning per dollar for early-stage flows. Build time: hours.

**The fake door.** A button in a real product that goes to a "coming soon" or signup screen. You measure click-through to gauge demand for a feature that does not yet exist. The signal is noisy but directionally useful when you have a real population to test against.

**The Wizard of Oz.** Front-end looks real, back-end is a human doing the work manually. Lets you test whether users want the experience before you build the infrastructure to deliver it at scale. Especially useful for AI-shaped features where the model work is expensive.

**The concierge MVP.** You deliver the service to a small number of users by hand. No software at all yet. You learn the workflow, the edge cases, the language users actually use, before writing the code.

**The landing-page test.** A real page describing the product, with real ad spend driving traffic, to measure conversion to a waitlist or pre-order. Tests whether the value proposition lands before the build.

**The single-feature live test.** You ship one feature behind a flag to a small cohort and measure outcome against a control. The "real" MVP — but only after the cheaper MVPs have ruled out the obvious wrong directions.

The discipline is to always pick the cheapest MVP that can produce the answer. Building the live feature when a clickable prototype would have answered the question is a tax on every other thing the team could have learned in the same week.

---

## Feedback and research — continuous

In the old model, research was a phase. There was a "research kickoff" before the design phase and maybe a "validation study" at the end. In between, the team flew blind and trusted the brief.

In this model, research is continuous. Every week the team is in front of users. Not a heavy "study" — small, regular contact. Two to five users per week, 30 minutes each, no production. Some weeks it is a usability test on an in-progress prototype. Some weeks it is an open conversation with a recent signup about what surprised them. Some weeks it is watching a partner use the live product over a shared screen.

The cadence matters more than the perfection of any one session. A team that talks to two users every week beats a team that runs one beautiful 12-user study per quarter.

Everyone on the team attends. Not just the designer. The engineer who built the feature watches the user struggle with it. The product manager hears the question that the user actually asks. The team holds the same picture of who they are building for. This is the single highest-leverage habit in the whole method.

Make a few practical commitments. A recruiting pipeline that is always warm — you do not start finding users when you need them. A standing weekly time slot — the team treats it like any other ceremony. A simple debrief format — what we expected, what we saw, what we will change. Save the conversations. Don't make them ceremonial. Make them cheap to do, so you do them often.

---

## Integrating with agile

Lean UX lives inside an agile cadence, not next to it. You design at the speed of the sprint, and you give the sprint enough design to ship without burning a sprint waiting for design to finish.

A few specific integrations.

**Sprint zero.** Before the first iteration, the team runs the framing exercise. Problem statement, assumptions, hypotheses, MVPs, learning loops. Usually one week. The output is not a complete design — it is enough alignment that the first sprint can pick up real work without inventing context.

**Story mapping.** Before the team commits sprint scope, lay out the end-to-end user journey on a wall, story by story. Prioritize the top row — the spine — and slice horizontally to define each release. Story mapping replaces the requirements document and beats it on every axis.

**Design at story-time.** Designers do not work a sprint ahead of engineers in a separate track. Design happens at the moment a story is picked up, with the engineer and the designer pairing on the screen for an hour, with the user research from last week still fresh. Decisions get made together. Implementation starts the same day.

**Design debt as a tracked item.** Some decisions are deferred — you ship a quick version because the priority is learning, not polish. Those deferrals are tickets in the backlog like any other technical debt item. They are visible. They get scheduled. They do not pile up silently and then ambush the team six months later.

**Definition of done includes the outcome.** A story is not done when the code merges. It is done when the team has instrumented and observed the outcome the story was meant to produce. This is a slow change and it will fight you. Hold the line.

---

## Organizational shifts

You cannot run Lean UX on top of an organization that rewards the old behaviors. A few shifts are non-negotiable.

**Roles.** Designers are members of the product team, not a service group that takes tickets from PMs. The team has a single point of design authority but everyone contributes to design. Product managers stop writing spec documents and start writing hypotheses. Engineers participate in design, not just in build.

**Governance.** Senior reviewers stop asking "is this on plan?" and start asking "what did you learn this sprint and what are you betting on next?" If the executive review asks for a Gantt chart, the work will be a Gantt chart, and Lean UX dies.

**Success metrics.** Promotions, performance reviews, and team-level OKRs measure outcomes, not output. "She shipped seven features" is a weak signal. "Her team's outcome metric moved 18%" is the signal you reward.

**Funding.** The work is funded in time-boxed bets, not project budgets. A team gets a quarter and an outcome target, not a 14-month roadmap. At the quarterly review, the team reports what worked, what didn't, and what the next bet is. The team that runs lean and learns fast gets the next round of funding. The team that just spent its budget on plan does not.

**Failure tolerance.** Hypotheses fail. That is the point. If no hypotheses fail, the team is testing only safe ideas, and you are not learning. You explicitly reward the team that ran a clean experiment that produced a clean "no." The "no" was the goal.

---

## Measurement, in detail

The outcome focus only works if the team measures the outcomes. A few practical notes.

**One primary metric per hypothesis.** Not five. Not fifteen. One number that, if it moves, tells you the hypothesis was right. Supporting metrics around it are useful, but the primary metric is the one the team commits to before the experiment runs. Without that commitment, the team will rationalize whatever the data shows.

**Define the metric precisely.** "Weekly active users" sounds clean until you ask what counts as active. Logged in? Performed a key action? Completed a task? The team agrees on the operational definition before measurement starts. Otherwise, the metric becomes whatever the most motivated person says it is.

**Baseline before you change.** You cannot tell if a change worked if you do not know what the metric was before the change. Establish the baseline. Run the experiment. Compare. The baseline window should be long enough to capture normal variance — a week or more for most metrics, longer for low-frequency behaviors.

**Statistical significance is not the only bar.** Sometimes a small movement matters. Sometimes a large movement is noise. The team uses statistical thinking but does not surrender to it. A pattern that holds across multiple experiments, even when no single experiment is significant, is real. A single significant experiment that contradicts everything else may be a fluke. Judgment is part of measurement.

**Leading vs lagging indicators.** Outcome metrics are often lagging — they tell you what happened, not what is about to happen. Pair them with leading indicators that move earlier. If your outcome is "monthly revenue per partner," a leading indicator might be "weekly active sessions" or "feature adoption in the first 14 days." The leading indicator lets the team adjust before the lagging metric confirms a problem.

**Counter-metrics.** Some changes that move the primary metric in the right direction also move other metrics in the wrong direction. A feature that increases short-term engagement may decrease long-term retention. Track counter-metrics — the things the team would not be okay with if they moved badly — alongside the primary. A primary that wins at the cost of a counter-metric is not actually a win.

**Cohort views.** Aggregate metrics hide important variation. The change that helped new partners may have hurt experienced ones, and the aggregate may be flat. Look at the metric by cohort: new vs experienced, by segment, by acquisition channel. The patterns inside the aggregate are usually more informative than the aggregate itself.

---

## The anti-pattern: Lean UX as cover

The most common failure of this method is not the method failing. It is the method getting weaponized.

A team says "we're doing Lean UX" to justify shipping unresearched, untested, unfinished work. A leader says "we're moving fast" to skip the framing exercise. Someone calls a one-hour internal review "research." Someone draws a half-baked sketch and calls it an MVP. The team accumulates fake learning and ships a worse product than they would have under the old method.

The defense is simple but unforgiving. The method is hypothesis, test, learn, decide. If you skipped the hypothesis, you are not running this method. If the "test" had zero users in it, you are not running this method. If you did not write down what you would change based on the outcome, you are not running this method.

Other anti-patterns to name and refuse.

**"We don't have time for research."** Research is hours, not weeks, in this model. The team that says this is usually the one that will spend three months building the wrong thing.

**"The MVP is just the first feature."** No. The MVP is the smallest learning instrument. If the only thing it produces is "we built one feature," it was not an MVP, it was a slice.

**"We'll instrument it later."** No. The instrumentation ships with the feature. Otherwise the outcome is invisible and the loop is broken.

**"The designer can handle the user research."** Sometimes. But the team going to the conversations together is the whole point. Outsource recruiting; don't outsource the conversations.

**"We'll do Lean UX once we have time."** You never have time. The method is what produces time, by killing the wrong work before it gets built.

---

## Working with stakeholders

The team does not work in a vacuum. There are executives, investors, partners, sales counterparts, and customer support voices that have legitimate input into the work. Lean UX gives you a way to engage them without surrendering the discipline.

**Engage stakeholders on outcomes, not features.** When an executive asks "when will feature X ship," the team's answer is "feature X is one of the bets we have running to move outcome Y. Here is what we have learned so far, here is what we are testing next, here is what we expect to be true in 60 days." This reframes the conversation away from features-as-promises and toward outcomes-as-bets.

**Invite stakeholders to sessions, not to reviews.** A stakeholder who watches a user struggle with the product becomes an ally of the work. A stakeholder who only sees polished slides becomes a source of demands. Bring them to research sessions, design studios, and demos. They will see what you see.

**Frame surprises early.** When the data shows that a stakeholder's pet feature is not landing, the team surfaces it early, with the data, before the stakeholder reads about it second-hand. The surfacing is not adversarial; it is collaborative. "Here is what we expected. Here is what happened. Here is what we are thinking about doing next." Stakeholders who are involved in the diagnosis are easier to align with the cure.

**Push back when the request is wrong.** Stakeholders sometimes ask for features that contradict what the team has learned. The team's job is not to comply; it is to surface the contradiction. "We can build this, but our user research suggests it will not move the outcome you care about. Here is the evidence. Here is what we propose instead." Some stakeholders will accept the redirect; some will override it. Either way, the team is not silently building the wrong thing.

**Protect the team's calendar.** Stakeholders have an unlimited appetite for status updates. The team's time is finite. Establish a regular rhythm — a fortnightly executive update, a monthly business review, a quarterly outcome readout — and stick to it. Out-of-cycle requests are handled in a lightweight way, but the team's working time is not consumed by ad-hoc reporting.

---

## Tooling

The method is not about tools, but a few practical notes on what supports it well.

**Whiteboards and walls.** Physical or virtual. The hypothesis, the assumptions, the MVPs, the learning loops all live on a wall the team can see daily. Tools that hide this in shared documents reduce the visibility and the work suffers. If remote, use a persistent collaborative whiteboard with the same content always at the same URL.

**Prototyping tools.** Whatever lets the designer move from sketch to clickable in an hour, not a day. The specific tool matters less than the loop speed it enables.

**Analytics.** The team has live access to the metrics it cares about. Not a quarterly report from a centralized analytics team. Dashboards the team can look at every morning. Otherwise, the outcome side of the loop is too slow to be useful.

**Issue tracking.** The team's backlog includes stories, design debt items, hypotheses being tested, and instrumentation tasks. The categories are visible so the team can see whether it is over-indexed on features and under-indexed on learning.

**Communication.** A team channel where the team works visibly. Research findings, design iterations, build progress, metric updates all flow through it. Stakeholders who need to follow along subscribe; the team does not produce a separate stream of stakeholder-friendly updates.

The principle behind all the tooling choices: prefer tools that put the work in the open and that minimize the cost of the next iteration. Heavy tools — complex project management software, formal design hand-off systems, ceremony-heavy review workflows — slow the loop. The team that fights for fast tools is fighting for the work.

---

## Scaling to multiple teams

The method is designed for one team. When the organization grows past one team, the method must be adapted, not abandoned.

**Each team owns an outcome.** When you have ten teams, each one is responsible for a different outcome metric. The outcomes are mapped to the overall company strategy at the top, and each team has a clear line from its work to a strategic objective. Without this clarity, teams compete for the same scope and step on each other's work.

**Coordination layer, not control layer.** The cross-team coordination is about information flow, not approval. A weekly forum where teams share what they are testing, what they have learned, what they need from other teams. Decisions remain within the teams; coordination ensures the teams are not duplicating effort or contradicting each other.

**Shared infrastructure.** Multiple teams running research need a shared research repository, shared recruiting pipeline, shared instrumentation tooling. Building all of this per team is wasteful; building it as shared infrastructure that each team uses is efficient.

**Shared vocabulary.** Hypotheses, outcomes, MVPs, learning loops — the terms mean the same thing across the organization. New team members are trained in the shared vocabulary so that conversations across teams do not require translation.

**Communities of practice.** Researchers across teams meet. Designers across teams meet. Engineers across teams meet. The communities share craft, tooling, and patterns. They are not management structures; they are peer learning networks that strengthen the practice at the discipline level.

The risk at scale is process bureaucracy — the method that worked for one team gets formalized into rules and ceremonies that slow ten teams down. Resist this. Keep the practice principles strong; let the specific implementations vary by team. The principle is "outcomes over outputs," not "every team must use the same template."

---

## A working week, in shape

To make the model concrete, here is what a healthy week looks like on a team practicing this well.

Monday: sprint kickoff. The team reviews the hypothesis the sprint is testing. Engineers and designers pair on the first story. A designer and a researcher recruit two users for Wednesday and Friday sessions.

Tuesday: design studio for the next bet. The team has identified the next big question after the current sprint, and an hour is invested in collaborative sketching. The designer takes the result and tightens it into a prototype overnight.

Wednesday: user session on the in-progress prototype. The whole team attends. 30 minutes of conversation, 30 minutes of team debrief immediately after. One specific change goes into Thursday's work.

Thursday: build and learn. Engineers ship. Designer refines. Two more user contacts happen.

Friday: outcome review. What did we ship? What did the metrics do? Did the hypothesis hold? What is the next bet? Update the wall. Reset for Monday.

That is the rhythm. Not heavy. Not ceremonial. Continuous, deliberate, small. The compound effect over a quarter is enormous, and it is what makes this method worth running.

---

## Common failure modes and their fixes

A few patterns appear in nearly every team that adopts this method and gets it partly wrong. Naming them in advance makes them easier to catch.

**The "research theater" failure.** The team holds weekly research sessions, but the sessions are scripted to confirm what the team already decided. The questions are leading. The recruiting is biased toward users who already love the product. The debrief consists of nodding at the parts that worked and ignoring the parts that didn't. The cure: write down what would change your mind before the session. If the session produces nothing that would change your mind, the session was theater.

**The "MVP that isn't"** failure. The team ships a "minimum viable product" that is in fact a six-month build of the first slice of the eventual product. There is nothing minimum about it. It tested no hypothesis because the team did not write a hypothesis before building. The cure: name the hypothesis first. Then ask what is the smallest possible test that could falsify it. If the smallest test is a six-month build, the hypothesis is wrong-sized; break it into smaller hypotheses.

**The "shipped equals done" failure.** A story moves to "done" when the code merges. The team celebrates velocity. Nobody checks whether users are doing what the story was supposed to make them do. Six months later, the team realizes that half the features it shipped did nothing for the business. The cure: definition of done includes the outcome metric. The story is not closed until the metric has been observed.

**The "designer in a cave" failure.** Despite all the rhetoric about collaboration, one designer in the team still owns all design output and produces it solo, away from the rest. The studios are theater; the actual design happens in the designer's head. The cure: the studio output is the starting point for the design, not a discardable warmup. The designer carries the studio direction forward; if they change direction, they explain why to the team.

**The "Gantt chart in disguise" failure.** The team says they run Lean UX. The artifacts on the wall include a quarterly plan with feature dates. The dates are sacred; the hypotheses are decorative. Leadership rewards hitting dates regardless of outcomes. The cure: explicit leadership change. The funding model and the review process must reward outcomes. Without that change, the method cannot survive.

**The "lab rat" failure.** The team runs lots of small experiments, but no single experiment is meaningful enough to move a metric. The team produces a churn of small wins and small losses with no overall direction. The cure: occasional bigger bets. Some experiments must be at the level where, if they work, the product is meaningfully better; if they don't, the team has learned something significant. Always-small is a way to avoid risk while feeling busy.

**The "research as a stage" failure.** The team treats research as a step that ends before build starts. "Research is done; now we build." The cure: research never ends. The team is always in the field. The build phase has research running in parallel — small sessions on in-progress prototypes, ongoing user contacts, continuous observation. Research is not a phase; it is a posture.

---

## How this fits with other methods

The method does not exist alone. It connects to and supports other ways of working. Understanding the connections sharpens the practice.

**With agile.** Agile gives the cadence and the ceremonies. Lean UX gives the substance of what the team works on during each iteration. Agile without Lean UX produces predictable delivery of features that may or may not matter. Lean UX without agile produces good thinking that does not ship reliably. They need each other.

**With design thinking.** Design thinking, fully practiced, includes the discovery and framing work — empathy, problem definition, ideation, prototyping, testing. Lean UX uses the same building blocks but runs them in a tight, continuous loop rather than a sequenced project. Design thinking workshops are a useful intervention at the start of a major initiative; Lean UX is the ongoing day-to-day after the workshop produces an opening direction.

**With lean startup.** Lean startup contributed the validated-learning posture, the build-measure-learn loop, the pivot-or-persevere decision. Lean UX is the design and product practice that operationalizes those ideas for a product team. You can think of Lean UX as lean startup applied to the design discipline.

**With outcome-driven roadmaps.** A roadmap built around outcomes — quarterly bets on user behavior changes — is the planning artifact that complements Lean UX delivery. Feature roadmaps and Lean UX work against each other; outcome roadmaps and Lean UX work together.

**With OKRs.** Quarterly objectives and key results, when written well, name the outcomes a team is pursuing. Lean UX is one way to actually achieve those outcomes. The OKR is the destination; Lean UX is the way the team walks there. Badly written OKRs that name outputs ("ship three features") undercut Lean UX; well-written OKRs that name outcomes ("increase weekly active partners by 20%") reinforce it.

**With service design.** When the product extends across multiple touchpoints — software, human service, physical experience — service design tools (journey maps, service blueprints, role definitions) layer on top of Lean UX. The hypothesis-driven posture remains; the artifacts get more comprehensive to handle the cross-touchpoint nature of the work.

---

## Roles in detail

The named roles in a Lean UX team are deliberately fluid. The work is collaborative; the roles describe what each person contributes most, not what they exclusively own. A few notes on each.

**The product manager.** Holds the strategic direction. Writes the hypotheses that frame each sprint or quarter. Owns the outcome metrics. Removes obstacles for the team. Talks to stakeholders so the team doesn't have to. Does not write specifications; the hypothesis is the specification. Does not control the design; the team designs collaboratively.

**The designer.** Carries the most visual and interaction craft on the team. Is the single point of authority on the visual direction and interaction patterns. Pairs with engineers throughout the build. Sketches in design studios and converts the studio output into the artifacts that get tested. Spends most of their time in the team's workflow, not in a separate design tool. Does not produce 90-page specifications. Their artifacts are sketches, prototypes, and code-friendly handoff materials.

**The engineer.** Builds the artifacts that the team tests and ships. Participates in design — sketches, critiques, helps the designer understand feasibility. Pairs with the designer on screens. Watches user research sessions. Owns the instrumentation that measures the outcomes. Is not a service provider implementing handed-off specs; is a peer who contributes to the design and product decisions.

**The researcher.** When the team is large enough to have a dedicated researcher, they own the recruiting pipeline, the conversation protocols, and the synthesis of findings. When the team is small, the designer or product manager runs research with the team's help. Either way, the researcher (or research function) makes sure the team is in front of users continuously and that the learning compounds.

**The taste-keeper.** On some teams this is the designer; on others, the product manager; on others, a senior leader who reviews regularly. The taste-keeper holds the bar on quality and on direction. They are the person whose call ends the conversation when the team is stuck on a design or product decision. Their authority is earned by being right often and by reasoning clearly.

These roles overlap heavily on a small team. One person may be the product manager, the researcher, and the taste-keeper. The point is not strict role separation; the point is making sure every responsibility is owned by someone, even if the same someone owns several.

---

## The shortlist

If you remember nothing else from this file, remember these.

- Outcomes, not outputs. Measure what changed for users, not what you shipped.
- Every meaningful design decision is a falsifiable hypothesis written in the standard template.
- Research is continuous, weekly, and attended by the whole team.
- MVPs are the smallest learning instrument, not the first feature.
- The design studio kills both groupthink and design-by-committee.
- Sprint zero produces five artifacts on a wall: problem, assumptions, hypotheses, MVPs, learning loops.
- The team is funded in time-boxed bets against outcome targets, not in project budgets against plans.
- Failed hypotheses are the goal. Teams that never fail one are running the wrong tests.
- "Lean UX" is not a license to skip rigor. The rigor is the method.
- If a stakeholder asks for a Gantt chart, the work becomes a Gantt chart. Hold the line.
- Definition of done includes the outcome metric. Code-merged is not done.
- The taste-keeper holds the bar. Without one, design loses spine and becomes committee-shaped.
- Watch for research theater, MVPs that aren't, Gantt charts in disguise. Catch them early.
