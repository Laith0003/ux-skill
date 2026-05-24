# /ux-design self-review — Dot landing demo

Anti-slop bans I consciously avoided:
1. Inter font — used the Apple system stack (`-apple-system, BlinkMacSystemFont, "SF Pro Display", "Geist", system-ui, sans-serif`) with an SF Arabic fallback under `dir="rtl"`.
2. Purple/blue AI gradient — the only chromatic accent is the brand-mark dot (`--brand-dot: #0EA5E9`) used as tiny punctuation only; the entire surface is monochrome zinc-950 on white. Semantic colors stay tied to meaning (emerald for "matched / added" success only).
3. Generic placeholder names + brands — used "Lina Touma", "Bashar Kuzbari", "Mira Halawani", "Adnan Tabbaa" and real Jordanian brands (Bashiti Hardware, Café Younes, Wild Jordan Center, Mlabbas, Casper & Gambini's).
4. Round/cliché numbers — 23,847 active members, 47.2% return rate, 1.7× spend uplift, 2,418,560 points awarded, 8,734 redemptions, 1,260 / 2,000 to Gold; phone `+962 79 786 8335`.
5. Centered hero — asymmetric 7/5 split, asset side translates `y-8` and the floating stamp card sits at `-bottom-6 -start-4` with a `-3deg` rotation.
6. Three equal cards — value-prop section is zig-zag: 8/4, then 5/7, then full-width.
7. `h-screen` — never used; layout flows by content with `min-h` available if needed.
8. `pl-/pr-/text-left/text-right` — used logical `ps-`, `pe-`, `text-start`, `text-end`, `ms-`, `start-`, `-start-`, `-bottom-` so RTL flips correctly; brand-dot uses `margin-inline-start`; CTA arrow icons get `rtl:rotate-180`.
9. Emoji — every glyph is inline SVG with 1.5–2px stroke and `currentColor` (Lucide/Feather style). Brand-mark dot is a pure CSS circle, not an icon.
10. Pure `#000` — `--ink: #0A0A0B` (with `zinc-950` Tailwind utility as the visible counterpart).
11. Customer email ask — final CTA is phone-only, with explicit "No password, no email" microcopy; partners get an email line (`partners@thedotwallet.com`) because that side is allowed.
12. "E.164" — never spoken; user-facing label is just "Your phone" with the `+962` prefix surfaced visually.
13. Filler words — no "Elevate / Seamless / Unleash / Next-Gen / Empower". Voice is "50 points added.", "Show your phone. Earn. Spend.", "Sent to your phone."
14. Unsplash / stock — no remote images; assets are inline SVG, CSS shapes, and the receipt + stamp card mocks built from Tailwind.
15. Animated `width/height/top/left` — every motion is `transform` (translate, rotate) and `opacity` only; scroll-path drawing animates `stroke-dashoffset` (allowed); reduced-motion preference disables animations.

Arsenal patterns used:
- **Asymmetric split hero** — `.grid-cols-12` with `lg:col-span-7` text + `lg:col-span-5` asset, asset shifted with `lg:translate-y-8`, plus floating stamp card at `-bottom-6 -start-4` rotated `-3deg`; `hero-fade` radial gradient subtly biases the asset side and mirrors under RTL.
- **Scroll progress path** — fixed `position` SVG line on the start side, hairline guide plus a `var(--ink)` drawn path animated via `stroke-dashoffset` tied to `scrollProgress`; a small `--brand-dot` puck (3.5px circle) rides the path using a 3-segment piecewise cubic eased by Alpine in a `requestAnimationFrame` loop. Hidden on mobile so it doesn't crowd small screens.
- **Spotlight border card** — `.spotlight-card` uses a `::before` pseudo with `radial-gradient(380px circle at var(--mx) var(--my), ...)` masked via `mask-composite: exclude` so only the border lights up; `@mousemove` Alpine handlers feed CSS custom props. Applied to all 4 value-prop cards.
- **Skeleton shimmer** — `.skeleton` blocks in the live event feed show until Alpine flips `ready = true` after 1.4s, then the real Lina/Bashar/Mira/Adnan rows fade in with `rise-in`. Shimmer keyframes are RTL-aware (reversed translate direction under `dir="rtl"`).