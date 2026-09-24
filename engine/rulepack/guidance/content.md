# Content

## Summary

Words are part of the design. This file holds the content rules every contract's copy rules point to: errors, empty states, buttons, destructive confirmations, labels, and numbers. Each rule is a rule, not a string: it says what the words do, so it holds in every language the product speaks. Test every piece of copy four ways: could it be an icon, could two pieces be one, would a person say it aloud, and what is the most that can go before it breaks.

## Error messages

- Say what happened, then the next step, in one or two short sentences.
- Name the field or the thing that failed, and use the real value when it helps: the file name, the amount, the number of characters over the limit.
- Give the fix a person can act on now; a message with no next step is not finished.
- Never apologize, never blame the person, and never write only that something is invalid or went wrong.
- Keep the same terms the interface uses; an error never introduces a new name for a field.
- Show the message next to what failed, with an icon, and announce it to assistive technology.

## Empty states

- Say what is missing in one sentence, then offer one action to fill it, as a verb.
- Say why it is empty when the reason is not obvious: nothing created yet, a filter hides everything, no access.
- A first-use empty state invites; a filtered empty state offers to clear the filter; an error empty state follows the error rules.
- Never apologize for an empty state, and never leave a blank area with no words.

## Buttons and actions

- Start with a verb that names what happens: Save, Send code, Add card.
- Use the verb alone when the context is clear; add the object when two actions on one view could be confused.
- Keep the same verb while the action runs; the spinner shows progress, the words do not change to a gerund.
- One line, no end punctuation, sentence case.
- A link inside text says where it goes; never click here.

## Destructive confirmations

- The title names the action and its object: Delete 3 files?
- The body says what will be lost and whether it can be undone.
- The confirming button repeats the verb and the loss: Delete files. The other button keeps things as they are: Keep files.
- Never offer yes and no, OK and cancel, or any pair that needs the question to make sense.
- A confirmation is for actions that cannot be undone; an action that can be undone runs at once and offers undo.

## Labels and helper text

- A label names the value in two or three words, with no colon.
- Helper text says the format or the limit before the person types, not after an error.
- A placeholder shows an example and never replaces the label.
- Headings and labels describe what follows them (WCAG 2.4.6); a heading such as More or Details alone is not enough.

## Numbers, dates and currency

- Use Western digits (0 to 9) in both scripts unless the product decides otherwise and says so.
- Put the currency after the amount with a space when the market reads it that way: 50 JOD.
- Write dates in the order the market reads them, with the month as a word when order could be ambiguous.
- Phone numbers, codes, email addresses and identifiers run left to right in every direction and are grouped as the country writes them (direction.md).

## Audit checks

- Every error names what failed and the fix; a generic error is a finding that quotes the message.
- Every empty state has one sentence and one action.
- Every button starts with a verb and keeps it while loading.
- No destructive confirmation offers yes and no.
- No label is replaced by a placeholder.
- Cite the rule by this file and heading, and trace it to the contract whose copy rule it breaks.
