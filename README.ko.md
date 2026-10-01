[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · **한국어** · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: Claude Code, Cursor, 그리고 모든 AI 코딩 도구를 위한 디자인 인텔리전스 엔진

**AI가 만든 UI를 평범하지 않고 개성 있게 만드는 디자인 인텔리전스 엔진.** 17개 AI 코딩 도구 중 어디에 넣어도 결과물이 더 이상 AI가 만든 것처럼 보이지 않습니다. 무료, MIT, 오프라인, LLM 없음.

```bash
pip install uxskill
```

**[GitHub에서 ux-skill에 스타 주기](https://github.com/Laith0003/ux-skill)**: 도움이 됐다면 이것이 프로젝트를 돕는 가장 손쉬운 방법입니다. 처음이신가요? [60초 둘러보기](#빠른-설치)로 시작하거나 [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)에서 실제로 확인하세요.

![전: 흔한 스톡 사진 히어로, 옅은 보라색 그라데이션, 브랜드 정체성 없음. 후: 어두운 스크림 아래의 실제 공사 현장 사진, 호박색 포인트를 준 에디토리얼 헤드라인, 히어로에 들어간 견적 요청 폼. 같은 프롬프트라도 ux-skill이 제약을 주면 결과가 달라집니다.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*전: 흔한 스톡 사진 SEO 슬롭. 후: 어두운 스크림 아래 실제 공사 현장 사진을 쓴 히어로, 호박색 포인트의 에디토리얼 헤드라인, 히어로 안의 견적 폼. 같은 AI 코딩 도구, 같은 프롬프트라도 ux-skill이 제약을 주면 결과가 달라집니다.*

> **v4.0, FOUNDATIONS: 명령 하나로 WCAG 검사를 통과한 완전한 디자인 시스템을 만들고, 아랍어와 오른쪽에서 왼쪽 쓰기를 기본 지원합니다.** AI 코딩을 위한 가장 강력한 UX 플러그인. 결정론적 7축 신시사이저를 갖춘 Python 추론 코어, 쿼리 가능한 JSON 매니페스트 12개(스타일 84개, 팔레트 176개, 타입 페어링 70개, 컴포넌트 148개, 산업 184개, 차트 유형 35개, 모션 프리셋 57개, UX 법칙 112개, 안티패턴 규칙 171개, 기술 스택 25개, 브랜드 스펙 160개), 슬래시 명령 18개, 서브에이전트 5개, MCP 도구 25개, 그리고 결정론적 반-AI 슬롭 린터. 크로스 IDE: Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer, Roo Cline에 설치됩니다.

> **브랜드 이름은 `ux-skill`입니다.** PyPI / npm 패키지 이름은 `uxskill` 그대로입니다. GitHub 저장소는 [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)에 있습니다.

**만든 사람:** [Laith Aljunaidy](https://laithjunaidy.com), 암만의 디자이너이자 CTO · **사이트:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **모든 Claude UX 플러그인과 비교:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-인스톨러)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### 4.0의 새 기능: 파운데이션

브랜드 색 하나를 넣으면 디자인 시스템이 나오고, 그 대비는 받기 전에 이미 검사되어 있습니다.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 이상. MCP 서버는 `pip install --upgrade 'uxskill[mcp]'`. pipx라면 `pipx install uxskill`(이미 설치된 3.x 위에는 `pipx upgrade uxskill`). npm이라면 `npx uxskill@latest`. 3.x에서 오셨나요? [마이그레이션 가이드](docs/migrating-to-4.md)가 3.x의 모든 토큰을 4.0의 역할에 대응시킵니다.

**제품이나 랜딩 페이지를 만드나요?** 페이지에서 연결할 `tokens.css`, 선택한 서체에 메트릭을 맞춘 대체 글꼴이 담긴 `fonts.css`, 서체를 직접 가진 파일에서 불러오는 `fonts-self-host.css`, 도구용 `tokens.json`, `art/`에 담긴 장식용 브랜드 아트, 그리고 무엇을 왜 만들었는지, 어떤 페이지 구성에서 시작하면 되는지 쉬운 말로 설명하는 `system-report.md`를 받습니다. 스타일은 역할(`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`)로 지정하고, 다크 모드, 고대비, 촘촘한 간격, 오른쪽에서 왼쪽, 동작 줄이기는 `<html>`의 속성 하나로 전환합니다. 서체는 보고서가 알려 주는 Google Fonts 링크나 `fonts-self-host.css`와 `fonts/` 폴더로 불러오고, 어느 쪽이든 `fonts.css`를 `tokens.css`보다 먼저 연결하세요. 두 파일 모두 수정하지 마세요. `--brief`를 쓰면 브리프에 산업과 톤이 있을 때 모양새가 그것을 따르고, 구조화된 필드(연령, 언어, 기본 스킴, 읽는 상황)가 글자 크기, 터치 영역, 문자 체계, 처음 열리는 스킴을 정합니다. discovery는 산업을 묻지 않으므로 `/ux-system create`가 묻습니다. Claude Code에서는 `/ux-system create`가 설치된 버전을 확인하고, 빌드를 실행하고, 보고서를 설명합니다.

**디자인 시스템을 설계하나요?** 아홉 가지 파운데이션(색, 타이포그래피, 간격, 레이아웃, 모서리, 테두리, 엘리베이션, 모션, 이미지)이 일곱 개 축에 따라 연속적으로 바뀌며, 프리미티브와 시맨틱 역할을 갖추고, 모든 모드의 값을 담은 W3C 디자인 토큰 형식(DTCG 2025.10)으로 나옵니다. 입력이 같으면 바이트까지 같습니다. MCP에서는 `ux_system_build`가 보고서, 게이트 결과, 각 파일의 크기를 돌려주고, `out`을 주면 명령과 같은 파일을 씁니다.

- **WCAG 게이트.** 텍스트, 컨트롤, 포커스의 모든 색 조합을 라이트와 다크, 표준 대비와 고대비에서 측정합니다. 표준 대비에서는 WCAG 1.4.3(텍스트 4.5:1)과 1.4.11(비텍스트 3:1), 고대비에서는 WCAG 1.4.6(텍스트 7:1)을 적용하고, WCAG가 비텍스트의 강화 기준을 정하지 않기 때문에 대부분의 비텍스트 요소에는 고대비에서 4.5:1이라는 자체 하한을 더합니다. 통과하지 못한 시스템은 쓰지 않으며, 메시지가 무엇을 바꿔야 하는지 알려 줍니다.
- **기본적으로 안전.** 내용이 다른 파일은 절대 덮어쓰지 않습니다. `--force`는 요청할 때만 파일을 교체합니다.
- **아랍어.** `dir="rtl"` 아래에서는 텍스트가 자체 크기와 줄 높이를 가진 아랍어 서체로 바뀝니다. 간격은 논리 속성을 쓰고 모션은 좌우가 뒤집힙니다. `--latin-only`로 뺄 수 있습니다.

**이미 가진 시스템.** `/ux-system enhance --from`은 기존 시스템을 원래 이름 그대로 읽고(DTCG 토큰, CSS 사용자 정의 속성, Tailwind 테마, markdown 규칙 파일, Figma 변수 내보내기), 같은 게이트로 검사하고, 코드가 실제로 그것을 어떻게 쓰는지 측정합니다. 아무것도 다시 쓰지 않습니다. `/ux-system extend --from`은 기존 토큰을 하나도 바꾸지 않고 파운데이션, 역할, 계약을 옆에 두는 확장 파일에 더하고, `uxskill system export`는 tokens.css, Tailwind 4 테마, Figma 변수로 써 냅니다. 4.2에서는 신뢰 레이어(쓸 때마다 lint, 마무리 리뷰어)와 출시가 더해집니다. [changelog](CHANGELOG.md)를 참고하세요.

**컴포넌트와 섹션.** 23개의 컴포넌트 계약은 컨트롤의 각 부분이 상태마다 어떤 토큰에 묶이는지, 각 상태가 어떻게 움직이는지를 정합니다. 상태 변화는 `motion.state`로 전환되고, 누르기는 `motion.press.scale`로 크기가 바뀌며(동작 줄이기에서는 멈춰 있음), 탭, 메뉴, 세그먼트 컨트롤은 인디케이터 하나를 밀어 움직입니다. 14개의 섹션 계약(히어로, 가격, FAQ, 푸터 등)은 각 섹션의 역할, 슬롯에 들어가는 컴포넌트, 필요한 근거, 휴대폰에서 쌓이는 방식을 정합니다. 이것으로 만든 페이지는 사진을 씁니다. 인터페이스 조각은 추가 이미지일 뿐, 사진을 대신하지 않습니다.

**페이지를 읽는 린터.** 171개 규칙 중 다수가 파싱된 CSS와 마크업을 추가로 검사하며 페이지 자체의 시스템을 읽습니다. 모션은 그 곡선에서 타이밍을 재고, 디스플레이 제목의 줄 높이는 엔진의 하한을 지키게 하며, 숨겨진 컨트롤은 탭 순서에서 빠져야 합니다. `uxskill lint --render`는 각 페이지를 헤드리스 Chromium에서 데스크톱 폭과 휴대폰 폭으로 열고 직접 조작해, 보이지 않거나 잘린 포커스 링, 늦게 반응하는 호버와 누르기, Escape 후 사라지는 포커스, 동작 줄이기에서도 여전히 움직이는 누르기를 잡아냅니다.

**명령은 더 적게.** 슬래시 명령 25개가 18개로 줄었습니다. `/ux-discover`는 `--frame`과 `--recommend`를, `/ux-design`은 `--component`, `--dashboard`, `--from-image`를 받고, `/ux-polish`는 점수가 90에 이르거나 세 라운드가 지날 때까지 lint, 수정, 재 lint를 반복하며, `/ux-init`은 `--stats`를 받습니다. 이전 이름 일곱 개는 별칭으로 계속 쓸 수 있고 4.1에서 사라집니다. [별칭](#별칭-41에서-제거)을 참고하세요.

**화면별 플레이북.** 랜딩, 대시보드, 컴포넌트 규칙은 `references/surfaces/`에 각각 플레이북 하나씩 있습니다. `/ux-design`은 모드에 맞춰 정확히 하나만 불러오므로, 대시보드 빌드가 히어로 규칙을 읽을 일은 없습니다.

테스트 **9764개 통과**. 오프라인. 결정론적. LLM은 절대 호출하지 않습니다.

### v3.1의 새 기능: 브랜드에 충실, 반응형, 생동감

- **브랜드 충실도는 기대가 아니라 강제입니다.** 기본 색은 로고의 픽셀에서 읽습니다(가장 많이 칠해진 CSS가 아니라). 기본 글꼴은 로고의 글자 스타일에 맞지 않으면 거부됩니다. 추출한 브랜드는 `recommend` -> `synthesize`로 전달되고, `evaluate`의 **엄격한 하한**이 브랜드 색이나 로고를 잃거나 실제 이미지가 없는 출력을 실패 처리합니다. 공개 `brand.md` 규약과 양방향 상호 운용(렌더 + 가져오기).
- **모바일 우선, 게이트로 보장.** 새로운 크래프트 파운데이션(`responsive.md`, `component-behaviors.md`)과 줄바꿈을 인식하는 게이트가 가로 스크롤, 줄이 넘어가는 내비, 워드마크, 버튼 레이블, 지나치게 높은 고정 헤더를 실패 처리합니다.
- **와우 레이어.** 엔진이 페이지마다 서로 맞물린 시그니처 순간 2-3개를 끌어냅니다. "와우는 사용자에게서만 나온다"는 원칙은 뒤집혔습니다.
- **더 날카로운 린터**(152개 규칙): 필수 이미지와 아이콘 전용 요소 감지, 플레이스홀더 토큰과 `100vw` 규칙. 시드가 있는 picsum은 유지하고 무작위는 제거.

전체 노트는 [CHANGELOG.md](CHANGELOG.md)에 있습니다.

### v3에서 새로워진 점

- **브랜드 스펙은 템플릿이 아니라 학습 데이터가 됩니다.** 160개 브랜드 스펙은 더 이상 추천기가 고르는 카탈로그가 아니라 신디사이저가 증류하는 어휘입니다. 호출마다 새로운 출력이 나옵니다.
- **7축 신디사이저** (warmth, contrast, density, geometry, formality, motion, type_personality). 브리프는 결정론적으로 축 값으로 매핑되고, 축 값은 새로운 palette + 타이포 + spacing + radius + motion 토큰으로 컴파일됩니다.
- **세 가지 자동 디스패치 모드**: `strict_brand` (단일 브랜드 100%), `brand_anchor` (단일 브랜드 70% + 형제 브랜드에서 축 적응 30%), `pure_synthesis` (브랜드 미지정, 축 일치 예제 8개에서 증류).
- **결정 원장이 추천기를 재정렬합니다.** `.ux/decisions.jsonl`이 동일한 `(industry, ui_type)` 버킷의 과거 승리로 후보를 재정렬합니다. 콜드스타트 안전. `lint_score >= 80` + `user_accepted = true`인 결정만 카운트합니다.
- **축 상호작용 행렬**: 경쟁 축 간의 명시적 충돌 해결 (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). 더 이상 침묵의 임시 규칙 없음.
- **`/ux-evolve` 자동 루프**(4.0에서는 `/ux-polish`의 기본 루프): 점수 ≥ 90, 정체기, 또는 4.0에서는 3라운드(v3에서는 5)까지 lint → polish → re-lint. 품질 게이트는 65.
- **3개의 신규 MCP 도구** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **로컬 통계 대시보드**: `uxskill stats --html`이 **당신의** 설치가 무엇을 배웠는지 보여주는 `.ux/stats.html`을 씁니다. 텔레메트리 없음, 글로벌 집계 없음.
- **223개 테스트 통과.** 오프라인. 결정론적. LLM 한 번도 호출 안 함.

전체 세부 내용은 [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain)에.

### Star 히스토리

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill란 무엇인가

ux-skill은 AI 코딩 도구를 위한 **디자인 인텔리전스 엔진**입니다. Python 패키지로(`pip install uxskill`), Claude Code 플러그인으로, 그리고 17 IDE용 멀티 인스톨러로 동작합니다. 엔진은 프로젝트 브리프(산업, 청중, 톤, 필수 항목, 금지 항목, 스택, 지역)를 받아 추천 디자인 시스템 한 벌을 반환합니다: 스타일, 팔레트, 타입 페어, 모션 프리셋, 컴포넌트, 연구할 브랜드 본보기, 그리고 지켜야 할 안티패턴 가드레일. 추천은 결정론적입니다, 같은 입력은 항상 같은 출력을 만들어냅니다.

플러그인은 당신과 AI 코딩 도구 사이에 자리합니다. Claude Code, Cursor 또는 다른 AI 어시스턴트에게 "핀테크 랜딩 페이지 만들어줘"라고 요청하면, 어시스턴트는 보통 즉흥적으로 만들고, 그 결과는 5초 안에 AI 생성으로 식별됩니다(보라색에서 파란색 그라데이션, 같은 크기의 카드 세 개, 디스플레이 크기의 Inter, 추천사의 "John Doe", 기본 300ms 트랜지션, 가운데 정렬 히어로, 튀는 화살표 CTA). ux-skill은 즉흥을 **구조화된 제약**으로 바꿉니다. `/ux-discover`로 브리프를 담고 시스템을 고르고, `/ux-design`으로 코드를 생성하고, `/ux-lint`로 커밋 전에 171개의 결정론적 반-AI 슬롭 규칙을 통과하는지 확인합니다.

이 README가 정전(正典) 참조입니다. 모든 명령, 모든 서브에이전트, 모든 데이터 매니페스트, 모든 설치 경로, 모든 브랜드 사양, 모든 안티패턴 카테고리, 전부 여기에 문서화되어 있습니다. Claude Code 디자인 플러그인을 찾고 있거나 Cursor, Windsurf, Codex용 AI 디자인 도구를 비교하고 있다면, 이걸 처음부터 끝까지 읽고 [compare.html](https://uxskill.laithjunaidy.com/compare.html)을 나란히 두고 보세요.

---

## 목차

1. [브레인, v3.0이란 무엇인가](#브레인-v30이란-무엇인가)
2. [빠른 설치](#빠른-설치)
3. [숫자, 상위 8개 Claude UX 스킬과의 실시간 비교](#숫자-상위-8개-claude-ux-스킬과의-실시간-비교)
4. [아키텍처, 부품들이 어떻게 맞물리는가](#아키텍처-부품들이-어떻게-맞물리는가)
5. [18개 슬래시 명령, 상세 참조](#18개-슬래시-명령-상세-참조)
6. [5개의 서브에이전트](#5개의-서브에이전트)
7. [11개의 데이터 매니페스트](#11개의-데이터-매니페스트)
8. [171개 반-AI 슬롭 규칙, 린터](#171개-반-ai-슬롭-규칙-린터)
9. [160개의 브랜드 DESIGN.md 사양, 카테고리별](#160개의-브랜드-designmd-사양-카테고리별)
10. [MCP 서버, 비대칭 한 수](#mcp-서버-비대칭-한-수)
11. [17 IDE 인스톨러](#17-ide-인스톨러)
12. [사용 사례, 구체적인 시나리오](#사용-사례-구체적인-시나리오)
13. [다른 대안들과의 비교](#다른-대안들과의-비교)
14. [로드맵](#로드맵)
15. [기여하기](#기여하기)
16. [라이선스, 저자, 감사의 말](#라이선스-저자-감사의-말)

---

## 브레인: v3.0이란 무엇인가

v3.1.0은 ux-skill 역사상 가장 큰 아키텍처 전환입니다. 추천기는 더 이상 카탈로그에서 템플릿을 고르지 않습니다, 엔진이 브리프마다 새로운 디자인 언어를 **합성**합니다. 동일한 브리프는 항상 동일한 출력을 만들지만(완전히 결정론적), 다른 브리프는 각자 새로운 시스템을 얻습니다. 브랜드 스펙은 더 이상 템플릿이 아니라 엔진이 어휘를 배우는 학습 데이터입니다. 시스템은 자신의 역사를 보고, 피드백 루프를 로컬에서 닫으며, LLM을 한 번도 호출하지 않습니다.

컴파일러는 **결정론적 7축 신디사이저**입니다, warmth, contrast, density, geometry, formality, motion, type_personality. 모든 브리프가 축 값으로 매핑되고, 축 값이 새로운 palette + 타이포 + spacing + radius + motion 토큰으로 컴파일됩니다. 모듈러 타이포 스케일은 contrast에서 비율을 고릅니다(1.200 quiet / 1.250 balanced / 1.333 loud). 레이아웃 프리미티브는 구축에 의해 반응형(`auto-fit minmax(min(N, 100%), 1fr)` + 컨테이너 쿼리). 깨진 레이아웃은 표현 불가하므로 발행할 수 없습니다.

세 가지 자동 디스패치 모드: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% Stripe 토큰, 최단 경로); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 4개 형제 브랜드에서 축 적응 30%); `pure_synthesis` (브랜드 미지정 → 무한 공간, 축 일치 예제 8개를 새 디자인 언어로 증류). 경쟁 축은 문서화된 **축 상호작용 행렬**로 해결됩니다, dense + corporate는 4px로 컴파일(density 승, Bloomberg 학파), airy + corporate는 12px(formality 승, 럭셔리), soft + playful은 18px radius, sharp + corporate는 2px. 구현에 숨은 임시 규칙 없음.

**결정 원장** (`.ux/decisions.jsonl`, 스키마 `_v: 1` 잠금)이 피드백 루프를 닫습니다. 추천기는 이제 같은 `(industry, ui_type)` 버킷의 과거 성공을 바탕으로 후보를 재정렬합니다. 콜드 스타트에도 안전하며, 이전 결정이 3건 미만이면 재정렬을 건너뜁니다. `lint_score >= 80` AND `user_accepted = true`인 결정만 셉니다. 또한 `/ux-polish`는 점수 ≥ 90, 정체기, 또는 3라운드까지 lint → polish → re-lint를 돌리고, 65라는 품질 게이트 아래의 출력은 `--force` 없이는 거부합니다. 결과적으로 모든 설치는 자기 코퍼스로 더 똑똑해지고, 모든 실행은 머신 사이에서 재현되며, 엔진은 완전히 오프라인으로 남습니다.

---

## 빠른 설치

세 가지 설치 경로. 환경에 맞는 것을 고르세요.

### 경로 1: Claude Code 마켓플레이스(정전)

Claude Code 안에서 일한다면, 플러그인 마켓플레이스를 통해 설치합니다:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

이것으로 슬래시 명령 18개(4.1까지 별칭으로 남는 이전 이름 7개 포함)와 서브에이전트 5개가 Claude Code 세션에 연결됩니다. 설치 후 `/ux-init`을 실행해서 프로젝트별 `.ux/` 상태 디렉터리를 설정하고 Python 엔진이 도달 가능한지 검증하세요.

### 경로 2: pip(범용)

Claude Code 밖에서 일한다면(Cursor, Windsurf, CLI, CI), Python 패키지를 설치합니다:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

패키지는 CLI 진입점으로 `ux`와 `uxskill` 두 가지를 노출합니다, 같은 바이너리입니다.

### 경로 3: npx(Python 직접 관리 불필요)

Python을 직접 관리하고 싶지 않다면, npx 래퍼가 `pipx`를 통해 모든 것을 부트스트랩합니다:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### 설치 검증

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

이 개수들을 모두 더하면 1,262개 항목입니다. 개수가 0으로 반환되면 JSON 파일이 누락된 것이니 [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues)에 이슈를 열어주세요.

---

## 숫자: 상위 8개 Claude UX 스킬과의 실시간 비교

스타 수는 **2026-05-28**에 `gh api`로 마지막으로 확인했습니다. ux-skill(Laith0003/ux-skill)은 가장 늦게 진입한 사람입니다, 인지도는 작고, 아키텍처는 깊습니다. 아래 비교는 솔직합니다: 어디서 지고, 어디서 이기는가.

| 플러그인 | 스타 수 | 아키텍처 | 슬래시 명령 | 린터(CI 안전) | 브랜드 사양 | 컴포넌트 | 모션 프리셋 | 지원 IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV, 단일 스킬 | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19개 스킬 + 미리보기 | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + 리서치 기반 안목 | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | 단일 62 KB SKILL.md + 스크립트 | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | MCP에 연결된 스킬 라이브러리 | 다수 | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | 단일 미학 스킬 | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | 반 슬롭 디자인 스킬 | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 컴포넌트 + 감사 | 1 | - | (MD3 전용) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python 엔진 + 매니페스트 12개 + 명령 18개 + 서브에이전트 5개 + CI 린터** | **18** | **결정론적 규칙 171개** | **160** | **148** | **57** | **17** |

### 지는 곳

- **인지도.** 그들은 수십만 스타를 가지고 있습니다. 우리는 14개. 스타를 눌러주세요, 가장 저렴한 도움 방법입니다.
- **브랜드 인지.** ui-ux-pro-max와 open-design는 일이 아닌 달 단위로 앞서 있습니다.
- **마케팅 윤기.** 스크린샷, 데모 영상, 찾기 쉬운 랜딩 페이지가 있습니다. 우리에게는 철저한 README와 가벼운 랜딩만 있습니다.

### 이기는 곳

- **컴포넌트 라이브러리:** 해부, 상태, 사용한 토큰, 모션 사양을 포함한 148개의 문서화된 컴포넌트. 다른 8개 중 어느 것도 컴포넌트 매니페스트를 출시하지 않습니다.
- **모션 프리셋:** 스택 준비된 57개 항목(Framer Motion, GSAP, CSS), reduced-motion 폴백 포함. 다른 어떤 곳도 모션 매니페스트를 출시하지 않습니다.
- **안티패턴 린터:** 결정론적 규칙 171개, CI에서 실행되며 Critical/High에서 0이 아닌 코드로 종료. 다른 어떤 곳도 결정론적 린터를 내놓지 않습니다.
- **브랜드 사양:** 160개의 실제 DESIGN.md 사양(Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude 외 96개). 다른 어떤 곳도 브랜드 라이브러리를 출시하지 않습니다.
- **17 IDE 지원:** 같은 엔진, IDE마다 다른 접착제.
- **슬래시 명령 18개:** discovery, 생성(페이지, 컴포넌트, 대시보드, 이미지에서), 감사, lint, 폴리시 루프, 수정 루프, 케이스 스터디, 워크숍, 카피, 모션, a11y, 컨덕터, 완전히 통합.

전체 컬럼별 비교는 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)에 있습니다.

---

## 아키텍처: 부품들이 어떻게 맞물리는가

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

### 엔진이 실제로 동작하는 방식

1. **입력.** 브리프를 줍니다. `/ux-discover`로 대화형으로(10개 필드) 주거나 `ux recommend`에 플래그를 넘겨 비대화형으로 줍니다.
2. **5개의 병렬 검색.** 엔진은 매니페스트 전반에서 다섯 가지 조회를 동시에 실행합니다:
   - **산업 → recommended_styles** (industries.json)
   - **스타일 → 팔레트 + 타입 + 모션 호환성** (styles.json)
   - **톤 × 필수 요건 → 팔레트 필터** (palettes.json)
   - **스택 → 컴포넌트 호환성 + 모션 프리셋** (tech-stacks.json, motion-presets.json)
   - **금지 사항 + 지역 → 가드레일 + 브랜드 본보기 후보** (anti-patterns.json, brands/)
3. **병합.** 결정론적 병합기가 후보의 순위를 매기고, 충돌을 해결하고(예를 들어 필수 다크 모드가 팔레트 모드를 정함), 추천 시스템 하나를 내놓습니다.
4. **출력.** 선택된 스타일, 팔레트, 타입 페어, 상위 5개 모션 프리셋, 상위 12개 컴포넌트, 상위 5개 브랜드 본보기, 그리고 활성화된 171개 안티패턴 가드레일 전부를 담은 JSON 문서. 여기에 각 선택을 설명하는 근거 블록이 붙습니다.
5. **생성.** 이후 명령(페이지, 컴포넌트, 대시보드, 이미지 모드의 `/ux-design`과 `/ux-system`)이 추천을 받아 서브에이전트를 통해 실제 코드를 생성합니다.
6. **검증.** `/ux-lint`가 생성된 코드를 171개 규칙으로 다시 스캔합니다. CI에서 Critical/High가 있으면 0이 아닌 코드로 종료.

**v3에서 추가된 것.** 추천기는 이제 `.ux/decisions.jsonl`을 사용해 `engine/decisions/`에서 후보를 재정렬합니다(`lint_score >= 80` AND `user_accepted = true`인 결정만 세고, 이전 결정이 3건 미만이면 콜드 스타트로 안전하게 처리). 생성 경로는 `engine/synthesizer/`로 넘길 수도 있습니다. 이것은 결정론적 7축 컴파일러로, 카탈로그에서 템플릿을 고르는 대신 브리프마다 새로운 팔레트 + 타입 + 간격 + 모서리 + 모션 토큰을 만듭니다. 자세한 내용은 [브레인, v3.0이란 무엇인가](#브레인-v30이란-무엇인가)를 보세요.

**Python은 생각하고, HTML은 보여 주고, Markdown은 잇습니다.**

---

## 18개 슬래시 명령: 상세 참조

모든 명령은 `commands/` 아래 `.md` 파일로 제공되며 `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process`, `output state file`을 담고 있습니다. 아래 설명은 요약이고, 공식 사양은 원본 전체입니다.

명령은 일곱 묶음으로 나뉩니다: **부트스트랩과 인벤토리**, **discovery와 추천**, **생성**, **감사와 검증**, **수정과 폴리시**, **discovery와 내러티브**, **컨덕터**. 3.x의 이름 일곱 개는 4.1까지 [별칭](#별칭-41에서-제거)으로 계속 쓸 수 있습니다.

### 부트스트랩 & 인벤토리

#### `/ux-init`: 프로젝트 부트스트랩

- **무엇:** 어떤 IDE를 쓰고 있는지(`.claude/`, `.cursor/`, `.windsurf/` 등) 감지하고, 올바른 아티팩트를 설치하고, Python 엔진이 도달 가능한지 검증하고, 통계 스냅샷을 인쇄합니다. `--stats`는 스냅샷만 인쇄합니다: 버전 + 데이터 매니페스트의 항목 수.
- **사용 시점:** 새 프로젝트에 처음 설치할 때. ux-skill을 쓰는 프로젝트를 clone한 뒤. `pip install --upgrade uxskill` 뒤. `--stats`는 설치 후, 업그레이드 후, 또는 추천이 뜻밖의 결과를 내서 매니페스트가 불완전하다고 의심될 때.
- **건너뛸 시점:** 이미 이 프로젝트에서 실행했고 아무것도 바뀌지 않았다. `--stats`는 건너뛸 필요가 없습니다: 50ms짜리 읽기입니다.
- **호출:** `/ux-init`(인자 없음), `/ux-init --stats`, 또는 CLI에서 `uxskill init` / `uxskill stats`. `--decisions`는 결정 원장 요약을 더하고, `--html`은 `.ux/stats.html`을 씁니다.
- **출력:** IDE별 아티팩트([17 IDE 인스톨러](#17-ide-인스톨러) 참조) + `.ux/` 디렉터리 + stdout 요약. `--stats`: stdout으로 JSON(위의 [설치 검증](#설치-검증) 참조).
- **다음:** `/ux-discover`. `--stats`는 진단용입니다.

#### `/ux-mcp`: 엔진을 MCP 서버로 실행

- **무엇:** 엔진을 stdio 위의 Model Context Protocol 서버로 시작합니다. 25개 도구(추천기, 린터, 영속화, 신시사이저, 결정 원장, 이미지 추출, 데이터 매니페스트, 그리고 디자인 시스템의 빌드, 가져오기, 개선, 확장, 내보내기, 검사)를 플러그인 없이 MCP를 지원하는 어떤 호스트에서든 호출할 수 있습니다.
- **사용 시점:** MCP를 지원하는 다른 호스트에서 작업하면서 같은 엔진을 쓰고 싶다. 디자인 제약의 단일 출처가 필요한 멀티 에이전트 파이프라인을 돌린다. 추천기나 린터를 CI에서 상주 프로세스로 쓰고 싶다.
- **건너뛸 시점:** 플러그인이 설치된 Claude Code 안에 있다. 슬래시 명령이 이미 엔진에 닿습니다. 한 번만 답이 필요하다. `uxskill recommend`나 `uxskill lint`가 더 간단합니다.
- **호출:** `/ux-mcp`, 또는 `pip install 'uxskill[mcp]'` 후 셸에서 `ux-mcp`.
- **출력:** stdio JSON-RPC 서버. 클라이언트별 설정은 [MCP 서버](#mcp-서버-비대칭-한-수)와 `commands/ux-mcp.md`를 참고하세요.
- **다음:** 없음. 단계가 아니라 전송 계층입니다.

### discovery & 추천

#### `/ux-discover`: 강제 관문(10개 필드 입력, 프레이밍, 추천)

- **무엇:** 모든 프로젝트가 생성 명령 전에 반드시 거치는 10개 필드의 필수 입력. 프로젝트 유형, 대상, 주요 목표, 톤, 필수 요건, 금지 사항, 참고 브랜드, 스택, 지역, 성공 지표. **즉흥 금지.** 금지 문구("모던", "깔끔한")가 사용자에게 구체성을 요구합니다. 이어서 추천기를 실행합니다. Python 엔진이 12개 매니페스트에 걸친 5개의 병렬 검색으로 통합된 디자인 시스템 하나를 돌려줍니다(산업 → 스타일 → 팔레트 → 타입 → 모션 + 컴포넌트 + 브랜드 본보기 + 가드레일).
- **모드:** `--frame`은 누구를 위한 것인지, 결과, 가설, 성공 신호를 네 필드짜리 프레이밍 블록에 담습니다. 전체 입력보다 가볍습니다. `--recommend`는 저장된 브리프나 일회성 플래그로 추천기만 실행합니다.
- **사용 시점:** 모든 `/ux-design` 또는 `/ux-system` 전. 이전 브리프가 낡았을 때. `--frame`은 프로젝트, 스프린트, 일회성 작업을 시작할 때나 대화가 옆길로 샜을 때 중간에. `--recommend`는 지쳐 보이는 제품의 방향을 바꿀 때.
- **건너뛸 시점:** 버그를 고치는 중이다(`/ux-fix`). 린터 패스만 돌린다(`/ux-lint`). 지난 세션 이후 브리프가 그대로다.
- **호출(Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"`, 또는 `/ux-discover --recommend`.
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
- **출력:** `.ux/last-discovery.json`(10개 필드 브리프), `.ux/last-recommendation.json`(선택된 스타일, 팔레트, 타입 페어, 상위 5개 모션 프리셋, 상위 12개 컴포넌트, 상위 5개 브랜드 본보기, 활성화된 171개 안티패턴 가드레일 전부, 그리고 근거), `--frame`을 쓰면 `.ux/last-frame.json`(`{audience, outcome, hypothesis, success_signal}`).
- **다음:** `/ux-design [extra brief]` → 추천에 기반한 프런트엔드 코드. `/ux-design --component <name>` → 파악된 제약에 맞춘 컴포넌트 하나. `/ux-system` → 추천에서 나온 완전한 디자인 시스템. `/ux-lint` → 생성된 코드 검증.

### 생성

#### `/ux-design`: 브리프에서 아름답고 반-슬롭인 화면 생성

- **무엇:** discovery 브리프 + 추천에서 완전한 프로덕션급 프런트엔드 아티팩트(랜딩, 마케팅 사이트, 앱 셸)를 생성합니다. 반-슬롭과 arsenal 참조의 창작 지침 아래 `frontend-engineer`를 파견합니다. 브리프나 플래그가 네 가지 모드 중 하나를 고릅니다:
  - **페이지**(기본): 완전한 페이지나 여러 섹션으로 된 화면. `.ux/last-design.json`을 씁니다.
  - **`--component [name]`**: 프로덕션급 컴포넌트 하나(버튼, 모달, 내비바, 사이드바, 카드, 테이블, 폼, 차트). 네 가지 상호작용 상태 전부, 접근성, 브랜드 일치. 먼저 `.ux/last-recommendation.json`에서 컴포넌트를 찾고, 없으면 매니페스트를 직접 조회합니다. `.ux/last-component.json`을 씁니다.
  - **`--dashboard`**: 데이터 밀도 규율, 벤토 레이아웃, 표 형식 고정폭 숫자, 스파크라인 패턴, 카드 남용 방지, 의미 있는 상태 색, 절제된 모션. 차트를 붙여 놓은 마케팅 사이트가 아닙니다. `.ux/last-dashboard.json`을 씁니다.
  - **`--from-image <path>`**: 디자인 참고 이미지(PNG/JPG/WebP)를 순수 Pillow 컴퓨터 비전으로 읽고(주된 팔레트, 캔버스 명암, 타입 신호), 팔레트와 스타일 매니페스트에 대조한 뒤 그 추천으로 빌드합니다. `--extract-only`는 추출 후 멈춥니다. `.ux/last-image-extract.json`을 씁니다.
- **사용 시점:** "디자인해 줘", "만들어 줘", "랜딩 페이지 생성", "대시보드 만들기", "컴포넌트 만들기", "버튼 만들기", "관리자 패널 디자인", "운영자 콘솔", "KPI 보드", "이 스크린샷처럼 만들어 줘", 자유 형식 시각 산출물 요청 일체.
- **건너뛸 시점:** 빌드가 아닌 리뷰가 필요하다(`/ux-audit` 또는 `/ux-critique`). 백엔드/인프라 작업.
- **호출:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **출력:** 생성된 코드(HTML / Blade / JSX / Vue / Astro)와 모드별 상태 파일.
- **다음:** `/ux-lint` → 가드레일 검증. `/ux-polish` → 폴리시. `/ux-a11y` → 접근성 감사. `/ux-copy` → 마이크로카피 감사. `/ux-fix` → 소견을 원자 커밋으로.

#### `/ux-system`: 완전한 스타터 디자인 시스템 생성

- **무엇:** 디자인 시스템이 없는 프로젝트에 완전한 스타터 시스템을 제안합니다, 토큰(색, 타입, 공간, 모션, 모서리, 그림자), 기초 문서, 컴포넌트 계약, 다크 모드 페어링, 테마 스위처. `design-system-architect`를 파견합니다.
- **사용 시점:** "디자인 시스템이 없다", "우리에게 시스템을 만들어 줘", "토큰을 제안해 줘", "테마는 어때야 하나", "DS를 셋업해 줘".
- **건너뛸 시점:** 프로젝트에 이미 디자인 시스템이 있다면 대신 기존 시스템에 `/ux-design --component`를 사용. 백엔드/인프라.
- **호출:** `/ux-system create`(파운데이션 엔진), `/ux-system enhance --from <file>`(이미 가진 시스템을 측정), `/ux-system extend --from <file> --add <foundation>`(바꾸지 않고 덧붙이기), 또는 `/ux-system`(3.x 흐름. 파일에 없으면 먼저 discovery).
- **출력:** `tokens.json`, `foundations.md`, `components/*.md` 계약, 선택적 Tailwind / vanilla / SCSS 출력. 연결 컨텍스트를 위해 `.ux/last-system.json`을 씁니다.
- **다음:** `/ux-design --component` → 새 시스템 위에서 빌드. `/ux-design` → 새 토큰으로 화면 생성.

#### `/ux-motion`: 모션 처리

- **무엇:** 화면의 모션 층을 생성합니다, 지속 시간, 이징, 안무, reduced-motion 폴백, 성능 규율. 기존 모션을 5차원(타이밍, 이징, 의미, reduced-motion, 성능)에 대해 감사하기도 합니다.
- **사용 시점:** "모션 확인", "애니메이션 괜찮나", "모션 고치기", "애니메이션 리뷰", "모션 감사", "모션 성능 패스".
- **건너뛸 시점:** 화면에 모션이 없다(`/ux-audit` 또는 `/ux-polish`). 백엔드/인프라.
- **호출:** `/ux-motion path/to/component.tsx`(감사 모드) 또는 `/ux-motion --generate hero-entry`(생성).
- **출력:** 업데이트된 코드(생성 모드) 또는 `.ux/last-motion.json` 보고서(감사 모드).
- **다음:** `/ux-fix` → 모션 소견 적용. `/ux-polish` → 다듬기.

### 감사 & 검증

#### `/ux-lint`: 결정론적 regex 기반 린터(LLM 없음, CI 안전)

- **무엇:** 코드에 대해 171개 규칙을 실행합니다. LLM 호출 없음. CI에서 Critical/High에 부딪히면 0이 아닌 코드로 종료. 소스: `data/anti-patterns.json`. 규칙은 A11y(45), 콘텐츠(35), 레이아웃(18), 타이포그래피(16), 모션(14), 시각(14), 품질(12), 색(10), 성능(5), 깊이(2)를 커버합니다.
- **사용 시점:** 사전 커밋 훅. CI 게이트. `/ux-audit` 비용을 치르기 전에 대형 코드베이스에 대한 빠른 첫 패스. 어떤 모드든 `/ux-design` 후 생성 검증.
- **건너뛸 시점:** 수정 루프가 필요하다(린터는 보고만 합니다, 편집하지 않음, `/ux-polish --fix`나 `/ux-fix`로 연결). 안목 판단이 필요하다(`/ux-critique`).
- **호출(슬래시):** `/ux-lint src/`.
- **호출(CLI):** `uxskill lint .` 또는 `python3 bin/ux-lint.py .` 또는 `bash bin/ux-lint.sh --ci --fail-on high`.
- **호출(CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **출력:** 표준 출력의 소견(위치, 규칙 id, 심각도, 증거). 깨끗하면 종료 코드 0, `--fail-on high` 설정 시 Critical/High이면 비영.
- **다음:** `/ux-polish --fix` → 같은 패턴의 LLM 구동 대응물. `/ux-fix` → 소견을 심각도 정렬로 커밋 적용. `/ux-audit` → 완전한 6렌즈 추론 패스. `/ux-next` → 컨덕터에 결정 맡기기.

#### `/ux-audit`: 6렌즈 디자인 감사

- **무엇:** 여섯 렌즈(명료성, 위계, 접근성, 보이스, 모션, 안목)에 대한 구조적, 입장 있는 리뷰로 심각도 태그 소견을 산출합니다. Polaris 스타일 보고서. 먼저 `.ux/last-frame.json`을 읽습니다, 청중과 결과가 모든 소견의 심각도를 닻으로 잡습니다.
- **사용 시점:** 화면이 존재하고 변호 가능한 비평이 필요하다. "감사", "ux 리뷰", "이거 괜찮나", "뭐가 망가졌나", "산산조각 내 봐".
- **건너뛸 시점:** 화면이 아직 없다(`/ux-design`). 사용자가 한 렌즈만 원한다(타깃 명령 사용: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). 사용자가 안목 의견을 원한다(`/ux-critique`). 백엔드/인프라.
- **호출:** `/ux-audit https://example.com/pricing` 또는 `/ux-audit src/components/Pricing.tsx`.
- **출력:** `.ux/last-audit.json`을 씁니다, `findings` 배열 `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **다음:** `/ux-fix` → 소견 적용. `/ux-polish` → 폴리시. `/ux-design` → 구조적 재설계가 필요하다면.

#### `/ux-a11y`: WCAG 2.1 AA 감사 + 기본 예의 체크

- **무엇:** 구조화된 WCAG 2.1 AA 감사에, 자동 도구는 통과하지만 실제 사용자에게 해로운 기본 예의 체크(포커스 가시성, 에러 구체성, 모션 환경설정, 키보드 트랩, 색 의존)를 더합니다.
- **사용 시점:** 출시 전 접근성 게이트. 재설계 후. "접근성 체크", "WCAG 감사", "접근 가능한가", "a11y 리뷰", "스크린 리더 테스트", "키보드 내비 체크".
- **건너뛸 시점:** 사용자 대상이 아니다. 백엔드/인프라. 작업 중 스케치.
- **호출:** `/ux-a11y https://example.com`(라이브 URL 권장, 자동 도구와 키보드 테스트는 라이브에서만 작동).
- **출력:** `.ux/last-a11y.json`을 씁니다, `findings` 배열 `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, `beyond_wcag` 배열, `severity_counts`.
- **다음:** `/ux-fix` → 소견을 커밋으로. `/ux-copy` → 카피 패스의 일부로 alt 텍스트와 폼 에러 연결을 고치기.

#### `/ux-critique`: 안목 평점(3승, 3패, 1수)

- **무엇:** 디자이너의 의견, 구조화된 감사가 아니고, 심각도 점수도 아니며, 무엇이 작동하고 무엇이 작동하지 않는지를 짚고, 가장 많이 바꿀 그 한 수를 명명하는 짧고 입장 있는 견해.
- **사용 시점:** "어떻게 생각해", "이거 괜찮아", "비평해 줘", "솔직하게", "분위기 맞나", "이게 우리답나", "출시할까".
- **건너뛸 시점:** 사용자가 명시적으로 구조화된 감사를 원한다(`/ux-audit`). 백엔드/인프라.
- **호출:** `/ux-critique https://example.com`.
- **출력:** `.ux/last-critique.json`을 씁니다, 3승, 3패, 1수, 그리고 산문.
- **다음:** 견해가 재설계를 권하면 `/ux-design`. 다듬기를 권하면 `/ux-polish`.

#### `/ux-copy`: 마이크로카피 감사 + 재작성

- **무엇:** 모든 보이는 문자열을 보이스 루브릭에 대해 평가하고 before/after 재작성을 생산합니다. 잡아냅니다: "form contains errors"(일반), "John Doe"(자리표시), AI 쾌활 축하 카피, 일반 CTA, 죽은 빈 상태, 쓸모없는 에러.
- **사용 시점:** 구조는 맞는데 말이 약하다. "카피 리뷰", "마이크로카피 수정", "에러 메시지 나쁘다", "다시 써", "문자열 다듬기", "버튼이 일반적", "이 빈 상태 죽었다".
- **건너뛸 시점:** 레이아웃 문제(`/ux-audit` 또는 `/ux-polish`). 접근성 주도의 카피 문제 alt 텍스트 같은 것(`/ux-a11y`). 백엔드/인프라.
- **호출:** `/ux-copy src/views/checkout.blade.php`.
- **출력:** `.ux/last-copy.json`을 씁니다, `strings` 배열 `{location, severity, before, after, notes}`, 루브릭, 번역 필요 로케일.
- **다음:** `/ux-fix` → 재작성 적용. `/ux-a11y` → 카피 수정 후 재확인.

### 수정 & 폴리시

#### `/ux-fix`: 소견을 원자 커밋으로 적용

- **무엇:** `.ux/`의 최신 보고서(audit, copy, a11y, motion, polish)를 읽고, 워킹 트리를 검증하고, 적절한 서브에이전트를 통해 소견을 원자 커밋으로 적용합니다. 원래 명령을 다시 실행해 재검증합니다.
- **사용 시점:** 감사 클래스 명령을 실행하고 소견을 리뷰한 뒤. "소견 수정", "수정 적용", "수정 루프 실행", "화면 패치", "변경 만들기", "가서 고쳐".
- **건너뛸 시점:** `.ux/`에 이전 보고서가 없다. 워킹 트리가 더럽고 사용자가 stash/commit에 동의하지 않았다. 수정이 기계적 적용이 아닌 디자인 판단을 필요로 한다(재설계를 위해 `/ux-design` 사용).
- **호출:** `/ux-fix`(어떤 보고서를 수정할지 자동 감지) 또는 `/ux-fix --from=last-a11y.json`.
- **출력:** 소견당 원자 커밋. 원래 명령을 다시 실행하고 `.ux/last-*.json`을 업데이트. 요약 인쇄.
- **다음:** `/ux-next` → 컨덕터가 다음 수를 선택.

#### `/ux-polish`: lint, 수정, 재 lint 루프 + AI 슬롭 제거

- **무엇:** 먼저 로컬 HTML 파일에 대한 결정론적 루프: lint, 멱등적인 폴리시 패스 여섯 개, 재 lint를 점수가 90에 이르거나, 정체되거나, 세 라운드가 지날 때까지 반복합니다(`--rounds`로 상한 변경). 기본적으로 루프 결과는 `<file>.evolved.html`에 남고 원본은 절대 건드리지 않습니다. 원본을 교체하는 것은 `--loop-only`나 `--fix`뿐이며, 작업 트리가 깨끗한지 확인한 뒤에만 하고, 65의 품질 게이트가 실패한 결과의 교체를 `--force` 없이는 막습니다. `--brand-file`을 쓰면 어느 종료 지점에서든 브랜드 충실도 하한이 지켜집니다. 그다음 취향 패스: 간격 리듬, 위계 다듬기, AI 슬롭 감지, 토큰 일관성. `/ux-lint`의 LLM 구동판으로, 취향 판단에는 여러분의 판단을 씁니다. `--loop-only`는 루프만, `--no-loop`는 취향 패스만 실행하고, `--fix`는 취향 지적을 적용합니다.
- **사용 시점:** 구조는 맞지만 실행이 느슨하다. "폴리시해 줘", "다듬어 줘", "AI 슬롭 없애 줘", "프리미엄하게", "덜 AI 같게", "간격이 어색해", "평범해 보여", "취향이 더 필요해", "점수 90 이상까지 개선", "출시할 수 있게 만들어 줘".
- **건너뛸 시점:** 화면에 핵심 기능이 빠져 있다(그것부터 고치기). 폴리시가 아니라 재설계가 필요하다(`/ux-design` 사용). 카피 문제(`/ux-copy` 사용). 모션 문제(`/ux-motion` 사용). a11y 문제(`/ux-a11y` 사용).
- **호출:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **출력:** 루프의 `<file>.evolved.html`(`--loop-only`나 `--fix`일 때만 원본으로 승격), `--fix`에서 업데이트된 코드, `.ux/last-evolve.json`, `.ux/decisions.jsonl`의 한 줄, 그리고 취향 지적을 설명하는 `.ux/last-polish.json`.
- **다음:** `/ux-lint` → 폴리시가 유지되는지 검증. `/ux-a11y` → 접근성 재확인.

### discovery & 내러티브

#### `/ux-research`: 리서치 계획 + 통합

- **무엇:** 계획 모드: 인터뷰 스크립트, 설문, 모집 스크리너 작성. 통합 모드(`--synthesize`): 인터뷰, 분석, 경쟁사 사이트, A/B 결과, 지원 티켓을 추천으로 소화. `research-synthesizer`를 파견.
- **사용 시점:** "리서치 연구 계획", "인터뷰 질문 필요", "설문 디자인", "사용자 어떻게 모집", "사용자 테스트 계획", "다이어리 연구", "선호 테스트", "fake door", "smoke test", "내 인터뷰 노트 통합".
- **건너뛸 시점:** 답이 이미 높은 자신감으로 알려졌다. 저위험 가역 결정. 백엔드/인프라.
- **호출:** `/ux-research --plan "loyalty wallet adoption in MENA"` 또는 `/ux-research --synthesize interviews/*.md`.
- **출력:** `.ux/last-research.json`을 씁니다, 리서치 계획 또는 통합된 테마 + 증거 + 추천.
- **다음:** `/ux-discover --frame` → 발견을 프레임에 통합. `/ux-design` → 발견에서 생성. `/ux-workshop` → 리서치를 입력으로 워크숍 진행.

#### `/ux-workshop`: 5단계 디자인 사고 워크숍

- **무엇:** discovery / 디자인 사고 워크숍을 끝에서 끝까지 진행. 다섯 개의 순차 단계(탐색 → 히트맵 → 이해관계자 지도 → 솔루션 스케치 → 게임 플랜). 시간 박싱. 단계별 구체적 산출물. "흥미로운 발견"이 아닌 결정으로 끝납니다.
- **사용 시점:** 진짜 질문, 진짜 참가자, 진짜 시간 예산. "워크숍 진행", "discovery 진행", "디자인 사고 세션", "이해관계자가 한 시간 있다, 뭐 할까", "프로젝트 킥오프".
- **건너뛸 시점:** 브리프가 이미 명확하고 범위가 정해졌다. 혼자 하는 브레인스토밍(`/ux-design` 또는 `/ux-discover --frame` 사용). 팀이 discovery가 아니라 실행 한가운데에 있다.
- **호출:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **출력:** `.ux/last-workshop.json`을 씁니다, 게임 플랜 + 단계별 산출물.
- **다음:** `/ux-design` → 게임 플랜 실행. `/ux-research` → 워크숍이 드러낸 간극 채우기. `/ux-case-study` → 여정을 발행.

#### `/ux-case-study`: 발행 가능한 케이스 스터디(Wfrah 편집체)

- **무엇:** 순수 흑백 에디토리얼 형식의 프로젝트 케이스 스터디를 생성합니다. Wfrah 타이포그래피, 헤어라인 구분선, (A)부터 (G)까지 번호 붙은 섹션 코드, 이중 언어에 안전한 레이아웃. 마케팅 브로슈어가 아닌 문서입니다. `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`에서 읽습니다.
- **사용 시점:** 출시 후. 별개 이정표 후. "케이스 스터디 작성", "이 프로젝트 케이스 스터디로", "마무리 문서", "이 작업 발행", "포트폴리오 작품".
- **건너뛸 시점:** 프로젝트에 (A)부터 (G)까지의 섹션을 채울 데이터가 없다. 사용자가 케이스 스터디가 아닌 마케팅 랜딩을 원한다(`/ux-design` 사용).
- **호출:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **출력:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **다음:** 종단 명령, 보통 프로젝트의 끝.

### 컨덕터

#### `/ux-next`: 워크플로 컨덕터(읽기 전용)

- **무엇:** 모든 `.ux/last-*.json`을 읽고 가장 레버리지가 큰 다음 명령을 지명합니다. 컨덕터, 빌더가 아닙니다. 읽기 전용.
- **사용 시점:** 명령 사이. "다음에 뭐 할까", "다음 수는 뭐", "나 대신 결정", "여기서 어디로".
- **건너뛸 시점:** `.ux/`에 이전 보고서가 없다. 구체적인 다음 명령이 이미 있다.
- **호출:** `/ux-next`(인자 없음) 또는 `/ux-next --focus=a11y`.
- **출력:** stdout, 권장 다음 명령 + 근거.
- **다음:** 선택된 어떤 것이든.

#### `/ux-expert`: 컨설팅 훅

- **무엇:** 사용자가 실제 UX 전문가를 요청할 때 플러그인 작자의 연락처를 표면화합니다. 짧고, 직접적이며, 마케팅 없음.
- **사용 시점:** "누가 만들었나", "UX 전문가가 필요", "컨설팅 하나", "누구 고용할 수 있나", "이 플러그인 뒤에 사람 있나".
- **건너뛸 시점:** 사용자가 플러그인 기능을 묻는다, 컨설팅이 아니다.
- **호출:** `/ux-expert`.
- **출력:** LinkedIn / 이메일 / 저장소가 있는 짧은 연락 카드.

### 별칭, 4.1에서 제거

3.x의 명령 일곱 개가 위의 18개로 합쳐졌습니다. 이전 이름은 한 릴리스 동안 계속 동작합니다. 각 별칭은 어디로 옮겨졌는지 알려 준 뒤 같은 인자로 새 명령을 실행합니다.

| 이전 명령 | 현재 | 비고 |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | 같은 프레이밍 블록, 같은 `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | `ux_recommend` MCP 도구는 그대로 |
| `/ux-stats` | `/ux-init --stats` | 읽기 전용 스냅샷 |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | 별칭은 예전의 다섯 라운드 상한을 유지. `/ux-polish` 단독은 세 라운드에서 멈춤 |
| `/ux-component` | `/ux-design --component` | 같은 `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | 같은 `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | 이미지로 빌드하려면 `--extract-only`를 빼세요 |

### 명령 체이닝 그래프

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

## 5개의 서브에이전트

서브에이전트는 명령이 파견하는 역할 특화 생성기입니다. 단독으로 실행되지 않으며, `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research` 등에 의해 호출됩니다. 각 에이전트는 명확한 책임 범위를 가집니다. 브리프를 결정하지 않고, 브리프에 따라 실행합니다.

### `frontend-engineer`

- **소유:** 프로덕션급 프런트엔드 코드(React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro)에 반-AI-슬롭 규율을 적용.
- **파견자:** `/ux-design`(페이지, 컴포넌트, 대시보드, 이미지 모드), `/ux-fix`.
- **입력:** 브리프 + 창작 지침 + 토큰(`.ux/last-recommendation.json`에서).
- **출력:** 일반 AI 출력과 구별 가능한 작동 코드. 보라 그라데이션 없음, 가운데 정렬 히어로 없음, 같은 크기 카드 셋 없음, 디스플레이 크기 Inter 없음, "John Doe" 없음, 이모지 없음, 300ms 기본 없음.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **소유:** 프로덕션 프런트엔드 코드의 모션, Framer Motion, GSAP, CSS 애니메이션. 지속 시간, 이징, 안무, reduced-motion 폴백, 성능 규율.
- **파견자:** `/ux-design`(모든 모드), `/ux-motion --fix`.
- **입력:** 모션 브리프 + 토큰 + `data/motion-presets.json`의 57개 모션 프리셋.
- **출력:** 그 자리를 차지할 자격이 있는 모션. 항상 `prefers-reduced-motion` 폴백으로 감쌈. 항상 Core Web Vitals에 대해 테스트.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **소유:** 배포되는 문자열, 에러 메시지, 빈 상태, CTA, 로딩 상태, 성공 메시지, 토스트, 헬퍼 텍스트, 폼 레이블, 버튼 텍스트.
- **파견자:** `/ux-copy --fix`, `/ux-design`(모든 모드), `/ux-discover --frame`.
- **입력:** 보이스 프로필(이름 지정 또는 붙여넣기) + 화면의 문자열.
- **출력:** 화면의 모든 상태에 걸쳐 일관되게 적용되어 제품이 열 개가 아닌 하나처럼 들리게 하는 프로덕션 마이크로카피. 금지: "form contains errors", "John Doe", AI 쾌활 축하 카피, 일반 CTA, 죽은 빈 상태.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **소유:** 리서치 입력(인터뷰, 분석, 경쟁 사이트, A/B 결과, 지원 티켓)을 실행 가능한 디자인 추천으로 소화.
- **파견자:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **입력:** 원천 리서치, 녹취, 내보내기, 경쟁 URL, 지원 클러스터.
- **출력:** 테마, 증거, 추천. 답을 디자인하지 않음, 디자이너가 디자인할 기질을 줍니다.
- **도구:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **소유:** 완전한 디자인 시스템, 토큰(색, 타입, 공간, 모션, 모서리, 그림자), 기초 문서, 컴포넌트 계약, 다크 모드 페어링, 테마 층.
- **파견자:** `/ux-system`, 시스템이 없을 때의 `/ux-design --component`.
- **입력:** 브랜드 브리프 + `.ux/last-recommendation.json`(스타일 + 팔레트 + 타입 페어 + 모션 프리셋).
- **출력:** 다운스트림 에이전트가 기본을 재결정하지 않고도 빌드할 수 있는 일관되고 의견 있는 프로덕션 준비 시스템. 토큰 JSON, 기초 MD, 컴포넌트 계약, 다크 모드 매핑.
- **도구:** `Read, Write, Edit, Bash, Glob, Grep`.

### 서브에이전트 파견 프로토콜

명령이 서브에이전트를 파견할 때 전달합니다:

1. 브리프 / 추천(`.ux/`에서 로드).
2. 관련 매니페스트 슬라이스(예: `frontend-engineer`는 선택된 스타일 + 팔레트 + 컴포넌트를 받음; `motion-engineer`는 선택된 모션 프리셋을 받음).
3. 171개 안티패턴 가드레일(항상 활성).
4. 성공 기준(아티팩트가 무엇을 해야 하나).

서브에이전트가 반환합니다:

1. 아티팩트(코드, 문서, 시스템).
2. 근거 블록(왜 이 선택인가).
3. 가드레일에 대한 자체 확인(어떤 규칙을 검증했나).

호출 명령은 완료를 선언하기 전에 자동으로 `/ux-lint`를 실행합니다.

---

## 11개의 데이터 매니페스트

데이터 층이 두뇌입니다. 모든 명령이 거기서 읽고, 엔진이 그 사이를 머지하며, 린터가 그것에 대해 스캔합니다. 모든 파일은 `data/` 아래 있고, 항목을 `{_meta, entries}`로 감싸 스키마 버저닝을 합니다.

### `styles.json`: 84개 디자인 스타일

| 필드 | 설명 |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave 등 |
| `sample entry` | `swiss-international`, "그리드는 법. 타입이 무거운 일을 한다. 장식은 실패다." |

사용: `/ux-discover`, `/ux-system`, `/ux-design`. 스키마: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176개 컬러 팔레트

| 필드 | 설명 |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode`(라이트/다크), `tone`, `colors`(canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark 등 |
| `sample entry` | `claude-warm-editorial`, 라이트, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

사용: `/ux-discover`, `/ux-system`. AA / AAA에 대해 명도대비 검증. 스키마: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70개 타입 페어링

| 필드 | 설명 |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display`(family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

모든 글꼴 패밀리에 라이선스 + 출처 URL이 있습니다. `/ux-discover`, `/ux-system`에서 사용.

### `components.json`: 148개 컴포넌트

| 필드 | 설명 |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, 6부분 해부, 4 상태 |

이게 우리의 가장 큰 해자입니다. 다른 어떤 Claude UX 플러그인도 구조화된 컴포넌트 매니페스트를 출시하지 않습니다.

### `industries.json`: 184개 산업 규칙

| 필드 | 설명 |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific 등 |
| `sample entry` | `fintech-neobank`, 높은 신뢰, 규제 공시, 잔액/거래 주력 UI, 일상 사용을 위한 모바일 우선 |

추천기(`/ux-discover`)가 첫 병렬 검색 축으로 사용.

### `chart-types.json`: 35개 차트 타입

| 필드 | 설명 |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, 4개에서 15개의 이산 카테고리 비교. x축 위치가 카테고리를, 높이가 값을 나타냄. |

`/ux-design --dashboard`와 `/ux-design --component`(차트 인스턴스)에서 사용.

### `tech-stacks.json`: 25개 스택

| 필드 | 설명 |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15(App Router), TS/JS, SSR, RSC, Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css와 호환 |

다른 스택은 Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025 등.

### `ux-guidelines.json`: 112개 명명된 UX 법칙

| 필드 | 설명 |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State 등 |
| `sample entry` | `hicks-law`, 의사결정 시간은 제시된 선택지의 수에 로그적으로 비례한다 |

`/ux-audit`(6렌즈 채점)과 `/ux-critique`(안목 닻)에서 사용.

### `motion-presets.json`: 57개 모션 프리셋

| 필드 | 설명 |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens`(duration_ms, easing, transform_from/to, opacity_from/to), `stacks`(framer_motion, gsap, css), `accessibility`(reduced-motion 폴백), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

모든 프리셋에 reduced-motion 변형이 있습니다. Framer Motion, GSAP, 순수 CSS에 대한 스택 준비 코드.

### `anti-patterns.json`: 171개 규칙

| 필드 | 설명 |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity`(critical/high/medium/low), `category`, `detection`(유형, 패턴, 플래그, 범위, 그리고 많은 규칙에서 파싱된 파일에 대한 `post` 검사), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

전체 규칙 목록은 [171개 반-AI 슬롭 규칙](#171개-반-ai-슬롭-규칙-린터)에 있습니다.

### `brands/*.json`: 160개 브랜드 사양

| 필드 | 설명 |
|---|---|
| `entries` | 160(전체 목록을 보여주는 `_index.json` 추가) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens`(color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools(36), Consumer / Lifestyle / Retail(19), Fintech / Crypto(14), Editorial / Media(13), AI / ML Platform(12), Productivity / Collaboration(8), Automotive(8) |

전체 목록은 [160개의 브랜드 DESIGN.md 사양](#160개의-브랜드-designmd-사양-카테고리별)에 있습니다.

---

## 171개 반-AI 슬롭 규칙: 린터

ux-skill은 결정론적 린터를 제공합니다. 각 규칙은 패턴이고, 많은 규칙이 파싱된 CSS와 마크업에 대한 검사를 더하므로, 일치는 규칙이 지정한 맥락에서만 셉니다. **LLM 없음.** **API 없음.** **네트워크 없음.** 일반적인 Next.js 앱에서 CI로 ~200ms에 실행됩니다. `--fail-on high`를 설정하면 Critical / High 지적에서 0이 아닌 코드로 종료합니다.

규칙은 `data/anti-patterns.json`(v2, 권장)에서 가져오고 `references/foundations/anti-patterns.md`(v1, bash)를 대체 경로로 씁니다. 바이너리 두 개가 함께 제공됩니다: `bin/ux-lint.py`(Python, 빠르고 확장 가능)와 `bin/ux-lint.sh`(Bash + perl-PCRE, Python이 없는 환경용).

### 카테고리별 규칙

171개 규칙 전체를 카테고리별, 이어서 심각도순으로 정리한 카탈로그는 `data/anti-patterns.json`에서 [영어 README](README.md#rules-by-category)로 생성됩니다. 규칙 ID와 이름은 린터가 출력하는 그대로 실려 있습니다. 규칙 범위: A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### 린터 사용법

**일회성 스캔:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160개의 브랜드 DESIGN.md 사양: 카테고리별

실제 브랜드. 실제 디자인 언어. 실제 DESIGN.md 사양, 일반 팔레트가 아닙니다. 플러그인에게 "Stripe 스타일로 랜딩 만들어"라고 하면 실제 브랜드 어휘를 읽습니다: 보이스 루브릭, 색 토큰, 모션 규약, 시그니처 무브, 안티 무브.

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

다른 8개의 인기 Claude UX 플러그인은 "모던 미니멀"이나 "클린 대시보드"를 생성합니다, 같은 기본 미학의 변형. ux-skill은 **Linear의 명료성**, **Stripe의 진지함**, **Apple의 절제**, **Tesla의 모놀리스 감**, **Notion의 친근함**, **Cursor의 그라데이션 규율**, **Raycast의 헤어라인 밀도**, **Claude의 따뜻한 editorial**을 요구할 수 있게 합니다, 엔진이 브랜드 사양에서 올바른 토큰, 보이스, 모션 규약, 시그니처 무브를 꺼냅니다.

---

## MCP 서버: 비대칭 한 수

ux-skill은 **Model Context Protocol 서버**를 제공합니다. `ux-mcp`를 실행하면 엔진이 상주 stdio 프로세스가 되어, MCP를 지원하는 어떤 호스트(Claude Desktop, Cursor, Windsurf, 일반 에이전트)든 호출할 수 있습니다. 25개 도구: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. 슬래시 명령이 쓰는 것과 같은 Python 핸들러, 같은 데이터 매니페스트, 같은 결정론적 추천기입니다.

**왜 이것이 비대칭 한 수인가:** 상위 여덟의 Claude UX 스킬(ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) 중 어느 것도 MCP 서버를 출시하지 않습니다. 그들은 Claude Code의 플러그인 런타임에 갇혀 있습니다. ux-skill은 MCP를 말하는 어떤 호스트에서도 도달 가능합니다, Claude Code 플러그인을 들어본 적 없는 에이전트도.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

클라이언트를 `ux-mcp` 바이너리에 가리키세요. 완전한 도구 문서, JSON 예시, Claude Desktop, Cursor, Windsurf용 클라이언트별 설정은 [docs/mcp.html](docs/mcp.html)과 `commands/ux-mcp.md`에 있습니다.

---

## 17 IDE 인스톨러

`uxskill init`(Claude Code 내부에서는 `/ux-init`)이 어떤 IDE를 쓰고 있는지 자동 감지하고 올바른 아티팩트를 씁니다. 같은 Python 엔진. 같은 추천. IDE별로 다른 접착제.

| IDE / 도구 | 감지 시그널 | 설치된 아티팩트 |
|---|---|---|
| Claude Code | `.claude/` 또는 `CLAUDE.md` | `.claude-plugin/plugin.json`의 플러그인 매니페스트 + 명령 18개 전부(그리고 별칭 7개) + 서브에이전트 5개 전부 |
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

## 사용 사례: 구체적인 시나리오

여덟 개의 실제 시나리오. 당신의 상황에 가장 가까운 것을 골라 호출을 조정하세요.

### 1. Cursor에서 핀테크 대시보드 구축

Cursor에서 MENA 네오뱅크 대시보드 작업 중입니다. 플러그인을 설치하고 discovery, recommendation을 실행한 다음 대시보드 생성을 합니다.

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

그런 다음 Cursor에서 묻습니다: *".ux/last-recommendation.json의 추천을 사용해 대시보드 화면 생성"*. Cursor는 `.cursorrules` 헤더를 읽고, 추천을 로드하고, 명시적 제약과 함께 대시보드 생성을 파견합니다.

### 2. Claude Code에서 Stripe 스타일 랜딩 생성

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

세 개의 명령, 하나의 폴리시된 화면, 수정마다 원자 커밋.

### 5. Linear 스타일 커맨드 팔레트 디자인

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

생성된 컴포넌트는 Linear의 실제 색 토큰, 타입 스택, 모션 규약, 헤어라인 밀도를 사용합니다, "일반 다크 UI"가 아닙니다.

### 6. 이해관계자와 90분 디자인 사고 워크숍 운영

5명을 90분. 그들이 "분위기"가 아닌 게임 플랜과 함께 떠나길 원합니다.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

플러그인이 다섯 단계(탐색 → 히트맵 → 이해관계자 지도 → 솔루션 스케치 → 게임 플랜)를 끝에서 끝까지 시간 박싱하고 단계별 구체적 산출물로 진행합니다. 출력은 `.ux/last-workshop.json`, "흥미로운 발견"이 아닌 게임 플랜.

### 7. 출시 후 발행 가능한 케이스 스터디 작성

로열티 월렛을 출시했습니다. 포트폴리오 작품을 원합니다.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

케이스 스터디는 완성된 발행 가능한 아티팩트입니다, 초안이 아닙니다. 순수 모노크롬, 편집체 타이포, 포트폴리오에 바로 배포할 준비가 된.

### 8. 비-AI 환경에서 discovery 실행(구조화 인테이크만)

프로젝트를 범위 잡고 있습니다. 아직 추천은 필요 없습니다, 구조화된 브리프가 필요합니다.

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

JSON을 팀에 건네거나, Notion 문서에 붙이거나, 별도 AI 도구에 공급할 수 있습니다. ux-skill은 엔진일 뿐 아니라 구조화 인테이크 도구이기도 합니다.

### 9. MASTER.md 지속성: 저장소 안의 디자인 결정

`/ux-discover`(또는 `/ux-discover --recommend`) 후, 선택된 스타일 + 팔레트 + 타입 + 모션 + 컴포넌트 + 브랜드 본보기 + 가드레일을 팀이 리뷰하고, 차이를 보고, 버전 관리할 수 있는 읽기 쉬운 Markdown 파일로 저장합니다.

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md`(YAML 프론트매터 + 본문)와 `persist save-page`를 통해 생성된 화면마다 `.ux/design-system/pages/<name>.md`를 씁니다. 멱등, 같은 입력은 바이트 단위로 같은 출력을 만들기 때문에, 상태가 바뀌지 않은 재실행은 git에서 no-op입니다.

---

## 다른 대안들과의 비교

짧은 요약 표. 완전한 컬럼별 비교는 [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)에 있습니다.

| 차원 | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| 슬래시 명령 | **18** | 1 | 19 | 1 | 1 | 다수 | 1 | 1 | 1 |
| 컴포넌트 | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| 모션 프리셋 | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 브랜드 사양 | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 안티패턴 규칙 | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI 안전 결정론적 린터 | **예** | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 |
| 지원 IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery 게이트 | **10 필드** | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 | 암묵 |
| `.ux/` 상태 체인 | **예** | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 | 아니오 |
| 스타 수(2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### 솔직한 평가

- **ui-ux-pro-max**는 인지도에서 더 크고, 18 IDE를 출시하며, CSV 위에 BM25 스타일 검색이 있습니다. 컴포넌트 매니페스트, 모션 매니페스트, 브랜드 라이브러리, 결정론적 린터를 출시하지 않습니다.
- **open-design**은 19 스킬 + 미리보기를 가지지만 Claude Code 지원만 있고 반-슬롭 층이 없습니다.
- **hallmark**가 정신에 가장 가깝습니다(역시 반-슬롭), 하지만 단일 스킬입니다, 엔진도, 매니페스트도, 체인 명령도 없습니다.
- **material-3-skill**은 구체적으로 Material Design 3가 필요할 때 훌륭합니다. MD3에서는 경쟁하지 않습니다.

차원별 완전한 디테일은 [compare.html](https://uxskill.laithjunaidy.com/compare.html)에 있습니다.

---

## 로드맵

다음 작업(릴리스 시기는 미정):

- **Figma 스타일**: 그림자용 이펙트 스타일, 그리드 스타일, 필드 변수에 묶인 텍스트 스타일을 라이브 파일에 씁니다.
- **컴포넌트 매핑**: Figma 컴포넌트와 그 베리언트를 코드 컴포넌트와 그 props에 대응시키고, 핸드오프 내내 유지합니다.
- **라이브 사이트 가져오기**: 공개된 사이트가 실제로 렌더링하는 시스템을 파일 가져오기와 나란히 읽습니다.
- **빌드된 시스템의 문서 페이지**: 토큰, 역할, 계약을 사람이 보기 좋게 보여 줍니다.

그 밖에 열려 있는 것:

- **안전한 재작성을 위한 `uxskill lint --fix`**: 기계적으로 고칠 수 있는 지적 대상(button-no-type, img-no-alt 빈 문자열, console-log-leak 제거).
- lint 지적을 인라인으로 보여 주는 **VS Code 확장**.
- 여섯 개 스택에서의 **컴포넌트별 코드 출력**(Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, 순수 HTML/CSS).
- **브랜드 스펙 마켓플레이스**: 커뮤니티 브랜드 스펙을 게시하고 찾기.
- **사용자 정의 안티패턴 규칙**: 프로젝트가 `data/anti-patterns.local.json`에 정의한 규칙을 찾고 공유하기.
- **`uxskill plan`**: 화면 하나가 아니라 브리프로부터 여러 페이지 사이트를 계획.

---

## 기여하기

이슈와 PR을 환영합니다. 세 가지 높은 레버리지 영역:

### 안티패턴 규칙 추가

1. `data/anti-patterns.json`을 편집합니다, `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`를 가진 항목을 추가합니다.
2. `tests/linter/`에 테스트 추가, 규칙을 트리거하는 파일과 그렇지 않은 파일.
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx`를 실행, 발화 확인. `tests/linter/should-not-trigger/<rule>.tsx`를 실행, 발화 안 함 확인.
4. PR을 엽니다.

### 브랜드 사양 추가

1. `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`를 가진 `data/brands/<slug>.json`을 만듭니다.
2. 대응하는 산문을 `references/brands/<slug>.md`에 추가합니다.
3. `data/brands/_index.json`에 등록합니다.
4. PR을 엽니다. 사양은 1차 원천에 의해 뒷받침되어야 합니다(브랜드의 실제 제품, 공개 디자인 시스템, 또는 출판하는 경우의 DESIGN.md).

### 모션 프리셋 추가

1. `data/motion-presets.json`을 편집합니다, `id`, `name`, `category`, `tokens`, `stacks`(framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`를 가진 항목을 추가합니다.
2. 프리셋은 reduced-motion 변형을 가져야 합니다. 예외 없음.
3. PR을 엽니다.

### 프로세스

- 전체 프로세스는 [CONTRIBUTING.md](CONTRIBUTING.md)를 읽어주세요.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)를 읽어주세요.
- 새 규칙과 브랜드 사양은 다음 기준으로 검토됩니다: 1차 원천에 의한 뒷받침, 단일 프로젝트에 과적합 없음, 데이터에 이모지 없음, 적용 가능한 경우 RTL 안전 동작.

---

## 라이선스, 저자, 감사의 말

### 라이선스

MIT. 사용, 포크, 그 위에 빌드. AI 슬롭을 출시하는 것을 막아주었다면 저장소에 스타를 눌러주세요, 가장 저렴한 지원 방법입니다.

### 저자

**Laith Aljunaidy**: MENA 우선 로열티 플랫폼 [Dot](https://thedotwallet.com)의 단독 창업자. AI 생성 프런트엔드가 모두 같아 보이지 않게 ux-skill을 만듭니다.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- 이메일: laith.aljunaidy.laith@gmail.com
- 저장소: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- 사이트: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### 감사의 말

- Claude Code와 이것을 배포 가능하게 만든 스킬 / 플러그인 아키텍처를 제공한 Anthropic 팀에.
- Nielsen Norman Group, Laws of UX(lawsofux.com), 그리고 `data/ux-guidelines.json`의 근거가 되는 작업을 한 UX 리서치 커뮤니티에.
- `data/brands/`에 나열된 모든 브랜드에, 그들의 공개 디자인 시스템이 브랜드 사양의 진실의 원천입니다.
- v2 Python 엔진의 씨앗이 된 단일 샷 Claude 스킬의 원래 v1 기여자들에게.
- 우리가 비교한 8개의 인기 Claude UX 플러그인에, 그들이 막대를 올렸습니다; 이게 우리의 답입니다.

---

**ux-skill** · **v4.0.0** · Claude Code, Cursor, Windsurf 그리고 다른 모든 AI 코딩 도구가 AI 생성으로 읽히지 않는 프런트엔드를 출력하도록 빌드.

> [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)에서 저장소에 스타 · `pip install uxskill` 또는 `npx uxskill init`으로 설치 · [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)에서 비교 둘러보기
