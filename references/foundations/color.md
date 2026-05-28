# Color

> Color carries meaning when scarce and noise when generous. A disciplined palette is the difference between a designed product and a decorated one.

## Tools we recommend for color discovery

When the brief is open and you need to explore palettes before locking one in, these are the tools we actually use. Each one has a different job; pick by what you're trying to figure out.

| Tool | URL | When to reach for it |
|---|---|---|
| **Huemint** | https://huemint.com | AI-driven palette generator with context awareness. Best when you want to feed in a brief ("fintech, calm, dark mode") and explore variants. |
| **Picular** | https://picular.co | Google Image-based color picker. Type "Spotify green" or "Tesla red" and get the dominant hue. Useful for matching a brand the user keeps citing. |
| **Colourcode** | https://colourco.de | Cursor-position-driven palette explorer. Best for taste calibration when you don't know what you want yet. |
| **Colir** | https://colir.io | Web color browser organized by hue family. Useful for finding the right shade family before fine-tuning. |
| **Coolors** | https://coolors.co | The mainstream palette generator. Best when you need 5-color schemes fast and don't have a strong brief. |
| **PhysicallyBased.info** | https://physicallybased.info | Public PBR materials database — real-world albedo / roughness / IOR values for actual materials (oak, brushed aluminium, glass, leather). Cite this when you need an *honest* L-value for a designed surface rather than guessing. |

**For verifying contrast after picking colors:**

| Tool | URL | Job |
|---|---|---|
| WebAIM Contrast Checker | https://webaim.org/resources/contrastchecker/ | The canonical WCAG AA/AAA verifier |
| OKLCH Color Picker | https://oklch.com | For palettes designed in OKLCH (the perceptual space) |
| APCA contrast | https://www.myndex.com/APCA/ | Newer perceptual contrast standard (WCAG 3 draft) — use for forward-compat checks |

ux-skill's `data/palettes.json` already includes 176 palettes verified for AAA contrast on body text. When you pick one of those, you've already cleared the contrast bar. When you build a new one from these tools, run it through WebAIM before shipping.

## Principles

1. **Color is a scarce resource** — Build the foundation in neutrals. Reserve chromatic energy for action (CTAs, links, focus rings, status indicators). Decoration uses spacing, typography, and contrast; not color.

2. **Semantic tokens, never raw hex in components** — Define semantic names (`primary`, `secondary`, `surface`, `on-surface`, `error`, `success`, `warning`) and reference them everywhere. Raw hex values scattered across components break theming, dark mode, and accessibility.

3. **Three-layer token architecture** — Primitive (raw values: `--color-blue-600: #2563EB`), semantic (purpose aliases: `--color-primary: var(--color-blue-600)`), component (component-specific: `--button-bg: var(--color-primary)`). Components reference component tokens; component tokens reference semantic; semantic references primitive.

4. **Light and dark are designed together** — Dark mode is not an inversion. Re-tune accents, re-calibrate text, rebuild the elevation ladder. The same hex never appears in both modes.

5. **Color carries reinforcement, not meaning** — Pair every color signal with an icon, text, or pattern. Red errors include a red color AND an icon AND a text message. Color-blind users and screen reader users get the same signal.

6. **Never pure black, never pure white** — Pure `#000000` is banned in product chrome (use `#050505` to `#1A1A1A`). Pure `#FFFFFF` reads as default; warm or cool off-whites at `#FAFAFA` to `#F7F7F4` read as designed.

7. **One accent, not three** — One primary brand accent appears on CTAs, focus rings, and the rare semantic highlight. Three or four accents fight for attention and dilute meaning.

8. **Saturation below 80% for accents** — Highly saturated accents on dark surfaces vibrate. Desaturate slightly so they settle and blend.

9. **Semantic state colors are reserved** — Green = success, red = destructive, amber = warning. Never repurpose semantic colors as brand colors. If the brand color happens to be green, success notifications get a different green (shifted in chroma) so meaning stays unambiguous.

10. **Logos and partner marks render monochrome** — Customer logo strips use a single muted color at uniform optical height. Native-color logo walls fight the page's palette and read as uncurated.

## Do / Don't

