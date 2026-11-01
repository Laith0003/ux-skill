---
id: form-contracts-per-control
title: Each form control states its own label, hover, error and target, and a check box stays a box
status: active
areas: [contracts, radius, border]
supersedes: form-contracts
superseded_by: null
---

# Each form control states its own label, hover, error and target, and a check box stays a box

## Context

The first record for the six form contracts said they all followed the text field: a ui-large label, a heavier edge on hover, an error icon, a reserved message line and 44px targets. Four of the six did not. The contracts also bound the check box to the chip corner, which is a pill in soft brands, and sized the box and the radio dot to the 44px target, so a soft build drew a round 44px check box that read as a radio button. The textarea took the control corner, a stadium at the soft end that clips its first and last lines. The field with a prefix drew three boxes with a double seam, and its phone prefix trailed the number under right to left. The date's arrows and calendar button and the open list's options had no focus binding, and the checked box's edge fell below 3:1 on cards and raised layers.

## Decision

Each control states what it binds; the table below is what the contracts bind and a test reads it against them.

| Control | Label | Hover | Error icon | Message line reserved | Target |
|---|---|---|---|---|---|
| checkbox | `type.text.body` | fill | no | no | target |
| radio | `type.text.ui-large` | fill | no | no | target |
| select | `type.text.ui-large` | field edge, option fill and edge | yes | yes | option, trigger |
| textarea | `type.text.ui-large` | edge | yes | yes | input |
| date | `type.text.ui-large` | field edge, day fill and edge | no | yes | button, day, input, next, previous |
| input-prefix | `type.text.ui-large` | edge | no | yes | group |

The radio's label column is its legend; each option's label is type.text.body, as the check box's is. The check box's box takes radius.box and the textarea radius.area, neither of which becomes a pill. The box and the dot are drawn at type.icon.size.control, and a target part wraps the glyph and its label and meets layout.target.min. The field with a prefix is one shape: the group holds the only edge, the fill and radius.control and clips its parts, and the prefix or suffix draws a divider where it meets the value, so every state changes one edge. A prefix leads a fixed left to right run in both directions (+962 791234567); a suffix follows the amount in the page's direction. Every part a person operates binds a focus ring, the active option under the keyboard takes the hover fill, edge and ring, and the select says what is loading and when nothing matches. The checked box's edge is color.line.selected, paired at 3:1 with every surface the box sits on. The target is 44px in comfortable density and 32px in compact (layout.md).

## Why

A record an agent reads has to match what the contracts bind, or the agent follows the record. A corner tells a check box from a radio button only while it stays square; a stadium is a shape for one line. A doubled seam and a red outer edge against grey inner edges read as three controls. WCAG 1.4.11 asks 3:1 for the boundary a person needs to identify a checked box, wherever the box sits, and 2.4.7 asks for visible focus on every control.

## What it touches

engine/contracts/seed/checkbox.yaml, radio.yaml, select.yaml, textarea.yaml, date.yaml, input-prefix.yaml and text-field.yaml (a multi-line field takes radius.area); engine/foundations/radius.py (radius.box, radius.area); guidance/radius.md and border.md; tests/contracts/test_contract_findings.py.

## Consequences

A disabled option and a day out of range are drawn in color.text.disabled with aria-disabled and stay reachable by the arrow keys; today carries an outline and aria-current. These are usage lines, since the state list is per component. Every contract still ships at experimental with a null provenance.
