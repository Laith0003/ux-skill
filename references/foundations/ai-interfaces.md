# Interfaces for AI features

A product that answers with a model has failure modes a form does not: answers that arrive slowly and in pieces, answers that are wrong with full confidence, actions taken on the person's behalf. This file sets what an AI feature's interface must do, whatever it looks like. It draws on the published guidelines for human-AI interaction from the major platform makers, public collections of AI interface patterns, and the transparency duties in Article 50 of the EU AI Act. It is guidance in our own words, not a restatement of any of them.

Load it beside the surface playbook (`references/surfaces/landing.md`, `dashboard.md` or `component.md`) whenever the product has a chat, an assistant, generated content or an agent that acts.

---

## Say what it is and what it can do

- Say plainly, at the point of use, that the answers come from an AI. Where a person might take generated text, images or audio for a human's or a real recording, label them. The EU AI Act asks that people be told when they interact with an AI system, and that generated or manipulated content be marked as such; how that applies to a given product is a legal question for its owners.
- Set expectations before the first question: what it is good at, what it does not know (its cut-off, the sources it reads), and one or two example prompts written for this product, not "Ask me anything".
- Never present the model as a person: no human name with a stock face, no "typing" theatre longer than the real wait.

## Show the work while it happens

- Answer the send at once: the message appears in the thread and the send control changes state within about 100ms.
- Stream long answers as they arrive, and keep the reading position stable: new text must not push what the person is reading off screen. Auto-scroll only while the person is already at the bottom.
- Give every running answer a visible **Stop** control that keeps what has arrived so far.
- For a long task, show which step it is on in words ("Reading 3 of 12 files"), not only a spinner.
- When it fails, say what failed and offer the next move (retry, shorten, rephrase), keeping the person's prompt in the box.

## Let the person correct it

- **Regenerate** and **edit the prompt** sit beside every answer. Editing a past prompt makes clear what happens to the answers after it.
- Generated text the person will use is editable in place, or copies cleanly (code with its formatting, tables as tables).
- Feedback (useful, not useful) is one action and optional, with a way to say why; it never interrupts the task.
- Keep a history the person can return to, and let them delete it.

## Show where an answer comes from, and how sure it is

- When an answer rests on sources (documents, the web, the person's data), cite them inline, next to the claim they support, and let the person open each one.
- Do not invent precision: no percentage confidence scores unless they are calibrated. Prefer words that change what the person does ("Check these figures before you send") and a visible difference between an answer from the person's own data and one from general knowledge.
- Numbers, names, dates and anything legal, medical or financial carry a prompt to verify, placed where the person acts on them.

## Keep a person in charge of actions

An agent that sends, buys, deletes, books or changes settings acts in the person's name.

- Before an action with consequences, show exactly what will happen (recipient, amount, files, the text to be sent) and ask once, in a dialog that names the action on its button ("Send to 14 people", never "OK").
- Prefer reversible actions, and offer **Undo** for a period after the action, stated in the interface.
- Show a running log of what the agent did, in plain steps, with a way to stop the rest of the run.
- Never widen what the agent may do without asking (new permissions, new accounts, spending), and make every standing permission visible and revocable in one place.

## Respect what people share

- Say what happens to what the person types or uploads: whether it is stored, for how long, and whether it trains a model. Put it next to the input, not only in the policy.
- Offer a way to keep a conversation out of history and out of training, and honour it.
- Never pre-tick consent to share data for training (the linter's `consent-prechecked` catches the marketing kind).

## Look like the product, not like a chatbot template

- The assistant uses the system's roles: its type, colors, radius and motion. A generic chat bubble kit with a purple gradient avatar reads as bolted on.
- Answers are typeset as content (headings, lists, tables, code) with the system's reading measure, not as one grey bubble.
- Empty, loading, error and streaming states are designed, each on the system's surfaces, and measured like any page: `uxskill lint --render` checks contrast, targets and overflow on them, and a complaint about any of them is kept and measured with `uxskill complaints check`.

See also: `copy.md` for error and empty-state wording, `interaction.md` for feedback timing, `motion.md` for streaming and loading motion, `accessibility.md` for live regions that announce new answers.
