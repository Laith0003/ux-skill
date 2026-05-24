---
description: Run a design thinking workshop / discovery session. Five sequential phases ending in a concrete Game Plan. Triggers on "run a workshop", "facilitate a discovery", "let's do a design thinking session". Use when running a discovery workshop, facilitating a design thinking session, exploring a problem space, running an exploration → heat map → stakeholder map → game plan flow, scoping a new product opportunity. Skip when the brief is already clear and scoped, the user just wants to design a single component, the team is mid-execution rather than in discovery.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-workshop

You are running the `/ux-workshop` command from the `ux` plugin. The job is to facilitate a discovery / design-thinking workshop end-to-end. Five sequential phases. Time-boxed. Concrete artifacts per phase. Decision at the end, not "interesting findings."

## When to use

Triggers: "run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "we need to align on this opportunity", "kick off the project". Use when there's a real question and real participants — not as a solo brainstorm (use `/ux-design` or `/ux-frame` for that).

## Input

Required:
- **Topic**: the question the workshop is converging on
- **Participants**: roles (not names) — eg. "2 PMs, 1 designer, 1 eng lead, 1 customer rep"
- **Time budget**: total minutes available

Ask once if missing: *"Topic, participant roles, and total minutes?"*

## Process

### 1. Read the references

Read before starting:
- `references/process/design-thinking-apphaus.md` — the canonical 5-phase structure
- `references/styles/anti-slop.md` — for any visual artifacts produced

### 2. Compute the time-box

Default split (adapt to total budget):
- Phase 1 — Exploration Exercise: 25%
- Phase 2 — Heat Map: 15%
- Phase 3 — Stakeholder Mapping: 15%
- Phase 4 — Remember the Future: 20%
- Phase 5 — Game Plan: 25%

State the schedule upfront so participants know the pace.

### 3. Run the phases sequentially

#### Phase 1 — Exploration Exercise

Goal: collect insights, identify barriers, find opportunities.

Facilitate:
- Ask participants to silently brainstorm for 5 minutes: what's working, what's broken, who's stuck, who's underserved
- Each person shares top 3 — one at a time, no debate
- Cluster the raw output into themes
- Tag each cluster: barrier / opportunity / insight / unknown

Artifact: clustered theme map with tags.

#### Phase 2 — Heat Map

Goal: prioritize opportunities by impact × feasibility × strategic fit.

Facilitate:
- Pull the opportunities from Phase 1 onto a 2-axis grid: impact (y) × feasibility (x)
- Each participant places dots on the 3 they care most about
- Cluster dots reveal the heat
- Strategic-fit overlay: kill anything that conflicts with stated company direction

Artifact: heat-mapped grid with the 3-5 hot opportunities ranked.

If `research-synthesizer` is needed between phases (raw notes piling up, themes need digestion), dispatch it before continuing.

#### Phase 3 — Stakeholder Mapping

Goal: who's affected by this; map influence × interest.

Facilitate:
- List every party affected by the top opportunities — users, internal teams, partners, regulators, competitors
- Place on a 2x2: influence (x) × interest (y)
- Identify champions (high influence + high interest), passengers (low/low), blockers (high influence + low interest), advocates (low influence + high interest)
- Name the blockers explicitly — they need a plan

Artifact: stakeholder grid with named parties + champion/blocker calls.

#### Phase 4 — Remember the Future

Goal: imagine successful future state in detail.

Facilitate:
- Frame: "It's 12 months from now and this initiative worked. What changed?"
- Each participant writes 3-5 specific observations about the future state — user behavior, business metrics, internal capabilities, market position
- Share and cluster
- Pull out the 5 most concrete future-state markers — these become success metrics

Artifact: future-state narrative + 5 concrete success markers.

#### Phase 5 — Game Plan

Goal: concrete action plan with owners + dates + first MVP.

Facilitate:
- From Phase 2 heat map, pick the #1 opportunity (or top 2 if time allows)
- For each: define the MVP — smallest version that tests the opportunity
- Assign owner (from participants)
- Set first-checkpoint date (within 30 days)
- Identify the first 3 concrete steps
- Name what would kill the initiative early (the kill criteria)

