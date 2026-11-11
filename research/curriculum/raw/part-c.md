# Part C: Design Thinking, Designing with AI, Advanced Design Techniques

Source block: hendurhance/ui-ux README.md lines 1136 to 1655 (local clone, read only). 162 links. Compared against /home/user/ux-skill: PLAN-4.1-inventory.md (152 principles), references/ (headings, with references/foundations/ai-interfaces.md read in full), data/anti-patterns.json rule ids, render rules in engine/render/core.py, taste.py and interact.py, and the complaints probe kinds in engine/complaints.py.

How to read this file:
- Each lesson is in our own words, with its source URLs, a status and, where missing, a proposal.
- Status keys: COVERED (file or rule named), MISSING-CHECK (lint rule, render measurement or complaints probe, with a one-line detection sketch), MISSING-GUIDE (the references/ file it belongs in).
- "Inventory" means PLAN-4.1-inventory.md; where a lesson repeats an inventory row, the row id is given and the lesson is not counted as new.
- Books were not read in full. Book lessons come from publisher or author descriptions and reputable summaries, and say so. Videos were checked live through YouTube oEmbed (title and channel); their content comes from the README description and public listings only.
- ux-skill is deterministic and uses no model at check time. Where a source is an AI tool, the lesson says what the tool's approach teaches and where ux-skill should differ.

Counts for this part: 162 links (51 read, 70 summarized from description of which 10 were blocked, 12 tools noted, 1 dead, 28 out of scope). 102 lessons: 34 COVERED, 21 MISSING-CHECK (19 distinct new checks; I-1 upgrades inventory E25 and I-2 folds into I-1), 44 MISSING-GUIDE, 3 already proposed in the inventory and not counted as new.

---

## 1. Design thinking and critique

DT-1. Design thinking is a loop, not a sequence: what testing shows routinely sends a team back to redefine the problem, so a design brief must stay open to revision after the first test.
- Sources: https://ixdf.org/literature/topics/design-thinking, https://ixdf.org/literature/article/5-stages-in-the-design-thinking-process, https://www.ama.org/marketing-news/the-5-phases-of-design-thinking/
- Status: COVERED. references/process/lean-ux-gothelf.md (build, measure, learn loop), references/process/lean-ux-klein.md and references/process/discovery-protocol.md.

DT-2. Frame the problem from the user's side (a point-of-view statement or a "How might we" question), never as the company's goal; check every idea against that statement while narrowing.
- Sources: https://careerfoundry.com/en/blog/ux-design/design-thinking-process/, https://www.ama.org/marketing-news/the-5-phases-of-design-thinking/, https://ixdf.org/literature/topics/design-thinking
- Status: MISSING-GUIDE. references/process/discovery-protocol.md: add a one-line user-side problem statement as a required output of discovery, and have /ux-frame echo it so later critique can test against it. (No "How might we" or POV framing found in references/process/.)

DT-3. Diverge before converging: generate many options without judging, then narrow with an analytic pass. Starting from technical constraints, or demanding a perfect first version, shrinks the option space.
- Sources: https://ixdf.org/literature/article/5-stages-in-the-design-thinking-process, https://ixdf.org/literature/topics/design-thinking
- Status: COVERED. references/process/generation-modes.md (shotgun exploration, anti-convergence test) and references/process/creative-selection.md.

DT-4. Prototype cheaply and in several variants; test to learn, not to prove.
- Sources: https://www.ama.org/marketing-news/the-5-phases-of-design-thinking/, https://careerfoundry.com/en/blog/ux-design/design-thinking-process/
- Status: COVERED. references/process/generation-modes.md (variant axes), commands/ux-research.md, references/laws/krug.md (testing on a budget).

CR-1. A critique judges the work against stated goals (business goal, user goal, constraints such as accessibility level, and the fidelity being reviewed), not against taste. Without those goals stated up front, feedback drifts into opinion.
- Sources: https://www.toptal.com/designers/product-design/productive-design-critique-guide, https://www.nngroup.com/articles/design-critiques/, https://www.uxpin.com/studio/blog/what-is-design-critique/, https://xd.adobe.com/ideas/process/ui-design/design-critique-tips/, Discussing Design (https://www.goodreads.com/book/show/25173297-discussing-design, from description)
- Status: MISSING-GUIDE. commands/ux-critique.md grounds critique in named principles (inventory H12) but does not require the goal, audience and fidelity as inputs. Add them to its Input section, and have it read the frame saved by /ux-frame when present.

CR-2. Name the problem before proposing a fix, be specific, phrase directives as questions tied to a goal, and give both positive and negative points (quotas help quiet reviewers speak).
- Sources: https://www.nngroup.com/articles/design-critiques/, https://www.toptal.com/designers/product-design/productive-design-critique-guide, https://xd.adobe.com/ideas/process/ui-design/design-critique-tips/
- Status: COVERED. commands/ux-critique.md ("find the three pairs", named-principle grounding).

CR-3. Run sessions with structure: 3 to 7 reviewers from mixed disciplines, a facilitator and a note-taker, about 2 minutes per person round the room, at most two topics an hour; a silent written round first suits remote teams.
- Sources: https://www.figma.com/blog/design-critiques-at-figma/, https://www.toptal.com/designers/product-design/productive-design-critique-guide, https://www.uxpin.com/studio/blog/what-is-design-critique/
- Status: MISSING-GUIDE (low). references/process/design-thinking-apphaus.md covers a workshop, not a critique; add a short critique-session protocol there or in commands/ux-workshop.md.
- Numbers: Toptal says 5 to 7 critiquers, UXPin 3 to 7. Not in conflict; use 3 to 7.

CR-4. Close the loop: tell reviewers which feedback was applied and what changed.
- Sources: https://www.uxpin.com/studio/blog/what-is-design-critique/, https://www.nngroup.com/articles/design-critiques/
- Status: COVERED. `uxskill complaints check` keeps each complaint and measures whether it is still open (engine/complaints.py), which is this loop made mechanical.

## 2. AI foundations: the paradigm and the vocabulary

AI-1. Intent-based interaction moves control to the system: people state an outcome, and the system chooses the steps. Because prompts are prose, an articulation barrier follows (Nielsen estimates roughly half of adults in wealthy countries may not write well enough to get good results). An interface that offers only an empty text box fails those people.
- Sources: https://www.nngroup.com/articles/ai-paradigm/, https://wattenberger.com/thoughts/boo-chatbots/
- Status: MISSING-CHECK `prompt-placeholder-ask-anything` (static lint, text channel). Detection: a textarea or text input whose placeholder or adjacent label matches /ask (me )?anything|how can i help( you)?( today)?|type (a|your) message|what can i do for you/i. ai-interfaces.md already forbids "Ask me anything" in prose; nothing checks it.
- Numbers: the "about half" figure is Nielsen's estimate from literacy data, not a measured prompting result. Cite it as an estimate.

AI-2. Prefer controls to prompts for parameters the product already knows (tone, length, audience, format): sliders, chips, presets and saved styles beat retyping instructions. Keep chat for open intent; keep forms and direct manipulation for the rest (hybrid UI, "AI second").
- Sources: https://www.nngroup.com/articles/ai-paradigm/, https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/, https://wattenberger.com/thoughts/boo-chatbots/, https://www.shapeof.ai/ (Tuners: parameters, preset styles, saved styles)
- Status: MISSING-GUIDE. references/foundations/ai-interfaces.md, new subsection "Steer with controls, not only words".

AI-3. Call something an agent only when it pursues a goal by acting on an environment, checking progress and choosing its next step; a model that only replies is not one. Agent patterns (permissions, logs, undo) apply when actions happen.
- Sources: https://www.nngroup.com/articles/definition-ai-agent/, https://www.anthropic.com/engineering/building-effective-agents
- Status: MISSING-GUIDE. references/foundations/ai-interfaces.md: one scoping paragraph at the top of "Keep a person in charge of actions" saying when that section applies.

AI-4. Start with the simplest structure (a fixed workflow) and add autonomy only where it measurably helps; agents should show their planning steps, stop at checkpoints for human input, and have stop conditions.
- Sources: https://www.anthropic.com/engineering/building-effective-agents
- Status: COVERED. ai-interfaces.md ("which step it is on in words", running log with a way to stop the rest of the run).

AI-5. Make AI output fast to verify: the person is the verifier, so the interface should show changes as diffs or highlights, size each change to what a person can check at a glance, and offer an autonomy ladder (suggest, edit a chunk, edit a file, act across many).
- Sources: https://www.youtube.com/watch?v=LCEmiRjPEtQ (from public summaries), https://wattenberger.com/thoughts/boo-chatbots/, https://www.shapeof.ai/ (Variations, Branches)
- Status: MISSING-GUIDE. references/foundations/ai-interfaces.md, "Let the person correct it": add "show what changed" (diff or highlight against the previous version) and "keep a working draft with version history" (Wattenberger's point that chat answers stand alone and revisions are hard to follow).

AI-6. Present model output as a signal to weigh, not a verdict: statistical output stated as fact over-sells it. Design for the system's odd or wrong conclusions as a normal case.
- Sources: https://bigmedium.com/ideas/hello-sentient-design.html, https://www.youtube.com/watch?v=Hu5Jc1yIfas (from AIGA listing), Sentient Design (https://rosenfeldmedia.com/books/sentient-design/, from publisher description)
- Status: COVERED. ai-interfaces.md "Show where an answer comes from, and how sure it is" and copy.md "Tone for AI features" (augmentation framing).

AI-7. Test the real model, including its failures and refusals, before designing the interface around it; design against observed outputs, not the ideal answer.
- Sources: https://platform.claude.com/ (tool), https://developer.apple.com/design/human-interface-guidelines/generative-ai (evaluate model capability hands-on early), https://hamel.dev/blog/posts/evals-faq/
- Status: MISSING-GUIDE. references/foundations/ai-interfaces.md: add "Design from real outputs: collect a sample of real answers, including bad ones, and design the empty, slow, wrong and refused states from them."

## 3. Setting expectations and onboarding

EX-1. Say what the system can do and how well it does it, before first use (HAX G1 and G2), with product-specific example inputs.
- Sources: https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/, https://www.microsoft.com/en-us/haxtoolkit/library/, https://developer.apple.com/design/human-interface-guidelines/generative-ai, https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guideline 3)
- Status: COVERED. ai-interfaces.md "Say what it is and what it can do". Check side is AI-1.

EX-2. After each answer, offer a few clickable follow-ups tied to that answer and the available content; drop ones the person has ignored. Follow-ups teach capability better than a static help page.
- Sources: https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design, https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guideline 4), https://www.shapeof.ai/ (Suggestions, Nudges)
- Status: MISSING-GUIDE. ai-interfaces.md covers only starter prompts; add follow-up suggestions to "Show the work while it happens".

