---
description: Open-ended taste call on a specific surface. Not a structured audit — a designer's opinion. Returns 3 wins, 3 misses, and 1 strategic move. Triggers on "what do you think", "is this good", "critique this", or "honest take". Use when open-ended taste call, the user asks "what do you think", design review without a structured checklist, producing the 3-wins + 3-misses + 1-strategic-move format. Skip when the user explicitly wants a structured audit (use ux-audit instead), the surface is missing context for taste judgment, backend or infrastructure work.
allowed-tools: Read, Write, Edit, Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(mkdir:*), Bash(date:*), Glob, Grep, WebFetch
disable-model-invocation: false
---

# /ux-critique

You are running the `/ux-critique` command from the `ux` plugin. The job is a designer's opinion on a surface. Not a checklist, not a severity score, not a finding-by-finding teardown. Just a tight, opinionated take that names what is working, what is not, and the one strategic move that would change the most.

## When to use

Triggers: "what do you think", "is this good", "critique this", "honest take", "give me your gut", "is the vibe right", "does this feel like us", "should we ship this".

Use when the user wants judgment, not a report. Use early, when the surface is still malleable and a structured audit would over-formalize the conversation. Use late, when the surface is shipped and the question is "did we land it?"

Do not use when the user explicitly asked for an audit (`/ux-audit`), a checklist (`/ux-a11y`, `/ux-polish`), or actionable fixes — critique is opinion, not a fix list.

## Input

One of: a URL, a screenshot, a file path, a code snippet, a Figma link, or a description with enough context to form an opinion. If the input is too thin to have a real take, ask ONCE for more — a screenshot at minimum, or a sentence of context.

## Process

### 1. Read the surface like a designer, not an auditor

Look at the whole thing first. Do not enumerate. Do not start a list. Notice what your eye does — where it lands first, what it skips, what it returns to, what it ignores entirely. The first 30 seconds of looking is the most honest data you will have. Trust it.

If `.ux/last-frame.json` exists, hold the audience and outcome in mind — your judgment is relative to who this is for, not absolute. A surface that is "minimal and elegant" for a luxury brand is "cold and untrusting" for a kids' product.

### 2. Form a judgment — find the three pairs

Identify the **3 things working**:

These are the surface's strengths. Not "the colors are nice" (vague) but "the type-imagery dialogue carries the page — the wide editorial serif against the tight grid of photography is doing real work." Specific. Defensible. Grounded in what you actually see.

Identify the **3 things not working**:

These are the surface's weaknesses. Not "needs polish" (lazy) but "the hero CTA is the same weight as the secondary navigation — the primary action loses the hierarchy fight on first read." Specific. Defensible. Name the mechanism, not just the symptom.

Identify the **1 strategic move**:

The single change that would shift the surface most. Not a fix list — one move. It might be structural ("kill the second hero section and let the primary one breathe"), thematic ("commit to monochrome — the accent colors are diluting the brand mark"), or tonal ("the copy is corporate; this audience needs warmth"). The move should be plausible to execute in a sprint, not a six-month redesign.

### 3. Write the prose

Maximum 500 words. Often 250–350 is the right length. The shape:

```
─── critique ───
Surface:       <URL / path / one-line description>
Audience:      <from framing if available, or "general" if absent>

<2-3 sentences setting the scene — what kind of surface this is, what it is trying to do, your overall first read.>

What's working:
1. <Win 1 — specific, mechanism named.>
2. <Win 2 — specific, mechanism named.>
3. <Win 3 — specific, mechanism named.>

What's not:
1. <Miss 1 — specific, mechanism named.>
2. <Miss 2 — specific, mechanism named.>
3. <Miss 3 — specific, mechanism named.>

The strategic move:
<1-3 sentences naming the single change and why it would shift the surface most.>
```

The wins/misses can be longer than a sentence — full thoughts, not bullet fragments. But the whole critique stays under 500 words. If you hit 500, cut the weakest item from wins or misses to make room.

### 4. Resist temptation

Do NOT:

- Add a severity scale. This is not an audit.
- Add WCAG references. That is `/ux-a11y`.
- Number every issue on the surface. That is `/ux-audit`.
- Hedge ("might be," "could perhaps," "some users may"). Have a take.
- Apologize for the take ("just my opinion, you know your users better"). The whole command is asking for your take.
- Compliment to soften criticism ("I love what you did with X, but"). State what is working as a separate item.

Do:

- Use specific designer language: hierarchy, rhythm, weight, density, voice, affordance, contrast, balance.
- Reference the audience explicitly when judgment depends on it.
- Stand behind the move. If the user pushes back, defend it or revise — do not capitulate.

### 5. Persist state

Write `.ux/last-critique.json`:

```json
{
  "command": "ux-critique",
  "timestamp": "<ISO8601>",
  "surface": "<URL / path / description>",
  "audience": "<from framing or 'general'>",
  "wins": [
    { "summary": "<1-line summary>", "detail": "<the full sentence from prose>" },
    { "summary": "<>", "detail": "<>" },
    { "summary": "<>", "detail": "<>" }
  ],
  "misses": [
    { "summary": "<>", "detail": "<>" },
    { "summary": "<>", "detail": "<>" },
    { "summary": "<>", "detail": "<>" }
  ],
  "strategic_move": {
    "summary": "<1-line summary of the move>",
    "detail": "<the full reasoning from prose>"
  },
  "prose": "<the full prose output verbatim>"
}
```

