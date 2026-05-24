# Generation Modes

How to choose the right working mode for a design task. There are three primary modes — Direct Generation, Shotgun Exploration, and Consultation — and the work of the first sixty seconds is picking which one applies. The wrong mode wastes hours; the right mode compounds.

This document codifies how to choose, how each mode flows, and how exploration converts back into a single committed direction.

---

## The three modes

### 1. Direct Generation

**Posture.** You have a brief. You know the direction. You ship one design end-to-end.

**Inputs required.**
- Clear surface (one page, one component, one flow).
- Clear aesthetic direction (named or referenced).
- Clear constraints (stack, audience, success metric).
- A decision-owner who can react fast if you ask.

**Outputs.**
- A single coded artifact, ready to ship or be reviewed.
- A short note on what was inferred where the brief was silent.
- A list of follow-ups that surfaced during the build but were out of scope.

**Time profile.** Linear. Most of the time is in execution, not in deciding what to execute.

**Failure mode.** Mistaking ambiguity for clarity. You start direct, you discover the brief is fuzzier than it looked, you have already burned hours producing a design that drifts. The fix is to upgrade the mode mid-task: stop, surface the ambiguity, propose two or three concepts, get a call.

---

### 2. Shotgun Exploration

**Posture.** The brief is fuzzy on visual direction. The team will recognize the answer when they see it but cannot describe it in words. You produce two to three genuinely-different variants, view them side by side, and pick the winner.

**Inputs required.**
- A surface (otherwise the variants have nothing to render against).
- A rough sense of the constraints (stack, audience, accessibility floor).
- Disagreement, ambiguity, or stuckness about visual direction.
- A decision-owner who will pick after seeing variants.

**Outputs.**
- N variants, each coherent within itself, genuinely divergent from the others.
- A side-by-side comparison artifact.
- A chosen direction, with notes on what worked from each variant.
- The losing variants saved as evidence of "directions rejected" for future sessions.

**Time profile.** Front-loaded. Most of the time is in producing comparable variants and presenting them well. The decision itself is fast once the variants are visible.

**Failure mode.** Frankenstein synthesis — taking the type from variant A, the color from variant B, the layout from variant C, and gluing them together. This destroys the coherence that made each variant good. The fix: iterate the winning variant, treat the losers as critique, never average across.

---

### 3. Consultation

**Posture.** Stakeholder-driven discovery. The brief is so ambiguous that producing visuals first would be guessing. You ask the right questions in a structured opening conversation, surface assumptions, propose a complete system with rationale, and adjust based on stakeholder response. The output is a written direction the team can ship against.

**Inputs required.**
- A stakeholder available to react (real-time or asynchronous).
- A product or surface in mind, even if undefined.
- Willingness from the stakeholder to commit to a direction once the conversation lands.

**Outputs.**
- A decision log (date, decision, rationale, one row per major call).
- A design direction document (aesthetic, palette with hex values, typography with font names and roles, spacing scale, layout approach, motion philosophy, explicit anti-patterns).
- A preview or mockup showing the system applied to a real screen.

**Time profile.** Front-loaded on discovery, then a single coherent proposal, then iteration. The build phase is fast once the consultation lands because there is nothing left to decide.

**Failure mode.** Death by options — presenting every aesthetic, every palette, every font, every layout as a menu. The stakeholder cannot evaluate; the consultant has dodged the work of recommending. The fix: have an opinion. Propose the whole system. Defend the moves. Adjust on pushback.

---

## When to commit vs explore vs consult

The default is **direct generation**. Most tasks have enough specificity that one coherent design beats three OK ones. Reach for the other modes only when the situation demands.

### Commit (direct) when:

- The brief names the direction ("brutalist editorial pricing page").
- A reference is in hand and the job is translation.
- The stakeholder has already committed to a direction in a prior session.
- The surface is small (one component, one card, one micro-interaction) and variants would be three flavors of the same thing.
- The implementation is the bottleneck, not the decision.

### Explore (shotgun) when:

- The brief gestures at direction but does not name it ("something modern but not generic").
- The team is converging on a generic answer and needs to see real divergence.
- The stakeholder said "I don't like how this looks" but cannot say what would be better.
- You are early in a redesign and want to validate three directions before committing.
- The design system is in place but you need to see it applied across genuinely different aesthetic moves.
- You suspect the team's default taste is not the right answer for this product.

### Consult when:

