# Creative Selection — Taste-Driven Product Development

## What this is for

Creative selection is the working method behind product design that has a spine — design that feels like one mind made every decision, even though many people contributed. It is not a methodology of process diagrams and ceremony. It is a culture: a way of running the work day-to-day so that the artifact, not the plan, is the unit of progress.

Use this when you are designing something where the difference between "fine" and "great" matters. When the work needs taste. When you can feel that committee-driven design will produce something soft and shapeless and you want to prevent that.

This method is small-team-shaped. It scales by being run many times in parallel, not by adding people to a single instance of it.

---

## The core principle: iterate on a thing, not a plan

The single principle that distinguishes this method from everything else: you iterate on a concrete artifact, not on a plan to make the artifact.

A plan is words about a thing. The thing is the thing. The thing can be reacted to — a person looking at it has an immediate, visceral, honest response. The plan can only be imagined, and imagination is full of charity. Everyone imagines the plan working out fine. Then the artifact arrives and everyone sees that it doesn't.

Building plans and reviewing plans feels like progress. It is not progress. The hours spent writing the document, presenting the slides, debating the bullet points, were hours not spent making the thing. When the thing finally arrives, every assumption that was charitably granted to the plan gets re-litigated against the artifact, except now you have spent the time and you have to ship.

The discipline is to convert plans into things as fast as possible. A sketch beats a paragraph describing a sketch. A clickable prototype beats a spec describing the flow. A working build beats a clickable prototype describing the interaction. Always push the work down the fidelity ladder toward a thing that can be reacted to.

This is not anti-thinking. The thinking is real. But the thinking shows up in the thing, not in the artifact that describes the thing. If you can write a 30-page document about a feature, you have done 30 pages of thinking. If you can make a working prototype of the feature, you have done more thinking, and you have a thing.

---

## Demo culture

The practical expression of this principle is demo culture. Every meeting that matters is a demo. Every milestone is a working artifact in front of a decision-maker. Every Friday — or Monday, or whenever the rhythm lands — the team shows what they have made since the last show.

The demo is not a presentation. A presentation is the maker explaining what they intended to make. A demo is the artifact itself, in the room, with the maker holding it so the decision-maker can see it and react. The decision-maker may speak less than the maker, and that is correct. The artifact is doing the talking.

A few rules for how the demo runs.

**Show, don't pitch.** The maker resists the urge to set up, contextualize, justify, or apologize. The artifact appears on the screen and the conversation starts. Setup time is wasted time. If the artifact needs ten minutes of explanation to be evaluated, the artifact is failing on its own.

**One decision-maker.** Demos are not committee reviews. There is one person whose taste call ends the conversation. That person is the same one each week. They build up context across demos and can hold the long arc. A rotating cast of reviewers produces inconsistent direction and the work loses spine.

**Direct, specific, kind.** The decision-maker speaks plainly. "This part works. This part doesn't. Here is what bothers me. Try this." Not "I wonder if perhaps we might consider whether possibly." Direct feedback is faster, clearer, and more respectful than padded feedback. The padding wastes everyone's time and obscures the actual signal.

**No notes by committee.** The maker does not collect a stack of feedback from six attendees and then "synthesize" it into next week's work. They listen to the decision-maker. Other voices in the room speak when they have something to add, not because the format requires their participation.

**Decisions made in the room.** The point of the demo is that the next move is decided before everyone leaves. Not "let me think about it and get back to you." Not "let's circulate it for review." Now, in the room, what is the next iteration. Walk out aligned.

**Cadence.** Weekly is a good default. Faster if the work is hot. Slower if the artifact takes more than a week to be ready for review — but be suspicious of that, and ask what would let you show something next week instead.

---

## Tightening feedback loops

The competitive advantage of this method is loop speed. The team that iterates daily beats the team that iterates monthly. The team that iterates hourly, on small things, beats the team that iterates daily.

Pay attention to the friction between "I made a change" and "I can see the change in context and decide whether it worked." Anything that adds time to that loop is the enemy.

Practical moves to tighten loops.

