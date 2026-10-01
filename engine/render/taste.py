"""Render checks that read the page's own system: the color budget, the
photo grade lock, accent text on every ground it lands on, and motion that
runs on its own.

The color budget and the grade lock apply only when the page carries the
engine's tokens (--color-budget-chromatic, --imagery-photo-*): they judge a
page against the system it was built from. Accent contrast and the motion
checks apply to every page.
"""
from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import unquote, urlparse

from engine.foundations.imagery import PhotoDirection, grade_problems

# Shared helpers: color parsing through a canvas, OKLab chroma, luminance.
_COLOR_JS = r"""
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const cx = cv.getContext('2d', {willReadFrequently: true});
  const cache = new Map();
  const rgba = (c) => {
    if (cache.has(c)) return cache.get(c);
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = 'rgba(0,0,0,0)'; cx.fillStyle = c;
    cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data;
    const out = [d[0], d[1], d[2], d[3] / 255]; cache.set(c, out); return out;
  };
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const chroma = ([r, g, b]) => {
    const R = lin(r), G = lin(g), B = lin(b);
    const l = Math.cbrt(0.4122214708*R + 0.5363325363*G + 0.0514459929*B);
    const m = Math.cbrt(0.2119034982*R + 0.6806995451*G + 0.1073969566*B);
    const s = Math.cbrt(0.0883024619*R + 0.2817188376*G + 0.6299787005*B);
    const a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s;
    const bb = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s;
    return Math.hypot(a, bb);
  };
  const lum = ([r, g, b]) => 0.2126*lin(r) + 0.7152*lin(g) + 0.0722*lin(b);
  const ratio = (x, y) => { const a = lum(x), b = lum(y); return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05); };
  const over = (top, under) => { const a = top[3]; return [0, 1, 2].map(i => Math.round(top[i]*a + under[i]*(1 - a))).concat([1]); };
  const hex = c => '#' + c.slice(0, 3).map(v => v.toString(16).padStart(2, '0')).join('');
  const sel = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '')
    + (typeof e.className === 'string' && e.className.trim()
       ? '.' + e.className.trim().split(/\s+/).join('.') : '');
  const shown = e => { const cs = getComputedStyle(e);
    return cs.visibility !== 'hidden' && cs.display !== 'none' && e.getClientRects().length > 0; };
  const root = getComputedStyle(document.documentElement);
  const token = n => parseFloat(root.getPropertyValue(n));
"""

