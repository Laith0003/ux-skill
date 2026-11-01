---
id: button-intents
title: Buttons have two intents, neutral and danger
status: active
areas: [contracts, color]
supersedes: null
superseded_by: null
---

# Buttons have two intents, neutral and danger

## Context

A button set can offer an intent for every status: positive, warning and info buttons beside neutral and danger ones, each in filled, outlined and text-only emphasis.

## Decision

The button contract has two intents, neutral and danger, in three emphases: primary (filled), secondary (an edge and brand text in every enabled state) and ghost (text only at rest, taking the secondary fill and edge on hover and press). Positive and warning outcomes are shown in a status banner or next to the result, never as the color of a button. Secondary and ghost buttons use the link text, the selected line and the selected surface; the danger versions use the danger status roles. Disabled, every emphasis takes color.text.disabled for its label, and the secondary button takes it for its edge as well.

## Why

A button's color says what pressing it does. Only destruction changes what a person must think about before pressing, so only danger earns its own color. A green or amber button reads as an outcome that has not happened yet.

## What it touches

The button contract and color-roles; the status-banner contract.

## Consequences

A confirm-and-continue action is a neutral primary button. A warning before an action sits in a banner above it, and the button says what will happen.
