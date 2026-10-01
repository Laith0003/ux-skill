"""Post checks for how components show their states: what a hidden control
leaves behind, whether a closing popover keeps its exit, whether a theme
switch animates every color on the page, and whether a state names itself
(an action inside a repeated item, a disabled menu row).
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional, Set

from engine.linter.structure import (
    Block, FileContext, _blocks, _children, _focus_kind, _same_container, _shares,
    _tag_tokens, attr_values, block_at, compounds, css_unescape, tokens,
)
from engine.linter.views import View

# ---------------------------------------------------------------------------
# focusable-at-opacity-zero
# ---------------------------------------------------------------------------

_OPACITY_1 = re.compile(r"opacity\s*:\s*1(?![.\d])", re.I)
_GONE = re.compile(r"visibility\s*:\s*hidden|display\s*:\s*none|content-visibility\s*:\s*hidden",
                   re.I)
# Classes a framework sets for the frames of an enter or leave transition.
_TRANSITION_CLASS = re.compile(r"(?:\.|-)(?:v-)?(?:enter|leave|exit|appear)"
                               r"(?:-(?:from|to|active|done))?(?![\w-])", re.I)
_KEYFRAME = re.compile(r"^(?:from|to|\d+(?:\.\d+)?%)$", re.I)
FOCUSABLE_TAGS = {"a", "button", "input", "select", "textarea", "summary", "iframe"}
# With no markup to read, a selector that names a control or a panel that
# holds controls.
_CONTROL_WORD = re.compile(r"(?<![\w-])(?:a|button|input|select|textarea|summary)(?![\w-])"
                           r"|\[(?:tabindex|href)|btn|button|link|menu|popover|dropdown|drawer"
                           r"|dialog|modal|sheet|nav", re.I)


# A one-argument :where() or :is() around a single compound, opened in place.
_ONE_ARG = re.compile(r":(?:where|is)\(([^()\s,>+~]*)\)")
_SIBLING = re.compile(r"[+~](?![^\[]*\])(?![^(]*\))")
_ATTR_NAME = re.compile(r"\[\s*([\w:-]+)")


def _expand(selector: str) -> str:
    """The selector with each one-argument :where() or :is() opened in
    place, so the tests inside them count when the selector is matched."""
    prev = None
    while prev != selector:
        prev, selector = selector, _ONE_ARG.sub(r"\1", selector)
    return selector


def _needs(compound: str) -> Set[str]:
    """What an element must carry to match a compound: its tag, classes
    (unescaped) and id, and the names of the attributes it tests."""
    out: Set[str] = set()
    for t in tokens(compound):
        if t.startswith("["):
            m = _ATTR_NAME.match(t)
            if m:
                out.add("[" + m.group(1).lower() + "]")
        else:
            out.add(css_unescape(t))
    return out


def _carries(ctx: FileContext, i: int) -> Set[str]:
    tag = ctx.tree()[0][i]
    have = set(_tag_tokens(ctx, tag))
    have.update("[" + name.lower() + "]" for name in attr_values(ctx.text, tag))
    return have


def _elements(ctx: FileContext, selector: str) -> List[int]:
    """Elements a selector can match, judged by tags, classes, ids and the
    attributes it tests; states and pseudo-classes are not evaluated, so
    this is a superset of what the browser matches."""
    parts = [_needs(c) for c in compounds(_expand(selector))]
    if not parts:
        return []
    tags, _ends, parents = ctx.tree()
    out = []
    for i in range(len(tags)):
        if not parts[-1] <= _carries(ctx, i):
            continue
        j, k = len(parts) - 2, parents[i]
        while j >= 0 and k >= 0:
            if parts[j] <= _carries(ctx, k):
                j -= 1
            k = parents[k]
        if j < 0:
            out.append(i)
    return out


def _named_in_scripts(ctx: FileContext, selector: str) -> bool:
    """A class, id or attribute of the selector appears in the page outside
    its styles (a script adds the class or sets the state), so the element
    may match at run time. A data attribute counts in its dataset form too
    (data-state as state)."""
    sel = _expand(selector)
    names = [css_unescape(n) for n in re.findall(r"[.#]((?:[\w-]|\\.)+)", sel)]
    for attr in _ATTR_NAME.findall(sel):
        names.append(attr)
        if attr.startswith("data-"):
            names.append(re.sub(r"-(\w)", lambda m: m.group(1).upper(), attr[5:]))
    outside = _outside_styles(ctx)
    return any(re.search(r"(?<![\w-])" + re.escape(n) + r"(?![\w-])", outside) for n in names)


def _outside_styles(ctx: FileContext) -> str:
    def build() -> str:
        return re.sub(r"<style\b[^>]*>.*?</style\s*>", " ", ctx.text, flags=re.S | re.I)
    return ctx.cached("components:outside-styles", build)  # type: ignore[return-value]


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
                if parts and any(_focus_kind(p) for p in parts) and _shares(sel, h):
                    return True
    return False


_PSEUDO_ELEMENT = re.compile(r"::[\w-]+|:(?:before|after|first-line|first-letter)\b", re.I)


def focusable_hidden_by_opacity(ctx: FileContext, view: View, match: re.Match, start: int) -> bool:
    """A control, or a panel holding controls, left at opacity 0 with no
    visibility: hidden, display: none, inert or hidden companion is still
    reached by Tab and read out, though nothing shows."""
    block = block_at(ctx, view, match.start())
    if block is None or not block.selectors or _GONE.search(block.body):
        return False
    if all(_KEYFRAME.match(s.strip()) for s in block.selectors):
        return False
    # A pseudo-element (a ::before mark, a ::placeholder) never takes focus.
    if all(_PSEUDO_ELEMENT.search(compounds(s)[-1] if compounds(s) else s)
           for s in block.selectors):
        return False
    if any(_TRANSITION_CLASS.search(s) for s in block.selectors):
        return False
    if _revealed_by_focus_or_hover(_blocks(ctx, view)[0], block):
        return False
    pages = [c for c in [ctx, *ctx.pages] if c.tree()[0]]
    matched = False
    for c in pages:
        for sel in block.selectors:
            for i in _elements(c, sel):
                matched = True
                if _holds_focusable(c, i) and not _shut(c, i):
                    return True
    if matched:
        return False
    # A page with markup of its own: a selector that matches nothing there
    # styles nothing, unless a script names its class, id or attribute, or
    # it reaches its element through a sibling, which the matcher does not
    # follow. A stylesheet read with its linked pages still guesses, since
    # the page that holds the element may not be among them.
    if ctx.tree()[0] and not any(_SIBLING.search(sel) or _named_in_scripts(ctx, sel)
                                 for sel in block.selectors):
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
    if "disabled" in a and _value(a["disabled"]) not in ("false",):
        return True
    return _value(a.get("aria-disabled", ("", ""))) == "true" and "aria-describedby" not in a


def _value(attr) -> str:
    """An attribute's value with JSX braces and quotes taken off, so
    disabled={false} reads false and aria-disabled={true} reads true."""
    v = attr[1].strip().strip("{}").strip().strip("\"'").lower()
    return v


COMPONENT_CHECKS = {
    "focusable-hidden-by-opacity": focusable_hidden_by_opacity,
    "exit-cut-short": exit_cut_short,
    "theme-transition-unsuspended": theme_transition_unsuspended,
    "repeated-action-same-name": repeated_action_same_name,
    "menu-row-disabled-silent": menu_row_disabled_silent,
}
