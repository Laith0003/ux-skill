[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · **Português** · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: o motor de inteligência de design para Claude Code, Cursor e qualquer outra ferramenta de coding com IA

**Um motor de inteligência de design que deixa a UI gerada por IA marcante em vez de genérica.** Coloque em qualquer uma das 17 ferramentas de coding com IA e o que você entrega deixa de parecer feito por IA. Grátis, MIT, offline, sem LLM.

```bash
pip install uxskill
```

**[Dê uma estrela ao ux-skill no GitHub](https://github.com/Laith0003/ux-skill)** se ele for útil: é o jeito mais simples de ajudar o projeto. Chegou agora? Comece pelo [tour de 60 segundos](#instalação-rápida) ou veja ao vivo em [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![Antes: hero genérico com foto de banco de imagens, gradiente violeta suave, nenhuma identidade de marca. Depois: foto real de canteiro de obras sob um véu escuro, título editorial com um destaque âmbar e um formulário de orçamento dentro do hero. Mesmo prompt, resultado diferente quando o ux-skill fornece as restrições.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Antes: slop de SEO genérico com foto de banco de imagens. Depois: hero com foto real de obra sob um véu escuro, título editorial com destaque âmbar, formulário de orçamento no hero. Mesma ferramenta de coding com IA, mesmo prompt, resultado diferente quando o ux-skill fornece as restrições.*

> **v4.0, FOUNDATIONS: um único comando cria um design system completo, verificado pela WCAG, com árabe e escrita da direita para a esquerda já incluídos.** O plugin de UX mais forte para coding com IA. Um núcleo de raciocínio em Python com um sintetizador determinístico de 7 eixos, 12 manifests JSON consultáveis (84 estilos, 176 paletas, 70 pares tipográficos, 148 componentes, 184 setores, 35 tipos de gráfico, 57 presets de motion, 112 leis de UX, 171 regras de anti-pattern, 25 stacks de tecnologia, 160 specs de marca), 18 comandos slash, 5 sub-agents, 25 ferramentas MCP e um linter determinístico anti-AI-slop. Multi-IDE: instala no Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer e Roo Cline.

> **O nome da marca é `ux-skill`.** O nome do pacote no PyPI / npm continua `uxskill`. O repositório no GitHub fica em [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Autor:** [Laith Aljunaidy](https://laithjunaidy.com), designer e CTO em Amã · **Site:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Comparativo com cada plugin de UX para Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#o-instalador-para-17-ides)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Novo na 4.0: fundamentos

Entra uma cor da marca, sai um design system, com o contraste verificado antes de chegar a você.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 ou mais recente. Para o servidor MCP, `pip install --upgrade 'uxskill[mcp]'`. Com pipx, `pipx install uxskill` (sobre uma 3.x já instalada, `pipx upgrade uxskill`). Com npm, `npx uxskill@latest`. Vindo da 3.x? O [guia de migração](docs/migrating-to-4.md) associa cada token da 3.x ao seu papel na 4.0.

**Está criando um produto ou uma landing page?** Você recebe `tokens.css` para linkar na sua página, `fonts.css` com fallbacks de métricas ajustadas para as fontes escolhidas, `fonts-self-host.css`, que carrega as fontes a partir dos seus próprios arquivos, `tokens.json` para ferramentas, arte decorativa da marca em `art/` e `system-report.md`, que explica em palavras simples o que foi criado, por quê e com qual composição de página começar. Estilize com os papéis (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`) e alterne modo escuro, alto contraste, espaçamento compacto, direita para a esquerda ou movimento reduzido com um único atributo no `<html>`. Carregue as fontes pelo link do Google Fonts que o relatório indica, ou com `fonts-self-host.css` e uma pasta `fonts/`, e linke `fonts.css` em qualquer dos casos, antes de `tokens.css`; não edite nenhum dos dois arquivos. Com `--brief`, o visual segue o setor e o tom quando o briefing os cita, e campos estruturados (idade, idiomas, esquema padrão, contexto de leitura) definem tamanho do texto, áreas de toque, sistemas de escrita e qual esquema abre; o discovery não pergunta o setor, então o `/ux-system create` pergunta. No Claude Code, `/ux-system create` confere a versão instalada, roda a build e explica o relatório.

**Está desenhando um design system?** Nove fundamentos (cor, tipografia, espaçamento, layout, raio, borda, elevação, movimento, imagem), cada um variando de forma contínua com os sete eixos, com primitivas e papéis semânticos, no formato W3C design tokens (DTCG 2025.10) com os valores de cada modo. Mesmas entradas, mesmos bytes. Via MCP, `ux_system_build` devolve o relatório, o resultado da verificação e o tamanho de cada arquivo, e grava os mesmos arquivos que o comando quando recebe `out`.

- **Verificação WCAG.** Cada par de cores de texto, controle e foco é medido nos modos claro e escuro, em contraste padrão e alto: WCAG 1.4.3 (texto 4.5:1) e 1.4.11 (não textual 3:1) em contraste padrão, WCAG 1.4.6 (texto 7:1) em alto contraste, mais um piso próprio de 4.5:1 em alto contraste para a maioria das partes não textuais, já que a WCAG não define um nível aprimorado para o não textual. Um sistema que falha não é gravado; a mensagem diz o que mudar.
- **Seguro por padrão.** Nunca sobrescreve um arquivo diferente. `--force` substitui arquivos só quando você pede.
- **Árabe.** Com `dir="rtl"` o texto passa para uma fonte árabe com tamanhos e altura de linha próprios; o espaçamento usa propriedades lógicas e o movimento é espelhado. `--latin-only` deixa isso de fora.

**Um sistema que você já tem.** `/ux-system enhance --from` o lê com os nomes dele (tokens DTCG, propriedades customizadas de CSS, um tema Tailwind, arquivos de regras em markdown ou um export de variáveis do Figma), passa pela mesma verificação e mede o que o seu código realmente faz com ele; nada é reescrito. `/ux-system extend --from` adiciona fundamentos, papéis ou contratos sem mudar nenhum token existente, num arquivo de extensão ao lado, e `uxskill system export` o grava como tokens.css, tema Tailwind 4 ou variáveis do Figma. A 4.2 traz a camada de confiança (lint a cada gravação, um revisor de acabamento) e o lançamento. Veja o [changelog](CHANGELOG.md).

**Componentes e seções.** 23 contratos de componente dizem quais tokens cada parte de um controle usa em cada estado e como cada estado se move: uma mudança de estado faz a transição em `motion.state`, um toque escala em `motion.press.scale` (e fica parado com movimento reduzido), e abas, menus e controles segmentados deslizam um único indicador. 14 contratos de seção (hero, preços, FAQ, rodapé e as demais) definem a função de cada seção, os componentes que seus slots aceitam, a prova de que ela precisa e como ela empilha no celular. Páginas montadas com eles usam fotografias; fragmentos de interface são imagem extra, nunca substitutos.

**Um linter que lê a página.** 171 regras, muitas com uma verificação sobre o CSS e o markup já analisados, leem o próprio sistema da página: o movimento é cronometrado pela sua curva, a altura de linha dos títulos display respeita o piso do motor, e um controle oculto precisa sair da ordem de tabulação. `uxskill lint --render` abre cada página no Chromium headless em largura de desktop e de celular e a opera: anéis de foco que não aparecem ou ficam cortados, hover e toque que respondem com atraso, foco perdido depois do Esc e um toque que ainda se move com movimento reduzido.

**Menos comandos.** 25 comandos slash viram 18. `/ux-discover` aceita `--frame` e `--recommend`, `/ux-design` aceita `--component`, `--dashboard` e `--from-image`, `/ux-polish` repete lint, fix e re-lint até o score chegar a 90 ou passarem três rodadas, e `/ux-init` aceita `--stats`. Os sete nomes antigos continuam funcionando como aliases e saem na 4.1; veja [os aliases](#aliases-removidos-na-41).

**Playbooks de superfície.** As regras de landing, dashboard e componente ficam em `references/surfaces/`, um playbook para cada. `/ux-design` carrega exatamente um, escolhido pelo modo, então uma build de dashboard nunca lê regras de hero.

Testes: **9764 passando**. Offline. Determinístico. Nenhum LLM é chamado, nunca.

### Novo na v3.1: fiel à marca, responsivo, vivo

- **A fidelidade à marca é imposta, não esperada.** A cor primária é lida dos pixels do LOGO (não do CSS mais pintado); fontes padrão são rejeitadas em favor do estilo das letras do logo. A marca extraída viaja `recommend` -> `synthesize`, e um **piso rígido** em `evaluate` REPROVA qualquer saída que perca a cor ou o logo da marca ou não traga imagens reais. Interoperabilidade nos dois sentidos com a convenção aberta `brand.md` (render + importação).
- **Mobile-first, verificado.** Novos fundamentos de ofício (`responsive.md`, `component-behaviors.md`) mais uma verificação atenta a quebras de linha que falha com rolagem horizontal, um rótulo de nav, logotipo ou botão que quebra linha, ou um header sticky alto demais.
- **A camada uau.** O motor deriva 2-3 momentos de assinatura coordenados por página; a doutrina de que «o uau só pode vir do usuário» cai por terra.
- **Linter mais afiado** (152 regras): detecção de imagem obrigatória e de elementos só com ícone, regras de tokens de placeholder e de `100vw`; picsum com seed é mantido, o aleatório é removido.

Notas completas em [CHANGELOG.md](CHANGELOG.md).

### O que há de novo na v3

- **As brand specs viram dados de treinamento, não templates.** As 160 brand specs deixam de ser um catálogo do qual o recommender escolhe, passam a ser vocabulário que o sintetizador destila. A saída é nova a cada chamada.
- **Sintetizador de 7 eixos** (warmth, contrast, density, geometry, formality, motion, type_personality). O brief mapeia de forma determinística para valores de eixos; os valores de eixos compilam em palette + tipografia + spacing + radius + motion frescos.
- **Três modos auto-despachados**: `strict_brand` (100% de uma marca), `brand_anchor` (70% uma marca + 30% adaptado por eixos a partir de marcas-irmãs), `pure_synthesis` (sem marca nomeada, destilação de 8 exemplos alinhados aos eixos).
- **O ledger de decisões re-ranqueia o recommender.** `.ux/decisions.jsonl` re-classifica candidatos por vitórias passadas no mesmo bucket `(industry, ui_type)`. Cold-start seguro. Só conta decisões com `lint_score >= 80` + `user_accepted = true`.
- **Matriz de interação de eixos**: resolução explícita de conflitos (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px de radius). Acabou a regra ad-hoc silenciosa.
- **Loop automático `/ux-evolve`** (na 4.0, o loop padrão do `/ux-polish`): lint → polish → re-lint até score ≥ 90, platô ou 3 rodadas na 4.0 (5 na v3). Quality gate em 65.
- **3 novas ferramentas MCP** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Dashboard de stats local**: `uxskill stats --html` escreve `.ux/stats.html` mostrando o que A SUA instalação aprendeu. Sem telemetria, sem agregado global.
- **223 testes passam.** Offline. Determinístico. Nunca chama um LLM.

Detalhes completos em [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Histórico de estrelas

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## O que é o ux-skill

O ux-skill é um **motor de inteligência de design** para ferramentas de coding com IA. Roda como pacote Python (`pip install uxskill`), como plugin do Claude Code e como multi-instalador para 17 IDEs. O motor ingere um brief de projeto (indústria, audiência, tom, must-haves, jogadas proibidas, stack, região) e devolve um sistema de design recomendado completo: estilo, paleta, par tipográfico, presets de motion, componentes, marcas exemplares para estudar e os guardrails de anti-pattern que precisam ser respeitados. A recomendação é determinística, a mesma entrada sempre produz a mesma saída.

O plugin fica entre você e a ferramenta de coding com IA. Quando você pede ao Claude Code, Cursor ou qualquer outro assistente de IA para «construir uma landing page fintech», o assistente normalmente improvisa, e o resultado é reconhecido como gerado por IA em cinco segundos (gradientes roxo-azul, três cards iguais, Inter em tamanho de display, «John Doe» nos depoimentos, transições padrão de 300ms, hero centralizado, setas saltitantes nos CTAs). O ux-skill substitui a improvisação por **restrições estruturadas**: você executa `/ux-discover` para capturar o brief e escolher o sistema, `/ux-design` para gerar o código e `/ux-lint` para verificar que ele passa nas 171 regras determinísticas anti-AI-slop antes do commit.

Este README é a referência canônica. Cada comando, cada sub-agent, cada manifest de dados, cada caminho de instalação, cada spec de marca, cada categoria de anti-pattern, está tudo documentado aqui. Se você está procurando um plugin de design para Claude Code ou comparando ferramentas de design com IA para Cursor, Windsurf ou Codex, leia do começo ao fim junto com [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Sumário

1. [O cérebro, o que é a v3.0](#o-cérebro-o-que-é-a-v30)
2. [Instalação rápida](#instalação-rápida)
3. [Os números, comparativo ao vivo contra as 8 melhores skills de UX do Claude](#os-números-comparativo-ao-vivo-contra-as-8-melhores-skills-de-ux-do-claude)
4. [Arquitetura, como as peças se encaixam](#arquitetura-como-as-peças-se-encaixam)
5. [Os 18 comandos slash, referência detalhada](#os-18-comandos-slash-referência-detalhada)
6. [Os 5 sub-agents](#os-5-sub-agents)
7. [Os 11 manifests de dados](#os-11-manifests-de-dados)
8. [As 171 regras anti-AI-slop, o linter](#as-171-regras-anti-ai-slop-o-linter)
9. [As 160 specs de marca DESIGN.md, por categoria](#as-160-specs-de-marca-designmd-por-categoria)
10. [Servidor MCP, a jogada assimétrica](#servidor-mcp-a-jogada-assimétrica)
11. [O instalador para 17 IDEs](#o-instalador-para-17-ides)
12. [Casos de uso, cenários concretos](#casos-de-uso-cenários-concretos)
13. [Comparado às alternativas](#comparado-às-alternativas)
14. [Roadmap](#roadmap)
15. [Como contribuir](#como-contribuir)
16. [Licença, autor, agradecimentos](#licença-autor-agradecimentos)

---

## O cérebro: o que é a v3.0

A v3.1.0 é a maior mudança arquitetural da história do ux-skill. O recommender não escolhe mais templates de um catálogo, o motor **sintetiza** uma linguagem de design fresca por brief. O mesmo brief sempre produz a mesma saída (totalmente determinística), mas cada brief distinto recebe seu próprio sistema novo. As brand specs deixam de ser templates; viram dados de treinamento dos quais o motor aprende o vocabulário. O sistema tem olhos sobre o próprio histórico, fecha o loop de feedback localmente, e nunca chama um LLM.

O compilador é um **sintetizador determinístico de 7 eixos**, warmth, contrast, density, geometry, formality, motion, type_personality. Cada brief mapeia para valores de eixos; valores de eixos compilam em palette + tipografia + spacing + radius + motion frescos. As escalas tipográficas modulares escolhem sua razão a partir do contrast (1.200 quiet / 1.250 balanced / 1.333 loud). As primitivas de layout são responsive by construction (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Layouts quebrados não podem ser emitidos porque não são representáveis.

Há três modos auto-despachados: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% dos tokens da Stripe, caminho mais rápido); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% adaptado por eixos a partir de 4 marcas-irmãs); e `pure_synthesis` (sem marca nomeada → espaço infinito, 8 exemplos alinhados aos eixos destilados em uma linguagem de design nova). Conflitos entre eixos são resolvidos por uma **matriz de interação de eixos** documentada, dense + corporate compila em 4px (density ganha, escola Bloomberg), airy + corporate em 12px (formality ganha, luxo), soft + playful em 18px de radius, sharp + corporate em 2px. Sem regras ad-hoc silenciosas na implementação.

O **ledger de decisões** (`.ux/decisions.jsonl`, schema `_v: 1` travado) fecha o loop de feedback. O recommender agora reordena candidatos por vitórias passadas no mesmo bucket `(industry, ui_type)`. Seguro no início a frio: abaixo de 3 antecedentes ele pula a reordenação. Só conta decisões com `lint_score >= 80` E `user_accepted = true`. Além disso, `/ux-polish` roda lint → polish → re-lint até score ≥ 90, platô ou 3 rodadas, com um quality gate em 65 abaixo do qual a saída é recusada sem `--force`. Resultado: cada instalação fica mais inteligente sobre o próprio corpus, cada execução é reproduzível entre máquinas, e o motor permanece totalmente offline.

---

## Instalação rápida

Três caminhos de instalação. Escolha o que se encaixa no seu ambiente.

### Caminho 1: marketplace do Claude Code (canônico)

Se você vive no Claude Code, instale via o marketplace de plugins:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Isso conecta todos os 18 comandos slash (mais 7 nomes antigos mantidos como aliases até a 4.1) e os 5 sub-agents na sua sessão do Claude Code. Após a instalação, execute `/ux-init` para configurar o diretório de estado `.ux/` por projeto e verificar que o motor Python está acessível.

### Caminho 2: pip (universal)

Se você vive fora do Claude Code (Cursor, Windsurf, CLI, CI), instale o pacote Python:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

O pacote expõe tanto `ux` quanto `uxskill` como entry points de CLI, são o mesmo binário.

### Caminho 3: npx (sem precisar de Python)

Se você não quer gerenciar Python diretamente, o wrapper npx faz o bootstrap de tudo via `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verificar a instalação

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

As doze contagens somam 1.262 entradas. Se alguma contagem retornar 0, o arquivo JSON está faltando: abra uma issue em [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Os números: comparativo ao vivo contra as 8 melhores skills de UX do Claude

As contagens de estrelas foram verificadas pela última vez via `gh api` em **2026-05-28**. O ux-skill (Laith0003/ux-skill) é o recém-chegado, somos pequenos em awareness, profundos em arquitetura. A comparação abaixo é honesta: onde a gente perde, onde a gente ganha.

| Plugin | Estrelas | Arquitetura | Comandos slash | Linter (CI-safe) | Specs de marca | Componentes | Presets de motion | IDEs suportados |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, skill única | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skills + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + taste embasada em pesquisa | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | SKILL.md único de 62 KB + scripts | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Biblioteca de skills conectada por MCP | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill de uma única estética | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill de design anti-slop | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Componentes MD3 + auditoria | 1 | - | (somente MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Motor Python + 12 manifests + 18 comandos + 5 sub-agents + linter de CI** | **18** | **171 regras determinísticas** | **160** | **148** | **57** | **17** |

### Onde a gente perde

- **Awareness.** Eles têm centenas de milhares de estrelas. A gente tem 14. Dá uma estrela, é o jeito mais barato de ajudar.
- **Reconhecimento de marca.** ui-ux-pro-max e open-design têm vantagem medida em meses, não em dias.
- **Acabamento de marketing.** Eles têm screenshots, vídeos de demo e uma landing achável. A gente tem um README minucioso e uma landing magrinha.

### Onde a gente ganha

- **Biblioteca de componentes:** 148 componentes documentados com anatomia, estados, tokens usados e especificações de motion. Nenhum dos outros 8 distribui um manifest de componentes.
- **Presets de motion:** 57 entradas prontas para o stack (Framer Motion, GSAP, CSS) com fallbacks de reduced-motion. Nenhum dos outros distribui um manifest de motion.
- **Linter de anti-pattern:** 171 regras determinísticas, roda em CI, sai com código não-zero em Critical/High. Nenhum dos outros distribui um linter determinístico.
- **Specs de marca:** 160 specs DESIGN.md reais (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude e mais 96). Nenhum dos outros distribui uma biblioteca de marca.
- **17 IDEs suportados:** mesmo motor, cola diferente por IDE.
- **18 comandos slash:** discovery, geração (páginas, componentes, dashboards, a partir de uma imagem), auditoria, lint, loop de polish, loop de fix, case-study, workshop, copy, motion, a11y, conductor, totalmente integrados.

Comparativo completo tabela por tabela em [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Arquitetura: como as peças se encaixam

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

### Como o motor funciona de verdade

1. **Entrada.** Você fornece um brief, de forma interativa via `/ux-discover` (10 campos) ou não interativa via flags para `ux recommend`.
2. **5 buscas em paralelo.** O motor faz cinco consultas simultâneas nos manifests:
   - **Setor → recommended_styles** (industries.json)
   - **Estilo → compatibilidade de paleta + tipografia + motion** (styles.json)
   - **Tom × must-have → filtro de paletas** (palettes.json)
   - **Stack → compatibilidade de componentes + presets de motion** (tech-stacks.json, motion-presets.json)
   - **Proibidos + região → guardrails + lista curta de marcas exemplares** (anti-patterns.json, brands/)
3. **Merge.** Um merger determinístico ordena os candidatos, resolve conflitos (por exemplo, modo escuro obrigatório força o modo da paleta) e emite um único sistema recomendado.
4. **Saída.** Um documento JSON com o estilo escolhido, a paleta, o par tipográfico, os 5 melhores presets de motion, os 12 melhores componentes, as 5 melhores marcas exemplares e todos os 171 guardrails de anti-pattern ativos. Mais um bloco de justificativa que explica cada escolha.
5. **Geração.** Os comandos seguintes (`/ux-design` nos modos página, componente, dashboard e imagem, e `/ux-system`) usam a recomendação para gerar código real pelos sub-agents.
6. **Verificação.** `/ux-lint` reescaneia o código gerado contra as 171 regras. Sai com código não-zero em Critical/High no CI.

**Novidades da v3.** O recommender agora reordena candidatos a partir de `engine/decisions/` usando `.ux/decisions.jsonl` (só conta decisões com `lint_score >= 80` E `user_accepted = true`; seguro no início a frio abaixo de 3 antecedentes). O caminho de geração pode passar por `engine/synthesizer/`, um compilador determinístico de 7 eixos que produz tokens novos de paleta + tipografia + espaçamento + raio + motion para cada brief em vez de escolher templates de um catálogo. Detalhes em [O cérebro, o que é a v3.0](#o-cérebro-o-que-é-a-v30).

**Python pensa. HTML mostra. Markdown encadeia.**

---

## Os 18 comandos slash: referência detalhada

Cada comando é distribuído como um arquivo `.md` em `commands/` com `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` e `output state file`. As descrições abaixo são resumidas; a fonte completa é a especificação de referência.

Os comandos são agrupados em sete blocos: **bootstrap e inventário**, **discovery e recomendação**, **geração**, **auditoria e verificação**, **correção e polish**, **discovery e narrativa** e **conductor**. Sete nomes da 3.x continuam funcionando como [aliases](#aliases-removidos-na-41) até a 4.1.

### Bootstrap & inventário

#### `/ux-init`: bootstrap do projeto

- **O que faz:** Detecta qual IDE você está usando (`.claude/`, `.cursor/`, `.windsurf/`, etc.), instala o artefato certo, verifica que o motor Python está acessível e imprime um snapshot de estatísticas. `--stats` imprime só o snapshot: versão + contagens de entradas dos manifests de dados.
- **Quando usar:** Primeira instalação em um projeto novo. Após clonar um projeto que usa ux-skill. Após `pip install --upgrade uxskill`. `--stats` após a instalação, após um upgrade ou quando uma recomendação traz escolhas surpreendentes e você suspeita de manifests incompletos.
- **Quando pular:** Você já rodou nesse projeto e nada mudou. `--stats` nunca precisa ser pulado: é uma leitura de 50ms.
- **Invocação:** `/ux-init` (sem argumentos), `/ux-init --stats`, ou `uxskill init` / `uxskill stats` pelo CLI. `--decisions` adiciona o resumo do ledger de decisões; `--html` grava `.ux/stats.html`.
- **Output:** Artefato por IDE (veja [O instalador para 17 IDEs](#o-instalador-para-17-ides)) + diretório `.ux/` + resumo no stdout. `--stats`: JSON no stdout (veja [Verificar a instalação](#verificar-a-instalação) acima).
- **Encadeia para:** `/ux-discover` em seguida. `--stats` é só diagnóstico.

#### `/ux-mcp`: rodar o motor como servidor MCP

- **O que faz:** Inicia o motor como servidor Model Context Protocol via stdio. 25 ferramentas (o recommender, o linter, a persistência, o sintetizador, o ledger de decisões, a extração de imagem, os manifests de dados, e criar, importar, aprimorar, estender, exportar e verificar um design system) passam a ser chamáveis de qualquer host compatível com MCP, sem o plugin.
- **Quando usar:** Você trabalha em outro host compatível com MCP e quer o mesmo motor. Você roda um pipeline multiagente que precisa de uma única fonte de restrições de design. Você quer o recommender ou o linter como processo de longa duração no CI.
- **Quando pular:** Você está no Claude Code com o plugin instalado; os comandos slash já chegam ao motor. Você precisa de uma resposta pontual; `uxskill recommend` ou `uxskill lint` é mais simples.
- **Invocação:** `/ux-mcp`, ou `ux-mcp` no shell depois de `pip install 'uxskill[mcp]'`.
- **Output:** Um servidor JSON-RPC via stdio. Veja [Servidor MCP](#servidor-mcp-a-jogada-assimétrica) e `commands/ux-mcp.md` para a configuração de cada cliente.
- **Encadeia para:** Nada; é um transporte, não uma etapa.

### Discovery & recomendação

#### `/ux-discover`: a função obrigatória (intake de 10 campos, framing, recomendação)

- **O que faz:** O intake obrigatório de 10 campos pelo qual todo projeto passa antes de qualquer comando de geração. Tipo de projeto, público, objetivo principal, tom, must-haves, proibidos, marcas de referência, stack, região, métrica de sucesso. **Sem improviso.** Frases banidas («moderno», «clean») obrigam o usuário a ser específico. Depois roda o recommender: as 5 buscas em paralelo do motor Python em 12 manifests devolvem um único design system mesclado (Setor → Estilo → Paleta → Tipografia → Motion + Componentes + Marcas exemplares + Guardrails).
- **Modos:** `--frame` registra para quem, outcome, hipótese e sinal de sucesso num bloco de framing de quatro campos, mais leve que o intake completo. `--recommend` roda só o recommender, a partir de um brief salvo ou de flags pontuais.
- **Quando usar:** Antes de qualquer `/ux-design` ou `/ux-system`. Sempre que um brief anterior ficou velho. `--frame` no início de um projeto, sprint ou trabalho pontual, ou no meio do caminho quando uma conversa se perdeu. `--recommend` ao reposicionar um produto com cara de cansado.
- **Quando pular:** Você está corrigindo um bug (`/ux-fix`). Você só está rodando uma passada de linter (`/ux-lint`). O brief não mudou desde a última sessão.
- **Invocação (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` ou `/ux-discover --recommend`.
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
- **Output:** `.ux/last-discovery.json` (o brief de 10 campos), `.ux/last-recommendation.json` (estilo escolhido, paleta, par tipográfico, 5 melhores presets de motion, 12 melhores componentes, 5 melhores marcas exemplares, todos os 171 guardrails de anti-pattern ativos, mais justificativa) e, com `--frame`, `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Encadeia para:** `/ux-design [extra brief]` → código frontend baseado na recomendação. `/ux-design --component <name>` → um componente alinhado às restrições levantadas. `/ux-system` → design system completo a partir da recomendação. `/ux-lint` → verifica o código gerado.

### Geração

#### `/ux-design`: gera uma superfície bonita e anti-slop a partir de um brief

- **O que faz:** Gera um artefato frontend completo, de nível produção (landing, site de marketing, app shell) a partir do brief de discovery + recomendação. Despacha `frontend-engineer` com direção criativa das referências anti-slop e de arsenal. O brief, ou uma flag, escolhe um de quatro modos:
  - **página** (padrão): uma página completa ou uma superfície com várias seções. Grava `.ux/last-design.json`.
  - **`--component [name]`**: um único componente de nível produção (botão, modal, navbar, sidebar, card, tabela, formulário, gráfico). Os quatro estados de interação, acessível, fiel à marca. Procura primeiro o componente em `.ux/last-recommendation.json` e, se não achar, consulta direto o manifest. Grava `.ux/last-component.json`.
  - **`--dashboard`**: disciplina de densidade de dados, layout bento, numerais monoespaçados tabulares, padrões de sparkline, sem excesso de cards, cores de estado semânticas, motion econômico. Não é um site de marketing com gráficos colados. Grava `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: lê uma imagem de referência (PNG/JPG/WebP) com visão computacional pura em Pillow (paleta dominante, polaridade do fundo, sinal tipográfico), compara com os manifests de paletas e estilos e constrói a partir da recomendação resultante. `--extract-only` para depois da extração. Grava `.ux/last-image-extract.json`.
- **Quando usar:** «Desenhe uma», «me constrói uma», «gere uma landing page», «cria um dashboard», «faz um componente», «constrói um botão», «desenha o painel admin», «console de operador», «painel de KPI», «faz igual a esta captura de tela», qualquer pedido de entrega visual livre.
- **Quando pular:** Você quer uma revisão, não uma build (use `/ux-audit` ou `/ux-critique`). Trabalho de backend ou infraestrutura.
- **Invocação:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Output:** Código gerado (HTML / Blade / JSX / Vue / Astro), mais o arquivo de estado do modo.
- **Encadeia para:** `/ux-lint` → verifica contra os guardrails. `/ux-polish` → passada cosmética. `/ux-a11y` → auditoria de acessibilidade. `/ux-copy` → revisão de microcopy. `/ux-fix` → aplica achados como commits atômicos.

#### `/ux-system`: gera um sistema de design starter completo

- **O que faz:** Propõe um sistema de design starter completo para um projeto que não tem um, tokens (cor, tipo, espaço, motion, raio, sombra), docs de foundation, contratos de componentes, pareamentos dark-mode, theme switcher. Despacha `design-system-architect`.
- **Quando usar:** «A gente não tem um sistema de design», «constrói um sistema pra gente», «propõe os tokens», «qual deve ser nosso tema», «configura nosso DS».
- **Quando pular:** O projeto já tem um design system; use `/ux-design --component` sobre o sistema existente. Backend ou infraestrutura.
- **Invocação:** `/ux-system create` (o motor de fundamentos), `/ux-system enhance --from <file>` (medir um sistema que você já tem), `/ux-system extend --from <file> --add <foundation>` (ampliar sem alterar) ou `/ux-system` (o fluxo da 3.x; roda o discovery primeiro se ainda não houver um brief salvo).
- **Output:** `tokens.json`, `foundations.md`, contratos `components/*.md`, emit opcional Tailwind / vanilla / SCSS. Escreve `.ux/last-system.json` para contexto de encadeamento.
- **Encadeia para:** `/ux-design --component` → construir sobre o novo sistema. `/ux-design` → gerar uma superfície com os novos tokens.

#### `/ux-motion`: tratamento de motion

- **O que faz:** Gera a camada de motion de uma superfície, durações, easings, coreografia, fallbacks de reduced-motion, disciplina de performance. Também audita motion existente contra as 5 dimensões (timing, easing, significado, reduced-motion, performance).
- **Quando usar:** «Verifica o motion», «as animações estão boas», «conserta o motion», «revisa as animações», «auditoria de motion», «passada de performance no motion».
- **Quando pular:** Superfície não tem motion (use `/ux-audit` ou `/ux-polish`). Backend ou infraestrutura.
- **Invocação:** `/ux-motion path/to/component.tsx` (modo auditoria) ou `/ux-motion --generate hero-entry` (geração).
- **Output:** Código atualizado (em modo geração) ou relatório `.ux/last-motion.json` (em modo auditoria).
- **Encadeia para:** `/ux-fix` → aplica achados de motion. `/ux-polish` → aperta.

### Auditoria & verificação

#### `/ux-lint`: linter determinístico baseado em regex (sem LLM, CI-safe)

- **O que faz:** Roda 171 regras contra seu código. Sem chamada LLM. Sai com código não-zero em Critical / High no CI. Fonte: `data/anti-patterns.json`. As regras cobrem A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).
- **Quando usar:** Hook de pre-commit. Gate de CI. Primeira passada rápida em uma codebase grande antes de pagar o custo de `/ux-audit`. Após `/ux-design` em qualquer modo para verificar a geração.
- **Quando pular:** Você quer um fix loop (o linter reporta, não edita, encadeia em `/ux-polish --fix` ou `/ux-fix`). Você quer julgamento de taste (use `/ux-critique`).
- **Invocação (slash):** `/ux-lint src/`.
- **Invocação (CLI):** `uxskill lint .` ou `python3 bin/ux-lint.py .` ou `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocação (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Achados no stdout (localização, id da regra, severidade, evidência). Código de saída 0 se limpo, não-zero em Critical/High quando `--fail-on high` está setado.
- **Encadeia para:** `/ux-polish --fix` → contraparte LLM-driven nos mesmos padrões. `/ux-fix` → aplica achados como commits, ordenados por severidade. `/ux-audit` → passada completa de raciocínio em 6 lentes. `/ux-next` → deixa o conductor decidir.

#### `/ux-audit`: auditoria de design em 6 lentes

- **O que faz:** Uma revisão estruturada e opinada contra seis lentes (clareza, hierarquia, acessibilidade, voz, motion, taste), produzindo achados marcados por severidade. Relatório estilo Polaris. Lê `.ux/last-frame.json` primeiro, audiência e outcome ancoram a severidade de cada achado.
- **Quando usar:** Superfície existe e você quer uma crítica defensável. «Audita», «revisa o ux», «isso tá bom», «o que tá quebrado», «destrói isso».
- **Quando pular:** Superfície ainda não existe (use `/ux-design`). Usuário quer uma lente (use o comando focado: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Usuário quer opinião de taste (use `/ux-critique`). Backend ou infraestrutura.
- **Invocação:** `/ux-audit https://example.com/pricing` ou `/ux-audit src/components/Pricing.tsx`.
- **Output:** Escreve `.ux/last-audit.json`, array `findings` de `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Encadeia para:** `/ux-fix` → aplica achados. `/ux-polish` → passada cosmética. `/ux-design` → se um redesign estrutural for necessário.

#### `/ux-a11y`: auditoria WCAG 2.1 AA + checagens de cortesia comum

- **O que faz:** Uma auditoria estruturada WCAG 2.1 AA, mais as checagens de cortesia comum que passam pelas ferramentas automatizadas mas ainda machucam usuários reais (visibilidade de foco, especificidade de erro, preferências de motion, armadilhas de teclado, dependência de cor).
- **Quando usar:** Gate de acessibilidade pré-release. Após um redesign. «Verifica acessibilidade», «auditoria WCAG», «isso é acessível», «revisão a11y», «teste de screen reader», «verifica navegação por teclado».
- **Quando pular:** Não voltado para usuário. Backend ou infraestrutura. Esboços work-in-progress.
- **Invocação:** `/ux-a11y https://example.com` (URL live preferido, ferramentas automatizadas e teste de teclado só funcionam ao vivo).
- **Output:** Escreve `.ux/last-a11y.json`, array `findings` de `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Encadeia para:** `/ux-fix` → aplica achados como commits. `/ux-copy` → corrige alt text e wiring de erro de form como parte de uma passada de copy.

#### `/ux-critique`: chamada de taste (3 acertos, 3 erros, 1 jogada estratégica)

- **O que faz:** A opinião de um designer, não uma auditoria estruturada, não uma nota de severidade, só um take apertado e opinado que nomeia o que está funcionando, o que não está e a jogada estratégica que mudaria o máximo.
- **Quando usar:** «O que você acha», «isso tá bom», «critica isso», «opinião honesta», «a vibe tá certa», «parece a gente», «devemos lançar».
- **Quando pular:** Usuário quer explicitamente uma auditoria estruturada (use `/ux-audit`). Backend ou infraestrutura.
- **Invocação:** `/ux-critique https://example.com`.
- **Output:** Escreve `.ux/last-critique.json`, 3 acertos, 3 erros, 1 jogada estratégica, mais a prosa.
- **Encadeia para:** `/ux-design` se o take recomenda redesign. `/ux-polish` se o take recomenda apertar.

#### `/ux-copy`: revisão + reescrita de microcopy

- **O que faz:** Avalia cada string visível contra a rubrica de voz e produz uma reescrita before/after. Pega: «form contains errors» (genérico), «John Doe» (placeholder), copy AI-animada celebrativa, CTAs genéricas, empty states mortos, erros inúteis.
- **Quando usar:** Estrutura está certa mas as palavras estão fracas. «Revisa a copy», «conserta a microcopy», «as mensagens de erro estão ruins», «reescreve isso», «aperta as strings», «os botões soam genéricos», «esse empty state tá morto».
- **Quando pular:** Problemas de layout (use `/ux-audit` ou `/ux-polish`). Problemas de copy dirigidos por acessibilidade como alt text (use `/ux-a11y`). Backend ou infraestrutura.
- **Invocação:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Escreve `.ux/last-copy.json`, array `strings` de `{location, severity, before, after, notes}`, mais rubrica + locais que precisam de tradução.
- **Encadeia para:** `/ux-fix` → aplica reescritas. `/ux-a11y` → re-verifica após correções de copy.

### Fix & polish

#### `/ux-fix`: aplica achados como commits atômicos

- **O que faz:** Lê o último relatório de `.ux/` (audit, copy, a11y, motion ou polish), valida a working tree e aplica os achados como commits atômicos via os sub-agents certos. Re-verifica rodando o comando de origem.
- **Quando usar:** Após executar um comando da classe auditoria e revisar os achados. «Conserta os achados», «aplica as correções», «roda o fix loop», «aplica patch na superfície», «faz as mudanças», «vai consertar».
- **Quando pular:** Nenhum relatório anterior em `.ux/`. Working tree está suja e o usuário não concordou com stash/commit. Correções precisam de julgamento de design, não aplicação mecânica (use `/ux-design` para redesign).
- **Invocação:** `/ux-fix` (detecta automaticamente qual relatório consertar) ou `/ux-fix --from=last-a11y.json`.
- **Output:** Commits atômicos por achado. Re-roda o comando de origem e atualiza o arquivo `.ux/last-*.json`. Imprime um resumo.
- **Encadeia para:** `/ux-next` → conductor escolhe a próxima jogada.

#### `/ux-polish`: loop de lint, fix e re-lint + matar AI-slop

- **O que faz:** Primeiro um loop determinístico sobre um arquivo HTML local: lint, seis passadas de polish idempotentes, re-lint, até o score chegar a 90, estabilizar ou passarem três rodadas (`--rounds` muda o limite). Por padrão, a saída do loop fica em `<file>.evolved.html` e o original nunca é tocado. Só `--loop-only` ou `--fix` substituem o original, depois de verificar que a árvore de trabalho está limpa, e um quality gate em 65 impede que um resultado reprovado o substitua sem `--force`; com `--brand-file`, o piso de fidelidade à marca vale em cada saída. Depois vem a passada de taste: ritmo do espaçamento, hierarquia mais nítida, detecção de AI-slop, consistência de tokens. A contraparte guiada por LLM do `/ux-lint`, que usa o seu julgamento nas decisões de taste. `--loop-only` roda só o loop; `--no-loop`, só a passada de taste; `--fix` aplica os achados de taste.
- **Quando usar:** A estrutura está certa, mas a execução está frouxa. «Polir», «aperta isso», «remove o AI-slop», «deixa premium», «faz isso parecer menos AI», «o espaçamento está estranho», «isso parece genérico», «precisa de mais taste», «melhora até score 90+», «deixa pronto pra publicar».
- **Quando pular:** Falta funcionalidade essencial na superfície (corrija isso primeiro). Precisa de redesign, não de polish (use `/ux-design`). Problemas de copy (use `/ux-copy`). Problemas de motion (use `/ux-motion`). Problemas de a11y (use `/ux-a11y`).
- **Invocação:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Output:** `<file>.evolved.html` do loop (promovido no lugar do original só com `--loop-only` ou `--fix`), código atualizado com `--fix`, `.ux/last-evolve.json`, uma linha em `.ux/decisions.jsonl` e `.ux/last-polish.json` descrevendo os achados de taste.
- **Encadeia para:** `/ux-lint` → verifica que o polish se manteve. `/ux-a11y` → reconfere a acessibilidade.

### Discovery & narrativa

#### `/ux-research`: planejamento de pesquisa + síntese

- **O que faz:** Modo planejamento: escreve roteiros de entrevista, surveys, screeners de recrutamento. Modo síntese (`--synthesize`): digere entrevistas, analytics, sites de concorrentes, resultados A/B, tickets de suporte em recomendações. Despacha `research-synthesizer`.
- **Quando usar:** «Planeja um estudo de pesquisa», «preciso de perguntas de entrevista», «desenha um survey», «como recruto usuários», «plano de user testing», «diary study», «teste de preferência», «fake door», «smoke test», «sintetiza minhas notas de entrevista».
- **Quando pular:** Resposta já é conhecida com alta confiança. Decisões reversíveis de baixo risco. Backend ou infraestrutura.
- **Invocação:** `/ux-research --plan "loyalty wallet adoption in MENA"` ou `/ux-research --synthesize interviews/*.md`.
- **Output:** Escreve `.ux/last-research.json`, plano de pesquisa ou temas sintetizados + evidências + recomendações.
- **Encadeia para:** `/ux-discover --frame` → integrar os achados num frame. `/ux-design` → gerar a partir dos achados. `/ux-workshop` → conduzir um workshop usando a pesquisa como entrada.

#### `/ux-workshop`: workshop de design thinking em 5 fases

- **O que faz:** Facilita um workshop de discovery / design thinking end-to-end. Cinco fases sequenciais (exploração → heat map → mapa de stakeholders → solução em esboço → game plan). Cronometrado. Artefatos concretos por fase. Termina com uma decisão, não «achados interessantes».
- **Quando usar:** Pergunta real, participantes reais, orçamento de tempo real. «Roda um workshop», «facilita uma discovery», «vamos fazer uma sessão de design thinking», «tenho stakeholders por uma hora, o que fazemos», «começa o projeto».
- **Quando pular:** O brief já está claro e delimitado. Brainstorm sozinho (use `/ux-design` ou `/ux-discover --frame`). O time está no meio da execução, não em discovery.
- **Invocação:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Escreve `.ux/last-workshop.json`, game plan + artefatos por fase.
- **Encadeia para:** `/ux-design` → executa o game plan. `/ux-research` → preenche lacunas que o workshop surfou. `/ux-case-study` → publica a jornada.

#### `/ux-case-study`: case study publicável (formato editorial Wfrah)

- **O que faz:** Gera um case study do projeto em formato editorial monocromático puro, tipografia Wfrah, separadores finos, códigos de seção numerados de (A) a (G), layout seguro para conteúdo bilíngue. Um documento, não um folheto de marketing. Lê de `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Quando usar:** Pós-lançamento. Após um marco discreto. «Escreve um case study», «case study desse projeto», «faz o documento de fechamento», «publica esse trabalho», «peça de portfólio».
- **Quando pular:** Faltam dados ao projeto para preencher as seções (A) a (G). O usuário quer uma landing de marketing, não um case study (use `/ux-design`).
- **Invocação:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Encadeia para:** Comando terminal, geralmente o fim de um projeto.

### Conductor

#### `/ux-next`: condutor de workflow (read-only)

- **O que faz:** Lê cada `.ux/last-*.json` e nomeia o próximo comando de maior alavancagem. Um condutor, não um construtor. Read-only.
- **Quando usar:** Entre comandos. «O que devo fazer em seguida», «qual é a próxima jogada», «decide por mim», «pra onde vamos daqui».
- **Quando pular:** Nenhum relatório anterior em `.ux/`. Você tem um próximo comando específico em mente.
- **Invocação:** `/ux-next` (sem argumentos) ou `/ux-next --focus=a11y`.
- **Output:** Stdout, próximo comando recomendado + racional.
- **Encadeia para:** Seja qual for o comando escolhido.

#### `/ux-expert`: hook de consultoria

- **O que faz:** Surface a informação de contato do criador do plugin quando um usuário pede por um especialista de UX da vida real. Breve, direto, sem marketing.
- **Quando usar:** «Quem construiu isso», «preciso de um especialista de UX», «vocês fazem consultoria», «posso contratar alguém pra isso», «tem um humano por trás desse plugin».
- **Quando pular:** Usuário está perguntando sobre features do plugin, não sobre consultoria.
- **Invocação:** `/ux-expert`.
- **Output:** Cartão de contato breve com LinkedIn / email / repo.

### Aliases, removidos na 4.1

Sete comandos da 3.x foram incorporados aos 18 acima. Os nomes deles continuam funcionando por mais uma versão: cada alias diz para onde foi e depois roda o novo comando com os mesmos argumentos.

| Comando antigo | Agora | Notas |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | O mesmo bloco de framing, o mesmo `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | A ferramenta MCP `ux_recommend` não muda |
| `/ux-stats` | `/ux-init --stats` | Snapshot somente leitura |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | O alias mantém o antigo limite de cinco rodadas; `/ux-polish` sozinho para em três |
| `/ux-component` | `/ux-design --component` | O mesmo `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | O mesmo `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Tire `--extract-only` para construir a partir da imagem |

### Grafo de encadeamento de comandos

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

## Os 5 sub-agents

Sub-agents são geradores específicos de papel despachados por comandos. Eles nunca rodam de forma independente: são chamados por `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Cada agent tem um escopo de responsabilidade definido: ele NÃO decide o brief; ele o executa.

### `frontend-engineer`

- **Possui:** Código frontend de nível produção (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) com disciplina anti-AI-slop.
- **Despachado por:** `/ux-design` (modos página, componente, dashboard e imagem), `/ux-fix`.
- **Inputs:** Brief + direção criativa + tokens (de `.ux/last-recommendation.json`).
- **Outputs:** Código funcionando que se distingue do output genérico de IA. Sem gradientes roxos, sem hero centralizado, sem três cards iguais, sem Inter em tamanho de display, sem «John Doe», sem emoji, sem defaults de 300ms.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Possui:** Motion em código frontend de produção, Framer Motion, GSAP, animações CSS. Durações, easings, coreografia, fallbacks de reduced-motion, disciplina de performance.
- **Despachado por:** `/ux-design` (todos os modos), `/ux-motion --fix`.
- **Inputs:** Brief de motion + tokens + os 57 presets de motion de `data/motion-presets.json`.
- **Outputs:** Motion que merece seu lugar. Sempre envolto em fallbacks de `prefers-reduced-motion`. Sempre testado contra Core Web Vitals.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Possui:** As strings que vão pro ar, mensagens de erro, empty states, CTAs, estados de loading, mensagens de sucesso, toasts, texto auxiliar, labels de form, texto de botão.
- **Despachado por:** `/ux-copy --fix`, `/ux-design` (todos os modos), `/ux-discover --frame`.
- **Inputs:** Perfil de voz (nomeado ou colado) + as strings da superfície.
- **Outputs:** Microcopy de produção aplicada consistentemente em cada estado de uma superfície para que o produto soe como um produto, não dez. Proibidos: «form contains errors», «John Doe», copy AI-animada celebrativa, CTAs genéricas, empty states mortos.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Possui:** Digerir inputs de pesquisa (entrevistas, analytics, sites competitivos, resultados A/B, tickets de suporte) em recomendações de design acionáveis.
- **Despachado por:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Inputs:** Pesquisa bruta, transcrições, exports, URLs de concorrentes, clusters de suporte.
- **Outputs:** Temas, evidências, recomendações. Nunca desenha a resposta, dá ao designer o substrato a partir do qual desenhar.
- **Ferramentas:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Possui:** Sistemas de design completos, tokens (cor, tipo, espaço, motion, raio, sombra), docs de foundation, contratos de componentes, pareamentos dark-mode, camada de theming.
- **Despachado por:** `/ux-system`, `/ux-design --component` quando não existe nenhum sistema.
- **Inputs:** Brief de marca + `.ux/last-recommendation.json` (estilo + paleta + par tipográfico + presets de motion).
- **Outputs:** Um sistema coerente, opinado e pronto pra produção sobre o qual os agents a jusante podem construir sem ter que re-decidir fundamentos. Tokens JSON, foundations MD, contratos de componentes, mapeamento dark-mode.
- **Ferramentas:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocolo de despacho de sub-agents

Quando um comando despacha um sub-agent, ele passa:

1. O brief / recomendação (carregados de `.ux/`).
2. A fatia de manifest relevante (ex: `frontend-engineer` recebe o estilo + paleta + componentes escolhidos; `motion-engineer` recebe os presets de motion escolhidos).
3. Os 171 guardrails de anti-pattern (sempre ativos).
4. Um critério de sucesso (o que o artefato precisa fazer).

Sub-agents retornam:

1. O artefato (código, doc, sistema).
2. Um bloco de racional (por que essas escolhas).
3. Um self-check contra os guardrails (quais regras eles verificaram).

O comando que chama então roda `/ux-lint` automaticamente antes de declarar pronto.

---

## Os 11 manifests de dados

A camada de dados é o cérebro. Cada comando lê dela; o motor mescla através dela; o linter escaneia contra ela. Todos os arquivos vivem em `data/` e envolvem suas entradas em `{_meta, entries}` para versionamento de schema.

### `styles.json`: 84 estilos de design

| Campo | Descrição |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, etc. |
| `sample entry` | `swiss-international`, «O grid é lei. A tipografia faz o trabalho pesado. Decoração é falha.» |

Usado por: `/ux-discover`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 paletas de cor

| Campo | Descrição |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, etc. |
| `sample entry` | `claude-warm-editorial`, light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Usado por: `/ux-discover`, `/ux-system`. Contraste verificado em AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 pareamentos tipográficos

| Campo | Descrição |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + pesos + fonte + licença + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Todas as famílias têm licença + URL de origem. Usado por `/ux-discover`, `/ux-system`.

### `components.json`: 148 componentes

| Campo | Descrição |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, anatomia de 6 partes, 4 estados |

Esse é nosso maior fosso. Nenhum outro plugin de UX para Claude distribui um manifest estruturado de componentes.

### `industries.json`: 184 regras de indústria

| Campo | Descrição |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, etc. |
| `sample entry` | `fintech-neobank`, alta confiança, divulgações regulatórias, UI primária de saldo/transação, mobile-first uso diário |

Usado pelo recommender (`/ux-discover`) como primeiro eixo de busca paralela.

### `chart-types.json`: 35 tipos de gráfico

| Campo | Descrição |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, compara de 4 a 15 categorias discretas. A posição no eixo x representa a categoria; a altura, o valor. |

Usado por `/ux-design --dashboard` e `/ux-design --component` (instâncias de gráfico).

### `tech-stacks.json`: 25 stacks

| Campo | Descrição |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, compatível com Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Outras stacks incluem Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 leis de UX nomeadas

| Campo | Descrição |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, etc. |
| `sample entry` | `hicks-law`, Tempo de decisão cresce logaritmicamente com o número de escolhas apresentadas |

Usado por `/ux-audit` (scoring de 6 lentes) e `/ux-critique` (âncora de taste).

### `motion-presets.json`: 57 presets de motion

| Campo | Descrição |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback de reduced-motion), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Cada preset tem uma variante reduced-motion. Código pronto pro stack para Framer Motion, GSAP e CSS puro.

### `anti-patterns.json`: 171 regras

| Campo | Descrição |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (tipo, padrão, flags, escopo e, em muitas regras, uma verificação `post` sobre o arquivo analisado), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

A lista completa de regras está em [As 171 regras anti-AI-slop](#as-171-regras-anti-ai-slop-o-linter).

### `brands/*.json`: 160 specs de marca

| Campo | Descrição |
|---|---|
| `entries` | 160 (mais `_index.json` listando todas) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Lista completa em [As 160 specs de marca DESIGN.md](#as-160-specs-de-marca-designmd-por-categoria).

---

## As 171 regras anti-AI-slop: o linter

O ux-skill distribui um linter determinístico: cada regra é um padrão, e muitas acrescentam uma verificação sobre o CSS e o markup analisados, de modo que uma ocorrência só conta no contexto que ela nomeia. **Sem LLM.** **Sem API.** **Sem rede.** Roda no CI em ~200ms num app Next.js típico. Sai com código não-zero em achados Critical / High quando `--fail-on high` está definido.

As regras vêm de `data/anti-patterns.json` (v2, preferido) com `references/foundations/anti-patterns.md` como fallback (v1, bash). Dois binários são distribuídos: `bin/ux-lint.py` (Python, rápido, extensível) e `bin/ux-lint.sh` (Bash + perl-PCRE, para ambientes sem Python).

### Regras por categoria

O catálogo completo das 171 regras, por categoria e depois por severidade, é gerado a partir de `data/anti-patterns.json` no [README em inglês](README.md#rules-by-category); lá os IDs e nomes das regras aparecem como o linter os imprime. As regras cobrem A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### Uso do linter

**Scan avulso:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## As 160 specs de marca DESIGN.md: por categoria

Marcas reais. Linguagens de design reais. Specs DESIGN.md reais, não paletas genéricas. Diz pro plugin «constrói uma landing no estilo da Stripe» e ele lê o vocabulário real da marca: rubrica de voz, tokens de cor, convenções de motion, jogadas de assinatura, jogadas proibidas.

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

Os outros 8 plugins de UX populares para Claude geram «modern minimal» ou «clean dashboard», variantes da mesma estética default. O ux-skill permite que você peça **a clareza da Linear**, **a seriedade da Stripe**, **a contenção da Apple**, **o monólito da Tesla**, **a simpatia da Notion**, **a disciplina de gradiente do Cursor**, **a densidade hairline do Raycast**, **o editorial caloroso da Claude**, e o motor puxa os tokens certos, voz, convenções de motion e jogadas de assinatura da spec da marca.

---

## Servidor MCP: a jogada assimétrica

O ux-skill distribui um **servidor Model Context Protocol**. Rode `ux-mcp` e o motor vira um processo stdio de longa duração que qualquer host compatível com MCP (Claude Desktop, Cursor, Windsurf, agents genéricos) pode chamar. 25 ferramentas: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Os mesmos handlers Python que os comandos slash usam; os mesmos manifests de dados; o mesmo recommender determinístico.

**Por que essa é a jogada assimétrica:** nenhuma das oito principais skills de UX para Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) distribui um servidor MCP. Elas estão trancadas dentro do runtime de plugins do Claude Code. O ux-skill é alcançável de qualquer host que fale MCP, incluindo agents que nunca ouviram falar de um plugin do Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Aponta seu client para o binário `ux-mcp`. Documentação completa de ferramentas, exemplos JSON e configuração por client para Claude Desktop, Cursor e Windsurf vivem em [docs/mcp.html](docs/mcp.html) e em `commands/ux-mcp.md`.

---

## O instalador para 17 IDEs

`uxskill init` (ou `/ux-init` dentro do Claude Code) detecta automaticamente qual IDE você está usando e escreve o artefato certo. Mesmo motor Python. Mesmas recomendações. Cola diferente por IDE.

| IDE / Ferramenta | Sinal de detecção | Artefato instalado |
|---|---|---|
| Claude Code | `.claude/` ou `CLAUDE.md` | Manifest do plugin em `.claude-plugin/plugin.json` + todos os 18 comandos (e 7 aliases) + todos os 5 sub-agents |
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

## Casos de uso: cenários concretos

Oito cenários reais. Escolhe o mais próximo da sua situação e adapta a invocação.

### 1. Construindo um dashboard fintech no Cursor

Você está no Cursor trabalhando no dashboard de uma neobank MENA. Você instala o plugin e roda discovery, recomendação, depois geração de dashboard.

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

Depois no Cursor, peça: *«Gere a superfície de dashboard usando a recomendação em .ux/last-recommendation.json»*. O Cursor lê o header `.cursorrules`, carrega a recomendação, despacha uma geração de dashboard com restrições explícitas.

### 2. Gerando uma landing estilo Stripe no Claude Code

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Três comandos, uma superfície polida, commits atômicos por correção.

### 5. Desenhando uma command palette estilo Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

O componente gerado usa os tokens de cor reais da Linear, stack de tipografia, convenções de motion, densidades hairline, não «UI dark genérica».

### 6. Conduzindo um workshop de design thinking de 90 minutos com stakeholders

Você tem uma sala com 5 pessoas por 90 minutos. Você quer que eles saiam com um game plan, não com uma vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

O plugin facilita as cinco fases (exploração → heat map → mapa de stakeholders → solução em esboço → game plan) end-to-end, cronometrado, com artefatos concretos por fase. O output é `.ux/last-workshop.json`, o game plan, não só «achados interessantes».

### 7. Escrevendo um case study publicável após o lançamento

Você lançou a loyalty wallet. Você quer uma peça pra portfólio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

O case study é um artefato pronto e publicável, não um rascunho. Monocromia pura, tipografia editorial, pronto pra mandar pro seu portfólio.

### 8. Rodando discovery em contexto não-IA (só intake estruturado)

Você está escopando um projeto. Você não precisa de uma recomendação ainda, você precisa de um brief estruturado.

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

Você pode entregar o JSON pro seu time, colar num doc do Notion ou alimentar uma ferramenta de IA separada. O ux-skill também é uma ferramenta de intake estruturado além de ser um motor.

### 9. Persistência MASTER.md: suas decisões de design, no repo

Depois de `/ux-discover` (ou `/ux-discover --recommend`), salve o estilo + paleta + tipografia + motion + componentes + marcas exemplares + guardrails escolhidos num arquivo Markdown legível que o seu time pode revisar, comparar e versionar.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Escreve `.ux/design-system/MASTER.md` (frontmatter YAML + corpo) e `.ux/design-system/pages/<name>.md` por superfície gerada via `persist save-page`. Idempotente, o mesmo input produz output byte-idêntico, então re-rodar em estado inalterado é no-op no git.

---

## Comparado às alternativas

Tabela resumo curta. Comparação completa tabela por tabela em [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensão | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Comandos slash | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Componentes | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Presets de motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specs de marca | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Regras de anti-pattern | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter determinístico CI-safe | **sim** | não | não | não | não | não | não | não | não |
| IDEs suportados | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Gate de discovery | **10 campos** | implícito | implícito | implícito | implícito | implícito | implícito | implícito | implícito |
| Cadeia de estado `.ux/` | **sim** | não | não | não | não | não | não | não | não |
| Estrelas (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Avaliação honesta

- **ui-ux-pro-max** é maior em awareness, suporta 18 IDEs, tem busca estilo BM25 no CSV dele. Não distribui manifest de componentes, manifest de motion, biblioteca de marca ou linter determinístico.
- **open-design** tem 19 skills + preview mas só suporte Claude Code e nenhuma camada anti-slop.
- **hallmark** é o mais próximo em espírito (também anti-slop) mas é uma skill única, sem motor, sem manifests, sem comandos encadeados.
- **material-3-skill** é excelente se você quer especificamente Material Design 3. A gente não compete em MD3.

Para detalhe completo por dimensão, veja [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

Próximos passos, sem versão definida:

- **Estilos do Figma**: estilos de efeito para sombras, estilos de grade e estilos de texto vinculados às variáveis de campo, gravados num arquivo ao vivo.
- **Mapeamento de componentes**: um componente do Figma e suas variantes ligados a um componente de código e suas props, preservados durante o handoff.
- **Um importador de sites ao vivo**: ler o sistema que um site publicado realmente renderiza, ao lado dos importadores de arquivos.
- **Páginas de documentação para um sistema criado**: a visão humana dos seus tokens, papéis e contratos.

Também em aberto:

- **`uxskill lint --fix` para reescritas seguras** de achados corrigíveis mecanicamente (button-no-type, img-no-alt com string vazia, remoção de console-log-leak).
- **Extensão para VS Code** que mostra os achados do lint inline.
- **Emissão de código por componente** em seis stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Marketplace de specs de marca**: publicar e descobrir specs de marca da comunidade.
- **Regras de anti-pattern personalizadas**: descoberta e compartilhamento das regras que os projetos definem em `data/anti-patterns.local.json`.
- **`uxskill plan`**: planejamento de sites com várias páginas a partir de um brief, não só de uma superfície.

---

## Como contribuir

Issues e PRs bem-vindas. Três áreas de alta alavancagem:

### Adicionar uma regra de anti-pattern

1. Edita `data/anti-patterns.json`, adiciona uma entrada com `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Adiciona um teste em `tests/linter/`, um arquivo que dispara a regra, um que não.
3. Roda `uxskill lint tests/linter/should-trigger/<rule>.tsx`, confirma que dispara. Roda em `tests/linter/should-not-trigger/<rule>.tsx`, confirma que não dispara.
4. Abre uma PR.

### Adicionar uma spec de marca

1. Cria `data/brands/<slug>.json` com `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Adiciona a prosa correspondente em `references/brands/<slug>.md`.
3. Registra em `data/brands/_index.json`.
4. Abre uma PR. A spec deve ser baseada em referências de fonte-primária (o produto real da marca, o sistema de design público, ou DESIGN.md se eles publicam um).

### Adicionar um preset de motion

1. Edita `data/motion-presets.json`, adiciona uma entrada com `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. O preset deve ter uma variante reduced-motion. Sem exceções.
3. Abre uma PR.

### Processo

- Leia [CONTRIBUTING.md](CONTRIBUTING.md) pra processo completo.
- Leia [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Novas regras e specs de marca são revisadas para: ancoragem em fonte-primária, sem overfit em projeto único, sem emoji em nenhum dos dados, comportamento RTL-safe onde aplicável.

---

## Licença, autor, agradecimentos

### Licença

MIT. Usa, faz fork, constrói em cima. Se te salva de mandar AI slop pra produção, dá uma estrela no repo, é o jeito mais barato de apoiar.

### Autor

**Laith Aljunaidy**: fundador solo de [Dot](https://thedotwallet.com), uma plataforma de loyalty MENA-first. Construindo o ux-skill pra que o frontend gerado por IA não pareça todo igual.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Agradecimentos

- O time da Anthropic pelo Claude Code e a arquitetura de skill / plugin que tornou isso distribuível.
- Nielsen Norman Group, Laws of UX (lawsofux.com) e a comunidade de pesquisa em UX cujo trabalho informa `data/ux-guidelines.json`.
- Cada marca listada em `data/brands/`, seus sistemas de design públicos são a fonte da verdade para as specs de marca.
- Os contribuidores originais da v1: uma skill Claude single-shot que virou semente para o motor Python v2.
- Os 8 plugins de UX populares para Claude com os quais a gente se comparou, eles elevaram o sarrafo; essa é nossa resposta.

---

**ux-skill** · **v4.0.0** · Construído pra que Claude Code, Cursor, Windsurf e qualquer outra ferramenta de coding com IA emitam frontend que não se lê como gerado por IA.

> Dá uma estrela no repo em [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Instala via `pip install uxskill` ou `npx uxskill init` · Navega o comparativo em [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
