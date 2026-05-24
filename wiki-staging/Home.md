# ux plugin for Claude Code — anti-AI-slop design intelligence

The `ux` plugin is a Claude Code plugin that turns your terminal into a senior product designer — 17 slash commands, 5 sub-agents, 30+ reference files, all engineered to defeat the AI-aesthetic fingerprints that mark generated work as machine-made.

---

## The pitch

You're shipping a SaaS, a product, a landing page, a dashboard, a component — and you refuse to ship work that looks AI-generated. The `ux` plugin is the discipline you've been missing. It runs a 10-field discovery protocol before it writes a line of code, dispatches specialized sub-agents for parallel work, enforces a 60+ pattern arsenal, and bans the defaults that betray model output: Inter on everything, purple-blue gradients, three equal cards, centered hero over dark image, "John Doe", `99.99%`, "Elevate / Seamless / Unleash".

The bar is what the best premium SaaS sites actually do — studied directly, codified as native guidance. Every command reads the reference files before it produces output. Every generation command refuses to start without the wow moment.

Built by a solo founder shipping a real product against real partners in a real market. Field-tested, not theoretical.

---

## Quick start

Install in under 60 seconds. Three lines:

```bash
git clone https://github.com/Laith0003/ux-skill.git ~/ux-skill
ln -s ~/ux-skill ~/.claude/plugins/ux
# restart Claude Code, then run /ux-frame to capture your first brief
```

Full install instructions, marketplace path, and troubleshooting: [Installation](Installation).

---

## The 4 command groups

Seventeen commands. Four groups. One workflow.

- **FRAME** — set the brief before you build. `/ux-frame`, `/ux-research`, `/ux-workshop`. Lean-UX intake, study planning, design-thinking facilitation. The work upstream of the design.
- **AUDIT** — review what exists. `/ux-audit`, `/ux-critique`, `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`. Six lenses on the surface, each producing structured findings with severity, evidence, and fix.
- **GENERATE** — produce the artifact. `/ux-design`, `/ux-system`, `/ux-dashboard`, `/ux-component`. Anti-slop output dispatched through sub-agents with full creative direction.
- **APPLY** — act on findings. `/ux-fix`, `/ux-case-study`, `/ux-next`, `/ux-expert`. The fix loop, the publishable wrap-up, the workflow conductor, the real-life consulting contact.

Full reference with trigger phrases, inputs, outputs, and code examples: [All 17 Commands](All-17-Commands).

---

## The 5 sub-agents

Generation commands don't write code directly. They dispatch specialized sub-agents that own one discipline each.

- **frontend-engineer** — production-grade React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro. Anti-AI-slop discipline. SEO surface for public-web outputs.
- **motion-engineer** — Framer Motion, GSAP, CSS animations. Easing curves, spring physics, scroll choreography, reduced-motion fallbacks. Performance-conscious.
- **copy-writer** — error specificity, empty states, CTAs, helper text, microcopy. Owns voice consistency across every state of a surface.
- **research-synthesizer** — digests interviews, analytics, competitive sites, A/B results, support tickets into themes with confidence labels and actionable recommendations.
- **design-system-architect** — tokens, foundations, component contracts, dark-mode pairings, theming. Builds the system the other sub-agents build against.

Full dispatch contracts, inputs, outputs, and discipline: [All 5 Sub-Agents](All-5-Sub-Agents).

---

## The discovery protocol

Every generation command runs a mandatory 10-field intake before producing anything. Brand identity, reference inspirations, product type and audience, style direction, voice, stack, imagery sources, must-have patterns, avoid list, and the wow moment. Improvisation is banned. The plugin asks before it builds. The wow moment is the most important question — without it, the model produces a competent Apple-clean landing that nobody remembers 24 hours later.

The protocol groups the 10 fields into 2-3 conversational messages, never a single wall. Skip conditions are narrow: `--skip-discovery` flag, complete spec in one message, or iteration on a prior artifact via `.ux/last-frame.json`.

Full protocol, field-by-field intake scripts, delivery rules, and hard rules: [Discovery Protocol](Discovery-Protocol).

---

## The SEO foundation

Every public-web output ships with the full head surface — title, description, charset, viewport, theme-color, canonical, Open Graph cards, Twitter cards, JSON-LD structured data per page type, semantic HTML landmarks, image discipline, font preloading, Core Web Vitals patterns. SEO is not bolted on after generation. It's a foundation, like accessibility. The frontend-engineer refuses to ship a landing page without it.

Components, dashboards, and other behind-auth surfaces don't get the full surface — no canonical, no OG cards — but they still get semantic HTML and image discipline.

---

## Real-life UX consulting

The plugin is open source under MIT. The author also takes consulting work directly — design reviews, full audits, system-level critiques, pre-launch readiness, MENA-market positioning, anti-slop sessions for teams whose surfaces have started reading as AI-generated, founder mentorship for early-stage builders. Run `/ux-expert` inside Claude Code, or jump straight to the contact: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/).

---

## Wiki index

Read the wiki tier-by-tier. Start with installation, capture a brief, run a generation.

### Tier 1 — Get started

- [Installation](Installation) — clone, symlink, restart, verify
- [Discovery Protocol](Discovery-Protocol) — the 10-field intake every generation command runs
- [All 17 Commands](All-17-Commands) — full reference with trigger phrases and examples
- [All 5 Sub-Agents](All-5-Sub-Agents) — dispatch contracts and discipline

### Tier 2 — The workflow (planned)

- FRAME workflow — `/ux-frame`, `/ux-research`, `/ux-workshop` end-to-end
- AUDIT workflow — picking the right review command for the symptom
- GENERATE workflow — from brief to shipped surface
- APPLY workflow — the fix loop and workflow conductor

### Tier 3 — The reference library (planned)

- foundations — accessibility, color, components, copy, dashboards, interaction, layout, motion, seo, spacing, typography
- laws — Norman, Krug, the 30 laws of UX
- styles — anti-slop tells, the arsenal, the style library, exemplars
- process — Lean UX, design thinking, creative selection, generation modes, visual translation, refactor-existing

### Tier 4 — Stacks and patterns (planned)

- React + Tailwind output rules
- Next.js App Router + RSC safety
- Vue 3 output rules
- Blade + Alpine + HTMX output rules
- Vanilla HTML + Astro output rules
- The arsenal — 60+ patterns to reach for
- The anti-slop ban list — every AI fingerprint with do-instead

### Tier 5 — Operate and extend (planned)

- The `.ux/` state directory — what each `last-*.json` file means
- Writing your own reference file
- Contributing to the plugin
- Roadmap and v2 plans

---

## Plugin facts

- 17 callable slash commands, 5 specialized sub-agents, 30+ reference files
- 19,000+ lines of curated UX guidance
- MIT licensed, open source
- v1.2 — SEO foundation baked in as mandatory discipline for public-web outputs
- v1.1 — Discovery protocol enforced before any generation
- Supported stacks: React, Next.js (App Router), Vue, Blade + Alpine + HTMX, vanilla HTML, Astro, Svelte
- Built for: anyone shipping a SaaS, product, or partner-facing surface who refuses to ship work that looks AI-generated

---

**See also**: [Installation](Installation) · [Discovery Protocol](Discovery-Protocol) · [All 17 Commands](All-17-Commands)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
