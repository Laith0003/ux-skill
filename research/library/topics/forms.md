# forms
Input rows: 144. Output rows: 46.

Confidence note: scored with the sources.md weight table; rule 5 then lifts any lesson that three or more independent books support to high (two books by the same author count once).

## Labels and structure

- **Give every field a persistent visible label tied to the input in code.** Use a label element whose for matches the input id (or wrap the input); without it a screen reader announces only a blank edit field, and a bound label also enlarges the hit area of small checkboxes. This is required by WCAG 2.2 (1.3.1, 3.3.2, 4.1.2). Confidence: high. Sources: B18 p.89, 93; B80 p.49-51; B91 p.240; B88 p.171
- **Never use placeholder text as the only label.** Placeholders vanish once typing starts, look like filled data, are weak for screen readers and confuse distracted users; keep the label above and use the placeholder only for a format example styled unlike a real value. Confidence: high. Sources: B86 p.493, 495; B52 p.164-165; B24 p.86-87; B14 p.97; B23 p.564; B88 p.171; B77 p.201
- **Place labels above fields in a single column.** Top labels survive translation growth and zoom, do not steal input width on small screens, and make completion order unambiguous; fields placed in a second column to the right tend to be skipped, except for tightly related parts such as name or date pieces. Confidence: high. Sources: B52 p.164; B24 p.85-86; B08 p.56; B23 p.563-564; B59 p.13
- **Group radio buttons and checkboxes in a fieldset with a short legend.** The question goes in the legend and each option gets its own associated label to its right; keep legends brief because some screen readers repeat them per option. Confidence: high. Sources: B80 p.16-17; B91 p.242; B59 p.13
- **Draw a clear edge around each input and make its width fit the answer it expects.** A short field signals a short answer (a three-digit security code), display-only values sit without borders, and labels must not be so pale they read as disabled. Confidence: high. Sources: B46 p.218-219, 495-497; B23 p.566; B80 p.118-120; B38 p.51
- **Put format hints and instructions next to the field they govern, before input.** Hints belong beside or under the field, instructions just before the controls they cover, never at the bottom of the form. Confidence: high. Sources: B46 p.234-236; B77 p.57-58; B18 p.100, 202-204; B91 p.240
- **Mark required and optional fields consistently, in text, and explain any symbol.** Either mark every required field or label optional ones with the word optional; an unexplained asterisk is insider knowledge, and required state must also exist in code. Confidence: high. Sources: B86 p.494-495; B23 p.564; B59 p.13; B46 p.236-237; B52 p.175-176; B91 p.240
- **Put inputs inside an actual form element so pressing Enter sends it.** That Enter behavior depends on the form element and, with multiple fields, a submit button; use POST so credentials never appear in a URL. Confidence: medium. Sources: B80 p.52-53; B52 p.153-154

## Ask less

- **Cut every field that is not needed for value right now.** Each extra question lowers completion; trimming marketing fields lifts sign-ups, and when people abandon around the middle, cutting half the form matters more than cutting one field. Confidence: high. Sources: B52 p.152-153, 156; B23 p.569-570; B54 p.128; B86 p.492; B38 p.68; B44 p.45; B24 p.77; B06 p.232-233; B61 p.19
- **Ask each question at the moment it matters and let people defer the rest.** Collect essentials first, move secondary questions to confirmation or later in the relationship, allow guest checkout, and let incomplete records be saved and flagged rather than blocked. Confidence: high. Sources: B86 p.36-37; B46 p.236-237; B58 p.473-474, 591; B54 p.158-159; B26 p.188-189, 328-329, 673; B06 p.232-233
- **Derive and infer instead of asking.** Fill city and region from the postal code, detect the card network from the leading digits, country from location, and reuse anything the person already gave in this process. Confidence: high. Sources: B86 p.492; B54 p.129-130; B11 p.112-113; B02 p.233-235; B58 p.623
- **Do not make people type the same value twice.** Repeat-your-email and repeat-your-password fields usually receive a pasted copy of the same mistake; offer a show-password toggle and detect likely mistakes (misspelled domains) instead. WCAG 2.2 Redundant Entry (3.3.7) requires reusing data already entered in the same process. Confidence: high. Sources: B52 p.157; B24 p.77, 83-85; B20 p.774-775
- **Explain why each personal field is requested and what the person gets.** A one-line benefit next to an unusual field makes it worth giving, and every data request should be paid back with a visible convenience. Confidence: high. Sources: B54 p.22; B86 p.492; B44 p.205-207; B23 p.569-570
- **Do not store data you do not need.** Data never collected cannot be breached; question every card, phone and address field and whether an account is needed at all. Confidence: low. Sources: B44 p.66
- **Reveal optional fields on demand.** Show what everyone needs and expand extra inputs (phone, website) when asked, hiding complexity without removing capability. Confidence: low. Sources: B54 p.127

