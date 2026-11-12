# 4.1 research inventory

The principles behind the 4.1 checks, gathered from the WCAG 2.2 text, platform guides, usability research, the classic design books and two curated UI and UX reading lists, de-duplicated and set against what ux-skill already does. Each row is one checkable principle in our own words, its source, and where it lands. PLAN-4.1.md ranks what to build from it. Delete this file with PLAN-4.1.md in the release commit.

Status key:
- BUILT: shipped on feat/4.1-stageshow as the rule named
- COVERED: already in ux-skill (rule id or file named)
- PARTIAL: guidance exists, no machine check (counted as covered for guidance, listed again in MISSING-B when a check is worth building)
- B-LINT / B-RENDER / B-PROBE: missing and machine-checkable (static lint rule, headless render measurement, complaints probe)
- C: missing, guidance only (target reference file)

Counting rule: an item is "covered" when ux-skill already encodes it as a check, or as guidance where no check is reasonable. An item with guidance but no feasible check it should have is counted as missing (B), and the guidance file is named.

Sources (short names): WCAG22 = W3C WCAG 2.2 Recommendation (normative text fetched); HIG = Apple HIG JSON (accessibility, buttons, layout, typography pages, fetched); M3 = Material/Android touch target docs; NNG = Nielsen Norman Group; LoUX = lawsofux.com (30 laws, fetched); Baymard = baymard.com checkout and input-field guidelines (fetched); RUI = Refactoring UI (Wathan, Schoger); DMMT = Krug, Don't Make Me Think; DOET = Norman; AF = Cooper, About Face; UPD = Lidwell et al, Universal Principles of Design; Tufte = Visual Display of Quantitative Information; Few = Information Dashboard Design (13 pitfalls); TOGI = togiberlin/ui-ux-designer-roadmap (symmetry table, nudges); HEND = hendurhance/ui-ux (curated list, incl. AI design section); DD = deceptive.design (Brignull); SLOP = 2025 and 2026 writing on why AI-built interfaces look generic.

## A. Accessibility (WCAG 2.2 and platform guides)

