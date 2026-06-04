# v3.0 Social Launch Playbook: copy, paste, post

**Status:** ready to ship. **Action:** copy each block, paste to the platform, post.

URLs in posts:
- Site: https://uxskill.laithjunaidy.com
- GitHub: https://github.com/Laith0003/ux-skill
- GitHub release: https://github.com/Laith0003/ux-skill/releases/tag/v3.0.0
- PyPI: https://pypi.org/project/uxskill/
- npm: https://www.npmjs.com/package/uxskill
- Launch blog: https://uxskill.laithjunaidy.com/blog/v3-the-brain-launch.html

---

## Day 0: Launch hour (post all these within 60 min of each other)

### POST 1: X / Twitter (single tweet, 280 chars max)

```
ux-skill v3.0 · THE BRAIN ships today.

Brand specs are training data now, not templates. A 7-axis synthesizer compiles a novel design language per brief. Recommender re-ranks from a local decisions ledger.

Offline. Deterministic. No LLM.

pip install uxskill

https://uxskill.laithjunaidy.com
```

### POST 2: LinkedIn (long-form, ~1200 chars)

```
After 3 months of work I'm shipping ux-skill v3.0 today: THE BRAIN.

It's a design intelligence engine for AI coding tools (Claude Code, Cursor, Windsurf + 14 more IDEs). The shift in v3.0: brand specs are no longer templates the recommender picks from. They're training data for a 7-axis synthesizer that compiles a novel design language per brief.

What's in v3.0:
→ 7-axis synthesizer (warmth/contrast/density/geometry/formality/motion/type_personality)
→ Triple-mode dispatch (strict_brand / brand_anchor / pure_synthesis)
→ Axis interaction matrix (explicit conflict resolution)
→ Decisions ledger drives recommender re-rank (closed feedback loop)
→ /ux-evolve auto-loop with quality gate at 65
→ 145 deterministic anti-pattern rules
→ 160 brand DESIGN specs (Apple, Stripe, Linear, Ferrari, Anthropic + 155 more)
→ 17 IDE integrations
→ 18 MCP tools
→ 223 tests passing

Critically: no LLM in the engine. Same brief always produces the same output. Runs offline.

MIT licensed. Free forever. No telemetry.

If you ship products via AI coding tools, ux-skill is the layer between you and the assistant that catches AI design slop before commit and learns from your local history.

GitHub: https://github.com/Laith0003/ux-skill
Install: pip install uxskill

#AICoding #DesignSystems #OpenSource #ClaudeCode #Cursor
```

### POST 3: HN (Show HN), submit as a new "Show HN" post

**Title:** `Show HN: ux-skill v3.0, deterministic 7-axis design synthesizer for AI coding`

**URL:** `https://uxskill.laithjunaidy.com`

**Text field:** (paste this)

```
Hi HN, Laith here. I shipped v3.0 of ux-skill, an open-source design intelligence engine for AI coding tools (Claude Code, Cursor, Windsurf + 14 more IDEs).

The architectural shift in v3.0: brand specs are no longer templates the recommender picks from. They're training data the engine distills into a fresh design language per brief.

Concrete pieces:

- 7-axis synthesizer (warmth/contrast/density/geometry/formality/motion/type_personality). Briefs map deterministically to axis values, axis values compile to palette + type + spacing + radius + motion tokens. Same brief → same output, always.
- Three modes, auto-dispatched: strict_brand (100% named brand), brand_anchor (70/30 named + adapted), pure_synthesis (no brand, infinity space from 8 axis-matching exemplars).
- Axis interaction matrix: explicit conflict resolution for when axes compete for one token (dense + corporate → 4px Bloomberg-style; airy + corporate → 12px luxury; sharp + corporate → 2px NYT; soft + playful → 18px Glossier).
- Decisions ledger drives recommender re-rank. Every call writes one JSONL line to .ux/decisions.jsonl (schema locked at _v: 1). The recommender reads this on the next call and bumps candidates that previously shipped clean (lint_score >= 80 AND user_accepted = true). Cold-start safe (>=3 priors per bucket).
- /ux-evolve auto-loop: lint → polish → re-lint until score >= 90 or plateau. 6 idempotent polish passes. Quality gate at 65.
- 145 deterministic anti-pattern rules (severity-weighted, sub-50ms scan).
- 160 brand DESIGN specs (Apple, Stripe, Linear, Ferrari, Anthropic, ...).
- Offline. No LLM in the engine. No telemetry. No network.

223 tests pass. MIT.

GitHub: https://github.com/Laith0003/ux-skill
PyPI: pip install uxskill
npm: npx uxskill init

Happy to answer questions about the synthesizer math, the decisions ledger schema, why we rejected LLM-judged subjective aesthetic axes (ChatGPT pushed hard for these in review; we went deterministic), or anything else.
```

