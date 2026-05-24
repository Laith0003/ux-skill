# Lean UX Research — Faster, Smarter, Smaller

## What this is for

This is the research playbook for a team that does not have a research department, does not have a year, and cannot afford to be wrong about whether anyone wants the thing.

You will learn three things here. The questions every product must answer. The loop that produces those answers without burning a quarter. The methods that work on a startup budget and the traps that look like methods but aren't.

Use this when the product is new, the audience is partly hypothetical, and the cost of building the wrong thing is higher than the cost of asking. Skip the parts you have already answered with hard evidence. Run the rest cheap and often.

---

## Three research questions every team must answer

Every product question, at every stage, reduces to one of three. Knowing which one you are answering tells you which method to reach for.

### 1. Should I build this?

The hardest and earliest question. Is this a real problem that real people will pay you, in time or money or attention, to solve? Does the problem hurt enough that someone is currently solving it badly with a spreadsheet, a WhatsApp group, a printout, or a series of resentful workarounds? Is the segment that has this problem large enough and reachable enough to matter?

Wrong answers here cost you the whole company. Right answers here are worth more than any other piece of research you will ever do. Treat them with proportional respect.

You answer "should I build this" with conversations, not surveys. With observation, not opinion. With a focus on what users do today, not what they say they would do tomorrow.

### 2. Did I build it well?

You decided to build the thing. Now you need to know whether the version you built works for the people you built it for. Can they accomplish the task? Do they understand the language? Do they find the buttons? Do they recover from errors? Do they feel calm or harried?

You answer "did I build it well" with usability testing, prototype reviews, and direct observation of users in the live product. You answer it continuously. The first version is never the last.

### 3. Are people using it?

The hardest answer in production. You shipped. Someone uses it. Does anyone use it again? Does the segment you built for actually engage? Are the people you reached the ones you wanted to reach? Are the outcomes you predicted appearing in the data?

You answer "are people using it" with analytics paired to qualitative conversations. Numbers alone tell you that something is wrong; conversations tell you why.

Most teams confuse the three. They run a usability test ("did I build it well") when the real question is "should I build this at all." They run a survey to validate demand ("should I build this") when only behavior can tell them. They look at analytics ("are people using it") and call it research, when analytics without conversations is just a Rorschach test.

Name the question first. Then pick the method.

---

## The lean research loop

The loop has six steps. You run it constantly. The cadence is weekly, sometimes daily. The whole team participates.

**Hypothesize.** State what you believe, who you believe it about, and what you think will happen. Write it down. A hypothesis you have not written is not a hypothesis — it is a feeling.

**Research.** Pick the smallest, cheapest method that can confirm or kill the hypothesis. The method is determined by the question.

**Decide.** Look at the evidence. Decide. Pivot, persevere, or refine. The decision is recorded — what did we believe before, what do we believe now, what is the change.

**Build.** Build the thing the decision implies. Small slice. Behind a flag. Instrumented.

**Measure.** Observe the outcome. Quantitative metrics paired to qualitative observation. Did the change you predicted happen?

**Repeat.** Form the next hypothesis. The cycle restarts.

The loop is the work. Anything that does not feed the loop is not work — it is theater. A 60-page research deck that does not change any team decision is a piece of theater. A two-paragraph debrief that produces a clear "we will change this on Friday" is the work.

---

## Customer interview methodology

The interview is the foundational method. Done right, it produces more usable insight per hour than any other research activity. Done wrong, it produces nothing but reassurance.

A few hard rules.

**Behavior over opinion.** People are bad at predicting what they will do. They are reasonable at describing what they have done. Push every question back into the past. "Tell me about the last time you needed to do this" is worth ten times "would you use a feature that does this."

**Recent over typical.** "What do you usually do" gets you a sanitized story the user has told themselves. "Walk me through the most recent time" gets you the actual story, with the mess intact.

**Open-ended over leading.** "What happened next" beats "and were you frustrated by that." Your job is to make the user fill the silence. Their words are the data. Your words are pollution.

**Context over abstraction.** If you can run the interview in the user's actual workplace, with the actual tool, on the actual problem in front of them, do it. The lab interview tells you what the user thinks they think. The contextual one tells you what they actually do.

A working interview structure, 30 to 45 minutes.