**Live preview, always.** The maker has the artifact open in a state where the change shows up immediately. Not "save, build, deploy, refresh, navigate, log in, navigate again, finally see the change." Every layer of pipeline between change and observation is a tax on the work.

**Small artifacts.** A small thing is faster to iterate on than a big thing. If the artifact is a whole product, the iteration cycle is too long. Break the artifact down: this screen, this interaction, this component. Iterate at the level where the loop is minutes, not hours.

**One artifact in flight at a time.** Holding two unfinished things in your head produces worse output on both than finishing one and then starting the other. The maker resists the temptation to parallelize their own work; the team parallelizes by having multiple makers, each working on one thing.

**The artifact comes first.** When the maker sits down to work, the first thing they do is open the artifact, not their email. The first move is to react to where the work stands. Everything else can wait.

**End each day with something visible.** Even if it is a snapshot of the in-progress state, push the artifact to a place where it can be seen. The next morning starts with a reaction, not a search.

Loop speed compounds. Halving the loop time means twice the iterations in the same week, which means the artifact reaches a much higher quality bar by week's end. Teams that fight for loop speed are doing the work of the work; teams that accept slow loops are losing weekly to teams that don't.

---

## The role of a strong decision-maker

The method requires one person, on each work stream, whose taste is the final word. Not a manager who manages. A taste-keeper who decides.

This is uncomfortable in some cultures. It feels hierarchical. It feels anti-collaborative. It is neither, when done well.

The taste-keeper is not the source of all ideas. They are the source of the final cut. Anyone on the team can propose a direction, sketch an option, advocate for a path. The taste-keeper listens to all of it and picks one.

The taste-keeper builds context over time. They know what the product is trying to be. They have seen what has worked and what has failed in previous iterations. They have the memory of all the directions tried and rejected. They are not running a poll; they are running a sustained editorial line.

The taste-keeper holds the bar. When something is good enough but not great, they say so. When something is great, they say so and ship it. They protect the team from the slow drift of "ship to hit the date" that erodes quality in a hundred invisible ways.

The taste-keeper is wrong sometimes. They make calls that don't work. The discipline is that when a call doesn't work, the team adjusts and tries again — not that the taste-keeper is removed and replaced with a committee. The committee will be wrong more often, and worse, with no spine to course-correct.

How the taste-keeper earns their authority is by being right often, by communicating their reasoning so the team can predict and learn it, and by showing in their own work what good looks like. Authority by org chart alone does not survive long under this method; the team will silently route around a taste-keeper who is not actually trusted.

---

## Avoiding frankenstein synthesis

The classic failure of design-by-committee. Six stakeholders review the work. Each offers a "small" change. The maker, trying to be inclusive, incorporates them all. The result is a frankenstein — a thing built from parts that belong to different bodies. It does not look like any of the six original suggestions. It does not look like the maker's original direction. It is a compromise that nobody wanted, and it looks like one.

The defense is to refuse synthesis at the point of feedback. The taste-keeper hears the suggestions, decides which one is right (often zero of them), and tells the maker the single direction to pursue. The maker does not try to honor all six voices. They pursue one direction with conviction.

When two strong directions are both worth pursuing — and they sometimes are — the answer is not to blend. The answer is to make two versions, see them both, and pick. Or to pick one for this iteration, ship it, and try the other next iteration if the first one doesn't fly. Never blend, because blending loses what is best about each direction and keeps what is worst.

A specific tell: when the maker shows a new iteration and the team can list which feedback note inspired which part, the iteration is a frankenstein. A coherent iteration has feedback woven into a unified vision; you cannot tear it apart and assign credit. If you can, the work was assembled, not designed.

---

## "What's the demo?"

The single most useful question in a team running this method. Said in any meeting, at any planning session, at any review.

"What's the demo?"

It means: what is the concrete artifact this work produces? Not the deliverable in the abstract. Not the slide that describes it. The thing the team will put in front of the decision-maker. The screen, the flow, the prototype, the working feature.

The question is useful because it forces the team off the plan and onto the artifact. If the answer is "well, we're going to investigate," the work is not ready to start. If the answer is "we'll have a clickable prototype of the redemption flow by Friday," the work has a shape.

