# Curriculum research: the 742-link UX and UI learning list

Four reports cover every link in a large public curated list of UX and UI learning material. Each report has topic sections of lessons (sources, status against ux-skill, proposal), the checks it proposes, number conflicts with ux-skill text, and a ledger row for every link.

| File | List section | Links | Lessons |
|---|---|---|---|
| raw/part-a.md | UX, UI, tools, visual design | 188 | 98 |
| raw/part-b.md | User research, information architecture, interaction design, prototyping | 158 | 86 |
| raw/part-c.md | Design thinking, designing with AI, advanced techniques | 162 | 102 |
| raw/part-d.md | Emerging tech, UX strategy, portfolio, career | 234 | 77 |

Method: pages were read where they loaded; videos, books and pages that refused automated fetches were summarized from the list's own descriptions and marked so. Paywalls were not bypassed and links to unofficial copies of paid books were not opened.

## Still to do

The four reports are raw. The planned merge into one deduplicated set (lessons.md, checks.md, guidance.md, corrections.md, ledger.tsv) was not run. PLAN-5.0.md Phases 3, 5 and 6 expect it. Do that merge first, deduplicating against data/anti-patterns.json, PLAN-4.1-inventory.md and research/library/, then apply the corrections a primary source supports.

Corrections the reports already found against current ux-skill text, each to verify before applying:

- references/laws/laws-of-ux.md uses Miller's law to cap navigation at five to seven items; the law's own summary warns against that use. Move the cap under Hick's law and scanning cost.
- commands/ux-research.md sets a quantitative sample floor of 30; NN/g recommends 20, and the margin of error should size it.
- Card sorting at 15 to 25 people fits only a qualitative sort; a quantitative sort needs 30 to 50. Tree testing and pilot sessions are missing.
- data/ux-guidelines.json credits the 60-30-10 rule to Itten (1961); the rule comes from interior decorating.
- The 30 to 50 percent translation expansion understates short strings, which grow to 200 to 300 percent (W3C, citing IBM).
- Color blindness affects 8 percent of men, not 8 percent of people.
- references/foundations/color.md gives the modal scrim as 60 to 80 percent alpha in tokens and 40 to 60 percent in its checklist.
- ai-interfaces.md allows following the bottom of a streaming answer; NN/g says keep the start of a new answer in view.
- case-study-style.md turns screenshots grayscale and bans citing standards, which suits documents but hides the work in a designer's portfolio.
