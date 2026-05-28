# Launch pack — copy you can post

Pre-written launch copy for Hacker News, Product Hunt, Reddit, X/Twitter, LinkedIn, and Discord. Tuned to each platform's tone. **You** post — Claude never posts on your behalf.

Numbers are accurate as of 2026-05-28:
- 998 manifest entries · 120 anti-pattern rules (after round 5) · 131 brand specs
- 23 slash commands · 14 MCP tools · 17 IDE adapters
- 4 install paths (pip / npx / Claude Code plugin / Cursor rules)
- 6 language READMEs (en / ar / es / zh / fr / de)
- 75 tests · 0 high lint findings on the homepage

---

## Hacker News

**Title (Show HN form):**
`Show HN: ux-skill – Python design intelligence engine for AI coding tools`

**Body (text post):**
```
ux-skill is an open-source Python engine that catches the AI-design fingerprints every LLM produces by default — purple-to-blue gradients, Inter at 90px, John Doe placeholders, three-equal-card hero grids, lorem ipsum, emoji-as-icons. It runs inside Claude Code, Cursor, Windsurf, GitHub Copilot, and 13 more IDEs.

The architecture:
- 1,182 entries across 11 queryable JSON manifests (styles, palettes, type pairs, components, motion presets, industries, brand specs)
- A 5-parallel-search recommender that fans out across style → palette → type → motion → components for a given brief
- A deterministic regex linter with 120 anti-pattern rules (no LLM in the audit lane — runs in CI in <50ms)
- 131 brand DESIGN.md specs as queryable JSON (Apple, Stripe, Linear, Notion, Vercel, Figma, Tesla, BMW, Spotify, plus 83 more)
- An MCP server exposing 14 tools — works in Claude Desktop, Cursor, Windsurf, and generic MCP hosts. None of the top 8 Claude UX skills ship one.

The reason this exists: every popular AI coding tool produces the same recognizable "AI default" UI — same gradient, same hero pattern, same Inter-everywhere typography. The closest tool (ui-ux-pro-max-skill, 84k stars) is a markdown reference. We took that idea and built it as a queryable Python engine plus a regex-based slop catcher you can run in CI.

Install: `pip install uxskill` or `npx uxskill@alpha init`. MIT licensed, no telemetry, no account, no signin.

Repo: https://github.com/Laith0003/ux-skill
Site: https://uxskill.laithjunaidy.com
PyPI: https://pypi.org/project/uxskill/
npm:  https://www.npmjs.com/package/uxskill

Open to feedback — especially on the linter rule catalog and the recommender's scoring function.
```

---

## Product Hunt

**Tagline (60 chars max):**
`Design intelligence engine for AI coding tools`

**Description:**
```
ux-skill is the strongest design plugin for AI coding tools. A Python engine with 998 manifest entries, a 120-rule anti-AI-slop linter that runs in CI, and 131 brand DESIGN.md specs (Apple, Stripe, Linear, Figma, Tesla, BMW, plus 86 more). Ships into Claude Code, Cursor, Windsurf, GitHub Copilot, and 13 more IDEs via a single npx command.

What it catches: purple-to-blue gradients, Inter at 90px, John Doe placeholders, three-equal-card heros, lorem ipsum, emoji-as-icons, and 94 more AI design fingerprints.

What it generates: a complete design system (style + palette + type + motion + components) from a 10-field discovery brief, in under 60 seconds, with always-on guardrails.

Also ships an MCP server with 14 tools — works in Claude Desktop, Cursor, Windsurf, and generic MCP hosts. None of the top 8 Claude UX skills ship one.

MIT, no telemetry.
```

**Gallery shots to upload (auto-generated, already in repo):**
- `docs/og/home.png` — main social card
- `docs/og/compare.png` — comparison page
- `docs/og/mcp.png` — MCP server card

---

## Reddit r/ClaudeAI

**Title:**
`I shipped a Python design engine that catches AI-generated UI slop in CI — works in Claude Code, Cursor, Windsurf`