It is also useful as a redirect when meetings drift. Someone is monologuing about the strategy. Someone is debating an abstraction. The question — what's the demo — pulls the conversation back to the artifact, which is where the value is.

A team that asks this question constantly converges faster. A team that doesn't ask it spends weeks on plans that produce nothing visible and then panics when the date arrives.

---

## Heroic effort plus small team

This method needs both. Take either away and it falls apart.

**Small team.** The team is small enough that the maker and the taste-keeper are in regular, frequent contact. Small enough that decisions made in a demo travel to everyone who needs to know within an hour. Small enough that there are no political layers between the work and the call.

A small team is faster, not because each individual is more productive, but because coordination overhead is lower. A team of five can hold a single mental model of the product. A team of fifty cannot, and so the fifty produce work that is internally inconsistent — pieces don't fit, languages clash, the spine of taste is broken across the seams.

When the work grows beyond what a small team can hold, the answer is not to grow the team. The answer is to split the work into pieces, each owned by a small team, with the connections between pieces well defined. The small teams stay small; the system gets larger by composition.

**Heroic effort.** The work demanded by this method is not low-effort. The maker is iterating constantly, paying attention to detail at a level that exhausts most people. The taste-keeper is holding the bar against a thousand small pressures to lower it. Everyone in the room cares about the work in a way that goes beyond job-shaped duty.

This is not about working long hours. It is about working with the right intensity in the hours you work. A maker who is half-present in their work cannot iterate fast enough to make the loop pay off. A taste-keeper who is hedging every call is not actually a taste-keeper. The energy required is real.

You cannot fake this. A team that goes through the motions — running the demos, doing the iterations, mouthing the principles — without the actual care, produces mediocre work. The principles are necessary but not sufficient. The care is the active ingredient.

Two implications. First, you protect your team's energy. Burnt-out makers do not iterate well. Burnt-out taste-keepers lower the bar. The pace must be sustainable across the long arc of the work. Second, you choose the work carefully. This level of intensity cannot be applied to every line of code. Pick the things that matter, apply the method there, and let the rest run on lighter discipline.

---

## Restraint as a design value

The dominant force in product design, unchecked, is addition. Every meeting produces requests to add features. Every stakeholder has an idea that would "just" add one more thing. Every quarter adds buttons, options, configurations, edge cases, dropdowns, screens.

The result is bloat. The product becomes harder to use, harder to maintain, harder to teach, harder to love. The original spine — the one thing the product was meant to do, done well — gets buried under accumulated additions, none of which were individually wrong.

Restraint is the counterforce. The question is not "what could we add" but "what doesn't earn its place." Every element of the design — every button, every option, every word — is on trial. It must justify its presence by what it adds, against the cost it imposes.

A few practical commitments to restraint.

**Default to no.** When a request comes in, the default response is "no" until the request earns "yes." The burden of proof is on the addition. This is uncomfortable; people are used to having their requests honored. But the team's job is to make the product great, not to make every requester feel heard.

**Subtract before adding.** Before adding a feature, look at what could be removed to make room for it. This isn't about literal physical space; it's about cognitive space. A user can only hold so many things at once. Each new thing crowds out an old thing. Make the trade explicit.

**Strip every screen.** When a design is mostly done, the maker asks: what can I remove? Not "what is necessary" — what is sufficient. The screen that has been stripped is faster to use, easier to teach, calmer to look at, and more likely to age well.

**Resist the "while we're at it." ** A change is being made to one part of the product. Stakeholders see the chance to slip in their pet feature "while we're at it." Resist. The change at hand should be done with a clear scope and shipped. Other features get their own decision.

Restraint is a discipline because addition feels productive and removal feels unproductive. The team that practices restraint must have a culture that rewards saying no, that celebrates the line of code deleted, that recognizes the feature removed. Without that culture, the gravity of addition wins and the product bloats anyway.

---

## The seven elements

Creative selection rests on seven traits that, taken together, define the working culture. Any team that runs this method should be cultivating all seven. Missing any one degrades the method.

