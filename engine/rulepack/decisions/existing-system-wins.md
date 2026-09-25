---
id: existing-system-wins
title: A project's existing design system wins over the guidance's generic label and accent rules
status: active
areas: [color, type]
supersedes: null
superseded_by: null
---

# A project's existing design system wins over the guidance's generic label and accent rules

## Context

The guidance describes type.text.label as spaced open and color.text.accent as the brand color on an eyebrow. Those are defaults for a system the engine builds. A project that already has its own design system sets these itself: a client may set its labels at zero tracking and in sentence case, or color its eyebrows in a neutral. Read as binding, the defaults tell an agent to restyle the client's labels, which overrides a deliberate identity with a generic rule.

## Decision

When the project has an existing design system (what `ux system detect` finds: a token file, foundation CSS, a hand-written MASTER.md or DESIGN.md), its own label style and label color win over type.text.label and color.text.accent, on tracking, case and color; a mark beside a label still needs the recorded waiver (decisions/eyebrow-is-text.md). guidance/type.md and guidance/color.md say so on those two roles. The same clause stands in references/styles/anti-slop.md (principle 9 and the eyebrow rows).

## Why

The anti-slop defaults guard against a model's reflexes, not against a client's choices. An existing system is fixed input: a page built on it keeps its labels as the system sets them, and the guidance must not read as a reason to change them.

## What it touches

guidance/type.md (type.text.label); guidance/color.md (color.text.accent); references/styles/anti-slop.md; commands/ux-design.md step 1a.

## Consequences

On a project with its own system, an agent keeps the client's label tracking, case and color. A system the engine builds keeps the guidance's defaults, since no existing system is in play there.
