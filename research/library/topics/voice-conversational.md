# voice-conversational
Input rows: 152. Output rows: 40.

Confidence note: voice and chat are technology-dependent (+1 for 2018 and later). Rule 5 of sources.md lifts any lesson that three or more independent books support to high.

## When to use voice and chat

- **Offer at most three spoken options, four for short familiar items.** Listeners with partial attention lose track after the fourth or fifth item; present a handful and supply more if asked, keep phone menus to about three levels of four choices, and expect older callers to struggle more (one study: 32 versus 82 percent task completion). Confidence: high. Sources: B02 p.148, 259; B63 p.114-115; B73 p.40-41; B41 p.256; B46 p.714-715
- **Add voice or chat only where it beats a screen.** Voice suits hands-busy, partial-attention, screenless and emotional moments and is poor for browsing, public spaces, open offices and private topics; open chat suits problem spaces too varied for fixed paths, while visual interfaces stay primary for speed. Confidence: high. Sources: B41 p.26-27; B73 p.22-23; B21 p.42, 145-146; B16 p.144-145
- **Use voice for input and a screen for dense output.** Speaking is about three times faster than typing on a phone (about 161 versus 53 words per minute), but listening runs near 60 words per minute against about 300 for reading, so move multi-item answers to a card. Confidence: high. Sources: B82 p.101; B79 p.264; B02 p.258; B73 p.38
- **Always provide a non-voice fallback and hand spatial or sensitive steps to a screen.** Noise, privacy and recognition errors break voice; let people switch to touch or typing, and finish seat picks or card entry on the device. Confidence: medium. Sources: B73 p.75, 92-93, 101; B41 p.26-27
- **In cars, cut features and visual demand.** Focus on a few core tasks with two or three spoken options, avoid on-screen command lists, and remember that glances away from the road should stay under about two seconds. Confidence: medium. Sources: B41 p.256-263

## Cooperative dialog

- **Follow the cooperative maxims.** Give enough and no more, say only what is true, stay relevant, and be brief, clear and orderly; most broken exchanges violate one of these, including an open greeting when only one task is supported. Confidence: high. Sources: B33 p.33-36; B66 p.73-74; B41 p.15-16
- **State scope and limits in the first turn.** Say what the assistant does and how to start, add a few example prompts (not enough to paralyze), and admit a constrained grammar up front; acting as if anything can be said leads to failure after failure and a too-human voice sets expectations it cannot meet. Confidence: high. Sources: B16 p.164-167, 174; B63 p.118-120; B41 p.15-16; B33 p.37-38, 81
- **Never answer with a bare no.** Ask for detail when a request is vague, offer an alternative when the answer is no, and refuse briefly with a gentle reason in the product voice so the user knows they can continue. Confidence: high. Sources: B73 p.35-36; B51 p.199-200; B82 p.162-163
- **Keep context across turns so follow-ups need no repetition.** Resolve pronouns and place words against earlier turns, reuse the prior intent and entities for incremental requests, and anticipate likely follow-ups. Confidence: high. Sources: B60 p.120-121; B41 p.40-41, 71-72; B66 p.72; B73 p.29-31
- **Use context before asking, then ask short and accept loose answers.** Location, calendar and recent activity resolve most ambiguity; when it remains, ask one short question and accept replies such as the state name or the first one, instead of saying it did not understand. Confidence: medium. Sources: B41 p.80-81, 157-158; B73 p.26
- **Serve experts in one turn and novices step by step.** Fulfil at once when every detail is given, otherwise elicit details turn by turn, and infer intent rather than walking a scripted tree. Confidence: medium. Sources: B60 p.53-54; B73 p.24-26
- **Have chatbots solve the problem or route to a person.** A bot earns its place by finding the need and reaching the right human, never by fooling people; always provide a way back to the top menu or to a human agent. Confidence: medium. Sources: B21 p.145, 147; B02 p.259-260
- **Handle negation explicitly.** A request such as mushrooms but no pepperoni, or a review saying not very good, breaks if parsed by keyword spotting. Confidence: low. Sources: B41 p.162

## Turn-taking and prompts

- **Close any prompt that passes the turn with a single cue at the very end.** Listeners start replying the moment a question lands, so options and context come first and the question last, with no pause inside the prompt when barge-in is on. Confidence: high. Sources: B63 p.96, 102; B41 p.60, 131-132; B73 p.43
- **Respect conversational timing.** Gaps between human turns run about 200 ms and rarely exceed 400 ms, a pause near 0.6 s signals disagreement, and a reply that needs thought sounds natural with a short marker and pause; text chat agents read as natural when replies land in roughly 2 to 3 seconds. Confidence: high. Sources: B73 p.43-44, 62-63; B63 p.41; B41 p.249; B60 p.48; B82 p.125
- **Tune listening timeouts per state.** Start with about 1.5 s end-of-speech (trimmed for yes or no replies, extended for open answers and digit strings), about 10 s for no speech and for the listening window, and 7 to 10 s before cutting off long speech. Confidence: medium. Sources: B41 p.58, 119, 135-136, 142, 233-234; B63 p.44
- **Speak in short chunks and hand the turn back.** Keep a spoken turn under about 20 seconds, deliver long content two or three sentences at a time with a pause for an acknowledgment, allow repair per chunk and offer to stop. Confidence: medium. Sources: B63 p.117; B60 p.103-106, 125-126
- **Pace speech with prosody and pauses.** Pause between list items and around key words, about 200 ms between digit groups, use speech markup for synthesis, and read every script aloud. Confidence: medium. Sources: B63 p.116-118; B41 p.171
- **Use directed prompts and specific reprompts.** Constraining the expected answer improves recognition; on failure, reprompt with a targeted question and support barge-in. Confidence: medium. Sources: B02 p.148, 259-260
- **Choose the cue type for the answer you need.** Open, menu, yes or no, location, quantity and instruction cues shape replies differently. Confidence: low. Sources: B63 p.98-102
- **Vary the wording of prompts heard often.** Rotate equivalent phrasings, starting with the most frequent prompts. Confidence: low. Sources: B73 p.42-43
- **Phrase help like a person, not a phone tree.** Avoid say X for more options; offer to tell more. Confidence: low. Sources: B73 p.36-37

