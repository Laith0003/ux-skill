# Don Norman's Design Principles Applied

Don Norman's design principles applied to web and product UX: affordances, signifiers, mapping, feedback, conceptual models, gulfs of execution and evaluation, the seven stages of action, and error design.

This is the canonical reference. Every principle is treated with its definition, the cognitive theory behind it, the violation pattern in modern interface work, and the prescriptive fix. The goal is not history; the goal is shippable design.

The principles fall into three layers:

- **Layer 1 — Object properties**: affordances, signifiers, constraints, mapping
- **Layer 2 — System properties**: conceptual model, feedback, discoverability
- **Layer 3 — Process properties**: stages of action, gulfs, error design, knowledge placement

Master all three layers and the surface that comes out is intelligible, forgiving, and self-teaching. Ignore any one of them and the user feels stupid — which is the worst usability failure, because users blame themselves rather than the design.

---

## Affordances

**Definition.** An affordance is what an object permits the user to do. It is the relationship between the object's properties and the user's capabilities. A button has the affordance of being pressed. A handle has the affordance of being pulled. A slot has the affordance of receiving.

Affordances are not properties of objects alone; they emerge from the interaction between object and actor. A doorknob affords gripping to a human; it affords nothing to a fish.

**In digital UX.** Pixels on a screen have no inherent physical affordance — the affordance is purely visual and learned. A button "affords" pressing because we recognize the visual code: filled shape, contrasting color, hover response. Strip away those visual codes and the affordance disappears.

**Violation pattern.** Flat design carried too far. Text-styled "buttons" with no fill, no border, no underline — readers cannot tell whether the text is interactive. Floating action buttons rendered without shadow on light backgrounds — they read as decorative dots. Drag handles without visible grip marks.

**Fix example.** Buttons get a fill, a border, or both — never raw text alone unless the convention is unmistakable (top-nav links). Interactive icons get hover affordances even when static: a slight darkening, a tooltip on hover, a cursor change. Drag handles get the universal grip icon (six dots or three lines). Anything pressable looks pressable.

**How to spot a violation.** Show the screen to someone unfamiliar. Ask them to point at everything they could interact with. If they miss anything you intended to be interactive, the affordance is missing.

---

## Signifiers

**Definition.** Signifiers are the visible signals that communicate where action is possible and what the action will accomplish. Affordances are the possibility of action; signifiers are the perception of that possibility. Signifiers are what designers actually control.

The distinction matters. An object can afford an action without signifying it — at which point the affordance is invisible and useless. The designer's job is to add signifiers so the affordance becomes perceivable.

**In digital UX.** Every visual cue that says "this is interactive" is a signifier: button styling, hover states, cursor changes, underlines on links, drag handles, scrollbars, expand/collapse chevrons.

**Violation pattern.** Aesthetic minimalism that strips signifiers. Cards that turn out to be clickable but have no hover state, no cursor change, no visual indication of interactivity. Hidden gestures (swipe to delete, long-press to edit) with no signifier — users discover them by accident or never.

**Fix example.** Every interactive element has at least three signifiers: a visual treatment (fill, border, underline, icon), a hover state (color shift, slight motion, cursor change), and a touch-target size sufficient for confident interaction. Hidden gestures are paired with an alternative visible affordance — swipe to delete is fine, but only if a long-press also reveals an explicit delete button.

**How to spot a violation.** Hover over every element on a screen with a mouse. If anything responds without a corresponding visual change before the hover, the signifier is missing. On touch devices, the equivalent: tap and see if you can predict whether the element will respond.

---

## Mapping

**Definition.** Mapping is the relationship between controls and the effects they produce in the world. Natural mapping aligns the control to the effect spatially, temporally, or by analogy. Bad mapping creates a translation step in the user's head.

The classic example: a stove with four burners and four knobs. If the knobs are arranged in a 2x2 grid matching the burner layout, the mapping is natural — knob top-left controls burner top-left. If the knobs are in a row, the user has to learn an arbitrary mapping and will burn dinner.

