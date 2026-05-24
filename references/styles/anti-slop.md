# Anti-slop — the forbidden patterns

> Distilled from `gpt-taste` and `design-taste-frontend`. These are the AI fingerprints that mark output as machine-generated. Avoiding them is the price of admission to high-end frontend.

## Principles

1. **Specificity beats genericity.** A generic 3-card row is the AI tell. Asymmetry, named brands, organic numbers — those signal a human (or a careful machine).
2. **Restraint beats decoration.** Single accent color, neutral base, intentional white space. Don't add a gradient because the model defaults to one.
3. **Type carries weight, not just size.** Hierarchy from weight + color + spacing — not just `text-9xl`.
4. **Motion has meaning or it doesn't ship.** Decorative animation is slop. Every motion expresses cause and effect.
5. **Content is a design surface.** "John Doe" + "Acme Corp" + `99.99%` is content slop and ruins the design no matter how good the layout is.

## Forbidden — visual & CSS

| Don't | Do instead |
|---|---|
| Default `box-shadow` glows, neon outer glows | Inner border (`border-white/10`) + tinted inner shadow (`shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`) |
| Pure black (`#000000`) | Zinc-950, charcoal, off-black |
| Oversaturated accents | Desaturate to < 80% — high contrast comes from value, not saturation |
| Text-fill gradients on large headers | Solid color + weight hierarchy |
| Purple/blue "AI" gradient combos | Single accent (Emerald, Electric Blue, Deep Rose) + neutral |
| Custom mouse cursors | Native cursors only — performance + a11y + outdated |
| Mixing warm gray + cool gray in same project | Pick one (Zinc OR Slate) and commit across the whole surface |
| Default shadcn/ui | Customize radii, colors, shadows — never ship the default look |

## Forbidden — typography

| Don't | Do instead |
|---|---|
| Serif on dashboards/admin/data UIs | Sans-serif only — Inter + JetBrains Mono, Geist + Geist Mono, or Satoshi + JetBrains Mono are all fine |
| H1 that screams (`text-9xl`) | Weight + color + spacing carry hierarchy; cap display at `text-4xl md:text-6xl tracking-tighter leading-none` |
| H1 longer than 2 lines | Tighten the headline; split into headline + supporting line if needed |
| Mismatched font families per section | One display + one body across the project |
| Body text > 75 characters per line | `max-w-[65ch]` on paragraphs |

## Forbidden — layout & spacing

| Don't | Do instead |
|---|---|
| 3 equal cards in a row ("feature grid") | 2-col zig-zag, asymmetric grid, horizontal scroll, or bento |
| Centered hero with text over dark image | Asymmetric hero — text left or right, image with subtle stylistic fade |
| Center alignment when DESIGN_VARIANCE > 4 | Split screen, left-aligned over right-aligned, asymmetric white-space |
| `h-screen` on mobile hero | `min-h-[100dvh]` — `100vh` is broken on iOS Safari |
| Flex math like `w-[calc(33%-1rem)]` | CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) |
| Random spacing increments | 4/8 rhythm — every gap, padding, margin in multiples of 4 |
| Horizontal scroll on mobile | Always — there's no exception |
| Meta-labels like "SECTION 01" | If the section needs a label, name it; if not, delete it |

## Forbidden — content (the "Jane Doe" effect)

This is what immediately marks output as AI. The design can be perfect; if the placeholder content is generic, the whole thing reads as slop.

| Don't | Do instead |
|---|---|
| "John Doe", "Jane Smith", "Sarah Chan", "Jack Su" | Creative + plausible: "Mira Halawani", "Bashar Kuzbari", "Lina Touma", "Adrian Volkov" |
| "Acme", "Nexus", "SmartFlow", "Zenith", "Stellar" | Contextual: a fintech might be "Tash" or "Ledgerine"; a CRM might be "Patio" or "Greta" |
| "99.99%", "50%", "$1,234", `+1 (555) 123-4567` | Organic: "47.2%", "63%", "$3,847.20", "+1 (312) 847-1928" |
| Lucide / Heroicons user-egg avatars | Real placeholder photos via `picsum.photos/seed/<random>/200/200` or distinct SVG initials with intentional styling |
| Filler verbs: "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize" | Concrete verbs that describe what the product does: "Send", "Settle", "Track", "Decide" |
| Unsplash URLs | `picsum.photos/seed/<random>/W/H` or hand-picked stock |
| Stock testimonials ("This product changed my life") | Specific testimonials with role + company + measurable outcome |

