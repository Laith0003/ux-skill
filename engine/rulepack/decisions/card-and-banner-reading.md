---
id: card-and-banner-reading
title: Card bodies and banner text read at full strength
status: active
areas: [contracts]
supersedes: null
superseded_by: null
---

# Card bodies and banner text read at full strength

## Context

A card body in the muted color greys out the card's main content, the card's inner radius rule could give a negative radius, and a banner's title and body sat smaller than the paragraphs around them.

## Decision

A card's title and body take the default text color; a meta part takes the muted color for dates and counts. Inner media is rounded by the card radius minus the padding, never below 0 (radius.joined where the padding is larger). A status banner's title and body are set in type.text.body, the title in type.strong. A banner has at most one action button; an error summary lists a link to each field in error, and those links are not actions.

## Why

Muted is for what supports the content, not for the content. A banner interrupts reading, so it must be at least as readable as the text it interrupts.

## What it touches

engine/contracts/seed/card.yaml and status-banner.yaml.

## Consequences

Cards gain a meta part. An error summary banner is allowed to list many links.