EX-3. Let the system show what it can do by doing a first piece of real work (configure, analyse, draft) instead of tooltips on an empty screen.
- Sources: https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design
- Status: MISSING-GUIDE. ai-interfaces.md (onboarding) and references/foundations/copy.md (Empty state patterns: an AI feature's empty state can be a worked example).

EX-4. Offer a non-AI path when the model is unavailable or the person opts out; the core task must still be possible.
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai
- Status: MISSING-GUIDE. ai-interfaces.md, new bullet under "Say what it is".

EX-5. Progress text names the actual work ("Summarizing key themes from your notes"), not "Processing..." or "Thinking...".
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai, ai-interfaces.md already says this for long tasks.
- Status: MISSING-CHECK `progress-text-generic` (static lint, text channel). Detection: an element with role=status, aria-live or aria-busy, or a spinner sibling, whose only text matches /^(processing|thinking|loading|working|please wait|generating)(\.\.\.|\u2026)?$/i.

EX-6. Never present the model as a person: no human name with a stock face, no first-person feelings, no "typing" theatre. Neutral wording keeps trust calibrated.
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai, https://www.nngroup.com/articles/explainable-ai/
- Status: COVERED. ai-interfaces.md ("Never present the model as a person") and copy.md "Tone for AI features".

EX-7. Proactive AI help must be quick to invoke, quick to dismiss and quick to correct, and should hold back (ask or narrow scope) when unsure (HAX G7 to G10).
- Sources: https://www.microsoft.com/en-us/haxtoolkit/library/
- Status: MISSING-GUIDE. ai-interfaces.md: "A suggestion the person did not ask for closes in one action and does not return in the same session."

EX-8. Over time: remember recent context, adapt cautiously, give global controls over personalization and memory, and tell people when the model or its behaviour changes (HAX G12 to G18). Let people view, edit and delete what the system remembers about them.
- Sources: https://www.microsoft.com/en-us/haxtoolkit/library/, https://www.shapeof.ai/ (Memory, Incognito mode, Data ownership)
- Status: MISSING-GUIDE. ai-interfaces.md "Respect what people share" covers history and training opt-out; add a memory panel and a change notice ("What's new in the assistant") as patterns.

EX-9. When output is blocked or poor, coach: say why in plain words and suggest a better request.
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai, https://pair.withgoogle.com/chapter/errors-failing/
- Status: COVERED. ai-interfaces.md ("say what failed and offer the next move ... keeping the person's prompt in the box").

EX-10. A site should have one assistant entry point, available on every page, not several competing bots.
- Sources: https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guidelines 1 and 2), https://pair.withgoogle.com/chapter/errors-failing/ (multiple systems, signal crashes)
- Status: MISSING-CHECK `chat-launcher-more-than-one` (render). Detection: at 1280 and 390 widths, count position:fixed elements whose accessible name or text matches /chat|assistant|ask|help|support/i and that are buttons or links; flag 2 or more. landing.md already rules on launcher placement.

## 4. Explainability, grounding and trust

TR-1. Cite inline, next to the claim, with a descriptive label (publication or page title), visually distinct from the answer, linking to the passage where possible.
- Sources: https://www.nngroup.com/articles/explainable-ai/, https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design, https://www.shapeof.ai/ (Citations, References), https://elements.ai-sdk.dev/ (InlineCitation, Sources)
- Status: placement COVERED in ai-interfaces.md; label is MISSING-CHECK `citation-label-generic` (static lint, advisory). Detection: a[href] with visible text matching /^\s*(source|sources|link|ref|\[?\d+\]?)\s*$/i and no aria-label or title naming the source. WCAG 2.4.4 Link Purpose (In Context) lets context supply the purpose, so this is a usability rule from NN/g, not a WCAG failure.

TR-2. Citations raise felt confidence whether or not anyone opens them, and people rarely open them; citations can also be invented, dead or not support the claim. So a citation is not a trust ornament: tell people to check, and make the check cheap.
- Sources: https://www.nngroup.com/articles/explainable-ai/
- Status: MISSING-GUIDE. ai-interfaces.md, add: "A citation must open the passage it supports; never show a source count as a badge of reliability."
- Numbers: the README says users "almost never click" citations. The NN/g article gives no percentage; it reports that people rarely click. Keep it qualitative.

TR-3. Separate process from result: put the answer first and full width; keep reasoning and tool activity in a collapsed area, one line per step, expandable for those who want it. Do not present a reasoning trace as a faithful explanation; it can be written after the fact.
- Sources: https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design, https://www.nngroup.com/articles/explainable-ai/, https://www.shapeof.ai/ (Stream of Thought, Footprints), https://elements.ai-sdk.dev/ (Reasoning, ChainOfThought, Tool)
- Status: MISSING-GUIDE. ai-interfaces.md "Show the work while it happens": add the collapsed step list and the caution on reasoning text.

TR-4. Put the "can make mistakes, check it" note next to the input box in plain words with a concrete action, not in the footer or behind a help icon; introduce it at onboarding too.
- Sources: https://www.nngroup.com/articles/explainable-ai/, https://developer.apple.com/design/human-interface-guidelines/generative-ai (tell people output may contain errors)
- Status: MISSING-CHECK `ai-caveat-far-from-input` (render). Detection: when the page has a prompt input (textarea plus a send button), find visible text matching /(can|may) (make mistakes|be (wrong|inaccurate))|check (important|its) (info|answers)|verify/i; flag if absent from the first screen, or if its box is inside footer, or more than 160px from the input box at 390px width, or present only in a title attribute or tooltip.

TR-5. Do not show uncalibrated confidence percentages; prefer words that change what the person does. If a confidence display is used, it must be calibrated, and low confidence should slow review rather than decorate.
- Sources: ai-interfaces.md, https://pair.withgoogle.com/explorables/ ("Are model predictions probabilities?"), https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/
- Status: COVERED. ai-interfaces.md. Conflict noted in section 12 (Yocco shows "95%" badges).

TR-6. Label AI-generated content with one consistent marker that opens a short explanation (what produced it, from what, how to check), at every scale from a field to a page. When a person edits AI content, it switches to the normal human state, with a way to revert to the AI version.
- Sources: https://carbondesignsystem.com/guidelines/carbon-for-ai/ (current home of the dead link https://www.carbondesignsystem.com/building-blocks/core/components/ai-label/guidelines), https://www.shapeof.ai/ (Disclosure, Identifiers)
- Status: MISSING-GUIDE. ai-interfaces.md, new subsection "Mark what the AI made". The marker must be keyboard operable and named (covered by `div-onclick-no-role`, `inline-svg-no-aria`).

TR-7. An AI identity mark (colour, icon) is allowed only as one token-defined marker used where AI acts; it is never decoration. Carbon uses a subtle glow and gradient for AI presence but forbids using it decoratively and keeps text contrast intact.
- Sources: https://carbondesignsystem.com/guidelines/carbon-for-ai/, https://www.shapeof.ai/ (Identifiers: avatar, color, iconography, name)
- Status: MISSING-GUIDE. ai-interfaces.md "Look like the product": reconcile with references/styles/anti-slop.md, which bans sparkle and glow as AI iconography. Recommended reading: anti-slop bans glow as decoration; a single AI token used only to mark AI output is acceptable. The check side is inventory E22 (cliche icons), not new.

TR-8. Show where the system is looking: what is in context (attached files, selected text, connected sources) and how full the context is.
- Sources: https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design, https://www.shapeof.ai/ (Attachments, Connectors, Filters), https://elements.ai-sdk.dev/ (Context, Attachments)
- Status: MISSING-GUIDE. ai-interfaces.md "Show where an answer comes from".

TR-9. Distinguish answers from the person's own data from general-knowledge answers.
- Sources: ai-interfaces.md, https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design
- Status: COVERED. ai-interfaces.md.

## 5. Errors, uncertainty, hallucination and chat UX

ER-1. Use a failure taxonomy when designing AI states: context errors (system right, explanation poor), failstates (system cannot answer), background errors (wrong and nobody notices), unexpected input, breaking habituation, miscalibrated input, low confidence, irrelevance, and competing systems. Each needs a different response.
- Sources: https://pair.withgoogle.com/chapter/errors-failing/
- Status: MISSING-GUIDE. ai-interfaces.md, new section "Plan for each kind of failure", one line per type with its response.

ER-2. Keep unpredictable AI output in a designated area; never reorder or replace controls people use from muscle memory on the strength of a prediction, and let them return to a stable layout.
- Sources: https://pair.withgoogle.com/chapter/errors-failing/ (breaking habituation), https://www.microsoft.com/en-us/haxtoolkit/library/ (G14 update and adapt cautiously)
- Status: MISSING-GUIDE. ai-interfaces.md and references/laws/laws-of-ux.md (Jakob's law note on adaptive menus).

ER-3. Loose or misspelled input gets a "did you mean" offer instead of a dead end; ambiguous intent gets a short clarifying question or a few options.
- Sources: https://pair.withgoogle.com/chapter/errors-failing/, https://www.nngroup.com/articles/definition-ai-agent/, https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ (Escalation Pathway)
- Status: MISSING-GUIDE. ai-interfaces.md "Let the person correct it".

ER-4. Low confidence ends in an explanation and alternatives, never a blank; failure is made safe and dull, and the person gets control back with the context they need.
- Sources: https://pair.withgoogle.com/chapter/errors-failing/, https://developer.apple.com/design/human-interface-guidelines/generative-ai
- Status: COVERED. ai-interfaces.md (fails with next move), references/foundations/copy.md (Error message patterns).

ER-5. When a long answer streams in, keep the start of the new answer in view; do not drag the viewport to the bottom as text arrives.
- Sources: https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guideline 7)
- Status: MISSING-CHECK `chat-scrolls-to-bottom` (static lint on scripts, heuristic, advisory). Detection: inside a handler that appends streamed text (onmessage, for await, reader.read, onToken), an unconditional `scrollTop = el.scrollHeight` or `scrollIntoView({ block: 'end' })` with no guard comparing the current position to the bottom. Plus MISSING-GUIDE: amend ai-interfaces.md (see conflict in section 12).

ER-6. Let the chat surface grow (resize or maximize) for maps, tables and long lists; use expandable details to keep turns short; include images and diagrams instead of walls of text.
- Sources: https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guidelines 5, 6, 8), https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design (multimedia over text)
- Status: MISSING-GUIDE. ai-interfaces.md "Look like the product" (answers typeset as content is COVERED; resize and expandable details are not).

