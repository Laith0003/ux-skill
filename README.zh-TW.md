[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · **繁體中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — 為 Claude Code、Cursor 及一切 AI 程式設計工具打造的設計智慧引擎

> **AI 程式設計領域最強的 UX 外掛。** 一個由 Python 驅動的推理核心,包含 11 份可查詢的 JSON 清單(84 種風格、176 套配色、70 組字體搭配、148 個元件、184 個產業、35 種圖表類型、57 個動效預設、112 條 UX 法則、120 條反模式規則、25 個技術堆疊、131 份品牌規範)、22 個斜線命令、5 個子代理,以及一個確定性的反 AI-slop 程式碼檢查器。跨 IDE 支援:可安裝到 Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、Kiro、Cline、Continue、Aider、Zed、JetBrains AI、Pieces、Tabby、Tabnine、CodeWhisperer 以及 Roo Cline。

> **品牌名稱是 `ux-skill`。** PyPI / npm 上的套件名稱仍然是 `uxskill`。GitHub 儲存庫位於 [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)。

**官網:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **與每個 Claude UX 外掛的對照:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-2.0.0--alpha.1-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#面向-17-個-ide-的安裝程式)
[![Brands](https://img.shields.io/badge/brand_specs-110-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-120-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Star 歷史

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill 是什麼

ux-skill 是一個面向 AI 程式設計工具的**設計智慧引擎**。它以 Python 套件的形式運行(`pip install uxskill`),也作為 Claude Code 外掛運行,同時提供一個面向 17 個 IDE 的多重安裝程式。引擎接收一份專案簡報(產業、受眾、語氣、必備項、禁忌項、技術堆疊、地區),並回傳一套完整的推薦設計系統:風格、配色、字體搭配、動效預設、元件、可供研習的品牌範例,以及必須堅守的反模式護欄。該推薦是確定性的——相同輸入永遠產出相同結果。

這個外掛位於你與 AI 程式設計工具之間。當你讓 Claude Code、Cursor 或任何其他 AI 助理「做一個金融科技著陸頁」時,助理通常會即興發揮——結果在五秒鐘內就能被識別為 AI 生成(紫到藍的漸層、三張等大的卡片、用 Inter 做超大顯示字、推薦語裡出現「John Doe」、預設 300ms 的轉場、置中 hero、CTA 上跳動的箭頭)。ux-skill 用**結構化的約束**替代即興:你跑 `/ux-discover` 擷取簡報,跑 `/ux-recommend` 選定系統,跑 `/ux-design` 生成程式碼,再跑 `/ux-lint` 在提交前驗證它通過 100 條確定性反 AI-slop 規則。

這份 README 是權威參考。每一個命令、每一個子代理、每一份資料清單、每一條安裝路徑、每一份品牌規範、每一類反模式——全都記錄在這裡。如果你正在挑選 Claude Code 的設計外掛,或者在為 Cursor、Windsurf 或 Codex 比較 AI 設計工具,請把這篇從頭到尾讀一遍,並對照 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 目錄

1. [快速安裝](#快速安裝)
2. [數據對照——與 Top 8 Claude UX 技能的即時比較](#數據對照與-top-8-claude-ux-技能的即時比較)
3. [架構——各部件如何咬合](#架構各部件如何咬合)
4. [22 個斜線命令——詳細參考](#22-個斜線命令詳細參考)
5. [5 個子代理](#5-個子代理)
6. [11 份資料清單](#11-份資料清單)
7. [120 條反 AI-slop 規則——程式碼檢查器](#120-條反-ai-slop-規則程式碼檢查器)
8. [131 份 DESIGN.md 品牌規範——按類別](#131-份-designmd-品牌規範按類別)
9. [MCP 伺服器——非對稱的一著](#mcp-伺服器非對稱的一著)
10. [面向 17 個 IDE 的安裝程式](#面向-17-個-ide-的安裝程式)
11. [使用案例——具體場景](#使用案例具體場景)
12. [與其他方案的對照](#與其他方案的對照)
13. [路線圖](#路線圖)
14. [參與貢獻](#參與貢獻)
15. [授權、作者、致謝](#授權作者致謝)

---

## 快速安裝

三條安裝路徑。請挑選與你的環境匹配的那條。

### 路徑 1 — Claude Code 市集(權威路徑)

如果你常駐 Claude Code,請透過外掛市集安裝:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

這會將全部 22 個斜線命令與 5 個子代理接入你的 Claude Code 會話。安裝完成後,執行 `/ux-init` 以建立專案層級的 `.ux/` 狀態目錄,並核實 Python 引擎可達。

### 路徑 2 — pip(通用路徑)

如果你身處 Claude Code 之外(Cursor、Windsurf、CLI、CI),請安裝 Python 套件:

```bash
pip install uxskill
uxskill init                       # 自動識別 IDE,安裝對應的產出物
uxskill stats                      # 印出清單計數以驗證安裝
uxskill lint .                     # 對當前目錄執行程式碼檢查器
```

套件同時暴露 `ux` 與 `uxskill` 兩個 CLI 入口點——它們是同一個執行檔。

### 路徑 3 — npx(無需自行管理 Python)

如果你不想直接管理 Python,npx 包裝層會透過 `pipx` 自動拉起:

```bash
npx uxskill init                  # 首次執行時會下載 pipx + uxskill
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### 驗證安裝

```bash
ux stats
# {
#   "version": "2.0.0-alpha.1",
#   "counts": {
#     "styles": 84,
#     "palettes": 176,
#     "type-pairs": 70,
#     "components": 148,
#     "industries": 184,
#     "chart-types": 35,
#     "tech-stacks": 25,
#     "ux-guidelines": 112,
#     "motion-presets": 57,
#     "anti-patterns": 100,
#     "brands": 110
#   }
# }
```

如果任一計數回傳 0,意味著對應的 JSON 檔案缺失——請到 [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) 開個 issue。

---

## 數據對照——與 Top 8 Claude UX 技能的即時比較

Star 數最後一次透過 `gh api` 核對的時間是 **2026-05-28**。ux-skill(Laith0003/ux-skill)是最新入場的——我們在認知度上極小,在架構深度上極深。下面這張表是誠實的:哪裡我們輸,哪裡我們贏。

| 外掛 | Star 數 | 架構 | 斜線命令 | 程式碼檢查器(可上 CI) | 品牌規範 | 元件 | 動效預設 | 支援的 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV,單一 skill | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 個 skill + 預覽 | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + 研究背書的品味 | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 單份 62 KB SKILL.md + 指令稿 | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | 接入 MCP 的 skill 庫 | 多個 | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 單一美學 skill | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 反 slop 設計 skill | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 元件 + 稽核 | 1 | — | (僅 MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python 引擎 + 11 份清單 + 22 個命令 + 5 個子代理 + CI 檢查器** | **22** | **120 條 regex 規則** | **110** | **148** | **57** | **17** |

### 我們輸在哪裡

- **認知度。** 他們有數十萬顆 star。我們有 14 顆。給我們點個 star——這是成本最低的支持方式。
- **品牌識別度。** ui-ux-pro-max 和 open-design 的領先優勢是按月算的,不是按天。
- **行銷打磨。** 他們有截圖、示範影片和可被搜尋到的著陸頁。我們有一份完備的 README 和一張輕量的著陸頁。

### 我們贏在哪裡

- **元件庫:** 148 個帶解剖結構、狀態、所用 token 與動效規範的文件化元件。其他 8 個裡沒有任何一個發布過元件清單。
- **動效預設:** 57 個開箱即用的堆疊層級項目(Framer Motion、GSAP、CSS),全部帶 reduced-motion 後援。其他幾家都不發布動效清單。
- **反模式程式碼檢查器:** 120 條確定性 regex 規則,能在 CI 中執行,遇 Critical/High 結束非零碼。其他幾家沒有任何確定性檢查器。
- **品牌規範:** 110 份真實 DESIGN.md 規範(Apple、Stripe、Linear、Figma、Tesla、BMW、Notion、Spotify、Airbnb、Vercel、Supabase、Cursor、Raycast、Claude,以及其餘 96 個)。其他幾家沒有品牌庫。
- **支援 17 個 IDE:** 同一個引擎,IDE 之間用不同的「膠水」對接。
- **22 個斜線命令:** discovery、生成、稽核、lint、polish、修復循環、案例研究、工作坊、文案、動效、a11y、dashboard、conductor——彼此完全打通。

完整的逐欄對照詳見 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 架構——各部件如何咬合

```
ux-skill (套件名: uxskill)
│
├── data/                              大腦——可查詢的 JSON 清單
│   ├── styles.json                    84 種設計風格 + when/skip + tokens
│   ├── palettes.json                  176 套配色(明/暗,對比度已核)
│   ├── type-pairs.json                70 組 display × body × mono 三元組
│   ├── components.json                148 個元件(解剖、狀態、動效)
│   ├── industries.json                184 條產業規則 + 受眾訊號
│   ├── chart-types.json               35 種圖表(when/skip,編碼)
│   ├── tech-stacks.json               25 個技術堆疊(Next、Astro、SvelteKit、Blade...)
│   ├── ux-guidelines.json             112 條具名 UX 法則(Hick、Fitts、Miller...)
│   ├── motion-presets.json            57 個動效預設(進場、出場、hover...)
│   ├── anti-patterns.json             120 條 regex 規則(CI 安全的檢查器來源)
│   └── brands/*.json                  110 份 DESIGN 規範 + _index.json
│
├── engine/                            Python——推理層
│   ├── recommender/                   五路平行檢索的合併引擎
│   ├── linter/                        確定性反 slop 掃描器
│   ├── discovery/                     10 欄位強制協定
│   ├── generator/                     token + 清單發射器
│   ├── installer/                     面向 17 個 IDE 的多重安裝程式
│   └── cli/                           `ux` / `uxskill` 入口點
│
├── commands/                          22 個 Claude Code 斜線命令(.md)
│   ├── ux-init.md                     初始化
│   ├── ux-stats.md                    存貨快照
│   ├── ux-discover.md                 10 欄位收件(關卡)
│   ├── ux-recommend.md                旗艦——五路平行檢索
│   ├── ux-lint.md                     確定性檢查器
│   ├── ux-design.md                   生成前端程式碼
│   ├── ux-component.md                生成單個元件
│   ├── ux-system.md                   生成完整設計系統
│   ├── ux-dashboard.md                生成儀表板介面
│   ├── ux-motion.md                   動效處理 + 稽核
│   ├── ux-audit.md                    六鏡頭設計稽核
│   ├── ux-a11y.md                     WCAG 2.1 AA 稽核
│   ├── ux-critique.md                 品味評點(3 個亮點、3 個失分、1 步關鍵招)
│   ├── ux-copy.md                     微文案稽核 + 重寫
│   ├── ux-fix.md                      以原子提交落地稽核結果
│   ├── ux-polish.md                   拋光 + 清除 AI-slop
│   ├── ux-frame.md                    4 欄位定調區塊
│   ├── ux-research.md                 研究計畫 + 綜合
│   ├── ux-workshop.md                 五階段設計思考工作坊
│   ├── ux-case-study.md               可發布的 Wfrah 編輯風格案例研究
│   ├── ux-next.md                     工作流指揮(唯讀)
│   └── ux-expert.md                   諮詢入口
│
├── agents/                            5 個子代理(.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 品牌聲音的微文案
│   ├── research-synthesizer.md        訪談 + 分析 + 競品
│   └── design-system-architect.md     tokens / 元件 / 基礎
│
├── references/                        資料的散文化原文 + 示範頁面
│   ├── foundations/                   anti-patterns.md、原則、品味
│   ├── laws/                          UX 法則長文
│   ├── process/                       discovery-protocol.md(關鍵)
│   ├── styles/                        風格散文(anti-slop.md 等)
│   ├── components/                    元件長文
│   ├── output/                        輸出量規
│   └── conditional/                   按技術堆疊的特定指引
│
├── bin/
│   ├── uxskill.mjs                    npx 包裝 -> Python 引擎
│   ├── ux-lint.py                     v2 檢查器(優先)
│   └── ux-lint.sh                     v1 後援(bash + perl-PCRE)
│
└── .ux/                               (按專案生成)
    ├── last-discovery.json            簡報快照
    ├── last-recommendation.json       選定的系統
    ├── last-frame.json                定調區塊
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### 引擎到底是怎麼運作的

1. **輸入。** 你提供一份簡報——可透過 `/ux-discover` 互動式填寫(10 個欄位),也可透過給 `ux recommend` 傳 flag 的方式非互動填寫。
2. **五路平行檢索。** 引擎在清單之間並行跑五次查詢:
   - **產業 → 推薦風格**(industries.json)
   - **風格 → 配色 + 字體 + 動效的相容性**(styles.json)
   - **語氣 × 必備項 → 配色過濾**(palettes.json)
   - **技術堆疊 → 元件相容性 + 動效預設**(tech-stacks.json、motion-presets.json)
   - **禁忌項 + 地區 → 護欄 + 品牌範例候選**(anti-patterns.json、brands/)
3. **合併。** 一個確定性的合併器對候選項排序、化解衝突(例如,「必備暗色模式」會強制配色模式),最終給出唯一的推薦系統。
4. **輸出。** 一份 JSON,內含選定的風格、配色、字體搭配、動效 Top 5、元件 Top 12、品牌範例 Top 5,以及全部 120 條反模式護欄的啟用狀態。外加一段說明,逐項解釋為什麼這樣選。
5. **生成。** 下游命令(`/ux-design`、`/ux-component`、`/ux-system`、`/ux-dashboard`)讀取推薦結果,透過子代理生成實際程式碼。
6. **驗證。** `/ux-lint` 用 120 條 regex 規則再掃一遍生成出的程式碼。在 CI 中遇 Critical/High 結束非零碼。

**Python 思考。HTML 展示。Markdown 串聯。**

---

## 22 個斜線命令——詳細參考

每個命令以 `commands/` 下的 `.md` 檔案發布,包含 `description`、`allowed-tools`、`triggers`、`when to use`、`when to skip`、`input`、`process`、`output state file`。下文是濃縮版說明;完整原始檔才是權威規格。

命令分為五大類:**初始化與存貨**、**discovery 與推薦**、**生成**、**稽核與驗證**、**修復與拋光**,以及**指揮**。

### 初始化與存貨

#### `/ux-init` — 為專案做初始化

- **做什麼:** 識別你在哪個 IDE(`.claude/`、`.cursor/`、`.windsurf/` 等),安裝匹配的產出物,核實 Python 引擎可達,印出一份統計快照。
- **何時使用:** 在新專案裡首次安裝;clone 了使用 ux-skill 的專案之後;`pip install --upgrade uxskill` 之後。
- **何時跳過:** 你已經在這個專案裡跑過,而且沒有任何變動。
- **呼叫方式:** `/ux-init`(無參數)或在 CLI 裡跑 `uxskill init`。
- **輸出:** 各 IDE 對應的產出物(詳見[面向 17 個 IDE 的安裝程式](#面向-17-個-ide-的安裝程式))+ `.ux/` 目錄 + 標準輸出摘要。
- **下接:** 接下來是 `/ux-discover`。

#### `/ux-stats` — 印出資料存貨

- **做什麼:** 印出版本號以及 11 份資料清單的項目計數,便於核對你裝了什麼。
- **何時使用:** 安裝後、升級後;以及當 `/ux-recommend` 給出意外結果、你懷疑清單不完整時。
- **何時跳過:** 從不——它是個 50 ms 的唯讀命令。
- **呼叫方式:** `/ux-stats` 或 `uxskill stats`。
- **輸出:** 標準輸出的 JSON(見上方[驗證安裝](#驗證安裝))。
- **下接:** 僅用於診斷,不餵任何下游流程。

### discovery 與推薦

#### `/ux-discover` — 強制函式(10 欄位收件)

- **做什麼:** 每個專案在跑任何生成類命令之前必經的 10 欄位強制收件。專案類型、受眾、首要目標、語氣、必備項、禁忌項、參考品牌、技術堆疊、地區、成功指標。**杜絕即興。** 被禁短語(「現代」、「乾淨」)會逼著使用者講得具體。
- **何時使用:** 在任何 `/ux-design`、`/ux-component`、`/ux-system` 或 `/ux-dashboard` 之前;以及任何先前簡報已經過期時。
- **何時跳過:** 你在修 bug(`/ux-fix`);你只跑一次 lint(`/ux-lint`);簡報和上次會話保持不變。
- **呼叫方式:** `/ux-discover`。外掛問,你答。
- **輸出:** 寫入 `.ux/last-discovery.json`(10 欄位簡報)。
- **下接:** `/ux-recommend` → 據 discovery 選風格、配色、字體、動效與元件;`/ux-design [補充簡報]` → 在推薦結果上生成前端程式碼;`/ux-component <名稱>` → 在 discovery 約束下生成單個元件。

#### `/ux-recommend` — 旗艦五路平行檢索引擎

- **做什麼:** 在 11 份清單之間跑 Python 引擎的五路平行檢索,回傳一套合併後的設計系統。產業 → 風格 → 配色 → 字體 → 動效 + 元件 + 品牌範例 + 護欄。
- **何時使用:** 從零起一個新專案;為做疲了的產品做轉向;在 `/ux-design` 或 `/ux-component` 之前的預檢。
- **何時跳過:** 你已經跑過 `/ux-discover` 並儲存了簡報——在該流程裡 `/ux-recommend` 是自動銜接的;你在修 bug(用 `/ux-fix`);你只需要 lint(用 `/ux-lint`)。
- **呼叫方式(Claude Code):**
  ```
  /ux-recommend
  ```
  **呼叫方式(CLI):**
  ```bash
  ux recommend \
    --project-type=landing \
    --industry=fintech-neobank \
    --tone=warm --tone=editorial \
    --must-have=dark-mode --must-have=a11y-AA \
    --forbidden=brutalism --forbidden=purple-gradients \
    --stack=nextjs-15-app-router \
    --region=mena
  ```
- **輸出:** 寫入 `.ux/last-recommendation.json` —— 選定的風格、選定的配色、選定的字體搭配、動效 Top 5、元件 Top 12、品牌範例 Top 5、120 條反模式護欄的啟用狀態,以及理據。
- **下接:** `/ux-design [簡報]` → 用推薦 token 生成前端程式碼;`/ux-system` → 由推薦生成完整設計系統;`/ux-component <名稱>` → 用推薦風格生成單個元件;`/ux-lint` → 驗證生成的程式碼。

### 生成

#### `/ux-design` — 由簡報生成漂亮、反 slop 的介面

- **做什麼:** 由 discovery 簡報 + 推薦生成完整的生產級前端產出物(著陸頁、行銷站、應用外殼)。在反 slop 與 arsenal 參考的創意指引下,派遣 `frontend-engineer`。
- **何時使用:** 「設計一個」、「給我做一個」、「生成一個著陸頁」、「做一個儀表板」、「做一個元件」——任何形式自由的視覺交付請求。
- **何時跳過:** 你要的是評審而不是建造(用 `/ux-audit` 或 `/ux-critique`);你只想要一個元件(用 `/ux-component`);後端或基礎建設工作。
- **呼叫方式:** `/ux-design 生成一個面向 MENA 新銀行的金融科技著陸頁,暖色 editorial 語氣,暗色 AA,不要紫色漸層`。
- **輸出:** 生成的程式碼(HTML / Blade / JSX / Vue / Astro),以及 `.ux/last-design.json`。
- **下接:** `/ux-lint` → 驗護欄;`/ux-polish` → 拋光;`/ux-a11y` → 無障礙稽核;`/ux-copy` → 微文案稽核;`/ux-fix` → 以原子提交落地。

#### `/ux-component` — 生成單個元件

- **做什麼:** 由一份規格生成單個生產級元件(按鈕、模態框、導覽列、側邊欄、卡片、表格、表單、圖表)。四種互動狀態齊備,可無障礙存取,貼合品牌。先在 `.ux/last-recommendation.json` 裡查該元件,再回落到直接查清單。
- **何時使用:** 任何單元素請求——「做一個按鈕」、「做一張定價卡」、「做一個模態框」、「加一個導覽列」、「設計一個側邊欄」、「我需要一張資料表」、「做一個表單」、「做一個圖表元件」。
- **何時跳過:** 整頁或多段式介面(用 `/ux-design`);後端或基礎建設。
- **呼叫方式:** `/ux-component pricing-card-trio --brief="金融科技,暗色,等寬數字"`。
- **輸出:** 生成的元件程式碼,以及 `.ux/last-component.json`。
- **下接:** `/ux-lint` → 驗證;`/ux-polish` → 拋光。

#### `/ux-system` — 生成一套完整的起步設計系統

- **做什麼:** 為還沒有設計系統的專案提議一整套起步系統——tokens(顏色、字體、間距、動效、圓角、陰影)、基礎文件、元件契約、暗色模式對應、主題切換器。派遣 `design-system-architect`。
- **何時使用:** 「我們沒有設計系統」、「給我們搭一套」、「提議一份 tokens」、「我們的主題該長什麼樣」、「把 DS 搭起來」。
- **何時跳過:** 專案已經有設計系統——直接用 `/ux-component` 基於現有系統建造即可;後端或基礎建設。
- **呼叫方式:** `/ux-system`(如果還沒存檔,先跑 discovery)。
- **輸出:** `tokens.json`、`foundations.md`、`components/*.md` 契約,可選輸出 Tailwind / vanilla / SCSS。寫入 `.ux/last-system.json` 以供後續銜接。
- **下接:** `/ux-component` → 基於新系統建造;`/ux-design` → 用新 tokens 生成介面。

#### `/ux-dashboard` — 專門的儀表板生成

- **做什麼:** 以資料密度紀律建構的儀表板——bento 配置、等寬表格數字、迷你折線模式、避免濫用卡片、語意化狀態色、動效節制。它不是把圖表貼上去的行銷著陸頁。
- **何時使用:** 「做一個儀表板」、「設計 admin 面板」、「做一個指標頁」、「操作員主控台」、「分析檢視」、「KPI 板」、「監控頁」。
- **何時跳過:** 帶統計數字的行銷著陸頁(用 `/ux-design`);只要一個 widget(用 `/ux-component`);後端或基礎建設。
- **呼叫方式:** `/ux-dashboard`。
- **輸出:** 生成的儀表板程式碼 + `.ux/last-dashboard.json`。
- **下接:** `/ux-lint`、`/ux-audit`、`/ux-a11y`。

#### `/ux-motion` — 動效處理

- **做什麼:** 生成介面的動效層——時長、緩動、編排、reduced-motion 後援、效能紀律。也對現有動效按五個維度做稽核(時長、緩動、含義、reduced-motion、效能)。
- **何時使用:** 「檢查一下動效」、「動畫做得對不對」、「修一下動效」、「複核動畫」、「動效稽核」、「對動效做效能掃」。
- **何時跳過:** 介面沒有動效(用 `/ux-audit` 或 `/ux-polish`);後端或基礎建設。
- **呼叫方式:** `/ux-motion path/to/component.tsx`(稽核模式)或 `/ux-motion --generate hero-entry`(生成模式)。
- **輸出:** 更新後的程式碼(生成模式)或 `.ux/last-motion.json` 報告(稽核模式)。
- **下接:** `/ux-fix` → 落地動效結論;`/ux-polish` → 拋光。

### 稽核與驗證

#### `/ux-lint` — 基於 regex 的確定性檢查器(無 LLM,CI 安全)

- **做什麼:** 對你的程式碼跑 120 條 regex 規則。無 LLM 呼叫。CI 中遇 Critical / High 結束非零碼。原始檔:`data/anti-patterns.json`。規則覆蓋 A11y(23)、內容(15)、配置(13)、字體(10)、顏色(9)、品質(9)、視覺(9)、動效(8)、效能(4)。
- **何時使用:** 預提交鉤子;CI 關卡;在花 `/ux-audit` 成本之前對大程式碼庫做的快速首輪;在 `/ux-design` 或 `/ux-component` 之後用於驗證生成。
- **何時跳過:** 你想要修復循環(檢查器只報告、不修改——請接 `/ux-polish --fix` 或 `/ux-fix`);你想要品味判斷(用 `/ux-critique`)。
- **呼叫方式(slash):** `/ux-lint src/`。
- **呼叫方式(CLI):** `uxskill lint .` 或 `python3 bin/ux-lint.py .` 或 `bash bin/ux-lint.sh --ci --fail-on high`。
- **呼叫方式(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **輸出:** 標準輸出中的命中(位置、規則 id、嚴重等級、證據)。無命中時結束碼 0,設了 `--fail-on high` 且命中 Critical/High 時結束非零。
- **下接:** `/ux-polish --fix` → 同類模式的 LLM 版對手;`/ux-fix` → 按嚴重等級落地為提交;`/ux-audit` → 完整的六鏡頭推理回合;`/ux-next` → 讓指揮來決定。

#### `/ux-audit` — 六鏡頭設計稽核

- **做什麼:** 一次結構化、帶立場的評審,從六個鏡頭(清晰度、層級、無障礙、聲音、動效、品味)出發,產出按嚴重等級打標的發現。Polaris 風格的報告。先讀 `.ux/last-frame.json`——受眾與結果決定每條發現的嚴重等級。
- **何時使用:** 介面已存在,你需要一份能站得住腳的批評。「稽核一下」、「看看這版 UX」、「做得好不好」、「哪裡壞了」、「狠狠拆一下」。
- **何時跳過:** 介面尚未存在(用 `/ux-design`);使用者只要一個鏡頭(用對應專項命令:`/ux-a11y`、`/ux-copy`、`/ux-motion`、`/ux-polish`);使用者想要品味觀點(用 `/ux-critique`);後端或基礎建設。
- **呼叫方式:** `/ux-audit https://example.com/pricing` 或 `/ux-audit src/components/Pricing.tsx`。
- **輸出:** 寫入 `.ux/last-audit.json` —— `findings` 陣列,欄位為 `{lens, severity, title, principle, evidence, fix}`,以及 `severity_counts`、`dominant_lens`、`strategic_moves`。
- **下接:** `/ux-fix` → 落地;`/ux-polish` → 拋光;`/ux-design` → 若需結構性重設計。

#### `/ux-a11y` — WCAG 2.1 AA 稽核 + 基本禮貌檢查

- **做什麼:** 一次結構化的 WCAG 2.1 AA 稽核,外加那些自動工具能放行、但仍會傷害真實使用者的「基本禮貌」檢查(可見焦點、錯誤具體性、動效偏好、鍵盤陷阱、顏色依賴)。
- **何時使用:** 發布前無障礙關卡;重新設計之後;「做一下無障礙檢查」、「WCAG 稽核」、「這個無障礙嗎」、「a11y 複核」、「讀屏測試」、「鍵盤導覽檢查」。
- **何時跳過:** 不面向使用者;後端或基礎建設;還在草圖階段的工作。
- **呼叫方式:** `/ux-a11y https://example.com`(優先用線上 URL——自動工具和鍵盤測試只能在線上跑)。
- **輸出:** 寫入 `.ux/last-a11y.json` —— `findings` 陣列,欄位為 `{wcag_sc, sc_name, severity, title, evidence, fix, category}`、`beyond_wcag` 陣列、`severity_counts`。
- **下接:** `/ux-fix` → 落地為提交;`/ux-copy` → 在一次文案回合中順手修 alt 文字和表單錯誤串接。

#### `/ux-critique` — 品味評點(3 個亮點、3 個失分、1 步關鍵招)

- **做什麼:** 一個設計師的態度——不是結構化稽核,不是嚴重等級打分,只是一段緊緻、有立場的看法,點名什麼在起作用、什麼沒起作用,以及那一步能改變最多的關鍵招。
- **何時使用:** 「你怎麼看」、「這個好嗎」、「評點一下」、「實話說」、「語氣對不對」、「這像我們嗎」、「該不該發」。
- **何時跳過:** 使用者明確要的是結構化稽核(用 `/ux-audit`);後端或基礎建設。
- **呼叫方式:** `/ux-critique https://example.com`。
- **輸出:** 寫入 `.ux/last-critique.json` —— 3 個亮點、3 個失分、1 步關鍵招,外加散文。
- **下接:** 如果評點建議重設計就接 `/ux-design`;如果建議收緊就接 `/ux-polish`。

#### `/ux-copy` — 微文案稽核 + 重寫

- **做什麼:** 用聲音量規評估每一句可見文案,產出 before/after 重寫。專抓:「表單存在錯誤」(籠統)、「John Doe」(佔位符)、AI 式歡欣鼓舞的慶祝話術、籠統的 CTA、空蕩蕩的空狀態、毫無用處的錯誤提示。
- **何時使用:** 結構對了但文案弱。「複核文案」、「修微文案」、「錯誤提示糟糕」、「重寫這個」、「收緊文案」、「按鈕太籠統」、「空狀態死氣沉沉」。
- **何時跳過:** 配置問題(用 `/ux-audit` 或 `/ux-polish`);無障礙驅動的文案問題如 alt 文字(用 `/ux-a11y`);後端或基礎建設。
- **呼叫方式:** `/ux-copy src/views/checkout.blade.php`。
- **輸出:** 寫入 `.ux/last-copy.json` —— `strings` 陣列,欄位為 `{location, severity, before, after, notes}`,以及量規與需翻譯的語言。
- **下接:** `/ux-fix` → 落地重寫;`/ux-a11y` → 在文案改動後再複核。

### 修復與拋光

#### `/ux-fix` — 以原子提交落地稽核結果

- **做什麼:** 從 `.ux/` 讀取最近的報告(audit、copy、a11y、motion 或 polish),校驗工作樹,經由對應子代理把發現以原子提交的形式落地。落地後會重跑觸發命令再核驗。
- **何時使用:** 跑完一個稽核類命令並回顧了發現之後。「修一下這些發現」、「把修復落地」、「跑修復循環」、「打修補程式」、「按建議改」、「去修」。
- **何時跳過:** `.ux/` 裡沒有先前的報告;工作樹是髒的且使用者尚未同意 stash/commit;修復需要設計判斷而不是機械落地(請改用 `/ux-design` 重設計)。
- **呼叫方式:** `/ux-fix`(自動識別要修哪份報告)或 `/ux-fix --from=last-a11y.json`。
- **輸出:** 每條發現一個原子提交。重跑觸發命令並更新 `.ux/last-*.json`。印出一段摘要。
- **下接:** `/ux-next` → 由指揮挑下一步。

#### `/ux-polish` — 拋光 + 清除 AI-slop

- **做什麼:** 間距節奏、層級銳化、AI-slop 探測、token 一致性。`/ux-lint` 的 LLM 版對手——品味判斷由它代你執行。
- **何時使用:** 結構對了但執行鬆了。「拋個光」、「收緊」、「把 AI-slop 清掉」、「做得高級一點」、「讓它不那麼像 AI」、「間距感覺不對」、「看上去太通用」、「缺點品味」。
- **何時跳過:** 介面缺核心功能(先修那個);需要重設計而不是拋光(用 `/ux-design`);文案問題(用 `/ux-copy`);動效問題(用 `/ux-motion`);a11y 問題(用 `/ux-a11y`)。
- **呼叫方式:** `/ux-polish src/components/Hero.tsx`。
- **輸出:** 更新後的程式碼 + `.ux/last-polish.json` 描述改動。
- **下接:** `/ux-lint` → 驗證拋光穩了;`/ux-a11y` → 再做一次無障礙複核。

### discovery 與敘事

#### `/ux-frame` — 4 欄位定調區塊

- **做什麼:** 把「為誰、目標、假設、成功訊號」打進一個結構化的定調區塊。不做設計——只是把一個含糊請求轉成可工作簡報的四欄位收件。比 `/ux-discover` 更輕(4 欄位 vs 10 欄位)。
- **何時使用:** 任何專案、衝刺或一次性任務的開端;對話偏離主題時的中途收束。「框一下」、「簡報是什麼」、「立項」、「定調」。
- **何時跳過:** 已經框過(檢查 `.ux/last-frame.json`);沒有定調影響的一次性元件建造;後端或基礎建設。
- **呼叫方式:** `/ux-frame "為 Bashiti MENA 試點做的會員錢包"`。
- **輸出:** 寫入 `.ux/last-frame.json` —— `{audience, outcome, hypothesis, success_signal}`。
- **下接:** `/ux-discover` → 把框擴成 10 欄位簡報;`/ux-design` → 用框作錨點生成。

#### `/ux-research` — 研究計畫 + 綜合

- **做什麼:** 計畫模式:寫訪談腳本、問卷、招募篩選器。綜合模式(`--synthesize`):把訪談、分析、競品站點、A/B 結果、客服工單消化為建議。派遣 `research-synthesizer`。
- **何時使用:** 「計畫一次研究」、「我需要訪談題」、「設計一份問卷」、「如何招募使用者」、「使用者測試計畫」、「日記研究」、「偏好測試」、「fake door」、「smoke test」、「把我的訪談筆記綜合一下」。
- **何時跳過:** 答案已有高信心度;低風險且可逆的決策;後端或基礎建設。
- **呼叫方式:** `/ux-research --plan "MENA 會員錢包採用率"` 或 `/ux-research --synthesize interviews/*.md`。
- **輸出:** 寫入 `.ux/last-research.json` —— 研究計畫,或綜合後的主題 + 證據 + 建議。
- **下接:** `/ux-frame` → 把結論納入定調;`/ux-design` → 據結論生成;`/ux-workshop` → 以研究為輸入開工作坊。

#### `/ux-workshop` — 五階段設計思考工作坊

- **做什麼:** 端到端主持一場 discovery / 設計思考工作坊。五個順序階段(探索 → 熱度圖 → 利害關係人地圖 → 解決方案草圖 → 行動方案)。計時;每階段都有具體產出物。結束於一個決定,而不是「有趣的發現」。
- **何時使用:** 真問題、真參與者、真時間預算。「開一場工作坊」、「主持一次 discovery」、「來一次設計思考」、「我有利害關係人一小時,該幹啥」、「專案啟動」。
- **何時跳過:** 簡報已經清晰且收斂;單人腦力激盪(用 `/ux-design` 或 `/ux-frame`);團隊正在執行中,不在 discovery。
- **呼叫方式:** `/ux-workshop "會員錢包轉向" --participants="2 名 PM、1 名設計師、1 名工程 lead、1 名客戶代表" --minutes=90`。
- **輸出:** 寫入 `.ux/last-workshop.json` —— 行動方案 + 各階段產出物。
- **下接:** `/ux-design` → 執行行動方案;`/ux-research` → 補工作坊暴露的缺口;`/ux-case-study` → 把過程發表。

#### `/ux-case-study` — 可發布的案例研究(Wfrah 編輯格式)

- **做什麼:** 以純黑白編輯格式生成專案案例研究——Wfrah 字型、髮絲分隔線、帶序號的 (A)–(G) 段落碼、雙語相容配置。是一份文件,不是行銷小冊子。從 `.ux/last-frame.json`、`.ux/last-workshop.json`、`.ux/last-research.json`、`.ux/last-design.json`、`.ux/last-a11y.json`、`.ux/last-polish.json`、`.ux/last-recommendation.json`、`.ux/last-discovery.json` 讀取。
- **何時使用:** 發布後;經歷一個明確里程碑後。「寫一份案例研究」、「把這個專案做成案例」、「做收尾文件」、「把這工作發出來」、「作品集篇」。
- **何時跳過:** 專案資料不足以填滿 (A)–(G);使用者想要的是行銷著陸頁而非案例研究(用 `/ux-design`)。
- **呼叫方式:** `/ux-case-study --format=html --slug=bashiti-loyalty`。
- **輸出:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`。
- **下接:** 終端命令——通常是專案的句點。

### 指揮

#### `/ux-next` — 工作流指揮(唯讀)

- **做什麼:** 讀取每個 `.ux/last-*.json`,指認下一步槓桿最大的命令。它是指揮,不是建造者。唯讀。
- **何時使用:** 在命令之間。「接下來該做什麼」、「下一步是什麼」、「替我決定」、「從這裡往哪走」。
- **何時跳過:** `.ux/` 裡沒有先前報告;你心裡已有具體的下一條命令。
- **呼叫方式:** `/ux-next`(無參數)或 `/ux-next --focus=a11y`。
- **輸出:** 標準輸出——建議的下一條命令 + 理由。
- **下接:** 它挑哪條就接哪條。

#### `/ux-expert` — 諮詢入口

- **做什麼:** 在使用者索取真人 UX 專家時,展示外掛作者的聯絡方式。簡短、直接、無行銷話術。
- **何時使用:** 「誰做的這個」、「我需要個 UX 專家」、「你做諮詢嗎」、「能雇個人幫我嗎」、「這外掛背後有人嗎」。
- **何時跳過:** 使用者問的是外掛功能,不是諮詢。
- **呼叫方式:** `/ux-expert`。
- **輸出:** 一張含 LinkedIn / 電子郵件 / 儲存庫的簡短聯絡卡。

### 命令串聯圖

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4 欄位定調區塊
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10 欄位收件(強制關卡)
                  └────────────┬─────────┘
                               │ 寫入 .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  五路平行 -> 合併系統
                  └────────────┬─────────┘
                               │ 寫入 .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ 寫入 .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ 寫入 .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  把發現落地為提交
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  可發布產出物
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  指揮——唯讀
                  │  /ux-expert          │  諮詢入口
                  └──────────────────────┘
```

---

## 5 個子代理

子代理是由命令派遣的角色化生成器。它們從不獨立執行——由 `/ux-design`、`/ux-component`、`/ux-system`、`/ux-fix`、`/ux-research` 等命令呼叫。每個代理都有清晰的職責邊界:它們**不**決定簡報,只針對簡報執行。

### `frontend-engineer`

- **職責:** 生產級前端程式碼(React、Next.js、Vue、Blade+Alpine、原生 HTML、Astro),並保持反 AI-slop 紀律。
- **派遣者:** `/ux-design`、`/ux-component`、`/ux-dashboard`、`/ux-fix`。
- **輸入:** 簡報 + 創意指引 + tokens(來自 `.ux/last-recommendation.json`)。
- **輸出:** 與通用 AI 輸出可區分的可執行程式碼。不出現紫色漸層、不置中 hero、不三張等大卡片、不用 Inter 當顯示字、不出現「John Doe」、不放 emoji、不留 300ms 的預設值。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `motion-engineer`

- **職責:** 生產前端程式碼中的動效——Framer Motion、GSAP、CSS 動畫。時長、緩動、編排、reduced-motion 後援、效能紀律。
- **派遣者:** `/ux-design`、`/ux-motion --fix`、`/ux-component`。
- **輸入:** 動效簡報 + tokens + 來自 `data/motion-presets.json` 的 57 個預設。
- **輸出:** 配得上自己位置的動效。永遠包裹在 `prefers-reduced-motion` 後援中。永遠拿 Core Web Vitals 測一遍。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `copy-writer`

- **職責:** 真正會發布的文案——錯誤訊息、空狀態、CTA、loading 狀態、成功訊息、toast、輔助文字、表單標籤、按鈕文字。
- **派遣者:** `/ux-copy --fix`、`/ux-design`、`/ux-frame`、`/ux-component`。
- **輸入:** 聲音檔案(命名或貼上) + 介面的文案。
- **輸出:** 在介面各個狀態間一致套用的生產級微文案,讓產品聽起來像一個產品,不像十個。禁忌:「表單存在錯誤」、「John Doe」、AI 式歡欣鼓舞的慶祝話術、籠統 CTA、空蕩蕩的空狀態。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `research-synthesizer`

- **職責:** 把研究輸入(訪談、分析、競品站點、A/B 結果、客服工單)消化為可執行的設計建議。
- **派遣者:** `/ux-research`、`/ux-workshop`、`/ux-frame`。
- **輸入:** 原始研究素材——訪談記錄、匯出檔案、競品 URL、客服群集。
- **輸出:** 主題、證據、建議。不替設計師設計答案——而是把可供設計的底料交給設計師。
- **工具:** `Read, Write, WebFetch, Bash, Glob, Grep`。

### `design-system-architect`

- **職責:** 完整的設計系統——tokens(顏色、字體、間距、動效、圓角、陰影)、基礎文件、元件契約、暗色模式對應、主題化層。
- **派遣者:** `/ux-system`,以及在不存在系統時被 `/ux-component` 呼叫。
- **輸入:** 品牌簡報 + `.ux/last-recommendation.json`(風格 + 配色 + 字體搭配 + 動效預設)。
- **輸出:** 一套連貫、立場鮮明、可上生產的系統,讓下游代理無需重新決定根基就能建造。tokens JSON、基礎 MD、元件契約、暗色對應。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### 子代理派遣協定

當一個命令派遣子代理時,它會傳入:

1. 簡報 / 推薦(從 `.ux/` 載入)。
2. 與之相關的清單切片(例如 `frontend-engineer` 拿到選定的風格 + 配色 + 元件;`motion-engineer` 拿到選定的動效預設)。
3. 120 條反模式護欄(始終啟用)。
4. 一個成功判據(產出物必須做到什麼)。

子代理回傳:

1. 產出物(程式碼、文件、系統)。
2. 一段理據(為什麼這樣選)。
3. 對照護欄的自檢(他們驗證了哪些規則)。

呼叫方命令隨後會自動跑 `/ux-lint`,通過之後才宣告完成。

---

## 11 份資料清單

資料層就是大腦。每個命令都從中讀取;引擎在其間合併;程式碼檢查器對其掃描。所有檔案都在 `data/` 下,項目用 `{_meta, entries}` 包裝以做 schema 版本管理。

### `styles.json` — 84 種設計風格

| 欄位 | 描述 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`、`name`、`category`、`philosophy`、`when_to_use`、`when_to_skip`、`tokens`、`references`、`compatible_palettes`、`compatible_type_pairs`、`compatible_motion`、`compatible_industries`、`taste_score` |
| `categories` | Minimalist / Swiss、Brutalist、Editorial、Glassmorphism、Neumorphism、Bento、Skeuomorphic、Industrial、Maximalist、AI-Futurist、MENA-modern、Vaporwave 等 |
| `sample entry` | `swiss-international` —— 「網格即法律。字體承擔重活。裝飾即失敗。」 |

由 `/ux-recommend`、`/ux-system`、`/ux-design` 使用。Schema:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `palettes.json` — 176 套配色

| 欄位 | 描述 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`、`name`、`mode`(明/暗)、`tone`、`colors`(canvas、surface、ink、body、muted、primary、primary_active、hairline、success、warning、danger、accent)、`wcag_contrast_audit`、`compatible_industries` |
| `tones` | warm、editorial、magazine、clinical、playful、brutalist、monochrome、jewel-tone、MENA-warm、dev-tools-dark 等 |
| `sample entry` | `claude-warm-editorial` —— 明色,warm/editorial/magazine,canvas #faf9f5,primary #cc785c |

由 `/ux-recommend`、`/ux-system` 使用。對比度按 AA / AAA 驗證。Schema:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `type-pairs.json` — 70 組字體搭配

| 欄位 | 描述 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`、`name`、`display`(family + weights + source + license + URL)、`body`、`mono`、`compatible_styles`、`taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` —— Cormorant Garamond × Inter × JetBrains Mono |

所有字族都帶授權 + 來源 URL。由 `/ux-recommend`、`/ux-system` 使用。

### `components.json` — 148 個元件

| 欄位 | 描述 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`、`name`、`category`、`purpose`、`anatomy`、`states`、`tokens_used`、`motion`、`accessibility`、`compatible_styles`、`compatible_industries`、`code_skeleton` |
| `categories` | Navigation、Forms、Data Display、Feedback、Overlays、Layout、Content、Marketing、E-commerce、Auth、Dashboard、Charts、Empty States、Loading States、Error States |
| `sample entry` | `mega-nav-product-grid` —— Mega Navigation、Product Grid —— 6 段解剖、4 個狀態 |

這是我們最深的護城河。其他 Claude UX 外掛沒有發布過結構化的元件清單。

### `industries.json` — 184 條產業規則

| 欄位 | 描述 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`、`name`、`category`、`characteristics`、`audience_signals`、`recommended_styles`、`recommended_palettes`、`recommended_type_pairs`、`recommended_motion`、`regulatory_notes`、`regional_notes` |
| `categories` | Financial Services、Healthcare、Education、E-commerce、SaaS B2B、SaaS B2C、Developer Tools、Media、Gaming、Travel、Real Estate、MENA-specific 等 |
| `sample entry` | `fintech-neobank` —— 高信任、監管揭露、餘額/交易為主 UI、日活的行動優先 |

由 `/ux-recommend` 用作首條平行檢索軸。

### `chart-types.json` — 35 種圖表

| 欄位 | 描述 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`category`、`when_to_use`、`when_to_skip`、`encoding`、`accessibility`、`data_shape`、`compatible_styles` |
| `categories` | Comparison、Time Series、Distribution、Composition、Relationship、Flow、Geographic |
| `sample entry` | `bar-vertical` —— 比較 4–15 個離散類別。x 軸位置對應類別;高度對應數值。 |

由 `/ux-dashboard`、`/ux-component`(圖表實例)使用。

### `tech-stacks.json` — 25 個技術堆疊

| 欄位 | 描述 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`、`name`、`category`、`tier`、`languages`、`ssr`、`rsc`、`compatible_styling`、`scaffold_command`、`compatible_motion`、`gotchas` |
| `tiers` | production、prerelease、experimental |
| `sample entry` | `nextjs-15-app-router` —— Next.js 15(App Router),TS/JS,SSR,RSC,相容 Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

其他技術堆疊包括 Astro、SvelteKit、Remix、Nuxt 3、Solid Start、Qwik、Blade+Alpine、Hotwire、Phoenix LiveView、Hydrogen 2025。

### `ux-guidelines.json` — 112 條具名 UX 法則

| 欄位 | 描述 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`、`name`、`category`、`source`、`principle`、`application`、`examples`、`caveats`、`related_laws` |
| `categories` | Decision Cost、Attention、Memory、Motor Control、Visual Perception、Social、Emotional、Form、Error Handling、Onboarding、Empty State 等 |
| `sample entry` | `hicks-law` —— 決策時間隨選項數量呈對數成長 |

由 `/ux-audit`(六鏡頭打分)與 `/ux-critique`(品味錨)使用。

### `motion-presets.json` — 57 個動效預設

| 欄位 | 描述 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`、`name`、`category`、`tokens`(duration_ms、easing、transform_from/to、opacity_from/to)、`stacks`(framer_motion、gsap、css)、`accessibility`(reduced-motion 後援)、`when_to_use` |
| `categories` | Entry、Exit、Hover、Focus、Tap、Loading、Empty、Success、Error、Scroll-linked |
| `sample entry` | `fade-up-12px` —— 360ms,`cubic-bezier(0.16, 1, 0.3, 1)`,translateY(12px) → 0,opacity 0 → 1 |

每個預設都有一個 reduced-motion 變體。Framer Motion、GSAP 和純 CSS 都提供開箱可用的程式碼。

### `anti-patterns.json` — 120 條 regex 規則

| 欄位 | 描述 |
|---|---|
| `entries` | 100 |
| `keys per entry` | `id`、`name`、`severity`(critical/high/medium/low)、`category`、`detection`(type、pattern、flags、scope)、`evidence_template`、`fix`、`references` |
| `categories` | A11y(23)、Content(15)、Layout(13)、Typography(10)、Color(9)、Quality(9)、Visual(9)、Motion(8)、Performance(4) |

完整規則清單見[120 條反 AI-slop 規則](#120-條反-ai-slop-規則程式碼檢查器)。

### `brands/*.json` — 131 份品牌規範

| 欄位 | 描述 |
|---|---|
| `entries` | 110(再加一份 `_index.json` 列出全部) |
| `keys per entry` | `id`、`name`、`category`、`voice`、`tokens`(color、type、motion)、`design_principles`、`signature_moves`、`anti-moves`、`references` |
| `categories` | Developer Tools(36)、Consumer / Lifestyle / Retail(19)、Fintech / Crypto(14)、Editorial / Media(13)、AI / ML Platform(12)、Productivity / Collaboration(8)、Automotive(8) |

完整名單見[131 份 DESIGN.md 品牌規範](#131-份-designmd-品牌規範按類別)。

---

## 120 條反 AI-slop 規則——程式碼檢查器

ux-skill 提供一個基於 regex 的確定性檢查器。**無 LLM。** **無 API。** **無網路。** 在典型 Next.js 應用上 CI 中 ~200ms 跑完。設定 `--fail-on high` 時,遇 Critical / High 結束非零碼。

規則來自 `data/anti-patterns.json`(優先 v2),回退來源為 `references/foundations/anti-patterns.md`(v1 bash)。發布兩個執行檔:`bin/ux-lint.py`(Python,快、可擴充)與 `bin/ux-lint.sh`(Bash + perl-PCRE,用於無 Python 的環境)。

### 按類別的規則

#### 字體(3 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| high | `inter-as-display` | 把 Inter 當顯示字使用 |
| medium | `hero-text-arbitrary-90px` | hero 區任意大字號 |
| low | `font-system-only` | 只用系統字體堆疊,未選定字體 |

#### 顏色(6 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| high | `purple-to-blue-gradient` | AI 預設的紫到藍漸層 |
| high | `dark-text-on-dark-card` | 卡片上低對比度文字 |
| medium | `gradient-text-rainbow` | 多停的彩虹文字漸層 |
| medium | `card-glow-purple-shadow` | 卡片上的紫色 glow 陰影 |
| medium | `gradient-mesh-purple-pink` | hero 紫粉網格漸層 |
| low | `tailwind-color-named-vague` | 命名的 Tailwind 顏色沒有語意 token |

#### 配置(5 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| high | `three-equal-card-grid` | 三張等大並排卡片 |
| medium | `centered-everything-hero` | 一切置中的 hero |
| medium | `avatar-stack-overlapping` | 通用的相互重疊頭像堆 |
| low | `pill-rounded-full-everywhere` | `rounded-full` 用在所有東西上 |
| low | `nav-equal-hamburger-desktop` | 桌面端用漢堡選單 |

#### 內容(5 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| high | `lorem-ipsum-leak` | 出貨程式碼裡有 Lorem ipsum |
| high | `emoji-in-ui` | 用 emoji 當 UI 元素 |
| high | `icon-emoji-stamp` | 用 emoji 當圖示章 |
| high | `testimonial-fake-five-stars` | 寫死的五星好評 |
| medium | `fake-name-john-doe` | 佔位人名 |

#### 動效(3 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | CTA 上跳動的箭頭 |
| low | `timing-300ms-default` | 轉場預設值 300ms |
| low | `cubic-bezier-material-only` | 到處都是 Material 預設緩動 |

#### A11y(6 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| high | `inline-svg-no-aria` | SVG 缺 aria-label 或 aria-hidden |
| high | `img-no-alt` | 圖片缺 alt 屬性 |
| high | `link-onclick-no-href` | 錨點有 onClick 但沒有 href |
| medium | `button-no-type` | 按鈕缺 type 屬性 |
| medium | `heading-skip-h1-h3` | 跳級標題 |
| medium | `infinite-scroll-no-pagination` | 無鍵盤後援的無限捲動 |

#### 品質(6 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| high | `console-log-leak` | 元件程式碼裡殘留 `console.log` |
| medium | `inline-style-attribute` | inline style 屬性 |
| medium | `any-type-leak` | TypeScript `any` 型別 |
| medium | `arbitrary-z-index-9999` | 偷懶的 z-index 數值 |
| low | `shadcn-default-everywhere` | shadcn 預設 token 一字未改 |
| low | `todo-fixme-comment` | 出貨程式碼裡有 TODO 或 FIXME |

#### 視覺(1 條)

| 嚴重等級 | 規則 ID | 名稱 |
|---|---|---|
| low | `blur-bg-only-decoration` | 沒有玻璃表面的 backdrop blur |

### 檢查器用法

**一次性掃描:**

```bash
uxskill lint .
# 或
python3 bin/ux-lint.py src/
# 或
bash bin/ux-lint.sh src/
```

**CI 關卡(GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**預提交鉤子:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**輸出範例:**

```
─── /ux-lint report ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidence: bg-gradient-to-br from-purple-500 to-blue-500
  fix: replace with the recommended palette's primary gradient or remove gradient

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  evidence: grid grid-cols-3 gap-6 (3 equal Card children)
  fix: feature one card; flank with two reduced-emphasis cards

3 files scanned · 2 high · 0 medium · 0 low · exit 1
Recommended next: /ux-polish --fix (LLM-driven, addresses both lintable and aesthetic findings)
```

---

## 131 份 DESIGN.md 品牌規範——按類別

真實的品牌。真實的設計語言。真實的 DESIGN.md 規範——不是通用配色。告訴外掛「按 Stripe 的風格做個著陸頁」,它會讀取真實的品牌詞彙表:聲音量規、顏色 tokens、動效約定、招牌手法、反向手法。

每個品牌都以一份結構化 JSON(`data/brands/<slug>.json`)外加一份散文參考(`references/brands/<slug>.md`)的形式發布。

### Developer Tools(36)

ClickHouse、Composio、Cursor、Datadog、dbt Labs、Expo、Fivetran、Fly.io、Framer、HashiCorp、Honeycomb、IBM、Lovable、Mintlify、Modal、MongoDB、Neon、Ollama、OpenCode、PostHog、Railway、Raycast、Render、Replicate、Resend、Retool、Sanity、Sentry、Slack、Snowflake、Sourcegraph、Supabase、Superhuman、Vercel、Warp、Webflow

### Consumer / Lifestyle / Retail(19)

Aesop、Airbnb、Allbirds、Apple、Apple Music、Glossier、HP、Hims & Hers、Instagram、Meta、Nike、Patagonia、Pinterest、PlayStation、Shopify、Spotify、Starbucks、TikTok、Uber

### Fintech / Crypto(14)

Binance、Brex、Coinbase、Kraken、Mastercard、Mercury、Monzo、N26、Plaid、Ramp、Revolut、Robinhood、Stripe、Wise

### Editorial / Media(13)

Bloomberg、Clay、Dezeen、NVIDIA、Pitchfork、Substack、The Atlantic、The Economist、The New York Times、The Verge、The Wall Street Journal、Vodafone、Wired

### AI / ML Platform(12)

Anthropic、Claude、Cohere、ElevenLabs、MiniMax、Mistral AI、OpenAI、Perplexity、Runway、Together AI、VoltAgent、xAI

### Productivity / Collaboration(8)

Airtable、Cal.com、Figma、Intercom、Linear、Miro、Notion、Zapier

### Automotive(8)

BMW、BMW M、Bugatti、Ferrari、Lamborghini、Renault、SpaceX、Tesla

### 為什麼這件事很重要

另外 8 個熱門 Claude UX 外掛生成的是「現代極簡」或「乾淨儀表板」——同一種預設美學的變體。ux-skill 讓你能要**Linear 的清晰**、**Stripe 的嚴肅**、**Apple 的克制**、**Tesla 的整塊感**、**Notion 的親和**、**Cursor 的漸層紀律**、**Raycast 的髮絲密度**、**Claude 的暖色 editorial**——引擎會從品牌規範裡取出對應的 tokens、聲音、動效約定與招牌手法。

---

## MCP 伺服器——非對稱的一著

ux-skill 提供一個 **Model Context Protocol 伺服器**。執行 `ux-mcp`,引擎就變成一個常駐的 stdio 程序,任何支援 MCP 的主機——Claude Desktop、Cursor、Windsurf 以及通用代理——都可以呼叫它。共 14 個工具:`ux_recommend`、`ux_lint`、`ux_styles`、`ux_palettes`、`ux_type_pairs`、`ux_components`、`ux_industries`、`ux_motion_presets`、`ux_anti_patterns`、`ux_brands`、`ux_landing_patterns`、`ux_persist_save`、`ux_persist_load`、`ux_stats`。這些工具背後是斜線命令使用的同一套 Python 處理器、同一批資料清單、同一個確定性推薦器。

**為什麼這是非對稱的一著:** 排名前八的 Claude UX 技能(ui-ux-pro-max-skill、open-design、taste-skill、huashu-design、stitch、nothing-design、hallmark、material-3)沒有一個提供 MCP 伺服器。它們都被鎖在 Claude Code 的外掛執行階段裡。ux-skill 則能從任何講 MCP 的主機接入,包括從未聽說過 Claude Code 外掛的代理。

```bash
pip install 'uxskill[mcp]'             # mcp 是一個可選 extra
ux-mcp                                  # 啟動 stdio JSON-RPC 伺服器
```

把你的用戶端指向 `ux-mcp` 執行檔即可。完整工具文件、JSON 範例,以及面向 Claude Desktop、Cursor、Windsurf 的逐用戶端設定見 [docs/mcp.html](docs/mcp.html) 和 `commands/ux-mcp.md`。

---

## 面向 17 個 IDE 的安裝程式

`uxskill init`(或在 Claude Code 中執行 `/ux-init`)會自動識別你在哪個 IDE,並寫入對應的產出物。同一個 Python 引擎。同一套推薦。各 IDE 之間用不同的「膠水」對接。

| IDE / 工具 | 識別訊號 | 安裝的產出物 |
|---|---|---|
| Claude Code | `.claude/` 或 `CLAUDE.md` | 在 `.claude-plugin/plugin.json` 的外掛清單 + 全部 22 個命令 + 全部 5 個子代理 |
| Cursor | `.cursor/` 或 `.cursorrules` | 指向引擎的 `.cursorrules` 提示頭 |
| Windsurf | `.windsurf/` 或 `.windsurfrules` | 同樣提示頭的 `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` 或 `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` 修補 |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` 或 `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

在每個 IDE 裡,從終端機跑 `uxskill recommend` / `uxskill lint` / `uxskill stats` 都一樣可用。Python 引擎是事實來源;IDE 的產出物只是薄薄的提示頭,負責把請求路由到引擎。

---

## 使用案例——具體場景

八個真實場景。挑一個最貼近你處境的,改一下呼叫參數即可。

### 1. 在 Cursor 裡做一個金融科技儀表板

你在 Cursor 上做一個 MENA 新銀行的儀表板。裝好外掛、跑 discovery、跑 recommendation,然後生成儀表板。

```bash
pip install uxskill
uxskill init                                # 識別 Cursor,寫入 .cursorrules
uxskill discover                            # 10 欄位收件
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

然後在 Cursor 裡說:*「用 .ux/last-recommendation.json 裡的推薦生成儀表板介面」*。Cursor 讀 `.cursorrules` 頭,載入推薦,帶著明確約束派遣一次儀表板生成。

### 2. 在 Claude Code 裡生成一份 Stripe 風格的著陸頁

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> 專案類型? landing
> 產業? fintech-payments
> 語氣? 嚴肅、技術、自信
> 必備項? dark-mode、AA、行動優先
> 禁忌項? purple-gradients、three-equal-cards
> 參考品牌? stripe
> 技術堆疊? nextjs-15-app-router
> 地區? 全球
> 成功指標? 註冊轉換

/ux-recommend
> [回傳選定的風格、配色、字體搭配、動效預設、元件、品牌範例]

/ux-design "用 Stripe 品牌規範作為範例生成著陸頁"
> [frontend-engineer 生成頁面]

/ux-lint .
> [通過——Stripe 品牌規範得到尊重]
```

### 3. 在 CI 裡稽核既有程式碼以圍剿 AI slop

兩週前你發了一個 Next.js 應用。你想在每個 PR 上設一條硬底線,擋住 AI 指紋。

```yaml
# .github/workflows/ux-lint.yml
name: ux-lint
on: [pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install uxskill
      - run: uxskill lint . --ci --fail-on high
```

只要 PR 引入紫到藍漸層、96px 的 Inter、「John Doe」推薦語或拿 emoji 當圖示,CI 就會失敗。沒有 LLM 成本。~200ms。

### 4. 給一個「看起來像 AI 生成」的既有介面拋光

你接手了一個 React 應用,看上去和其他 AI 生成的 SaaS 站點沒差。你想讓它不要長那樣。

```
/ux-critique src/components/Hero.tsx
> [3 個亮點、3 個失分、1 步關鍵招——評點很坦誠]

/ux-lint src/
> [標記出 15 個高嚴重等級的 AI 指紋]

/ux-polish src/components/Hero.tsx
> [LLM 驅動的拋光 + 清除 AI-slop]

/ux-fix
> [把發現作為原子提交落地,並重跑檢查器]
```

三條命令,一張拋光後的介面,每個修復一個原子提交。

### 5. 設計一個 Linear 風格的命令面板

```
/ux-component command-palette --brief="Linear 風格,暗色,等寬快速鍵,最近項目優先"
> [讀取 data/brands/linear.app.json 取 tokens + 招牌手法]
> [讀取 data/components.json 取 command-palette 解剖結構與狀態]
> [帶著明確的 Linear 規範派遣 frontend-engineer]
```

生成的元件用的是 Linear 真實的顏色 tokens、字體堆疊、動效約定與髮絲密度——而不是「通用暗色 UI」。

### 6. 用 90 分鐘和利害關係人開一場設計思考工作坊

你有一間會議室,5 個人,90 分鐘。你希望他們帶著行動方案離開,而不是帶著「感覺」。

```
/ux-workshop "會員錢包轉向" \
  --participants="2 名 PM、1 名設計師、1 名工程 lead、1 名客戶代表" \
  --minutes=90
```

外掛端到端地主持五個階段(探索 → 熱度圖 → 利害關係人地圖 → 解決方案草圖 → 行動方案),計時,每階段都有具體產出。最終輸出是 `.ux/last-workshop.json` —— 行動方案,而不是只剩「有趣的發現」。

### 7. 發布後寫一份可發表的案例研究

你發了會員錢包。你想要一篇作品集篇章。

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [讀取 .ux/last-frame.json、last-workshop.json、last-research.json、last-design.json、last-a11y.json、last-polish.json、last-recommendation.json、last-discovery.json]
> [生成 Wfrah 編輯格式的案例研究,含 (A)-(G) 編號段落、髮絲分隔線、雙語相容配置]
> [寫入 case-studies/bashiti-loyalty.html]
```

這份案例研究是已完成、可發布的產出物——不是草稿。純黑白、editorial 字型、可直接上你的作品集。

### 8. 在非 AI 環境裡跑 discovery(只要結構化收件)

你在做一份專案規劃。你還不需要推薦——只需要一份結構化簡報。

```bash
uxskill discover
# 10 欄位收件,儲存到 .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

你可以把 JSON 交給團隊,貼到 Notion 文件裡,或者餵給其他 AI 工具。ux-skill 不只是引擎,也是一個結構化收件工具。

### 9. MASTER.md 持久化——把你的設計決策寫進儲存庫

跑完 `/ux-recommend` 之後,把選定的風格 + 配色 + 字體 + 動效 + 元件 + 品牌範例 + 護欄持久化為一份可讀的 Markdown 檔案,讓團隊能審查、對比(diff)、納入版本控制。

```bash
python3 -m engine.cli.main persist save --project-root .
```

寫出 `.ux/design-system/MASTER.md`(YAML frontmatter + 正文),並透過 `persist save-page` 為每個生成出的介面寫出 `.ux/design-system/pages/<name>.md`。冪等——相同輸入產出按位元組完全一致的輸出,所以在狀態未變時重跑在 git 裡就是個 no-op。

---

## 與其他方案的對照

簡表如下。逐欄對照詳見 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

| 維度 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| 斜線命令 | **22** | 1 | 19 | 1 | 1 | 多 | 1 | 1 | 1 |
| 元件 | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| 動效預設 | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 品牌規範 | **110** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 反模式規則 | **100** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 安全的確定性檢查器 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 支援的 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery 關卡 | **10 欄位** | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 |
| `.ux/` 狀態鏈 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| Star 數(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 坦誠評估

- **ui-ux-pro-max** 認知度更大,支援 18 個 IDE,在它的 CSV 上做了類 BM25 的檢索。它沒有元件清單、動效清單、品牌庫或確定性檢查器。
- **open-design** 擁有 19 個 skill + 預覽,但只支援 Claude Code,而且沒有反 slop 層。
- **hallmark** 在精神氣質上最接近(也是反 slop),但它是單個 skill ——沒有引擎、沒有清單、沒有可串聯的命令。
- **material-3-skill** 在你專門要 Material Design 3 時極佳。我們不在 MD3 上跟它較勁。

按維度的完整細節見 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 路線圖

### v2.1 — 檢查器補全(2026 Q3)

- **+17 條延後的反模式規則**,合計 52 條。目標包括:dark-on-dark 的 hover 狀態、只用顏色編碼狀態、冗餘 z-index 升級、JS 裡寫死斷點、用 opacity 代替 disabled 狀態等。
- **`uxskill lint --fix`** 支援對機械可修復的命中進行安全重寫(`button-no-type`、`img-no-alt` 空串、移除 `console-log-leak`)。
- **VS Code 擴充功能**,在編輯器內聯呈現檢查器命中(無需先跑 CI)。

### v2.2 — 元件清單擴充(2026 Q4)

- **+50 個元件**,合計 198 個。新增:帶非同步過濾的 combobox、帶最近項啟發式的 command-palette、條件化表單步驟、payment-element 變體、RTL 感知的日期選擇器、MENA 專用電話輸入、帶 hijri 疊層的日曆網格。
- **按元件輸出 6 個技術堆疊的程式碼**(Next.js + React、Vue 3 + Nuxt、SvelteKit、Astro、Blade + Alpine、原生 HTML/CSS)。
- **元件 Playground**:在 uxskill.laithjunaidy.com/playground 試跑推薦引擎並即時預覽元件。

### v3 — 市集 + 鎖定(2027)

- **品牌規範市集** —— 發布與發現社群貢獻的品牌規範。付費發布以資助審核。
- **自訂反模式規則** —— 專案可在 `data/anti-patterns.local.json` 裡定義自己的 regex 規則(v2 已發布;v3 新增發現 + 共享)。
- **`uxskill plan`** —— 從一份簡報出發的完整多頁站點規劃,而不只是單個介面。
- **Figma 外掛等同實作** —— 同一個推薦引擎,搬到 Figma 裡。

---

## 參與貢獻

歡迎 issue 與 PR。三個高槓桿方向:

### 新增一條反模式規則

1. 編輯 `data/anti-patterns.json` —— 加入一條帶 `id`、`name`、`severity`、`category`、`detection.pattern`、`detection.flags`、`detection.scope`、`evidence_template`、`fix`、`references` 的項目。
2. 在 `tests/linter/` 裡加測試 —— 一份會觸發規則的檔案,一份不會的。
3. 跑 `uxskill lint tests/linter/should-trigger/<rule>.tsx` —— 確認會被命中。再跑 `tests/linter/should-not-trigger/<rule>.tsx` —— 確認不會被命中。
4. 開一個 PR。

### 新增一份品牌規範

1. 建立 `data/brands/<slug>.json`,欄位包含 `id`、`name`、`category`、`voice`、`tokens`、`design_principles`、`signature_moves`、`anti-moves`、`references`。
2. 在 `references/brands/<slug>.md` 加入對應散文。
3. 在 `data/brands/_index.json` 登錄。
4. 開一個 PR。規範必須有第一手出處(品牌實際的產品、公開的設計系統,或他們公開發布的 DESIGN.md)。

### 新增一個動效預設

1. 編輯 `data/motion-presets.json` —— 加入一條帶 `id`、`name`、`category`、`tokens`、`stacks`(framer_motion、gsap、css)、`accessibility.reduced_motion_fallback`、`when_to_use` 的項目。
2. 該預設必須有 reduced-motion 變體。無一例外。
3. 開一個 PR。

### 流程

- 閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解完整流程。
- 閱讀 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
- 新規則與品牌規範會按以下標準複核:第一手出處、不過度擬合到單個專案、資料中不出現 emoji、在適用時的 RTL 安全行為。

---

## 授權、作者、致謝

### 授權

MIT。用它、fork 它、在它之上建構。如果它幫你少出貨了一份 AI slop,請給儲存庫點個 star——這是成本最低的支持方式。

### 作者

**Laith Aljunaidy** —— [Dot](https://thedotwallet.com) 的獨立創辦人,Dot 是一個 MENA 優先的會員平台。我打造 ux-skill,是為了讓 AI 生成的前端不再千篇一律。

- LinkedIn:[linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- 電子郵件:laith.aljunaidy.laith@gmail.com
- 儲存庫:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- 官網:[uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI:[pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm:[npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 致謝

- 感謝 Anthropic 團隊提供了 Claude Code,以及讓這一切可分發的 skill / 外掛架構。
- 感謝 Nielsen Norman Group、Laws of UX(lawsofux.com)以及讓 `data/ux-guidelines.json` 言之有據的 UX 研究社群。
- 感謝 `data/brands/` 裡列出的每一個品牌——它們公開的設計系統是品牌規範的事實來源。
- 感謝原始的 v1 貢獻者:那份一次成型的 Claude skill 是 v2 Python 引擎的種子。
- 感謝我們對照的那 8 個熱門 Claude UX 外掛——他們抬高了基準;這是我們的回答。

---

**ux-skill** · **v2.0.0-alpha.1** · 為讓 Claude Code、Cursor、Windsurf 以及其他 AI 程式設計工具產出的前端不再被一眼識別為 AI 生成而打造。

> 給儲存庫點個 star:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · 透過 `pip install uxskill` 或 `npx uxskill init` 安裝 · 在 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) 瀏覽對照
