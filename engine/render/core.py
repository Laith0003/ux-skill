"""Render check: layout rules measured on the rendered page.

The regex linter reads source. Some failures only exist after layout: a
centered heading whose box is pinned to one edge, a row that pushes the page
sideways. This module loads each HTML file in headless Chromium at a phone and
a desktop width, measures geometry, and returns findings in the linter's own
``Finding`` shape so both land in one report and one CI exit code.

Needs the optional ``render`` extra: ``pip install 'uxskill[render]'``. It
uses installed Google Chrome when present, else Playwright's Chromium.
"""
from __future__ import annotations

import asyncio
import re
from pathlib import Path
from typing import Iterable, List, Sequence

from engine.linter.core import Finding, LintReport, SEVERITY_RANK, compute_score

# Phone, large phone, tablet, desktop. Some drift only exists between
# breakpoints (a max-width that is wider than a phone column but narrower
# than a tablet one), so two widths are not enough.
VIEWPORTS: Sequence[tuple] = ((390, 844), (430, 932), (768, 1024), (1280, 800))
# Pages rendered at once. Chromium handles this comfortably on a laptop.
CONCURRENCY = 8
# Box-center drift below this is sub-pixel rounding, not a layout bug.
TOLERANCE_PX = 4

# Freeze motion and transforms so geometry is the resting layout, not a
# mid-animation frame or a reveal transform waiting for a scroll trigger.
_FREEZE_CSS = (
    "*,*::before,*::after{animation-duration:0s!important;animation-delay:0s!important;"
    "transition:none!important;transform:none!important}"
)

_MEASURE_JS = r"""(tol) => {
  const vw = document.documentElement.clientWidth;
  const dir = getComputedStyle(document.documentElement).direction;
  const out = [];
  const BLOCK = new Set(['block', 'flow-root', 'list-item', 'table']);
  const FLOW = new Set(['block', 'flow-root', 'list-item', 'table-cell']);
  const visible = (e, cs) => cs.visibility !== 'hidden' && cs.display !== 'none'
    && e.getClientRects().length > 0;
  const text = e => (e.innerText || '').replace(/\s+/g, ' ').trim();
  const sel = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '')
    + (typeof e.className === 'string' && e.className.trim()
       ? '.' + e.className.trim().split(/\s+/).join('.') : '');

  for (const e of document.body.querySelectorAll('*')) {
    const cs = getComputedStyle(e);
    if (cs.textAlign !== 'center' || !BLOCK.has(cs.display) || !visible(e, cs)) continue;
    if (cs.position === 'absolute' || cs.position === 'fixed' || cs.float !== 'none') continue;
    if (!text(e)) continue;
    const p = e.parentElement; if (!p) continue;
    const ps = getComputedStyle(p);
    if (!FLOW.has(ps.display)) continue;  // flex/grid place children themselves
    const pr = p.getBoundingClientRect(), r = e.getBoundingClientRect();
    const cl = pr.left + parseFloat(ps.borderLeftWidth) + parseFloat(ps.paddingLeft);
    const cr = pr.right - parseFloat(ps.borderRightWidth) - parseFloat(ps.paddingRight);
    if (r.width >= (cr - cl) - 1) continue;  // full width: centered text is centered
    const drift = (r.left + r.right) / 2 - (cl + cr) / 2;
    if (Math.abs(drift) < tol) continue;
    out.push({rule: 'centered-text-off-center', sel: sel(e), cls: e.className || '',
              text: text(e).slice(0, 60), drift: Math.round(drift), dir});
  }

  const root = document.scrollingElement;
  if (root.scrollWidth > root.clientWidth + 1) {
    const clipped = e => { for (let a = e.parentElement; a; a = a.parentElement) {
      const o = getComputedStyle(a).overflowX; if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') return a !== document.body && a !== document.documentElement; } return false; };
    const culprits = [];
    for (const e of document.body.querySelectorAll('*')) {
      const r = e.getBoundingClientRect();
      if ((r.right > vw + 1 || r.left < -1) && !clipped(e)
          && !culprits.some(c => c.contains(e))) culprits.push(e);
      if (culprits.length >= 3) break;
    }
    // Every box fits, yet the page scrolls: some element's content (an
    // unbreakable string, a wide inline child) spills past its own box.
    // Name the deepest such element.
    if (!culprits.length) {
      const spills = [...document.body.querySelectorAll('*')].filter(e => {
        if (getComputedStyle(e).overflowX !== 'visible' || clipped(e)) return false;
        const r = e.getBoundingClientRect();
        return e.scrollWidth > e.clientWidth + 1 && r.left + e.scrollWidth > vw + 1;
      });
      for (const e of spills) {
        if (!spills.some(o => o !== e && e.contains(o))) culprits.push(e);
        if (culprits.length >= 3) break;
      }
    }
    for (const e of culprits.length ? culprits : [document.body]) out.push({
      rule: 'horizontal-overflow', sel: sel(e), cls: e.className || '', text: text(e).slice(0, 60),
      drift: Math.round(root.scrollWidth - root.clientWidth), dir});
  }
  return {vw, findings: out};
}"""