| # | Principle (checkable form) | Source | Status | Where / proposal |
|---|---|---|---|---|
| A1 | All text meets 4.5:1 (3:1 at 24px, or 18.66px bold) against its rendered background | WCAG22 1.4.3 | BUILT `text-low-contrast` | today: static `dark-text-on-dark-card`, `text-ink-at-low-alpha`; render only `accent-text-low-contrast`. Generalise to every visible text node |
| A2 | Input borders, checkbox/radio outlines, icons that carry meaning reach 3:1 vs adjacent color | WCAG22 1.4.11 | B-RENDER | guidance in foundations/accessibility.md (Contrast minimums); no check |
| A3 | Focus has a visible indicator | WCAG22 2.4.7 | COVERED | render `focus-ring-missing`, `focus-ring-clipped`; lint `outline-none-no-focus-visible` |
| A4 | Focus indicator area at least a 2px perimeter and 3:1 change | WCAG22 2.4.13 (AAA) | B-RENDER | extend `focus-ring-missing` to measure contrast and area (low priority, AAA) |
| A5 | A focused control is not entirely hidden by author content (sticky header, cookie bar, chat bubble) | WCAG22 2.4.11 | B-RENDER | add to interact.py tab pass: elementFromPoint over the focused box |
| A6 | Pointer targets at least 24x24 CSS px, or 24px-circle spacing exception; inline links exempt | WCAG22 2.5.8 | BUILT `target-too-small` | none today; accessibility.md says 44px web min (that is AAA 2.5.5) |
| A7 | Primary touch targets 44x44 (Apple 44pt, min 28pt; Material 48dp with 8dp gap; WCAG AAA 44px) | HIG accessibility/buttons, M3, WCAG22 2.5.5 | PARTIAL | guidance accessibility.md + interaction.md; same measurement as A6 at a 390px width, advisory tier |
| A8 | No two-dimensional scrolling at 320 CSS px width | WCAG22 1.4.10 | B-RENDER | `horizontal-overflow` runs at 390/430/768/1280 only; add a 320x640 viewport |
| A9 | No clipping or overlap when line-height 1.5, paragraph 2em, letter 0.12em, word 0.16em are forced | WCAG22 1.4.12 | B-RENDER | inject the WCAG text-spacing CSS, re-run `text-overflows-its-box` and a clip check |
| A10 | Text resizes to 200% without loss | WCAG22 1.4.4 | B-RENDER | low: root font-size 200% pass, overflow/clip re-check |
| A11 | Hover/focus popups are dismissible (Esc), hoverable and persistent | WCAG22 1.4.13 | B-RENDER | interact.py: hover each [title-less] tooltip trigger, press Esc, move into popup |
| A12 | Moving, blinking, auto-updating content over 5s can be paused | WCAG22 2.2.2 | COVERED | render `moving-content-without-pause`; lint `illustration-loop-without-pause`, `marquee-more-than-one` |
| A13 | Nothing flashes more than 3 times per second | WCAG22 2.3.1 | B-RENDER | low: sample frames of animated regions |
| A14 | Visible label text is contained in the accessible name | WCAG22 2.5.3 | B-LINT | button/link with visible text and an aria-label that does not contain it |
| A15 | Dragging has a single-pointer alternative | WCAG22 2.5.7 | COVERED | accessibility.md "Drag-and-drop alternative" |
| A16 | Help mechanisms in the same relative order across pages | WCAG22 3.2.6 | COVERED | accessibility.md WCAG baseline (multi-page, not checkable per page) |
| A17 | Previously entered data is auto-populated or selectable | WCAG22 3.3.7 | COVERED | accessibility.md baseline (flow-level) |
| A18 | No cognitive test for login: paste allowed, password managers not blocked | WCAG22 3.3.8 | B-LINT | onpaste return false / preventDefault on inputs; autocomplete="off" on password or one-time-code fields |
| A19 | Inputs collecting user data expose their purpose (autocomplete tokens) | WCAG22 1.3.5 | B-LINT | email/tel/name/address/postal/cc inputs without a valid autocomplete token |
| A20 | Detected errors identified and described in text, tied to the field | WCAG22 3.3.1 | B-LINT | aria-invalid="true" without aria-describedby or aria-errormessage; guidance covered in accessibility.md patterns |
| A21 | Labels or instructions for every input | WCAG22 3.3.2 | COVERED | `placeholder-as-label`, `select-without-label`, `input-has-no-name` |
| A22 | Status messages announced without focus | WCAG22 4.1.3 | COVERED | `aria-live-polite-on-error`, `aria-busy-without-aria-live` |
| A23 | Page has a descriptive title (not empty, not "Vite + React", "React App", "Create Next App", "Document") | WCAG22 2.4.2, SLOP | BUILT `title-is-a-framework-default` | none today; seo.md has guidance |
| A24 | Page language set | WCAG22 3.1.1 | COVERED | `lang-attribute-missing` |
| A25 | Heading levels in order | WCAG22 1.3.1, 2.4.6 | COVERED | `heading-skip-h1-h3` |
| A26 | Link purpose from link text | WCAG22 2.4.4 | COVERED | `generic-cta-text`, `cta-text-read-more`, `cta-text-tap-continue-go` |
| A27 | Links in running text distinguishable by more than color (underline, or 3:1 vs body text plus a non-color cue) | WCAG22 1.4.1 (technique G183), NNG visible links | B-RENDER | inline a inside p/li: no underline and link/body contrast under 3:1 |
| A28 | Data tables mark header cells (th, scope) and have a caption or name | WCAG22 1.3.1 (H51, H63) | B-LINT | table with td rows and no th; dashboards especially |
| A29 | Captions on video; no unmuted autoplay | WCAG22 1.2.2, 1.4.2 | COVERED | `video-without-captions`, `autoplay-without-muted` |
| A30 | Skip link / bypass blocks | WCAG22 2.4.1 | COVERED | accessibility.md Skip link; `screen-reader-only-without-class` |
| A31 | Reduced motion respected | WCAG22 2.3.3, HIG | COVERED | `infinite-animation-without-reduced-motion`, render `infinite-animation-under-reduced-motion`, `press-moves-under-reduced-motion` |
| A32 | Pinch zoom not blocked | WCAG22 1.4.4 | COVERED | `viewport-no-zoom` |
| A33 | No positive tabindex; focus order follows reading order | WCAG22 2.4.3 | COVERED | `tabindex-positive` |
| A34 | Focus returns after closing a dialog; Esc closes | WCAG22 2.4.3, NNG | COVERED | render `focus-lost-after-escape` |
| A35 | Focus stays inside an open modal dialog | ARIA APG dialog pattern | B-RENDER | low: open dialog, Tab N times, assert activeElement inside |
| A36 | Interactive elements hidden from AT are not focusable | WCAG22 4.1.2 | COVERED | `aria-hidden-on-interactive`, `focusable-inside-aria-hidden`, `focusable-at-opacity-zero` |
| A37 | Works in forced-colors / high-contrast mode (focus, icons, borders survive) | WCAG22 1.4.11 in practice, Windows HCM | B-RENDER | low: emulateMedia forcedColors active, re-run focus-ring check |
| A38 | Color is never the only signal | WCAG22 1.4.1 | COVERED | color.md, dashboard.md ("a state always shows its word") |
| A39 | Dynamic Type / text scaling on native | HIG | COVERED | accessibility.md Dynamic Type |

