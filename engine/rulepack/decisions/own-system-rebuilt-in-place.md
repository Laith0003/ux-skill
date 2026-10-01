---
id: own-system-rebuilt-in-place
title: An in-place extend of the engine's own system rebuilds its report and art from what the report records
status: active
areas: [output, imagery]
supersedes: null
superseded_by: null
---

# An in-place extend of the engine's own system rebuilds its report and art from what the report records

## Context

system extend writes the engine's own tokens.json again in place when the import read all of it. The build left system-report.md and art/ beside it, and both describe the tokens: the scripts, the gate line, the brand color, the fonts and the decorative colors the art paints with. tokens.json does not hold the brand color or the axes the art is drawn from; only the report says them.

## Decision

extend._built_beside builds system-report.md and each art file again from the extended tokens while the file is still as the engine wrote it (engine.existing.record.engine_wrote). emit.report_inputs reads the brand color, the axes (to the three places the report prints) and the axes line back from the report. emit.rebuild_report keeps what the system was built from, the notes, the composition and the photography direction as the build wrote them, says the opening, the scripts, the gate line, the brand color, the fonts, the brand art and the files again from the extended tokens, and adds an Extended in place section, before Files, with one line per extend naming what it added and pointing to the extend-report.md in its out folder. The opening names the foundations and modes the tokens hold and says the system was built by ux-skill and extended in place since. The Brand color section is written whenever the tokens have the brand's role, in the place a build puts it, before the notes. The art is art_files on the extended tokens with that brand color and those axes. A report the owner edited is theirs: it and the art stay as they are, and a decision line in the extend report says to build into a new folder for a fresh report and art. A report that does not say its brand color and axes is left the same way, with its own line.

## Why

A file beside the system that does not match it misleads whoever reads it next. The report is the one record of the build's inputs, so reading them back from it keeps the art on the same brand and axes without storing them twice. Notes the build made cannot be made again from tokens alone, so they stay as written, and the new section says plainly what changed after the build.

## What it touches

extend._built_beside, extend._report_and_art, emit.report_inputs, emit.rebuild_report, emit._scripts_line, emit._fonts_section, emit._extended_opening; commands/ux-system.md.

## Consequences

An in-place extend writes system-report.md and art/ with the other files it rebuilds, through the intake step, after a backup. Axes the build held to more than three places are drawn at the three the report prints, so the art can differ from the build's by that rounding.
