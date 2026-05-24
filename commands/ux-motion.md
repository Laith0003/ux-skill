---
description: Animation and motion rubric. Checks timing, easing, meaning, reduced-motion compliance, and performance for every animation on a surface. Triggers on "motion check", "are the animations good", or "fix the motion".
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(grep:*), Bash(find:*), Bash(mkdir:*), Bash(date:*), Glob, Grep, Task, WebFetch
disable-model-invocation: false
---

# /ux-motion

You are running the `/ux-motion` command from the `ux` plugin. The job is to evaluate every animation on a surface against five dimensions — timing, easing, meaning, reduced-motion compliance, performance — and identify what to keep, what to tune, and what to kill.

## When to use

Triggers: "motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "is this too much animation", "the motion feels off", "performance pass on the motion".

Use after building a motion-rich surface, after a redesign that added new transitions, or when something "feels wrong" but the user cannot name it. Not for layout or copy issues — those are `/ux-audit` and `/ux-copy`.

## Input

One of: a live URL (preferred — motion is observable), a screen recording, a CSS/JS file with animation definitions, or a code snippet. Static screenshots are insufficient — flag and request a recording or live URL.

## Process

### 1. Inventory every animation

List every animation present, including:

- CSS transitions on hover, focus, active states.
- CSS keyframe animations (loaders, indicators, attention-grabbers).
- JS-driven animations (libraries: GSAP, Framer Motion, Motion One, Web Animations API).
- Scroll-linked animations (parallax, scroll-tied transforms, scroll-triggered reveals).
- Page-transition animations.
- Micro-interactions (button press, checkbox tick, toggle slide).
- Implicit animations (carousel auto-advance, marquee, autoplay video).

For each, note: trigger, duration, easing, properties animated, scope (single element or page-wide).

### 2. Evaluate each animation on five dimensions

#### Dimension 1 — Timing

- **Micro-interactions** (button press, hover state, checkbox tick): 150–250ms. Anything ≥ 300ms feels sluggish on micro.
- **Component transitions** (modal open, drawer slide, toast appear): 200–300ms.
- **Complex transitions** (page transitions, multi-element choreography): up to 400ms — beyond that, the user starts waiting.
- **Loaders / indicators**: continuous, but the loop should be 800–1500ms to feel alive without nagging.

Flag any animation outside its tier's range.

#### Dimension 2 — Easing

- **Ease-out** (`cubic-bezier(0, 0, 0.2, 1)` or near) for elements entering — fast in, settled out.
- **Ease-in** for elements leaving — gentle start, quick out.
- **Ease-in-out** for state changes where neither end is "the destination."
- **Linear** only for loaders and rotations.
- **Spring** for elements that should feel physical (toggle, drag-release).

Flag default `ease` or `linear` on non-loaders — they almost always feel wrong.

#### Dimension 3 — Meaning

Every animation should answer one of:

- **Spatial continuity** — telling the user where something came from or went.
- **Causality** — showing that action A produced result B.
- **State change** — making a transition between two states perceivable.
- **Affordance hint** — drawing the eye to something interactive.
- **Loading signal** — telling the user the system is working.

Animations that do not serve one of these are decorative. Flag decorative motion as a candidate for cut.

#### Dimension 4 — Reduced-motion compliance

- `prefers-reduced-motion: reduce` query MUST be respected.
- Large translations, parallax, scroll-tied effects: disabled or replaced with opacity-only fade.
- Auto-playing animations: stopped or single-cycle.
- Loaders: simplified (no spinning, just static "loading" text or a single fade pulse).

Flag any animation that ignores reduced-motion.

#### Dimension 5 — Performance

- Animate `transform` and `opacity` only. Never `width`, `height`, `top`, `left`, `margin`, `padding`, or `box-shadow` (use a layered shadow element if needed).
- No layout thrashing — animations must not cause reflow during the animation.
- 60fps target — drops below 50fps are a finding.
- Avoid animating > 5 elements simultaneously without compositing.
- Avoid scroll-tied animations that pin the page for > 1.5 viewport heights — they break scroll instinct.

Flag any animation that violates these.

### 3. Score and group

For each animation, decide an action:

- **Keep** — passes all five dimensions.
- **Tune** — fails one or two dimensions, fixable without removing the animation.
- **Cut** — decorative, performance-costly, or actively harmful.

Assign severity to issues:

- **Critical** — breaks the surface for reduced-motion users, causes jank that blocks interaction, or actively misleads (e.g., animation suggests wrong spatial continuity).
- **High** — noticeably wrong timing or easing, decorative animation distracting from the task.
- **Medium** — would feel better tuned but works.
- **Cosmetic** — polish.

