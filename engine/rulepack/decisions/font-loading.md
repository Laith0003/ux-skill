---
id: font-loading
title: The build writes fonts.css with local faces first and matched fallbacks
status: superseded
areas: [type, output]
supersedes: null
superseded_by: font-files
---

# The build writes fonts.css with local faces first and matched fallbacks

## Context

Faces that are named in the tokens but never loaded leave a page in system fonts, and a face that loads late moves every line of text when it arrives.

## Decision

Every build writes fonts.css beside tokens.css. For each face it names, fonts.css has an @font-face that loads the reader's installed copy first (local()) and then a WOFF2 in a fonts/ folder beside it, with font-display swap; Arabic faces carry the Arabic unicode ranges so a page without Arabic never downloads them. Each face also gets a fallback face, named after it with Fallback added, on a common system font with size-adjust, ascent-override, descent-override and line-gap-override computed from the measured metrics, and the face tokens list it second. A comment in fonts.css and the Fonts section of the report give one Google Fonts link for loading the faces from there instead.

## Why

Local first costs nothing when the face is installed; a self-hosted file keeps the page independent of a third party; the matched fallback keeps line breaks where they will be, so swapping faces does not shift the layout.

## What it touches

fonts.fonts_css, cdn_url, loading_lines, fallback_overrides, FALLBACKS; emit.FILES and the report's Fonts section; the type face tokens.

## Consequences

A build writes four files. The fonts/ folder is the owner's to fill; fonts.css works without it, from local copies or the fallbacks.
