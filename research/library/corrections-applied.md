# Corrections applied (PLAN-5.0, Phase 3)

One row per gaps.md row marked contradicts, then the Phase 3 platform list and the Phase 3 items that rest on research/curriculum/. Locations are file:line on feat/4.1-stageshow at 82327a20, each checked to still say what the row claims before the edit. Sources are library codes with pages (research/library/ACKNOWLEDGEMENTS.md) or the standard. A proposed new check in a row's action is Phase 5 work (new checks, each measured as it lands) and is listed as parked, not dropped.

## Cluster A: research and process

| id | engine location | before | after | source | status |
|---|---|---|---|---|---|
| A-fix-proposal | commands/ux-research.md:57 | Interview reflection step asks "what would solve this" | Ask what a good day would have looked like or the last time it went badly; when a fix is offered, ask what problem it solves | B26 p.81-85; B89 p.84-85 | fixed |
| A-quant-floor | commands/ux-research.md:133, 156 | Never recommend n<30 for quant; refuse below the floor | Compute n from metric, precision and design; state what the n can detect; about 20 per group only as a labeled default; never refuse | B94 p.27, 133-134 | fixed |
| A-midpoint | references/process/lean-ux-klein.md:139 | Remove the middle position on a five-point scale | Keep the odd scale and its midpoint; fight satisficing with short surveys and attention checks | B03 p.331, 355; B28 p.235-236 | fixed |
| A-workshop-size | references/process/design-thinking-apphaus.md:37 | Size the group to 6 to 12 | Working groups of about 5 to 7, no more than 8; split larger rooms | B93 p.341; B39 p.40 | fixed |
| A-qual-floor | commands/ux-research.md:133, 156 | Never recommend n<5 for qual; refuse below it | 5 or more for a standalone round; 2 to 4 per round in a recurring or RITE series that meets its cumulative goal | B34 p.123-124; B77 p.125-130 | fixed |
| A-think-aloud | commands/ux-research.md:59, 74 | Think-aloud stated for the study while time-on-task is reported | Protocol stated per task; time-on-task only for silent tasks | B28 p.92, 118 | fixed |
| A-survey-n | agents/research-synthesizer.md:146 | Surveys under n=30: directional only | State the margin of error for the actual n (about 18 points at 30, about 5 at 385) | B94 p.36-37 | fixed |
| A-funnel | agents/research-synthesizer.md:148 | Funnel deltas under 5 percent are noise | Test the difference or read its interval, then judge practical size | B94 p.82-83 | fixed |
| A-design-lead | references/process/lean-ux-gothelf.md:194 | Designers do not work a sprint ahead | Design keeps a short lead (days to a sprint); detailed work pairs at story time | B34 p.153; B20 p.662-677 | fixed |
| A-first-read | commands/ux-critique.md:27 | First 30 seconds are the most honest data; trust it | Record the first read as a reaction and test it against the audience goal | B77 p.116-120; B09 p.23-28 | fixed |
| A-report-order | references/process/lean-ux-klein.md:349 | Lead with evidence, not interpretation | Lead with the one-sentence conclusion, then counted observations; observation versus extrapolation kept | B03 p.553; B28 p.307-309 | fixed |
| A-studio-length | references/process/lean-ux-gothelf.md:136 | Design studio usually two to three hours | At least about three hours | B34 p.76-81 | fixed |

## Cluster B: visual, system and platform

| id | engine location | before | after | source | status |
|---|---|---|---|---|---|
| B-chart-hues | references/foundations/color.md:264; references/foundations/accessibility.md:153 (also components.md:332, 535) | Qualitative palettes up to 7 to 8 hues | 6 at most, 4 to 5 for identification, the rest grouped as Other | B46 p.193-194, 746-747 | fixed |
| B-bar-gap | data/chart-types.json:23 | Bar-to-gap ratio of 0.4 or more | Gap at most half the bar width | B46 p.306-307 | fixed |
| B-dark-weight | references/foundations/typography.md:86, 164, 378 | Drop weight about 50 units in dark mode | Body and small text keep 400 or more with +0.01 to +0.02em tracking; only display weights of 600 and up may drop | B88 p.139; B18 p.135-136 | fixed in guidance; generator parked: engine/foundations/typography.py dark_weight still sets body 40 lighter in dark mode under decision record dark-text-sets-lighter. Changing generated tokens needs a superseding record and an owner call on that record |
| B-metadata-300 | references/foundations/typography.md:136 | Light 300 for support and metadata | Metadata at 400, muted by color or size | B47 p.40-41; B31 p.92 | fixed |

