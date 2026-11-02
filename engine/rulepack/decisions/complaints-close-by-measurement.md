---
id: complaints-close-by-measurement
title: What the person says is wrong closes only when the page measures fixed
status: active
areas: [output]
supersedes: null
superseded_by: null
---

# What the person says is wrong closes only when the page measures fixed

## Context

The costliest failure in a rebuild is calling the work done while the one thing the person complained about is still on the page. A model's own judgement of its screenshot misses it, and a check written after the fix tends to pass on the earlier page as well.

## Decision

Each complaint is kept in .ux/complaints.json as the person's words and a probe from a closed list: rule-clear, present, absent, text-present and text-absent, read at 390, 430, 768 and 1280px. uxskill complaints check measures a file or a running app's URL and exits 3 while any complaint is open. Run with --before, the page as it was, a probe that already passes there is weak and stays open until it is one the earlier page fails. Each check records the page, a digest and when it ran; the plugin's stop hook reads that record without rendering and holds the session once while it is missing, open, or older than the page or any page source in the project.

## Why

A complaint is a test the person wrote in words. Closing it by measurement, against a probe proven to fail on the original, is the only claim of done the person can trust.

## What it touches

engine/complaints.py; bin/ux-complaints-hook.py and the plugin's Stop hook; commands/ux-design.md step 7; tests/test_complaints.py and tests/test_complaints_hook.py.

## Consequences

A vague complaint ("make it nicer") cannot be written as a probe and is answered as a question first. The closed list grows only with a probe a browser can measure.