### POST 4: Reddit r/ClaudeAI

**Title:** `Just shipped v3.0 of ux-skill, a deterministic design synthesizer for Claude Code`

```
The big architectural shift: brand specs (Apple, Stripe, Linear, etc.) are no longer templates the recommender copies. They're training data the engine distills into a fresh design language per brief.

How it works:

1. You give a brief: industry=fintech-payments, tone=["bold","serious"]
2. The engine computes 7 axis values from that brief
3. It pulls the 8 brand specs whose category-seed axes are nearest in 7-D space
4. It distills palette anchors, type stacks, motion timings, radius signals
5. It mixes the vocabulary weighted by axis position to produce fresh tokens

Same brief → same output, every time. Zero LLM calls in the engine.

Beyond the synthesizer there's also:
- /ux-evolve auto-loop (lint → polish → re-lint until score >= 90)
- 145 deterministic anti-pattern rules
- A decisions ledger that biases future recommendations from your local history
- 18 MCP tools for Claude Desktop integration

223 tests pass. MIT. No telemetry.

GitHub: https://github.com/Laith0003/ux-skill
Install: pip install uxskill or /plugin install ux@ux-skill

Would love feedback on the axis interaction matrix (the documented conflict resolution between axes that compete for one token).
```

### POST 5: Reddit r/cursor

**Title:** `v3.0 of a design intelligence engine that also runs in Cursor, looking for early feedback`

```
I shipped v3.0 of ux-skill today. It runs in Cursor through the standard Python install (pip install uxskill, then `uxskill init` auto-wires .cursorrules).

What it does for Cursor specifically:
- Synthesizes a complete design language per brief (palette + type + spacing + radius + motion)
- Catches AI design slop in your code via 145 deterministic regex rules (sub-50ms scan)
- Auto-iterates polish until score >= 90 (/ux-evolve)
- Re-ranks recommendations based on your local history (.ux/decisions.jsonl)

Three modes auto-dispatched by what's in your brief:
- strict_brand → 100% one brand's tokens (fast)
- brand_anchor → 70% one brand + 30% axis-adapted (custom)
- pure_synthesis → no brand, infinity space (novel each call)

Critically: no LLM calls in the engine. Same brief always produces the same design tokens. Reproducible across machines.

GitHub: https://github.com/Laith0003/ux-skill
Install: pip install uxskill && uxskill init

MIT. 223 tests pass. Looking for honest feedback before announcing more broadly.
```

### POST 6: Reddit r/webdev

**Title:** `Shipped a 145-rule deterministic linter that catches AI-generated design fingerprints before commit`

```
This is part of ux-skill v3.0. The linter is a standalone regex scanner: no LLM, no API calls, runs in under 50ms on a 10K-line project.

What it catches:
- Purple → blue 135° gradients (the #1 AI-generated tell)
- "Lorem ipsum" / "John Doe" placeholders
- Three equal cards in a row
- Inter at 96px hero, centered
- Bouncing arrow CTAs
- 300ms default transitions
- 140 more named fingerprints

Each rule has a severity (low/medium/high), a regex, a why-it's-bad explanation, and a concrete fix suggestion. The result is a 0-100 quality score.

Pipe it to your pre-commit hook:
`uxskill lint . --threshold high`
Or just get the score:
`uxskill lint . --score-only`

Browse all 145 rules: https://uxskill.laithjunaidy.com/anti-patterns.html

Install: pip install uxskill
GitHub: https://github.com/Laith0003/ux-skill

MIT. 223 tests pass.
```

---

## Day 1 (24 hours after launch): second-wave posts