ER-7. Let people save, download, share or send an answer to their tools, and convert it between formats (table, list, document).
- Sources: https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guideline 9), https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/ (output transformations and sharing)
- Status: MISSING-GUIDE. ai-interfaces.md "copies cleanly" is partial; add export and share.

ER-8. Offer voice input beside typing for people who find typing hard.
- Sources: https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ (guideline 10), https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/
- Status: MISSING-GUIDE. ai-interfaces.md, with a pointer from references/foundations/accessibility.md.

ER-9. Apply a prompt to a selected part of the output (rewrite this paragraph, regenerate this region) instead of regenerating everything; let people pick pieces from several variations.
- Sources: https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/ (contextual edits, cherry-picking), https://www.shapeof.ai/ (Inline action, Inpainting, Variations)
- Status: MISSING-GUIDE. ai-interfaces.md "Let the person correct it".

ER-10. When listing many options, rank and highlight the best few instead of returning an unranked wall.
- Sources: https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/ (forced ranking)
- Status: MISSING-GUIDE (low). ai-interfaces.md; relates to Hick's law in references/laws/laws-of-ux.md.

ER-11. Each running answer has Stop; each finished answer has Regenerate, Edit prompt and Copy beside it.
- Sources: ai-interfaces.md, https://developer.apple.com/design/human-interface-guidelines/generative-ai (Edit, Undo, Retry near content), https://www.shapeof.ai/ (Regenerate, Controls), https://elements.ai-sdk.dev/ (Message actions)
- Status: guidance COVERED in ai-interfaces.md; MISSING-CHECK `ai-answer-actions-missing` (static lint, advisory). Detection: inside role=log or a container whose class or data attribute names messages, an assistant message element (data-role/aria-label/class matching assistant|bot|ai) with no descendant or sibling button whose accessible name matches /copy|regenerate|retry|edit/i. Complaints probe today: kind "present" with selector `button[aria-label*="Regenerate" i]`.

