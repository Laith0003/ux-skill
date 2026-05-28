[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · **Français** · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — le moteur d'intelligence de design pour Claude Code, Cursor et tous les autres outils de codage par IA

> **Le plugin UX le plus puissant pour le codage assisté par IA.** Un noyau de raisonnement Python avec 11 manifestes JSON interrogeables (84 styles, 176 palettes, 70 appariements typographiques, 148 composants, 184 secteurs, 35 types de graphique, 57 préréglages de motion, 112 lois UX, 145 règles d'anti-patterns, 25 stacks techniques, 160 spécifications de marque), 22 commandes slash, 5 sous-agents et un linter déterministe anti-slop IA. Multi-IDE : se distribue dans Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer et Roo Cline.

> **Le nom de marque est `ux-skill`.** Le nom du paquet PyPI / npm reste `uxskill`. Le dépôt GitHub vit à [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Site :** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Comparaison face à chaque plugin UX pour Claude :** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub :** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI :** [uxskill](https://pypi.org/project/uxskill/) · **npm :** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.0.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#linstallateur-pour-17-ides)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-223_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Historique des étoiles

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Qu'est-ce que ux-skill

ux-skill est un **moteur d'intelligence de design** pour les outils de codage par IA. Il s'exécute comme paquet Python (`pip install uxskill`), comme plugin Claude Code et comme installateur multi-IDE pour 17 environnements. Le moteur ingère un brief de projet (secteur, audience, ton, indispensables, mouvements interdits, stack, région) et renvoie un système de design recommandé complet : style, palette, paire typographique, préréglages de motion, composants, marques exemplaires à étudier et les garde-fous d'anti-patterns qui doivent tenir. La recommandation est déterministe — la même entrée produit toujours la même sortie.

Le plugin se place entre vous et l'outil de codage par IA. Quand vous demandez à Claude Code, Cursor ou tout autre assistant IA de « construire une landing fintech », l'assistant improvise typiquement — et le résultat se lit comme généré par IA en cinq secondes (dégradés violet-à-bleu, trois cartes égales, Inter en taille display, « John Doe » dans les témoignages, transitions par défaut à 300 ms, hero centré, flèches rebondissantes sur les CTA). ux-skill remplace l'improvisation par des **contraintes structurées** : vous lancez `/ux-discover` pour capturer le brief, `/ux-recommend` pour choisir le système, `/ux-design` pour générer le code et `/ux-lint` pour vérifier qu'il passe les 145 règles déterministes anti-slop IA avant le commit.

Ce README est la référence canonique. Chaque commande, chaque sous-agent, chaque manifeste de données, chaque chemin d'installation, chaque spécification de marque, chaque catégorie d'anti-pattern — tout est documenté ici. Si vous cherchez un plugin de design pour Claude Code ou comparez des outils de design par IA pour Cursor, Windsurf ou Codex, lisez ceci de bout en bout et [compare.html](https://uxskill.laithjunaidy.com/compare.html) en parallèle.

---

## Table des matières

1. [Installation rapide](#installation-rapide)
2. [Les chiffres — comparaison en direct face aux 8 meilleures skills UX pour Claude](#les-chiffres--comparaison-en-direct-face-aux-8-meilleures-skills-ux-pour-claude)
3. [Architecture — comment les pièces s'emboîtent](#architecture--comment-les-pièces-semboîtent)
4. [Les 22 commandes slash — référence détaillée](#les-22-commandes-slash--référence-détaillée)
5. [Les 5 sous-agents](#les-5-sous-agents)
6. [Les 11 manifestes de données](#les-11-manifestes-de-données)
7. [Les 145 règles anti-slop IA — le linter](#les-145-règles-anti-slop-ia--le-linter)
8. [Les 160 spécifications de marque DESIGN.md — par catégorie](#les-160-spécifications-de-marque-designmd--par-catégorie)
9. [Serveur MCP — le coup asymétrique](#serveur-mcp--le-coup-asymétrique)
10. [L'installateur pour 17 IDEs](#linstallateur-pour-17-ides)
11. [Cas d'usage — scénarios concrets](#cas-dusage--scénarios-concrets)
12. [Face aux alternatives](#face-aux-alternatives)
13. [Feuille de route](#feuille-de-route)
14. [Contribuer](#contribuer)
15. [Licence, auteur, remerciements](#licence-auteur-remerciements)

---

## Installation rapide

Trois voies d'installation. Choisissez celle qui correspond à votre environnement.

### Voie 1 — marketplace Claude Code (canonique)

Si vous travaillez dans Claude Code, installez via le marketplace de plugins :

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Cela branche les 22 commandes slash et les 5 sous-agents à votre session Claude Code. Après l'installation, lancez `/ux-init` pour configurer le répertoire d'état `.ux/` propre au projet et vérifier que le moteur Python est accessible.

### Voie 2 — pip (universelle)

Si vous travaillez hors de Claude Code (Cursor, Windsurf, CLI, CI), installez le paquet Python :

```bash
pip install uxskill
uxskill init                       # détecte automatiquement votre IDE, installe le bon artefact
uxskill stats                      # affiche les compteurs des manifestes pour vérifier l'installation
uxskill lint .                     # lance le linter sur le répertoire courant
```

Le paquet expose à la fois `ux` et `uxskill` comme points d'entrée CLI — c'est le même binaire.

### Voie 3 — npx (sans Python requis)

Si vous ne voulez pas gérer Python directement, le wrapper npx amorce tout via `pipx` :

```bash
npx uxskill init                  # télécharge pipx + uxskill au premier lancement
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Vérifier l'installation

```bash
ux stats
# {
#   "version": "3.0.0-stable",
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

Si l'un des compteurs renvoie 0, c'est qu'un fichier JSON manque — ouvrez une issue sur [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Les chiffres — comparaison en direct face aux 8 meilleures skills UX pour Claude

Les compteurs d'étoiles ont été vérifiés pour la dernière fois via `gh api` le **2026-05-28**. ux-skill (Laith0003/ux-skill) est le dernier entrant — nous sommes minuscules en notoriété, profonds en architecture. La comparaison ci-dessous est honnête : où nous perdons, où nous gagnons.

| Plugin | Étoiles | Architecture | Commandes slash | Linter (compatible CI) | Specs de marque | Composants | Préréglages motion | IDEs pris en charge |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83 958** | Python BM25 + CSV, skill unique | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54 406** | Node.js + 19 skills + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25 202** | Bash + goût adossé à la recherche | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15 455** | Unique SKILL.md de 62 Ko + scripts | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5 762** | Bibliothèque de skills câblée MCP | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2 391** | Skill mono-esthétique | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2 164** | Skill de design anti-slop | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Composants MD3 + audit | 1 | — | — | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Moteur Python + 11 manifestes + 22 commandes + 5 sous-agents + linter CI** | **22** | **145 règles regex** | **160** | **148** | **57** | **17** |

### Où nous perdons

- **Notoriété.** Eux ont des centaines de milliers d'étoiles. Nous en avons 14. Mettez-nous une étoile — c'est la façon la moins chère d'aider.
- **Reconnaissance de marque.** ui-ux-pro-max et open-design ont une avance qui se mesure en mois, pas en jours.
- **Finition marketing.** Ils ont des captures, des vidéos de démo et une landing découvrable. Nous avons un README exhaustif et une landing modeste.

### Où nous gagnons

- **Bibliothèque de composants :** 148 composants documentés avec anatomie, états, tokens utilisés et specs de motion. Aucun des 8 autres ne livre de manifeste de composants.
- **Préréglages de motion :** 57 entrées prêtes par stack (Framer Motion, GSAP, CSS) avec fallbacks reduced-motion. Aucun des autres ne livre de manifeste de motion.
- **Linter d'anti-patterns :** 145 règles regex déterministes, tourne en CI, sort en non-zéro sur Critical/High. Aucun des autres ne livre de linter déterministe.
- **Specs de marque :** 160 véritables specs DESIGN.md (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude et 96 autres). Aucun des autres ne livre de bibliothèque de marques.
- **17 IDEs pris en charge :** même moteur, glue différente par IDE.
- **22 commandes slash :** discovery, génération, audit, lint, polish, boucle de fix, étude de cas, atelier, copy, motion, a11y, dashboard, conductor — intégrées de bout en bout.

Tableau complet côte à côte sur [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Architecture — comment les pièces s'emboîtent

```
ux-skill (nom du paquet : uxskill)
│
├── data/                              Le cerveau — manifestes JSON interrogeables
│   ├── styles.json                    84 styles de design + when/skip + tokens
│   ├── palettes.json                  176 palettes (clair/sombre, contraste vérifié)
│   ├── type-pairs.json                70 triplets display × body × mono
│   ├── components.json                148 composants (anatomie, états, motion)
│   ├── industries.json                184 règles sectorielles + signaux d'audience
│   ├── chart-types.json               35 types de graphique (when/skip, encoding)
│   ├── tech-stacks.json               25 stacks (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 lois UX nommées (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 préréglages de motion (entrée, sortie, hover...)
│   ├── anti-patterns.json             145 règles regex (source du linter compatible CI)
│   └── brands/*.json                  160 specs DESIGN de marque + _index.json
│
├── engine/                            Python — le raisonnement
│   ├── recommender/                   moteur de fusion à 5 recherches parallèles
│   ├── linter/                        scanner anti-slop déterministe
│   ├── discovery/                     protocole forçant à 10 champs
│   ├── generator/                     émetteur de tokens + manifestes
│   ├── installer/                     installateur multi-IDE pour 17 environnements
│   └── cli/                           point d'entrée `ux` / `uxskill`
│
├── commands/                          22 commandes slash Claude Code (.md)
│   ├── ux-init.md                     amorçage
│   ├── ux-stats.md                    instantané d'inventaire
│   ├── ux-discover.md                 intake de 10 champs (porte)
│   ├── ux-recommend.md                PRODUIT PHARE — 5 recherches parallèles
│   ├── ux-lint.md                     linter déterministe
│   ├── ux-design.md                   génère du code frontend
│   ├── ux-component.md                génère un composant
│   ├── ux-system.md                   génère un système de design complet
│   ├── ux-dashboard.md                génère une surface dashboard
│   ├── ux-motion.md                   traitement de motion + audit
│   ├── ux-audit.md                    audit de design à 6 lentilles
│   ├── ux-a11y.md                     audit WCAG 2.1 AA
│   ├── ux-critique.md                 critique de goût (3 réussites, 3 ratés, 1 coup)
│   ├── ux-copy.md                     revue + réécriture microcopy
│   ├── ux-fix.md                      applique les findings en commits atomiques
│   ├── ux-polish.md                   passe cosmétique + élimination du slop IA
│   ├── ux-frame.md                    bloc de framing à 4 champs
│   ├── ux-research.md                 planification + synthèse de recherche
│   ├── ux-workshop.md                 atelier de design thinking en 5 phases
│   ├── ux-case-study.md               étude de cas publiable format éditorial Wfrah
│   ├── ux-next.md                     conducteur de workflow (lecture seule)
│   └── ux-expert.md                   crochet de conseil
│
├── agents/                            5 sous-agents (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy dans la voix de la marque
│   ├── research-synthesizer.md        entretiens + analytics + concurrents
│   └── design-system-architect.md     tokens / composants / fondations
│
├── references/                        Source en prose des données + pages de démo
│   ├── foundations/                   anti-patterns.md, principes, goût
│   ├── laws/                          lois UX format long
│   ├── process/                       discovery-protocol.md (portant)
│   ├── styles/                        prose par style (anti-slop.md, etc.)
│   ├── components/                    composants format long
│   ├── output/                        rubriques de sortie
│   └── conditional/                   guidance spécifique par stack
│
├── bin/
│   ├── uxskill.mjs                    wrapper npx -> moteur Python
│   ├── ux-lint.py                     linter v2 (préféré)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (créé par projet)
    ├── last-discovery.json            instantané du brief
    ├── last-recommendation.json       système choisi
    ├── last-frame.json                bloc de framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Comment le moteur fonctionne réellement

1. **Entrée.** Vous fournissez un brief — soit interactivement via `/ux-discover` (10 champs), soit non interactivement via flags à `ux recommend`.
2. **5 recherches parallèles.** Le moteur lance cinq lookups concurrents à travers les manifestes :
   - **Secteur → styles_recommandés** (industries.json)
   - **Style → compatibilité palette + typographie + motion** (styles.json)
   - **Ton × indispensable → filtre de palette** (palettes.json)
   - **Stack → compatibilité composants + préréglages motion** (tech-stacks.json, motion-presets.json)
   - **Interdit + région → garde-fous + shortlist de marques exemplaires** (anti-patterns.json, brands/)
3. **Fusion.** Un fusionneur déterministe classe les candidats, résout les conflits (par ex. un indispensable dark-mode force le mode de palette) et émet un système recommandé unique.
4. **Sortie.** Un document JSON avec le style choisi, la palette choisie, la paire typographique, les 5 meilleurs préréglages motion, les 12 meilleurs composants, les 5 meilleures marques exemplaires et les 35 garde-fous d'anti-patterns actifs. Plus un bloc de justification expliquant chaque choix.
5. **Génération.** Les commandes en aval (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) consomment la recommandation pour générer du code réel via les sous-agents.
6. **Vérification.** `/ux-lint` rescanne le code généré contre les 145 règles regex. Sort en non-zéro sur Critical/High en CI.

**Python pense. HTML montre. Markdown enchaîne.**

---

## Les 22 commandes slash — référence détaillée

Chaque commande est livrée comme fichier `.md` sous `commands/` avec `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` et `output state file`. Les descriptions ci-dessous sont condensées ; la source complète est la spec canonique.

Les commandes sont regroupées en cinq catégories : **amorçage et inventaire**, **discovery et recommandation**, **génération**, **audit et vérification**, **fix et polish**, et **conductor**.

### Amorçage et inventaire

#### `/ux-init` — amorcer le projet

- **Quoi :** Détecte l'IDE que vous utilisez (`.claude/`, `.cursor/`, `.windsurf/`, etc.), installe le bon artefact, vérifie que le moteur Python est accessible, affiche un instantané des stats.
- **Quand l'utiliser :** Première installation dans un nouveau projet. Après avoir cloné un projet qui utilise ux-skill. Après `pip install --upgrade uxskill`.
- **Quand passer :** Vous l'avez déjà lancé dans ce projet et rien n'a changé.
- **Invocation :** `/ux-init` (sans args) ou `uxskill init` depuis la CLI.
- **Sortie :** Artefact par IDE (voir [L'installateur pour 17 IDEs](#linstallateur-pour-17-ides)) + répertoire `.ux/` + résumé stdout.
- **Enchaîne avec :** `/ux-discover` ensuite.

#### `/ux-stats` — afficher l'inventaire des données

- **Quoi :** Affiche la version + les compteurs d'entrées pour les 11 manifestes de données, pour que vous puissiez vérifier ce qui est installé.
- **Quand l'utiliser :** Après l'installation. Après une mise à jour. Quand `/ux-recommend` renvoie des choix surprenants et que vous soupçonnez les manifestes d'être incomplets.
- **Quand passer :** Jamais — c'est une commande lecture seule de 50 ms.
- **Invocation :** `/ux-stats` ou `uxskill stats`.
- **Sortie :** JSON vers stdout (voir [Vérifier l'installation](#vérifier-linstallation) plus haut).
- **Enchaîne avec :** Diagnostic uniquement ; n'alimente rien en aval.

### Discovery et recommandation

#### `/ux-discover` — la fonction forçante (intake à 10 champs)

- **Quoi :** L'intake obligatoire de 10 champs que traverse chaque projet avant toute commande de génération. Type de projet, audience, objectif principal, ton, indispensables, interdits, marques de référence, stack, région, métrique de succès. **Pas d'improvisation.** Des phrases bannies (« moderne », « clean ») forcent l'utilisateur à être spécifique.
- **Quand l'utiliser :** Avant tout `/ux-design`, `/ux-component`, `/ux-system` ou `/ux-dashboard`. Chaque fois qu'un brief précédent est devenu obsolète.
- **Quand passer :** Vous corrigez un bug (`/ux-fix`). Vous lancez uniquement une passe linter (`/ux-lint`). Le brief n'a pas changé depuis la dernière session.
- **Invocation :** `/ux-discover`. Le plugin demande ; vous répondez.
- **Sortie :** Écrit `.ux/last-discovery.json` (le brief à 10 champs).
- **Enchaîne avec :** `/ux-recommend` → utilise la discovery pour choisir style + palette + typographie + motion + composants. `/ux-design [brief supplémentaire]` → génère du code frontend ancré sur la recommandation. `/ux-component <nom>` → génère un composant aligné aux contraintes découvertes.

#### `/ux-recommend` — le moteur phare à 5 recherches parallèles

- **Quoi :** Lance les 5 recherches parallèles du moteur Python à travers les 11 manifestes et renvoie un seul système de design fusionné. Secteur → Style → Palette → Typographie → Motion + Composants + Marques exemplaires + Garde-fous.
- **Quand l'utiliser :** Démarrer un nouveau projet à partir de zéro. Pivoter un produit fatigué. Pré-vol avant tout `/ux-design` ou `/ux-component`.
- **Quand passer :** Vous avez déjà lancé `/ux-discover` et enregistré un brief — `/ux-recommend` est automatique dans ce flux. Vous corrigez un bug (utilisez `/ux-fix`). Vous avez juste besoin de linter (utilisez `/ux-lint`).
- **Invocation (Claude Code) :**
  ```
  /ux-recommend
  ```
  **Invocation (CLI) :**
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
- **Sortie :** Écrit `.ux/last-recommendation.json` — style choisi, palette choisie, paire typographique choisie, 5 meilleurs préréglages motion, 12 meilleurs composants, 5 meilleures marques exemplaires, les 35 garde-fous d'anti-patterns actifs, plus justification.
- **Enchaîne avec :** `/ux-design [brief]` → code frontend utilisant les tokens recommandés. `/ux-system` → système de design complet à partir de la recommandation. `/ux-component <nom>` → un composant utilisant le style recommandé. `/ux-lint` → vérifier le code généré.

### Génération

#### `/ux-design` — générer une surface élégante et anti-slop depuis un brief

- **Quoi :** Génère un artefact frontend complet, de qualité production (landing, site marketing, app shell) à partir du brief de discovery + recommandation. Dépêche `frontend-engineer` avec une direction créative issue des références anti-slop et arsenal.
- **Quand l'utiliser :** « Dessine un », « construis-moi un », « génère une landing page », « crée un dashboard », « fais un composant » — toute demande de livrable visuel en format libre.
- **Quand passer :** Vous voulez une revue, pas une construction (utilisez `/ux-audit` ou `/ux-critique`). Vous voulez un seul composant (utilisez `/ux-component`). Travail backend ou infrastructure.
- **Invocation :** `/ux-design génère une landing fintech pour une néobanque MENA, ton chaleureux éditorial, dark-mode AA, pas de dégradés violets`.
- **Sortie :** Code généré (HTML / Blade / JSX / Vue / Astro), plus `.ux/last-design.json`.
- **Enchaîne avec :** `/ux-lint` → vérifier contre les garde-fous. `/ux-polish` → passe cosmétique. `/ux-a11y` → audit d'accessibilité. `/ux-copy` → revue microcopy. `/ux-fix` → appliquer les findings en commits atomiques.

#### `/ux-component` — générer un composant

- **Quoi :** Produit un composant unique de qualité production (bouton, modal, navbar, sidebar, carte, table, formulaire, graphique) à partir d'une spec. Les quatre états d'interaction, accessible, fidèle à la marque. Cherche d'abord le composant dans `.ux/last-recommendation.json`, retombe sur une requête directe au manifeste.
- **Quand l'utiliser :** Toute demande d'élément unique — « construis un bouton », « crée une carte de tarification », « fais un modal », « ajoute un navbar », « dessine un sidebar », « j'ai besoin d'une table de données », « construis un formulaire », « fais un composant de graphique ».
- **Quand passer :** Page complète ou surface multi-sections (utilisez `/ux-design`). Backend ou infrastructure.
- **Invocation :** `/ux-component pricing-card-trio --brief="fintech, sombre, chiffres monospace"`.
- **Sortie :** Code du composant généré, plus `.ux/last-component.json`.
- **Enchaîne avec :** `/ux-lint` → vérifier. `/ux-polish` → resserrer.

#### `/ux-system` — générer un système de design starter complet

- **Quoi :** Propose un système de design starter complet pour un projet qui n'en a pas — tokens (couleur, typographie, espace, motion, rayon, ombre), docs de fondations, contrats de composants, appariements dark-mode, switcher de thème. Dépêche `design-system-architect`.
- **Quand l'utiliser :** « On n'a pas de système de design », « construis-nous un système », « propose des tokens », « quel devrait être notre thème », « monte notre DS ».
- **Quand passer :** Le projet a déjà un système de design — utilisez plutôt `/ux-component` contre le système existant. Backend ou infrastructure.
- **Invocation :** `/ux-system` (lance la discovery d'abord si pas déjà en place).
- **Sortie :** `tokens.json`, `foundations.md`, contrats `components/*.md`, émission Tailwind / vanilla / SCSS optionnelle. Écrit `.ux/last-system.json` pour le contexte d'enchaînement.
- **Enchaîne avec :** `/ux-component` → construire contre le nouveau système. `/ux-design` → générer une surface utilisant les nouveaux tokens.

#### `/ux-dashboard` — génération spécialisée de dashboard

- **Quoi :** Dashboard avec discipline de densité de données — layout bento, chiffres monospace tabulaires, patterns de sparkline, anti-abus de cartes, couleurs sémantiques d'état, motion parcimonieuse. Pas un site marketing avec des graphiques collés dessus.
- **Quand l'utiliser :** « Construis un dashboard », « dessine le panneau admin », « fais une page de métriques », « console opérateur », « vue analytique », « tableau KPI », « écran de monitoring ».
- **Quand passer :** Landing marketing avec stats (utilisez `/ux-design`). Un seul widget (utilisez `/ux-component`). Backend ou infrastructure.
- **Invocation :** `/ux-dashboard`.
- **Sortie :** Code de dashboard généré + `.ux/last-dashboard.json`.
- **Enchaîne avec :** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — traitement de motion

- **Quoi :** Génère la couche motion d'une surface — durées, easings, chorégraphie, fallbacks reduced-motion, discipline de performance. Audite également la motion existante contre les 5 dimensions (timing, easing, signification, reduced-motion, performance).
- **Quand l'utiliser :** « Contrôle de motion », « les animations sont-elles bonnes », « corrige la motion », « revois les animations », « audit motion », « passe perf sur la motion ».
- **Quand passer :** La surface n'a pas de motion (utilisez `/ux-audit` ou `/ux-polish`). Backend ou infrastructure.
- **Invocation :** `/ux-motion path/to/component.tsx` (mode audit) ou `/ux-motion --generate hero-entry` (génération).
- **Sortie :** Code mis à jour (en mode génération) ou rapport `.ux/last-motion.json` (en mode audit).
- **Enchaîne avec :** `/ux-fix` → appliquer les findings de motion. `/ux-polish` → resserrer.

### Audit et vérification

#### `/ux-lint` — linter déterministe à base de regex (sans LLM, compatible CI)

- **Quoi :** Lance 145 règles regex contre votre code. Aucun appel LLM. Sort en non-zéro sur Critical / High en CI. Source : `data/anti-patterns.json`. Les règles couvrent A11y (23), Contenu (15), Layout (13), Typographie (10), Couleur (9), Qualité (9), Visuel (9), Motion (8), Performance (4).
- **Quand l'utiliser :** Hook pre-commit. Porte de CI. Première passe rapide sur une grosse codebase avant de payer le coût d'`/ux-audit`. Après `/ux-design` ou `/ux-component` pour vérifier la génération.
- **Quand passer :** Vous voulez une boucle de fix (le linter rapporte, il n'édite pas — enchaînez sur `/ux-polish --fix` ou `/ux-fix`). Vous voulez un jugement de goût (utilisez `/ux-critique`).
- **Invocation (slash) :** `/ux-lint src/`.
- **Invocation (CLI) :** `uxskill lint .` ou `python3 bin/ux-lint.py .` ou `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocation (CI) :**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Sortie :** Findings vers stdout (emplacement, id de règle, sévérité, preuve). Code de sortie 0 si propre, non-zéro sur Critical/High quand `--fail-on high` est posé.
- **Enchaîne avec :** `/ux-polish --fix` → contrepartie LLM sur les mêmes patterns. `/ux-fix` → applique les findings comme commits, triés par sévérité. `/ux-audit` → passe de raisonnement complète à 6 lentilles. `/ux-next` → laisser le conducteur décider.

#### `/ux-audit` — audit de design à 6 lentilles

- **Quoi :** Une revue structurée et opiniâtre contre six lentilles (clarté, hiérarchie, accessibilité, voix, motion, goût), produisant des findings étiquetés par sévérité. Rapport style Polaris. Lit d'abord `.ux/last-frame.json` — l'audience et l'outcome ancrent la sévérité de chaque finding.
- **Quand l'utiliser :** La surface existe et vous voulez une critique défendable. « Audit », « revois l'UX », « est-ce bon », « qu'est-ce qui cloche », « démonte-le ».
- **Quand passer :** La surface n'existe pas encore (utilisez `/ux-design`). L'utilisateur veut une seule lentille (utilisez la commande ciblée : `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). L'utilisateur veut une opinion de goût (utilisez `/ux-critique`). Backend ou infrastructure.
- **Invocation :** `/ux-audit https://example.com/pricing` ou `/ux-audit src/components/Pricing.tsx`.
- **Sortie :** Écrit `.ux/last-audit.json` — tableau `findings` de `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Enchaîne avec :** `/ux-fix` → appliquer les findings. `/ux-polish` → passe cosmétique. `/ux-design` → si refonte structurelle nécessaire.

#### `/ux-a11y` — audit WCAG 2.1 AA + vérifications de courtoisie élémentaire

- **Quoi :** Un audit WCAG 2.1 AA structuré, plus les vérifications de courtoisie élémentaire qui passent les outils automatiques mais blessent encore les vrais utilisateurs (visibilité du focus, spécificité des erreurs, préférences de motion, pièges clavier, dépendance à la couleur).
- **Quand l'utiliser :** Porte d'accessibilité pré-livraison. Après une refonte. « Contrôle d'accessibilité », « audit WCAG », « est-ce accessible », « revue a11y », « test lecteur d'écran », « contrôle de navigation clavier ».
- **Quand passer :** Pas orienté utilisateur. Backend ou infrastructure. Esquisses en cours.
- **Invocation :** `/ux-a11y https://example.com` (URL en direct préférée — les outils automatiques et le test clavier ne fonctionnent qu'en direct).
- **Sortie :** Écrit `.ux/last-a11y.json` — tableau `findings` de `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, tableau `beyond_wcag`, `severity_counts`.
- **Enchaîne avec :** `/ux-fix` → appliquer les findings en commits. `/ux-copy` → corriger les alt text et le câblage des erreurs de formulaire dans le cadre d'une passe copy.

#### `/ux-critique` — opinion de goût (3 réussites, 3 ratés, 1 coup stratégique)

- **Quoi :** L'opinion d'un designer — pas un audit structuré, pas un score de sévérité, juste une prise serrée et opiniâtre qui nomme ce qui marche, ce qui ne marche pas, et le seul coup stratégique qui changerait le plus.
- **Quand l'utiliser :** « Qu'est-ce que tu en penses », « c'est bon », « critique-moi ça », « avis honnête », « le vibe est juste », « ça nous ressemble », « on devrait expédier ».
- **Quand passer :** L'utilisateur veut explicitement un audit structuré (utilisez `/ux-audit`). Backend ou infrastructure.
- **Invocation :** `/ux-critique https://example.com`.
- **Sortie :** Écrit `.ux/last-critique.json` — 3 réussites, 3 ratés, 1 coup stratégique, plus de la prose.
- **Enchaîne avec :** `/ux-design` si la prise recommande la refonte. `/ux-polish` si la prise recommande de resserrer.

#### `/ux-copy` — revue + réécriture microcopy

- **Quoi :** Évalue chaque chaîne visible contre la rubrique de voix et produit une réécriture avant/après. Attrape : « le formulaire contient des erreurs » (générique), « John Doe » (placeholder), copy célébratoire enjoué d'IA, CTAs génériques, empty states morts, erreurs inutiles.
- **Quand l'utiliser :** La structure est bonne mais les mots sont faibles. « Revois le copy », « corrige le microcopy », « les messages d'erreur sont mauvais », « réécris-moi ça », « resserre les chaînes », « les boutons sonnent génériques », « cet empty state est mort ».
- **Quand passer :** Problèmes de layout (utilisez `/ux-audit` ou `/ux-polish`). Problèmes de copy liés à l'accessibilité comme les alt text (utilisez `/ux-a11y`). Backend ou infrastructure.
- **Invocation :** `/ux-copy src/views/checkout.blade.php`.
- **Sortie :** Écrit `.ux/last-copy.json` — tableau `strings` de `{location, severity, before, after, notes}`, plus rubrique + locales à traduire.
- **Enchaîne avec :** `/ux-fix` → appliquer les réécritures. `/ux-a11y` → recontrôler après les corrections de copy.

### Fix et polish

#### `/ux-fix` — appliquer les findings en commits atomiques

- **Quoi :** Lit le dernier rapport de `.ux/` (audit, copy, a11y, motion ou polish), valide l'arbre de travail et applique les findings comme commits atomiques via les bons sous-agents. Re-vérifie en relançant la commande d'origine.
- **Quand l'utiliser :** Après avoir lancé une commande de classe audit et passé en revue les findings. « Corrige les findings », « applique les fix », « lance la boucle de fix », « patche la surface », « fais les changements », « va corriger ça ».
- **Quand passer :** Pas de rapport préalable dans `.ux/`. L'arbre de travail est sale et l'utilisateur n'a pas accepté de stash/commit. Les fix demandent du jugement de design, pas une application mécanique (utilisez `/ux-design` pour une refonte).
- **Invocation :** `/ux-fix` (auto-détecte le rapport à corriger) ou `/ux-fix --from=last-a11y.json`.
- **Sortie :** Commits atomiques par finding. Relance la commande d'origine et met à jour le fichier `.ux/last-*.json`. Affiche un résumé.
- **Enchaîne avec :** `/ux-next` → le conducteur choisit le prochain coup.

#### `/ux-polish` — passe cosmétique + élimination du slop IA

- **Quoi :** Rythme de l'espacement, affûtage de la hiérarchie, détection de slop IA, cohérence des tokens. La contrepartie pilotée par LLM à `/ux-lint` — utilise votre jugement sur les décisions de goût.
- **Quand l'utiliser :** La structure est bonne mais l'exécution est lâche. « Polis ça », « resserre », « enlève le slop IA », « rends-le premium », « rends-le moins genre IA », « l'espacement sonne faux », « ça paraît générique », « il faut plus de goût ».
- **Quand passer :** La surface manque de fonctionnalité centrale (corrigez ça d'abord). Refonte nécessaire, pas polish (utilisez `/ux-design`). Problèmes de copy (utilisez `/ux-copy`). Problèmes de motion (utilisez `/ux-motion`). Problèmes a11y (utilisez `/ux-a11y`).
- **Invocation :** `/ux-polish src/components/Hero.tsx`.
- **Sortie :** Code mis à jour + `.ux/last-polish.json` décrivant les changements.
- **Enchaîne avec :** `/ux-lint` → vérifier que le polish a tenu. `/ux-a11y` → recontrôler l'accessibilité.

### Discovery et narration

#### `/ux-frame` — bloc de framing à 4 champs

- **Quoi :** Capture le pour-qui, l'outcome, l'hypothèse et le signal de succès dans un bloc de framing structuré. Aucun travail de design ne se produit — juste l'intake à quatre champs qui transforme une demande vague en brief de travail. Plus léger que `/ux-discover` (4 champs contre 10).
- **Quand l'utiliser :** Démarrage de tout projet, sprint ou mission ponctuelle. En milieu de course quand une conversation a dérivé. « Cadre ça », « c'est quoi le brief », « monte le projet », « framing ».
- **Quand passer :** Déjà cadré (vérifiez `.ux/last-frame.json`). Construction de composant ponctuel sans implication de cadrage. Backend ou infrastructure.
- **Invocation :** `/ux-frame "wallet de fidélité pour le pilote MENA Bashiti"`.
- **Sortie :** Écrit `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Enchaîne avec :** `/ux-discover` → étendre le cadre au brief à 10 champs. `/ux-design` → générer en utilisant le cadre comme ancre.

#### `/ux-research` — planification + synthèse de recherche

- **Quoi :** Mode planification : rédige scripts d'entretien, sondages, filtres de recrutement. Mode synthèse (`--synthesize`) : digère entretiens, analytics, sites concurrents, résultats A/B, tickets de support en recommandations. Dépêche `research-synthesizer`.
- **Quand l'utiliser :** « Planifie une étude de recherche », « j'ai besoin de questions d'entretien », « dessine un sondage », « comment je recrute des users », « plan de user testing », « étude journal », « test de préférence », « fake door », « smoke test », « synthétise mes notes d'entretien ».
- **Quand passer :** La réponse est déjà connue avec haute confiance. Décisions réversibles à faible risque. Backend ou infrastructure.
- **Invocation :** `/ux-research --plan "adoption de wallet de fidélité au MENA"` ou `/ux-research --synthesize interviews/*.md`.
- **Sortie :** Écrit `.ux/last-research.json` — plan de recherche ou thèmes synthétisés + preuves + recommandations.
- **Enchaîne avec :** `/ux-frame` → intégrer les findings dans un cadre. `/ux-design` → générer à partir des findings. `/ux-workshop` → animer un atelier en utilisant la recherche comme entrée.

#### `/ux-workshop` — atelier de design thinking en 5 phases

- **Quoi :** Anime un atelier discovery / design thinking de bout en bout. Cinq phases séquentielles (exploration → carte de chaleur → carte des acteurs → croquis de solution → plan de jeu). Chronométré. Artefacts concrets par phase. Se termine par une décision, pas par « findings intéressants ».
- **Quand l'utiliser :** Vraie question, vrais participants, vrai budget temps. « Anime un atelier », « facilite un discovery », « faisons une session de design thinking », « j'ai des stakeholders pendant une heure, qu'est-ce qu'on fait », « lance le projet ».
- **Quand passer :** Brief déjà clair et cadré. Brainstorm solo (utilisez `/ux-design` ou `/ux-frame`). L'équipe est en pleine exécution, pas en discovery.
- **Invocation :** `/ux-workshop "pivot wallet de fidélité" --participants="2 PMs, 1 designer, 1 lead eng, 1 client representative" --minutes=90`.
- **Sortie :** Écrit `.ux/last-workshop.json` — plan de jeu + artefacts par phase.
- **Enchaîne avec :** `/ux-design` → exécuter le plan de jeu. `/ux-research` → combler les manques que l'atelier a fait remonter. `/ux-case-study` → publier le parcours.

#### `/ux-case-study` — étude de cas publiable (format éditorial Wfrah)

- **Quoi :** Génère une étude de cas de projet en format éditorial monochrome pur — typographie Wfrah, séparateurs filaires, codes de section numérotés (A)–(G), layout bilingue-safe. Un document, pas une brochure marketing. Lit depuis `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Quand l'utiliser :** Post-lancement. Après un jalon discret. « Écris une étude de cas », « étude de cas ce projet », « fais le doc de clôture », « publie ce travail », « pièce portfolio ».
- **Quand passer :** Le projet manque de données pour peupler les sections (A)–(G). L'utilisateur veut une landing marketing, pas une étude de cas (utilisez `/ux-design`).
- **Invocation :** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Sortie :** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Enchaîne avec :** Commande terminale — généralement la fin d'un projet.

### Conductor

#### `/ux-next` — conducteur de workflow (lecture seule)

- **Quoi :** Lit chaque `.ux/last-*.json` et nomme la prochaine commande au plus fort effet de levier. Un conducteur, pas un constructeur. Lecture seule.
- **Quand l'utiliser :** Entre deux commandes. « Qu'est-ce que je devrais faire ensuite », « quel est le prochain coup », « décide pour moi », « on va où à partir d'ici ».
- **Quand passer :** Pas de rapports préalables dans `.ux/`. Vous avez une commande suivante précise en tête.
- **Invocation :** `/ux-next` (sans args) ou `/ux-next --focus=a11y`.
- **Sortie :** Stdout — commande recommandée + justification.
- **Enchaîne avec :** Celle qu'il choisit.

#### `/ux-expert` — crochet de conseil

- **Quoi :** Fait remonter les coordonnées du créateur du plugin quand un utilisateur demande un véritable expert UX. Bref, direct, sans marketing.
- **Quand l'utiliser :** « Qui a construit ça », « j'ai besoin d'un expert UX », « tu fais du conseil », « je peux engager quelqu'un pour ça », « il y a un humain derrière ce plugin ».
- **Quand passer :** L'utilisateur pose une question sur les fonctionnalités du plugin, pas sur le conseil.
- **Invocation :** `/ux-expert`.
- **Sortie :** Carte de contact brève avec LinkedIn / email / dépôt.

### Graphe d'enchaînement des commandes

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  bloc de framing à 4 champs
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  intake à 10 champs (PORTE FORÇANTE)
                  └────────────┬─────────┘
                               │ écrit .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 recherches parallèles -> système fusionné
                  └────────────┬─────────┘
                               │ écrit .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ écrit .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ écrit .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  applique les findings en commits
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artefact publiable
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conducteur — lecture seule
                  │  /ux-expert          │  crochet de conseil
                  └──────────────────────┘
```

---

## Les 5 sous-agents

Les sous-agents sont des générateurs spécifiques par rôle dépêchés par les commandes. Ils ne tournent jamais de manière indépendante — ils sont appelés par `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Chaque agent a un périmètre de propriété défini : ils NE décident PAS du brief ; ils l'exécutent.

### `frontend-engineer`

- **Possède :** Le code frontend de qualité production (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) avec discipline anti-slop IA.
- **Dépêché par :** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Entrées :** Brief + direction créative + tokens (depuis `.ux/last-recommendation.json`).
- **Sorties :** Du code qui marche, distinguable de l'output IA générique. Pas de dégradés violets, pas de hero centré, pas de trois cartes égales, pas d'Inter en taille display, pas de « John Doe », pas d'emoji, pas de défaut à 300 ms.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Possède :** La motion dans le code frontend de production — Framer Motion, GSAP, animations CSS. Durées, easings, chorégraphie, fallbacks reduced-motion, discipline de performance.
- **Dépêché par :** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Entrées :** Brief de motion + tokens + les 57 préréglages de motion de `data/motion-presets.json`.
- **Sorties :** De la motion qui gagne sa place. Toujours encapsulée dans des fallbacks `prefers-reduced-motion`. Toujours testée contre les Core Web Vitals.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Possède :** Les chaînes qui partent en production — messages d'erreur, empty states, CTAs, loading states, messages de succès, toasts, texte d'aide, libellés de formulaire, texte des boutons.
- **Dépêché par :** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Entrées :** Profil de voix (nommé ou collé) + les chaînes de la surface.
- **Sorties :** Du microcopy production appliqué de manière cohérente à chaque état d'une surface pour que le produit sonne comme un produit, pas dix. Bannis : « le formulaire contient des erreurs », « John Doe », copy célébratoire enjoué d'IA, CTAs génériques, empty states morts.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Possède :** La digestion des entrées de recherche (entretiens, analytics, sites concurrents, résultats A/B, tickets de support) en recommandations de design actionnables.
- **Dépêché par :** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Entrées :** Recherche brute — transcripts, exports, URLs concurrents, clusters de support.
- **Sorties :** Thèmes, preuves, recommandations. Ne dessine jamais la réponse — donne au designer le substrat depuis lequel concevoir.
- **Tools :** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Possède :** Les systèmes de design complets — tokens (couleur, typographie, espace, motion, rayon, ombre), docs de fondations, contrats de composants, appariements dark-mode, couche de theming.
- **Dépêché par :** `/ux-system`, `/ux-component` quand aucun système n'existe.
- **Entrées :** Brief de marque + `.ux/last-recommendation.json` (style + palette + paire typographique + préréglages motion).
- **Sorties :** Un système cohérent, opiniâtre, prêt pour la production contre lequel les agents en aval peuvent construire sans re-décider les fondamentaux. Tokens JSON, fondations MD, contrats de composants, mapping dark-mode.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocole de dépêche des sous-agents

Quand une commande dépêche un sous-agent, elle passe :

1. Le brief / la recommandation (chargés depuis `.ux/`).
2. La tranche de manifeste pertinente (par ex. `frontend-engineer` reçoit le style + la palette + les composants choisis ; `motion-engineer` reçoit les préréglages de motion choisis).
3. Les 35 garde-fous d'anti-patterns (toujours actifs).
4. Un critère de succès (ce que l'artefact doit faire).

Les sous-agents renvoient :

1. L'artefact (code, doc, système).
2. Un bloc de justification (pourquoi ces choix).
3. Une auto-vérification contre les garde-fous (quelles règles ils ont vérifiées).

La commande appelante lance ensuite `/ux-lint` automatiquement avant de déclarer la chose faite.

---

## Les 11 manifestes de données

La couche de données est le cerveau. Chaque commande lit dedans ; le moteur fusionne à travers ; le linter scanne contre. Tous les fichiers vivent sous `data/` et enveloppent leurs entrées dans `{_meta, entries}` pour le versioning de schéma.

### `styles.json` — 84 styles de design

| Champ | Description |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimaliste / Suisse, Brutaliste, Éditorial, Glassmorphisme, Néomorphisme, Bento, Skeuomorphique, Industriel, Maximaliste, IA-Futuriste, MENA-moderne, Vaporwave, etc. |
| `sample entry` | `swiss-international` — « La grille fait loi. La typographie fait le gros du travail. La décoration, c'est l'échec. » |

Utilisé par : `/ux-recommend`, `/ux-system`, `/ux-design`. Schéma : [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 palettes de couleur

| Champ | Description |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (clair/sombre), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | chaleureux, éditorial, magazine, clinique, joueur, brutaliste, monochrome, joyau, MENA-chaud, dev-tools-sombre, etc. |
| `sample entry` | `claude-warm-editorial` — clair, chaleureux/éditorial/magazine, canvas #faf9f5, primary #cc785c |

Utilisé par : `/ux-recommend`, `/ux-system`. Contraste vérifié AA / AAA. Schéma : [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 appariements typographiques

| Champ | Description |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Toutes les familles ont licence + URL source. Utilisé par `/ux-recommend`, `/ux-system`.

### `components.json` — 148 composants

| Champ | Description |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Formulaires, Affichage de données, Feedback, Overlays, Layout, Contenu, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Méga Navigation, Grille de Produit — anatomie en 6 parties, 4 états |

C'est notre plus grand fossé concurrentiel. Aucun autre plugin UX pour Claude ne livre un manifeste structuré de composants.

### `industries.json` — 184 règles sectorielles

| Champ | Description |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Services Financiers, Santé, Éducation, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Voyage, Immobilier, Spécifique MENA, etc. |
| `sample entry` | `fintech-neobank` — forte confiance, disclosures réglementaires, UI primaire balance/transaction, mobile-first d'usage quotidien |

Utilisé par `/ux-recommend` comme premier axe de recherche parallèle.

### `chart-types.json` — 35 types de graphique

| Champ | Description |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparaison, Séries Temporelles, Distribution, Composition, Relation, Flux, Géographique |
| `sample entry` | `bar-vertical` — Comparer 4–15 catégories discrètes. La position sur l'axe x mappe la catégorie ; la hauteur mappe la valeur. |

Utilisé par `/ux-dashboard`, `/ux-component` (instances de chart).

### `tech-stacks.json` — 25 stacks

| Champ | Description |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, expérimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, compatible avec Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Les autres stacks incluent Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 lois UX nommées

| Champ | Description |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Coût de Décision, Attention, Mémoire, Contrôle Moteur, Perception Visuelle, Social, Émotionnel, Formulaires, Gestion d'Erreurs, Onboarding, Empty State, etc. |
| `sample entry` | `hicks-law` — Le temps de décision croît logarithmiquement avec le nombre d'options présentées |

Utilisé par `/ux-audit` (scoring à 6 lentilles) et `/ux-critique` (ancre de goût).

### `motion-presets.json` — 57 préréglages de motion

| Champ | Description |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entrée, Sortie, Hover, Focus, Tap, Loading, Empty, Success, Error, Lié au scroll |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Chaque préréglage a une variante reduced-motion. Code prêt par stack pour Framer Motion, GSAP et CSS pur.

### `anti-patterns.json` — 145 règles regex

| Champ | Description |
|---|---|
| `entries` | 145 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y (23), Contenu (15), Layout (13), Typographie (10), Couleur (9), Qualité (9), Visuel (9), Motion (8), Performance (4) |

La liste complète des règles est dans [Les 145 règles anti-slop IA](#les-145-règles-anti-slop-ia--le-linter).

### `brands/*.json` — 160 specs de marque

| Champ | Description |
|---|---|
| `entries` | 160 (plus `_index.json` qui les liste toutes) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automobile (8) |

Liste complète dans [Les 160 spécifications DESIGN.md de marque](#les-160-spécifications-de-marque-designmd--par-catégorie).

---

## Les 145 règles anti-slop IA — le linter

ux-skill livre un linter déterministe à base de regex. **Pas de LLM.** **Pas d'API.** **Pas de réseau.** Tourne en CI en ~200 ms sur une app Next.js typique. Sort en non-zéro sur findings Critical / High quand `--fail-on high` est posé.

Les règles sont sourcées depuis `data/anti-patterns.json` (v2 préférée) avec un fallback `references/foundations/anti-patterns.md` (v1 bash). Deux binaires sont livrés : `bin/ux-lint.py` (Python, rapide, extensible) et `bin/ux-lint.sh` (Bash + perl-PCRE, pour les environnements sans Python).

### Règles par catégorie

#### Typographie (3 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| high | `inter-as-display` | Inter utilisée comme police display |
| medium | `hero-text-arbitrary-90px` | Taille de police arbitraire pour le hero |
| low | `font-system-only` | Stack de police système sans typographie choisie |

#### Couleur (6 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| high | `purple-to-blue-gradient` | Dégradé violet-vers-bleu par défaut d'IA |
| high | `dark-text-on-dark-card` | Texte à faible contraste sur carte |
| medium | `gradient-text-rainbow` | Texte avec dégradé multi-stops |
| medium | `card-glow-purple-shadow` | Ombre glow violette sur cartes |
| medium | `gradient-mesh-purple-pink` | Hero avec mesh violet-rose |
| low | `tailwind-color-named-vague` | Couleurs Tailwind nommées sans token sémantique |

#### Layout (5 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| high | `three-equal-card-grid` | Trois cartes égales en ligne |
| medium | `centered-everything-hero` | Composition de hero tout-centré |
| medium | `avatar-stack-overlapping` | Stack générique d'avatars chevauchants |
| low | `pill-rounded-full-everywhere` | `rounded-full` appliqué à tout |
| low | `nav-equal-hamburger-desktop` | Menu hamburger en desktop |

#### Contenu (5 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum dans du code envoyé en production |
| high | `emoji-in-ui` | Emoji utilisé comme élément d'UI |
| high | `icon-emoji-stamp` | Emoji utilisé comme tampon d'icône |
| high | `testimonial-fake-five-stars` | Témoignage cinq étoiles hardcodé |
| medium | `fake-name-john-doe` | Noms placeholder génériques |

#### Motion (3 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Flèche rebondissante sur CTA |
| low | `timing-300ms-default` | Timing de transition par défaut à 300 ms |
| low | `cubic-bezier-material-only` | Easing par défaut de Material partout |

#### A11y (6 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| high | `inline-svg-no-aria` | SVG sans aria-label ou aria-hidden |
| high | `img-no-alt` | Image sans attribut alt |
| high | `link-onclick-no-href` | Ancre avec onClick mais sans href |
| medium | `button-no-type` | Bouton sans attribut type |
| medium | `heading-skip-h1-h3` | Niveau de titre sauté |
| medium | `infinite-scroll-no-pagination` | Scroll infini sans fallback clavier |

#### Qualité (6 règles)

| Sévérité | ID de règle | Nom |
|---|---|---|
| high | `console-log-leak` | `console.log` dans le code d'un composant |
| medium | `inline-style-attribute` | Attribut style inline |
| medium | `any-type-leak` | Type TypeScript `any` |
| medium | `arbitrary-z-index-9999` | Valeur de z-index paresseuse |
| low | `shadcn-default-everywhere` | Bloc de tokens shadcn par défaut non modifié |
| low | `todo-fixme-comment` | TODO ou FIXME dans du code envoyé en production |

#### Visuel (1 règle)

| Sévérité | ID de règle | Nom |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur sans surface en verre |

### Utilisation du linter

**Scan ponctuel :**

```bash
uxskill lint .
# ou
python3 bin/ux-lint.py src/
# ou
bash bin/ux-lint.sh src/
```

**Porte de CI (GitHub Actions) :**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Hook pre-commit :**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Sortie (échantillon) :**

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

## Les 160 spécifications de marque DESIGN.md — par catégorie

Vraies marques. Vrais langages de design. Vraies specs DESIGN.md — pas des palettes génériques. Vous dites au plugin « construis une landing dans le style de Stripe » et il lit le vocabulaire de marque réel : rubrique de voix, tokens de couleur, conventions de motion, signature moves, anti-moves.

Chaque marque est livrée comme JSON structuré (`data/brands/<slug>.json`) plus une référence en prose (`references/brands/<slug>.md`).

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

### Automobile (8)

BMW, BMW M, Bugatti, Ferrari, Lamborghini, Renault, SpaceX, Tesla

### Pourquoi ça compte

Les 8 autres plugins UX populaires pour Claude génèrent du « minimal moderne » ou du « dashboard clean » — variantes de la même esthétique par défaut. ux-skill vous permet de demander **la clarté de Linear**, **le sérieux de Stripe**, **la retenue d'Apple**, **le monolithe de Tesla**, **la convivialité de Notion**, **la discipline des dégradés de Cursor**, **la densité filaire de Raycast**, **le chaleureux éditorial de Claude** — et le moteur tire les bons tokens, la voix, les conventions de motion et les signature moves depuis la spec de marque.

---

## Serveur MCP — le coup asymétrique

ux-skill livre un **serveur Model Context Protocol**. Lancez `ux-mcp` et le moteur devient un processus stdio long-running que n'importe quel host MCP-compatible — Claude Desktop, Cursor, Windsurf, agents génériques — peut appeler. Quatorze outils : `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Mêmes handlers Python que les commandes slash ; mêmes manifestes de données ; même recommandeur déterministe.

**Pourquoi c'est le coup asymétrique :** aucune des huit meilleures skills UX pour Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ne livre de serveur MCP. Elles sont verrouillées à l'intérieur du runtime de plugin Claude Code. ux-skill est joignable depuis n'importe quel host qui parle MCP, y compris des agents qui n'ont jamais entendu parler d'un plugin Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp est un extra opt-in
ux-mcp                                  # le serveur stdio JSON-RPC démarre
```

Pointez votre client sur le binaire `ux-mcp`. Documentation complète des outils, exemples JSON et config par client pour Claude Desktop, Cursor et Windsurf sur [docs/mcp.html](docs/mcp.html) et dans `commands/ux-mcp.md`.

---

## L'installateur pour 17 IDEs

`uxskill init` (ou `/ux-init` à l'intérieur de Claude Code) auto-détecte l'IDE que vous utilisez et écrit le bon artefact. Même moteur Python. Mêmes recommandations. Glue différente par IDE.

| IDE / Outil | Signal de détection | Artefact installé |
|---|---|---|
| Claude Code | `.claude/` ou `CLAUDE.md` | Manifeste de plugin à `.claude-plugin/plugin.json` + les 22 commandes + les 5 sous-agents |
| Cursor | `.cursor/` ou `.cursorrules` | En-tête de prompt `.cursorrules` pointant sur le moteur |
| Windsurf | `.windsurf/` ou `.windsurfrules` | `.windsurfrules` avec le même en-tête de prompt |
| GitHub Copilot | `.github/copilot-instructions.md` ou `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | patch `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` ou `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

Dans chaque IDE, les mêmes commandes CLI `uxskill recommend` / `uxskill lint` / `uxskill stats` fonctionnent depuis le terminal. Le moteur Python est la source de vérité ; les artefacts par IDE sont des en-têtes de prompt fins qui y routent.

---

## Cas d'usage — scénarios concrets

Huit scénarios réels. Choisissez celui le plus proche de votre situation et adaptez l'invocation.

### 1. Construire un dashboard fintech dans Cursor

Vous êtes dans Cursor en train de travailler sur un dashboard de néobanque MENA. Vous installez le plugin et lancez discovery, recommandation, puis génération du dashboard.

```bash
pip install uxskill
uxskill init                                # détecte Cursor, écrit .cursorrules
uxskill discover                            # intake à 10 champs
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Puis dans Cursor, vous demandez : *« Génère la surface du dashboard en utilisant la recommandation dans .ux/last-recommendation.json »*. Cursor lit l'en-tête `.cursorrules`, charge la recommandation, dépêche une génération de dashboard avec des contraintes explicites.

### 2. Générer une landing au style Stripe dans Claude Code

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Type de projet ? landing
> Secteur ? fintech-payments
> Ton ? sérieux, technique, sûr
> Indispensables ? dark-mode, AA, mobile-first
> Interdits ? purple-gradients, three-equal-cards
> Marques de référence ? stripe
> Stack ? nextjs-15-app-router
> Région ? global
> Métrique de succès ? conversion signup

/ux-recommend
> [renvoie style, palette, paire typographique, préréglages motion, composants, marques exemplaires choisis]

/ux-design "génère la landing en utilisant la spec de marque Stripe comme exemplaire"
> [frontend-engineer génère la page]

/ux-lint .
> [passe — la spec de marque Stripe a été respectée]
```

### 3. Auditer du code existant à la chasse au slop IA en CI

Vous avez expédié une app Next.js il y a deux semaines. Vous voulez un plancher dur contre les empreintes IA sur chaque PR.

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

Les PRs qui introduisent des dégradés violet-vers-bleu, Inter à 96 px, des témoignages « John Doe » ou des emojis comme icônes échouent au CI. Sans coût LLM. ~200 ms.

### 4. Polir une surface existante qui « sent l'IA »

Vous avez hérité d'une app React qui ressemble à n'importe quel autre site SaaS généré par IA. Vous voulez qu'elle arrête de ressembler à ça.

```
/ux-critique src/components/Hero.tsx
> [3 réussites, 3 ratés, 1 coup stratégique — la prise est honnête]

/ux-lint src/
> [15 empreintes IA de sévérité haute signalées]

/ux-polish src/components/Hero.tsx
> [passe cosmétique pilotée par LLM + élimination du slop IA]

/ux-fix
> [applique les findings en commits atomiques, relance le linter]
```

Trois commandes, une surface polie, commits atomiques par correctif.

### 5. Concevoir une command palette au style Linear

```
/ux-component command-palette --brief="style Linear, sombre, shortcuts monospace, items récents en tête"
> [lit data/brands/linear.app.json pour les tokens + signature moves]
> [lit data/components.json pour l'anatomie + les états de command-palette]
> [dépêche frontend-engineer avec la spec Linear explicite]
```

Le composant généré utilise les tokens de couleur réels de Linear, son stack typographique, ses conventions de motion, ses densités filaires — pas « UI sombre générique ».

### 6. Animer un atelier de design thinking de 90 minutes avec des stakeholders

Vous avez une salle de 5 personnes pour 90 minutes. Vous voulez qu'elles repartent avec un plan de jeu, pas avec un vibe.

```
/ux-workshop "pivot wallet de fidélité" \
  --participants="2 PMs, 1 designer, 1 lead eng, 1 client representative" \
  --minutes=90
```

Le plugin facilite les cinq phases (exploration → carte de chaleur → carte des acteurs → croquis de solution → plan de jeu) de bout en bout, chronométrées, avec des artefacts concrets par phase. La sortie est `.ux/last-workshop.json` — le plan de jeu, pas juste « des findings intéressants ».

### 7. Écrire une étude de cas publiable après lancement

Vous avez expédié le wallet de fidélité. Vous voulez une pièce portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [lit .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [génère une étude de cas éditoriale Wfrah avec sections numérotées (A)-(G), séparateurs filaires, layout bilingue-safe]
> [écrit case-studies/bashiti-loyalty.html]
```

L'étude de cas est un artefact fini, publiable — pas un brouillon. Monochrome pur, typographie éditoriale, prêt à publier sur votre portfolio.

### 8. Lancer la discovery dans un contexte non-IA (juste l'intake structuré)

Vous cadrez un projet. Vous n'avez pas encore besoin d'une recommandation — vous avez besoin d'un brief structuré.

```bash
uxskill discover
# intake à 10 champs, sauvegardé dans .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Vous pouvez remettre le JSON à votre équipe, le coller dans un doc Notion ou l'alimenter à un autre outil IA. ux-skill est aussi un outil d'intake structuré, en plus d'être un moteur.

### 9. Persistance MASTER.md — vos décisions de design, dans le dépôt

Après `/ux-recommend`, persistez le style choisi + palette + typographie + motion + composants + marques exemplaires + garde-fous dans un fichier Markdown lisible par humains que votre équipe peut relire, diffuser et versionner.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Écrit `.ux/design-system/MASTER.md` (frontmatter YAML + corps) et `.ux/design-system/pages/<name>.md` par surface générée via `persist save-page`. Idempotent — la même entrée produit une sortie identique octet pour octet, donc relancer sur un état inchangé est un no-op en git.

---

## Face aux alternatives

Table récapitulative courte. La comparaison complète côte à côte est sur [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimension | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Commandes slash | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Composants | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Préréglages motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specs de marque | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Règles d'anti-patterns | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter déterministe compatible CI | **oui** | non | non | non | non | non | non | non | non |
| IDEs pris en charge | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Porte de discovery | **10 champs** | implicite | implicite | implicite | implicite | implicite | implicite | implicite | implicite |
| Chaîne d'état `.ux/` | **oui** | non | non | non | non | non | non | non | non |
| Étoiles (2026-05-28) | 14 | 83 958 | 54 406 | 25 202 | 15 455 | 5 762 | 2 391 | 2 164 | 955 |

### Évaluation honnête

- **ui-ux-pro-max** est plus grand en notoriété, livre 18 IDEs, a une recherche style BM25 sur son CSV. Il ne livre pas de manifeste de composants, manifeste de motion, bibliothèque de marques ni linter déterministe.
- **open-design** a 19 skills + preview mais seulement support Claude Code et pas de couche anti-slop.
- **hallmark** est le plus proche en esprit (aussi anti-slop) mais c'est une skill unique — pas de moteur, pas de manifestes, pas de commandes enchaînées.
- **material-3-skill** est excellent si vous voulez spécifiquement Material Design 3. Nous ne concurrencons pas sur MD3.

Pour le détail complet par dimension, voir [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Feuille de route

### v2.1 — Complétude du linter (T3 2026)

- **+17 règles d'anti-patterns différées** pour atteindre 52 au total. Cibles : états hover sombre-sur-sombre, encodage d'état uniquement par couleur, escalade redondante de z-index, breakpoints hardcodés en JS, opacity en lieu et place d'état disabled, etc.
- **`uxskill lint --fix` pour réécritures sûres** des findings mécaniquement corrigibles (button-no-type, img-no-alt avec chaîne vide, suppression de console-log-leak).
- **Extension VS Code** qui fait remonter les findings du linter en ligne (pas besoin de lancer le CI).

### v2.2 — Expansion du manifeste de composants (T4 2026)

- **+50 composants** pour atteindre 198 au total. Nouveautés : combobox avec filtre async, command-palette avec heuristique d'items récents, conditional-form-step, variantes de payment-element, date picker conscient du RTL, input téléphone spécifique MENA, calendar grid avec overlay hijri.
- **Émission de code par composant** dans 6 stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Playground de composants** à uxskill.laithjunaidy.com/playground — essayez le moteur de recommandation + voyez la preview live du composant.

### v3 — Le marketplace + le lock-in (2027)

- **Marketplace de specs de marque** — publier et découvrir des specs de marque communautaires. Payer-pour-publier pour financer la modération.
- **Règles d'anti-patterns personnalisées** — les projets peuvent définir leurs propres règles regex dans `data/anti-patterns.local.json` (déjà livré en v2 ; v3 ajoute découverte + partage).
- **`uxskill plan`** — planification complète de site multi-pages depuis un brief, pas seulement une surface.
- **Parité plugin Figma** — même moteur de recommandation, exposé dans Figma.

---

## Contribuer

Issues et PRs bienvenues. Trois zones à fort effet de levier :

### Ajouter une règle d'anti-pattern

1. Éditez `data/anti-patterns.json` — ajoutez une entrée avec `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Ajoutez un test dans `tests/linter/` — un fichier qui déclenche la règle, un qui ne la déclenche pas.
3. Lancez `uxskill lint tests/linter/should-trigger/<rule>.tsx` — confirmez qu'elle se déclenche. Lancez sur `tests/linter/should-not-trigger/<rule>.tsx` — confirmez qu'elle ne se déclenche pas.
4. Ouvrez une PR.

### Ajouter une spec de marque

1. Créez `data/brands/<slug>.json` avec `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Ajoutez la prose correspondante à `references/brands/<slug>.md`.
3. Enregistrez dans `data/brands/_index.json`.
4. Ouvrez une PR. La spec doit être adossée à des références de source primaire (le produit réel de la marque, son système de design public ou son DESIGN.md si elle en publie un).

### Ajouter un préréglage de motion

1. Éditez `data/motion-presets.json` — ajoutez une entrée avec `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Le préréglage doit avoir une variante reduced-motion. Sans exception.
3. Ouvrez une PR.

### Processus

- Lisez [CONTRIBUTING.md](CONTRIBUTING.md) pour le processus complet.
- Lisez [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Les nouvelles règles et specs de marque sont relues pour : ancrage en source primaire, absence d'overfitting à un projet unique, absence d'emoji dans toutes les données, comportement RTL-safe quand applicable.

---

## Licence, auteur, remerciements

### Licence

MIT. Utilisez-le, forkez-le, construisez dessus. S'il vous évite d'expédier du slop IA, mettez une étoile au dépôt — c'est la façon la moins chère de le soutenir.

### Auteur

**Laith Aljunaidy** — fondateur solo de [Dot](https://thedotwallet.com), une plateforme de fidélité MENA-first. Construisant ux-skill pour que le frontend généré par IA ne se ressemble plus tout pareil.

- LinkedIn : [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email : laith.aljunaidy.laith@gmail.com
- Dépôt : [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site : [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI : [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm : [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Remerciements

- L'équipe d'Anthropic pour Claude Code et l'architecture skill / plugin qui a rendu ceci distribuable.
- Nielsen Norman Group, Laws of UX (lawsofux.com) et la communauté de recherche UX dont le travail nourrit `data/ux-guidelines.json`.
- Chaque marque listée dans `data/brands/` — leurs systèmes de design publics sont la source de vérité pour les specs de marque.
- Les contributeurs originaux de la v1 : une skill Claude one-shot devenue la graine du moteur Python v2.
- Les 8 plugins UX populaires pour Claude auxquels nous nous sommes comparés — ils ont relevé la barre ; ceci est notre réponse.

---

**ux-skill** · **v3.0.0-stable** · Construit pour que Claude Code, Cursor, Windsurf et tous les autres outils de codage par IA produisent du frontend qui ne se lit pas comme généré par IA.

> Mettez une étoile au dépôt sur [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Installez via `pip install uxskill` ou `npx uxskill init` · Parcourez la comparaison sur [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
