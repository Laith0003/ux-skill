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
from engine.render import interact, taste

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

# Before the freeze: a fixed element that its own transform parks mostly
# off screen, with nothing running to bring it in, is a closed drawer or
# menu. The freeze would set its transform to none and measure it open.
_PARK_JS = r"""() => {
  const vw = document.documentElement.clientWidth, vh = window.innerHeight;
  for (const e of document.body.querySelectorAll('*')) {
    const cs = getComputedStyle(e);
    if (cs.position !== 'fixed' || cs.transform === 'none') continue;
    if (e.getAnimations({subtree: true}).length) continue;
    const r = e.getBoundingClientRect(), a = r.width * r.height;
    if (a <= 0) continue;
    const w = Math.max(0, Math.min(vw, r.right) - Math.max(0, r.left));
    const h = Math.max(0, Math.min(vh, r.bottom) - Math.max(0, r.top));
    if (w * h < a / 2) e.setAttribute('data-ux-parked', '');
  }
}"""

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
  const clipped = e => { for (let a = e.parentElement; a; a = a.parentElement) {
    const o = getComputedStyle(a).overflowX; if (o === 'hidden' || o === 'clip' || o === 'auto' || o === 'scroll') return a !== document.body && a !== document.documentElement; } return false; };
  const culprits = [];
  if (root.scrollWidth > root.clientWidth + 1) {
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

  // Text that runs past its own box lies over whatever sits beside it, even
  // when the page does not scroll: an unbreakable word in a narrow column,
  // a display size wider than its column. The deepest such text is named,
  // once, and not again when it already made the page scroll.
  const TEXTY = 'h1,h2,h3,h4,h5,h6,p,li,dt,dd,blockquote,figcaption,label,th,td';
  // How far the element's own text runs past its padding box: each text
  // node's line boxes, leaving out text in a descendant that is hidden,
  // taken out of flow (absolute, fixed) or that clips or scrolls itself.
  const spill = e => {
    const cs = getComputedStyle(e);
    if (cs.display === 'inline' || cs.display === 'contents' || cs.display === 'none'
        || cs.visibility !== 'visible' || cs.overflowX !== 'visible' || !e.clientWidth
        || clipped(e)) return 0;
    const r = e.getBoundingClientRect();
    const left = r.left + parseFloat(cs.borderLeftWidth);
    const right = r.right - parseFloat(cs.borderRightWidth);
    let over = 0;
    const walk = document.createTreeWalker(e, NodeFilter.SHOW_TEXT);
    for (let n = walk.nextNode(); n; n = walk.nextNode()) {
      if (!n.textContent.trim()) continue;
      let out = false;
      for (let a = n.parentElement; a && a !== e; a = a.parentElement) {
        const s = getComputedStyle(a);
        if (s.visibility !== 'visible' || s.display === 'none' || s.position === 'absolute'
            || s.position === 'fixed' || s.overflowX !== 'visible') { out = true; break; }
      }
      if (out) continue;
      const range = document.createRange();
      range.selectNodeContents(n);
      for (const q of range.getClientRects()) over = Math.max(over, q.right - right, left - q.left);
    }
    return over > 2 ? over : 0;
  };
  const spilling = [];
  for (const e of document.body.querySelectorAll(TEXTY)) {
    const over = spill(e);
    if (over) spilling.push([e, over]);
  }
  let named = 0;
  for (const [e, over] of spilling) {
    if (named >= 3) break;
    if (spilling.some(([o]) => o !== e && e.contains(o))
        || culprits.some(c => c === e || c.contains(e))) continue;
    named++;
    out.push({rule: 'text-overflows-its-box', sel: sel(e), cls: e.className || '',
              text: text(e).slice(0, 60), drift: Math.round(over), dir});
  }

  // A fixed panel over the first screen at rest: a cookie card, a consent
  // wall, a bar over the form. It is reported when it lies on top of the
  // page's heading or a form's first control, covers 30% or more of the
  // screen over text or an image, or is a wide panel floating clear of both
  // edges over them. A thin bar docked to an edge over nothing key, a
  // narrow widget, a sidebar beside the content, a layer painted under the
  // page, a drawer parked off screen, and an overlay that paints nothing or
  // takes no pointer pass. A transparent fixed wrapper is measured by the
  // painted boxes inside it.
  const vh = window.innerHeight, area = vw * vh;
  const alpha = c => {
    if (!c || c === 'transparent') return 0;
    const m = c.match(/\(([^)]*)\)/); if (!m) return 1;
    const slash = m[1].split('/');
    let a = slash.length > 1 ? slash[1].trim()
      : (/^rgba/.test(c) ? (m[1].split(',')[3] || '1').trim() : '1');
    return a.endsWith('%') ? parseFloat(a) / 100 : parseFloat(a); };
  const painted = cs => alpha(cs.backgroundColor) >= 0.5 || cs.backgroundImage !== 'none';
  const fixedIn = e => { for (let a = e.parentElement; a; a = a.parentElement)
    if (getComputedStyle(a).position === 'fixed') return true; return false; };
  const faded = e => { for (let a = e.parentElement; a; a = a.parentElement)
    if (parseFloat(getComputedStyle(a).opacity) === 0) return true; return false; };
  const keys = [document.querySelector('h1'),
    document.querySelector('form input:not([type=hidden]), form select, form textarea, form button')]
    .filter(k => k && !fixedIn(k) && k.getClientRects().length);
  const media = new Set(['IMG', 'PICTURE', 'VIDEO', 'CANVAS', 'SVG', 'svg']);
  const ownText = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  const onTop = (e, x, y) => { const t = document.elementFromPoint(x, y); return !!t && e.contains(t); };
  const beneath = (e, x, y) => onTop(e, x, y) && document.elementsFromPoint(x, y).some(el =>
    !e.contains(el) && !el.contains(e) && (media.has(el.tagName) || ownText(el)));
  const box = e => { // the panel's painted area: itself, else the painted boxes inside it
    if (painted(getComputedStyle(e))) return e.getBoundingClientRect();
    let u = null;
    for (const d of e.querySelectorAll('*')) {
      const ds = getComputedStyle(d);
      if (!painted(ds) || !visible(d, ds)) continue;
      const q = d.getBoundingClientRect(); if (q.width <= 0 || q.height <= 0) continue;
      u = u ? {left: Math.min(u.left, q.left), top: Math.min(u.top, q.top),
               right: Math.max(u.right, q.right), bottom: Math.max(u.bottom, q.bottom)} : q;
    }
    return u; };
  const SPOTS = [[0.5, 0.5], [0.2, 0.3], [0.8, 0.7], [0.5, 0.15], [0.5, 0.85]];
  for (const e of document.body.querySelectorAll('*')) {
    const cs = getComputedStyle(e);
    if (cs.position !== 'fixed' || !visible(e, cs) || cs.pointerEvents === 'none'
        || parseFloat(cs.opacity) === 0 || fixedIn(e) || faded(e)
        || e.hasAttribute('data-ux-parked')) continue;
    const b = box(e); if (!b) continue;
    const r = {left: Math.max(0, b.left), top: Math.max(0, b.top),
               right: Math.min(vw, b.right), bottom: Math.min(vh, b.bottom)};
    const w = r.right - r.left, h = r.bottom - r.top;
    if (w <= 0 || h <= 0) continue;
    const share = Math.round(100 * w * h / area);
    const key = keys.find(k => { if (e.contains(k)) return false;
      const q = k.getBoundingClientRect(), cx = (q.left + q.right) / 2, cy = (q.top + q.bottom) / 2;
      return cx >= r.left && cx <= r.right && cy >= r.top && cy <= r.bottom && onTop(e, cx, cy); });
    const docked = r.top <= 1 || r.bottom >= vh - 1;
    const over = SPOTS.some(([fx, fy]) => beneath(e, r.left + fx * w, r.top + fy * h));
    let why = '';
    if (key) why = 'covers the page\'s ' + (key.tagName === 'H1' ? 'heading' : 'form');
    else if (share >= 30 && over) why = 'covers ' + share + '% of the first screen';
    else if (!docked && w >= vw / 2 && over) why = 'floats over the content, clear of both edges';
    if (!why) continue;
    out.push({rule: 'first-screen-covered', sel: sel(e), cls: e.className || '',
              text: text(e).slice(0, 60), drift: share, why, dir});
  }
  // Phone widths: a text field set under 16px, which iOS Safari zooms the
  // page into on focus.
  if (vw <= 430) {
    let zooms = 0;
    for (const f of document.querySelectorAll('input,textarea,select')) {
      if (f.tagName === 'INPUT' && /^(hidden|checkbox|radio|range|color|file|submit|button|reset|image)$/.test(f.type)) continue;
      const q = f.getBoundingClientRect(), fs = getComputedStyle(f);
      if (q.width < 1 || q.height < 1 || fs.visibility === 'hidden' || f.disabled) continue;
      const px = parseFloat(fs.fontSize);
      if (px >= 16 || ++zooms > 6) continue;
      const nm = f.getAttribute('name') || f.id || f.getAttribute('aria-label') || '';
      out.push({rule: 'input-text-zooms', sel: sel(f) + (nm ? '[' + nm.slice(0, 24) + ']' : ''),
                cls: typeof f.className === 'string' ? f.className : '', text: '', drift: 0,
                px: Math.round(px * 10) / 10, dir});
    }
  }

  const seenEl = el => { const cs = getComputedStyle(el);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0; };
  // Images that failed to load, and images drawn at a shape their pixels are
  // not (object-fit fill, the default, stretching them).
  for (const im of document.images) {
    const q = im.getBoundingClientRect();
    // A broken image shrinks to its alt text, so any visible box counts.
    if (q.width < 1 || q.height < 1 || !seenEl(im)) continue;
    const src = im.currentSrc || im.src || '';
    const nm = (im.getAttribute('alt') || src.split('/').pop() || '').slice(0, 40);
    const base = {sel: sel(im), cls: typeof im.className === 'string' ? im.className : '',
                  text: nm, drift: 0, dir};
    // A root-relative path on a page opened from disk points at the disk's
    // root, not the site's: it cannot be judged here.
    const rootRel = location.protocol === 'file:' && /^\/(?!\/)/.test(im.getAttribute('src') || '');
    if (im.complete && im.naturalWidth === 0 && src && !rootRel) {
      const shown = im.getAttribute('src') || src;
      out.push({...base, rule: 'image-broken', src: shown.length > 80 ? '...' + shown.slice(-77) : shown});
      continue;
    }
    if (!im.naturalWidth || /\.svgz?(\?|#|$)/i.test(src) || src.startsWith('data:image/svg')) continue;
    if (q.width < 32 || q.height < 32 || getComputedStyle(im).objectFit !== 'fill') continue;
    const is = getComputedStyle(im), px = v => parseFloat(v) || 0;
    const cw = q.width - px(is.paddingLeft) - px(is.paddingRight) - px(is.borderLeftWidth) - px(is.borderRightWidth);
    const ch = q.height - px(is.paddingTop) - px(is.paddingBottom) - px(is.borderTopWidth) - px(is.borderBottomWidth);
    if (cw < 32 || ch < 32) continue;
    const want = im.naturalWidth / im.naturalHeight, got = cw / ch;
    const off = Math.abs(got / want - 1);
    if (off > 0.03) out.push({...base, rule: 'image-distorted', pct: Math.round(off * 100),
      nat: im.naturalWidth + 'x' + im.naturalHeight, box: Math.round(cw) + 'x' + Math.round(ch)});
  }

  // A target smaller than 24 by 24 CSS pixels whose 24px circle, centred on
  // it, meets another target or another small target's circle (WCAG 2.5.8,
  // with its spacing exception). A link inside a sentence and a checkbox or
  // radio the browser draws unstyled are the criterion's own exceptions.
  const TARGETS = 'a[href],button,input:not([type=hidden]),select,textarea,summary,'
    + '[role=button],[role=link],[role=tab],[role=menuitem],[role=checkbox],[role=radio],'
    + '[role=switch],[role=option],[tabindex]:not([tabindex="-1"])';
  const seenBox = el => { const q = el.getBoundingClientRect();
    // A visually hidden element (a 1px box, or one clipped away) is not seen.
    if (q.width <= 1 || q.height <= 1) return false;
    const vs = getComputedStyle(el);
    if ((vs.clip && vs.clip !== 'auto') || /inset\(50%|circle\(0/.test(vs.clipPath)) return false;
    return el.checkVisibility ? el.checkVisibility({opacityProperty: true, visibilityProperty: true}) : true; };
  const tg = [];
  for (const el of document.body.querySelectorAll(TARGETS)) {
    if (el.disabled || el.closest('[inert],[aria-hidden="true"]') || !seenBox(el)) continue;
    if (tg.some(o => o.el.contains(el))) continue;  // the outer control is the target
    const q = el.getBoundingClientRect(), cs = getComputedStyle(el);
    const p = el.parentElement;
    const inSentence = cs.display === 'inline' && p
      && [...p.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const uaDrawn = el.tagName === 'INPUT' && /^(checkbox|radio)$/.test(el.type)
      && cs.appearance !== 'none';
    tg.push({el, q, cx: (q.left + q.right) / 2, cy: (q.top + q.bottom) / 2,
             small: (q.width < 24 || q.height < 24) && !inSentence && !uaDrawn});
  }
  const circleMeetsBox = (t, q) => {
    const dx = Math.max(q.left - t.cx, 0, t.cx - q.right);
    const dy = Math.max(q.top - t.cy, 0, t.cy - q.bottom);
    return dx * dx + dy * dy < 144; };
  let small = 0;
  for (const t of tg) {
    if (!t.small) continue;
    const near = tg.find(o => o !== t && !o.el.contains(t.el) && !t.el.contains(o.el)
      && (circleMeetsBox(t, o.q) || (o.small && Math.hypot(o.cx - t.cx, o.cy - t.cy) < 24)));
    if (!near || ++small > 12) continue;
    const name = (t.el.getAttribute('aria-label') || text(t.el)).slice(0, 24);
    out.push({rule: 'target-too-small', sel: sel(t.el) + (name ? ' "' + name + '"' : ''),
              cls: typeof t.el.className === 'string' ? t.el.className : '',
              text: text(t.el).slice(0, 60), drift: 0, w: Math.round(t.q.width), h: Math.round(t.q.height), near: sel(near.el), dir});
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
    "text-overflows-its-box": dict(
        name="Text runs past its own box", severity="high", category="Layout",
        fix=("A word or line is wider than the box it sits in and lies over what is beside "
             "it. Give the text the column it needs (a smaller type role at this width, a "
             "wider column, min-width: 0 on a grid or flex child) or let long strings break "
             "(overflow-wrap: anywhere)."),
        what="text is {drift}px wider than its box ({dir}, {vw}px viewport)"),
    "input-text-zooms": dict(
        name="A text field under 16px on a phone", severity="medium", category="Forms",
        fix=("Set form fields to 16px or larger at phone widths (font-size: max(16px, 1rem)); "
             "below that, iOS Safari zooms the page in when the field takes focus and leaves "
             "the visitor to pinch back out."),
        what="the field's text is {px}px ({vw}px viewport)"),
    "image-broken": dict(
        name="An image that failed to load", severity="high", category="Imagery",
        fix=("Fix the path or ship the file: the page shows a broken image where a "
             "photograph belongs. Check the URL, the case of the filename and the build "
             "step that copies assets."),
        what="{src} did not load ({vw}px viewport)"),
    "image-distorted": dict(
        name="An image stretched out of its shape", severity="medium", category="Imagery",
        fix=("Keep the photograph's own proportions: give it object-fit: cover (or contain) "
             "with a set aspect-ratio, or set only one of width and height."),
        what="{nat} pixels drawn at {box}, {pct}% off its shape ({vw}px viewport)"),
    "target-too-small": dict(
        name="A small target crowded by another", severity="high", category="A11y",
        fix=("The control is under 24 by 24 CSS pixels and a 24px circle centred on it meets "
             "another control (WCAG 2.5.8). Give it a 24px hit area, with min-width and "
             "min-height or padding, or space it from its neighbours until the circles clear."),
        what="target is {w}x{h}px and its 24px circle meets {near} ({vw}px viewport)"),
    "first-screen-covered": dict(
        name="A fixed panel covers the first screen", severity="high", category="Layout",
        fix=("A cookie notice, banner or popup sits over the page at rest. Dock it to the top "
             "or bottom edge as a thin bar that covers neither the heading nor the form, or "
             "open it as a real dialog only when the visitor asks; never leave a wide card "
             "floating over the content."),
        what="{why} ({vw}px viewport)"),
    "render-failed": dict(
        name="Page could not be rendered", severity="medium", category="Layout",
        fix=("The render check could not load or measure this page, so its layout is "
             "unchecked. Run it again; if it repeats, look for a script or resource that "
             "never finishes loading, or a page error, in the message."),
        what="not measured: {error} ({vw}px viewport)"),
    **taste.RULES,
    **interact.RULES,
}


class RenderUnavailable(RuntimeError):
    """Playwright or a Chromium browser is missing."""


async def _launch(pw, args=()):
    errors = []
    for kwargs in ({"channel": "chrome"}, {}):
        try:
            return await pw.chromium.launch(args=list(args), **kwargs)
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


async def _measure(browser, sem, f: Path, w: int, h: int, desktop: bool = False):
    async with sem:
        page = await browser.new_page(viewport={"width": w, "height": h})
        try:
            await page.goto(f.resolve().as_uri(), wait_until="load")
            await page.evaluate(_PARK_JS)
            await page.add_style_tag(content=_FREEZE_CSS)
            result = await page.evaluate(_MEASURE_JS, TOLERANCE_PX)
            if desktop:  # the page's color, accents and photos, measured once
                try:
                    result["findings"].extend(await taste.page_checks(page))
                except Exception as exc:  # the layout result above still stands
                    error = (str(exc).strip().splitlines() or [type(exc).__name__])[0][:160]
                    result["findings"].append({
                        "rule": "render-failed", "sel": "page", "cls": "", "text": "",
                        "error": "color and photo checks: " + error})
            return result
        except Exception as exc:  # one page that hangs or errors must not stop the run
            error = (str(exc).strip().splitlines() or [type(exc).__name__])[0][:160]
            return {"vw": w, "findings": [
                {"rule": "render-failed", "sel": "page", "cls": "", "text": "", "error": error}]}
        finally:
            await page.close()


async def _motion(browser, sem, f: Path, w: int, h: int):
    """Motion that runs on its own, on pages that are not frozen."""
    async with sem:
        try:
            return {"vw": w, "findings": await taste.motion_checks(browser, f, w, h)}
        except Exception as exc:  # one page that hangs or errors must not stop the run
            error = (str(exc).strip().splitlines() or [type(exc).__name__])[0][:160]
            return {"vw": w, "findings": [
                {"rule": "render-failed", "sel": "page", "cls": "", "text": "", "error": error}]}


async def _interact(browser, sem, f: Path):
    """Focus, timing and Escape on pages whose motion runs."""
    async with sem:
        try:
            return {"vw": interact.WIDTHS[0][0],
                    "findings": await interact.interaction_checks(browser, f)}
        except Exception as exc:  # one page that hangs or errors must not stop the run
            error = (str(exc).strip().splitlines() or [type(exc).__name__])[0][:160]
            return {"vw": interact.WIDTHS[0][0], "findings": [
                {"rule": "render-failed", "sel": "page", "cls": "", "text": "",
                 "error": "interaction pass: " + error}]}


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
            wide = max(viewports, key=lambda v: v[0])
            jobs = []
            for f in files:
                jobs.extend(_measure(browser, sem, f, w, h, desktop=(w, h) == wide)
                            for w, h in viewports)
                jobs.append(_motion(browser, sem, f, *wide))
                jobs.append(_interact(browser, sem, f))
            results = await asyncio.gather(*jobs)
        finally:
            await browser.close()
    n = len(viewports) + 2
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
                    excerpt=f'{hit["sel"]}: ' + rule["what"].format(**{"vw": result["vw"], **hit}),
                    fix=rule["fix"]))

    threshold = SEVERITY_RANK.get(severity_threshold, 2)
    return LintReport(
        findings=findings, files_scanned=len(files), rules_loaded=len(_RULES),
        exit_code=1 if any(SEVERITY_RANK[x.severity] >= threshold for x in findings) else 0,
        score=compute_score(findings, len(files)))