## B. Forms and checkout

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| B1 | Persistent labels above fields | Baymard, NNG | COVERED | components.md Form Field, `placeholder-as-label` |
| B2 | Mark both required and optional fields explicitly (only 14% of sites do; marking only optional caused 32% to skip required) | Baymard | B-LINT | form with required inputs where no label carries "*" or "required" and no optional field says "optional"; guidance gap in component-behaviors.md Form |
| B3 | Error messages name the problem and the fix; never "Invalid input" or "Error" (98% of sites fail) | Baymard, NNG heuristic 9 | B-LINT | text channel: invalid input, invalid value, an error occurred, something went wrong, field is invalid; copy.md covers the guidance |
| B4 | Validate on blur, not per keystroke; remove error as soon as fixed | Baymard, NNG | COVERED | components.md principle 7 |
| B5 | Correct keyboard: type=email, type=tel, inputmode=numeric for ZIP, card, OTP | Baymard checkout | B-LINT | name/id/label/autocomplete says email or phone or zip or card but type=text and no inputmode |
| B6 | Autocapitalize and autocorrect off for email, names, addresses | Baymard #1103 | B-LINT | email inputs without type=email or autocapitalize=off; fold into B5 |
| B7 | Accept lenient formats; mask instead of rejecting (89% type numbers their own way) | Baymard #658/#659, LoUX Postel | PARTIAL | `phone-field-requires-country-code`; extend to strict pattern= on phone/card/zip (low) |
| B8 | Field width hints expected length (ZIP, CVC, year not full width) | Baymard, NNG, RUI | B-RENDER | inputs with maxlength<=6 or autocomplete postal-code/cc-csc/cc-exp rendered wider than ~20ch at 1280 |
| B9 | Single-column form layout | Baymard, CXL | COVERED | surfaces/component.md Single-column form |
| B10 | 10 to 15+ visible fields intimidate; collapse, hide optional, or step | Baymard #668 (avg checkout 11.3 fields; 19.9 elements) | B-LINT | count visible inputs in one form > 12 with no fieldset/step structure (low) |
| B11 | Do not disable the submit button at rest; validate on submit and explain | NNG, Adam Silver, GOV.UK | B-LINT | button[type=submit][disabled] in static markup |
| B12 | No reset/clear-form button | NNG | B-LINT | input/button type=reset |
| B13 | Never clear entered data after an error | Baymard | C | foundations/component-behaviors.md (Form) |
| B14 | Guest checkout first and as prominent as sign-in; defer account creation (19% abandon on forced accounts) | Baymard | C | new surfaces/checkout.md, or component-behaviors.md |
| B15 | Total cost (shipping, tax, fees) shown before the final step; no new fees on review (39% abandon on unexpected costs) | Baymard | C | surfaces/landing.md Pricing + checkout guidance |
| B16 | Progress indicator matches real steps; past steps clickable; back button keeps data | Baymard | C | component-behaviors.md (Form) |
| B17 | "Security code" label with card-location hint, Luhn validation, card auto-format | Baymard #582/#584 | C | component-behaviors.md (Form, payment) |
| B18 | Address Line 2 and coupon fields behind a link; single Full Name field | Baymard | C | component-behaviors.md (Form) |
| B19 | Specific step CTAs ("Continue to Payment", "Place order") | Baymard, NNG | COVERED | `cta-text-tap-continue-go`, `generic-cta-text`, copy.md CTA verb library |
| B20 | Prefilled values shown in editable fields, not static text | Baymard #572 | C | component-behaviors.md |
| B21 | Allow paste and password managers; autocomplete=one-time-code on OTP | WCAG22 3.3.8, NCSC, NIST 800-63B | B-LINT | merged into A18 |

