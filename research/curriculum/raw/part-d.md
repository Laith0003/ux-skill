# Part D: Emerging Technologies, UX Strategy, Portfolio Development, Career Development

Block: hendurhance/ui-ux README.md lines 1656 to 2303 (local clone, read only).

Scope note. The block holds 234 link occurrences: 207 ordinary links (206 unique; designsystemchecklist.com appears twice) and 27 mega.nz "Mirror" links. The mirrors point at file copies of books, most of them paid books; they were not opened and should not be ingested or linked by ux-skill. Each mirrored book is analyzed through its publisher or author page instead (see ledger part 2b). The block also holds three link-free bodies of content that were analyzed: the "ChatGPT Prompts for UI/UX Design" table, Project Tasks #4 and #5, and the resume and cover letter boxes.

Method. Every unique link was fetched with curl (one pass, 16 in parallel); pages that returned text were read from extracted text. Pages that returned 403 to curl were retried with WebFetch; Toptal and Adobe pages came through that way. Medium, uxdesign.cc, uxplanet.org, Behance and a few others refused both and are recorded as blocked, with lessons taken only from the list's own description and, for two key pieces, from search-result summaries (said where used). YouTube pages were rate limited (429), so every video was confirmed live through YouTube oEmbed (title and channel) and summarized from the list description only. Books were summarized from publisher or author pages; no claim is made to have read any book.

Status key (against ux-skill as of this checkout):
- COVERED: ux-skill already encodes it (file or rule named).
- MISSING-CHECK: machine-checkable and absent; a lint rule, render measurement or complaints probe is proposed with a detection sketch.
- MISSING-GUIDE: guidance only; the target references/ (or commands/) file is named.

Lesson ids: V = voice, S = spatial (AR, VR, 3D), A = AI and ML, ST = strategy, P = portfolio and case study, C = career.

---

# Part 1. Topic sections

## 1. Voice and multimodal interfaces

ux-skill builds web pages, apps and dashboards. Voice matters to it in three places: a mic button or dictation in a form or chat, an assistant that speaks or reads back, and companion screens for voice devices (hub, TV, kiosk). There is no voice guidance in ux-skill today (grep for speech, voice UI, dictation finds only aria-live notes in accessibility.md).

**V1. Voice first, never voice only.** A task must be completable by voice, but never only by voice or only by screen: give a typed path for anything that can be spoken, put spoken output on screen as text, and let people switch mode mid-task. Hard-to-speak data (phone numbers, addresses, passwords, codes) gets a non-voice input.
- Sources: https://www.smashingmagazine.com/2022/02/voice-user-interfaces-guide/ ; https://www.toptal.com/designers/ui/designing-a-vui ; https://books.google.com/books/about/Voice_User_Interface_Design.html?id=Q3B_DwAAQBAJ (description)
- Status: MISSING-CHECK `voice-input-no-text-fallback` (lint). Detection: file references `SpeechRecognition`/`webkitSpeechRecognition`, or a button whose accessible name matches /mic|microphone|voice|dictat|speak/i, inside a form or region that has no `input[type=text|search]`, `textarea` or `[contenteditable]`.

**V2. Keep spoken output to one breath and three options.** Listeners cannot scan or rewind. A response should be sayable at conversational pace in one breath; offer the best option first and at most three; no complex data (tables, long lists) by voice: hand those to the screen.
- Sources: https://www.smashingmagazine.com/2022/02/voice-user-interfaces-guide/ ; https://www.uxpin.com/studio/blog/voice-user-interface/ ; https://www.toptal.com/designers/ui/designing-a-vui ; https://ixdf.org/literature/topics/voice-user-interfaces
- Status: MISSING-GUIDE: new references/foundations/voice-and-multimodal.md (Prompts and responses).

**V3. Ask closed questions with named choices.** "You can cancel or reschedule. Which one?" beats "What do you want to do?". Open or rhetorical prompts invite input the system cannot handle. Distinguish prompts (expect an answer) from statements (inform).
- Sources: Smashing (above) ; UXPin (above)
- Status: COVERED for chat entry points (foundations/ai-interfaces.md "Set expectations before the first question": example prompts, never "Ask me anything"); MISSING-GUIDE for spoken prompts in voice-and-multimodal.md.

**V4. Timing numbers for spoken turns.** Pause about 500 ms after a question before listing options; allow 8 to 10 s of silence before re-prompting; re-prompts are rephrased and conversational, not a repeated recording.
- Sources: Smashing (above) ; UXPin (above)
- Status: MISSING-GUIDE: voice-and-multimodal.md (Timing tokens).

**V5. Always show what the system is doing.** Wake, listening, processing and speaking are distinct states and each needs a signal (light, motion, sound, on-screen text). Silence while working reads as broken. On a web mic button that means a pressed state and an announced status.
- Sources: Smashing (above) ; UXPin (above) ; https://userguiding.com/blog/voice-user-interface
- Status: MISSING-CHECK `mic-button-no-listening-state` (lint). Detection: a button matching the V1 mic pattern with no `aria-pressed`, and no element with `aria-live` or `role=status` in the same component file.

**V6. Confirm by risk.** Explicit confirmation ("Send 1,000 dollars to Alice, correct?") for money, messages and anything hard to undo; implicit confirmation for low-risk acts (stop the music without asking); always confirm completion aloud when the person cannot see the result.
- Sources: Smashing (above) ; Toptal VUI (above)
- Status: COVERED for consequential actions (foundations/ai-interfaces.md "Keep a person in charge of actions": show what will happen, button names the action); MISSING-GUIDE for implicit confirmation and spoken completion (voice-and-multimodal.md).

**V7. Repair, not dead ends.** Design separate no-match and no-input paths; never answer only "I didn't understand"; say what it cannot do and offer what it can ("I can't book flights, but I can find hotels"); accept corrections ("No, I said Tuesday"); "repeat" works at any time. The Natural Conversation Framework treats these repair moves (repeat, paraphrase, what can you do, never mind) as a small fixed set of user actions every agent should support (per publisher and paper summaries; book not read).
- Sources: Smashing (above) ; Toptal VUI (above) ; https://dl.acm.org/doi/book/10.1145/3304087 (blocked; summarized from search results)
- Status: MISSING-CHECK `assistant-dead-end-fallback` (lint, text channel). Detection: string literal or text node matching /(sorry, )?I (did not|didn't|don't|do not) (understand|get that|catch that)/i whose containing element or next sibling holds no button, link or list of options. MISSING-GUIDE: add a "Repair" section to foundations/ai-interfaces.md (merged with A8).

**V8. The person starts the conversation.** A voice system should not speak first or bring up topics unprompted. On the web: no speech on page load.
- Sources: Smashing (above)
- Status: MISSING-CHECK `speech-autoplay-on-load` (lint). Detection: `speechSynthesis.speak(` reachable from `DOMContentLoaded`, `window.onload`, a top-level statement, or a React `useEffect` with an empty dependency array, and not inside a click, keydown or submit handler. (Also serves WCAG 1.4.2 audio control.)

**V9. Do not read private data aloud; add a second factor for sensitive acts.** Others may be in the room. Medical or financial details stay on screen; payments and personal messages need a factor beyond voice match.
- Sources: Smashing (above) ; Toptal VUI (above) ; UXPin (above)
- Status: MISSING-GUIDE: voice-and-multimodal.md (Privacy and trust).

**V10. Teach capabilities by doing.** Voice has no visible affordances: first use should walk through one or two real commands, and "what can you do" must always get a short, useful answer.
- Sources: Smashing (above) ; https://ixdf.org/literature/topics/voice-user-interfaces ; NCF (above)
- Status: COVERED for chat (foundations/ai-interfaces.md "Say what it is and what it can do"); MISSING-GUIDE for voice onboarding (voice-and-multimodal.md).

**V11. Design for the setting and the voice persona.** Shared or personal device, public or private, noisy or quiet change every prompt. Personas for voice include word choice, sentence shape and regional speech; the assistant's persona matches the brand voice.
- Sources: Smashing (above) ; UXPin (above) ; https://userguiding.com/blog/voice-user-interface
- Status: MISSING-GUIDE: voice-and-multimodal.md (Context) ; brand voice itself is COVERED by process/discovery-protocol.md field 5 (Voice).

**V12. Write dialog as spoken and test it out loud.** Script the happy path first, then the 20 percent of paths 80 percent of people take; read scripts aloud; test with role play or Wizard of Oz, participants back to back so no eye contact helps; then 5 first-time users.
- Sources: Smashing (above) ; https://www.toptal.com/designers/ui/designing-a-vui ; https://userguiding.com/blog/voice-user-interface ; https://www.youtube.com/watch?v=8OXN0ZDpwrM (description)
- Status: MISSING-GUIDE: voice-and-multimodal.md (Process). The 5-user rule itself is COVERED (laws/krug.md, process/lean-ux-klein.md).

**V13. Screens for voice devices are read from a distance.** Hubs are viewed from 1 to 2 m and TVs from about 3 m; Google's guidance cited by Smashing is at least 32 pt for primary text and 24 pt for secondary. Start from the smallest screen, keep one thing per screen in priority order, cards for comparing options, and keep picture and speech in sync (no lag, no hard cuts).
- Sources: Smashing (above)
- Status: MISSING-CHECK `distance-text-too-small` (render, conditional). Detection: only when the brief's platform is tv, hub or kiosk; at 1280x720 and 1920x1080 flag visible text nodes whose computed font-size is under 24 px (secondary) and headings under 32 px. MISSING-GUIDE: foundations/responsive.md (Distance viewing).

**V14. Measure the conversation.** Track sessions per user, turns per session, no-match and no-input rates, intents and utterances; mine the misses to fix the dialog.
- Sources: Toptal VUI (above) ; https://books.google.com/books/about/Designing_Voice_User_Interfaces.html?id=MmnEDQAAQBAJ (description: measuring VUI performance)
- Status: MISSING-GUIDE: voice-and-multimodal.md (Metrics) ; general metric discipline COVERED in process/lean-ux-gothelf.md (Measurement).

**V15. Is voice the right tool at all?** Voice wins hands-busy and eyes-busy moments (driving, cooking, exercise); it loses at browsing, comparing and reviewing. Decide per task, not per product.
- Sources: https://www.uxpin.com/studio/blog/voice-user-interface/ ; https://www.boldare.com/blog/what-is-voice-user-interface/ ; Smashing (above)
- Status: MISSING-GUIDE: voice-and-multimodal.md (When to use).

---

## 2. Spatial interfaces: AR, VR, 3D on the web

For ux-skill the live cases are 3D product viewers (model-viewer, three.js), WebXR entry points and scroll-driven camera scenes on landing pages. Full headset apps are out of its build scope, so most of this is guidance.

**S1. Comfort is the floor.** The person controls movement; never move or zoom the camera for them; when tracking or immersion must break, fade to black rather than cut. Beau Cronin's VR hierarchy puts comfort at its base (per secondary summaries; article blocked). On the web the equivalent is an auto-rotating or auto-flying 3D camera with no reduced-motion branch.
- Sources: https://www.creativebloq.com/ux/the-user-experience-of-virtual-reality-31619635 ; https://medium.com/@beaucronin/the-hierarchy-of-needs-in-virtual-reality-development-4333a4833acc (blocked) ; https://www.youtube.com/watch?v=Qwh1LBzz3AU&t=488s (description: physiological and ergonomic constraints)
- Status: MISSING-CHECK `autorotate-without-reduced-motion` (lint). Detection: `autoRotate\s*[:=]\s*true` (three.js OrbitControls, drei), or `<model-viewer` with an `auto-rotate` attribute, or a GSAP/ScrollTrigger tween on `camera.position`, in a project with no `prefers-reduced-motion` query anywhere in its scripts. Extends the existing `infinite-animation-without-reduced-motion` family from CSS to JS-driven 3D.

**S2. Place UI in the world, not glued to the eyes.** World-locked elements stay put (signs); follow-along elements travel with the person (a dashboard); menus and labels sit at the same depth as the object they describe; game-style HUDs fixed to the view do not work in VR.
- Sources: https://www.toptal.com/designers/ui/vr-ar-design-guide ; https://www.creativebloq.com/ux/the-user-experience-of-virtual-reality-31619635
- Status: MISSING-GUIDE: new references/conditional/spatial.md (Placement).

**S3. Text in 3D is short, large and heavy.** Low-resolution headsets need larger, thicker type and less detail; a 2D paragraph pasted into 3D is barely legible; keep spatial copy to labels and short lines.
- Sources: Toptal VR/AR (above) ; Creative Bloq (above)
- Status: MISSING-GUIDE: conditional/spatial.md (Type).

**S4. Design for the platform's input set and confirm every input.** Gaze, gesture, voice, controllers and touch differ per platform; there is no tactile keyboard, so controls must be easy; give a hint before and feedback after every interaction; use familiar physical metaphors (turn a dial, grab an object).
- Sources: Toptal VR/AR (above) ; Creative Bloq (above)
- Status: MISSING-GUIDE: conditional/spatial.md (Input). Physical metaphor and mapping are COVERED by laws/norman.md (affordances, natural mapping).

