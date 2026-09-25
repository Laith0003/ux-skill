---
id: brand-roles
title: The axes choose whether the brand fills the action, marks words or draws edges
status: superseded
areas: [color]
supersedes: null
superseded_by: brand-leads-the-role
---

# The axes choose whether the brand fills the action, marks words or draws edges

## Context

One brand treatment for every system, the brand as the main button's fill, makes a formal payments product and a playful restaurant look alike, whatever the brief says.

## Decision

The brand has one of three roles. fill: the brand fills the main action and colors links. accent: the main action is ink, a neutral from the far end of its ramp, and the brand colors links, accents and the selected state. edge: actions and links are ink, and the brand draws edges, rules, underlines, the selected state and the focus ring. character.brand_role_scores weighs the axes (fill: contrast, low formality and warmth; accent: formality, low contrast and type personality; edge: formality, coolness and sharp geometry) and the highest score wins, fill on a tie. A brief may name the role instead. Every role, whichever wins, is generated and measured in every context.

## Why

A formal, quiet brand reads as confident with ink buttons and a brand accent; a bold, warm one wants its color on the action. The choice is a function of the axes, not of an industry, so any two briefs that differ in character can differ here, and the roles stay the same set so contracts bind the same names.

## What it touches

color.INK, INK_HIGH, EDGE_LINK, EDGE_LINK_HIGH and BRAND_ROLES; character.brand_role and brand_role_scores; generate_color's brand_role; the brief's brand_role field.

## Consequences

With an ink action the primary button does not carry the brand; the report says which role was chosen and why. Contracts keep binding color.action.primary and color.text.link, whatever the role.
