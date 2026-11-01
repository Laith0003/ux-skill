---
id: figma-modes-on-one-axis
title: A Figma collection of three or more modes that name no engine axis is read whole on one axis named for it
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# A Figma collection of three or more modes that name no engine axis is read whole on one axis named for it

## Context

A Figma collection often holds several brands or themes as modes (Harbor, Meadow and Ember). Their names place into none of the engine's axes, and a mode axis of the engine holds two values, so the importer read the default mode and left the other modes' values in a note. A system read that way loses every value its file holds outside the default mode, and an extension written back to the file cannot give its own modes their values.

## Decision

A collection of more than two modes that place into no axis of the engine's is read whole on one axis named for the collection (Brand Theme gives brand-theme). The default mode is the base and every other mode is a value of the axis, the way the CSS importer holds an attribute that takes several values: the axis's values are base and each other mode's name as a slug. The report notes the axis and each mode's context. When the names cannot make the axis, the default mode is read and the note names the rename: the collection is named for one of the engine's own axes, a mode's name does not start with a letter or repeats another, a mode would take the name base, or another collection names the same axis with other modes. second_modes still reads one mode beside the default instead.

## Why

An importer reads a value or says how to write it; a note that holds the values of whole modes does neither. The collection is the file's own name for what its modes switch, so it names the axis without a guess, and the default mode is what Figma shows when nothing is chosen.

## What it touches

engine/io/figma_in.py (_every_mode, _plan); commands/ux-system.md; tests/io/test_figma_in.py.

## Consequences

The axis is not mapped to an engine axis by name: like any axis whose base is the root, the owner maps it by hand in mapping.json. An extension into the file places a token that varies on it in that collection, one value per mode.
