[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · **繁體中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill：為 Claude Code、Cursor 及一切 AI 程式設計工具打造的設計智慧引擎

**一個設計智慧引擎，讓 AI 生成的 UI 有辨識度，而不是千篇一律。** 接入 17 款 AI 程式設計工具中的任何一款，產出就不再一看就是 AI 做的。免費、MIT、離線、無 LLM。

```bash
pip install uxskill
```

**[在 GitHub 上給 ux-skill 一顆星](https://github.com/Laith0003/ux-skill)**：如果它對你有用，這是支持專案最省事的方式。第一次來？從 [60 秒導覽](#快速安裝)開始，或到 [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) 看實際效果。

![之前：千篇一律的圖庫照片 hero，柔和的紫色漸層，毫無品牌辨識度。之後：深色遮罩下的真實工地照片，帶琥珀色強調的編輯風標題，以及嵌在 hero 裡的報價申請表單。同樣的提示詞，由 ux-skill 提供約束時結果就不同。](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*之前：千篇一律的圖庫照片 SEO 垃圾內容。之後：深色遮罩下的真實工地照片 hero，帶琥珀色強調的編輯風標題，hero 內的報價表單。同樣的 AI 程式設計工具、同樣的提示詞，由 ux-skill 提供約束時結果就不同。*

> **v4.0，FOUNDATIONS：一道命令就能建立一套完整、經過 WCAG 檢查的設計系統，內建阿拉伯文與由右至左排版。** 面向 AI 程式設計的最強 UX 外掛。一個 Python 推理核心，搭配確定性的 7 軸合成器，12 份可查詢的 JSON 清單（84 種風格、176 套配色、70 組字體搭配、148 個元件、184 個產業、35 種圖表、57 個動效預設、112 條 UX 定律、171 條反模式規則、25 個技術堆疊、160 份品牌規範），18 個斜線命令、5 個子代理、25 個 MCP 工具，以及一個確定性的反 AI slop 檢查器。跨 IDE：可裝入 Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、Kiro、Cline、Continue、Aider、Zed、JetBrains AI、Pieces、Tabby、Tabnine、CodeWhisperer 與 Roo Cline。

> **品牌名稱是 `ux-skill`。** PyPI / npm 套件名稱仍為 `uxskill`。GitHub 儲存庫位於 [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)。

**作者：** [Laith Aljunaidy](https://laithjunaidy.com)，常駐安曼的設計師兼 CTO · **網站：** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **與所有 Claude UX 外掛比較：** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub：** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI：** [uxskill](https://pypi.org/project/uxskill/) · **npm：** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#面向-17-個-ide-的安裝程式)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### 4.0 新功能：設計基礎

輸入一個品牌色，輸出一套設計系統，對比在交到你手上之前就已檢查過。

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

需要 Python 3.10 或更新版本。MCP 伺服器請用 `pip install --upgrade 'uxskill[mcp]'`。用 pipx 則是 `pipx install uxskill`（在已安裝的 3.x 上升級用 `pipx upgrade uxskill`）。用 npm 則是 `npx uxskill@latest`。從 3.x 遷移？[遷移指南](docs/migrating-to-4.md)把每個 3.x token 對應到它在 4.0 中的角色。

**在做產品或著陸頁？** 你會拿到：供頁面引用的 `tokens.css`，為所選字體配好度量相符之備用字體的 `fonts.css`，從你自己的檔案載入字體的 `fonts-self-host.css`，供工具使用的 `tokens.json`，放在 `art/` 裡的裝飾性品牌圖像，以及 `system-report.md`，用平實的話說明建立了什麼、為什麼這樣做、應該從哪種頁面構圖開始。用角色撰寫樣式（`var(--color-action-primary)`、`var(--color-text-default)`、`var(--color-surface-page)`），在 `<html>` 上用一個屬性就能切換深色模式、高對比、緊湊間距、由右至左或減少動態效果。字體可以用報告提供的 Google Fonts 連結載入，也可以用 `fonts-self-host.css` 加上一個 `fonts/` 資料夾載入；無論哪種方式，都要在 `tokens.css` 之前引用 `fonts.css`；這兩個檔案都不要修改。加上 `--brief` 時，若簡報寫明了產業與語氣，外觀就隨之調整；結構化欄位（年齡、語言、預設配色方案、閱讀情境）決定文字大小、點按區域、文字系統以及預設開啟哪種配色方案；discovery 不會詢問產業，所以由 `/ux-system create` 來問。在 Claude Code 中，`/ux-system create` 會檢查已安裝的版本、執行建置並解讀報告。

**在設計設計系統？** 九大基礎（顏色、字體、間距、版面、圓角、邊框、層次、動效、影像），每一項都隨七個軸連續變化，包含原始值與語意角色，採用 W3C 設計權杖格式（DTCG 2025.10）並列出每種模式的數值。輸入相同，位元組相同。透過 MCP，`ux_system_build` 會回傳報告、檢查結果與每個檔案的大小，傳入 `out` 時會寫出與命令相同的檔案。

- **WCAG 檢查。** 每一組文字、控制項與焦點的顏色搭配，都會在淺色與深色、標準對比與高對比下量測：標準對比下依 WCAG 1.4.3（文字 4.5:1）與 1.4.11（非文字 3:1），高對比下依 WCAG 1.4.6（文字 7:1）；此外，由於 WCAG 並未規定非文字的強化等級，我們為大多數非文字元件另訂了高對比下 4.5:1 的下限，這是我們自己的標準。未通過的系統不會寫出，訊息會說明該改什麼。
- **預設安全。** 絕不覆寫內容不同的檔案。只有你要求時，`--force` 才會取代檔案。
- **阿拉伯文。** 在 `dir="rtl"` 下，文字會切換到一款阿拉伯字體，使用它自己的字級與行高；間距採用邏輯屬性，動效左右鏡像。`--latin-only` 可以拿掉這部分。

**你已經有一套系統？** `/ux-system enhance --from` 依它原本的命名讀取（DTCG token、CSS 自訂屬性、Tailwind 主題、markdown 規則檔或 Figma 變數匯出），用同一套檢查把關，並量測你的程式碼實際上如何使用它；不會改寫任何東西。`/ux-system extend --from` 在旁邊的一個擴充檔裡補上基礎、角色或契約，不更動任何既有的 token；`uxskill system export` 則把它寫成 tokens.css、Tailwind 4 主題或 Figma 變數。4.2 會加入信任層（每次寫入都跑 lint，加上一位收尾審查者）並正式發布。詳見 [changelog](CHANGELOG.md)。

**元件與區塊。** 23 份元件契約規定控制項的每個部分在每種狀態下綁定哪些 token，以及每種狀態如何運動：狀態變化依 `motion.state` 轉場，按下時依 `motion.press.scale` 縮放（在減少動態效果時保持靜止），分頁、選單與分段控制項則滑動同一個指示器。14 份區塊契約（hero、定價、FAQ、頁尾等）規定每個區塊的任務、各插槽可放的元件、需要的佐證，以及在手機上如何堆疊。用它們組成的頁面使用照片；介面片段只是額外的影像，絕不取代照片。

**會讀頁面的檢查器。** 171 條規則，其中許多會對剖析後的 CSS 與標記再做一次檢查，讀取頁面自身的系統：動效時間依它的曲線計算，標題大字的行高須守住引擎的下限，隱藏的控制項必須退出 Tab 順序。`uxskill lint --render` 會在無頭 Chromium 中以桌面寬度與手機寬度開啟每個頁面並實際操作：看不見或被裁切的焦點環、反應遲緩的懸停與按下、按 Escape 後遺失的焦點，以及在減少動態效果時仍在運動的按下效果。

**命令更少。** 25 個斜線命令精簡為 18 個。`/ux-discover` 支援 `--frame` 與 `--recommend`，`/ux-design` 支援 `--component`、`--dashboard` 與 `--from-image`，`/ux-polish` 循環執行 lint、修正、再 lint，直到分數達到 90 或跑滿三輪，`/ux-init` 支援 `--stats`。七個舊名稱仍可作為別名使用，將在 4.1 移除；見[別名](#別名將在-41-移除)。

**依介面分類的規則手冊。** 著陸頁、儀表板與元件的規則放在 `references/surfaces/`，各有一份手冊。`/ux-design` 依模式只載入其中一份，所以建置儀表板時永遠不會讀到 hero 的規則。

測試 **9764 項通過**。離線。確定性。從不呼叫 LLM。

### v3.1 新增：忠於品牌、響應式、有生命力

- **品牌忠實度是強制的，而不是寄望的。** 主色從 LOGO 的像素讀取（而不是從塗得最多的 CSS 讀取）；與 logo 字形風格不符的預設字體會被拒絕。擷取出的品牌沿 `recommend` -> `synthesize` 傳遞，`evaluate` 中的**硬性下限**會將任何遺失品牌色或 logo、或沒有真實影像的輸出判為失敗。與開放的 `brand.md` 慣例雙向互通（算繪 + 匯入）。
- **行動優先，有關卡把守。** 新的工藝基礎（`responsive.md`、`component-behaviors.md`），加上一個能感知換行的關卡：出現水平捲動、導覽、字標或按鈕文字換行，或固定頁首過高，都判為失敗。
- **驚豔層。** 引擎為每個頁面推導出 2-3 個彼此呼應的招牌時刻；「驚豔只能來自使用者」的說法就此被推翻。
- **更敏銳的檢查器**（152 條規則）：偵測必要影像與純圖示元素，新增佔位 token 與 `100vw` 規則；保留帶種子的 picsum，移除隨機的。

完整說明見 [CHANGELOG.md](CHANGELOG.md)。

### v3 新增內容

- **品牌規格成為訓練資料,而非範本。** 160 個品牌規格不再是推薦器從中挑選的目錄,而是合成器蒸餾的詞彙。每次呼叫都產生新輸出。
- **7 軸合成器**(warmth, contrast, density, geometry, formality, motion, type_personality)。Brief 確定性映射到軸值;軸值編譯為全新的 palette + 字體 + spacing + radius + motion token。
- **三種自動派發模式**：`strict_brand`(單一品牌 100%)、`brand_anchor`(單一品牌 70% + 同類品牌軸向適配 30%)、`pure_synthesis`(未指定品牌，從軸向匹配的 8 個範例中蒸餾)。
- **決策日誌重新排序推薦器。** `.ux/decisions.jsonl` 按同一 `(industry, ui_type)` 桶內的歷史勝出對候選重新排序。冷啟動安全。僅計算 `lint_score >= 80` 且 `user_accepted = true` 的決策。
- **軸交互矩陣**：顯式解決競爭軸之間的衝突(dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius)。不再有沉默的臨時規則。
- **`/ux-evolve` 自動循環**（在 4.0 中是 `/ux-polish` 的預設循環）：lint → polish → re-lint，直到分數 ≥ 90、進入停滯期，或在 4.0 中跑滿 3 輪（v3 中為 5 輪）。品質關卡在 65。
- **3 個新 MCP 工具**(15 → 18):`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`。
- **本地統計儀表板**：`uxskill stats --html` 寫出 `.ux/stats.html`,顯示**你的**安裝學到了什麼。無遙測,無全域彙整。
- **223 個測試通過。** 離線。確定性。從不呼叫 LLM。

完整細節見 [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain)。

### Star 歷史

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill 是什麼

ux-skill 是一個面向 AI 程式設計工具的**設計智慧引擎**。它以 Python 套件的形式運行(`pip install uxskill`),也作為 Claude Code 外掛運行,同時提供一個面向 17 個 IDE 的多重安裝程式。引擎接收一份專案簡報(產業、受眾、語氣、必備項、禁忌項、技術堆疊、地區),並回傳一套完整的推薦設計系統:風格、配色、字體搭配、動效預設、元件、可供研習的品牌範例,以及必須堅守的反模式護欄。該推薦是確定性的，相同輸入永遠產出相同結果。

這個外掛位於你與 AI 程式設計工具之間。當你讓 Claude Code、Cursor 或任何其他 AI 助理「做一個金融科技著陸頁」時，助理通常會即興發揮，結果在五秒鐘內就能被識別為 AI 生成（紫到藍的漸層、三張等大的卡片、用 Inter 做超大顯示字、評價裡出現「John Doe」、預設 300ms 的轉場、置中 hero、CTA 上跳動的箭頭）。ux-skill 用**結構化約束**取代即興發揮：你用 `/ux-discover` 記錄簡報並選定系統，用 `/ux-design` 生成程式碼，再用 `/ux-lint` 在提交前確認它通過 171 條確定性的反 AI slop 規則。

這份 README 是權威參考。每一個命令、每一個子代理、每一份資料清單、每一條安裝路徑、每一份品牌規範、每一類反模式，全都記錄在這裡。如果你正在挑選 Claude Code 的設計外掛,或者在為 Cursor、Windsurf 或 Codex 比較 AI 設計工具,請把這篇從頭到尾讀一遍,並對照 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 目錄

1. [大腦，v3.0 是什麼](#大腦v30-是什麼)
2. [快速安裝](#快速安裝)
3. [數據對照，與 Top 8 Claude UX 技能的即時比較](#數據對照與-top-8-claude-ux-技能的即時比較)
4. [架構，各部件如何咬合](#架構各部件如何咬合)
5. [18 個斜線命令，詳細參考](#18-個斜線命令詳細參考)
6. [5 個子代理](#5-個子代理)
7. [11 份資料清單](#11-份資料清單)
8. [171 條反 AI slop 規則，程式碼檢查器](#171-條反-ai-slop-規則程式碼檢查器)
9. [160 份 DESIGN.md 品牌規範，按類別](#160-份-designmd-品牌規範按類別)
10. [MCP 伺服器，非對稱的一著](#mcp-伺服器非對稱的一著)
11. [面向 17 個 IDE 的安裝程式](#面向-17-個-ide-的安裝程式)
12. [使用案例，具體場景](#使用案例具體場景)
13. [與其他方案的對照](#與其他方案的對照)
14. [路線圖](#路線圖)
15. [參與貢獻](#參與貢獻)
16. [授權、作者、致謝](#授權作者致謝)

---

## 大腦：v3.0 是什麼

v3.1.0 是 ux-skill 歷史上最大的架構轉變。推薦器不再從目錄中挑選範本，引擎為每份 brief **合成**新鮮的設計語言。相同的 brief 始終產生相同的輸出(完全確定性),但每份不同的 brief 都得到自己的新系統。品牌規格不再是範本;它們是引擎從中學習詞彙的訓練資料。系統能看到自身歷史,在本地閉合回饋迴路,從不呼叫 LLM。

編譯器是**確定性 7 軸合成器**，warmth, contrast, density, geometry, formality, motion, type_personality。每份 brief 映射到軸值;軸值編譯為全新的 palette + 字體 + spacing + radius + motion token。模組化字體比例從 contrast 中選取比率(1.200 quiet / 1.250 balanced / 1.333 loud)。版面配置原語由構造即響應式(`auto-fit minmax(min(N, 100%), 1fr)` + 容器查詢)。損壞的版面無法發出,因為它們不可表示。

三種自動派發模式:`strict_brand`(`reference_brands=[stripe] strict=True` → 100% Stripe token,最快路徑);`brand_anchor`(`reference_brands=[stripe]` → 70% Stripe + 來自 4 個同類品牌的軸向適配 30%);以及 `pure_synthesis`(未指定品牌 → 無限空間,從軸向匹配的 8 個範例蒸餾為新設計語言)。競爭軸由文件化的**軸交互矩陣**解決，dense + corporate 編譯為 4px(density 勝出,Bloomberg 流派),airy + corporate 為 12px(formality 勝出,奢華),soft + playful 為 18px radius,sharp + corporate 為 2px。實作中無沉默的臨時規則。

**決策日誌**（`.ux/decisions.jsonl`，schema `_v: 1` 已鎖定）閉合回饋迴路。推薦器現在依同一 `(industry, ui_type)` 桶內的歷史勝出對候選重新排序。冷啟動安全：先前的決策少於 3 筆時略過重排。僅計算 `lint_score >= 80` AND `user_accepted = true` 的決策。此外 `/ux-polish` 執行 lint → polish → re-lint，直到分數 ≥ 90、進入停滯期或跑滿 3 輪，低於 65 分品質關卡的輸出，除非加上 `--force`，否則拒絕。結果：每個安裝都在自己的語料上越用越聰明，每次執行都能跨機器重現，引擎始終完全離線。

---

## 快速安裝

三條安裝路徑。請挑選與你的環境匹配的那條。

### 路徑 1：Claude Code 市集(權威路徑)

如果你常駐 Claude Code,請透過外掛市集安裝:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

這會將全部 18 個斜線命令（以及作為別名保留到 4.1 的 7 個舊名稱）與 5 個子代理接入你的 Claude Code 會話。安裝完成後，執行 `/ux-init` 以建立專案層級的 `.ux/` 狀態目錄，並確認 Python 引擎可達。

### 路徑 2：pip(通用路徑)

如果你身處 Claude Code 之外(Cursor、Windsurf、CLI、CI),請安裝 Python 套件:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

套件同時暴露 `ux` 與 `uxskill` 兩個 CLI 入口點，它們是同一個執行檔。

### 路徑 3：npx(無需自行管理 Python)

如果你不想直接管理 Python,npx 包裝層會透過 `pipx` 自動拉起:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### 驗證安裝

```bash
ux stats
# {
#   "version": "4.0.0",
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
#     "anti-patterns": 171,
#     "landing-patterns": 40,
#     "brands": 160
#   }
# }
```

這些計數加起來共 1,262 筆。如果任一計數回傳 0，表示對應的 JSON 檔案遺失，請到 [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) 開一個 issue。

---

## 數據對照：與 Top 8 Claude UX 技能的即時比較

Star 數最後一次透過 `gh api` 核對的時間是 **2026-05-28**。ux-skill(Laith0003/ux-skill)是最新入場的，我們在認知度上極小,在架構深度上極深。下面這張表是誠實的:哪裡我們輸,哪裡我們贏。

| 外掛 | Star 數 | 架構 | 斜線命令 | 程式碼檢查器(可上 CI) | 品牌規範 | 元件 | 動效預設 | 支援的 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV,單一 skill | 1 | - |，| 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 個 skill + 預覽 | 19 | - |，| 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + 研究背書的品味 | 1 | - |，| 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 單份 62 KB SKILL.md + 指令稿 | 1 | - |，| 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | 接入 MCP 的 skill 庫 | 多個 | - |，| 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 單一美學 skill | 1 | - |，| 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 反 slop 設計 skill | 1 | - |，| 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 元件 + 稽核 | 1 | - | (僅 MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python 引擎 + 12 份清單 + 18 個命令 + 5 個子代理 + CI 檢查器** | **18** | **171 條確定性規則** | **160** | **148** | **57** | **17** |

### 我們輸在哪裡

- **認知度。** 他們有數十萬顆 star。我們有 14 顆。給我們點個 star，這是成本最低的支持方式。
- **品牌識別度。** ui-ux-pro-max 和 open-design 的領先優勢是按月算的,不是按天。
- **行銷打磨。** 他們有截圖、示範影片和可被搜尋到的著陸頁。我們有一份完備的 README 和一張輕量的著陸頁。

### 我們贏在哪裡

- **元件庫:** 148 個帶解剖結構、狀態、所用 token 與動效規範的文件化元件。其他 8 個裡沒有任何一個發布過元件清單。
- **動效預設:** 57 個開箱即用的堆疊層級項目(Framer Motion、GSAP、CSS),全部帶 reduced-motion 後援。其他幾家都不發布動效清單。
- **反模式靜態檢查器：** 171 條確定性規則，能在 CI 中執行，遇 Critical/High 以非零碼結束。其他幾家沒有任何確定性檢查器。
- **品牌規範:** 160 份真實 DESIGN.md 規範(Apple、Stripe、Linear、Figma、Tesla、BMW、Notion、Spotify、Airbnb、Vercel、Supabase、Cursor、Raycast、Claude,以及其餘 96 個)。其他幾家沒有品牌庫。
- **支援 17 個 IDE:** 同一個引擎,IDE 之間用不同的「膠水」對接。
- **18 個斜線命令：** discovery、生成（頁面、元件、儀表板、從圖片生成）、審查、lint、polish 循環、修正循環、案例研究、工作坊、文案、動效、a11y、conductor，彼此完全打通。

完整的逐欄對照詳見 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 架構：各部件如何咬合

```
ux-skill (package name: uxskill)
│
├── data/                              The brain, queryable JSON manifests
│   ├── styles.json                    84 design styles + when/skip + tokens
│   ├── palettes.json                  176 palettes (light/dark, contrast verified)
│   ├── type-pairs.json                70 display × body × mono triplets
│   ├── components.json                148 components (anatomy, states, motion)
│   ├── industries.json                184 industry rules + audience signals
│   ├── chart-types.json               35 chart types (when/skip, encoding)
│   ├── tech-stacks.json               25 stacks (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 named UX laws (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 motion presets (entry, exit, hover...)
│   ├── anti-patterns.json             171 rules (CI-safe linter source)
│   └── brands/*.json                  160 brand DESIGN specs + _index.json
│
├── engine/                            Python, the reasoning
│   ├── synthesizer/                   v3-7-axis deterministic compiler
│   ├── decisions/                     v3, .ux/decisions.jsonl ledger + recommender re-rank
│   ├── recommender/                   5-parallel-search merge engine (re-ranked by decisions)
│   ├── linter/                        Deterministic anti-slop scanner
│   ├── discovery/                     10-field forcing protocol
│   ├── generator/                     Token + manifest emitter
│   ├── installer/                     17-IDE multi-installer
│   └── cli/                           `ux` / `uxskill` entry point
│
├── commands/                          18 Claude Code slash commands (.md) + 7 aliases
│   ├── ux-init.md                     bootstrap + inventory snapshot (--stats)
│   ├── ux-discover.md                 10-field intake (gate), --frame, --recommend
│   ├── ux-lint.md                     deterministic linter
│   ├── ux-design.md                   generate a page, --component, --dashboard, --from-image
│   ├── ux-system.md                   generate full design system
│   ├── ux-motion.md                   motion treatment + audit
│   ├── ux-audit.md                    6-lens design audit
│   ├── ux-a11y.md                     WCAG 2.1 AA audit
│   ├── ux-critique.md                 taste critique (3 wins, 3 misses, 1 move)
│   ├── ux-copy.md                     microcopy review + rewrite
│   ├── ux-fix.md                      apply findings as atomic commits
│   ├── ux-polish.md                   lint, fix, re-lint loop + taste pass
│   ├── ux-research.md                 research planning + synthesis
│   ├── ux-workshop.md                 5-phase design thinking workshop
│   ├── ux-case-study.md               publishable Wfrah-editorial case study
│   ├── ux-next.md                     workflow conductor (read-only)
│   ├── ux-expert.md                   consulting hook
│   ├── ux-mcp.md                      MCP server
│   └── ux-frame.md, ux-recommend.md, ux-stats.md, ux-evolve.md,
│       ux-component.md, ux-dashboard.md, ux-image-to-code.md
│                                      aliases, removed in 4.1
│
├── agents/                            5 sub-agents (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy in brand voice
│   ├── research-synthesizer.md        interviews + analytics + competitors
│   └── design-system-architect.md     tokens / components / foundations
│
├── references/                        Prose source for the data + demo pages
│   ├── foundations/                   anti-patterns.md, principles, taste
│   ├── laws/                          UX laws long-form
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        per-style prose (anti-slop.md, etc.)
│   ├── components/                    component long-form
│   ├── output/                        output rubrics
│   └── conditional/                   stack-specific guidance
│
├── bin/
│   ├── uxskill.mjs                    npx wrapper -> Python engine
│   ├── ux-lint.py                     v2 linter (preferred)
│   └── ux-lint.sh                     v1 fallback (bash + perl-PCRE)
│
└── .ux/                               (created per project)
    ├── last-discovery.json            brief snapshot
    ├── last-recommendation.json       picked system
    ├── last-frame.json                framing block
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### 引擎實際如何運作

1. **輸入。** 你提供一份簡報，可以透過 `/ux-discover` 互動式填寫（10 個欄位），也可以傳參數給 `ux recommend` 以非互動方式提供。
2. **5 路並行檢索。** 引擎在各清單上同時執行五項查詢：
   - **產業 → recommended_styles** (industries.json)
   - **風格 → 配色 + 字體 + 動效相容性** (styles.json)
   - **語氣 × 必備項 → 配色篩選** (palettes.json)
   - **技術堆疊 → 元件相容性 + 動效預設** (tech-stacks.json, motion-presets.json)
   - **禁用項 + 地區 → 護欄 + 品牌範例候選** (anti-patterns.json, brands/)
3. **合併。** 一個確定性的合併器為候選排序、解決衝突（例如必備的深色模式決定配色模式），並輸出唯一一套推薦系統。
4. **輸出。** 一份 JSON 文件，包含選定的風格、配色、字體搭配、前 5 個動效預設、前 12 個元件、前 5 個品牌範例，以及全部啟用的 171 條反模式護欄。另附一段說明每項選擇理由的依據。
5. **生成。** 後續命令（頁面、元件、儀表板與圖片模式下的 `/ux-design`，以及 `/ux-system`）使用這份推薦，經由子代理生成真正的程式碼。
6. **驗證。** `/ux-lint` 以 171 條規則重新掃描生成的程式碼。CI 中遇 Critical/High 以非零碼結束。

**v3 新增。** 推薦器現在藉助 `.ux/decisions.jsonl` 從 `engine/decisions/` 對候選重新排序（僅計算 `lint_score >= 80` AND `user_accepted = true` 的決策；先前的決策少於 3 筆時以冷啟動安全處理）。生成路徑可以轉入 `engine/synthesizer/`，這是一個確定性的 7 軸編譯器，會為每份簡報產出全新的配色 + 字體 + 間距 + 圓角 + 動效 token，而不是從目錄裡挑範本。詳見[大腦，v3.0 是什麼](#大腦v30-是什麼)。

**Python 負責思考。HTML 負責呈現。Markdown 負責串接。**

---

## 18 個斜線命令：詳細參考

每個命令都以 `.md` 檔案形式放在 `commands/` 下，包含 `description`、`allowed-tools`、`triggers`、`when to use`、`when to skip`、`input`、`process` 與 `output state file`。下面的描述是精簡版；完整原始檔才是權威規格。

命令分為七組：**引導與盤點**、**探索與推薦**、**生成**、**審查與驗證**、**修正與打磨**、**探索與敘事**，以及**指揮**。七個 3.x 名稱在 4.1 之前仍可作為[別名](#別名將在-41-移除)使用。

### 初始化與存貨

#### `/ux-init`：為專案做初始化

- **做什麼：** 識別你在哪個 IDE（`.claude/`、`.cursor/`、`.windsurf/` 等），安裝匹配的產出物，確認 Python 引擎可達，印出一份統計快照。`--stats` 只印出快照：版本 + 各資料清單的條目數。
- **何時使用：** 在新專案裡首次安裝；clone 了使用 ux-skill 的專案之後；`pip install --upgrade uxskill` 之後。`--stats` 用於安裝後、升級後，或推薦結果出乎意料、懷疑清單不完整時。
- **何時跳過：** 你已經在這個專案裡跑過，而且沒有任何變動。`--stats` 永遠不必跳過：它只是一次 50ms 的讀取。
- **呼叫方式：** `/ux-init`（無參數）、`/ux-init --stats`，或在 CLI 裡跑 `uxskill init` / `uxskill stats`。`--decisions` 會附上決策日誌摘要；`--html` 會寫出 `.ux/stats.html`。
- **輸出：** 各 IDE 對應的產出物（詳見[面向 17 個 IDE 的安裝程式](#面向-17-個-ide-的安裝程式)）+ `.ux/` 目錄 + 標準輸出摘要。`--stats`：向標準輸出印出 JSON（見上文[驗證安裝](#驗證安裝)）。
- **下接：** 接下來是 `/ux-discover`。`--stats` 僅供診斷。

#### `/ux-mcp`：把引擎當作 MCP 伺服器執行

- **做什麼：** 透過 stdio 把引擎當作 Model Context Protocol 伺服器啟動。25 個工具（推薦器、檢查器、持久化、合成器、決策日誌、圖片擷取、各資料清單，以及設計系統的建立、匯入、強化、擴充、匯出與檢查）無需外掛即可從任何支援 MCP 的主機呼叫。
- **何時使用：** 你在另一個支援 MCP 的主機裡工作，想用同一個引擎。你執行的多代理管線需要單一的設計約束來源。你想在 CI 中把推薦器或檢查器當作常駐程序。
- **何時跳過：** 你在已安裝外掛的 Claude Code 裡；斜線命令已經能直達引擎。你只需要一次性的答案；`uxskill recommend` 或 `uxskill lint` 更簡單。
- **呼叫方式：** `/ux-mcp`，或在 `pip install 'uxskill[mcp]'` 之後從 shell 執行 `ux-mcp`。
- **輸出：** 一個 stdio JSON-RPC 伺服器。各用戶端的設定見 [MCP 伺服器](#mcp-伺服器非對稱的一著) 與 `commands/ux-mcp.md`。
- **下接：** 無；它是傳輸層，不是一個步驟。

### discovery 與推薦

#### `/ux-discover`：強制關卡（10 欄位擷取、框定、推薦）

- **做什麼：** 每個專案在執行任何生成命令之前都必須完成的 10 欄位擷取。專案類型、受眾、主要目標、語氣、必備項、禁用項、參考品牌、技術堆疊、地區、成功指標。**不許即興發揮。** 被禁用的詞（「modern」、「clean」）逼使用者說具體。接著執行推薦器：Python 引擎在 12 份清單上做 5 路並行檢索，回傳一套合併後的設計系統（產業 → 風格 → 配色 → 字體 → 動效 + 元件 + 品牌範例 + 護欄）。
- **模式：** `--frame` 用一個四欄位的框定區塊記錄為誰、成果、假設與成功訊號，比完整擷取更輕量。`--recommend` 只執行推薦器，輸入來自已儲存的簡報或一次性參數。
- **何時使用：** 在任何 `/ux-design` 或 `/ux-system` 之前。每當先前的簡報已經過時。`--frame` 用在專案、衝刺或一次性任務的開頭，或對話離題時的半途中。`--recommend` 用在為一個看起來疲態的產品重新定位時。
- **何時跳過：** 你在修 bug（`/ux-fix`）；你只是跑一遍檢查器（`/ux-lint`）；簡報自上次會話以來沒有變化。
- **呼叫方式（Claude Code）：** `/ux-discover`、`/ux-discover --frame "loyalty wallet for a MENA retail pilot"` 或 `/ux-discover --recommend`。
  **呼叫方式（CLI）：**
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
- **輸出：** `.ux/last-discovery.json`（10 欄位簡報）、`.ux/last-recommendation.json`（選定的風格、配色、字體搭配、前 5 個動效預設、前 12 個元件、前 5 個品牌範例、全部啟用的 171 條反模式護欄，以及依據），使用 `--frame` 時另有 `.ux/last-frame.json`（`{audience, outcome, hypothesis, success_signal}`）。
- **下接：** `/ux-design [extra brief]` → 以推薦為依據的前端程式碼。`/ux-design --component <name>` → 符合已發現約束的單一元件。`/ux-system` → 由推薦生成的完整設計系統。`/ux-lint` → 驗證生成的程式碼。

### 生成

#### `/ux-design`：由簡報生成漂亮、反 slop 的介面

- **做什麼：** 由 discovery 簡報 + 推薦生成完整的生產級前端產出物（著陸頁、行銷站、應用外殼）。在反 slop 與 arsenal 參考的創意指引下，派遣 `frontend-engineer`。由簡報或參數在四種模式中擇一：
  - **頁面**（預設）：一個完整頁面或多區塊介面。寫入 `.ux/last-design.json`。
  - **`--component [name]`**：單一生產級元件（按鈕、對話框、導覽列、側邊欄、卡片、表格、表單、圖表）。四種互動狀態齊全，無障礙，貼合品牌。先在 `.ux/last-recommendation.json` 中尋找該元件，找不到再直接查詢清單。寫入 `.ux/last-component.json`。
  - **`--dashboard`**：講究資料密度、bento 版面、表格等寬數字、sparkline 模式、避免卡片氾濫、語意化狀態色、克制的動效。不是貼了幾張圖表的行銷站。寫入 `.ux/last-dashboard.json`。
  - **`--from-image <path>`**：用純 Pillow 電腦視覺讀取一張設計參考圖（PNG/JPG/WebP）（主色盤、畫布明暗、字體訊號），與配色與風格清單比對，再依得到的推薦來建立。`--extract-only` 在擷取後停止。寫入 `.ux/last-image-extract.json`。
- **何時使用：** 「設計一個」、「幫我做一個」、「生成一個著陸頁」、「做一個儀表板」、「做一個元件」、「做一個按鈕」、「設計後台管理面板」、「營運主控台」、「KPI 看板」、「照這張截圖做」，任何形式自由的視覺交付請求。
- **何時跳過：** 你要的是評審而不是建造（用 `/ux-audit` 或 `/ux-critique`）；後端或基礎建設工作。
- **呼叫方式：** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`、`/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`、`/ux-design --dashboard`、`/ux-design --from-image ref.png`。
- **輸出：** 生成的程式碼（HTML / Blade / JSX / Vue / Astro），外加該模式的狀態檔。
- **下接:** `/ux-lint` → 驗護欄;`/ux-polish` → 拋光;`/ux-a11y` → 無障礙稽核;`/ux-copy` → 微文案稽核;`/ux-fix` → 以原子提交落地。

#### `/ux-system`：生成一套完整的起步設計系統

- **做什麼:** 為還沒有設計系統的專案提議一整套起步系統，tokens(顏色、字體、間距、動效、圓角、陰影)、基礎文件、元件契約、暗色模式對應、主題切換器。派遣 `design-system-architect`。
- **何時使用:** 「我們沒有設計系統」、「給我們搭一套」、「提議一份 tokens」、「我們的主題該長什麼樣」、「把 DS 搭起來」。
- **何時跳過：** 專案已經有設計系統，改用 `/ux-design --component` 基於現有系統建造即可；後端或基礎建設。
- **呼叫方式：** `/ux-system create`（設計基礎引擎）、`/ux-system enhance --from <file>`（量測你已有的系統）、`/ux-system extend --from <file> --add <foundation>`（在不更動的前提下擴充），或 `/ux-system`（3.x 流程；若尚未存檔，先跑 discovery）。
- **輸出:** `tokens.json`、`foundations.md`、`components/*.md` 契約,可選輸出 Tailwind / vanilla / SCSS。寫入 `.ux/last-system.json` 以供後續銜接。
- **下接：** `/ux-design --component` → 基於新系統建造。`/ux-design` → 用新 token 生成介面。

#### `/ux-motion`：動效處理

- **做什麼:** 生成介面的動效層，時長、緩動、編排、reduced-motion 後援、效能紀律。也對現有動效按五個維度做稽核(時長、緩動、含義、reduced-motion、效能)。
- **何時使用:** 「檢查一下動效」、「動畫做得對不對」、「修一下動效」、「複核動畫」、「動效稽核」、「對動效做效能掃」。
- **何時跳過:** 介面沒有動效(用 `/ux-audit` 或 `/ux-polish`);後端或基礎建設。
- **呼叫方式:** `/ux-motion path/to/component.tsx`(稽核模式)或 `/ux-motion --generate hero-entry`(生成模式)。
- **輸出:** 更新後的程式碼(生成模式)或 `.ux/last-motion.json` 報告(稽核模式)。
- **下接:** `/ux-fix` → 落地動效結論;`/ux-polish` → 拋光。

### 稽核與驗證

#### `/ux-lint`：基於 regex 的確定性檢查器(無 LLM,CI 安全)

- **做什麼：** 對你的程式碼跑 171 條規則。無 LLM 呼叫。CI 中遇 Critical / High 以非零碼結束。原始檔：`data/anti-patterns.json`。規則覆蓋 A11y（45）、內容（35）、配置（18）、字體（16）、動效（14）、視覺（14）、品質（12）、顏色（10）、效能（5）、層次（2）。
- **何時使用：** 預提交鉤子；CI 關卡；在花 `/ux-audit` 成本之前對大型程式碼庫做的快速首輪；在任一模式的 `/ux-design` 之後用於驗證生成。
- **何時跳過:** 你想要修復循環(檢查器只報告、不修改，請接 `/ux-polish --fix` 或 `/ux-fix`);你想要品味判斷(用 `/ux-critique`)。
- **呼叫方式(slash):** `/ux-lint src/`。
- **呼叫方式(CLI):** `uxskill lint .` 或 `python3 bin/ux-lint.py .` 或 `bash bin/ux-lint.sh --ci --fail-on high`。
- **呼叫方式(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **輸出:** 標準輸出中的命中(位置、規則 id、嚴重等級、證據)。無命中時結束碼 0,設了 `--fail-on high` 且命中 Critical/High 時結束非零。
- **下接:** `/ux-polish --fix` → 同類模式的 LLM 版對手;`/ux-fix` → 按嚴重等級落地為提交;`/ux-audit` → 完整的六鏡頭推理回合;`/ux-next` → 讓指揮來決定。

#### `/ux-audit`：六鏡頭設計稽核

- **做什麼:** 一次結構化、帶立場的評審,從六個鏡頭(清晰度、層級、無障礙、聲音、動效、品味)出發,產出按嚴重等級打標的發現。Polaris 風格的報告。先讀 `.ux/last-frame.json`，受眾與結果決定每條發現的嚴重等級。
- **何時使用:** 介面已存在,你需要一份能站得住腳的批評。「稽核一下」、「看看這版 UX」、「做得好不好」、「哪裡壞了」、「狠狠拆一下」。
- **何時跳過:** 介面尚未存在(用 `/ux-design`);使用者只要一個鏡頭(用對應專項命令:`/ux-a11y`、`/ux-copy`、`/ux-motion`、`/ux-polish`);使用者想要品味觀點(用 `/ux-critique`);後端或基礎建設。
- **呼叫方式:** `/ux-audit https://example.com/pricing` 或 `/ux-audit src/components/Pricing.tsx`。
- **輸出:** 寫入 `.ux/last-audit.json`，`findings` 陣列,欄位為 `{lens, severity, title, principle, evidence, fix}`,以及 `severity_counts`、`dominant_lens`、`strategic_moves`。
- **下接:** `/ux-fix` → 落地;`/ux-polish` → 拋光;`/ux-design` → 若需結構性重設計。

#### `/ux-a11y`：WCAG 2.1 AA 稽核 + 基本禮貌檢查

- **做什麼:** 一次結構化的 WCAG 2.1 AA 稽核,外加那些自動工具能放行、但仍會傷害真實使用者的「基本禮貌」檢查(可見焦點、錯誤具體性、動效偏好、鍵盤陷阱、顏色依賴)。
- **何時使用:** 發布前無障礙關卡;重新設計之後;「做一下無障礙檢查」、「WCAG 稽核」、「這個無障礙嗎」、「a11y 複核」、「讀屏測試」、「鍵盤導覽檢查」。
- **何時跳過:** 不面向使用者;後端或基礎建設;還在草圖階段的工作。
- **呼叫方式:** `/ux-a11y https://example.com`(優先用線上 URL，自動工具和鍵盤測試只能在線上跑)。
- **輸出:** 寫入 `.ux/last-a11y.json`，`findings` 陣列,欄位為 `{wcag_sc, sc_name, severity, title, evidence, fix, category}`、`beyond_wcag` 陣列、`severity_counts`。
- **下接:** `/ux-fix` → 落地為提交;`/ux-copy` → 在一次文案回合中順手修 alt 文字和表單錯誤串接。

#### `/ux-critique`：品味評點(3 個亮點、3 個失分、1 步關鍵招)

- **做什麼:** 一個設計師的態度，不是結構化稽核,不是嚴重等級打分,只是一段緊緻、有立場的看法,點名什麼在起作用、什麼沒起作用,以及那一步能改變最多的關鍵招。
- **何時使用:** 「你怎麼看」、「這個好嗎」、「評點一下」、「實話說」、「語氣對不對」、「這像我們嗎」、「該不該發」。
- **何時跳過:** 使用者明確要的是結構化稽核(用 `/ux-audit`);後端或基礎建設。
- **呼叫方式:** `/ux-critique https://example.com`。
- **輸出:** 寫入 `.ux/last-critique.json`，3 個亮點、3 個失分、1 步關鍵招,外加散文。
- **下接:** 如果評點建議重設計就接 `/ux-design`;如果建議收緊就接 `/ux-polish`。

#### `/ux-copy`：微文案稽核 + 重寫

- **做什麼:** 用聲音量規評估每一句可見文案,產出 before/after 重寫。專抓:「表單存在錯誤」(籠統)、「John Doe」(佔位符)、AI 式歡欣鼓舞的慶祝話術、籠統的 CTA、空蕩蕩的空狀態、毫無用處的錯誤提示。
- **何時使用:** 結構對了但文案弱。「複核文案」、「修微文案」、「錯誤提示糟糕」、「重寫這個」、「收緊文案」、「按鈕太籠統」、「空狀態死氣沉沉」。
- **何時跳過:** 配置問題(用 `/ux-audit` 或 `/ux-polish`);無障礙驅動的文案問題如 alt 文字(用 `/ux-a11y`);後端或基礎建設。
- **呼叫方式:** `/ux-copy src/views/checkout.blade.php`。
- **輸出:** 寫入 `.ux/last-copy.json`，`strings` 陣列,欄位為 `{location, severity, before, after, notes}`,以及量規與需翻譯的語言。
- **下接:** `/ux-fix` → 落地重寫;`/ux-a11y` → 在文案改動後再複核。

### 修復與拋光

#### `/ux-fix`：以原子提交落地稽核結果

- **做什麼:** 從 `.ux/` 讀取最近的報告(audit、copy、a11y、motion 或 polish),校驗工作樹,經由對應子代理把發現以原子提交的形式落地。落地後會重跑觸發命令再核驗。
- **何時使用:** 跑完一個稽核類命令並回顧了發現之後。「修一下這些發現」、「把修復落地」、「跑修復循環」、「打修補程式」、「按建議改」、「去修」。
- **何時跳過:** `.ux/` 裡沒有先前的報告;工作樹是髒的且使用者尚未同意 stash/commit;修復需要設計判斷而不是機械落地(請改用 `/ux-design` 重設計)。
- **呼叫方式:** `/ux-fix`(自動識別要修哪份報告)或 `/ux-fix --from=last-a11y.json`。
- **輸出:** 每條發現一個原子提交。重跑觸發命令並更新 `.ux/last-*.json`。印出一段摘要。
- **下接:** `/ux-next` → 由指揮挑下一步。

#### `/ux-polish`：lint、修正、再 lint 的循環 + 清除 AI slop

- **做什麼：** 先對本機 HTML 檔案跑一個確定性的循環：lint，執行六遍冪等的打磨，再 lint，直到分數達到 90、進入停滯期或跑滿三輪（`--rounds` 可改上限）。預設情況下循環結果留在 `<file>.evolved.html`，原檔絕不更動。只有 `--loop-only` 或 `--fix` 會在確認工作區乾淨後取代原檔，而 65 分的品質關卡會阻止未通過的結果取代原檔，除非加上 `--force`；使用 `--brand-file` 時，品牌忠實度下限在每個出口都成立。接著是品味打磨：間距節奏、層級強化、AI slop 偵測、token 一致性。它是 `/ux-lint` 的 LLM 驅動版，在品味問題上依靠你的判斷。`--loop-only` 只跑循環；`--no-loop` 只做品味打磨；`--fix` 套用品味方面的發現。
- **何時使用：** 結構沒問題但執行鬆散。「打磨一下」、「收緊一點」、「去掉 AI slop」、「做得高級點」、「別那麼像 AI」、「間距不對勁」、「看起來很普通」、「需要更有品味」、「改到 90 分以上」、「弄到能上線」。
- **何時跳過：** 介面缺少核心功能（先修那個）；需要重新設計而不是打磨（用 `/ux-design`）；文案問題（用 `/ux-copy`）；動效問題（用 `/ux-motion`）；a11y 問題（用 `/ux-a11y`）。
- **呼叫方式：** `/ux-polish src/components/Hero.tsx`、`/ux-polish out/landing.html --css out/landing.css`、`/ux-polish out/landing.html --loop-only --rounds 5`。
- **輸出：** 循環產出的 `<file>.evolved.html`（僅在 `--loop-only` 或 `--fix` 下取代原檔）、`--fix` 下更新後的程式碼、`.ux/last-evolve.json`、`.ux/decisions.jsonl` 中的一行，以及描述品味發現的 `.ux/last-polish.json`。
- **下接：** `/ux-lint` → 驗證打磨效果有守住。`/ux-a11y` → 重新檢查無障礙。

### discovery 與敘事

#### `/ux-research`：研究計畫 + 綜合

- **做什麼:** 計畫模式:寫訪談腳本、問卷、招募篩選器。綜合模式(`--synthesize`):把訪談、分析、競品站點、A/B 結果、客服工單消化為建議。派遣 `research-synthesizer`。
- **何時使用:** 「計畫一次研究」、「我需要訪談題」、「設計一份問卷」、「如何招募使用者」、「使用者測試計畫」、「日記研究」、「偏好測試」、「fake door」、「smoke test」、「把我的訪談筆記綜合一下」。
- **何時跳過:** 答案已有高信心度;低風險且可逆的決策;後端或基礎建設。
- **呼叫方式:** `/ux-research --plan "loyalty wallet adoption in MENA"` 或 `/ux-research --synthesize interviews/*.md`。
- **輸出:** 寫入 `.ux/last-research.json`，研究計畫,或綜合後的主題 + 證據 + 建議。
- **下接：** `/ux-discover --frame` → 把研究發現整合進框定。`/ux-design` → 依據發現生成。`/ux-workshop` → 以研究為輸入開一場工作坊。

#### `/ux-workshop`：五階段設計思考工作坊

- **做什麼:** 端到端主持一場 discovery / 設計思考工作坊。五個順序階段(探索 → 熱度圖 → 利害關係人地圖 → 解決方案草圖 → 行動方案)。計時;每階段都有具體產出物。結束於一個決定,而不是「有趣的發現」。
- **何時使用:** 真問題、真參與者、真時間預算。「開一場工作坊」、「主持一次 discovery」、「來一次設計思考」、「我有利害關係人一小時,該幹啥」、「專案啟動」。
- **何時跳過：** 簡報已經清楚且範圍明確；獨自腦力激盪（用 `/ux-design` 或 `/ux-discover --frame`）；團隊正處在執行中段而非探索階段。
- **呼叫方式:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`。
- **輸出:** 寫入 `.ux/last-workshop.json`，行動方案 + 各階段產出物。
- **下接:** `/ux-design` → 執行行動方案;`/ux-research` → 補工作坊暴露的缺口;`/ux-case-study` → 把過程發表。

#### `/ux-case-study`：可發布的案例研究(Wfrah 編輯格式)

- **做什麼：** 以純黑白的編輯風格生成專案案例研究：Wfrah 字體、細線分隔、從 (A) 到 (G) 編號的章節代碼、適合雙語的版面。它是一份文件，而不是行銷手冊。讀取 `.ux/last-frame.json`、`.ux/last-workshop.json`、`.ux/last-research.json`、`.ux/last-design.json`、`.ux/last-a11y.json`、`.ux/last-polish.json`、`.ux/last-recommendation.json`、`.ux/last-discovery.json`。
- **何時使用:** 發布後;經歷一個明確里程碑後。「寫一份案例研究」、「把這個專案做成案例」、「做收尾文件」、「把這工作發出來」、「作品集篇」。
- **何時跳過：** 專案缺少填入 (A) 到 (G) 各章節的資料；使用者要的是行銷著陸頁而不是案例研究（用 `/ux-design`）。
- **呼叫方式:** `/ux-case-study --format=html --slug=bashiti-loyalty`。
- **輸出:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`。
- **下接:** 終端命令，通常是專案的句點。

### 指揮

#### `/ux-next`：工作流指揮(唯讀)

- **做什麼:** 讀取每個 `.ux/last-*.json`,指認下一步槓桿最大的命令。它是指揮,不是建造者。唯讀。
- **何時使用:** 在命令之間。「接下來該做什麼」、「下一步是什麼」、「替我決定」、「從這裡往哪走」。
- **何時跳過:** `.ux/` 裡沒有先前報告;你心裡已有具體的下一條命令。
- **呼叫方式:** `/ux-next`(無參數)或 `/ux-next --focus=a11y`。
- **輸出:** 標準輸出，建議的下一條命令 + 理由。
- **下接:** 它挑哪條就接哪條。

#### `/ux-expert`：諮詢入口

- **做什麼:** 在使用者索取真人 UX 專家時,展示外掛作者的聯絡方式。簡短、直接、無行銷話術。
- **何時使用:** 「誰做的這個」、「我需要個 UX 專家」、「你做諮詢嗎」、「能雇個人幫我嗎」、「這外掛背後有人嗎」。
- **何時跳過:** 使用者問的是外掛功能,不是諮詢。
- **呼叫方式:** `/ux-expert`。
- **輸出:** 一張含 LinkedIn / 電子郵件 / 儲存庫的簡短聯絡卡。

### 別名，將在 4.1 移除

七個 3.x 命令已併入上面的 18 個命令。它們的名稱在一個版本內仍可使用：每個別名會說明自己移到了哪裡，然後以相同參數執行新命令。

| 舊命令 | 現在 | 說明 |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | 同樣的框定區塊，同樣的 `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | MCP 工具 `ux_recommend` 不變 |
| `/ux-stats` | `/ux-init --stats` | 唯讀快照 |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | 別名保留舊的五輪上限；單獨的 `/ux-polish` 跑滿三輪即停 |
| `/ux-component` | `/ux-design --component` | 同樣的 `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | 同樣的 `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | 拿掉 `--extract-only` 即依圖片建立 |

### 命令串聯圖

```
                  ┌──────────────────────┐
                  │  /ux-init            │  --stats: inventory
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10-field intake (FORCING GATE)
                  │                      │  --frame: 4-field framing block
                  │                      │  then 5 parallel searches -> merged system
                  └────────────┬─────────┘
                               │ writes .ux/last-discovery.json
                               │ writes .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-motion      │ │ /ux-system  │
   │  --component   │ │                 │ │             │
   │  --dashboard   │ │                 │ │             │
   │  --from-image  │ │                 │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ writes .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ writes .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  apply findings as commits
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  publishable artifact
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor, read-only
                  │  /ux-expert          │  consulting hook
                  └──────────────────────┘
```

---

## 5 個子代理

子代理是由命令派遣的角色化生成器。它們從不獨立執行，由 `/ux-design`、`/ux-system`、`/ux-fix`、`/ux-research` 等命令呼叫。每個代理都有清楚的職責邊界：它們**不**決定簡報，只依簡報執行。

### `frontend-engineer`

- **職責:** 生產級前端程式碼(React、Next.js、Vue、Blade+Alpine、原生 HTML、Astro),並保持反 AI-slop 紀律。
- **派遣者：** `/ux-design`（頁面、元件、儀表板與圖片模式）、`/ux-fix`。
- **輸入:** 簡報 + 創意指引 + tokens(來自 `.ux/last-recommendation.json`)。
- **輸出:** 與通用 AI 輸出可區分的可執行程式碼。不出現紫色漸層、不置中 hero、不三張等大卡片、不用 Inter 當顯示字、不出現「John Doe」、不放 emoji、不留 300ms 的預設值。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `motion-engineer`

- **職責:** 生產前端程式碼中的動效，Framer Motion、GSAP、CSS 動畫。時長、緩動、編排、reduced-motion 後援、效能紀律。
- **派遣者：** `/ux-design`（所有模式）、`/ux-motion --fix`。
- **輸入:** 動效簡報 + tokens + 來自 `data/motion-presets.json` 的 57 個預設。
- **輸出:** 配得上自己位置的動效。永遠包裹在 `prefers-reduced-motion` 後援中。永遠拿 Core Web Vitals 測一遍。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `copy-writer`

- **職責:** 真正會發布的文案，錯誤訊息、空狀態、CTA、loading 狀態、成功訊息、toast、輔助文字、表單標籤、按鈕文字。
- **派遣者：** `/ux-copy --fix`、`/ux-design`（所有模式）、`/ux-discover --frame`。
- **輸入:** 聲音檔案(命名或貼上) + 介面的文案。
- **輸出:** 在介面各個狀態間一致套用的生產級微文案,讓產品聽起來像一個產品,不像十個。禁忌:「表單存在錯誤」、「John Doe」、AI 式歡欣鼓舞的慶祝話術、籠統 CTA、空蕩蕩的空狀態。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `research-synthesizer`

- **職責:** 把研究輸入(訪談、分析、競品站點、A/B 結果、客服工單)消化為可執行的設計建議。
- **派遣者：** `/ux-research`、`/ux-workshop`、`/ux-discover --frame`。
- **輸入:** 原始研究素材，訪談記錄、匯出檔案、競品 URL、客服群集。
- **輸出:** 主題、證據、建議。不替設計師設計答案，而是把可供設計的底料交給設計師。
- **工具:** `Read, Write, WebFetch, Bash, Glob, Grep`。

### `design-system-architect`

- **職責:** 完整的設計系統，tokens(顏色、字體、間距、動效、圓角、陰影)、基礎文件、元件契約、暗色模式對應、主題化層。
- **派遣者：** `/ux-system`，以及尚無系統時的 `/ux-design --component`。
- **輸入:** 品牌簡報 + `.ux/last-recommendation.json`(風格 + 配色 + 字體搭配 + 動效預設)。
- **輸出:** 一套連貫、立場鮮明、可上生產的系統,讓下游代理無需重新決定根基就能建造。tokens JSON、基礎 MD、元件契約、暗色對應。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### 子代理派遣協定

當一個命令派遣子代理時,它會傳入:

1. 簡報 / 推薦(從 `.ux/` 載入)。
2. 與之相關的清單切片(例如 `frontend-engineer` 拿到選定的風格 + 配色 + 元件;`motion-engineer` 拿到選定的動效預設)。
3. 171 條反模式護欄（始終啟用）。
4. 一個成功判據(產出物必須做到什麼)。

子代理回傳:

1. 產出物(程式碼、文件、系統)。
2. 一段理據(為什麼這樣選)。
3. 對照護欄的自檢(他們驗證了哪些規則)。

呼叫方命令隨後會自動跑 `/ux-lint`,通過之後才宣告完成。

---

## 11 份資料清單

資料層就是大腦。每個命令都從中讀取;引擎在其間合併;程式碼檢查器對其掃描。所有檔案都在 `data/` 下,項目用 `{_meta, entries}` 包裝以做 schema 版本管理。

### `styles.json`：84 種設計風格

| 欄位 | 描述 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`、`name`、`category`、`philosophy`、`when_to_use`、`when_to_skip`、`tokens`、`references`、`compatible_palettes`、`compatible_type_pairs`、`compatible_motion`、`compatible_industries`、`taste_score` |
| `categories` | Minimalist / Swiss、Brutalist、Editorial、Glassmorphism、Neumorphism、Bento、Skeuomorphic、Industrial、Maximalist、AI-Futurist、MENA-modern、Vaporwave 等 |
| `sample entry` | `swiss-international`，「網格即法律。字體承擔重活。裝飾即失敗。」 |

由 `/ux-discover`、`/ux-system`、`/ux-design` 使用。Schema：[data/SCHEMAS.md](data/SCHEMAS.md)。

### `palettes.json`：176 套配色

| 欄位 | 描述 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`、`name`、`mode`(明/暗)、`tone`、`colors`(canvas、surface、ink、body、muted、primary、primary_active、hairline、success、warning、danger、accent)、`wcag_contrast_audit`、`compatible_industries` |
| `tones` | warm、editorial、magazine、clinical、playful、brutalist、monochrome、jewel-tone、MENA-warm、dev-tools-dark 等 |
| `sample entry` | `claude-warm-editorial`，明色,warm/editorial/magazine,canvas #faf9f5,primary #cc785c |

由 `/ux-discover`、`/ux-system` 使用。對比依 AA / AAA 驗證。Schema：[data/SCHEMAS.md](data/SCHEMAS.md)。

### `type-pairs.json`：70 組字體搭配

| 欄位 | 描述 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`、`name`、`display`(family + weights + source + license + URL)、`body`、`mono`、`compatible_styles`、`taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`，Cormorant Garamond × Inter × JetBrains Mono |

所有字體家族都附有授權 + 來源 URL。由 `/ux-discover`、`/ux-system` 使用。

### `components.json`：148 個元件

| 欄位 | 描述 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`、`name`、`category`、`purpose`、`anatomy`、`states`、`tokens_used`、`motion`、`accessibility`、`compatible_styles`、`compatible_industries`、`code_skeleton` |
| `categories` | Navigation、Forms、Data Display、Feedback、Overlays、Layout、Content、Marketing、E-commerce、Auth、Dashboard、Charts、Empty States、Loading States、Error States |
| `sample entry` | `mega-nav-product-grid`，Mega Navigation、Product Grid，6 段解剖、4 個狀態 |

這是我們最深的護城河。其他 Claude UX 外掛沒有發布過結構化的元件清單。

### `industries.json`：184 條產業規則

| 欄位 | 描述 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`、`name`、`category`、`characteristics`、`audience_signals`、`recommended_styles`、`recommended_palettes`、`recommended_type_pairs`、`recommended_motion`、`regulatory_notes`、`regional_notes` |
| `categories` | Financial Services、Healthcare、Education、E-commerce、SaaS B2B、SaaS B2C、Developer Tools、Media、Gaming、Travel、Real Estate、MENA-specific 等 |
| `sample entry` | `fintech-neobank`，高信任、監管揭露、餘額/交易為主 UI、日活的行動優先 |

由推薦器（`/ux-discover`）作為首條並行檢索軸。

### `chart-types.json`：35 種圖表

| 欄位 | 描述 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`category`、`when_to_use`、`when_to_skip`、`encoding`、`accessibility`、`data_shape`、`compatible_styles` |
| `categories` | Comparison、Time Series、Distribution、Composition、Relationship、Flow、Geographic |
| `sample entry` | `bar-vertical`，比較 4 到 15 個離散類別。x 軸位置表示類別；高度表示數值。 |

由 `/ux-design --dashboard` 與 `/ux-design --component`（圖表實例）使用。

### `tech-stacks.json`：25 個技術堆疊

| 欄位 | 描述 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`、`name`、`category`、`tier`、`languages`、`ssr`、`rsc`、`compatible_styling`、`scaffold_command`、`compatible_motion`、`gotchas` |
| `tiers` | production、prerelease、experimental |
| `sample entry` | `nextjs-15-app-router`，Next.js 15(App Router),TS/JS,SSR,RSC,相容 Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

其他技術堆疊包括 Astro、SvelteKit、Remix、Nuxt 3、Solid Start、Qwik、Blade+Alpine、Hotwire、Phoenix LiveView、Hydrogen 2025。

### `ux-guidelines.json`：112 條具名 UX 法則

| 欄位 | 描述 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`、`name`、`category`、`source`、`principle`、`application`、`examples`、`caveats`、`related_laws` |
| `categories` | Decision Cost、Attention、Memory、Motor Control、Visual Perception、Social、Emotional、Form、Error Handling、Onboarding、Empty State 等 |
| `sample entry` | `hicks-law`，決策時間隨選項數量呈對數成長 |

由 `/ux-audit`(六鏡頭打分)與 `/ux-critique`(品味錨)使用。

### `motion-presets.json`：57 個動效預設

| 欄位 | 描述 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`、`name`、`category`、`tokens`(duration_ms、easing、transform_from/to、opacity_from/to)、`stacks`(framer_motion、gsap、css)、`accessibility`(reduced-motion 後援)、`when_to_use` |
| `categories` | Entry、Exit、Hover、Focus、Tap、Loading、Empty、Success、Error、Scroll-linked |
| `sample entry` | `fade-up-12px`，360ms,`cubic-bezier(0.16, 1, 0.3, 1)`,translateY(12px) → 0,opacity 0 → 1 |

每個預設都有一個 reduced-motion 變體。Framer Motion、GSAP 和純 CSS 都提供開箱可用的程式碼。

### `anti-patterns.json`：171 條規則

| 欄位 | 說明 |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`、`name`、`severity`（critical/high/medium/low）、`category`、`detection`（類型、模式、旗標、範圍，許多規則另有一項針對剖析後檔案的 `post` 檢查）、`why`、`fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

完整規則清單見 [171 條反 AI slop 規則](#171-條反-ai-slop-規則程式碼檢查器)。

### `brands/*.json`：160 份品牌規範

| 欄位 | 描述 |
|---|---|
| `entries` | 160(再加一份 `_index.json` 列出全部) |
| `keys per entry` | `id`、`name`、`category`、`voice`、`tokens`(color、type、motion)、`design_principles`、`signature_moves`、`anti-moves`、`references` |
| `categories` | Developer Tools(36)、Consumer / Lifestyle / Retail(19)、Fintech / Crypto(14)、Editorial / Media(13)、AI / ML Platform(12)、Productivity / Collaboration(8)、Automotive(8) |

完整名單見[160 份 DESIGN.md 品牌規範](#160-份-designmd-品牌規範按類別)。

---

## 171 條反 AI slop 規則：程式碼檢查器

ux-skill 內建一個確定性的檢查器：每條規則都是一個模式，許多規則還會對剖析後的 CSS 與標記再做一次檢查，因此只有在規則指定的情境中相符才算數。**無 LLM。** **無 API。** **無網路。** 在典型的 Next.js 應用上，CI 中約 200ms 跑完。設定 `--fail-on high` 時，遇到 Critical / High 發現會以非零碼結束。

規則來源為 `data/anti-patterns.json`（v2，首選），以 `references/foundations/anti-patterns.md` 作為備援（v1，bash）。附帶兩個執行檔：`bin/ux-lint.py`（Python，快速，可擴充）與 `bin/ux-lint.sh`（Bash + perl-PCRE，用於沒有 Python 的環境）。

### 按類別的規則

全部 171 條規則依類別、再依嚴重程度排列的完整目錄，由 `data/anti-patterns.json` 生成於[英文 README](README.md#rules-by-category) 中；其中的規則 ID 與名稱與檢查器的輸出一致。規則覆蓋 A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2)。

### 檢查器用法

**一次性掃描:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 份 DESIGN.md 品牌規範：按類別

真實的品牌。真實的設計語言。真實的 DESIGN.md 規範，不是通用配色。告訴外掛「按 Stripe 的風格做個著陸頁」,它會讀取真實的品牌詞彙表:聲音量規、顏色 tokens、動效約定、招牌手法、反向手法。

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

另外 8 個熱門 Claude UX 外掛生成的是「現代極簡」或「乾淨儀表板」，同一種預設美學的變體。ux-skill 讓你能要**Linear 的清晰**、**Stripe 的嚴肅**、**Apple 的克制**、**Tesla 的整塊感**、**Notion 的親和**、**Cursor 的漸層紀律**、**Raycast 的髮絲密度**、**Claude 的暖色 editorial**，引擎會從品牌規範裡取出對應的 tokens、聲音、動效約定與招牌手法。

---

## MCP 伺服器：非對稱的一著

ux-skill 提供一個 **Model Context Protocol 伺服器**。執行 `ux-mcp`，引擎就變成一個常駐的 stdio 程序，任何支援 MCP 的主機（Claude Desktop、Cursor、Windsurf 以及通用代理）都可以呼叫它。共 25 個工具：`ux_recommend`、`ux_system_detect`、`ux_lint`、`ux_styles`、`ux_palettes`、`ux_type_pairs`、`ux_components`、`ux_industries`、`ux_motion_presets`、`ux_anti_patterns`、`ux_brands`、`ux_landing_patterns`、`ux_persist_save`、`ux_persist_load`、`ux_stats`、`ux_image_extract`、`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`、`ux_system_build`、`ux_system_import`、`ux_system_enhance`、`ux_system_extend`、`ux_system_export`、`ux_contracts_check`。與斜線命令使用相同的 Python 處理器、相同的資料清單、相同的確定性推薦器。

**為什麼這是非對稱的一著:** 排名前八的 Claude UX 技能(ui-ux-pro-max-skill、open-design、taste-skill、huashu-design、stitch、nothing-design、hallmark、material-3)沒有一個提供 MCP 伺服器。它們都被鎖在 Claude Code 的外掛執行階段裡。ux-skill 則能從任何講 MCP 的主機接入,包括從未聽說過 Claude Code 外掛的代理。

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

把你的用戶端指向 `ux-mcp` 執行檔即可。完整工具文件、JSON 範例,以及面向 Claude Desktop、Cursor、Windsurf 的逐用戶端設定見 [docs/mcp.html](docs/mcp.html) 和 `commands/ux-mcp.md`。

---

## 面向 17 個 IDE 的安裝程式

`uxskill init`(或在 Claude Code 中執行 `/ux-init`)會自動識別你在哪個 IDE,並寫入對應的產出物。同一個 Python 引擎。同一套推薦。各 IDE 之間用不同的「膠水」對接。

| IDE / 工具 | 識別訊號 | 安裝的產出物 |
|---|---|---|
| Claude Code | `.claude/` 或 `CLAUDE.md` | 位於 `.claude-plugin/plugin.json` 的外掛清單 + 全部 18 個命令（以及 7 個別名）+ 全部 5 個子代理 |
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

## 使用案例：具體場景

八個真實場景。挑一個最貼近你處境的,改一下呼叫參數即可。

### 1. 在 Cursor 裡做一個金融科技儀表板

你在 Cursor 上做一個 MENA 新銀行的儀表板。裝好外掛、跑 discovery、跑 recommendation,然後生成儀表板。

```bash
pip install uxskill
uxskill init                                # detects Cursor, writes .cursorrules
uxskill discover                            # 10-field intake
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
> Project type? landing
> Industry? fintech-payments
> Tone? serious, technical, confident
> Must have? dark-mode, AA, mobile-first
> Forbidden? purple-gradients, three-equal-cards
> Reference brands? stripe
> Stack? nextjs-15-app-router
> Region? global
> Success metric? signup conversion

/ux-discover --recommend
> [returns picked style, palette, type pair, motion presets, components, brand exemplars]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer generates the page]

/ux-lint .
> [passes, Stripe brand spec was respected]
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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

三條命令,一張拋光後的介面,每個修復一個原子提交。

### 5. 設計一個 Linear 風格的命令面板

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

生成的元件用的是 Linear 真實的顏色 tokens、字體堆疊、動效約定與髮絲密度，而不是「通用暗色 UI」。

### 6. 用 90 分鐘和利害關係人開一場設計思考工作坊

你有一間會議室,5 個人,90 分鐘。你希望他們帶著行動方案離開,而不是帶著「感覺」。

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

外掛端到端地主持五個階段(探索 → 熱度圖 → 利害關係人地圖 → 解決方案草圖 → 行動方案),計時,每階段都有具體產出。最終輸出是 `.ux/last-workshop.json`，行動方案,而不是只剩「有趣的發現」。

### 7. 發布後寫一份可發表的案例研究

你發了會員錢包。你想要一篇作品集篇章。

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

這份案例研究是已完成、可發布的產出物，不是草稿。純黑白、editorial 字型、可直接上你的作品集。

### 8. 在非 AI 環境裡跑 discovery(只要結構化收件)

你在做一份專案規劃。你還不需要推薦，只需要一份結構化簡報。

```bash
uxskill discover
# 10-field intake, saves to .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

你可以把 JSON 交給團隊,貼到 Notion 文件裡,或者餵給其他 AI 工具。ux-skill 不只是引擎,也是一個結構化收件工具。

### 9. MASTER.md 持久化：把你的設計決策寫進儲存庫

跑完 `/ux-discover`（或 `/ux-discover --recommend`）之後，把選定的風格 + 配色 + 字體 + 動效 + 元件 + 品牌範例 + 護欄儲存為一份可讀的 Markdown 檔案，讓團隊能審查、對比（diff）、納入版本控制。

```bash
python3 -m engine.cli.main persist save --project-root .
```

寫出 `.ux/design-system/MASTER.md`(YAML frontmatter + 正文),並透過 `persist save-page` 為每個生成出的介面寫出 `.ux/design-system/pages/<name>.md`。冪等，相同輸入產出按位元組完全一致的輸出,所以在狀態未變時重跑在 git 裡就是個 no-op。

---

## 與其他方案的對照

簡表如下。逐欄對照詳見 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

| 維度 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| 斜線命令 | **18** | 1 | 19 | 1 | 1 | 多個 | 1 | 1 | 1 |
| 元件 | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| 動效預設 | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 品牌規範 | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 反模式規則 | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 安全的確定性檢查器 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 支援的 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery 關卡 | **10 欄位** | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 | 隱式 |
| `.ux/` 狀態鏈 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| Star 數(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 坦誠評估

- **ui-ux-pro-max** 認知度更大,支援 18 個 IDE,在它的 CSV 上做了類 BM25 的檢索。它沒有元件清單、動效清單、品牌庫或確定性檢查器。
- **open-design** 擁有 19 個 skill + 預覽,但只支援 Claude Code,而且沒有反 slop 層。
- **hallmark** 在精神氣質上最接近(也是反 slop),但它是單個 skill，沒有引擎、沒有清單、沒有可串聯的命令。
- **material-3-skill** 在你專門要 Material Design 3 時極佳。我們不在 MD3 上跟它較勁。

按維度的完整細節見 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 路線圖

接下來（不綁定特定版本）：

- **Figma 樣式**：陰影的效果樣式、格線樣式，以及綁定到欄位變數的文字樣式，寫入線上檔案。
- **元件對應**：把 Figma 元件及其變體對應到程式碼元件及其 props，並在交付過程中一路保留。
- **線上網站匯入器**：讀取一個已發布網站實際算繪出的系統，與檔案匯入器並列。
- **已建立系統的文件頁**：以適合人閱讀的方式呈現它的 token、角色與契約。

其他待辦：

- **`uxskill lint --fix` 安全改寫**：針對可機械修正的發現（button-no-type、img-no-alt 空字串、移除 console-log-leak）。
- 在編輯器內直接顯示 lint 發現的 **VS Code 擴充功能**。
- 涵蓋六個技術堆疊的**依元件輸出程式碼**（Next.js + React、Vue 3 + Nuxt、SvelteKit、Astro、Blade + Alpine、原生 HTML/CSS）。
- **品牌規範市集**：發布與發現社群的品牌規範。
- **自訂反模式規則**：發現與分享各專案在 `data/anti-patterns.local.json` 中定義的規則。
- **`uxskill plan`**：依簡報規劃多頁網站，而不只是單一介面。

---

## 參與貢獻

歡迎 issue 與 PR。三個高槓桿方向:

### 新增一條反模式規則

1. 編輯 `data/anti-patterns.json`，加入一條帶 `id`、`name`、`severity`、`category`、`detection.pattern`、`detection.flags`、`detection.scope`、`evidence_template`、`fix`、`references` 的項目。
2. 在 `tests/linter/` 裡加測試，一份會觸發規則的檔案,一份不會的。
3. 跑 `uxskill lint tests/linter/should-trigger/<rule>.tsx`，確認會被命中。再跑 `tests/linter/should-not-trigger/<rule>.tsx`，確認不會被命中。
4. 開一個 PR。

### 新增一份品牌規範

1. 建立 `data/brands/<slug>.json`,欄位包含 `id`、`name`、`category`、`voice`、`tokens`、`design_principles`、`signature_moves`、`anti-moves`、`references`。
2. 在 `references/brands/<slug>.md` 加入對應散文。
3. 在 `data/brands/_index.json` 登錄。
4. 開一個 PR。規範必須有第一手出處(品牌實際的產品、公開的設計系統,或他們公開發布的 DESIGN.md)。

### 新增一個動效預設

1. 編輯 `data/motion-presets.json`，加入一條帶 `id`、`name`、`category`、`tokens`、`stacks`(framer_motion、gsap、css)、`accessibility.reduced_motion_fallback`、`when_to_use` 的項目。
2. 該預設必須有 reduced-motion 變體。無一例外。
3. 開一個 PR。

### 流程

- 閱讀 [CONTRIBUTING.md](CONTRIBUTING.md) 了解完整流程。
- 閱讀 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
- 新規則與品牌規範會按以下標準複核:第一手出處、不過度擬合到單個專案、資料中不出現 emoji、在適用時的 RTL 安全行為。

---

## 授權、作者、致謝

### 授權

MIT。用它、fork 它、在它之上建構。如果它幫你少出貨了一份 AI slop,請給儲存庫點個 star，這是成本最低的支持方式。

### 作者

**Laith Aljunaidy**：[Dot](https://thedotwallet.com) 的獨立創辦人,Dot 是一個 MENA 優先的會員平台。我打造 ux-skill,是為了讓 AI 生成的前端不再千篇一律。

- LinkedIn:[linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- 電子郵件:laith.aljunaidy.laith@gmail.com
- 儲存庫:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- 官網:[uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI:[pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm:[npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 致謝

- 感謝 Anthropic 團隊提供了 Claude Code,以及讓這一切可分發的 skill / 外掛架構。
- 感謝 Nielsen Norman Group、Laws of UX(lawsofux.com)以及讓 `data/ux-guidelines.json` 言之有據的 UX 研究社群。
- 感謝 `data/brands/` 裡列出的每一個品牌，它們公開的設計系統是品牌規範的事實來源。
- 感謝原始的 v1 貢獻者:那份一次成型的 Claude skill 是 v2 Python 引擎的種子。
- 感謝我們對照的那 8 個熱門 Claude UX 外掛，他們抬高了基準;這是我們的回答。

---

**ux-skill** · **v4.0.0** · 為讓 Claude Code、Cursor、Windsurf 以及其他 AI 程式設計工具產出的前端不再被一眼識別為 AI 生成而打造。

> 給儲存庫點個 star:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · 透過 `pip install uxskill` 或 `npx uxskill init` 安裝 · 在 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) 瀏覽對照