| Do | Don't |
|---|---|
| Use off-white backgrounds (`#FAFAF8`, `#F7F7F4`) | Use pure `#FFFFFF` as the canvas |
| Use deep charcoal for primary text (`#171717`, `#1F1F1F`) | Use pure `#000000` as body text |
| Define semantic tokens and reference them in components | Hardcode hex values inside components |
| Pair color signals with an icon AND a text label | Convey state through color alone |
| Test foreground/background pairs at 4.5:1 (AA) or 7:1 (AAA) | Ship gray-on-gray combinations |
| Design dark mode variants alongside light | Invert light mode to produce a "dark mode" |
| Use one accent color, applied surgically | Use three or four accents at near-equal weight |
| Greyscale customer logo walls | Display logos in their original brand colors |
| Use semantic state colors (success/error/warning) only inside product UI and status pills | Use semantic colors as section backgrounds or brand decoration |
| Use HSL or oklch format for opacity control | Build palettes only in raw hex |
| Apply a 3 to 6% noise overlay over solid color blocks | Ship flat solid color blocks |
| Pick warm OR cool neutrals; commit | Mix warm and cool grays in the same project |
| Use restrained gradients in 30 to 60 degree hue windows | Ship rainbow blob gradients |
| Tint shadows to match the background hue | Use generic black shadows under colored cards |
| Reserve true black for the brand mark or emphasized UI controls | Use pure black liberally across body text and backgrounds |

## Examples

### Pattern: Single accent on near-monochrome chassis
**Use when**: Any product surface where restraint matters — premium SaaS, fintech, AI tooling, editorial, B2B.
**Anti-pattern**: Five accent colors splattered across body, links, CTAs, and decorative illustration simultaneously.
**How**: Build the chassis from off-white background, charcoal text, mid-gray dividers. Pick one saturated accent (a calibrated blue, green, teal, violet, or warm ochre). Deploy the accent only on primary CTAs, in-line links, focused form states, and one or two illustrated highlights per section. The accent loses its signaling power if everything is "the accent."

### Pattern: Light + dark with separately calibrated accents
**Use when**: Any product shipping both light and dark variants.
**Anti-pattern**: One hex value used as the accent across both modes (vibrates on dark, mutes on light).
**How**: Define a paired palette. A teal that reads at `#1A8FA8` on white shifts to `#5BD9EE` on near-black. Lift lightness by 10 to 15% when moving to dark surfaces so chroma reads at the same perceived intensity. Reduce chroma slightly on highly saturated accents in dark mode to prevent vibration.

### Pattern: Dark mode elevation ladder
**Use when**: Building surfaces for dark variants of any product.
**Anti-pattern**: Using drop shadows to express elevation in dark mode (shadows get swallowed on dark backgrounds).
**How**: Build a 4 to 5 step lightness ladder rather than relying on shadows.
- Page background: L = 4 to 8% (slightly cool or neutral cast; never pure black)
- Card / surface: L = 8 to 12%
- Raised surface / popover: L = 14 to 18%
- Overlay / modal scrim: page background at 60 to 80% alpha
- Each lift is ~3 to 5% L; cumulative effect creates real depth without shadows

### Pattern: Tinted shadows that match the surface hue
**Use when**: Cards, modals, hero imagery, or any elevated container.
**Anti-pattern**: A black shadow at 30% opacity under a colored card.
**How**: A teal section gets a teal-mist shadow. A faintly cool background wants a faintly cool shadow. Default formula: `0 8px 32px` at 8 to 14% alpha in the brand hue, often paired with a tighter `0 1px 2px` black at 6% for grounding. The combined effect reads as "lit from inside the brand."

### Pattern: Section-anchored background shifts
**Use when**: Long pages need visual chunking without decorative dividers.
**Anti-pattern**: Three or four bright color blocks alternating down the page.
**How**: Use three to four micro-shades of off-white (`#FFFFFF` → `#FAFAFA` → `#F4F6FA`) to differentiate sections. The page feels structured without feeling segmented. Reserve a true-dark band for one moment per page — often the final CTA or one feature deep-dive.

### Pattern: Semantic color discipline
**Use when**: Status pills, error states, success confirmations, dashboard data.
**Anti-pattern**: Using red as a brand accent and then a red error state — the meaning collapses.
**How**: Reserve red for destructive and error states. Reserve green for success and live. Reserve amber for warning. Reserve a single neutral or branded blue for informational. These four colors do not appear as brand colors or section backgrounds; they appear only in pills, badges, dashboard data, log lines, and validation states.