## Repair, help and navigation

- **Keep the core navigation intents live at every point.** Capability questions, repeat, what do you mean, help, go back, start over, never mind, talk to a person and goodbye must always work; help and where-am-I should explain the current step and next moves. Confidence: high. Sources: B60 p.100-102; B63 p.140; B41 p.75-77, 88; B02 p.259-260
- **Support repair from every position and show what was understood.** Let users fix wording mid-turn, query or correct the last response, restate understanding before complex tasks, recap goals to fight drift, and read back captured answers before saving them. Confidence: high. Sources: B60 p.56-58, 131-132, 160; B16 p.174-176; B48 p.170-171
- **Scaffold discovery in voice, which has no visible signifiers.** Reveal capability progressively, with hints after repeated success and help after a partial failure; most smart-speaker owners never move past songs and timers. Confidence: medium. Sources: B66 p.31, 70; B33 p.60
- **Switch modes only after the user agrees.** A quiz or game mode changes how input is read, so offer it and wait. Confidence: medium. Sources: B60 p.129
- **Show clearly when the system is listening.** Use a distinct listening state (ring, wave, border) and different cues for not heard and not understood; a static mic icon invites taps. Confidence: low. Sources: B41 p.56-57, 113-114, 118-119
- **Make memory limits visible.** Suggest a new conversation for a new topic, warn as the context fills, and show a notice when something is remembered. Confidence: low. Sources: B16 p.179
- **Keep voice commands short, distinct and undoable.** Steer clear of commands that sound alike, give each phrase a single meaning and leave system commands untouched. Confidence: low. Sources: B48 p.170-171

## Closings

- **Do not take the user's closing slot with a feedback question.** A was-this-helpful after every answer blocks thanks or repair; wait about 2 to 3 s in voice or 20 to 30 s in text before anything else, ask only if the agent helped, and treat goodbye as a chance to confirm success. Confidence: medium. Sources: B60 p.33, 162-163, 186-192
- **End turns with a useful next move when the user needs one.** Offer to go deeper, refine, pivot, act or wrap up so a conversation neither dead-ends nor rambles. Confidence: low. Sources: B16 p.172-173

## Intents and language coverage

- **Cover many phrasings and real conditions.** Gather at least 30 example phrasings for each intent, drawn from real logs, and keep adding after launch; command systems that demanded exact wording failed, and recognition must cope with children, road noise and crowded rooms. Confidence: high. Sources: B73 p.24; B66 p.17-18, 121; B63 p.134-137
- **Split topics into intents where answers differ, and sort them by hand.** Hours becomes open now, closing soon and opening when; label utterances by social action (request, inquiry, closer, repair) and do not let keyword clustering decide. Confidence: high. Sources: B63 p.134-139; B60 p.48-52, 70-72; B73 p.24
- **Build expandable sequences, not only slot filling.** Wrap each request with room for checks before asking, requests to hear the options, repeats, rewordings and sign-offs. Confidence: medium. Sources: B60 p.86-87

## Persona

- **Define the persona deliberately from its role and goals.** People infer a personality anyway; pick the real-world role it plays, three or four interaction goals and about three traits, plan key behaviors (greeting, failing, being interrupted, inappropriate questions), and keep the same character across channels. Confidence: high. Sources: B63 p.65-68, 75, 78-79, 87-88; B33 p.94-96; B73 p.16, 46, 49
- **Scale personification to the task.** A bot that only completes transactions needs neither a name nor an I; recommendations read better as you may like than as I think, while long-term assistants can carry a name and small talk. Confidence: high. Sources: B63 p.70-71; B51 p.198; B33 p.81
- **Match emotional tone to the user's moment.** An upbeat reply to a bad day reads as uncaring, and a mismatched cheerful voice raised driving accidents in one study; keep scripted emotion balanced. Confidence: medium. Sources: B73 p.66-67; B41 p.100
- **Reflect the power relationship in tone.** Bots serving boss-like users must be deferential; sass that works between peers offends in hierarchies. Confidence: low. Sources: B63 p.73-74

## Multimodal

- **Complement speech on screen instead of duplicating it.** People read and stop listening when both compete; show icons, numbers and extra context, and keep audio and visuals within about 400 ms of each other so they read as one response. Confidence: medium. Sources: B63 p.212-213; B73 p.38
- **Design the conversation first, then add visual aids.** Make every task work in words alone so the agent ports across voice, text and screens, then add buttons and cards. Confidence: medium. Sources: B60 p.27-36