**In digital UX.** Volume slider goes up for louder. Brightness slider goes right for brighter. Save button on the right (next to confirm-style actions in left-to-right languages). Forward/back arrows match the reading direction. Drag handle to the left of the item it grips, on the side closest to where the user's hand will be.

**Violation pattern.** Controls divorced from their effects. A row of identical icons in a toolbar where the user has to hover each one to learn what it does. Navigation that flips on every page because the layout system doesn't enforce consistency. A volume slider that goes left-to-right but increases the more you push left.

**Fix example.** Controls live next to (or directly on) the thing they affect. Volume up is always up — never reversed for aesthetic reasons. Edit buttons on each row of a table, not in a corner menu the user must visit. Drag-to-reorder uses a clear handle, not arbitrary clickability. Save and Cancel always in the same positions, every screen, every modal.

**How to spot a violation.** Watch a new user try a task. Every time they hover over the wrong control first, the mapping has failed. The right control should be the one they reach for instinctively.

---

## Feedback

**Definition.** Feedback is the immediate sensory confirmation that an action has been received and what its effect was. Without feedback, users repeat actions, doubt themselves, or assume the system is broken.

Feedback must be: **immediate** (within 100ms for "instant" perception, under 400ms for "responsive"), **informative** (what happened, not just "something happened"), and **appropriate to scale** (loud for important events, quiet for routine actions).

**In digital UX.** Button presses have a hover state, an active state, and a confirmation (the form submitted, the modal closed, the item added). Loading states fill the gap between action and result. Error states explain what went wrong. Success states confirm what went right.

**Violation pattern.** Silent failures — the button was clicked, nothing changes, the user doesn't know if it worked. Generic loading spinners that never end. Success toasts that vanish before the user notices them. Form submissions that reload the page with no indication of whether the submission succeeded.

**Fix example.** Every action gets immediate visual feedback: button depresses on click, form fields show real-time validation, search results appear as the user types. Long operations show progress, not just a spinner — "Uploading 3 of 7" beats an indefinite wheel. Success states linger for at least 3 seconds, with action context ("Saved" beats "Done"). Errors persist until acknowledged or resolved.

**How to spot a violation.** Click every button. Submit every form. Is there a clear, instant signal that the system received the action and is doing something? If you have to wait wondering, the feedback failed.

---

## Conceptual Models

**Definition.** A conceptual model is the user's understanding of how a system works — what its parts are, how they fit together, what each part does, and what will happen if they take a particular action. The user's conceptual model is built from past experience, the visible structure of the interface, the system's behavior over time, and any documentation they encounter.

When the user's conceptual model matches the designer's intended model, the system feels intuitive. When the models diverge, the system feels confusing — and users will blame themselves, not the design.

**In digital UX.** The user's mental model of "file" is a thing in a folder. The system's actual model of "file" may be a row in a database with no folder structure at all. Bridging that gap is the conceptual model work — the interface presents files and folders even if the storage is flat.

**Violation pattern.** Exposing the implementation model to the user. Calling things by their internal engineering names. Organizing the IA around the database schema or the team org chart. Showing the user system states (loading, syncing, conflict) without translating them into user states (your changes will appear in a moment, your changes are saved, two people edited this).

**Fix example.** Build the conceptual model from user research, not engineering. The user says "projects" and "tasks"; the database has "workspaces" and "items" — the UI surfaces projects and tasks. The user thinks of points as a balance; the ledger is event-sourced — the UI shows balance, the ledger stays internal. Words, metaphors, and structure all match the user's view.

**How to spot a violation.** Read every label, error, and status indicator. Are they in the user's vocabulary, or in the team's? If a user has to ask "what's a workspace?", the model has leaked.

---

## Constraints

**Definition.** Constraints are the things a design forbids — either by making them impossible, by making them visibly wrong, or by communicating that they're wrong through cultural convention. Good constraints guide the user away from errors before they happen.

There are four kinds:

1. **Physical** — actually impossible. A button that's disabled cannot be clicked.
2. **Logical** — possible but doesn't make sense given context. Selecting a destination before a date doesn't compute, so the date picker is shown first.
3. **Semantic** — based on meaning. The "submit" button doesn't appear until required fields are filled.
4. **Cultural** — based on social or learned conventions. The X icon means close because everyone has learned it does.

