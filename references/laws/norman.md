# Norman's Design Principles

A working reference for the foundational design laws every interface obeys, whether the designer knows it or not. Use this when you review a screen, plan a flow, or argue with a stakeholder about why a button is broken.

## How to read this file

Each section follows the same shape: a definition you can hand to a junior designer, a list of when the principle applies, the violation pattern you will see in AI-slop and rushed work, a fix example, and a checklist for spotting the violation in a design review. Treat the principles as a lens. Lay one over a screen and ask: "Is this satisfied? If not, where is the cost going?"

The cost is always paid by the user. The question is whether the designer makes them pay it.

---

## Affordances and Signifiers

### Definition

An **affordance** is a relationship between an object and a person — what the object permits that person to do. A door has the affordance of pushing or pulling because it has a hinge and a person has hands. A scrollable list has the affordance of being scrolled because pixels can move and a pointer can drag.

Affordances exist whether or not anyone perceives them. A flat sheet of glass affords smashing, but a user does not know that until they pick up a brick.

A **signifier** is a perceivable indicator that communicates the affordance. The handle on the door says "pull." The scrollbar on the list says "this content continues." The underline under text says "this is a link."

The two are not the same. Affordances are possibilities. Signifiers are signals. You cannot have a usable interface with only one.

### When it applies

- Every interactive element on every screen.
- Any control that users do not interact with the moment they see it.
- Any control that users interact with by mistake.
- Any control that users describe with the wrong verb ("I tried to click the icon" when it was a label).

### Violation pattern

- Flat design that strips signifiers from buttons. The element affords clicking, but nothing tells the user it does.
- Hover-only signifiers on touch devices. On a phone, there is no hover. The signifier never appears.
- Decorative icons that look like buttons but do nothing. The icon affords pressing, but the system ignores the press. Reverse-violation.
- "Click here" links where the affordance is "the underlined word." Users now have to read prose to find what to click.
- Cards that are sometimes clickable and sometimes not. Same visual signifier, different affordance, depending on context.

### Fix example

Make the signifier match the affordance:

```html
<!-- Bad: looks like text, is a button -->
<span onclick="submit()">Submit</span>

<!-- Good: looks like a button, is a button -->
<button type="submit" class="btn btn-primary">Submit</button>
```

On touch interfaces, make every interactive surface look interactive without hover. Borders, fills, shadows, and weight communicate "I can be pressed."

If an element looks pressable but has no action, remove the visual cues. Make it look like a label. If an element is pressable but does not look it, add a border, a weight, a fill, or a chevron.

### How to spot it in review

- Walk through the screen with the question: "If I had never seen this app, would I know what to press?"
- Cover the labels. Are the controls still identifiable as controls by shape and weight alone?
- Check every icon. Is it interactive? If yes, does it look interactive? If no, does it look static?
- Check hover-only behaviors on a touch device. They are invisible there.

---

## Mapping

### Definition

Mapping is the relationship between a control and the thing it controls. Good mapping reduces the user's need to think. Bad mapping forces the user to remember.

**Natural mapping** uses spatial or physical analogy. Up means up. Right means right. A volume slider going up makes the sound louder.

**Cultural mapping** uses learned convention. Red means stop or danger. Green means proceed. A floppy-disk icon means save. These are not natural — they are taught, but once taught they are universal within a culture.

**Arbitrary mapping** is the failure mode. The control bears no perceivable relation to the thing it controls. Users have to memorize the relationship.

### When it applies

- Any control that selects, adjusts, or aims at another part of the system.
- Spatial controls (sliders, drag handles, joysticks, knobs).
- Sequential controls (carousels, paginators, tabs).
- Multi-input forms where the field arrangement should match the entity being described.

### Violation pattern

