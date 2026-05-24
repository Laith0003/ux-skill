# How to install the ux plugin for Claude Code

Install the ux plugin in under 60 seconds. Three steps: clone the repo, symlink it into your Claude Code plugins directory, restart Claude Code. The plugin then exposes 17 slash commands and 5 sub-agents inside every Claude Code session.

---

## Prerequisites

You need:

- **Claude Code** installed and runnable from your shell. If you can run `claude` and get a session, you're set. If not, install it from the official Claude Code docs first.
- **Git** for cloning the repo. Pre-installed on macOS and most Linux distros. On Windows, install via [git-scm.com](https://git-scm.com/) or use WSL.
- A Claude Code account with plugin support enabled. Plugin discovery is on by default in current versions; if your `~/.claude/plugins/` directory doesn't exist, create it.

You do not need:

- Node, npm, or any package manager. The plugin is pure markdown and shell wrappers.
- A specific OS. macOS, Linux, and Windows (WSL or native PowerShell) all work.
- An API key beyond what Claude Code already needs.

---

## Step 1: Clone the repo

Pick a stable location to keep the clone — somewhere you won't accidentally delete it. Most users put it in `~/` or `~/code/`.

```bash
git clone https://github.com/Laith0003/ux-skill.git ~/ux-skill
```

This pulls the latest tagged release. The default branch is `main`, which always reflects the latest published version.

Verify the clone:

```bash
ls ~/ux-skill
# you should see: .claude-plugin/  agents/  commands/  references/  README.md  LICENSE
```

If the directory is empty or the clone failed, check your network and try again. The repo is public — no auth required.

---

## Step 2: Symlink into Claude Code's plugins directory

Claude Code reads plugins from `~/.claude/plugins/`. The plugin name (folder name inside that directory) is what Claude Code uses to namespace your commands.

### macOS and Linux

```bash
mkdir -p ~/.claude/plugins
ln -s ~/ux-skill ~/.claude/plugins/ux
```

The symlink approach keeps the plugin updateable via `git pull` from the clone location. Copying the directory instead of symlinking works, but you'll have to copy again on every update.

Verify the symlink:

```bash
ls -la ~/.claude/plugins/ux
# expected: ux -> /Users/<you>/ux-skill (or similar)
```

### Windows (PowerShell, native)

PowerShell 5+ supports symbolic links via `New-Item -ItemType SymbolicLink`. Run as Administrator if your account doesn't have symlink privilege.

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\.claude\plugins"
New-Item -ItemType SymbolicLink -Path "$HOME\.claude\plugins\ux" -Target "$HOME\ux-skill"
```

If symlink creation fails with a privilege error, enable Developer Mode in Windows Settings (Settings > Update & Security > For developers > Developer Mode), or run PowerShell as Administrator.

### Windows (WSL)

Use the macOS/Linux commands above inside your WSL distro. The plugin lives in the WSL filesystem; Claude Code launched from WSL will pick it up.

---

## Step 3: Restart Claude Code

Plugin discovery happens at startup. If you have a session open, exit and start a new one.

```bash
# end any running session, then:
claude
```

The plugin loads automatically on session start. There's no `enable` step.

---

## Step 4: Verify the install

Inside Claude Code, run any of the 17 plugin commands. The simplest sanity check is `/ux-frame`, which captures a project brief without doing any real work:

```
/ux-frame
```

Claude Code should respond with the framing prompt, not "unknown command." If you see "unknown command," see [Troubleshooting](#troubleshooting) below.

Alternative checks:

```
/help
```

Look for `/ux-frame`, `/ux-audit`, `/ux-design`, and the other 14 in the command list.

```
/ux-expert
```

Returns the author's consulting contact block. Confirms the plugin's reference files are reachable.

---

## Marketplace installation

When the plugin is published to the Claude Code marketplace, the install path collapses to one command:

```
/plugin install ux
```

This is the same plugin — same commands, same sub-agents, same references — distributed through the official marketplace channel. Use marketplace install if you want zero-touch updates pushed by the marketplace lifecycle. Use the git clone path above if you want to read the source, fork, or stay on a pinned version.

Both methods coexist; only run one at a time. If you've installed both, Claude Code will pick the marketplace copy and your symlink becomes dormant.

---

## Updating the plugin

The symlink approach makes updates a single command:

```bash
cd ~/ux-skill
git pull
```

That's it. The symlink already points at the directory, so Claude Code picks up the new files on the next session.

If you want to pin to a specific version, check out the tag instead of pulling main:

```bash
cd ~/ux-skill
git fetch --tags
git checkout v1.2.0
```

Switch back to main with `git checkout main && git pull`.

After updating, restart Claude Code so the new command frontmatter is parsed cleanly.

---

## Uninstalling

Remove the symlink. The clone stays on disk for re-installation later.

### macOS and Linux

```bash
rm ~/.claude/plugins/ux
```

### Windows (PowerShell)

```powershell
Remove-Item "$HOME\.claude\plugins\ux"
```

If you also want to remove the source clone:

```bash
rm -rf ~/ux-skill
```

Restart Claude Code. The slash commands disappear from `/help`.

---

## Troubleshooting

### "Unknown command: /ux-frame"

The plugin isn't being discovered. Run each of these in order until one fixes it:

1. **Confirm the symlink exists.** `ls -la ~/.claude/plugins/ux` should show a symlink pointing at your clone. If the result is "No such file," redo step 2.
2. **Confirm the clone is intact.** `ls ~/ux-skill/commands` should list 17 `.md` files. If empty, redo step 1.
3. **Confirm Claude Code restarted after symlinking.** Plugins are read at session start. Exit any current session and run `claude` again.
4. **Confirm plugin discovery is enabled.** Some Claude Code configurations disable plugin loading. Run `claude --help` and look for a plugins flag, or check `~/.claude/config.json` for a `plugins.enabled: false` field. Flip to `true` and restart.

### Commands appear in `/help` but error on run

Almost always a path issue inside a reference file. The plugin uses relative paths like `references/styles/anti-slop.md`; if your symlink is broken, Claude Code can't read those references.

Test by running:

```bash
cat ~/.claude/plugins/ux/references/styles/anti-slop.md | head -5
```

If you get "No such file," the symlink target is wrong. Recreate it.

### "Permission denied" on symlink creation (Windows)

Either enable Developer Mode in Windows Settings, or open PowerShell as Administrator. The first time, restart the shell after enabling Developer Mode.

### macOS Gatekeeper blocking the plugin

The plugin contains only markdown and shell wrappers — no compiled binaries — so Gatekeeper has nothing to block. If you see Gatekeeper warnings, the issue is somewhere else; check Claude Code's own permissions in System Settings > Privacy & Security.

### Multiple Claude Code installations

If you have Claude Code from both the marketplace and a manual install, they may use different plugins directories. Run:

```bash
claude --debug 2>&1 | grep plugins
```

to see which path is actively loading. Match your symlink to that path.

### Plugin loads but sub-agents fail to dispatch

This is rare and almost always a Claude Code version mismatch. Sub-agent dispatch requires a recent version of Claude Code that supports the `Task` tool with named sub-agents. Update Claude Code itself:

```bash
# follow your existing Claude Code update path — npm, brew, marketplace, etc.
```

### Still stuck

Open an issue at [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) with your OS, Claude Code version, and the exact error. Include the output of `ls -la ~/.claude/plugins/ux` and `ls ~/ux-skill`.

---

## Next steps

Install confirmed. Now:

1. **Read the [Discovery Protocol](Discovery-Protocol).** Every generation command runs the protocol. Reading it once means every subsequent generation makes sense.
2. **Skim [All 17 Commands](All-17-Commands).** You don't need to memorize them — they trigger on natural-language phrases like "audit this page" or "build me a pricing card" — but knowing what exists lets you reach for the right one.
3. **Run `/ux-frame` on your current project.** Captures audience, outcome, hypothesis, and success signal in a `.ux/last-frame.json` file that every downstream command reads. Five minutes; saves hours.
4. **Pick a starter command.** If you have an existing surface, run `/ux-audit` or `/ux-critique`. If you're starting fresh, run `/ux-design`. If you don't know, run `/ux-next` and let the plugin tell you.
5. **Skim the [Sub-Agents](All-5-Sub-Agents) page.** Once you've run a generation, knowing how the frontend-engineer, motion-engineer, and copy-writer split the work lets you steer them better on the next dispatch.

---

**See also**: [Installation](Installation) · [Discovery Protocol](Discovery-Protocol) · [All 17 Commands](All-17-Commands)
**Install**: `git clone https://github.com/Laith0003/ux-skill.git`
**Author**: [Laith Aljunaidy on LinkedIn](https://www.linkedin.com/in/laithaljunaidy/)