## Input formats and controls

- **Accept any intelligible format and normalize it in code.** Allow spaces and hyphens in card and phone numbers, varied date orders, pasted extras, and any case for codes other than passwords; and never hold back the expected format until someone gets it wrong. Confidence: high. Sources: B77 p.179; B79 p.81-82; B86 p.480-481; B14 p.91-93; B46 p.242-243; B23 p.566; B49 p.106
- **Prefer bounded choices when the answer set is small, typed entry when it is large or known.** Buttons and lists beat typing for a few options; long lists such as countries need type-ahead with popular items first, and dates need a picker plus typed entry. Confidence: high. Sources: B52 p.153-154, 174-175; B02 p.233-235; B33 p.62, 81; B04 p.176; B11 p.112-113; B39 p.53
- **Shorten option lists and float the likely answers.** Ask only the precision needed (a handful of round values beats a list of 30), and show recent and common items first, then the full sorted list. Confidence: high. Sources: B52 p.174-175; B14 p.91-93; B02 p.233-235
- **Disable invalid choices in pickers and never change input silently.** Gray out unavailable dates, show related dates in context, and tell the person whenever the system adjusts a value. Confidence: high. Sources: B04 p.173-175; B11 p.112-113; B14 p.82, 90
- **Use international-ready name, address and phone fields.** Use given and family name, two address lines, region, an alphanumeric postal code of no fixed length and a country; accept phone numbers of 6 to 15 digits with separators and do not force an area-code split. Confidence: medium. Sources: B08 p.66-68; B02 p.232-233
- **Set the input type and keyboard to fit the data.** Use email, tel, numeric and url types so mobile shows the right keyboard and autofill works; turn off autocorrect and auto-capitalization for usernames and codes. Confidence: medium. Sources: B07 p.45-46; B52 p.168
- **Display long codes in groups of three or four characters.** Strings of five or more characters without natural breaks are easier to read and check when chunked. Confidence: medium. Sources: B46 p.256; B86 p.482-483
- **Let people type alphanumerics, names and spellings rather than speak them.** Speech is poor for this data; offer a text field and validate against checksums and known formats. Use touch for entry and correction and voice for short commands. Confidence: medium. Sources: B41 p.148-149; B73 p.102-103
- **Scaffold generative prompts with structure.** Templates with labeled fields, mode chips and an advanced toggle cut vagueness without making the basic route any harder. Confidence: medium. Sources: B82 p.96-98, 101-102
- **Replace empty open-text boxes with recognizable choices when collecting preferences.** Clickable options collected many times more answers than a blank list-your-favorites field. Confidence: low. Sources: B54 p.23-25, 159
- **Express expert settings in plain structures.** A fill-in-the-blank sentence or a sensitivity slider that starts at a sensible automatic value reads better than raw percentile dropdowns; keep manual override available. Confidence: low. Sources: B12 p.300-303, 309-310

## Defaults

- **Default only to values most people keep and that are safe if overlooked.** Default to today, preselect the only option, and place the cursor in the next field; base defaults on observed choices, and skip a default where a wrong value is costly. Confidence: high. Sources: B20 p.771-773, 792; B52 p.173; B07 p.68-69; B44 p.46; B86 p.520; B04 p.171-172
- **Autofocus the first field only when input is clearly the first step.** On sign-in or search-led screens, place focus in the field so the keyboard is already up. Confidence: high. Sources: B24 p.75-76; B78 p.55; B20 p.771-773
- **Never pre-check consent, marketing opt-ins or terms acceptance, and never default sensitive fields.** Most users leave defaults alone, so a pre-ticked box manufactures consent; leave gender, citizenship, passwords and ad consent empty. Confidence: medium. Sources: B86 p.520; B78 p.63-64