### Pattern: Greyscale logo strip
**Use when**: Customer logo walls, partner showcases, "as used by" sections.
**Anti-pattern**: Logos at their native brand colors and native pixel heights, packed in a row.
**How**: Apply `filter: grayscale(1) contrast(1.1)` or use pre-rendered greyscale assets. Normalize all logos to the same target color (text color, 70% black, or white at 60% alpha on dark) and the same optical height (not the same pixel height; adjust per logo so they read evenly). Generous gutters between logos. The strip reads as a single band of social proof.

### Pattern: Subtle gradient on a single hero
**Use when**: One section of a long page needs ambient depth or atmospheric color.
**Anti-pattern**: Three gradient sections in a single page — the palette reads uncertain.
**How**: Apply one gradient to the hero or one feature section. Use 2 to 3 stops max with a narrow hue spread (30 to 60 degree window). Saturation stays low; the gradient adds light, not color. Mesh gradients of 3 to 5 blurred radial orbs in brand colors, gaussian blur 120px, drift slowly (4 to 8s loops, 3 to 6px translation), positioned outside the safe text area.

### Pattern: Per-feature color codes
**Use when**: A feature stack of 4 to 6 items needs navigational distinction.
**Anti-pattern**: Random color assignment with no semantic logic.
**How**: Assign each feature a distinct color and preserve that color throughout — subnav highlight, icon tint, product UI screenshot accent. Section A is teal-on-ink; section B is coral-on-ink; section C returns to neutral. The colors form a memorable system: teal = collaboration, coral = AI, violet = automation. The product UI carries the color forward so marketing surface and product surface match.

### Pattern: Brutalist light-print substrate
**Use when**: Industrial, technical, or anti-mainstream products.
**Anti-pattern**: Glassmorphism, soft drop shadows, or full-spectrum gradients on a brutalist substrate.
**How**: Background warm matte off-white (`#F4F4F0` to `#EAE8E3`) — unbleached documentation paper, not bright SaaS white. Foreground near-black carbon ink (`#050505` to `#111111`). Accent a single aviation or hazard red (`#E61919` or `#FF2A2A`), used as strike-throughs, structural dividers, or vital data highlights. The hazard red carries all chromatic load. No gradients, no soft shadows, no translucency beyond simulated noise overlays.

### Pattern: Brutalist dark tactical substrate
**Use when**: Industrial, terminal-adjacent, or tactical products.
**Anti-pattern**: Pure `#000000` background that reads as raw HTML, not designed.
**How**: Background deactivated CRT black (`#0A0A0A` to `#121212`). Foreground white phosphor (`#EAEAEA`). Same hazard red accent. An optional terminal green (`#4AF626`) may appear on a single specific element (one status indicator or one live readout) — never as a general body color.

### Pattern: High-end ethereal glass substrate
**Use when**: Technical, AI, SaaS surfaces where premium ambient depth is required.
**Anti-pattern**: Flat solid color hero blocks with no texture or depth.
**How**: Substrate is the deepest OLED black (`#050505`). Radial mesh gradients in the background — subtle glowing orbs in deep purple, emerald, indigo, or magenta, well outside saturation thresholds that would feel garish. Card surfaces near-vantablack with heavy backdrop blur and hairline white borders at low opacity (`rgba(255,255,255,0.08)` to `rgba(255,255,255,0.12)`). Inner highlights on glass elements: a single 1px inset top highlight at low opacity to suggest a glass plate catching light. Apply backdrop-blur only to fixed or sticky elements; never to scrolling content.

### Pattern: High-end editorial luxury substrate
**Use when**: Lifestyle, real estate, agency, hospitality surfaces.
**Anti-pattern**: Generic SaaS off-white with cool gray neutrals — reads as templated.
**How**: Substrate warm cream (`#FDFBF7`) or deep espresso for dark variants. Accent tones muted sage, ochre, soft terracotta, dusty rose, or a single saturated jewel tone used surgically. High-contrast variable serif fonts at massive scale. Subtle film-grain overlay at very low opacity (`0.03`) on a fixed `pointer-events-none` layer for a physical paper feel.