## Forbidden — interaction & motion

| Don't | Do instead |
|---|---|
| Static "successful" state with no loading/empty/error | Always ship all four states |
| Generic circular spinners | Skeleton loaders matching the layout shape |
| Linear easing on UI motion | `ease-out` on enter, `ease-in` on exit, or spring physics |
| Instant state changes (0ms) | 150–300ms for micro-interactions |
| Slow motion (>500ms) | Cap micro at 300ms, complex at 400ms |
| Continuous animations driven by `useState` | `useMotionValue` + `useTransform` only — `useState` causes re-render storms |
| Hover-only critical interactions | Tap/click for primary; hover is enhancement only |
| Animating `width`, `height`, `top`, `left` | `transform` + `opacity` only — hardware acceleration |
| Ignoring `prefers-reduced-motion` | Wrap motion in `usePrefersReducedMotion()` check |

## Forbidden — components

| Don't | Do instead |
|---|---|
| Generic card containers everywhere | Cards only when elevation communicates hierarchy; otherwise `border-t`, `divide-y`, or pure negative space |
| Emoji as icons | Google Material Symbols (preferred — `Material Symbols Outlined` / `Material Symbols Rounded` / `Material Symbols Sharp`) styled via font-variation-settings. Phosphor / Radix / Lucide are acceptable fallbacks at consistent stroke width (1.5 or 2.0). |
| Mixed icon styles (filled + outline at same level) | One icon family, one style across the surface |
| No imagery anywhere (a wall of text + cards) | Use real imagery interspersed with content. Placeholders via `picsum.photos/seed/<descriptive-seed>/W/H`. Layouts must accommodate imagery, not avoid it. |
| Random radius values | Token: `rounded-sm` / `md` / `lg` / `2xl` / `[2.5rem]` — pick a scale, stick to it |
| Toast that steals focus | `aria-live="polite"` toasts; never grab focus |
| Placeholder-only labels | Visible label above; helper below; error below input |
| 3-column card hero grids on landing | Bento, masonry, asymmetric — anything but the equal-3 |

## Tokens / numeric guardrails

- **Color saturation**: < 80% for any accent
- **Contrast**: ≥ 4.5:1 for body text, ≥ 3:1 for large/UI text
- **Spacing**: multiples of 4 (4, 8, 12, 16, 24, 32, 48, 64)
- **Touch targets**: ≥ 44×44 pt (iOS), ≥ 48×48 dp (Android)
- **Animation duration**: 150–300ms micro, ≤400ms complex, never >500ms
- **Body line length**: 35–60 chars mobile, 60–75 desktop (`max-w-[65ch]`)
- **Max H1 lines**: 2
- **Container max-width**: 1400px or `max-w-7xl`
- **Font scale**: 12 / 14 / 16 / 18 / 24 / 32 / 48 / 64 / 96 (consistent ratio)

## Checklist (run before shipping any /ux-design output)

- [ ] No purple/blue AI gradient (Critical)
- [ ] No generic names or "Acme/Nexus" brand placeholders (Critical)
- [ ] No 3-equal-cards layout (High)
- [ ] No centered hero when DESIGN_VARIANCE > 4 (High)
- [ ] No `h-screen` for mobile hero (High)
- [ ] No pure `#000` (High)
- [ ] All four interaction states present (Critical)
- [ ] All animations on transform/opacity only (High)
- [ ] H1 ≤ 2 lines (Medium)
- [ ] Single accent color, < 80% saturation (Medium)
- [ ] One icon family at consistent stroke width (Medium)
- [ ] Spacing on 4/8 rhythm (Medium)
- [ ] No Unsplash URLs (Medium)
- [ ] `prefers-reduced-motion` respected (High)
- [ ] Imagery is present and intentional (Medium) — text-only walls are forbidden
- [ ] Icons are Google Material Symbols (preferred) or one consistent SVG family (High)
