---
id: extension-carried-forward
title: A later extend writes the engine's own extension file again without force, and each out folder keeps its own intake record
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# A later extend writes the engine's own extension file again without force, and each out folder keeps its own intake record

## Context

An extension file sits beside the system it extends, since that is where it loads from. A later extend of the same system reads that file first and keeps everything it added, so the file it writes holds the earlier additions and the new ones. The report and the mapping go into the out folder the caller names, and a second extend often names another one.

## Decision

write_with_intake takes `rewrite`: files the write may replace without force while the engine's record still matches them. extend.write_extended passes the system's extension files there (theme-ext.css, tokens-ext.json, or the Figma variables file and its script) whenever the system is not written in place. Each is backed up under the source folder's .uxskill/backup before it is replaced, as any replaced file is. An extension the owner edited does not match the record, so it is theirs and needs force, and a file of the owner's in the way still needs force and the replace flag. Each folder written keeps its own intake record: the source's folder lists the extension, and each out folder lists the report and mapping written there.

## Why

The extension is carried forward whole, so writing it again loses nothing, and asking for force there would make every second extend look like a risky overwrite. The engine's record is what tells its own file from an edited one, the same test force itself uses.

## What it touches

intake.write_with_intake, extend.write_extended; commands/ux-system.md.

## Consequences

A second extend into a different out folder writes the extension again and its report into the new folder. A second extend into the same out folder still stops at the report and mapping already there, which force replaces.
