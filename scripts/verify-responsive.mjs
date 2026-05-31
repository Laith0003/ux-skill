#!/usr/bin/env node
/**
 * verify-responsive.mjs - the REAL responsive gate.
 *
 * Renders a page in headless Chrome at TRUE mobile viewports (via the DevTools
 * Emulation domain, not a lying harness), MEASURES real horizontal overflow +
 * sticky-chrome height, and writes a screenshot per viewport so a human can SEE it.
 *
 * The honesty contract (this is the whole point - a gate that cannot render must
 * never report green):
 *   exit 0  = VERIFIED and clean
 *   exit 1  = VERIFIED and FAILED (real horizontal scroll / over-tall sticky header)
 *   exit 2  = DEGRADED / UNVERIFIED (no Chrome, or the viewport could not be trusted)
 *             -> you have NOT verified. Eyeball on a real device. Do NOT claim passed.
 *
 * Usage: node scripts/verify-responsive.mjs <file-or-url> [widths=360,390] [outdir=.]
 * Chrome path override: CHROME_BIN=/path/to/chrome
 * Needs only Node 21+ (built-in fetch + WebSocket) and a Chrome/Chromium binary.
 */
import { spawn } from 'node:child_process';
import { mkdtempSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const STICKY_CEILING = 96;        // px; a taller pinned header is a fail
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function degrade(msg) {
  console.log('DEGRADED (UNVERIFIED): ' + msg);
  console.log('  A gate that cannot render has NOT verified. Eyeball on a real device; never claim passed.');
  process.exit(2);
}

const target = process.argv[2];
if (!target) degrade('no target given (usage: verify-responsive.mjs <file-or-url> [widths] [outdir])');
const widths = (process.argv[3] || '360,390').split(',').map((n) => parseInt(n, 10)).filter(Boolean);
const outDir = process.argv[4] || '.';
const url = /^(https?|file):/.test(target)
  ? target
  : 'file://' + (target.startsWith('/') ? target : join(process.cwd(), target));

const CHROME = process.env.CHROME_BIN ||
  ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
   '/Applications/Chromium.app/Contents/MacOS/Chromium',
   '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser']
   .find((p) => existsSync(p));
if (!CHROME) degrade('no Chrome/Chromium binary found (set CHROME_BIN)');

const MEASURE = `(()=>{
  const d=document.documentElement, vw=window.innerWidth;
  const all=[...document.querySelectorAll('body *')];
  const over=all.filter(e=>{const r=e.getBoundingClientRect();const c=getComputedStyle(e);
      return (r.right>vw+1||r.left<-1)&&r.width>0&&r.height>0&&c.position!=='fixed'&&c.visibility!=='hidden';})
    .sort((a,b)=>b.getBoundingClientRect().right-a.getBoundingClientRect().right).slice(0,6)
    .map(e=>({tag:e.tagName.toLowerCase(),cls:(typeof e.className==='string'?e.className.trim().split(/\\s+/)[0]:''),
      right:Math.round(e.getBoundingClientRect().right),text:(e.textContent||'').replace(/\\s+/g,' ').trim().slice(0,30)}));
  const st=all.concat([d]).filter(e=>{const c=getComputedStyle(e);if(c.position!=='sticky'&&c.position!=='fixed')return false;
      const t=parseFloat(c.top);return isFinite(t)&&Math.abs(t)<=1&&e.getClientRects().length;});
  const outer=st.filter(e=>!st.some(o=>o!==e&&o.contains(e)));
  return {innerWidth:vw,scrollWidth:d.scrollWidth,clientWidth:d.clientWidth,
    stickyH:outer.reduce((s,e)=>s+e.offsetHeight,0),
    vp:(document.querySelector('meta[name=viewport]')||{}).content||'(none)'};
})()`;

const udd = mkdtempSync(join(tmpdir(), 'uxverify-'));
let chrome;
try {
  chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox',
    '--hide-scrollbars=false', '--remote-debugging-port=0', '--user-data-dir=' + udd,
    '--no-first-run', '--no-default-browser-check', 'about:blank'], { stdio: 'ignore' });
} catch (e) { degrade('cannot launch Chrome: ' + e.message); }
chrome.on('error', (e) => degrade('Chrome process error: ' + e.message));

async function readPort() {
  const f = join(udd, 'DevToolsActivePort');
  for (let i = 0; i < 100; i++) { if (existsSync(f)) { const p = readFileSync(f, 'utf8').split('\n')[0].trim(); if (p) return p; } await sleep(100); }
  degrade('Chrome never opened a debugging port');
}

