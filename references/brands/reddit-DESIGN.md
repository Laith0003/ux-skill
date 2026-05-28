# Design System Inspired by Reddit

## 1. Visual Theme & Atmosphere

Reddit's design is the community-feed grammar of the internet's largest message board, translated into a modern but unapologetically text-heavy UI. The atmosphere is community-first, nostalgic-of-bulletin-boards, and dark-mode-first. Where peer social platforms (Instagram, TikTok, X) lean into media-edge-to-edge feeds, Reddit leans into the title, the vote count, the comment count, and the community name — text-dominant, link-dominant, conversation-dominant.

Reddit Orange (#ff4500) is the brand's chromatic voltage. It appears on the wordmark, on the active state of the upvote arrow, on premium chrome (Reddit Gold awards), and in special-occasion illustrations. The orange is specific: not red, not amber, a saturated #ff4500. Replacing it with a more "modern" coral or rose is a recognition failure.

Snoo — the small white alien silhouette — is the brand character. Snoo appears as a prefix in the wordmark, in special-occasion illustrations (Snoo wearing a Santa hat, Snoo holding a Reddit Award), and as a subtle illustrated detail on premium chrome. Snoo's personality is "weird-internet-friendly" — the alien is doing whatever the community is doing.

The upvote / downvote arrow stack is the most-recognized voting UI on the internet. The arrows are a vertically-stacked up-and-down pair, sitting to the left of every post and comment. Click the up-arrow and it fills with Reddit Orange; click the down-arrow and it fills with a blue (#7193ff). The vote count between them updates in real time.

**Key Characteristics:**
- Reddit Orange (#ff4500) — chromatic voltage on wordmark, upvote active state, and premium chrome
- Snoo alien mascot — appears as wordmark prefix and special-occasion illustration
- Upvote / downvote arrow stack — the iconic voting UI
- Dark-mode default chrome (#0e1113 canvas) with full light-mode mirror
- IBM Plex Sans across chrome — the open-source IBM font family
- Dense list-view as default, card-view as alternative — both views well-developed
- Nested comment threads with left-indent lines

## 2. Color Palette & Roles

### Brand Voltage
- **Reddit Orange** (`#ff4500`): Upvote-active fill, wordmark color, premium chrome accent
- **Orange Hover** (`#cc3700`): Slightly deeper press state
- **Downvote Blue** (`#7193ff`): The downvote-active fill — a periwinkle blue, distinct from saturated brand blues

### Surface & Background (Dark Mode)
- **Canvas** (`#0e1113`): The dark-mode page background
- **Surface 1** (`#181c1f`): Card backgrounds in dark mode
- **Surface 2** (`#1a1a1b`): Hover state, elevated panels
- **Hairline** (`#2a3236`): 1px borders in dark mode

### Surface & Background (Light Mode)
- **Canvas** (`#ffffff`): Light-mode page background
- **Surface 1** (`#f6f7f8`): Card backgrounds
- **Surface 2** (`#e4e6eb`): Hover state
- **Hairline** (`#d3d6da`): Light-mode borders

### Neutrals & Text
- **Ink (dark)** (`#f2f4f5`): Primary text on dark mode
- **Ink (light)** (`#1c1c1c`): Primary text on light mode
- **Muted (dark)** (`#838f99`): Captions, metadata in dark mode
- **Muted (light)** (`#7a8082`): Captions in light mode

### Semantic
- **Award Gold** (`#ffd635`): Reddit Gold premium chrome
- **Link** (`#3aa0ff`): Inline body links (a softer blue distinct from downvote blue)

## 3. Typography Rules

### Font Family
- **Display + Body**: `IBM Plex Sans, system-ui, sans-serif` — the open-source IBM font, used across chrome
- **Mono**: `IBM Plex Mono` — used in code blocks and `/r/<subreddit>` references

### Hierarchy
- **Post title** — 18–22px IBM Plex Sans weight 600, line-height 1.3
- **Subreddit header** — 24–32px weight 700
- **Body / comment** — 14–16px weight 400, line-height 1.5
- **Vote count / metadata** — 12–13px weight 500, muted color
- **Button label** — 13–14px weight 600
- **Comment author** — 12px weight 600 with subtle "OP" badge if original poster

### Principles
- IBM Plex Sans's slightly geometric proportions read as "technical" — matches the message-board-internet aesthetic
- Weight 600 is the workhorse for headlines and labels
- Monospace `/r/<subreddit>` references are signature — never set them in proportional sans
- Body text intentionally smaller than peer platforms — Reddit users read densely

## 4. Layout & Spacing

The feed uses a 3-column desktop layout: left rail (subscribed subreddit list), center column (post feed, ~640px wide), right rail (subreddit info, rules, moderator list). The center column dominates.

Card padding is 12–16px internal. Card-to-card gap is 8px. List-view rows have ~64px tall posts with just the title, vote count, and metadata visible.

## 5. Componentry Feel

- **Post card (feed view)** — Dark or light surface, 12px radius, vote-arrow stack on the left, content (title, body preview, link card if external), action row (upvote/downvote, comment count, share, save) at the bottom
- **Post card (list view)** — Compact 64px tall row, just the title + vote count + comment count + metadata. No body preview
- **Upvote/downvote stack** — Vertical pair of arrow buttons with vote count between. Default state outlined; active state filled Reddit Orange (up) or Downvote Blue (down)
- **Comment thread** — Nested comment list with left-indent vertical lines indicating thread depth. Each comment has avatar, author, time, body, action row
- **Subreddit header** — Banner image, circular subreddit icon (often using Snoo variants), name, subscriber count, "Join" pill CTA
- **Premium award** — Small icon (silver, gold, platinum) attached to high-value posts/comments — uses gold gradient for the Gold award
- **Mascot illustration** — Snoo appears in special-occasion contexts (404 pages, holiday banners, achievement badges)

## 6. Voice / Microcopy Do's & Don'ts

**Do.** Use community-vernacular language ("Join the conversation", "TIL", "AMA"). Reference subreddits as `/r/<name>` and users as `/u/<name>`. Lead with the post title — that is the contract Reddit has with its user.

**Don't.** Don't sanitize the community vernacular. Don't replace `/r/` with `/community/` or `/u/` with `/user/` (each is recognizable shorthand). Don't translate Snoo to a generic robot. Don't bowdlerize moderator-flagged content beyond what the moderator chose.

## 7. Motion Vocabulary

The vote arrows are the brand's signature motion: on click, the arrow fills with orange (up) or blue (down), and the vote count tick-animates the change. Comment expand/collapse uses a 200ms ease. Mascot illustrations have idle animations in special-occasion banners (Snoo blinking, waving). Overall motion stays functional — no spring overshoots, no scroll-triggered card reveals.

## 8. Anti-patterns to Avoid

- **Don't replace Reddit Orange with a warmer red.** The specific #ff4500 is part of the recognition
- **Don't redesign the upvote/downvote arrows to a generic thumbs-up.** They are the most-recognized voting UI on the internet
- **Don't strip the Snoo mascot.** It is the brand character
- **Don't sanitize the dense list view.** Reddit's text-density is the brand
- **Don't replace IBM Plex with Inter.** The slightly geometric IBM proportions are part of the technical-internet aesthetic
- **Don't add gradient backgrounds to the canvas.** The dark mode is solid #0e1113; the light mode is solid #ffffff
- **Don't break the `/r/` subreddit URL convention.** It is brand IA
