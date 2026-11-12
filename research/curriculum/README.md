# Curriculum research: the 742-link UX and UI learning list

Four reports cover every link in a large public curated list of UX and UI learning material. Each report has topic sections of lessons (sources, status against ux-skill, proposal), the checks it proposes, number conflicts with ux-skill text, and a ledger row for every link.

| File | List section | Links | Lessons |
|---|---|---|---|
| raw/part-a.md | UX, UI, tools, visual design | 188 | 98 |
| raw/part-b.md | User research, information architecture, interaction design, prototyping | 158 | 86 |
| raw/part-c.md | Design thinking, designing with AI, advanced techniques | 162 | 102 |
| raw/part-d.md | Emerging tech, UX strategy, portfolio, career | 234 | 77 |

Method: pages were read where they loaded; videos, books and pages that refused automated fetches were summarized from the list's own descriptions and marked so. Paywalls were not bypassed and links to unofficial copies of paid books were not opened.

## Merged set

The four raw reports are merged into one deduplicated set, checked against data/anti-patterns.json, the render and linter rule ids in engine/, PLAN-4.1-inventory.md and research/library/.

| File | What it holds | Count |
|---|---|---|
| ledger.tsv | One row per link: id (K001 to K742), part, list section, title, url, read status, lessons that use it | 742 rows: read 199, summarized-from-list 277, blocked 266; 624 unique urls, 108 withheld mirror links, 10 repeat occurrences |
| lessons.md | Lessons merged by topic across the parts, paraphrased, with status against this branch and engine location | 323 lessons from 363 raw: agrees 108, partial 22, missing-guide 112, missing-check 74, contradicts 7 |
| checks.md | Proposed checks ranked by impact on a working, un-generic page | 85 rows: new 66, tune existing 8, drop as duplicate 11 |
| guidance.md | Missing guidance grouped by target file | 76 items across 34 files, 6 of them new |
| corrections.md | Every place the reports say ux-skill text is wrong, verified on this branch | 14 rows: open 0, already-fixed 14 |

Ledger read status: read covers pages read and tool pages read for what they do; summarized-from-list covers videos, books and tool pages noted from the list's description or metadata; blocked covers pages that refused the fetcher, JavaScript-only pages, dead links and the unofficial mirrors of paid books, which were never opened and whose links stay withheld. Primary sources the reports checked outside the list (standards, research pages) are named in words in corrections.md because the ledger holds only the list's own links.
