# Imagery

## Summary

Imagery sets how photos and illustrations sit in the system: the aspect ratios media is cropped to, a scrim that keeps text over any image readable, a brand tint and a duotone pair that bring photos into the brand's light, and, with the radius foundation, the corner of media. Generated brand art (art/ beside tokens.json) fills a page that has no photos yet. Every value follows the axes and the brand color. Imagery does not choose photos; it says how to crop, treat and place them.

## Principles

- **Media serves the task.** An image earns its place by showing the product, the people who use it or the result; a decorative image is marked decorative and never carries a message alone.
- **Crop to a ratio, not to the photo.** Media takes the system's ratios so a grid of images reads as one set.
- **Text over an image always has a scrim.** The scrim is measured against the worst image for its text, the brightest under light text and the darkest under dark text, so no photo can take the text below its minimum.
- **Generated art takes a veil, not the scrim.** The build knows every color its art draws, so text over the art sits on color.media.veil, a veil of the page's own color measured over those colors, in color.text.on-media: light art needs little veil and keeps its colors, where the photo scrim would turn it grey (decisions/media-veil.md).
- **Treat photos as a set.** A tint or a duotone pulls photos from different sources into the brand's light; use one treatment per page.
- **Art fills, it does not explain.** Generated art is decoration: it sets the mood where a photo is missing and says nothing a screen reader needs.
- **Art is composed, not scattered.** The hero art has one focal shape in the brand color, a quiet neutral plane behind it and small support accents in front, open space on the heading's side, and area in proportion, about 60, 30 and 10 percent (decisions/art-composition.md).

## Roles

- `imagery.ratio.hero`: the aspect ratio of a hero image or a full-width band of media, as width over height.
- `imagery.ratio.card`: the aspect ratio of the image at the top of a card or in a grid.
- `imagery.ratio.portrait`: the aspect ratio of a person's photo or an upright product shot.
- `imagery.scrim`: the translucent layer between an image and the text on it; stronger under high contrast.
- `imagery.on-scrim`: the text and icons on the scrim.
- `imagery.duotone.shadow`: the dark end of a duotone treatment, deep in the brand's hue.
- `imagery.duotone.highlight`: the light end of a duotone treatment, pulled warm or cool with the warmth axis.
- `imagery.tint`: a translucent brand wash laid over a photo, stronger in a warm system.

## Choosing

| Media | Ratio | Treatment |
|---|---|---|
| A hero photo with the headline on it | imagery.ratio.hero | imagery.scrim under the text, imagery.on-scrim for the text |
| A hero over the generated art with the headline on it | the art full bleed | color.media.veil over the art, color.text.on-media for the text |
| A secondary or ghost button on media | color.text.on-media for its label, edge and ring over art, imagery.on-scrim over a photo | color.text.link, measured against surfaces only |
| A hero photo beside the headline | imagery.ratio.hero | none, or the page's one treatment |
| Images in a card grid | imagery.ratio.card | the page's one treatment, the same on every card |
| A person, a team member, an upright product | imagery.ratio.portrait | none |
| A hero with no photo yet | art/shapes.svg, the heading on its open side | decorative, with an empty alt; mirrored under right to left |
| A section, a card or an empty state with no photo | art/pattern.svg as a repeating background, or art/gradient.svg | decorative |
| Photos from mixed sources on one page | their ratio | imagery.duotone or imagery.tint on all of them |

Art direction, in our words: crop to the subject's eyes or the product's working face and keep it off the center line in a split layout; choose light that matches the scheme (bright, high key light for a light page, low key light for a dark one); prefer real use over staged smiles; show hands and faces from the audience the brief names; and keep the horizon and verticals level so the grid stays calm.

## Modes

Imagery varies on contrast: under high contrast the scrim is stronger, so white text reaches 7:1 over a white image. Ratios, the duotone pair and the tint are the same in every mode. Images do not change with the scheme; a page that shows the same photo in light and dark lets the photo keep its own light.

## Changing the system

1. Imagery moves with the axes and the brand color: the hero ratio with the contrast, density and formality axes, the card ratio with the geometry and formality axes, the duotone highlight and the tint with the warmth axis, and the scrim, the duotone shadow and the tint with the brand hue. The highlight moves toward the warm or cool hue through grey, never around the wheel (decisions/neutrals-lean-along-the-brand.md), and the scrim and the duotone take chroma from the brand in proportion, so a grey brand gets a grey scrim and, at the middle warmth, a grey highlight (decisions/grey-brands-steer-no-hue.md). Change them in --axes or the brief and build again with `uxskill system build`, adding --force to replace the files in the same folder and --rule-pack to refresh this pack, then read the system report it writes beside tokens.json.
2. The build keeps the text on the scrim at 4.5:1 over the worst image for it (7:1 under high contrast), every ratio between 1:5 and 5:1, and the duotone pair 7:1 apart, our floor; a failed check names the role.
3. Never edit a generated value in tokens.json or tokens.css: the build has not checked it, and the next build replaces it.
4. Repointing one role, exempting a role from a check or adding a role comes with the 4.1 importers and the extend mode. Until then, record the need for the system owner.

## Audit scope

Audits how media is cropped, treated and captioned: ratios, the scrim under any text on an image, one treatment per page, alt text, and generated art marked decorative. It does not audit the choice of photos beyond the art direction above.

## Checks

- `scrim-text`: the text on the scrim reaches 4.5:1 over both a white and a black image, 7:1 under high contrast (WCAG 1.4.3 and 1.4.6); a white image is the worst under light text and a black one under dark text, and the finding names the image that failed.
- `media-ratios`: every ratio lies between 1:5 and 5:1.
- `duotone-range`: the duotone shadow and highlight are at least 7:1 apart, our floor, so a treated photo keeps its detail.

## Beyond the gate

- Every image that carries meaning has alt text that says what it shows in the context of the page; a decorative image, generated art included, has an empty alt and aria-hidden on its wrapper.
- Text never sits on an image without the scrim, however dark the photo looks: the next photo may be white.
- A carousel or background video that moves for more than five seconds has a pause control (WCAG 2.2.2).
- An image never holds the only copy of a price, a date or a call to action.

## Handoff notes

- Set aspect-ratio from the imagery.ratio roles and object-fit: cover on the image, and round it with radius.media.
- Lay the scrim as a layer between the image and the text, with background from imagery.scrim; set the text in imagery.on-scrim.
- Over the generated art, lay color.media.veil the same way and set the text, and the label, edge and focus ring of any control there, in color.text.on-media.
- A duotone is a filter: map the image's shadows to imagery.duotone.shadow and its highlights to imagery.duotone.highlight, for example with an SVG feComponentTransfer or a mix-blend-mode pair.
- The tint is a layer over the photo with background from imagery.tint and mix-blend-mode: multiply in light, screen in dark.
- The generated art in art/ is SVG with its own palette from the build; place it with an empty alt.

## Common mistakes

- Text on a photo with no scrim because the photo is dark: the next photo is not.
- Cropping each image to its own shape: a grid of mixed ratios reads as clutter.
- Mixing a duotone and a tint on one page: pick one treatment.
- Describing generated art in alt text: it is decoration, so the alt is empty.