## C. Dark patterns and honesty

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| C1 | No pre-checked consent, marketing or add-on checkbox | DD (sneaking, preselection), TOGI "defaulting", GDPR (CJEU Planet49) | BUILT `consent-prechecked` | input[type=checkbox][checked] whose label mentions newsletter, offers, marketing, partners, subscribe, insurance, protection; guidance exists in laws/laws-of-ux.md (Cognitive Bias) |
| C2 | No confirmshaming decline copy | DD | BUILT `confirmshaming` | text channel: "No thanks, I", "I don't want", "I prefer to pay full price", "I'll stay" on a button/link |
| C3 | No fake urgency or scarcity (hardcoded countdowns, "only 3 left", "12 people viewing") | DD, FTC 2022 dark patterns report, TOGI loss aversion | BUILT `fake-urgency` | text regex for "only \d+ left", "\d+ people (are )?viewing", "offer ends in" with a hardcoded timer in markup |
| C4 | Decoy pricing tier used to steer | TOGI phantom pricing, DD | C | surfaces/landing.md Pricing (name it as a pattern to avoid) |
| C5 | Cancel as easy as sign-up (roach motel) | DD, FTC click-to-cancel | C | foundations/copy.md or process guidance (flow-level) |
| C6 | Real social proof only | DD, SLOP | COVERED | `testimonial-fake-five-stars`, `trust-badge-no-source`, `logo-cloud-no-real-logos`, `round-number-stats` |
| C7 | Nudge ethics: defaults serve the user | TOGI, Thaler/Sunstein, Nodder | COVERED | laws/laws-of-ux.md Cognitive Bias |

## D. Typography and reading

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| D1 | Body measure about 45 to 75 characters; never above 80 | Baymard (50 to 75), WCAG22 1.4.8 AAA (80, 40 CJK), Bringhurst (45 to 75) | B-RENDER | guidance typography.md (house defaults 42 to 70); measure chars per rendered line of p/li |
| D2 | Body line-height at least about 1.4 to 1.5 | WCAG22 1.4.8 AAA (1.5), RUI | B-RENDER | guidance typography.md; only display floor is linted (`display-line-height-under-floor`) |
| D3 | Inputs at least 16px so iOS Safari does not zoom on focus; mobile body 16px | WebKit behavior, typography.md | BUILT `input-text-zooms` | guidance typography.md Mobile floors; computed font-size of input/select/textarea at 390px |
| D4 | No text below about 12px (Apple minimum 11pt; default 17pt) | HIG typography | B-RENDER | smallest visible text at 390px |
| D5 | Few distinct font sizes per page (a scale, about 4 to 7 roles) | RUI, TOGI symmetry table (4 sizes vs 7) | B-RENDER | static `size-outside-system` only fires against a declared system; count distinct computed sizes on the rendered page |
| D6 | Few text colors (1 ink in 2 to 3 opacities) | TOGI, RUI | B-RENDER | count distinct computed text colors; `color-over-budget` counts chromatic fill only |
| D7 | Three weights or fewer | RUI, typography.md | COVERED | `weight-outside-system` |
| D8 | No justified text on the web | WCAG22 1.4.8 | COVERED | `text-align-justify-web` |
| D9 | No all caps for running text | typography canon | COVERED | `all-caps-large`, `capitals-outside-system` |
| D10 | No one-word last line in headings (balance) | typographic canon, RUI | B-RENDER | guidance typography.md; count words on last line box of h1-h3 |
| D11 | Tabular numerals in tables, stats, tickers | Few, dashboard.md | B-RENDER | guidance dashboard.md principle 3; computed font-variant-numeric on digit-heavy td/stat text |
| D12 | Numeric columns right-aligned, text left | Few, M3 data tables | B-RENDER | guidance components.md Table; computed text-align on digit-heavy td/th |
| D13 | Hierarchy through weight and color, not size alone; de-emphasise secondary | RUI | COVERED | typography.md three-weight hierarchy |
| D14 | Grey text on colored backgrounds looks dirty; tint toward the background hue | RUI | B-RENDER | low: neutral (chroma < x) text on a chromatic ground |
| D15 | Never pure #000 body, never stark #FFF chassis | RUI, color.md | COVERED | color.md principle 6 |
| D16 | Display tracking and leading floors | typography canon | COVERED | `letterspacing-tracking-tight-display`, `display-line-height-under-floor` |

