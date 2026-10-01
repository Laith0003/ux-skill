"""Replace dash punctuation in Markdown prose with a period, comma, colon,
semicolon or parentheses.

An em dash (U+2014), an en dash (U+2013) used as punctuation and a spaced
"--" are each read in their sentence and replaced:

- a bold term, link, code token or heading followed by a dash takes a colon;
- a pair of dashes around an aside takes parentheses, or commas when the
  aside already holds parentheses or would cross bold, quotes or code;
- a dash inside parentheses takes a comma after a value, a colon after a word;
- a dash before "and", "not", "never" and similar words takes a comma;
- a dash before a new sentence that starts with a pronoun takes a period;
- any other dash takes a colon;
- a numeric range such as 4 (en dash) 8px reads "4 to 8px";
- a dash that stands alone for an empty value reads "n/a".

Code is left alone: fenced blocks, inline code spans and HTML comments,
CLI flags (--foo), custom properties (--color-x), table separator rows and
horizontal rules. In YAML front matter a colon is used only inside a quoted
value, so the front matter still parses.

fix_text() handles one prose string; fix_markdown() handles a document.
Standard library only.
"""
from __future__ import annotations

import re

EM, EN = "\u2014", "\u2013"
_PH_OPEN, _PH_CLOSE = "\ue000", "\ue001"
_PH = _PH_OPEN + r"\d+" + _PH_CLOSE
_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_SEPARATOR = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")
_DOUBLE = re.compile(r"(?<![-!])--(?![-\w>])")
_MARKER = re.compile(r"^(\s*(?:>\s*)*(?:[-*+]\s+(?:\[[ xX]\]\s+)?|\d+[.)]\s+|#{1,6}\s+)?)")
_BLOCKSTART = re.compile(r"^\s*(?:>|[-*+]\s|\d+[.)]\s|#{1,6}\s|\|)")

# Words after which a dash reads best as a comma.
COMMA_WORDS = frozenset("""and but or nor so yet not never which who whose whom where while
whereas because since unless until though although even rather except including especially
plus then often usually typically sometimes mostly ideally preferably otherwise as like with
without from at in on by for via per than only just almost e.g. i.e. etc versus vs vs. after
before""".split())
# Words that start a new sentence after a dash.
PRONOUNS = frozenset("""that it it's they they're we we're you you're this these those there
there's here he she i""".split())
# Words that open a new independent clause after a closing parenthesis.
_CLAUSE = frozenset("""the it its it's this these those they there we you only no each every
both all a an he she""".split())
# Words that open a sentence with an introductory phrase.
_INTRO = frozenset("""when if every as while because although though once until after before
since in on at for during whenever wherever where unless""".split())
# Words that open a subordinate clause the main clause must follow.
_SUBORDINATE = frozenset("""when if while because although though once until after before since
whenever wherever unless""".split())
# Verbs that show an "only ..." tail is a clause of its own.
_ONLY_VERBS = re.compile(r"\b(is|are|was|were|vary|varies|change|changes|flip|flips|inverts?|"
                         r"shifts?|differentiates?|distinguishes?|pivots?|appears?|documented)\b")


class _Doc:
    """State for one fix: the protected code spans and whether colons are allowed."""

    def __init__(self):
        self.store: list[str] = []
        self.colon_ok = True

    def hold(self, text: str) -> str:
        self.store.append(text)
        return f"{_PH_OPEN}{len(self.store) - 1}{_PH_CLOSE}"

    def protect_inline(self, line: str) -> str:
        out, i = [], 0
        while i < len(line):
            if line[i] != "`":
                out.append(line[i])
                i += 1
                continue
            run = len(line[i:]) - len(line[i:].lstrip("`"))
            m = re.compile(r"(?<!`)" + "`" * run + r"(?!`)").search(line, i + run)
            if m is None:
                out.append(line[i:i + run])
                i += run
                continue
            out.append(self.hold(line[i:m.end()]))
            i = m.end()
        return "".join(out)

    def restore(self, text: str) -> str:
        while _PH_OPEN in text:
            text = re.sub(_PH_OPEN + r"(\d+)" + _PH_CLOSE, lambda m: self.store[int(m.group(1))], text)
        return text