function makeCdp(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0; const waiters = new Map(); const evq = [];
  const ready = new Promise((res, rej) => { ws.onopen = () => res(); ws.onerror = (e) => rej(new Error('ws error')); });
  ws.onmessage = (m) => {
    const d = JSON.parse(m.data);
    if (d.id && waiters.has(d.id)) { waiters.get(d.id)(d.result || {}); waiters.delete(d.id); }
    else if (d.method) { for (let i = evq.length - 1; i >= 0; i--) if (evq[i].m === d.method) { evq[i].res(d); evq.splice(i, 1); } }
  };
  const send = (method, params = {}, sessionId) => new Promise((res) => { const mid = ++id; waiters.set(mid, res); ws.send(JSON.stringify({ id: mid, method, params, sessionId })); });
  const wait = (m, t = 8000) => new Promise((res) => { const w = { m, res }; evq.push(w); setTimeout(() => { const i = evq.indexOf(w); if (i >= 0) { evq.splice(i, 1); res(null); } }, t); });
  return { ready, send, wait };
}

(async () => {
  const port = await readPort();
  let verUrl;
  try { verUrl = (await (await fetch('http://127.0.0.1:' + port + '/json/version')).json()).webSocketDebuggerUrl; }
  catch (e) { degrade('could not reach Chrome DevTools endpoint'); }
  const cdp = makeCdp(verUrl);
  try { await cdp.ready; } catch (e) { degrade('could not open a CDP WebSocket'); }

  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  await cdp.send('Page.enable', {}, sessionId);

  // Self-calibrate: confirm Chrome honors device-metrics overrides in THIS env. If a
  // width=device-width baseline does not report the set width, the verifier itself cannot
  // be trusted -> degrade (never mislabel a render failure as a page pass/fail).
  {
    const cw = widths[0];
    await cdp.send('Emulation.setDeviceMetricsOverride', { width: cw, height: 800, deviceScaleFactor: 2, mobile: true, screenWidth: cw, screenHeight: 800 }, sessionId);
    await cdp.send('Page.navigate', { url: 'data:text/html,<!doctype html><meta name=viewport content="width=device-width,initial-scale=1"><body style="margin:0">cal' }, sessionId);
    await cdp.wait('Page.loadEventFired'); await sleep(120);
    const { result } = await cdp.send('Runtime.evaluate', { expression: 'window.innerWidth', returnByValue: true }, sessionId);
    if (!result || result.value !== cw) degrade('Chrome ignored a width=device-width baseline (' + (result && result.value) + ' != ' + cw + ') - cannot trust measurements here');
  }

  let failed = false; const lines = []; const shots = [];
  for (const w of widths) {
    await cdp.send('Emulation.setDeviceMetricsOverride',
      { width: w, height: 900, deviceScaleFactor: 2, mobile: true, screenWidth: w, screenHeight: 900 }, sessionId);
    await cdp.send('Page.navigate', { url }, sessionId);
    await cdp.wait('Page.loadEventFired');
    await sleep(450); // let fonts + layout settle
    const { result } = await cdp.send('Runtime.evaluate', { expression: MEASURE, returnByValue: true }, sessionId);
    const v = result && result.value;
    if (!v) degrade('could not measure the page at ' + w + 'px');
    const shot = join(outDir, 'verify-' + w + '.png');
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'png' }, sessionId);
    writeFileSync(shot, Buffer.from(data, 'base64')); shots.push(shot);
    if (v.innerWidth > w) {
      // Calibration proved Chrome honors the device width, so a page rendering WIDER than
      // the device is a real page failure (bad viewport meta / a fixed min-width) -> the
      // exact cause of horizontal scroll on a real phone.
      failed = true;
      lines.push('  ' + w + 'px: PAGE DOES NOT FIT THE DEVICE (innerWidth=' + v.innerWidth + ' at a ' + w + 'px device) -> horizontal scroll on real phones. Usual cause: a bad <meta name="viewport"> (got "' + v.vp + '") or a fixed min-width wider than the device. | shot ' + shot);
      continue;
    }
    const hscroll = v.scrollWidth > v.innerWidth + 1;
    const tallSticky = v.stickyH > STICKY_CEILING;
    if (hscroll || tallSticky) failed = true;
    lines.push('  ' + w + 'px: scrollWidth=' + v.scrollWidth + ' vs ' + v.innerWidth +
      (hscroll ? '  H-SCROLL (FAIL)' : '  ok') + ' | sticky=' + v.stickyH + 'px' +
      (tallSticky ? ' (FAIL >' + STICKY_CEILING + ')' : '') + ' | shot ' + shot);
    if (hscroll && v.over.length) for (const o of v.over) lines.push('      overflow: <' + o.tag + ' .' + o.cls + '> right=' + o.right + '  "' + o.text + '"');
  }
  chrome.kill();
  console.log((failed ? 'FAIL' : 'VERIFIED clean') + ' - responsive @ ' + widths.join('/') + 'px (real headless Chrome)');
  console.log(lines.join('\n'));
  console.log('  screenshots: ' + shots.join(', '));
  process.exit(failed ? 1 : 0);
})().catch((e) => degrade('verifier crashed: ' + (e && e.message)));
