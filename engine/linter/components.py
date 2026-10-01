"""Post checks for how components show their states: what a hidden control
leaves behind, whether a closing popover keeps its exit, whether a theme
switch animates every color on the page, and whether a state names itself
(an action inside a repeated item, a disabled menu row).
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Set

from engine.linter.structure import (
    Block, FileContext, _blocks, _children, _focus_kind, _matching_elements,
    _same_container, _shares, attr_values, block_at, compounds, tokens,
)
from engine.linter.views import View

# ---------------------------------------------------------------------------
# focusable-at-opacity-zero
# ---------------------------------------------------------------------------

_OPACITY_1 = re.compile(r"opacity\s*:\s*1(?![.\d])", re.I)
_GONE = re.compile(r"visibility\s*:\s*hidden|display\s*:\s*none|content-visibility\s*:\s*hidden",
                   re.I)
# Classes a framework sets for the frames of an enter or leave transition.
_TRANSITION_CLASS = re.compile(r"enter|leave|exit|appear|from\b", re.I)
_KEYFRAME = re.compile(r"^(?:from|to|\d+(?:\.\d+)?%)$", re.I)
FOCUSABLE_TAGS = {"a", "button", "input", "select", "textarea", "summary", "iframe"}
# With no markup to read, a selector that names a control or a panel that
# holds controls.
_CONTROL_WORD = re.compile(r"(?<![\w-])(?:a|button|input|select|textarea|summary)(?![\w-])"
                           r"|\[(?:tabindex|href)|btn|button|link|menu|popover|dropdown|drawer"
                           r"|dialog|modal|sheet|nav", re.I)


def _focusable(ctx: FileContext, i: int) -> bool:
    tags = ctx.tree()[0]
    t = tags[i]
    a = attr_values(ctx.text, t)
    name = t.name.lower()
    if "tabindex" in a:
        return a["tabindex"][1].strip() != "-1"
    if name == "a":
        return "href" in a
    if name == "input":
        return a.get("type", ("", ""))[1].lower() != "hidden"
    return name in FOCUSABLE_TAGS or "contenteditable" in a


def _shut(ctx: FileContext, i: int) -> bool:
    """The element or an ancestor is hidden or inert in the markup."""
    tags, _ends, parents = ctx.tree()
    k = i
    while k >= 0:
        a = attr_values(ctx.text, tags[k])
        if "inert" in a or "hidden" in a:
            return True
        k = parents[k]
    return False


def _holds_focusable(ctx: FileContext, i: int) -> bool:
    kids = _children(ctx)
    todo = [i]
    while todo:
        k = todo.pop()
        if _focusable(ctx, k):
            return True
        todo.extend(kids.get(k, []))
    return False


def _revealed_by_focus_or_hover(blocks: List[Block], hidden: Block) -> bool:
    """A rule shows the element again on hover (hover-only-card-actions
    judges that) or on its own focus (a skip link)."""
    for b in blocks:
        if not _OPACITY_1.search(b.body):
            continue
        for sel in b.selectors:
            parts = compounds(sel)
            for h in hidden.selectors:
                if ":hover" in sel and _shares(sel.replace(":hover", ""), h) \
                        and _same_container(sel, h):
                    return True
                if parts and _focus_kind(parts[-1]) and _shares(sel, h):
                    return True
    return False


def focusable_hidden_by_opacity(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A control, or a panel holding controls, left at opacity 0 with no
    visibility: hidden, display: none, inert or hidden companion is still
    reached by Tab and read out, though nothing shows."""
    block = block_at(ctx, view, match.start())
    if block is None or not block.selectors or _GONE.search(block.body):
        return False
    if all(_KEYFRAME.match(s.strip()) for s in block.selectors):
        return False
    if any(_TRANSITION_CLASS.search(s) for s in block.selectors):
        return False
    if _revealed_by_focus_or_hover(_blocks(ctx, view)[0], block):
        return False
    pages = [c for c in [ctx, *ctx.pages] if c.tree()[0]]
    matched = False
    for c in pages:
        for sel in block.selectors:
            parts = compounds(sel)
            if not parts:
                continue
            for i in _matching_elements(c, [tokens(x) for x in parts]):
                matched = True
                if _holds_focusable(c, i) and not _shut(c, i):
                    return True
    if matched:
        return False
    return any(_CONTROL_WORD.search(compounds(s)[-1] if compounds(s) else s)
               for s in block.selectors)


# ---------------------------------------------------------------------------
# exit-cut-by-display-none
# ---------------------------------------------------------------------------

_CLOSED = re.compile(r"\[data-state\s*=\s*[\"']?closed|\.is-closed\b|\.closed\b"
                     r"|:not\(\s*(?:\.is-open|\.open|\[open\]|:popover-open|\[data-state\s*=\s*"
                     r"[\"']?open[\"']?\])\s*\)|\[aria-hidden\s*=\s*[\"']?true", re.I)
_STATE_PART = re.compile(r"\[data-state[^\]]*\]|\.is-closed\b|\.closed\b|:not\([^)]*\)"
                         r"|\[aria-hidden[^\]]*\]", re.I)
_MOVES = re.compile(r"(?<![\w-])transition(?:-property)?\s*:[^;]*(?:opacity|transform|scale"
                    r"|translate|\ball\b)", re.I)
_DISCRETE = re.compile(r"allow-discrete", re.I)