### POST 7: X thread (7 tweets, post as thread)

```
1/ ux-skill v3.0 · THE BRAIN is live.

The biggest architectural shift since v1: brand specs aren't templates anymore. They're training data.

160 brands. 7 axes. Three modes. A closed feedback loop.

→ https://uxskill.laithjunaidy.com
```

```
2/ The 7 axes: warmth · contrast · density · geometry · formality · motion · type_personality.

Every brief maps deterministically to all seven. The values compile to palette + type ladder + spacing scale + radius + motion timing.

Same brief → same output. Always.
```

```
3/ Three modes, auto-dispatched:

→ strict_brand: 100% named brand tokens (fastest)
→ brand_anchor: 70% named + 30% axis-adapted (custom but fast)
→ pure_synthesis: 8 axis-matching brands distilled (infinity space)

The brief decides. You don't have to.
```

```
4/ The decisions ledger is the real Brain.

Every /ux-design and /ux-lint writes one line to .ux/decisions.jsonl.

The recommender reads it on the next call and bumps candidates that previously shipped clean for the same industry+ui_type.

The loop is closed.
```

```
5/ Other v3.0 hits:

→ 145 deterministic anti-pattern rules
→ 18 MCP tools (was 15)
→ /ux-evolve auto-loop with quality gate at 65
→ Layout primitives that can't produce broken layouts
→ 17 IDEs supported
→ 17 localized homepages
```

```
6/ Critically: NO LLM in the engine.

Generation is deterministic Python math. Scoring is regex + heuristics. The decisions log is JSONL on your disk.

Same brief → same output. Reproducible across machines. Runs on a plane.
```

```
7/ MIT license. 0 telemetry. 0 LLM calls in the engine. 223 tests pass.

pip install uxskill or npx uxskill init

GitHub: https://github.com/Laith0003/ux-skill
Launch post: https://uxskill.laithjunaidy.com/blog/v3-the-brain-launch.html
```

### POST 8: LinkedIn (Day 1 follow-up, post 24 hours after Day 0)

```
24 hours since v3.0 of ux-skill shipped. A short technical breakdown of the part I'm proudest of: the axis interaction matrix.

The 7-axis synthesizer has axes that sometimes compete for the same token. Example: density (push tight) and formality (push spacious in luxury contexts). Both look at the spacing token.

Before v3.0, whichever axis the primitive consulted first won implicitly. The output was correct but not predictable under load.

v3.0 documents the conflicts explicitly:

→ dense + corporate (Bloomberg-school) → 4px spacing: density wins
→ airy + corporate (luxury) → 12px spacing: formality wins
→ sharp + corporate (NYT) → 2px radius: geometry wins outright
→ soft + playful (Glossier) → 18px radius: geometry wins outright
→ high motion + corporate → kinetic timings dampened by 25%

The matrix lives in engine/synthesizer/interactions.py. Each function is tested against the named real-world archetype. Adding a new conflict requires registering the function name in a DOCUMENTED_INTERACTIONS tuple. Silent ad-hoc rules are blocked by the test suite.

Why does this matter? It removes ambiguity. The same brief now produces predictable output regardless of which primitive's code path runs first. Reproducible across machines, filesystems, Python versions.

GitHub: https://github.com/Laith0003/ux-skill
Wiki: https://github.com/Laith0003/ux-skill/wiki/Axis-Interaction-Matrix

MIT. Free.
```

---

## Day 2-3: niche deep-dives

### POST 9: Mastodon (Day 2)

```
ux-skill v3.0, for the design + dev folks on the Fediverse.

It's a Python design engine for AI coding tools. The thing I think you'll care about:

160 brand DESIGN specs (Apple, Stripe, Linear, Ferrari, Anthropic, 155 more) are no longer templates the engine picks from. They're TRAINING DATA the engine distills into a fresh design language per brief.

Same brief → same output. No LLM in the engine. Local decisions ledger learns from your work. MIT licensed.

https://uxskill.laithjunaidy.com
```

### POST 10: Bluesky (Day 2)

```
shipped a design engine for AI coding tools that runs without any LLM in the generation path

same brief → same output, every time. reproducible across machines. 160 brand specs as training data, not templates

pip install uxskill

https://github.com/Laith0003/ux-skill
```

