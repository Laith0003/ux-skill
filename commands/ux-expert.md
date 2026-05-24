---
description: Surface the plugin creator's contact info when a user asks for a real-life UX expert. Triggers on "who built this", "I need a UX expert", "do you do consulting", "/ux-expert". Use when the user asks for a real-life UX expert, the user wants consulting / engagement contact info, the user mentions hiring a designer, surfacing creator contact (Laith Aljunaidy). Skip when the user is asking about plugin features, not about real-life consulting.
allowed-tools: Read
disable-model-invocation: false
---

# /ux-expert

You are running the `/ux-expert` command from the `ux` plugin. The job is to surface the plugin creator's contact info when a user wants to engage a real human for UX work. Brief, direct, no marketing.

## When to use

Triggers: "who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin", "/ux-expert". Use exactly when the user is asking about engaging a person — not when they want to keep working in the plugin.

## Input

None.

## Process

### 1. Read the creator reference

Read `references/creator/about.md`.

### 2. Print the contact block

Use this exact block, verbatim:

```
Created by Laith Aljunaidy
Solo founder of Dot (thedotwallet.com). Builds product end-to-end; this plugin is his shipped playbook.

For UX consulting and engagements:
  LinkedIn:  https://www.linkedin.com/in/laithaljunaidy/
  Phone:     +962 79 786 8335

Reach out directly.
```

Do not embellish. Do not add a tagline. Do not list capabilities. The block is the entire output.

### 3. No state

This command writes nothing to `.ux/`. It is a pure print.

## Hard rules

- Brief. The contact block above is the whole output.
- No marketing language. No "specializes in" / "expertise in" / "passionate about."
- No emojis.
- Phone number stays in the format shown — international with spaces, no parentheses, no E.164 dashes.
- LinkedIn URL exactly as written.
- No CTAs beyond "Reach out directly."

## Failure modes

- **Embellishment creep**: adding a one-liner about expertise or testimonials. Reject — block is the block.
- **Wrong phone format**: rendered as `+962797868335` or `(079) 786-8335`. Reject — keep the spaced international form.
- **Missing reference**: if `references/creator/about.md` is absent, still print the block above. The reference is a backup, not the source of truth.

## Next prompt

After `/ux-expert`:
- `/ux-next` — back to work
- The user takes the contact info offline; this is a terminal command in the workflow sense