_RULES = {
    "centered-text-off-center": dict(
        name="Centered text in a box that is not centered", severity="high",
        category="Layout",
        fix=("The text is centered inside its box, but the box sits against the start edge "
             "(left in LTR, right in RTL). Center the box itself: margin-inline: auto, or "
             "place it with the parent (flex/grid + justify-content/justify-items: center)."),
        what="box drifts {drift:+d}px from its container's center ({dir}, {vw}px viewport)"),
    "horizontal-overflow": dict(
        name="Page scrolls sideways", severity="high", category="Layout",
        fix=("An element is wider than the viewport. Constrain it (max-width: 100%, "
             "min-width: 0 on flex children, overflow-wrap: anywhere on long strings) "
             "instead of hiding overflow on the body."),
        what="page is {drift}px wider than the viewport ({dir}, {vw}px viewport)"),
    "render-failed": dict(
        name="Page could not be rendered", severity="medium", category="Layout",
        fix=("The render check could not load or measure this page, so its layout is "
             "unchecked. Run it again; if it repeats, look for a script or resource that "
             "never finishes loading, or a page error, in the message."),
        what="not measured: {error} ({vw}px viewport)"),
}


class RenderUnavailable(RuntimeError):
    """Playwright or a Chromium browser is missing."""


async def _launch(pw):
    errors = []
    for kwargs in ({"channel": "chrome"}, {}):
        try:
            return await pw.chromium.launch(**kwargs)
        except Exception as exc:  # browser not installed on this channel
            errors.append(str(exc).splitlines()[0])
    raise RenderUnavailable(
        "No browser for the render check. Install Google Chrome, or run "
        "`python -m playwright install chromium`. (" + "; ".join(errors) + ")")


def _locate(source: str, cls: str, text: str) -> int:
    """Best-effort source line for a rendered element: its class attribute,
    else the start of its text. 0 when neither is found."""
    needles = []
    if cls:
        needles.append(re.compile(r'class=["\']' + re.escape(cls) + r'["\']'))
    if text:
        needles.append(re.compile(re.escape(text[:24])))
    for rx in needles:
        m = rx.search(source)
        if m:
            return source.count("\n", 0, m.start()) + 1
    return 0


def _html_files(paths: Iterable[str]) -> List[Path]:
    out: List[Path] = []
    for p in map(Path, paths):
        if p.is_file() and p.suffix.lower() in (".html", ".htm"):
            out.append(p)
        elif p.is_dir():
            out.extend(sorted(x for x in p.rglob("*.htm*") if x.suffix.lower() in (".html", ".htm")))
    return out


async def _measure(browser, sem, f: Path, w: int, h: int):
    async with sem:
        page = await browser.new_page(viewport={"width": w, "height": h})
        try:
            await page.goto(f.resolve().as_uri(), wait_until="load")
            await page.add_style_tag(content=_FREEZE_CSS)
            return await page.evaluate(_MEASURE_JS, TOLERANCE_PX)
        except Exception as exc:  # one page that hangs or errors must not stop the run
            error = (str(exc).strip().splitlines() or [type(exc).__name__])[0][:160]
            return {"vw": w, "findings": [
                {"rule": "render-failed", "sel": "page", "cls": "", "text": "", "error": error}]}
        finally:
            await page.close()


async def _run(files: List[Path], viewports: Sequence[tuple]):
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise RenderUnavailable(
            "The render check needs Playwright: pip install 'uxskill[render]'") from exc
    sem = asyncio.Semaphore(CONCURRENCY)
    async with async_playwright() as pw:
        browser = await _launch(pw)
        try:
            jobs = [_measure(browser, sem, f, w, h) for f in files for w, h in viewports]
            results = await asyncio.gather(*jobs)
        finally:
            await browser.close()
    n = len(viewports)
    return [results[i * n:(i + 1) * n] for i in range(len(files))]


def render_check(paths: Iterable[str], severity_threshold: str = "high",
                 viewports: Sequence[tuple] = VIEWPORTS) -> LintReport:
    """Render every HTML file under ``paths`` and return layout findings."""
    files = _html_files(paths)
    per_file = asyncio.run(_run(files, viewports)) if files else []
    findings: List[Finding] = []
    for f, results in zip(files, per_file):
        source = f.read_text(encoding="utf-8", errors="ignore")
        seen = set()
        for result in results:  # viewport order: report each element once, at its first width
            for hit in result["findings"]:
                key = (hit["rule"], hit["sel"])
                if key in seen:
                    continue
                seen.add(key)
                rule = _RULES[hit["rule"]]
                findings.append(Finding(
                    rule_id=hit["rule"], rule_name=rule["name"],
                    severity=rule["severity"], category=rule["category"],
                    file=str(f), line=_locate(source, hit["cls"], hit["text"]),
                    column=0,
                    excerpt=f'{hit["sel"]}: ' + rule["what"].format(vw=result["vw"], **hit),
                    fix=rule["fix"]))

    threshold = SEVERITY_RANK.get(severity_threshold, 2)
    return LintReport(
        findings=findings, files_scanned=len(files), rules_loaded=len(_RULES),
        exit_code=1 if any(SEVERITY_RANK[x.severity] >= threshold for x in findings) else 0,
        score=compute_score(findings, len(files)))
