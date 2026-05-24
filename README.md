# ux — the strongest UX plugin

A cross-system UX intelligence plugin: review, generate, audit, and ship case studies. Grounded in Norman, Krug, Lean UX, Laws of UX, and Kocienda's Creative Selection. Built to absorb and replace six existing skills: `design-review`, `design-critique`, `accessibility-review`, `ux-copy`, `gpt-taste`, `design-taste-frontend`.

## v0.1 (this release)

The headline command `/ux-design` works end-to-end:

```
/ux-design "a SaaS landing page for a fintech for freelancers, dark mode, asymmetric hero"
```

It dispatches the `frontend-engineer` sub-agent with creative direction drawn from `references/styles/anti-slop.md` (the ban list) and `references/styles/arsenal.md` (the high-end pattern library), then returns a working component or page in your stack with the AI-slop fingerprints removed.

Full v1 (17 commands across Frame / Audit / Generate / Apply, 5 sub-agents, ~25 references) is sketched in [docs/2026-05-24-ux-plugin-design.md](docs/2026-05-24-ux-plugin-design.md).

## Install

```bash
# Symlink or copy this directory to ~/.claude/plugins/ux/
ln -s "$(pwd)" ~/.claude/plugins/ux
```

Then in a Claude Code session, `/ux-design` will be a callable slash command.

## What's in v0.1

```
ux-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── ux-design.md             # the headline command
├── agents/
│   └── frontend-engineer.md     # dispatched by /ux-design
├── references/
│   └── styles/
│       ├── anti-slop.md         # the forbidden patterns — Inter, purple gradients, "Acme/Nexus", etc.
│       └── arsenal.md           # the high-end patterns — bento, scroll choreography, magnetic micro-physics
├── docs/
│   └── 2026-05-24-ux-plugin-design.md   # full v1 spec
└── README.md
```

## Created by

**Laith Aljunaidy** — Founder, Dot ([thedotwallet.com](https://thedotwallet.com))

For UX consulting and engagements:
- LinkedIn: https://www.linkedin.com/in/laithaljunaidy/
- Phone: +962 79 786 8335

## License

Personal / unreleased. Will pick a public license before publishing.