- No brief exists. The work starts with "we need a design for X" and nothing else.
- Multiple stakeholders disagree on what the product is.
- Brand equity is in play — there is something to preserve, and the rules of preservation have not been articulated.
- The success metric is undefined. "Looks better" is not a metric and the consultation is what makes one concrete.
- The product is genuinely new — no precedent in the codebase, no analog in the team's history.
- The stakeholder is asking for a recommendation, not a design.

---

## The decision tree: brief clarity × stakeholder count

```
                    Brief Clarity
                  Vague        Sharp
                  -----        -----
Stakeholders
   1              Shotgun     Direct
   2-3            Consult     Direct
   4+             Consult     Direct (with sign-off)
```

**Brief is sharp.** Direct, regardless of stakeholders. With multiple stakeholders, get sign-off before building — but build, do not workshop.

**Brief is vague, one stakeholder.** Shotgun. Produce three variants, let the single decision-maker pick. Conversation can resolve the rest after they have something visual to react to.

**Brief is vague, multiple stakeholders.** Consult. Variants without alignment produce more disagreement, not less. Get the room to agree on the system first.

**Edge case: vague brief, decisive solo stakeholder, no time.** Direct, with assumptions made explicit. Document what you inferred. The stakeholder either confirms or corrects, and either is faster than a shotgun.

**Edge case: sharp brief, contested team.** Direct, but the contest is about taste, not requirements. Build the sharp brief; if the team still contests after seeing it, that is a consultation triggered by the build, not the brief.

---

## How each mode flows from /ux-frame

Every mode starts the same way: the frame establishes who the work is for, what it is for, what the constraints are, and what success looks like. The frame is the input to mode selection.

### Frame outputs that govern mode selection

The frame should produce four things:

1. **The product description.** What it does, who uses it, what space it occupies.
2. **The aesthetic direction (if known).** Named or referenced, or marked as "to discover."
3. **The constraints.** Stack, accessibility floor, performance budget, timeline.
4. **The memorable thing.** What the first-time user should remember after seeing this product, in one sentence.

If items 1-4 are concrete, the mode is **direct**.

If item 2 is "to discover" but 1, 3, 4 are sharp, the mode is **shotgun** — variants explore axis 2 while holding the others constant.

If items 1, 3, and 4 are themselves fuzzy, the mode is **consultation** — the frame itself needs more work before any visual production starts.

### The flow into each mode

**Direct flow.** Frame → reference (image, audit, or generated mockup) → analysis → build → self-review → ship.

**Shotgun flow.** Frame → axis selection → variant concepts (one sentence each, in writing) → confirm divergence with stakeholder → generate variants → side-by-side comparison → pick winner → iterate winner → ship.

**Consultation flow.** Frame → discovery questions (asked in one structured conversation, not fragmented) → surface assumptions → propose coherent system (aesthetic, layout, color, type, spacing, motion) with rationale → present safe choices + risks → drive to decision → write decision log + direction document → produce one mockup → ship.

The frame is the funnel; the modes are the paths through it. The choice of path is the most important call of the session.

---

## Variant axes for shotgun mode

A shotgun without an axis is noise. The axis is what makes the variants comparable: you hold most things constant and vary one or two things sharply. Without an axis, the variants are random divergence and the comparison teaches nothing.

The standard axes:

### Style

Brutalist vs editorial vs luxury vs playful vs industrial vs organic. The aesthetic family changes; layout, density, and motion may stay similar. Use when the team cannot name the aesthetic but will recognize it.

### Layout

Grid-disciplined vs editorial-asymmetric vs poster-stacked vs masonry vs single-column-narrative. Same palette and type, different composition. Use when the content is settled but the spatial arrangement is contested.

### Density

Airy gallery vs balanced product vs cockpit-dense. Same components, different breathing room. Use when the team disagrees about how much information per viewport.

### Motion intensity

Static, intentional, or expressive. Same surface, different motion philosophy. Use when motion is a real product decision (e.g., dashboards where animations affect comprehension) rather than chrome.

### Color approach

Restrained mono vs balanced bi-color vs expressive multi-accent. Use when the palette is the most contested decision.

### Typography character

Clean grotesk vs expressive display vs editorial serif-sans pairing. Use when the type is the strongest carrier of mood and the team is unsure.

### Picking the axis

The strongest shotguns vary one axis sharply and let the consequences fall where they may. Trying to vary every axis at once produces incomparable variants — three variants that disagree on everything cannot be compared at all.

If the team cannot agree which axis is the contested one, that is itself a signal: the brief is too fuzzy and consultation comes before shotgun.

