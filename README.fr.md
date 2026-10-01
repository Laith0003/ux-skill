[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · **Français** · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: le moteur d'intelligence de design pour Claude Code, Cursor et tous les autres outils de codage par IA

**Un moteur d'intelligence de design qui rend l'UI générée par IA singulière au lieu de générique.** Branchez-le dans l'un des 17 outils de codage par IA et ce que vous produisez cesse de ressembler à du travail d'IA. Gratuit, MIT, hors ligne, sans LLM.

```bash
pip install uxskill
```

**[Mettez une étoile à ux-skill sur GitHub](https://github.com/Laith0003/ux-skill)** si l'outil vous sert : c'est le moyen le plus simple d'aider le projet. Vous découvrez ? Commencez par la [visite de 60 secondes](#installation-rapide) ou voyez-le en action sur [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![Avant : hero générique en photo de banque d'images, dégradé violet doux, aucune identité de marque. Après : vraie photo de chantier sous un voile sombre, titre éditorial avec un accent ambre et un formulaire de demande de devis intégré au hero. Même prompt, résultat différent quand ux-skill fournit les contraintes.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Avant : du slop SEO générique en photo de banque d'images. Après : un hero avec une vraie photo de chantier sous un voile sombre, un titre éditorial avec un accent ambre, un formulaire de devis dans le hero. Même outil de codage par IA, même prompt, résultat différent quand ux-skill fournit les contraintes.*

> **v4.0, FOUNDATIONS : une seule commande construit un design system complet, contrôlé selon les WCAG, avec l'arabe et la droite à gauche intégrés.** Le plugin UX le plus puissant pour le codage par IA. Un noyau de raisonnement Python avec un synthétiseur déterministe à 7 axes, 12 manifestes JSON interrogeables (84 styles, 176 palettes, 70 appariements typographiques, 148 composants, 184 secteurs, 35 types de graphique, 57 préréglages de motion, 112 lois UX, 171 règles d'anti-patterns, 25 stacks techniques, 160 spécifications de marque), 18 commandes slash, 5 sous-agents, 25 outils MCP et un linter déterministe anti-slop IA. Multi-IDE : se distribue dans Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer et Roo Cline.

> **Le nom de marque est `ux-skill`.** Le nom du paquet PyPI / npm reste `uxskill`. Le dépôt GitHub vit à [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Auteur :** [Laith Aljunaidy](https://laithjunaidy.com), designer et CTO à Amman · **Site :** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Comparaison avec chaque plugin UX pour Claude :** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub :** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI :** [uxskill](https://pypi.org/project/uxskill/) · **npm :** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#linstallateur-pour-17-ides)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Nouveau dans la 4.0 : les fondations

Une couleur de marque en entrée, un design system en sortie, avec son contraste vérifié avant qu'il vous soit remis.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 ou plus récent. Pour le serveur MCP, `pip install --upgrade 'uxskill[mcp]'`. Avec pipx, `pipx install uxskill` (par-dessus une 3.x installée, `pipx upgrade uxskill`). Avec npm, `npx uxskill@latest`. Vous venez de la 3.x ? Le [guide de migration](docs/migrating-to-4.md) fait correspondre chaque token 3.x à son rôle en 4.0.

**Vous construisez un produit ou une landing page ?** Vous obtenez `tokens.css` à lier depuis votre page, `fonts.css` avec des polices de repli aux métriques ajustées pour les fontes choisies, `fonts-self-host.css` qui charge les fontes depuis vos propres fichiers, `tokens.json` pour les outils, des visuels de marque décoratifs dans `art/` et `system-report.md`, qui explique en termes simples ce qui a été construit, pourquoi, et par quelle composition de page commencer. Stylez avec les rôles (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`), et basculez le mode sombre, le contraste élevé, l'espacement compact, la droite à gauche ou le mouvement réduit avec un seul attribut sur `<html>`. Chargez les fontes avec le lien Google Fonts que donne le rapport, ou avec `fonts-self-host.css` et un dossier `fonts/`, et liez `fonts.css` dans les deux cas, avant `tokens.css` ; ne modifiez aucun de ces deux fichiers. Avec `--brief`, le rendu suit le secteur et le ton quand le brief les nomme, et des champs structurés (âge, langues, schéma par défaut, contexte de lecture) fixent la taille du texte, les cibles, les écritures et le schéma qui s'ouvre ; la discovery ne demande pas de secteur, donc `/ux-system create` le demande. Dans Claude Code, `/ux-system create` vérifie la version installée, lance la construction et explique le rapport.

**Vous concevez un design system ?** Neuf fondations (couleur, typographie, espacement, mise en page, rayon, bordure, élévation, mouvement, image), chacune variant de façon continue avec les sept axes, avec des primitives et des rôles sémantiques, au format W3C design tokens (DTCG 2025.10) avec les valeurs de chaque mode. Mêmes entrées, mêmes octets. Via MCP, `ux_system_build` renvoie le rapport, le résultat du contrôle et la taille de chaque fichier, et écrit les mêmes fichiers que la commande quand on lui donne `out`.

- **Contrôle WCAG.** Chaque paire de couleurs de texte, de contrôle et de focus est mesurée en mode clair et sombre, en contraste standard et élevé : WCAG 1.4.3 (texte 4.5:1) et 1.4.11 (non textuel 3:1) en contraste standard, WCAG 1.4.6 (texte 7:1) en contraste élevé, plus un plancher de 4.5:1 en contraste élevé pour la plupart des éléments non textuels, qui est le nôtre, puisque les WCAG ne fixent aucun niveau renforcé pour le non textuel. Un système qui échoue n'est pas écrit ; le message dit quoi changer.
- **Sûr par défaut.** Il n'écrase jamais un fichier qui diffère. `--force` remplace les fichiers uniquement si vous le demandez.
- **Arabe.** Sous `dir="rtl"`, le texte passe à une fonte arabe avec ses propres tailles et sa propre hauteur de ligne ; l'espacement utilise des propriétés logiques et les mouvements sont inversés. `--latin-only` l'exclut.

**Un système que vous avez déjà.** `/ux-system enhance --from` le lit avec ses propres noms (tokens DTCG, propriétés personnalisées CSS, thème Tailwind, fichiers de règles markdown ou export de variables Figma), le passe au même contrôle et mesure ce que votre code en fait réellement ; rien n'est réécrit. `/ux-system extend --from` ajoute des fondations, des rôles ou des contrats sans changer un seul de ses tokens, dans un fichier d'extension posé à côté, et `uxskill system export` l'écrit en tokens.css, en thème Tailwind 4 ou en variables Figma. La 4.2 ajoute la couche de confiance (lint à chaque écriture, un relecteur de finition) et le lancement. Voir le [changelog](CHANGELOG.md).

**Composants et sections.** 23 contrats de composants indiquent quels tokens chaque partie d'un contrôle utilise dans chaque état et comment chaque état s'anime : un changement d'état transite sur `motion.state`, un appui se met à l'échelle sur `motion.press.scale` (et reste immobile en mouvement réduit), et les onglets, menus et contrôles segmentés font glisser un seul indicateur. 14 contrats de sections (hero, tarifs, FAQ, pied de page et les autres) nomment le rôle de chaque section, les composants que prennent ses emplacements, la preuve qu'elle exige et la façon dont elle s'empile sur mobile. Les pages construites avec eux utilisent des photographies ; les fragments d'interface sont une imagerie en plus, jamais un remplacement.

**Un linter qui lit la page.** 171 règles, dont beaucoup ajoutent un contrôle sur le CSS et le balisage analysés, lisent le propre système de la page : le mouvement est minuté d'après sa courbe, la hauteur de ligne des titres display est tenue au plancher du moteur, et un contrôle masqué doit sortir de l'ordre de tabulation. `uxskill lint --render` ouvre chaque page dans Chromium headless en largeur desktop et mobile et la pilote : anneaux de focus invisibles ou rognés, survol et appui qui répondent en retard, focus perdu après Échap, et appui qui bouge encore en mouvement réduit.

**Moins de commandes.** 25 commandes slash deviennent 18. `/ux-discover` prend `--frame` et `--recommend`, `/ux-design` prend `--component`, `--dashboard` et `--from-image`, `/ux-polish` enchaîne lint, fix, re-lint jusqu'à ce que le score atteigne 90 ou que trois tours soient passés, et `/ux-init` prend `--stats`. Les sept anciens noms fonctionnent encore comme alias et disparaissent en 4.1 ; voir [les alias](#alias-retirés-en-41).

**Playbooks de surface.** Les règles landing, dashboard et composant vivent dans `references/surfaces/`, un playbook chacune. `/ux-design` en charge exactement un, choisi selon son mode, si bien qu'une construction de dashboard ne lit jamais les règles du hero.

Tests : **9764 réussis**. Hors ligne. Déterministe. Aucun LLM appelé, jamais.

### Nouveau dans la v3.1 : fidèle à la marque, responsive, vivant

- **La fidélité à la marque est imposée, pas espérée.** La couleur primaire est lue dans les pixels du LOGO (pas dans le CSS le plus peint) ; les polices par défaut sont rejetées au profit du style de lettre du logo. La marque extraite voyage `recommend` -> `synthesize`, et un **plancher strict** dans `evaluate` fait ÉCHOUER toute sortie qui perd la couleur ou le logo de la marque ou ne livre aucune vraie image. Interopérabilité dans les deux sens avec la convention ouverte `brand.md` (rendu + import).
- **Mobile-first, contrôlé.** De nouvelles fondations de métier (`responsive.md`, `component-behaviors.md`) et un contrôle attentif aux retours à la ligne qui échoue sur un défilement horizontal, un libellé de nav, de logotype ou de bouton qui passe à la ligne, ou un en-tête sticky trop haut.
- **La couche wow.** Le moteur dérive 2-3 moments signature coordonnés par page ; la doctrine « le wow ne peut venir que de l'utilisateur » est renversée.
- **Linter plus affûté** (152 règles) : détection des images obligatoires et des éléments icône seule, règles sur les tokens de remplissage et `100vw` ; picsum avec graine conservé, aléatoire supprimé.

Notes complètes dans [CHANGELOG.md](CHANGELOG.md).

### Nouveautés de la v3

- **Les brand specs deviennent des données d'entraînement, pas des templates.** Les 160 brand specs ne sont plus un catalogue dans lequel le recommandeur pioche, c'est un vocabulaire que le synthétiseur distille. La sortie est nouvelle à chaque appel.
- **Synthétiseur à 7 axes** (warmth, contrast, density, geometry, formality, motion, type_personality). Le brief est mappé de façon déterministe à des valeurs d'axes ; les axes compilent vers une palette + une typo + un spacing + un radius + un motion frais.
- **Trois modes auto-dispatchés**: `strict_brand` (100 % d'une marque), `brand_anchor` (70 % d'une marque + 30 % adapté par axes depuis des marques sœurs), `pure_synthesis` (aucune marque nommée, distillation de 8 exemples alignés sur les axes).
- **Le journal des décisions ré-ordonne le recommandeur.** `.ux/decisions.jsonl` re-classe les candidats selon les victoires passées dans le même bucket `(industry, ui_type)`. Cold-start sûr. Compte uniquement les décisions avec `lint_score >= 80` + `user_accepted = true`.
- **Matrice d'interaction d'axes**: résolution explicite des conflits (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Plus de règles ad hoc silencieuses.
- **Boucle automatique `/ux-evolve`** (en 4.0, la boucle par défaut de `/ux-polish`) : lint → polish → re-lint jusqu'à score ≥ 90, plateau ou 3 tours en 4.0 (5 en v3). Quality gate à 65.
- **3 nouveaux outils MCP** (15 → 18) : `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Tableau de bord local**: `uxskill stats --html` écrit `.ux/stats.html` montrant ce que VOTRE installation a appris. Pas de télémétrie, pas d'agrégation globale.
- **223 tests passent.** Hors ligne. Déterministe. Aucun appel LLM.

Détails complets dans [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Historique des étoiles

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Qu'est-ce que ux-skill

ux-skill est un **moteur d'intelligence de design** pour les outils de codage par IA. Il s'exécute comme paquet Python (`pip install uxskill`), comme plugin Claude Code et comme installateur multi-IDE pour 17 environnements. Le moteur ingère un brief de projet (secteur, audience, ton, indispensables, mouvements interdits, stack, région) et renvoie un système de design recommandé complet : style, palette, paire typographique, préréglages de motion, composants, marques exemplaires à étudier et les garde-fous d'anti-patterns qui doivent tenir. La recommandation est déterministe, la même entrée produit toujours la même sortie.

Le plugin se place entre vous et l'outil de codage par IA. Quand vous demandez à Claude Code, Cursor ou tout autre assistant IA de « construire une landing fintech », l'assistant improvise typiquement, et le résultat se lit comme généré par IA en cinq secondes (dégradés violet-à-bleu, trois cartes égales, Inter en taille display, « John Doe » dans les témoignages, transitions par défaut à 300 ms, hero centré, flèches rebondissantes sur les CTA). ux-skill remplace l'improvisation par des **contraintes structurées** : vous lancez `/ux-discover` pour capturer le brief et choisir le système, `/ux-design` pour générer le code et `/ux-lint` pour vérifier qu'il passe les 171 règles déterministes anti-slop IA avant le commit.

Ce README est la référence canonique. Chaque commande, chaque sous-agent, chaque manifeste de données, chaque chemin d'installation, chaque spécification de marque, chaque catégorie d'anti-pattern, tout est documenté ici. Si vous cherchez un plugin de design pour Claude Code ou comparez des outils de design par IA pour Cursor, Windsurf ou Codex, lisez ceci de bout en bout et [compare.html](https://uxskill.laithjunaidy.com/compare.html) en parallèle.

---

## Table des matières

1. [Le cerveau, ce qu'est la v3.0](#le-cerveau-ce-quest-la-v30)
2. [Installation rapide](#installation-rapide)
3. [Les chiffres, comparaison en direct face aux 8 meilleures skills UX pour Claude](#les-chiffres-comparaison-en-direct-face-aux-8-meilleures-skills-ux-pour-claude)
4. [Architecture, comment les pièces s'emboîtent](#architecture-comment-les-pièces-semboîtent)
5. [Les 18 commandes slash, référence détaillée](#les-18-commandes-slash--référence-détaillée)
6. [Les 5 sous-agents](#les-5-sous-agents)
7. [Les 11 manifestes de données](#les-11-manifestes-de-données)
8. [Les 171 règles anti-slop IA, le linter](#les-171-règles-anti-slop-ia--le-linter)
9. [Les 160 spécifications de marque DESIGN.md, par catégorie](#les-160-spécifications-de-marque-designmd-par-catégorie)
10. [Serveur MCP, le coup asymétrique](#serveur-mcp-le-coup-asymétrique)
11. [L'installateur pour 17 IDEs](#linstallateur-pour-17-ides)
12. [Cas d'usage, scénarios concrets](#cas-dusage-scénarios-concrets)
13. [Face aux alternatives](#face-aux-alternatives)
14. [Feuille de route](#feuille-de-route)
15. [Contribuer](#contribuer)
16. [Licence, auteur, remerciements](#licence-auteur-remerciements)

---

## Le cerveau: ce qu'est la v3.0

La v3.1.0 est le plus grand changement architectural de l'histoire d'ux-skill. Le recommandeur ne pioche plus de templates dans un catalogue, le moteur **synthétise** un langage de design frais à chaque brief. Le même brief produit toujours la même sortie (entièrement déterministe), mais chaque brief distinct obtient son propre système nouveau. Les brand specs ne sont plus des templates ; ce sont des données d'entraînement dont le moteur apprend le vocabulaire. Le système voit son propre historique, ferme la boucle de feedback localement, et n'appelle jamais de LLM.

Le compilateur est un **synthétiseur déterministe à 7 axes**, warmth, contrast, density, geometry, formality, motion, type_personality. Chaque brief mappe vers des valeurs d'axes ; les valeurs d'axes compilent vers une palette + une typo + un spacing + un radius + un motion frais. Les échelles typographiques modulaires choisissent leur ratio à partir du contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Les primitives de layout sont responsive par construction (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Les layouts cassés ne peuvent pas être émis parce qu'ils ne sont pas représentables.

Trois modes sont auto-dispatchés : `strict_brand` (`reference_brands=[stripe] strict=True` → 100 % des tokens Stripe, chemin le plus rapide) ; `brand_anchor` (`reference_brands=[stripe]` → 70 % Stripe + 30 % adapté par axes depuis 4 marques sœurs) ; et `pure_synthesis` (aucune marque nommée → espace infini, 8 exemples alignés sur les axes distillés en un langage de design nouveau). Les conflits d'axes sont résolus par une **matrice d'interaction d'axes** documentée, dense + corporate compile vers 4px (density gagne, école Bloomberg), airy + corporate vers 12px (formality gagne, luxe), soft + playful vers 18px radius, sharp + corporate vers 2px. Pas de règle ad hoc silencieuse dans l'implémentation.

Le **journal des décisions** (`.ux/decisions.jsonl`, schema `_v: 1` verrouillé) ferme la boucle de feedback. Le recommandeur re-classe désormais les candidats par victoires passées dans le même bucket `(industry, ui_type)`. Sûr au démarrage à froid : il passe son tour en dessous de 3 antécédents. Il ne compte que les décisions avec `lint_score >= 80` ET `user_accepted = true`. Et `/ux-polish` exécute lint → polish → re-lint jusqu'à score ≥ 90, plateau ou 3 tours, avec une porte qualité à 65 en dessous de laquelle la sortie est refusée sans `--force`. Résultat : chaque installation devient plus intelligente sur son propre corpus, chaque exécution est reproductible d'une machine à l'autre, et le moteur reste totalement hors ligne.

---

## Installation rapide

Trois voies d'installation. Choisissez celle qui correspond à votre environnement.

### Voie 1: marketplace Claude Code (canonique)

Si vous travaillez dans Claude Code, installez via le marketplace de plugins :

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Cela branche les 18 commandes slash (plus 7 anciens noms gardés comme alias jusqu'à la 4.1) et les 5 sous-agents à votre session Claude Code. Après l'installation, lancez `/ux-init` pour configurer le répertoire d'état `.ux/` propre au projet et vérifier que le moteur Python est accessible.

### Voie 2: pip (universelle)

Si vous travaillez hors de Claude Code (Cursor, Windsurf, CLI, CI), installez le paquet Python :

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

Le paquet expose à la fois `ux` et `uxskill` comme points d'entrée CLI, c'est le même binaire.

### Voie 3: npx (sans Python requis)

Si vous ne voulez pas gérer Python directement, le wrapper npx amorce tout via `pipx` :

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Vérifier l'installation

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

Les douze compteurs totalisent 1 262 entrées. Si l'un des compteurs renvoie 0, c'est qu'un fichier JSON manque : ouvrez une issue sur [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Les chiffres: comparaison en direct face aux 8 meilleures skills UX pour Claude

Les compteurs d'étoiles ont été vérifiés pour la dernière fois via `gh api` le **2026-05-28**. ux-skill (Laith0003/ux-skill) est le dernier entrant, nous sommes minuscules en notoriété, profonds en architecture. La comparaison ci-dessous est honnête : où nous perdons, où nous gagnons.

| Plugin | Étoiles | Architecture | Commandes slash | Linter (compatible CI) | Specs de marque | Composants | Préréglages motion | IDEs pris en charge |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83 958** | Python BM25 + CSV, skill unique | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54 406** | Node.js + 19 skills + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25 202** | Bash + goût adossé à la recherche | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15 455** | Unique SKILL.md de 62 Ko + scripts | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5 762** | Bibliothèque de skills câblée MCP | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2 391** | Skill mono-esthétique | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2 164** | Skill de design anti-slop | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Composants MD3 + audit | 1 | - |, | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Moteur Python + 12 manifestes + 18 commandes + 5 sous-agents + linter CI** | **18** | **171 règles déterministes** | **160** | **148** | **57** | **17** |

### Où nous perdons

- **Notoriété.** Eux ont des centaines de milliers d'étoiles. Nous en avons 14. Mettez-nous une étoile, c'est la façon la moins chère d'aider.
- **Reconnaissance de marque.** ui-ux-pro-max et open-design ont une avance qui se mesure en mois, pas en jours.
- **Finition marketing.** Ils ont des captures, des vidéos de démo et une landing découvrable. Nous avons un README exhaustif et une landing modeste.

### Où nous gagnons

- **Bibliothèque de composants :** 148 composants documentés avec anatomie, états, tokens utilisés et specs de motion. Aucun des 8 autres ne livre de manifeste de composants.
- **Préréglages de motion :** 57 entrées prêtes par stack (Framer Motion, GSAP, CSS) avec fallbacks reduced-motion. Aucun des autres ne livre de manifeste de motion.
- **Linter d'anti-patterns :** 171 règles déterministes, tourne en CI, sort en non-zéro sur Critical/High. Aucun des autres ne livre de linter déterministe.
- **Specs de marque :** 160 véritables specs DESIGN.md (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude et 96 autres). Aucun des autres ne livre de bibliothèque de marques.
- **17 IDEs pris en charge :** même moteur, glue différente par IDE.
- **18 commandes slash :** discovery, génération (pages, composants, dashboards, à partir d'une image), audit, lint, boucle de polish, boucle de fix, étude de cas, atelier, copy, motion, a11y, conductor, intégrées de bout en bout.

Tableau complet côte à côte sur [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Architecture: comment les pièces s'emboîtent

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

### Comment le moteur fonctionne réellement

1. **Entrée.** Vous fournissez un brief, soit de manière interactive via `/ux-discover` (10 champs), soit sans interaction via des flags passés à `ux recommend`.
2. **5 recherches parallèles.** Le moteur lance cinq recherches simultanées à travers les manifestes :
   - **Secteur → recommended_styles** (industries.json)
   - **Style → compatibilité palette + typographie + motion** (styles.json)
   - **Ton × indispensable → filtre de palette** (palettes.json)
   - **Stack → compatibilité des composants + préréglages de motion** (tech-stacks.json, motion-presets.json)
   - **Interdits + région → garde-fous + shortlist de marques exemplaires** (anti-patterns.json, brands/)
3. **Fusion.** Un fusionneur déterministe classe les candidats, résout les conflits (par ex. un mode sombre indispensable impose le mode de la palette) et émet un seul système recommandé.
4. **Sortie.** Un document JSON avec le style choisi, la palette, la paire typographique, les 5 meilleurs préréglages de motion, les 12 meilleurs composants, les 5 meilleures marques exemplaires et les 171 garde-fous d'anti-patterns actifs. Plus un bloc de justification qui explique chaque choix.
5. **Génération.** Les commandes en aval (`/ux-design` dans ses modes page, composant, dashboard et image, et `/ux-system`) consomment la recommandation pour générer du vrai code via les sous-agents.
6. **Vérification.** `/ux-lint` rescanne le code généré au regard des 171 règles. Sort en non-zéro sur Critical/High en CI.

**Apports de la v3.** Le recommandeur re-classe désormais les candidats depuis `engine/decisions/` en s'appuyant sur `.ux/decisions.jsonl` (seules comptent les décisions avec `lint_score >= 80` ET `user_accepted = true` ; sûr au démarrage à froid en dessous de 3 antécédents). Le chemin de génération peut passer par `engine/synthesizer/`, un compilateur déterministe à 7 axes qui produit pour chaque brief de nouveaux tokens de palette + typographie + espacement + rayon + motion au lieu de choisir des templates dans un catalogue. Détails dans [Le cerveau, ce qu'est la v3.0](#le-cerveau-ce-quest-la-v30).

**Python pense. HTML montre. Markdown enchaîne.**

---

## Les 18 commandes slash : référence détaillée

Chaque commande est livrée sous forme de fichier `.md` dans `commands/` avec `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` et `output state file`. Les descriptions ci-dessous sont condensées ; la source complète fait foi.

Les commandes sont regroupées en sept familles : **amorçage & inventaire**, **discovery & recommandation**, **génération**, **audit & vérification**, **correction & polish**, **discovery & récit** et **chef d'orchestre**. Sept noms de la 3.x fonctionnent encore comme [alias](#alias-retirés-en-41) jusqu'à la 4.1.

### Amorçage et inventaire

#### `/ux-init`: amorcer le projet

- **Quoi :** Détecte l'IDE que vous utilisez (`.claude/`, `.cursor/`, `.windsurf/`, etc.), installe le bon artefact, vérifie que le moteur Python est accessible, affiche un instantané des stats. `--stats` n'affiche que l'instantané : version + compteurs d'entrées des manifestes de données.
- **Quand l'utiliser :** Première installation dans un nouveau projet. Après avoir cloné un projet qui utilise ux-skill. Après `pip install --upgrade uxskill`. `--stats` après l'installation, après une mise à jour, ou quand une recommandation renvoie des choix surprenants et que vous soupçonnez des manifestes incomplets.
- **Quand passer :** Vous l'avez déjà lancé dans ce projet et rien n'a changé. `--stats` n'a jamais besoin d'être sauté : c'est une lecture de 50 ms.
- **Invocation :** `/ux-init` (sans args), `/ux-init --stats`, ou `uxskill init` / `uxskill stats` depuis la CLI. `--decisions` ajoute le résumé du journal des décisions ; `--html` écrit `.ux/stats.html`.
- **Sortie :** Artefact par IDE (voir [L'installateur pour 17 IDEs](#linstallateur-pour-17-ides)) + répertoire `.ux/` + résumé stdout. `--stats` : JSON vers stdout (voir [Vérifier l'installation](#vérifier-linstallation) plus haut).
- **Enchaîne avec :** `/ux-discover` ensuite. `--stats` sert uniquement au diagnostic.

#### `/ux-mcp`: faire tourner le moteur comme serveur MCP

- **Quoi :** Démarre le moteur comme serveur Model Context Protocol sur stdio. 25 outils (le recommandeur, le linter, la persistance, le synthétiseur, le journal des décisions, l'extraction d'image, les manifestes de données, ainsi que la construction, l'import, l'amélioration, l'extension, l'export et le contrôle d'un design system) deviennent appelables depuis n'importe quel host compatible MCP, sans le plugin.
- **Quand l'utiliser :** Vous travaillez dans un autre host compatible MCP et voulez le même moteur. Vous faites tourner un pipeline multi-agents qui a besoin d'une source unique de contraintes de design. Vous voulez le recommandeur ou le linter comme processus de longue durée en CI.
- **Quand passer :** Vous êtes dans Claude Code avec le plugin installé ; les commandes slash atteignent déjà le moteur. Vous avez besoin d'une réponse ponctuelle ; `uxskill recommend` ou `uxskill lint` est plus simple.
- **Invocation :** `/ux-mcp`, ou `ux-mcp` depuis le shell après `pip install 'uxskill[mcp]'`.
- **Sortie :** Un serveur JSON-RPC sur stdio. Voir [Serveur MCP](#serveur-mcp-le-coup-asymétrique) et `commands/ux-mcp.md` pour la configuration par client.
- **Enchaîne avec :** Rien ; c'est un transport, pas une étape.

### Discovery et recommandation

#### `/ux-discover`: la fonction forçante (intake à 10 champs, cadrage, recommandation)

- **Quoi :** L'intake obligatoire de 10 champs que traverse chaque projet avant toute commande de génération. Type de projet, audience, objectif principal, ton, indispensables, interdits, marques de référence, stack, région, métrique de succès. **Pas d'improvisation.** Des phrases bannies (« moderne », « clean ») forcent l'utilisateur à être précis. Lance ensuite le recommandeur : les 5 recherches parallèles du moteur Python sur 12 manifestes renvoient un seul design system fusionné (Secteur → Style → Palette → Typographie → Motion + Composants + Marques exemplaires + Garde-fous).
- **Modes :** `--frame` capture le pour-qui, l'outcome, l'hypothèse et le signal de succès dans un bloc de cadrage à quatre champs, plus léger que l'intake complet. `--recommend` ne lance que le recommandeur, à partir d'un brief enregistré ou de flags ponctuels.
- **Quand l'utiliser :** Avant tout `/ux-design` ou `/ux-system`. Chaque fois qu'un brief précédent est devenu obsolète. `--frame` au démarrage d'un projet, d'un sprint ou d'une mission ponctuelle, ou en cours de route quand une conversation a dérivé. `--recommend` pour faire pivoter un produit qui paraît fatigué.
- **Quand passer :** Vous corrigez un bug (`/ux-fix`). Vous lancez uniquement une passe de linter (`/ux-lint`). Le brief n'a pas changé depuis la dernière session.
- **Invocation (Claude Code) :** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` ou `/ux-discover --recommend`.
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
- **Sortie :** `.ux/last-discovery.json` (le brief à 10 champs), `.ux/last-recommendation.json` (style choisi, palette, paire typographique, 5 meilleurs préréglages de motion, 12 meilleurs composants, 5 meilleures marques exemplaires, les 171 garde-fous d'anti-patterns actifs, plus justification) et, avec `--frame`, `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Enchaîne avec :** `/ux-design [extra brief]` → code frontend ancré sur la recommandation. `/ux-design --component <name>` → un composant aligné sur les contraintes découvertes. `/ux-system` → design system complet à partir de la recommandation. `/ux-lint` → vérifier le code généré.

### Génération

#### `/ux-design`: générer une surface élégante et anti-slop depuis un brief

- **Quoi :** Génère un artefact frontend complet, de qualité production (landing, site marketing, app shell) à partir du brief de discovery + recommandation. Dépêche `frontend-engineer` avec une direction créative issue des références anti-slop et arsenal. Le brief, ou un flag, choisit l'un des quatre modes :
  - **page** (par défaut) : une page complète ou une surface à plusieurs sections. Écrit `.ux/last-design.json`.
  - **`--component [name]`** : un composant unique de qualité production (bouton, modal, navbar, sidebar, carte, table, formulaire, graphique). Les quatre états d'interaction, accessible, fidèle à la marque. Cherche d'abord le composant dans `.ux/last-recommendation.json`, puis se rabat sur une requête directe au manifeste. Écrit `.ux/last-component.json`.
  - **`--dashboard`** : discipline de densité de données, layout bento, chiffres monospace tabulaires, motifs de sparkline, pas d'abus de cartes, couleurs d'état sémantiques, motion parcimonieuse. Pas un site marketing avec des graphiques collés dessus. Écrit `.ux/last-dashboard.json`.
  - **`--from-image <path>`** : lit une image de référence (PNG/JPG/WebP) en pure vision par ordinateur Pillow (palette dominante, polarité du fond, signal typographique), la confronte aux manifestes de palettes et de styles et construit à partir de la recommandation qui en résulte. `--extract-only` s'arrête après l'extraction. Écrit `.ux/last-image-extract.json`.
- **Quand l'utiliser :** « Dessine un », « construis-moi un », « génère une landing page », « crée un dashboard », « fais un composant », « construis un bouton », « dessine le panneau admin », « console opérateur », « tableau KPI », « fais-le comme cette capture », toute demande de livrable visuel en format libre.
- **Quand passer :** Vous voulez une revue, pas une construction (utilisez `/ux-audit` ou `/ux-critique`). Travail backend ou infrastructure.
- **Invocation :** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Sortie :** Code généré (HTML / Blade / JSX / Vue / Astro), plus le fichier d'état du mode.
- **Enchaîne avec :** `/ux-lint` → vérifier contre les garde-fous. `/ux-polish` → passe cosmétique. `/ux-a11y` → audit d'accessibilité. `/ux-copy` → revue microcopy. `/ux-fix` → appliquer les findings en commits atomiques.

#### `/ux-system`: générer un système de design starter complet

- **Quoi :** Propose un système de design starter complet pour un projet qui n'en a pas, tokens (couleur, typographie, espace, motion, rayon, ombre), docs de fondations, contrats de composants, appariements dark-mode, switcher de thème. Dépêche `design-system-architect`.
- **Quand l'utiliser :** « On n'a pas de système de design », « construis-nous un système », « propose des tokens », « quel devrait être notre thème », « monte notre DS ».
- **Quand passer :** Le projet a déjà un design system ; utilisez plutôt `/ux-design --component` sur le système existant. Backend ou infrastructure.
- **Invocation :** `/ux-system create` (le moteur de fondations), `/ux-system enhance --from <file>` (mesurer un système que vous avez déjà), `/ux-system extend --from <file> --add <foundation>` (le compléter sans le modifier), ou `/ux-system` (le flux 3.x ; lance d'abord la discovery si elle n'est pas déjà enregistrée).
- **Sortie :** `tokens.json`, `foundations.md`, contrats `components/*.md`, émission Tailwind / vanilla / SCSS optionnelle. Écrit `.ux/last-system.json` pour le contexte d'enchaînement.
- **Enchaîne avec :** `/ux-design --component` → construire sur le nouveau système. `/ux-design` → générer une surface avec les nouveaux tokens.

#### `/ux-motion`: traitement de motion

- **Quoi :** Génère la couche motion d'une surface, durées, easings, chorégraphie, fallbacks reduced-motion, discipline de performance. Audite également la motion existante contre les 5 dimensions (timing, easing, signification, reduced-motion, performance).
- **Quand l'utiliser :** « Contrôle de motion », « les animations sont-elles bonnes », « corrige la motion », « revois les animations », « audit motion », « passe perf sur la motion ».
- **Quand passer :** La surface n'a pas de motion (utilisez `/ux-audit` ou `/ux-polish`). Backend ou infrastructure.
- **Invocation :** `/ux-motion path/to/component.tsx` (mode audit) ou `/ux-motion --generate hero-entry` (génération).
- **Sortie :** Code mis à jour (en mode génération) ou rapport `.ux/last-motion.json` (en mode audit).
- **Enchaîne avec :** `/ux-fix` → appliquer les findings de motion. `/ux-polish` → resserrer.

### Audit et vérification

#### `/ux-lint`: linter déterministe à base de regex (sans LLM, compatible CI)

- **Quoi :** Lance 171 règles sur votre code. Aucun appel LLM. Sort en non-zéro sur Critical / High en CI. Source : `data/anti-patterns.json`. Les règles couvrent A11y (45), Contenu (35), Layout (18), Typographie (16), Motion (14), Visuel (14), Qualité (12), Couleur (10), Performance (5), Profondeur (2).
- **Quand l'utiliser :** Hook pre-commit. Porte de CI. Première passe rapide sur une grosse codebase avant de payer le coût d'`/ux-audit`. Après `/ux-design` dans n'importe quel mode pour vérifier la génération.
- **Quand passer :** Vous voulez une boucle de fix (le linter rapporte, il n'édite pas, enchaînez sur `/ux-polish --fix` ou `/ux-fix`). Vous voulez un jugement de goût (utilisez `/ux-critique`).
- **Invocation (slash) :** `/ux-lint src/`.
- **Invocation (CLI) :** `uxskill lint .` ou `python3 bin/ux-lint.py .` ou `bash bin/ux-lint.sh --ci --fail-on high`.
- **Invocation (CI) :**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Sortie :** Findings vers stdout (emplacement, id de règle, sévérité, preuve). Code de sortie 0 si propre, non-zéro sur Critical/High quand `--fail-on high` est posé.
- **Enchaîne avec :** `/ux-polish --fix` → contrepartie LLM sur les mêmes patterns. `/ux-fix` → applique les findings comme commits, triés par sévérité. `/ux-audit` → passe de raisonnement complète à 6 lentilles. `/ux-next` → laisser le conducteur décider.

#### `/ux-audit`: audit de design à 6 lentilles

- **Quoi :** Une revue structurée et opiniâtre contre six lentilles (clarté, hiérarchie, accessibilité, voix, motion, goût), produisant des findings étiquetés par sévérité. Rapport style Polaris. Lit d'abord `.ux/last-frame.json`, l'audience et l'outcome ancrent la sévérité de chaque finding.
- **Quand l'utiliser :** La surface existe et vous voulez une critique défendable. « Audit », « revois l'UX », « est-ce bon », « qu'est-ce qui cloche », « démonte-le ».
- **Quand passer :** La surface n'existe pas encore (utilisez `/ux-design`). L'utilisateur veut une seule lentille (utilisez la commande ciblée : `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). L'utilisateur veut une opinion de goût (utilisez `/ux-critique`). Backend ou infrastructure.
- **Invocation :** `/ux-audit https://example.com/pricing` ou `/ux-audit src/components/Pricing.tsx`.
- **Sortie :** Écrit `.ux/last-audit.json`, tableau `findings` de `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Enchaîne avec :** `/ux-fix` → appliquer les findings. `/ux-polish` → passe cosmétique. `/ux-design` → si refonte structurelle nécessaire.

#### `/ux-a11y`: audit WCAG 2.1 AA + vérifications de courtoisie élémentaire

- **Quoi :** Un audit WCAG 2.1 AA structuré, plus les vérifications de courtoisie élémentaire qui passent les outils automatiques mais blessent encore les vrais utilisateurs (visibilité du focus, spécificité des erreurs, préférences de motion, pièges clavier, dépendance à la couleur).
- **Quand l'utiliser :** Porte d'accessibilité pré-livraison. Après une refonte. « Contrôle d'accessibilité », « audit WCAG », « est-ce accessible », « revue a11y », « test lecteur d'écran », « contrôle de navigation clavier ».
- **Quand passer :** Pas orienté utilisateur. Backend ou infrastructure. Esquisses en cours.
- **Invocation :** `/ux-a11y https://example.com` (URL en direct préférée, les outils automatiques et le test clavier ne fonctionnent qu'en direct).
- **Sortie :** Écrit `.ux/last-a11y.json`, tableau `findings` de `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, tableau `beyond_wcag`, `severity_counts`.
- **Enchaîne avec :** `/ux-fix` → appliquer les findings en commits. `/ux-copy` → corriger les alt text et le câblage des erreurs de formulaire dans le cadre d'une passe copy.

#### `/ux-critique`: opinion de goût (3 réussites, 3 ratés, 1 coup stratégique)

- **Quoi :** L'opinion d'un designer, pas un audit structuré, pas un score de sévérité, juste une prise serrée et opiniâtre qui nomme ce qui marche, ce qui ne marche pas, et le seul coup stratégique qui changerait le plus.
- **Quand l'utiliser :** « Qu'est-ce que tu en penses », « c'est bon », « critique-moi ça », « avis honnête », « le vibe est juste », « ça nous ressemble », « on devrait expédier ».
- **Quand passer :** L'utilisateur veut explicitement un audit structuré (utilisez `/ux-audit`). Backend ou infrastructure.
- **Invocation :** `/ux-critique https://example.com`.
- **Sortie :** Écrit `.ux/last-critique.json`, 3 réussites, 3 ratés, 1 coup stratégique, plus de la prose.
- **Enchaîne avec :** `/ux-design` si la prise recommande la refonte. `/ux-polish` si la prise recommande de resserrer.

#### `/ux-copy`: revue + réécriture microcopy

- **Quoi :** Évalue chaque chaîne visible contre la rubrique de voix et produit une réécriture avant/après. Attrape : « le formulaire contient des erreurs » (générique), « John Doe » (placeholder), copy célébratoire enjoué d'IA, CTAs génériques, empty states morts, erreurs inutiles.
- **Quand l'utiliser :** La structure est bonne mais les mots sont faibles. « Revois le copy », « corrige le microcopy », « les messages d'erreur sont mauvais », « réécris-moi ça », « resserre les chaînes », « les boutons sonnent génériques », « cet empty state est mort ».
- **Quand passer :** Problèmes de layout (utilisez `/ux-audit` ou `/ux-polish`). Problèmes de copy liés à l'accessibilité comme les alt text (utilisez `/ux-a11y`). Backend ou infrastructure.
- **Invocation :** `/ux-copy src/views/checkout.blade.php`.
- **Sortie :** Écrit `.ux/last-copy.json`, tableau `strings` de `{location, severity, before, after, notes}`, plus rubrique + locales à traduire.
- **Enchaîne avec :** `/ux-fix` → appliquer les réécritures. `/ux-a11y` → recontrôler après les corrections de copy.

### Fix et polish

#### `/ux-fix`: appliquer les findings en commits atomiques

- **Quoi :** Lit le dernier rapport de `.ux/` (audit, copy, a11y, motion ou polish), valide l'arbre de travail et applique les findings comme commits atomiques via les bons sous-agents. Re-vérifie en relançant la commande d'origine.
- **Quand l'utiliser :** Après avoir lancé une commande de classe audit et passé en revue les findings. « Corrige les findings », « applique les fix », « lance la boucle de fix », « patche la surface », « fais les changements », « va corriger ça ».
- **Quand passer :** Pas de rapport préalable dans `.ux/`. L'arbre de travail est sale et l'utilisateur n'a pas accepté de stash/commit. Les fix demandent du jugement de design, pas une application mécanique (utilisez `/ux-design` pour une refonte).
- **Invocation :** `/ux-fix` (auto-détecte le rapport à corriger) ou `/ux-fix --from=last-a11y.json`.
- **Sortie :** Commits atomiques par finding. Relance la commande d'origine et met à jour le fichier `.ux/last-*.json`. Affiche un résumé.
- **Enchaîne avec :** `/ux-next` → le conducteur choisit le prochain coup.

#### `/ux-polish`: boucle lint, fix, re-lint + élimination du slop IA

- **Quoi :** D'abord une boucle déterministe sur un fichier HTML local : lint, six passes de polish idempotentes, re-lint, jusqu'à ce que le score atteigne 90, stagne ou que trois tours soient passés (`--rounds` change la limite). Par défaut, la sortie de la boucle reste dans `<file>.evolved.html` et l'original n'est jamais touché. Seuls `--loop-only` ou `--fix` remplacent l'original, après une vérification d'arbre propre, et une porte qualité à 65 empêche un résultat en échec de le remplacer sans `--force` ; avec `--brand-file`, le plancher de fidélité à la marque tient à chaque sortie. Puis la passe de goût : rythme de l'espacement, hiérarchie affûtée, détection du slop IA, cohérence des tokens. La contrepartie pilotée par LLM de `/ux-lint`, qui s'appuie sur votre jugement pour les questions de goût. `--loop-only` ne lance que la boucle ; `--no-loop` seulement la passe de goût ; `--fix` applique les constats de goût.
- **Quand l'utiliser :** La structure est bonne mais l'exécution est lâche. « Polis ça », « resserre », « enlève le slop IA », « rends-le premium », « rends-le moins IA », « l'espacement sonne faux », « ça paraît générique », « il faut plus de goût », « améliore jusqu'à un score de 90+ », « rends-le prêt à livrer ».
- **Quand passer :** La surface manque d'une fonctionnalité centrale (corrigez ça d'abord). Il faut une refonte, pas un polish (utilisez `/ux-design`). Problèmes de copy (utilisez `/ux-copy`). Problèmes de motion (utilisez `/ux-motion`). Problèmes a11y (utilisez `/ux-a11y`).
- **Invocation :** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Sortie :** `<file>.evolved.html` issu de la boucle (promu à la place de l'original uniquement avec `--loop-only` ou `--fix`), code mis à jour avec `--fix`, `.ux/last-evolve.json`, une ligne dans `.ux/decisions.jsonl` et `.ux/last-polish.json` qui décrit les constats de goût.
- **Enchaîne avec :** `/ux-lint` → vérifier que le polish a tenu. `/ux-a11y` → recontrôler l'accessibilité.

### Discovery et narration

#### `/ux-research`: planification + synthèse de recherche

- **Quoi :** Mode planification : rédige scripts d'entretien, sondages, filtres de recrutement. Mode synthèse (`--synthesize`) : digère entretiens, analytics, sites concurrents, résultats A/B, tickets de support en recommandations. Dépêche `research-synthesizer`.
- **Quand l'utiliser :** « Planifie une étude de recherche », « j'ai besoin de questions d'entretien », « dessine un sondage », « comment je recrute des users », « plan de user testing », « étude journal », « test de préférence », « fake door », « smoke test », « synthétise mes notes d'entretien ».
- **Quand passer :** La réponse est déjà connue avec haute confiance. Décisions réversibles à faible risque. Backend ou infrastructure.
- **Invocation :** `/ux-research --plan "loyalty wallet adoption in MENA"` ou `/ux-research --synthesize interviews/*.md`.
- **Sortie :** Écrit `.ux/last-research.json`, plan de recherche ou thèmes synthétisés + preuves + recommandations.
- **Enchaîne avec :** `/ux-discover --frame` → intégrer les constats dans un cadre. `/ux-design` → générer à partir des constats. `/ux-workshop` → animer un atelier en utilisant la recherche comme entrée.

#### `/ux-workshop`: atelier de design thinking en 5 phases

- **Quoi :** Anime un atelier discovery / design thinking de bout en bout. Cinq phases séquentielles (exploration → carte de chaleur → carte des acteurs → croquis de solution → plan de jeu). Chronométré. Artefacts concrets par phase. Se termine par une décision, pas par « findings intéressants ».
- **Quand l'utiliser :** Vraie question, vrais participants, vrai budget temps. « Anime un atelier », « facilite un discovery », « faisons une session de design thinking », « j'ai des stakeholders pendant une heure, qu'est-ce qu'on fait », « lance le projet ».
- **Quand passer :** Brief déjà clair et cadré. Brainstorm solo (utilisez `/ux-design` ou `/ux-discover --frame`). L'équipe est en pleine exécution, pas en discovery.
- **Invocation :** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Sortie :** Écrit `.ux/last-workshop.json`, plan de jeu + artefacts par phase.
- **Enchaîne avec :** `/ux-design` → exécuter le plan de jeu. `/ux-research` → combler les manques que l'atelier a fait remonter. `/ux-case-study` → publier le parcours.

#### `/ux-case-study`: étude de cas publiable (format éditorial Wfrah)

- **Quoi :** Génère une étude de cas de projet en format éditorial monochrome pur, typographie Wfrah, séparateurs filaires, codes de section numérotés de (A) à (G), mise en page sûre en bilingue. Un document, pas une brochure marketing. Lit depuis `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Quand l'utiliser :** Post-lancement. Après un jalon discret. « Écris une étude de cas », « étude de cas ce projet », « fais le doc de clôture », « publie ce travail », « pièce portfolio ».
- **Quand passer :** Le projet manque de données pour remplir les sections (A) à (G). L'utilisateur veut une landing marketing, pas une étude de cas (utilisez `/ux-design`).
- **Invocation :** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Sortie :** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Enchaîne avec :** Commande terminale, généralement la fin d'un projet.

### Conductor

#### `/ux-next`: conducteur de workflow (lecture seule)

- **Quoi :** Lit chaque `.ux/last-*.json` et nomme la prochaine commande au plus fort effet de levier. Un conducteur, pas un constructeur. Lecture seule.
- **Quand l'utiliser :** Entre deux commandes. « Qu'est-ce que je devrais faire ensuite », « quel est le prochain coup », « décide pour moi », « on va où à partir d'ici ».
- **Quand passer :** Pas de rapports préalables dans `.ux/`. Vous avez une commande suivante précise en tête.
- **Invocation :** `/ux-next` (sans args) ou `/ux-next --focus=a11y`.
- **Sortie :** Stdout, commande recommandée + justification.
- **Enchaîne avec :** Celle qu'il choisit.

#### `/ux-expert`: crochet de conseil

- **Quoi :** Fait remonter les coordonnées du créateur du plugin quand un utilisateur demande un véritable expert UX. Bref, direct, sans marketing.
- **Quand l'utiliser :** « Qui a construit ça », « j'ai besoin d'un expert UX », « tu fais du conseil », « je peux engager quelqu'un pour ça », « il y a un humain derrière ce plugin ».
- **Quand passer :** L'utilisateur pose une question sur les fonctionnalités du plugin, pas sur le conseil.
- **Invocation :** `/ux-expert`.
- **Sortie :** Carte de contact brève avec LinkedIn / email / dépôt.

### Alias, retirés en 4.1

Sept commandes de la 3.x ont fusionné dans les 18 ci-dessus. Leurs noms fonctionnent encore le temps d'une version : chaque alias indique où il a déménagé, puis lance la nouvelle commande avec les mêmes arguments.

| Ancienne commande | Désormais | Notes |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | Même bloc de cadrage, même `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | L'outil MCP `ux_recommend` ne change pas |
| `/ux-stats` | `/ux-init --stats` | Instantané en lecture seule |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | L'alias garde l'ancienne limite de cinq tours ; `/ux-polish` seul s'arrête à trois |
| `/ux-component` | `/ux-design --component` | Même `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | Même `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Retirez `--extract-only` pour construire à partir de l'image |

### Graphe d'enchaînement des commandes

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

## Les 5 sous-agents

Les sous-agents sont des générateurs spécifiques par rôle dépêchés par les commandes. Ils ne tournent jamais de manière indépendante, ils sont appelés par `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research`, etc. Chaque agent a un périmètre de responsabilité défini : il NE décide PAS du brief ; il l'exécute.

### `frontend-engineer`

- **Possède :** Le code frontend de qualité production (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) avec discipline anti-slop IA.
- **Dépêché par :** `/ux-design` (modes page, composant, dashboard et image), `/ux-fix`.
- **Entrées :** Brief + direction créative + tokens (depuis `.ux/last-recommendation.json`).
- **Sorties :** Du code qui marche, distinguable de l'output IA générique. Pas de dégradés violets, pas de hero centré, pas de trois cartes égales, pas d'Inter en taille display, pas de « John Doe », pas d'emoji, pas de défaut à 300 ms.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Possède :** La motion dans le code frontend de production, Framer Motion, GSAP, animations CSS. Durées, easings, chorégraphie, fallbacks reduced-motion, discipline de performance.
- **Dépêché par :** `/ux-design` (tous les modes), `/ux-motion --fix`.
- **Entrées :** Brief de motion + tokens + les 57 préréglages de motion de `data/motion-presets.json`.
- **Sorties :** De la motion qui gagne sa place. Toujours encapsulée dans des fallbacks `prefers-reduced-motion`. Toujours testée contre les Core Web Vitals.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Possède :** Les chaînes qui partent en production, messages d'erreur, empty states, CTAs, loading states, messages de succès, toasts, texte d'aide, libellés de formulaire, texte des boutons.
- **Dépêché par :** `/ux-copy --fix`, `/ux-design` (tous les modes), `/ux-discover --frame`.
- **Entrées :** Profil de voix (nommé ou collé) + les chaînes de la surface.
- **Sorties :** Du microcopy production appliqué de manière cohérente à chaque état d'une surface pour que le produit sonne comme un produit, pas dix. Bannis : « le formulaire contient des erreurs », « John Doe », copy célébratoire enjoué d'IA, CTAs génériques, empty states morts.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Possède :** La digestion des entrées de recherche (entretiens, analytics, sites concurrents, résultats A/B, tickets de support) en recommandations de design actionnables.
- **Dépêché par :** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Entrées :** Recherche brute, transcripts, exports, URLs concurrents, clusters de support.
- **Sorties :** Thèmes, preuves, recommandations. Ne dessine jamais la réponse, donne au designer le substrat depuis lequel concevoir.
- **Tools :** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Possède :** Les systèmes de design complets, tokens (couleur, typographie, espace, motion, rayon, ombre), docs de fondations, contrats de composants, appariements dark-mode, couche de theming.
- **Dépêché par :** `/ux-system`, `/ux-design --component` quand aucun système n'existe.
- **Entrées :** Brief de marque + `.ux/last-recommendation.json` (style + palette + paire typographique + préréglages motion).
- **Sorties :** Un système cohérent, opiniâtre, prêt pour la production contre lequel les agents en aval peuvent construire sans re-décider les fondamentaux. Tokens JSON, fondations MD, contrats de composants, mapping dark-mode.
- **Tools :** `Read, Write, Edit, Bash, Glob, Grep`.

### Protocole de dépêche des sous-agents

Quand une commande dépêche un sous-agent, elle passe :

1. Le brief / la recommandation (chargés depuis `.ux/`).
2. La tranche de manifeste pertinente (par ex. `frontend-engineer` reçoit le style + la palette + les composants choisis ; `motion-engineer` reçoit les préréglages de motion choisis).
3. Les 171 garde-fous d'anti-patterns (toujours actifs).
4. Un critère de succès (ce que l'artefact doit faire).

Les sous-agents renvoient :

1. L'artefact (code, doc, système).
2. Un bloc de justification (pourquoi ces choix).
3. Une auto-vérification contre les garde-fous (quelles règles ils ont vérifiées).

La commande appelante lance ensuite `/ux-lint` automatiquement avant de déclarer la chose faite.

---

## Les 11 manifestes de données

La couche de données est le cerveau. Chaque commande lit dedans ; le moteur fusionne à travers ; le linter scanne contre. Tous les fichiers vivent sous `data/` et enveloppent leurs entrées dans `{_meta, entries}` pour le versioning de schéma.

### `styles.json`: 84 styles de design

| Champ | Description |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimaliste / Suisse, Brutaliste, Éditorial, Glassmorphisme, Néomorphisme, Bento, Skeuomorphique, Industriel, Maximaliste, IA-Futuriste, MENA-moderne, Vaporwave, etc. |
| `sample entry` | `swiss-international`, « La grille fait loi. La typographie fait le gros du travail. La décoration, c'est l'échec. » |

Utilisé par : `/ux-discover`, `/ux-system`, `/ux-design`. Schéma : [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 palettes de couleur

| Champ | Description |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (clair/sombre), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | chaleureux, éditorial, magazine, clinique, joueur, brutaliste, monochrome, joyau, MENA-chaud, dev-tools-sombre, etc. |
| `sample entry` | `claude-warm-editorial`, clair, chaleureux/éditorial/magazine, canvas #faf9f5, primary #cc785c |

Utilisé par : `/ux-discover`, `/ux-system`. Contraste vérifié AA / AAA. Schéma : [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 appariements typographiques

| Champ | Description |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Toutes les familles ont licence + URL source. Utilisé par `/ux-discover`, `/ux-system`.

### `components.json`: 148 composants

| Champ | Description |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Formulaires, Affichage de données, Feedback, Overlays, Layout, Contenu, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Méga Navigation, Grille de Produit, anatomie en 6 parties, 4 états |

C'est notre plus grand fossé concurrentiel. Aucun autre plugin UX pour Claude ne livre un manifeste structuré de composants.

### `industries.json`: 184 règles sectorielles

| Champ | Description |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Services Financiers, Santé, Éducation, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Voyage, Immobilier, Spécifique MENA, etc. |
| `sample entry` | `fintech-neobank`, forte confiance, disclosures réglementaires, UI primaire balance/transaction, mobile-first d'usage quotidien |

Utilisé par le recommandeur (`/ux-discover`) comme premier axe de recherche parallèle.

### `chart-types.json`: 35 types de graphique

| Champ | Description |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparaison, Séries Temporelles, Distribution, Composition, Relation, Flux, Géographique |
| `sample entry` | `bar-vertical`, comparer de 4 à 15 catégories discrètes. La position sur l'axe x porte la catégorie ; la hauteur porte la valeur. |

Utilisé par `/ux-design --dashboard` et `/ux-design --component` (instances de graphique).

### `tech-stacks.json`: 25 stacks

| Champ | Description |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, expérimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, compatible avec Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Les autres stacks incluent Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 lois UX nommées

| Champ | Description |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Coût de Décision, Attention, Mémoire, Contrôle Moteur, Perception Visuelle, Social, Émotionnel, Formulaires, Gestion d'Erreurs, Onboarding, Empty State, etc. |
| `sample entry` | `hicks-law`, Le temps de décision croît logarithmiquement avec le nombre d'options présentées |

Utilisé par `/ux-audit` (scoring à 6 lentilles) et `/ux-critique` (ancre de goût).

### `motion-presets.json`: 57 préréglages de motion

| Champ | Description |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entrée, Sortie, Hover, Focus, Tap, Loading, Empty, Success, Error, Lié au scroll |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Chaque préréglage a une variante reduced-motion. Code prêt par stack pour Framer Motion, GSAP et CSS pur.

### `anti-patterns.json` : 171 règles

| Champ | Description |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, motif, flags, portée et, pour beaucoup de règles, un contrôle `post` sur le fichier analysé), `why`, `fix` |
| `categories` | A11y (45), Contenu (35), Layout (18), Typographie (16), Motion (14), Visuel (14), Qualité (12), Couleur (10), Performance (5), Profondeur (2) |

La liste complète des règles se trouve dans [Les 171 règles anti-slop IA](#les-171-règles-anti-slop-ia--le-linter).

### `brands/*.json`: 160 specs de marque

| Champ | Description |
|---|---|
| `entries` | 160 (plus `_index.json` qui les liste toutes) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automobile (8) |

Liste complète dans [Les 160 spécifications DESIGN.md de marque](#les-160-spécifications-de-marque-designmd-par-catégorie).

---

## Les 171 règles anti-slop IA : le linter

ux-skill livre un linter déterministe : chaque règle est un motif, et beaucoup ajoutent un contrôle sur le CSS et le balisage analysés, si bien qu'une correspondance ne compte que dans le contexte qu'elle nomme. **Pas de LLM.** **Pas d'API.** **Pas de réseau.** Tourne en CI en ~200 ms sur une app Next.js typique. Sort en non-zéro sur les constats Critical / High quand `--fail-on high` est défini.

Les règles proviennent de `data/anti-patterns.json` (v2, préféré) avec `references/foundations/anti-patterns.md` en repli (v1, bash). Deux binaires sont livrés : `bin/ux-lint.py` (Python, rapide, extensible) et `bin/ux-lint.sh` (Bash + perl-PCRE, pour les environnements sans Python).

### Règles par catégorie

Le catalogue complet des 171 règles, par catégorie puis par sévérité, est généré depuis `data/anti-patterns.json` dans le [README anglais](README.md#rules-by-category) ; les identifiants et les noms des règles y figurent tels que le linter les affiche. Les règles couvrent A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### Utilisation du linter

**Scan ponctuel :**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## Les 160 spécifications de marque DESIGN.md: par catégorie

Vraies marques. Vrais langages de design. Vraies specs DESIGN.md, pas des palettes génériques. Vous dites au plugin « construis une landing dans le style de Stripe » et il lit le vocabulaire de marque réel : rubrique de voix, tokens de couleur, conventions de motion, signature moves, anti-moves.

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

Les 8 autres plugins UX populaires pour Claude génèrent du « minimal moderne » ou du « dashboard clean », variantes de la même esthétique par défaut. ux-skill vous permet de demander **la clarté de Linear**, **le sérieux de Stripe**, **la retenue d'Apple**, **le monolithe de Tesla**, **la convivialité de Notion**, **la discipline des dégradés de Cursor**, **la densité filaire de Raycast**, **le chaleureux éditorial de Claude**, et le moteur tire les bons tokens, la voix, les conventions de motion et les signature moves depuis la spec de marque.

---

## Serveur MCP: le coup asymétrique

ux-skill livre un **serveur Model Context Protocol**. Lancez `ux-mcp` et le moteur devient un processus stdio de longue durée que n'importe quel host compatible MCP (Claude Desktop, Cursor, Windsurf, agents génériques) peut appeler. 25 outils : `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Mêmes handlers Python que les commandes slash ; mêmes manifestes de données ; même recommandeur déterministe.

**Pourquoi c'est le coup asymétrique :** aucune des huit meilleures skills UX pour Claude (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ne livre de serveur MCP. Elles sont verrouillées à l'intérieur du runtime de plugin Claude Code. ux-skill est joignable depuis n'importe quel host qui parle MCP, y compris des agents qui n'ont jamais entendu parler d'un plugin Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Pointez votre client sur le binaire `ux-mcp`. Documentation complète des outils, exemples JSON et config par client pour Claude Desktop, Cursor et Windsurf sur [docs/mcp.html](docs/mcp.html) et dans `commands/ux-mcp.md`.

---

## L'installateur pour 17 IDEs

`uxskill init` (ou `/ux-init` à l'intérieur de Claude Code) auto-détecte l'IDE que vous utilisez et écrit le bon artefact. Même moteur Python. Mêmes recommandations. Glue différente par IDE.

| IDE / Outil | Signal de détection | Artefact installé |
|---|---|---|
| Claude Code | `.claude/` ou `CLAUDE.md` | Manifeste de plugin à `.claude-plugin/plugin.json` + les 18 commandes (et 7 alias) + les 5 sous-agents |
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

## Cas d'usage: scénarios concrets

Huit scénarios réels. Choisissez celui le plus proche de votre situation et adaptez l'invocation.

### 1. Construire un dashboard fintech dans Cursor

Vous êtes dans Cursor en train de travailler sur un dashboard de néobanque MENA. Vous installez le plugin et lancez discovery, recommandation, puis génération du dashboard.

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

Puis dans Cursor, vous demandez : *« Génère la surface du dashboard en utilisant la recommandation dans .ux/last-recommendation.json »*. Cursor lit l'en-tête `.cursorrules`, charge la recommandation, dépêche une génération de dashboard avec des contraintes explicites.

### 2. Générer une landing au style Stripe dans Claude Code

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Trois commandes, une surface polie, commits atomiques par correctif.

### 5. Concevoir une command palette au style Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

Le composant généré utilise les tokens de couleur réels de Linear, son stack typographique, ses conventions de motion, ses densités filaires, pas « UI sombre générique ».

### 6. Animer un atelier de design thinking de 90 minutes avec des stakeholders

Vous avez une salle de 5 personnes pour 90 minutes. Vous voulez qu'elles repartent avec un plan de jeu, pas avec un vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Le plugin facilite les cinq phases (exploration → carte de chaleur → carte des acteurs → croquis de solution → plan de jeu) de bout en bout, chronométrées, avec des artefacts concrets par phase. La sortie est `.ux/last-workshop.json`, le plan de jeu, pas juste « des findings intéressants ».

### 7. Écrire une étude de cas publiable après lancement

Vous avez expédié le wallet de fidélité. Vous voulez une pièce portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

L'étude de cas est un artefact fini, publiable, pas un brouillon. Monochrome pur, typographie éditoriale, prêt à publier sur votre portfolio.

### 8. Lancer la discovery dans un contexte non-IA (juste l'intake structuré)

Vous cadrez un projet. Vous n'avez pas encore besoin d'une recommandation, vous avez besoin d'un brief structuré.

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

Vous pouvez remettre le JSON à votre équipe, le coller dans un doc Notion ou l'alimenter à un autre outil IA. ux-skill est aussi un outil d'intake structuré, en plus d'être un moteur.

### 9. Persistance MASTER.md: vos décisions de design, dans le dépôt

Après `/ux-discover` (ou `/ux-discover --recommend`), enregistrez le style choisi + palette + typographie + motion + composants + marques exemplaires + garde-fous dans un fichier Markdown lisible que votre équipe peut relire, comparer et versionner.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Écrit `.ux/design-system/MASTER.md` (frontmatter YAML + corps) et `.ux/design-system/pages/<name>.md` par surface générée via `persist save-page`. Idempotent, la même entrée produit une sortie identique octet pour octet, donc relancer sur un état inchangé est un no-op en git.

---

## Face aux alternatives

Table récapitulative courte. La comparaison complète côte à côte est sur [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimension | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Commandes slash | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Composants | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Préréglages motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Specs de marque | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Règles d'anti-patterns | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter déterministe compatible CI | **oui** | non | non | non | non | non | non | non | non |
| IDEs pris en charge | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Porte de discovery | **10 champs** | implicite | implicite | implicite | implicite | implicite | implicite | implicite | implicite |
| Chaîne d'état `.ux/` | **oui** | non | non | non | non | non | non | non | non |
| Étoiles (2026-05-28) | 14 | 83 958 | 54 406 | 25 202 | 15 455 | 5 762 | 2 391 | 2 164 | 955 |

### Évaluation honnête

- **ui-ux-pro-max** est plus grand en notoriété, livre 18 IDEs, a une recherche style BM25 sur son CSV. Il ne livre pas de manifeste de composants, manifeste de motion, bibliothèque de marques ni linter déterministe.
- **open-design** a 19 skills + preview mais seulement support Claude Code et pas de couche anti-slop.
- **hallmark** est le plus proche en esprit (aussi anti-slop) mais c'est une skill unique, pas de moteur, pas de manifestes, pas de commandes enchaînées.
- **material-3-skill** est excellent si vous voulez spécifiquement Material Design 3. Nous ne concurrencons pas sur MD3.

Pour le détail complet par dimension, voir [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Feuille de route

Ensuite, sans version fixée :

- **Styles Figma** : styles d'effet pour les ombres, styles de grille et styles de texte liés aux variables de champ, écrits dans un fichier vivant.
- **Correspondance des composants** : un composant Figma et ses variantes reliés à un composant de code et à ses props, conservés tout au long du passage de relais.
- **Un importeur de site en ligne** : lire le système qu'un site publié rend réellement, à côté des importeurs de fichiers.
- **Pages de documentation pour un système construit** : la vue humaine de ses tokens, rôles et contrats.

Également ouverts :

- **`uxskill lint --fix` pour des réécritures sûres** des constats corrigeables mécaniquement (button-no-type, img-no-alt en chaîne vide, suppression de console-log-leak).
- **Extension VS Code** qui affiche les constats du lint dans le code.
- **Émission de code par composant** dans six stacks (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Place de marché de spécifications de marque** : publier et découvrir les spécifications de marque de la communauté.
- **Règles d'anti-patterns personnalisées** : découverte et partage des règles que les projets définissent dans `data/anti-patterns.local.json`.
- **`uxskill plan`** : planification de sites de plusieurs pages à partir d'un brief, pas seulement d'une surface.

---

## Contribuer

Issues et PRs bienvenues. Trois zones à fort effet de levier :

### Ajouter une règle d'anti-pattern

1. Éditez `data/anti-patterns.json`, ajoutez une entrée avec `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Ajoutez un test dans `tests/linter/`, un fichier qui déclenche la règle, un qui ne la déclenche pas.
3. Lancez `uxskill lint tests/linter/should-trigger/<rule>.tsx`, confirmez qu'elle se déclenche. Lancez sur `tests/linter/should-not-trigger/<rule>.tsx`, confirmez qu'elle ne se déclenche pas.
4. Ouvrez une PR.

### Ajouter une spec de marque

1. Créez `data/brands/<slug>.json` avec `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Ajoutez la prose correspondante à `references/brands/<slug>.md`.
3. Enregistrez dans `data/brands/_index.json`.
4. Ouvrez une PR. La spec doit être adossée à des références de source primaire (le produit réel de la marque, son système de design public ou son DESIGN.md si elle en publie un).

### Ajouter un préréglage de motion

1. Éditez `data/motion-presets.json`, ajoutez une entrée avec `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Le préréglage doit avoir une variante reduced-motion. Sans exception.
3. Ouvrez une PR.

### Processus

- Lisez [CONTRIBUTING.md](CONTRIBUTING.md) pour le processus complet.
- Lisez [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Les nouvelles règles et specs de marque sont relues pour : ancrage en source primaire, absence d'overfitting à un projet unique, absence d'emoji dans toutes les données, comportement RTL-safe quand applicable.

---

## Licence, auteur, remerciements

### Licence

MIT. Utilisez-le, forkez-le, construisez dessus. S'il vous évite d'expédier du slop IA, mettez une étoile au dépôt, c'est la façon la moins chère de le soutenir.

### Auteur

**Laith Aljunaidy**: fondateur solo de [Dot](https://thedotwallet.com), une plateforme de fidélité MENA-first. Construisant ux-skill pour que le frontend généré par IA ne se ressemble plus tout pareil.

- LinkedIn : [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email : laith.aljunaidy.laith@gmail.com
- Dépôt : [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site : [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI : [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm : [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Remerciements

- L'équipe d'Anthropic pour Claude Code et l'architecture skill / plugin qui a rendu ceci distribuable.
- Nielsen Norman Group, Laws of UX (lawsofux.com) et la communauté de recherche UX dont le travail nourrit `data/ux-guidelines.json`.
- Chaque marque listée dans `data/brands/`, leurs systèmes de design publics sont la source de vérité pour les specs de marque.
- Les contributeurs originaux de la v1 : une skill Claude one-shot devenue la graine du moteur Python v2.
- Les 8 plugins UX populaires pour Claude auxquels nous nous sommes comparés, ils ont relevé la barre ; ceci est notre réponse.

---

**ux-skill** · **v4.0.0** · Construit pour que Claude Code, Cursor, Windsurf et tous les autres outils de codage par IA produisent du frontend qui ne se lit pas comme généré par IA.

> Mettez une étoile au dépôt sur [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Installez via `pip install uxskill` ou `npx uxskill init` · Parcourez la comparaison sur [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