**S5. Sound and setup are part of the interface.** Spatial (binaural) audio cues direct attention; the physical setup (seated or standing, clear play space) is designed, not assumed.
- Sources: Creative Bloq (above)
- Status: MISSING-GUIDE: conditional/spatial.md (Audio and setup).

**S6. Specify spatial UIs as objects.** VRID decomposes a VR interface into objects, each with graphics, behaviors (physical or "magical", simple or composite), interactions and communications, specified first at high level and then low level, which gives designers and developers a shared spec.
- Sources: http://www.cs.tufts.edu/~jacob/papers/vrst01.tanriverdi.pdf (read)
- Status: MISSING-GUIDE: conditional/spatial.md (Specifying), low priority.

**S7. Prototype spatial work cheaply before building.** Pre-visualise in 2D tools and move to the headset early (Figma to Unity, no-code XR previews); test sightlines before committing to placement.
- Sources: https://www.youtube.com/watch?v=id86HeV-Vb8 ; https://www.youtube.com/watch?v=mW8tRQRQD74 ; https://www.youtube.com/watch?v=nmlWiK9AokE ; https://uxdesign.cc/lets-design-xr-ui-in-figma-and-bring-it-to-xr-with-no-code-a123b9b647ab (all from descriptions; article blocked) ; Toptal VR/AR (above)
- Status: MISSING-GUIDE: conditional/spatial.md (Process).

**S8. WebXR is an enhancement.** The page must work without a headset; check support before offering "Enter VR/AR" and keep a 2D path to the same content.
- Sources: https://www.youtube.com/watch?v=ZOaOYTOpwyM (description: UX for WebVR on the open web) ; https://books.google.com/books/about/Learning_Virtual_Reality.html?id=T5XtrQEACAAJ (description: desktop, web and mobile VR)
- Status: MISSING-CHECK `webxr-without-support-check` (lint). Detection: `navigator.xr.requestSession(` present and `isSessionSupported(` absent in the same bundle, or an "Enter VR/AR" button rendered unconditionally.

**S9. Body and avatar must match the person.** A visible body raises immersion, but one that does not track the real body disorients.
- Sources: Creative Bloq (above)
- Status: MISSING-GUIDE: conditional/spatial.md (Avatars), low priority.

---

## 3. AI and machine learning features

ux-skill already has foundations/ai-interfaces.md (disclosure, streaming, stop, regenerate, citations, uncertainty, agent consent, privacy, system look). Most of this section confirms it; three gaps are new.

**A1. Design for being wrong.** Conventional software is always right about easy things; ML is often right about hard things. Every ML output needs a way to correct it, a fallback, and honest signals of certainty.
- Sources: https://www.oreilly.com/radar/machine-learning-for-designers/
- Status: COVERED (foundations/ai-interfaces.md "Let the person correct it" and "Show where an answer comes from, and how sure it is").

**A2. Use ML only where plain logic cannot do the job.** If a rule, a filter or a form solves it, ship that; AI added for its own sake adds unpredictability and cost.
- Sources: O'Reilly (above) ; https://www.toptal.com/designers/product-design/infographic-ai-in-design (AI is over-hyped)
- Status: MISSING-GUIDE: foundations/ai-interfaces.md (new opening section "When not to use AI"). Copy-side hype is COVERED by `marketing-buzz-ai-powered-driven` and `marketing-buzz-leverage-ai-harness`.

**A3. The system proposes, the person decides.** Review, approve, reject, adjust.
- Sources: Toptal AI (above)
- Status: COVERED (foundations/ai-interfaces.md "Keep a person in charge of actions").

**A4. Adaptive systems must show what they learned.** AI behavior changes over time while its interface usually does not. Show what personalization is based on, let people see, edit and reset it, and say when behavior changed.
- Sources: https://www.goodreads.com/en/book/show/61514121-designing-human-centric-ai-experiences (description) ; Smashing (personalization from stored profiles)
- Status: MISSING-GUIDE: foundations/ai-interfaces.md ("Respect what people share": add view, edit and reset of learned preferences).

**A5. Generated output stays inside the design system.**
- Sources: Toptal AI (above)
- Status: COVERED (foundations/ai-interfaces.md "Look like the product, not like a chatbot template").

**A6. AI-made research is a hypothesis, not data.** The list's ChatGPT prompt table suggests generating personas, user stories and "demographic data of my target audience". Output like that must be labeled an assumption to validate, never presented as findings.
- Sources: README lines 1794 to 1816 (ChatGPT Prompts for UI/UX Design)
- Status: MISSING-GUIDE: commands/ux-research.md (Hard rules: synthetic personas and demographics are labeled "assumption, not research") and process/lean-ux-klein.md (Common research traps).

**A7. Generated copy replaces lorem ipsum, not facts.** The same table uses AI copy as a lorem replacement; it still must not invent names, numbers or testimonials.
- Sources: README ChatGPT prompts table
- Status: COVERED (`lorem-ipsum-leak`, `fake-name-john-doe`, `round-number-stats`, `testimonial-fake-five-stars`, `placeholder-token-shipped`).

**A8. Give the person repair moves in conversational UI.** Beyond regenerate: ask it to repeat, rephrase simpler, define a term, shorten, or say what it can do; when declining, offer the nearest thing it can do. (Merged with V7.)
- Sources: https://dl.acm.org/doi/book/10.1145/3304087 (summaries) ; Smashing (above)
- Status: MISSING-GUIDE: foundations/ai-interfaces.md (new "Repair" section). Check: see `assistant-dead-end-fallback` under V7 (not double counted).

**A9. Explainability and fairness are design inputs.** ML engineering patterns include explainability and fairness; the interface is where they surface.
- Sources: https://books.google.com/books/about/Machine_Learning_Design_Patterns.html?id=dDwDEAAAQBAJ (description)
- Status: COVERED (foundations/ai-interfaces.md sources and citation and uncertainty sections).

---

## 4. UX strategy: research, metrics, prioritization, IA, sprints

**ST1. Strategy has four parts.** Jaime Levy: UX strategy = business strategy + value innovation + validated user research + frictionless UX. A polished UX for a product nobody wants, or a validated need with no differentiated offer, both fail.
- Sources: https://jaimelevy.com/ux-strategy-book/ (free chapters read) ; https://www.youtube.com/watch?v=iTYulrROJP8 (description)
- Status: MISSING-GUIDE: process/discovery-protocol.md (add an optional "What makes this different from the alternatives" field next to 3a). Validated research and frictionless UX are COVERED (process/lean-ux-klein.md, laws/krug.md).

**ST2. Competitive analysis is a bounded matrix.** 5 to 10 direct and indirect competitors; record the tasks people can do and the journeys; summarize impact on our decisions rather than listing findings; the classic failure is the endless list.
- Sources: https://usabilitygeek.com/how-to-do-ux-competitor-analysis/ ; https://jaimelevy.com/ux-strategy-book/ (toolkit)
- Status: MISSING-GUIDE: commands/ux-research.md (method "Competitive matrix"). Today ux-research only consumes competitor sites as `forbidden` and `reference_brands` inputs.

**ST3. A research plan answers who, why, what, when and how it moves the business.** Tie each study to the product phase (discovery, definition, testing, delivery, post-launch); plan research rather than reacting after release.
- Sources: https://maze.co/guides/ux-research/ux-research-strategy/ ; https://www.userinterviews.com/blog/the-ultimate-guide-to-ux-research-strategy ; https://www.youtube.com/watch?v=Kj16KEqHsy4 (description)
- Status: COVERED (commands/ux-research.md "Frame the research question"; process/lean-ux-klein.md "Three research questions").

**ST4. Rank findings by severity, then impact against effort.** Severity says how bad; impact against effort says what to do first; tie both to the metric the team owns (retention beats taste).
- Sources: https://contentsquare.com/guides/ux/analysis/
- Status: MISSING-GUIDE: commands/ux-audit.md (add an effort estimate per finding cluster and order "next moves" by impact over effort; severity tiers already exist).

**ST5. Pair numbers with observation.** Heatmaps, funnels and surveys say where; replays, tests and interviews say why.
- Sources: Contentsquare (above) ; https://careerfoundry.com/en/blog/ux-design/how-to-conduct-user-experience-research-like-a-professional/
- Status: COVERED (process/lean-ux-klein.md "Analytics and qualitative paired").

**ST6. You are not the user.** Testing on yourself is the amateur's mistake.
- Sources: CareerFoundry research (above)
- Status: COVERED (process/lean-ux-klein.md; laws/krug.md).

**ST7. Problem statements name the broken thing.** "Users can't find their account overview; it's buried two menus deep" beats "the app is frustrating and churn is high".
- Sources: https://uxcel.com/blog/how-to-write-a-ux-case-study-in-5-steps
- Status: MISSING-GUIDE: commands/ux-case-study.md (section B) and output/case-study-style.md (Voice: "claims carry evidence" exists; add the problem-statement rule).

**ST8. Outcome metrics with a baseline and a counter-metric.**
- Sources: https://leanuxbook.com/ (description) ; Contentsquare (above)
- Status: COVERED (process/lean-ux-gothelf.md "Measurement, in detail").

**ST9. Content strategy keeps words from drifting.** Audit existing labels, errors and onboarding; keep a terminology list (one concept, one word); standardize voice, button, error, empty and confirmation patterns; give someone governance or the language rots.
- Sources: https://technicalwriterhq.com/content/content-strategy/content-strategy-in-ux/ ; https://www.peachpit.com/store/content-strategy-for-the-web-9780132883238 (description) ; https://shop.elsevier.com/books/content-strategy-at-work/bloomstein/978-0-12-391922-9 (description) ; https://www.youtube.com/watch?v=OPHfDVWyuZU (description)
- Status: COVERED in part (foundations/copy.md "Voice consistency across surfaces"; lint `one-action-several-labels`, `repeated-action-same-name` within one page). MISSING-CHECK `nav-label-destination-mismatch` (lint, multi-page): for each internal nav link, compare its text with the target page's h1 and title; flag when they share no content word after stemming (nav "Pricing", page h1 "Plans and billing").

**ST10. IA basics.** Structure before hierarchy; the most used feature gets the most prominence; every step follows logically from the last; flow diagrams carry a legend, consistent shapes and labelled connectors; IA is built from research and considers accessibility from the start.
- Sources: https://www.toptal.com/designers/ia/guide-to-information-architecture ; https://www.bynder.com/en/blog/content-101-information-architecture/ (blocked) ; https://www.youtube.com/watch?v=j0y8YBhDjIA (description)
- Status: COVERED (laws/krug.md street signs and conventions; laws/laws-of-ux.md; inventory rows E8 and E9 for prominence).

**ST11. Search is designed, not bolted on.** Integrate search with browse (filters, categories, suggestions in one finding UI); design the zero-results state with a way forward.
- Sources: https://www.wiley.com/en-ae/Designing+Search%3A+UX+Strategies+for+eCommerce+Success-p-9781118109953 (description)
- Status: MISSING-GUIDE: foundations/component-behaviors.md (new "Search" behavior: suggestions, scoped search, zero-results with alternatives). component-behaviors.md has no search entry today.

**ST12. Design sprint mechanics.** Five days (map, sketch, decide, prototype, test) with 5 to 7 people and one decider; "how might we" notes voted; sketch alone (Crazy 8s, three-panel storyboard); a prototype just real enough to test; 5 to 6 testers on day five with a five-part interview (welcome, context, introduce prototype, tasks with think-aloud, debrief); book testers on day one. Variants: the 4-day Sprint 2.0 and 10-day UX sprints with a handover to the design system.
- Sources: https://www.toptal.com/designers/product-design/effective-design-sprint ; https://ixdf.org/literature/topics/design-sprints ; https://careerfoundry.com/en/blog/ux-design/what-are-design-sprints/ ; https://boanastudio.com/blog/ux-design-sprint-digital-products ; https://www.character.vc/sprint ; https://books.google.com/books/about/Design_Sprint.html?id=mCKsAQAACAAJ ; https://www.youtube.com/playlist?list=PLxk9zj3EDi0X5CgoFckoheIFAx-uT2i7j ; videos 1930 to 1932 (descriptions) ; https://uxplanet.org/whats-a-design-sprint-and-why-is-it-important-f7b826651e09 (blocked)
- Status: MISSING-GUIDE: new references/process/design-sprint.md, offered as a /ux-workshop variant (today /ux-workshop runs the AppHaus format only). Generating many variations is already COVERED (process/generation-modes.md), and realistic prototype content by `lorem-ipsum-leak`.

**ST13. Lean UX and lean startup research.**
- Sources: https://leanuxbook.com/ ; https://www.goodreads.com/book/show/16128986-ux-for-lean-startups (descriptions)
- Status: COVERED (process/lean-ux-gothelf.md, process/lean-ux-klein.md distill both books).

**ST14. Interview with open questions about past behavior.**
- Sources: https://projects.iq.harvard.edu/files/harvarduxgroup/files/ux-research-guide-sample-questions-for-user-interviews.pdf (blocked; description) ; https://shop.elsevier.com/books/understanding-your-users/baxter/978-0-12-800232-2 (description)
- Status: COVERED (process/lean-ux-klein.md "Customer interview methodology").

