---
id: wider-vocabulary
title: Common tone words carry axis weights, and four more industries seed the axes
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# Common tone words carry axis weights, and four more industries seed the axes

## Context

Real client briefs used words the engine did not read: fast, clear, practical, solid, modern, reliable, simple. The host AI then swapped a word for one the engine knew, and a plain construction brief read "practical" as "professional" and got a formal serif. Four industries a client named had no seed: construction and building materials, a B2B marketplace or wholesale, security, and pharmacy or medical supply.

## Decision

engine/synthesizer/axes.py gives thirty more tone words a weight on the seven axes, each by what the word says: fast and quick read as short and snappy (motion a little down, density a little up, since the motion axis lengthens durations and adds overshoot), dynamic and lively move motion up, clear and simple open the density, practical and modern move type personality toward geometric, solid and robust firm the contrast and square the corners, reliable and secure raise formality and calm the motion, approachable and caring warm the system. A word's weights stay small (at most 0.35 on one axis) and add after the industry seed, and its formality weight reaches geometry and type personality as every word's does (decisions/tone-words-reach-shape.md). Four industries join INDUSTRY_SEEDS as seven axis values each: construction, b2b-marketplace, security and pharmacy. INDUSTRY_ALIASES points building-materials, wholesale, cybersecurity and medical-supply at them. A seed is never a look: it names no face, color or size.

## Why

The word-to-axis weights are the engine's one sanctioned mapping from words, so a word the brief uses should reach it instead of being swapped for a nearby word with a different meaning. An axis seed keeps the choice continuous: two industries that differ a little give systems that differ a little.

## What it touches

axes.TONE_NUDGES, INDUSTRY_SEEDS, INDUSTRY_ALIASES, _seed_from_industry; emit._reading and _accepted; commands/ux-system.md.

## Consequences

A brief that used these words builds a different system than before, closer to what it says. The discovery word "confident" stays unread and keeps its line in the report.
