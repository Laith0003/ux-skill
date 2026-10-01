[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · **日本語** · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill：Claude Code、Cursor、その他すべての AI コーディングツールのためのデザイン知能エンジン

**AI が生成する UI を、ありきたりではなく個性あるものにするデザイン知能エンジン。** 17 の AI コーディングツールのどれに組み込んでも、出力が AI 製に見えなくなります。無料、MIT、オフライン、LLM なし。

```bash
pip install uxskill
```

**[GitHub で ux-skill にスターを付ける](https://github.com/Laith0003/ux-skill)**：役に立ったなら、これがプロジェクトを支援するいちばん手軽な方法です。はじめての方は [60 秒ツアー](#クイックインストール)から、または [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) で実際の動きをご覧ください。

![ビフォー：ありがちなストックフォトのヒーロー、淡い紫のグラデーション、ブランドらしさはゼロ。アフター：暗いスクリムを敷いた本物の建設現場の写真、琥珀色のアクセントを効かせたエディトリアルな見出し、ヒーローに組み込まれた見積もり依頼フォーム。同じプロンプトでも、ux-skill が制約を与えると結果が変わります。](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*ビフォー：ありがちなストックフォトの SEO スロップ。アフター：暗いスクリムを敷いた本物の建設現場写真のヒーロー、琥珀色のアクセントを効かせたエディトリアルな見出し、ヒーロー内の見積もりフォーム。同じ AI コーディングツール、同じプロンプトでも、ux-skill が制約を与えると結果が変わります。*

> **v4.0、FOUNDATIONS：コマンドひとつで、WCAG で検証された完全なデザインシステムを構築。アラビア語と右から左への表記にも標準対応。** AI コーディング向け最強の UX プラグイン。決定論的な 7 軸シンセサイザーを備えた Python の推論コア、12 個のクエリ可能な JSON マニフェスト(84 のスタイル、176 のパレット、70 のタイプペアリング、148 のコンポーネント、184 の業種、35 のチャートタイプ、57 のモーションプリセット、112 の UX ロー、171 のアンチパターンルール、25 の技術スタック、160 のブランド仕様)、18 のスラッシュコマンド、5 つのサブエージェント、25 の MCP ツール、そして決定論的な反 AI スロップリンター。クロス IDE：Claude Code、Cursor、Windsurf、GitHub Copilot、Gemini CLI、Codex、Kiro、Cline、Continue、Aider、Zed、JetBrains AI、Pieces、Tabby、Tabnine、CodeWhisperer、Roo Cline に導入できます。

> **ブランド名は `ux-skill`。** PyPI / npm のパッケージ名は `uxskill` のままです。GitHub リポジトリは [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill) にあります。

**作者:** [Laith Aljunaidy](https://laithjunaidy.com)、アンマン在住のデザイナー兼 CTO · **サイト:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **すべての Claude UX プラグインとの比較:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-向けインストーラー)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### 4.0 の新機能：基盤

ブランドカラーをひとつ入れると、デザインシステムが出てくる。コントラストは手元に届く前に確認済みです。

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 以降が必要です。MCP サーバーには `pip install --upgrade 'uxskill[mcp]'`。pipx なら `pipx install uxskill`(インストール済みの 3.x を更新するなら `pipx upgrade uxskill`)。npm なら `npx uxskill@latest`。3.x から移行しますか。[移行ガイド](docs/migrating-to-4.md)が 3.x のすべてのトークンを 4.0 のロールに対応付けています。

**プロダクトやランディングページを作るなら。** ページから読み込む `tokens.css`、選んだ書体のメトリクスに合わせたフォールバックを含む `fonts.css`、書体を自前のファイルから読み込む `fonts-self-host.css`、ツール向けの `tokens.json`、`art/` に入った装飾用のブランドアート、そして何をなぜ作ったのか、どのページ構成から始めるべきかを平易な言葉で説明する `system-report.md` が手に入ります。スタイルはロール(`var(--color-action-primary)`、`var(--color-text-default)`、`var(--color-surface-page)`)で指定し、ダークモード、ハイコントラスト、コンパクトな余白、右から左、動きを減らす設定は `<html>` の属性ひとつで切り替えます。書体はレポートが示す Google Fonts のリンクか、`fonts-self-host.css` と `fonts/` フォルダで読み込み、どちらの場合も `fonts.css` を `tokens.css` より先に読み込んでください。どちらのファイルも編集しないでください。`--brief` を付けると、ブリーフに業種とトーンがあれば見た目がそれに従い、構造化フィールド(年齢、言語、既定のスキーム、読まれる状況)が文字サイズ、タップ領域、文字体系、最初に開くスキームを決めます。discovery は業種を尋ねないので、`/ux-system create` が尋ねます。Claude Code では、`/ux-system create` がインストール済みのバージョンを確認し、ビルドを実行してレポートを説明します。

**デザインシステムを設計するなら。** 9 つの基盤(カラー、タイプ、スペース、レイアウト、角丸、ボーダー、エレベーション、モーション、イメージ)が 7 つの軸に合わせて連続的に変化し、プリミティブとセマンティックなロールを備え、すべてのモードの値を含む W3C デザイントークン形式(DTCG 2025.10)で出力されます。入力が同じならバイト単位で同じ結果。MCP では `ux_system_build` がレポート、ゲートの結果、各ファイルのサイズを返し、`out` を渡せばコマンドと同じファイルを書き出します。

- **WCAG ゲート。** テキスト、コントロール、フォーカスのすべての色の組み合わせを、ライトとダーク、標準コントラストとハイコントラストで測定します。標準コントラストでは WCAG 1.4.3(テキスト 4.5:1)と 1.4.11(非テキスト 3:1)、ハイコントラストでは WCAG 1.4.6(テキスト 7:1)。さらに、WCAG は非テキストの高い水準を定めていないため、ほとんどの非テキスト部分にはハイコントラスト時 4.5:1 という独自の下限を設けています。基準を満たさないシステムは書き出されず、メッセージが何を直すべきかを伝えます。
- **既定で安全。** 内容が異なるファイルは決して上書きしません。`--force` を付けたときだけファイルを置き換えます。
- **アラビア語。** `dir="rtl"` のもとでは、テキストが独自のサイズと行の高さを持つアラビア文字の書体に切り替わります。余白は論理プロパティを使い、モーションは左右反転します。`--latin-only` で除外できます。

**すでにあるシステムを使うなら。** `/ux-system enhance --from` は既存のシステムを元の名前のまま読み込み(DTCG トークン、CSS カスタムプロパティ、Tailwind のテーマ、markdown のルールファイル、Figma 変数のエクスポート)、同じゲートで確認し、コードが実際にそれをどう使っているかを測定します。何も書き換えません。`/ux-system extend --from` は既存のトークンを一切変えずに基盤、ロール、コントラクトを追加し、隣に置く拡張ファイルに書き出します。`uxskill system export` は tokens.css、Tailwind 4 のテーマ、Figma 変数として書き出します。4.2 では信頼レイヤー(書き込みごとの lint、仕上げのレビュアー)とローンチが加わります。[changelog](CHANGELOG.md) をご覧ください。

**コンポーネントとセクション。** 23 のコンポーネントコントラクトが、コントロールの各パーツがどの状態でどのトークンに結び付くか、各状態がどう動くかを定めます。状態の変化は `motion.state` で遷移し、押下は `motion.press.scale` で拡縮し(動きを減らす設定では静止)、タブ、メニュー、セグメンテッドコントロールはひとつのインジケーターをスライドさせます。14 のセクションコントラクト(ヒーロー、料金、FAQ、フッターなど)は、各セクションの役割、スロットに入るコンポーネント、必要な裏付け、スマートフォンでの積み重ね方を定めます。これらで組んだページは写真を使います。インターフェースの断片はあくまで追加のイメージで、写真の代わりにはなりません。

**ページを読むリンター。** 171 のルールの多くは、パース済みの CSS とマークアップに対する検査を伴い、ページ自身のシステムを読み取ります。モーションはそのカーブからタイミングを測り、ディスプレイ見出しの行の高さはエンジンの下限を守らせ、非表示のコントロールはタブ順から外れていなければなりません。`uxskill lint --render` は各ページをヘッドレス Chromium でデスクトップ幅とスマートフォン幅で開いて実際に操作し、表示されない、または切れているフォーカスリング、反応の遅いホバーと押下、Escape 後に失われるフォーカス、動きを減らす設定でもまだ動く押下を検出します。

**コマンドを整理。** 25 のスラッシュコマンドが 18 になりました。`/ux-discover` は `--frame` と `--recommend` を、`/ux-design` は `--component`、`--dashboard`、`--from-image` を受け付け、`/ux-polish` はスコアが 90 に達するか 3 ラウンド経つまで lint、修正、再 lint を繰り返し、`/ux-init` は `--stats` を受け付けます。古い 7 つの名前はエイリアスとして引き続き使え、4.1 で廃止されます。[エイリアス](#エイリアス41-で廃止)を参照してください。

**画面別プレイブック。** ランディング、ダッシュボード、コンポーネントのルールは `references/surfaces/` にそれぞれひとつずつのプレイブックとして置かれています。`/ux-design` はモードに応じてちょうどひとつだけを読み込むので、ダッシュボードのビルドがヒーローのルールを読むことはありません。

テスト **9764 件合格**。オフライン。決定論的。LLM は一切呼び出しません。

### v3.1 の新機能：ブランドに忠実、レスポンシブ、生き生き

- **ブランドへの忠実さは期待ではなく強制。** プライマリカラーはロゴのピクセルから読み取ります(最も多く塗られた CSS からではありません)。既定のフォントはロゴの字形スタイルに合わなければ却下されます。抽出したブランドは `recommend` -> `synthesize` へと受け渡され、`evaluate` の**厳格な下限**が、ブランドカラーやロゴを落とした出力、本物のイメージを含まない出力を不合格にします。オープンな `brand.md` 規約との双方向の相互運用(レンダリング + 取り込み)。
- **モバイルファーストをゲートで担保。** 新しいクラフトの基盤(`responsive.md`、`component-behaviors.md`)に加え、折り返しを考慮したゲートが、横スクロール、折り返したナビ、ワードマーク、ボタンのラベル、高すぎる固定ヘッダーを不合格にします。
- **ワウのレイヤー。** エンジンがページごとに 2-3 の連動したシグネチャーモーメントを導き出します。「ワウはユーザーからしか生まれない」という考え方は覆されました。
- **より鋭いリンター**(152 ルール):必須イメージとアイコンのみの要素の検出、プレースホルダートークンと `100vw` のルール。シード付きの picsum は残し、ランダムなものは除去。

詳細は [CHANGELOG.md](CHANGELOG.md) にあります。

### v3 の新機能

- **ブランド仕様はテンプレートではなく訓練データになります。** 160 のブランド仕様はレコメンダーが選ぶカタログではなくなり、シンセサイザーが蒸留する語彙になります。出力は呼び出しごとに新しくなります。
- **7 軸シンセサイザー**(warmth、contrast、density、geometry、formality、motion、type_personality)。ブリーフは決定論的に軸の値にマップされ、軸の値が新鮮な palette + タイポ + spacing + radius + motion トークンへとコンパイルされます。
- **3 つの自動振り分けモード**：`strict_brand`(単一ブランドの 100%)、`brand_anchor`(単一ブランド 70% + 兄弟ブランドから軸適応された 30%)、`pure_synthesis`(ブランド指定なし、軸が一致する 8 例から蒸留)。
- **決定台帳がレコメンダーをリランクします。** `.ux/decisions.jsonl` が同じ `(industry, ui_type)` バケットでの過去の勝者で候補をリランクします。コールドスタートに安全。`lint_score >= 80` かつ `user_accepted = true` の決定のみカウントします。
- **軸相互作用マトリックス**：競合軸間の明示的な衝突解決(dense + corporate → 4px、airy + corporate → 12px、soft + playful → 18px radius)。もうサイレントな場当たりルールはありません。
- **`/ux-evolve` 自動ループ**(4.0 では `/ux-polish` の既定のループ):スコア ≥ 90、プラトー、または 4.0 では 3 ラウンド(v3 では 5)まで lint → polish → re-lint。品質ゲートは 65。
- **3 つの新 MCP ツール**(15 → 18):`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`。
- **ローカル統計ダッシュボード**：`uxskill stats --html` が `.ux/stats.html` を書き、**あなたの**インストールが何を学んだかを示します。テレメトリなし、グローバル集約なし。
- **223 テスト通過。** オフライン。決定論的。LLM を呼ばない。

詳細は [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain) に。

### Star 履歴

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill とは

ux-skill は AI コーディングツールのための**デザイン知能エンジン**です。Python パッケージとして(`pip install uxskill`)、Claude Code プラグインとして、そして 17 IDE 向けマルチインストーラーとして動作します。エンジンはプロジェクトのブリーフ(業種、オーディエンス、トーン、必須項目、禁止事項、スタック、地域)を取り込み、推奨デザインシステム一式を返します:スタイル、パレット、タイプペア、モーションプリセット、コンポーネント、研究すべきブランド事例、そして守らねばならないアンチパターンのガードレール。推奨は決定論的です、同じ入力は常に同じ出力を生みます。

このプラグインはあなたと AI コーディングツールの間に入ります。Claude Code、Cursor、その他の AI アシスタントに「フィンテックのランディングページを作って」と頼むと、アシスタントはたいてい即興で作り、その結果は 5 秒で AI 生成と見抜かれます(紫から青のグラデーション、等大の 3 枚カード、ディスプレイサイズの Inter、推薦文の「John Doe」、デフォルト 300ms のトランジション、中央寄せのヒーロー、CTA で跳ねる矢印)。ux-skill は即興を**構造化された制約**に置き換えます。`/ux-discover` でブリーフを取り込んでシステムを選び、`/ux-design` でコードを生成し、`/ux-lint` でコミット前に 171 の決定論的な反 AI スロップルールを通過することを確かめます。

この README が正典のリファレンスです。すべてのコマンド、すべてのサブエージェント、すべてのデータマニフェスト、すべてのインストール経路、すべてのブランド仕様、すべてのアンチパターンカテゴリ、すべてここに記録されています。Claude Code のデザインプラグインを探している、または Cursor、Windsurf、Codex 向けの AI デザインツールを比較しているなら、これを最初から最後まで読み、[compare.html](https://uxskill.laithjunaidy.com/compare.html) と並べてご覧ください。

---

## 目次

1. [ブレイン、v3.0 とは何か](#ブレインv30-とは何か)
2. [クイックインストール](#クイックインストール)
3. [数字、トップ 8 の Claude UX スキルとのライブ比較](#数字トップ-8-の-claude-ux-スキルとのライブ比較)
4. [アーキテクチャ、各部品がどう噛み合うか](#アーキテクチャ各部品がどう噛み合うか)
5. [18 のスラッシュコマンド、詳細リファレンス](#18-のスラッシュコマンド詳細リファレンス)
6. [5 つのサブエージェント](#5-つのサブエージェント)
7. [11 のデータマニフェスト](#11-のデータマニフェスト)
8. [171 の反 AI スロップルール、リンター](#171-の反-ai-スロップルールリンター)
9. [160 のブランド DESIGN.md 仕様、カテゴリ別](#160-のブランド-designmd-仕様カテゴリ別)
10. [MCP サーバー、非対称な一手](#mcp-サーバー非対称な一手)
11. [17 IDE 向けインストーラー](#17-ide-向けインストーラー)
12. [ユースケース、具体的なシナリオ](#ユースケース具体的なシナリオ)
13. [他の選択肢との比較](#他の選択肢との比較)
14. [ロードマップ](#ロードマップ)
15. [コントリビューション](#コントリビューション)
16. [ライセンス、作者、謝辞](#ライセンス作者謝辞)

---

## ブレイン：v3.0 とは何か

v3.1.0 は ux-skill 史上最大のアーキテクチャ的シフトです。レコメンダーはもうカタログからテンプレートを選びません、エンジンがブリーフごとに新鮮なデザイン言語を**合成**します。同じブリーフは常に同じ出力を生み(完全に決定論的)、しかし異なるブリーフごとに独自の新しいシステムが生まれます。ブランド仕様はテンプレートではなくなり、エンジンが語彙を学ぶ訓練データになります。システムは自身の履歴に目を持ち、フィードバックループをローカルで閉じ、LLM を一度も呼びません。

コンパイラーは**決定論的な 7 軸シンセサイザー**です、warmth、contrast、density、geometry、formality、motion、type_personality。すべてのブリーフが軸の値にマップされ、軸の値が新鮮な palette + タイポ + spacing + radius + motion トークンにコンパイルされます。モジュラータイポスケールは contrast から比を選びます(1.200 quiet / 1.250 balanced / 1.333 loud)。レイアウトプリミティブは構築によりレスポンシブ(`auto-fit minmax(min(N, 100%), 1fr)` + コンテナクエリ)。壊れたレイアウトは表現不可能なので発行できません。

自動振り分けの 3 モード:`strict_brand`(`reference_brands=[stripe] strict=True` → 100% Stripe トークン、最速パス);`brand_anchor`(`reference_brands=[stripe]` → 70% Stripe + 4 兄弟ブランドから軸適応の 30%);そして `pure_synthesis`(ブランド指定なし → 無限空間、軸が一致する 8 例を新しいデザイン言語に蒸留)。軸の衝突は文書化された**軸相互作用マトリックス**で解決されます、dense + corporate は 4px にコンパイル(density 勝ち、ブルームバーグ流派)、airy + corporate は 12px(formality 勝ち、ラグジュアリー)、soft + playful は 18px radius、sharp + corporate は 2px。実装に隠れた場当たりルールはありません。

**決定台帳**(`.ux/decisions.jsonl`、スキーマ `_v: 1` 固定)がフィードバックループを閉じます。レコメンダーは同じ `(industry, ui_type)` バケットでの過去の成功をもとに候補を並べ替えます。コールドスタートでも安全で、過去の決定が 3 件未満なら並べ替えを行いません。`lint_score >= 80` かつ `user_accepted = true` の決定だけを数えます。さらに `/ux-polish` はスコア ≥ 90、プラトー、または 3 ラウンドまで lint → polish → re-lint を回し、65 という品質ゲートを下回る出力は `--force` なしでは拒否します。結果として、どのインストールも自分のコーパスで賢くなり、どの実行もマシン間で再現でき、エンジンは完全にオフラインのままです。

---

## クイックインストール

3 つのインストール経路。あなたの環境に合うものを選んでください。

### 経路 1：Claude Code マーケットプレイス(正典)

Claude Code に常駐しているなら、プラグインマーケットプレイスからインストールします:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

これで 18 のスラッシュコマンド(加えて 4.1 までエイリアスとして残る古い 7 つの名前)と 5 つのサブエージェントが Claude Code セッションに接続されます。インストール後、`/ux-init` を実行してプロジェクト単位の `.ux/` 状態ディレクトリをセットアップし、Python エンジンが到達可能であることを確認してください。

### 経路 2：pip(汎用)

Claude Code の外で作業している場合(Cursor、Windsurf、CLI、CI)、Python パッケージをインストールします:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

パッケージは CLI エントリポイントとして `ux` と `uxskill` の両方を公開します、同じバイナリです。

### 経路 3：npx(Python 管理不要)

Python を直接管理したくない場合、npx ラッパーが `pipx` 経由で一切を起動します:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### インストール検証

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

これらの件数を合計すると 1,262 エントリになります。いずれかの件数が 0 を返したら JSON ファイルが欠けているので、[github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) に issue を立ててください。

---

## 数字：トップ 8 の Claude UX スキルとのライブ比較

スター数の最終確認は `gh api` 経由で **2026-05-28**。ux-skill(Laith0003/ux-skill)は最新の参入者です、認知度では小さく、アーキテクチャでは深い。以下の比較は正直です:どこで負け、どこで勝つか。

| プラグイン | スター数 | アーキテクチャ | スラッシュコマンド | リンター(CI 対応) | ブランド仕様 | コンポーネント | モーションプリセット | 対応 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV、単一スキル | 1 | - |、| 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 スキル + プレビュー | 19 | - |、| 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + リサーチ裏付けの審美眼 | 1 | - |、| 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 単一の 62 KB SKILL.md + スクリプト | 1 | - |、| 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | MCP に接続されたスキルライブラリ | 複数 | - |、| 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 単一美学スキル | 1 | - |、| 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 反スロップデザインスキル | 1 | - |、| 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 コンポーネント + 監査 | 1 | - | (MD3 のみ) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python エンジン + 12 マニフェスト + 18 コマンド + 5 サブエージェント + CI リンター** | **18** | **171 の決定論的ルール** | **160** | **148** | **57** | **17** |

### 負けているところ

- **認知度。** 彼らは数十万のスターを持っています。私たちは 14 です。スターを付けてください、最も安価な支援方法です。
- **ブランド認知。** ui-ux-pro-max と open-design は、日ではなく月単位で先行しています。
- **マーケティングの磨き込み。** スクリーンショット、デモ動画、見つけやすいランディングページがあります。私たちには徹底した README と質素なランディングしかありません。

### 勝っているところ

- **コンポーネントライブラリ:** 148 個のドキュメント化されたコンポーネント。解剖、ステート、使用 token、モーション仕様付き。他の 8 つはどれもコンポーネントマニフェストを同梱していません。
- **モーションプリセット:** 57 個のスタック対応エントリ(Framer Motion、GSAP、CSS)、reduced-motion フォールバック付き。他のどこもモーションマニフェストを同梱していません。
- **アンチパターンリンター:** 171 個の決定論的ルール、CI で実行し Critical/High で非ゼロ終了。他のどこも決定論的リンターを同梱していません。
- **ブランド仕様:** 160 個の実在 DESIGN.md 仕様(Apple、Stripe、Linear、Figma、Tesla、BMW、Notion、Spotify、Airbnb、Vercel、Supabase、Cursor、Raycast、Claude ほか 96 件)。他のどこもブランドライブラリを同梱していません。
- **17 IDE 対応:** 同じエンジン、IDE ごとに違う糊。
- **18 のスラッシュコマンド:** discovery、生成(ページ、コンポーネント、ダッシュボード、画像から)、監査、lint、ポリッシュループ、修正ループ、ケーススタディ、ワークショップ、コピー、モーション、a11y、コンダクター、完全に統合済み。

完全な列ごとの比較表は [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) で。

---

## アーキテクチャ：各部品がどう噛み合うか

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

### エンジンが実際にどう動くか

1. **入力。** ブリーフを渡します。`/ux-discover` で対話的に(10 フィールド)、または `ux recommend` にフラグを渡して非対話的に。
2. **5 つの並列検索。** エンジンはマニフェストをまたいで 5 つの検索を同時に実行します:
   - **業種 → recommended_styles** (industries.json)
   - **スタイル → パレット + タイプ + モーションの互換性** (styles.json)
   - **トーン × 必須要件 → パレットの絞り込み** (palettes.json)
   - **スタック → コンポーネントの互換性 + モーションプリセット** (tech-stacks.json, motion-presets.json)
   - **禁止事項 + 地域 → ガードレール + ブランド事例の候補** (anti-patterns.json, brands/)
3. **統合。** 決定論的なマージャーが候補を順位付けし、競合を解決し(たとえば必須のダークモードがパレットのモードを決める)、推奨システムをひとつ出力します。
4. **出力。** 選ばれたスタイル、パレット、タイプペア、上位 5 つのモーションプリセット、上位 12 のコンポーネント、上位 5 つのブランド事例、そして有効な 171 のアンチパターンガードレールすべてを含む JSON ドキュメント。加えて、各選択の理由を説明するブロック。
5. **生成。** 後続のコマンド(ページ、コンポーネント、ダッシュボード、画像の各モードの `/ux-design` と `/ux-system`)が推奨を使い、サブエージェントを通じて実際のコードを生成します。
6. **検証。** `/ux-lint` が生成されたコードを 171 のルールで再スキャンします。CI で Critical/High があれば非ゼロ終了。

**v3 での追加。** レコメンダーは `.ux/decisions.jsonl` を使って `engine/decisions/` から候補を並べ替えます(`lint_score >= 80` かつ `user_accepted = true` の決定だけを数え、過去の決定が 3 件未満ならコールドスタートとして安全に扱います)。生成の経路は `engine/synthesizer/` に回すこともできます。これは決定論的な 7 軸コンパイラーで、カタログからテンプレートを選ぶのではなく、ブリーフごとに新しいパレット + タイプ + 余白 + 角丸 + モーションのトークンを生み出します。詳しくは [ブレイン、v3.0 とは何か](#ブレインv30-とは何か) を参照してください。

**Python が考え、HTML が見せ、Markdown がつなぐ。**

---

## 18 のスラッシュコマンド：詳細リファレンス

各コマンドは `commands/` 配下の `.md` ファイルとして同梱され、`description`、`allowed-tools`、`triggers`、`when to use`、`when to skip`、`input`、`process`、`output state file` を備えています。以下の説明は要約で、正式な仕様はソース全文です。

コマンドは 7 つのグループに分かれます:**ブートストラップと棚卸し**、**discovery と推奨**、**生成**、**監査と検証**、**修正とポリッシュ**、**discovery とナラティブ**、**コンダクター**。3.x の 7 つの名前は 4.1 まで[エイリアス](#エイリアス41-で廃止)として使えます。

### ブートストラップ & インベントリ

#### `/ux-init`：プロジェクトをブートストラップする

- **何をするか:** どの IDE を使っているか(`.claude/`、`.cursor/`、`.windsurf/` など)を検出し、対応するアーティファクトをインストールし、Python エンジンが到達可能であることを検証し、統計スナップショットを表示します。`--stats` はスナップショットだけを表示します:バージョン + データマニフェストのエントリ数。
- **使うタイミング:** 新規プロジェクトに初めてインストールするとき。ux-skill を使うプロジェクトを clone した後。`pip install --upgrade uxskill` 後。`--stats` はインストール後、アップグレード後、または推奨が意外な選択を返してマニフェストの欠けが疑われるとき。
- **スキップするタイミング:** すでにこのプロジェクトで実行済みで、何も変わっていない。`--stats` はスキップする必要がありません:50ms の読み取りです。
- **呼び出し方:** `/ux-init`(引数なし)、`/ux-init --stats`、または CLI から `uxskill init` / `uxskill stats`。`--decisions` で決定台帳のサマリーを追加し、`--html` で `.ux/stats.html` を書き出します。
- **出力:** IDE ごとのアーティファクト([17 IDE 向けインストーラー](#17-ide-向けインストーラー)参照)+ `.ux/` ディレクトリ + 標準出力サマリー。`--stats`:標準出力に JSON(上の[インストール検証](#インストール検証)参照)。
- **次に繋がる:** 次は `/ux-discover`。`--stats` は診断専用です。

#### `/ux-mcp`：エンジンを MCP サーバーとして動かす

- **何をするか:** エンジンを stdio 上の Model Context Protocol サーバーとして起動します。25 のツール(レコメンダー、リンター、永続化、シンセサイザー、決定台帳、画像からの抽出、データマニフェスト、そしてデザインシステムの構築、取り込み、強化、拡張、書き出し、検査)を、プラグインなしで任意の MCP 対応ホストから呼び出せます。
- **使うタイミング:** 別の MCP 対応ホストで作業していて、同じエンジンを使いたい。デザイン制約の唯一の情報源を必要とするマルチエージェントのパイプラインを動かしている。レコメンダーやリンターを CI で常駐プロセスとして使いたい。
- **スキップするタイミング:** プラグインを入れた Claude Code の中にいる。スラッシュコマンドがすでにエンジンに届いています。一度きりの答えが欲しい。`uxskill recommend` か `uxskill lint` のほうが簡単です。
- **呼び出し方:** `/ux-mcp`、または `pip install 'uxskill[mcp]'` の後にシェルから `ux-mcp`。
- **出力:** stdio の JSON-RPC サーバー。クライアントごとの設定は [MCP サーバー](#mcp-サーバー非対称な一手)と `commands/ux-mcp.md` を参照。
- **次に繋がる:** なし。これは手順ではなくトランスポートです。

### discovery & 推奨

#### `/ux-discover`：強制ゲート(10 フィールドの取り込み、フレーミング、推奨)

- **何をするか:** あらゆるプロジェクトが生成コマンドの前に必ず通る、10 フィールドの必須の取り込み。プロジェクトの種類、オーディエンス、主目的、トーン、必須要件、禁止事項、参考ブランド、スタック、地域、成功指標。**即興はなし。** 禁止フレーズ(「モダン」「クリーン」)でユーザーに具体性を求めます。続いてレコメンダーを実行し、Python エンジンが 12 のマニフェストをまたぐ 5 つの並列検索から、統合されたデザインシステムをひとつ返します(業種 → スタイル → パレット → タイプ → モーション + コンポーネント + ブランド事例 + ガードレール)。
- **モード:** `--frame` は誰のためか、アウトカム、仮説、成功シグナルを 4 フィールドのフレーミングブロックにまとめます。フルの取り込みより軽量です。`--recommend` は保存済みのブリーフか単発のフラグから、レコメンダーだけを実行します。
- **使うタイミング:** `/ux-design` や `/ux-system` の前。以前のブリーフが古くなったとき。`--frame` はプロジェクト、スプリント、単発の案件の始まり、または会話が脱線したときの途中で。`--recommend` はくたびれて見えるプロダクトを立て直すときに。
- **スキップするタイミング:** バグを直している(`/ux-fix`)。リンターのパスだけを実行している(`/ux-lint`)。前回のセッションからブリーフが変わっていない。
- **呼び出し方(Claude Code):** `/ux-discover`、`/ux-discover --frame "loyalty wallet for a MENA retail pilot"`、または `/ux-discover --recommend`。
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
- **出力:** `.ux/last-discovery.json`(10 フィールドのブリーフ)、`.ux/last-recommendation.json`(選ばれたスタイル、パレット、タイプペア、上位 5 つのモーションプリセット、上位 12 のコンポーネント、上位 5 つのブランド事例、有効な 171 のアンチパターンガードレールすべて、加えて理由)、`--frame` を付けた場合は `.ux/last-frame.json`(`{audience, outcome, hypothesis, success_signal}`)。
- **次に繋がる:** `/ux-design [extra brief]` → 推奨に基づくフロントエンドコード。`/ux-design --component <name>` → 判明した制約に沿ったコンポーネントひとつ。`/ux-system` → 推奨からの完全なデザインシステム。`/ux-lint` → 生成されたコードを検証。

### 生成

#### `/ux-design`：ブリーフから美しい、反スロップな画面を生成する

- **何をするか:** discovery ブリーフ + 推奨から完全なプロダクション級フロントエンドアーティファクト(ランディング、マーケティングサイト、アプリシェル)を生成します。反スロップと arsenal リファレンスからのクリエイティブディレクションのもと、`frontend-engineer` を派遣します。ブリーフかフラグで、次の 4 つのモードからひとつを選びます:
  - **ページ**(既定):完全なページ、または複数セクションの画面。`.ux/last-design.json` を書き出します。
  - **`--component [name]`**:プロダクション級のコンポーネントひとつ(ボタン、モーダル、ナビバー、サイドバー、カード、テーブル、フォーム、チャート)。4 つのインタラクション状態をすべて備え、アクセシブルでブランドに忠実。まず `.ux/last-recommendation.json` でコンポーネントを探し、なければマニフェストを直接参照します。`.ux/last-component.json` を書き出します。
  - **`--dashboard`**:データ密度の規律、ベントーレイアウト、表形式の等幅数字、スパークラインのパターン、カードの多用を避ける設計、意味のある状態色、控えめなモーション。チャートを貼り付けただけのマーケティングサイトではありません。`.ux/last-dashboard.json` を書き出します。
  - **`--from-image <path>`**:デザインの参考画像(PNG/JPG/WebP)を純粋な Pillow のコンピュータービジョンで読み取り(支配的なパレット、キャンバスの明暗、タイプの手がかり)、パレットとスタイルのマニフェストに照らし合わせ、得られた推奨から構築します。`--extract-only` は抽出の後で止まります。`.ux/last-image-extract.json` を書き出します。
- **使うタイミング:** 「~をデザインして」「~を作って」「ランディングページを生成して」「ダッシュボードを作って」「コンポーネントを作って」「ボタンを作って」「管理画面をデザインして」「オペレーターコンソール」「KPI ボード」「このスクリーンショットのように作って」、自由形式の視覚成果物のリクエストすべて。
- **スキップするタイミング:** 構築ではなくレビューが欲しい(`/ux-audit` または `/ux-critique` を使う)。バックエンドやインフラの作業。
- **呼び出し方:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`、`/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`、`/ux-design --dashboard`、`/ux-design --from-image ref.png`。
- **出力:** 生成されたコード(HTML / Blade / JSX / Vue / Astro)、加えてモードごとの状態ファイル。
- **次に繋がる:** `/ux-lint` → ガードレール検証。`/ux-polish` → 仕上げ。`/ux-a11y` → アクセシビリティ監査。`/ux-copy` → マイクロコピー監査。`/ux-fix` → 所見をアトミックコミットとして適用。

#### `/ux-system`：完全なスターターデザインシステムを生成する

- **何をするか:** デザインシステムがまだないプロジェクトに完全なスタータシステムを提案します、tokens(色、タイプ、空間、モーション、角丸、影)、基盤ドキュメント、コンポーネントコントラクト、ダークモードペアリング、テーマスイッチャー。`design-system-architect` を派遣。
- **使うタイミング:** 「デザインシステムがない」「システムを作って」「token を提案して」「テーマはどうあるべき」「DS をセットアップして」。
- **スキップするタイミング:** プロジェクトにすでにデザインシステムがある場合は、代わりに既存システムに対して `/ux-design --component` を使う。バックエンドやインフラ。
- **呼び出し方:** `/ux-system create`(基盤エンジン)、`/ux-system enhance --from <file>`(すでにあるシステムを測定)、`/ux-system extend --from <file> --add <foundation>`(変更せずに追加)、または `/ux-system`(3.x の流れ。まだなら discovery を先に実行)。
- **出力:** `tokens.json`、`foundations.md`、`components/*.md` のコントラクト、オプションで Tailwind / vanilla / SCSS の出力。チェーンのため `.ux/last-system.json` を書き出します。
- **次に繋がる:** `/ux-design --component` → 新システムに対して構築。`/ux-design` → 新しいトークンで画面を生成。

#### `/ux-motion`：モーション処理

- **何をするか:** 画面のモーション層を生成します、デュレーション、イージング、振り付け、reduced-motion フォールバック、パフォーマンス規律。既存モーションを 5 次元(タイミング、イージング、意味、reduced-motion、パフォーマンス)で監査もします。
- **使うタイミング:** 「モーション確認」「アニメーション大丈夫?」「モーションを直して」「アニメーションをレビューして」「モーション監査」「モーションのパフォーマンスパス」。
- **スキップするタイミング:** 画面にモーションがない(`/ux-audit` または `/ux-polish` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-motion path/to/component.tsx`(監査モード)または `/ux-motion --generate hero-entry`(生成)。
- **出力:** 更新されたコード(生成モード)または `.ux/last-motion.json` レポート(監査モード)。
- **次に繋がる:** `/ux-fix` → モーションの所見を適用。`/ux-polish` → 締め。

### 監査 & 検証

#### `/ux-lint`：決定論的な正規表現ベースのリンター(LLM なし、CI 安全)

- **何をするか:** あなたのコードに対して 171 のルールを実行します。LLM 呼び出しなし。CI で Critical / High に当たると非ゼロ終了。ソース:`data/anti-patterns.json`。ルールカバレッジ:A11y(45)、コンテンツ(35)、レイアウト(18)、タイポ(16)、モーション(14)、ビジュアル(14)、品質(12)、色(10)、パフォーマンス(5)、デプス(2)。
- **使うタイミング:** プリコミットフック。CI ゲート。`/ux-audit` のコストを払う前の大規模コードベースへの素早い初回パス。どのモードでも `/ux-design` の後の生成検証。
- **スキップするタイミング:** 修正ループが欲しい(リンターは報告のみ、編集しません、`/ux-polish --fix` か `/ux-fix` にチェーン)。審美的判断が欲しい(`/ux-critique` を使う)。
- **呼び出し方(slash):** `/ux-lint src/`。
- **呼び出し方(CLI):** `uxskill lint .` または `python3 bin/ux-lint.py .` または `bash bin/ux-lint.sh --ci --fail-on high`。
- **呼び出し方(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **出力:** 標準出力に所見(位置、ルール id、重大度、エビデンス)。クリーンなら終了コード 0、`--fail-on high` 設定時に Critical/High があれば非ゼロ。
- **次に繋がる:** `/ux-polish --fix` → 同パターンの LLM ドリブン対応物。`/ux-fix` → 所見を重大度順にコミットとして適用。`/ux-audit` → 6 レンズの完全な推論パス。`/ux-next` → コンダクターに決めさせる。

#### `/ux-audit`：6 レンズのデザイン監査

- **何をするか:** 6 つのレンズ(明瞭さ、ヒエラルキー、アクセシビリティ、ボイス、モーション、審美眼)に対する構造化された意見付きレビューで、重大度タグ付きの所見を生成します。Polaris スタイルのレポート。まず `.ux/last-frame.json` を読みます、オーディエンスとアウトカムがすべての所見の重大度を錨にします。
- **使うタイミング:** 画面が存在し、擁護可能な批評が欲しい。「監査して」「UX をレビューして」「これは良い?」「何が壊れてる?」「徹底的に解剖して」。
- **スキップするタイミング:** 画面がまだ存在しない(`/ux-design` を使う)。1 レンズだけ欲しい(専用コマンドを使う:`/ux-a11y`、`/ux-copy`、`/ux-motion`、`/ux-polish`)。審美的意見が欲しい(`/ux-critique` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-audit https://example.com/pricing` または `/ux-audit src/components/Pricing.tsx`。
- **出力:** `.ux/last-audit.json` を書き出します、`findings` 配列で `{lens, severity, title, principle, evidence, fix}`、`severity_counts`、`dominant_lens`、`strategic_moves`。
- **次に繋がる:** `/ux-fix` → 所見を適用。`/ux-polish` → 仕上げ。`/ux-design` → 構造的な再設計が必要なら。

#### `/ux-a11y`：WCAG 2.1 AA 監査 + 一般礼節チェック

- **何をするか:** 構造化された WCAG 2.1 AA 監査に加え、自動ツールはパスするが実ユーザーを傷つけ続ける一般礼節チェック(フォーカスの可視性、エラーの具体性、モーション設定、キーボードトラップ、色依存)。
- **使うタイミング:** リリース前のアクセシビリティゲート。再設計後。「アクセシビリティチェック」「WCAG 監査」「これはアクセシブル?」「a11y レビュー」「スクリーンリーダーテスト」「キーボードナビ確認」。
- **スキップするタイミング:** ユーザー向けでない。バックエンドやインフラ。作業途中のラフ。
- **呼び出し方:** `/ux-a11y https://example.com`(ライブ URL 推奨、自動ツールとキーボードテストはライブでしか動作しません)。
- **出力:** `.ux/last-a11y.json` を書き出します、`findings` 配列で `{wcag_sc, sc_name, severity, title, evidence, fix, category}`、`beyond_wcag` 配列、`severity_counts`。
- **次に繋がる:** `/ux-fix` → 所見をコミットとして適用。`/ux-copy` → コピーパスの一環として alt テキストやフォームエラーの結線を修正。

#### `/ux-critique`：審美的講評(3 つの勝ち、3 つの負け、1 つの戦略的一手)

- **何をするか:** デザイナーの意見、構造化監査ではない、重大度スコアではない、何が効いていて、何が効いていないかを名指しし、最も変化を生む 1 つの戦略的一手を示す、引き締まった意見付きの見解。
- **使うタイミング:** 「どう思う」「これは良い?」「批評して」「正直な見解」「雰囲気合ってる?」「これは私たちらしい?」「出して良い?」。
- **スキップするタイミング:** ユーザーが明示的に構造化監査を望む(`/ux-audit` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-critique https://example.com`。
- **出力:** `.ux/last-critique.json` を書き出します、3 つの勝ち、3 つの負け、1 つの戦略的一手、加えて散文。
- **次に繋がる:** 講評が再設計を勧めるなら `/ux-design`。締め直しを勧めるなら `/ux-polish`。

#### `/ux-copy`：マイクロコピーの監査 + 書き換え

- **何をするか:** すべての見える文字列をボイスルーブリックに照らして評価し、before/after の書き換えを生成します。捕捉対象:「フォームにエラーがあります」(汎用)、「John Doe」(プレースホルダー)、AI 的にはしゃぐ祝賀的コピー、汎用 CTA、生気のない空ステート、役立たずのエラー。
- **使うタイミング:** 構造は正しいが言葉が弱い。「コピーをレビュー」「マイクロコピーを直して」「エラーメッセージが悪い」「これを書き直して」「文字列を引き締めて」「ボタンが汎用すぎる」「この空ステートが死んでる」。
- **スキップするタイミング:** レイアウト問題(`/ux-audit` または `/ux-polish` を使う)。アクセシビリティ起因のコピー問題(alt テキストなど。`/ux-a11y` を使う)。バックエンドやインフラ。
- **呼び出し方:** `/ux-copy src/views/checkout.blade.php`。
- **出力:** `.ux/last-copy.json` を書き出します、`strings` 配列で `{location, severity, before, after, notes}`、加えてルーブリックと翻訳が必要なロケール。
- **次に繋がる:** `/ux-fix` → 書き換えを適用。`/ux-a11y` → コピー修正後の再確認。

### 修正 & 仕上げ

#### `/ux-fix`：所見をアトミックなコミットとして適用する

- **何をするか:** `.ux/` の最新レポート(audit、copy、a11y、motion、polish)を読み、作業ツリーを検証し、適切なサブエージェントを通じて所見をアトミックなコミットとして適用します。元コマンドを再実行して再検証します。
- **使うタイミング:** 監査クラスのコマンドを実行し所見をレビューした後。「所見を修正」「修正を適用」「修正ループを走らせる」「画面にパッチ」「変更を適用」「直して」。
- **スキップするタイミング:** `.ux/` に先行レポートがない。作業ツリーが汚れていてユーザーが stash/commit に同意していない。修正に機械的適用ではなくデザイン判断が必要(再設計のため `/ux-design` を使う)。
- **呼び出し方:** `/ux-fix`(どのレポートを修正するか自動検出)または `/ux-fix --from=last-a11y.json`。
- **出力:** 所見ごとのアトミックなコミット。元コマンドを再実行して `.ux/last-*.json` を更新。サマリーを表示。
- **次に繋がる:** `/ux-next` → コンダクターが次の一手を選ぶ。

#### `/ux-polish`：lint、修正、再 lint のループ + AI スロップ退治

- **何をするか:** まずローカルの HTML ファイルに対する決定論的なループ。lint、6 つの冪等なポリッシュパス、再 lint を、スコアが 90 に達する、頭打ちになる、または 3 ラウンド経つまで繰り返します(`--rounds` で上限を変更)。既定ではループの出力は `<file>.evolved.html` に残り、元のファイルには一切触れません。元のファイルを置き換えるのは `--loop-only` か `--fix` のときだけで、作業ツリーがクリーンかを確認したうえで行い、65 の品質ゲートが不合格の結果による置き換えを `--force` なしでは防ぎます。`--brand-file` を付けると、どの終了時点でもブランド忠実度の下限が守られます。続いてテイストのパス:余白のリズム、階層の明確化、AI スロップの検出、トークンの一貫性。`/ux-lint` の LLM 駆動版で、テイストの判断にはあなたの判断を使います。`--loop-only` はループだけ、`--no-loop` はテイストのパスだけを実行し、`--fix` はテイストの指摘を適用します。
- **使うタイミング:** 構造は正しいが仕上げが甘い。「ポリッシュして」「引き締めて」「AI スロップを取り除いて」「プレミアムにして」「AI っぽさを減らして」「余白がしっくりこない」「ありきたりに見える」「もっとテイストが欲しい」「スコア 90 以上まで改善して」「出荷できる状態にして」。
- **スキップするタイミング:** 画面に中核機能が欠けている(まずそれを直す)。ポリッシュではなく再設計が必要(`/ux-design` を使う)。コピーの問題(`/ux-copy` を使う)。モーションの問題(`/ux-motion` を使う)。a11y の問題(`/ux-a11y` を使う)。
- **呼び出し方:** `/ux-polish src/components/Hero.tsx`、`/ux-polish out/landing.html --css out/landing.css`、`/ux-polish out/landing.html --loop-only --rounds 5`。
- **出力:** ループからの `<file>.evolved.html`(`--loop-only` か `--fix` のときだけ元のファイルに昇格)、`--fix` での更新済みコード、`.ux/last-evolve.json`、`.ux/decisions.jsonl` への 1 行、そしてテイストの指摘を記した `.ux/last-polish.json`。
- **次に繋がる:** `/ux-lint` → ポリッシュが保たれているか検証。`/ux-a11y` → アクセシビリティを再確認。

### discovery & 物語

#### `/ux-research`：リサーチ計画 + 統合

- **何をするか:** 計画モード:インタビュースクリプト、サーベイ、リクルートのスクリーナーを書きます。統合モード(`--synthesize`):インタビュー、分析、競合サイト、A/B 結果、サポートチケットを推奨に消化します。`research-synthesizer` を派遣。
- **使うタイミング:** 「リサーチ研究を計画」「インタビューの質問が必要」「サーベイを設計」「ユーザーをどう募集」「ユーザーテスト計画」「ダイアリースタディ」「プリファレンステスト」「フェイクドア」「スモークテスト」「インタビューメモを統合」。
- **スキップするタイミング:** 答えが高い確信度で既知。低リスクで可逆的な決定。バックエンドやインフラ。
- **呼び出し方:** `/ux-research --plan "loyalty wallet adoption in MENA"` または `/ux-research --synthesize interviews/*.md`。
- **出力:** `.ux/last-research.json` を書き出します、リサーチプランか、統合されたテーマ + エビデンス + 推奨。
- **次に繋がる:** `/ux-discover --frame` → 知見をフレームに統合。`/ux-design` → 知見から生成。`/ux-workshop` → リサーチを入力にワークショップを実行。

#### `/ux-workshop`：5 段階のデザインシンキングワークショップ

- **何をするか:** discovery / デザインシンキングのワークショップを端から端まで進行します。5 つの順序段階(探索 → ヒートマップ → ステークホルダーマップ → 解決策スケッチ → ゲームプラン)。時間枠付き。段階ごとに具体的なアーティファクト。「興味深い発見」ではなく決定で終わります。
- **使うタイミング:** 真の問い、真の参加者、真の時間予算。「ワークショップを進行」「discovery を進行」「デザインシンキングをやろう」「ステークホルダーが 1 時間いる、何をする」「プロジェクトをキックオフ」。
- **スキップするタイミング:** ブリーフがすでに明確でスコープされている。単独でのブレスト(`/ux-design` か `/ux-discover --frame` を使う)。チームが実行中で discovery にいない。
- **呼び出し方:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`。
- **出力:** `.ux/last-workshop.json` を書き出します、ゲームプラン + 段階別アーティファクト。
- **次に繋がる:** `/ux-design` → ゲームプランを実行。`/ux-research` → ワークショップが浮かび上がらせたギャップを埋める。`/ux-case-study` → 旅路を公開。

#### `/ux-case-study`：公開可能なケーススタディ(Wfrah エディトリアル形式)

- **何をするか:** 純モノクロのエディトリアル形式でプロジェクトのケーススタディを生成します。Wfrah タイポ、ヘアラインの区切り、(A) から (G) までの番号付きセクションコード、バイリンガル対応のレイアウト。ドキュメントであり、マーケティングのパンフレットではありません。`.ux/last-frame.json`、`.ux/last-workshop.json`、`.ux/last-research.json`、`.ux/last-design.json`、`.ux/last-a11y.json`、`.ux/last-polish.json`、`.ux/last-recommendation.json`、`.ux/last-discovery.json` から読み込みます。
- **使うタイミング:** ローンチ後。個別マイルストーン後。「ケーススタディを書いて」「このプロジェクトをケーススタディに」「まとめドキュメントを作って」「この仕事を公開して」「ポートフォリオ作品」。
- **スキップするタイミング:** プロジェクトに (A) から (G) のセクションを埋めるデータがない。ケーススタディではなくマーケティングのランディングが欲しい(`/ux-design` を使う)。
- **呼び出し方:** `/ux-case-study --format=html --slug=bashiti-loyalty`。
- **出力:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`。
- **次に繋がる:** ターミナルコマンド、通常はプロジェクトの終止符。

### コンダクター

#### `/ux-next`：ワークフローコンダクター(読み取り専用)

- **何をするか:** すべての `.ux/last-*.json` を読み、最もレバレッジの高い次のコマンドを指名します。コンダクター、ビルダーではない。読み取り専用。
- **使うタイミング:** コマンドの合間。「次は何をすべき」「次の一手は」「私の代わりに決めて」「ここからどこへ」。
- **スキップするタイミング:** `.ux/` に先行レポートがない。具体的な次のコマンドがすでにある。
- **呼び出し方:** `/ux-next`(引数なし)または `/ux-next --focus=a11y`。
- **出力:** 標準出力、推奨する次のコマンド + 根拠。
- **次に繋がる:** 選ばれたコマンドへ。

#### `/ux-expert`：コンサルティングフック

- **何をするか:** ユーザーが実在の UX 専門家を求めるとき、プラグイン作者の連絡先を表示します。簡潔、直接、マーケなし。
- **使うタイミング:** 「これは誰が作った」「UX エキスパートが必要」「コンサルティングはやる?」「これで誰か雇えるか」「このプラグインの背後に人はいる?」。
- **スキップするタイミング:** ユーザーがプラグインの機能を尋ねている、コンサルティングでない。
- **呼び出し方:** `/ux-expert`。
- **出力:** LinkedIn / メール / リポジトリの簡潔なコンタクトカード。

### エイリアス、4.1 で廃止

3.x の 7 つのコマンドは上の 18 に統合されました。古い名前はもう 1 リリースの間使えます。各エイリアスは移動先を示したうえで、同じ引数で新しいコマンドを実行します。

| 旧コマンド | 現在 | 備考 |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | 同じフレーミングブロック、同じ `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | MCP ツール `ux_recommend` は変更なし |
| `/ux-stats` | `/ux-init --stats` | 読み取り専用のスナップショット |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | エイリアスは従来の 5 ラウンドの上限を維持。`/ux-polish` 単体は 3 で止まる |
| `/ux-component` | `/ux-design --component` | 同じ `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | 同じ `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | 画像から構築するには `--extract-only` を外す |

### コマンドチェーンのグラフ

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

## 5 つのサブエージェント

サブエージェントはコマンドが派遣する役割特化型のジェネレーターです。単独では実行されず、`/ux-design`、`/ux-system`、`/ux-fix`、`/ux-research` などから呼ばれます。各エージェントには明確な責任範囲があり、ブリーフを決めるのではなく、ブリーフに沿って実行します。

### `frontend-engineer`

- **担当:** プロダクション級フロントエンドコード(React、Next.js、Vue、Blade+Alpine、純 HTML、Astro)を反 AI スロップの規律で。
- **派遣元:** `/ux-design`(ページ、コンポーネント、ダッシュボード、画像の各モード)、`/ux-fix`。
- **入力:** ブリーフ + クリエイティブディレクション + tokens(`.ux/last-recommendation.json` から)。
- **出力:** 汎用 AI 出力と区別できる動くコード。紫グラデーションなし、ヒーロー中央寄せなし、等大 3 カードなし、ディスプレイサイズの Inter なし、「John Doe」なし、絵文字なし、300ms デフォルトなし。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### `motion-engineer`

- **担当:** プロダクションフロントエンドコード内のモーション、Framer Motion、GSAP、CSS アニメーション。デュレーション、イージング、振り付け、reduced-motion フォールバック、パフォーマンス規律。
- **派遣元:** `/ux-design`(全モード)、`/ux-motion --fix`。
- **入力:** モーションブリーフ + tokens + `data/motion-presets.json` から 57 のモーションプリセット。
- **出力:** その場所を勝ち取るモーション。常に `prefers-reduced-motion` フォールバックで包む。常に Core Web Vitals に対してテスト。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### `copy-writer`

- **担当:** 出荷される文字列、エラーメッセージ、空ステート、CTA、ローディングステート、成功メッセージ、トースト、ヘルパーテキスト、フォームラベル、ボタンテキスト。
- **派遣元:** `/ux-copy --fix`、`/ux-design`(全モード)、`/ux-discover --frame`。
- **入力:** ボイスプロファイル(名前指定または貼り付け) + 画面の文字列。
- **出力:** 画面のすべてのステート横断で一貫適用されるプロダクションマイクロコピーで、製品がばらばらの十個ではなく、ひとつの製品として聞こえる。禁止:「フォームにエラーがあります」「John Doe」、AI 的にはしゃぐ祝賀コピー、汎用 CTA、生気のない空ステート。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### `research-synthesizer`

- **担当:** リサーチ入力(インタビュー、分析、競合サイト、A/B 結果、サポートチケット)を実行可能なデザイン推奨に消化する。
- **派遣元:** `/ux-research`、`/ux-workshop`、`/ux-discover --frame`。
- **入力:** 生のリサーチ素材、トランスクリプト、エクスポート、競合 URL、サポートクラスター。
- **出力:** テーマ、エビデンス、推奨。答えをデザインしない、デザイナーがデザインするための基層を渡します。
- **ツール:** `Read, Write, WebFetch, Bash, Glob, Grep`。

### `design-system-architect`

- **担当:** 完全なデザインシステム、tokens(色、タイプ、空間、モーション、角丸、影)、基盤ドキュメント、コンポーネントコントラクト、ダークモードペアリング、テーマ層。
- **派遣元:** `/ux-system`、システムが存在しないときの `/ux-design --component`。
- **入力:** ブランドブリーフ + `.ux/last-recommendation.json`(スタイル + パレット + タイプペア + モーションプリセット)。
- **出力:** 一貫性、立場、プロダクション準備が揃ったシステムで、下流エージェントが基礎を再決定せず構築できる。tokens JSON、基盤 MD、コンポーネントコントラクト、ダークモードマッピング。
- **ツール:** `Read, Write, Edit, Bash, Glob, Grep`。

### サブエージェント派遣プロトコル

コマンドがサブエージェントを派遣するとき、渡すもの:

1. ブリーフ / 推奨(`.ux/` からロード)。
2. 関連するマニフェストスライス(例:`frontend-engineer` は選定スタイル + パレット + コンポーネントを得る;`motion-engineer` は選定モーションプリセットを得る)。
3. 171 のアンチパターンガードレール(常に有効)。
4. 成功基準(アーティファクトは何を満たすべきか)。

サブエージェントが返すもの:

1. アーティファクト(コード、ドキュメント、システム)。
2. 根拠ブロック(なぜこの選択か)。
3. ガードレールへの自己チェック(どのルールを検証したか)。

呼び出し側のコマンドは完了を宣言する前に自動で `/ux-lint` を実行します。

---

## 11 のデータマニフェスト

データ層が脳です。すべてのコマンドはそこから読み、エンジンはそれを横断してマージし、リンターはそれに対してスキャンします。すべてのファイルは `data/` 下にあり、エントリを `{_meta, entries}` で包んでスキーマバージョニングを行います。

### `styles.json`：84 のデザインスタイル

| フィールド | 説明 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`、`name`、`category`、`philosophy`、`when_to_use`、`when_to_skip`、`tokens`、`references`、`compatible_palettes`、`compatible_type_pairs`、`compatible_motion`、`compatible_industries`、`taste_score` |
| `categories` | Minimalist / Swiss、Brutalist、Editorial、Glassmorphism、Neumorphism、Bento、Skeuomorphic、Industrial、Maximalist、AI-Futurist、MENA-modern、Vaporwave など |
| `sample entry` | `swiss-international`、「グリッドは法。タイプが重労働をこなす。装飾は失敗。」 |

使用:`/ux-discover`、`/ux-system`、`/ux-design`。スキーマ:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `palettes.json`：176 のカラーパレット

| フィールド | 説明 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`、`name`、`mode`(明/暗)、`tone`、`colors`(canvas、surface、ink、body、muted、primary、primary_active、hairline、success、warning、danger、accent)、`wcag_contrast_audit`、`compatible_industries` |
| `tones` | warm、editorial、magazine、clinical、playful、brutalist、monochrome、jewel-tone、MENA-warm、dev-tools-dark など |
| `sample entry` | `claude-warm-editorial`、明、warm/editorial/magazine、canvas #faf9f5、primary #cc785c |

使用:`/ux-discover`、`/ux-system`。コントラストは AA / AAA で検証済み。スキーマ:[data/SCHEMAS.md](data/SCHEMAS.md)。

### `type-pairs.json`：70 のタイプペアリング

| フィールド | 説明 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`、`name`、`display`(family + weights + source + license + URL)、`body`、`mono`、`compatible_styles`、`taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`、Cormorant Garamond × Inter × JetBrains Mono |

すべてのファミリーにライセンス + ソース URL があります。`/ux-discover`、`/ux-system` で使用。

### `components.json`：148 のコンポーネント

| フィールド | 説明 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`、`name`、`category`、`purpose`、`anatomy`、`states`、`tokens_used`、`motion`、`accessibility`、`compatible_styles`、`compatible_industries`、`code_skeleton` |
| `categories` | Navigation、Forms、Data Display、Feedback、Overlays、Layout、Content、Marketing、E-commerce、Auth、Dashboard、Charts、Empty States、Loading States、Error States |
| `sample entry` | `mega-nav-product-grid`、Mega Navigation、Product Grid、6 パーツの解剖、4 ステート |

これが私たちの最大の堀です。他の Claude UX プラグインは構造化コンポーネントマニフェストを同梱していません。

### `industries.json`：184 の業種ルール

| フィールド | 説明 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`、`name`、`category`、`characteristics`、`audience_signals`、`recommended_styles`、`recommended_palettes`、`recommended_type_pairs`、`recommended_motion`、`regulatory_notes`、`regional_notes` |
| `categories` | Financial Services、Healthcare、Education、E-commerce、SaaS B2B、SaaS B2C、Developer Tools、Media、Gaming、Travel、Real Estate、MENA-specific など |
| `sample entry` | `fintech-neobank`、高信頼、規制開示、残高/取引が主 UI、日次利用のモバイル優先 |

レコメンダー(`/ux-discover`)が最初の並列検索軸として使用。

### `chart-types.json`：35 のチャートタイプ

| フィールド | 説明 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`、`name`、`category`、`when_to_use`、`when_to_skip`、`encoding`、`accessibility`、`data_shape`、`compatible_styles` |
| `categories` | Comparison、Time Series、Distribution、Composition、Relationship、Flow、Geographic |
| `sample entry` | `bar-vertical`、4 から 15 の離散カテゴリを比較。x 軸の位置がカテゴリに、高さが値に対応。 |

`/ux-design --dashboard` と `/ux-design --component`(チャートのインスタンス)で使用。

### `tech-stacks.json`：25 のスタック

| フィールド | 説明 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`、`name`、`category`、`tier`、`languages`、`ssr`、`rsc`、`compatible_styling`、`scaffold_command`、`compatible_motion`、`gotchas` |
| `tiers` | production、prerelease、experimental |
| `sample entry` | `nextjs-15-app-router`、Next.js 15(App Router)、TS/JS、SSR、RSC、Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css と互換 |

他のスタックは Astro、SvelteKit、Remix、Nuxt 3、Solid Start、Qwik、Blade+Alpine、Hotwire、Phoenix LiveView、Hydrogen 2025 など。

### `ux-guidelines.json`：112 の名前付き UX ロー

| フィールド | 説明 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`、`name`、`category`、`source`、`principle`、`application`、`examples`、`caveats`、`related_laws` |
| `categories` | Decision Cost、Attention、Memory、Motor Control、Visual Perception、Social、Emotional、Form、Error Handling、Onboarding、Empty State など |
| `sample entry` | `hicks-law`、意思決定時間は提示された選択肢数に対数的に増加する |

`/ux-audit`(6 レンズ採点)と `/ux-critique`(審美の錨)で使用。

### `motion-presets.json`：57 のモーションプリセット

| フィールド | 説明 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`、`name`、`category`、`tokens`(duration_ms、easing、transform_from/to、opacity_from/to)、`stacks`(framer_motion、gsap、css)、`accessibility`(reduced-motion フォールバック)、`when_to_use` |
| `categories` | Entry、Exit、Hover、Focus、Tap、Loading、Empty、Success、Error、Scroll-linked |
| `sample entry` | `fade-up-12px`、360ms、`cubic-bezier(0.16, 1, 0.3, 1)`、translateY(12px) → 0、opacity 0 → 1 |

各プリセットに reduced-motion バリアントがあります。Framer Motion、GSAP、純 CSS 向けのスタック対応コード。

### `anti-patterns.json`：171 のルール

| フィールド | 説明 |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`、`name`、`severity`(critical/high/medium/low)、`category`、`detection`(種類、パターン、フラグ、スコープ、多くのルールではパース済みファイルに対する `post` 検査)、`why`、`fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

ルールの全一覧は [171 の反 AI スロップルール](#171-の反-ai-スロップルールリンター)にあります。

### `brands/*.json`：160 のブランド仕様

| フィールド | 説明 |
|---|---|
| `entries` | 160(さらに全リストを示す `_index.json`) |
| `keys per entry` | `id`、`name`、`category`、`voice`、`tokens`(color、type、motion)、`design_principles`、`signature_moves`、`anti-moves`、`references` |
| `categories` | Developer Tools(36)、Consumer / Lifestyle / Retail(19)、Fintech / Crypto(14)、Editorial / Media(13)、AI / ML Platform(12)、Productivity / Collaboration(8)、Automotive(8) |

完全な一覧は [160 のブランド DESIGN.md 仕様](#160-のブランド-designmd-仕様カテゴリ別)。

---

## 171 の反 AI スロップルール：リンター

ux-skill は決定論的なリンターを同梱しています。各ルールはパターンで、多くはパース済みの CSS とマークアップに対する検査を加えるため、一致はルールが示す文脈でのみ数えられます。**LLM なし。** **API なし。** **ネットワークなし。** 一般的な Next.js アプリなら CI で ~200ms で動きます。`--fail-on high` を設定すると、Critical / High の指摘で非ゼロ終了します。

ルールは `data/anti-patterns.json`(v2、推奨)を元にし、フォールバックとして `references/foundations/anti-patterns.md`(v1、bash)を使います。同梱されるバイナリは 2 つ:`bin/ux-lint.py`(Python、高速、拡張可能)と `bin/ux-lint.sh`(Bash + perl-PCRE、Python のない環境向け)。

### カテゴリ別ルール

171 のルールすべてをカテゴリ別、続いて重大度順に並べたカタログは、`data/anti-patterns.json` から[英語版 README](README.md#rules-by-category) に生成されます。ルール ID と名前はリンターが出力するとおりに載っています。ルールカバレッジ:A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2)。

### リンターの使用

**単発スキャン:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  evidence: grid grid-cols-3 gap-6 (3 equal Card children)
  fix: feature one card; flank with two reduced-emphasis cards

3 files scanned · 2 high · 0 medium · 0 low · exit 1
Recommended next: /ux-polish --fix (LLM-driven, addresses both lintable and aesthetic findings)
```

---

## 160 のブランド DESIGN.md 仕様：カテゴリ別

本物のブランド。本物のデザイン言語。本物の DESIGN.md 仕様、汎用パレットではありません。プラグインに「Stripe のスタイルでランディングを作って」と頼むと、実際のブランドボキャブラリを読みます:ボイスルーブリック、カラー token、モーション規約、シグネチャムーブ、アンチムーブ。

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

他の 8 つの人気 Claude UX プラグインは「モダンミニマル」や「クリーンダッシュボード」、同じデフォルト美学のバリアントを生成します。ux-skill は **Linear の明瞭さ**、**Stripe の真剣さ**、**Apple の抑制**、**Tesla のモノリス感**、**Notion の親しみ**、**Cursor のグラデーション規律**、**Raycast のヘアライン密度**、**Claude の暖色エディトリアル** を要求でき、エンジンはブランド仕様から正しい token、ボイス、モーション規約、シグネチャムーブを引き出します。

---

## MCP サーバー：非対称な一手

ux-skill は **Model Context Protocol サーバー** を同梱します。`ux-mcp` を実行するとエンジンは常駐の stdio プロセスになり、任意の MCP 対応ホスト(Claude Desktop、Cursor、Windsurf、汎用エージェント)から呼び出せます。25 のツール:`ux_recommend`、`ux_system_detect`、`ux_lint`、`ux_styles`、`ux_palettes`、`ux_type_pairs`、`ux_components`、`ux_industries`、`ux_motion_presets`、`ux_anti_patterns`、`ux_brands`、`ux_landing_patterns`、`ux_persist_save`、`ux_persist_load`、`ux_stats`、`ux_image_extract`、`ux_synthesize`、`ux_decisions_query`、`ux_decisions_stats`、`ux_system_build`、`ux_system_import`、`ux_system_enhance`、`ux_system_extend`、`ux_system_export`、`ux_contracts_check`。スラッシュコマンドが使うのと同じ Python ハンドラー、同じデータマニフェスト、同じ決定論的レコメンダーです。

**なぜこれが非対称な一手か:** トップ 8 の Claude UX スキル(ui-ux-pro-max-skill、open-design、taste-skill、huashu-design、stitch、nothing-design、hallmark、material-3)はどれも MCP サーバーを同梱していません。Claude Code のプラグインランタイムに閉じ込められています。ux-skill は MCP を話す任意のホストから到達可能で、Claude Code プラグインを聞いたこともないエージェントからも届きます。

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

クライアントを `ux-mcp` バイナリに向けてください。完全なツールドキュメント、JSON 例、Claude Desktop、Cursor、Windsurf のクライアント別設定は [docs/mcp.html](docs/mcp.html) と `commands/ux-mcp.md` に。

---

## 17 IDE 向けインストーラー

`uxskill init`(Claude Code 内では `/ux-init`)はどの IDE を使っているか自動検出し、正しいアーティファクトを書き出します。同じ Python エンジン。同じ推奨。IDE ごとに違う糊。

| IDE / ツール | 検出シグナル | インストールされるアーティファクト |
|---|---|---|
| Claude Code | `.claude/` または `CLAUDE.md` | `.claude-plugin/plugin.json` のプラグインマニフェスト + 全 18 コマンド(と 7 つのエイリアス)+ 全 5 サブエージェント |
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

## ユースケース：具体的なシナリオ

8 つの実シナリオ。あなたの状況に最も近いものを選び、呼び出しを適応させてください。

### 1. Cursor でフィンテックダッシュボードを構築

Cursor で MENA ネオバンクのダッシュボードを作っています。プラグインをインストールし、discovery、recommendation、そしてダッシュボード生成を順に実行します。

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

そして Cursor に頼みます:*「.ux/last-recommendation.json の推奨を使ってダッシュボード画面を生成」*。Cursor は `.cursorrules` ヘッダを読み、推奨をロードし、明示的な制約付きでダッシュボード生成を派遣します。

### 2. Claude Code で Stripe スタイルのランディングを生成

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

3 つのコマンド、1 つのポリッシュされた画面、修正ごとにアトミックなコミット。

### 5. Linear スタイルのコマンドパレットを設計

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

生成されるコンポーネントは Linear の実際のカラー token、タイプスタック、モーション規約、ヘアライン密度を使用します、「汎用ダーク UI」ではなく。

### 6. ステークホルダーと 90 分のデザインシンキングワークショップを開催

5 人を 90 分。「雰囲気」ではなくゲームプランを持って退室してほしい。

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

プラグインが 5 段階(探索 → ヒートマップ → ステークホルダーマップ → 解決策スケッチ → ゲームプラン)を端から端まで時間枠付きで進行し、段階ごとに具体的なアーティファクトを生成します。出力は `.ux/last-workshop.json`、「興味深い発見」ではなくゲームプラン。

### 7. ローンチ後に公開可能なケーススタディを書く

ロイヤルティウォレットを出荷しました。ポートフォリオピースが欲しい。

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

ケーススタディは完成された公開可能なアーティファクト、草稿ではありません。純モノクロ、エディトリアルタイポ、あなたのポートフォリオに即出荷可能。

### 8. 非 AI 環境で discovery を実行(構造化インテークだけ)

プロジェクトをスコープしています。まだ推奨は不要、構造化されたブリーフが必要。

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

JSON をチームに渡せます、Notion ドキュメントに貼れます、別の AI ツールに供給できます。ux-skill はエンジンであるだけでなく、構造化インテークツールでもあります。

### 9. MASTER.md 永続化：リポジトリ内のデザイン決定

`/ux-discover`(または `/ux-discover --recommend`)の後、選定したスタイル + パレット + タイプ + モーション + コンポーネント + ブランド事例 + ガードレールを、チームがレビュー、差分確認、バージョン管理できる読みやすい Markdown ファイルとして保存します。

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md`(YAML フロントマター + 本文)と、`persist save-page` 経由で生成済み画面ごとに `.ux/design-system/pages/<name>.md` を書き出します。冪等、同じ入力はバイト単位で同じ出力を生むので、状態が変わらない再実行は git で no-op です。

---

## 他の選択肢との比較

簡潔なサマリー表。完全な列ごとの比較は [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)。

| 次元 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| スラッシュコマンド | **18** | 1 | 19 | 1 | 1 | 複数 | 1 | 1 | 1 |
| コンポーネント | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| モーションプリセット | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ブランド仕様 | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| アンチパターンルール | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 安全な決定論的リンター | **はい** | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| 対応 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery ゲート | **10 フィールド** | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 | 暗黙 |
| `.ux/` 状態チェーン | **はい** | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ | いいえ |
| スター数(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 正直な評価

- **ui-ux-pro-max** は認知度で勝り、18 IDE を出荷し、CSV 上で BM25 風検索を持ちます。コンポーネントマニフェスト、モーションマニフェスト、ブランドライブラリ、決定論的リンターはありません。
- **open-design** は 19 スキル + プレビューを持ちますが、Claude Code のみのサポートで反スロップ層もありません。
- **hallmark** は精神的に最も近い(同じく反スロップ)ですが、単一スキル、エンジンも、マニフェストも、チェーンコマンドもありません。
- **material-3-skill** は特に Material Design 3 が欲しい時に優れています。MD3 では競いません。

次元ごとの完全な詳細は [compare.html](https://uxskill.laithjunaidy.com/compare.html)。

---

## ロードマップ

今後(リリース時期は未定):

- **Figma スタイル**:影のエフェクトスタイル、グリッドスタイル、フィールド変数に結び付いたテキストスタイルを、ライブのファイルに書き込みます。
- **コンポーネントのマッピング**:Figma のコンポーネントとそのバリアントを、コードのコンポーネントとその props に対応付け、ハンドオフを通じて保持します。
- **ライブサイトのインポーター**:公開サイトが実際にレンダリングしているシステムを、ファイルのインポーターと並んで読み取ります。
- **構築済みシステムのドキュメントページ**:トークン、ロール、コントラクトを人が読める形で見せます。

ほかに検討中のもの:

- **`uxskill lint --fix` による安全な書き換え**:機械的に直せる指摘が対象(button-no-type、img-no-alt の空文字列、console-log-leak の削除)。
- lint の指摘をインラインで表示する **VS Code 拡張**。
- 6 つのスタックでの**コンポーネント単位のコード出力**(Next.js + React、Vue 3 + Nuxt、SvelteKit、Astro、Blade + Alpine、素の HTML/CSS)。
- **ブランド仕様のマーケットプレイス**:コミュニティのブランド仕様を公開し、見つけられる場所。
- **独自のアンチパターンルール**:プロジェクトが `data/anti-patterns.local.json` で定義するルールの発見と共有。
- **`uxskill plan`**:ひとつの画面だけでなく、ブリーフから複数ページのサイトを計画。

---

## コントリビューション

issue と PR を歓迎します。3 つの高レバレッジ領域:

### アンチパターンルールを追加

1. `data/anti-patterns.json` を編集、`id`、`name`、`severity`、`category`、`detection.pattern`、`detection.flags`、`detection.scope`、`evidence_template`、`fix`、`references` を持つエントリを追加。
2. `tests/linter/` にテストを追加、ルールをトリガーするファイルとしないファイル。
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx` を実行、発火を確認。`tests/linter/should-not-trigger/<rule>.tsx` を実行、発火しないことを確認。
4. PR を開く。

### ブランド仕様を追加

1. `data/brands/<slug>.json` を `id`、`name`、`category`、`voice`、`tokens`、`design_principles`、`signature_moves`、`anti-moves`、`references` で作成。
2. 対応する散文を `references/brands/<slug>.md` に追加。
3. `data/brands/_index.json` に登録。
4. PR を開く。仕様は第一次情報源によって裏付けられねばなりません(ブランドの実際の製品、公開デザインシステム、公開している場合の DESIGN.md)。

### モーションプリセットを追加

1. `data/motion-presets.json` を編集、`id`、`name`、`category`、`tokens`、`stacks`(framer_motion、gsap、css)、`accessibility.reduced_motion_fallback`、`when_to_use` を持つエントリを追加。
2. プリセットには reduced-motion バリアントが必須。例外なし。
3. PR を開く。

### プロセス

- 完全なプロセスは [CONTRIBUTING.md](CONTRIBUTING.md)。
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) を読む。
- 新規ルールとブランド仕様は次の点でレビューされます:第一次情報源での裏付け、単一プロジェクトへの過適合なし、データ内に絵文字なし、該当する場合の RTL 安全動作。

---

## ライセンス、作者、謝辞

### ライセンス

MIT。使う、フォークする、その上に構築する。AI スロップを出荷せずに済んだなら、リポジトリにスターを、最も安価な支援方法です。

### 作者

**Laith Aljunaidy**：MENA 優先のロイヤルティプラットフォーム [Dot](https://thedotwallet.com) の独立創業者。AI 生成のフロントエンドが皆同じに見えないように ux-skill を作っています。

- LinkedIn:[linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- メール:laith.aljunaidy.laith@gmail.com
- リポジトリ:[github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- サイト:[uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI:[pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm:[npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 謝辞

- Claude Code と、これを配布可能にしたスキル / プラグインアーキテクチャを提供してくれた Anthropic チームに。
- Nielsen Norman Group、Laws of UX(lawsofux.com)、そして `data/ux-guidelines.json` の根拠となる仕事をした UX リサーチコミュニティに。
- `data/brands/` にリストされたすべてのブランドに、公開デザインシステムがブランド仕様の真実の源泉です。
- 元の v1 コントリビューターに:v2 Python エンジンの種となった一発撮りの Claude スキル。
- 比較した 8 つの人気 Claude UX プラグインに、彼らがバーを上げた;これが私たちの答え。

---

**ux-skill** · **v4.0.0** · Claude Code、Cursor、Windsurf、その他すべての AI コーディングツールが、AI 生成と読まれないフロントエンドを出力するために構築。

> [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) でリポジトリにスター · `pip install uxskill` または `npx uxskill init` でインストール · [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) で比較をブラウズ