### 4. Format the output

```
─── motion audit ───
Surface:        <URL / path / description>
Animations:     <total count>
Verdict:        Keep <n> | Tune <n> | Cut <n>
Severity:       Critical <n> | High <n> | Medium <n> | Cosmetic <n>

─── per-animation findings ───

<animation name or selector>
  Trigger:           <what fires it>
  Duration:          <current> → <recommended if changed>
  Easing:            <current> → <recommended if changed>
  Properties:        <animated properties>
  Verdict:           Keep | Tune | Cut
  [<severity>] <one-line issue title if not Keep>
    Evidence:  <what you observed>
    Fix:       <what to do>

<next animation>
  ...

─── reduced-motion ───
<list of animations that fail or pass reduced-motion>

─── performance ───
<animations animating non-composite properties or causing jank>
```

### 5. Persist state

Write `.ux/last-motion.json`:

```json
{
  "command": "ux-motion",
  "timestamp": "<ISO8601>",
  "surface": "<URL / path / description>",
  "animations": [
    {
      "name": "<name or selector>",
      "trigger": "<what fires it>",
      "duration_ms": <n>,
      "easing": "<curve>",
      "properties": ["<animated properties>"],
      "verdict": "Keep | Tune | Cut",
      "severity": "Critical | High | Medium | Cosmetic | none",
      "issue": "<short>",
      "evidence": "<>",
      "fix": "<>",
      "reduced_motion_safe": true | false,
      "performance_safe": true | false
    }
  ],
  "verdict_counts": { "keep": <n>, "tune": <n>, "cut": <n> },
  "severity_counts": { "critical": <n>, "high": <n>, "medium": <n>, "cosmetic": <n> }
}
```

### 6. Optional fix flag

If the user passed `--fix`, after writing the report:

1. Validate clean working tree.
2. For each animation marked Tune or Cut, sorted by severity:
   - Dispatch `motion-engineer` sub-agent via the Task tool with the animation's current state and target.
   - Pass the agent the full motion rubric (timing tiers, easing rules, reduced-motion expectation, performance constraints).
3. Independent animations dispatched in parallel; animations sharing a stylesheet/component queued sequential.
4. Each fix commits atomically with a message naming the animation and the action (Tune or Cut).
5. After fixes, request a fresh recording or live re-check and report deltas.

## Output

The motion audit and (if `--fix`) the fix-loop results.

## State persisted

- `.ux/last-motion.json` — keys: `command`, `timestamp`, `surface`, `animations` (array of `{name, trigger, duration_ms, easing, properties, verdict, severity, issue, evidence, fix, reduced_motion_safe, performance_safe}`), `verdict_counts`, `severity_counts`.

## Next prompt

```
─── next ───
Recommended: /ux-motion --fix    (apply tune/cut actions)
Other moves: /ux-design          (motion gaps suggest a redesign moment)
             /ux-a11y            (reduced-motion deep-dive)
             /ux-audit           (broader structural review)
             /ux-next            (let me decide)
```

If the verdict is "Cut" on more than half the animations, recommend `/ux-design` — the surface is over-animated and a structural redo will be cheaper than per-animation surgery.

## Hard rules

- Never accept default `ease` or `linear` on a non-loader without flagging it.
- Never let an animation that animates `width`, `height`, `top`, `left`, `margin`, or `padding` pass as Keep — that is a Tune at minimum.
- Never let an animation that ignores `prefers-reduced-motion` pass as Keep — Critical severity, no exceptions.
- Never recommend "make it longer" as a fix — that almost always feels wrong. The correct answer is usually faster.
- Never declare an animation decorative without giving the user the chance to defend it — meaning can be intentional even when not obvious.
- Never auto-cut without re-verifying — cutting a motion that signaled state change creates a new finding (loss of feedback).

## Failure modes

- **Static-screenshot audits**: trying to evaluate motion from a screenshot. Stop and request a recording or live URL.
- **Cut-everything maximalism**: declaring all motion decorative. Some motion is functional — protect the spatial-continuity and causality animations.
- **Performance theater**: flagging "animates `margin`" without checking if the animation actually causes layout (sometimes the parent is `position: absolute` and there is no reflow). Verify before flagging.
- **Reduced-motion blind spot**: testing on the dev's machine where reduced-motion is off. Toggle the OS setting or simulate via DevTools.
- **Spring overuse**: applying spring easing to every animation because it "feels modern." Springs belong on physical interactions, not on every transition.