*Opening, 5 minutes.* Warm up. Explain the format. Lower the stakes — "we are early, we are figuring it out, your honesty helps us more than your politeness." Establish that there are no wrong answers.

*Recent-event probe, 15 minutes.* "Tell me about the last time you tried to do X." Then shut up. Then ask "what happened next?" Then shut up. Resist the urge to fill silence — silence is where the real answer comes out. Stay with one specific instance. When the user generalizes ("I usually..."), pull them back to the specific event ("the last time, specifically, what did you do?").

*Pain probe, 10 minutes.* Inside the story they told you, find the worst moments. "When you hit X, how did you feel? What did you do? What would have made it better?" Pain is the signal. A user who shrugs at a workflow will not pay for the fix. A user who curses at it might.

*Workaround probe, 5 minutes.* People who have a real problem build workarounds. The spreadsheet, the WhatsApp thread, the printout. Workarounds are gold. They tell you that the pain is real, what the user values, and what the minimum acceptable solution looks like. "How do you handle that today?" — followed by silence — is your most productive sentence.

*Closing, 5 minutes.* Ask if there's anything you didn't ask that you should have. Thank them. Note their permission to follow up.

What you do not do. You do not pitch your solution in the interview. You do not describe your roadmap. You do not show them comps. You are there to learn what is true, not to test what you wish were true. If you find yourself talking, you are doing it wrong.

---

## Problem interview vs solution interview

These are different sessions with different agendas. Mixing them is a common mistake.

**The problem interview** comes first. You are validating that the problem exists, that it is painful enough to warrant attention, that it is happening to the segment you think it is happening to, and that the current ways of solving it are insufficient. There is no product yet. You ask only about the user's world. You leave with a sharper picture of who hurts, where, and how badly.

Signals you ran a good problem interview: you can describe the user's workflow in their words. You can name the specific moments of pain. You can point to a workaround. You can describe what triggers the problem to flare up. You found out something you did not already believe.

**The solution interview** comes after you have a candidate solution worth testing. Now you show — a sketch, a prototype, a description, a demo — and you watch the user react. You learn whether the solution lands, whether it is comprehensible, whether the user can imagine using it, whether they would pay (in money, time, or behavior change) for it.

Signals you ran a good solution interview: you watched the user try to use the thing, not just hear about it. You found at least one part that confused them. You found at least one part that surprised them positively. You came away with a list of changes.

A common failure: running a solution interview when the problem is not validated yet. The user is too polite to say the problem isn't real, and so they react to your prototype as if the problem were real, and you walk away believing you have product-market fit when you have only polite people. Always validate the problem first.

---

## Recruitment

Finding the right users to talk to is half the research. Talking to the wrong users is worse than not talking at all — it produces confident wrong answers.

**Where to find them.** Existing customers (best signal, easiest to reach, but biased toward the ones who already love you). Inactive customers (highest learning value; they tell you why your product failed them). Prospects from your top-of-funnel (they tell you what almost-customers think). Niche communities — forums, subreddits, professional groups, industry groups — where your target user already gathers. Referrals from existing users (warm intro, lower no-show rate). Cold outreach with a strong screener and an incentive.

Public recruitment platforms are a fast path when you cannot reach the segment otherwise. Treat results with appropriate skepticism — recruited panelists are a different population than organic users.

**Screener design.** A screener is a short questionnaire that filters the population down to the segment you want. Two rules. First, the screener tests for behavior, not identity. "How many times in the last month did you do X?" is a behavior screen. "Are you the kind of person who values X?" is an identity screen and useless. Second, the screener does not telegraph the answer. If the screener asks "do you struggle with X?" everyone says yes. Ask about the underlying behavior and infer.

A working screener has five to seven questions, takes the user two minutes, and produces a clean yes/no on whether to invite the user to a session.

**Incentives.** Pay your users. Cash, gift cards, account credits, or a charitable donation in their name. A free 30-minute conversation costs the user real time and they deserve compensation. The exception is when you are interviewing existing customers about a product they love — many will do it for free, but offer anyway. Pay at a rate consistent with the user's professional value of time; underpaying produces a self-selected pool of the unemployed and undermotivated.