**Inspiration.** The work begins with a vision of what something could be. Not what the spec says, not what the request describes, not what the competitor has — a sense of what the artifact, made well, would do for the user. Inspiration is not optional, and it cannot be manufactured by process. It is fed by paying attention to good work, in your field and outside it, and by spending time with users until you understand their world deeply enough to feel where the gaps are.

**Collaboration.** No one does this alone. The maker has a taste-keeper. The taste-keeper has makers. Engineers and designers pair on the artifact. Researchers feed the team's understanding of the user. Collaboration here is not "alignment meetings"; it is the substance of the work being done by multiple people in concert.

**Craft.** The artifact is made with care for its own quality. Not just "does it work" but "is it good." The interaction is smooth. The text is clear. The animation is timed right. The edge case is handled gracefully. Craft is what separates competent work from work that feels great.

**Diligence.** The hundredth time the maker reviews the artifact, they catch a thing they missed in the first ninety-nine. Diligence is the willingness to keep looking, to not declare done early, to sweat the detail that no one else will notice. It compounds: a hundred small acts of diligence produce a finished artifact that is qualitatively different from one made with ninety acts of diligence.

**Decisiveness.** The taste-keeper picks. The maker commits. The team moves. Indecision rots the work; every day spent not deciding is a day the iterations did not run. Decisiveness is not impulsiveness — it is the willingness to commit to a direction with the information you have, and to update when new information arrives. Hedging produces mediocre work.

**Taste.** The accumulated sense of what is good. Built over years of looking at things, making things, watching things succeed and fail. Taste cannot be taught directly; it can be developed by exposure to good work and practice in evaluating work. The taste-keeper has more of it; the maker is building it. The team's taste is more than the sum of individual tastes — it is a shared sense of what this product, specifically, should be.

**Empathy.** The user comes first. Not as a slogan but as a habit of imagination. The maker, while designing, holds the user in mind: their context, their constraints, their goals, their irritations. The decision-maker, while critiquing, asks "what is the user's experience of this." Empathy is what saves the work from being clever instead of useful, from being beautiful instead of usable, from being a designer's expression instead of a user's tool.

These seven traits are interdependent. Inspiration without craft is a sketch. Craft without taste is polish on the wrong thing. Decisiveness without empathy is cruelty. Collaboration without diligence is committee. The team builds all seven and balances them across each piece of work.

---

## Applying this to assistant-driven design

The method translates directly to working with an AI assistant on design and product work. The principles do not change; only the cast of characters does.

**Every command produces a concrete artifact.** Not "a plan to design the screen" — the screen. Not "a description of the flow" — a clickable representation of the flow. Not "thoughts about the visual direction" — three visual directions you can compare side by side. The assistant's output is an artifact, every time, even if it is rough.

**The user is the taste-keeper.** The human in the conversation is the one whose call ends the iteration. The assistant does not run a committee; it produces artifacts and listens for direction. When the user says "more like this, less like that," the assistant pursues that single direction, not a blend.

**Refuse to synthesize when the human gives mixed signals.** If the human says "make it more bold AND more refined AND more playful AND more serious," the assistant surfaces the contradiction rather than producing a frankenstein. "I can pursue any of these; they pull in different directions. Which one is the primary?" That is the discipline of creative selection in dialogue form.

**Tighten the loop ruthlessly.** The artifact is built fast enough that the user can react and redirect in minutes. If a request would take an hour to fulfill, the assistant produces a faster, lower-fidelity version that can be reacted to immediately, with the understanding that the higher-fidelity follow-up is next iteration. Loop speed is everything.

**One artifact in flight.** When the conversation has three half-finished directions, none of them improve. The assistant proposes which one to push to completion first, completes it, then comes back to the others. Multiple half-things produce no taste signal; one whole thing does.

**Restraint.** When the user asks for more — more options, more variants, more features — the assistant first asks whether something should come out to make room. Not always; sometimes the additions are right. But the question is asked, and the default leans toward less.

**Demo each turn.** The assistant ends each iteration with the artifact in a state the user can see and react to. Not "I'll have it ready by tomorrow." Not "let me think about it." Now, in this turn, the thing the user asked for, as concrete as it can be made.

