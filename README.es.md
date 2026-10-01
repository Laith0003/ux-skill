[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · **Español** · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: el motor de inteligencia de diseño para Claude Code, Cursor y todas las demás herramientas de codificación con IA

**Un motor de inteligencia de diseño que hace que la UI generada por IA sea distintiva en lugar de genérica.** Intégralo en cualquiera de 17 herramientas de codificación con IA y lo que produces deja de parecer hecho por una IA. Gratis, MIT, sin conexión, sin LLM.

```bash
pip install uxskill
```

**[Dale una estrella a ux-skill en GitHub](https://github.com/Laith0003/ux-skill)** si te resulta útil: es la forma más sencilla de ayudar al proyecto. ¿Eres nuevo? Empieza por el [recorrido de 60 segundos](#instalación-rápida) o míralo en vivo en [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![Antes: hero genérico con foto de stock, degradado violeta suave, sin identidad de marca. Después: foto real de una obra bajo un velo oscuro, titular editorial con un acento ámbar y un formulario de presupuesto integrado en el hero. Mismo prompt, resultado distinto cuando ux-skill aporta las restricciones.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Antes: slop SEO genérico con foto de stock. Después: hero con foto real de obra bajo un velo oscuro, titular editorial con un acento ámbar, formulario de presupuesto en el hero. Misma herramienta de codificación con IA, mismo prompt, resultado distinto cuando ux-skill aporta las restricciones.*

> **v4.0, FOUNDATIONS: un solo comando crea un sistema de diseño completo, comprobado con WCAG, con árabe y escritura de derecha a izquierda incluidos.** El plugin de UX más potente para la codificación con IA. Un núcleo de razonamiento en Python con un sintetizador determinista de 7 ejes, 12 manifiestos JSON consultables (84 estilos, 176 paletas, 70 combinaciones tipográficas, 148 componentes, 184 sectores, 35 tipos de gráfico, 57 presets de movimiento, 112 leyes de UX, 171 reglas de antipatrones, 25 stacks tecnológicos, 160 especificaciones de marca), 18 comandos slash, 5 sub-agentes, 25 herramientas MCP y un linter determinista anti-slop de IA. Multi-IDE: se instala en Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer y Roo Cline.

> **El nombre de la marca es `ux-skill`.** El nombre del paquete en PyPI / npm sigue siendo `uxskill`. El repositorio de GitHub está en [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Autor:** [Laith Aljunaidy](https://laithjunaidy.com), diseñador y CTO en Amán · **Sitio:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Comparativa con cada plugin de UX para Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#el-instalador-para-17-ides)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Novedades de 4.0: fundamentos

Entra un color de marca, sale un sistema de diseño, con su contraste comprobado antes de que te llegue.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 o posterior. Para el servidor MCP, `pip install --upgrade 'uxskill[mcp]'`. Con pipx, `pipx install uxskill` (sobre una 3.x ya instalada, `pipx upgrade uxskill`). Con npm, `npx uxskill@latest`. ¿Vienes de 3.x? La [guía de migración](docs/migrating-to-4.md) asigna cada token de 3.x a su rol en 4.0.

**¿Construyes un producto o una landing?** Recibes `tokens.css` para enlazar desde tu página, `fonts.css` con fuentes de respaldo de métricas ajustadas para las tipografías elegidas, `fonts-self-host.css`, que carga las tipografías desde tus propios archivos, `tokens.json` para herramientas, arte de marca decorativo en `art/` y `system-report.md`, que explica con palabras sencillas qué se construyó, por qué y con qué composición de página empezar. Aplica estilos con los roles (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`) y cambia a modo oscuro, alto contraste, espaciado compacto, derecha a izquierda o movimiento reducido con un solo atributo en `<html>`. Carga las tipografías con el enlace de Google Fonts que indica el informe, o con `fonts-self-host.css` y una carpeta `fonts/`, y enlaza `fonts.css` con cualquiera de las dos, antes de `tokens.css`; no edites ninguno de los dos archivos. Con `--brief`, el aspecto sigue al sector y al tono cuando el brief los nombra, y los campos estructurados (edad, idiomas, esquema por defecto, contexto de lectura) fijan el tamaño del texto, los objetivos táctiles, las escrituras y el esquema con el que se abre; discovery no pregunta por el sector, así que `/ux-system create` lo pide. En Claude Code, `/ux-system create` comprueba la versión instalada, ejecuta la compilación y explica el informe.

**¿Diseñas un sistema de diseño?** Nueve fundamentos (color, tipografía, espaciado, maquetación, radio, borde, elevación, movimiento, imagen), cada uno variando de forma continua con los siete ejes, con primitivas y roles semánticos, en el formato de design tokens del W3C (DTCG 2025.10) con los valores de cada modo. Mismas entradas, mismos bytes. Por MCP, `ux_system_build` devuelve el informe, el resultado de la comprobación y el tamaño de cada archivo, y escribe los mismos archivos que el comando cuando recibe `out`.

- **Comprobación WCAG.** Cada combinación de colores de texto, control y foco se mide en modo claro y oscuro, con contraste normal y alto: WCAG 1.4.3 (texto 4.5:1) y 1.4.11 (no textual 3:1) con contraste normal, WCAG 1.4.6 (texto 7:1) con alto contraste, más un mínimo propio de 4.5:1 en alto contraste para la mayoría de los elementos no textuales, ya que WCAG no fija un nivel reforzado para lo no textual. Un sistema que no pasa no se escribe; el mensaje dice qué cambiar.
- **Seguro por defecto.** Nunca sobrescribe un archivo que sea distinto. `--force` reemplaza archivos solo cuando lo pides.
- **Árabe.** Con `dir="rtl"` el texto cambia a una fuente árabe con sus propios tamaños e interlineado; el espaciado usa propiedades lógicas y el movimiento se refleja. `--latin-only` lo deja fuera.

**Un sistema que ya tienes.** `/ux-system enhance --from` lo lee con sus propios nombres (tokens DTCG, propiedades personalizadas de CSS, un tema de Tailwind, archivos de reglas en markdown o una exportación de variables de Figma), lo pasa por la misma comprobación y mide lo que tu código hace realmente con él; no se reescribe nada. `/ux-system extend --from` añade fundamentos, roles o contratos sin cambiar ningún token que ya tenga, en un archivo de extensión junto a él, y `uxskill system export` lo escribe como tokens.css, un tema de Tailwind 4 o variables de Figma. La 4.2 añade la capa de confianza (lint en cada escritura, un revisor de acabado) y el lanzamiento. Consulta el [changelog](CHANGELOG.md).

**Componentes y secciones.** 23 contratos de componentes indican qué tokens enlaza cada parte de un control en cada estado y cómo se mueve cada estado: un cambio de estado transiciona con `motion.state`, una pulsación escala con `motion.press.scale` (y se queda quieta con movimiento reducido), y las pestañas, menús y controles segmentados deslizan un único indicador. 14 contratos de secciones (hero, precios, FAQ, pie de página y el resto) nombran la función de cada sección, los componentes que admiten sus huecos, la prueba que necesita y cómo se apila en un móvil. Las páginas construidas con ellos usan fotografías; los fragmentos de interfaz son imagen adicional, nunca un sustituto.

**Un linter que lee la página.** 171 reglas, muchas con una comprobación sobre el CSS y el marcado ya analizados, leen el propio sistema de la página: el movimiento se temporiza según su curva, el interlineado de los titulares display se mantiene en el mínimo del motor y un control oculto debe salir del orden de tabulación. `uxskill lint --render` abre cada página en Chromium sin interfaz a ancho de escritorio y de móvil y la recorre: anillos de foco que no se ven o quedan recortados, hover y pulsación que responden tarde, foco perdido tras Escape y una pulsación que sigue moviéndose con movimiento reducido.

**Menos comandos.** 25 comandos slash pasan a ser 18. `/ux-discover` acepta `--frame` y `--recommend`, `/ux-design` acepta `--component`, `--dashboard` y `--from-image`, `/ux-polish` repite lint, fix y re-lint hasta que la puntuación llega a 90 o pasan tres vueltas, y `/ux-init` acepta `--stats`. Los siete nombres antiguos siguen funcionando como alias y desaparecen en 4.1; consulta [los alias](#alias-retirados-en-41).

**Playbooks de superficie.** Las reglas de landing, dashboard y componente viven en `references/surfaces/`, un playbook cada una. `/ux-design` carga exactamente uno, elegido según su modo, así que un build de dashboard nunca lee reglas de hero.

Tests: **9764 superados**. Sin conexión. Determinista. Nunca se llama a un LLM.

### Novedades de v3.1: fiel a la marca, responsive, vivo

- **La fidelidad a la marca se impone, no se espera.** El color primario se lee de los píxeles del LOGO (no del CSS más pintado); las fuentes por defecto se rechazan en favor del estilo de letra del logo. La marca extraída viaja `recommend` -> `synthesize`, y un **mínimo estricto** en `evaluate` hace FALLAR cualquier salida que pierda el color o el logo de la marca o no incluya imágenes reales. Interoperabilidad en ambos sentidos con la convención abierta `brand.md` (render + importación).
- **Mobile-first, comprobado.** Nuevos fundamentos de oficio (`responsive.md`, `component-behaviors.md`) más una comprobación consciente del ajuste de línea que falla ante scroll horizontal, una etiqueta de navegación, logotipo o botón que se parte en dos líneas, o una cabecera sticky demasiado alta.
- **La capa wow.** El motor deriva 2-3 momentos distintivos coordinados por página; la doctrina de que «el wow solo puede venir del usuario» queda descartada.
- **Linter más afinado** (152 reglas): detección de imagen obligatoria y de elementos solo con icono, reglas de tokens de relleno y de `100vw`; picsum con semilla se conserva, el aleatorio se elimina.

Notas completas en [CHANGELOG.md](CHANGELOG.md).

### Novedades de v3

- **Las especificaciones de marca pasan a ser datos de entrenamiento, no plantillas.** Las 160 brand specs ya no son un catálogo del que el recomendador elige, son vocabulario que el sintetizador destila. Cada llamada produce un sistema novedoso.
- **Sintetizador de 7 ejes** (warmth, contrast, density, geometry, formality, motion, type_personality). El brief mapea de forma determinista a valores de ejes; los ejes compilan a paleta + tipografía + spacing + radius + motion frescos.
- **Tres modos auto-despachados**: `strict_brand` (100% de una marca), `brand_anchor` (70% una marca + 30% adaptado por ejes a partir de marcas hermanas), `pure_synthesis` (sin marca nombrada, destila 8 ejemplos coincidentes en ejes).
- **El ledger de decisiones reordena al recomendador.** `.ux/decisions.jsonl` re-ranquea candidatos por victorias pasadas en el mismo bucket `(industry, ui_type)`. Cold-start seguro. Solo cuenta decisiones con `lint_score >= 80` + `user_accepted = true`.
- **Matriz de interacción entre ejes**: resolución explícita de conflictos entre ejes (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Sin reglas ad-hoc silenciosas.
- **Bucle automático `/ux-evolve`** (en 4.0, el bucle por defecto de `/ux-polish`): lint → polish → re-lint hasta puntaje ≥ 90, meseta o 3 vueltas en 4.0 (5 en v3). Quality gate en 65.
- **3 nuevas herramientas MCP** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Panel de stats local**: `uxskill stats --html` escribe `.ux/stats.html` que muestra lo que TU instalación ha aprendido. Sin telemetría, sin agregados globales.
- **223 tests pasan.** Offline. Determinista. Nunca llama a un LLM.

Detalles completos en [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Historial de estrellas

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Qué es ux-skill

ux-skill es un **motor de inteligencia de diseño** para herramientas de codificación con IA. Se ejecuta como paquete de Python (`pip install uxskill`), como plugin de Claude Code y como multi-instalador para 17 IDEs. El motor ingiere un brief de proyecto (sector, audiencia, tono, imprescindibles, elementos prohibidos, stack, región) y devuelve un sistema de diseño recomendado completo: estilo, paleta, par tipográfico, presets de movimiento, componentes, marcas ejemplares para estudiar y las barreras de antipatrones que deben respetarse. La recomendación es determinista, la misma entrada produce siempre la misma salida.

El plugin se sitúa entre tú y la herramienta de codificación con IA. Cuando le pides a Claude Code, Cursor o cualquier otro asistente de IA «construir una landing fintech», el asistente típicamente improvisa, y el resultado se identifica como generado por IA en cinco segundos (gradientes de morado a azul, tres tarjetas iguales, Inter en tamaño display, «John Doe» en los testimonios, transiciones por defecto de 300 ms, hero centrado, flechas rebotando en los CTA). ux-skill sustituye la improvisación por **restricciones estructuradas**: ejecutas `/ux-discover` para capturar el brief y elegir el sistema, `/ux-design` para generar el código y `/ux-lint` para verificar que pasa las 171 reglas deterministas anti-slop de IA antes del commit.

Este README es la referencia canónica. Cada comando, cada sub-agente, cada manifiesto de datos, cada ruta de instalación, cada especificación de marca, cada categoría de antipatrón, está todo documentado aquí. Si estás buscando un plugin de diseño para Claude Code o comparando herramientas de diseño con IA para Cursor, Windsurf o Codex, lee esto de principio a fin junto a [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Índice

1. [El cerebro, qué es v3.0](#el-cerebro-qué-es-v30)
2. [Instalación rápida](#instalación-rápida)
3. [Los números, comparativa en vivo frente a las 8 mejores skills de UX para Claude](#los-números-comparativa-en-vivo-frente-a-las-8-mejores-skills-de-ux-para-claude)
4. [Arquitectura, cómo encajan las piezas](#arquitectura-cómo-encajan-las-piezas)
5. [Los 18 comandos slash, referencia detallada](#los-18-comandos-slash-referencia-detallada)
6. [Los 5 sub-agentes](#los-5-sub-agentes)
7. [Los 11 manifiestos de datos](#los-11-manifiestos-de-datos)
8. [Las 171 reglas anti-slop de IA, el linter](#las-171-reglas-anti-slop-de-ia-el-linter)
9. [Las 160 especificaciones DESIGN.md de marca, por categoría](#las-160-especificaciones-designmd-de-marca-por-categoría)
10. [Servidor MCP, el movimiento asimétrico](#servidor-mcp-el-movimiento-asimétrico)
11. [El instalador para 17 IDEs](#el-instalador-para-17-ides)
12. [Casos de uso, escenarios concretos](#casos-de-uso-escenarios-concretos)
13. [Frente a las alternativas](#frente-a-las-alternativas)
14. [Hoja de ruta](#hoja-de-ruta)
15. [Cómo contribuir](#cómo-contribuir)
16. [Licencia, autor, agradecimientos](#licencia-autor-agradecimientos)

---

## El cerebro: qué es v3.0

v3.1.0 es el cambio arquitectónico más grande en la historia de ux-skill. El recomendador ya no elige plantillas de un catálogo, el motor **sintetiza** un lenguaje de diseño fresco por brief. El mismo brief siempre produce la misma salida (totalmente determinista), pero cada brief distinto recibe su propio sistema novedoso. Las brand specs dejan de ser plantillas; son datos de entrenamiento de los que el motor aprende vocabulario. El sistema tiene ojos sobre su propia historia, cierra el bucle de retroalimentación localmente y nunca llama a un LLM.

El compilador es un **sintetizador determinista de 7 ejes**, warmth, contrast, density, geometry, formality, motion, type_personality. Cada brief mapea a valores de ejes; los valores de ejes compilan a paleta + tipografía + spacing + radius + motion frescos. Las escalas tipográficas modulares eligen su razón a partir del contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Los primitivos de layout son responsive por construcción (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Los layouts rotos no pueden emitirse porque no son representables.

Hay tres modos auto-despachados: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% tokens de Stripe, ruta más rápida); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% adaptado por ejes a partir de 4 marcas hermanas); y `pure_synthesis` (sin marca nombrada → espacio infinito, 8 ejemplos coincidentes en ejes destilados en un lenguaje de diseño novedoso). Los conflictos entre ejes se resuelven con una **matriz de interacción de ejes** documentada, dense + corporate compila a 4px (gana density, escuela Bloomberg), airy + corporate a 12px (gana formality, lujo), soft + playful a 18px radius, sharp + corporate a 2px. Sin reglas ad-hoc silenciosas en la implementación.

El **ledger de decisiones** (`.ux/decisions.jsonl`, schema `_v: 1` bloqueado) cierra el bucle de retroalimentación. El recomendador ahora reordena candidatos por victorias pasadas en el mismo bucket `(industry, ui_type)`. Seguro en arranque en frío: se lo salta si hay menos de 3 antecedentes. Solo cuenta decisiones con `lint_score >= 80` Y `user_accepted = true`. Además, `/ux-polish` corre lint → polish → re-lint hasta puntaje ≥ 90, meseta o 3 vueltas, con un quality gate en 65 por debajo del cual la salida se rechaza salvo `--force`. Resultado: cada instalación se vuelve más inteligente sobre su propio corpus, cada ejecución es reproducible entre máquinas y el motor permanece totalmente offline.

---

## Instalación rápida

Tres rutas de instalación. Elige la que se ajuste a tu entorno.

### Ruta 1: marketplace de Claude Code (canónica)

Si trabajas en Claude Code, instala vía el marketplace de plugins:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Eso conecta los 18 comandos slash (más 7 nombres antiguos que se mantienen como alias hasta la 4.1) y los 5 sub-agentes a tu sesión de Claude Code. Tras la instalación, ejecuta `/ux-init` para configurar el directorio de estado `.ux/` por proyecto y verificar que el motor de Python es accesible.

### Ruta 2: pip (universal)

Si trabajas fuera de Claude Code (Cursor, Windsurf, CLI, CI), instala el paquete de Python:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

El paquete expone `ux` y `uxskill` como entry points de CLI, son el mismo binario.

### Ruta 3: npx (sin Python obligatorio)

Si no quieres gestionar Python directamente, el wrapper de npx arranca todo vía `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verificar la instalación

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

Los doce recuentos suman 1 262 entradas. Si algún recuento devuelve 0, falta el archivo JSON: abre una issue en [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Los números: comparativa en vivo frente a las 8 mejores skills de UX para Claude

Los recuentos de estrellas se verificaron por última vez vía `gh api` el **2026-05-28**. ux-skill (Laith0003/ux-skill) es el recién llegado, somos diminutos en notoriedad, profundos en arquitectura. La comparativa de abajo es honesta: dónde perdemos, dónde ganamos.

| Plugin | Estrellas | Arquitectura | Comandos slash | Linter (apto para CI) | Specs de marca | Componentes | Presets de movimiento | IDEs soportados |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83 958** | Python BM25 + CSV, skill única | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54 406** | Node.js + 19 skills + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25 202** | Bash + buen gusto basado en investigación | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15 455** | Único SKILL.md de 62 KB + scripts | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5 762** | Biblioteca de skills cableada con MCP | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2 391** | Skill mono-estética | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2 164** | Skill de diseño anti-slop | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Componentes MD3 + auditoría | 1 | - |, | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Motor de Python + 12 manifiestos + 18 comandos + 5 sub-agentes + linter de CI** | **18** | **171 reglas deterministas** | **160** | **148** | **57** | **17** |

### Dónde perdemos

- **Notoriedad.** Ellos tienen cientos de miles de estrellas. Nosotros tenemos 14. Danos una estrella, es la forma más barata de ayudar.
- **Reconocimiento de marca.** ui-ux-pro-max y open-design llevan una ventaja medida en meses, no en días.
- **Pulido de marketing.** Tienen capturas, vídeos de demo y una landing descubrible. Nosotros tenemos un README exhaustivo y una landing modesta.

### Dónde ganamos

- **Biblioteca de componentes:** 148 componentes documentados con anatomía, estados, tokens usados y especificaciones de movimiento. Ninguno de los otros 8 distribuye un manifiesto de componentes.
- **Presets de movimiento:** 57 entradas listas por stack (Framer Motion, GSAP, CSS) con fallbacks de movimiento reducido. Ninguno de los demás distribuye un manifiesto de movimiento.
- **Linter de antipatrones:** 171 reglas deterministas, se ejecuta en CI, sale con código no-cero en Critical/High. Ninguno de los demás distribuye un linter determinista.
- **Specs de marca:** 160 especificaciones DESIGN.md reales (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude y 96 más). Ninguno de los demás distribuye una biblioteca de marcas.
- **17 IDEs soportados:** el mismo motor, diferente pegamento por IDE.
- **18 comandos slash:** discovery, generación (páginas, componentes, dashboards, a partir de una imagen), auditoría, lint, bucle de pulido, bucle de fix, caso de estudio, taller, copy, motion, a11y, conductor, totalmente integrados.

Tabla completa lado a lado en [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Arquitectura: cómo encajan las piezas

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

### Cómo funciona realmente el motor

1. **Entrada.** Proporcionas un brief, ya sea de forma interactiva con `/ux-discover` (10 campos) o de forma no interactiva con flags para `ux recommend`.
2. **5 búsquedas en paralelo.** El motor lanza cinco consultas simultáneas sobre los manifiestos:
   - **Sector → recommended_styles** (industries.json)
   - **Estilo → compatibilidad de paleta + tipografía + movimiento** (styles.json)
   - **Tono × imprescindible → filtro de paletas** (palettes.json)
   - **Stack → compatibilidad de componentes + presets de movimiento** (tech-stacks.json, motion-presets.json)
   - **Prohibido + región → barreras + lista corta de marcas ejemplares** (anti-patterns.json, brands/)
3. **Fusión.** Un fusionador determinista ordena a los candidatos, resuelve conflictos (p. ej., un modo oscuro imprescindible impone el modo de la paleta) y emite un único sistema recomendado.
4. **Salida.** Un documento JSON con el estilo elegido, la paleta, la pareja tipográfica, los 5 mejores presets de movimiento, los 12 mejores componentes, las 5 mejores marcas ejemplares y las 171 barreras de antipatrones activas. Más un bloque de justificación que explica cada elección.
5. **Generación.** Los comandos posteriores (`/ux-design` en sus modos de página, componente, dashboard e imagen, y `/ux-system`) consumen la recomendación para generar código real a través de los sub-agentes.
6. **Verificación.** `/ux-lint` vuelve a escanear el código generado contra las 171 reglas. Sale con código no-cero en Critical/High en CI.

**Novedades de v3.** El recomendador ahora reordena candidatos desde `engine/decisions/` usando `.ux/decisions.jsonl` (solo cuenta decisiones con `lint_score >= 80` Y `user_accepted = true`; seguro en arranque en frío por debajo de 3 antecedentes). La ruta de generación puede pasar por `engine/synthesizer/`, un compilador determinista de 7 ejes que produce tokens nuevos de paleta + tipografía + espaciado + radio + movimiento para cada brief en lugar de elegir plantillas de un catálogo. Detalles en [El cerebro, qué es v3.0](#el-cerebro-qué-es-v30).

**Python piensa. HTML muestra. Markdown encadena.**

---

## Los 18 comandos slash: referencia detallada

Cada comando se distribuye como un archivo `.md` en `commands/` con `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` y `output state file`. Las descripciones siguientes están condensadas; la fuente completa es la especificación de referencia.

Los comandos se agrupan en siete bloques: **arranque e inventario**, **discovery y recomendación**, **generación**, **auditoría y verificación**, **corrección y pulido**, **discovery y narrativa**, y **conductor**. Siete nombres de 3.x siguen funcionando como [alias](#alias-retirados-en-41) hasta la 4.1.

### Arranque e inventario

#### `/ux-init`: arrancar el proyecto

- **Qué:** Detecta el IDE que usas (`.claude/`, `.cursor/`, `.windsurf/`, etc.), instala el artefacto correcto, verifica que el motor de Python es accesible e imprime un snapshot de estadísticas. `--stats` imprime solo el snapshot: versión + recuentos de entradas de los manifiestos de datos.
- **Cuándo usar:** Primera instalación en un proyecto nuevo. Tras clonar un proyecto que usa ux-skill. Después de `pip install --upgrade uxskill`. `--stats` tras la instalación, tras una actualización o cuando una recomendación devuelve elecciones sorprendentes y sospechas que los manifiestos están incompletos.
- **Cuándo saltar:** Ya lo ejecutaste en este proyecto y nada ha cambiado. `--stats` nunca hace falta saltarlo: es una lectura de 50 ms.
- **Invocación:** `/ux-init` (sin argumentos), `/ux-init --stats`, o `uxskill init` / `uxskill stats` desde la CLI. `--decisions` añade el resumen del ledger de decisiones; `--html` escribe `.ux/stats.html`.
- **Salida:** Artefacto por IDE (ver [El instalador para 17 IDEs](#el-instalador-para-17-ides)) + directorio `.ux/` + resumen por stdout. `--stats`: JSON por stdout (ver [Verificar la instalación](#verificar-la-instalación) más arriba).
- **Encadena con:** `/ux-discover` a continuación. `--stats` es solo de diagnóstico.

#### `/ux-mcp`: ejecutar el motor como servidor MCP

- **Qué:** Inicia el motor como servidor Model Context Protocol sobre stdio. 25 herramientas (el recomendador, el linter, la persistencia, el sintetizador, el ledger de decisiones, la extracción de imágenes, los manifiestos de datos, y la creación, importación, mejora, ampliación, exportación y comprobación de un sistema de diseño) pasan a poder llamarse desde cualquier host compatible con MCP, sin el plugin.
- **Cuándo usar:** Trabajas en otro host compatible con MCP y quieres el mismo motor. Ejecutas un pipeline multiagente que necesita una única fuente de restricciones de diseño. Quieres el recomendador o el linter como proceso de larga duración en CI.
- **Cuándo saltar:** Estás en Claude Code con el plugin instalado; los comandos slash ya llegan al motor. Necesitas una respuesta puntual; `uxskill recommend` o `uxskill lint` es más sencillo.
- **Invocación:** `/ux-mcp`, o `ux-mcp` desde la terminal tras `pip install 'uxskill[mcp]'`.
- **Salida:** Un servidor JSON-RPC sobre stdio. Consulta [Servidor MCP](#servidor-mcp-el-movimiento-asimétrico) y `commands/ux-mcp.md` para la configuración de cada cliente.
- **Encadena con:** Nada; es un transporte, no un paso.

### Discovery y recomendación

#### `/ux-discover`: la función forzosa (intake de 10 campos, framing, recomendación)

- **Qué:** El intake obligatorio de 10 campos por el que pasa todo proyecto antes de cualquier comando de generación. Tipo de proyecto, audiencia, objetivo principal, tono, imprescindibles, prohibidos, marcas de referencia, stack, región, métrica de éxito. **Sin improvisación.** Las frases prohibidas («moderno», «limpio») obligan al usuario a ser concreto. Después ejecuta el recomendador: las 5 búsquedas en paralelo del motor de Python sobre 12 manifiestos devuelven un único sistema de diseño fusionado (Sector → Estilo → Paleta → Tipografía → Movimiento + Componentes + Marcas ejemplares + Barreras).
- **Modos:** `--frame` captura para quién, outcome, hipótesis y señal de éxito en un bloque de framing de cuatro campos, más ligero que el intake completo. `--recommend` ejecuta solo el recomendador, a partir de un brief guardado o de flags puntuales.
- **Cuándo usar:** Antes de cualquier `/ux-design` o `/ux-system`. Siempre que un brief anterior se haya quedado obsoleto. `--frame` al inicio de un proyecto, sprint o encargo puntual, o a mitad de camino cuando una conversación ha derivado. `--recommend` cuando reorientas un producto que se ve cansado.
- **Cuándo saltar:** Estás arreglando un bug (`/ux-fix`). Solo ejecutas una pasada de linter (`/ux-lint`). El brief no ha cambiado desde la última sesión.
- **Invocación (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` o `/ux-discover --recommend`.
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
- **Salida:** `.ux/last-discovery.json` (el brief de 10 campos), `.ux/last-recommendation.json` (estilo elegido, paleta, pareja tipográfica, 5 mejores presets de movimiento, 12 mejores componentes, 5 mejores marcas ejemplares, las 171 barreras de antipatrones activas, más justificación) y, con `--frame`, `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Encadena con:** `/ux-design [extra brief]` → código frontend basado en la recomendación. `/ux-design --component <name>` → un componente alineado con las restricciones descubiertas. `/ux-system` → sistema de diseño completo a partir de la recomendación. `/ux-lint` → verifica el código generado.

### Generación

#### `/ux-design`: genera una superficie bonita y anti-slop desde un brief

- **Qué:** Genera un artefacto frontend completo y de calidad de producción (landing, sitio de marketing, app shell) a partir del brief de discovery + recomendación. Despacha `frontend-engineer` con dirección creativa basada en las referencias anti-slop y de arsenal. El brief, o un flag, elige uno de cuatro modos:
  - **página** (por defecto): una página completa o una superficie de varias secciones. Escribe `.ux/last-design.json`.
  - **`--component [name]`**: un único componente de calidad de producción (botón, modal, navbar, sidebar, tarjeta, tabla, formulario, gráfico). Los cuatro estados de interacción, accesible, fiel a la marca. Busca primero el componente en `.ux/last-recommendation.json` y, si no, consulta directamente el manifiesto. Escribe `.ux/last-component.json`.
  - **`--dashboard`**: disciplina de densidad de datos, layout bento, números monospace tabulares, patrones de sparkline, sin abuso de tarjetas, colores semánticos de estado, movimiento contenido. No es un sitio de marketing con gráficos pegados. Escribe `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: lee una imagen de referencia (PNG/JPG/WebP) con visión por computadora pura de Pillow (paleta dominante, polaridad del fondo, señal tipográfica), la compara con los manifiestos de paletas y estilos y construye a partir de la recomendación resultante. `--extract-only` se detiene tras la extracción. Escribe `.ux/last-image-extract.json`.
- **Cuándo usar:** «Diseña», «constrúyeme», «genera una landing», «crea un dashboard», «haz un componente», «construye un botón», «diseña el panel de admin», «consola de operaciones», «tablero de KPI», «hazlo como esta captura», cualquier petición de entregable visual de formato libre.
- **Cuándo saltar:** Quieres una revisión, no un build (usa `/ux-audit` o `/ux-critique`). Trabajo de backend o infraestructura.
- **Invocación:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Salida:** Código generado (HTML / Blade / JSX / Vue / Astro), más el archivo de estado del modo.
- **Encadena con:** `/ux-lint` → verifica contra las barreras. `/ux-polish` → pasada cosmética. `/ux-a11y` → auditoría de accesibilidad. `/ux-copy` → revisión de microcopy. `/ux-fix` → aplica hallazgos como commits atómicos.

#### `/ux-system`: genera un sistema de diseño inicial completo

- **Qué:** Propone un sistema de diseño inicial completo para un proyecto que no tiene uno, tokens (color, tipografía, espacio, movimiento, radio, sombra), documentos de fundamentos, contratos de componentes, emparejamientos para modo oscuro, conmutador de tema. Despacha `design-system-architect`.
- **Cuándo usar:** «No tenemos sistema de diseño», «constrúyenos un sistema», «propón tokens», «cuál debería ser nuestro tema», «monta nuestro DS».
- **Cuándo saltar:** El proyecto ya tiene sistema de diseño; usa `/ux-design --component` contra el sistema existente. Backend o infraestructura.
- **Invocación:** `/ux-system create` (el motor de fundamentos), `/ux-system enhance --from <file>` (medir un sistema que ya tienes), `/ux-system extend --from <file> --add <foundation>` (ampliarlo sin cambiarlo) o `/ux-system` (el flujo de 3.x; ejecuta discovery primero si aún no hay un brief guardado).
- **Salida:** `tokens.json`, `foundations.md`, contratos `components/*.md`, emisión opcional Tailwind / vanilla / SCSS. Escribe `.ux/last-system.json` para contexto de cadena.
- **Encadena con:** `/ux-design --component` → construir sobre el nuevo sistema. `/ux-design` → generar una superficie con los nuevos tokens.

#### `/ux-motion`: tratamiento de movimiento

- **Qué:** Genera la capa de movimiento de una superficie, duraciones, easings, coreografía, fallbacks de movimiento reducido, disciplina de rendimiento. También audita el movimiento existente contra las 5 dimensiones (timing, easing, significado, movimiento reducido, rendimiento).
- **Cuándo usar:** «Comprueba el movimiento», «¿están bien las animaciones?», «arregla el movimiento», «revisa las animaciones», «auditoría de movimiento», «pasada de rendimiento sobre el movimiento».
- **Cuándo saltar:** La superficie no tiene movimiento (usa `/ux-audit` o `/ux-polish`). Backend o infraestructura.
- **Invocación:** `/ux-motion path/to/component.tsx` (modo auditoría) o `/ux-motion --generate hero-entry` (generación).
- **Salida:** Código actualizado (en modo generación) o informe `.ux/last-motion.json` (en modo auditoría).
- **Encadena con:** `/ux-fix` → aplica hallazgos de movimiento. `/ux-polish` → afinar.

### Auditoría y verificación

#### `/ux-lint`: linter determinista basado en regex (sin LLM, apto para CI)

- **Qué:** Ejecuta 171 reglas contra tu código. Sin llamada a LLM. Sale con código no-cero en Critical / High en CI. Fuente: `data/anti-patterns.json`. Las reglas cubren A11y (45), Contenido (35), Layout (18), Tipografía (16), Movimiento (14), Visual (14), Calidad (12), Color (10), Performance (5), Profundidad (2).
- **Cuándo usar:** Hook de pre-commit. Puerta de CI. Primera pasada rápida en una base de código grande antes de pagar el coste de `/ux-audit`. Después de `/ux-design` en cualquier modo para verificar la generación.
- **Cuándo saltar:** Quieres un bucle de fix (el linter reporta, no edita, encadena con `/ux-polish --fix` o `/ux-fix`). Quieres juicio de gusto (usa `/ux-critique`).
- **Invocación (slash):** `/ux-lint src/`.
- **Invocación (CLI):** `uxskill lint .` o `python3 bin/ux-lint.py .` o `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocación (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Salida:** Hallazgos a stdout (ubicación, id de regla, severidad, evidencia). Código de salida 0 si está limpio, no-cero en Critical/High cuando `--fail-on high` está activo.
- **Encadena con:** `/ux-polish --fix` → contraparte impulsada por LLM sobre los mismos patrones. `/ux-fix` → aplica hallazgos como commits, ordenados por severidad. `/ux-audit` → pasada completa de razonamiento con 6 lentes. `/ux-next` → deja que el conductor decida.

#### `/ux-audit`: auditoría de diseño con 6 lentes

- **Qué:** Una revisión estructurada y opinada contra seis lentes (claridad, jerarquía, accesibilidad, voz, movimiento, gusto), produciendo hallazgos etiquetados por severidad. Informe estilo Polaris. Lee `.ux/last-frame.json` primero, la audiencia y el outcome anclan la severidad de cada hallazgo.
- **Cuándo usar:** La superficie existe y quieres una crítica defendible. «Audita», «revisa la ux», «¿es esto bueno?», «¿qué está roto?», «destroza esto».
- **Cuándo saltar:** La superficie aún no existe (usa `/ux-design`). El usuario quiere una sola lente (usa el comando dirigido: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). El usuario quiere opinión de gusto (usa `/ux-critique`). Backend o infraestructura.
- **Invocación:** `/ux-audit https://example.com/pricing` o `/ux-audit src/components/Pricing.tsx`.
- **Salida:** Escribe `.ux/last-audit.json`, array `findings` con `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Encadena con:** `/ux-fix` → aplica hallazgos. `/ux-polish` → pasada cosmética. `/ux-design` → si se necesita rediseño estructural.

#### `/ux-a11y`: auditoría WCAG 2.1 AA + comprobaciones de cortesía común

- **Qué:** Auditoría WCAG 2.1 AA estructurada, más las comprobaciones de cortesía común que pasan los tools automáticos pero que aún hieren a los usuarios reales (visibilidad de foco, especificidad de errores, preferencias de movimiento, trampas de teclado, dependencia del color).
- **Cuándo usar:** Puerta de accesibilidad pre-envío. Tras un rediseño. «Comprobación de accesibilidad», «auditoría WCAG», «¿es esto accesible?», «revisión a11y», «test con lector de pantalla», «comprobación de navegación con teclado».
- **Cuándo saltar:** No es de cara al usuario. Backend o infraestructura. Bocetos en construcción.
- **Invocación:** `/ux-a11y https://example.com` (URL en vivo preferido, los tools automáticos y las pruebas de teclado solo funcionan en vivo).
- **Salida:** Escribe `.ux/last-a11y.json`, array `findings` con `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Encadena con:** `/ux-fix` → aplica hallazgos como commits. `/ux-copy` → arregla alt text y cableado de errores de formulario como parte de una pasada de copy.

#### `/ux-critique`: opinión de gusto (3 aciertos, 3 fallos, 1 movimiento estratégico)

- **Qué:** La opinión de un diseñador, no una auditoría estructurada, no una puntuación de severidad, solo una toma ceñida y opinada que nombra lo que funciona, lo que no, y el único movimiento estratégico que cambiaría más.
- **Cuándo usar:** «¿Qué piensas?», «¿es esto bueno?», «critica esto», «opinión honesta», «¿es correcto el vibe?», «¿se siente como nosotros?», «¿deberíamos enviar esto?».
- **Cuándo saltar:** El usuario quiere explícitamente una auditoría estructurada (usa `/ux-audit`). Backend o infraestructura.
- **Invocación:** `/ux-critique https://example.com`.
- **Salida:** Escribe `.ux/last-critique.json`, 3 aciertos, 3 fallos, 1 movimiento estratégico, además de prosa.
- **Encadena con:** `/ux-design` si la opinión recomienda rediseño. `/ux-polish` si recomienda afinar.

#### `/ux-copy`: revisión + reescritura de microcopy

- **Qué:** Evalúa cada cadena visible contra la rúbrica de voz y produce una reescritura antes/después. Detecta: «el formulario contiene errores» (genérico), «John Doe» (placeholder), copy celebratorio cantarín de IA, CTAs genéricos, empty states muertos, errores inútiles.
- **Cuándo usar:** La estructura está bien pero las palabras flojean. «Revisa el copy», «arregla el microcopy», «los mensajes de error son malos», «reescribe esto», «afina las cadenas», «los botones suenan genéricos», «este empty state está muerto».
- **Cuándo saltar:** Problemas de layout (usa `/ux-audit` o `/ux-polish`). Problemas de copy ligados a accesibilidad como el alt text (usa `/ux-a11y`). Backend o infraestructura.
- **Invocación:** `/ux-copy src/views/checkout.blade.php`.
- **Salida:** Escribe `.ux/last-copy.json`, array `strings` con `{location, severity, before, after, notes}`, además de rúbrica + locales que necesitan traducción.
- **Encadena con:** `/ux-fix` → aplica reescrituras. `/ux-a11y` → vuelve a comprobar tras los arreglos de copy.

### Fix y pulido

#### `/ux-fix`: aplicar hallazgos como commits atómicos

- **Qué:** Lee el último informe de `.ux/` (audit, copy, a11y, motion o polish), valida el árbol de trabajo y aplica los hallazgos como commits atómicos vía los sub-agentes correctos. Vuelve a verificar reejecutando el comando originador.
- **Cuándo usar:** Tras ejecutar un comando de clase auditoría y revisar los hallazgos. «Arregla los hallazgos», «aplica los arreglos», «ejecuta el bucle de fix», «parchea la superficie», «haz los cambios», «vete a arreglarlo».
- **Cuándo saltar:** No hay informe previo en `.ux/`. El árbol de trabajo está sucio y el usuario no ha aceptado stash/commit. Los arreglos requieren juicio de diseño, no aplicación mecánica (usa `/ux-design` para rediseñar).
- **Invocación:** `/ux-fix` (auto-detecta qué informe arreglar) o `/ux-fix --from=last-a11y.json`.
- **Salida:** Commits atómicos por hallazgo. Reejecuta el comando originador y actualiza el archivo `.ux/last-*.json`. Imprime un resumen.
- **Encadena con:** `/ux-next` → el conductor elige el siguiente movimiento.

#### `/ux-polish`: bucle de lint, fix y re-lint + matar el slop de IA

- **Qué:** Primero un bucle determinista sobre un archivo HTML local: lint, seis pasadas de pulido idempotentes, re-lint, hasta que la puntuación llega a 90, se estanca o pasan tres vueltas (`--rounds` cambia el tope). Por defecto, la salida del bucle se queda en `<file>.evolved.html` y el original nunca se toca. Solo `--loop-only` o `--fix` reemplazan el original, tras comprobar que el árbol de trabajo está limpio, y un quality gate en 65 impide que un resultado que no pasa lo reemplace salvo `--force`; con `--brand-file`, el mínimo de fidelidad a la marca se mantiene en cada salida. Después, la pasada de gusto: ritmo del espaciado, jerarquía más nítida, detección de slop de IA, consistencia de tokens. La contraparte impulsada por LLM de `/ux-lint`, que usa tu criterio en las decisiones de gusto. `--loop-only` ejecuta solo el bucle; `--no-loop`, solo la pasada de gusto; `--fix` aplica los hallazgos de gusto.
- **Cuándo usar:** La estructura está bien pero la ejecución está floja. «Pule», «aprieta esto», «quita el slop de IA», «hazlo premium», «haz que esto no parezca de IA», «el espaciado se siente raro», «esto parece genérico», «necesita más gusto», «mejora hasta una puntuación de 90+», «déjalo listo para publicar».
- **Cuándo saltar:** A la superficie le falta funcionalidad central (arregla eso primero). Necesita un rediseño, no un pulido (usa `/ux-design`). Problemas de copy (usa `/ux-copy`). Problemas de movimiento (usa `/ux-motion`). Problemas de a11y (usa `/ux-a11y`).
- **Invocación:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Salida:** `<file>.evolved.html` del bucle (sustituye al original solo con `--loop-only` o `--fix`), código actualizado con `--fix`, `.ux/last-evolve.json`, una línea en `.ux/decisions.jsonl` y `.ux/last-polish.json`, que describe los hallazgos de gusto.
- **Encadena con:** `/ux-lint` → verifica que el pulido se sostuvo. `/ux-a11y` → vuelve a comprobar la accesibilidad.

### Discovery y narrativa

#### `/ux-research`: planificación + síntesis de investigación

- **Qué:** Modo planificación: escribe guiones de entrevista, encuestas, filtros de reclutamiento. Modo síntesis (`--synthesize`): digiere entrevistas, analítica, sitios competidores, resultados de A/B, tickets de soporte en recomendaciones. Despacha `research-synthesizer`.
- **Cuándo usar:** «Planifica un estudio de investigación», «necesito preguntas de entrevista», «diseña una encuesta», «cómo recluto usuarios», «plan de user testing», «estudio de diario», «test de preferencia», «fake door», «smoke test», «sintetiza mis notas de entrevista».
- **Cuándo saltar:** La respuesta ya se conoce con alta confianza. Decisiones reversibles de bajo riesgo. Backend o infraestructura.
- **Invocación:** `/ux-research --plan "loyalty wallet adoption in MENA"` o `/ux-research --synthesize interviews/*.md`.
- **Salida:** Escribe `.ux/last-research.json`, plan de investigación o temas sintetizados + evidencia + recomendaciones.
- **Encadena con:** `/ux-discover --frame` → integrar los hallazgos en un marco. `/ux-design` → generar a partir de los hallazgos. `/ux-workshop` → dirigir un taller usando la investigación como entrada.

#### `/ux-workshop`: taller de design thinking en 5 fases

- **Qué:** Facilita un taller de discovery / design thinking de extremo a extremo. Cinco fases secuenciales (exploración → mapa de calor → mapa de actores → boceto de solución → plan de juego). Cronometrado. Artefactos concretos por fase. Termina con una decisión, no con «hallazgos interesantes».
- **Cuándo usar:** Pregunta real, participantes reales, presupuesto real de tiempo. «Corre un taller», «facilita un discovery», «hagamos una sesión de design thinking», «tengo stakeholders por una hora, ¿qué hacemos?», «arranca el proyecto».
- **Cuándo saltar:** El brief ya está claro y acotado. Lluvia de ideas en solitario (usa `/ux-design` o `/ux-discover --frame`). El equipo está en plena ejecución, no en discovery.
- **Invocación:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Salida:** Escribe `.ux/last-workshop.json`, plan de juego + artefactos por fase.
- **Encadena con:** `/ux-design` → ejecuta el plan de juego. `/ux-research` → rellena las brechas que el taller sacó a la superficie. `/ux-case-study` → publica el recorrido.

#### `/ux-case-study`: caso de estudio publicable (formato editorial Wfrah)

- **Qué:** Genera un caso de estudio del proyecto en formato editorial monocromo puro, tipografía Wfrah, separadores finos, códigos de sección numerados de (A) a (G), maquetación segura para contenido bilingüe. Un documento, no un folleto de marketing. Lee de `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Cuándo usar:** Post-lanzamiento. Tras un hito discreto. «Escribe un caso de estudio», «caso de estudio de este proyecto», «haz el documento de cierre», «publica este trabajo», «pieza de portafolio».
- **Cuándo saltar:** Al proyecto le faltan datos para rellenar las secciones (A) a (G). El usuario quiere una landing de marketing, no un caso de estudio (usa `/ux-design`).
- **Invocación:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Salida:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Encadena con:** Comando terminal, normalmente el final de un proyecto.

### Conductor

#### `/ux-next`: conductor de flujo de trabajo (solo lectura)

- **Qué:** Lee cada `.ux/last-*.json` y nombra el siguiente comando de mayor apalancamiento. Un conductor, no un constructor. Solo lectura.
- **Cuándo usar:** Entre comandos. «¿Qué debería hacer ahora?», «¿cuál es el siguiente movimiento?», «decide por mí», «¿hacia dónde vamos desde aquí?».
- **Cuándo saltar:** No hay informes previos en `.ux/`. Tienes un siguiente comando específico en mente.
- **Invocación:** `/ux-next` (sin argumentos) o `/ux-next --focus=a11y`.
- **Salida:** Stdout, comando recomendado siguiente + justificación.
- **Encadena con:** Cualquier comando que elija.

#### `/ux-expert`: gancho de consultoría

- **Qué:** Aflora la información de contacto del creador del plugin cuando un usuario pide un experto de UX real. Breve, directo, sin marketing.
- **Cuándo usar:** «¿Quién construyó esto?», «necesito un experto en UX», «¿haces consultoría?», «¿puedo contratar a alguien para esto?», «¿hay un humano detrás de este plugin?».
- **Cuándo saltar:** El usuario pregunta por features del plugin, no por consultoría.
- **Invocación:** `/ux-expert`.
- **Salida:** Tarjeta breve de contacto con LinkedIn / email / repo.

### Alias, retirados en 4.1

Siete comandos de 3.x se fusionaron en los 18 de arriba. Sus nombres siguen funcionando durante una versión: cada alias indica adónde se movió y luego ejecuta el nuevo comando con los mismos argumentos.

| Comando antiguo | Ahora | Notas |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | El mismo bloque de framing, el mismo `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | La herramienta MCP `ux_recommend` no cambia |
| `/ux-stats` | `/ux-init --stats` | Snapshot de solo lectura |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | El alias mantiene el antiguo tope de cinco vueltas; `/ux-polish` solo se detiene en tres |
| `/ux-component` | `/ux-design --component` | El mismo `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | El mismo `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Quita `--extract-only` para construir a partir de la imagen |

### Grafo de encadenamiento de comandos

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

## Los 5 sub-agentes

Los sub-agentes son generadores específicos por rol despachados por comandos. Nunca se ejecutan de forma independiente: los llaman `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Cada agente tiene un ámbito de responsabilidad definido: NO decide el brief; lo ejecuta.

### `frontend-engineer`

- **Posee:** Código frontend de calidad de producción (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) con disciplina anti-slop de IA.
- **Despachado por:** `/ux-design` (modos de página, componente, dashboard e imagen), `/ux-fix`.
- **Entradas:** Brief + dirección creativa + tokens (de `.ux/last-recommendation.json`).
- **Salidas:** Código funcional distinguible del output genérico de IA. Sin gradientes morados, sin hero centrado, sin tres tarjetas iguales, sin Inter en tamaño display, sin «John Doe», sin emoji, sin defaults de 300 ms.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Posee:** El movimiento en código frontend de producción, Framer Motion, GSAP, animaciones CSS. Duraciones, easings, coreografía, fallbacks de movimiento reducido, disciplina de rendimiento.
- **Despachado por:** `/ux-design` (todos los modos), `/ux-motion --fix`.
- **Entradas:** Brief de movimiento + tokens + los 57 presets de movimiento de `data/motion-presets.json`.
- **Salidas:** Movimiento que se gana su lugar. Siempre envuelto en fallbacks `prefers-reduced-motion`. Siempre probado contra Core Web Vitals.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Posee:** Las cadenas que se envían, mensajes de error, empty states, CTAs, loading states, mensajes de éxito, toasts, texto auxiliar, etiquetas de formulario, texto de botones.
- **Despachado por:** `/ux-copy --fix`, `/ux-design` (todos los modos), `/ux-discover --frame`.
- **Entradas:** Perfil de voz (nombrado o pegado) + las cadenas de la superficie.
- **Salidas:** Microcopy de producción aplicado consistentemente a cada estado de una superficie para que el producto suene como un producto, no como diez. Prohibido: «el formulario contiene errores», «John Doe», copy celebratorio cantarín de IA, CTAs genéricos, empty states muertos.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Posee:** Digerir entradas de investigación (entrevistas, analítica, sitios competidores, resultados de A/B, tickets de soporte) en recomendaciones de diseño accionables.
- **Despachado por:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Entradas:** Investigación cruda, transcripciones, exports, URLs de competidores, clusters de soporte.
- **Salidas:** Temas, evidencia, recomendaciones. Nunca diseña la respuesta, le da al diseñador el sustrato desde el que diseñar.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Posee:** Sistemas de diseño completos, tokens (color, tipografía, espacio, movimiento, radio, sombra), documentos de fundamentos, contratos de componentes, emparejamientos de modo oscuro, capa de theming.
- **Despachado por:** `/ux-system`, `/ux-design --component` cuando no existe ningún sistema.
- **Entradas:** Brief de marca + `.ux/last-recommendation.json` (estilo + paleta + par tipográfico + presets de movimiento).
- **Salidas:** Un sistema coherente, opinado, listo para producción contra el que los agentes posteriores puedan construir sin volver a decidir los fundamentos. Tokens JSON, fundamentos MD, contratos de componentes, mapeo de modo oscuro.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocolo de despacho de sub-agentes

Cuando un comando despacha un sub-agente, le pasa:

1. El brief / recomendación (cargado desde `.ux/`).
2. La porción de manifiesto relevante (p. ej., `frontend-engineer` recibe el estilo + paleta + componentes elegidos; `motion-engineer` recibe los presets de movimiento elegidos).
3. Las 171 barreras de antipatrones (siempre activas).
4. Un criterio de éxito (qué debe hacer el artefacto).

Los sub-agentes devuelven:

1. El artefacto (código, doc, sistema).
2. Un bloque de justificación (por qué estas elecciones).
3. Una auto-comprobación contra las barreras (qué reglas verificaron).

El comando que llama ejecuta entonces `/ux-lint` automáticamente antes de declarar terminado.

---

## Los 11 manifiestos de datos

La capa de datos es el cerebro. Cada comando lee de ella; el motor fusiona a través de ella; el linter escanea contra ella. Todos los archivos viven bajo `data/` y envuelven sus entradas en `{_meta, entries}` para versionado de esquema.

### `styles.json`: 84 estilos de diseño

| Campo | Descripción |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalista / Suizo, Brutalista, Editorial, Glassmorfismo, Neumorfismo, Bento, Skeumórfico, Industrial, Maximalista, IA-Futurista, MENA-moderno, Vaporwave, etc. |
| `sample entry` | `swiss-international`, «La cuadrícula es ley. La tipografía hace el trabajo pesado. La decoración es fracaso.» |

Usado por: `/ux-discover`, `/ux-system`, `/ux-design`. Esquema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 paletas de color

| Campo | Descripción |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (claro/oscuro), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | cálido, editorial, magazine, clínico, juguetón, brutalista, monocromo, joya, MENA-cálido, dev-tools-oscuro, etc. |
| `sample entry` | `claude-warm-editorial`, claro, cálido/editorial/magazine, canvas #faf9f5, primary #cc785c |

Usado por: `/ux-discover`, `/ux-system`. Contraste verificado en AA / AAA. Esquema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 emparejamientos tipográficos

| Campo | Descripción |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Todas las familias tienen licencia + URL de origen. Usado por `/ux-discover`, `/ux-system`.

### `components.json`: 148 componentes

| Campo | Descripción |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navegación, Formularios, Visualización de datos, Feedback, Overlays, Layout, Contenido, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navegación, Cuadrícula de Producto, anatomía de 6 partes, 4 estados |

Este es nuestro mayor moat. Ningún otro plugin de UX para Claude distribuye un manifiesto estructurado de componentes.

### `industries.json`: 184 reglas sectoriales

| Campo | Descripción |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Servicios Financieros, Salud, Educación, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Viajes, Inmobiliaria, Específico MENA, etc. |
| `sample entry` | `fintech-neobank`, alta confianza, disclosures regulatorios, UI primario de balance/transacción, mobile-first de uso diario |

Usado por el recomendador (`/ux-discover`) como primer eje de búsqueda en paralelo.

### `chart-types.json`: 35 tipos de gráfico

| Campo | Descripción |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparación, Series Temporales, Distribución, Composición, Relación, Flujo, Geográfico |
| `sample entry` | `bar-vertical`, compara de 4 a 15 categorías discretas. La posición en el eje x representa la categoría; la altura, el valor. |

Usado por `/ux-design --dashboard` y `/ux-design --component` (instancias de gráfico).

### `tech-stacks.json`: 25 stacks

| Campo | Descripción |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | producción, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, compatible con Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Otros stacks incluyen Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 leyes de UX con nombre

| Campo | Descripción |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Coste de Decisión, Atención, Memoria, Control Motor, Percepción Visual, Social, Emocional, Formularios, Manejo de Errores, Onboarding, Empty State, etc. |
| `sample entry` | `hicks-law`, El tiempo de decisión crece logarítmicamente con el número de opciones presentadas |

Usado por `/ux-audit` (puntuación de 6 lentes) y `/ux-critique` (ancla de gusto).

### `motion-presets.json`: 57 presets de movimiento

| Campo | Descripción |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback de movimiento reducido), `when_to_use` |
| `categories` | Entrada, Salida, Hover, Focus, Tap, Loading, Empty, Success, Error, Anclado a scroll |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Cada preset tiene una variante de movimiento reducido. Código listo por stack para Framer Motion, GSAP y CSS puro.

### `anti-patterns.json`: 171 reglas

| Campo | Descripción |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (tipo, patrón, flags, ámbito y, en muchas reglas, una comprobación `post` sobre el archivo analizado), `why`, `fix` |
| `categories` | A11y (45), Contenido (35), Layout (18), Tipografía (16), Movimiento (14), Visual (14), Calidad (12), Color (10), Performance (5), Profundidad (2) |

La lista completa de reglas está en [Las 171 reglas anti-slop de IA](#las-171-reglas-anti-slop-de-ia-el-linter).

### `brands/*.json`: 160 specs de marca

| Campo | Descripción |
|---|---|
| `entries` | 160 (más `_index.json` que las lista todas) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotriz (8) |

Lista completa en [Las 160 especificaciones DESIGN.md de marca](#las-160-especificaciones-designmd-de-marca-por-categoría).

---

## Las 171 reglas anti-slop de IA: el linter

ux-skill incluye un linter determinista: cada regla es un patrón, y muchas añaden una comprobación sobre el CSS y el marcado analizados, de modo que una coincidencia solo cuenta en el contexto que nombra. **Sin LLM.** **Sin API.** **Sin red.** Se ejecuta en CI en ~200 ms en una app Next.js típica. Sale con código no-cero ante hallazgos Critical / High cuando se define `--fail-on high`.

Las reglas salen de `data/anti-patterns.json` (v2, preferido) con `references/foundations/anti-patterns.md` como respaldo (v1, bash). Se distribuyen dos binarios: `bin/ux-lint.py` (Python, rápido, extensible) y `bin/ux-lint.sh` (Bash + perl-PCRE, para entornos sin Python).

### Reglas por categoría

El catálogo completo de las 171 reglas, por categoría y luego por severidad, se genera a partir de `data/anti-patterns.json` en el [README en inglés](README.md#rules-by-category); allí los identificadores y nombres de las reglas aparecen tal como los imprime el linter. Las reglas cubren A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### Uso del linter

**Escaneo puntual:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## Las 160 especificaciones DESIGN.md de marca: por categoría

Marcas reales. Lenguajes de diseño reales. Especificaciones DESIGN.md reales, no paletas genéricas. Le dices al plugin «construye una landing al estilo de Stripe» y lee el vocabulario de marca real: rúbrica de voz, tokens de color, convenciones de movimiento, signature moves, anti-moves.

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

Los otros 8 plugins populares de UX para Claude generan «minimal moderno» o «dashboard limpio», variantes de la misma estética por defecto. ux-skill te permite pedir **la claridad de Linear**, **la seriedad de Stripe**, **la moderación de Apple**, **el monolito de Tesla**, **la cercanía de Notion**, **la disciplina de gradientes de Cursor**, **la densidad de pelo de Raycast**, **el editorial cálido de Claude**, y el motor saca los tokens, voz, convenciones de movimiento y signature moves correctos del brand spec.

---

## Servidor MCP: el movimiento asimétrico

ux-skill distribuye un **servidor Model Context Protocol**. Ejecutas `ux-mcp` y el motor se convierte en un proceso stdio de larga duración al que cualquier host compatible con MCP (Claude Desktop, Cursor, Windsurf, agentes genéricos) puede llamar. 25 herramientas: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Los mismos handlers de Python que usan los comandos slash; los mismos manifiestos de datos; el mismo recomendador determinista.

**Por qué este es el movimiento asimétrico:** ninguna de las ocho mejores skills de UX para Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) distribuye un servidor MCP. Están encerradas dentro del runtime de plugins de Claude Code. ux-skill es accesible desde cualquier host que hable MCP, incluidos agentes que nunca han oído hablar de un plugin de Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Apunta tu cliente al binario `ux-mcp`. La documentación completa de herramientas, ejemplos JSON y configuración por cliente para Claude Desktop, Cursor y Windsurf vive en [docs/mcp.html](docs/mcp.html) y en `commands/ux-mcp.md`.

---

## El instalador para 17 IDEs

`uxskill init` (o `/ux-init` dentro de Claude Code) auto-detecta qué IDE usas y escribe el artefacto correcto. El mismo motor de Python. Las mismas recomendaciones. Diferente pegamento por IDE.

| IDE / Tool | Señal de detección | Artefacto instalado |
|---|---|---|
| Claude Code | `.claude/` o `CLAUDE.md` | Manifiesto del plugin en `.claude-plugin/plugin.json` + los 18 comandos (y 7 alias) + los 5 sub-agentes |
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

## Casos de uso: escenarios concretos

Ocho escenarios reales. Elige el más cercano a tu situación y adapta la invocación.

### 1. Construir un dashboard fintech en Cursor

Estás en Cursor trabajando en un dashboard de un neobanco MENA. Instalas el plugin y ejecutas discovery, recomendación y luego generación del dashboard.

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

Luego en Cursor, pides: *«Genera la superficie del dashboard usando la recomendación en .ux/last-recommendation.json»*. Cursor lee la cabecera `.cursorrules`, carga la recomendación, despacha una generación de dashboard con restricciones explícitas.

### 2. Generar una landing al estilo de Stripe en Claude Code

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Tres comandos, una superficie pulida, commits atómicos por arreglo.

### 5. Diseñar un command palette al estilo Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

El componente generado usa los tokens de color reales de Linear, su stack tipográfico, sus convenciones de movimiento y densidades de pelo, no «UI oscura genérica».

### 6. Correr un taller de design thinking de 90 minutos con stakeholders

Tienes una sala con 5 personas durante 90 minutos. Quieres que salgan con un plan de juego, no con un vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

El plugin facilita las cinco fases (exploración → mapa de calor → mapa de actores → boceto de solución → plan de juego) de extremo a extremo, cronometradas, con artefactos concretos por fase. La salida es `.ux/last-workshop.json`, el plan de juego, no solo «hallazgos interesantes».

### 7. Escribir un caso de estudio publicable tras el lanzamiento

Enviaste la billetera de fidelización. Quieres una pieza de portafolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

El caso de estudio es un artefacto acabado y publicable, no un borrador. Monocromo puro, tipografía editorial, listo para enviar a tu portafolio.

### 8. Correr discovery en un contexto no-IA (solo intake estructurado)

Estás acotando un proyecto. Aún no necesitas una recomendación, necesitas un brief estructurado.

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

Puedes entregar el JSON a tu equipo, pegarlo en un doc de Notion o meterlo en una herramienta de IA aparte. ux-skill también es una herramienta de intake estructurado, además de ser un motor.

### 9. Persistencia con MASTER.md: tus decisiones de diseño, en el repositorio

Tras `/ux-discover` (o `/ux-discover --recommend`), guarda el estilo + paleta + tipografía + movimiento + componentes + marcas ejemplares + barreras elegidos como un archivo Markdown legible que tu equipo pueda revisar, comparar (diff) y versionar.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Escribe `.ux/design-system/MASTER.md` (YAML frontmatter + cuerpo) y `.ux/design-system/pages/<name>.md` por cada superficie generada vía `persist save-page`. Idempotente, la misma entrada produce salida byte a byte idéntica, así que re-ejecutarlo sobre estado no cambiado es un no-op en git.

---

## Frente a las alternativas

Tabla resumen corta. La comparativa completa lado a lado está en [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensión | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Comandos slash | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Componentes | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Presets de movimiento | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specs de marca | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Reglas de antipatrones | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter determinista apto para CI | **sí** | no | no | no | no | no | no | no | no |
| IDEs soportados | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Puerta de discovery | **10 campos** | implícita | implícita | implícita | implícita | implícita | implícita | implícita | implícita |
| Cadena de estado `.ux/` | **sí** | no | no | no | no | no | no | no | no |
| Estrellas (2026-05-28) | 14 | 83 958 | 54 406 | 25 202 | 15 455 | 5 762 | 2 391 | 2 164 | 955 |

### Evaluación honesta

- **ui-ux-pro-max** es más grande en notoriedad, distribuye 18 IDEs, tiene búsqueda estilo BM25 sobre su CSV. No distribuye manifiesto de componentes, manifiesto de movimiento, biblioteca de marcas ni linter determinista.
- **open-design** tiene 19 skills + preview pero solo soporte para Claude Code y sin capa anti-slop.
- **hallmark** es lo más cercano en espíritu (también anti-slop) pero es una única skill, sin motor, sin manifiestos, sin comandos encadenados.
- **material-3-skill** es excelente si específicamente quieres Material Design 3. No competimos en MD3.

Para detalle completo por dimensión, ver [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Hoja de ruta

A continuación, sin versión fija:

- **Estilos de Figma**: estilos de efecto para sombras, estilos de cuadrícula y estilos de texto enlazados a las variables de campo, escritos en un archivo en vivo.
- **Mapeo de componentes**: un componente de Figma y sus variantes vinculados a un componente de código y sus props, conservados durante el traspaso.
- **Un importador de sitios en vivo**: leer el sistema que un sitio publicado renderiza realmente, junto a los importadores de archivos.
- **Páginas de documentación para un sistema construido**: la vista humana de sus tokens, roles y contratos.

También abiertos:

- **`uxskill lint --fix` para reescrituras seguras** de hallazgos corregibles mecánicamente (button-no-type, img-no-alt con cadena vacía, eliminación de console-log-leak).
- **Extensión de VS Code** que muestra los hallazgos del lint en línea.
- **Emisión de código por componente** en seis stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Marketplace de especificaciones de marca**: publicar y descubrir especificaciones de marca de la comunidad.
- **Reglas de antipatrones personalizadas**: descubrimiento y uso compartido de las reglas que los proyectos definen en `data/anti-patterns.local.json`.
- **`uxskill plan`**: planificación de sitios de varias páginas a partir de un brief, no solo de una superficie.

---

## Cómo contribuir

Issues y PRs bienvenidos. Tres áreas de alto apalancamiento:

### Añadir una regla de antipatrón

1. Edita `data/anti-patterns.json`, añade una entrada con `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Añade un test en `tests/linter/`, un archivo que dispara la regla, uno que no.
3. Ejecuta `uxskill lint tests/linter/should-trigger/<rule>.tsx`, confirma que se dispara. Ejecuta sobre `tests/linter/should-not-trigger/<rule>.tsx`, confirma que no.
4. Abre una PR.

### Añadir un brand spec

1. Crea `data/brands/<slug>.json` con `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Añade la prosa correspondiente en `references/brands/<slug>.md`.
3. Regístralo en `data/brands/_index.json`.
4. Abre una PR. La spec debe estar respaldada por referencias de fuente primaria (el producto real de la marca, su sistema de diseño público o su DESIGN.md si lo publican).

### Añadir un preset de movimiento

1. Edita `data/motion-presets.json`, añade una entrada con `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. El preset debe tener una variante de movimiento reducido. Sin excepciones.
3. Abre una PR.

### Proceso

- Lee [CONTRIBUTING.md](CONTRIBUTING.md) para el proceso completo.
- Lee [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Las nuevas reglas y brand specs se revisan buscando: anclaje en fuente primaria, ausencia de overfitting a un único proyecto, ausencia de emoji en cualquier dato, comportamiento seguro en RTL cuando aplique.

---

## Licencia, autor, agradecimientos

### Licencia

MIT. Úsalo, fórkalo, construye sobre él. Si te ahorra enviar slop de IA, ponle una estrella al repo, es la forma más barata de apoyarlo.

### Autor

**Laith Aljunaidy**: fundador en solitario de [Dot](https://thedotwallet.com), una plataforma de fidelización MENA-first. Construyendo ux-skill para que el frontend generado por IA deje de parecerse todo.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Sitio: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Agradecimientos

- Al equipo de Anthropic por Claude Code y la arquitectura de skill / plugin que hizo posible distribuir esto.
- A Nielsen Norman Group, Laws of UX (lawsofux.com) y la comunidad de investigación de UX cuyo trabajo informa `data/ux-guidelines.json`.
- A cada marca listada en `data/brands/`, sus sistemas de diseño públicos son la fuente de verdad de los brand specs.
- A los contribuidores originales de v1: una skill de Claude de un solo disparo que se convirtió en la semilla del motor Python de v2.
- A los 8 plugins populares de UX para Claude con los que nos comparamos, subieron el listón; esta es nuestra respuesta.

---

**ux-skill** · **v4.0.0** · Construido para que Claude Code, Cursor, Windsurf y todas las demás herramientas de codificación con IA produzcan frontend que no se lea como generado por IA.

> Pon una estrella al repo en [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Instala vía `pip install uxskill` o `npx uxskill init` · Explora la comparativa en [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