def exit_cut_short(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A closed state that sets display: none while the open state moves on
    a transition cuts the exit off at its first frame, unless the
    transition lets display wait (allow-discrete)."""
    block = block_at(ctx, view, match.start())
    if block is None or not any(_CLOSED.search(s) for s in block.selectors):
        return False
    if _DISCRETE.search(block.body):
        return False
    bases = {" ".join(_STATE_PART.sub("", s).split()) for s in block.selectors}
    for b in _blocks(ctx, view)[0]:
        if b is block or not _MOVES.search(b.body):
            continue
        if any(" ".join(s.split()) in bases for s in b.selectors):
            return not _DISCRETE.search(b.body)
    return False


# ---------------------------------------------------------------------------
# theme-switch-animates-everything
# ---------------------------------------------------------------------------

_EVERY = re.compile(r"^(?:\*|html\s+\*|body\s+\*|:root\s+\*|\*::?(?:before|after))$")
_THEME_COLORS = re.compile(r"(?:background(?:-color)?|(?<![\w-])color|border(?:-color)?|fill"
                           r"|stroke|\ball\b)", re.I)
_THEME_HOOK = re.compile(r"\[data-(?:theme|mode|color-scheme)|\.(?:dark|light|theme-[\w-]+)\b",
                         re.I)
_SUSPEND_HOOK = re.compile(r"switch|no-?transition|disable-?transition|theme-change|changing",
                           re.I)
_NONE = re.compile(r"transition\s*:\s*none|transition-duration\s*:\s*0m?s", re.I)


def theme_transition_unsuspended(ctx: FileContext, view: View, match: re.Match,
                                 start: int) -> bool:
    """A transition on every element's colors, on a page with a theme
    switch, animates the whole page through the switch. It passes when a
    switching hook (a class or attribute naming the switch) sets transition
    none for the frame the theme changes in."""
    block = block_at(ctx, view, match.start())
    if block is None or not block.selectors:
        return False
    if not any(_EVERY.match(s.strip()) for s in block.selectors):
        return False
    value = match.group(0)
    if not _THEME_COLORS.search(value):
        return False
    blocks = _blocks(ctx, view)[0]
    if not any(_THEME_HOOK.search(s) for b in blocks for s in b.selectors):
        return False
    return not any(_NONE.search(b.body) and any(_SUSPEND_HOOK.search(s) for s in b.selectors)
                   for b in blocks)


# ---------------------------------------------------------------------------
# repeated-action-same-name
# ---------------------------------------------------------------------------

_ITEM_TAGS = {"li", "tr", "article"}
_ITEM_ROLES = {"listitem", "row", "article", "option", "gridcell"}
_STRIP_TAGS = re.compile(r"<[^>]*>")


def _name(ctx: FileContext, i: int) -> Optional[str]:
    tags, ends, _ = ctx.tree()
    a = attr_values(ctx.text, tags[i])
    if "aria-labelledby" in a:
        return None
    if "aria-label" in a:
        return " ".join(a["aria-label"][1].split()).lower() or None
    inner = ctx.text[tags[i].end:ends[i]]
    text = " ".join(_STRIP_TAGS.sub(" ", inner).split()).lower()
    return text or None


def _item(ctx: FileContext, i: int) -> Optional[int]:
    """The repeated item an element sits in: the nearest li, tr, article or
    element with an item role."""
    tags, _ends, parents = ctx.tree()
    k = parents[i]
    while k >= 0:
        t = tags[k]
        role = attr_values(ctx.text, t).get("role", ("", ""))[1].lower()
        if t.name.lower() in _ITEM_TAGS or role in _ITEM_ROLES:
            return k
        k = parents[k]
    return None


def _repeated_names(ctx: FileContext) -> Set[int]:
    def build() -> Set[int]:
        tags, _ends, parents = ctx.tree()
        groups: Dict[str, List[int]] = {}
        for i, t in enumerate(tags):
            if t.name.lower() not in ("button", "a"):
                continue
            item = _item(ctx, i)
            name = _name(ctx, i)
            if item is None or name is None:
                continue
            groups.setdefault(f"{parents[item]}|{name}", []).append(i)
        out: Set[int] = set()
        for members in groups.values():
            items = {_item(ctx, i) for i in members}
            if len(items) >= 2:
                out.add(tags[members[0]].start)
        return out
    return ctx.cached("components:repeated-names", build)  # type: ignore[return-value]


def repeated_action_same_name(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """Buttons or links that share one accessible name across the items of
    a list, table or feed: a screen reader's list of controls reads Save,
    Save, Save. Reported once, on the first."""
    return start in _repeated_names(ctx)


# ---------------------------------------------------------------------------
# menu-row-disabled-without-reason
# ---------------------------------------------------------------------------

def menu_row_disabled_silent(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A menu row disabled with the disabled attribute (it leaves the arrow
    keys' path) or with aria-disabled and no reason it can be read with."""
    tag = ctx.tag_at(start)
    if tag is None:
        return False
    a = attr_values(ctx.text, tag)
    if "disabled" in a:
        return True
    return a.get("aria-disabled", ("", ""))[1].lower() == "true" and "aria-describedby" not in a


COMPONENT_CHECKS = {
    "focusable-hidden-by-opacity": focusable_hidden_by_opacity,
    "exit-cut-short": exit_cut_short,
    "theme-transition-unsuspended": theme_transition_unsuspended,
    "repeated-action-same-name": repeated_action_same_name,
    "menu-row-disabled-silent": menu_row_disabled_silent,
}
