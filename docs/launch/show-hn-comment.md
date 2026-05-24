# Show HN — paste-ready

> Post Tuesday or Wednesday 8–11 AM ET. Post the first comment as an OP reply within 60 seconds of submitting.

---

## Title

```
Show HN: I built a Claude Code plugin that catalogues 30 AI design fingerprints and refuses every one
```

**Why this title:** specific (30), direct ("I built"), contrarian stance ("refuses"), audience signal ("Claude Code plugin"), curiosity gap ("what are the 30?"). Avoids superlatives. Avoids the repo name as bait. Reads like an engineer's note, not a marketing post.

## URL

```
https://uxskill.laithjunaidy.com
```

**Why not the GitHub repo:** the landing is the proof. Visitor sees the live `/ux-design` typewriter, the discipline in action, and the install command in one scroll. The repo URL goes in the OP comment below.

## Body field

Leave the body blank. URL-only Show HN posts perform better; the comment carries the depth.

---

## First comment — post immediately as your own reply

> Markdown-light works on HN (paragraph breaks via blank line; lists need blank line above + dash-space prefix; code blocks use four-space indent).

```
I'm Laith, a solo founder shipping a MENA loyalty platform. I kept hitting the same wall: I'd ask Claude Code to build me a landing, and what came back was clean — but it had the same fingerprints every time. Same fonts, same gradients, same "John Doe."

So I started cataloguing them. There are now:

- 30 deterministic anti-patterns with regex/DOM detection. The /ux-lint command runs them without an LLM and exits non-zero on Critical/High — wire it into your CI.
- 37 motion principles synthesized from Emil Kowalski's design-engineering work (Sonner/Vaul author).
- 72 brand DESIGN.md specs — Apple, Stripe, Linear, Figma, Tesla, BMW, Coinbase, Notion, Airbnb, Spotify, etc. Tell the plugin "build me a landing in Stripe's style" and it reads the actual brand language, not a generic default.
- 18 slash commands across Frame / Audit / Generate / Apply.
- 5 sub-agents dispatched in parallel (frontend-engineer, motion-engineer, copy-writer, research-synthesizer, design-system-architect).
- A discovery protocol that runs a mandatory 10-field intake before generating anything. Push back on "anything's fine" — there's no improvisation.

Some of what the linter catches:

- Inter as the brand display face (Inter is fine for body)
- Purple-to-blue gradients on white
- Three equal cards in a row
- "John Doe" / "Acme" / 99.99% in placeholders
- Centered hero over a dark image
- h-screen on mobile (should be min-h-[100dvh])
- Animating width/height/top/left instead of transform + opacity
- Marketing filler verbs ("Elevate", "Seamless", "Unleash")

Install in any Claude Code session:

    /plugin marketplace add https://github.com/Laith0003/ux-skill.git
    /plugin install ux@ux-skill

Then /ux-design "a SaaS landing for X" — the plugin asks ten discovery questions, then dispatches the frontend-engineer with the bans + arsenal + brand spec loaded.

Open to critique. Especially interested in fingerprints I missed and brand specs I should add to the library.

Repo: https://github.com/Laith0003/ux-skill (MIT)
Landing (dogfooded by the plugin itself): https://uxskill.laithjunaidy.com
```

---

## What to do after submitting

**Minute 0:** submit with the title + URL above. Don't fill the body field.

**Minute 1:** post the first comment above as a reply to your own submission. Don't edit it after posting — HN penalizes edits within the first 10 minutes.

**Minutes 2–60:** watch for comments. Reply to every one within 15 minutes. HN engagement signals push you up the rank.

**Reply patterns that work:**
- Critical comment: concede the point, add nuance, link to where you address it (or commit to addressing it).
- Feature request: link to the relevant existing command if it already does the thing, OR add it to the issue tracker and tag the commenter.
- "Looks AI-generated" jab: paste the lint output of your own page passing; let the work speak.
- "How is this different from X?": one-line factual comparison + link to the README's comparison section if X is a known competitor.

**What NOT to do:**
- Don't say "we" — you're solo.
- Don't claim "strongest", "best", "revolutionary".
- Don't argue with downvotes; the more you defend, the more you sink.
- Don't link out to your own other content (Twitter thread, etc.) — HN sees that as karma farming.
- Don't post twice if the first one flops. One shot.

---

## Backup title (if the first one feels too long for HN's display)

```
Show HN: A Claude Code plugin that catalogues 30 fingerprints of AI-generated design
```

Slightly shorter, same depth-signal. Use if the first one runs over the visible-character cutoff on small viewports.
