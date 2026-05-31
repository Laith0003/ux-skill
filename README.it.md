[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · **Italiano** · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — il motore di intelligenza di design per Claude Code, Cursor e ogni altro strumento di coding con IA

> **v3.1.0 stable — THE BRAIN.** Il plugin UX più potente per il coding con IA. Un nucleo di ragionamento Python con 12 manifest JSON interrogabili (84 stili, 176 palette, 70 abbinamenti tipografici, 148 componenti, 184 settori, 35 tipi di grafico, 57 preset di motion, 112 leggi UX, 152 regole di anti-pattern, 25 stack tecnologici, 160 specifiche di brand), 25 comandi slash, 5 sub-agent e un linter deterministico anti-AI-slop. Multi-IDE: si distribuisce in Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer e Roo Cline.

> **Il nome del brand è `ux-skill`.** Il nome del pacchetto PyPI / npm rimane `uxskill`. Il repository GitHub si trova su [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Sito:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Confronto con ogni plugin UX per Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.1.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#linstallatore-per-17-ide)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-223_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Novità di v3

- **Le brand specs diventano dati di addestramento, non template.** Le 160 brand specs non sono più un catalogo da cui il recommender pesca — sono vocabolario che il sintetizzatore distilla. Ogni chiamata produce un sistema nuovo.
- **Sintetizzatore a 7 assi** (warmth, contrast, density, geometry, formality, motion, type_personality). Il brief è mappato in modo deterministico su valori di assi; i valori di assi compilano in palette + tipografia + spacing + radius + motion freschi.
- **Tre modalità auto-dispatch** — `strict_brand` (100 % di un brand), `brand_anchor` (70 % di un brand + 30 % adattato per assi da brand fratelli), `pure_synthesis` (nessun brand nominato — distillazione di 8 esempi allineati agli assi).
- **Il ledger delle decisioni ri-ordina il recommender.** `.ux/decisions.jsonl` ri-classifica i candidati per vittorie passate nello stesso bucket `(industry, ui_type)`. Cold-start sicuro. Conta solo le decisioni con `lint_score >= 80` + `user_accepted = true`.
- **Matrice di interazione degli assi** — risoluzione esplicita dei conflitti (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px di radius). Niente più regole ad-hoc silenziose.
- **Loop automatico `/ux-evolve`** — lint → polish → re-lint fino a punteggio ≥ 90, plateau o 5 giri. Quality gate a 65.
- **3 nuovi strumenti MCP** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Dashboard di stats locale** — `uxskill stats --html` scrive `.ux/stats.html` che mostra cosa ha imparato la TUA installazione. Niente telemetria, niente aggregazione globale.
- **223 test passano.** Offline. Deterministico. Mai una chiamata LLM.

Dettagli completi in [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Cronologia stelle

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Cos'è ux-skill

ux-skill è un **motore di intelligenza di design** per strumenti di coding con IA. Funziona come pacchetto Python (`pip install uxskill`), come plugin di Claude Code e come multi-installatore per 17 IDE. Il motore acquisisce un brief di progetto (settore, audience, tono, must-have, mosse vietate, stack, regione) e restituisce un sistema di design raccomandato completo: stile, palette, abbinamento tipografico, preset di motion, componenti, brand esemplari da studiare e i guardrail di anti-pattern che devono reggere. La raccomandazione è deterministica — lo stesso input produce sempre lo stesso output.

Il plugin si colloca tra te e lo strumento di coding con IA. Quando chiedi a Claude Code, Cursor o a qualsiasi altro assistente IA di «costruire una landing fintech», l'assistente di solito improvvisa — e il risultato si riconosce come generato dall'IA in cinque secondi (gradienti viola-blu, tre card uguali, Inter a dimensione display, «John Doe» nelle testimonianze, transizioni di default a 300ms, hero centrato, frecce rimbalzanti sulle CTA). ux-skill sostituisce l'improvvisazione con **vincoli strutturati**: esegui `/ux-discover` per catturare il brief, `/ux-recommend` per scegliere il sistema, `/ux-design` per generare il codice e `/ux-lint` per verificare che superi le 152 regole deterministiche anti-AI-slop prima del commit.

Questo README è il riferimento canonico. Ogni comando, ogni sub-agent, ogni manifest di dati, ogni percorso di installazione, ogni specifica di brand, ogni categoria di anti-pattern — è tutto documentato qui. Se stai cercando un plugin di design per Claude Code o confrontando strumenti di design IA per Cursor, Windsurf o Codex, leggi questo dall'inizio alla fine insieme a [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Indice

1. [Il cervello — cos'è v3.0](#il-cervello--cosè-v30)
2. [Installazione rapida](#installazione-rapida)
3. [I numeri — confronto live con le 8 migliori skill UX per Claude](#i-numeri--confronto-live-con-le-8-migliori-skill-ux-per-claude)
4. [Architettura — come si incastrano i pezzi](#architettura--come-si-incastrano-i-pezzi)
5. [I 25 comandi slash — riferimento dettagliato](#i-22-comandi-slash--riferimento-dettagliato)
6. [I 5 sub-agent](#i-5-sub-agent)
7. [Gli 12 manifest di dati](#gli-11-manifest-di-dati)
8. [Le 152 regole anti-AI-slop — il linter](#le-145-regole-anti-ai-slop--il-linter)
9. [Le 160 specifiche di brand DESIGN.md — per categoria](#le-160-specifiche-di-brand-designmd--per-categoria)
10. [Server MCP — la mossa asimmetrica](#server-mcp--la-mossa-asimmetrica)
11. [L'installatore per 17 IDE](#linstallatore-per-17-ide)
12. [Casi d'uso — scenari concreti](#casi-duso--scenari-concreti)
13. [Confronto con le alternative](#confronto-con-le-alternative)
14. [Roadmap](#roadmap)
15. [Contribuire](#contribuire)
16. [Licenza, autore, ringraziamenti](#licenza-autore-ringraziamenti)

---

## Il cervello — cos'è v3.0

v3.1.0 è il cambiamento architetturale più grande nella storia di ux-skill. Il recommender non sceglie più template da un catalogo — il motore **sintetizza** un linguaggio di design fresco per ogni brief. Lo stesso brief produce sempre lo stesso output (totalmente deterministico), ma ogni brief distinto riceve il suo sistema nuovo. Le brand specs non sono più template; sono dati di addestramento da cui il motore impara il vocabolario. Il sistema ha occhi sulla propria storia, chiude il loop di feedback localmente, e non chiama mai un LLM.

Il compilatore è un **sintetizzatore deterministico a 7 assi** — warmth, contrast, density, geometry, formality, motion, type_personality. Ogni brief mappa a valori di assi; i valori di assi compilano in palette + tipografia + spacing + radius + motion freschi. Le scale tipografiche modulari scelgono il loro rapporto dal contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Le primitive di layout sono responsive by construction (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Layout rotti non possono essere emessi perché non sono rappresentabili.

Ci sono tre modalità auto-dispatch: `strict_brand` (`reference_brands=[stripe] strict=True` → 100 % token Stripe, percorso più veloce); `brand_anchor` (`reference_brands=[stripe]` → 70 % Stripe + 30 % adattato per assi da 4 brand fratelli); e `pure_synthesis` (nessun brand nominato → spazio infinito, 8 esempi allineati agli assi distillati in un linguaggio di design nuovo). I conflitti tra assi sono risolti da una **matrice di interazione degli assi** documentata — dense + corporate compila in 4px (density vince, scuola Bloomberg), airy + corporate in 12px (formality vince, lusso), soft + playful in 18px di radius, sharp + corporate in 2px. Niente regole ad-hoc silenziose nell'implementazione.

Il **ledger delle decisioni** (`.ux/decisions.jsonl`, schema `_v: 1` bloccato) chiude il loop di feedback. Il recommender ora ri-classifica i candidati per vittorie passate nello stesso bucket `(industry, ui_type)`. Cold-start sicuro — salta sotto i 3 priors. Conta solo le decisioni con `lint_score >= 80` E `user_accepted = true`. Inoltre `/ux-evolve` esegue lint → polish → re-lint fino a punteggio ≥ 90, plateau o 5 giri, con un quality gate a 65 sotto il quale l'output viene rifiutato senza `--force`. Risultato: ogni installazione diventa più intelligente sul proprio corpus, ogni esecuzione è riproducibile tra macchine, e il motore rimane totalmente offline.

---

## Installazione rapida

Tre percorsi di installazione. Scegli quello adatto al tuo ambiente.

### Percorso 1 — marketplace di Claude Code (canonico)

Se lavori in Claude Code, installa tramite il marketplace dei plugin:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Questo collega tutti i 25 comandi slash e i 5 sub-agent alla tua sessione di Claude Code. Dopo l'installazione, esegui `/ux-init` per configurare la directory di stato `.ux/` per progetto e verificare che il motore Python sia raggiungibile.

### Percorso 2 — pip (universale)

Se lavori fuori da Claude Code (Cursor, Windsurf, CLI, CI), installa il pacchetto Python:

```bash
pip install uxskill
uxskill init                       # rileva automaticamente il tuo IDE e installa l'artefatto giusto
uxskill stats                      # stampa i conteggi dei manifest per verificare l'installazione
uxskill lint .                     # esegue il linter sulla directory corrente
```

Il pacchetto espone sia `ux` sia `uxskill` come entry point CLI — sono lo stesso binario.

### Percorso 3 — npx (nessun Python richiesto)

Se non vuoi gestire Python direttamente, il wrapper npx fa il bootstrap di tutto tramite `pipx`:

```bash
npx uxskill init                  # scarica pipx + uxskill alla prima esecuzione
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verifica dell'installazione

```bash
ux stats
# {
#   "version": "3.1.0-stable",
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
#     "anti-patterns": 145,
#     "brands": 160
#   }
# }
```

Se uno qualsiasi dei conteggi restituisce 0, il file JSON è mancante — apri una issue su [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## I numeri — confronto live con le 8 migliori skill UX per Claude

I conteggi delle stelle sono stati verificati l'ultima volta tramite `gh api` il **2026-05-28**. ux-skill (Laith0003/ux-skill) è il nuovo arrivato — siamo piccoli sull'awareness, profondi sull'architettura. Il confronto qui sotto è onesto: dove perdiamo, dove vinciamo.

| Plugin | Stelle | Architettura | Comandi slash | Linter (CI-safe) | Specifiche di brand | Componenti | Preset di motion | IDE supportati |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, skill singola | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + taste basata su ricerca | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Singolo SKILL.md da 62 KB + script | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Libreria di skill collegata via MCP | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill su un'unica estetica | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill di design anti-slop | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Componenti MD3 + audit | 1 | — | (solo MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Motore Python + 12 manifest + 25 comandi + 5 sub-agent + linter CI** | **22** | **152 regole regex** | **160** | **148** | **57** | **17** |

### Dove perdiamo

- **Awareness.** Loro hanno centinaia di migliaia di stelle. Noi ne abbiamo 14. Mettici una stella — è il modo più economico per aiutare.
- **Riconoscibilità del brand.** ui-ux-pro-max e open-design hanno un vantaggio misurato in mesi, non in giorni.
- **Rifinitura di marketing.** Loro hanno screenshot, video demo e una landing trovabile. Noi abbiamo un README accurato e una landing essenziale.

### Dove vinciamo

- **Libreria di componenti:** 148 componenti documentati con anatomia, stati, token usati e specifiche di motion. Nessuno degli altri 8 distribuisce un manifest di componenti.
- **Preset di motion:** 57 voci pronte per lo stack (Framer Motion, GSAP, CSS) con fallback per reduced-motion. Nessuno degli altri distribuisce un manifest di motion.
- **Linter anti-pattern:** 152 regole regex deterministiche, gira in CI, esce con codice diverso da zero su Critical/High. Nessuno degli altri distribuisce un linter deterministico.
- **Specifiche di brand:** 160 specifiche DESIGN.md reali (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude e altre 96). Nessuno degli altri distribuisce una libreria di brand.
- **17 IDE supportati:** stesso motore, collante diverso per IDE.
- **25 comandi slash:** discovery, generazione, audit, lint, polish, fix loop, case-study, workshop, copy, motion, a11y, dashboard, conductor — completamente integrati.

Il confronto completo tabella per tabella è su [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Architettura — come si incastrano i pezzi

```
ux-skill (nome del pacchetto: uxskill)
│
├── data/                              Il cervello — manifest JSON interrogabili
│   ├── styles.json                    84 stili di design + quando/saltare + token
│   ├── palettes.json                  176 palette (light/dark, contrasto verificato)
│   ├── type-pairs.json                70 triplette display × body × mono
│   ├── components.json                148 componenti (anatomia, stati, motion)
│   ├── industries.json                184 regole di settore + segnali di audience
│   ├── chart-types.json               35 tipi di grafico (quando/saltare, encoding)
│   ├── tech-stacks.json               25 stack (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 leggi UX nominate (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 preset di motion (entry, exit, hover...)
│   ├── anti-patterns.json             152 regole regex (sorgente linter CI-safe)
│   └── brands/*.json                  160 specifiche DESIGN di brand + _index.json
│
├── engine/                            Python — il ragionamento
│   ├── synthesizer/                   v3 — compilatore deterministico a 7 assi
│   ├── decisions/                     v3 — ledger .ux/decisions.jsonl + ri-classificazione del recommender
│   ├── recommender/                   motore di merge a 5 ricerche parallele
│   ├── linter/                        scanner deterministico anti-slop
│   ├── discovery/                     protocollo forzante a 10 campi
│   ├── generator/                     emettitore di token + manifest
│   ├── installer/                     multi-installatore per 17 IDE
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          25 comandi slash di Claude Code (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    snapshot dell'inventario
│   ├── ux-discover.md                 intake a 10 campi (gate)
│   ├── ux-recommend.md                FLAGSHIP — ricerca a 5 parallele
│   ├── ux-lint.md                     linter deterministico
│   ├── ux-design.md                   genera codice frontend
│   ├── ux-component.md                genera un singolo componente
│   ├── ux-system.md                   genera un sistema di design completo
│   ├── ux-dashboard.md                genera una superficie dashboard
│   ├── ux-motion.md                   trattamento + audit di motion
│   ├── ux-audit.md                    audit di design a 6 lenti
│   ├── ux-a11y.md                     audit WCAG 2.1 AA
│   ├── ux-critique.md                 critica di gusto (3 vittorie, 3 mancanze, 1 mossa)
│   ├── ux-copy.md                     revisione + riscrittura della microcopy
│   ├── ux-fix.md                      applica i finding come commit atomici
│   ├── ux-polish.md                   passata cosmetica + uccisione dell'AI-slop
│   ├── ux-frame.md                    blocco di framing a 4 campi
│   ├── ux-research.md                 pianificazione + sintesi della ricerca
│   ├── ux-workshop.md                 workshop di design thinking in 5 fasi
│   ├── ux-case-study.md               case study pubblicabile in formato editoriale Wfrah
│   ├── ux-next.md                     conductor di workflow (read-only)
│   └── ux-expert.md                   hook di consulenza
│
├── agents/                            5 sub-agent (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy nella voce del brand
│   ├── research-synthesizer.md        interviste + analytics + competitor
│   └── design-system-architect.md     token / componenti / foundations
│
├── references/                        Sorgenti in prosa per i dati + pagine demo
│   ├── foundations/                   anti-patterns.md, principi, taste
│   ├── laws/                          leggi UX in formato esteso
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        prosa per stile (anti-slop.md, ecc.)
│   ├── components/                    componenti in formato esteso
│   ├── output/                        rubriche di output
│   └── conditional/                   guida specifica per stack
│
├── bin/
│   ├── uxskill.mjs                    wrapper npx -> motore Python
│   ├── ux-lint.py                     linter v2 (preferito)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (creato per progetto)
    ├── last-discovery.json            snapshot del brief
    ├── last-recommendation.json       sistema scelto
    ├── last-frame.json                blocco di framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Come funziona davvero il motore

1. **Input.** Fornisci un brief — in modo interattivo via `/ux-discover` (10 campi) o non interattivo via flag a `ux recommend`.
2. **5 ricerche parallele.** Il motore esegue cinque lookup in modo concorrente sui manifest:
   - **Settore → recommended_styles** (industries.json)
   - **Stile → palette + tipografia + compatibilità motion** (styles.json)
   - **Tono × must-have → filtro palette** (palettes.json)
   - **Stack → compatibilità componenti + preset di motion** (tech-stacks.json, motion-presets.json)
   - **Forbidden + regione → guardrail + shortlist brand esemplari** (anti-patterns.json, brands/)
3. **Merge.** Un merger deterministico classifica i candidati, risolve i conflitti (es. must-have dark-mode forza la modalità della palette) ed emette un singolo sistema raccomandato.
4. **Output.** Un documento JSON con stile scelto, palette, abbinamento tipografico, top 5 preset di motion, top 12 componenti, top 5 brand esemplari e tutti i 152 guardrail anti-pattern attivi. Più un blocco di razionale che spiega ogni scelta.
5. **Generazione.** I comandi a valle (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) consumano la raccomandazione per generare codice reale tramite i sub-agent.
6. **Verifica.** `/ux-lint` riscansiona il codice generato contro le 152 regole regex. Esce con codice diverso da zero su Critical/High in CI.

**Python pensa. HTML mostra. Markdown concatena.**

---

## I 25 comandi slash — riferimento dettagliato

Ogni comando viene distribuito come file `.md` sotto `commands/` con `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` e `output state file`. Le descrizioni qui sotto sono condensate; il sorgente completo è la spec canonica.

I comandi sono raggruppati in cinque secchielli: **bootstrap e inventario**, **discovery e raccomandazione**, **generazione**, **audit e verifica**, **fix e polish** e **conductor**.

### Bootstrap e inventario

#### `/ux-init` — bootstrap del progetto

- **Cosa fa:** Rileva quale IDE stai usando (`.claude/`, `.cursor/`, `.windsurf/`, ecc.), installa l'artefatto giusto, verifica che il motore Python sia raggiungibile, stampa uno snapshot delle statistiche.
- **Quando usarlo:** Prima installazione in un progetto nuovo. Dopo aver clonato un progetto che usa ux-skill. Dopo `pip install --upgrade uxskill`.
- **Quando saltarlo:** L'hai già eseguito in questo progetto e nulla è cambiato.
- **Invocazione:** `/ux-init` (nessun argomento) o `uxskill init` da CLI.
- **Output:** Artefatto per IDE (vedi [L'installatore per 17 IDE](#linstallatore-per-17-ide)) + directory `.ux/` + riepilogo su stdout.
- **Concatena a:** `/ux-discover` come passo successivo.

#### `/ux-stats` — stampa l'inventario dei dati

- **Cosa fa:** Stampa versione + conteggi di voci per gli 12 manifest di dati, così puoi verificare cosa è installato.
- **Quando usarlo:** Dopo l'installazione. Dopo l'upgrade. Quando `/ux-recommend` restituisce scelte sorprendenti e sospetti che i manifest siano incompleti.
- **Quando saltarlo:** Mai — è un comando read-only da 50ms.
- **Invocazione:** `/ux-stats` o `uxskill stats`.
- **Output:** JSON su stdout (vedi [Verifica dell'installazione](#verifica-dellinstallazione) sopra).
- **Concatena a:** Solo diagnostico; non alimenta nulla a valle.

### Discovery e raccomandazione

#### `/ux-discover` — la funzione forzante (intake a 10 campi)

- **Cosa fa:** L'intake obbligatorio a 10 campi che ogni progetto attraversa prima di qualsiasi comando di generazione. Tipo di progetto, audience, obiettivo primario, tono, must-have, vietati, brand di riferimento, stack, regione, metrica di successo. **Nessuna improvvisazione.** Frasi vietate («moderno», «pulito») costringono l'utente a essere specifico.
- **Quando usarlo:** Prima di qualsiasi `/ux-design`, `/ux-component`, `/ux-system` o `/ux-dashboard`. Ogni volta che un brief precedente è diventato obsoleto.
- **Quando saltarlo:** Stai correggendo un bug (`/ux-fix`). Stai solo eseguendo una passata di linter (`/ux-lint`). Il brief è invariato dall'ultima sessione.
- **Invocazione:** `/ux-discover`. Il plugin chiede; tu rispondi.
- **Output:** Scrive `.ux/last-discovery.json` (il brief a 10 campi).
- **Concatena a:** `/ux-recommend` → usa la discovery per scegliere stile + palette + tipografia + motion + componenti. `/ux-design [brief extra]` → genera codice frontend ancorato alla raccomandazione. `/ux-component <nome>` → genera un componente allineato ai vincoli scoperti.

#### `/ux-recommend` — il motore flagship a 5 ricerche parallele

- **Cosa fa:** Esegue la ricerca a 5 parallele del motore Python sugli 12 manifest e restituisce un sistema di design unito. Settore → Stile → Palette → Tipografia → Motion + Componenti + Brand esemplari + Guardrail.
- **Quando usarlo:** Avviando un nuovo progetto da zero. Facendo pivot a un prodotto stanco. Pre-flight prima di qualsiasi `/ux-design` o `/ux-component`.
- **Quando saltarlo:** Hai già eseguito `/ux-discover` e salvato un brief — `/ux-recommend` è automatico in quel flusso. Stai correggendo un bug (usa `/ux-fix`). Devi solo fare lint (usa `/ux-lint`).
- **Invocazione (Claude Code):**
  ```
  /ux-recommend
  ```
  **Invocazione (CLI):**
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
- **Output:** Scrive `.ux/last-recommendation.json` — stile scelto, palette scelta, abbinamento tipografico scelto, top 5 preset di motion, top 12 componenti, top 5 brand esemplari, tutti i 152 guardrail anti-pattern attivi, più il razionale.
- **Concatena a:** `/ux-design [brief]` → codice frontend con i token raccomandati. `/ux-system` → sistema di design completo dalla raccomandazione. `/ux-component <nome>` → un componente con lo stile raccomandato. `/ux-lint` → verifica il codice generato.

### Generazione

#### `/ux-design` — genera una superficie bella e anti-slop da un brief

- **Cosa fa:** Genera un artefatto frontend completo, di livello produzione (landing, sito marketing, app shell) dal brief di discovery + raccomandazione. Dispaccia `frontend-engineer` con direzione creativa da anti-slop e referenze d'arsenale.
- **Quando usarlo:** «Design una», «costruiscimi una», «genera una landing page», «crea una dashboard», «fa' un componente» — qualsiasi richiesta di consegna visiva libera.
- **Quando saltarlo:** Vuoi una review, non una build (usa `/ux-audit` o `/ux-critique`). Vuoi un solo componente (usa `/ux-component`). Lavoro di backend o infrastruttura.
- **Invocazione:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Output:** Codice generato (HTML / Blade / JSX / Vue / Astro), più `.ux/last-design.json`.
- **Concatena a:** `/ux-lint` → verifica contro i guardrail. `/ux-polish` → passata cosmetica. `/ux-a11y` → audit di accessibilità. `/ux-copy` → revisione della microcopy. `/ux-fix` → applica i finding come commit atomici.

#### `/ux-component` — genera un singolo componente

- **Cosa fa:** Produce un singolo componente di livello produzione (button, modal, navbar, sidebar, card, table, form, chart) da una spec. Tutti e quattro gli stati di interazione, accessibile, on-brand. Cerca il componente in `.ux/last-recommendation.json` per primo, ripiega sulla query diretta al manifest.
- **Quando usarlo:** Qualsiasi richiesta di singolo elemento — «costruisci un button», «crea una pricing card», «fa' un modal», «aggiungi una navbar», «design una sidebar», «mi serve una tabella dati», «costruisci un form», «fa' un componente chart».
- **Quando saltarlo:** Pagina intera o superficie multi-sezione (usa `/ux-design`). Backend o infrastruttura.
- **Invocazione:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Output:** Codice componente generato, più `.ux/last-component.json`.
- **Concatena a:** `/ux-lint` → verifica. `/ux-polish` → stringe.

#### `/ux-system` — genera un sistema di design starter completo

- **Cosa fa:** Propone un sistema di design starter completo per un progetto che non ne ha uno — token (colore, tipografia, spazio, motion, raggi, ombre), documenti di foundations, contratti di componenti, abbinamenti dark-mode, theme switcher. Dispaccia `design-system-architect`.
- **Quando usarlo:** «Non abbiamo un sistema di design», «costruiscici un sistema», «proponi i token», «quale dovrebbe essere il nostro tema», «configura il nostro DS».
- **Quando saltarlo:** Il progetto ha già un sistema di design — usa `/ux-component` contro il sistema esistente. Backend o infrastruttura.
- **Invocazione:** `/ux-system` (esegue prima la discovery se non già in archivio).
- **Output:** `tokens.json`, `foundations.md`, contratti `components/*.md`, emit opzionale Tailwind / vanilla / SCSS. Scrive `.ux/last-system.json` per il contesto di concatenamento.
- **Concatena a:** `/ux-component` → costruisce contro il nuovo sistema. `/ux-design` → genera una superficie usando i nuovi token.

#### `/ux-dashboard` — generazione specializzata di dashboard

- **Cosa fa:** Dashboard con disciplina di densità dei dati — layout bento, numerali monospace tabulari, pattern di sparkline, anti-overuse di card, colori di stato semantici, motion parsimonioso. Non una pagina marketing con grafici incollati.
- **Quando usarlo:** «Costruisci una dashboard», «design il pannello admin», «fa' una pagina di metriche», «console operatore», «vista analytics», «board KPI», «schermata di monitoring».
- **Quando saltarlo:** Landing marketing con statistiche (usa `/ux-design`). Un solo widget (usa `/ux-component`). Backend o infrastruttura.
- **Invocazione:** `/ux-dashboard`.
- **Output:** Codice dashboard generato + `.ux/last-dashboard.json`.
- **Concatena a:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — trattamento di motion

- **Cosa fa:** Genera lo strato di motion di una superficie — durate, easing, coreografia, fallback reduced-motion, disciplina di performance. Esegue anche l'audit del motion esistente contro le 5 dimensioni (timing, easing, significato, reduced-motion, performance).
- **Quando usarlo:** «Verifica del motion», «le animazioni sono buone», «sistema il motion», «rivedi le animazioni», «audit del motion», «passata di performance sul motion».
- **Quando saltarlo:** La superficie non ha motion (usa `/ux-audit` o `/ux-polish`). Backend o infrastruttura.
- **Invocazione:** `/ux-motion path/to/component.tsx` (modalità audit) o `/ux-motion --generate hero-entry` (generazione).
- **Output:** Codice aggiornato (in modalità generazione) o report `.ux/last-motion.json` (in modalità audit).
- **Concatena a:** `/ux-fix` → applica i finding di motion. `/ux-polish` → stringe.

### Audit e verifica

#### `/ux-lint` — linter deterministico regex (no LLM, CI-safe)

- **Cosa fa:** Esegue 152 regole regex contro il tuo codice. Nessuna chiamata LLM. Esce con codice diverso da zero su Critical / High in CI. Sorgente: `data/anti-patterns.json`. Le regole coprono A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4).
- **Quando usarlo:** Hook pre-commit. Gate CI. Prima passata veloce su una codebase grande prima di pagare il costo di `/ux-audit`. Dopo `/ux-design` o `/ux-component` per verificare la generazione.
- **Quando saltarlo:** Vuoi un fix loop (il linter riporta, non modifica — concatena con `/ux-polish --fix` o `/ux-fix`). Vuoi un giudizio di gusto (usa `/ux-critique`).
- **Invocazione (slash):** `/ux-lint src/`.
- **Invocazione (CLI):** `uxskill lint .` o `python3 bin/ux-lint.py .` o `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocazione (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Finding su stdout (posizione, id della regola, severità, evidenza). Codice di uscita 0 se pulito, diverso da zero su Critical/High quando `--fail-on high` è impostato.
- **Concatena a:** `/ux-polish --fix` → controparte LLM-driven sugli stessi pattern. `/ux-fix` → applica i finding come commit, ordinati per severità. `/ux-audit` → passata di ragionamento completa a 6 lenti. `/ux-next` → lascia decidere al conductor.

#### `/ux-audit` — audit di design a 6 lenti

- **Cosa fa:** Una review strutturata e opinata contro sei lenti (chiarezza, gerarchia, accessibilità, voce, motion, gusto), che produce finding etichettati per severità. Report in stile Polaris. Legge prima `.ux/last-frame.json` — audience e outcome ancorano la severità di ogni finding.
- **Quando usarlo:** La superficie esiste e vuoi una critica difendibile. «Audit», «rivedi la ux», «è buono questo», «cosa è rotto», «smonta questo».
- **Quando saltarlo:** La superficie non esiste ancora (usa `/ux-design`). L'utente vuole una sola lente (usa il comando mirato: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). L'utente vuole un'opinione di gusto (usa `/ux-critique`). Backend o infrastruttura.
- **Invocazione:** `/ux-audit https://example.com/pricing` o `/ux-audit src/components/Pricing.tsx`.
- **Output:** Scrive `.ux/last-audit.json` — array `findings` di `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Concatena a:** `/ux-fix` → applica i finding. `/ux-polish` → passata cosmetica. `/ux-design` → se serve un redesign strutturale.

#### `/ux-a11y` — audit WCAG 2.1 AA + verifiche di common-courtesy

- **Cosa fa:** Un audit strutturato WCAG 2.1 AA, più le verifiche di common-courtesy che superano gli strumenti automatici ma fanno comunque male agli utenti reali (visibilità del focus, specificità degli errori, preferenze di motion, trappole della tastiera, affidamento al colore).
- **Quando usarlo:** Gate di accessibilità pre-rilascio. Dopo un redesign. «Verifica accessibilità», «audit WCAG», «è accessibile questo», «revisione a11y», «test screen reader», «verifica navigazione tastiera».
- **Quando saltarlo:** Non rivolto all'utente. Backend o infrastruttura. Bozze work-in-progress.
- **Invocazione:** `/ux-a11y https://example.com` (URL live preferito — gli strumenti automatici e il test da tastiera funzionano solo su live).
- **Output:** Scrive `.ux/last-a11y.json` — array `findings` di `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Concatena a:** `/ux-fix` → applica i finding come commit. `/ux-copy` → sistema gli alt text e il wiring degli errori dei form come parte di una passata di copy.

#### `/ux-critique` — chiamata di gusto (3 vittorie, 3 mancanze, 1 mossa strategica)

- **Cosa fa:** L'opinione di un designer — non un audit strutturato, non un punteggio di severità, solo un take stretto e opinato che nomina cosa funziona, cosa no e l'unica mossa strategica che cambierebbe di più.
- **Quando usarlo:** «Cosa ne pensi», «è buono questo», «critica questo», «opinione onesta», «la vibe è giusta», «sembra nostro questo», «dovremmo rilasciare».
- **Quando saltarlo:** L'utente vuole esplicitamente un audit strutturato (usa `/ux-audit`). Backend o infrastruttura.
- **Invocazione:** `/ux-critique https://example.com`.
- **Output:** Scrive `.ux/last-critique.json` — 3 vittorie, 3 mancanze, 1 mossa strategica, più la prosa.
- **Concatena a:** `/ux-design` se il take raccomanda redesign. `/ux-polish` se il take raccomanda stringere.

#### `/ux-copy` — revisione + riscrittura della microcopy

- **Cosa fa:** Valuta ogni stringa visibile contro la rubrica della voce e produce una riscrittura before/after. Cattura: «form contains errors» (generico), «John Doe» (placeholder), copy AI-allegra celebrativa, CTA generiche, empty state morti, errori inutili.
- **Quando usarlo:** La struttura è giusta ma le parole sono deboli. «Rivedi la copy», «sistema la microcopy», «i messaggi di errore sono brutti», «riscrivi questo», «stringi le stringhe», «i bottoni suonano generici», «questo empty state è morto».
- **Quando saltarlo:** Problemi di layout (usa `/ux-audit` o `/ux-polish`). Problemi di copy guidati da accessibilità come alt text (usa `/ux-a11y`). Backend o infrastruttura.
- **Invocazione:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Scrive `.ux/last-copy.json` — array `strings` di `{location, severity, before, after, notes}`, più rubrica + locale che necessitano traduzione.
- **Concatena a:** `/ux-fix` → applica le riscritture. `/ux-a11y` → riverifica dopo i fix di copy.

### Fix e polish

#### `/ux-fix` — applica i finding come commit atomici

- **Cosa fa:** Legge l'ultimo report da `.ux/` (audit, copy, a11y, motion o polish), valida il working tree e applica i finding come commit atomici tramite i sub-agent giusti. Riverifica rieseguendo il comando originante.
- **Quando usarlo:** Dopo aver eseguito un comando di classe audit e aver rivisto i finding. «Sistema i finding», «applica i fix», «esegui il fix loop», «patcha la superficie», «fa' le modifiche», «vai a sistemarlo».
- **Quando saltarlo:** Nessun report precedente in `.ux/`. Il working tree è sporco e l'utente non ha acconsentito a stash/commit. I fix richiedono giudizio di design, non applicazione meccanica (usa `/ux-design` per un redesign).
- **Invocazione:** `/ux-fix` (rileva automaticamente quale report sistemare) o `/ux-fix --from=last-a11y.json`.
- **Output:** Commit atomici per finding. Riesegue il comando originante e aggiorna il file `.ux/last-*.json`. Stampa un riepilogo.
- **Concatena a:** `/ux-next` → il conductor sceglie la mossa successiva.

#### `/ux-polish` — passata cosmetica + uccisione dell'AI-slop

- **Cosa fa:** Ritmo di spaziatura, affilatura della gerarchia, rilevamento di AI-slop, coerenza dei token. La controparte LLM-driven di `/ux-lint` — usa il tuo giudizio sulle chiamate di gusto.
- **Quando usarlo:** La struttura è giusta ma l'esecuzione è lasca. «Polisci», «stringi questo», «rimuovi l'AI-slop», «rendilo premium», «rendilo meno AI», «la spaziatura non funziona», «sembra generico», «serve più gusto».
- **Quando saltarlo:** Alla superficie manca funzionalità core (sistema quella prima). Serve redesign, non polish (usa `/ux-design`). Problemi di copy (usa `/ux-copy`). Problemi di motion (usa `/ux-motion`). Problemi a11y (usa `/ux-a11y`).
- **Invocazione:** `/ux-polish src/components/Hero.tsx`.
- **Output:** Codice aggiornato + `.ux/last-polish.json` che descrive le modifiche.
- **Concatena a:** `/ux-lint` → verifica che il polish abbia retto. `/ux-a11y` → riverifica accessibilità.

### Discovery e narrativa

#### `/ux-frame` — blocco di framing a 4 campi

- **Cosa fa:** Cattura per-chi-è, outcome, ipotesi e segnale di successo in un blocco di framing strutturato. Nessun lavoro di design — solo l'intake a quattro campi che trasforma una richiesta vaga in un brief funzionante. Più leggero di `/ux-discover` (4 campi vs 10).
- **Quando usarlo:** All'inizio di qualsiasi progetto, sprint o ingaggio una tantum. A metà flusso quando una conversazione è andata alla deriva. «Inquadra questo», «qual è il brief», «configura il progetto», «framing».
- **Quando saltarlo:** Già inquadrato (controlla `.ux/last-frame.json`). Build di un componente una tantum senza implicazioni di framing. Backend o infrastruttura.
- **Invocazione:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Output:** Scrive `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Concatena a:** `/ux-discover` → estende il frame al brief a 10 campi. `/ux-design` → genera usando il frame come ancora.

#### `/ux-research` — pianificazione + sintesi della ricerca

- **Cosa fa:** Modalità pianificazione: scrive script di intervista, sondaggi, screener di recruitment. Modalità sintesi (`--synthesize`): digerisce interviste, analytics, siti di competitor, risultati A/B, ticket di supporto in raccomandazioni. Dispaccia `research-synthesizer`.
- **Quando usarlo:** «Pianifica uno studio di ricerca», «mi servono domande di intervista», «design un sondaggio», «come reclutare utenti», «piano di user testing», «studio diaristico», «test di preferenza», «fake door», «smoke test», «sintetizza le mie note d'intervista».
- **Quando saltarlo:** La risposta è già nota con alta confidenza. Decisioni reversibili a basso rischio. Backend o infrastruttura.
- **Invocazione:** `/ux-research --plan "loyalty wallet adoption in MENA"` o `/ux-research --synthesize interviews/*.md`.
- **Output:** Scrive `.ux/last-research.json` — piano di ricerca o temi sintetizzati + evidenze + raccomandazioni.
- **Concatena a:** `/ux-frame` → integra i finding in un frame. `/ux-design` → genera dai finding. `/ux-workshop` → conduce un workshop usando la ricerca come input.

#### `/ux-workshop` — workshop di design thinking in 5 fasi

- **Cosa fa:** Facilita un workshop di discovery / design-thinking end-to-end. Cinque fasi sequenziali (esplorazione → heat map → mappa degli stakeholder → soluzione sketch → game plan). Tempo limitato. Artefatti concreti per fase. Termina con una decisione, non «finding interessanti».
- **Quando usarlo:** Vera domanda, veri partecipanti, vero budget di tempo. «Conduci un workshop», «facilita una discovery», «facciamo una sessione di design thinking», «ho gli stakeholder per un'ora, cosa facciamo», «avvia il progetto».
- **Quando saltarlo:** Il brief è già chiaro e scopato. Brainstorm solitario (usa `/ux-design` o `/ux-frame`). Il team è a metà esecuzione, non in discovery.
- **Invocazione:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Scrive `.ux/last-workshop.json` — game plan + artefatti per fase.
- **Concatena a:** `/ux-design` → esegue il game plan. `/ux-research` → riempie i gap che il workshop ha fatto emergere. `/ux-case-study` → pubblica il viaggio.

#### `/ux-case-study` — case study pubblicabile (formato editoriale Wfrah)

- **Cosa fa:** Genera un case study di progetto in formato editoriale monocromatico puro — tipografia Wfrah, separatori hairline, codici sezione numerati (A)–(G), layout bilingue-safe. Un documento, non una brochure di marketing. Legge da `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Quando usarlo:** Post-lancio. Dopo un milestone discreto. «Scrivi un case study», «case study di questo progetto», «fa' il documento di wrap-up», «pubblica questo lavoro», «pezzo da portfolio».
- **Quando saltarlo:** Il progetto manca di dati per popolare le sezioni (A)–(G). L'utente vuole una landing marketing, non un case study (usa `/ux-design`).
- **Invocazione:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Concatena a:** Comando terminale — di solito la fine di un progetto.

### Conductor

#### `/ux-next` — conductor di workflow (read-only)

- **Cosa fa:** Legge ogni `.ux/last-*.json` e nomina il comando successivo a più alta leva. Un conductor, non un costruttore. Read-only.
- **Quando usarlo:** Tra un comando e l'altro. «Cosa dovrei fare dopo», «qual è la prossima mossa», «decidi tu», «dove andiamo da qui».
- **Quando saltarlo:** Nessun report precedente in `.ux/`. Hai un comando successivo specifico in mente.
- **Invocazione:** `/ux-next` (nessun argomento) o `/ux-next --focus=a11y`.
- **Output:** Stdout — comando successivo raccomandato + razionale.
- **Concatena a:** Qualsiasi comando scelga.

#### `/ux-expert` — hook di consulenza

- **Cosa fa:** Fa emergere le info di contatto del creatore del plugin quando un utente chiede un esperto di UX in carne e ossa. Breve, diretto, niente marketing.
- **Quando usarlo:** «Chi ha costruito questo», «mi serve un esperto di UX», «fai consulenza», «posso assumere qualcuno per questo», «c'è un umano dietro questo plugin».
- **Quando saltarlo:** L'utente sta chiedendo delle feature del plugin, non di consulenza.
- **Invocazione:** `/ux-expert`.
- **Output:** Biglietto da visita breve con LinkedIn / email / repo.

### Grafo di concatenamento dei comandi

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  blocco di framing a 4 campi
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  intake a 10 campi (FORCING GATE)
                  └────────────┬─────────┘
                               │ scrive .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 ricerche parallele -> sistema unito
                  └────────────┬─────────┘
                               │ scrive .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ scrive .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ scrive .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  applica i finding come commit
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artefatto pubblicabile
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — read-only
                  │  /ux-expert          │  hook di consulenza
                  └──────────────────────┘
```

---

## I 5 sub-agent

I sub-agent sono generatori specifici per ruolo dispacciati dai comandi. Non funzionano mai in modo indipendente — vengono chiamati da `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, ecc. Ogni agent ha un confine di responsabilità definito: NON decide il brief; esegue contro di esso.

### `frontend-engineer`

- **Possiede:** Codice frontend di livello produzione (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) con disciplina anti-AI-slop.
- **Dispacciato da:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Input:** Brief + direzione creativa + token (da `.ux/last-recommendation.json`).
- **Output:** Codice funzionante che si distingue dall'output generico dell'IA. Niente gradienti viola, niente hero centrato, niente tre card uguali, niente Inter a dimensione display, niente «John Doe», niente emoji, niente default a 300ms.
- **Strumenti:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Possiede:** Motion nel codice frontend di produzione — Framer Motion, GSAP, animazioni CSS. Durate, easing, coreografia, fallback reduced-motion, disciplina di performance.
- **Dispacciato da:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Input:** Brief di motion + token + i 57 preset di motion da `data/motion-presets.json`.
- **Output:** Motion che si guadagna il suo posto. Sempre avvolto in fallback `prefers-reduced-motion`. Sempre testato contro Core Web Vitals.
- **Strumenti:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Possiede:** Le stringhe che vengono rilasciate — messaggi di errore, empty state, CTA, stati di loading, messaggi di successo, toast, helper text, label dei form, testo dei button.
- **Dispacciato da:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Input:** Profilo di voce (nominato o incollato) + le stringhe della superficie.
- **Output:** Microcopy di produzione applicata in modo coerente su ogni stato di una superficie così che il prodotto suoni come un unico prodotto, non dieci. Vietati: «form contains errors», «John Doe», copy AI-allegra celebrativa, CTA generiche, empty state morti.
- **Strumenti:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Possiede:** Digestione degli input di ricerca (interviste, analytics, siti competitivi, risultati A/B, ticket di supporto) in raccomandazioni di design azionabili.
- **Dispacciato da:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Input:** Ricerca grezza — trascrizioni, export, URL di competitor, cluster di supporto.
- **Output:** Temi, evidenze, raccomandazioni. Non disegna mai la risposta — dà al designer il substrato da cui partire.
- **Strumenti:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Possiede:** Sistemi di design completi — token (colore, tipografia, spazio, motion, raggio, ombra), documenti di foundations, contratti di componenti, abbinamenti dark-mode, strato di theming.
- **Dispacciato da:** `/ux-system`, `/ux-component` quando non esiste un sistema.
- **Input:** Brief del brand + `.ux/last-recommendation.json` (stile + palette + abbinamento tipografico + preset di motion).
- **Output:** Un sistema coerente, opinato e pronto per la produzione su cui gli agent a valle possono costruire senza dover ridecidere i fondamentali. Token JSON, foundations MD, contratti di componenti, mapping dark-mode.
- **Strumenti:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocollo di dispacciamento dei sub-agent

Quando un comando dispaccia un sub-agent, passa:

1. Il brief / raccomandazione (caricato da `.ux/`).
2. La fetta di manifest pertinente (es. `frontend-engineer` riceve stile + palette + componenti scelti; `motion-engineer` riceve i preset di motion scelti).
3. I 152 guardrail anti-pattern (sempre attivi).
4. Un criterio di successo (cosa deve fare l'artefatto).

I sub-agent restituiscono:

1. L'artefatto (codice, doc, sistema).
2. Un blocco di razionale (perché queste scelte).
3. Un self-check contro i guardrail (quali regole hanno verificato).

Il comando chiamante esegue poi `/ux-lint` automaticamente prima di dichiarare il completamento.

---

## Gli 12 manifest di dati

Il livello dati è il cervello. Ogni comando legge da esso; il motore unisce attraverso di esso; il linter scansiona contro di esso. Tutti i file vivono sotto `data/` e avvolgono le loro voci in `{_meta, entries}` per il versioning dello schema.

### `styles.json` — 84 stili di design

| Campo | Descrizione |
|---|---|
| `entries` | 84 |
| `chiavi per voce` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categorie` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, ecc. |
| `voce di esempio` | `swiss-international` — «La griglia è legge. La tipografia fa il lavoro pesante. La decorazione è fallimento.» |

Usato da: `/ux-recommend`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 palette di colore

| Campo | Descrizione |
|---|---|
| `entries` | 176 |
| `chiavi per voce` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `toni` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, ecc. |
| `voce di esempio` | `claude-warm-editorial` — light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Usato da: `/ux-recommend`, `/ux-system`. Contrasto verificato a AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 abbinamenti tipografici

| Campo | Descrizione |
|---|---|
| `entries` | 70 |
| `chiavi per voce` | `id`, `name`, `display` (famiglia + pesi + sorgente + licenza + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `voce di esempio` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Tutte le famiglie hanno licenza + URL sorgente. Usato da `/ux-recommend`, `/ux-system`.

### `components.json` — 148 componenti

| Campo | Descrizione |
|---|---|
| `entries` | 148 |
| `chiavi per voce` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categorie` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `voce di esempio` | `mega-nav-product-grid` — Mega Navigation, Product Grid — anatomia in 6 parti, 4 stati |

Questo è il nostro più grande fossato. Nessun altro plugin UX per Claude distribuisce un manifest strutturato di componenti.

### `industries.json` — 184 regole di settore

| Campo | Descrizione |
|---|---|
| `entries` | 184 |
| `chiavi per voce` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categorie` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, ecc. |
| `voce di esempio` | `fintech-neobank` — alta fiducia, disclosure regolatorie, UI primaria di balance/transazione, mobile-first uso quotidiano |

Usato da `/ux-recommend` come primo asse di ricerca parallela.

### `chart-types.json` — 35 tipi di grafico

| Campo | Descrizione |
|---|---|
| `entries` | 35 |
| `chiavi per voce` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categorie` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `voce di esempio` | `bar-vertical` — Confronta 4–15 categorie discrete. La posizione lungo l'asse x mappa la categoria; l'altezza mappa il valore. |

Usato da `/ux-dashboard`, `/ux-component` (istanze di chart).

### `tech-stacks.json` — 25 stack

| Campo | Descrizione |
|---|---|
| `entries` | 25 |
| `chiavi per voce` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tier` | production, prerelease, experimental |
| `voce di esempio` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, compatibile con Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Altri stack includono Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 leggi UX nominate

| Campo | Descrizione |
|---|---|
| `entries` | 112 |
| `chiavi per voce` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categorie` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, ecc. |
| `voce di esempio` | `hicks-law` — Il tempo di decisione cresce logaritmicamente con il numero di scelte presentate |

Usato da `/ux-audit` (scoring a 6 lenti) e `/ux-critique` (ancora di gusto).

### `motion-presets.json` — 57 preset di motion

| Campo | Descrizione |
|---|---|
| `entries` | 57 |
| `chiavi per voce` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categorie` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `voce di esempio` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Ogni preset ha una variante reduced-motion. Codice pronto per lo stack per Framer Motion, GSAP e CSS puro.

### `anti-patterns.json` — 152 regole regex

| Campo | Descrizione |
|---|---|
| `entries` | 152 |
| `chiavi per voce` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categorie` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

L'elenco completo delle regole è in [Le 152 regole anti-AI-slop](#le-145-regole-anti-ai-slop--il-linter).

### `brands/*.json` — 160 specifiche di brand

| Campo | Descrizione |
|---|---|
| `entries` | 160 (più `_index.json` che le elenca tutte) |
| `chiavi per voce` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categorie` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Elenco completo in [Le 160 specifiche di brand DESIGN.md](#le-160-specifiche-di-brand-designmd--per-categoria).

---

## Le 152 regole anti-AI-slop — il linter

ux-skill distribuisce un linter deterministico basato su regex. **Niente LLM.** **Niente API.** **Niente rete.** Gira in CI in ~200ms su una tipica app Next.js. Esce con codice diverso da zero su finding Critical / High quando `--fail-on high` è impostato.

Le regole derivano da `data/anti-patterns.json` (v2 preferito) con un fallback `references/foundations/anti-patterns.md` (v1 bash). Vengono distribuiti due binari: `bin/ux-lint.py` (Python, veloce, estensibile) e `bin/ux-lint.sh` (Bash + perl-PCRE, per ambienti senza Python).

### Regole per categoria

#### Typography (3 regole)

| Severità | ID regola | Nome |
|---|---|---|
| high | `inter-as-display` | Inter usato come display font |
| medium | `hero-text-arbitrary-90px` | Dimensione hero font arbitraria |
| low | `font-system-only` | Stack di font di sistema senza typeface scelto |

#### Color (6 regole)

| Severità | ID regola | Nome |
|---|---|---|
| high | `purple-to-blue-gradient` | Gradiente AI di default viola-azzurro |
| high | `dark-text-on-dark-card` | Testo a basso contrasto su card |
| medium | `gradient-text-rainbow` | Testo gradiente multi-stop |
| medium | `card-glow-purple-shadow` | Ombra di glow viola sulle card |
| medium | `gradient-mesh-purple-pink` | Hero con mesh gradient viola-rosa |
| low | `tailwind-color-named-vague` | Colori Tailwind nominati senza token semantico |

#### Layout (5 regole)

| Severità | ID regola | Nome |
|---|---|---|
| high | `three-equal-card-grid` | Tre card uguali in fila |
| medium | `centered-everything-hero` | Composizione hero centrata |
| medium | `avatar-stack-overlapping` | Stack di avatar sovrapposti generico |
| low | `pill-rounded-full-everywhere` | `rounded-full` applicato a tutto |
| low | `nav-equal-hamburger-desktop` | Menu hamburger su desktop |

#### Content (5 regole)

| Severità | ID regola | Nome |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum nel codice rilasciato |
| high | `emoji-in-ui` | Emoji usata come elemento UI |
| high | `icon-emoji-stamp` | Emoji usata come timbro di icona |
| high | `testimonial-fake-five-stars` | Testimonianza con cinque stelle hardcoded |
| medium | `fake-name-john-doe` | Nomi placeholder generici |

#### Motion (3 regole)

| Severità | ID regola | Nome |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Freccia rimbalzante su CTA |
| low | `timing-300ms-default` | Timing di transizione 300ms di default |
| low | `cubic-bezier-material-only` | Easing di default Material ovunque |

#### A11y (6 regole)

| Severità | ID regola | Nome |
|---|---|---|
| high | `inline-svg-no-aria` | SVG senza aria-label o aria-hidden |
| high | `img-no-alt` | Immagine senza attributo alt |
| high | `link-onclick-no-href` | Anchor con onClick ma senza href |
| medium | `button-no-type` | Button senza attributo type |
| medium | `heading-skip-h1-h3` | Livello di heading saltato |
| medium | `infinite-scroll-no-pagination` | Scroll infinito senza fallback da tastiera |

#### Quality (6 regole)

| Severità | ID regola | Nome |
|---|---|---|
| high | `console-log-leak` | `console.log` nel codice del componente |
| medium | `inline-style-attribute` | Attributo style inline |
| medium | `any-type-leak` | Tipo `any` di TypeScript |
| medium | `arbitrary-z-index-9999` | Valore di z-index pigro |
| low | `shadcn-default-everywhere` | Blocco di token shadcn di default non modificato |
| low | `todo-fixme-comment` | TODO o FIXME nel codice rilasciato |

#### Visual (1 regola)

| Severità | ID regola | Nome |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur senza superficie glass |

### Utilizzo del linter

**Scansione una tantum:**

```bash
uxskill lint .
# oppure
python3 bin/ux-lint.py src/
# oppure
bash bin/ux-lint.sh src/
```

**Gate CI (GitHub Actions):**

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

**Output (esempio):**

```
─── report /ux-lint ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidenza: bg-gradient-to-br from-purple-500 to-blue-500
  fix: sostituisci con il gradiente primario della palette raccomandata o rimuovi il gradiente

src/components/Pricing.tsx:12  [high] three-equal-card-grid
  evidenza: grid grid-cols-3 gap-6 (3 figli Card uguali)
  fix: caratterizza una card; affiancala con due card a enfasi ridotta

3 file scansionati · 2 high · 0 medium · 0 low · exit 1
Raccomandato prossimo: /ux-polish --fix (LLM-driven, affronta sia i finding lint-abili sia quelli estetici)
```

---

## Le 160 specifiche di brand DESIGN.md — per categoria

Brand reali. Linguaggi di design reali. Specifiche DESIGN.md reali — non palette generiche. Dici al plugin «costruisci una landing nello stile di Stripe» e legge il vocabolario reale del brand: rubrica della voce, token di colore, convenzioni di motion, mosse firma, mosse vietate.

Ogni brand viene distribuito come JSON strutturato (`data/brands/<slug>.json`) più un riferimento in prosa (`references/brands/<slug>.md`).

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

### Perché conta

Gli altri 8 plugin UX popolari per Claude generano «modern minimal» o «clean dashboard» — varianti della stessa estetica di default. ux-skill ti lascia chiedere **la chiarezza di Linear**, **la serietà di Stripe**, **la sobrietà di Apple**, **il monolite di Tesla**, **la cordialità di Notion**, **la disciplina di gradiente di Cursor**, **la densità hairline di Raycast**, **l'editoriale caldo di Claude** — e il motore tira fuori i token giusti, voce, convenzioni di motion e mosse firma dalla specifica del brand.

---

## Server MCP — la mossa asimmetrica

ux-skill distribuisce un **server Model Context Protocol**. Esegui `ux-mcp` e il motore diventa un processo stdio long-running che qualsiasi host MCP-compatibile — Claude Desktop, Cursor, Windsurf, agent generici — può richiamare. Quattordici strumenti: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Stessi handler Python che usano i comandi slash; stessi manifest di dati; stesso recommender deterministico.

**Perché è la mossa asimmetrica:** nessuna delle 8 migliori skill UX per Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) distribuisce un server MCP. Sono bloccate dentro il runtime dei plugin di Claude Code. ux-skill è raggiungibile da qualsiasi host che parli MCP, inclusi agent che non hanno mai sentito parlare di un plugin di Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp è un extra opt-in
ux-mcp                                  # parte il server stdio JSON-RPC
```

Punta il tuo client al binario `ux-mcp`. La documentazione completa degli strumenti, gli esempi JSON e la config per client per Claude Desktop, Cursor e Windsurf vivono su [docs/mcp.html](docs/mcp.html) e in `commands/ux-mcp.md`.

---

## L'installatore per 17 IDE

`uxskill init` (o `/ux-init` dentro Claude Code) rileva automaticamente quale IDE stai usando e scrive l'artefatto giusto. Stesso motore Python. Stesse raccomandazioni. Collante diverso per IDE.

| IDE / Strumento | Segnale di rilevamento | Artefatto installato |
|---|---|---|
| Claude Code | `.claude/` o `CLAUDE.md` | Manifest plugin in `.claude-plugin/plugin.json` + tutti i 25 comandi + tutti i 5 sub-agent |
| Cursor | `.cursor/` o `.cursorrules` | Header prompt `.cursorrules` che punta al motore |
| Windsurf | `.windsurf/` o `.windsurfrules` | `.windsurfrules` con lo stesso header prompt |
| GitHub Copilot | `.github/copilot-instructions.md` o `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | patch `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` o `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

In ogni IDE, gli stessi comandi CLI `uxskill recommend` / `uxskill lint` / `uxskill stats` funzionano dal terminale. Il motore Python è la sorgente di verità; gli artefatti di IDE sono header di prompt sottili che instradano verso di esso.

---

## Casi d'uso — scenari concreti

Otto scenari reali. Scegli quello più vicino alla tua situazione e adatta l'invocazione.

### 1. Costruire una dashboard fintech in Cursor

Sei in Cursor a lavorare sulla dashboard di una neobank MENA. Installi il plugin ed esegui discovery, raccomandazione, poi generazione della dashboard.

```bash
pip install uxskill
uxskill init                                # rileva Cursor, scrive .cursorrules
uxskill discover                            # intake a 10 campi
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Poi in Cursor, chiedi: *«Genera la superficie dashboard usando la raccomandazione in .ux/last-recommendation.json»*. Cursor legge l'header `.cursorrules`, carica la raccomandazione, dispaccia una generazione di dashboard con vincoli espliciti.

### 2. Generare una landing in stile Stripe in Claude Code

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Tipo di progetto? landing
> Settore? fintech-payments
> Tono? serious, technical, confident
> Must have? dark-mode, AA, mobile-first
> Forbidden? purple-gradients, three-equal-cards
> Brand di riferimento? stripe
> Stack? nextjs-15-app-router
> Regione? global
> Metrica di successo? conversione signup

/ux-recommend
> [restituisce stile scelto, palette, abbinamento tipografico, preset di motion, componenti, brand esemplari]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer genera la pagina]

/ux-lint .
> [passa — la specifica del brand Stripe è stata rispettata]
```

### 3. Audit del codice esistente per AI slop in CI

Hai rilasciato un'app Next.js due settimane fa. Vuoi un floor duro contro le impronte dell'IA su ogni PR.

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

Le PR che introducono gradienti viola-azzurro, Inter a 96px, testimonianze «John Doe» o emoji come icone falliscono in CI. Nessun costo LLM. ~200ms.

### 4. Polish di una superficie esistente che «sembra generata dall'IA»

Hai ereditato un'app React che sembra ogni altro sito SaaS generato dall'IA. Vuoi farla sembrare diversa.

```
/ux-critique src/components/Hero.tsx
> [3 vittorie, 3 mancanze, 1 mossa strategica — il take è onesto]

/ux-lint src/
> [15 impronte AI di alta severità segnalate]

/ux-polish src/components/Hero.tsx
> [passata cosmetica LLM-driven + uccisione dell'AI-slop]

/ux-fix
> [applica i finding come commit atomici, riesegue il linter]
```

Tre comandi, una superficie rifinita, commit atomici per fix.

### 5. Design di una command palette in stile Linear

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [legge data/brands/linear.app.json per token + mosse firma]
> [legge data/components.json per l'anatomia + stati della command-palette]
> [dispaccia frontend-engineer con la spec Linear esplicita]
```

Il componente generato usa i token di colore reali di Linear, lo stack tipografico, le convenzioni di motion, le densità hairline — non «UI scura generica».

### 6. Eseguire un workshop di design thinking da 90 minuti con stakeholder

Hai una stanza con 5 persone per 90 minuti. Vuoi che escano con un game plan, non con una vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Il plugin facilita le cinque fasi (esplorazione → heat map → mappa stakeholder → soluzione sketch → game plan) end-to-end, tempo limitato, con artefatti concreti per fase. L'output è `.ux/last-workshop.json` — il game plan, non solo «finding interessanti».

### 7. Scrivere un case study pubblicabile dopo il lancio

Hai rilasciato il loyalty wallet. Vuoi un pezzo da portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [legge .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [genera il case study editoriale Wfrah con sezioni numerate (A)-(G), separatori hairline, layout bilingue-safe]
> [scrive case-studies/bashiti-loyalty.html]
```

Il case study è un artefatto finito e pubblicabile — non una bozza. Monocromia pura, tipografia editoriale, pronto per il rilascio al tuo portfolio.

### 8. Eseguire discovery in un contesto non-IA (solo intake strutturato)

Stai facendo lo scoping di un progetto. Non ti serve ancora una raccomandazione — ti serve un brief strutturato.

```bash
uxskill discover
# intake a 10 campi, salva in .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Puoi consegnare il JSON al tuo team, incollarlo in un documento Notion o darlo in pasto a uno strumento IA separato. ux-skill è anche uno strumento di intake strutturato oltre che un motore.

### 9. Persistenza MASTER.md — le tue decisioni di design, nel repo

Dopo `/ux-recommend`, persisti lo stile + palette + tipografia + motion + componenti + brand esemplari + guardrail scelti come file Markdown leggibile dall'umano che il tuo team può rivedere, diffare e versionare.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Scrive `.ux/design-system/MASTER.md` (frontmatter YAML + body) e `.ux/design-system/pages/<nome>.md` per superficie generata via `persist save-page`. Idempotente — lo stesso input produce output byte-identico, quindi rieseguire su stato invariato è un no-op in git.

---

## Confronto con le alternative

Tabella di riepilogo breve. Il confronto completo tabella per tabella è su [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensione | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Comandi slash | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Componenti | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Preset di motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specifiche di brand | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Regole anti-pattern | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter deterministico CI-safe | **sì** | no | no | no | no | no | no | no | no |
| IDE supportati | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Gate di discovery | **10 campi** | implicito | implicito | implicito | implicito | implicito | implicito | implicito | implicito |
| Catena di stato `.ux/` | **sì** | no | no | no | no | no | no | no | no |
| Stelle (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Valutazione onesta

- **ui-ux-pro-max** è più grande in awareness, supporta 18 IDE, ha ricerca in stile BM25 sul suo CSV. Non distribuisce manifest di componenti, manifest di motion, libreria di brand o linter deterministico.
- **open-design** ha 19 skill + preview ma solo supporto Claude Code e nessun livello anti-slop.
- **hallmark** è il più vicino in spirito (anche lui anti-slop) ma è una singola skill — niente motore, niente manifest, niente comandi concatenati.
- **material-3-skill** è eccellente se vuoi specificamente Material Design 3. Non competiamo su MD3.

Per dettaglio completo per dimensione, vedi [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Completezza del linter (Q3 2026)

- **+17 regole anti-pattern rimandate** per arrivare a 52 totali. Obiettivi: stati hover dark-on-dark, codifica di stato solo per colore, escalation di z-index ridondante, breakpoint hardcoded in JS, opacity invece di stato disabled, ecc.
- **`uxskill lint --fix` per riscritture sicure** dei finding meccanicamente correggibili (button-no-type, img-no-alt con stringa vuota, rimozione console-log-leak).
- **Estensione VS Code** che fa emergere i finding di lint inline (non c'è bisogno di eseguire CI).

### v2.2 — Espansione del manifest dei componenti (Q4 2026)

- **+50 componenti** per arrivare a 198 totali. Nuovi: combobox con filtro async, command-palette con euristica di recent-items, conditional-form-step, varianti payment-element, date picker RTL-aware, phone input specifico MENA, griglia calendario con overlay hijri.
- **Emit di codice per componente** in 6 stack (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Playground di componenti** su uxskill.laithjunaidy.com/playground — prova il motore di raccomandazione + vedi preview live dei componenti.

### v3 — Il marketplace + il lock-in (2027)

- **Marketplace di specifiche di brand** — pubblica e scopri specifiche di brand della community. Pubblicazione a pagamento per finanziare la moderazione.
- **Regole anti-pattern custom** — i progetti possono definire le proprie regole regex in `data/anti-patterns.local.json` (già distribuito in v2; v3 aggiunge discovery + condivisione).
- **`uxskill plan`** — pianificazione completa di sito multi-pagina da un brief, non solo una superficie.
- **Parità con il plugin Figma** — stesso motore di raccomandazione, emerso in Figma.

---

## Contribuire

Issue e PR benvenute. Tre aree ad alta leva:

### Aggiungere una regola anti-pattern

1. Modifica `data/anti-patterns.json` — aggiungi una voce con `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Aggiungi un test in `tests/linter/` — un file che scatena la regola, uno che no.
3. Esegui `uxskill lint tests/linter/should-trigger/<rule>.tsx` — conferma che si attivi. Esegui su `tests/linter/should-not-trigger/<rule>.tsx` — conferma che non si attivi.
4. Apri una PR.

### Aggiungere una specifica di brand

1. Crea `data/brands/<slug>.json` con `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Aggiungi la prosa corrispondente in `references/brands/<slug>.md`.
3. Registralo in `data/brands/_index.json`.
4. Apri una PR. La specifica deve essere supportata da referenze di prima fonte (il prodotto reale del brand, il sistema di design pubblico o DESIGN.md se lo pubblicano).

### Aggiungere un preset di motion

1. Modifica `data/motion-presets.json` — aggiungi una voce con `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Il preset deve avere una variante reduced-motion. Senza eccezioni.
3. Apri una PR.

### Processo

- Leggi [CONTRIBUTING.md](CONTRIBUTING.md) per il processo completo.
- Leggi [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Le nuove regole e specifiche di brand vengono riviste per: ancoraggio a prima fonte, niente overfitting su un singolo progetto, niente emoji in nessuno dei dati, comportamento RTL-safe dove applicabile.

---

## Licenza, autore, ringraziamenti

### Licenza

MIT. Usalo, forkalo, costruiscici sopra. Se ti salva dal rilasciare AI slop, metti una stella al repo — è il modo più economico di supportarlo.

### Autore

**Laith Aljunaidy** — fondatore solo di [Dot](https://thedotwallet.com), una piattaforma di loyalty MENA-first. Sta costruendo ux-skill perché il frontend generato dall'IA non sembri tutto uguale.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Sito: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Ringraziamenti

- Il team di Anthropic per Claude Code e l'architettura di skill / plugin che ha reso questo distribuibile.
- Nielsen Norman Group, Laws of UX (lawsofux.com) e la community di ricerca UX il cui lavoro informa `data/ux-guidelines.json`.
- Ogni brand elencato in `data/brands/` — i loro sistemi di design pubblici sono la sorgente di verità per le specifiche di brand.
- I contributori originali della v1: una skill Claude one-shot che è diventata il seme per il motore Python v2.
- Gli 8 plugin UX popolari per Claude con cui ci siamo confrontati — hanno alzato l'asticella; questa è la nostra risposta.

---

**ux-skill** · **v3.1.0-stable** · Costruito perché Claude Code, Cursor, Windsurf e ogni altro strumento di coding con IA emettano frontend che non si legge come generato dall'IA.

> Metti una stella al repo su [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Installa via `pip install uxskill` o `npx uxskill init` · Sfoglia il confronto su [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
