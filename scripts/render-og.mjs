#!/usr/bin/env node
// Render scripts/og-card.html -> docs/og-image.png at 1200x630 (DPR 2 for crispness).
import { spawn } from 'node:child_process';
import { mkdtempSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const SRC = 'file://' + join(process.cwd(), 'scripts/og-card.html');
const OUT = join(process.cwd(), 'docs/og-image.png');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const CHROME = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium'].find((p) => existsSync(p));
if (!CHROME) { console.log('no chrome'); process.exit(2); }

const udd = mkdtempSync(join(tmpdir(), 'ogcap-'));
const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--no-sandbox',
  '--remote-debugging-port=0', '--user-data-dir=' + udd, '--no-first-run',
  '--no-default-browser-check', '--hide-scrollbars', '--force-color-profile=srgb', 'about:blank'], { stdio: 'ignore' });
async function readPort() {
  const f = join(udd, 'DevToolsActivePort');
  for (let i = 0; i < 120; i++) { if (existsSync(f)) { const p = readFileSync(f, 'utf8').split('\n')[0].trim(); if (p) return p; } await sleep(100); }
  throw new Error('no port');
}
function makeCdp(wsUrl) {
  const ws = new WebSocket(wsUrl); let id = 0; const waiters = new Map(); const evq = [];
  const ready = new Promise((res, rej) => { ws.onopen = () => res(); ws.onerror = () => rej(new Error('ws')); });
  ws.onmessage = (m) => { const d = JSON.parse(m.data);
    if (d.id && waiters.has(d.id)) { waiters.get(d.id)(d.result || {}); waiters.delete(d.id); }
    else if (d.method) { for (let i = evq.length - 1; i >= 0; i--) if (evq[i].m === d.method) { evq[i].res(d); evq.splice(i, 1); } } };
  const send = (method, params = {}, sessionId) => new Promise((res) => { const mid = ++id; waiters.set(mid, res); ws.send(JSON.stringify({ id: mid, method, params, sessionId })); });
  const wait = (m, t = 12000) => new Promise((res) => { const w = { m, res }; evq.push(w); setTimeout(() => { const i = evq.indexOf(w); if (i >= 0) { evq.splice(i, 1); res(null); } }, t); });
  return { ready, send, wait };
}
(async () => {
  const port = await readPort();
  const verUrl = (await (await fetch('http://127.0.0.1:' + port + '/json/version')).json()).webSocketDebuggerUrl;
  const cdp = makeCdp(verUrl); await cdp.ready;
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId: sid } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  await cdp.send('Page.enable', {}, sid);
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1200, height: 630, deviceScaleFactor: 2, mobile: false }, sid);
  await cdp.send('Page.navigate', { url: SRC }, sid);
  await cdp.wait('Page.loadEventFired'); await sleep(2600); // fonts + glow settle
  const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', clip: { x: 0, y: 0, width: 1200, height: 630, scale: 2 } }, sid);
  writeFileSync(OUT, Buffer.from(data, 'base64'));
  console.log('wrote', OUT, '(' + Math.round(Buffer.from(data, 'base64').length / 1024) + ' KB)');
  chrome.kill(); process.exit(0);
})().catch((e) => { console.log('crash', e.message); try { chrome.kill(); } catch {} process.exit(2); });
