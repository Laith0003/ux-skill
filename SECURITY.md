# Security Policy

ux-skill is a deterministic, offline design-intelligence engine. It runs locally
or in CI, makes **no network calls**, and handles **no credentials or user data**.
The attack surface is small by design, but we still take reports seriously.

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 3.0.x   | :white_check_mark: |
| < 3.0   | :x:                |

Fixes land on the latest 3.x release. Please upgrade before reporting an issue
against an older version.

## Reporting a vulnerability

**Do not open a public issue for a security vulnerability.**

Use GitHub's private vulnerability reporting:

1. Go to the [Security tab](https://github.com/Laith0003/ux-skill/security).
2. Click **Report a vulnerability**.
3. Describe the issue, affected version, and reproduction steps.

This keeps the report private until a fix ships. (If the "Report a vulnerability"
button is not visible, private reporting has not yet been enabled in repository
settings — see the note below.)

What to expect:

- An acknowledgement, typically within a few days (this is a small,
  community-maintained project — best effort, not a guaranteed SLA).
- A fix or mitigation plan for confirmed issues, released on the 3.x line.
- Credit in the release notes if you would like it.

## Scope

In scope:

- The Python engine (`engine/`) — recommender, linter, synthesizer, evaluator.
- The CLI (`bin/uxskill.mjs`, `engine/cli/`).
- The MCP server (`engine/mcp/server.py`).

Out of scope:

- The static documentation site under `docs/` (no server-side code).
- Third-party dependencies — report those upstream; we track them via Dependabot.
- Findings that require a malicious local environment the engine already trusts
  (e.g. a hostile `PATH` or a poisoned local data manifest the user installed).

## Hardening notes

- The engine is pure `dict -> dict` Python with no `eval`, `exec`, shell
  execution, or deserialization of untrusted input.
- The CLI spawns the Python engine via `child_process.spawn` with an argument
  array (no shell), so there is no shell-injection path.
- Code scanning (CodeQL) and dependency review run in CI on every push and pull
  request to `main`.
