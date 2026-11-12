# ai-ethics
Input rows: 154. Output rows: 46.

Confidence note: data and AI practice is treated as technology-dependent (+1 for 2018 and later). Rule 5 of sources.md lifts any lesson that three or more independent books support to high.

## Honesty about the machine

- **Never let a system pass as a person, and label AI output up front.** Say when a bot is answering, when a voice agent calls someone, when content is generated and when a human operator is secretly behind an automated service; several jurisdictions now require this disclosure. Confidence: high. Sources: B16 p.193-194, 396-397; B73 p.14, 54, 57-58; B82 p.147-148; B65 p.74-75; B12 p.442
- **Do not ship AI text detectors or rely on them.** They miss most generated text, falsely flag human writing (one withdrawn classifier caught about 26 percent and wrongly flagged 9 percent), are easy to evade and are biased against nonnative writers. Confidence: high. Sources: B43 p.35, 235-236; B82 p.159; B75 p.428-430
- **Do not simulate feelings or cultivate dependency.** Keep personality minimal: no claimed emotions, no forced pleasantries, no chirpiness on serious topics; heavy companion use is linked to loneliness, and simulated emotion reads as deception. Confidence: medium. Sources: B16 p.155-157; B21 p.41, 148
- **Say which kind of AI is in play.** Generative, predictive and moderation systems fail in different ways, so copy and decisions should name the type rather than the umbrella term. Confidence: low. Sources: B43 p.11-12
- **Never cast the system as a neutral judge of right and wrong.** Treating it as the arbiter of ethical questions hides the choices in its data and model. Confidence: low. Sources: B45 p.71, 73

## Explanation and contestability

- **Pair each automated decision with a stated reason and a way to dispute it.** People scored by a system must learn why and be able to contest before, during and after deployment, through more than one channel; friction that lets people refuse is a right, not a defect. Confidence: high. Sources: B56 p.15-16; B45 p.34-36; B02 p.428-429; B12 p.435-439
- **Scale explanation to the stakes, in plain language.** An ad needs little, a loan or visa decision needs a lay explanation; heatmaps alone help little, and attributions describe one model and dataset, not a general truth. Confidence: medium. Sources: B02 p.428-429; B61 p.413-414
- **Prefer simple, explainable rules where people are affected.** People can read and dispute a rule they can see; claims to predict individual outcomes such as job performance or dropout barely beat chance and need independent validation first. Confidence: low. Sources: B43 p.12, 19, 71, 77, 238-239
- **Weigh a lottery among qualified applicants when supply is limited.** Drawing at random once a minimum bar is met admits that outcomes cannot be forecast and stops early winners from compounding their lead. Confidence: low. Sources: B43 p.239-240

## Bias and fairness testing

- **Test outcomes per group, because removing sensitive fields does not remove bias.** Proxies such as postcode or gendered wording carry bias through; keep protected attributes for auditing, test intersections, report metrics per slice (one loan model ran 94 versus 85 percent accuracy and 72 versus 55 percent approval across sources) and choose a fairness criterion explicitly. Confidence: high. Sources: B61 p.416-417, 427; B65 p.129-130; B21 p.170, 175-176; B51 p.306-307
- **Audit generated output across demographics and for who is missing.** Image generators lightened skin for a professional look and returned 25 male biologists to 1 female against a roughly even workforce; set diverse defaults for role queries and adjust prompts or data. Confidence: high. Sources: B43 p.96, 115; B12 p.424-432; B51 p.306-307
- **Check that a strong score did not come from the wrong cue.** Models have keyed on annotations or props instead of the subject; test on novel cases and use explanations and surprising outputs to catch it. Confidence: high. Sources: B65 p.10-13; B61 p.109-110, 391, 409; B45 p.19, 21
- **Fix the data, not the label.** Deleting an offensive label leaves the broken model in place; where a model cannot justify an output (gender from a photo), suppress it with a disallow list instead. Confidence: medium. Sources: B43 p.108; B61 p.430-431
- **Remember that interface ordering can create bias.** Sorting candidates by name rather than urgency skews outcomes through the layout itself, with no help from the data. Confidence: medium. Sources: B21 p.174
- **Interrogate every dataset before use.** Establish its origin and collection method, whether cells were imputed or bot-filled, and whether one institution or era skews it; keep imputation flags attached, and do not assume public data is free of ethical risk. Confidence: medium. Sources: B66 p.78-81, 94, 101, 108-111; B65 p.124-125
- **Test that swapping an identity term leaves the output unchanged.** Replacing one name or group with another should not change a sentiment or toxicity score. Confidence: low. Sources: B61 p.424, 431
- **Review category schemes with the people they label.** Every taxonomy of people is a value choice; drop labels that judge character (a major image set removed more than half its person categories after a decade). Confidence: low. Sources: B65 p.144-150

## Objectives and feedback loops

- **Write down what the model optimizes and who benefits.** A model encodes its builders' definition of success; name the metric and the stakeholders who gain or pay before tuning anything. Confidence: medium. Sources: B56 p.23-24; B65 p.18
- **Watch for scores that justify their own inputs.** High risk scores bring more scrutiny that raises the score; drop inputs that create unfair loops. Confidence: medium. Sources: B65 p.206-207; B56 p.78, 83, 125
- **Check any ranking or eligibility feature for opacity, scale and damage.** When the people scored cannot see how it works, it applies to many and it can hurt them, it needs redesign or oversight before launch. Confidence: low. Sources: B56 p.29-31
- **State assumptions and never oversell accuracy.** Models trained on history reproduce it; be explicit about blind spots and add explicit values even when it costs revenue. Confidence: low. Sources: B56 p.168-170
- **Design scored work around human limits.** Centrally set productivity rates drove injuries; give workers a voice in the targets a tool enforces. Confidence: low. Sources: B65 p.62-65, 83-85, 91-94

