---
name: ux-skill
description: Use when designing, auditing, recommending, linting, or polishing frontend UX with ux-skill's deterministic design engine, anti-AI-slop linter, brand references, command recipes, and optional MCP tools. This skill translates the Claude Code /ux-* workflows into Codex prompts plus uxskill CLI or MCP calls while preserving Claude plugin support.
metadata:
  short-description: UX design engine, linter, and brand guidance
---

# ux-skill

ux-skill is a Codex skill wrapper around the same assets used by the Claude Code
plugin:

- `commands/*.md` are the canonical Claude slash-command recipes. In Codex,
  treat them as workflow specs, not native slash commands.
- `agents/*.md` are Claude Code sub-agent role specs. In Codex, use them as role
  references when doing implementation, copy, motion, research, or design-system
  work.
- `references/` contains the design laws, foundations, anti-slop guidance,
  process docs, output formats, and brand references.
- `data/` contains the deterministic manifests used by the Python engine.
- `engine/` and `bin/` provide the CLI, linter, recommender, synthesizer, and MCP
  server.

## Codex workflow

1. Load the most relevant command spec from `commands/` when the user asks for a
   ux-skill workflow.
2. Prefer the `uxskill` or `ux` CLI for deterministic work:
   - `uxskill stats`
   - `uxskill discover`
   - `uxskill recommend --brief-file .ux/last-discovery.json`
   - `uxskill lint .`
3. If an MCP server named `uxskill` is available, prefer its tools for
   recommender, linter, stats, manifest lookup, synthesis, and decisions queries.
4. Use `references/styles/anti-slop.md`, `references/foundations/*`, and
   `references/brands/*` as needed for design judgment. Load only the specific
   reference files needed for the task.
5. After generating or editing UI, run `uxskill lint .` when feasible and report
   the score/findings.

## Claude-only features in Codex

These features are preserved for Claude Code but are not native Codex features:

- Direct slash command invocation such as `/ux-audit`.
- Claude Code `Task` dispatch to named sub-agents.
- Claude plugin marketplace install from `.claude-plugin/`.
- Claude launch config under `.claude/`.

In Codex, translate those to prompts plus CLI/MCP calls. For example, "run the
equivalent of `/ux-audit`" means read `commands/ux-audit.md`, inspect the
surface, produce the same structured report, and optionally run CLI/MCP checks.

## Command translations

Use these examples when a user asks for a Claude slash command inside Codex:

- `/ux-init`: "Use ux-skill to bootstrap this project for Codex. Run
  `uxskill init`, verify `uxskill stats`, and tell me which files changed."
- `/ux-discover`: "Use ux-skill discovery. Ask the 10 required brief fields,
  save them to `.ux/last-discovery.json`, then recommend next steps."
- `/ux-recommend`: "Use ux-skill to recommend a design system from the saved
  discovery brief. Run `uxskill recommend --brief-file .ux/last-discovery.json`
  and summarize the tokens, components, motion, brands, and guardrails."
- `/ux-audit`: "Use ux-skill to audit this surface. Follow
  `commands/ux-audit.md`, run the six lenses, cite evidence, assign severity,
  and save `.ux/last-audit.json` if edits are in scope."
- `/ux-stats`: "Run `uxskill stats` and summarize the manifest counts."

## MCP

When MCP is configured, use the `uxskill` server for deterministic context.
The server command is:

```bash
ux-mcp
```

Typical Codex config:

```toml
[mcp_servers.uxskill]
command = "ux-mcp"
args = []
startup_timeout_sec = 30
```