## E. Layout and visual polish

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| E1 | No sideways page scroll | responsive canon | COVERED | render `horizontal-overflow`, lint `full-viewport-width-overflow` |
| E2 | Text never runs past its box | canon | COVERED | render `text-overflows-its-box` |
| E3 | Edges align: no near-miss left edges (1 to 6px apart) within a column | RUI, CRAP alignment, TOGI symmetry, UPD Alignment | B-RENDER | cluster left x of text/media boxes per section; flag pairs 1 to 6px apart |
| E4 | Spacing comes from a scale (4/8 grid) | RUI, M3 8dp grid, spacing.md | B-RENDER | guidance spacing.md; measure sibling gaps and paddings, flag share off the page's own scale |
| E5 | A heading sits closer to what it introduces than to what came before (space above > below) | LoUX Proximity, RUI | B-RENDER | for each h2-h4: gap to previous block vs gap to next block |
| E6 | A label sits closer to its own input than to the previous field | LoUX Proximity, Baymard | B-RENDER | fold into E5 |
| E7 | Sibling controls and icons share size (one button height per row, one icon size per group) | TOGI symmetry table, LoUX Similarity | B-RENDER | buttons in one flex row with differing heights; svg icons in one list with differing sizes |
| E8 | The h1 (or page title) is the most prominent text on the first screen | RUI hierarchy, DMMT billboard | B-RENDER | largest rendered text in first viewport is not h1/heading |
| E9 | One primary action per group; others visibly secondary or tertiary | RUI button hierarchy, LoUX Hick, Von Restorff | B-RENDER | button group with two or more filled buttons of equal weight; static `cta-buttons-clustered-in-hero` only counts 3+ in hero |
| E10 | Few distinct corner radii | RUI systems | B-RENDER | low: count distinct computed radii; static `border-radius-2xl-default`, `pill-rounded-full-everywhere` partial |
| E11 | Shadows express elevation; not everything floats | RUI, M3 elevation | COVERED | color.md tinted shadows; `box-shadow-multilayer-default`, `glow-shadow-zero-offset`, `hairline-border-heavy-shadow` |
| E12 | Popups/cookie bars do not cover the first screen | NNG popups | COVERED | render `first-screen-covered` |
| E13 | Sticky header stays within a mobile height budget | landing.md, NNG sticky headers | B-RENDER | guidance landing.md "Sticky-header budget on mobile"; sum fixed/sticky heights at 390x844 |
| E14 | In-page anchor targets are not hidden under a sticky header (scroll-margin) | NNG, CSS scroll-margin | B-RENDER | navigate to each #hash target, compare heading top with sticky bottom |
| E15 | Images keep their aspect ratio (no stretch) | canon | B-RENDER | natural ratio vs box ratio off by >3% with object-fit fill |
| E16 | Images are not upscaled past their pixels (blur) | canon | B-RENDER | naturalWidth < rendered width x DPR x 0.9 |
| E17 | No broken images or failed resources | canon | BUILT `image-broken` | img.complete && naturalWidth===0; requestfailed / 404 responses during load |
| E18 | Reserve image space (no layout shift) | Core Web Vitals CLS 0.1 | COVERED/B-RENDER | `img-no-dimensions` covered; a measured CLS via PerformanceObserver is missing (low) |
| E19 | Centered text sits in a centered box | canon | COVERED | render `centered-text-off-center` |
| E20 | Distinct layouts per section; no three equal cards | SLOP | COVERED | `three-equal-card-grid`, `layout-family-repeated`, `split-sections-in-a-row` |
| E21 | Colored side-stripe card (thick left border on a rounded card) is an AI tell | SLOP (superdesign, noqta) | B-LINT | border-left/border-inline-start >= 3px in an accent color on an element with border-radius, or Tailwind border-l-4 + rounded |
| E22 | Cliche icons (sparkles, rocket, lightbulb, zap, shield) and mixed icon families | SLOP, anti-slop.md | B-LINT | guidance anti-slop.md; imports of Sparkles/Rocket/Lightbulb/Zap from lucide-react in feature grids; imports from two icon packages |
| E23 | Numbered 1-2-3 "how it works" step row as default | SLOP | C | styles/anti-slop.md (composition fingerprint) |
| E24 | Purple gradient, Inter-only, centered hero, glass, rounded everything | SLOP | COVERED | `purple-to-blue-gradient`, `default-font-only`, `centered-everything-hero`, `glass-morphism-default`, `border-radius-2xl-default` |
| E25 | Pseudo-localized strings still fit, padded by length band (short strings up to 200 to 300%, long text about 30%; see accessibility.md) | i18n canon (HEND i18n section), accessibility.md text expansion | B-RENDER | guidance accessibility.md; pad text nodes by length band, re-run overflow checks |
| E26 | Dashboard fits one screen for its overview | Few pitfall 1 | C | surfaces/dashboard.md (optionally measure page height at 1280x800) |