- Volume slider whose handle moves right but the level meter goes up. Conflicting directions.
- A grid of four stove burners controlled by four knobs in a line. Which knob is which burner? The user has to read labels every time, or burn dinner.
- A carousel with left/right arrows whose order does not match left-to-right reading. The right arrow goes backward.
- A form with first-name on the right and last-name on the left, both right-aligned, in an LTR language. The mapping fights the user's reading direction.
- RTL languages where the designer forgot to mirror direction controls. Forward and back are flipped, but the buttons are not.

### Fix example

A stove with four burners arranged in a square should have four knobs arranged in the same square, each below its burner. The user looks at the burner, looks at the knob below it, turns the knob. No labels needed.

A volume slider should have low at the bottom and high at the top. Or low on the left and high on the right (in an LTR layout). Or — if you must — flip the whole thing in RTL.

A carousel in an RTL layout should advance in the natural reading direction (right to left). The "next" button is on the left. The "previous" button is on the right.

### How to spot it in review

- Ask: "If I press this control, what do I expect to move? Does that thing actually move that way?"
- For grouped controls, ask: "Does the spatial arrangement of controls match the spatial arrangement of what they control?"
- Verify RTL behavior. Mirror the layout and re-check every directional control.
- Look for labels that are doing the work the mapping should be doing. Labels are a sign of failed mapping.

---

## Feedback

### Definition

Feedback is the system's reply to the user's action. "I heard you. Here is what happened, or what is happening, or what failed."

Feedback is mandatory. Every action must produce feedback within a perceivable window, or the user assumes the action did not register and either repeats it or abandons the task.

Feedback has types:

- **Immediate visual feedback**: button press states, focus rings, hover effects, loading spinners that appear within 100ms.
- **Audible feedback**: confirmation sounds, error tones, click sounds for hardware-style interactions.
- **Haptic feedback**: vibration on touch devices for confirmations, errors, or impact effects.
- **Status feedback**: progress bars, percentages, ETA strings, log scrolls.
- **Result feedback**: success toasts, banners, navigation transitions, refreshed content.

### When it applies

- Every user action — every tap, click, drag, swipe, keystroke, voice command.
- Especially long-running actions where the user cannot tell whether anything is happening.
- Especially destructive or financial actions where the user needs to know the system accepted or refused the command.

### Violation pattern

- Form submit button that gives no visual change when pressed. The user presses again. Now the form submits twice.
- Async action with no loading state. The user does not know if the system is working or frozen.
- Saved-without-feedback. The user does not know whether their edit took. Many users will try to save again, or close the screen and find out later.
- Error toasts that flash for 1.5 seconds and disappear. The user did not have time to read the message.
- Audible feedback by default at volumes that embarrass the user in public.
- Haptic feedback for trivial actions, draining battery and attention.

### Fix example

For an async save:

```js
async function save() {
  // 1. Immediate feedback: disable button, show spinner
  button.disabled = true
  button.textContent = 'Saving...'

  try {
    await api.save(payload)
    // 2. Result feedback: success state, visible long enough to read
    showToast('Saved.', { duration: 3000 })
    button.textContent = 'Saved'
    setTimeout(() => { button.textContent = 'Save' }, 1500)
  } catch (err) {
    // 3. Error feedback: persistent, named, actionable
    showBanner('Save failed: connection lost. Try again or copy your text.')
    button.disabled = false
    button.textContent = 'Try again'
  }
}
```

Feedback should be loud enough to perceive, brief enough not to interrupt, and persistent enough for errors that the user can act on the information.

### How to spot it in review

- Press every button and watch for a visual change within 100ms.
- Trigger every async path. Is there a loading state? Is it visible long enough?
- Trigger every error path. Does the user know what failed and what to do?
- Trigger the success path. Does the user know it succeeded?
- Check destructive actions specifically — delete, send, charge, submit. Feedback here must be unambiguous.

---

## Conceptual Models

### Definition

A **conceptual model** is the user's compressed, working theory of how a system works. It does not have to be accurate. It has to be useful enough that the user can predict the next thing the system will do.

