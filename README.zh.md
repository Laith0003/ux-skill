[English](README.md) · [العربية](README.ar.md) · **简体中文** · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill：为 Claude Code、Cursor 及一切 AI 编程工具打造的设计智能引擎

**一个设计智能引擎，让 AI 生成的 UI 有辨识度，而不是千篇一律。** 接入 17 款 AI 编程工具中的任何一款，产出就不再一看就是 AI 做的。免费、MIT、离线、无 LLM。

```bash
pip install uxskill
```

**[在 GitHub 上给 ux-skill 点个星](https://github.com/Laith0003/ux-skill)**：如果它对你有用，这是支持项目最省事的方式。第一次来？从 [60 秒导览](#快速安装)开始，或者到 [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) 看实际效果。

![之前：千篇一律的图库照片 hero，柔和的紫色渐变，毫无品牌辨识度。之后：深色遮罩下的真实工地照片，带琥珀色强调的编辑风标题，以及嵌在 hero 里的报价申请表单。同样的提示词，由 ux-skill 提供约束时结果就不同。](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*之前：千篇一律的图库照片 SEO 废料。之后：深色遮罩下的真实工地照片 hero，带琥珀色强调的编辑风标题，hero 内的报价表单。同样的 AI 编程工具、同样的提示词，由 ux-skill 提供约束时结果就不同。*

> **v4.0，FOUNDATIONS：一条命令构建一套完整、经过 WCAG 检查的设计系统，内置阿拉伯语和从右到左排版。** 面向 AI 编程的最强 UX 插件。一个 Python 推理内核，带确定性的 7 轴合成器，12 份可查询的 JSON 清单（84 种风格、176 套配色、70 组字体搭配、148 个组件、184 个行业、35 种图表、57 个动效预设、112 条 UX 定律、171 条反模式规则、25 个技术栈、160 份品牌规范），18 个斜杠命令、5 个子代理、25 个 MCP 工具，以及一个确定性的反 AI slop 检查器。跨 IDE：可装入 Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、Kiro、Cline、Continue、Aider、Zed、JetBrains AI、Pieces、Tabby、Tabnine、CodeWhisperer 和 Roo Cline。

> **品牌名是 `ux-skill`。** PyPI / npm 包名仍为 `uxskill`。GitHub 仓库位于 [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)。

**作者：** [Laith Aljunaidy](https://laithjunaidy.com)，常驻安曼的设计师兼 CTO · **网站：** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **与所有 Claude UX 插件对比：** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub：** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI：** [uxskill](https://pypi.org/project/uxskill/) · **npm：** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#面向-17-个-ide-的安装器)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### 4.0 新功能：设计基础

输入一个品牌色，输出一套设计系统，对比度在交到你手上之前就已检查过。

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

需要 Python 3.10 或更高版本。MCP 服务器请用 `pip install --upgrade 'uxskill[mcp]'`。用 pipx 则是 `pipx install uxskill`（在已安装的 3.x 上升级用 `pipx upgrade uxskill`）。用 npm 则是 `npx uxskill@latest`。从 3.x 迁移？[迁移指南](docs/migrating-to-4.md)把每个 3.x token 对应到它在 4.0 中的角色。

**在做产品或落地页？** 你会得到：供页面引用的 `tokens.css`，为所选字体配好度量匹配的后备字体的 `fonts.css`，从你自己的文件加载字体的 `fonts-self-host.css`，供工具使用的 `tokens.json`，放在 `art/` 里的装饰性品牌图形，以及 `system-report.md`，用平实的话说明构建了什么、为什么这样做、应该从哪种页面构图开始。用角色写样式（`var(--color-action-primary)`、`var(--color-text-default)`、`var(--color-surface-page)`），在 `<html>` 上用一个属性就能切换深色模式、高对比度、紧凑间距、从右到左或减少动态效果。字体可以用报告给出的 Google Fonts 链接加载，也可以用 `fonts-self-host.css` 加一个 `fonts/` 文件夹加载；无论哪种方式，都要在 `tokens.css` 之前引用 `fonts.css`；这两个文件都不要改。加上 `--brief` 时，如果简报写明了行业和语气，外观就随之调整；结构化字段（年龄、语言、默认配色方案、阅读场景）决定文字大小、点按区域、文字系统以及默认打开哪种配色方案；discovery 不会问行业，所以由 `/ux-system create` 来问。在 Claude Code 中，`/ux-system create` 会检查已安装的版本、运行构建并解读报告。

**在设计设计系统？** 九大基础（颜色、字体、间距、布局、圆角、边框、层级、动效、图像），每一项都随七个轴连续变化，包含原始值和语义角色，采用 W3C 设计令牌格式（DTCG 2025.10）并给出每种模式的取值。输入相同，字节相同。通过 MCP，`ux_system_build` 返回报告、检查结果和每个文件的大小，传入 `out` 时会写出与命令相同的文件。

- **WCAG 检查。** 每一组文字、控件和焦点的颜色搭配，都会在浅色和深色、标准对比度和高对比度下测量：标准对比度下按 WCAG 1.4.3（文字 4.5:1）和 1.4.11（非文本 3:1），高对比度下按 WCAG 1.4.6（文字 7:1）；此外，由于 WCAG 没有规定非文本的增强级别，我们为大多数非文本部件额外设定了高对比度下 4.5:1 的下限，这是我们自己的标准。未通过的系统不会写出，提示信息会说明该改什么。
- **默认安全。** 绝不覆盖内容不同的文件。只有你要求时，`--force` 才会替换文件。
- **阿拉伯语。** 在 `dir="rtl"` 下，文字切换到一款阿拉伯字体，使用它自己的字号和行高；间距使用逻辑属性，动效左右镜像。`--latin-only` 可以去掉这部分。

**你已经有一套系统？** `/ux-system enhance --from` 按它原本的命名读取（DTCG token、CSS 自定义属性、Tailwind 主题、markdown 规则文件或 Figma 变量导出），用同一套检查把关，并测量你的代码实际上是怎么使用它的；不会改写任何东西。`/ux-system extend --from` 在旁边的一个扩展文件里补充基础、角色或契约，不改动它已有的任何 token；`uxskill system export` 则把它写成 tokens.css、Tailwind 4 主题或 Figma 变量。4.2 会加入信任层（每次写入都跑 lint，加一个收尾评审）并正式发布。详见 [changelog](CHANGELOG.md)。

**组件与区块。** 23 份组件契约规定控件的每个部分在每种状态下绑定哪些 token，以及每种状态如何运动：状态变化按 `motion.state` 过渡，按下时按 `motion.press.scale` 缩放（在减少动态效果时保持静止），标签页、菜单和分段控件则滑动同一个指示器。14 份区块契约（hero、定价、FAQ、页脚等）规定每个区块的职责、各插槽可放的组件、需要的佐证，以及在手机上如何堆叠。用它们搭出的页面使用照片；界面截图只是额外的图像，绝不替代照片。

**会读页面的检查器。** 171 条规则，其中许多会对解析后的 CSS 和标记再做一次检查，读取页面自身的系统：动效时长按它的曲线计算，标题大字的行高要守住引擎的下限，隐藏的控件必须退出 Tab 顺序。`uxskill lint --render` 会在无头 Chromium 中以桌面宽度和手机宽度打开每个页面并实际操作：看不见或被裁切的焦点环、响应迟缓的悬停和按下、按 Escape 后丢失的焦点，以及在减少动态效果时仍在运动的按下效果。

**命令更少。** 25 个斜杠命令精简为 18 个。`/ux-discover` 支持 `--frame` 和 `--recommend`，`/ux-design` 支持 `--component`、`--dashboard` 和 `--from-image`，`/ux-polish` 循环执行 lint、修复、再 lint，直到分数达到 90 或跑满三轮，`/ux-init` 支持 `--stats`。七个旧名称仍可作为别名使用，将在 4.1 移除；见[别名](#别名将在-41-移除)。

**按界面分的规则手册。** 落地页、仪表盘和组件的规则放在 `references/surfaces/`，各有一份手册。`/ux-design` 按模式只加载其中一份，所以构建仪表盘时永远不会读到 hero 的规则。

测试 **9764 项通过**。离线。确定性。从不调用 LLM。

### v3.1 新增：忠于品牌、响应式、有生命力

- **品牌忠实度是强制的，而不是寄望的。** 主色从 LOGO 的像素中读取（而不是从涂得最多的 CSS 中读取）；与 logo 字形风格不符的默认字体会被拒绝。提取出的品牌沿 `recommend` -> `synthesize` 传递，`evaluate` 中的**硬性下限**会判定任何丢掉品牌色或 logo、或没有真实图像的输出为失败。与开放的 `brand.md` 约定双向互通（渲染 + 导入）。
- **移动优先，有关卡把守。** 新的工艺基础（`responsive.md`、`component-behaviors.md`），加上一个能感知换行的关卡：出现横向滚动、导航、字标或按钮文字换行，或者吸顶页头过高，都判为失败。
- **惊艳层。** 引擎为每个页面推导出 2-3 个相互配合的标志性时刻；"惊艳只能来自用户"的说法就此被推翻。
- **更敏锐的检查器**（152 条规则）：检测必需图像和纯图标元素，新增占位 token 与 `100vw` 规则；保留带种子的 picsum，去掉随机的。

完整说明见 [CHANGELOG.md](CHANGELOG.md)。

### v3 新增内容

- **品牌规格变成训练数据,而非模板。** 160 个品牌规格不再是推荐器从中挑选的目录,而是合成器蒸馏的词汇。每次调用都产生新输出。
- **7 轴合成器**(warmth, contrast, density, geometry, formality, motion, type_personality)。Brief 确定性映射到轴值;轴值编译为全新的 palette + 字体 + spacing + radius + motion token。
- **三种自动分派模式**：`strict_brand`(单一品牌 100%)、`brand_anchor`(单一品牌 70% + 同类品牌轴向适配 30%)、`pure_synthesis`(未指定品牌，从轴向匹配的 8 个范例中蒸馏)。
- **决策日志重新排序推荐器。** `.ux/decisions.jsonl` 按同一 `(industry, ui_type)` 桶内的历史胜出对候选重新排序。冷启动安全。仅计算 `lint_score >= 80` 且 `user_accepted = true` 的决策。
- **轴交互矩阵**：显式解决竞争轴之间的冲突(dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius)。不再有沉默的临时规则。
- **`/ux-evolve` 自动循环**（在 4.0 中是 `/ux-polish` 的默认循环）：lint → polish → re-lint，直到分数 ≥ 90、进入平台期，或在 4.0 中跑满 3 轮（v3 中为 5 轮）。质量门控在 65。
- **3 个新 MCP 工具**(15 → 18):`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`。
- **本地统计仪表盘**：`uxskill stats --html` 写出 `.ux/stats.html`,显示**你的**安装学到了什么。无遥测,无全局聚合。
- **223 个测试通过。** 离线。确定性。从不调用 LLM。

完整细节见 [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain)。

### Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill 是什么

ux-skill 是一个面向 AI 编程工具的**设计智能引擎**。它以 Python 包的形式运行(`pip install uxskill`),也作为 Claude Code 插件运行,同时提供一个面向 17 个 IDE 的多重安装器。引擎接收一份项目简报(行业、受众、调性、必备项、禁忌项、技术栈、地区),并返回一套完整的推荐设计系统:风格、配色、字体搭配、动效预设、组件、可供研习的品牌范例,以及必须坚守的反模式护栏。该推荐是确定性的，相同输入永远产出相同结果。

这个插件位于你与 AI 编程工具之间。当你让 Claude Code、Cursor 或任何其他 AI 助手"做一个金融科技落地页"时，助手通常会即兴发挥，结果在五秒钟内就能被识别为 AI 生成（紫到蓝的渐变、三张等大的卡片、用 Inter 做超大显示字、测评里出现"John Doe"、默认 300ms 的过渡、居中 hero、CTA 上跳动的箭头）。ux-skill 用**结构化约束**取代即兴发挥：你用 `/ux-discover` 记录简报并选定系统，用 `/ux-design` 生成代码，再用 `/ux-lint` 在提交前确认它通过 171 条确定性的反 AI slop 规则。

这份 README 是权威参考。每一个命令、每一个子代理、每一份数据清单、每一条安装路径、每一份品牌规范、每一类反模式，全都记录在这里。如果你正在挑选 Claude Code 的设计插件,或者在为 Cursor、Windsurf 或 Codex 比较 AI 设计工具,请把这篇从头到尾读一遍,并对照 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 目录

1. [大脑，v3.0 是什么](#大脑v30-是什么)
2. [快速安装](#快速安装)
3. [数据对比，与 Top 8 Claude UX 技能的实时比较](#数据对比与-top-8-claude-ux-技能的实时比较)
4. [架构，各部件如何咬合](#架构各部件如何咬合)
5. [18 个斜杠命令，详细参考](#18-个斜杠命令详细参考)
6. [5 个子代理](#5-个子代理)
7. [11 份数据清单](#11-份数据清单)
8. [171 条反 AI slop 规则，检查器](#171-条反-ai-slop-规则检查器)
9. [160 份 DESIGN.md 品牌规范，按类别](#160-份-designmd-品牌规范按类别)
10. [MCP 服务器，非对称的一着](#mcp-服务器非对称的一着)
11. [面向 17 个 IDE 的安装器](#面向-17-个-ide-的安装器)
12. [使用案例，具体场景](#使用案例具体场景)
13. [与其他方案的对比](#与其他方案的对比)
14. [路线图](#路线图)
15. [参与贡献](#参与贡献)
16. [许可证、作者、致谢](#许可证作者致谢)

---

## 大脑：v3.0 是什么

v3.1.0 是 ux-skill 历史上最大的架构转变。推荐器不再从目录中挑选模板，引擎为每份 brief **合成**新鲜的设计语言。相同的 brief 始终产生相同的输出(完全确定性),但每份不同的 brief 都得到自己的新系统。品牌规格不再是模板;它们是引擎从中学习词汇的训练数据。系统能看到自身历史,在本地闭合反馈回路,从不调用 LLM。

编译器是**确定性 7 轴合成器**，warmth, contrast, density, geometry, formality, motion, type_personality。每份 brief 映射到轴值;轴值编译为全新的 palette + 字体 + spacing + radius + motion token。模块化字体比例从 contrast 中选取比率(1.200 quiet / 1.250 balanced / 1.333 loud)。布局原语由构造即响应式(`auto-fit minmax(min(N, 100%), 1fr)` + 容器查询)。损坏的布局无法发出,因为它们不可表示。

三种自动分派模式:`strict_brand`(`reference_brands=[stripe] strict=True` → 100% Stripe token,最快路径);`brand_anchor`(`reference_brands=[stripe]` → 70% Stripe + 来自 4 个同类品牌的轴向适配 30%);以及 `pure_synthesis`(未指定品牌 → 无限空间,从轴向匹配的 8 个范例蒸馏为新设计语言)。竞争轴由文档化的**轴交互矩阵**解决，dense + corporate 编译为 4px(density 胜出,Bloomberg 流派),airy + corporate 为 12px(formality 胜出,奢华),soft + playful 为 18px radius,sharp + corporate 为 2px。实现中无沉默的临时规则。

**决策日志**（`.ux/decisions.jsonl`，schema `_v: 1` 已锁定）闭合反馈回路。推荐器现在按同一 `(industry, ui_type)` 桶内的历史胜出对候选重新排序。冷启动安全：先前的决策少于 3 条时跳过重排。仅计算 `lint_score >= 80` AND `user_accepted = true` 的决策。此外 `/ux-polish` 运行 lint → polish → re-lint，直到分数 ≥ 90、进入平台期或跑满 3 轮，低于 65 分质量门控的输出，除非加 `--force`，否则拒绝。结果：每个安装都在自己的语料上越用越聪明，每次运行都能跨机器复现，引擎始终完全离线。

---

## 快速安装

三条安装路径。请挑选与你的环境匹配的那条。

### 路径 1：Claude Code 市场(权威路径)

如果你常驻 Claude Code,请通过插件市场安装:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

这会将全部 18 个斜杠命令（以及作为别名保留到 4.1 的 7 个旧名称）与 5 个子代理接入你的 Claude Code 会话。安装完成后，执行 `/ux-init` 以建立项目级别的 `.ux/` 状态目录，并核实 Python 引擎可达。

### 路径 2：pip(通用路径)

如果你身处 Claude Code 之外(Cursor、Windsurf、CLI、CI),请安装 Python 包:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

包同时暴露 `ux` 与 `uxskill` 两个 CLI 入口，它们是同一个二进制。

### 路径 3：npx(无需自行管理 Python)

如果你不想直接管理 Python,npx 封装层会通过 `pipx` 自动拉起:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### 验证安装

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

这些计数加起来共 1,262 条。如果任一计数返回 0，意味着对应的 JSON 文件缺失，请到 [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) 提个 issue。

---

## 数据对比：与 Top 8 Claude UX 技能的实时比较

Star 数最后一次通过 `gh api` 核对的时间是 **2026-05-28**。ux-skill(Laith0003/ux-skill)是最新入场的，我们在认知度上极小,在架构深度上极深。下面这张表是诚实的:哪里我们输,哪里我们赢。

| 插件 | Star 数 | 架构 | 斜杠命令 | 静态检查器(可上 CI) | 品牌规范 | 组件 | 动效预设 | 支持的 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV,单一 skill | 1 | - |，| 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 个 skill + 预览 | 19 | - |，| 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + 研究背书的审美 | 1 | - |，| 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 单份 62 KB SKILL.md + 脚本 | 1 | - |，| 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | 接入 MCP 的 skill 库 | 多个 | - |，| 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 单一审美 skill | 1 | - |，| 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 反 slop 设计 skill | 1 | - |，| 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 组件 + 审查 | 1 | - | (仅 MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python 引擎 + 12 份清单 + 18 个命令 + 5 个子代理 + CI 检查器** | **18** | **171 条确定性规则** | **160** | **148** | **57** | **17** |

### 我们输在哪里

- **认知度。** 他们有数十万颗 star。我们有 14 颗。给我们点个 star，这是成本最低的支持方式。
- **品牌识别度。** ui-ux-pro-max 和 open-design 的领先优势是按月算的,不是按天。
- **营销打磨。** 他们有截图、演示视频和能被搜到的落地页。我们有一份完备的 README 和一张轻量的落地页。

### 我们赢在哪里

- **组件库:** 148 个带解剖结构、状态、所用 token 与动效规范的文档化组件。其他 8 个里没有任何一个发布过组件清单。
- **动效预设:** 57 个开箱即用的栈级条目(Framer Motion、GSAP、CSS),全部带 reduced-motion 兜底。其他几家都不发布动效清单。
- **反模式静态检查器：** 171 条确定性规则，能在 CI 中运行，遇 Critical/High 退出非零码。其他几家没有任何确定性检查器。
- **品牌规范:** 160 份真实 DESIGN.md 规范(Apple、Stripe、Linear、Figma、Tesla、BMW、Notion、Spotify、Airbnb、Vercel、Supabase、Cursor、Raycast、Claude,以及其余 96 个)。其他几家没有品牌库。
- **支持 17 个 IDE:** 同一个引擎,IDE 之间用不同的"胶水"对接。
- **18 个斜杠命令：** discovery、生成（页面、组件、仪表盘、从图片生成）、审查、lint、polish 循环、修复循环、案例研究、工作坊、文案、动效、a11y、conductor，彼此完全打通。

完整的逐列对比详见 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 架构：各部件如何咬合

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

### 引擎实际如何运作

1. **输入。** 你提供一份简报，可以通过 `/ux-discover` 交互式填写（10 个字段），也可以给 `ux recommend` 传参数以非交互方式提供。
2. **5 路并行检索。** 引擎在各清单上同时执行五项查询：
   - **行业 → recommended_styles** (industries.json)
   - **风格 → 配色 + 字体 + 动效兼容性** (styles.json)
   - **语气 × 必备项 → 配色筛选** (palettes.json)
   - **技术栈 → 组件兼容性 + 动效预设** (tech-stacks.json, motion-presets.json)
   - **禁用项 + 地区 → 护栏 + 品牌范例候选** (anti-patterns.json, brands/)
3. **合并。** 一个确定性的合并器为候选排序、解决冲突（例如必备的深色模式决定配色模式），并输出唯一一套推荐系统。
4. **输出。** 一份 JSON 文档，包含选定的风格、配色、字体搭配、前 5 个动效预设、前 12 个组件、前 5 个品牌范例，以及全部启用的 171 条反模式护栏。另附一段说明每项选择理由的依据。
5. **生成。** 后续命令（页面、组件、仪表盘和图片模式下的 `/ux-design`，以及 `/ux-system`）使用这份推荐，经由子代理生成真实代码。
6. **验证。** `/ux-lint` 用 171 条规则重新扫描生成的代码。CI 中遇 Critical/High 退出非零码。

**v3 新增。** 推荐器现在借助 `.ux/decisions.jsonl` 从 `engine/decisions/` 对候选重新排序（仅计算 `lint_score >= 80` AND `user_accepted = true` 的决策；先前的决策少于 3 条时作为冷启动安全处理）。生成路径可以转入 `engine/synthesizer/`，这是一个确定性的 7 轴编译器，会为每份简报产出全新的配色 + 字体 + 间距 + 圆角 + 动效 token，而不是从目录里挑模板。详见[大脑，v3.0 是什么](#大脑v30-是什么)。

**Python 负责思考。HTML 负责呈现。Markdown 负责串联。**

---

## 18 个斜杠命令：详细参考

每个命令都以 `.md` 文件形式放在 `commands/` 下，包含 `description`、`allowed-tools`、`triggers`、`when to use`、`when to skip`、`input`、`process` 和 `output state file`。下面的描述是精简版；完整源文件才是权威规范。

命令分为七组：**引导与盘点**、**发现与推荐**、**生成**、**审查与验证**、**修复与打磨**、**发现与叙事**，以及**指挥**。七个 3.x 名称在 4.1 之前仍可作为[别名](#别名将在-41-移除)使用。

### 初始化与库存

#### `/ux-init`：给项目做初始化

- **做什么：** 识别你在哪个 IDE（`.claude/`、`.cursor/`、`.windsurf/` 等），安装匹配的产物，核实 Python 引擎可达，打印一份统计快照。`--stats` 只打印快照：版本 + 各数据清单的条目数。
- **何时使用：** 在新项目里首次安装；克隆了使用 ux-skill 的项目之后；`pip install --upgrade uxskill` 之后。`--stats` 用于安装后、升级后，或推荐结果出人意料、怀疑清单不完整时。
- **何时跳过：** 你已经在这个项目里跑过，而且没有任何变动。`--stats` 永远不必跳过：它只是一次 50ms 的读取。
- **调用方式：** `/ux-init`（无参数）、`/ux-init --stats`，或在 CLI 里跑 `uxskill init` / `uxskill stats`。`--decisions` 会附上决策日志摘要；`--html` 会写出 `.ux/stats.html`。
- **输出：** 各 IDE 对应的产物（详见[面向 17 个 IDE 的安装器](#面向-17-个-ide-的安装器)）+ `.ux/` 目录 + 标准输出摘要。`--stats`：向标准输出打印 JSON（见上文[验证安装](#验证安装)）。
- **下接：** 接下来是 `/ux-discover`。`--stats` 仅用于诊断。

#### `/ux-mcp`：把引擎作为 MCP 服务器运行

- **做什么：** 通过 stdio 把引擎作为 Model Context Protocol 服务器启动。25 个工具（推荐器、检查器、持久化、合成器、决策日志、图片提取、各数据清单，以及设计系统的构建、导入、增强、扩展、导出和检查）无需插件即可从任何支持 MCP 的宿主调用。
- **何时使用：** 你在另一个支持 MCP 的宿主里工作，想用同一个引擎。你运行的多代理流水线需要单一的设计约束来源。你想在 CI 中把推荐器或检查器作为常驻进程。
- **何时跳过：** 你在已安装插件的 Claude Code 里；斜杠命令已经能直达引擎。你只需要一次性的答案；`uxskill recommend` 或 `uxskill lint` 更简单。
- **调用方式：** `/ux-mcp`，或在 `pip install 'uxskill[mcp]'` 之后从 shell 运行 `ux-mcp`。
- **输出：** 一个 stdio JSON-RPC 服务器。各客户端的配置见 [MCP 服务器](#mcp-服务器非对称的一着) 和 `commands/ux-mcp.md`。
- **下接：** 无；它是传输层，不是一个步骤。

### discovery 与推荐

#### `/ux-discover`：强制关卡（10 字段采集、框定、推荐）

- **做什么：** 每个项目在执行任何生成命令之前都必须完成的 10 字段采集。项目类型、受众、主要目标、语气、必备项、禁用项、参考品牌、技术栈、地区、成功指标。**不许即兴发挥。** 被禁用的词（"modern"、"clean"）逼用户说具体。随后运行推荐器：Python 引擎在 12 份清单上做 5 路并行检索，返回一套合并后的设计系统（行业 → 风格 → 配色 → 字体 → 动效 + 组件 + 品牌范例 + 护栏）。
- **模式：** `--frame` 用一个四字段的框定块记录为谁、结果、假设和成功信号，比完整采集更轻量。`--recommend` 只运行推荐器，输入来自已保存的简报或一次性参数。
- **何时使用：** 在任何 `/ux-design` 或 `/ux-system` 之前。每当之前的简报已经过时。`--frame` 用在项目、冲刺或一次性任务的开头，或对话跑偏时的半途中。`--recommend` 用在给一个看起来疲惫的产品重新定位时。
- **何时跳过：** 你在修 bug（`/ux-fix`）；你只是跑一遍检查器（`/ux-lint`）；简报自上次会话以来没有变化。
- **调用方式（Claude Code）：** `/ux-discover`、`/ux-discover --frame "loyalty wallet for a MENA retail pilot"` 或 `/ux-discover --recommend`。
  **调用方式（CLI）：**
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
- **输出：** `.ux/last-discovery.json`（10 字段简报）、`.ux/last-recommendation.json`（选定的风格、配色、字体搭配、前 5 个动效预设、前 12 个组件、前 5 个品牌范例、全部启用的 171 条反模式护栏，以及依据），使用 `--frame` 时还有 `.ux/last-frame.json`（`{audience, outcome, hypothesis, success_signal}`）。
- **下接：** `/ux-design [extra brief]` → 以推荐为依据的前端代码。`/ux-design --component <name>` → 符合已发现约束的单个组件。`/ux-system` → 由推荐生成的完整设计系统。`/ux-lint` → 验证生成的代码。

### 生成

#### `/ux-design`：由简报生成漂亮、反 slop 的界面

- **做什么：** 由 discovery 简报 + 推荐生成完整的生产级前端产物（落地页、营销站、应用外壳）。在反 slop 与 arsenal 参考的创意指引下，派遣 `frontend-engineer`。由简报或参数在四种模式中选一种：
  - **页面**（默认）：一个完整页面或多区块界面。写入 `.ux/last-design.json`。
  - **`--component [name]`**：单个生产级组件（按钮、模态框、导航栏、侧边栏、卡片、表格、表单、图表）。四种交互状态齐全，无障碍，贴合品牌。先在 `.ux/last-recommendation.json` 中查找该组件，找不到再直接查询清单。写入 `.ux/last-component.json`。
  - **`--dashboard`**：讲究数据密度、bento 布局、表格等宽数字、sparkline 模式、避免卡片泛滥、语义化状态色、克制的动效。不是贴了几张图表的营销站。写入 `.ux/last-dashboard.json`。
  - **`--from-image <path>`**：用纯 Pillow 计算机视觉读取一张设计参考图（PNG/JPG/WebP）（主色板、画布明暗、字体信号），与配色和风格清单比对，再按得到的推荐来构建。`--extract-only` 在提取后停止。写入 `.ux/last-image-extract.json`。
- **何时使用：** "设计一个"、"给我做一个"、"生成一个落地页"、"做一个仪表盘"、"做一个组件"、"做一个按钮"、"设计后台管理面板"、"运营控制台"、"KPI 看板"、"照这张截图做"，任何形式自由的视觉交付请求。
- **何时跳过：** 你要的是评审而不是构建（用 `/ux-audit` 或 `/ux-critique`）；后端或基础设施工作。
- **调用方式：** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`、`/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`、`/ux-design --dashboard`、`/ux-design --from-image ref.png`。
- **输出：** 生成的代码（HTML / Blade / JSX / Vue / Astro），外加该模式的状态文件。
- **下接:** `/ux-lint` → 验护栏;`/ux-polish` → 抛光;`/ux-a11y` → 可访问性审查;`/ux-copy` → 微文案审查;`/ux-fix` → 以原子提交落地。

#### `/ux-system`：生成一套完整的起步设计系统

- **做什么:** 给还没有设计系统的项目提议一整套起步系统，tokens(颜色、字体、间距、动效、圆角、阴影)、基础文档、组件契约、暗色模式映射、主题切换器。派遣 `design-system-architect`。
- **何时使用:** "我们没有设计系统"、"给我们搭一套"、"提议一份 tokens"、"我们的主题该长什么样"、"把 DS 搭起来"。
- **何时跳过：** 项目已经有设计系统，改用 `/ux-design --component` 基于现有系统构建即可；后端或基础设施。
- **调用方式：** `/ux-system create`（设计基础引擎）、`/ux-system enhance --from <file>`（测量你已有的系统）、`/ux-system extend --from <file> --add <foundation>`（在不改动的前提下扩充），或 `/ux-system`（3.x 流程；如果还没存档，先跑 discovery）。
- **输出:** `tokens.json`、`foundations.md`、`components/*.md` 契约,可选输出 Tailwind / vanilla / SCSS。写入 `.ux/last-system.json` 以供后续衔接。
- **下接：** `/ux-design --component` → 基于新系统构建。`/ux-design` → 用新 token 生成界面。

#### `/ux-motion`：动效处理

- **做什么:** 生成界面的动效层，时长、缓动、编排、reduced-motion 兜底、性能纪律。也对现有动效按五个维度做审查(时长、缓动、含义、reduced-motion、性能)。
- **何时使用:** "检查一下动效"、"动画做得对不对"、"修一下动效"、"复核动画"、"动效审查"、"对动效做性能扫"。
- **何时跳过:** 界面没有动效(用 `/ux-audit` 或 `/ux-polish`);后端或基础设施。
- **调用方式:** `/ux-motion path/to/component.tsx`(审查模式)或 `/ux-motion --generate hero-entry`(生成模式)。
- **输出:** 更新后的代码(生成模式)或 `.ux/last-motion.json` 报告(审查模式)。
- **下接:** `/ux-fix` → 落地动效结论;`/ux-polish` → 抛光。

### 审查与验证

#### `/ux-lint`：基于正则的确定性检查器(无 LLM,CI 安全)

- **做什么：** 对你的代码跑 171 条规则。无 LLM 调用。CI 中遇 Critical / High 退出非零码。源文件：`data/anti-patterns.json`。规则覆盖 A11y（45）、内容（35）、布局（18）、字体（16）、动效（14）、视觉（14）、质量（12）、颜色（10）、性能（5）、层次（2）。
- **何时使用：** 预提交钩子；CI 关卡；在花 `/ux-audit` 成本之前对大代码库做的快速首轮；在任一模式的 `/ux-design` 之后用于验证生成。
- **何时跳过:** 你想要修复循环(检查器只报告、不修改，请接 `/ux-polish --fix` 或 `/ux-fix`);你想要审美判断(用 `/ux-critique`)。
- **调用方式(slash):** `/ux-lint src/`。
- **调用方式(CLI):** `uxskill lint .` 或 `python3 bin/ux-lint.py .` 或 `bash bin/ux-lint.sh --ci --fail-on high`。
- **调用方式(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **输出:** 标准输出中的命中(位置、规则 id、严重级别、证据)。无命中时退出码 0,设了 `--fail-on high` 且命中 Critical/High 时退出非零。
- **下接:** `/ux-polish --fix` → 同类模式的 LLM 版对手;`/ux-fix` → 按严重级别落地为提交;`/ux-audit` → 完整的六镜头推理回合;`/ux-next` → 让指挥来决定。

#### `/ux-audit`：六镜头设计审查

- **做什么:** 一次结构化、带立场的评审,从六个镜头(清晰度、层级、可访问性、嗓音、动效、审美)出发,产出按严重级别打标的发现。Polaris 风格的报告。先读 `.ux/last-frame.json`，受众与结果决定每条发现的严重级别。
- **何时使用:** 界面已存在,你需要一份能站得住脚的批评。"审一下"、"看看这版 UX"、"做得好不好"、"哪里坏了"、"狠狠拆一下"。
- **何时跳过:** 界面尚未存在(用 `/ux-design`);用户只要一个镜头(用对应专项命令:`/ux-a11y`、`/ux-copy`、`/ux-motion`、`/ux-polish`);用户想要审美观点(用 `/ux-critique`);后端或基础设施。
- **调用方式:** `/ux-audit https://example.com/pricing` 或 `/ux-audit src/components/Pricing.tsx`。
- **输出:** 写入 `.ux/last-audit.json`，`findings` 数组,字段为 `{lens, severity, title, principle, evidence, fix}`,以及 `severity_counts`、`dominant_lens`、`strategic_moves`。
- **下接:** `/ux-fix` → 落地;`/ux-polish` → 抛光;`/ux-design` → 若需结构性重设计。

#### `/ux-a11y`：WCAG 2.1 AA 审查 + 基本礼貌检查

- **做什么:** 一次结构化的 WCAG 2.1 AA 审查,外加那些自动工具能放行、但仍会伤害真实用户的"基本礼貌"检查(可见焦点、错误具体性、动效偏好、键盘陷阱、颜色依赖)。
- **何时使用:** 发布前可访问性关卡;重新设计之后;"做一下可访问性检查"、"WCAG 审查"、"这个可访问吗"、"a11y 复核"、"读屏测试"、"键盘导航检查"。
- **何时跳过:** 不面向用户;后端或基础设施;还在草图阶段的工作。
- **调用方式:** `/ux-a11y https://example.com`(优先用线上 URL，自动工具和键盘测试只能在线上跑)。
- **输出:** 写入 `.ux/last-a11y.json`，`findings` 数组,字段为 `{wcag_sc, sc_name, severity, title, evidence, fix, category}`、`beyond_wcag` 数组、`severity_counts`。
- **下接:** `/ux-fix` → 落地为提交;`/ux-copy` → 在一次文案回合中顺手修 alt 文本和表单错误串接。

#### `/ux-critique`：审美评点(3 个亮点、3 个失分、1 步关键招)

- **做什么:** 一个设计师的态度，不是结构化审查,不是严重级别打分,只是一段紧致、有立场的看法,点名什么在起作用、什么没起作用,以及那一步能改变最多的关键招。
- **何时使用:** "你怎么看"、"这个好吗"、"评点一下"、"实话说"、"调性对不对"、"这像我们吗"、"该不该发"。
- **何时跳过:** 用户明确要的是结构化审查(用 `/ux-audit`);后端或基础设施。
- **调用方式:** `/ux-critique https://example.com`。
- **输出:** 写入 `.ux/last-critique.json`，3 个亮点、3 个失分、1 步关键招,外加散文。
- **下接:** 如果评点建议重设计就接 `/ux-design`;如果建议收紧就接 `/ux-polish`。

#### `/ux-copy`：微文案审查 + 重写

- **做什么:** 用嗓音量规评估每一句可见文案,产出 before/after 重写。专抓:"表单存在错误"(笼统)、"John Doe"(占位符)、AI 式欢欣鼓舞的庆祝话术、笼统的 CTA、空荡荡的空状态、毫无用处的错误提示。
- **何时使用:** 结构对了但文案弱。"复核文案"、"修微文案"、"错误提示糟糕"、"重写这个"、"收紧文案"、"按钮太笼统"、"空状态死气沉沉"。
- **何时跳过:** 布局问题(用 `/ux-audit` 或 `/ux-polish`);可访问性驱动的文案问题如 alt 文本(用 `/ux-a11y`);后端或基础设施。
- **调用方式:** `/ux-copy src/views/checkout.blade.php`。
- **输出:** 写入 `.ux/last-copy.json`，`strings` 数组,字段为 `{location, severity, before, after, notes}`,以及量规与需翻译的语言。
- **下接:** `/ux-fix` → 落地重写;`/ux-a11y` → 在文案改动后再复核。

### 修复与抛光

#### `/ux-fix`：以原子提交落地审查结果

- **做什么:** 从 `.ux/` 读取最近的报告(audit、copy、a11y、motion 或 polish),校验工作树,经由对应子代理把发现以原子提交的形式落地。落地后会重跑触发命令再核验。
- **何时使用:** 跑完一个审查类命令并复盘了发现之后。"修一下这些发现"、"把修复落地"、"跑修复循环"、"打补丁"、"按建议改"、"去修"。
- **何时跳过:** `.ux/` 里没有先前的报告;工作树是脏的且用户尚未同意 stash/commit;修复需要设计判断而不是机械落地(请改用 `/ux-design` 重设计)。
- **调用方式:** `/ux-fix`(自动识别要修哪份报告)或 `/ux-fix --from=last-a11y.json`。
- **输出:** 每条发现一个原子提交。重跑触发命令并更新 `.ux/last-*.json`。打印一段摘要。
- **下接:** `/ux-next` → 由指挥挑下一步。

#### `/ux-polish`：lint、修复、再 lint 的循环 + 清除 AI slop

- **做什么：** 先对本地 HTML 文件跑一个确定性的循环：lint，执行六遍幂等的打磨，再 lint，直到分数达到 90、进入平台期或跑满三轮（`--rounds` 可改上限）。默认情况下循环结果留在 `<file>.evolved.html`，原文件绝不改动。只有 `--loop-only` 或 `--fix` 会在确认工作区干净后替换原文件，而 65 分的质量门控会阻止未通过的结果替换原文件，除非加 `--force`；使用 `--brand-file` 时，品牌忠实度下限在每个出口都成立。接着是品味打磨：间距节奏、层级强化、AI slop 检测、token 一致性。它是 `/ux-lint` 的 LLM 驱动版，在品味问题上依靠你的判断。`--loop-only` 只跑循环；`--no-loop` 只做品味打磨；`--fix` 应用品味方面的发现。
- **何时使用：** 结构没问题但执行松散。"打磨一下"、"收紧一点"、"去掉 AI slop"、"做得高级点"、"别那么像 AI"、"间距不对劲"、"看起来很普通"、"需要更有品味"、"改到 90 分以上"、"弄到能上线"。
- **何时跳过：** 界面缺少核心功能（先修那个）；需要重新设计而不是打磨（用 `/ux-design`）；文案问题（用 `/ux-copy`）；动效问题（用 `/ux-motion`）；a11y 问题（用 `/ux-a11y`）。
- **调用方式：** `/ux-polish src/components/Hero.tsx`、`/ux-polish out/landing.html --css out/landing.css`、`/ux-polish out/landing.html --loop-only --rounds 5`。
- **输出：** 循环产出的 `<file>.evolved.html`（仅在 `--loop-only` 或 `--fix` 下替换原文件）、`--fix` 下更新后的代码、`.ux/last-evolve.json`、`.ux/decisions.jsonl` 中的一行，以及描述品味发现的 `.ux/last-polish.json`。
- **下接：** `/ux-lint` → 验证打磨效果保持住了。`/ux-a11y` → 重新检查无障碍。

### discovery 与叙事

#### `/ux-research`：研究计划 + 综合

- **做什么:** 计划模式:写访谈脚本、问卷、招募筛选器。综合模式(`--synthesize`):把访谈、分析、竞品站点、A/B 结果、客服工单消化为建议。派遣 `research-synthesizer`。
- **何时使用:** "计划一次研究"、"我需要访谈题"、"设计一份问卷"、"如何招募用户"、"用户测试计划"、"日记研究"、"偏好测试"、"fake door"、"smoke test"、"把我的访谈笔记综合一下"。
- **何时跳过:** 答案已有高置信度;低风险且可逆的决策;后端或基础设施。
- **调用方式:** `/ux-research --plan "loyalty wallet adoption in MENA"` 或 `/ux-research --synthesize interviews/*.md`。
- **输出:** 写入 `.ux/last-research.json`，研究计划,或综合后的主题 + 证据 + 建议。
- **下接：** `/ux-discover --frame` → 把研究发现整合进框定。`/ux-design` → 依据发现生成。`/ux-workshop` → 以研究为输入开一场工作坊。

#### `/ux-workshop`：五阶段设计思维工作坊

- **做什么:** 端到端主持一场 discovery / 设计思维工作坊。五个顺序阶段(探索 → 热度图 → 干系人地图 → 解决方案草图 → 行动方案)。计时;每阶段都有具体产出物。结束于一个决定,而不是"有趣的发现"。
- **何时使用:** 真问题、真参与者、真时间预算。"开一场工作坊"、"主持一次 discovery"、"来一次设计思维"、"我有干系人一小时,该干啥"、"项目启动"。
- **何时跳过：** 简报已经清晰且范围明确；独自头脑风暴（用 `/ux-design` 或 `/ux-discover --frame`）；团队正处在执行中段而非发现阶段。
- **调用方式:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`。
- **输出:** 写入 `.ux/last-workshop.json`，行动方案 + 各阶段产出物。
- **下接:** `/ux-design` → 执行行动方案;`/ux-research` → 补工作坊暴露的缺口;`/ux-case-study` → 把过程发表。

#### `/ux-case-study`：可发布的案例研究(Wfrah 编辑格式)

- **做什么：** 以纯黑白的编辑风格生成项目案例研究：Wfrah 字体、细线分隔、从 (A) 到 (G) 编号的章节代码、适配双语的版式。它是一份文档，而不是营销手册。读取 `.ux/last-frame.json`、`.ux/last-workshop.json`、`.ux/last-research.json`、`.ux/last-design.json`、`.ux/last-a11y.json`、`.ux/last-polish.json`、`.ux/last-recommendation.json`、`.ux/last-discovery.json`。
- **何时使用:** 发布后;经历一个明确里程碑后。"写一份案例研究"、"把这个项目做成案例"、"做收尾文档"、"把这工作发出来"、"作品集篇"。
- **何时跳过：** 项目缺少填充 (A) 到 (G) 各章节的数据；用户要的是营销落地页而不是案例研究（用 `/ux-design`）。
- **调用方式:** `/ux-case-study --format=html --slug=bashiti-loyalty`。
- **输出:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`。
- **下接:** 终端命令，通常是项目的句号。

### 指挥

#### `/ux-next`：工作流指挥(只读)

- **做什么:** 读取每个 `.ux/last-*.json`,指认下一步杠杆最大的命令。它是指挥,不是建造者。只读。
- **何时使用:** 在命令之间。"接下来该做什么"、"下一步是什么"、"替我决定"、"从这里往哪走"。
- **何时跳过:** `.ux/` 里没有先前报告;你心里已有具体的下一条命令。
- **调用方式:** `/ux-next`(无参数)或 `/ux-next --focus=a11y`。
- **输出:** 标准输出，建议的下一条命令 + 理由。
- **下接:** 它挑哪条就接哪条。

#### `/ux-expert`：咨询入口

- **做什么:** 在用户索取真人 UX 专家时,展示插件作者的联系方式。简短、直接、无营销话术。
- **何时使用:** "谁做的这个"、"我需要个 UX 专家"、"你做咨询吗"、"能雇个人帮我吗"、"这插件背后有人吗"。
- **何时跳过:** 用户问的是插件功能,不是咨询。
- **调用方式:** `/ux-expert`。
- **输出:** 一张含 LinkedIn / 邮箱 / 仓库的简短联系卡。

### 别名，将在 4.1 移除

七个 3.x 命令已并入上面的 18 个命令。它们的名称在一个版本内仍然可用：每个别名会说明自己迁到了哪里，然后用相同的参数运行新命令。

| 旧命令 | 现在 | 说明 |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | 同样的框定块，同样的 `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | MCP 工具 `ux_recommend` 不变 |
| `/ux-stats` | `/ux-init --stats` | 只读快照 |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | 别名保留旧的五轮上限；单独的 `/ux-polish` 跑满三轮即停 |
| `/ux-component` | `/ux-design --component` | 同样的 `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | 同样的 `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | 去掉 `--extract-only` 即按图片构建 |

### 命令串联图

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

## 5 个子代理

子代理是由命令派遣的角色化生成器。它们从不独立运行，由 `/ux-design`、`/ux-system`、`/ux-fix`、`/ux-research` 等命令调起。每个代理都有清晰的职责边界：它们**不**决定简报，只按简报执行。

### `frontend-engineer`

- **职责:** 生产级前端代码(React、Next.js、Vue、Blade+Alpine、原生 HTML、Astro),并保持反 AI-slop 纪律。
- **派遣者：** `/ux-design`（页面、组件、仪表盘和图片模式）、`/ux-fix`。
- **输入:** 简报 + 创意指引 + tokens(来自 `.ux/last-recommendation.json`)。
- **输出:** 与通用 AI 输出可区分的可运行代码。不出现紫色渐变、不居中 hero、不三张等大卡片、不用 Inter 当展示字、不出现"John Doe"、不放 emoji、不留 300ms 的默认值。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `motion-engineer`

- **职责:** 生产前端代码中的动效，Framer Motion、GSAP、CSS 动画。时长、缓动、编排、reduced-motion 兜底、性能纪律。
- **派遣者：** `/ux-design`（所有模式）、`/ux-motion --fix`。
- **输入:** 动效简报 + tokens + 来自 `data/motion-presets.json` 的 57 个预设。
- **输出:** 配得上自己位置的动效。永远包裹在 `prefers-reduced-motion` 兜底中。永远拿 Core Web Vitals 测一遍。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `copy-writer`

- **职责:** 真正会发布的文案，错误消息、空状态、CTA、loading 状态、成功消息、toast、辅助文字、表单标签、按钮文字。
- **派遣者：** `/ux-copy --fix`、`/ux-design`（所有模式）、`/ux-discover --frame`。
- **输入:** 嗓音档案(命名或粘贴) + 界面的文案。
- **输出:** 在界面各个状态间一致应用的生产级微文案,让产品听起来像一个产品,不像十个。禁忌:"表单存在错误"、"John Doe"、AI 式欢欣鼓舞的庆祝话术、笼统 CTA、空荡荡的空状态。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### `research-synthesizer`

- **职责:** 把研究输入(访谈、分析、竞品站点、A/B 结果、客服工单)消化为可执行的设计建议。
- **派遣者：** `/ux-research`、`/ux-workshop`、`/ux-discover --frame`。
- **输入:** 原始研究材料，访谈记录、导出文件、竞品 URL、客服聚类。
- **输出:** 主题、证据、建议。不替设计师设计答案，而是把可供设计的底料交给设计师。
- **工具:** `Read, Write, WebFetch, Bash, Glob, Grep`。

### `design-system-architect`

- **职责:** 完整的设计系统，tokens(颜色、字体、间距、动效、圆角、阴影)、基础文档、组件契约、暗色模式映射、主题化层。
- **派遣者：** `/ux-system`，以及尚无系统时的 `/ux-design --component`。
- **输入:** 品牌简报 + `.ux/last-recommendation.json`(风格 + 配色 + 字体搭配 + 动效预设)。
- **输出:** 一套连贯、立场鲜明、可上生产的系统,让下游代理无需重新决定根基就能构建。tokens JSON、基础 MD、组件契约、暗色映射。
- **工具:** `Read, Write, Edit, Bash, Glob, Grep`。

### 子代理派遣协议

当一个命令派遣子代理时,它会传入:

1. 简报 / 推荐(从 `.ux/` 加载)。
2. 与之相关的清单切片(例如 `frontend-engineer` 拿到选定的风格 + 配色 + 组件;`motion-engineer` 拿到选定的动效预设)。
3. 171 条反模式护栏（始终启用）。
4. 一个成功判据(产物必须做到什么)。

子代理返回:

1. 产物(代码、文档、系统)。
2. 一段理据(为什么这样选)。
3. 对照护栏的自检(他们验证了哪些规则)。

调用方命令随后会自动跑 `/ux-lint`,通过之后才宣告完成。

---

## 11 份数据清单

数据层就是大脑。每个命令都从中读取;引擎在其间合并;静态检查器对其扫描。所有文件都在 `data/` 下,条目用 `{_meta, entries}` 包装以做 schema 版本管理。

### `styles.json`：84 种设计风格

| 字段 | 描述 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`、`name`、`category`、`philosophy`、`when_to_use`、`when_to_skip`、`tokens`、`references`、`compatible_palettes`、`compatible_type_pairs`、`compatible_motion`、`compatible_industries`、`taste_score` |
| `categories` | Minimalist / Swiss、Brutalist、Editorial、Glassmorphism、Neumorphism、Bento、Skeuomorphic、Industrial、Maximalist、AI-Futurist、MENA-modern、Vaporwave 等 |
| `sample entry` | `swiss-international`，"网格即法律。字体承担重活。装饰即失败。" |

由 `/ux-discover`、`/ux-system`、`/ux-design` 使用。Schema：[data/SCHEMAS.md](data/SCHEMAS.md)。

### `palettes.json`：176 套配色

| 字段 | 描述 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`、`name`、`mode`(明/暗)、`tone`、`colors`(canvas、surface、ink、body、muted、primary、primary_active、hairline、success、warning、danger、accent)、`wcag_contrast_audit`、`compatible_industries` |
| `tones` | warm、editorial、magazine、clinical、playful、brutalist、monochrome、jewel-tone、MENA-warm、dev-tools-dark 等 |
| `sample entry` | `claude-warm-editorial`，明色,warm/editorial/magazine,canvas #faf9f5,primary #cc785c |

由 `/ux-discover`、`/ux-system` 使用。对比度按 AA / AAA 验证。Schema：[data/SCHEMAS.md](data/SCHEMAS.md)。

### `type-pairs.json`：70 组字体搭配

| 字段 | 描述 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`、`name`、`display`(family + weights + source + license + URL)、`body`、`mono`、`compatible_styles`、`taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`，Cormorant Garamond × Inter × JetBrains Mono |

所有字体家族都附有许可证 + 来源 URL。由 `/ux-discover`、`/ux-system` 使用。

### `components.json`：148 个组件

| 字段 | 描述 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`、`name`、`category`、`purpose`、`anatomy`、`states`、`tokens_used`、`motion`、`accessibility`、`compatible_styles`、`compatible_industries`、`code_skeleton` |
| `categories` | Navigation、Forms、Data Display、Feedback、Overlays、Layout、Content、Marketing、E-commerce、Auth、Dashboard、Charts、Empty States、Loading States、Error States |
| `sample entry` | `mega-nav-product-grid`，Mega Navigation、Product Grid，6 段解剖、4 个状态 |

这是我们最深的护城河。其他 Claude UX 插件没有发布过结构化的组件清单。

### `industries.json`：184 条行业规则

| 字段 | 描述 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`、`name`、`category`、`characteristics`、`audience_signals`、`recommended_styles`、`recommended_palettes`、`recommended_type_pairs`、`recommended_motion`、`regulatory_notes`、`regional_notes` |
| `categories` | Financial Services、Healthcare、Education、E-commerce、SaaS B2B、SaaS B2C、Developer Tools、Media、Gaming、Travel、Real Estate、MENA-specific 等 |
| `sample entry` | `fintech-neobank`，高信任、监管披露、余额/交易为主 UI、日活的移动优先 |

由推荐器（`/ux-discover`）用作首条并行检索轴。

### `chart-types.json`：35 种图表

| 字段 | 描述 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`category`、`when_to_use`、`when_to_skip`、`encoding`、`accessibility`、`data_shape`、`compatible_styles` |
| `categories` | Comparison、Time Series、Distribution、Composition、Relationship、Flow、Geographic |
| `sample entry` | `bar-vertical`，比较 4 到 15 个离散类别。x 轴位置表示类别；高度表示数值。 |

由 `/ux-design --dashboard` 和 `/ux-design --component`（图表实例）使用。

### `tech-stacks.json`：25 个技术栈

| 字段 | 描述 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`、`name`、`category`、`tier`、`languages`、`ssr`、`rsc`、`compatible_styling`、`scaffold_command`、`compatible_motion`、`gotchas` |
| `tiers` | production、prerelease、experimental |
| `sample entry` | `nextjs-15-app-router`，Next.js 15(App Router),TS/JS,SSR,RSC,兼容 Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

其他技术栈包括 Astro、SvelteKit、Remix、Nuxt 3、Solid Start、Qwik、Blade+Alpine、Hotwire、Phoenix LiveView、Hydrogen 2025。

### `ux-guidelines.json`：112 条具名 UX 法则

| 字段 | 描述 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`、`name`、`category`、`source`、`principle`、`application`、`examples`、`caveats`、`related_laws` |
| `categories` | Decision Cost、Attention、Memory、Motor Control、Visual Perception、Social、Emotional、Form、Error Handling、Onboarding、Empty State 等 |
| `sample entry` | `hicks-law`，决策时间随选项数量呈对数增长 |

由 `/ux-audit`(六镜头打分)与 `/ux-critique`(审美锚)使用。

### `motion-presets.json`：57 个动效预设

| 字段 | 描述 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`、`name`、`category`、`tokens`(duration_ms、easing、transform_from/to、opacity_from/to)、`stacks`(framer_motion、gsap、css)、`accessibility`(reduced-motion 兜底)、`when_to_use` |
| `categories` | Entry、Exit、Hover、Focus、Tap、Loading、Empty、Success、Error、Scroll-linked |
| `sample entry` | `fade-up-12px`，360ms,`cubic-bezier(0.16, 1, 0.3, 1)`,translateY(12px) → 0,opacity 0 → 1 |

每个预设都有一个 reduced-motion 变体。Framer Motion、GSAP 和纯 CSS 都提供开箱可用的代码。

### `anti-patterns.json`：171 条规则

| 字段 | 说明 |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`、`name`、`severity`（critical/high/medium/low）、`category`、`detection`（类型、模式、标志、范围，许多规则还有一项针对解析后文件的 `post` 检查）、`why`、`fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

完整规则列表见 [171 条反 AI slop 规则](#171-条反-ai-slop-规则检查器)。

### `brands/*.json`：160 份品牌规范

| 字段 | 描述 |
|---|---|
| `entries` | 160(再加一份 `_index.json` 列出全部) |
| `keys per entry` | `id`、`name`、`category`、`voice`、`tokens`(color、type、motion)、`design_principles`、`signature_moves`、`anti-moves`、`references` |
| `categories` | Developer Tools(36)、Consumer / Lifestyle / Retail(19)、Fintech / Crypto(14)、Editorial / Media(13)、AI / ML Platform(12)、Productivity / Collaboration(8)、Automotive(8) |

完整名单见[160 份 DESIGN.md 品牌规范](#160-份-designmd-品牌规范按类别)。

---

## 171 条反 AI slop 规则：检查器

ux-skill 自带一个确定性的检查器：每条规则都是一个模式，许多规则还会对解析后的 CSS 和标记再做一次检查，因此只有在规则指定的上下文中匹配才算数。**无 LLM。** **无 API。** **无网络。** 在典型的 Next.js 应用上，CI 中约 200ms 跑完。设置 `--fail-on high` 时，遇到 Critical / High 发现会以非零码退出。

规则来源于 `data/anti-patterns.json`（v2，首选），以 `references/foundations/anti-patterns.md` 作为后备（v1，bash）。附带两个二进制：`bin/ux-lint.py`（Python，快速，可扩展）和 `bin/ux-lint.sh`（Bash + perl-PCRE，用于没有 Python 的环境）。

### 按类别的规则

全部 171 条规则按类别、再按严重级别排列的完整目录，由 `data/anti-patterns.json` 生成在[英文 README](README.md#rules-by-category) 中；其中的规则 ID 和名称与检查器的输出一致。规则覆盖 A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2)。

### 检查器用法

**一次性扫描:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 份 DESIGN.md 品牌规范：按类别

真实的品牌。真实的设计语言。真实的 DESIGN.md 规范，不是通用配色。告诉插件"按 Stripe 的风格做个落地页",它会读取真实的品牌词汇表:嗓音量规、颜色 tokens、动效约定、签名手法、反向手法。

每个品牌都以一份结构化 JSON(`data/brands/<slug>.json`)外加一份散文参考(`references/brands/<slug>.md`)的形式发布。

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

### 为什么这件事很重要

另外 8 个热门 Claude UX 插件生成的是"现代极简"或"干净仪表盘"，同一种默认美学的变体。ux-skill 让你能要**Linear 的清晰**、**Stripe 的严肃**、**Apple 的克制**、**Tesla 的整块感**、**Notion 的亲和**、**Cursor 的渐变纪律**、**Raycast 的发丝密度**、**Claude 的暖色 editorial**，引擎会从品牌规范里取出对应的 tokens、嗓音、动效约定与签名手法。

---

## MCP 服务器：非对称的一着

ux-skill 提供一个 **Model Context Protocol 服务器**。运行 `ux-mcp`，引擎就变成一个常驻的 stdio 进程，任何支持 MCP 的宿主（Claude Desktop、Cursor、Windsurf 以及通用代理）都可以调用它。共 25 个工具：`ux_recommend`、`ux_system_detect`、`ux_lint`、`ux_styles`、`ux_palettes`、`ux_type_pairs`、`ux_components`、`ux_industries`、`ux_motion_presets`、`ux_anti_patterns`、`ux_brands`、`ux_landing_patterns`、`ux_persist_save`、`ux_persist_load`、`ux_stats`、`ux_image_extract`、`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`、`ux_system_build`、`ux_system_import`、`ux_system_enhance`、`ux_system_extend`、`ux_system_export`、`ux_contracts_check`。与斜杠命令使用相同的 Python 处理器、相同的数据清单、相同的确定性推荐器。

**为什么这是非对称的一着:** 排名前八的 Claude UX 技能(ui-ux-pro-max-skill、open-design、taste-skill、huashu-design、stitch、nothing-design、hallmark、material-3)没有一个提供 MCP 服务器。它们都被锁在 Claude Code 的插件运行时里。ux-skill 则能从任何讲 MCP 的宿主接入,包括从未听说过 Claude Code 插件的代理。

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

把你的客户端指向 `ux-mcp` 二进制即可。完整工具文档、JSON 示例,以及面向 Claude Desktop、Cursor、Windsurf 的逐客户端配置见 [docs/mcp.html](docs/mcp.html) 和 `commands/ux-mcp.md`。

---

## 面向 17 个 IDE 的安装器

`uxskill init`(或在 Claude Code 中执行 `/ux-init`)会自动识别你在哪个 IDE,并写入对应的产物。同一个 Python 引擎。同一套推荐。各 IDE 之间用不同的"胶水"对接。

| IDE / 工具 | 识别信号 | 安装的产物 |
|---|---|---|
| Claude Code | `.claude/` 或 `CLAUDE.md` | 位于 `.claude-plugin/plugin.json` 的插件清单 + 全部 18 个命令（以及 7 个别名）+ 全部 5 个子代理 |
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

## 使用案例：具体场景

八个真实场景。挑一个最贴近你处境的,改一下调用参数即可。

### 1. 在 Cursor 里做一个金融科技仪表盘

你在 Cursor 上做一个 MENA 新银行的仪表盘。装好插件、跑 discovery、跑 recommendation,然后生成仪表盘。

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

然后在 Cursor 里说:*"用 .ux/last-recommendation.json 里的推荐生成仪表盘界面"*。Cursor 读 `.cursorrules` 头,加载推荐,带着明确约束派遣一次仪表盘生成。

### 2. 在 Claude Code 里生成一份 Stripe 风格的落地页

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

三条命令,一张抛光后的界面,每个修复一个原子提交。

### 5. 设计一个 Linear 风格的命令面板

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

生成的组件用的是 Linear 真实的颜色 tokens、字体栈、动效约定与发丝密度，而不是"通用暗色 UI"。

### 6. 用 90 分钟和干系人开一场设计思维工作坊

你有一间会议室,5 个人,90 分钟。你希望他们带着行动方案离开,而不是带着"感觉"。

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

插件端到端地主持五个阶段(探索 → 热度图 → 干系人地图 → 解决方案草图 → 行动方案),计时,每阶段都有具体产出。最终输出是 `.ux/last-workshop.json`，行动方案,而不是只剩"有趣的发现"。

### 7. 发布后写一份可发表的案例研究

你发了会员钱包。你想要一篇作品集篇章。

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

这份案例研究是已完成、可发布的产物，不是草稿。纯黑白、editorial 字型、可直接上你的作品集。

### 8. 在非 AI 环境里跑 discovery(只要结构化录入)

你在做一份项目规划。你还不需要推荐，只需要一份结构化简报。

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

你可以把 JSON 交给团队,粘到 Notion 文档里,或者喂给其他 AI 工具。ux-skill 不止是引擎,也是一个结构化录入工具。

### 9. MASTER.md 持久化：把你的设计决策写进仓库

跑完 `/ux-discover`（或 `/ux-discover --recommend`）之后，把选定的风格 + 配色 + 字体 + 动效 + 组件 + 品牌范例 + 护栏保存为一份可读的 Markdown 文件，让团队能审查、对比（diff）、纳入版本控制。

```bash
python3 -m engine.cli.main persist save --project-root .
```

写出 `.ux/design-system/MASTER.md`(YAML frontmatter + 正文),并通过 `persist save-page` 为每个生成出的界面写出 `.ux/design-system/pages/<name>.md`。幂等，相同输入产出按字节完全一致的输出,所以在状态未变时重跑在 git 里就是个 no-op。

---

## 与其他方案的对比

简表如下。逐列对比详见 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

| 维度 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| 斜杠命令 | **18** | 1 | 19 | 1 | 1 | 多个 | 1 | 1 | 1 |
| 组件 | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| 动效预设 | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 品牌规范 | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 反模式规则 | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 安全的确定性检查器 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| 支持的 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery 关卡 | **10 字段** | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 | 隐式 |
| `.ux/` 状态链 | **是** | 否 | 否 | 否 | 否 | 否 | 否 | 否 | 否 |
| Star 数(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 坦诚评估

- **ui-ux-pro-max** 认知度更大,支持 18 个 IDE,在它的 CSV 上做了类 BM25 的检索。它没有组件清单、动效清单、品牌库或确定性检查器。
- **open-design** 拥有 19 个 skill + 预览,但只支持 Claude Code,而且没有反 slop 层。
- **hallmark** 在精神气质上最接近(也是反 slop),但它是单个 skill，没有引擎、没有清单、没有可串联的命令。
- **material-3-skill** 在你专门要 Material Design 3 时极佳。我们不在 MD3 上跟它较劲。

按维度的完整细节见 [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## 路线图

接下来（不绑定具体版本）：

- **Figma 样式**：阴影的效果样式、网格样式，以及绑定到字段变量的文本样式，写入在线文件。
- **组件映射**：把 Figma 组件及其变体映射到代码组件及其 props，并在交付过程中一直保留。
- **线上站点导入器**：读取一个已发布站点实际渲染出的系统，与文件导入器并列。
- **已构建系统的文档页**：以适合人阅读的方式呈现它的 token、角色和契约。

其他待办：

- **`uxskill lint --fix` 安全改写**：针对可机械修复的发现（button-no-type、img-no-alt 空字符串、移除 console-log-leak）。
- 在编辑器内直接显示 lint 发现的 **VS Code 扩展**。
- 覆盖六个技术栈的**按组件输出代码**（Next.js + React、Vue 3 + Nuxt、SvelteKit、Astro、Blade + Alpine、原生 HTML/CSS）。
- **品牌规范市场**：发布和发现社区的品牌规范。
- **自定义反模式规则**：发现和分享各项目在 `data/anti-patterns.local.json` 中定义的规则。
- **`uxskill plan`**：根据简报规划多页面站点，而不只是单个界面。

---

## 参与贡献

欢迎 issue 与 PR。三个高杠杆方向:

### 新增一条反模式规则

1. 编辑 `data/anti-patterns.json`，添加一条带 `id`、`name`、`severity`、`category`、`detection.pattern`、`detection.flags`、`detection.scope`、`evidence_template`、`fix`、`references` 的条目。
2. 在 `tests/linter/` 里加测试，一份会触发规则的文件,一份不会的。
3. 跑 `uxskill lint tests/linter/should-trigger/<rule>.tsx`，确认会被命中。再跑 `tests/linter/should-not-trigger/<rule>.tsx`，确认不会被命中。
4. 提一个 PR。

### 新增一份品牌规范

1. 创建 `data/brands/<slug>.json`,字段包含 `id`、`name`、`category`、`voice`、`tokens`、`design_principles`、`signature_moves`、`anti-moves`、`references`。
2. 在 `references/brands/<slug>.md` 添加对应散文。
3. 在 `data/brands/_index.json` 登记。
4. 提一个 PR。规范必须有一手出处(品牌实际的产品、公开的设计系统,或他们公开发布的 DESIGN.md)。

### 新增一个动效预设

1. 编辑 `data/motion-presets.json`，添加一条带 `id`、`name`、`category`、`tokens`、`stacks`(framer_motion、gsap、css)、`accessibility.reduced_motion_fallback`、`when_to_use` 的条目。
2. 该预设必须有 reduced-motion 变体。无一例外。
3. 提一个 PR。

### 流程

- 阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 了解完整流程。
- 阅读 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
- 新规则与品牌规范会按以下标准复核:一手出处、不过度拟合到单个项目、数据中不出现 emoji、在适用时的 RTL 安全行为。

---

## 许可证、作者、致谢

### 许可证

MIT。用它、fork 它、在它之上构建。如果它帮你少出货了一份 AI slop,请给仓库点个 star，这是成本最低的支持方式。

### 作者

**Laith Aljunaidy**：[Dot](https://thedotwallet.com) 的独立创始人,Dot 是一个 MENA 优先的会员平台。我打造 ux-skill,是为了让 AI 生成的前端不再千篇一律。

- LinkedIn:[linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- 邮箱:laith.aljunaidy.laith@gmail.com
- 仓库:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- 官网:[uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI:[pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm:[npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 致谢

- 感谢 Anthropic 团队提供了 Claude Code,以及让这一切可分发的 skill / 插件架构。
- 感谢 Nielsen Norman Group、Laws of UX(lawsofux.com)以及让 `data/ux-guidelines.json` 言之有据的 UX 研究社群。
- 感谢 `data/brands/` 里列出的每一个品牌，它们公开的设计系统是品牌规范的事实来源。
- 感谢原始的 v1 贡献者:那份一次成型的 Claude skill 是 v2 Python 引擎的种子。
- 感谢我们对比的那 8 个热门 Claude UX 插件，他们抬高了基准;这是我们的回答。

---

**ux-skill** · **v4.0.0** · 为让 Claude Code、Cursor、Windsurf 以及其他 AI 编程工具产出的前端不再被一眼识别为 AI 生成而打造。

> 给仓库点星:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · 通过 `pip install uxskill` 或 `npx uxskill init` 安装 · 浏览对比:[uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
