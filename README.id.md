[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · **Bahasa Indonesia** · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — mesin design intelligence untuk Claude Code, Cursor, dan setiap tool coding AI lainnya

> **v3.1.0 stable — THE BRAIN.** Plugin UX terkuat untuk coding AI. Inti reasoning Python dengan 12 manifest JSON yang bisa di-query (84 style, 176 palette, 70 pasangan tipografi, 148 komponen, 184 industri, 35 tipe chart, 57 preset motion, 112 hukum UX, 152 aturan anti-pattern, 25 tech stack, 160 spec brand), 25 slash command, 5 sub-agent, dan linter deterministik anti-AI-slop. Lintas IDE: tersedia di Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer, dan Roo Cline.

> **Nama brand-nya adalah `ux-skill`.** Nama paket PyPI / npm tetap `uxskill`. Repo GitHub ada di [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Situs:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Bandingkan dengan setiap plugin UX Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.1.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#installer-17-ide)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-223_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Apa yang baru di v3

- **Brand specs jadi data pelatihan, bukan template.** 160 brand specs tidak lagi katalog yang diambil recommender — melainkan kosakata yang disuling synthesizer. Output baru di setiap panggilan.
- **Synthesizer 7-sumbu** (warmth, contrast, density, geometry, formality, motion, type_personality). Brief dipetakan secara deterministik ke nilai sumbu; nilai sumbu dikompilasi ke palette + tipografi + spacing + radius + motion segar.
- **Tiga mode auto-dispatch** — `strict_brand` (100% satu brand), `brand_anchor` (70% satu brand + 30% adaptasi sumbu dari brand saudara), `pure_synthesis` (tanpa brand disebut — destilasi 8 contoh selaras sumbu).
- **Decisions ledger me-rerank recommender.** `.ux/decisions.jsonl` me-rerank kandidat berdasar kemenangan masa lalu di bucket `(industry, ui_type)` yang sama. Cold-start aman. Hanya menghitung keputusan dengan `lint_score >= 80` + `user_accepted = true`.
- **Matriks interaksi sumbu** — resolusi konflik eksplisit antar sumbu bersaing (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Tidak ada lagi aturan ad-hoc senyap.
- **Loop otomatis `/ux-evolve`** — lint → polish → re-lint hingga skor ≥ 90, plateau, atau 5 putaran. Quality gate di 65.
- **3 tool MCP baru** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Dashboard stats lokal** — `uxskill stats --html` menulis `.ux/stats.html` yang menunjukkan apa yang dipelajari instalasi **kamu**. Tanpa telemetri, tanpa agregasi global.
- **223 tes lolos.** Offline. Deterministik. LLM tak pernah dipanggil.

Detail lengkap di [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Riwayat star

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Apa itu ux-skill

ux-skill adalah **mesin design intelligence** untuk tool coding AI. Berjalan sebagai paket Python (`pip install uxskill`), sebagai plugin Claude Code, dan sebagai multi-installer 17 IDE. Mesinnya menerima brief proyek (industri, audiens, tone, must-have, hal yang dilarang, stack, region) dan mengembalikan sistem design rekomendasi lengkap: style, palette, pasangan tipografi, preset motion, komponen, brand teladan untuk dipelajari, dan guardrail anti-pattern yang harus dipertahankan. Rekomendasinya deterministik — input yang sama selalu menghasilkan output yang sama.

Plugin ini duduk di antara kamu dan tool coding AI. Ketika kamu meminta Claude Code, Cursor, atau asisten AI lainnya untuk "buat landing page fintech," asisten biasanya berimprovisasi — dan hasilnya terbaca sebagai buatan AI dalam lima detik (gradien ungu-ke-biru, tiga card sama besar, Inter di ukuran display, "John Doe" di testimonial, transisi default 300ms, hero centered, panah CTA yang bouncing). ux-skill mengganti improvisasi dengan **batasan terstruktur**: kamu jalankan `/ux-discover` untuk menangkap brief, `/ux-recommend` untuk memilih sistem, `/ux-design` untuk menghasilkan code, dan `/ux-lint` untuk memverifikasi bahwa hasilnya lolos 152 aturan deterministik anti-AI-slop sebelum commit.

README ini adalah referensi kanonis. Setiap command, setiap sub-agent, setiap data manifest, setiap path install, setiap brand spec, setiap kategori anti-pattern — semuanya didokumentasikan di sini. Jika kamu sedang mencari plugin design untuk Claude Code atau membandingkan tool design AI untuk Cursor, Windsurf, atau Codex, baca ini dari atas ke bawah bersama [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Daftar isi

1. [Otak — apa itu v3.0](#otak--apa-itu-v30)
2. [Install cepat](#install-cepat)
3. [Angka — perbandingan live dengan 8 skill UX Claude teratas](#angka--perbandingan-live-dengan-8-skill-ux-claude-teratas)
4. [Arsitektur — bagaimana semuanya cocok](#arsitektur--bagaimana-semuanya-cocok)
5. [25 slash command — referensi detail](#22-slash-command--referensi-detail)
6. [5 sub-agent](#5-sub-agent)
7. [12 data manifest](#11-data-manifest)
8. [152 aturan anti-AI-slop — linter](#145-aturan-anti-ai-slop--linter)
9. [160 spec brand DESIGN.md — per kategori](#160-spec-brand-designmd--per-kategori)
10. [Server MCP — langkah asimetris](#server-mcp--langkah-asimetris)
11. [Installer 17 IDE](#installer-17-ide)
12. [Use case — skenario konkret](#use-case--skenario-konkret)
13. [Dibandingkan dengan alternatif](#dibandingkan-dengan-alternatif)
14. [Roadmap](#roadmap)
15. [Kontribusi](#kontribusi)
16. [Lisensi, penulis, ucapan terima kasih](#lisensi-penulis-ucapan-terima-kasih)

---

## Otak — apa itu v3.0

v3.1.0 adalah pergeseran arsitektur terbesar dalam sejarah ux-skill. Recommender tidak lagi mengambil template dari katalog — engine **mensintesis** bahasa desain segar per brief. Brief yang sama selalu menghasilkan output yang sama (sepenuhnya deterministik), tetapi setiap brief berbeda mendapat sistem barunya sendiri. Brand specs bukan lagi template; mereka adalah data pelatihan tempat engine belajar kosakata. Sistem memiliki mata pada sejarahnya sendiri, menutup loop umpan balik secara lokal, dan tidak pernah memanggil LLM.

Compiler adalah **synthesizer deterministik 7-sumbu** — warmth, contrast, density, geometry, formality, motion, type_personality. Setiap brief dipetakan ke nilai sumbu; nilai sumbu dikompilasi ke palette + tipografi + spacing + radius + motion segar. Skala tipografi modular memilih rasio dari contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Primitif layout responsif sejak dirancang (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Layout rusak tak bisa dipancarkan karena tak bisa direpresentasikan.

Ada tiga mode auto-dispatch: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% token Stripe, jalur tercepat); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% adaptasi sumbu dari 4 brand saudara); dan `pure_synthesis` (tanpa brand disebut → ruang tak terbatas, 8 contoh selaras sumbu disuling jadi bahasa desain baru). Konflik antar sumbu diselesaikan oleh **matriks interaksi sumbu** terdokumentasi — dense + corporate kompilasi ke 4px (density menang, mazhab Bloomberg), airy + corporate ke 12px (formality menang, mewah), soft + playful ke 18px radius, sharp + corporate ke 2px. Tak ada aturan ad-hoc senyap dalam implementasi.

**Decisions ledger** (`.ux/decisions.jsonl`, schema `_v: 1` terkunci) menutup loop umpan balik. Recommender kini me-rerank kandidat berdasar kemenangan masa lalu di bucket `(industry, ui_type)` yang sama. Cold-start aman — melewati di bawah 3 priors. Hanya menghitung keputusan dengan `lint_score >= 80` DAN `user_accepted = true`. Selain itu `/ux-evolve` menjalankan lint → polish → re-lint hingga skor ≥ 90, plateau, atau 5 putaran, dengan quality gate di 65 yang menolak output di bawahnya tanpa `--force`. Hasilnya: tiap instalasi makin pintar di corpus-nya sendiri, tiap run reproducible antar mesin, dan engine tetap sepenuhnya offline.

---

## Install cepat

Tiga jalur install. Pilih yang cocok dengan environment kamu.

### Jalur 1 — marketplace Claude Code (kanonis)

Kalau kamu hidup di Claude Code, install via marketplace plugin:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Itu menghubungkan semua 25 slash command dan 5 sub-agent ke sesi Claude Code kamu. Setelah install, jalankan `/ux-init` untuk setup direktori state `.ux/` per proyek dan verifikasi bahwa engine Python bisa dijangkau.

### Jalur 2 — pip (universal)

Kalau kamu hidup di luar Claude Code (Cursor, Windsurf, CLI, CI), install paket Python:

```bash
pip install uxskill
uxskill init                       # mendeteksi IDE kamu otomatis, install artifact yang tepat
uxskill stats                      # cetak hitungan manifest untuk verifikasi install
uxskill lint .                     # jalankan linter terhadap direktori saat ini
```

Paket ini meng-expose `ux` dan `uxskill` sebagai entry point CLI — keduanya binary yang sama.

### Jalur 3 — npx (tidak perlu Python)

Kalau kamu tidak mau mengelola Python langsung, wrapper npx melakukan bootstrap segalanya via `pipx`:

```bash
npx uxskill init                  # download pipx + uxskill pada eksekusi pertama
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verifikasi install

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

Kalau ada hitungan yang mengembalikan 0, file JSON-nya hilang — buka issue di [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Angka — perbandingan live dengan 8 skill UX Claude teratas

Hitungan star terakhir diverifikasi via `gh api` pada **2026-05-28**. ux-skill (Laith0003/ux-skill) adalah pendatang baru — kami kecil di awareness, dalam di arsitektur. Perbandingan di bawah ini jujur: di mana kami kalah, di mana kami menang.

| Plugin | Star | Arsitektur | Slash command | Linter (CI-safe) | Brand spec | Komponen | Preset motion | IDE didukung |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, skill tunggal | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + taste berbasis riset | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | SKILL.md tunggal 62 KB + script | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Library skill terhubung MCP | multi | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill satu-estetika | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill design anti-slop | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Komponen MD3 + audit | 1 | — | (MD3 saja) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Engine Python + 12 manifest + 25 command + 5 sub-agent + CI linter** | **22** | **152 aturan regex** | **160** | **148** | **57** | **17** |

### Di mana kami kalah

- **Awareness.** Mereka punya ratusan ribu star. Kami punya 14. Beri kami star — itu cara termurah untuk membantu.
- **Pengenalan brand.** ui-ux-pro-max dan open-design punya keunggulan terdepan yang diukur dalam bulan, bukan hari.
- **Polesan marketing.** Mereka punya screenshot, video demo, dan landing page yang bisa ditemukan. Kami punya README yang lengkap dan landing yang tipis.

### Di mana kami menang

- **Library komponen:** 148 komponen yang didokumentasikan dengan anatomi, state, token yang dipakai, dan spec motion. Tidak ada dari 8 yang lain mengirim manifest komponen.
- **Preset motion:** 57 entri siap-stack (Framer Motion, GSAP, CSS) dengan fallback reduced-motion. Tidak ada dari yang lain mengirim manifest motion.
- **Linter anti-pattern:** 152 aturan regex deterministik, berjalan di CI, exit non-zero pada Critical/High. Tidak ada dari yang lain mengirim linter deterministik.
- **Brand spec:** 160 spec DESIGN.md asli (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude, dan 96 lainnya). Tidak ada dari yang lain mengirim library brand.
- **17 IDE didukung:** engine yang sama, perekat berbeda per IDE.
- **25 slash command:** discovery, generation, audit, lint, polish, fix loop, case-study, workshop, copy, motion, a11y, dashboard, conductor — terintegrasi sepenuhnya.

Tabel side-by-side lengkap per tabel ada di [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Arsitektur — bagaimana semuanya cocok

```
ux-skill (nama paket: uxskill)
│
├── data/                              Otaknya — manifest JSON yang bisa di-query
│   ├── styles.json                    84 style design + when/skip + token
│   ├── palettes.json                  176 palette (light/dark, kontras terverifikasi)
│   ├── type-pairs.json                70 triplet display × body × mono
│   ├── components.json                148 komponen (anatomi, state, motion)
│   ├── industries.json                184 aturan industri + sinyal audiens
│   ├── chart-types.json               35 tipe chart (when/skip, encoding)
│   ├── tech-stacks.json               25 stack (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 hukum UX bernama (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 preset motion (entry, exit, hover...)
│   ├── anti-patterns.json             152 aturan regex (sumber linter CI-safe)
│   └── brands/*.json                  160 spec DESIGN brand + _index.json
│
├── engine/                            Python — penalarannya
│   ├── synthesizer/                   v3 — compiler deterministik 7-sumbu
│   ├── decisions/                     v3 — ledger .ux/decisions.jsonl + re-rank recommender
│   ├── recommender/                   engine merge 5-pencarian-paralel
│   ├── linter/                        scanner anti-slop deterministik
│   ├── discovery/                     protokol pemaksa 10-field
│   ├── generator/                     emitter token + manifest
│   ├── installer/                     multi-installer 17 IDE
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          25 slash command Claude Code (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    snapshot inventaris
│   ├── ux-discover.md                 intake 10-field (gate)
│   ├── ux-recommend.md                FLAGSHIP — 5 pencarian paralel
│   ├── ux-lint.md                     linter deterministik
│   ├── ux-design.md                   generate code frontend
│   ├── ux-component.md                generate satu komponen
│   ├── ux-system.md                   generate sistem design lengkap
│   ├── ux-dashboard.md                generate permukaan dashboard
│   ├── ux-motion.md                   treatment motion + audit
│   ├── ux-audit.md                    audit design 6-lensa
│   ├── ux-a11y.md                     audit WCAG 2.1 AA
│   ├── ux-critique.md                 critique selera (3 menang, 3 meleset, 1 langkah)
│   ├── ux-copy.md                     review microcopy + rewrite
│   ├── ux-fix.md                      terapkan temuan sebagai commit atomik
│   ├── ux-polish.md                   pass kosmetik + bunuh AI-slop
│   ├── ux-frame.md                    blok framing 4-field
│   ├── ux-research.md                 perencanaan riset + sintesis
│   ├── ux-workshop.md                 workshop design thinking 5-fase
│   ├── ux-case-study.md               case study editorial Wfrah yang bisa dipublikasi
│   ├── ux-next.md                     conductor workflow (read-only)
│   └── ux-expert.md                   hook konsultasi
│
├── agents/                            5 sub-agent (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy dengan suara brand
│   ├── research-synthesizer.md        wawancara + analitik + kompetitor
│   └── design-system-architect.md     token / komponen / foundation
│
├── references/                        Sumber prosa untuk data + halaman demo
│   ├── foundations/                   anti-patterns.md, prinsip, taste
│   ├── laws/                          hukum UX panjang
│   ├── process/                       discovery-protocol.md (load-bearing)
│   ├── styles/                        prosa per-style (anti-slop.md, dll)
│   ├── components/                    komponen panjang
│   ├── output/                        rubrik output
│   └── conditional/                   panduan spesifik-stack
│
├── bin/
│   ├── uxskill.mjs                    wrapper npx -> engine Python
│   ├── ux-lint.py                     linter v2 (preferensi)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (dibuat per proyek)
    ├── last-discovery.json            snapshot brief
    ├── last-recommendation.json       sistem yang dipilih
    ├── last-frame.json                blok framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Bagaimana engine sebenarnya bekerja

1. **Input.** Kamu memberikan brief — secara interaktif via `/ux-discover` (10 field) atau non-interaktif via flag ke `ux recommend`.
2. **5 pencarian paralel.** Engine menjalankan lima lookup secara konkuren ke seluruh manifest:
   - **Industri → recommended_styles** (industries.json)
   - **Style → kompatibilitas palette + tipografi + motion** (styles.json)
   - **Tone × must-have → filter palette** (palettes.json)
   - **Stack → kompatibilitas komponen + preset motion** (tech-stacks.json, motion-presets.json)
   - **Forbidden + region → guardrail + shortlist brand teladan** (anti-patterns.json, brands/)
3. **Merge.** Merger deterministik me-rangking kandidat, menyelesaikan konflik (mis. must-have dark-mode memaksa mode palette), dan menghasilkan satu sistem rekomendasi.
4. **Output.** Dokumen JSON dengan style yang dipilih, palette, pasangan tipografi, top 5 preset motion, top 12 komponen, top 5 brand teladan, dan semua 152 guardrail anti-pattern aktif. Plus blok rasional yang menjelaskan setiap pilihan.
5. **Generasi.** Command hilir (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) mengonsumsi rekomendasi untuk menghasilkan code aktual via sub-agent.
6. **Verifikasi.** `/ux-lint` me-rescan code yang dihasilkan terhadap 152 aturan regex. Exit non-zero pada Critical/High di CI.

**Python berpikir. HTML menampilkan. Markdown merantai.**

---

## 25 slash command — referensi detail

Setiap command dikirim sebagai file `.md` di bawah `commands/` dengan `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process`, dan `output state file`. Deskripsi di bawah dipadatkan; source lengkap adalah spec kanonis.

Command dikelompokkan ke dalam lima ember: **bootstrap & inventaris**, **discovery & rekomendasi**, **generasi**, **audit & verifikasi**, **fix & polish**, dan **conductor**.

### Bootstrap & inventaris

#### `/ux-init` — bootstrap proyek

- **Apa:** Mendeteksi IDE mana yang kamu pakai (`.claude/`, `.cursor/`, `.windsurf/`, dll), install artifact yang tepat, verifikasi engine Python bisa dijangkau, cetak snapshot stats.
- **Kapan dipakai:** Install pertama kali di proyek baru. Setelah meng-clone proyek yang pakai ux-skill. Setelah `pip install --upgrade uxskill`.
- **Kapan dilewati:** Kamu sudah jalankan di proyek ini dan tidak ada yang berubah.
- **Pemanggilan:** `/ux-init` (tanpa argumen) atau `uxskill init` dari CLI.
- **Output:** Artifact per IDE (lihat [Installer 17 IDE](#installer-17-ide)) + direktori `.ux/` + ringkasan stdout.
- **Merantai ke:** `/ux-discover` berikutnya.

#### `/ux-stats` — cetak inventaris data

- **Apa:** Mencetak versi + hitungan entri untuk 12 data manifest, jadi kamu bisa verifikasi apa yang terinstall.
- **Kapan dipakai:** Setelah install. Setelah upgrade. Saat `/ux-recommend` mengembalikan pilihan yang mengejutkan dan kamu curiga manifest tidak lengkap.
- **Kapan dilewati:** Tidak pernah — ini command read-only 50ms.
- **Pemanggilan:** `/ux-stats` atau `uxskill stats`.
- **Output:** JSON ke stdout (lihat [Verifikasi install](#verifikasi-install) di atas).
- **Merantai ke:** Hanya diagnostik; tidak memberi makan hilir.

### Discovery & rekomendasi

#### `/ux-discover` — fungsi pemaksa (intake 10-field)

- **Apa:** Intake wajib 10-field yang dilewati setiap proyek sebelum command generasi apa pun. Tipe proyek, audiens, tujuan utama, tone, must-have, forbidden, brand referensi, stack, region, metrik sukses. **Tidak ada improvisasi.** Frasa terlarang ("modern", "clean") memaksa user untuk spesifik.
- **Kapan dipakai:** Sebelum `/ux-design`, `/ux-component`, `/ux-system`, atau `/ux-dashboard` apa pun. Kapan pun brief sebelumnya sudah basi.
- **Kapan dilewati:** Kamu sedang memperbaiki bug (`/ux-fix`). Kamu hanya menjalankan pass linter (`/ux-lint`). Brief tidak berubah dari sesi terakhir.
- **Pemanggilan:** `/ux-discover`. Plugin bertanya; kamu menjawab.
- **Output:** Menulis `.ux/last-discovery.json` (brief 10-field).
- **Merantai ke:** `/ux-recommend` → memakai discovery untuk memilih style + palette + tipografi + motion + komponen. `/ux-design [brief tambahan]` → menghasilkan code frontend berdasar rekomendasi. `/ux-component <nama>` → menghasilkan satu komponen sesuai batasan yang ditemukan.

#### `/ux-recommend` — engine flagship 5-pencarian-paralel

- **Apa:** Menjalankan 5-pencarian-paralel engine Python di 12 manifest dan mengembalikan satu sistem design yang sudah digabungkan. Industri → Style → Palette → Tipografi → Motion + Komponen + Brand teladan + Guardrail.
- **Kapan dipakai:** Memulai proyek baru dari nol. Mem-pivot produk yang terlihat lelah. Pre-flight sebelum `/ux-design` atau `/ux-component` apa pun.
- **Kapan dilewati:** Kamu sudah jalankan `/ux-discover` dan simpan brief — `/ux-recommend` otomatis di alur itu. Kamu sedang memperbaiki satu bug (pakai `/ux-fix`). Kamu hanya perlu lint (pakai `/ux-lint`).
- **Pemanggilan (Claude Code):**
  ```
  /ux-recommend
  ```
  **Pemanggilan (CLI):**
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
- **Output:** Menulis `.ux/last-recommendation.json` — style terpilih, palette terpilih, pasangan tipografi terpilih, top 5 preset motion, top 12 komponen, top 5 brand teladan, semua 152 guardrail anti-pattern aktif, plus rasional.
- **Merantai ke:** `/ux-design [brief]` → code frontend memakai token yang direkomendasikan. `/ux-system` → sistem design lengkap dari rekomendasi. `/ux-component <nama>` → satu komponen memakai style yang direkomendasikan. `/ux-lint` → verifikasi code yang dihasilkan.

### Generasi

#### `/ux-design` — hasilkan permukaan yang indah dan anti-slop dari brief

- **Apa:** Menghasilkan artifact frontend lengkap, kelas produksi (landing, situs marketing, app shell) dari brief discovery + rekomendasi. Mengirim `frontend-engineer` dengan arah kreatif dari anti-slop dan referensi arsenal.
- **Kapan dipakai:** "Design sebuah", "buatin gue", "generate landing page", "buat dashboard", "bikin komponen" — permintaan deliverable visual bebas-bentuk apa pun.
- **Kapan dilewati:** Kamu mau review, bukan build (pakai `/ux-audit` atau `/ux-critique`). Kamu mau satu komponen saja (pakai `/ux-component`). Pekerjaan backend atau infrastruktur.
- **Pemanggilan:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Output:** Code yang dihasilkan (HTML / Blade / JSX / Vue / Astro), plus `.ux/last-design.json`.
- **Merantai ke:** `/ux-lint` → verifikasi terhadap guardrail. `/ux-polish` → pass kosmetik. `/ux-a11y` → audit aksesibilitas. `/ux-copy` → review microcopy. `/ux-fix` → terapkan temuan sebagai commit atomik.

#### `/ux-component` — hasilkan satu komponen

- **Apa:** Memproduksi satu komponen kelas produksi (button, modal, navbar, sidebar, card, table, form, chart) dari sebuah spec. Semua empat state interaksi, accessible, sesuai brand. Mencari komponen di `.ux/last-recommendation.json` dulu, jatuh kembali ke query manifest langsung.
- **Kapan dipakai:** Permintaan elemen tunggal apa pun — "buat button", "buat pricing card", "bikin modal", "tambahin navbar", "design sidebar", "gue butuh data table", "buat form", "bikin komponen chart".
- **Kapan dilewati:** Halaman penuh atau permukaan multi-section (pakai `/ux-design`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Output:** Code komponen yang dihasilkan, plus `.ux/last-component.json`.
- **Merantai ke:** `/ux-lint` → verifikasi. `/ux-polish` → kencangkan.

#### `/ux-system` — hasilkan sistem design starter lengkap

- **Apa:** Mengusulkan sistem design starter lengkap untuk proyek yang belum punya — token (warna, tipografi, spasi, motion, radius, shadow), dokumen foundation, kontrak komponen, pasangan dark-mode, theme switcher. Mengirim `design-system-architect`.
- **Kapan dipakai:** "Kami nggak punya sistem design", "bikinin sistem", "usulkan token", "tema kita harusnya kayak apa", "setup DS kita".
- **Kapan dilewati:** Proyek sudah punya sistem design — pakai `/ux-component` terhadap sistem yang ada. Backend atau infrastruktur.
- **Pemanggilan:** `/ux-system` (jalankan discovery dulu kalau belum ada).
- **Output:** `tokens.json`, `foundations.md`, kontrak `components/*.md`, emit Tailwind / vanilla / SCSS opsional. Menulis `.ux/last-system.json` untuk konteks rantai.
- **Merantai ke:** `/ux-component` → bangun terhadap sistem baru. `/ux-design` → hasilkan permukaan memakai token baru.

#### `/ux-dashboard` — generasi dashboard terspesialisasi

- **Apa:** Dashboard dengan disiplin densitas data — layout bento, numeral monospace tabular, pola sparkline, anti-overuse card, warna state semantik, motion yang hemat. Bukan situs marketing dengan chart ditempel.
- **Kapan dipakai:** "Bangun dashboard", "design panel admin", "bikin halaman metrik", "konsol operator", "view analitik", "papan KPI", "layar monitoring".
- **Kapan dilewati:** Landing marketing dengan statistik (pakai `/ux-design`). Satu widget saja (pakai `/ux-component`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-dashboard`.
- **Output:** Code dashboard yang dihasilkan + `.ux/last-dashboard.json`.
- **Merantai ke:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — treatment motion

- **Apa:** Menghasilkan lapisan motion dari sebuah permukaan — durasi, easing, koreografi, fallback reduced-motion, disiplin performa. Juga meng-audit motion yang ada terhadap 5 dimensi (timing, easing, makna, reduced-motion, performa).
- **Kapan dipakai:** "Cek motion", "animasinya bagus nggak", "fix motion-nya", "review animasi", "audit motion", "pass performa di motion".
- **Kapan dilewati:** Permukaan tidak punya motion (pakai `/ux-audit` atau `/ux-polish`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-motion path/to/component.tsx` (mode audit) atau `/ux-motion --generate hero-entry` (generasi).
- **Output:** Code yang diperbarui (mode generasi) atau laporan `.ux/last-motion.json` (mode audit).
- **Merantai ke:** `/ux-fix` → terapkan temuan motion. `/ux-polish` → kencangkan.

### Audit & verifikasi

#### `/ux-lint` — linter berbasis regex deterministik (tanpa LLM, CI-safe)

- **Apa:** Menjalankan 152 aturan regex terhadap code kamu. Tidak ada panggilan LLM. Exit non-zero pada Critical / High di CI. Sumber: `data/anti-patterns.json`. Aturan mencakup A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4).
- **Kapan dipakai:** Hook pre-commit. Gate CI. Pass pertama yang cepat di codebase besar sebelum bayar biaya `/ux-audit`. Setelah `/ux-design` atau `/ux-component` untuk verifikasi generasi.
- **Kapan dilewati:** Kamu mau fix loop (linter melapor, tidak mengedit — rantai ke `/ux-polish --fix` atau `/ux-fix`). Kamu mau penilaian selera (pakai `/ux-critique`).
- **Pemanggilan (slash):** `/ux-lint src/`.
- **Pemanggilan (CLI):** `uxskill lint .` atau `python3 bin/ux-lint.py .` atau `bash bin/ux-lint.sh --ci --fail-on high`.
- **Pemanggilan (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Temuan ke stdout (lokasi, id aturan, severity, bukti). Exit code 0 kalau bersih, non-zero pada Critical/High saat `--fail-on high` di-set.
- **Merantai ke:** `/ux-polish --fix` → counterpart LLM-driven pada pola yang sama. `/ux-fix` → terapkan temuan sebagai commit, diurutkan severity. `/ux-audit` → pass penalaran 6-lensa lengkap. `/ux-next` → biarkan conductor yang putuskan.

#### `/ux-audit` — audit design 6-lensa

- **Apa:** Review terstruktur, opinionated terhadap enam lensa (kejelasan, hirarki, aksesibilitas, suara, motion, taste), menghasilkan temuan ber-tag severity. Laporan gaya Polaris. Membaca `.ux/last-frame.json` dulu — audiens dan outcome menjangkar severity setiap temuan.
- **Kapan dipakai:** Permukaan ada dan kamu mau critique yang bisa dipertahankan. "Audit", "review UX-nya", "ini bagus nggak", "apa yang rusak", "robek ini".
- **Kapan dilewati:** Permukaan belum ada (pakai `/ux-design`). User mau satu lensa (pakai command yang tertarget: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). User mau opini selera (pakai `/ux-critique`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-audit https://example.com/pricing` atau `/ux-audit src/components/Pricing.tsx`.
- **Output:** Menulis `.ux/last-audit.json` — array `findings` berisi `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Merantai ke:** `/ux-fix` → terapkan temuan. `/ux-polish` → pass kosmetik. `/ux-design` → kalau perlu redesign struktural.

#### `/ux-a11y` — audit WCAG 2.1 AA + cek sopan-santun umum

- **Apa:** Audit WCAG 2.1 AA terstruktur, plus cek sopan-santun umum yang lolos tool otomatis tapi tetap menyakiti user nyata (visibilitas focus, kespesifikan error, preferensi motion, perangkap keyboard, ketergantungan warna).
- **Kapan dipakai:** Gate aksesibilitas pre-ship. Setelah redesign. "Cek aksesibilitas", "audit WCAG", "ini accessible nggak", "review a11y", "tes screen reader", "cek navigasi keyboard".
- **Kapan dilewati:** Tidak menghadap-user. Backend atau infrastruktur. Sketsa work-in-progress.
- **Pemanggilan:** `/ux-a11y https://example.com` (URL live lebih disukai — tool otomatis dan testing keyboard hanya bekerja di live).
- **Output:** Menulis `.ux/last-a11y.json` — array `findings` berisi `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Merantai ke:** `/ux-fix` → terapkan temuan sebagai commit. `/ux-copy` → perbaiki alt text dan wiring error form sebagai bagian dari pass copy.

#### `/ux-critique` — penilaian selera (3 menang, 3 meleset, 1 langkah strategis)

- **Apa:** Opini seorang designer — bukan audit terstruktur, bukan skor severity, hanya take yang ringkas dan opinionated yang menamai apa yang bekerja, apa yang tidak, dan satu langkah strategis yang akan mengubah paling banyak.
- **Kapan dipakai:** "Menurut lo gimana", "ini bagus nggak", "kritik ini", "honest take", "vibe-nya pas nggak", "kerasa kayak kita nggak", "ini ship-able nggak".
- **Kapan dilewati:** User eksplisit mau audit terstruktur (pakai `/ux-audit`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-critique https://example.com`.
- **Output:** Menulis `.ux/last-critique.json` — 3 menang, 3 meleset, 1 langkah strategis, plus prosa.
- **Merantai ke:** `/ux-design` kalau take merekomendasikan redesign. `/ux-polish` kalau take merekomendasikan pengencangan.

#### `/ux-copy` — review microcopy + rewrite

- **Apa:** Mengevaluasi setiap string yang terlihat terhadap rubrik suara dan menghasilkan rewrite before/after. Menangkap: "form contains errors" (generik), "John Doe" (placeholder), copy AI yang ceria-perayaan, CTA generik, empty state mati, error tidak berguna.
- **Kapan dipakai:** Struktur sudah benar tapi kata-kata lemah. "Review copy-nya", "fix microcopy", "pesan error-nya jelek", "rewrite ini", "kencangin string-nya", "tombolnya kedengeran generik", "empty state-nya mati".
- **Kapan dilewati:** Masalah layout (pakai `/ux-audit` atau `/ux-polish`). Masalah copy yang digerakkan a11y seperti alt text (pakai `/ux-a11y`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Menulis `.ux/last-copy.json` — array `strings` berisi `{location, severity, before, after, notes}`, plus rubrik + locale yang butuh terjemahan.
- **Merantai ke:** `/ux-fix` → terapkan rewrite. `/ux-a11y` → cek ulang setelah fix copy.

### Fix & polish

#### `/ux-fix` — terapkan temuan sebagai commit atomik

- **Apa:** Membaca laporan terbaru dari `.ux/` (audit, copy, a11y, motion, atau polish), memvalidasi working tree, dan menerapkan temuan sebagai commit atomik via sub-agent yang tepat. Verifikasi ulang dengan menjalankan ulang command asal.
- **Kapan dipakai:** Setelah menjalankan command kelas-audit dan me-review temuan. "Fix temuannya", "terapkan fix-nya", "jalankan fix loop", "patch permukaannya", "lakukan perubahan", "fix-in dah".
- **Kapan dilewati:** Tidak ada laporan sebelumnya di `.ux/`. Working tree kotor dan user belum setuju stash/commit. Fix butuh penilaian design, bukan penerapan mekanis (pakai `/ux-design` untuk redesign).
- **Pemanggilan:** `/ux-fix` (deteksi otomatis laporan mana yang akan diperbaiki) atau `/ux-fix --from=last-a11y.json`.
- **Output:** Commit atomik per temuan. Jalankan ulang command asal dan update file `.ux/last-*.json`. Cetak ringkasan.
- **Merantai ke:** `/ux-next` → conductor memilih langkah berikutnya.

#### `/ux-polish` — pass kosmetik + bunuh AI-slop

- **Apa:** Ritme spasi, penajaman hirarki, deteksi AI-slop, konsistensi token. Counterpart LLM-driven dari `/ux-lint` — pakai penilaian kamu pada penilaian selera.
- **Kapan dipakai:** Struktur sudah benar tapi eksekusi longgar. "Polish", "kencangin ini", "hapus AI-slop", "bikin premium", "bikin nggak terlihat AI", "spasinya nggak enak", "ini terlihat generik", "butuh lebih banyak taste".
- **Kapan dilewati:** Permukaan kehilangan fungsionalitas inti (perbaiki itu dulu). Butuh redesign, bukan polish (pakai `/ux-design`). Masalah copy (pakai `/ux-copy`). Masalah motion (pakai `/ux-motion`). Masalah a11y (pakai `/ux-a11y`).
- **Pemanggilan:** `/ux-polish src/components/Hero.tsx`.
- **Output:** Code yang diperbarui + `.ux/last-polish.json` yang menjelaskan perubahan.
- **Merantai ke:** `/ux-lint` → verifikasi polish bertahan. `/ux-a11y` → cek ulang aksesibilitas.

### Discovery & narasi

#### `/ux-frame` — blok framing 4-field

- **Apa:** Menangkap untuk-siapa, outcome, hipotesis, dan sinyal sukses dalam blok framing terstruktur. Tidak ada pekerjaan design — hanya intake empat-field yang mengubah permintaan kabur jadi brief kerja. Lebih ringan dari `/ux-discover` (4 field vs 10).
- **Kapan dipakai:** Awal proyek apa pun, sprint, atau engagement satu kali. Di tengah aliran saat percakapan menyimpang. "Frame ini", "brief-nya apa", "setup proyek", "framing".
- **Kapan dilewati:** Sudah di-frame (cek `.ux/last-frame.json`). Build komponen satu-kali tanpa implikasi framing. Backend atau infrastruktur.
- **Pemanggilan:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Output:** Menulis `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Merantai ke:** `/ux-discover` → memperluas frame ke brief 10-field. `/ux-design` → hasilkan memakai frame sebagai jangkar.

#### `/ux-research` — perencanaan riset + sintesis

- **Apa:** Mode perencanaan: menulis script wawancara, survei, screener rekrutmen. Mode sintesis (`--synthesize`): mencerna wawancara, analitik, situs kompetitor, hasil A/B, tiket support jadi rekomendasi. Mengirim `research-synthesizer`.
- **Kapan dipakai:** "Rencanakan studi riset", "gue butuh pertanyaan wawancara", "design survei", "gimana cara rekrut user", "rencana user testing", "diary study", "preference test", "fake door", "smoke test", "sintesis catatan wawancara gue".
- **Kapan dilewati:** Jawaban sudah diketahui dengan keyakinan tinggi. Keputusan reversibel risiko rendah. Backend atau infrastruktur.
- **Pemanggilan:** `/ux-research --plan "loyalty wallet adoption in MENA"` atau `/ux-research --synthesize interviews/*.md`.
- **Output:** Menulis `.ux/last-research.json` — rencana riset atau tema yang disintesis + bukti + rekomendasi.
- **Merantai ke:** `/ux-frame` → integrasikan temuan ke dalam frame. `/ux-design` → hasilkan dari temuan. `/ux-workshop` → jalankan workshop memakai riset sebagai input.

#### `/ux-workshop` — workshop design thinking 5-fase

- **Apa:** Memfasilitasi workshop discovery / design-thinking end-to-end. Lima fase berurutan (eksplorasi → heat map → peta stakeholder → sketsa solusi → game plan). Diatur waktunya. Artifact konkret per fase. Berakhir dengan keputusan, bukan "temuan menarik."
- **Kapan dipakai:** Pertanyaan nyata, partisipan nyata, budget waktu nyata. "Jalankan workshop", "fasilitasi discovery", "ayo design thinking", "gue punya stakeholder satu jam, ngapain", "kick off proyek".
- **Kapan dilewati:** Brief sudah jelas dan ter-scope. Brainstorm solo (pakai `/ux-design` atau `/ux-frame`). Tim di tengah eksekusi, bukan di discovery.
- **Pemanggilan:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Menulis `.ux/last-workshop.json` — game plan + artifact per-fase.
- **Merantai ke:** `/ux-design` → eksekusi game plan. `/ux-research` → isi gap yang dimunculkan workshop. `/ux-case-study` → publikasi perjalanannya.

#### `/ux-case-study` — case study yang bisa dipublikasi (format editorial Wfrah)

- **Apa:** Menghasilkan case study proyek dalam format editorial monokromatik murni — tipografi Wfrah, pemisah hairline, kode bagian bernomor (A)–(G), layout aman-bilingual. Sebuah dokumen, bukan brosur marketing. Membaca dari `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Kapan dipakai:** Pasca-launch. Setelah milestone diskrit. "Tulis case study", "case study proyek ini", "dokumen wrap-up", "publikasi karya ini", "bahan portfolio".
- **Kapan dilewati:** Proyek kekurangan data untuk mengisi bagian (A)–(G). User mau landing marketing, bukan case study (pakai `/ux-design`).
- **Pemanggilan:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Merantai ke:** Command terminal — biasanya akhir proyek.

### Conductor

#### `/ux-next` — conductor workflow (read-only)

- **Apa:** Membaca setiap `.ux/last-*.json` dan menamai command berikutnya dengan leverage tertinggi. Seorang conductor, bukan builder. Read-only.
- **Kapan dipakai:** Antar command. "Selanjutnya ngapain", "langkah berikut apa", "tentuin buat gue", "dari sini ke mana".
- **Kapan dilewati:** Tidak ada laporan sebelumnya di `.ux/`. Kamu punya command berikutnya yang spesifik di pikiran.
- **Pemanggilan:** `/ux-next` (tanpa argumen) atau `/ux-next --focus=a11y`.
- **Output:** Stdout — command berikutnya yang direkomendasikan + rasional.
- **Merantai ke:** Apa pun yang dia pilih.

#### `/ux-expert` — hook konsultasi

- **Apa:** Memunculkan info kontak pembuat plugin saat user meminta ahli UX kehidupan nyata. Ringkas, langsung, tidak ada marketing.
- **Kapan dipakai:** "Siapa yang bikin ini", "gue butuh ahli UX", "lo nerima konsultasi", "bisa hire orang buat ini", "ada manusia di balik plugin ini".
- **Kapan dilewati:** User menanyakan fitur plugin, bukan konsultasi.
- **Pemanggilan:** `/ux-expert`.
- **Output:** Kartu kontak ringkas dengan LinkedIn / email / repo.

### Graf perantaian command

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  blok framing 4-field
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  intake 10-field (FORCING GATE)
                  └────────────┬─────────┘
                               │ menulis .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 pencarian paralel -> sistem gabungan
                  └────────────┬─────────┘
                               │ menulis .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ menulis .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ menulis .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  terapkan temuan sebagai commit
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artifact yang bisa dipublikasi
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  conductor — read-only
                  │  /ux-expert          │  hook konsultasi
                  └──────────────────────┘
```

---

## 5 sub-agent

Sub-agent adalah generator spesifik-peran yang dikirim oleh command. Mereka tidak pernah berjalan secara independen — mereka dipanggil oleh `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, dll. Setiap agent punya batas kepemilikan yang ditentukan: mereka TIDAK memutuskan brief; mereka mengeksekusi terhadapnya.

### `frontend-engineer`

- **Memiliki:** Code frontend kelas produksi (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) dengan disiplin anti-AI-slop.
- **Dikirim oleh:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Input:** Brief + arah kreatif + token (dari `.ux/last-recommendation.json`).
- **Output:** Code yang berfungsi yang bisa dibedakan dari output AI generik. Tidak ada gradien ungu, tidak ada hero centered, tidak ada tiga card sama besar, tidak ada Inter ukuran display, tidak ada "John Doe", tidak ada emoji, tidak ada default 300ms.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Memiliki:** Motion dalam code frontend produksi — Framer Motion, GSAP, animasi CSS. Durasi, easing, koreografi, fallback reduced-motion, disiplin performa.
- **Dikirim oleh:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Input:** Brief motion + token + 57 preset motion dari `data/motion-presets.json`.
- **Output:** Motion yang layak tempatnya. Selalu dibungkus dalam fallback `prefers-reduced-motion`. Selalu diuji terhadap Core Web Vitals.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Memiliki:** String yang ship — pesan error, empty state, CTA, state loading, pesan sukses, toast, teks helper, label form, teks tombol.
- **Dikirim oleh:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Input:** Profil suara (bernama atau di-paste) + string permukaan.
- **Output:** Microcopy produksi yang diterapkan secara konsisten di setiap state sebuah permukaan jadi produknya kedengaran seperti satu produk, bukan sepuluh. Larangan: "form contains errors", "John Doe", copy AI ceria-perayaan, CTA generik, empty state mati.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Memiliki:** Mencerna input riset (wawancara, analitik, situs kompetitif, hasil A/B, tiket support) jadi rekomendasi design yang bisa ditindaklanjuti.
- **Dikirim oleh:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Input:** Riset mentah — transkrip, ekspor, URL kompetitor, klaster support.
- **Output:** Tema, bukti, rekomendasi. Tidak pernah men-design jawabannya — memberi designer substrat untuk di-design dari sana.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Memiliki:** Sistem design lengkap — token (warna, tipografi, spasi, motion, radius, shadow), dokumen foundation, kontrak komponen, pasangan dark-mode, lapisan theming.
- **Dikirim oleh:** `/ux-system`, `/ux-component` saat tidak ada sistem.
- **Input:** Brief brand + `.ux/last-recommendation.json` (style + palette + pasangan tipografi + preset motion).
- **Output:** Sistem yang koheren, opinionated, dan siap-produksi yang bisa dibangun oleh agent hilir tanpa harus menentukan ulang fundamental. Token JSON, foundation MD, kontrak komponen, mapping dark-mode.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protokol pengiriman sub-agent

Saat sebuah command mengirim sub-agent, ia melewatkan:

1. Brief / rekomendasi (di-load dari `.ux/`).
2. Slice manifest yang relevan (mis. `frontend-engineer` dapat style + palette + komponen yang dipilih; `motion-engineer` dapat preset motion yang dipilih).
3. 152 guardrail anti-pattern (selalu aktif).
4. Kriteria sukses (apa yang harus dilakukan artifact).

Sub-agent mengembalikan:

1. Artifact (code, doc, sistem).
2. Blok rasional (kenapa pilihan ini).
3. Self-check terhadap guardrail (aturan mana yang mereka verifikasi).

Command pemanggil kemudian menjalankan `/ux-lint` otomatis sebelum menyatakan selesai.

---

## 12 data manifest

Lapisan data adalah otaknya. Setiap command membaca darinya; engine bergabung melintasinya; linter memindai terhadapnya. Semua file ada di bawah `data/` dan membungkus entri mereka di `{_meta, entries}` untuk versioning skema.

### `styles.json` — 84 style design

| Field | Deskripsi |
|---|---|
| `entries` | 84 |
| `key per entri` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `kategori` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, dll. |
| `contoh entri` | `swiss-international` — "Grid adalah hukum. Tipografi yang melakukan pekerjaan berat. Dekorasi adalah kegagalan." |

Dipakai oleh: `/ux-recommend`, `/ux-system`, `/ux-design`. Skema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 palette warna

| Field | Deskripsi |
|---|---|
| `entries` | 176 |
| `key per entri` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tone` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, dll. |
| `contoh entri` | `claude-warm-editorial` — light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Dipakai oleh: `/ux-recommend`, `/ux-system`. Kontras diverifikasi pada AA / AAA. Skema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 pasangan tipografi

| Field | Deskripsi |
|---|---|
| `entries` | 70 |
| `key per entri` | `id`, `name`, `display` (family + bobot + sumber + lisensi + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `contoh entri` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Semua family punya lisensi + URL sumber. Dipakai oleh `/ux-recommend`, `/ux-system`.

### `components.json` — 148 komponen

| Field | Deskripsi |
|---|---|
| `entries` | 148 |
| `key per entri` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `kategori` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `contoh entri` | `mega-nav-product-grid` — Mega Navigation, Product Grid — anatomi 6-bagian, 4 state |

Ini parit terbesar kami. Tidak ada plugin UX Claude lain yang mengirim manifest komponen terstruktur.

### `industries.json` — 184 aturan industri

| Field | Deskripsi |
|---|---|
| `entries` | 184 |
| `key per entri` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `kategori` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, dll. |
| `contoh entri` | `fintech-neobank` — trust tinggi, disclosure regulasi, UI utama balance/transaksi, mobile-first pemakaian harian |

Dipakai oleh `/ux-recommend` sebagai sumbu pencarian paralel pertama.

### `chart-types.json` — 35 tipe chart

| Field | Deskripsi |
|---|---|
| `entries` | 35 |
| `key per entri` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `kategori` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `contoh entri` | `bar-vertical` — Membandingkan 4–15 kategori diskrit. Posisi sepanjang sumbu x memetakan kategori; tinggi memetakan nilai. |

Dipakai oleh `/ux-dashboard`, `/ux-component` (instance chart).

### `tech-stacks.json` — 25 stack

| Field | Deskripsi |
|---|---|
| `entries` | 25 |
| `key per entri` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tier` | production, prerelease, experimental |
| `contoh entri` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, kompatibel dengan Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Stack lain termasuk Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 hukum UX bernama

| Field | Deskripsi |
|---|---|
| `entries` | 112 |
| `key per entri` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `kategori` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, dll. |
| `contoh entri` | `hicks-law` — Waktu keputusan tumbuh secara logaritmik dengan jumlah pilihan yang disajikan |

Dipakai oleh `/ux-audit` (scoring 6-lensa) dan `/ux-critique` (jangkar selera).

### `motion-presets.json` — 57 preset motion

| Field | Deskripsi |
|---|---|
| `entries` | 57 |
| `key per entri` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `kategori` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `contoh entri` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Setiap preset punya varian reduced-motion. Code siap-stack untuk Framer Motion, GSAP, dan CSS murni.

### `anti-patterns.json` — 152 aturan regex

| Field | Deskripsi |
|---|---|
| `entries` | 152 |
| `key per entri` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `kategori` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

Daftar aturan lengkap ada di [152 aturan anti-AI-slop](#145-aturan-anti-ai-slop--linter).

### `brands/*.json` — 160 spec brand

| Field | Deskripsi |
|---|---|
| `entries` | 160 (plus `_index.json` yang mendaftar semua) |
| `key per entri` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `kategori` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Daftar lengkap di [160 spec brand DESIGN.md](#160-spec-brand-designmd--per-kategori).

---

## 152 aturan anti-AI-slop — linter

ux-skill mengirim linter deterministik berbasis regex. **Tanpa LLM.** **Tanpa API.** **Tanpa jaringan.** Berjalan di CI dalam ~200ms pada app Next.js tipikal. Exit non-zero pada temuan Critical / High saat `--fail-on high` di-set.

Aturan bersumber dari `data/anti-patterns.json` (v2 lebih disukai) dengan fallback `references/foundations/anti-patterns.md` (v1 bash). Dua binary dikirim: `bin/ux-lint.py` (Python, cepat, dapat diperluas) dan `bin/ux-lint.sh` (Bash + perl-PCRE, untuk lingkungan tanpa Python).

### Aturan per kategori

#### Typography (3 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| high | `inter-as-display` | Inter dipakai sebagai font display |
| medium | `hero-text-arbitrary-90px` | Ukuran font hero arbitrer |
| low | `font-system-only` | Stack font sistem tanpa typeface terpilih |

#### Color (6 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| high | `purple-to-blue-gradient` | Gradien AI default ungu-ke-biru |
| high | `dark-text-on-dark-card` | Teks kontras rendah di card |
| medium | `gradient-text-rainbow` | Teks gradien multi-stop |
| medium | `card-glow-purple-shadow` | Shadow glow ungu pada card |
| medium | `gradient-mesh-purple-pink` | Hero gradien mesh ungu-pink |
| low | `tailwind-color-named-vague` | Warna Tailwind bernama tanpa token semantik |

#### Layout (5 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| high | `three-equal-card-grid` | Tiga card sama besar dalam baris |
| medium | `centered-everything-hero` | Komposisi hero yang centered |
| medium | `avatar-stack-overlapping` | Stack avatar tumpang tindih generik |
| low | `pill-rounded-full-everywhere` | `rounded-full` diterapkan ke segalanya |
| low | `nav-equal-hamburger-desktop` | Menu hamburger di desktop |

#### Content (5 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum di code yang ship |
| high | `emoji-in-ui` | Emoji dipakai sebagai elemen UI |
| high | `icon-emoji-stamp` | Emoji dipakai sebagai stamp ikon |
| high | `testimonial-fake-five-stars` | Testimonial bintang lima hardcoded |
| medium | `fake-name-john-doe` | Nama placeholder generik |

#### Motion (3 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Panah bouncing pada CTA |
| low | `timing-300ms-default` | Timing transisi default 300ms |
| low | `cubic-bezier-material-only` | Easing default Material di mana-mana |

#### A11y (6 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| high | `inline-svg-no-aria` | SVG tanpa aria-label atau aria-hidden |
| high | `img-no-alt` | Image kehilangan atribut alt |
| high | `link-onclick-no-href` | Anchor dengan onClick tapi tanpa href |
| medium | `button-no-type` | Button kehilangan atribut type |
| medium | `heading-skip-h1-h3` | Level heading dilewati |
| medium | `infinite-scroll-no-pagination` | Infinite scroll tanpa fallback keyboard |

#### Quality (6 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| high | `console-log-leak` | `console.log` di code komponen |
| medium | `inline-style-attribute` | Atribut style inline |
| medium | `any-type-leak` | Tipe `any` TypeScript |
| medium | `arbitrary-z-index-9999` | Nilai z-index malas |
| low | `shadcn-default-everywhere` | Blok token shadcn default tidak dimodifikasi |
| low | `todo-fixme-comment` | TODO atau FIXME di code yang ship |

#### Visual (1 aturan)

| Severity | ID aturan | Nama |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur tanpa permukaan glass |

### Pemakaian linter

**Scan satu kali:**

```bash
uxskill lint .
# atau
python3 bin/ux-lint.py src/
# atau
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

**Output (sampel):**

```
─── laporan /ux-lint ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  bukti: bg-gradient-to-br from-purple-500 to-blue-500
  fix: ganti dengan gradien primary palette yang direkomendasikan atau hapus gradien

src/components/Pricing.tsx:12  [high] three-equal-card-grid
  bukti: grid grid-cols-3 gap-6 (3 child Card sama besar)
  fix: fiturkan satu card; apit dengan dua card yang penekanannya dikurangi

3 file di-scan · 2 high · 0 medium · 0 low · exit 1
Direkomendasikan berikutnya: /ux-polish --fix (LLM-driven, menangani temuan lintable dan estetik)
```

---

## 160 spec brand DESIGN.md — per kategori

Brand asli. Bahasa design asli. Spec DESIGN.md asli — bukan palette generik. Bilang ke plugin "bangun landing dengan style Stripe" dan dia membaca kosakata brand yang sebenarnya: rubrik suara, token warna, konvensi motion, gerakan tanda tangan, gerakan terlarang.

Setiap brand dikirim sebagai JSON terstruktur (`data/brands/<slug>.json`) plus referensi prosa (`references/brands/<slug>.md`).

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

### Kenapa ini penting

8 plugin UX populer lain untuk Claude menghasilkan "modern minimal" atau "clean dashboard" — varian dari estetika default yang sama. ux-skill memungkinkan kamu meminta **kejelasan Linear**, **keseriusan Stripe**, **kehematan Apple**, **monolit Tesla**, **keramahan Notion**, **disiplin gradien Cursor**, **densitas hairline Raycast**, **editorial hangat Claude** — dan engine mengambil token yang tepat, suara, konvensi motion, dan gerakan tanda tangan dari spec brand.

---

## Server MCP — langkah asimetris

ux-skill mengirim **server Model Context Protocol**. Jalankan `ux-mcp` dan engine menjadi proses stdio long-running yang bisa dipanggil oleh host MCP-capable apa pun — Claude Desktop, Cursor, Windsurf, agent generik. Empat belas tool: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Handler Python yang sama yang dipakai slash command; data manifest yang sama; recommender deterministik yang sama.

**Kenapa ini langkah asimetris:** tidak ada dari delapan skill UX Claude teratas (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) yang mengirim server MCP. Mereka terkunci di dalam runtime plugin Claude Code. ux-skill bisa dijangkau dari host apa pun yang berbicara MCP, termasuk agent yang belum pernah dengar plugin Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp adalah extra opt-in
ux-mcp                                  # server stdio JSON-RPC mulai
```

Arahkan client kamu ke binary `ux-mcp`. Dokumentasi tool lengkap, contoh JSON, dan konfig per-client untuk Claude Desktop, Cursor, dan Windsurf hidup di [docs/mcp.html](docs/mcp.html) dan di `commands/ux-mcp.md`.

---

## Installer 17 IDE

`uxskill init` (atau `/ux-init` di dalam Claude Code) mendeteksi otomatis IDE mana yang kamu pakai dan menulis artifact yang tepat. Engine Python yang sama. Rekomendasi yang sama. Perekat berbeda per IDE.

| IDE / Tool | Sinyal deteksi | Artifact terinstall |
|---|---|---|
| Claude Code | `.claude/` atau `CLAUDE.md` | Manifest plugin di `.claude-plugin/plugin.json` + semua 25 command + semua 5 sub-agent |
| Cursor | `.cursor/` atau `.cursorrules` | Header prompt `.cursorrules` yang menunjuk ke engine |
| Windsurf | `.windsurf/` atau `.windsurfrules` | `.windsurfrules` dengan header prompt yang sama |
| GitHub Copilot | `.github/copilot-instructions.md` atau `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | patch `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` atau `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

Di setiap IDE, command CLI `uxskill recommend` / `uxskill lint` / `uxskill stats` yang sama bekerja dari terminal. Engine Python adalah sumber kebenaran; artifact IDE adalah header prompt tipis yang me-routing ke sana.

---

## Use case — skenario konkret

Delapan skenario nyata. Pilih yang paling dekat dengan situasi kamu dan sesuaikan pemanggilannya.

### 1. Membangun dashboard fintech di Cursor

Kamu di Cursor sedang ngerjain dashboard neobank MENA. Kamu install plugin dan jalankan discovery, rekomendasi, lalu generasi dashboard.

```bash
pip install uxskill
uxskill init                                # deteksi Cursor, tulis .cursorrules
uxskill discover                            # intake 10-field
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Lalu di Cursor, tanyakan: *"Generate the dashboard surface using the recommendation in .ux/last-recommendation.json"*. Cursor membaca header `.cursorrules`, me-load rekomendasi, mengirim generasi dashboard dengan batasan eksplisit.

### 2. Menghasilkan landing gaya Stripe di Claude Code

```
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
/ux-discover
> Tipe proyek? landing
> Industri? fintech-payments
> Tone? serious, technical, confident
> Must have? dark-mode, AA, mobile-first
> Forbidden? purple-gradients, three-equal-cards
> Brand referensi? stripe
> Stack? nextjs-15-app-router
> Region? global
> Metrik sukses? signup conversion

/ux-recommend
> [mengembalikan style terpilih, palette, pasangan tipografi, preset motion, komponen, brand teladan]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer menghasilkan halaman]

/ux-lint .
> [lulus — spec brand Stripe dihormati]
```

### 3. Mengaudit code yang ada untuk AI slop di CI

Kamu nge-ship aplikasi Next.js dua minggu lalu. Kamu mau lantai keras terhadap sidik jari AI di setiap PR.

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

PR yang memperkenalkan gradien ungu-ke-biru, Inter di 96px, testimonial "John Doe", atau emoji sebagai ikon gagal di CI. Tanpa biaya LLM. ~200ms.

### 4. Mem-polish permukaan yang ada yang "kerasa AI-generated"

Kamu mewarisi app React yang kelihatan kayak situs SaaS AI lain. Kamu mau bikinnya nggak kelihatan begitu.

```
/ux-critique src/components/Hero.tsx
> [3 menang, 3 meleset, 1 langkah strategis — take-nya jujur]

/ux-lint src/
> [15 sidik jari AI severity tinggi ditandai]

/ux-polish src/components/Hero.tsx
> [pass kosmetik LLM-driven + bunuh AI-slop]

/ux-fix
> [terapkan temuan sebagai commit atomik, jalankan ulang linter]
```

Tiga command, satu permukaan ter-polish, commit atomik per fix.

### 5. Men-design command palette gaya Linear

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [baca data/brands/linear.app.json untuk token + gerakan tanda tangan]
> [baca data/components.json untuk anatomi + state command-palette]
> [kirim frontend-engineer dengan spec Linear eksplisit]
```

Komponen yang dihasilkan memakai token warna asli Linear, stack tipografi, konvensi motion, densitas hairline — bukan "UI gelap generik."

### 6. Menjalankan workshop design thinking 90 menit dengan stakeholder

Kamu punya ruangan dengan 5 orang selama 90 menit. Kamu mau mereka pulang dengan game plan, bukan vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Plugin memfasilitasi lima fase (eksplorasi → heat map → peta stakeholder → sketsa solusi → game plan) end-to-end, diatur waktunya, dengan artifact konkret per-fase. Output-nya `.ux/last-workshop.json` — game plan, bukan cuma "temuan menarik."

### 7. Menulis case study yang bisa dipublikasi setelah launch

Kamu nge-ship loyalty wallet. Kamu mau bahan portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [baca .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [hasilkan case study editorial Wfrah dengan bagian bernomor (A)-(G), pemisah hairline, layout aman-bilingual]
> [tulis case-studies/bashiti-loyalty.html]
```

Case study-nya artifact selesai dan bisa dipublikasi — bukan draft. Monokromatik murni, tipografi editorial, siap di-ship ke portfolio kamu.

### 8. Menjalankan discovery di konteks non-AI (intake terstruktur saja)

Kamu sedang men-scope proyek. Kamu belum butuh rekomendasi — kamu butuh brief terstruktur.

```bash
uxskill discover
# intake 10-field, simpan ke .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Kamu bisa serahkan JSON-nya ke tim kamu, paste ke dokumen Notion, atau masukkan ke tool AI terpisah. ux-skill juga tool intake terstruktur sebagai tambahan dari menjadi engine.

### 9. Persistensi MASTER.md — keputusan design kamu, di repo

Setelah `/ux-recommend`, persistensikan style + palette + tipografi + motion + komponen + brand teladan + guardrail yang dipilih sebagai file Markdown yang bisa dibaca manusia yang bisa direview, di-diff, dan di-version-control oleh tim kamu.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Menulis `.ux/design-system/MASTER.md` (frontmatter YAML + body) dan `.ux/design-system/pages/<nama>.md` per permukaan yang dihasilkan via `persist save-page`. Idempoten — input yang sama menghasilkan output byte-identical, jadi menjalankan ulang di state tidak berubah adalah no-op di git.

---

## Dibandingkan dengan alternatif

Tabel ringkasan singkat. Perbandingan lengkap tabel-per-tabel ada di [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensi | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash command | **22** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Komponen | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Preset motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand spec | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Aturan anti-pattern | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter deterministik CI-safe | **ya** | tidak | tidak | tidak | tidak | tidak | tidak | tidak | tidak |
| IDE didukung | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Gate discovery | **10 field** | implisit | implisit | implisit | implisit | implisit | implisit | implisit | implisit |
| Rantai state `.ux/` | **ya** | tidak | tidak | tidak | tidak | tidak | tidak | tidak | tidak |
| Star (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Penilaian jujur

- **ui-ux-pro-max** lebih besar di awareness, mendukung 18 IDE, punya search gaya BM25 di CSV-nya. Tidak mengirim manifest komponen, manifest motion, library brand, atau linter deterministik.
- **open-design** punya 19 skill + preview tapi hanya dukungan Claude Code dan tanpa lapisan anti-slop.
- **hallmark** paling dekat dalam spirit (juga anti-slop) tapi adalah single skill — tanpa engine, tanpa manifest, tanpa command yang dirantai.
- **material-3-skill** sangat baik kalau kamu khusus mau Material Design 3. Kami tidak bersaing di MD3.

Untuk detail lengkap per dimensi, lihat [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

### v2.1 — Kelengkapan linter (Q3 2026)

- **+17 aturan anti-pattern yang ditangguhkan** untuk mencapai 52 total. Target: state hover dark-on-dark, encoding state hanya-warna, eskalasi z-index berlebih, breakpoint hardcoded di JS, opacity menggantikan state disabled, dll.
- **`uxskill lint --fix` untuk rewrite aman** dari temuan yang mekanis-dapat-diperbaiki (button-no-type, img-no-alt empty-string, penghapusan console-log-leak).
- **Ekstensi VS Code** yang memunculkan temuan lint inline (nggak perlu jalanin CI).

### v2.2 — Ekspansi manifest komponen (Q4 2026)

- **+50 komponen** untuk mencapai 198 total. Yang baru: combobox dengan filter async, command-palette dengan heuristik recent-items, conditional-form-step, varian payment-element, date picker yang RTL-aware, phone input spesifik-MENA, calendar grid dengan overlay hijri.
- **Emit code per-komponen** di 6 stack (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS vanilla).
- **Playground komponen** di uxskill.laithjunaidy.com/playground — coba engine rekomendasi + lihat preview komponen live.

### v3 — Marketplace + kunci-masuk (2027)

- **Marketplace brand spec** — terbitkan dan temukan brand spec komunitas. Bayar-untuk-terbit untuk mendanai moderasi.
- **Aturan anti-pattern custom** — proyek bisa mendefinisikan aturan regex mereka sendiri di `data/anti-patterns.local.json` (sudah dikirim di v2; v3 menambah discovery + sharing).
- **`uxskill plan`** — perencanaan situs multi-halaman lengkap dari brief, bukan hanya satu permukaan.
- **Paritas plugin Figma** — engine rekomendasi yang sama, dimunculkan di Figma.

---

## Kontribusi

Issue dan PR diterima. Tiga area dengan leverage tinggi:

### Menambah aturan anti-pattern

1. Edit `data/anti-patterns.json` — tambah entri dengan `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Tambah test di `tests/linter/` — satu file yang men-trigger aturan, satu yang tidak.
3. Jalankan `uxskill lint tests/linter/should-trigger/<rule>.tsx` — konfirmasi terpicu. Jalankan di `tests/linter/should-not-trigger/<rule>.tsx` — konfirmasi tidak.
4. Buka PR.

### Menambah brand spec

1. Buat `data/brands/<slug>.json` dengan `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Tambah prosa yang bersesuaian di `references/brands/<slug>.md`.
3. Daftarkan di `data/brands/_index.json`.
4. Buka PR. Spec harus didukung referensi sumber-utama (produk asli brand, sistem design publik, atau DESIGN.md kalau mereka mempublikasikannya).

### Menambah preset motion

1. Edit `data/motion-presets.json` — tambah entri dengan `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Preset harus punya varian reduced-motion. Tanpa pengecualian.
3. Buka PR.

### Proses

- Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk proses lengkap.
- Baca [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Aturan baru dan brand spec direview untuk: pendasaran sumber-utama, tidak overfit ke satu proyek, tanpa emoji di data mana pun, perilaku RTL-safe jika berlaku.

---

## Lisensi, penulis, ucapan terima kasih

### Lisensi

MIT. Pakai, fork, bangun di atasnya. Kalau menyelamatkan kamu dari nge-ship AI slop, beri star repo-nya — itu cara termurah untuk mendukungnya.

### Penulis

**Laith Aljunaidy** — solo founder dari [Dot](https://thedotwallet.com), platform loyalty MENA-first. Membangun ux-skill supaya frontend yang dihasilkan AI nggak kelihatan semuanya sama.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Situs: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Ucapan terima kasih

- Tim Anthropic untuk Claude Code dan arsitektur skill / plugin yang membuat ini bisa didistribusikan.
- Nielsen Norman Group, Laws of UX (lawsofux.com), dan komunitas riset UX yang karyanya menginformasikan `data/ux-guidelines.json`.
- Setiap brand yang terdaftar di `data/brands/` — sistem design publik mereka adalah sumber kebenaran untuk brand spec.
- Kontributor v1 asli: skill Claude single-shot yang menjadi benih untuk engine Python v2.
- 8 plugin UX Claude populer yang kami bandingkan dengan — mereka mengangkat standar; ini adalah jawaban kami.

---

**ux-skill** · **v3.1.0-stable** · Dibangun supaya Claude Code, Cursor, Windsurf, dan setiap tool coding AI lain mengeluarkan frontend yang tidak terbaca seperti AI-generated.

> Beri star repo di [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Install via `pip install uxskill` atau `npx uxskill init` · Telusuri perbandingan di [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
