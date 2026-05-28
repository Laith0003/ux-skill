[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · **Português** · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — o motor de inteligência de design para Claude Code, Cursor e qualquer outra ferramenta de coding com IA

> **O plugin de UX mais forte para coding com IA.** Um núcleo de raciocínio em Python com 11 manifests JSON consultáveis (84 estilos, 176 paletas, 70 pareamentos tipográficos, 148 componentes, 184 indústrias, 35 tipos de gráfico, 57 presets de motion, 112 leis de UX, 100 regras de anti-pattern, 25 stacks técnicas, 110 specs de marca), 22 comandos slash, 5 sub-agents e um linter determinístico anti-AI-slop. Multi-IDE: distribui para Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer e Roo Cline.

> **O nome da marca é `ux-skill`.** O nome do pacote no PyPI / npm continua `uxskill`. O repositório do GitHub fica em [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Site:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Comparativo contra todo plugin de UX para Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-2.0.0--alpha.1-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#o-instalador-para-17-ides)
[![Brands](https://img.shields.io/badge/brand_specs-131-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-100-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Histórico de estrelas

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## O que é o ux-skill

O ux-skill é um **motor de inteligência de design** para ferramentas de coding com IA. Roda como pacote Python (`pip install uxskill`), como plugin do Claude Code e como multi-instalador para 17 IDEs. O motor ingere um brief de projeto (indústria, audiência, tom, must-haves, jogadas proibidas, stack, região) e devolve um sistema de design recomendado completo: estilo, paleta, par tipográfico, presets de motion, componentes, marcas exemplares para estudar e os guardrails de anti-pattern que precisam ser respeitados. A recomendação é determinística — a mesma entrada sempre produz a mesma saída.

O plugin fica entre você e a ferramenta de coding com IA. Quando você pede ao Claude Code, Cursor ou qualquer outro assistente de IA para «construir uma landing page fintech», o assistente normalmente improvisa — e o resultado é reconhecido como gerado por IA em cinco segundos (gradientes roxo-azul, três cards iguais, Inter em tamanho de display, «John Doe» nos depoimentos, transições padrão de 300ms, hero centralizado, setas saltitantes nos CTAs). O ux-skill substitui a improvisação por **restrições estruturadas**: você executa `/ux-discover` para capturar o brief, `/ux-recommend` para escolher o sistema, `/ux-design` para gerar o código e `/ux-lint` para verificar que ele passa nas 100 regras determinísticas anti-AI-slop antes do commit.

Este README é a referência canônica. Cada comando, cada sub-agent, cada manifest de dados, cada caminho de instalação, cada spec de marca, cada categoria de anti-pattern — está tudo documentado aqui. Se você está procurando um plugin de design para Claude Code ou comparando ferramentas de design com IA para Cursor, Windsurf ou Codex, leia do começo ao fim junto com [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Sumário

1. [Instalação rápida](#instalação-rápida)
2. [Os números — comparativo ao vivo contra as 8 melhores skills de UX do Claude](#os-números--comparativo-ao-vivo-contra-as-8-melhores-skills-de-ux-do-claude)
3. [Arquitetura — como as peças se encaixam](#arquitetura--como-as-peças-se-encaixam)
4. [Os 22 comandos slash — referência detalhada](#os-22-comandos-slash--referência-detalhada)
5. [Os 5 sub-agents](#os-5-sub-agents)
6. [Os 11 manifests de dados](#os-11-manifests-de-dados)
7. [As 100 regras anti-AI-slop — o linter](#as-100-regras-anti-ai-slop--o-linter)
8. [As 110 specs de marca DESIGN.md — por categoria](#as-110-specs-de-marca-designmd--por-categoria)
9. [Servidor MCP — a jogada assimétrica](#servidor-mcp--a-jogada-assimétrica)
10. [O instalador para 17 IDEs](#o-instalador-para-17-ides)
11. [Casos de uso — cenários concretos](#casos-de-uso--cenários-concretos)
12. [Comparado às alternativas](#comparado-às-alternativas)
13. [Roadmap](#roadmap)
14. [Como contribuir](#como-contribuir)
15. [Licença, autor, agradecimentos](#licença-autor-agradecimentos)

---

## Instalação rápida

Três caminhos de instalação. Escolha o que se encaixa no seu ambiente.

### Caminho 1 — marketplace do Claude Code (canônico)

Se você vive no Claude Code, instale via o marketplace de plugins:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Isso conecta todos os 22 comandos slash e os 5 sub-agents na sua sessão do Claude Code. Após a instalação, execute `/ux-init` para configurar o diretório de estado `.ux/` por projeto e verificar que o motor Python está acessível.

### Caminho 2 — pip (universal)

Se você vive fora do Claude Code (Cursor, Windsurf, CLI, CI), instale o pacote Python:

```bash
pip install uxskill
uxskill init                       # detecta automaticamente seu IDE, instala o artefato certo
uxskill stats                      # imprime contagens de manifests para verificar a instalação
uxskill lint .                     # roda o linter contra o diretório atual
```

O pacote expõe tanto `ux` quanto `uxskill` como entry points de CLI — são o mesmo binário.

### Caminho 3 — npx (sem precisar de Python)

Se você não quer gerenciar Python diretamente, o wrapper npx faz o bootstrap de tudo via `pipx`:

```bash
npx uxskill init                  # baixa pipx + uxskill na primeira execução
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verificar a instalação

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

Se alguma contagem retornar 0, o arquivo JSON está faltando — abra uma issue em [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Os números — comparativo ao vivo contra as 8 melhores skills de UX do Claude

As contagens de estrelas foram verificadas pela última vez via `gh api` em **2026-05-28**. O ux-skill (Laith0003/ux-skill) é o recém-chegado — somos pequenos em awareness, profundos em arquitetura. A comparação abaixo é honesta: onde a gente perde, onde a gente ganha.

| Plugin | Estrelas | Arquitetura | Comandos slash | Linter (CI-safe) | Specs de marca | Componentes | Presets de motion | IDEs suportados |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, skill única | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skills + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + taste embasada em pesquisa | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | SKILL.md único de 62 KB + scripts | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Biblioteca de skills conectada por MCP | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill de uma única estética | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill de design anti-slop | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Componentes MD3 + auditoria | 1 | — | (somente MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Motor Python + 11 manifests + 22 comandos + 5 sub-agents + linter de CI** | **22** | **100 regras regex** | **110** | **148** | **57** | **17** |

### Onde a gente perde

- **Awareness.** Eles têm centenas de milhares de estrelas. A gente tem 14. Dá uma estrela — é o jeito mais barato de ajudar.
- **Reconhecimento de marca.** ui-ux-pro-max e open-design têm vantagem medida em meses, não em dias.
- **Acabamento de marketing.** Eles têm screenshots, vídeos de demo e uma landing achável. A gente tem um README minucioso e uma landing magrinha.

### Onde a gente ganha

- **Biblioteca de componentes:** 148 componentes documentados com anatomia, estados, tokens usados e especificações de motion. Nenhum dos outros 8 distribui um manifest de componentes.
- **Presets de motion:** 57 entradas prontas para o stack (Framer Motion, GSAP, CSS) com fallbacks de reduced-motion. Nenhum dos outros distribui um manifest de motion.
- **Linter de anti-pattern:** 100 regras regex determinísticas, roda em CI, sai com código não-zero em Critical/High. Nenhum dos outros distribui um linter determinístico.
- **Specs de marca:** 110 specs DESIGN.md reais (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude e mais 96). Nenhum dos outros distribui uma biblioteca de marca.
- **17 IDEs suportados:** mesmo motor, cola diferente por IDE.
- **22 comandos slash:** discovery, geração, auditoria, lint, polish, fix loop, case-study, workshop, copy, motion, a11y, dashboard, conductor — totalmente integrados.

Comparativo completo tabela por tabela em [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Arquitetura — como as peças se encaixam

```
ux-skill (nome do pacote: uxskill)
│
├── data/                              O cérebro — manifests JSON consultáveis
│   ├── styles.json                    84 estilos de design + when/skip + tokens
│   ├── palettes.json                  176 paletas (light/dark, contraste verificado)
│   ├── type-pairs.json                70 trincas display × body × mono
│   ├── components.json                148 componentes (anatomia, estados, motion)
│   ├── industries.json                184 regras de indústria + sinais de audiência
│   ├── chart-types.json               35 tipos de gráfico (when/skip, encoding)
│   ├── tech-stacks.json               25 stacks (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 leis de UX nomeadas (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 presets de motion (entry, exit, hover...)
│   ├── anti-patterns.json             100 regras regex (fonte do linter CI-safe)
│   └── brands/*.json                  110 specs DESIGN de marca + _index.json
│
├── engine/                            Python — o raciocínio
│   ├── recommender/                   motor de merge com 5 buscas paralelas
│   ├── linter/                        scanner anti-slop determinístico
│   ├── discovery/                     protocolo forçante de 10 campos
│   ├── generator/                     emissor de tokens + manifest
│   ├── installer/                     multi-instalador para 17 IDEs
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          22 comandos slash do Claude Code (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    snapshot de inventário
│   ├── ux-discover.md                 intake de 10 campos (gate)
│   ├── ux-recommend.md                FLAGSHIP — busca em 5 paralelas
│   ├── ux-lint.md                     linter determinístico
│   ├── ux-design.md                   gerar código frontend
│   ├── ux-component.md                gerar um componente
│   ├── ux-system.md                   gerar sistema de design completo
│   ├── ux-dashboard.md                gerar superfície de dashboard
│   ├── ux-motion.md                   tratamento + auditoria de motion
│   ├── ux-audit.md                    auditoria de design em 6 lentes
│   ├── ux-a11y.md                     auditoria WCAG 2.1 AA
│   ├── ux-critique.md                 crítica de taste (3 acertos, 3 erros, 1 jogada)
│   ├── ux-copy.md                     revisão + reescrita de microcopy
│   ├── ux-fix.md                      aplicar achados como commits atômicos
│   ├── ux-polish.md                   passada cosmética + matar AI-slop
│   ├── ux-frame.md                    bloco de framing de 4 campos
│   ├── ux-research.md                 planejamento de pesquisa + síntese
│   ├── ux-workshop.md                 workshop de design thinking em 5 fases
│   ├── ux-case-study.md               case study publicável estilo editorial Wfrah
│   ├── ux-next.md                     condutor de workflow (read-only)
│   └── ux-expert.md                   hook de consultoria
│
├── agents/                            5 sub-agents (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy na voz da marca
│   ├── research-synthesizer.md        entrevistas + analytics + concorrentes
│   └── design-system-architect.md     tokens / componentes / foundations
│
├── references/                        Fontes em prosa para os dados + páginas demo
│   ├── foundations/                   anti-patterns.md, princípios, taste
│   ├── laws/                          leis de UX em formato longo
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        prosa por estilo (anti-slop.md, etc.)
│   ├── components/                    componentes em formato longo
│   ├── output/                        rubricas de output
│   └── conditional/                   guia específica por stack
│
├── bin/
│   ├── uxskill.mjs                    wrapper npx -> motor Python
│   ├── ux-lint.py                     linter v2 (preferido)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (criado por projeto)
    ├── last-discovery.json            snapshot do brief
    ├── last-recommendation.json       sistema escolhido
    ├── last-frame.json                bloco de framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Como o motor realmente funciona

1. **Input.** Você fornece um brief — de forma interativa via `/ux-discover` (10 campos) ou não-interativa via flags para `ux recommend`.
2. **5 buscas paralelas.** O motor executa cinco lookups concorrentemente pelos manifests:
   - **Indústria → recommended_styles** (industries.json)
   - **Estilo → compatibilidade paleta + tipo + motion** (styles.json)
   - **Tom × must-have → filtro de paleta** (palettes.json)
   - **Stack → compatibilidade componentes + presets de motion** (tech-stacks.json, motion-presets.json)
   - **Forbidden + região → guardrails + shortlist de marcas exemplares** (anti-patterns.json, brands/)
3. **Merge.** Um merger determinístico ranqueia candidatos, resolve conflitos (ex: must-have de dark-mode força o modo da paleta) e emite um único sistema recomendado.
4. **Output.** Um documento JSON com o estilo escolhido, paleta, par tipográfico, top 5 presets de motion, top 12 componentes, top 5 marcas exemplares e todos os 100 guardrails de anti-pattern ativos. Mais um bloco de racional explicando cada escolha.
5. **Geração.** Comandos a jusante (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) consomem a recomendação para gerar código real via os sub-agents.
6. **Verificação.** `/ux-lint` re-escaneia o código gerado contra as 100 regras regex. Sai com código não-zero em Critical/High no CI.

**Python pensa. HTML mostra. Markdown encadeia.**

---

## Os 22 comandos slash — referência detalhada

Cada comando é distribuído como arquivo `.md` em `commands/` com `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` e `output state file`. As descrições abaixo estão condensadas; o source completo é a spec canônica.

Os comandos estão agrupados em cinco baldes: **bootstrap & inventário**, **discovery & recomendação**, **geração**, **auditoria & verificação**, **fix & polish** e **conductor**.

### Bootstrap & inventário

#### `/ux-init` — bootstrap do projeto

- **O que faz:** Detecta qual IDE você está usando (`.claude/`, `.cursor/`, `.windsurf/`, etc.), instala o artefato certo, verifica que o motor Python está acessível, imprime um snapshot de estatísticas.
- **Quando usar:** Primeira instalação em um projeto novo. Após clonar um projeto que usa ux-skill. Após `pip install --upgrade uxskill`.
- **Quando pular:** Você já rodou nesse projeto e nada mudou.
- **Invocação:** `/ux-init` (sem argumentos) ou `uxskill init` pelo CLI.
- **Output:** Artefato por IDE (veja [O instalador para 17 IDEs](#o-instalador-para-17-ides)) + diretório `.ux/` + resumo no stdout.
- **Encadeia para:** `/ux-discover` em seguida.

#### `/ux-stats` — imprime o inventário de dados

- **O que faz:** Imprime versão + contagens de entradas para os 11 manifests de dados, para você verificar o que está instalado.
- **Quando usar:** Após instalação. Após upgrade. Quando `/ux-recommend` retorna escolhas surpreendentes e você suspeita que os manifests estão incompletos.
- **Quando pular:** Nunca — é um comando read-only de 50ms.
- **Invocação:** `/ux-stats` ou `uxskill stats`.
- **Output:** JSON no stdout (veja [Verificar a instalação](#verificar-a-instalação) acima).
- **Encadeia para:** Apenas diagnóstico; não alimenta a jusante.

### Discovery & recomendação

#### `/ux-discover` — a função forçante (intake de 10 campos)

- **O que faz:** O intake obrigatório de 10 campos por que todo projeto passa antes de qualquer comando de geração. Tipo de projeto, audiência, objetivo primário, tom, must-haves, forbidden, marcas de referência, stack, região, métrica de sucesso. **Sem improvisação.** Frases proibidas («moderno», «clean») obrigam o usuário a ser específico.
- **Quando usar:** Antes de qualquer `/ux-design`, `/ux-component`, `/ux-system` ou `/ux-dashboard`. Sempre que um brief anterior tiver envelhecido.
- **Quando pular:** Você está corrigindo um bug (`/ux-fix`). Você só está rodando uma passada de linter (`/ux-lint`). O brief não mudou desde a última sessão.
- **Invocação:** `/ux-discover`. O plugin pergunta; você responde.
- **Output:** Escreve `.ux/last-discovery.json` (o brief de 10 campos).
- **Encadeia para:** `/ux-recommend` → usa a discovery para escolher estilo + paleta + tipo + motion + componentes. `/ux-design [brief extra]` → gera código frontend ancorado na recomendação. `/ux-component <nome>` → gera um componente alinhado às restrições descobertas.

#### `/ux-recommend` — o motor flagship de 5 buscas paralelas

- **O que faz:** Roda a busca em 5 paralelas do motor Python pelos 11 manifests e retorna um sistema de design mesclado. Indústria → Estilo → Paleta → Tipografia → Motion + Componentes + Marcas exemplares + Guardrails.
- **Quando usar:** Iniciando um novo projeto do zero. Fazendo pivot em um produto desgastado. Pre-flight antes de qualquer `/ux-design` ou `/ux-component`.
- **Quando pular:** Você já rodou `/ux-discover` e salvou um brief — `/ux-recommend` é automático nesse fluxo. Você está corrigindo um bug (use `/ux-fix`). Você só precisa fazer lint (use `/ux-lint`).
- **Invocação (Claude Code):**
  ```
  /ux-recommend
  ```
  **Invocação (CLI):**
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
- **Output:** Escreve `.ux/last-recommendation.json` — estilo escolhido, paleta escolhida, par tipográfico escolhido, top 5 presets de motion, top 12 componentes, top 5 marcas exemplares, todos os 100 guardrails de anti-pattern ativos, mais o racional.
- **Encadeia para:** `/ux-design [brief]` → código frontend usando os tokens recomendados. `/ux-system` → sistema de design completo a partir da recomendação. `/ux-component <nome>` → um componente usando o estilo recomendado. `/ux-lint` → verifica o código gerado.

### Geração

#### `/ux-design` — gera uma superfície bonita e anti-slop a partir de um brief

- **O que faz:** Gera um artefato frontend completo, de nível produção (landing, site de marketing, app shell) a partir do brief de discovery + recomendação. Despacha `frontend-engineer` com direção criativa de anti-slop e referências de arsenal.
- **Quando usar:** «Desenhe uma», «me constrói uma», «gere uma landing page», «cria um dashboard», «faz um componente» — qualquer pedido de entrega visual livre.
- **Quando pular:** Você quer uma revisão, não uma build (use `/ux-audit` ou `/ux-critique`). Você quer um componente só (use `/ux-component`). Trabalho de backend ou infraestrutura.
- **Invocação:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Output:** Código gerado (HTML / Blade / JSX / Vue / Astro), mais `.ux/last-design.json`.
- **Encadeia para:** `/ux-lint` → verifica contra os guardrails. `/ux-polish` → passada cosmética. `/ux-a11y` → auditoria de acessibilidade. `/ux-copy` → revisão de microcopy. `/ux-fix` → aplica achados como commits atômicos.

#### `/ux-component` — gera um componente

- **O que faz:** Produz um único componente de nível produção (button, modal, navbar, sidebar, card, table, form, chart) a partir de uma spec. Todos os quatro estados de interação, acessível, on-brand. Procura o componente em `.ux/last-recommendation.json` primeiro, recua para query direta no manifest.
- **Quando usar:** Qualquer pedido de elemento único — «constrói um botão», «cria um card de preço», «faz um modal», «adiciona uma navbar», «desenha uma sidebar», «preciso de uma tabela de dados», «constrói um form», «faz um componente de gráfico».
- **Quando pular:** Página inteira ou superfície multi-seção (use `/ux-design`). Backend ou infraestrutura.
- **Invocação:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Output:** Código do componente gerado, mais `.ux/last-component.json`.
- **Encadeia para:** `/ux-lint` → verifica. `/ux-polish` → aperta.

#### `/ux-system` — gera um sistema de design starter completo

- **O que faz:** Propõe um sistema de design starter completo para um projeto que não tem um — tokens (cor, tipo, espaço, motion, raio, sombra), docs de foundation, contratos de componentes, pareamentos dark-mode, theme switcher. Despacha `design-system-architect`.
- **Quando usar:** «A gente não tem um sistema de design», «constrói um sistema pra gente», «propõe os tokens», «qual deve ser nosso tema», «configura nosso DS».
- **Quando pular:** O projeto já tem um sistema de design — use `/ux-component` contra o sistema existente. Backend ou infraestrutura.
- **Invocação:** `/ux-system` (roda discovery primeiro se ainda não tiver).
- **Output:** `tokens.json`, `foundations.md`, contratos `components/*.md`, emit opcional Tailwind / vanilla / SCSS. Escreve `.ux/last-system.json` para contexto de encadeamento.
- **Encadeia para:** `/ux-component` → constrói contra o novo sistema. `/ux-design` → gera uma superfície usando os novos tokens.

#### `/ux-dashboard` — geração especializada de dashboard

- **O que faz:** Dashboard com disciplina de densidade de dados — layout bento, numerais monoespaçados tabulares, padrões de sparkline, anti-superuso de cards, cores de estado semânticas, motion econômico. Não é site de marketing com gráficos colados.
- **Quando usar:** «Constrói um dashboard», «desenha o painel admin», «faz uma página de métricas», «console de operador», «vista de analytics», «painel de KPI», «tela de monitoramento».
- **Quando pular:** Landing de marketing com estatísticas (use `/ux-design`). Um widget só (use `/ux-component`). Backend ou infraestrutura.
- **Invocação:** `/ux-dashboard`.
- **Output:** Código de dashboard gerado + `.ux/last-dashboard.json`.
- **Encadeia para:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — tratamento de motion

- **O que faz:** Gera a camada de motion de uma superfície — durações, easings, coreografia, fallbacks de reduced-motion, disciplina de performance. Também audita motion existente contra as 5 dimensões (timing, easing, significado, reduced-motion, performance).
- **Quando usar:** «Verifica o motion», «as animações estão boas», «conserta o motion», «revisa as animações», «auditoria de motion», «passada de performance no motion».
- **Quando pular:** Superfície não tem motion (use `/ux-audit` ou `/ux-polish`). Backend ou infraestrutura.
- **Invocação:** `/ux-motion path/to/component.tsx` (modo auditoria) ou `/ux-motion --generate hero-entry` (geração).
- **Output:** Código atualizado (em modo geração) ou relatório `.ux/last-motion.json` (em modo auditoria).
- **Encadeia para:** `/ux-fix` → aplica achados de motion. `/ux-polish` → aperta.

### Auditoria & verificação

#### `/ux-lint` — linter determinístico baseado em regex (sem LLM, CI-safe)

- **O que faz:** Roda 100 regras regex contra seu código. Sem chamada LLM. Sai com código não-zero em Critical / High no CI. Fonte: `data/anti-patterns.json`. As regras cobrem A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4).
- **Quando usar:** Hook de pre-commit. Gate de CI. Primeira passada rápida em uma codebase grande antes de pagar o custo de `/ux-audit`. Após `/ux-design` ou `/ux-component` para verificar geração.
- **Quando pular:** Você quer um fix loop (o linter reporta, não edita — encadeia em `/ux-polish --fix` ou `/ux-fix`). Você quer julgamento de taste (use `/ux-critique`).
- **Invocação (slash):** `/ux-lint src/`.
- **Invocação (CLI):** `uxskill lint .` ou `python3 bin/ux-lint.py .` ou `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocação (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Achados no stdout (localização, id da regra, severidade, evidência). Código de saída 0 se limpo, não-zero em Critical/High quando `--fail-on high` está setado.
- **Encadeia para:** `/ux-polish --fix` → contraparte LLM-driven nos mesmos padrões. `/ux-fix` → aplica achados como commits, ordenados por severidade. `/ux-audit` → passada completa de raciocínio em 6 lentes. `/ux-next` → deixa o conductor decidir.

#### `/ux-audit` — auditoria de design em 6 lentes

- **O que faz:** Uma revisão estruturada e opinada contra seis lentes (clareza, hierarquia, acessibilidade, voz, motion, taste), produzindo achados marcados por severidade. Relatório estilo Polaris. Lê `.ux/last-frame.json` primeiro — audiência e outcome ancoram a severidade de cada achado.
- **Quando usar:** Superfície existe e você quer uma crítica defensável. «Audita», «revisa o ux», «isso tá bom», «o que tá quebrado», «destrói isso».
- **Quando pular:** Superfície ainda não existe (use `/ux-design`). Usuário quer uma lente (use o comando focado: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Usuário quer opinião de taste (use `/ux-critique`). Backend ou infraestrutura.
- **Invocação:** `/ux-audit https://example.com/pricing` ou `/ux-audit src/components/Pricing.tsx`.
- **Output:** Escreve `.ux/last-audit.json` — array `findings` de `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Encadeia para:** `/ux-fix` → aplica achados. `/ux-polish` → passada cosmética. `/ux-design` → se um redesign estrutural for necessário.

#### `/ux-a11y` — auditoria WCAG 2.1 AA + checagens de cortesia comum

- **O que faz:** Uma auditoria estruturada WCAG 2.1 AA, mais as checagens de cortesia comum que passam pelas ferramentas automatizadas mas ainda machucam usuários reais (visibilidade de foco, especificidade de erro, preferências de motion, armadilhas de teclado, dependência de cor).
- **Quando usar:** Gate de acessibilidade pré-release. Após um redesign. «Verifica acessibilidade», «auditoria WCAG», «isso é acessível», «revisão a11y», «teste de screen reader», «verifica navegação por teclado».
- **Quando pular:** Não voltado para usuário. Backend ou infraestrutura. Esboços work-in-progress.
- **Invocação:** `/ux-a11y https://example.com` (URL live preferido — ferramentas automatizadas e teste de teclado só funcionam ao vivo).
- **Output:** Escreve `.ux/last-a11y.json` — array `findings` de `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Encadeia para:** `/ux-fix` → aplica achados como commits. `/ux-copy` → corrige alt text e wiring de erro de form como parte de uma passada de copy.

#### `/ux-critique` — chamada de taste (3 acertos, 3 erros, 1 jogada estratégica)

- **O que faz:** A opinião de um designer — não uma auditoria estruturada, não uma nota de severidade, só um take apertado e opinado que nomeia o que está funcionando, o que não está e a jogada estratégica que mudaria o máximo.
- **Quando usar:** «O que você acha», «isso tá bom», «critica isso», «opinião honesta», «a vibe tá certa», «parece a gente», «devemos lançar».
- **Quando pular:** Usuário quer explicitamente uma auditoria estruturada (use `/ux-audit`). Backend ou infraestrutura.
- **Invocação:** `/ux-critique https://example.com`.
- **Output:** Escreve `.ux/last-critique.json` — 3 acertos, 3 erros, 1 jogada estratégica, mais a prosa.
- **Encadeia para:** `/ux-design` se o take recomenda redesign. `/ux-polish` se o take recomenda apertar.

#### `/ux-copy` — revisão + reescrita de microcopy

- **O que faz:** Avalia cada string visível contra a rubrica de voz e produz uma reescrita before/after. Pega: «form contains errors» (genérico), «John Doe» (placeholder), copy AI-animada celebrativa, CTAs genéricas, empty states mortos, erros inúteis.
- **Quando usar:** Estrutura está certa mas as palavras estão fracas. «Revisa a copy», «conserta a microcopy», «as mensagens de erro estão ruins», «reescreve isso», «aperta as strings», «os botões soam genéricos», «esse empty state tá morto».
- **Quando pular:** Problemas de layout (use `/ux-audit` ou `/ux-polish`). Problemas de copy dirigidos por acessibilidade como alt text (use `/ux-a11y`). Backend ou infraestrutura.
- **Invocação:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Escreve `.ux/last-copy.json` — array `strings` de `{location, severity, before, after, notes}`, mais rubrica + locais que precisam de tradução.
- **Encadeia para:** `/ux-fix` → aplica reescritas. `/ux-a11y` → re-verifica após correções de copy.

### Fix & polish

#### `/ux-fix` — aplica achados como commits atômicos

- **O que faz:** Lê o último relatório de `.ux/` (audit, copy, a11y, motion ou polish), valida a working tree e aplica os achados como commits atômicos via os sub-agents certos. Re-verifica rodando o comando de origem.
- **Quando usar:** Após executar um comando da classe auditoria e revisar os achados. «Conserta os achados», «aplica as correções», «roda o fix loop», «aplica patch na superfície», «faz as mudanças», «vai consertar».
- **Quando pular:** Nenhum relatório anterior em `.ux/`. Working tree está suja e o usuário não concordou com stash/commit. Correções precisam de julgamento de design, não aplicação mecânica (use `/ux-design` para redesign).
- **Invocação:** `/ux-fix` (detecta automaticamente qual relatório consertar) ou `/ux-fix --from=last-a11y.json`.
- **Output:** Commits atômicos por achado. Re-roda o comando de origem e atualiza o arquivo `.ux/last-*.json`. Imprime um resumo.
- **Encadeia para:** `/ux-next` → conductor escolhe a próxima jogada.

#### `/ux-polish` — passada cosmética + matar AI-slop

- **O que faz:** Ritmo de espaçamento, afiação de hierarquia, detecção de AI-slop, consistência de tokens. A contraparte LLM-driven de `/ux-lint` — usa seu julgamento nas chamadas de taste.
- **Quando usar:** Estrutura está certa mas a execução está frouxa. «Polir», «aperta isso», «remove o AI-slop», «deixa premium», «faz isso parecer menos AI», «o espaçamento está estranho», «isso parece genérico», «precisa de mais taste».
- **Quando pular:** Superfície está faltando funcionalidade core (conserta isso primeiro). Precisa de redesign, não polish (use `/ux-design`). Problemas de copy (use `/ux-copy`). Problemas de motion (use `/ux-motion`). Problemas de a11y (use `/ux-a11y`).
- **Invocação:** `/ux-polish src/components/Hero.tsx`.
- **Output:** Código atualizado + `/.ux/last-polish.json` descrevendo as mudanças.
- **Encadeia para:** `/ux-lint` → verifica que o polish se manteve. `/ux-a11y` → re-verifica acessibilidade.

### Discovery & narrativa

#### `/ux-frame` — bloco de framing de 4 campos

- **O que faz:** Captura para-quem-é, outcome, hipótese e sinal de sucesso em um bloco de framing estruturado. Sem trabalho de design — apenas o intake de quatro campos que transforma um pedido vago em um brief funcional. Mais leve que `/ux-discover` (4 campos vs 10).
- **Quando usar:** Início de qualquer projeto, sprint ou engajamento avulso. No meio do caminho quando uma conversa se desviou. «Enquadra isso», «qual é o brief», «configura o projeto», «framing».
- **Quando pular:** Já enquadrado (confira `.ux/last-frame.json`). Build de componente avulso sem implicações de framing. Backend ou infraestrutura.
- **Invocação:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Output:** Escreve `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Encadeia para:** `/ux-discover` → estende o frame para o brief de 10 campos. `/ux-design` → gera usando o frame como âncora.

#### `/ux-research` — planejamento de pesquisa + síntese

- **O que faz:** Modo planejamento: escreve roteiros de entrevista, surveys, screeners de recrutamento. Modo síntese (`--synthesize`): digere entrevistas, analytics, sites de concorrentes, resultados A/B, tickets de suporte em recomendações. Despacha `research-synthesizer`.
- **Quando usar:** «Planeja um estudo de pesquisa», «preciso de perguntas de entrevista», «desenha um survey», «como recruto usuários», «plano de user testing», «diary study», «teste de preferência», «fake door», «smoke test», «sintetiza minhas notas de entrevista».
- **Quando pular:** Resposta já é conhecida com alta confiança. Decisões reversíveis de baixo risco. Backend ou infraestrutura.
- **Invocação:** `/ux-research --plan "loyalty wallet adoption in MENA"` ou `/ux-research --synthesize interviews/*.md`.
- **Output:** Escreve `.ux/last-research.json` — plano de pesquisa ou temas sintetizados + evidências + recomendações.
- **Encadeia para:** `/ux-frame` → integra achados em um frame. `/ux-design` → gera a partir dos achados. `/ux-workshop` → roda um workshop usando a pesquisa como input.

#### `/ux-workshop` — workshop de design thinking em 5 fases

- **O que faz:** Facilita um workshop de discovery / design thinking end-to-end. Cinco fases sequenciais (exploração → heat map → mapa de stakeholders → solução em esboço → game plan). Cronometrado. Artefatos concretos por fase. Termina com uma decisão, não «achados interessantes».
- **Quando usar:** Pergunta real, participantes reais, orçamento de tempo real. «Roda um workshop», «facilita uma discovery», «vamos fazer uma sessão de design thinking», «tenho stakeholders por uma hora, o que fazemos», «começa o projeto».
- **Quando pular:** Brief já está claro e escopado. Brainstorm solo (use `/ux-design` ou `/ux-frame`). Time no meio da execução, não em discovery.
- **Invocação:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Escreve `.ux/last-workshop.json` — game plan + artefatos por fase.
- **Encadeia para:** `/ux-design` → executa o game plan. `/ux-research` → preenche lacunas que o workshop surfou. `/ux-case-study` → publica a jornada.

#### `/ux-case-study` — case study publicável (formato editorial Wfrah)

- **O que faz:** Gera um case study de projeto em formato editorial monocromático puro — tipografia Wfrah, separadores hairline, códigos de seção numerados (A)–(G), layout bilíngue-safe. Um documento, não um folheto de marketing. Lê de `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Quando usar:** Pós-lançamento. Após um marco discreto. «Escreve um case study», «case study desse projeto», «faz o documento de fechamento», «publica esse trabalho», «peça de portfólio».
- **Quando pular:** Projeto carece de dados para popular as seções (A)–(G). Usuário quer uma landing de marketing, não um case study (use `/ux-design`).
- **Invocação:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Encadeia para:** Comando terminal — geralmente o fim de um projeto.

### Conductor

#### `/ux-next` — condutor de workflow (read-only)

- **O que faz:** Lê cada `.ux/last-*.json` e nomeia o próximo comando de maior alavancagem. Um condutor, não um construtor. Read-only.
- **Quando usar:** Entre comandos. «O que devo fazer em seguida», «qual é a próxima jogada», «decide por mim», «pra onde vamos daqui».
- **Quando pular:** Nenhum relatório anterior em `.ux/`. Você tem um próximo comando específico em mente.
- **Invocação:** `/ux-next` (sem argumentos) ou `/ux-next --focus=a11y`.
- **Output:** Stdout — próximo comando recomendado + racional.
- **Encadeia para:** Seja qual for o comando escolhido.

#### `/ux-expert` — hook de consultoria

- **O que faz:** Surface a informação de contato do criador do plugin quando um usuário pede por um especialista de UX da vida real. Breve, direto, sem marketing.
- **Quando usar:** «Quem construiu isso», «preciso de um especialista de UX», «vocês fazem consultoria», «posso contratar alguém pra isso», «tem um humano por trás desse plugin».
- **Quando pular:** Usuário está perguntando sobre features do plugin, não sobre consultoria.
- **Invocação:** `/ux-expert`.
- **Output:** Cartão de contato breve com LinkedIn / email / repo.

### Grafo de encadeamento de comandos

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  bloco de framing de 4 campos
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  intake de 10 campos (FORCING GATE)
                  └────────────┬─────────┘
                               │ escreve .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 buscas paralelas -> sistema mesclado
                  └────────────┬─────────┘
                               │ escreve .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ escreve .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ escreve .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  aplica achados como commits
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artefato publicável
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — read-only
                  │  /ux-expert          │  hook de consultoria
                  └──────────────────────┘
```

---

## Os 5 sub-agents

Sub-agents são geradores específicos de papel despachados por comandos. Eles nunca rodam de forma independente — são chamados por `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Cada agent tem uma fronteira de propriedade definida: eles NÃO decidem o brief; eles executam contra ele.

### `frontend-engineer`

- **Possui:** Código frontend de nível produção (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) com disciplina anti-AI-slop.
- **Despachado por:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Inputs:** Brief + direção criativa + tokens (de `.ux/last-recommendation.json`).
- **Outputs:** Código funcionando que se distingue do output genérico de IA. Sem gradientes roxos, sem hero centralizado, sem três cards iguais, sem Inter em tamanho de display, sem «John Doe», sem emoji, sem defaults de 300ms.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Possui:** Motion em código frontend de produção — Framer Motion, GSAP, animações CSS. Durações, easings, coreografia, fallbacks de reduced-motion, disciplina de performance.
- **Despachado por:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Inputs:** Brief de motion + tokens + os 57 presets de motion de `data/motion-presets.json`.
- **Outputs:** Motion que merece seu lugar. Sempre envolto em fallbacks de `prefers-reduced-motion`. Sempre testado contra Core Web Vitals.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Possui:** As strings que vão pro ar — mensagens de erro, empty states, CTAs, estados de loading, mensagens de sucesso, toasts, texto auxiliar, labels de form, texto de botão.
- **Despachado por:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Inputs:** Perfil de voz (nomeado ou colado) + as strings da superfície.
- **Outputs:** Microcopy de produção aplicada consistentemente em cada estado de uma superfície para que o produto soe como um produto, não dez. Proibidos: «form contains errors», «John Doe», copy AI-animada celebrativa, CTAs genéricas, empty states mortos.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Possui:** Digerir inputs de pesquisa (entrevistas, analytics, sites competitivos, resultados A/B, tickets de suporte) em recomendações de design acionáveis.
- **Despachado por:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Inputs:** Pesquisa bruta — transcrições, exports, URLs de concorrentes, clusters de suporte.
- **Outputs:** Temas, evidências, recomendações. Nunca desenha a resposta — dá ao designer o substrato a partir do qual desenhar.
- **Ferramentas:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Possui:** Sistemas de design completos — tokens (cor, tipo, espaço, motion, raio, sombra), docs de foundation, contratos de componentes, pareamentos dark-mode, camada de theming.
- **Despachado por:** `/ux-system`, `/ux-component` quando não existe sistema.
- **Inputs:** Brief de marca + `.ux/last-recommendation.json` (estilo + paleta + par tipográfico + presets de motion).
- **Outputs:** Um sistema coerente, opinado e pronto pra produção sobre o qual os agents a jusante podem construir sem ter que re-decidir fundamentos. Tokens JSON, foundations MD, contratos de componentes, mapeamento dark-mode.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocolo de despacho de sub-agents

Quando um comando despacha um sub-agent, ele passa:

1. O brief / recomendação (carregados de `.ux/`).
2. A fatia de manifest relevante (ex: `frontend-engineer` recebe o estilo + paleta + componentes escolhidos; `motion-engineer` recebe os presets de motion escolhidos).
3. Os 100 guardrails de anti-pattern (sempre ativos).
4. Um critério de sucesso (o que o artefato precisa fazer).

Sub-agents retornam:

1. O artefato (código, doc, sistema).
2. Um bloco de racional (por que essas escolhas).
3. Um self-check contra os guardrails (quais regras eles verificaram).

O comando que chama então roda `/ux-lint` automaticamente antes de declarar pronto.

---

## Os 11 manifests de dados

A camada de dados é o cérebro. Cada comando lê dela; o motor mescla através dela; o linter escaneia contra ela. Todos os arquivos vivem em `data/` e envolvem suas entradas em `{_meta, entries}` para versionamento de schema.

### `styles.json` — 84 estilos de design

| Campo | Descrição |
|---|---|
| `entries` | 84 |
| `chaves por entrada` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categorias` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, etc. |
| `entrada de exemplo` | `swiss-international` — «O grid é lei. A tipografia faz o trabalho pesado. Decoração é falha.» |

Usado por: `/ux-recommend`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 paletas de cor

| Campo | Descrição |
|---|---|
| `entries` | 176 |
| `chaves por entrada` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tons` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, etc. |
| `entrada de exemplo` | `claude-warm-editorial` — light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Usado por: `/ux-recommend`, `/ux-system`. Contraste verificado em AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 pareamentos tipográficos

| Campo | Descrição |
|---|---|
| `entries` | 70 |
| `chaves por entrada` | `id`, `name`, `display` (family + pesos + fonte + licença + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `entrada de exemplo` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Todas as families têm licença + URL fonte. Usado por `/ux-recommend`, `/ux-system`.

### `components.json` — 148 componentes

| Campo | Descrição |
|---|---|
| `entries` | 148 |
| `chaves por entrada` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categorias` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `entrada de exemplo` | `mega-nav-product-grid` — Mega Navigation, Product Grid — anatomia de 6 partes, 4 estados |

Esse é nosso maior fosso. Nenhum outro plugin de UX para Claude distribui um manifest estruturado de componentes.

### `industries.json` — 184 regras de indústria

| Campo | Descrição |
|---|---|
| `entries` | 184 |
| `chaves por entrada` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categorias` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, etc. |
| `entrada de exemplo` | `fintech-neobank` — alta confiança, divulgações regulatórias, UI primária de saldo/transação, mobile-first uso diário |

Usado por `/ux-recommend` como primeiro eixo de busca paralela.

### `chart-types.json` — 35 tipos de gráfico

| Campo | Descrição |
|---|---|
| `entries` | 35 |
| `chaves por entrada` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categorias` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `entrada de exemplo` | `bar-vertical` — Compara 4–15 categorias discretas. Posição no eixo x mapeia categoria; altura mapeia valor. |

Usado por `/ux-dashboard`, `/ux-component` (instâncias de gráfico).

### `tech-stacks.json` — 25 stacks

| Campo | Descrição |
|---|---|
| `entries` | 25 |
| `chaves por entrada` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `entrada de exemplo` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, compatível com Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Outras stacks incluem Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 leis de UX nomeadas

| Campo | Descrição |
|---|---|
| `entries` | 112 |
| `chaves por entrada` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categorias` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, etc. |
| `entrada de exemplo` | `hicks-law` — Tempo de decisão cresce logaritmicamente com o número de escolhas apresentadas |

Usado por `/ux-audit` (scoring de 6 lentes) e `/ux-critique` (âncora de taste).

### `motion-presets.json` — 57 presets de motion

| Campo | Descrição |
|---|---|
| `entries` | 57 |
| `chaves por entrada` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback de reduced-motion), `when_to_use` |
| `categorias` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `entrada de exemplo` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Cada preset tem uma variante reduced-motion. Código pronto pro stack para Framer Motion, GSAP e CSS puro.

### `anti-patterns.json` — 100 regras regex

| Campo | Descrição |
|---|---|
| `entries` | 100 |
| `chaves por entrada` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categorias` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

A lista completa de regras está em [As 100 regras anti-AI-slop](#as-100-regras-anti-ai-slop--o-linter).

### `brands/*.json` — 110 specs de marca

| Campo | Descrição |
|---|---|
| `entries` | 110 (mais `_index.json` listando todas) |
| `chaves por entrada` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categorias` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Lista completa em [As 110 specs de marca DESIGN.md](#as-110-specs-de-marca-designmd--por-categoria).

---

## As 100 regras anti-AI-slop — o linter

O ux-skill distribui um linter determinístico baseado em regex. **Sem LLM.** **Sem API.** **Sem rede.** Roda em CI em ~200ms em um app Next.js típico. Sai com código não-zero em achados Critical / High quando `--fail-on high` está setado.

As regras vêm de `data/anti-patterns.json` (v2 preferido) com fallback `references/foundations/anti-patterns.md` (v1 bash). Dois binários são distribuídos: `bin/ux-lint.py` (Python, rápido, extensível) e `bin/ux-lint.sh` (Bash + perl-PCRE, para ambientes sem Python).

### Regras por categoria

#### Typography (3 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| high | `inter-as-display` | Inter usado como display font |
| medium | `hero-text-arbitrary-90px` | Tamanho de font de hero arbitrário |
| low | `font-system-only` | Stack de font de sistema sem typeface escolhido |

#### Color (6 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| high | `purple-to-blue-gradient` | Gradiente AI default roxo-pra-azul |
| high | `dark-text-on-dark-card` | Texto de baixo contraste em card |
| medium | `gradient-text-rainbow` | Texto em gradiente multi-stop |
| medium | `card-glow-purple-shadow` | Sombra de glow roxo em cards |
| medium | `gradient-mesh-purple-pink` | Hero com gradient mesh roxo-rosa |
| low | `tailwind-color-named-vague` | Cores Tailwind nomeadas sem token semântico |

#### Layout (5 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| high | `three-equal-card-grid` | Três cards iguais em fila |
| medium | `centered-everything-hero` | Composição de hero centralizada |
| medium | `avatar-stack-overlapping` | Stack genérico de avatares sobrepostos |
| low | `pill-rounded-full-everywhere` | `rounded-full` aplicado em tudo |
| low | `nav-equal-hamburger-desktop` | Menu hamburger no desktop |

#### Content (5 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum em código que vai pra produção |
| high | `emoji-in-ui` | Emoji usado como elemento de UI |
| high | `icon-emoji-stamp` | Emoji usado como carimbo de ícone |
| high | `testimonial-fake-five-stars` | Depoimento de cinco estrelas hardcoded |
| medium | `fake-name-john-doe` | Nomes placeholder genéricos |

#### Motion (3 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Seta saltitante em CTA |
| low | `timing-300ms-default` | Timing default de transição de 300ms |
| low | `cubic-bezier-material-only` | Easing default Material em tudo |

#### A11y (6 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| high | `inline-svg-no-aria` | SVG sem aria-label ou aria-hidden |
| high | `img-no-alt` | Imagem sem atributo alt |
| high | `link-onclick-no-href` | Anchor com onClick mas sem href |
| medium | `button-no-type` | Button sem atributo type |
| medium | `heading-skip-h1-h3` | Nível de heading pulado |
| medium | `infinite-scroll-no-pagination` | Scroll infinito sem fallback de teclado |

#### Quality (6 regras)

| Severidade | ID da regra | Nome |
|---|---|---|
| high | `console-log-leak` | `console.log` em código de componente |
| medium | `inline-style-attribute` | Atributo style inline |
| medium | `any-type-leak` | Tipo `any` do TypeScript |
| medium | `arbitrary-z-index-9999` | Valor de z-index preguiçoso |
| low | `shadcn-default-everywhere` | Bloco de tokens default do shadcn sem modificação |
| low | `todo-fixme-comment` | TODO ou FIXME em código que vai pra produção |

#### Visual (1 regra)

| Severidade | ID da regra | Nome |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur sem superfície glass |

### Uso do linter

**Scan avulso:**

```bash
uxskill lint .
# ou
python3 bin/ux-lint.py src/
# ou
bash bin/ux-lint.sh src/
```

**Gate de CI (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Hook de pre-commit:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Output (amostra):**

```
─── relatório /ux-lint ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidência: bg-gradient-to-br from-purple-500 to-blue-500
  fix: troca pelo gradiente primário da paleta recomendada ou remove o gradiente

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  evidência: grid grid-cols-3 gap-6 (3 filhos Card iguais)
  fix: destaca um card; flanqueia com dois cards de ênfase reduzida

3 arquivos escaneados · 2 high · 0 medium · 0 low · exit 1
Próximo recomendado: /ux-polish --fix (LLM-driven, lida com achados lintáveis e estéticos)
```

---

## As 110 specs de marca DESIGN.md — por categoria

Marcas reais. Linguagens de design reais. Specs DESIGN.md reais — não paletas genéricas. Diz pro plugin «constrói uma landing no estilo da Stripe» e ele lê o vocabulário real da marca: rubrica de voz, tokens de cor, convenções de motion, jogadas de assinatura, jogadas proibidas.

Cada marca é distribuída como JSON estruturado (`data/brands/<slug>.json`) mais uma referência em prosa (`references/brands/<slug>.md`).

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

### Por que isso importa

Os outros 8 plugins de UX populares para Claude geram «modern minimal» ou «clean dashboard» — variantes da mesma estética default. O ux-skill permite que você peça **a clareza da Linear**, **a seriedade da Stripe**, **a contenção da Apple**, **o monólito da Tesla**, **a simpatia da Notion**, **a disciplina de gradiente do Cursor**, **a densidade hairline do Raycast**, **o editorial caloroso da Claude** — e o motor puxa os tokens certos, voz, convenções de motion e jogadas de assinatura da spec da marca.

---

## Servidor MCP — a jogada assimétrica

O ux-skill distribui um **servidor Model Context Protocol**. Rode `ux-mcp` e o motor vira um processo stdio long-running que qualquer host MCP-capaz — Claude Desktop, Cursor, Windsurf, agents genéricos — pode chamar. Catorze ferramentas: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Os mesmos handlers Python que os comandos slash usam; os mesmos manifests de dados; o mesmo recommender determinístico.

**Por que essa é a jogada assimétrica:** nenhuma das oito principais skills de UX para Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) distribui um servidor MCP. Elas estão trancadas dentro do runtime de plugins do Claude Code. O ux-skill é alcançável de qualquer host que fale MCP, incluindo agents que nunca ouviram falar de um plugin do Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp é um extra opt-in
ux-mcp                                  # servidor stdio JSON-RPC inicia
```

Aponta seu client para o binário `ux-mcp`. Documentação completa de ferramentas, exemplos JSON e configuração por client para Claude Desktop, Cursor e Windsurf vivem em [docs/mcp.html](docs/mcp.html) e em `commands/ux-mcp.md`.

---

## O instalador para 17 IDEs

`uxskill init` (ou `/ux-init` dentro do Claude Code) detecta automaticamente qual IDE você está usando e escreve o artefato certo. Mesmo motor Python. Mesmas recomendações. Cola diferente por IDE.

| IDE / Ferramenta | Sinal de detecção | Artefato instalado |
|---|---|---|
| Claude Code | `.claude/` ou `CLAUDE.md` | Manifest de plugin em `.claude-plugin/plugin.json` + todos os 22 comandos + todos os 5 sub-agents |
| Cursor | `.cursor/` ou `.cursorrules` | Header de prompt `.cursorrules` apontando pro motor |
| Windsurf | `.windsurf/` ou `.windsurfrules` | `.windsurfrules` com o mesmo header de prompt |
| GitHub Copilot | `.github/copilot-instructions.md` ou `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | patch em `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` ou `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

Em qualquer IDE, os mesmos comandos CLI `uxskill recommend` / `uxskill lint` / `uxskill stats` funcionam pelo terminal. O motor Python é a fonte da verdade; os artefatos de IDE são headers de prompt finos que roteiam pra ele.

---

## Casos de uso — cenários concretos

Oito cenários reais. Escolhe o mais próximo da sua situação e adapta a invocação.

### 1. Construindo um dashboard fintech no Cursor

Você está no Cursor trabalhando no dashboard de uma neobank MENA. Você instala o plugin e roda discovery, recomendação, depois geração de dashboard.

```bash
pip install uxskill
uxskill init                                # detecta Cursor, escreve .cursorrules
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

Depois no Cursor, peça: *«Gere a superfície de dashboard usando a recomendação em .ux/last-recommendation.json»*. O Cursor lê o header `.cursorrules`, carrega a recomendação, despacha uma geração de dashboard com restrições explícitas.

### 2. Gerando uma landing estilo Stripe no Claude Code

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Tipo de projeto? landing
> Indústria? fintech-payments
> Tom? serious, technical, confident
> Must have? dark-mode, AA, mobile-first
> Forbidden? purple-gradients, three-equal-cards
> Marcas de referência? stripe
> Stack? nextjs-15-app-router
> Região? global
> Métrica de sucesso? signup conversion

/ux-recommend
> [retorna estilo escolhido, paleta, par tipográfico, presets de motion, componentes, marcas exemplares]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer gera a página]

/ux-lint .
> [passa — a spec da marca Stripe foi respeitada]
```

### 3. Auditando código existente para AI slop no CI

Você lançou um app Next.js duas semanas atrás. Você quer um piso duro contra impressões digitais de IA em toda PR.

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

PRs que introduzem gradientes roxo-pra-azul, Inter em 96px, depoimentos «John Doe» ou emoji como ícones falham no CI. Sem custo de LLM. ~200ms.

### 4. Polindo uma superfície existente que «parece gerada por IA»

Você herdou um app React que parece todo outro site SaaS gerado por IA. Você quer fazer ele não parecer com isso.

```
/ux-critique src/components/Hero.tsx
> [3 acertos, 3 erros, 1 jogada estratégica — o take é honesto]

/ux-lint src/
> [15 impressões digitais AI de alta severidade sinalizadas]

/ux-polish src/components/Hero.tsx
> [passada cosmética LLM-driven + matar AI-slop]

/ux-fix
> [aplica achados como commits atômicos, re-roda o linter]
```

Três comandos, uma superfície polida, commits atômicos por correção.

### 5. Desenhando uma command palette estilo Linear

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [lê data/brands/linear.app.json para tokens + jogadas de assinatura]
> [lê data/components.json para a anatomia + estados da command-palette]
> [despacha frontend-engineer com spec Linear explícita]
```

O componente gerado usa os tokens de cor reais da Linear, stack de tipografia, convenções de motion, densidades hairline — não «UI dark genérica».

### 6. Conduzindo um workshop de design thinking de 90 minutos com stakeholders

Você tem uma sala com 5 pessoas por 90 minutos. Você quer que eles saiam com um game plan, não com uma vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

O plugin facilita as cinco fases (exploração → heat map → mapa de stakeholders → solução em esboço → game plan) end-to-end, cronometrado, com artefatos concretos por fase. O output é `.ux/last-workshop.json` — o game plan, não só «achados interessantes».

### 7. Escrevendo um case study publicável após o lançamento

Você lançou a loyalty wallet. Você quer uma peça pra portfólio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [lê .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [gera case study editorial Wfrah com seções numeradas (A)-(G), separadores hairline, layout bilíngue-safe]
> [escreve case-studies/bashiti-loyalty.html]
```

O case study é um artefato pronto e publicável — não um rascunho. Monocromia pura, tipografia editorial, pronto pra mandar pro seu portfólio.

### 8. Rodando discovery em contexto não-IA (só intake estruturado)

Você está escopando um projeto. Você não precisa de uma recomendação ainda — você precisa de um brief estruturado.

```bash
uxskill discover
# intake de 10 campos, salva em .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Você pode entregar o JSON pro seu time, colar num doc do Notion ou alimentar uma ferramenta de IA separada. O ux-skill também é uma ferramenta de intake estruturado além de ser um motor.

### 9. Persistência MASTER.md — suas decisões de design, no repo

Após `/ux-recommend`, persiste o estilo + paleta + tipografia + motion + componentes + marcas exemplares + guardrails escolhidos como arquivo Markdown legível por humano que seu time pode revisar, diferenciar e versionar.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Escreve `.ux/design-system/MASTER.md` (frontmatter YAML + corpo) e `.ux/design-system/pages/<nome>.md` por superfície gerada via `persist save-page`. Idempotente — o mesmo input produz output byte-idêntico, então re-rodar em estado inalterado é no-op no git.

---

## Comparado às alternativas

Tabela resumo curta. Comparação completa tabela por tabela em [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensão | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Comandos slash | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Componentes | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Presets de motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specs de marca | **110** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Regras de anti-pattern | **100** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter determinístico CI-safe | **sim** | não | não | não | não | não | não | não | não |
| IDEs suportados | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Gate de discovery | **10 campos** | implícito | implícito | implícito | implícito | implícito | implícito | implícito | implícito |
| Cadeia de estado `.ux/` | **sim** | não | não | não | não | não | não | não | não |
| Estrelas (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Avaliação honesta

- **ui-ux-pro-max** é maior em awareness, suporta 18 IDEs, tem busca estilo BM25 no CSV dele. Não distribui manifest de componentes, manifest de motion, biblioteca de marca ou linter determinístico.
- **open-design** tem 19 skills + preview mas só suporte Claude Code e nenhuma camada anti-slop.
- **hallmark** é o mais próximo em espírito (também anti-slop) mas é uma skill única — sem motor, sem manifests, sem comandos encadeados.
- **material-3-skill** é excelente se você quer especificamente Material Design 3. A gente não compete em MD3.

Para detalhe completo por dimensão, veja [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Completude do linter (Q3 2026)

- **+17 regras de anti-pattern adiadas** pra chegar a 52 totais. Alvos: estados hover dark-on-dark, codificação de estado só-por-cor, escalada de z-index redundante, breakpoints hardcoded em JS, opacity ao invés de estado disabled, etc.
- **`uxskill lint --fix` para reescritas seguras** de achados mecanicamente corrigíveis (button-no-type, img-no-alt empty-string, remoção de console-log-leak).
- **Extensão VS Code** que surface achados de lint inline (sem precisar rodar CI).

### v2.2 — Expansão do manifest de componentes (Q4 2026)

- **+50 componentes** pra chegar a 198 totais. Novos: combobox com filtro async, command-palette com heurística de recent-items, conditional-form-step, variantes de payment-element, date picker RTL-aware, phone input específico MENA, calendar grid com overlay hijri.
- **Emit de código por componente** em 6 stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Playground de componentes** em uxskill.laithjunaidy.com/playground — testa o motor de recomendação + vê preview ao vivo dos componentes.

### v3 — O marketplace + o lock-in (2027)

- **Marketplace de specs de marca** — publica e descobre specs de marca da comunidade. Pague-pra-publicar pra financiar moderação.
- **Regras de anti-pattern custom** — projetos podem definir suas próprias regras regex em `data/anti-patterns.local.json` (já lançado em v2; v3 adiciona discovery + compartilhamento).
- **`uxskill plan`** — planejamento completo de site multi-página a partir de um brief, não só uma superfície.
- **Paridade com plugin Figma** — o mesmo motor de recomendação, surfaceado no Figma.

---

## Como contribuir

Issues e PRs bem-vindas. Três áreas de alta alavancagem:

### Adicionar uma regra de anti-pattern

1. Edita `data/anti-patterns.json` — adiciona uma entrada com `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Adiciona um teste em `tests/linter/` — um arquivo que dispara a regra, um que não.
3. Roda `uxskill lint tests/linter/should-trigger/<rule>.tsx` — confirma que dispara. Roda em `tests/linter/should-not-trigger/<rule>.tsx` — confirma que não dispara.
4. Abre uma PR.

### Adicionar uma spec de marca

1. Cria `data/brands/<slug>.json` com `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Adiciona a prosa correspondente em `references/brands/<slug>.md`.
3. Registra em `data/brands/_index.json`.
4. Abre uma PR. A spec deve ser baseada em referências de fonte-primária (o produto real da marca, o sistema de design público, ou DESIGN.md se eles publicam um).

### Adicionar um preset de motion

1. Edita `data/motion-presets.json` — adiciona uma entrada com `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. O preset deve ter uma variante reduced-motion. Sem exceções.
3. Abre uma PR.

### Processo

- Leia [CONTRIBUTING.md](CONTRIBUTING.md) pra processo completo.
- Leia [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Novas regras e specs de marca são revisadas para: ancoragem em fonte-primária, sem overfit em projeto único, sem emoji em nenhum dos dados, comportamento RTL-safe onde aplicável.

---

## Licença, autor, agradecimentos

### Licença

MIT. Usa, faz fork, constrói em cima. Se te salva de mandar AI slop pra produção, dá uma estrela no repo — é o jeito mais barato de apoiar.

### Autor

**Laith Aljunaidy** — fundador solo de [Dot](https://thedotwallet.com), uma plataforma de loyalty MENA-first. Construindo o ux-skill pra que o frontend gerado por IA não pareça todo igual.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Agradecimentos

- O time da Anthropic pelo Claude Code e a arquitetura de skill / plugin que tornou isso distribuível.
- Nielsen Norman Group, Laws of UX (lawsofux.com) e a comunidade de pesquisa em UX cujo trabalho informa `data/ux-guidelines.json`.
- Cada marca listada em `data/brands/` — seus sistemas de design públicos são a fonte da verdade para as specs de marca.
- Os contribuidores originais da v1: uma skill Claude single-shot que virou semente para o motor Python v2.
- Os 8 plugins de UX populares para Claude com os quais a gente se comparou — eles elevaram o sarrafo; essa é nossa resposta.

---

**ux-skill** · **v2.0.0-alpha.1** · Construído pra que Claude Code, Cursor, Windsurf e qualquer outra ferramenta de coding com IA emitam frontend que não se lê como gerado por IA.

> Dá uma estrela no repo em [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Instala via `pip install uxskill` ou `npx uxskill init` · Navega o comparativo em [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
