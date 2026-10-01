[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · **ไทย** · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: เครื่องยนต์ปัญญาด้านการออกแบบสำหรับ Claude Code, Cursor และเครื่องมือเขียนโค้ดด้วย AI ทุกตัว

**เครื่องยนต์ปัญญาด้านการออกแบบที่ทำให้ UI ที่ AI สร้างมีเอกลักษณ์ ไม่ใช่หน้าตาจืดๆ เหมือนกันหมด** ใส่ลงในเครื่องมือเขียนโค้ดด้วย AI ตัวไหนก็ได้จาก 17 ตัว แล้วผลงานของคุณจะไม่ดูเหมือน AI ทำอีกต่อไป ฟรี MIT ออฟไลน์ ไม่ใช้ LLM

```bash
pip install uxskill
```

**[กดดาวให้ ux-skill บน GitHub](https://github.com/Laith0003/ux-skill)** ถ้ามีประโยชน์ นี่คือวิธีที่ง่ายที่สุดในการช่วยโปรเจ็กต์ มาใหม่หรือ เริ่มจาก[ทัวร์ 60 วินาที](#ติดตั้งด่วน) หรือดูของจริงที่ [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)

![ก่อน: hero ภาพสต็อกแบบเดิมๆ ไล่สีม่วงอ่อน ไม่มีตัวตนของแบรนด์ หลัง: ภาพไซต์ก่อสร้างจริงใต้ชั้นมืด หัวข้อแบบงานบรรณาธิการเน้นด้วยสีอำพัน และฟอร์มขอใบเสนอราคาอยู่ใน hero prompt เดียวกัน แต่ผลต่างออกไปเมื่อ ux-skill เป็นผู้กำหนดข้อจำกัด](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*ก่อน: SEO slop ภาพสต็อกแบบเดิมๆ หลัง: hero ภาพก่อสร้างจริงใต้ชั้นมืด หัวข้อแบบงานบรรณาธิการเน้นสีอำพัน ฟอร์มขอใบเสนอราคาใน hero เครื่องมือเขียนโค้ดด้วย AI ตัวเดิม prompt เดิม แต่ผลต่างออกไปเมื่อ ux-skill เป็นผู้กำหนดข้อจำกัด*

> **v4.0, FOUNDATIONS: คำสั่งเดียวสร้างระบบดีไซน์ที่ครบและผ่านการตรวจตาม WCAG พร้อมรองรับภาษาอาหรับและการเขียนจากขวาไปซ้ายในตัว** ปลั๊กอิน UX ที่แข็งแกร่งที่สุดสำหรับการเขียนโค้ดด้วย AI แกนการให้เหตุผลด้วย Python พร้อมตัวสังเคราะห์ 7 แกนแบบกำหนดผลได้ manifest JSON ที่ query ได้ 12 ชุด (84 สไตล์ 176 พาเลตต์ 70 คู่ตัวอักษร 148 คอมโพเนนต์ 184 อุตสาหกรรม 35 ประเภทกราฟ 57 พรีเซ็ตการเคลื่อนไหว 112 กฎ UX 171 กฎ anti-pattern 25 tech stack 160 สเปกแบรนด์) 18 สแลชคอมมานด์ 5 ซับเอเจนต์ 25 เครื่องมือ MCP และลินเตอร์ต้าน AI slop แบบกำหนดผลได้ ข้าม IDE: ติดตั้งได้ใน Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer และ Roo Cline

> **ชื่อแบรนด์คือ `ux-skill`** ชื่อแพ็กเกจบน PyPI / npm ยังคงเป็น `uxskill` รีโพ GitHub อยู่ที่ [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill)

**ผู้สร้าง:** [Laith Aljunaidy](https://laithjunaidy.com) นักออกแบบและ CTO ในอัมมาน · **เว็บไซต์:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **เทียบกับปลั๊กอิน UX ของ Claude ทุกตัว:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#ตัวติดตั้ง-17-ide)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### ใหม่ใน 4.0: รากฐาน

ใส่สีแบรนด์หนึ่งสี ได้ระบบดีไซน์ทั้งชุด และคอนทราสต์ถูกตรวจแล้วก่อนถึงมือคุณ

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

ต้องใช้ Python 3.10 ขึ้นไป สำหรับเซิร์ฟเวอร์ MCP ใช้ `pip install --upgrade 'uxskill[mcp]'` ถ้าใช้ pipx ใช้ `pipx install uxskill` (ถ้ามี 3.x ติดตั้งอยู่แล้ว ใช้ `pipx upgrade uxskill`) ถ้าใช้ npm ใช้ `npx uxskill@latest` ย้ายมาจาก 3.x หรือ [คู่มือการย้าย](docs/migrating-to-4.md)จับคู่ทุก token ของ 3.x เข้ากับบทบาทใน 4.0

**กำลังสร้างผลิตภัณฑ์หรือหน้าแลนดิ้งอยู่หรือ** คุณจะได้ `tokens.css` สำหรับลิงก์จากหน้าเว็บ `fonts.css` ที่มีฟอนต์สำรองซึ่งปรับเมตริกให้ตรงกับฟอนต์ที่เลือก `fonts-self-host.css` ที่โหลดฟอนต์จากไฟล์ของคุณเอง `tokens.json` สำหรับเครื่องมือต่างๆ งานกราฟิกตกแต่งของแบรนด์ใน `art/` และ `system-report.md` ที่อธิบายด้วยภาษาง่ายๆ ว่าสร้างอะไร เพราะอะไร และควรเริ่มจากการจัดหน้าแบบไหน ใส่สไตล์ด้วยบทบาท (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`) และสลับโหมดมืด คอนทราสต์สูง ระยะห่างกระชับ ขวาไปซ้าย หรือลดการเคลื่อนไหว ได้ด้วย attribute เดียวบน `<html>` โหลดฟอนต์ด้วยลิงก์ Google Fonts ที่รายงานให้มา หรือด้วย `fonts-self-host.css` และโฟลเดอร์ `fonts/` แล้วลิงก์ `fonts.css` คู่กับวิธีใดก็ได้ ก่อน `tokens.css` และอย่าแก้ไขทั้งสองไฟล์ เมื่อใช้ `--brief` หน้าตาจะตามอุตสาหกรรมและน้ำเสียงเมื่อบรีฟระบุไว้ และฟิลด์แบบมีโครงสร้าง (อายุ ภาษา โหมดเริ่มต้น บริบทการอ่าน) จะกำหนดขนาดตัวอักษร พื้นที่แตะ ระบบตัวเขียน และโหมดที่เปิดขึ้นมาก่อน discovery ไม่ถามอุตสาหกรรม ดังนั้น `/ux-system create` จะถามเอง ใน Claude Code `/ux-system create` จะตรวจเวอร์ชันที่ติดตั้ง รันการบิลด์ และอธิบายรายงาน

**กำลังออกแบบระบบดีไซน์อยู่หรือ** รากฐานเก้าด้าน (สี ตัวอักษร ระยะห่าง เลย์เอาต์ มุมโค้ง เส้นขอบ ระดับความลึก การเคลื่อนไหว ภาพ) แต่ละด้านเปลี่ยนอย่างต่อเนื่องตามเจ็ดแกน มีทั้ง primitive และบทบาทเชิงความหมาย ในรูปแบบ W3C design tokens (DTCG 2025.10) พร้อมค่าของทุกโหมด อินพุตเดิม ได้ไบต์เดิม ผ่าน MCP `ux_system_build` จะคืนรายงาน ผลการตรวจ และขนาดของแต่ละไฟล์ และเมื่อส่ง `out` จะเขียนไฟล์ชุดเดียวกับคำสั่ง

- **ด่านตรวจ WCAG** ทุกคู่สีของข้อความ ตัวควบคุม และโฟกัส ถูกวัดทั้งโหมดสว่างและมืด ที่คอนทราสต์ปกติและสูง: WCAG 1.4.3 (ข้อความ 4.5:1) และ 1.4.11 (สิ่งที่ไม่ใช่ข้อความ 3:1) ที่คอนทราสต์ปกติ WCAG 1.4.6 (ข้อความ 7:1) ที่คอนทราสต์สูง และยังมีเกณฑ์ขั้นต่ำ 4.5:1 ที่คอนทราสต์สูงสำหรับส่วนที่ไม่ใช่ข้อความส่วนใหญ่ ซึ่งเป็นเกณฑ์ของเราเอง เพราะ WCAG ไม่ได้กำหนดระดับเข้มข้นสำหรับสิ่งที่ไม่ใช่ข้อความ ระบบที่ไม่ผ่านจะไม่ถูกเขียน และข้อความแจ้งจะบอกว่าต้องแก้อะไร
- **ปลอดภัยเป็นค่าเริ่มต้น** ไม่เขียนทับไฟล์ที่มีเนื้อหาต่างไปเด็ดขาด `--force` จะแทนที่ไฟล์เฉพาะเมื่อคุณสั่ง
- **ภาษาอาหรับ** ภายใต้ `dir="rtl"` ข้อความจะเปลี่ยนไปใช้ฟอนต์อาหรับที่มีขนาดและความสูงบรรทัดของตัวเอง ระยะห่างใช้ logical property และการเคลื่อนไหวกลับด้าน `--latin-only` จะตัดส่วนนี้ออก

**ระบบที่คุณมีอยู่แล้ว** `/ux-system enhance --from` อ่านระบบด้วยชื่อเดิมของมัน (token DTCG, CSS custom property, ธีม Tailwind, ไฟล์กฎ markdown หรือไฟล์ส่งออกตัวแปรของ Figma) ตรวจผ่านด่านเดียวกัน และวัดว่าโค้ดของคุณใช้มันจริงอย่างไร โดยไม่เขียนอะไรใหม่ `/ux-system extend --from` เพิ่มรากฐาน บทบาท หรือสัญญา โดยไม่เปลี่ยน token ที่มีอยู่เลย ในไฟล์ส่วนขยายที่วางไว้ข้างกัน และ `uxskill system export` เขียนระบบออกเป็น tokens.css ธีม Tailwind 4 หรือตัวแปร Figma ส่วน 4.2 จะเพิ่มชั้นความน่าเชื่อถือ (lint ทุกครั้งที่เขียน ผู้ตรวจขั้นสุดท้าย) และการเปิดตัว ดู[บันทึกการเปลี่ยนแปลง](CHANGELOG.md)

**คอมโพเนนต์และเซกชัน** สัญญาคอมโพเนนต์ 23 ฉบับระบุว่าแต่ละส่วนของตัวควบคุมผูกกับ token ใดในแต่ละสถานะ และแต่ละสถานะเคลื่อนไหวอย่างไร: การเปลี่ยนสถานะใช้ทรานซิชันตาม `motion.state` การกดย่อขยายตาม `motion.press.scale` (และนิ่งเมื่อลดการเคลื่อนไหว) ส่วนแท็บ เมนู และ segmented control เลื่อนตัวชี้ตัวเดียว สัญญาเซกชัน 14 ฉบับ (hero ราคา FAQ footer และส่วนอื่นๆ) ระบุหน้าที่ของแต่ละเซกชัน คอมโพเนนต์ที่ช่องของมันรับได้ หลักฐานที่ต้องมี และวิธีเรียงซ้อนบนมือถือ หน้าที่สร้างจากสัญญาเหล่านี้ใช้ภาพถ่าย ส่วนชิ้นส่วนอินเทอร์เฟซเป็นภาพเสริม ไม่ใช่ตัวแทน

**ลินเตอร์ที่อ่านหน้าเว็บ** กฎ 171 ข้อ ซึ่งหลายข้อตรวจเพิ่มบน CSS และมาร์กอัปที่ parse แล้ว อ่านระบบของหน้าเว็บเอง: การเคลื่อนไหวถูกจับเวลาจากเส้นโค้งของมัน ความสูงบรรทัดของหัวข้อ display ต้องไม่ต่ำกว่าเกณฑ์ของเครื่องยนต์ และตัวควบคุมที่ซ่อนอยู่ต้องออกจากลำดับแท็บ `uxskill lint --render` เปิดแต่ละหน้าใน Chromium แบบ headless ที่ความกว้างเดสก์ท็อปและมือถือแล้วลองใช้งานจริง: วงโฟกัสที่ไม่แสดงหรือถูกตัด hover และการกดที่ตอบสนองช้า โฟกัสที่หายไปหลังกด Escape และการกดที่ยังขยับอยู่เมื่อลดการเคลื่อนไหว

**คำสั่งน้อยลง** สแลชคอมมานด์ 25 ตัวเหลือ 18 ตัว `/ux-discover` รับ `--frame` และ `--recommend` `/ux-design` รับ `--component` `--dashboard` และ `--from-image` `/ux-polish` วน lint แก้ไข และ lint ซ้ำ จนคะแนนถึง 90 หรือครบสามรอบ และ `/ux-init` รับ `--stats` ชื่อเก่าเจ็ดชื่อยังใช้เป็น alias ได้และจะถูกถอดออกใน 4.1 ดู[alias](#alias-ที่จะถูกถอดใน-41)

**Playbook ตามประเภทหน้า** กฎของหน้าแลนดิ้ง แดชบอร์ด และคอมโพเนนต์อยู่ใน `references/surfaces/` ประเภทละหนึ่ง playbook `/ux-design` โหลดเพียงหนึ่งเดียวตามโหมดของมัน ดังนั้นการบิลด์แดชบอร์ดจะไม่อ่านกฎของ hero เลย

เทสต์ **ผ่าน 9764 รายการ** ออฟไลน์ กำหนดผลได้ ไม่เคยเรียก LLM

### ใหม่ใน v3.1: ซื่อตรงต่อแบรนด์ รองรับทุกจอ มีชีวิตชีวา

- **ความซื่อตรงต่อแบรนด์ถูกบังคับ ไม่ใช่แค่หวัง** สีหลักอ่านจากพิกเซลของโลโก้ (ไม่ใช่จาก CSS ที่ระบายมากที่สุด) ฟอนต์ค่าเริ่มต้นจะถูกปฏิเสธหากไม่เข้ากับสไตล์ตัวอักษรของโลโก้ แบรนด์ที่สกัดได้ถูกส่งต่อ `recommend` -> `synthesize` และ**เกณฑ์ขั้นต่ำแบบเข้มงวด**ใน `evaluate` จะตัดสินให้ผลลัพธ์ที่ทำสีหรือโลโก้แบรนด์หาย หรือไม่มีภาพจริง ไม่ผ่าน ทำงานร่วมกันได้สองทางกับข้อตกลงเปิด `brand.md` (เรนเดอร์ + นำเข้า)
- **Mobile-first มีด่านตรวจ** รากฐานงานฝีมือใหม่ (`responsive.md`, `component-behaviors.md`) พร้อมด่านที่รู้เรื่องการตัดบรรทัด ซึ่งไม่ผ่านเมื่อมีการเลื่อนแนวนอน ป้ายเมนู โลโก้ตัวอักษร หรือปุ่มที่ตัดขึ้นบรรทัดใหม่ หรือ sticky header ที่สูงเกินไป
- **ชั้นว้าว** เครื่องยนต์คิดช่วงเวลาซิกเนเจอร์ที่ประสานกัน 2-3 จุดต่อหน้า หลักคิดที่ว่า "ความว้าวมาจากผู้ใช้เท่านั้น" ถูกพลิกกลับ
- **ลินเตอร์คมขึ้น** (152 กฎ): ตรวจจับภาพที่จำเป็นและองค์ประกอบที่มีแค่ไอคอน กฎ token ตัวยึดตำแหน่งและ `100vw` เก็บ picsum แบบมี seed ไว้ ตัดแบบสุ่มออก

บันทึกฉบับเต็มอยู่ใน [CHANGELOG.md](CHANGELOG.md)

### มีอะไรใหม่ใน v3

- **Brand specs กลายเป็นข้อมูลฝึกสอน ไม่ใช่เทมเพลต** brand specs 160 รายการไม่ใช่แค็ตตาล็อกที่ recommender เลือกอีกต่อไป เป็นคำศัพท์ที่ synthesizer กลั่นกรอง เอาต์พุตใหม่ทุกการเรียก
- **Synthesizer 7 แกน** (warmth, contrast, density, geometry, formality, motion, type_personality) brief แมปเป็นค่าแกนแบบกำหนดได้ ค่าแกนคอมไพล์เป็น palette + ไทโป + spacing + radius + motion โทเค็นใหม่ๆ
- **สามโหมดอัตโนมัติ**: `strict_brand` (แบรนด์เดียว 100%), `brand_anchor` (แบรนด์เดียว 70% + ปรับตามแกนจากแบรนด์พี่น้อง 30%), `pure_synthesis` (ไม่ระบุแบรนด์ กลั่นจากตัวอย่างที่ตรงแกน 8 ตัว)
- **บัญชีตัดสินใจจัดอันดับ recommender ใหม่** `.ux/decisions.jsonl` จัดอันดับใหม่ตามชัยชนะในอดีตในบักเก็ต `(industry, ui_type)` เดียวกัน ปลอดภัยกับ cold-start นับเฉพาะการตัดสินใจที่ `lint_score >= 80` + `user_accepted = true`
- **เมทริกซ์การมีปฏิสัมพันธ์ของแกน**: แก้ไขความขัดแย้งระหว่างแกนแข่งขันอย่างชัดเจน (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius) ไม่มีกฎเฉพาะกิจเงียบๆ อีกแล้ว
- **ลูปอัตโนมัติ `/ux-evolve`** (ใน 4.0 คือลูปเริ่มต้นของ `/ux-polish`): lint → polish → re-lint จนคะแนน ≥ 90 ที่ราบ หรือครบ 3 รอบใน 4.0 (5 รอบใน v3) Quality gate ที่ 65
- **เครื่องมือ MCP ใหม่ 3 ตัว** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`
- **แดชบอร์ดสถิติท้องถิ่น**: `uxskill stats --html` เขียน `.ux/stats.html` แสดงสิ่งที่การติดตั้ง**ของคุณ**ได้เรียนรู้ ไม่มี telemetry ไม่มีการรวมระดับโลก
- **เทสต์ผ่าน 223 รายการ** ออฟไลน์ กำหนดได้ ไม่เคยเรียก LLM

รายละเอียดเต็มใน [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain)

### ประวัติดาว

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill คืออะไร

ux-skill เป็น **เครื่องยนต์ปัญญาด้านการออกแบบ** สำหรับเครื่องมือเขียนโค้ดด้วย AI ทำงานในรูปแบบแพ็กเกจ Python (`pip install uxskill`) ในรูปแบบปลั๊กอิน Claude Code และในรูปแบบตัวติดตั้งหลาย IDE สำหรับ 17 สภาพแวดล้อม เครื่องยนต์รับ brief ของโปรเจ็กต์ (อุตสาหกรรม กลุ่มเป้าหมาย โทน ข้อกำหนดที่ต้องมี ข้อห้าม สแตก พื้นที่) แล้วคืนระบบการออกแบบที่แนะนำแบบครบถ้วน: สไตล์ พาเลตต์ คู่ตัวอักษร พรีเซตการเคลื่อนไหว คอมโพเนนต์ แบรนด์ตัวอย่างที่ควรศึกษา และรั้วกัน anti-pattern ที่ต้องยึดถือ คำแนะนำเป็นเชิงกำหนด อินพุตเดียวกันให้เอาต์พุตเดียวกันเสมอ

ปลั๊กอินวางตัวอยู่ระหว่างคุณกับเครื่องมือเขียนโค้ดด้วย AI เมื่อคุณขอ Claude Code, Cursor หรือผู้ช่วย AI อื่นๆ ให้ "สร้างหน้าแลนดิ้งฟินเทค" ผู้ช่วยมักจะด้นสด และผลลัพธ์ก็ดูออกว่า AI สร้างภายในห้าวินาที (ไล่สีม่วงไปน้ำเงิน การ์ดเท่ากันสามใบ Inter ขนาด display "John Doe" ในคำรับรอง ทรานซิชันค่าเริ่มต้น 300ms hero จัดกึ่งกลาง ลูกศร CTA เด้งไปมา) ux-skill แทนที่การด้นสดด้วย**ข้อจำกัดที่มีโครงสร้าง**: คุณรัน `/ux-discover` เพื่อเก็บบรีฟและเลือกระบบ `/ux-design` เพื่อสร้างโค้ด และ `/ux-lint` เพื่อยืนยันว่าผ่านกฎต้าน AI slop แบบกำหนดผลได้ 171 ข้อก่อน commit

README นี้คือเอกสารอ้างอิงหลัก ทุกคอมมานด์ ทุกซับเอเจนต์ ทุกแมนิเฟสต์ข้อมูล ทุกเส้นทางการติดตั้ง ทุกสเปกแบรนด์ ทุกหมวด anti-pattern มีบันทึกไว้ทั้งหมดที่นี่ หากคุณกำลังเลือกปลั๊กอินการออกแบบสำหรับ Claude Code หรือเปรียบเทียบเครื่องมือออกแบบด้วย AI สำหรับ Cursor, Windsurf หรือ Codex ให้อ่านเอกสารนี้ตั้งแต่ต้นจนจบควบคู่กับ [compare.html](https://uxskill.laithjunaidy.com/compare.html)

---

## สารบัญ

1. [สมอง v3.0 คืออะไร](#สมอง-v30-คืออะไร)
2. [ติดตั้งด่วน](#ติดตั้งด่วน)
3. [ตัวเลข เปรียบเทียบสดกับ 8 สกิล UX อันดับต้นของ Claude](#ตัวเลข-เปรียบเทียบสดกับ-8-สกิล-ux-อันดับต้นของ-claude)
4. [สถาปัตยกรรม ชิ้นส่วนเข้ากันได้อย่างไร](#สถาปัตยกรรม-ชิ้นส่วนเข้ากันได้อย่างไร)
5. [18 สแลชคอมมานด์ ข้อมูลอ้างอิงโดยละเอียด](#18-สแลชคอมมานด์-ข้อมูลอ้างอิงโดยละเอียด)
6. [5 ซับเอเจนต์](#5-ซับเอเจนต์)
7. [11 แมนิเฟสต์ข้อมูล](#11-แมนิเฟสต์ข้อมูล)
8. [171 กฎต้าน AI slop ลินเตอร์](#171-กฎต้าน-ai-slop-ลินเตอร์)
9. [160 สเปก DESIGN.md แบรนด์ แบ่งตามหมวด](#160-สเปก-designmd-แบรนด์-แบ่งตามหมวด)
10. [เซิร์ฟเวอร์ MCP หมากอสมมาตร](#เซิร์ฟเวอร์-mcp-หมากอสมมาตร)
11. [ตัวติดตั้ง 17 IDE](#ตัวติดตั้ง-17-ide)
12. [กรณีใช้งาน สถานการณ์รูปธรรม](#กรณีใช้งาน-สถานการณ์รูปธรรม)
13. [เปรียบเทียบกับทางเลือกอื่น](#เปรียบเทียบกับทางเลือกอื่น)
14. [แผนงาน](#แผนงาน)
15. [การมีส่วนร่วม](#การมีส่วนร่วม)
16. [ใบอนุญาต ผู้แต่ง คำขอบคุณ](#ใบอนุญาต-ผู้แต่ง-คำขอบคุณ)

---

## สมอง: v3.0 คืออะไร

v3.1.0 คือการเปลี่ยนแปลงทางสถาปัตยกรรมที่ใหญ่ที่สุดในประวัติศาสตร์ของ ux-skill recommender ไม่เลือกเทมเพลตจากแค็ตตาล็อกอีกแล้ว engine **สังเคราะห์**ภาษาดีไซน์ใหม่ต่อ brief แต่ละครั้ง brief เดียวกันให้เอาต์พุตเดียวกันเสมอ (กำหนดได้สมบูรณ์) แต่ brief ที่แตกต่างจะได้ระบบใหม่ของตัวเอง Brand specs ไม่ใช่เทมเพลตอีกต่อไป แต่เป็นข้อมูลฝึกสอนที่ engine เรียนรู้คำศัพท์มา ระบบมีตาเฝ้าดูประวัติของตัวเอง ปิดลูปฟีดแบ็กในเครื่อง และไม่เคยเรียก LLM

Compiler คือ **synthesizer 7 แกนแบบกำหนดได้** warmth, contrast, density, geometry, formality, motion, type_personality ทุก brief แมปเป็นค่าแกน ค่าแกนคอมไพล์เป็น palette + ไทโป + spacing + radius + motion โทเค็นใหม่ๆ สเกลตัวอักษรแบบโมดูลาร์เลือกอัตราส่วนจาก contrast (1.200 quiet / 1.250 balanced / 1.333 loud) Layout primitive ตอบสนองได้ตามการก่อสร้าง (`auto-fit minmax(min(N, 100%), 1fr)` + container queries) Layout เสียไม่สามารถปล่อยออกมาได้เพราะแสดงไม่ได้

มีสามโหมดอัตโนมัติ: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% โทเค็น Stripe เส้นทางที่เร็วที่สุด); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% ปรับตามแกนจาก 4 แบรนด์พี่น้อง); และ `pure_synthesis` (ไม่ระบุแบรนด์ → พื้นที่ไม่จำกัด ตัวอย่างที่ตรงแกน 8 ตัวถูกกลั่นเป็นภาษาดีไซน์ใหม่) แกนที่ขัดแย้งถูกแก้โดย **เมทริกซ์การมีปฏิสัมพันธ์ของแกน** ที่บันทึกไว้ dense + corporate คอมไพล์เป็น 4px (density ชนะ ตระกูล Bloomberg) airy + corporate เป็น 12px (formality ชนะ หรูหรา) soft + playful เป็น 18px radius, sharp + corporate เป็น 2px ไม่มีกฎเฉพาะกิจเงียบๆ ในการใช้งาน

**บัญชีตัดสินใจ** (`.ux/decisions.jsonl`, schema `_v: 1` ล็อก) ปิดลูปฟีดแบ็ก recommender ตอนนี้จัดอันดับผู้สมัครใหม่ตามความสำเร็จในอดีตในบักเก็ต `(industry, ui_type)` เดียวกัน ปลอดภัยตอนเริ่มเย็น: ข้ามการจัดอันดับใหม่เมื่อมีการตัดสินใจก่อนหน้าน้อยกว่า 3 รายการ นับเฉพาะการตัดสินใจที่ `lint_score >= 80` AND `user_accepted = true` นอกจากนี้ `/ux-polish` รัน lint → polish → re-lint จนคะแนน ≥ 90 ที่ราบ หรือครบ 3 รอบ พร้อม quality gate ที่ 65 ซึ่งผลลัพธ์ที่ต่ำกว่าจะถูกปฏิเสธ เว้นแต่ใช้ `--force` ผลคือ: ทุกการติดตั้งฉลาดขึ้นจากคลังข้อมูลของตัวเอง ทุกการรันทำซ้ำได้ข้ามเครื่อง และเครื่องยนต์ยังออฟไลน์เต็มที่

---

## ติดตั้งด่วน

เส้นทางการติดตั้งสามทาง เลือกทางที่ตรงกับสภาพแวดล้อมของคุณ

### เส้นทางที่ 1: มาร์เก็ตเพลส Claude Code (ทางหลัก)

ถ้าคุณใช้งานใน Claude Code ให้ติดตั้งผ่านมาร์เก็ตเพลสปลั๊กอิน:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

สิ่งนั้นจะเชื่อมต่อสแลชคอมมานด์ทั้ง 18 ตัว (บวกชื่อเก่า 7 ชื่อที่คงไว้เป็น alias จนถึง 4.1) และซับเอเจนต์ทั้ง 5 ตัวเข้ากับเซสชัน Claude Code ของคุณ หลังติดตั้งให้รัน `/ux-init` เพื่อตั้งค่าไดเรกทอรีสถานะ `.ux/` ของแต่ละโปรเจ็กต์และยืนยันว่าเครื่องยนต์ Python เข้าถึงได้

### เส้นทางที่ 2: pip (สากล)

ถ้าคุณทำงานนอก Claude Code (Cursor, Windsurf, CLI, CI) ให้ติดตั้งแพ็กเกจ Python:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

แพ็กเกจเผย `ux` และ `uxskill` เป็น entry point ของ CLI เป็น binary ตัวเดียวกัน

### เส้นทางที่ 3: npx (ไม่ต้องใช้ Python)

ถ้าคุณไม่อยากจัดการ Python โดยตรง ตัวห่อ npx จะ bootstrap ทุกอย่างผ่าน `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### ยืนยันการติดตั้ง

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

จำนวนทั้งสิบสองรวมกันได้ 1,262 รายการ ถ้ามีจำนวนใดคืน 0 หมายความว่าไฟล์ JSON หายไป ให้เปิด issue ที่ [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues)

---

## ตัวเลข: เปรียบเทียบสดกับ 8 สกิล UX อันดับต้นของ Claude

จำนวนดาวยืนยันล่าสุดผ่าน `gh api` เมื่อ **2026-05-28** ux-skill (Laith0003/ux-skill) เป็นผู้เข้ามาใหม่ล่าสุด เราเล็กในด้านการรับรู้ แต่ลึกในด้านสถาปัตยกรรม การเปรียบเทียบด้านล่างซื่อสัตย์: เราแพ้ตรงไหน เราชนะตรงไหน

| ปลั๊กอิน | ดาว | สถาปัตยกรรม | สแลชคอมมานด์ | ลินเตอร์ (CI-safe) | สเปกแบรนด์ | คอมโพเนนต์ | พรีเซตการเคลื่อนไหว | IDE ที่รองรับ |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV, สกิลเดียว | 1 | - | | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 สกิล + พรีวิว | 19 | - | | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + รสนิยมที่อิงงานวิจัย | 1 | - | | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | SKILL.md ขนาด 62 KB ไฟล์เดียว + สคริปต์ | 1 | - | | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | ไลบรารีสกิลต่อ MCP | หลายตัว | - | | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | สกิลแนวสวยงามแบบเดียว | 1 | - | | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | สกิลออกแบบต้านสลอป | 1 | - | | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | คอมโพเนนต์ MD3 + audit | 1 | - | (เฉพาะ MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **เครื่องยนต์ Python + 12 manifest + 18 คอมมานด์ + 5 ซับเอเจนต์ + ลินเตอร์ CI** | **18** | **171 กฎเชิงกำหนด** | **160** | **148** | **57** | **17** |

### ที่เราแพ้

- **การรับรู้** พวกเขามีดาวหลายแสน เรามี 14 ดวง ติดดาวให้เรา เป็นวิธีช่วยที่ถูกที่สุด
- **การจดจำแบรนด์** ui-ux-pro-max และ open-design นำหน้ามาเป็นเดือน ไม่ใช่วัน
- **การขัดเกลาด้านการตลาด** พวกเขามีสกรีนช็อต วิดีโอเดโม และหน้าแลนดิ้งที่หาเจอง่าย เรามี README ที่ละเอียดและแลนดิ้งบางๆ

### ที่เราชนะ

- **ไลบรารีคอมโพเนนต์:** คอมโพเนนต์ 148 ตัวที่บันทึกไว้พร้อม anatomy สถานะ โทเค็นที่ใช้ และสเปกการเคลื่อนไหว ไม่มีใน 8 ปลั๊กอินอื่นที่ส่งแมนิเฟสต์คอมโพเนนต์
- **พรีเซตการเคลื่อนไหว:** 57 รายการพร้อมใช้แบ่งตามสแตก (Framer Motion, GSAP, CSS) พร้อม fallback แบบ reduced-motion ไม่มีตัวอื่นที่ส่งแมนิเฟสต์การเคลื่อนไหว
- **ลินเตอร์ anti-pattern:** 171 กฎเชิงกำหนด รันใน CI ออกด้วยรหัสไม่ใช่ศูนย์ที่ Critical/High ไม่มีตัวอื่นที่ส่งลินเตอร์เชิงกำหนด
- **สเปกแบรนด์:** สเปก DESIGN.md จริง 160 รายการ (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude และอีก 96 แบรนด์) ไม่มีตัวอื่นที่ส่งไลบรารีแบรนด์
- **รองรับ 17 IDE:** เครื่องยนต์เดียวกัน กาวที่ต่างกันในแต่ละ IDE
- **18 สแลชคอมมานด์:** discovery, generation (หน้าเว็บ คอมโพเนนต์ แดชบอร์ด จากภาพ), audit, lint, ลูป polish, ลูปแก้ไข, case study, workshop, copy, motion, a11y, conductor บูรณาการครบถ้วน

ตารางเปรียบเทียบเคียงข้างกันเต็มรูปแบบที่ [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)

---

## สถาปัตยกรรม: ชิ้นส่วนเข้ากันได้อย่างไร

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

### เครื่องยนต์ทำงานจริงอย่างไร

1. **อินพุต** คุณให้บรีฟ จะโต้ตอบผ่าน `/ux-discover` (10 ฟิลด์) หรือไม่โต้ตอบโดยส่งแฟล็กให้ `ux recommend` ก็ได้
2. **ค้นหาขนาน 5 ทาง** เครื่องยนต์รันการค้นหาห้ารายการพร้อมกันข้าม manifest:
   - **อุตสาหกรรม → recommended_styles** (industries.json)
   - **สไตล์ → ความเข้ากันได้ของพาเลตต์ + ตัวอักษร + การเคลื่อนไหว** (styles.json)
   - **น้ำเสียง × สิ่งที่ต้องมี → ตัวกรองพาเลตต์** (palettes.json)
   - **Stack → ความเข้ากันได้ของคอมโพเนนต์ + พรีเซ็ตการเคลื่อนไหว** (tech-stacks.json, motion-presets.json)
   - **ข้อห้าม + ภูมิภาค → รั้วกัน + รายชื่อแบรนด์ตัวอย่าง** (anti-patterns.json, brands/)
3. **รวมผล** ตัวรวมแบบกำหนดผลได้จัดอันดับผู้สมัคร แก้ข้อขัดแย้ง (เช่น โหมดมืดที่ต้องมีจะกำหนดโหมดของพาเลตต์) และส่งออกระบบแนะนำหนึ่งชุด
4. **เอาต์พุต** เอกสาร JSON ที่มีสไตล์ที่เลือก พาเลตต์ คู่ตัวอักษร พรีเซ็ตการเคลื่อนไหว 5 อันดับแรก คอมโพเนนต์ 12 อันดับแรก แบรนด์ตัวอย่าง 5 อันดับแรก และรั้วกัน anti-pattern ทั้ง 171 ตัวที่เปิดใช้งาน พร้อมบล็อกเหตุผลที่อธิบายแต่ละตัวเลือก
5. **การสร้าง** คอมมานด์ถัดไป (`/ux-design` ในโหมดหน้าเว็บ คอมโพเนนต์ แดชบอร์ด และภาพ รวมทั้ง `/ux-system`) ใช้คำแนะนำนั้นสร้างโค้ดจริงผ่านซับเอเจนต์
6. **การยืนยัน** `/ux-lint` สแกนโค้ดที่สร้างซ้ำตามกฎ 171 ข้อ ออกด้วยรหัสไม่ใช่ศูนย์ที่ Critical/High ใน CI

**สิ่งที่เพิ่มใน v3** ตอนนี้ recommender จัดอันดับผู้สมัครใหม่จาก `engine/decisions/` โดยใช้ `.ux/decisions.jsonl` (นับเฉพาะการตัดสินใจที่ `lint_score >= 80` AND `user_accepted = true` และปลอดภัยตอนเริ่มเย็นเมื่อมีการตัดสินใจก่อนหน้าน้อยกว่า 3 รายการ) เส้นทางการสร้างส่งต่อไปยัง `engine/synthesizer/` ได้ ซึ่งเป็นคอมไพเลอร์ 7 แกนแบบกำหนดผลได้ ที่สร้าง token พาเลตต์ + ตัวอักษร + ระยะห่าง + มุมโค้ง + การเคลื่อนไหวใหม่สำหรับแต่ละบรีฟ แทนการหยิบเทมเพลตจากแค็ตตาล็อก ดูรายละเอียดที่ [สมอง v3.0 คืออะไร](#สมอง-v30-คืออะไร)

**Python คิด HTML แสดง Markdown ร้อยต่อ**

---

## 18 สแลชคอมมานด์: ข้อมูลอ้างอิงโดยละเอียด

ทุกคอมมานด์มาเป็นไฟล์ `.md` ใต้ `commands/` ที่มี `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` และ `output state file` คำอธิบายด้านล่างเป็นฉบับย่อ ซอร์สฉบับเต็มคือสเปกที่ถือเป็นหลัก

คอมมานด์แบ่งเป็นเจ็ดกลุ่ม: **บูตสแตรปและสำรวจคลัง**, **discovery และคำแนะนำ**, **การสร้าง**, **ตรวจสอบและยืนยัน**, **แก้ไขและขัดเกลา**, **discovery และการเล่าเรื่อง** และ **ผู้ควบคุมวง** ชื่อจาก 3.x เจ็ดชื่อยังใช้เป็น [alias](#alias-ที่จะถูกถอดใน-41) ได้จนถึง 4.1

### Bootstrap & คลังข้อมูล

#### `/ux-init`: bootstrap โปรเจ็กต์

- **คืออะไร:** ตรวจจับ IDE ที่คุณใช้ (`.claude/`, `.cursor/`, `.windsurf/` ฯลฯ) ติดตั้ง artifact ที่ถูกต้อง ยืนยันว่าเครื่องยนต์ Python เข้าถึงได้ พิมพ์สแน็ปช็อตสถิติ `--stats` พิมพ์เฉพาะสแน็ปช็อต: เวอร์ชัน + จำนวนรายการใน manifest ข้อมูล
- **ใช้เมื่อไหร่:** ติดตั้งครั้งแรกในโปรเจ็กต์ใหม่ หลังโคลนโปรเจ็กต์ที่ใช้ ux-skill หลัง `pip install --upgrade uxskill` ใช้ `--stats` หลังติดตั้ง หลังอัปเกรด หรือเมื่อคำแนะนำออกมาแปลกๆ และสงสัยว่า manifest ไม่ครบ
- **ข้ามเมื่อไหร่:** คุณรันในโปรเจ็กต์นี้แล้วและไม่มีอะไรเปลี่ยน `--stats` ไม่จำเป็นต้องข้าม: เป็นการอ่านแค่ 50ms
- **การเรียก:** `/ux-init` (ไม่มี args), `/ux-init --stats` หรือ `uxskill init` / `uxskill stats` จาก CLI `--decisions` เพิ่มสรุปบัญชีตัดสินใจ `--html` เขียน `.ux/stats.html`
- **เอาต์พุต:** artifact ต่อ IDE (ดู [ตัวติดตั้ง 17 IDE](#ตัวติดตั้ง-17-ide)) + ไดเรกทอรี `.ux/` + สรุปทาง stdout `--stats`: JSON ทาง stdout (ดู [ยืนยันการติดตั้ง](#ยืนยันการติดตั้ง) ด้านบน)
- **ร้อยต่อ:** `/ux-discover` ต่อไป `--stats` ใช้เพื่อวินิจฉัยเท่านั้น

#### `/ux-mcp`: รันเครื่องยนต์เป็นเซิร์ฟเวอร์ MCP

- **คืออะไร:** เริ่มเครื่องยนต์เป็นเซิร์ฟเวอร์ Model Context Protocol ผ่าน stdio เครื่องมือ 25 ตัว (recommender ลินเตอร์ การบันทึกสถานะ ตัวสังเคราะห์ บัญชีตัดสินใจ การสกัดจากภาพ manifest ข้อมูล และการสร้าง นำเข้า ปรับปรุง ขยาย ส่งออก และตรวจระบบดีไซน์) เรียกใช้ได้จาก host ใดก็ได้ที่รองรับ MCP โดยไม่ต้องมีปลั๊กอิน
- **ใช้เมื่อไหร่:** คุณทำงานใน host อื่นที่รองรับ MCP และอยากได้เครื่องยนต์เดียวกัน คุณรัน pipeline หลายเอเจนต์ที่ต้องการแหล่งข้อจำกัดด้านดีไซน์เพียงแหล่งเดียว คุณอยากให้ recommender หรือลินเตอร์เป็น process ที่รันยาวใน CI
- **ข้ามเมื่อไหร่:** คุณอยู่ใน Claude Code ที่ติดตั้งปลั๊กอินแล้ว สแลชคอมมานด์เข้าถึงเครื่องยนต์อยู่แล้ว คุณต้องการคำตอบครั้งเดียว `uxskill recommend` หรือ `uxskill lint` ง่ายกว่า
- **การเรียก:** `/ux-mcp` หรือ `ux-mcp` จากเชลล์หลัง `pip install 'uxskill[mcp]'`
- **เอาต์พุต:** เซิร์ฟเวอร์ JSON-RPC ทาง stdio ดู [เซิร์ฟเวอร์ MCP](#เซิร์ฟเวอร์-mcp-หมากอสมมาตร) และ `commands/ux-mcp.md` สำหรับการตั้งค่าแต่ละไคลเอนต์
- **ร้อยต่อ:** ไม่มี เป็นชั้นขนส่ง ไม่ใช่ขั้นตอน

### Discovery & คำแนะนำ

#### `/ux-discover`: ด่านบังคับ (เก็บข้อมูล 10 ฟิลด์ การวางกรอบ คำแนะนำ)

- **คืออะไร:** การเก็บข้อมูล 10 ฟิลด์ภาคบังคับที่ทุกโปรเจ็กต์ต้องผ่านก่อนคอมมานด์สร้างใดๆ ประเภทโปรเจ็กต์ กลุ่มเป้าหมาย เป้าหมายหลัก น้ำเสียง สิ่งที่ต้องมี สิ่งต้องห้าม แบรนด์อ้างอิง stack ภูมิภาค ตัวชี้วัดความสำเร็จ **ไม่มีการด้นสด** วลีต้องห้าม ("modern", "clean") บังคับให้ผู้ใช้พูดให้เจาะจง จากนั้นรัน recommender: การค้นหาขนาน 5 ทางของเครื่องยนต์ Python ข้าม 12 manifest คืนระบบดีไซน์ที่รวมแล้วหนึ่งชุด (อุตสาหกรรม → สไตล์ → พาเลตต์ → ตัวอักษร → การเคลื่อนไหว + คอมโพเนนต์ + แบรนด์ตัวอย่าง + รั้วกัน)
- **โหมด:** `--frame` บันทึกว่าทำเพื่อใคร ผลลัพธ์ สมมติฐาน และสัญญาณความสำเร็จ ในบล็อกวางกรอบสี่ฟิลด์ เบากว่าการเก็บข้อมูลเต็ม `--recommend` รันเฉพาะ recommender จากบรีฟที่บันทึกไว้หรือจากแฟล็กครั้งเดียว
- **ใช้เมื่อไหร่:** ก่อน `/ux-design` หรือ `/ux-system` ใดๆ เมื่อบรีฟก่อนหน้าเก่าไปแล้ว `--frame` ตอนเริ่มโปรเจ็กต์ สปรินต์ หรืองานครั้งเดียว หรือกลางทางเมื่อบทสนทนาหลุดประเด็น `--recommend` เมื่อจะปรับทิศทางผลิตภัณฑ์ที่ดูเหนื่อยล้า
- **ข้ามเมื่อไหร่:** คุณกำลังแก้บั๊ก (`/ux-fix`) คุณแค่รันลินเตอร์หนึ่งรอบ (`/ux-lint`) บรีฟไม่เปลี่ยนจากเซสชันก่อน
- **การเรียก (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"` หรือ `/ux-discover --recommend`
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
- **เอาต์พุต:** `.ux/last-discovery.json` (บรีฟ 10 ฟิลด์), `.ux/last-recommendation.json` (สไตล์ที่เลือก พาเลตต์ คู่ตัวอักษร พรีเซ็ตการเคลื่อนไหว 5 อันดับแรก คอมโพเนนต์ 12 อันดับแรก แบรนด์ตัวอย่าง 5 อันดับแรก รั้วกัน anti-pattern ทั้ง 171 ตัวที่เปิดใช้งาน พร้อมเหตุผล) และเมื่อใช้ `--frame` จะได้ `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`)
- **ร้อยต่อ:** `/ux-design [extra brief]` → โค้ดฟรอนต์เอนด์ที่ยึดตามคำแนะนำ `/ux-design --component <name>` → คอมโพเนนต์หนึ่งตัวที่ตรงกับข้อจำกัดที่ค้นพบ `/ux-system` → ระบบดีไซน์เต็มชุดจากคำแนะนำ `/ux-lint` → ยืนยันโค้ดที่สร้าง

### การสร้าง

#### `/ux-design`: สร้างพื้นผิวที่สวยงาม ต้านสลอป จาก brief

- **คืออะไร:** สร้าง artifact ฟรอนต์เอนด์คุณภาพ production ครบถ้วน (landing เว็บไซต์การตลาด app shell) จาก brief discovery + คำแนะนำ มอบหมาย `frontend-engineer` พร้อมทิศทางสร้างสรรค์จากตัวอ้างอิงต้านสลอปและคลังอาวุธ บรีฟหรือแฟล็กจะเลือกหนึ่งในสี่โหมด:
  - **หน้าเว็บ** (ค่าเริ่มต้น): หน้าเต็มหรือหน้าที่มีหลายเซกชัน เขียน `.ux/last-design.json`
  - **`--component [name]`**: คอมโพเนนต์เดี่ยวคุณภาพ production (ปุ่ม โมดัล แถบนำทาง แถบข้าง การ์ด ตาราง ฟอร์ม กราฟ) ครบทั้งสี่สถานะการโต้ตอบ เข้าถึงได้ ตรงแบรนด์ ค้นหาคอมโพเนนต์ใน `.ux/last-recommendation.json` ก่อน ถ้าไม่พบจึง query manifest โดยตรง เขียน `.ux/last-component.json`
  - **`--dashboard`**: วินัยด้านความหนาแน่นของข้อมูล เลย์เอาต์ bento ตัวเลข monospace แบบตาราง รูปแบบ sparkline ไม่ใช้การ์ดพร่ำเพรื่อ สีสถานะเชิงความหมาย การเคลื่อนไหวที่พอดี ไม่ใช่เว็บไซต์การตลาดที่แปะกราฟ เขียน `.ux/last-dashboard.json`
  - **`--from-image <path>`**: อ่านภาพอ้างอิงการออกแบบ (PNG/JPG/WebP) ด้วย computer vision ล้วนของ Pillow (พาเลตต์หลัก ความสว่างของพื้น สัญญาณตัวอักษร) เทียบกับ manifest พาเลตต์และสไตล์ แล้วสร้างจากคำแนะนำที่ได้ `--extract-only` หยุดหลังการสกัด เขียน `.ux/last-image-extract.json`
- **ใช้เมื่อไหร่:** "Design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "build a button", "design the admin panel", "operator console", "KPI board", "build it like this screenshot" คำขอผลงานภาพแบบฟอร์มอิสระใดๆ
- **ข้ามเมื่อไหร่:** คุณต้องการรีวิว ไม่ใช่สร้าง (ใช้ `/ux-audit` หรือ `/ux-critique`) งานแบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`
- **เอาต์พุต:** โค้ดที่สร้าง (HTML / Blade / JSX / Vue / Astro) พร้อมไฟล์สถานะของโหมดนั้น
- **ร้อยต่อ:** `/ux-lint` → ยืนยันกับรั้วกัน `/ux-polish` → พาสเครื่องสำอาง `/ux-a11y` → audit การเข้าถึง `/ux-copy` → ทบทวน microcopy `/ux-fix` → นำผลตรวจมาใช้เป็น commit อะตอม

#### `/ux-system`: สร้างระบบการออกแบบเริ่มต้นเต็มรูปแบบ

- **คืออะไร:** เสนอระบบการออกแบบเริ่มต้นเต็มรูปแบบสำหรับโปรเจ็กต์ที่ยังไม่มี โทเค็น (สี ตัวอักษร space การเคลื่อนไหว radius shadow) เอกสาร foundation สัญญาคอมโพเนนต์ การจับคู่ dark-mode สวิตช์ theme มอบหมาย `design-system-architect`
- **ใช้เมื่อไหร่:** "We don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS"
- **ข้ามเมื่อไหร่:** โปรเจ็กต์มีระบบการออกแบบแล้ว ให้ใช้ `/ux-design --component` กับระบบที่มีอยู่แทน แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-system create` (เครื่องยนต์รากฐาน), `/ux-system enhance --from <file>` (วัดระบบที่คุณมีอยู่แล้ว), `/ux-system extend --from <file> --add <foundation>` (เพิ่มโดยไม่เปลี่ยนของเดิม) หรือ `/ux-system` (ลำดับงานของ 3.x รัน discovery ก่อนถ้ายังไม่มี)
- **เอาต์พุต:** `tokens.json`, `foundations.md`, สัญญา `components/*.md` ปล่อย Tailwind / vanilla / SCSS ทางเลือก เขียน `.ux/last-system.json` สำหรับ chain context
- **ร้อยต่อ:** `/ux-design --component` → สร้างบนระบบใหม่ `/ux-design` → สร้างหน้าด้วย token ใหม่

#### `/ux-motion`: การจัดการการเคลื่อนไหว

- **คืออะไร:** สร้างชั้นการเคลื่อนไหวของพื้นผิว ระยะเวลา easing ออกแบบท่าทาง fallback reduced-motion วินัยประสิทธิภาพ ยัง audit การเคลื่อนไหวที่มีอยู่ตาม 5 มิติ (timing, easing, ความหมาย, reduced-motion, ประสิทธิภาพ)
- **ใช้เมื่อไหร่:** "Motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "performance pass on the motion"
- **ข้ามเมื่อไหร่:** พื้นผิวไม่มีการเคลื่อนไหว (ใช้ `/ux-audit` หรือ `/ux-polish`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-motion path/to/component.tsx` (โหมด audit) หรือ `/ux-motion --generate hero-entry` (สร้าง)
- **เอาต์พุต:** โค้ดอัปเดต (ในโหมดสร้าง) หรือรายงาน `.ux/last-motion.json` (ในโหมด audit)
- **ร้อยต่อ:** `/ux-fix` → ใช้ผลตรวจการเคลื่อนไหว `/ux-polish` → กระชับ

### Audit & ยืนยัน

#### `/ux-lint`: ลินเตอร์อิง regex เชิงกำหนด (ไม่ใช้ LLM, CI-safe)

- **คืออะไร:** รัน 171 กฎบนโค้ดของคุณ ไม่เรียก LLM ออกด้วยรหัสไม่ใช่ศูนย์ที่ Critical / High ใน CI แหล่ง: `data/anti-patterns.json` กฎครอบคลุม A11y (45) เนื้อหา (35) Layout (18) ตัวอักษร (16) การเคลื่อนไหว (14) ภาพ (14) คุณภาพ (12) สี (10) ประสิทธิภาพ (5) ความลึก (2)
- **ใช้เมื่อไหร่:** pre-commit hook ประตู CI พาสแรกที่เร็วบน codebase ใหญ่ก่อนเสียค่า `/ux-audit` หลัง `/ux-design` ในโหมดใดก็ได้ เพื่อยืนยันการสร้าง
- **ข้ามเมื่อไหร่:** คุณต้องการลูปแก้ไข (ลินเตอร์รายงาน ไม่แก้ ต่อเป็น `/ux-polish --fix` หรือ `/ux-fix`) คุณต้องการการตัดสินรสนิยม (ใช้ `/ux-critique`)
- **การเรียก (slash):** `/ux-lint src/`
- **การเรียก (CLI):** `uxskill lint .` หรือ `python3 bin/ux-lint.py .` หรือ `bash bin/ux-lint.sh --ci --fail-on high`
- **การเรียก (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **เอาต์พุต:** ผลตรวจทาง stdout (ตำแหน่ง id กฎ ความรุนแรง หลักฐาน) exit code 0 ถ้าสะอาด ไม่ใช่ศูนย์ที่ Critical/High เมื่อตั้ง `--fail-on high`
- **ร้อยต่อ:** `/ux-polish --fix` → คู่หูขับเคลื่อนด้วย LLM บนรูปแบบเดียวกัน `/ux-fix` → ใช้ผลตรวจเป็น commit จัดเรียงตามความรุนแรง `/ux-audit` → พาสให้เหตุผล 6 เลนส์เต็ม `/ux-next` → ให้วาทยกรตัดสิน

#### `/ux-audit`: audit การออกแบบ 6 เลนส์

- **คืออะไร:** รีวิวที่มีโครงสร้าง มีความเห็น เทียบกับ 6 เลนส์ (ความชัดเจน ลำดับชั้น การเข้าถึง เสียง การเคลื่อนไหว รสนิยม) ผลิตผลตรวจที่ติดป้ายความรุนแรง รายงานสไตล์ Polaris อ่าน `.ux/last-frame.json` ก่อน กลุ่มเป้าหมายและผลลัพธ์ยึดความรุนแรงของแต่ละผลตรวจ
- **ใช้เมื่อไหร่:** พื้นผิวมีอยู่และคุณต้องการการวิจารณ์ที่ปกป้องได้ "Audit", "review the ux", "is this any good", "what's broken", "tear this apart"
- **ข้ามเมื่อไหร่:** พื้นผิวยังไม่มีอยู่ (ใช้ `/ux-design`) ผู้ใช้ต้องการเลนส์เดียว (ใช้คอมมานด์เป้าหมาย: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`) ผู้ใช้ต้องการความเห็นรสนิยม (ใช้ `/ux-critique`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-audit https://example.com/pricing` หรือ `/ux-audit src/components/Pricing.tsx`
- **เอาต์พุต:** เขียน `.ux/last-audit.json` อาร์เรย์ `findings` ของ `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`
- **ร้อยต่อ:** `/ux-fix` → นำผลตรวจมาใช้ `/ux-polish` → พาสเครื่องสำอาง `/ux-design` → ถ้าต้องการ redesign เชิงโครงสร้าง

#### `/ux-a11y`: audit WCAG 2.1 AA + การตรวจมารยาททั่วไป

- **คืออะไร:** audit WCAG 2.1 AA ที่มีโครงสร้าง พร้อมการตรวจมารยาททั่วไปที่ผ่านเครื่องมืออัตโนมัติแต่ยังทำร้ายผู้ใช้จริง (การมองเห็น focus ความเฉพาะของ error การตั้งค่าการเคลื่อนไหว กับดักคีย์บอร์ด การพึ่งพาสี)
- **ใช้เมื่อไหร่:** ประตูการเข้าถึงก่อนส่ง หลัง redesign "Accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check"
- **ข้ามเมื่อไหร่:** ไม่ใช่ส่วนที่ผู้ใช้เห็น แบ็คเอนด์หรือโครงสร้างพื้นฐาน สเก็ตช์ work-in-progress
- **การเรียก:** `/ux-a11y https://example.com` (URL สดดีกว่า เครื่องมืออัตโนมัติและการทดสอบคีย์บอร์ดทำงานเฉพาะตอนสด)
- **เอาต์พุต:** เขียน `.ux/last-a11y.json` อาร์เรย์ `findings` ของ `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, อาร์เรย์ `beyond_wcag`, `severity_counts`
- **ร้อยต่อ:** `/ux-fix` → นำผลตรวจมาใช้เป็น commit `/ux-copy` → แก้ alt text และการต่อ error ของฟอร์มเป็นส่วนหนึ่งของพาส copy

#### `/ux-critique`: การเรียกรสนิยม (3 ชนะ 3 พลาด 1 หมากกลยุทธ์)

- **คืออะไร:** ความเห็นของนักออกแบบ ไม่ใช่ audit เชิงโครงสร้าง ไม่ใช่คะแนนความรุนแรง แค่มุมมองที่กระชับ มีความเห็น ที่ระบุว่าอะไรใช้ได้ อะไรไม่ และหมากกลยุทธ์หนึ่งหมากที่จะเปลี่ยนแปลงมากที่สุด
- **ใช้เมื่อไหร่:** "What do you think", "is this good", "critique this", "honest take", "is the vibe right", "does this feel like us", "should we ship this"
- **ข้ามเมื่อไหร่:** ผู้ใช้ต้องการ audit เชิงโครงสร้างชัดเจน (ใช้ `/ux-audit`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-critique https://example.com`
- **เอาต์พุต:** เขียน `.ux/last-critique.json` 3 ชนะ 3 พลาด 1 หมากกลยุทธ์ พร้อมข้อความ
- **ร้อยต่อ:** `/ux-design` ถ้ามุมมองแนะนำ redesign `/ux-polish` ถ้ามุมมองแนะนำกระชับ

#### `/ux-copy`: ทบทวน + เขียนใหม่ microcopy

- **คืออะไร:** ประเมินทุกสตริงที่เห็นเทียบกับรูบริกเสียง และผลิตการเขียนใหม่แบบก่อน/หลัง จับ: "form contains errors" (ทั่วไป) "John Doe" (placeholder) copy AI ฉลองสนุก CTA ทั่วไป empty state ตาย error ไร้ประโยชน์
- **ใช้เมื่อไหร่:** โครงสร้างถูกแต่คำอ่อนแอ "Review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "tighten the strings", "the buttons sound generic", "this empty state is dead"
- **ข้ามเมื่อไหร่:** ปัญหา layout (ใช้ `/ux-audit` หรือ `/ux-polish`) ปัญหา copy ที่ขับเคลื่อนด้วยการเข้าถึง เช่น alt text (ใช้ `/ux-a11y`) แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-copy src/views/checkout.blade.php`
- **เอาต์พุต:** เขียน `.ux/last-copy.json` อาร์เรย์ `strings` ของ `{location, severity, before, after, notes}` พร้อมรูบริก + locales ที่ต้องแปล
- **ร้อยต่อ:** `/ux-fix` → ใช้การเขียนใหม่ `/ux-a11y` → ตรวจซ้ำหลังแก้ copy

### Fix & polish

#### `/ux-fix`: นำผลการตรวจมาใช้เป็น commit อะตอม

- **คืออะไร:** อ่านรายงานล่าสุดจาก `.ux/` (audit, copy, a11y, motion หรือ polish) ตรวจสอบ working tree และใช้ผลการตรวจเป็น commit อะตอมผ่านซับเอเจนต์ที่ถูกต้อง ยืนยันซ้ำโดยรันคอมมานด์ต้นทางอีกครั้ง
- **ใช้เมื่อไหร่:** หลังรันคอมมานด์คลาส audit และทบทวนผลตรวจ "Fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it"
- **ข้ามเมื่อไหร่:** ไม่มีรายงานก่อนหน้าใน `.ux/` working tree สกปรกและผู้ใช้ไม่ยอมให้ stash/commit การแก้ต้องการการตัดสินใจด้านการออกแบบ ไม่ใช่การใช้กลไก (ใช้ `/ux-design` สำหรับ redesign)
- **การเรียก:** `/ux-fix` (ตรวจอัตโนมัติว่าจะแก้รายงานไหน) หรือ `/ux-fix --from=last-a11y.json`
- **เอาต์พุต:** commit อะตอมต่อผลตรวจ รันคอมมานด์ต้นทางอีกครั้งและอัปเดตไฟล์ `.ux/last-*.json` พิมพ์สรุป
- **ร้อยต่อ:** `/ux-next` → วาทยกรเลือกการเคลื่อนไหวถัดไป

#### `/ux-polish`: ลูป lint แก้ไข lint ซ้ำ + กำจัด AI slop

- **คืออะไร:** ขั้นแรกเป็นลูปแบบกำหนดผลได้บนไฟล์ HTML ในเครื่อง: lint ขัดเกลาแบบ idempotent หกรอบ แล้ว lint ซ้ำ จนคะแนนถึง 90 คะแนนหยุดขยับ หรือครบสามรอบ (`--rounds` เปลี่ยนเพดาน) โดยค่าเริ่มต้นผลของลูปจะอยู่ที่ `<file>.evolved.html` และไม่แตะไฟล์ต้นฉบับเลย มีเพียง `--loop-only` หรือ `--fix` ที่แทนที่ต้นฉบับ หลังตรวจว่า working tree สะอาด และ quality gate ที่ 65 กันไม่ให้ผลที่ไม่ผ่านไปแทนที่ เว้นแต่ใช้ `--force` เมื่อใช้ `--brand-file` เกณฑ์ขั้นต่ำความซื่อตรงต่อแบรนด์จะคงอยู่ทุกทางออก จากนั้นคือรอบรสนิยม: จังหวะระยะห่าง ลำดับชั้นที่คมขึ้น การตรวจจับ AI slop ความสม่ำเสมอของ token เป็นคู่หูที่ขับเคลื่อนด้วย LLM ของ `/ux-lint` ซึ่งใช้วิจารณญาณของคุณเรื่องรสนิยม `--loop-only` รันแค่ลูป `--no-loop` รันแค่รอบรสนิยม `--fix` นำข้อสังเกตด้านรสนิยมไปใช้
- **ใช้เมื่อไหร่:** โครงสร้างถูกแล้วแต่งานยังหลวม "Polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste", "improve until score 90+", "make it ship-ready"
- **ข้ามเมื่อไหร่:** หน้ายังขาดฟังก์ชันหลัก (แก้ก่อน) ต้องออกแบบใหม่ ไม่ใช่ขัดเกลา (ใช้ `/ux-design`) ปัญหาข้อความ (ใช้ `/ux-copy`) ปัญหาการเคลื่อนไหว (ใช้ `/ux-motion`) ปัญหา a11y (ใช้ `/ux-a11y`)
- **การเรียก:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`
- **เอาต์พุต:** `<file>.evolved.html` จากลูป (แทนที่ต้นฉบับเฉพาะเมื่อใช้ `--loop-only` หรือ `--fix`) โค้ดที่อัปเดตเมื่อใช้ `--fix`, `.ux/last-evolve.json`, หนึ่งบรรทัดใน `.ux/decisions.jsonl` และ `.ux/last-polish.json` ที่อธิบายข้อสังเกตด้านรสนิยม
- **ร้อยต่อ:** `/ux-lint` → ยืนยันว่าการขัดเกลายังคงอยู่ `/ux-a11y` → ตรวจการเข้าถึงอีกครั้ง

### Discovery & การเล่าเรื่อง

#### `/ux-research`: วางแผน + สังเคราะห์งานวิจัย

- **คืออะไร:** โหมดวางแผน: เขียนสคริปต์สัมภาษณ์ แบบสำรวจ ตัวกรองสรรหา โหมดสังเคราะห์ (`--synthesize`): ย่อยสัมภาษณ์ analytics เว็บคู่แข่ง ผล A/B ตั๋ว support เป็นคำแนะนำ มอบหมาย `research-synthesizer`
- **ใช้เมื่อไหร่:** "Plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes"
- **ข้ามเมื่อไหร่:** คำตอบทราบแล้วด้วยความมั่นใจสูง การตัดสินใจที่กลับได้ ความเสี่ยงต่ำ แบ็คเอนด์หรือโครงสร้างพื้นฐาน
- **การเรียก:** `/ux-research --plan "loyalty wallet adoption in MENA"` หรือ `/ux-research --synthesize interviews/*.md`
- **เอาต์พุต:** เขียน `.ux/last-research.json` แผนงานวิจัยหรือธีมที่สังเคราะห์ + หลักฐาน + คำแนะนำ
- **ร้อยต่อ:** `/ux-discover --frame` → รวมข้อค้นพบเข้ากรอบ `/ux-design` → สร้างจากข้อค้นพบ `/ux-workshop` → จัดเวิร์กช็อปโดยใช้งานวิจัยเป็นอินพุต

#### `/ux-workshop`: เวิร์กชอป design thinking 5 ระยะ

- **คืออะไร:** อำนวยความสะดวกเวิร์กชอป discovery / design-thinking ตั้งแต่ต้นจนจบ ห้าระยะตามลำดับ (สำรวจ → heat map → แผนที่ stakeholder → สเก็ตช์โซลูชัน → game plan) จำกัดเวลา artifact เป็นรูปธรรมต่อระยะ จบด้วยการตัดสิน ไม่ใช่ "ผลการตรวจที่น่าสนใจ"
- **ใช้เมื่อไหร่:** คำถามจริง ผู้ร่วมจริง งบเวลาจริง "Run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "kick off the project"
- **ข้ามเมื่อไหร่:** บรีฟชัดเจนและมีขอบเขตแล้ว ระดมสมองคนเดียว (ใช้ `/ux-design` หรือ `/ux-discover --frame`) ทีมอยู่กลางการลงมือทำ ไม่ใช่ช่วง discovery
- **การเรียก:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`
- **เอาต์พุต:** เขียน `.ux/last-workshop.json` game plan + artifact ต่อระยะ
- **ร้อยต่อ:** `/ux-design` → ลงมือ game plan `/ux-research` → เติมช่องว่างที่ workshop ทำให้เห็น `/ux-case-study` → เผยแพร่การเดินทาง

#### `/ux-case-study`: case study ตีพิมพ์ได้ (รูปแบบ Wfrah-editorial)

- **คืออะไร:** สร้างกรณีศึกษาโปรเจ็กต์ในรูปแบบงานบรรณาธิการขาวดำล้วน ตัวอักษร Wfrah เส้นคั่นบาง รหัสเซกชันมีหมายเลขตั้งแต่ (A) ถึง (G) เลย์เอาต์ที่ปลอดภัยสำหรับสองภาษา เป็นเอกสาร ไม่ใช่โบรชัวร์การตลาด อ่านจาก `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`
- **ใช้เมื่อไหร่:** หลัง launch หลัง milestone แยก "Write a case study", "case study this project", "do the wrap-up doc", "publish this work", "portfolio piece"
- **ข้ามเมื่อไหร่:** โปรเจ็กต์ไม่มีข้อมูลพอจะเติมเซกชัน (A) ถึง (G) ผู้ใช้ต้องการหน้าแลนดิ้งการตลาด ไม่ใช่กรณีศึกษา (ใช้ `/ux-design`)
- **การเรียก:** `/ux-case-study --format=html --slug=bashiti-loyalty`
- **เอาต์พุต:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`
- **ร้อยต่อ:** คอมมานด์ปลายทาง มักเป็นจุดจบโปรเจ็กต์

### วาทยกร

#### `/ux-next`: วาทยกร workflow (อ่านอย่างเดียว)

- **คืออะไร:** อ่านทุก `.ux/last-*.json` และระบุชื่อคอมมานด์ถัดไปที่มีคานงัดสูงสุด วาทยกร ไม่ใช่ผู้สร้าง อ่านอย่างเดียว
- **ใช้เมื่อไหร่:** ระหว่างคอมมานด์ "What should I do next", "what's the next move", "decide for me", "where do we go from here"
- **ข้ามเมื่อไหร่:** ไม่มีรายงานก่อนหน้าใน `.ux/` คุณมีคอมมานด์ถัดไปเฉพาะในใจ
- **การเรียก:** `/ux-next` (ไม่มี args) หรือ `/ux-next --focus=a11y`
- **เอาต์พุต:** stdout คอมมานด์ถัดไปที่แนะนำ + เหตุผล
- **ร้อยต่อ:** คอมมานด์ใดก็ตามที่เลือก

#### `/ux-expert`: ตะขอที่ปรึกษา

- **คืออะไร:** เผยข้อมูลติดต่อของผู้สร้างปลั๊กอินเมื่อผู้ใช้ถามถึงผู้เชี่ยวชาญ UX จริง สั้น ตรง ไม่ใช่การตลาด
- **ใช้เมื่อไหร่:** "Who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin"
- **ข้ามเมื่อไหร่:** ผู้ใช้ถามเรื่องฟีเจอร์ของปลั๊กอิน ไม่ใช่การให้คำปรึกษา
- **การเรียก:** `/ux-expert`
- **เอาต์พุต:** การ์ดติดต่อสั้นพร้อม LinkedIn / อีเมล / repo

### Alias ที่จะถูกถอดใน 4.1

คอมมานด์จาก 3.x เจ็ดตัวถูกรวมเข้ากับ 18 ตัวข้างบน ชื่อเดิมยังใช้ได้อีกหนึ่งรุ่น: alias แต่ละตัวจะบอกว่าย้ายไปที่ใด แล้วรันคอมมานด์ใหม่ด้วยอาร์กิวเมนต์เดิม

| คอมมานด์เดิม | ตอนนี้ | หมายเหตุ |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | บล็อกวางกรอบเดิม `.ux/last-frame.json` เดิม |
| `/ux-recommend` | `/ux-discover --recommend` | เครื่องมือ MCP `ux_recommend` ไม่เปลี่ยน |
| `/ux-stats` | `/ux-init --stats` | สแน็ปช็อตแบบอ่านอย่างเดียว |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | alias คงเพดานเดิมห้ารอบ `/ux-polish` เปล่าๆ หยุดที่สามรอบ |
| `/ux-component` | `/ux-design --component` | `.ux/last-component.json` เดิม |
| `/ux-dashboard` | `/ux-design --dashboard` | `.ux/last-dashboard.json` เดิม |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | เอา `--extract-only` ออกเพื่อสร้างจากภาพ |

### กราฟร้อยคอมมานด์

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

## 5 ซับเอเจนต์

ซับเอเจนต์เป็นตัวสร้างเฉพาะบทบาทที่ถูกมอบหมายโดยคอมมานด์ ไม่เคยทำงานอิสระ ถูกเรียกโดย `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research` ฯลฯ แต่ละเอเจนต์มีขอบเขตความรับผิดชอบที่ชัดเจน: ไม่ได้ตัดสินบรีฟ แต่ลงมือทำตามบรีฟ

### `frontend-engineer`

- **เป็นเจ้าของ:** โค้ดฟรอนต์เอนด์คุณภาพ production (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro) ด้วยวินัยต้านสลอป AI
- **มอบหมายโดย:** `/ux-design` (โหมดหน้าเว็บ คอมโพเนนต์ แดชบอร์ด และภาพ), `/ux-fix`
- **อินพุต:** brief + ทิศทางสร้างสรรค์ + โทเค็น (จาก `.ux/last-recommendation.json`)
- **เอาต์พุต:** โค้ดที่ทำงานได้แยกแยะจาก output AI ทั่วไป ไม่มีกราเดียนต์ม่วง ไม่มีฮีโร่จัดกึ่งกลาง ไม่มีสามการ์ดเท่ากัน ไม่มี Inter ในขนาด display ไม่มี "John Doe" ไม่มีอีโมจิ ไม่มีค่าเริ่มต้น 300ms
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### `motion-engineer`

- **เป็นเจ้าของ:** การเคลื่อนไหวในโค้ดฟรอนต์เอนด์ production Framer Motion, GSAP, CSS animation ระยะเวลา easing ออกแบบท่าทาง fallback reduced-motion วินัยประสิทธิภาพ
- **มอบหมายโดย:** `/ux-design` (ทุกโหมด), `/ux-motion --fix`
- **อินพุต:** brief การเคลื่อนไหว + โทเค็น + 57 พรีเซตการเคลื่อนไหวจาก `data/motion-presets.json`
- **เอาต์พุต:** การเคลื่อนไหวที่สมควรมีที่ของมัน ห่อใน fallback `prefers-reduced-motion` เสมอ ทดสอบกับ Core Web Vitals เสมอ
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### `copy-writer`

- **เป็นเจ้าของ:** สตริงที่ส่ง ข้อความ error empty state CTA loading state ข้อความสำเร็จ toast ข้อความช่วย label form ข้อความปุ่ม
- **มอบหมายโดย:** `/ux-copy --fix`, `/ux-design` (ทุกโหมด), `/ux-discover --frame`
- **อินพุต:** โปรไฟล์เสียง (ตั้งชื่อหรือวาง) + สตริงของพื้นผิว
- **เอาต์พุต:** microcopy production ใช้อย่างสม่ำเสมอทุกสถานะของพื้นผิวเพื่อให้สินค้าฟังเหมือนสินค้าเดียว ไม่ใช่สิบ ห้าม: "form contains errors", "John Doe", copy AI ฉลองสนุก, CTA ทั่วไป, empty state ตาย
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### `research-synthesizer`

- **เป็นเจ้าของ:** ย่อยอินพุตงานวิจัย (สัมภาษณ์ analytics เว็บคู่แข่ง ผล A/B ตั๋ว support) เป็นคำแนะนำการออกแบบที่ลงมือได้
- **มอบหมายโดย:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`
- **อินพุต:** งานวิจัยดิบ transcript, export, URL คู่แข่ง, support cluster
- **เอาต์พุต:** ธีม หลักฐาน คำแนะนำ ไม่เคยออกแบบคำตอบ ให้พื้นฐานแก่นักออกแบบเพื่อออกแบบจากนั้น
- **เครื่องมือ:** `Read, Write, WebFetch, Bash, Glob, Grep`

### `design-system-architect`

- **เป็นเจ้าของ:** ระบบการออกแบบเต็มรูปแบบ โทเค็น (สี ตัวอักษร space การเคลื่อนไหว radius shadow) เอกสาร foundation สัญญาคอมโพเนนต์ การจับคู่ dark-mode ชั้น theming
- **มอบหมายโดย:** `/ux-system` และ `/ux-design --component` เมื่อยังไม่มีระบบ
- **อินพุต:** brief แบรนด์ + `.ux/last-recommendation.json` (สไตล์ + พาเลตต์ + คู่ตัวอักษร + พรีเซตการเคลื่อนไหว)
- **เอาต์พุต:** ระบบที่สอดคล้อง มีความเห็น พร้อม production ที่เอเจนต์ปลายน้ำสร้างต่อได้โดยไม่ต้องตัดสินใจพื้นฐานใหม่ โทเค็น JSON foundations MD สัญญาคอมโพเนนต์ การ map dark-mode
- **เครื่องมือ:** `Read, Write, Edit, Bash, Glob, Grep`

### โปรโตคอลมอบหมายซับเอเจนต์

เมื่อคอมมานด์มอบหมายซับเอเจนต์ จะส่ง:

1. brief / คำแนะนำ (โหลดจาก `.ux/`)
2. ส่วนของแมนิเฟสต์ที่เกี่ยวข้อง (เช่น `frontend-engineer` ได้สไตล์ + พาเลตต์ + คอมโพเนนต์ที่เลือก; `motion-engineer` ได้พรีเซตการเคลื่อนไหวที่เลือก)
3. รั้วกัน anti-pattern 171 ตัว (เปิดใช้เสมอ)
4. เกณฑ์ความสำเร็จ (artifact ต้องทำอะไร)

ซับเอเจนต์คืน:

1. artifact (โค้ด เอกสาร ระบบ)
2. บล็อกเหตุผล (ทำไมเลือกแบบนี้)
3. การตรวจสอบตนเองเทียบกับรั้วกัน (กฎไหนที่ยืนยัน)

คอมมานด์ที่เรียกแล้วรัน `/ux-lint` อัตโนมัติก่อนประกาศเสร็จ

---

## 11 แมนิเฟสต์ข้อมูล

ชั้นข้อมูลคือสมอง ทุกคอมมานด์อ่านจากมัน เครื่องยนต์ merge ข้ามมัน ลินเตอร์สแกนกับมัน ทุกไฟล์อยู่ใต้ `data/` และห่อ entry ใน `{_meta, entries}` สำหรับ versioning schema

### `styles.json`: 84 สไตล์การออกแบบ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave ฯลฯ |
| `sample entry` | `swiss-international` "Grid คือกฎ ตัวอักษรทำงานหนัก การประดับคือความล้มเหลว" |

ใช้โดย: `/ux-discover`, `/ux-system`, `/ux-design` Schema: [data/SCHEMAS.md](data/SCHEMAS.md)

### `palettes.json`: 176 พาเลตต์สี

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (สว่าง/มืด), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark ฯลฯ |
| `sample entry` | `claude-warm-editorial` สว่าง warm/editorial/magazine canvas #faf9f5 primary #cc785c |

ใช้โดย: `/ux-discover`, `/ux-system` คอนทราสต์ยืนยันที่ AA / AAA Schema: [data/SCHEMAS.md](data/SCHEMAS.md)

### `type-pairs.json`: 70 คู่ตัวอักษร

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + น้ำหนัก + แหล่ง + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` Cormorant Garamond × Inter × JetBrains Mono |

ทุกตระกูลฟอนต์มีใบอนุญาต + URL แหล่งที่มา ใช้โดย `/ux-discover`, `/ux-system`

### `components.json`: 148 คอมโพเนนต์

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` Mega Navigation, Product Grid anatomy 6 ส่วน 4 สถานะ |

นี่คือคูเมืองที่ใหญ่ที่สุดของเรา ไม่มีปลั๊กอิน UX Claude อื่นที่ส่งแมนิเฟสต์คอมโพเนนต์ที่มีโครงสร้าง

### `industries.json`: 184 กฎอุตสาหกรรม

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific ฯลฯ |
| `sample entry` | `fintech-neobank` ความเชื่อใจสูง การเปิดเผยกฎระเบียบ UI หลักของยอด/ธุรกรรม mobile-first ใช้ประจำวัน |

ใช้โดย recommender (`/ux-discover`) เป็นแกนการค้นหาขนานแรก

### `chart-types.json`: 35 ประเภทกราฟ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical` เปรียบเทียบหมวดแยก 4 ถึง 15 หมวด ตำแหน่งบนแกน x แทนหมวด ความสูงแทนค่า |

ใช้โดย `/ux-design --dashboard` และ `/ux-design --component` (อินสแตนซ์ chart)

### `tech-stacks.json`: 25 สแตก

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` Next.js 15 (App Router), TS/JS, SSR, RSC เข้ากับ Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

สแตกอื่นมี Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025

### `ux-guidelines.json`: 112 กฎ UX ที่มีชื่อ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State ฯลฯ |
| `sample entry` | `hicks-law` เวลาตัดสินใจเพิ่มแบบ logarithm ตามจำนวนตัวเลือกที่นำเสนอ |

ใช้โดย `/ux-audit` (การให้คะแนน 6 เลนส์) และ `/ux-critique` (จุดยึดรสนิยม)

### `motion-presets.json`: 57 พรีเซตการเคลื่อนไหว

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px` 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

ทุกพรีเซตมีตัวแปร reduced-motion โค้ดพร้อมใช้ตามสแตกสำหรับ Framer Motion, GSAP และ CSS บริสุทธิ์

### `anti-patterns.json`: 171 กฎ

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (ชนิด รูปแบบ แฟล็ก ขอบเขต และในหลายกฎมีการตรวจ `post` บนไฟล์ที่ parse แล้ว), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

รายการกฎทั้งหมดอยู่ที่ [171 กฎต้าน AI slop](#171-กฎต้าน-ai-slop-ลินเตอร์)

### `brands/*.json`: 160 สเปกแบรนด์

| ฟิลด์ | คำอธิบาย |
|---|---|
| `entries` | 160 (พร้อม `_index.json` ที่แจกแจงทั้งหมด) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

รายการเต็มใน [160 สเปก DESIGN.md แบรนด์](#160-สเปก-designmd-แบรนด์-แบ่งตามหมวด)

---

## 171 กฎต้าน AI slop: ลินเตอร์

ux-skill มาพร้อมลินเตอร์แบบกำหนดผลได้: แต่ละกฎคือรูปแบบหนึ่ง และหลายกฎเพิ่มการตรวจบน CSS และมาร์กอัปที่ parse แล้ว ดังนั้นการตรงกันจะนับเฉพาะในบริบทที่กฎระบุ **ไม่มี LLM** **ไม่มี API** **ไม่มีเครือข่าย** รันใน CI ราว 200ms บนแอป Next.js ทั่วไป ออกด้วยรหัสไม่ใช่ศูนย์เมื่อพบ Critical / High หากตั้ง `--fail-on high`

กฎมาจาก `data/anti-patterns.json` (v2 แนะนำ) โดยมี `references/foundations/anti-patterns.md` (v1 bash) เป็นทางสำรอง มีไบนารีสองตัว: `bin/ux-lint.py` (Python เร็ว ขยายได้) และ `bin/ux-lint.sh` (Bash + perl-PCRE สำหรับสภาพแวดล้อมที่ไม่มี Python)

### กฎตามหมวด

แค็ตตาล็อกเต็มของกฎทั้ง 171 ข้อ เรียงตามหมวดแล้วตามระดับความรุนแรง ถูกสร้างจาก `data/anti-patterns.json` ไว้ใน [README ภาษาอังกฤษ](README.md#rules-by-category) ซึ่งแสดง ID และชื่อกฎตามที่ลินเตอร์พิมพ์ออกมา กฎครอบคลุม A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2)

### การใช้ลินเตอร์

**สแกนครั้งเดียว:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 สเปก DESIGN.md แบรนด์: แบ่งตามหมวด

แบรนด์จริง ภาษาออกแบบจริง สเปก DESIGN.md จริง ไม่ใช่พาเลตต์ทั่วไป บอกปลั๊กอินว่า "สร้างหน้าแลนดิ้งสไตล์ Stripe" แล้วมันอ่านคำศัพท์แบรนด์จริง: รูบริกเสียง โทเค็นสี ธรรมเนียมการเคลื่อนไหว หมากเซ็น หมากกีดกั้น

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

ปลั๊กอิน UX Claude ยอดนิยมอีก 8 ตัวสร้าง "modern minimal" หรือ "clean dashboard" เวอร์ชันของสุนทรียะค่าเริ่มต้นเดียวกัน ux-skill ให้คุณขอ **ความชัดเจนของ Linear**, **ความจริงจังของ Stripe**, **การยับยั้งชั่งใจของ Apple**, **โมโนลิธของ Tesla**, **ความเป็นมิตรของ Notion**, **วินัยกราเดียนต์ของ Cursor**, **ความหนาแน่นเส้น hairline ของ Raycast**, **editorial อบอุ่นของ Claude** และเครื่องยนต์ดึงโทเค็น เสียง ธรรมเนียมการเคลื่อนไหว หมากเซ็นที่ถูกต้องจากสเปกแบรนด์

---

## เซิร์ฟเวอร์ MCP: หมากอสมมาตร

ux-skill มาพร้อม **เซิร์ฟเวอร์ Model Context Protocol** รัน `ux-mcp` แล้วเครื่องยนต์จะกลายเป็น process stdio ที่รันยาว ซึ่ง host ใดๆ ที่รองรับ MCP (Claude Desktop, Cursor, Windsurf, agent ทั่วไป) เรียกเข้ามาได้ เครื่องมือ 25 ตัว: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check` ใช้ handler Python ชุดเดียวกับสแลชคอมมานด์ manifest ข้อมูลชุดเดียวกัน และ recommender แบบกำหนดผลได้ตัวเดียวกัน

**ทำไมนี่เป็นหมากอสมมาตร:** ไม่มีสกิล UX Claude อันดับต้นแปดตัว (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) ตัวใดที่ส่งเซิร์ฟเวอร์ MCP พวกมันถูกล็อกอยู่ใน runtime ปลั๊กอินของ Claude Code ux-skill เข้าถึงได้จาก host ใดๆ ที่พูด MCP รวมถึง agent ที่ไม่เคยได้ยินเรื่องปลั๊กอิน Claude Code

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

ชี้ client ของคุณไปยัง binary `ux-mcp` เอกสาร tool เต็ม ตัวอย่าง JSON และคอนฟิกต่อ client สำหรับ Claude Desktop, Cursor และ Windsurf อยู่ที่ [docs/mcp.html](docs/mcp.html) และใน `commands/ux-mcp.md`

---

## ตัวติดตั้ง 17 IDE

`uxskill init` (หรือ `/ux-init` ใน Claude Code) ตรวจจับ IDE ที่คุณใช้อัตโนมัติและเขียน artifact ที่ถูกต้อง เครื่องยนต์ Python เดียวกัน คำแนะนำเดียวกัน กาวต่าง IDE

| IDE / เครื่องมือ | สัญญาณตรวจจับ | artifact ที่ติดตั้ง |
|---|---|---|
| Claude Code | `.claude/` หรือ `CLAUDE.md` | manifest ปลั๊กอินที่ `.claude-plugin/plugin.json` + คอมมานด์ทั้ง 18 ตัว (และ alias 7 ตัว) + ซับเอเจนต์ทั้ง 5 ตัว |
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

## กรณีใช้งาน: สถานการณ์รูปธรรม

แปดสถานการณ์จริง เลือกตัวที่ใกล้กับสถานการณ์ของคุณที่สุดและปรับการเรียก

### 1. สร้าง dashboard ฟินเทคใน Cursor

คุณอยู่ใน Cursor ทำ dashboard neobank MENA คุณติดตั้งปลั๊กอินและรัน discovery, คำแนะนำ แล้วสร้าง dashboard

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

/ux-discover --recommend
> [returns picked style, palette, type pair, motion presets, components, brand exemplars]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer generates the page]

/ux-lint .
> [passes, Stripe brand spec was respected]
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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

สามคอมมานด์ หนึ่งพื้นผิวที่ polish แล้ว commit อะตอมต่อการแก้

### 5. ออกแบบ command palette สไตล์ Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

คอมโพเนนต์ที่สร้างใช้โทเค็นสี สแตกตัวอักษร ธรรมเนียมการเคลื่อนไหว ความหนาแน่น hairline จริงของ Linear ไม่ใช่ "dark UI ทั่วไป"

### 6. รันเวิร์กชอป design thinking 90 นาทีกับ stakeholder

คุณมีห้อง 5 คน 90 นาที คุณต้องการให้พวกเขาเดินออกพร้อม game plan ไม่ใช่ vibe

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

ปลั๊กอินอำนวยความสะดวกห้าระยะ (สำรวจ → heat map → แผนที่ stakeholder → สเก็ตช์โซลูชัน → game plan) ตั้งแต่ต้นจนจบ จำกัดเวลา พร้อม artifact ที่เป็นรูปธรรมต่อระยะ เอาต์พุตคือ `.ux/last-workshop.json` game plan ไม่ใช่ "ผลการตรวจที่น่าสนใจ" อย่างเดียว

### 7. เขียน case study ตีพิมพ์ได้หลัง launch

คุณส่ง loyalty wallet คุณต้องการชิ้นงาน portfolio

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

case study เป็น artifact ที่เสร็จและตีพิมพ์ได้ ไม่ใช่ดราฟต์ โมโนโครมบริสุทธิ์ ตัวอักษร editorial พร้อมส่งไปยัง portfolio ของคุณ

### 8. รัน discovery ในบริบทไม่ใช่ AI (แค่การรับที่มีโครงสร้าง)

คุณกำลังขอบเขตโปรเจ็กต์ คุณยังไม่ต้องการคำแนะนำ คุณต้องการ brief ที่มีโครงสร้าง

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

คุณสามารถส่ง JSON ให้ทีมของคุณ วางลงใน Notion doc หรือป้อนเข้า AI tool แยกต่างหาก ux-skill ยังเป็นเครื่องมือรับที่มีโครงสร้างนอกเหนือจากการเป็นเครื่องยนต์

### 9. MASTER.md ถาวร: การตัดสินใจออกแบบของคุณใน repo

หลัง `/ux-discover` (หรือ `/ux-discover --recommend`) บันทึกสไตล์ + พาเลตต์ + ตัวอักษร + การเคลื่อนไหว + คอมโพเนนต์ + แบรนด์ตัวอย่าง + รั้วกันที่เลือก เป็นไฟล์ Markdown ที่อ่านง่าย ให้ทีมของคุณรีวิว diff และเก็บใน version control ได้

```bash
python3 -m engine.cli.main persist save --project-root .
```

เขียน `.ux/design-system/MASTER.md` (YAML frontmatter + body) และ `.ux/design-system/pages/<name>.md` ต่อพื้นผิวที่สร้างผ่าน `persist save-page` Idempotent อินพุตเดียวกันสร้างเอาต์พุตที่เหมือนกันทุก byte ดังนั้นการรันซ้ำบนสถานะที่ไม่เปลี่ยนเป็น no-op ใน git

---

## เปรียบเทียบกับทางเลือกอื่น

ตารางสรุปสั้น เปรียบเทียบตารางต่อตารางเต็มที่ [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)

| มิติ | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| สแลชคอมมานด์ | **18** | 1 | 19 | 1 | 1 | หลายตัว | 1 | 1 | 1 |
| คอมโพเนนต์ | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| พรีเซตการเคลื่อนไหว | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| สเปกแบรนด์ | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| กฎ anti-pattern | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ลินเตอร์เชิงกำหนด CI-safe | **ใช่** | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ |
| IDE รองรับ | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| ประตู discovery | **10 ฟิลด์** | implicit | implicit | implicit | implicit | implicit | implicit | implicit | implicit |
| chain สถานะ `.ux/` | **ใช่** | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ | ไม่ |
| ดาว (2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### การประเมินซื่อสัตย์

- **ui-ux-pro-max** ใหญ่กว่าในด้านการรับรู้ ส่ง 18 IDE มีการค้นหาสไตล์ BM25 บน CSV ของเขา ไม่ส่งแมนิเฟสต์คอมโพเนนต์ แมนิเฟสต์การเคลื่อนไหว ไลบรารีแบรนด์ หรือลินเตอร์เชิงกำหนด
- **open-design** มี 19 สกิล + พรีวิว แต่รองรับเฉพาะ Claude Code และไม่มีชั้นต้านสลอป
- **hallmark** ใกล้ที่สุดในจิตวิญญาณ (ต้านสลอปเช่นกัน) แต่เป็นสกิลเดียว ไม่มีเครื่องยนต์ ไม่มีแมนิเฟสต์ ไม่มีคอมมานด์ที่ร้อยต่อ
- **material-3-skill** ยอดเยี่ยมถ้าคุณต้องการ Material Design 3 โดยเฉพาะ เราไม่แข่งใน MD3

สำหรับรายละเอียดเต็มต่อมิติ ดู [compare.html](https://uxskill.laithjunaidy.com/compare.html)

---

## แผนงาน

ถัดไป โดยยังไม่กำหนดรุ่น:

- **สไตล์ Figma**: effect style สำหรับเงา grid style และ text style ที่ผูกกับตัวแปรของฟิลด์ เขียนลงไฟล์ที่ใช้งานอยู่
- **การจับคู่คอมโพเนนต์**: คอมโพเนนต์ Figma และ variant ของมัน จับคู่กับคอมโพเนนต์ในโค้ดและ props ของมัน คงอยู่ตลอดการส่งต่องาน
- **ตัวนำเข้าเว็บไซต์ที่ใช้งานจริง**: อ่านระบบที่เว็บไซต์ที่เผยแพร่แล้วเรนเดอร์จริง ควบคู่กับตัวนำเข้าไฟล์
- **หน้าเอกสารสำหรับระบบที่สร้างแล้ว**: มุมมองสำหรับคนอ่านของ token บทบาท และสัญญาของระบบ

ที่ยังเปิดอยู่:

- **`uxskill lint --fix` สำหรับการเขียนใหม่อย่างปลอดภัย** ของข้อสังเกตที่แก้แบบกลไกได้ (button-no-type, img-no-alt สตริงว่าง, การลบ console-log-leak)
- **ส่วนขยาย VS Code** ที่แสดงข้อสังเกตจาก lint ในบรรทัด
- **การส่งออกโค้ดต่อคอมโพเนนต์** ในหก stack (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS ล้วน)
- **ตลาดสเปกแบรนด์**: เผยแพร่และค้นหาสเปกแบรนด์จากชุมชน
- **กฎ anti-pattern แบบกำหนดเอง**: การค้นหาและแบ่งปันกฎที่โปรเจ็กต์กำหนดใน `data/anti-patterns.local.json`
- **`uxskill plan`**: วางแผนเว็บไซต์หลายหน้าจากบรีฟ ไม่ใช่แค่หน้าเดียว

---

## การมีส่วนร่วม

issue และ PR ยินดีต้อนรับ สามพื้นที่คานงัดสูง:

### เพิ่มกฎ anti-pattern

1. แก้ `data/anti-patterns.json` เพิ่ม entry พร้อม `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`
2. เพิ่มเทสต์ใน `tests/linter/` ไฟล์หนึ่งที่ทริกเกอร์กฎ ไฟล์หนึ่งที่ไม่
3. รัน `uxskill lint tests/linter/should-trigger/<rule>.tsx` ยืนยันว่ายิง รันบน `tests/linter/should-not-trigger/<rule>.tsx` ยืนยันว่าไม่ยิง
4. เปิด PR

### เพิ่มสเปกแบรนด์

1. สร้าง `data/brands/<slug>.json` พร้อม `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`
2. เพิ่มข้อความที่สอดคล้องที่ `references/brands/<slug>.md`
3. ลงทะเบียนใน `data/brands/_index.json`
4. เปิด PR สเปกต้องถูก backed ด้วยการอ้างอิงแหล่งหลัก (ผลิตภัณฑ์จริงของแบรนด์ ระบบการออกแบบสาธารณะ หรือ DESIGN.md ถ้าพวกเขาเผยแพร่)

### เพิ่มพรีเซตการเคลื่อนไหว

1. แก้ `data/motion-presets.json` เพิ่ม entry พร้อม `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`
2. พรีเซตต้องมีตัวแปร reduced-motion ไม่มีข้อยกเว้น
3. เปิด PR

### กระบวนการ

- อ่าน [CONTRIBUTING.md](CONTRIBUTING.md) สำหรับกระบวนการเต็ม
- อ่าน [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- กฎและสเปกแบรนด์ใหม่ถูกรีวิวสำหรับ: การยึดแหล่งหลัก ไม่ overfit กับโปรเจ็กต์เดียว ไม่มีอีโมจิในข้อมูลใดๆ พฤติกรรมปลอดภัย RTL เมื่อนำไปใช้ได้

---

## ใบอนุญาต ผู้แต่ง คำขอบคุณ

### ใบอนุญาต

MIT ใช้ fork สร้างต่อจากมัน ถ้ามันช่วยคุณจากการส่งสลอป AI ติดดาวให้ repo เป็นวิธีสนับสนุนที่ถูกที่สุด

### ผู้แต่ง

**Laith Aljunaidy**: ผู้ก่อตั้งคนเดียวของ [Dot](https://thedotwallet.com) แพลตฟอร์ม loyalty MENA-first สร้าง ux-skill เพื่อให้ฟรอนต์เอนด์ที่ AI สร้างไม่ดูเหมือนกันหมด

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- อีเมล: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- เว็บไซต์: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### คำขอบคุณ

- ทีม Anthropic สำหรับ Claude Code และสถาปัตยกรรม skill / plugin ที่ทำให้สิ่งนี้แจกจ่ายได้
- Nielsen Norman Group, Laws of UX (lawsofux.com) และชุมชนวิจัย UX ที่ผลงานของพวกเขาช่วยให้ข้อมูล `data/ux-guidelines.json`
- ทุกแบรนด์ที่ระบุใน `data/brands/` ระบบการออกแบบสาธารณะของพวกเขาคือแหล่งความจริงสำหรับสเปกแบรนด์
- ผู้สนับสนุน v1 ดั้งเดิม: สกิล Claude แบบช็อตเดียวที่กลายเป็นเมล็ดพันธุ์สำหรับเครื่องยนต์ Python v2
- ปลั๊กอิน UX Claude ยอดนิยม 8 ตัวที่เราเปรียบเทียบด้วย พวกเขายกระดับมาตรฐาน นี่คือคำตอบของเรา

---

**ux-skill** · **v4.0.0** · สร้างเพื่อให้ Claude Code, Cursor, Windsurf และเครื่องมือเขียนโค้ดด้วย AI ทุกตัวอื่นๆ ส่งออกฟรอนต์เอนด์ที่ไม่อ่านเหมือน AI สร้าง

> ติดดาว repo ที่ [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · ติดตั้งผ่าน `pip install uxskill` หรือ `npx uxskill init` · เปรียบเทียบที่ [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
