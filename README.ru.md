[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · **Русский** · [Türkçe](README.tr.md)

# ux-skill — движок design intelligence для Claude Code, Cursor и любого другого AI-инструмента для кодинга

> **Сильнейший UX-плагин для AI-кодинга.** Ядро рассуждений на Python с 11 запрашиваемыми JSON-манифестами (84 стиля, 176 палитр, 70 типографических пар, 148 компонентов, 184 индустрии, 35 типов графиков, 57 motion-пресетов, 112 UX-законов, 100 правил анти-паттернов, 25 техстеков, 110 brand-спеков), 22 slash-команды, 5 саб-агентов и детерминированный linter против AI-slop. Кросс-IDE: разворачивается в Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer и Roo Cline.

> **Имя бренда — `ux-skill`.** Имя пакета на PyPI / npm остаётся `uxskill`. Репозиторий GitHub живёт по адресу [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Сайт:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Сравнение со всеми UX-плагинами Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-2.0.0--alpha.1-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#установщик-для-17-ide)
[![Brands](https://img.shields.io/badge/brand_specs-110-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-100-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### История звёзд

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Что такое ux-skill

ux-skill — это **движок design intelligence** для AI-инструментов кодинга. Он работает как пакет Python (`pip install uxskill`), как плагин для Claude Code и как мультиустановщик для 17 IDE. Движок принимает бриф проекта (индустрия, аудитория, тон, must-have, запрещённые ходы, стек, регион) и возвращает полную рекомендованную design-систему: стиль, палитру, типографическую пару, motion-пресеты, компоненты, образцовые бренды для изучения и guardrails анти-паттернов, которые надо удержать. Рекомендация детерминированная — одинаковый вход всегда даёт одинаковый выход.

Плагин стоит между тобой и AI-инструментом кодинга. Когда ты просишь Claude Code, Cursor или любого другого AI-ассистента «собрать fintech-лендинг», ассистент обычно импровизирует — и результат читается как AI-сгенерированный за пять секунд (фиолетово-синие градиенты, три одинаковые карточки, Inter в размере display, «John Doe» в отзывах, переходы по умолчанию 300мс, центрированный hero, прыгающие стрелки на CTA). ux-skill заменяет импровизацию **структурными ограничениями**: ты запускаешь `/ux-discover`, чтобы захватить бриф, `/ux-recommend`, чтобы выбрать систему, `/ux-design`, чтобы сгенерировать код, и `/ux-lint`, чтобы проверить, что он проходит 100 детерминированных правил против AI-slop перед коммитом.

Этот README — каноническая справка. Каждая команда, каждый саб-агент, каждый data-манифест, каждый путь установки, каждый brand-спек, каждая категория анти-паттернов — всё задокументировано здесь. Если ты ищешь design-плагин для Claude Code или сравниваешь AI-инструменты дизайна для Cursor, Windsurf или Codex, прочитай это от начала до конца параллельно с [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Содержание

1. [Быстрая установка](#быстрая-установка)
2. [Цифры — live-сравнение с топ-8 UX-скилами Claude](#цифры--live-сравнение-с-топ-8-ux-скилами-claude)
3. [Архитектура — как складываются части](#архитектура--как-складываются-части)
4. [22 slash-команды — детальная справка](#22-slash-команды--детальная-справка)
5. [5 саб-агентов](#5-саб-агентов)
6. [11 data-манифестов](#11-data-манифестов)
7. [100 правил против AI-slop — linter](#100-правил-против-ai-slop--linter)
8. [110 brand-спеков DESIGN.md — по категориям](#110-brand-спеков-designmd--по-категориям)
9. [MCP-сервер — асимметричный ход](#mcp-сервер--асимметричный-ход)
10. [Установщик для 17 IDE](#установщик-для-17-ide)
11. [Сценарии использования — конкретные кейсы](#сценарии-использования--конкретные-кейсы)
12. [Сравнение с альтернативами](#сравнение-с-альтернативами)
13. [Roadmap](#roadmap)
14. [Как контрибьютить](#как-контрибьютить)
15. [Лицензия, автор, благодарности](#лицензия-автор-благодарности)

---

## Быстрая установка

Три пути установки. Выбирай тот, что подходит твоей среде.

### Путь 1 — marketplace Claude Code (канонический)

Если ты живёшь в Claude Code, ставь через marketplace плагинов:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Это подключает все 22 slash-команды и 5 саб-агентов к твоей сессии Claude Code. После установки запусти `/ux-init`, чтобы настроить директорию состояния `.ux/` для проекта и проверить, что Python-движок доступен.

### Путь 2 — pip (универсальный)

Если ты живёшь вне Claude Code (Cursor, Windsurf, CLI, CI), ставь Python-пакет:

```bash
pip install uxskill
uxskill init                       # автоопределяет твою IDE, ставит правильный артефакт
uxskill stats                      # печатает счётчики манифестов, чтобы проверить установку
uxskill lint .                     # запускает linter в текущей директории
```

Пакет выставляет и `ux`, и `uxskill` как CLI-entry-point — это один и тот же бинарь.

### Путь 3 — npx (без Python)

Если не хочешь управлять Python напрямую, npx-обёртка бутстрапит всё через `pipx`:

```bash
npx uxskill init                  # скачивает pipx + uxskill при первом запуске
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Проверка установки

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

Если какой-то счётчик возвращает 0, JSON-файл отсутствует — открой issue на [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Цифры — live-сравнение с топ-8 UX-скилами Claude

Количество звёзд в последний раз сверено через `gh api` **2026-05-28**. ux-skill (Laith0003/ux-skill) — новичок: мы маленькие по узнаваемости, глубокие по архитектуре. Сравнение ниже честное: где проигрываем, где выигрываем.

| Плагин | Звёзды | Архитектура | Slash-команды | Linter (CI-safe) | Brand-спеки | Компоненты | Motion-пресеты | Поддерживаемые IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83 958** | Python BM25 + CSV, одиночный skill | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54 406** | Node.js + 19 скилов + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25 202** | Bash + taste на исследовательской основе | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15 455** | Один SKILL.md на 62 КБ + скрипты | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5 762** | Библиотека скилов, подключённая через MCP | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2 391** | Skill одной эстетики | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2 164** | Anti-slop design skill | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Компоненты MD3 + аудит | 1 | — | (только MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python-движок + 11 манифестов + 22 команды + 5 саб-агентов + CI-linter** | **22** | **100 regex-правил** | **110** | **148** | **57** | **17** |

### Где мы проигрываем

- **Узнаваемость.** У них сотни тысяч звёзд. У нас 14. Поставь звезду — это самый дешёвый способ помочь.
- **Узнаваемость бренда.** У ui-ux-pro-max и open-design фора, измеряемая месяцами, а не днями.
- **Marketing-полировка.** У них есть скриншоты, демо-видео и findable-лендинг. У нас обстоятельный README и тощий лендинг.

### Где мы выигрываем

- **Библиотека компонентов:** 148 задокументированных компонентов с анатомией, состояниями, использованными токенами и motion-спецификациями. Никто из остальных 8 не поставляет манифест компонентов.
- **Motion-пресеты:** 57 stack-ready записей (Framer Motion, GSAP, CSS) с reduced-motion-фолбэками. Никто из остальных не поставляет motion-манифест.
- **Anti-pattern linter:** 100 детерминированных regex-правил, работает в CI, выходит с non-zero на Critical/High. Никто из остальных не поставляет детерминированный linter.
- **Brand-спеки:** 110 реальных DESIGN.md-спеков (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude и ещё 96). Никто из остальных не поставляет brand-библиотеку.
- **17 поддерживаемых IDE:** один и тот же движок, разный клей для каждой IDE.
- **22 slash-команды:** discovery, генерация, audit, lint, polish, fix loop, case-study, workshop, copy, motion, a11y, dashboard, conductor — полностью интегрированы.

Полный stable-by-table side-by-side на [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Архитектура — как складываются части

```
ux-skill (имя пакета: uxskill)
│
├── data/                              Мозг — запрашиваемые JSON-манифесты
│   ├── styles.json                    84 design-стиля + when/skip + токены
│   ├── palettes.json                  176 палитр (light/dark, контраст проверен)
│   ├── type-pairs.json                70 троек display × body × mono
│   ├── components.json                148 компонентов (анатомия, состояния, motion)
│   ├── industries.json                184 правила индустрий + сигналы аудитории
│   ├── chart-types.json               35 типов графиков (when/skip, encoding)
│   ├── tech-stacks.json               25 стеков (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 именованных UX-законов (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 motion-пресетов (entry, exit, hover...)
│   ├── anti-patterns.json             100 regex-правил (источник CI-safe linter)
│   └── brands/*.json                  110 brand DESIGN-спеков + _index.json
│
├── engine/                            Python — рассуждения
│   ├── recommender/                   движок merge с 5 параллельными поисками
│   ├── linter/                        детерминированный анти-slop сканер
│   ├── discovery/                     протокол принуждения на 10 полей
│   ├── generator/                     эмиттер токенов + манифеста
│   ├── installer/                     мультиустановщик для 17 IDE
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          22 slash-команды Claude Code (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    снимок инвентаря
│   ├── ux-discover.md                 intake на 10 полей (gate)
│   ├── ux-recommend.md                FLAGSHIP — поиск в 5 параллельных
│   ├── ux-lint.md                     детерминированный linter
│   ├── ux-design.md                   генерация frontend-кода
│   ├── ux-component.md                генерация одного компонента
│   ├── ux-system.md                   генерация полной design-системы
│   ├── ux-dashboard.md                генерация dashboard-поверхности
│   ├── ux-motion.md                   motion-обработка + аудит
│   ├── ux-audit.md                    6-линзовый design-аудит
│   ├── ux-a11y.md                     WCAG 2.1 AA аудит
│   ├── ux-critique.md                 taste-критика (3 выигрыша, 3 промаха, 1 ход)
│   ├── ux-copy.md                     ревью + переписывание microcopy
│   ├── ux-fix.md                      применить findings атомарными коммитами
│   ├── ux-polish.md                   косметический проход + убийство AI-slop
│   ├── ux-frame.md                    framing-блок на 4 поля
│   ├── ux-research.md                 планирование исследования + синтез
│   ├── ux-workshop.md                 5-фазный workshop design-thinking
│   ├── ux-case-study.md               публикуемый case study в формате Wfrah-editorial
│   ├── ux-next.md                     дирижёр workflow (read-only)
│   └── ux-expert.md                   крючок для консалтинга
│
├── agents/                            5 саб-агентов (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy в голосе бренда
│   ├── research-synthesizer.md        интервью + аналитика + конкуренты
│   └── design-system-architect.md     токены / компоненты / основания
│
├── references/                        Источник в прозе для данных + демо-страниц
│   ├── foundations/                   anti-patterns.md, принципы, taste
│   ├── laws/                          UX-законы long-form
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        проза по стилю (anti-slop.md и т.д.)
│   ├── components/                    компоненты long-form
│   ├── output/                        рубрики output
│   └── conditional/                   stack-специфичные указания
│
├── bin/
│   ├── uxskill.mjs                    npx-обёртка -> Python-движок
│   ├── ux-lint.py                     linter v2 (предпочтительно)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (создаётся для каждого проекта)
    ├── last-discovery.json            снимок брифа
    ├── last-recommendation.json       выбранная система
    ├── last-frame.json                framing-блок
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Как движок реально работает

1. **Вход.** Ты даёшь бриф — интерактивно через `/ux-discover` (10 полей) или неинтерактивно через флаги в `ux recommend`.
2. **5 параллельных поисков.** Движок параллельно гоняет пять lookup'ов по манифестам:
   - **Индустрия → recommended_styles** (industries.json)
   - **Стиль → совместимость палитры + типа + motion** (styles.json)
   - **Тон × must-have → фильтр палитры** (palettes.json)
   - **Стек → совместимость компонентов + motion-пресетов** (tech-stacks.json, motion-presets.json)
   - **Forbidden + регион → guardrails + шорт-лист brand-образцов** (anti-patterns.json, brands/)
3. **Merge.** Детерминированный merger ранжирует кандидатов, разрешает конфликты (например, must-have dark-mode форсит режим палитры) и выдаёт одну рекомендованную систему.
4. **Выход.** JSON-документ с выбранным стилем, палитрой, типографической парой, топ-5 motion-пресетами, топ-12 компонентами, топ-5 brand-образцами и всеми 100 активными guardrails анти-паттернов. Плюс блок rationale, объясняющий каждый выбор.
5. **Генерация.** Команды ниже по пайплайну (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) потребляют рекомендацию для генерации реального кода через саб-агентов.
6. **Верификация.** `/ux-lint` повторно сканирует сгенерированный код против 100 regex-правил. Выходит с non-zero на Critical/High в CI.

**Python думает. HTML показывает. Markdown связывает в цепочку.**

---

## 22 slash-команды — детальная справка

Каждая команда поставляется как `.md`-файл в `commands/` с `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` и `output state file`. Описания ниже сжаты; полный source — это каноническая спека.

Команды сгруппированы в пять корзин: **bootstrap & инвентарь**, **discovery & рекомендация**, **генерация**, **audit & верификация**, **fix & polish** и **conductor**.

### Bootstrap & инвентарь

#### `/ux-init` — bootstrap проекта

- **Что:** Определяет, какую IDE ты используешь (`.claude/`, `.cursor/`, `.windsurf/`, и т.д.), ставит правильный артефакт, проверяет, что Python-движок доступен, печатает снимок статистики.
- **Когда использовать:** Первая установка в новом проекте. После клонирования проекта, использующего ux-skill. После `pip install --upgrade uxskill`.
- **Когда пропустить:** Уже запускал в этом проекте, и ничего не изменилось.
- **Вызов:** `/ux-init` (без аргументов) или `uxskill init` из CLI.
- **Output:** Артефакт под IDE (см. [Установщик для 17 IDE](#установщик-для-17-ide)) + директория `.ux/` + сводка в stdout.
- **Цепляется к:** `/ux-discover` следующим.

#### `/ux-stats` — печатает инвентарь данных

- **Что:** Печатает версию + счётчики записей по 11 data-манифестам, чтобы ты мог проверить, что установлено.
- **Когда использовать:** После установки. После апгрейда. Когда `/ux-recommend` возвращает неожиданные выборы, и ты подозреваешь, что манифесты неполные.
- **Когда пропустить:** Никогда — это read-only команда на 50мс.
- **Вызов:** `/ux-stats` или `uxskill stats`.
- **Output:** JSON в stdout (см. [Проверка установки](#проверка-установки) выше).
- **Цепляется к:** Только диагностика; не питает дальнейшее.

### Discovery & рекомендация

#### `/ux-discover` — функция принуждения (intake на 10 полей)

- **Что:** Обязательный intake на 10 полей, через который проходит каждый проект перед любой командой генерации. Тип проекта, аудитория, главная цель, тон, must-have, forbidden, brand-референсы, стек, регион, метрика успеха. **Никакой импровизации.** Запрещённые фразы («modern», «clean») заставляют пользователя быть конкретным.
- **Когда использовать:** Перед любым `/ux-design`, `/ux-component`, `/ux-system` или `/ux-dashboard`. Когда предыдущий бриф устарел.
- **Когда пропустить:** Чинишь баг (`/ux-fix`). Только проходишься linter'ом (`/ux-lint`). Бриф не менялся с последней сессии.
- **Вызов:** `/ux-discover`. Плагин спрашивает; ты отвечаешь.
- **Output:** Пишет `.ux/last-discovery.json` (бриф на 10 полей).
- **Цепляется к:** `/ux-recommend` → использует discovery для выбора стиля + палитры + типа + motion + компонентов. `/ux-design [extra brief]` → генерирует frontend-код, привязанный к рекомендации. `/ux-component <name>` → генерирует один компонент, выровненный по найденным ограничениям.

#### `/ux-recommend` — флагманский движок 5-параллельного поиска

- **Что:** Запускает 5-параллельный поиск Python-движка по 11 манифестам и возвращает одну объединённую design-систему. Индустрия → Стиль → Палитра → Типографика → Motion + Компоненты + Brand-образцы + Guardrails.
- **Когда использовать:** Запускаешь новый проект с нуля. Пивотишь уставший продукт. Pre-flight перед любым `/ux-design` или `/ux-component`.
- **Когда пропустить:** Уже запустил `/ux-discover` и сохранил бриф — `/ux-recommend` автоматический в этом флоу. Чинишь один баг (используй `/ux-fix`). Нужно только lint (используй `/ux-lint`).
- **Вызов (Claude Code):**
  ```
  /ux-recommend
  ```
  **Вызов (CLI):**
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
- **Output:** Пишет `.ux/last-recommendation.json` — выбранный стиль, выбранная палитра, выбранная типографическая пара, топ-5 motion-пресетов, топ-12 компонентов, топ-5 brand-образцов, все 100 активных guardrails анти-паттернов, плюс rationale.
- **Цепляется к:** `/ux-design [brief]` → frontend-код, использующий рекомендованные токены. `/ux-system` → полная design-система из рекомендации. `/ux-component <name>` → один компонент с рекомендованным стилем. `/ux-lint` → проверка сгенерированного кода.

### Генерация

#### `/ux-design` — генерирует красивую анти-slop поверхность из брифа

- **Что:** Генерирует полный production-grade frontend-артефакт (landing, маркетинговый сайт, app shell) из discovery-брифа + рекомендации. Диспатчит `frontend-engineer` с креативным направлением из anti-slop и arsenal-референсов.
- **Когда использовать:** «Design a», «build me a», «generate a landing page», «create a dashboard», «make a component» — любой free-form запрос визуального deliverable.
- **Когда пропустить:** Нужен ревью, а не сборка (используй `/ux-audit` или `/ux-critique`). Нужен только один компонент (используй `/ux-component`). Backend или инфраструктурная работа.
- **Вызов:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Output:** Сгенерированный код (HTML / Blade / JSX / Vue / Astro), плюс `.ux/last-design.json`.
- **Цепляется к:** `/ux-lint` → проверка против guardrails. `/ux-polish` → косметический проход. `/ux-a11y` → аудит доступности. `/ux-copy` → ревью microcopy. `/ux-fix` → применить findings атомарными коммитами.

#### `/ux-component` — генерирует один компонент

- **Что:** Производит один production-grade компонент (button, modal, navbar, sidebar, card, table, form, chart) из спеки. Все четыре состояния взаимодействия, доступный, on-brand. Сначала ищет компонент в `.ux/last-recommendation.json`, откатывается к прямому запросу к манифесту.
- **Когда использовать:** Любой запрос одного элемента — «build a button», «create a pricing card», «make a modal», «add a navbar», «design a sidebar», «I need a data table», «build a form», «make a chart component».
- **Когда пропустить:** Полная страница или multi-section поверхность (используй `/ux-design`). Backend или инфраструктура.
- **Вызов:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Output:** Сгенерированный код компонента, плюс `.ux/last-component.json`.
- **Цепляется к:** `/ux-lint` → проверка. `/ux-polish` → подтянуть.

#### `/ux-system` — генерирует полную стартовую design-систему

- **Что:** Предлагает полную стартовую design-систему для проекта, у которого её нет — токены (цвет, тип, пространство, motion, радиус, тень), foundation-документы, контракты компонентов, dark-mode-сопряжения, theme switcher. Диспатчит `design-system-architect`.
- **Когда использовать:** «We don't have a design system», «build us a system», «propose tokens», «what should our theme be», «set up our DS».
- **Когда пропустить:** У проекта уже есть design-система — используй `/ux-component` против существующей системы. Backend или инфраструктура.
- **Вызов:** `/ux-system` (запускает discovery, если её ещё нет).
- **Output:** `tokens.json`, `foundations.md`, контракты `components/*.md`, опциональный emit Tailwind / vanilla / SCSS. Пишет `.ux/last-system.json` для цепочечного контекста.
- **Цепляется к:** `/ux-component` → строит против новой системы. `/ux-design` → генерирует поверхность, использующую новые токены.

#### `/ux-dashboard` — специализированная генерация dashboard

- **Что:** Dashboard с дисциплиной плотности данных — bento-лейаут, табличные моноширинные цифры, sparkline-паттерны, anti-card-overuse, семантические цвета состояний, скупой motion. Не маркетинговый сайт с приклеенными графиками.
- **Когда использовать:** «Build a dashboard», «design the admin panel», «make a metrics page», «operator console», «analytics view», «KPI board», «monitoring screen».
- **Когда пропустить:** Маркетинговый лендинг со статистикой (используй `/ux-design`). Только один виджет (используй `/ux-component`). Backend или инфраструктура.
- **Вызов:** `/ux-dashboard`.
- **Output:** Сгенерированный код dashboard + `.ux/last-dashboard.json`.
- **Цепляется к:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — обработка motion

- **Что:** Генерирует motion-слой поверхности — длительности, easing, хореографию, reduced-motion-фолбэки, perf-дисциплину. Также аудитирует существующий motion против 5 измерений (timing, easing, смысл, reduced-motion, performance).
- **Когда использовать:** «Motion check», «are the animations good», «fix the motion», «review the animations», «motion audit», «performance pass on the motion».
- **Когда пропустить:** Поверхность не имеет motion (используй `/ux-audit` или `/ux-polish`). Backend или инфраструктура.
- **Вызов:** `/ux-motion path/to/component.tsx` (режим аудита) или `/ux-motion --generate hero-entry` (генерация).
- **Output:** Обновлённый код (в режиме генерации) или отчёт `.ux/last-motion.json` (в режиме аудита).
- **Цепляется к:** `/ux-fix` → применить motion-findings. `/ux-polish` → подтянуть.

### Audit & верификация

#### `/ux-lint` — детерминированный regex-based linter (без LLM, CI-safe)

- **Что:** Запускает 100 regex-правил против твоего кода. Никакого вызова LLM. Выходит с non-zero на Critical / High в CI. Источник: `data/anti-patterns.json`. Правила покрывают A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4).
- **Когда использовать:** Pre-commit хук. CI gate. Быстрый первый проход по большой кодовой базе перед тратой на `/ux-audit`. После `/ux-design` или `/ux-component` для проверки генерации.
- **Когда пропустить:** Хочешь fix loop (linter отчитывается, не редактирует — цепляй в `/ux-polish --fix` или `/ux-fix`). Хочешь taste-суждение (используй `/ux-critique`).
- **Вызов (slash):** `/ux-lint src/`.
- **Вызов (CLI):** `uxskill lint .` или `python3 bin/ux-lint.py .` или `bash bin/ux-lint.sh --ci --fail-on high`.
- **Вызов (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Findings в stdout (локация, id правила, severity, evidence). Exit code 0, если чисто, non-zero на Critical/High, когда установлен `--fail-on high`.
- **Цепляется к:** `/ux-polish --fix` → LLM-driven контрпартнёр на тех же паттернах. `/ux-fix` → применить findings коммитами, отсортированными по severity. `/ux-audit` → полный 6-линзовый проход рассуждения. `/ux-next` → пусть conductor решит.

#### `/ux-audit` — 6-линзовый design-аудит

- **Что:** Структурированный, мнение-имеющий ревью против шести линз (ясность, иерархия, доступность, голос, motion, taste), производящий severity-помеченные findings. Polaris-стиль отчёта. Сначала читает `.ux/last-frame.json` — аудитория и outcome закрепляют severity каждого finding.
- **Когда использовать:** Поверхность существует, и тебе нужна защитимая критика. «Audit», «review the ux», «is this any good», «what's broken», «tear this apart».
- **Когда пропустить:** Поверхность ещё не существует (используй `/ux-design`). Пользователь хочет одну линзу (используй целевую команду: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Пользователь хочет taste-мнение (используй `/ux-critique`). Backend или инфраструктура.
- **Вызов:** `/ux-audit https://example.com/pricing` или `/ux-audit src/components/Pricing.tsx`.
- **Output:** Пишет `.ux/last-audit.json` — массив `findings` из `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Цепляется к:** `/ux-fix` → применить findings. `/ux-polish` → косметический проход. `/ux-design` → если нужен структурный редизайн.

#### `/ux-a11y` — WCAG 2.1 AA аудит + проверки общей вежливости

- **Что:** Структурированный WCAG 2.1 AA аудит, плюс проверки общей вежливости, которые проходят автоматические инструменты, но всё равно вредят реальным пользователям (видимость фокуса, специфичность ошибок, motion-предпочтения, ловушки клавиатуры, опора на цвет).
- **Когда использовать:** Pre-ship гейт доступности. После редизайна. «Accessibility check», «WCAG audit», «is this accessible», «a11y review», «screen reader test», «keyboard nav check».
- **Когда пропустить:** Не user-facing. Backend или инфраструктура. WIP-наброски.
- **Вызов:** `/ux-a11y https://example.com` (предпочтителен live URL — автоматические инструменты и keyboard-тестирование работают только в live).
- **Output:** Пишет `.ux/last-a11y.json` — массив `findings` из `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, массив `beyond_wcag`, `severity_counts`.
- **Цепляется к:** `/ux-fix` → применить findings коммитами. `/ux-copy` → починить alt-текст и wiring ошибок форм в рамках copy-прохода.

#### `/ux-critique` — taste-выбор (3 выигрыша, 3 промаха, 1 стратегический ход)

- **Что:** Мнение дизайнера — не структурный аудит, не severity-оценка, а просто плотное, мнение-имеющее take, которое называет, что работает, что нет, и тот единственный стратегический ход, который изменит больше всего.
- **Когда использовать:** «What do you think», «is this good», «critique this», «honest take», «is the vibe right», «does this feel like us», «should we ship this».
- **Когда пропустить:** Пользователь явно хочет структурный аудит (используй `/ux-audit`). Backend или инфраструктура.
- **Вызов:** `/ux-critique https://example.com`.
- **Output:** Пишет `.ux/last-critique.json` — 3 выигрыша, 3 промаха, 1 стратегический ход, плюс проза.
- **Цепляется к:** `/ux-design`, если take рекомендует редизайн. `/ux-polish`, если take рекомендует подтянуть.

#### `/ux-copy` — ревью microcopy + переписывание

- **Что:** Оценивает каждую видимую строку против voice-рубрики и производит before/after переписывание. Ловит: «form contains errors» (общее), «John Doe» (заполнитель), AI-весёлая праздничная copy, общие CTA, мёртвые empty states, бесполезные ошибки.
- **Когда использовать:** Структура правильная, но слова слабы. «Review the copy», «fix the microcopy», «the error messages are bad», «rewrite this», «tighten the strings», «the buttons sound generic», «this empty state is dead».
- **Когда пропустить:** Проблемы лейаута (используй `/ux-audit` или `/ux-polish`). Copy-проблемы, вызванные доступностью, как alt-текст (используй `/ux-a11y`). Backend или инфраструктура.
- **Вызов:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Пишет `.ux/last-copy.json` — массив `strings` из `{location, severity, before, after, notes}`, плюс рубрика + локали, требующие перевода.
- **Цепляется к:** `/ux-fix` → применить переписывания. `/ux-a11y` → перепроверить после copy-починок.

### Fix & polish

#### `/ux-fix` — применить findings атомарными коммитами

- **Что:** Читает последний отчёт из `.ux/` (audit, copy, a11y, motion или polish), валидирует рабочее дерево и применяет findings атомарными коммитами через правильных саб-агентов. Перепроверяет, перезапуская исходную команду.
- **Когда использовать:** После запуска команды audit-класса и ревью findings. «Fix the findings», «apply the fixes», «run the fix loop», «patch the surface», «make the changes», «go fix it».
- **Когда пропустить:** Нет предыдущего отчёта в `.ux/`. Рабочее дерево грязное, и пользователь не согласился stash/commit. Починки требуют design-суждения, а не механического применения (используй `/ux-design` для редизайна).
- **Вызов:** `/ux-fix` (автоопределяет, какой отчёт чинить) или `/ux-fix --from=last-a11y.json`.
- **Output:** Атомарные коммиты на finding. Перезапускает исходную команду и обновляет файл `.ux/last-*.json`. Печатает сводку.
- **Цепляется к:** `/ux-next` → conductor выбирает следующий ход.

#### `/ux-polish` — косметический проход + убийство AI-slop

- **Что:** Ритм spacing'а, заточка иерархии, детекция AI-slop, согласованность токенов. LLM-driven контрпартнёр `/ux-lint` — использует твоё суждение в taste-выборах.
- **Когда использовать:** Структура правильная, но исполнение рыхлое. «Polish», «tighten this up», «remove the AI-slop», «make it premium», «make this less AI-looking», «the spacing feels off», «this looks generic», «needs more taste».
- **Когда пропустить:** Поверхности не хватает core-функциональности (сначала почини это). Нужен редизайн, не polish (используй `/ux-design`). Copy-проблемы (используй `/ux-copy`). Motion-проблемы (используй `/ux-motion`). A11y-проблемы (используй `/ux-a11y`).
- **Вызов:** `/ux-polish src/components/Hero.tsx`.
- **Output:** Обновлённый код + `.ux/last-polish.json`, описывающий изменения.
- **Цепляется к:** `/ux-lint` → проверка, что polish удержался. `/ux-a11y` → перепроверить доступность.

### Discovery & нарратив

#### `/ux-frame` — framing-блок на 4 поля

- **Что:** Захватывает кому-это-для, outcome, гипотезу и signal of success в структурный framing-блок. Никакой design-работы — только intake на четыре поля, который превращает размытый запрос в рабочий бриф. Легче, чем `/ux-discover` (4 поля против 10).
- **Когда использовать:** Начало любого проекта, спринта или разового engagement'а. В середине потока, когда разговор сошёл с курса. «Frame this», «what's the brief», «set up the project», «framing».
- **Когда пропустить:** Уже зафреймлено (проверь `.ux/last-frame.json`). One-off сборка компонента без framing-импликаций. Backend или инфраструктура.
- **Вызов:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Output:** Пишет `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Цепляется к:** `/ux-discover` → расширяет фрейм до 10-полевого брифа. `/ux-design` → генерирует, используя фрейм как якорь.

#### `/ux-research` — планирование исследования + синтез

- **Что:** Режим планирования: пишет скрипты интервью, опросы, скринеры рекрутинга. Режим синтеза (`--synthesize`): переваривает интервью, аналитику, сайты конкурентов, A/B-результаты, support-тикеты в рекомендации. Диспатчит `research-synthesizer`.
- **Когда использовать:** «Plan a research study», «I need interview questions», «design a survey», «how do I recruit users», «user testing plan», «diary study», «preference test», «fake door», «smoke test», «synthesize my interview notes».
- **Когда пропустить:** Ответ уже известен с высокой уверенностью. Низкорисковые обратимые решения. Backend или инфраструктура.
- **Вызов:** `/ux-research --plan "loyalty wallet adoption in MENA"` или `/ux-research --synthesize interviews/*.md`.
- **Output:** Пишет `.ux/last-research.json` — research-план или синтезированные темы + evidence + рекомендации.
- **Цепляется к:** `/ux-frame` → интегрировать findings во фрейм. `/ux-design` → генерация из findings. `/ux-workshop` → провести воркшоп, используя research как вход.

#### `/ux-workshop` — 5-фазный workshop design-thinking

- **Что:** Фасилитирует discovery / design-thinking workshop end-to-end. Пять последовательных фаз (исследование → heat map → stakeholder map → решение-набросок → game plan). Тайм-боксы. Конкретные артефакты на каждую фазу. Заканчивается решением, а не «интересными находками».
- **Когда использовать:** Реальный вопрос, реальные участники, реальный временной бюджет. «Run a workshop», «facilitate a discovery», «let's do a design thinking session», «I have stakeholders for an hour, what do we do», «kick off the project».
- **Когда пропустить:** Бриф уже ясен и заскопирован. Сольный брейнсторм (используй `/ux-design` или `/ux-frame`). Команда в середине исполнения, не в discovery.
- **Вызов:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Пишет `.ux/last-workshop.json` — game plan + артефакты по фазам.
- **Цепляется к:** `/ux-design` → исполнить game plan. `/ux-research` → закрыть пробелы, которые всплыл воркшоп. `/ux-case-study` → опубликовать путь.

#### `/ux-case-study` — публикуемый case study (формат Wfrah-editorial)

- **Что:** Генерирует case study проекта в чисто-монохромном editorial-формате — Wfrah-типографика, hairline-разделители, нумерованные секционные коды (A)–(G), bilingual-safe лейаут. Документ, а не маркетинговая брошюра. Читает из `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Когда использовать:** Пост-лонч. После дискретной вехи. «Write a case study», «case study this project», «do the wrap-up doc», «publish this work», «portfolio piece».
- **Когда пропустить:** В проекте не хватает данных, чтобы заполнить секции (A)–(G). Пользователь хочет маркетинговый лендинг, а не case study (используй `/ux-design`).
- **Вызов:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Цепляется к:** Терминальная команда — обычно конец проекта.

### Conductor

#### `/ux-next` — дирижёр workflow (read-only)

- **Что:** Читает каждый `.ux/last-*.json` и называет следующую команду с самым высоким рычагом. Дирижёр, не строитель. Read-only.
- **Когда использовать:** Между командами. «What should I do next», «what's the next move», «decide for me», «where do we go from here».
- **Когда пропустить:** Нет предыдущих отчётов в `.ux/`. У тебя в голове конкретная следующая команда.
- **Вызов:** `/ux-next` (без аргументов) или `/ux-next --focus=a11y`.
- **Output:** Stdout — рекомендованная следующая команда + rationale.
- **Цепляется к:** Какую бы команду она ни выбрала.

#### `/ux-expert` — крючок для консалтинга

- **Что:** Выводит контактную инфу создателя плагина, когда пользователь просит реального UX-эксперта. Кратко, прямо, без маркетинга.
- **Когда использовать:** «Who built this», «I need a UX expert», «do you do consulting», «can I hire someone for this», «is there a human behind this plugin».
- **Когда пропустить:** Пользователь спрашивает про фичи плагина, а не про консалтинг.
- **Вызов:** `/ux-expert`.
- **Output:** Краткая контактная карточка с LinkedIn / email / репо.

### Граф цепочек команд

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  framing-блок на 4 поля
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  intake на 10 полей (FORCING GATE)
                  └────────────┬─────────┘
                               │ пишет .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 параллельных поисков -> объединённая система
                  └────────────┬─────────┘
                               │ пишет .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ пишет .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ пишет .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  применить findings коммитами
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  публикуемый артефакт
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — read-only
                  │  /ux-expert          │  крючок для консалтинга
                  └──────────────────────┘
```

---

## 5 саб-агентов

Саб-агенты — это специфичные для роли генераторы, диспатчируемые командами. Они никогда не работают независимо — их вызывают `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, и т.д. У каждого агента определена граница ответственности: они НЕ решают бриф; они исполняют против него.

### `frontend-engineer`

- **Владеет:** Production-grade frontend-кодом (React, Next.js, Vue, Blade+Alpine, ванильный HTML, Astro) с анти-AI-slop дисциплиной.
- **Диспатчится:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Входы:** Бриф + креативное направление + токены (из `.ux/last-recommendation.json`).
- **Выходы:** Рабочий код, отличимый от общего AI-вывода. Никаких фиолетовых градиентов, никакого центрированного hero, никаких трёх одинаковых карточек, никакого Inter в display-размере, никакого «John Doe», никаких emoji, никаких дефолтов 300мс.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Владеет:** Motion в production frontend-коде — Framer Motion, GSAP, CSS-анимации. Длительности, easing, хореография, reduced-motion-фолбэки, perf-дисциплина.
- **Диспатчится:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Входы:** Motion-бриф + токены + 57 motion-пресетов из `data/motion-presets.json`.
- **Выходы:** Motion, заслуживший своё место. Всегда обёрнут в `prefers-reduced-motion`-фолбэки. Всегда протестирован против Core Web Vitals.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Владеет:** Строками, которые уходят в продакшен — сообщения об ошибках, empty states, CTA, состояния загрузки, success-сообщения, тосты, текст-подсказки, лейблы форм, текст кнопок.
- **Диспатчится:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Входы:** Voice-профиль (названный или вставленный) + строки поверхности.
- **Выходы:** Production-microcopy, применяемая последовательно через каждое состояние поверхности, чтобы продукт звучал как один продукт, а не десять. Запрещено: «form contains errors», «John Doe», AI-весёлая праздничная copy, общие CTA, мёртвые empty states.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Владеет:** Перевариванием research-входов (интервью, аналитика, сайты конкурентов, A/B-результаты, support-тикеты) в действенные design-рекомендации.
- **Диспатчится:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Входы:** Сырое исследование — транскрипты, экспорты, URL'ы конкурентов, support-кластеры.
- **Выходы:** Темы, evidence, рекомендации. Никогда не дизайнит ответ — даёт дизайнеру субстрат, от которого дизайнить.
- **Инструменты:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Владеет:** Полными design-системами — токены (цвет, тип, пространство, motion, радиус, тень), foundation-документы, контракты компонентов, dark-mode-сопряжения, theming-слой.
- **Диспатчится:** `/ux-system`, `/ux-component`, когда системы нет.
- **Входы:** Бренд-бриф + `.ux/last-recommendation.json` (стиль + палитра + типографическая пара + motion-пресеты).
- **Выходы:** Связная, мнение-имеющая, production-ready система, на которой downstream-агенты могут строить, не переопределяя фундаментал. Токены JSON, foundations MD, контракты компонентов, dark-mode-маппинг.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### Протокол диспатча саб-агентов

Когда команда диспатчит саб-агента, она передаёт:

1. Бриф / рекомендацию (загруженные из `.ux/`).
2. Релевантный срез манифеста (например, `frontend-engineer` получает выбранный стиль + палитру + компоненты; `motion-engineer` получает выбранные motion-пресеты).
3. 100 guardrails анти-паттернов (всегда активны).
4. Критерий успеха (что артефакт должен делать).

Саб-агенты возвращают:

1. Артефакт (код, документ, система).
2. Блок rationale (почему эти выборы).
3. Self-check против guardrails (какие правила они верифицировали).

Вызывающая команда затем автоматически запускает `/ux-lint` перед объявлением готовности.

---

## 11 data-манифестов

Слой данных — это мозг. Каждая команда читает из него; движок мёрджит через него; linter сканирует против него. Все файлы живут в `data/` и оборачивают записи в `{_meta, entries}` для версионирования схемы.

### `styles.json` — 84 design-стиля

| Поле | Описание |
|---|---|
| `entries` | 84 |
| `ключи на запись` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `категории` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, и т.д. |
| `пример записи` | `swiss-international` — «Сетка — это закон. Типографика делает тяжёлую работу. Декорация — это провал.» |

Используется: `/ux-recommend`, `/ux-system`, `/ux-design`. Схема: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 цветовых палитр

| Поле | Описание |
|---|---|
| `entries` | 176 |
| `ключи на запись` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `тона` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, и т.д. |
| `пример записи` | `claude-warm-editorial` — light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Используется: `/ux-recommend`, `/ux-system`. Контраст проверен на AA / AAA. Схема: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 типографических пар

| Поле | Описание |
|---|---|
| `entries` | 70 |
| `ключи на запись` | `id`, `name`, `display` (family + веса + источник + лицензия + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `пример записи` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

У всех families есть лицензия + URL источника. Используется `/ux-recommend`, `/ux-system`.

### `components.json` — 148 компонентов

| Поле | Описание |
|---|---|
| `entries` | 148 |
| `ключи на запись` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `категории` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `пример записи` | `mega-nav-product-grid` — Mega Navigation, Product Grid — 6-частная анатомия, 4 состояния |

Это наш самый большой ров. Никакой другой UX-плагин для Claude не поставляет структурный манифест компонентов.

### `industries.json` — 184 правила индустрий

| Поле | Описание |
|---|---|
| `entries` | 184 |
| `ключи на запись` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `категории` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, и т.д. |
| `пример записи` | `fintech-neobank` — высокое доверие, регуляторные раскрытия, primary-UI баланса/транзакций, mobile-first ежедневное использование |

Используется `/ux-recommend` как первая ось параллельного поиска.

### `chart-types.json` — 35 типов графиков

| Поле | Описание |
|---|---|
| `entries` | 35 |
| `ключи на запись` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `категории` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `пример записи` | `bar-vertical` — Сравнивает 4–15 дискретных категорий. Позиция по оси x — категория; высота — значение. |

Используется `/ux-dashboard`, `/ux-component` (chart-инстансы).

### `tech-stacks.json` — 25 стеков

| Поле | Описание |
|---|---|
| `entries` | 25 |
| `ключи на запись` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `пример записи` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, совместим с Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Другие стеки включают Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 именованных UX-законов

| Поле | Описание |
|---|---|
| `entries` | 112 |
| `ключи на запись` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `категории` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, и т.д. |
| `пример записи` | `hicks-law` — Время решения растёт логарифмически с количеством представленных выборов |

Используется `/ux-audit` (6-линзовый scoring) и `/ux-critique` (taste-якорь).

### `motion-presets.json` — 57 motion-пресетов

| Поле | Описание |
|---|---|
| `entries` | 57 |
| `ключи на запись` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion-фолбэк), `when_to_use` |
| `категории` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `пример записи` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

У каждого пресета есть reduced-motion-вариант. Stack-ready код для Framer Motion, GSAP и чистого CSS.

### `anti-patterns.json` — 100 regex-правил

| Поле | Описание |
|---|---|
| `entries` | 100 |
| `ключи на запись` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `категории` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

Полный список правил в [100 правил против AI-slop](#100-правил-против-ai-slop--linter).

### `brands/*.json` — 110 brand-спеков

| Поле | Описание |
|---|---|
| `entries` | 110 (плюс `_index.json`, листающий все) |
| `ключи на запись` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `категории` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Полный список в [110 brand-спеков DESIGN.md](#110-brand-спеков-designmd--по-категориям).

---

## 100 правил против AI-slop — linter

ux-skill поставляет детерминированный regex-based linter. **Никакого LLM.** **Никаких API.** **Никакой сети.** Работает в CI за ~200мс на типичном Next.js-приложении. Выходит с non-zero на Critical / High findings, когда установлен `--fail-on high`.

Правила берутся из `data/anti-patterns.json` (предпочтительно v2) с fallback `references/foundations/anti-patterns.md` (v1 bash). Поставляются два бинаря: `bin/ux-lint.py` (Python, быстрый, расширяемый) и `bin/ux-lint.sh` (Bash + perl-PCRE, для сред без Python).

### Правила по категориям

#### Typography (3 правила)

| Severity | ID правила | Имя |
|---|---|---|
| high | `inter-as-display` | Inter использован как display-шрифт |
| medium | `hero-text-arbitrary-90px` | Произвольный размер hero-шрифта |
| low | `font-system-only` | Системный font-stack без выбранного typeface |

#### Color (6 правил)

| Severity | ID правила | Имя |
|---|---|---|
| high | `purple-to-blue-gradient` | Дефолтный AI-градиент фиолетовый-в-синий |
| high | `dark-text-on-dark-card` | Низкоконтрастный текст на карточке |
| medium | `gradient-text-rainbow` | Multi-stop градиентный текст |
| medium | `card-glow-purple-shadow` | Фиолетовая glow-тень на карточках |
| medium | `gradient-mesh-purple-pink` | Hero с purple-pink mesh-градиентом |
| low | `tailwind-color-named-vague` | Именованные Tailwind-цвета без семантического токена |

#### Layout (5 правил)

| Severity | ID правила | Имя |
|---|---|---|
| high | `three-equal-card-grid` | Три одинаковых карточки в ряд |
| medium | `centered-everything-hero` | Центрированная композиция hero |
| medium | `avatar-stack-overlapping` | Generic перекрывающийся стек аватаров |
| low | `pill-rounded-full-everywhere` | `rounded-full` применён ко всему |
| low | `nav-equal-hamburger-desktop` | Гамбургер-меню на десктопе |

#### Content (5 правил)

| Severity | ID правила | Имя |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum в shipping-коде |
| high | `emoji-in-ui` | Emoji использована как UI-элемент |
| high | `icon-emoji-stamp` | Emoji использована как icon-штамп |
| high | `testimonial-fake-five-stars` | Хардкоженный пятизвёздочный отзыв |
| medium | `fake-name-john-doe` | Общие placeholder-имена |

#### Motion (3 правила)

| Severity | ID правила | Имя |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Прыгающая стрелка на CTA |
| low | `timing-300ms-default` | Дефолтный timing перехода 300мс |
| low | `cubic-bezier-material-only` | Дефолтный Material-easing повсюду |

#### A11y (6 правил)

| Severity | ID правила | Имя |
|---|---|---|
| high | `inline-svg-no-aria` | SVG без aria-label или aria-hidden |
| high | `img-no-alt` | Изображение без атрибута alt |
| high | `link-onclick-no-href` | Anchor с onClick, но без href |
| medium | `button-no-type` | Button без атрибута type |
| medium | `heading-skip-h1-h3` | Пропущенный уровень heading |
| medium | `infinite-scroll-no-pagination` | Бесконечный скролл без keyboard-фолбэка |

#### Quality (6 правил)

| Severity | ID правила | Имя |
|---|---|---|
| high | `console-log-leak` | `console.log` в коде компонента |
| medium | `inline-style-attribute` | Inline style-атрибут |
| medium | `any-type-leak` | TypeScript-тип `any` |
| medium | `arbitrary-z-index-9999` | Ленивое значение z-index |
| low | `shadcn-default-everywhere` | Дефолтный shadcn token-блок не изменён |
| low | `todo-fixme-comment` | TODO или FIXME в shipping-коде |

#### Visual (1 правило)

| Severity | ID правила | Имя |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur без glass-поверхности |

### Использование linter'а

**Разовый scan:**

```bash
uxskill lint .
# или
python3 bin/ux-lint.py src/
# или
bash bin/ux-lint.sh src/
```

**CI gate (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Pre-commit хук:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Output (пример):**

```
─── отчёт /ux-lint ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidence: bg-gradient-to-br from-purple-500 to-blue-500
  fix: заменить на primary-градиент рекомендованной палитры или убрать градиент

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  evidence: grid grid-cols-3 gap-6 (3 одинаковых Card-потомка)
  fix: выделить одну карточку; обрамить двумя карточками с пониженным акцентом

3 файла просканировано · 2 high · 0 medium · 0 low · exit 1
Рекомендовано далее: /ux-polish --fix (LLM-driven, адресует lintable и эстетические findings)
```

---

## 110 brand-спеков DESIGN.md — по категориям

Реальные бренды. Реальные design-языки. Реальные DESIGN.md-спеки — не общие палитры. Скажи плагину «собери лендинг в стиле Stripe», и он читает реальный bran-словарь: voice-рубрика, color-токены, motion-конвенции, signature-ходы, anti-ходы.

Каждый бренд поставляется как структурный JSON (`data/brands/<slug>.json`) плюс ссылка в прозе (`references/brands/<slug>.md`).

### Developer Tools (36)

ClickHouse, Composio, Cursor, Datadog, dbt Labs, Expo, Fivetran, Fly.io, Framer, HashiCorp, Honeycomb, IBM, Lovable, Mintlify, Modal, MongoDB, Neon, Ollama, OpenCode, PostHog, Railway, Raycast, Render, Replicate, Resend, Retool, Sanity, Sentry, Slack, Snowflake, Sourcegraph, Supabase, Superhuman, Vercel, Warp, Webflow

### Consumer / Lifestyle / Retail (19)

Aesop, Airbnb, Allbirds, Apple, Apple Music, Glossier, HP, Hims & Hers, Instagram, Meta, Nike, Patagonia, Pinterest, PlayStation, Shopify, Spotify, Starbucks, TikTok, Uber

### Fintech / Crypto (14)

Binance, Brex, Coinbase, Kraken, Mastercard, Mercury, Monzo, N26, Plaid, Ramp, Revolut, Robinhood, Stripe, Wise

### Editorial / Media (13)

Bloomberg, Clay, Dezeen, NVIDIA, Pitchfork, Substack, The Atlantic, The Economist, The New York Times, The Verge, The Wall Street Journal, Vodafone, Wired

### AI / ML Platform (12)

Anthropic, Claude, Cohere, ElevenLabs, MiniMax, Mistral AI, OpenAI, Perplexity, Runway, Together AI, VoltAgent, xAI

### Productivity / Collaboration (8)

Airtable, Cal.com, Figma, Intercom, Linear, Miro, Notion, Zapier

### Automotive (8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### Почему это важно

Остальные 8 популярных UX-плагинов для Claude генерируют «modern minimal» или «clean dashboard» — варианты одной и той же дефолтной эстетики. ux-skill позволяет просить **ясность Linear**, **серьёзность Stripe**, **сдержанность Apple**, **монолит Tesla**, **дружелюбие Notion**, **gradient-дисциплину Cursor**, **hairline-плотность Raycast**, **тёплый editorial Claude** — и движок тянет правильные токены, voice, motion-конвенции и signature-ходы из brand-спеки.

---

## MCP-сервер — асимметричный ход

ux-skill поставляет **сервер Model Context Protocol**. Запусти `ux-mcp`, и движок становится long-running stdio-процессом, который любой MCP-совместимый хост — Claude Desktop, Cursor, Windsurf, общие агенты — может вызывать. Четырнадцать инструментов: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Те же Python-handler'ы, что используют slash-команды; те же data-манифесты; тот же детерминированный recommender.

**Почему это асимметричный ход:** ни один из топ-8 UX-скилов Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) не поставляет MCP-сервер. Они заперты внутри runtime'а плагинов Claude Code. ux-skill достижим из любого хоста, говорящего на MCP, включая агентов, которые никогда не слышали о плагине Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp — это opt-in extra
ux-mcp                                  # запускается stdio JSON-RPC сервер
```

Направь своего клиента на бинарь `ux-mcp`. Полная документация инструментов, JSON-примеры и конфиги для клиентов Claude Desktop, Cursor и Windsurf живут на [docs/mcp.html](docs/mcp.html) и в `commands/ux-mcp.md`.

---

## Установщик для 17 IDE

`uxskill init` (или `/ux-init` внутри Claude Code) автоопределяет, какую IDE ты используешь, и пишет правильный артефакт. Один и тот же Python-движок. Те же рекомендации. Разный клей для каждой IDE.

| IDE / инструмент | Сигнал детекции | Установленный артефакт |
|---|---|---|
| Claude Code | `.claude/` или `CLAUDE.md` | Plugin-манифест на `.claude-plugin/plugin.json` + все 22 команды + все 5 саб-агентов |
| Cursor | `.cursor/` или `.cursorrules` | `.cursorrules` prompt-header, указывающий на движок |
| Windsurf | `.windsurf/` или `.windsurfrules` | `.windsurfrules` с тем же prompt-header |
| GitHub Copilot | `.github/copilot-instructions.md` или `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | патч `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` или `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

В каждой IDE те же CLI-команды `uxskill recommend` / `uxskill lint` / `uxskill stats` работают из терминала. Python-движок — источник истины; IDE-артефакты — тонкие prompt-header'ы, маршрутизирующие в него.

---

## Сценарии использования — конкретные кейсы

Восемь реальных сценариев. Выбери ближайший к твоей ситуации и адаптируй вызов.

### 1. Сборка fintech-dashboard в Cursor

Ты в Cursor работаешь над dashboard'ом MENA-необанка. Ты ставишь плагин и запускаешь discovery, рекомендацию, затем генерацию dashboard'а.

```bash
pip install uxskill
uxskill init                                # детектит Cursor, пишет .cursorrules
uxskill discover                            # intake на 10 полей
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Затем в Cursor попроси: *«Сгенерируй dashboard-поверхность, используя рекомендацию в .ux/last-recommendation.json»*. Cursor читает `.cursorrules`-header, загружает рекомендацию, диспатчит генерацию dashboard'а с явными ограничениями.

### 2. Генерация Stripe-стилевого лендинга в Claude Code

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

/ux-recommend
> [возвращает выбранный стиль, палитру, типографическую пару, motion-пресеты, компоненты, brand-образцы]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer генерирует страницу]

/ux-lint .
> [проходит — Stripe brand spec был соблюдён]
```

### 3. Аудит существующего кода на AI slop в CI

Ты задеплоил Next.js-приложение две недели назад. Тебе нужен жёсткий пол против AI-отпечатков на каждом PR.

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

PR'ы, вносящие фиолетово-синие градиенты, Inter в 96px, отзывы «John Doe» или emoji-как-иконки, фейлят CI. Никакой стоимости LLM. ~200мс.

### 4. Polish существующей поверхности, которая «выглядит AI-сгенерированной»

Ты унаследовал React-приложение, которое выглядит как любой другой AI-сгенерированный SaaS-сайт. Ты хочешь сделать так, чтобы оно так не выглядело.

```
/ux-critique src/components/Hero.tsx
> [3 выигрыша, 3 промаха, 1 стратегический ход — take честный]

/ux-lint src/
> [15 high-severity AI-отпечатков помечено]

/ux-polish src/components/Hero.tsx
> [LLM-driven косметический проход + убийство AI-slop]

/ux-fix
> [применяет findings атомарными коммитами, перезапускает linter]
```

Три команды, одна отполированная поверхность, атомарные коммиты на починку.

### 5. Дизайн Linear-стилевой command palette

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [читает data/brands/linear.app.json для токенов + signature-ходов]
> [читает data/components.json для анатомии + состояний command-palette]
> [диспатчит frontend-engineer с явной Linear-спекой]
```

Сгенерированный компонент использует реальные цветовые токены Linear, type-stack, motion-конвенции, hairline-плотности — не «общий dark UI».

### 6. Запуск 90-минутного design-thinking воркшопа со стейкхолдерами

У тебя комната с 5 людьми на 90 минут. Ты хочешь, чтобы они ушли с game plan'ом, не с vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Плагин фасилитирует пять фаз (исследование → heat map → stakeholder map → решение-набросок → game plan) end-to-end, в тайм-боксах, с конкретными per-phase артефактами. Output — `.ux/last-workshop.json` — game plan, не просто «интересные находки».

### 7. Написание публикуемого case study после лонча

Ты задеплоил loyalty-кошелёк. Тебе нужен кусок для портфолио.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [читает .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [генерирует Wfrah-editorial case study с нумерованными (A)-(G) секциями, hairline-разделителями, bilingual-safe лейаутом]
> [пишет case-studies/bashiti-loyalty.html]
```

Case study — это законченный, публикуемый артефакт, не черновик. Чистая монохромия, editorial-типографика, готов отгружать в портфолио.

### 8. Запуск discovery в non-AI контексте (только структурный intake)

Ты скопируешь проект. Тебе пока не нужна рекомендация — тебе нужен структурный бриф.

```bash
uxskill discover
# intake на 10 полей, сохраняется в .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Ты можешь передать JSON команде, вставить в Notion-документ или подать в отдельный AI-инструмент. ux-skill — это также инструмент структурного intake, в дополнение к тому, что он движок.

### 9. MASTER.md persistence — твои design-решения в репо

После `/ux-recommend` сохрани выбранный стиль + палитру + тип + motion + компоненты + brand-образцы + guardrails как human-readable Markdown-файл, который твоя команда может ревьювить, диффать и контролировать версиями.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Пишет `.ux/design-system/MASTER.md` (YAML-frontmatter + body) и `.ux/design-system/pages/<name>.md` на каждую сгенерированную поверхность через `persist save-page`. Идемпотентно — тот же вход даёт байт-идентичный выход, так что перезапуск на неизменном состоянии — это no-op в git.

---

## Сравнение с альтернативами

Краткая сводная таблица. Полное сравнение таблица за таблицей на [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Измерение | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash-команды | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Компоненты | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion-пресеты | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand-спеки | **110** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Правила анти-паттернов | **100** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-safe детерминированный linter | **да** | нет | нет | нет | нет | нет | нет | нет | нет |
| Поддерживаемые IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery-gate | **10 полей** | неявный | неявный | неявный | неявный | неявный | неявный | неявный | неявный |
| Цепь состояний `.ux/` | **да** | нет | нет | нет | нет | нет | нет | нет | нет |
| Звёзды (2026-05-28) | 14 | 83 958 | 54 406 | 25 202 | 15 455 | 5 762 | 2 391 | 2 164 | 955 |

### Честная оценка

- **ui-ux-pro-max** больше по узнаваемости, поставляет 18 IDE, имеет BM25-стилевой поиск по своему CSV. Не поставляет манифест компонентов, манифест motion, brand-библиотеку или детерминированный linter.
- **open-design** имеет 19 скилов + preview, но только поддержку Claude Code и никакого anti-slop слоя.
- **hallmark** ближайший по духу (тоже anti-slop), но это один скил — нет движка, нет манифестов, нет цепочечных команд.
- **material-3-skill** отличен, если ты специально хочешь Material Design 3. Мы не конкурируем по MD3.

Полные детали по каждому измерению см. [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Полнота linter'а (Q3 2026)

- **+17 отложенных правил анти-паттернов** до 52 в сумме. Цели: dark-on-dark hover-состояния, кодирование состояния только цветом, избыточная z-index эскалация, хардкоженные breakpoints в JS, opacity вместо disabled-состояния, и т.д.
- **`uxskill lint --fix` для безопасных переписываний** механически чинимых findings (button-no-type, img-no-alt empty-string, удаление console-log-leak).
- **Расширение VS Code**, которое выводит lint-findings inline (без необходимости запускать CI).

### v2.2 — Расширение манифеста компонентов (Q4 2026)

- **+50 компонентов** до 198 в сумме. Новые: combobox с async-фильтром, command-palette с heuristics recent-items, conditional-form-step, варианты payment-element, RTL-aware date picker, MENA-специфичный phone input, calendar grid с hijri-оверлеем.
- **Per-component code emit** в 6 стеках (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, ванильный HTML/CSS).
- **Component playground** на uxskill.laithjunaidy.com/playground — попробовать recommendation engine + увидеть live-превью компонентов.

### v3 — Marketplace + lock-in (2027)

- **Marketplace brand-спеков** — публикуй и находи community-brand-спеки. Pay-to-publish для финансирования модерации.
- **Custom anti-pattern rules** — проекты могут определять свои regex-правила в `data/anti-patterns.local.json` (уже в v2; v3 добавляет discovery + sharing).
- **`uxskill plan`** — полное планирование multi-page сайта из брифа, не только одной поверхности.
- **Паритет с Figma-плагином** — тот же recommendation engine, выведенный в Figma.

---

## Как контрибьютить

Issue и PR приветствуются. Три области высокого рычага:

### Добавить правило анти-паттерна

1. Отредактируй `data/anti-patterns.json` — добавь запись с `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Добавь тест в `tests/linter/` — один файл, триггерящий правило, один — нет.
3. Запусти `uxskill lint tests/linter/should-trigger/<rule>.tsx` — подтверди, что срабатывает. Запусти на `tests/linter/should-not-trigger/<rule>.tsx` — подтверди, что нет.
4. Открой PR.

### Добавить brand-спеку

1. Создай `data/brands/<slug>.json` с `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Добавь соответствующую прозу в `references/brands/<slug>.md`.
3. Зарегистрируй в `data/brands/_index.json`.
4. Открой PR. Спека должна быть подкреплена ссылками на первоисточники (реальный продукт бренда, публичная design-система или DESIGN.md, если они его публикуют).

### Добавить motion-пресет

1. Отредактируй `data/motion-presets.json` — добавь запись с `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. У пресета должен быть reduced-motion вариант. Никаких исключений.
3. Открой PR.

### Процесс

- Прочитай [CONTRIBUTING.md](CONTRIBUTING.md) для полного процесса.
- Прочитай [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Новые правила и brand-спеки ревьюются на: привязку к первоисточнику, отсутствие overfitting к одному проекту, отсутствие emoji в любых данных, RTL-safe поведение, где применимо.

---

## Лицензия, автор, благодарности

### Лицензия

MIT. Используй, форкай, строй сверху. Если это спасло тебя от отгрузки AI slop, поставь звезду репо — это самый дешёвый способ поддержать.

### Автор

**Laith Aljunaidy** — solo founder [Dot](https://thedotwallet.com), MENA-first loyalty-платформы. Строит ux-skill, чтобы AI-сгенерированный frontend не выглядел весь одинаково.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Репо: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Сайт: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Благодарности

- Команде Anthropic за Claude Code и архитектуру skill / plugin, сделавшую это распространяемым.
- Nielsen Norman Group, Laws of UX (lawsofux.com) и UX-research community, чьи работы информируют `data/ux-guidelines.json`.
- Каждому бренду, перечисленному в `data/brands/` — их публичные design-системы являются источником истины для brand-спеков.
- Оригинальным контрибьюторам v1: single-shot Claude skill, ставшему семенем для v2 Python-движка.
- 8 популярным UX-плагинам Claude, с которыми мы сравнивались — они подняли планку; это наш ответ.

---

**ux-skill** · **v2.0.0-alpha.1** · Построено так, чтобы Claude Code, Cursor, Windsurf и любой другой AI-инструмент кодинга выдавали frontend, который не читается как AI-сгенерированный.

> Поставь звезду репо на [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Установи через `pip install uxskill` или `npx uxskill init` · Изучи сравнение на [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
