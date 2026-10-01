---
id: states-answer-on-motion
title: Every state a component changes under answers on the system's motion roles
status: active
areas: [motion, contracts]
supersedes: null
superseded_by: null
---

# Every state a component changes under answers on the system's motion roles

## Context

Contracts bound the colors and edges a part takes under hover, selected and pressed, but most bound no transition, so the change snapped on one page and drifted on a browser default curve on the next. A pressed control had no scale to take, and menus that open on motion.reveal had no exit.

## Decision

The schema refuses a contract in which a part changes under hover, selected or pressed and binds no transition-duration and transition-curve, with no state or under that state; the error names the part, the state and the binding to add. The seeds bind those parts to motion.state. button, chip, selectable-row and an interactive card bind a new press-scale property to motion.press.scale under pressed, and the binding check holds it to 0.95 to 1, exactly 1 under reduced motion. select and nav bind their menus' exit to motion.dismiss, and keep the exit running until it ends before the panel is hidden.

## Why

A state change is a response to a person, and the system already decides how a response moves (motion.state, motion.press). Binding it in the contract means every page built from the contract moves the same way and follows the reduced motion mode the system builds.

## What it touches

engine/contracts/schema.py (MOVING_STATES, press-scale, the no-transition check); engine/contracts/bind.py (PRESS_SCALE, the press check); the seed contracts; tests/contracts/test_state_motion.py.

## Consequences

An existing project contract that changes a part under hover with no transition is refused until it binds one. chip gains a pressed state and card an interaction variant, so their variant and state counts grow.