**In digital UX.** Form validation that prevents invalid states. Date pickers that disable past dates when the user is booking future travel. Buttons greyed out until prerequisites are met. Sort orders that maintain consistent direction across sessions.

**Violation pattern.** Allowing invalid actions and then explaining the error after the fact. A "Submit" button always clickable, even with empty required fields. Date pickers that allow selecting February 30th and then reject the submission. Settings that contradict each other with no warning.

**Fix example.** Disable the submit button until required fields are filled (visibly, with a hint about what's missing). Date pickers grey out impossible dates. Conflicting settings show a real-time warning, not a post-submit error. Use physical constraints (disabled controls) where possible; fall back to semantic constraints (validation) when not.

**How to spot a violation.** Try to do the wrong thing on every screen. Submit a blank form. Pick an impossible date. Set conflicting options. If the system lets you proceed and only then complains, it's relying on error correction instead of error prevention.

---

## The Seven Stages of Action

**Definition.** Every interaction with a system passes through seven cognitive stages:

1. **Goal** — what does the user want to accomplish at the highest level?
2. **Plan** — what's the sequence of actions to get there?
3. **Specify** — what's the next specific action?
4. **Perform** — execute the action.
5. **Perceive** — what changed?
6. **Interpret** — what does the change mean?
7. **Compare** — does this match the goal?

The cycle repeats until the goal is met or abandoned. Each stage is a place where the design can fail.

**In digital UX.** A user wants to send a message (goal). They plan to find the contact, type the message, and send (plan). The next action is to open the contact list (specify). They tap the contact icon (perform). The contact list opens (perceive). They recognize the names (interpret). They confirm the right contact is there (compare). Repeat.

**Violation pattern.** Failure at any stage breaks the interaction. Goals not surfaceable (the user doesn't know the system can do what they want). Plans impossible to form (the IA hides the path). Actions not specifiable (the right control isn't findable). Performance impossible (the control is too small, too slow, or unresponsive). Perception unclear (no feedback). Interpretation hard (cryptic labels, system jargon). Comparison broken (no confirmation of state).

**Fix example.** Map every interaction to the seven stages. For each stage, ensure the design supports the user:

- Goal: discoverability — the user can see that the system supports this goal
- Plan: clear IA, search, navigation — the user can form a route
- Specify: visible affordances and signifiers at each step
- Perform: appropriate target sizes, response times, controls
- Perceive: immediate feedback
- Interpret: feedback in user language
- Compare: state visibility, undo, history

**How to spot a violation.** Watch a user attempt a task. The stage where they hesitate, ask for help, or undo their action is the stage the design is failing.

---

## Gulf of Execution + Gulf of Evaluation

**Definition.** Two gaps separate the user's intention from the system's response:

- **Gulf of Execution** — the gap between what the user wants to do and what the system requires them to do. Wide gulf: many steps, hidden affordances, unclear next actions. Narrow gulf: direct paths, visible controls, predictable behavior.
- **Gulf of Evaluation** — the gap between what the system did and what the user can perceive and understand. Wide gulf: cryptic feedback, hidden state, no confirmation. Narrow gulf: clear feedback, visible state, comprehensible language.

**In digital UX.** Wide execution gulf: a "save" function that requires clicking File > Save As > selecting a folder > naming the file > confirming. Narrow execution gulf: Ctrl-S or autosave with a visible indicator.

Wide evaluation gulf: the file is saved somewhere, the user doesn't know where, the file picker shows a flat list of files. Narrow evaluation gulf: a "saved" indicator with timestamp, a clear file location, and easy search.

**Violation pattern.** Every additional click, every hidden state, every cryptic label, every missing feedback widens the gulfs. The wider the gulfs, the more cognitive translation the user does — and the more they fail.

**Fix example.** Narrow execution: minimize steps, surface common actions, provide keyboard shortcuts, autocomplete, smart defaults. Narrow evaluation: clear, immediate, persistent feedback. Visible state. User-language labels. Undo first-class.

**How to spot a violation.** Time a user through a common task. If they hesitate before each action (execution gulf) or after each action (evaluation gulf), the gulfs need narrowing.

---

## The Seven Fundamental Design Principles

Norman's seven principles distill the above into operational rules:

### 1. Discoverability
The user can see what actions are possible and the current state of the system. Hidden features are invisible features. Affordances and signifiers make actions discoverable.

### 2. Feedback
Every action gets a visible, audible, or tactile response. Immediate, informative, appropriately scaled.

### 3. Conceptual Model
The design communicates a clear model of how the system works. The user's model matches the designer's intended model.

### 4. Affordances
The design supports the actions it permits. The visible properties of objects suggest the actions possible.

### 5. Signifiers
The visible cues that communicate where action should take place. Affordances perceivable.

### 6. Mappings
Controls are connected to their effects in obvious ways. Spatial layout, naming, and behavior reinforce the connection.

### 7. Constraints
Possible actions are limited so that errors are prevented and the path of intended use is clear.

**Applied together,** these seven create a self-explaining interface. The user sees what's possible (discoverability), can predict what will happen (mappings, affordances, conceptual model), receives confirmation of what did happen (feedback), and is prevented from common mistakes (constraints). The visible cues (signifiers) connect intention to action throughout.

**Violation pattern.** Designs that score high on one principle but ignore others. Beautiful interfaces with no affordances. Feature-rich interfaces with no discoverability. Powerful systems with no feedback. Each principle is necessary; none is sufficient.

**Fix example.** Use the seven as a checklist on every design review. For the screen at hand:
- What's discoverable? What's hidden?
- What feedback exists? What's silent?
- What's the conceptual model the design communicates? Is it correct?
- What affordances are visible? What's invisible?
- Which signifiers are working? Which are missing?
- Are the mappings natural?
- Which errors are prevented by constraints? Which are only caught after the fact?

Any gap is a fix.

---

## Error Design — Slips vs Mistakes

**Definition.** Human errors fall into two categories:

- **Slips** — the user formed the right intention but executed the wrong action. Clicked the wrong button by accident. Typed the wrong number. Forgot to fill a field.
- **Mistakes** — the user formed the wrong intention. Misunderstood the system. Followed the wrong plan to a flawed conclusion. Chose the wrong option deliberately, because they thought it was right.

Slips and mistakes need different solutions. Slips are addressed by reducing the cost of any single action (undo, confirmation for destructive actions only, autosave). Mistakes are addressed by improving the user's mental model (better information, clearer affordances, narrower gulfs).

**In digital UX.** Slip: user clicks "Delete" instead of "Archive" because the buttons are adjacent and similar. Mistake: user clicks "Delete" thinking it will hide the item rather than remove it permanently.

**Violation pattern.** Treating all errors the same. Confirmation dialogs on every save (which slows the routine case and trains users to dismiss the dialog without reading). Cryptic error messages for both slips and mistakes. No undo because "users should be careful."

**Fix example.** For slips: undo for everything that's undoable. Confirmation dialogs only for destructive, irreversible actions. Adjacent buttons visually differentiated. Smart autosave. Forgiveness over prevention.

For mistakes: clear naming. Visible state. Examples and inline hints. Empty states with example data. Better onboarding for complex features. Better information at the moment of decision.

**Error messages** in either case: specific, in user language, with the fix. Never "form contains errors." Always "Phone number must include the country code." Never "operation failed." Always "Couldn't save — your session expired. [Sign in again]."

**How to spot a violation.** Read every error message in the product. Specific? In user language? Actionable? If not, the error design is failing both slips and mistakes.

---

## Knowledge in the World vs Knowledge in the Head

**Definition.** Knowledge required to operate a system can live in two places:

- **Knowledge in the world** — embedded in the design, visible to the user as they interact. Labels, icons, menus, prompts, defaults, breadcrumbs, current state indicators.
- **Knowledge in the head** — held in the user's memory. Remembered commands, learned shortcuts, mental models of how the system works.

Knowledge in the world is easier for new users, more forgiving, and doesn't require learning. Knowledge in the head is faster for experts, doesn't clutter the interface, and enables fluent use.

Good design supports both. Surface affordances visibly for new users; provide shortcuts and shortcuts for experts. Never force the user to remember what the interface could show.

**In digital UX.** Knowledge in the world: a labeled "Save" button. Knowledge in the head: Ctrl-S. Both should work.

**Violation pattern.** Pure-world designs are cluttered and slow for experts. Pure-head designs are intimidating to new users and exclude anyone who can't memorize. Most violations are pure-head failures — assuming users will remember system structure, command names, or hidden gestures.

**Fix example.** Surface common actions visibly. Provide keyboard shortcuts for the same actions. Show command names alongside icons until the user is fluent. Tooltip-on-hover for everything. Recent items and search to compensate for memory load. Power-user shortcuts that don't compete with novice affordances.

**How to spot a violation.** Watch a new user. What do they have to learn before they can use the product? Anything they have to memorize is knowledge in the head — could it have been knowledge in the world?

---

## Double Diamond Design Thinking

**Definition.** A four-stage design process organized around two divergent-convergent phases:

1. **Discover** (diverge) — understand the problem space. Research, interview, observe, gather. Don't narrow yet.
2. **Define** (converge) — synthesize findings into a clear problem statement. Pick the problem worth solving.
3. **Develop** (diverge) — generate many solutions. Sketch, prototype, ideate, explore. Don't critique yet.
4. **Deliver** (converge) — test, refine, ship the chosen solution.

The first diamond is about problem. The second is about solution. Skipping or compressing either diamond produces fragile design.

**In digital UX.** Discover: user interviews, analytics review, competitive scan, observational research. Define: problem statement, opportunity sizing, persona, scope. Develop: sketches, wireframes, prototypes, multiple approaches. Deliver: usability testing, iteration, handoff, ship.

**Violation pattern.** Jumping to solutions before defining the problem. Defining the problem from inside the team without user data. Picking the first solution without exploring alternatives. Shipping without testing.

**Fix example.** Force the diamonds to be explicit phases. Time-box each. Discover: minimum 5 user interviews. Define: a written problem statement signed off before design starts. Develop: minimum 3 alternative approaches. Deliver: usability testing with at least 5 users before launch.

**How to spot a violation.** Look at any design artifact. Can you point to: the user research that informed the problem? The problem statement? The alternatives considered? The user testing that validated the choice? Any gap is a process violation.

---

## How to spot Norman violations in a review

Run any screen through this checklist. Each "no" is a fix.

**Discoverability**
- Can a new user see what actions are possible on this screen?
- Is the current state visible?
- Is the path to common goals findable in under 3 seconds?

**Affordances + Signifiers**
- Does every interactive element look interactive?
- Does every interactive element have a hover state (or equivalent)?
- Are touch targets at least 44x44 on mobile?

**Mapping**
- Are controls placed near the things they affect?
- Do directional controls match cultural conventions (left-to-right, up-for-more)?
- Are save/cancel/back actions in consistent positions across screens?

**Feedback**
- Does every action produce immediate visible feedback?
- Are long operations indicated with progress, not just a spinner?
- Are success states acknowledged before they disappear?

**Conceptual Model**
- Does the UI use the user's vocabulary?
- Does the IA match the user's mental model, not the engineering model?
- Are states named in user-meaningful terms?

**Constraints**
- Is the system preventing invalid states, not just catching them after?
- Are conflicting options surfaced before submission?
- Are destructive actions distinguishable from routine actions?

**Error Design**
- Is every error message specific and actionable?
- Is undo available for non-destructive actions?
- Are slips prevented through layout (not just confirmation)?

**Gulfs**
- Is the path from intention to action as short as possible?
- Is the path from action to confirmation as short as possible?

Each principle is a lens. Use them in sequence on every review.

---

## Related references

- [The 30 Laws of UX](The-30-Laws-of-UX.md)
- [Krug 3 Laws of Usability with examples](Krug-3-Laws-of-Usability-with-examples.md)
- [The creative arsenal pattern library](The-creative-arsenal-pattern-library.md)
- [Anti-AI slop ban list](Anti-AI-slop-ban-list.md)

---

Repository: github.com/Laith0003/ux-skill | Maintainer: linkedin.com/in/laithaljunaidy
