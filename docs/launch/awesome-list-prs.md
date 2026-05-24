# Awesome-list PR submissions

> "Awesome" lists are curated GitHub repos that link to top resources in a category. Getting listed = passive SEO + backlinks + GitHub traffic. Each list has its own contribution format; follow the existing pattern in their README.

---

## Target lists (priority order)

### 1. awesome-claude-code (highest priority — direct audience)

**Where to look:** GitHub search for `awesome-claude-code` returns multiple community lists. Top candidates:
- `hesreallyhim/awesome-claude-code`
- `langgptai/awesome-claude-code`
- `coleam00/awesome-claude-code` (if active)

Pick whichever is most-starred + most-recently-maintained.

**PR title:**
```
Add ux-skill — comprehensive UX plugin
```

**PR body:**
```markdown
## Adding: ux-skill

A comprehensive UX intelligence plugin for Claude Code that produces frontend work that doesn't read as AI-generated.

- **Repo:** https://github.com/Laith0003/ux-skill
- **Live:** https://uxskill.laithjunaidy.com
- **License:** MIT
- **Category:** Plugins / Design / Frontend (insert where it fits the list's structure)

**What it does:**
- 18 callable slash commands (`/ux-design`, `/ux-audit`, `/ux-system`, `/ux-dashboard`, `/ux-lint`, `/ux-case-study`, and 12 more)
- 5 specialized sub-agents (frontend-engineer, motion-engineer, copy-writer, research-synthesizer, design-system-architect)
- 30+ Polaris-style reference files
- 72 brand DESIGN.md specs (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Coinbase, Airbnb, Spotify, etc.)
- Deterministic regex linter (no LLM) catching 30 AI-aesthetic fingerprints
- Mandatory 10-field discovery protocol before any generation
- SEO foundation baked into every public-web output
- Cross-stack: React, Next.js, Vue, Blade, Astro, vanilla

**Install:**
```
/plugin marketplace add https://github.com/Laith0003/ux-skill.git
/plugin install ux@ux-skill
```

Active development, MIT-licensed, no telemetry.
```

**The exact entry to add to the list's README** (adapt format to match existing entries):
```
- [ux-skill](https://github.com/Laith0003/ux-skill) — Comprehensive UX plugin: 18 slash commands, 5 sub-agents, deterministic linter, 72 brand DESIGN.md specs. Anti-AI-slop discipline. MIT.
```

---

### 2. awesome-design-systems (high priority — overlap with our brand library)

**Likely repo:** `klaufel/awesome-design-systems` (popular, 4k+ stars) or `alexpate/awesome-design-systems`.

**Adapted PR rationale:** ux-skill ships specs for 72 design systems (`references/brands/_index.md`) including Apple, Stripe, Linear, Figma, Tesla, BMW, Coinbase, Airbnb, Shopify, Vercel, Supabase, Cursor, Raycast, Spotify — useful as a reference catalogue for designers studying systems.

**PR title:**
```
Add ux-skill — 72 brand DESIGN.md specs as a reference library
```

**The exact entry to add** (under "Tools" or "Resources" section, depending on list structure):
```
- [ux-skill](https://github.com/Laith0003/ux-skill) — Open-source library of 72 brand DESIGN.md specs (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify and 64 more), plus a Claude Code plugin that uses them to generate work matching a named brand's design language.
```

**PR body should emphasize the brand-library angle** — that's what their list cares about. Don't lead with the plugin features.

---

### 3. awesome-ai-coding

**Likely repo:** `dotneet/awesome-ai-agents-and-tools` or similar. Search GitHub for "awesome-ai-coding" or "awesome-claude" — multiple community lists exist.

**Adapted PR rationale:** ux-skill is one of the most thorough AI-coding plugins focused specifically on design+frontend quality (most AI-coding tools focus on logic/algorithms; this one tackles aesthetic).

**PR title:**
```
Add ux-skill — design-focused Claude Code plugin
```

**The exact entry:**
```
- [ux-skill](https://github.com/Laith0003/ux-skill) — Claude Code plugin focused on producing frontend code that doesn't read as AI-generated. 18 slash commands, deterministic anti-pattern linter, 72 brand DESIGN.md specs.
```

---

## Process for each PR

For each of the 3 target lists:

1. **Find the canonical repo** — `gh search repos awesome-<topic>` and pick the top-starred one that's been updated in the last 90 days.
2. **Read the list's CONTRIBUTING.md or README** — they all have specific rules (alphabetical order, formatting, no broken links, license requirement).
3. **Fork the repo.**
4. **Add the entry** in the right section + right alphabetical position. Match the existing entry format exactly (em dash, no em dash, one-line, etc.).
5. **Commit** with a tight message:
   ```bash
   git checkout -b add-ux-skill
   git commit -m "Add ux-skill"
   git push -u origin add-ux-skill
   ```
6. **Open PR** with the title + body above.
7. **Wait** — most awesome lists merge within a few days. Some take weeks. Don't bump them.

## Additional awesome lists to consider (lower priority but easy wins)

- `awesome-frontend-tools` — for the linter angle
- `awesome-claude-prompts` — for the discovery protocol pattern
- `awesome-anthropic` (if it exists) — for the Claude-ecosystem angle
- `awesome-stackoverflow-questions` — no, that's a joke; the list might not be real but it shows the pattern: there's probably an awesome list for any niche you can name

## Why this matters

- Each merged PR = a permanent backlink from a 1k–10k-star repo to your project
- Google reads these as authority signals
- Direct GitHub traffic — every visitor to an awesome list scrolling for tools might click through
- Cumulative: 3-5 merged PRs add up to noticeable steady traffic over months

## Realistic expectation

- 1-3 of the 3 will merge within 2 weeks
- Each merged PR adds 5-20 stars over the following month (cumulative, not viral)
- The compounding signal matters more than the immediate spike — search rankings improve

---

## What NOT to do

- Don't submit to multiple lists simultaneously and link them to each other in PR descriptions ("I'm also adding this to X list") — looks spammy
- Don't argue with maintainers who reject for format reasons; fix the format and re-submit
- Don't open PRs adding multiple of your own projects; awesome-list maintainers will detect the pattern
- Don't write PR descriptions in marketing voice — these are technical curators, not consumers
