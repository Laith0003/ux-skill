"""Checks for product illustrations: a picture of the product's interface on
a page, the subject of references/styles/product-illustration.md, often
built with the Stageshow kit (engine/kits/stageshow).

focusable-in-hidden-subtree: a control a keyboard can reach, inside an
aria-hidden subtree that is not inert. heading-in-stage: a real heading
inside a Stageshow stage, which joins the host page's outline.
stage-loops-unpaused: a scripted Stage left on its default loop, in a file
with no pause control.

Whether a keyboard reaches an element is the one answer structure.py gives
(takes_focus and shut), shared with the component checks.
"""
from __future__ import annotations

import re
from typing import Callable, Dict, Optional

from engine.linter.structure import FileContext, attr_values, bound_attr, shut, takes_focus
from engine.linter.views import View

_INTERACTIVE = {"button", "a", "input", "select", "textarea"}
_STAGE_CLASS = re.compile(r"(?<![\w-])ss-(?:stage|window|fit)(?![\w-])")
_HEADING = re.compile(r"^h[1-6]$")
_PAUSE_WORD = re.compile(r"\bpause\b", re.I)
_NO_SCRIPT = {"undefined", "null", "false", ""}


def _index(ctx: FileContext, start: int) -> Optional[int]:
    """The tree index of the tag whose attribute list holds `start`."""
    tag = ctx.tag_at(start)
    if tag is None:
        return None
    by_start: Dict[int, int] = ctx.cached(  # type: ignore[assignment]
        "illustration:index", lambda: {t.start: i for i, t in enumerate(ctx.tree()[0])})
    return by_start.get(tag.start)


def focusable_in_hidden_subtree(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """An aria-hidden element is a finding when a control a keyboard can
    reach sits inside it: not in a hidden or inert part, and not disabled or
    out of the tab order. The control itself carrying aria-hidden is
    aria-hidden-on-interactive."""
    i = _index(ctx, start)
    if i is None:
        return False
    tags, ends, _ = ctx.tree()
    if tags[i].name.lower() in _INTERACTIVE or shut(ctx, i):
        return False
    j = i + 1
    while j < len(tags) and tags[j].start < ends[i]:
        if not shut(ctx, j) and takes_focus(ctx, j):
            return True
        j += 1
    return False


def heading_in_stage(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A heading is a finding inside a Stageshow stage: a <Stage> element, or
    an element whose class names ss-stage, ss-window or ss-fit."""
    i = _index(ctx, start)
    if i is None:
        return False
    tags, _, parents = ctx.tree()
    if not _HEADING.match(tags[i].name.lower()):
        return False
    k = parents[i]
    while k >= 0:
        if tags[k].name == "Stage":
            return True
        a = attr_values(ctx.text, tags[k])
        cls = a.get("classname", a.get("class", ("", "")))[1]
        if _STAGE_CLASS.search(cls):
            return True
        k = parents[k]
    return False


def _has_pause_control(ctx: FileContext) -> bool:
    """A button in the file named for pausing: its aria-label (an expression
    included, such as paused ? 'Play' : 'Pause') or its text says pause."""
    def build() -> bool:
        tags, ends, _ = ctx.tree()
        for i, t in enumerate(tags):
            a = attr_values(ctx.text, t)
            role = (bound_attr(a, "role") or "").lower()
            if t.name.lower() != "button" and role != "button":
                continue
            label = a.get("aria-label", a.get(":aria-label", ("", "")))[1]
            if _PAUSE_WORD.search(label) or _PAUSE_WORD.search(ctx.text[t.end:ends[i]]):
                return True
        return False
    return ctx.cached("illustration:pause", build)  # type: ignore[return-value]


def stage_loops_unpaused(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A Stage is a finding when it has a script, plays on its default loop
    (no play, or play="loop") and no button in the file pauses it. play
    bound to an expression is left alone: it may be the pause. A script of
    undefined or null makes the Stage a still."""
    i = _index(ctx, start)
    if i is None:
        return False
    tag = ctx.tree()[0][i]
    if tag.name != "Stage":
        return False
    a = attr_values(ctx.text, tag)
    script = bound_attr(a, "script")
    if script is None or script.lower() in _NO_SCRIPT:
        return False
    if "play" in a:
        kind, raw = a["play"]
        literal = re.fullmatch(r"""\{?\s*['"`](\w+)['"`]\s*\}?|(\w+)""", raw.strip())
        if kind == "expr" and not (literal and literal.group(1)):
            return False
        if bound_attr(a, "play") != "loop":
            return False
    return not _has_pause_control(ctx)


ILLUSTRATION_CHECKS: Dict[str, Callable[[FileContext, View, re.Match, int], bool]] = {
    "focusable-in-hidden-subtree": focusable_in_hidden_subtree,
    "heading-in-stage": heading_in_stage,
    "stage-loops-unpaused": stage_loops_unpaused,
}
