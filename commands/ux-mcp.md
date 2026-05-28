---
name: ux-mcp
description: Run the ux-skill engine as a Model Context Protocol server over stdio. Exposes 14 tools (recommender, linter, MASTER.md persistence, and the 11 data manifests) so ANY MCP-capable client — Claude Desktop, Cursor, Windsurf, generic agents — can query the engine without installing the full plugin.
allowed-tools: Bash
disable-model-invocation: false
---

# /ux-mcp — the design intelligence MCP

**One server. Fourteen tools. Every MCP-aware client gets the engine.**

This is the asymmetric move. None of the leading Claude UX skills (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ship an MCP server. Doing so turns ux-skill into the canonical *design-intelligence MCP* — agents in any host can call into the same recommender, linter, and manifests that the plugin uses, without needing to install the plugin itself.

## When to use

- You're using **Cursor**, **Windsurf**, **Claude Desktop**, or any other MCP-capable host and want ux-skill available without forcing the host to learn the plugin layout.
- You're orchestrating a **multi-agent pipeline** and need a single source of truth for design constraints across agents.
- You're writing **CI tooling** that calls the recommender or linter from a long-running daemon rather than spawning a CLI each time.

## When to skip

- You're already inside Claude Code with the plugin installed — the slash commands hit the engine directly, no MCP transport needed.
- You only need a one-shot recommendation or lint — `ux recommend` / `ux lint` from the CLI is simpler.

## Install

The MCP transport is an **optional dependency** to keep the base install slim:

```bash
pip install 'uxskill[mcp]'
```

Or, if you already have `uxskill`:

```bash
pip install 'mcp>=1.0'
```

## Start the server

```bash
ux-mcp                       # entry point (preferred — wired by pyproject.toml)
python3 -m engine.mcp.server # equivalent module form
```

The server speaks stdio JSON-RPC. Logs go to **stderr only**; stdout is reserved for the protocol stream.

## Exposed tools (14)

| Tool | What it does |
|---|---|
| `ux_recommend` | Run the 5-parallel-search recommender over a brief. Returns style + palette + type pair + motion + components + brand exemplars + guardrails + rationale. |
| `ux_lint` | Run the anti-AI-slop regex linter over paths. Returns findings with rule id, severity, file, line, excerpt, fix. |
| `ux_styles` | Return all 84+ entries from `data/styles.json`. |
| `ux_palettes` | Return all 176+ entries from `data/palettes.json`. Optional `mode` filter (`light` / `dark`). |
| `ux_type_pairs` | Return all 70+ entries from `data/type-pairs.json`. |
| `ux_components` | Return all 148+ entries from `data/components.json`. Optional `category` filter. |
| `ux_industries` | Return all 184+ entries from `data/industries.json`. Optional `category` filter. |
| `ux_motion_presets` | Return all 57+ entries from `data/motion-presets.json`. Optional `category` filter. |
| `ux_anti_patterns` | Return all 35+ regex rules from `data/anti-patterns.json`. Optional `severity` filter. |
| `ux_brands` | Return all 72 brand specs from `data/brands/*.json` (Apple, Stripe, Linear, Tesla, Notion, etc.). Optional `category` filter. |
| `ux_landing_patterns` | Return all 24+ entries from `data/landing-patterns.json`. Optional `category` filter. |
| `ux_persist_save` | Persist a recommendation as `.ux/design-system/MASTER.md` in a given project root. Idempotent — same input writes byte-identical bytes. |
| `ux_persist_load` | Load `.ux/design-system/MASTER.md` back into a structured dict. |
| `ux_stats` | Return the engine version and per-manifest entry counts. Useful as a health probe. |

## Client configuration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "ux-skill": {
      "command": "ux-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

If `ux-mcp` isn't on PATH, replace `"ux-mcp"` with the absolute path printed by `which ux-mcp`.

### Cursor

In `.cursor/mcp.json` at your project root (or globally at `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "ux-skill": {
      "command": "ux-mcp"
    }
  }
}
```

Then add a one-line hint to `.cursorrules`:

```
When designing UI, call the ux-skill MCP tools first: ux_recommend for the system, ux_lint to catch slop.
```

### Windsurf

In `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "ux-skill": {
      "command": "ux-mcp"
    }
  }
}
```

### Generic stdio client

Any MCP client supporting stdio transport works. Spawn `ux-mcp` as a subprocess and exchange JSON-RPC frames on stdin/stdout. Logs land on stderr.

## Example tool calls

### `ux_recommend`

```json
{
  "brief": {
    "project_type": "landing",
    "industry": "fintech-neobank",
    "audience": ["founders", "operators"],
    "tone": ["warm", "editorial", "precise"],
    "must_have": ["dark-mode", "a11y-AA"],
    "forbidden": ["brutalism", "purple-gradients"],
    "stack": "nextjs-15-app-router",
    "region": "mena"
  }
}
```

Returns the full Recommendation: a picked style, palette, type pair, top 5 motion presets, top 12 compatible components, top 5 brand exemplars, all 35+ anti-pattern guardrails, and a rationale list explaining each pick.

### `ux_lint`

```json
{
  "paths": ["./app", "./components"],
  "threshold": "high"
}
```

Returns `{ findings, files_scanned, rules_loaded, exit_code, summary }`. `exit_code` is 1 if any finding meets or exceeds the threshold.

### `ux_palettes`

```json
{ "mode": "dark" }
```

Returns only dark-mode palettes.

### `ux_persist_save`

```json
{
  "project_root": "/absolute/path/to/project",
  "recommendation": { "...": "from ux_recommend" },
  "brief": { "project_type": "landing" }
}
```

Writes `.ux/design-system/MASTER.md` and returns the absolute file path.

## How it works

The transport is **separated from the handlers**. Each tool is a pure `dict -> dict` Python function in `engine.mcp.server`, exercised by tests directly. `run_server()` is a thin async wrapper that wires those handlers into `mcp.server.stdio.stdio_server()`.

This means:

- The `engine.mcp` module imports cleanly **whether or not** the `mcp` Python package is installed.
- `ux-mcp` fails fast with a clear `pip install` hint if the transport library is missing.
- Tests run without the transport — no event loop, no subprocess plumbing.

## Why this is asymmetric

| Plugin | MCP server | Reach |
|---|---|---|
| **ux-skill** | yes (this) | any MCP host |
| ui-ux-pro-max-skill | no | Claude Code only |
| open-design | no | Claude Code only |
| taste-skill | no | Claude Code only |
| huashu-design | no | Claude Code only |
| stitch-skills | no | Claude Code only |
| nothing-design-skill | no | Claude Code only |
| hallmark | no | Claude Code only |
| material-3-skill | no | Claude Code only |

The competition is locked into Claude Code's plugin runtime. The MCP server makes ux-skill reachable from any agent — including agents that don't know what a "Claude Code plugin" is.

## Errors

- **`mcp package not installed`** → run `pip install 'uxskill[mcp]'` and try again.
- **`Unknown tool: foo`** → the tool name in the JSON-RPC call doesn't match one of the 14 in `TOOLS`. Check the table above.
- **`engine.mcp.server` import error** → likely pydantic missing from your environment; `pip install 'uxskill'` reinstalls the base deps.
