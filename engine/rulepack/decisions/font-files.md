---
id: font-files
title: fonts.css holds the matched fallbacks, fonts-self-host.css the faces, and every weight is one a face ships
status: active
areas: [output, type]
supersedes: font-loading
superseded_by: null
---

# fonts.css holds the matched fallbacks, fonts-self-host.css the faces, and every weight is one a face ships

## Context

One fonts.css held both the faces (local() then a self-hosted file) and their fallbacks. The Google Fonts route told the owner to delete the first block of it, which made the file differ from the next build, so the build refused to write and a forced build put the block back. local("<family>") matched the installed Regular file at every weight, so an installed face drew its bold text in Regular strokes. The Arabic fallback face had no unicode range, so it drew the spaces, digits and Latin letters of every Arabic run for good. And a static face was treated as shipping every weight between its ends, so a link could ask Google Fonts for Tajawal 600, which it refuses, and a token could name a weight the browser never draws.

## Decision

A build writes two font files. fonts.css holds only the metric-matched fallback faces, one per face, with the Arabic fallbacks limited to the Arabic blocks. fonts-self-host.css holds the faces: for a variable face one file with its weight range and no local(), since an installed copy may hold a single weight; for a static face one file per weight it ships, found first by that weight's own full and PostScript names ("Tajawal Bold", "Tajawal-Bold"). The page loads the faces with the Google Fonts link the report gives, or with fonts-self-host.css, and links fonts.css with either one; neither file is edited. The catalog records the weights a static face ships, and every weight the tokens, the link and fonts-self-host.css name snaps to the nearest one it ships, the heavier at the same distance.

## Why

A route that needs a hand edit fights the build's own rule never to overwrite a file that differs. Per-weight names are what local() matches, so an installed face keeps its weights. A fallback that covers only the Arabic blocks lets Latin in an Arabic run reach the Latin face. A token that names a weight the face ships is the weight the reader sees, and a link that asks only for shipped weights loads.

## What it touches

fonts.Face.stops and clamp, STYLE_NAMES, local_names, css2_family, cdn_url, link_tags, fonts_css and self_host_css; emit.FILES and the report's Fonts and Files sections; typography's Arabic weights and type.strong, which snap through the face; the CLI and MCP descriptions of what a build writes.

## Consequences

A build writes five files and the art. Both font files follow the axes, not the brand, so a new brand color leaves them unchanged. A static face at a weight between two it ships renders the heavier one, and the tokens say so.