ER-12. Conversation design needs repair moves: rephrase the question more narrowly, offer choices, and hand off to a person when the system keeps misunderstanding. Prototype and test conversation flows before building them.
- Sources: Conversations with Things (https://rosenfeldmedia.com/books/conversations-with-things/, from reviews), Conversational Design (https://abookapart.com/products/conversational-design, from publisher description), https://www.voiceflow.com/ (tool)
- Status: MISSING-GUIDE. ai-interfaces.md, new bullet list "Repair a misunderstanding".

## 6. Agentic interfaces

AG-1. Before a consequential action, show the plan in plain steps and offer three choices: go ahead, edit the plan, or do it myself.
- Sources: https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ (Intent Preview), https://www.shapeof.ai/ (Action plan, Verification, Sample response), https://elements.ai-sdk.dev/ (Plan, Confirmation)
- Status: preview COVERED in ai-interfaces.md ("show exactly what will happen ... ask once"); the "edit the plan" and "do it myself" options are MISSING-GUIDE (same file).

AG-2. A confirm dialog names the action on its button ("Send to 14 people"), never "OK" or "Yes".
- Sources: ai-interfaces.md, references/foundations/copy.md (Confirmation dialog), https://developer.apple.com/design/human-interface-guidelines/generative-ai (confirm significant actions)
- Status: MISSING-CHECK `dialog-button-ok` (static lint). Detection: a button inside dialog, [role=dialog] or [role=alertdialog] whose whole text is /^(ok|okay|yes|confirm|sure|proceed)$/i. Today `generic-cta-text` and `cta-text-tap-continue-go` do not include these words.

AG-3. Let people set how independent the agent is per kind of task, not one global switch: observe and suggest, plan and propose, act with confirmation, act alone within a pre-approved limit. Start new users low.
- Sources: https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ (Autonomy Dial), https://www.youtube.com/watch?v=LCEmiRjPEtQ (autonomy slider, from summaries), Human-Centered AI (https://books.google.com/books/about/Human_centered_AI.html?id=YS9VEAAAQBAJ, from listing: high control with high automation)
- Status: MISSING-GUIDE. ai-interfaces.md "Keep a person in charge of actions".

AG-4. For actions the agent took in the background, explain proactively in the form "because you said X, I did Y".
- Sources: https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ (Explainable Rationale), https://www.microsoft.com/en-us/haxtoolkit/library/ (G11 make clear why the system did what it did)
- Status: MISSING-GUIDE. ai-interfaces.md.

AG-5. Keep a timeline of agent actions with status labels (done, running, undone), Undo per action where possible, and a stated undo window.
- Sources: https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ (Action Audit and Undo), Human-Centered AI (audit trails, from listing), https://elements.ai-sdk.dev/ (Checkpoint, Task)
- Status: COVERED. ai-interfaces.md (running log, Undo "for a period after the action, stated in the interface").

AG-6. Oversight must not become rubber-stamping: ask once per consequential action, batch low-risk steps, highlight what is unusual, and keep the review effort smaller than doing the task by hand; set the accuracy bar by the stakes.
- Sources: https://www.nngroup.com/articles/definition-ai-agent/, https://www.youtube.com/watch?v=LCEmiRjPEtQ (keep AI on a leash, from summaries)
- Status: MISSING-GUIDE. ai-interfaces.md.

AG-7. Show cost before an expensive run (credits, money, time), and offer a cheap draft mode for exploring before the final.
- Sources: https://www.shapeof.ai/ (Cost estimates, Draft mode)
- Status: MISSING-GUIDE. ai-interfaces.md.

AG-8. Never automate destructive or hard-to-undo actions (deleting, buying) without confirmation; never widen permissions silently.
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai, ai-interfaces.md
- Status: COVERED. ai-interfaces.md.

AG-9. The AI component set has a known vocabulary with states: conversation, message, prompt input, reasoning, sources and inline citation, tool call (running, approved, denied), plan, queue, confirmation, checkpoint, context meter, loading shimmer. Each needs its empty, streaming, stopped and error states designed.
- Sources: https://elements.ai-sdk.dev/, https://www.shapeof.ai/
- Status: MISSING-GUIDE. references/components/library.md: add AI component contracts with their states, so /ux-component can generate them from the system's tokens instead of a chat kit.

AG-10. Assistants should leave people more capable, not de-skilled: show the reasoning a person needs to learn the task, and offer to let them do the step themselves.
- Sources: Designing Assistant Technology (https://rosenfeldmedia.com/books/designing-assistant-technology/, from author pages), Designing Agentive Technology (https://rosenfeldmedia.com/books/designing-agentive-technology/, from description), https://wattenberger.com/thoughts/boo-chatbots/
- Status: MISSING-GUIDE (low). ai-interfaces.md.

## 7. Disclosure, responsible AI and compliance

DS-1. Tell people they are dealing with an AI unless that is obvious to a reasonably observant person (Article 50(1), a provider duty).
- Sources: https://artificialintelligenceact.eu/article/50/, https://developer.apple.com/design/human-interface-guidelines/generative-ai
- Status: guidance COVERED in ai-interfaces.md; MISSING-CHECK `ai-chat-no-disclosure` (static lint, advisory). Detection: a page with a prompt input and send button, or a chat launcher, where no visible text in the chat region or on the first screen matches /\bAI\b|assistant|automated|generated|bot\b/i.

DS-2. The disclosure must be clear and distinguishable, given no later than the first interaction or exposure, and meet applicable accessibility requirements (Article 50(5)). An icon alone, or text only in a tooltip, does not meet that bar.
- Sources: https://artificialintelligenceact.eu/article/50/
- Status: MISSING-GUIDE. ai-interfaces.md: name the timing and accessibility clause; the check side is DS-1 plus existing `inline-svg-no-aria`.

DS-3. Machine-readable marking of synthetic audio, image, video and text is a duty of the provider of the generating system (Article 50(2)); deployers must disclose deepfakes and AI text published on matters of public interest unless it had human editorial review (Article 50(4)). A page that shows AI images should keep the provenance metadata the generator attached rather than strip it.
- Sources: https://artificialintelligenceact.eu/article/50/, https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations, https://www.shapeof.ai/ (Watermark)
- Status: MISSING-GUIDE. ai-interfaces.md, compliance paragraph; and references/styles/product-illustration.md: image pipelines must not strip embedded provenance metadata from generated images. Optional MISSING-CHECK is not proposed: metadata in binary assets is outside a page linter.

DS-4. Say what happens to what people type or upload (stored, how long, used for training) next to the input; never pre-tick consent to training.
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai, https://maze.co/ (states it does not train on customer data), https://www.shapeof.ai/ (Consent, Data ownership)
- Status: COVERED. ai-interfaces.md "Respect what people share" and `consent-prechecked`.

DS-5. Do not infer personal attributes; ask for what is needed, and test with diverse people for stereotypes. For forms, a gender question offers more than two options and a way to decline, or is not asked.
- Sources: https://developer.apple.com/design/human-interface-guidelines/generative-ai (avoid assumptions about people), https://pair.withgoogle.com/explorables/ (hidden bias, datasets have worldviews), https://www.ibm.com/design/ai/ethics/ (fairness)
- Status: MISSING-CHECK `gender-choice-binary-only` (static lint, advisory). Detection: a select or radio group whose label or name matches /gender|sex/i and whose option set is exactly {male, female} (or man, woman) with no third option and no "prefer not to say".

DS-6. Decisions about people (scores, approvals, rankings) show the main factors behind the outcome and a route to a human to contest it.
- Sources: Weapons of Math Destruction (https://www.penguinrandomhouse.com/books/241363/weapons-of-math-destruction-by-cathy-oneil/, from description), AI Snake Oil (https://press.princeton.edu/books/hardcover/9780691249131/ai-snake-oil, from description), https://www.ibm.com/design/ai/ethics/ (accountability, explainability)
- Status: MISSING-GUIDE. ai-interfaces.md, new bullet under "Keep a person in charge".

DS-7. Penalties for breaching Article 50 reach EUR 15 million or 3% of worldwide annual turnover, whichever is higher (Article 99(4)); the README states the same figure.
- Sources: https://artificialintelligenceact.eu/article/50/ (README claim), checked against the Act's penalties article.
- Status: COVERED as context only: ai-interfaces.md rightly says how the Act applies is a legal question for the product's owners. No check.

## 8. AI in the design workflow (tools)

WF-1. Synthetic users are not evidence: across 12 peer-reviewed comparisons there were 9 encouraging and 14 discouraging findings; one study replicated 3 of 14 classic results; synthetic answers show reduced variance and exaggerated effects. Use them for directional hypotheses only.
- Sources: https://measuringu.com/review-of-experiments-with-synthetic-users/, https://dovetail.com/ (sells "Digital Twins")
- Status: MISSING-GUIDE. references/process/discovery-protocol.md: any persona or user quote produced by a model is labelled as a hypothesis, never as research.

WF-2. Evaluate by error analysis first: read real outputs, note the first failure in each, group failures into categories, then write one pass/fail check per failure mode and validate each check against human labels, tracking both true positive and true negative rates.
- Sources: https://hamel.dev/blog/posts/evals-faq/
- Status: MISSING-CHECK (meta) `rule-calibration-fixtures`. Every lint and render rule ships with labelled positive and negative fixtures, and the test suite reports per-rule TPR and TNR; a rule below a set floor is held back from the default pack. This is how a deterministic linter earns trust; ux-skill's rules are exactly the "code-based evaluators" this source recommends.

WF-3. Prompt-to-UI generators converge on their defaults when given no system: v0 emits Next.js, Tailwind and shadcn/ui; Lovable and Stitch are similar. Tools that read your components, tokens and guidelines (Figma Make, Builder.io) produce output that matches the shipped product. Lesson for ux-skill: emit tokens and component contracts first, then lint the generated page; do not depend on a model to remember them.
- Sources: https://v0.app/, https://lovable.dev/, https://stitch.withgoogle.com/, https://www.figma.com/make/, https://www.builder.io/use-cases/design-to-code
- Status: COVERED. `shadcn-default-everywhere`, `default-font-only`, references/styles/anti-slop.md, engine/foundations (token emit), engine/existing (detect the existing system), references/process/refactor-existing.md.

WF-4. Research tools (Dovetail, Looppanel, Maze) speed transcription and theming; their accuracy figures are vendor claims, and theme detection is a starting point for human synthesis.
- Sources: https://dovetail.com/, https://www.looppanel.com/, https://maze.co/
- Status: COVERED (out of linter scope). commands/ux-research.md (--synthesize, anti-bias by default) keeps synthesis a method the person runs.

WF-5. Generated imagery stays coherent when it comes from one reusable style reference rather than ad hoc prompts.
- Sources: https://www.recraft.ai/, https://www.krea.ai/
- Status: COVERED. references/styles/product-illustration.md, `photo-grade-off` (render).

## 9. Accessibility (Advanced Design Techniques)

Most lessons in this block repeat what the inventory already lists (section A). They are listed with the inventory id and not counted as new.

A-1. Touch targets 44px or 10mm (digital.gov) vs WCAG 2.5.8 AA 24px. Status: COVERED by `target-too-small` and inventory A6, A7. Number conflict logged in section 12.
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design

A-2. 16px minimum body text. Status: COVERED (typography.md mobile floors; inventory D3, D4).
- Sources: https://xd.adobe.com/ideas/principles/web-design/what-is-accessible-design/

A-3. Contrast 4.5:1 normal, 3:1 large; no colour-only meaning; no more than three flashes a second; pause moving content; 200% zoom. Status: COVERED (`text-low-contrast`, `moving-content-without-pause`, color.md) or already proposed (inventory A10, A13).
- Sources: https://www.ramotion.com/blog/accessibility-in-ux-design/, https://uxmag.com/articles/accessibility-in-ux-the-case-for-radical-empathy, https://ixdf.org/literature/topics/accessibility

A-4. Map landmarks (header, nav, main, footer, search) and give every page a main region.
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design, https://ixdf.org/literature/topics/accessibility
- Status: guidance COVERED (accessibility.md principle 5 and Skip link pattern); MISSING-CHECK `main-landmark-missing` (static lint, advisory). Detection: a full page (has html and body) with no `<main>` and no `[role=main]`. WCAG note: landmarks are a sufficient technique for 1.3.1 and 2.4.1, not a requirement on their own, so keep this advisory.

A-5. Avoid text inside images; where unavoidable, make it at least 14pt with strong contrast. Live text also translates.
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design, https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/
- Status: MISSING-GUIDE. references/foundations/accessibility.md (Alt text discipline). WCAG 1.4.5 Images of Text (AA) asks for real text where the technology can render the same visual presentation, except logotypes and essential cases.

A-6. Design in layers: the basic version works on the simplest technology, and richer behaviour is added on top.
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design
- Status: MISSING-CHECK `content-needs-script` (render, advisory). Detection: render once with JavaScript disabled; flag when visible text length is under 20% of the scripted render, or when no link or heading is present. Low priority for app shells; useful for landing pages and docs.

A-7. Place primary actions where a thumb reaches on phones (lower part of the screen).
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design
- Status: MISSING-GUIDE (low). references/foundations/responsive.md or interaction.md (no "thumb" guidance found in either).

A-8. Keyboard: every control reachable by Tab in a logical order, links on Enter, buttons on Space or Enter, visible focus, skip link. Status: COVERED (`focus-ring-missing`, `tabindex-positive`, `div-onclick-no-role`, `link-onclick-no-href`, accessibility.md).
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design, https://blog.logrocket.com/ux-design/how-to-build-accessible-design-system/

A-9. Icons pair with visible text labels. Status: already proposed (inventory F7).
- Sources: https://blog.logrocket.com/ux-design/how-to-build-accessible-design-system/

A-10. Check what a screen magnifier user sees by viewing through a narrow window. Status: already proposed (inventory A8, 320px reflow).
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design

A-11. Limit questions per page and give context cues in long forms. Status: already proposed (inventory B10).
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design

A-12. Include people with disabilities in personas, research and testing, using their own device settings. Status: MISSING-GUIDE (low). references/process/discovery-protocol.md.
- Sources: https://digital.gov/guides/accessibility-for-teams/ux-design, https://xd.adobe.com/ideas/principles/web-design/what-is-accessible-design/, https://www.ramotion.com/blog/accessibility-in-ux-design/

A-13. Elevation or colour is never the only cue for importance or state. Status: COVERED (color.md, dashboard.md "a state always shows its word").
- Sources: https://blog.logrocket.com/ux-design/how-to-build-accessible-design-system/

A-14. Permanent, temporary and situational impairments (one hand, bright sun) all count. Status: COVERED (accessibility.md "Common courtesy").
- Sources: https://ixdf.org/literature/topics/accessibility, https://uxmag.com/articles/accessibility-in-ux-the-case-for-radical-empathy

## 10. Internationalization

I-1. Expansion depends on string length. Per the W3C summary of IBM guidance, English strings up to 10 characters grow to about 200 to 300% of their length in translation, 11 to 20 to 180 to 200%, and text over 70 characters to about 130%. Buttons, tabs and labels break first.
- Sources: https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/ (German "user" about twice, French about three times), https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/ ("New!" 4 characters vs "Nouveau!" 9), primary check: https://www.w3.org/International/articles/article-text-size
- Status: MISSING-CHECK `pseudo-locale-overflow` (render; supersedes inventory E25 with corrected numbers). Detection: before the overflow checks, replace each visible text node with an accented copy padded by length band (<=10 chars x3, 11 to 20 x2, 21 to 70 x1.6, >70 x1.3) and with one 24-character unbroken word in headings and buttons; re-run `text-overflows-its-box`, `horizontal-overflow` and a clipped-text check. Also MISSING-GUIDE: references/foundations/accessibility.md says "30 to 50% longer", which holds only for long text.

I-2. Compound words in German, Dutch and Finnish do not wrap in narrow boxes; long tokens need a wrap rule (overflow-wrap, hyphens with a lang attribute).
- Sources: https://www.w3.org/International/articles/article-text-size (checked), https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/
- Status: folded into I-1's unbroken-word injection (no separate check).

I-3. CJK text needs larger minimum sizes and taller line height; Thai and some other scripts need more vertical space (W3C cites about 150% for Thai). Set type minimums per locale.
- Sources: https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/, https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/, https://www.w3.org/International/articles/article-text-size
- Status: MISSING-GUIDE. references/foundations/typography.md (per-script floors).

I-4. Mirror the interface for right-to-left languages with logical properties; swap next and back; mirror directional icons (arrows), not symbols that are not directional.
- Sources: https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/
- Status: guidance COVERED (accessibility.md "Multi-language and RTL support"). MISSING-CHECK `physical-direction-properties` (static lint, advisory, only when the project ships more than one locale or any dir="rtl"). Detection: count margin-left/right, padding-left/right, left/right offsets, text-align:left/right and border-left/right declarations in authored CSS; flag when they outnumber their logical equivalents.

I-5. A purely numeric date such as 10/02/2022 reads as different days in the US and Europe; use a month name or the locale's formatter.
- Sources: https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/
- Status: MISSING-CHECK `date-numeric-ambiguous` (static lint, text channel). Detection: visible text matching \b(0?[1-9]|1[0-2])[/.-](0?[1-9]|1[0-2])[/.-](\d{2}|\d{4})\b, where both leading parts could be a month.

I-6. Numbers, currency and negatives vary by locale (separators, currency after the amount in some markets, -527 vs (527)); format through the locale API, never by string concatenation.
- Sources: https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/, https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/
- Status: COVERED (accessibility.md: number and date formatting locale-aware).

I-7. Names and addresses differ by culture (surname first, two family names, no postal code); a single full-name field is safest.
- Sources: https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/, https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/
- Status: inventory B18 lists this as guidance; MISSING-CHECK `name-split-required` (static lint, advisory) is new. Detection: a form with required inputs whose name, id or autocomplete is given-name and family-name (or first and last) and no single name field.

I-8. Symbols and gestures are cultural: a thumbs-up is offensive in some regions, red means luck in China and danger elsewhere, the first day of the week varies.
- Sources: https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/, https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/
- Status: MISSING-GUIDE. accessibility.md "Multi-language and RTL support". Note the tension with AI feedback controls, where thumbs up/down is standard (Apple HIG names it); offer labelled buttons ("Useful", "Not useful") in localized products.

I-9. Keyboard shortcuts depend on the keyboard layout; single-character shortcuts also trap speech-input users.
- Sources: https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/
- Status: MISSING-CHECK `single-key-shortcut` (static lint on scripts). Detection: a keydown or keypress handler comparing e.key or e.code to a single printable character with no check of ctrlKey, metaKey or altKey and no surrounding setting to turn it off. WCAG 2.1.4 Character Key Shortcuts (A) requires that such a shortcut can be turned off, remapped, or works only while the control has focus.

I-10. A translation can also be much shorter, leaving awkward gaps in fixed-size layouts.
- Sources: https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/, https://www.w3.org/International/articles/article-text-size
- Status: MISSING-GUIDE (low). accessibility.md (layouts must flex both ways).

## 11. Design systems

S-1. A design system is three things: a style guide, a component library and a pattern library; adopting or adapting an existing system is cheapest, and heavy customisation erodes the saving.
- Sources: https://www.nngroup.com/articles/design-systems-101/, https://ixdf.org/literature/topics/design-systems, https://www.youtube.com/watch?v=rO5dBA-avfw
- Status: COVERED. references/components/library.md, references/brands/, engine/foundations.

S-2. Values live in named tokens referenced by components, so one change propagates.
- Sources: https://ixdf.org/literature/topics/design-systems, https://designsystemfoundations.com/ (from author page), https://ant.design/ (semantic tokens), https://primer.style/ (primitives)
- Status: COVERED. color.md principle 2, `class-multiple-utility-than-token`, `size-outside-system`, `weight-outside-system`.

S-3. Document the allowed text and background pairs, and validate each pair for contrast.
- Sources: https://blog.logrocket.com/ux-design/how-to-build-accessible-design-system/
- Status: COVERED. engine/foundations (color and validation modules emit and check role pairs), `text-low-contrast` at render.

S-4. An icon has one reserved meaning across the product, and one meaning has one icon.
- Sources: https://www.designsystemchecklist.com/ (Iconography: reserved uses, naming, keywords)
- Status: MISSING-CHECK `icon-meaning-inconsistent` (static lint). Detection: map each icon identity (lucide or heroicons import name, sprite href, or svg path hash) to the accessible names of the controls that use it; flag one icon with two or more unrelated names, or one action name with two different icons. Sits beside `one-action-several-labels` and `repeated-action-same-name`.

S-5. Typography performance is part of the system: load few font files.
- Sources: https://www.designsystemchecklist.com/ (Typography: performance), https://developer.apple.com/design/resources/ (one system family in several weights)
- Status: MISSING-CHECK `font-files-over-budget` (static lint). Detection: count distinct family and weight pairs requested through @font-face, Google Fonts css2 URLs and next/font calls; flag more than 4. Distinct from `weight-outside-system`, which polices use, not loading.

S-6. Elevation includes a z-axis layering scale for overlays, not ad hoc z-index values.
- Sources: https://www.designsystemchecklist.com/ (Elevation: z-axis layering)
- Status: COVERED. engine/foundations/elevation.py (role to z-index order), `arbitrary-z-index-9999`.

S-7. Component docs list every state (hover, focus, disabled, loading, error) and usage rules.
- Sources: https://www.nngroup.com/articles/design-systems-101/, https://designsystemfoundations.com/
- Status: COVERED. references/foundations/components.md "Component documentation requirements".

S-8. Design with realistic content and annotate focus order in the design itself (Fluent ships plugins for both).
- Sources: https://fluent2.microsoft.design/
- Status: COVERED for content (`fake-name-john-doe`, `lorem-ipsum-leak`, anti-slop.md content fingerprint); focus-order annotation is MISSING-GUIDE (low) in references/foundations/accessibility.md (Keyboard navigation).

S-9. Match icon weight and size to the adjacent text (SF Symbols come in nine weights and three scales for this reason).
- Sources: https://developer.apple.com/design/resources/
- Status: MISSING-GUIDE. references/foundations/components.md (no icon-to-text weight rule found).

S-10. Major systems now publish AI patterns inside the system (Carbon for AI, Atlassian Rovo, SLDS agentic): AI surfaces use the system's tokens, not a separate chat kit.
- Sources: https://www.carbondesignsystem.com/, https://atlassian.design/, https://www.lightningdesignsystem.com/2e1ef8501/p/03c548-agentic-patterns
- Status: COVERED. ai-interfaces.md "Look like the product, not like a chatbot template".

## 12. Number checks and conflicts

- Text expansion. ux-skill accessibility.md says translations "may be 30 to 50% longer"; inventory E25 says +30 to 40%. The W3C article (citing IBM) gives about 130% for strings over 70 characters (+30%) but 200 to 300% for strings up to 10 characters. The W3C table itself prints 151 to 170% for 51 to 70 characters, above the 31 to 50 band; that row looks like a typo in the source, so verify against IBM's original before quoting it. Recommendation: length-banded padding (I-1).
- Streaming scroll. ai-interfaces.md says "Auto-scroll only while the person is already at the bottom." NN/g guideline 7 says do not scroll to the bottom for long streamed answers; keep the view at the start of the new message. Recommendation: when a new answer starts, scroll its first line to the top of the view once, then stop following; follow the bottom only for short answers.
- Confidence display. ai-interfaces.md forbids percentage confidence unless calibrated. Yocco proposes a visible confidence level (for example 95%) with a calibration target above 0.8. Compatible only if the number is calibrated; NN/g warns confident presentation inflates trust. Keep ux-skill's rule.
- Agentic metrics. Yocco's targets (plan acceptance above 85%, override above 10% triggers review, reversion under 5%, escalation 5 to 15%, recovery above 90%, undo window example 15 minutes) are the author's suggested product metrics, not research findings. Use as starting points, not thresholds in a linter.
- Citations. README: users "almost never click" citations. NN/g: they rarely click; no percentage given.
- AI Act. README: "since 2 August 2026, the EU AI Act requires AI-generated content to be machine-readably marked". Article 50(2) places marking on providers of generative systems; deployers (most sites that show AI output) have the disclosure duties in 50(1) via providers, 50(3) and 50(4). The README conflates the two. The Article 50 page also shows an amended version of paragraph 7, so the code-of-practice mechanics may change; the application date of 2 August 2026 is as stated on the page. Penalty figure (EUR 15 million or 3%) matches.
- Touch targets. digital.gov says 44px or 10mm; WCAG 2.5.8 AA is 24 by 24 CSS px; 2.5.5 AAA is 44. Same conflict already logged in the inventory; keep 24 hard, 44 advisory on touch.
- Critique group size. Toptal 5 to 7, UXPin 3 to 7. Not in conflict.
- UX for AI. Wiley's page cites an 85% failure rate for AI initiatives without a source on the page. Do not repeat it as fact.
- Synthetic users. MeasuringU counts 9 encouraging and 14 discouraging findings across 12 papers (findings, not papers, so the counts exceed 12).
- Looppanel's 95% transcript accuracy across 96+ languages is a vendor claim.
- Credits in the README that do not match the target: row 9 (credited to InVision; the live video is from "This is HCD" with a different title), row 109 (credited to CareerFoundry; it is an IxDF page), row 125 (the description is copied from a video row about contrast and clickable areas, not the Dropbox article). The Anthropic agents article now redirects from /engineering/ to /research/.
- Ramotion recommends sans serif for body text only. ux-skill's typography allows serif body text; this is opinion, not a standard. No change.

## 13. Proposed checks in this part

| Id | Kind | Lesson | One-line detection |
|---|---|---|---|
| prompt-placeholder-ask-anything | lint (text) | AI-1 | prompt input placeholder or label matches "ask me anything", "how can I help", "type a message" |
| progress-text-generic | lint (text) | EX-5 | status/live region whose only text is Processing, Thinking, Loading, Please wait, Generating |
| chat-launcher-more-than-one | render | EX-10 | 2+ fixed-position buttons named chat, assistant, ask, help or support |
| citation-label-generic | lint (advisory) | TR-1 | link text is "Source", "Link" or a bare number with no naming aria-label or title |
| ai-caveat-far-from-input | render | TR-4 | no "may make mistakes / check" text within 160px of the prompt input on the first screen, or only in footer or tooltip |
| chat-scrolls-to-bottom | lint (script, advisory) | ER-5 | unguarded scrollTop = scrollHeight or scrollIntoView end inside a stream handler |
| ai-answer-actions-missing | lint (advisory) | ER-11 | assistant message with no Copy, Regenerate, Retry or Edit control |
| dialog-button-ok | lint | AG-2 | button inside dialog or alertdialog whose whole text is OK, Yes, Confirm, Sure, Proceed |
| ai-chat-no-disclosure | lint (advisory) | DS-1 | prompt input or chat launcher present, no visible "AI", "assistant", "automated", "generated" text |
| gender-choice-binary-only | lint (advisory) | DS-5 | gender or sex choice offering exactly male and female, no other or decline option |
| rule-calibration-fixtures | meta (tests) | WF-2 | each rule has labelled positive and negative fixtures; suite reports TPR and TNR per rule |
| main-landmark-missing | lint (advisory) | A-4 | full page with no main element and no role=main |
| content-needs-script | render (advisory) | A-6 | no-JS render has under 20% of the scripted text or no heading and link |
| pseudo-locale-overflow (upgrades inventory E25) | render | I-1 | length-banded padding plus a long unbroken word, then re-run overflow and clip checks |
| physical-direction-properties | lint (advisory) | I-4 | in multi-locale or RTL projects, physical left/right declarations outnumber logical ones |
| date-numeric-ambiguous | lint (text) | I-5 | dd/mm vs mm/dd ambiguous numeric date in visible text |
| name-split-required | lint (advisory) | I-7 | required given-name and family-name inputs with no single name field |
| single-key-shortcut | lint (script) | I-9 | key handler on a single printable key with no modifier and no off switch (WCAG 2.1.4) |
| icon-meaning-inconsistent | lint | S-4 | one icon used for two different action names, or one action with two icons |
| font-files-over-budget | lint | S-5 | more than 4 family-weight pairs requested |

Counting: 20 rows, of which `pseudo-locale-overflow` upgrades inventory E25 (same measurement, corrected length-banded numbers) and so is not counted as new. New checks in this part: 19. Two lessons also name a complaints probe usable today before the rule exists: ER-11 (kind "present", a Regenerate button selector) and TR-4 (kind "text-present", the caveat phrase).

---

## Ledger: every link in the block (162)

Status key: read (page fetched and read); summarized from description (books, videos, script-shell pages: publisher, author or listing text, README description, and for videos a live oEmbed check); blocked, summarized from description (HTTP 403 to fetch, counted under summarized); tool noted (product page read for what it does); dead (HTTP 404); out of scope (unauthorized mirrors of paid books, not opened).

Totals: 162 links. read 51; summarized from description 70 (60 plus 10 blocked); tool noted 12; dead 1; out of scope 28.

| # | Title | URL | Type | Status | Takeaway |
|---|---|---|---|---|---|
| 1 | Basics Design 08: Design Thinking (Ambrose, Harris) | https://www.goodreads.com/book/show/20594015-basics-design-08 | book | summarized from description | Goodreads page read: design as practical problem solving from brief to finished piece; no checkable rule. |
| 2 | Mirror: Basics Design 08 | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 3 | Design Thinking: NPD Essentials from the PDMA (Luchs, Swan, Griffin) | https://www.goodreads.com/book/show/27270256-design-thinking | book | summarized from description | Goodreads page read: structured creativity toward a clearly defined problem; process, not page checks. |
| 4 | Mirror: PDMA Design Thinking | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 5 | What is Design Thinking? (IxDF) | https://ixdf.org/literature/topics/design-thinking | article | read | Five phases, non-linear; pitfalls: constraints first, company-centred framing, perfectionism. |
| 6 | The 5 Phases of Design Thinking (AMA) | https://www.ama.org/marketing-news/the-5-phases-of-design-thinking/ | article | read | How Might We framing; test to refine, not to prove; ask how to test an idea fast. |
| 7 | The 5 Stages in the Design Thinking Process (IxDF) | https://ixdf.org/literature/article/5-stages-in-the-design-thinking-process | article | read | Output per stage; diverge (brainstorm, worst idea) then converge (SCAMPER); test can reopen define. |
| 8 | A Complete Guide to the Design Thinking Process (CareerFoundry) | https://careerfoundry.com/en/blog/ux-design/design-thinking-process/ | article | read | POV statement from the user's side; keep checking ideas against it while narrowing. |
| 9 | 5 Stages of the Design Thinking Process (listed as InVision) | https://www.youtube.com/watch?v=Vg8koqyQ52E | video | summarized from description | Live, but oEmbed shows a different title and channel ('The Design Thinking Process (2024)', This is HCD): README credit is stale. |
| 10 | Design Thinking Full Course (Simplilearn) | https://www.youtube.com/watch?v=4nTh3AP6knM | video | summarized from description | Long intro course; empathy maps, five phases, agile pairing. No new lesson. |
| 11 | ADVANCED DESIGN PROCESS: MUST KNOW!! (Satori Graphics) | https://www.youtube.com/watch?v=YzSooKa1PwM | video | summarized from description | Graphic designer's personal process; out of scope for UI checks. |
| 12 | UX Design Process: Empathize, Define, Ideate (My Lesson) | https://www.youtube.com/watch?v=7V8k4uwAll8 | video | summarized from description | Course part 2/7 on the first three phases; duplicates articles. |
| 13 | The Design Thinking Process, Explained by an Expert (CareerFoundry) | https://www.youtube.com/watch?v=FrsQSplB_Cg | video | summarized from description | Design thinking as mindset plus process, applied beyond design; duplicates article 8. |
| 14 | Discussing Design (Connor, Irizarry) | https://www.goodreads.com/book/show/25173297-discussing-design | book | summarized from description | Critique as goal-referenced analysis, not authority or taste; already the basis of /ux-critique (inventory H12). |
| 15 | Mirror: Discussing Design | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 16 | Productive design critique guide (Toptal) | https://www.toptal.com/designers/product-design/productive-design-critique-guide | article | read | Roles (presenter, facilitator, note-taker, 5 to 7 critiquers); set goals and fidelity first; problems before solutions. |
| 17 | Design Critiques (NN/g, Gibbons) | https://www.nngroup.com/articles/design-critiques/ | article | read | Round robin or quotas; rotate facilitator; reword directives as goal-linked questions; summary with actions. |
| 18 | What is a Design Critique (UXPin) | https://www.uxpin.com/studio/blog/what-is-design-critique/ | article | read | Written agenda, share prototype early, 3 to 7 panelists, close the loop on what changed. |
| 19 | 5 Do's and Don'ts of Design Critique (Adobe XD Ideas) | https://xd.adobe.com/ideas/process/ui-design/design-critique-tips/ | article | read | Explain reasoning, tie to goals, propose alternatives, critique the design not the designer. |
| 20 | Design critiques at Figma (Levin) | https://www.figma.com/blog/design-critiques-at-figma/ | article | read | Six formats incl. silent critique; about 2 minutes per person; at most two topics per hour. |
| 21 | A practical guide for design critiques (UX Planet, Galvan) | https://uxplanet.org/a-practical-guide-for-design-critiques-ea72028de8bb | article | blocked, summarized from description | Medium returned 403. Listed description only: what to look for when giving and receiving critique. |
| 22 | Design Feedback in Action (Grow with Google) | https://www.youtube.com/watch?v=VLwZc0JNAT8 | video | summarized from description | Mock critique turning feedback into actions; duplicates 16 to 20. |
| 23 | Websites Design Critique: Student Work (Flux Academy) | https://www.youtube.com/watch?v=E84GpsDuaS0 | video | summarized from description | Worked critique of student sites; example material, no new rule. |
| 24 | UX Design Critique live (DareIT) | https://www.youtube.com/watch?v=2AHNGaVg02w | video | summarized from description | Live structured critique; duplicates 16 to 20. |
| 25 | Behance: Fridge Recipes App case study | https://www.behance.net/gallery/153624479/Fridge-Recipes-App-UX-UI-Case-Study | other | blocked, summarized from description | Project inspiration for a course task; Behance 403. Out of scope for checks. |
| 26 | Behance: Fitness Mobile App | https://www.behance.net/gallery/120589209/Fitness-Mobile-App | other | blocked, summarized from description | Project inspiration for a redesign task; Behance 403. Out of scope for checks. |
| 27 | UX for AI (Nudelman, Kempka) | https://www.wiley.com/en-us/UX+for+AI:+A+Framework+for+Designing+AI-Driven+Products-p-9781394345922 | book | summarized from description | Wiley page read: framework from 35 AI projects; Digital Twin and Value Matrix exercises; cites an 85% AI project failure rate (unsourced on page). |
| 28 | Mirror: UX for AI | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 29 | AI and UX (Lew, Schumacher) | https://link.springer.com/book/10.1007/978-1-4842-5775-3 | book | summarized from description | Springer page redirects to login; per listing, AI adoption is gated by UX, not model quality. |
| 30 | Mirror: AI and UX | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 31 | AI Snake Oil (Narayanan, Kapoor) | https://press.princeton.edu/books/hardcover/9780691249131/ai-snake-oil | book | summarized from description | Princeton page 403; per description, separate AI that works from AI sold as working; predictive scoring of people is the weakest category. |
| 32 | Mirror: AI Snake Oil | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 33 | People + AI Guidebook (Google PAIR) | https://pair.withgoogle.com/guidebook/ | guideline | summarized from description | Home is a script shell with no text; its chapter on errors (row 62) was read. Method source for HAX-style guidance. |
| 34 | AI: First New UI Paradigm in 60 Years (Nielsen) | https://www.nngroup.com/articles/ai-paradigm/ | article | read | Intent-based outcome specification; articulation barrier (author estimates about half of people in rich countries); hybrid GUI plus intent. |
| 35 | A Concrete Definition of an AI Agent (NN/g) | https://www.nngroup.com/articles/definition-ai-agent/ | article | read | Agent = goal, iteration, actions on an environment, evaluation, self-direction; keep review effort low; stakes set accuracy bar. |
| 36 | Building Effective Agents (Anthropic) | https://www.anthropic.com/engineering/building-effective-agents | article | read | Workflows vs agents; start simple; show planning steps; human checkpoints and stop conditions. URL now redirects to /research/. |
| 37 | AI Is Your New Design Material (Josh Clark, AIGA) | https://www.youtube.com/watch?v=Hu5Jc1yIfas | video | summarized from description | Per AIGA listing: design with machine output and around its weird or wrong conclusions. |
| 38 | Software Is Changing (Again) (Karpathy, YC) | https://www.youtube.com/watch?v=LCEmiRjPEtQ | video | summarized from description | Per public summaries: autonomy slider, fast generate-verify loop, app-specific GUIs to audit output, keep AI on a leash. |
| 39 | Designing Human-Centric AI Experiences (Kore) | https://link.springer.com/book/10.1007/978-1-4842-8088-1 | book | summarized from description | Springer login redirect; per listing: onboarding, expectation setting, communicating confidence. |
| 40 | Mirror: Designing Human-Centric AI Experiences | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 41 | Human-Centered AI (Shneiderman) | https://books.google.com/books/about/Human_centered_AI.html?id=YS9VEAAAQBAJ | book | summarized from description | Google Books listing read: high human control with high automation; governance via audit trails and independent oversight. |
| 42 | Mirror: Human-Centered AI | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 43 | Guidelines for Human-AI Interaction (Microsoft HAX) | https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ | guideline | read | 18 guidelines across four phases (initially, during, when wrong, over time); page gives phases, library gives G1 to G18. |
| 44 | HAX Design Library (Microsoft) | https://www.microsoft.com/en-us/haxtoolkit/library/ | guideline | read | Filterable guidelines, patterns, examples; confirms 18 guidelines from 'make clear what the system can do' to 'notify users about changes'. |
| 45 | HIG: Generative AI (Apple) | https://developer.apple.com/design/human-interface-guidelines/generative-ai | guideline | read | Read via HIG JSON. Label AI, never imply a human; non-AI fallback; specific progress text; Edit/Undo/Retry near output; confirm irreversible actions. |
| 46 | Durable Patterns in AI Product Design (LukeW) | https://www.lukew.com/ff/2145/durable-patterns-in-ai-product-design | article | read | Follow-up suggestions, citations, context awareness, collapsed agent steps, process separated from results, AI-led onboarding. |
| 47 | The Shape of AI | https://www.shapeof.ai/ | guideline | read | Six pattern families (wayfinders, inputs, tuners, governors, trust builders, identifiers); ready-made vocabulary for an AI component set. |
| 48 | Claude Console | https://platform.claude.com/ | tool | tool noted | Sign-in page for Anthropic's developer platform; lesson: test real model output, including failures, before designing around it. |
| 49 | Sentient Design (Clark, Kindred) | https://rosenfeldmedia.com/books/sentient-design/ | book | summarized from description | Publisher page 403; per publisher and interviews: experience postures (tools, chat, agents, copilots and more). |
| 50 | Mirror: Sentient Design | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 51 | Designing AI Interfaces (Macfadyen) | https://www.oreilly.com/library/view/designing-ai-interfaces/9798341639812/ | book | summarized from description | O'Reilly 403; per listings: patterns from content moderation to interruptibility for agentic systems. |
| 52 | Mirror: Designing AI Interfaces | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 53 | Explainable AI in Chat Interfaces (NN/g) | https://www.nngroup.com/articles/explainable-ai/ | article | read | People rarely click citations; citations raise perceived reliability anyway; reasoning traces can be post-hoc; disclaimers belong near the input. |
| 54 | Design Patterns for AI Interfaces (Smashing, Friedman) | https://www.smashingmagazine.com/2025/07/design-patterns-ai-interfaces/ | article | read | Controls over prompts for refinement, contextual edits on a selection, forced ranking, presets, AI-second. |
| 55 | Design for AI: Everyday Ethics (IBM) | https://www.ibm.com/design/ai/ethics/ | guideline | read | Five focal areas (accountability, value alignment, explainability, fairness, user data rights); page gives headings only. |
| 56 | IBM Carbon AI Label | https://www.carbondesignsystem.com/building-blocks/core/components/ai-label/guidelines | tool | dead | 404. Current guidance read at carbondesignsystem.com/guidelines/carbon-for-ai/: AI label opens explainability popover; human-edited state; revert to AI; AI styling not decoration. |
| 57 | PAIR Explorables | https://pair.withgoogle.com/explorables/ | tool | read | Interactive essays; most relevant: 'Are model predictions probabilities?' (calibration) and confident wrongness out of distribution. |
| 58 | Conversations with Things (Deibel, Evanhoe) | https://rosenfeldmedia.com/books/conversations-with-things/ | book | summarized from description | Rosenfeld 403; per reviews: conversation design for chat and voice, useful, ethical, human-centred; repair after misunderstanding. |
| 59 | Mirror: Conversations with Things | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 60 | Conversational Design (Erika Hall) | https://abookapart.com/products/conversational-design | book | summarized from description | A Book Apart page read: conversation as the model for interfaces; language as a design tool. |
| 61 | Mirror: Conversational Design | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 62 | Errors + Graceful Failure (Google PAIR) | https://pair.withgoogle.com/chapter/errors-failing/ | guideline | read | Error taxonomy: context errors, failstates, background errors, unexpected input, breaking habituation, low confidence, irrelevance, competing systems. |
| 63 | Why Chatbots Are Not the Future (Wattenberger) | https://wattenberger.com/thoughts/boo-chatbots/ | article | read | Empty text box has no affordances; context belongs in the UI; chat answers stand alone so revisions are hard to track. |
| 64 | 10 Guidelines for Site AI Chatbots (NN/g) | https://www.nngroup.com/articles/ai-chatbots-design-guidelines/ | article | read | One chatbot, on every page, say what it does, clickable follow-ups, images, expandable details, do not scroll to bottom, resizable, save/share, voice. |
| 65 | Designing Agentive Technology (Noessel) | https://rosenfeldmedia.com/books/designing-agentive-technology/ | book | summarized from description | Rosenfeld 403; per publisher: software that acts for the user; monitoring, handoff and takeback. |
| 66 | Mirror: Designing Agentive Technology | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 67 | Designing Assistant Technology (Noessel) | https://rosenfeldmedia.com/books/designing-assistant-technology/ | book | summarized from description | Rosenfeld 403; per author pages: assistants that make users smarter, avoid de-skilling. |
| 68 | Mirror: Designing Assistant Technology | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 69 | Designing for Agentic AI (Smashing, Yocco) | https://www.smashingmagazine.com/2026/02/designing-agentic-ai-practical-ux-patterns/ | article | read | Intent Preview, Autonomy Dial, Explainable Rationale, Confidence Signal, Action Audit and Undo, Escalation Pathway, each with suggested metrics. |
| 70 | Say Hello to Sentient Design (Big Medium) | https://bigmedium.com/ideas/hello-sentient-design.html | article | read | Interfaces aware of context and intent; deferential: offer signals, not answers; design for failure and uncertainty. |
| 71 | Salesforce SLDS 2 Agentic Patterns | https://www.lightningdesignsystem.com/2e1ef8501/p/03c548-agentic-patterns | guideline | summarized from description | Page is a script shell with no readable text; listed as production agentic patterns. |
| 72 | Vercel AI Elements | https://elements.ai-sdk.dev/ | tool | read | Component vocabulary: Conversation, Message, PromptInput, Reasoning, Sources, InlineCitation, Tool, Plan, Confirmation, Checkpoint, Context, Shimmer. |
| 73 | Voiceflow | https://www.voiceflow.com/ | tool | tool noted | Agent builder for support teams; lesson: prototype conversation flows and split-test them before building. |
| 74 | Weapons of Math Destruction (O'Neil) | https://www.penguinrandomhouse.com/books/241363/weapons-of-math-destruction-by-cathy-oneil/ | book | summarized from description | Publisher returned 406; per description: opaque, unaccountable scoring harms those least able to contest it. |
| 75 | Mirror: Weapons of Math Destruction | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 76 | Atlas of AI (Crawford) | https://yalebooks.yale.edu/book/9780300264630/atlas-of-ai/ | book | summarized from description | Per publisher description: labour, minerals and energy behind models. Context, no page check. |
| 77 | Mirror: Atlas of AI | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 78 | Rethink Design (Giaccardi, Bendor, eds.) | https://books.open.tudelft.nl/home/catalog/book/110 | book | summarized from description | Open-access TU Delft page read (CC BY 4.0, 2024): 17 terms for designing with proactive, data-sharing systems. |
| 79 | EU AI Act Article 50 | https://artificialintelligenceact.eu/article/50/ | guideline or standard | read | Disclose AI interaction unless obvious; providers mark synthetic output machine-readably; deepfake and public-interest text disclosure; clear, by first exposure, accessible. |
| 80 | EC Guidelines on transparency of AI-generated content | https://digital-strategy.ec.europa.eu/en/policies/guidelines-ai-transparency-obligations | guideline or standard | read | Guidelines plus a Code of Practice; code adherence demonstrates marking and labelling compliance; no specific icon or watermark named on page. |
| 81 | Creative Prototyping with Generative AI (Pennefather) | https://link.springer.com/book/10.1007/978-1-4842-9579-3 | book | summarized from description | Springer login redirect; per listing: generative tools inside a prototyping workflow, where they help and where they waste time. |
| 82 | Mirror: Creative Prototyping with Generative AI | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 83 | Review of Experiments with Synthetic Users (MeasuringU) | https://measuringu.com/review-of-experiments-with-synthetic-users/ | article | read | 12 papers: 9 encouraging vs 14 discouraging findings; 3 of 14 classic studies replicated; synthetic data has reduced variance. |
| 84 | Evals FAQ (Hamel Husain) | https://hamel.dev/blog/posts/evals-faq/ | article | read | Error analysis first; binary pass/fail; one evaluator per failure mode; validate judges with labelled data and track TPR and TNR. |
| 85 | Figma Make | https://www.figma.com/make/ | tool | tool noted | Prompt to code-backed prototype; syncs npm packages, library styles and guidelines: output quality follows supplied design context. |
| 86 | Google Stitch | https://stitch.withgoogle.com/ | tool | tool noted | Page text is a shell ('Design with AI'); listed as text or sketch to UI with Figma and code export. |
| 87 | v0 by Vercel | https://v0.app/ | tool | tool noted | Prompt to Next.js, Tailwind, shadcn/ui; its defaults are the house look ux-skill flags as shadcn-default-everywhere. |
| 88 | Lovable | https://lovable.dev/ | tool | tool noted | 403 to fetch; listed as prompt to full-stack app. Same lesson as v0: generation without a system converges on defaults. |
| 89 | Builder.io design to code | https://www.builder.io/use-cases/design-to-code | tool | tool noted | Indexes components, tokens and icons so output reuses the shipped system; input quality (auto layout, components) matters. |
| 90 | Dovetail | https://dovetail.com/ | tool | tool noted | Research repository: transcription, themes, cited answers, and 'Digital Twins' of segments (see row 83 before trusting those). |
| 91 | Looppanel | https://www.looppanel.com/ | tool | tool noted | AI interview notes and repository; vendor claims about 95% transcript accuracy (unverified). |
| 92 | Maze | https://maze.co/ | tool | tool noted | AI moderator and analysis for testing; states research data is not used for training. |
| 93 | Recraft | https://www.recraft.ai/ | tool | tool noted | Editable vector output and a reusable style from your own images: one style reference keeps generated assets consistent. |
| 94 | Krea | https://www.krea.ai/ | tool | tool noted | Multi-model image, video and 3D generation, upscaling, LoRA training; asset generation, outside a page linter. |
| 95 | Practical Approaches for Designing Accessible Websites (Smashing) | https://www.smashingmagazine.com/ebooks/practical-approaches-for-designing-accessible-websites/ | book | summarized from description | eBook listing: accessibility treated with the same rigour as viewports and performance. |
| 96 | Mirror: Practical Approaches for Designing Accessible Websites | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 97 | Designing for Accessibility (Keates) | https://books.google.com/books/about/Designing_for_Accessibility.html?id=gXqHUN8g4FcC | book | summarized from description | Per listing: business case and method for countering design exclusion. |
| 98 | Mirror: Designing for Accessibility | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 99 | Inclusive Design for a Digital World (Gilbert) | https://books.google.com/books/about/Inclusive_Design_for_a_Digital_World.html?id=OfqTEQAAQBAJ | book | summarized from description | Per listing: inclusive design as intent to serve as many users as possible. |
| 100 | Mirror: Inclusive Design for a Digital World | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 101 | A Web for Everyone (Horton, Quesenbery) | https://www.goodreads.com/book/show/20640233-a-web-for-everyone | book | summarized from description | Per listing: universal design principles applied to sites, with personas of people with disabilities. |
| 102 | Mirror: A Web for Everyone | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 103 | Design for Inclusivity (Coleman et al.) | https://www.goodreads.com/book/show/3295983-design-for-inclusivity | book | summarized from description | Per listing: inclusive design benefits everyone, not only people with impairments. |
| 104 | Mirror: Design for Inclusivity | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 105 | Refactoring UI (Schoger, Wathan) | https://refactoringui.com/ | book | summarized from description | Already mined in PLAN-4.1-inventory (RUI rows D13, D14, E3, E9 and others). |
| 106 | Mirror: Refactoring UI | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 107 | What is Accessible Design? (Adobe XD Ideas) | https://xd.adobe.com/ideas/principles/web-design/what-is-accessible-design/ | article | read | 16px body minimum, contrast, test early with disabled users; cites 57 million Americans with disabilities. |
| 108 | How to build an accessible design system (LogRocket) | https://blog.logrocket.com/ux-design/how-to-build-accessible-design-system/ | article | read | Audit every component; document text/background pairs; icons with labels; elevation never the only cue; screen reader tests. |
| 109 | What is Accessibility? (IxDF; README credits CareerFoundry) | https://ixdf.org/literature/topics/accessibility | article | read | POUR; permanent, temporary and situational impairments; WAVE and Color Oracle checks. |
| 110 | Accessibility guidelines for UX Designers (uxdesign.cc, Kaur) | https://uxdesign.cc/accessibility-guidelines-for-a-ux-designer-c3ba775539be | article | blocked, summarized from description | Medium 403; listed description: treat accessibility requirements as design constraints. |
| 111 | Accessibility for UX designers (digital.gov) | https://digital.gov/guides/accessibility-for-teams/ux-design | guideline | read | Checklist: tab order map, landmarks, skip link, visible labels, text in images at least 14pt, targets 44px or 10mm, thumb reach. |
| 112 | Accessibility in UX: radical empathy (UX Magazine) | https://uxmag.com/articles/accessibility-in-ux-the-case-for-radical-empathy | article | read | Situational barriers; axe baseline; 200% zoom; keep primary actions visible rather than on hover. |
| 113 | Accessibility in UX Design (Ramotion) | https://www.ramotion.com/blog/accessibility-in-ux-design/ | article | read | 4.5:1 and 3:1 per WCAG 2.2 AA; no more than three flashes a second; label required fields and formats. |
| 114 | 7 Things Every Designer Needs to Know about Accessibility (Salesforce UX) | https://medium.com/salesforce-ux/7-things-every-designer-needs-to-know-about-accessibility-64f105f0881b | article | blocked, summarized from description | Medium 403; listed description only. |
| 115 | Designing for Accessibility: Top 3 Strategies (Liz Brown UX) | https://www.youtube.com/watch?v=hAoZI-yT4aU | video | summarized from description | Intro strategies; duplicates articles. |
| 116 | Accessible Web Design (Flux Academy) | https://www.youtube.com/watch?v=-ao_Kc_8rpE | video | summarized from description | Intro; duplicates articles. |
| 117 | Designing for Accessibility: Overview (Trillium) | https://www.youtube.com/watch?v=dJfhi2P60Xo | video | summarized from description | Intro; duplicates articles. |
| 118 | Design for Accessibility (Canva webinar) | https://www.youtube.com/watch?v=GGR8UDCdi14 | video | summarized from description | Graphic content accessibility; duplicates articles. |
| 119 | Design for Accessibility (UX Loop) | https://www.youtube.com/watch?v=4OuI6Qsh1D0 | video | summarized from description | Contrast, clickable area, content; covered by existing rules. |
| 120 | Designing for Accessibility (UA Technology Accessibility) | https://www.youtube.com/watch?v=Ww2wddAZUdU | video | summarized from description | Documents, images, audio, video basics; covered. |
| 121 | Usability and Internationalization of IT (Aykin) | https://books.google.com/books/about/Usability_and_Internationalization_of_In.html?id=Fyd50AEACAAJ | book | summarized from description | Per listing: cultural, language and economic factors in IT usability. |
| 122 | Mirror: Usability and Internationalization of IT | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 123 | Intercultural User Interface Design (Heimgartner) | https://books.google.com/books/about/Intercultural_User_Interface_Design.html?id=J0efDwAAQBAJ | book | summarized from description | Per listing: process for internationally usable HMIs from theory to implementation. |
| 124 | Mirror: Intercultural User Interface Design | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 125 | Design for internationalization (Dropbox Design, Saito) | https://medium.com/dropbox-design/design-for-internationalization-24c12ea6b38f | article | blocked, summarized from description | Medium 403. README description is wrong (copied from a video row about contrast and clickable areas). |
| 126 | Internationalization and Localization (UX Knowledge Base) | https://uxknowledgebase.com/internationalization-localization-d84795b7962c | article | blocked, summarized from description | Medium-hosted, 403; listed as a sketchnote of localization design aspects. |
| 127 | UX Localization (Phrase) | https://phrase.com/blog/posts/app-localization-developers-guide-to-user-experience/ | article | read | Expansion (German about 2x, French about 3x for one word), pseudo-loc at double length, CJK line height, RTL mirroring, formats, colour meaning. |
| 128 | Internationalization vs Localization (UXPin) | https://www.uxpin.com/studio/blog/internationalization-vs-localization-in-app-design/ | article | read | 'New!' 4 chars vs 'Nouveau!' 9; ambiguous 10/02/2022; negative number forms; currency position; live text not images. |
| 129 | Localization in UX (uxdesign.cc, Conte) | https://uxdesign.cc/beyond-text-translation-ux-design-and-localization-77b337b1f686 | article | blocked, summarized from description | Medium 403; listed description: culture and mindset beyond translation. |
| 130 | What Is Internationalization (Localization Academy) | https://www.youtube.com/watch?v=CIwNjfTlmgA | video | summarized from description | Whiteboard basics of i18n; duplicates articles. |
| 131 | How to make design really inclusive (Florence Okoye, TEDx) | https://www.youtube.com/watch?v=7M-VSI9RuPU | video | summarized from description | Empathy is not enough; design with, not for. Framing, no check. |
| 132 | 51. Designing for Internationalization: UI Design (ADF Architecture TV) | https://www.youtube.com/watch?v=ARx0hRNGfcU | video | summarized from description | Oracle ADF-specific UI i18n issues; framework-specific. |
| 133 | 50. Understanding Internationalization (ADF Architecture TV) | https://www.youtube.com/watch?v=wxwKxZW2edQ | video | summarized from description | i18n is more than translating the UI; framework-specific. |
| 134 | Practical UI Patterns for Design Systems (MacDonald) | https://books.google.com/books?id=E0efDwAAQBAJ | book | summarized from description | Per listing: choosing the right pattern for the job and context. |
| 135 | Mirror: Practical UI Patterns for Design Systems | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 136 | Laying the Foundations (Couldwell) | https://designsystemfoundations.com/ | book | summarized from description | Author page read: foundations model, naming, tokens, component states, keeping design and code in sync. |
| 137 | Mirror: Laying the Foundations | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 138 | Modular Web Design (Curtis) | https://www.oreilly.com/library/view/modular-web-design/9780321638311 | book | summarized from description | O'Reilly 403; per listing: reusable components and documentation instead of reinventing each screen. |
| 139 | Mirror: Modular Web Design | (unofficial mirror, link withheld) | other | out of scope | Unauthorized mirror of a paid book; not opened or used. |
| 140 | Everything you need to know about Design Systems (Hacq) | https://uxdesign.cc/everything-you-need-to-know-about-design-systems-54b109851969 | article | blocked, summarized from description | Medium 403; listed description only. |
| 141 | Design Systems 101 (NN/g) | https://www.nngroup.com/articles/design-systems-101/ | article | read | Style guide, component library, pattern library; adopt, adapt or build; heavy customisation erodes savings. |
| 142 | Design Systems (IxDF) | https://ixdf.org/literature/topics/design-systems | article | read | Tokens as named variables; components and patterns; maintenance and content rules. |
| 143 | What is a Design System? (DesignCourse) | https://www.youtube.com/watch?v=wc5krC28ynQ | video | summarized from description | Definitions and examples; covered. |
| 144 | Create a Design System with Figma (freeCodeCamp) | https://www.youtube.com/watch?v=RYDiDpW2VkM | video | summarized from description | Figma components course; tool tutorial. |
| 145 | Build it in Figma: Create a Design System (Figma) | https://www.youtube.com/watch?v=EK-pHkc5EL4 | video | summarized from description | Type scale, colour styles, grids as shared styles; covered by foundations. |
| 146 | Design Systems, Pattern Libraries and Style Guides (Showalter) | https://www.youtube.com/watch?v=rO5dBA-avfw | video | summarized from description | Differences between the three; covered by row 141. |
| 147 | 5 Best Design Systems (DesignerUp) | https://www.youtube.com/watch?v=BISC15OPeGA | video | summarized from description | Study public systems as teaching tools; covered by references/brands. |
| 148 | Design System Series playlist (Mizko) | https://www.youtube.com/playlist?list=PLvnhVb8yYRQ1rvEFiPEyNbVPiJxvuCbgL | video | summarized from description | Playlist live; Figma system-building series. |
| 149 | Design System Checklist | https://www.designsystemchecklist.com/ | template or kit | read | Read via its open data file: color, layout, typography, elevation (incl. z-axis), motion, iconography (incl. reserved uses). |
| 150 | Airbnb: Building a visual language | https://medium.com/airbnb-design/building-a-visual-language-behind-the-scenes-of-our-airbnb-design-system-224748775e4e | article | blocked, summarized from description | Medium 403; listed description only. |
| 151 | Atlassian Design System | https://atlassian.design/ | template or kit | read | Home read: foundations incl. tokens and accessibility; dedicated AI (Rovo) patterns. |
| 152 | IBM Design Language | https://www.ibm.com/design/language/ | template or kit | summarized from description | Page returns a shell; listed as IBM's principles and guidance. |
| 153 | Material Design 3 | https://m3.material.io/ | template or kit | summarized from description | Page returns a shell; already mined in inventory (M3 targets, motion). |
| 154 | Microsoft Fluent 2 | https://fluent2.microsoft.design/ | template or kit | read | Home read: Figma plugins for focus order, contrast checking, realistic content (Content Reel), icon scaling. |
| 155 | Polaris (Shopify) | https://shopify.dev/docs/api/polaris | template or kit | read | Now a web-components framework across admin, checkout, POS extensions. |
| 156 | Primer (GitHub) | https://primer.style/ | template or kit | read | Shared foundations: accessibility, Octicons, primitives (tokens). |
| 157 | Salesforce Lightning Design System | https://www.lightningdesignsystem.com/2e1ef8501 | template or kit | summarized from description | Page returns a shell; SLDS 2 per listing. |
| 158 | Ant Design | https://ant.design/ | template or kit | read | Enterprise React system; theming via semantic tokens that both people and AI tools consume. |
| 159 | Apple Design Resources | https://developer.apple.com/design/resources/ | template or kit | read | UI kits per platform; SF Symbols over 7,000 in nine weights and three scales. |
| 160 | AtlasKit | https://atlaskit.atlassian.com/ | template or kit | read | Examples page only; legacy name for Atlassian's React kit (row 151 is current). |
| 161 | Carbon Design System | https://www.carbondesignsystem.com/ | template or kit | read | Foundations incl. Carbon for AI, accessibility, motion; data visualization section. |
| 162 | Atomize | https://atomizecode.com/ | template or kit | read | Small React UI framework based on atomic design; no release dates shown. |

