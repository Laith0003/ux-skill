"""The interaction pass of the render check: a page loaded with its motion
running, driven the way a person would drive it.

At each width it tabs through the first FOCUS_STEPS focusable elements and
asks for a focus indicator that differs from the resting style (2.4.7) and
that no ancestor clips. It hovers and presses the first buttons, chips and
cards and times how long each takes to reach half its change; a direct
response is half done within motion.DIRECT_T50 (our pacing, the one the
lint reads from a curve). It opens each control with aria-haspopup,
presses Escape, and asks for focus back on the control. With reduced motion
set it presses again and asks for no scale or movement.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Sequence

from engine.foundations.motion import DIRECT_T50

# The widths the pass drives, the focusables it tabs through, the controls
# it times, the menus it opens, and how long it samples each move.
WIDTHS: Sequence[tuple] = ((1280, 800), (390, 844))
FOCUS_STEPS = 30
PRESS_LIMIT = 6
POPUP_LIMIT = 6
SAMPLE_MS = 380
# One frame of slack on top of the half-travel time, for sampling by frame.
FRAME_MS = 17

_SETUP_JS = r"""() => {
  if (window.__ux) return;
  const sel = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '')
    + (typeof e.className === 'string' && e.className.trim()
       ? '.' + e.className.trim().split(/\s+/).join('.') : '');
  const shown = e => { const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'
      && parseFloat(cs.opacity) > 0; };
  const look = e => { const cs = getComputedStyle(e);
    return [cs.outlineStyle, cs.outlineWidth, cs.outlineColor, cs.boxShadow, cs.borderColor,
            cs.backgroundColor, cs.color, cs.textDecorationLine].join('|'); };
  const rest = new Map();
  const FOCUSABLE = 'a[href],button,input:not([type=hidden]),select,textarea,summary,'
    + '[tabindex]:not([tabindex="-1"]),[contenteditable=""],[contenteditable=true]';
  for (const e of document.querySelectorAll(FOCUSABLE)) rest.set(e, look(e));
  const vec = e => { const cs = getComputedStyle(e);
    let m = [1, 0, 0, 1, 0, 0];
    const t = cs.transform.match(/matrix\(([^)]+)\)/);
    if (t) m = t[1].split(',').map(Number);
    const c = (cs.backgroundColor.match(/[\d.]+/g) || [0, 0, 0, 0]).map(Number);
    const a = c.length > 3 ? c[3] : 1;
    return [...m.slice(0, 4), m[4] / 40, m[5] / 40, c[0] / 255, c[1] / 255, c[2] / 255, a,
            parseFloat(cs.opacity)]; };
  window.__ux = {sel, shown, look, rest, vec, rec: null};
  window.__ux.start = (e, kind) => {
    const r = {e, samples: [], t0: null};
    const mark = () => { if (r.t0 === null) r.t0 = performance.now(); };
    e.addEventListener(kind, mark, {once: true});
    const tick = () => { r.samples.push([performance.now(), vec(e)]);
      if (window.__ux.rec === r) requestAnimationFrame(tick); };
    window.__ux.rec = r; tick();
  };
  window.__ux.stop = () => { const r = window.__ux.rec; window.__ux.rec = null;
    if (!r || r.t0 === null) return null;
    const v0 = r.samples.filter(s => s[0] <= r.t0).pop() || r.samples[0];
    const vf = r.samples[r.samples.length - 1][1];
    const d = (a, b) => Math.hypot(...a.map((x, i) => x - b[i]));
    const span = d(vf, v0[1]);
    if (span < 0.01) return {t50: null};
    for (const [t, v] of r.samples) if (t >= r.t0 && d(v, v0[1]) >= span / 2) return {t50: t - r.t0};
    return {t50: null};
  };
}"""

_FOCUS_JS = r"""() => {
  const u = window.__ux, e = document.activeElement;
  if (!e || e === document.body || e === document.documentElement) return {none: true};
  const cs = getComputedStyle(e);
  const before = u.rest.get(e);
  const changed = before === undefined ? true : u.look(e) !== before;
  const ow = cs.outlineStyle !== 'none' ? parseFloat(cs.outlineWidth) || 0 : 0;
  const shadow = cs.boxShadow !== 'none';
  const pad = ow ? ow + Math.max(0, parseFloat(cs.outlineOffset) || 0) : (shadow ? 2 : 0);
  const r = e.getBoundingClientRect();
  const ring = {l: r.left - pad, t: r.top - pad, r: r.right + pad, b: r.bottom + pad};
  let clip = null;
  if (pad) for (let a = e.parentElement; a && a !== document.body; a = a.parentElement) {
    const as = getComputedStyle(a);
    if (!/hidden|clip|auto|scroll/.test(as.overflowX + as.overflowY)) continue;
    const ar = a.getBoundingClientRect();
    if (ring.l < ar.left - 0.5 || ring.t < ar.top - 0.5 || ring.r > ar.right + 0.5
        || ring.b > ar.bottom + 0.5) { clip = u.sel(a); break; }
  }
  return {sel: u.sel(e), cls: typeof e.className === 'string' ? e.className : '',
          text: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 60),
          visible: changed, clip};
}"""

_PRESSABLES_JS = r"""(limit) => {
  const u = window.__ux, seen = new Set(), out = [];
  const cand = document.querySelectorAll(
    'button,[role=button],a[class*=btn],a[class*=button],[class*=chip],a[class*=card],[class*=card] > a');
  for (const e of cand) {
    if (!u.shown(e) || e.disabled) continue;
    const key = e.tagName + '|' + (typeof e.className === 'string' ? e.className : '');
    if (seen.has(key)) continue;
    seen.add(key); e.setAttribute('data-ux-probe', out.length); out.push(u.sel(e));
    if (out.length >= limit) break;
  }
  return out;
}"""

_POPUPS_JS = r"""(limit) => {
  const u = window.__ux, out = [];
  for (const e of document.querySelectorAll('button[aria-haspopup],[role=button][aria-haspopup]')) {
    if (!u.shown(e) || e.getAttribute('aria-haspopup') === 'false') continue;
    e.setAttribute('data-ux-popup', out.length); out.push(u.sel(e));
    if (out.length >= limit) break;
  }
  return out;
}"""


def _hit(rule: str, sel: str, detail: str, cls: str = "", text: str = "") -> Dict[str, Any]:
    return {"rule": rule, "sel": sel, "cls": cls, "text": text, "detail": detail}


async def _focus_pass(page) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    seen = set()
    for _ in range(FOCUS_STEPS):
        await page.keyboard.press("Tab")
        info = await page.evaluate(_FOCUS_JS)
        if info.get("none"):
            continue
        if info["sel"] in seen:
            break  # the tab order came back round
        seen.add(info["sel"])
        if not info["visible"]:
            hits.append(_hit("focus-ring-missing", info["sel"],
                             "takes focus with no visible change from its resting style",
                             info["cls"], info["text"]))
        elif info["clip"]:
            hits.append(_hit("focus-ring-clipped", info["sel"],
                             f"its focus ring is cut off by {info['clip']}, which clips its "
                             "overflow", info["cls"], info["text"]))
    return hits


async def _timing_pass(page, reduced: bool) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    names = await page.evaluate(_PRESSABLES_JS, PRESS_LIMIT)
    for i, name in enumerate(names):
        handle = await page.query_selector(f'[data-ux-probe="{i}"]')
        if handle is None:
            continue
        try:
            if not reduced:
                await page.evaluate("(e) => window.__ux.start(e, 'mouseover')", handle)
                await handle.hover(timeout=1000)
                await page.wait_for_timeout(SAMPLE_MS)
                hover = await page.evaluate("() => window.__ux.stop()")
                if hover and hover["t50"] is not None and hover["t50"] > DIRECT_T50 + FRAME_MS:
                    hits.append(_hit("state-answers-late", name,
                                     f"hover reaches half its change at {round(hover['t50'])}ms"))
            else:
                await handle.hover(timeout=1000)
                await page.wait_for_timeout(60)
            await page.evaluate("(e) => window.__ux.start(e, 'pointerdown')", handle)
            await page.mouse.down()
            await page.wait_for_timeout(SAMPLE_MS)
            press = await page.evaluate("() => window.__ux.stop()")
            matrix = await page.evaluate("(e) => getComputedStyle(e).transform", handle)
            await page.mouse.up()
            if reduced and matrix not in ("none", "matrix(1, 0, 0, 1, 0, 0)"):
                hits.append(_hit("press-moves-under-reduced-motion", name,
                                 f"pressed with reduced motion set, it takes {matrix}"))
            elif not reduced and press and press["t50"] is not None \
                    and press["t50"] > DIRECT_T50 + FRAME_MS:
                hits.append(_hit("state-answers-late", name,
                                 f"a press reaches half its change at {round(press['t50'])}ms"))
        except Exception:  # a control covered or moved away by the page is skipped
            await page.mouse.up()
            continue
        await page.mouse.move(0, 0)
    return hits


async def _escape_pass(page) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    names = await page.evaluate(_POPUPS_JS, POPUP_LIMIT)
    for i, name in enumerate(names):
        handle = await page.query_selector(f'[data-ux-popup="{i}"]')
        if handle is None:
            continue
        try:
            await handle.focus()
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(120)
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(120)
        except Exception:  # a trigger the page removed is skipped
            continue
        back = await page.evaluate("(e) => document.activeElement === e", handle)
        if not back:
            where = await page.evaluate(
                "() => { const a = document.activeElement; return !a || a === document.body "
                "? 'the page body' : window.__ux.sel(a); }")
            hits.append(_hit("focus-lost-after-escape", name,
                             f"after Escape closes what it opened, focus lands on {where}"))
    return hits


async def interaction_checks(browser, f: Path) -> List[Dict[str, Any]]:
    """Focus, timing and Escape at each width in WIDTHS, then a press with
    reduced motion at the widest, on pages whose motion runs."""
    hits: List[Dict[str, Any]] = []
    for w, h in WIDTHS:
        page = await browser.new_page(viewport={"width": w, "height": h},
                                      reduced_motion="no-preference")
        try:
            await page.goto(f.resolve().as_uri(), wait_until="load")
            await page.evaluate(_SETUP_JS)
            found = await _focus_pass(page)
            await page.mouse.move(0, 0)
            if (w, h) == WIDTHS[0]:
                found += await _timing_pass(page, reduced=False)
            found += await _escape_pass(page)
            hits.extend(dict(x, vw=w) for x in found)
        finally:
            await page.close()
    page = await browser.new_page(viewport={"width": WIDTHS[0][0], "height": WIDTHS[0][1]},
                                  reduced_motion="reduce")
    try:
        await page.goto(f.resolve().as_uri(), wait_until="load")
        await page.evaluate(_SETUP_JS)
        hits.extend(dict(x, vw=WIDTHS[0][0]) for x in await _timing_pass(page, reduced=True))
    finally:
        await page.close()
    return hits


RULES = {
    "focus-ring-missing": dict(
        name="Focus shows no visible change", severity="high", category="A11y",
        fix=("Give the control a focus indicator: the system's focus ring (color.focus.ring, "
             "border.focus-ring.width and offset) on :focus-visible. An outline: none needs a "
             "replacement that is visible, as 2.4.7 asks."),
        what="{detail} ({vw}px viewport)"),
    "focus-ring-clipped": dict(
        name="Focus ring clipped by an ancestor", severity="medium", category="A11y",
        fix=("Keep the ring inside the clipping box: draw it inset (a negative outline-offset or "
             "an inset shadow), add padding to the scroller, or move overflow clipping off the "
             "ancestor."),
        what="{detail} ({vw}px viewport)"),
    "state-answers-late": dict(
        name="Hover or press answers late", severity="medium", category="Motion",
        fix=("Bind the state change to motion.state (or motion.press for a press): a direct "
             "response is half done within 70ms. Avoid transition: all on a slow ease-in-out "
             "curve; name the properties that change and use the system's curve."),
        what="{detail} ({vw}px viewport)"),
    "focus-lost-after-escape": dict(
        name="Focus lost after Escape", severity="high", category="A11y",
        fix=("When Escape closes a menu, list or dialog, move focus back to the control that "
             "opened it, so a keyboard user carries on from the same place."),
        what="{detail} ({vw}px viewport)"),
    "press-moves-under-reduced-motion": dict(
        name="Press moves under reduced motion", severity="medium", category="Motion",
        fix=("Bind the press scale to motion.press.scale, which is 1 under reduced motion, or set "
             "transform: none on :active inside @media (prefers-reduced-motion: reduce)."),
        what="{detail} ({vw}px viewport)"),
}