**ST15. A design system is planned as a checklist.** Design language (principles, tone, terminology), foundations (semantic color, dark mode, grid, breakpoints, spacing, type, elevation and z-index, motion easing and duration, icon naming), and every component with its states (hover, active, loading, disabled, focus, error, empty) plus reduced motion for loaders and skeletons. One idea is new to ux-skill: reserved icons, an icon that means one thing everywhere.
- Sources: https://www.designsystemchecklist.com/ (item list read from the page data)
- Status: COVERED for foundations and states (commands/ux-system.md, foundations/components.md, foundations/component-behaviors.md). MISSING-CHECK `icon-meaning-reused` (lint): within one page, the same inline SVG (hash of its path data) or the same named icon import appears in two buttons or links whose accessible names share no word.

---

## 5. Portfolio sites and case studies

This is the section with the most weight for ux-skill: it already has a `portfolio-agency` page sequence (data/page-sequences.json), `creator-portfolio-builder` and `media-photography-portfolio` industries, a minimal-portfolio style, and /ux-case-study with references/output/case-study-style.md. The sources below show what that set misses.

### 5a. The portfolio site

**P1. Open with a positioning line, not a greeting.** The first screen says what you design, for whom or in what domain, and where you are or work: "Staff product designer at Pinterest; complex systems made trustworthy." Weak openers lead with hobbies or a bare "Hi, I'm X".
- Sources: https://saschas.ai/ ; https://priyanka.io/ ; https://lolajiang.com/index.html ; https://zaradrei.com/ ; https://www.sarasoueidan.com/ (strong) ; https://www.glorialo.design/ (hobby-first hero) ; https://www.peachpit.com/store/stand-out-design-a-personal-brand.-build-a-killer-portfolio-9780134134086 (description) ; https://www.toptal.com/designers/ux/ux-design-job-interview-tips
- Status: COVERED as guidance (data/page-sequences.json portfolio-agency hero: "confident positioning statement"). MISSING-CHECK `portfolio-hero-no-role` (lint or render, page_sequence portfolio-agency only): the h1 plus the first paragraph in the first viewport contain no role noun (designer, engineer, developer, researcher, studio, illustrator, photographer, writer, consultant, director) or are a greeting only (/^(hi|hey|hello)[,!.]? i'?m \w+[.!]?$/i).

**P2. The work shows up on the first screen or right after it.** Reviewers come for the work; an about block, skill bars or a long intro above it costs attention.
- Sources: https://www.toptal.com/designers/ux/ux-designer-portfolios ; https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/ (cover page links straight to case studies) ; data/page-sequences.json (hero with selected work peek)
- Status: COVERED as guidance (portfolio-agency sequence). MISSING-CHECK `portfolio-work-below-fold` (render): on a portfolio page, the top of the first project tile (first link to a case study or first item of the work grid) sits below 1.5 viewport heights at 1280x800 or 390x844.

**P3. Every project tile names the project, your part and the result.** Strong tiles carry company or project name, a one-line scope or outcome (with a real number when there is one) and link to the case study. Image-only tiles make the reviewer click to learn anything.
- Sources: https://priyanka.io/ ; https://lolajiang.com/index.html ; https://saschas.ai/ ; https://www.oliviatruong.design/ ; https://www.youtube.com/watch?v=emSv9TTHZVY (description)
- Status: MISSING-CHECK `work-tile-image-only` (lint): a link or card inside the work grid whose content is only an img or picture (no heading, no text node of 3 or more words, alt text not counted). MISSING-GUIDE: new references/surfaces/portfolio.md (Tile anatomy: title, role, one-line outcome).

**P4. Curate three to six projects.** Recent, relevant to the work you want next, ones you are proud of and would do again; no school work outside the target field, no non-design jobs, no "everything I ever made". Every extra piece raises the odds a reviewer opens a weak one.
- Sources: https://www.learnui.design/blog/how-create-ux-ui-portfolio-without-much-experience.html ; https://www.toptal.com/designers/ux/ux-designer-portfolios ; https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/ (three to five) ; https://www.youtube.com/watch?v=NGiQCBsVayI (description)
- Status: MISSING-GUIDE: references/surfaces/portfolio.md (Selection). Possible advisory later: more than 12 tiles on the home work grid.

**P5. Locked work is unseen work.** Reviewers rarely ask for passwords (one reviewer of many portfolios says he never once did); Toptal calls password walls bad UX. If work must be locked, show a public summary (problem, role, outcome) and offer an anonymized version; do not lock most of the grid.
- Sources: https://www.learnui.design/blog/how-create-ux-ui-portfolio-without-much-experience.html ; https://www.toptal.com/designers/ux/ux-designer-portfolios ; https://www.lisasuefischer.com/ (about 6 of 10 tiles locked)
- Status: MISSING-CHECK `portfolio-mostly-locked` (lint): more than half of the work tiles carry a lock marker (lock emoji U+1F512, an icon named lock, or text "password", "NDA", "protected") or link to a page with an `input[type=password]`. MISSING-GUIDE: surfaces/portfolio.md (NDA options: get a release date, rename and anonymize, fictionalize and label, logo only).

**P6. Label concept, unsolicited and fictionalized work up front.** An unsolicited redesign opens with a note that it is unsolicited and made without the company's context; NDA work rebuilt for a made-up company says so, including that its results are illustrative.
- Sources: https://www.learnui.design/blog/how-create-ux-ui-portfolio-without-much-experience.html ; https://priyanka.io/ ("LastPass, an unsolicited redesign" labeled in the title)
- Status: MISSING-GUIDE: commands/ux-case-study.md (Input: ask "real client, concept, unsolicited or fictionalized?" and print the label under the title) ; fits the existing "never invent metrics" rule.

**P16. The portfolio is itself judged as a UX project.** Working links and menus, no page that duplicates another (a Work page identical to Home), "see all" that shows more, nothing that reloads instead of navigating.
- Sources: https://www.toptal.com/designers/ux/ux-designer-portfolios
- Status: MISSING-CHECK `internal-link-broken` (render): crawl same-origin hrefs from the rendered page (depth 1), flag 4xx/5xx and anchors whose #id does not exist. Today `image-broken` covers failed resources only. A second, optional check `duplicate-page-content`: two internal routes whose main text is over 95 percent identical.

**P17. Real content without JavaScript and real metadata.** Seen in the list: a portfolio shipped as a bare create-react-app shell whose meta description is still "Web site created using create-react-app" and which shows nothing without JS; another whose title reads "One moment, please... Loader"; two Angular pages leaking an unrendered "{{ngMeta.description}}". Link previews, search and slow devices all see the broken version.
- Sources: https://danielautry.com/#portfolio ; https://pixeldahn.com/ ; https://www.bestfolios.com/casestudy ; https://www.bestfolios.com/resumes
- Status: MISSING-CHECK, four parts:
  - `meta-description-framework-default` (lint): `<meta name="description" content="Web site created using create-react-app">`, "Generated by create next app", "Vite App" and similar.
  - extend `title-is-a-framework-default` with loader titles (/^(loading|one moment|please wait)\b/i) and template tokens (`{{`, `{%`, `${`) in title or meta.
  - `social-meta-missing` (lint): a public page without `og:title`, `og:description`, `og:image` or `meta name=description` (guidance exists in foundations/seo.md "Open Graph (mandatory)", no check).
  - `js-only-content` (render): load with JavaScript disabled; flag when the page has no h1 and under 50 words of visible text.

**P18. Emoji and exclamation marks in titles and headings read as unprofessional to most reviewers.** Seen: a crown emoji and ten exclamation marks in a page title, a wave emoji in an h1. It can be a deliberate personality move; keep it advisory.
- Sources: https://www.elizabethylin.com/ ; https://www.verachen.me/ ; https://www.moritzoesterlau.de/
- Status: COVERED for headings and controls (`emoji-in-ui` matches h1 to h6). Gap: `<title>` is not in its scope; propose adding title to the existing rule rather than a new one (not counted as a new check).

**P19. Meta copy drifts from the page.** Seen: meta description says six years of experience while the page says ten. Facts in meta, OG and JSON-LD must come from current page copy.
- Sources: https://www.moritzoesterlau.de/
- Status: MISSING-CHECK `meta-claims-not-on-page` (lint): numeric tokens (with their unit word, such as "6 years", "120 clients") in meta description or og:description that do not appear in the visible text. MISSING-GUIDE: foundations/seo.md (write meta last, from the page).

**P20. A short, human About with a direct contact route.** Name, current role, location and a line of personality give interviewers a starting point; skip trivia lists and long skill bars.
- Sources: https://www.toptal.com/designers/ux/ux-design-job-interview-tips ; https://www.toptal.com/designers/ux/ux-designer-portfolios ; https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/
- Status: COVERED in part (portfolio-agency "About / team" and CTA band; footer contact). MISSING-CHECK `portfolio-no-contact` (lint): a page using the portfolio-agency sequence has no `mailto:` link, no link whose text or href says contact, LinkedIn or resume/CV, and no form. MISSING-GUIDE: surfaces/portfolio.md (About: three to five lines, skip skill bars).

**P21. Testimonials from named stakeholders strengthen a portfolio.**
- Sources: https://www.toptal.com/designers/ux/ux-designer-portfolios
- Status: COVERED (portfolio-agency "named testimonials with attribution"; `testimonial-fake-five-stars` blocks the fake kind).

**P22. Order work for the reader.** Lead with the project closest to the target employer's product and aesthetic; check what a non-designer picks as your best.
- Sources: https://dribbble.com/resources/career/ux-interview-questions ; https://michaeljanda.com/burnyourportfolio/ (description)
- Status: MISSING-GUIDE: surfaces/portfolio.md (Ordering).

**P23. Shot galleries are not product portfolios.** Dribbble and Behance profiles show finished visuals with no story; for product roles they supplement case studies, they do not replace them. Illustration and visual portfolios (titled pieces in a gallery) are the exception.
- Sources: https://dribbble.com/druids01 ; https://dribbble.com/naijatechguy ; https://janmraz.com/ ; https://www.cofolios.com/
- Status: COVERED for visual portfolios (data/industries.json media-photography-portfolio "gallery-first"; components art-portfolio-image-first). MISSING-GUIDE: surfaces/portfolio.md (product vs visual portfolio modes).

### 5b. The case study

**P7. Open with a summary block: role, team, timeline, tools, problem, outcome.** Every guide and template puts this first; reviewers scan for business impact in the first two paragraphs and for what you personally did. ux-skill's seven sections (About, Mission, Outcomes, Impact, Market, Chance, Target Audience) have no Role section and put Impact fourth.
- Sources: https://careerfoundry.com/en/blog/ux-design/ux-case-study/ ; https://uxcel.com/blog/how-to-write-a-ux-case-study-in-5-steps ; https://www.linkedin.com/pulse/8-step-guide-write-amazing-ux-case-study-reetika-gupta-1c/ ; https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/ ; https://www.figma.com/community/file/1015129345947090766/Case-Study-Template ; https://www.toptal.com/designers/ux/ux-designer-portfolios ; https://www.toptal.com/designers/ux/ux-design-job-interview-tips ; https://www.springboard.com/blog/design/ui-portfolio/ (blocked)
- Status: MISSING-CHECK `case-study-summary-missing` (lint, on /ux-case-study output and pages tagged as case studies): the first 150 words contain no role statement (/\b(my role|role:|i (led|owned|designed)|as (the )?(lead|sole|senior))\b/i) or no outcome (a number with unit or an outcome verb such as shipped, launched, reduced, increased). MISSING-GUIDE: commands/ux-case-study.md and output/case-study-style.md: add a designer-portfolio section set with a summary block first.

**P8. Lead with business impact, then tell the story.** Impact framed against the original goal; a results preview at the top that links to the results section.
- Sources: Uxcel (above) ; Toptal interview tips (above) ; Adobe XD Ideas (above) ; https://lolajiang.com/index.html
- Status: MISSING-GUIDE: commands/ux-case-study.md (summary first; Impact cross-linked). Check folded into `case-study-summary-missing`.

**P9. No real numbers? Say how success would be measured.** Never invent; instead name the metric, the baseline and how it would be read.
- Sources: https://careerfoundry.com/en/blog/ux-design/ux-case-study/
- Status: COVERED for the ban (commands/ux-case-study.md "No invented metrics"); MISSING-GUIDE for the replacement: ux-case-study.md Error Handling ("Impact metrics requested but none are real": write the measurement plan, not only qualitative notes).

**P10. One idea per section: one or two short paragraphs and one visual.** A reader who only reads, or only looks at the images, should still follow the story; scannable headers and lists; quality over quantity of artifacts; keep extra deliverables for the interview.
- Sources: CareerFoundry case study (above) ; LinkedIn (above) ; https://www.toptal.com/designers/ux/ux-designer-portfolios ; https://uxdesign.cc/case-study-template-8832941a9d1b (blocked; description) ; https://www.youtube.com/watch?v=d8FtsgQyGXw (description)
- Status: COVERED in part (case-study-style.md "Length Discipline", 65-character measure). MISSING-CHECK `case-study-wall-of-text` (lint or render): any section of a case study with more than 250 words and no img, figure, video or table.

**P11. Show the path, including the turns that failed.** Alternatives explored, early tests, constraints, a setback and how it was resolved, and what you would do next. Interviewers ask "tell me about a time it went wrong" in most loops; the case study should already hold that story.
- Sources: CareerFoundry case study (above) ; https://ixdf.org/literature/topics/ux-case-studies ; https://dribbble.com/resources/career/ux-interview-questions ; https://careerfoundry.com/en/blog/ux-design/make-sure-you-can-answer-these-11-ux-design-interview-questions/ ; https://uxdesign.cc/how-to-write-a-case-study-1b1b5f5e3e2c (blocked; description) ; https://www.youtube.com/watch?v=ptnYGRPlzN8 (description)
- Status: MISSING-GUIDE: commands/ux-case-study.md (sections for Process, Iterations, Learnings; today only (F) Chance touches risk).

**P12. Annotate the visuals.** Call-outs on screenshots that point at the decision and the reason; annotated wireframes beat polished-but-mute mockups. Citing a standard (WCAG, HIG, Material) is a valid reason.
- Sources: https://www.learnui.design/blog/how-create-ux-ui-portfolio-without-much-experience.html ; https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/ ; CareerFoundry case study (above)
- Status: MISSING-GUIDE: output/case-study-style.md (Image Handling: annotated call-outs). Conflict: case-study-style.md Pre-Publish Checklist forbids "name-checked authorities, inline citations"; for portfolio case studies a cited standard is part of the argument. Recommend relaxing that item in a portfolio mode.

**P13. Write for a non-designer reader.** Recruiters and HR screens often read first; plain words, outcome first, no method jargon without a reason.
- Sources: https://dribbble.com/resources/career/ux-interview-questions ; https://www.toptal.com/designers/ux/ux-design-job-interview-tips
- Status: COVERED (output/case-study-style.md Voice; commands/ux-case-study.md "Direct, declarative voice", banned inflation words).

**P14. Show the visual work as it really looks.** A design portfolio is judged on visual craft, so screens appear in color, at full resolution, with motion where it matters (GIF or video of the final flow). This conflicts with case-study-style.md Image Handling, which converts every screenshot to grayscale.
- Sources: https://www.toptal.com/designers/ux/ux-designer-portfolios (animated or interactive views strengthen a case study) ; https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/ (final mockups or GIFs) ; Behance case studies 2059 to 2061 (descriptions)
- Status: MISSING-GUIDE: output/case-study-style.md (keep the monochrome document chrome, exempt the work images in a portfolio mode). Blurry or stretched screenshots are inventory rows E15 and E16 (proposed render checks, not new here).

**P15. Typos get portfolios rejected.** Proofread; a spell pass is cheap.
- Sources: https://www.linkedin.com/pulse/8-step-guide-write-amazing-ux-case-study-reetika-gupta-1c/
- Status: MISSING-CHECK `spelling-suspect` (lint or complaints probe, advisory): run visible text through a dictionary (hunspell or a bundled word list) after removing brand names from the project's tokens and README; report unknown lowercase words seen once.

**P24. The case study can come with a talk track.** Interviews ask for a 10 to 15 minute walkthrough of one project; the same structure (problem, role, process, decision, outcome, learning) becomes the slides.
- Sources: https://www.youtube.com/watch?v=ZVZfWfqmRBY ; https://www.youtube.com/watch?v=hx7XyA8RNIw (descriptions) ; https://dribbble.com/resources/career/ux-interview-questions
- Status: MISSING-GUIDE: commands/ux-case-study.md (optional "presentation outline" output after the document).

**P25. A designer-process section set.** The list's own final-project brief asks for: problem statement, user research, personas, journey map, user flows, wireframes, visual design, usability testing, reflection, plus a design system (type, color, layout, components); the Figma template adds overview, roles, tools and duration, goals and findings. ux-skill's A to G set suits a product launch write-up, not a designer's portfolio piece. case-study-style.md already allows a different section set with codes that still march, so this is a second preset, not a rewrite.
- Sources: README lines 2067 to 2132 (Project Tasks #4 and #5) ; https://www.figma.com/community/file/1015129345947090766/Case-Study-Template ; https://www.figma.com/community/file/949395060452790372/Case-Study-Template---Creative-Ferry ; https://uxplanet.org/ux-portfolio-case-study-template-plus-examples-from-successful-hires-86d5b0faa2d6 (blocked) ; videos 2048, 2050, 2051 (descriptions)
- Status: MISSING-GUIDE: commands/ux-case-study.md (a `--portfolio` preset: (A) Summary, (B) Problem, (C) Users and research, (D) Process and iterations, (E) Solution, (F) Outcome, (G) Learnings).

---

## 6. Career development: what should shape the skill's advice

Most career links (job boards, freelance marketplaces, communities, social profiles, donation pages) hold nothing for a design tool; they are recorded out of scope in the ledger. Four lessons carry over.

**C1. Ask before solving.** Design exercises and whiteboard rounds test whether you clarify users, goals and constraints before drawing; the same discipline ux-skill applies to briefs.
- Sources: https://productdesigninterview.com/solving-product-design-exercises (description) ; https://www.coursera.org/articles/ux-designer-interview-questions-and-answers
- Status: COVERED (process/discovery-protocol.md "ask first, never improvise").

**C2. "How would you improve our product?" is a critique.** Frame it with heuristics and evidence, not taste.
- Sources: Coursera (above) ; https://uxbeginner.com/the-4-types-of-ux-interview-questions-to-master/
- Status: COVERED (commands/ux-critique.md ; laws/nielsen-heuristics.md).

**C3. A portfolio project can be built with a one-person sprint.** Map, sketch, decide, prototype, test, done alone, gives a beginner a complete case study arc.
- Sources: https://sprintstories.com/i-ran-a-one-person-google-design-sprint-to-create-my-ux-ui-design-portfolio-4661c3e97858 (unreachable; description) ; https://www.learnui.design/blog/how-create-ux-ui-portfolio-without-much-experience.html (project sources: wish-it-existed apps, side projects, non-profits, labelled unsolicited redesigns)
- Status: MISSING-GUIDE: references/process/design-sprint.md (solo variant) and surfaces/portfolio.md (Finding projects).

**C4. A resume page prints.** Resume galleries show one-page, scannable CVs; a resume or CV route on a portfolio site is printed or saved as PDF.
- Sources: https://www.bestfolios.com/resumes ; cover letter box (README line 2189, mirror only)
- Status: MISSING-CHECK `resume-page-no-print-styles` (lint): a route or file named resume, cv or curriculum with no `@media print` rule and no linked PDF.

---

## 7. Non-link content in the block

- ChatGPT prompt table (lines 1794 to 1816): 16 prompt templates (copy, wireframe layout, usability test methods, user story, persona, IA flowchart, palette, handoff topics, presentation format, user flow from research, UX ideas, error message, product brief, Dribbble hook, demographics, button documentation). Lessons A6 and A7. The error-message prompt is consistent with ux-skill's error copy rules (foundations/copy.md "Error message specificity").
- Project Tasks #4 and #5 (lines 2067 to 2132): case study tasks with Figma templates, and a final brief requiring a voice interface (optional AR/VR) or an accessible wellness product, with a design system and a nine-section case study. Lessons P25 and ST15.
- Resume and cover letter boxes (lines 2174 to 2193): Bestfolios resume gallery and a cover-letter file mirror. Lesson C4.

---

## Counts

- Lessons: 77 (V 15, S 9, A 9, ST 15, P 25, C 4), after merging duplicates across links (for example V7 and A8 share one check; P8 folds into P7's check; the 5-user rule, interview method and Lean UX points merge into existing files).
- Status per lesson, counted once by its strongest gap (check over guide over covered; several lessons carry both a check and a guide):
  - MISSING-CHECK: 21 lessons (V1, V5, V7, V8, V13, S1, S8, ST9, ST15, P1, P2, P3, P5, P7, P10, P15, P16, P17, P19, P20, C4)
  - MISSING-GUIDE: 39 lessons
  - COVERED: 17 lessons (A1, A3, A5, A7, A9, ST3, ST5, ST6, ST8, ST10, ST13, ST14, P13, P18, P21, C1, C2)
- New checks: 24 new rule ids plus 2 extensions of existing rules (table below).
- New guidance: 4 new reference files and additions to 10 existing files.

### New checks (24 new ids, 2 extensions)

| # | id | kind | lesson | detection (one line) |
|---|---|---|---|---|
| 1 | voice-input-no-text-fallback | lint | V1 | SpeechRecognition or a mic-named button in a form/region with no text input or textarea |
| 2 | mic-button-no-listening-state | lint | V5 | mic-named button without aria-pressed and no aria-live/role=status in the component |
| 3 | assistant-dead-end-fallback | lint (text) | V7, A8 | "I didn't understand" style string with no sibling buttons, links or option list |
| 4 | speech-autoplay-on-load | lint | V8 | speechSynthesis.speak reachable from load or empty-deps useEffect, not from a user event |
| 5 | distance-text-too-small | render, tv/hub/kiosk briefs only | V13 | visible text under 24px, headings under 32px at 1280x720 and 1920x1080 |
| 6 | autorotate-without-reduced-motion | lint | S1 | autoRotate true, model-viewer auto-rotate, or tweened camera.position with no prefers-reduced-motion in scripts |
| 7 | webxr-without-support-check | lint | S8 | navigator.xr.requestSession without isSessionSupported |
| 8 | nav-label-destination-mismatch | lint, multi-page | ST9 | nav link text shares no content word with the target page h1/title |
| 9 | icon-meaning-reused | lint | ST15 | same SVG path hash or icon import in two controls whose names share no word |
| 10 | portfolio-hero-no-role | lint or render | P1 | first-viewport h1 plus first paragraph has no role noun, or is a bare greeting |
| 11 | portfolio-work-below-fold | render | P2 | first work tile top below 1.5 viewport heights at 1280x800 or 390x844 |
| 12 | work-tile-image-only | lint | P3 | work-grid link or card containing only img/picture, no heading or 3+ word text |
| 13 | portfolio-mostly-locked | lint | P5 | over half of work tiles carry a lock marker or lead to a password input |
| 14 | internal-link-broken | render | P16 | depth-1 crawl of same-origin hrefs: 4xx/5xx or missing #id targets |
| 15 | duplicate-page-content | render (optional) | P16 | two internal routes with main text over 95 percent identical |
| 16 | meta-description-framework-default | lint | P17 | meta description equals a scaffold default ("Web site created using create-react-app", etc.) |
| 17 | social-meta-missing | lint | P17 | public page lacks og:title, og:description, og:image or meta description |
| 18 | js-only-content | render | P17 | with JS disabled: no h1 and under 50 visible words |
| 19 | meta-claims-not-on-page | lint | P19 | number plus unit in meta/OG description absent from visible text |
| 20 | portfolio-no-contact | lint | P20 | portfolio sequence page with no mailto, contact/LinkedIn/resume link or form |
| 21 | case-study-summary-missing | lint | P7, P8 | first 150 words of a case study lack a role statement or an outcome |
| 22 | case-study-wall-of-text | lint or render | P10 | case-study section over 250 words with no img, figure, video or table |
| 23 | spelling-suspect | lint or probe, advisory | P15 | dictionary pass over visible text, brand tokens excluded |
| 24 | resume-page-no-print-styles | lint | C4 | resume/cv route with no @media print and no linked PDF |
| E1 | title-is-a-framework-default (extend) | lint | P17 | add loader titles (Loading, One moment, Please wait) and unrendered template tokens in title/meta |
| E2 | emoji-in-ui (extend) | lint | P18 | add title to the rule's element scope |

Complaints probes: each render rule above becomes a `rule-clear` probe target once added to `_RULES` (per the inventory's note); until then `text-absent` can hold rows 3 and 16.

### New guidance targets

- New files: references/foundations/voice-and-multimodal.md (V2 to V6, V9 to V15) ; references/conditional/spatial.md (S2 to S7, S9) ; references/surfaces/portfolio.md (P3 to P5, P20, P22, P23, C3) ; references/process/design-sprint.md (ST12, C3).
- Additions: foundations/ai-interfaces.md (A2, A4, A8 Repair) ; commands/ux-research.md (A6, ST2) ; process/lean-ux-klein.md (A6) ; process/discovery-protocol.md (ST1) ; commands/ux-audit.md (ST4) ; foundations/component-behaviors.md (ST11 Search) ; foundations/responsive.md (V13) ; foundations/seo.md (P19) ; commands/ux-case-study.md (P6, P7, P8, P9, P11, P24, P25, ST7) ; output/case-study-style.md (P7, P12, P14 and the two conflicts).

### Conflicts found with current ux-skill text

1. output/case-study-style.md converts all screenshots to grayscale. For a designer's portfolio case study this hides the evidence (P14). Keep monochrome chrome; exempt work images in a portfolio mode.
2. output/case-study-style.md forbids name-checked authorities and inline citations. Portfolio guides recommend citing WCAG or HIG as the reason for a decision (P12).
3. commands/ux-case-study.md section set A to G has no Role and puts Impact fourth; every portfolio source puts role and outcome in the opening summary (P7, P8).

---

# Part 2. Ledger

## Part 2a. Ledger: every unique link (206)

Columns: id, README line, title, URL, type, status, one-line takeaway. Status values: read; summarized from description (books, videos); blocked, summarized from description (403 or similar to both curl and WebFetch); out of scope; dead. Every video was confirmed live through YouTube oEmbed. Lesson ids in takeaways point to part 1.

| id | line | title | URL | type | status | takeaway |
|---|---|---|---|---|---|---|
| 000 | 1673 | Designing Voice User Interfaces: Principles of Conversational Experiences | https://books.google.com/books/about/Designing_Voice_User_Interfaces.html?id=MmnEDQAAQBAJ | book | summarized from description | Cathy Pearl's VUI primer (publisher page): conversation design basics, choosing a recognizer, measuring VUI performance; source for voice-first rules V1 to V7. |
| 001 | 1674 | Voice User Interface Design: Moving from GUI to Mixed Modal Interaction | https://books.google.com/books/about/Voice_User_Interface_Design.html?id=Q3B_DwAAQBAJ | book | summarized from description | Dasgupta (publisher page): moving from GUI to mixed-modal GUI plus voice; supports multimodal fallback (V1). |
| 002 | 1675 | Conversational UX Design: A Practitioner's Guide to the Natural Conversation Framework | https://dl.acm.org/doi/book/10.1145/3304087 | book | blocked, summarized from description | ACM page blocked (403). Per publisher and paper summaries: Natural Conversation Framework, expandable sequences, 100 patterns, six basic user navigation actions incl. repair; source for A8/V7. |
| 003 | 1681 | A Definitive Guide to Voice User Interface Design | https://userguiding.com/blog/voice-user-interface | article | read | Voice process: journey map with voice as a channel, device persona, competitor review, dialog scripts, intent/utterance/slot anatomy, role-play testing. |
| 004 | 1682 | What are Voice User Interfaces? | https://ixdf.org/literature/topics/voice-user-interfaces | article | read | IxDF: no visual affordances in voice, so state options, say what function is active, cap information to what can be remembered (V2, V11). |
| 005 | 1683 | Everything You Want To Know About Creating Voice User Interfaces | https://www.smashingmagazine.com/2022/02/voice-user-interfaces-guide/ | article | read | Smashing (Kuznetsov): richest voice source. One-breath responses, max 3 options, 500ms pause, 8 to 10s timeout, explicit vs implicit confirmation, repeat, 32pt/24pt at 1 to 3m distance. |
| 006 | 1684 | Voice User Interface Design, Examples & Advantages of VUI | https://www.boldare.com/blog/what-is-voice-user-interface/ | article | read | Boldare: when to use voice, speech is resource-intensive, privacy and misrecognition risks; general overview. |
| 007 | 1685 | VUI: Designing for Voice UI | https://www.uxpin.com/studio/blog/voice-user-interface/ | article | read | UXPin: prompts vs statements, max three options, natural re-prompts, wake and listening microinteractions (LED, sound, animation), personas with speech patterns. |
| 008 | 1686 | Designing a VUI to Voice User Interface | https://www.toptal.com/designers/ui/designing-a-vui | article | read | Toptal VUI (via WebFetch): required vs optional slots, confirm completion aloud, no-match and no-input paths, extra auth for payments, keep companion screen simple. |
| 009 | 1687 | Designing Voice Experience | https://uxdesign.cc/voice-user-experience-design-and-prototyping-for-mere-mortals-ef080c843640 | article | blocked, summarized from description | uxdesign.cc blocked (403). Per list description: practitioner lessons from Fortune 500 speech apps; no unique lesson recoverable. |
| 010 | 1693 | The Voice Design Process For Voice User Interfaces (VUIs) | https://www.youtube.com/watch?v=8OXN0ZDpwrM | video | summarized from description | CareerFoundry video (oEmbed live): a voice design process; supports V13 process. |
| 011 | 1694 | How to Improve Voice User Interface Design | https://www.youtube.com/watch?v=vKM4OMz8qmQ | video | summarized from description | SoundHound video (oEmbed live): improving VUI; vendor talk, no unique lesson. |
| 012 | 1695 | Designing Voice User Interfaces" | https://www.youtube.com/watch?v=RdCmMMwaFRs | video | summarized from description | Cathy Pearl talk (oEmbed live): conversation design best practices; duplicates book 000. |
| 013 | 1715 | 3D User Interfaces: Theory and Practice | https://books.google.com/books/about/3D_User_Interfaces.html?id=fxWSDgAAQBAJ | book | summarized from description | LaViola et al. (publisher page): 3D UI theory and practice, the standard 3D interaction reference; supports spatial guide S2 to S4. |
| 014 | 1716 | Virtual & Augmented Reality for Dummies | https://books.google.com/books/about/Virtual_Augmented_Reality_For_Dummies.html?id=KrBfDwAAQBAJ | book | summarized from description | VR and AR for Dummies (publisher page): hardware-neutral primer; no design rule. |
| 015 | 1717 | Learning Virtual Reality: Developing Immersive Experiences and Applications for Desktop, Web, and Mobile | https://books.google.com/books/about/Learning_Virtual_Reality.html?id=T5XtrQEACAAJ | book | summarized from description | Learning Virtual Reality (publisher page): desktop, mobile and web VR development; supports S10 WebXR fallback. |
| 016 | 1718 | Oculus Rift in Action | https://www.manning.com/books/oculus-rift-in-action | book | summarized from description | Oculus Rift in Action (Manning page): SDK programming; out of scope for design rules beyond comfort. |
| 017 | 1719 | A Design Model and Methodology for Developing Virtual Reality Interfaces | http://www.cs.tufts.edu/~jacob/papers/vrst01.tanriverdi.pdf | article | read | VRID paper (PDF read): decompose VR interfaces into objects with graphics, behaviors (physical vs magical, simple vs composite), interactions, communications; high then low level spec (S8). |
| 018 | 1725 | Leap Into VR/AR Design | https://www.toptal.com/designers/ui/vr-ar-design-guide | article | read | Toptal VR/AR (via WebFetch): world-locked vs follow-along UI, larger thicker fonts on low-res headsets, design per platform input set, hints and feedback for every interaction. |
| 019 | 1726 | Introduction - The Design of Virtual and Augmented Reality | https://aliheston.gitbook.io/the-design-of-virtual-and-augmented-reality | article | read | Heston gitbook (intro read): curated VR/AR knowledge base; design for whole bodies and diverse people; index only. |
| 020 | 1727 | UI/UX: Designing for AR & VR | https://uxplanet.org/ui-ux-designing-for-ar-vr-8c695caccc5e | article | blocked, summarized from description | uxplanet blocked (403). Per list description: AR vs VR primer; no unique lesson recoverable. |
| 021 | 1728 | The hierarchy of needs in virtual reality development | https://medium.com/@beaucronin/the-hierarchy-of-needs-in-virtual-reality-development-4333a4833acc | article | blocked, summarized from description | Medium blocked (403). Per secondary summaries: Maslow-style VR hierarchy with comfort as the base layer (S1). |
| 022 | 1729 | Speculations on neuro-motivated design for VR | https://medium.com/@beaucronin/speculations-on-neuro-motivated-design-for-vr-3f26685c5c40 | article | blocked, summarized from description | Medium blocked (403). Per list description: humans are strong at 3D navigation; speculative, no rule. |
| 023 | 1730 | From Product Design to Virtual Reality | https://medium.com/google-design/from-product-design-to-virtual-reality-be46fa793e9b | article | blocked, summarized from description | Medium blocked (403). Per list description: a Google product designer moving from Inbox to VR; no rule recoverable. |
| 024 | 1731 | Immersive Design | https://medium.com/backchannel/immersive-design-76499204d5f6#.rw8u2q3gp | article | blocked, summarized from description | Medium blocked (403). Per list description: immersive design essay; no rule recoverable. |
| 025 | 1732 | 5 Lessons I Learned From Designing the VRUI of Beloola | https://medium.com/beloola-all-our-news-updates/5-lessons-i-learned-from-designing-the-vrui-of-beloola-754f16062c0b#.evgt1cepa | article | blocked, summarized from description | Medium blocked (403). Per list description: lessons from a social VR UI (Beloola); no rule recoverable. |
| 026 | 1733 | The UX of VR | https://www.creativebloq.com/ux/the-user-experience-of-virtual-reality-31619635 | article | read | Creative Bloq (UNIT9): user controls movement, no automated zooms, fade to black when tracking breaks, UI at the depth of its target, no HUD, spatial audio cues, safe play space. |
| 027 | 1734 | Designing VR UI in Figma and testing it with no code | https://uxdesign.cc/lets-design-xr-ui-in-figma-and-bring-it-to-xr-with-no-code-a123b9b647ab | article | blocked, summarized from description | uxdesign.cc blocked (403). Per list description: design XR UI in Figma and test with no code (S9). |
| 028 | 1740 | VR Interface Design Pre-Visualisation Methods | https://www.youtube.com/watch?v=id86HeV-Vb8 | video | summarized from description | Mike Alger (oEmbed live): pre-visualising VR interfaces before building (S9). |
| 029 | 1741 | UI/UX design for WebVR | https://www.youtube.com/watch?v=ZOaOYTOpwyM | video | summarized from description | Josh Carpenter, Mozilla (oEmbed live): UX for WebVR on the open web (S10). |
| 030 | 1742 | Google I/O 2015 - Designing for virtual reality | https://www.youtube.com/watch?v=Qwh1LBzz3AU&t=488s | video | summarized from description | Google I/O 2015 (oEmbed live): VR adds physiological and ergonomic constraints (S1). |
| 031 | 1743 | Oculus Connect 2: Navigating New Worlds: Designing UI and UX in VR | https://www.youtube.com/watch?v=braV_c4M8oI | video | summarized from description | Oculus Connect 2 (oEmbed live): navigating VR worlds; comfort and locomotion (S1). |
| 032 | 1744 | How to Prototype AR and VR UI/UX with FIGMA and UNITY! (Tutorial) | https://www.youtube.com/watch?v=mW8tRQRQD74 | video | summarized from description | Figma plus Unity tutorial (oEmbed live): field of vision, comfort, exporting UI to a headset (S9). |
| 033 | 1745 | Designing for AR - UX/UI Case Study | https://www.youtube.com/watch?v=v0c5P3prpMM | video | summarized from description | AR skateboarding case study (oEmbed live): concept AR view screen; example of a spatial case study. |
| 034 | 1746 | Building a VR app in Figma | https://www.youtube.com/watch?v=nmlWiK9AokE | video | summarized from description | Building a VR app in Figma (oEmbed live): tool tutorial (S9). |
| 035 | 1752 | Unity | https://unity.com/ | tool | read | Unity (homepage): real-time 3D engine for AR/VR builds; tool, no rule. |
| 036 | 1771 | Machine Learning Design Patterns | https://books.google.com/books/about/Machine_Learning_Design_Patterns.html?id=dDwDEAAAQBAJ | book | summarized from description | Machine Learning Design Patterns (publisher page): 30 engineering patterns incl. explainability and fairness; engineering-side, informs A9. |
| 037 | 1772 | Designing Human-Centric AI Experiences: Applied UX Design for Artificial Intelligence (Design Thinking) | https://www.goodreads.com/en/book/show/61514121-designing-human-centric-ai-experiences | book | summarized from description | Designing Human-Centric AI Experiences (Goodreads): AI systems change over time while their UX often does not adapt (A4). |
| 038 | 1778 | Design for AI: What should people who design AI know? | https://uxdesign.cc/design-for-ai-what-should-people-who-design-ai-know-761e78fdabb | article | blocked, summarized from description | uxdesign.cc blocked (403). Per list description: what AI designers should know; overlaps ai-interfaces.md. |
| 039 | 1779 | ML+DESIGN | https://machinelearning.design/ | article | read | ML+Design (homepage read, JS index): curated resource list; no rule. |
| 040 | 1780 | The Present and Future of AI in Design (with Infographic) | https://www.toptal.com/designers/product-design/infographic-ai-in-design | article | read | Toptal AI in design (via WebFetch): AI as augmentation, propose then human approves or adjusts, keep output on the design system (A3, A5). |
| 041 | 1781 | 7 Ways to Get Started Designing for AI/ML Products | https://uxplanet.org/7-ways-to-get-started-designing-for-ai-ml-products-bef764ca1b27 | article | blocked, summarized from description | uxplanet blocked (403). Per list description: getting started on AI/ML products; overlaps ai-interfaces.md. |
| 042 | 1782 | Machine Learning for Designers | https://www.oreilly.com/radar/machine-learning-for-designers/ | article | read | O'Reilly ML for Designers: ML is often right about hard things, not always right about easy ones; use ML only where conventional logic fails (A1, A2). |
| 043 | 1783 | Design for Machine Learning | https://uxdesign.cc/becoming-a-machine-learning-designer-42920afeeb28 | article | blocked, summarized from description | uxdesign.cc blocked (403). Per list description: ideating ML product offerings; no rule recoverable. |
| 044 | 1789 | AI & Machine Learning Will Change UX Research & Design | https://www.youtube.com/watch?v=mBu_LmD69tc | video | summarized from description | NN/g Jakob Nielsen (oEmbed live): AI's effect on UX research and design; opinion. |
| 045 | 1790 | Designing AI Experiences | https://www.youtube.com/watch?v=AAJ2vQXm5HQ | video | summarized from description | Adrian Zumbrunnen, awwwards (oEmbed live): designing AI experiences, conversational UI; overlaps ai-interfaces.md. |
| 046 | 1791 | Amazing New UX/UI Design Tools + AI Tools - August 2022 | https://www.youtube.com/watch?v=0uvu3TCyZN4 | video | summarized from description | Punit Chawla (oEmbed live): AI design tools roundup 2022; dated tool list. |
| 047 | 1835 | Starter Questions for User Research | https://projects.iq.harvard.edu/files/harvarduxgroup/files/ux-research-guide-sample-questions-for-user-interviews.pdf | other | blocked, summarized from description | Harvard UX group PDF blocked (403). Per list description: starter questions for user interviews; covered by lean-ux-klein.md interviews. |
| 048 | 1836 | UX Strategy: How to Devise Innovative Digital Products that People Want | https://jaimelevy.com/ux-strategy-book/ | book | read | Jaime Levy (author page and free chapters read): UX strategy = business strategy + value innovation + validated user research + frictionless UX (ST1). |
| 049 | 1837 | Designing Search: UX Strategies for eCommerce Success | https://www.wiley.com/en-ae/Designing+Search%3A+UX+Strategies+for+eCommerce+Success-p-9781118109953 | book | summarized from description | Nudelman, Designing Search (Wiley page): ecommerce search patterns, integrating search with browse (ST11). |
| 050 | 1838 | Lean UX: Designing Great Products with Agile Teams | https://leanuxbook.com/ | book | summarized from description | Lean UX site (Gothelf, Seiden): outcomes over output; already distilled in process/lean-ux-gothelf.md. |
| 051 | 1844 | How to nail your UX research strategy | https://maze.co/guides/ux-research/ux-research-strategy/ | article | read | Maze: research strategy questions (who, why, what, when, business link), research tied to product phase (ST3). |
| 052 | 1845 | How to Conduct User Experience Research Like a Professional | https://careerfoundry.com/en/blog/ux-design/how-to-conduct-user-experience-research-like-a-professional/ | article | read | CareerFoundry research: never test on yourself, methods by behavioral vs attitudinal and qual vs quant (ST5, ST6). |
| 053 | 1846 | The Ultimate Guide to UX Research Strategy | https://www.userinterviews.com/blog/the-ultimate-guide-to-ux-research-strategy | article | read | User Interviews: research strategy, stakeholder types, align metrics, store findings (ST3). |
| 054 | 1847 | How To Do A UX Competitor Analysis: A Step By Step Guide | https://usabilitygeek.com/how-to-do-ux-competitor-analysis/ | article | read | UsabilityGeek: competitor matrix of 5 to 10 direct and indirect rivals, list tasks and journeys, present impact not findings, avoid endless lists (ST2). |
| 055 | 1848 | UX analysis: best methods and key tools | https://contentsquare.com/guides/ux/analysis/ | article | read | Contentsquare: pair quant (heatmaps, surveys) with qual (replays, tests); prioritize fixes by severity then impact vs effort (ST4, ST5). |
| 056 | 1854 | Strategic & Reactionary User Research | https://www.youtube.com/watch?v=Kj16KEqHsy4 | video | summarized from description | NN/g (oEmbed live): strategic vs reactionary research; plan research before the sprint (ST3). |
| 057 | 1855 | What's UX Strategy? And Why You Should Have It In Place? | https://www.youtube.com/watch?v=iTYulrROJP8 | video | summarized from description | Koru UX (oEmbed live): UX strategy as a roadmap before building (ST1). |
| 058 | 1856 | How to create a UX Research Report to free template included! | https://www.youtube.com/watch?v=esg5iUALAJM | video | summarized from description | femke.design (oEmbed live): research report template; covered by lean-ux-klein.md Reporting research. |
| 059 | 1875 | Content Strategy for the Web | https://www.peachpit.com/store/content-strategy-for-the-web-9780132883238 | book | summarized from description | Halvorson, Content Strategy for the Web (publisher page): content processes, people and governance (ST9). |
| 060 | 1876 | Content Strategy at Work. Real-world Stories to Strengthen Every Interactive Project | https://shop.elsevier.com/books/content-strategy-at-work/bloomstein/978-0-12-391922-9 | book | summarized from description | Bloomstein, Content Strategy at Work (publisher page): real-world content strategy stories (ST9). |
| 061 | 1882 | Content 101: Information Architecture | https://www.bynder.com/en/blog/content-101-information-architecture/ | article | blocked, summarized from description | Bynder blocked (403). Per list description: IA is a team process; overlaps Toptal IA. |
| 062 | 1883 | What is Content Strategy in UX? | https://technicalwriterhq.com/content/content-strategy/content-strategy-in-ux/ | article | read | TechnicalWriterHQ: content audit, terminology list, voice and tone rules, content patterns, governance so wording does not drift (ST9). |
| 063 | 1884 | The Comprehensive Guide to Information Architecture | https://www.toptal.com/designers/ia/guide-to-information-architecture | article | read | Toptal IA (via WebFetch): structure over hierarchy, most-used features most prominent, every step logical, legend and labelled lines in flow diagrams (ST10). |
| 064 | 1890 | Full Workshop: Content Strategy & Information Architecture | https://www.youtube.com/watch?v=j0y8YBhDjIA | video | summarized from description | Flux Academy workshop (oEmbed live): content strategy and IA basics (ST9, ST10). |
| 065 | 1891 | Plan Before You Build: Information Architecture & Content Strategy | https://www.youtube.com/watch?v=OPHfDVWyuZU | video | summarized from description | Pods Framework (oEmbed live): plan the content model before building; reuse content (ST9). |
| 066 | 1892 | Case Study: The Role of Information Architecture in Adaptive Content Strategy | https://www.youtube.com/watch?v=6yVDY3bGxz8 | video | summarized from description | Precision Content case (oEmbed live): adaptive, componentised content authoring (ST9). |
| 067 | 1911 | Design Sprint: A Practical Guidebook for Creating Great Digital Products | https://books.google.com/books/about/Design_Sprint.html?id=mCKsAQAACAAJ | book | summarized from description | Banfield et al., Design Sprint (publisher page): prototype and test an idea within a week (ST12). |
| 068 | 1912 | Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days | https://www.character.vc/sprint | book | summarized from description | Knapp, Sprint (book site): small team, cleared week, prototype tested with real customers (ST12). |
| 069 | 1913 | UX for Lean Startups: Faster, Smarter User Experience Research and Design | https://www.goodreads.com/book/show/16128986-ux-for-lean-startups | book | summarized from description | Klein, UX for Lean Startups (Goodreads): fast, cheap research and design; distilled in process/lean-ux-klein.md. |
| 070 | 1919 | What's a Design Sprint and why is it important? | https://uxplanet.org/whats-a-design-sprint-and-why-is-it-important-f7b826651e09 | article | blocked, summarized from description | uxplanet blocked (403). Per list description: notes from a design sprint masterclass (ST12). |
| 071 | 1920 | Design Sprints | https://ixdf.org/literature/topics/design-sprints | article | read | IxDF design sprints: unpack, sketch, decide, prototype, test; pros and cons (ST12). |
| 072 | 1921 | What Are Design Sprints? | https://careerfoundry.com/en/blog/ux-design/what-are-design-sprints/ | article | read | CareerFoundry sprints: map, sketch, decide, prototype, validate; remote sprint prep (ST12). |
| 073 | 1922 | I ran a one-person Design Sprint to create my UX/UI design portfolio | https://sprintstories.com/i-ran-a-one-person-google-design-sprint-to-create-my-ux-ui-design-portfolio-4661c3e97858 | article | blocked, summarized from description | sprintstories.com unreachable (connection reset, 503 via WebFetch). Per list description: a one-person sprint used to build a portfolio (ST14). |
| 074 | 1923 | How to Conduct an Effective Design Sprint | https://www.toptal.com/designers/product-design/effective-design-sprint | article | read | Toptal sprint (via WebFetch): roles incl. a decider, HMW voting, Crazy 8s, five-act test interview, schedule testers early (ST12). |
| 075 | 1924 | The UX Sprint | https://boanastudio.com/blog/ux-design-sprint-digital-products | article | read | Boana Studio: a 10-day UX sprint variant with story map, UX/UI reviews, test day and handover to a design system (ST12). |
| 076 | 1930 | UX vs Design Thinking vs Design Sprint | https://www.youtube.com/watch?v=Kma42sfOZds | video | summarized from description | vaexperience (oEmbed live): UX vs design thinking vs sprints; framing only. |
| 077 | 1931 | An Introduction To Design Thinking & Design Sprints | https://www.youtube.com/watch?v=9lljOVfOi6o | video | summarized from description | CareerFoundry (oEmbed live): design thinking and sprints intro (ST12). |
| 078 | 1932 | What is a Design Sprint? | https://www.youtube.com/watch?v=xVvVaIWTuck | video | summarized from description | Grow with Google (oEmbed live): what a design sprint is (ST12). |
| 079 | 1933 | Design Sprint 2.0: Every Excercise | https://www.youtube.com/playlist?list=PLxk9zj3EDi0X5CgoFckoheIFAx-uT2i7j | video | read | AJ&Smart Design Sprint 2.0 playlist (page read): every exercise of the compressed 4-day sprint (ST12). |
| 080 | 1955 | Burn Your Portfolio | https://michaeljanda.com/burnyourportfolio/ | book | read | Burn Your Portfolio (author page read): working in design beyond the portfolio; clients, process, pricing; career, light on page design. |
| 081 | 1956 | Design Matters: Portfolios 01: An Essential Primer for Today's Competitive Market | https://books.google.com/books/about/Design_Matters.html?id=AEdMzQEACAAJ | book | summarized from description | Design Matters: Portfolios 01 (publisher page): portfolio as self-promotion; no rule. |
| 082 | 1957 | Stand Out: Design a personal brand. Build a killer portfolio. Find a great design job. | https://www.peachpit.com/store/stand-out-design-a-personal-brand.-build-a-killer-portfolio-9780134134086 | book | summarized from description | Stand Out (publisher page): personal brand, portfolio, job; supports P1 positioning. |
| 083 | 1958 | The Squiggly Career: Ditch the ladder, discover opportunity, design your career: The five skills you need to succeed in work today | https://www.penguin.co.uk/books/312993/the-squiggly-career-by-ellis-helen-tupper-and-sarah/9780241385845 | book | out of scope | Squiggly Career (publisher page): career self-reflection; out of scope for a design tool. |
| 084 | 1964 | Tips For Your First Great UX Portfolio | https://careerfoundry.com/en/tutorials/ux-design-for-beginners/tips-for-your-first-great-ux-portfolio/ | article | dead | CareerFoundry portfolio tips: page moved (redirect stub, target not found). |
| 085 | 1965 | The Best UX Designer Portfolios to Inspiring Case Studies and Examples | https://www.toptal.com/designers/ux/ux-designer-portfolios | article | read | Toptal portfolios (via WebFetch): curate few recent projects, problem, role, tools, results, learnings; no passwords; working nav, no duplicate pages (P4, P5, P7, P16). |
| 086 | 1966 | How To Build a UI Portfolio [2023 Career Guide] | https://www.springboard.com/blog/design/ui-portfolio/ | article | blocked, summarized from description | Springboard blocked (403). Per list description: show process and the value created (P7, P8). |
| 087 | 1967 | 110+ Essential User Experience Portfolios for Inspiration | https://uxplanet.org/110-curated-ux-portfolios-for-inspiration-492e6156ed2b | article | blocked, summarized from description | uxplanet blocked (403). Per list description: 110 portfolio links; inspiration list only. |
| 088 | 1968 | How to Create Your UX/UI Portfolio (Without Much Experience) | https://www.learnui.design/blog/how-create-ux-ui-portfolio-without-much-experience.html | article | read | Learn UI Design: project sources, NDA options (fictionalize and label, logo only), annotations justify decisions, cut work you would not repeat (P5, P6, P12, P4). |
| 089 | 1974 | My First UX Design Portfolio - Advice for Beginners | https://www.youtube.com/watch?v=NGiQCBsVayI | video | summarized from description | Tanya Niu (oEmbed live): first portfolio advice for beginners (P4). |
| 090 | 1975 | How to prepare your design portfolio / Design Tutorial | https://www.youtube.com/watch?v=emSv9TTHZVY | video | summarized from description | Cuberto (oEmbed live): present portfolio projects to generate leads (P3). |
| 091 | 1976 | How to Build a UX Design Portfolio Website with Notion for FREE [Step-by-Step Tutorial] | https://www.youtube.com/watch?v=t5OYI-IEkgU | video | summarized from description | Aliena Cai (oEmbed live): portfolio site in Notion; tool tutorial. |
| 092 | 1982 | Notion | https://www.notion.com/ | tool | out of scope | Notion homepage: general workspace product; out of scope as a rule source. |
| 093 | 1983 | Dribbble | https://dribbble.com/ | tool | out of scope | Dribbble homepage (202, bot check): shot-based showcase; out of scope (P24 note). |
| 094 | 1984 | Behance | https://www.behance.net/ | tool | out of scope | Behance homepage blocked (403): project showcase platform; out of scope as a rule source. |
| 095 | 1985 | Adobe Portfolio | https://www.adobe.com/products/portfolio.html | tool | out of scope | Adobe Portfolio blocked (Access Denied): hosted portfolio builder; out of scope. |
| 096 | 1991 | Rama Krushna | https://app.notion.com/p/Hey-I-m-Rama-Krushna-53ebad1b8bb04bd491108cac9c293be9 | other | dead | Rama Krushna Notion portfolio: link now resolves to the Notion marketing page, portfolio content gone. |
| 097 | 1992 | Cofolios - UX portfolios of interns at FAANG | https://www.cofolios.com/ | other | read | Cofolios: intern portfolios grouped by company and college; inspiration index. |
| 098 | 1993 | Lisa Fisher | https://www.lisasuefischer.com/ | other | read | Lisa Fischer: about 6 of 10 project tiles behind a lock icon; shows the cost of locked work (P5). |
| 099 | 1994 | Sasha | https://saschas.ai/ | other | read | Sasha Erman: one-line positioning plus project tiles that state scope and scale (4 billion users) (P1, P3). |
| 100 | 1995 | Gloria Lo | https://www.glorialo.design/ | other | read | Gloria Lo: hobby-led hero ("I design, sing, paint & write") before the role; weaker positioning (P1). |
| 101 | 1996 | Moritz Oesterlau | https://www.moritzoesterlau.de/ | other | read | Moritz Oesterlau: meta says six years, body says ten; stale meta drift (P19); emoji in intro. |
| 102 | 1997 | Elizabeth Lin | https://www.elizabethylin.com/ | other | read | Elizabeth Lin: JS-rendered; title carries an emoji and ten exclamation marks; personality over convention (P18). |
| 103 | 1998 | Olivia Truong | https://www.oliviatruong.design/ | other | read | Olivia Truong: role, years and sectors in meta; project tiles framed as user questions (P3). |
| 104 | 1999 | Priyanka Gupta (Medium profile) | https://medium.com/@priyankagupta.rj | other | blocked, summarized from description | Priyanka Gupta Medium profile blocked (403); see priyanka.io. |
| 105 | 1999 | Priyanka Gupta (site) | https://priyanka.io/ | other | read | Priyanka Gupta: positioning line, tiles by company with one-line scope, writing section incl. labelled unsolicited redesign (P1, P3, P6). |
| 106 | 2000 | Lola Jiang | https://lolajiang.com/index.html | other | read | Lola Jiang: tiles lead with outcomes and real numbers (91.7% CSAT, 30% revenue) (P3, P8). |
| 107 | 2001 | Druids | https://dribbble.com/druids01 | other | read | Druids Dribbble: shot grid, visual-only; no case narrative (P24). |
| 108 | 2002 | Daniel Autry | https://danielautry.com/#portfolio | other | read | Daniel Autry: client-only React shell with the create-react-app default meta description and no content without JS (P17). |
| 109 | 2003 | Sara Soueidan (SVG demo) | https://svg-animations.surge.sh/ | other | read | Sara Soueidan SVG demo: animation demo page, title only; demo not portfolio. |
| 110 | 2003 | Sara Soueidan (site) | https://www.sarasoueidan.com/ | other | read | Sara Soueidan site: clear who-for statement and writing/teaching as proof (P1). |
| 111 | 2004 | Vera Chen | https://www.verachen.me/ | other | read | Vera Chen: wave emoji in the h1, role and employers in meta (P18). |
| 112 | 2005 | Daniel Abayomi | https://pixeldahn.com/ | other | read | Daniel Abayomi (pixeldahn): title reads "One moment, please... Loader"; loader-gated page (P17). |
| 113 | 2006 | Jan Mraz | https://janmraz.com/ | other | read | Jan Mraz: illustration gallery of titled pieces; visual portfolio pattern. |
| 114 | 2007 | Michael Ajah | https://dribbble.com/naijatechguy | other | read | Michael Ajah Dribbble: profile shots; visual-only (P24). |
| 115 | 2008 | Zara Drei | https://zaradrei.com/ | other | read | Zara Drei: positioning by sector and outcome (conversion); repeated carousel headings in markup. |
| 116 | 2027 | Understanding Your Users, Second Edition: A Practical Guide to User Research Methods | https://shop.elsevier.com/books/understanding-your-users/baxter/978-0-12-800232-2 | book | summarized from description | Baxter et al., Understanding Your Users (publisher page): research methods with case studies; covered by lean-ux-klein.md. |
| 117 | 2034 | What are UX Case Studies? | https://ixdf.org/literature/topics/ux-case-studies | article | read | IxDF case studies: storytelling to hook hiring managers; step-by-step structure (P7, P11). |
| 118 | 2035 | How to write a UX case study | https://uxdesign.cc/how-to-write-a-case-study-1b1b5f5e3e2c | article | blocked, summarized from description | uxdesign.cc blocked (403). Per list description: tell the story behind the design: research, decisions, process (P11). |
| 119 | 2036 | 8 step guide to write an amazing UX Case study | https://www.linkedin.com/pulse/8-step-guide-write-amazing-ux-case-study-reetika-gupta-1c/ | article | read | LinkedIn 8 steps: title, overview with role, team, problem, tools; process; tests; learnings; proofread; quality over quantity (P7, P10, P15). |
| 120 | 2037 | UX Portfolio Case Study template (plus examples from successful hires) | https://uxplanet.org/ux-portfolio-case-study-template-plus-examples-from-successful-hires-86d5b0faa2d6 | article | blocked, summarized from description | uxplanet blocked (403). Per list description: case study template from successful hires (P25). |
| 121 | 2038 | How to Craft an Outstanding Case Study for Your UX Portfolio | https://careerfoundry.com/en/blog/ux-design/ux-case-study/ | article | read | CareerFoundry case study: two stories (project and designer), 1 to 2 paragraphs plus one image per section, say which work is yours, cite HIG/WCAG for decisions, say how you would measure impact (P7, P9, P10). |
| 122 | 2039 | How To Write a UX Case Study in 5 Steps | https://uxcel.com/blog/how-to-write-a-ux-case-study-in-5-steps | article | read | Uxcel 5 steps: specific problem statements, show your work; hiring managers scan for business impact in the first two paragraphs (P8, ST7). |
| 123 | 2040 | How to Write a UX Case Study: Template and Examples | https://xd.adobe.com/ideas/perspectives/leadership-insights/ux-case-study-template/ | article | read | Adobe XD Ideas (via WebFetch): intro gives company, challenge, role, scope, constraints and a results preview linking to results; 3 to 5 case studies; call-outs on screenshots; per method what, why, result, learned (P7, P8, P12, P4). |
| 124 | 2041 | How to build your own case study | https://uxdesign.cc/case-study-template-8832941a9d1b | article | blocked, summarized from description | uxdesign.cc blocked (403). Per list description: move case studies beyond headings, bullets and wireframe dumps (P10). |
| 125 | 2047 | How to Present a UX Case Study in a Job Interview | https://www.youtube.com/watch?v=ZVZfWfqmRBY | video | summarized from description | Mizko (oEmbed live): presenting a case study in an interview (C1). |
| 126 | 2048 | How to Write & Structure Your UX Case Study - Website Presentation Design | https://www.youtube.com/watch?v=hx7XyA8RNIw | video | summarized from description | Sharon Yeun Kim (oEmbed live): structure the case study on the portfolio site (P25). |
| 127 | 2049 | UX case study that got me hired - A walkthrough | https://www.youtube.com/watch?v=ptnYGRPlzN8 | video | summarized from description | Anfisa Bogomolova (oEmbed live): walkthrough of a hiring case study (P11). |
| 128 | 2050 | How to Outline & Write your UX Case Study | https://www.youtube.com/watch?v=M5HC58tTC2U | video | summarized from description | Maddy Beard (oEmbed live): outline and write a case study from a real example (P25). |
| 129 | 2051 | UX Portfolio - How to Create a UX Case Study | https://www.youtube.com/watch?v=mWnfc0Lm_F4 | video | summarized from description | yobi321 (oEmbed live): what makes a great case study (P25). |
| 130 | 2052 | Writing the Perfect UI/UX Case Study! | https://www.youtube.com/watch?v=d8FtsgQyGXw | video | summarized from description | Design Pilot (oEmbed live): critique of a real case study (P10). |
| 131 | 2059 | Google Mentor Case Study | https://www.behance.net/gallery/90958309/Google-Mentor-Design-Case-Study | other | blocked, summarized from description | Behance case study blocked (403). Per list description: Google Mentor process case study. |
| 132 | 2060 | Money transfer - A Better Way to Handle Your Money | https://www.behance.net/gallery/95491533/Money-transfer-A-Better-Way-to-Handle-Your-Money | other | blocked, summarized from description | Behance case study blocked (403). Per list description: money transfer app case study. |
| 133 | 2061 | Medico - Case Study | https://www.behance.net/gallery/91410737/Medico-Online-Medical-Services-Case-Study | other | blocked, summarized from description | Behance case study blocked (403). Per list description: Medico app case study. |
| 134 | 2062 | Case study: Designing an in-app messaging feature | https://medium.com/design-bootcamp/a-ux-case-study-on-carbon-an-in-app-messaging-feature-7b5c819982aa | other | blocked, summarized from description | Medium case study blocked (403). Per list description: in-app messaging feature case study. |
| 135 | 2063 | Case Studies Curated List | https://www.bestfolios.com/casestudy | other | read | Bestfolios case studies: Angular shell, unrendered meta "{{ngMeta.description}}" (P17 example); gallery index. |
| 136 | 2064 | Behance: Case Study List | https://www.behance.net/search/projects/?sort=appreciations&time=week&search=case+study | other | blocked, summarized from description | Behance search blocked (403): live search results, no fixed content. |
| 137 | 2150 | Solving Product Design Exercises: Questions & Answers | https://productdesigninterview.com/solving-product-design-exercises | book | summarized from description | Solving Product Design Exercises (author page): structured thinking, ask the right questions before solving (C2). |
| 138 | 2151 | Get Into UX: A Foolproof Guide to Getting Your First User Experience Job | https://www.goodreads.com/en/book/show/59024821 | book | summarized from description | Get Into UX (Goodreads): career breaking-in advice; out of scope beyond C1. |
| 139 | 2157 | 21 Essential UX Interview Questions & How to Answer Them | https://dribbble.com/resources/career/ux-interview-questions | article | read | Dribbble 21 questions: describe each project and why decisions were made; pick work for the employer; prepare a what-went-wrong story; non-designers review portfolios (P11, P13, P23). |
| 140 | 2158 | The 4 Types of UX Interview Questions to Master | https://uxbeginner.com/the-4-types-of-ux-interview-questions-to-master/ | article | read | UX Beginner: four interview question types; career only. |
| 141 | 2159 | 46 Interview Questions for User Experience Researchers at Google, Amazon, Microsoft and Facebook | https://medium.com/@eleonorazucconi/46-interview-questions-for-user-experience-researchers-at-google-amazon-microsoft-and-facebook-c582827267b9 | article | blocked, summarized from description | Medium blocked (403). Per list description: researcher interview questions; career only. |
| 142 | 2160 | 11 UX Design Interview Questions You Should Be Able to Answer | https://careerfoundry.com/en/blog/ux-design/make-sure-you-can-answer-these-11-ux-design-interview-questions/ | article | read | CareerFoundry 11 questions: workflow, most and least successful project, universal design; career, supports P11. |
| 143 | 2161 | Cracking the UX Design Interview | https://medium.com/interactive-mind/cracking-the-ux-design-interview-3ea6407093f5 | article | blocked, summarized from description | Medium blocked (403). Per list description: 50 rounds of interviews; career only. |
| 144 | 2162 | 12 UX Designer Interview Questions and Answers | https://www.coursera.org/articles/ux-designer-interview-questions-and-answers | article | read | Coursera 12 questions: incl. how would you improve our product and the whiteboard challenge (C2, C3). |
| 145 | 2163 | UX Design Job Interview Tips for Global Candidates: Landing Your Dream Role in the US | https://www.toptal.com/designers/ux/ux-design-job-interview-tips | article | read | Toptal global candidates (via WebFetch): lead case studies with business impact, spell out individual contribution, map process visually (P7, P8). |
| 146 | 2169 | The Essential UX Interview Questions (And How To Answer Them!) | https://www.youtube.com/watch?v=vu3xcQm7cEo | video | summarized from description | CareerFoundry (oEmbed live): common interview questions; career only. |
| 147 | 2170 | UX Design: How to ACE Your Next UX Job Interview | https://www.youtube.com/watch?v=I00LwSMABtk | video | summarized from description | AJ&Smart (oEmbed live): interview prep and rookie mistakes; career only. |
| 148 | 2171 | 10 CRUCIAL Questions You MUST Ask Your Interviewer (as a UX/UI Designer) | https://www.youtube.com/watch?v=ygMvS7RLUGs | video | summarized from description | Mizko (oEmbed live): questions to ask the interviewer; career only. |
| 149 | 2172 | UI/UX Design Job Interview Questions and Answers - Ace Your Next UX Design Interview! | https://www.youtube.com/watch?v=2OzTi0iUMlE | video | summarized from description | Sharon Onyinye (oEmbed live): interview Q and A; career only. |
| 150 | 2173 | Microsoft Interview Questions and Process - UIUX Design - TIPS to crack Microsoft Interview rounds | https://www.youtube.com/watch?v=feP6wiDor5U | video | summarized from description | Raghu nathan (oEmbed live): Microsoft interview process; career only. |
| 151 | 2197 | UX Jobs | https://www.uxjobsboard.com/ | job board | out of scope | UX Jobs Board: job listings; nothing for a design tool. |
| 152 | 2198 | UI/UX Jobs Board | https://uiuxjobsboard.com/ | job board | out of scope | UI/UX Jobs Board: job listings; nothing for a design tool. |
| 153 | 2199 | Dribbble Jobs | https://dribbble.com/jobs | job board | out of scope | Dribbble Jobs: job listings; nothing for a design tool. |
| 154 | 2200 | Behance Jobs | https://www.behance.net/joblist | job board | out of scope | Behance job list (403): job listings; nothing for a design tool. |
| 155 | 2201 | LinkedIn Jobs | https://www.linkedin.com/jobs/ | job board | out of scope | LinkedIn Jobs: job search; nothing for a design tool. |
| 156 | 2202 | AngelList Jobs | https://wellfound.com/jobs | job board | out of scope | Wellfound (AngelList renamed): startup jobs; nothing for a design tool. |
| 157 | 2203 | Glassdoor Jobs | https://www.glassdoor.com/index.htm | job board | out of scope | Glassdoor (403): jobs and reviews; nothing for a design tool. |
| 158 | 2204 | Indeed Jobs | https://www.indeed.com/ | job board | out of scope | Indeed (403): job search; nothing for a design tool. |
| 159 | 2205 | YC Jobs | https://www.ycombinator.com/jobs/ | job board | out of scope | YC Jobs: startup jobs; nothing for a design tool. |
| 160 | 2206 | Remotive Jobs | https://remotive.com/ | job board | out of scope | Remotive: remote jobs; nothing for a design tool. |
| 161 | 2207 | Remote Jobs | https://remote.co/remote-jobs/ | job board | out of scope | Remote.co: HTTP/2 error and 503 (unreachable now); remote jobs; out of scope. |
| 162 | 2208 | Facebook Jobs | https://www.facebook.com/careers/ | job board | out of scope | Facebook careers: redirects to a login wall (careers moved to metacareers.com); out of scope. |
| 163 | 2209 | Google Jobs | https://www.google.com/about/careers/applications/ | job board | out of scope | Google careers: job search; nothing for a design tool. |
| 164 | 2210 | Twitter Jobs | https://careers.twitter.com/ | job board | out of scope | Twitter careers: redirects to x.ai/careers (403); stale link; out of scope. |
| 165 | 2211 | Microsoft Jobs | https://careers.microsoft.com/v2/global/en/home.html | job board | out of scope | Microsoft careers: job search; nothing for a design tool. |
| 166 | 2231 | Upwork | https://www.upwork.com/ | job board | out of scope | Upwork (403): freelance marketplace; out of scope. |
| 167 | 2232 | Fiverr | https://www.fiverr.com/ | job board | out of scope | Fiverr (403): freelance marketplace; out of scope. |
| 168 | 2233 | Freelancer | https://www.freelancer.com/ | job board | out of scope | Freelancer: freelance marketplace; out of scope. |
| 169 | 2234 | 99Designs | https://99designs.com/ | job board | out of scope | 99designs: design contests; out of scope. |
| 170 | 2235 | DesignCrowd | https://www.designcrowd.com/ | job board | out of scope | DesignCrowd: design contests; out of scope. |
| 171 | 2236 | CrowdSpring | https://www.crowdspring.com/ | job board | out of scope | CrowdSpring (202 bot check): design contests; out of scope. |
| 172 | 2237 | Designhill | https://www.designhill.com/ | job board | out of scope | Designhill: design marketplace; out of scope. |
| 173 | 2238 | DesignContest | https://www.designcontest.com/ | job board | out of scope | DesignContest: design contests; out of scope. |
| 174 | 2239 | PeoplePerHour | https://www.peopleperhour.com/ | job board | out of scope | PeoplePerHour: freelance marketplace; out of scope. |
| 175 | 2240 | Toptal | https://www.toptal.com/ | job board | out of scope | Toptal (403 homepage): vetted freelance network; out of scope. |
| 176 | 2259 | Jupiter Design Community | https://chat.whatsapp.com/Ku4SUjSmc4zIAg5XzffEcs | community | out of scope | WhatsApp group invite: private chat; out of scope. |
| 177 | 2260 | UX Design Hangout | https://designerhangout.co/?mwr=3a1f1519/ | community | dead | Designer Hangout: domain does not resolve (DNS failure). |
| 178 | 2261 | Figma Africa | https://foflagos.slack.com/ | community | out of scope | Figma Africa Slack (403, sign-in required): private community; out of scope. |
| 179 | 2262 | UX Guide | https://ux.guide/ | community | dead | UX Guide: domain does not resolve (DNS failure). |
| 180 | 2263 | UX Her | https://uxher.com/ | community | out of scope | UX HER: now a consultancy site, not a community; out of scope. |
| 181 | 2264 | Designer Slack Communities | https://www.designerslack.community/ | community | out of scope | Designer Slack Communities: directory of Slack groups; out of scope. |
| 182 | 2270 | Jared Spool | https://twitter.com/jmspool | community | out of scope | Jared Spool on X: social profile; out of scope (his work is cited elsewhere in ux-skill via NN/g style sources). |
| 183 | 2271 | Luke Wroblewski | https://twitter.com/lukew | community | out of scope | Luke Wroblewski on X: social profile; out of scope. |
| 184 | 2272 | Chris Do | https://twitter.com/thechrisdo | community | out of scope | Chris Do on X: social profile; out of scope. |
| 185 | 2273 | Zander Whitehurst | https://twitter.com/zander_supafast | community | out of scope | Zander Whitehurst on X: social profile; out of scope. |
| 186 | 2274 | Grace Ling | https://twitter.com/graceleaf_ | community | out of scope | Grace Ling on X: social profile; out of scope. |
| 187 | 2275 | Timothy Achumba | https://twitter.com/timothyachumba | community | out of scope | Timothy Achumba on X: social profile; out of scope. |
| 188 | 2276 | Daniel Abayomi | https://twitter.com/pixelDahn | community | out of scope | Daniel Abayomi on X: social profile; out of scope. |
| 189 | 2277 | Oyindamola Ajibike | https://twitter.com/MystiqueDammy | community | out of scope | Oyindamola Ajibike on X: social profile; out of scope. |
| 190 | 2278 | Jan Mrazek | https://twitter.com/janm_uiux | community | out of scope | Jan Mrazek on X: social profile; out of scope. |
| 191 | 2279 | Hammed Taiwo | https://twitter.com/rapzzyofficial | community | out of scope | Hammed Taiwo on X: social profile; out of scope. |
| 192 | 2280 | Victor Onazi | https://twitter.com/VictorOnazi_ | community | out of scope | Victor Onazi on X: social profile; out of scope. |
| 193 | 2281 | Tunbosun Tobilola | https://twitter.com/Futureio | community | out of scope | Tunbosun Tobilola on X: social profile; out of scope. |
| 194 | 2282 | Druids | https://twitter.com/druids01 | community | out of scope | Druids on X: social profile; out of scope. |
| 195 | 2283 | Josiah Endurance | https://twitter.com/hendurhance | community | out of scope | Josiah Endurance (list author) on X: social profile; out of scope. |
| 196 | 2284 | UX Collective | https://twitter.com/uxdesigncc | community | out of scope | UX Collective on X: publication feed; out of scope. |
| 197 | 2285 | UX Planet | https://twitter.com/uxplanet | community | out of scope | UX Planet on X: publication feed; out of scope. |
| 198 | 2298 | [Buy me a coffee](https://buymeacoffee.com/hendurhance) | https://buymeacoffee.com/hendurhance | other | out of scope | Buy Me a Coffee (list author): donation page; out of scope. |
| 199 | 2299 | [GitHub Sponsors](https://github.com/sponsors/hendurhance) | https://github.com/sponsors/hendurhance | other | out of scope | GitHub Sponsors (list author, 403 without sign-in): donation page; out of scope. |
| 200 | 2068 | Figma case study template (Project Tasks #4, task one) | https://www.figma.com/community/file/1067428863353945820 | template or kit | blocked, summarized from description | Figma case study template (403 via WebFetch, 202 via curl): content not retrievable; part of Project Tasks #4. |
| 201 | 2069 | Figma Case Study Template (Project Tasks #4, task two) | https://www.figma.com/community/file/1015129345947090766/Case-Study-Template | template or kit | read | Figma Case Study Template v0.1: overview, roles, tools and duration, challenge, goals, research, persona, findings and more (P7, P25). |
| 202 | 2070 | Figma Case Study Template, Creative Ferry (Project Tasks #4) | https://www.figma.com/community/file/949395060452790372/Case-Study-Template---Creative-Ferry | template or kit | read | Figma Creative Ferry template: comes with a case study checklist and a best-practice video (P25). |
| 203 | 2070 | Figma Behance Presentation Template (Project Tasks #4) | https://www.figma.com/community/file/1079111124242711698/Behance-Presentation-Template-UI%2FUX-Case-study | template or kit | blocked, summarized from description | Figma Behance presentation template (403): content not retrievable. |
| 204 | 2090 | Design System Checklist (Project Tasks #5; linked twice, lines 2090 and 2119) | https://www.designsystemchecklist.com/ | guideline or standard | read | Design System Checklist: design language, foundations, every component with states incl. reduced motion and reserved icons (ST16). |
| 205 | 2180 | Bestfolios resumes (resume examples box) | https://www.bestfolios.com/resumes | other | read | Bestfolios resumes: Angular shell, unrendered meta; resume gallery (C4). |

## Part 2b. Ledger: mirror links (27)

These mega.nz links are file copies of books and documents, most of them paid books. They were deliberately not opened. ux-skill should not ingest or link them. Each mirrored book is analyzed through its publisher or author page in 2a; three rows have only a mirror and are summarized from the list description.

| line | title | URL | type | status | note |
|---|---|---|---|---|---|
| 1673 | Designing Voice User Interfaces: Principles of Conversational Experiences | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1674 | Voice User Interface Design: Moving from GUI to Mixed Modal Interaction | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1675 | Conversational UX Design: A Practitioner's Guide to the Natural Conversation Framework | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1715 | 3D User Interfaces: Theory and Practice | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1716 | Virtual & Augmented Reality for Dummies | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1717 | Learning Virtual Reality: Developing Immersive Experiences and Applications for Desktop, Web, and Mobile | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1718 | Oculus Rift in Action | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1771 | Machine Learning Design Patterns | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1772 | Designing Human-Centric AI Experiences: Applied UX Design for Artificial Intelligence (Design Thinking) | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1836 | UX Strategy: How to Devise Innovative Digital Products that People Want | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1837 | Designing Search: UX Strategies for eCommerce Success | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1838 | Lean UX: Designing Great Products with Agile Teams | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1875 | Content Strategy for the Web | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1876 | Content Strategy at Work. Real-world Stories to Strengthen Every Interactive Project | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1911 | Design Sprint: A Practical Guidebook for Creating Great Digital Products | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1912 | Sprint: How to Solve Big Problems and Test New Ideas in Just Five Days | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1913 | UX for Lean Startups: Faster, Smarter User Experience Research and Design | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1955 | Burn Your Portfolio | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1956 | Design Matters: Portfolios 01: An Essential Primer for Today's Competitive Market | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1957 | Stand Out: Design a personal brand. Build a killer portfolio. Find a great design job. | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 1958 | The Squiggly Career: Ditch the ladder, discover opportunity, design your career: The five skills you need to succeed in work today | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 2027 | Understanding Your Users, Second Edition: A Practical Guide to User Research Methods | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 2028 | A UI Design Case Study and a Prototype of a Travel Search Engine Project Report | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | only link for this row; summarized from the list description: a UI case study and travel search engine prototype report (supports P25) |
| 2058 | Health Wise Case Study | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | only link for this row; summarized from the list description: Health Wise app process case study (supports P11) |
| 2150 | Solving Product Design Exercises: Questions & Answers | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 2151 | Get Into UX: A Foolproof Guide to Getting Your First User Experience Job | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | book analyzed via its publisher page (see 2a) |
| 2189 | UI/UX Cover Letter Template | (unofficial mirror, link withheld) | mirror (file copy) | not fetched | only link for this row; a cover-letter file; career, out of scope beyond C4 |

## Part 2c. Ledger totals

- Link occurrences in the block: 234 = 207 ordinary (206 unique, designsystemchecklist.com twice) + 27 mirrors.
- Unique ordinary links: 206. Read: 63. Summarized from description: 56. Blocked (summarized from description): 31. Out of scope: 52. Dead: 4.
- Mirrors: 27, not fetched (3 of them are the only link on their row and were summarized from the list description).
- Dead: 084 CareerFoundry tips (moved, no target), 096 Rama Krushna Notion page (now Notion marketing), 177 designerhangout.co and 179 ux.guide (domains do not resolve). Stale but live: 156 AngelList (now Wellfound), 162 Facebook careers (login wall; now metacareers.com), 164 Twitter careers (redirects to x.ai/careers), 182 to 197 twitter.com (now x.com), 180 UX HER (now a consultancy, not a community).