### The anti-convergence test

Each variant must use a different font family, a different palette, and a different layout approach. The test: if someone could swap the headline text between two variants without noticing, they are too similar. Regenerate the weaker one with a deliberately different direction.

Variants should feel like they came from three different design teams, not from the same team at three different coffee levels.

---

## The Frankenstein synthesis warning

The most tempting failure mode in shotgun work is to take "the typography from A, the color from B, the layout from C" and produce a synthesized fourth option. This is almost always bad.

### Why synthesis fails

- **Choices are coherent because they were made together.** Taking the type from A removes it from the structure that made it work. The serif/grotesk pairing in A was chosen against A's spacing rhythm and A's palette. Drop it into B's environment and it stops working — the rhythm is different, the contrast is different, the proportions disagree.

- **The synthesis has no author.** Every variant was a deliberate point of view; the synthesis is a committee. The synthesis is what each individual variant was designed not to be.

- **The synthesis loses the risk-taking that made any variant interesting.** Averaging produces the bland median. The variants existed to show divergence; collapsing them to a synthesis erases the divergence.

### The right move when stakeholders want to combine

When the stakeholder says "I want the color from B but the layout from A," there are three legitimate responses, and synthesis is not one of them.

**1. Pick the strongest variant and iterate.**

Take the variant that wins on the most important axis. Refine it with feedback from the others. "B wins on color. Let's iterate B with the spacing rhythm from A." The iteration absorbs the critique; the base variant keeps its coherence.

**2. Treat the others as critique, not parts.**

What did A do well that B could absorb without breaking? Often the answer is "B was too restrained — borrow A's confidence with type scale." That is a refinement, not a frankenstein. The principle from A is absorbed; the literal element is not transplanted.

**3. Run a second shotgun.**

If the answer is genuinely "the right direction is none of these but somewhere in between," run another round with new concepts informed by the first. The second round's concepts are not averages of the first — they are new positions that absorb the lessons.

### The boundary

The boundary between legitimate iteration and Frankenstein synthesis is the word "literal." Borrowing a principle (e.g., "more confident type scale") is fine. Borrowing a literal element (e.g., "use B's exact palette in A") will produce mush. When unsure, ask: am I taking a lesson or an element? Lessons compose; elements collide.

---

## Converting exploration output back into a commit-to-one decision

The shotgun is the start of the work, not the end. Once the winner is picked, the mode switches back to direct generation — and the discipline is to actually commit.

### The handoff

The shotgun produces:

- A winning variant.
- A list of refinements drawn from the losing variants (as critique, not parts).
- A note on what was rejected and why.

The handoff into direct mode produces:

- A design tokens extraction from the winning variant: color values, typography stack, spacing scale, radius scale.
- An updated frame document: the aesthetic direction is now sharp (named after the winning variant), and the rest of the surface will be built against it.
- A list of next surfaces to apply the system to.

### The commit discipline

Once the winner is picked, do not re-litigate. The shotgun was the decision moment. Subsequent surfaces inherit the winning direction. New evidence (user research, accessibility findings, performance data) reopens the decision; new opinions do not.

If a stakeholder reopens the decision without new evidence, the response is: "We ran the shotgun on this. The winning direction was X for these reasons. What new evidence changes the call?" If there is none, the conversation closes and the build continues.

### Saving the rejected directions

Save the losing variants as evidence of "directions rejected" for future sessions. This serves two purposes:

1. **Future shotguns can avoid retreading.** When the same product needs another exploration round later, the saved rejects bias the new round toward genuinely new directions instead of accidentally re-running the lost battles.

2. **The decision log is auditable.** If a stakeholder asks "why didn't we try X?" the answer is either "we did, and we rejected it because Y" or "we did not, here is why." Both are better than a shrug.

The saves go into the project's design archive — not deleted, not lost, but clearly marked as not-the-direction.

---

## When to escalate or downgrade modes

Modes are not fixed at the start. The work surfaces information that may change the right mode mid-task.

### Escalate direct → shotgun

You started direct, you are halfway through, and you cannot decide between two genuinely different approaches. Stop. Stage both as concepts. Run a fast shotgun of two variants. Pick. Resume.

### Escalate direct → consultation

You started direct, you are halfway through, and you realize the brief is wrong — the product is not what you thought, the audience is different, the constraints are heavier than disclosed. Stop. Do not push through. Surface the ambiguity and run a consultation conversation. The cost of pausing is far less than the cost of shipping a design built on the wrong assumptions.