## F. Interaction, feedback, navigation

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| F1 | Feedback within 100ms; flow kept under 1s; progress for >1s, percent for >10s | NNG response times (0.1/1/10s), Miller 1968 | COVERED | render `state-answers-late`, interaction.md Feedback timings and Loading patterns |
| F2 | Under 400ms system response | LoUX Doherty | COVERED | laws-of-ux.md 6, `transition-duration-500ms-or-longer` |
| F3 | Undo over confirm for reversible actions | NNG heuristic 3, DOET errors | COVERED | components.md, copy.md Confirmation dialog |
| F4 | Visible exits (close, cancel) on overlays | NNG heuristic 3 | COVERED | accessibility.md Escape route on modal |
| F5 | Hover-only actions fail touch and keyboard | NNG | COVERED | `hover-only-card-actions` |
| F6 | Disabled looks disabled and says why | NNG | COVERED | `cursor-not-allowed-no-visual`, `menu-row-disabled-without-reason` |
| F7 | Icons carry visible text labels in navigation | NNG icon usability | B-RENDER | nav/tab bar items whose visible content is only an svg/img (aria-label alone) |
| F8 | Logo links to the home page | DMMT, NNG, LoUX Jakob | B-LINT | header/nav logo img/svg not inside a[href] (krug.md has the guidance) |
| F9 | Current location shown (aria-current, you-are-here) | DMMT street signs, NNG | PARTIAL | krug.md, accessibility.md aria-current; static check for a nav with no aria-current is possible (low) |
| F10 | Auto-dismissing toast must not carry the only path to an action (Undo) | WCAG22 2.2.1 Timing Adjustable (interpretation), M3 snackbar | C | foundations/components.md Toast specs: today says auto-dismiss 3 to 5s for all toasts; conflict for toasts with actions |
| F11 | Infinite scroll keeps footer reachable | NNG | COVERED | `infinite-scroll-no-pagination` |
| F12 | No hamburger on desktop | NNG | COVERED | `nav-equal-hamburger-desktop` |
| F13 | Recognition over recall; visible options | NNG heuristic 6 | COVERED | laws-of-ux.md, krug.md |
| F14 | Conventions first (Jakob) | LoUX, DMMT | COVERED | krug.md conventions, laws-of-ux.md 11 |
| F15 | Nielsen's 10 heuristics as an audit frame | NNG | C | new references/laws/nielsen-heuristics.md, cited from commands/ux-audit.md |
| F16 | Microinteraction structure (trigger, rules, feedback, loops) | Saffer (HEND) | COVERED | interaction.md, motion-principles.md |
| F17 | Animate transform/opacity only; durations 100 to 500ms | M3 motion, NNG animation | COVERED | `animating-layout-properties`, motion-principles.md |