**Scheduling.** Default to short, frequent sessions over long, rare ones. Five 30-minute sessions per week, in two slots a day, beats one 90-minute session per month every time. Use a scheduling tool that lets the user pick their own time. Confirm 24 hours in advance. Expect 20% no-show on cold recruits, near-zero on warm referrals.

---

## Survey design — and when not to

Surveys are useful for a narrow band of questions. They are dangerous when applied outside that band.

**Use surveys when** you need to confirm a quantitative pattern across a large population, validate the prevalence of something you already heard qualitatively, segment a known user base by attribute, or measure a specific metric over time. Surveys are good at "how many" and "how often" once you already know "what."

**Do not use surveys to** discover unknown problems, validate demand for a product nobody has used yet, predict whether someone will adopt a behavior, or substitute for a conversation. Surveys do not produce discovery; they produce confirmation or refutation of what you already suspected.

A few biases to refuse.

**Leading questions.** "How satisfied are you with our excellent new feature?" leads. "Tell us about your experience with the new feature" does not. Phrase every question neutrally. If a question has a tone, rewrite it.

**Satisficing.** Users on surveys take the path of least cognitive effort. They will click "agree" on a long scale to be done with it. The defense is short surveys, mandatory open-ended answers on critical questions, and removing the option that lets them coast (the middle position on a five-point scale, the "neither agree nor disagree").

**Sample bias.** The users who fill out your survey are different from the ones who don't. They are more engaged, more opinionated, more invested. Caveat every finding with the awareness that you heard from the loud, not the silent. Cross-check with behavior data.

**Loaded scales.** A scale that runs "Strongly agree, Agree, Neutral, Disagree, Strongly disagree" measures something different from one that runs 0 to 10. Pick the scale that fits the construct, document the choice, and do not switch scales mid-program.

**Forced choice on poorly understood options.** Asking users to rank features they have never used produces noise. Ask about behavior they have, not preferences they don't.

Survey discipline: short, behavioral, neutral, anonymous when honesty is at stake, attributable when follow-up is needed. Ten well-designed questions beat 40 messy ones. Send fewer surveys. Make them count.

---

## Usability testing on a tight budget

The single highest-leverage research method per dollar. You can run it on a clickable prototype. You can run it on a coded build. You can run it on the live product. You should run it constantly.

**Five users per round.** This is not a budget compromise; it is a statistical finding. Five users will surface the vast majority of meaningful usability issues. The sixth, seventh, eighth user mostly confirm what the first five found. Spend the money on more rounds, not more users per round.

**Low-fi over high-fi early.** A grayscale clickable wireframe lets users react to the structure without getting distracted by the visual. High-fidelity comps cause users to comment on color and font — useful sometimes, distracting often. Save the polish for the round that needs it.

**Frequent over thorough.** Three rounds of five users each, each round following a real iteration, beats one round of 25 users on a single version. The learning compounds: round two tests the fixes from round one, round three tests the fixes from round two.

**The task, not the interface.** Give the user a goal, not instructions. "Sign up for the loyalty program" is a task. "Click the button at the top, then click the second option" is theater. The point is to see whether the user can accomplish the task; if you have to tell them how, the test failed before it started.

**Think-aloud protocol.** Ask the user to narrate. "Tell me what you are looking at. What are you trying to do? What do you expect to happen when you click that?" Their narration is the data. Silence in a usability test is bad — it means the user has gone internal and you are learning nothing.

**Do not lead.** When the user gets stuck, do not save them. Wait. Watch what they try. Note where they get stuck. If they ask "is this where I would do X?" — turn it around: "where would you expect to find that?" Their answer is the data you came for.

**Run the team in the room.** Engineer, designer, PM all watch. Live, if possible — observation room or screen share. The team that watches the user struggle with the button they built builds a different button next time. The team that reads the report does not.

**Debrief immediately.** Five minutes after the user leaves. What we expected, what we saw, what surprised us, what we will change. The notes are the artifact, not a 30-page report.

---

## Analytics and qualitative paired

Either alone misleads. Together they triangulate.

**Quant tells you what.** Funnel data tells you 60% drop on step two. Engagement data tells you a feature is used by 8% of weekly actives. Cohort retention tells you that the users acquired in March are dropping off faster than the ones from February.

