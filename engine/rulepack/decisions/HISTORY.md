# Decision history

A router, not a story. Each line opens one record; the record says what was decided and why. Read it before changing what it decides.

## Token structure

- [Tokens have two layers, primitives and semantic roles](two-layers.md)
- [Mode axes switch on the root element only](axes-on-the-root.md)
- [Breakpoints are reference values, and type does not change by breakpoint](breakpoints-are-reference-values.md)
- [Density has two modes, comfortable and compact](two-density-modes.md)

## Roles per foundation

- [Color keeps one role per job, and interaction states belong to their fill](color-roles.md)
- [Spacing roles name a relationship, and there are eight of them](space-roles.md)
- [Six radius roles follow structure, and geometry sets the scale](radius-roles.md)
- [Border roles are widths for four jobs plus the focus ring](border-roles.md)
- [Elevation is four shadows and a stacking order; surfaces are color](elevation-roles.md)
- [Motion has seven interaction roles and reduced motion is a mode](motion-roles.md)
- [Layout tokens cover the page grid; regions and panes belong to page patterns](layout-scope.md)
- [Nine text styles as composites, faces chosen per script](type-roles.md)

## Contrast and the gate

- [High contrast raises non-text parts to our own 4.5:1 floor](high-contrast-non-text-floor.md)
- [The gate blocks on the AAA criteria it applies](aaa-criteria-that-block.md)
- [Every text style is held to the body text minimum](no-large-text-relaxation.md)
- [The focus ring clears the surfaces, and an offset keeps it off the fill](ring-offset.md)
- [A filled control's fill clears 3:1 against the page only](fill-edge-page-only.md)
- [A focus ring on a tinted fill keeps 3:1 in high contrast](ring-on-tinted-fills.md)
- [Disabled colors stay distinct and visible, not readable at 4.5:1](disabled-contrast.md)
- [Status colors keep their own hues, whatever the brand hue](status-hues.md)
- [In dark mode, surfaces lighten as they rise](dark-elevation-cue.md)

## Shape, space and motion

- [Border widths are whole pixels](whole-pixel-borders.md)
- [A dialog is never less rounded than a card, and inner corners follow the padding](nested-radius.md)
- [Stacked rows use the list gap, controls in a row use the control gap](list-gap-and-control-gap.md)
- [Travel distances are unsigned, and one sign follows the reading direction](unsigned-distances.md)
- [Emphasis inside text uses the heading weight](strong-equals-heading-weight.md)
- [Reading styles have a line height of 1.5 or more by default](reading-line-height.md)

## Components

- [A container whose fill measures below 1.2:1 against its surface draws an edge](container-edge.md)
- [Buttons have two intents, neutral and danger](button-intents.md)
