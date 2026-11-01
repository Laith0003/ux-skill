# Product illustration

A product illustration is a picture of the product's interface made for a page: a window, a dashboard, a phone screen or a short cursor demo, sitting in a hero beside the copy, in a feature card, in a bento tile or at the top of a docs page. It is imagery, not the product: a believable screen, cut down to what the viewer needs, in which at most one thing happens.

`/ux-design` loads this file whenever a build shows the product's interface as imagery: the interface-fragment heroes and collages in `references/surfaces/landing.md`, a feature card, a bento tile, a cursor demo. It is not a surface playbook; it loads beside the one the mode picks, the way the component contracts do. In dashboard mode the interface is the page itself, not a picture of it, so this file does not apply there and the dashboard playbook's real content rule holds.

The rules here are distilled from Stageshow (github.com/benjitaylor/skills, MIT; see NOTICE), whose kit builds these illustrations in React.

## Where it sits on a page

- **Photographs stay.** A product illustration is extra imagery. It never stands in for the photographs the page carries (`references/surfaces/landing.md`, the photo rule); a hero can show the product, and the page around it still shows people, places and things.
- **It wears the page's system.** The illustration's surfaces, text, accent, status colors, faces and radii are the system's, so the picture and the page read as one product. With the Stageshow kit, `uxskill system export --to stageshow` writes the look; built by hand, it uses the system's role variables like the rest of the page.
- **It is designed at the size it is shown.** About 720 by 340 for a hero beside copy, 900 to 1100 wide for a full-width hero, about 400 by 300 for a card, shown at 1:1 (the close-up excepted, below). An animated demo stays at least about 320 wide; only a small tile or a detail card goes below that.
- **The phone gets its own design.** In the phone column the illustration is recomposed, cropped closer with the action and the result whole, never the desktop picture squeezed. It fits the column at every phone width the build is checked at: 358 wide in a 390 viewport, 328 in a 360 one, so it scales with the column rather than holding a fixed width.
- **It is not a heading or a second page.** A faux window's title is a `div`, never `h1` to `h6`, because the illustration sits inside a real page's outline. The page's own copy carries the meaning; mark the illustration `aria-hidden="true"`, or give it `role="img"` and a short label when it says something the copy does not. Either way it holds nothing focusable: its buttons and fields are drawn with plain elements, or the whole illustration is `inert`, so a keyboard never lands on a control no one can see or use.

## The test it must pass

A viewer should take it for the real product, see only what the story needs, feel the crop was chosen, and never catch anything moving without a reason. It goes wrong in five ways:

- **Overfilled.** Copy on every line, figures on every surface, no pane left quiet. Detail past the story is what makes a screen look machine made.
- **Skeletal.** A few gray blocks and a button, too small or too stripped to recognize as any product.
- **Shrunk into a box.** The entire app reduced to fit a card, with the same margin on all four sides, so it reads as a captured screen on display rather than a composed shot.
- **Flat.** All parts equally heavy, each in an identical outlined box, so nothing invites the first look.
- **Generic.** The same neutral window and pointer no matter what was asked. When the brief names a character (a blueprint look, glass over color, a playful mascot), delivering it is the job.

## Plan before drawing

Write five lines first: where it sits and its size; the one focal object; the action, if it moves; the result that stays on screen; what is left out. These lines settle more of the outcome than any later polish.

## The still frame

- **Ration the words, not the parts.** Real copy goes on the window's name, the item being worked on, any typed input and the outcome, usually three to seven pieces in all; everything else is a placeholder bar in the product's quiet gray. A calendar still needs a full week and a search still needs results; only their words become bars.
- **Words where the eye lands, bars at the edges.** Placeholder bars vary in width row to row (for example 60, 45, 70 and 52 percent of the track) and sit in the same line box as the text they stand for.
- **One number is big.** The other figures are ordinary lines.
- **Say each fact once.** The feature's signal appears in one place, not in the header, a satellite and every row.
- **Keep what makes the product recognizable:** its real window chrome, its own icons, the content it is known for (album art, avatars, thumbnails). Cut repeated framing before cutting character.
- **No invented logo.** An initial on a tinted tile is not branding; show the product's actual mark, or set its name in plain type. Never signal an AI feature with sparkles, a wand or a purple tint; show the work it does instead.
- **Icons come from one set,** at one size and one stroke width, never drawn by hand. Emoji are content, not icons.
- **UI text is 11 to 15px before the illustration is scaled,** never smaller, with a line height of at least 1.3 on small text.
- **Words keep 12px from the edge** of their window, card or row; a button keeps at least 8px from the field or line above it. Two edges that almost meet, within 3px, look like a slip, so either line them up or open a gap of 8px or more.
- **One neutral family and one accent,** spent on the thing being acted on. Status colors appear only where status is the subject. On a dark theme, depth comes from a lighter surface, not a shadow.

