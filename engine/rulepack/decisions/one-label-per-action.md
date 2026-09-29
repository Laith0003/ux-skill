---
id: one-label-per-action
title: One action carries one label everywhere on the page
status: active
areas: [content]
supersedes: null
superseded_by: null
---

# One action carries one label everywhere on the page

## Context

A landing page repeats its primary action in the header, the hero, a sticky bar and the closing band. Generated pages word each repeat afresh, so a reader who meets the action a third time under a third name has to work out whether it is the same step.

## Decision

Every call to action that does the same thing carries the same words, the verb of the hero's button. The label says what happens next and promises what the form asks for. The lint rule one-action-several-labels groups calls to action by what they do (the same link destination, a trailing slash aside, or the same form by a button's form attribute) and fires on each one whose visible words differ from the first in the file. A call to action is a button, an element with role="button", or a link with a btn, button or cta class. Plain text links, controls with no visible words, words filled in at run time, and empty, phone and mail links are not compared.

## Why

The primary action is the one thing the page asks for. When it has one name, the reader recognizes it at every depth of the page; when it has several, the page reads as undecided.

## What it touches

data/anti-patterns.json one-action-several-labels; engine/linter/structure.py one_action_several_labels; references/surfaces/landing.md (CTA); tests/lint_corpus/cases/one-action-several-labels, tests/lint_corpus/probes/label and tests/lint_corpus/dirty.

## Consequences

A different next step, such as watching a demo beside starting a trial, has its own destination and its own label, and it is a text link when it is secondary. A link styled as a plain text link is not compared, so a footer that names a page differently from the nav stays quiet. Buttons for different plans that share one destination ("Choose Basic" and "Choose Pro" both to /signup) fire, and the fix is to carry the plan in the link (/signup?plan=pro), not to give them one label: the label promises a plan the link must carry.