**Qual tells you why.** You watch a user hit step two and freeze because the language confuses them. You ask the 8% why they use the feature and learn that they all share one specific job role. You interview five March cohort users and discover an onboarding email broke that month.

The discipline is to never publish a quantitative finding without a qualitative answer attached, and never publish a qualitative finding without checking whether it scales quantitatively. The 60% drop is a hypothesis until five user sessions tell you why. The "users hate the wizard" anecdote is gossip until the analytics show it correlates with churn.

A working cadence. Once a week, look at the dashboards. Find the three most surprising numbers. For each, recruit two users from the relevant cohort and run a 20-minute conversation. Bring the qualitative findings back to the dashboard. Update the team's mental model. Repeat.

---

## MVP testing methods

Cheaper than building. Used to answer "should I build this" before you build it.

**Smoke test.** Run real ads against a real landing page describing a product you have not built. Measure click-through to signup. If nobody clicks, the value proposition does not land — and you have not written a line of code. Budget: tens to low hundreds.

**Concierge MVP.** Deliver the service by hand to a small number of users. No software, no automation. The user gets the outcome, you learn what the workflow actually looks like, what edge cases matter, what language the user uses. Three to ten users. Budget: your time.

**Wizard of Oz.** The interface looks real but the back-end is you, manually. Useful when the value proposition depends on a technical capability you have not yet built (search, matching, recommendation, generation). The user experiences the product; you learn whether it lands before you invest in the build. Caveat: brittle at scale, run it on five to twenty users, not five hundred.

**Fake door.** A button in the live product that goes to a "coming soon" page. Measures intent to use a feature that does not yet exist. The signal is noisy — clicking is cheap — but useful when you need a directional read. Ethical note: do not leave fake doors up indefinitely; users notice and trust drops.

**Pre-order or paid waitlist.** Take money or a credit card hold for a product you have not finished. The strongest signal in research — willingness to pay before delivery. Best for products where the buyer can imagine the value clearly.

**Manual onboarding.** For early products, replace the automated onboarding flow with a human one. A 30-minute call to set up each user. You learn what users actually need help with, which becomes the spec for the automated flow you will build later.

Pick the cheapest one that can answer the question. Many founders skip to a full build because building is comfortable and asking is uncomfortable. The discipline is to be uncomfortable first.

---

## Common research traps

Recognize these in yourself and in your teammates.

**Confirmation bias.** You hear what you came to hear. The user mentions a frustration that fits your hypothesis and you note it; they mention three that don't and you don't. Defense: write down the hypothesis before the session, and explicitly note the moments that contradicted it. If a session produced no contradicting evidence, you probably missed it.

**Sample of the eager.** The users who show up to talk to you are the engaged ones, the loud ones, the ones who already like you. They are not your churners, your silent majority, your skeptics. Defense: actively recruit the people who left, the people who never converted, the people who use your competitor. Their data is what you need.

**Optimism on roadmap items.** Your team is excited about feature X. You run a session and ask users about it. They will mostly say nice things, because users are polite and your team is in the room. Defense: ask about the user's world, not your roadmap. If they bring up the problem your feature solves, unprompted, the signal is real. If they only validate it after you describe it, the signal is noise.

**Overgeneralizing from one user.** You ran a session, the user said something striking, the team got excited. One user is one data point. Two users saying the same thing unprompted is a signal worth investigating. Five is a finding. One is a story.

**Treating opinions as data.** Users will tell you what they would do, what they would pay, whether they would recommend you. Their opinions are not reliable predictors of their behavior. Behavior is data; opinion is hypothesis.

**Calling stakeholder reviews "research."** Showing the design to four colleagues and collecting their reactions is not research. It is internal review. Useful, sometimes, for clarity and morale; not a substitute for user research.

**Mistaking volume for signal.** Three thousand survey responses sounds impressive. If the survey was poorly designed, the responses are noise multiplied. A clean five-user usability test produces more usable insight than a sloppy five-thousand-user survey.

**The "interesting" trap.** A finding is interesting if it surprised you. A finding is useful if it changes a team decision. Many findings are interesting and not useful. Demand both.

---

## The fast cycles

Research that takes a quarter to complete cannot guide a sprint. The discipline is to run fast cycles, even at the cost of methodological purity. A few patterns that compress the cycle.