_PAGE_JS = r"""(limits) => {
""" + _COLOR_JS + r"""
  const out = {findings: [], photos: [], grade: null};
  const CHROMATIC = limits.chromatic, ACCENT = limits.accent;
  // Status colors: every custom property named for a status, as the page
  // resolves it. They carry meaning, so the budget leaves them out.
  const status = new Set();
  const walk = rules => { for (const r of rules) {
    if (r.cssRules) walk(r.cssRules);
    if (!r.style) continue;
    for (const name of r.style) if (name.startsWith('--')
        && /status|error|danger|success|warning|info|positive|negative|critical/i.test(name)) {
      const v = root.getPropertyValue(name).trim();
      if (v) { const c = rgba(v); if (c[3] > 0) status.add(hex(c)); }
    } } };
  for (const s of document.styleSheets) { try { walk(s.cssRules); } catch (e) {} }

  // Text: characters in a chromatic color, and accent text on its ground.
  const skip = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'TEMPLATE']);
  let chars = 0, colored = 0;
  const seenPairs = new Set();
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n = tw.nextNode(); n; n = tw.nextNode()) {
    const t = n.nodeValue.replace(/\s+/g, '');
    const p = n.parentElement;
    if (!t || !p || skip.has(p.tagName) || p.closest('svg,canvas') || !shown(p)) continue;
    const c = rgba(getComputedStyle(p).color);
    if (c[3] === 0) continue;
    const isStatus = status.has(hex(c));
    chars += t.length;
    if (!isStatus && chroma(c) >= CHROMATIC) colored += t.length;
    if (isStatus || chroma(c) < ACCENT) continue;
    // The ground: the backgrounds under the text, composited on white. A
    // photograph or gradient under it, or an overlay beside media, is left
    // to the scrim check.
    let ground = [255, 255, 255, 1], layers = [], unknown = false;
    for (let a = p; a; a = a.parentElement) {
      const cs = getComputedStyle(a);
      if (cs.backgroundImage !== 'none') { unknown = true; break; }
      if ((cs.position === 'absolute' || cs.position === 'fixed') && a.parentElement
          && a.parentElement.querySelector('img,picture,video,canvas')) { unknown = true; break; }
      const b = rgba(cs.backgroundColor);
      if (b[3] > 0) { layers.push(b); if (b[3] >= 1) break; }
    }
    if (unknown) continue;
    for (const b of layers.reverse()) ground = over(b, ground);
    const ink = over(c, ground);
    const r = ratio(ink, ground);
    const key = hex(c) + hex(ground);
    if (r < 4.5 && !seenPairs.has(key)) {
      seenPairs.add(key);
      // 1.4.3 asks 3:1 of large text (24px, or 18.66px bold); the system
      // holds every text role to 4.5:1 as its own floor.
      const ps = getComputedStyle(p), px = parseFloat(ps.fontSize), w = parseInt(ps.fontWeight, 10);
      const large = px >= 24 || (px >= 18.66 && w >= 700);
      const under = (large && r >= 3)
        ? 'under 4.5:1, the system\'s own floor for all text (1.4.3 asks 3:1 of large text)'
        : (large ? 'under 3:1 (1.4.3, large text)' : 'under 4.5:1 (1.4.3)');
      out.findings.push({rule: 'accent-text-low-contrast', sel: sel(p), cls: p.className || '',
        text: t.slice(0, 60),
        detail: 'accent text ' + hex(c) + ' on ' + hex(ground) + ' measures '
          + (Math.floor(r * 100) / 100).toFixed(2) + ':1, ' + under});
    }
  }

  // Fill: a 16px grid over the page, painted in document order. Images,
  // video, canvas, SVG and background pictures are left out of the count.
  const budget = token('--color-budget-chromatic');
  if (!isNaN(budget)) {
    const bands = token('--color-budget-bands') || 0;
    const W = document.documentElement.scrollWidth, H = document.documentElement.scrollHeight;
    const S = 16, cols = Math.ceil(W / S), rows = Math.ceil(H / S);
    const grid = new Uint8Array(cols * rows);  // 0 neutral, 1 chromatic, 2 image
    const kind = cs => {
      if (/url\(/.test(cs.backgroundImage)) return 2;
      const stops = (cs.backgroundImage.match(/rgba?\([^)]*\)/g) || []).map(rgba).filter(x => x[3] > 0.5);
      if (stops.length) return stops.reduce((s, x) => s + chroma(x), 0) / stops.length >= CHROMATIC ? 1 : 0;
      const b = rgba(cs.backgroundColor);
      if (b[3] < 0.5) return -1;
      return (!status.has(hex(b)) && chroma(b) >= CHROMATIC) ? 1 : 0;
    };
    const paint = (r, k) => {
      const x0 = Math.max(0, Math.floor((r.left + scrollX) / S)), x1 = Math.min(cols, Math.ceil((r.right + scrollX) / S));
      const y0 = Math.max(0, Math.floor((r.top + scrollY) / S)), y1 = Math.min(rows, Math.ceil((r.bottom + scrollY) / S));
      for (let y = y0; y < y1; y++) grid.fill(k, y * cols + x0, y * cols + x1);
    };
    const base = kind(getComputedStyle(document.documentElement));
    const bodyKind = kind(getComputedStyle(document.body));
    grid.fill(bodyKind >= 0 ? bodyKind : Math.max(base, 0));
    for (const e of document.body.querySelectorAll('*')) {
      if (skip.has(e.tagName) || e.closest('svg') && e.tagName.toLowerCase() !== 'svg' || !shown(e)) continue;
      const r = e.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) continue;
      if (e.matches('img,picture,video,canvas,iframe,svg')) { paint(r, 2); continue; }
      const k = kind(getComputedStyle(e));
      if (k >= 0) paint(r, k);
    }
    let ui = 0, fill = 0;
    for (const v of grid) { if (v !== 2) { ui++; if (v === 1) fill++; } }
    const textShare = chars ? colored / chars : 0, fillShare = ui ? fill / ui : 0;
    const excess = [];
    if (textShare > budget + limits.slack)
      excess.push(Math.round(textShare * 100) + '% of the text is in a chromatic color');
    if (fillShare > budget + bands + limits.slack)
      excess.push('chromatic fill covers ' + Math.round(fillShare * 100) + '% of the interface');
    if (excess.length) out.findings.push({rule: 'color-over-budget', sel: 'page', cls: '', text: '',
      detail: excess.join(' and ') + '; the system allows ' + Math.round(budget * 100)
        + '% (color.budget.chromatic) plus ' + Math.round(bands * 100)
        + '% of fill for bands (color.budget.bands)'});
  }

  // Photographs, for the grade lock: raster images and backgrounds at least
  // 120px on each side that are not a logo.
  const names = ['lightness', 'temperature', 'chroma', 'spread-lightness', 'spread-temperature',
                 'spread-chroma'];
  const grade = {};
  for (const n of names) grade[n] = token('--imagery-photo-' + n);
  if (names.every(n => !isNaN(grade[n]))) {
    out.grade = grade;
    const logo = e => /logo|wordmark|brandmark/i.test([e.id, e.className, e.getAttribute('alt') || ''].join(' '));
    for (const e of document.querySelectorAll('*')) {
      if (!shown(e) || e.closest('svg')) continue;
      const r = e.getBoundingClientRect();
      if (r.width < 120 || r.height < 120 || logo(e)) continue;
      let src = null;
      if (e.tagName === 'IMG') src = e.currentSrc || e.src;
      else { const m = /url\(["']?([^"')]+)["']?\)/.exec(getComputedStyle(e).backgroundImage); if (m) src = m[1]; }
      if (!src || /\.svgz?(\?|#|$)/i.test(src) || src.startsWith('data:image/svg')) continue;
      let href = null;
      try { href = new URL(src, document.baseURI).href; } catch (err) { href = null; }
      if (href) out.photos.push({src: href, sel: sel(e), cls: e.className || ''});
    }
  }
  return out;
}"""

