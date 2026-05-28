[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · **Türkçe**

# ux-skill — Claude Code, Cursor ve diğer her AI coding aracı için design intelligence motoru

> **AI coding için en güçlü UX plugin'i.** 11 sorgulanabilir JSON manifesti olan Python akıl yürütme çekirdeği (84 stil, 176 palet, 70 tipografik eşleşme, 148 component, 184 sektör, 35 chart tipi, 57 motion preset, 112 UX yasası, 145 anti-pattern kuralı, 25 tech stack, 160 brand specs), 22 slash komutu, 5 sub-agent ve deterministik anti-AI-slop linter. IDE'ler arası: Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer ve Roo Cline'a dağıtılır.

> **Brand adı `ux-skill`.** PyPI / npm paket adı `uxskill` olarak kalır. GitHub deposu [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill) adresinde.

**Site:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Her Claude UX plugin'i ile karşılaştırma:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.0.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-yükleyicisi)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-223_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Yıldız geçmişi

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill nedir

ux-skill, AI coding araçları için bir **design intelligence motoru**. Bir Python paketi olarak (`pip install uxskill`), Claude Code plugin'i olarak ve 17 IDE'lik multi-yükleyici olarak çalışır. Motor bir proje brief'ini (sektör, hedef kitle, ton, must-have, yasaklı hamleler, stack, bölge) alır ve eksiksiz bir önerilen design sistemi döndürür: stil, palet, tipografik çift, motion preset'leri, component'ler, çalışılacak örnek brand'ler ve tutulması gereken anti-pattern guardrail'ları. Öneri deterministik — aynı girdi her zaman aynı çıktıyı verir.

Plugin, sen ve AI coding aracı arasında durur. Claude Code'a, Cursor'a veya başka bir AI asistanına «bir fintech landing oluştur» dediğinde, asistan tipik olarak doğaçlama yapar — ve sonuç beş saniye içinde AI üretimi olarak okunur (mor-mavi gradyanlar, üç eşit card, display boyutunda Inter, testimonial'larda «John Doe», 300ms varsayılan geçişler, ortalanmış hero, zıplayan ok CTA'lar). ux-skill doğaçlamayı **yapılandırılmış kısıtlamalarla** değiştirir: brief'i yakalamak için `/ux-discover`, sistemi seçmek için `/ux-recommend`, kodu üretmek için `/ux-design` ve commit'ten önce 145 deterministik anti-AI-slop kuralından geçtiğini doğrulamak için `/ux-lint` çalıştırırsın.

Bu README kanonik referans. Her komut, her sub-agent, her data manifest, her install yolu, her brand spec, her anti-pattern kategorisi — hepsi burada belgelendi. Eğer Claude Code için bir design plugin'i arıyorsan ya da Cursor, Windsurf veya Codex için AI design araçlarını karşılaştırıyorsan, bunu baştan sona [compare.html](https://uxskill.laithjunaidy.com/compare.html) ile birlikte oku.

---

## İçindekiler

1. [Hızlı kurulum](#hızlı-kurulum)
2. [Sayılar — top 8 Claude UX skill'ine karşı canlı karşılaştırma](#sayılar--top-8-claude-ux-skilline-karşı-canlı-karşılaştırma)
3. [Mimari — parçalar nasıl birleşiyor](#mimari--parçalar-nasıl-birleşiyor)
4. [22 slash komutu — detaylı referans](#22-slash-komutu--detaylı-referans)
5. [5 sub-agent](#5-sub-agent)
6. [11 data manifest'i](#11-data-manifesti)
7. [145 anti-AI-slop kuralı — linter](#145-anti-ai-slop-kuralı--linter)
8. [160 brand DESIGN.md spec'i — kategoriye göre](#160-brand-designmd-speci--kategoriye-göre)
9. [MCP sunucusu — asimetrik hamle](#mcp-sunucusu--asimetrik-hamle)
10. [17 IDE yükleyicisi](#17-ide-yükleyicisi)
11. [Kullanım senaryoları — somut senaryolar](#kullanım-senaryoları--somut-senaryolar)
12. [Alternatiflerle karşılaştırma](#alternatiflerle-karşılaştırma)
13. [Roadmap](#roadmap)
14. [Katkıda bulunma](#katkıda-bulunma)
15. [Lisans, yazar, teşekkürler](#lisans-yazar-teşekkürler)

---

## Hızlı kurulum

Üç kurulum yolu. Ortamına uyanı seç.

### Yol 1 — Claude Code marketplace (kanonik)

Claude Code'da yaşıyorsan, plugin marketplace üzerinden kur:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Bu, 22 slash komutunun ve 5 sub-agent'ın hepsini Claude Code oturumuna bağlar. Kurulumdan sonra, projeye özel `.ux/` state dizinini kurmak ve Python motorunun erişilebilir olduğunu doğrulamak için `/ux-init` çalıştır.

### Yol 2 — pip (evrensel)

Claude Code dışında yaşıyorsan (Cursor, Windsurf, CLI, CI), Python paketini kur:

```bash
pip install uxskill
uxskill init                       # IDE'ni otomatik algılar, doğru artefaktı kurar
uxskill stats                      # kurulumu doğrulamak için manifest sayılarını yazdırır
uxskill lint .                     # geçerli dizine karşı linter'ı çalıştırır
```

Paket hem `ux` hem de `uxskill`'i CLI entry point'i olarak sunar — aynı binary.

### Yol 3 — npx (Python gerekmez)

Python'u doğrudan yönetmek istemiyorsan, npx wrapper her şeyi `pipx` üzerinden bootstrap'ler:

```bash
npx uxskill init                  # ilk çalıştırmada pipx + uxskill indirir
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Kurulumu doğrula

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

Herhangi bir sayı 0 dönerse, JSON dosyası eksik — [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) adresinde bir issue aç.

---

## Sayılar — top 8 Claude UX skill'ine karşı canlı karşılaştırma

Yıldız sayıları en son **2026-05-28**'de `gh api` ile doğrulandı. ux-skill (Laith0003/ux-skill) en yeni — farkındalıkta küçüğüz, mimaride derin. Aşağıdaki karşılaştırma dürüst: nerede kaybediyoruz, nerede kazanıyoruz.

| Plugin | Yıldız | Mimari | Slash komutları | Linter (CI-safe) | Brand spec'leri | Component'ler | Motion preset'leri | Desteklenen IDE'ler |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, tek skill | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + araştırma destekli taste | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Tek 62 KB SKILL.md + script'ler | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | MCP-bağlı skill kütüphanesi | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Tek estetik skill'i | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Anti-slop design skill'i | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 component'ler + audit | 1 | — | (sadece MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python motoru + 11 manifest + 22 komut + 5 sub-agent + CI linter** | **22** | **145 regex kuralı** | **160** | **148** | **57** | **17** |

### Nerede kaybediyoruz

- **Farkındalık.** Onların yüzbinlerce yıldızı var. Bizim 14. Bize yıldız ver — yardım etmenin en ucuz yolu.
- **Brand tanınırlığı.** ui-ux-pro-max ve open-design'ın günler değil aylarla ölçülen bir başlangıç farkı var.
- **Marketing parlatması.** Onların ekran görüntüleri, demo videoları ve bulunabilir bir landing'i var. Bizim kapsamlı bir README'miz ve zayıf bir landing'imiz var.

### Nerede kazanıyoruz

- **Component kütüphanesi:** Anatomi, durumlar, kullanılan token'lar ve motion özellikleri ile 148 belgelenmiş component. Diğer 8'in hiçbiri component manifest'i dağıtmıyor.
- **Motion preset'leri:** Reduced-motion fallback'leriyle stack-ready 57 giriş (Framer Motion, GSAP, CSS). Diğerlerinin hiçbiri motion manifest'i dağıtmıyor.
- **Anti-pattern linter:** 145 deterministik regex kuralı, CI'da çalışır, Critical/High'ta non-zero ile çıkar. Diğerlerinin hiçbiri deterministik linter dağıtmıyor.
- **Brand spec'leri:** 160 gerçek DESIGN.md spec (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude ve 96 daha). Diğerlerinin hiçbiri brand kütüphanesi dağıtmıyor.
- **17 desteklenen IDE:** aynı motor, IDE başına farklı yapıştırıcı.
- **22 slash komutu:** discovery, üretim, audit, lint, polish, fix loop, case-study, workshop, copy, motion, a11y, dashboard, conductor — tamamen entegre.

Tam tablo bazlı yan yana karşılaştırma için: [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Mimari — parçalar nasıl birleşiyor

```
ux-skill (paket adı: uxskill)
│
├── data/                              Beyin — sorgulanabilir JSON manifest'ler
│   ├── styles.json                    84 design stili + when/skip + token'lar
│   ├── palettes.json                  176 palet (light/dark, kontrast doğrulanmış)
│   ├── type-pairs.json                70 display × body × mono üçlüsü
│   ├── components.json                148 component (anatomi, durumlar, motion)
│   ├── industries.json                184 sektör kuralı + hedef kitle sinyalleri
│   ├── chart-types.json               35 chart tipi (when/skip, encoding)
│   ├── tech-stacks.json               25 stack (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 isimli UX yasası (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 motion preset'i (entry, exit, hover...)
│   ├── anti-patterns.json             145 regex kuralı (CI-safe linter kaynağı)
│   └── brands/*.json                  160 brand DESIGN spec'i + _index.json
│
├── engine/                            Python — akıl yürütme
│   ├── recommender/                   5-paralel-arama merge motoru
│   ├── linter/                        Deterministik anti-slop tarayıcı
│   ├── discovery/                     10 alanlı zorlayıcı protokol
│   ├── generator/                     Token + manifest emitter'ı
│   ├── installer/                     17 IDE multi-yükleyicisi
│   └── cli/                           `ux` / `uxskill` entry point'i
│
├── commands/                          22 Claude Code slash komutu (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    envanter anlık görüntüsü
│   ├── ux-discover.md                 10 alanlı intake (gate)
│   ├── ux-recommend.md                FLAGSHIP — 5 paralel arama
│   ├── ux-lint.md                     deterministik linter
│   ├── ux-design.md                   frontend kodu üretir
│   ├── ux-component.md                bir component üretir
│   ├── ux-system.md                   eksiksiz design sistemi üretir
│   ├── ux-dashboard.md                dashboard yüzeyi üretir
│   ├── ux-motion.md                   motion işlemi + audit
│   ├── ux-audit.md                    6 lensli design audit'i
│   ├── ux-a11y.md                     WCAG 2.1 AA audit'i
│   ├── ux-critique.md                 taste eleştirisi (3 kazanım, 3 ıskalama, 1 hamle)
│   ├── ux-copy.md                     microcopy incelemesi + yeniden yazım
│   ├── ux-fix.md                      bulguları atomik commit olarak uygular
│   ├── ux-polish.md                   kozmetik geçiş + AI-slop'u öldürme
│   ├── ux-frame.md                    4 alanlı framing bloğu
│   ├── ux-research.md                 araştırma planlama + sentez
│   ├── ux-workshop.md                 5 fazlı design thinking workshop'u
│   ├── ux-case-study.md               yayınlanabilir Wfrah-editorial case study
│   ├── ux-next.md                     workflow yöneticisi (read-only)
│   └── ux-expert.md                   danışmanlık bağlantısı
│
├── agents/                            5 sub-agent (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 brand sesiyle microcopy
│   ├── research-synthesizer.md        görüşmeler + analytics + rakipler
│   └── design-system-architect.md     token'lar / component'ler / foundation'lar
│
├── references/                        Veri + demo sayfaları için düzyazı kaynağı
│   ├── foundations/                   anti-patterns.md, prensipler, taste
│   ├── laws/                          UX yasaları uzun form
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        stil başına düzyazı (anti-slop.md, vs.)
│   ├── components/                    component uzun form
│   ├── output/                        output rubrikleri
│   └── conditional/                   stack-spesifik rehberlik
│
├── bin/
│   ├── uxskill.mjs                    npx wrapper -> Python motoru
│   ├── ux-lint.py                     v2 linter (tercih edilen)
│   └── ux-lint.sh                     v1 fallback (bash + perl-PCRE)
│
└── .ux/                               (her proje için oluşturulur)
    ├── last-discovery.json            brief anlık görüntüsü
    ├── last-recommendation.json       seçilen sistem
    ├── last-frame.json                framing bloğu
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Motor gerçekten nasıl çalışıyor

1. **Girdi.** Bir brief sağlarsın — `/ux-discover` (10 alan) ile interaktif olarak veya `ux recommend`'a flag'lerle non-interaktif olarak.
2. **5 paralel arama.** Motor manifest'ler üzerinde beş lookup'ı eşzamanlı çalıştırır:
   - **Sektör → recommended_styles** (industries.json)
   - **Stil → palet + tip + motion uyumluluğu** (styles.json)
   - **Ton × must-have → palet filtresi** (palettes.json)
   - **Stack → component uyumluluğu + motion preset'leri** (tech-stacks.json, motion-presets.json)
   - **Forbidden + bölge → guardrail'lar + brand örnek kısa listesi** (anti-patterns.json, brands/)
3. **Merge.** Deterministik bir merger adayları sıralar, çakışmaları çözer (örn. must-have dark-mode palet modunu zorlar) ve tek bir önerilen sistem emit eder.
4. **Çıktı.** Seçilen stil, palet, tipografik çift, top 5 motion preset'i, top 12 component, top 5 brand örneği ve aktif 145 anti-pattern guardrail'ının hepsiyle bir JSON dokümanı. Artı her seçimi açıklayan bir rationale bloğu.
5. **Üretim.** Aşağı komutlar (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) sub-agent'lar aracılığıyla gerçek kod üretmek için öneriyi tüketir.
6. **Doğrulama.** `/ux-lint` üretilen kodu 145 regex kuralına karşı yeniden tarar. CI'da Critical/High'ta non-zero ile çıkar.

**Python düşünür. HTML gösterir. Markdown zincirler.**

---

## 22 slash komutu — detaylı referans

Her komut `commands/` altında `.md` dosyası olarak dağıtılır: `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` ve `output state file` ile. Aşağıdaki açıklamalar yoğunlaştırılmış; tam kaynak kanonik spec'tir.

Komutlar beş kovaya gruplanmıştır: **bootstrap & envanter**, **discovery & öneri**, **üretim**, **audit & doğrulama**, **fix & polish** ve **conductor**.

### Bootstrap & envanter

#### `/ux-init` — projeyi bootstrap'le

- **Ne yapar:** Hangi IDE'yi kullandığını algılar (`.claude/`, `.cursor/`, `.windsurf/`, vs.), doğru artefaktı kurar, Python motorunun erişilebilir olduğunu doğrular, bir istatistik anlık görüntüsü yazdırır.
- **Ne zaman kullan:** Yeni bir projeye ilk yükleme. ux-skill kullanan bir projeyi klonladıktan sonra. `pip install --upgrade uxskill` sonrası.
- **Ne zaman atla:** Bu projede zaten çalıştırdın ve hiçbir şey değişmedi.
- **Çağırma:** `/ux-init` (argüman yok) veya CLI'dan `uxskill init`.
- **Çıktı:** IDE başına artefakt ([17 IDE yükleyicisi](#17-ide-yükleyicisi)'ne bak) + `.ux/` dizini + stdout özeti.
- **Bağlanır:** Sırada `/ux-discover`.

#### `/ux-stats` — veri envanterini yazdır

- **Ne yapar:** 11 data manifest'i için sürüm + giriş sayılarını yazdırır, böylece neyin kurulu olduğunu doğrulayabilirsin.
- **Ne zaman kullan:** Kurulum sonrası. Yükseltme sonrası. `/ux-recommend` şaşırtıcı seçimler döndürdüğünde ve manifest'lerin eksik olduğundan şüphelendiğinde.
- **Ne zaman atla:** Asla — 50ms'lik read-only bir komut.
- **Çağırma:** `/ux-stats` veya `uxskill stats`.
- **Çıktı:** stdout'a JSON (yukarıdaki [Kurulumu doğrula](#kurulumu-doğrula)'ya bak).
- **Bağlanır:** Sadece tanı; aşağıyı beslemez.

### Discovery & öneri

#### `/ux-discover` — zorlayıcı fonksiyon (10 alanlı intake)

- **Ne yapar:** Her projenin herhangi bir üretim komutundan önce geçtiği zorunlu 10 alanlı intake. Proje tipi, hedef kitle, birincil hedef, ton, must-have, forbidden, referans brand'ler, stack, bölge, başarı metriği. **Doğaçlama yok.** Yasaklı ifadeler («modern», «clean») kullanıcıyı spesifik olmaya zorlar.
- **Ne zaman kullan:** Herhangi bir `/ux-design`, `/ux-component`, `/ux-system` veya `/ux-dashboard`'dan önce. Önceki bir brief eskidiğinde.
- **Ne zaman atla:** Bir bug'ı düzeltiyorsun (`/ux-fix`). Sadece bir linter geçişi çalıştırıyorsun (`/ux-lint`). Brief son oturumdan değişmedi.
- **Çağırma:** `/ux-discover`. Plugin sorar; sen cevaplarsın.
- **Çıktı:** `.ux/last-discovery.json` yazar (10 alanlı brief).
- **Bağlanır:** `/ux-recommend` → stil + palet + tip + motion + component'leri seçmek için discovery'yi kullanır. `/ux-design [ek brief]` → öneriye dayalı frontend kodu üretir. `/ux-component <isim>` → keşfedilen kısıtlamalara uygun bir component üretir.

#### `/ux-recommend` — flagship 5-paralel-arama motoru

- **Ne yapar:** Python motorunun 11 manifest üzerindeki 5-paralel-aramasını çalıştırır ve birleşik bir design sistemi döndürür. Sektör → Stil → Palet → Tip → Motion + Component'ler + Brand Örnekleri + Guardrail'lar.
- **Ne zaman kullan:** Sıfırdan yeni bir projeye başlarken. Yorgun görünümlü bir ürünü pivotlarken. Herhangi bir `/ux-design` veya `/ux-component`'tan önce pre-flight.
- **Ne zaman atla:** `/ux-discover`'ı zaten çalıştırdın ve bir brief kaydettin — o akışta `/ux-recommend` otomatik. Bir bug'ı düzeltiyorsun (`/ux-fix` kullan). Sadece lint çalıştırman gerek (`/ux-lint` kullan).
- **Çağırma (Claude Code):**
  ```
  /ux-recommend
  ```
  **Çağırma (CLI):**
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
- **Çıktı:** `.ux/last-recommendation.json` yazar — seçilen stil, seçilen palet, seçilen tipografik çift, top 5 motion preset'i, top 12 component, top 5 brand örneği, aktif 145 anti-pattern guardrail'ı, artı rationale.
- **Bağlanır:** `/ux-design [brief]` → önerilen token'ları kullanan frontend kodu. `/ux-system` → öneriden eksiksiz design sistemi. `/ux-component <isim>` → önerilen stili kullanan bir component. `/ux-lint` → üretilen kodu doğrula.

### Üretim

#### `/ux-design` — brief'ten güzel, anti-slop bir yüzey üretir

- **Ne yapar:** Discovery brief'i + öneriden eksiksiz, production-grade bir frontend artefaktı (landing, marketing sitesi, app shell) üretir. anti-slop ve arsenal referanslarından gelen yaratıcı yönlendirmeyle `frontend-engineer`'ı görevlendirir.
- **Ne zaman kullan:** «Design a», «build me a», «generate a landing page», «create a dashboard», «make a component» — serbest formatlı görsel teslimat isteği.
- **Ne zaman atla:** İnceleme istiyorsun, build değil (`/ux-audit` veya `/ux-critique` kullan). Sadece bir component istiyorsun (`/ux-component` kullan). Backend veya altyapı işi.
- **Çağırma:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Çıktı:** Üretilen kod (HTML / Blade / JSX / Vue / Astro), artı `.ux/last-design.json`.
- **Bağlanır:** `/ux-lint` → guardrail'lara karşı doğrula. `/ux-polish` → kozmetik geçiş. `/ux-a11y` → erişilebilirlik audit'i. `/ux-copy` → microcopy incelemesi. `/ux-fix` → bulguları atomik commit olarak uygula.

#### `/ux-component` — bir component üretir

- **Ne yapar:** Bir spec'ten tek bir production-grade component üretir (button, modal, navbar, sidebar, card, table, form, chart). Dört etkileşim durumunun hepsi, erişilebilir, on-brand. Önce `.ux/last-recommendation.json`'da component'i arar, doğrudan manifest sorgusuna geri döner.
- **Ne zaman kullan:** Herhangi bir tek-element isteği — «build a button», «create a pricing card», «make a modal», «add a navbar», «design a sidebar», «I need a data table», «build a form», «make a chart component».
- **Ne zaman atla:** Tam sayfa veya çok bölümlü yüzey (`/ux-design` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Çıktı:** Üretilen component kodu, artı `.ux/last-component.json`.
- **Bağlanır:** `/ux-lint` → doğrula. `/ux-polish` → sıkıştır.

#### `/ux-system` — eksiksiz başlangıç design sistemi üretir

- **Ne yapar:** Sahip olmayan bir proje için eksiksiz bir başlangıç design sistemi önerir — token'lar (renk, tip, boşluk, motion, yarıçap, gölge), foundation belgeleri, component kontratları, dark-mode eşleşmeleri, theme switcher. `design-system-architect`'i görevlendirir.
- **Ne zaman kullan:** «Bir design sistemimiz yok», «bize bir sistem kur», «token öner», «temamız ne olmalı», «DS'mizi kur».
- **Ne zaman atla:** Projenin zaten bir design sistemi var — mevcut sisteme karşı `/ux-component` kullan. Backend veya altyapı.
- **Çağırma:** `/ux-system` (henüz kayıtta yoksa önce discovery çalıştırır).
- **Çıktı:** `tokens.json`, `foundations.md`, `components/*.md` kontratları, opsiyonel Tailwind / vanilla / SCSS emit. Zincir bağlamı için `.ux/last-system.json` yazar.
- **Bağlanır:** `/ux-component` → yeni sisteme karşı inşa et. `/ux-design` → yeni token'ları kullanarak bir yüzey üret.

#### `/ux-dashboard` — uzmanlaşmış dashboard üretimi

- **Ne yapar:** Veri yoğunluğu disiplini olan dashboard — bento layout, tablo monospace rakamlar, sparkline pattern'leri, anti-card-overuse, semantik durum renkleri, az motion. Üzerine grafikler yapıştırılmış bir marketing sitesi değil.
- **Ne zaman kullan:** «Bir dashboard kur», «admin panelini tasarla», «bir metrik sayfası yap», «operatör konsolu», «analitik görünüm», «KPI panosu», «monitoring ekranı».
- **Ne zaman atla:** İstatistikli marketing landing'i (`/ux-design` kullan). Sadece bir widget (`/ux-component` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-dashboard`.
- **Çıktı:** Üretilen dashboard kodu + `.ux/last-dashboard.json`.
- **Bağlanır:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — motion işlemi

- **Ne yapar:** Bir yüzeyin motion katmanını üretir — süreler, easing'ler, koreografi, reduced-motion fallback'leri, performans disiplini. Ayrıca mevcut motion'ı 5 boyuta karşı denetler (timing, easing, anlam, reduced-motion, performans).
- **Ne zaman kullan:** «Motion kontrolü», «animasyonlar iyi mi», «motion'ı düzelt», «animasyonları incele», «motion audit'i», «motion'da performans geçişi».
- **Ne zaman atla:** Yüzeyde motion yok (`/ux-audit` veya `/ux-polish` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-motion path/to/component.tsx` (audit modu) veya `/ux-motion --generate hero-entry` (üretim).
- **Çıktı:** Güncellenmiş kod (üretim modunda) veya `.ux/last-motion.json` raporu (audit modunda).
- **Bağlanır:** `/ux-fix` → motion bulgularını uygula. `/ux-polish` → sıkıştır.

### Audit & doğrulama

#### `/ux-lint` — deterministik regex tabanlı linter (LLM yok, CI-safe)

- **Ne yapar:** Kodun üzerinde 145 regex kuralı çalıştırır. LLM çağrısı yok. CI'da Critical / High'ta non-zero ile çıkar. Kaynak: `data/anti-patterns.json`. Kurallar A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) kapsar.
- **Ne zaman kullan:** Pre-commit hook. CI gate. `/ux-audit` maliyetini ödemeden önce büyük bir codebase'de hızlı ilk geçiş. Üretimi doğrulamak için `/ux-design` veya `/ux-component` sonrası.
- **Ne zaman atla:** Bir fix loop istiyorsun (linter raporlar, düzenlemez — `/ux-polish --fix` veya `/ux-fix`'e bağla). Taste yargısı istiyorsun (`/ux-critique` kullan).
- **Çağırma (slash):** `/ux-lint src/`.
- **Çağırma (CLI):** `uxskill lint .` veya `python3 bin/ux-lint.py .` veya `bash bin/ux-lint.sh --ci --fail-on high`.
- **Çağırma (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Çıktı:** stdout'a bulgular (konum, kural id'si, severity, kanıt). Temizse exit kodu 0, `--fail-on high` set olduğunda Critical/High'ta non-zero.
- **Bağlanır:** `/ux-polish --fix` → aynı pattern'ler üzerinde LLM-driven karşılık. `/ux-fix` → bulguları severity'ye göre sıralanmış commit olarak uygula. `/ux-audit` → tam 6-lensli akıl yürütme geçişi. `/ux-next` → conductor'a karar verdir.

#### `/ux-audit` — 6 lensli design audit'i

- **Ne yapar:** Altı lense karşı yapılandırılmış, görüş sahibi bir inceleme (netlik, hiyerarşi, erişilebilirlik, ses, motion, taste), severity-etiketli bulgular üretir. Polaris tarzı rapor. Önce `.ux/last-frame.json`'ı okur — hedef kitle ve outcome her bulgunun severity'sini sabitler.
- **Ne zaman kullan:** Yüzey var ve savunulabilir bir eleştiri istiyorsun. «Audit», «UX'i incele», «iyi mi bu», «ne bozuk», «bunu parçala».
- **Ne zaman atla:** Yüzey henüz yok (`/ux-design` kullan). Kullanıcı bir lens istiyor (hedeflenmiş komutu kullan: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Kullanıcı taste görüşü istiyor (`/ux-critique` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-audit https://example.com/pricing` veya `/ux-audit src/components/Pricing.tsx`.
- **Çıktı:** `.ux/last-audit.json` yazar — `{lens, severity, title, principle, evidence, fix}`'ten `findings` dizisi, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Bağlanır:** `/ux-fix` → bulguları uygula. `/ux-polish` → kozmetik geçiş. `/ux-design` → yapısal redesign gerekirse.

#### `/ux-a11y` — WCAG 2.1 AA audit'i + ortak nezaket kontrolleri

- **Ne yapar:** Yapılandırılmış bir WCAG 2.1 AA audit'i, artı otomatik araçları geçen ama gerçek kullanıcıları hâlâ inciten ortak nezaket kontrolleri (focus görünürlüğü, hata özgüllüğü, motion tercihleri, klavye tuzakları, renge bağımlılık).
- **Ne zaman kullan:** Pre-ship erişilebilirlik gate'i. Bir redesign'dan sonra. «Erişilebilirlik kontrolü», «WCAG audit'i», «bu erişilebilir mi», «a11y incelemesi», «screen reader testi», «klavye nav kontrolü».
- **Ne zaman atla:** Kullanıcıya dönük değil. Backend veya altyapı. Work-in-progress eskizler.
- **Çağırma:** `/ux-a11y https://example.com` (live URL tercih edilir — otomatik araçlar ve klavye testi sadece live'da çalışır).
- **Çıktı:** `.ux/last-a11y.json` yazar — `{wcag_sc, sc_name, severity, title, evidence, fix, category}`'ten `findings` dizisi, `beyond_wcag` dizisi, `severity_counts`.
- **Bağlanır:** `/ux-fix` → bulguları commit olarak uygula. `/ux-copy` → bir copy geçişinin parçası olarak alt text ve form-hata kablolamasını düzelt.

#### `/ux-critique` — taste çağrısı (3 kazanım, 3 ıskalama, 1 stratejik hamle)

- **Ne yapar:** Bir designer'ın görüşü — yapılandırılmış audit değil, severity puanı değil, sadece neyin işe yaradığını, neyin yaramadığını ve en çok şeyi değiştirecek o tek stratejik hamleyi adlandıran sıkı, görüş sahibi bir take.
- **Ne zaman kullan:** «Ne düşünüyorsun», «iyi mi bu», «bunu eleştir», «dürüst görüş», «vibe doğru mu», «biz gibi hissettiriyor mu», «bunu ship etmeli miyiz».
- **Ne zaman atla:** Kullanıcı açıkça yapılandırılmış bir audit istiyor (`/ux-audit` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-critique https://example.com`.
- **Çıktı:** `.ux/last-critique.json` yazar — 3 kazanım, 3 ıskalama, 1 stratejik hamle, artı düzyazı.
- **Bağlanır:** Take redesign önerirse `/ux-design`. Take sıkıştırma önerirse `/ux-polish`.

#### `/ux-copy` — microcopy incelemesi + yeniden yazım

- **Ne yapar:** Her görünür string'i ses rubriğine karşı değerlendirir ve bir before/after yeniden yazımı üretir. Yakalar: «form contains errors» (genel), «John Doe» (placeholder), AI-neşeli kutlayıcı copy, genel CTA'lar, ölü empty state'ler, yararsız hatalar.
- **Ne zaman kullan:** Yapı doğru ama kelimeler zayıf. «Copy'yi incele», «microcopy'yi düzelt», «hata mesajları kötü», «bunu yeniden yaz», «string'leri sıkıştır», «butonlar genel duyuyor», «bu empty state ölü».
- **Ne zaman atla:** Layout sorunları (`/ux-audit` veya `/ux-polish` kullan). Alt text gibi erişilebilirlikten kaynaklanan copy sorunları (`/ux-a11y` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-copy src/views/checkout.blade.php`.
- **Çıktı:** `.ux/last-copy.json` yazar — `{location, severity, before, after, notes}`'tan `strings` dizisi, artı rubrik + çeviri gerektiren locale'ler.
- **Bağlanır:** `/ux-fix` → yeniden yazımları uygula. `/ux-a11y` → copy düzeltmelerinden sonra tekrar kontrol et.

### Fix & polish

#### `/ux-fix` — bulguları atomik commit olarak uygula

- **Ne yapar:** `.ux/`'den son raporu okur (audit, copy, a11y, motion veya polish), working tree'yi doğrular ve bulguları doğru sub-agent'lar aracılığıyla atomik commit olarak uygular. Kaynak komutu yeniden çalıştırarak yeniden doğrular.
- **Ne zaman kullan:** Bir audit-sınıfı komutu çalıştırdıktan ve bulguları inceledikten sonra. «Bulguları düzelt», «düzeltmeleri uygula», «fix loop'u çalıştır», «yüzeyi yamala», «değişiklikleri yap», «düzelt onu».
- **Ne zaman atla:** `.ux/`'de önceki rapor yok. Working tree kirli ve kullanıcı stash/commit'e razı olmadı. Düzeltmeler mekanik uygulama değil, design yargısı gerektiriyor (redesign için `/ux-design` kullan).
- **Çağırma:** `/ux-fix` (hangi raporun düzelteceğini otomatik algılar) veya `/ux-fix --from=last-a11y.json`.
- **Çıktı:** Bulgu başına atomik commit'ler. Kaynak komutu yeniden çalıştırır ve `.ux/last-*.json` dosyasını günceller. Bir özet yazdırır.
- **Bağlanır:** `/ux-next` → conductor sonraki hamleyi seçer.

#### `/ux-polish` — kozmetik geçiş + AI-slop'u öldür

- **Ne yapar:** Boşluk ritmi, hiyerarşi keskinleştirme, AI-slop tespiti, token tutarlılığı. `/ux-lint`'in LLM-driven karşılığı — taste çağrılarında senin yargını kullanır.
- **Ne zaman kullan:** Yapı doğru ama uygulama gevşek. «Cilala», «bunu sıkıştır», «AI-slop'u kaldır», «premium yap», «daha az AI görünümlü yap», «boşluk yanlış geliyor», «bu genel görünüyor», «daha fazla taste gerek».
- **Ne zaman atla:** Yüzeyde temel işlevsellik eksik (önce onu düzelt). Polish değil, redesign gerekiyor (`/ux-design` kullan). Copy sorunları (`/ux-copy` kullan). Motion sorunları (`/ux-motion` kullan). A11y sorunları (`/ux-a11y` kullan).
- **Çağırma:** `/ux-polish src/components/Hero.tsx`.
- **Çıktı:** Güncellenmiş kod + değişiklikleri açıklayan `.ux/last-polish.json`.
- **Bağlanır:** `/ux-lint` → polish'in tuttuğunu doğrula. `/ux-a11y` → erişilebilirliği tekrar kontrol et.

### Discovery & anlatı

#### `/ux-frame` — 4 alanlı framing bloğu

- **Ne yapar:** Kim için olduğu, outcome, hipotez ve başarı sinyalini yapılandırılmış bir framing bloğunda yakalar. Design işi yok — sadece belirsiz bir isteği çalışan bir brief'e dönüştüren dört alanlı intake. `/ux-discover`'dan daha hafif (4 alan vs 10).
- **Ne zaman kullan:** Herhangi bir proje, sprint veya tek-seferlik engagement'ın başlangıcı. Bir konuşma yoldan çıktığında orta akışta. «Bunu çerçevele», «brief ne», «projeyi kur», «framing».
- **Ne zaman atla:** Zaten çerçevelendi (`.ux/last-frame.json`'a bak). Framing implikasyonu olmayan one-off component build'i. Backend veya altyapı.
- **Çağırma:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Çıktı:** `.ux/last-frame.json` yazar — `{audience, outcome, hypothesis, success_signal}`.
- **Bağlanır:** `/ux-discover` → frame'i 10 alanlı brief'e genişlet. `/ux-design` → frame'i çapa olarak kullanarak üret.

#### `/ux-research` — araştırma planlama + sentez

- **Ne yapar:** Planlama modu: görüşme script'leri, anketler, recruitment screener'ları yazar. Sentez modu (`--synthesize`): görüşmeleri, analytics'i, rakip sitelerini, A/B sonuçlarını, support ticket'larını önerilere sindirir. `research-synthesizer`'ı görevlendirir.
- **Ne zaman kullan:** «Bir araştırma çalışması planla», «görüşme soruları lazım», «bir anket tasarla», «kullanıcı nasıl recruit ederim», «kullanıcı test planı», «diary study», «preference test», «fake door», «smoke test», «görüşme notlarımı sentezle».
- **Ne zaman atla:** Cevap yüksek güvenle zaten biliniyor. Düşük riskli geri alınabilir kararlar. Backend veya altyapı.
- **Çağırma:** `/ux-research --plan "loyalty wallet adoption in MENA"` veya `/ux-research --synthesize interviews/*.md`.
- **Çıktı:** `.ux/last-research.json` yazar — araştırma planı veya sentezlenmiş temalar + kanıt + öneriler.
- **Bağlanır:** `/ux-frame` → bulguları bir frame'e entegre et. `/ux-design` → bulgulardan üret. `/ux-workshop` → araştırmayı girdi olarak kullanarak bir workshop yürüt.

#### `/ux-workshop` — 5 fazlı design thinking workshop'u

- **Ne yapar:** Bir discovery / design-thinking workshop'unu uçtan uca kolaylaştırır. Beş ardışık faz (keşif → heat map → stakeholder haritası → çözüm eskizi → game plan). Zaman kutulu. Faz başına somut artefaktlar. «İlginç bulgularla» değil, bir kararla biter.
- **Ne zaman kullan:** Gerçek soru, gerçek katılımcılar, gerçek zaman bütçesi. «Bir workshop yürüt», «bir discovery kolaylaştır», «design thinking oturumu yapalım», «bir saatliğine stakeholder'larım var, ne yapıyoruz», «projeyi başlat».
- **Ne zaman atla:** Brief zaten net ve scope'lu. Solo brainstorm (`/ux-design` veya `/ux-frame` kullan). Takım discovery'de değil, yürütme ortasında.
- **Çağırma:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Çıktı:** `.ux/last-workshop.json` yazar — game plan + faz başına artefaktlar.
- **Bağlanır:** `/ux-design` → game plan'i yürüt. `/ux-research` → workshop'un yüzeye çıkardığı boşlukları doldur. `/ux-case-study` → yolculuğu yayımla.

#### `/ux-case-study` — yayınlanabilir case study (Wfrah-editorial formatı)

- **Ne yapar:** Saf monokrom editorial formatında bir proje case study'si üretir — Wfrah tipografi, hairline ayırıcılar, numaralandırılmış (A)–(G) bölüm kodları, çift-dil-güvenli layout. Bir doküman, marketing broşürü değil. `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`'dan okur.
- **Ne zaman kullan:** Lansman sonrası. Ayrık bir milestone'dan sonra. «Bir case study yaz», «bu projeyi case study yap», «wrap-up belgesini yap», «bu işi yayımla», «portfolio parçası».
- **Ne zaman atla:** Projede (A)–(G) bölümlerini doldurmak için veri eksik. Kullanıcı marketing landing'i istiyor, case study değil (`/ux-design` kullan).
- **Çağırma:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Çıktı:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Bağlanır:** Terminal komutu — genellikle bir projenin sonu.

### Conductor

#### `/ux-next` — workflow yöneticisi (read-only)

- **Ne yapar:** Her `.ux/last-*.json`'ı okur ve en yüksek kaldıraçlı sonraki komutu adlandırır. Bir yönetici, inşaatçı değil. Read-only.
- **Ne zaman kullan:** Komutlar arasında. «Sırada ne yapmalıyım», «sıradaki hamle ne», «benim için karar ver», «buradan nereye gidiyoruz».
- **Ne zaman atla:** `.ux/`'de önceki rapor yok. Aklında spesifik bir sonraki komut var.
- **Çağırma:** `/ux-next` (argüman yok) veya `/ux-next --focus=a11y`.
- **Çıktı:** Stdout — önerilen sonraki komut + rationale.
- **Bağlanır:** Hangi komutu seçerse.

#### `/ux-expert` — danışmanlık bağlantısı

- **Ne yapar:** Bir kullanıcı gerçek hayatta bir UX uzmanı istediğinde plugin yaratıcısının iletişim bilgisini yüzeye çıkarır. Kısa, doğrudan, marketing yok.
- **Ne zaman kullan:** «Bunu kim yaptı», «bir UX uzmanına ihtiyacım var», «danışmanlık yapar mısın», «bunun için birini tutabilir miyim», «bu plugin'in arkasında bir insan var mı».
- **Ne zaman atla:** Kullanıcı danışmanlık değil plugin özelliklerini soruyor.
- **Çağırma:** `/ux-expert`.
- **Çıktı:** LinkedIn / email / repo ile kısa iletişim kartı.

### Komut zincir grafı

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  4 alanlı framing bloğu
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  10 alanlı intake (FORCING GATE)
                  └────────────┬─────────┘
                               │ .ux/last-discovery.json yazar
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 paralel arama -> birleştirilmiş sistem
                  └────────────┬─────────┘
                               │ .ux/last-recommendation.json yazar
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ .ux/last-<surface>.json yazar
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ .ux/last-<lens>.json yazar
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  bulguları commit olarak uygula
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  yayınlanabilir artefakt
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — read-only
                  │  /ux-expert          │  danışmanlık bağlantısı
                  └──────────────────────┘
```

---

## 5 sub-agent

Sub-agent'lar komutlar tarafından görevlendirilen rol-spesifik üreticilerdir. Asla bağımsız çalışmazlar — `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research` vs. tarafından çağrılırlar. Her agent'ın tanımlı bir sahiplik sınırı vardır: brief'e karar VERMEZLER; ona karşı yürütürler.

### `frontend-engineer`

- **Sahibi:** Anti-AI-slop disiplini ile production-grade frontend kodu (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro).
- **Görevlendiren:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Girdiler:** Brief + yaratıcı yönlendirme + token'lar (`.ux/last-recommendation.json`'dan).
- **Çıktılar:** Genel AI çıktısından ayırt edilebilir çalışan kod. Mor gradyan yok, ortalanmış hero yok, üç eşit card yok, display boyutunda Inter yok, «John Doe» yok, emoji yok, 300ms varsayılan yok.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Sahibi:** Production frontend kodunda motion — Framer Motion, GSAP, CSS animasyonları. Süreler, easing'ler, koreografi, reduced-motion fallback'leri, performans disiplini.
- **Görevlendiren:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Girdiler:** Motion brief'i + token'lar + `data/motion-presets.json`'dan 57 motion preset'i.
- **Çıktılar:** Yerini kazanan motion. Her zaman `prefers-reduced-motion` fallback'leriyle sarılır. Her zaman Core Web Vitals'a karşı test edilir.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Sahibi:** Ship'lenen string'ler — hata mesajları, empty state'ler, CTA'lar, loading state'leri, başarı mesajları, toast'lar, helper text, form etiketleri, button text'i.
- **Görevlendiren:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Girdiler:** Ses profili (isimli veya yapıştırılmış) + yüzeyin string'leri.
- **Çıktılar:** Ürünün on değil, tek bir ürün gibi ses çıkarması için bir yüzeyin her durumunda tutarlı şekilde uygulanan production microcopy. Yasaklar: «form contains errors», «John Doe», AI-neşeli kutlayıcı copy, genel CTA'lar, ölü empty state'ler.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Sahibi:** Araştırma girdilerini (görüşmeler, analytics, rekabetçi siteler, A/B sonuçları, support ticket'ları) eyleme geçirilebilir design önerilerine sindirme.
- **Görevlendiren:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Girdiler:** Ham araştırma — transkriptler, export'lar, rakip URL'ler, support cluster'ları.
- **Çıktılar:** Temalar, kanıtlar, öneriler. Cevabı asla tasarlamaz — designer'a tasarımdan başlayacağı substratı verir.
- **Araçlar:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Sahibi:** Eksiksiz design sistemleri — token'lar (renk, tip, boşluk, motion, yarıçap, gölge), foundation belgeleri, component kontratları, dark-mode eşleşmeleri, theming katmanı.
- **Görevlendiren:** `/ux-system`, sistem yoksa `/ux-component`.
- **Girdiler:** Brand brief'i + `.ux/last-recommendation.json` (stil + palet + tipografik çift + motion preset'leri).
- **Çıktılar:** Aşağı agent'ların temelleri yeniden karara bağlamadan inşa edebileceği tutarlı, görüş sahibi, production-ready bir sistem. Token JSON, foundation MD, component kontratları, dark-mode mapping.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### Sub-agent görevlendirme protokolü

Bir komut bir sub-agent'ı görevlendirdiğinde, şunları geçirir:

1. Brief / öneri (`.ux/`'den yüklenir).
2. İlgili manifest dilimi (örn. `frontend-engineer` seçilen stil + palet + component'leri alır; `motion-engineer` seçilen motion preset'lerini alır).
3. 145 anti-pattern guardrail'ı (her zaman aktif).
4. Bir başarı kriteri (artefaktın ne yapması gerektiği).

Sub-agent'lar şunu döndürür:

1. Artefakt (kod, doküman, sistem).
2. Bir rationale bloğu (neden bu seçimler).
3. Guardrail'lara karşı bir self-check (hangi kuralları doğruladılar).

Çağıran komut sonra tamamlandığını ilan etmeden önce `/ux-lint`'i otomatik çalıştırır.

---

## 11 data manifest'i

Data katmanı beyindir. Her komut ondan okur; motor onun üzerinden merge eder; linter ona karşı tarar. Tüm dosyalar `data/` altında yaşar ve schema sürümlemesi için girişlerini `{_meta, entries}`'e sarar.

### `styles.json` — 84 design stili

| Alan | Açıklama |
|---|---|
| `entries` | 84 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `kategoriler` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, vs. |
| `örnek giriş` | `swiss-international` — «Grid yasa. Tipografi ağır işi yapar. Dekorasyon başarısızlıktır.» |

Kullanan: `/ux-recommend`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 renk paleti

| Alan | Açıklama |
|---|---|
| `entries` | 176 |
| `giriş başına anahtarlar` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tonlar` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, vs. |
| `örnek giriş` | `claude-warm-editorial` — light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Kullanan: `/ux-recommend`, `/ux-system`. Kontrast AA / AAA'da doğrulanmış. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 tipografik eşleşme

| Alan | Açıklama |
|---|---|
| `entries` | 70 |
| `giriş başına anahtarlar` | `id`, `name`, `display` (aile + ağırlıklar + kaynak + lisans + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `örnek giriş` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Tüm ailelerin lisansı + kaynak URL'si var. `/ux-recommend`, `/ux-system` tarafından kullanılır.

### `components.json` — 148 component

| Alan | Açıklama |
|---|---|
| `entries` | 148 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `kategoriler` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `örnek giriş` | `mega-nav-product-grid` — Mega Navigation, Product Grid — 6 parçalı anatomi, 4 durum |

Bu en büyük hendeğimiz. Başka hiçbir Claude UX plugin'i yapılandırılmış component manifest'i dağıtmıyor.

### `industries.json` — 184 sektör kuralı

| Alan | Açıklama |
|---|---|
| `entries` | 184 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `kategoriler` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, vs. |
| `örnek giriş` | `fintech-neobank` — yüksek güven, regülasyon disclosure'ları, bakiye/işlem birincil UI, mobile-first günlük kullanım |

`/ux-recommend` tarafından ilk paralel arama ekseni olarak kullanılır.

### `chart-types.json` — 35 chart tipi

| Alan | Açıklama |
|---|---|
| `entries` | 35 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `kategoriler` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `örnek giriş` | `bar-vertical` — 4–15 ayrık kategoriyi karşılaştır. x-ekseni boyunca konum kategoriyi, yükseklik değeri map'ler. |

`/ux-dashboard`, `/ux-component` (chart instance'ları) tarafından kullanılır.

### `tech-stacks.json` — 25 stack

| Alan | Açıklama |
|---|---|
| `entries` | 25 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tier'lar` | production, prerelease, experimental |
| `örnek giriş` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css ile uyumlu |

Diğer stack'ler arasında Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025 var.

### `ux-guidelines.json` — 112 isimli UX yasası

| Alan | Açıklama |
|---|---|
| `entries` | 112 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `kategoriler` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, vs. |
| `örnek giriş` | `hicks-law` — Karar süresi sunulan seçim sayısıyla logaritmik olarak büyür |

`/ux-audit` (6 lensli puanlama) ve `/ux-critique` (taste çapası) tarafından kullanılır.

### `motion-presets.json` — 57 motion preset'i

| Alan | Açıklama |
|---|---|
| `entries` | 57 |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion fallback), `when_to_use` |
| `kategoriler` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `örnek giriş` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Her preset'in bir reduced-motion varyantı var. Framer Motion, GSAP ve saf CSS için stack-ready kod.

### `anti-patterns.json` — 145 regex kuralı

| Alan | Açıklama |
|---|---|
| `entries` | 145 |
| `giriş başına anahtarlar` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `kategoriler` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

Tam kural listesi [145 anti-AI-slop kuralı](#145-anti-ai-slop-kuralı--linter)'nda.

### `brands/*.json` — 160 brand specs'i

| Alan | Açıklama |
|---|---|
| `entries` | 160 (artı tümünü listeleyen `_index.json`) |
| `giriş başına anahtarlar` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `kategoriler` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Tam liste [160 brand DESIGN.md spec'i](#160-brand-designmd-speci--kategoriye-göre)'nde.

---

## 145 anti-AI-slop kuralı — linter

ux-skill deterministik regex tabanlı bir linter dağıtır. **LLM yok.** **API yok.** **Ağ yok.** Tipik bir Next.js app'inde CI'da ~200ms'de çalışır. `--fail-on high` set olduğunda Critical / High bulgularda non-zero ile çıkar.

Kurallar `data/anti-patterns.json`'dan (v2 tercih edilir) `references/foundations/anti-patterns.md` fallback'iyle (v1 bash) kaynaklanır. İki binary dağıtılır: `bin/ux-lint.py` (Python, hızlı, genişletilebilir) ve `bin/ux-lint.sh` (Bash + perl-PCRE, Python'suz ortamlar için).

### Kategoriye göre kurallar

#### Typography (3 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| high | `inter-as-display` | Inter display font olarak kullanılmış |
| medium | `hero-text-arbitrary-90px` | Keyfi hero font boyutu |
| low | `font-system-only` | Seçilmiş typeface olmadan sistem font stack'i |

#### Color (6 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| high | `purple-to-blue-gradient` | Varsayılan mor-mavi AI gradyanı |
| high | `dark-text-on-dark-card` | Card üzerinde düşük kontrastlı metin |
| medium | `gradient-text-rainbow` | Çok-stop gradient text |
| medium | `card-glow-purple-shadow` | Card'larda mor glow gölgesi |
| medium | `gradient-mesh-purple-pink` | Mor-pembe mesh gradient hero |
| low | `tailwind-color-named-vague` | Semantik token olmadan isimli Tailwind renkleri |

#### Layout (5 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| high | `three-equal-card-grid` | Bir sırada üç eşit card |
| medium | `centered-everything-hero` | Ortalanmış hero kompozisyonu |
| medium | `avatar-stack-overlapping` | Genel üst üste binmiş avatar stack |
| low | `pill-rounded-full-everywhere` | Her şeye uygulanmış `rounded-full` |
| low | `nav-equal-hamburger-desktop` | Desktop'ta hamburger menü |

#### Content (5 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| high | `lorem-ipsum-leak` | Ship edilen kodda Lorem ipsum |
| high | `emoji-in-ui` | UI elementi olarak emoji kullanımı |
| high | `icon-emoji-stamp` | İkon damgası olarak emoji kullanımı |
| high | `testimonial-fake-five-stars` | Hardcoded beş yıldızlı testimonial |
| medium | `fake-name-john-doe` | Genel placeholder isimler |

#### Motion (3 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | CTA'da zıplayan ok |
| low | `timing-300ms-default` | Varsayılan 300ms geçiş timing'i |
| low | `cubic-bezier-material-only` | Her yerde Material varsayılan easing |

#### A11y (6 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| high | `inline-svg-no-aria` | aria-label veya aria-hidden olmayan SVG |
| high | `img-no-alt` | alt attribute'u eksik image |
| high | `link-onclick-no-href` | onClick'li ama href'siz anchor |
| medium | `button-no-type` | type attribute'u eksik button |
| medium | `heading-skip-h1-h3` | Atlanmış heading seviyesi |
| medium | `infinite-scroll-no-pagination` | Klavye fallback'siz sonsuz scroll |

#### Quality (6 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| high | `console-log-leak` | Component kodunda `console.log` |
| medium | `inline-style-attribute` | Inline style attribute |
| medium | `any-type-leak` | TypeScript `any` tipi |
| medium | `arbitrary-z-index-9999` | Tembel z-index değeri |
| low | `shadcn-default-everywhere` | Değiştirilmemiş varsayılan shadcn token bloğu |
| low | `todo-fixme-comment` | Ship edilen kodda TODO veya FIXME |

#### Visual (1 kural)

| Severity | Kural ID'si | İsim |
|---|---|---|
| low | `blur-bg-only-decoration` | Glass yüzeyi olmadan backdrop blur |

### Linter kullanımı

**Tek seferlik tarama:**

```bash
uxskill lint .
# veya
python3 bin/ux-lint.py src/
# veya
bash bin/ux-lint.sh src/
```

**CI gate (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**Pre-commit hook:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**Çıktı (örnek):**

```
─── /ux-lint raporu ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  kanıt: bg-gradient-to-br from-purple-500 to-blue-500
  fix: önerilen paletin primary gradient'i ile değiştir veya gradient'i kaldır

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  kanıt: grid grid-cols-3 gap-6 (3 eşit Card çocuğu)
  fix: bir card'ı öne çıkar; iki azaltılmış vurgulu card ile yanına yerleştir

3 dosya tarandı · 2 high · 0 medium · 0 low · exit 1
Önerilen sıradaki: /ux-polish --fix (LLM-driven, hem lint-edilebilir hem estetik bulguları ele alır)
```

---

## 160 brand DESIGN.md spec'i — kategoriye göre

Gerçek brand'ler. Gerçek design dilleri. Gerçek DESIGN.md spec'leri — genel paletler değil. Plugin'e «Stripe'ın stilinde bir landing kur» de, ve gerçek brand sözlüğünü okur: ses rubriği, renk token'ları, motion konvansiyonları, imza hamleleri, anti-hamleleri.

Her brand yapılandırılmış JSON (`data/brands/<slug>.json`) artı bir düzyazı referansı (`references/brands/<slug>.md`) olarak dağıtılır.

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

### Bu neden önemli

Diğer 8 popüler Claude UX plugin'i «modern minimal» veya «clean dashboard» üretir — aynı varsayılan estetiğin varyantları. ux-skill **Linear'ın netliği**, **Stripe'ın ciddiyeti**, **Apple'ın ölçülülüğü**, **Tesla'nın monoliti**, **Notion'un samimiyeti**, **Cursor'ın gradient disiplini**, **Raycast'in hairline yoğunluğu**, **Claude'un sıcak editorial'ı** istemene izin verir — ve motor doğru token'ları, sesi, motion konvansiyonlarını ve imza hamlelerini brand spec'inden çeker.

---

## MCP sunucusu — asimetrik hamle

ux-skill bir **Model Context Protocol sunucusu** dağıtır. `ux-mcp`'yi çalıştır ve motor herhangi bir MCP-yetenekli host'un — Claude Desktop, Cursor, Windsurf, generic agent'lar — çağırabileceği long-running bir stdio process'i olur. On dört araç: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Slash komutlarının kullandığı aynı Python handler'ları; aynı data manifest'leri; aynı deterministik recommender.

**Bu neden asimetrik hamle:** top sekiz Claude UX skill'inin hiçbiri (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) MCP sunucusu dağıtmaz. Claude Code'un plugin runtime'ı içinde kilitliler. ux-skill, Claude Code plugin'ini hiç duymamış agent'lar dahil MCP konuşan herhangi bir host'tan ulaşılabilir.

```bash
pip install 'uxskill[mcp]'             # mcp opt-in bir extra'dır
ux-mcp                                  # stdio JSON-RPC sunucusu başlar
```

Client'ını `ux-mcp` binary'sine yönelt. Claude Desktop, Cursor ve Windsurf için tam araç dokümanları, JSON örnekleri ve client başına config [docs/mcp.html](docs/mcp.html)'de ve `commands/ux-mcp.md`'de yaşar.

---

## 17 IDE yükleyicisi

`uxskill init` (veya Claude Code içinde `/ux-init`) hangi IDE'yi kullandığını otomatik algılar ve doğru artefaktı yazar. Aynı Python motor. Aynı öneriler. IDE başına farklı yapıştırıcı.

| IDE / Araç | Tespit sinyali | Kurulan artefakt |
|---|---|---|
| Claude Code | `.claude/` veya `CLAUDE.md` | `.claude-plugin/plugin.json`'da plugin manifest'i + 22 komutun hepsi + 5 sub-agent'ın hepsi |
| Cursor | `.cursor/` veya `.cursorrules` | Motoru işaret eden `.cursorrules` prompt header'ı |
| Windsurf | `.windsurf/` veya `.windsurfrules` | Aynı prompt header'lı `.windsurfrules` |
| GitHub Copilot | `.github/copilot-instructions.md` veya `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` patch'i |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` veya `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

Her IDE'de, aynı `uxskill recommend` / `uxskill lint` / `uxskill stats` CLI komutları terminalden çalışır. Python motor doğruluğun kaynağıdır; IDE artefaktları motora yönlendiren ince prompt-header'lardır.

---

## Kullanım senaryoları — somut senaryolar

Sekiz gerçek senaryo. Durumuna en yakın olanı seç ve çağırmayı uyarla.

### 1. Cursor'da bir fintech dashboard'u inşa etme

Cursor'da bir MENA neobank dashboard'u üzerinde çalışıyorsun. Plugin'i kurarsın ve discovery, öneri, ardından dashboard üretimi çalıştırırsın.

```bash
pip install uxskill
uxskill init                                # Cursor'ı algılar, .cursorrules yazar
uxskill discover                            # 10 alanlı intake
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Sonra Cursor'da sor: *«.ux/last-recommendation.json'daki öneriyi kullanarak dashboard yüzeyini üret»*. Cursor `.cursorrules` header'ını okur, öneriyi yükler, açık kısıtlamalarla bir dashboard üretimini görevlendirir.

### 2. Claude Code'da Stripe stili bir landing üretme

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Proje tipi? landing
> Sektör? fintech-payments
> Ton? serious, technical, confident
> Must have? dark-mode, AA, mobile-first
> Forbidden? purple-gradients, three-equal-cards
> Referans brand'ler? stripe
> Stack? nextjs-15-app-router
> Bölge? global
> Başarı metriği? signup conversion

/ux-recommend
> [seçilen stili, paleti, tipografik çifti, motion preset'lerini, component'leri, brand örneklerini döndürür]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer sayfayı üretir]

/ux-lint .
> [geçer — Stripe brand spec'ine uyuldu]
```

### 3. CI'da AI slop için mevcut kodu denetleme

İki hafta önce bir Next.js app'i ship ettin. Her PR'da AI parmak izlerine karşı sert bir taban istiyorsun.

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

Mor-mavi gradient'ler, 96px'te Inter, «John Doe» testimonial'ları veya emoji-ikonlar getiren PR'lar CI'da fail olur. LLM maliyeti yok. ~200ms.

### 4. «AI üretilmiş hissettiren» mevcut bir yüzeyi parlatma

Diğer her AI-üretilmiş SaaS sitesi gibi görünen bir React app'i miras aldın. Öyle görünmemesini istiyorsun.

```
/ux-critique src/components/Hero.tsx
> [3 kazanım, 3 ıskalama, 1 stratejik hamle — take dürüst]

/ux-lint src/
> [15 high-severity AI parmak izi işaretlendi]

/ux-polish src/components/Hero.tsx
> [LLM-driven kozmetik geçiş + AI-slop öldürme]

/ux-fix
> [bulguları atomik commit olarak uygular, linter'ı yeniden çalıştırır]
```

Üç komut, bir parlatılmış yüzey, fix başına atomik commit'ler.

### 5. Linear stili bir command palette tasarlama

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [token'lar + imza hamleleri için data/brands/linear.app.json okur]
> [command-palette anatomisi + durumları için data/components.json okur]
> [açık Linear spec'iyle frontend-engineer'ı görevlendirir]
```

Üretilen component Linear'ın gerçek renk token'larını, tip stack'ini, motion konvansiyonlarını, hairline yoğunluklarını kullanır — «generic dark UI» değil.

### 6. Stakeholder'larla 90 dakikalık bir design thinking workshop'u yürütme

90 dakika için 5 kişilik bir odan var. Bir vibe ile değil, bir game plan ile çıkmalarını istiyorsun.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Plugin beş fazı (keşif → heat map → stakeholder haritası → çözüm eskizi → game plan) uçtan uca, zaman kutulu, faz başına somut artefaktlarla kolaylaştırır. Çıktı `.ux/last-workshop.json` — game plan, sadece «ilginç bulgular» değil.

### 7. Lansman sonrası yayınlanabilir bir case study yazma

Loyalty wallet'i ship ettin. Bir portfolio parçası istiyorsun.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [.ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json okur]
> [numaralandırılmış (A)-(G) bölümler, hairline ayırıcılar, çift-dil-güvenli layout ile Wfrah-editorial case study üretir]
> [case-studies/bashiti-loyalty.html yazar]
```

Case study tamamlanmış, yayınlanabilir bir artefakt — taslak değil. Saf monokrom, editorial tipografi, portfolio'na ship'lemeye hazır.

### 8. AI olmayan bağlamda discovery çalıştırma (sadece yapılandırılmış intake)

Bir projeyi scope'luyorsun. Henüz bir öneri lazım değil — yapılandırılmış bir brief lazım.

```bash
uxskill discover
# 10 alanlı intake, .ux/last-discovery.json'a kaydeder

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

JSON'u takımına verebilir, bir Notion belgesine yapıştırabilir veya ayrı bir AI aracına besleyebilirsin. ux-skill bir motor olmaya ek olarak yapılandırılmış bir intake aracı da.

### 9. MASTER.md persistence — design kararların, repo'da

`/ux-recommend`'dan sonra, seçilen stil + palet + tip + motion + component'ler + brand örnekleri + guardrail'ları takımın inceleyebileceği, diff alabileceği ve sürüm kontrolü yapabileceği insan-okunabilir bir Markdown dosyası olarak kalıcı yap.

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md` (YAML frontmatter + body) ve `persist save-page` aracılığıyla üretilen yüzey başına `.ux/design-system/pages/<name>.md` yazar. Idempotent — aynı girdi byte-identical çıktı üretir, böylece değişmemiş state üzerinde yeniden çalıştırma git'te no-op'tur.

---

## Alternatiflerle karşılaştırma

Kısa özet tablosu. Tam tablo bazlı karşılaştırma [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)'de.

| Boyut | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash komutları | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Component'ler | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion preset'leri | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand spec'leri | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Anti-pattern kuralları | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-safe deterministik linter | **evet** | hayır | hayır | hayır | hayır | hayır | hayır | hayır | hayır |
| Desteklenen IDE'ler | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery gate | **10 alan** | örtük | örtük | örtük | örtük | örtük | örtük | örtük | örtük |
| `.ux/` state zinciri | **evet** | hayır | hayır | hayır | hayır | hayır | hayır | hayır | hayır |
| Yıldızlar (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Dürüst değerlendirme

- **ui-ux-pro-max** farkındalıkta daha büyük, 18 IDE dağıtır, CSV'si üzerinde BM25 tarzı arama var. Component manifest'i, motion manifest'i, brand kütüphanesi veya deterministik linter dağıtmıyor.
- **open-design** 19 skill + preview var ama sadece Claude Code desteği ve anti-slop katmanı yok.
- **hallmark** ruhen en yakın (o da anti-slop) ama tek skill — motor yok, manifest yok, zincirli komut yok.
- **material-3-skill** spesifik olarak Material Design 3 istiyorsan mükemmel. MD3'te rekabet etmiyoruz.

Her boyut için tam detay için: [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Linter tamlığı (Q3 2026)

- **52 toplama ulaşmak için +17 ertelenen anti-pattern kuralı.** Hedefler: dark-on-dark hover state'leri, sadece-renk state encoding, gereksiz z-index escalation, JS'te hardcoded breakpoint'ler, disabled state yerine opacity, vs.
- **Mekanik olarak düzeltilebilir bulgular için güvenli yeniden yazımlar için `uxskill lint --fix`** (button-no-type, img-no-alt boş-string, console-log-leak kaldırma).
- **Lint bulgularını inline yüzeye çıkaran VS Code extension'ı** (CI çalıştırmaya gerek yok).

### v2.2 — Component manifest'i genişletmesi (Q4 2026)

- **198 toplama ulaşmak için +50 component.** Net-yeni: async filter'lı combobox, recent-items heuristic'li command-palette, conditional-form-step, payment-element varyantları, RTL-aware date picker, MENA-spesifik phone input, hijri overlay'li calendar grid.
- **6 stack'te per-component kod emit** (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, vanilla HTML/CSS).
- **Component playground'u** uxskill.laithjunaidy.com/playground'da — öneri motorunu dene + canlı component preview gör.

### v3 — Marketplace + lock-in (2027)

- **Brand spec marketplace** — topluluk brand spec'lerini yayımla ve keşfet. Moderasyonu finanse etmek için pay-to-publish.
- **Custom anti-pattern kuralları** — projeler kendi regex kurallarını `data/anti-patterns.local.json`'da tanımlayabilir (zaten v2'de var; v3 discovery + paylaşım ekler).
- **`uxskill plan`** — sadece bir yüzey değil, brief'ten tam multi-page site planlama.
- **Figma plugin pariteti** — aynı öneri motoru, Figma'da yüzeye çıkmış.

---

## Katkıda bulunma

Issue ve PR'lar memnuniyetle karşılanır. Üç yüksek-kaldıraçlı alan:

### Bir anti-pattern kuralı ekle

1. `data/anti-patterns.json`'ı düzenle — `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references` ile bir giriş ekle.
2. `tests/linter/`'da bir test ekle — kuralı tetikleyen bir dosya, tetiklemeyen bir tane.
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx` çalıştır — ateş ettiğini doğrula. `tests/linter/should-not-trigger/<rule>.tsx`'te çalıştır — etmediğini doğrula.
4. Bir PR aç.

### Bir brand spec ekle

1. `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references` ile `data/brands/<slug>.json` oluştur.
2. Karşılık gelen düzyazıyı `references/brands/<slug>.md`'ye ekle.
3. `data/brands/_index.json`'a kaydet.
4. Bir PR aç. Spec birincil-kaynak referanslarla desteklenmeli (brand'in gerçek ürünü, herkese açık design sistemi veya yayımlıyorlarsa DESIGN.md).

### Bir motion preset ekle

1. `data/motion-presets.json`'ı düzenle — `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use` ile bir giriş ekle.
2. Preset'in bir reduced-motion varyantı olmalı. İstisna yok.
3. Bir PR aç.

### Süreç

- Tam süreç için [CONTRIBUTING.md](CONTRIBUTING.md)'yi oku.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)'yi oku.
- Yeni kurallar ve brand spec'leri şunlar için incelenir: birincil-kaynak tabanlanma, tek bir projeye overfit yok, hiçbir veride emoji yok, uygulanabilir yerlerde RTL-safe davranış.

---

## Lisans, yazar, teşekkürler

### Lisans

MIT. Kullan, fork'la, üstüne inşa et. Eğer seni AI slop ship etmekten kurtarırsa, repo'ya yıldız ver — bunu desteklemenin en ucuz yolu.

### Yazar

**Laith Aljunaidy** — MENA-first bir loyalty platformu olan [Dot](https://thedotwallet.com)'un solo kurucusu. AI üretilmiş frontend'in hepsi aynı görünmesin diye ux-skill'i inşa ediyor.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Teşekkürler

- Claude Code ve bunu dağıtılabilir kılan skill / plugin mimarisi için Anthropic ekibine.
- `data/ux-guidelines.json`'ı bilgilendiren çalışmaları için Nielsen Norman Group, Laws of UX (lawsofux.com) ve UX araştırma topluluğuna.
- `data/brands/`'de listelenen her brand'e — herkese açık design sistemleri brand spec'lerinin doğruluk kaynağı.
- Orijinal v1 katkıda bulunanlarına: v2 Python motoruna tohum olan tek-atışlık Claude skill'i.
- Karşılaştırdığımız 8 popüler Claude UX plugin'i — çıtayı yükselttiler; bu bizim cevabımız.

---

**ux-skill** · **v3.0.0-stable** · Claude Code, Cursor, Windsurf ve diğer her AI coding aracının AI üretilmiş gibi okunmayan frontend çıktısı vermesi için inşa edildi.

> Repo'ya [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) adresinden yıldız ver · `pip install uxskill` veya `npx uxskill init` ile kur · Karşılaştırmaya [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) adresinden göz at
