# Launch plan: first wave

> Distribution playbook. Single-source-of-truth for the launch posts so I can re-use the copy verbatim or close to it.

## Show HN

**Time:** Tuesday or Wednesday, 8-11 AM ET. Tuesday > Wednesday.

**Title:**
> Show HN: A Claude Code plugin that catalogues every AI design fingerprint and refuses them

**URL:** https://uxskill.laithjunaidy.com

**First comment (post immediately as OP reply):** see `docs/launch/show-hn-comment.md`

## X (Twitter) thread

**Time:** Tuesday morning, parallel with the Show HN post. Pin to profile.

**Content:** see `docs/launch/twitter-thread.md`

## Reddit drops

After HN traction (or as parallel posts on Tuesday):

- `r/ClaudeAI`, title: "I shipped a Claude Code plugin that refuses default AI output. 30 fingerprints catalogued, 72 brand specs, deterministic lint."
- `r/webdev`, focus on the linter angle: "Made a regex-only AI-slop linter for frontend code. No LLM, no API key, runs in CI."
- `r/programming`, focus on the discipline angle: "Catalogued 30 deterministic anti-patterns AI frontend generators reach for, plus 37 motion principles, plus 72 brand specs"
- `r/SaaS`, focus on the design-system angle: "Free Claude Code plugin generates a full design system from a brand brief"
- `r/Frontend`: focus on Kowalski motion + ban list

Same body across all four, customized intro.

## Newsletter submissions

- TLDR Newsletter: https://tldr.tech/submit
- JavaScript Weekly: https://cooperpress.com/publications/javascript-weekly/
- React Newsletter: https://reactnewsletter.com/submit
- Frontend Focus: https://cooperpress.com/publications/frontend-focus/
- Bytes: https://bytes.dev/

Submit with the same hook: "ux-skill: Claude Code plugin that refuses default AI output. 18 slash commands, 5 sub-agents, deterministic linter, 72 brand DESIGN.md specs, MIT."

## Awesome lists (PR submissions)

- `awesome-claude-code` (search GitHub for this; there are usually 2-3 community lists)
- `awesome-design-systems`
- `awesome-ai-coding`
- `awesome-frontend-tools`

PR each one adding `ux-skill` with the description.

## Anthropic marketplace PR

Submit to `anthropics/claude-plugins-public` adding `ux` to the marketplace catalog. Single highest-leverage move: passive discovery forever.

## Tracking

Track star growth daily for the first 30 days. If a particular channel drives 10+ stars in a day, double down on that channel.

## What NOT to do

- Don't post on more than 2 platforms simultaneously (looks spammy)
- Don't link your own posts to each other from comments
- Don't fight critics on HN: concede, learn, ship the fix
- Don't claim "strongest ever" anywhere
- Don't use AI-generated post copy verbatim (HN smells it)

---

## Live launch state (auto-updated)

### Submitted PRs (waiting on review)

| PR | Repo | Status | Link |
|---|---|---|---|
| Anthropic marketplace (the big one) | `anthropics/claude-plugins-official` | Open | [#2010](https://github.com/anthropics/claude-plugins-official/pull/2010) |
| Claude Code Toolkit awesome list | `rohitg00/awesome-claude-code-toolkit` | Open | [#447](https://github.com/rohitg00/awesome-claude-code-toolkit/pull/447) |
| Composio awesome-claude-plugins | `ComposioHQ/awesome-claude-plugins` | Open | [#244](https://github.com/ComposioHQ/awesome-claude-plugins/pull/244) |
| CCplugins Design UX list | `ccplugins/awesome-claude-code-plugins` | Open | [#230](https://github.com/ccplugins/awesome-claude-code-plugins/pull/230) |

### Submitted on Day 1 (review timelines)

- Anthropic marketplace: 1-2 weeks typical
- Awesome lists: 2-3 days typical (community-maintained, faster turnaround)

### Watch for

- Anthropic reviewers may ask for: stronger description trimming, install verification, screenshots, demo video. Address inline.
- Awesome-list reviewers usually merge or close in one pass. If closed, ask why, usually a format issue.
- After 7 days of silence: leave one polite comment on the PR. Don't bump twice.

### Still blocked on user action

- ProductHunt: requires PH account login (see `producthunt-launch.md`)
- Hacker News Show HN: restricted on the current account; needs 1-2 weeks of karma-building first (see `show-hn-comment.md`)
- Twitter/X thread: image needs to be screenshot from the `tweet-hook` HTML mockup (see `twitter-thread.md`)