def _plain(s: str) -> str:
    """Text for word checks: code becomes a word, links lose their targets."""
    s = re.sub(_PH, "CODE", s)
    s = re.sub(r"\]\([^)]*\)", "]", s)
    return re.sub(r"https?://\S+", "URL", s)


def _outside(s: str) -> str:
    """The plain text with parenthesized and quoted parts removed."""
    s = _plain(s)
    prev = None
    while prev != s:
        prev = s
        s = re.sub(r"\([^()]*\)", "", s)
    return re.sub(r"\"[^\"]*\"", "", s)


def _has_colon(s: str) -> bool:
    return re.search(r":(\s|\*|_|$)", _outside(s)) is not None


def _words(s: str) -> list[str]:
    return re.findall(r"[\w'.]+", _plain(s))


def _next_word(s: str) -> str:
    m = re.match(r"[\w'.]+", _plain(s).lstrip(" \t\n*_>\"'("))
    return m.group(0) if m else ""


def _balanced(s: str) -> bool:
    p = _plain(s)
    bold = p.count("**")
    single = p.replace("**", "").count("*")
    return bold % 2 == 0 and single % 2 == 0 and p.count("\"") % 2 == 0 and "|" not in p


def _pick_gap(lws: str, rws: str) -> str:
    if "\n" in lws:
        return lws[lws.rfind("\n"):]
    if "\n" in rws:
        return rws[rws.rfind("\n"):]
    return " "


def _gap_of(left: str, right: str) -> str:
    return _pick_gap(re.search(r"\s*$", left).group(0), re.match(r"\s*", right).group(0))


def _capitalize(s: str) -> str:
    m = re.match(r"([*_\"'(]*)([a-z])", s)
    return s if not m else s[:m.start(2)] + m.group(2).upper() + s[m.end(2):]


def _can_cap(s: str) -> bool:
    return re.match(r"[*_\"'(]*[a-z]", s.lstrip()) is not None


def _join(left: str, punct: str, right: str, cap: bool = False) -> str:
    lws = re.search(r"\s*$", left).group(0)
    rws = re.match(r"\s*", right).group(0)
    gap = _pick_gap(lws, rws)
    right = right[len(rws):]
    if cap:
        right = _capitalize(right)
    return left[:len(left) - len(lws)] + punct + gap + right


def _sentence_spans(unit: str, skip: int = 0) -> list[tuple[int, int]]:
    bounds = [0]
    for m in re.finditer(r"\|", unit):
        bounds += [m.start(), m.end()]
    for m in re.finditer(r"(?<=[.!?])(?:[*_\"')\]]*)\s+(?=[*_\"'(\[]*[A-Z0-9" + _PH_OPEN + "])", unit):
        if m.start() > skip:
            bounds.append(m.end())
    bounds.append(len(unit))
    bounds = sorted(set(bounds))
    return list(zip(bounds, bounds[1:]))


def _paren_depth(s: str) -> int:
    d = 0
    for ch in _plain(s):
        if ch == "(":
            d += 1
        elif ch == ")":
            d = max(0, d - 1)
    return d


def _in_quotes(sent: str, p: int) -> bool:
    return sent[:p].count("\"") % 2 == 1 and "\"" in sent[p + 1:]


def _inside_paren_kind(sent: str, p: int) -> str:
    pre = sent[:p]
    inner_pre = pre[pre.rfind("(") + 1:]
    close_at = sent.find(")", p)
    inner_post = sent[p + 1:close_at if close_at != -1 else len(sent)]
    nxt = inner_post.lstrip()
    if (_next_word(inner_post).lower() in COMMA_WORDS
            or nxt.startswith((_PH_OPEN, "#", "rgb", "oklch", "hsl"))
            or re.match(r"[\d~$]", nxt) or _has_colon(inner_pre) or _has_colon(inner_post)
            or not re.search(r"[A-Za-z]", re.sub(_PH, "", inner_pre))
            or EM in inner_post or EM in inner_pre
            or re.fullmatch(r"\s*(#[0-9a-fA-F]{3,8}|[\d.\s/%a-z]*\d[\d.\s/%a-z]*)\s*", inner_pre)):
        return "comma"
    return "colon"


