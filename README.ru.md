[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · **Русский** · [Türkçe](README.tr.md)

# ux-skill: движок design intelligence для Claude Code, Cursor и любого другого AI-инструмента для кодинга

**Движок design intelligence, который делает AI-сгенерированный UI самобытным, а не шаблонным.** Подключи его к любому из 17 AI-инструментов для кодинга, и результат перестанет выглядеть как сделанный нейросетью. Бесплатно, MIT, офлайн, без LLM.

```bash
pip install uxskill
```

**[Поставь ux-skill звезду на GitHub](https://github.com/Laith0003/ux-skill)**, если он полезен: это самый простой способ помочь проекту. Впервые здесь? Начни с [60-секундного обзора](#быстрая-установка) или посмотри вживую на [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![До: шаблонный hero со стоковым фото, мягкий фиолетовый градиент, никакой айдентики бренда. После: настоящее фото стройплощадки под тёмной подложкой, редакционный заголовок с янтарным акцентом и форма запроса сметы прямо в hero. Тот же промпт, другой результат, когда ограничения задаёт ux-skill.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*До: шаблонный SEO-slop со стоковым фото. После: hero с настоящим фото стройки под тёмной подложкой, редакционный заголовок с янтарным акцентом, форма сметы в hero. Тот же AI-инструмент для кодинга, тот же промпт, другой результат, когда ограничения задаёт ux-skill.*

> **v4.0, FOUNDATIONS: одна команда строит полную дизайн-систему, проверенную по WCAG, с арабским языком и письмом справа налево из коробки.** Самый сильный UX-плагин для AI-кодинга. Python-ядро рассуждений с детерминированным 7-осевым синтезатором, 12 запрашиваемых JSON-манифестов (84 стиля, 176 палитр, 70 шрифтовых пар, 148 компонентов, 184 отрасли, 35 типов графиков, 57 motion-пресетов, 112 законов UX, 171 правило анти-паттернов, 25 техстеков, 160 спецификаций брендов), 18 slash-команд, 5 саб-агентов, 25 MCP-инструментов и детерминированный linter против AI-slop. Кросс-IDE: ставится в Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer и Roo Cline.

> **Название бренда: `ux-skill`.** Имя пакета в PyPI / npm остаётся `uxskill`. Репозиторий на GitHub находится по адресу [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Автор:** [Laith Aljunaidy](https://laithjunaidy.com), дизайнер и CTO в Аммане · **Сайт:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Сравнение со всеми UX-плагинами для Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#установщик-для-17-ide)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Новое в 4.0: основы

На входе цвет бренда, на выходе дизайн-система, и её контраст проверен до того, как ты её получишь.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 или новее. Для MCP-сервера: `pip install --upgrade 'uxskill[mcp]'`. Через pipx: `pipx install uxskill` (поверх установленной 3.x: `pipx upgrade uxskill`). Через npm: `npx uxskill@latest`. Переходишь с 3.x? [Руководство по миграции](docs/migrating-to-4.md) сопоставляет каждый токен 3.x с его ролью в 4.0.

**Делаешь продукт или лендинг?** Ты получаешь `tokens.css`, который подключается к странице, `fonts.css` с запасными шрифтами, подогнанными по метрикам под выбранные гарнитуры, `fonts-self-host.css`, который грузит гарнитуры из твоих собственных файлов, `tokens.json` для инструментов, декоративную бренд-графику в `art/` и `system-report.md`, где простыми словами сказано, что построено, почему и с какой композиции страницы начать. Стилизуй через роли (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`) и переключай тёмную тему, высокий контраст, компактные отступы, письмо справа налево или сокращённую анимацию одним атрибутом на `<html>`. Подключай гарнитуры по ссылке Google Fonts из отчёта или через `fonts-self-host.css` и папку `fonts/`, а `fonts.css` подключай в обоих случаях, до `tokens.css`; ни тот ни другой файл не редактируй. С `--brief` облик следует отрасли и тону, если бриф их называет, а структурированные поля (возраст, языки, схема по умолчанию, контекст чтения) задают размер текста, области касания, письменности и схему, с которой всё открывается; discovery не спрашивает отрасль, поэтому её спрашивает `/ux-system create`. В Claude Code `/ux-system create` проверяет установленную версию, запускает сборку и объясняет отчёт.

**Проектируешь дизайн-систему?** Девять основ (цвет, шрифты, отступы, сетка, скругления, обводки, глубина, движение, изображения), каждая плавно меняется вместе с семью осями, с примитивами и семантическими ролями, в формате W3C design tokens (DTCG 2025.10) со значениями для каждого режима. Те же входные данные, те же байты. Через MCP `ux_system_build` возвращает отчёт, результат проверки и размер каждого файла, а если передать `out`, пишет те же файлы, что и команда.

- **Проверка WCAG.** Каждая цветовая пара для текста, элементов управления и фокуса измеряется в светлой и тёмной теме, при обычном и высоком контрасте: WCAG 1.4.3 (текст 4.5:1) и 1.4.11 (нетекстовые элементы 3:1) при обычном контрасте, WCAG 1.4.6 (текст 7:1) при высоком контрасте, плюс наш собственный порог 4.5:1 в высоком контрасте для большинства нетекстовых элементов, поскольку WCAG не задаёт усиленного уровня для нетекстовых элементов. Система, которая не прошла проверку, не записывается; сообщение говорит, что изменить.
- **Безопасно по умолчанию.** Никогда не перезаписывает файл, который отличается. `--force` заменяет файлы, только когда ты сам об этом просишь.
- **Арабский.** При `dir="rtl"` текст переключается на арабский шрифт со своими размерами и межстрочным интервалом; отступы используют логические свойства, а анимация зеркалится. `--latin-only` это отключает.

**Система, которая у тебя уже есть.** `/ux-system enhance --from` читает её в её собственных именах (токены DTCG, кастомные свойства CSS, тема Tailwind, markdown-файлы с правилами или экспорт переменных Figma), прогоняет через ту же проверку и измеряет, что твой код на самом деле с ней делает; ничего не переписывается. `/ux-system extend --from` добавляет основы, роли или контракты, не меняя ни одного существующего токена, в отдельном файле расширения рядом, а `uxskill system export` выгружает её как tokens.css, тему Tailwind 4 или переменные Figma. В 4.2 появятся слой доверия (lint при каждой записи, финальный ревьюер) и запуск. См. [changelog](CHANGELOG.md).

**Компоненты и секции.** 23 контракта компонентов описывают, какие токены связывает каждая часть элемента управления в каждом состоянии и как движется каждое состояние: смена состояния идёт по `motion.state`, нажатие масштабируется по `motion.press.scale` (и замирает при сокращённой анимации), а вкладки, меню и сегментированные контролы двигают один общий индикатор. 14 контрактов секций (hero, цены, FAQ, футер и остальные) называют задачу каждой секции, компоненты для её слотов, доказательство, которое ей нужно, и то, как она складывается на телефоне. Страницы, собранные из них, используют фотографии; фрагменты интерфейса служат дополнительными изображениями, но никогда не заменой.

**Linter, который читает страницу.** 171 правило, многие с проверкой по разобранному CSS и разметке, читают собственную систему страницы: тайминг анимации берётся из её кривой, межстрочный интервал display-заголовков держится на пороге движка, а скрытый элемент управления должен выпадать из порядка табуляции. `uxskill lint --render` открывает каждую страницу в headless Chromium на ширине десктопа и телефона и прогоняет её: кольца фокуса, которые не видны или обрезаны, hover и нажатие, которые отвечают с опозданием, фокус, потерянный после Escape, и нажатие, которое всё ещё двигается при сокращённой анимации.

**Меньше команд.** 25 slash-команд превращаются в 18. `/ux-discover` принимает `--frame` и `--recommend`, `/ux-design` принимает `--component`, `--dashboard` и `--from-image`, `/ux-polish` гоняет lint, fix, re-lint, пока оценка не дойдёт до 90 или не пройдут три раунда, а `/ux-init` принимает `--stats`. Семь старых имён продолжают работать как алиасы и исчезнут в 4.1; см. [алиасы](#алиасы-удаляются-в-41).

**Плейбуки поверхностей.** Правила для лендингов, дашбордов и компонентов лежат в `references/surfaces/`, по одному плейбуку на каждый вид. `/ux-design` загружает ровно один, выбранный по режиму, так что сборка дашборда никогда не читает правила hero.

Тесты: **9764 проходят**. Офлайн. Детерминированно. LLM не вызывается никогда.

### Новое в v3.1: верность бренду, адаптивность, живость

- **Верность бренду обеспечивается, а не ожидается.** Основной цвет считывается с пикселей ЛОГОТИПА (а не из самого закрашенного CSS); шрифты по умолчанию отвергаются в пользу стиля букв логотипа. Извлечённый бренд проходит путь `recommend` -> `synthesize`, а **жёсткий порог** в `evaluate` ПРОВАЛИВАЕТ любой результат, который теряет цвет или логотип бренда либо не содержит настоящих изображений. Двусторонняя совместимость с открытой конвенцией `brand.md` (рендер + импорт).
- **Mobile-first с проверкой.** Новые основы ремесла (`responsive.md`, `component-behaviors.md`) плюс проверка, учитывающая переносы строк: она падает на горизонтальной прокрутке, на переносе подписи в навигации, логотипе или кнопке и на слишком высокой sticky-шапке.
- **Слой wow.** Движок выводит 2-3 согласованных фирменных момента на страницу; доктрина «wow может прийти только от пользователя» отменена.
- **Более острый linter** (152 правила): обнаружение обязательных изображений и элементов только с иконкой, правила для токенов-заглушек и `100vw`; picsum с seed сохраняется, случайный удаляется.

Полные заметки в [CHANGELOG.md](CHANGELOG.md).

### Что нового в v3

- **Brand specs становятся обучающими данными, а не шаблонами.** 160 brand specs больше не каталог, из которого рекомендатор выбирает, это словарь, который синтезатор дистиллирует. Вывод нов на каждом вызове.
- **Синтезатор по 7 осям** (warmth, contrast, density, geometry, formality, motion, type_personality). Бриф детерминистически отображается в значения осей; значения осей компилируются в свежие palette + типографику + spacing + radius + motion-токены.
- **Три авто-диспатчируемых режима**: `strict_brand` (100% одного бренда), `brand_anchor` (70% один бренд + 30% адаптировано по осям от родственных брендов), `pure_synthesis` (бренд не назван, дистилляция 8 примеров с совпадающими осями).
- **Журнал решений переранжирует рекомендатор.** `.ux/decisions.jsonl` ре-ранкует кандидатов по прошлым победам в том же бакете `(industry, ui_type)`. Cold-start безопасен. Учитывает только решения с `lint_score >= 80` + `user_accepted = true`.
- **Матрица взаимодействия осей**: явное разрешение конфликтов между конкурирующими осями (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Больше никаких тихих ad-hoc правил.
- **Авто-цикл `/ux-evolve`** (в 4.0 это цикл по умолчанию в `/ux-polish`): lint → polish → re-lint, пока оценка ≥ 90, плато или 3 раунда в 4.0 (5 в v3). Quality gate на 65.
- **3 новых MCP-инструмента** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Локальный дашборд статистики**: `uxskill stats --html` пишет `.ux/stats.html`, показывающий, что выучила ИМЕННО ваша установка. Без телеметрии, без глобального агрегата.
- **223 теста проходят.** Офлайн. Детерминистично. LLM ни разу не вызывается.

Подробности в [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### История звёзд

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Что такое ux-skill

ux-skill, это **движок design intelligence** для AI-инструментов кодинга. Он работает как пакет Python (`pip install uxskill`), как плагин для Claude Code и как мультиустановщик для 17 IDE. Движок принимает бриф проекта (индустрия, аудитория, тон, must-have, запрещённые ходы, стек, регион) и возвращает полную рекомендованную design-систему: стиль, палитру, типографическую пару, motion-пресеты, компоненты, образцовые бренды для изучения и guardrails анти-паттернов, которые надо удержать. Рекомендация детерминированная, одинаковый вход всегда даёт одинаковый выход.

Плагин стоит между тобой и AI-инструментом кодинга. Когда ты просишь Claude Code, Cursor или любого другого AI-ассистента «собрать fintech-лендинг», ассистент обычно импровизирует, и результат читается как AI-сгенерированный за пять секунд (фиолетово-синие градиенты, три одинаковые карточки, Inter в размере display, «John Doe» в отзывах, переходы по умолчанию 300мс, центрированный hero, прыгающие стрелки на CTA). ux-skill заменяет импровизацию **структурными ограничениями**: ты запускаешь `/ux-discover`, чтобы зафиксировать бриф и выбрать систему, `/ux-design`, чтобы сгенерировать код, и `/ux-lint`, чтобы перед коммитом проверить, что он проходит 171 детерминированное правило против AI-slop.

Этот README, каноническая справка. Каждая команда, каждый саб-агент, каждый data-манифест, каждый путь установки, каждый brand-спек, каждая категория анти-паттернов, всё задокументировано здесь. Если ты ищешь design-плагин для Claude Code или сравниваешь AI-инструменты дизайна для Cursor, Windsurf или Codex, прочитай это от начала до конца параллельно с [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Содержание

1. [Мозг, что такое v3.0](#мозг-что-такое-v30)
2. [Быстрая установка](#быстрая-установка)
3. [Цифры, live-сравнение с топ-8 UX-скилами Claude](#цифры-live-сравнение-с-топ-8-ux-скилами-claude)
4. [Архитектура, как складываются части](#архитектура-как-складываются-части)
5. [18 slash-команд, подробный справочник](#18-slash-команд-подробный-справочник)
6. [5 саб-агентов](#5-саб-агентов)
7. [11 data-манифестов](#11-data-манифестов)
8. [171 правило против AI-slop, linter](#171-правило-против-ai-slop-linter)
9. [160 brand-спеков DESIGN.md, по категориям](#160-brand-спеков-designmd-по-категориям)
10. [MCP-сервер, асимметричный ход](#mcp-сервер-асимметричный-ход)
11. [Установщик для 17 IDE](#установщик-для-17-ide)
12. [Сценарии использования, конкретные кейсы](#сценарии-использования-конкретные-кейсы)
13. [Сравнение с альтернативами](#сравнение-с-альтернативами)
14. [Roadmap](#roadmap)
15. [Как контрибьютить](#как-контрибьютить)
16. [Лицензия, автор, благодарности](#лицензия-автор-благодарности)

---

## Мозг: что такое v3.0

v3.1.0, крупнейший архитектурный сдвиг в истории ux-skill. Рекомендатор больше не выбирает шаблоны из каталога, движок **синтезирует** свежий язык дизайна на каждый бриф. Один и тот же бриф всегда даёт один и тот же вывод (полностью детерминистично), но каждый отличающийся бриф получает свою новую систему. Brand specs больше не шаблоны; это обучающие данные, из которых движок учит словарь. Система видит собственную историю, замыкает цикл обратной связи локально и никогда не вызывает LLM.

Компилятор, это **детерминистический синтезатор по 7 осям**: warmth, contrast, density, geometry, formality, motion, type_personality. Каждый бриф отображается в значения осей; значения осей компилируются в свежие palette + типографику + spacing + radius + motion-токены. Модульные типографические шкалы выбирают своё отношение из contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Примитивы лейаута адаптивны по построению (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Сломанные лейауты невозможно эмитить, потому что они не представимы.

Есть три авто-диспатчируемых режима: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% токенов Stripe, самый быстрый путь); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% адаптировано по осям от 4 родственных брендов); и `pure_synthesis` (бренд не назван → бесконечное пространство, 8 примеров с совпадающими осями дистиллированы в новый язык дизайна). Конфликты между осями разрешает документированная **матрица взаимодействия осей**, dense + corporate компилируется в 4px (побеждает density, школа Bloomberg), airy + corporate в 12px (побеждает formality, люкс), soft + playful в 18px radius, sharp + corporate в 2px. Никаких тихих ad-hoc правил в реализации.

**Журнал решений** (`.ux/decisions.jsonl`, схема `_v: 1` зафиксирована) замыкает цикл обратной связи. Рекомендатор теперь переранжирует кандидатов по прошлым победам в том же бакете `(industry, ui_type)`. Безопасен при холодном старте: при менее чем 3 предыдущих решениях пропускает переранжирование. Учитываются только решения с `lint_score >= 80` И `user_accepted = true`. Плюс `/ux-polish` гоняет lint → polish → re-lint, пока оценка ≥ 90, плато или 3 раунда, с quality gate на 65, ниже которого вывод отклоняется без `--force`. Итог: каждая установка становится умнее на своём корпусе, каждый прогон воспроизводим между машинами, а движок остаётся полностью офлайн.

---

## Быстрая установка

Три пути установки. Выбирай тот, что подходит твоей среде.

### Путь 1: marketplace Claude Code (канонический)

Если ты живёшь в Claude Code, ставь через marketplace плагинов:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Это подключает все 18 slash-команд (плюс 7 старых имён, которые остаются алиасами до 4.1) и 5 саб-агентов к твоей сессии Claude Code. После установки запусти `/ux-init`, чтобы настроить директорию состояния `.ux/` для проекта и проверить, что Python-движок доступен.

### Путь 2: pip (универсальный)

Если ты живёшь вне Claude Code (Cursor, Windsurf, CLI, CI), ставь Python-пакет:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

Пакет выставляет и `ux`, и `uxskill` как CLI-entry-point, это один и тот же бинарь.

### Путь 3: npx (без Python)

Если не хочешь управлять Python напрямую, npx-обёртка бутстрапит всё через `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Проверка установки

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

Двенадцать счётчиков в сумме дают 1 262 записи. Если какой-то счётчик возвращает 0, значит, JSON-файл отсутствует: открой issue на [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Цифры: live-сравнение с топ-8 UX-скилами Claude

Количество звёзд в последний раз сверено через `gh api` **2026-05-28**. ux-skill (Laith0003/ux-skill), новичок: мы маленькие по узнаваемости, глубокие по архитектуре. Сравнение ниже честное: где проигрываем, где выигрываем.

| Плагин | Звёзды | Архитектура | Slash-команды | Linter (CI-safe) | Brand-спеки | Компоненты | Motion-пресеты | Поддерживаемые IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83 958** | Python BM25 + CSV, одиночный skill | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54 406** | Node.js + 19 скилов + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25 202** | Bash + taste на исследовательской основе | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15 455** | Один SKILL.md на 62 КБ + скрипты | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5 762** | Библиотека скилов, подключённая через MCP | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2 391** | Skill одной эстетики | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2 164** | Anti-slop design skill | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Компоненты MD3 + аудит | 1 | - | (только MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python-движок + 12 манифестов + 18 команд + 5 саб-агентов + CI-linter** | **18** | **171 детерминированное правило** | **160** | **148** | **57** | **17** |

### Где мы проигрываем

- **Узнаваемость.** У них сотни тысяч звёзд. У нас 14. Поставь звезду, это самый дешёвый способ помочь.
- **Узнаваемость бренда.** У ui-ux-pro-max и open-design фора, измеряемая месяцами, а не днями.
- **Marketing-полировка.** У них есть скриншоты, демо-видео и findable-лендинг. У нас обстоятельный README и тощий лендинг.

### Где мы выигрываем

- **Библиотека компонентов:** 148 задокументированных компонентов с анатомией, состояниями, использованными токенами и motion-спецификациями. Никто из остальных 8 не поставляет манифест компонентов.
- **Motion-пресеты:** 57 stack-ready записей (Framer Motion, GSAP, CSS) с reduced-motion-фолбэками. Никто из остальных не поставляет motion-манифест.
- **Anti-pattern linter:** 171 детерминированное правило, работает в CI, выходит с non-zero на Critical/High. Никто из остальных не поставляет детерминированный linter.
- **Brand-спеки:** 160 реальных DESIGN.md-спеков (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude и ещё 96). Никто из остальных не поставляет brand-библиотеку.
- **17 поддерживаемых IDE:** один и тот же движок, разный клей для каждой IDE.
- **18 slash-команд:** discovery, генерация (страницы, компоненты, дашборды, по изображению), audit, lint, цикл polish, fix loop, case-study, workshop, copy, motion, a11y, conductor, полностью интегрированы.

Полный stable-by-table side-by-side на [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Архитектура: как складываются части

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

### Как движок работает на самом деле

1. **Вход.** Ты даёшь бриф: интерактивно через `/ux-discover` (10 полей) или неинтерактивно через флаги `ux recommend`.
2. **5 параллельных поисков.** Движок одновременно выполняет пять запросов по манифестам:
   - **Отрасль → recommended_styles** (industries.json)
   - **Стиль → совместимость палитры, шрифтов и motion** (styles.json)
   - **Тон × обязательные требования → фильтр палитр** (palettes.json)
   - **Стек → совместимость компонентов + motion-пресеты** (tech-stacks.json, motion-presets.json)
   - **Запреты + регион → guardrails + шорт-лист эталонных брендов** (anti-patterns.json, brands/)
3. **Слияние.** Детерминированный механизм слияния ранжирует кандидатов, разрешает конфликты (например, обязательная тёмная тема задаёт режим палитры) и выдаёт одну рекомендованную систему.
4. **Вывод.** JSON-документ с выбранным стилем, палитрой, шрифтовой парой, 5 лучшими motion-пресетами, 12 лучшими компонентами, 5 лучшими эталонными брендами и всеми 171 активными guardrails анти-паттернов. Плюс блок обоснования, который объясняет каждый выбор.
5. **Генерация.** Последующие команды (`/ux-design` в режимах страницы, компонента, дашборда и изображения, а также `/ux-system`) используют рекомендацию, чтобы сгенерировать настоящий код через саб-агентов.
6. **Проверка.** `/ux-lint` повторно сканирует сгенерированный код по 171 правилу. Выходит с non-zero на Critical/High в CI.

**Что добавила v3.** Рекомендатор теперь переранжирует кандидатов из `engine/decisions/` по `.ux/decisions.jsonl` (учитываются только решения с `lint_score >= 80` И `user_accepted = true`; безопасен при холодном старте, если предыдущих решений меньше 3). Генератор может передавать работу в `engine/synthesizer/`, детерминированный 7-осевой компилятор, который для каждого брифа выпускает свежие токены палитры + шрифтов + отступов + скруглений + motion вместо выбора шаблонов из каталога. Подробности в разделе [Мозг, что такое v3.0](#мозг-что-такое-v30).

**Python думает. HTML показывает. Markdown связывает.**

---

## 18 slash-команд: подробный справочник

Каждая команда поставляется как `.md`-файл в `commands/` с `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` и `output state file`. Описания ниже сокращены; полный исходник и есть каноническая спецификация.

Команды разбиты на семь групп: **bootstrap и инвентарь**, **discovery и рекомендация**, **генерация**, **audit и проверка**, **fix и polish**, **discovery и нарратив** и **conductor**. Семь имён из 3.x продолжают работать как [алиасы](#алиасы-удаляются-в-41) до 4.1.

### Bootstrap & инвентарь

#### `/ux-init`: bootstrap проекта

- **Что:** Определяет, какую IDE ты используешь (`.claude/`, `.cursor/`, `.windsurf/`, и т.д.), ставит правильный артефакт, проверяет, что Python-движок доступен, печатает снимок статистики. `--stats` печатает только снимок: версию + количество записей в манифестах данных.
- **Когда использовать:** Первая установка в новом проекте. После клонирования проекта, использующего ux-skill. После `pip install --upgrade uxskill`. `--stats` после установки, после обновления или когда рекомендация выдаёт неожиданный выбор и есть подозрение, что манифесты неполные.
- **Когда пропустить:** Уже запускал в этом проекте, и ничего не изменилось. `--stats` пропускать не нужно никогда: это чтение за 50мс.
- **Вызов:** `/ux-init` (без аргументов), `/ux-init --stats` или `uxskill init` / `uxskill stats` из CLI. `--decisions` добавляет сводку журнала решений; `--html` пишет `.ux/stats.html`.
- **Output:** Артефакт под IDE (см. [Установщик для 17 IDE](#установщик-для-17-ide)) + директория `.ux/` + сводка в stdout. `--stats`: JSON в stdout (см. [Проверка установки](#проверка-установки) выше).
- **Цепляется к:** `/ux-discover` следующим. `--stats` нужен только для диагностики.

#### `/ux-mcp`: запустить движок как MCP-сервер

- **Что:** Запускает движок как сервер Model Context Protocol через stdio. 25 инструментов (рекомендатор, linter, хранение состояния, синтезатор, журнал решений, извлечение из изображений, манифесты данных, а также сборка, импорт, улучшение, расширение, экспорт и проверка дизайн-системы) становятся доступны из любого MCP-совместимого хоста без плагина.
- **Когда использовать:** Ты работаешь в другом MCP-совместимом хосте и хочешь тот же движок. У тебя мультиагентный пайплайн, которому нужен единый источник дизайн-ограничений. Тебе нужен рекомендатор или linter как долгоживущий процесс в CI.
- **Когда пропустить:** Ты в Claude Code с установленным плагином; slash-команды и так достают до движка. Нужен разовый ответ; `uxskill recommend` или `uxskill lint` проще.
- **Вызов:** `/ux-mcp` или `ux-mcp` из шелла после `pip install 'uxskill[mcp]'`.
- **Output:** stdio JSON-RPC сервер. См. [MCP-сервер](#mcp-сервер-асимметричный-ход) и `commands/ux-mcp.md` для настройки под каждый клиент.
- **Цепляется к:** Ни к чему; это транспорт, а не шаг.

### Discovery & рекомендация

#### `/ux-discover`: обязательная воронка (10 полей, framing, рекомендация)

- **Что:** Обязательный опрос из 10 полей, через который проходит каждый проект перед любой командой генерации. Тип проекта, аудитория, главная цель, тон, обязательные требования, запреты, референсные бренды, стек, регион, метрика успеха. **Никакой импровизации.** Запрещённые фразы («современный», «чистый») заставляют пользователя конкретизировать. Затем запускается рекомендатор: 5 параллельных поисков Python-движка по 12 манифестам возвращают одну объединённую дизайн-систему (Отрасль → Стиль → Палитра → Шрифты → Motion + Компоненты + Эталонные бренды + Guardrails).
- **Режимы:** `--frame` фиксирует, для кого, outcome, гипотезу и сигнал успеха в framing-блоке из четырёх полей, легче полного опроса. `--recommend` запускает только рекомендатор, по сохранённому брифу или разовым флагам.
- **Когда использовать:** Перед любым `/ux-design` или `/ux-system`. Всякий раз, когда прежний бриф устарел. `--frame` в начале проекта, спринта или разовой задачи либо посреди работы, когда разговор ушёл в сторону. `--recommend`, когда перезапускаешь продукт, который выглядит уставшим.
- **Когда пропустить:** Ты чинишь баг (`/ux-fix`). Ты запускаешь только проход linter (`/ux-lint`). Бриф не менялся с прошлой сессии.
- **Вызов (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` или `/ux-discover --recommend`.
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
- **Output:** `.ux/last-discovery.json` (бриф из 10 полей), `.ux/last-recommendation.json` (выбранный стиль, палитра, шрифтовая пара, 5 лучших motion-пресетов, 12 лучших компонентов, 5 лучших эталонных брендов, все 171 активные guardrails анти-паттернов плюс обоснование) и, с `--frame`, `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Цепляется к:** `/ux-design [extra brief]` → frontend-код на основе рекомендации. `/ux-design --component <name>` → один компонент под выявленные ограничения. `/ux-system` → полная дизайн-система из рекомендации. `/ux-lint` → проверить сгенерированный код.

### Генерация

#### `/ux-design`: генерирует красивую анти-slop поверхность из брифа

- **Что:** Генерирует полный production-grade frontend-артефакт (landing, маркетинговый сайт, app shell) из discovery-брифа + рекомендации. Диспатчит `frontend-engineer` с креативным направлением из anti-slop и arsenal-референсов. Бриф или флаг выбирает один из четырёх режимов:
  - **страница** (по умолчанию): полная страница или поверхность из нескольких секций. Пишет `.ux/last-design.json`.
  - **`--component [name]`**: один production-grade компонент (кнопка, модальное окно, navbar, sidebar, карточка, таблица, форма, график). Все четыре состояния взаимодействия, доступный, в стиле бренда. Сначала ищет компонент в `.ux/last-recommendation.json`, затем обращается к манифесту напрямую. Пишет `.ux/last-component.json`.
  - **`--dashboard`**: дисциплина плотности данных, bento-лейаут, табличные моноширинные цифры, sparkline-паттерны, без злоупотребления карточками, семантические цвета состояний, скупой motion. Не маркетинговый сайт с приклеенными графиками. Пишет `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: читает референсное изображение (PNG/JPG/WebP) средствами чистого компьютерного зрения на Pillow (доминирующая палитра, полярность фона, типографический сигнал), сопоставляет его с манифестами палитр и стилей и строит по полученной рекомендации. `--extract-only` останавливается после извлечения. Пишет `.ux/last-image-extract.json`.
- **Когда использовать:** «Design a», «build me a», «generate a landing page», «create a dashboard», «make a component», «build a button», «design the admin panel», «operator console», «KPI board», «build it like this screenshot», любой free-form запрос визуального deliverable.
- **Когда пропустить:** Нужен ревью, а не сборка (используй `/ux-audit` или `/ux-critique`). Backend или инфраструктурная работа.
- **Вызов:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Output:** Сгенерированный код (HTML / Blade / JSX / Vue / Astro) плюс файл состояния режима.
- **Цепляется к:** `/ux-lint` → проверка против guardrails. `/ux-polish` → косметический проход. `/ux-a11y` → аудит доступности. `/ux-copy` → ревью microcopy. `/ux-fix` → применить findings атомарными коммитами.

#### `/ux-system`: генерирует полную стартовую design-систему

- **Что:** Предлагает полную стартовую design-систему для проекта, у которого её нет, токены (цвет, тип, пространство, motion, радиус, тень), foundation-документы, контракты компонентов, dark-mode-сопряжения, theme switcher. Диспатчит `design-system-architect`.
- **Когда использовать:** «We don't have a design system», «build us a system», «propose tokens», «what should our theme be», «set up our DS».
- **Когда пропустить:** У проекта уже есть дизайн-система; используй вместо этого `/ux-design --component` поверх существующей системы. Backend или инфраструктура.
- **Вызов:** `/ux-system create` (движок основ), `/ux-system enhance --from <file>` (измерить систему, которая у тебя уже есть), `/ux-system extend --from <file> --add <foundation>` (дополнить её, не меняя) или `/ux-system` (поток из 3.x; сначала запускает discovery, если брифа ещё нет).
- **Output:** `tokens.json`, `foundations.md`, контракты `components/*.md`, опциональный emit Tailwind / vanilla / SCSS. Пишет `.ux/last-system.json` для цепочечного контекста.
- **Цепляется к:** `/ux-design --component` → строить поверх новой системы. `/ux-design` → сгенерировать поверхность на новых токенах.

#### `/ux-motion`: обработка motion

- **Что:** Генерирует motion-слой поверхности, длительности, easing, хореографию, reduced-motion-фолбэки, perf-дисциплину. Также аудитирует существующий motion против 5 измерений (timing, easing, смысл, reduced-motion, performance).
- **Когда использовать:** «Motion check», «are the animations good», «fix the motion», «review the animations», «motion audit», «performance pass on the motion».
- **Когда пропустить:** Поверхность не имеет motion (используй `/ux-audit` или `/ux-polish`). Backend или инфраструктура.
- **Вызов:** `/ux-motion path/to/component.tsx` (режим аудита) или `/ux-motion --generate hero-entry` (генерация).
- **Output:** Обновлённый код (в режиме генерации) или отчёт `.ux/last-motion.json` (в режиме аудита).
- **Цепляется к:** `/ux-fix` → применить motion-findings. `/ux-polish` → подтянуть.

### Audit & верификация

#### `/ux-lint`: детерминированный regex-based linter (без LLM, CI-safe)

- **Что:** Запускает 171 правило против твоего кода. Никакого вызова LLM. Выходит с non-zero на Critical / High в CI. Источник: `data/anti-patterns.json`. Правила покрывают A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).
- **Когда использовать:** Pre-commit хук. CI gate. Быстрый первый проход по большой кодовой базе перед тратой на `/ux-audit`. После `/ux-design` в любом режиме для проверки генерации.
- **Когда пропустить:** Хочешь fix loop (linter отчитывается, не редактирует, цепляй в `/ux-polish --fix` или `/ux-fix`). Хочешь taste-суждение (используй `/ux-critique`).
- **Вызов (slash):** `/ux-lint src/`.
- **Вызов (CLI):** `uxskill lint .` или `python3 bin/ux-lint.py .` или `bash bin/ux-lint.sh --ci --fail-on high`.
- **Вызов (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Findings в stdout (локация, id правила, severity, evidence). Exit code 0, если чисто, non-zero на Critical/High, когда установлен `--fail-on high`.
- **Цепляется к:** `/ux-polish --fix` → LLM-driven контрпартнёр на тех же паттернах. `/ux-fix` → применить findings коммитами, отсортированными по severity. `/ux-audit` → полный 6-линзовый проход рассуждения. `/ux-next` → пусть conductor решит.

#### `/ux-audit`: 6-линзовый design-аудит

- **Что:** Структурированный, мнение-имеющий ревью против шести линз (ясность, иерархия, доступность, голос, motion, taste), производящий severity-помеченные findings. Polaris-стиль отчёта. Сначала читает `.ux/last-frame.json`, аудитория и outcome закрепляют severity каждого finding.
- **Когда использовать:** Поверхность существует, и тебе нужна защитимая критика. «Audit», «review the ux», «is this any good», «what's broken», «tear this apart».
- **Когда пропустить:** Поверхность ещё не существует (используй `/ux-design`). Пользователь хочет одну линзу (используй целевую команду: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Пользователь хочет taste-мнение (используй `/ux-critique`). Backend или инфраструктура.
- **Вызов:** `/ux-audit https://example.com/pricing` или `/ux-audit src/components/Pricing.tsx`.
- **Output:** Пишет `.ux/last-audit.json`, массив `findings` из `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Цепляется к:** `/ux-fix` → применить findings. `/ux-polish` → косметический проход. `/ux-design` → если нужен структурный редизайн.

#### `/ux-a11y`: WCAG 2.1 AA аудит + проверки общей вежливости

- **Что:** Структурированный WCAG 2.1 AA аудит, плюс проверки общей вежливости, которые проходят автоматические инструменты, но всё равно вредят реальным пользователям (видимость фокуса, специфичность ошибок, motion-предпочтения, ловушки клавиатуры, опора на цвет).
- **Когда использовать:** Pre-ship гейт доступности. После редизайна. «Accessibility check», «WCAG audit», «is this accessible», «a11y review», «screen reader test», «keyboard nav check».
- **Когда пропустить:** Не user-facing. Backend или инфраструктура. WIP-наброски.
- **Вызов:** `/ux-a11y https://example.com` (предпочтителен live URL, автоматические инструменты и keyboard-тестирование работают только в live).
- **Output:** Пишет `.ux/last-a11y.json`, массив `findings` из `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, массив `beyond_wcag`, `severity_counts`.
- **Цепляется к:** `/ux-fix` → применить findings коммитами. `/ux-copy` → починить alt-текст и wiring ошибок форм в рамках copy-прохода.

#### `/ux-critique`: taste-выбор (3 выигрыша, 3 промаха, 1 стратегический ход)

- **Что:** Мнение дизайнера, не структурный аудит, не severity-оценка, а просто плотное, мнение-имеющее take, которое называет, что работает, что нет, и тот единственный стратегический ход, который изменит больше всего.
- **Когда использовать:** «What do you think», «is this good», «critique this», «honest take», «is the vibe right», «does this feel like us», «should we ship this».
- **Когда пропустить:** Пользователь явно хочет структурный аудит (используй `/ux-audit`). Backend или инфраструктура.
- **Вызов:** `/ux-critique https://example.com`.
- **Output:** Пишет `.ux/last-critique.json`, 3 выигрыша, 3 промаха, 1 стратегический ход, плюс проза.
- **Цепляется к:** `/ux-design`, если take рекомендует редизайн. `/ux-polish`, если take рекомендует подтянуть.

#### `/ux-copy`: ревью microcopy + переписывание

- **Что:** Оценивает каждую видимую строку против voice-рубрики и производит before/after переписывание. Ловит: «form contains errors» (общее), «John Doe» (заполнитель), AI-весёлая праздничная copy, общие CTA, мёртвые empty states, бесполезные ошибки.
- **Когда использовать:** Структура правильная, но слова слабы. «Review the copy», «fix the microcopy», «the error messages are bad», «rewrite this», «tighten the strings», «the buttons sound generic», «this empty state is dead».
- **Когда пропустить:** Проблемы лейаута (используй `/ux-audit` или `/ux-polish`). Copy-проблемы, вызванные доступностью, как alt-текст (используй `/ux-a11y`). Backend или инфраструктура.
- **Вызов:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Пишет `.ux/last-copy.json`, массив `strings` из `{location, severity, before, after, notes}`, плюс рубрика + локали, требующие перевода.
- **Цепляется к:** `/ux-fix` → применить переписывания. `/ux-a11y` → перепроверить после copy-починок.

### Fix & polish

#### `/ux-fix`: применить findings атомарными коммитами

- **Что:** Читает последний отчёт из `.ux/` (audit, copy, a11y, motion или polish), валидирует рабочее дерево и применяет findings атомарными коммитами через правильных саб-агентов. Перепроверяет, перезапуская исходную команду.
- **Когда использовать:** После запуска команды audit-класса и ревью findings. «Fix the findings», «apply the fixes», «run the fix loop», «patch the surface», «make the changes», «go fix it».
- **Когда пропустить:** Нет предыдущего отчёта в `.ux/`. Рабочее дерево грязное, и пользователь не согласился stash/commit. Починки требуют design-суждения, а не механического применения (используй `/ux-design` для редизайна).
- **Вызов:** `/ux-fix` (автоопределяет, какой отчёт чинить) или `/ux-fix --from=last-a11y.json`.
- **Output:** Атомарные коммиты на finding. Перезапускает исходную команду и обновляет файл `.ux/last-*.json`. Печатает сводку.
- **Цепляется к:** `/ux-next` → conductor выбирает следующий ход.

#### `/ux-polish`: цикл lint, fix, re-lint + удаление AI-slop

- **Что:** Сначала детерминированный цикл над локальным HTML-файлом: lint, шесть идемпотентных проходов полировки, re-lint, пока оценка не дойдёт до 90, не выйдет на плато или не пройдут три раунда (`--rounds` меняет предел). По умолчанию результат цикла остаётся в `<file>.evolved.html`, а оригинал не трогается. Заменить оригинал могут только `--loop-only` или `--fix`, после проверки чистого рабочего дерева, а quality gate на 65 не даёт провалившемуся результату заменить его без `--force`; с `--brand-file` порог верности бренду действует на каждом выходе. Затем проход вкуса: ритм отступов, более чёткая иерархия, детекция AI-slop, согласованность токенов. LLM-driven контрпартнёр `/ux-lint`, который опирается на твоё суждение в вопросах вкуса. `--loop-only` запускает только цикл; `--no-loop` только проход вкуса; `--fix` применяет замечания по вкусу.
- **Когда использовать:** Структура правильная, но исполнение рыхлое. «Polish», «tighten this up», «remove the AI-slop», «make it premium», «make this less AI-looking», «the spacing feels off», «this looks generic», «needs more taste», «improve until score 90+», «make it ship-ready».
- **Когда пропустить:** На поверхности не хватает базовой функциональности (сначала исправь это). Нужен редизайн, а не полировка (используй `/ux-design`). Проблемы с текстами (используй `/ux-copy`). Проблемы с анимацией (используй `/ux-motion`). Проблемы a11y (используй `/ux-a11y`).
- **Вызов:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Output:** `<file>.evolved.html` из цикла (заменяет оригинал только с `--loop-only` или `--fix`), обновлённый код с `--fix`, `.ux/last-evolve.json`, одна строка в `.ux/decisions.jsonl` и `.ux/last-polish.json` с описанием замечаний по вкусу.
- **Цепляется к:** `/ux-lint` → проверить, что полировка удержалась. `/ux-a11y` → повторно проверить доступность.

### Discovery & нарратив

#### `/ux-research`: планирование исследования + синтез

- **Что:** Режим планирования: пишет скрипты интервью, опросы, скринеры рекрутинга. Режим синтеза (`--synthesize`): переваривает интервью, аналитику, сайты конкурентов, A/B-результаты, support-тикеты в рекомендации. Диспатчит `research-synthesizer`.
- **Когда использовать:** «Plan a research study», «I need interview questions», «design a survey», «how do I recruit users», «user testing plan», «diary study», «preference test», «fake door», «smoke test», «synthesize my interview notes».
- **Когда пропустить:** Ответ уже известен с высокой уверенностью. Низкорисковые обратимые решения. Backend или инфраструктура.
- **Вызов:** `/ux-research --plan "loyalty wallet adoption in MENA"` или `/ux-research --synthesize interviews/*.md`.
- **Output:** Пишет `.ux/last-research.json`, research-план или синтезированные темы + evidence + рекомендации.
- **Цепляется к:** `/ux-discover --frame` → встроить находки во frame. `/ux-design` → генерировать по находкам. `/ux-workshop` → провести воркшоп с исследованием на входе.

#### `/ux-workshop`: 5-фазный workshop design-thinking

- **Что:** Фасилитирует discovery / design-thinking workshop end-to-end. Пять последовательных фаз (исследование → heat map → stakeholder map → решение-набросок → game plan). Тайм-боксы. Конкретные артефакты на каждую фазу. Заканчивается решением, а не «интересными находками».
- **Когда использовать:** Реальный вопрос, реальные участники, реальный временной бюджет. «Run a workshop», «facilitate a discovery», «let's do a design thinking session», «I have stakeholders for an hour, what do we do», «kick off the project».
- **Когда пропустить:** Бриф уже ясен и очерчен. Сольный брейншторм (используй `/ux-design` или `/ux-discover --frame`). Команда в разгаре исполнения, а не на этапе discovery.
- **Вызов:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Пишет `.ux/last-workshop.json`, game plan + артефакты по фазам.
- **Цепляется к:** `/ux-design` → исполнить game plan. `/ux-research` → закрыть пробелы, которые всплыл воркшоп. `/ux-case-study` → опубликовать путь.

#### `/ux-case-study`: публикуемый case study (формат Wfrah-editorial)

- **Что:** Генерирует кейс проекта в чисто монохромном редакционном формате: типографика Wfrah, тонкие разделители, пронумерованные коды секций от (A) до (G), раскладка, безопасная для двуязычного текста. Документ, а не маркетинговая брошюра. Читает из `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Когда использовать:** Пост-лонч. После дискретной вехи. «Write a case study», «case study this project», «do the wrap-up doc», «publish this work», «portfolio piece».
- **Когда пропустить:** У проекта нет данных, чтобы заполнить секции от (A) до (G). Пользователю нужен маркетинговый лендинг, а не кейс (используй `/ux-design`).
- **Вызов:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Цепляется к:** Терминальная команда, обычно конец проекта.

### Conductor

#### `/ux-next`: дирижёр workflow (read-only)

- **Что:** Читает каждый `.ux/last-*.json` и называет следующую команду с самым высоким рычагом. Дирижёр, не строитель. Read-only.
- **Когда использовать:** Между командами. «What should I do next», «what's the next move», «decide for me», «where do we go from here».
- **Когда пропустить:** Нет предыдущих отчётов в `.ux/`. У тебя в голове конкретная следующая команда.
- **Вызов:** `/ux-next` (без аргументов) или `/ux-next --focus=a11y`.
- **Output:** Stdout, рекомендованная следующая команда + rationale.
- **Цепляется к:** Какую бы команду она ни выбрала.

#### `/ux-expert`: крючок для консалтинга

- **Что:** Выводит контактную инфу создателя плагина, когда пользователь просит реального UX-эксперта. Кратко, прямо, без маркетинга.
- **Когда использовать:** «Who built this», «I need a UX expert», «do you do consulting», «can I hire someone for this», «is there a human behind this plugin».
- **Когда пропустить:** Пользователь спрашивает про фичи плагина, а не про консалтинг.
- **Вызов:** `/ux-expert`.
- **Output:** Краткая контактная карточка с LinkedIn / email / репо.

### Алиасы, удаляются в 4.1

Семь команд из 3.x слились в 18 команд выше. Их имена работают ещё один релиз: каждый алиас сообщает, куда он переехал, и затем запускает новую команду с теми же аргументами.

| Старая команда | Теперь | Примечания |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | Тот же framing-блок, тот же `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | MCP-инструмент `ux_recommend` не меняется |
| `/ux-stats` | `/ux-init --stats` | Снимок только для чтения |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | Алиас сохраняет старый предел в пять раундов; `/ux-polish` сам по себе останавливается на трёх |
| `/ux-component` | `/ux-design --component` | Тот же `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | Тот же `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Убери `--extract-only`, чтобы строить по изображению |

### Граф цепочек команд

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

## 5 саб-агентов

Саб-агенты представляют собой генераторы под конкретную роль, которых диспатчат команды. Они никогда не работают самостоятельно: их вызывают `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research` и т.д. У каждого агента чёткая зона ответственности: он НЕ решает, каким быть брифу; он его исполняет.

### `frontend-engineer`

- **Владеет:** Production-grade frontend-кодом (React, Next.js, Vue, Blade+Alpine, ванильный HTML, Astro) с анти-AI-slop дисциплиной.
- **Диспатчится:** `/ux-design` (режимы страницы, компонента, дашборда и изображения), `/ux-fix`.
- **Входы:** Бриф + креативное направление + токены (из `.ux/last-recommendation.json`).
- **Выходы:** Рабочий код, отличимый от общего AI-вывода. Никаких фиолетовых градиентов, никакого центрированного hero, никаких трёх одинаковых карточек, никакого Inter в display-размере, никакого «John Doe», никаких emoji, никаких дефолтов 300мс.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Владеет:** Motion в production frontend-коде, Framer Motion, GSAP, CSS-анимации. Длительности, easing, хореография, reduced-motion-фолбэки, perf-дисциплина.
- **Диспатчится:** `/ux-design` (любой режим), `/ux-motion --fix`.
- **Входы:** Motion-бриф + токены + 57 motion-пресетов из `data/motion-presets.json`.
- **Выходы:** Motion, заслуживший своё место. Всегда обёрнут в `prefers-reduced-motion`-фолбэки. Всегда протестирован против Core Web Vitals.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Владеет:** Строками, которые уходят в продакшен, сообщения об ошибках, empty states, CTA, состояния загрузки, success-сообщения, тосты, текст-подсказки, лейблы форм, текст кнопок.
- **Диспатчится:** `/ux-copy --fix`, `/ux-design` (любой режим), `/ux-discover --frame`.
- **Входы:** Voice-профиль (названный или вставленный) + строки поверхности.
- **Выходы:** Production-microcopy, применяемая последовательно через каждое состояние поверхности, чтобы продукт звучал как один продукт, а не десять. Запрещено: «form contains errors», «John Doe», AI-весёлая праздничная copy, общие CTA, мёртвые empty states.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Владеет:** Перевариванием research-входов (интервью, аналитика, сайты конкурентов, A/B-результаты, support-тикеты) в действенные design-рекомендации.
- **Диспатчится:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Входы:** Сырое исследование, транскрипты, экспорты, URL'ы конкурентов, support-кластеры.
- **Выходы:** Темы, evidence, рекомендации. Никогда не дизайнит ответ, даёт дизайнеру субстрат, от которого дизайнить.
- **Инструменты:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Владеет:** Полными design-системами, токены (цвет, тип, пространство, motion, радиус, тень), foundation-документы, контракты компонентов, dark-mode-сопряжения, theming-слой.
- **Диспатчится:** `/ux-system`, `/ux-design --component`, когда системы ещё нет.
- **Входы:** Бренд-бриф + `.ux/last-recommendation.json` (стиль + палитра + типографическая пара + motion-пресеты).
- **Выходы:** Связная, мнение-имеющая, production-ready система, на которой downstream-агенты могут строить, не переопределяя фундаментал. Токены JSON, foundations MD, контракты компонентов, dark-mode-маппинг.
- **Инструменты:** `Read, Write, Edit, Bash, Glob, Grep`.

### Протокол диспатча саб-агентов

Когда команда диспатчит саб-агента, она передаёт:

1. Бриф / рекомендацию (загруженные из `.ux/`).
2. Релевантный срез манифеста (например, `frontend-engineer` получает выбранный стиль + палитру + компоненты; `motion-engineer` получает выбранные motion-пресеты).
3. 171 guardrail анти-паттернов (всегда активны).
4. Критерий успеха (что артефакт должен делать).

Саб-агенты возвращают:

1. Артефакт (код, документ, система).
2. Блок rationale (почему эти выборы).
3. Self-check против guardrails (какие правила они верифицировали).

Вызывающая команда затем автоматически запускает `/ux-lint` перед объявлением готовности.

---

## 11 data-манифестов

Слой данных, это мозг. Каждая команда читает из него; движок мёрджит через него; linter сканирует против него. Все файлы живут в `data/` и оборачивают записи в `{_meta, entries}` для версионирования схемы.

### `styles.json`: 84 design-стиля

| Поле | Описание |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, и т.д. |
| `sample entry` | `swiss-international`, «Сетка, это закон. Типографика делает тяжёлую работу. Декорация, это провал.» |

Используется: `/ux-discover`, `/ux-system`, `/ux-design`. Схема: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 цветовых палитр

| Поле | Описание |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, и т.д. |
| `sample entry` | `claude-warm-editorial`, light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Используется: `/ux-discover`, `/ux-system`. Контраст проверен на AA / AAA. Схема: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 типографических пар

| Поле | Описание |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + веса + источник + лицензия + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

У всех гарнитур есть лицензия + URL источника. Используется: `/ux-discover`, `/ux-system`.

### `components.json`: 148 компонентов

| Поле | Описание |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, 6-частная анатомия, 4 состояния |

Это наш самый большой ров. Никакой другой UX-плагин для Claude не поставляет структурный манифест компонентов.

### `industries.json`: 184 правила индустрий

| Поле | Описание |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, и т.д. |
| `sample entry` | `fintech-neobank`, высокое доверие, регуляторные раскрытия, primary-UI баланса/транзакций, mobile-first ежедневное использование |

Используется рекомендатором (`/ux-discover`) как первая ось параллельного поиска.

### `chart-types.json`: 35 типов графиков

| Поле | Описание |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, сравнивает от 4 до 15 дискретных категорий. Позиция по оси x кодирует категорию, высота кодирует значение. |

Используется `/ux-design --dashboard` и `/ux-design --component` (экземпляры графиков).

### `tech-stacks.json`: 25 стеков

| Поле | Описание |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, совместим с Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Другие стеки включают Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 именованных UX-законов

| Поле | Описание |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, и т.д. |
| `sample entry` | `hicks-law`, Время решения растёт логарифмически с количеством представленных выборов |

Используется `/ux-audit` (6-линзовый scoring) и `/ux-critique` (taste-якорь).

### `motion-presets.json`: 57 motion-пресетов

| Поле | Описание |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion-фолбэк), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

У каждого пресета есть reduced-motion-вариант. Stack-ready код для Framer Motion, GSAP и чистого CSS.

### `anti-patterns.json`: 171 правило

| Поле | Описание |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (тип, паттерн, флаги, область и у многих правил проверка `post` по разобранному файлу), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

Полный список правил в разделе [171 правило против AI-slop](#171-правило-против-ai-slop-linter).

### `brands/*.json`: 160 brand-спеков

| Поле | Описание |
|---|---|
| `entries` | 160 (плюс `_index.json`, листающий все) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Полный список в [160 brand-спеков DESIGN.md](#160-brand-спеков-designmd-по-категориям).

---

## 171 правило против AI-slop: linter

ux-skill поставляет детерминированный linter: каждое правило представляет собой паттерн, а многие добавляют проверку по разобранному CSS и разметке, так что совпадение засчитывается только в том контексте, который правило называет. **Без LLM.** **Без API.** **Без сети.** Работает в CI за ~200мс на типичном Next.js-приложении. Выходит с non-zero на находках Critical / High, если задан `--fail-on high`.

Правила берутся из `data/anti-patterns.json` (v2, предпочтительно) с запасным вариантом `references/foundations/anti-patterns.md` (v1, bash). Поставляются два бинарника: `bin/ux-lint.py` (Python, быстрый, расширяемый) и `bin/ux-lint.sh` (Bash + perl-PCRE, для окружений без Python).

### Правила по категориям

Полный каталог всех 171 правил, по категориям и затем по серьёзности, генерируется из `data/anti-patterns.json` в [английском README](README.md#rules-by-category); там идентификаторы и названия правил приведены так, как их печатает linter. Правила покрывают A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### Использование linter'а

**Разовый scan:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 brand-спеков DESIGN.md: по категориям

Реальные бренды. Реальные design-языки. Реальные DESIGN.md-спеки, не общие палитры. Скажи плагину «собери лендинг в стиле Stripe», и он читает реальный bran-словарь: voice-рубрика, color-токены, motion-конвенции, signature-ходы, anti-ходы.

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

Остальные 8 популярных UX-плагинов для Claude генерируют «modern minimal» или «clean dashboard», варианты одной и той же дефолтной эстетики. ux-skill позволяет просить **ясность Linear**, **серьёзность Stripe**, **сдержанность Apple**, **монолит Tesla**, **дружелюбие Notion**, **gradient-дисциплину Cursor**, **hairline-плотность Raycast**, **тёплый editorial Claude**, и движок тянет правильные токены, voice, motion-конвенции и signature-ходы из brand-спеки.

---

## MCP-сервер: асимметричный ход

ux-skill поставляет **сервер Model Context Protocol**. Запусти `ux-mcp`, и движок становится долгоживущим stdio-процессом, который может вызывать любой MCP-совместимый хост (Claude Desktop, Cursor, Windsurf, обычные агенты). 25 инструментов: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Те же Python-обработчики, что используют slash-команды; те же манифесты данных; тот же детерминированный рекомендатор.

**Почему это асимметричный ход:** ни один из топ-8 UX-скилов Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) не поставляет MCP-сервер. Они заперты внутри runtime'а плагинов Claude Code. ux-skill достижим из любого хоста, говорящего на MCP, включая агентов, которые никогда не слышали о плагине Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Направь своего клиента на бинарь `ux-mcp`. Полная документация инструментов, JSON-примеры и конфиги для клиентов Claude Desktop, Cursor и Windsurf живут на [docs/mcp.html](docs/mcp.html) и в `commands/ux-mcp.md`.

---

## Установщик для 17 IDE

`uxskill init` (или `/ux-init` внутри Claude Code) автоопределяет, какую IDE ты используешь, и пишет правильный артефакт. Один и тот же Python-движок. Те же рекомендации. Разный клей для каждой IDE.

| IDE / инструмент | Сигнал детекции | Установленный артефакт |
|---|---|---|
| Claude Code | `.claude/` или `CLAUDE.md` | Манифест плагина в `.claude-plugin/plugin.json` + все 18 команд (и 7 алиасов) + все 5 саб-агентов |
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

В каждой IDE те же CLI-команды `uxskill recommend` / `uxskill lint` / `uxskill stats` работают из терминала. Python-движок, источник истины; IDE-артефакты, тонкие prompt-header'ы, маршрутизирующие в него.

---

## Сценарии использования: конкретные кейсы

Восемь реальных сценариев. Выбери ближайший к твоей ситуации и адаптируй вызов.

### 1. Сборка fintech-dashboard в Cursor

Ты в Cursor работаешь над dashboard'ом MENA-необанка. Ты ставишь плагин и запускаешь discovery, рекомендацию, затем генерацию dashboard'а.

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

/ux-discover --recommend
> [returns picked style, palette, type pair, motion presets, components, brand exemplars]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer generates the page]

/ux-lint .
> [passes, Stripe brand spec was respected]
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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Три команды, одна отполированная поверхность, атомарные коммиты на починку.

### 5. Дизайн Linear-стилевой command palette

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

Сгенерированный компонент использует реальные цветовые токены Linear, type-stack, motion-конвенции, hairline-плотности, не «общий dark UI».

### 6. Запуск 90-минутного design-thinking воркшопа со стейкхолдерами

У тебя комната с 5 людьми на 90 минут. Ты хочешь, чтобы они ушли с game plan'ом, не с vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Плагин фасилитирует пять фаз (исследование → heat map → stakeholder map → решение-набросок → game plan) end-to-end, в тайм-боксах, с конкретными per-phase артефактами. Output, `.ux/last-workshop.json`, game plan, не просто «интересные находки».

### 7. Написание публикуемого case study после лонча

Ты задеплоил loyalty-кошелёк. Тебе нужен кусок для портфолио.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

Case study, это законченный, публикуемый артефакт, не черновик. Чистая монохромия, editorial-типографика, готов отгружать в портфолио.

### 8. Запуск discovery в non-AI контексте (только структурный intake)

Ты скопируешь проект. Тебе пока не нужна рекомендация, тебе нужен структурный бриф.

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

Ты можешь передать JSON команде, вставить в Notion-документ или подать в отдельный AI-инструмент. ux-skill, это также инструмент структурного intake, в дополнение к тому, что он движок.

### 9. MASTER.md persistence: твои design-решения в репо

После `/ux-discover` (или `/ux-discover --recommend`) сохрани выбранный стиль + палитру + шрифты + motion + компоненты + эталонные бренды + guardrails в читаемый Markdown-файл, который твоя команда может ревьюить, сравнивать и держать под контролем версий.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Пишет `.ux/design-system/MASTER.md` (YAML-frontmatter + body) и `.ux/design-system/pages/<name>.md` на каждую сгенерированную поверхность через `persist save-page`. Идемпотентно, тот же вход даёт байт-идентичный выход, так что перезапуск на неизменном состоянии, это no-op в git.

---

## Сравнение с альтернативами

Краткая сводная таблица. Полное сравнение таблица за таблицей на [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Измерение | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash-команды | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Компоненты | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion-пресеты | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand-спеки | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Правила анти-паттернов | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-safe детерминированный linter | **да** | нет | нет | нет | нет | нет | нет | нет | нет |
| Поддерживаемые IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery-gate | **10 полей** | неявный | неявный | неявный | неявный | неявный | неявный | неявный | неявный |
| Цепь состояний `.ux/` | **да** | нет | нет | нет | нет | нет | нет | нет | нет |
| Звёзды (2026-05-28) | 14 | 83 958 | 54 406 | 25 202 | 15 455 | 5 762 | 2 391 | 2 164 | 955 |

### Честная оценка

- **ui-ux-pro-max** больше по узнаваемости, поставляет 18 IDE, имеет BM25-стилевой поиск по своему CSV. Не поставляет манифест компонентов, манифест motion, brand-библиотеку или детерминированный linter.
- **open-design** имеет 19 скилов + preview, но только поддержку Claude Code и никакого anti-slop слоя.
- **hallmark** ближайший по духу (тоже anti-slop), но это один скил, нет движка, нет манифестов, нет цепочечных команд.
- **material-3-skill** отличен, если ты специально хочешь Material Design 3. Мы не конкурируем по MD3.

Полные детали по каждому измерению см. [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

Дальше, без привязки к релизу:

- **Стили Figma**: стили эффектов для теней, стили сеток и текстовые стили, привязанные к переменным полей, записанные в живой файл.
- **Сопоставление компонентов**: компонент Figma с его вариантами сопоставляется с компонентом в коде и его props и сохраняется на всём пути передачи в разработку.
- **Импорт с живого сайта**: прочитать систему, которую опубликованный сайт действительно рендерит, рядом с импортом из файлов.
- **Страницы документации для построенной системы**: человеческий взгляд на её токены, роли и контракты.

Также в работе:

- **`uxskill lint --fix` для безопасных правок** механически исправимых находок (button-no-type, img-no-alt с пустой строкой, удаление console-log-leak).
- **Расширение для VS Code**, которое показывает находки linter прямо в коде.
- **Генерация кода по компонентам** в шести стеках (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, ванильный HTML/CSS).
- **Маркетплейс бренд-спецификаций**: публиковать и находить бренд-спецификации сообщества.
- **Собственные правила анти-паттернов**: поиск и обмен правилами, которые проекты задают в `data/anti-patterns.local.json`.
- **`uxskill plan`**: планирование многостраничных сайтов по брифу, а не только одной поверхности.

---

## Как контрибьютить

Issue и PR приветствуются. Три области высокого рычага:

### Добавить правило анти-паттерна

1. Отредактируй `data/anti-patterns.json`, добавь запись с `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Добавь тест в `tests/linter/`, один файл, триггерящий правило, один, нет.
3. Запусти `uxskill lint tests/linter/should-trigger/<rule>.tsx`, подтверди, что срабатывает. Запусти на `tests/linter/should-not-trigger/<rule>.tsx`, подтверди, что нет.
4. Открой PR.

### Добавить brand-спеку

1. Создай `data/brands/<slug>.json` с `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Добавь соответствующую прозу в `references/brands/<slug>.md`.
3. Зарегистрируй в `data/brands/_index.json`.
4. Открой PR. Спека должна быть подкреплена ссылками на первоисточники (реальный продукт бренда, публичная design-система или DESIGN.md, если они его публикуют).

### Добавить motion-пресет

1. Отредактируй `data/motion-presets.json`, добавь запись с `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. У пресета должен быть reduced-motion вариант. Никаких исключений.
3. Открой PR.

### Процесс

- Прочитай [CONTRIBUTING.md](CONTRIBUTING.md) для полного процесса.
- Прочитай [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Новые правила и brand-спеки ревьюются на: привязку к первоисточнику, отсутствие overfitting к одному проекту, отсутствие emoji в любых данных, RTL-safe поведение, где применимо.

---

## Лицензия, автор, благодарности

### Лицензия

MIT. Используй, форкай, строй сверху. Если это спасло тебя от отгрузки AI slop, поставь звезду репо, это самый дешёвый способ поддержать.

### Автор

**Laith Aljunaidy**: solo founder [Dot](https://thedotwallet.com), MENA-first loyalty-платформы. Строит ux-skill, чтобы AI-сгенерированный frontend не выглядел весь одинаково.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Репо: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Сайт: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Благодарности

- Команде Anthropic за Claude Code и архитектуру skill / plugin, сделавшую это распространяемым.
- Nielsen Norman Group, Laws of UX (lawsofux.com) и UX-research community, чьи работы информируют `data/ux-guidelines.json`.
- Каждому бренду, перечисленному в `data/brands/`, их публичные design-системы являются источником истины для brand-спеков.
- Оригинальным контрибьюторам v1: single-shot Claude skill, ставшему семенем для v2 Python-движка.
- 8 популярным UX-плагинам Claude, с которыми мы сравнивались, они подняли планку; это наш ответ.

---

**ux-skill** · **v4.0.0** · Построено так, чтобы Claude Code, Cursor, Windsurf и любой другой AI-инструмент кодинга выдавали frontend, который не читается как AI-сгенерированный.

> Поставь звезду репо на [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Установи через `pip install uxskill` или `npx uxskill init` · Изучи сравнение на [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