## Validation and errors in forms

- **Check a field when the person leaves it, or after a short pause, never while a correct value is only half typed.** Waiting roughly half a second after typing stops, or until blur, works; flashing an error mid-entry punishes people who are not done. Confidence: high. Sources: B86 p.493-494, 526; B26 p.646-648; B52 p.175-176; B24 p.87-88
- **Never clear entered data on focus, on a failed validation, or after an error, including card details.** Hold on to half-finished input and drafts so work can be picked up again; offer an explicit start-over instead. Confidence: high. Sources: B52 p.157-158; B02 p.232-233; B20 p.774-775, 792-793
- **Show password rules before typing, allow paste and password managers, and offer a show-password toggle.** WCAG 2.2 Accessible Authentication (3.3.8) forbids cognitive tests at login unless an alternative or paste and autofill are allowed; avoid partial-password character challenges. Confidence: high. Sources: B52 p.171-172; B24 p.83-88; B02 p.142-143
- **Let people check, fix or undo legal and financial submissions.** Add a review step and read back multi-detail requests before committing them (WCAG 3.3.4). Confidence: high. Sources: B91 p.266-267; B60 p.117-120; B18 p.100
- **Avoid visual CAPTCHAs.** They block blind and low-vision users and paid services break them for fractions of a cent; use behavioral or server-side checks with an accessible alternative. Confidence: medium. Sources: B91 p.75-78; B18 p.87
- **Warn before timeouts, show time remaining, and keep the data.** Short purchase windows can expire for screen reader users; let people extend and never lose what they entered. Confidence: medium. Sources: B91 p.72, 77, 99, 119, 240; B46 p.236-237

## Flow, steps and buttons

- **Label the primary button with its outcome, not Submit.** Name what happens (Create account, Pay 40 dollars, Send request), make secondary actions visually weaker, and drop Cancel or Reset buttons that wipe web forms. Confidence: high. Sources: B23 p.564; B07 p.45-46, 138; B59 p.13; B88 p.171
- **Show the whole task before it starts.** List the steps and what documents or details people need, then show progress (a compact step X of Y works on small screens). Confidence: high. Sources: B18 p.202-204; B23 p.569-570; B24 p.93-95; B25 p.73-74
- **Chunk long or high-stakes forms into labeled sections with a way back.** Progressive steps simplify each decision and let people revise earlier answers; a slightly longer but chunked form can feel shorter and build more confidence than a minimal one. Confidence: high. Sources: B21 p.181; B34 p.183-185; B78 p.66-67; B77 p.57-58
- **Keep sign-in minimal and explain why it is needed.** Identifier, password, recovery and a register link; state the reason for a login prompt and return people to where they were afterwards. Confidence: medium. Sources: B24 p.75-76; B07 p.82, 84, 137-139
- **Keep the relevant details visible throughout the flow.** Short-term recall fades within seconds; prices, choices and shipping details should stay on screen rather than rely on memory. Confidence: medium. Sources: B44 p.121-122
- **Write closed answer sets that are specific, exhaustive and exclusive.** Offer none, other and not applicable choices, write out units and exact time windows, and avoid double-barreled or negative questions. Confidence: medium. Sources: B03 p.350-354, 359; B51 p.222
- **Keep a single scrolling page for moderate forms on mobile, and follow platform placement for submit and cancel.** Splitting a short form into artificial pages adds taps without benefit. Confidence: low. Sources: B24 p.114-115
- **Make terms and privacy policy reachable at sign-up and again in the account.** Confidence: low. Sources: B38 p.69
- **Shape user-generated content with examples, limits and type-ahead.** Sample entries and prefilled values steer the voice and size of answers, and type-ahead removes spelling variants. Confidence: low. Sources: B39 p.50, 53

## Fairness in forms

- **Keep form behavior out of eligibility scoring and avoid opaque scored questionnaires.** Spelling, capitalization or reading time track education and language, not trustworthiness; forced-choice items with hidden scoring leave people unable to answer honestly. Confidence: medium. Sources: B56 p.93-94, 132
- **Accept plain structured uploads where machines will parse them.** Automated parsers drop content in images, decorative fonts or symbols; tell people when a document will be machine read. Confidence: low. Sources: B56 p.97