## Consent, data and privacy

- **Get a clear yes before keeping any personal data, in the channel the person is using.** Say what is stored and why, let people view and delete it, and let them ask why a detail is needed or refuse it without derailing the flow. Confidence: high. Sources: B63 p.197, 206-208; B60 p.118-119; B12 p.435-439; B65 p.98-103, 114, 118-119
- **Make consent readable, modular and revisable.** A single agree checkbox hides a web of third-party terms and long policies cause fatigue; explain collection, use, sharing and storage in plain words and let consent change over time. Confidence: high. Sources: B45 p.56-62; B51 p.167, 311; B63 p.206-208
- **Tell people when their behavior or inputs train the system.** Do not quietly extract training labor through tagging tasks, and assume users will paste sensitive data into a generative tool unless told how inputs are used. Confidence: high. Sources: B16 p.193-194; B65 p.78, 115; B75 p.69-70, 149-150
- **Make permissions granular in human terms and as easy to revoke as to grant.** Offer scopes people understand (this conversation, this folder, all files, location on or off) and a reachable panel of active permissions; do not expose model tuning such as precision settings. Confidence: medium. Sources: B82 p.74; B51 p.168-169
- **Answer privacy questions inside the feature and show the benefit.** Explain who can see transcripts and data where the feature lives, tie collection to a visible useful result, and provide an incognito setting whose activity never shapes recommendations. Confidence: medium. Sources: B12 p.168-169; B66 p.106-107
- **Treat anonymized and aggregate data as sensitive.** Hashed identifiers in a large trip dataset were re-identified; show summaries or buckets, mask identifiers on screen and assess harm to groups, not only individuals. Confidence: medium. Sources: B65 p.119-120; B51 p.309-310
- **Detect the wake word locally and retain only audio meant for the assistant.** Discard anything heard before activation, strip identifiers from logs; about one in five people surveyed did not know their device was always listening. Confidence: medium. Sources: B41 p.149-150, 175; B63 p.203
- **Design for privacy inside the household.** A device several people share can expose one person's messages or orders to the rest; separate profiles or speaker recognition prevent it. Confidence: low. Sources: B66 p.105-106
- **Get verifiable parental consent before collecting data from children under 13.** This is a legal requirement in the US. Confidence: low. Sources: B08 p.289
- **Weigh consent in shared physical space for AR.** Face recognition overlays and geotagged content raise questions of consent, clutter and ownership of public space. Confidence: low. Sources: B48 p.243-244, 262, 314-315

## Conversation safety

- **Answer abuse firmly and never with a joke.** Up to 30 percent of chatbot input can be off-topic, abusive or sexual; object once at the first insult, stop engaging at the second, resume if the user apologizes, and log any agent line a user flags as offensive. Confidence: high. Sources: B63 p.122-125; B60 p.196-200; B73 p.68-72
- **Do not replace human support with untested bots in care settings.** In one study more than half of people could not finish medical tasks with assistants and 29 percent of those who did chose a potentially harmful action; keep a human fallback and test first. Confidence: medium. Sources: B43 p.247; B63 p.285-286
- **Specify how the system declines.** List what it refuses to do, refuse gently with a safe alternative, and assume guardrails can be talked around. Confidence: low. Sources: B12 p.196-199, 203
- **Counter sycophancy and mood mirroring.** Models tend to agree with the premise; flag leading questions or offer an alternative view. Confidence: low. Sources: B82 p.12, 89-90
- **Judge proactive suggestions on a helpful-to-creepy scale.** Set guardrails before acting on a learned pattern and record when users decline. Confidence: low. Sources: B66 p.125-127
- **Keep stable, non-partisan positions.** Assistants should not take political sides and should move on from abuse without judgment. Confidence: low. Sources: B73 p.68-72

## Governance

- **Turn principles into enforced review gates.** Hundreds of voluntary ethics frameworks change little alone; map who is responsible at each pipeline step and score trustworthiness on openly reported practices (one proposed scale has 12 items worth 0 to 24 points). Confidence: high. Sources: B65 p.232-233; B45 p.77-78; B21 p.269
- **Match oversight to potential harm.** Automate review for high-volume low-stakes work, put people on rare risky decisions, and grant new users graduated access; regulation already sorts AI into risk levels. Confidence: medium. Sources: B16 p.421-423; B02 p.425
- **Publish what a model is for and not for.** Documentation listing the uses a model suits and the uses it does not, plus documented curation and prompt choices, keeps mitigations valid. Confidence: medium. Sources: B61 p.432-433; B45 p.19
- **Count the compute cost.** Large models carry an energy and water footprint; prefer smaller models and skip compute spent on marginal gains. Confidence: medium. Sources: B65 p.50-53; B12 p.443
- **Document compliance trade-offs.** Meeting privacy rules can reduce dataset representativeness; record the justification. Confidence: low. Sources: B45 p.73-75
- **Design across all layers, not only the screen.** Algorithms, terms, business model and governance interact, so a choice in one can undo work in another. Confidence: low. Sources: B45 p.9-10

## Generative media

- **Keep living artists and identifiable people out of prompts unless they agreed.** Naming them raises copyright and consent problems; likeness use needs explicit permission and payment. Confidence: low. Sources: B75 p.312, 329-330, 444-445
- **Discard outputs carrying signatures or watermarks and support provenance.** A visible mark means source material leaked through; attach content credentials and honor do-not-train signals. Confidence: low. Sources: B75 p.313-314, 428-430, 543-544
