#!/usr/bin/env node
// Render ALL per-page OG cards -> docs/og/<slug>.png at 2400x1260, in the
// homepage style (giant cyan release numeral + brand dot + stats bar). One Chrome session.
import { spawn } from 'node:child_process';
import { mkdtempSync, existsSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const OUT_DIR = join(process.cwd(), 'docs/og');
// The giant numeral is the release line from pyproject.toml, e.g. 3.2.
const LINE = readFileSync(join(process.cwd(), 'pyproject.toml'), 'utf8').match(/^version\s*=\s*"(\d+\.\d+)/m)[1];
// Slugs on the command line render only those cards: node scripts/render-og-pages.mjs home faq
const ONLY = process.argv.slice(2);
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
  "roadmap": ["Roadmap", "What ships next", `v${LINE} shipped · the render check is live`],
  "mcp": ["MCP server", "18 tools over stdio.\nAny MCP host.", "Claude Desktop · Cursor · Windsurf · generic agents"],
  "blog-index": ["Blog", "Long-form writing on\nAI coding's design problem", "Honest comparisons. Real numbers. No marketing verbs."],
  "vs-ui-ux-pro-max": ["Comparison", "ui-ux-pro-max alternative:\nthe honest table", "1,243 entries vs ~600 · 152-rule linter vs none"],
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
  "motion-presets-framer-gsap-css": ["Motion", "Motion presets for\nFramer, GSAP, CSS", "57 presets · 8 categories · 3 engines"],
  "dogfooding-design-engine": ["Story", "Dogfooding ux-skill:\nbugs we found", "Engine bugs filed against ourselves · all fixed"],
  "zed-design-plugin": ["Integration", "Zed design plugin", "Install ux-skill in the Rust IDE · 152-rule linter"],
  "github-copilot-design-rules": ["Integration", "GitHub Copilot\ndesign rules", "Catch AI-design fingerprints in Copilot output"],
  "jetbrains-ai-design-system": ["Integration", "JetBrains AI\ndesign system rules", "IntelliJ + WebStorm · 152-rule linter"],
  "ai-design-system-cli": ["Tooling", "AI design system CLI", "10-field discovery · 60-second design language"],
  "claude-desktop-mcp-design": ["MCP", "Claude Desktop + MCP\ndesign intelligence", "ux-skill as stdio server · 18 tools"],
  "commands": ["Reference", "Every slash command,\ndocumented", "25 commands · discover → recommend → generate → lint"],
  // Blog posts whose og:image had no card (English and translated posts).
  "ai-built-website-no-slop": ["Blog", "AI-built websites in 2026 · why every one looks the same", ""],
  "ai-design-system-figma-to-code": ["Blog", "From Figma to code without losing the design system", ""],
  "anti-slop-cli-vibe-coders": ["Blog", "The anti-slop CLI for vibe coders, 145 rules, no LLM, runs in CI", ""],
  "ar-ai-coding-design-arabic": ["Blog · العربية", "تصميم برمجة الذكاء الاصطناعي, كيف تبني نظام تصميم لـ Claude Code", ""],
  "ar-v3-the-brain": ["Blog · العربية", "ux-skill v3.0 · أطلقنا The Brain. مواصفات العلامات صارت بيانات تدريب لا قوالب.", ""],
  "best-ai-coding-tools-2026-design-quality": ["Blog", "Best AI coding tools for design-quality output in 2026", ""],
  "de-ki-coding-design-deutsch": ["Blog · Deutsch", "KI-Coding Design · wie man ein Cursor-AI-Designsystem baut", ""],
  "de-v3-the-brain": ["Blog · Deutsch", "ux-skill v3.0 · The Brain. Brand-Specs sind Trainingsdaten, keine Templates.", ""],
  "es-diseno-ai-coding-espanol": ["Blog · Español", "Reglas de diseño para coding con IA · por qué toda IA genera la misma UI", ""],
  "es-v3-the-brain": ["Blog · Español", "ux-skill v3.0 · lanzamos The Brain. Las brand specs son datos de entrenamiento, no plantillas.", ""],
  "fr-ia-coding-design-francais": ["Blog · Français", "IA coding design · construire un système de design pour Claude Code", ""],
  "fr-v3-the-brain": ["Blog · Français", "ux-skill v3.0 · The Brain. Les brand specs sont des données d'entraînement, pas des templates.", ""],
  "hi-ai-coding-design-rules": ["Blog · हिन्दी", "AI कोडिंग के लिए डिज़ाइन नियम, हर AI एक जैसी UI क्यों बनाता है", ""],
  "hi-mcp-server-design-india": ["Blog · हिन्दी", "MCP सर्वर, AI डिज़ाइन इंजन को Claude Desktop में जोड़ना", ""],
  "it-ai-coding-design-italian": ["Blog · Italiano", "Design AI coding · come costruire un design system con Claude Code", ""],
  "ja-ai-coding-design-japanese": ["Blog · 日本語", "AI コーディング デザイン, Claude Code デザインシステムの作り方", ""],
  "ja-ai-design-system-cli": ["Blog · 日本語", "AI 設計システム CLI, Claude Code と Cursor のためのデザインインテリジェンス", ""],
  "ja-v3-the-brain": ["Blog · 日本語", "ux-skill v3.0 · The Brain をリリース。ブランド仕様はテンプレートではなく訓練データに。", ""],
  "ja-vibe-coding-design": ["Blog · 日本語", "「Vibe coding」でAIが書いたUIが毎回同じに見える理由", ""],
  "ko-ai-coding-design-korean": ["Blog · 한국어", "AI 코딩 디자인 · Claude Code 디자인 시스템을 만드는 법", ""],
  "ko-ai-coding-design-rules": ["Blog · 한국어", "AI 코딩 시대의 디자인 규칙 · 왜 모든 AI가 같은 UI를 만드는가", ""],
  "ko-cursor-design-rules-korean": ["Blog · 한국어", "Cursor 디자인 규칙 · AI 코딩의 디자인 슬롭을 막는 방법", ""],
  "pt-BR-ai-coding-design-portuguese": ["Blog · Português", "Design para programação com IA · como montar um sistema no Claude Code", ""],
  "pt-br-design-ai-coding-brasil": ["Blog · Português", "Regras de design para AI coding, por que toda IA produz a mesma UI?", ""],
  "v3-the-brain-launch": ["Blog", "ux-skill v3.0 · we shipped The Brain. Brand specs are training data, not templates.", ""],
  "vi-anti-ai-slop-vietnam": ["Blog · Tiếng Việt", "Chống AI slop trong thiết kế web, cho người Việt dùng AI coding", ""],
  "vibe-coding-design-system": ["Blog", "Vibe coding is real · but your AI still ships the same defaults", ""],
  "zh-CN-ai-coding-design-chinese": ["Blog · 简体中文", "AI 编程设计, 用 ux-skill 给 Cursor 设计系统兜底", ""],
  "zh-CN-anti-ai-slop-cli-china": ["Blog · 简体中文", "AI Slop CLI,145 条规则,无 LLM,在 CI 中运行", ""],
  "zh-CN-v3-the-brain": ["Blog · 简体中文", "ux-skill v3.0 · 我们发布了 The Brain。品牌规范是训练数据,不是模板。", ""],
  "zh-vibe-coding-shipping-real-design": ["Blog · 简体中文", "用 Vibe Coding 做出真正能交付的设计,而非 AI 默认渐变", ""],
  "zh-tw-ai-coding-design": ["Blog · 繁體中文", "AI 編程的設計規則,為什麼每個 AI 寫出來的網站都長得一樣", ""],
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
<div class="card"><div class="grid"></div><div class="three">${LINE.split(".")[0]}<em>.</em>${LINE.split(".")[1]}</div>
<div class="inner">
  <div class="top"><span class="dot"></span><span class="brand">uxskill</span><span class="tag">deterministic · offline · no LLM</span></div>
  <div class="mid"><div class="eyebrow">${esc(eyebrow)}</div><h1 dir="auto">${titleHtml}</h1>${sub?`<p class="sub" dir="auto">${esc(sub)}</p>`:''}</div>
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
    if(ONLY.length && !ONLY.includes(slug)) continue;
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
