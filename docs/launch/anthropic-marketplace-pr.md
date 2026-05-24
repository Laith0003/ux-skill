# Anthropic plugin marketplace — submission (CORRECTED)

> **2026-05-24 correction:** the original guidance to PR `anthropics/claude-plugins-official` was wrong. That repo is curated by Anthropic with **no application process** — third-party PRs are auto-closed. The correct path is the community marketplace via the in-app submission form.

---

## TL;DR

Submit through the in-app form at **[claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)** (or the equivalent on platform.claude.com). Approved plugins land in **`anthropics/claude-plugins-community`** — the public community catalog that users add with:

```
/plugin marketplace add anthropics/claude-plugins-community
```

Then install ours via:

```
/plugin install ux@claude-community
```

---

## Why there are two marketplaces (clarified from the official docs)

| Marketplace | Who curates | How plugins get in |
|---|---|---|
| `claude-plugins-official` | Anthropic, at their discretion | No application process. PRs are auto-closed. Anthropic picks plugins to feature. |
| **`claude-plugins-community`** | The submission pipeline + automated safety screening | **The in-app form is the canonical path.** Approved plugins are pinned to a specific commit SHA, and CI bumps the pin automatically on new commits. |

The previous PR (`anthropics/claude-plugins-official#2010`) was opened against the wrong repo and got auto-closed within seconds. No harm done — the plugin's discoverability path is still the community marketplace, which is what reaches every Claude Code user once the catalog syncs nightly.

---

## What we have on our side (verified)

- `claude plugin validate .` **passes** against our `marketplace.json`
- Plugin is at v1.5.3, MIT-licensed, public on GitHub
- Live landing at https://uxskill.laithjunaidy.com (dogfood proof)
- Full README, CONTRIBUTING, Code of Conduct, Issue Templates already shipped
- 18 commands, 5 sub-agents, 30+ reference files, 72 brand specs

---

## Step-by-step: submit via the in-app form

1. Sign in to **[claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)** (or platform.claude.com/plugins/submit).
2. The form will ask for:
   - **Plugin name**: `ux`
   - **Repository URL**: `https://github.com/Laith0003/ux-skill`
   - **Description**: paste the one from `.claude-plugin/plugin.json` (already optimized; ~278 chars within their likely limit)
   - **Category**: design
   - **License**: MIT
   - **Homepage**: `https://uxskill.laithjunaidy.com`
   - **Author**: Laith Aljunaidy
3. The form runs the same `claude plugin validate` we ran locally + automated safety screening.
4. After approval, the plugin is pinned to a specific commit SHA in the [community catalog](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json). The public catalog syncs **nightly**, so expect a delay between approval and visible listing.

---

## How users install once we're in the community catalog

Two-command install in any Claude Code session:

```
/plugin marketplace add anthropics/claude-plugins-community
/plugin install ux@claude-community
```

If they've already added the community marketplace once (most users will, since it's the main third-party source), they just run the second command.

---

## How to check status

Search for `"name": "ux"` in the [community catalog file](https://github.com/anthropics/claude-plugins-community/blob/main/.claude-plugin/marketplace.json) to see if the plugin has appeared. Until it does, the existing self-hosted marketplace path still works for direct installs:

```
/plugin marketplace add https://github.com/Laith0003/ux-skill.git
/plugin install ux@ux-skill
```

This stays a valid fallback even after the community catalog merge.

---

## Why this matters

Once we're in `claude-plugins-community`:

- Every Claude Code user can install with two short commands
- The catalog is the canonical third-party source — users browse it from inside Claude Code
- Each new commit we push automatically updates the pinned SHA in the catalog (no manual PRs needed after the first approval)
- It's the highest-leverage passive-discovery channel that exists for Claude Code plugins

The original PR's intent — "passive discovery for every Claude Code user, forever" — is achieved by the community route, just via the in-app form rather than a GitHub PR.