## Framing

- **One hero object,** with at most one or two satellites of different kinds (a phone, a receipt, a notification at its real size), each straddling the hero's edge about half outside, over chrome or margin and never over content.
- **The main window spans two thirds of the stage or more and runs past at least one edge, with a tenth to two fifths of it out of frame; in satellite focus the window is only context and the satellite carries the story.** Only filler is cut: every real word, the action and the result stay whole. A control the crop would slice is moved or removed, never sliced.
- **One gutter.** Measure how far the main window sits from the stage's edge and reuse that distance for every other margin in the frame. Each edge either keeps that full margin or clearly crosses it; a gap under 24px reads as a near miss.
- **No plate behind it.** On a white or dark page the illustration sits straight on the page, with no tinted panel underneath; a complete window centered with space all round looks adrift.
- **Proportions are kept.** A complete window is at least 1.25 times as wide as it is tall; a cut one still shows at least a square. When it does not fit, change the crop or the layout rather than distorting it.
- **Every corner of the frame has something to do,** in the still and through every moment of an animation.

| Layout | The hero | Use it for |
|---|---|---|
| Corner bleed | Inset about 10% from the top and left, 15 to 35% past the right and bottom | A hero beside copy |
| Bottom bleed | Inset 8 to 12% on three sides, 15 to 35% past the bottom | A feature card or bento tile |
| Satellite focus | The window mostly cropped away, with a big secondary card, 30 to 40% of the window's width, telling the story | A single small moment, such as an alert or a payment slip |
| Wide hero | A 900 to 1100px window at 1:1, off the bottom and often both sides | A full-width homepage hero |
| Device pair | A desktop window about 75 to 80% wide, a phone straddling its right edge | A story across devices |
| Close-up | The whole window, designed at 1:1 and enlarged 1.3 to 1.6 times with its chrome, off the bottom; the type and spacing rules apply before the enlargement | A card about one control |
| Fade crop | A window fading out over its last third, over filler only, with a mask | When a hard edge would cut at an arbitrary line |

## When it moves

- **A single event:** a few steps, three at least and five at most, that end in an outcome, the whole cycle lasting 10 to 16 seconds. When more story would crowd the frame, cut the story.
- **Every movement has a cause.** No cursor move without a reason; data never rewinds in view without one.
- **Content moves rather than swaps.** An added row slides the ones beneath it down, and a panel that grows or shrinks keeps its type at its own size.
- **A loop returns to its opening state,** or something on screen explains why it starts over.
- **It can be stopped.** A demo that plays by itself for more than 5 seconds beside the page's copy gets a pause control, as `references/foundations/motion.md` sets for anything that moves that long (2.2.2); one that plays once in view and settles within 5 seconds, or plays only on hover, needs none.
- **Choose the poster frame first.** Most people see one frame: a thumbnail, a screenshot, or the still that reduced motion shows. It is the beat that tells the story alone, with the result on screen, never a frame caught mid-change. Under `prefers-reduced-motion` the illustration shows that frame and does not play.

## Check it

- **Look at it at the size it is shown and at 390 and 360 wide,** beside a strong reference shot at the same size. If yours is emptier, flatter or more boxed, fix the framing first, then the hierarchy, then the motion, then the polish.
- **Notice where you look first.** That should be the outcome, and a single window, tile or device should plainly dominate.
- **Screenshot every look the page uses.** Checking light tells you nothing about dark.

## With Stageshow

Stageshow's kit draws the windows, phones, cursors and motion these rules describe, with examples that set the bar. Install it with `npx skills add benjitaylor/skills --skill stageshow`, then give it the system's look:

```bash
uxskill --no-pretty system export --from design-system/tokens.json --to stageshow --out design-system/export
```

Load `stageshow-look.css` after the kit's stylesheet, with the system's `fonts.css`, and give each stage the class: `<Stage className="ux-look">`; `theme="dark"` on a stage takes the system's dark values. The kit keeps its own shadows, control heights and placeholder inks, which are tuned to an illustration's scale. Its app icons and other companies' logos stay under their owners' terms: fine in a mockup of how something works, never shipped as the product's own assets.
