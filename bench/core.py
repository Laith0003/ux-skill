"""Run the engine over the corpus or the seeded set and key every finding.

A finding's key is the page, the pass (static or render), the rule, the file
(relative to the page store), the line and a short hash of the excerpt, with
an occurrence number when the same rule fires twice on one line with the
same excerpt. Pages are frozen, so the key of a finding is stable across
runs and engine versions; labels and goldens are stored by key.

The render pass blocks every request that is not a file url, so a page
renders the same way on every run whatever the network does.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

from bench import EXPECTED, OUT, PAGES, PRIVATE, ROOT, SEEDED
from bench import manifest as mf


def default_out(seeded: bool = False) -> Path:
    return OUT / ("seeded.json" if seeded else "run.json")


def engine_version() -> Dict[str, str]:
    import engine

    root = Path(engine.__file__).resolve().parent.parent
    try:
        rev = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=10,
        ).stdout.strip()
    except Exception:  # not a git checkout
        rev = ""
    rules = root / "data" / "anti-patterns.json"
    digest = hashlib.sha256(rules.read_bytes()).hexdigest()[:12] if rules.exists() else ""
    return {
        "engine_root": str(root),
        "git": rev,
        "anti_patterns_sha256": digest,
        "python": platform.python_version(),
    }


def _excerpt_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8", "replace")).hexdigest()[:10]


def identity(f: Dict[str, Any]) -> str:
    """What makes two findings the same finding. A static finding is its
    excerpt. A render finding is its element (the selector before the first
    ': '), because its message carries measured values, such as a time in
    milliseconds, that move between runs on the same page."""
    if f["pass"] == "render":
        return f["excerpt"].split(": ", 1)[0]
    return f["excerpt"]


def key_findings(page_id: str, findings: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Give every finding its stable key, in a stable order."""
    rows = sorted(
        findings,
        key=lambda f: (f["pass"], f["rule"], f["file"], f["line"], identity(f), f["excerpt"]),
    )
    seen: Dict[str, int] = {}
    out = []
    for f in rows:
        base = "|".join(
            [page_id, f["pass"], f["rule"], f["file"], str(f["line"]), _excerpt_hash(identity(f))]
        )
        seen[base] = seen.get(base, 0) + 1
        out.append({**f, "key": f"{base}#{seen[base]}"})
    return out


def _rel(path: str, bases: Tuple[Path, ...]) -> str:
    p = Path(path).resolve()
    for b in bases:
        try:
            return p.relative_to(b.resolve()).as_posix()
        except ValueError:
            continue
    return p.name


def _norm(f: Any, pass_: str, bases: Tuple[Path, ...]) -> Dict[str, Any]:
    return {
        "pass": pass_,
        "rule": f.rule_id,
        "severity": f.severity,
        "category": f.category,
        "file": _rel(f.file, bases),
        "line": int(f.line),
        "column": int(f.column or 0),
        "excerpt": f.excerpt[:300],
    }


def static_findings(paths: List[Path], bases: Tuple[Path, ...]) -> List[Dict[str, Any]]:
    from engine.linter.core import lint

    report = lint([str(p) for p in paths], severity_threshold="critical")
    return [_norm(f, "static", bases) for f in report.findings]


class _Blocked:
    """A browser whose pages abort every request that is not a file url."""

    def __init__(self, browser: Any):
        self._b = browser

    def __getattr__(self, name: str) -> Any:
        return getattr(self._b, name)

    async def new_page(self, *a: Any, **kw: Any) -> Any:
        page = await self._b.new_page(*a, **kw)

        async def gate(route: Any) -> None:
            if route.request.url.startswith(("file:", "data:", "about:", "blob:")):
                await route.continue_()
            else:
                await route.abort()

        await page.route("**/*", gate)
        return page


def render_available() -> Optional[str]:
    """None when the render pass can run, else the reason it cannot."""
    try:
        import playwright  # noqa: F401
    except ImportError:
        return "Playwright is not installed: pip install 'uxskill[render]'"
    return None


def render_findings(html: Path, bases: Tuple[Path, ...]) -> Tuple[List[Dict[str, Any]], str]:
    """Render findings for one page, and an error string ('' on success)."""
    from engine.render import core as rc

    original = rc._launch

    async def launch(pw: Any, *a: Any, **kw: Any) -> Any:
        return _Blocked(await original(pw, *a, **kw))

    rc._launch = launch
    try:
        report = rc.render_check([str(html)], severity_threshold="critical")
    except Exception as exc:  # RenderUnavailable or a crash in the pass itself
        return [], f"{type(exc).__name__}: {str(exc).splitlines()[0][:200] if str(exc) else ''}"
    finally:
        rc._launch = original
    return [_norm(f, "render", bases) for f in report.findings], ""


