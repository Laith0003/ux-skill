"""Read a project's Tailwind theme as text, never run: a Tailwind 3 config
(tailwind.config.js, .cjs, .mjs or .ts) with the presets it names, and a
Tailwind 4 @theme block in any stylesheet.

A config is read statically: the object literal it exports (module.exports
= {...}, export default {...}, defineConfig({...}), or a name bound to one
of them), its presets (require('./preset') or an import of a file in the
project, followed to their own object literals), and each theme namespace,
in theme (which replaces what a preset set there) and theme.extend (which
adds to it). A name maps to a value: var(--x) names the custom property x,
so the utility it produces reaches that token; a string, a number or the
first member of a list is a value as written. Nested names flatten the way
Tailwind names its utilities: ink: { DEFAULT, muted } gives ink and
ink-muted.

Nothing is executed. What cannot be read from the text alone (a function
call, a spread, a computed key, a name bound to something other than a
literal, a preset from a package) is listed in not_read with its file,
line and how to write it so it is read, never guessed.

A Tailwind 4 @theme block maps its own names: --color-canvas:
var(--brand-canvas) makes bg-canvas reach --brand-canvas.
"""
from __future__ import annotations

import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from engine.foundations.errors import InputError

CONFIG_SUFFIXES = (".js", ".cjs", ".mjs", ".ts", ".cts", ".mts")
_CONFIG = re.compile(r"^tailwind\.config\.(?:js|cjs|mjs|ts|cts|mts)$")
_SKIP = frozenset(("node_modules", ".git", "dist", "build", "vendor", ".next", "out",
                   "coverage", ".uxskill"))
_MAX_DEPTH = 4
_MAX_UP = 6
# Tailwind 4's theme namespaces: a variable in one of them makes utilities.
# The one list the reader here and the exporter (tailwind_out) share.
# Longest first, so --font-weight-bold is font-weight and --font-display
# is font, --text-shadow-soft is text-shadow and --text-body is text. A
# duration is in none: Tailwind's duration utilities take a number, and
# no theme variable makes one.
NAMESPACES: Tuple[str, ...] = (
    "font-weight", "inset-shadow", "drop-shadow", "text-shadow", "color", "font", "text",
    "tracking", "leading", "breakpoint", "container", "spacing", "radius", "shadow", "blur",
    "perspective", "aspect", "ease", "animate")
_VAR = re.compile(r"^var\(\s*--([A-Za-z0-9_-]+)\s*(?:,[^)]*)?\)$")
_WHY_COMPUTED = ("is computed in JavaScript, so its value is not read; write it as a string, "
                 "such as 'var(--x)' or '#0B5F4A', so the theme can be read without running "
                 "the config")
_WHY_SPREAD = ("spreads another object into the theme, so what it brings is not read; write "
               "those names out, each as a string such as 'var(--x)'")
_WHY_PACKAGE = ("is a preset from a package, which is not read here; copy its theme names into "
                "the config, each as a string such as 'var(--x)', to have them read")
_WHY_MISSING = ("names a preset file that could not be found; fix the path, or copy its theme "
                "into the config")
_WHY_EXPORT = ("exports no object literal that can be read without running it; write the "
               "config as module.exports = { ... } or export default { ... }")


@dataclass(frozen=True)
class ThemeEntry:
    """One name a theme namespace maps: the value as written, the custom
    property it names ("" for a plain value), and where it is written."""
    namespace: str
    name: str
    value: str
    var: str
    file: str
    line: int


@dataclass
class ThemeMap:
    """(namespace, name) -> entry, the files read, what was not read as
    (file, line, text, why), and the namespaces the theme replaces, in the
    order read: a Tailwind 3 theme key set outside extend (spacing), or a
    Tailwind 4 reset (--spacing-*: initial; "*" for --*: initial), so
    Tailwind's own values in it are gone."""
    entries: Dict[Tuple[str, str], ThemeEntry] = field(default_factory=dict)
    files: List[str] = field(default_factory=list)
    not_read: List[Tuple[str, int, str, str]] = field(default_factory=list)
    replaced: List[str] = field(default_factory=list)

    def keeps(self, namespace: str) -> bool:
        """Whether Tailwind's own values in a namespace still apply: a
        theme was read (a config or an @theme block) and it does not
        replace the namespace."""
        return bool(self.files) and not {namespace, "*"} & set(self.replaced)

    def get(self, namespace: str, name: str) -> Optional[ThemeEntry]:
        return self.entries.get((namespace, name))

    def names_for(self, var: str) -> List[Tuple[str, str]]:
        """Every (namespace, name) whose value is var(--`var`)."""
        return [k for k, e in self.entries.items() if e.var == var]

    def __bool__(self) -> bool:
        return bool(self.entries or self.not_read)