The assistant working with a human in this method is closer to a fast, tireless maker working with a single taste-keeper than to a team of helpers running a committee. The conversation has spine because the human has spine; the artifact has quality because the loop runs hot.

---

## Critique, given and received

The demo culture lives or dies on the quality of the critique. Soft critique produces soft work. Cruel critique produces defensive work. The discipline is critique that is direct without being personal, specific without being prescriptive, and high-bar without being unrealistic.

**Critique what is on the screen, not what is in your head.** The reviewer responds to the artifact in front of them. They do not respond to what they wish the maker had built or what they had imagined the artifact would look like. The artifact is the artifact; respond to it.

**Describe before judging.** Before saying "this is wrong," say what you see. "The signup flow asks for the phone first, then sends a code, then asks for the name." That description anchors the conversation. The maker may say "that is not what we intended"; now the conversation is about the actual artifact, not about competing imaginations.

**Distinguish craft from direction.** "The animation is too slow" is craft critique — specific, fixable, narrowly scoped. "This is the wrong feature" is direction critique — broader, harder to act on, sometimes warranted. Make clear which one you are giving. Mixing them confuses the maker about what to change.

**Offer the constraint, not the solution.** "I want the user to feel calmer at this step" is a useful constraint. "Make the button blue" is a prescription that constrains the maker's space. The taste-keeper holds the constraints; the maker explores within them. When the taste-keeper specifies the solution, the maker becomes a hand and stops contributing taste.

**No "interesting."** Reviewers who say "interesting" without taking a position are not contributing. Interesting is not feedback. Push for a position: do you like it, do you not like it, does it work, does it not. The taste-keeper especially cannot hide behind "interesting."

**Receive critique without explaining.** When the maker is critiqued, they listen. They do not immediately explain why they made the choice they made. The explanation comes later, when needed. In the moment of critique, the maker absorbs the signal. The instinct to defend is the enemy of the work.

**Separate the work from the worker.** The artifact is critiqued. The person who made the artifact is not critiqued. "This signup flow is confusing" is fine. "You always make confusing signup flows" is not. Maintain this distinction; it is what makes high-bar critique sustainable over time.

---

## When the demo isn't ready

Sometimes the work isn't ready for the demo. The maker has not finished the iteration; the artifact is still too rough to react to. What then?

**Show what you have.** A rough artifact is still an artifact. The maker shows the in-progress state, with a brief setup about what it is and what it isn't. The taste-keeper reacts to what exists. The conversation is about what to do next, not about why the artifact isn't further along.

**Don't fake polish.** The temptation is to add cosmetic polish to a rough artifact to make it look "ready." Resist. The reviewer will react to the polish and miss the underlying decisions. Rough is fine; fake-polished is misleading.

**Diagnose why.** When a demo is consistently not ready, something is wrong. The work is too large for the cadence. The maker is being interrupted by other demands. The artifact requires too much setup to reach demo state. Find the cause; fix the cause; don't just demand "be ready next time."

**Move the cadence if needed.** If a weekly demo is consistently producing unfinished work, the cadence is too tight for the artifact type. Move to fortnightly. But keep the cadence regular; sliding demos based on readiness is worse than a longer regular cadence.

**Cancel rather than fake.** If there is nothing to show, cancel the demo. Use the time on the work. A canceled demo is honest; a demo where the maker fills the time with slides about what they would have built is theater.

---

## Working with engineers in this method

The maker, in many software contexts, is a designer-engineer pair. The two roles work closely enough that the boundary blurs. A few notes on the pairing.

**The designer and engineer sit together.** Physically or virtually, the two are in continuous contact during the work. The designer sketches; the engineer immediately considers feasibility and prototypes a version; the designer reacts; they iterate. The artifact gets built quickly because the loop between idea and code is one person away.

**Engineers contribute design decisions.** The engineer is not implementing handed-off specs. They are noticing where the design is overconstraining the system, where small design adjustments would unlock big implementation wins, where edge cases the designer didn't think about need handling. The engineer's voice in the design conversation makes the artifact better.

