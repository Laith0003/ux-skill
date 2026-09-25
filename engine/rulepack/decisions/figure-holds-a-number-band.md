---
id: figure-holds-a-number-band
title: The figure style reads at the page title's size, so it holds a number band
status: active
areas: [type]
supersedes: null
superseded_by: null
---

# The figure style reads at the page title's size, so it holds a number band

## Context

On real landing pages the figure style came out at 27 to 29px, the size of a card title, so a band of three or four proof numbers read as a row of labels and the pages set their numbers by hand.

## Decision

type.text.figure takes heading-1's step (typography.ROLES), in the display face at the display weight with the tightest display leading, so at a mid contrast it is about 40px at 1440 and it follows the scale ratio like every other step. It stays outside the size order of hero, headings and body, since a figure is a number, not a level.

## Why

A proof band is a section whose content is its numbers; at the page title's size three or four of them fill a row at desktop and still step with the system. A step on the scale moves with the contrast and density axes, so a bold system gets larger figures and a dense one smaller.

## What it touches

typography.ROLES; guidance/type.md.

## Consequences

A dashboard's key figure is as large as a page title; a smaller number in a card takes heading-2 with tabular figures instead.