### Pattern: High-end soft structuralism substrate
**Use when**: Consumer, health, portfolio, premium hardware companion apps.
**Anti-pattern**: Hard drop shadows under floating components.
**How**: Substrate silver-gray, warm white, or completely white. Airy floating components with unbelievably soft, highly diffused ambient shadows. The shadow is large in spread but extremely low in opacity. Massive bold display sans-serifs. Occasional precision color accents — a single saturated color reserved for a CTA or single brand mark. The single saturated color provides the only chromatic punch on the page.

### Pattern: Mesh-orb hero background
**Use when**: Premium creative-tool category, AI products, modern SaaS heroes.
**Anti-pattern**: Single static gradient covering the entire hero.
**How**: 3 to 5 large, blurred radial gradients in brand colors form ambient backgrounds. Gaussian blur ~120px. Noise opacity 60 to 80% on the gradient layer. Each orb animated subtly: 4 to 8 second ease loops, 3 to 6px translation. Orbs positioned outside the safe text area so contrast on copy stays consistent. The hero feels alive without distracting.

### Pattern: Grain / noise overlay
**Use when**: Solid color blocks that would otherwise read as flat or "stock."
**Anti-pattern**: Applying grain to scrolling containers (triggers continuous GPU repaints; mobile frame rate collapses).
**How**: A 3 to 6% opacity high-frequency noise texture sits over solid color blocks to break up the digital flatness. The grain is barely perceptible — but its absence is what makes a flat color look stock. The noise must attach EXCLUSIVELY to fixed `pointer-events-none` pseudo-elements. Never on scrolling content.

### Pattern: Per-section accent color propagating to product UI
**Use when**: Marketing surfaces showing product screenshots embedded inside feature sections.
**Anti-pattern**: Marketing surface in teal, product screenshot in default blue — visual disconnect.
**How**: Each feature section gets a section accent color (teal = collaboration, coral = AI, violet = automation). The product UI screenshot embedded inside that section has interface chrome tinted to match the section accent. The "color match" between marketing surface and product surface signals the team controls both ends. The screenshot is a styled render where the accent is tuned to the surrounding context.

## Tokens / values

### Contrast targets
- Normal text: 4.5:1 minimum (WCAG AA)
- Large text (18pt+ regular or 14pt+ bold): 3:1 minimum
- Target for all body copy: 7:1 (WCAG AAA) where feasible
- Icons and UI controls: 3:1 minimum for boundaries, 4.5:1 for small icons
- Data lines, bars vs background: 3:1 minimum; text labels 4.5:1
- Disabled states: contrast not required, but visibly muted (0.4 to 0.6 opacity)

### Background tokens (light mode)
- Pure canvas: avoid `#FFFFFF`
- Off-white default: `#FAFAFA` to `#FBFBFA`
- Warm off-white: `#F7F6F3`, `#FBFBFA`, `#FDFBF7`
- Cool off-white: `#FAFAFA`, `#F9F9F8`
- Section break shade: `#F7F5F2`, `#F4F4F1`, `#FAF8F5`
- Borders / dividers: `#EAEAEA`, `rgba(0,0,0,0.06)` to `rgba(0,0,0,0.10)`

### Background tokens (dark mode)
- Page background: L = 4 to 8% (e.g., `#0A0A0A`, `#0E0E10`, `#111111`, `#121212`); avoid `#000000` except for embedded media (terminal, code)
- Card / surface: L = 8 to 12% (~3-5% L lift from page)
- Raised surface / popover: L = 14 to 18%
- Overlay scrim: page background at 60 to 80% alpha
- Borders / dividers: white at 8 to 12% alpha; focused state at 16 to 24% alpha

### Text tokens (light mode)
- Primary text: `#0A0A0A` to `#1F1F1F` (charcoal, never pure black)
- Body text: `#171717` to `#1F1F1F`
- Secondary text: `#6B7280` to `#71717A` (mid-grays)
- Tertiary text: `#9CA3AF`, `#787774`
- Captions / metadata: `#9B9A97`
- Disabled: 0.38 to 0.5 opacity

### Text tokens (dark mode)
- Primary text: L = 92 to 96%, very low chroma (avoid pure white)
- Secondary text: L = 64 to 72%
- Tertiary / caption: L = 48 to 56%
- Disabled: L = 32 to 40%

