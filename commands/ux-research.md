---
description: User research planning — interview scripts, survey design, recruitment screener, synthesis. Triggers on "plan a research study", "I need interview questions", "design a survey", "how do I recruit users".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Glob, Grep, Task
disable-model-invocation: false
---

# /ux-research

You are running the `/ux-research` command from the `ux` plugin. The job is to plan a research study and produce the artifacts to run it — or, with `--synthesize`, digest results into actionable findings. Methodologically rigorous, anti-bias by default.

## When to use

Triggers: "plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes". Also runs as a sub-step of `/ux-workshop` between phases.

## Input

Required (planning mode):
- **Research question(s)**: what you want to learn, in plain language
- **Design decision the research informs**: the action that will change based on findings
- **Budget / timeline**: minutes per session, total sessions, dollars

Required (synthesis mode, triggered by `--synthesize`):
- Path to raw notes / transcripts / survey CSV
- The original research question(s) for grounding

If anything's missing, ask once: *"Research question, the design decision it informs, and budget/timeline (sessions × minutes × incentive)?"*

## Process (planning mode)

### 1. Frame the research question

Classify the question into one of:
- **Problem discovery** — is there a problem worth solving here?
- **Solution validation** — does our proposed solution address the problem?
- **Usability testing** — can users actually use what we built?
- **Preference / desirability** — which option resonates?
- **Segmentation** — who are the user types and what differentiates them?

A research question that fits two categories is too broad. Split it.

### 2. Pick the method

| Question type | Default method | Alternative |
|---|---|---|
| Problem discovery | Semi-structured interview (n=5-8) | Diary study (n=5, 1 week) |
| Solution validation | Concept test (n=5-8) + structured interview | Fake door (n=∞ via traffic) |
| Usability testing | Moderated task-based test (n=5-8) | Unmoderated remote (n=15+) |
| Preference / desirability | Within-subjects preference test (n=8-12) | A/B test (n=large, traffic-dependent) |
| Segmentation | Survey (n=100+) | Card sort + cluster analysis (n=15-25) |

Smoke tests and fake doors are valid for binary problem-existence checks before deeper qual work.

### 3. Generate the artifact

Build the deliverable for the chosen method:

- **Interview script** — open-ended + behavior-focused questions, no leading wording. Structure: warm-up (2-3 q), context (current behavior), specific (past experience with the problem), reflection (what would solve this), wrap-up. Never ask "would you use" — ask about past behavior.
- **Survey** — anti-bias structure. Randomize answer order. Mix 5-point Likert with open-ended. Screen out professionals/insiders. Attention check question.
- **Usability test plan** — tasks framed as goals not steps. Time-box per task. Define success criteria upfront. Think-aloud protocol stated to participant.
- **Diary study brief** — daily prompt, max 5 min effort, end-of-study debrief interview.
- **Screener questionnaire** — disqualifying criteria first, then qualifying. Stated incentive, time commitment, schedule.

### 4. Recruitment plan

- **Where**: user pool / customer list / Respondent.io / UserInterviews / Prolific / community forums / DM intercept on the product / partner contacts
- **Incentive**: dollar value matched to time (industry rule of thumb: ~$1-2/minute for B2C, $3-6/minute for B2B / experts)
- **Volume**: target sample + 30% buffer for no-shows

### 5. Analysis plan

State upfront how findings will be synthesized:
- Affinity mapping for interviews
- Cross-tabs + chi-square for surveys
- Task completion + time-on-task + System Usability Scale (SUS) for usability
- Tag taxonomy for diary studies

## Process (synthesis mode)

Dispatch `research-synthesizer` via Task. Pass:
- Raw input files
- Original research question
- Method that was used
- Instruction to produce: themes (with supporting quotes), behavioral patterns, surprises, decision-ready insights (each tied back to the original design decision), recommended next steps

### Output format

```
─── research plan ───
Question:   <verbatim>
Decision:   <what changes based on findings>
Method:     <method>
Sample:     n=<target> (n=<target+buffer> recruited)
Timeline:   <weeks>
Budget:     $<total>

─── artifact ───
<the deliverable — interview script / survey / test plan / screener — in full>

─── recruitment ───
Source:     <where>
Incentive:  $<amount> / <duration>
Screener:   <key criteria>

─── analysis plan ───
<how findings will be synthesized>

─── next ───
Run the study, then come back with /ux-research --synthesize
```

### State

Write to `.ux/last-research.json`:

```json
{
  "command": "ux-research",
  "timestamp": "<ISO8601>",
  "mode": "planning|synthesis",
  "question": "<verbatim>",
  "decision": "<design decision>",
  "method": "<method>",
  "sample_target": <n>,
  "incentive": "<amount>",
  "artifact_file": "<path>",
  "synthesis_findings": ["<key themes>"]
}
```

## Hard rules

- Never ask "would you use" — ask about past behavior. Stated intent is a noise channel.
- Never recommend n<5 for qual; never recommend n<30 for quant; never recommend n<100 for segmentation surveys.
- Screen out product professionals (designers, PMs, UXers) unless they ARE the target user.
- Randomize answer order in surveys. No order-bias artifacts.
- Attention check questions on every survey.
- Time-box every session. Sessions that run long produce diminishing returns and respondent fatigue.
- Tie every finding back to the original research question. Findings that don't map are notes, not insights.

## Failure modes

- **Multi-question studies**: trying to learn 5 things in one session = learning 0 things well. Split the study.
- **Leading wording**: "How much do you love X?" — reject and rewrite.
- **Recruiting from product users only**: confirmation bias. Mix in non-users for discovery work.
- **No incentive**: response rate craters. Always pay participants.
- **Synthesis as a quote dump**: themes need to be patterns across participants, not "one person said X."

## Next prompt

After `/ux-research` (planning):
- Run the study
- `/ux-research --synthesize` — dispatch `research-synthesizer` on raw results

After `/ux-research --synthesize`:
- `/ux-design` — apply findings to a design
- `/ux-frame` — re-baseline the brief on what you learned
- `/ux-workshop` — if findings open a bigger question
- `/ux-next` — let the conductor pick