The designer also has a conceptual model — usually closer to the actual implementation. The **system image** is what the user sees and interacts with: the interface, the docs, the error messages, the marketing pages, the icon.

The user constructs their conceptual model entirely from the system image. They cannot read your code. They cannot read your mind. If the system image is incoherent, the user's model will be incoherent.

The communication gap between the designer's model and the user's model is the source of most usability failures.

### When it applies

- New product onboarding.
- Any abstraction the user must reason about (folders, tags, accounts, projects, workspaces, channels).
- Recovery from error states ("Where is my data?").
- Migration between similar products (the user brings the old product's conceptual model with them).

### Violation pattern

- Three different abstractions that look the same in the interface but behave differently (e.g., "folder," "collection," "library" all rendered as folders).
- Hidden state that the user cannot perceive (a sync that has not completed but is not visible).
- Inconsistent vocabulary in different parts of the product. The dashboard says "Members," the settings says "Users," the API says "Accounts."
- Magic — features that work without the user understanding why. Magic looks great until it breaks; then the user has no model with which to recover.

### Fix example

Pick a single conceptual model and enforce it everywhere — code, UI, docs, marketing, error messages. If your product is "a workspace with channels and members," then every screen, error message, and email uses those three words. Not "team," not "user," not "group."

Make the model visible. If a sync is happening, show a sync indicator. If an item is shared, show a shared icon. If a feature is in beta, label it beta. Externalize the model into the system image so the user can construct it from what they see.

When the user is wrong about the model, fix the system image, not the user.

### How to spot it in review

- Ask: "What does the user think this system is?"
- Read the screen with no prior context. Can you construct a coherent model from this one screen?
- Walk through the product with three different feature areas. Do they share the same vocabulary, the same metaphors, the same mental shape?
- Check error messages and empty states. Do they teach the model, or assume the user already has it?

---

## Constraints

### Definition

Constraints are the limits that guide the user toward correct actions and away from errors. They are the second-best tool in the usability toolbox; the best is "the wrong action is impossible."

Constraints come in four flavors:

- **Physical constraints** — the action is physically impossible. A jigsaw piece only fits one way. A USB-C plug fits either orientation. A USB-A plug fits one orientation in practice and three in user expectation.
- **Logical constraints** — the user reasons that the action does not make sense. If three of four pieces fit, the fourth must go in the empty slot.
- **Semantic constraints** — meaning rules out the action. A windshield faces forward; you would not install it on the back of the car because windshields are for seeing the road.
- **Cultural constraints** — convention rules out the action. Red is stop. Files go in folders. The X in the top-right closes the window (depending on platform).

### When it applies

- Forms with strict input requirements.
- Wizards with sequential steps.
- Configuration screens with co-dependent options.
- Anywhere the user could make an irreversible mistake.

### Violation pattern

- Date pickers that allow February 30. The system should refuse the impossible.
- Forms that allow submission with invalid data and reject only at the server. The constraint is server-side, not visible to the user. The user thinks they completed the task; the server disagrees.
- Sequential wizards where step 3 is enabled before step 2 is complete. The user fills in step 3, then discovers step 2 invalidated it.
- Buttons that are visually enabled but do nothing when pressed because some hidden state is invalid. The constraint exists but is invisible.

### Fix example

Use HTML5 input constraints to prevent the impossible at the input level:

```html
<input type="email" required>
<input type="number" min="0" max="100">
<input type="date" min="2026-01-01">
```

Disable controls that cannot be used yet. Show why they are disabled (tooltip, helper text, or inline message): "Complete step 2 to continue." A disabled button without explanation is a worse experience than no button at all.

Use semantic and cultural constraints to your advantage. If your audience reads top-to-bottom, lay out the form top-to-bottom. If your audience expects a destructive action to be on the right with a confirmation, do not put it on the left without confirmation.

### How to spot it in review

- Look for ways to enter invalid data. If the user can submit invalid data, the constraints are weak.
- Look for disabled controls. Is the reason clear?
- Look for cultural assumptions. Are they true for the audience you actually have, not the one you imagined?

---

## The Seven Stages of Action

### Definition

Every interaction with a system passes through seven stages. The user moves from a goal to an outcome by:

1. **Goal**: What does the user want to achieve? ("I want to share this document with my team.")
2. **Plan**: What is the rough plan to achieve it? ("I will open the document, find a share button, enter their names.")
3. **Specify**: What specific actions does the plan require? ("Click 'Share.' Type 'alice@team.com.' Click 'Send.'")
4. **Perform**: Execute the action. (The user clicks, types, clicks.)
5. **Perceive**: What did the system do in response? (A modal appears. A toast says "Invitation sent.")
6. **Interpret**: What does the response mean? ("My team can now access this.")
7. **Compare**: Did the outcome match the goal? ("Yes. Done.")

Stages 1–3 are the user's planning. Stage 4 is the user's input. Stages 5–7 are the user's understanding of the result.

### When it applies

- Any task you are designing or reviewing.
- Especially: tasks that users abandon, get wrong, or do not start.

### Violation pattern

- Goal-formation failure: the user does not know what is possible. They cannot form a goal because they do not know the system can help. (Solve by surfacing capabilities — empty states, onboarding, examples.)
- Planning failure: the user cannot construct a plan. The product is too abstract or too novel. (Solve by progressive disclosure, templates, and guided flows.)
- Specification failure: the user knows the plan but cannot map it to actions. They do not know which button does which thing. (Solve by labels, signifiers, mappings.)
- Performance failure: the user knows the action but cannot execute it (target too small, too far, blocked). (Solve by Fitts's Law, layout, accessibility.)
- Perception failure: the user cannot tell what the system did. (Solve by feedback.)
- Interpretation failure: the user perceived the response but does not understand it. (Solve by clear language, conceptual models.)
- Comparison failure: the user is unsure whether the goal was achieved. (Solve by clear success states and persistent confirmation.)

### Fix example

For each stage, define what the user needs:

- Goal: discoverability. "Share" is visible in the toolbar.
- Plan: an obvious starting point. "Share" is the first button.
- Specify: explicit options. "Share" opens a dialog with three named fields.
- Perform: actionable. The "Send" button is large and reachable.
- Perceive: feedback. Toast: "Shared with Alice."
- Interpret: clear language. "Shared" not "Invitation deliverable status: ACCEPTED."
- Compare: persistent state. The share dialog now shows "Alice has access."

### How to spot it in review

- Pick a user goal. Walk through all seven stages. At each stage, ask what the user needs and whether the design supplies it.
- Stages where users get stuck reveal the design's weak spot.

---

## Gulfs of Execution and Evaluation

### Definition

The **gulf of execution** is the gap between what the user wants and what the system requires them to do. A wide gulf means the user must do a lot of work to translate their goal into commands the system understands.

The **gulf of evaluation** is the gap between what the system shows and what the user can understand from it. A wide gulf means the user cannot tell what the system did, or why, or what to do next.

A good design closes both gulfs.

### Measurement

- Time to complete a task (gulf of execution).
- Number of actions per task (gulf of execution).
- Time from result to user comprehension (gulf of evaluation).
- Rate of correct user inference from system output (gulf of evaluation).

### How to close them

- Close the gulf of execution by making the system understand the user's natural way of expressing their goal. Provide affordances that map to goals, not to internal implementation. ("Share a file" not "configure ACL.")
- Close the gulf of evaluation by making the system's state perceivable, interpretable, and aligned with the user's conceptual model. Clear status, clear errors, clear language.

### Violation pattern

- User has to think through internal mechanisms to do anything. "To share, I need to first configure permissions, then generate a token, then..." — the system has made the user do its work.
- User completes the action but cannot tell whether it worked. The screen shows a JSON payload, a status code, or no visible change. Translation work falls on the user.

### Fix example

Replace "Configure ACL for user@team.com" with "Share with user@team.com." The gulf of execution shrinks because the system speaks the user's language.

Replace a green "Success" with no further info with "Shared with Alice. She can now view this document." The gulf of evaluation shrinks because the system explains what happened in terms the user already understands.

### How to spot it in review

- Time the task. If it takes longer than the user expects, the gulf of execution is wide.
- Ask testers to explain what the system did after they finished an action. If they cannot, the gulf of evaluation is wide.

---

## The Seven Fundamental Design Principles

### Definition

The seven principles that should be visible in every well-designed interface:

1. **Discoverability**. Can the user find what they need? Every required action must be visible or trivially uncovered.
2. **Feedback**. Does the system tell the user what is happening? Every action gets a response.
3. **Conceptual model**. Can the user predict what will happen next? The system image teaches the model.
4. **Affordances**. Does the system support the actions the user wants? Capabilities are present.
5. **Signifiers**. Does the user know the actions are available? Capabilities are perceivable.
6. **Mappings**. Do the relationships between controls and outcomes match natural expectations?
7. **Constraints**. Does the system prevent or guide against errors?

### When they apply

- Every screen.
- Every interaction.
- Every error.

### How to use them in review

Treat them as a checklist. Run a screen through all seven, asking "Is this principle satisfied? If not, where is the gap?"

A screen that passes all seven is rare. A screen that fails three or more is the source of most user complaints.

### Violation pattern

- Discoverability gone: a critical feature is buried four levels deep with no entry point.
- Feedback gone: the action button does nothing visible for two seconds, then completes.
- Conceptual model gone: the same word means different things in different parts of the product.
- Affordances gone: the user wants to share but the share function exists only in the API.
- Signifiers gone: every control is a flat label, no visible borders, no apparent grouping.
- Mappings broken: arrows that go the wrong way, sliders that increase by going left.
- Constraints absent: the user can break things easily and there is no warning, no undo, no guidance.

### Fix example

Walk through the screen with the seven principles, naming the gap, and fixing it. Often the fix is small: a border around a button (signifier), a confirmation toast (feedback), a tooltip on a disabled control (constraint).

### How to spot violations in review

Score the screen 1 to 5 on each principle. Any 1 or 2 is a blocker. Any 3 is a quality risk. 4s and 5s are baseline.

---

## Errors: Slips vs Mistakes

### Definition

Errors come in two kinds:

A **slip** is when the user knows what they want to do but executes the wrong action. Their intention is correct; their execution is wrong. Example: typing the wrong password because their fingers slipped. Wanting to "Save" but clicking "Save As." Selecting the wrong item from a long list because the items look similar.

A **mistake** is when the user executes the action they intended, but their intention was wrong. Their plan was based on bad information or a bad model. Example: deleting a file they thought was a duplicate but was actually the only copy. Configuring DNS to point to the wrong server because the user's model of "production" was outdated.

### Prevention

- For slips: constraints, larger targets, confirmation only for destructive actions, autocomplete, undo.
- For mistakes: better conceptual models, clearer feedback, externalized state, dry-runs and previews, helpful defaults, education.

### Recovery

- For slips: undo. The user knows what they meant; let them get back.
- For mistakes: longer-form recovery. The user did not realize they were wrong. Provide audit logs, snapshots, support escalation.

### Design for both

Every action that could be a slip should be reversible. Every action that could be a mistake should produce a state the user can examine and understand before commitment.

### Violation pattern

- Destructive actions with no undo. The user slipped and now their data is gone.
- One-click confirmations on irreversible operations. The user made a mistake and now their environment is broken.
- Confirmation dialogs for every action, including trivial ones. The user stops reading them and clicks through, making the confirmation worthless.

### Fix example

```html
<!-- Bad: irreversible, no warning, no undo -->
<button onclick="deleteAccount()">Delete account</button>

<!-- Good: reversible default, named consequence, recovery window -->
<button onclick="scheduleAccountDeletion()">Schedule deletion</button>
<!-- User sees: "Your account will be deleted in 30 days.
     Sign in any time before then to cancel." -->
```

For high-consequence actions, replace immediate destruction with delayed destruction plus a recovery path.

### How to spot it in review

- Look at every action that cannot be reversed. Is there a confirmation? Is there undo? Is there an audit trail?
- Look at every confirmation. Is it specific enough that the user has to think before clicking? Or is it generic enough that the user clicks through without reading?

---

## Knowledge in the World vs Knowledge in the Head

### Definition

**Knowledge in the world** is information available in the environment — labels, signs, controls, displays. The user does not have to remember; they look.

**Knowledge in the head** is information the user must remember — keyboard shortcuts, command syntax, the meaning of icons, the order of steps in a wizard.

Knowledge in the world is slower per interaction but requires no learning. Knowledge in the head is faster per interaction (after learning) but requires effort to acquire and is fragile to disuse.

### When to externalize (put it in the world)

- First-use experiences.
- Infrequent actions.
- High-consequence actions.
- Actions the user does not perform daily.
- Anything where the cost of forgetting is high.

### When to internalize (let it stay in the head)

- Power-user shortcuts.
- High-frequency actions where speed matters.
- Tasks that build muscle memory.

The best designs offer both. Externalize by default, with shortcuts for experts.

### Violation pattern

- A power-user interface that requires memorizing keyboard shortcuts to be productive, with no discoverable equivalent. New users cannot use the system.
- A novice interface that requires every action to be done through menus, with no shortcuts. Power users are throttled.
- Icon-only toolbars where the meaning is not labeled. The user has to learn an iconography.
- Documentation that lives only on a website. The user cannot find it from inside the app.

### Fix example

Show keyboard shortcuts next to menu items. Externalize the head knowledge. Power users learn the shortcuts over time; new users use the menus. Same control, two paths.

```
File
  New          Cmd+N
  Open         Cmd+O
  Save         Cmd+S
  Save As      Shift+Cmd+S
```

### How to spot it in review

- Ask: "What does the user have to remember to use this screen?"
- Find every piece of knowledge in the head. Can it be in the world without slowing power users?
- Find every piece of knowledge in the world. Is it slowing power users? Offer a shortcut.

---

## Human-Centered Design Process

### Definition

Human-centered design is iterative. It is not a sequence; it is a loop. The loop has four phases:

1. **Observation**: watch real users in their real environments. Understand the actual problem, not the assumed one.
2. **Idea generation**: produce many possible solutions. The first idea is rarely the best one.
3. **Prototyping**: build the cheapest version of the idea that can be tested.
4. **Testing**: put the prototype in front of users and observe.

The loop runs until the design solves the actual problem. Each loop teaches what the previous loop missed.

### When it applies

- Every product. Every feature. Every screen.
- Especially: new problem spaces, novel user groups, high-consequence systems.

### Violation pattern

- Designing from your own intuition without observation. Assuming you know the user because you have been a user of similar things.
- One idea, no alternatives. Locking in too early.
- Prototyping at high fidelity. Polishing what should be tested as a sketch.
- Testing only with people who already understand the product. Friends, colleagues, internal testers.
- Stopping after one loop. The first prototype almost never solves the problem; it surfaces the next question.

### Fix example

For a new feature:

1. Observe five real users doing the task today (without your product). What is hard? What workarounds do they use? What is the actual goal?
2. Sketch five different solutions. Do not commit yet.
3. Prototype the most promising sketch in low fidelity. Paper, click-through, screenshots.
4. Test with five users. Watch where they get stuck. Note what they expected versus what happened.
5. Refine. Loop.

The first three loops are cheap. The fourth and later loops should be in code, but only after the design is settled in concept.

### How to spot violations in review

- Ask: "Who did we observe doing this task?" If the answer is "no one" or "ourselves," the design is at risk.
- Ask: "What was the original problem?" If the answer is "we wanted to add this feature," the design is at risk.
- Ask: "What did the first prototype look like? What did we learn?" If there was no prototype, the design has not been tested.

---

## Solving the Right Problem

### Definition

Most failed designs solve the wrong problem brilliantly. Solving the right problem requires you to question the problem statement before you accept it.

The **Double Diamond** model describes the process:

- **Diamond 1: discover the problem.**
    - Diverge: explore the problem space. What is going on? Why does the user struggle? What are all the framings of the issue?
    - Converge: define the actual problem. State it in one sentence.
- **Diamond 2: solve the problem.**
    - Diverge: generate many possible solutions. Refuse to lock in.
    - Converge: choose a solution. Prototype it. Test it.

Each diamond has divergence (open up the space) followed by convergence (commit to a single answer).

### When it applies

- Any time someone hands you a problem statement.
- Any time you are about to start designing.

### Violation pattern

- Accepting the first problem statement. The stakeholder says, "Users do not click the upgrade button." You add an arrow pointing to the button. The actual problem was that users do not see value in the upgrade — the button works fine.
- Skipping divergence in the first diamond. You see the symptom and reach for the obvious fix.
- Skipping divergence in the second diamond. You pick the first solution that comes to mind and ship it.
- Converging too early in either diamond. You commit before you understand.

### Fix example

A team is asked: "Add an export-to-PDF feature; users keep asking for it." Apply the Double Diamond:

- Diverge in diamond 1: why are users asking for PDF? Because they want to share with people who do not have the product? Because they need printable copies? Because they need to send to their accountant? Because they need to archive?
- Converge: the real problem is "users need to send data to external parties who do not use our system."
- Diverge in diamond 2: PDF, CSV, email-a-summary, a public link, a printable web view, a partner integration.
- Converge: a public, read-only link with a "Download as PDF" option satisfies most cases. Cheaper to build than full export. Solves the actual problem.

### How to spot it in review

- Ask: "What problem are we solving?" If the answer is the same as the proposed solution, you are not solving a problem — you are building a feature.
- Ask: "What were the other framings? What did we rule out?"
- Ask: "What were the other solutions? Why did we pick this one?"

If those answers do not exist, run both diamonds before approving the design.

---

## Putting it together: design review checklist

Use this when reviewing a screen, a flow, or a feature.

### Affordances and signifiers
- Is every interactive element visibly interactive without hover?
- Are decorative elements distinct from interactive ones?

### Mapping
- Do directional controls match the direction of effect?
- Does the spatial layout of controls match the spatial layout of what they control?
- Does the design work in RTL?

### Feedback
- Does every action produce a response within 100ms?
- Do long actions show a progress state?
- Do errors say what failed and what to do?
- Do successes confirm in a way the user can perceive?

### Conceptual model
- Is the vocabulary consistent across the product?
- Is hidden state made visible?
- Can a new user predict the next thing the system will do?

### Constraints
- Is invalid input prevented at the source?
- Are disabled controls explained?
- Are destructive actions guarded?

### Seven Stages of Action
- For each user goal, can you trace all seven stages? Where does the design support or fail each stage?

### Gulfs
- Does the user have to translate their goal into the system's vocabulary?
- Does the user have to translate the system's output into their understanding?

### Errors
- Are slips recoverable (undo)?
- Are mistakes detectable before commitment (preview, dry-run)?

### Knowledge
- What does the user have to remember to use this screen?
- Can that knowledge be externalized without slowing experts?

### Process
- Was this designed from observation?
- Were alternatives considered?
- Was a prototype tested?
- Is the problem the actual problem, not the stated one?

A design that scores well on every line is rare. A design that scores poorly on more than three is unfit to ship.
