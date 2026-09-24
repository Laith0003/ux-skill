"""Decision records: front matter, five fixed sections in order, the fact
as it stands, and a HISTORY index that routes to every record once."""
import pytest

from engine.rulepack.records import (
    HEADINGS, RecordError, check_folder, history_problems, load_records, read_record,
    record_sources)

GOOD = """\
---
id: sample-choice
title: Samples keep one role
status: active
areas: [color]
supersedes: null
superseded_by: null
---

# Samples keep one role

## Context

Two roles did one job.

## Decision

One role does it.

## Why

One is easier to check.

## What it touches

color.py.

## Consequences

Nothing else changes.
"""


def test_a_valid_record_reads_whole():
    record, problems = read_record(GOOD, "sample-choice.md")
    assert problems == []
    assert (record.id, record.title, record.status, record.areas) == (
        "sample-choice", "Samples keep one role", "active", ("color",))
    assert [h for h, _ in record.sections] == list(HEADINGS)
    assert record.section("Why") == "One is easier to check."


@pytest.mark.parametrize("edit,rule,message", [
    (lambda t: t.replace("---\nid", "id", 1), "front-matter",
     "x.md: the file does not open with a front matter block"),
    (lambda t: t.replace("id: sample-choice", "id: other"), "id",
     "sample-choice.md: id is 'other'; use the file name without .md"),
    (lambda t: t.replace("status: active", "status: draft"), "status",
     "sample-choice.md: status is 'draft'; use active or superseded"),
    (lambda t: t.replace("areas: [color]", "areas: [paint]"), "areas",
     "sample-choice.md: areas is ['paint']"),
    (lambda t: t.replace("status: active", "status: superseded"), "superseded_by",
     "sample-choice.md: a superseded record names the record that replaces it"),
    (lambda t: t.replace("## Why", "## Reasons"), "headings",
     "sample-choice.md: the sections are ['Context', 'Decision', 'Reasons', 'What it touches', "
     "'Consequences']; use exactly Context, Decision, Why, What it touches, Consequences, in "
     "that order"),
    (lambda t: t.replace("One is easier to check.", ""), "empty-section",
     "sample-choice.md: the Why section is empty; write it"),
    (lambda t: t.replace("# Samples keep one role\n", "# Another title\n"), "title",
     "sample-choice.md: the body's heading is ['Another title']"),
    (lambda t: t.replace("One role does it.", "One role does it; the old pair is gone."),
     "history", "sample-choice.md: 'the old' tells how the rule changed"),
    (lambda t: t.replace("One role does it.", "We no longer keep two."), "history",
     "sample-choice.md: 'no longer' tells how the rule changed; state the decision as it "
     "stands, and let HISTORY.md route to what came before"),
    (lambda t: t.replace("One role does it.", "One role \u2014 does it."), "dash",
     "sample-choice.md: the record holds an em dash"),
])
def test_each_rule_names_the_record_and_the_fix(edit, rule, message):
    source = "x.md" if rule == "front-matter" else "sample-choice.md"
    record, problems = read_record(edit(GOOD), source)
    assert record is None
    assert any(p.rule == rule and p.message.startswith(message) for p in problems), problems


def _folder(tmp_path, records, history):
    for name, text in records.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    if history is not None:
        (tmp_path / "HISTORY.md").write_text(history, encoding="utf-8")
    return tmp_path


def test_history_routes_to_every_record_once(tmp_path):
    folder = _folder(tmp_path, {"sample-choice.md": GOOD},
                     "# History\n\n- [Samples keep one role](sample-choice.md)\n")
    records = load_records(folder)
    assert [r.id for r in records] == ["sample-choice"]
    assert history_problems(records, "- [x](sample-choice.md)\n- [y](sample-choice.md)\n"
                                     "- [z](gone.md)\n") != []
    messages = [p.message for p in history_problems(records, "# History\n")]
    assert messages == ["HISTORY.md: sample-choice is not listed; add a line "
                        "- [Samples keep one role](sample-choice.md) under its chapter"]


def test_a_supersede_chain_must_hold_both_ways(tmp_path):
    old = GOOD.replace("status: active", "status: superseded").replace(
        "superseded_by: null", "superseded_by: newer-choice")
    newer = GOOD.replace("sample-choice", "newer-choice").replace(
        "supersedes: null", "supersedes: sample-choice")
    history = "- [a](sample-choice.md)\n- [b](newer-choice.md)\n"
    folder = _folder(tmp_path, {"sample-choice.md": old, "newer-choice.md": newer}, history)
    assert [r.id for r in load_records(folder)] == ["newer-choice", "sample-choice"]
    (tmp_path / "newer-choice.md").write_text(GOOD.replace("sample-choice", "newer-choice"),
                                              encoding="utf-8")
    _, problems = check_folder(folder)
    assert [p.rule for p in problems] == ["supersede-chain"]