**Same-week recruiting.** When a question arises Monday, sessions are scheduled for Thursday and Friday. The week ends with new data. This requires a warm pipeline; without one, the cycle drags into the following week and the team has moved on by the time findings arrive.

**Three-session decisions.** For low-stakes design questions, three sessions are enough to reveal whether a pattern holds. The team observes session one, refines the question for session two, confirms the pattern in session three. Decision is made Friday afternoon based on what was seen Thursday and Friday morning.

**Continuous discovery.** The team has two standing sessions per week — every Tuesday and every Thursday, with users recruited fresh each week. The conversations are loosely themed but flexible; the most pressing question at the start of the week becomes the focus of that week's sessions. The continuous slot prevents research from becoming a thing the team has to schedule and start; it is always running.

**Lightweight prototyping.** Sessions can run on rough artifacts. A paper sketch, a clickable wireframe, a coded prototype, a live product. Lower fidelity is faster to build and faster to revise. Use the lowest fidelity that can answer the question.

**Decision in the room.** The team that watched the session debriefs immediately and makes the decision before the day ends. Not "let's circulate the findings and discuss next week." The decision is part of the session; without it, the cycle stretches and the work loses the freshness of the observation.

These compressions are not perfect methodology. They make trade-offs: smaller sample sizes, lower fidelity, faster judgment. The trade-offs are usually worth it for product decisions at this scale. A week-fast decision based on three sessions, with the team committed to revisiting if behavior in production contradicts the finding, is better than a quarter-slow decision based on twelve sessions that comes too late to act on.

---

## Reporting research

The output of a research session is a decision and a change, not a deck.

A working report format, used after every session or round, fits on one page.

*Question.* What were we trying to learn?

*Method.* How did we learn it? How many users, what type, what protocol.

*Findings.* Three to five bullets. Each one a behavior or pattern, in the user's words where possible. Not opinions — observations.

*Decision.* What we will change as a result. Concrete. Owner. Date.

*Open questions.* What we still don't know that this session didn't answer. Becomes the seed for next week's research.

That is it. No 50-page deck. No "executive summary" of a 50-page deck that nobody read. A one-page artifact, ten minutes to write, used as the change log of the team's thinking.

The exceptions: when research is being used to make a board-level bet or to coordinate a large organization, you may need a longer artifact. But the longer artifact is a derivative of the one-pagers, not a replacement. The team works off the one-pagers; the longer artifact serves the audience that does not work in the team.

---

## When to skip research entirely

The lean discipline is not "always do research." It is "do the right amount of research for the question."

You may skip research when the decision is reversible and the cost of being wrong is low. Changing a button color: probably don't run a study. Trying a new copy variant on a low-traffic page: just A/B test it.

You may skip research when the answer is already well established. There is a large body of evidence on basic usability patterns. Reinventing it on every project is a waste. Use what is known; spend research budget on what is unknown.

You may skip research when the bet is small enough that the cost of researching exceeds the cost of just trying. A two-hour engineering experiment may be cheaper to run than a two-hour user research session to decide whether to run it.

You should not skip research when the decision is hard to reverse, the cost of failure is high, the audience is one you have not validated with before, or the bet is large and built on assumptions. Those are exactly the moments you slow down and learn.

The skill is calibrating. A team that researches everything ships nothing. A team that researches nothing ships the wrong things. The discipline is to know which question you are answering and which method, including no method, is right for it.

---

## Research operations

The mechanics of getting research done are often what separates teams that run continuous research from teams that talk about it. A few operational practices to put in place.

**A standing recruiting pipeline.** You do not start recruiting when you need a user; you keep a pipeline always warm. Sources include past participants who agreed to follow-up, customer segments who opted in to be contacted, a public recruiting platform with active campaigns, and community channels where target users hang out. The pipeline is maintained as a living list — names added, names retired as they age, response rates tracked.

**Standard incentives.** Decide the rate the team pays and stick to it. A flat rate across most studies, with a higher rate for hard-to-recruit users (executives, niche professions, time-constrained roles). Negotiating incentives per session wastes time and creates inconsistency.

**A standard session structure.** Most studies follow a similar shape — opening, behavior probes, prototype walkthrough, debrief. The variation is in the specifics. A standard template that the researcher customizes for each study saves time and produces more comparable results across sessions.

