---
id: gallery-from-spec-facts
title: Each gallery system is built from its own spec's design facts and passes the gate in every mode
status: active
areas: [output, color]
supersedes: null
superseded_by: null
---

# Each gallery system is built from its own spec's design facts and passes the gate in every mode

## Context

The gallery holds one system per brand spec in data/brands. Each spec states design facts: a primary color and sometimes accents, a canvas, an ink, its radii, its spacing base, its faces and a motion signature that may name durations. A gallery system needs a brand color and the seven axes, and each must come from those facts and nothing else, the same way every other look the engine builds does.

## Decision

scripts/build_gallery.py writes data/gallery/<id>.json for every spec. The brand color is the primary when it reaches 3:1 on the canvas (1.4.11, what a control needs to be seen); otherwise the accent with the most contrast on the canvas, when that accent reaches 3:1; otherwise the primary, and the engine derives the action color from it. Each axis is a continuous function of the spec's facts, written out in the script's docstring: warmth from the primary's and the canvas's hue weighted by their sRGB chroma; contrast from the ink's ratio on the canvas, the loudest chroma and how dark the page is; density from the spacing base; geometry from the mean radius, with a pill counted as 32px; formality from the chroma of the primary and the ink; motion from the durations the motion signature states; type personality, and a share of formality, from the measured place of a face the engine's catalog holds. A fact the spec does not state leaves its axis at 0.5, and the entry's source sentence says so. Every entry is built with make_system with the Arabic face and scale, so it is validated and gated in light, dark, high contrast, compact, right to left and reduced motion; an entry that fails is not written. Each entry carries a digest of its tokens.

## Why

A spec's facts are the only evidence of how the brand looks, and reading them through formulas keeps the gallery honest: a small change in a fact makes a small change in the system, and two specs with the same facts build the same system whatever they are called. Choosing the brand color by contrast keeps the action visible without naming any spec. The digest makes a change in the engine show up as a reviewable diff in the gallery.

## What it touches

scripts/build_gallery.py; data/gallery; scripts/release_checks.py (reads the gallery for the round trip); tests/test_gallery.py.

## Consequences

The gallery is rebuilt by running python scripts/build_gallery.py, and python scripts/build_gallery.py --check names every entry that drifted. A change to the engine that moves any built token changes the digests, so the gallery is rebuilt in the same change. Prose fields, names and ids of a spec never move its axes. A spec that states few facts sits near the middle of the axes it does not state.
