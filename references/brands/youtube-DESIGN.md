# Design System Inspired by YouTube

## 1. Visual Theme & Atmosphere

YouTube's web interface is the most-trafficked video surface on the internet, and its design is engineered for one thing: get the user from "open page" to "playing a video" in as few visual moments as possible. The atmosphere is chrome-light, content-heavy, and unapologetically utilitarian. Every pixel that isn't a video thumbnail is a candidate for removal. The result is a grid-dominant interface: thumbnails as the hero, channel avatar as the second-tier hero, everything else collapsing into the negative space.

YouTube Red (#ff0000) — the signature chromatic asset — appears almost exclusively on the play-arrow logo, on the "Subscribe" button, and on live-now indicators. It is one of the most-restrained brand-red implementations on the web; the actual interface uses a near-monochrome ladder of grays in light mode and a similar ladder of dark gray-blacks in the system-preferred dark mode. The dark mode is, in fact, the default for an increasing share of users — and the system reads as more native to dark than light.

The typography commits to Roboto and Roboto Mono — Google's open-source Material face — at a small-but-readable 14–16px body across the interface. Thumbnails are 16:9, mostly user-uploaded, and the visual variety inside them carries 90% of the page's "atmosphere." The chrome around them is the quietest possible.

**Key Characteristics:**
- 16:9 thumbnail grid is the dominant visual unit — 4 to 5 columns at desktop, 2 at tablet, 1 at mobile
- YouTube Red (#ff0000) used only on the play-arrow logo and on Subscribe / live indicators
- Dark mode default for power users; light mode and dark mode are token-mirror twins
- Roboto family throughout — display, body, caption, captions-on-video
- Thumbnail title in 16px Roboto Medium, channel name in 14px Roboto Regular muted gray
- "Subscribe" red button is a 2px-radius solid rectangle — the only chromatic CTA on the page
- Hover on a thumbnail triggers a 2–3 second auto-preview (silent) — a signature interaction
- Pill-shaped category filter chips at the top of the homepage feed
- Hamburger drawer left-nav with channel subscriptions list — collapsible to icon-only

## 2. Color Palette & Roles

### Primary
- **YouTube Red** (`#ff0000`): The brand wordmark, the play-arrow icon, the "Subscribe" button, the live-indicator dot. Used scarcely on chrome and never on body text

### Surface & Background (Light Mode)
- **Canvas** (`#ffffff`): Page background
- **Hover Tint** (`#f2f2f2`): Thumbnail card hover background, button hover state
- **Subtle Surface** (`#f9f9f9`): Sidebar background, secondary panels
- **Hairline** (`#e5e5e5`): 1px borders, divider lines

### Surface & Background (Dark Mode)
- **Canvas** (`#0f0f0f`): Page background — near-pure black, slightly warmer than `#000`
- **Surface 1** (`#1f1f1f`): Card hover, button hover
- **Surface 2** (`#272727`): Elevated dialogs, dropdown menus
- **Hairline** (`#3d3d3d`): 1px borders in dark mode

### Neutrals & Text
- **Ink Light Mode** (`#0f0f0f`): Primary text on white
- **Ink Dark Mode** (`#f1f1f1`): Primary text on `#0f0f0f`
- **Muted Light** (`#606060`): Channel names, metadata (view counts, dates)
- **Muted Dark** (`#aaaaaa`): Same role in dark mode
- **Disabled** (`#909090`): Disabled button labels

### Semantic
- The interface largely avoids semantic colors — red doubles for both brand voltage and live indicators. Verified channel checkmark is a small gray glyph, not a saturated blue

## 3. Typography Rules

### Font Family
- **Display + Body**: `Roboto, sans-serif` — the open-source Google Material face. Used across the entire UI
- **Mono**: `Roboto Mono` — used inside the code-snippet panel of Creator Studio and in time-stamp displays

### Hierarchy
- **Channel page hero name** — 24px Roboto Medium, slight negative tracking
- **Video title (in player)** — 20px Roboto Medium, line-height 1.4
- **Video title (in thumbnail grid)** — 16px Roboto Medium, two-line clamp
- **Channel name (under thumbnail)** — 14px Roboto Regular, muted gray
- **Metadata** (view count, age) — 12px Roboto Regular, muted gray, dot-separated
- **Comment body** — 14px Roboto Regular, 1.4 line-height
- **Sidebar nav label** — 14px Roboto Medium

### Principles
- Type stays small relative to most marketing sites — the thumbnail is the hero, not the text
- Two-line clamp on video titles is universal; titles longer than that are truncated with ellipsis
- Weight ladder: 400 (Regular), 500 (Medium), 700 (Bold). 500 is the workhorse for titles and labels
- Tracking sits at 0 across the system — Roboto's defaults aren't adjusted

## 4. Layout & Spacing

The homepage feed is a 4-or-5-column grid of 16:9 thumbnails at desktop, with each column ~320px wide, 8px gap between thumbnails. Below each thumbnail is a 12px gap, then channel avatar (36px circle), title (16px Roboto Medium), and metadata stack. Total thumbnail card height ~280px.

The video watch page splits 67/33: video player + controls on the left at 1280×720, recommended-video sidebar on the right with smaller thumbnail tiles (320×180). Below the video, the description card and comment section stack vertically.

Section spacing is tight — 16–24px between major bands, far tighter than marketing sites. The interface is designed for skimming dozens of thumbnails per scroll, not for editorial reading.

## 5. Componentry Feel

- **Thumbnail card** — 16:9 image, slight 8px radius (subtle), title clamped to 2 lines, channel name muted, metadata row beneath
- **Subscribe button** — Solid red `#ff0000`, white text, 2–4px radius, 36px height — the only chromatic CTA in the chrome
- **Subscribe button (subscribed state)** — Inverts to neutral gray fill, "Subscribed" label with a bell icon
- **Like / Dislike pill** — Joint pill with a vertical divider, thumb icons + count, gray fill on dark mode, hover lifts to surface-1
- **Category filter chip** — Pill-shaped, 32px height, neutral gray fill, "active" state inverts to dark fill + light text
- **Comment thread** — Avatar 40px circle, author name + time, body text, like/reply row beneath
- **Sidebar nav item** — 40px row height, 24px icon + 14px label, hover background `#f2f2f2` (light) or `#1f1f1f` (dark)
- **Mini player** — When user scrolls past the video, the player shrinks to a 400×225 floating card pinned bottom-right
- **Live indicator** — Red dot + "LIVE" label in caps, overlay on thumbnail
- **Verification checkmark** — Small gray glyph beside channel name, never blue or chromatic

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use direct platform language ("Subscribe", "Like", "Share", "Save"). Quantify metadata (1.2M views, 6 days ago). Treat comment moderation messages neutrally ("This comment was held for review"). Use Material-style sentence-case for buttons.

**Don't.** Don't anthropomorphize the algorithm ("we picked this for you" reads off-brand). Don't use exclamation points in chrome. Don't translate platform verbs across locales — "Subscribe" stays consistent in localization tone.

## 7. Motion Vocabulary

YouTube's motion is restrained and functional. Thumbnail hover triggers a silent 2–3 second video preview (the signature interaction). The mini-player shrinks with a 200ms ease-out cubic-bezier transition when scrolling. The sidebar drawer slides in with 240ms ease. Like/dislike buttons have a subtle scale tick on click. The progress bar at the bottom of the player is a hairline red strip that fills smoothly as the video plays — the strip is the same `#ff0000` as the wordmark.

## 8. Anti-patterns to Avoid

- **Don't paint the entire interface red.** YouTube Red is scarce — wordmark, Subscribe, live indicator. Painting cards or hover states red breaks the brand
- **Don't add a secondary chromatic accent.** The system is monochrome + red. Adding blue, green, or amber accents reads as off-brand
- **Don't shadow the thumbnails.** Cards are flat — depth comes from the surface tint shift on hover, not from drop shadows
- **Don't bold the metadata.** Channel name and view count stay regular weight at muted gray
- **Don't break the 16:9 aspect ratio.** Vertical thumbnails (for Shorts) get their own component grammar; standard feed stays 16:9
- **Don't widen the "Subscribe" radius.** It stays at 2–4px, never pill — the rectilinear shape is part of the brand
- **Don't auto-play with sound.** The hover preview is silent. Audio-on autoplay is universally hated and never appears in the YouTube web chrome
