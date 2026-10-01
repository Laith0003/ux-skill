---
name: ux-skill-foundations
description: "Build a brand's design system with ux-skill and bring it into Figma as variables and components that match the code. Use when the user wants Figma variables, modes or components from a brand color, a brief or an existing token file, or wants a Figma library checked against the tokens a site ships. Load figma-use alongside it for every use_figma call."
disable-model-invocation: false
---

# ux-skill foundations in Figma

ux-skill builds a design system from a brand color and a brief (or reads one a team already has) and checks it before handing it over: every pairing is measured for contrast in light, dark and high contrast, and the build refuses to write a system that fails. This skill brings that system into a Figma file as variables with their modes, and builds components from ux-skill's contracts with every visual property bound to a variable. The code and the file then hold one system.

**Prerequisites.** The `figma-use` skill MUST be loaded for every `use_figma` call. ux-skill runs locally (`pip install uxskill`, Python 3.10 or newer); it never calls a model and needs no network.

## 1. Get the system

Pick one source, in this order:

1. **The team's own tokens.** A DTCG tokens.json, a CSS file of custom properties, a Tailwind 4 theme, Markdown rule files or a Figma variables export. Read it as it is, never rebuilt: `uxskill system import --from <file>` reports what it read and lists every entry it did not read with how to write it. An existing system is fixed input; extend it beside its source with `uxskill system extend`, never rewrite it.
2. **A brand color and a brief.** `uxskill system build --brand '#3366FF' --brief .ux/system-brief.json --out design-system`. The look follows the brand and the brief's axes as continuous values, never a preset by industry. Read `design-system/system-report.md` before going on: it says what was built and what the engine moved to pass contrast.

Stop and tell the user when the build reports a failure: nothing was written, and the message names the token and the change to make.

## 2. Variables

Export the variables and the script that applies them: `uxskill system export --from design-system/tokens.json --to figma --out figma-export`.

- `figma-variables.json` holds one collection per foundation (color, type, space, layout, radius, border, elevation, motion, imagery), each with the modes it changes in: light and dark, standard and high contrast, comfortable and compact, left to right and right to left, full and reduced motion.
- `figma-variables.js` creates or updates them in the open file. Run its text through `use_figma`. It matches by name, so a second run updates in place; it never deletes a variable or renames a mode it did not make.
- Primitives are hidden and unscoped; roles alias them and carry the scope that binds them (fills, text, strokes, gaps, radii) and their web code syntax (`var(--color-action-primary)`).
- What Figma variables cannot hold is listed in the export's notes, for example a font family keeps its first face and the fallbacks stay in tokens.json.

To read the file back, run `figma-read-variables.js` through `use_figma`, save its result as JSON, and pass it to `uxskill system import --from <file> --format figma`. A round trip gives the same names and values.

## 3. Components from contracts

ux-skill ships component contracts (`engine/contracts/seed/*.yaml`) and section contracts (`engine/contracts/seed/sections/*.yaml`). A contract names a component's parts, its variants (each value listed), its states, and the semantic role every part binds per variant and state. Build each one in Figma as the contract says; see [references/contracts.md](references/contracts.md) for the mapping.

- Bind every fill, stroke, text color, padding, gap and radius to the role's variable. Never type a hex or a number the contract does not name.
- A state is a variant property value (Default, Hover, Pressed, Focus, Selected, Disabled), and a part that changes under hover, selected or pressed carries the transition the contract binds (motion.state, or motion.press for a press) in its prototype interaction.
- The focus ring is the system's (color.focus.ring, border.focus-ring.width and offset), drawn outside the part.
- Run `uxskill contracts check` after the build to confirm every binding and pairing against the tokens.

## 4. Pages built from sections

A page is a sequence of section contracts: a hero, proof, the argument, a closing band and the footer. Each section names its job, the components its slots take, its variants and its phone recomposition. Every page carries photographs sourced by the system's photo direction (the report's photo direction section); an interface fragment is extra imagery beside a photograph, never in its place.

## 5. Check

- Variables: the collection and mode counts match the export, and every role aliases a primitive.
- Components: every visual property is bound; the variant count equals the product of the contract's variant values; each state shows as an instance in one review frame.
- Contrast holds: the system was measured before it was written, and binding to its roles keeps it.

## Definition of done

The file's variables match the export, the requested components are built from their contracts with every property bound, a screenshot of the review frame shows every requested state clearly, and nothing was hardcoded that the system names.
