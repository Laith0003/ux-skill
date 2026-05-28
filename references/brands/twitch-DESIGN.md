# Twitch — DESIGN.md

## Overview
Twitch is Amazon's live-streaming platform built for gamers, vtubers, IRL streamers, and the parasocial chat economy. Canvas is deep purple-tinted black (`#0e0e10`) — distinguishably more purple than Netflix's true black or YouTube's pure black. The signature is Twitch purple (`#9146ff`) — used at full saturation on the wordmark, on every primary CTA, on the 'Following', 'Subscribe', and 'Cheer' buttons. Type runs Inter (Twitch transitioned from Roobert to Inter as the system face) at modest scale. The interface is dominated by the chat sidebar and the channel grid — every stream is rendered with the streamer's webcam in the corner of game footage, and the chat scrolls live with subscriber-only badges, emote spam, and channel-points redemptions.

## Color
- **Primary:** `#9146ff` — Twitch purple (every CTA + wordmark + speech-balloon glyph)
- **Canvas:** `#0e0e10` — Purple-tinted black (distinguishably purpler than `#000`)
- **Canvas card:** `#1f1f23` — Elevated card surface
- **Ink:** `#efeff1` — Off-white type
- **Muted:** `#adadb8` — Captions, viewer counts, metadata
- **Accent:** `#bf94ff` — Lighter purple for emphasis and active states
- **Hairlines:** `rgba(255,255,255,0.08)`
- **Sub-tier (Hype Train):** purple gradient `#9146ff` → `#bf94ff`

## Typography
- **Display:** Inter, weight 700, 32–48px hero (modest, chat-dominant UI)
- **Sub-display:** Inter, weight 600, 18–22px row titles
- **Body:** Inter, weight 400, 14–15px, 1.5 line-height
- **Caption:** weight 500, 12–13px viewer counts
- **Mono:** JetBrains Mono, 13px for chat-command help and developer pages

## Spacing & rhythm
4-base (4/8/12/16/24/32). Dense — chat sidebar is 30–40% of viewport, video is 60–70%. Stream tiles stack 3-up or 4-up in directory. Page padding 16–24px maximum to maximize chat real estate.

## Motion signature
Real-time chat scroll — message bubbles slide up at variable cadence (sometimes 1/sec, sometimes 20/sec during hype moments). Subscriber-baked emote animations loop infinitely. Sub-Hype-Train celebration overlays cascade purple confetti for 5 seconds on viewer milestone events. Channel-points-redemption notifications float in from the right with a 600ms cubic-bezier slide.

## Components observed
- `live-stream-tile-with-webcam` — game thumbnail + streamer webcam circle overlay
- `chat-sidebar-scrolling` — real-time chat panel with badges and emotes
- `speech-balloon-glyph` — Twitch wordmark's purple chat-bubble accent
- `subscribe-button-purple` — purple-fill 'Subscribe' CTA
- `channel-category-card` — game/category browse tile
- `emote-grid-keyboard` — bespoke emote picker with channel-emotes
- `hype-train-overlay-purple` — purple confetti milestone overlay
- `button-primary-twitch-purple` — primary CTA on purple

## Trademark signals
- Deep purple-tinted black canvas (`#0e0e10`) — purple tint distinguishes Twitch from Netflix true black and YouTube pure black
- Twitch purple (`#9146ff`) — vivid near-Brand-saturated purple on every CTA, every primary button, wordmark, speech-balloon glyph
- Speech-balloon glyph — wordmark's chat-bubble accent emerging from the 'T' — always alive to the chat-driven brand
- Live-stream tile with streamer webcam in corner — gameplay full-frame with face-cam overlaid in a circular thumbnail
- Chat-sidebar UI dominance — every channel page is split: video left (60–70%), chat right (30–40%) — chat is NOT optional; it IS the platform voltage

## What they DON'T do
- No dropping the chat sidebar — video-only layouts read as YouTube/Netflix
- No tinting the purple — `#9146ff` is the recognized voltage
- No true-black canvas — purple-tint (`#0e0e10`) is the brand differentiator
- No stripping the streamer-webcam overlay from thumbnails — face-cam IS the parasocial brand promise
- No serif typography substitution — Twitch's voice is grotesk-utility
- No emoji as decoration (the in-chat emote economy is its own affordance, not brand chrome)

## Exemplar pages
- https://twitch.tv/
- https://twitch.tv/directory
- https://twitch.tv/p/about
- https://blog.twitch.tv/

## When to reference
Reach for Twitch when the user wants live-stream platform UI with strong chat-sidebar density and parasocial creator economics — live commerce, esports broadcasting, video chat communities, real-time auction platforms. The "purple-tinted black canvas + Twitch purple voltage + chat-sidebar dominance + face-cam thumbnail overlay" combination is the most-copyable Twitch move. Pairs well with brands whose value prop depends on real-time audience interaction rather than passive consumption.
