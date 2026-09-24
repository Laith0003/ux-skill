"""A strict reader for the small YAML subset component contracts use.

Contracts are YAML so people and agents can read and write them, but the
engine stays standard library only, so it reads a documented subset and
refuses everything else by line number, with the fix:

- block mappings (``key: value``) and block sequences (``- item``),
  nested by indentation with spaces; a sequence may sit at its key's
  indentation;
- a sequence item may open a mapping on its own line (``- name: label``);
- one-line flow collections: ``[a, b]`` and ``{key: value}``, nested;
- scalars: ``null`` and ``~``, ``true`` and ``false``, integers, decimals
  with a point, single or double quoted text, and plain text;
- comments after ``#`` at the start of a line or after a space.

Refused, each with a message: tabs, anchors, aliases, tags, multi-line
scalars (``|`` and ``>``), document markers, duplicate keys, a plain value
holding ``": "``, plain keys that are not simple names, and the YAML 1.1
words yes, no, on, off, y and n, which other readers turn into booleans.
Lists and maps nest at most MAX_DEPTH deep and a number has at most
MAX_DIGITS digits, so no input reaches the caller as anything but a
YamlError.
A date such as 2026-09-25 is read as text.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*")
_INT = re.compile(r"[-+]?(0|[1-9][0-9]*)")
_FLOAT = re.compile(r"[-+]?([0-9]*\.[0-9]+|[0-9]+\.[0-9]*)([eE][-+]?[0-9]+)?")
_NULLS = ("null", "Null", "NULL", "~")
_TRUE = ("true", "True", "TRUE")
_FALSE = ("false", "False", "FALSE")
_AMBIGUOUS = ("yes", "no", "on", "off", "y", "n")
_RESERVED = ("&", "*", "!", "|", ">", "%", "@", "`")
# How many lists and maps may nest inside each other. Contracts need a
# handful; the cap turns runaway nesting into an error with the line.
MAX_DEPTH = 64
# How many digits a number may have. Longer numbers are refused rather than
# handed to int() and float(), which fail or lose them.
MAX_DIGITS = 100


class YamlError(ValueError):
    """Text outside the supported subset, or malformed. The message names
    the source and the line, and says the fix."""


@dataclass(frozen=True)
class _Line:
    number: int
    indent: int
    text: str


def _fail(source: str, number: int, message: str) -> YamlError:
    return YamlError(f"{source} line {number}: {message}")


def _strip_comment(text: str, source: str, number: int) -> str:
    """The line without its comment. A '#' starts a comment at the start of
    the line or after a space, outside quotes. A quote opens only where a
    value can start, so an apostrophe inside plain text is text."""
    quote = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if quote == '"':
            if ch == "\\":
                i += 2
                continue
            if ch == '"':
                quote = ""
        elif quote == "'":
            if ch == "'":
                if text[i + 1:i + 2] == "'":
                    i += 2
                    continue
                quote = ""
        elif ch in "\"'" and (i == 0 or text[i - 1] in " [{,"):
            quote = ch
        elif ch == "#" and (i == 0 or text[i - 1] == " "):
            return text[:i].rstrip()
        i += 1
    if quote:
        raise _fail(source, number, f"a {quote} quote is never closed; close it on the same line")
    return text.rstrip()


def _lines(text: str, source: str) -> List[_Line]:
    out: List[_Line] = []
    for number, raw in enumerate(text.splitlines(), 1):
        body = raw.lstrip(" \t")
        if "\t" in raw[:len(raw) - len(body)]:
            raise _fail(source, number, "a tab indents this line; indent with spaces")
        content = _strip_comment(body, source, number)
        if not content:
            continue
        if content in ("---", "...") or content.startswith("%"):
            raise _fail(source, number, f"{content!r} is a document marker or directive; "
                                        "a contract is one document, so remove the line")
        out.append(_Line(number, len(raw) - len(body), content))
    return out


def _show(text: str) -> str:
    """The text for a message, cut to a readable length."""
    return repr(text if len(text) <= 40 else text[:37] + "...")


def _deeper(depth: int, source: str, number: int) -> int:
    """The depth of a list or map that opens inside `depth` others."""
    if depth + 1 > MAX_DEPTH:
        raise _fail(source, number, f"this value nests more than {MAX_DEPTH} lists and maps "
                                    "deep; flatten it")
    return depth + 1


def _plain(text: str, source: str, number: int, in_flow: bool = False) -> Any:
    """A plain (unquoted) scalar, resolved to None, a bool, a number or text."""
    if text in _NULLS:
        return None
    if text in _TRUE:
        return True
    if text in _FALSE:
        return False
    if text.lower() in _AMBIGUOUS:
        raise _fail(source, number, f"the plain word {text!r} reads as a yes or no in other YAML "
                                    f"readers; write true or false, or quote it as '{text}'")
    if text.startswith(_RESERVED):
        raise _fail(source, number, f"{text!r} starts with {text[0]!r}, which marks an anchor, "
                                    "alias, tag or multi-line text this reader does not "
                                    "support; quote the value or keep it on one line")
    if ": " in text or (not in_flow and text.endswith(":")):
        raise _fail(source, number, f"{text!r} holds ': ' inside a plain value; quote the value")
    is_int, is_float = _INT.fullmatch(text), _FLOAT.fullmatch(text)
    if (is_int or is_float) and sum(ch.isdigit() for ch in text) > MAX_DIGITS:
        raise _fail(source, number, f"the number {_show(text)} has more than {MAX_DIGITS} "
                                    "digits; quote it if it is text, or shorten it")
    if is_int:
        return int(text)
    if is_float:
        return float(text)
    return text


_ESCAPES = {"n": "\n", "t": "\t", '"': '"', "\\": "\\", "/": "/", "0": "\0"}


def _quoted(text: str, start: int, source: str, number: int) -> Tuple[str, int]:
    """The quoted scalar starting at text[start]; returns (value, index after
    the closing quote)."""
    quote = text[start]
    out: List[str] = []
    i = start + 1
    while i < len(text):
        ch = text[i]
        if quote == "'":
            if ch == "'":
                if text[i + 1:i + 2] == "'":
                    out.append("'")
                    i += 2
                    continue
                return "".join(out), i + 1
            out.append(ch)
        else:
            if ch == "\\":
                nxt = text[i + 1:i + 2]
                if nxt not in _ESCAPES:
                    raise _fail(source, number, f"'\\{nxt}' is not an escape this reader "
                                                "knows; use \\n, \\t, \\\" or \\\\")
                out.append(_ESCAPES[nxt])
                i += 2
                continue
            if ch == '"':
                return "".join(out), i + 1
            out.append(ch)
        i += 1
    raise _fail(source, number, f"a {quote} quote is never closed; close it on the same line")


class _Flow:
    """Recursive reader for one-line flow collections and scalars."""

    def __init__(self, text: str, source: str, number: int, depth: int = 0):
        self.text, self.source, self.number, self.i = text, source, number, 0
        self.depth = depth

    def fail(self, message: str) -> YamlError:
        return _fail(self.source, self.number, message)

    def skip(self) -> None:
        while self.i < len(self.text) and self.text[self.i] == " ":
            self.i += 1

    def value(self, stops: str, depth: int) -> Any:
        self.skip()
        if self.i >= len(self.text):
            raise self.fail("a value is missing in a [...] or {...} list; write one or remove "
                            "the extra comma")
        ch = self.text[self.i]
        if ch == "[":
            return self.sequence(_deeper(depth, self.source, self.number))
        if ch == "{":
            return self.mapping(_deeper(depth, self.source, self.number))
        if ch in "\"'":
            value, self.i = _quoted(self.text, self.i, self.source, self.number)
            return value
        start = self.i
        while self.i < len(self.text) and self.text[self.i] not in stops:
            self.i += 1
        word = self.text[start:self.i].strip()
        if not word:
            raise self.fail("a value is missing in a [...] or {...} list; write one or remove "
                            "the extra comma")
        return _plain(word, self.source, self.number, in_flow=True)

    def sequence(self, depth: int) -> List[Any]:
        self.i += 1
        items: List[Any] = []
        self.skip()
        if self.text[self.i:self.i + 1] == "]":
            self.i += 1
            return items
        while True:
            items.append(self.value(",]", depth))
            self.skip()
            ch = self.text[self.i:self.i + 1]
            self.i += 1
            if ch == "]":
                return items
            if ch != ",":
                raise self.fail("a [...] list is not closed with ']'; close it on the same line")

    def mapping(self, depth: int) -> Dict[str, Any]:
        self.i += 1
        items: Dict[str, Any] = {}
        self.skip()
        if self.text[self.i:self.i + 1] == "}":
            self.i += 1
            return items
        while True:
            self.skip()
            if self.text[self.i:self.i + 1] in ("\"", "'"):
                key, self.i = _quoted(self.text, self.i, self.source, self.number)
            else:
                start = self.i
                while self.i < len(self.text) and self.text[self.i] not in ":,}":
                    self.i += 1
                key = self.text[start:self.i].strip()
                if not _KEY.fullmatch(key):
                    raise self.fail(f"{key!r} is not a simple key; use letters, digits, '_', "
                                    "'.' and '-', or quote it")
            self.skip()
            if self.text[self.i:self.i + 1] != ":":
                raise self.fail(f"key {key!r} in a {{...}} map has no ':'; write key: value")
            self.i += 1
            if key in items:
                raise self.fail(f"key {key!r} appears twice in one {{...}} map; keep one")
            items[key] = self.value(",}", depth)
            self.skip()
            ch = self.text[self.i:self.i + 1]
            self.i += 1
            if ch == "}":
                return items
            if ch != ",":
                raise self.fail("a {...} map is not closed with '}'; close it on the same line")

    def whole(self) -> Any:
        value = self.value("", self.depth)
        self.skip()
        if self.i != len(self.text):
            raise self.fail(f"{self.text[self.i:]!r} follows a complete value; remove it or "
                            "quote the whole value")
        return value


def _inline(text: str, source: str, number: int, depth: int = 0) -> Any:
    if text[0] in "[{\"'":
        return _Flow(text, source, number, depth).whole()
    return _plain(text, source, number)


def _split_key(line: _Line, source: str) -> Tuple[str, str]:
    """(key, rest) of a mapping line; rest is "" when the value is a block."""
    text = line.text
    if text[0] in "\"'":
        key, end = _quoted(text, 0, source, line.number)
        rest = text[end:]
        if not rest.startswith(":"):
            raise _fail(source, line.number, f"key {key!r} has no ':' after it; write key: value")
        rest = rest[1:]
    else:
        m = re.match(r"([^:]*?):(?: |$)", text)
        if not m:
            raise _fail(source, line.number, f"{text!r} is not a 'key: value' line or a '- item' "
                                             "line; fix its indentation or add the ':'")
        key = m.group(1)
        if not _KEY.fullmatch(key):
            raise _fail(source, line.number, f"{key!r} is not a simple key; use letters, digits, "
                                             "'_', '.' and '-', or quote it")
        rest = text[m.end(1) + 1:]
    if rest and not rest.startswith(" "):
        raise _fail(source, line.number, f"key {key!r} needs a space after its ':'")
    return key, rest.strip()


class _Block:
    def __init__(self, lines: List[_Line], source: str):
        self.lines, self.source = lines, source

    def fail(self, line: _Line, message: str) -> YamlError:
        return _fail(self.source, line.number, message)

    def block(self, i: int, indent: int, depth: int) -> Tuple[Any, int]:
        line = self.lines[i]
        depth = _deeper(depth, self.source, line.number)
        if line.text == "-" or line.text.startswith("- "):
            return self.sequence(i, indent, depth)
        return self.mapping(i, indent, depth)

    def child(self, i: int, indent: int, allow_same: bool, depth: int) -> Tuple[Any, int]:
        """The block that follows line i-1 as its value, or None when none does."""
        if i < len(self.lines):
            nxt = self.lines[i]
            if nxt.indent > indent or (allow_same and nxt.indent == indent
                                       and (nxt.text == "-" or nxt.text.startswith("- "))):
                return self.block(i, nxt.indent, depth)
        return None, i

    def mapping(self, i: int, indent: int, depth: int,
                first: Optional[_Line] = None) -> Tuple[Dict[str, Any], int]:
        out: Dict[str, Any] = {}
        while i < len(self.lines) or first is not None:
            line = first if first is not None else self.lines[i]
            if first is None:
                if line.indent < indent:
                    break
                if line.indent > indent:
                    raise self.fail(line, "this line is indented deeper than the key before it "
                                          "allows; line it up with its siblings")
                if line.text == "-" or line.text.startswith("- "):
                    raise self.fail(line, "a '- item' sits among 'key: value' lines; put the "
                                          "list under a key")
            key, rest = _split_key(line, self.source)
            if key in out:
                raise self.fail(line, f"key {key!r} appears twice in one map; keep one")
            i = i + 1 if first is None else i
            first = None
            if rest:
                out[key] = _inline(rest, self.source, line.number, depth)
            else:
                out[key], i = self.child(i, indent, True, depth)
        return out, i

    def sequence(self, i: int, indent: int, depth: int) -> Tuple[List[Any], int]:
        out: List[Any] = []
        while i < len(self.lines):
            line = self.lines[i]
            if line.indent < indent:
                break
            if line.indent > indent:
                raise self.fail(line, "this line is indented deeper than the list before it "
                                      "allows; line it up with its siblings")
            if not (line.text == "-" or line.text.startswith("- ")):
                break
            item = line.text[1:].lstrip(" ")
            i += 1
            if not item:
                value, i = self.child(i, indent, False, depth)
                out.append(value)
            elif item[0] not in "[{\"'" and re.match(r"[^:]*?:(?: |$)", item):
                inner = _Line(line.number, indent + len(line.text) - len(item), item)
                value, i = self.mapping(i, inner.indent,
                                        _deeper(depth, self.source, line.number), first=inner)
                out.append(value)
            else:
                out.append(_inline(item, self.source, line.number, depth))
        return out, i


def loads(text: str, source: str = "<text>") -> Any:
    """Read one YAML document in the supported subset. Raises YamlError
    naming the source, the line and the fix. An empty document is None."""
    if not isinstance(text, str):
        raise TypeError(f"{source} is {type(text).__name__}; pass the YAML as text")
    lines = _lines(text, source)
    if not lines:
        return None
    first = lines[0]
    if first.indent != 0:
        raise _fail(source, first.number, "the first line is indented; start the document at "
                                          "the left edge")
    if first.text[0] in "[{\"'" or (not (first.text == "-" or first.text.startswith("- "))
                                     and not re.match(r"[^:]*?:(?: |$)", first.text)):
        value = _inline(first.text, source, first.number)
        if len(lines) > 1:
            raise _fail(source, lines[1].number, "text follows a complete value; a document "
                                                 "holds one map, list or value")
        return value
    value, i = _Block(lines, source).block(0, 0, 0)
    if i != len(lines):
        raise _fail(source, lines[i].number, "this line is indented less than the document "
                                             "allows; line it up with its siblings")
    return value
