# From a ux-skill contract to a Figma component

A contract is YAML in one schema. This is how each field becomes part of a Figma component.

| Contract field | In Figma |
|---|---|
| `parts` | Layers inside the component, named as the parts. `rtlBehavior: logical` uses auto layout that follows the text direction; `mirror` flips for right to left; `fixed` never flips. |
| `variants` | Variant properties, each with the values the contract lists and its default. |
| `states` | One more variant property, State, with the states listed. |
| `tokens` | Variable bindings: `fill` binds the layer's fill, `text` the text fill, `border-color` and `border-width` the stroke, `radius` the corner radius, `padding-inline`, `padding-block` and `gap` the auto layout spacing, `font` the text style's fields, `shadow` an effect style. A binding with `when` applies to those variant values only; one with `state` applies in that state only. |
| `press-scale`, `transition-*` | Prototype interactions: a pressed state scales by `motion.press.scale` and every state change animates with the duration and curve the contract binds. |
| `contrast` | Pairings the engine already measured on the built tokens; keep the bindings and they hold. |
| `surfaces` | The fills the component may sit on; show it on each in the review frame. |
| `a11y` | The minimum target (`layout.target.min`) is the component's minimum height and width; the cue is the second signal besides color, shown in every state that carries meaning. |
| `copy` | Rules for the words in each state; write sample text that follows them. |
| `usage` | The do and do not rules; follow them when composing a page. |

A section contract adds `job` (what it must prove), `slots` (the components or media each slot takes), `proof` (the real proof it needs, or it is left out with its reason) and `phone` (how it recomposes on a phone, in order). Build a section as a frame of instances of the components its slots take.
