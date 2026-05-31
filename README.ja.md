[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · **日本語** · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — Claude Code、Cursor、その他すべての AI コーディングツールのためのデザイン知能エンジン

> **v3.1.0 安定版 — THE BRAIN.** AI コーディング向け最強の UX プラグイン。 12 個のクエリ可能な JSON マニフェスト(84 のスタイル、176 のパレット、70 のタイプペアリング、148 のコンポーネント、184 の業種、35 のチャートタイプ、57 のモーションプリセット、112 の UX ロー、152 のアンチパターンルール、25 の技術スタック、160 のブランド仕様)、25 のスラッシュコマンド、5 つのサブエージェント、そして決定論的な反 AI スロップリンターを備えた Python 推論コア。クロス IDE 対応:Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、Kiro、Cline、Continue、Aider、Zed、JetBrains AI、Pieces、Tabby、Tabnine、CodeWhisperer、Roo Cline に同梱されます。

> **ブランド名は `ux-skill`。** PyPI / npm のパッケージ名は `uxskill` のままです。GitHub リポジトリは [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill) にあります。

**サイト:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **すべての Claude UX プラグインとの比較:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.1.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-向けインストーラー)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-223_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### v3 の新機能

- **ブランド仕様はテンプレートではなく訓練データになります。** 160 のブランド仕様はレコメンダーが選ぶカタログではなくなり、シンセサイザーが蒸留する語彙になります。出力は呼び出しごとに新しくなります。
- **7 軸シンセサイザー**(warmth、contrast、density、geometry、formality、motion、type_personality)。ブリーフは決定論的に軸の値にマップされ、軸の値が新鮮な palette + タイポ + spacing + radius + motion トークンへとコンパイルされます。
- **3 つの自動振り分けモード** — `strict_brand`(単一ブランドの 100%)、`brand_anchor`(単一ブランド 70% + 兄弟ブランドから軸適応された 30%)、`pure_synthesis`(ブランド指定なし — 軸が一致する 8 例から蒸留)。
- **決定台帳がレコメンダーをリランクします。** `.ux/decisions.jsonl` が同じ `(industry, ui_type)` バケットでの過去の勝者で候補をリランクします。コールドスタートに安全。`lint_score >= 80` かつ `user_accepted = true` の決定のみカウントします。
- **軸相互作用マトリックス** — 競合軸間の明示的な衝突解決(dense + corporate → 4px、airy + corporate → 12px、soft + playful → 18px radius)。もうサイレントな場当たりルールはありません。
- **`/ux-evolve` 自動ループ** — スコア ≥ 90、プラトー、または 5 ラウンドまで lint → polish → re-lint。品質ゲートは 65。
- **3 つの新 MCP ツール**(15 → 18):`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`。
- **ローカル統計ダッシュボード** — `uxskill stats --html` が `.ux/stats.html` を書き、**あなたの**インストールが何を学んだかを示します。テレメトリなし、グローバル集約なし。
- **223 テスト通過。** オフライン。決定論的。LLM を呼ばない。

詳細は [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain) に。

### Star 履歴

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill とは

ux-skill は AI コーディングツールのための**デザイン知能エンジン**です。Python パッケージとして(`pip install uxskill`)、Claude Code プラグインとして、そして 17 IDE 向けマルチインストーラーとして動作します。エンジンはプロジェクトのブリーフ(業種、オーディエンス、トーン、必須項目、禁止事項、スタック、地域)を取り込み、推奨デザインシステム一式を返します:スタイル、パレット、タイプペア、モーションプリセット、コンポーネント、研究すべきブランド事例、そして守らねばならないアンチパターンのガードレール。推奨は決定論的です——同じ入力は常に同じ出力を生みます。

このプラグインはあなたと AI コーディングツールの間に座ります。Claude Code、Cursor、その他の AI アシスタントに「フィンテックのランディングページを作って」と頼むと、アシスタントは通常即興で作ります——そして結果は 5 秒で AI 生成と見抜かれます(紫から青のグラデーション、等大の 3 枚カード、ディスプレイサイズの Inter、推薦文の「John Doe」、デフォルト 300ms のトランジション、中央寄せのヒーロー、CTA で跳ねる矢印)。ux-skill は即興を**構造化された制約**で置き換えます:`/ux-discover` でブリーフを取り、`/ux-recommend` でシステムを選び、`/ux-design` でコードを生成し、`/ux-lint` でコミット前に 152 個の決定論的な反 AI スロップルールを通すことを検証します。

