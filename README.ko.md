[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **한국어** · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — Claude Code, Cursor, 그리고 모든 AI 코딩 도구를 위한 디자인 인텔리전스 엔진

> **AI 코딩을 위한 가장 강력한 UX 플러그인.** 11개의 쿼리 가능한 JSON 매니페스트(84개 스타일, 176개 팔레트, 70개 타입 페어링, 148개 컴포넌트, 184개 산업, 35개 차트 타입, 57개 모션 프리셋, 112개 UX 법칙, 145개 안티패턴 규칙, 25개 기술 스택, 160개 브랜드 사양), 22개의 슬래시 명령, 5개의 서브에이전트, 그리고 결정론적 반 AI-슬롭 린터를 갖춘 Python 추론 코어. 크로스 IDE: Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer, Roo Cline에 탑재됩니다.

> **브랜드 이름은 `ux-skill`입니다.** PyPI / npm 패키지명은 그대로 `uxskill`입니다. GitHub 저장소는 [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)에 있습니다.

**사이트:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **모든 Claude UX 플러그인과의 비교:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.0.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-인스톨러)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Star 히스토리

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill란 무엇인가

ux-skill은 AI 코딩 도구를 위한 **디자인 인텔리전스 엔진**입니다. Python 패키지로(`pip install uxskill`), Claude Code 플러그인으로, 그리고 17 IDE용 멀티 인스톨러로 동작합니다. 엔진은 프로젝트 브리프(산업, 청중, 톤, 필수 항목, 금지 항목, 스택, 지역)를 받아 추천 디자인 시스템 한 벌을 반환합니다: 스타일, 팔레트, 타입 페어, 모션 프리셋, 컴포넌트, 연구할 브랜드 본보기, 그리고 지켜야 할 안티패턴 가드레일. 추천은 결정론적입니다 — 같은 입력은 항상 같은 출력을 만들어냅니다.

플러그인은 당신과 AI 코딩 도구 사이에 자리합니다. Claude Code, Cursor 또는 다른 AI 어시스턴트에게 "핀테크 랜딩 페이지 만들어줘"라고 요청하면, 어시스턴트는 보통 즉흥적으로 만듭니다 — 그리고 결과는 5초 안에 AI 생성으로 식별됩니다(보라색에서 파란색 그라데이션, 같은 크기의 카드 세 개, 디스플레이 크기의 Inter, 추천사의 "John Doe", 기본 300ms 트랜지션, 가운데 정렬 히어로, CTA의 튀는 화살표). ux-skill은 즉흥을 **구조화된 제약**으로 대체합니다: `/ux-discover`로 브리프를 잡고, `/ux-recommend`로 시스템을 고르고, `/ux-design`으로 코드를 만들고, `/ux-lint`로 커밋 전에 100개의 결정론적 반 AI-슬롭 규칙을 통과하는지 검증합니다.

