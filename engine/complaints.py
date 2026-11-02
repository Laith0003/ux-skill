"""Complaints: what the person said is wrong with a page, each one written
as a probe the page is measured against, kept in .ux/complaints.json.

A complaint is closed only by measurement. Each has an id, the words the
person used (`said`) and a probe from a closed list:

  rule-clear    {"rule": id}       the lint or render check reports no
                                   finding of that rule on the page
  present       {"selector": css}  a visible element matches, at every width
  absent        {"selector": css}  no visible element matches, at any width
  text-present  {"text": words}    the visible text holds the words, at every width
  text-absent   {"text": words}    the visible text holds them at no width

Text is matched without regard to case or runs of white space. Widths are
the render check's: 390, 430, 768 and 1280 pixels.

check_complaints() measures a page (an HTML file, or an http or https URL,
which is loaded once, its scripts removed after they ran, and measured as
that snapshot) and gives each complaint a status: fixed, open, or weak. With
`before`, the page as it was when the person complained, every probe is run
there too, and a probe that already passes on it proves nothing: the
complaint stays open as weak until its probe is one the old page fails. The
check's status is passed when every complaint is fixed, else open.

snapshot_page() keeps the page as it is before it changes, for --before:
the running app's state is gone once the code changes.

Every run leaves .ux/complaints-last.json beside the complaints: the page,
a digest of it and of the complaints, and the ids still open, so a stop hook
can tell a stale or failing check without rendering anything.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import re
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

from engine.foundations.errors import InputError

DEFAULT_FILE = ".ux/complaints.json"
LAST_FILE = "complaints-last.json"
KINDS: Mapping[str, str] = {"rule-clear": "rule", "present": "selector", "absent": "selector",
                            "text-present": "text", "text-absent": "text"}
LABELS: Mapping[str, str] = {"file": "--file", "page": "--page", "before": "--before"}
SNAPSHOT_LABELS: Mapping[str, str] = {"page": "--page", "out": "--out", "force": "--force"}
_ID = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_URL = re.compile(r"^https?://", re.I)

_PROBE_JS = r"""(sels) => {
  const seen = el => {
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) return false;
    return el.checkVisibility ? el.checkVisibility({opacityProperty: true, visibilityProperty: true})
                              : getComputedStyle(el).visibility !== 'hidden';
  };
  const counts = {};
  for (const s of sels) {
    try { counts[s] = Array.from(document.querySelectorAll(s)).filter(seen).length; }
    catch (e) { counts[s] = null; }
  }
  return {text: document.body ? document.body.innerText : '', counts};
}"""

_SNAPSHOT_JS = r"""(url) => {
  document.querySelectorAll('script').forEach(s => s.remove());
  if (!document.querySelector('base')) {
    const b = document.createElement('base'); b.href = url;
    (document.head || document.documentElement).prepend(b);
  }
  return '<!doctype html>\n' + document.documentElement.outerHTML;
}"""


def _known_rules() -> set:
    from engine.linter.core import _REGION_RULE, _compile_rules
    from engine.render.core import _RULES
    return {r["id"] for r in _compile_rules() if r.get("id")} | set(_RULES) | {_REGION_RULE["id"]}


def load_complaints(path: Any, label: str = LABELS["file"]) -> List[Dict[str, Any]]:
    """The complaints in `path`, each checked: a unique id, the words said
    and a probe of a known kind with the one field that kind reads."""
    p = Path(path)
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise InputError(f"{label} {p} does not exist; write the complaints there as "
                         '{"complaints": [{"id": ..., "said": ..., "probe": {...}}]}') from None
    except (OSError, ValueError) as exc:
        raise InputError(f"{label} {p} is not readable JSON ({exc}); fix the file") from None
    items = data.get("complaints") if isinstance(data, dict) else None
    if not isinstance(items, list) or not items:
        raise InputError(f'{label} {p} has no "complaints" list; add one with at least one '
                         "complaint")
    rules: Optional[set] = None
    ids = set()
    out = []
    for n, c in enumerate(items):
        at = f"{p} complaints[{n}]"
        if not isinstance(c, dict):
            raise InputError(f"{at} is not an object; write it as "
                             '{"id": ..., "said": ..., "probe": {...}}')
        cid = c.get("id")
        if not isinstance(cid, str) or not _ID.match(cid):
            raise InputError(f"{at}.id is {cid!r}; give it a short id of lowercase letters, "
                             "digits and hyphens, such as cookie-banner")
        if cid in ids:
            raise InputError(f"{at}.id {cid!r} is used twice; give each complaint its own id")
        ids.add(cid)
        said = c.get("said")
        if not isinstance(said, str) or not said.strip():
            raise InputError(f"{at}.said is empty; write what the person said, in their words")
        probe = c.get("probe")
        if not isinstance(probe, dict):
            raise InputError(f"{at}.probe is missing; add one such as "
                             '{"kind": "rule-clear", "rule": "first-screen-covered"}')
        kind = probe.get("kind")
        if kind not in KINDS:
            raise InputError(f"{at}.probe.kind is {kind!r}; write one of "
                             f"{', '.join(KINDS)}")
        field = KINDS[kind]
        value = probe.get(field)
        if not isinstance(value, str) or not value.strip():
            raise InputError(f"{at}.probe.{field} is empty; a {kind} probe reads {field}")
        extra = sorted(set(probe) - {"kind", field})
        if extra:
            raise InputError(f"{at}.probe has {', '.join(extra)}, which a {kind} probe does not "
                             f"read; remove it or pick the kind that reads it")
        if kind == "rule-clear":
            rules = _known_rules() if rules is None else rules
            if value not in rules:
                raise InputError(f"{at}.probe.rule {value!r} is no lint or render rule; use an id "
                                 "uxskill lint reports, such as first-screen-covered")
        out.append({"id": cid, "said": said.strip(), "kind": kind, "value": value})
    return out


def _norm(text: str) -> str:
    return " ".join(text.split()).lower()


async def _snapshot(url: str, dest: Path) -> Path:
    from playwright.async_api import async_playwright
    from engine.render.core import _launch
    async with async_playwright() as pw:
        browser = await _launch(pw)
        try:
            page = await browser.new_page(viewport={"width": 1280, "height": 800})
            try:
                await page.goto(url, wait_until="load", timeout=30000)
            except Exception as exc:
                first = (str(exc).strip().splitlines() or [type(exc).__name__])[0][:160]
                raise InputError(f"{url} did not load ({first}); start the app or fix the "
                                 "URL") from None
            await page.wait_for_timeout(400)
            html = await page.evaluate(_SNAPSHOT_JS, url)
        finally:
            await browser.close()
    dest.write_text(html, encoding="utf-8")
    return dest


async def _dom(file: Path, sels: Sequence[str]) -> List[Dict[str, Any]]:
    from playwright.async_api import async_playwright
    from engine.render.core import VIEWPORTS, _launch
    out = []
    async with async_playwright() as pw:
        browser = await _launch(pw)
        try:
            for w, h in VIEWPORTS:
                page = await browser.new_page(viewport={"width": w, "height": h})
                try:
                    await page.goto(file.resolve().as_uri(), wait_until="load")
                    got = await page.evaluate(_PROBE_JS, list(sels))
                finally:
                    await page.close()
                out.append({"vw": w, "text": _norm(got["text"]), "counts": got["counts"]})
        finally:
            await browser.close()
    return out


def _measure(file: Path, complaints: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """Everything the probes read from one page: the visible text and the
    selector counts at every width, and the findings by rule."""
    from engine.render import RenderUnavailable
    from engine.render.core import _RULES
    try:
        sels = sorted({c["value"] for c in complaints if KINDS[c["kind"]] == "selector"})
        dom = asyncio.run(_dom(file, sels))
        findings: Dict[str, List[str]] = {}
        wanted = {c["value"] for c in complaints if c["kind"] == "rule-clear"}
        if wanted & set(_RULES):
            from engine.render import render_check
            for f in render_check([str(file)]).findings:
                findings.setdefault(f.rule_id, []).append(f.excerpt)
        if wanted - set(_RULES):
            from engine.linter.core import lint
            for f in lint([str(file)], severity_threshold="low").findings:
                findings.setdefault(f.rule_id, []).append(f"line {f.line}: {f.excerpt}")
    except ImportError:
        raise RenderUnavailable("Complaints are measured in a browser and need Playwright: "
                                "pip install 'uxskill[render]'") from None
    return {"dom": dom, "findings": findings}


def _bad_selectors(m: Mapping[str, Any], complaints, label: str) -> None:
    for c in complaints:
        if KINDS[c["kind"]] == "selector" and m["dom"][0]["counts"].get(c["value"]) is None:
            raise InputError(f"complaint {c['id']}: probe.selector {c['value']!r} is not a CSS "
                             f"selector the browser reads (on {label}); fix the selector")


def _verdict(c: Mapping[str, Any], m: Mapping[str, Any]) -> Tuple[bool, str]:
    """Whether the probe passes on the measured page, and what it saw."""
    kind, value, dom = c["kind"], c["value"], m["dom"]
    if kind == "rule-clear":
        hits = m["findings"].get(value, [])
        return (not hits, f"{value} not reported" if not hits
                else f"{value} reported {len(hits)} time(s), first: {hits[0]}")
    if kind in ("present", "absent"):
        counts = [(d["vw"], d["counts"][value]) for d in dom]
        if kind == "present":
            missing = [w for w, n in counts if not n]
            return (not missing, f"{value} visible at every width" if not missing
                    else f"no visible {value} at {', '.join(f'{w}px' for w in missing)}")
        shown = [f"{n} at {w}px" for w, n in counts if n]
        return (not shown, f"no visible {value}" if not shown
                else f"visible {value}: {', '.join(shown)}")
    words = _norm(value)
    where = [d["vw"] for d in dom if words in d["text"]]
    if kind == "text-present":
        missing = [d["vw"] for d in dom if d["vw"] not in where]
        return (not missing, f"{value!r} shown at every width" if not missing
                else f"{value!r} not shown at {', '.join(f'{w}px' for w in missing)}")
    return (not where, f"{value!r} not shown" if not where
            else f"{value!r} shown at {', '.join(f'{w}px' for w in where)}")


def _page_file(page: str, label: str, tmp: Path, name: str) -> Path:
    if _URL.match(page):
        try:
            return asyncio.run(_snapshot(page, tmp / f"{name}.html"))
        except ImportError:
            from engine.render import RenderUnavailable
            raise RenderUnavailable("A URL is loaded in a browser and needs Playwright: "
                                    "pip install 'uxskill[render]'") from None
    p = Path(page)
    if not p.is_file() or p.suffix.lower() not in (".html", ".htm"):
        raise InputError(f"{label} {page} is not an HTML file or an http(s) URL; pass the page "
                         "as built, such as dist/index.html, or the running app's URL")
    return p


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def check_complaints(page: Optional[str], *, file: Any = DEFAULT_FILE,
                     before: Optional[str] = None,
                     labels: Mapping[str, str] = LABELS) -> Dict[str, Any]:
    """Measure `page` against every complaint in `file`. Returns the status
    (passed or open), each complaint with its status and evidence, and the
    ids still open."""
    if not page:
        raise InputError(f"{labels['page']} is missing; pass the page to measure, an HTML file "
                         "or the running app's URL")
    complaints = load_complaints(file, labels["file"])
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        target = _page_file(page, labels["page"], tmp, "page")
        now = _measure(target, complaints)
        _bad_selectors(now, complaints, labels["page"])
        old = None
        if before:
            old = _measure(_page_file(before, labels["before"], tmp, "before"), complaints)
            _bad_selectors(old, complaints, labels["before"])
        local = not _URL.match(page)
        page_digest = _digest(target.read_bytes()) if local else ""
        page_path = str(target.resolve()) if local else ""
    rows = []
    for c in complaints:
        ok, seen = _verdict(c, now)
        status = "fixed" if ok else "open"
        row = {"id": c["id"], "said": c["said"], "probe": {"kind": c["kind"],
               KINDS[c["kind"]]: c["value"]}, "status": status, "evidence": seen}
        if old is not None:
            was, seen_before = _verdict(c, old)
            row["before"] = seen_before
            if was and ok:
                row["status"] = "weak"
                row["evidence"] += ("; it passed on the old page too, so it proves nothing: "
                                    "tighten the probe until the old page fails it")
        rows.append(row)
    still = [r["id"] for r in rows if r["status"] != "fixed"]
    result = {"status": "open" if still else "passed", "page": page, "complaints": rows,
              "open": still,
              "message": (f"{len(still)} of {len(rows)} complaint(s) still open: "
                          f"{', '.join(still)}; fix the page, then run the check again"
                          if still else f"all {len(rows)} complaint(s) fixed on {page}")}
    _record(Path(file), page, page_path, page_digest, still)
    return result


def snapshot_page(page: Optional[str], out: Any, *, force: bool = False,
                  labels: Mapping[str, str] = SNAPSHOT_LABELS) -> Dict[str, Any]:
    """Keep the page as it is now, before it changes, for --before: a URL
    loaded once with its scripts removed after they ran, or a copy of the
    file. A different file already at `out` is kept unless forced."""
    if not page:
        raise InputError(f"{labels['page']} is missing; pass the page to keep, an HTML file "
                         "or the running app's URL")
    if not out:
        raise InputError(f"{labels['out']} is missing; pass where to keep it, such as "
                         ".ux/before.html")
    dest = Path(out)
    with tempfile.TemporaryDirectory() as td:
        data = _page_file(page, labels["page"], Path(td), "snapshot").read_bytes()
    if dest.is_dir():
        raise InputError(f"{labels['out']} {dest} is a folder; name a file, such as "
                         f"{dest / 'before.html'}")
    if dest.is_file() and dest.read_bytes() != data and not force:
        return {"status": "refused", "page": page, "out": str(dest),
                "message": (f"{dest} already holds another page, so nothing was written; "
                            f"pass {labels['force']} to replace it, or another {labels['out']}")}
    status = "unchanged" if dest.is_file() and dest.read_bytes() == data else "written"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return {"status": status, "page": page, "out": str(dest),
            "message": f"kept {page} at {dest}; pass it to complaints check as --before"}


def _record(file: Path, page: str, page_path: str, page_digest: str,
            still: List[str]) -> None:
    """Leave the last result beside the complaints for the stop hook."""
    try:
        (file.parent / LAST_FILE).write_text(json.dumps({
            "page": page, "page_path": page_path, "page_digest": page_digest,
            "complaints_digest": _digest(file.read_bytes()), "open": still}, indent=2) + "\n",
            encoding="utf-8")
    except OSError:
        pass  # a read-only folder keeps the check's own result; only the hook loses it


def gate(root: Any = ".") -> Optional[str]:
    """Why the work is not done, or None. Read by the stop hook: complaints
    exist, and the last check is missing, ran on other complaints or another
    page, or left some open. Nothing here renders."""
    folder = Path(root) / ".ux"
    complaints = folder / "complaints.json"
    if not complaints.is_file():
        return None
    try:
        items = json.loads(complaints.read_text(encoding="utf-8")).get("complaints") or []
    except (OSError, ValueError, AttributeError):
        return (f"{complaints} is not readable JSON; fix it, then run "
                "uxskill complaints check --page <page>")
    if not items:
        return None
    run = "uxskill complaints check --page <page>"
    try:
        last = json.loads((folder / LAST_FILE).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return f"{len(items)} complaint(s) recorded and never checked; run {run}"
    if last.get("complaints_digest") != _digest(complaints.read_bytes()):
        return f"the complaints changed since the last check; run {run}"
    page = str(last.get("page") or "")
    if last.get("page_digest") and last.get("page_path"):
        p = Path(last["page_path"])
        if not p.is_file() or _digest(p.read_bytes()) != last["page_digest"]:
            return f"{page} changed since the last check; run uxskill complaints check --page {page}"
    if last.get("open"):
        return (f"complaint(s) still open on {page}: {', '.join(last['open'])}; fix them and "
                f"run uxskill complaints check --page {page}")
    return None