# Mean CIELAB lightness, b* and chroma of each image, drawn from a data URL
# into a small canvas so no image taints it.
_PHOTO_JS = r"""async (urls) => {
  const lin = v => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
  const f = t => t > 216 / 24389 ? Math.cbrt(t) : (24389 / 27 * t + 16) / 116;
  const out = [];
  for (const u of urls) {
    try {
      const img = new Image(); img.src = u; await img.decode();
      const w = Math.max(1, Math.min(64, img.naturalWidth)), h = Math.max(1, Math.min(64, img.naturalHeight));
      const c = document.createElement('canvas'); c.width = w; c.height = h;
      const x = c.getContext('2d'); x.drawImage(img, 0, 0, w, h);
      const d = x.getImageData(0, 0, w, h).data;
      let L = 0, B = 0, C = 0, n = 0;
      for (let i = 0; i < d.length; i += 4) {
        if (d[i + 3] < 128) continue;
        const r = lin(d[i]), g = lin(d[i + 1]), b = lin(d[i + 2]);
        const X = (0.4124*r + 0.3576*g + 0.1805*b) / 0.95047, Y = 0.2126*r + 0.7152*g + 0.0722*b,
              Z = (0.0193*r + 0.1192*g + 0.9505*b) / 1.08883;
        const l = 116 * f(Y) - 16, a = 500 * (f(X) - f(Y)), bb = 200 * (f(Y) - f(Z));
        L += l; B += bb; C += Math.hypot(a, bb); n++;
      }
      out.push(n ? [L / n, B / n, C / n] : null);
    } catch (e) { out.push(null); }
  }
  return out;
}"""