### Brand accent rules
- Saturation: < 80% (desaturate so accents blend with neutrals)
- Maximum 1 accent in chrome; one supporting semantic color permitted in data viz
- Accent appears only on: primary CTAs, in-line links, focused form fields, status pips, key icon highlights
- Accent does NOT appear in: section backgrounds, card chrome, body text, decorative illustration fills

### Semantic state colors (reserved)
- Success: green family (e.g., `#16A34A` to `#22C55E` for light; lifted equivalents for dark)
- Error / destructive: red family (e.g., `#DC2626` to `#EF4444` for light)
- Warning: amber family (e.g., `#CA8A04` to `#FACC15` for light)
- Informational: blue family (e.g., `#1F6C9F` to `#3B82F6` for light)
- These colors do NOT appear as primary brand colors. If the brand happens to be green, success uses a different green shifted in chroma.

### Tonal scales
- Build each color as a 50–100–200–300–400–500–600–700–800–900 ramp
- 50 to 200 = soft backgrounds, badge fills
- 300 to 500 = secondary surfaces, borders
- 500 to 700 = primary text, CTAs
- 700 to 900 = strong emphasis, focus
- Light mode default uses 500 to 700 for accents; dark mode uses 300 to 500 (lifted)

### Tinted shadow formulas
- Default: `0 8px 32px` at 8 to 14% alpha in the brand or accent hue
- Grounded: pair with `0 1px 2px` black at 6%
- Diffuse premium: `shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]` — wide-spreading, low-opacity
- Brutalist: hard offset `4px 4px 0 var(--ink)` reading as printed registration mark, NOT a soft drop shadow

### Off-color discipline
- Avoid `#FFFFFF` as canvas; prefer off-whites
- Avoid `#000000` as text or background; use `#050505`, `#0A0A0A`, `#111111`, `#171717`, `#1A1A1A`, `#1F1F1F`
- Avoid pure-saturated accents in dark mode (reduce chroma 10 to 15%)
- Avoid "AI purple gradient" (purple-to-blue on white) — banned

### Palette systems by industry / product type

**SaaS / dev tools:**
- Cool blues (`#2563EB`, `#4F46E5`, `#0EA5E9`), deep purples (`#7C3AED`, `#6366F1`)
- Neutrals: slate or zinc scale
- One accent (teal, amber) for CTA differentiation
- Mood: trust, capability, focused

**E-commerce / retail:**
- Brand-led (varies); common defaults: black, deep red, navy
- Accents: sale red (`#DC2626`), trust green (`#16A34A`)
- Warm gray neutrals for product backgrounds
- Mood: desire, urgency, clarity

**Healthcare / medical:**
- Calming blues (`#0284C7`), soft greens (`#10B981`), warm whites
- Never alarming reds for primary CTAs
- Soft warm grays
- Mood: trust, care, calm

**Beauty / wellness / spa:**
- Soft pinks (`#FCE7F3`, `#F9A8D4`), nude tones (`#FBCFE8`, `#E5C7B7`), sage (`#A7C4A0`)
- Accents: gold (`#D4A574`), terracotta (`#C97B5C`)
- Cream and off-white neutrals
- Mood: serenity, indulgence, premium

**Fintech / banking / crypto:**
- Deep blues (`#1E40AF`, `#0F172A`), black, electric green for growth
- Accents: sharp green (gains), red (losses), gold (premium tier)
- Cool gray and charcoal neutrals
- Mood: trust, precision, authority

**Service / booking / marketplace:**
- Friendly brand colors: coral (`#FF6B6B`), warm blue (`#3B82F6`), teal (`#14B8A6`)
- Accents: booking-success green, premium gold
- Warm gray neutrals
- Mood: approachable, reliable, energetic

**Gaming / entertainment:**
- Saturated, high-contrast: neon pink (`#EC4899`), electric purple (`#8B5CF6`), acid green (`#84CC16`), cyan (`#06B6D4`)
- Accents: glow effects, gradient blends
- Deep black and near-black surfaces
- Mood: energy, immersion, hype

**Food & beverage:**
- Warm earth tones: terracotta (`#C2410C`), olive (`#65A30D`), mustard (`#CA8A04`), deep burgundy
- Accents: cream, butter yellow
- Warm beige and parchment neutrals
- Mood: appetite, craft, warmth

