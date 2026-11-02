"""Checks for product illustrations: a picture of the product's interface on
a page, the subject of references/styles/product-illustration.md, often
built with the Stageshow kit (engine/kits/stageshow).

focusable-in-hidden-subtree: a control a keyboard can reach, inside an
aria-hidden subtree that is not inert. heading-in-stage: a real heading
inside a Stageshow stage, which joins the host page's outline.
stage-loops-unpaused: a scripted Stage left on its default loop, in a file
with no pause control.
"""
from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional

from engine.linter.structure import FileContext, attr_values
from engine.linter.views import View

_INTERACTIVE = {"button", "a", "input", "select", "textarea"}
_FIELDS = {"button", "select", "textarea", "input"}
_STAGE_CLASS = re.compile(r"(?<![\w-])ss-(?:stage|window|fit)(?![\w-])")
_HEADING = re.compile(r"^h[1-6]$")
_PAUSE = re.compile(r"""aria-label\s*=\s*[{"'`][^}"'`]*\bpause\b|>\s*pause\b|\bpause\s*<"""
                    r"""|\bonPause\b|\bdata-pause\b""", re.I)


def _value(raw: str) -> str:
    """An attribute's value without JSX braces or quotes."""
    v = raw.strip()
    if v.startswith("{") and v.endswith("}"):
        v = v[1:-1].strip()
    return v.strip("'\"`").strip()


def _index(ctx: FileContext, start: int) -> Optional[int]:
    tag = ctx.tag_at(start)
    if tag is None:
        return None
    tags, _, _ = ctx.tree()
    for i, t in enumerate(tags):
        if t.start == tag.start:
            return i
    return None


def _chain(ctx: FileContext, i: int) -> List[int]:
    """The element and each of its ancestors, nearest first."""
    _, _, parents = ctx.tree()
    out = []
    while i >= 0:
        out.append(i)
        i = parents[i]
    return out


def _focusable(ctx: FileContext, tag) -> bool:
    name = tag.name.lower()
    a = attr_values(ctx.text, tag)
    if "tabindex" in a:
        return not _value(a["tabindex"][1]).startswith("-")
    if "disabled" in a and _value(a["disabled"][1]).lower() not in ("false",):
        return False
    if name == "input":
        return _value(a.get("type", ("", ""))[1]).lower() != "hidden"
    if name in _FIELDS:
        return True
    if name in ("a", "area"):
        return "href" in a
    if "contenteditable" in a:
        return _value(a["contenteditable"][1]).lower() != "false"
    return False


def focusable_in_hidden_subtree(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An aria-hidden element is a finding when a control a keyboard can
    reach sits inside it and neither it nor an ancestor is inert. The
    control itself carrying aria-hidden is aria-hidden-on-interactive."""
    i = _index(ctx, start)
    if i is None:
        return False
    tags, _, _ = ctx.tree()
    if tags[i].name.lower() in _INTERACTIVE:
        return False
    if any("inert" in attr_values(ctx.text, tags[k]) for k in _chain(ctx, i)):
        return False
    j = i + 1
    _, ends, _ = ctx.tree()
    while j < len(tags) and tags[j].start < ends[i]:
        if _focusable(ctx, tags[j]):
            return True
        j += 1
    return False


def heading_in_stage(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A heading is a finding inside a Stageshow stage: a <Stage> element, or
    an element whose class names ss-stage, ss-window or ss-fit."""
    i = _index(ctx, start)
    if i is None:
        return False
    tags, _, _ = ctx.tree()
    if not _HEADING.match(tags[i].name.lower()):
        return False
    for k in _chain(ctx, i)[1:]:
        if tags[k].name == "Stage":
            return True
        a = attr_values(ctx.text, tags[k])
        cls = a.get("classname", a.get("class", ("", "")))[1]
        if _STAGE_CLASS.search(cls):
            return True
    return False


def stage_loops_unpaused(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A Stage is a finding when it has a script, plays on its default loop
    (no play, or play="loop") and nothing in the file is a pause control.
    play bound to an expression is left alone: it may be the pause."""
    i = _index(ctx, start)
    if i is None:
        return False
    tags, _, _ = ctx.tree()
    tag = tags[i]
    if tag.name != "Stage":
        return False
    a = attr_values(ctx.text, tag)
    if "script" not in a:
        return False
    if "play" in a:
        kind, raw = a["play"]
        value = _value(raw)
        if kind == "expr" and not re.fullmatch(r"""['"`]\w+['"`]""", raw.strip("{} ")):
            return False
        if value != "loop":
            return False
    return not _PAUSE.search(ctx.text)


ILLUSTRATION_CHECKS: Dict[str, Callable[[FileContext, View, re.Match, int], bool]] = {
    "focusable-in-hidden-subtree": focusable_in_hidden_subtree,
    "heading-in-stage": heading_in_stage,
    "stage-loops-unpaused": stage_loops_unpaused,
}