この README が正典のリファレンスです。すべてのコマンド、すべてのサブエージェント、すべてのデータマニフェスト、すべてのインストール経路、すべてのブランド仕様、すべてのアンチパターンカテゴリ——すべてここに記録されています。Claude Code のデザインプラグインを探している、または Cursor、Windsurf、Codex 向けの AI デザインツールを比較しているなら、これを最初から最後まで読み、[compare.html](https://uxskill.laithjunaidy.com/compare.html) と並べてご覧ください。

---

## 目次

1. [ブレイン — v3.0 とは何か](#ブレイン--v30-とは何か)
2. [クイックインストール](#クイックインストール)
3. [数字 — トップ 8 の Claude UX スキルとのライブ比較](#数字--トップ-8-の-claude-ux-スキルとのライブ比較)
4. [アーキテクチャ — 各部品がどう噛み合うか](#アーキテクチャ--各部品がどう噛み合うか)
5. [25 のスラッシュコマンド — 詳細リファレンス](#22-のスラッシュコマンド--詳細リファレンス)
6. [5 つのサブエージェント](#5-つのサブエージェント)
7. [12 のデータマニフェスト](#11-のデータマニフェスト)
8. [152 の反 AI スロップルール — リンター](#145-の反-ai-スロップルール--リンター)
9. [160 のブランド DESIGN.md 仕様 — カテゴリ別](#160-のブランド-designmd-仕様--カテゴリ別)
10. [MCP サーバー — 非対称な一手](#mcp-サーバー--非対称な一手)
11. [17 IDE 向けインストーラー](#17-ide-向けインストーラー)
12. [ユースケース — 具体的なシナリオ](#ユースケース--具体的なシナリオ)
13. [他の選択肢との比較](#他の選択肢との比較)
14. [ロードマップ](#ロードマップ)
15. [コントリビューション](#コントリビューション)
16. [ライセンス、作者、謝辞](#ライセンス作者謝辞)

---

## ブレイン — v3.0 とは何か

v3.1.0 は ux-skill 史上最大のアーキテクチャ的シフトです。レコメンダーはもうカタログからテンプレートを選びません — エンジンがブリーフごとに新鮮なデザイン言語を**合成**します。同じブリーフは常に同じ出力を生み(完全に決定論的)、しかし異なるブリーフごとに独自の新しいシステムが生まれます。ブランド仕様はテンプレートではなくなり、エンジンが語彙を学ぶ訓練データになります。システムは自身の履歴に目を持ち、フィードバックループをローカルで閉じ、LLM を一度も呼びません。

コンパイラーは**決定論的な 7 軸シンセサイザー**です — warmth、contrast、density、geometry、formality、motion、type_personality。すべてのブリーフが軸の値にマップされ、軸の値が新鮮な palette + タイポ + spacing + radius + motion トークンにコンパイルされます。モジュラータイポスケールは contrast から比を選びます(1.200 quiet / 1.250 balanced / 1.333 loud)。レイアウトプリミティブは構築によりレスポンシブ(`auto-fit minmax(min(N, 100%), 1fr)` + コンテナクエリ)。壊れたレイアウトは表現不可能なので発行できません。

自動振り分けの 3 モード:`strict_brand`(`reference_brands=[stripe] strict=True` → 100% Stripe トークン、最速パス);`brand_anchor`(`reference_brands=[stripe]` → 70% Stripe + 4 兄弟ブランドから軸適応の 30%);そして `pure_synthesis`(ブランド指定なし → 無限空間、軸が一致する 8 例を新しいデザイン言語に蒸留)。軸の衝突は文書化された**軸相互作用マトリックス**で解決されます — dense + corporate は 4px にコンパイル(density 勝ち、ブルームバーグ流派)、airy + corporate は 12px(formality 勝ち、ラグジュアリー)、soft + playful は 18px radius、sharp + corporate は 2px。実装に隠れた場当たりルールはありません。

**決定台帳**(`.ux/decisions.jsonl`、スキーマ `_v: 1` ロック)がフィードバックループを閉じます。レコメンダーは同じ `(industry, ui_type)` バケットでの過去の勝者により候補をリランクします。コールドスタートに安全 — 事前データが 3 件未満ならスキップ。`lint_score >= 80` かつ `user_accepted = true` の決定のみカウント。さらに `/ux-evolve` はスコア ≥ 90、プラトー、または 5 ラウンドまで lint → polish → re-lint を回し、65 を下回る出力は `--force` なしに拒否されます。結果として、各インストールは自身のコーパスで賢くなり、各実行はマシン間で再現可能になり、エンジンは完全にオフラインのままです。

---

## クイックインストール

3 つのインストール経路。あなたの環境に合うものを選んでください。

### 経路 1 — Claude Code マーケットプレイス(正典)

Claude Code に常駐しているなら、プラグインマーケットプレイスからインストールします:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

これで 25 のスラッシュコマンドと 5 つのサブエージェントが Claude Code セッションに接続されます。インストール後、`/ux-init` を実行してプロジェクト単位の `.ux/` 状態ディレクトリをセットアップし、Python エンジンが到達可能であることを検証してください。

### 経路 2 — pip(汎用)

Claude Code の外で作業している場合(Cursor、Windsurf、CLI、CI)、Python パッケージをインストールします:

```bash
pip install uxskill
uxskill init                       # IDE を自動検出し、対応するアーティファクトを配置
uxskill stats                      # マニフェスト件数を表示してインストールを検証
uxskill lint .                     # カレントディレクトリにリンターを実行
```

パッケージは CLI エントリポイントとして `ux` と `uxskill` の両方を公開します——同じバイナリです。

### 経路 3 — npx(Python 管理不要)

Python を直接管理したくない場合、npx ラッパーが `pipx` 経由で一切を起動します:

```bash
npx uxskill init                  # 初回実行時に pipx + uxskill をダウンロード
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### インストール検証

```bash
ux stats
# {
#   "version": "3.1.0-stable",
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
#     "anti-patterns": 145,
#     "brands": 160
#   }
# }
```

いずれかの件数が 0 を返したら、JSON ファイルが欠けています——[github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) に issue を立ててください。

---

## 数字 — トップ 8 の Claude UX スキルとのライブ比較

スター数の最終確認は `gh api` 経由で **2026-05-28**。ux-skill(Laith0003/ux-skill)は最新の参入者です——認知度では小さく、アーキテクチャでは深い。以下の比較は正直です:どこで負け、どこで勝つか。

| プラグイン | スター数 | アーキテクチャ | スラッシュコマンド | リンター(CI 対応) | ブランド仕様 | コンポーネント | モーションプリセット | 対応 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV、単一スキル | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 スキル + プレビュー | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + リサーチ裏付けの審美眼 | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 単一の 62 KB SKILL.md + スクリプト | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | MCP に接続されたスキルライブラリ | 複数 | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 単一美学スキル | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 反スロップデザインスキル | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 コンポーネント + 監査 | 1 | — | (MD3 のみ) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python エンジン + 12 マニフェスト + 25 コマンド + 5 サブエージェント + CI リンター** | **22** | **152 の正規表現ルール** | **160** | **148** | **57** | **17** |

### 負けているところ

- **認知度。** 彼らは数十万のスターを持っています。私たちは 14 です。スターを付けてください——最も安価な支援方法です。
- **ブランド認知。** ui-ux-pro-max と open-design は、日ではなく月単位で先行しています。
- **マーケティングの磨き込み。** スクリーンショット、デモ動画、見つけやすいランディングページがあります。私たちには徹底した README と質素なランディングしかありません。

### 勝っているところ

- **コンポーネントライブラリ:** 148 個のドキュメント化されたコンポーネント。解剖、ステート、使用 token、モーション仕様付き。他の 8 つはどれもコンポーネントマニフェストを同梱していません。
- **モーションプリセット:** 57 個のスタック対応エントリ(Framer Motion、GSAP、CSS)、reduced-motion フォールバック付き。他のどこもモーションマニフェストを同梱していません。
- **アンチパターンリンター:** 152 個の決定論的な正規表現ルール、CI で実行し Critical/High で非ゼロ終了。他のどこも決定論的リンターを同梱していません。
- **ブランド仕様:** 160 個の実在 DESIGN.md 仕様(Apple、Stripe、Linear、Figma、Tesla、BMW、Notion、Spotify、Airbnb、Vercel、Supabase、Cursor、Raycast、Claude ほか 96 件)。他のどこもブランドライブラリを同梱していません。
- **17 IDE 対応:** 同じエンジン、IDE ごとに違う糊。
- **25 のスラッシュコマンド:** discovery、生成、監査、lint、ポリッシュ、修正ループ、ケーススタディ、ワークショップ、コピー、モーション、a11y、ダッシュボード、コンダクター——完全に統合済み。

完全な列ごとの比較表は [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) で。

---

## アーキテクチャ — 各部品がどう噛み合うか

```
ux-skill (パッケージ名: uxskill)
│
├── data/                              脳 — クエリ可能な JSON マニフェスト
│   ├── styles.json                    84 のデザインスタイル + when/skip + tokens
│   ├── palettes.json                  176 のパレット(明/暗、コントラスト検証済み)
│   ├── type-pairs.json                70 の display × body × mono トリプレット
│   ├── components.json                148 のコンポーネント(解剖、ステート、モーション)
│   ├── industries.json                184 の業種ルール + オーディエンスシグナル
│   ├── chart-types.json               35 のチャートタイプ(when/skip、エンコーディング)
│   ├── tech-stacks.json               25 のスタック(Next、Astro、SvelteKit、Blade…)
│   ├── ux-guidelines.json             112 の名前付き UX ロー(Hick、Fitts、Miller…)
│   ├── motion-presets.json            57 のモーションプリセット(入場、退場、ホバー…)
│   ├── anti-patterns.json             152 の正規表現ルール(CI 対応リンターのソース)
│   └── brands/*.json                  160 のブランド DESIGN 仕様 + _index.json
│
├── engine/                            Python — 推論層
│   ├── synthesizer/                   v3 — 決定論的 7 軸コンパイラー
│   ├── decisions/                     v3 — .ux/decisions.jsonl 台帳 + レコメンダーのリランク
│   ├── recommender/                   5 並列検索のマージエンジン
│   ├── linter/                        決定論的な反スロップスキャナー
│   ├── discovery/                     10 フィールドの強制プロトコル
│   ├── generator/                     token + マニフェストエミッター
│   ├── installer/                     17 IDE 向けマルチインストーラー
│   └── cli/                           `ux` / `uxskill` エントリポイント
│
├── commands/                          25 の Claude Code スラッシュコマンド (.md)
│   ├── ux-init.md                     ブートストラップ
│   ├── ux-stats.md                    インベントリのスナップショット
│   ├── ux-discover.md                 10 フィールドのインテーク(ゲート)
│   ├── ux-recommend.md                旗艦 — 5 並列検索
│   ├── ux-lint.md                     決定論的リンター
│   ├── ux-design.md                   フロントエンドコード生成
│   ├── ux-component.md                単一コンポーネント生成
│   ├── ux-system.md                   完全なデザインシステム生成
│   ├── ux-dashboard.md                ダッシュボード画面生成
│   ├── ux-motion.md                   モーション処理 + 監査
│   ├── ux-audit.md                    6 レンズのデザイン監査
│   ├── ux-a11y.md                     WCAG 2.1 AA 監査
│   ├── ux-critique.md                 審美的講評(3 つの勝ち、3 つの負け、1 つの一手)
│   ├── ux-copy.md                     マイクロコピーの監査 + 書き換え
│   ├── ux-fix.md                      所見をアトミックなコミットとして適用
│   ├── ux-polish.md                   仕上げ + AI スロップの除去
│   ├── ux-frame.md                    4 フィールドのフレーミングブロック
│   ├── ux-research.md                 リサーチの計画 + 統合
│   ├── ux-workshop.md                 5 段階のデザインシンキングワークショップ
│   ├── ux-case-study.md               公開可能な Wfrah エディトリアル形式のケーススタディ
│   ├── ux-next.md                     ワークフローコンダクター(読み取り専用)
│   └── ux-expert.md                   コンサルティングのフック
│
├── agents/                            5 つのサブエージェント (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 ブランドボイスのマイクロコピー
│   ├── research-synthesizer.md        インタビュー + 分析 + 競合
│   └── design-system-architect.md     tokens / コンポーネント / 基盤
│
├── references/                        データの散文ソース + デモページ
│   ├── foundations/                   anti-patterns.md、原則、審美眼
│   ├── laws/                          UX ローの長文
│   ├── process/                       discovery-protocol.md(要)
│   ├── styles/                        スタイルごとの散文(anti-slop.md など)
│   ├── components/                    コンポーネントの長文
│   ├── output/                        出力ルーブリック
│   └── conditional/                   スタック別ガイダンス
│
├── bin/
│   ├── uxskill.mjs                    npx ラッパー -> Python エンジン
│   ├── ux-lint.py                     v2 リンター(優先)
│   └── ux-lint.sh                     v1 フォールバック(bash + perl-PCRE)
│
└── .ux/                               (プロジェクトごとに作成)
    ├── last-discovery.json            ブリーフのスナップショット
    ├── last-recommendation.json       選定システム
    ├── last-frame.json                フレーミングブロック
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### エンジンが実際にどう動くか

1. **入力。** ブリーフを提供します——`/ux-discover` 経由でインタラクティブに(10 フィールド)、または `ux recommend` にフラグを渡して非インタラクティブに。
2. **5 並列検索。** エンジンはマニフェスト全体に対して 5 つのルックアップを同時実行します:
   - **業種 → 推奨スタイル**(industries.json)
   - **スタイル → パレット + タイプ + モーション互換性**(styles.json)
   - **トーン × 必須項目 → パレットフィルター**(palettes.json)
   - **スタック → コンポーネント互換性 + モーションプリセット**(tech-stacks.json、motion-presets.json)
   - **禁止事項 + 地域 → ガードレール + ブランド事例の候補**(anti-patterns.json、brands/)
3. **マージ。** 決定論的なマージャーが候補をランク付けし、衝突を解決します(例:必須のダークモードはパレットモードを強制)、最終的に推奨システムを 1 つ提示します。
4. **出力。** 選定スタイル、選定パレット、選定タイプペア、上位 5 モーションプリセット、上位 12 コンポーネント、上位 5 ブランド事例、152 のアンチパターンガードレールすべて有効を含む JSON ドキュメント。加えて各選定の根拠ブロック。
5. **生成。** 下流コマンド(`/ux-design`、`/ux-component`、`/ux-system`、`/ux-dashboard`)が推奨を消費し、サブエージェント経由で実コードを生成します。
6. **検証。** `/ux-lint` が生成コードを 152 の正規表現ルールに対して再スキャンします。CI で Critical/High に当たると非ゼロ終了。

**Python が考える。HTML が見せる。Markdown が繋ぐ。**

---

## 25 のスラッシュコマンド — 詳細リファレンス

各コマンドは `commands/` 下の `.md` ファイルとして配布されており、`description`、`allowed-tools`、`triggers`、`when to use`、`when to skip`、`input`、`process`、`output state file` を持ちます。以下の説明は要約版です;完全なソースが正典の仕様です。

コマンドは 5 つのバケットに分類されます:**ブートストラップ & インベントリ**、**discovery & 推奨**、**生成**、**監査 & 検証**、**修正 & 仕上げ**、そして**コンダクター**。

### ブートストラップ & インベントリ

#### `/ux-init` — プロジェクトをブートストラップする

- **何をするか:** どの IDE を使っているか(`.claude/`、`.cursor/`、`.windsurf/` など)を検出し、対応するアーティファクトをインストールし、Python エンジンが到達可能であることを検証し、統計スナップショットを表示します。
- **使うタイミング:** 新規プロジェクトに初めてインストールするとき。ux-skill を使うプロジェクトを clone した後。`pip install --upgrade uxskill` 後。
- **スキップするタイミング:** すでにこのプロジェクトで実行済みで、何も変わっていない。
- **呼び出し方:** `/ux-init`(引数なし)または CLI から `uxskill init`。
- **出力:** IDE ごとのアーティファクト([17 IDE 向けインストーラー](#17-ide-向けインストーラー)参照)+ `.ux/` ディレクトリ + 標準出力サマリー。
- **次に繋がる:** 次は `/ux-discover`。

#### `/ux-stats` — データインベントリを表示する

- **何をするか:** バージョン + 12 データマニフェストのエントリ件数を表示し、何がインストールされているか検証できるようにします。
- **使うタイミング:** インストール後、アップグレード後、`/ux-recommend` が予想外の結果を返してマニフェストが不完全なのではと疑うとき。
- **スキップするタイミング:** 決してない——50ms の読み取り専用コマンドです。
- **呼び出し方:** `/ux-stats` または `uxskill stats`。
- **出力:** 標準出力への JSON(上記の [インストール検証](#インストール検証) 参照)。
- **次に繋がる:** 診断専用;下流には何も流しません。

### discovery & 推奨

#### `/ux-discover` — 強制関数(10 フィールドのインテーク)

- **何をするか:** どのプロジェクトも生成コマンドの前に通る必須の 10 フィールドインテーク。プロジェクトタイプ、オーディエンス、主要ゴール、トーン、必須項目、禁止事項、参照ブランド、スタック、地域、成功指標。**即興は禁止。** 禁止フレーズ(「モダン」「クリーン」)がユーザーに具体的な言葉を強います。
- **使うタイミング:** `/ux-design`、`/ux-component`、`/ux-system`、`/ux-dashboard` の前。以前のブリーフが古びたとき。
- **スキップするタイミング:** バグを直している(`/ux-fix`)。リンターパスだけ実行する(`/ux-lint`)。ブリーフが前回セッションから変わっていない。
- **呼び出し方:** `/ux-discover`。プラグインが質問し、あなたが答えます。
- **出力:** `.ux/last-discovery.json`(10 フィールドのブリーフ)を書き出します。
- **次に繋がる:** `/ux-recommend` → discovery を使ってスタイル + パレット + タイプ + モーション + コンポーネントを選ぶ。`/ux-design [追加ブリーフ]` → 推奨に基礎付けてフロントエンドコードを生成。`/ux-component <名前>` → discovery 制約に沿った単一コンポーネントを生成。

#### `/ux-recommend` — 旗艦の 5 並列検索エンジン

- **何をするか:** Python エンジンの 5 並列検索を 12 マニフェスト横断で実行し、マージされたデザインシステムを 1 つ返します。業種 → スタイル → パレット → タイプ → モーション + コンポーネント + ブランド事例 + ガードレール。
- **使うタイミング:** 新規プロジェクトをゼロから開始する。疲れた見た目の製品をピボットする。`/ux-design` や `/ux-component` の前の事前点検。
- **スキップするタイミング:** すでに `/ux-discover` を実行してブリーフを保存している——そのフローでは `/ux-recommend` は自動。1 つのバグを修正している(`/ux-fix` を使う)。lint だけ必要(`/ux-lint` を使う)。
- **呼び出し方(Claude Code):**
  ```
  /ux-recommend
  ```
  **呼び出し方(CLI):**
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
- **出力:** `.ux/last-recommendation.json` を書き出します — 選定スタイル、選定パレット、選定タイプペア、上位 5 モーションプリセット、上位 12 コンポーネント、上位 5 ブランド事例、152 のアンチパターンガードレールすべて有効、加えて根拠。
- **次に繋がる:** `/ux-design [ブリーフ]` → 推奨 token でフロントエンドコードを生成。`/ux-system` → 推奨から完全なデザインシステムを生成。`/ux-component <名前>` → 推奨スタイルで単一コンポーネントを生成。`/ux-lint` → 生成コードを検証。

### 生成

#### `/ux-design` — ブリーフから美しい、反スロップな画面を生成する

- **何をするか:** discovery ブリーフ + 推奨から完全なプロダクション級フロントエンドアーティファクト(ランディング、マーケティングサイト、アプリシェル)を生成します。反スロップと arsenal リファレンスからのクリエイティブディレクションのもと、`frontend-engineer` を派遣します。
- **使うタイミング:** 「~をデザインして」「~を作って」「ランディングページを生成して」「ダッシュボードを作って」「コンポーネントを作って」——自由形式の視覚成果物のリクエストすべて。
- **スキップするタイミング:** 構築ではなくレビューが欲しい(`/ux-audit` または `/ux-critique` を使う)。コンポーネント 1 つだけ欲しい(`/ux-component` を使う)。バックエンドやインフラの作業。
- **呼び出し方:** `/ux-design MENA のネオバンク向けフィンテックランディングを生成、暖色エディトリアルトーン、ダーク AA、紫グラデーション禁止`。
- **出力:** 生成されたコード(HTML / Blade / JSX / Vue / Astro)、加えて `.ux/last-design.json`。
- **次に繋がる:** `/ux-lint` → ガードレール検証。`/ux-polish` → 仕上げ。`/ux-a11y` → アクセシビリティ監査。`/ux-copy` → マイクロコピー監査。`/ux-fix` → 所見をアトミックコミットとして適用。

#### `/ux-component` — 単一コンポーネントを生成する

- **何をするか:** 仕様から単一のプロダクション級コンポーネント(ボタン、モーダル、ナビバー、サイドバー、カード、テーブル、フォーム、チャート)を生成します。4 種のインタラクションステートを完備、アクセシブル、ブランドに沿う。まず `.ux/last-recommendation.json` でコンポーネントを検索、フォールバックでマニフェストを直接クエリ。
- **使うタイミング:** 任意の単一要素リクエスト——「ボタンを作って」「価格カードを作って」「モーダルを作って」「ナビバーを追加して」「サイドバーをデザインして」「データテーブルが必要」「フォームを作って」「チャートコンポーネントを作って」。
- **スキップするタイミング:** ページ全体や複数セクションの画面(`/ux-design` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-component pricing-card-trio --brief="フィンテック、ダーク、等幅数字"`。
- **出力:** 生成されたコンポーネントコード、加えて `.ux/last-component.json`。
- **次に繋がる:** `/ux-lint` → 検証。`/ux-polish` → 締め。

#### `/ux-system` — 完全なスターターデザインシステムを生成する

- **何をするか:** デザインシステムがまだないプロジェクトに完全なスタータシステムを提案します — tokens(色、タイプ、空間、モーション、角丸、影)、基盤ドキュメント、コンポーネントコントラクト、ダークモードペアリング、テーマスイッチャー。`design-system-architect` を派遣。
- **使うタイミング:** 「デザインシステムがない」「システムを作って」「token を提案して」「テーマはどうあるべき」「DS をセットアップして」。
- **スキップするタイミング:** プロジェクトにすでにデザインシステムがある — その場合は既存システムに対して `/ux-component` を使う。バックエンドやインフラ。
- **呼び出し方:** `/ux-system`(まだなら discovery を先に実行)。
- **出力:** `tokens.json`、`foundations.md`、`components/*.md` のコントラクト、オプションで Tailwind / vanilla / SCSS の出力。チェーンのため `.ux/last-system.json` を書き出します。
- **次に繋がる:** `/ux-component` → 新システムに対して構築。`/ux-design` → 新 token で画面を生成。

#### `/ux-dashboard` — ダッシュボード専用生成

- **何をするか:** データ密度の規律を伴うダッシュボード — bento レイアウト、表組み用の等幅数字、スパークラインのパターン、カードの濫用回避、セマンティックなステート色、控えめなモーション。チャートを貼り付けたマーケサイトではありません。
- **使うタイミング:** 「ダッシュボードを作って」「admin パネルをデザインして」「メトリクスページを作って」「オペレーターコンソール」「分析ビュー」「KPI ボード」「監視画面」。
- **スキップするタイミング:** 統計付きのマーケランディング(`/ux-design` を使う)。1 つのウィジェットだけ(`/ux-component` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-dashboard`。
- **出力:** 生成されたダッシュボードコード + `.ux/last-dashboard.json`。
- **次に繋がる:** `/ux-lint`、`/ux-audit`、`/ux-a11y`。

#### `/ux-motion` — モーション処理

- **何をするか:** 画面のモーション層を生成します — デュレーション、イージング、振り付け、reduced-motion フォールバック、パフォーマンス規律。既存モーションを 5 次元(タイミング、イージング、意味、reduced-motion、パフォーマンス)で監査もします。
- **使うタイミング:** 「モーション確認」「アニメーション大丈夫?」「モーションを直して」「アニメーションをレビューして」「モーション監査」「モーションのパフォーマンスパス」。
- **スキップするタイミング:** 画面にモーションがない(`/ux-audit` または `/ux-polish` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-motion path/to/component.tsx`(監査モード)または `/ux-motion --generate hero-entry`(生成)。
- **出力:** 更新されたコード(生成モード)または `.ux/last-motion.json` レポート(監査モード)。
- **次に繋がる:** `/ux-fix` → モーションの所見を適用。`/ux-polish` → 締め。

### 監査 & 検証

#### `/ux-lint` — 決定論的な正規表現ベースのリンター(LLM なし、CI 安全)

- **何をするか:** あなたのコードに対して 152 の正規表現ルールを実行します。LLM 呼び出しなし。CI で Critical / High に当たると非ゼロ終了。ソース:`data/anti-patterns.json`。ルールカバレッジ:A11y(23)、コンテンツ(15)、レイアウト(13)、タイポ(10)、色(9)、品質(9)、ビジュアル(9)、モーション(8)、パフォーマンス(4)。
- **使うタイミング:** プリコミットフック。CI ゲート。`/ux-audit` のコストを払う前の大規模コードベースへの素早い初回パス。`/ux-design` や `/ux-component` の後の生成検証。
- **スキップするタイミング:** 修正ループが欲しい(リンターは報告のみ、編集しません — `/ux-polish --fix` か `/ux-fix` にチェーン)。審美的判断が欲しい(`/ux-critique` を使う)。
- **呼び出し方(slash):** `/ux-lint src/`。
- **呼び出し方(CLI):** `uxskill lint .` または `python3 bin/ux-lint.py .` または `bash bin/ux-lint.sh --ci --fail-on high`。
- **呼び出し方(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **出力:** 標準出力に所見(位置、ルール id、重大度、エビデンス)。クリーンなら終了コード 0、`--fail-on high` 設定時に Critical/High があれば非ゼロ。
- **次に繋がる:** `/ux-polish --fix` → 同パターンの LLM ドリブン対応物。`/ux-fix` → 所見を重大度順にコミットとして適用。`/ux-audit` → 6 レンズの完全な推論パス。`/ux-next` → コンダクターに決めさせる。

#### `/ux-audit` — 6 レンズのデザイン監査

- **何をするか:** 6 つのレンズ(明瞭さ、ヒエラルキー、アクセシビリティ、ボイス、モーション、審美眼)に対する構造化された意見付きレビューで、重大度タグ付きの所見を生成します。Polaris スタイルのレポート。まず `.ux/last-frame.json` を読みます — オーディエンスとアウトカムがすべての所見の重大度を錨にします。
- **使うタイミング:** 画面が存在し、擁護可能な批評が欲しい。「監査して」「UX をレビューして」「これは良い?」「何が壊れてる?」「徹底的に解剖して」。
- **スキップするタイミング:** 画面がまだ存在しない(`/ux-design` を使う)。1 レンズだけ欲しい(専用コマンドを使う:`/ux-a11y`、`/ux-copy`、`/ux-motion`、`/ux-polish`)。審美的意見が欲しい(`/ux-critique` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-audit https://example.com/pricing` または `/ux-audit src/components/Pricing.tsx`。
- **出力:** `.ux/last-audit.json` を書き出します — `findings` 配列で `{lens, severity, title, principle, evidence, fix}`、`severity_counts`、`dominant_lens`、`strategic_moves`。
- **次に繋がる:** `/ux-fix` → 所見を適用。`/ux-polish` → 仕上げ。`/ux-design` → 構造的な再設計が必要なら。

#### `/ux-a11y` — WCAG 2.1 AA 監査 + 一般礼節チェック

- **何をするか:** 構造化された WCAG 2.1 AA 監査に加え、自動ツールはパスするが実ユーザーを傷つけ続ける一般礼節チェック(フォーカスの可視性、エラーの具体性、モーション設定、キーボードトラップ、色依存)。
- **使うタイミング:** リリース前のアクセシビリティゲート。再設計後。「アクセシビリティチェック」「WCAG 監査」「これはアクセシブル?」「a11y レビュー」「スクリーンリーダーテスト」「キーボードナビ確認」。
- **スキップするタイミング:** ユーザー向けでない。バックエンドやインフラ。作業途中のラフ。
- **呼び出し方:** `/ux-a11y https://example.com`(ライブ URL 推奨 — 自動ツールとキーボードテストはライブでしか動作しません)。
- **出力:** `.ux/last-a11y.json` を書き出します — `findings` 配列で `{wcag_sc, sc_name, severity, title, evidence, fix, category}`、`beyond_wcag` 配列、`severity_counts`。
- **次に繋がる:** `/ux-fix` → 所見をコミットとして適用。`/ux-copy` → コピーパスの一環として alt テキストやフォームエラーの結線を修正。

#### `/ux-critique` — 審美的講評(3 つの勝ち、3 つの負け、1 つの戦略的一手)

- **何をするか:** デザイナーの意見 — 構造化監査ではない、重大度スコアではない、何が効いていて、何が効いていないかを名指しし、最も変化を生む 1 つの戦略的一手を示す、引き締まった意見付きの見解。
- **使うタイミング:** 「どう思う」「これは良い?」「批評して」「正直な見解」「雰囲気合ってる?」「これは私たちらしい?」「出して良い?」。
- **スキップするタイミング:** ユーザーが明示的に構造化監査を望む(`/ux-audit` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-critique https://example.com`。
- **出力:** `.ux/last-critique.json` を書き出します — 3 つの勝ち、3 つの負け、1 つの戦略的一手、加えて散文。
- **次に繋がる:** 講評が再設計を勧めるなら `/ux-design`。締め直しを勧めるなら `/ux-polish`。

#### `/ux-copy` — マイクロコピーの監査 + 書き換え

- **何をするか:** すべての見える文字列をボイスルーブリックに照らして評価し、before/after の書き換えを生成します。捕捉対象:「フォームにエラーがあります」(汎用)、「John Doe」(プレースホルダー)、AI 的にはしゃぐ祝賀的コピー、汎用 CTA、生気のない空ステート、役立たずのエラー。
- **使うタイミング:** 構造は正しいが言葉が弱い。「コピーをレビュー」「マイクロコピーを直して」「エラーメッセージが悪い」「これを書き直して」「文字列を引き締めて」「ボタンが汎用すぎる」「この空ステートが死んでる」。
- **スキップするタイミング:** レイアウト問題(`/ux-audit` または `/ux-polish` を使う)。アクセシビリティ起因のコピー問題(alt テキストなど。`/ux-a11y` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-copy src/views/checkout.blade.php`。
- **出力:** `.ux/last-copy.json` を書き出します — `strings` 配列で `{location, severity, before, after, notes}`、加えてルーブリックと翻訳が必要なロケール。
- **次に繋がる:** `/ux-fix` → 書き換えを適用。`/ux-a11y` → コピー修正後の再確認。

### 修正 & 仕上げ

#### `/ux-fix` — 所見をアトミックなコミットとして適用する

- **何をするか:** `.ux/` の最新レポート(audit、copy、a11y、motion、polish)を読み、作業ツリーを検証し、適切なサブエージェントを通じて所見をアトミックなコミットとして適用します。元コマンドを再実行して再検証します。
- **使うタイミング:** 監査クラスのコマンドを実行し所見をレビューした後。「所見を修正」「修正を適用」「修正ループを走らせる」「画面にパッチ」「変更を適用」「直して」。
- **スキップするタイミング:** `.ux/` に先行レポートがない。作業ツリーが汚れていてユーザーが stash/commit に同意していない。修正に機械的適用ではなくデザイン判断が必要(再設計のため `/ux-design` を使う)。
- **呼び出し方:** `/ux-fix`(どのレポートを修正するか自動検出)または `/ux-fix --from=last-a11y.json`。
- **出力:** 所見ごとのアトミックなコミット。元コマンドを再実行して `.ux/last-*.json` を更新。サマリーを表示。
- **次に繋がる:** `/ux-next` → コンダクターが次の一手を選ぶ。

#### `/ux-polish` — 仕上げ + AI スロップ除去

- **何をするか:** 余白のリズム、ヒエラルキーの鋭利化、AI スロップ検出、token の一貫性。`/ux-lint` の LLM ドリブン対応物 — 審美的判断はあなたの代わりに行います。
- **使うタイミング:** 構造は正しいが実装が緩い。「ポリッシュ」「引き締めて」「AI スロップを除去」「プレミアムにして」「AI っぽさを減らして」「余白がおかしい」「汎用に見える」「もっと品が欲しい」。
- **スキップするタイミング:** 画面が中核機能を欠く(まずそれを修正)。仕上げでなく再設計が必要(`/ux-design` を使う)。コピー問題(`/ux-copy` を使う)。モーション問題(`/ux-motion` を使う)。a11y 問題(`/ux-a11y` を使う)。
- **呼び出し方:** `/ux-polish src/components/Hero.tsx`。
- **出力:** 更新されたコード + 変更を記述した `.ux/last-polish.json`。
- **次に繋がる:** `/ux-lint` → 仕上げが保持されたか検証。`/ux-a11y` → アクセシビリティ再確認。

### discovery & 物語

#### `/ux-frame` — 4 フィールドのフレーミングブロック

- **何をするか:** 誰のためか、アウトカム、仮説、成功シグナルを構造化されたフレーミングブロックに収めます。デザインは行わない — 漠然としたリクエストを動くブリーフに変える 4 フィールドのインテーク。`/ux-discover` より軽い(4 フィールド vs 10)。
- **使うタイミング:** どのプロジェクト、スプリント、単発エンゲージメントの始点でも。会話が脱線した中盤で。「フレーミングして」「ブリーフは?」「プロジェクトをセットアップ」「フレーミング」。
- **スキップするタイミング:** 既にフレーミング済み(`.ux/last-frame.json` を確認)。フレーミング影響のない単発コンポーネント構築。バックエンドやインフラ。
- **呼び出し方:** `/ux-frame "MENA Bashiti パイロット向けロイヤルティウォレット"`。
- **出力:** `.ux/last-frame.json` を書き出します — `{audience, outcome, hypothesis, success_signal}`。
- **次に繋がる:** `/ux-discover` → フレームを 10 フィールドブリーフに拡張。`/ux-design` → フレームを錨に生成。

#### `/ux-research` — リサーチ計画 + 統合

- **何をするか:** 計画モード:インタビュースクリプト、サーベイ、リクルートのスクリーナーを書きます。統合モード(`--synthesize`):インタビュー、分析、競合サイト、A/B 結果、サポートチケットを推奨に消化します。`research-synthesizer` を派遣。
- **使うタイミング:** 「リサーチ研究を計画」「インタビューの質問が必要」「サーベイを設計」「ユーザーをどう募集」「ユーザーテスト計画」「ダイアリースタディ」「プリファレンステスト」「フェイクドア」「スモークテスト」「インタビューメモを統合」。
- **スキップするタイミング:** 答えが高い確信度で既知。低リスクで可逆的な決定。バックエンドやインフラ。
- **呼び出し方:** `/ux-research --plan "MENA ロイヤルティウォレット採用"` または `/ux-research --synthesize interviews/*.md`。
- **出力:** `.ux/last-research.json` を書き出します — リサーチプランか、統合されたテーマ + エビデンス + 推奨。
- **次に繋がる:** `/ux-frame` → 知見をフレームに統合。`/ux-design` → 知見から生成。`/ux-workshop` → リサーチを入力にワークショップを実行。

#### `/ux-workshop` — 5 段階のデザインシンキングワークショップ

- **何をするか:** discovery / デザインシンキングのワークショップを端から端まで進行します。5 つの順序段階(探索 → ヒートマップ → ステークホルダーマップ → 解決策スケッチ → ゲームプラン)。時間枠付き。段階ごとに具体的なアーティファクト。「興味深い発見」ではなく決定で終わります。
- **使うタイミング:** 真の問い、真の参加者、真の時間予算。「ワークショップを進行」「discovery を進行」「デザインシンキングをやろう」「ステークホルダーが 1 時間いる、何をする」「プロジェクトをキックオフ」。
- **スキップするタイミング:** ブリーフがすでに明確でスコープされている。単独でのブレスト(`/ux-design` か `/ux-frame` を使う)。チームが実行中で discovery にいない。
- **呼び出し方:** `/ux-workshop "ロイヤルティウォレットのピボット" --participants="2 PM、1 デザイナー、1 エンジニアリードと、1 顧客担当" --minutes=90`。
- **出力:** `.ux/last-workshop.json` を書き出します — ゲームプラン + 段階別アーティファクト。
- **次に繋がる:** `/ux-design` → ゲームプランを実行。`/ux-research` → ワークショップが浮かび上がらせたギャップを埋める。`/ux-case-study` → 旅路を公開。

#### `/ux-case-study` — 公開可能なケーススタディ(Wfrah エディトリアル形式)

- **何をするか:** 純モノクロのエディトリアル形式でプロジェクトケーススタディを生成します — Wfrah タイポ、ヘアライン区切り、(A)–(G) 番号付きセクションコード、バイリンガル対応レイアウト。ドキュメントであり、マーケのパンフレットではありません。`.ux/last-frame.json`、`.ux/last-workshop.json`、`.ux/last-research.json`、`.ux/last-design.json`、`.ux/last-a11y.json`、`.ux/last-polish.json`、`.ux/last-recommendation.json`、`.ux/last-discovery.json` から読み込みます。
- **使うタイミング:** ローンチ後。個別マイルストーン後。「ケーススタディを書いて」「このプロジェクトをケーススタディに」「まとめドキュメントを作って」「この仕事を公開して」「ポートフォリオ作品」。
- **スキップするタイミング:** プロジェクトに (A)–(G) を埋めるデータがない。マーケランディングが欲しい、ケーススタディではない(`/ux-design` を使う)。
- **呼び出し方:** `/ux-case-study --format=html --slug=bashiti-loyalty`。
- **出力:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`。
- **次に繋がる:** ターミナルコマンド — 通常はプロジェクトの終止符。

### コンダクター

#### `/ux-next` — ワークフローコンダクター(読み取り専用)

- **何をするか:** すべての `.ux/last-*.json` を読み、最もレバレッジの高い次のコマンドを指名します。コンダクター、ビルダーではない。読み取り専用。
- **使うタイミング:** コマンドの合間。「次は何をすべき」「次の一手は」「私の代わりに決めて」「ここからどこへ」。
- **スキップするタイミング:** `.ux/` に先行レポートがない。具体的な次のコマンドがすでにある。
- **呼び出し方:** `/ux-next`(引数なし)または `/ux-next --focus=a11y`。
- **出力:** 標準出力 — 推奨する次のコマンド + 根拠。
- **次に繋がる:** 選ばれたコマンドへ。

#### `/ux-expert` — コンサルティングフック

- **何をするか:** ユーザーが実在の UX 専門家を求めるとき、プラグイン作者の連絡先を表示します。簡潔、直接、マーケなし。
- **使うタイミング:** 「これは誰が作った」「UX エキスパートが必要」「コンサルティングはやる?」「これで誰か雇えるか」「このプラグインの背後に人はいる?」。
- **スキップするタイミング:** ユーザーがプラグインの機能を尋ねている、コンサルティングでない。
- **呼び出し方:** `/ux-expert`。
- **出力:** LinkedIn / メール / リポジトリの簡潔なコンタクトカード。

### コマンドチェーンのグラフ

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4 フィールドのフレーミングブロック
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10 フィールドインテーク(強制ゲート)
                  └────────────┬─────────┘
                               │ .ux/last-discovery.json に書き込み
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 並列検索 -> マージされたシステム
                  └────────────┬─────────┘
                               │ .ux/last-recommendation.json に書き込み
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ .ux/last-<surface>.json に書き込み
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ .ux/last-<lens>.json に書き込み
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  所見をコミットとして適用
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  公開可能なアーティファクト
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  コンダクター — 読み取り専用
                  │  /ux-expert          │  コンサルティングフック
                  └──────────────────────┘
```

---

## 5 つのサブエージェント

サブエージェントはコマンドが派遣する役割特化型のジェネレーターです。単独で実行されません — `/ux-design`、`/ux-component`、`/ux-system`、`/ux-fix`、`/ux-research` などから呼ばれます。各エージェントには明確な責任境界があります:ブリーフを決めるのではなく、ブリーフに対して実行します。

### `frontend-engineer`

- **担当:** プロダクション級フロントエンドコード(React、Next.js、Vue、Blade+Alpine、純 HTML、Astro)を反 AI スロップの規律で。
- **派遣元:** `/ux-design`、`/ux-component`、`/ux-dashboard`、`/ux-fix`。
- **入力:** ブリーフ + クリエイティブディレクション + tokens(`.ux/last-recommendation.json` から)。
- **出力:** 汎用 AI 出力と区別できる動くコード。紫グラデーションなし、ヒーロー中央寄せなし、等大 3 カードなし、ディスプレイサイズの Inter なし、「John Doe」なし、絵文字なし、300ms デフォルトなし。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### `motion-engineer`

- **担当:** プロダクションフロントエンドコード内のモーション — Framer Motion、GSAP、CSS アニメーション。デュレーション、イージング、振り付け、reduced-motion フォールバック、パフォーマンス規律。
- **派遣元:** `/ux-design`、`/ux-motion --fix`、`/ux-component`。
- **入力:** モーションブリーフ + tokens + `data/motion-presets.json` から 57 のモーションプリセット。
- **出力:** その場所を勝ち取るモーション。常に `prefers-reduced-motion` フォールバックで包む。常に Core Web Vitals に対してテスト。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### `copy-writer`

- **担当:** 出荷される文字列 — エラーメッセージ、空ステート、CTA、ローディングステート、成功メッセージ、トースト、ヘルパーテキスト、フォームラベル、ボタンテキスト。
- **派遣元:** `/ux-copy --fix`、`/ux-design`、`/ux-frame`、`/ux-component`。
- **入力:** ボイスプロファイル(名前指定または貼り付け) + 画面の文字列。
- **出力:** 画面のすべてのステート横断で一貫適用されるプロダクションマイクロコピーで、製品が 10 個ではなく 1 つに聞こえる。禁止:「フォームにエラーがあります」「John Doe」、AI 的にはしゃぐ祝賀コピー、汎用 CTA、生気のない空ステート。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### `research-synthesizer`

- **担当:** リサーチ入力(インタビュー、分析、競合サイト、A/B 結果、サポートチケット)を実行可能なデザイン推奨に消化する。
- **派遣元:** `/ux-research`、`/ux-workshop`、`/ux-frame`。
- **入力:** 生のリサーチ素材 — トランスクリプト、エクスポート、競合 URL、サポートクラスター。
- **出力:** テーマ、エビデンス、推奨。答えをデザインしない — デザイナーがデザインするための基層を渡します。
- **ツール:** `Read, Write, WebFetch, Bash, Glob, Grep`。

### `design-system-architect`

- **担当:** 完全なデザインシステム — tokens(色、タイプ、空間、モーション、角丸、影)、基盤ドキュメント、コンポーネントコントラクト、ダークモードペアリング、テーマ層。
- **派遣元:** `/ux-system`、システムが存在しないとき `/ux-component` から。
- **入力:** ブランドブリーフ + `.ux/last-recommendation.json`(スタイル + パレット + タイプペア + モーションプリセット)。
- **出力:** 一貫性、立場、プロダクション準備が揃ったシステムで、下流エージェントが基礎を再決定せず構築できる。tokens JSON、基盤 MD、コンポーネントコントラクト、ダークモードマッピング。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### サブエージェント派遣プロトコル

コマンドがサブエージェントを派遣するとき、渡すもの:

1. ブリーフ / 推奨(`.ux/` からロード)。
2. 関連するマニフェストスライス(例:`frontend-engineer` は選定スタイル + パレット + コンポーネントを得る;`motion-engineer` は選定モーションプリセットを得る)。
3. 152 のアンチパターンガードレール(常に有効)。
4. 成功基準(アーティファクトは何を満たすべきか)。

サブエージェントが返すもの:

1. アーティファクト(コード、ドキュメント、システム)。
2. 根拠ブロック(なぜこの選択か)。
3. ガードレールへの自己チェック(どのルールを検証したか)。

呼び出し側のコマンドは完了を宣言する前に自動で `/ux-lint` を実行します。

---

## 12 のデータマニフェスト

データ層が脳です。すべてのコマンドはそこから読み、エンジンはそれを横断してマージし、リンターはそれに対してスキャンします。すべてのファイルは `data/` 下にあり、エントリを `{_meta, entries}` で包んでスキーマバージョニングを行います。

### `styles.json` — 84 のデザインスタイル

| フィールド | 説明 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`、`name`、`category`、`philosophy`、`when_to_use`、`when_to_skip`、`tokens`、`references`、`compatible_palettes`、`compatible_type_pairs`、`compatible_motion`、`compatible_industries`、`taste_score` |
| `categories` | Minimalist / Swiss、Brutalist、Editorial、Glassmorphism、Neumorphism、Bento、Skeuomorphic、Industrial、Maximalist、AI-Futurist、MENA-modern、Vaporwave など |
| `sample entry` | `swiss-international` — 「グリッドは法。タイプが重労働をこなす。装飾は失敗。」 |

使用:`/ux-recommend`、`/ux-system`、`/ux-design`。スキーマ:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `palettes.json` — 176 のカラーパレット

| フィールド | 説明 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`、`name`、`mode`(明/暗)、`tone`、`colors`(canvas、surface、ink、body、muted、primary、primary_active、hairline、success、warning、danger、accent)、`wcag_contrast_audit`、`compatible_industries` |
| `tones` | warm、editorial、magazine、clinical、playful、brutalist、monochrome、jewel-tone、MENA-warm、dev-tools-dark など |
| `sample entry` | `claude-warm-editorial` — 明、warm/editorial/magazine、canvas #faf9f5、primary #cc785c |

使用:`/ux-recommend`、`/ux-system`。コントラストは AA / AAA で検証済み。スキーマ:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `type-pairs.json` — 70 のタイプペアリング

| フィールド | 説明 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`、`name`、`display`(family + weights + source + license + URL)、`body`、`mono`、`compatible_styles`、`taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

すべてのファミリーにライセンス + ソース URL があります。`/ux-recommend`、`/ux-system` で使用。

### `components.json` — 148 のコンポーネント

| フィールド | 説明 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`、`name`、`category`、`purpose`、`anatomy`、`states`、`tokens_used`、`motion`、`accessibility`、`compatible_styles`、`compatible_industries`、`code_skeleton` |
| `categories` | Navigation、Forms、Data Display、Feedback、Overlays、Layout、Content、Marketing、E-commerce、Auth、Dashboard、Charts、Empty States、Loading States、Error States |
| `sample entry` | `mega-nav-product-grid` — Mega Navigation、Product Grid — 6 パーツの解剖、4 ステート |

これが私たちの最大の堀です。他の Claude UX プラグインは構造化コンポーネントマニフェストを同梱していません。

### `industries.json` — 184 の業種ルール

| フィールド | 説明 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`、`name`、`category`、`characteristics`、`audience_signals`、`recommended_styles`、`recommended_palettes`、`recommended_type_pairs`、`recommended_motion`、`regulatory_notes`、`regional_notes` |
| `categories` | Financial Services、Healthcare、Education、E-commerce、SaaS B2B、SaaS B2C、Developer Tools、Media、Gaming、Travel、Real Estate、MENA-specific など |
| `sample entry` | `fintech-neobank` — 高信頼、規制開示、残高/取引が主 UI、日次利用のモバイル優先 |

`/ux-recommend` が最初の並列検索軸として使用。

### `chart-types.json` — 35 のチャートタイプ

| フィールド | 説明 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`category`、`when_to_use`、`when_to_skip`、`encoding`、`accessibility`、`data_shape`、`compatible_styles` |
| `categories` | Comparison、Time Series、Distribution、Composition、Relationship、Flow、Geographic |
| `sample entry` | `bar-vertical` — 4–15 の離散カテゴリを比較。x 軸の位置がカテゴリに、高さが値にマッピング。 |

`/ux-dashboard`、`/ux-component`(チャートインスタンス)で使用。

### `tech-stacks.json` — 25 のスタック

| フィールド | 説明 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`、`name`、`category`、`tier`、`languages`、`ssr`、`rsc`、`compatible_styling`、`scaffold_command`、`compatible_motion`、`gotchas` |
| `tiers` | production、prerelease、experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15(App Router)、TS/JS、SSR、RSC、Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css と互換 |

他のスタックは Astro、SvelteKit、Remix、Nuxt 3、Solid Start、Qwik、Blade+Alpine、Hotwire、Phoenix LiveView、Hydrogen 2025 など。

### `ux-guidelines.json` — 112 の名前付き UX ロー

| フィールド | 説明 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`、`name`、`category`、`source`、`principle`、`application`、`examples`、`caveats`、`related_laws` |
| `categories` | Decision Cost、Attention、Memory、Motor Control、Visual Perception、Social、Emotional、Form、Error Handling、Onboarding、Empty State など |
| `sample entry` | `hicks-law` — 意思決定時間は提示された選択肢数に対数的に増加する |

`/ux-audit`(6 レンズ採点)と `/ux-critique`(審美の錨)で使用。

### `motion-presets.json` — 57 のモーションプリセット

| フィールド | 説明 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`、`name`、`category`、`tokens`(duration_ms、easing、transform_from/to、opacity_from/to)、`stacks`(framer_motion、gsap、css)、`accessibility`(reduced-motion フォールバック)、`when_to_use` |
| `categories` | Entry、Exit、Hover、Focus、Tap、Loading、Empty、Success、Error、Scroll-linked |
| `sample entry` | `fade-up-12px` — 360ms、`cubic-bezier(0.16, 1, 0.3, 1)`、translateY(12px) → 0、opacity 0 → 1 |

各プリセットに reduced-motion バリアントがあります。Framer Motion、GSAP、純 CSS 向けのスタック対応コード。

### `anti-patterns.json` — 152 の正規表現ルール

| フィールド | 説明 |
|---|---|
| `entries` | 152 |
| `keys per entry` | `id`、`name`、`severity`(critical/high/medium/low)、`category`、`detection`(type、pattern、flags、scope)、`evidence_template`、`fix`、`references` |
| `categories` | A11y(23)、Content(15)、Layout(13)、Typography(10)、Color(9)、Quality(9)、Visual(9)、Motion(8)、Performance(4) |

完全なルール一覧は [152 の反 AI スロップルール](#145-の反-ai-スロップルール--リンター)。

### `brands/*.json` — 160 のブランド仕様

| フィールド | 説明 |
|---|---|
| `entries` | 160(さらに全リストを示す `_index.json`) |
| `keys per entry` | `id`、`name`、`category`、`voice`、`tokens`(color、type、motion)、`design_principles`、`signature_moves`、`anti-moves`、`references` |
| `categories` | Developer Tools(36)、Consumer / Lifestyle / Retail(19)、Fintech / Crypto(14)、Editorial / Media(13)、AI / ML Platform(12)、Productivity / Collaboration(8)、Automotive(8) |

完全な一覧は [160 のブランド DESIGN.md 仕様](#160-のブランド-designmd-仕様--カテゴリ別)。

---

## 152 の反 AI スロップルール — リンター

ux-skill は決定論的な正規表現ベースのリンターを同梱します。**LLM なし。** **API なし。** **ネットワークなし。** 典型的な Next.js アプリで CI で ~200ms で実行されます。`--fail-on high` 設定時、Critical / High に当たると非ゼロ終了。

ルールは `data/anti-patterns.json`(v2 が優先)から取得され、`references/foundations/anti-patterns.md`(v1 bash)がフォールバック。2 つのバイナリ:`bin/ux-lint.py`(Python、高速、拡張可能)と `bin/ux-lint.sh`(Bash + perl-PCRE、Python のない環境向け)。

### カテゴリ別ルール

#### タイポグラフィ(3 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| high | `inter-as-display` | Inter をディスプレイフォントとして使用 |
| medium | `hero-text-arbitrary-90px` | 任意のヒーロー文字サイズ |
| low | `font-system-only` | システムフォントスタックのみで指定タイプフェイスなし |

#### 色(6 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| high | `purple-to-blue-gradient` | デフォルトの紫から青の AI グラデーション |
| high | `dark-text-on-dark-card` | カード上の低コントラストテキスト |
| medium | `gradient-text-rainbow` | 多段グラデーションテキスト |
| medium | `card-glow-purple-shadow` | カード上の紫グロー影 |
| medium | `gradient-mesh-purple-pink` | ヒーローの紫-ピンクメッシュグラデーション |
| low | `tailwind-color-named-vague` | セマンティック token のない命名 Tailwind カラー |

#### レイアウト(5 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| high | `three-equal-card-grid` | 並ぶ等大 3 カード |
| medium | `centered-everything-hero` | 中央寄せのヒーロー構成 |
| medium | `avatar-stack-overlapping` | 汎用的に重なるアバタースタック |
| low | `pill-rounded-full-everywhere` | すべてに適用された `rounded-full` |
| low | `nav-equal-hamburger-desktop` | デスクトップ上のハンバーガーメニュー |

#### コンテンツ(5 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| high | `lorem-ipsum-leak` | 出荷コード中の Lorem ipsum |
| high | `emoji-in-ui` | UI 要素としての絵文字 |
| high | `icon-emoji-stamp` | アイコンスタンプとしての絵文字 |
| high | `testimonial-fake-five-stars` | ハードコードされた五つ星のお客様の声 |
| medium | `fake-name-john-doe` | 汎用プレースホルダー名 |

#### モーション(3 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | CTA で跳ねる矢印 |
| low | `timing-300ms-default` | デフォルトの 300ms トランジションタイミング |
| low | `cubic-bezier-material-only` | どこでも Material デフォルトのイージング |

#### A11y(6 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| high | `inline-svg-no-aria` | aria-label も aria-hidden もない SVG |
| high | `img-no-alt` | alt 属性のない画像 |
| high | `link-onclick-no-href` | onClick はあるが href のないアンカー |
| medium | `button-no-type` | type 属性のないボタン |
| medium | `heading-skip-h1-h3` | 飛び級の見出しレベル |
| medium | `infinite-scroll-no-pagination` | キーボードフォールバックのない無限スクロール |

#### 品質(6 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| high | `console-log-leak` | コンポーネントコード中の `console.log` |
| medium | `inline-style-attribute` | インライン style 属性 |
| medium | `any-type-leak` | TypeScript `any` 型 |
| medium | `arbitrary-z-index-9999` | 雑な z-index 値 |
| low | `shadcn-default-everywhere` | shadcn デフォルト token のブロックそのまま |
| low | `todo-fixme-comment` | 出荷コード中の TODO や FIXME |

#### ビジュアル(1 ルール)

| 重大度 | ルール ID | 名前 |
|---|---|---|
| low | `blur-bg-only-decoration` | ガラス表面のない backdrop blur |

### リンターの使用

**単発スキャン:**

```bash
uxskill lint .
# または
python3 bin/ux-lint.py src/
# または
bash bin/ux-lint.sh src/
```

**CI ゲート(GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**プリコミットフック:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**出力(サンプル):**

```
─── /ux-lint report ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidence: bg-gradient-to-br from-purple-500 to-blue-500
  fix: replace with the recommended palette's primary gradient or remove gradient

src/components/Pricing.tsx:12  [high] three-equal-card-grid
  evidence: grid grid-cols-3 gap-6 (3 equal Card children)
  fix: feature one card; flank with two reduced-emphasis cards

3 files scanned · 2 high · 0 medium · 0 low · exit 1
Recommended next: /ux-polish --fix (LLM-driven, addresses both lintable and aesthetic findings)
```

---

## 160 のブランド DESIGN.md 仕様 — カテゴリ別

本物のブランド。本物のデザイン言語。本物の DESIGN.md 仕様 — 汎用パレットではありません。プラグインに「Stripe のスタイルでランディングを作って」と頼むと、実際のブランドボキャブラリを読みます:ボイスルーブリック、カラー token、モーション規約、シグネチャムーブ、アンチムーブ。

各ブランドは構造化された JSON(`data/brands/<slug>.json`)と散文リファレンス(`references/brands/<slug>.md`)として同梱されます。

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

### なぜこれが重要か

他の 8 つの人気 Claude UX プラグインは「モダンミニマル」や「クリーンダッシュボード」 — 同じデフォルト美学のバリアントを生成します。ux-skill は **Linear の明瞭さ**、**Stripe の真剣さ**、**Apple の抑制**、**Tesla のモノリス感**、**Notion の親しみ**、**Cursor のグラデーション規律**、**Raycast のヘアライン密度**、**Claude の暖色エディトリアル** を要求でき、エンジンはブランド仕様から正しい token、ボイス、モーション規約、シグネチャムーブを引き出します。

---

## MCP サーバー — 非対称な一手

ux-skill は **Model Context Protocol サーバー** を同梱します。`ux-mcp` を実行するとエンジンは長期実行の stdio プロセスになり、任意の MCP 対応ホスト — Claude Desktop、Cursor、Windsurf、汎用エージェント — から呼び出せます。14 のツール:`ux_recommend`、`ux_lint`、`ux_styles`、`ux_palettes`、`ux_type_pairs`、`ux_components`、`ux_industries`、`ux_motion_presets`、`ux_anti_patterns`、`ux_brands`、`ux_landing_patterns`、`ux_persist_save`、`ux_persist_load`、`ux_stats`。スラッシュコマンドが使うのと同じ Python ハンドラ、同じデータマニフェスト、同じ決定論的レコメンダー。

**なぜこれが非対称な一手か:** トップ 8 の Claude UX スキル(ui-ux-pro-max-skill、open-design、taste-skill、huashu-design、stitch、nothing-design、hallmark、material-3)はどれも MCP サーバーを同梱していません。Claude Code のプラグインランタイムに閉じ込められています。ux-skill は MCP を話す任意のホストから到達可能で、Claude Code プラグインを聞いたこともないエージェントからも届きます。

```bash
pip install 'uxskill[mcp]'             # mcp はオプトインの extra
ux-mcp                                  # stdio JSON-RPC サーバーが起動
```

クライアントを `ux-mcp` バイナリに向けてください。完全なツールドキュメント、JSON 例、Claude Desktop、Cursor、Windsurf のクライアント別設定は [docs/mcp.html](docs/mcp.html) と `commands/ux-mcp.md` に。

---

## 17 IDE 向けインストーラー

`uxskill init`(Claude Code 内では `/ux-init`)はどの IDE を使っているか自動検出し、正しいアーティファクトを書き出します。同じ Python エンジン。同じ推奨。IDE ごとに違う糊。

| IDE / ツール | 検出シグナル | インストールされるアーティファクト |
|---|---|---|
| Claude Code | `.claude/` または `CLAUDE.md` | `.claude-plugin/plugin.json` のプラグインマニフェスト + 全 25 コマンド + 全 5 サブエージェント |
| Cursor | `.cursor/` または `.cursorrules` | エンジンを指す `.cursorrules` プロンプトヘッダ |
| Windsurf | `.windsurf/` または `.windsurfrules` | 同じプロンプトヘッダの `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` または `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` パッチ |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` または `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

すべての IDE でターミナルから同じ `uxskill recommend` / `uxskill lint` / `uxskill stats` CLI コマンドが動きます。Python エンジンが真実の源泉;IDE のアーティファクトはエンジンへルーティングする薄いプロンプトヘッダにすぎません。

---

## ユースケース — 具体的なシナリオ

8 つの実シナリオ。あなたの状況に最も近いものを選び、呼び出しを適応させてください。

### 1. Cursor でフィンテックダッシュボードを構築

Cursor で MENA ネオバンクのダッシュボードを作っています。プラグインをインストールし、discovery、recommendation、そしてダッシュボード生成を順に実行します。

```bash
pip install uxskill
uxskill init                                # Cursor を検出、.cursorrules を書き出し
uxskill discover                            # 10 フィールドインテーク
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

そして Cursor に頼みます:*「.ux/last-recommendation.json の推奨を使ってダッシュボード画面を生成」*。Cursor は `.cursorrules` ヘッダを読み、推奨をロードし、明示的な制約付きでダッシュボード生成を派遣します。

### 2. Claude Code で Stripe スタイルのランディングを生成

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> プロジェクトタイプ? landing
> 業種? fintech-payments
> トーン? 真剣、技術的、自信
> 必須項目? dark-mode、AA、mobile-first
> 禁止事項? purple-gradients、three-equal-cards
> 参照ブランド? stripe
> スタック? nextjs-15-app-router
> 地域? global
> 成功指標? サインアップコンバージョン

/ux-recommend
> [選定スタイル、パレット、タイプペア、モーションプリセット、コンポーネント、ブランド事例を返す]

/ux-design "Stripe のブランド仕様を事例に使ってランディングを生成"
> [frontend-engineer がページを生成]

/ux-lint .
> [パス — Stripe のブランド仕様が尊重された]
```

### 3. CI で既存コードを AI スロップに対して監査

2 週間前に Next.js アプリを出荷しました。すべての PR で AI 指紋に対する硬い床が欲しい。

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

紫から青グラデーション、96px の Inter、「John Doe」のお客様の声、アイコンとしての絵文字を導入する PR は CI で失敗します。LLM コストなし。~200ms。

### 4. 「AI 生成っぽい」既存画面をポリッシュ

他のすべての AI 生成 SaaS サイトと同じに見える React アプリを引き継ぎました。そう見えなくしたい。

```
/ux-critique src/components/Hero.tsx
> [3 つの勝ち、3 つの負け、1 つの戦略的一手 — 講評は正直]

/ux-lint src/
> [15 件の高重大度 AI 指紋がフラグされる]

/ux-polish src/components/Hero.tsx
> [LLM ドリブンの仕上げ + AI スロップ除去]

/ux-fix
> [所見をアトミックコミットとして適用、リンターを再実行]
```

3 つのコマンド、1 つのポリッシュされた画面、修正ごとにアトミックなコミット。

### 5. Linear スタイルのコマンドパレットを設計

```
/ux-component command-palette --brief="Linear スタイル、ダーク、等幅ショートカット、最近のアイテムを先頭"
> [data/brands/linear.app.json から token + シグネチャムーブを読み込む]
> [data/components.json から command-palette の解剖 + ステートを読み込む]
> [明示的な Linear 仕様で frontend-engineer を派遣]
```

生成されるコンポーネントは Linear の実際のカラー token、タイプスタック、モーション規約、ヘアライン密度を使用します — 「汎用ダーク UI」ではなく。

### 6. ステークホルダーと 90 分のデザインシンキングワークショップを開催

5 人を 90 分。「雰囲気」ではなくゲームプランを持って退室してほしい。

```
/ux-workshop "ロイヤルティウォレットのピボット" \
  --participants="2 PM、1 デザイナー、1 エンジニアリードと、1 顧客担当" \
  --minutes=90
```

プラグインが 5 段階(探索 → ヒートマップ → ステークホルダーマップ → 解決策スケッチ → ゲームプラン)を端から端まで時間枠付きで進行し、段階ごとに具体的なアーティファクトを生成します。出力は `.ux/last-workshop.json` — 「興味深い発見」ではなくゲームプラン。

### 7. ローンチ後に公開可能なケーススタディを書く

ロイヤルティウォレットを出荷しました。ポートフォリオピースが欲しい。

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [.ux/last-frame.json、last-workshop.json、last-research.json、last-design.json、last-a11y.json、last-polish.json、last-recommendation.json、last-discovery.json を読む]
> [(A)-(G) 番号付きセクション、ヘアライン区切り、バイリンガル対応レイアウトの Wfrah エディトリアルケーススタディを生成]
> [case-studies/bashiti-loyalty.html を書き出す]
```

ケーススタディは完成された公開可能なアーティファクト — 草稿ではありません。純モノクロ、エディトリアルタイポ、あなたのポートフォリオに即出荷可能。

### 8. 非 AI 環境で discovery を実行(構造化インテークだけ)

プロジェクトをスコープしています。まだ推奨は不要 — 構造化されたブリーフが必要。

```bash
uxskill discover
# 10 フィールドインテーク、.ux/last-discovery.json に保存

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

JSON をチームに渡せます、Notion ドキュメントに貼れます、別の AI ツールに供給できます。ux-skill はエンジンであるだけでなく、構造化インテークツールでもあります。

### 9. MASTER.md 永続化 — リポジトリ内のデザイン決定

`/ux-recommend` の後、選定したスタイル + パレット + タイプ + モーション + コンポーネント + ブランド事例 + ガードレールを、チームがレビュー、差分、バージョン管理できる人間可読の Markdown ファイルとして永続化します。

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md`(YAML フロントマター + 本文)と、`persist save-page` 経由で生成済み画面ごとに `.ux/design-system/pages/<name>.md` を書き出します。冪等 — 同じ入力はバイト単位で同じ出力を生むので、状態が変わらない再実行は git で no-op です。

---

## 他の選択肢との比較

簡潔なサマリー表。完全な列ごとの比較は [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

| 次元 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| スラッシュコマンド | **22** | 1 | 19 | 1 | 1 | 複数 | 1 | 1 | 1 |
| コンポーネント | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| モーションプリセット | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ブランド仕様 | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| アンチパターンルール | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 安全な決定論的リンター | **はい** | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| 対応 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery ゲート | **10 フィールド** | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 |
| `.ux/` 状態チェーン | **はい** | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| スター数(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 正直な評価

- **ui-ux-pro-max** は認知度で勝り、18 IDE を出荷し、CSV 上で BM25 風検索を持ちます。コンポーネントマニフェスト、モーションマニフェスト、ブランドライブラリ、決定論的リンターはありません。
- **open-design** は 19 スキル + プレビューを持ちますが、Claude Code のみのサポートで反スロップ層もありません。
- **hallmark** は精神的に最も近い(同じく反スロップ)ですが、単一スキル — エンジンも、マニフェストも、チェーンコマンドもありません。
- **material-3-skill** は特に Material Design 3 が欲しい時に優れています。MD3 では競いません。

次元ごとの完全な詳細は [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## ロードマップ

### v2.1 — リンター完備(2026 Q3)

- **+17 の延期されたアンチパターンルール** で合計 52。ターゲット:dark-on-dark のホバーステート、色のみによるステートエンコーディング、冗長な z-index エスカレーション、JS 中のハードコードブレークポイント、disabled ステートの代わりの opacity など。
- **機械的に修正可能な所見の安全な書き換えに対する `uxskill lint --fix`**(`button-no-type`、`img-no-alt` 空文字列、`console-log-leak` 除去)。
- **インラインでリンターの所見を表示する VS Code 拡張機能**(CI を回す必要なし)。

### v2.2 — コンポーネントマニフェスト拡張(2026 Q4)

- **+50 コンポーネント** で合計 198。新規:非同期フィルタ付き combobox、最近のアイテムのヒューリスティック付き command-palette、条件付きフォームステップ、payment-element バリアント、RTL 認識デートピッカー、MENA 専用電話入力、ヒジュラ暦オーバーレイ付きカレンダーグリッド。
- **6 スタックでのコンポーネント別コード生成**(Next.js + React、Vue 3 + Nuxt、SvelteKit、Astro、Blade + Alpine、純 HTML/CSS)。
- **コンポーネントプレイグラウンド** が uxskill.laithjunaidy.com/playground に — 推奨エンジンを試し、ライブコンポーネントプレビューを確認。

### v3 — マーケットプレイス + ロックイン(2027)

- **ブランド仕様マーケットプレイス** — コミュニティのブランド仕様を公開、発見。モデレーションを賄うための有料公開。
- **カスタムアンチパターンルール** — プロジェクトが `data/anti-patterns.local.json` で独自の正規表現ルールを定義(v2 で出荷済み;v3 で発見 + 共有を追加)。
- **`uxskill plan`** — ブリーフから単一画面ではなくフルマルチページサイトの計画。
- **Figma プラグインパリティ** — 同じ推奨エンジンを Figma に表面化。

---

## コントリビューション

issue と PR を歓迎します。3 つの高レバレッジ領域:

### アンチパターンルールを追加

1. `data/anti-patterns.json` を編集 — `id`、`name`、`severity`、`category`、`detection.pattern`、`detection.flags`、`detection.scope`、`evidence_template`、`fix`、`references` を持つエントリを追加。
2. `tests/linter/` にテストを追加 — ルールをトリガーするファイルとしないファイル。
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx` を実行 — 発火を確認。`tests/linter/should-not-trigger/<rule>.tsx` を実行 — 発火しないことを確認。
4. PR を開く。

### ブランド仕様を追加

1. `data/brands/<slug>.json` を `id`、`name`、`category`、`voice`、`tokens`、`design_principles`、`signature_moves`、`anti-moves`、`references` で作成。
2. 対応する散文を `references/brands/<slug>.md` に追加。
3. `data/brands/_index.json` に登録。
4. PR を開く。仕様は第一次情報源によって裏付けられねばなりません(ブランドの実際の製品、公開デザインシステム、公開している場合の DESIGN.md)。

### モーションプリセットを追加

1. `data/motion-presets.json` を編集 — `id`、`name`、`category`、`tokens`、`stacks`(framer_motion、gsap、css)、`accessibility.reduced_motion_fallback`、`when_to_use` を持つエントリを追加。
2. プリセットには reduced-motion バリアントが必須。例外なし。
3. PR を開く。

### プロセス

- 完全なプロセスは [CONTRIBUTING.md](CONTRIBUTING.md)。
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) を読む。
- 新規ルールとブランド仕様は次の点でレビューされます:第一次情報源での裏付け、単一プロジェクトへの過適合なし、データ内に絵文字なし、該当する場合の RTL 安全動作。

---

## ライセンス、作者、謝辞

### ライセンス

MIT。使う、フォークする、その上に構築する。AI スロップを出荷せずに済んだなら、リポジトリにスターを — 最も安価な支援方法です。

### 作者

**Laith Aljunaidy** — MENA 優先のロイヤルティプラットフォーム [Dot](https://thedotwallet.com) の独立創業者。AI 生成のフロントエンドが皆同じに見えないように ux-skill を作っています。

- LinkedIn:[linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- メール:laith.aljunaidy.laith@gmail.com
- リポジトリ:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- サイト:[uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI:[pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm:[npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 謝辞

- Claude Code と、これを配布可能にしたスキル / プラグインアーキテクチャを提供してくれた Anthropic チームに。
- Nielsen Norman Group、Laws of UX(lawsofux.com)、そして `data/ux-guidelines.json` の根拠となる仕事をした UX リサーチコミュニティに。
- `data/brands/` にリストされたすべてのブランドに — 公開デザインシステムがブランド仕様の真実の源泉です。
- 元の v1 コントリビューターに:v2 Python エンジンの種となった一発撮りの Claude スキル。
- 比較した 8 つの人気 Claude UX プラグインに — 彼らがバーを上げた;これが私たちの答え。

---

**ux-skill** · **v3.1.0-stable** · Claude Code、Cursor、Windsurf、その他すべての AI コーディングツールが、AI 生成と読まれないフロントエンドを出力するために構築。

> [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) でリポジトリにスター · `pip install uxskill` または `npx uxskill init` でインストール · [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) で比較をブラウズ