# ---------------------------------------------------------------- JS text


@dataclass(frozen=True)
class _Tok:
    kind: str   # str, num, name, punct
    text: str
    pos: int


_TOKEN = re.compile(r"""
    (?P<ws>\s+)
  | (?P<comment>//[^\n]*|/\*.*?\*/)
  | (?P<str>"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|`(?:[^`\\]|\\.)*`)
  | (?P<num>-?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)
  | (?P<name>[A-Za-z_$][\w$]*)
  | (?P<punct>\.\.\.|=>|[{}\[\](),:;=.?!<>+*/|&-])
  | (?P<other>.)
""", re.S | re.X)


def _tokens(text: str) -> List[_Tok]:
    out = []
    for m in _TOKEN.finditer(text):
        kind = m.lastgroup
        if kind in ("ws", "comment"):
            continue
        out.append(_Tok(kind or "other", m.group(0), m.start()))
    return out


def _unquote(text: str) -> Optional[str]:
    """A string literal's text, or None for a template with ${}."""
    body = text[1:-1]
    if text[0] == "`" and "${" in body:
        return None
    return re.sub(r"\\(.)", r"\1", body)


class _Computed:
    """A value that cannot be read without running the code."""

    def __init__(self, text: str, pos: int, why: str = _WHY_COMPUTED) -> None:
        self.text, self.pos, self.why = text, pos, why


class _Require:
    def __init__(self, ref: str, pos: int) -> None:
        self.ref, self.pos = ref, pos


class _Name:
    def __init__(self, name: str, pos: int) -> None:
        self.name, self.pos = name, pos


class _Obj:
    """An object literal: its members in order, each (key, value, pos); a
    spread or computed key is kept as a _Computed member."""

    def __init__(self, pos: int) -> None:
        self.pos = pos
        self.members: List[Tuple[Optional[str], Any, int]] = []


class _Parser:
    def __init__(self, text: str) -> None:
        self.text = text
        self.toks = _tokens(text)
        self.i = 0

    def peek(self, k: int = 0) -> Optional[_Tok]:
        j = self.i + k
        return self.toks[j] if j < len(self.toks) else None

    def next(self) -> Optional[_Tok]:
        t = self.peek()
        self.i += 1
        return t

    def at(self, text: str, k: int = 0) -> bool:
        t = self.peek(k)
        return t is not None and t.text == text

    def skip_expr(self) -> int:
        """Past one expression up to a top-level , ; } ] or ); the end offset."""
        depth = 0
        end = len(self.text)
        while self.peek() is not None:
            t = self.peek()
            if t.text in "([{" and t.kind == "punct":
                depth += 1
            elif t.text in ")]}" and t.kind == "punct":
                if depth == 0:
                    end = t.pos
                    break
                depth -= 1
            elif t.text in (",", ";") and depth == 0:
                end = t.pos
                break
            self.i += 1
        return end

    def value(self) -> Any:
        start = self.peek()
        if start is None:
            return _Computed("", len(self.text))
        begin = self.i
        v = self._value()
        # Anything after a value inside the expression (a call on it, an
        # operator, `as const`, `satisfies Config`) makes it computed, save
        # the TypeScript annotations that leave the value as it is.
        t = self.peek()
        prev = self.toks[self.i - 1]
        if t is not None and t.kind == "name" and t.text not in ("as", "satisfies") \
                and "\n" in self.text[prev.pos + len(prev.text):t.pos]:
            return v   # a new statement on the next line, with no semicolon
        if t is not None and t.kind == "name" and t.text in ("as", "satisfies") \
                and not isinstance(v, _Computed):
            self.i += 1
            self.skip_expr()
            return v
        if t is not None and not (t.text in (",", ";", "}", "]", ")") and t.kind == "punct"):
            self.i = begin
            end = self.skip_expr()
            return _Computed(self.text[start.pos:end].strip(), start.pos)
        return v

    def _value(self) -> Any:
        ti = self.i
        t = self.next()
        if t.kind == "str":
            text = _unquote(t.text)
            return _Computed(t.text, t.pos) if text is None else text
        if t.kind == "num":
            return float(t.text) if "." in t.text or "e" in t.text.lower() else int(t.text)
        if t.text == "{":
            return self.obj(t.pos)
        if t.text == "[":
            return self.arr(t.pos)
        if t.kind == "name" and t.text == "require" and self.at("("):
            self.next()
            ref = self.peek()
            if ref is not None and ref.kind == "str" and self.at(")", 1):
                self.next()
                self.next()
                return _Require(_unquote(ref.text) or "", t.pos)
            self.i = ti
            end = self.skip_expr()
            return _Computed(self.text[t.pos:end].strip(), t.pos)
        if t.kind == "name" and t.text in ("true", "false", "null", "undefined"):
            return t.text
        if t.kind == "name" and not self.at("(") and not self.at(".") and not self.at("=>"):
            return _Name(t.text, t.pos)
        self.i -= 1
        end = self.skip_expr()
        return _Computed(self.text[t.pos:end].strip(), t.pos)

    def obj(self, pos: int) -> _Obj:
        o = _Obj(pos)
        while self.peek() is not None and not self.at("}"):
            t = self.peek()
            if t.text == "...":
                self.next()
                end = self.skip_expr()
                o.members.append((None, _Computed(self.text[t.pos:end].strip(), t.pos,
                                                  _WHY_SPREAD), t.pos))
            elif t.text == "[":
                end = self.skip_expr()
                o.members.append((None, _Computed(self.text[t.pos:end].strip(), t.pos),
                                  t.pos))
            elif t.kind in ("name", "str", "num"):
                key = _unquote(t.text) if t.kind == "str" else t.text
                self.next()
                if self.at(":"):
                    self.next()
                    o.members.append((key, self.value(), t.pos))
                elif self.at("("):   # a method
                    self.i -= 1
                    end = self.skip_expr()
                    o.members.append((key, _Computed(self.text[t.pos:end].strip(), t.pos),
                                      t.pos))
                else:                 # shorthand { colors }
                    o.members.append((key, _Name(t.text, t.pos), t.pos))
            else:
                self.next()
                continue
            if self.at(","):
                self.next()
        self.next()
        return o

    def arr(self, pos: int) -> List[Any]:
        out: List[Any] = []
        while self.peek() is not None and not self.at("]"):
            if self.at(","):
                self.next()
                continue
            t = self.peek()
            if t.text == "...":
                self.next()
                end = self.skip_expr()
                out.append(_Computed(self.text[t.pos:end].strip(), t.pos, _WHY_SPREAD))
                continue
            out.append(self.value())
        self.next()
        return out


