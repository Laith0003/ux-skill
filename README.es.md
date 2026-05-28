[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · **Español** · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — el motor de inteligencia de diseño para Claude Code, Cursor y todas las demás herramientas de codificación con IA

> **El plugin de UX más potente para la codificación con IA.** Un núcleo de razonamiento en Python con 11 manifiestos JSON consultables (84 estilos, 176 paletas, 70 emparejamientos tipográficos, 148 componentes, 184 sectores, 35 tipos de gráfico, 57 presets de movimiento, 112 leyes de UX, 100 reglas de antipatrones, 25 stacks tecnológicos, 110 especificaciones de marca), 22 comandos slash, 5 sub-agentes y un linter determinista anti-slop de IA. Multi-IDE: se distribuye en Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer y Roo Cline.

> **El nombre de marca es `ux-skill`.** El nombre de paquete en PyPI / npm sigue siendo `uxskill`. El repositorio de GitHub vive en [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Sitio:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Comparativa frente a todos los plugins de UX para Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-2.0.0--alpha.1-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#el-instalador-para-17-ides)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-100-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Historial de estrellas

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Qué es ux-skill

ux-skill es un **motor de inteligencia de diseño** para herramientas de codificación con IA. Se ejecuta como paquete de Python (`pip install uxskill`), como plugin de Claude Code y como multi-instalador para 17 IDEs. El motor ingiere un brief de proyecto (sector, audiencia, tono, imprescindibles, elementos prohibidos, stack, región) y devuelve un sistema de diseño recomendado completo: estilo, paleta, par tipográfico, presets de movimiento, componentes, marcas ejemplares para estudiar y las barreras de antipatrones que deben respetarse. La recomendación es determinista — la misma entrada produce siempre la misma salida.

El plugin se sitúa entre tú y la herramienta de codificación con IA. Cuando le pides a Claude Code, Cursor o cualquier otro asistente de IA «construir una landing fintech», el asistente típicamente improvisa — y el resultado se identifica como generado por IA en cinco segundos (gradientes de morado a azul, tres tarjetas iguales, Inter en tamaño display, «John Doe» en los testimonios, transiciones por defecto de 300 ms, hero centrado, flechas rebotando en los CTA). ux-skill sustituye la improvisación por **restricciones estructuradas**: ejecutas `/ux-discover` para capturar el brief, `/ux-recommend` para elegir el sistema, `/ux-design` para generar el código y `/ux-lint` para verificar que pasa las 100 reglas deterministas anti-slop de IA antes del commit.

Este README es la referencia canónica. Cada comando, cada sub-agente, cada manifiesto de datos, cada ruta de instalación, cada especificación de marca, cada categoría de antipatrón — está todo documentado aquí. Si estás buscando un plugin de diseño para Claude Code o comparando herramientas de diseño con IA para Cursor, Windsurf o Codex, lee esto de principio a fin junto a [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Índice

1. [Instalación rápida](#instalación-rápida)
2. [Los números — comparativa en vivo frente a las 8 mejores skills de UX para Claude](#los-números--comparativa-en-vivo-frente-a-las-8-mejores-skills-de-ux-para-claude)
3. [Arquitectura — cómo encajan las piezas](#arquitectura--cómo-encajan-las-piezas)
4. [Los 22 comandos slash — referencia detallada](#los-22-comandos-slash--referencia-detallada)
5. [Los 5 sub-agentes](#los-5-sub-agentes)
6. [Los 11 manifiestos de datos](#los-11-manifiestos-de-datos)
7. [Las 100 reglas anti-slop de IA — el linter](#las-100-reglas-anti-slop-de-ia--el-linter)
8. [Las 110 especificaciones DESIGN.md de marca — por categoría](#las-110-especificaciones-designmd-de-marca--por-categoría)
9. [Servidor MCP — el movimiento asimétrico](#servidor-mcp--el-movimiento-asimétrico)
10. [El instalador para 17 IDEs](#el-instalador-para-17-ides)
11. [Casos de uso — escenarios concretos](#casos-de-uso--escenarios-concretos)
12. [Frente a las alternativas](#frente-a-las-alternativas)
13. [Hoja de ruta](#hoja-de-ruta)
14. [Cómo contribuir](#cómo-contribuir)
15. [Licencia, autor, agradecimientos](#licencia-autor-agradecimientos)

---

## Instalación rápida

Tres rutas de instalación. Elige la que se ajuste a tu entorno.

### Ruta 1 — marketplace de Claude Code (canónica)

Si trabajas en Claude Code, instala vía el marketplace de plugins:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Eso conecta los 22 comandos slash y los 5 sub-agentes a tu sesión de Claude Code. Tras la instalación, ejecuta `/ux-init` para configurar el directorio de estado `.ux/` por proyecto y verificar que el motor de Python es accesible.

### Ruta 2 — pip (universal)

Si trabajas fuera de Claude Code (Cursor, Windsurf, CLI, CI), instala el paquete de Python:

```bash
pip install uxskill
uxskill init                       # detecta automáticamente tu IDE e instala el artefacto correcto
uxskill stats                      # imprime los recuentos de manifiestos para verificar la instalación
uxskill lint .                     # ejecuta el linter contra el directorio actual
```

El paquete expone `ux` y `uxskill` como entry points de CLI — son el mismo binario.

### Ruta 3 — npx (sin Python obligatorio)

Si no quieres gestionar Python directamente, el wrapper de npx arranca todo vía `pipx`:

```bash
npx uxskill init                  # descarga pipx + uxskill en la primera ejecución
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verificar la instalación

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

Si algún recuento devuelve 0, falta el archivo JSON — abre una issue en [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Los números — comparativa en vivo frente a las 8 mejores skills de UX para Claude

Los recuentos de estrellas se verificaron por última vez vía `gh api` el **2026-05-28**. ux-skill (Laith0003/ux-skill) es el recién llegado — somos diminutos en notoriedad, profundos en arquitectura. La comparativa de abajo es honesta: dónde perdemos, dónde ganamos.

| Plugin | Estrellas | Arquitectura | Comandos slash | Linter (apto para CI) | Specs de marca | Componentes | Presets de movimiento | IDEs soportados |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83 958** | Python BM25 + CSV, skill única | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54 406** | Node.js + 19 skills + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25 202** | Bash + buen gusto basado en investigación | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15 455** | Único SKILL.md de 62 KB + scripts | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5 762** | Biblioteca de skills cableada con MCP | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2 391** | Skill mono-estética | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2 164** | Skill de diseño anti-slop | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Componentes MD3 + auditoría | 1 | — | — | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Motor de Python + 11 manifiestos + 22 comandos + 5 sub-agentes + linter de CI** | **22** | **100 reglas regex** | **110** | **148** | **57** | **17** |

### Dónde perdemos

- **Notoriedad.** Ellos tienen cientos de miles de estrellas. Nosotros tenemos 14. Danos una estrella — es la forma más barata de ayudar.
- **Reconocimiento de marca.** ui-ux-pro-max y open-design llevan una ventaja medida en meses, no en días.
- **Pulido de marketing.** Tienen capturas, vídeos de demo y una landing descubrible. Nosotros tenemos un README exhaustivo y una landing modesta.

### Dónde ganamos

- **Biblioteca de componentes:** 148 componentes documentados con anatomía, estados, tokens usados y especificaciones de movimiento. Ninguno de los otros 8 distribuye un manifiesto de componentes.
- **Presets de movimiento:** 57 entradas listas por stack (Framer Motion, GSAP, CSS) con fallbacks de movimiento reducido. Ninguno de los demás distribuye un manifiesto de movimiento.
- **Linter de antipatrones:** 100 reglas regex deterministas, se ejecuta en CI, sale con código no-cero en Critical/High. Ninguno de los demás distribuye un linter determinista.
- **Specs de marca:** 110 especificaciones DESIGN.md reales (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude y 96 más). Ninguno de los demás distribuye una biblioteca de marcas.
- **17 IDEs soportados:** el mismo motor, diferente pegamento por IDE.
- **22 comandos slash:** discovery, generación, auditoría, lint, pulido, bucle de fix, caso de estudio, taller, copy, motion, a11y, dashboard, conductor — totalmente integrados.

Tabla completa lado a lado en [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Arquitectura — cómo encajan las piezas

```
ux-skill (nombre del paquete: uxskill)
│
├── data/                              El cerebro — manifiestos JSON consultables
│   ├── styles.json                    84 estilos de diseño + when/skip + tokens
│   ├── palettes.json                  176 paletas (claro/oscuro, contraste verificado)
│   ├── type-pairs.json                70 tripletas display × body × mono
│   ├── components.json                148 componentes (anatomía, estados, movimiento)
│   ├── industries.json                184 reglas sectoriales + señales de audiencia
│   ├── chart-types.json               35 tipos de gráfico (when/skip, encoding)
│   ├── tech-stacks.json               25 stacks (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 leyes de UX con nombre (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 presets de movimiento (entrada, salida, hover...)
│   ├── anti-patterns.json             100 reglas regex (fuente del linter apto para CI)
│   └── brands/*.json                  110 specs DESIGN de marca + _index.json
│
├── engine/                            Python — el razonamiento
│   ├── recommender/                   motor de fusión con 5 búsquedas paralelas
│   ├── linter/                        escáner anti-slop determinista
│   ├── discovery/                     protocolo forzoso de 10 campos
│   ├── generator/                     emisor de tokens + manifiestos
│   ├── installer/                     multi-instalador para 17 IDEs
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          22 comandos slash de Claude Code (.md)
│   ├── ux-init.md                     arranque
│   ├── ux-stats.md                    snapshot de inventario
│   ├── ux-discover.md                 intake de 10 campos (puerta)
│   ├── ux-recommend.md                EMBLEMÁTICO — 5 búsquedas paralelas
│   ├── ux-lint.md                     linter determinista
│   ├── ux-design.md                   genera código frontend
│   ├── ux-component.md                genera un componente
│   ├── ux-system.md                   genera el sistema de diseño completo
│   ├── ux-dashboard.md                genera la superficie de dashboard
│   ├── ux-motion.md                   tratamiento de movimiento + auditoría
│   ├── ux-audit.md                    auditoría de diseño con 6 lentes
│   ├── ux-a11y.md                     auditoría WCAG 2.1 AA
│   ├── ux-critique.md                 crítica de gusto (3 aciertos, 3 fallos, 1 movimiento)
│   ├── ux-copy.md                     revisión + reescritura de microcopy
│   ├── ux-fix.md                      aplica hallazgos como commits atómicos
│   ├── ux-polish.md                   pasada cosmética + matar slop de IA
│   ├── ux-frame.md                    bloque de framing de 4 campos
│   ├── ux-research.md                 planificación + síntesis de investigación
│   ├── ux-workshop.md                 taller de design thinking en 5 fases
│   ├── ux-case-study.md               caso de estudio publicable estilo editorial Wfrah
│   ├── ux-next.md                     conductor de flujo de trabajo (solo lectura)
│   └── ux-expert.md                   gancho de consultoría
│
├── agents/                            5 sub-agentes (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy con la voz de la marca
│   ├── research-synthesizer.md        entrevistas + analítica + competidores
│   └── design-system-architect.md     tokens / componentes / fundamentos
│
├── references/                        Fuente en prosa de los datos + páginas demo
│   ├── foundations/                   anti-patterns.md, principios, gusto
│   ├── laws/                          leyes de UX en formato largo
│   ├── process/                       discovery-protocol.md (crítico)
│   ├── styles/                        prosa por estilo (anti-slop.md, etc.)
│   ├── components/                    componentes en formato largo
│   ├── output/                        rúbricas de salida
│   └── conditional/                   guía específica por stack
│
├── bin/
│   ├── uxskill.mjs                    wrapper npx -> motor Python
│   ├── ux-lint.py                     linter v2 (preferido)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (creado por proyecto)
    ├── last-discovery.json            snapshot del brief
    ├── last-recommendation.json       sistema elegido
    ├── last-frame.json                bloque de framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Cómo funciona realmente el motor

1. **Entrada.** Proporcionas un brief — de forma interactiva vía `/ux-discover` (10 campos) o no interactiva mediante flags a `ux recommend`.
2. **5 búsquedas paralelas.** El motor ejecuta cinco consultas concurrentes a través de los manifiestos:
   - **Sector → estilos_recomendados** (industries.json)
   - **Estilo → compatibilidad paleta + tipografía + movimiento** (styles.json)
   - **Tono × imprescindible → filtro de paletas** (palettes.json)
   - **Stack → compatibilidad de componentes + presets de movimiento** (tech-stacks.json, motion-presets.json)
   - **Prohibido + región → barreras + shortlist de marcas ejemplares** (anti-patterns.json, brands/)
3. **Fusión.** Un fusionador determinista ordena los candidatos, resuelve conflictos (p. ej., un imprescindible de modo oscuro fuerza el modo de paleta) y emite un único sistema recomendado.
4. **Salida.** Un documento JSON con el estilo elegido, la paleta elegida, el par tipográfico, los 5 mejores presets de movimiento, los 12 mejores componentes, las 5 mejores marcas ejemplares y las 100 barreras de antipatrones activas. Además, un bloque de justificación que explica cada elección.
5. **Generación.** Los comandos posteriores (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) consumen la recomendación para generar código real vía los sub-agentes.
6. **Verificación.** `/ux-lint` vuelve a escanear el código generado contra las 100 reglas regex. Sale con código no-cero en Critical/High en CI.

**Python piensa. HTML muestra. Markdown encadena.**

---

## Los 22 comandos slash — referencia detallada

Cada comando se distribuye como archivo `.md` dentro de `commands/` con `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` y `output state file`. Las descripciones de abajo son condensadas; el código fuente completo es la especificación canónica.

Los comandos se agrupan en cinco categorías: **arranque e inventario**, **discovery y recomendación**, **generación**, **auditoría y verificación**, **fix y pulido**, y **conductor**.

### Arranque e inventario

#### `/ux-init` — arrancar el proyecto

- **Qué:** Detecta el IDE que usas (`.claude/`, `.cursor/`, `.windsurf/`, etc.), instala el artefacto correcto, verifica que el motor de Python es accesible, imprime un snapshot de estadísticas.
- **Cuándo usar:** Primera instalación en un proyecto nuevo. Tras clonar un proyecto que usa ux-skill. Después de `pip install --upgrade uxskill`.
- **Cuándo saltar:** Ya lo ejecutaste en este proyecto y nada ha cambiado.
- **Invocación:** `/ux-init` (sin argumentos) o `uxskill init` desde la CLI.
- **Salida:** Artefacto por IDE (ver [El instalador para 17 IDEs](#el-instalador-para-17-ides)) + directorio `.ux/` + resumen por stdout.
- **Encadena con:** `/ux-discover` a continuación.

#### `/ux-stats` — imprimir el inventario de datos

- **Qué:** Imprime la versión + recuentos de entradas para los 11 manifiestos de datos, para que puedas verificar qué hay instalado.
- **Cuándo usar:** Tras instalar. Tras actualizar. Cuando `/ux-recommend` devuelve elecciones sorprendentes y sospechas que los manifiestos están incompletos.
- **Cuándo saltar:** Nunca — es un comando de solo lectura de 50 ms.
- **Invocación:** `/ux-stats` o `uxskill stats`.
- **Salida:** JSON a stdout (ver [Verificar la instalación](#verificar-la-instalación) arriba).
- **Encadena con:** Solo diagnóstico; no alimenta nada aguas abajo.

### Discovery y recomendación

#### `/ux-discover` — la función forzosa (intake de 10 campos)

- **Qué:** El intake obligatorio de 10 campos por el que pasa cada proyecto antes de cualquier comando de generación. Tipo de proyecto, audiencia, objetivo principal, tono, imprescindibles, prohibidos, marcas de referencia, stack, región, métrica de éxito. **Nada de improvisación.** Frases prohibidas («moderno», «limpio») obligan al usuario a ser específico.
- **Cuándo usar:** Antes de cualquier `/ux-design`, `/ux-component`, `/ux-system` o `/ux-dashboard`. Siempre que un brief anterior se haya quedado obsoleto.
- **Cuándo saltar:** Estás arreglando un bug (`/ux-fix`). Solo vas a pasar el linter (`/ux-lint`). El brief no ha cambiado desde la última sesión.
- **Invocación:** `/ux-discover`. El plugin pregunta; tú respondes.
- **Salida:** Escribe `.ux/last-discovery.json` (el brief de 10 campos).
- **Encadena con:** `/ux-recommend` → usa el discovery para elegir estilo + paleta + tipografía + movimiento + componentes. `/ux-design [brief adicional]` → genera código frontend anclado a la recomendación. `/ux-component <nombre>` → genera un componente alineado con las restricciones descubiertas.

#### `/ux-recommend` — el motor emblemático de 5 búsquedas paralelas

- **Qué:** Ejecuta las 5 búsquedas paralelas del motor de Python a través de los 11 manifiestos y devuelve un sistema de diseño fusionado. Sector → Estilo → Paleta → Tipografía → Movimiento + Componentes + Marcas ejemplares + Barreras.
- **Cuándo usar:** Empezar un proyecto desde cero. Pivotar un producto cansado. Pre-vuelo antes de cualquier `/ux-design` o `/ux-component`.
- **Cuándo saltar:** Ya ejecutaste `/ux-discover` y guardaste un brief — `/ux-recommend` es automático en ese flujo. Estás arreglando un bug (usa `/ux-fix`). Solo necesitas el linter (usa `/ux-lint`).
- **Invocación (Claude Code):**
  ```
  /ux-recommend
  ```
  **Invocación (CLI):**
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
- **Salida:** Escribe `.ux/last-recommendation.json` — estilo elegido, paleta elegida, par tipográfico, 5 mejores presets de movimiento, 12 mejores componentes, 5 mejores marcas ejemplares, las 100 barreras de antipatrones activas, además de la justificación.
- **Encadena con:** `/ux-design [brief]` → código frontend usando los tokens recomendados. `/ux-system` → sistema de diseño completo a partir de la recomendación. `/ux-component <nombre>` → un componente usando el estilo recomendado. `/ux-lint` → verifica el código generado.

### Generación

#### `/ux-design` — genera una superficie bonita y anti-slop desde un brief

- **Qué:** Genera un artefacto frontend completo y de calidad de producción (landing, sitio de marketing, app shell) a partir del brief de discovery + recomendación. Despacha `frontend-engineer` con dirección creativa basada en las referencias anti-slop y de arsenal.
- **Cuándo usar:** «Diseña», «constrúyeme», «genera una landing», «crea un dashboard», «haz un componente» — cualquier petición de entregable visual de formato libre.
- **Cuándo saltar:** Quieres una revisión, no un build (usa `/ux-audit` o `/ux-critique`). Quieres solo un componente (usa `/ux-component`). Trabajo de backend o infraestructura.
- **Invocación:** `/ux-design genera una landing fintech para un neobanco MENA, tono cálido editorial, modo oscuro AA, sin gradientes morados`.
- **Salida:** Código generado (HTML / Blade / JSX / Vue / Astro), más `.ux/last-design.json`.
- **Encadena con:** `/ux-lint` → verifica contra las barreras. `/ux-polish` → pasada cosmética. `/ux-a11y` → auditoría de accesibilidad. `/ux-copy` → revisión de microcopy. `/ux-fix` → aplica hallazgos como commits atómicos.

#### `/ux-component` — genera un componente

- **Qué:** Produce un único componente de calidad de producción (botón, modal, navbar, sidebar, tarjeta, tabla, formulario, gráfico) a partir de una especificación. Los cuatro estados de interacción, accesible, fiel a la marca. Primero busca el componente en `.ux/last-recommendation.json`, vuelve a la consulta directa al manifiesto como fallback.
- **Cuándo usar:** Cualquier petición de un único elemento — «construye un botón», «crea una tarjeta de precios», «haz un modal», «añade un navbar», «diseña un sidebar», «necesito una tabla de datos», «construye un formulario», «haz un componente de gráfico».
- **Cuándo saltar:** Página completa o superficie multi-sección (usa `/ux-design`). Backend o infraestructura.
- **Invocación:** `/ux-component pricing-card-trio --brief="fintech, oscuro, números monospace"`.
- **Salida:** Código del componente generado, más `.ux/last-component.json`.
- **Encadena con:** `/ux-lint` → verifica. `/ux-polish` → afinar.

#### `/ux-system` — genera un sistema de diseño inicial completo

- **Qué:** Propone un sistema de diseño inicial completo para un proyecto que no tiene uno — tokens (color, tipografía, espacio, movimiento, radio, sombra), documentos de fundamentos, contratos de componentes, emparejamientos para modo oscuro, conmutador de tema. Despacha `design-system-architect`.
- **Cuándo usar:** «No tenemos sistema de diseño», «constrúyenos un sistema», «propón tokens», «cuál debería ser nuestro tema», «monta nuestro DS».
- **Cuándo saltar:** El proyecto ya tiene sistema de diseño — usa `/ux-component` contra el sistema existente. Backend o infraestructura.
- **Invocación:** `/ux-system` (ejecuta discovery primero si no está ya archivado).
- **Salida:** `tokens.json`, `foundations.md`, contratos `components/*.md`, emisión opcional Tailwind / vanilla / SCSS. Escribe `.ux/last-system.json` para contexto de cadena.
- **Encadena con:** `/ux-component` → construir contra el nuevo sistema. `/ux-design` → generar una superficie usando los nuevos tokens.

#### `/ux-dashboard` — generación especializada de dashboards

- **Qué:** Dashboard con disciplina de densidad de datos — layout bento, números monospace tabulares, patrones de sparkline, anti-abuso de tarjetas, colores semánticos de estado, movimiento parco. No es una landing de marketing con gráficos pegados.
- **Cuándo usar:** «Construye un dashboard», «diseña el panel de admin», «haz una página de métricas», «consola de operaciones», «vista de analítica», «tablero de KPI», «pantalla de monitorización».
- **Cuándo saltar:** Landing de marketing con estadísticas (usa `/ux-design`). Un único widget (usa `/ux-component`). Backend o infraestructura.
- **Invocación:** `/ux-dashboard`.
- **Salida:** Código de dashboard generado + `.ux/last-dashboard.json`.
- **Encadena con:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — tratamiento de movimiento

- **Qué:** Genera la capa de movimiento de una superficie — duraciones, easings, coreografía, fallbacks de movimiento reducido, disciplina de rendimiento. También audita el movimiento existente contra las 5 dimensiones (timing, easing, significado, movimiento reducido, rendimiento).
- **Cuándo usar:** «Comprueba el movimiento», «¿están bien las animaciones?», «arregla el movimiento», «revisa las animaciones», «auditoría de movimiento», «pasada de rendimiento sobre el movimiento».
- **Cuándo saltar:** La superficie no tiene movimiento (usa `/ux-audit` o `/ux-polish`). Backend o infraestructura.
- **Invocación:** `/ux-motion path/to/component.tsx` (modo auditoría) o `/ux-motion --generate hero-entry` (generación).
- **Salida:** Código actualizado (en modo generación) o informe `.ux/last-motion.json` (en modo auditoría).
- **Encadena con:** `/ux-fix` → aplica hallazgos de movimiento. `/ux-polish` → afinar.

### Auditoría y verificación

#### `/ux-lint` — linter determinista basado en regex (sin LLM, apto para CI)

- **Qué:** Ejecuta 100 reglas regex contra tu código. Sin llamada a LLM. Sale con código no-cero en Critical / High en CI. Fuente: `data/anti-patterns.json`. Las reglas cubren A11y (23), Contenido (15), Layout (13), Tipografía (10), Color (9), Calidad (9), Visual (9), Movimiento (8), Performance (4).
- **Cuándo usar:** Hook pre-commit. Puerta de CI. Primer paso rápido en un código grande antes de pagar el coste de `/ux-audit`. Tras `/ux-design` o `/ux-component` para verificar la generación.
- **Cuándo saltar:** Quieres un bucle de fix (el linter reporta, no edita — encadena con `/ux-polish --fix` o `/ux-fix`). Quieres juicio de gusto (usa `/ux-critique`).
- **Invocación (slash):** `/ux-lint src/`.
- **Invocación (CLI):** `uxskill lint .` o `python3 bin/ux-lint.py .` o `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocación (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Salida:** Hallazgos a stdout (ubicación, id de regla, severidad, evidencia). Código de salida 0 si está limpio, no-cero en Critical/High cuando `--fail-on high` está activo.
- **Encadena con:** `/ux-polish --fix` → contraparte impulsada por LLM sobre los mismos patrones. `/ux-fix` → aplica hallazgos como commits, ordenados por severidad. `/ux-audit` → pasada completa de razonamiento con 6 lentes. `/ux-next` → deja que el conductor decida.

#### `/ux-audit` — auditoría de diseño con 6 lentes

- **Qué:** Una revisión estructurada y opinada contra seis lentes (claridad, jerarquía, accesibilidad, voz, movimiento, gusto), produciendo hallazgos etiquetados por severidad. Informe estilo Polaris. Lee `.ux/last-frame.json` primero — la audiencia y el outcome anclan la severidad de cada hallazgo.
- **Cuándo usar:** La superficie existe y quieres una crítica defendible. «Audita», «revisa la ux», «¿es esto bueno?», «¿qué está roto?», «destroza esto».
- **Cuándo saltar:** La superficie aún no existe (usa `/ux-design`). El usuario quiere una sola lente (usa el comando dirigido: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). El usuario quiere opinión de gusto (usa `/ux-critique`). Backend o infraestructura.
- **Invocación:** `/ux-audit https://example.com/pricing` o `/ux-audit src/components/Pricing.tsx`.
- **Salida:** Escribe `.ux/last-audit.json` — array `findings` con `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Encadena con:** `/ux-fix` → aplica hallazgos. `/ux-polish` → pasada cosmética. `/ux-design` → si se necesita rediseño estructural.

#### `/ux-a11y` — auditoría WCAG 2.1 AA + comprobaciones de cortesía común

- **Qué:** Auditoría WCAG 2.1 AA estructurada, más las comprobaciones de cortesía común que pasan los tools automáticos pero que aún hieren a los usuarios reales (visibilidad de foco, especificidad de errores, preferencias de movimiento, trampas de teclado, dependencia del color).
- **Cuándo usar:** Puerta de accesibilidad pre-envío. Tras un rediseño. «Comprobación de accesibilidad», «auditoría WCAG», «¿es esto accesible?», «revisión a11y», «test con lector de pantalla», «comprobación de navegación con teclado».
- **Cuándo saltar:** No es de cara al usuario. Backend o infraestructura. Bocetos en construcción.
- **Invocación:** `/ux-a11y https://example.com` (URL en vivo preferido — los tools automáticos y las pruebas de teclado solo funcionan en vivo).
- **Salida:** Escribe `.ux/last-a11y.json` — array `findings` con `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Encadena con:** `/ux-fix` → aplica hallazgos como commits. `/ux-copy` → arregla alt text y cableado de errores de formulario como parte de una pasada de copy.

#### `/ux-critique` — opinión de gusto (3 aciertos, 3 fallos, 1 movimiento estratégico)

- **Qué:** La opinión de un diseñador — no una auditoría estructurada, no una puntuación de severidad, solo una toma ceñida y opinada que nombra lo que funciona, lo que no, y el único movimiento estratégico que cambiaría más.
- **Cuándo usar:** «¿Qué piensas?», «¿es esto bueno?», «critica esto», «opinión honesta», «¿es correcto el vibe?», «¿se siente como nosotros?», «¿deberíamos enviar esto?».
- **Cuándo saltar:** El usuario quiere explícitamente una auditoría estructurada (usa `/ux-audit`). Backend o infraestructura.
- **Invocación:** `/ux-critique https://example.com`.
- **Salida:** Escribe `.ux/last-critique.json` — 3 aciertos, 3 fallos, 1 movimiento estratégico, además de prosa.
- **Encadena con:** `/ux-design` si la opinión recomienda rediseño. `/ux-polish` si recomienda afinar.

#### `/ux-copy` — revisión + reescritura de microcopy

- **Qué:** Evalúa cada cadena visible contra la rúbrica de voz y produce una reescritura antes/después. Detecta: «el formulario contiene errores» (genérico), «John Doe» (placeholder), copy celebratorio cantarín de IA, CTAs genéricos, empty states muertos, errores inútiles.
- **Cuándo usar:** La estructura está bien pero las palabras flojean. «Revisa el copy», «arregla el microcopy», «los mensajes de error son malos», «reescribe esto», «afina las cadenas», «los botones suenan genéricos», «este empty state está muerto».
- **Cuándo saltar:** Problemas de layout (usa `/ux-audit` o `/ux-polish`). Problemas de copy ligados a accesibilidad como el alt text (usa `/ux-a11y`). Backend o infraestructura.
- **Invocación:** `/ux-copy src/views/checkout.blade.php`.
- **Salida:** Escribe `.ux/last-copy.json` — array `strings` con `{location, severity, before, after, notes}`, además de rúbrica + locales que necesitan traducción.
- **Encadena con:** `/ux-fix` → aplica reescrituras. `/ux-a11y` → vuelve a comprobar tras los arreglos de copy.

### Fix y pulido

#### `/ux-fix` — aplicar hallazgos como commits atómicos

- **Qué:** Lee el último informe de `.ux/` (audit, copy, a11y, motion o polish), valida el árbol de trabajo y aplica los hallazgos como commits atómicos vía los sub-agentes correctos. Vuelve a verificar reejecutando el comando originador.
- **Cuándo usar:** Tras ejecutar un comando de clase auditoría y revisar los hallazgos. «Arregla los hallazgos», «aplica los arreglos», «ejecuta el bucle de fix», «parchea la superficie», «haz los cambios», «vete a arreglarlo».
- **Cuándo saltar:** No hay informe previo en `.ux/`. El árbol de trabajo está sucio y el usuario no ha aceptado stash/commit. Los arreglos requieren juicio de diseño, no aplicación mecánica (usa `/ux-design` para rediseñar).
- **Invocación:** `/ux-fix` (auto-detecta qué informe arreglar) o `/ux-fix --from=last-a11y.json`.
- **Salida:** Commits atómicos por hallazgo. Reejecuta el comando originador y actualiza el archivo `.ux/last-*.json`. Imprime un resumen.
- **Encadena con:** `/ux-next` → el conductor elige el siguiente movimiento.

#### `/ux-polish` — pasada cosmética + matar slop de IA

- **Qué:** Ritmo de espaciado, agudización de jerarquía, detección de slop de IA, consistencia de tokens. La contraparte impulsada por LLM a `/ux-lint` — usa tu juicio en las decisiones de gusto.
- **Cuándo usar:** La estructura está bien pero la ejecución está floja. «Pule», «aprieta esto», «quita el slop de IA», «hazlo premium», «haz que esto no parezca de IA», «el espaciado se siente raro», «esto parece genérico», «necesita más gusto».
- **Cuándo saltar:** A la superficie le falta funcionalidad central (arregla eso primero). Necesita un rediseño, no un pulido (usa `/ux-design`). Problemas de copy (usa `/ux-copy`). Problemas de movimiento (usa `/ux-motion`). Problemas de a11y (usa `/ux-a11y`).
- **Invocación:** `/ux-polish src/components/Hero.tsx`.
- **Salida:** Código actualizado + `.ux/last-polish.json` describiendo los cambios.
- **Encadena con:** `/ux-lint` → verifica que el pulido se sostuvo. `/ux-a11y` → vuelve a comprobar accesibilidad.

### Discovery y narrativa

#### `/ux-frame` — bloque de framing de 4 campos

- **Qué:** Captura para-quién, outcome, hipótesis y señal de éxito en un bloque de framing estructurado. No hay trabajo de diseño — solo el intake de cuatro campos que convierte una petición vaga en un brief de trabajo. Más ligero que `/ux-discover` (4 campos vs 10).
- **Cuándo usar:** Inicio de cualquier proyecto, sprint o encargo puntual. A mitad de flujo cuando una conversación ha derivado. «Enmarca esto», «¿cuál es el brief?», «monta el proyecto», «framing».
- **Cuándo saltar:** Ya enmarcado (comprueba `.ux/last-frame.json`). Construcción de un componente puntual sin implicaciones de framing. Backend o infraestructura.
- **Invocación:** `/ux-frame "billetera de fidelización para el piloto MENA de Bashiti"`.
- **Salida:** Escribe `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Encadena con:** `/ux-discover` → extiende el frame al brief de 10 campos. `/ux-design` → genera usando el frame como ancla.

#### `/ux-research` — planificación + síntesis de investigación

- **Qué:** Modo planificación: escribe guiones de entrevista, encuestas, filtros de reclutamiento. Modo síntesis (`--synthesize`): digiere entrevistas, analítica, sitios competidores, resultados de A/B, tickets de soporte en recomendaciones. Despacha `research-synthesizer`.
- **Cuándo usar:** «Planifica un estudio de investigación», «necesito preguntas de entrevista», «diseña una encuesta», «cómo recluto usuarios», «plan de user testing», «estudio de diario», «test de preferencia», «fake door», «smoke test», «sintetiza mis notas de entrevista».
- **Cuándo saltar:** La respuesta ya se conoce con alta confianza. Decisiones reversibles de bajo riesgo. Backend o infraestructura.
- **Invocación:** `/ux-research --plan "adopción de billetera de fidelización en MENA"` o `/ux-research --synthesize interviews/*.md`.
- **Salida:** Escribe `.ux/last-research.json` — plan de investigación o temas sintetizados + evidencia + recomendaciones.
- **Encadena con:** `/ux-frame` → integra los hallazgos en un frame. `/ux-design` → genera desde los hallazgos. `/ux-workshop` → corre un taller usando la investigación como entrada.

#### `/ux-workshop` — taller de design thinking en 5 fases

- **Qué:** Facilita un taller de discovery / design thinking de extremo a extremo. Cinco fases secuenciales (exploración → mapa de calor → mapa de actores → boceto de solución → plan de juego). Cronometrado. Artefactos concretos por fase. Termina con una decisión, no con «hallazgos interesantes».
- **Cuándo usar:** Pregunta real, participantes reales, presupuesto real de tiempo. «Corre un taller», «facilita un discovery», «hagamos una sesión de design thinking», «tengo stakeholders por una hora, ¿qué hacemos?», «arranca el proyecto».
- **Cuándo saltar:** El brief ya está claro y acotado. Brainstorm en solitario (usa `/ux-design` o `/ux-frame`). El equipo está en plena ejecución, no en discovery.
- **Invocación:** `/ux-workshop "pivote de billetera de fidelización" --participants="2 PMs, 1 diseñador, 1 lead de eng, 1 representante del cliente" --minutes=90`.
- **Salida:** Escribe `.ux/last-workshop.json` — plan de juego + artefactos por fase.
- **Encadena con:** `/ux-design` → ejecuta el plan de juego. `/ux-research` → rellena las brechas que el taller sacó a la superficie. `/ux-case-study` → publica el recorrido.

#### `/ux-case-study` — caso de estudio publicable (formato editorial Wfrah)

- **Qué:** Genera un caso de estudio de proyecto en formato editorial monocromo puro — tipografía Wfrah, separadores de pelo, códigos de sección numerados (A)–(G), layout bilingüe seguro. Un documento, no un folleto de marketing. Lee de `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Cuándo usar:** Post-lanzamiento. Tras un hito discreto. «Escribe un caso de estudio», «caso de estudio de este proyecto», «haz el documento de cierre», «publica este trabajo», «pieza de portafolio».
- **Cuándo saltar:** Al proyecto le faltan datos para poblar las secciones (A)–(G). El usuario quiere una landing de marketing, no un caso de estudio (usa `/ux-design`).
- **Invocación:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Salida:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Encadena con:** Comando terminal — normalmente el final de un proyecto.

### Conductor

#### `/ux-next` — conductor de flujo de trabajo (solo lectura)

- **Qué:** Lee cada `.ux/last-*.json` y nombra el siguiente comando de mayor apalancamiento. Un conductor, no un constructor. Solo lectura.
- **Cuándo usar:** Entre comandos. «¿Qué debería hacer ahora?», «¿cuál es el siguiente movimiento?», «decide por mí», «¿hacia dónde vamos desde aquí?».
- **Cuándo saltar:** No hay informes previos en `.ux/`. Tienes un siguiente comando específico en mente.
- **Invocación:** `/ux-next` (sin argumentos) o `/ux-next --focus=a11y`.
- **Salida:** Stdout — comando recomendado siguiente + justificación.
- **Encadena con:** Cualquier comando que elija.

#### `/ux-expert` — gancho de consultoría

- **Qué:** Aflora la información de contacto del creador del plugin cuando un usuario pide un experto de UX real. Breve, directo, sin marketing.
- **Cuándo usar:** «¿Quién construyó esto?», «necesito un experto en UX», «¿haces consultoría?», «¿puedo contratar a alguien para esto?», «¿hay un humano detrás de este plugin?».
- **Cuándo saltar:** El usuario pregunta por features del plugin, no por consultoría.
- **Invocación:** `/ux-expert`.
- **Salida:** Tarjeta breve de contacto con LinkedIn / email / repo.

### Grafo de encadenamiento de comandos

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  bloque de framing de 4 campos
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  intake de 10 campos (PUERTA FORZOSA)
                  └────────────┬─────────┘
                               │ escribe .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 búsquedas paralelas -> sistema fusionado
                  └────────────┬─────────┘
                               │ escribe .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ escribe .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ escribe .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  aplica hallazgos como commits
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artefacto publicable
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — solo lectura
                  │  /ux-expert          │  gancho de consultoría
                  └──────────────────────┘
```

---

## Los 5 sub-agentes

Los sub-agentes son generadores específicos por rol despachados por comandos. Nunca se ejecutan de forma independiente — los llaman `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Cada agente tiene un límite de propiedad definido: NO deciden el brief; lo ejecutan.

### `frontend-engineer`

- **Posee:** Código frontend de calidad de producción (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) con disciplina anti-slop de IA.
- **Despachado por:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Entradas:** Brief + dirección creativa + tokens (de `.ux/last-recommendation.json`).
- **Salidas:** Código funcional distinguible del output genérico de IA. Sin gradientes morados, sin hero centrado, sin tres tarjetas iguales, sin Inter en tamaño display, sin «John Doe», sin emoji, sin defaults de 300 ms.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Posee:** El movimiento en código frontend de producción — Framer Motion, GSAP, animaciones CSS. Duraciones, easings, coreografía, fallbacks de movimiento reducido, disciplina de rendimiento.
- **Despachado por:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Entradas:** Brief de movimiento + tokens + los 57 presets de movimiento de `data/motion-presets.json`.
- **Salidas:** Movimiento que se gana su lugar. Siempre envuelto en fallbacks `prefers-reduced-motion`. Siempre probado contra Core Web Vitals.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Posee:** Las cadenas que se envían — mensajes de error, empty states, CTAs, loading states, mensajes de éxito, toasts, texto auxiliar, etiquetas de formulario, texto de botones.
- **Despachado por:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Entradas:** Perfil de voz (nombrado o pegado) + las cadenas de la superficie.
- **Salidas:** Microcopy de producción aplicado consistentemente a cada estado de una superficie para que el producto suene como un producto, no como diez. Prohibido: «el formulario contiene errores», «John Doe», copy celebratorio cantarín de IA, CTAs genéricos, empty states muertos.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Posee:** Digerir entradas de investigación (entrevistas, analítica, sitios competidores, resultados de A/B, tickets de soporte) en recomendaciones de diseño accionables.
- **Despachado por:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Entradas:** Investigación cruda — transcripciones, exports, URLs de competidores, clusters de soporte.
- **Salidas:** Temas, evidencia, recomendaciones. Nunca diseña la respuesta — le da al diseñador el sustrato desde el que diseñar.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Posee:** Sistemas de diseño completos — tokens (color, tipografía, espacio, movimiento, radio, sombra), documentos de fundamentos, contratos de componentes, emparejamientos de modo oscuro, capa de theming.
- **Despachado por:** `/ux-system`, `/ux-component` cuando no existe sistema.
- **Entradas:** Brief de marca + `.ux/last-recommendation.json` (estilo + paleta + par tipográfico + presets de movimiento).
- **Salidas:** Un sistema coherente, opinado, listo para producción contra el que los agentes posteriores puedan construir sin volver a decidir los fundamentos. Tokens JSON, fundamentos MD, contratos de componentes, mapeo de modo oscuro.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocolo de despacho de sub-agentes

Cuando un comando despacha un sub-agente, le pasa:

1. El brief / recomendación (cargado desde `.ux/`).
2. La porción de manifiesto relevante (p. ej., `frontend-engineer` recibe el estilo + paleta + componentes elegidos; `motion-engineer` recibe los presets de movimiento elegidos).
3. Las 100 barreras de antipatrones (siempre activas).
4. Un criterio de éxito (qué debe hacer el artefacto).

Los sub-agentes devuelven:

1. El artefacto (código, doc, sistema).
2. Un bloque de justificación (por qué estas elecciones).
3. Una auto-comprobación contra las barreras (qué reglas verificaron).

El comando que llama ejecuta entonces `/ux-lint` automáticamente antes de declarar terminado.

---

## Los 11 manifiestos de datos

La capa de datos es el cerebro. Cada comando lee de ella; el motor fusiona a través de ella; el linter escanea contra ella. Todos los archivos viven bajo `data/` y envuelven sus entradas en `{_meta, entries}` para versionado de esquema.

### `styles.json` — 84 estilos de diseño

| Campo | Descripción |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalista / Suizo, Brutalista, Editorial, Glassmorfismo, Neumorfismo, Bento, Skeumórfico, Industrial, Maximalista, IA-Futurista, MENA-moderno, Vaporwave, etc. |
| `sample entry` | `swiss-international` — «La cuadrícula es ley. La tipografía hace el trabajo pesado. La decoración es fracaso.» |

Usado por: `/ux-recommend`, `/ux-system`, `/ux-design`. Esquema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 paletas de color

| Campo | Descripción |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (claro/oscuro), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | cálido, editorial, magazine, clínico, juguetón, brutalista, monocromo, joya, MENA-cálido, dev-tools-oscuro, etc. |
| `sample entry` | `claude-warm-editorial` — claro, cálido/editorial/magazine, canvas #faf9f5, primary #cc785c |

Usado por: `/ux-recommend`, `/ux-system`. Contraste verificado en AA / AAA. Esquema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 emparejamientos tipográficos

| Campo | Descripción |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Todas las familias tienen licencia + URL fuente. Usado por `/ux-recommend`, `/ux-system`.

### `components.json` — 148 componentes

| Campo | Descripción |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navegación, Formularios, Visualización de datos, Feedback, Overlays, Layout, Contenido, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Mega Navegación, Cuadrícula de Producto — anatomía de 6 partes, 4 estados |

Este es nuestro mayor moat. Ningún otro plugin de UX para Claude distribuye un manifiesto estructurado de componentes.

### `industries.json` — 184 reglas sectoriales

| Campo | Descripción |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Servicios Financieros, Salud, Educación, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Viajes, Inmobiliaria, Específico MENA, etc. |
| `sample entry` | `fintech-neobank` — alta confianza, disclosures regulatorios, UI primario de balance/transacción, mobile-first de uso diario |

Usado por `/ux-recommend` como primer eje de búsqueda paralela.

### `chart-types.json` — 35 tipos de gráfico

| Campo | Descripción |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparación, Series Temporales, Distribución, Composición, Relación, Flujo, Geográfico |
| `sample entry` | `bar-vertical` — Comparar 4–15 categorías discretas. Posición sobre eje x mapea categoría; altura mapea valor. |

Usado por `/ux-dashboard`, `/ux-component` (instancias de chart).

### `tech-stacks.json` — 25 stacks

| Campo | Descripción |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | producción, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, compatible con Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Otros stacks incluyen Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 leyes de UX con nombre

| Campo | Descripción |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Coste de Decisión, Atención, Memoria, Control Motor, Percepción Visual, Social, Emocional, Formularios, Manejo de Errores, Onboarding, Empty State, etc. |
| `sample entry` | `hicks-law` — El tiempo de decisión crece logarítmicamente con el número de opciones presentadas |

Usado por `/ux-audit` (puntuación de 6 lentes) y `/ux-critique` (ancla de gusto).

### `motion-presets.json` — 57 presets de movimiento

| Campo | Descripción |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback de movimiento reducido), `when_to_use` |
| `categories` | Entrada, Salida, Hover, Focus, Tap, Loading, Empty, Success, Error, Anclado a scroll |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Cada preset tiene una variante de movimiento reducido. Código listo por stack para Framer Motion, GSAP y CSS puro.

### `anti-patterns.json` — 100 reglas regex

| Campo | Descripción |
|---|---|
| `entries` | 100 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y (23), Contenido (15), Layout (13), Tipografía (10), Color (9), Calidad (9), Visual (9), Movimiento (8), Performance (4) |

La lista completa de reglas está en [Las 100 reglas anti-slop de IA](#las-100-reglas-anti-slop-de-ia--el-linter).

### `brands/*.json` — 110 specs de marca

| Campo | Descripción |
|---|---|
| `entries` | 110 (más `_index.json` que las lista todas) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotriz (8) |

Lista completa en [Las 110 especificaciones DESIGN.md de marca](#las-110-especificaciones-designmd-de-marca--por-categoría).

---

## Las 100 reglas anti-slop de IA — el linter

ux-skill distribuye un linter determinista basado en regex. **Sin LLM.** **Sin API.** **Sin red.** Se ejecuta en CI en ~200 ms sobre una app típica de Next.js. Sale con código no-cero en hallazgos Critical / High cuando `--fail-on high` está activo.

Las reglas vienen de `data/anti-patterns.json` (v2 preferida) con fallback a `references/foundations/anti-patterns.md` (v1 bash). Se distribuyen dos binarios: `bin/ux-lint.py` (Python, rápido, extensible) y `bin/ux-lint.sh` (Bash + perl-PCRE, para entornos sin Python).

### Reglas por categoría

#### Tipografía (3 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| high | `inter-as-display` | Inter usada como fuente display |
| medium | `hero-text-arbitrary-90px` | Tamaño de fuente arbitrario para hero |
| low | `font-system-only` | Stack de fuente del sistema sin tipografía elegida |

#### Color (6 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| high | `purple-to-blue-gradient` | Gradiente morado-a-azul por defecto de IA |
| high | `dark-text-on-dark-card` | Texto de bajo contraste sobre tarjeta |
| medium | `gradient-text-rainbow` | Texto con gradiente multi-stop |
| medium | `card-glow-purple-shadow` | Sombra de glow morado en tarjetas |
| medium | `gradient-mesh-purple-pink` | Hero con mesh morado-rosa |
| low | `tailwind-color-named-vague` | Colores Tailwind nombrados sin token semántico |

#### Layout (5 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| high | `three-equal-card-grid` | Tres tarjetas iguales en fila |
| medium | `centered-everything-hero` | Composición de hero todo-centrado |
| medium | `avatar-stack-overlapping` | Stack genérico de avatares solapados |
| low | `pill-rounded-full-everywhere` | `rounded-full` aplicado a todo |
| low | `nav-equal-hamburger-desktop` | Menú hamburguesa en desktop |

#### Contenido (5 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum en código que se envía |
| high | `emoji-in-ui` | Emoji usado como elemento de UI |
| high | `icon-emoji-stamp` | Emoji usado como sello de icono |
| high | `testimonial-fake-five-stars` | Testimonio hardcoded con cinco estrellas |
| medium | `fake-name-john-doe` | Nombres placeholder genéricos |

#### Movimiento (3 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Flecha rebotando en el CTA |
| low | `timing-300ms-default` | Timing de transición por defecto a 300 ms |
| low | `cubic-bezier-material-only` | Easing por defecto de Material por doquier |

#### A11y (6 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| high | `inline-svg-no-aria` | SVG sin aria-label o aria-hidden |
| high | `img-no-alt` | Imagen sin atributo alt |
| high | `link-onclick-no-href` | Anchor con onClick pero sin href |
| medium | `button-no-type` | Botón sin atributo type |
| medium | `heading-skip-h1-h3` | Nivel de encabezado saltado |
| medium | `infinite-scroll-no-pagination` | Scroll infinito sin fallback de teclado |

#### Calidad (6 reglas)

| Severidad | ID de regla | Nombre |
|---|---|---|
| high | `console-log-leak` | `console.log` en código de componente |
| medium | `inline-style-attribute` | Atributo style inline |
| medium | `any-type-leak` | Tipo `any` de TypeScript |
| medium | `arbitrary-z-index-9999` | Valor de z-index perezoso |
| low | `shadcn-default-everywhere` | Bloque de token shadcn por defecto sin modificar |
| low | `todo-fixme-comment` | TODO o FIXME en código que se envía |

#### Visual (1 regla)

| Severidad | ID de regla | Nombre |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur sin superficie de cristal |

### Uso del linter

**Escaneo puntual:**

```bash
uxskill lint .
# o
python3 bin/ux-lint.py src/
# o
bash bin/ux-lint.sh src/
```

**Puerta de CI (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Hook pre-commit:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Salida (ejemplo):**

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

## Las 110 especificaciones DESIGN.md de marca — por categoría

Marcas reales. Lenguajes de diseño reales. Especificaciones DESIGN.md reales — no paletas genéricas. Le dices al plugin «construye una landing al estilo de Stripe» y lee el vocabulario de marca real: rúbrica de voz, tokens de color, convenciones de movimiento, signature moves, anti-moves.

Cada marca se distribuye como un JSON estructurado (`data/brands/<slug>.json`) más una referencia en prosa (`references/brands/<slug>.md`).

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

### Automotriz (8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### Por qué importa esto

Los otros 8 plugins populares de UX para Claude generan «minimal moderno» o «dashboard limpio» — variantes de la misma estética por defecto. ux-skill te permite pedir **la claridad de Linear**, **la seriedad de Stripe**, **la moderación de Apple**, **el monolito de Tesla**, **la cercanía de Notion**, **la disciplina de gradientes de Cursor**, **la densidad de pelo de Raycast**, **el editorial cálido de Claude** — y el motor saca los tokens, voz, convenciones de movimiento y signature moves correctos del brand spec.

---

## Servidor MCP — el movimiento asimétrico

ux-skill distribuye un **servidor Model Context Protocol**. Ejecutas `ux-mcp` y el motor se convierte en un proceso stdio de larga duración al que cualquier host compatible con MCP — Claude Desktop, Cursor, Windsurf, agentes genéricos — puede llamar. Catorce herramientas: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Los mismos handlers de Python que usan los comandos slash; los mismos manifiestos de datos; el mismo recomendador determinista.

**Por qué este es el movimiento asimétrico:** ninguna de las ocho mejores skills de UX para Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) distribuye un servidor MCP. Están encerradas dentro del runtime de plugins de Claude Code. ux-skill es accesible desde cualquier host que hable MCP, incluidos agentes que nunca han oído hablar de un plugin de Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp es un extra opcional
ux-mcp                                  # arranca el servidor stdio JSON-RPC
```

Apunta tu cliente al binario `ux-mcp`. La documentación completa de herramientas, ejemplos JSON y configuración por cliente para Claude Desktop, Cursor y Windsurf vive en [docs/mcp.html](docs/mcp.html) y en `commands/ux-mcp.md`.

---

## El instalador para 17 IDEs

`uxskill init` (o `/ux-init` dentro de Claude Code) auto-detecta qué IDE usas y escribe el artefacto correcto. El mismo motor de Python. Las mismas recomendaciones. Diferente pegamento por IDE.

| IDE / Tool | Señal de detección | Artefacto instalado |
|---|---|---|
| Claude Code | `.claude/` o `CLAUDE.md` | Manifiesto de plugin en `.claude-plugin/plugin.json` + los 22 comandos + los 5 sub-agentes |
| Cursor | `.cursor/` o `.cursorrules` | Cabecera de prompt `.cursorrules` que apunta al motor |
| Windsurf | `.windsurf/` o `.windsurfrules` | `.windsurfrules` con la misma cabecera de prompt |
| GitHub Copilot | `.github/copilot-instructions.md` o `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | parche `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` o `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

En cada IDE, los mismos comandos de CLI `uxskill recommend` / `uxskill lint` / `uxskill stats` funcionan desde la terminal. El motor de Python es la fuente de la verdad; los artefactos de IDE son cabeceras de prompt finas que enrutan a él.

---

## Casos de uso — escenarios concretos

Ocho escenarios reales. Elige el más cercano a tu situación y adapta la invocación.

### 1. Construir un dashboard fintech en Cursor

Estás en Cursor trabajando en un dashboard de un neobanco MENA. Instalas el plugin y ejecutas discovery, recomendación y luego generación del dashboard.

```bash
pip install uxskill
uxskill init                                # detecta Cursor, escribe .cursorrules
uxskill discover                            # intake de 10 campos
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Luego en Cursor, pides: *«Genera la superficie del dashboard usando la recomendación en .ux/last-recommendation.json»*. Cursor lee la cabecera `.cursorrules`, carga la recomendación, despacha una generación de dashboard con restricciones explícitas.

### 2. Generar una landing al estilo de Stripe en Claude Code

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> ¿Tipo de proyecto? landing
> ¿Sector? fintech-payments
> ¿Tono? serio, técnico, seguro
> ¿Imprescindibles? dark-mode, AA, mobile-first
> ¿Prohibidos? purple-gradients, three-equal-cards
> ¿Marcas de referencia? stripe
> ¿Stack? nextjs-15-app-router
> ¿Región? global
> ¿Métrica de éxito? conversión de signup

/ux-recommend
> [devuelve estilo, paleta, par tipográfico, presets de movimiento, componentes y marcas ejemplares elegidos]

/ux-design "genera la landing usando el brand spec de Stripe como ejemplar"
> [frontend-engineer genera la página]

/ux-lint .
> [pasa — el brand spec de Stripe se respetó]
```

### 3. Auditar código existente buscando slop de IA en CI

Has enviado una app de Next.js hace dos semanas. Quieres un suelo firme contra huellas de IA en cada PR.

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

Las PRs que introducen gradientes morado-a-azul, Inter a 96 px, testimonios de «John Doe» o emojis como iconos fallan el CI. Sin coste de LLM. ~200 ms.

### 4. Pulir una superficie existente que «parece generada por IA»

Heredaste una app de React que parece cualquier otra web SaaS generada por IA. Quieres que deje de parecerlo.

```
/ux-critique src/components/Hero.tsx
> [3 aciertos, 3 fallos, 1 movimiento estratégico — la opinión es honesta]

/ux-lint src/
> [15 huellas de IA de alta severidad marcadas]

/ux-polish src/components/Hero.tsx
> [pasada cosmética impulsada por LLM + matar slop de IA]

/ux-fix
> [aplica hallazgos como commits atómicos, vuelve a ejecutar el linter]
```

Tres comandos, una superficie pulida, commits atómicos por arreglo.

### 5. Diseñar un command palette al estilo Linear

```
/ux-component command-palette --brief="estilo Linear, oscuro, shortcuts monospace, items recientes primero"
> [lee data/brands/linear.app.json para tokens + signature moves]
> [lee data/components.json para la anatomía + estados de command-palette]
> [despacha frontend-engineer con la spec explícita de Linear]
```

El componente generado usa los tokens de color reales de Linear, su stack tipográfico, sus convenciones de movimiento y densidades de pelo — no «UI oscura genérica».

### 6. Correr un taller de design thinking de 90 minutos con stakeholders

Tienes una sala con 5 personas durante 90 minutos. Quieres que salgan con un plan de juego, no con un vibe.

```
/ux-workshop "pivote de billetera de fidelización" \
  --participants="2 PMs, 1 diseñador, 1 lead de eng, 1 representante del cliente" \
  --minutes=90
```

El plugin facilita las cinco fases (exploración → mapa de calor → mapa de actores → boceto de solución → plan de juego) de extremo a extremo, cronometradas, con artefactos concretos por fase. La salida es `.ux/last-workshop.json` — el plan de juego, no solo «hallazgos interesantes».

### 7. Escribir un caso de estudio publicable tras el lanzamiento

Enviaste la billetera de fidelización. Quieres una pieza de portafolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [lee .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [genera caso de estudio editorial Wfrah con secciones numeradas (A)-(G), separadores de pelo, layout bilingüe seguro]
> [escribe case-studies/bashiti-loyalty.html]
```

El caso de estudio es un artefacto acabado y publicable — no un borrador. Monocromo puro, tipografía editorial, listo para enviar a tu portafolio.

### 8. Correr discovery en un contexto no-IA (solo intake estructurado)

Estás acotando un proyecto. Aún no necesitas una recomendación — necesitas un brief estructurado.

```bash
uxskill discover
# intake de 10 campos, guarda en .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Puedes entregar el JSON a tu equipo, pegarlo en un doc de Notion o meterlo en una herramienta de IA aparte. ux-skill también es una herramienta de intake estructurado, además de ser un motor.

### 9. Persistencia con MASTER.md — tus decisiones de diseño, en el repositorio

Tras `/ux-recommend`, persiste el estilo + paleta + tipografía + movimiento + componentes + marcas ejemplares + barreras elegidos como un archivo Markdown legible que tu equipo pueda revisar, comparar (diff) y versionar.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Escribe `.ux/design-system/MASTER.md` (YAML frontmatter + cuerpo) y `.ux/design-system/pages/<name>.md` por cada superficie generada vía `persist save-page`. Idempotente — la misma entrada produce salida byte a byte idéntica, así que re-ejecutarlo sobre estado no cambiado es un no-op en git.

---

## Frente a las alternativas

Tabla resumen corta. La comparativa completa lado a lado está en [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensión | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Comandos slash | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Componentes | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Presets de movimiento | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specs de marca | **110** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Reglas de antipatrones | **100** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter determinista apto para CI | **sí** | no | no | no | no | no | no | no | no |
| IDEs soportados | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Puerta de discovery | **10 campos** | implícita | implícita | implícita | implícita | implícita | implícita | implícita | implícita |
| Cadena de estado `.ux/` | **sí** | no | no | no | no | no | no | no | no |
| Estrellas (2026-05-28) | 14 | 83 958 | 54 406 | 25 202 | 15 455 | 5 762 | 2 391 | 2 164 | 955 |

### Evaluación honesta

- **ui-ux-pro-max** es más grande en notoriedad, distribuye 18 IDEs, tiene búsqueda estilo BM25 sobre su CSV. No distribuye manifiesto de componentes, manifiesto de movimiento, biblioteca de marcas ni linter determinista.
- **open-design** tiene 19 skills + preview pero solo soporte para Claude Code y sin capa anti-slop.
- **hallmark** es lo más cercano en espíritu (también anti-slop) pero es una única skill — sin motor, sin manifiestos, sin comandos encadenados.
- **material-3-skill** es excelente si específicamente quieres Material Design 3. No competimos en MD3.

Para detalle completo por dimensión, ver [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Hoja de ruta

### v2.1 — Completitud del linter (Q3 2026)

- **+17 reglas de antipatrón diferidas** para llegar a 52 en total. Objetivos: estados hover oscuro-sobre-oscuro, codificación de estado solo por color, escalada redundante de z-index, breakpoints hardcoded en JS, opacity en lugar de estado disabled, etc.
- **`uxskill lint --fix` para reescrituras seguras** de hallazgos mecánicamente arreglables (button-no-type, img-no-alt con string vacío, eliminación de console-log-leak).
- **Extensión de VS Code** que aflora los hallazgos del linter en línea (sin necesidad de ejecutar CI).

### v2.2 — Expansión del manifiesto de componentes (Q4 2026)

- **+50 componentes** para llegar a 198 en total. Nuevos: combobox con filtro async, command-palette con heurística de items recientes, conditional-form-step, variantes de payment-element, date picker consciente de RTL, input de teléfono específico MENA, calendar grid con overlay hijri.
- **Emisión de código por componente** en 6 stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Playground de componentes** en uxskill.laithjunaidy.com/playground — prueba el motor de recomendación + ve preview en vivo del componente.

### v3 — El marketplace + el lock-in (2027)

- **Marketplace de brand specs** — publica y descubre brand specs de la comunidad. Pago por publicar para financiar la moderación.
- **Reglas de antipatrón custom** — los proyectos pueden definir sus propias reglas regex en `data/anti-patterns.local.json` (ya distribuidas en v2; v3 añade descubrimiento + compartición).
- **`uxskill plan`** — planificación completa de sitios multi-página desde un brief, no solo una superficie.
- **Paridad con plugin de Figma** — el mismo motor de recomendación, expuesto en Figma.

---

## Cómo contribuir

Issues y PRs bienvenidos. Tres áreas de alto apalancamiento:

### Añadir una regla de antipatrón

1. Edita `data/anti-patterns.json` — añade una entrada con `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Añade un test en `tests/linter/` — un archivo que dispara la regla, uno que no.
3. Ejecuta `uxskill lint tests/linter/should-trigger/<rule>.tsx` — confirma que se dispara. Ejecuta sobre `tests/linter/should-not-trigger/<rule>.tsx` — confirma que no.
4. Abre una PR.

### Añadir un brand spec

1. Crea `data/brands/<slug>.json` con `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Añade la prosa correspondiente en `references/brands/<slug>.md`.
3. Regístralo en `data/brands/_index.json`.
4. Abre una PR. La spec debe estar respaldada por referencias de fuente primaria (el producto real de la marca, su sistema de diseño público o su DESIGN.md si lo publican).

### Añadir un preset de movimiento

1. Edita `data/motion-presets.json` — añade una entrada con `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. El preset debe tener una variante de movimiento reducido. Sin excepciones.
3. Abre una PR.

### Proceso

- Lee [CONTRIBUTING.md](CONTRIBUTING.md) para el proceso completo.
- Lee [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Las nuevas reglas y brand specs se revisan buscando: anclaje en fuente primaria, ausencia de overfitting a un único proyecto, ausencia de emoji en cualquier dato, comportamiento seguro en RTL cuando aplique.

---

## Licencia, autor, agradecimientos

### Licencia

MIT. Úsalo, fórkalo, construye sobre él. Si te ahorra enviar slop de IA, ponle una estrella al repo — es la forma más barata de apoyarlo.

### Autor

**Laith Aljunaidy** — fundador en solitario de [Dot](https://thedotwallet.com), una plataforma de fidelización MENA-first. Construyendo ux-skill para que el frontend generado por IA deje de parecerse todo.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Sitio: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Agradecimientos

- Al equipo de Anthropic por Claude Code y la arquitectura de skill / plugin que hizo posible distribuir esto.
- A Nielsen Norman Group, Laws of UX (lawsofux.com) y la comunidad de investigación de UX cuyo trabajo informa `data/ux-guidelines.json`.
- A cada marca listada en `data/brands/` — sus sistemas de diseño públicos son la fuente de verdad de los brand specs.
- A los contribuidores originales de v1: una skill de Claude de un solo disparo que se convirtió en la semilla del motor Python de v2.
- A los 8 plugins populares de UX para Claude con los que nos comparamos — subieron el listón; esta es nuestra respuesta.

---

**ux-skill** · **v2.0.0-alpha.1** · Construido para que Claude Code, Cursor, Windsurf y todas las demás herramientas de codificación con IA produzcan frontend que no se lea como generado por IA.

> Pon una estrella al repo en [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Instala vía `pip install uxskill` o `npx uxskill init` · Explora la comparativa en [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