## Cluster C: interaction, content, access and AI

| id | engine location | before | after | source | status |
|---|---|---|---|---|---|
| C-button-link | references/foundations/components.md:54 | Button for every clickable action, navigate included | Buttons act, links navigate; a primary link may look like a button and stays a link | HTML spec; B26 p.622-623; B80 p.42-45 | fixed |
| C-menu-length | references/laws/laws-of-ux.md:97 | Menus over seven items are choice overload | Group long menus; drop-downs near 8, cascades at 2 levels | B02 p.141-142; B46 p.402-408 | fixed |
| C-select-radio | references/foundations/components.md:374-375 | Select for any single choice from a known set | Control-choice table: radios up to about 7 when space allows, select when short, combobox for long lists | B46 p.497-500; B14 p.47-48 | fixed |
| C-duration | references/foundations/motion.md:89, 290 | Hero reveal 800ms or longer; only past 1500ms banned | One-shot motion capped at 1000ms; counters and brand marks 600 to 1000ms (also exemplars.md, landing.md) | B42 p.73-76; B26 p.297 | fixed |
| C-carousel | references/foundations/motion.md:288 | Bans only slides under 4 s | No auto-advance by default; a rotating carousel needs a pause control (also anti-slop.md, exemplars.md) | WCAG 2.2 SC 2.2.2 | fixed |
| C-error-summary | references/foundations/accessibility.md:63-71; references/foundations/components.md:19 | Inline-only errors are an anti-pattern; every multi-error form needs a summary | Inline message mandatory; summary only on long or multi-section forms | B18 p.92-93; B86 p.525-526 | fixed |
| C-toast | references/foundations/accessibility.md:170; references/foundations/copy.md:188 (also components.md, copy-writer.md, library.md, heroui.md) | Auto-dismiss toasts, errors included, in 3 to 5 s | Errors and action toasts persist; success may fade and pauses on hover and focus | WCAG 2.2 SC 2.2.1 | fixed; check error-toast-auto-dismiss parked for Phase 5 |
| C-required | agents/copy-writer.md:127-129 | Required indicators are visual only (dot, asterisk, pill) | Required in text and code: "(optional)" or an explained asterisk plus the required attribute | WCAG 2.2 SC 3.3.2, 1.3.1; B86 p.494-495 | fixed; check required-indicator-mismatch parked for Phase 5 |
| C-drag | references/foundations/accessibility.md:223 | aria-grabbed and aria-dropeffect during drag | Live-region announcements and move buttons; the two attributes are deprecated | WAI-ARIA 1.1; WCAG 2.2 SC 2.5.7 | fixed; check drag-without-pointer-alternative parked for Phase 5 |
| C-miller | references/laws/laws-of-ux.md:709-727 (also data/ux-guidelines.json millers-law) | Cap visible items 5 to 9, nav 5 to 7, autocomplete 7 | Recall limit of 3 to 5 chunks for held information; visible menus grouped (4 to 8 ungrouped, about 24 grouped) | B93 p.141; B46 p.107, 347-349; B79 p.102-103 | fixed; check menu-ungrouped-count parked for Phase 5 |
| C-hick | references/laws/laws-of-ux.md:415 | Cap visible choices under seven, ideally five | Order (natural, frequency, alphabetical), group, trim unused; no fixed cap | B46 p.347-352; B93 p.141-143 | fixed |
| C-hamburger | references/laws/laws-of-ux.md:458; references/foundations/components.md:227, 247, 516 | Hamburger is the winning mobile convention and default under 768px | 3 to 5 primary destinations visible; secondary items behind a labeled Menu | B02 p.534-535; B07 p.198-201 | fixed; check nav-primary-hidden-mobile parked for Phase 5 |
| C-mega-menu | references/foundations/components.md:229 | Organize by job-to-be-done, not alphabetical | Task groups for exploring, alphabetical within groups or as an A to Z index | B93 p.127-131; B46 p.350-352 | fixed |
| C-expansion | references/foundations/accessibility.md:234; agents/copy-writer.md:186 | Flat 30 to 50 percent (30 percent) longer | Length table: up to 10 chars 100 to 200 percent down to about 30 percent for long text; pseudo-localization | B46 p.657-662; B23 p.603-604 | fixed; check i18n-expansion-overflow parked for Phase 5 |
| C-mental-model | references/laws/krug.md:191 | Users are not building a mental model | Users do not study the system but still build a model; show state and cause | B02 p.151-152; B20 p.335-339; B79 p.42-46 | fixed |