### POST 11: Product Hunt (Day 2 or 3, schedule for a Tuesday-Thursday for best traffic)

**Tagline:** `Design intelligence for AI coding: a 7-axis synthesizer + closed feedback loop`

**Description:**

```
ux-skill v3.0 · THE BRAIN is an open-source design intelligence engine for AI coding tools (Claude Code, Cursor, Windsurf + 14 more IDEs).

Built different:
• 7-axis design synthesizer (warmth/contrast/density/geometry/formality/motion/type_personality)
• Three auto-dispatched modes (strict_brand / brand_anchor / pure_synthesis)
• 160 brand DESIGN specs as training data
• Local decisions ledger drives recommender re-rank
• 145 deterministic anti-pattern rules
• /ux-evolve auto-polish loop
• 18 MCP tools (Claude Desktop / Cursor compatible)
• 17 IDE integrations
• 223 tests passing

NO LLM in the engine. NO telemetry. MIT licensed.

The trick: brand specs become training data for the synthesizer (not templates it copies from). Output is novel every call but grounded in real brand vocabulary. Same brief always produces the same output. Reproducible across machines.

If you ship products via Claude Code or Cursor, ux-skill is the layer between you and the assistant that catches AI design slop before commit AND learns from your local work history over time.

pip install uxskill
```

---

## Day 7: momentum post

### POST 12: X / Twitter (Day 7 retrospective)

```
One week since ux-skill v3.0 shipped. Quick numbers:

- GitHub stars: [check actual count]
- PyPI downloads: [check]
- Discussions / issues opened: [check]
- HN comments: [check]

Open in v3.1 backlog:
- i18n keys for new sections (in flight)
- 2 linter rule bugs fixed (shipped)
- Round 7 anti-patterns 145 → 170

Keep going.

https://github.com/Laith0003/ux-skill
```

---

## Hashtag pool: use 3-5 per platform

| Platform | Recommended |
|---|---|
| X / Twitter | #AICoding #ClaudeCode #Cursor #OpenSource #DesignSystems |
| LinkedIn | #AICoding #DesignSystems #OpenSource #ClaudeCode #DeveloperTools |
| Mastodon | #opensource #design #ai #ClaudeCode |
| Bluesky | none needed (algorithmic feed) |
| Reddit | none in body; community-specific in title |

## Posting cadence (rough)

| When | Where | Post # |
|---|---|---|
| Hour 0 | X single | 1 |
| Hour 0 | LinkedIn | 2 |
| Hour 1 | HN | 3 |
| Hour 2 | Reddit r/ClaudeAI | 4 |
| Hour 3 | Reddit r/cursor | 5 |
| Hour 4 | Reddit r/webdev | 6 |
| Day 1 | X thread (7 tweets) | 7 |
| Day 1 | LinkedIn deep-dive | 8 |
| Day 2 | Mastodon | 9 |
| Day 2 | Bluesky | 10 |
| Day 3 (Tue) | Product Hunt | 11 |
| Day 7 | X retro | 12 |

## What I can't do

- Post on your behalf (security rules + standing repo rule "only commit + push")
- Create the X / LinkedIn / Reddit accounts
- Schedule via Buffer or any external tool
- Watch the engagement and reply

What I can do is keep the posts updated as numbers move (star count, test count, new features). Tell me when you want a v3.0.X retrospective version of the kit.

## Pre-flight checklist (run before Day 0)

- [ ] Homepage screenshot ready (1200×630 OG image, already exists at /og/home.png)
- [ ] GitHub release notes published (DONE, https://github.com/Laith0003/ux-skill/releases/tag/v3.0.0)
- [ ] PyPI page shows v3.0.0 (TODO, needs `pip publish`)
- [ ] npm page shows v3.0.0 (TODO, needs `npm publish`)
- [ ] CHANGELOG.md top entry is v3.0.0 (DONE)
- [ ] README.md hero says "v3.0.0 stable · THE BRAIN" (DONE)
- [ ] Verify uxskill.laithjunaidy.com loads (DONE, Cloudflare CDN cached)

Last two TODOs (PyPI + npm publish) need YOUR sign-off per Standing Rule #9. I'll prep the commands when you say apply.
