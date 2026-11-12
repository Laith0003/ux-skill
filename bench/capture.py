"""Freeze a designer-built page into bench/pages/<id>/ (or bench/private/<id>/).

Each source in sources.json names a url (or a zip and the member to read),
its licence and whether it may be redistributed. Capture keeps the page's
HTML as served, with three recorded changes so it replays offline:

1. Stylesheet links are rewritten to local copies in pages/_css/, named by
   content hash so a framework file shared by many pages is stored once. A
   stylesheet whose file name matches the source's ``vendor`` patterns
   (default: anything with ``.min.`` in its name, or served from another
   host) is listed as vendor and only read by the render pass; the rest is
   the page's own CSS and is linted with the page.
2. ``integrity`` and ``crossorigin`` are dropped from rewritten links, since
   subresource integrity cannot be checked on a file url.
3. Anything matched by the source's ``strip`` patterns is removed (logos and
   crests a licence excludes).

Every script element, inline or external, is removed from the stored page.
Images and fonts are not stored. The render pass blocks the network,
so every run sees the same page: no scripts from other hosts, no remote
images, fallback fonts. The manifest records this per page.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import io
import json
import re
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from bench import BENCH, PAGES, PRIVATE

UA = "Mozilla/5.0 (ux-bench capture; +https://github.com/Laith0003/ux-skill)"
SOURCES = BENCH / "sources.json"
_LINK = re.compile(r"<link\b[^>]*>", re.I)
_ATTR = re.compile(r'\s(integrity|crossorigin)(=("[^"]*"|\'[^\']*\'|[^\s>]*))?', re.I)


class CaptureError(RuntimeError):
    """A source could not be fetched or frozen; the message names the source and the fix."""


def fetch(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (fixed sources)
            return resp.read()
    except Exception as exc:
        raise CaptureError(f"fetch {url} failed: {exc}; check the url in sources.json") from exc


def _href(tag: str) -> Optional[str]:
    m = re.search(r'\shref=("([^"]*)"|\'([^\']*)\'|([^\s>]+))', tag, re.I)
    if not m:
        return None
    return m.group(2) or m.group(3) or m.group(4)


def _is_stylesheet(tag: str) -> bool:
    return bool(re.search(r'\srel=("|\')?[^"\'>]*stylesheet', tag, re.I))


def _vendor(css_url: str, page_url: str, patterns: List[str]) -> bool:
    host = urllib.parse.urlparse(css_url).netloc
    if host and host != urllib.parse.urlparse(page_url).netloc:
        return True
    name = Path(urllib.parse.urlparse(css_url).path).name
    pats = patterns or [r"\.min\."]
    return any(re.search(p, name) for p in pats)


_SCRIPT = re.compile(r"<script\b[^>]*>.*?</script\s*>|<script\b[^>]*/>", re.S | re.I)


def strip_scripts(html: str) -> Tuple[str, int]:
    """Every script element removed, inline and external, so a stored page
    can never load or run third-party code (tag managers, analytics, CDNs)."""
    return _SCRIPT.subn("", html)


def css_name(url: str, body: bytes) -> str:
    """The stored name of a stylesheet: a content hash and its own name."""
    base = Path(urllib.parse.urlparse(url).path).name or "style.css"
    base = re.sub(r"[^A-Za-z0-9._-]", "_", base)[-40:]
    if not base.endswith(".css"):
        base += ".css"
    return f"{hashlib.sha256(body).hexdigest()[:12]}-{base}"


def freeze_html(
    html: str, page_url: str, source: Dict[str, Any], get=fetch
) -> Tuple[str, Dict[str, bytes], Dict[str, List[str]], List[str]]:
    """The frozen HTML, the stylesheet files to write (stored name to
    bytes), which of them are the page's own and which vendor, and the
    notes on what changed."""
    files: Dict[str, bytes] = {}
    roles: Dict[str, List[str]] = {"own": [], "vendor": []}
    notes: List[str] = []

    def swap(m: "re.Match[str]") -> str:
        tag = m.group(0)
        href = _href(tag)
        if not href or not _is_stylesheet(tag) or href.startswith("data:"):
            return tag
        css_url = urllib.parse.urljoin(page_url, href)
        if "fonts.googleapis.com" in css_url or "use.typekit" in css_url:
            notes.append(f"font stylesheet left remote and blocked at render: {css_url}")
            return tag
        try:
            body = get(css_url)
        except CaptureError as exc:
            notes.append(f"stylesheet not stored: {exc}")
            return tag
        role = "vendor" if _vendor(css_url, page_url, source.get("vendor", [])) else "own"
        name = css_name(css_url, body)
        files[name] = body
        if name not in roles[role]:
            roles[role].append(name)
        new = tag.replace(href, "../_css/" + name, 1)
        new = _ATTR.sub("", new)
        return new

    out = _LINK.sub(swap, html)
    for pat in source.get("strip", []):
        out, n = re.subn(pat, "", out, flags=re.S | re.I)
        notes.append(f"removed {n} match(es) of {pat!r}: {source.get('strip_reason', 'licence')}")
    out, n_scripts = strip_scripts(out)
    if n_scripts:
        notes.append(f"removed {n_scripts} script element(s), inline and external")
    notes.append("images and web fonts not stored; render runs with the network blocked")
    return out, files, roles, notes


def files_sha256(base: Path, rels: List[str]) -> str:
    """sha256 over the page's stored files, path and bytes, in sorted order."""
    h = hashlib.sha256()
    for rel in sorted(rels):
        h.update(rel.encode())
        h.update(b"\0")
        h.update((base / rel).read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def _zip_member(source: Dict[str, Any]) -> Tuple[str, Dict[str, bytes]]:
    blob = fetch(source["zip"])
    zf = zipfile.ZipFile(io.BytesIO(blob))
    names = zf.namelist()
    member = source.get("member", "index.html")
    if member not in names:
        raise CaptureError(
            f"{source['id']}: {member} is not in {source['zip']}; set member to one of {names[:8]}"
        )
    html = zf.read(member).decode("utf-8", errors="replace")
    css = {n: zf.read(n) for n in names if n.endswith(".css")}
    return html, css


def capture(source: Dict[str, Any], today: Optional[str] = None) -> Dict[str, Any]:
    """Freeze one source and return its manifest entry."""
    sid = source["id"]
    base = PAGES if source["redistributable"] else PRIVATE
    dest = base / sid
    dest.mkdir(parents=True, exist_ok=True)
    for old in dest.iterdir():
        if old.is_file():
            old.unlink()
    url = source["url"]
    if "zip" in source:
        html, zipped = _zip_member(source)
        folder = Path(source.get("member", "index.html")).parent

        def get_zip(css_url: str) -> bytes:
            rel = urllib.parse.urlparse(css_url).path.lstrip("/")
            key = (folder / rel).as_posix() if str(folder) != "." else rel
            if key not in zipped:
                raise CaptureError(f"{key} is not in {source['zip']}")
            return zipped[key]

        html, files, roles, notes = freeze_html(html, "http://zip.local/", source, get=get_zip)
    else:
        html = fetch(url).decode("utf-8", errors="replace")
        html, files, roles, notes = freeze_html(html, url, source)
    (dest / "index.html").write_text(html, encoding="utf-8")
    (base / "_css").mkdir(parents=True, exist_ok=True)
    for name, body in files.items():
        (base / "_css" / name).write_bytes(body)
    stored = {
        "html": f"{sid}/index.html",
        "own": [f"_css/{n}" for n in roles["own"]],
        "vendor": [f"_css/{n}" for n in roles["vendor"]],
    }
    entry = {
        k: source[k]
        for k in (
            "id",
            "origin",
            "licence",
            "attribution",
            "redistributable",
            "url",
            "page_type",
            "direction",
            "split",
        )
        if k in source
    }
    entry.update(
        {
            "storage": "A" if source["redistributable"] else "B",
            "capture_date": today or _dt.date.today().isoformat(),
            "files": stored,
            "sha256": files_sha256(base, [stored["html"], *stored["own"], *stored["vendor"]]),
            "notes": notes,
        }
    )
    return entry


def load_sources() -> List[Dict[str, Any]]:
    return json.loads(SOURCES.read_text(encoding="utf-8"))["sources"]
