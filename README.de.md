[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · **Deutsch** · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: die Design-Intelligence-Engine für Claude Code, Cursor und alle anderen KI-Coding-Werkzeuge

**Eine Design-Intelligence-Engine, die KI-generierte UI unverwechselbar statt generisch macht.** Binden Sie sie in eines von 17 KI-Coding-Werkzeugen ein, und Ihre Ausgabe wirkt nicht mehr wie von einer KI gebaut. Kostenlos, MIT, offline, ohne LLM.

```bash
pip install uxskill
```

**[Geben Sie ux-skill einen Stern auf GitHub](https://github.com/Laith0003/ux-skill)**, wenn es Ihnen nützt: Das ist die günstigste Art, dem Projekt zu helfen. Neu hier? Starten Sie mit der [60-Sekunden-Tour](#schnellinstallation) oder sehen Sie es live auf [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![Vorher: generischer Stockfoto-Hero, weicher Violett-Verlauf, keine Markenidentität. Nachher: echtes Baustellenfoto unter einem dunklen Scrim, redaktionelle Headline mit Bernstein-Akzent und ein Angebotsformular direkt im Hero. Derselbe Prompt, ein anderes Ergebnis, wenn ux-skill die Vorgaben liefert.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Vorher: generischer Stockfoto-SEO-Slop. Nachher: echter Baustellenfoto-Hero unter einem dunklen Scrim, redaktionelle Headline mit Bernstein-Akzent, Angebotsformular im Hero. Dasselbe KI-Coding-Werkzeug, derselbe Prompt, ein anderes Ergebnis, wenn ux-skill die Vorgaben liefert.*

> **v4.0, FOUNDATIONS: Ein Befehl baut ein vollständiges, gegen WCAG geprüftes Designsystem, mit Arabisch und der Schreibrichtung von rechts nach links eingebaut.** Das stärkste UX-Plugin für KI-Coding. Ein Python-Reasoning-Kern mit einem deterministischen 7-Achsen-Synthesizer, 12 abfragbaren JSON-Manifesten (84 Styles, 176 Paletten, 70 Typografie-Paarungen, 148 Komponenten, 184 Branchen, 35 Diagrammtypen, 57 Motion-Presets, 112 UX-Gesetze, 171 Anti-Pattern-Regeln, 25 Tech-Stacks, 160 Brand-Specs), 18 Slash-Befehlen, 5 Sub-Agents, 25 MCP-Tools und einem deterministischen Anti-KI-Slop-Linter. Cross-IDE: ausgeliefert für Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer und Roo Cline.

> **Der Markenname lautet `ux-skill`.** Der PyPI- / npm-Paketname bleibt `uxskill`. Das GitHub-Repository liegt unter [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Autor:** [Laith Aljunaidy](https://laithjunaidy.com), Designer und CTO in Amman · **Website:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Vergleich mit jedem Claude-UX-Plugin:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0--beta.2-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#der-installer-für-17-ides)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Neu in 4.0: Grundlagen

Eine Markenfarbe rein, ein Designsystem raus, und sein Kontrast ist geprüft, bevor Sie es bekommen.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 oder neuer. Für den MCP-Server `pip install --upgrade 'uxskill[mcp]'`. Mit pipx `pipx install uxskill` (über einer installierten 3.x `pipx upgrade uxskill`). Mit npm `npx uxskill@latest`. Sie kommen von 3.x? Der [Migrationsleitfaden](docs/migrating-to-4.md) ordnet jedes 3.x-Token seiner Rolle in 4.0 zu.

**Sie bauen ein Produkt oder eine Landingpage?** Sie erhalten `tokens.css` zum Einbinden in Ihre Seite, `fonts.css` mit metrisch angeglichenen Fallbacks für die gewählten Schriften, `fonts-self-host.css`, das die Schriften aus Ihren eigenen Dateien lädt, `tokens.json` für Werkzeuge, dekorative Markengrafik in `art/` und `system-report.md`, der in einfachen Worten sagt, was gebaut wurde, warum, und mit welcher Seitenkomposition Sie beginnen. Gestalten Sie mit den Rollen (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`) und schalten Sie Dunkelmodus, hohen Kontrast, kompakte Abstände, rechts nach links oder reduzierte Bewegung mit einem Attribut auf `<html>` um. Laden Sie die Schriften über den Google-Fonts-Link aus dem Bericht oder über `fonts-self-host.css` und einen Ordner `fonts/`, und binden Sie in beiden Fällen `fonts.css` vor `tokens.css` ein; bearbeiten Sie keine der beiden Dateien. Mit `--brief` folgt der Look der Branche und der Tonalität, wenn das Briefing sie nennt, und strukturierte Felder (Alter, Sprachen, Standardschema, Lesekontext) legen Textgröße, Zielflächen, Schriftsysteme und das Startschema fest; die Discovery fragt nicht nach einer Branche, deshalb fragt `/ux-system create` danach. In Claude Code prüft `/ux-system create` die installierte Version, führt den Build aus und erklärt den Bericht.

**Sie entwerfen ein Designsystem?** Neun Grundlagen (Farbe, Typografie, Abstände, Layout, Radius, Rahmen, Elevation, Bewegung, Bildsprache), jede stufenlos an die sieben Achsen gekoppelt, mit Primitives und semantischen Rollen, im W3C-Design-Tokens-Format (DTCG 2025.10) mit den Werten jedes Modus. Gleiche Eingaben, gleiche Bytes. Über MCP liefert `ux_system_build` den Bericht, das Ergebnis der Prüfung und die Größe jeder Datei, und mit `out` schreibt es dieselben Dateien wie der Befehl.

- **WCAG-Prüfung.** Jede Farbpaarung für Text, Bedienelemente und Fokus wird im hellen und dunklen Modus gemessen, bei normalem und hohem Kontrast: WCAG 1.4.3 (Text 4.5:1) und 1.4.11 (Nicht-Text 3:1) bei normalem Kontrast, WCAG 1.4.6 (Text 7:1) bei hohem Kontrast, dazu eine eigene Untergrenze von 4.5:1 im hohen Kontrast für die meisten Nicht-Text-Elemente, da WCAG keine erweiterte Stufe für Nicht-Text festlegt. Ein System, das durchfällt, wird nicht geschrieben; die Meldung sagt, was zu ändern ist.
- **Standardmäßig sicher.** Es überschreibt nie eine Datei, die abweicht. `--force` ersetzt Dateien nur, wenn Sie es verlangen.
- **Arabisch.** Unter `dir="rtl"` wechselt der Text zu einer arabischen Schrift mit eigenen Größen und eigener Zeilenhöhe; Abstände nutzen logische Eigenschaften, und Bewegungen werden gespiegelt. `--latin-only` lässt das weg.

**Ein System, das Sie schon haben.** `/ux-system enhance --from` liest es in seinen eigenen Namen (DTCG-Tokens, CSS Custom Properties, ein Tailwind-Theme, Markdown-Regeldateien oder ein Export von Figma-Variablen), prüft es mit derselben Prüfung und misst, was Ihr Code tatsächlich damit macht; nichts wird umgeschrieben. `/ux-system extend --from` ergänzt Grundlagen, Rollen oder Verträge, ohne ein vorhandenes Token zu ändern, in einer Erweiterungsdatei daneben, und `uxskill system export` schreibt es als tokens.css, als Tailwind-4-Theme oder als Figma-Variablen. 4.2 bringt die Vertrauensschicht (Lint bei jedem Schreiben, ein Abschluss-Reviewer) und den Launch. Siehe das [Changelog](CHANGELOG.md).

**Komponenten und Sektionen.** 23 Komponentenverträge legen fest, welche Tokens jeder Teil eines Bedienelements in jedem Zustand bindet und wie sich jeder Zustand bewegt: Ein Zustandswechsel geht über `motion.state`, ein Druck skaliert über `motion.press.scale` (und bleibt bei reduzierter Bewegung still), und Tabs, Menüs und Segmented Controls verschieben einen einzigen Indikator. 14 Sektionsverträge (Hero, Pricing, FAQ, Footer und die übrigen) benennen die Aufgabe jeder Sektion, die Komponenten für ihre Slots, den Beleg, den sie braucht, und wie sie sich auf dem Smartphone stapelt. Seiten, die daraus gebaut werden, verwenden Fotos; Interface-Ausschnitte sind zusätzliche Bilder, nie ein Ersatz.

**Ein Linter, der die Seite liest.** 171 Regeln, viele davon mit einer Prüfung auf dem geparsten CSS und Markup, lesen das eigene System der Seite: Bewegung wird nach ihrer Kurve getaktet, die Zeilenhöhe von Display-Text an der Untergrenze der Engine gemessen, und ein verborgenes Bedienelement muss die Tab-Reihenfolge verlassen. `uxskill lint --render` öffnet jede Seite in Headless Chromium in Desktop- und Smartphone-Breite und bedient sie: Fokusringe, die nicht erscheinen oder abgeschnitten sind, Hover und Druck, die zu spät reagieren, Fokus, der nach Escape verloren geht, und ein Druck, der sich bei reduzierter Bewegung trotzdem bewegt.

**Weniger Befehle.** Aus 25 Slash-Befehlen werden 18. `/ux-discover` nimmt `--frame` und `--recommend`, `/ux-design` nimmt `--component`, `--dashboard` und `--from-image`, `/ux-polish` wiederholt Lint, Fix und erneuten Lint, bis der Score 90 erreicht oder drei Runden vorbei sind, und `/ux-init` nimmt `--stats`. Die sieben alten Namen funktionieren weiter als Aliase und entfallen in 4.1; siehe [die Aliase](#aliase-entfallen-in-41).

**Surface-Playbooks.** Die Regeln für Landing, Dashboard und Komponenten liegen in `references/surfaces/`, je ein Playbook. `/ux-design` lädt genau eines, gewählt nach seinem Modus, sodass ein Dashboard-Build nie Hero-Regeln liest.

Tests **9764 bestanden**. Offline. Deterministisch. Es wird nie ein LLM aufgerufen.

### Neu in v3.1: markentreu, responsiv, lebendig

- **Markentreue wird erzwungen, nicht erhofft.** Die Primärfarbe wird aus den Pixeln des LOGOS gelesen (nicht aus dem am häufigsten gemalten CSS); Standardschriften werden zugunsten des Buchstabenstils des Logos abgelehnt. Die extrahierte Marke wandert `recommend` -> `synthesize`, und eine **harte Untergrenze** in `evaluate` lässt jede Ausgabe DURCHFALLEN, die Markenfarbe oder Logo verliert oder keine echten Bilder liefert. Interoperabilität in beide Richtungen mit der offenen `brand.md`-Konvention (Rendern + Einlesen).
- **Mobile-first, geprüft.** Neue Handwerksgrundlagen (`responsive.md`, `component-behaviors.md`) plus eine umbruchbewusste Prüfung, die bei horizontalem Scrollen, einem umbrechenden Nav-, Wortmarken- oder Button-Label oder einem zu hohen Sticky-Header fehlschlägt.
- **Die Wow-Schicht.** Die Engine leitet 2-3 abgestimmte Signature-Momente pro Seite ab; die Doktrin „das Wow kann nur vom Nutzer kommen“ ist damit aufgehoben.
- **Schärferer Linter** (152 Regeln): Erkennung von Pflichtbildern und Nur-Icon-Elementen, Regeln für Platzhalter-Tokens und `100vw`; gesetztes picsum bleibt, zufälliges wird entfernt.

Vollständige Notizen in [CHANGELOG.md](CHANGELOG.md).

### Was ist neu in v3

- **Brand Specs werden zu Trainingsdaten, nicht Templates.** Die 160 Brand Specs sind kein Katalog mehr, aus dem der Recommender wählt, sie sind Vokabular, das der Synthesizer destilliert. Die Ausgabe ist bei jedem Aufruf neu.
- **7-Achsen-Synthesizer** (warmth, contrast, density, geometry, formality, motion, type_personality). Der Brief wird deterministisch auf Achsenwerte gemappt; Achsenwerte kompilieren zu frischen Palette-, Typografie-, Spacing-, Radius- und Motion-Tokens.
- **Drei automatisch dispatchierte Modi**: `strict_brand` (100 % einer Marke), `brand_anchor` (70 % einer Marke + 30 % achsenadaptiert aus Geschwistermarken), `pure_synthesis` (keine Marke genannt, Destillation aus 8 achsenpassenden Beispielen).
- **Decisions-Ledger steuert das Recommender-Re-Ranking.** `.ux/decisions.jsonl` re-rankt Kandidaten nach vergangenen Erfolgen im selben `(industry, ui_type)`-Bucket. Cold-Start-sicher. Zählt nur Entscheidungen mit `lint_score >= 80` + `user_accepted = true`.
- **Achseninteraktions-Matrix**: explizite Konfliktauflösung zwischen konkurrierenden Achsen (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px Radius). Keine stillen Ad-hoc-Regeln mehr.
- **Automatische `/ux-evolve`-Schleife** (in 4.0 die Standardschleife von `/ux-polish`): lint → polish → re-lint, bis Score ≥ 90, Plateau oder 3 Runden in 4.0 (5 in v3). Quality Gate bei 65.
- **3 neue MCP-Tools** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Lokales Stats-Dashboard**: `uxskill stats --html` schreibt `.ux/stats.html`, das zeigt, was DEINE Installation gelernt hat. Keine Telemetrie, keine globale Aggregation.
- **223 Tests bestehen.** Offline. Deterministisch. Niemals ein LLM-Aufruf.

Vollständige Details in [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Star-Historie

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Was ist ux-skill

ux-skill ist eine **Design-Intelligence-Engine** für KI-Coding-Werkzeuge. Sie läuft als Python-Paket (`pip install uxskill`), als Claude-Code-Plugin und als Multi-Installer für 17 IDEs. Die Engine nimmt ein Projekt-Brief entgegen (Branche, Zielgruppe, Tonalität, Must-haves, verbotene Mittel, Stack, Region) und liefert ein vollständiges empfohlenes Designsystem zurück: Style, Palette, Typographie-Paar, Motion-Presets, Komponenten, exemplarische Marken zum Studieren und die Anti-Pattern-Leitplanken, die einzuhalten sind. Die Empfehlung ist deterministisch, dieselbe Eingabe erzeugt stets dieselbe Ausgabe.

Das Plugin sitzt zwischen Ihnen und dem KI-Coding-Werkzeug. Wenn Sie Claude Code, Cursor oder einen anderen KI-Assistenten bitten, „eine Fintech-Landingpage zu bauen“, improvisiert der Assistent typischerweise, und das Ergebnis wirkt innerhalb von fünf Sekunden KI-generiert (Violett-zu-Blau-Verläufe, drei gleiche Karten, Inter in Display-Größe, „John Doe“ in den Testimonials, 300-ms-Standardübergänge, zentrierter Hero, hüpfende Pfeil-CTAs). ux-skill ersetzt Improvisation durch **strukturierte Einschränkungen**: Sie führen `/ux-discover` aus, um das Briefing zu erfassen und das System zu wählen, `/ux-design`, um den Code zu generieren, und `/ux-lint`, um vor dem Commit zu prüfen, dass er die 171 deterministischen Anti-KI-Slop-Regeln besteht.

Diese README ist die kanonische Referenz. Jeder Befehl, jeder Sub-Agent, jedes Datenmanifest, jeder Installationspfad, jede Brand-Spec, jede Anti-Pattern-Kategorie, alles ist hier dokumentiert. Wenn Sie nach einem Design-Plugin für Claude Code suchen oder KI-Design-Werkzeuge für Cursor, Windsurf oder Codex vergleichen, lesen Sie dies von oben bis unten und [compare.html](https://uxskill.laithjunaidy.com/compare.html) parallel dazu.

---

## Inhaltsverzeichnis

1. [Das Gehirn, was v3.0 ist](#das-gehirn-was-v30-ist)
2. [Schnellinstallation](#schnellinstallation)
3. [Die Zahlen, Live-Vergleich gegen die Top-8-Claude-UX-Skills](#die-zahlen-live-vergleich-gegen-die-top-8-claude-ux-skills)
4. [Architektur, wie die Teile ineinandergreifen](#architektur-wie-die-teile-ineinandergreifen)
5. [Die 18 Slash-Befehle, detaillierte Referenz](#die-18-slash-befehle-detaillierte-referenz)
6. [Die 5 Sub-Agents](#die-5-sub-agents)
7. [Die 11 Datenmanifeste](#die-11-datenmanifeste)
8. [Die 171 Anti-KI-Slop-Regeln, der Linter](#die-171-anti-ki-slop-regeln-der-linter)
9. [Die 160 Brand-DESIGN.md-Specs, nach Kategorie](#die-160-brand-designmd-specs-nach-kategorie)
10. [MCP-Server, der asymmetrische Zug](#mcp-server-der-asymmetrische-zug)
11. [Der Installer für 17 IDEs](#der-installer-für-17-ides)
12. [Anwendungsfälle, konkrete Szenarien](#anwendungsfälle-konkrete-szenarien)
13. [Im Vergleich zu Alternativen](#im-vergleich-zu-alternativen)
14. [Roadmap](#roadmap)
15. [Beitragen](#beitragen)
16. [Lizenz, Autor, Danksagungen](#lizenz-autor-danksagungen)

---

## Das Gehirn: was v3.0 ist

v3.1.0 ist die größte architektonische Umstellung in der Geschichte von ux-skill. Der Recommender wählt nicht mehr Templates aus einem Katalog, die Engine **synthetisiert** pro Brief eine frische Designsprache. Derselbe Brief liefert immer dieselbe Ausgabe (vollständig deterministisch), aber jeder unterschiedliche Brief bekommt sein eigenes neues System. Brand Specs sind keine Templates mehr; sie sind Trainingsdaten, aus denen die Engine das Vokabular lernt. Das System hat Augen auf seine eigene Historie, schließt die Feedback-Schleife lokal und ruft niemals ein LLM auf.

Der Compiler ist ein **deterministischer 7-Achsen-Synthesizer**, warmth, contrast, density, geometry, formality, motion, type_personality. Jeder Brief mappt auf Achsenwerte; Achsenwerte kompilieren zu frischen Palette-, Typografie-, Spacing-, Radius- und Motion-Tokens. Modulare Typoskalen wählen ihr Verhältnis aus dem Contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Layout-Primitives sind responsive by construction (`auto-fit minmax(min(N, 100%), 1fr)` + Container-Queries). Kaputte Layouts können nicht emittiert werden, weil sie nicht repräsentierbar sind.

Es gibt drei automatisch dispatchierte Modi: `strict_brand` (`reference_brands=[stripe] strict=True` → 100 % Stripe-Tokens, schnellster Weg); `brand_anchor` (`reference_brands=[stripe]` → 70 % Stripe + 30 % achsenadaptiert aus 4 Geschwistermarken); und `pure_synthesis` (keine Marke genannt → unendlicher Raum, 8 achsenpassende Beispiele zu einer neuen Designsprache destilliert). Konkurrierende Achsen werden durch eine dokumentierte **Achseninteraktions-Matrix** aufgelöst, dense + corporate kompiliert zu 4px (density gewinnt, Bloomberg-Schule), airy + corporate zu 12px (formality gewinnt, Luxus), soft + playful zu 18px Radius, sharp + corporate zu 2px. Keine stillen Ad-hoc-Regeln in der Implementierung.

Das **Decisions-Ledger** (`.ux/decisions.jsonl`, Schema `_v: 1` festgeschrieben) schließt die Feedback-Schleife. Der Recommender ordnet Kandidaten jetzt nach früheren Erfolgen im selben `(industry, ui_type)`-Bucket neu. Kaltstartsicher: Unter 3 Vorläufern überspringt er das. Es zählen nur Entscheidungen mit `lint_score >= 80` UND `user_accepted = true`. Dazu führt `/ux-polish` lint → polish → re-lint aus, bis Score ≥ 90, Plateau oder 3 Runden, mit einem Quality Gate bei 65, unter dem die Ausgabe ohne `--force` verweigert wird. Ergebnis: Jede Installation wird auf ihrem eigenen Korpus klüger, jeder Lauf ist über Maschinen hinweg reproduzierbar, und die Engine bleibt vollständig offline.

---

## Schnellinstallation

Drei Installationswege. Wählen Sie den, der zu Ihrer Umgebung passt.

### Weg 1: Claude-Code-Marketplace (kanonisch)

Wenn Sie in Claude Code arbeiten, installieren Sie über den Plugin-Marketplace:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Damit werden alle 18 Slash-Befehle (plus 7 alte Namen, die bis 4.1 als Aliase bleiben) und 5 Sub-Agents in Ihre Claude-Code-Session eingebunden. Nach der Installation führen Sie `/ux-init` aus, um das projektspezifische Zustandsverzeichnis `.ux/` einzurichten und zu prüfen, dass die Python-Engine erreichbar ist.

### Weg 2: pip (universell)

Wenn Sie außerhalb von Claude Code arbeiten (Cursor, Windsurf, CLI, CI), installieren Sie das Python-Paket:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

Das Paket stellt sowohl `ux` als auch `uxskill` als CLI-Entrypoints bereit, beide sind dasselbe Binary.

### Weg 3: npx (kein Python erforderlich)

Wenn Sie Python nicht direkt verwalten möchten, bootstrappt der npx-Wrapper alles über `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Installation verifizieren

```bash
ux stats
# {
#   "version": "4.0.0b2",
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

Die zwölf Zähler ergeben zusammen 1.262 Einträge. Wenn ein Zähler 0 zurückgibt, fehlt die JSON-Datei; öffnen Sie dann ein Issue unter [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Die Zahlen: Live-Vergleich gegen die Top-8-Claude-UX-Skills

Die Sternzahlen wurden zuletzt am **2026-05-28** über `gh api` verifiziert. ux-skill (Laith0003/ux-skill) ist der jüngste Neuzugang, wir sind klein in Bekanntheit, tief in Architektur. Der Vergleich unten ist ehrlich: wo wir verlieren, wo wir gewinnen.

| Plugin | Sterne | Architektur | Slash-Befehle | Linter (CI-fähig) | Brand-Specs | Komponenten | Motion-Presets | Unterstützte IDEs |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, einzelne Skill | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 Skills + Preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + forschungsgestützter Geschmack | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Einzige 62-KB-SKILL.md + Skripte | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | MCP-verdrahtete Skill-Bibliothek | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Mono-ästhetische Skill | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Anti-Slop-Design-Skill | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3-Komponenten + Audit | 1 | - |, | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python-Engine + 12 Manifeste + 18 Befehle + 5 Sub-Agents + CI-Linter** | **18** | **171 deterministische Regeln** | **160** | **148** | **57** | **17** |

### Wo wir verlieren

- **Bekanntheit.** Sie haben Hunderttausende Sterne. Wir haben 14. Setzen Sie einen Stern, das ist die günstigste Form der Unterstützung.
- **Markenwiedererkennung.** ui-ux-pro-max und open-design haben einen Vorsprung, der sich in Monaten misst, nicht in Tagen.
- **Marketing-Politur.** Sie haben Screenshots, Demo-Videos und eine auffindbare Landingpage. Wir haben eine gründliche README und eine schlanke Landingpage.

### Wo wir gewinnen

- **Komponentenbibliothek:** 148 dokumentierte Komponenten mit Anatomie, Zuständen, verwendeten Tokens und Motion-Specs. Keine der anderen 8 liefert ein Komponentenmanifest.
- **Motion-Presets:** 57 stack-fertige Einträge (Framer Motion, GSAP, CSS) mit reduced-motion-Fallbacks. Keine der anderen liefert ein Motion-Manifest.
- **Anti-Pattern-Linter:** 171 deterministische Regeln, läuft in CI, beendet mit Non-Zero bei Critical/High. Keine der anderen liefert einen deterministischen Linter.
- **Brand-Specs:** 160 echte DESIGN.md-Specs (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude und 96 weitere). Keine der anderen liefert eine Markenbibliothek.
- **17 unterstützte IDEs:** dieselbe Engine, anderer Klebstoff je IDE.
- **18 Slash-Befehle:** Discovery, Generierung (Seiten, Komponenten, Dashboards, aus einem Bild), Audit, Lint, Polish-Schleife, Fix-Schleife, Case-Study, Workshop, Copy, Motion, A11y, Conductor, vollständig integriert.

Vollständige Tabelle Seite an Seite unter [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Architektur: wie die Teile ineinandergreifen

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

### Wie die Engine tatsächlich arbeitet

1. **Eingabe.** Sie geben ein Briefing an, entweder interaktiv über `/ux-discover` (10 Felder) oder nicht interaktiv über Flags an `ux recommend`.
2. **5 parallele Suchen.** Die Engine führt fünf Lookups gleichzeitig über die Manifeste aus:
   - **Branche → recommended_styles** (industries.json)
   - **Style → Kompatibilität von Palette, Typografie und Motion** (styles.json)
   - **Tonalität × Must-have → Palettenfilter** (palettes.json)
   - **Stack → Komponentenkompatibilität + Motion-Presets** (tech-stacks.json, motion-presets.json)
   - **Verboten + Region → Leitplanken + Shortlist exemplarischer Marken** (anti-patterns.json, brands/)
3. **Merge.** Ein deterministischer Merger ordnet die Kandidaten, löst Konflikte auf (z. B. erzwingt ein Must-have Dark Mode den Palettenmodus) und gibt ein einziges empfohlenes System aus.
4. **Ausgabe.** Ein JSON-Dokument mit dem gewählten Style, der Palette, dem Typografie-Paar, den 5 besten Motion-Presets, den 12 besten Komponenten, den 5 besten exemplarischen Marken und allen 171 aktiven Anti-Pattern-Leitplanken. Dazu ein Begründungsblock, der jede Wahl erklärt.
5. **Generierung.** Nachgelagerte Befehle (`/ux-design` in seinen Modi Seite, Komponente, Dashboard und Bild sowie `/ux-system`) nutzen die Empfehlung, um über die Sub-Agents echten Code zu erzeugen.
6. **Verifikation.** `/ux-lint` scannt den generierten Code erneut gegen die 171 Regeln. Beendet mit Non-Zero bei Critical/High in CI.

**Neu in v3.** Der Recommender ordnet Kandidaten jetzt aus `engine/decisions/` anhand von `.ux/decisions.jsonl` neu (es zählen nur Entscheidungen mit `lint_score >= 80` UND `user_accepted = true`; kaltstartsicher unter 3 Vorläufern). Der Generator kann an `engine/synthesizer/` übergeben, einen deterministischen 7-Achsen-Compiler, der pro Briefing frische Tokens für Palette + Typografie + Abstände + Radius + Motion erzeugt, statt Vorlagen aus einem Katalog zu wählen. Details unter [Das Gehirn, was v3.0 ist](#das-gehirn-was-v30-ist).

**Python denkt. HTML zeigt. Markdown verkettet.**

---

## Die 18 Slash-Befehle: detaillierte Referenz

Jeder Befehl wird als `.md`-Datei unter `commands/` ausgeliefert, mit `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` und `output state file`. Die Beschreibungen unten sind verdichtet; die vollständige Quelle ist die maßgebliche Spezifikation.

Die Befehle sind in sieben Gruppen geordnet: **Bootstrap & Inventar**, **Discovery & Empfehlung**, **Generierung**, **Audit & Verifikation**, **Fix & Polish**, **Discovery & Narrativ** und **Conductor**. Sieben Namen aus 3.x funktionieren bis 4.1 weiter als [Aliase](#aliase-entfallen-in-41).

### Bootstrap & Inventar

#### `/ux-init`: das Projekt bootstrappen

- **Was:** Erkennt, welche IDE Sie verwenden (`.claude/`, `.cursor/`, `.windsurf/` usw.), installiert das passende Artefakt, prüft, dass die Python-Engine erreichbar ist, und gibt einen Statistik-Schnappschuss aus. `--stats` gibt nur den Schnappschuss aus: Version + Eintragszähler der Datenmanifeste.
- **Wann verwenden:** Erste Installation in einem neuen Projekt. Nach dem Klonen eines Projekts, das ux-skill nutzt. Nach `pip install --upgrade uxskill`. `--stats` nach der Installation, nach einem Upgrade oder wenn eine Empfehlung überraschende Auswahlen liefert und Sie unvollständige Manifeste vermuten.
- **Wann überspringen:** Sie haben es in diesem Projekt bereits ausgeführt und nichts hat sich geändert. `--stats` muss nie übersprungen werden: Es ist ein Lesezugriff von 50 ms.
- **Aufruf:** `/ux-init` (ohne Argumente), `/ux-init --stats` oder `uxskill init` / `uxskill stats` von der CLI aus. `--decisions` ergänzt die Zusammenfassung des Decisions-Ledgers; `--html` schreibt `.ux/stats.html`.
- **Ausgabe:** IDE-spezifisches Artefakt (siehe [Der Installer für 17 IDEs](#der-installer-für-17-ides)) + `.ux/`-Verzeichnis + stdout-Zusammenfassung. `--stats`: JSON nach stdout (siehe [Installation verifizieren](#installation-verifizieren) oben).
- **Verkettet mit:** als Nächstes `/ux-discover`. `--stats` dient nur der Diagnose.

#### `/ux-mcp`: die Engine als MCP-Server betreiben

- **Was:** Startet die Engine als Model-Context-Protocol-Server über stdio. 25 Tools (Recommender, Linter, Persistenz, Synthesizer, Decisions-Ledger, Bildextraktion, die Datenmanifeste sowie Bauen, Importieren, Verbessern, Erweitern, Exportieren und Prüfen eines Designsystems) werden von jedem MCP-fähigen Host aus aufrufbar, ohne das Plugin.
- **Wann verwenden:** Sie arbeiten in einem anderen MCP-fähigen Host und wollen dieselbe Engine. Sie betreiben eine Multi-Agent-Pipeline, die eine einzige Quelle für Design-Vorgaben braucht. Sie wollen den Recommender oder den Linter als langlebigen Prozess in CI.
- **Wann überspringen:** Sie arbeiten in Claude Code mit installiertem Plugin; die Slash-Befehle erreichen die Engine bereits. Sie brauchen eine einmalige Antwort; `uxskill recommend` oder `uxskill lint` ist einfacher.
- **Aufruf:** `/ux-mcp` oder `ux-mcp` in der Shell nach `pip install 'uxskill[mcp]'`.
- **Ausgabe:** Ein stdio-JSON-RPC-Server. Siehe [MCP-Server](#mcp-server-der-asymmetrische-zug) und `commands/ux-mcp.md` für die Konfiguration je Client.
- **Verkettet mit:** Nichts; es ist ein Transport, kein Schritt.

### Discovery & Empfehlung

#### `/ux-discover`: die Zwangsfunktion (10-Felder-Intake, Framing, Empfehlung)

- **Was:** Der verpflichtende 10-Felder-Intake, durch den jedes Projekt vor einem Generierungsbefehl geht. Projekttyp, Zielgruppe, Hauptziel, Tonalität, Must-haves, Verbotenes, Referenzmarken, Stack, Region, Erfolgsmetrik. **Keine Improvisation.** Verbotene Phrasen („modern“, „clean“) zwingen den Nutzer zu konkreten Angaben. Danach läuft der Recommender: Die 5 parallelen Suchen der Python-Engine über 12 Manifeste liefern ein zusammengeführtes Designsystem (Branche → Style → Palette → Typografie → Motion + Komponenten + exemplarische Marken + Leitplanken).
- **Modi:** `--frame` erfasst Für-wen, Outcome, Hypothese und Erfolgssignal in einem Framing-Block mit vier Feldern, leichter als der vollständige Intake. `--recommend` führt nur den Recommender aus, aus einem gespeicherten Briefing oder einmaligen Flags.
- **Wann verwenden:** Vor jedem `/ux-design` oder `/ux-system`. Immer wenn ein früheres Briefing veraltet ist. `--frame` zu Beginn eines Projekts, Sprints oder Einzelauftrags oder mittendrin, wenn ein Gespräch abgedriftet ist. `--recommend`, wenn Sie ein müde wirkendes Produkt neu ausrichten.
- **Wann überspringen:** Sie beheben einen Bug (`/ux-fix`). Sie führen nur einen Linter-Durchgang aus (`/ux-lint`). Das Briefing ist seit der letzten Session unverändert.
- **Aufruf (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` oder `/ux-discover --recommend`.
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
- **Ausgabe:** `.ux/last-discovery.json` (das 10-Felder-Briefing), `.ux/last-recommendation.json` (gewählter Style, Palette, Typografie-Paar, 5 beste Motion-Presets, 12 beste Komponenten, 5 beste exemplarische Marken, alle 171 aktiven Anti-Pattern-Leitplanken, plus Begründung) und mit `--frame` `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Verkettet mit:** `/ux-design [extra brief]` → Frontend-Code, verankert in der Empfehlung. `/ux-design --component <name>` → eine Komponente, ausgerichtet an den ermittelten Vorgaben. `/ux-system` → vollständiges Designsystem aus der Empfehlung. `/ux-lint` → den generierten Code verifizieren.

### Generierung

#### `/ux-design`: eine schöne, Anti-Slop-Oberfläche aus einem Brief generieren

- **Was:** Generiert ein vollständiges, produktionsreifes Frontend-Artefakt (Landing, Marketing-Site, App-Shell) aus dem Discovery-Briefing + der Empfehlung. Entsendet `frontend-engineer` mit kreativer Richtung aus den Anti-Slop- und Arsenal-Referenzen. Das Briefing oder ein Flag wählt einen von vier Modi:
  - **Seite** (Standard): eine vollständige Seite oder Oberfläche mit mehreren Sektionen. Schreibt `.ux/last-design.json`.
  - **`--component [name]`**: eine einzelne, produktionsreife Komponente (Button, Modal, Navbar, Sidebar, Card, Tabelle, Formular, Chart). Alle vier Interaktionszustände, barrierefrei, markentreu. Sucht die Komponente zuerst in `.ux/last-recommendation.json` und fällt auf eine direkte Manifestabfrage zurück. Schreibt `.ux/last-component.json`.
  - **`--dashboard`**: Disziplin bei der Datendichte, Bento-Layout, tabellarische Monospace-Ziffern, Sparkline-Patterns, keine Kartenflut, semantische Statusfarben, sparsame Motion. Keine Marketing-Site mit aufgeklebten Charts. Schreibt `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: liest ein Referenzbild (PNG/JPG/WebP) mit reiner Pillow-CV (dominante Palette, Polarität der Fläche, Schriftsignal), gleicht es mit den Manifesten für Paletten und Styles ab und baut aus der resultierenden Empfehlung. `--extract-only` hört nach der Extraktion auf. Schreibt `.ux/last-image-extract.json`.
- **Wann verwenden:** „Designe ein“, „bau mir ein“, „generiere eine Landingpage“, „erstelle ein Dashboard“, „mach eine Komponente“, „bau einen Button“, „designe das Admin-Panel“, „Operator-Konsole“, „KPI-Board“, „bau es wie diesen Screenshot“, jede freie Anfrage nach einem visuellen Ergebnis.
- **Wann überspringen:** Sie wollen einen Review, keinen Build (verwenden Sie `/ux-audit` oder `/ux-critique`). Backend- oder Infrastrukturarbeit.
- **Aufruf:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Ausgabe:** Generierter Code (HTML / Blade / JSX / Vue / Astro) plus die Zustandsdatei des Modus.
- **Verkettet mit:** `/ux-lint` → gegen Leitplanken verifizieren. `/ux-polish` → kosmetischer Durchgang. `/ux-a11y` → Accessibility-Audit. `/ux-copy` → Microcopy-Review. `/ux-fix` → Findings als atomare Commits anwenden.

#### `/ux-system`: ein vollständiges Starter-Designsystem generieren

- **Was:** Schlägt ein vollständiges Starter-Designsystem für ein Projekt vor, das noch keines hat, Tokens (Farbe, Typographie, Raum, Motion, Radius, Schatten), Foundation-Dokumente, Komponentenverträge, Dark-Mode-Paarungen, Theme-Switcher. Entsendet `design-system-architect`.
- **Wann verwenden:** „Wir haben kein Designsystem", „bau uns ein System", „schlag Tokens vor", „was sollte unser Theme sein", „richte unser DS ein".
- **Wann überspringen:** Das Projekt hat bereits ein Designsystem; verwenden Sie stattdessen `/ux-design --component` gegen das bestehende System. Backend oder Infrastruktur.
- **Aufruf:** `/ux-system create` (die Foundations-Engine), `/ux-system enhance --from <file>` (ein vorhandenes System messen), `/ux-system extend --from <file> --add <foundation>` (es ergänzen, ohne es zu ändern) oder `/ux-system` (der Ablauf aus 3.x; führt zuerst die Discovery aus, falls noch keine hinterlegt ist).
- **Ausgabe:** `tokens.json`, `foundations.md`, `components/*.md`-Verträge, optionale Tailwind- / vanilla- / SCSS-Emission. Schreibt `.ux/last-system.json` für den Verkettungskontext.
- **Verkettet mit:** `/ux-design --component` → gegen das neue System bauen. `/ux-design` → eine Oberfläche mit den neuen Tokens generieren.

#### `/ux-motion`: Motion-Behandlung

- **Was:** Generiert die Motion-Schicht einer Oberfläche, Dauern, Easings, Choreografie, reduced-motion-Fallbacks, Performance-Disziplin. Auditiert auch bestehende Motion gegen die 5 Dimensionen (Timing, Easing, Bedeutung, reduced-motion, Performance).
- **Wann verwenden:** „Motion-Check", „sind die Animationen gut", „repariere die Motion", „prüfe die Animationen", „Motion-Audit", „Performance-Durchgang über die Motion".
- **Wann überspringen:** Die Oberfläche hat keine Motion (verwenden Sie `/ux-audit` oder `/ux-polish`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-motion path/to/component.tsx` (Audit-Modus) oder `/ux-motion --generate hero-entry` (Generierung).
- **Ausgabe:** Aktualisierter Code (im Generierungsmodus) oder `.ux/last-motion.json`-Bericht (im Audit-Modus).
- **Verkettet mit:** `/ux-fix` → Motion-Findings anwenden. `/ux-polish` → straffen.

### Audit & Verifikation

#### `/ux-lint`: deterministischer Regex-basierter Linter (kein LLM, CI-fähig)

- **Was:** Führt 171 Regeln gegen Ihren Code aus. Kein LLM-Aufruf. Beendet mit Non-Zero bei Critical / High in CI. Quelle: `data/anti-patterns.json`. Die Regeln decken A11y (45), Inhalt (35), Layout (18), Typografie (16), Motion (14), Visuell (14), Qualität (12), Farbe (10), Performance (5), Tiefe (2) ab.
- **Wann verwenden:** Pre-Commit-Hook. CI-Gate. Schneller erster Durchgang über eine große Codebasis, bevor man die Kosten von `/ux-audit` zahlt. Nach `/ux-design` in jedem Modus, um die Generierung zu verifizieren.
- **Wann überspringen:** Sie wollen eine Fix-Schleife (der Linter meldet, er editiert nicht, verketten Sie mit `/ux-polish --fix` oder `/ux-fix`). Sie wollen Geschmacksurteil (verwenden Sie `/ux-critique`).
- **Aufruf (Slash):** `/ux-lint src/`.
- **Aufruf (CLI):** `uxskill lint .` oder `python3 bin/ux-lint.py .` oder `bash bin/ux-lint.sh --ci --fail-on high`.
- **Aufruf (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Ausgabe:** Findings nach stdout (Ort, Regel-ID, Schweregrad, Beweis). Exit-Code 0 wenn sauber, Non-Zero bei Critical/High, wenn `--fail-on high` gesetzt ist.
- **Verkettet mit:** `/ux-polish --fix` → LLM-getriebenes Gegenstück auf denselben Patterns. `/ux-fix` → Findings als Commits anwenden, nach Schweregrad sortiert. `/ux-audit` → vollständiger 6-Linsen-Reasoning-Durchgang. `/ux-next` → den Conductor entscheiden lassen.

#### `/ux-audit`: Design-Audit mit 6 Linsen

- **Was:** Eine strukturierte, meinungsstarke Prüfung gegen sechs Linsen (Klarheit, Hierarchie, Barrierefreiheit, Stimme, Motion, Geschmack), die nach Schweregrad gekennzeichnete Findings erzeugt. Bericht im Polaris-Stil. Liest zuerst `.ux/last-frame.json`, Zielgruppe und Outcome verankern den Schweregrad jedes Findings.
- **Wann verwenden:** Die Oberfläche existiert und Sie wollen eine vertretbare Kritik. „Auditiere", „prüfe die UX", „ist das gut", „was ist kaputt", „zerlege das".
- **Wann überspringen:** Die Oberfläche existiert noch nicht (verwenden Sie `/ux-design`). Der Nutzer will eine einzelne Linse (verwenden Sie den gezielten Befehl: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Der Nutzer will eine Geschmacksmeinung (verwenden Sie `/ux-critique`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-audit https://example.com/pricing` oder `/ux-audit src/components/Pricing.tsx`.
- **Ausgabe:** Schreibt `.ux/last-audit.json`, `findings`-Array mit `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Verkettet mit:** `/ux-fix` → Findings anwenden. `/ux-polish` → kosmetischer Durchgang. `/ux-design` → falls strukturelles Redesign nötig.

#### `/ux-a11y`: WCAG-2.1-AA-Audit + Höflichkeitsprüfungen

- **Was:** Ein strukturierter WCAG-2.1-AA-Audit plus die Höflichkeitsprüfungen, die automatisierte Werkzeuge passieren, aber echte Nutzer immer noch verletzen (Fokus-Sichtbarkeit, Fehlerspezifizität, Motion-Präferenzen, Tastaturfallen, Farbabhängigkeit).
- **Wann verwenden:** Pre-Ship-Accessibility-Gate. Nach einem Redesign. „Accessibility-Check", „WCAG-Audit", „ist das barrierefrei", „A11y-Review", „Screen-Reader-Test", „Tastatur-Navigations-Check".
- **Wann überspringen:** Nicht nutzerseitig. Backend oder Infrastruktur. Skizzen in Arbeit.
- **Aufruf:** `/ux-a11y https://example.com` (Live-URL bevorzugt, automatisierte Werkzeuge und Tastaturtests funktionieren nur live).
- **Ausgabe:** Schreibt `.ux/last-a11y.json`, `findings`-Array mit `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, `beyond_wcag`-Array, `severity_counts`.
- **Verkettet mit:** `/ux-fix` → Findings als Commits anwenden. `/ux-copy` → Alt-Texte und Formular-Fehler-Verdrahtung als Teil eines Copy-Durchgangs korrigieren.

#### `/ux-critique`: Geschmacksurteil (3 Treffer, 3 Fehler, 1 strategischer Zug)

- **Was:** Die Meinung eines Designers, kein strukturierter Audit, kein Schweregrad-Score, nur eine straffe, meinungsstarke Einschätzung, die benennt, was funktioniert, was nicht und der einzige strategische Zug, der am meisten verändern würde.
- **Wann verwenden:** „Was denkst du", „ist das gut", „kritisier das", „ehrliche Meinung", „stimmt der Vibe", „fühlt sich das nach uns an", „sollten wir shippen".
- **Wann überspringen:** Der Nutzer will explizit einen strukturierten Audit (verwenden Sie `/ux-audit`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-critique https://example.com`.
- **Ausgabe:** Schreibt `.ux/last-critique.json`, 3 Treffer, 3 Fehler, 1 strategischer Zug, plus Prosa.
- **Verkettet mit:** `/ux-design`, falls die Einschätzung Redesign empfiehlt. `/ux-polish`, falls sie Straffung empfiehlt.

#### `/ux-copy`: Microcopy-Review + -Umschreiben

- **Was:** Bewertet jeden sichtbaren String gegen die Stimm-Rubrik und erzeugt eine Vorher/Nachher-Umschreibung. Fängt: „Formular enthält Fehler" (generisch), „John Doe" (Platzhalter), KI-fröhlicher feierlicher Copy, generische CTAs, tote Empty States, nutzlose Fehler.
- **Wann verwenden:** Struktur stimmt, aber die Worte schwächeln. „Prüfe den Copy", „repariere die Microcopy", „die Fehlermeldungen sind schlecht", „schreib das um", „strafffe die Strings", „die Buttons klingen generisch", „dieser Empty State ist tot".
- **Wann überspringen:** Layout-Probleme (verwenden Sie `/ux-audit` oder `/ux-polish`). Accessibility-getriebene Copy-Probleme wie Alt-Texte (verwenden Sie `/ux-a11y`). Backend oder Infrastruktur.
- **Aufruf:** `/ux-copy src/views/checkout.blade.php`.
- **Ausgabe:** Schreibt `.ux/last-copy.json`, `strings`-Array mit `{location, severity, before, after, notes}`, plus Rubrik + Locales, die Übersetzung brauchen.
- **Verkettet mit:** `/ux-fix` → Umschreibungen anwenden. `/ux-a11y` → nach den Copy-Fixes erneut prüfen.

### Fix & Polish

#### `/ux-fix`: Findings als atomare Commits anwenden

- **Was:** Liest den neuesten Bericht aus `.ux/` (Audit, Copy, A11y, Motion oder Polish), validiert den Working-Tree und wendet die Findings als atomare Commits über die richtigen Sub-Agents an. Verifiziert erneut, indem der ursprüngliche Befehl wieder ausgeführt wird.
- **Wann verwenden:** Nach dem Ausführen eines Audit-Klassen-Befehls und der Durchsicht der Findings. „Behebe die Findings", „wende die Fixes an", „starte die Fix-Schleife", „patche die Oberfläche", „mach die Änderungen", „los, repariere das".
- **Wann überspringen:** Kein vorheriger Bericht in `.ux/`. Working-Tree ist schmutzig und der Nutzer hat Stash/Commit nicht zugestimmt. Fixes brauchen Design-Urteil, keine mechanische Anwendung (verwenden Sie `/ux-design` für ein Redesign).
- **Aufruf:** `/ux-fix` (erkennt automatisch, welcher Bericht zu beheben ist) oder `/ux-fix --from=last-a11y.json`.
- **Ausgabe:** Atomare Commits pro Finding. Führt den ursprünglichen Befehl erneut aus und aktualisiert die `.ux/last-*.json`-Datei. Gibt eine Zusammenfassung aus.
- **Verkettet mit:** `/ux-next` → der Conductor wählt den nächsten Zug.

#### `/ux-polish`: Lint, Fix, Re-Lint als Schleife + KI-Slop entfernen

- **Was:** Zuerst eine deterministische Schleife auf einer lokalen HTML-Datei: Lint, sechs idempotente Polish-Durchgänge, erneuter Lint, bis der Score 90 erreicht, stagniert oder drei Runden vorbei sind (`--rounds` ändert die Obergrenze). Standardmäßig bleibt das Ergebnis der Schleife in `<file>.evolved.html`, und das Original wird nie angefasst. Nur `--loop-only` oder `--fix` ersetzen das Original, nach einer Prüfung auf einen sauberen Arbeitsbaum, und ein Quality Gate bei 65 verhindert, dass ein durchgefallenes Ergebnis es ohne `--force` ersetzt; mit `--brand-file` gilt die Untergrenze für Markentreue an jedem Ausgang. Danach der Geschmacksdurchgang: Abstandsrhythmus, schärfere Hierarchie, Erkennung von KI-Slop, Token-Konsistenz. Das LLM-getriebene Gegenstück zu `/ux-lint`, das bei Geschmacksfragen Ihr Urteil nutzt. `--loop-only` führt nur die Schleife aus; `--no-loop` nur den Geschmacksdurchgang; `--fix` wendet die Geschmacksbefunde an.
- **Wann verwenden:** Die Struktur stimmt, aber die Ausführung ist locker. „Polier das“, „straff das“, „entferne den KI-Slop“, „mach es premium“, „lass es weniger nach KI aussehen“, „die Abstände fühlen sich falsch an“, „das wirkt generisch“, „braucht mehr Geschmack“, „verbessere bis Score 90+“, „mach es versandfertig“.
- **Wann überspringen:** Der Oberfläche fehlt Kernfunktionalität (das zuerst beheben). Braucht ein Redesign, kein Polish (verwenden Sie `/ux-design`). Copy-Probleme (verwenden Sie `/ux-copy`). Motion-Probleme (verwenden Sie `/ux-motion`). A11y-Probleme (verwenden Sie `/ux-a11y`).
- **Aufruf:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Ausgabe:** `<file>.evolved.html` aus der Schleife (ersetzt das Original nur mit `--loop-only` oder `--fix`), aktualisierter Code mit `--fix`, `.ux/last-evolve.json`, eine Zeile in `.ux/decisions.jsonl` und `.ux/last-polish.json`, das die Geschmacksbefunde beschreibt.
- **Verkettet mit:** `/ux-lint` → prüfen, dass der Polish hält. `/ux-a11y` → Barrierefreiheit erneut prüfen.

### Discovery & Narrativ

#### `/ux-research`: Forschungsplanung + -synthese

- **Was:** Planungsmodus: schreibt Interviewleitfäden, Umfragen, Recruiting-Screener. Synthesemodus (`--synthesize`): verdaut Interviews, Analytics, Wettbewerber-Sites, A/B-Ergebnisse, Support-Tickets zu Empfehlungen. Entsendet `research-synthesizer`.
- **Wann verwenden:** „Plan eine Forschungsstudie", „ich brauche Interviewfragen", „designe eine Umfrage", „wie rekrutiere ich Nutzer", „User-Testing-Plan", „Tagebuchstudie", „Präferenztest", „Fake-Door", „Smoke-Test", „synthetisiere meine Interviewnotizen".
- **Wann überspringen:** Antwort ist bereits mit hoher Sicherheit bekannt. Reversible Entscheidungen mit geringem Risiko. Backend oder Infrastruktur.
- **Aufruf:** `/ux-research --plan "loyalty wallet adoption in MENA"` oder `/ux-research --synthesize interviews/*.md`.
- **Ausgabe:** Schreibt `.ux/last-research.json`, Forschungsplan oder synthetisierte Themen + Belege + Empfehlungen.
- **Verkettet mit:** `/ux-discover --frame` → Befunde in ein Frame integrieren. `/ux-design` → aus den Befunden generieren. `/ux-workshop` → einen Workshop mit der Forschung als Input durchführen.

#### `/ux-workshop`: 5-Phasen-Design-Thinking-Workshop

- **Was:** Moderiert einen Discovery-/Design-Thinking-Workshop von Anfang bis Ende. Fünf sequenzielle Phasen (Exploration → Heatmap → Stakeholder-Map → Lösungsskizze → Game-Plan). Zeitgetaktet. Konkrete Artefakte je Phase. Endet mit einer Entscheidung, nicht „interessanten Findings".
- **Wann verwenden:** Echte Frage, echte Teilnehmer, echtes Zeitbudget. „Mach einen Workshop", „moderiere ein Discovery", „lass uns eine Design-Thinking-Session machen", „ich habe Stakeholder für eine Stunde, was machen wir", „kicke das Projekt an".
- **Wann überspringen:** Das Briefing ist bereits klar und abgegrenzt. Solo-Brainstorm (verwenden Sie `/ux-design` oder `/ux-discover --frame`). Das Team steckt mitten in der Umsetzung, nicht in der Discovery.
- **Aufruf:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Ausgabe:** Schreibt `.ux/last-workshop.json`, Game-Plan + Artefakte je Phase.
- **Verkettet mit:** `/ux-design` → den Game-Plan ausführen. `/ux-research` → Lücken füllen, die der Workshop sichtbar gemacht hat. `/ux-case-study` → die Reise publizieren.

#### `/ux-case-study`: veröffentlichbare Case-Study (Wfrah-Editorial-Format)

- **Was:** Generiert eine Projekt-Case-Study im rein monochromen Editorial-Format, Wfrah-Typografie, Haarlinien-Trenner, nummerierte Sektionscodes von (A) bis (G), zweisprachig sicheres Layout. Ein Dokument, keine Marketing-Broschüre. Liest aus `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Wann verwenden:** Nach Launch. Nach einem diskreten Meilenstein. „Schreib eine Case-Study", „Case-Study dieses Projekt", „mach das Abschluss-Dokument", „publizier diese Arbeit", „Portfolio-Stück".
- **Wann überspringen:** Dem Projekt fehlen Daten, um die Sektionen (A) bis (G) zu füllen. Der Nutzer will eine Marketing-Landing, keine Case-Study (verwenden Sie `/ux-design`).
- **Aufruf:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Ausgabe:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Verkettet mit:** Terminalbefehl, meist das Ende eines Projekts.

### Conductor

#### `/ux-next`: Workflow-Conductor (nur-lesend)

- **Was:** Liest jede `.ux/last-*.json` und benennt den nächsten Befehl mit dem höchsten Hebel. Ein Conductor, kein Bauender. Nur-lesend.
- **Wann verwenden:** Zwischen Befehlen. „Was sollte ich als Nächstes tun", „was ist der nächste Zug", „entscheide für mich", „wohin gehen wir von hier".
- **Wann überspringen:** Keine vorherigen Berichte in `.ux/`. Sie haben einen konkreten nächsten Befehl im Sinn.
- **Aufruf:** `/ux-next` (ohne Argumente) oder `/ux-next --focus=a11y`.
- **Ausgabe:** Stdout, empfohlener nächster Befehl + Begründung.
- **Verkettet mit:** Welchen Befehl auch immer er wählt.

#### `/ux-expert`: Consulting-Hook

- **Was:** Bringt die Kontaktdaten des Plugin-Erstellers an die Oberfläche, wenn ein Nutzer nach einem echten UX-Experten fragt. Kurz, direkt, ohne Marketing.
- **Wann verwenden:** „Wer hat das gebaut", „ich brauche einen UX-Experten", „machst du Consulting", „kann ich jemanden dafür engagieren", „steckt ein Mensch hinter diesem Plugin".
- **Wann überspringen:** Der Nutzer fragt nach Plugin-Features, nicht nach Consulting.
- **Aufruf:** `/ux-expert`.
- **Ausgabe:** Kurze Kontaktkarte mit LinkedIn / E-Mail / Repo.

### Aliase, entfallen in 4.1

Sieben Befehle aus 3.x sind in den 18 oben aufgegangen. Ihre Namen funktionieren noch ein Release lang: Jeder Alias sagt, wohin er umgezogen ist, und führt dann den neuen Befehl mit denselben Argumenten aus.

| Alter Befehl | Jetzt | Hinweise |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | Derselbe Framing-Block, dieselbe `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | Das MCP-Tool `ux_recommend` bleibt unverändert |
| `/ux-stats` | `/ux-init --stats` | Schnappschuss, nur lesend |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | Der Alias behält die alte Obergrenze von fünf Runden; `/ux-polish` allein hört nach drei auf |
| `/ux-component` | `/ux-design --component` | Dieselbe `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | Dieselbe `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Ohne `--extract-only` wird aus dem Bild gebaut |

### Befehlskettengraph

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

## Die 5 Sub-Agents

Sub-Agents sind rollenspezifische Generatoren, die von Befehlen entsandt werden. Sie laufen nie eigenständig, sie werden von `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research` usw. aufgerufen. Jeder Agent hat eine klar definierte Zuständigkeit: Er entscheidet NICHT über das Briefing; er setzt es um.

### `frontend-engineer`

- **Besitzt:** Produktionsreifen Frontend-Code (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro) mit Anti-KI-Slop-Disziplin.
- **Entsandt von:** `/ux-design` (Modi Seite, Komponente, Dashboard und Bild), `/ux-fix`.
- **Eingaben:** Brief + kreative Richtung + Tokens (aus `.ux/last-recommendation.json`).
- **Ausgaben:** Funktionierender Code, der von generischer KI-Ausgabe unterscheidbar ist. Keine Violett-Verläufe, kein zentrierter Hero, keine drei gleichen Cards, kein Inter in Display-Größe, kein „John Doe", keine Emojis, keine 300-ms-Standards.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Besitzt:** Motion in produktionsreifem Frontend-Code, Framer Motion, GSAP, CSS-Animationen. Dauern, Easings, Choreografie, reduced-motion-Fallbacks, Performance-Disziplin.
- **Entsandt von:** `/ux-design` (jeder Modus), `/ux-motion --fix`.
- **Eingaben:** Motion-Brief + Tokens + die 57 Motion-Presets aus `data/motion-presets.json`.
- **Ausgaben:** Motion, die ihren Platz verdient. Stets in `prefers-reduced-motion`-Fallbacks eingehüllt. Stets gegen Core Web Vitals getestet.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Besitzt:** Die Strings, die ausgeliefert werden, Fehlermeldungen, Empty States, CTAs, Loading States, Erfolgsmeldungen, Toasts, Hilfstext, Formularlabels, Buttontext.
- **Entsandt von:** `/ux-copy --fix`, `/ux-design` (jeder Modus), `/ux-discover --frame`.
- **Eingaben:** Stimmprofil (benannt oder eingefügt) + die Strings der Oberfläche.
- **Ausgaben:** Produktions-Microcopy konsistent über alle Zustände einer Oberfläche angewandt, damit das Produkt wie ein Produkt klingt, nicht wie zehn. Verbote: „Formular enthält Fehler", „John Doe", KI-fröhlicher feierlicher Copy, generische CTAs, tote Empty States.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Besitzt:** Das Verdauen von Forschungseingaben (Interviews, Analytics, Wettbewerber-Sites, A/B-Ergebnisse, Support-Tickets) zu umsetzbaren Designempfehlungen.
- **Entsandt von:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Eingaben:** Rohforschung, Transkripte, Exporte, Wettbewerber-URLs, Support-Cluster.
- **Ausgaben:** Themen, Belege, Empfehlungen. Designt nie die Antwort, gibt dem Designer das Substrat, aus dem zu gestalten ist.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Besitzt:** Vollständige Designsysteme, Tokens (Farbe, Typographie, Raum, Motion, Radius, Schatten), Foundation-Dokumente, Komponentenverträge, Dark-Mode-Paarungen, Theming-Schicht.
- **Entsandt von:** `/ux-system`, `/ux-design --component`, wenn kein System existiert.
- **Eingaben:** Brand-Brief + `.ux/last-recommendation.json` (Style + Palette + Typographie-Paar + Motion-Presets).
- **Ausgaben:** Ein kohärentes, meinungsstarkes, produktionsreifes System, gegen das nachgelagerte Agents bauen können, ohne Grundlagen neu entscheiden zu müssen. Tokens-JSON, Foundations-MD, Komponentenverträge, Dark-Mode-Mapping.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Sub-Agent-Dispatch-Protokoll

Wenn ein Befehl einen Sub-Agent entsendet, übergibt er:

1. Das Brief / die Empfehlung (aus `.ux/` geladen).
2. Den relevanten Manifest-Ausschnitt (z. B. erhält `frontend-engineer` den gewählten Style + Palette + Komponenten; `motion-engineer` erhält die gewählten Motion-Presets).
3. Die 171 Anti-Pattern-Leitplanken (stets aktiv).
4. Ein Erfolgskriterium (was das Artefakt leisten muss).

Sub-Agents geben zurück:

1. Das Artefakt (Code, Dokument, System).
2. Einen Begründungsblock (warum diese Auswahl).
3. Eine Selbstprüfung gegen die Leitplanken (welche Regeln sie verifiziert haben).

Der aufrufende Befehl führt dann automatisch `/ux-lint` aus, bevor er sich für fertig erklärt.

---

## Die 11 Datenmanifeste

Die Datenschicht ist das Gehirn. Jeder Befehl liest aus ihr; die Engine merged darüber; der Linter scannt gegen sie. Alle Dateien liegen unter `data/` und kapseln ihre Einträge in `{_meta, entries}` zur Schemaversionierung.

### `styles.json`: 84 Design-Styles

| Feld | Beschreibung |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalistisch / Schweizerisch, Brutalistisch, Editorial, Glassmorphismus, Neumorphismus, Bento, Skeuomorph, Industriell, Maximalistisch, KI-Futuristisch, MENA-modern, Vaporwave usw. |
| `sample entry` | `swiss-international`, „Das Raster ist Gesetz. Die Typographie leistet die Schwerarbeit. Dekoration ist Scheitern." |

Verwendet von: `/ux-discover`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 Farbpaletten

| Feld | Beschreibung |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (hell/dunkel), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazin, klinisch, verspielt, brutalistisch, monochrom, juwelenfarbig, MENA-warm, dev-tools-dunkel usw. |
| `sample entry` | `claude-warm-editorial`, hell, warm/editorial/magazin, canvas #faf9f5, primary #cc785c |

Verwendet von: `/ux-discover`, `/ux-system`. Kontrast verifiziert auf AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 Typographie-Paarungen

| Feld | Beschreibung |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Alle Schriftfamilien haben Lizenz + Quell-URL. Verwendet von `/ux-discover`, `/ux-system`.

### `components.json`: 148 Komponenten

| Feld | Beschreibung |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Formulare, Datenanzeige, Feedback, Overlays, Layout, Inhalt, Marketing, E-Commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega-Navigation, Produkt-Grid, 6-teilige Anatomie, 4 Zustände |

Das ist unser größter Burggraben. Kein anderes Claude-UX-Plugin liefert ein strukturiertes Komponentenmanifest.

### `industries.json`: 184 Branchenregeln

| Feld | Beschreibung |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Finanzdienstleistungen, Gesundheitswesen, Bildung, E-Commerce, SaaS B2B, SaaS B2C, Developer Tools, Medien, Gaming, Reisen, Immobilien, MENA-spezifisch usw. |
| `sample entry` | `fintech-neobank`, hohes Vertrauen, regulatorische Disclosures, Saldo-/Transaktions-Primär-UI, mobile-first für täglichen Gebrauch |

Verwendet vom Recommender (`/ux-discover`) als erste parallele Suchachse.

### `chart-types.json`: 35 Diagrammtypen

| Feld | Beschreibung |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Vergleich, Zeitreihen, Verteilung, Zusammensetzung, Beziehung, Fluss, Geografisch |
| `sample entry` | `bar-vertical`, vergleicht 4 bis 15 diskrete Kategorien. Die Position auf der x-Achse bildet die Kategorie ab, die Höhe den Wert. |

Verwendet von `/ux-design --dashboard` und `/ux-design --component` (Chart-Instanzen).

### `tech-stacks.json`: 25 Stacks

| Feld | Beschreibung |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, kompatibel mit Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Weitere Stacks: Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 benannte UX-Gesetze

| Feld | Beschreibung |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Entscheidungskosten, Aufmerksamkeit, Gedächtnis, Motorische Kontrolle, Visuelle Wahrnehmung, Sozial, Emotional, Formulare, Fehlerbehandlung, Onboarding, Empty State usw. |
| `sample entry` | `hicks-law`, Die Entscheidungszeit wächst logarithmisch mit der Anzahl der dargestellten Optionen |

Verwendet von `/ux-audit` (6-Linsen-Bewertung) und `/ux-critique` (Geschmacksanker).

### `motion-presets.json`: 57 Motion-Presets

| Feld | Beschreibung |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion-Fallback), `when_to_use` |
| `categories` | Eintritt, Austritt, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-gebunden |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Jedes Preset hat eine reduced-motion-Variante. Stack-fertiger Code für Framer Motion, GSAP und reines CSS.

### `anti-patterns.json`: 171 Regeln

| Feld | Beschreibung |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (Typ, Muster, Flags, Geltungsbereich und bei vielen Regeln eine `post`-Prüfung auf der geparsten Datei), `why`, `fix` |
| `categories` | A11y (45), Inhalt (35), Layout (18), Typografie (16), Motion (14), Visuell (14), Qualität (12), Farbe (10), Performance (5), Tiefe (2) |

Die vollständige Regelliste steht unter [Die 171 Anti-KI-Slop-Regeln](#die-171-anti-ki-slop-regeln-der-linter).

### `brands/*.json`: 160 Brand-Specs

| Feld | Beschreibung |
|---|---|
| `entries` | 160 (plus `_index.json`, das alle listet) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automobil (8) |

Vollständige Liste in [Die 160 Brand-DESIGN.md-Specs](#die-160-brand-designmd-specs-nach-kategorie).

---

## Die 171 Anti-KI-Slop-Regeln: der Linter

ux-skill liefert einen deterministischen Linter: Jede Regel ist ein Muster, und viele ergänzen eine Prüfung auf dem geparsten CSS und Markup, sodass ein Treffer nur in dem Kontext zählt, den die Regel nennt. **Kein LLM.** **Keine API.** **Kein Netzwerk.** Läuft in CI in ~200 ms auf einer typischen Next.js-App. Beendet mit Non-Zero bei Critical- / High-Befunden, wenn `--fail-on high` gesetzt ist.

Die Regeln stammen aus `data/anti-patterns.json` (v2, bevorzugt) mit `references/foundations/anti-patterns.md` als Fallback (v1, Bash). Zwei Binaries werden ausgeliefert: `bin/ux-lint.py` (Python, schnell, erweiterbar) und `bin/ux-lint.sh` (Bash + perl-PCRE, für Umgebungen ohne Python).

### Regeln nach Kategorie

Der vollständige Katalog aller 171 Regeln, nach Kategorie und dann nach Schweregrad geordnet, wird aus `data/anti-patterns.json` erzeugt und steht im [englischen README](README.md#rules-by-category); Regel-IDs und Namen stehen dort so, wie der Linter sie ausgibt. Die Regeln decken A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) ab.

### Linter-Nutzung

**Einmaliger Scan:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## Die 160 Brand-DESIGN.md-Specs: nach Kategorie

Echte Marken. Echte Designsprachen. Echte DESIGN.md-Specs, keine generischen Paletten. Sagen Sie dem Plugin „bau eine Landing im Stil von Stripe" und es liest das tatsächliche Markenvokabular: Stimm-Rubrik, Farbtokens, Motion-Konventionen, Signature Moves, Anti-Moves.

Jede Marke wird als strukturiertes JSON (`data/brands/<slug>.json`) plus Prosa-Referenz (`references/brands/<slug>.md`) ausgeliefert.

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

### Automobil (8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### Warum das wichtig ist

Die anderen 8 populären Claude-UX-Plugins erzeugen „modern minimal" oder „clean dashboard", Varianten derselben Default-Ästhetik. ux-skill erlaubt es Ihnen, nach **Linears Klarheit**, **Stripes Ernsthaftigkeit**, **Apples Zurückhaltung**, **Teslas Monolith**, **Notions Freundlichkeit**, **Cursors Gradient-Disziplin**, **Raycasts Haarlinien-Dichte**, **Claudes warmem Editorial** zu fragen, und die Engine zieht die richtigen Tokens, Stimme, Motion-Konventionen und Signature Moves aus der Brand-Spec.

---

## MCP-Server: der asymmetrische Zug

ux-skill liefert einen **Model-Context-Protocol-Server** aus. Führen Sie `ux-mcp` aus, und die Engine wird zu einem langlebigen stdio-Prozess, den jeder MCP-fähige Host (Claude Desktop, Cursor, Windsurf, generische Agents) aufrufen kann. 25 Tools: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Dieselben Python-Handler, die auch die Slash-Befehle nutzen; dieselben Datenmanifeste; derselbe deterministische Recommender.

**Warum das der asymmetrische Zug ist:** Keine der Top-8-Claude-UX-Skills (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) liefert einen MCP-Server aus. Sie sind in der Claude-Code-Plugin-Runtime eingesperrt. ux-skill ist von jedem Host erreichbar, der MCP spricht, einschließlich Agents, die nie von einem Claude-Code-Plugin gehört haben.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Richten Sie Ihren Client auf das `ux-mcp`-Binary. Vollständige Tool-Dokumentation, JSON-Beispiele und Client-spezifische Konfiguration für Claude Desktop, Cursor und Windsurf liegen unter [docs/mcp.html](docs/mcp.html) und in `commands/ux-mcp.md`.

---

## Der Installer für 17 IDEs

`uxskill init` (oder `/ux-init` innerhalb von Claude Code) erkennt automatisch, welche IDE Sie verwenden, und schreibt das passende Artefakt. Dieselbe Python-Engine. Dieselben Empfehlungen. Anderer Klebstoff je IDE.

| IDE / Werkzeug | Erkennungssignal | Installiertes Artefakt |
|---|---|---|
| Claude Code | `.claude/` oder `CLAUDE.md` | Plugin-Manifest unter `.claude-plugin/plugin.json` + alle 18 Befehle (und 7 Aliase) + alle 5 Sub-Agents |
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

## Anwendungsfälle: konkrete Szenarien

Acht reale Szenarien. Wählen Sie das Ihrer Situation am nächsten kommende und passen Sie den Aufruf an.

### 1. Ein Fintech-Dashboard in Cursor bauen

Sie sitzen in Cursor und arbeiten an einem Dashboard für eine MENA-Neobank. Sie installieren das Plugin und führen Discovery, Empfehlung und dann Dashboard-Generierung aus.

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

Dann fragen Sie in Cursor: *„Generiere die Dashboard-Oberfläche mit der Empfehlung in .ux/last-recommendation.json"*. Cursor liest den `.cursorrules`-Header, lädt die Empfehlung und entsendet eine Dashboard-Generierung mit expliziten Einschränkungen.

### 2. Eine Landing im Stripe-Stil in Claude Code generieren

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Drei Befehle, eine polierte Oberfläche, atomare Commits pro Fix.

### 5. Eine Command-Palette im Linear-Stil entwerfen

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

Die generierte Komponente nutzt Linears echte Farbtokens, Typographie-Stack, Motion-Konventionen, Haarlinien-Dichten, keine „generische dunkle UI".

### 6. Einen 90-minütigen Design-Thinking-Workshop mit Stakeholdern moderieren

Sie haben einen Raum mit 5 Personen für 90 Minuten. Sie wollen, dass sie mit einem Game-Plan rausgehen, nicht mit einem Vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Das Plugin moderiert die fünf Phasen (Exploration → Heatmap → Stakeholder-Map → Lösungsskizze → Game-Plan) von Anfang bis Ende, zeitgetaktet, mit konkreten Artefakten je Phase. Die Ausgabe ist `.ux/last-workshop.json`, der Game-Plan, nicht nur „interessante Findings".

### 7. Nach Launch eine veröffentlichbare Case-Study schreiben

Sie haben die Loyalty-Wallet ausgeliefert. Sie wollen ein Portfolio-Stück.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

Die Case-Study ist ein fertiges, veröffentlichbares Artefakt, kein Entwurf. Reines Monochrom, Editorial-Typographie, bereit für Ihr Portfolio.

### 8. Discovery in einem Nicht-KI-Kontext fahren (nur strukturierter Intake)

Sie grenzen ein Projekt ein. Sie brauchen noch keine Empfehlung, Sie brauchen ein strukturiertes Brief.

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

Sie können das JSON an Ihr Team weitergeben, in ein Notion-Doc einfügen oder in ein separates KI-Werkzeug einspeisen. ux-skill ist auch ein strukturiertes Intake-Werkzeug, nicht nur eine Engine.

### 9. MASTER.md-Persistenz: Ihre Designentscheidungen, im Repo

Nach `/ux-discover` (oder `/ux-discover --recommend`) speichern Sie den gewählten Style + Palette + Typografie + Motion + Komponenten + exemplarische Marken + Leitplanken als gut lesbare Markdown-Datei, die Ihr Team prüfen, diffen und versionieren kann.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Schreibt `.ux/design-system/MASTER.md` (YAML-Frontmatter + Body) und `.ux/design-system/pages/<name>.md` pro generierter Oberfläche über `persist save-page`. Idempotent, dieselbe Eingabe erzeugt byte-identische Ausgabe, daher ist ein erneuter Lauf auf unverändertem Zustand ein No-op in Git.

---

## Im Vergleich zu Alternativen

Kurze Zusammenfassungstabelle. Vollständiger Tabelle-für-Tabelle-Vergleich unter [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimension | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash-Befehle | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Komponenten | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion-Presets | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand-Specs | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Anti-Pattern-Regeln | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-fähiger deterministischer Linter | **ja** | nein | nein | nein | nein | nein | nein | nein | nein |
| Unterstützte IDEs | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery-Gate | **10 Felder** | implizit | implizit | implizit | implizit | implizit | implizit | implizit | implizit |
| `.ux/`-Zustandskette | **ja** | nein | nein | nein | nein | nein | nein | nein | nein |
| Sterne (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Ehrliche Bewertung

- **ui-ux-pro-max** ist größer in Bekanntheit, liefert 18 IDEs, hat BM25-Suche über sein CSV. Es liefert weder Komponentenmanifest, Motion-Manifest, Markenbibliothek noch deterministischen Linter.
- **open-design** hat 19 Skills + Preview, aber nur Claude-Code-Support und keine Anti-Slop-Schicht.
- **hallmark** ist im Geist am nächsten (ebenfalls Anti-Slop), ist aber eine einzelne Skill, keine Engine, keine Manifeste, keine verketteten Befehle.
- **material-3-skill** ist exzellent, wenn Sie ausdrücklich Material Design 3 wollen. Wir konkurrieren nicht auf MD3.

Für vollständige Details je Dimension siehe [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

Als Nächstes, ohne festes Release:

- **Figma-Styles**: Effektstile für Schatten, Rasterstile und Textstile, die an die Feldvariablen gebunden sind, geschrieben in eine Live-Datei.
- **Komponenten-Mapping**: eine Figma-Komponente mit ihren Varianten auf eine Code-Komponente mit ihren Props abgebildet, durch die Übergabe hindurch erhalten.
- **Ein Importer für Live-Sites**: das System lesen, das eine veröffentlichte Site tatsächlich rendert, neben den Datei-Importern.
- **Doku-Seiten für ein gebautes System**: die menschliche Sicht auf seine Tokens, Rollen und Verträge.

Ebenfalls offen:

- **`uxskill lint --fix` für sichere Umschreibungen** mechanisch behebbarer Befunde (button-no-type, img-no-alt als leerer String, Entfernen von console-log-leak).
- **VS-Code-Erweiterung**, die Lint-Befunde inline anzeigt.
- **Code-Ausgabe pro Komponente** in sechs Stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, Vanilla HTML/CSS).
- **Marktplatz für Brand-Specs**: Community-Brand-Specs veröffentlichen und entdecken.
- **Eigene Anti-Pattern-Regeln**: Entdecken und Teilen der Regeln, die Projekte in `data/anti-patterns.local.json` definieren.
- **`uxskill plan`**: Planung mehrseitiger Sites aus einem Briefing, nicht nur einer Oberfläche.

---

## Beitragen

Issues und PRs willkommen. Drei Bereiche mit hohem Hebel:

### Eine Anti-Pattern-Regel hinzufügen

1. Bearbeiten Sie `data/anti-patterns.json`, fügen Sie einen Eintrag mit `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references` hinzu.
2. Fügen Sie einen Test in `tests/linter/` hinzu, eine Datei, die die Regel auslöst, eine, die es nicht tut.
3. Führen Sie `uxskill lint tests/linter/should-trigger/<rule>.tsx` aus, bestätigen Sie, dass sie feuert. Führen Sie auf `tests/linter/should-not-trigger/<rule>.tsx` aus, bestätigen Sie, dass sie es nicht tut.
4. Öffnen Sie einen PR.

### Eine Brand-Spec hinzufügen

1. Erstellen Sie `data/brands/<slug>.json` mit `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Fügen Sie die entsprechende Prosa unter `references/brands/<slug>.md` hinzu.
3. Registrieren Sie sie in `data/brands/_index.json`.
4. Öffnen Sie einen PR. Die Spec muss durch Primärquellen-Referenzen gestützt sein (das tatsächliche Produkt der Marke, ihr öffentliches Designsystem oder ihre DESIGN.md, falls sie eine publiziert).

### Ein Motion-Preset hinzufügen

1. Bearbeiten Sie `data/motion-presets.json`, fügen Sie einen Eintrag mit `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use` hinzu.
2. Das Preset muss eine reduced-motion-Variante haben. Keine Ausnahmen.
3. Öffnen Sie einen PR.

### Prozess

- Lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md) für den vollständigen Prozess.
- Lesen Sie [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Neue Regeln und Brand-Specs werden geprüft auf: Verankerung in Primärquellen, kein Overfitting auf ein einzelnes Projekt, keine Emojis in den Daten, RTL-sicheres Verhalten wo zutreffend.

---

## Lizenz, Autor, Danksagungen

### Lizenz

MIT. Nutzen Sie es, forken Sie es, bauen Sie darauf auf. Wenn es Sie davor bewahrt, KI-Slop auszuliefern, vergeben Sie einen Stern an das Repo, das ist die günstigste Form der Unterstützung.

### Autor

**Laith Aljunaidy**: Solo-Gründer von [Dot](https://thedotwallet.com), einer MENA-first-Loyalty-Plattform. Baut ux-skill, damit das KI-generierte Frontend nicht mehr gleich aussieht.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- E-Mail: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Website: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Danksagungen

- Dem Team von Anthropic für Claude Code und die Skill- / Plugin-Architektur, die dies vertreibbar macht.
- Nielsen Norman Group, Laws of UX (lawsofux.com) und der UX-Forschungs-Community, deren Arbeit `data/ux-guidelines.json` speist.
- Jeder in `data/brands/` gelisteten Marke, ihre öffentlichen Designsysteme sind die Quelle der Wahrheit für die Brand-Specs.
- Den ursprünglichen v1-Mitwirkenden: eine Einzel-Claude-Skill, die zum Samen für die v2-Python-Engine wurde.
- Den 8 populären Claude-UX-Plugins, mit denen wir uns verglichen haben, sie haben die Latte höher gelegt; dies ist unsere Antwort.

---

**ux-skill** · **v4.0.0b2** · Gebaut, damit Claude Code, Cursor, Windsurf und jedes andere KI-Coding-Werkzeug Frontend ausgeben, das nicht KI-generiert wirkt.

> Setzen Sie einen Stern auf [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Installieren Sie via `pip install uxskill` oder `npx uxskill init` · Durchsuchen Sie den Vergleich unter [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
