[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · **Bahasa Indonesia** · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: mesin design intelligence untuk Claude Code, Cursor, dan setiap tool coding AI lainnya

**Mesin design intelligence yang membuat UI buatan AI terasa khas, bukan generik.** Pasang di salah satu dari 17 tool coding AI dan hasilmu tidak lagi terlihat seperti buatan AI. Gratis, MIT, offline, tanpa LLM.

```bash
pip install uxskill
```

**[Beri ux-skill bintang di GitHub](https://github.com/Laith0003/ux-skill)** kalau ini berguna: itu cara paling murah untuk membantu proyek ini. Baru di sini? Mulai dengan [tur 60 detik](#install-cepat) atau lihat langsung di [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![Sebelum: hero generik dengan foto stok, gradien violet lembut, tanpa identitas merek. Sesudah: foto lokasi konstruksi asli di bawah lapisan gelap, judul editorial dengan aksen amber, dan formulir permintaan penawaran langsung di hero. Prompt yang sama, hasil berbeda saat ux-skill memberi batasannya.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Sebelum: slop SEO generik dengan foto stok. Sesudah: hero dengan foto konstruksi asli di bawah lapisan gelap, judul editorial dengan aksen amber, formulir penawaran di hero. Tool coding AI yang sama, prompt yang sama, hasil berbeda saat ux-skill memberi batasannya.*

> **v4.0, FOUNDATIONS: satu perintah membangun sistem desain lengkap yang diperiksa terhadap WCAG, dengan bahasa Arab dan tulisan kanan ke kiri sudah tersedia.** Plugin UX terkuat untuk coding dengan AI. Inti penalaran Python dengan synthesizer deterministik 7 sumbu, 12 manifest JSON yang bisa di-query (84 style, 176 palette, 70 pasangan tipografi, 148 komponen, 184 industri, 35 jenis chart, 57 preset motion, 112 hukum UX, 171 aturan anti-pattern, 25 tech stack, 160 spesifikasi brand), 18 slash command, 5 sub-agent, 25 tool MCP, dan linter anti-AI-slop yang deterministik. Lintas IDE: terpasang di Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer, dan Roo Cline.

> **Nama brand-nya `ux-skill`.** Nama paket PyPI / npm tetap `uxskill`. Repo GitHub ada di [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Penulis:** [Laith Aljunaidy](https://laithjunaidy.com), desainer dan CTO di Amman · **Situs:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **Bandingkan dengan semua plugin UX untuk Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0--beta.2-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#installer-17-ide)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Baru di 4.0: fondasi

Satu warna merek masuk, satu sistem desain keluar, dengan kontras yang sudah diperiksa sebelum sampai ke tanganmu.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 atau lebih baru. Untuk server MCP, `pip install --upgrade 'uxskill[mcp]'`. Dengan pipx, `pipx install uxskill` (di atas 3.x yang sudah terpasang, `pipx upgrade uxskill`). Dengan npm, `npx uxskill@latest`. Datang dari 3.x? [Panduan migrasi](docs/migrating-to-4.md) memetakan setiap token 3.x ke perannya di 4.0.

**Sedang membangun produk atau landing page?** Kamu mendapat `tokens.css` untuk ditautkan dari halamanmu, `fonts.css` dengan fallback bermetrik serupa untuk huruf yang dipilih, `fonts-self-host.css` yang memuat huruf dari berkasmu sendiri, `tokens.json` untuk tool, aset brand dekoratif di `art/`, dan `system-report.md`, yang menjelaskan dengan bahasa sederhana apa yang dibangun, kenapa, dan komposisi halaman mana yang jadi titik awal. Beri gaya dengan peran (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`), lalu nyalakan mode gelap, kontras tinggi, spasi rapat, kanan ke kiri, atau gerak dikurangi dengan satu atribut di `<html>`. Muat huruf lewat tautan Google Fonts dari laporan, atau lewat `fonts-self-host.css` dan folder `fonts/`, lalu tautkan `fonts.css` bersama salah satunya, sebelum `tokens.css`; jangan ubah kedua berkas itu. Dengan `--brief`, tampilan mengikuti industri dan nada saat brief menyebutkannya, dan field terstruktur (usia, bahasa, skema default, konteks membaca) menentukan ukuran teks, area sentuh, aksara, dan skema mana yang terbuka; discovery tidak menanyakan industri, jadi `/ux-system create` yang menanyakannya. Di Claude Code, `/ux-system create` memeriksa versi yang terpasang, menjalankan build, dan menjelaskan laporannya.

**Sedang merancang sistem desain?** Sembilan fondasi (warna, tipografi, spasi, tata letak, radius, garis tepi, elevasi, gerak, citra), masing-masing berubah secara kontinu mengikuti tujuh sumbu, dengan primitive dan peran semantik, dalam format W3C design tokens (DTCG 2025.10) beserta nilai untuk setiap mode. Input sama, byte sama. Lewat MCP, `ux_system_build` mengembalikan laporan, hasil pemeriksaan, dan ukuran tiap berkas, lalu menulis berkas yang sama dengan perintahnya saat diberi `out`.

- **Pemeriksaan WCAG.** Setiap pasangan warna teks, kontrol, dan fokus diukur dalam mode terang dan gelap, pada kontras standar dan tinggi: WCAG 1.4.3 (teks 4.5:1) dan 1.4.11 (non-teks 3:1) pada kontras standar, WCAG 1.4.6 (teks 7:1) pada kontras tinggi, ditambah batas bawah 4.5:1 pada kontras tinggi untuk sebagian besar elemen non-teks yang merupakan aturan kami sendiri, karena WCAG tidak menetapkan level non-teks yang lebih tinggi. Sistem yang gagal tidak ditulis; pesannya menyebutkan apa yang harus diubah.
- **Aman secara default.** Tidak pernah menimpa berkas yang berbeda. `--force` mengganti berkas hanya saat kamu memintanya.
- **Bahasa Arab.** Di bawah `dir="rtl"` teks beralih ke huruf Arab dengan ukuran dan tinggi baris sendiri; spasi memakai properti logis dan gerak dicerminkan. `--latin-only` tidak menyertakannya.

**Sistem yang sudah kamu punya.** `/ux-system enhance --from` membacanya dengan nama-namanya sendiri (token DTCG, custom property CSS, tema Tailwind, berkas aturan markdown, atau ekspor variabel Figma), memeriksanya dengan pemeriksaan yang sama, dan mengukur apa yang benar-benar dilakukan code-mu dengannya; tidak ada yang ditulis ulang. `/ux-system extend --from` menambahkan fondasi, peran, atau kontrak tanpa mengubah token yang sudah ada, dalam berkas ekstensi di sebelahnya, dan `uxskill system export` menuliskannya sebagai tokens.css, tema Tailwind 4, atau variabel Figma. 4.2 menambahkan lapisan kepercayaan (lint di setiap penulisan, peninjau akhir) dan peluncurannya. Lihat [changelog](CHANGELOG.md).

**Komponen dan section.** 23 kontrak komponen menyebutkan token mana yang diikat setiap bagian kontrol di setiap state dan bagaimana tiap state bergerak: perubahan state bertransisi pada `motion.state`, tekanan berskala pada `motion.press.scale` (dan diam saat gerak dikurangi), dan tab, menu, serta segmented control menggeser satu indikator. 14 kontrak section (hero, harga, FAQ, footer, dan lainnya) menyebutkan tugas tiap section, komponen yang diterima slot-nya, bukti yang dibutuhkan, dan cara section itu bertumpuk di ponsel. Halaman yang dibangun darinya memakai foto; potongan antarmuka adalah citra tambahan, bukan pengganti.

**Linter yang membaca halaman.** 171 aturan, banyak di antaranya dengan pemeriksaan pada CSS dan markup yang sudah di-parse, membaca sistem milik halaman itu sendiri: gerak diatur waktunya dari kurvanya, tinggi baris judul display dijaga pada batas bawah engine, dan kontrol yang tersembunyi harus keluar dari urutan tab. `uxskill lint --render` membuka setiap halaman di Chromium headless pada lebar desktop dan ponsel lalu mengoperasikannya: cincin fokus yang tidak tampil atau terpotong, hover dan tekan yang responsnya telat, fokus yang hilang setelah Escape, dan tekanan yang masih bergerak saat gerak dikurangi.

**Lebih sedikit command.** 25 slash command menjadi 18. `/ux-discover` menerima `--frame` dan `--recommend`, `/ux-design` menerima `--component`, `--dashboard`, dan `--from-image`, `/ux-polish` mengulang lint, fix, re-lint sampai skor mencapai 90 atau tiga putaran lewat, dan `/ux-init` menerima `--stats`. Tujuh nama lama tetap jalan sebagai alias dan dihapus di 4.1; lihat [alias](#alias-dihapus-di-41).

**Playbook surface.** Aturan landing, dashboard, dan komponen ada di `references/surfaces/`, satu playbook untuk masing-masing. `/ux-design` memuat tepat satu, dipilih sesuai mode-nya, jadi build dashboard tidak pernah membaca aturan hero.

Tes: **9764 lolos**. Offline. Deterministik. Tidak pernah memanggil LLM.

### Baru di v3.1: setia pada brand, responsif, hidup

- **Kesetiaan pada brand ditegakkan, bukan diharapkan.** Warna primer dibaca dari piksel LOGO (bukan dari CSS yang paling banyak dicat); font default ditolak demi gaya huruf logo. Brand yang diekstrak berjalan `recommend` -> `synthesize`, dan **batas bawah keras** di `evaluate` menggagalkan output apa pun yang kehilangan warna atau logo brand, atau tidak memuat citra asli. Interop dua arah dengan konvensi terbuka `brand.md` (render + impor).
- **Mobile-first, diperiksa.** Fondasi kerajinan baru (`responsive.md`, `component-behaviors.md`) plus pemeriksaan yang sadar pemenggalan baris dan gagal pada scroll horizontal, label nav, wordmark, atau tombol yang terpotong ke baris baru, atau header sticky yang terlalu tinggi.
- **Lapisan wow.** Engine menurunkan 2-3 momen khas yang terkoordinasi per halaman; doktrin "wow hanya bisa datang dari pengguna" dibalik.
- **Linter lebih tajam** (152 aturan): deteksi citra wajib dan elemen ikon saja, aturan token placeholder dan `100vw`; picsum ber-seed dipertahankan, yang acak dibuang.

Catatan lengkap di [CHANGELOG.md](CHANGELOG.md).

### Apa yang baru di v3

- **Brand specs jadi data pelatihan, bukan template.** 160 brand specs tidak lagi katalog yang diambil recommender, melainkan kosakata yang disuling synthesizer. Output baru di setiap panggilan.
- **Synthesizer 7-sumbu** (warmth, contrast, density, geometry, formality, motion, type_personality). Brief dipetakan secara deterministik ke nilai sumbu; nilai sumbu dikompilasi ke palette + tipografi + spacing + radius + motion segar.
- **Tiga mode auto-dispatch**: `strict_brand` (100% satu brand), `brand_anchor` (70% satu brand + 30% adaptasi sumbu dari brand saudara), `pure_synthesis` (tanpa brand disebut, destilasi 8 contoh selaras sumbu).
- **Decisions ledger me-rerank recommender.** `.ux/decisions.jsonl` me-rerank kandidat berdasar kemenangan masa lalu di bucket `(industry, ui_type)` yang sama. Cold-start aman. Hanya menghitung keputusan dengan `lint_score >= 80` + `user_accepted = true`.
- **Matriks interaksi sumbu**: resolusi konflik eksplisit antar sumbu bersaing (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Tidak ada lagi aturan ad-hoc senyap.
- **Loop otomatis `/ux-evolve`** (di 4.0, loop default `/ux-polish`): lint → polish → re-lint hingga skor ≥ 90, plateau, atau 3 putaran di 4.0 (5 di v3). Quality gate di 65.
- **3 tool MCP baru** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Dashboard stats lokal**: `uxskill stats --html` menulis `.ux/stats.html` yang menunjukkan apa yang dipelajari instalasi **kamu**. Tanpa telemetri, tanpa agregasi global.
- **223 tes lolos.** Offline. Deterministik. LLM tak pernah dipanggil.

Detail lengkap di [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Riwayat star

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## Apa itu ux-skill

ux-skill adalah **mesin design intelligence** untuk tool coding AI. Berjalan sebagai paket Python (`pip install uxskill`), sebagai plugin Claude Code, dan sebagai multi-installer 17 IDE. Mesinnya menerima brief proyek (industri, audiens, tone, must-have, hal yang dilarang, stack, region) dan mengembalikan sistem design rekomendasi lengkap: style, palette, pasangan tipografi, preset motion, komponen, brand teladan untuk dipelajari, dan guardrail anti-pattern yang harus dipertahankan. Rekomendasinya deterministik, input yang sama selalu menghasilkan output yang sama.

Plugin ini duduk di antara kamu dan tool coding AI. Ketika kamu meminta Claude Code, Cursor, atau asisten AI lainnya untuk "buat landing page fintech," asisten biasanya berimprovisasi, dan hasilnya terbaca sebagai buatan AI dalam lima detik (gradien ungu-ke-biru, tiga card sama besar, Inter di ukuran display, "John Doe" di testimonial, transisi default 300ms, hero centered, panah CTA yang bouncing). ux-skill mengganti improvisasi dengan **batasan terstruktur**: kamu jalankan `/ux-discover` untuk menangkap brief dan memilih sistem, `/ux-design` untuk menghasilkan code, dan `/ux-lint` untuk memverifikasi bahwa hasilnya lolos 171 aturan deterministik anti-AI-slop sebelum commit.

README ini adalah referensi kanonis. Setiap command, setiap sub-agent, setiap data manifest, setiap path install, setiap brand spec, setiap kategori anti-pattern, semuanya didokumentasikan di sini. Jika kamu sedang mencari plugin design untuk Claude Code atau membandingkan tool design AI untuk Cursor, Windsurf, atau Codex, baca ini dari atas ke bawah bersama [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Daftar isi

1. [Otak, apa itu v3.0](#otak-apa-itu-v30)
2. [Install cepat](#install-cepat)
3. [Angka, perbandingan live dengan 8 skill UX Claude teratas](#angka-perbandingan-live-dengan-8-skill-ux-claude-teratas)
4. [Arsitektur, bagaimana semuanya cocok](#arsitektur-bagaimana-semuanya-cocok)
5. [18 slash command, referensi detail](#18-slash-command-referensi-detail)
6. [5 sub-agent](#5-sub-agent)
7. [11 data manifest](#11-data-manifest)
8. [171 aturan anti-AI-slop, linter-nya](#171-aturan-anti-ai-slop-linter-nya)
9. [160 spec brand DESIGN.md, per kategori](#160-spec-brand-designmd-per-kategori)
10. [Server MCP, langkah asimetris](#server-mcp-langkah-asimetris)
11. [Installer 17 IDE](#installer-17-ide)
12. [Use case, skenario konkret](#use-case-skenario-konkret)
13. [Dibandingkan dengan alternatif](#dibandingkan-dengan-alternatif)
14. [Roadmap](#roadmap)
15. [Kontribusi](#kontribusi)
16. [Lisensi, penulis, ucapan terima kasih](#lisensi-penulis-ucapan-terima-kasih)

---

## Otak: apa itu v3.0

v3.1.0 adalah pergeseran arsitektur terbesar dalam sejarah ux-skill. Recommender tidak lagi mengambil template dari katalog, engine **mensintesis** bahasa desain segar per brief. Brief yang sama selalu menghasilkan output yang sama (sepenuhnya deterministik), tetapi setiap brief berbeda mendapat sistem barunya sendiri. Brand specs bukan lagi template; mereka adalah data pelatihan tempat engine belajar kosakata. Sistem memiliki mata pada sejarahnya sendiri, menutup loop umpan balik secara lokal, dan tidak pernah memanggil LLM.

Compiler adalah **synthesizer deterministik 7-sumbu**, warmth, contrast, density, geometry, formality, motion, type_personality. Setiap brief dipetakan ke nilai sumbu; nilai sumbu dikompilasi ke palette + tipografi + spacing + radius + motion segar. Skala tipografi modular memilih rasio dari contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Primitif layout responsif sejak dirancang (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Layout rusak tak bisa dipancarkan karena tak bisa direpresentasikan.

Ada tiga mode auto-dispatch: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% token Stripe, jalur tercepat); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% adaptasi sumbu dari 4 brand saudara); dan `pure_synthesis` (tanpa brand disebut → ruang tak terbatas, 8 contoh selaras sumbu disuling jadi bahasa desain baru). Konflik antar sumbu diselesaikan oleh **matriks interaksi sumbu** terdokumentasi, dense + corporate kompilasi ke 4px (density menang, mazhab Bloomberg), airy + corporate ke 12px (formality menang, mewah), soft + playful ke 18px radius, sharp + corporate ke 2px. Tak ada aturan ad-hoc senyap dalam implementasi.

**Decisions ledger** (`.ux/decisions.jsonl`, schema `_v: 1` terkunci) menutup loop umpan balik. Recommender kini mengurutkan ulang kandidat berdasar kemenangan masa lalu di bucket `(industry, ui_type)` yang sama. Aman saat cold start: di bawah 3 keputusan sebelumnya, pengurutan ulang dilewati. Hanya menghitung keputusan dengan `lint_score >= 80` DAN `user_accepted = true`. Selain itu `/ux-polish` menjalankan lint → polish → re-lint hingga skor ≥ 90, plateau, atau 3 putaran, dengan quality gate di 65 yang menolak output di bawahnya tanpa `--force`. Hasilnya: tiap instalasi makin pintar di corpus-nya sendiri, tiap run reproducible antar mesin, dan engine tetap sepenuhnya offline.

---

## Install cepat

Tiga jalur install. Pilih yang cocok dengan environment kamu.

### Jalur 1: marketplace Claude Code (kanonis)

Kalau kamu hidup di Claude Code, install via marketplace plugin:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Itu menghubungkan semua 18 slash command (plus 7 nama lama yang tetap jadi alias sampai 4.1) dan 5 sub-agent ke sesi Claude Code kamu. Setelah install, jalankan `/ux-init` untuk setup direktori state `.ux/` per proyek dan verifikasi bahwa engine Python bisa dijangkau.

### Jalur 2: pip (universal)

Kalau kamu hidup di luar Claude Code (Cursor, Windsurf, CLI, CI), install paket Python:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

Paket ini meng-expose `ux` dan `uxskill` sebagai entry point CLI, keduanya binary yang sama.

### Jalur 3: npx (tidak perlu Python)

Kalau kamu tidak mau mengelola Python langsung, wrapper npx melakukan bootstrap segalanya via `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Verifikasi install

```bash
ux stats
# {
#   "version": "4.0.0b2",
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

Kedua belas hitungan itu berjumlah 1.262 entri. Kalau ada hitungan yang mengembalikan 0, file JSON-nya hilang; buka issue di [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Angka: perbandingan live dengan 8 skill UX Claude teratas

Hitungan star terakhir diverifikasi via `gh api` pada **2026-05-28**. ux-skill (Laith0003/ux-skill) adalah pendatang baru, kami kecil di awareness, dalam di arsitektur. Perbandingan di bawah ini jujur: di mana kami kalah, di mana kami menang.

| Plugin | Star | Arsitektur | Slash command | Linter (CI-safe) | Brand spec | Komponen | Preset motion | IDE didukung |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, skill tunggal | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + taste berbasis riset | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | SKILL.md tunggal 62 KB + script | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Library skill terhubung MCP | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill satu-estetika | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill design anti-slop | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Komponen MD3 + audit | 1 | - | (MD3 saja) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Engine Python + 12 manifest + 18 command + 5 sub-agent + linter CI** | **18** | **171 aturan deterministik** | **160** | **148** | **57** | **17** |

### Di mana kami kalah

- **Awareness.** Mereka punya ratusan ribu star. Kami punya 14. Beri kami star, itu cara termurah untuk membantu.
- **Pengenalan brand.** ui-ux-pro-max dan open-design punya keunggulan terdepan yang diukur dalam bulan, bukan hari.
- **Polesan marketing.** Mereka punya screenshot, video demo, dan landing page yang bisa ditemukan. Kami punya README yang lengkap dan landing yang tipis.

### Di mana kami menang

- **Library komponen:** 148 komponen yang didokumentasikan dengan anatomi, state, token yang dipakai, dan spec motion. Tidak ada dari 8 yang lain mengirim manifest komponen.
- **Preset motion:** 57 entri siap-stack (Framer Motion, GSAP, CSS) dengan fallback reduced-motion. Tidak ada dari yang lain mengirim manifest motion.
- **Linter anti-pattern:** 171 aturan deterministik, berjalan di CI, exit non-zero pada Critical/High. Tidak ada dari yang lain mengirim linter deterministik.
- **Brand spec:** 160 spec DESIGN.md asli (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude, dan 96 lainnya). Tidak ada dari yang lain mengirim library brand.
- **17 IDE didukung:** engine yang sama, perekat berbeda per IDE.
- **18 slash command:** discovery, generation (halaman, komponen, dashboard, dari gambar), audit, lint, loop polish, fix loop, case-study, workshop, copy, motion, a11y, conductor, terintegrasi sepenuhnya.

Tabel side-by-side lengkap per tabel ada di [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Arsitektur: bagaimana semuanya cocok

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

### Cara engine benar-benar bekerja

1. **Input.** Kamu memberi brief, baik secara interaktif lewat `/ux-discover` (10 field) atau non-interaktif lewat flag ke `ux recommend`.
2. **5 pencarian paralel.** Engine menjalankan lima pencarian sekaligus di seluruh manifest:
   - **Industri → recommended_styles** (industries.json)
   - **Style → kompatibilitas palette + tipografi + motion** (styles.json)
   - **Nada × wajib-ada → filter palette** (palettes.json)
   - **Stack → kompatibilitas komponen + preset motion** (tech-stacks.json, motion-presets.json)
   - **Terlarang + wilayah → guardrail + daftar pendek brand teladan** (anti-patterns.json, brands/)
3. **Merge.** Merger deterministik mengurutkan kandidat, menyelesaikan konflik (misalnya mode gelap yang wajib memaksa mode palette), dan mengeluarkan satu sistem rekomendasi.
4. **Output.** Dokumen JSON berisi style terpilih, palette, pasangan tipografi, 5 preset motion teratas, 12 komponen teratas, 5 brand teladan teratas, dan semua 171 guardrail anti-pattern dalam keadaan aktif. Plus blok alasan yang menjelaskan setiap pilihan.
5. **Generasi.** Command berikutnya (`/ux-design` dalam mode halaman, komponen, dashboard, dan gambar, serta `/ux-system`) memakai rekomendasi itu untuk menghasilkan code sungguhan lewat sub-agent.
6. **Verifikasi.** `/ux-lint` memindai ulang code yang dihasilkan terhadap 171 aturan. Exit non-zero pada Critical/High di CI.

**Tambahan v3.** Recommender kini mengurutkan ulang kandidat dari `engine/decisions/` memakai `.ux/decisions.jsonl` (hanya menghitung keputusan dengan `lint_score >= 80` DAN `user_accepted = true`; aman saat cold start di bawah 3 keputusan sebelumnya). Jalur generator bisa diteruskan ke `engine/synthesizer/`, compiler deterministik 7 sumbu yang menghasilkan token palette + tipografi + spasi + radius + motion yang baru untuk setiap brief, alih-alih memilih template dari katalog. Detailnya di [Otak, apa itu v3.0](#otak-apa-itu-v30).

**Python berpikir. HTML menampilkan. Markdown merantai.**

---

## 18 slash command: referensi detail

Setiap command dikirim sebagai berkas `.md` di bawah `commands/` dengan `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process`, dan `output state file`. Deskripsi di bawah sudah diringkas; sumber lengkapnya adalah spesifikasi kanonis.

Command dikelompokkan ke tujuh kelompok: **bootstrap & inventaris**, **discovery & rekomendasi**, **generasi**, **audit & verifikasi**, **perbaikan & polish**, **discovery & narasi**, dan **conductor**. Tujuh nama 3.x tetap jalan sebagai [alias](#alias-dihapus-di-41) sampai 4.1.

### Bootstrap & inventaris

#### `/ux-init`: bootstrap proyek

- **Apa:** Mendeteksi IDE mana yang kamu pakai (`.claude/`, `.cursor/`, `.windsurf/`, dll), install artifact yang tepat, verifikasi engine Python bisa dijangkau, cetak snapshot stats. `--stats` hanya mencetak snapshot: versi + jumlah entri di manifest data.
- **Kapan dipakai:** Install pertama kali di proyek baru. Setelah meng-clone proyek yang pakai ux-skill. Setelah `pip install --upgrade uxskill`. `--stats` setelah install, setelah upgrade, atau saat rekomendasi memberi pilihan yang mengejutkan dan kamu curiga manifest-nya tidak lengkap.
- **Kapan dilewati:** Kamu sudah jalankan di proyek ini dan tidak ada yang berubah. `--stats` tidak pernah perlu dilewati: cuma pembacaan 50ms.
- **Pemanggilan:** `/ux-init` (tanpa argumen), `/ux-init --stats`, atau `uxskill init` / `uxskill stats` dari CLI. `--decisions` menambahkan ringkasan decisions ledger; `--html` menulis `.ux/stats.html`.
- **Output:** Artifact per IDE (lihat [Installer 17 IDE](#installer-17-ide)) + direktori `.ux/` + ringkasan stdout. `--stats`: JSON ke stdout (lihat [Verifikasi install](#verifikasi-install) di atas).
- **Merantai ke:** `/ux-discover` berikutnya. `--stats` hanya untuk diagnostik.

#### `/ux-mcp`: menjalankan engine sebagai server MCP

- **Apa:** Menjalankan engine sebagai server Model Context Protocol lewat stdio. 25 tool (recommender, linter, persistensi, synthesizer, decisions ledger, ekstraksi gambar, manifest data, serta membangun, mengimpor, meningkatkan, memperluas, mengekspor, dan memeriksa sistem desain) bisa dipanggil dari host apa pun yang mendukung MCP, tanpa plugin.
- **Kapan dipakai:** Kamu bekerja di host lain yang mendukung MCP dan ingin engine yang sama. Kamu menjalankan pipeline multi-agent yang butuh satu sumber batasan desain. Kamu ingin recommender atau linter sebagai proses yang berjalan lama di CI.
- **Kapan dilewati:** Kamu ada di Claude Code dengan plugin terpasang; slash command sudah menjangkau engine. Kamu butuh jawaban sekali jalan; `uxskill recommend` atau `uxskill lint` lebih sederhana.
- **Pemanggilan:** `/ux-mcp`, atau `ux-mcp` dari shell setelah `pip install 'uxskill[mcp]'`.
- **Output:** Server JSON-RPC lewat stdio. Lihat [Server MCP](#server-mcp-langkah-asimetris) dan `commands/ux-mcp.md` untuk konfigurasi tiap klien.
- **Merantai ke:** Tidak ada; ini transport, bukan langkah.

### Discovery & rekomendasi

#### `/ux-discover`: fungsi pemaksa (intake 10 field, framing, rekomendasi)

- **Apa:** Intake wajib 10 field yang dilalui setiap proyek sebelum command generasi apa pun. Jenis proyek, audiens, tujuan utama, nada, wajib-ada, terlarang, brand referensi, stack, wilayah, metrik keberhasilan. **Tanpa improvisasi.** Frasa terlarang ("modern", "clean") memaksa pengguna untuk spesifik. Lalu recommender berjalan: 5 pencarian paralel engine Python di 12 manifest mengembalikan satu sistem desain gabungan (Industri → Style → Palette → Tipografi → Motion + Komponen + Brand teladan + Guardrail).
- **Mode:** `--frame` mencatat untuk siapa, outcome, hipotesis, dan sinyal keberhasilan dalam blok framing empat field, lebih ringan dari intake lengkap. `--recommend` hanya menjalankan recommender, dari brief yang tersimpan atau flag sekali jalan.
- **Kapan dipakai:** Sebelum `/ux-design` atau `/ux-system` apa pun. Setiap kali brief sebelumnya sudah basi. `--frame` di awal proyek, sprint, atau pekerjaan sekali jalan, atau di tengah jalan saat percakapan melenceng. `--recommend` saat mengarahkan ulang produk yang tampak lelah.
- **Kapan dilewati:** Kamu sedang memperbaiki bug (`/ux-fix`). Kamu hanya menjalankan satu pass linter (`/ux-lint`). Brief tidak berubah sejak sesi terakhir.
- **Pemanggilan (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"`, atau `/ux-discover --recommend`.
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
- **Output:** `.ux/last-discovery.json` (brief 10 field), `.ux/last-recommendation.json` (style terpilih, palette, pasangan tipografi, 5 preset motion teratas, 12 komponen teratas, 5 brand teladan teratas, semua 171 guardrail anti-pattern aktif, plus alasan), dan dengan `--frame`, `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Merantai ke:** `/ux-design [extra brief]` → code frontend yang berpijak pada rekomendasi. `/ux-design --component <name>` → satu komponen yang selaras dengan batasan yang ditemukan. `/ux-system` → sistem desain lengkap dari rekomendasi. `/ux-lint` → verifikasi code yang dihasilkan.

### Generasi

#### `/ux-design`: hasilkan permukaan yang indah dan anti-slop dari brief

- **Apa:** Menghasilkan artifact frontend lengkap, kelas produksi (landing, situs marketing, app shell) dari brief discovery + rekomendasi. Mengirim `frontend-engineer` dengan arah kreatif dari anti-slop dan referensi arsenal. Brief, atau sebuah flag, memilih satu dari empat mode:
  - **halaman** (default): satu halaman penuh atau surface dengan banyak section. Menulis `.ux/last-design.json`.
  - **`--component [name]`**: satu komponen kelas produksi (button, modal, navbar, sidebar, card, tabel, form, chart). Keempat state interaksi, aksesibel, sesuai brand. Mencari komponen di `.ux/last-recommendation.json` dulu, lalu kembali ke query manifest langsung. Menulis `.ux/last-component.json`.
  - **`--dashboard`**: disiplin densitas data, layout bento, numeral monospace tabular, pola sparkline, anti-overuse card, warna state semantik, motion yang hemat. Bukan situs marketing dengan chart ditempel. Menulis `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: membaca gambar referensi desain (PNG/JPG/WebP) dengan computer vision murni Pillow (palette dominan, polaritas kanvas, sinyal tipografi), mencocokkannya dengan manifest palette dan style, lalu membangun dari rekomendasi yang dihasilkan. `--extract-only` berhenti setelah ekstraksi. Menulis `.ux/last-image-extract.json`.
- **Kapan dipakai:** "Design sebuah", "buatin gue", "generate landing page", "buat dashboard", "bikin komponen", "bikin tombol", "design panel admin", "konsol operator", "papan KPI", "bikin seperti screenshot ini", permintaan deliverable visual bebas-bentuk apa pun.
- **Kapan dilewati:** Kamu mau review, bukan build (pakai `/ux-audit` atau `/ux-critique`). Pekerjaan backend atau infrastruktur.
- **Pemanggilan:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Output:** Code yang dihasilkan (HTML / Blade / JSX / Vue / Astro), plus berkas state dari mode tersebut.
- **Merantai ke:** `/ux-lint` → verifikasi terhadap guardrail. `/ux-polish` → pass kosmetik. `/ux-a11y` → audit aksesibilitas. `/ux-copy` → review microcopy. `/ux-fix` → terapkan temuan sebagai commit atomik.

#### `/ux-system`: hasilkan sistem design starter lengkap

- **Apa:** Mengusulkan sistem design starter lengkap untuk proyek yang belum punya, token (warna, tipografi, spasi, motion, radius, shadow), dokumen foundation, kontrak komponen, pasangan dark-mode, theme switcher. Mengirim `design-system-architect`.
- **Kapan dipakai:** "Kami nggak punya sistem design", "bikinin sistem", "usulkan token", "tema kita harusnya kayak apa", "setup DS kita".
- **Kapan dilewati:** Proyek sudah punya sistem desain; pakai `/ux-design --component` terhadap sistem yang ada. Backend atau infrastruktur.
- **Pemanggilan:** `/ux-system create` (engine fondasi), `/ux-system enhance --from <file>` (mengukur sistem yang sudah kamu punya), `/ux-system extend --from <file> --add <foundation>` (menambahinya tanpa mengubahnya), atau `/ux-system` (alur 3.x; menjalankan discovery dulu kalau belum ada).
- **Output:** `tokens.json`, `foundations.md`, kontrak `components/*.md`, emit Tailwind / vanilla / SCSS opsional. Menulis `.ux/last-system.json` untuk konteks rantai.
- **Merantai ke:** `/ux-design --component` → membangun di atas sistem baru. `/ux-design` → menghasilkan surface dengan token baru.

#### `/ux-motion`: treatment motion

- **Apa:** Menghasilkan lapisan motion dari sebuah permukaan, durasi, easing, koreografi, fallback reduced-motion, disiplin performa. Juga meng-audit motion yang ada terhadap 5 dimensi (timing, easing, makna, reduced-motion, performa).
- **Kapan dipakai:** "Cek motion", "animasinya bagus nggak", "fix motion-nya", "review animasi", "audit motion", "pass performa di motion".
- **Kapan dilewati:** Permukaan tidak punya motion (pakai `/ux-audit` atau `/ux-polish`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-motion path/to/component.tsx` (mode audit) atau `/ux-motion --generate hero-entry` (generasi).
- **Output:** Code yang diperbarui (mode generasi) atau laporan `.ux/last-motion.json` (mode audit).
- **Merantai ke:** `/ux-fix` → terapkan temuan motion. `/ux-polish` → kencangkan.

### Audit & verifikasi

#### `/ux-lint`: linter berbasis regex deterministik (tanpa LLM, CI-safe)

- **Apa:** Menjalankan 171 aturan terhadap code kamu. Tidak ada panggilan LLM. Exit non-zero pada Critical / High di CI. Sumber: `data/anti-patterns.json`. Aturan mencakup A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).
- **Kapan dipakai:** Hook pre-commit. Gate CI. Pass pertama yang cepat di codebase besar sebelum bayar biaya `/ux-audit`. Setelah `/ux-design` dalam mode apa pun untuk verifikasi generasi.
- **Kapan dilewati:** Kamu mau fix loop (linter melapor, tidak mengedit, rantai ke `/ux-polish --fix` atau `/ux-fix`). Kamu mau penilaian selera (pakai `/ux-critique`).
- **Pemanggilan (slash):** `/ux-lint src/`.
- **Pemanggilan (CLI):** `uxskill lint .` atau `python3 bin/ux-lint.py .` atau `bash bin/ux-lint.sh --ci --fail-on high`.
- **Pemanggilan (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Output:** Temuan ke stdout (lokasi, id aturan, severity, bukti). Exit code 0 kalau bersih, non-zero pada Critical/High saat `--fail-on high` di-set.
- **Merantai ke:** `/ux-polish --fix` → counterpart LLM-driven pada pola yang sama. `/ux-fix` → terapkan temuan sebagai commit, diurutkan severity. `/ux-audit` → pass penalaran 6-lensa lengkap. `/ux-next` → biarkan conductor yang putuskan.

#### `/ux-audit`: audit design 6-lensa

- **Apa:** Review terstruktur, opinionated terhadap enam lensa (kejelasan, hirarki, aksesibilitas, suara, motion, taste), menghasilkan temuan ber-tag severity. Laporan gaya Polaris. Membaca `.ux/last-frame.json` dulu, audiens dan outcome menjangkar severity setiap temuan.
- **Kapan dipakai:** Permukaan ada dan kamu mau critique yang bisa dipertahankan. "Audit", "review UX-nya", "ini bagus nggak", "apa yang rusak", "robek ini".
- **Kapan dilewati:** Permukaan belum ada (pakai `/ux-design`). User mau satu lensa (pakai command yang tertarget: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). User mau opini selera (pakai `/ux-critique`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-audit https://example.com/pricing` atau `/ux-audit src/components/Pricing.tsx`.
- **Output:** Menulis `.ux/last-audit.json`, array `findings` berisi `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Merantai ke:** `/ux-fix` → terapkan temuan. `/ux-polish` → pass kosmetik. `/ux-design` → kalau perlu redesign struktural.

#### `/ux-a11y`: audit WCAG 2.1 AA + cek sopan-santun umum

- **Apa:** Audit WCAG 2.1 AA terstruktur, plus cek sopan-santun umum yang lolos tool otomatis tapi tetap menyakiti user nyata (visibilitas focus, kespesifikan error, preferensi motion, perangkap keyboard, ketergantungan warna).
- **Kapan dipakai:** Gate aksesibilitas pre-ship. Setelah redesign. "Cek aksesibilitas", "audit WCAG", "ini accessible nggak", "review a11y", "tes screen reader", "cek navigasi keyboard".
- **Kapan dilewati:** Tidak menghadap-user. Backend atau infrastruktur. Sketsa work-in-progress.
- **Pemanggilan:** `/ux-a11y https://example.com` (URL live lebih disukai, tool otomatis dan testing keyboard hanya bekerja di live).
- **Output:** Menulis `.ux/last-a11y.json`, array `findings` berisi `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, array `beyond_wcag`, `severity_counts`.
- **Merantai ke:** `/ux-fix` → terapkan temuan sebagai commit. `/ux-copy` → perbaiki alt text dan wiring error form sebagai bagian dari pass copy.

#### `/ux-critique`: penilaian selera (3 menang, 3 meleset, 1 langkah strategis)

- **Apa:** Opini seorang designer, bukan audit terstruktur, bukan skor severity, hanya take yang ringkas dan opinionated yang menamai apa yang bekerja, apa yang tidak, dan satu langkah strategis yang akan mengubah paling banyak.
- **Kapan dipakai:** "Menurut lo gimana", "ini bagus nggak", "kritik ini", "honest take", "vibe-nya pas nggak", "kerasa kayak kita nggak", "ini ship-able nggak".
- **Kapan dilewati:** User eksplisit mau audit terstruktur (pakai `/ux-audit`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-critique https://example.com`.
- **Output:** Menulis `.ux/last-critique.json`, 3 menang, 3 meleset, 1 langkah strategis, plus prosa.
- **Merantai ke:** `/ux-design` kalau take merekomendasikan redesign. `/ux-polish` kalau take merekomendasikan pengencangan.

#### `/ux-copy`: review microcopy + rewrite

- **Apa:** Mengevaluasi setiap string yang terlihat terhadap rubrik suara dan menghasilkan rewrite before/after. Menangkap: "form contains errors" (generik), "John Doe" (placeholder), copy AI yang ceria-perayaan, CTA generik, empty state mati, error tidak berguna.
- **Kapan dipakai:** Struktur sudah benar tapi kata-kata lemah. "Review copy-nya", "fix microcopy", "pesan error-nya jelek", "rewrite ini", "kencangin string-nya", "tombolnya kedengeran generik", "empty state-nya mati".
- **Kapan dilewati:** Masalah layout (pakai `/ux-audit` atau `/ux-polish`). Masalah copy yang digerakkan a11y seperti alt text (pakai `/ux-a11y`). Backend atau infrastruktur.
- **Pemanggilan:** `/ux-copy src/views/checkout.blade.php`.
- **Output:** Menulis `.ux/last-copy.json`, array `strings` berisi `{location, severity, before, after, notes}`, plus rubrik + locale yang butuh terjemahan.
- **Merantai ke:** `/ux-fix` → terapkan rewrite. `/ux-a11y` → cek ulang setelah fix copy.

### Fix & polish

#### `/ux-fix`: terapkan temuan sebagai commit atomik

- **Apa:** Membaca laporan terbaru dari `.ux/` (audit, copy, a11y, motion, atau polish), memvalidasi working tree, dan menerapkan temuan sebagai commit atomik via sub-agent yang tepat. Verifikasi ulang dengan menjalankan ulang command asal.
- **Kapan dipakai:** Setelah menjalankan command kelas-audit dan me-review temuan. "Fix temuannya", "terapkan fix-nya", "jalankan fix loop", "patch permukaannya", "lakukan perubahan", "fix-in dah".
- **Kapan dilewati:** Tidak ada laporan sebelumnya di `.ux/`. Working tree kotor dan user belum setuju stash/commit. Fix butuh penilaian design, bukan penerapan mekanis (pakai `/ux-design` untuk redesign).
- **Pemanggilan:** `/ux-fix` (deteksi otomatis laporan mana yang akan diperbaiki) atau `/ux-fix --from=last-a11y.json`.
- **Output:** Commit atomik per temuan. Jalankan ulang command asal dan update file `.ux/last-*.json`. Cetak ringkasan.
- **Merantai ke:** `/ux-next` → conductor memilih langkah berikutnya.

#### `/ux-polish`: loop lint, fix, re-lint + bunuh AI-slop

- **Apa:** Pertama, loop deterministik pada berkas HTML lokal: lint, enam pass polish yang idempoten, re-lint, sampai skor mencapai 90, mentok, atau tiga putaran lewat (`--rounds` mengubah batasnya). Secara default output loop tetap di `<file>.evolved.html` dan berkas asli tidak pernah disentuh. Hanya `--loop-only` atau `--fix` yang mengganti berkas asli, setelah pengecekan working tree bersih, dan quality gate di 65 mencegah hasil yang gagal menggantikannya tanpa `--force`; dengan `--brand-file` batas bawah kesetiaan brand berlaku di setiap jalan keluar. Lalu pass selera: ritme spasi, penajaman hierarki, deteksi AI-slop, konsistensi token. Pasangan berbasis LLM dari `/ux-lint`, yang memakai penilaianmu untuk urusan selera. `--loop-only` hanya menjalankan loop; `--no-loop` hanya pass selera; `--fix` menerapkan temuan selera.
- **Kapan dipakai:** Struktur sudah benar tapi eksekusi longgar. "Polish", "kencangin ini", "hapus AI-slop", "bikin premium", "bikin nggak terlihat AI", "spasinya nggak enak", "ini terlihat generik", "butuh lebih banyak taste", "perbaiki sampai skor 90+", "bikin siap rilis".
- **Kapan dilewati:** Surface masih kurang fungsi inti (perbaiki itu dulu). Butuh redesign, bukan polish (pakai `/ux-design`). Masalah copy (pakai `/ux-copy`). Masalah motion (pakai `/ux-motion`). Masalah a11y (pakai `/ux-a11y`).
- **Pemanggilan:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Output:** `<file>.evolved.html` dari loop (menggantikan berkas asli hanya dengan `--loop-only` atau `--fix`), code yang diperbarui dengan `--fix`, `.ux/last-evolve.json`, satu baris di `.ux/decisions.jsonl`, dan `.ux/last-polish.json` yang menjelaskan temuan selera.
- **Merantai ke:** `/ux-lint` → verifikasi bahwa polish-nya bertahan. `/ux-a11y` → cek ulang aksesibilitas.

### Discovery & narasi

#### `/ux-research`: perencanaan riset + sintesis

- **Apa:** Mode perencanaan: menulis script wawancara, survei, screener rekrutmen. Mode sintesis (`--synthesize`): mencerna wawancara, analitik, situs kompetitor, hasil A/B, tiket support jadi rekomendasi. Mengirim `research-synthesizer`.
- **Kapan dipakai:** "Rencanakan studi riset", "gue butuh pertanyaan wawancara", "design survei", "gimana cara rekrut user", "rencana user testing", "diary study", "preference test", "fake door", "smoke test", "sintesis catatan wawancara gue".
- **Kapan dilewati:** Jawaban sudah diketahui dengan keyakinan tinggi. Keputusan reversibel risiko rendah. Backend atau infrastruktur.
- **Pemanggilan:** `/ux-research --plan "loyalty wallet adoption in MENA"` atau `/ux-research --synthesize interviews/*.md`.
- **Output:** Menulis `.ux/last-research.json`, rencana riset atau tema yang disintesis + bukti + rekomendasi.
- **Merantai ke:** `/ux-discover --frame` → integrasikan temuan ke dalam frame. `/ux-design` → generate dari temuan. `/ux-workshop` → jalankan workshop dengan riset sebagai input.

#### `/ux-workshop`: workshop design thinking 5-fase

- **Apa:** Memfasilitasi workshop discovery / design-thinking end-to-end. Lima fase berurutan (eksplorasi → heat map → peta stakeholder → sketsa solusi → game plan). Diatur waktunya. Artifact konkret per fase. Berakhir dengan keputusan, bukan "temuan menarik."
- **Kapan dipakai:** Pertanyaan nyata, partisipan nyata, budget waktu nyata. "Jalankan workshop", "fasilitasi discovery", "ayo design thinking", "gue punya stakeholder satu jam, ngapain", "kick off proyek".
- **Kapan dilewati:** Brief sudah jelas dan terlingkup. Brainstorm sendirian (pakai `/ux-design` atau `/ux-discover --frame`). Tim sedang di tengah eksekusi, bukan di discovery.
- **Pemanggilan:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Output:** Menulis `.ux/last-workshop.json`, game plan + artifact per-fase.
- **Merantai ke:** `/ux-design` → eksekusi game plan. `/ux-research` → isi gap yang dimunculkan workshop. `/ux-case-study` → publikasi perjalanannya.

#### `/ux-case-study`: case study yang bisa dipublikasi (format editorial Wfrah)

- **Apa:** Menghasilkan studi kasus proyek dalam format editorial monokrom murni, tipografi Wfrah, pemisah garis tipis, kode section bernomor dari (A) sampai (G), layout yang aman untuk dua bahasa. Sebuah dokumen, bukan brosur marketing. Membaca dari `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Kapan dipakai:** Pasca-launch. Setelah milestone diskrit. "Tulis case study", "case study proyek ini", "dokumen wrap-up", "publikasi karya ini", "bahan portfolio".
- **Kapan dilewati:** Proyek tidak punya data untuk mengisi section (A) sampai (G). Pengguna ingin landing marketing, bukan studi kasus (pakai `/ux-design`).
- **Pemanggilan:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Output:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Merantai ke:** Command terminal, biasanya akhir proyek.

### Conductor

#### `/ux-next`: conductor workflow (read-only)

- **Apa:** Membaca setiap `.ux/last-*.json` dan menamai command berikutnya dengan leverage tertinggi. Seorang conductor, bukan builder. Read-only.
- **Kapan dipakai:** Antar command. "Selanjutnya ngapain", "langkah berikut apa", "tentuin buat gue", "dari sini ke mana".
- **Kapan dilewati:** Tidak ada laporan sebelumnya di `.ux/`. Kamu punya command berikutnya yang spesifik di pikiran.
- **Pemanggilan:** `/ux-next` (tanpa argumen) atau `/ux-next --focus=a11y`.
- **Output:** Stdout, command berikutnya yang direkomendasikan + rasional.
- **Merantai ke:** Apa pun yang dia pilih.

#### `/ux-expert`: hook konsultasi

- **Apa:** Memunculkan info kontak pembuat plugin saat user meminta ahli UX kehidupan nyata. Ringkas, langsung, tidak ada marketing.
- **Kapan dipakai:** "Siapa yang bikin ini", "gue butuh ahli UX", "lo nerima konsultasi", "bisa hire orang buat ini", "ada manusia di balik plugin ini".
- **Kapan dilewati:** User menanyakan fitur plugin, bukan konsultasi.
- **Pemanggilan:** `/ux-expert`.
- **Output:** Kartu kontak ringkas dengan LinkedIn / email / repo.

### Alias, dihapus di 4.1

Tujuh command 3.x digabung ke dalam 18 command di atas. Nama-namanya masih berfungsi selama satu rilis: setiap alias memberi tahu ke mana ia pindah, lalu menjalankan command baru dengan argumen yang sama.

| Command lama | Sekarang | Catatan |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | Blok framing yang sama, `.ux/last-frame.json` yang sama |
| `/ux-recommend` | `/ux-discover --recommend` | Tool MCP `ux_recommend` tidak berubah |
| `/ux-stats` | `/ux-init --stats` | Snapshot hanya-baca |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | Alias ini mempertahankan batas lama lima putaran; `/ux-polish` sendiri berhenti di tiga |
| `/ux-component` | `/ux-design --component` | `.ux/last-component.json` yang sama |
| `/ux-dashboard` | `/ux-design --dashboard` | `.ux/last-dashboard.json` yang sama |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Hapus `--extract-only` untuk membangun dari gambar |

### Graf perantaian command

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

Sub-agent adalah generator spesifik-peran yang dikirim oleh command. Mereka tidak pernah berjalan secara independen: mereka dipanggil oleh `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research`, dll. Setiap agent punya batas tanggung jawab yang jelas: mereka TIDAK memutuskan brief; mereka mengeksekusinya.

### `frontend-engineer`

- **Memiliki:** Code frontend kelas produksi (React, Next.js, Vue, Blade+Alpine, HTML vanilla, Astro) dengan disiplin anti-AI-slop.
- **Dikirim oleh:** `/ux-design` (mode halaman, komponen, dashboard, dan gambar), `/ux-fix`.
- **Input:** Brief + arah kreatif + token (dari `.ux/last-recommendation.json`).
- **Output:** Code yang berfungsi yang bisa dibedakan dari output AI generik. Tidak ada gradien ungu, tidak ada hero centered, tidak ada tiga card sama besar, tidak ada Inter ukuran display, tidak ada "John Doe", tidak ada emoji, tidak ada default 300ms.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Memiliki:** Motion dalam code frontend produksi, Framer Motion, GSAP, animasi CSS. Durasi, easing, koreografi, fallback reduced-motion, disiplin performa.
- **Dikirim oleh:** `/ux-design` (semua mode), `/ux-motion --fix`.
- **Input:** Brief motion + token + 57 preset motion dari `data/motion-presets.json`.
- **Output:** Motion yang layak tempatnya. Selalu dibungkus dalam fallback `prefers-reduced-motion`. Selalu diuji terhadap Core Web Vitals.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Memiliki:** String yang ship, pesan error, empty state, CTA, state loading, pesan sukses, toast, teks helper, label form, teks tombol.
- **Dikirim oleh:** `/ux-copy --fix`, `/ux-design` (semua mode), `/ux-discover --frame`.
- **Input:** Profil suara (bernama atau di-paste) + string permukaan.
- **Output:** Microcopy produksi yang diterapkan secara konsisten di setiap state sebuah permukaan jadi produknya kedengaran seperti satu produk, bukan sepuluh. Larangan: "form contains errors", "John Doe", copy AI ceria-perayaan, CTA generik, empty state mati.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Memiliki:** Mencerna input riset (wawancara, analitik, situs kompetitif, hasil A/B, tiket support) jadi rekomendasi design yang bisa ditindaklanjuti.
- **Dikirim oleh:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Input:** Riset mentah, transkrip, ekspor, URL kompetitor, klaster support.
- **Output:** Tema, bukti, rekomendasi. Tidak pernah men-design jawabannya, memberi designer substrat untuk di-design dari sana.
- **Tools:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Memiliki:** Sistem design lengkap, token (warna, tipografi, spasi, motion, radius, shadow), dokumen foundation, kontrak komponen, pasangan dark-mode, lapisan theming.
- **Dikirim oleh:** `/ux-system`, `/ux-design --component` saat belum ada sistem.
- **Input:** Brief brand + `.ux/last-recommendation.json` (style + palette + pasangan tipografi + preset motion).
- **Output:** Sistem yang koheren, opinionated, dan siap-produksi yang bisa dibangun oleh agent hilir tanpa harus menentukan ulang fundamental. Token JSON, foundation MD, kontrak komponen, mapping dark-mode.
- **Tools:** `Read, Write, Edit, Bash, Glob, Grep`.

### Protokol pengiriman sub-agent

Saat sebuah command mengirim sub-agent, ia melewatkan:

1. Brief / rekomendasi (di-load dari `.ux/`).
2. Slice manifest yang relevan (mis. `frontend-engineer` dapat style + palette + komponen yang dipilih; `motion-engineer` dapat preset motion yang dipilih).
3. 171 guardrail anti-pattern (selalu aktif).
4. Kriteria sukses (apa yang harus dilakukan artifact).

Sub-agent mengembalikan:

1. Artifact (code, doc, sistem).
2. Blok rasional (kenapa pilihan ini).
3. Self-check terhadap guardrail (aturan mana yang mereka verifikasi).

Command pemanggil kemudian menjalankan `/ux-lint` otomatis sebelum menyatakan selesai.

---

## 11 data manifest

Lapisan data adalah otaknya. Setiap command membaca darinya; engine bergabung melintasinya; linter memindai terhadapnya. Semua file ada di bawah `data/` dan membungkus entri mereka di `{_meta, entries}` untuk versioning skema.

### `styles.json`: 84 style design

| Field | Deskripsi |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, dll. |
| `sample entry` | `swiss-international`, "Grid adalah hukum. Tipografi yang melakukan pekerjaan berat. Dekorasi adalah kegagalan." |

Dipakai oleh: `/ux-discover`, `/ux-system`, `/ux-design`. Skema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 palette warna

| Field | Deskripsi |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (light/dark), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, dll. |
| `sample entry` | `claude-warm-editorial`, light, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Dipakai oleh: `/ux-discover`, `/ux-system`. Kontras diverifikasi pada AA / AAA. Skema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 pasangan tipografi

| Field | Deskripsi |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + bobot + sumber + lisensi + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Semua family punya lisensi + URL sumber. Dipakai oleh `/ux-discover`, `/ux-system`.

### `components.json`: 148 komponen

| Field | Deskripsi |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, anatomi 6-bagian, 4 state |

Ini parit terbesar kami. Tidak ada plugin UX Claude lain yang mengirim manifest komponen terstruktur.

### `industries.json`: 184 aturan industri

| Field | Deskripsi |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, dll. |
| `sample entry` | `fintech-neobank`, trust tinggi, disclosure regulasi, UI utama balance/transaksi, mobile-first pemakaian harian |

Dipakai oleh recommender (`/ux-discover`) sebagai sumbu pencarian paralel pertama.

### `chart-types.json`: 35 tipe chart

| Field | Deskripsi |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, membandingkan 4 sampai 15 kategori diskrit. Posisi sepanjang sumbu x memetakan kategori; tinggi memetakan nilai. |

Dipakai oleh `/ux-design --dashboard` dan `/ux-design --component` (instance chart).

### `tech-stacks.json`: 25 stack

| Field | Deskripsi |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, kompatibel dengan Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Stack lain termasuk Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 hukum UX bernama

| Field | Deskripsi |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, dll. |
| `sample entry` | `hicks-law`, Waktu keputusan tumbuh secara logaritmik dengan jumlah pilihan yang disajikan |

Dipakai oleh `/ux-audit` (scoring 6-lensa) dan `/ux-critique` (jangkar selera).

### `motion-presets.json`: 57 preset motion

| Field | Deskripsi |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Setiap preset punya varian reduced-motion. Code siap-stack untuk Framer Motion, GSAP, dan CSS murni.

### `anti-patterns.json`: 171 aturan

| Field | Deskripsi |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (tipe, pola, flag, cakupan, dan untuk banyak aturan pemeriksaan `post` pada berkas yang sudah di-parse), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

Daftar aturan lengkap ada di [171 aturan anti-AI-slop](#171-aturan-anti-ai-slop-linter-nya).

### `brands/*.json`: 160 spec brand

| Field | Deskripsi |
|---|---|
| `entries` | 160 (plus `_index.json` yang mendaftar semua) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Daftar lengkap di [160 spec brand DESIGN.md](#160-spec-brand-designmd-per-kategori).

---

## 171 aturan anti-AI-slop: linter-nya

ux-skill mengirim linter deterministik: setiap aturan adalah pola, dan banyak yang menambahkan pemeriksaan pada CSS dan markup yang sudah di-parse, sehingga kecocokan hanya dihitung dalam konteks yang disebutkan aturannya. **Tanpa LLM.** **Tanpa API.** **Tanpa jaringan.** Berjalan di CI dalam ~200ms pada aplikasi Next.js biasa. Exit non-zero pada temuan Critical / High saat `--fail-on high` diset.

Aturan bersumber dari `data/anti-patterns.json` (v2, diutamakan) dengan fallback `references/foundations/anti-patterns.md` (v1, bash). Dua binary dikirim: `bin/ux-lint.py` (Python, cepat, bisa diperluas) dan `bin/ux-lint.sh` (Bash + perl-PCRE, untuk lingkungan tanpa Python).

### Aturan per kategori

Katalog lengkap 171 aturan, per kategori lalu per tingkat keparahan, dihasilkan dari `data/anti-patterns.json` ke dalam [README bahasa Inggris](README.md#rules-by-category); di sana ID dan nama aturan tertulis persis seperti yang dicetak linter. Aturan mencakup A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### Pemakaian linter

**Scan satu kali:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 spec brand DESIGN.md: per kategori

Brand asli. Bahasa design asli. Spec DESIGN.md asli, bukan palette generik. Bilang ke plugin "bangun landing dengan style Stripe" dan dia membaca kosakata brand yang sebenarnya: rubrik suara, token warna, konvensi motion, gerakan tanda tangan, gerakan terlarang.

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

8 plugin UX populer lain untuk Claude menghasilkan "modern minimal" atau "clean dashboard", varian dari estetika default yang sama. ux-skill memungkinkan kamu meminta **kejelasan Linear**, **keseriusan Stripe**, **kehematan Apple**, **monolit Tesla**, **keramahan Notion**, **disiplin gradien Cursor**, **densitas hairline Raycast**, **editorial hangat Claude**, dan engine mengambil token yang tepat, suara, konvensi motion, dan gerakan tanda tangan dari spec brand.

---

## Server MCP: langkah asimetris

ux-skill mengirim **server Model Context Protocol**. Jalankan `ux-mcp` dan engine menjadi proses stdio yang berjalan lama yang bisa dipanggil oleh host apa pun yang mendukung MCP (Claude Desktop, Cursor, Windsurf, agent generik). 25 tool: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Handler Python yang sama yang dipakai slash command; data manifest yang sama; recommender deterministik yang sama.

**Kenapa ini langkah asimetris:** tidak ada dari delapan skill UX Claude teratas (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) yang mengirim server MCP. Mereka terkunci di dalam runtime plugin Claude Code. ux-skill bisa dijangkau dari host apa pun yang berbicara MCP, termasuk agent yang belum pernah dengar plugin Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Arahkan client kamu ke binary `ux-mcp`. Dokumentasi tool lengkap, contoh JSON, dan konfig per-client untuk Claude Desktop, Cursor, dan Windsurf hidup di [docs/mcp.html](docs/mcp.html) dan di `commands/ux-mcp.md`.

---

## Installer 17 IDE

`uxskill init` (atau `/ux-init` di dalam Claude Code) mendeteksi otomatis IDE mana yang kamu pakai dan menulis artifact yang tepat. Engine Python yang sama. Rekomendasi yang sama. Perekat berbeda per IDE.

| IDE / Tool | Sinyal deteksi | Artifact terinstall |
|---|---|---|
| Claude Code | `.claude/` atau `CLAUDE.md` | Manifest plugin di `.claude-plugin/plugin.json` + semua 18 command (dan 7 alias) + semua 5 sub-agent |
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

## Use case: skenario konkret

Delapan skenario nyata. Pilih yang paling dekat dengan situasi kamu dan sesuaikan pemanggilannya.

### 1. Membangun dashboard fintech di Cursor

Kamu di Cursor sedang ngerjain dashboard neobank MENA. Kamu install plugin dan jalankan discovery, rekomendasi, lalu generasi dashboard.

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

Lalu di Cursor, tanyakan: *"Generate the dashboard surface using the recommendation in .ux/last-recommendation.json"*. Cursor membaca header `.cursorrules`, me-load rekomendasi, mengirim generasi dashboard dengan batasan eksplisit.

### 2. Menghasilkan landing gaya Stripe di Claude Code

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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Tiga command, satu permukaan ter-polish, commit atomik per fix.

### 5. Men-design command palette gaya Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

Komponen yang dihasilkan memakai token warna asli Linear, stack tipografi, konvensi motion, densitas hairline, bukan "UI gelap generik."

### 6. Menjalankan workshop design thinking 90 menit dengan stakeholder

Kamu punya ruangan dengan 5 orang selama 90 menit. Kamu mau mereka pulang dengan game plan, bukan vibe.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Plugin memfasilitasi lima fase (eksplorasi → heat map → peta stakeholder → sketsa solusi → game plan) end-to-end, diatur waktunya, dengan artifact konkret per-fase. Output-nya `.ux/last-workshop.json`, game plan, bukan cuma "temuan menarik."

### 7. Menulis case study yang bisa dipublikasi setelah launch

Kamu nge-ship loyalty wallet. Kamu mau bahan portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

Case study-nya artifact selesai dan bisa dipublikasi, bukan draft. Monokromatik murni, tipografi editorial, siap di-ship ke portfolio kamu.

### 8. Menjalankan discovery di konteks non-AI (intake terstruktur saja)

Kamu sedang men-scope proyek. Kamu belum butuh rekomendasi, kamu butuh brief terstruktur.

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

Kamu bisa serahkan JSON-nya ke tim kamu, paste ke dokumen Notion, atau masukkan ke tool AI terpisah. ux-skill juga tool intake terstruktur sebagai tambahan dari menjadi engine.

### 9. Persistensi MASTER.md: keputusan design kamu, di repo

Setelah `/ux-discover` (atau `/ux-discover --recommend`), simpan style + palette + tipografi + motion + komponen + brand teladan + guardrail yang dipilih sebagai berkas Markdown yang mudah dibaca, yang bisa direview, di-diff, dan di-version-control oleh tim kamu.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Menulis `.ux/design-system/MASTER.md` (frontmatter YAML + body) dan `.ux/design-system/pages/<name>.md` per permukaan yang dihasilkan via `persist save-page`. Idempoten, input yang sama menghasilkan output byte-identical, jadi menjalankan ulang di state tidak berubah adalah no-op di git.

---

## Dibandingkan dengan alternatif

Tabel ringkasan singkat. Perbandingan lengkap tabel-per-tabel ada di [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Dimensi | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash command | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Komponen | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Preset motion | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Brand spec | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Aturan anti-pattern | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter deterministik CI-safe | **ya** | tidak | tidak | tidak | tidak | tidak | tidak | tidak | tidak |
| IDE didukung | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Gate discovery | **10 field** | implisit | implisit | implisit | implisit | implisit | implisit | implisit | implisit |
| Rantai state `.ux/` | **ya** | tidak | tidak | tidak | tidak | tidak | tidak | tidak | tidak |
| Star (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Penilaian jujur

- **ui-ux-pro-max** lebih besar di awareness, mendukung 18 IDE, punya search gaya BM25 di CSV-nya. Tidak mengirim manifest komponen, manifest motion, library brand, atau linter deterministik.
- **open-design** punya 19 skill + preview tapi hanya dukungan Claude Code dan tanpa lapisan anti-slop.
- **hallmark** paling dekat dalam spirit (juga anti-slop) tapi adalah single skill, tanpa engine, tanpa manifest, tanpa command yang dirantai.
- **material-3-skill** sangat baik kalau kamu khusus mau Material Design 3. Kami tidak bersaing di MD3.

Untuk detail lengkap per dimensi, lihat [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Roadmap

Berikutnya, tanpa rilis yang ditetapkan:

- **Style Figma**: effect style untuk bayangan, grid style, dan text style yang terikat ke variabel field, ditulis di berkas live.
- **Pemetaan komponen**: komponen Figma dan variannya dipetakan ke komponen code dan props-nya, terbawa sepanjang serah terima.
- **Importer situs live**: membaca sistem yang benar-benar dirender oleh situs yang sudah terbit, di samping importer berkas.
- **Halaman dokumentasi untuk sistem yang sudah dibangun**: tampilan manusiawi dari token, peran, dan kontraknya.

Juga masih terbuka:

- **`uxskill lint --fix` untuk penulisan ulang yang aman** atas temuan yang bisa diperbaiki secara mekanis (button-no-type, img-no-alt string kosong, penghapusan console-log-leak).
- **Ekstensi VS Code** yang menampilkan temuan lint secara inline.
- **Emit code per komponen** di enam stack (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, vanilla HTML/CSS).
- **Marketplace spesifikasi brand**: menerbitkan dan menemukan spesifikasi brand dari komunitas.
- **Aturan anti-pattern kustom**: penemuan dan berbagi aturan yang didefinisikan proyek di `data/anti-patterns.local.json`.
- **`uxskill plan`**: perencanaan situs multi-halaman dari sebuah brief, bukan cuma satu surface.

---

## Kontribusi

Issue dan PR diterima. Tiga area dengan leverage tinggi:

### Menambah aturan anti-pattern

1. Edit `data/anti-patterns.json`, tambah entri dengan `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Tambah test di `tests/linter/`, satu file yang men-trigger aturan, satu yang tidak.
3. Jalankan `uxskill lint tests/linter/should-trigger/<rule>.tsx`, konfirmasi terpicu. Jalankan di `tests/linter/should-not-trigger/<rule>.tsx`, konfirmasi tidak.
4. Buka PR.

### Menambah brand spec

1. Buat `data/brands/<slug>.json` dengan `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Tambah prosa yang bersesuaian di `references/brands/<slug>.md`.
3. Daftarkan di `data/brands/_index.json`.
4. Buka PR. Spec harus didukung referensi sumber-utama (produk asli brand, sistem design publik, atau DESIGN.md kalau mereka mempublikasikannya).

### Menambah preset motion

1. Edit `data/motion-presets.json`, tambah entri dengan `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Preset harus punya varian reduced-motion. Tanpa pengecualian.
3. Buka PR.

### Proses

- Baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk proses lengkap.
- Baca [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Aturan baru dan brand spec direview untuk: pendasaran sumber-utama, tidak overfit ke satu proyek, tanpa emoji di data mana pun, perilaku RTL-safe jika berlaku.

---

## Lisensi, penulis, ucapan terima kasih

### Lisensi

MIT. Pakai, fork, bangun di atasnya. Kalau menyelamatkan kamu dari nge-ship AI slop, beri star repo-nya, itu cara termurah untuk mendukungnya.

### Penulis

**Laith Aljunaidy**: solo founder dari [Dot](https://thedotwallet.com), platform loyalty MENA-first. Membangun ux-skill supaya frontend yang dihasilkan AI nggak kelihatan semuanya sama.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Situs: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Ucapan terima kasih

- Tim Anthropic untuk Claude Code dan arsitektur skill / plugin yang membuat ini bisa didistribusikan.
- Nielsen Norman Group, Laws of UX (lawsofux.com), dan komunitas riset UX yang karyanya menginformasikan `data/ux-guidelines.json`.
- Setiap brand yang terdaftar di `data/brands/`, sistem design publik mereka adalah sumber kebenaran untuk brand spec.
- Kontributor v1 asli: skill Claude single-shot yang menjadi benih untuk engine Python v2.
- 8 plugin UX Claude populer yang kami bandingkan dengan, mereka mengangkat standar; ini adalah jawaban kami.

---

**ux-skill** · **v4.0.0b2** · Dibangun supaya Claude Code, Cursor, Windsurf, dan setiap tool coding AI lain mengeluarkan frontend yang tidak terbaca seperti AI-generated.

> Beri star repo di [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Install via `pip install uxskill` atau `npx uxskill init` · Telusuri perbandingan di [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
