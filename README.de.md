[English](README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [中文](README.zh.md) · [Français](README.fr.md) · **Deutsch**

# ux-skill — die Design-Intelligence-Engine für Claude Code, Cursor und alle anderen KI-Coding-Werkzeuge

> **Das stärkste UX-Plugin für KI-Coding.** Ein Python-Reasoning-Kern mit 11 abfragbaren JSON-Manifesten (84 Styles, 176 Paletten, 70 Typographie-Paarungen, 148 Komponenten, 184 Branchen, 35 Diagrammtypen, 57 Motion-Presets, 112 UX-Gesetze, 100 Anti-Pattern-Regeln, 25 Tech-Stacks, 110 Brand-Specs), 22 Slash-Befehle, 5 Sub-Agents und ein deterministischer Anti-KI-Slop-Linter. Cross-IDE: ausgeliefert für Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer und Roo Cline.

> **Der Markenname lautet `ux-skill`.** Der PyPI- / npm-Paketname bleibt `uxskill`. Das GitHub-Repository liegt unter [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Website:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Vergleich gegen jedes Claude-UX-Plugin:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-2.0.0--alpha.1-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#der-installer-für-17-ides)
[![Brands](https://img.shields.io/badge/brand_specs-110-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-100-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Star-Historie

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Was ist ux-skill

ux-skill ist eine **Design-Intelligence-Engine** für KI-Coding-Werkzeuge. Sie läuft als Python-Paket (`pip install uxskill`), als Claude-Code-Plugin und als Multi-Installer für 17 IDEs. Die Engine nimmt ein Projekt-Brief entgegen (Branche, Zielgruppe, Tonalität, Must-haves, verbotene Mittel, Stack, Region) und liefert ein vollständiges empfohlenes Designsystem zurück: Style, Palette, Typographie-Paar, Motion-Presets, Komponenten, exemplarische Marken zum Studieren und die Anti-Pattern-Leitplanken, die einzuhalten sind. Die Empfehlung ist deterministisch — dieselbe Eingabe erzeugt stets dieselbe Ausgabe.

Das Plugin sitzt zwischen Ihnen und dem KI-Coding-Werkzeug. Wenn Sie Claude Code, Cursor oder einen anderen KI-Assistenten bitten, „eine Fintech-Landingpage zu bauen", improvisiert der Assistent typischerweise — und das Ergebnis wirkt innerhalb von fünf Sekunden KI-generiert (Violett-zu-Blau-Verläufe, drei gleiche Karten, Inter in Display-Größe, „John Doe" in den Testimonials, 300-ms-Standardübergänge, zentrierter Hero, hüpfende Pfeil-CTAs). ux-skill ersetzt Improvisation durch **strukturierte Einschränkungen**: Sie führen `/ux-discover` aus, um das Brief zu erfassen, `/ux-recommend`, um das System zu wählen, `/ux-design`, um den Code zu generieren, und `/ux-lint`, um vor dem Commit zu prüfen, dass er die 100 deterministischen Anti-KI-Slop-Regeln besteht.

Diese README ist die kanonische Referenz. Jeder Befehl, jeder Sub-Agent, jedes Datenmanifest, jeder Installationspfad, jede Brand-Spec, jede Anti-Pattern-Kategorie — alles ist hier dokumentiert. Wenn Sie nach einem Design-Plugin für Claude Code suchen oder KI-Design-Werkzeuge für Cursor, Windsurf oder Codex vergleichen, lesen Sie dies von oben bis unten und [compare.html](https://uxskill.laithjunaidy.com/compare.html) parallel dazu.

---

## Inhaltsverzeichnis

1. [Schnellinstallation](#schnellinstallation)
2. [Die Zahlen — Live-Vergleich gegen die Top-8-Claude-UX-Skills](#die-zahlen--live-vergleich-gegen-die-top-8-claude-ux-skills)
3. [Architektur — wie die Teile ineinandergreifen](#architektur--wie-die-teile-ineinandergreifen)
4. [Die 22 Slash-Befehle — detaillierte Referenz](#die-22-slash-befehle--detaillierte-referenz)
5. [Die 5 Sub-Agents](#die-5-sub-agents)
6. [Die 11 Datenmanifeste](#die-11-datenmanifeste)
7. [Die 100 Anti-KI-Slop-Regeln — der Linter](#die-100-anti-ki-slop-regeln--der-linter)
8. [Die 110 Brand-DESIGN.md-Specs — nach Kategorie](#die-110-brand-designmd-specs--nach-kategorie)
9. [MCP-Server — der asymmetrische Zug](#mcp-server--der-asymmetrische-zug)
10. [Der Installer für 17 IDEs](#der-installer-für-17-ides)
11. [Anwendungsfälle — konkrete Szenarien](#anwendungsfälle--konkrete-szenarien)
12. [Im Vergleich zu Alternativen](#im-vergleich-zu-alternativen)
13. [Roadmap](#roadmap)
14. [Beitragen](#beitragen)
15. [Lizenz, Autor, Danksagungen](#lizenz-autor-danksagungen)

---

## Schnellinstallation

Drei Installationswege. Wählen Sie den, der zu Ihrer Umgebung passt.

### Weg 1 — Claude-Code-Marketplace (kanonisch)

Wenn Sie in Claude Code arbeiten, installieren Sie über den Plugin-Marketplace:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Damit werden alle 22 Slash-Befehle und 5 Sub-Agents in Ihre Claude-Code-Session eingebunden. Nach der Installation führen Sie `/ux-init` aus, um das projektspezifische Zustandsverzeichnis `.ux/` einzurichten und zu prüfen, dass die Python-Engine erreichbar ist.

### Weg 2 — pip (universell)

Wenn Sie außerhalb von Claude Code arbeiten (Cursor, Windsurf, CLI, CI), installieren Sie das Python-Paket:

```bash
pip install uxskill
uxskill init                       # erkennt Ihre IDE automatisch und installiert das passende Artefakt
uxskill stats                      # gibt die Manifest-Zähler aus, um die Installation zu verifizieren
uxskill lint .                     # startet den Linter gegen das aktuelle Verzeichnis
```

Das Paket stellt sowohl `ux` als auch `uxskill` als CLI-Entrypoints bereit — beide sind dasselbe Binary.

### Weg 3 — npx (kein Python erforderlich)

Wenn Sie Python nicht direkt verwalten möchten, bootstrappt der npx-Wrapper alles über `pipx`:

```bash
npx uxskill init                  # lädt pipx + uxskill beim ersten Lauf
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Installation verifizieren

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

Wenn ein Zähler 0 zurückgibt, fehlt die JSON-Datei — öffnen Sie ein Issue unter [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Die Zahlen — Live-Vergleich gegen die Top-8-Claude-UX-Skills

Die Sternzahlen wurden zuletzt am **2026-05-28** über `gh api` verifiziert. ux-skill (Laith0003/ux-skill) ist der jüngste Neuzugang — wir sind klein in Bekanntheit, tief in Architektur. Der Vergleich unten ist ehrlich: wo wir verlieren, wo wir gewinnen.

| Plugin | Sterne | Architektur | Slash-Befehle | Linter (CI-fähig) | Brand-Specs | Komponenten | Motion-Presets | Unterstützte IDEs |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, einzelne Skill | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 Skills + Preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + forschungsgestützter Geschmack | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Einzige 62-KB-SKILL.md + Skripte | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | MCP-verdrahtete Skill-Bibliothek | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Mono-ästhetische Skill | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Anti-Slop-Design-Skill | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3-Komponenten + Audit | 1 | — | — | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python-Engine + 11 Manifeste + 22 Befehle + 5 Sub-Agents + CI-Linter** | **22** | **100 Regex-Regeln** | **110** | **148** | **57** | **17** |

### Wo wir verlieren

- **Bekanntheit.** Sie haben Hunderttausende Sterne. Wir haben 14. Setzen Sie einen Stern — das ist die günstigste Form der Unterstützung.
- **Markenwiedererkennung.** ui-ux-pro-max und open-design haben einen Vorsprung, der sich in Monaten misst, nicht in Tagen.
- **Marketing-Politur.** Sie haben Screenshots, Demo-Videos und eine auffindbare Landingpage. Wir haben eine gründliche README und eine schlanke Landingpage.

### Wo wir gewinnen

- **Komponentenbibliothek:** 148 dokumentierte Komponenten mit Anatomie, Zuständen, verwendeten Tokens und Motion-Specs. Keine der anderen 8 liefert ein Komponentenmanifest.
- **Motion-Presets:** 57 stack-fertige Einträge (Framer Motion, GSAP, CSS) mit reduced-motion-Fallbacks. Keine der anderen liefert ein Motion-Manifest.
- **Anti-Pattern-Linter:** 100 deterministische Regex-Regeln, läuft in CI, beendet mit Non-Zero bei Critical/High. Keine der anderen liefert einen deterministischen Linter.
- **Brand-Specs:** 110 echte DESIGN.md-Specs (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude und 96 weitere). Keine der anderen liefert eine Markenbibliothek.
- **17 unterstützte IDEs:** dieselbe Engine, anderer Klebstoff je IDE.
- **22 Slash-Befehle:** Discovery, Generierung, Audit, Lint, Polish, Fix-Schleife, Case-Study, Workshop, Copy, Motion, A11y, Dashboard, Conductor — vollständig integriert.

Vollständige Tabelle Seite an Seite unter [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Architektur — wie die Teile ineinandergreifen

```
ux-skill (Paketname: uxskill)
│
├── data/                              Das Gehirn — abfragbare JSON-Manifeste
│   ├── styles.json                    84 Design-Styles + when/skip + Tokens
│   ├── palettes.json                  176 Paletten (hell/dunkel, Kontrast verifiziert)
│   ├── type-pairs.json                70 display × body × mono Tripel
│   ├── components.json                148 Komponenten (Anatomie, Zustände, Motion)
│   ├── industries.json                184 Branchenregeln + Zielgruppensignale
│   ├── chart-types.json               35 Diagrammtypen (when/skip, Encoding)
│   ├── tech-stacks.json               25 Stacks (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 benannte UX-Gesetze (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 Motion-Presets (Eintritt, Austritt, Hover...)
│   ├── anti-patterns.json             100 Regex-Regeln (CI-fähige Linter-Quelle)
│   └── brands/*.json                  110 Brand-DESIGN-Specs + _index.json
│
├── engine/                            Python — das Reasoning
│   ├── recommender/                   5-parallele-Suche-Merge-Engine
│   ├── linter/                        Deterministischer Anti-Slop-Scanner
│   ├── discovery/                     10-Felder-Zwangsprotokoll
│   ├── generator/                     Token- + Manifest-Emitter
│   ├── installer/                     Multi-IDE-Installer für 17 Umgebungen
│   └── cli/                           `ux` / `uxskill` Entrypoint
│
├── commands/                          22 Claude-Code-Slash-Befehle (.md)
│   ├── ux-init.md                     Bootstrap
│   ├── ux-stats.md                    Inventar-Schnappschuss
│   ├── ux-discover.md                 10-Felder-Intake (Tor)
│   ├── ux-recommend.md                FLAGSCHIFF — 5 parallele Suchen
│   ├── ux-lint.md                     deterministischer Linter
│   ├── ux-design.md                   generiert Frontend-Code
│   ├── ux-component.md                generiert eine Komponente
│   ├── ux-system.md                   generiert komplettes Designsystem
│   ├── ux-dashboard.md                generiert Dashboard-Oberfläche
│   ├── ux-motion.md                   Motion-Behandlung + Audit
│   ├── ux-audit.md                    Design-Audit mit 6 Linsen
│   ├── ux-a11y.md                     WCAG-2.1-AA-Audit
│   ├── ux-critique.md                 Geschmackskritik (3 Treffer, 3 Fehler, 1 Zug)
│   ├── ux-copy.md                     Microcopy-Review + -Umschreiben
│   ├── ux-fix.md                      wendet Findings als atomare Commits an
│   ├── ux-polish.md                   kosmetischer Durchgang + KI-Slop-Tötung
│   ├── ux-frame.md                    4-Felder-Framing-Block
│   ├── ux-research.md                 Forschungsplanung + -synthese
│   ├── ux-workshop.md                 5-Phasen-Design-Thinking-Workshop
│   ├── ux-case-study.md               veröffentlichbare Wfrah-Editorial-Case-Study
│   ├── ux-next.md                     Workflow-Conductor (nur-lesend)
│   └── ux-expert.md                   Consulting-Hook
│
├── agents/                            5 Sub-Agents (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 Microcopy in der Markenstimme
│   ├── research-synthesizer.md        Interviews + Analytics + Wettbewerber
│   └── design-system-architect.md     Tokens / Komponenten / Fundament
│
├── references/                        Prosa-Quelle der Daten + Demo-Seiten
│   ├── foundations/                   anti-patterns.md, Prinzipien, Geschmack
│   ├── laws/                          UX-Gesetze in Langform
│   ├── process/                       discovery-protocol.md (tragend)
│   ├── styles/                        Prosa je Style (anti-slop.md usw.)
│   ├── components/                    Komponenten in Langform
│   ├── output/                        Ausgabe-Rubriken
│   └── conditional/                   stack-spezifische Hinweise
│
├── bin/
│   ├── uxskill.mjs                    npx-Wrapper -> Python-Engine
│   ├── ux-lint.py                     v2-Linter (bevorzugt)
│   └── ux-lint.sh                     v1-Fallback (bash + perl-PCRE)
│
└── .ux/                               (pro Projekt erstellt)
    ├── last-discovery.json            Brief-Schnappschuss
    ├── last-recommendation.json       gewähltes System
    ├── last-frame.json                Framing-Block
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Wie die Engine tatsächlich arbeitet

1. **Eingabe.** Sie geben ein Brief an — entweder interaktiv über `/ux-discover` (10 Felder) oder nicht-interaktiv über Flags an `ux recommend`.
2. **5 parallele Suchen.** Die Engine führt fünf Lookups gleichzeitig über die Manifeste aus:
   - **Branche → empfohlene_Styles** (industries.json)
   - **Style → Palette- + Typographie- + Motion-Kompatibilität** (styles.json)
   - **Tonalität × Must-have → Palettenfilter** (palettes.json)
   - **Stack → Komponentenkompatibilität + Motion-Presets** (tech-stacks.json, motion-presets.json)
   - **Verboten + Region → Leitplanken + Shortlist exemplarischer Marken** (anti-patterns.json, brands/)
3. **Merge.** Ein deterministischer Merger ordnet die Kandidaten, löst Konflikte auf (z. B. erzwingt ein Must-have-Dark-Mode den Palettenmodus) und gibt ein einziges empfohlenes System aus.
4. **Ausgabe.** Ein JSON-Dokument mit dem gewählten Style, der gewählten Palette, dem Typographie-Paar, den 5 besten Motion-Presets, den 12 besten Komponenten, den 5 besten exemplarischen Marken und allen 35 aktiven Anti-Pattern-Leitplanken. Plus ein Begründungsblock, der jede Wahl erklärt.
5. **Generierung.** Nachgelagerte Befehle (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) konsumieren die Empfehlung, um tatsächlichen Code über die Sub-Agents zu erzeugen.
6. **Verifikation.** `/ux-lint` scannt den generierten Code erneut gegen die 100 Regex-Regeln. Beendet mit Non-Zero bei Critical/High in CI.

**Python denkt. HTML zeigt. Markdown verkettet.**

---

## Die 22 Slash-Befehle — detaillierte Referenz

Jeder Befehl wird als `.md`-Datei unter `commands/` ausgeliefert, mit `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` und `output state file`. Die untenstehenden Beschreibungen sind verdichtet; die vollständige Quelle ist die kanonische Spezifikation.

Die Befehle sind in fünf Eimer gruppiert: **Bootstrap & Inventar**, **Discovery & Empfehlung**, **Generierung**, **Audit & Verifikation**, **Fix & Polish** und **Conductor**.

### Bootstrap & Inventar

#### `/ux-init` — das Projekt bootstrappen

- **Was:** Erkennt, welche IDE Sie verwenden (`.claude/`, `.cursor/`, `.windsurf/` usw.), installiert das passende Artefakt, prüft, dass die Python-Engine erreichbar ist, gibt einen Statistik-Schnappschuss aus.
- **Wann verwenden:** Erste Installation in einem neuen Projekt. Nach dem Klonen eines Projekts, das ux-skill nutzt. Nach `pip install --upgrade uxskill`.
- **Wann überspringen:** Sie haben es in diesem Projekt bereits ausgeführt und nichts hat sich geändert.
- **Aufruf:** `/ux-init` (ohne Argumente) oder `uxskill init` von der CLI aus.
- **Ausgabe:** IDE-spezifisches Artefakt (siehe [Der Installer für 17 IDEs](#der-installer-für-17-ides)) + `.ux/`-Verzeichnis + stdout-Zusammenfassung.
- **Verkettet mit:** als Nächstes `/ux-discover`.

#### `/ux-stats` — das Dateninventar ausgeben

- **Was:** Gibt Version + Eintragszähler für die 11 Datenmanifeste aus, damit Sie prüfen können, was installiert ist.
- **Wann verwenden:** Nach der Installation. Nach einem Upgrade. Wenn `/ux-recommend` überraschende Auswahlen liefert und Sie unvollständige Manifeste vermuten.
- **Wann überspringen:** Nie — es ist ein 50-ms-Nur-Lese-Befehl.
- **Aufruf:** `/ux-stats` oder `uxskill stats`.
- **Ausgabe:** JSON nach stdout (siehe [Installation verifizieren](#installation-verifizieren) oben).
- **Verkettet mit:** Nur Diagnose; speist nichts nachgelagert.

### Discovery & Empfehlung

#### `/ux-discover` — die Zwangsfunktion (10-Felder-Intake)

- **Was:** Der verpflichtende 10-Felder-Intake, durch den jedes Projekt vor einem Generierungsbefehl gehen muss. Projekttyp, Zielgruppe, Hauptziel, Tonalität, Must-haves, Verbotenes, Referenzmarken, Stack, Region, Erfolgsmetrik. **Keine Improvisation.** Verbotene Phrasen („modern", „clean") zwingen den Nutzer zu konkreten Angaben.
- **Wann verwenden:** Vor jedem `/ux-design`, `/ux-component`, `/ux-system` oder `/ux-dashboard`. Immer wenn ein früheres Brief veraltet ist.
- **Wann überspringen:** Sie beheben einen Bug (`/ux-fix`). Sie führen nur einen Linter-Durchgang aus (`/ux-lint`). Das Brief ist seit der letzten Session unverändert.
- **Aufruf:** `/ux-discover`. Das Plugin fragt; Sie antworten.
- **Ausgabe:** Schreibt `.ux/last-discovery.json` (das 10-Felder-Brief).
- **Verkettet mit:** `/ux-recommend` → nutzt die Discovery, um Style + Palette + Typographie + Motion + Komponenten zu wählen. `/ux-design [zusätzliches Brief]` → erzeugt Frontend-Code, verankert in der Empfehlung. `/ux-component <Name>` → erzeugt eine Komponente, ausgerichtet an den entdeckten Einschränkungen.

#### `/ux-recommend` — die Flaggschiff-5-parallele-Such-Engine

- **Was:** Führt die 5 parallelen Suchen der Python-Engine über die 11 Manifeste aus und liefert ein zusammengeführtes Designsystem zurück. Branche → Style → Palette → Typographie → Motion + Komponenten + exemplarische Marken + Leitplanken.
- **Wann verwenden:** Ein neues Projekt aus dem Nichts starten. Ein müde aussehendes Produkt pivotieren. Pre-Flight vor jedem `/ux-design` oder `/ux-component`.
- **Wann überspringen:** Sie haben `/ux-discover` bereits ausgeführt und ein Brief gespeichert — `/ux-recommend` ist in diesem Flow automatisch. Sie beheben einen Bug (verwenden Sie `/ux-fix`). Sie benötigen nur den Linter (verwenden Sie `/ux-lint`).
- **Aufruf (Claude Code):**
  ```
  /ux-recommend
  ```
  **Aufruf (CLI):**
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
- **Ausgabe:** Schreibt `.ux/last-recommendation.json` — gewählter Style, gewählte Palette, gewähltes Typographie-Paar, 5 beste Motion-Presets, 12 beste Komponenten, 5 beste exemplarische Marken, alle 35 aktiven Anti-Pattern-Leitplanken, plus Begründung.
- **Verkettet mit:** `/ux-design [Brief]` → Frontend-Code mit den empfohlenen Tokens. `/ux-system` → vollständiges Designsystem aus der Empfehlung. `/ux-component <Name>` → eine Komponente im empfohlenen Style. `/ux-lint` → den generierten Code verifizieren.

### Generierung

#### `/ux-design` — eine schöne, Anti-Slop-Oberfläche aus einem Brief generieren

- **Was:** Generiert ein vollständiges, produktionsreifes Frontend-Artefakt (Landing, Marketing-Site, App-Shell) aus dem Discovery-Brief + der Empfehlung. Entsendet `frontend-engineer` mit kreativer Richtung aus den Anti-Slop- und Arsenal-Referenzen.
- **Wann verwenden:** „Designe ein", „bau mir ein", „generiere eine Landingpage", „erstelle ein Dashboard", „mach eine Komponente" — jede freiformatige visuelle Deliverable-Anfrage.
- **Wann überspringen:** Sie wollen einen Review, kein Build (verwenden Sie `/ux-audit` oder `/ux-critique`). Sie wollen nur eine Komponente (verwenden Sie `/ux-component`). Backend- oder Infrastrukturarbeit.
- **Aufruf:** `/ux-design generiere eine Fintech-Landing für eine MENA-Neobank, warme Editorial-Tonalität, Dark-Mode AA, keine Violett-Verläufe`.
- **Ausgabe:** Generierter Code (HTML / Blade / JSX / Vue / Astro), plus `.ux/last-design.json`.
- **Verkettet mit:** `/ux-lint` → gegen Leitplanken verifizieren. `/ux-polish` → kosmetischer Durchgang. `/ux-a11y` → Accessibility-Audit. `/ux-copy` → Microcopy-Review. `/ux-fix` → Findings als atomare Commits anwenden.

#### `/ux-component` — eine Komponente generieren

- **Was:** Erzeugt eine einzelne, produktionsreife Komponente (Button, Modal, Navbar, Sidebar, Card, Tabelle, Formular, Chart) aus einer Spezifikation. Alle vier Interaktionszustände, barrierefrei, markentreu. Sucht die Komponente zuerst in `.ux/last-recommendation.json`, fällt zurück auf eine direkte Manifestabfrage.
- **Wann verwenden:** Jede Anfrage nach einem einzelnen Element — „bau einen Button", „erstelle eine Pricing-Card", „mach ein Modal", „füge eine Navbar hinzu", „designe eine Sidebar", „ich brauche eine Datentabelle", „bau ein Formular", „mach eine Chart-Komponente".
- **Wann überspringen:** Vollständige Seite oder Multi-Sektionen-Oberfläche (verwenden Sie `/ux-design`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-component pricing-card-trio --brief="fintech, dunkel, Monospace-Zahlen"`.
- **Ausgabe:** Generierter Komponentencode, plus `.ux/last-component.json`.
- **Verkettet mit:** `/ux-lint` → verifizieren. `/ux-polish` → straffen.

#### `/ux-system` — ein vollständiges Starter-Designsystem generieren

- **Was:** Schlägt ein vollständiges Starter-Designsystem für ein Projekt vor, das noch keines hat — Tokens (Farbe, Typographie, Raum, Motion, Radius, Schatten), Foundation-Dokumente, Komponentenverträge, Dark-Mode-Paarungen, Theme-Switcher. Entsendet `design-system-architect`.
- **Wann verwenden:** „Wir haben kein Designsystem", „bau uns ein System", „schlag Tokens vor", „was sollte unser Theme sein", „richte unser DS ein".
- **Wann überspringen:** Das Projekt hat bereits ein Designsystem — verwenden Sie stattdessen `/ux-component` gegen das bestehende System. Backend oder Infrastruktur.
- **Aufruf:** `/ux-system` (führt zuerst Discovery aus, falls nicht bereits hinterlegt).
- **Ausgabe:** `tokens.json`, `foundations.md`, `components/*.md`-Verträge, optionale Tailwind- / vanilla- / SCSS-Emission. Schreibt `.ux/last-system.json` für den Verkettungskontext.
- **Verkettet mit:** `/ux-component` → gegen das neue System bauen. `/ux-design` → eine Oberfläche mit den neuen Tokens generieren.

#### `/ux-dashboard` — spezialisierte Dashboard-Generierung

- **Was:** Dashboard mit Datendichte-Disziplin — Bento-Layout, tabellarische Monospace-Ziffern, Sparkline-Patterns, Anti-Card-Überdosis, semantische Statusfarben, sparsame Motion. Keine Marketing-Landing mit aufgeklebten Charts.
- **Wann verwenden:** „Bau ein Dashboard", „designe das Admin-Panel", „mach eine Metrics-Seite", „Operator-Konsole", „Analytics-Ansicht", „KPI-Board", „Monitoring-Bildschirm".
- **Wann überspringen:** Marketing-Landingpage mit Statistiken (verwenden Sie `/ux-design`). Nur ein Widget (verwenden Sie `/ux-component`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-dashboard`.
- **Ausgabe:** Generierter Dashboard-Code + `.ux/last-dashboard.json`.
- **Verkettet mit:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — Motion-Behandlung

- **Was:** Generiert die Motion-Schicht einer Oberfläche — Dauern, Easings, Choreografie, reduced-motion-Fallbacks, Performance-Disziplin. Auditiert auch bestehende Motion gegen die 5 Dimensionen (Timing, Easing, Bedeutung, reduced-motion, Performance).
- **Wann verwenden:** „Motion-Check", „sind die Animationen gut", „repariere die Motion", „prüfe die Animationen", „Motion-Audit", „Performance-Durchgang über die Motion".
- **Wann überspringen:** Die Oberfläche hat keine Motion (verwenden Sie `/ux-audit` oder `/ux-polish`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-motion path/to/component.tsx` (Audit-Modus) oder `/ux-motion --generate hero-entry` (Generierung).
- **Ausgabe:** Aktualisierter Code (im Generierungsmodus) oder `.ux/last-motion.json`-Bericht (im Audit-Modus).
- **Verkettet mit:** `/ux-fix` → Motion-Findings anwenden. `/ux-polish` → straffen.

### Audit & Verifikation

#### `/ux-lint` — deterministischer Regex-basierter Linter (kein LLM, CI-fähig)

- **Was:** Führt 100 Regex-Regeln gegen Ihren Code aus. Kein LLM-Call. Beendet mit Non-Zero bei Critical / High in CI. Quelle: `data/anti-patterns.json`. Die Regeln decken A11y (23), Inhalt (15), Layout (13), Typographie (10), Farbe (9), Qualität (9), Visuell (9), Motion (8), Performance (4) ab.
- **Wann verwenden:** Pre-Commit-Hook. CI-Gate. Schneller erster Durchgang über eine große Codebase, bevor man die Kosten von `/ux-audit` zahlt. Nach `/ux-design` oder `/ux-component`, um die Generierung zu verifizieren.
- **Wann überspringen:** Sie wollen eine Fix-Schleife (der Linter meldet, er editiert nicht — verketten Sie mit `/ux-polish --fix` oder `/ux-fix`). Sie wollen Geschmacksurteil (verwenden Sie `/ux-critique`).
- **Aufruf (Slash):** `/ux-lint src/`.
- **Aufruf (CLI):** `uxskill lint .` oder `python3 bin/ux-lint.py .` oder `bash bin/ux-lint.sh --ci --fail-on high`.
- **Aufruf (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Ausgabe:** Findings nach stdout (Ort, Regel-ID, Schweregrad, Beweis). Exit-Code 0 wenn sauber, Non-Zero bei Critical/High, wenn `--fail-on high` gesetzt ist.
- **Verkettet mit:** `/ux-polish --fix` → LLM-getriebenes Gegenstück auf denselben Patterns. `/ux-fix` → Findings als Commits anwenden, nach Schweregrad sortiert. `/ux-audit` → vollständiger 6-Linsen-Reasoning-Durchgang. `/ux-next` → den Conductor entscheiden lassen.

#### `/ux-audit` — Design-Audit mit 6 Linsen

- **Was:** Eine strukturierte, meinungsstarke Prüfung gegen sechs Linsen (Klarheit, Hierarchie, Barrierefreiheit, Stimme, Motion, Geschmack), die nach Schweregrad gekennzeichnete Findings erzeugt. Bericht im Polaris-Stil. Liest zuerst `.ux/last-frame.json` — Zielgruppe und Outcome verankern den Schweregrad jedes Findings.
- **Wann verwenden:** Die Oberfläche existiert und Sie wollen eine vertretbare Kritik. „Auditiere", „prüfe die UX", „ist das gut", „was ist kaputt", „zerlege das".
- **Wann überspringen:** Die Oberfläche existiert noch nicht (verwenden Sie `/ux-design`). Der Nutzer will eine einzelne Linse (verwenden Sie den gezielten Befehl: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Der Nutzer will eine Geschmacksmeinung (verwenden Sie `/ux-critique`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-audit https://example.com/pricing` oder `/ux-audit src/components/Pricing.tsx`.
- **Ausgabe:** Schreibt `.ux/last-audit.json` — `findings`-Array mit `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Verkettet mit:** `/ux-fix` → Findings anwenden. `/ux-polish` → kosmetischer Durchgang. `/ux-design` → falls strukturelles Redesign nötig.

#### `/ux-a11y` — WCAG-2.1-AA-Audit + Höflichkeitsprüfungen

- **Was:** Ein strukturierter WCAG-2.1-AA-Audit plus die Höflichkeitsprüfungen, die automatisierte Werkzeuge passieren, aber echte Nutzer immer noch verletzen (Fokus-Sichtbarkeit, Fehlerspezifizität, Motion-Präferenzen, Tastaturfallen, Farbabhängigkeit).
- **Wann verwenden:** Pre-Ship-Accessibility-Gate. Nach einem Redesign. „Accessibility-Check", „WCAG-Audit", „ist das barrierefrei", „A11y-Review", „Screen-Reader-Test", „Tastatur-Navigations-Check".
- **Wann überspringen:** Nicht nutzerseitig. Backend oder Infrastruktur. Skizzen in Arbeit.
- **Aufruf:** `/ux-a11y https://example.com` (Live-URL bevorzugt — automatisierte Werkzeuge und Tastaturtests funktionieren nur live).
- **Ausgabe:** Schreibt `.ux/last-a11y.json` — `findings`-Array mit `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, `beyond_wcag`-Array, `severity_counts`.
- **Verkettet mit:** `/ux-fix` → Findings als Commits anwenden. `/ux-copy` → Alt-Texte und Formular-Fehler-Verdrahtung als Teil eines Copy-Durchgangs korrigieren.

#### `/ux-critique` — Geschmacksurteil (3 Treffer, 3 Fehler, 1 strategischer Zug)

- **Was:** Die Meinung eines Designers — kein strukturierter Audit, kein Schweregrad-Score, nur eine straffe, meinungsstarke Einschätzung, die benennt, was funktioniert, was nicht und der einzige strategische Zug, der am meisten verändern würde.
- **Wann verwenden:** „Was denkst du", „ist das gut", „kritisier das", „ehrliche Meinung", „stimmt der Vibe", „fühlt sich das nach uns an", „sollten wir shippen".
- **Wann überspringen:** Der Nutzer will explizit einen strukturierten Audit (verwenden Sie `/ux-audit`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-critique https://example.com`.
- **Ausgabe:** Schreibt `.ux/last-critique.json` — 3 Treffer, 3 Fehler, 1 strategischer Zug, plus Prosa.
- **Verkettet mit:** `/ux-design`, falls die Einschätzung Redesign empfiehlt. `/ux-polish`, falls sie Straffung empfiehlt.

#### `/ux-copy` — Microcopy-Review + -Umschreiben

- **Was:** Bewertet jeden sichtbaren String gegen die Stimm-Rubrik und erzeugt eine Vorher/Nachher-Umschreibung. Fängt: „Formular enthält Fehler" (generisch), „John Doe" (Platzhalter), KI-fröhlicher feierlicher Copy, generische CTAs, tote Empty States, nutzlose Fehler.
- **Wann verwenden:** Struktur stimmt, aber die Worte schwächeln. „Prüfe den Copy", „repariere die Microcopy", „die Fehlermeldungen sind schlecht", „schreib das um", „strafffe die Strings", „die Buttons klingen generisch", „dieser Empty State ist tot".
- **Wann überspringen:** Layout-Probleme (verwenden Sie `/ux-audit` oder `/ux-polish`). Accessibility-getriebene Copy-Probleme wie Alt-Texte (verwenden Sie `/ux-a11y`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-copy src/views/checkout.blade.php`.
- **Ausgabe:** Schreibt `.ux/last-copy.json` — `strings`-Array mit `{location, severity, before, after, notes}`, plus Rubrik + Locales, die Übersetzung brauchen.
- **Verkettet mit:** `/ux-fix` → Umschreibungen anwenden. `/ux-a11y` → nach den Copy-Fixes erneut prüfen.

### Fix & Polish

#### `/ux-fix` — Findings als atomare Commits anwenden

- **Was:** Liest den neuesten Bericht aus `.ux/` (Audit, Copy, A11y, Motion oder Polish), validiert den Working-Tree und wendet die Findings als atomare Commits über die richtigen Sub-Agents an. Verifiziert erneut, indem der ursprüngliche Befehl wieder ausgeführt wird.
- **Wann verwenden:** Nach dem Ausführen eines Audit-Klassen-Befehls und der Durchsicht der Findings. „Behebe die Findings", „wende die Fixes an", „starte die Fix-Schleife", „patche die Oberfläche", „mach die Änderungen", „los, repariere das".
- **Wann überspringen:** Kein vorheriger Bericht in `.ux/`. Working-Tree ist schmutzig und der Nutzer hat Stash/Commit nicht zugestimmt. Fixes brauchen Design-Urteil, keine mechanische Anwendung (verwenden Sie `/ux-design` für ein Redesign).
- **Aufruf:** `/ux-fix` (erkennt automatisch, welcher Bericht zu beheben ist) oder `/ux-fix --from=last-a11y.json`.
- **Ausgabe:** Atomare Commits pro Finding. Führt den ursprünglichen Befehl erneut aus und aktualisiert die `.ux/last-*.json`-Datei. Gibt eine Zusammenfassung aus.
- **Verkettet mit:** `/ux-next` → der Conductor wählt den nächsten Zug.

#### `/ux-polish` — kosmetischer Durchgang + KI-Slop-Tötung

- **Was:** Abstandsrhythmus, Hierarchie-Schärfung, KI-Slop-Erkennung, Token-Konsistenz. Das LLM-getriebene Gegenstück zu `/ux-lint` — nutzt Ihr Urteil bei Geschmacksentscheidungen.
- **Wann verwenden:** Struktur stimmt, aber Ausführung ist lose. „Polier", „strafffe das", „entferne den KI-Slop", „mach es premium", „lass es weniger nach KI aussehen", „die Abstände fühlen sich falsch an", „das wirkt generisch", „braucht mehr Geschmack".
- **Wann überspringen:** Der Oberfläche fehlt Kernfunktionalität (das zuerst beheben). Braucht Redesign, kein Polish (verwenden Sie `/ux-design`). Copy-Probleme (verwenden Sie `/ux-copy`). Motion-Probleme (verwenden Sie `/ux-motion`). A11y-Probleme (verwenden Sie `/ux-a11y`).
- **Aufruf:** `/ux-polish src/components/Hero.tsx`.
- **Ausgabe:** Aktualisierter Code + `.ux/last-polish.json`, das die Änderungen beschreibt.
- **Verkettet mit:** `/ux-lint` → prüfen, dass der Polish hält. `/ux-a11y` → Barrierefreiheit erneut prüfen.

### Discovery & Narrativ

#### `/ux-frame` — 4-Felder-Framing-Block

- **Was:** Erfasst Für-wen, Outcome, Hypothese und Erfolgssignal in einem strukturierten Framing-Block. Es geschieht keine Designarbeit — nur der Vier-Felder-Intake, der eine vage Anfrage in ein Arbeits-Brief verwandelt. Leichter als `/ux-discover` (4 Felder vs. 10).
- **Wann verwenden:** Beginn eines Projekts, Sprints oder Einzelauftrags. Mitten im Strom, wenn ein Gespräch abgedriftet ist. „Frame das", „was ist das Brief", „richte das Projekt ein", „Framing".
- **Wann überspringen:** Bereits geframet (prüfen Sie `.ux/last-frame.json`). Einzelner Komponentenbau ohne Framing-Implikationen. Backend oder Infrastruktur.
- **Aufruf:** `/ux-frame "Loyalty-Wallet für den MENA-Bashiti-Pilot"`.
- **Ausgabe:** Schreibt `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Verkettet mit:** `/ux-discover` → das Frame zum 10-Felder-Brief ausbauen. `/ux-design` → mit dem Frame als Anker generieren.

#### `/ux-research` — Forschungsplanung + -synthese

- **Was:** Planungsmodus: schreibt Interviewleitfäden, Umfragen, Recruiting-Screener. Synthesemodus (`--synthesize`): verdaut Interviews, Analytics, Wettbewerber-Sites, A/B-Ergebnisse, Support-Tickets zu Empfehlungen. Entsendet `research-synthesizer`.
- **Wann verwenden:** „Plan eine Forschungsstudie", „ich brauche Interviewfragen", „designe eine Umfrage", „wie rekrutiere ich Nutzer", „User-Testing-Plan", „Tagebuchstudie", „Präferenztest", „Fake-Door", „Smoke-Test", „synthetisiere meine Interviewnotizen".
- **Wann überspringen:** Antwort ist bereits mit hoher Sicherheit bekannt. Reversible Entscheidungen mit geringem Risiko. Backend oder Infrastruktur.
- **Aufruf:** `/ux-research --plan "Loyalty-Wallet-Adoption im MENA-Raum"` oder `/ux-research --synthesize interviews/*.md`.
- **Ausgabe:** Schreibt `.ux/last-research.json` — Forschungsplan oder synthetisierte Themen + Belege + Empfehlungen.
- **Verkettet mit:** `/ux-frame` → Findings in ein Frame integrieren. `/ux-design` → aus den Findings generieren. `/ux-workshop` → einen Workshop mit der Forschung als Input fahren.

#### `/ux-workshop` — 5-Phasen-Design-Thinking-Workshop

- **Was:** Moderiert einen Discovery-/Design-Thinking-Workshop von Anfang bis Ende. Fünf sequenzielle Phasen (Exploration → Heatmap → Stakeholder-Map → Lösungsskizze → Game-Plan). Zeitgetaktet. Konkrete Artefakte je Phase. Endet mit einer Entscheidung, nicht „interessanten Findings".
- **Wann verwenden:** Echte Frage, echte Teilnehmer, echtes Zeitbudget. „Mach einen Workshop", „moderiere ein Discovery", „lass uns eine Design-Thinking-Session machen", „ich habe Stakeholder für eine Stunde, was machen wir", „kicke das Projekt an".
- **Wann überspringen:** Brief ist bereits klar und abgegrenzt. Solo-Brainstorm (verwenden Sie `/ux-design` oder `/ux-frame`). Team steckt mitten in der Umsetzung, nicht in Discovery.
- **Aufruf:** `/ux-workshop "Loyalty-Wallet-Pivot" --participants="2 PMs, 1 Designer, 1 Eng-Lead, 1 Kundenvertreter" --minutes=90`.
- **Ausgabe:** Schreibt `.ux/last-workshop.json` — Game-Plan + Artefakte je Phase.
- **Verkettet mit:** `/ux-design` → den Game-Plan ausführen. `/ux-research` → Lücken füllen, die der Workshop sichtbar gemacht hat. `/ux-case-study` → die Reise publizieren.

#### `/ux-case-study` — veröffentlichbare Case-Study (Wfrah-Editorial-Format)

- **Was:** Generiert eine Projekt-Case-Study im reinen monochromen Editorial-Format — Wfrah-Typographie, Haarlinien-Separatoren, nummerierte (A)–(G)-Sektionscodes, bilingual-sicheres Layout. Ein Dokument, keine Marketing-Broschüre. Liest aus `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Wann verwenden:** Nach Launch. Nach einem diskreten Meilenstein. „Schreib eine Case-Study", „Case-Study dieses Projekt", „mach das Abschluss-Dokument", „publizier diese Arbeit", „Portfolio-Stück".
- **Wann überspringen:** Dem Projekt fehlen Daten, um die (A)–(G)-Sektionen zu füllen. Der Nutzer will eine Marketing-Landing, keine Case-Study (verwenden Sie `/ux-design`).
- **Aufruf:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Ausgabe:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Verkettet mit:** Terminalbefehl — meist das Ende eines Projekts.

### Conductor

#### `/ux-next` — Workflow-Conductor (nur-lesend)

- **Was:** Liest jede `.ux/last-*.json` und benennt den nächsten Befehl mit dem höchsten Hebel. Ein Conductor, kein Bauender. Nur-lesend.
- **Wann verwenden:** Zwischen Befehlen. „Was sollte ich als Nächstes tun", „was ist der nächste Zug", „entscheide für mich", „wohin gehen wir von hier".
- **Wann überspringen:** Keine vorherigen Berichte in `.ux/`. Sie haben einen konkreten nächsten Befehl im Sinn.
- **Aufruf:** `/ux-next` (ohne Argumente) oder `/ux-next --focus=a11y`.
- **Ausgabe:** Stdout — empfohlener nächster Befehl + Begründung.
- **Verkettet mit:** Welchen Befehl auch immer er wählt.

#### `/ux-expert` — Consulting-Hook

- **Was:** Bringt die Kontaktdaten des Plugin-Erstellers an die Oberfläche, wenn ein Nutzer nach einem echten UX-Experten fragt. Kurz, direkt, ohne Marketing.
- **Wann verwenden:** „Wer hat das gebaut", „ich brauche einen UX-Experten", „machst du Consulting", „kann ich jemanden dafür engagieren", „steckt ein Mensch hinter diesem Plugin".
- **Wann überspringen:** Der Nutzer fragt nach Plugin-Features, nicht nach Consulting.
- **Aufruf:** `/ux-expert`.
- **Ausgabe:** Kurze Kontaktkarte mit LinkedIn / E-Mail / Repo.

### Befehlskettengraph

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4-Felder-Framing-Block
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10-Felder-Intake (ZWANGSTOR)
                  └────────────┬─────────┘
                               │ schreibt .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 parallele Suchen -> zusammengeführtes System
                  └────────────┬─────────┘
                               │ schreibt .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ schreibt .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ schreibt .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  Findings als Commits anwenden
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  veröffentlichbares Artefakt
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  Conductor — nur-lesend
                  │  /ux-expert          │  Consulting-Hook
                  └──────────────────────┘
```

---

## Die 5 Sub-Agents

Sub-Agents sind rollenspezifische Generatoren, die von Befehlen entsandt werden. Sie laufen nie eigenständig — sie werden von `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research` usw. aufgerufen. Jeder Agent hat eine definierte Eigentumsgrenze: Sie entscheiden NICHT das Brief; sie führen es aus.

### `frontend-engineer`

- **Besitzt:** Produktionsreifen Frontend-Code (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro) mit Anti-KI-Slop-Disziplin.
- **Entsandt von:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Eingaben:** Brief + kreative Richtung + Tokens (aus `.ux/last-recommendation.json`).
- **Ausgaben:** Funktionierender Code, der von generischer KI-Ausgabe unterscheidbar ist. Keine Violett-Verläufe, kein zentrierter Hero, keine drei gleichen Cards, kein Inter in Display-Größe, kein „John Doe", keine Emojis, keine 300-ms-Standards.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Besitzt:** Motion in produktionsreifem Frontend-Code — Framer Motion, GSAP, CSS-Animationen. Dauern, Easings, Choreografie, reduced-motion-Fallbacks, Performance-Disziplin.
- **Entsandt von:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Eingaben:** Motion-Brief + Tokens + die 57 Motion-Presets aus `data/motion-presets.json`.
- **Ausgaben:** Motion, die ihren Platz verdient. Stets in `prefers-reduced-motion`-Fallbacks eingehüllt. Stets gegen Core Web Vitals getestet.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Besitzt:** Die Strings, die ausgeliefert werden — Fehlermeldungen, Empty States, CTAs, Loading States, Erfolgsmeldungen, Toasts, Hilfstext, Formularlabels, Buttontext.
- **Entsandt von:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Eingaben:** Stimmprofil (benannt oder eingefügt) + die Strings der Oberfläche.
- **Ausgaben:** Produktions-Microcopy konsistent über alle Zustände einer Oberfläche angewandt, damit das Produkt wie ein Produkt klingt, nicht wie zehn. Verbote: „Formular enthält Fehler", „John Doe", KI-fröhlicher feierlicher Copy, generische CTAs, tote Empty States.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Besitzt:** Das Verdauen von Forschungseingaben (Interviews, Analytics, Wettbewerber-Sites, A/B-Ergebnisse, Support-Tickets) zu umsetzbaren Designempfehlungen.
- **Entsandt von:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Eingaben:** Rohforschung — Transkripte, Exporte, Wettbewerber-URLs, Support-Cluster.
- **Ausgaben:** Themen, Belege, Empfehlungen. Designt nie die Antwort — gibt dem Designer das Substrat, aus dem zu gestalten ist.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Besitzt:** Vollständige Designsysteme — Tokens (Farbe, Typographie, Raum, Motion, Radius, Schatten), Foundation-Dokumente, Komponentenverträge, Dark-Mode-Paarungen, Theming-Schicht.
- **Entsandt von:** `/ux-system`, `/ux-component`, wenn kein System existiert.
- **Eingaben:** Brand-Brief + `.ux/last-recommendation.json` (Style + Palette + Typographie-Paar + Motion-Presets).
- **Ausgaben:** Ein kohärentes, meinungsstarkes, produktionsreifes System, gegen das nachgelagerte Agents bauen können, ohne Grundlagen neu entscheiden zu müssen. Tokens-JSON, Foundations-MD, Komponentenverträge, Dark-Mode-Mapping.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Sub-Agent-Dispatch-Protokoll

Wenn ein Befehl einen Sub-Agent entsendet, übergibt er:

1. Das Brief / die Empfehlung (aus `.ux/` geladen).
2. Den relevanten Manifest-Ausschnitt (z. B. erhält `frontend-engineer` den gewählten Style + Palette + Komponenten; `motion-engineer` erhält die gewählten Motion-Presets).
3. Die 100 Anti-Pattern-Leitplanken (stets aktiv).
4. Ein Erfolgskriterium (was das Artefakt leisten muss).

Sub-Agents geben zurück:

1. Das Artefakt (Code, Dokument, System).
2. Einen Begründungsblock (warum diese Auswahl).
3. Eine Selbstprüfung gegen die Leitplanken (welche Regeln sie verifiziert haben).

Der aufrufende Befehl führt dann automatisch `/ux-lint` aus, bevor er sich für fertig erklärt.

---

## Die 11 Datenmanifeste

Die Datenschicht ist das Gehirn. Jeder Befehl liest aus ihr; die Engine merged darüber; der Linter scannt gegen sie. Alle Dateien liegen unter `data/` und kapseln ihre Einträge in `{_meta, entries}` zur Schemaversionierung.

### `styles.json` — 84 Design-Styles

| Feld | Beschreibung |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalistisch / Schweizerisch, Brutalistisch, Editorial, Glassmorphismus, Neumorphismus, Bento, Skeuomorph, Industriell, Maximalistisch, KI-Futuristisch, MENA-modern, Vaporwave usw. |
| `sample entry` | `swiss-international` — „Das Raster ist Gesetz. Die Typographie leistet die Schwerarbeit. Dekoration ist Scheitern." |

Verwendet von: `/ux-recommend`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 Farbpaletten

| Feld | Beschreibung |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (hell/dunkel), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazin, klinisch, verspielt, brutalistisch, monochrom, juwelenfarbig, MENA-warm, dev-tools-dunkel usw. |
| `sample entry` | `claude-warm-editorial` — hell, warm/editorial/magazin, canvas #faf9f5, primary #cc785c |

Verwendet von: `/ux-recommend`, `/ux-system`. Kontrast verifiziert auf AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 Typographie-Paarungen

| Feld | Beschreibung |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Alle Schriftfamilien haben Lizenz + Quell-URL. Verwendet von `/ux-recommend`, `/ux-system`.

### `components.json` — 148 Komponenten

| Feld | Beschreibung |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Formulare, Datenanzeige, Feedback, Overlays, Layout, Inhalt, Marketing, E-Commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Mega-Navigation, Produkt-Grid — 6-teilige Anatomie, 4 Zustände |

Das ist unser größter Burggraben. Kein anderes Claude-UX-Plugin liefert ein strukturiertes Komponentenmanifest.

### `industries.json` — 184 Branchenregeln

| Feld | Beschreibung |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Finanzdienstleistungen, Gesundheitswesen, Bildung, E-Commerce, SaaS B2B, SaaS B2C, Developer Tools, Medien, Gaming, Reisen, Immobilien, MENA-spezifisch usw. |
| `sample entry` | `fintech-neobank` — hohes Vertrauen, regulatorische Disclosures, Saldo-/Transaktions-Primär-UI, mobile-first für täglichen Gebrauch |

Verwendet von `/ux-recommend` als erste parallele Suchachse.

### `chart-types.json` — 35 Diagrammtypen

| Feld | Beschreibung |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Vergleich, Zeitreihen, Verteilung, Zusammensetzung, Beziehung, Fluss, Geografisch |
| `sample entry` | `bar-vertical` — Vergleicht 4–15 diskrete Kategorien. Position auf der x-Achse mappt Kategorie; Höhe mappt Wert. |

Verwendet von `/ux-dashboard`, `/ux-component` (Chart-Instanzen).

### `tech-stacks.json` — 25 Stacks

| Feld | Beschreibung |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, kompatibel mit Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Weitere Stacks: Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 benannte UX-Gesetze

| Feld | Beschreibung |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Entscheidungskosten, Aufmerksamkeit, Gedächtnis, Motorische Kontrolle, Visuelle Wahrnehmung, Sozial, Emotional, Formulare, Fehlerbehandlung, Onboarding, Empty State usw. |
| `sample entry` | `hicks-law` — Die Entscheidungszeit wächst logarithmisch mit der Anzahl der dargestellten Optionen |

Verwendet von `/ux-audit` (6-Linsen-Bewertung) und `/ux-critique` (Geschmacksanker).

### `motion-presets.json` — 57 Motion-Presets

| Feld | Beschreibung |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion-Fallback), `when_to_use` |
| `categories` | Eintritt, Austritt, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-gebunden |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Jedes Preset hat eine reduced-motion-Variante. Stack-fertiger Code für Framer Motion, GSAP und reines CSS.

### `anti-patterns.json` — 100 Regex-Regeln

| Feld | Beschreibung |
|---|---|
| `entries` | 100 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y (23), Inhalt (15), Layout (13), Typographie (10), Farbe (9), Qualität (9), Visuell (9), Motion (8), Performance (4) |

Die vollständige Regelliste findet sich in [Die 100 Anti-KI-Slop-Regeln](#die-100-anti-ki-slop-regeln--der-linter).

### `brands/*.json` — 110 Brand-Specs

| Feld | Beschreibung |
|---|---|
| `entries` | 110 (plus `_index.json`, das alle listet) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automobil (8) |

Vollständige Liste in [Die 110 Brand-DESIGN.md-Specs](#die-110-brand-designmd-specs--nach-kategorie).

---

## Die 100 Anti-KI-Slop-Regeln — der Linter

ux-skill liefert einen deterministischen Regex-basierten Linter aus. **Kein LLM.** **Keine API.** **Kein Netzwerk.** Läuft in CI in ~200 ms gegen eine typische Next.js-App. Beendet mit Non-Zero bei Critical-/High-Findings, wenn `--fail-on high` gesetzt ist.

Die Regeln stammen aus `data/anti-patterns.json` (v2 bevorzugt) mit einem `references/foundations/anti-patterns.md`-Fallback (v1 bash). Zwei Binärdateien werden ausgeliefert: `bin/ux-lint.py` (Python, schnell, erweiterbar) und `bin/ux-lint.sh` (Bash + perl-PCRE, für Umgebungen ohne Python).

### Regeln nach Kategorie

#### Typographie (3 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| high | `inter-as-display` | Inter als Display-Schrift verwendet |
| medium | `hero-text-arbitrary-90px` | Willkürliche Hero-Schriftgröße |
| low | `font-system-only` | System-Font-Stack ohne gewählte Schriftart |

#### Farbe (6 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| high | `purple-to-blue-gradient` | Standard-KI-Verlauf Violett-zu-Blau |
| high | `dark-text-on-dark-card` | Kontrastarmer Text auf Karte |
| medium | `gradient-text-rainbow` | Mehrstufiger Gradient-Text |
| medium | `card-glow-purple-shadow` | Violettes Glow-Schatten auf Karten |
| medium | `gradient-mesh-purple-pink` | Hero mit Violett-Pink-Mesh-Gradient |
| low | `tailwind-color-named-vague` | Benannte Tailwind-Farben ohne semantischen Token |

#### Layout (5 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| high | `three-equal-card-grid` | Drei gleiche Karten in einer Reihe |
| medium | `centered-everything-hero` | Komplett zentrierte Hero-Komposition |
| medium | `avatar-stack-overlapping` | Generischer überlappender Avatar-Stack |
| low | `pill-rounded-full-everywhere` | `rounded-full` überall angewandt |
| low | `nav-equal-hamburger-desktop` | Hamburger-Menü auf Desktop |

#### Inhalt (5 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum im ausgelieferten Code |
| high | `emoji-in-ui` | Emoji als UI-Element verwendet |
| high | `icon-emoji-stamp` | Emoji als Icon-Stempel verwendet |
| high | `testimonial-fake-five-stars` | Hardcoded Fünf-Sterne-Testimonial |
| medium | `fake-name-john-doe` | Generische Platzhalternamen |

#### Motion (3 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Hüpfender Pfeil am CTA |
| low | `timing-300ms-default` | Standard-Übergangs-Timing 300 ms |
| low | `cubic-bezier-material-only` | Material-Standard-Easing überall |

#### A11y (6 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| high | `inline-svg-no-aria` | SVG ohne aria-label oder aria-hidden |
| high | `img-no-alt` | Bild ohne alt-Attribut |
| high | `link-onclick-no-href` | Anchor mit onClick aber ohne href |
| medium | `button-no-type` | Button ohne type-Attribut |
| medium | `heading-skip-h1-h3` | Übersprungene Überschriftenebene |
| medium | `infinite-scroll-no-pagination` | Endlos-Scroll ohne Tastatur-Fallback |

#### Qualität (6 Regeln)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| high | `console-log-leak` | `console.log` im Komponentencode |
| medium | `inline-style-attribute` | Inline-style-Attribut |
| medium | `any-type-leak` | TypeScript-`any`-Typ |
| medium | `arbitrary-z-index-9999` | Faule z-index-Werte |
| low | `shadcn-default-everywhere` | Standard-shadcn-Token-Block unverändert |
| low | `todo-fixme-comment` | TODO oder FIXME im ausgelieferten Code |

#### Visuell (1 Regel)

| Schweregrad | Regel-ID | Name |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop-Blur ohne Glas-Oberfläche |

### Linter-Nutzung

**Einmaliger Scan:**

```bash
uxskill lint .
# oder
python3 bin/ux-lint.py src/
# oder
bash bin/ux-lint.sh src/
```

**CI-Gate (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Pre-Commit-Hook:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Ausgabe (Beispiel):**

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

## Die 72 Brand-DESIGN.md-Specs — nach Kategorie

Echte Marken. Echte Designsprachen. Echte DESIGN.md-Specs — keine generischen Paletten. Sagen Sie dem Plugin „bau eine Landing im Stil von Stripe" und es liest das tatsächliche Markenvokabular: Stimm-Rubrik, Farbtokens, Motion-Konventionen, Signature Moves, Anti-Moves.

Jede Marke wird als strukturiertes JSON (`data/brands/<slug>.json`) plus Prosa-Referenz (`references/brands/<slug>.md`) ausgeliefert.

### Developer Tools (24)

ClickHouse, Composio, Cursor, Expo, Framer, HashiCorp, IBM, Lovable, Mintlify, MongoDB, Ollama, OpenCode, PostHog, Raycast, Replicate, Resend, Sanity, Sentry, Slack, Supabase, Superhuman, Vercel, Warp, Webflow

### Consumer / Lifestyle / Retail (11)

Airbnb, Apple, HP, Meta, Nike, Pinterest, PlayStation, Shopify, Spotify, Starbucks, Uber

### AI / ML Platform (9)

Claude, Cohere, ElevenLabs, MiniMax, Mistral AI, Runway, Together AI, VoltAgent, xAI

### Productivity / Collaboration (8)

Airtable, Cal.com, Figma, Intercom, Linear, Miro, Notion, Zapier

### Automobil (8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### Fintech / Crypto (7)

Binance, Coinbase, Kraken, Mastercard, Revolut, Stripe, Wise

### Editorial / Media (5)

Clay, NVIDIA, The Verge, Vodafone, Wired

### Warum das wichtig ist

Die anderen 8 populären Claude-UX-Plugins erzeugen „modern minimal" oder „clean dashboard" — Varianten derselben Default-Ästhetik. ux-skill erlaubt es Ihnen, nach **Linears Klarheit**, **Stripes Ernsthaftigkeit**, **Apples Zurückhaltung**, **Teslas Monolith**, **Notions Freundlichkeit**, **Cursors Gradient-Disziplin**, **Raycasts Haarlinien-Dichte**, **Claudes warmem Editorial** zu fragen — und die Engine zieht die richtigen Tokens, Stimme, Motion-Konventionen und Signature Moves aus der Brand-Spec.

---

## MCP-Server — der asymmetrische Zug

ux-skill liefert einen **Model-Context-Protocol-Server** aus. Führen Sie `ux-mcp` aus und die Engine wird zu einem langlebigen stdio-Prozess, den jeder MCP-fähige Host — Claude Desktop, Cursor, Windsurf, generische Agents — aufrufen kann. Vierzehn Tools: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Dieselben Python-Handler, die auch die Slash-Befehle nutzen; dieselben Datenmanifeste; derselbe deterministische Recommender.

**Warum das der asymmetrische Zug ist:** Keine der Top-8-Claude-UX-Skills (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) liefert einen MCP-Server aus. Sie sind in der Claude-Code-Plugin-Runtime eingesperrt. ux-skill ist von jedem Host erreichbar, der MCP spricht, einschließlich Agents, die nie von einem Claude-Code-Plugin gehört haben.

```bash
pip install 'uxskill[mcp]'             # mcp ist ein opt-in-Extra
ux-mcp                                  # stdio-JSON-RPC-Server startet
```

Richten Sie Ihren Client auf das `ux-mcp`-Binary. Vollständige Tool-Dokumentation, JSON-Beispiele und Client-spezifische Konfiguration für Claude Desktop, Cursor und Windsurf liegen unter [docs/mcp.html](docs/mcp.html) und in `commands/ux-mcp.md`.

---

## Der Installer für 17 IDEs

`uxskill init` (oder `/ux-init` innerhalb von Claude Code) erkennt automatisch, welche IDE Sie verwenden, und schreibt das passende Artefakt. Dieselbe Python-Engine. Dieselben Empfehlungen. Anderer Klebstoff je IDE.

| IDE / Werkzeug | Erkennungssignal | Installiertes Artefakt |
|---|---|---|
| Claude Code | `.claude/` oder `CLAUDE.md` | Plugin-Manifest unter `.claude-plugin/plugin.json` + alle 22 Befehle + alle 5 Sub-Agents |
| Cursor | `.cursor/` oder `.cursorrules` | `.cursorrules`-Prompt-Header, der auf die Engine zeigt |
| Windsurf | `.windsurf/` oder `.windsurfrules` | `.windsurfrules` mit demselben Prompt-Header |
| GitHub Copilot | `.github/copilot-instructions.md` oder `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json`-Patch |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` oder `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

In jeder IDE funktionieren dieselben CLI-Befehle `uxskill recommend` / `uxskill lint` / `uxskill stats` vom Terminal aus. Die Python-Engine ist die Quelle der Wahrheit; die IDE-Artefakte sind schlanke Prompt-Header, die zu ihr routen.

---

## Anwendungsfälle — konkrete Szenarien

Acht reale Szenarien. Wählen Sie das Ihrer Situation am nächsten kommende und passen Sie den Aufruf an.

### 1. Ein Fintech-Dashboard in Cursor bauen

Sie sitzen in Cursor und arbeiten an einem Dashboard für eine MENA-Neobank. Sie installieren das Plugin und führen Discovery, Empfehlung und dann Dashboard-Generierung aus.

```bash
pip install uxskill
uxskill init                                # erkennt Cursor, schreibt .cursorrules
uxskill discover                            # 10-Felder-Intake
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Dann fragen Sie in Cursor: *„Generiere die Dashboard-Oberfläche mit der Empfehlung in .ux/last-recommendation.json"*. Cursor liest den `.cursorrules`-Header, lädt die Empfehlung und entsendet eine Dashboard-Generierung mit expliziten Einschränkungen.

### 2. Eine Landing im Stripe-Stil in Claude Code generieren

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Projekttyp? landing
> Branche? fintech-payments
> Tonalität? ernst, technisch, sicher
> Must-have? dark-mode, AA, mobile-first
> Verboten? purple-gradients, three-equal-cards
> Referenzmarken? stripe
> Stack? nextjs-15-app-router
> Region? global
> Erfolgsmetrik? Signup-Conversion

/ux-recommend
> [gibt gewählten Style, Palette, Typographie-Paar, Motion-Presets, Komponenten, exemplarische Marken zurück]

/ux-design "generiere die Landing mit der Stripe-Brand-Spec als Exemplar"
> [frontend-engineer generiert die Seite]

/ux-lint .
> [passt — die Stripe-Brand-Spec wurde respektiert]
```

### 3. Bestehenden Code in CI auf KI-Slop auditieren

Sie haben vor zwei Wochen eine Next.js-App ausgeliefert. Sie wollen eine harte Untergrenze gegen KI-Fingerabdrücke bei jedem PR.

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

PRs, die Violett-zu-Blau-Verläufe, Inter in 96 px, „John Doe"-Testimonials oder Emojis als Icons einführen, scheitern in CI. Ohne LLM-Kosten. ~200 ms.

### 4. Eine bestehende Oberfläche polieren, die „nach KI riecht"

Sie haben eine React-App geerbt, die wie jede andere KI-generierte SaaS-Seite aussieht. Sie wollen, dass sie aufhört, so auszusehen.

```
/ux-critique src/components/Hero.tsx
> [3 Treffer, 3 Fehler, 1 strategischer Zug — die Einschätzung ist ehrlich]

/ux-lint src/
> [15 KI-Fingerabdrücke mit hohem Schweregrad markiert]

/ux-polish src/components/Hero.tsx
> [LLM-getriebener kosmetischer Durchgang + KI-Slop-Tötung]

/ux-fix
> [wendet Findings als atomare Commits an, startet den Linter erneut]
```

Drei Befehle, eine polierte Oberfläche, atomare Commits pro Fix.

### 5. Eine Command-Palette im Linear-Stil entwerfen

```
/ux-component command-palette --brief="Linear-Stil, dunkel, Monospace-Shortcuts, neueste Items zuerst"
> [liest data/brands/linear.app.json für Tokens + Signature Moves]
> [liest data/components.json für Anatomie + Zustände der Command-Palette]
> [entsendet frontend-engineer mit expliziter Linear-Spec]
```

Die generierte Komponente nutzt Linears echte Farbtokens, Typographie-Stack, Motion-Konventionen, Haarlinien-Dichten — keine „generische dunkle UI".

### 6. Einen 90-minütigen Design-Thinking-Workshop mit Stakeholdern moderieren

Sie haben einen Raum mit 5 Personen für 90 Minuten. Sie wollen, dass sie mit einem Game-Plan rausgehen, nicht mit einem Vibe.

```
/ux-workshop "Loyalty-Wallet-Pivot" \
  --participants="2 PMs, 1 Designer, 1 Eng-Lead, 1 Kundenvertreter" \
  --minutes=90
```

Das Plugin moderiert die fünf Phasen (Exploration → Heatmap → Stakeholder-Map → Lösungsskizze → Game-Plan) von Anfang bis Ende, zeitgetaktet, mit konkreten Artefakten je Phase. Die Ausgabe ist `.ux/last-workshop.json` — der Game-Plan, nicht nur „interessante Findings".

### 7. Nach Launch eine veröffentlichbare Case-Study schreiben

Sie haben die Loyalty-Wallet ausgeliefert. Sie wollen ein Portfolio-Stück.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [liest .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generiert Wfrah-Editorial-Case-Study mit nummerierten (A)-(G)-Sektionen, Haarlinien-Separatoren, bilingual-sicherem Layout]
> [schreibt case-studies/bashiti-loyalty.html]
```

Die Case-Study ist ein fertiges, veröffentlichbares Artefakt — kein Entwurf. Reines Monochrom, Editorial-Typographie, bereit für Ihr Portfolio.

### 8. Discovery in einem Nicht-KI-Kontext fahren (nur strukturierter Intake)

Sie grenzen ein Projekt ein. Sie brauchen noch keine Empfehlung — Sie brauchen ein strukturiertes Brief.

```bash
uxskill discover
# 10-Felder-Intake, wird in .ux/last-discovery.json gespeichert

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Sie können das JSON an Ihr Team weitergeben, in ein Notion-Doc einfügen oder in ein separates KI-Werkzeug einspeisen. ux-skill ist auch ein strukturiertes Intake-Werkzeug, nicht nur eine Engine.

### 9. MASTER.md-Persistenz — Ihre Designentscheidungen, im Repo

Nach `/ux-recommend` persistieren Sie den gewählten Style + Palette + Typographie + Motion + Komponenten + exemplarische Marken + Leitplanken als menschlich lesbare Markdown-Datei, die Ihr Team prüfen, diffen und versionieren kann.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Schreibt `.ux/design-system/MASTER.md` (YAML-Frontmatter + Body) und `.ux/design-system/pages/<name>.md` pro generierter Oberfläche über `persist save-page`. Idempotent — dieselbe Eingabe erzeugt byte-identische Ausgabe, daher ist ein erneuter Lauf auf unverändertem Zustand ein No-op in Git.

---

## Im Vergleich zu Alternativen

Kurze Zusammenfassungstabelle. Vollständiger Tabelle-für-Tabelle-Vergleich unter [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimension | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash-Befehle | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Komponenten | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion-Presets | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand-Specs | **72** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Anti-Pattern-Regeln | **35** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-fähiger deterministischer Linter | **ja** | nein | nein | nein | nein | nein | nein | nein | nein |
| Unterstützte IDEs | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery-Gate | **10 Felder** | implizit | implizit | implizit | implizit | implizit | implizit | implizit | implizit |
| `.ux/`-Zustandskette | **ja** | nein | nein | nein | nein | nein | nein | nein | nein |
| Sterne (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Ehrliche Bewertung

- **ui-ux-pro-max** ist größer in Bekanntheit, liefert 18 IDEs, hat BM25-Suche über sein CSV. Es liefert weder Komponentenmanifest, Motion-Manifest, Markenbibliothek noch deterministischen Linter.
- **open-design** hat 19 Skills + Preview, aber nur Claude-Code-Support und keine Anti-Slop-Schicht.
- **hallmark** ist im Geist am nächsten (ebenfalls Anti-Slop), ist aber eine einzelne Skill — keine Engine, keine Manifeste, keine verketteten Befehle.
- **material-3-skill** ist exzellent, wenn Sie ausdrücklich Material Design 3 wollen. Wir konkurrieren nicht auf MD3.

Für vollständige Details je Dimension siehe [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Vollständigkeit des Linters (Q3 2026)

- **+17 zurückgestellte Anti-Pattern-Regeln** für insgesamt 52. Ziele: Dunkel-auf-dunkel-Hover-Zustände, ausschließliche Farbcodierung von Zuständen, redundante z-index-Eskalation, hartkodierte Breakpoints in JS, opacity statt disabled-Zustand usw.
- **`uxskill lint --fix` für sichere Umschreibungen** mechanisch behebbarer Findings (button-no-type, img-no-alt mit leerem String, Entfernung von console-log-leak).
- **VS-Code-Erweiterung**, die Linter-Findings inline an die Oberfläche bringt (kein CI nötig).

### v2.2 — Erweiterung des Komponentenmanifests (Q4 2026)

- **+50 Komponenten** für insgesamt 198. Neuerungen: Combobox mit Async-Filter, Command-Palette mit Heuristik für neueste Items, conditional-form-step, Payment-Element-Varianten, RTL-bewusster Date-Picker, MENA-spezifisches Telefon-Input, Calendar-Grid mit Hijri-Overlay.
- **Code-Emission je Komponente** in 6 Stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, vanilla HTML/CSS).
- **Komponenten-Playground** auf uxskill.laithjunaidy.com/playground — probieren Sie die Empfehlungs-Engine aus + sehen Sie eine Live-Preview der Komponente.

### v3 — Der Marketplace + der Lock-in (2027)

- **Brand-Spec-Marketplace** — Community-Brand-Specs veröffentlichen und entdecken. Bezahltes Publizieren zur Finanzierung der Moderation.
- **Eigene Anti-Pattern-Regeln** — Projekte können eigene Regex-Regeln in `data/anti-patterns.local.json` definieren (bereits in v2 ausgeliefert; v3 fügt Entdeckung + Teilen hinzu).
- **`uxskill plan`** — vollständige mehrseitige Site-Planung aus einem Brief, nicht nur eine Oberfläche.
- **Figma-Plugin-Parität** — dieselbe Empfehlungs-Engine, in Figma sichtbar.

---

## Beitragen

Issues und PRs willkommen. Drei Bereiche mit hohem Hebel:

### Eine Anti-Pattern-Regel hinzufügen

1. Bearbeiten Sie `data/anti-patterns.json` — fügen Sie einen Eintrag mit `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references` hinzu.
2. Fügen Sie einen Test in `tests/linter/` hinzu — eine Datei, die die Regel auslöst, eine, die es nicht tut.
3. Führen Sie `uxskill lint tests/linter/should-trigger/<rule>.tsx` aus — bestätigen Sie, dass sie feuert. Führen Sie auf `tests/linter/should-not-trigger/<rule>.tsx` aus — bestätigen Sie, dass sie es nicht tut.
4. Öffnen Sie einen PR.

### Eine Brand-Spec hinzufügen

1. Erstellen Sie `data/brands/<slug>.json` mit `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Fügen Sie die entsprechende Prosa unter `references/brands/<slug>.md` hinzu.
3. Registrieren Sie sie in `data/brands/_index.json`.
4. Öffnen Sie einen PR. Die Spec muss durch Primärquellen-Referenzen gestützt sein (das tatsächliche Produkt der Marke, ihr öffentliches Designsystem oder ihre DESIGN.md, falls sie eine publiziert).

### Ein Motion-Preset hinzufügen

1. Bearbeiten Sie `data/motion-presets.json` — fügen Sie einen Eintrag mit `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use` hinzu.
2. Das Preset muss eine reduced-motion-Variante haben. Keine Ausnahmen.
3. Öffnen Sie einen PR.

### Prozess

- Lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) für den vollständigen Prozess.
- Lesen Sie [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Neue Regeln und Brand-Specs werden geprüft auf: Verankerung in Primärquellen, kein Overfitting auf ein einzelnes Projekt, keine Emojis in den Daten, RTL-sicheres Verhalten wo zutreffend.

---

## Lizenz, Autor, Danksagungen

### Lizenz

MIT. Nutzen Sie es, forken Sie es, bauen Sie darauf auf. Wenn es Sie davor bewahrt, KI-Slop auszuliefern, vergeben Sie einen Stern an das Repo — das ist die günstigste Form der Unterstützung.

### Autor

**Laith Aljunaidy** — Solo-Gründer von [Dot](https://thedotwallet.com), einer MENA-first-Loyalty-Plattform. Baut ux-skill, damit das KI-generierte Frontend nicht mehr gleich aussieht.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- E-Mail: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Website: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Danksagungen

- Dem Team von Anthropic für Claude Code und die Skill- / Plugin-Architektur, die dies vertreibbar macht.
- Nielsen Norman Group, Laws of UX (lawsofux.com) und der UX-Forschungs-Community, deren Arbeit `data/ux-guidelines.json` speist.
- Jeder in `data/brands/` gelisteten Marke — ihre öffentlichen Designsysteme sind die Quelle der Wahrheit für die Brand-Specs.
- Den ursprünglichen v1-Mitwirkenden: eine Einzel-Claude-Skill, die zum Samen für die v2-Python-Engine wurde.
- Den 8 populären Claude-UX-Plugins, mit denen wir uns verglichen haben — sie haben die Latte höher gelegt; dies ist unsere Antwort.

---

**ux-skill** · **v2.0.0-alpha.1** · Gebaut, damit Claude Code, Cursor, Windsurf und jedes andere KI-Coding-Werkzeug Frontend ausgeben, das nicht KI-generiert wirkt.

> Setzen Sie einen Stern auf [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Installieren Sie via `pip install uxskill` oder `npx uxskill init` · Durchsuchen Sie den Vergleich unter [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