**Designers respect implementation reality.** The designer learns enough about the technology to know what is cheap and what is expensive. A design that requires re-architecting the database is more expensive than a design that uses an existing API. Designers who ignore this produce specs that don't ship; designers who learn it design solutions that fit the system.

**Both attend the demo.** When the artifact is demoed to the taste-keeper, both the designer and the engineer are there. The decisions made in the demo affect both their work. Hearing it secondhand produces drift.

**No "throw it over the wall."** The handoff phase, in this method, does not exist. The designer's work is not "done" when the engineer starts; both work together until the artifact ships. The end of the work is "ready for users," not "ready for engineering."

---

## When this method doesn't apply

The method is powerful but not universal. Recognize the conditions under which it does not apply.

**When the work is execution-only.** If the design is known, the implementation is well-understood, and the only question is who builds what by when, you do not need this method. Standard project execution is fine.

**When the team is too large.** This method needs a small team. If the work requires twenty people in coordinated motion, the demo culture breaks down — there are too many voices, too many parallel artifacts, too much coordination overhead. Either split the work into smaller team-sized pieces or use a different method.

**When the timeline is fixed and short.** This method involves iteration, and iteration takes time. A two-week deliverable with a fixed scope and no flexibility is not the right context. Ship the first viable thing and call it done.

**When the taste-keeper is absent.** Without someone whose taste call ends the iteration, the method has no spine. If the organization cannot designate or empower a taste-keeper, the method cannot run. Force the question: who decides? If the answer is "the committee," you are not running this method.

**When the user is highly heterogeneous.** This method works best when there is a clear target user with a clear set of needs. If the user base is so varied that no single artifact can serve all of them well, you may need a different approach — perhaps building configurable systems rather than opinionated artifacts.

**When craft is not valued.** If the buyer of the work doesn't care about quality — they buy on price, or on feature checklist, or on speed — investment in craft does not pay. The method optimizes for craft and decisiveness; if those are not rewarded, the investment is wasted.

Recognizing when not to use the method is as important as knowing how to use it. Force-fitting it to the wrong context produces worse outcomes than just running a different method honestly.

---

## A daily rhythm

The method translates into a daily rhythm that is repeatable, sustainable, and produces work. A simple template.

**Morning: react to the artifact.** The maker opens the work in progress and reacts. Yesterday's iteration is fresh; today's iteration begins by seeing where the artifact stands. The first hour of the day is spent in the artifact, not in email or meetings.

**Mid-morning: iterate.** Build on what was reacted to. Make the change. See the change. Make the next change. The morning is when the maker has the most focus; protect it for craft work.

**Midday: collaborate.** Pair with the engineer or the designer. Discuss the choices. Adjust. The collaboration happens mid-day when both are present, not as a separate scheduled block.

**Afternoon: refine.** Take the artifact further. Polish. Try the variation that was discussed. Cut the version that didn't work.

**End of day: push.** Commit the artifact to a place the team can see. Even if it is in-progress, the visibility prevents stalling and enables next-day reactions from the taste-keeper.

**Demo days: show.** Once a week or twice a week, the artifact goes in front of the taste-keeper. Direction is set. The next iteration's goal becomes clear.

This rhythm is not heroic in the sense of long hours. It is heroic in the sense of focused hours. Six hours a day spent in the artifact, with attention, produces more than ten hours spent in slack-shaped distraction. The discipline is to protect the focused time.

---

## The shortlist

If you remember nothing else from this file, remember these.

- Iterate on a thing, not a plan. The artifact is the conversation.
- Every meeting that matters is a demo of a working artifact.
- One decision-maker per work stream. The taste-keeper, not the committee.
- Refuse frankenstein synthesis. Pick a direction; don't blend incompatible feedback.
- Ask "what's the demo?" until the team has a concrete artifact in flight.
- Tighten the loop. Minutes between iterations, not weeks.
- Heroic effort plus small team. Either alone fails.
- Default to no. Restraint is the counter to bloat.
- Seven elements: inspiration, collaboration, craft, diligence, decisiveness, taste, empathy.
- For assistant-driven design: every turn produces a concrete artifact, never a plan.
