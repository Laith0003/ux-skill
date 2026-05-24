# Anti-patterns — lintable AI fingerprints

> The 30 rules below are DETERMINISTIC. Each one has a regex or DOM-query that detects it without an LLM. Run them as a pre-commit hook, in CI, or via the plugin's `/ux-lint` command. Where `styles/anti-slop.md` catalogs the aesthetic feel of AI-generated output, this file catalogs the patterns a linter can flag mechanically.

These are not preferences. They are mechanical tells — patterns the unconstrained generator reaches for reflexively, and that mark output as machine-made within seconds of a human review. Strip them at ship time. Strip them in CI. Don't ship them.

---

## How to read this file

Every rule follows the same shape:

- **Why it's bad**: one line explaining what the pattern signals.
- **How to detect**: a regex, selector, or DOM query that flags the violation without ambiguity.
- **Better alternative**: the pattern that replaces it.
- **Severity**: how badly it impairs the surface.
- **Mode**: which surface type the rule applies to (brand-only marketing surfaces, product-only app surfaces, or both).
- **Example bad / Example good**: actual code snippets, copy-paste-able.

Run them in order: Critical first, then High, then Medium, then Cosmetic. Critical rules block ship.

---

## Severity scale

- **Critical**: ships broken or violates accessibility / SEO / security; blocks merge.
- **High**: ships unprofessional; ranks lower; reduces trust. Must be fixed before next sprint.
- **Medium**: looks AI-generated; degrades premium positioning. Fix before claiming the work is done.
- **Cosmetic**: minor polish miss; doesn't ship-block. Schedule a cleanup pass.

---

## Mode

- **brand-only**: applies to marketing / landing / brand surfaces only. The rule may relax inside product chrome.
- **product-only**: applies to app / admin / dashboard surfaces only. The rule may relax on marketing.
- **both**: applies everywhere.

---

## The 30 rules

### Color

#### 1. Default purple-to-blue AI gradient on white

**Why it's bad**: This is the single strongest visual fingerprint of unconstrained model output. Any time the generator is asked for "something premium" or "a hero," it reaches for purple-to-blue gradient on white. Users associate the combination with template marketplaces and AI-generated landing pages. The work reads as ungrounded the moment it loads.

**How to detect**:

```regex
bg-gradient-to-[a-z]+\s+from-(purple|violet|fuchsia|indigo)-(400|500|600)\s+to-(blue|sky|cyan)-(400|500|600)
```

Also flag literal CSS gradients with similar hue spans:

```regex
linear-gradient\([^)]*#[6-9a-f][0-9a-f]{2}[0-9a-f]{2}ff[^)]*#[0-9a-f]{2}[8-9a-f][0-9a-f]{2}ff[^)]*\)
```

**Better alternative**: A single restrained accent color (one of: Emerald, Electric Blue, Deep Rose, Amber) against neutrals. Save gradients for narrow hue windows (30-60 degrees apart) at low saturation, used as accents rather than canvas.

**Severity**: High
**Mode**: brand-only

**Example bad**:

```html
<section class="bg-gradient-to-r from-purple-500 to-blue-500 text-white">
  <h1>Build something amazing</h1>
</section>
```

**Example good**:

```html
<section class="bg-zinc-950 text-zinc-50">
  <h1 class="text-emerald-400">Build something amazing</h1>
</section>
```

---

#### 2. Pure black `#000000` for ink

**Why it's bad**: Pure black creates harsh edges on screens and reads as a flat default rather than a chosen color. Pure black on white has too much contrast and causes visual vibration on glossy displays. Off-black (zinc-950, charcoal) reads as deliberate and easier on the eye.

**How to detect**:

```regex
(?:color|background|fill|stroke|border|--[a-z-]+):\s*#000000?(?![0-9a-f])
```

```regex
\b(?:text|bg|border|fill|stroke)-black\b
```

Also flag the Tailwind `text-black` utility when not paired with a justification.

**Better alternative**: Use `#0a0a0a`, `#111111`, or Tailwind's `zinc-950` (`#09090b`) / `neutral-950` (`#0a0a0a`). The shift is invisible to most users but reads as more considered to designers.

**Severity**: Medium
**Mode**: both

**Example bad**:

```css
body { color: #000; background: #fff; }
```

**Example good**:

```css
body { color: #09090b; background: #fafaf8; }
```

---

#### 3. Pure white `#FFFFFF` canvas on premium marketing

**Why it's bad**: Pure white reads as "default" — the value the editor shipped with, not a value that was chosen. On premium marketing surfaces, a warm off-white in the `#FAFAF8` to `#F7F6F3` range carries the same airy feel without the unintentional-looking sterility.

**How to detect**:

```regex
(?:background|color|fill|--[a-z-]+):\s*(?:#ffffff?|#fff|white)(?![0-9a-f])
```

```regex
\bbg-white\b
```

In marketing / landing surfaces (files under `/marketing`, `/landing`, `/website`, `/(home|hero|brand)`), flag every occurrence.

**Better alternative**: Warm off-white — `#FAFAF8`, `#F7F6F3`, `#F5F4F0`. Adjust toward the brand's temperature.

**Severity**: Medium
**Mode**: brand-only

**Example bad**:

```html
<body class="bg-white text-black">
```

**Example good**:

```html
<body class="bg-[#FAFAF8] text-zinc-950">
```

---

#### 4. Default shadcn slate palette unmodified

**Why it's bad**: The default shadcn token set — slate-50 through slate-950 mapped onto the standard component primitives — is a known fingerprint. Anyone who has built one shadcn app recognizes the look within two seconds. Customization is required.