def _comma_or_semicolon(after: str) -> str:
    """A comma, or a semicolon when a clause of its own follows."""
    nw = _next_word(after).lower()
    clause = re.split(r"(?<=[.!?])\s", after, 1)[0]
    if nw == "instead" or (nw in _CLAUSE - {"only", "a", "an", "no", "all", "both", "each", "every"}
                           and re.search(r"\b(is|are|was|were|has|have|does|do|holds?|reads?|"
                                         r"sits?|runs?|uses?|carries|carry|trusts?|comes?)\b", clause)):
        return "semicolon"
    if nw == "only" and _ONLY_VERBS.search(clause):
        return "semicolon"
    return "comma"


def _decide_single(pre: str, after: str, fm: bool, heading: bool, colon_ok: bool) -> str:
    nw = _next_word(after).lower()
    if _paren_depth(pre) > 0:
        return "comma"
    if nw == "instead":
        return "semicolon"
    if nw in COMMA_WORDS:
        return _comma_or_semicolon(after)
    if _has_colon(pre):
        short = len(_words(after)) <= 16
        if (short and not _plain(pre).rstrip().endswith(")") and "(" not in _plain(after)
                and ")" not in _plain(after) and _balanced(_tail_split(after)[0])):
            return "paren"
        return _comma_or_semicolon(after)
    if _has_colon(after):
        return "paren" if heading and _balanced(_tail_split(after)[0]) else _comma_or_semicolon(after)
    if heading:
        return "colon" if colon_ok else "comma"
    if nw in PRONOUNS and _can_cap(after) and len(_words(pre)) >= 4:
        return "period"
    return "colon" if colon_ok else _comma_or_semicolon(after)


def _tail_split(right: str) -> tuple[str, str]:
    m = re.search(r"([.!?;,]?[\"'*_]*\s*)$", right)
    return right[:m.start()], right[m.start():]


def _apply_paren(sent: str, i: int) -> str:
    left, right = sent[:i], sent[i + 1:]
    body, tail = _tail_split(right)
    gap = _gap_of(left, body)
    return left.rstrip() + gap + "(" + body.strip() + ")" + tail


def _after_close(sent_before_open: str, r2: str) -> str:
    """Punctuation after a closing parenthesis so the sentence does not run on."""
    m = re.match(r"\s*([a-z][\w'-]*)", r2)
    if not m:
        return ""
    nw = m.group(1)
    first = _next_word(sent_before_open).lower()
    if first in _SUBORDINATE and "," not in _plain(sent_before_open):
        return ","
    if nw in _CLAUSE:
        return "," if first in _INTRO else ";"
    if nw in ("never", "not", "so") or (nw.endswith("ing") and len(nw) > 5):
        return ","
    return ""