## Platform (PLAN-5.0 Phase 3; research/5.0/landscape.md A3)

| id | engine location | before | after | source | status |
|---|---|---|---|---|---|
| P-100vh | data/anti-patterns.json h-screen-no-dvh-fallback; references/foundations/anti-patterns.md sections 13 and 15 | Keep 100vh as the fallback for browsers without dvh; only dvh accepted | svh for heroes, dvh where resizing is wanted; svh, lvh and dvh all pass; no fallback advice | Baseline viewport-unit-variants, widely available 2025-06-05 | fixed; the id is kept (rule ids are a public surface; the suggested rename full-height-uses-vh is parked for the Phase 12 id review) |
| P-glass | data/anti-patterns.json glass-without-fallback; data/landing-patterns.json:338 | backdrop-filter unsupported on Firefox and older Safari | Judged on legibility: high-alpha background so text contrast holds; prefers-reduced-transparency optional | Baseline backdrop-filter, newly available 2024-09-16 | fixed |
| P-avif | data/anti-patterns.json image-format-jpg-no-webp-avif | picture with AVIF universal since 2023 | AVIF Baseline 2024-01-25, widely 2026-07-25; a bare img pointing at .avif or .webp passes | Baseline avif | fixed |
| P-starting-style | data/anti-patterns.json exit-cut-by-display-none; commands/ux-lint.md | Fix names allow-discrete only | Fix names transition-behavior: allow-discrete, overlay and @starting-style; both allow-discrete forms pass. @starting-style alone does not keep an exit running, so it is not a pass | Baseline starting-style and transition-behavior, newly 2024-08-06 | fixed |
| P-interpolate-size | data/anti-patterns.json animating-layout-properties; engine/linter/taste.py | Grid-rows trick only | A height or block-size disclosure passes through ::details-content, interpolate-size: allow-keywords, or a disclosure selector on a page using root interpolate-size or a calc-size() open state; decision record layout-transitions-through-the-platform | Baseline details-content, newly 2025-09-16; interpolate-size Chromium only, instant open as fallback | fixed |
| P-top-layer | data/anti-patterns.json arbitrary-z-index-9999; references/foundations/spacing.md:80 | z-scale token map only | Overlays go to the top layer (popover, dialog with showModal) first, the token scale for the rest | HTML popover and dialog | fixed |
| P-justify | data/anti-patterns.json text-align-justify-web | CSS has none of the hyphenation a print justifier relies on | Rivers remain at web measures; if required, hyphens: auto with a correct lang is dependable | Baseline hyphens, widely 2026-03-18 | fixed |

## Phase 3 items that rest on research/curriculum/

research/curriculum/ named in PLAN-5.0 does not exist in this checkout, so nothing below can be traced to a source there.

| id | engine location | before | after | source | status |
|---|---|---|---|---|---|
| K-card-sort | commands/ux-research.md:49 and the method table | Card sort n=15-25 | unchanged | curriculum only | parked: curriculum absent; the library row is partial (conflicts.md A6), not contradicts |
| K-60-30-10 | data/ux-guidelines.json 60-30-10-rule source field | Credited to a color-theory tradition | unchanged | curriculum only | parked: curriculum absent; no library lesson covers the credit |
| K-color-blindness | data/ux-guidelines.json:603; references/foundations/accessibility.md:149 | About 8 percent of men | unchanged | B46 p.726-727 | agrees already; no change needed |
| K-scrim-alpha | references/foundations/color.md | Scrim alpha | unchanged | curriculum only | parked: curriculum absent |
| K-streaming-scroll | references/foundations/ai-interfaces.md | Streaming scroll rule | unchanged | curriculum only | parked: curriculum absent |
| K-case-study | portfolio case-study grayscale and section order | unchanged | unchanged | curriculum only | parked: curriculum absent |