### Escalate shotgun → consultation

You generated three variants, none of them are landing, and the stakeholder cannot articulate what is wrong. The shotgun was diagnostic: it showed that the axes were wrong or the concepts were not divergent enough. Before running a second shotgun, have a consultation conversation to fix the brief.

### Downgrade consultation → direct

You started a consultation, the stakeholder is decisive, the system fell into place fast. Skip the long discovery — propose the system, defend it, get the call, build.

### Downgrade shotgun → direct

You started a shotgun, the first concept you wrote down is obviously the right answer, the other two would be straw men. Skip the variants. Build the direct version. Document why the variants were skipped so the team understands the decision was deliberate, not lazy.

---

## Standing rules across all modes

These hold whether the mode is direct, shotgun, or consultation:

1. **Reference first, code second.** Whether the reference is an image, an audit, a generated mockup, or a written direction, it precedes the build.

2. **Coherence over individuality.** Choices that reinforce each other beat choices that are individually optimal but mismatched. A shotgun produces variants where each variant is coherent within itself; never sacrifice that for cross-variant averaging.

3. **Constraint, restraint, intentionality.** When in doubt, do less. The restrained option wins the tiebreaker. Every element exists for a reason you can name in one sentence.

4. **Demo, do not describe.** The visual artifact closes more decisions than the document. Consultation produces a mockup; shotgun produces side-by-side variants; direct produces a working build. All three end in a visual, not a paragraph.

5. **Default to the more restrained option.** When the stakeholder is genuinely torn, recommend the quieter choice. Restraint compounds; loudness does not.

6. **Commit and ship.** Litigation after commit is overhead. Demo-driven iteration is progress. The mode picks itself when the question is "what should I do?" — but once chosen, the mode is closed until the work ships or the brief changes.

---

## Anti-patterns

- **Picking shotgun by default.** Three variants for every task is wasteful. The default is direct. Shotgun is for genuine ambiguity, not for showing off range.

- **Picking consultation when the brief is fine.** "Let me ask you ten questions before I build" is friction when the brief is sharp. Consultation is for fuzz, not for ceremony.

- **Switching modes mid-task without saying so.** If you started direct and you are now exploring variants in your head, you have switched to shotgun without telling anyone. Surface the switch; do not silently produce three designs the stakeholder did not ask for.

- **Running a shotgun without an axis.** Three variants that disagree on everything are not comparable. Pick the axis, hold the rest constant, produce variants that vary on the axis. Otherwise the comparison teaches nothing.

- **Synthesis after a shotgun.** Already covered: never take the type from A, color from B, layout from C and call it a fourth option. Iterate the winner instead.

- **Skipping the decision log in consultation.** A consultation that produces no written record of decisions and rationale is not a consultation — it is a meeting. The log is the artifact that prevents re-litigation.

- **Refusing to commit.** "I could go either way" is not a consultation; it is a deferral. The consultant's job is to have the way. Defer only when new information is genuinely needed.

- **Litigating after commit.** Once the mode produces a decision (direct's build, shotgun's winner, consultation's system), the decision is closed unless new evidence emerges. Second thoughts do not count as evidence.

---

## The session frame

Every working session opens with the same three questions, and the answers determine the mode.

1. **What is the brief?** State it in one sentence. If you cannot, the mode is consultation.

2. **Is the visual direction known?** If yes, direct. If no, shotgun (for vague direction) or consultation (for absent direction).

3. **Who decides?** If one stakeholder, the work can move fast. If multiple stakeholders disagree, consultation comes first — variants without alignment produce more disagreement, not less.

These three questions are the cheapest part of the session and they prevent the most expensive failure mode: spending hours producing the wrong artifact in the wrong mode.

---

## The compounding effect

Each mode teaches the system.

- **Direct mode** builds execution speed. The more direct designs you produce, the faster you read briefs and the more reliably you translate.
- **Shotgun mode** builds range. The more variants you produce, the more clearly you see what differentiates aesthetics and the less likely you are to default to a generic answer.
- **Consultation mode** builds judgment. The more discoveries you run, the better you get at recognizing fuzz before it costs hours and at proposing systems that actually hold together.

The goal is not to specialize in one mode; it is to know which mode applies and to switch fluidly. A senior designer runs all three in the same week and barely notices the switching — the mode is part of the work, not separate from it.

Hold the rules. Pick the mode. Ship the work. The next project gets easier.