def _module(text: str) -> Tuple[Any, Dict[str, Any]]:
    """(what the file exports, the names it binds at the top level to a
    value, a require() or an import)."""
    p = _Parser(text)
    names: Dict[str, Any] = {}
    exported: Any = None
    while p.peek() is not None:
        t = p.peek()
        if t.kind == "name" and t.text in ("const", "let", "var") and p.peek(1) is not None \
                and p.peek(1).kind == "name" and p.at("=", 2):
            name = p.peek(1).text
            p.i += 3
            names[name] = p.value()
            continue
        if t.kind == "name" and t.text == "import":
            m = re.match(r"import\s+([A-Za-z_$][\w$]*)\s+from\s+(['\"])([^'\"]+)\2",
                         text[t.pos:])
            if m:
                names[m.group(1)] = _Require(m.group(3), t.pos)
            p.i += 1
            continue
        if t.kind == "name" and t.text == "module" and p.at(".", 1) and p.at("exports", 2) \
                and p.at("=", 3):
            p.i += 4
            exported = p.value()
            continue
        if t.kind == "name" and t.text == "export" and p.at("default", 1):
            p.i += 2
            exported = p.value()
            continue
        p.i += 1
    if isinstance(exported, _Computed):
        m = re.match(r"[A-Za-z_$][\w$.]*\s*\(\s*", exported.text)
        if m and exported.text.endswith(")"):   # defineConfig({...}) or a wrapper
            # Read from the brace in the whole text, so lines stay the file's.
            brace = exported.pos + m.end()
            at = next((k for k, t in enumerate(p.toks) if t.pos == brace), None)
            if at is not None and p.toks[at].text == "{":
                p.i = at + 1
                return p.obj(brace), names
    return exported, names


# ---------------------------------------------------------------- reading


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _resolve_file(ref: str, near: Path) -> Optional[Path]:
    base = near.parent / ref
    for cand in [base, *(base.with_name(base.name + s) for s in CONFIG_SUFFIXES),
                 *(base / f"index{s}" for s in CONFIG_SUFFIXES)]:
        try:
            if cand.is_file():
                return cand.resolve()
        except OSError:
            continue
    return None