**Education / learning:**
- Optimistic blues (`#3B82F6`), encouraging greens (`#22C55E`), playful yellows (`#FACC15`)
- Accents: achievement gold, growth purple
- Soft warm white neutrals
- Mood: optimism, growth, achievement

**Travel / hospitality:**
- Sky blues, sunset oranges, lush greens, sand neutrals
- Brand-specific accents (airline branding leans bold red or navy)
- Warm sandy beige neutrals
- Mood: escape, wonder, comfort

**Productivity / notes / calendar:**
- Restrained: single accent (`#3B82F6` or `#18181B`) over near-monochrome neutrals
- Subtle category colors (limited palette)
- Warm or cool gray scale neutrals
- Mood: focus, clarity, calm

**Real estate / luxury:**
- Deep charcoal, navy, cream, gold accents
- Accents: brass, deep emerald
- Warm ivory, soft taupe
- Mood: premium, established, trusted

**Kids / family:**
- Saturated primary colors: bright blue (`#3B82F6`), pure red, sunshine yellow
- Accents: playful pastels
- Pure white, soft cream neutrals
- Mood: joy, safety, play

**Crypto / web3:**
- Black, electric purple (`#A855F7`), neon green (`#22D3EE`), white
- Accents: holographic gradients (sparingly)
- Deep black, charcoal neutrals
- Mood: future, decentralized, premium-tech

### Pastel pair system (for muted UI badges)
- Pale red surface `#FDEBEC` with text `#9F2F2D` (destructive, warning)
- Pale blue surface `#E1F3FE` with text `#1F6C9F` (informational, neutral)
- Pale green surface `#EDF3EC` with text `#346538` (success, completion)
- Pale yellow surface `#FBF3DB` with text `#956400` (pending, caution)
- Each pair holds 4.5:1 minimum at the chosen sizes

### Banned color patterns
- Pure `#000000` and `#FFFFFF` in product chrome
- "AI purple gradient" (purple-to-blue on white) as a default
- Rainbow accent palettes with five or more hues
- Saturated brand color used as a full-bleed hero wall
- Multiple gradient sections on a single page
- Customer logos in their native brand colors on a logo strip
- Semantic state colors (red, green, amber) used as primary brand colors
- Text-fill gradients on large headers
- Heavy oversaturated drop shadows (use tinted, low-opacity shadows)
- "Diverging" red-green chart palettes (fails color-blind users)
- Holographic foil treatments as default (acceptable for premium / collectible contexts only)
- Cookie-banner-grade neon green and orange in product chrome
- Pastels paired with saturated accents in the same chrome layer

### Color-blind safe palette specs
- Diverging: blue → gray → red (negative-positive scales); never red → green
- Sequential: single-hue gradient (light to dark) for ordered data
- Qualitative: maximum 7 to 8 distinct hues; perceptually uniform
- Colorblind-safe families: Viridis, Cividis, Magma — perceptually uniform across colorblind variants
- Validate using a color-blindness simulator (deuteranopia, protanopia, tritanopia)
- Always supplement color with patterns, textures, shapes, or icons

### Iconography color rules
- Single-color icons match the surrounding type color OR carry the brand accent
- One icon family across the entire product (same stroke width, same corner radius)
- Icon contrast meets WCAG 4.5:1 for small glyphs, 3:1 for larger
- Filled vs outline discipline — one style per hierarchy level
- Filled for active/selected states, outlined for resting states
- Standardize stroke width (1.5px or 2px); mixing weights is a visible AI tell

### Banned color contexts
- Glowing or animated brain / neural-net / spark iconography for AI features (use restrained generic symbols)
- "Purple-to-pink gradient" as a stand-in for "AI"
- Neon green and orange as default cookie-banner-grade chrome
- Rainbow gradient backgrounds covering large surface areas
- 3D chrome, ray-traced spheres, metaverse cube clusters
- Floating UI windows with drop shadows and tilted-perspective screenshots presented as the default

## Checklist (severity-tagged)