def test_a_folder_without_history_or_records_is_named(tmp_path):
    with pytest.raises(RecordError, match="holds no decision record"):
        load_records(tmp_path)
    _folder(tmp_path, {"sample-choice.md": GOOD}, None)
    _, problems = check_folder(tmp_path)
    assert [p.rule for p in problems] == ["history-missing"]


# Each row below proves one branch of read_record: remove the branch and its
# row fails.
@pytest.mark.parametrize("edit,rule,message", [
    (lambda t: t.replace("supersedes: null", "supersedes: Old_Choice"), "supersedes",
     "sample-choice.md: supersedes is 'Old_Choice'; name a record id or write null"),
    (lambda t: t.replace("superseded_by: null", "superseded_by: newer-choice"), "superseded_by",
     "sample-choice.md: an active record has no superseded_by; set status to superseded or "
     "clear it"),
    (lambda t: t.replace("title: Samples keep one role", 'title: ""'), "title",
     "sample-choice.md: title is empty; state the decision in one line"),
    (lambda t: t.replace("superseded_by: null\n", "superseded_by: null\nowner: design\n"),
     "front-matter",
     "sample-choice.md: the front matter has ['areas', 'id', 'owner', 'status', 'superseded_by', "
     "'supersedes', 'title']; give it exactly id, title, status, areas, supersedes, "
     "superseded_by"),
    (lambda t: t.replace("One role does it.", "One role \u2013 does it."), "dash",
     "sample-choice.md: the record holds an em dash, an en dash or '--'"),
    (lambda t: t.replace("One role does it.", "One role -- does it."), "dash",
     "sample-choice.md: the record holds an em dash, an en dash or '--'"),
])
def test_each_front_matter_and_prose_rule_is_proven(edit, rule, message):
    record, problems = read_record(edit(GOOD), "sample-choice.md")
    assert record is None
    assert any(p.rule == rule and p.message.startswith(message) for p in problems), problems


def _one_record():
    record, problems = read_record(GOOD, "sample-choice.md")
    assert problems == []
    return (record,)


@pytest.mark.parametrize("history,messages", [
    ("- [a](sample-choice.md)\n- [z](gone.md)\n",
     ["HISTORY.md: links gone.md, which is not a record; link each record as (id.md)"]),
    ("- [a](sample-choice.md)\n- [z](sample-choice.ts)\n",
     ["HISTORY.md: links sample-choice.ts, which is not a record; link each record as (id.md)"]),
    ("- [a](sample-choice.md)\n- [b](sample-choice.md)\n",
     ["HISTORY.md: links sample-choice.md 2 times; route to each record once"]),
    ("- [a](sample-choice.md) \u2014 the first\n",
     ["HISTORY.md: holds an em dash, an en dash or '--'; use a period, a comma or a colon"]),
    ("- [a](sample-choice.md) \u2013 the first\n",
     ["HISTORY.md: holds an em dash, an en dash or '--'; use a period, a comma or a colon"]),
    ("- [a](sample-choice.md) -- the first\n",
     ["HISTORY.md: holds an em dash, an en dash or '--'; use a period, a comma or a colon"]),
])
def test_each_history_rule_names_the_fault_alone(history, messages):
    assert [p.message for p in history_problems(_one_record(), history)] == messages


def test_a_record_that_supersedes_one_that_does_not_name_it_back(tmp_path):
    newer = GOOD.replace("sample-choice", "newer-choice").replace(
        "supersedes: null", "supersedes: sample-choice")
    history = "- [a](sample-choice.md)\n- [b](newer-choice.md)\n"
    folder = _folder(tmp_path, {"sample-choice.md": GOOD, "newer-choice.md": newer}, history)
    _, problems = check_folder(folder)
    assert [p.message for p in problems] == [
        "newer-choice.md: supersedes names sample-choice, which must exist, be superseded and "
        "name newer-choice in superseded_by"]


def test_record_sources_lists_every_file_history_included(tmp_path):
    folder = _folder(tmp_path, {"sample-choice.md": GOOD}, "# History\n")
    (tmp_path / "notes.txt").write_text("not a record", encoding="utf-8")
    assert record_sources(folder) == {"HISTORY.md": "# History\n", "sample-choice.md": GOOD}