**A research repository.** Every session is recorded (with permission), transcribed, and tagged. Findings are stored in a searchable repository so that future studies can build on past ones. Without this, every study restarts from zero and the institutional knowledge evaporates with personnel changes.

**A note-taking protocol.** Two people in each session: the interviewer (drives the conversation) and the note-taker (captures verbatim quotes and observations). The note-taker is essential; an interviewer trying to listen, ask, and write at the same time will lose data. Rotate the role so multiple team members build their interviewing chops.

**Debriefs immediately after.** Within 30 minutes of the session, the team that watched holds a 10-minute debrief. What was the strongest signal? What surprised us? What changed our mind? What is the action we are taking? Capture the answers in the repository. Do not let the day pass without debriefing; the memory degrades faster than you expect.

**Research review cadence.** Every two weeks, the team reviews accumulated findings. What patterns are emerging across sessions? Are there contradictions worth resolving? Are there hypotheses that the cumulative evidence has resolved? The review is when the small individual sessions integrate into bigger insights.

---

## Ethical research

The user agreed to talk to you. That trust is the most valuable thing the research operation has. Protect it.

**Informed consent.** Users know what the session is for, how the recording will be used, who will see it, how long their data will be retained. Consent is given explicitly, not buried in a long form. The user can withdraw at any time, including after the session.

**Minimum data.** Collect only the information you actually need for the research. A user's name and contact information for follow-up is needed. Their full address, demographic details unrelated to the study, and personal histories generally are not. The more you collect, the more risk you carry.

**Confidentiality of identity.** When findings are shared inside the team, the user's identity is protected. Use pseudonyms or codes in shared notes. The video is access-controlled. Quotes are attributed by role, not by name.

**No dark-pattern recruiting.** Some platforms incentivize the user to give the answer the researcher seems to want. A user who is told "we are testing a feature for power users" will perform as a power user. Recruit and frame neutrally; describe the study without giving the user a script for how to behave.

**No coercion.** Existing customers are sometimes recruited via the product itself — a prompt that appears in the live experience. Make these opt-in, with no penalty for declining. A customer who feels pressured into a session will give you compliance data, not honest data.

**Respect the user's time.** Sessions start on time and end on time. The user is paid promptly. Follow-ups happen when promised. The user leaves the session feeling respected; they tell other potential participants that the experience was worth it. Word-of-mouth either fills your pipeline or empties it.

**Vulnerable populations require more care.** When the user is a minor, a patient, a person with disabilities, or someone in a precarious life situation, the protocols tighten. Specialized recruiting, specialized consent processes, and sometimes specialized researchers are needed. Do not run on these populations with the same approach you use for general consumer research.

---

## Building research into the team culture

The hardest part is not knowing how to do research; it is making research a habit. A few cultural moves that help.

**Everyone watches research.** Engineers, designers, product managers, marketers, support staff all watch sessions regularly. Watching is not optional. The team that watches sees the user; the team that reads a report imagines the user. Imagination is wrong more often than direct observation.

**Research findings drive decisions, visibly.** When a decision is made, the team cites the research that informed it. "We chose to ship X because in seven sessions we saw Y." This habit makes research operationally relevant; without it, research becomes a sideshow that the team performs while making decisions on intuition.

**Failed predictions get celebrated.** When a team member says "I thought X, but the research showed Y," that admission is rewarded, not punished. The culture that punishes wrong predictions also punishes honest research; the team learns to make safe predictions that the research confirms, and the research stops being useful.

**Disagreement with research is resolved by more research.** When the team and the research disagree, the response is not "ignore the research." It is "run more research, sharper this time." Sometimes the original research was flawed. Sometimes the team's intuition was. The way to find out is to look again with better methods.

**Junior team members are trained to run research.** Not just senior researchers. The interview is a skill that improves with practice. Junior team members get coached through their first ten interviews; by the twentieth they are competent; by the fiftieth they are good. The pipeline of skilled interviewers is what scales the research function over time.

---

## When findings contradict the stakeholder

Sometimes the research produces a finding that a stakeholder does not want to hear. The CEO has bet on a direction; the research suggests that direction is not landing. The product manager has championed a feature; the research suggests users find it confusing.

The team's job is to surface the finding clearly and to support the conversation that follows. A few practices that make this go well.