## G. Data visualization and dashboards

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| G1 | Bar axes start at zero | Tufte lie factor, Few | PARTIAL / B-LINT | dashboard.md Do/Don't; static on chart configs: Chart.js beginAtZero:false or min on bar, Recharts BarChart YAxis domain not starting at 0 |
| G2 | Pie/donut 5 slices or fewer | Few, dashboard.md | PARTIAL / B-LINT | guidance present; static: pie dataset length > 5 |
| G3 | No 3D charts | Tufte, Few | PARTIAL / B-LINT | dashboard.md; static: options3d, 3d: true |
| G4 | No dual y-axes | Few | C (+B-LINT low) | add to surfaces/dashboard.md; static: two y axes (yAxisId, y1) |
| G5 | Maximise data-ink: faint or no gridlines, no chart borders, backgrounds, gradients, shadows | Tufte data-ink, chartjunk | C | surfaces/dashboard.md Chart specs (partial: "no soft drop shadows" in Brutalist pattern) |
| G6 | Label series directly instead of a distant legend | Tufte, Few | C | surfaces/dashboard.md |
| G7 | Small multiples over spaghetti (more than about 4 to 5 lines) | Tufte | C | surfaces/dashboard.md (static: line chart with >5 series, low) |
| G8 | No excessive precision in KPIs (no 3+ decimals, no 7-digit raw numbers) | Few pitfall 3 | B-LINT | text regex in stat/td: \d\.\d{3,}, unabbreviated >= 1,000,000 in a tile |
| G9 | Sort categorical bars by value unless ordinal | Few | C | surfaces/dashboard.md Chart type selection |
| G10 | No meaningless variety: same chart type for same kind of data | Few pitfall 6 | C | surfaces/dashboard.md |
| G11 | Every figure has context (comparison, period, count) | Few pitfall 2 | COVERED | dashboard.md principle 11 |
| G12 | Chart states (empty, loading, error) and text alternative | dashboard.md | COVERED | dashboard.md Chart with full state coverage, Chart accessibility |
| G13 | Color for meaning only; colorblind-safe | Few, WCAG 1.4.1 | COVERED | dashboard.md principle 5 |
| G14 | Sparklines for at-a-glance trend | Tufte | COVERED | dashboard.md Inline sparkline |

## H. Canon frameworks and new surfaces

| # | Principle | Source | Status | Where / proposal |
|---|---|---|---|---|
| H1 | Laws of UX (all 30) | LoUX | COVERED | laws/laws-of-ux.md (all 30 sections) |
| H2 | Krug: billboard test, conventions, street signs, home page test, omit needless words | DMMT | COVERED | laws/krug.md |
| H3 | Norman: affordances, signifiers, mapping, feedback, constraints, gulfs, errors | DOET | COVERED | laws/norman.md |
| H4 | Application posture (sovereign, transient, daemonic) sets density and chrome | AF | C | new references/laws/cooper.md, linked from surfaces/dashboard.md (density) |
| H5 | Reduce excise (navigation, confirmations, modal steps that do not serve the goal) | AF | C | references/laws/cooper.md |
| H6 | Perpetual intermediates: optimise for the middle user, offer accelerators | AF, NNG heuristic 7 | C | references/laws/cooper.md; accelerators partly in accessibility.md keyboard shortcuts |
| H7 | Signal-to-noise, progressive disclosure, forgiveness, consistency | UPD | COVERED | laws-of-ux.md, norman.md, krug.md |
| H8 | AI interface patterns: streaming state, stop/cancel, regenerate, editable output, citations/grounding, uncertainty, disclosure of AI content | HEND AI section (Shape of AI, Microsoft HAX, Google PAIR, Apple HIG Generative AI, NNG chatbot guidelines), EU AI Act Art. 50 | C | new references/surfaces/ai-interface.md (copy.md has only "Tone for AI features") |
| H9 | Agentic UI: scope, oversight, reversible and auditable actions, consent before acting | HEND (Noessel, Yocco, SLDS agentic) | C | references/surfaces/ai-interface.md |
| H10 | Internationalization: text expansion, RTL, logical properties | HEND i18n | COVERED | accessibility.md Multi-language and RTL; seo.md hreflang |
| H11 | Behavior models (Fogg B=MAT, CREATE funnel, Hook) | TOGI | C (low) | process/discovery-protocol.md as a framing note with an ethics boundary |
| H12 | Design critique framing | HEND (Connor, Irizarry) | COVERED | commands/ux-critique.md |
| H13 | Usability testing with about 5 users per round | NNG | COVERED | laws/krug.md Usability Testing on a Budget |
| H14 | Generic-AI-look causes: distributional convergence, no direction, vague feedback; fix with references, tokens, separated direction/exploration/build | SLOP | COVERED | styles/anti-slop.md, process/generation-modes.md, process/creative-selection.md |
| H15 | Iterate from screenshots because the model cannot see its output | SLOP (superdesign, vp0) | COVERED | render check exists; responsive.md "Verify: this is mandatory" |

