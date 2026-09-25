---
id: controls-on-brand-surfaces
title: Controls keep their edges and focus ring on the tint, the band, the stripe and the brand band
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Controls keep their edges and focus ring on the tint, the band, the stripe and the brand band

## Context

The guidance puts controls on the brand-tinted surfaces: ghost buttons in a striped table row, a field or a link in a tinted feature panel, a closing call to action on a band or the brand band. Measured only against the page, card, sunken and raised surfaces, the focus ring fell to about 3.9:1 on the stripe under high contrast and the selected and accent lines to about 2.9:1 on the band.

## Decision

The tint, the band and the table stripe join the surfaces every line role (input, selected, error, accent) and the focus ring are paired with, at 3:1 (WCAG 1.4.11) and our 4.5:1 floor under high contrast. The ring solver reads its surfaces from those pairings, so it chooses a ring that clears them too. The brand band is not one of them: it is the exact brand, often a mid tone, and under high contrast no single ring can stand 4.5:1 off both a mid tone band and a white page (a mid blue such as #3366FF would need a ring darker than black). A control on the brand band takes color.text.on-brand for its focus ring and edges instead; that role is paired with the band at the text minimum, 4.5:1 and 7:1 under high contrast, above the non-text one.

## Why

A surface that holds controls must hold their edges and focus, or a keyboard user loses the focus on exactly the rows and panels the guidance recommends. The text on the brand band is already measured against it and contrasts with it by construction, so it is the one color that is always safe there.

## What it touches

color.LINE_SURFACES and the pairings build_pairings writes from it; the ring solver's surfaces (_paired_with); guidance/color.md, brand-surfaces.md, ring-offset.md and error-edge.md.

## Consequences

Line roles and the ring may take a step further out on brands whose band or stripe sits close to them. A contract that places a control on the brand band binds its ring and edges to color.text.on-brand.