# Motion that runs on its own: loops under reduced motion, and anything that
# moves for more than five seconds with no pause control.
_MOTION_JS = r"""(reduced) => {
""" + _COLOR_JS + r"""
  const out = [];
  const progress = e => !!e.closest('[role=progressbar],[aria-busy=true]')
    || /spin|loader|loading|progress/i.test([e.id, e.className].join(' '));
  // Pause and stop in the shipped languages: whole words in Latin scripts,
  // the word anywhere in the others. Play counts only as a toggle.
  const PAUSE = /(?:^|[^\p{L}])(?:pause|stop|pausa|pausar|arr\u00eater|anhalten)(?![\p{L}])|\u0625\u064a\u0642\u0627\u0641|\u0623\u0648\u0642\u0641|\u062a\u0648\u0642\u0641|\u505c\u6b62|\u6682\u505c|\u4e00\u6642\u505c\u6b62/iu;
  const PLAY = /(?:^|[^\p{L}])play(?![\p{L}])/iu;
  const AREA = 'section,article,aside,header,footer,figure,[role=region],[role=banner],[role=contentinfo]';
  const controls = [...document.querySelectorAll('button,[role=button],input[type=checkbox],[aria-pressed]')]
    .filter(shown);
  const named = e => [e.getAttribute('aria-label'), e.innerText, e.getAttribute('title'), e.value].join(' ');
  const seen = new Set();
  for (const a of document.getAnimations()) {
    const e = a.effect && a.effect.target;
    if (!e || a.playState !== 'running' || !(e instanceof Element) || !shown(e) || progress(e)) continue;
    const t = a.effect.getComputedTiming();
    const forever = t.iterations === Infinity;
    const name = a.animationName || 'an animation';
    if (reduced) {
      if (!forever || seen.has(e)) continue;
      seen.add(e);
      out.push({rule: 'infinite-animation-under-reduced-motion', sel: sel(e), cls: e.className || '',
        text: (e.innerText || '').slice(0, 60),
        detail: name + ' keeps running with reduced motion set'});
      continue;
    }
    const total = forever ? Infinity : (t.delay || 0) + t.activeDuration;
    if (total <= 5000 || seen.has(e)) continue;
    const other = (document.body.innerText || '').length - (e.innerText || '').length;
    if (other <= 0) continue;
    const owns = c => { const id = c.getAttribute('aria-controls');
      if (!id) return false; const tgt = document.getElementById(id); return !!tgt && tgt.contains(e); };
    // A control counts when it names the moving element (aria-controls on
    // it or an ancestor), or is a pause control in the same area of the page.
    const area = e.closest(AREA) || document.body;
    const pauses = c => PAUSE.test(named(c)) || (PLAY.test(named(c)) && c.hasAttribute('aria-pressed'));
    if (controls.some(c => owns(c) || (area.contains(c) && pauses(c)))) continue;
    seen.add(e);
    out.push({rule: 'moving-content-without-pause', sel: sel(e), cls: e.className || '',
      text: (e.innerText || '').slice(0, 60),
      detail: name + ' moves on its own for ' + (forever ? 'ever' : Math.round(total / 1000) + 's')
        + ' beside other content and the page has no pause control'});
  }
  return out;
}"""

# A text color counts toward the budget at OKLCH chroma 0.08 and above
# (about CIELAB C* 30, where measured pages read as saturated); accent text
# is any color at 0.04 and above. The budget tolerates two points of slack.
LIMITS = {"chromatic": 0.08, "accent": 0.04, "slack": 0.02}
MOTION_WAIT_MS = 300


async def _bytes(page, url: str) -> Optional[str]:
    """A data URL for the image at ``url``: a file read from disk, a data
    URL as is, or a web image fetched through the page's own context."""
    try:
        if url.startswith("data:"):
            return url
        parsed = urlparse(url)
        if parsed.scheme == "file":
            path = Path(unquote(parsed.path))
            data = path.read_bytes()
            mime = mimetypes.guess_type(path.name)[0] or "image/png"
        else:
            resp = await page.request.get(url)
            if not resp.ok:
                return None
            data = await resp.body()
            mime = (resp.headers.get("content-type") or "image/png").split(";")[0]
        return f"data:{mime};base64," + base64.b64encode(data).decode("ascii")
    except Exception:  # an image that cannot be read is not graded
        return None