def _process_sentence(sent: str, fm: bool, heading: bool, first: bool, marker: str, colon_ok: bool) -> str:
    if sent.strip() == EM:
        return sent.replace(EM, "n/a")
    if re.search(r":(\*\*|__)?\s*" + EM + r"\s*$", sent):
        sent = re.sub(EM + r"(\s*)$", r"n/a\1", sent)
    if EM not in sent:
        return sent
    pos = [m.start() for m in re.finditer(EM, sent)]
    plan: dict[int, str] = {}
    for p in list(pos):
        if _in_quotes(sent, p):
            nw = _next_word(sent[p + 1:]).lower()
            plan[p] = "comma" if nw in COMMA_WORDS or not colon_ok else "colon"
            pos.remove(p)
    label_i = None
    if first and pos:
        pre = sent[:pos[0]]
        body = pre[len(marker):] if pre.startswith(marker) else pre
        strong = heading or re.fullmatch(
            r"\s*(\*\*[^*]+\*\*|__[^_]+__|\[[^\]]+\]\([^)]*\)|" + _PH + r"|\*\*" + _PH + r"\*\*)"
            r"(\s*[+&,/]\s*(\*\*[^*]+\*\*|" + _PH + r"|\*\*" + _PH + r"\*\*))*(\s*\([^)]*\))?\s*",
            body) is not None
        if (len(_words(body)) <= 10 and not re.search(r"[.;!?]\s", _plain(body))
                and not _has_colon(body) and _paren_depth(body) == 0 and body.strip()
                and _balanced(body) and (strong or len(pos) % 2 == 1)):
            label_i = pos[0]
    rest = [p for p in pos if p != label_i]
    if label_i is not None:
        after = sent[label_i + 1:]
        nw = _next_word(after).lower()
        quiet = COMMA_WORDS - {"with", "from", "at", "in", "on", "by", "for", "as", "like"}
        if nw in quiet and not re.match(r"\s*[*_\"]*[A-Z]", after):
            plan[label_i] = "comma"
        elif not colon_ok:
            plan[label_i] = "comma"
        elif _has_colon(after):
            plan[label_i] = "period" if re.match(r"\s*[*_\"]*[A-Z]", after) else "comma"
        else:
            plan[label_i] = "colon"
    for p in list(rest):
        if _paren_depth(sent[:p]) > 0:
            kind = _inside_paren_kind(sent, p)
            plan[p] = kind if colon_ok or kind != "colon" else "comma"
            rest.remove(p)
    while len(rest) >= 2:
        a, b = rest[0], rest[1]
        aside = sent[a + 1:b]
        nested = "(" in _plain(aside) or ")" in _plain(aside)
        adjacent = sent[:a].rstrip().endswith(")") or sent[b + 1:].lstrip().startswith("(")
        if nested or adjacent or not _balanced(aside):
            plan[a] = plan[b] = "comma"
        else:
            plan[a], plan[b] = "open", "close"
        rest = rest[2:]
    for p in rest:
        start = len(marker) if first and sent.startswith(marker) else 0
        pre = sent[start:p]
        if label_i is not None and plan.get(label_i) == "colon" and label_i < p:
            pre = pre.replace(EM, ":", 1)
        plan[p] = _decide_single(pre, sent[p + 1:], fm, heading, colon_ok)
    out = sent
    for p in sorted(plan, reverse=True):
        kind = plan[p]
        left, right = out[:p], out[p + 1:]
        if kind == "colon":
            out = _join(left, ":", right)
        elif kind == "semicolon":
            out = _join(left, ";", right)
        elif kind == "comma":
            right = re.sub(r"^(\s*)(The|A|An) ", lambda m: m.group(1) + m.group(2).lower() + " ", right)
            out = _join(left, ",", right)
        elif kind == "period":
            out = _join(left, ".", right, cap=True)
        elif kind == "open":
            out = left.rstrip() + _gap_of(left, right) + "(" + right.lstrip()
        elif kind == "close":
            lws = re.search(r"\s*$", left).group(0)
            rws = re.match(r"\s*", right).group(0)
            r2 = right[len(rws):]
            opener = [q for q in plan if plan[q] == "open" and q < p]
            before_open = out[:max(opener)] if opener else ""
            if before_open.startswith(marker):
                before_open = before_open[len(marker):]
            mark = _after_close(before_open, r2)
            sep = "" if re.match(r"[.,;:!?)]", r2) or not r2 else " "
            if "\n" in lws + rws:
                sep = _pick_gap(lws, rws)
            out = left.rstrip() + ")" + mark + sep + r2
        elif kind == "paren":
            out = _apply_paren(out, p)
    return out