**How to detect**: Look for the unmodified token names in CSS / Tailwind config:

```regex
--background:\s*0\s+0%\s+100%;\s*\n\s*--foreground:\s*222\.2\s+84%\s+4\.9%;
```

Or detect the default `globals.css` from init with no token modification:

```regex
--primary:\s*222\.2\s+47\.4%\s+11\.2%;\s*\n\s*--primary-foreground:\s*210\s+40%\s+98%;
```

**Better alternative**: Customize the token palette at project init. Swap slate for zinc or a custom neutral. Adjust primary to a brand-specific hue. Adjust radii from the default `0.5rem` to something deliberate (typically `0.625rem` or `0.75rem` for modern feel).

**Severity**: High
**Mode**: both

**Example bad**:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --radius: 0.5rem;
}
```

**Example good**:

```css
:root {
  --background: 40 12% 96%;
  --foreground: 240 10% 8%;
  --primary: 158 64% 42%;
  --radius: 0.75rem;
}
```

---

#### 5. Three-stop rainbow gradient

**Why it's bad**: Three-stop gradients with broad hue ranges (pink-purple-blue, orange-pink-purple, blue-cyan-green) read as decorative noise. The eye can't parse them as intentional color choices — they look like color test panels.

**How to detect**:

```regex
linear-gradient\([^)]*,[^)]*,[^)]*,[^)]*\)
```

(Three or more comma-separated color stops inside the gradient.)

```regex
bg-gradient-to-[a-z]+\s+from-[a-z]+-[0-9]+\s+via-[a-z]+-[0-9]+\s+to-[a-z]+-[0-9]+
```

Then check the hue distance: if `from` and `to` are more than 60 degrees apart in hue, flag.

**Better alternative**: Two-stop gradients only. Keep hue spread under 60 degrees (analogous colors). Keep saturation modest (under 60%). Use gradients as accents, not canvas.

**Severity**: Medium
**Mode**: brand-only

**Example bad**:

```html
<div class="bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500">
```

**Example good**:

```html
<div class="bg-gradient-to-r from-emerald-600 to-teal-500">
```

---

### Typography

#### 6. Inter as the brand display face

**Why it's bad**: Inter is a strong body face — its hinting, x-height, and metrics are tuned for screen body copy. As a display face on a brand surface, it reads as "the default font for shipping a startup landing page from 2022." Every other product is using it; using it for display gives up the chance to have a typographic identity.

**Inter as body type is fine.** Inter as the display face is the violation.

**How to detect**: Search for Inter applied to `h1`, `h2`, `h3`, or `.display` classes:

```regex
(?:h1|h2|h3|\.display|\.hero|\.headline)[^{]*\{[^}]*font-family:[^;]*Inter
```

Also flag `font-family` declarations on display classes:

```regex
font-(?:display|hero|headline|title)[^:]*:[^;]*Inter
```

Also flag Tailwind's `font-sans` declaration in tailwind.config when it points only to Inter and is used on display elements.

**Better alternative**: A distinctive display face — Geist, Satoshi, Cabinet Grotesk, General Sans, Outfit, Suisse, or a brand-specific variable sans. Pair with Inter (or a workhorse sans) for body.

**Severity**: High
**Mode**: brand-only

**Example bad**:

```css
h1, h2, h3 { font-family: Inter, sans-serif; }
```

**Example good**:

```css
h1, h2, h3 { font-family: 'Geist', 'Satoshi', sans-serif; }
body { font-family: 'Inter', sans-serif; }
```

---

#### 7. Title Case Headlines

**Why it's bad**: Title case reads as advertising copy from the previous decade. Sentence case (only the first word capitalized) reads as modern, editorial, and confident. Every premium product launched in the last five years uses sentence case.

**How to detect**:

```regex
<h[1-3][^>]*>\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,}\s*<\/h[1-3]>
```

(Three or more capitalized words in a row inside a heading.)

Allow exceptions for proper nouns, product names, and acronyms. The detector should flag the line; a human or a downstream check decides if any of the words are proper nouns.

**Better alternative**: Sentence case. Only the first word and proper nouns capitalized.

**Severity**: High
**Mode**: brand-only

**Example bad**:

```html
<h1>Build Beautiful Products Faster</h1>
<h2>The Best Way To Manage Your Team</h2>
```

**Example good**:

```html
<h1>Build beautiful products faster</h1>
<h2>The best way to manage your team</h2>
```

---

#### 8. All-caps headlines at >14px

**Why it's bad**: All-caps at display sizes is hard to read, reads as shouting, and is a fingerprint of automated layout generators. All-caps belongs to eyebrow labels at 10-13px with tracked spacing.

**How to detect**:

```regex
text-transform:\s*uppercase[^}]*font-size:\s*(?:1[5-9]|[2-9][0-9])px
```

```regex
\.(?:display|hero|headline|h1|h2|h3)[^{]*\{[^}]*text-transform:\s*uppercase
```

For Tailwind:

```regex
uppercase[^"']*(?:text-(?:base|lg|xl|2xl|3xl|4xl|5xl|6xl|7xl|8xl|9xl))
```

**Better alternative**: Sentence case at display sizes; reserve uppercase for eyebrow labels at 10-13px with `letter-spacing: 0.05em` to `0.1em`.

**Severity**: Medium
**Mode**: both

**Example bad**:

```html
<h1 style="text-transform: uppercase; font-size: 48px">Welcome</h1>
```

**Example good**:

```html
<p class="text-xs uppercase tracking-wider text-zinc-500">Welcome</p>
<h1 class="text-5xl">Build something better</h1>
```

---

#### 9. Serif on dashboards / admin / app surfaces

**Why it's bad**: Serif faces have higher visual texture and lower screen-reading legibility at small sizes. They belong on editorial, marketing, and brand surfaces — never on data-dense product UI. Serif in a dashboard reads as "an editor styled a database admin like a magazine."

**How to detect**: Find serif font-family declarations in files matching dashboard / admin / app paths:

```regex
font-family:\s*(?:'[^']*serif[^']*'|"[^"]*serif[^"]*"|[a-zA-Z\s]+\s+serif)
```

In files matching: `/admin`, `/dashboard`, `/app`, `/console`, `/panel`, `/settings`, `/account`, `/(table|grid|list)`.

Also flag Tailwind `font-serif` utility used inside those file paths.

**Better alternative**: Sans only on dashboards and admin surfaces. Pair display and body sans (Geist + Geist Mono, Satoshi + JetBrains Mono, IBM Plex Sans + IBM Plex Mono).

**Severity**: High
**Mode**: product-only

**Example bad**:

```html
<!-- /admin/users.html -->
<body class="font-serif">
  <h1>User Management</h1>
</body>
```

**Example good**:

```html
<!-- /admin/users.html -->
<body class="font-sans">
  <h1>User management</h1>
</body>
```

---

#### 10. Display weight set to bold (700+)

**Why it's bad**: Modern display type carries its weight through tracking, size, and contrast — not through bold weight. Display set to 700 or heavier reads as a default editor setting rather than a typographic decision. The premium look uses medium (500) or semibold (600) at large sizes.

**How to detect**:

```regex
\.(?:display|hero|headline|h1|h2)[^{]*\{[^}]*font-weight:\s*(?:700|800|900|bold)
```

Tailwind:

```regex
(?:text-(?:5xl|6xl|7xl|8xl|9xl)[^"']*font-(?:bold|extrabold|black))
```

**Better alternative**: Display at weight 500 (medium) or 600 (semibold). Reserve 700+ for utility labels and ultra-compact UI elements.

**Severity**: Medium
**Mode**: brand-only

**Example bad**:

```html
<h1 class="text-7xl font-bold">Build something great</h1>
```

**Example good**:

```html
<h1 class="text-7xl font-medium tracking-tight">Build something great</h1>
```

---

### Layout

#### 11. Three equal cards in a row ("feature row" cliché)

**Why it's bad**: Three equal cards with three icons, three short titles, three short paragraphs — this is the strongest layout fingerprint in AI-generated marketing surfaces. The generator reaches for it on every "features" prompt because it's the safest default. Users skim past it without registering content.

**How to detect**:

```regex
grid-cols-3[^"']*"[^"']*(?:\n[^<]*<div[^>]*class="[^"]*(?:card|feature)[^"]*"[^>]*>[\s\S]*?</div>\s*){3,3}
```

Or more practically: count children of `grid-cols-3` containers; if exactly three children share the same class signature, flag.

**Better alternative**: Asymmetric layouts. Bento grids. A row of 2-and-1, 1-and-3, 4 with one feature card spanning the width. Vary card sizes by content priority.

**Severity**: High
**Mode**: brand-only

**Example bad**:

```html
<div class="grid grid-cols-3 gap-8">
  <div class="card"><h3>Fast</h3><p>...</p></div>
  <div class="card"><h3>Secure</h3><p>...</p></div>
  <div class="card"><h3>Reliable</h3><p>...</p></div>
</div>
```

**Example good**:

```html
<div class="grid grid-cols-6 gap-8">
  <div class="col-span-4 card-large"><h3>Speed is the feature</h3><p>...</p></div>
  <div class="col-span-2 card-tall"><h3>Built-in security</h3><p>...</p></div>
  <div class="col-span-2 card-wide"><h3>Reliable by design</h3><p>...</p></div>
  <div class="col-span-4 card-wide"><h3>One bill, every team</h3><p>...</p></div>
</div>
```

---

#### 12. Centered hero with text over dark background image

**Why it's bad**: Centered headlines over dark photographs are the laziest hero composition. The generator picks this when it can't find a better layout. The text-image relationship is unclear (is the photo decoration or content?), readability is fragile (a brighter photo region kills contrast), and the composition wastes the photo's depth.

**How to detect**:

```regex
<(?:section|div)[^>]*class="[^"]*(?:hero|banner)[^"]*"[^>]*>[\s\S]{0,500}<h1[^>]*class="[^"]*text-center[^"]*"
```

Combined with a background image:

```regex
background-image:\s*url\([^)]*\.(?:jpg|jpeg|png|webp|avif)[^)]*\)
```

Or Tailwind: `bg-cover` with a centered h1 inside.

**Better alternative**: Left-aligned hero text with image either to the side, as an inline element, or as an asymmetric composition. Photo earns its own space rather than serving as backdrop.

**Severity**: Medium
**Mode**: brand-only

**Example bad**:

```html
<section class="hero bg-cover" style="background-image: url('/hero.jpg')">
  <h1 class="text-center text-white">Welcome</h1>
</section>
```

**Example good**:

```html
<section class="grid grid-cols-12 gap-8 items-center">
  <div class="col-span-7">
    <h1 class="text-6xl tracking-tight">A better way to ship</h1>
    <p class="mt-4 text-lg">Specific value proposition with named outcome.</p>
  </div>
  <div class="col-span-5">
    <img src="/hero.jpg" alt="Product team reviewing dashboard">
  </div>
</section>
```

---

#### 13. `h-screen` on mobile hero

**Why it's bad**: `h-screen` resolves to `100vh`. On iOS Safari, `100vh` includes the address bar even when it's visible — which means the hero is taller than the viewport while the bar is showing, then suddenly correct when it collapses. The result: a layout that jumps when the user scrolls, and a hero that's not actually full-height when they first land.

**How to detect**:

```regex
\bh-screen\b
```

For raw CSS:

```regex
height:\s*100vh\b
```

```regex
min-height:\s*100vh\b
```

Allow `100vh` only when paired with a fallback to `100dvh`.

**Better alternative**: Use `100dvh` (dynamic viewport height) which excludes the collapsing UI. Or `min-h-[100dvh]` in Tailwind. Provide a fallback to `100vh` for older browsers.

**Severity**: High
**Mode**: both

**Example bad**:

```html
<section class="hero h-screen">
```

**Example good**:

```html
<section class="hero min-h-[100vh] min-h-[100dvh]">
```

---

#### 14. Disable zoom in viewport meta

**Why it's bad**: Disabling user-scaling is a WCAG 2.1 failure (Success Criterion 1.4.4). Users with low vision rely on pinch-to-zoom to read content. Disabling it is treated by major accessibility scanners as an automatic fail and may also be a legal liability in markets with web accessibility laws.

**How to detect**:

```regex
<meta\s+name="viewport"[^>]*user-scalable=no
```

```regex
<meta\s+name="viewport"[^>]*maximum-scale=1
```

```regex
<meta\s+name="viewport"[^>]*minimum-scale=1[^>]*maximum-scale=1
```

**Better alternative**: Allow zoom. The correct viewport meta is:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Severity**: Critical
**Mode**: both

**Example bad**:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no, maximum-scale=1">
```

**Example good**:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

---

#### 15. Fixed `100vh` on mobile container

**Why it's bad**: Same root cause as `h-screen` but applied to any container, not just hero. `100vh` on a sticky panel, sidebar, or full-page wrapper causes the same jump-on-scroll issue on iOS Safari. The fix is `100dvh`, which respects the dynamic viewport.

**How to detect**:

```regex
(?:min-)?height:\s*100vh\b
```

```regex
\b(?:min-h-\[100vh\]|h-\[100vh\])\b
```

Flag unless paired with a `100dvh` fallback or applied inside a media query that gates it to desktop.

**Better alternative**:

```css
.fullscreen-panel {
  min-height: 100vh; /* fallback */
  min-height: 100dvh;
}
```

Or Tailwind: `min-h-[100vh] min-h-[100dvh]`.

**Severity**: Medium
**Mode**: both

**Example bad**:

```css
.sidebar { height: 100vh; }
```

**Example good**:

```css
.sidebar {
  height: 100vh;
  height: 100dvh;
}
```

---

### Content

#### 16. "Click here" / "Learn more" / "Get started"

**Why it's bad**: Generic CTAs tell the user nothing about what's on the other side of the click. They also rank poorly in screen readers (the user hears "Link: click here" with no context) and SEO scanners (anchor text is part of the page's link graph). Every CTA should describe the destination or action.

**How to detect**:

```regex
>(?:Click here|Learn more|Get started|Read more|Find out more|See more|View more)<
```

Also flag bare `<a>` text inside buttons:

```regex
<button[^>]*>(?:Click here|Learn more|Get started)<\/button>
```

**Better alternative**: Describe the destination or action specifically. "Read the deployment guide." "See pricing for teams." "Start a 14-day trial." "Open dashboard."

**Severity**: High
**Mode**: both

**Example bad**:

```html
<a href="/pricing">Click here</a>
<button>Get started</button>
<a href="/docs">Learn more</a>
```

**Example good**:

```html
<a href="/pricing">See pricing for teams</a>
<button>Start a 14-day trial</button>
<a href="/docs">Read the deployment guide</a>
```

---

#### 17. Generic placeholder names

**Why it's bad**: "John Doe" / "Jane Doe" / "Sarah Chan" / "John Smith" are content slop fingerprints. They signal to the reader (and to anyone reviewing the work) that nobody actually thought about who would be using the product. Real names — even placeholder real names that fit the product's market — make the surface read as considered.

**How to detect**:

```regex
\b(?:John Doe|Jane Doe|Sarah Chan|John Smith|Jane Smith|Test User|Demo User)\b
```

Also flag the email patterns:

```regex
\b(?:john\.doe|jane\.doe|test\.user)@(?:example\.com|test\.com|demo\.com)\b
```

**Better alternative**: Use names that fit the product's target market. For a B2B SaaS aimed at startup founders: "Maya Iqbal," "Adam Levin," "Wen Zhang." For a regional product: names that reflect the region. Avoid the obviously-fictional patterns.

**Severity**: Medium
**Mode**: both

**Example bad**:

```jsx
const exampleUser = { name: 'John Doe', email: 'john.doe@example.com' };
```

**Example good**:

```jsx
const exampleUser = { name: 'Maya Iqbal', email: 'maya@northwind.co' };
```

---

#### 18. Fake brand names

**Why it's bad**: "Acme," "Nexus," "SmartFlow," "Zenith," "Stellar" — these are the canonical "fake startup names" that have appeared in every tutorial, every starter template, every screenshot from a content farm. The reader has seen them a thousand times. They register as "this product hasn't done its research."

**How to detect**:

```regex
\b(?:Acme|Acme\s+Corp|Acme\s+Inc|Nexus|SmartFlow|Zenith|Stellar|Lorem|Ipsum|Globex|Initech|Cyberdyne)\b
```

**Better alternative**: Use real customer names where available. Where unavailable, use names that sound like they could be real products in the target market — short, distinctive, not generic-tech-vocabulary.

**Severity**: Medium
**Mode**: brand-only

**Example bad**:

```html
<blockquote>"Game-changing." — Sarah Chan, CTO at Acme Corp</blockquote>
```

**Example good**:

```html
<blockquote>"We shipped three weeks faster on the migration alone." — Maya Iqbal, Engineering Manager at Northwind</blockquote>
```

---

#### 19. Round-number stats

**Why it's bad**: "99.99% uptime," "99.9% guaranteed," "100% money-back," "10x faster" — round-number statistics read as marketing fluff because real measurements rarely produce round numbers. Specific, organic numbers (74%, 3.2x, 18 days) signal that real measurement was done.

**How to detect**:

```regex
\b(?:99\.99%|99\.9%|99%|100%\s+guarantee|10x\s+(?:faster|better|more))\b
```

```regex
\b(?:10|20|25|50|100|1000|10000)x\s+(?:faster|better|more|easier)\b
```

**Better alternative**: Use specific, measured numbers. "99.94% uptime over the last 12 months." "3.7x faster median page load." "Cut onboarding from 11 days to 4."

**Severity**: Medium
**Mode**: brand-only

**Example bad**:

```html
<p>99.99% uptime guaranteed. 10x faster than the competition.</p>
```

**Example good**:

```html
<p>99.94% uptime measured across 12 regions, May 2025-May 2026. Median page load: 320ms.</p>
```

---

#### 20. Filler marketing verbs

**Why it's bad**: "Elevate your workflow." "Seamless integration." "Unleash productivity." "Next-Gen platform." "Revolutionize your business." "Empower your team." These verbs are the load-bearing pillars of marketing slop. They say nothing. They evaluate to nothing. They are the words a generator reaches for when it has no specific claim to make.

**How to detect**:

```regex
\b(?:Elevate|Seamless|Unleash|Next-Gen|Next\s+Gen|Revolutionize|Empower|Streamline|Transform\s+your|Unlock\s+(?:your\s+)?potential|Supercharge|Maximize)\b
```

In headlines and subheads (h1, h2, h3, hero subtitles), flag every occurrence. In body copy, flag and allow with a single warning.

**Better alternative**: Make a specific claim. Replace the filler verb with what the product actually does.

| Bad | Good |
|---|---|
| Elevate your workflow | Ship features 3 days sooner |
| Seamless integration | Set up in 4 minutes; no SDK required |
| Unleash productivity | Cut your standup time in half |
| Next-Gen platform | One canvas; all your docs |
| Revolutionize your business | Replace 4 tools with 1 |
| Empower your team | Read receipts that don't lie |

**Severity**: High
**Mode**: brand-only

**Example bad**:

```html
<h1>Elevate your workflow with our next-gen platform.</h1>
<h2>Seamlessly transform your business and empower your team.</h2>
```

**Example good**:

```html
<h1>Ship faster, with less back-and-forth.</h1>
<h2>One workspace replaces four tools — and the price drops by half.</h2>
```

---

### Components

#### 21. Emoji as icon

**Why it's bad**: Emojis are inconsistent across platforms (every OS renders them differently), they don't take a brand color, they don't scale cleanly with type, and they signal informality in a product context. Inline SVG (Lucide, Feather, Phosphor) gives consistent rendering, brand-color inheritance via `currentColor`, and crisp scaling at any size.

**How to detect**: Match emoji Unicode ranges inside button or anchor or icon-slot contexts:

```regex
<(?:button|a)[^>]*>[^<]*[\u{1F300}-\u{1F9FF}\u{2600}-\u{27BF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}][^<]*<
```

JavaScript regex with `u` flag:

```js
const emojiInButton = /<(?:button|a)[^>]*>[^<]*[\u{1F300}-\u{1F9FF}\u{2600}-\u{27BF}\u{1F600}-\u{1F6FF}\u{1F680}-\u{1F6FF}][^<]*</gu;
```

Also flag in icon-class contexts:

```regex
class="[^"]*(?:icon|emoji)[^"]*"[^>]*>[\u{1F300}-\u{1F9FF}]
```

**Better alternative**: Inline SVG icons from a curated set (Lucide, Feather, Phosphor, Heroicons) at 1.5px or 2px stroke, sized to the type baseline, colored via `currentColor`.

**Severity**: High
**Mode**: both

**Example bad**:

```html
<button>Star this</button>
```

(With an emoji character as a prefix or replacement for the icon.)

**Example good**:

```html
<button>
  <svg width="16" height="16" stroke="currentColor" stroke-width="1.5" fill="none" viewBox="0 0 24 24">
    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />
  </svg>
  Star this
</button>
```

---

#### 22. Icon-only button without `aria-label`

**Why it's bad**: Icon-only buttons have no accessible name. A screen reader user hears "button" with no further information. The button is unusable for them — they have to guess, or skip it entirely. WCAG 2.1 Success Criterion 4.1.2 (Name, Role, Value) requires every interactive element to have an accessible name.

**How to detect**:

```regex
<button(?![^>]*aria-label)(?![^>]*aria-labelledby)[^>]*>\s*<svg[^>]*>[^<]*<\/svg>\s*<\/button>
```

(A `<button>` whose only child is an `<svg>`, with no `aria-label` or `aria-labelledby` attribute.)

Also catch wrapped versions where the SVG is the only meaningful child:

```regex
<button(?![^>]*aria-label)[^>]*>\s*(?:<span[^>]*>)?\s*<svg[^>]*>[\s\S]*?<\/svg>\s*(?:<\/span>)?\s*<\/button>
```

**Better alternative**: Add an `aria-label` describing what the button does.

**Severity**: Critical
**Mode**: both

**Example bad**:

```html
<button>
  <svg>...</svg>
</button>
```

**Example good**:

```html
<button aria-label="Close dialog">
  <svg>...</svg>
</button>
```

---

#### 23. `<div onClick>` without role and tabindex

**Why it's bad**: A `<div>` with a click handler but no `role="button"` and no `tabindex="0"` is unreachable by keyboard, invisible to assistive tech, and missing the focus-visible affordance that lets keyboard users see where they are. The user clicks with a mouse and nothing else can interact with it. This is a critical accessibility failure and a SEO signal that the page is not built with semantic HTML.

**How to detect**:

```regex
<div(?![^>]*role=)(?![^>]*tabindex=)[^>]*onClick=
```

JSX in React:

```regex
<div(?![^>]*role=)(?![^>]*tabIndex=)[^>]*onClick=
```

**Better alternative**: Use `<button>`. If you absolutely cannot (you're inside a structure that semantically rejects buttons), add `role="button"`, `tabindex="0"`, and a keyboard handler that fires the same action on `Enter` and `Space`.

**Severity**: Critical
**Mode**: both

**Example bad**:

```jsx
<div onClick={handleClick} className="card">
  Click me
</div>
```

**Example good**:

```jsx
<button onClick={handleClick} className="card">
  Click me
</button>
```

Or if a button is impossible:

```jsx
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); handleClick(); }}}
  className="card"
>
  Click me
</div>
```

---

#### 24. Anchor without `href` used as button

**Why it's bad**: `<a>` without `href` is not focusable by default, has no role announcement, and looks like a link to a sighted user (who expects link behavior — middle-click to new tab, drag to bookmark) while behaving like a button. Misleading on every axis.

**How to detect**:

```regex
<a(?![^>]*href=)[^>]*(?:class="[^"]*(?:btn|button)[^"]*"|onClick=)
```

```regex
<a(?![^>]*href=)[^>]*role="button"
```

**Better alternative**: Use `<button>`. If the click should navigate, give the anchor an `href`. If the click should perform an action without navigation, it's a button.

**Severity**: High
**Mode**: both

**Example bad**:

```html
<a class="btn-primary" onclick="submitForm()">Submit</a>
```

**Example good**:

```html
<button class="btn-primary" onclick="submitForm()">Submit</button>
```

---

#### 25. Placeholder used as label

**Why it's bad**: The `placeholder` attribute is not a label. It vanishes when the user types. It has poor contrast on most browsers (gray-400 by default). Screen readers may or may not announce it depending on the input state. Forms that rely on placeholder text as the only label are unusable for screen reader users and confusing for everyone else.

**How to detect**: An input with a `placeholder` attribute and no associated `<label>`:

```regex
<input[^>]*placeholder=[^>]*>(?![^<]*<label)
```

A more thorough check: the input has an `id`, but no `<label for="that-id">` anywhere in the document. This requires a parse, not a regex, but the regex above catches the common case.

Also flag explicitly:

```regex
<input[^>]*placeholder=[^>]*aria-label=
```

(Aria-label is better than nothing, but a visible `<label>` is better than aria-label.)

**Better alternative**: A `<label>` tied to the input via `for` / `id` or by wrapping the input. Placeholder text describes what to type; the label describes what the field is for.

**Severity**: High
**Mode**: both

**Example bad**:

```html
<input type="email" placeholder="Email">
```

**Example good**:

```html
<label for="email">Email address</label>
<input id="email" type="email" placeholder="you@company.com">
```

---

### Interaction

#### 26. Animating `width`, `height`, `top`, `left`

**Why it's bad**: These properties trigger layout. Layout cascades through the DOM tree, recalculating positions for every descendant on every animation frame. On mid-range hardware, this drops frames immediately. The animation reads as choppy and slow. Even on high-end hardware, the main-thread cost is real and starves other work.

**How to detect**:

```regex
(?:transition|animation)[^;]*:[^;]*(?:width|height|top|left|right|bottom|margin|padding)
```

```regex
@keyframes[^{]*\{[^}]*(?:width|height|top|left)\s*:
```

For Framer Motion / motion libraries:

```regex
animate=\{[^}]*(?:width|height|top|left|right|bottom)\s*:
```

**Better alternative**: Animate `transform` and `opacity` only. Use `scaleX` / `scaleY` instead of `width` / `height`. Use `translateX` / `translateY` instead of `top` / `left`.

**Severity**: High
**Mode**: both

**Example bad**:

```css
.menu {
  transition: width 200ms, height 200ms;
}
.menu.open {
  width: 320px;
  height: 480px;
}
```

**Example good**:

```css
.menu {
  transform-origin: top left;
  transform: scale(0);
  transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
}
.menu.open {
  transform: scale(1);
}
```

---

#### 27. `outline: none` without focus-visible replacement

**Why it's bad**: Removing the default focus outline without providing a replacement strips keyboard users of the ability to know where they are. WCAG 2.1 Success Criterion 2.4.7 (Focus Visible) requires a visible focus indicator. This is a critical accessibility failure that also degrades the experience for power users navigating via Tab.

**How to detect**:

```regex
outline:\s*(?:none|0)(?![^}]*:focus-visible)
```

A more reliable form: search for `outline: none` and then check whether the same selector (or a `:focus-visible` pseudo-class on that selector) has a replacement.

Selectors to check the replacement on:

```regex
:focus-visible\s*\{[^}]*(?:outline|box-shadow|ring|border):
```

**Better alternative**: Replace the default outline with a focus ring that fits the design system. Use `:focus-visible` so the ring shows on keyboard navigation but not on mouse-click.

**Severity**: Critical
**Mode**: both

**Example bad**:

```css
button { outline: none; }
```

**Example good**:

```css
button:focus { outline: none; }
button:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}
```

---

#### 28. `cursor: pointer` on non-interactive elements

**Why it's bad**: `cursor: pointer` tells the user "this is clickable." If the element has no click handler, no `role="button"`, no anchor, and no form action, the cursor is lying. Users hover, expect feedback, and get nothing. Bad signal-to-noise on interactivity is one of the strongest "this product feels broken" tells.

**How to detect**:

```regex
<(?:div|span|p|li|article|section)(?![^>]*onClick=)(?![^>]*onclick=)(?![^>]*role="button")(?![^>]*role='button')[^>]*style="[^"]*cursor:\s*pointer
```

For CSS:

```regex
(?:div|span|p|li|article|section)[^{]*\{[^}]*cursor:\s*pointer
```

(Naive — also requires checking the same selector or descendants for actual click handlers. The regex catches the obvious case.)

**Better alternative**: Use `cursor: pointer` only on elements that respond to a click. If the element shouldn't be clickable, drop the cursor.

**Severity**: Medium
**Mode**: both

**Example bad**:

```css
.feature-label { cursor: pointer; }
```

(Where the element has no click handler.)

**Example good**:

```css
button, a, [role="button"] { cursor: pointer; }
.feature-label { cursor: default; }
```

---

### Performance

#### 29. Missing `alt` attribute on `<img>`

**Why it's bad**: Three failures at once. Screen readers cannot describe the image to their user — accessibility failure (WCAG 2.1 SC 1.1.1). Search engines cannot index the image — SEO failure. When the image fails to load, the user sees a broken-image icon with no context — UX failure.

**How to detect**:

```regex
<img(?![^>]*\balt=)[^>]*>
```

JSX:

```regex
<img(?![^>]*alt=)[^>]*\/>
```

Allow `alt=""` for purely decorative images (the empty alt signals "this image is intentionally decorative; don't announce it").

**Better alternative**: Every `<img>` has an `alt`. Decorative images get `alt=""`. Informative images get a description that conveys what a screen reader user would need to know.

**Severity**: Critical
**Mode**: both

**Example bad**:

```html
<img src="/hero.jpg">
<img src="/product-photo.png">
```

**Example good**:

```html
<img src="/hero.jpg" alt="Engineering team reviewing a deployment dashboard at sunset">
<img src="/product-photo.png" alt="Close-up of the analytics summary view with three filter chips visible">
```

For decorative:

```html
<img src="/decorative-grain.png" alt="" role="presentation">
```

---

#### 30. Missing `width` and `height` attributes on `<img>`

**Why it's bad**: Without explicit width and height, the browser cannot reserve space for the image before it loads. When the image finally arrives, it pushes content around, causing layout shift (CLS). High CLS scores are a Core Web Vitals failure and a direct SEO ranking penalty. They also visually annoy the user — text they were reading jumps as images load below.

**How to detect**:

```regex
<img(?![^>]*\bwidth=)[^>]*>
```

```regex
<img(?![^>]*\bheight=)[^>]*>
```

Both must be present. Flag any `<img>` missing either.

In Next.js / React frameworks: prefer the framework's image component (`<Image>` in Next.js), which enforces dimensions; flag bare `<img>` in framework files.

**Better alternative**: Always include `width` and `height` attributes on `<img>`. The values can be set as the natural aspect ratio (the browser will scale via CSS); the goal is to reserve the layout slot before the image loads.

**Severity**: High
**Mode**: both

**Example bad**:

```html
<img src="/hero.jpg" alt="Engineering team">
```

**Example good**:

```html
<img src="/hero.jpg" alt="Engineering team" width="1200" height="800" loading="lazy" decoding="async">
```

In Next.js:

```jsx
import Image from 'next/image';
<Image src="/hero.jpg" alt="Engineering team" width={1200} height={800} />
```

---

## Quick reference — all 30 in a single table

| # | Rule | Severity | Mode | Detect (short regex / selector) |
|---|---|---|---|---|
| 1 | Default purple-to-blue AI gradient | High | brand-only | `bg-gradient-to-[a-z]+\s+from-(purple\|violet\|fuchsia\|indigo)-...\s+to-(blue\|sky\|cyan)-...` |
| 2 | Pure black `#000000` ink | Medium | both | `(?:color\|background\|fill):\s*#000000?\b` or `\btext-black\b` |
| 3 | Pure white `#FFFFFF` canvas (marketing) | Medium | brand-only | `(?:background\|color):\s*(?:#ffffff?\|#fff\|white)\b` or `\bbg-white\b` |
| 4 | Default shadcn slate palette unmodified | High | both | Default token block in `:root` matching the init defaults |
| 5 | Three-stop rainbow gradient | Medium | brand-only | `linear-gradient` with 3+ stops or `from-... via-... to-...` |
| 6 | Inter as the brand display face | High | brand-only | `font-family` on h1/h2/h3/`.display` containing `Inter` |
| 7 | Title Case Headlines | High | brand-only | `<h[1-3][^>]*>\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){2,}` |
| 8 | All-caps headlines at >14px | Medium | both | `text-transform:\s*uppercase` + `font-size > 14px` |
| 9 | Serif on dashboards / admin | High | product-only | `font-family.*serif` in `/admin`, `/dashboard`, `/app`, `/console` |
| 10 | Display weight set to bold (700+) | Medium | brand-only | `font-weight:\s*(700\|800\|900\|bold)` on `.display` / display headings |
| 11 | Three equal cards in a row | High | brand-only | `grid-cols-3` with three children of identical class signature |
| 12 | Centered hero over dark background image | Medium | brand-only | `.hero` + `text-center` h1 + `bg-cover` with image |
| 13 | `h-screen` on mobile hero | High | both | `\bh-screen\b` without `100dvh` fallback |
| 14 | Disabled zoom in viewport meta | Critical | both | `<meta name="viewport"[^>]*(user-scalable=no\|maximum-scale=1)` |
| 15 | Fixed `100vh` on mobile container | Medium | both | `(?:min-)?height:\s*100vh` without `100dvh` fallback |
| 16 | "Click here" / "Learn more" / "Get started" | High | both | `>(?:Click here\|Learn more\|Get started\|Read more)<` |
| 17 | Generic placeholder names | Medium | both | `\b(John Doe\|Jane Doe\|Sarah Chan\|John Smith)\b` |
| 18 | Fake brand names | Medium | brand-only | `\b(Acme\|Nexus\|SmartFlow\|Zenith\|Stellar\|Globex\|Initech)\b` |
| 19 | Round-number stats | Medium | brand-only | `\b(99\.99%\|99\.9%\|100%\s+guarantee\|10x\s+(faster\|better))\b` |
| 20 | Filler marketing verbs | High | brand-only | `\b(Elevate\|Seamless\|Unleash\|Next-Gen\|Revolutionize\|Empower)\b` |
| 21 | Emoji as icon | High | both | Emoji Unicode ranges (`U+1F300-1F9FF`, etc.) inside `<button>` / `<a>` |
| 22 | Icon-only button without aria-label | Critical | both | `<button(?![^>]*aria-label)[^>]*>\s*<svg` |
| 23 | `<div onClick>` without role / tabindex | Critical | both | `<div(?![^>]*role=)(?![^>]*tabindex=)[^>]*onClick=` |
| 24 | Anchor without href used as button | High | both | `<a(?![^>]*href=)[^>]*(?:class="[^"]*btn\|onClick=)` |
| 25 | Placeholder used as label | High | both | `<input[^>]*placeholder=` with no `<label for=...>` sibling |
| 26 | Animating width / height / top / left | High | both | `transition\|animation:.*(width\|height\|top\|left)` |
| 27 | `outline: none` without focus-visible replacement | Critical | both | `outline:\s*(none\|0)` without sibling `:focus-visible` |
| 28 | `cursor: pointer` on non-interactive elements | Medium | both | `cursor:\s*pointer` on `<div>` / `<span>` without click handler |
| 29 | Missing `alt` attribute on `<img>` | Critical | both | `<img(?![^>]*\balt=)[^>]*>` |
| 30 | Missing `width` + `height` on `<img>` | High | both | `<img(?![^>]*\bwidth=)` or `<img(?![^>]*\bheight=)` |

---

## How to wire this into CI

The `/ux-lint` command (v1.5+) reads this file directly and produces a report. For a custom CI integration:

1. Parse the rules into JSON: `[{ id, name, severity, mode, regex, message, fix }, ...]`.
2. Walk the project tree. For each file, classify as brand or product based on path prefixes (`/marketing`, `/landing`, `/app`, `/admin`).
3. Apply each rule's regex with the appropriate file scope.
4. Emit findings in SARIF or GitHub Annotations format.
5. Fail the build on any Critical finding; warn on High; report-only on Medium and Cosmetic.

A reasonable budget: zero Critical, zero High, fewer than 5 Medium per surface.

---

## Severity summary

- **Critical (5 rules)**: 14, 22, 23, 27, 29. Each ships with a Web Content Accessibility Guidelines failure or a security / SEO regression. Block ship.
- **High (12 rules)**: 1, 4, 6, 7, 9, 11, 13, 16, 20, 24, 25, 26, 30. Each is an obvious AI fingerprint or a degraded user experience. Fix before claiming "done."
- **Medium (12 rules)**: 2, 3, 5, 8, 10, 12, 15, 17, 18, 19, 28. Quality polish. Look broken to designers; the user notices the cumulative effect.
- **Cosmetic (0 rules)**: nothing in this set is pure-cosmetic; the severity distribution intentionally leans toward functional.

---

## Related

- see `styles/anti-slop.md` for aesthetic AI-fingerprints (less lintable, more taste-driven; the visual-pattern catalogue)
- see `foundations/accessibility.md` for WCAG-driven rules including the full focus-visible specification, color-contrast thresholds, and screen-reader requirements
- see `foundations/seo.md` for SEO-driven rules including Core Web Vitals, image attributes, and semantic-HTML requirements
- see `foundations/motion-principles.md` for the deeper motion vocabulary (rule 26 here is the lintable subset of that file's full guidance)
- see `foundations/components.md` for the canonical button, link, input, and icon patterns these anti-patterns rule out
- the `/ux-lint` command (v1.5+) uses this file as its primary rule source; updates to this file are picked up on the next `/ux-lint` run