def _direction(grade: Dict[str, float]) -> PhotoDirection:
    spread = {k: grade["spread-" + k] for k in ("lightness", "temperature", "chroma")}
    return PhotoDirection(allowed=True, lightness=grade["lightness"],
                          temperature=grade["temperature"], chroma=grade["chroma"], contrast=0.0,
                          black_point=0.0, grain=0.0, energy=0.0, spread=spread, subject="",
                          framing="", kinds=(), words=())


async def page_checks(page) -> List[Dict[str, Any]]:
    """The color budget, accent grounds and grade lock on a loaded page."""
    result = await page.evaluate(_PAGE_JS, LIMITS)
    hits: List[Dict[str, Any]] = list(result["findings"])
    photos = result["photos"]
    if result["grade"] and photos:
        urls = [await _bytes(page, p["src"]) for p in photos]
        keep = [(p, u) for p, u in zip(photos, urls) if u]
        means = await page.evaluate(_PHOTO_JS, [u for _, u in keep]) if keep else []
        measured = [(p, m) for (p, _), m in zip(keep, means) if m]
        if measured:
            names = [Path(urlparse(p["src"]).path).name or p["src"][:40] for p, _ in measured]
            problems = grade_problems([(n, *m) for n, (_, m) in zip(names, measured)],
                                      _direction(result["grade"]))
            for message in problems:
                who = next(((p, n) for n, (p, _) in zip(names, measured) if message.startswith(n)),
                           None)
                p = who[0] if who else {"sel": "page", "cls": ""}
                hits.append({"rule": "photo-grade-off", "sel": p["sel"], "cls": p["cls"],
                             "text": "", "detail": message})
    return hits


async def motion_checks(browser, f: Path, width: int, height: int) -> List[Dict[str, Any]]:
    """Loops under reduced motion, then moving content with no pause."""
    hits: List[Dict[str, Any]] = []
    for reduced in (True, False):
        page = await browser.new_page(viewport={"width": width, "height": height},
                                      reduced_motion="reduce" if reduced else "no-preference")
        try:
            await page.goto(f.resolve().as_uri(), wait_until="load")
            await page.wait_for_timeout(MOTION_WAIT_MS)
            hits.extend(await page.evaluate(_MOTION_JS, reduced))
        finally:
            await page.close()
    return hits


RULES = {
    "color-over-budget": dict(
        name="Chromatic color past the system's budget", severity="medium", category="Color",
        fix=("Set running text and most headings in the neutral text roles and keep the brand "
             "color for the primary action, links and the moments the brand calls for; carry "
             "section rhythm on the band roles, within color.budget.bands."),
        what="{detail} ({vw}px viewport)"),
    "photo-grade-off": dict(
        name="Photo outside the page's grade", severity="medium", category="Imagery",
        fix=("Regrade the photo to the system's photo direction (imagery.photo.*), or replace it "
             "with one that already sits within the grade lock beside the others."),
        what="{detail}"),
    "accent-text-low-contrast": dict(
        name="Accent text under 4.5:1 on its ground", severity="high", category="A11y",
        fix=("Use the system's link or accent role for this surface (it is checked at 4.5:1 on "
             "every ground it sits on), or darken the accent on this ground until it reaches "
             "4.5:1."),
        what="{detail} ({vw}px viewport)"),
    "infinite-animation-under-reduced-motion": dict(
        name="Loop keeps running under reduced motion", severity="high", category="Motion",
        fix=("Stop the animation in @media (prefers-reduced-motion: reduce) with animation: none, "
             "or run it only inside @media (prefers-reduced-motion: no-preference)."),
        what="{detail}"),
    "moving-content-without-pause": dict(
        name="Moving content with no pause control", severity="high", category="Motion",
        fix=("Add a button that pauses the motion (aria-controls naming the moving region, "
             "aria-pressed for its state, a name such as Pause), as 2.2.2 asks for anything that "
             "moves on its own for more than five seconds beside other content."),
        what="{detail}"),
}
