# Brand-anchored redesign — the process every reference build must follow

When ux-skill redesigns or extends an EXISTING site (a reference URL/screenshot is
supplied), it must honor that site's identity and serve the page's goal. The engine
must NOT impose its own house style. The output should look like the *client* leveled
up — never like a ux-skill or Claude template.

This file is canonical. `/ux-design`, `/ux-discover`, the frontend-engineer agent,
and the linter/rating all read these rules. They are enforced, not advisory.

The travelling `brand.md` is a portable markdown file — YAML frontmatter plus
Strategy / Voice / Visual sections (a shape compatible with the common `brand.md`
convention; cf. thebrandmd/brand.md) — carrying our one-line brand-fidelity-gate
anchor on top. It works as input too: a project's existing `brand.md` is consumed
as the authoritative anchor (`uxskill brand --from-brand-md ./brand.md`, parsed by
`engine.brand.parse_brand_md`) instead of re-extracting. Auto-extraction + the
brand-fidelity hard floor are unchanged.

## The 9 rules

1. **Always auto-extract the brand** when a reference exists, with no confirm step
   unless told otherwise. The result is a travelling `brand.md` (+ `brand.json`).
2. **The brand.md travels** to every step (discover -> synthesize -> generate) as a
   hard anchor, and is **scored by the linter/rating**. Output that drifts off-brand
   fails — see rule 7.
3. **Color comes from the LOGO, not the CSS.** A site's most-painted CSS color is
   usually theme chrome (e.g. a green section background), not the brand. Sample the
   logo's pixels; its dominant non-neutral color is the primary. (InstantSkipHire:
   logo is amber `#f0890f`; the CSS green `#1c3829` is secondary.)
4. **Type comes from the LOGO's letterform style, and default fonts are rejected.**
   A site font that is a known default (Roboto/Roboto Flex, Inter, Arial, Helvetica,
   system-ui, Open Sans, Lato, Segoe UI, Source Sans) is the *absence* of a type
   choice — do not preserve it. Read the logo's wordmark style (a vision pass) and
   pick a deliberate pairing that matches it. Only preserve a site font when it is
   genuinely distinctive.
5. **Preserve human copy by default.** Do not rewrite existing headlines/body that
   are already human and good. Restructure walls of text into scannable blocks, keep
   the words. Rewrite only when asked.
6. **Layout follows the page goal.** For lead-gen, the quote/contact form belongs in
   the hero (text left, form or brand imagery right) — not buried at the bottom.
7. **Brand fidelity is scored AND gated.** A `brand_fidelity` dimension checks: uses
   the brand primary color, carries the logo, type matches the brand, no house-style
   drift. It is a hard floor: if a brand.md exists and the output ignores the primary
   or drops the logo, it FAILS regardless of other scores. Overridable per run.
8. **Imagery is mandatory and real.** Source the client's own assets first; fill with
   curated Unsplash/Pexels chosen to match the 7-axis temperature and brand; pick the
   best per slot. Ban only *random/generic* stock and AI-slop clutter — not all
   photography. Abstract SVG is not a substitute for a real product/site image.
9. **Richness via a page-level section sequence.** Pick a whole-page pattern by goal
   and expand the FULL sequence with completeness and a per-item icon. For lead-gen:
   Hero (+form) -> Proof/stats bar -> value cards -> category pills -> item cards ->
   split feature rows -> coverage -> social proof / pull-quote -> CTA band -> rich
   footer. Map ALL source content into it (every sector -> pill, every size -> card,
   every benefit -> checklist). Add the conversion mechanisms the goal needs (hero
   form, proof bar, trust signals, phone) even if the original lacked them.

## Why (what the dogfood proved)

A first dogfood on instantskiphire.com/commercial-skip-hire/ failed every rule: it
shipped clay `#cc785c` (Claude's color) + monochrome + an editorial serif for a brand
whose real identity is amber + green + a friendly rounded logo; it rewrote a good
human headline; it dropped the form out of the hero; it used an abstract SVG instead
of real images; and it came out sparse. A competitor (ui-ux-pro-max) produced a richer
page by following a page-level section sequence + per-item icons + conversion
mechanisms — but also got the brand wrong (navy, not amber) and ships no reviewer.
ux-skill's win is to combine richness with brand-accuracy AND deterministic
enforcement.

## How the pieces fit (the LIVE pipeline)

Wired end-to-end, not aspirational. The flow when a reference brand exists:

1. **Capture** (I/O / vision -- the caller, NOT the engine, which is offline): read the
   live DOM, SAMPLE THE LOGO PIXELS for the dominant non-neutral color, read the logo's
   letterform style. Write `.ux/brand-signals.json`.
2. **Normalize + anchor:** `uxskill brand --signals-file .ux/brand-signals.json --out .ux`
   -> `engine/brand/build_profile` -> writes `.ux/brand.json` (the travelling
   `BrandProfile`) + `.ux/brand.md` (human-readable). CONFIRM the read before locking.
3. **Recommend:** `uxskill recommend --brand-file .ux/brand.json` -> `Brief.brand` ->
   `anchor_recommendation` overrides the palette primary/accent with the brand color and
   attaches `brand` + `type_directive`.
4. **Synthesize:** `--brand-file` -> `synthesize()` `_stamp_client_brand` overlays the
   client primary/type on the synthesized system (composes with the reference_brands
   exemplar modes; does not replace them).
5. **Generate:** `/ux-design` pastes `brand.md` into the frontend-engineer prompt as a
   HARD ANCHOR; the agent uses the logo + brand color + logo-style type, PRESERVES the
   client's human copy verbatim, and expands the page sequence with real imagery.
6. **Gate:** `evaluate(..., brand_profile=...)` reports `brand_fidelity` + `imagery` and
   applies a HARD FLOOR (`brand_passed`) -- off-brand drift fails regardless of the
   7-axis composite. `uxskill evolve --brand-file` honors the floor at every exit
   (exit 1 = gate_failed). The linter's `imagery-mandatory` rule is the live text-wall
   backstop.

Integration points (for maintainers): `engine/evaluator/core.py` (floor),
`engine/evolve/core.py` (loop gate), `engine/recommender/core.py` (anchor),
`engine/synthesizer/core.py` (`_stamp_client_brand`), `engine/cli/main.py`
(`brand` subcommand + `--brand-file`), `commands/ux-design.md` (Steps 1.5/2/4/5),
`agents/frontend-engineer.md` + `agents/copy-writer.md` (consume + copy-preserve).
Tests: `tests/test_brand.py`, `tests/test_brand_wiring.py`, `tests/test_cli_brand.py`.

## Standing rule for maintainers

When the user gives notes for this skill: challenge assumptions, verify against the
REAL artifact (look at the logo, sample the pixels, read the page) rather than
theorize, then fold the resulting principle into this file + the engine + the agents
so the skill applies it on every future run. Notes become permanent skill intelligence,
never one-off chat fixes.