- [ ] All foreground/background pairs verified at 4.5:1 minimum (severity: Critical)
- [ ] Color is never the only signal — every color signal pairs with an icon or text (severity: Critical)
- [ ] Pure `#000000` not used in product chrome (severity: High)
- [ ] Pure `#FFFFFF` not used as canvas; off-white preferred (severity: Medium)
- [ ] One accent color in chrome, applied surgically (severity: High)
- [ ] Accent saturation < 80% (severity: Medium)
- [ ] Semantic state colors (success/error/warning) used only inside product UI and pills (severity: High)
- [ ] Semantic state colors NOT used as brand colors or section backgrounds (severity: High)
- [ ] Dark mode uses desaturated tonal variants, not pure inversion (severity: High)
- [ ] Dark mode accents lifted 10 to 15% in lightness from light-mode equivalents (severity: Medium)
- [ ] Dark mode elevation expressed through lightness ladder, not drop shadows (severity: High)
- [ ] Customer logos rendered monochrome at uniform optical height (severity: Medium)
- [ ] Semantic tokens defined; no hardcoded hex in components (severity: High)
- [ ] Three-layer token architecture: primitive → semantic → component (severity: Medium)
- [ ] HSL or oklch format used for accents (enables opacity control) (severity: Cosmetic)
- [ ] Shadows tinted to match the background hue (severity: Medium)
- [ ] Warm OR cool gray family picked and committed (no mixing) (severity: Medium)
- [ ] Maximum one gradient section per page (severity: Medium)
- [ ] Gradients sit inside a 30 to 60 degree hue window with low saturation (severity: Medium)
- [ ] "AI purple gradient" (purple-to-blue on white) not used (severity: High)
- [ ] Text-fill gradients not used on large headers (severity: High)
- [ ] Pastel pairs hold 4.5:1 contrast at chosen sizes (severity: Critical)
- [ ] Light and dark variants designed together, not inferred from one (severity: High)
- [ ] Chart palettes use diverging (blue-gray-red) or qualitative options that survive color-blindness (severity: Critical)
- [ ] Red-green-only chart palettes avoided (severity: Critical)
- [ ] Modal scrim opacity strong enough to isolate foreground (40 to 60% black) (severity: High)
- [ ] Disabled states use reduced opacity (0.38 to 0.5) + cursor change (severity: Medium)
- [ ] Border and divider colors visible in both light and dark modes (severity: High)
- [ ] Brand mark color preserved through redesigns (equity preservation) (severity: Medium)
- [ ] Single brand accent applied surgically — not as decoration (severity: High)
- [ ] No multiple-color logo walls — customer logos forced to single muted color (severity: Medium)
- [ ] No glowing AI / neural-net / brain iconography (severity: Medium)
- [ ] Noise / grain overlays on fixed `pointer-events-none` layers only (severity: Critical)
- [ ] Backdrop blur only on fixed or sticky elements; never on scrolling containers (severity: Critical)
- [ ] Mesh-orb gradients drift slowly (4 to 8s loops, low amplitude) (severity: Cosmetic)
- [ ] Per-section accent color propagated into embedded product UI screenshots (severity: Cosmetic)
- [ ] Dark surface elevation expressed through L-ladder (page 4-8%, card 8-12%, raised 14-18%) (severity: High)
- [ ] Dark mode text at L = 92 to 96%; never pure white (severity: Medium)
- [ ] Dark mode borders at white 8 to 12% alpha (severity: Medium)
- [ ] One icon family across the product with consistent stroke width (severity: Medium)
- [ ] No emojis as structural icons; SVG only (severity: Critical)
- [ ] Color palettes validated against color-blindness simulators (severity: Critical)

## Related

- See **typography.md** for body text colors paired with these surfaces.
- See **accessibility.md** for contrast minimums, color-not-only rules, and color-blind palette guidance.
- See **dashboards.md** for semantic color discipline inside data viz.
- See **components.md** for state-specific color tokens (default, hover, active, focus, disabled).
- See **motion.md** for accent-tinted shadows and ambient color drift.
- See **layout.md** for section-anchored background color shifts.
- See **interaction.md** for state color shifts on hover, press, and focus.
- See **copy.md** for semantic color paired with success / error / warning microcopy.

### Restraint signals (premium surfaces)
- Off-white or near-black background; never pure
- Charcoal or off-white text; never pure black or pure white
- One accent color, CTA / focus only
- Hairline borders or near-absent shadows
- Mono-color logo and chrome
- Tinted shadows matching surface hue
- Section background shifts via micro-tones, not harsh borders