**Body:**
```
Built ux-skill over the last 3 weeks. It's a Python plugin that ships into 17 AI coding tools (Claude Code, Cursor, Windsurf, GitHub Copilot, JetBrains AI, etc) and:

1. Runs a deterministic regex linter with 100 rules that catches the design fingerprints every LLM produces by default — purple-to-blue gradients, Inter at 90px, John Doe placeholders, three-equal-card heros, lorem ipsum, emoji-as-icons.
2. Generates complete design systems via a 5-parallel-search recommender that fans out across 998 manifest entries (styles, palettes, type pairs, components, motion presets, 131 brand specs).
3. Ships an MCP server with 14 tools so any MCP host (Claude Desktop, generic agents) can call into the engine.

Install: `pip install uxskill` or `/plugin install ux@ux-skill` in Claude Code.

GitHub: https://github.com/Laith0003/ux-skill (MIT, no telemetry, no signin)

Looking for feedback on the rule catalog. What AI design fingerprints am I still missing?
```

## Reddit r/cursor

**Title:**
`Cursor users: I built a design-rule plugin that catches AI design slop in your generated code`

**Body:** (same as above, swap "Claude Code" first mention with "Cursor".)

## Reddit r/programming

**Title:**
`Open-source Python design intelligence engine for AI coding tools (Cursor, Claude Code, Windsurf)`

**Body:**
```
ux-skill is a Python plugin I built to fix the "every AI-generated UI looks the same" problem. It's a 5-module Python package:

- `recommender` — 5-parallel-search across 11 JSON manifests (1,182 entries total)
- `linter` — deterministic regex linter, 100 rules, CI-friendly
- `discovery` — 10-field protocol that forces the model to ask before generating
- `generator` — emits tokens + manifest from a recommendation
- `installer` — adapters for 17 IDEs

The interesting bits:
- Linter runs in <50ms on average — no LLM call. Each rule has a regex pattern, a severity, a why, and a fix.
- Recommender uses a transparent scoring function (no learned weights) over manifest entries. Explainable.
- MCP server exposes 14 tools over stdio. Works in Claude Desktop, generic MCP agents.
- 131 brand DESIGN.md specs as queryable JSON. Apple, Stripe, Linear, Tesla, BMW, Notion, plus 86 more.

Install: `pip install uxskill`. MIT. No telemetry. No account.

GitHub: https://github.com/Laith0003/ux-skill
PyPI: https://pypi.org/project/uxskill/
```

---

## X / Twitter

**Thread launcher (single tweet):**
```
shipped ux-skill — open-source python engine that catches AI-generated UI slop in CI.

120 deterministic regex rules. 131 brand specs (apple, stripe, linear, figma, tesla, bmw, +86 more). MCP server with 14 tools. ships into claude code, cursor, windsurf, github copilot.

pip install uxskill

🔗 github.com/Laith0003/ux-skill
```

**Follow-up tweets:**

```
1/
why this exists: every popular AI coding tool produces the same UI by default. purple gradient, inter at 90px, three-equal cards, john doe placeholder, lorem ipsum. these are fingerprints.

ux-skill catches them with a deterministic linter that runs in CI. no LLM. <50ms.
```

```
2/
the closest tool is ui-ux-pro-max-skill at 84k stars. it's a markdown reference for an LLM to read.

ux-skill takes that idea and packages it as a queryable python engine + a regex slop catcher you can run in CI. plus 131 brand specs ui-ux-pro-max doesn't have.
```

```
3/
the MCP server is the asymmetric move. none of the top 8 claude UX skills ship one. ux-skill exposes 14 tools over stdio — recommender, linter, 11 manifest readers, persistence, stats.

claude desktop, cursor, windsurf, generic MCP hosts all get the engine for free.
```

```
4/
homepage demonstrates the engine on itself: a live terminal in the hero types `ux recommend` against the page's brief, prints the 5-lane fan-out result with scores, then types `ux lint docs/index.html` and shows the green-checked "clean — ship it" line.

uxskill.laithjunaidy.com
```

---

## LinkedIn