## Counts

- Rows: 155. Three rows fold into another row's check (B6 into B5, B21 into A18, E6 into E5), so 152 distinct principles.
- Covered: 67 (63 COVERED, E18 covered by img-no-dimensions, and 3 PARTIAL where guidance exists and a check is low value: A7, B7, F9)
- Missing: 85
  - machine-checkable: 60 (38 render measurements, 22 static lint rules incl. G1 to G3 whose guidance exists but no check)
  - guidance only: 25

Note on complaints probes: every proposed render rule automatically becomes a `rule-clear` probe target once its id is in `_RULES`, so no new probe kind is needed. Before a rule exists, the existing `text-absent` probe can hold C2 and C3 (for example text-absent "only 3 left"). It cannot hold A23, because a <title> is not visible text, and probes only read what is visible.

## Number checks and conflicts

- Target size: WCAG 2.2 AA 2.5.8 = 24x24 CSS px with a 24px-circle spacing exception; AAA 2.5.5 = 44x44. Apple HIG: default 44x44 pt, minimum 28x28 pt (iOS), 60x60 pt visionOS, button centers 60pt apart in visionOS. Material/Android: 48x48 dp with 8 dp between targets. ux-skill accessibility.md says "Web minimum: 44x44px" and tags it Critical: that is the AAA level, not AA. Recommend: hard fail under 24 (AA), advisory under 44 on touch widths.
- Line length: Baymard 50 to 75 chars (Ruder 50 to 60); WCAG 1.4.8 (AAA) max 80 (40 CJK); Bringhurst 45 to 75. ux-skill landing measure 42 to 56 is below Baymard's floor: label it a house default.
- Contrast: 4.5:1 normal, 3:1 large text (18pt = 24px, or 14pt bold = 18.66px), 3:1 non-text (1.4.11). ux-skill matches.
- Text spacing (1.4.12): 1.5x line height, 2x paragraph spacing, 0.12em letter, 0.16em word. Reflow (1.4.10): 320 CSS px wide / 256 tall. ux-skill render widths start at 390.
- Response time: NNG 0.1s / 1s / 10s (Miller 1968); Laws of UX Doherty 400ms. Not in conflict: different limits for different purposes.
- Mobile text: Apple default body 17pt, minimum 11pt; ux-skill mobile body 16px. iOS zoom on focus is triggered by input font-size under 16px; ux-skill ties it to body size, which is only right if inputs inherit body size.
- Toasts: ux-skill components.md says every toast auto-dismisses in 3 to 5s; a toast carrying an action (Undo) that vanishes is a time limit under WCAG 2.2.1 (interpretation). Recommend: persistent or user-dismissed when the toast holds an action.
- Checkout field counts: Baymard pages give both 11.3 average form fields and 19.9 average form elements; they measure different things.
- Inline validation: Baymard cites 31% and 32% of sites with none, on different pages/dates.