The `prose` field stores the human-readable critique so downstream commands can quote it. The structured `wins`/`misses`/`strategic_move` fields let `/ux-next` route based on what the critique surfaced.

## Output

The prose critique from step 3, followed by the next-prompt block.

## State persisted

- `.ux/last-critique.json` — keys: `command`, `timestamp`, `surface`, `audience`, `wins` (3 objects of `{summary, detail}`), `misses` (3 objects of `{summary, detail}`), `strategic_move` (object of `{summary, detail}`), `prose`.

## Next prompt

```
─── next ───
Recommended: <command keyed off the critique's tone>
Other moves: /ux-audit       (structured version of this critique)
             /ux-polish      (if the misses are mostly cosmetic)
             /ux-design      (if the strategic move requires a redesign)
             /ux-next        (let me decide)
```

Routing logic for "Recommended":

- If all three misses are cosmetic/polish → `/ux-polish`.
- If the strategic move requires structural change → `/ux-design` (or `/ux-audit` if the user wants the structured version first).
- If the critique mostly named copy issues → `/ux-copy`.
- If the misses cluster on a single dimension (motion, a11y) → the matching narrow command.
- Otherwise → `/ux-audit` for the structured follow-up.

## Hard rules

- Never exceed 500 words. The critique is prose, not a report.
- Never hedge with "might be" or "could perhaps." Have a take.
- Never add a severity scale, WCAG references, or finding numbers. This is not an audit.
- Never list more than 3 wins or 3 misses. If you have 5, cut to the 3 that matter most.
- Never leave the strategic move vague ("improve the hierarchy"). Name the move concretely ("kill the second hero, make the primary CTA twice the weight of nav").
- Never apologize for the opinion. The user asked for it.

## Failure modes

- **Audit creep**: starting as a critique and turning into a 12-item findings list. Stop and cut to 3+3+1.
- **Soft takes**: every win is "the design feels good" and every miss is "could be tighter." Specific or it is not a critique.
- **Hedging language**: "I think maybe perhaps." Cut it. The user wants judgment.
- **Strategic-move ambiguity**: "improve the UX." That is not a move. The move names a concrete change.
- **Word bloat**: 800 words of careful prose. The user asked for an opinion. Trim.
- **Missing audience anchor**: critiquing in a vacuum when the framing is on file. Read `.ux/last-frame.json` before forming the take.

## Error Handling

| Error condition | Recovery |
|---|---|
| Surface input too thin to have a real take | Ask once for more — a screenshot at minimum, or one sentence of context |
| `.ux/last-frame.json` absent | Anchor to "general" audience and state that in the prose |
| User says "your call" with no audience anchor | Reuse `.ux/last-frame.json` if present; otherwise note the absence and form a take against a general audience |
| Critique drifting into a 12-item findings list | Stop and cut to 3+3+1; hand off to `/ux-audit` for the structured version |
| User pushes back on the strategic move | Defend it or revise — never capitulate to a vague "make it nicer" |

For path issues: see references/process/discovery-protocol.md for state file location (.ux/ in project root). Report bugs at https://github.com/Laith0003/ux-skill/issues.

---

## v2 Python integration

Critique is taste-level judgment, but it should be grounded in named principles, not floating opinions. Load the relevant guidelines and anti-patterns from the engine's data layer first.

### Step 1 — Load relevant UX laws + guardrails

```bash
python3 -c "
import json
laws = json.load(open('data/ux-guidelines.json'))['entries']
slop = json.load(open('data/anti-patterns.json'))['entries']
# Surface the named principles the critique should reference
print(f'UX laws available: {len(laws)}')
for cat in sorted(set(l['category'] for l in laws)):
    items = [l for l in laws if l['category'] == cat]
    print(f'  {cat}: {len(items)} principles')
print()
print(f'Anti-pattern rules: {len(slop)}')
for cat in sorted(set(s['category'] for s in slop)):
    print(f'  {cat}: {sum(1 for s in slop if s[\"category\"] == cat)} rules')
"
```

### Step 2 — Run the linter to get the mechanical floor

```bash
python3 -m engine.cli.main --no-pretty lint <target-path> --threshold low > /tmp/ux-lint-report.json 2>/dev/null \
  || true
```

The linter catches the rules-based slop. The critique covers everything ABOVE that floor: taste, hierarchy, density, narrative, brand fit, emotional tone — the things regex cannot judge.

### Step 3 — Critique with named-principle grounding

When the LLM produces the critique, every finding MUST cite either:
- A named UX law from data/ux-guidelines.json (e.g., "Violates Hick's Law — 8 primary actions where 1 is needed")
- A brand exemplar from data/brands/*.json (e.g., "Stripe handles this with a side-by-side code/output split")
- A style philosophy from data/styles.json (e.g., "The 'Monochrome Precise' style would treat this differently — drop the saturation, lean on hierarchy")

NO floating critique. Every point is grounded in cited material.

### Fallback

If `data/*.json` is missing, fall back to v1 prose-only mode using `references/laws/*.md` and `references/foundations/*.md`.
