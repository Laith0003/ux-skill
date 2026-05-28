[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · **ไทย** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — เครื่องยนต์ปัญญาด้านการออกแบบสำหรับ Claude Code, Cursor และเครื่องมือเขียนโค้ดด้วย AI ทุกตัว

> **ปลั๊กอิน UX ที่แข็งแกร่งที่สุดสำหรับการเขียนโค้ดด้วย AI** แกนการให้เหตุผลภาษา Python พร้อมแมนิเฟสต์ JSON ที่ค้นหาได้ 11 ชุด (84 สไตล์, 176 พาเลตต์, 70 คู่ตัวอักษร, 148 คอมโพเนนต์, 184 อุตสาหกรรม, 35 ประเภทกราฟ, 57 พรีเซตการเคลื่อนไหว, 112 กฎ UX, 145 กฎ anti-pattern, 25 tech stack, 160 สเปกแบรนด์), 22 สแลชคอมมานด์, 5 ซับเอเจนต์ และลินเตอร์เชิงกำหนดต้านสลอป AI พร้อมรองรับข้าม IDE: ติดตั้งใน Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer และ Roo Cline

> **ชื่อแบรนด์คือ `ux-skill`** ชื่อแพ็กเกจ PyPI / npm ยังคงเป็น `uxskill` รีโป GitHub อยู่ที่ [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)

**เว็บไซต์:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **เปรียบเทียบกับปลั๊กอิน UX สำหรับ Claude ทุกตัว:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.0.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#ตัวติดตั้ง-17-ide)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### ประวัติดาว

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill คืออะไร

ux-skill เป็น **เครื่องยนต์ปัญญาด้านการออกแบบ** สำหรับเครื่องมือเขียนโค้ดด้วย AI ทำงานในรูปแบบแพ็กเกจ Python (`pip install uxskill`) ในรูปแบบปลั๊กอิน Claude Code และในรูปแบบตัวติดตั้งหลาย IDE สำหรับ 17 สภาพแวดล้อม เครื่องยนต์รับ brief ของโปรเจ็กต์ (อุตสาหกรรม กลุ่มเป้าหมาย โทน ข้อกำหนดที่ต้องมี ข้อห้าม สแตก พื้นที่) แล้วคืนระบบการออกแบบที่แนะนำแบบครบถ้วน: สไตล์ พาเลตต์ คู่ตัวอักษร พรีเซตการเคลื่อนไหว คอมโพเนนต์ แบรนด์ตัวอย่างที่ควรศึกษา และรั้วกัน anti-pattern ที่ต้องยึดถือ คำแนะนำเป็นเชิงกำหนด — อินพุตเดียวกันให้เอาต์พุตเดียวกันเสมอ

ปลั๊กอินวางตัวอยู่ระหว่างคุณกับเครื่องมือเขียนโค้ดด้วย AI เมื่อคุณขอ Claude Code, Cursor หรือผู้ช่วย AI อื่นๆ ให้ "สร้างหน้าแลนดิ้งฟินเทค" ผู้ช่วยมักจะด้นสด — และผลลัพธ์ก็ดูออกว่าเป็น AI ภายในห้าวินาที (กราเดียนต์จากม่วงไปฟ้า สามการ์ดเท่ากัน Inter ในขนาด display "John Doe" ในเทสติโมเนียล ทรานซิชันค่าเริ่มต้น 300ms ฮีโร่จัดกึ่งกลาง ลูกศร CTA เด้งขึ้นลง) ux-skill แทนที่การด้นสดด้วย **ข้อจำกัดเชิงโครงสร้าง**: คุณรัน `/ux-discover` เพื่อจับ brief, `/ux-recommend` เพื่อเลือกระบบ, `/ux-design` เพื่อสร้างโค้ด และ `/ux-lint` เพื่อยืนยันว่าผ่าน 145 กฎเชิงกำหนดต้านสลอป AI ก่อน commit

README นี้คือเอกสารอ้างอิงหลัก ทุกคอมมานด์ ทุกซับเอเจนต์ ทุกแมนิเฟสต์ข้อมูล ทุกเส้นทางการติดตั้ง ทุกสเปกแบรนด์ ทุกหมวด anti-pattern — มีบันทึกไว้ทั้งหมดที่นี่ หากคุณกำลังเลือกปลั๊กอินการออกแบบสำหรับ Claude Code หรือเปรียบเทียบเครื่องมือออกแบบด้วย AI สำหรับ Cursor, Windsurf หรือ Codex ให้อ่านเอกสารนี้ตั้งแต่ต้นจนจบควบคู่กับ [compare.html](https://uxskill.laithjunaidy.com/compare.html)

---

## สารบัญ

1. [ติดตั้งด่วน](#ติดตั้งด่วน)
2. [ตัวเลข — เปรียบเทียบสดกับ 8 สกิล UX อันดับต้นของ Claude](#ตัวเลข--เปรียบเทียบสดกับ-8-สกิล-ux-อันดับต้นของ-claude)
3. [สถาปัตยกรรม — ชิ้นส่วนเข้ากันได้อย่างไร](#สถาปัตยกรรม--ชิ้นส่วนเข้ากันได้อย่างไร)
4. [22 สแลชคอมมานด์ — การอ้างอิงโดยละเอียด](#22-สแลชคอมมานด์--การอ้างอิงโดยละเอียด)
5. [5 ซับเอเจนต์](#5-ซับเอเจนต์)
6. [11 แมนิเฟสต์ข้อมูล](#11-แมนิเฟสต์ข้อมูล)
7. [145 กฎต้านสลอป AI — ลินเตอร์](#145-กฎต้านสลอป-ai--ลินเตอร์)
8. [160 สเปก DESIGN.md แบรนด์ — แบ่งตามหมวด](#160-สเปก-designmd-แบรนด์--แบ่งตามหมวด)
9. [เซิร์ฟเวอร์ MCP — หมากอสมมาตร](#เซิร์ฟเวอร์-mcp--หมากอสมมาตร)
10. [ตัวติดตั้ง 17 IDE](#ตัวติดตั้ง-17-ide)
11. [กรณีใช้งาน — สถานการณ์รูปธรรม](#กรณีใช้งาน--สถานการณ์รูปธรรม)
12. [เปรียบเทียบกับทางเลือกอื่น](#เปรียบเทียบกับทางเลือกอื่น)
13. [แผนงาน](#แผนงาน)
14. [การมีส่วนร่วม](#การมีส่วนร่วม)
15. [ใบอนุญาต ผู้แต่ง คำขอบคุณ](#ใบอนุญาต-ผู้แต่ง-คำขอบคุณ)

---

## ติดตั้งด่วน

เส้นทางการติดตั้งสามทาง เลือกทางที่ตรงกับสภาพแวดล้อมของคุณ

### เส้นทางที่ 1 — มาร์เก็ตเพลส Claude Code (ทางหลัก)

ถ้าคุณใช้งานใน Claude Code ให้ติดตั้งผ่านมาร์เก็ตเพลสปลั๊กอิน:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

สิ่งนั้นจะเชื่อมต่อสแลชคอมมานด์ทั้ง 22 ตัวและซับเอเจนต์ทั้ง 5 ตัวเข้ากับเซสชัน Claude Code ของคุณ หลังติดตั้งให้รัน `/ux-init` เพื่อตั้งค่าไดเรกทอรีสถานะ `.ux/` ของแต่ละโปรเจ็กต์และยืนยันว่าเครื่องยนต์ Python เข้าถึงได้

### เส้นทางที่ 2 — pip (สากล)

ถ้าคุณทำงานนอก Claude Code (Cursor, Windsurf, CLI, CI) ให้ติดตั้งแพ็กเกจ Python:

```bash
pip install uxskill
uxskill init                       # ตรวจจับ IDE อัตโนมัติ ติดตั้ง artifact ที่ถูกต้อง
uxskill stats                      # พิมพ์จำนวนแมนิเฟสต์เพื่อยืนยันการติดตั้ง
uxskill lint .                     # รันลินเตอร์กับไดเรกทอรีปัจจุบัน
```

แพ็กเกจเผย `ux` และ `uxskill` เป็น entry point ของ CLI — เป็น binary ตัวเดียวกัน

### เส้นทางที่ 3 — npx (ไม่ต้องใช้ Python)

ถ้าคุณไม่อยากจัดการ Python โดยตรง ตัวห่อ npx จะ bootstrap ทุกอย่างผ่าน `pipx`:

```bash
npx uxskill init                  # ดาวน์โหลด pipx + uxskill ในการรันครั้งแรก
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### ยืนยันการติดตั้ง

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
#     "anti-patterns": 145,
#     "brands": 160
#   }
# }
```

ถ้ามีจำนวนใดคืน 0 หมายความว่าไฟล์ JSON หายไป — เปิด issue ที่ [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues)

---

## ตัวเลข — เปรียบเทียบสดกับ 8 สกิล UX อันดับต้นของ Claude

จำนวนดาวยืนยันล่าสุดผ่าน `gh api` เมื่อ **2026-05-28** ux-skill (Laith0003/ux-skill) เป็นผู้เข้ามาใหม่ล่าสุด — เราเล็กในด้านการรับรู้ แต่ลึกในด้านสถาปัตยกรรม การเปรียบเทียบด้านล่างซื่อสัตย์: เราแพ้ตรงไหน เราชนะตรงไหน

| ปลั๊กอิน | ดาว | สถาปัตยกรรม | สแลชคอมมานด์ | ลินเตอร์ (CI-safe) | สเปกแบรนด์ | คอมโพเนนต์ | พรีเซตการเคลื่อนไหว | IDE ที่รองรับ |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV, สกิลเดียว | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 สกิล + พรีวิว | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + รสนิยมที่อิงงานวิจัย | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | SKILL.md ขนาด 62 KB ไฟล์เดียว + สคริปต์ | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | ไลบรารีสกิลต่อ MCP | หลายตัว | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | สกิลแนวสวยงามแบบเดียว | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | สกิลออกแบบต้านสลอป | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | คอมโพเนนต์ MD3 + audit | 1 | — | (เฉพาะ MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **เครื่องยนต์ Python + 11 แมนิเฟสต์ + 22 คอมมานด์ + 5 ซับเอเจนต์ + ลินเตอร์ CI** | **22** | **145 กฎ regex** | **160** | **148** | **57** | **17** |

### ที่เราแพ้

- **การรับรู้** พวกเขามีดาวหลายแสน เรามี 14 ดวง ติดดาวให้เรา — เป็นวิธีช่วยที่ถูกที่สุด
- **การจดจำแบรนด์** ui-ux-pro-max และ open-design นำหน้ามาเป็นเดือน ไม่ใช่วัน
- **การขัดเกลาด้านการตลาด** พวกเขามีสกรีนช็อต วิดีโอเดโม และหน้าแลนดิ้งที่หาเจอง่าย เรามี README ที่ละเอียดและแลนดิ้งบางๆ

### ที่เราชนะ

- **ไลบรารีคอมโพเนนต์:** คอมโพเนนต์ 148 ตัวที่บันทึกไว้พร้อม anatomy สถานะ โทเค็นที่ใช้ และสเปกการเคลื่อนไหว ไม่มีใน 8 ปลั๊กอินอื่นที่ส่งแมนิเฟสต์คอมโพเนนต์
- **พรีเซตการเคลื่อนไหว:** 57 รายการพร้อมใช้แบ่งตามสแตก (Framer Motion, GSAP, CSS) พร้อม fallback แบบ reduced-motion ไม่มีตัวอื่นที่ส่งแมนิเฟสต์การเคลื่อนไหว
- **ลินเตอร์ anti-pattern:** 145 กฎ regex เชิงกำหนด รันใน CI ออกด้วยรหัสไม่ใช่ศูนย์ที่ Critical/High ไม่มีตัวอื่นที่ส่งลินเตอร์เชิงกำหนด
- **สเปกแบรนด์:** สเปก DESIGN.md จริง 160 รายการ (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude และอีก 117 แบรนด์) ไม่มีตัวอื่นที่ส่งไลบรารีแบรนด์
- **รองรับ 17 IDE:** เครื่องยนต์เดียวกัน กาวที่ต่างกันในแต่ละ IDE
- **22 สแลชคอมมานด์:** discovery, generation, audit, lint, polish, ลูปแก้ไข, case study, workshop, copy, motion, a11y, dashboard, conductor — บูรณาการครบถ้วน

ตารางเปรียบเทียบเคียงข้างกันเต็มรูปแบบที่ [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)

---

## สถาปัตยกรรม — ชิ้นส่วนเข้ากันได้อย่างไร

```
ux-skill (ชื่อแพ็กเกจ: uxskill)
│
├── data/                              สมอง — แมนิเฟสต์ JSON ที่ค้นหาได้
│   ├── styles.json                    84 สไตล์การออกแบบ + when/skip + โทเค็น
│   ├── palettes.json                  176 พาเลตต์ (สว่าง/มืด ยืนยันคอนทราสต์แล้ว)
│   ├── type-pairs.json                70 ทริปเล็ต display × body × mono
│   ├── components.json                148 คอมโพเนนต์ (anatomy สถานะ การเคลื่อนไหว)
│   ├── industries.json                184 กฎอุตสาหกรรม + สัญญาณกลุ่มเป้าหมาย
│   ├── chart-types.json               35 ประเภทกราฟ (when/skip การเข้ารหัส)
│   ├── tech-stacks.json               25 สแตก (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 กฎ UX ที่มีชื่อ (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 พรีเซตการเคลื่อนไหว (entry, exit, hover...)
│   ├── anti-patterns.json             145 กฎ regex (แหล่งลินเตอร์ CI-safe)
│   └── brands/*.json                  160 สเปก DESIGN แบรนด์ + _index.json
│
├── engine/                            Python — การให้เหตุผล
│   ├── recommender/                   เครื่องยนต์ merge 5-การค้นหาขนาน
│   ├── linter/                        ตัวสแกนต้านสลอปเชิงกำหนด
│   ├── discovery/                     โปรโตคอลบังคับ 10 ฟิลด์
│   ├── generator/                     ตัวปล่อยโทเค็น + แมนิเฟสต์
│   ├── installer/                     ตัวติดตั้งหลาย IDE 17 ตัว
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          22 สแลชคอมมานด์ Claude Code (.md)
│   ├── ux-init.md                     bootstrap
│   ├── ux-stats.md                    สแน็ปช็อตคลังข้อมูล
│   ├── ux-discover.md                 รับ 10 ฟิลด์ (ประตู)
│   ├── ux-recommend.md                เรือธง — ค้นหาขนาน 5 ทิศทาง
│   ├── ux-lint.md                     ลินเตอร์เชิงกำหนด
│   ├── ux-design.md                   สร้างโค้ดฟรอนต์เอนด์
│   ├── ux-component.md                สร้างคอมโพเนนต์หนึ่งตัว
│   ├── ux-system.md                   สร้างระบบการออกแบบเต็มรูปแบบ
│   ├── ux-dashboard.md                สร้างพื้นผิว dashboard
│   ├── ux-motion.md                   การจัดการการเคลื่อนไหว + audit
│   ├── ux-audit.md                    audit การออกแบบ 6 เลนส์
│   ├── ux-a11y.md                     audit WCAG 2.1 AA
│   ├── ux-critique.md                 วิจารณ์รสนิยม (3 ชนะ 3 พลาด 1 หมาก)
│   ├── ux-copy.md                     ทบทวน + เขียนใหม่ microcopy
│   ├── ux-fix.md                      นำผลการตรวจมาใช้เป็น commit อะตอม
│   ├── ux-polish.md                   พาสเครื่องสำอาง + ฆ่าสลอป AI
│   ├── ux-frame.md                    บล็อก framing 4 ฟิลด์
│   ├── ux-research.md                 วางแผน + สังเคราะห์งานวิจัย
│   ├── ux-workshop.md                 เวิร์กชอป design thinking 5 ระยะ
│   ├── ux-case-study.md               case study ตีพิมพ์ได้สไตล์ Wfrah-editorial
│   ├── ux-next.md                     วาทยกร workflow (อ่านอย่างเดียว)
│   └── ux-expert.md                   ตะขอที่ปรึกษา
│
├── agents/                            5 ซับเอเจนต์ (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy ในเสียงของแบรนด์
│   ├── research-synthesizer.md        สัมภาษณ์ + analytics + คู่แข่ง
│   └── design-system-architect.md     โทเค็น / คอมโพเนนต์ / รากฐาน
│
├── references/                        แหล่งข้อความสำหรับข้อมูล + หน้า demo
│   ├── foundations/                   anti-patterns.md หลักการ รสนิยม
│   ├── laws/                          กฎ UX แบบเต็ม
│   ├── process/                       discovery-protocol.md (หัวใจ)
│   ├── styles/                        ข้อความตามสไตล์ (anti-slop.md ฯลฯ)
│   ├── components/                    คอมโพเนนต์แบบเต็ม
│   ├── output/                        รูบริกผลลัพธ์
│   └── conditional/                   คำแนะนำเฉพาะสแตก
│
├── bin/
│   ├── uxskill.mjs                    ตัวห่อ npx -> เครื่องยนต์ Python
│   ├── ux-lint.py                     ลินเตอร์ v2 (แนะนำ)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (สร้างต่อโปรเจ็กต์)
    ├── last-discovery.json            สแน็ปช็อต brief
    ├── last-recommendation.json       ระบบที่เลือก
    ├── last-frame.json                บล็อก framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### เครื่องยนต์ทำงานจริงอย่างไร

1. **อินพุต** คุณให้ brief — แบบโต้ตอบผ่าน `/ux-discover` (10 ฟิลด์) หรือไม่โต้ตอบผ่าน flag ของ `ux recommend`
2. **5 การค้นหาขนาน** เครื่องยนต์รัน lookup ห้าตัวพร้อมกันบนแมนิเฟสต์:
   - **อุตสาหกรรม → recommended_styles** (industries.json)
   - **สไตล์ → ความเข้ากันได้ของพาเลตต์ + ตัวอักษร + การเคลื่อนไหว** (styles.json)
   - **โทน × ข้อกำหนดที่ต้องมี → ตัวกรองพาเลตต์** (palettes.json)
   - **สแตก → ความเข้ากันได้ของคอมโพเนนต์ + พรีเซตการเคลื่อนไหว** (tech-stacks.json, motion-presets.json)
   - **ข้อห้าม + พื้นที่ → รั้วกัน + รายชื่อย่อแบรนด์ตัวอย่าง** (anti-patterns.json, brands/)
3. **Merge** ตัว merger เชิงกำหนดจัดอันดับผู้สมัคร แก้ความขัดแย้ง (เช่น ข้อกำหนด dark-mode บังคับโหมดพาเลตต์) และปล่อยระบบที่แนะนำหนึ่งระบบ
4. **เอาต์พุต** เอกสาร JSON ที่มีสไตล์ที่เลือก พาเลตต์ที่เลือก คู่ตัวอักษร พรีเซตการเคลื่อนไหวอันดับ 5 อันแรก คอมโพเนนต์อันดับ 12 ตัวแรก แบรนด์ตัวอย่างอันดับ 5 แบรนด์แรก และรั้วกัน anti-pattern ทั้ง 145 ตัวที่เปิดใช้ พร้อมบล็อกอธิบายเหตุผลของแต่ละการเลือก
5. **การสร้าง** คอมมานด์ถัดมา (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) ใช้คำแนะนำเพื่อสร้างโค้ดจริงผ่านซับเอเจนต์
6. **การยืนยัน** `/ux-lint` สแกนโค้ดที่สร้างกับ 145 กฎ regex อีกครั้ง ออกด้วยรหัสไม่ใช่ศูนย์ที่ Critical/High ใน CI

**Python คิด HTML แสดง Markdown ร้อย**

---

## 22 สแลชคอมมานด์ — การอ้างอิงโดยละเอียด

ทุกคอมมานด์ส่งมาเป็นไฟล์ `.md` ใต้ `commands/` พร้อม `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` และ `output state file` คำอธิบายด้านล่างย่อมา; แหล่งโค้ดเต็มคือสเปกหลัก

คอมมานด์ถูกจัดเป็นห้ากลุ่ม: **bootstrap & คลังข้อมูล**, **discovery & คำแนะนำ**, **การสร้าง**, **audit & ยืนยัน**, **fix & polish** และ **วาทยกร**

### Bootstrap & คลังข้อมูล

#### `/ux-init` — bootstrap โปรเจ็กต์

- **คืออะไร:** ตรวจจับ IDE ที่คุณใช้ (`.claude/`, `.cursor/`, `.windsurf/` ฯลฯ) ติดตั้ง artifact ที่ถูกต้อง ยืนยันว่าเครื่องยนต์ Python เข้าถึงได้ พิมพ์สแน็ปช็อตสถิติ
- **ใช้เมื่อไหร่:** ติดตั้งครั้งแรกในโปรเจ็กต์ใหม่ หลังโคลนโปรเจ็กต์ที่ใช้ ux-skill หลัง `pip install --upgrade uxskill`
- **ข้ามเมื่อไหร่:** คุณรันในโปรเจ็กต์นี้แล้วและไม่มีอะไรเปลี่ยน
- **การเรียก:** `/ux-init` (ไม่มี args) หรือ `uxskill init` จาก CLI
- **เอาต์พุต:** artifact ต่อ IDE (ดู [ตัวติดตั้ง 17 IDE](#ตัวติดตั้ง-17-ide)) + ไดเรกทอรี `.ux/` + สรุปทาง stdout
- **ร้อยต่อ:** `/ux-discover` ต่อไป

#### `/ux-stats` — พิมพ์คลังข้อมูล

- **คืออะไร:** พิมพ์เวอร์ชัน + จำนวนรายการของแมนิเฟสต์ข้อมูล 11 ตัว เพื่อให้คุณยืนยันสิ่งที่ติดตั้งได้
- **ใช้เมื่อไหร่:** หลังติดตั้ง หลังอัปเกรด เมื่อ `/ux-recommend` คืนผลที่น่าประหลาดใจและคุณสงสัยว่าแมนิเฟสต์ไม่สมบูรณ์
- **ข้ามเมื่อไหร่:** ไม่ต้องข้าม — เป็นคอมมานด์อ่านอย่างเดียว 50ms
- **การเรียก:** `/ux-stats` หรือ `uxskill stats`
- **เอาต์พุต:** JSON ทาง stdout (ดู [ยืนยันการติดตั้ง](#ยืนยันการติดตั้ง) ด้านบน)
- **ร้อยต่อ:** วินิจฉัยอย่างเดียว ไม่ป้อนต่อไป

### Discovery & คำแนะนำ

#### `/ux-discover` — ฟังก์ชันบังคับ (รับ 10 ฟิลด์)

- **คืออะไร:** ขั้นรับ 10 ฟิลด์บังคับที่ทุกโปรเจ็กต์ต้องผ่านก่อนคอมมานด์สร้างใดๆ ประเภทโปรเจ็กต์ กลุ่มเป้าหมาย เป้าหมายหลัก โทน ข้อกำหนดที่ต้องมี ข้อห้าม แบรนด์อ้างอิง สแตก พื้นที่ ตัวชี้วัดความสำเร็จ **ไม่ด้นสด** วลีต้องห้าม ("modern", "clean") บังคับให้ผู้ใช้ระบุชัดเจน
- **ใช้เมื่อไหร่:** ก่อน `/ux-design`, `/ux-component`, `/ux-system` หรือ `/ux-dashboard` ใดๆ เมื่อ brief เก่าหมดอายุ
- **ข้ามเมื่อไหร่:** คุณกำลังแก้บั๊ก (`/ux-fix`) คุณรันแค่ลินเตอร์ (`/ux-lint`) brief ไม่เปลี่ยนจากเซสชันที่แล้ว
- **การเรียก:** `/ux-discover` ปลั๊กอินถาม คุณตอบ
- **เอาต์พุต:** เขียน `.ux/last-discovery.json` (brief 10 ฟิลด์)
- **ร้อยต่อ:** `/ux-recommend` → ใช้ discovery เลือกสไตล์ + พาเลตต์ + ตัวอักษร + การเคลื่อนไหว + คอมโพเนนต์ `/ux-design [brief เพิ่ม]` → สร้างโค้ดฟรอนต์เอนด์ยึดกับคำแนะนำ `/ux-component <ชื่อ>` → สร้างคอมโพเนนต์ที่สอดคล้องกับข้อจำกัดที่ค้นพบ

#### `/ux-recommend` — เครื่องยนต์เรือธง 5-การค้นหาขนาน

- **คืออะไร:** รัน 5-การค้นหาขนานของเครื่องยนต์ Python ผ่านแมนิเฟสต์ 11 ตัว และคืนระบบการออกแบบที่ merge มาแล้ว อุตสาหกรรม → สไตล์ → พาเลตต์ → ตัวอักษร → การเคลื่อนไหว + คอมโพเนนต์ + แบรนด์ตัวอย่าง + รั้วกัน
- **ใช้เมื่อไหร่:** เริ่มโปรเจ็กต์ใหม่จากศูนย์ pivot สินค้าที่ดูเหนื่อย เช็คก่อนบินก่อน `/ux-design` หรือ `/ux-component` ใดๆ
- **ข้ามเมื่อไหร่:** คุณรัน `/ux-discover` แล้วและบันทึก brief — `/ux-recommend` อัตโนมัติใน flow นั้น คุณกำลังแก้บั๊ก (ใช้ `/ux-fix`) คุณแค่ต้อง lint (ใช้ `/ux-lint`)
- **การเรียก (Claude Code):**
  ```
  /ux-recommend
  ```
  **การเรียก (CLI):**
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
- **เอาต์พุต:** เขียน `.ux/last-recommendation.json` — สไตล์ที่เลือก พาเลตต์ที่เลือก คู่ตัวอักษรที่เลือก พรีเซตการเคลื่อนไหวอันดับ 5 อันดับแรก คอมโพเนนต์ 12 ตัวแรก แบรนด์ตัวอย่าง 5 แบรนด์แรก รั้วกัน anti-pattern 145 ตัวเปิดใช้ พร้อมเหตุผล
- **ร้อยต่อ:** `/ux-design [brief]` → โค้ดฟรอนต์เอนด์ใช้โทเค็นที่แนะนำ `/ux-system` → ระบบการออกแบบเต็มจากคำแนะนำ `/ux-component <ชื่อ>` → คอมโพเนนต์หนึ่งตัวใช้สไตล์ที่แนะนำ `/ux-lint` → ยืนยันโค้ดที่สร้าง

### การสร้าง

#### `/ux-design` — สร้างพื้นผิวที่สวยงาม ต้านสลอป จาก brief

- **คืออะไร:** สร้าง artifact ฟรอนต์เอนด์คุณภาพ production ครบถ้วน (landing เว็บไซต์การตลาด app shell) จาก brief discovery + คำแนะนำ มอบหมาย `frontend-engineer` พร้อมทิศทางสร้างสรรค์จากตัวอ้างอิงต้านสลอปและคลังอาวุธ
- **ใช้เมื่อไหร่:** "Design a", "build me a", "generate a landing page", "create a dashboard", "make a component" — คำขอผลงานภาพแบบฟอร์มอิสระใดๆ
- **ข้ามเมื่อไหร่:** คุณต้องการรีวิว ไม่ใช่สร้าง (ใช้ `/ux-audit` หรือ `/ux-critique`) คุณต้องการแค่คอมโพเนนต์ (ใช้ `/ux-component`) งานแบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`
- **เอาต์พุต:** โค้ดที่สร้าง (HTML / Blade / JSX / Vue / Astro) พร้อม `.ux/last-design.json`
- **ร้อยต่อ:** `/ux-lint` → ยืนยันกับรั้วกัน `/ux-polish` → พาสเครื่องสำอาง `/ux-a11y` → audit การเข้าถึง `/ux-copy` → ทบทวน microcopy `/ux-fix` → นำผลตรวจมาใช้เป็น commit อะตอม

#### `/ux-component` — สร้างคอมโพเนนต์หนึ่งตัว

- **คืออะไร:** ผลิตคอมโพเนนต์เดี่ยวคุณภาพ production (ปุ่ม modal navbar sidebar การ์ด ตาราง ฟอร์ม กราฟ) จากสเปก ครบสี่สถานะปฏิสัมพันธ์ เข้าถึงได้ ตรงแบรนด์ ค้นหาคอมโพเนนต์ใน `.ux/last-recommendation.json` ก่อน fallback ไปที่ query แมนิเฟสต์โดยตรง
- **ใช้เมื่อไหร่:** คำขอ element เดี่ยวใดๆ — "build a button", "create a pricing card", "make a modal", "add a navbar", "design a sidebar", "I need a data table", "build a form", "make a chart component"
- **ข้ามเมื่อไหร่:** หน้าเต็มหรือพื้นผิวหลายส่วน (ใช้ `/ux-design`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`
- **เอาต์พุต:** โค้ดคอมโพเนนต์ที่สร้าง พร้อม `.ux/last-component.json`
- **ร้อยต่อ:** `/ux-lint` → ยืนยัน `/ux-polish` → กระชับ

#### `/ux-system` — สร้างระบบการออกแบบเริ่มต้นเต็มรูปแบบ

- **คืออะไร:** เสนอระบบการออกแบบเริ่มต้นเต็มรูปแบบสำหรับโปรเจ็กต์ที่ยังไม่มี — โทเค็น (สี ตัวอักษร space การเคลื่อนไหว radius shadow) เอกสาร foundation สัญญาคอมโพเนนต์ การจับคู่ dark-mode สวิตช์ theme มอบหมาย `design-system-architect`
- **ใช้เมื่อไหร่:** "We don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS"
- **ข้ามเมื่อไหร่:** โปรเจ็กต์มีระบบการออกแบบแล้ว — ใช้ `/ux-component` กับระบบที่มีอยู่ แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-system` (รัน discovery ก่อนถ้ายังไม่มี)
- **เอาต์พุต:** `tokens.json`, `foundations.md`, สัญญา `components/*.md` ปล่อย Tailwind / vanilla / SCSS ทางเลือก เขียน `.ux/last-system.json` สำหรับ chain context
- **ร้อยต่อ:** `/ux-component` → สร้างกับระบบใหม่ `/ux-design` → สร้างพื้นผิวใช้โทเค็นใหม่

#### `/ux-dashboard` — การสร้าง dashboard เฉพาะทาง

- **คืออะไร:** Dashboard ที่มีวินัยความหนาแน่นข้อมูล — เลย์เอาต์ bento ตัวเลข monospace ทรงตาราง รูปแบบ sparkline ต้านการใช้การ์ดเกินขนาด สีสถานะตามความหมาย การเคลื่อนไหวประหยัด ไม่ใช่หน้าการตลาดติดกราฟ
- **ใช้เมื่อไหร่:** "Build a dashboard", "design the admin panel", "make a metrics page", "operator console", "analytics view", "KPI board", "monitoring screen"
- **ข้ามเมื่อไหร่:** หน้าแลนดิ้งการตลาดที่มีสถิติ (ใช้ `/ux-design`) widget ตัวเดียว (ใช้ `/ux-component`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-dashboard`
- **เอาต์พุต:** โค้ด dashboard ที่สร้าง + `.ux/last-dashboard.json`
- **ร้อยต่อ:** `/ux-lint`, `/ux-audit`, `/ux-a11y`

#### `/ux-motion` — การจัดการการเคลื่อนไหว

- **คืออะไร:** สร้างชั้นการเคลื่อนไหวของพื้นผิว — ระยะเวลา easing ออกแบบท่าทาง fallback reduced-motion วินัยประสิทธิภาพ ยัง audit การเคลื่อนไหวที่มีอยู่ตาม 5 มิติ (timing, easing, ความหมาย, reduced-motion, ประสิทธิภาพ)
- **ใช้เมื่อไหร่:** "Motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "performance pass on the motion"
- **ข้ามเมื่อไหร่:** พื้นผิวไม่มีการเคลื่อนไหว (ใช้ `/ux-audit` หรือ `/ux-polish`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-motion path/to/component.tsx` (โหมด audit) หรือ `/ux-motion --generate hero-entry` (สร้าง)
- **เอาต์พุต:** โค้ดอัปเดต (ในโหมดสร้าง) หรือรายงาน `.ux/last-motion.json` (ในโหมด audit)
- **ร้อยต่อ:** `/ux-fix` → ใช้ผลตรวจการเคลื่อนไหว `/ux-polish` → กระชับ

### Audit & ยืนยัน

#### `/ux-lint` — ลินเตอร์อิง regex เชิงกำหนด (ไม่ใช้ LLM, CI-safe)

- **คืออะไร:** รัน 145 กฎ regex บนโค้ดของคุณ ไม่เรียก LLM ออกด้วยรหัสไม่ใช่ศูนย์ที่ Critical / High ใน CI แหล่ง: `data/anti-patterns.json` กฎครอบคลุม A11y (23) เนื้อหา (15) Layout (13) ตัวอักษร (10) สี (9) คุณภาพ (9) ภาพ (9) การเคลื่อนไหว (8) ประสิทธิภาพ (4)
- **ใช้เมื่อไหร่:** pre-commit hook ประตู CI พาสแรกที่เร็วบน codebase ใหญ่ก่อนเสียค่า `/ux-audit` หลัง `/ux-design` หรือ `/ux-component` เพื่อยืนยันการสร้าง
- **ข้ามเมื่อไหร่:** คุณต้องการลูปแก้ไข (ลินเตอร์รายงาน ไม่แก้ — ต่อเป็น `/ux-polish --fix` หรือ `/ux-fix`) คุณต้องการการตัดสินรสนิยม (ใช้ `/ux-critique`)
- **การเรียก (slash):** `/ux-lint src/`
- **การเรียก (CLI):** `uxskill lint .` หรือ `python3 bin/ux-lint.py .` หรือ `bash bin/ux-lint.sh --ci --fail-on high`
- **การเรียก (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **เอาต์พุต:** ผลตรวจทาง stdout (ตำแหน่ง id กฎ ความรุนแรง หลักฐาน) exit code 0 ถ้าสะอาด ไม่ใช่ศูนย์ที่ Critical/High เมื่อตั้ง `--fail-on high`
- **ร้อยต่อ:** `/ux-polish --fix` → คู่หูขับเคลื่อนด้วย LLM บนรูปแบบเดียวกัน `/ux-fix` → ใช้ผลตรวจเป็น commit จัดเรียงตามความรุนแรง `/ux-audit` → พาสให้เหตุผล 6 เลนส์เต็ม `/ux-next` → ให้วาทยกรตัดสิน

#### `/ux-audit` — audit การออกแบบ 6 เลนส์

- **คืออะไร:** รีวิวที่มีโครงสร้าง มีความเห็น เทียบกับ 6 เลนส์ (ความชัดเจน ลำดับชั้น การเข้าถึง เสียง การเคลื่อนไหว รสนิยม) ผลิตผลตรวจที่ติดป้ายความรุนแรง รายงานสไตล์ Polaris อ่าน `.ux/last-frame.json` ก่อน — กลุ่มเป้าหมายและผลลัพธ์ยึดความรุนแรงของแต่ละผลตรวจ
- **ใช้เมื่อไหร่:** พื้นผิวมีอยู่และคุณต้องการการวิจารณ์ที่ปกป้องได้ "Audit", "review the ux", "is this any good", "what's broken", "tear this apart"
- **ข้ามเมื่อไหร่:** พื้นผิวยังไม่มีอยู่ (ใช้ `/ux-design`) ผู้ใช้ต้องการเลนส์เดียว (ใช้คอมมานด์เป้าหมาย: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`) ผู้ใช้ต้องการความเห็นรสนิยม (ใช้ `/ux-critique`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-audit https://example.com/pricing` หรือ `/ux-audit src/components/Pricing.tsx`
- **เอาต์พุต:** เขียน `.ux/last-audit.json` — อาร์เรย์ `findings` ของ `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`
- **ร้อยต่อ:** `/ux-fix` → นำผลตรวจมาใช้ `/ux-polish` → พาสเครื่องสำอาง `/ux-design` → ถ้าต้องการ redesign เชิงโครงสร้าง

#### `/ux-a11y` — audit WCAG 2.1 AA + การตรวจมารยาททั่วไป

- **คืออะไร:** audit WCAG 2.1 AA ที่มีโครงสร้าง พร้อมการตรวจมารยาททั่วไปที่ผ่านเครื่องมืออัตโนมัติแต่ยังทำร้ายผู้ใช้จริง (การมองเห็น focus ความเฉพาะของ error การตั้งค่าการเคลื่อนไหว กับดักคีย์บอร์ด การพึ่งพาสี)
- **ใช้เมื่อไหร่:** ประตูการเข้าถึงก่อนส่ง หลัง redesign "Accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check"
- **ข้ามเมื่อไหร่:** ไม่ใช่ส่วนที่ผู้ใช้เห็น แบ็คเอนด์หรือโครงสร้างพื้นฐาน สเก็ตช์ work-in-progress
- **การเรียก:** `/ux-a11y https://example.com` (URL สดดีกว่า — เครื่องมืออัตโนมัติและการทดสอบคีย์บอร์ดทำงานเฉพาะตอนสด)
- **เอาต์พุต:** เขียน `.ux/last-a11y.json` — อาร์เรย์ `findings` ของ `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, อาร์เรย์ `beyond_wcag`, `severity_counts`
- **ร้อยต่อ:** `/ux-fix` → นำผลตรวจมาใช้เป็น commit `/ux-copy` → แก้ alt text และการต่อ error ของฟอร์มเป็นส่วนหนึ่งของพาส copy

#### `/ux-critique` — การเรียกรสนิยม (3 ชนะ 3 พลาด 1 หมากกลยุทธ์)

- **คืออะไร:** ความเห็นของนักออกแบบ — ไม่ใช่ audit เชิงโครงสร้าง ไม่ใช่คะแนนความรุนแรง แค่มุมมองที่กระชับ มีความเห็น ที่ระบุว่าอะไรใช้ได้ อะไรไม่ และหมากกลยุทธ์หนึ่งหมากที่จะเปลี่ยนแปลงมากที่สุด
- **ใช้เมื่อไหร่:** "What do you think", "is this good", "critique this", "honest take", "is the vibe right", "does this feel like us", "should we ship this"
- **ข้ามเมื่อไหร่:** ผู้ใช้ต้องการ audit เชิงโครงสร้างชัดเจน (ใช้ `/ux-audit`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-critique https://example.com`
- **เอาต์พุต:** เขียน `.ux/last-critique.json` — 3 ชนะ 3 พลาด 1 หมากกลยุทธ์ พร้อมข้อความ
- **ร้อยต่อ:** `/ux-design` ถ้ามุมมองแนะนำ redesign `/ux-polish` ถ้ามุมมองแนะนำกระชับ

#### `/ux-copy` — ทบทวน + เขียนใหม่ microcopy

- **คืออะไร:** ประเมินทุกสตริงที่เห็นเทียบกับรูบริกเสียง และผลิตการเขียนใหม่แบบก่อน/หลัง จับ: "form contains errors" (ทั่วไป) "John Doe" (placeholder) copy AI ฉลองสนุก CTA ทั่วไป empty state ตาย error ไร้ประโยชน์
- **ใช้เมื่อไหร่:** โครงสร้างถูกแต่คำอ่อนแอ "Review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "tighten the strings", "the buttons sound generic", "this empty state is dead"
- **ข้ามเมื่อไหร่:** ปัญหา layout (ใช้ `/ux-audit` หรือ `/ux-polish`) ปัญหา copy ที่ขับเคลื่อนด้วยการเข้าถึง เช่น alt text (ใช้ `/ux-a11y`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-copy src/views/checkout.blade.php`
- **เอาต์พุต:** เขียน `.ux/last-copy.json` — อาร์เรย์ `strings` ของ `{location, severity, before, after, notes}` พร้อมรูบริก + locales ที่ต้องแปล
- **ร้อยต่อ:** `/ux-fix` → ใช้การเขียนใหม่ `/ux-a11y` → ตรวจซ้ำหลังแก้ copy

### Fix & polish

#### `/ux-fix` — นำผลการตรวจมาใช้เป็น commit อะตอม

- **คืออะไร:** อ่านรายงานล่าสุดจาก `.ux/` (audit, copy, a11y, motion หรือ polish) ตรวจสอบ working tree และใช้ผลการตรวจเป็น commit อะตอมผ่านซับเอเจนต์ที่ถูกต้อง ยืนยันซ้ำโดยรันคอมมานด์ต้นทางอีกครั้ง
- **ใช้เมื่อไหร่:** หลังรันคอมมานด์คลาส audit และทบทวนผลตรวจ "Fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it"
- **ข้ามเมื่อไหร่:** ไม่มีรายงานก่อนหน้าใน `.ux/` working tree สกปรกและผู้ใช้ไม่ยอมให้ stash/commit การแก้ต้องการการตัดสินใจด้านการออกแบบ ไม่ใช่การใช้กลไก (ใช้ `/ux-design` สำหรับ redesign)
- **การเรียก:** `/ux-fix` (ตรวจอัตโนมัติว่าจะแก้รายงานไหน) หรือ `/ux-fix --from=last-a11y.json`
- **เอาต์พุต:** commit อะตอมต่อผลตรวจ รันคอมมานด์ต้นทางอีกครั้งและอัปเดตไฟล์ `.ux/last-*.json` พิมพ์สรุป
- **ร้อยต่อ:** `/ux-next` → วาทยกรเลือกการเคลื่อนไหวถัดไป

#### `/ux-polish` — พาสเครื่องสำอาง + ฆ่าสลอป AI

- **คืออะไร:** จังหวะ spacing เพิ่มคมลำดับชั้น ตรวจหาสลอป AI ความสม่ำเสมอของโทเค็น คู่หูขับเคลื่อนด้วย LLM ของ `/ux-lint` — ใช้การตัดสินใจของคุณในการเรียกรสนิยม
- **ใช้เมื่อไหร่:** โครงสร้างถูกแต่การลงมือหละหลวม "Polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste"
- **ข้ามเมื่อไหร่:** พื้นผิวขาดฟังก์ชันหลัก (แก้ตรงนั้นก่อน) ต้องการ redesign ไม่ใช่ polish (ใช้ `/ux-design`) ปัญหา copy (ใช้ `/ux-copy`) ปัญหา motion (ใช้ `/ux-motion`) ปัญหา a11y (ใช้ `/ux-a11y`)
- **การเรียก:** `/ux-polish src/components/Hero.tsx`
- **เอาต์พุต:** โค้ดอัปเดต + `.ux/last-polish.json` อธิบายการเปลี่ยนแปลง
- **ร้อยต่อ:** `/ux-lint` → ยืนยันว่า polish ยังอยู่ `/ux-a11y` → ตรวจการเข้าถึงซ้ำ

### Discovery & การเล่าเรื่อง

#### `/ux-frame` — บล็อก framing 4 ฟิลด์

- **คืออะไร:** จับ ใครเป็นเป้าหมาย ผลลัพธ์ สมมติฐาน และสัญญาณความสำเร็จ ในบล็อก framing ที่มีโครงสร้าง ไม่มีงานออกแบบเกิดขึ้น — แค่การรับสี่ฟิลด์ที่เปลี่ยนคำขอที่คลุมเครือให้เป็น brief ทำงาน เบากว่า `/ux-discover` (4 ฟิลด์ vs 10)
- **ใช้เมื่อไหร่:** ต้นโปรเจ็กต์ sprint หรือ engagement ครั้งเดียว กลางทางเมื่อการสนทนาเบี่ยงเบน "Frame this", "what's the brief", "set up the project", "framing"
- **ข้ามเมื่อไหร่:** framed แล้ว (ตรวจ `.ux/last-frame.json`) สร้างคอมโพเนนต์ครั้งเดียวที่ไม่มี implication ของ framing แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`
- **เอาต์พุต:** เขียน `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`
- **ร้อยต่อ:** `/ux-discover` → ขยาย frame เป็น brief 10 ฟิลด์ `/ux-design` → สร้างโดยใช้ frame เป็นจุดยึด

#### `/ux-research` — วางแผน + สังเคราะห์งานวิจัย

- **คืออะไร:** โหมดวางแผน: เขียนสคริปต์สัมภาษณ์ แบบสำรวจ ตัวกรองสรรหา โหมดสังเคราะห์ (`--synthesize`): ย่อยสัมภาษณ์ analytics เว็บคู่แข่ง ผล A/B ตั๋ว support เป็นคำแนะนำ มอบหมาย `research-synthesizer`
- **ใช้เมื่อไหร่:** "Plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes"
- **ข้ามเมื่อไหร่:** คำตอบทราบแล้วด้วยความมั่นใจสูง การตัดสินใจที่กลับได้ ความเสี่ยงต่ำ แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-research --plan "loyalty wallet adoption in MENA"` หรือ `/ux-research --synthesize interviews/*.md`
- **เอาต์พุต:** เขียน `.ux/last-research.json` — แผนงานวิจัยหรือธีมที่สังเคราะห์ + หลักฐาน + คำแนะนำ
- **ร้อยต่อ:** `/ux-frame` → รวมผลการตรวจเข้าใน frame `/ux-design` → สร้างจากผลการตรวจ `/ux-workshop` → รัน workshop โดยใช้งานวิจัยเป็นอินพุต

#### `/ux-workshop` — เวิร์กชอป design thinking 5 ระยะ

- **คืออะไร:** อำนวยความสะดวกเวิร์กชอป discovery / design-thinking ตั้งแต่ต้นจนจบ ห้าระยะตามลำดับ (สำรวจ → heat map → แผนที่ stakeholder → สเก็ตช์โซลูชัน → game plan) จำกัดเวลา artifact เป็นรูปธรรมต่อระยะ จบด้วยการตัดสิน ไม่ใช่ "ผลการตรวจที่น่าสนใจ"
- **ใช้เมื่อไหร่:** คำถามจริง ผู้ร่วมจริง งบเวลาจริง "Run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "kick off the project"
- **ข้ามเมื่อไหร่:** brief ชัดและขอบเขตแล้ว brainstorm คนเดียว (ใช้ `/ux-design` หรือ `/ux-frame`) ทีมอยู่กลางการลงมือ ไม่ใช่ discovery
- **การเรียก:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`
- **เอาต์พุต:** เขียน `.ux/last-workshop.json` — game plan + artifact ต่อระยะ
- **ร้อยต่อ:** `/ux-design` → ลงมือ game plan `/ux-research` → เติมช่องว่างที่ workshop ทำให้เห็น `/ux-case-study` → เผยแพร่การเดินทาง

#### `/ux-case-study` — case study ตีพิมพ์ได้ (รูปแบบ Wfrah-editorial)

- **คืออะไร:** สร้าง case study ของโปรเจ็กต์ในรูปแบบ editorial โมโนโครมบริสุทธิ์ — ตัวอักษร Wfrah เส้นแบ่ง hairline รหัส section ตามตัวเลข (A)–(G) เลย์เอาต์ที่ปลอดภัยสองภาษา เอกสาร ไม่ใช่โบรชัวร์การตลาด อ่านจาก `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`
- **ใช้เมื่อไหร่:** หลัง launch หลัง milestone แยก "Write a case study", "case study this project", "do the wrap-up doc", "publish this work", "portfolio piece"
- **ข้ามเมื่อไหร่:** โปรเจ็กต์ขาดข้อมูลเติม section (A)–(G) ผู้ใช้ต้องการ landing การตลาด ไม่ใช่ case study (ใช้ `/ux-design`)
- **การเรียก:** `/ux-case-study --format=html --slug=bashiti-loyalty`
- **เอาต์พุต:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`
- **ร้อยต่อ:** คอมมานด์ปลายทาง — มักเป็นจุดจบโปรเจ็กต์

### วาทยกร

#### `/ux-next` — วาทยกร workflow (อ่านอย่างเดียว)

- **คืออะไร:** อ่านทุก `.ux/last-*.json` และระบุชื่อคอมมานด์ถัดไปที่มีคานงัดสูงสุด วาทยกร ไม่ใช่ผู้สร้าง อ่านอย่างเดียว
- **ใช้เมื่อไหร่:** ระหว่างคอมมานด์ "What should I do next", "what's the next move", "decide for me", "where do we go from here"
- **ข้ามเมื่อไหร่:** ไม่มีรายงานก่อนหน้าใน `.ux/` คุณมีคอมมานด์ถัดไปเฉพาะในใจ
- **การเรียก:** `/ux-next` (ไม่มี args) หรือ `/ux-next --focus=a11y`
- **เอาต์พุต:** stdout — คอมมานด์ถัดไปที่แนะนำ + เหตุผล
- **ร้อยต่อ:** คอมมานด์ใดก็ตามที่เลือก

#### `/ux-expert` — ตะขอที่ปรึกษา

- **คืออะไร:** เผยข้อมูลติดต่อของผู้สร้างปลั๊กอินเมื่อผู้ใช้ถามถึงผู้เชี่ยวชาญ UX จริง สั้น ตรง ไม่ใช่การตลาด
- **ใช้เมื่อไหร่:** "Who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin"
- **ข้ามเมื่อไหร่:** ผู้ใช้ถามเรื่องฟีเจอร์ของปลั๊กอิน ไม่ใช่การให้คำปรึกษา
- **การเรียก:** `/ux-expert`
- **เอาต์พุต:** การ์ดติดต่อสั้นพร้อม LinkedIn / อีเมล / repo

### กราฟร้อยคอมมานด์

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  บล็อก framing 4 ฟิลด์
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  รับ 10 ฟิลด์ (ประตูบังคับ)
                  └────────────┬─────────┘
                               │ เขียน .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 การค้นหาขนาน -> ระบบ merged
                  └────────────┬─────────┘
                               │ เขียน .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ เขียน .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ เขียน .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  นำผลตรวจมาใช้เป็น commit
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artifact ตีพิมพ์ได้
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  วาทยกร — อ่านอย่างเดียว
                  │  /ux-expert          │  ตะขอที่ปรึกษา
                  └──────────────────────┘
```

---

## 5 ซับเอเจนต์

ซับเอเจนต์เป็นตัวสร้างเฉพาะบทบาทที่ถูกมอบหมายโดยคอมมานด์ ไม่เคยทำงานอิสระ — ถูกเรียกโดย `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research` ฯลฯ แต่ละเอเจนต์มีขอบเขตความเป็นเจ้าของที่ชัดเจน: พวกเขา ไม่ ตัดสิน brief; พวกเขาลงมือตาม brief

### `frontend-engineer`

- **เป็นเจ้าของ:** โค้ดฟรอนต์เอนด์คุณภาพ production (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro) ด้วยวินัยต้านสลอป AI
- **มอบหมายโดย:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`
- **อินพุต:** brief + ทิศทางสร้างสรรค์ + โทเค็น (จาก `.ux/last-recommendation.json`)
- **เอาต์พุต:** โค้ดที่ทำงานได้แยกแยะจาก output AI ทั่วไป ไม่มีกราเดียนต์ม่วง ไม่มีฮีโร่จัดกึ่งกลาง ไม่มีสามการ์ดเท่ากัน ไม่มี Inter ในขนาด display ไม่มี "John Doe" ไม่มีอีโมจิ ไม่มีค่าเริ่มต้น 300ms
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### `motion-engineer`

- **เป็นเจ้าของ:** การเคลื่อนไหวในโค้ดฟรอนต์เอนด์ production — Framer Motion, GSAP, CSS animation ระยะเวลา easing ออกแบบท่าทาง fallback reduced-motion วินัยประสิทธิภาพ
- **มอบหมายโดย:** `/ux-design`, `/ux-motion --fix`, `/ux-component`
- **อินพุต:** brief การเคลื่อนไหว + โทเค็น + 57 พรีเซตการเคลื่อนไหวจาก `data/motion-presets.json`
- **เอาต์พุต:** การเคลื่อนไหวที่สมควรมีที่ของมัน ห่อใน fallback `prefers-reduced-motion` เสมอ ทดสอบกับ Core Web Vitals เสมอ
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### `copy-writer`

- **เป็นเจ้าของ:** สตริงที่ส่ง — ข้อความ error empty state CTA loading state ข้อความสำเร็จ toast ข้อความช่วย label form ข้อความปุ่ม
- **มอบหมายโดย:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`
- **อินพุต:** โปรไฟล์เสียง (ตั้งชื่อหรือวาง) + สตริงของพื้นผิว
- **เอาต์พุต:** microcopy production ใช้อย่างสม่ำเสมอทุกสถานะของพื้นผิวเพื่อให้สินค้าฟังเหมือนสินค้าเดียว ไม่ใช่สิบ ห้าม: "form contains errors", "John Doe", copy AI ฉลองสนุก, CTA ทั่วไป, empty state ตาย
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### `research-synthesizer`

- **เป็นเจ้าของ:** ย่อยอินพุตงานวิจัย (สัมภาษณ์ analytics เว็บคู่แข่ง ผล A/B ตั๋ว support) เป็นคำแนะนำการออกแบบที่ลงมือได้
- **มอบหมายโดย:** `/ux-research`, `/ux-workshop`, `/ux-frame`
- **อินพุต:** งานวิจัยดิบ — transcript, export, URL คู่แข่ง, support cluster
- **เอาต์พุต:** ธีม หลักฐาน คำแนะนำ ไม่เคยออกแบบคำตอบ — ให้พื้นฐานแก่นักออกแบบเพื่อออกแบบจากนั้น
- **เครื่องมือ:** `Read, Write, WebFetch, Bash, Glob, Grep`

### `design-system-architect`

- **เป็นเจ้าของ:** ระบบการออกแบบเต็มรูปแบบ — โทเค็น (สี ตัวอักษร space การเคลื่อนไหว radius shadow) เอกสาร foundation สัญญาคอมโพเนนต์ การจับคู่ dark-mode ชั้น theming
- **มอบหมายโดย:** `/ux-system`, `/ux-component` เมื่อไม่มีระบบอยู่
- **อินพุต:** brief แบรนด์ + `.ux/last-recommendation.json` (สไตล์ + พาเลตต์ + คู่ตัวอักษร + พรีเซตการเคลื่อนไหว)
- **เอาต์พุต:** ระบบที่สอดคล้อง มีความเห็น พร้อม production ที่เอเจนต์ปลายน้ำสร้างต่อได้โดยไม่ต้องตัดสินใจพื้นฐานใหม่ โทเค็น JSON foundations MD สัญญาคอมโพเนนต์ การ map dark-mode
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### โปรโตคอลมอบหมายซับเอเจนต์

เมื่อคอมมานด์มอบหมายซับเอเจนต์ จะส่ง:

1. brief / คำแนะนำ (โหลดจาก `.ux/`)
2. ส่วนของแมนิเฟสต์ที่เกี่ยวข้อง (เช่น `frontend-engineer` ได้สไตล์ + พาเลตต์ + คอมโพเนนต์ที่เลือก; `motion-engineer` ได้พรีเซตการเคลื่อนไหวที่เลือก)
3. รั้วกัน anti-pattern 145 ตัว (เปิดใช้เสมอ)
4. เกณฑ์ความสำเร็จ (artifact ต้องทำอะไร)

ซับเอเจนต์คืน:

1. artifact (โค้ด เอกสาร ระบบ)
2. บล็อกเหตุผล (ทำไมเลือกแบบนี้)
3. การตรวจสอบตนเองเทียบกับรั้วกัน (กฎไหนที่ยืนยัน)

คอมมานด์ที่เรียกแล้วรัน `/ux-lint` อัตโนมัติก่อนประกาศเสร็จ

---

## 11 แมนิเฟสต์ข้อมูล

ชั้นข้อมูลคือสมอง ทุกคอมมานด์อ่านจากมัน เครื่องยนต์ merge ข้ามมัน ลินเตอร์สแกนกับมัน ทุกไฟล์อยู่ใต้ `data/` และห่อ entry ใน `{_meta, entries}` สำหรับ versioning schema

### `styles.json` — 84 สไตล์การออกแบบ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave ฯลฯ |
| `sample entry` | `swiss-international` — "Grid คือกฎ ตัวอักษรทำงานหนัก การประดับคือความล้มเหลว" |

ใช้โดย: `/ux-recommend`, `/ux-system`, `/ux-design` Schema: [data/SCHEMAS.md](data/SCHEMAS.md)

### `palettes.json` — 176 พาเลตต์สี

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (สว่าง/มืด), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark ฯลฯ |
| `sample entry` | `claude-warm-editorial` — สว่าง warm/editorial/magazine canvas #faf9f5 primary #cc785c |

ใช้โดย: `/ux-recommend`, `/ux-system` คอนทราสต์ยืนยันที่ AA / AAA Schema: [data/SCHEMAS.md](data/SCHEMAS.md)

### `type-pairs.json` — 70 คู่ตัวอักษร

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + น้ำหนัก + แหล่ง + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

ทุก family มี license + URL แหล่ง ใช้โดย `/ux-recommend`, `/ux-system`

### `components.json` — 148 คอมโพเนนต์

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Mega Navigation, Product Grid — anatomy 6 ส่วน 4 สถานะ |

นี่คือคูเมืองที่ใหญ่ที่สุดของเรา ไม่มีปลั๊กอิน UX Claude อื่นที่ส่งแมนิเฟสต์คอมโพเนนต์ที่มีโครงสร้าง

### `industries.json` — 184 กฎอุตสาหกรรม

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific ฯลฯ |
| `sample entry` | `fintech-neobank` — ความเชื่อใจสูง การเปิดเผยกฎระเบียบ UI หลักของยอด/ธุรกรรม mobile-first ใช้ประจำวัน |

ใช้โดย `/ux-recommend` เป็นแกนการค้นหาขนานแรก

### `chart-types.json` — 35 ประเภทกราฟ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical` — เปรียบเทียบ 4–15 หมวดแยก ตำแหน่งบนแกน x map หมวด ความสูง map ค่า |

ใช้โดย `/ux-dashboard`, `/ux-component` (อินสแตนซ์ chart)

### `tech-stacks.json` — 25 สแตก

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC เข้ากับ Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

สแตกอื่นมี Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025

### `ux-guidelines.json` — 112 กฎ UX ที่มีชื่อ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State ฯลฯ |
| `sample entry` | `hicks-law` — เวลาตัดสินใจเพิ่มแบบ logarithm ตามจำนวนตัวเลือกที่นำเสนอ |

ใช้โดย `/ux-audit` (การให้คะแนน 6 เลนส์) และ `/ux-critique` (จุดยึดรสนิยม)

### `motion-presets.json` — 57 พรีเซตการเคลื่อนไหว

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

ทุกพรีเซตมีตัวแปร reduced-motion โค้ดพร้อมใช้ตามสแตกสำหรับ Framer Motion, GSAP และ CSS บริสุทธิ์

### `anti-patterns.json` — 145 กฎ regex

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 145 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

รายการกฎเต็มอยู่ใน [145 กฎต้านสลอป AI](#145-กฎต้านสลอป-ai--ลินเตอร์)

### `brands/*.json` — 160 สเปกแบรนด์

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 160 (พร้อม `_index.json` ที่แจกแจงทั้งหมด) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

รายการเต็มใน [160 สเปก DESIGN.md แบรนด์](#160-สเปก-designmd-แบรนด์--แบ่งตามหมวด)

---

## 145 กฎต้านสลอป AI — ลินเตอร์

ux-skill ส่งลินเตอร์อิง regex เชิงกำหนด **ไม่ใช้ LLM** **ไม่ใช้ API** **ไม่ใช้เครือข่าย** รันใน CI ใน ~200ms บนแอป Next.js ทั่วไป ออกด้วยรหัสไม่ใช่ศูนย์เมื่อพบ Critical / High เมื่อตั้ง `--fail-on high`

กฎมาจาก `data/anti-patterns.json` (v2 แนะนำ) พร้อม fallback `references/foundations/anti-patterns.md` (v1 bash) ส่งสอง binary: `bin/ux-lint.py` (Python เร็ว ขยายได้) และ `bin/ux-lint.sh` (Bash + perl-PCRE สำหรับสภาพแวดล้อมที่ไม่มี Python)

### กฎตามหมวด

#### ตัวอักษร (3 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| high | `inter-as-display` | ใช้ Inter เป็นฟอนต์ display |
| medium | `hero-text-arbitrary-90px` | ขนาดฟอนต์ hero ตามอำเภอใจ |
| low | `font-system-only` | สแตกฟอนต์ระบบไม่มี typeface ที่เลือก |

#### สี (6 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| high | `purple-to-blue-gradient` | กราเดียนต์ AI ค่าเริ่มต้น ม่วงไปฟ้า |
| high | `dark-text-on-dark-card` | ข้อความคอนทราสต์ต่ำบนการ์ด |
| medium | `gradient-text-rainbow` | ข้อความกราเดียนต์หลายสต็อป |
| medium | `card-glow-purple-shadow` | เงาเรืองม่วงบนการ์ด |
| medium | `gradient-mesh-purple-pink` | ฮีโร่กราเดียนต์ mesh ม่วง-ชมพู |
| low | `tailwind-color-named-vague` | สี Tailwind ที่มีชื่อโดยไม่มี semantic token |

#### Layout (5 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| high | `three-equal-card-grid` | สามการ์ดเท่ากันในหนึ่งแถว |
| medium | `centered-everything-hero` | องค์ประกอบฮีโร่จัดกึ่งกลางทั้งหมด |
| medium | `avatar-stack-overlapping` | สแตกอวตารซ้อนทับทั่วไป |
| low | `pill-rounded-full-everywhere` | `rounded-full` ใช้กับทุกอย่าง |
| low | `nav-equal-hamburger-desktop` | เมนูแฮมเบอร์เกอร์บน desktop |

#### เนื้อหา (5 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum ในโค้ดส่ง |
| high | `emoji-in-ui` | อีโมจิใช้เป็น element UI |
| high | `icon-emoji-stamp` | อีโมจิใช้เป็น icon stamp |
| high | `testimonial-fake-five-stars` | เทสติโมเนียลห้าดาว hardcode |
| medium | `fake-name-john-doe` | ชื่อ placeholder ทั่วไป |

#### การเคลื่อนไหว (3 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | ลูกศรเด้งบน CTA |
| low | `timing-300ms-default` | timing transition ค่าเริ่มต้น 300ms |
| low | `cubic-bezier-material-only` | easing ค่าเริ่มต้น Material ทุกที่ |

#### A11y (6 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| high | `inline-svg-no-aria` | SVG ไม่มี aria-label หรือ aria-hidden |
| high | `img-no-alt` | รูปขาด attribute alt |
| high | `link-onclick-no-href` | anchor มี onClick แต่ไม่มี href |
| medium | `button-no-type` | button ขาด attribute type |
| medium | `heading-skip-h1-h3` | ข้ามระดับ heading |
| medium | `infinite-scroll-no-pagination` | infinite scroll ไม่มี fallback คีย์บอร์ด |

#### คุณภาพ (6 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| high | `console-log-leak` | `console.log` ในโค้ดคอมโพเนนต์ |
| medium | `inline-style-attribute` | attribute style แบบ inline |
| medium | `any-type-leak` | TypeScript type `any` |
| medium | `arbitrary-z-index-9999` | ค่า z-index ขี้เกียจ |
| low | `shadcn-default-everywhere` | บล็อกโทเค็น shadcn ค่าเริ่มต้นไม่แก้ |
| low | `todo-fixme-comment` | TODO หรือ FIXME ในโค้ดส่ง |

#### ภาพ (1 กฎ)

| ความรุนแรง | id กฎ | ชื่อ |
|---|---|---|
| low | `blur-bg-only-decoration` | backdrop blur โดยไม่มีพื้นผิว glass |

### การใช้ลินเตอร์

**สแกนครั้งเดียว:**

```bash
uxskill lint .
# หรือ
python3 bin/ux-lint.py src/
# หรือ
bash bin/ux-lint.sh src/
```

**ประตู CI (GitHub Actions):**

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

**เอาต์พุต (ตัวอย่าง):**

```
─── รายงาน /ux-lint ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  หลักฐาน: bg-gradient-to-br from-purple-500 to-blue-500
  แก้: แทนที่ด้วยกราเดียนต์ primary ของพาเลตต์ที่แนะนำหรือถอดกราเดียนต์ออก

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  หลักฐาน: grid grid-cols-3 gap-6 (3 Card children เท่ากัน)
  แก้: เน้นการ์ดหนึ่งใบ; ขนาบด้วยสองใบที่ลดการเน้น

3 ไฟล์ถูกสแกน · 2 high · 0 medium · 0 low · exit 1
แนะนำถัดไป: /ux-polish --fix (ขับเคลื่อนด้วย LLM จัดการทั้งผลตรวจที่ lint ได้และด้านสุนทรียะ)
```

---

## 160 สเปก DESIGN.md แบรนด์ — แบ่งตามหมวด

แบรนด์จริง ภาษาออกแบบจริง สเปก DESIGN.md จริง — ไม่ใช่พาเลตต์ทั่วไป บอกปลั๊กอินว่า "สร้างหน้าแลนดิ้งสไตล์ Stripe" แล้วมันอ่านคำศัพท์แบรนด์จริง: รูบริกเสียง โทเค็นสี ธรรมเนียมการเคลื่อนไหว หมากเซ็น หมากกีดกั้น

แต่ละแบรนด์ส่งเป็น JSON ที่มีโครงสร้าง (`data/brands/<slug>.json`) พร้อมเอกสารอ้างอิงข้อความ (`references/brands/<slug>.md`)

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

### ทำไมเรื่องนี้สำคัญ

ปลั๊กอิน UX Claude ยอดนิยมอีก 8 ตัวสร้าง "modern minimal" หรือ "clean dashboard" — เวอร์ชันของสุนทรียะค่าเริ่มต้นเดียวกัน ux-skill ให้คุณขอ **ความชัดเจนของ Linear**, **ความจริงจังของ Stripe**, **การยับยั้งชั่งใจของ Apple**, **โมโนลิธของ Tesla**, **ความเป็นมิตรของ Notion**, **วินัยกราเดียนต์ของ Cursor**, **ความหนาแน่นเส้น hairline ของ Raycast**, **editorial อบอุ่นของ Claude** — และเครื่องยนต์ดึงโทเค็น เสียง ธรรมเนียมการเคลื่อนไหว หมากเซ็นที่ถูกต้องจากสเปกแบรนด์

---

## เซิร์ฟเวอร์ MCP — หมากอสมมาตร

ux-skill ส่ง **เซิร์ฟเวอร์ Model Context Protocol** รัน `ux-mcp` และเครื่องยนต์กลายเป็น process stdio ที่รันยาวซึ่ง host ใดๆ ที่รองรับ MCP — Claude Desktop, Cursor, Windsurf, agent ทั่วไป — เรียกเข้ามาได้ สิบสี่ tool: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats` handler Python เดียวกับที่สแลชคอมมานด์ใช้ แมนิเฟสต์ข้อมูลเดียวกัน recommender เชิงกำหนดเดียวกัน

**ทำไมนี่เป็นหมากอสมมาตร:** ไม่มีสกิล UX Claude อันดับต้นแปดตัว (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ตัวใดที่ส่งเซิร์ฟเวอร์ MCP พวกมันถูกล็อกอยู่ใน runtime ปลั๊กอินของ Claude Code ux-skill เข้าถึงได้จาก host ใดๆ ที่พูด MCP รวมถึง agent ที่ไม่เคยได้ยินเรื่องปลั๊กอิน Claude Code

```bash
pip install 'uxskill[mcp]'             # mcp เป็น extra แบบ opt-in
ux-mcp                                  # เซิร์ฟเวอร์ stdio JSON-RPC เริ่มทำงาน
```

ชี้ client ของคุณไปยัง binary `ux-mcp` เอกสาร tool เต็ม ตัวอย่าง JSON และคอนฟิกต่อ client สำหรับ Claude Desktop, Cursor และ Windsurf อยู่ที่ [docs/mcp.html](docs/mcp.html) และใน `commands/ux-mcp.md`

---

## ตัวติดตั้ง 17 IDE

`uxskill init` (หรือ `/ux-init` ใน Claude Code) ตรวจจับ IDE ที่คุณใช้อัตโนมัติและเขียน artifact ที่ถูกต้อง เครื่องยนต์ Python เดียวกัน คำแนะนำเดียวกัน กาวต่าง IDE

| IDE / เครื่องมือ | สัญญาณตรวจจับ | artifact ที่ติดตั้ง |
|---|---|---|
| Claude Code | `.claude/` หรือ `CLAUDE.md` | แมนิเฟสต์ปลั๊กอินที่ `.claude-plugin/plugin.json` + ทุก 22 คอมมานด์ + ทุก 5 ซับเอเจนต์ |
| Cursor | `.cursor/` หรือ `.cursorrules` | header prompt `.cursorrules` ชี้ไปที่เครื่องยนต์ |
| Windsurf | `.windsurf/` หรือ `.windsurfrules` | `.windsurfrules` พร้อม header prompt เดียวกัน |
| GitHub Copilot | `.github/copilot-instructions.md` หรือ `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | patch `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` หรือ `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

ในทุก IDE คอมมานด์ CLI `uxskill recommend` / `uxskill lint` / `uxskill stats` เดียวกันทำงานจาก terminal เครื่องยนต์ Python เป็นแหล่งความจริง artifact ของ IDE เป็น header prompt บางๆ ที่นำเข้าไปยังมัน

---

## กรณีใช้งาน — สถานการณ์รูปธรรม

แปดสถานการณ์จริง เลือกตัวที่ใกล้กับสถานการณ์ของคุณที่สุดและปรับการเรียก

### 1. สร้าง dashboard ฟินเทคใน Cursor

คุณอยู่ใน Cursor ทำ dashboard neobank MENA คุณติดตั้งปลั๊กอินและรัน discovery, คำแนะนำ แล้วสร้าง dashboard

```bash
pip install uxskill
uxskill init                                # ตรวจจับ Cursor เขียน .cursorrules
uxskill discover                            # รับ 10 ฟิลด์
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

จากนั้นใน Cursor ถาม: *"Generate the dashboard surface using the recommendation in .ux/last-recommendation.json"* Cursor อ่าน header `.cursorrules` โหลดคำแนะนำ มอบหมายการสร้าง dashboard ด้วยข้อจำกัดที่ชัดเจน

### 2. สร้างหน้าแลนดิ้งสไตล์ Stripe ใน Claude Code

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

/ux-recommend
> [คืนสไตล์ พาเลตต์ คู่ตัวอักษร พรีเซตการเคลื่อนไหว คอมโพเนนต์ แบรนด์ตัวอย่างที่เลือก]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer สร้างหน้า]

/ux-lint .
> [ผ่าน — สเปกแบรนด์ Stripe ได้รับการเคารพ]
```

### 3. audit โค้ดที่มีอยู่หาสลอป AI ใน CI

คุณส่งแอป Next.js สองสัปดาห์ก่อน คุณต้องการพื้นแข็งต่อต้านลายนิ้วมือ AI ทุก PR

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

PR ที่นำกราเดียนต์ม่วงไปฟ้า Inter ที่ 96px เทสติโมเนียล "John Doe" หรือ emoji-as-icons มาจะ fail CI ไม่มีต้นทุน LLM ~200ms

### 4. polish พื้นผิวที่มีอยู่ที่ "รู้สึกเหมือน AI สร้าง"

คุณรับมรดกแอป React ที่ดูเหมือนเว็บ SaaS ที่ AI สร้างทุกอัน คุณอยากให้มันไม่ดูแบบนั้น

```
/ux-critique src/components/Hero.tsx
> [3 ชนะ 3 พลาด 1 หมากกลยุทธ์ — มุมมองซื่อสัตย์]

/ux-lint src/
> [15 ลายนิ้วมือ AI ระดับ high ถูกตั้งธง]

/ux-polish src/components/Hero.tsx
> [พาสเครื่องสำอางขับเคลื่อนด้วย LLM + ฆ่าสลอป AI]

/ux-fix
> [ใช้ผลตรวจเป็น commit อะตอม รันลินเตอร์อีกครั้ง]
```

สามคอมมานด์ หนึ่งพื้นผิวที่ polish แล้ว commit อะตอมต่อการแก้

### 5. ออกแบบ command palette สไตล์ Linear

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [อ่าน data/brands/linear.app.json สำหรับโทเค็น + หมากเซ็น]
> [อ่าน data/components.json สำหรับ anatomy + สถานะของ command-palette]
> [มอบหมาย frontend-engineer พร้อมสเปก Linear ชัดเจน]
```

คอมโพเนนต์ที่สร้างใช้โทเค็นสี สแตกตัวอักษร ธรรมเนียมการเคลื่อนไหว ความหนาแน่น hairline จริงของ Linear — ไม่ใช่ "dark UI ทั่วไป"

### 6. รันเวิร์กชอป design thinking 90 นาทีกับ stakeholder

คุณมีห้อง 5 คน 90 นาที คุณต้องการให้พวกเขาเดินออกพร้อม game plan ไม่ใช่ vibe

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

ปลั๊กอินอำนวยความสะดวกห้าระยะ (สำรวจ → heat map → แผนที่ stakeholder → สเก็ตช์โซลูชัน → game plan) ตั้งแต่ต้นจนจบ จำกัดเวลา พร้อม artifact ที่เป็นรูปธรรมต่อระยะ เอาต์พุตคือ `.ux/last-workshop.json` — game plan ไม่ใช่ "ผลการตรวจที่น่าสนใจ" อย่างเดียว

### 7. เขียน case study ตีพิมพ์ได้หลัง launch

คุณส่ง loyalty wallet คุณต้องการชิ้นงาน portfolio

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [อ่าน .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [สร้าง case study Wfrah-editorial พร้อม section ตามตัวเลข (A)-(G) เส้นแบ่ง hairline เลย์เอาต์ปลอดภัยสองภาษา]
> [เขียน case-studies/bashiti-loyalty.html]
```

case study เป็น artifact ที่เสร็จและตีพิมพ์ได้ — ไม่ใช่ดราฟต์ โมโนโครมบริสุทธิ์ ตัวอักษร editorial พร้อมส่งไปยัง portfolio ของคุณ

### 8. รัน discovery ในบริบทไม่ใช่ AI (แค่การรับที่มีโครงสร้าง)

คุณกำลังขอบเขตโปรเจ็กต์ คุณยังไม่ต้องการคำแนะนำ — คุณต้องการ brief ที่มีโครงสร้าง

```bash
uxskill discover
# รับ 10 ฟิลด์ บันทึกไปที่ .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

คุณสามารถส่ง JSON ให้ทีมของคุณ วางลงใน Notion doc หรือป้อนเข้า AI tool แยกต่างหาก ux-skill ยังเป็นเครื่องมือรับที่มีโครงสร้างนอกเหนือจากการเป็นเครื่องยนต์

### 9. MASTER.md ถาวร — การตัดสินใจออกแบบของคุณใน repo

หลัง `/ux-recommend` บันทึกสไตล์ + พาเลตต์ + ตัวอักษร + การเคลื่อนไหว + คอมโพเนนต์ + แบรนด์ตัวอย่าง + รั้วกันที่เลือกเป็นไฟล์ Markdown ที่มนุษย์อ่านได้ ที่ทีมของคุณรีวิว diff และ version-control ได้

```bash
python3 -m engine.cli.main persist save --project-root .
```

เขียน `.ux/design-system/MASTER.md` (YAML frontmatter + body) และ `.ux/design-system/pages/<name>.md` ต่อพื้นผิวที่สร้างผ่าน `persist save-page` Idempotent — อินพุตเดียวกันสร้างเอาต์พุตที่เหมือนกันทุก byte ดังนั้นการรันซ้ำบนสถานะที่ไม่เปลี่ยนเป็น no-op ใน git

---

## เปรียบเทียบกับทางเลือกอื่น

ตารางสรุปสั้น เปรียบเทียบตารางต่อตารางเต็มที่ [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)

| มิติ | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| สแลชคอมมานด์ | **22** | 1 | 19 | 1 | 1 | หลายตัว | 1 | 1 | 1 |
| คอมโพเนนต์ | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| พรีเซตการเคลื่อนไหว | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| สเปกแบรนด์ | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| กฎ anti-pattern | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ลินเตอร์เชิงกำหนด CI-safe | **ใช่** | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ |
| IDE รองรับ | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| ประตู discovery | **10 ฟิลด์** | implicit | implicit | implicit | implicit | implicit | implicit | implicit | implicit |
| chain สถานะ `.ux/` | **ใช่** | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ |
| ดาว (2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### การประเมินซื่อสัตย์

- **ui-ux-pro-max** ใหญ่กว่าในด้านการรับรู้ ส่ง 18 IDE มีการค้นหาสไตล์ BM25 บน CSV ของเขา ไม่ส่งแมนิเฟสต์คอมโพเนนต์ แมนิเฟสต์การเคลื่อนไหว ไลบรารีแบรนด์ หรือลินเตอร์เชิงกำหนด
- **open-design** มี 19 สกิล + พรีวิว แต่รองรับเฉพาะ Claude Code และไม่มีชั้นต้านสลอป
- **hallmark** ใกล้ที่สุดในจิตวิญญาณ (ต้านสลอปเช่นกัน) แต่เป็นสกิลเดียว — ไม่มีเครื่องยนต์ ไม่มีแมนิเฟสต์ ไม่มีคอมมานด์ที่ร้อยต่อ
- **material-3-skill** ยอดเยี่ยมถ้าคุณต้องการ Material Design 3 โดยเฉพาะ เราไม่แข่งใน MD3

สำหรับรายละเอียดเต็มต่อมิติ ดู [compare.html](https://uxskill.laithjunaidy.com/compare.html)

---

## แผนงาน

### v2.1 — ความครบถ้วนของลินเตอร์ (Q3 2026)

- **+17 กฎ anti-pattern ที่เลื่อน** เพื่อให้ครบ 52 เป้าหมาย: state hover dark-on-dark, การเข้ารหัสสถานะด้วยสีอย่างเดียว, การยก z-index ซ้ำซ้อน, breakpoint hardcode ใน JS, opacity แทน state disabled ฯลฯ
- **`uxskill lint --fix` สำหรับการเขียนใหม่ที่ปลอดภัย** ของผลตรวจที่แก้กลไกได้ (button-no-type, img-no-alt empty-string, ลบ console-log-leak)
- **VS Code extension** ที่นำผลตรวจ lint ขึ้นมา inline (ไม่ต้องรัน CI)

### v2.2 — ขยายแมนิเฟสต์คอมโพเนนต์ (Q4 2026)

- **+50 คอมโพเนนต์** เพื่อให้ครบ 198 ตัวใหม่ทั้งหมด: combobox พร้อม async filter, command-palette พร้อม heuristic recent-items, conditional-form-step, ตัวแปร payment-element, date picker ที่รู้ RTL, phone input เฉพาะ MENA, calendar grid พร้อม overlay hijri
- **การส่งโค้ดต่อคอมโพเนนต์** ใน 6 สแตก (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS บริสุทธิ์)
- **playground คอมโพเนนต์** ที่ uxskill.laithjunaidy.com/playground — ลองเครื่องยนต์คำแนะนำ + ดูพรีวิวคอมโพเนนต์สด

### v3 — มาร์เก็ตเพลส + การล็อกอิน (2027)

- **มาร์เก็ตเพลสสเปกแบรนด์** — เผยแพร่และค้นหาสเปกแบรนด์ของชุมชน จ่ายเพื่อเผยแพร่เพื่อสนับสนุน moderation
- **กฎ anti-pattern กำหนดเอง** — โปรเจ็กต์สามารถกำหนดกฎ regex ของตัวเองใน `data/anti-patterns.local.json` (ส่งแล้วใน v2; v3 เพิ่มการค้นพบ + การแชร์)
- **`uxskill plan`** — วางแผนเว็บไซต์หลายหน้าเต็มจาก brief ไม่ใช่แค่พื้นผิวเดียว
- **ความเทียบเท่าปลั๊กอิน Figma** — เครื่องยนต์คำแนะนำเดียวกัน นำขึ้นมาใน Figma

---

## การมีส่วนร่วม

issue และ PR ยินดีต้อนรับ สามพื้นที่คานงัดสูง:

### เพิ่มกฎ anti-pattern

1. แก้ `data/anti-patterns.json` — เพิ่ม entry พร้อม `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`
2. เพิ่มเทสต์ใน `tests/linter/` — ไฟล์หนึ่งที่ทริกเกอร์กฎ ไฟล์หนึ่งที่ไม่
3. รัน `uxskill lint tests/linter/should-trigger/<rule>.tsx` — ยืนยันว่ายิง รันบน `tests/linter/should-not-trigger/<rule>.tsx` — ยืนยันว่าไม่ยิง
4. เปิด PR

### เพิ่มสเปกแบรนด์

1. สร้าง `data/brands/<slug>.json` พร้อม `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`
2. เพิ่มข้อความที่สอดคล้องที่ `references/brands/<slug>.md`
3. ลงทะเบียนใน `data/brands/_index.json`
4. เปิด PR สเปกต้องถูก backed ด้วยการอ้างอิงแหล่งหลัก (ผลิตภัณฑ์จริงของแบรนด์ ระบบการออกแบบสาธารณะ หรือ DESIGN.md ถ้าพวกเขาเผยแพร่)

### เพิ่มพรีเซตการเคลื่อนไหว

1. แก้ `data/motion-presets.json` — เพิ่ม entry พร้อม `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`
2. พรีเซตต้องมีตัวแปร reduced-motion ไม่มีข้อยกเว้น
3. เปิด PR

### กระบวนการ

- อ่าน [CONTRIBUTING.md](CONTRIBUTING.md) สำหรับกระบวนการเต็ม
- อ่าน [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- กฎและสเปกแบรนด์ใหม่ถูกรีวิวสำหรับ: การยึดแหล่งหลัก ไม่ overfit กับโปรเจ็กต์เดียว ไม่มีอีโมจิในข้อมูลใดๆ พฤติกรรมปลอดภัย RTL เมื่อนำไปใช้ได้

---

## ใบอนุญาต ผู้แต่ง คำขอบคุณ

### ใบอนุญาต

MIT ใช้ fork สร้างต่อจากมัน ถ้ามันช่วยคุณจากการส่งสลอป AI ติดดาวให้ repo — เป็นวิธีสนับสนุนที่ถูกที่สุด

### ผู้แต่ง

**Laith Aljunaidy** — ผู้ก่อตั้งคนเดียวของ [Dot](https://thedotwallet.com) แพลตฟอร์ม loyalty MENA-first สร้าง ux-skill เพื่อให้ฟรอนต์เอนด์ที่ AI สร้างไม่ดูเหมือนกันหมด

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- อีเมล: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- เว็บไซต์: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### คำขอบคุณ

- ทีม Anthropic สำหรับ Claude Code และสถาปัตยกรรม skill / plugin ที่ทำให้สิ่งนี้แจกจ่ายได้
- Nielsen Norman Group, Laws of UX (lawsofux.com) และชุมชนวิจัย UX ที่ผลงานของพวกเขาช่วยให้ข้อมูล `data/ux-guidelines.json`
- ทุกแบรนด์ที่ระบุใน `data/brands/` — ระบบการออกแบบสาธารณะของพวกเขาคือแหล่งความจริงสำหรับสเปกแบรนด์
- ผู้สนับสนุน v1 ดั้งเดิม: สกิล Claude แบบช็อตเดียวที่กลายเป็นเมล็ดพันธุ์สำหรับเครื่องยนต์ Python v2
- ปลั๊กอิน UX Claude ยอดนิยม 8 ตัวที่เราเปรียบเทียบด้วย — พวกเขายกระดับมาตรฐาน นี่คือคำตอบของเรา

---

**ux-skill** · **v2.0.0-alpha.1** · สร้างเพื่อให้ Claude Code, Cursor, Windsurf และเครื่องมือเขียนโค้ดด้วย AI ทุกตัวอื่นๆ ส่งออกฟรอนต์เอนด์ที่ไม่อ่านเหมือน AI สร้าง

> ติดดาว repo ที่ [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · ติดตั้งผ่าน `pip install uxskill` หรือ `npx uxskill init` · เปรียบเทียบที่ [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