class _Reader:
    def __init__(self, label: Any) -> None:
        self.label = label
        self.out = ThemeMap()
        self.seen: set = set()

    def config(self, path: Path) -> None:
        """Read one config and its presets into out."""
        theme = self.theme_of(path)
        if theme is None:
            return
        for ns, (replace, entries) in theme.items():
            if replace:
                self.out.entries = {k: v for k, v in self.out.entries.items() if k[0] != ns}
                if ns not in self.out.replaced:
                    self.out.replaced.append(ns)
            for e in entries:
                self.out.entries[(ns, e.name)] = e

    def theme_of(self, path: Path, depth: int = 0
                 ) -> Optional[Dict[str, Tuple[bool, List[ThemeEntry]]]]:
        """namespace -> (whether it replaces, its entries) for one config
        file, presets first."""
        key = str(path.resolve())
        if key in self.seen or depth > 4:
            return None
        self.seen.add(key)
        try:
            if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > 1_000_000:
                return None
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            return None
        name = self.label(path)
        self.out.files.append(name)
        exported, names = _module(text)
        exported = self.bound(exported, names)
        if not isinstance(exported, _Obj):
            if exported is not None:
                self.out.not_read.append((name, 1, "the config", _WHY_EXPORT))
            return None
        merged: Dict[str, Tuple[bool, List[ThemeEntry]]] = {}
        members = {k: (v, pos) for k, v, pos in exported.members if k is not None}
        presets = members.get("presets")
        if presets is not None:
            listed = self.bound(presets[0], names)
            for item in listed if isinstance(listed, list) else [listed]:
                self.preset(item, names, path, text, name, merged, depth)
        theme = members.get("theme")
        if theme is not None:
            obj = self.bound(theme[0], names)
            if isinstance(obj, _Obj):
                for ns, v, pos in obj.members:
                    if ns is None:
                        self.not_read(name, text, v)
                    elif ns == "extend":
                        ext = self.bound(v, names)
                        if isinstance(ext, _Obj):
                            for ens, ev, epos in ext.members:
                                if ens is None:
                                    self.not_read(name, text, ev)
                                    continue
                                got = self.namespace(ens, ev, names, name, text)
                                had = merged.get(ens, (False, []))
                                merged[ens] = (had[0], had[1] + got)
                        else:
                            self.not_read(name, text, ext)
                    else:
                        merged[ns] = (True, self.namespace(ns, v, names, name, text))
            else:
                self.not_read(name, text, obj)
        return merged

    def preset(self, item: Any, names: Dict[str, Any], near: Path, text: str, name: str,
               merged: Dict[str, Tuple[bool, List[ThemeEntry]]], depth: int) -> None:
        item = self.bound(item, names)
        if isinstance(item, _Require):
            if not item.ref.startswith("."):
                self.out.not_read.append((name, _line(text, item.pos),
                                          f"preset {item.ref}", _WHY_PACKAGE))
                return
            found = _resolve_file(item.ref, near)
            if found is None:
                self.out.not_read.append((name, _line(text, item.pos),
                                          f"preset {item.ref}", _WHY_MISSING))
                return
            got = self.theme_of(found, depth + 1)
            for ns, (replace, entries) in (got or {}).items():
                if replace or ns not in merged:
                    merged[ns] = (replace, list(entries))
                else:
                    merged[ns] = (merged[ns][0], merged[ns][1] + entries)
        elif isinstance(item, _Obj):
            self.out.not_read.append((name, _line(text, item.pos), "an inline preset",
                                      "is written in the config; move it into a file of its "
                                      "own and name it with require() to have it read"))
        else:
            self.not_read(name, text, item)

    @staticmethod
    def bound(value: Any, names: Dict[str, Any]) -> Any:
        seen = 0
        while isinstance(value, _Name) and value.name in names and seen < 8:
            value = names[value.name]
            seen += 1
        return value

    def not_read(self, name: str, text: str, value: Any) -> None:
        if isinstance(value, _Computed):
            shown = " ".join(value.text.split())
            shown = shown if len(shown) <= 80 else shown[:77] + "..."
            self.out.not_read.append((name, _line(text, value.pos), shown, value.why))
        elif isinstance(value, _Name):
            self.out.not_read.append((name, _line(text, value.pos), value.name, (
                "is a name bound to a value this reader cannot follow; write the value out, "
                "such as 'var(--x)'")))

    def namespace(self, ns: str, value: Any, names: Dict[str, Any], name: str,
                  text: str, prefix: str = "") -> List[ThemeEntry]:
        value = self.bound(value, names)
        out: List[ThemeEntry] = []
        if not isinstance(value, _Obj):
            self.not_read(name, text, value)
            return out
        for key, v, pos in value.members:
            if key is None:
                self.not_read(name, text, v)
                continue
            full = prefix if key == "DEFAULT" and prefix else (
                f"{prefix}-{key}" if prefix else key)
            v = self.bound(v, names)
            if isinstance(v, _Obj) and ns not in ("fontSize",):
                out += self.namespace(ns, v, names, name, text, full)
                continue
            first = v[0] if isinstance(v, list) and v else v
            if isinstance(first, (int, float)) and not isinstance(first, bool):
                first = f"{first:g}"
            if isinstance(first, str):
                m = _VAR.match(first.strip())
                out.append(ThemeEntry(ns, full, first.strip(), m.group(1) if m else "", name,
                                      _line(text, pos)))
            else:
                self.not_read(name, text, first if isinstance(first, (_Computed, _Name))
                              else _Computed(str(first), pos))
        return out