이 README가 정전(正典) 참조입니다. 모든 명령, 모든 서브에이전트, 모든 데이터 매니페스트, 모든 설치 경로, 모든 브랜드 사양, 모든 안티패턴 카테고리 — 전부 여기에 문서화되어 있습니다. Claude Code 디자인 플러그인을 찾고 있거나 Cursor, Windsurf, Codex용 AI 디자인 도구를 비교하고 있다면, 이걸 처음부터 끝까지 읽고 [compare.html](https://uxskill.laithjunaidy.com/compare.html)을 나란히 두고 보세요.

---

## 목차

1. [빠른 설치](#빠른-설치)
2. [숫자 — 상위 8개 Claude UX 스킬과의 실시간 비교](#숫자--상위-8개-claude-ux-스킬과의-실시간-비교)
3. [아키텍처 — 부품들이 어떻게 맞물리는가](#아키텍처--부품들이-어떻게-맞물리는가)
4. [22개의 슬래시 명령 — 상세 레퍼런스](#22개의-슬래시-명령--상세-레퍼런스)
5. [5개의 서브에이전트](#5개의-서브에이전트)
6. [11개의 데이터 매니페스트](#11개의-데이터-매니페스트)
7. [145개의 반 AI-슬롭 규칙 — 린터](#145개의-반-ai-슬롭-규칙--린터)
8. [160개의 브랜드 DESIGN.md 사양 — 카테고리별](#160개의-브랜드-designmd-사양--카테고리별)
9. [MCP 서버 — 비대칭 한 수](#mcp-서버--비대칭-한-수)
10. [17 IDE 인스톨러](#17-ide-인스톨러)
11. [사용 사례 — 구체적인 시나리오](#사용-사례--구체적인-시나리오)
12. [다른 대안들과의 비교](#다른-대안들과의-비교)
13. [로드맵](#로드맵)
14. [기여하기](#기여하기)
15. [라이선스, 저자, 감사의 말](#라이선스-저자-감사의-말)

---

## 빠른 설치

세 가지 설치 경로. 환경에 맞는 것을 고르세요.

### 경로 1 — Claude Code 마켓플레이스(정전)

Claude Code 안에서 일한다면, 플러그인 마켓플레이스를 통해 설치합니다:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

이것으로 22개의 슬래시 명령과 5개의 서브에이전트가 Claude Code 세션에 연결됩니다. 설치 후 `/ux-init`을 실행해서 프로젝트별 `.ux/` 상태 디렉터리를 설정하고 Python 엔진이 도달 가능한지 검증하세요.

### 경로 2 — pip(범용)

Claude Code 밖에서 일한다면(Cursor, Windsurf, CLI, CI), Python 패키지를 설치합니다:

```bash
pip install uxskill
uxskill init                       # IDE를 자동 감지하고, 올바른 아티팩트를 설치
uxskill stats                      # 매니페스트 개수를 출력해 설치를 검증
uxskill lint .                     # 현재 디렉터리에 린터 실행
```

패키지는 CLI 진입점으로 `ux`와 `uxskill` 두 가지를 노출합니다 — 같은 바이너리입니다.

### 경로 3 — npx(Python 직접 관리 불필요)

Python을 직접 관리하고 싶지 않다면, npx 래퍼가 `pipx`를 통해 모든 것을 부트스트랩합니다:

```bash
npx uxskill init                  # 최초 실행 시 pipx + uxskill을 다운로드
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### 설치 검증

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

개수가 0으로 반환되면 JSON 파일이 누락된 것입니다 — [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues)에 이슈를 열어주세요.

---

## 숫자 — 상위 8개 Claude UX 스킬과의 실시간 비교

스타 수는 **2026-05-28**에 `gh api`로 마지막으로 확인했습니다. ux-skill(Laith0003/ux-skill)은 가장 늦게 진입한 사람입니다 — 인지도는 작고, 아키텍처는 깊습니다. 아래 비교는 솔직합니다: 어디서 지고, 어디서 이기는가.

| 플러그인 | 스타 수 | 아키텍처 | 슬래시 명령 | 린터(CI 안전) | 브랜드 사양 | 컴포넌트 | 모션 프리셋 | 지원 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV, 단일 스킬 | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19개 스킬 + 미리보기 | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + 리서치 기반 안목 | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 단일 62 KB SKILL.md + 스크립트 | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | MCP에 연결된 스킬 라이브러리 | 다수 | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 단일 미학 스킬 | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 반 슬롭 디자인 스킬 | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 컴포넌트 + 감사 | 1 | — | (MD3 전용) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python 엔진 + 11개 매니페스트 + 22개 명령 + 5개 서브에이전트 + CI 린터** | **22** | **145개 regex 규칙** | **110** | **148** | **57** | **17** |

### 지는 곳

- **인지도.** 그들은 수십만 스타를 가지고 있습니다. 우리는 14개. 스타를 눌러주세요 — 가장 저렴한 도움 방법입니다.
- **브랜드 인지.** ui-ux-pro-max와 open-design는 일이 아닌 달 단위로 앞서 있습니다.
- **마케팅 윤기.** 스크린샷, 데모 영상, 찾기 쉬운 랜딩 페이지가 있습니다. 우리에게는 철저한 README와 가벼운 랜딩만 있습니다.

### 이기는 곳

- **컴포넌트 라이브러리:** 해부, 상태, 사용한 토큰, 모션 사양을 포함한 148개의 문서화된 컴포넌트. 다른 8개 중 어느 것도 컴포넌트 매니페스트를 출시하지 않습니다.
- **모션 프리셋:** 스택 준비된 57개 항목(Framer Motion, GSAP, CSS), reduced-motion 폴백 포함. 다른 어떤 곳도 모션 매니페스트를 출시하지 않습니다.
- **안티패턴 린터:** 145개의 결정론적 regex 규칙, CI에서 실행되며 Critical/High에서 비영(非零) 종료. 다른 어떤 곳도 결정론적 린터를 출시하지 않습니다.
- **브랜드 사양:** 110개의 실제 DESIGN.md 사양(Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude 외 96개). 다른 어떤 곳도 브랜드 라이브러리를 출시하지 않습니다.
- **17 IDE 지원:** 같은 엔진, IDE마다 다른 접착제.
- **22개의 슬래시 명령:** discovery, 생성, 감사, lint, 폴리시, 수정 루프, 케이스 스터디, 워크숍, 카피, 모션, a11y, 대시보드, 컨덕터 — 완전히 통합.

전체 컬럼별 비교는 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)에 있습니다.

---

## 아키텍처 — 부품들이 어떻게 맞물리는가

```
ux-skill (패키지명: uxskill)
│
├── data/                              두뇌 — 쿼리 가능한 JSON 매니페스트
│   ├── styles.json                    84개 디자인 스타일 + when/skip + tokens
│   ├── palettes.json                  176개 팔레트(라이트/다크, 명도대비 검증)
│   ├── type-pairs.json                70개 display × body × mono 트리플렛
│   ├── components.json                148개 컴포넌트(해부, 상태, 모션)
│   ├── industries.json                184개 산업 규칙 + 청중 시그널
│   ├── chart-types.json               35개 차트 타입(when/skip, 인코딩)
│   ├── tech-stacks.json               25개 스택(Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112개 명명된 UX 법칙(Hick, Fitts, Miller...)
│   ├── motion-presets.json            57개 모션 프리셋(진입, 퇴장, 호버...)
│   ├── anti-patterns.json             145개 regex 규칙(CI 안전 린터 소스)
│   └── brands/*.json                  110개 브랜드 DESIGN 사양 + _index.json
│
├── engine/                            Python — 추론 층
│   ├── recommender/                   5병렬 검색 머지 엔진
│   ├── linter/                        결정론적 반-슬롭 스캐너
│   ├── discovery/                     10 필드 강제 프로토콜
│   ├── generator/                     토큰 + 매니페스트 발행기
│   ├── installer/                     17 IDE용 멀티 인스톨러
│   └── cli/                           `ux` / `uxskill` 진입점
│
├── commands/                          22개 Claude Code 슬래시 명령(.md)
│   ├── ux-init.md                     부트스트랩
│   ├── ux-stats.md                    인벤토리 스냅샷
│   ├── ux-discover.md                 10 필드 인테이크(게이트)
│   ├── ux-recommend.md                기함 — 5병렬 검색
│   ├── ux-lint.md                     결정론적 린터
│   ├── ux-design.md                   프런트엔드 코드 생성
│   ├── ux-component.md                단일 컴포넌트 생성
│   ├── ux-system.md                   전체 디자인 시스템 생성
│   ├── ux-dashboard.md                대시보드 화면 생성
│   ├── ux-motion.md                   모션 처리 + 감사
│   ├── ux-audit.md                    6렌즈 디자인 감사
│   ├── ux-a11y.md                     WCAG 2.1 AA 감사
│   ├── ux-critique.md                 안목 평점(3승, 3패, 1수)
│   ├── ux-copy.md                     마이크로카피 감사 + 재작성
│   ├── ux-fix.md                      소견을 원자 커밋으로 적용
│   ├── ux-polish.md                   폴리시 + AI-슬롭 제거
│   ├── ux-frame.md                    4 필드 프레이밍 블록
│   ├── ux-research.md                 리서치 계획 + 통합
│   ├── ux-workshop.md                 5단계 디자인 사고 워크숍
│   ├── ux-case-study.md               발행 가능한 Wfrah 편집체 케이스 스터디
│   ├── ux-next.md                     워크플로 컨덕터(읽기 전용)
│   └── ux-expert.md                   컨설팅 훅
│
├── agents/                            5개 서브에이전트(.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 브랜드 보이스의 마이크로카피
│   ├── research-synthesizer.md        인터뷰 + 분석 + 경쟁사
│   └── design-system-architect.md     토큰 / 컴포넌트 / 기초
│
├── references/                        데이터의 산문 소스 + 데모 페이지
│   ├── foundations/                   anti-patterns.md, 원칙, 안목
│   ├── laws/                          UX 법칙 장문
│   ├── process/                       discovery-protocol.md(핵심)
│   ├── styles/                        스타일별 산문(anti-slop.md 등)
│   ├── components/                    컴포넌트 장문
│   ├── output/                        출력 루브릭
│   └── conditional/                   스택별 안내
│
├── bin/
│   ├── uxskill.mjs                    npx 래퍼 -> Python 엔진
│   ├── ux-lint.py                     v2 린터(우선)
│   └── ux-lint.sh                     v1 폴백(bash + perl-PCRE)
│
└── .ux/                               (프로젝트마다 생성)
    ├── last-discovery.json            브리프 스냅샷
    ├── last-recommendation.json       선택된 시스템
    ├── last-frame.json                프레이밍 블록
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### 엔진은 실제로 어떻게 작동하는가

1. **입력.** 브리프를 제공합니다 — `/ux-discover`로 대화식(10 필드) 또는 `ux recommend`에 플래그를 넘겨 비대화식.
2. **5병렬 검색.** 엔진이 매니페스트를 가로질러 다섯 개의 조회를 동시에 실행합니다:
   - **산업 → 추천 스타일**(industries.json)
   - **스타일 → 팔레트 + 타입 + 모션 호환성**(styles.json)
   - **톤 × 필수 항목 → 팔레트 필터**(palettes.json)
   - **스택 → 컴포넌트 호환성 + 모션 프리셋**(tech-stacks.json, motion-presets.json)
   - **금지 + 지역 → 가드레일 + 브랜드 본보기 후보**(anti-patterns.json, brands/)
3. **머지.** 결정론적 머저(merger)가 후보의 순위를 매기고 충돌을 해결하며(예: 다크 모드 필수가 팔레트 모드를 강제), 단일 추천 시스템을 발행합니다.
4. **출력.** 선택된 스타일, 팔레트, 타입 페어, 상위 5 모션 프리셋, 상위 12 컴포넌트, 상위 5 브랜드 본보기, 그리고 145개 안티패턴 가드레일 모두 활성을 담은 JSON 문서. 각 선택의 근거 블록까지.
5. **생성.** 다운스트림 명령(`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`)이 추천을 소비하여 서브에이전트를 통해 실제 코드를 생성합니다.
6. **검증.** `/ux-lint`가 생성된 코드를 145개 regex 규칙에 대해 다시 스캔합니다. CI에서 Critical/High에 부딪히면 비영 종료.

**Python이 생각한다. HTML이 보여준다. Markdown이 연결한다.**

---

## 22개의 슬래시 명령 — 상세 레퍼런스

각 명령은 `commands/` 아래에 `.md` 파일로 배포되며 `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process`, `output state file`을 포함합니다. 아래 설명은 압축본입니다; 전체 소스가 정전의 사양입니다.

명령은 다섯 가지 버킷으로 묶입니다: **부트스트랩 & 인벤토리**, **discovery & 추천**, **생성**, **감사 & 검증**, **수정 & 폴리시**, 그리고 **컨덕터**.

### 부트스트랩 & 인벤토리

#### `/ux-init` — 프로젝트 부트스트랩

- **무엇:** 어떤 IDE를 쓰고 있는지(`.claude/`, `.cursor/`, `.windsurf/` 등) 감지하고, 올바른 아티팩트를 설치하고, Python 엔진이 도달 가능한지 검증하고, 통계 스냅샷을 인쇄합니다.
- **사용 시점:** 새 프로젝트에 처음 설치할 때. ux-skill을 쓰는 프로젝트를 clone한 뒤. `pip install --upgrade uxskill` 뒤.
- **건너뛸 시점:** 이미 이 프로젝트에서 실행했고 아무것도 바뀌지 않았다.
- **호출:** `/ux-init`(인자 없음) 또는 CLI에서 `uxskill init`.
- **출력:** IDE별 아티팩트([17 IDE 인스톨러](#17-ide-인스톨러) 참조) + `.ux/` 디렉터리 + stdout 요약.
- **다음:** `/ux-discover`.

#### `/ux-stats` — 데이터 인벤토리 인쇄

- **무엇:** 버전 + 11개 데이터 매니페스트의 항목 수를 인쇄하여 무엇이 설치되어 있는지 검증할 수 있게 합니다.
- **사용 시점:** 설치 후, 업그레이드 후. `/ux-recommend`가 의외의 선택을 반환하고 매니페스트가 불완전한지 의심될 때.
- **건너뛸 시점:** 절대 없음 — 50ms 읽기 전용 명령입니다.
- **호출:** `/ux-stats` 또는 `uxskill stats`.
- **출력:** stdout으로 JSON(위 [설치 검증](#설치-검증) 참조).
- **다음:** 진단 전용; 다운스트림을 먹이지 않습니다.

### discovery & 추천

#### `/ux-discover` — 강제 함수(10 필드 인테이크)

- **무엇:** 생성 명령 이전에 모든 프로젝트가 거치는 의무적인 10 필드 인테이크. 프로젝트 타입, 청중, 주요 목표, 톤, 필수 항목, 금지 항목, 참조 브랜드, 스택, 지역, 성공 지표. **즉흥 금지.** 금지된 문구("modern", "clean")가 사용자에게 구체적이게 만듭니다.
- **사용 시점:** `/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard` 이전. 이전 브리프가 낡았을 때.
- **건너뛸 시점:** 버그를 고치고 있다(`/ux-fix`). 린터만 실행한다(`/ux-lint`). 브리프가 지난 세션과 동일하다.
- **호출:** `/ux-discover`. 플러그인이 묻고, 당신이 답합니다.
- **출력:** `.ux/last-discovery.json`(10 필드 브리프)을 씁니다.
- **다음:** `/ux-recommend` → discovery로 스타일 + 팔레트 + 타입 + 모션 + 컴포넌트 선택. `/ux-design [추가 브리프]` → 추천에 기초한 프런트엔드 코드 생성. `/ux-component <이름>` → discovery 제약에 맞는 단일 컴포넌트 생성.

#### `/ux-recommend` — 기함 5병렬 검색 엔진

- **무엇:** 11개 매니페스트에 걸쳐 Python 엔진의 5병렬 검색을 실행하고 병합된 디자인 시스템 하나를 반환합니다. 산업 → 스타일 → 팔레트 → 타입 → 모션 + 컴포넌트 + 브랜드 본보기 + 가드레일.
- **사용 시점:** 새 프로젝트를 0에서 시작한다. 지친 제품을 피벗한다. `/ux-design`이나 `/ux-component` 전의 사전 점검.
- **건너뛸 시점:** 이미 `/ux-discover`를 실행하고 브리프를 저장했다 — 그 흐름에서 `/ux-recommend`는 자동입니다. 버그 한 개를 고치고 있다(`/ux-fix`를 쓴다). 린트만 필요하다(`/ux-lint`를 쓴다).
- **호출(Claude Code):**
  ```
  /ux-recommend
  ```
  **호출(CLI):**
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
- **출력:** `.ux/last-recommendation.json`을 씁니다 — 선택된 스타일, 선택된 팔레트, 선택된 타입 페어, 상위 5 모션 프리셋, 상위 12 컴포넌트, 상위 5 브랜드 본보기, 145개 안티패턴 가드레일 모두 활성, 그리고 근거.
- **다음:** `/ux-design [브리프]` → 추천 토큰으로 프런트엔드 코드 생성. `/ux-system` → 추천에서 전체 디자인 시스템. `/ux-component <이름>` → 추천 스타일을 쓰는 한 개의 컴포넌트. `/ux-lint` → 생성된 코드를 검증.

### 생성

#### `/ux-design` — 브리프에서 아름답고 반-슬롭인 화면 생성

- **무엇:** discovery 브리프 + 추천에서 완전한 프로덕션급 프런트엔드 아티팩트(랜딩, 마케팅 사이트, 앱 셸)를 생성합니다. 반-슬롭과 arsenal 참조의 창작 지침 아래 `frontend-engineer`를 파견합니다.
- **사용 시점:** "디자인해 줘", "만들어 줘", "랜딩 페이지 생성", "대시보드 만들기", "컴포넌트 만들기" — 자유 형식 시각 산출물 요청 일체.
- **건너뛸 시점:** 빌드가 아닌 리뷰가 필요하다(`/ux-audit` 또는 `/ux-critique`). 컴포넌트 하나만 원한다(`/ux-component`). 백엔드/인프라 작업.
- **호출:** `/ux-design MENA 네오뱅크 핀테크 랜딩 생성, 따뜻한 editorial 톤, 다크 AA, 보라 그라데이션 금지`.
- **출력:** 생성된 코드(HTML / Blade / JSX / Vue / Astro), 그리고 `.ux/last-design.json`.
- **다음:** `/ux-lint` → 가드레일 검증. `/ux-polish` → 폴리시. `/ux-a11y` → 접근성 감사. `/ux-copy` → 마이크로카피 감사. `/ux-fix` → 소견을 원자 커밋으로.

#### `/ux-component` — 단일 컴포넌트 생성

- **무엇:** 사양에서 단일 프로덕션급 컴포넌트(버튼, 모달, 내비바, 사이드바, 카드, 테이블, 폼, 차트)를 생산합니다. 4가지 상호작용 상태 완비, 접근 가능, 브랜드에 맞춤. 먼저 `.ux/last-recommendation.json`에서 컴포넌트를 찾고, 매니페스트 직접 쿼리로 폴백합니다.
- **사용 시점:** 단일 요소 요청 일체 — "버튼 만들기", "가격 카드 만들기", "모달 만들기", "내비바 추가", "사이드바 디자인", "데이터 테이블 필요", "폼 만들기", "차트 컴포넌트 만들기".
- **건너뛸 시점:** 전체 페이지나 다중 섹션 화면(`/ux-design`). 백엔드/인프라.
- **호출:** `/ux-component pricing-card-trio --brief="핀테크, 다크, 모노스페이스 숫자"`.
- **출력:** 생성된 컴포넌트 코드, 그리고 `.ux/last-component.json`.
- **다음:** `/ux-lint` → 검증. `/ux-polish` → 다듬기.

#### `/ux-system` — 완전한 스타터 디자인 시스템 생성

- **무엇:** 디자인 시스템이 없는 프로젝트에 완전한 스타터 시스템을 제안합니다 — 토큰(색, 타입, 공간, 모션, 모서리, 그림자), 기초 문서, 컴포넌트 계약, 다크 모드 페어링, 테마 스위처. `design-system-architect`를 파견합니다.
- **사용 시점:** "디자인 시스템이 없다", "우리에게 시스템을 만들어 줘", "토큰을 제안해 줘", "테마는 어때야 하나", "DS를 셋업해 줘".
- **건너뛸 시점:** 프로젝트에 이미 디자인 시스템이 있다 — 그러면 기존 시스템에 `/ux-component`를 사용. 백엔드/인프라.
- **호출:** `/ux-system`(파일에 없으면 먼저 discovery).
- **출력:** `tokens.json`, `foundations.md`, `components/*.md` 계약, 선택적 Tailwind / vanilla / SCSS 출력. 연결 컨텍스트를 위해 `.ux/last-system.json`을 씁니다.
- **다음:** `/ux-component` → 새 시스템에 대해 빌드. `/ux-design` → 새 토큰으로 화면 생성.

#### `/ux-dashboard` — 특화 대시보드 생성

- **무엇:** 데이터 밀도 규율의 대시보드 — 벤토 레이아웃, 표 모노스페이스 숫자, 스파크라인 패턴, 카드 과용 방지, 시맨틱 상태 색, 절제된 모션. 차트를 붙인 마케팅 페이지가 아닙니다.
- **사용 시점:** "대시보드 만들기", "관리자 패널 디자인", "지표 페이지", "오퍼레이터 콘솔", "분석 뷰", "KPI 보드", "모니터링 화면".
- **건너뛸 시점:** 통계가 있는 마케팅 랜딩(`/ux-design`). 위젯 하나만(`/ux-component`). 백엔드/인프라.
- **호출:** `/ux-dashboard`.
- **출력:** 생성된 대시보드 코드 + `.ux/last-dashboard.json`.
- **다음:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — 모션 처리

- **무엇:** 화면의 모션 층을 생성합니다 — 지속 시간, 이징, 안무, reduced-motion 폴백, 성능 규율. 기존 모션을 5차원(타이밍, 이징, 의미, reduced-motion, 성능)에 대해 감사하기도 합니다.
- **사용 시점:** "모션 확인", "애니메이션 괜찮나", "모션 고치기", "애니메이션 리뷰", "모션 감사", "모션 성능 패스".
- **건너뛸 시점:** 화면에 모션이 없다(`/ux-audit` 또는 `/ux-polish`). 백엔드/인프라.
- **호출:** `/ux-motion path/to/component.tsx`(감사 모드) 또는 `/ux-motion --generate hero-entry`(생성).
- **출력:** 업데이트된 코드(생성 모드) 또는 `.ux/last-motion.json` 보고서(감사 모드).
- **다음:** `/ux-fix` → 모션 소견 적용. `/ux-polish` → 다듬기.

### 감사 & 검증

#### `/ux-lint` — 결정론적 regex 기반 린터(LLM 없음, CI 안전)

- **무엇:** 코드에 대해 145개 regex 규칙을 실행합니다. LLM 호출 없음. CI에서 Critical/High에 부딪히면 비영 종료. 소스: `data/anti-patterns.json`. 규칙은 A11y(23), 콘텐츠(15), 레이아웃(13), 타이포그래피(10), 색(9), 품질(9), 시각(9), 모션(8), 성능(4)을 커버합니다.
- **사용 시점:** 사전 커밋 훅. CI 게이트. `/ux-audit` 비용을 치르기 전에 대형 코드베이스에 대한 빠른 첫 패스. `/ux-design`이나 `/ux-component` 후 생성 검증.
- **건너뛸 시점:** 수정 루프가 필요하다(린터는 보고만 합니다, 편집하지 않음 — `/ux-polish --fix`나 `/ux-fix`로 연결). 안목 판단이 필요하다(`/ux-critique`).
- **호출(슬래시):** `/ux-lint src/`.
- **호출(CLI):** `uxskill lint .` 또는 `python3 bin/ux-lint.py .` 또는 `bash bin/ux-lint.sh --ci --fail-on high`.
- **호출(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **출력:** 표준 출력의 소견(위치, 규칙 id, 심각도, 증거). 깨끗하면 종료 코드 0, `--fail-on high` 설정 시 Critical/High이면 비영.
- **다음:** `/ux-polish --fix` → 같은 패턴의 LLM 구동 대응물. `/ux-fix` → 소견을 심각도 정렬로 커밋 적용. `/ux-audit` → 완전한 6렌즈 추론 패스. `/ux-next` → 컨덕터에 결정 맡기기.

#### `/ux-audit` — 6렌즈 디자인 감사

- **무엇:** 여섯 렌즈(명료성, 위계, 접근성, 보이스, 모션, 안목)에 대한 구조적, 입장 있는 리뷰로 심각도 태그 소견을 산출합니다. Polaris 스타일 보고서. 먼저 `.ux/last-frame.json`을 읽습니다 — 청중과 결과가 모든 소견의 심각도를 닻으로 잡습니다.
- **사용 시점:** 화면이 존재하고 변호 가능한 비평이 필요하다. "감사", "ux 리뷰", "이거 괜찮나", "뭐가 망가졌나", "산산조각 내 봐".
- **건너뛸 시점:** 화면이 아직 없다(`/ux-design`). 사용자가 한 렌즈만 원한다(타깃 명령 사용: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). 사용자가 안목 의견을 원한다(`/ux-critique`). 백엔드/인프라.
- **호출:** `/ux-audit https://example.com/pricing` 또는 `/ux-audit src/components/Pricing.tsx`.
- **출력:** `.ux/last-audit.json`을 씁니다 — `findings` 배열 `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **다음:** `/ux-fix` → 소견 적용. `/ux-polish` → 폴리시. `/ux-design` → 구조적 재설계가 필요하다면.

#### `/ux-a11y` — WCAG 2.1 AA 감사 + 기본 예의 체크

- **무엇:** 구조화된 WCAG 2.1 AA 감사에, 자동 도구는 통과하지만 실제 사용자에게 해로운 기본 예의 체크(포커스 가시성, 에러 구체성, 모션 환경설정, 키보드 트랩, 색 의존)를 더합니다.
- **사용 시점:** 출시 전 접근성 게이트. 재설계 후. "접근성 체크", "WCAG 감사", "접근 가능한가", "a11y 리뷰", "스크린 리더 테스트", "키보드 내비 체크".
- **건너뛸 시점:** 사용자 대상이 아니다. 백엔드/인프라. 작업 중 스케치.
- **호출:** `/ux-a11y https://example.com`(라이브 URL 권장 — 자동 도구와 키보드 테스트는 라이브에서만 작동).
- **출력:** `.ux/last-a11y.json`을 씁니다 — `findings` 배열 `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, `beyond_wcag` 배열, `severity_counts`.
- **다음:** `/ux-fix` → 소견을 커밋으로. `/ux-copy` → 카피 패스의 일부로 alt 텍스트와 폼 에러 연결을 고치기.

#### `/ux-critique` — 안목 평점(3승, 3패, 1수)

- **무엇:** 디자이너의 의견 — 구조화된 감사가 아니고, 심각도 점수도 아니며, 무엇이 작동하고 무엇이 작동하지 않는지를 짚고, 가장 많이 바꿀 그 한 수를 명명하는 짧고 입장 있는 견해.
- **사용 시점:** "어떻게 생각해", "이거 괜찮아", "비평해 줘", "솔직하게", "분위기 맞나", "이게 우리답나", "출시할까".
- **건너뛸 시점:** 사용자가 명시적으로 구조화된 감사를 원한다(`/ux-audit`). 백엔드/인프라.
- **호출:** `/ux-critique https://example.com`.
- **출력:** `.ux/last-critique.json`을 씁니다 — 3승, 3패, 1수, 그리고 산문.
- **다음:** 견해가 재설계를 권하면 `/ux-design`. 다듬기를 권하면 `/ux-polish`.

#### `/ux-copy` — 마이크로카피 감사 + 재작성

- **무엇:** 모든 보이는 문자열을 보이스 루브릭에 대해 평가하고 before/after 재작성을 생산합니다. 잡아냅니다: "form contains errors"(일반), "John Doe"(자리표시), AI 쾌활 축하 카피, 일반 CTA, 죽은 빈 상태, 쓸모없는 에러.
- **사용 시점:** 구조는 맞는데 말이 약하다. "카피 리뷰", "마이크로카피 수정", "에러 메시지 나쁘다", "다시 써", "문자열 다듬기", "버튼이 일반적", "이 빈 상태 죽었다".
- **건너뛸 시점:** 레이아웃 문제(`/ux-audit` 또는 `/ux-polish`). 접근성 주도의 카피 문제 alt 텍스트 같은 것(`/ux-a11y`). 백엔드/인프라.
- **호출:** `/ux-copy src/views/checkout.blade.php`.
- **출력:** `.ux/last-copy.json`을 씁니다 — `strings` 배열 `{location, severity, before, after, notes}`, 루브릭, 번역 필요 로케일.
- **다음:** `/ux-fix` → 재작성 적용. `/ux-a11y` → 카피 수정 후 재확인.

### 수정 & 폴리시

#### `/ux-fix` — 소견을 원자 커밋으로 적용

- **무엇:** `.ux/`의 최신 보고서(audit, copy, a11y, motion, polish)를 읽고, 워킹 트리를 검증하고, 적절한 서브에이전트를 통해 소견을 원자 커밋으로 적용합니다. 원래 명령을 다시 실행해 재검증합니다.
- **사용 시점:** 감사 클래스 명령을 실행하고 소견을 리뷰한 뒤. "소견 수정", "수정 적용", "수정 루프 실행", "화면 패치", "변경 만들기", "가서 고쳐".
- **건너뛸 시점:** `.ux/`에 이전 보고서가 없다. 워킹 트리가 더럽고 사용자가 stash/commit에 동의하지 않았다. 수정이 기계적 적용이 아닌 디자인 판단을 필요로 한다(재설계를 위해 `/ux-design` 사용).
- **호출:** `/ux-fix`(어떤 보고서를 수정할지 자동 감지) 또는 `/ux-fix --from=last-a11y.json`.
- **출력:** 소견당 원자 커밋. 원래 명령을 다시 실행하고 `.ux/last-*.json`을 업데이트. 요약 인쇄.
- **다음:** `/ux-next` → 컨덕터가 다음 수를 선택.

#### `/ux-polish` — 폴리시 + AI-슬롭 제거

- **무엇:** 간격 리듬, 위계 날카로움, AI-슬롭 탐지, 토큰 일관성. `/ux-lint`의 LLM 구동 대응물 — 안목 판단을 당신을 대신해 행사.
- **사용 시점:** 구조는 맞는데 실행이 헐겁다. "폴리시", "다듬기", "AI-슬롭 제거", "프리미엄으로", "AI 같지 않게", "간격이 어색", "이거 일반적", "안목이 더 필요".
- **건너뛸 시점:** 화면이 핵심 기능을 잃었다(그것부터 고치기). 폴리시가 아닌 재설계가 필요(`/ux-design`). 카피 문제(`/ux-copy`). 모션 문제(`/ux-motion`). a11y 문제(`/ux-a11y`).
- **호출:** `/ux-polish src/components/Hero.tsx`.
- **출력:** 업데이트된 코드 + 변경 사항을 기술하는 `.ux/last-polish.json`.
- **다음:** `/ux-lint` → 폴리시가 유지되는지 검증. `/ux-a11y` → 접근성 재확인.

### discovery & 내러티브

#### `/ux-frame` — 4 필드 프레이밍 블록

- **무엇:** 누구를 위한 것인지, 결과, 가설, 성공 신호를 구조화된 프레이밍 블록에 포착합니다. 디자인 작업은 없습니다 — 모호한 요청을 작동하는 브리프로 바꾸는 4 필드 인테이크. `/ux-discover`보다 가볍다(4 필드 vs 10).
- **사용 시점:** 모든 프로젝트, 스프린트, 단발 약속의 시작. 대화가 표류한 중도에. "프레이밍", "브리프가 뭐냐", "프로젝트 셋업", "프레이밍".
- **건너뛸 시점:** 이미 프레이밍됨(`.ux/last-frame.json` 확인). 프레이밍 영향이 없는 단발 컴포넌트 빌드. 백엔드/인프라.
- **호출:** `/ux-frame "MENA Bashiti 파일럿용 로열티 월렛"`.
- **출력:** `.ux/last-frame.json`을 씁니다 — `{audience, outcome, hypothesis, success_signal}`.
- **다음:** `/ux-discover` → 프레임을 10 필드 브리프로 확장. `/ux-design` → 프레임을 닻으로 생성.

#### `/ux-research` — 리서치 계획 + 통합

- **무엇:** 계획 모드: 인터뷰 스크립트, 설문, 모집 스크리너 작성. 통합 모드(`--synthesize`): 인터뷰, 분석, 경쟁사 사이트, A/B 결과, 지원 티켓을 추천으로 소화. `research-synthesizer`를 파견.
- **사용 시점:** "리서치 연구 계획", "인터뷰 질문 필요", "설문 디자인", "사용자 어떻게 모집", "사용자 테스트 계획", "다이어리 연구", "선호 테스트", "fake door", "smoke test", "내 인터뷰 노트 통합".
- **건너뛸 시점:** 답이 이미 높은 자신감으로 알려졌다. 저위험 가역 결정. 백엔드/인프라.
- **호출:** `/ux-research --plan "MENA 로열티 월렛 채택"` 또는 `/ux-research --synthesize interviews/*.md`.
- **출력:** `.ux/last-research.json`을 씁니다 — 리서치 계획 또는 통합된 테마 + 증거 + 추천.
- **다음:** `/ux-frame` → 발견을 프레임에 통합. `/ux-design` → 발견에서 생성. `/ux-workshop` → 리서치를 입력으로 워크숍 실행.

#### `/ux-workshop` — 5단계 디자인 사고 워크숍

- **무엇:** discovery / 디자인 사고 워크숍을 끝에서 끝까지 진행. 다섯 개의 순차 단계(탐색 → 히트맵 → 이해관계자 지도 → 솔루션 스케치 → 게임 플랜). 시간 박싱. 단계별 구체적 산출물. "흥미로운 발견"이 아닌 결정으로 끝납니다.
- **사용 시점:** 진짜 질문, 진짜 참가자, 진짜 시간 예산. "워크숍 진행", "discovery 진행", "디자인 사고 세션", "이해관계자가 한 시간 있다, 뭐 할까", "프로젝트 킥오프".
- **건너뛸 시점:** 브리프가 이미 명확하고 범위 잡혔다. 단독 브레인스토밍(`/ux-design` 또는 `/ux-frame`). 팀이 실행 중, discovery에 없다.
- **호출:** `/ux-workshop "로열티 월렛 피벗" --participants="PM 2명, 디자이너 1명, 엔지 리드 1명, 고객 담당 1명" --minutes=90`.
- **출력:** `.ux/last-workshop.json`을 씁니다 — 게임 플랜 + 단계별 산출물.
- **다음:** `/ux-design` → 게임 플랜 실행. `/ux-research` → 워크숍이 드러낸 간극 채우기. `/ux-case-study` → 여정을 발행.

#### `/ux-case-study` — 발행 가능한 케이스 스터디(Wfrah 편집체)

- **무엇:** 프로젝트 케이스 스터디를 순수 모노크롬 편집체로 생성합니다 — Wfrah 타이포, 헤어라인 구분선, (A)–(G) 번호 섹션 코드, 양언어 안전 레이아웃. 문서이지 마케팅 브로슈어가 아닙니다. `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`에서 읽습니다.
- **사용 시점:** 출시 후. 별개 이정표 후. "케이스 스터디 작성", "이 프로젝트 케이스 스터디로", "마무리 문서", "이 작업 발행", "포트폴리오 작품".
- **건너뛸 시점:** 프로젝트에 (A)–(G)를 채울 데이터가 없다. 사용자가 마케팅 랜딩을 원한다, 케이스 스터디가 아니다(`/ux-design`).
- **호출:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **출력:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **다음:** 종단 명령 — 보통 프로젝트의 끝.

### 컨덕터

#### `/ux-next` — 워크플로 컨덕터(읽기 전용)

- **무엇:** 모든 `.ux/last-*.json`을 읽고 가장 레버리지가 큰 다음 명령을 지명합니다. 컨덕터, 빌더가 아닙니다. 읽기 전용.
- **사용 시점:** 명령 사이. "다음에 뭐 할까", "다음 수는 뭐", "나 대신 결정", "여기서 어디로".
- **건너뛸 시점:** `.ux/`에 이전 보고서가 없다. 구체적인 다음 명령이 이미 있다.
- **호출:** `/ux-next`(인자 없음) 또는 `/ux-next --focus=a11y`.
- **출력:** stdout — 권장 다음 명령 + 근거.
- **다음:** 선택된 어떤 것이든.

#### `/ux-expert` — 컨설팅 훅

- **무엇:** 사용자가 실제 UX 전문가를 요청할 때 플러그인 작자의 연락처를 표면화합니다. 짧고, 직접적이며, 마케팅 없음.
- **사용 시점:** "누가 만들었나", "UX 전문가가 필요", "컨설팅 하나", "누구 고용할 수 있나", "이 플러그인 뒤에 사람 있나".
- **건너뛸 시점:** 사용자가 플러그인 기능을 묻는다, 컨설팅이 아니다.
- **호출:** `/ux-expert`.
- **출력:** LinkedIn / 이메일 / 저장소가 있는 짧은 연락 카드.

### 명령 체이닝 그래프

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4 필드 프레이밍 블록
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10 필드 인테이크(강제 게이트)
                  └────────────┬─────────┘
                               │ .ux/last-discovery.json 쓰기
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5병렬 검색 -> 병합 시스템
                  └────────────┬─────────┘
                               │ .ux/last-recommendation.json 쓰기
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ .ux/last-<surface>.json 쓰기
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ .ux/last-<lens>.json 쓰기
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  소견을 커밋으로 적용
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  발행 가능한 아티팩트
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  컨덕터 — 읽기 전용
                  │  /ux-expert          │  컨설팅 훅
                  └──────────────────────┘
```

---

## 5개의 서브에이전트

서브에이전트는 명령이 파견하는 역할 특화 생성기입니다. 단독으로 실행되지 않습니다 — `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research` 등에 의해 호출됩니다. 각 에이전트는 명확한 소유 경계를 가집니다: 브리프를 결정하지 않으며, 브리프에 대해 실행합니다.

### `frontend-engineer`

- **소유:** 프로덕션급 프런트엔드 코드(React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro)에 반-AI-슬롭 규율을 적용.
- **파견자:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **입력:** 브리프 + 창작 지침 + 토큰(`.ux/last-recommendation.json`에서).
- **출력:** 일반 AI 출력과 구별 가능한 작동 코드. 보라 그라데이션 없음, 가운데 정렬 히어로 없음, 같은 크기 카드 셋 없음, 디스플레이 크기 Inter 없음, "John Doe" 없음, 이모지 없음, 300ms 기본 없음.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **소유:** 프로덕션 프런트엔드 코드의 모션 — Framer Motion, GSAP, CSS 애니메이션. 지속 시간, 이징, 안무, reduced-motion 폴백, 성능 규율.
- **파견자:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **입력:** 모션 브리프 + 토큰 + `data/motion-presets.json`의 57개 모션 프리셋.
- **출력:** 그 자리를 차지할 자격이 있는 모션. 항상 `prefers-reduced-motion` 폴백으로 감쌈. 항상 Core Web Vitals에 대해 테스트.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **소유:** 배포되는 문자열 — 에러 메시지, 빈 상태, CTA, 로딩 상태, 성공 메시지, 토스트, 헬퍼 텍스트, 폼 레이블, 버튼 텍스트.
- **파견자:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **입력:** 보이스 프로필(이름 지정 또는 붙여넣기) + 화면의 문자열.
- **출력:** 화면의 모든 상태에 걸쳐 일관되게 적용되어 제품이 열 개가 아닌 하나처럼 들리게 하는 프로덕션 마이크로카피. 금지: "form contains errors", "John Doe", AI 쾌활 축하 카피, 일반 CTA, 죽은 빈 상태.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **소유:** 리서치 입력(인터뷰, 분석, 경쟁 사이트, A/B 결과, 지원 티켓)을 실행 가능한 디자인 추천으로 소화.
- **파견자:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **입력:** 원천 리서치 — 녹취, 내보내기, 경쟁 URL, 지원 클러스터.
- **출력:** 테마, 증거, 추천. 답을 디자인하지 않음 — 디자이너가 디자인할 기질을 줍니다.
- **도구:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **소유:** 완전한 디자인 시스템 — 토큰(색, 타입, 공간, 모션, 모서리, 그림자), 기초 문서, 컴포넌트 계약, 다크 모드 페어링, 테마 층.
- **파견자:** `/ux-system`, 시스템이 없을 때 `/ux-component`에서.
- **입력:** 브랜드 브리프 + `.ux/last-recommendation.json`(스타일 + 팔레트 + 타입 페어 + 모션 프리셋).
- **출력:** 다운스트림 에이전트가 기본을 재결정하지 않고도 빌드할 수 있는 일관되고 의견 있는 프로덕션 준비 시스템. 토큰 JSON, 기초 MD, 컴포넌트 계약, 다크 모드 매핑.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### 서브에이전트 파견 프로토콜

명령이 서브에이전트를 파견할 때 전달합니다:

1. 브리프 / 추천(`.ux/`에서 로드).
2. 관련 매니페스트 슬라이스(예: `frontend-engineer`는 선택된 스타일 + 팔레트 + 컴포넌트를 받음; `motion-engineer`는 선택된 모션 프리셋을 받음).
3. 145개 안티패턴 가드레일(항상 활성).
4. 성공 기준(아티팩트가 무엇을 해야 하나).

서브에이전트가 반환합니다:

1. 아티팩트(코드, 문서, 시스템).
2. 근거 블록(왜 이 선택인가).
3. 가드레일에 대한 자체 확인(어떤 규칙을 검증했나).

호출 명령은 완료를 선언하기 전에 자동으로 `/ux-lint`를 실행합니다.

---

## 11개의 데이터 매니페스트

데이터 층이 두뇌입니다. 모든 명령이 거기서 읽고, 엔진이 그 사이를 머지하며, 린터가 그것에 대해 스캔합니다. 모든 파일은 `data/` 아래 있고, 항목을 `{_meta, entries}`로 감싸 스키마 버저닝을 합니다.

### `styles.json` — 84개 디자인 스타일

| 필드 | 설명 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave 등 |
| `sample entry` | `swiss-international` — "그리드는 법. 타입이 무거운 일을 한다. 장식은 실패다." |

사용: `/ux-recommend`, `/ux-system`, `/ux-design`. 스키마: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176개 컬러 팔레트

| 필드 | 설명 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode`(라이트/다크), `tone`, `colors`(canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark 등 |
| `sample entry` | `claude-warm-editorial` — 라이트, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

사용: `/ux-recommend`, `/ux-system`. AA / AAA에 대해 명도대비 검증. 스키마: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70개 타입 페어링

| 필드 | 설명 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display`(family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

모든 패밀리에 라이선스 + 소스 URL이 있습니다. `/ux-recommend`, `/ux-system`에서 사용.

### `components.json` — 148개 컴포넌트

| 필드 | 설명 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Mega Navigation, Product Grid — 6부분 해부, 4 상태 |

이게 우리의 가장 큰 해자입니다. 다른 어떤 Claude UX 플러그인도 구조화된 컴포넌트 매니페스트를 출시하지 않습니다.

### `industries.json` — 184개 산업 규칙

| 필드 | 설명 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific 등 |
| `sample entry` | `fintech-neobank` — 높은 신뢰, 규제 공시, 잔액/거래 주력 UI, 일상 사용을 위한 모바일 우선 |

`/ux-recommend`가 첫 병렬 검색 축으로 사용.

### `chart-types.json` — 35개 차트 타입

| 필드 | 설명 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical` — 4–15개의 이산 카테고리 비교. x축 위치가 카테고리에, 높이가 값에 매핑. |

`/ux-dashboard`, `/ux-component`(차트 인스턴스)에서 사용.

### `tech-stacks.json` — 25개 스택

| 필드 | 설명 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15(App Router), TS/JS, SSR, RSC, Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css와 호환 |

다른 스택은 Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025 등.

### `ux-guidelines.json` — 112개 명명된 UX 법칙

| 필드 | 설명 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State 등 |
| `sample entry` | `hicks-law` — 의사결정 시간은 제시된 선택지의 수에 로그적으로 비례한다 |

`/ux-audit`(6렌즈 채점)과 `/ux-critique`(안목 닻)에서 사용.

### `motion-presets.json` — 57개 모션 프리셋

| 필드 | 설명 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens`(duration_ms, easing, transform_from/to, opacity_from/to), `stacks`(framer_motion, gsap, css), `accessibility`(reduced-motion 폴백), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

모든 프리셋에 reduced-motion 변형이 있습니다. Framer Motion, GSAP, 순수 CSS에 대한 스택 준비 코드.

### `anti-patterns.json` — 145개 regex 규칙

| 필드 | 설명 |
|---|---|
| `entries` | 100 |
| `keys per entry` | `id`, `name`, `severity`(critical/high/medium/low), `category`, `detection`(type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y(23), Content(15), Layout(13), Typography(10), Color(9), Quality(9), Visual(9), Motion(8), Performance(4) |

전체 규칙 목록은 [145개의 반 AI-슬롭 규칙](#145개의-반-ai-슬롭-규칙--린터)에 있습니다.

### `brands/*.json` — 160개 브랜드 사양

| 필드 | 설명 |
|---|---|
| `entries` | 110(전체 목록을 보여주는 `_index.json` 추가) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens`(color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools(36), Consumer / Lifestyle / Retail(19), Fintech / Crypto(14), Editorial / Media(13), AI / ML Platform(12), Productivity / Collaboration(8), Automotive(8) |

전체 목록은 [160개의 브랜드 DESIGN.md 사양](#160개의-브랜드-designmd-사양--카테고리별)에 있습니다.

---

## 145개의 반 AI-슬롭 규칙 — 린터

ux-skill은 결정론적 regex 기반 린터를 출시합니다. **LLM 없음.** **API 없음.** **네트워크 없음.** 전형적인 Next.js 앱에서 CI에서 ~200ms로 실행됩니다. `--fail-on high` 설정 시 Critical / High에 부딪히면 비영 종료.

규칙은 `data/anti-patterns.json`(v2 우선)에서 가져오며, `references/foundations/anti-patterns.md`(v1 bash) 폴백이 있습니다. 두 개의 바이너리를 출시합니다: `bin/ux-lint.py`(Python, 빠르고 확장 가능)와 `bin/ux-lint.sh`(Bash + perl-PCRE, Python 없는 환경용).

### 카테고리별 규칙

#### 타이포그래피(3개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| high | `inter-as-display` | Inter를 디스플레이 폰트로 사용 |
| medium | `hero-text-arbitrary-90px` | 임의의 히어로 폰트 크기 |
| low | `font-system-only` | 선택된 타입페이스 없는 시스템 폰트 스택만 |

#### 색(6개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| high | `purple-to-blue-gradient` | 기본 보라-파랑 AI 그라데이션 |
| high | `dark-text-on-dark-card` | 카드 위 낮은 명도대비 텍스트 |
| medium | `gradient-text-rainbow` | 다중 스톱 그라데이션 텍스트 |
| medium | `card-glow-purple-shadow` | 카드 위 보라 글로우 그림자 |
| medium | `gradient-mesh-purple-pink` | 히어로 보라-분홍 메시 그라데이션 |
| low | `tailwind-color-named-vague` | 시맨틱 토큰 없는 명명된 Tailwind 색 |

#### 레이아웃(5개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| high | `three-equal-card-grid` | 한 줄에 같은 크기 카드 셋 |
| medium | `centered-everything-hero` | 가운데 정렬 히어로 구성 |
| medium | `avatar-stack-overlapping` | 일반적인 겹친 아바타 스택 |
| low | `pill-rounded-full-everywhere` | 모든 것에 적용된 `rounded-full` |
| low | `nav-equal-hamburger-desktop` | 데스크톱의 햄버거 메뉴 |

#### 콘텐츠(5개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| high | `lorem-ipsum-leak` | 배포 코드의 Lorem ipsum |
| high | `emoji-in-ui` | UI 요소로 사용된 이모지 |
| high | `icon-emoji-stamp` | 아이콘 스탬프로 사용된 이모지 |
| high | `testimonial-fake-five-stars` | 하드코딩된 별 다섯 추천사 |
| medium | `fake-name-john-doe` | 일반 자리표시 이름 |

#### 모션(3개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | CTA의 튀는 화살표 |
| low | `timing-300ms-default` | 기본 300ms 트랜지션 타이밍 |
| low | `cubic-bezier-material-only` | 어디서나 Material 기본 이징 |

#### A11y(6개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| high | `inline-svg-no-aria` | aria-label이나 aria-hidden 없는 SVG |
| high | `img-no-alt` | alt 속성 누락된 이미지 |
| high | `link-onclick-no-href` | onClick은 있지만 href 없는 앵커 |
| medium | `button-no-type` | type 속성 누락된 버튼 |
| medium | `heading-skip-h1-h3` | 건너뛴 헤딩 레벨 |
| medium | `infinite-scroll-no-pagination` | 키보드 폴백 없는 무한 스크롤 |

#### 품질(6개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| high | `console-log-leak` | 컴포넌트 코드에 `console.log` |
| medium | `inline-style-attribute` | 인라인 style 속성 |
| medium | `any-type-leak` | TypeScript `any` 타입 |
| medium | `arbitrary-z-index-9999` | 게으른 z-index 값 |
| low | `shadcn-default-everywhere` | 변경 없는 shadcn 기본 토큰 블록 |
| low | `todo-fixme-comment` | 배포 코드에 TODO 또는 FIXME |

#### 시각(1개 규칙)

| 심각도 | 규칙 ID | 이름 |
|---|---|---|
| low | `blur-bg-only-decoration` | 글래스 표면 없는 backdrop blur |

### 린터 사용법

**일회성 스캔:**

```bash
uxskill lint .
# 또는
python3 bin/ux-lint.py src/
# 또는
bash bin/ux-lint.sh src/
```

**CI 게이트(GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**사전 커밋 훅:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**출력(예시):**

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

## 160개의 브랜드 DESIGN.md 사양 — 카테고리별

실제 브랜드. 실제 디자인 언어. 실제 DESIGN.md 사양 — 일반 팔레트가 아닙니다. 플러그인에게 "Stripe 스타일로 랜딩 만들어"라고 하면 실제 브랜드 어휘를 읽습니다: 보이스 루브릭, 색 토큰, 모션 규약, 시그니처 무브, 안티 무브.

각 브랜드는 구조화된 JSON(`data/brands/<slug>.json`)과 산문 참조(`references/brands/<slug>.md`)로 출시됩니다.

### Developer Tools(36)

ClickHouse, Composio, Cursor, Datadog, dbt Labs, Expo, Fivetran, Fly.io, Framer, HashiCorp, Honeycomb, IBM, Lovable, Mintlify, Modal, MongoDB, Neon, Ollama, OpenCode, PostHog, Railway, Raycast, Render, Replicate, Resend, Retool, Sanity, Sentry, Slack, Snowflake, Sourcegraph, Supabase, Superhuman, Vercel, Warp, Webflow

### Consumer / Lifestyle / Retail(19)

Aesop, Airbnb, Allbirds, Apple, Apple Music, Glossier, HP, Hims & Hers, Instagram, Meta, Nike, Patagonia, Pinterest, PlayStation, Shopify, Spotify, Starbucks, TikTok, Uber

### Fintech / Crypto(14)

Binance, Brex, Coinbase, Kraken, Mastercard, Mercury, Monzo, N26, Plaid, Ramp, Revolut, Robinhood, Stripe, Wise

### Editorial / Media(13)

Bloomberg, Clay, Dezeen, NVIDIA, Pitchfork, Substack, The Atlantic, The Economist, The New York Times, The Verge, The Wall Street Journal, Vodafone, Wired

### AI / ML Platform(12)

Anthropic, Claude, Cohere, ElevenLabs, MiniMax, Mistral AI, OpenAI, Perplexity, Runway, Together AI, VoltAgent, xAI

### Productivity / Collaboration(8)

Airtable, Cal.com, Figma, Intercom, Linear, Miro, Notion, Zapier

### Automotive(8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### 왜 이것이 중요한가

다른 8개의 인기 Claude UX 플러그인은 "모던 미니멀"이나 "클린 대시보드"를 생성합니다 — 같은 기본 미학의 변형. ux-skill은 **Linear의 명료성**, **Stripe의 진지함**, **Apple의 절제**, **Tesla의 모놀리스 감**, **Notion의 친근함**, **Cursor의 그라데이션 규율**, **Raycast의 헤어라인 밀도**, **Claude의 따뜻한 editorial**을 요구할 수 있게 합니다 — 엔진이 브랜드 사양에서 올바른 토큰, 보이스, 모션 규약, 시그니처 무브를 꺼냅니다.

---

## MCP 서버 — 비대칭 한 수

ux-skill은 **Model Context Protocol 서버**를 출시합니다. `ux-mcp`를 실행하면 엔진이 장기 실행 stdio 프로세스가 되어, MCP 호환 호스트 누구나 — Claude Desktop, Cursor, Windsurf, 일반 에이전트 — 호출할 수 있습니다. 열네 개의 도구: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. 슬래시 명령이 사용하는 것과 같은 Python 핸들러, 같은 데이터 매니페스트, 같은 결정론적 추천기.

**왜 이것이 비대칭 한 수인가:** 상위 여덟의 Claude UX 스킬(ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) 중 어느 것도 MCP 서버를 출시하지 않습니다. 그들은 Claude Code의 플러그인 런타임에 갇혀 있습니다. ux-skill은 MCP를 말하는 어떤 호스트에서도 도달 가능합니다, Claude Code 플러그인을 들어본 적 없는 에이전트도.

```bash
pip install 'uxskill[mcp]'             # mcp는 옵트인 extra
ux-mcp                                  # stdio JSON-RPC 서버 시작
```

클라이언트를 `ux-mcp` 바이너리에 가리키세요. 완전한 도구 문서, JSON 예시, Claude Desktop, Cursor, Windsurf용 클라이언트별 설정은 [docs/mcp.html](docs/mcp.html)과 `commands/ux-mcp.md`에 있습니다.

---

## 17 IDE 인스톨러

`uxskill init`(Claude Code 내부에서는 `/ux-init`)이 어떤 IDE를 쓰고 있는지 자동 감지하고 올바른 아티팩트를 씁니다. 같은 Python 엔진. 같은 추천. IDE별로 다른 접착제.

| IDE / 도구 | 감지 시그널 | 설치된 아티팩트 |
|---|---|---|
| Claude Code | `.claude/` 또는 `CLAUDE.md` | `.claude-plugin/plugin.json`의 플러그인 매니페스트 + 22개 명령 모두 + 5개 서브에이전트 모두 |
| Cursor | `.cursor/` 또는 `.cursorrules` | 엔진을 가리키는 `.cursorrules` 프롬프트 헤더 |
| Windsurf | `.windsurf/` 또는 `.windsurfrules` | 같은 프롬프트 헤더의 `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` 또는 `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` 패치 |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` 또는 `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

모든 IDE에서 같은 `uxskill recommend` / `uxskill lint` / `uxskill stats` CLI 명령이 터미널에서 작동합니다. Python 엔진이 진실의 원천; IDE 아티팩트는 그것으로 라우팅하는 얇은 프롬프트 헤더일 뿐입니다.

---

## 사용 사례 — 구체적인 시나리오

여덟 개의 실제 시나리오. 당신의 상황에 가장 가까운 것을 골라 호출을 조정하세요.

### 1. Cursor에서 핀테크 대시보드 구축

Cursor에서 MENA 네오뱅크 대시보드 작업 중입니다. 플러그인을 설치하고 discovery, recommendation을 실행한 다음 대시보드 생성을 합니다.

```bash
pip install uxskill
uxskill init                                # Cursor를 감지, .cursorrules 작성
uxskill discover                            # 10 필드 인테이크
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

그런 다음 Cursor에서 묻습니다: *".ux/last-recommendation.json의 추천을 사용해 대시보드 화면 생성"*. Cursor는 `.cursorrules` 헤더를 읽고, 추천을 로드하고, 명시적 제약과 함께 대시보드 생성을 파견합니다.

### 2. Claude Code에서 Stripe 스타일 랜딩 생성

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> 프로젝트 타입? landing
> 산업? fintech-payments
> 톤? 진지함, 기술적, 자신감
> 필수 항목? dark-mode, AA, 모바일 우선
> 금지 항목? purple-gradients, three-equal-cards
> 참조 브랜드? stripe
> 스택? nextjs-15-app-router
> 지역? 글로벌
> 성공 지표? 가입 전환

/ux-recommend
> [선택된 스타일, 팔레트, 타입 페어, 모션 프리셋, 컴포넌트, 브랜드 본보기 반환]

/ux-design "Stripe 브랜드 사양을 본보기로 랜딩 생성"
> [frontend-engineer가 페이지 생성]

/ux-lint .
> [통과 — Stripe 브랜드 사양이 존중됨]
```

### 3. AI 슬롭을 위한 CI에서 기존 코드 감사

2주 전에 Next.js 앱을 출시했습니다. 모든 PR에 AI 지문에 대한 단단한 바닥을 원합니다.

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

보라-파랑 그라데이션, 96px의 Inter, "John Doe" 추천사, 아이콘으로서의 이모지를 도입하는 PR은 CI에서 실패합니다. LLM 비용 없음. ~200ms.

### 4. "AI 생성처럼 느껴지는" 기존 화면 폴리시

다른 모든 AI 생성 SaaS 사이트처럼 보이는 React 앱을 물려받았습니다. 그렇게 보이지 않게 만들고 싶습니다.

```
/ux-critique src/components/Hero.tsx
> [3승, 3패, 1수 — 견해는 솔직]

/ux-lint src/
> [15개의 높은 심각도 AI 지문이 표시됨]

/ux-polish src/components/Hero.tsx
> [LLM 구동 폴리시 + AI-슬롭 제거]

/ux-fix
> [소견을 원자 커밋으로 적용, 린터 재실행]
```

세 개의 명령, 하나의 폴리시된 화면, 수정마다 원자 커밋.

### 5. Linear 스타일 커맨드 팔레트 디자인

```
/ux-component command-palette --brief="Linear 스타일, 다크, 모노스페이스 단축키, 최근 항목 우선"
> [data/brands/linear.app.json에서 토큰 + 시그니처 무브 읽기]
> [data/components.json에서 command-palette 해부 + 상태 읽기]
> [명시적 Linear 사양으로 frontend-engineer 파견]
```

생성된 컴포넌트는 Linear의 실제 색 토큰, 타입 스택, 모션 규약, 헤어라인 밀도를 사용합니다 — "일반 다크 UI"가 아닙니다.

### 6. 이해관계자와 90분 디자인 사고 워크숍 운영

5명을 90분. 그들이 "분위기"가 아닌 게임 플랜과 함께 떠나길 원합니다.

```
/ux-workshop "로열티 월렛 피벗" \
  --participants="PM 2명, 디자이너 1명, 엔지 리드 1명, 고객 담당 1명" \
  --minutes=90
```

플러그인이 다섯 단계(탐색 → 히트맵 → 이해관계자 지도 → 솔루션 스케치 → 게임 플랜)를 끝에서 끝까지 시간 박싱하고 단계별 구체적 산출물로 진행합니다. 출력은 `.ux/last-workshop.json` — "흥미로운 발견"이 아닌 게임 플랜.

### 7. 출시 후 발행 가능한 케이스 스터디 작성

로열티 월렛을 출시했습니다. 포트폴리오 작품을 원합니다.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [.ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json 읽기]
> [(A)-(G) 번호 섹션, 헤어라인 구분선, 양언어 안전 레이아웃의 Wfrah 편집체 케이스 스터디 생성]
> [case-studies/bashiti-loyalty.html 작성]
```

케이스 스터디는 완성된 발행 가능한 아티팩트입니다 — 초안이 아닙니다. 순수 모노크롬, 편집체 타이포, 포트폴리오에 바로 배포할 준비가 된.

### 8. 비-AI 환경에서 discovery 실행(구조화 인테이크만)

프로젝트를 범위 잡고 있습니다. 아직 추천은 필요 없습니다 — 구조화된 브리프가 필요합니다.

```bash
uxskill discover
# 10 필드 인테이크, .ux/last-discovery.json에 저장

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

JSON을 팀에 건네거나, Notion 문서에 붙이거나, 별도 AI 도구에 공급할 수 있습니다. ux-skill은 엔진일 뿐 아니라 구조화 인테이크 도구이기도 합니다.

### 9. MASTER.md 지속성 — 저장소 안의 디자인 결정

`/ux-recommend` 후, 선택된 스타일 + 팔레트 + 타입 + 모션 + 컴포넌트 + 브랜드 본보기 + 가드레일을 팀이 리뷰하고, 차이를 보고, 버전 관리할 수 있는 사람이 읽기 쉬운 Markdown 파일로 지속시킵니다.

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md`(YAML 프론트매터 + 본문)와 `persist save-page`를 통해 생성된 화면마다 `.ux/design-system/pages/<name>.md`를 씁니다. 멱등 — 같은 입력은 바이트 단위로 같은 출력을 만들기 때문에, 상태가 바뀌지 않은 재실행은 git에서 no-op입니다.

---

## 다른 대안들과의 비교

짧은 요약 표. 완전한 컬럼별 비교는 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)에 있습니다.

| 차원 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| 슬래시 명령 | **22** | 1 | 19 | 1 | 1 | 다수 | 1 | 1 | 1 |
| 컴포넌트 | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| 모션 프리셋 | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 브랜드 사양 | **110** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 안티패턴 규칙 | **100** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 안전 결정론적 린터 | **예** | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 |
| 지원 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery 게이트 | **10 필드** | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 |
| `.ux/` 상태 체인 | **예** | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 |
| 스타 수(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 솔직한 평가

- **ui-ux-pro-max**는 인지도에서 더 크고, 18 IDE를 출시하며, CSV 위에 BM25 스타일 검색이 있습니다. 컴포넌트 매니페스트, 모션 매니페스트, 브랜드 라이브러리, 결정론적 린터를 출시하지 않습니다.
- **open-design**은 19 스킬 + 미리보기를 가지지만 Claude Code 지원만 있고 반-슬롭 층이 없습니다.
- **hallmark**가 정신에 가장 가깝습니다(역시 반-슬롭) — 하지만 단일 스킬입니다, 엔진도, 매니페스트도, 체인 명령도 없습니다.
- **material-3-skill**은 구체적으로 Material Design 3가 필요할 때 훌륭합니다. MD3에서는 경쟁하지 않습니다.

차원별 완전한 디테일은 [compare.html](https://uxskill.laithjunaidy.com/compare.html)에 있습니다.

---

## 로드맵

### v2.1 — 린터 완성(2026 Q3)

- **+17개의 미루어진 안티패턴 규칙**으로 총 52개. 타깃: dark-on-dark 호버 상태, 색만으로 상태 인코딩, 잉여 z-index 에스컬레이션, JS의 하드코딩 브레이크포인트, disabled 상태 대신 opacity 등.
- **기계적으로 수정 가능한 소견의 안전한 재작성을 위한 `uxskill lint --fix`**(`button-no-type`, `img-no-alt` 빈 문자열, `console-log-leak` 제거).
- **린터 소견을 인라인으로 표시하는 VS Code 확장**(CI 실행 불필요).

### v2.2 — 컴포넌트 매니페스트 확장(2026 Q4)

- **+50 컴포넌트**로 총 198. 새로움: 비동기 필터 콤보박스, 최근 항목 휴리스틱 커맨드 팔레트, 조건부 폼 스텝, payment-element 변형, RTL 인식 데이트 피커, MENA 전용 전화 입력, 히즈리 오버레이가 있는 캘린더 그리드.
- **6개 스택에서 컴포넌트별 코드 발행**(Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, vanilla HTML/CSS).
- **컴포넌트 플레이그라운드**가 uxskill.laithjunaidy.com/playground에 — 추천 엔진 시도와 라이브 컴포넌트 미리보기.

### v3 — 마켓플레이스 + 락인(2027)

- **브랜드 사양 마켓플레이스** — 커뮤니티 브랜드 사양 발행과 발견. 모더레이션을 지원하는 유료 발행.
- **커스텀 안티패턴 규칙** — 프로젝트가 `data/anti-patterns.local.json`에서 자체 regex 규칙을 정의(v2에 이미 출시; v3에서 발견 + 공유 추가).
- **`uxskill plan`** — 브리프에서 단일 화면이 아닌 전체 다중 페이지 사이트 계획.
- **Figma 플러그인 패리티** — 같은 추천 엔진을 Figma에서 표면화.

---

## 기여하기

이슈와 PR을 환영합니다. 세 가지 높은 레버리지 영역:

### 안티패턴 규칙 추가

1. `data/anti-patterns.json`을 편집합니다 — `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`를 가진 항목을 추가합니다.
2. `tests/linter/`에 테스트 추가 — 규칙을 트리거하는 파일과 그렇지 않은 파일.
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx`를 실행 — 발화 확인. `tests/linter/should-not-trigger/<rule>.tsx`를 실행 — 발화 안 함 확인.
4. PR을 엽니다.

### 브랜드 사양 추가

1. `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`를 가진 `data/brands/<slug>.json`을 만듭니다.
2. 대응하는 산문을 `references/brands/<slug>.md`에 추가합니다.
3. `data/brands/_index.json`에 등록합니다.
4. PR을 엽니다. 사양은 1차 원천에 의해 뒷받침되어야 합니다(브랜드의 실제 제품, 공개 디자인 시스템, 또는 출판하는 경우의 DESIGN.md).

### 모션 프리셋 추가

1. `data/motion-presets.json`을 편집합니다 — `id`, `name`, `category`, `tokens`, `stacks`(framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`를 가진 항목을 추가합니다.
2. 프리셋은 reduced-motion 변형을 가져야 합니다. 예외 없음.
3. PR을 엽니다.

### 프로세스

- 전체 프로세스는 [CONTRIBUTING.md](CONTRIBUTING.md)를 읽어주세요.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)를 읽어주세요.
- 새 규칙과 브랜드 사양은 다음 기준으로 검토됩니다: 1차 원천에 의한 뒷받침, 단일 프로젝트에 과적합 없음, 데이터에 이모지 없음, 적용 가능한 경우 RTL 안전 동작.

---

## 라이선스, 저자, 감사의 말

### 라이선스

MIT. 사용, 포크, 그 위에 빌드. AI 슬롭을 출시하는 것을 막아주었다면 저장소에 스타를 눌러주세요 — 가장 저렴한 지원 방법입니다.

### 저자

**Laith Aljunaidy** — MENA 우선 로열티 플랫폼 [Dot](https://thedotwallet.com)의 단독 창업자. AI 생성 프런트엔드가 모두 같아 보이지 않게 ux-skill을 만듭니다.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- 이메일: laith.aljunaidy.laith@gmail.com
- 저장소: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- 사이트: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 감사의 말

- Claude Code와 이것을 배포 가능하게 만든 스킬 / 플러그인 아키텍처를 제공한 Anthropic 팀에.
- Nielsen Norman Group, Laws of UX(lawsofux.com), 그리고 `data/ux-guidelines.json`의 근거가 되는 작업을 한 UX 리서치 커뮤니티에.
- `data/brands/`에 나열된 모든 브랜드에 — 그들의 공개 디자인 시스템이 브랜드 사양의 진실의 원천입니다.
- v2 Python 엔진의 씨앗이 된 단일 샷 Claude 스킬의 원래 v1 기여자들에게.
- 우리가 비교한 8개의 인기 Claude UX 플러그인에 — 그들이 막대를 올렸습니다; 이게 우리의 답입니다.

---

**ux-skill** · **v2.0.0-alpha.1** · Claude Code, Cursor, Windsurf 그리고 다른 모든 AI 코딩 도구가 AI 생성으로 읽히지 않는 프런트엔드를 출력하도록 빌드.

> [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)에서 저장소에 스타 · `pip install uxskill` 또는 `npx uxskill init`으로 설치 · [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)에서 비교 둘러보기
