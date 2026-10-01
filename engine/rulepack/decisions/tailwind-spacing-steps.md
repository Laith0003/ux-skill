---
id: tailwind-spacing-steps
title: Tailwind's own spacing steps are raw values while the project's theme keeps the scale
status: active
areas: [space, output]
supersedes: null
superseded_by: null
---

# Tailwind's own spacing steps are raw values while the project's theme keeps the scale

## Context

A Tailwind preset that sets theme.extend.spacing adds names to Tailwind's spacing scale and keeps the scale itself, so px-6 is still 24px and inset-0 is 0. A preset that sets theme.spacing replaces the scale, and so does a Tailwind 4 @theme block with --spacing-*: initial. A class that names no token of the system is listed apart, as a name the system lacks.

## Decision

The theme reader records each namespace a theme replaces (ThemeMap.replaced): a Tailwind 3 theme key set outside extend, or a Tailwind 4 reset, with "*" for --*: initial. When a theme was read and it keeps the spacing namespace (ThemeMap.keeps), a spacing class on a step of Tailwind's default scale (0, px, 0.5 to 3.5, 4 to 12, then 14 to 96) is a raw spacing value of that many 4px steps, signed for a negative class, and drift reports it as a raw value. With no theme read, or with the scale replaced, the class names no token and is listed apart. A name the theme or the system maps still wins.

## Why

A raw value the code writes through Tailwind's scale is drift the owner can move onto a token; calling it a missing token says the system lacks a name it never had to have. Reading the scale only when a theme shows the project keeps it avoids treating a replaced scale as present.

## What it touches

tailwind_config.ThemeMap (replaced, keeps), tailwind_config._Reader.config, tailwind_config._theme_blocks, scan.TAILWIND_SPACING and the Tailwind class reader; commands/ux-system.md.

## Consequences

Code on a preset that extends spacing reports px-6 as 24px among the raw space values, not among the classes that name no token.