**Surface early, not late.** The earlier the stakeholder learns about a contrary finding, the easier it is to adjust. Late surprises produce defensive reactions. Build a rhythm where stakeholders see the research as it emerges, not only when the team has a fully formed contrary view.

**Lead with evidence, not interpretation.** Present what was observed before presenting what the team thinks it means. "In seven of eight sessions, users took longer than two minutes to find the rules-setup option. Six of eight users reported they couldn't tell what 'rules' referred to." The numbers and behaviors come first; the team's recommendation follows.

**Distinguish observations from extrapolations.** Some findings are direct observations of behavior; others are extrapolations the team made from limited data. Be transparent about which is which. A stakeholder who pushes back is more likely to be pushing back on an extrapolation than on an observation.

**Offer alternatives, not just objections.** If the team disagrees with a stakeholder's direction based on research, the team also proposes what to do instead. "We don't think feature X will land for the reasons above; based on what we've learned, we propose Y as a better bet." A team that only says "no" loses influence; a team that says "no, and here is yes" builds credibility.

**Respect the stakeholder's judgment.** Sometimes the stakeholder will override the research and proceed. That is their call to make. The team's job is to make sure the stakeholder is making the call with full information, not in ignorance of the research. If they make the call anyway, the team executes. The research record is preserved; if the prediction proves correct, the team and the stakeholder both learn from it.

---

## Common methodological mistakes

A few specific errors that researchers and product teams make repeatedly.

**Sample size confusion.** Five users per round is correct for usability testing. Five users is not enough for quantitative survey work. The two methods have different sample size logic; using one method's rules for the other produces bad research.

**Aggregating heterogeneous users.** Five users of widely different roles, contexts, and use cases are not five data points; they are five separate single-user studies. The team that treats them as a single sample produces confused findings. Either sample within a single segment or run separate analyses per segment.

**Confusing usability with desirability.** A user who can complete a task does not necessarily want to complete the task. A usable feature is not the same as a desirable one. Test for both, with different methods. Usability tests answer "can they?" Desirability research answers "would they?"

**Overweighting the most vivid story.** One user told a compelling story; the team rewrites the strategy. Compelling stories are anchors that can pull a team off course. Look at the pattern across users, not the single most articulate one.

**Forgetting the population.** A finding from research applies to the population that was studied. If you ran sessions with power users and found a pattern, that pattern may not hold for casual users. Always note the population, and resist the urge to generalize beyond it.

**Treating the prototype as the product.** Users react to prototypes differently than to live products. A prototype that performs well may not predict a product that performs well; the conditions differ. Treat prototype results as directional, and verify with live results once shipped.

---

## The shortlist

If you remember nothing else from this file, remember these.

- Three questions: should I build this, did I build it well, are people using it. Always name the question first.
- The loop is hypothesize, research, decide, build, measure, repeat. Weekly. Whole team.
- Interview about behavior, not opinion. Past events, not predictions. Specific instances, not generalizations.
- Problem interview before solution interview. Validate the pain before showing the cure.
- Five users per round. Many rounds. Low fidelity early. Whole team in the room.
- Surveys confirm; conversations discover. Do not mix them up.
- Quant tells you what, qual tells you why. Always pair them.
- MVPs are learning instruments, not first releases. Pick the cheapest one that can answer.
- One-page reports with decisions, not 50-page decks.
- Skip research when the answer is known or the bet is small. Slow down when it isn't.
- Build a warm recruiting pipeline before you need it. Recruitment delays are the most common research bottleneck.
- Insist on the debrief within 30 minutes. The memory degrades faster than you expect.
- Pair an interviewer with a note-taker. Trying to do both produces worse data on both.
- Run the team in the room. The team that watches the user changes more than the team that reads the report.
- Tag and store every session in a searchable repository. Institutional memory is an asset; treat it that way.
- When findings contradict a stakeholder, surface early, lead with evidence, and offer alternatives.
- Five users for usability, larger samples for prevalence. Do not confuse the rules.
- Continuous research, not phased. Two standing sessions per week beats a quarterly study.
- The cycle should compress to a week when the question is small. Quarterly research cannot guide a sprint.
- Protect the trust of users you recruit. Without trust, the pipeline empties and the research operation dies.
