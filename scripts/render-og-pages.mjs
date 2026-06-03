#!/usr/bin/env node
// Render ALL per-page OG cards -> docs/og/<slug>.png at 2400x1260, in the v3.1
// homepage style (giant cyan 3.1 + brand dot + stats bar). One Chrome session.
import { spawn } from 'node:child_process';
import { mkdtempSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const OUT_DIR = join(process.cwd(), 'docs/og');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const CHROME = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium'].find((p) => existsSync(p));
if (!CHROME) { console.log('no chrome'); process.exit(2); }

// slug -> [eyebrow, title (\n = line break), sub]  (numbers refreshed to v3.1 canon)
const PAGES = {
  "home": ["The design brain for AI coding", "Stop your AI code\nlooking generated.", "A deterministic engine that compiles a real design language per brief."],
  "compare": ["Compare", "Every Claude design\nskill, side by side", "ux-skill 46/50 · next best 30/50"],
  "about": ["About", "Why ux-skill exists", "From the prose-only v1 to the queryable Python engine"],
  "faq": ["FAQ", "25 questions,\nanswered straight", "Install, license, plugin landscape, MCP"],
  "roadmap": ["Roadmap", "What ships next", "v3.1 shipped · the road to v3.5"],
  "mcp": ["MCP server", "18 tools over stdio.\nAny MCP host.", "Claude Desktop · Cursor · Windsurf · generic agents"],
  "blog-index": ["Blog", "Long-form writing on\nAI coding's design problem", "Honest comparisons. Real numbers. No marketing verbs."],
  "vs-ui-ux-pro-max": ["Comparison", "ui-ux-pro-max alternative\n— the honest table", "1,243 entries vs ~600 · 152-rule linter vs none"],
  "anti-ai-slop-claude-skills": ["Ranking", "Anti-AI-slop tools for\nClaude Code in 2026", "taste-skill · hallmark · ux-skill v3.1"],
  "best-claude-code-design-skills-2026": ["Ranking", "Best Claude Code skills\nfor UX/UI design (2026)", "ui-ux-pro-max · open-design · taste-skill · ux-skill"],
  "cursor-design-plugin": ["Integration", "Cursor design plugin", "Install ux-skill via npx · 152-rule linter"],
  "python-design-system-generator": ["Architecture", "Python design system\ngenerator", "1,243 entries · 5 parallel lanes · pip install"],
  "ai-design-fingerprints-list": ["Catalog", "The AI design\nfingerprints, listed", "Detection regex · why each is slop · the fix"],
  "claude-code-marketplace-best-plugins": ["Marketplace", "Best Claude Code\nmarketplace plugins (2026)", "All the popular UX skills · honest ranking"],
  "figma-vs-ux-skill": ["Comparison", "Figma vs ux-skill", "Different jobs · honest table"],
  "windsurf-design-rules": ["Integration", "Windsurf design rules", "Install ux-skill in Windsurf · 152-rule linter"],
  "monorepo-design-system-ai-coding": ["Architecture", "Monorepo design system\nfor AI coding", "One MASTER.md · all agents grounded"],
  "regex-linter-for-ai-coding": ["Tooling", "Regex linter for\nAI coding output", "152 rules · deterministic · no LLM"],
  "dark-editorial-cinema-design": ["Design", "Dark editorial\ncinema design", "Charcoal + variable opsz + scroll-pinned scenes"],
  "mcp-server-design-intelligence": ["MCP", "MCP server for\ndesign intelligence", "18 tools over stdio"],
  "motion-presets-framer-gsap-css": ["Motion", "Motion presets —\nFramer, GSAP, CSS", "57 presets · 8 categories · 3 engines"],
  "dogfooding-design-engine": ["Story", "Dogfooding ux-skill —\nbugs we found", "Engine bugs filed against ourselves · all fixed"],
  "zed-design-plugin": ["Integration", "Zed design plugin", "Install ux-skill in the Rust IDE · 152-rule linter"],
  "github-copilot-design-rules": ["Integration", "GitHub Copilot\ndesign rules", "Catch AI-design fingerprints in Copilot output"],
  "jetbrains-ai-design-system": ["Integration", "JetBrains AI\ndesign system rules", "IntelliJ + WebStorm · 152-rule linter"],
  "ai-design-system-cli": ["Tooling", "AI design system CLI", "10-field discovery · 60-second design language"],
  "claude-desktop-mcp-design": ["MCP", "Claude Desktop + MCP\ndesign intelligence", "ux-skill as stdio server · 18 tools"],
  "commands": ["Reference", "Every slash command,\ndocumented", "25 commands · discover → recommend → generate → lint"],
};

const CSS = readFileSync(join(process.cwd(), 'scripts/og-card.html'), 'utf8').match(/<style>([\s\S]*?)<\/style>/)[1];
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function buildHTML(eyebrow, title, sub){
  const titleHtml = esc(title).replace(/\n/g,'<br>');
  return `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800&family=Inter:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>${CSS}
  h1{font-size:58px}
  .sub{font-size:21px;margin-top:22px}
  .three{font-size:480px}
</style></head><body>
<div class="card"><div class="grid"></div><div class="three">3<em>.</em>1</div>
<div class="inner">
  <div class="top"><span class="dot"></span><span class="brand">uxskill</span><span class="tag">deterministic · offline · no LLM</span></div>
  <div class="mid"><div class="eyebrow">${esc(eyebrow)}</div><h1>${titleHtml}</h1>${sub?`<p class="sub">${esc(sub)}</p>`:''}</div>
  <div class="stats"><span><b>1,243</b> entries</span><span><b>160</b> brand specs</span><span><b>152</b> anti-patterns</span><span><b>17</b> IDEs</span></div>
</div></div></body></html>`;
}

const udd = mkdtempSync(join(tmpdir(), 'ogp-'));
const chrome = spawn(CHROME, ['--headless=new','--disable-gpu','--no-sandbox','--remote-debugging-port=0','--user-data-dir='+udd,'--no-first-run','--no-default-browser-check','--hide-scrollbars','--force-color-profile=srgb','about:blank'], { stdio: 'ignore' });
async function readPort(){const f=join(udd,'DevToolsActivePort');for(let i=0;i<120;i++){if(existsSync(f)){const p=readFileSync(f,'utf8').split('\n')[0].trim();if(p)return p;}await sleep(100);}throw new Error('no port');}
function makeCdp(wsUrl){const ws=new WebSocket(wsUrl);let id=0;const waiters=new Map(),evq=[];const ready=new Promise((res,rej)=>{ws.onopen=()=>res();ws.onerror=()=>rej(new Error('ws'));});ws.onmessage=(m)=>{const d=JSON.parse(m.data);if(d.id&&waiters.has(d.id)){waiters.get(d.id)(d.result||{});waiters.delete(d.id);}else if(d.method){for(let i=evq.length-1;i>=0;i--)if(evq[i].m===d.method){evq[i].res(d);evq.splice(i,1);}}};const send=(method,params={},sessionId)=>new Promise((res)=>{const mid=++id;waiters.set(mid,res);ws.send(JSON.stringify({id:mid,method,params,sessionId}));});const wait=(m,t=12000)=>new Promise((res)=>{const w={m,res};evq.push(w);setTimeout(()=>{const i=evq.indexOf(w);if(i>=0){evq.splice(i,1);res(null);}},t);});return{ready,send,wait};}
(async()=>{
  const port=await readPort();
  const verUrl=(await (await fetch('http://127.0.0.1:'+port+'/json/version')).json()).webSocketDebuggerUrl;
  const cdp=makeCdp(verUrl);await cdp.ready;
  const {targetId}=await cdp.send('Target.createTarget',{url:'about:blank'});
  const {sessionId:sid}=await cdp.send('Target.attachToTarget',{targetId,flatten:true});
  await cdp.send('Page.enable',{},sid);
  await cdp.send('Emulation.setDeviceMetricsOverride',{width:1200,height:630,deviceScaleFactor:2,mobile:false},sid);
  let first=true;
  for(const [slug,[eyebrow,title,sub]] of Object.entries(PAGES)){
    const html=buildHTML(eyebrow,title,sub);
    const tmp=join(udd,slug.replace(/[^a-z0-9-]/gi,'_')+'.html');
    writeFileSync(tmp,html);
    await cdp.send('Page.navigate',{url:'file://'+tmp},sid);
    await cdp.wait('Page.loadEventFired');
    await sleep(first?2600:900); first=false; // fonts cached after first
    const {data}=await cdp.send('Page.captureScreenshot',{format:'png',clip:{x:0,y:0,width:1200,height:630,scale:1}},sid);
    const out=join(OUT_DIR, slug+'.png');
    writeFileSync(out,Buffer.from(data,'base64'));
    console.log('  '+slug+'.png');
  }
  chrome.kill();console.log('done');process.exit(0);
})().catch((e)=>{console.log('crash',e.message);try{chrome.kill();}catch{}process.exit(2);});
