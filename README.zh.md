[English](README.md) · [العربية](README.ar.md) · [Español](README.es.md) · **中文** · [Français](README.fr.md) · [Deutsch](README.de.md)

# ux-skill — 为 Claude Code、Cursor 及一切 AI 编程工具打造的设计智能引擎

> **AI 编程领域最强的 UX 插件。** 一个由 Python 驱动的推理内核,包含 11 份可查询的 JSON 清单(84 种风格、176 套配色、70 组字体搭配、148 个组件、184 个行业、35 种图表类型、57 个动效预设、112 条 UX 法则、100 条反模式规则、25 个技术栈、110 份品牌规范)、22 个斜杠命令、5 个子代理,以及一个确定性的反 AI-slop 静态检查器。跨 IDE 支持:可装入 Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、Kiro、Cline、Continue、Aider、Zed、JetBrains AI、Pieces、Tabby、Tabnine、CodeWhisperer 以及 Roo Cline。

> **品牌名是 `ux-skill`。** PyPI / npm 上的包名依旧是 `uxskill`。GitHub 仓库地址是 [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)。

**官网:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **与每一个 Claude UX 插件的对比:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-2.0.0--alpha.1-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#面向-17-个-ide-的安装器)
[![Brands](https://img.shields.io/badge/brand_specs-72-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-35-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)

---

## ux-skill 是什么

ux-skill 是一个面向 AI 编程工具的**设计智能引擎**。它以 Python 包的形式运行(`pip install uxskill`),也作为 Claude Code 插件运行,同时提供一个面向 17 个 IDE 的多重安装器。引擎接收一份项目简报(行业、受众、调性、必备项、禁忌项、技术栈、地区),并返回一套完整的推荐设计系统:风格、配色、字体搭配、动效预设、组件、可供研习的品牌范例,以及必须坚守的反模式护栏。该推荐是确定性的——相同输入永远产出相同结果。

这个插件位于你与 AI 编程工具之间。当你让 Claude Code、Cursor 或任何其他 AI 助手"做一个金融科技落地页"时,助手通常会即兴发挥——结果在五秒钟内就能被识别为 AI 生成(紫到蓝的渐变、三张等大的卡片、用 Inter 做超大显示字、测评里出现"John Doe"、默认 300ms 的过渡、居中 hero、CTA 上跳动的箭头)。ux-skill 用**结构化的约束**替代即兴:你跑 `/ux-discover` 抓取简报,跑 `/ux-recommend` 选定系统,跑 `/ux-design` 生成代码,再跑 `/ux-lint` 在提交前验证它通过 100 条确定性反 AI-slop 规则。

这份 README 是权威参考。每一个命令、每一个子代理、每一份数据清单、每一条安装路径、每一份品牌规范、每一类反模式——全都记录在这里。如果你正在挑选 Claude Code 的设计插件,或者在为 Cursor、Windsurf 或 Codex 比较 AI 设计工具,请把这篇从头到尾读一遍,并对照 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 目录

1. [快速安装](#快速安装)
2. [数据对比——与 Top 8 Claude UX 技能的实时比较](#数据对比与-top-8-claude-ux-技能的实时比较)
3. [架构——各部件如何咬合](#架构各部件如何咬合)
4. [22 个斜杠命令——详细参考](#22-个斜杠命令详细参考)
5. [5 个子代理](#5-个子代理)
6. [11 份数据清单](#11-份数据清单)
7. [100 条反 AI-slop 规则——静态检查器](#35-条反-ai-slop-规则静态检查器)
8. [72 份 DESIGN.md 品牌规范——按类别](#72-份-designmd-品牌规范按类别)
9. [面向 17 个 IDE 的安装器](#面向-17-个-ide-的安装器)
10. [使用案例——具体场景](#使用案例具体场景)
11. [与其他方案的对比](#与其他方案的对比)
12. [路线图](#路线图)
13. [参与贡献](#参与贡献)
14. [许可证、作者、致谢](#许可证作者致谢)

---

## 快速安装

三条安装路径。请挑选与你的环境匹配的那条。

### 路径 1 — Claude Code 市场(权威路径)

如果你常驻 Claude Code,请通过插件市场安装:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

这会将全部 22 个斜杠命令与 5 个子代理接入你的 Claude Code 会话。安装完成后,执行 `/ux-init` 以建立项目级别的 `.ux/` 状态目录,并核实 Python 引擎可达。

### 路径 2 — pip(通用路径)

如果你身处 Claude Code 之外(Cursor、Windsurf、CLI、CI),请安装 Python 包:

```bash
pip install uxskill
uxskill init                       # 自动识别 IDE,安装对应的产物
uxskill stats                      # 打印清单计数以验证安装
uxskill lint .                     # 对当前目录运行静态检查器
```

包同时暴露 `ux` 与 `uxskill` 两个 CLI 入口——它们是同一个二进制。

### 路径 3 — npx(无需自行管理 Python)

如果你不想直接管理 Python,npx 封装层会通过 `pipx` 自动拉起:

```bash
npx uxskill init                  # 首次运行时会下载 pipx + uxskill
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### 验证安装

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
#     "anti-patterns": 35,
#     "brands": 72
#   }
# }
```

如果任一计数返回 0,意味着对应的 JSON 文件缺失——请到 [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) 提个 issue。

---

## 数据对比——与 Top 8 Claude UX 技能的实时比较

Star 数最后一次通过 `gh api` 核对的时间是 **2026-05-28**。ux-skill(Laith0003/ux-skill)是最新入场的——我们在认知度上极小,在架构深度上极深。下面这张表是诚实的:哪里我们输,哪里我们赢。

| 插件 | Star 数 | 架构 | 斜杠命令 | 静态检查器(可上 CI) | 品牌规范 | 组件 | 动效预设 | 支持的 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV,单一 skill | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 个 skill + 预览 | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + 研究背书的审美 | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 单份 62 KB SKILL.md + 脚本 | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | 接入 MCP 的 skill 库 | 多个 | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 单一审美 skill | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 反 slop 设计 skill | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 组件 + 审查 | 1 | — | (仅 MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python 引擎 + 11 份清单 + 22 个命令 + 5 个子代理 + CI 检查器** | **22** | **100 条正则规则** | **72** | **148** | **57** | **17** |

### 我们输在哪里

- **认知度。** 他们有数十万颗 star。我们有 14 颗。给我们点个 star——这是成本最低的支持方式。
- **品牌识别度。** ui-ux-pro-max 和 open-design 的领先优势是按月算的,不是按天。
- **营销打磨。** 他们有截图、演示视频和能被搜到的落地页。我们有一份完备的 README 和一张轻量的落地页。

### 我们赢在哪里

- **组件库:** 148 个带解剖结构、状态、所用 token 与动效规范的文档化组件。其他 8 个里没有任何一个发布过组件清单。
- **动效预设:** 57 个开箱即用的栈级条目(Framer Motion、GSAP、CSS),全部带 reduced-motion 兜底。其他几家都不发布动效清单。
- **反模式静态检查器:** 100 条确定性正则规则,能在 CI 中运行,遇 Critical/High 退出非零码。其他几家没有任何确定性检查器。
- **品牌规范:** 72 份真实 DESIGN.md 规范(Apple、Stripe、Linear、Figma、Tesla、BMW、Notion、Spotify、Airbnb、Vercel、Supabase、Cursor、Raycast、Claude,以及其余 58 个)。其他几家没有品牌库。
- **支持 17 个 IDE:** 同一个引擎,IDE 之间用不同的"胶水"对接。
- **22 个斜杠命令:** discovery、生成、审查、lint、polish、修复循环、案例研究、工作坊、文案、动效、a11y、dashboard、conductor——彼此完全打通。

完整的逐列对比详见 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 架构——各部件如何咬合

```
ux-skill (包名: uxskill)
│
├── data/                              大脑——可查询的 JSON 清单
│   ├── styles.json                    84 种设计风格 + when/skip + tokens
│   ├── palettes.json                  176 套配色(明/暗,对比度已核)
│   ├── type-pairs.json                70 组 display × body × mono 三元组
│   ├── components.json                148 个组件(解剖、状态、动效)
│   ├── industries.json                184 条行业规则 + 受众信号
│   ├── chart-types.json               35 种图表(when/skip,编码)
│   ├── tech-stacks.json               25 个技术栈(Next、Astro、SvelteKit、Blade...)
│   ├── ux-guidelines.json             112 条具名 UX 法则(Hick、Fitts、Miller...)
│   ├── motion-presets.json            57 个动效预设(入场、出场、hover...)
│   ├── anti-patterns.json             100 条正则规则(CI 安全的检查器源)
│   └── brands/*.json                  72 份 DESIGN 规范 + _index.json
│
├── engine/                            Python——推理层
│   ├── recommender/                   五路并行检索的合并引擎
│   ├── linter/                        确定性反 slop 扫描器
│   ├── discovery/                     10 字段强制协议
│   ├── generator/                     token + 清单生成器
│   ├── installer/                     面向 17 个 IDE 的多重安装器
│   └── cli/                           `ux` / `uxskill` 入口
│
├── commands/                          22 个 Claude Code 斜杠命令(.md)
│   ├── ux-init.md                     初始化
│   ├── ux-stats.md                    库存快照
│   ├── ux-discover.md                 10 字段录入(关卡)
│   ├── ux-recommend.md                旗舰——五路并行检索
│   ├── ux-lint.md                     确定性检查器
│   ├── ux-design.md                   生成前端代码
│   ├── ux-component.md                生成单个组件
│   ├── ux-system.md                   生成完整设计系统
│   ├── ux-dashboard.md                生成仪表盘界面
│   ├── ux-motion.md                   动效处理 + 审查
│   ├── ux-audit.md                    六镜头设计审查
│   ├── ux-a11y.md                     WCAG 2.1 AA 审查
│   ├── ux-critique.md                 审美评点(3 个亮点、3 个失分、1 步关键招)
│   ├── ux-copy.md                     微文案审查 + 重写
│   ├── ux-fix.md                      以原子提交落地审查结果
│   ├── ux-polish.md                   抛光 + 清除 AI-slop
│   ├── ux-frame.md                    4 字段定调块
│   ├── ux-research.md                 研究计划 + 综合
│   ├── ux-workshop.md                 五阶段设计思维工作坊
│   ├── ux-case-study.md               可发布的 Wfrah 编辑风格案例研究
│   ├── ux-next.md                     工作流指挥(只读)
│   └── ux-expert.md                   咨询入口
│
├── agents/                            5 个子代理(.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 品牌嗓音的微文案
│   ├── research-synthesizer.md        访谈 + 分析 + 竞品
│   └── design-system-architect.md     tokens / 组件 / 基础
│
├── references/                        数据的散文化源文 + 演示页面
│   ├── foundations/                   anti-patterns.md、原则、审美
│   ├── laws/                          UX 法则长文
│   ├── process/                       discovery-protocol.md(关键)
│   ├── styles/                        风格散文(anti-slop.md 等)
│   ├── components/                    组件长文
│   ├── output/                        输出量规
│   └── conditional/                   按技术栈的特定指引
│
├── bin/
│   ├── uxskill.mjs                    npx 封装 -> Python 引擎
│   ├── ux-lint.py                     v2 检查器(优先)
│   └── ux-lint.sh                     v1 兜底(bash + perl-PCRE)
│
└── .ux/                               (按项目生成)
    ├── last-discovery.json            简报快照
    ├── last-recommendation.json       选定的系统
    ├── last-frame.json                定调块
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### 引擎到底是怎么工作的

1. **输入。** 你提供一份简报——可通过 `/ux-discover` 交互式填(10 个字段),也可通过给 `ux recommend` 传 flag 的方式非交互填。
2. **五路并行检索。** 引擎在清单之间并发跑五次查询:
   - **行业 → 推荐风格**(industries.json)
   - **风格 → 配色 + 字体 + 动效的兼容性**(styles.json)
   - **调性 × 必备项 → 配色过滤**(palettes.json)
   - **技术栈 → 组件兼容性 + 动效预设**(tech-stacks.json、motion-presets.json)
   - **禁忌项 + 地区 → 护栏 + 品牌范例候选**(anti-patterns.json、brands/)
3. **合并。** 一个确定性的合并器对候选项排序、化解冲突(例如,"必备暗色模式"会强制配色模式),最终给出唯一的推荐系统。
4. **输出。** 一份 JSON,内含选定的风格、配色、字体搭配、动效 Top 5、组件 Top 12、品牌范例 Top 5,以及全部 100 条反模式护栏的启用状态。外加一段说明,逐项解释为什么这样选。
5. **生成。** 下游命令(`/ux-design`、`/ux-component`、`/ux-system`、`/ux-dashboard`)读取推荐结果,通过子代理生成真实代码。
6. **验证。** `/ux-lint` 用 100 条正则规则再扫一遍生成出的代码。在 CI 中遇 Critical/High 退出非零码。

**Python 思考。HTML 展示。Markdown 串联。**

---

## 22 个斜杠命令——详细参考

每个命令以 `commands/` 下的 `.md` 文件发布,包含 `description`、`allowed-tools`、`triggers`、`when to use`、`when to skip`、`input`、`process`、`output state file`。下文是浓缩版描述;完整源文件才是权威规范。

命令分为五大类:**初始化与库存**、**discovery 与推荐**、**生成**、**审查与验证**、**修复与抛光**,以及**指挥**。

### 初始化与库存

#### `/ux-init` — 给项目做初始化

- **做什么:** 识别你在哪个 IDE(`.claude/`、`.cursor/`、`.windsurf/` 等),安装匹配的产物,核实 Python 引擎可达,打印一份统计快照。
- **何时使用:** 在新项目里首次安装;克隆了使用 ux-skill 的项目之后;`pip install --upgrade uxskill` 之后。
- **何时跳过:** 你已经在这个项目里跑过,而且没有任何变动。
- **调用方式:** `/ux-init`(无参数)或在 CLI 里跑 `uxskill init`。
- **输出:** 各 IDE 对应的产物(详见[面向 17 个 IDE 的安装器](#面向-17-个-ide-的安装器))+ `.ux/` 目录 + 标准输出摘要。
- **下接:** 接下来是 `/ux-discover`。

#### `/ux-stats` — 打印数据库存

- **做什么:** 打印版本号以及 11 份数据清单的条目计数,便于核对你装了什么。
- **何时使用:** 安装后、升级后;以及当 `/ux-recommend` 给出意外结果、你怀疑清单不完整时。
- **何时跳过:** 从不——它是个 50 ms 的只读命令。
- **调用方式:** `/ux-stats` 或 `uxskill stats`。
- **输出:** 标准输出的 JSON(见上方[验证安装](#验证安装))。
- **下接:** 仅用于诊断,不喂任何下游流程。

### discovery 与推荐

#### `/ux-discover` — 强制函数(10 字段录入)

- **做什么:** 每个项目在跑任何生成类命令之前必经的 10 字段强制录入。项目类型、受众、首要目标、调性、必备项、禁忌项、参考品牌、技术栈、地区、成功指标。**杜绝即兴。** 被禁短语("现代"、"干净")会逼着用户讲得具体。
- **何时使用:** 在任何 `/ux-design`、`/ux-component`、`/ux-system` 或 `/ux-dashboard` 之前;以及任何先前简报已经过期时。
- **何时跳过:** 你在修 bug(`/ux-fix`);你只跑一次 lint(`/ux-lint`);简报和上次会话保持不变。
- **调用方式:** `/ux-discover`。插件问,你答。
- **输出:** 写入 `.ux/last-discovery.json`(10 字段简报)。
- **下接:** `/ux-recommend` → 据 discovery 选风格、配色、字体、动效与组件;`/ux-design [补充简报]` → 在推荐结果上生成前端代码;`/ux-component <名称>` → 在 discovery 约束下生成单个组件。

#### `/ux-recommend` — 旗舰五路并行检索引擎

- **做什么:** 在 11 份清单之间跑 Python 引擎的五路并行检索,返回一套合并后的设计系统。行业 → 风格 → 配色 → 字体 → 动效 + 组件 + 品牌范例 + 护栏。
- **何时使用:** 从零起一个新项目;给做疲了的产品做转向;在 `/ux-design` 或 `/ux-component` 之前的预检。
- **何时跳过:** 你已经跑过 `/ux-discover` 并保存了简报——在该流程里 `/ux-recommend` 是自动衔接的;你在修 bug(用 `/ux-fix`);你只需要 lint(用 `/ux-lint`)。
- **调用方式(Claude Code):**
  ```
  /ux-recommend
  ```
  **调用方式(CLI):**
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
- **输出:** 写入 `.ux/last-recommendation.json` —— 选定的风格、选定的配色、选定的字体搭配、动效 Top 5、组件 Top 12、品牌范例 Top 5、100 条反模式护栏的启用状态,以及理据。
- **下接:** `/ux-design [简报]` → 用推荐 token 生成前端代码;`/ux-system` → 由推荐生成完整设计系统;`/ux-component <名称>` → 用推荐风格生成单个组件;`/ux-lint` → 验证生成的代码。

### 生成

#### `/ux-design` — 由简报生成漂亮、反 slop 的界面

- **做什么:** 由 discovery 简报 + 推荐生成完整的生产级前端产物(落地页、营销站、应用外壳)。在反 slop 与 arsenal 参考的创意指引下,派遣 `frontend-engineer`。
- **何时使用:** "设计一个"、"给我做一个"、"生成一个落地页"、"做一个仪表盘"、"做一个组件"——任何形式自由的视觉交付请求。
- **何时跳过:** 你要的是评审而不是构建(用 `/ux-audit` 或 `/ux-critique`);你只想要一个组件(用 `/ux-component`);后端或基础设施工作。
- **调用方式:** `/ux-design 生成一个面向 MENA 新银行的金融科技落地页,暖色 editorial 调性,暗色 AA,不要紫色渐变`。
- **输出:** 生成的代码(HTML / Blade / JSX / Vue / Astro),以及 `.ux/last-design.json`。
- **下接:** `/ux-lint` → 验护栏;`/ux-polish` → 抛光;`/ux-a11y` → 可访问性审查;`/ux-copy` → 微文案审查;`/ux-fix` → 以原子提交落地。

#### `/ux-component` — 生成单个组件

- **做什么:** 由一份规格生成单个生产级组件(按钮、模态、导航栏、侧栏、卡片、表格、表单、图表)。四种交互状态齐备,可访问,贴合品牌。先在 `.ux/last-recommendation.json` 里查该组件,再回落到直接查清单。
- **何时使用:** 任何单元素请求——"做一个按钮"、"做一张定价卡"、"做一个模态"、"加一个导航栏"、"设计一个侧栏"、"我需要一张数据表"、"做一个表单"、"做一个图表组件"。
- **何时跳过:** 整页或多段式界面(用 `/ux-design`);后端或基础设施。
- **调用方式:** `/ux-component pricing-card-trio --brief="金融科技,暗色,等宽数字"`。
- **输出:** 生成的组件代码,以及 `.ux/last-component.json`。
- **下接:** `/ux-lint` → 验证;`/ux-polish` → 抛光。

#### `/ux-system` — 生成一套完整的起步设计系统

- **做什么:** 给还没有设计系统的项目提议一整套起步系统——tokens(颜色、字体、间距、动效、圆角、阴影)、基础文档、组件契约、暗色模式映射、主题切换器。派遣 `design-system-architect`。
- **何时使用:** "我们没有设计系统"、"给我们搭一套"、"提议一份 tokens"、"我们的主题该长什么样"、"把 DS 搭起来"。
- **何时跳过:** 项目已经有设计系统——直接用 `/ux-component` 基于现有系统构建即可;后端或基础设施。
- **调用方式:** `/ux-system`(如果还没存档,先跑 discovery)。
- **输出:** `tokens.json`、`foundations.md`、`components/*.md` 契约,可选输出 Tailwind / vanilla / SCSS。写入 `.ux/last-system.json` 以供后续衔接。
- **下接:** `/ux-component` → 基于新系统构建;`/ux-design` → 用新 tokens 生成界面。

#### `/ux-dashboard` — 专门的仪表盘生成

- **做什么:** 以数据密度纪律构建的仪表盘——bento 布局、等宽表格数字、迷你折线模式、避免滥用卡片、语义化状态色、动效节制。它不是把图表贴上去的营销落地页。
- **何时使用:** "做一个仪表盘"、"设计 admin 面板"、"做一个指标页"、"操作员控制台"、"分析视图"、"KPI 板"、"监控页"。
- **何时跳过:** 带统计数字的营销落地页(用 `/ux-design`);只要一个 widget(用 `/ux-component`);后端或基础设施。
- **调用方式:** `/ux-dashboard`。
- **输出:** 生成的仪表盘代码 + `.ux/last-dashboard.json`。
- **下接:** `/ux-lint`、`/ux-audit`、`/ux-a11y`。

#### `/ux-motion` — 动效处理

- **做什么:** 生成界面的动效层——时长、缓动、编排、reduced-motion 兜底、性能纪律。也对现有动效按五个维度做审查(时长、缓动、含义、reduced-motion、性能)。
- **何时使用:** "检查一下动效"、"动画做得对不对"、"修一下动效"、"复核动画"、"动效审查"、"对动效做性能扫"。
- **何时跳过:** 界面没有动效(用 `/ux-audit` 或 `/ux-polish`);后端或基础设施。
- **调用方式:** `/ux-motion path/to/component.tsx`(审查模式)或 `/ux-motion --generate hero-entry`(生成模式)。
- **输出:** 更新后的代码(生成模式)或 `.ux/last-motion.json` 报告(审查模式)。
- **下接:** `/ux-fix` → 落地动效结论;`/ux-polish` → 抛光。

### 审查与验证

#### `/ux-lint` — 基于正则的确定性检查器(无 LLM,CI 安全)

- **做什么:** 对你的代码跑 100 条正则规则。无 LLM 调用。CI 中遇 Critical / High 退出非零码。源文件:`data/anti-patterns.json`。规则覆盖颜色(6)、字体(3)、布局(5)、动效(3)、内容(5)、a11y(6)、质量(6)、视觉(1)。
- **何时使用:** 预提交钩子;CI 关卡;在花 `/ux-audit` 成本之前对大代码库做的快速首轮;在 `/ux-design` 或 `/ux-component` 之后用于验证生成。
- **何时跳过:** 你想要修复循环(检查器只报告、不修改——请接 `/ux-polish --fix` 或 `/ux-fix`);你想要审美判断(用 `/ux-critique`)。
- **调用方式(slash):** `/ux-lint src/`。
- **调用方式(CLI):** `uxskill lint .` 或 `python3 bin/ux-lint.py .` 或 `bash bin/ux-lint.sh --ci --fail-on high`。
- **调用方式(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **输出:** 标准输出中的命中(位置、规则 id、严重级别、证据)。无命中时退出码 0,设了 `--fail-on high` 且命中 Critical/High 时退出非零。
- **下接:** `/ux-polish --fix` → 同类模式的 LLM 版对手;`/ux-fix` → 按严重级别落地为提交;`/ux-audit` → 完整的六镜头推理回合;`/ux-next` → 让指挥来决定。

#### `/ux-audit` — 六镜头设计审查

- **做什么:** 一次结构化、带立场的评审,从六个镜头(清晰度、层级、可访问性、嗓音、动效、审美)出发,产出按严重级别打标的发现。Polaris 风格的报告。先读 `.ux/last-frame.json`——受众与结果决定每条发现的严重级别。
- **何时使用:** 界面已存在,你需要一份能站得住脚的批评。"审一下"、"看看这版 UX"、"做得好不好"、"哪里坏了"、"狠狠拆一下"。
- **何时跳过:** 界面尚未存在(用 `/ux-design`);用户只要一个镜头(用对应专项命令:`/ux-a11y`、`/ux-copy`、`/ux-motion`、`/ux-polish`);用户想要审美观点(用 `/ux-critique`);后端或基础设施。
- **调用方式:** `/ux-audit https://example.com/pricing` 或 `/ux-audit src/components/Pricing.tsx`。
- **输出:** 写入 `.ux/last-audit.json` —— `findings` 数组,字段为 `{lens, severity, title, principle, evidence, fix}`,以及 `severity_counts`、`dominant_lens`、`strategic_moves`。
- **下接:** `/ux-fix` → 落地;`/ux-polish` → 抛光;`/ux-design` → 若需结构性重设计。

#### `/ux-a11y` — WCAG 2.1 AA 审查 + 基本礼貌检查

- **做什么:** 一次结构化的 WCAG 2.1 AA 审查,外加那些自动工具能放行、但仍会伤害真实用户的"基本礼貌"检查(可见焦点、错误具体性、动效偏好、键盘陷阱、颜色依赖)。
- **何时使用:** 发布前可访问性关卡;重新设计之后;"做一下可访问性检查"、"WCAG 审查"、"这个可访问吗"、"a11y 复核"、"读屏测试"、"键盘导航检查"。
- **何时跳过:** 不面向用户;后端或基础设施;还在草图阶段的工作。
- **调用方式:** `/ux-a11y https://example.com`(优先用线上 URL——自动工具和键盘测试只能在线上跑)。
- **输出:** 写入 `.ux/last-a11y.json` —— `findings` 数组,字段为 `{wcag_sc, sc_name, severity, title, evidence, fix, category}`、`beyond_wcag` 数组、`severity_counts`。
- **下接:** `/ux-fix` → 落地为提交;`/ux-copy` → 在一次文案回合中顺手修 alt 文本和表单错误串接。

#### `/ux-critique` — 审美评点(3 个亮点、3 个失分、1 步关键招)

- **做什么:** 一个设计师的态度——不是结构化审查,不是严重级别打分,只是一段紧致、有立场的看法,点名什么在起作用、什么没起作用,以及那一步能改变最多的关键招。
- **何时使用:** "你怎么看"、"这个好吗"、"评点一下"、"实话说"、"调性对不对"、"这像我们吗"、"该不该发"。
- **何时跳过:** 用户明确要的是结构化审查(用 `/ux-audit`);后端或基础设施。
- **调用方式:** `/ux-critique https://example.com`。
- **输出:** 写入 `.ux/last-critique.json` —— 3 个亮点、3 个失分、1 步关键招,外加散文。
- **下接:** 如果评点建议重设计就接 `/ux-design`;如果建议收紧就接 `/ux-polish`。

#### `/ux-copy` — 微文案审查 + 重写

- **做什么:** 用嗓音量规评估每一句可见文案,产出 before/after 重写。专抓:"表单存在错误"(笼统)、"John Doe"(占位符)、AI 式欢欣鼓舞的庆祝话术、笼统的 CTA、空荡荡的空状态、毫无用处的错误提示。
- **何时使用:** 结构对了但文案弱。"复核文案"、"修微文案"、"错误提示糟糕"、"重写这个"、"收紧文案"、"按钮太笼统"、"空状态死气沉沉"。
- **何时跳过:** 布局问题(用 `/ux-audit` 或 `/ux-polish`);可访问性驱动的文案问题如 alt 文本(用 `/ux-a11y`);后端或基础设施。
- **调用方式:** `/ux-copy src/views/checkout.blade.php`。
- **输出:** 写入 `.ux/last-copy.json` —— `strings` 数组,字段为 `{location, severity, before, after, notes}`,以及量规与需翻译的语言。
- **下接:** `/ux-fix` → 落地重写;`/ux-a11y` → 在文案改动后再复核。

### 修复与抛光

#### `/ux-fix` — 以原子提交落地审查结果

- **做什么:** 从 `.ux/` 读取最近的报告(audit、copy、a11y、motion 或 polish),校验工作树,经由对应子代理把发现以原子提交的形式落地。落地后会重跑触发命令再核验。
- **何时使用:** 跑完一个审查类命令并复盘了发现之后。"修一下这些发现"、"把修复落地"、"跑修复循环"、"打补丁"、"按建议改"、"去修"。
- **何时跳过:** `.ux/` 里没有先前的报告;工作树是脏的且用户尚未同意 stash/commit;修复需要设计判断而不是机械落地(请改用 `/ux-design` 重设计)。
- **调用方式:** `/ux-fix`(自动识别要修哪份报告)或 `/ux-fix --from=last-a11y.json`。
- **输出:** 每条发现一个原子提交。重跑触发命令并更新 `.ux/last-*.json`。打印一段摘要。
- **下接:** `/ux-next` → 由指挥挑下一步。

#### `/ux-polish` — 抛光 + 清除 AI-slop

- **做什么:** 间距节奏、层级锐化、AI-slop 探测、token 一致性。`/ux-lint` 的 LLM 版对手——审美判断由它代你执行。
- **何时使用:** 结构对了但执行松了。"抛个光"、"收紧"、"把 AI-slop 清掉"、"做得高级一点"、"让它不那么像 AI"、"间距感觉不对"、"看上去太通用"、"缺点品位"。
- **何时跳过:** 界面缺核心功能(先修那个);需要重设计而不是抛光(用 `/ux-design`);文案问题(用 `/ux-copy`);动效问题(用 `/ux-motion`);a11y 问题(用 `/ux-a11y`)。
- **调用方式:** `/ux-polish src/components/Hero.tsx`。
- **输出:** 更新后的代码 + `.ux/last-polish.json` 描述改动。
- **下接:** `/ux-lint` → 验证抛光稳了;`/ux-a11y` → 再做一次可访问性复核。

### discovery 与叙事

#### `/ux-frame` — 4 字段定调块

- **做什么:** 把"为谁、目标、假设、成功信号"打进一个结构化的定调块。不做设计——只是把一个含糊请求转成可工作简报的四字段录入。比 `/ux-discover` 更轻(4 字段 vs 10 字段)。
- **何时使用:** 任何项目、冲刺或一次性任务的开端;对话偏离主题时的中途收束。"框一下"、"简报是什么"、"立项"、"定调"。
- **何时跳过:** 已经框过(检查 `.ux/last-frame.json`);没有定调影响的一次性组件构建;后端或基础设施。
- **调用方式:** `/ux-frame "为 Bashiti MENA 试点做的会员钱包"`。
- **输出:** 写入 `.ux/last-frame.json` —— `{audience, outcome, hypothesis, success_signal}`。
- **下接:** `/ux-discover` → 把框扩成 10 字段简报;`/ux-design` → 用框作锚点生成。

#### `/ux-research` — 研究计划 + 综合

- **做什么:** 计划模式:写访谈脚本、问卷、招募筛选器。综合模式(`--synthesize`):把访谈、分析、竞品站点、A/B 结果、客服工单消化为建议。派遣 `research-synthesizer`。
- **何时使用:** "计划一次研究"、"我需要访谈题"、"设计一份问卷"、"如何招募用户"、"用户测试计划"、"日记研究"、"偏好测试"、"fake door"、"smoke test"、"把我的访谈笔记综合一下"。
- **何时跳过:** 答案已有高置信度;低风险且可逆的决策;后端或基础设施。
- **调用方式:** `/ux-research --plan "MENA 会员钱包采纳率"` 或 `/ux-research --synthesize interviews/*.md`。
- **输出:** 写入 `.ux/last-research.json` —— 研究计划,或综合后的主题 + 证据 + 建议。
- **下接:** `/ux-frame` → 把结论纳入定调;`/ux-design` → 据结论生成;`/ux-workshop` → 以研究为输入开工作坊。

#### `/ux-workshop` — 五阶段设计思维工作坊

- **做什么:** 端到端主持一场 discovery / 设计思维工作坊。五个顺序阶段(探索 → 热度图 → 干系人地图 → 解决方案草图 → 行动方案)。计时;每阶段都有具体产出物。结束于一个决定,而不是"有趣的发现"。
- **何时使用:** 真问题、真参与者、真时间预算。"开一场工作坊"、"主持一次 discovery"、"来一次设计思维"、"我有干系人一小时,该干啥"、"项目启动"。
- **何时跳过:** 简报已经清晰且收敛;单人头脑风暴(用 `/ux-design` 或 `/ux-frame`);团队正在执行中,不在 discovery。
- **调用方式:** `/ux-workshop "会员钱包转向" --participants="2 名 PM、1 名设计师、1 名工程 lead、1 名客户代表" --minutes=90`。
- **输出:** 写入 `.ux/last-workshop.json` —— 行动方案 + 各阶段产出物。
- **下接:** `/ux-design` → 执行行动方案;`/ux-research` → 补工作坊暴露的缺口;`/ux-case-study` → 把过程发表。

#### `/ux-case-study` — 可发布的案例研究(Wfrah 编辑格式)

- **做什么:** 以纯黑白编辑格式生成项目案例研究——Wfrah 字型、发丝分隔线、带序号的 (A)–(G) 段落码、双语兼容布局。是一份文档,不是营销小册子。从 `.ux/last-frame.json`、`.ux/last-workshop.json`、`.ux/last-research.json`、`.ux/last-design.json`、`.ux/last-a11y.json`、`.ux/last-polish.json`、`.ux/last-recommendation.json`、`.ux/last-discovery.json` 读取。
- **何时使用:** 发布后;经历一个明确里程碑后。"写一份案例研究"、"把这个项目做成案例"、"做收尾文档"、"把这工作发出来"、"作品集篇"。
- **何时跳过:** 项目数据不足以填满 (A)–(G);用户想要的是营销落地页而非案例研究(用 `/ux-design`)。
- **调用方式:** `/ux-case-study --format=html --slug=bashiti-loyalty`。
- **输出:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`。
- **下接:** 终端命令——通常是项目的句号。

### 指挥

#### `/ux-next` — 工作流指挥(只读)

- **做什么:** 读取每个 `.ux/last-*.json`,指认下一步杠杆最大的命令。它是指挥,不是建造者。只读。
- **何时使用:** 在命令之间。"接下来该做什么"、"下一步是什么"、"替我决定"、"从这里往哪走"。
- **何时跳过:** `.ux/` 里没有先前报告;你心里已有具体的下一条命令。
- **调用方式:** `/ux-next`(无参数)或 `/ux-next --focus=a11y`。
- **输出:** 标准输出——建议的下一条命令 + 理由。
- **下接:** 它挑哪条就接哪条。

#### `/ux-expert` — 咨询入口

- **做什么:** 在用户索取真人 UX 专家时,展示插件作者的联系方式。简短、直接、无营销话术。
- **何时使用:** "谁做的这个"、"我需要个 UX 专家"、"你做咨询吗"、"能雇个人帮我吗"、"这插件背后有人吗"。
- **何时跳过:** 用户问的是插件功能,不是咨询。
- **调用方式:** `/ux-expert`。
- **输出:** 一张含 LinkedIn / 邮箱 / 仓库的简短联系卡。

### 命令串联图

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4 字段定调块
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10 字段录入(强制关卡)
                  └────────────┬─────────┘
                               │ 写入 .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  五路并行 -> 合并系统
                  └────────────┬─────────┘
                               │ 写入 .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ 写入 .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ 写入 .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  把发现落地为提交
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  可发布产物
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  指挥——只读
                  │  /ux-expert          │  咨询入口
                  └──────────────────────┘
```

---

## 5 个子代理

子代理是由命令派遣的角色化生成器。它们从不独立运行——由 `/ux-design`、`/ux-component`、`/ux-system`、`/ux-fix`、`/ux-research` 等命令调起。每个代理都有清晰的职责边界:它们**不**决定简报,只针对简报执行。

### `frontend-engineer`

- **职责:** 生产级前端代码(React、Next.js、Vue、Blade+Alpine、原生 HTML、Astro),并保持反 AI-slop 纪律。
- **派遣者:** `/ux-design`、`/ux-component`、`/ux-dashboard`、`/ux-fix`。
- **输入:** 简报 + 创意指引 + tokens(来自 `.ux/last-recommendation.json`)。
- **输出:** 与通用 AI 输出可区分的可运行代码。不出现紫色渐变、不居中 hero、不三张等大卡片、不用 Inter 当展示字、不出现"John Doe"、不放 emoji、不留 300ms 的默认值。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `motion-engineer`

- **职责:** 生产前端代码中的动效——Framer Motion、GSAP、CSS 动画。时长、缓动、编排、reduced-motion 兜底、性能纪律。
- **派遣者:** `/ux-design`、`/ux-motion --fix`、`/ux-component`。
- **输入:** 动效简报 + tokens + 来自 `data/motion-presets.json` 的 57 个预设。
- **输出:** 配得上自己位置的动效。永远包裹在 `prefers-reduced-motion` 兜底中。永远拿 Core Web Vitals 测一遍。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `copy-writer`

- **职责:** 真正会发布的文案——错误消息、空状态、CTA、loading 状态、成功消息、toast、辅助文字、表单标签、按钮文字。
- **派遣者:** `/ux-copy --fix`、`/ux-design`、`/ux-frame`、`/ux-component`。
- **输入:** 嗓音档案(命名或粘贴) + 界面的文案。
- **输出:** 在界面各个状态间一致应用的生产级微文案,让产品听起来像一个产品,不像十个。禁忌:"表单存在错误"、"John Doe"、AI 式欢欣鼓舞的庆祝话术、笼统 CTA、空荡荡的空状态。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `research-synthesizer`

- **职责:** 把研究输入(访谈、分析、竞品站点、A/B 结果、客服工单)消化为可执行的设计建议。
- **派遣者:** `/ux-research`、`/ux-workshop`、`/ux-frame`。
- **输入:** 原始研究材料——访谈记录、导出文件、竞品 URL、客服聚类。
- **输出:** 主题、证据、建议。不替设计师设计答案——而是把可供设计的底料交给设计师。
- **工具:** `Read, Write, WebFetch, Bash, Glob, Grep`。

### `design-system-architect`

- **职责:** 完整的设计系统——tokens(颜色、字体、间距、动效、圆角、阴影)、基础文档、组件契约、暗色模式映射、主题化层。
- **派遣者:** `/ux-system`,以及在不存在系统时被 `/ux-component` 调用。
- **输入:** 品牌简报 + `.ux/last-recommendation.json`(风格 + 配色 + 字体搭配 + 动效预设)。
- **输出:** 一套连贯、立场鲜明、可上生产的系统,让下游代理无需重新决定根基就能构建。tokens JSON、基础 MD、组件契约、暗色映射。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### 子代理派遣协议

当一个命令派遣子代理时,它会传入:

1. 简报 / 推荐(从 `.ux/` 加载)。
2. 与之相关的清单切片(例如 `frontend-engineer` 拿到选定的风格 + 配色 + 组件;`motion-engineer` 拿到选定的动效预设)。
3. 100 条反模式护栏(始终启用)。
4. 一个成功判据(产物必须做到什么)。

子代理返回:

1. 产物(代码、文档、系统)。
2. 一段理据(为什么这样选)。
3. 对照护栏的自检(他们验证了哪些规则)。

调用方命令随后会自动跑 `/ux-lint`,通过之后才宣告完成。

---

## 11 份数据清单

数据层就是大脑。每个命令都从中读取;引擎在其间合并;静态检查器对其扫描。所有文件都在 `data/` 下,条目用 `{_meta, entries}` 包装以做 schema 版本管理。

### `styles.json` — 84 种设计风格

| 字段 | 描述 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`、`name`、`category`、`philosophy`、`when_to_use`、`when_to_skip`、`tokens`、`references`、`compatible_palettes`、`compatible_type_pairs`、`compatible_motion`、`compatible_industries`、`taste_score` |
| `categories` | Minimalist / Swiss、Brutalist、Editorial、Glassmorphism、Neumorphism、Bento、Skeuomorphic、Industrial、Maximalist、AI-Futurist、MENA-modern、Vaporwave 等 |
| `sample entry` | `swiss-international` —— "网格即法律。字体承担重活。装饰即失败。" |

由 `/ux-recommend`、`/ux-system`、`/ux-design` 使用。Schema:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `palettes.json` — 176 套配色

| 字段 | 描述 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`、`name`、`mode`(明/暗)、`tone`、`colors`(canvas、surface、ink、body、muted、primary、primary_active、hairline、success、warning、danger、accent)、`wcag_contrast_audit`、`compatible_industries` |
| `tones` | warm、editorial、magazine、clinical、playful、brutalist、monochrome、jewel-tone、MENA-warm、dev-tools-dark 等 |
| `sample entry` | `claude-warm-editorial` —— 明色,warm/editorial/magazine,canvas #faf9f5,primary #cc785c |

由 `/ux-recommend`、`/ux-system` 使用。对比度按 AA / AAA 验证。Schema:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `type-pairs.json` — 70 组字体搭配

| 字段 | 描述 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`、`name`、`display`(family + weights + source + license + URL)、`body`、`mono`、`compatible_styles`、`taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` —— Cormorant Garamond × Inter × JetBrains Mono |

所有字族都带许可证 + 源 URL。由 `/ux-recommend`、`/ux-system` 使用。

### `components.json` — 148 个组件

| 字段 | 描述 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`、`name`、`category`、`purpose`、`anatomy`、`states`、`tokens_used`、`motion`、`accessibility`、`compatible_styles`、`compatible_industries`、`code_skeleton` |
| `categories` | Navigation、Forms、Data Display、Feedback、Overlays、Layout、Content、Marketing、E-commerce、Auth、Dashboard、Charts、Empty States、Loading States、Error States |
| `sample entry` | `mega-nav-product-grid` —— Mega Navigation、Product Grid —— 6 段解剖、4 个状态 |

这是我们最深的护城河。其他 Claude UX 插件没有发布过结构化的组件清单。

### `industries.json` — 184 条行业规则

| 字段 | 描述 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`、`name`、`category`、`characteristics`、`audience_signals`、`recommended_styles`、`recommended_palettes`、`recommended_type_pairs`、`recommended_motion`、`regulatory_notes`、`regional_notes` |
| `categories` | Financial Services、Healthcare、Education、E-commerce、SaaS B2B、SaaS B2C、Developer Tools、Media、Gaming、Travel、Real Estate、MENA-specific 等 |
| `sample entry` | `fintech-neobank` —— 高信任、监管披露、余额/交易为主 UI、日活的移动优先 |

由 `/ux-recommend` 用作首条并行检索轴。

### `chart-types.json` — 35 种图表

| 字段 | 描述 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`category`、`when_to_use`、`when_to_skip`、`encoding`、`accessibility`、`data_shape`、`compatible_styles` |
| `categories` | Comparison、Time Series、Distribution、Composition、Relationship、Flow、Geographic |
| `sample entry` | `bar-vertical` —— 比较 4–15 个离散类别。x 轴位置映射类别;高度映射数值。 |

由 `/ux-dashboard`、`/ux-component`(图表实例)使用。

### `tech-stacks.json` — 25 个技术栈

| 字段 | 描述 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`、`name`、`category`、`tier`、`languages`、`ssr`、`rsc`、`compatible_styling`、`scaffold_command`、`compatible_motion`、`gotchas` |
| `tiers` | production、prerelease、experimental |
| `sample entry` | `nextjs-15-app-router` —— Next.js 15(App Router),TS/JS,SSR,RSC,兼容 Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

其他技术栈包括 Astro、SvelteKit、Remix、Nuxt 3、Solid Start、Qwik、Blade+Alpine、Hotwire、Phoenix LiveView、Hydrogen 2025。

### `ux-guidelines.json` — 112 条具名 UX 法则

| 字段 | 描述 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`、`name`、`category`、`source`、`principle`、`application`、`examples`、`caveats`、`related_laws` |
| `categories` | Decision Cost、Attention、Memory、Motor Control、Visual Perception、Social、Emotional、Form、Error Handling、Onboarding、Empty State 等 |
| `sample entry` | `hicks-law` —— 决策时间随选项数量呈对数增长 |

由 `/ux-audit`(六镜头打分)与 `/ux-critique`(审美锚)使用。

### `motion-presets.json` — 57 个动效预设

| 字段 | 描述 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`、`name`、`category`、`tokens`(duration_ms、easing、transform_from/to、opacity_from/to)、`stacks`(framer_motion、gsap、css)、`accessibility`(reduced-motion 兜底)、`when_to_use` |
| `categories` | Entry、Exit、Hover、Focus、Tap、Loading、Empty、Success、Error、Scroll-linked |
| `sample entry` | `fade-up-12px` —— 360ms,`cubic-bezier(0.16, 1, 0.3, 1)`,translateY(12px) → 0,opacity 0 → 1 |

每个预设都有一个 reduced-motion 变体。Framer Motion、GSAP 和纯 CSS 都提供开箱可用的代码。

### `anti-patterns.json` — 100 条正则规则

| 字段 | 描述 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`severity`(high/medium/low)、`category`、`detection`(type、pattern、flags、scope)、`evidence_template`、`fix`、`references` |
| `categories` | A11y(6)、Color(6)、Content(5)、Layout(5)、Motion(3)、Quality(6)、Typography(3)、Visual(1) |

完整规则清单见[100 条反 AI-slop 规则](#35-条反-ai-slop-规则静态检查器)。

### `brands/*.json` — 110 份品牌规范

| 字段 | 描述 |
|---|---|
| `entries` | 72(再加一份 `_index.json` 列出全部) |
| `keys per entry` | `id`、`name`、`category`、`voice`、`tokens`(color、type、motion)、`design_principles`、`signature_moves`、`anti-moves`、`references` |
| `categories` | Developer Tools(24)、Consumer / Lifestyle / Retail(11)、AI / ML Platform(9)、Productivity / Collaboration(8)、Automotive(8)、Fintech / Crypto(7)、Editorial / Media(5) |

完整名单见[72 份 DESIGN.md 品牌规范](#72-份-designmd-品牌规范按类别)。

---

## 100 条反 AI-slop 规则——静态检查器

ux-skill 提供一个基于正则的确定性检查器。**无 LLM。** **无 API。** **无网络。** 在典型 Next.js 应用上 CI 中 ~200ms 跑完。设置 `--fail-on high` 时,遇 Critical / High 退出非零码。

规则来自 `data/anti-patterns.json`(首选 v2),回退源为 `references/foundations/anti-patterns.md`(v1 bash)。发布两个二进制:`bin/ux-lint.py`(Python,快、可扩展)与 `bin/ux-lint.sh`(Bash + perl-PCRE,用于无 Python 的环境)。

### 按类别的规则

#### 字体(3 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| high | `inter-as-display` | 把 Inter 当展示字使用 |
| medium | `hero-text-arbitrary-90px` | hero 区任意大字号 |
| low | `font-system-only` | 只用系统字体栈,未选定字体 |

#### 颜色(6 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| high | `purple-to-blue-gradient` | AI 默认的紫到蓝渐变 |
| high | `dark-text-on-dark-card` | 卡片上低对比度文字 |
| medium | `gradient-text-rainbow` | 多停的彩虹文字渐变 |
| medium | `card-glow-purple-shadow` | 卡片上的紫色 glow 阴影 |
| medium | `gradient-mesh-purple-pink` | hero 紫粉网格渐变 |
| low | `tailwind-color-named-vague` | 命名的 Tailwind 颜色没有语义 token |

#### 布局(5 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| high | `three-equal-card-grid` | 三张等大并排卡片 |
| medium | `centered-everything-hero` | 一切居中的 hero |
| medium | `avatar-stack-overlapping` | 通用的相互重叠头像栈 |
| low | `pill-rounded-full-everywhere` | `rounded-full` 用在所有东西上 |
| low | `nav-equal-hamburger-desktop` | 桌面端用汉堡菜单 |

#### 内容(5 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| high | `lorem-ipsum-leak` | 出货代码里有 Lorem ipsum |
| high | `emoji-in-ui` | 用 emoji 当 UI 元素 |
| high | `icon-emoji-stamp` | 用 emoji 当图标章 |
| high | `testimonial-fake-five-stars` | 写死的五星好评 |
| medium | `fake-name-john-doe` | 占位人名 |

#### 动效(3 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | CTA 上跳动的箭头 |
| low | `timing-300ms-default` | 过渡默认值 300ms |
| low | `cubic-bezier-material-only` | 到处都是 Material 默认缓动 |

#### A11y(6 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| high | `inline-svg-no-aria` | SVG 缺 aria-label 或 aria-hidden |
| high | `img-no-alt` | 图片缺 alt 属性 |
| high | `link-onclick-no-href` | 锚点有 onClick 但没有 href |
| medium | `button-no-type` | 按钮缺 type 属性 |
| medium | `heading-skip-h1-h3` | 跳级标题 |
| medium | `infinite-scroll-no-pagination` | 无键盘兜底的无限滚动 |

#### 质量(6 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| high | `console-log-leak` | 组件代码里残留 `console.log` |
| medium | `inline-style-attribute` | 内联 style 属性 |
| medium | `any-type-leak` | TypeScript `any` 类型 |
| medium | `arbitrary-z-index-9999` | 偷懒的 z-index 数值 |
| low | `shadcn-default-everywhere` | shadcn 默认 token 一字未改 |
| low | `todo-fixme-comment` | 出货代码里有 TODO 或 FIXME |

#### 视觉(1 条)

| 严重级别 | 规则 ID | 名称 |
|---|---|---|
| low | `blur-bg-only-decoration` | 没有玻璃表面的 backdrop blur |

### 检查器用法

**一次性扫描:**

```bash
uxskill lint .
# 或
python3 bin/ux-lint.py src/
# 或
bash bin/ux-lint.sh src/
```

**CI 关卡(GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**预提交钩子:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**输出示例:**

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

## 72 份 DESIGN.md 品牌规范——按类别

真实的品牌。真实的设计语言。真实的 DESIGN.md 规范——不是通用配色。告诉插件"按 Stripe 的风格做个落地页",它会读取真实的品牌词汇表:嗓音量规、颜色 tokens、动效约定、签名手法、反向手法。

每个品牌都以一份结构化 JSON(`data/brands/<slug>.json`)外加一份散文参考(`references/brands/<slug>.md`)的形式发布。

### Developer Tools(24)

ClickHouse、Composio、Cursor、Expo、Framer、HashiCorp、IBM、Lovable、Mintlify、MongoDB、Ollama、OpenCode、PostHog、Raycast、Replicate、Resend、Sanity、Sentry、Slack、Supabase、Superhuman、Vercel、Warp、Webflow

### Consumer / Lifestyle / Retail(11)

Airbnb、Apple、HP、Meta、Nike、Pinterest、PlayStation、Shopify、Spotify、Starbucks、Uber

### AI / ML Platform(9)

Claude、Cohere、ElevenLabs、MiniMax、Mistral AI、Runway、Together AI、VoltAgent、xAI

### Productivity / Collaboration(8)

Airtable、Cal.com、Figma、Intercom、Linear、Miro、Notion、Zapier

### Automotive(8)

BMW、BMW M、Bugatti、Ferrari、Lamborghini、Renault、SpaceX、Tesla

### Fintech / Crypto(7)

Binance、Coinbase、Kraken、Mastercard、Revolut、Stripe、Wise

### Editorial / Media(5)

Clay、NVIDIA、The Verge、Vodafone、Wired

### 为什么这件事很重要

另外 8 个热门 Claude UX 插件生成的是"现代极简"或"干净仪表盘"——同一种默认美学的变体。ux-skill 让你能要**Linear 的清晰**、**Stripe 的严肃**、**Apple 的克制**、**Tesla 的整块感**、**Notion 的亲和**、**Cursor 的渐变纪律**、**Raycast 的发丝密度**、**Claude 的暖色 editorial**——引擎会从品牌规范里取出对应的 tokens、嗓音、动效约定与签名手法。

---

## 面向 17 个 IDE 的安装器

`uxskill init`(或在 Claude Code 中执行 `/ux-init`)会自动识别你在哪个 IDE,并写入对应的产物。同一个 Python 引擎。同一套推荐。各 IDE 之间用不同的"胶水"对接。

| IDE / 工具 | 识别信号 | 安装的产物 |
|---|---|---|
| Claude Code | `.claude/` 或 `CLAUDE.md` | 在 `.claude-plugin/plugin.json` 的插件清单 + 全部 22 个命令 + 全部 5 个子代理 |
| Cursor | `.cursor/` 或 `.cursorrules` | 指向引擎的 `.cursorrules` 提示头 |
| Windsurf | `.windsurf/` 或 `.windsurfrules` | 同样提示头的 `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` 或 `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` 补丁 |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` 或 `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

在每个 IDE 里,从终端跑 `uxskill recommend` / `uxskill lint` / `uxskill stats` 都一样可用。Python 引擎是事实来源;IDE 的产物只是薄薄的提示头,负责把请求路由到引擎。

---

## 使用案例——具体场景

八个真实场景。挑一个最贴近你处境的,改一下调用参数即可。

### 1. 在 Cursor 里做一个金融科技仪表盘

你在 Cursor 上做一个 MENA 新银行的仪表盘。装好插件、跑 discovery、跑 recommendation,然后生成仪表盘。

```bash
pip install uxskill
uxskill init                                # 识别 Cursor,写入 .cursorrules
uxskill discover                            # 10 字段录入
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

然后在 Cursor 里说:*"用 .ux/last-recommendation.json 里的推荐生成仪表盘界面"*。Cursor 读 `.cursorrules` 头,加载推荐,带着明确约束派遣一次仪表盘生成。

### 2. 在 Claude Code 里生成一份 Stripe 风格的落地页

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> 项目类型? landing
> 行业? fintech-payments
> 调性? 严肃、技术、自信
> 必备项? dark-mode、AA、移动优先
> 禁忌项? purple-gradients、three-equal-cards
> 参考品牌? stripe
> 技术栈? nextjs-15-app-router
> 地区? 全球
> 成功指标? 注册转化

/ux-recommend
> [返回选定的风格、配色、字体搭配、动效预设、组件、品牌范例]

/ux-design "用 Stripe 品牌规范作为范例生成落地页"
> [frontend-engineer 生成页面]

/ux-lint .
> [通过——Stripe 品牌规范得到尊重]
```

### 3. 在 CI 里审查既有代码以围剿 AI slop

两周前你发了一个 Next.js 应用。你想在每个 PR 上设一条硬底线,挡住 AI 指纹。

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

只要 PR 引入紫到蓝渐变、96px 的 Inter、"John Doe" 推荐语或拿 emoji 当图标,CI 就会失败。没有 LLM 成本。~200ms。

### 4. 给一个"看起来像 AI 生成"的既有界面抛光

你接手了一个 React 应用,看上去和其他 AI 生成的 SaaS 站点没差。你想让它不要长那样。

```
/ux-critique src/components/Hero.tsx
> [3 个亮点、3 个失分、1 步关键招——评点很坦诚]

/ux-lint src/
> [标记出 15 个高严重级别的 AI 指纹]

/ux-polish src/components/Hero.tsx
> [LLM 驱动的抛光 + 清除 AI-slop]

/ux-fix
> [把发现作为原子提交落地,并重跑检查器]
```

三条命令,一张抛光后的界面,每个修复一个原子提交。

### 5. 设计一个 Linear 风格的命令面板

```
/ux-component command-palette --brief="Linear 风格,暗色,等宽快捷键,最近项目优先"
> [读取 data/brands/linear.app.json 取 tokens + 签名手法]
> [读取 data/components.json 取 command-palette 解剖结构与状态]
> [带着明确的 Linear 规范派遣 frontend-engineer]
```

生成的组件用的是 Linear 真实的颜色 tokens、字体栈、动效约定与发丝密度——而不是"通用暗色 UI"。

### 6. 用 90 分钟和干系人开一场设计思维工作坊

你有一间会议室,5 个人,90 分钟。你希望他们带着行动方案离开,而不是带着"感觉"。

```
/ux-workshop "会员钱包转向" \
  --participants="2 名 PM、1 名设计师、1 名工程 lead、1 名客户代表" \
  --minutes=90
```

插件端到端地主持五个阶段(探索 → 热度图 → 干系人地图 → 解决方案草图 → 行动方案),计时,每阶段都有具体产出。最终输出是 `.ux/last-workshop.json` —— 行动方案,而不是只剩"有趣的发现"。

### 7. 发布后写一份可发表的案例研究

你发了会员钱包。你想要一篇作品集篇章。

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [读取 .ux/last-frame.json、last-workshop.json、last-research.json、last-design.json、last-a11y.json、last-polish.json、last-recommendation.json、last-discovery.json]
> [生成 Wfrah 编辑格式的案例研究,含 (A)-(G) 编号段落、发丝分隔线、双语兼容布局]
> [写入 case-studies/bashiti-loyalty.html]
```

这份案例研究是已完成、可发布的产物——不是草稿。纯黑白、editorial 字型、可直接上你的作品集。

### 8. 在非 AI 环境里跑 discovery(只要结构化录入)

你在做一份项目规划。你还不需要推荐——只需要一份结构化简报。

```bash
uxskill discover
# 10 字段录入,保存到 .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

你可以把 JSON 交给团队,粘到 Notion 文档里,或者喂给其他 AI 工具。ux-skill 不止是引擎,也是一个结构化录入工具。

---

## 与其他方案的对比

简表如下。逐列对比详见 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

| 维度 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| 斜杠命令 | **22** | 1 | 19 | 1 | 1 | 多 | 1 | 1 | 1 |
| 组件 | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| 动效预设 | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 品牌规范 | **72** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 反模式规则 | **35** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 安全的确定性检查器 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 支持的 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery 关卡 | **10 字段** | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 |
| `.ux/` 状态链 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| Star 数(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 坦诚评估

- **ui-ux-pro-max** 认知度更大,支持 18 个 IDE,在它的 CSV 上做了类 BM25 的检索。它没有组件清单、动效清单、品牌库或确定性检查器。
- **open-design** 拥有 19 个 skill + 预览,但只支持 Claude Code,而且没有反 slop 层。
- **hallmark** 在精神气质上最接近(也是反 slop),但它是单个 skill ——没有引擎、没有清单、没有可串联的命令。
- **material-3-skill** 在你专门要 Material Design 3 时极佳。我们不在 MD3 上跟它较劲。

按维度的完整细节见 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 路线图

### v2.1 — 检查器补全(2026 Q3)

- **+17 条延后的反模式规则**,合计 52 条。目标包括:dark-on-dark 的 hover 状态、只用颜色编码状态、冗余 z-index 升级、JS 里写死断点、用 opacity 代替 disabled 状态等。
- **`uxskill lint --fix`** 支持对机械可修复的命中进行安全重写(`button-no-type`、`img-no-alt` 空串、移除 `console-log-leak`)。
- **VS Code 扩展**,在编辑器内联呈现检查器命中(无需先跑 CI)。

### v2.2 — 组件清单扩展(2026 Q4)

- **+50 个组件**,合计 198 个。新增:带异步过滤的 combobox、带最近项启发式的 command-palette、条件化表单步骤、payment-element 变体、RTL 感知的日期选择器、MENA 专用电话输入、带 hijri 叠层的日历网格。
- **按组件输出 6 个技术栈的代码**(Next.js + React、Vue 3 + Nuxt、SvelteKit、Astro、Blade + Alpine、原生 HTML/CSS)。
- **组件 Playground**:在 uxskill.laithjunaidy.com/playground 试跑推荐引擎并实时预览组件。

### v3 — 市场 + 锁定(2027)

- **品牌规范市场** —— 发布与发现社区贡献的品牌规范。付费发布以资助审核。
- **自定义反模式规则** —— 项目可在 `data/anti-patterns.local.json` 里定义自己的正则规则(v2 已发布;v3 增加发现 + 共享)。
- **`uxskill plan`** —— 从一份简报出发的完整多页站点规划,而不只是单个界面。
- **Figma 插件等同实现** —— 同一个推荐引擎,搬到 Figma 里。

---

## 参与贡献

欢迎 issue 与 PR。三个高杠杆方向:

### 新增一条反模式规则

1. 编辑 `data/anti-patterns.json` —— 添加一条带 `id`、`name`、`severity`、`category`、`detection.pattern`、`detection.flags`、`detection.scope`、`evidence_template`、`fix`、`references` 的条目。
2. 在 `tests/linter/` 里加测试 —— 一份会触发规则的文件,一份不会的。
3. 跑 `uxskill lint tests/linter/should-trigger/<rule>.tsx` —— 确认会被命中。再跑 `tests/linter/should-not-trigger/<rule>.tsx` —— 确认不会被命中。
4. 提一个 PR。

### 新增一份品牌规范

1. 创建 `data/brands/<slug>.json`,字段包含 `id`、`name`、`category`、`voice`、`tokens`、`design_principles`、`signature_moves`、`anti-moves`、`references`。
2. 在 `references/brands/<slug>.md` 添加对应散文。
3. 在 `data/brands/_index.json` 登记。
4. 提一个 PR。规范必须有一手出处(品牌实际的产品、公开的设计系统,或他们公开发布的 DESIGN.md)。

### 新增一个动效预设

1. 编辑 `data/motion-presets.json` —— 添加一条带 `id`、`name`、`category`、`tokens`、`stacks`(framer_motion、gsap、css)、`accessibility.reduced_motion_fallback`、`when_to_use` 的条目。
2. 该预设必须有 reduced-motion 变体。无一例外。
3. 提一个 PR。

### 流程

- 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解完整流程。
- 阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
- 新规则与品牌规范会按以下标准复核:一手出处、不过度拟合到单个项目、数据中不出现 emoji、在适用时的 RTL 安全行为。

---

## 许可证、作者、致谢

### 许可证

MIT。用它、fork 它、在它之上构建。如果它帮你少出货了一份 AI slop,请给仓库点个 star——这是成本最低的支持方式。

### 作者

**Laith Aljunaidy** —— [Dot](https://thedotwallet.com) 的独立创始人,Dot 是一个 MENA 优先的会员平台。我打造 ux-skill,是为了让 AI 生成的前端不再千篇一律。

- LinkedIn:[linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- 邮箱:laith.aljunaidy.laith@gmail.com
- 仓库:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- 官网:[uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI:[pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm:[npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 致谢

- 感谢 Anthropic 团队提供了 Claude Code,以及让这一切可分发的 skill / 插件架构。
- 感谢 Nielsen Norman Group、Laws of UX(lawsofux.com)以及让 `data/ux-guidelines.json` 言之有据的 UX 研究社群。
- 感谢 `data/brands/` 里列出的每一个品牌——它们公开的设计系统是品牌规范的事实来源。
- 感谢原始的 v1 贡献者:那份一次成型的 Claude skill 是 v2 Python 引擎的种子。
- 感谢我们对比的那 8 个热门 Claude UX 插件——他们抬高了基准;这是我们的回答。

---

**ux-skill** · **v2.0.0-alpha.1** · 为让 Claude Code、Cursor、Windsurf 以及其他 AI 编程工具产出的前端不再被一眼识别为 AI 生成而打造。

> 给仓库点星:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · 通过 `pip install uxskill` 或 `npx uxskill init` 安装 · 浏览对比:[uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