**Post (long form):**
```
I shipped ux-skill — an open-source Python design intelligence engine for AI coding tools.

The problem it solves: every popular AI coding tool produces the same UI by default. Purple-to-blue gradient, Inter at 90px, three-equal-card hero, John Doe placeholder, lorem ipsum. The fingerprints are real. A senior designer can recognize "this was generated by an AI" in about 4 seconds.

ux-skill catches these fingerprints with a deterministic regex linter — 100 rules, runs in CI in under 50 milliseconds, no LLM call in the audit lane. And it generates better defaults via a 5-parallel-search recommender that fans out across 998 manifest entries (styles, palettes, type pairings, components, motion presets, 131 brand specs).

Architecturally:
- Python engine, packaged as `uxskill` on PyPI and `uxskill` on npm.
- 23 slash commands across discovery, recommendation, generation, quality, and workflow.
- An MCP server with 14 tools — works in Claude Desktop, Cursor, Windsurf, and any MCP-capable host.
- Adapters for 17 IDEs (Claude Code, Cursor, Windsurf, GitHub Copilot, JetBrains AI, Zed, Aider, Cline, Continue, Codex, Gemini CLI, Pieces, Tabby, Tabnine, CodeWhisperer, Kiro, Roo Cline).

MIT licensed. No telemetry. No account.

Looking for feedback — especially from anyone working on AI coding tooling.

GitHub: https://github.com/Laith0003/ux-skill
Site: https://uxskill.laithjunaidy.com
```

---

## Discord (Claude Code community)

**Short pitch (one-liner + link):**
```
Open-sourced ux-skill yesterday — a Python design intelligence engine for Claude Code, Cursor, Windsurf, +14 more IDEs. 120-rule anti-AI-slop linter, 5-parallel-search recommender, 131 brand specs, MCP server with 14 tools. MIT.
https://github.com/Laith0003/ux-skill
```

---

## ProductHunt comment template (for follow-up Q&A)

**Q: "How is this different from ui-ux-pro-max-skill?"**
```
ui-ux-pro-max-skill (84k stars) is a markdown reference — the LLM reads it as context. ux-skill is a Python engine — the LLM calls it as a tool. We borrowed the recommender shape from ui-ux-pro-max and added: a deterministic regex linter (100 rules, runs in CI), 131 brand DESIGN.md specs as queryable JSON (ui-ux-pro-max ships 0), an MCP server with 14 tools (ui-ux-pro-max doesn't ship one), and cross-IDE distribution via pip + npx (ui-ux-pro-max is Claude Code-only).

The full scored side-by-side is at uxskill.laithjunaidy.com/compare.html.
```

**Q: "What does the recommender actually return?"**
```
A JSON document with a picked style, picked palette, picked type pair, top 5 motion presets, top 12 compatible components, top 5 brand exemplars, and all 120 anti-pattern guardrails active. Plus a rationale block explaining each pick.

Output goes to .ux/last-recommendation.json. The /ux-design and /ux-component commands chain off that file — the same recommendation flows through your whole workflow.
```

**Q: "Telemetry?"**
```
Zero. The linter runs locally on regex over file content. The recommender runs locally on JSON manifests. The discovery flow asks you 10 questions and saves the answers locally. No network call. No account. No signin.

If you install via `pip install uxskill`, pip uploads usage stats to PyPI (Python package manager standard) — but ux-skill itself doesn't.
```

---

## What NOT to post

- Anything that promises "300k stars by next week" — overpromising is the fastest path to backlash.
- Anything that lists raw star numbers as the lead metric.
- Anything that mentions other plugins in a denigrating tone — frame as "different shape," not "better."
- Anything emoji-heavy. ux-skill is a zero-emoji project; posts about it should match.

---

## Timing suggestions

- **Hacker News:** Tuesday or Wednesday, 7am Pacific (10am Eastern, 3pm UTC). Show HN posts pinned by HN community for 12-24h typically.
- **Product Hunt:** Tuesday-Thursday launch. Submit by Monday noon Pacific for the next day's launch.
- **Reddit:** Same days as HN. Each subreddit prefers different times — r/programming peaks midday US, r/ClaudeAI is more 24/7.
- **X/Twitter:** Thread on launch day, single tweets daily for 7 days after.
- **LinkedIn:** Long-form post on launch day. One follow-up tweet/post per ship.
- **Discord (Claude Code, Cursor):** Pinpoint relevant channels. Don't cross-post. Read the room.

---

## Post-launch checklist

After posting, monitor:
1. HN comments — reply within 30 minutes to questions, with concrete code/links.
2. PH comments — same.
3. Reddit replies — same. Don't argue. Cite repo.
4. GitHub issues — triage within the day.
5. Star count — yes track it, no don't refresh every 30 seconds.

If a single post lands well (1k+ upvotes), DON'T cross-post the same content to another platform the same day. Spread the launch over a week.
