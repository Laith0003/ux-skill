---
id: two-density-modes
title: Density has two modes, comfortable and compact
status: active
areas: [space, layout]
supersedes: null
superseded_by: null
---

# Density has two modes, comfortable and compact

## Context

Systems often offer three densities, with a spacious mode above the default. Every mode multiplies the values each role must hold and the contexts every check must walk.

## Decision

Density is one axis with two values. Comfortable is the base; the density axis of the brief places it between airy and dense. Compact takes each role one step lower on the scale, never below the role's floor and never larger than comfortable. There is no third, spacious mode.

## Why

A brief that wants more room says so through the density axis, which moves the comfortable values; a third mode would duplicate that. Two values keep every axis binary, which keeps the CSS switch and the override rules exact.

## What it touches

modes.AXES; space.py compact_step and floors; layout gutters, margins and the target size; the compact-not-larger check.

## Consequences

A marketing page that wants more space builds with a lower density axis value, not a spacious mode. Compact never removes the 8px control gap or the 24px minimum target.
