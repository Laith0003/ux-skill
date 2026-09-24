---
id: status-hues
title: Status colors keep their own hues, whatever the brand hue
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Status colors keep their own hues, whatever the brand hue

## Context

A brand color can sit near a status hue: a red brand near danger, a green one near success. Shifting the status hue away from the brand is one answer; keeping both is another.

## Decision

The four status families are generated at fixed hues (danger red, warning amber, success green, info blue) with fixed lightness and chroma seeds, independent of the brand. A brand that shares a status hue keeps its hue, and the status keeps its own.

## Why

Moving danger away from a red brand makes danger read as orange, which is worse than sitting close to the brand. Status never relies on hue alone: every status carries an icon and words, and the contracts refuse a status color without a second cue. A near collision is a design judgment for the owner, not a contrast floor.

## What it touches

color.STATUS_HUES and STATUS_SEED; the a11y cue rule in the contract schema; the status-banner contract.

## Consequences

A brand close to a status hue should not use its brand fill for anything that could read as that status. The owner decides; the generator does not move either color.
