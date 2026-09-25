---
id: client-identity-wins
title: A client's own identity wins over the generic bans, even without a full design system
status: active
areas: [color, imagery, output]
supersedes: null
superseded_by: null
---

# A client's own identity wins over the generic bans, even without a full design system

## Context

A project with its own token files wins over the guidance's label and accent defaults (decisions/existing-system-wins.md). Most clients have less than that: a logo, a site, an app, a brand book. On three real landing pages the generic bans in references/styles/anti-slop.md hit those identities: an electric blue above the saturation ceiling, a brand gradient from blue to violet, pure white as the client's canvas, a blue gradient band on the client's own app. Read as binding, each ban told an agent to change the client's brand.

## Decision

The client's own identity is fixed input whether or not a full system exists. When the client's logo, site, app or brand book uses a color above the saturation ceiling, a gradient, pure white or pure black, a blue or violet hue, or tracked or untracked labels, the page keeps it as the client uses it. The bans in anti-slop.md apply to what a model reaches for by default, never to what the client chose. The evidence is the client's own material, named in the build notes (which file, which screen); a word in the brief ("we like blue") is not an identity. A mark beside an eyebrow still needs the recorded waiver (decisions/eyebrow-is-text.md), and the contrast gate still holds: the identity's color is kept and the text on it is solved for contrast (decisions/natural-fill-for-white-text.md).

## Why

The bans exist to stop generated pages from looking alike. A client's identity is the opposite of a default: it is what makes the page theirs. Applying the bans to it produces a generic page with the client's name on it.

## What it touches

references/styles/anti-slop.md (principle 10 and the color rows); commands/ux-design.md (the hard rules and the tokens step); decisions/existing-system-wins.md covers the full-system case and stays in force.

## Consequences

An agent keeps the client's saturated brand, gradient or white canvas and says where it came from. A page with no client identity, or a system the engine builds from a hex alone, keeps every ban.