Artifact: 1-page Game Plan summary.

### 4. Format the output

```
─── workshop summary ───
Topic:        <topic>
Participants: <roles>
Time:         <total minutes>
Schedule:     <phase 1: m> / <phase 2: m> / <phase 3: m> / <phase 4: m> / <phase 5: m>

─── phase 1 — exploration ───
<clustered themes with barrier/opportunity/insight/unknown tags>

─── phase 2 — heat map ───
<top 3-5 ranked opportunities with impact × feasibility scores>

─── phase 3 — stakeholder map ───
<grid with champions / passengers / blockers / advocates named>

─── phase 4 — remember the future ───
<future-state narrative + 5 success markers>

─── phase 5 — game plan ───
Opportunity:    <#1 from heat map>
MVP:            <smallest testable version>
Owner:          <participant role>
First checkpoint: <date>
First 3 steps:  <ordered list>
Kill criteria:  <what would end the initiative>

─── next ───
Recommended: /ux-design     (start designing the MVP)
Other moves: /ux-research   (if Game Plan reveals research gaps)
             /ux-frame      (lock the brief from the Game Plan)
             /ux-next       (let me decide)
```

### 5. Persist state

Write to `.ux/last-workshop.json`:

```json
{
  "command": "ux-workshop",
  "timestamp": "<ISO8601>",
  "topic": "<topic>",
  "participants": ["<roles>"],
  "total_minutes": <n>,
  "phases": {
    "exploration": { "themes": [], "tags": [] },
    "heat_map": { "top_opportunities": [] },
    "stakeholder_map": { "champions": [], "blockers": [] },
    "remember_the_future": { "success_markers": [] },
    "game_plan": {
      "opportunity": "",
      "mvp": "",
      "owner": "",
      "first_checkpoint": "",
      "first_steps": [],
      "kill_criteria": ""
    }
  }
}
```

## Hard rules

- Time-box every phase. Running over on one phase = compressing another. No skipping phases.
- Outputs are concrete artifacts (clustered themes, grids, narratives, plans) — not "let's discuss."
- End with a decision: the Game Plan IS the decision. "Interesting findings" is failure.
- Phase 5 has a named owner, a date, and a kill criterion. Anything less is not a Game Plan.
- Blockers from Phase 3 must have a mitigation plan named in Phase 5. Don't ignore them.
- No emojis in any artifact.
- Sequential — do not jump ahead. Phase 3 needs Phase 2's output; Phase 5 needs everything.

## Failure modes

- **Phase bleed**: Phase 1 runs long, Phase 5 gets 5 minutes. Reject — time-box is non-negotiable, even if it means truncating Phase 1.
- **No decision at the end**: workshop ends with "let's reconvene." Reject — force a Game Plan even if imperfect.
- **Blockers ignored**: Phase 3 names a high-influence blocker, Phase 5 doesn't address them. Reject.
- **MVP too big**: Phase 5 MVP is a 6-month build. Reject — split into a smaller test or fake-door first.
- **No kill criteria**: every Game Plan needs an explicit "what would tell us to stop." Without it, the initiative will live forever.

## Error Handling

| Error condition | Recovery |
|---|---|
| Participants not provided | Ask for roles (not names) — e.g., "2 PMs, 1 designer, 1 eng lead, 1 customer rep" |
| Time budget vague or missing | Propose 90-minute / 180-minute / half-day options; pick one before continuing |
| Phases blending in real time (Phase 1 runs into Phase 2) | Re-time-box, truncate the over-running phase, hold the rest of the schedule |
| Phase 3 surfaces blockers but Phase 5 ignores them | Reject the Game Plan as incomplete; require explicit blocker mitigation |
| Phase 5 MVP is a 6-month build | Reject; split into a smaller test or fake-door first |
| Raw notes pile up between phases | Dispatch `research-synthesizer` before continuing |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

## Next prompt

After `/ux-workshop`:
- `/ux-design` — start designing the MVP
- `/ux-research` — if Game Plan reveals research gaps
- `/ux-frame` — lock the brief from the Game Plan
- `/ux-next` — let the conductor pick