def _theme_blocks(path: Path, label: str, out: ThemeMap) -> None:
    """Names a Tailwind 4 @theme block in a stylesheet maps. Only a regular
    file is opened: a pipe named like a stylesheet would never answer."""
    try:
        if not stat.S_ISREG(path.stat().st_mode) or path.stat().st_size > 1_000_000:
            return
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return
    if "@theme" not in text:
        return
    from engine.io.css_in import parse_css
    try:
        rules = parse_css(text, path.name)
    except (InputError, ValueError):  # a stylesheet that does not parse is the scanner's
        return
    read = False
    for rule in rules:
        if rule.selector != "@theme":
            continue
        for d in rule.declarations:
            prop = d.name[2:]
            ns = next((n for n in NAMESPACES if prop.startswith(n + "-")), "")
            if prop == "*" or (ns and prop == ns + "-*"):
                # A reset clears Tailwind's own values in the namespace.
                if d.value.strip() == "initial" and (ns or "*") not in out.replaced:
                    out.replaced.append(ns or "*")
                read = True
                continue
            if not ns:
                continue
            name = prop[len(ns) + 1:]
            m = _VAR.match(d.value.strip())
            out.entries.setdefault((ns, name), ThemeEntry(ns, name, d.value.strip(),
                                                          m.group(1) if m else "", label,
                                                          d.line))
            read = True
    if read and label not in out.files:
        out.files.append(label)


def find_configs(roots: Sequence[Any]) -> List[Path]:
    """Tailwind 3 configs for code under `roots`: in each root and the
    folders above it up to the project's own (the first holding
    package.json or .git), and inside each root to a few levels."""
    found: List[Path] = []

    def add(p: Path) -> None:
        r = p.resolve()
        if r not in found:
            found.append(r)

    for root in roots:
        r = Path(root).expanduser().resolve()
        folder = r if r.is_dir() else r.parent
        for _ in range(_MAX_UP):
            try:
                for child in sorted(folder.iterdir()):
                    if child.is_file() and _CONFIG.match(child.name):
                        add(child)
            except OSError:
                break
            if (folder / "package.json").is_file() or (folder / ".git").exists() \
                    or folder.parent == folder:
                break
            folder = folder.parent
        if r.is_dir():
            base_depth = len(r.parts)
            for dirpath, dirnames, filenames in os.walk(r):
                dirnames[:] = sorted(d for d in dirnames
                                     if d not in _SKIP and not d.startswith("."))
                if len(Path(dirpath).parts) - base_depth >= _MAX_DEPTH:
                    dirnames[:] = []
                for f in sorted(filenames):
                    if _CONFIG.match(f):
                        add(Path(dirpath) / f)
    return found


def read_theme(roots: Sequence[Any], sheets: Iterable[Any] = (),
               base: Optional[Any] = None) -> ThemeMap:
    """The Tailwind theme the code under `roots` is written against: every
    config found (find_configs) with its presets, then each @theme block in
    `sheets`. Files are named relative to `base` (the folder the roots
    share when not given)."""
    rs = [Path(r).expanduser().resolve() for r in roots]
    if base is None:
        dirs = [r if r.is_dir() else r.parent for r in rs]
        base = Path(os.path.commonpath([str(d) for d in dirs])) if dirs else Path(".")
    base = Path(base).resolve()

    def label(p: Path) -> str:
        try:
            return Path(os.path.relpath(p.resolve(), base)).as_posix()
        except ValueError:
            return p.name

    reader = _Reader(label)
    for cfg in find_configs(rs):
        reader.config(cfg)
    for sheet in sheets:
        p = Path(sheet)
        _theme_blocks(p, label(p), reader.out)
    return reader.out
