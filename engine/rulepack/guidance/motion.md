# Motion

## Summary

Motion sets how things move: seven interaction roles and one expressive role for decoration, each with a duration and a curve and, where something travels, a distance, plus a sign that mirrors horizontal travel under right to left. The motion axis sets the pace, and the motion and formality axes bend every curve continuously from plain to springy (decisions/expressive-motion.md). Reduced motion is a mode: roles keep their meaning with no travel, and one-shot moves take gentle curves and short durations. Motion does not govern the color or layout of what moves.

## Principles

- **Motion explains a change.** Every move shows what changed, where something came from or went; motion for decoration is removed first.
- **Continuity.** A move links the before and the after, so people keep track of the object.
- **Right at the moment.** A change is shown when it happens, not before and not long after.
- **Orientation.** The direction of a move matches where things are: a panel from the start edge moves along the line of reading.
- **Restraint.** Motion is quiet by default and lively only when the brand asks for it through the motion axis.
- **Proportion.** Small changes move briefly; larger changes move longer, but never so long that people wait.
- **Natural pace.** Things arriving slow down into place; things leaving speed up out of the way.
- **Same change, same motion.** One role per kind of change, used the same way everywhere.
- **Leaving is faster than arriving.** A dismiss never holds the next action longer than the reveal did.
- **One clear signal.** Under reduced motion a change keeps one plain signal, such as a quick fade, rather than several weak ones.

## Roles

- `motion.<role>.duration`: how long the <role> move lasts.
- `motion.<role>.curve`: how the <role> move speeds up and slows down.
- `motion.<role>.distance`: how far the element travels in the <role> move; never negative (0 under reduced motion), with the direction from motion.inline-sign.
- `motion.inline-sign`: 1 in left to right and -1 in right to left; multiply horizontal travel by it.

## Choosing

The seven roles are press (a control confirms a tap in place), reveal (something arrives: a menu, a dialog, a panel), dismiss (something leaves), swap (one content replaces another in place, such as tab content), expand (something grows or shrinks, such as an accordion), page (a move between pages or views) and progress (a loop that shows work under way, the only linear curve).

| Change | Role | Notes |
|---|---|---|
| A tap, a toggle, a check | press | no travel; the feedback stays under the finger |
| A menu, a dialog, a panel appears | reveal | short travel from where it comes from |
| It closes | dismiss | shorter than the reveal |
| One content replaces another in the same place | swap | no travel when the place does not change |
| A section opens or closes | expand | size changes, the page reflows |
| A move to another page or view | page | the longest one-shot move |
| Work under way | progress | a linear loop that keeps its pace |
| A value updates in a dense view | none, or swap at its shortest | frequent changes stay quiet |
| A section reveals on scroll, a success is celebrated | expressive | decoration only; gone under reduced motion |
| Nothing changes that matters | none | never add motion for its own sake |

Movement follows the smallest axis that explains the change: along one axis before two, translate for position, scale only for growth from a point, and opacity to support a move, not to replace one that carries meaning. The transform origin is where the change starts: a menu grows from its trigger.

## Modes

Motion varies on motion (standard, reduced) and direction (ltr, rtl). Under reduced motion every role keeps its meaning: travel drops to 0, one-shot curves turn gentle, one-shot durations cap at 100ms and never grow, a dismiss may tie a reveal but never outlast it, the progress loop keeps its standard duration and linear curve because it reports status (decisions/motion-roles.md), and the expressive role is removed: 0ms and no travel. Under right to left the sign turns -1 so horizontal travel mirrors (decisions/unsigned-distances.md). The mode follows prefers-reduced-motion unless data-motion is set on the html element.

Under reduced motion drop scale as well as travel: an element that grows from a point appears at full size, with a quick fade if it needs a signal.

## Changing the system

1. Motion moves with the motion axis, and its curves with the motion and formality axes: every role grows calmer or livelier together. Change the axis in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
2. The build keeps dismiss shorter than reveal, press in place, reduced values never longer than standard ones, and progress linear at 334ms or more per cycle, our floor; a failed check names the role and the mode.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

Audits the motion roles in both motion modes and both directions: reduced travel, length and curves, dismiss against reveal, press in place, the progress loop, and the mirrored sign. The WCAG risks are flashes (2.3.1: nothing flashes more than three times in any one second unless the flashes stay below the flash thresholds), motion from interaction that cannot be turned off (2.3.3, AAA) and moving content that cannot be paused (2.2.2). One-shot moves cannot flash, so 2.3.1 matters for loops only. It does not audit the color of what moves or video content.

## Checks

- `reduced-travel`: under reduced motion no role travels (WCAG 2.3.3).
- `reduced-length`: under reduced motion no one-shot role lasts more than 100ms.
- `reduced-curve`: under reduced motion no curve overshoots.
- `dismiss-faster`: a dismiss is shorter than a reveal; under reduced motion it may tie but never be longer.
- `progress-linear`: the progress loop runs at an even pace.
- `progress-keeps-pace`: under reduced motion the progress loop keeps its standard duration and curve.
- `mirrored-motion`: the inline sign is 1 in left to right and -1 in right to left.
- `press-in-place`: a press never travels.
- `linear-progress-only`: only the progress loop is linear; every one-shot move eases.
- `reduced-not-longer`: reduced motion never makes a role longer.
- `expressive-removed`: under reduced motion the expressive role lasts 0ms and does not travel (WCAG 2.3.3).
- `progress-floor`: one cycle of the progress loop lasts at least 334ms, our floor; a loop that flashes more than three times a second falls under WCAG 2.3.1, which sets no duration.

## Beyond the gate

- A loop that runs more than 5 seconds next to other content needs a way to pause, stop or hide it (WCAG 2.2.2).
- A pulse or attention loop is a finding unless it is the progress loop; a notice that must be seen is a banner, not a pulse.
- Under reduced motion a state change must still be perceivable, through a quick fade or an immediate change; removing the change entirely is a finding.
- Motion that ignores prefers-reduced-motion, or a component that hardcodes a duration instead of a role, is a finding.
- A move that goes the wrong way under right to left is a finding naming the component.

## Handoff notes

- Each role is three custom properties: duration, curve (a cubic-bezier) and, for roles that travel, distance.
- Horizontal travel: translateX(calc(var(--motion-reveal-distance) * var(--motion-inline-sign))). Vertical travel does not use the sign.
- Reduced motion needs no extra code in components: the same properties switch under prefers-reduced-motion or data-motion="reduced".
- Transition only transform and opacity where possible; they do not reflow the page.
- The progress loop uses animation-timing-function from its curve and runs infinitely; give it a pause control when it can run long.

## Common mistakes

- Using reveal for something that toggles in place: it slides from nowhere; use swap or press.
- Staging a dismiss so it lingers: the next action waits.
- Easing the progress loop: the pace wobbles and misreports work.
- Signing a distance by hand for right to left: the sign token already does it.
- Animating width, height or margins for a small change: the whole page reflows.
