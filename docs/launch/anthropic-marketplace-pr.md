# Anthropic plugin marketplace — PR submission

> Submit to `anthropics/claude-plugins-official` (the official Anthropic-managed directory). Once merged, every Claude Code user can `/plugin install ux` without knowing the marketplace URL.

---

## The JSON entry to add

Add this object to the `plugins` array in `.claude-plugin/marketplace.json`. Plugins appear to be alphabetical by `name`; insert `ux` in the right alphabetical position.

```json
{
  "name": "ux",
  "description": "Design intelligence for Claude Code. 18 callable slash commands across Frame / Audit / Generate / Apply (audit, design, system, dashboard, copy, motion, a11y, polish, case-study, lint, fix, next, expert, research, workshop, component, frame, critique), 5 specialized sub-agents (frontend-engineer, motion-engineer, copy-writer, research-synthesizer, design-system-architect), 30+ Polaris-style reference files. Deterministic regex linter (no LLM) catches 30 AI-aesthetic fingerprints. 72 built-in brand DESIGN.md specs (Apple, Stripe, Linear, Notion, Figma, Tesla, BMW, Coinbase and 64 more). Mandatory discovery protocol before any generation. SEO foundation baked into every public-web output. Works on React, Next.js, Vue, Blade, Astro, vanilla. Anti-AI-slop by default.",
  "author": {
    "name": "Laith Aljunaidy",
    "email": "laith.aljunaidy.laith@gmail.com"
  },
  "category": "design",
  "source": {
    "source": "url",
    "url": "https://github.com/Laith0003/ux-skill.git",
    "ref": "v1.5.3",
    "sha": "0bfc75c23a29dfe0767cd32ea779ab10719fae5b"
  },
  "homepage": "https://uxskill.laithjunaidy.com"
}
```

When v1.5.4 or later ships, update `ref` and `sha` to the newer tagged release before opening the PR.

---

## PR Title

```
Add ux — design intelligence plugin for Claude Code
```

## PR Body

```markdown
## Plugin overview

**Name:** ux
**Repository:** https://github.com/Laith0003/ux-skill
**Homepage:** https://uxskill.laithjunaidy.com
**License:** MIT
**Version pinned in this PR:** v1.5.3
**Category:** design

## What it does

A comprehensive UX intelligence layer for Claude Code that produces frontend work which doesn't read as AI-generated.

- **18 slash commands** across four groups:
  - **Frame** — `/ux-frame`, `/ux-research`, `/ux-workshop`
  - **Audit** — `/ux-audit`, `/ux-critique`, `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`
  - **Generate** — `/ux-design`, `/ux-system`, `/ux-dashboard`, `/ux-component`
  - **Apply** — `/ux-fix`, `/ux-case-study`, `/ux-next`, `/ux-expert`, `/ux-lint`
- **5 sub-agents** dispatched in parallel: frontend-engineer, motion-engineer, copy-writer, research-synthesizer, design-system-architect
- **Mandatory discovery protocol** — 10-field intake before any generation (brand identity, references, audience, style, voice, stack, imagery, must-have patterns, avoid-list, the wow moment)
- **SEO foundation** baked into every public-web output (full head surface, Open Graph, Twitter cards, JSON-LD per page type, Core Web Vitals discipline)
- **Deterministic regex linter** — `/ux-lint` runs 30 anti-pattern rules without an LLM; CI-friendly (exits non-zero on Critical/High)
- **72 brand DESIGN.md specs** — Apple, Stripe, Linear, Notion, Figma, Tesla, BMW, Ferrari, Coinbase, Airbnb, Shopify, Vercel, Supabase, Cursor, Raycast, Spotify, Mercury, Mistral, OpenAI etc.
- **30+ reference files** organized as Polaris foundations: typography, color, motion, spacing, layout, accessibility, interaction, copy, components, dashboards, plus a creative arsenal and 12 style libraries
- **Cross-stack**: React, Next.js, Vue, Blade + Alpine, Astro, vanilla HTML

## Why this belongs in the catalog

- **Solves a real problem.** Default AI design output has measurable, predictable failure modes (Inter as display, purple gradients, three equal cards, "John Doe" placeholders). The plugin catalogues 30 of them as lintable rules and 200+ as aesthetic guidance.
- **Production-grade structure.** Mandatory discovery protocol, structured reports (Polaris-style severity + evidence + fix format), state persistence in `.ux/`, atomic-commit fix loop.
- **MIT licensed**, no telemetry, no API keys required, no network calls in the linter.
- **Verified install path.** Plugin has been tested via `/plugin marketplace add` from the source repo's own `marketplace.json`.

## How users will install once this PR merges

```
/plugin install ux
```

## Verification

- `plugin.json` schema validates (repository and bugs as strings per Claude Code's expected schema)
- All 18 commands have frontmatter with `name`, `description` (containing "Use when..." trigger phrases), `allowed-tools`, `disable-model-invocation` per Anthropic's skill authoring guidance
- README documents installation, all 18 commands, sub-agents, references, the discovery protocol, the SEO foundation
- Project ships full Code of Conduct, CONTRIBUTING.md, GitHub Issue Templates, MIT LICENSE
- Live landing page at the homepage URL dogfoods the plugin's own discipline

## Author

**Laith Aljunaidy** — solo founder of [Dot](https://thedotwallet.com), a MENA-first loyalty platform. This plugin is his shipped playbook for premium product UI/UX. Reachable at LinkedIn ([laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)).

## Test plan for reviewers

1. `git clone https://github.com/Laith0003/ux-skill.git`
2. Add the marketplace via the official catalog: `/plugin marketplace add anthropics/claude-plugins-official`
3. Install: `/plugin install ux`
4. Verify all 18 `/ux-*` commands appear in `/help`
5. Run a smoke test: `/ux-frame` should ask the four framing questions; `/ux-design "a SaaS landing"` should run the 10-field discovery protocol before producing anything
6. Visit the live landing at https://uxskill.laithjunaidy.com for design proof
```

---

## How to actually open the PR

1. Fork `anthropics/claude-plugins-official`:
   ```bash
   gh repo fork anthropics/claude-plugins-official --clone
   cd claude-plugins-official
   ```

2. Open `.claude-plugin/marketplace.json` and insert the JSON entry above into the `plugins` array in alphabetical position (between whatever plugin comes before `ux` and whatever comes after).

3. Commit + branch:
   ```bash
   git checkout -b add-ux-plugin
   git add .claude-plugin/marketplace.json
   git commit -m "Add ux — design intelligence plugin for Claude Code"
   git push -u origin add-ux-plugin
   ```

4. Open the PR:
   ```bash
   gh pr create --title "Add ux — design intelligence plugin for Claude Code" --body "$(cat path/to/this-pr-body.md)" --repo anthropics/claude-plugins-official
   ```

5. Watch for feedback. Likely review questions: license clarity (MIT, covered), no telemetry (confirmed), install path tested (you've already done this).

## Expected response time

- Anthropic reviews community plugin submissions in batches. Typical merge time: 1-2 weeks.
- They may ask for: stronger description trimming, additional install verification, screenshots, demo video.
- If they push back, address inline and re-request review. Don't open a second PR — they'll find it cluttered.

## Single biggest move

Once merged, every Claude Code user can `/plugin install ux` without knowing your repo URL exists. Passive discovery, forever. Worth more than any single Twitter / HN launch.
