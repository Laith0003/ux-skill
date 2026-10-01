[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · **Türkçe**

# ux-skill: Claude Code, Cursor ve diğer her AI coding aracı için design intelligence motoru

**AI tarafından üretilen arayüzü sıradan değil, ayırt edici kılan bir design intelligence motoru.** 17 AI coding aracından herhangi birine ekle, çıktın artık AI işi gibi görünmesin. Ücretsiz, MIT, çevrimdışı, LLM yok.

```bash
pip install uxskill
```

**[GitHub'da ux-skill'e yıldız ver](https://github.com/Laith0003/ux-skill)**, işine yarıyorsa projeye yardım etmenin en kolay yolu bu. Yeni misin? [60 saniyelik turla](#hızlı-kurulum) başla ya da canlı olarak [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) adresinde gör.

![Önce: sıradan stok fotoğraflı hero, yumuşak mor gradyan, marka kimliği yok. Sonra: koyu bir perdenin altında gerçek şantiye fotoğrafı, kehribar vurgulu editoryal başlık ve hero'ya yerleştirilmiş teklif isteme formu. Aynı prompt, kısıtları ux-skill verdiğinde farklı sonuç.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Önce: sıradan, stok fotoğraflı SEO slop. Sonra: koyu bir perdenin altında gerçek şantiye fotoğraflı hero, kehribar vurgulu editoryal başlık, hero içinde teklif formu. Aynı AI coding aracı, aynı prompt, kısıtları ux-skill verdiğinde farklı sonuç.*

> **v4.0, FOUNDATIONS: tek bir komut, WCAG'ye göre denetlenmiş eksiksiz bir tasarım sistemi kurar; Arapça ve sağdan sola yazım yerleşik gelir.** AI coding için en güçlü UX plugin'i. Deterministik 7 eksenli bir sentezleyiciye sahip Python akıl yürütme çekirdeği, sorgulanabilir 12 JSON manifest (84 stil, 176 palet, 70 tipografi eşleşmesi, 148 component, 184 sektör, 35 grafik türü, 57 motion preset'i, 112 UX yasası, 171 anti-pattern kuralı, 25 teknoloji stack'i, 160 marka spec'i), 18 slash komutu, 5 sub-agent, 25 MCP aracı ve deterministik bir anti-AI-slop linter. Cross-IDE: Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer ve Roo Cline'a kurulur.

> **Marka adı `ux-skill`.** PyPI / npm paket adı `uxskill` olarak kalır. GitHub reposu [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill) adresinde.

**Yazar:** [Laith Aljunaidy](https://laithjunaidy.com), Amman'da tasarımcı ve CTO · **Site:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Tüm Claude UX plugin'leriyle karşılaştırma:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-yükleyicisi)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### 4.0'da yeni: temeller

Bir marka rengi girer, bir tasarım sistemi çıkar; kontrastı da sana ulaşmadan önce denetlenmiş olur.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 veya daha yenisi. MCP sunucusu için `pip install --upgrade 'uxskill[mcp]'`. pipx ile `pipx install uxskill` (kurulu bir 3.x'in üzerine `pipx upgrade uxskill`). npm ile `npx uxskill@latest`. 3.x'ten mi geliyorsun? [Geçiş rehberi](docs/migrating-to-4.md) her 3.x token'ını 4.0'daki rolüne eşler.

**Bir ürün ya da landing page mi yapıyorsun?** Sayfana bağlayacağın `tokens.css`, seçilen yazı tipleri için metrikleri eşlenmiş yedek fontlarla `fonts.css`, yazı tiplerini kendi dosyalarından yükleyen `fonts-self-host.css`, araçlar için `tokens.json`, `art/` altında dekoratif marka görselleri ve neyin neden kurulduğunu, hangi sayfa kompozisyonuyla başlanacağını sade bir dille anlatan `system-report.md` elde edersin. Stilleri rollerle ver (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`), koyu modu, yüksek kontrastı, sıkı boşluğu, sağdan sola yazımı ya da azaltılmış hareketi `<html>` üzerindeki tek bir attribute ile aç kapa. Yazı tiplerini raporun verdiği Google Fonts bağlantısıyla ya da `fonts-self-host.css` ve bir `fonts/` klasörüyle yükle; her iki durumda da `fonts.css`'i `tokens.css`'ten önce bağla; iki dosyayı da düzenleme. `--brief` ile görünüm, brief sektörü ve tonu belirttiğinde onları izler; yapılandırılmış alanlar (yaş, diller, varsayılan şema, okuma bağlamı) metin boyutunu, dokunma alanlarını, yazı sistemlerini ve açılışta hangi şemanın geleceğini belirler; discovery sektör sormaz, bu yüzden `/ux-system create` sorar. Claude Code'da `/ux-system create` kurulu sürümü kontrol eder, build'i çalıştırır ve raporu açıklar.

**Bir tasarım sistemi mi tasarlıyorsun?** Dokuz temel (renk, tipografi, boşluk, yerleşim, köşe yarıçapı, kenarlık, yükselti, hareket, görsel), her biri yedi eksenle sürekli olarak değişir; primitive'ler ve semantik rollerle, W3C design tokens biçiminde (DTCG 2025.10) ve her modun değerleriyle. Aynı girdiler, aynı byte'lar. MCP üzerinden `ux_system_build` raporu, denetim sonucunu ve her dosyanın boyutunu döndürür; `out` verildiğinde komutla aynı dosyaları yazar.

- **WCAG denetimi.** Her metin, kontrol ve odak renk eşleşmesi açık ve koyu modda, standart ve yüksek kontrastta ölçülür: standart kontrastta WCAG 1.4.3 (metin 4.5:1) ve 1.4.11 (metin dışı 3:1), yüksek kontrastta WCAG 1.4.6 (metin 7:1); buna ek olarak, WCAG metin dışı öğeler için gelişmiş bir seviye tanımlamadığından, metin dışı öğelerin çoğu için yüksek kontrastta bize ait 4.5:1'lik bir alt sınır. Denetimden geçemeyen sistem yazılmaz; mesaj neyin değişmesi gerektiğini söyler.
- **Varsayılan olarak güvenli.** Farklı olan bir dosyanın üzerine asla yazmaz. `--force` dosyaları yalnızca sen istediğinde değiştirir.
- **Arapça.** `dir="rtl"` altında metin, kendi boyutları ve satır yüksekliği olan bir Arapça yazı tipine geçer; boşluklar mantıksal özellikler kullanır, hareket aynalanır. `--latin-only` bunu dışarıda bırakır.

**Zaten sahip olduğun bir sistem.** `/ux-system enhance --from` sistemi kendi adlarıyla okur (DTCG token'ları, CSS özel özellikleri, bir Tailwind teması, markdown kural dosyaları ya da bir Figma değişken dışa aktarımı), aynı denetimden geçirir ve kodunun onunla gerçekte ne yaptığını ölçer; hiçbir şey yeniden yazılmaz. `/ux-system extend --from` mevcut hiçbir token'ı değiştirmeden temeller, roller veya sözleşmeler ekler, bunu yanındaki bir uzantı dosyasında yapar; `uxskill system export` ise sistemi tokens.css, Tailwind 4 teması ya da Figma değişkenleri olarak yazar. 4.2 güven katmanını (her yazımda lint, bir son kontrol incelemecisi) ve lansmanı getiriyor. [Changelog](CHANGELOG.md)'a bak.

**Component'ler ve bölümler.** 23 component sözleşmesi, bir kontrolün her parçasının her durumda hangi token'lara bağlandığını ve her durumun nasıl hareket ettiğini söyler: durum değişikliği `motion.state` ile geçiş yapar, basma `motion.press.scale` ile ölçeklenir (azaltılmış harekette sabit kalır), sekmeler, menüler ve segmentli kontroller tek bir göstergeyi kaydırır. 14 bölüm sözleşmesi (hero, fiyatlandırma, SSS, footer ve diğerleri) her bölümün görevini, slot'larının aldığı component'leri, ihtiyaç duyduğu kanıtı ve telefonda nasıl üst üste dizildiğini belirtir. Bunlarla kurulan sayfalar fotoğraf kullanır; arayüz parçaları ek görseldir, asla yerine geçmez.

**Sayfayı okuyan bir linter.** 171 kural, çoğu ayrıştırılmış CSS ve markup üzerinde ek bir kontrolle, sayfanın kendi sistemini okur: hareketin zamanlaması kendi eğrisinden alınır, display başlıkların satır yüksekliği motorun alt sınırında tutulur, gizli bir kontrol sekme sırasından çıkmak zorundadır. `uxskill lint --render` her sayfayı headless Chromium'da masaüstü ve telefon genişliğinde açar ve kullanır: görünmeyen ya da kırpılan odak halkaları, geç yanıt veren hover ve basma, Escape sonrası kaybolan odak ve azaltılmış harekette hâlâ hareket eden bir basma.

**Daha az komut.** 25 slash komutu 18'e iner. `/ux-discover` `--frame` ve `--recommend` alır, `/ux-design` `--component`, `--dashboard` ve `--from-image` alır, `/ux-polish` skor 90'a ulaşana ya da üç tur geçene kadar lint, fix, re-lint döngüsünü çalıştırır, `/ux-init` ise `--stats` alır. Yedi eski ad takma ad olarak çalışmaya devam eder ve 4.1'de kalkar; [takma adlara](#takma-adlar-41de-kaldırılıyor) bak.

**Yüzey playbook'ları.** Landing, dashboard ve component kuralları `references/surfaces/` altında, her biri için bir playbook olarak durur. `/ux-design` moduna göre seçilen tam olarak birini yükler; böylece bir dashboard build'i hero kurallarını hiç okumaz.

Testler: **9764 geçiyor**. Çevrimdışı. Deterministik. Hiçbir zaman LLM çağrılmaz.

### v3.1'de yeni: markaya sadık, duyarlı, canlı

- **Marka sadakati umulmaz, zorunlu kılınır.** Ana renk LOGONUN piksellerinden okunur (en çok boyanan CSS'ten değil); varsayılan fontlar logonun harf stiline uymadığında reddedilir. Çıkarılan marka `recommend` -> `synthesize` yolunu izler ve `evaluate` içindeki **katı bir alt sınır**, marka rengini ya da logosunu kaybeden veya gerçek görsel içermeyen her çıktıyı BAŞARISIZ sayar. Açık `brand.md` kuralıyla iki yönlü uyum (render + içe aktarma).
- **Mobile-first, denetimli.** Yeni zanaat temelleri (`responsive.md`, `component-behaviors.md`) ve satır kaydırmayı dikkate alan bir denetim: yatay kaydırmada, satıra bölünen bir nav, logo ya da buton etiketinde veya fazla yüksek bir sticky header'da başarısız olur.
- **Wow katmanı.** Motor sayfa başına 2-3 eşgüdümlü imza anı türetir; «wow yalnızca kullanıcıdan gelebilir» doktrini geride kalır.
- **Daha keskin linter** (152 kural): zorunlu görsel ve yalnızca ikon tespiti, placeholder token ve `100vw` kuralları; seed'li picsum korunur, rastgele olan çıkarılır.

Notların tamamı [CHANGELOG.md](CHANGELOG.md) dosyasında.

### v3'te yeni neler var

- **Brand spec'leri artık şablon değil, eğitim verisi.** 160 brand spec, recommender'ın seçtiği bir katalog olmaktan çıktı, sentezleyicinin damıttığı kelime hazinesine dönüştü. Çıktı her çağrıda yeni.
- **7 eksenli sentezleyici** (warmth, contrast, density, geometry, formality, motion, type_personality). Brief deterministik biçimde eksen değerlerine eşlenir; eksen değerleri taze palette + tipografi + spacing + radius + motion token'larına derlenir.
- **Üç otomatik mod**: `strict_brand` (tek bir markanın %100'ü), `brand_anchor` (%70 tek marka + %30 kardeş markalardan eksen uyarlamalı), `pure_synthesis` (marka adı yok, eksen eşleşmeli 8 örnekten damıtma).
- **Decisions ledger recommender'ı yeniden sıralıyor.** `.ux/decisions.jsonl` aynı `(industry, ui_type)` kovasındaki geçmiş kazanımlara göre adayları re-rank ediyor. Cold-start güvenli. Sadece `lint_score >= 80` + `user_accepted = true` olan kararlar sayılır.
- **Eksen etkileşim matrisi**: rakip eksenler arasında açık çatışma çözümü (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Artık sessiz ad-hoc kural yok.
- **`/ux-evolve` otomatik döngüsü** (4.0'da `/ux-polish`'in varsayılan döngüsü): skor ≥ 90 olana, plato olana veya 4.0'da 3 tura (v3'te 5) kadar lint → polish → re-lint. Kalite kapısı 65'te.
- **3 yeni MCP aracı** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Yerel stats panosu**: `uxskill stats --html` SENİN kurulumunun öğrendiklerini `.ux/stats.html`'e yazar. Telemetri yok, küresel toplam yok.
- **223 test geçiyor.** Çevrimdışı. Deterministik. LLM hiç çağrılmıyor.

Tüm detaylar [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain) içinde.

### Yıldız geçmişi

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill nedir

ux-skill, AI coding araçları için bir **design intelligence motoru**. Bir Python paketi olarak (`pip install uxskill`), Claude Code plugin'i olarak ve 17 IDE'lik multi-yükleyici olarak çalışır. Motor bir proje brief'ini (sektör, hedef kitle, ton, must-have, yasaklı hamleler, stack, bölge) alır ve eksiksiz bir önerilen design sistemi döndürür: stil, palet, tipografik çift, motion preset'leri, component'ler, çalışılacak örnek brand'ler ve tutulması gereken anti-pattern guardrail'ları. Öneri deterministik, aynı girdi her zaman aynı çıktıyı verir.

Plugin, sen ve AI coding aracı arasında durur. Claude Code'a, Cursor'a veya başka bir AI asistanına «bir fintech landing oluştur» dediğinde, asistan tipik olarak doğaçlama yapar ve sonuç beş saniye içinde AI üretimi olarak okunur (mor-mavi gradyanlar, üç eşit card, display boyutunda Inter, testimonial'larda «John Doe», 300ms varsayılan geçişler, ortalanmış hero, zıplayan ok CTA'lar). ux-skill doğaçlamayı **yapılandırılmış kısıtlamalarla** değiştirir: brief'i yakalayıp sistemi seçmek için `/ux-discover`, kodu üretmek için `/ux-design` ve commit'ten önce 171 deterministik anti-AI-slop kuralından geçtiğini doğrulamak için `/ux-lint` çalıştırırsın.

Bu README kanonik referans. Her komut, her sub-agent, her data manifest, her install yolu, her brand spec, her anti-pattern kategorisi, hepsi burada belgelendi. Eğer Claude Code için bir design plugin'i arıyorsan ya da Cursor, Windsurf veya Codex için AI design araçlarını karşılaştırıyorsan, bunu baştan sona [compare.html](https://uxskill.laithjunaidy.com/compare.html) ile birlikte oku.

---

## İçindekiler

1. [Beyin, v3.0 nedir](#beyin-v30-nedir)
2. [Hızlı kurulum](#hızlı-kurulum)
3. [Sayılar, top 8 Claude UX skill'ine karşı canlı karşılaştırma](#sayılar-top-8-claude-ux-skilline-karşı-canlı-karşılaştırma)
4. [Mimari, parçalar nasıl birleşiyor](#mimari-parçalar-nasıl-birleşiyor)
5. [18 slash komutu, ayrıntılı başvuru](#18-slash-komutu-ayrıntılı-başvuru)
6. [5 sub-agent](#5-sub-agent)
7. [11 data manifest'i](#11-data-manifesti)
8. [171 anti-AI-slop kuralı, linter](#171-anti-ai-slop-kuralı-linter)
9. [160 brand DESIGN.md spec'i, kategoriye göre](#160-brand-designmd-speci-kategoriye-göre)
10. [MCP sunucusu, asimetrik hamle](#mcp-sunucusu-asimetrik-hamle)
11. [17 IDE yükleyicisi](#17-ide-yükleyicisi)
12. [Kullanım senaryoları, somut senaryolar](#kullanım-senaryoları-somut-senaryolar)
13. [Alternatiflerle karşılaştırma](#alternatiflerle-karşılaştırma)
14. [Roadmap](#roadmap)
15. [Katkıda bulunma](#katkıda-bulunma)
16. [Lisans, yazar, teşekkürler](#lisans-yazar-teşekkürler)

---

## Beyin: v3.0 nedir

v3.1.0, ux-skill tarihindeki en büyük mimari kaymadır. Recommender artık bir katalogdan şablon seçmiyor, motor her brief için taze bir tasarım dili **sentezliyor**. Aynı brief her zaman aynı çıktıyı verir (tamamen deterministik), ama her farklı brief kendi yeni sistemini alır. Brand spec'leri artık şablon değil; motorun kelime hazinesini öğrendiği eğitim verisidir. Sistem kendi geçmişini görür, geri besleme döngüsünü yerel olarak kapatır ve asla LLM çağırmaz.

Derleyici, **deterministik 7 eksenli sentezleyicidir**, warmth, contrast, density, geometry, formality, motion, type_personality. Her brief eksen değerlerine eşlenir; eksen değerleri taze palette + tipografi + spacing + radius + motion token'larına derlenir. Modüler tipografi ölçekleri oranlarını contrast'tan seçer (1.200 quiet / 1.250 balanced / 1.333 loud). Layout primitif'leri inşa gereği responsive (`auto-fit minmax(min(N, 100%), 1fr)` + container query). Kırık layout'lar yayınlanamaz çünkü temsil edilemezler.

Üç otomatik mod var: `strict_brand` (`reference_brands=[stripe] strict=True` → %100 Stripe token, en hızlı yol); `brand_anchor` (`reference_brands=[stripe]` → %70 Stripe + %30 4 kardeş markadan eksen uyarlamalı); ve `pure_synthesis` (marka adı yok → sonsuz uzay, eksen eşleşmeli 8 örnekten damıtılmış yeni bir tasarım dili). Çatışan eksenler belgelenmiş bir **eksen etkileşim matrisi** ile çözülür, dense + corporate 4px'e derlenir (density kazanır, Bloomberg ekolü), airy + corporate 12px'e (formality kazanır, lüks), soft + playful 18px radius'a, sharp + corporate 2px'e. Uygulamada sessiz ad-hoc kural yok.

**Decisions ledger** (`.ux/decisions.jsonl`, schema `_v: 1` kilitli) geri besleme döngüsünü kapatır. Recommender artık aynı `(industry, ui_type)` kovasındaki geçmiş kazanımlara göre adayları yeniden sıralıyor. Soğuk başlangıçta güvenli: 3 önceki kararın altında sıralamayı atlar. Yalnızca `lint_score >= 80` VE `user_accepted = true` olan kararları sayar. Ayrıca `/ux-polish` skor ≥ 90 olana, plato olana veya 3 tura kadar lint → polish → re-lint çalıştırır; 65'lik kalite kapısının altındaki çıktı `--force` olmadan reddedilir. Sonuç: her kurulum kendi külliyatı üzerinde daha akıllı hale gelir, her çalıştırma makineler arasında tekrarlanabilir, motor tamamen çevrimdışı kalır.

---

## Hızlı kurulum

Üç kurulum yolu. Ortamına uyanı seç.

### Yol 1: Claude Code marketplace (kanonik)

Claude Code'da yaşıyorsan, plugin marketplace üzerinden kur:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Bu, 18 slash komutunun hepsini (artı 4.1'e kadar takma ad olarak kalan 7 eski adı) ve 5 sub-agent'ı Claude Code oturumuna bağlar. Kurulumdan sonra, projeye özel `.ux/` state dizinini kurmak ve Python motorunun erişilebilir olduğunu doğrulamak için `/ux-init` çalıştır.

### Yol 2: pip (evrensel)

Claude Code dışında yaşıyorsan (Cursor, Windsurf, CLI, CI), Python paketini kur:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

Paket hem `ux` hem de `uxskill`'i CLI entry point'i olarak sunar, aynı binary.

### Yol 3: npx (Python gerekmez)

Python'u doğrudan yönetmek istemiyorsan, npx wrapper her şeyi `pipx` üzerinden bootstrap'ler:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Kurulumu doğrula

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

On iki sayının toplamı 1.262 giriş eder. Herhangi bir sayı 0 dönerse JSON dosyası eksiktir; [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) adresinde bir issue aç.

---

## Sayılar: top 8 Claude UX skill'ine karşı canlı karşılaştırma

Yıldız sayıları en son **2026-05-28**'de `gh api` ile doğrulandı. ux-skill (Laith0003/ux-skill) en yeni, farkındalıkta küçüğüz, mimaride derin. Aşağıdaki karşılaştırma dürüst: nerede kaybediyoruz, nerede kazanıyoruz.

| Plugin | Yıldız | Mimari | Slash komutları | Linter (CI-safe) | Brand spec'leri | Component'ler | Motion preset'leri | Desteklenen IDE'ler |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, tek skill | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + araştırma destekli taste | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Tek 62 KB SKILL.md + script'ler | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | MCP-bağlı skill kütüphanesi | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Tek estetik skill'i | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Anti-slop design skill'i | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 component'ler + audit | 1 | - | (sadece MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python motoru + 12 manifest + 18 komut + 5 sub-agent + CI linter** | **18** | **171 deterministik kural** | **160** | **148** | **57** | **17** |

### Nerede kaybediyoruz

- **Farkındalık.** Onların yüzbinlerce yıldızı var. Bizim 14. Bize yıldız ver, yardım etmenin en ucuz yolu.
- **Brand tanınırlığı.** ui-ux-pro-max ve open-design'ın günler değil aylarla ölçülen bir başlangıç farkı var.
- **Marketing parlatması.** Onların ekran görüntüleri, demo videoları ve bulunabilir bir landing'i var. Bizim kapsamlı bir README'miz ve zayıf bir landing'imiz var.

### Nerede kazanıyoruz

- **Component kütüphanesi:** Anatomi, durumlar, kullanılan token'lar ve motion özellikleri ile 148 belgelenmiş component. Diğer 8'in hiçbiri component manifest'i dağıtmıyor.
- **Motion preset'leri:** Reduced-motion fallback'leriyle stack-ready 57 giriş (Framer Motion, GSAP, CSS). Diğerlerinin hiçbiri motion manifest'i dağıtmıyor.
- **Anti-pattern linter:** 171 deterministik kural, CI'da çalışır, Critical/High'ta non-zero ile çıkar. Diğerlerinin hiçbiri deterministik linter dağıtmıyor.
- **Brand spec'leri:** 160 gerçek DESIGN.md spec (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude ve 96 daha). Diğerlerinin hiçbiri brand kütüphanesi dağıtmıyor.
- **17 desteklenen IDE:** aynı motor, IDE başına farklı yapıştırıcı.
- **18 slash komutu:** discovery, üretim (sayfalar, component'ler, dashboard'lar, bir görselden), audit, lint, polish döngüsü, fix döngüsü, case-study, workshop, copy, motion, a11y, conductor, tamamen entegre.

Tam tablo bazlı yan yana karşılaştırma için: [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Mimari: parçalar nasıl birleşiyor

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

### Motor gerçekte nasıl çalışır

1. **Girdi.** Brief'i ya `/ux-discover` (10 alan) ile etkileşimli olarak ya da `ux recommend` bayraklarıyla etkileşimsiz olarak verirsin.
2. **5 paralel arama.** Motor manifest'ler üzerinde aynı anda beş sorgu çalıştırır:
   - **Sektör → recommended_styles** (industries.json)
   - **Stil → palet + tipografi + motion uyumluluğu** (styles.json)
   - **Ton × olmazsa olmaz → palet filtresi** (palettes.json)
   - **Stack → component uyumluluğu + motion preset'leri** (tech-stacks.json, motion-presets.json)
   - **Yasaklar + bölge → guardrail'lar + örnek marka kısa listesi** (anti-patterns.json, brands/)
3. **Birleştirme.** Deterministik bir birleştirici adayları sıralar, çakışmaları çözer (örneğin olmazsa olmaz koyu mod palet modunu belirler) ve tek bir önerilen sistem çıkarır.
4. **Çıktı.** Seçilen stil, palet, tipografi çifti, en iyi 5 motion preset'i, en iyi 12 component, en iyi 5 örnek marka ve 171 anti-pattern guardrail'ının tamamı etkin olarak içeren bir JSON belgesi. Artı her seçimi açıklayan bir gerekçe bloğu.
5. **Üretim.** Sonraki komutlar (sayfa, component, dashboard ve görsel modlarıyla `/ux-design` ile `/ux-system`) öneriyi kullanarak sub-agent'lar aracılığıyla gerçek kod üretir.
6. **Doğrulama.** `/ux-lint` üretilen kodu 171 kurala karşı yeniden tarar. CI'da Critical/High'ta non-zero ile çıkar.

**v3 eklemeleri.** Recommender artık adayları `engine/decisions/` üzerinden `.ux/decisions.jsonl` kullanarak yeniden sıralıyor (yalnızca `lint_score >= 80` VE `user_accepted = true` olan kararlar sayılır; 3 önceki kararın altında soğuk başlangıçta güvenli). Üretim yolu, bir katalogdan şablon seçmek yerine her brief için taze palet + tipografi + boşluk + köşe yarıçapı + motion token'ları üreten deterministik 7 eksenli derleyici `engine/synthesizer/`'a yönlenebilir. Ayrıntılar için [Beyin, v3.0 nedir](#beyin-v30-nedir).

**Python düşünür. HTML gösterir. Markdown zincirler.**

---

## 18 slash komutu: ayrıntılı başvuru

Her komut `commands/` altında `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` ve `output state file` içeren bir `.md` dosyası olarak gelir. Aşağıdaki açıklamalar kısaltılmıştır; tam kaynak, asıl spesifikasyondur.

Komutlar yedi grupta toplanır: **bootstrap ve envanter**, **discovery ve öneri**, **üretim**, **audit ve doğrulama**, **fix ve polish**, **discovery ve anlatı** ve **conductor**. 3.x'ten yedi ad 4.1'e kadar [takma ad](#takma-adlar-41de-kaldırılıyor) olarak çalışmaya devam eder.

### Bootstrap & envanter

#### `/ux-init`: projeyi bootstrap'le

- **Ne yapar:** Hangi IDE'yi kullandığını algılar (`.claude/`, `.cursor/`, `.windsurf/`, vs.), doğru artefaktı kurar, Python motorunun erişilebilir olduğunu doğrular ve bir istatistik anlık görüntüsü yazdırır. `--stats` yalnızca anlık görüntüyü yazdırır: sürüm + veri manifest'lerindeki giriş sayıları.
- **Ne zaman kullan:** Yeni bir projeye ilk yükleme. ux-skill kullanan bir projeyi klonladıktan sonra. `pip install --upgrade uxskill` sonrası. `--stats` kurulumdan sonra, güncellemeden sonra ya da bir öneri şaşırtıcı seçimler döndürdüğünde ve manifest'lerin eksik olduğundan şüphelendiğinde.
- **Ne zaman atla:** Bu projede zaten çalıştırdın ve hiçbir şey değişmedi. `--stats` asla atlanması gereken bir şey değil: 50ms'lik bir okuma.
- **Çağırma:** `/ux-init` (argüman yok), `/ux-init --stats` ya da CLI'dan `uxskill init` / `uxskill stats`. `--decisions` decisions ledger özetini ekler; `--html` `.ux/stats.html` dosyasını yazar.
- **Çıktı:** IDE başına artefakt ([17 IDE yükleyicisi](#17-ide-yükleyicisi)'ne bak) + `.ux/` dizini + stdout özeti. `--stats`: stdout'a JSON (yukarıdaki [Kurulumu doğrula](#kurulumu-doğrula) bölümüne bak).
- **Bağlanır:** Sırada `/ux-discover`. `--stats` yalnızca tanı içindir.

#### `/ux-mcp`: motoru bir MCP sunucusu olarak çalıştır

- **Ne yapar:** Motoru stdio üzerinden bir Model Context Protocol sunucusu olarak başlatır. 25 araç (recommender, linter, kalıcılık, sentezleyici, decisions ledger, görselden çıkarım, veri manifest'leri ve bir tasarım sistemini kurma, içe aktarma, iyileştirme, genişletme, dışa aktarma ve denetleme) plugin olmadan MCP destekli herhangi bir host'tan çağrılabilir hale gelir.
- **Ne zaman kullan:** MCP destekli başka bir host'ta çalışıyorsun ve aynı motoru istiyorsun. Tek bir tasarım kısıtı kaynağına ihtiyaç duyan çok agent'lı bir pipeline çalıştırıyorsun. Recommender'ı ya da linter'ı CI'da uzun ömürlü bir süreç olarak istiyorsun.
- **Ne zaman atla:** Plugin'i kurulu Claude Code içindesin; slash komutları motora zaten ulaşıyor. Tek seferlik bir cevaba ihtiyacın var; `uxskill recommend` ya da `uxskill lint` daha basit.
- **Çağırma:** `/ux-mcp` ya da `pip install 'uxskill[mcp]'` sonrası shell'den `ux-mcp`.
- **Çıktı:** Bir stdio JSON-RPC sunucusu. İstemci başına yapılandırma için [MCP sunucusu](#mcp-sunucusu-asimetrik-hamle) ve `commands/ux-mcp.md` dosyasına bak.
- **Bağlanır:** Hiçbir şeye; bir taşıma katmanıdır, bir adım değil.

### Discovery & öneri

#### `/ux-discover`: zorlayıcı işlev (10 alanlı giriş, çerçeveleme, öneri)

- **Ne yapar:** Her projenin herhangi bir üretim komutundan önce geçtiği zorunlu 10 alanlı giriş. Proje türü, hedef kitle, birincil hedef, ton, olmazsa olmazlar, yasaklar, referans markalar, stack, bölge, başarı metriği. **Doğaçlama yok.** Yasaklı ifadeler («modern», «temiz») kullanıcıyı somut olmaya zorlar. Ardından recommender'ı çalıştırır: Python motorunun 12 manifest üzerindeki 5 paralel araması tek bir birleştirilmiş tasarım sistemi döndürür (Sektör → Stil → Palet → Tipografi → Motion + Component'ler + Örnek markalar + Guardrail'lar).
- **Modlar:** `--frame` kimin için, sonuç, hipotez ve başarı sinyalini dört alanlı bir çerçeveleme bloğunda toplar; tam girişten daha hafiftir. `--recommend` yalnızca recommender'ı, kayıtlı bir brief'ten ya da tek seferlik bayraklardan çalıştırır.
- **Ne zaman kullan:** Herhangi bir `/ux-design` ya da `/ux-system` öncesinde. Önceki brief eskidiğinde. `--frame` bir projenin, sprintin ya da tek seferlik bir işin başında veya bir konuşma rotadan çıktığında yolun ortasında. `--recommend` yorgun görünen bir ürünü yeniden konumlandırırken.
- **Ne zaman atla:** Bir hatayı düzeltiyorsun (`/ux-fix`). Yalnızca bir linter geçişi çalıştırıyorsun (`/ux-lint`). Brief son oturumdan beri değişmedi.
- **Çağırma (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` ya da `/ux-discover --recommend`.
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
- **Çıktı:** `.ux/last-discovery.json` (10 alanlı brief), `.ux/last-recommendation.json` (seçilen stil, palet, tipografi çifti, en iyi 5 motion preset'i, en iyi 12 component, en iyi 5 örnek marka, 171 anti-pattern guardrail'ının tamamı etkin, artı gerekçe) ve `--frame` ile `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Bağlanır:** `/ux-design [extra brief]` → öneriye dayanan frontend kodu. `/ux-design --component <name>` → ortaya çıkan kısıtlara uyumlu tek bir component. `/ux-system` → öneriden eksiksiz tasarım sistemi. `/ux-lint` → üretilen kodu doğrula.

### Üretim

#### `/ux-design`: brief'ten güzel, anti-slop bir yüzey üretir

- **Ne yapar:** Discovery brief'i + öneriden eksiksiz, production-grade bir frontend artefaktı (landing, marketing sitesi, app shell) üretir. anti-slop ve arsenal referanslarından gelen yaratıcı yönlendirmeyle `frontend-engineer`'ı görevlendirir. Brief ya da bir bayrak dört moddan birini seçer:
  - **sayfa** (varsayılan): tam bir sayfa ya da çok bölümlü bir yüzey. `.ux/last-design.json` yazar.
  - **`--component [name]`**: tek bir production-grade component (buton, modal, navbar, sidebar, card, tablo, form, grafik). Dört etkileşim durumunun hepsi, erişilebilir, markaya uygun. Component'i önce `.ux/last-recommendation.json` içinde arar, bulamazsa doğrudan manifest'i sorgular. `.ux/last-component.json` yazar.
  - **`--dashboard`**: veri yoğunluğu disiplini, bento layout, tablo hizalı monospace rakamlar, sparkline pattern'leri, card aşırılığına karşı tutum, semantik durum renkleri, ölçülü motion. Üzerine grafikler yapıştırılmış bir marketing sitesi değil. `.ux/last-dashboard.json` yazar.
  - **`--from-image <path>`**: bir referans görseli (PNG/JPG/WebP) saf Pillow görüntü işlemeyle okur (baskın palet, zemin kutupluluğu, tipografi sinyali), palet ve stil manifest'leriyle eşleştirir ve ortaya çıkan öneriden kurar. `--extract-only` çıkarımdan sonra durur. `.ux/last-image-extract.json` yazar.
- **Ne zaman kullan:** «Design a», «build me a», «generate a landing page», «create a dashboard», «make a component», «build a button», «design the admin panel», «operator console», «KPI board», «build it like this screenshot», serbest formatlı görsel teslimat isteği.
- **Ne zaman atla:** İnceleme istiyorsun, build değil (`/ux-audit` veya `/ux-critique` kullan). Backend veya altyapı işi.
- **Çağırma:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Çıktı:** Üretilen kod (HTML / Blade / JSX / Vue / Astro) artı modun state dosyası.
- **Bağlanır:** `/ux-lint` → guardrail'lara karşı doğrula. `/ux-polish` → kozmetik geçiş. `/ux-a11y` → erişilebilirlik audit'i. `/ux-copy` → microcopy incelemesi. `/ux-fix` → bulguları atomik commit olarak uygula.

#### `/ux-system`: eksiksiz başlangıç design sistemi üretir

- **Ne yapar:** Sahip olmayan bir proje için eksiksiz bir başlangıç design sistemi önerir, token'lar (renk, tip, boşluk, motion, yarıçap, gölge), foundation belgeleri, component kontratları, dark-mode eşleşmeleri, theme switcher. `design-system-architect`'i görevlendirir.
- **Ne zaman kullan:** «Bir design sistemimiz yok», «bize bir sistem kur», «token öner», «temamız ne olmalı», «DS'mizi kur».
- **Ne zaman atla:** Projenin zaten bir tasarım sistemi var; bunun yerine mevcut sistem üzerinde `/ux-design --component` kullan. Backend veya altyapı.
- **Çağırma:** `/ux-system create` (temeller motoru), `/ux-system enhance --from <file>` (zaten sahip olduğun bir sistemi ölç), `/ux-system extend --from <file> --add <foundation>` (onu değiştirmeden genişlet) ya da `/ux-system` (3.x akışı; henüz kayıtta yoksa önce discovery çalıştırır).
- **Çıktı:** `tokens.json`, `foundations.md`, `components/*.md` kontratları, opsiyonel Tailwind / vanilla / SCSS emit. Zincir bağlamı için `.ux/last-system.json` yazar.
- **Bağlanır:** `/ux-design --component` → yeni sistem üzerine kur. `/ux-design` → yeni token'larla bir yüzey üret.

#### `/ux-motion`: motion işlemi

- **Ne yapar:** Bir yüzeyin motion katmanını üretir, süreler, easing'ler, koreografi, reduced-motion fallback'leri, performans disiplini. Ayrıca mevcut motion'ı 5 boyuta karşı denetler (timing, easing, anlam, reduced-motion, performans).
- **Ne zaman kullan:** «Motion kontrolü», «animasyonlar iyi mi», «motion'ı düzelt», «animasyonları incele», «motion audit'i», «motion'da performans geçişi».
- **Ne zaman atla:** Yüzeyde motion yok (`/ux-audit` veya `/ux-polish` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-motion path/to/component.tsx` (audit modu) veya `/ux-motion --generate hero-entry` (üretim).
- **Çıktı:** Güncellenmiş kod (üretim modunda) veya `.ux/last-motion.json` raporu (audit modunda).
- **Bağlanır:** `/ux-fix` → motion bulgularını uygula. `/ux-polish` → sıkıştır.

### Audit & doğrulama

#### `/ux-lint`: deterministik regex tabanlı linter (LLM yok, CI-safe)

- **Ne yapar:** Kodun üzerinde 171 kural çalıştırır. LLM çağrısı yok. CI'da Critical / High'ta non-zero ile çıkar. Kaynak: `data/anti-patterns.json`. Kurallar A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) kapsar.
- **Ne zaman kullan:** Pre-commit hook. CI gate. `/ux-audit` maliyetini ödemeden önce büyük bir codebase'de hızlı ilk geçiş. Üretimi doğrulamak için herhangi bir moddaki `/ux-design` sonrası.
- **Ne zaman atla:** Bir fix loop istiyorsun (linter raporlar, düzenlemez, `/ux-polish --fix` veya `/ux-fix`'e bağla). Taste yargısı istiyorsun (`/ux-critique` kullan).
- **Çağırma (slash):** `/ux-lint src/`.
- **Çağırma (CLI):** `uxskill lint .` veya `python3 bin/ux-lint.py .` veya `bash bin/ux-lint.sh --ci --fail-on high`.
- **Çağırma (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Çıktı:** stdout'a bulgular (konum, kural id'si, severity, kanıt). Temizse exit kodu 0, `--fail-on high` set olduğunda Critical/High'ta non-zero.
- **Bağlanır:** `/ux-polish --fix` → aynı pattern'ler üzerinde LLM-driven karşılık. `/ux-fix` → bulguları severity'ye göre sıralanmış commit olarak uygula. `/ux-audit` → tam 6-lensli akıl yürütme geçişi. `/ux-next` → conductor'a karar verdir.

#### `/ux-audit`: 6 lensli design audit'i

- **Ne yapar:** Altı lense karşı yapılandırılmış, görüş sahibi bir inceleme (netlik, hiyerarşi, erişilebilirlik, ses, motion, taste), severity-etiketli bulgular üretir. Polaris tarzı rapor. Önce `.ux/last-frame.json`'ı okur, hedef kitle ve outcome her bulgunun severity'sini sabitler.
- **Ne zaman kullan:** Yüzey var ve savunulabilir bir eleştiri istiyorsun. «Audit», «UX'i incele», «iyi mi bu», «ne bozuk», «bunu parçala».
- **Ne zaman atla:** Yüzey henüz yok (`/ux-design` kullan). Kullanıcı bir lens istiyor (hedeflenmiş komutu kullan: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Kullanıcı taste görüşü istiyor (`/ux-critique` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-audit https://example.com/pricing` veya `/ux-audit src/components/Pricing.tsx`.
- **Çıktı:** `.ux/last-audit.json` yazar, `{lens, severity, title, principle, evidence, fix}`'ten `findings` dizisi, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Bağlanır:** `/ux-fix` → bulguları uygula. `/ux-polish` → kozmetik geçiş. `/ux-design` → yapısal redesign gerekirse.

#### `/ux-a11y`: WCAG 2.1 AA audit'i + ortak nezaket kontrolleri

- **Ne yapar:** Yapılandırılmış bir WCAG 2.1 AA audit'i, artı otomatik araçları geçen ama gerçek kullanıcıları hâlâ inciten ortak nezaket kontrolleri (focus görünürlüğü, hata özgüllüğü, motion tercihleri, klavye tuzakları, renge bağımlılık).
- **Ne zaman kullan:** Pre-ship erişilebilirlik gate'i. Bir redesign'dan sonra. «Erişilebilirlik kontrolü», «WCAG audit'i», «bu erişilebilir mi», «a11y incelemesi», «screen reader testi», «klavye nav kontrolü».
- **Ne zaman atla:** Kullanıcıya dönük değil. Backend veya altyapı. Work-in-progress eskizler.
- **Çağırma:** `/ux-a11y https://example.com` (live URL tercih edilir, otomatik araçlar ve klavye testi sadece live'da çalışır).
- **Çıktı:** `.ux/last-a11y.json` yazar, `{wcag_sc, sc_name, severity, title, evidence, fix, category}`'ten `findings` dizisi, `beyond_wcag` dizisi, `severity_counts`.
- **Bağlanır:** `/ux-fix` → bulguları commit olarak uygula. `/ux-copy` → bir copy geçişinin parçası olarak alt text ve form-hata kablolamasını düzelt.

#### `/ux-critique`: taste çağrısı (3 kazanım, 3 ıskalama, 1 stratejik hamle)

- **Ne yapar:** Bir designer'ın görüşü, yapılandırılmış audit değil, severity puanı değil, sadece neyin işe yaradığını, neyin yaramadığını ve en çok şeyi değiştirecek o tek stratejik hamleyi adlandıran sıkı, görüş sahibi bir take.
- **Ne zaman kullan:** «Ne düşünüyorsun», «iyi mi bu», «bunu eleştir», «dürüst görüş», «vibe doğru mu», «biz gibi hissettiriyor mu», «bunu ship etmeli miyiz».
- **Ne zaman atla:** Kullanıcı açıkça yapılandırılmış bir audit istiyor (`/ux-audit` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-critique https://example.com`.
- **Çıktı:** `.ux/last-critique.json` yazar, 3 kazanım, 3 ıskalama, 1 stratejik hamle, artı düzyazı.
- **Bağlanır:** Take redesign önerirse `/ux-design`. Take sıkıştırma önerirse `/ux-polish`.

#### `/ux-copy`: microcopy incelemesi + yeniden yazım

- **Ne yapar:** Her görünür string'i ses rubriğine karşı değerlendirir ve bir before/after yeniden yazımı üretir. Yakalar: «form contains errors» (genel), «John Doe» (placeholder), AI-neşeli kutlayıcı copy, genel CTA'lar, ölü empty state'ler, yararsız hatalar.
- **Ne zaman kullan:** Yapı doğru ama kelimeler zayıf. «Copy'yi incele», «microcopy'yi düzelt», «hata mesajları kötü», «bunu yeniden yaz», «string'leri sıkıştır», «butonlar genel duyuyor», «bu empty state ölü».
- **Ne zaman atla:** Layout sorunları (`/ux-audit` veya `/ux-polish` kullan). Alt text gibi erişilebilirlikten kaynaklanan copy sorunları (`/ux-a11y` kullan). Backend veya altyapı.
- **Çağırma:** `/ux-copy src/views/checkout.blade.php`.
- **Çıktı:** `.ux/last-copy.json` yazar, `{location, severity, before, after, notes}`'tan `strings` dizisi, artı rubrik + çeviri gerektiren locale'ler.
- **Bağlanır:** `/ux-fix` → yeniden yazımları uygula. `/ux-a11y` → copy düzeltmelerinden sonra tekrar kontrol et.

### Fix & polish

#### `/ux-fix`: bulguları atomik commit olarak uygula

- **Ne yapar:** `.ux/`'den son raporu okur (audit, copy, a11y, motion veya polish), working tree'yi doğrular ve bulguları doğru sub-agent'lar aracılığıyla atomik commit olarak uygular. Kaynak komutu yeniden çalıştırarak yeniden doğrular.
- **Ne zaman kullan:** Bir audit-sınıfı komutu çalıştırdıktan ve bulguları inceledikten sonra. «Bulguları düzelt», «düzeltmeleri uygula», «fix loop'u çalıştır», «yüzeyi yamala», «değişiklikleri yap», «düzelt onu».
- **Ne zaman atla:** `.ux/`'de önceki rapor yok. Working tree kirli ve kullanıcı stash/commit'e razı olmadı. Düzeltmeler mekanik uygulama değil, design yargısı gerektiriyor (redesign için `/ux-design` kullan).
- **Çağırma:** `/ux-fix` (hangi raporun düzelteceğini otomatik algılar) veya `/ux-fix --from=last-a11y.json`.
- **Çıktı:** Bulgu başına atomik commit'ler. Kaynak komutu yeniden çalıştırır ve `.ux/last-*.json` dosyasını günceller. Bir özet yazdırır.
- **Bağlanır:** `/ux-next` → conductor sonraki hamleyi seçer.

#### `/ux-polish`: lint, fix, re-lint döngüsü + AI-slop'u öldür

- **Ne yapar:** Önce yerel bir HTML dosyası üzerinde deterministik bir döngü: lint, altı idempotent polish geçişi, re-lint; skor 90'a ulaşana, yerinde sayana ya da üç tur geçene kadar (`--rounds` sınırı değiştirir). Varsayılan olarak döngü çıktısı `<file>.evolved.html` içinde kalır ve orijinale asla dokunulmaz. Orijinali yalnızca `--loop-only` ya da `--fix` değiştirir, temiz çalışma ağacı kontrolünden sonra; 65'lik kalite kapısı başarısız bir sonucun `--force` olmadan onun yerine geçmesini engeller; `--brand-file` ile marka sadakati alt sınırı her çıkışta geçerlidir. Ardından zevk geçişi: boşluk ritmi, hiyerarşinin keskinleştirilmesi, AI-slop tespiti, token tutarlılığı. `/ux-lint`'in LLM güdümlü karşılığı, zevk kararlarında senin yargını kullanır. `--loop-only` yalnızca döngüyü çalıştırır; `--no-loop` yalnızca zevk geçişini; `--fix` zevk bulgularını uygular.
- **Ne zaman kullan:** Yapı doğru ama uygulama gevşek. «Cilala», «bunu sıkılaştır», «AI-slop'u kaldır», «premium yap», «daha az AI görünümlü yap», «boşluk yanlış geliyor», «bu sıradan görünüyor», «daha fazla zevk gerek», «skor 90+ olana kadar iyileştir», «yayına hazır hale getir».
- **Ne zaman atla:** Yüzeyde temel işlevsellik eksik (önce onu düzelt). Polish değil yeniden tasarım gerekiyor (`/ux-design` kullan). Metin sorunları (`/ux-copy` kullan). Motion sorunları (`/ux-motion` kullan). A11y sorunları (`/ux-a11y` kullan).
- **Çağırma:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Çıktı:** Döngüden `<file>.evolved.html` (orijinalin yerine yalnızca `--loop-only` ya da `--fix` ile geçer), `--fix` ile güncellenmiş kod, `.ux/last-evolve.json`, `.ux/decisions.jsonl` içinde bir satır ve zevk bulgularını anlatan `.ux/last-polish.json`.
- **Bağlanır:** `/ux-lint` → polish'in tuttuğunu doğrula. `/ux-a11y` → erişilebilirliği yeniden kontrol et.

### Discovery & anlatı

#### `/ux-research`: araştırma planlama + sentez

- **Ne yapar:** Planlama modu: görüşme script'leri, anketler, recruitment screener'ları yazar. Sentez modu (`--synthesize`): görüşmeleri, analytics'i, rakip sitelerini, A/B sonuçlarını, support ticket'larını önerilere sindirir. `research-synthesizer`'ı görevlendirir.
- **Ne zaman kullan:** «Bir araştırma çalışması planla», «görüşme soruları lazım», «bir anket tasarla», «kullanıcı nasıl recruit ederim», «kullanıcı test planı», «diary study», «preference test», «fake door», «smoke test», «görüşme notlarımı sentezle».
- **Ne zaman atla:** Cevap yüksek güvenle zaten biliniyor. Düşük riskli geri alınabilir kararlar. Backend veya altyapı.
- **Çağırma:** `/ux-research --plan "loyalty wallet adoption in MENA"` veya `/ux-research --synthesize interviews/*.md`.
- **Çıktı:** `.ux/last-research.json` yazar, araştırma planı veya sentezlenmiş temalar + kanıt + öneriler.
- **Bağlanır:** `/ux-discover --frame` → bulguları bir çerçeveye entegre et. `/ux-design` → bulgulardan üret. `/ux-workshop` → araştırmayı girdi olarak kullanan bir workshop yürüt.

#### `/ux-workshop`: 5 fazlı design thinking workshop'u

- **Ne yapar:** Bir discovery / design-thinking workshop'unu uçtan uca kolaylaştırır. Beş ardışık faz (keşif → heat map → stakeholder haritası → çözüm eskizi → game plan). Zaman kutulu. Faz başına somut artefaktlar. «İlginç bulgularla» değil, bir kararla biter.
- **Ne zaman kullan:** Gerçek soru, gerçek katılımcılar, gerçek zaman bütçesi. «Bir workshop yürüt», «bir discovery kolaylaştır», «design thinking oturumu yapalım», «bir saatliğine stakeholder'larım var, ne yapıyoruz», «projeyi başlat».
- **Ne zaman atla:** Brief zaten net ve kapsamı belli. Tek başına beyin fırtınası (`/ux-design` ya da `/ux-discover --frame` kullan). Takım discovery'de değil, uygulamanın ortasında.
- **Çağırma:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Çıktı:** `.ux/last-workshop.json` yazar, game plan + faz başına artefaktlar.
- **Bağlanır:** `/ux-design` → game plan'i yürüt. `/ux-research` → workshop'un yüzeye çıkardığı boşlukları doldur. `/ux-case-study` → yolculuğu yayımla.

#### `/ux-case-study`: yayınlanabilir case study (Wfrah-editorial formatı)

- **Ne yapar:** Saf monokrom editoryal formatta bir proje vaka çalışması üretir: Wfrah tipografisi, ince ayırıcılar, (A) ile (G) arasında numaralı bölüm kodları, iki dilli içeriğe güvenli yerleşim. Bir belge, pazarlama broşürü değil. `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json` dosyalarından okur.
- **Ne zaman kullan:** Lansman sonrası. Ayrık bir milestone'dan sonra. «Bir case study yaz», «bu projeyi case study yap», «wrap-up belgesini yap», «bu işi yayımla», «portfolio parçası».
- **Ne zaman atla:** Projede (A) ile (G) arasındaki bölümleri dolduracak veri yok. Kullanıcı vaka çalışması değil, pazarlama landing'i istiyor (`/ux-design` kullan).
- **Çağırma:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Çıktı:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Bağlanır:** Terminal komutu, genellikle bir projenin sonu.

### Conductor

#### `/ux-next`: workflow yöneticisi (read-only)

- **Ne yapar:** Her `.ux/last-*.json`'ı okur ve en yüksek kaldıraçlı sonraki komutu adlandırır. Bir yönetici, inşaatçı değil. Read-only.
- **Ne zaman kullan:** Komutlar arasında. «Sırada ne yapmalıyım», «sıradaki hamle ne», «benim için karar ver», «buradan nereye gidiyoruz».
- **Ne zaman atla:** `.ux/`'de önceki rapor yok. Aklında spesifik bir sonraki komut var.
- **Çağırma:** `/ux-next` (argüman yok) veya `/ux-next --focus=a11y`.
- **Çıktı:** Stdout, önerilen sonraki komut + rationale.
- **Bağlanır:** Hangi komutu seçerse.

#### `/ux-expert`: danışmanlık bağlantısı

- **Ne yapar:** Bir kullanıcı gerçek hayatta bir UX uzmanı istediğinde plugin yaratıcısının iletişim bilgisini yüzeye çıkarır. Kısa, doğrudan, marketing yok.
- **Ne zaman kullan:** «Bunu kim yaptı», «bir UX uzmanına ihtiyacım var», «danışmanlık yapar mısın», «bunun için birini tutabilir miyim», «bu plugin'in arkasında bir insan var mı».
- **Ne zaman atla:** Kullanıcı danışmanlık değil plugin özelliklerini soruyor.
- **Çağırma:** `/ux-expert`.
- **Çıktı:** LinkedIn / email / repo ile kısa iletişim kartı.

### Takma adlar, 4.1'de kaldırılıyor

3.x'ten yedi komut yukarıdaki 18 komutun içine katıldı. Adları bir sürüm daha çalışır: her takma ad nereye taşındığını söyler, sonra yeni komutu aynı argümanlarla çalıştırır.

| Eski komut | Şimdi | Notlar |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | Aynı çerçeveleme bloğu, aynı `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | `ux_recommend` MCP aracı değişmedi |
| `/ux-stats` | `/ux-init --stats` | Salt okunur anlık görüntü |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | Takma ad eski beş turluk sınırı korur; `/ux-polish` tek başına üçte durur |
| `/ux-component` | `/ux-design --component` | Aynı `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | Aynı `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Görselden kurmak için `--extract-only`'yi kaldır |

### Komut zincir grafı

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

## 5 sub-agent

Sub-agent'lar komutlar tarafından görevlendirilen role özgü üreticilerdir. Asla bağımsız çalışmazlar; `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research` vs. tarafından çağrılırlar. Her agent'ın tanımlı bir sorumluluk sınırı vardır: brief'e karar VERMEZ; onu uygular.

### `frontend-engineer`

- **Sahibi:** Anti-AI-slop disiplini ile production-grade frontend kodu (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro).
- **Görevlendiren:** `/ux-design` (sayfa, component, dashboard ve görsel modları), `/ux-fix`.
- **Girdiler:** Brief + yaratıcı yönlendirme + token'lar (`.ux/last-recommendation.json`'dan).
- **Çıktılar:** Genel AI çıktısından ayırt edilebilir çalışan kod. Mor gradyan yok, ortalanmış hero yok, üç eşit card yok, display boyutunda Inter yok, «John Doe» yok, emoji yok, 300ms varsayılan yok.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Sahibi:** Production frontend kodunda motion, Framer Motion, GSAP, CSS animasyonları. Süreler, easing'ler, koreografi, reduced-motion fallback'leri, performans disiplini.
- **Görevlendiren:** `/ux-design` (her mod), `/ux-motion --fix`.
- **Girdiler:** Motion brief'i + token'lar + `data/motion-presets.json`'dan 57 motion preset'i.
- **Çıktılar:** Yerini kazanan motion. Her zaman `prefers-reduced-motion` fallback'leriyle sarılır. Her zaman Core Web Vitals'a karşı test edilir.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Sahibi:** Ship'lenen string'ler, hata mesajları, empty state'ler, CTA'lar, loading state'leri, başarı mesajları, toast'lar, helper text, form etiketleri, button text'i.
- **Görevlendiren:** `/ux-copy --fix`, `/ux-design` (her mod), `/ux-discover --frame`.
- **Girdiler:** Ses profili (isimli veya yapıştırılmış) + yüzeyin string'leri.
- **Çıktılar:** Ürünün on değil, tek bir ürün gibi ses çıkarması için bir yüzeyin her durumunda tutarlı şekilde uygulanan production microcopy. Yasaklar: «form contains errors», «John Doe», AI-neşeli kutlayıcı copy, genel CTA'lar, ölü empty state'ler.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Sahibi:** Araştırma girdilerini (görüşmeler, analytics, rekabetçi siteler, A/B sonuçları, support ticket'ları) eyleme geçirilebilir design önerilerine sindirme.
- **Görevlendiren:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Girdiler:** Ham araştırma, transkriptler, export'lar, rakip URL'ler, support cluster'ları.
- **Çıktılar:** Temalar, kanıtlar, öneriler. Cevabı asla tasarlamaz, designer'a tasarımdan başlayacağı substratı verir.
- **Araçlar:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Sahibi:** Eksiksiz design sistemleri, token'lar (renk, tip, boşluk, motion, yarıçap, gölge), foundation belgeleri, component kontratları, dark-mode eşleşmeleri, theming katmanı.
- **Görevlendiren:** `/ux-system`, sistem yokken `/ux-design --component`.
- **Girdiler:** Brand brief'i + `.ux/last-recommendation.json` (stil + palet + tipografik çift + motion preset'leri).
- **Çıktılar:** Aşağı agent'ların temelleri yeniden karara bağlamadan inşa edebileceği tutarlı, görüş sahibi, production-ready bir sistem. Token JSON, foundation MD, component kontratları, dark-mode mapping.
- **Araçlar:** `Read, Write, Edit, Bash, Glob, Grep`.

### Sub-agent görevlendirme protokolü

Bir komut bir sub-agent'ı görevlendirdiğinde, şunları geçirir:

1. Brief / öneri (`.ux/`'den yüklenir).
2. İlgili manifest dilimi (örn. `frontend-engineer` seçilen stil + palet + component'leri alır; `motion-engineer` seçilen motion preset'lerini alır).
3. 171 anti-pattern guardrail'ı (her zaman aktif).
4. Bir başarı kriteri (artefaktın ne yapması gerektiği).

Sub-agent'lar şunu döndürür:

1. Artefakt (kod, doküman, sistem).
2. Bir rationale bloğu (neden bu seçimler).
3. Guardrail'lara karşı bir self-check (hangi kuralları doğruladılar).

Çağıran komut sonra tamamlandığını ilan etmeden önce `/ux-lint`'i otomatik çalıştırır.

---

## 11 data manifest'i

Data katmanı beyindir. Her komut ondan okur; motor onun üzerinden merge eder; linter ona karşı tarar. Tüm dosyalar `data/` altında yaşar ve schema sürümlemesi için girişlerini `{_meta, entries}`'e sarar.

### `styles.json`: 84 design stili

| Alan | Açıklama |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, vs. |
| `sample entry` | `swiss-international`, «Grid yasa. Tipografi ağır işi yapar. Dekorasyon başarısızlıktır.» |

Kullanan: `/ux-discover`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 renk paleti

| Alan | Açıklama |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, vs. |
| `sample entry` | `claude-warm-editorial`, light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Kullanan: `/ux-discover`, `/ux-system`. Kontrast AA / AAA'da doğrulanmış. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 tipografik eşleşme

| Alan | Açıklama |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (aile + ağırlıklar + kaynak + lisans + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Tüm aileler lisans + kaynak URL'sine sahip. Kullanan: `/ux-discover`, `/ux-system`.

### `components.json`: 148 component

| Alan | Açıklama |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, 6 parçalı anatomi, 4 durum |

Bu en büyük hendeğimiz. Başka hiçbir Claude UX plugin'i yapılandırılmış component manifest'i dağıtmıyor.

### `industries.json`: 184 sektör kuralı

| Alan | Açıklama |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, vs. |
| `sample entry` | `fintech-neobank`, yüksek güven, regülasyon disclosure'ları, bakiye/işlem birincil UI, mobile-first günlük kullanım |

Recommender (`/ux-discover`) tarafından ilk paralel arama ekseni olarak kullanılır.

### `chart-types.json`: 35 chart tipi

| Alan | Açıklama |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, 4 ile 15 arasında ayrık kategoriyi karşılaştırır. x ekseni boyunca konum kategoriyi, yükseklik değeri gösterir. |

`/ux-design --dashboard` ve `/ux-design --component` (grafik örnekleri) tarafından kullanılır.

### `tech-stacks.json`: 25 stack

| Alan | Açıklama |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css ile uyumlu |

Diğer stack'ler arasında Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025 var.

### `ux-guidelines.json`: 112 isimli UX yasası

| Alan | Açıklama |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, vs. |
| `sample entry` | `hicks-law`, Karar süresi sunulan seçim sayısıyla logaritmik olarak büyür |

`/ux-audit` (6 lensli puanlama) ve `/ux-critique` (taste çapası) tarafından kullanılır.

### `motion-presets.json`: 57 motion preset'i

| Alan | Açıklama |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (reduced-motion fallback), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Her preset'in bir reduced-motion varyantı var. Framer Motion, GSAP ve saf CSS için stack-ready kod.

### `anti-patterns.json`: 171 kural

| Alan | Açıklama |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (tür, desen, bayraklar, kapsam ve birçok kural için ayrıştırılmış dosya üzerinde bir `post` kontrolü), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

Kuralların tam listesi [171 anti-AI-slop kuralı](#171-anti-ai-slop-kuralı-linter) bölümünde.

### `brands/*.json`: 160 brand specs'i

| Alan | Açıklama |
|---|---|
| `entries` | 160 (artı tümünü listeleyen `_index.json`) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Tam liste [160 brand DESIGN.md spec'i](#160-brand-designmd-speci-kategoriye-göre)'nde.

---

## 171 anti-AI-slop kuralı: linter

ux-skill deterministik bir linter ile gelir: her kural bir desendir ve birçoğu ayrıştırılmış CSS ve markup üzerinde ek bir kontrol yapar; böylece bir eşleşme yalnızca kuralın belirttiği bağlamda sayılır. **LLM yok.** **API yok.** **Ağ yok.** Tipik bir Next.js uygulamasında CI'da ~200ms'de çalışır. `--fail-on high` ayarlandığında Critical / High bulgularda non-zero ile çıkar.

Kurallar `data/anti-patterns.json` (v2, tercih edilen) kaynağından, `references/foundations/anti-patterns.md` yedeğiyle (v1, bash) gelir. İki binary dağıtılır: `bin/ux-lint.py` (Python, hızlı, genişletilebilir) ve `bin/ux-lint.sh` (Bash + perl-PCRE, Python olmayan ortamlar için).

### Kategoriye göre kurallar

171 kuralın tamamını önce kategoriye, sonra önem derecesine göre listeleyen katalog, `data/anti-patterns.json` dosyasından [İngilizce README](README.md#rules-by-category) içine üretilir; kural kimlikleri ve adları orada linter'ın yazdırdığı haliyle yer alır. Kurallar A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) kapsar.

### Linter kullanımı

**Tek seferlik tarama:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 brand DESIGN.md spec'i: kategoriye göre

Gerçek brand'ler. Gerçek design dilleri. Gerçek DESIGN.md spec'leri, genel paletler değil. Plugin'e «Stripe'ın stilinde bir landing kur» de, ve gerçek brand sözlüğünü okur: ses rubriği, renk token'ları, motion konvansiyonları, imza hamleleri, anti-hamleleri.

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

Diğer 8 popüler Claude UX plugin'i «modern minimal» veya «clean dashboard» üretir, aynı varsayılan estetiğin varyantları. ux-skill **Linear'ın netliği**, **Stripe'ın ciddiyeti**, **Apple'ın ölçülülüğü**, **Tesla'nın monoliti**, **Notion'un samimiyeti**, **Cursor'ın gradient disiplini**, **Raycast'in hairline yoğunluğu**, **Claude'un sıcak editorial'ı** istemene izin verir, ve motor doğru token'ları, sesi, motion konvansiyonlarını ve imza hamlelerini brand spec'inden çeker.

---

## MCP sunucusu: asimetrik hamle

ux-skill bir **Model Context Protocol sunucusu** dağıtır. `ux-mcp`'yi çalıştır; motor, MCP destekli herhangi bir host'un (Claude Desktop, Cursor, Windsurf, genel agent'lar) çağırabileceği uzun ömürlü bir stdio süreci olur. 25 araç: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Slash komutlarının kullandığı aynı Python handler'ları; aynı veri manifest'leri; aynı deterministik recommender.

**Bu neden asimetrik hamle:** top sekiz Claude UX skill'inin hiçbiri (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) MCP sunucusu dağıtmaz. Claude Code'un plugin runtime'ı içinde kilitliler. ux-skill, Claude Code plugin'ini hiç duymamış agent'lar dahil MCP konuşan herhangi bir host'tan ulaşılabilir.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Client'ını `ux-mcp` binary'sine yönelt. Claude Desktop, Cursor ve Windsurf için tam araç dokümanları, JSON örnekleri ve client başına config [docs/mcp.html](docs/mcp.html)'de ve `commands/ux-mcp.md`'de yaşar.

---

## 17 IDE yükleyicisi

`uxskill init` (veya Claude Code içinde `/ux-init`) hangi IDE'yi kullandığını otomatik algılar ve doğru artefaktı yazar. Aynı Python motor. Aynı öneriler. IDE başına farklı yapıştırıcı.

| IDE / Araç | Tespit sinyali | Kurulan artefakt |
|---|---|---|
| Claude Code | `.claude/` veya `CLAUDE.md` | `.claude-plugin/plugin.json` konumunda plugin manifest'i + 18 komutun tamamı (ve 7 takma ad) + 5 sub-agent'ın tamamı |
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

## Kullanım senaryoları: somut senaryolar

Sekiz gerçek senaryo. Durumuna en yakın olanı seç ve çağırmayı uyarla.

### 1. Cursor'da bir fintech dashboard'u inşa etme

Cursor'da bir MENA neobank dashboard'u üzerinde çalışıyorsun. Plugin'i kurarsın ve discovery, öneri, ardından dashboard üretimi çalıştırırsın.

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

Sonra Cursor'da sor: *«.ux/last-recommendation.json'daki öneriyi kullanarak dashboard yüzeyini üret»*. Cursor `.cursorrules` header'ını okur, öneriyi yükler, açık kısıtlamalarla bir dashboard üretimini görevlendirir.

### 2. Claude Code'da Stripe stili bir landing üretme

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Üç komut, bir parlatılmış yüzey, fix başına atomik commit'ler.

### 5. Linear stili bir command palette tasarlama

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

Üretilen component Linear'ın gerçek renk token'larını, tip stack'ini, motion konvansiyonlarını, hairline yoğunluklarını kullanır, «generic dark UI» değil.

### 6. Stakeholder'larla 90 dakikalık bir design thinking workshop'u yürütme

90 dakika için 5 kişilik bir odan var. Bir vibe ile değil, bir game plan ile çıkmalarını istiyorsun.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Plugin beş fazı (keşif → heat map → stakeholder haritası → çözüm eskizi → game plan) uçtan uca, zaman kutulu, faz başına somut artefaktlarla kolaylaştırır. Çıktı `.ux/last-workshop.json`, game plan, sadece «ilginç bulgular» değil.

### 7. Lansman sonrası yayınlanabilir bir case study yazma

Loyalty wallet'i ship ettin. Bir portfolio parçası istiyorsun.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

Case study tamamlanmış, yayınlanabilir bir artefakt, taslak değil. Saf monokrom, editorial tipografi, portfolio'na ship'lemeye hazır.

### 8. AI olmayan bağlamda discovery çalıştırma (sadece yapılandırılmış intake)

Bir projeyi scope'luyorsun. Henüz bir öneri lazım değil, yapılandırılmış bir brief lazım.

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

JSON'u takımına verebilir, bir Notion belgesine yapıştırabilir veya ayrı bir AI aracına besleyebilirsin. ux-skill bir motor olmaya ek olarak yapılandırılmış bir intake aracı da.

### 9. MASTER.md persistence: design kararların, repo'da

`/ux-discover` (ya da `/ux-discover --recommend`) sonrasında, seçilen stil + palet + tipografi + motion + component'ler + örnek markalar + guardrail'ları takımının inceleyebileceği, diff alabileceği ve sürüm kontrolüne koyabileceği okunaklı bir Markdown dosyası olarak kaydet.

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md` (YAML frontmatter + body) ve `persist save-page` aracılığıyla üretilen yüzey başına `.ux/design-system/pages/<name>.md` yazar. Idempotent, aynı girdi byte-identical çıktı üretir, böylece değişmemiş state üzerinde yeniden çalıştırma git'te no-op'tur.

---

## Alternatiflerle karşılaştırma

Kısa özet tablosu. Tam tablo bazlı karşılaştırma [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)'de.

| Boyut | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash komutları | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Component'ler | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Motion preset'leri | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand spec'leri | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Anti-pattern kuralları | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-safe deterministik linter | **evet** | hayır | hayır | hayır | hayır | hayır | hayır | hayır | hayır |
| Desteklenen IDE'ler | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Discovery gate | **10 alan** | örtük | örtük | örtük | örtük | örtük | örtük | örtük | örtük |
| `.ux/` state zinciri | **evet** | hayır | hayır | hayır | hayır | hayır | hayır | hayır | hayır |
| Yıldızlar (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Dürüst değerlendirme

- **ui-ux-pro-max** farkındalıkta daha büyük, 18 IDE dağıtır, CSV'si üzerinde BM25 tarzı arama var. Component manifest'i, motion manifest'i, brand kütüphanesi veya deterministik linter dağıtmıyor.
- **open-design** 19 skill + preview var ama sadece Claude Code desteği ve anti-slop katmanı yok.
- **hallmark** ruhen en yakın (o da anti-slop) ama tek skill, motor yok, manifest yok, zincirli komut yok.
- **material-3-skill** spesifik olarak Material Design 3 istiyorsan mükemmel. MD3'te rekabet etmiyoruz.

Her boyut için tam detay için: [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

Sırada, belirli bir sürüme bağlı olmadan:

- **Figma stilleri**: gölgeler için efekt stilleri, grid stilleri ve alan değişkenlerine bağlı metin stilleri, canlı bir dosyaya yazılır.
- **Component eşleme**: bir Figma component'i ve varyantları, bir kod component'ine ve onun props'larına eşlenir; devir teslim boyunca korunur.
- **Canlı site içe aktarıcı**: yayındaki bir sitenin gerçekte render ettiği sistemi okumak, dosya içe aktarıcılarının yanında.
- **Kurulmuş bir sistem için doküman sayfaları**: token'larının, rollerinin ve sözleşmelerinin insan için görünümü.

Ayrıca açık olanlar:

- **Güvenli yeniden yazımlar için `uxskill lint --fix`**: mekanik olarak düzeltilebilir bulgular (button-no-type, img-no-alt boş dize, console-log-leak kaldırma).
- Lint bulgularını satır içinde gösteren **VS Code eklentisi**.
- Altı stack'te **component başına kod üretimi** (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, vanilla HTML/CSS).
- **Marka spec'i pazaryeri**: topluluk marka spec'lerini yayınla ve keşfet.
- **Özel anti-pattern kuralları**: projelerin `data/anti-patterns.local.json` içinde tanımladığı kuralları keşfetme ve paylaşma.
- **`uxskill plan`**: yalnızca tek bir yüzey değil, bir brief'ten çok sayfalı site planlaması.

---

## Katkıda bulunma

Issue ve PR'lar memnuniyetle karşılanır. Üç yüksek-kaldıraçlı alan:

### Bir anti-pattern kuralı ekle

1. `data/anti-patterns.json`'ı düzenle, `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references` ile bir giriş ekle.
2. `tests/linter/`'da bir test ekle, kuralı tetikleyen bir dosya, tetiklemeyen bir tane.
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx` çalıştır, ateş ettiğini doğrula. `tests/linter/should-not-trigger/<rule>.tsx`'te çalıştır, etmediğini doğrula.
4. Bir PR aç.

### Bir brand spec ekle

1. `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references` ile `data/brands/<slug>.json` oluştur.
2. Karşılık gelen düzyazıyı `references/brands/<slug>.md`'ye ekle.
3. `data/brands/_index.json`'a kaydet.
4. Bir PR aç. Spec birincil-kaynak referanslarla desteklenmeli (brand'in gerçek ürünü, herkese açık design sistemi veya yayımlıyorlarsa DESIGN.md).

### Bir motion preset ekle

1. `data/motion-presets.json`'ı düzenle, `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use` ile bir giriş ekle.
2. Preset'in bir reduced-motion varyantı olmalı. İstisna yok.
3. Bir PR aç.

### Süreç

- Tam süreç için [CONTRIBUTING.md](CONTRIBUTING.md)'yi oku.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)'yi oku.
- Yeni kurallar ve brand spec'leri şunlar için incelenir: birincil-kaynak tabanlanma, tek bir projeye overfit yok, hiçbir veride emoji yok, uygulanabilir yerlerde RTL-safe davranış.

---

## Lisans, yazar, teşekkürler

### Lisans

MIT. Kullan, fork'la, üstüne inşa et. Eğer seni AI slop ship etmekten kurtarırsa, repo'ya yıldız ver, bunu desteklemenin en ucuz yolu.

### Yazar

**Laith Aljunaidy**: MENA-first bir loyalty platformu olan [Dot](https://thedotwallet.com)'un solo kurucusu. AI üretilmiş frontend'in hepsi aynı görünmesin diye ux-skill'i inşa ediyor.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Site: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Teşekkürler

- Claude Code ve bunu dağıtılabilir kılan skill / plugin mimarisi için Anthropic ekibine.
- `data/ux-guidelines.json`'ı bilgilendiren çalışmaları için Nielsen Norman Group, Laws of UX (lawsofux.com) ve UX araştırma topluluğuna.
- `data/brands/`'de listelenen her brand'e, herkese açık design sistemleri brand spec'lerinin doğruluk kaynağı.
- Orijinal v1 katkıda bulunanlarına: v2 Python motoruna tohum olan tek-atışlık Claude skill'i.
- Karşılaştırdığımız 8 popüler Claude UX plugin'i, çıtayı yükselttiler; bu bizim cevabımız.

---

**ux-skill** · **v4.0.0** · Claude Code, Cursor, Windsurf ve diğer her AI coding aracının AI üretilmiş gibi okunmayan frontend çıktısı vermesi için inşa edildi.

> Repo'ya [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) adresinden yıldız ver · `pip install uxskill` veya `npx uxskill init` ile kur · Karşılaştırmaya [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) adresinden göz at
