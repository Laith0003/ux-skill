# Nielsen's ten heuristics, as checks on a built page

Jakob Nielsen's ten usability heuristics (1994, refined since) are the most used checklist for reviewing an interface. They are broad on purpose. This file turns each into what to look for on a page an AI built, and names the ux-skill check that measures it where one exists, so a review spends its attention on what no check can see.

Use it as the spine of `/ux-audit`: walk the ten in order, and for each write findings as counts and places, never adjectives.

---

## 1. The system shows what is happening

The person always knows the state: what loaded, what is saving, what failed, where they are.

- Every action answers within about 100ms with a visible change: a pressed state, a spinner, a disabled button while it works. `uxskill lint --render` measures hover and press that answer late.
- Anything that takes longer than a second shows progress; anything that takes longer than ten says how long or lets the person leave.
- The current page or tab is marked in the navigation, and the mark is more than color.
- A form says it saved, in words near the button, not only in a toast that vanishes.

## 2. The words are the person's, not the system's

Labels, order and icons follow how the audience already thinks about the task.

- No internal names in the interface: table names, status codes, enum values ("PENDING_REVIEW").
- Dates, currency and numbers in the reader's locale. For Arabic copy, see `references/foundations/copy.md`.
- Icons that need a label to be understood have one.
- The steps follow the real order of the task, not the order of the database.

## 3. The person can leave and undo

People act by mistake. They need a clearly marked way out that does not cost them their work.

- Every dialog closes on Escape and by a visible close control, and focus returns to what opened it. `lint --render` drives Escape and checks where focus lands.
- A destructive action can be undone, or asks first and names exactly what it will remove.
- A multi-step flow keeps what was typed when the person goes back.
- A toast that carries Undo stays until the person acts or dismisses it.

## 4. One thing, one name, one look

The same action looks and is named the same everywhere, and the page follows the platform's conventions.

- One label per action across the page (record `one-label-per-action`).
- Links look like links and buttons look like buttons; nothing that does nothing has a pointer cursor.
- The logo returns home; the search field sits where people look for it.
- Every color, size and radius comes from the system's roles: `lint` reads values against the page's own token set.

## 5. Mistakes are prevented before they are reported

The best error message is the one that never needs to show.

- Fields carry the right `type`, `inputmode` and `autocomplete`, so the keyboard and autofill do the work.
- Constraints are stated before the person types (password rules, accepted formats), not discovered on submit.
- A risky action and its safe neighbour are not the same size and color side by side.
- `target-too-small` catches controls crowded close enough to hit the wrong one.

## 6. Options are visible, not remembered

The person recognises what they need on screen instead of recalling it from a page ago.

- Labels sit outside fields, not as placeholders that vanish on typing (`placeholder-as-label`).
- Choices are shown, not hidden behind an icon nobody can name.
- Recent and frequent items surface first where the task repeats.

## 7. Fast for the expert, clear for the newcomer

The interface serves the first visit and the hundredth.

- Keyboard paths for repeated actions, and every action reachable by Tab in a sensible order.
- Defaults that suit most people, with the rest one step away.
- Dense views stay readable: see the compact density mode in the system.

## 8. Only what the task needs

Every extra element competes with the ones that matter.

- One clear first thing on each screen: the largest text is the heading, and one button leads.
- No decoration standing in for content: three equal icon cards, a gradient where a photograph belongs, a stat strip with no source (the anti-slop rules in `references/styles/anti-slop.md`).
- Nothing fixed covers the first screen at rest (`first-screen-covered`).

## 9. Errors say what happened and how to fix it

When something fails, the message names the problem in plain words and the way forward.

- The message sits beside the field it is about, in text, and is announced to assistive technology.
- It names the fix ("Enter a date after today"), not the rule that was broken ("Invalid input").
- What the person typed stays in place after the error.

## 10. Help is there when it is needed

Most people never read help, so the interface explains itself; what help there is sits next to the task.

- Hints sit beside the field that needs them, not on a separate page.
- Empty states say what goes here and offer the first action.
- Help text is searchable and written as steps.

---

## What the checks cover, and what is left to you

`uxskill lint` and `uxskill lint --render` measure parts of heuristics 1, 3, 4, 5, 6 and 8: late feedback, focus after Escape, value drift from the system, crowded targets, placeholders as labels, covered first screens, low contrast. Heuristics 2, 7, 9 and 10 are about words and the task: read them yourself, and when the person names something wrong, keep it as a complaint (`uxskill complaints check`) so the fix is measured before it is called done.

See also: `krug.md`, `norman.md`, `laws-of-ux.md`.