def _process_unit(doc: _Doc, unit: str, fm: bool = False) -> str:
    mk = _MARKER.match(unit).group(1)
    doc.colon_ok = (not fm) or bool(re.match(r'^\s*(?:-\s+)?[\w.$-]+:\s*"', unit))
    if fm:
        mk = re.match(r"^\s*(?:-\s+)?(?:[\w.$-]+:\s*)?[\"'>|]?\s*", unit).group(0)
    heading = mk.strip().startswith("#")
    spans = _sentence_spans(unit, len(mk.rstrip()))
    pieces = []
    for idx, (a, b) in enumerate(spans):
        s = unit[a:b]
        first = idx == 0 or unit[a - 1:a] == "|" or unit[spans[idx - 1][0]:spans[idx - 1][1]] == "|"
        marker = mk if idx == 0 else re.match(r"\s*", s).group(0)
        pieces.append(_process_sentence(s, fm, heading, first, marker, doc.colon_ok))
    return "".join(pieces)


def _normalize(line: str) -> str:
    """'--' and en dashes become em dashes or 'to' ranges, on one protected line."""
    if not _SEPARATOR.match(line):
        line = _DOUBLE.sub(EM, line)
    tok = r"[\d" + _PH_CLOSE + "%x\u00d7]"
    line = re.sub(r"(?<=" + tok + r")\s*" + EN + "\\s*(?=[~$+\\-\u2212]?[\\d" + _PH_OPEN + r"])", " to ", line)
    line = re.sub(r"(?<=\w)" + EN + r"(?=\w)", " to ", line)
    line = line.replace(EN, EM)
    line = re.sub(r"(?<=\|)(\s*)" + EM + r"(?=\s*\|)", r"\1n/a", line)
    line = re.sub(r"(:(?:\*\*|__)?\s*)" + EM + r"(\s*)$", r"\1n/a\2", line)
    if line.strip() == EM:
        line = line.replace(EM, "n/a")
    return line


def _process_block(doc: _Doc, lines: list[str], fm: bool = False) -> str:
    units, cur = [], []
    for ln in lines:
        if cur and (_BLOCKSTART.match(ln) or fm):
            units.append(cur)
            cur = []
        cur.append(ln)
    if cur:
        units.append(cur)
    out = []
    for u in units:
        text = "\n".join(u)
        if EM in text:
            text = _process_unit(doc, text, fm)
        out.append(text)
    return "\n".join(out)


def fix_text(text: str) -> str:
    """One prose string (a paragraph, a list item, a field value) without dashes."""
    if EM not in text and EN not in text and "--" not in text:
        return text
    doc = _Doc()
    lines = [_normalize(doc.protect_inline(ln)) for ln in text.split("\n")]
    return doc.restore(_process_block(doc, lines))


def fix_markdown(text: str) -> str:
    """A Markdown document with dash punctuation replaced in its prose."""
    comments: list[str] = []

    def hide(m):
        comments.append(m.group(0))
        return f"\ue002{len(comments) - 1}\ue003"

    doc = _Doc()
    lines = re.sub(r"<!--.*?-->", hide, text, flags=re.S).split("\n")
    fm_end = -1
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() in ("---", "..."):
                fm_end = j
                break
    out: list[str] = []
    para: list[str] = []
    para_fm = False

    def flush():
        if para:
            out.append(_process_block(doc, para, para_fm))
            para.clear()

    fence = None
    for n, line in enumerate(lines):
        if fm_end > 0 and n == 0:
            out.append(line)
            continue
        if 0 < n < fm_end:
            para_fm = True
            para.append(_normalize(doc.protect_inline(line)))
            continue
        if n == fm_end:
            flush()
            para_fm = False
            out.append(line)
            continue
        m = _FENCE.match(line)
        if fence:
            out.append(line)
            if (m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence)
                    and not line.strip().strip(fence[0])):
                fence = None
            continue
        if m:
            flush()
            fence = m.group(1)
            out.append(line)
            continue
        if not line.strip():
            flush()
            out.append(line)
            continue
        para.append(_normalize(doc.protect_inline(line)))
    flush()
    result = doc.restore("\n".join(out))
    return re.sub("\ue002(\\d+)\ue003", lambda m: comments[int(m.group(1))], result)
