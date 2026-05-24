# Privacy policy

**Last updated:** 2026-05-24

## The short version

The `ux-skill` plugin runs entirely on your machine. It doesn't phone home. It doesn't collect telemetry. It has no account system. The landing page at [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) is a static file served by GitHub Pages with no analytics tracking, no tracking pixels, and no cookies from our domain.

The long version is below.

---

## Who maintains this

`ux-skill` is a personal open-source project maintained by **Laith Aljunaidy**. Contact: [laith.aljunaidy.laith@gmail.com](mailto:laith.aljunaidy.laith@gmail.com).

---

## The plugin (when you install and run it in Claude Code)

### Data we collect from you

**None.** The plugin has no analytics, no telemetry, no usage metrics, no crash reports, no API keys, no phone-home checks, no "anonymous improvement data", no A/B testing.

### Network calls the plugin makes

**None.** Specifically:

- The plugin's deterministic linter (`/ux-lint`) runs pure regex over local files. Zero network.
- Generation commands (`/ux-design`, `/ux-component`, etc.) run inside your Claude Code session. Any LLM calls go through your own Claude Code authentication, not the plugin's.
- Sub-agents (frontend-engineer, motion-engineer, copy-writer, research-synthesizer, design-system-architect) are dispatched via Claude Code's own `Task` tool. They don't add separate network channels.

If you find a network call you didn't expect, that's a bug. Please file an issue.

### Files the plugin reads on your machine

- Files in the project directory you point commands at (e.g. `/ux-audit ./components/Hero.tsx`).
- The plugin's own internal files — commands, sub-agents, references, brand specs.
- `.ux/last-*.json` state files written by the plugin's prior commands, so commands can chain.

### Files the plugin writes on your machine

- `.ux/last-frame.json`, `.ux/last-audit.json`, `.ux/last-design.json`, etc. — local state for command chaining.
- Code files when you run generation commands like `/ux-design`, `/ux-fix`, or `/ux-component` — at paths you've specified or that the calling command identifies.

All file reads and writes stay on your local filesystem. Nothing is transmitted off your machine.

### Updates

The plugin updates only when you run `/plugin update ux` or pull the repo manually. There is no auto-update channel and no telemetry tied to updates.

---

## The landing page ([uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com))

The landing is a single self-contained HTML file served by **GitHub Pages**.

### What loads when you visit

- The HTML file itself from GitHub's CDN.
- A small amount of JavaScript bundled into that file (Tailwind CSS, Alpine.js, and GSAP libraries delivered via public CDNs).
- Webfonts from Google Fonts (Cormorant Garamond, Inter, JetBrains Mono). Google receives your IP for font delivery per Google's own [privacy policy](https://policies.google.com/privacy).

### What we explicitly do NOT use

- No Google Analytics.
- No Plausible / Fathom / Umami / Heap / Mixpanel / any analytics.
- No tracking pixels.
- No cookies set by `uxskill.laithjunaidy.com`.
- No third-party tracking scripts.
- No A/B testing infrastructure.
- No marketing-attribution tools.
- No advertising or retargeting scripts.

### What GitHub Pages may log

GitHub may keep server-side access logs (IP address, user agent, requested resource, timestamp) for its own operations and abuse prevention. We don't see or process these. See [GitHub's privacy statement](https://docs.github.com/en/site-policy/privacy-policies/github-privacy-statement).

### What Google Fonts may log

When fonts load from `fonts.googleapis.com` and `fonts.gstatic.com`, Google receives the request URL, your IP, and the requested font file. We don't have control over this — it's part of how web fonts work. See [Google's font privacy FAQ](https://developers.google.com/fonts/faq#what_does_using_the_google_fonts_api_mean_for_the_privacy_of_my_users).

### What CDN providers (Tailwind, Alpine, GSAP) may log

The script tags load from public CDN endpoints. The CDN provider receives the same kind of basic request log GitHub Pages does (IP, timestamp, requested file). We don't see or process these.

---

## Third-party brand references (`references/brands/`)

The plugin ships **72 brand DESIGN.md spec files** as design references — Apple, Stripe, Linear, Notion, Figma, Tesla, BMW, and 65 others. These describe brand design languages for educational and reference purposes only.

- They are derived from publicly observable design patterns and publicly available brand guidelines.
- They do not include trademarks, logos, or proprietary assets owned by those brands.
- They should be treated as design references and study aids, not as endorsements or partnerships.

**If you are a rights-holder** and believe a brand reference misrepresents your brand or includes content that should be removed: email `laith.aljunaidy.laith@gmail.com` and it will be addressed within 5 business days.

---

## Cookies

The landing page at `uxskill.laithjunaidy.com` sets **zero cookies**. GitHub Pages may use cookies for its own operation (e.g. session tracking on its admin surfaces, but not on the served static site). We don't set, read, or store cookies.

---

## Children's privacy

This service is not directed at children under 13. We do not knowingly collect data from anyone, including minors.

---

## Your data subject rights (GDPR, CCPA, etc.)

If you are in a jurisdiction with data subject rights:

- **The plugin:** there is no personal data on our side to access, correct, port, or delete. We don't have any.
- **The landing page:** there is no account, no profile, no stored data on our side. The only data flowing related to you is the brief server-side access log GitHub keeps, which is out of our control. Direct any requests there to GitHub.

If you have a specific request or question, contact: [laith.aljunaidy.laith@gmail.com](mailto:laith.aljunaidy.laith@gmail.com).

---

## Changes to this policy

If this policy changes, the **Last updated** date at the top updates. Material changes will be announced in the repository's release notes.

---

## Contact

**Laith Aljunaidy**
Email: [laith.aljunaidy.laith@gmail.com](mailto:laith.aljunaidy.laith@gmail.com)
LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
Repository: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