def _page_inputs(entry: Dict[str, Any]) -> Tuple[Path, List[Path], Tuple[Path, ...]]:
    base = PAGES if entry["redistributable"] else PRIVATE
    files = entry.get("files") or {"html": f"{entry['id']}/index.html", "own": []}
    html = base / files["html"]
    own = [base / rel for rel in files.get("own", [])]
    return html, own, (base,)


def _one(
    page_id: str, html: Path, own: List[Path], bases: Tuple[Path, ...], render: bool
) -> Dict[str, Any]:
    out: Dict[str, Any] = {"findings": [], "errors": []}
    try:
        out["findings"] += static_findings([html, *own], bases)
    except Exception as exc:  # an engine crash is a result, not a stop
        out["errors"].append({"pass": "static", "error": f"{type(exc).__name__}: {exc}"[:300]})
    if render:
        rf, err = render_findings(html, bases)
        out["findings"] += rf
        if err:
            out["errors"].append({"pass": "render", "error": err})
        failed = [f for f in rf if f["rule"] == "render-failed"]
        for f in failed:
            out["errors"].append({"pass": "render", "error": f["excerpt"][:300]})
    out["findings"] = key_findings(page_id, out["findings"])
    return out


def seeded_pages() -> List[Dict[str, Any]]:
    plants = json.loads((SEEDED / "plants.json").read_text(encoding="utf-8"))
    return plants["pages"]


def run(
    render: bool = True, only: Optional[List[str]] = None, seeded: bool = False, twice: bool = False
) -> Dict[str, Any]:
    reason = render_available() if render else "render pass skipped by --static-only"
    do_render = render and reason is None
    pages: Dict[str, Any] = {}
    if seeded:
        todo = [
            (p["id"], SEEDED / "pages" / p["file"], [], (SEEDED / "pages",)) for p in seeded_pages()
        ]
    else:
        todo = []
        for e in mf.load()["pages"]:
            html, own, bases = _page_inputs(e)
            if not html.exists():
                pages[e["id"]] = {
                    "findings": [],
                    "errors": [
                        {
                            "pass": "load",
                            "error": f"{html} is missing; run python -m bench capture "
                            f"--only {e['id']} or restore the snapshot",
                        }
                    ],
                }
                continue
            todo.append((e["id"], html, own, bases))
    nondeterministic = []
    for pid, html, own, bases in todo:
        if only and pid not in only:
            continue
        print(f"bench: {pid}", file=sys.stderr, flush=True)
        first = _one(pid, html, own, bases, do_render)
        if twice:
            second = _one(pid, html, own, bases, do_render)
            a = [f["key"] for f in first["findings"]]
            b = [f["key"] for f in second["findings"]]
            if a != b:
                nondeterministic.append(
                    {
                        "page": pid,
                        "only_first": sorted(set(a) - set(b)),
                        "only_second": sorted(set(b) - set(a)),
                    }
                )
        pages[pid] = first
    return {
        "engine": engine_version(),
        "render": do_render,
        "render_note": "" if do_render else reason,
        "twice": twice,
        "nondeterministic": nondeterministic,
        "pages": pages,
    }


def summary(result: Dict[str, Any]) -> str:
    n_pages = len(result["pages"])
    n_find = sum(len(p["findings"]) for p in result["pages"].values())
    n_err = sum(len(p["errors"]) for p in result["pages"].values())
    lines = [
        f"{n_pages} pages, {n_find} findings, {n_err} errors, render "
        f"{'on' if result['render'] else 'off (' + result['render_note'] + ')'}"
    ]
    if result.get("twice"):
        lines.append(
            f"determinism: {len(result['nondeterministic'])} page(s) differed between two runs"
        )
    return "\n".join(lines)


def write_expected(result: Dict[str, Any]) -> int:
    EXPECTED.mkdir(parents=True, exist_ok=True)
    n = 0
    for pid, page in result["pages"].items():
        rows = [
            {k: f[k] for k in ("key", "pass", "rule", "severity", "file", "line")}
            for f in page["findings"]
        ]
        (EXPECTED / f"{pid}.json").write_text(
            json.dumps({"page": pid, "findings": rows}, indent=1, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
        n += 1
    return n


def load_run(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist; run python -m bench run first")
    return json.loads(path.read_text(encoding="utf-8"))


def all_findings(result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [f for p in result["pages"].values() for f in p["findings"]]


__all__ = [
    "run",
    "summary",
    "write_expected",
    "load_run",
    "all_findings",
    "key_findings",
    "engine_version",
    "default_out",
    "ROOT",
]
