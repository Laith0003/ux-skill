[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · **Tiếng Việt** · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill — bộ máy trí tuệ thiết kế cho Claude Code, Cursor và mọi công cụ lập trình AI khác

> **Plugin UX mạnh nhất cho lập trình AI.** Một lõi suy luận Python với 11 manifest JSON truy vấn được (84 phong cách, 176 bảng màu, 70 cặp typography, 148 component, 184 ngành nghề, 35 loại biểu đồ, 57 preset chuyển động, 112 quy luật UX, 145 quy tắc anti-pattern, 25 tech stack, 160 spec thương hiệu), 22 slash command, 5 sub-agent và một bộ linter chống AI-slop xác định. Liên-IDE: triển khai vào Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer và Roo Cline.

> **Tên thương hiệu là `ux-skill`.** Tên gói PyPI / npm vẫn là `uxskill`. Kho GitHub nằm tại [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Trang chủ:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **So sánh với mọi plugin UX cho Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-3.0.0-stable-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#trình-cài-đặt-17-ide)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-145-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-223_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Lịch sử sao

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill là gì

ux-skill là một **bộ máy trí tuệ thiết kế** dành cho các công cụ lập trình AI. Nó chạy như một gói Python (`pip install uxskill`), như một plugin của Claude Code, và như một trình cài đặt đa-IDE cho 17 môi trường. Bộ máy nhận vào một brief dự án (ngành nghề, đối tượng, tone, yêu-cầu-bắt-buộc, điều-cấm-kỵ, stack, khu vực) và trả về một hệ thống thiết kế được khuyến nghị đầy đủ: phong cách, bảng màu, cặp typography, preset chuyển động, component, các thương hiệu hình mẫu để nghiên cứu và những rào chắn anti-pattern phải tuân thủ. Khuyến nghị mang tính xác định — cùng một đầu vào luôn tạo ra cùng một đầu ra.

Plugin nằm giữa bạn và công cụ lập trình AI. Khi bạn yêu cầu Claude Code, Cursor hay bất kỳ trợ lý AI nào "xây một landing page fintech", trợ lý thường ứng tác — và kết quả lộ ra là do AI tạo ra trong vòng năm giây (gradient từ tím sang xanh, ba thẻ bằng nhau, Inter ở kích thước display, "John Doe" trong testimonial, transition mặc định 300ms, hero căn giữa, mũi tên CTA nảy lên xuống). ux-skill thay thế việc ứng tác bằng **những ràng buộc có cấu trúc**: bạn chạy `/ux-discover` để nắm bắt brief, `/ux-recommend` để chọn hệ thống, `/ux-design` để sinh mã, và `/ux-lint` để xác minh code vượt qua 145 quy tắc chống AI-slop xác định trước khi commit.

README này là tài liệu tham chiếu chính thức. Mọi command, mọi sub-agent, mọi data manifest, mọi đường cài đặt, mọi spec thương hiệu, mọi danh mục anti-pattern — tất cả đều được tài liệu hóa ở đây. Nếu bạn đang tìm một plugin thiết kế cho Claude Code hoặc so sánh các công cụ thiết kế AI cho Cursor, Windsurf hay Codex, hãy đọc tài liệu này từ đầu đến cuối song song với [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Mục lục

1. [Cài đặt nhanh](#cài-đặt-nhanh)
2. [Những con số — so sánh trực tiếp với 8 skill UX hàng đầu cho Claude](#những-con-số--so-sánh-trực-tiếp-với-8-skill-ux-hàng-đầu-cho-claude)
3. [Kiến trúc — các mảnh ghép khớp với nhau thế nào](#kiến-trúc--các-mảnh-ghép-khớp-với-nhau-thế-nào)
4. [22 slash command — tham chiếu chi tiết](#22-slash-command--tham-chiếu-chi-tiết)
5. [5 sub-agent](#5-sub-agent)
6. [11 data manifest](#11-data-manifest)
7. [145 quy tắc chống AI-slop — bộ linter](#145-quy-tắc-chống-ai-slop--bộ-linter)
8. [160 spec DESIGN.md thương hiệu — theo danh mục](#160-spec-designmd-thương-hiệu--theo-danh-mục)
9. [Máy chủ MCP — nước cờ bất đối xứng](#máy-chủ-mcp--nước-cờ-bất-đối-xứng)
10. [Trình cài đặt 17 IDE](#trình-cài-đặt-17-ide)
11. [Tình huống sử dụng — kịch bản cụ thể](#tình-huống-sử-dụng--kịch-bản-cụ-thể)
12. [So sánh với các lựa chọn khác](#so-sánh-với-các-lựa-chọn-khác)
13. [Lộ trình](#lộ-trình)
14. [Đóng góp](#đóng-góp)
15. [Giấy phép, tác giả, lời cảm ơn](#giấy-phép-tác-giả-lời-cảm-ơn)

---

## Cài đặt nhanh

Ba đường cài đặt. Chọn đường phù hợp với môi trường của bạn.

### Đường 1 — chợ Claude Code (chính thống)

Nếu bạn làm việc trong Claude Code, cài qua chợ plugin:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Điều đó kết nối toàn bộ 22 slash command và 5 sub-agent vào phiên Claude Code của bạn. Sau khi cài, chạy `/ux-init` để thiết lập thư mục state `.ux/` cho dự án và xác minh rằng bộ máy Python có thể truy cập được.

### Đường 2 — pip (đa năng)

Nếu bạn làm việc ngoài Claude Code (Cursor, Windsurf, CLI, CI), cài gói Python:

```bash
pip install uxskill
uxskill init                       # tự phát hiện IDE, cài đúng artifact
uxskill stats                      # in ra số đếm manifest để xác minh cài đặt
uxskill lint .                     # chạy linter trên thư mục hiện tại
```

Gói cung cấp cả `ux` và `uxskill` làm entry point CLI — chúng là cùng một binary.

### Đường 3 — npx (không cần Python)

Nếu bạn không muốn quản lý Python trực tiếp, wrapper npx tự bootstrap mọi thứ qua `pipx`:

```bash
npx uxskill init                  # tải pipx + uxskill ngay lần chạy đầu
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Xác minh cài đặt

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

Nếu bất kỳ số đếm nào trả về 0, file JSON đang thiếu — mở một issue tại [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Những con số — so sánh trực tiếp với 8 skill UX hàng đầu cho Claude

Số sao được xác minh lần cuối qua `gh api` vào **2026-05-28**. ux-skill (Laith0003/ux-skill) là người mới nhất gia nhập — chúng tôi nhỏ về độ nhận biết, sâu về kiến trúc. Bảng so sánh dưới đây thành thật: chỗ chúng tôi thua, chỗ chúng tôi thắng.

| Plugin | Sao | Kiến trúc | Slash command | Linter (CI-safe) | Spec thương hiệu | Component | Preset chuyển động | IDE hỗ trợ |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, một skill duy nhất | 1 | — | — | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | — | — | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + gu thẩm mỹ dựa trên nghiên cứu | 1 | — | — | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Một SKILL.md 62 KB + script | 1 | — | — | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Thư viện skill nối với MCP | nhiều | — | — | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill thẩm mỹ đơn nhất | 1 | — | — | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill thiết kế anti-slop | 1 | — | — | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Component MD3 + audit | 1 | — | (chỉ MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Bộ máy Python + 11 manifest + 22 command + 5 sub-agent + linter CI** | **22** | **145 quy tắc regex** | **160** | **148** | **57** | **17** |

### Chỗ chúng tôi thua

- **Độ nhận biết.** Họ có hàng trăm nghìn sao. Chúng tôi có 14. Hãy gắn sao cho repo — đó là cách rẻ nhất để giúp.
- **Nhận diện thương hiệu.** ui-ux-pro-max và open-design có một lợi thế đi trước được đo bằng tháng, không phải ngày.
- **Bóng bẩy marketing.** Họ có screenshot, video demo, và một landing page dễ khám phá. Chúng tôi có một README đầy đủ và một landing mỏng.

### Chỗ chúng tôi thắng

- **Thư viện component:** 148 component được tài liệu hóa với anatomy, state, token sử dụng, và spec chuyển động. Không có cái nào trong 8 plugin kia ship được manifest component.
- **Preset chuyển động:** 57 entry sẵn sàng theo stack (Framer Motion, GSAP, CSS) với fallback reduced-motion. Không có ai trong số còn lại ship manifest chuyển động.
- **Linter anti-pattern:** 145 quy tắc regex xác định, chạy trong CI, exit khác 0 ở mức Critical/High. Không có ai trong số còn lại ship một linter xác định.
- **Spec thương hiệu:** 160 spec DESIGN.md thật (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude, và 146 thương hiệu khác). Không có ai trong số còn lại ship một thư viện thương hiệu.
- **17 IDE được hỗ trợ:** cùng một bộ máy, keo dán khác nhau cho mỗi IDE.
- **22 slash command:** discovery, generation, audit, lint, polish, vòng lặp fix, case study, workshop, copy, motion, a11y, dashboard, conductor — tích hợp đầy đủ.

Bảng so sánh đầy đủ cạnh nhau tại [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Kiến trúc — các mảnh ghép khớp với nhau thế nào

```
ux-skill (tên gói: uxskill)
│
├── data/                              Bộ não — các manifest JSON truy vấn được
│   ├── styles.json                    84 phong cách thiết kế + when/skip + token
│   ├── palettes.json                  176 bảng màu (sáng/tối, đã xác minh contrast)
│   ├── type-pairs.json                70 bộ ba display × body × mono
│   ├── components.json                148 component (anatomy, state, motion)
│   ├── industries.json                184 quy tắc ngành nghề + tín hiệu đối tượng
│   ├── chart-types.json               35 loại biểu đồ (when/skip, encoding)
│   ├── tech-stacks.json               25 stack (Next, Astro, SvelteKit, Blade...)
│   ├── ux-guidelines.json             112 quy luật UX có tên (Hick, Fitts, Miller...)
│   ├── motion-presets.json            57 preset chuyển động (entry, exit, hover...)
│   ├── anti-patterns.json             145 quy tắc regex (nguồn linter CI-safe)
│   └── brands/*.json                  160 spec DESIGN thương hiệu + _index.json
│
├── engine/                            Python — phần suy luận
│   ├── recommender/                   bộ máy merge 5 tìm kiếm song song
│   ├── linter/                        bộ quét anti-slop xác định
│   ├── discovery/                     giao thức ép buộc 10 trường
│   ├── generator/                     bộ phát token + manifest
│   ├── installer/                     trình cài đặt đa 17 IDE
│   └── cli/                           entry point `ux` / `uxskill`
│
├── commands/                          22 slash command Claude Code (.md)
│   ├── ux-init.md                     khởi động
│   ├── ux-stats.md                    chụp nhanh kiểm kê
│   ├── ux-discover.md                 thu thập 10 trường (cổng)
│   ├── ux-recommend.md                CHỦ LỰC — tìm kiếm song song 5 luồng
│   ├── ux-lint.md                     linter xác định
│   ├── ux-design.md                   sinh code frontend
│   ├── ux-component.md                sinh một component
│   ├── ux-system.md                   sinh hệ thống thiết kế đầy đủ
│   ├── ux-dashboard.md                sinh bề mặt dashboard
│   ├── ux-motion.md                   xử lý chuyển động + audit
│   ├── ux-audit.md                    audit thiết kế 6 lăng kính
│   ├── ux-a11y.md                     audit WCAG 2.1 AA
│   ├── ux-critique.md                 phê bình thẩm mỹ (3 điểm thắng, 3 điểm trượt, 1 nước cờ)
│   ├── ux-copy.md                     đánh giá + viết lại microcopy
│   ├── ux-fix.md                      áp dụng phát hiện thành các commit nguyên tử
│   ├── ux-polish.md                   pass mỹ thuật + diệt AI-slop
│   ├── ux-frame.md                    khối framing 4 trường
│   ├── ux-research.md                 lên kế hoạch + tổng hợp nghiên cứu
│   ├── ux-workshop.md                 workshop design thinking 5 giai đoạn
│   ├── ux-case-study.md               case study có thể xuất bản phong cách Wfrah-editorial
│   ├── ux-next.md                     nhạc trưởng workflow (chỉ đọc)
│   └── ux-expert.md                   móc nối tư vấn
│
├── agents/                            5 sub-agent (.md)
│   ├── frontend-engineer.md           React/Next/Vue/Blade/Astro
│   ├── motion-engineer.md             Framer Motion / GSAP / CSS
│   ├── copy-writer.md                 microcopy theo giọng thương hiệu
│   ├── research-synthesizer.md        phỏng vấn + analytics + đối thủ
│   └── design-system-architect.md     token / component / nền tảng
│
├── references/                        Nguồn văn xuôi cho dữ liệu + trang demo
│   ├── foundations/                   anti-patterns.md, nguyên tắc, gu thẩm mỹ
│   ├── laws/                          quy luật UX dạng dài
│   ├── process/                       discovery-protocol.md (cốt lõi)
│   ├── styles/                        văn xuôi theo phong cách (anti-slop.md, v.v.)
│   ├── components/                    component dạng dài
│   ├── output/                        rubric đầu ra
│   └── conditional/                   hướng dẫn riêng theo stack
│
├── bin/
│   ├── uxskill.mjs                    wrapper npx -> bộ máy Python
│   ├── ux-lint.py                     linter v2 (ưu tiên)
│   └── ux-lint.sh                     fallback v1 (bash + perl-PCRE)
│
└── .ux/                               (tạo ra cho mỗi dự án)
    ├── last-discovery.json            ảnh chụp brief
    ├── last-recommendation.json       hệ thống đã chọn
    ├── last-frame.json                khối framing
    ├── last-audit.json / last-a11y.json / last-copy.json / last-motion.json
    ├── last-design.json / last-component.json / last-dashboard.json
    └── last-critique.json / last-polish.json / last-research.json / last-workshop.json / last-case-study.json
```

### Bộ máy thực sự hoạt động như thế nào

1. **Đầu vào.** Bạn cung cấp một brief — tương tác qua `/ux-discover` (10 trường) hoặc không tương tác qua flag truyền vào `ux recommend`.
2. **5 tìm kiếm song song.** Bộ máy chạy năm lookup đồng thời trên các manifest:
   - **Ngành nghề → recommended_styles** (industries.json)
   - **Phong cách → tương thích bảng màu + typography + chuyển động** (styles.json)
   - **Tone × yêu-cầu-bắt-buộc → bộ lọc bảng màu** (palettes.json)
   - **Stack → tương thích component + preset chuyển động** (tech-stacks.json, motion-presets.json)
   - **Điều-cấm-kỵ + khu vực → rào chắn + danh sách rút gọn thương hiệu hình mẫu** (anti-patterns.json, brands/)
3. **Merge.** Một bộ merger xác định xếp hạng các ứng viên, giải quyết xung đột (ví dụ, yêu-cầu-bắt-buộc dark-mode ép chế độ bảng màu), và phát ra một hệ thống được khuyến nghị duy nhất.
4. **Đầu ra.** Một tài liệu JSON với phong cách đã chọn, bảng màu đã chọn, cặp typography, top 5 preset chuyển động, top 12 component, top 5 thương hiệu hình mẫu và toàn bộ 145 rào chắn anti-pattern được kích hoạt. Cộng với một khối lý giải cho từng lựa chọn.
5. **Sinh code.** Các command phía sau (`/ux-design`, `/ux-component`, `/ux-system`, `/ux-dashboard`) tiêu thụ khuyến nghị để sinh ra code thật qua các sub-agent.
6. **Xác minh.** `/ux-lint` quét lại code đã sinh trên 145 quy tắc regex. Exit khác 0 ở Critical/High trong CI.

**Python suy nghĩ. HTML hiển thị. Markdown nối chuỗi.**

---

## 22 slash command — tham chiếu chi tiết

Mỗi command được ship như một file `.md` dưới `commands/` với `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process`, và `output state file`. Mô tả bên dưới là rút gọn; nguồn đầy đủ chính là spec chính thức.

Các command được nhóm thành năm xô: **khởi động & kiểm kê**, **discovery & khuyến nghị**, **sinh code**, **audit & xác minh**, **fix & polish**, và **nhạc trưởng**.

### Khởi động & kiểm kê

#### `/ux-init` — khởi động dự án

- **Là gì:** Phát hiện IDE bạn đang dùng (`.claude/`, `.cursor/`, `.windsurf/`, v.v.), cài đúng artifact, xác minh bộ máy Python có thể truy cập được, in ra ảnh chụp số liệu.
- **Khi dùng:** Lần đầu cài trong một dự án mới. Sau khi clone một dự án dùng ux-skill. Sau `pip install --upgrade uxskill`.
- **Khi bỏ qua:** Bạn đã chạy trong dự án này và không có gì thay đổi.
- **Gọi:** `/ux-init` (không tham số) hoặc `uxskill init` từ CLI.
- **Đầu ra:** Artifact theo IDE (xem [Trình cài đặt 17 IDE](#trình-cài-đặt-17-ide)) + thư mục `.ux/` + tóm tắt qua stdout.
- **Nối vào:** `/ux-discover` kế tiếp.

#### `/ux-stats` — in kiểm kê dữ liệu

- **Là gì:** In version + số đếm entry cho 11 data manifest, để bạn có thể xác minh những gì đã cài.
- **Khi dùng:** Sau khi cài. Sau khi nâng cấp. Khi `/ux-recommend` trả về lựa chọn bất ngờ và bạn nghi ngờ manifest chưa đầy đủ.
- **Khi bỏ qua:** Không bao giờ — đây là command chỉ đọc 50ms.
- **Gọi:** `/ux-stats` hoặc `uxskill stats`.
- **Đầu ra:** JSON ra stdout (xem [Xác minh cài đặt](#xác-minh-cài-đặt) ở trên).
- **Nối vào:** Chỉ chẩn đoán; không nối vào bước sau.

### Discovery & khuyến nghị

#### `/ux-discover` — hàm cưỡng bức (thu thập 10 trường)

- **Là gì:** Bước thu thập 10 trường bắt buộc mà mọi dự án đi qua trước bất kỳ command sinh code nào. Loại dự án, đối tượng, mục tiêu chính, tone, yêu-cầu-bắt-buộc, điều-cấm-kỵ, thương hiệu tham chiếu, stack, khu vực, chỉ số thành công. **Không ứng tác.** Các cụm từ bị cấm ("modern", "clean") ép người dùng phải cụ thể.
- **Khi dùng:** Trước bất kỳ `/ux-design`, `/ux-component`, `/ux-system`, hoặc `/ux-dashboard` nào. Bất cứ khi brief trước đã cũ.
- **Khi bỏ qua:** Bạn đang sửa lỗi (`/ux-fix`). Bạn chỉ chạy linter (`/ux-lint`). Brief không thay đổi từ phiên trước.
- **Gọi:** `/ux-discover`. Plugin hỏi; bạn trả lời.
- **Đầu ra:** Ghi `.ux/last-discovery.json` (brief 10 trường).
- **Nối vào:** `/ux-recommend` → dùng discovery để chọn phong cách + bảng màu + typography + motion + component. `/ux-design [brief bổ sung]` → sinh code frontend neo theo khuyến nghị. `/ux-component <tên>` → sinh một component khớp với các ràng buộc được khám phá.

#### `/ux-recommend` — bộ máy chủ lực 5 tìm kiếm song song

- **Là gì:** Chạy 5-tìm-kiếm-song-song của bộ máy Python trên 11 manifest và trả về một hệ thống thiết kế được merge. Ngành nghề → Phong cách → Bảng màu → Typography → Motion + Component + Thương hiệu hình mẫu + Rào chắn.
- **Khi dùng:** Bắt đầu một dự án mới từ con số không. Pivot một sản phẩm đã mệt. Bay tiền trạm trước bất kỳ `/ux-design` hay `/ux-component` nào.
- **Khi bỏ qua:** Bạn đã chạy `/ux-discover` và lưu một brief — `/ux-recommend` tự động trong flow đó. Bạn đang sửa một lỗi (dùng `/ux-fix`). Bạn chỉ cần lint (dùng `/ux-lint`).
- **Gọi (Claude Code):**
  ```
  /ux-recommend
  ```
  **Gọi (CLI):**
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
- **Đầu ra:** Ghi `.ux/last-recommendation.json` — phong cách đã chọn, bảng màu đã chọn, cặp typography đã chọn, top 5 preset chuyển động, top 12 component, top 5 thương hiệu hình mẫu, toàn bộ 145 rào chắn anti-pattern được kích hoạt, kèm lý giải.
- **Nối vào:** `/ux-design [brief]` → code frontend dùng token được khuyến nghị. `/ux-system` → hệ thống thiết kế đầy đủ từ khuyến nghị. `/ux-component <tên>` → một component dùng phong cách được khuyến nghị. `/ux-lint` → xác minh code đã sinh.

### Sinh code

#### `/ux-design` — sinh một bề mặt đẹp, chống slop từ một brief

- **Là gì:** Sinh một artifact frontend hoàn chỉnh, chất lượng production (landing, marketing site, app shell) từ brief discovery + khuyến nghị. Điều phối `frontend-engineer` với hướng sáng tạo từ tham chiếu anti-slop và kho vũ khí.
- **Khi dùng:** "Design a", "build me a", "generate a landing page", "create a dashboard", "make a component" — bất kỳ yêu cầu sản phẩm hình ảnh tự do nào.
- **Khi bỏ qua:** Bạn muốn review, không phải build (dùng `/ux-audit` hoặc `/ux-critique`). Bạn chỉ muốn một component (dùng `/ux-component`). Việc backend hay hạ tầng.
- **Gọi:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`.
- **Đầu ra:** Code được sinh (HTML / Blade / JSX / Vue / Astro), cộng với `.ux/last-design.json`.
- **Nối vào:** `/ux-lint` → xác minh đối chiếu rào chắn. `/ux-polish` → pass mỹ thuật. `/ux-a11y` → audit khả năng truy cập. `/ux-copy` → review microcopy. `/ux-fix` → áp dụng phát hiện thành các commit nguyên tử.

#### `/ux-component` — sinh một component

- **Là gì:** Tạo ra một component đơn lẻ chất lượng production (button, modal, navbar, sidebar, card, table, form, chart) từ một spec. Đủ bốn trạng thái tương tác, có khả năng truy cập, đúng thương hiệu. Tra component trong `.ux/last-recommendation.json` trước, dự phòng truy vấn trực tiếp manifest.
- **Khi dùng:** Bất kỳ yêu cầu một-thành-phần nào — "build a button", "create a pricing card", "make a modal", "add a navbar", "design a sidebar", "I need a data table", "build a form", "make a chart component".
- **Khi bỏ qua:** Trang đầy đủ hoặc bề mặt nhiều section (dùng `/ux-design`). Backend hay hạ tầng.
- **Gọi:** `/ux-component pricing-card-trio --brief="fintech, dark, monospace numbers"`.
- **Đầu ra:** Code component được sinh, cộng với `.ux/last-component.json`.
- **Nối vào:** `/ux-lint` → xác minh. `/ux-polish` → siết chặt.

#### `/ux-system` — sinh một hệ thống thiết kế khởi đầu đầy đủ

- **Là gì:** Đề xuất một hệ thống thiết kế khởi đầu đầy đủ cho dự án chưa có — token (màu, typography, không gian, motion, radius, shadow), tài liệu nền tảng, hợp đồng component, cặp dark-mode, công tắc theme. Điều phối `design-system-architect`.
- **Khi dùng:** "We don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS".
- **Khi bỏ qua:** Dự án đã có hệ thống thiết kế — dùng `/ux-component` đối chiếu hệ thống hiện có thay vào. Backend hay hạ tầng.
- **Gọi:** `/ux-system` (chạy discovery trước nếu chưa có sẵn file).
- **Đầu ra:** `tokens.json`, `foundations.md`, các hợp đồng `components/*.md`, phát Tailwind / vanilla / SCSS tùy chọn. Ghi `.ux/last-system.json` cho ngữ cảnh chuỗi.
- **Nối vào:** `/ux-component` → build đối chiếu hệ thống mới. `/ux-design` → sinh một bề mặt dùng token mới.

#### `/ux-dashboard` — sinh dashboard chuyên dụng

- **Là gì:** Dashboard với kỷ luật mật độ dữ liệu — layout bento, số monospace dạng bảng, mẫu sparkline, chống lạm dụng card, màu state có nghĩa, motion tiết chế. Không phải landing marketing dán chart lên.
- **Khi dùng:** "Build a dashboard", "design the admin panel", "make a metrics page", "operator console", "analytics view", "KPI board", "monitoring screen".
- **Khi bỏ qua:** Landing marketing có thống kê (dùng `/ux-design`). Chỉ một widget (dùng `/ux-component`). Backend hay hạ tầng.
- **Gọi:** `/ux-dashboard`.
- **Đầu ra:** Code dashboard được sinh + `.ux/last-dashboard.json`.
- **Nối vào:** `/ux-lint`, `/ux-audit`, `/ux-a11y`.

#### `/ux-motion` — xử lý chuyển động

- **Là gì:** Sinh lớp chuyển động của một bề mặt — thời lượng, easing, biên đạo, fallback reduced-motion, kỷ luật hiệu năng. Cũng audit chuyển động hiện có đối chiếu 5 chiều (timing, easing, ý nghĩa, reduced-motion, hiệu năng).
- **Khi dùng:** "Motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "performance pass on the motion".
- **Khi bỏ qua:** Bề mặt không có chuyển động (dùng `/ux-audit` hoặc `/ux-polish`). Backend hay hạ tầng.
- **Gọi:** `/ux-motion path/to/component.tsx` (chế độ audit) hoặc `/ux-motion --generate hero-entry` (sinh).
- **Đầu ra:** Code cập nhật (ở chế độ sinh) hoặc báo cáo `.ux/last-motion.json` (ở chế độ audit).
- **Nối vào:** `/ux-fix` → áp dụng phát hiện motion. `/ux-polish` → siết chặt.

### Audit & xác minh

#### `/ux-lint` — linter dựa trên regex xác định (không LLM, CI-safe)

- **Là gì:** Chạy 145 quy tắc regex trên code của bạn. Không gọi LLM. Exit khác 0 ở Critical / High trong CI. Nguồn: `data/anti-patterns.json`. Quy tắc bao trùm A11y (23), Nội dung (15), Layout (13), Typography (10), Màu (9), Chất lượng (9), Visual (9), Motion (8), Hiệu năng (4).
- **Khi dùng:** Pre-commit hook. Cổng CI. Pass đầu nhanh trên codebase lớn trước khi trả giá `/ux-audit`. Sau `/ux-design` hoặc `/ux-component` để xác minh việc sinh.
- **Khi bỏ qua:** Bạn muốn vòng lặp fix (linter báo cáo, không sửa — nối vào `/ux-polish --fix` hoặc `/ux-fix`). Bạn muốn phán xét gu thẩm mỹ (dùng `/ux-critique`).
- **Gọi (slash):** `/ux-lint src/`.
- **Gọi (CLI):** `uxskill lint .` hoặc `python3 bin/ux-lint.py .` hoặc `bash bin/ux-lint.sh --ci --fail-on high`.
- **Gọi (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Đầu ra:** Phát hiện ra stdout (vị trí, id quy tắc, mức độ, bằng chứng). Exit code 0 nếu sạch, khác 0 ở Critical/High khi đặt `--fail-on high`.
- **Nối vào:** `/ux-polish --fix` → đối tác được dẫn dắt bởi LLM trên cùng mẫu. `/ux-fix` → áp dụng phát hiện thành commit, sắp xếp theo mức độ. `/ux-audit` → pass suy luận 6 lăng kính đầy đủ. `/ux-next` → để nhạc trưởng quyết định.

#### `/ux-audit` — audit thiết kế 6 lăng kính

- **Là gì:** Một review có cấu trúc, có chính kiến đối chiếu sáu lăng kính (rõ ràng, phân cấp, khả năng truy cập, giọng nói, motion, gu thẩm mỹ), sinh ra phát hiện được gắn nhãn mức độ. Báo cáo phong cách Polaris. Đọc `.ux/last-frame.json` trước — đối tượng và outcome neo mức độ của mỗi phát hiện.
- **Khi dùng:** Bề mặt tồn tại và bạn muốn một phê bình có thể bảo vệ được. "Audit", "review the ux", "is this any good", "what's broken", "tear this apart".
- **Khi bỏ qua:** Bề mặt chưa tồn tại (dùng `/ux-design`). Người dùng muốn một lăng kính (dùng command nhắm mục tiêu: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Người dùng muốn ý kiến gu thẩm mỹ (dùng `/ux-critique`). Backend hay hạ tầng.
- **Gọi:** `/ux-audit https://example.com/pricing` hoặc `/ux-audit src/components/Pricing.tsx`.
- **Đầu ra:** Ghi `.ux/last-audit.json` — mảng `findings` gồm `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Nối vào:** `/ux-fix` → áp dụng phát hiện. `/ux-polish` → pass mỹ thuật. `/ux-design` → nếu cần redesign cấu trúc.

#### `/ux-a11y` — audit WCAG 2.1 AA + các kiểm tra lịch sự thông thường

- **Là gì:** Một audit WCAG 2.1 AA có cấu trúc, cộng với các kiểm tra lịch sự thông thường mà công cụ tự động vượt qua nhưng vẫn làm tổn thương người dùng thật (khả năng nhìn thấy focus, độ cụ thể của lỗi, ưu tiên chuyển động, bẫy bàn phím, phụ thuộc màu sắc).
- **Khi dùng:** Cổng khả năng truy cập trước khi ship. Sau một redesign. "Accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check".
- **Khi bỏ qua:** Không hướng người dùng. Backend hay hạ tầng. Phác thảo work-in-progress.
- **Gọi:** `/ux-a11y https://example.com` (ưu tiên URL trực tiếp — công cụ tự động và kiểm tra bàn phím chỉ hoạt động khi live).
- **Đầu ra:** Ghi `.ux/last-a11y.json` — mảng `findings` gồm `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, mảng `beyond_wcag`, `severity_counts`.
- **Nối vào:** `/ux-fix` → áp dụng phát hiện thành commit. `/ux-copy` → sửa alt text và đấu nối lỗi form như một phần của pass copy.

#### `/ux-critique` — gọi gu thẩm mỹ (3 điểm thắng, 3 điểm trượt, 1 nước cờ chiến lược)

- **Là gì:** Ý kiến của một nhà thiết kế — không phải audit có cấu trúc, không phải điểm mức độ, chỉ là một quan điểm chặt chẽ có chính kiến gọi tên cái gì đang ổn, cái gì không, và một nước cờ chiến lược sẽ thay đổi nhiều nhất.
- **Khi dùng:** "What do you think", "is this good", "critique this", "honest take", "is the vibe right", "does this feel like us", "should we ship this".
- **Khi bỏ qua:** Người dùng muốn rõ ràng một audit có cấu trúc (dùng `/ux-audit`). Backend hay hạ tầng.
- **Gọi:** `/ux-critique https://example.com`.
- **Đầu ra:** Ghi `.ux/last-critique.json` — 3 điểm thắng, 3 điểm trượt, 1 nước cờ chiến lược, kèm văn xuôi.
- **Nối vào:** `/ux-design` nếu quan điểm khuyến nghị redesign. `/ux-polish` nếu quan điểm khuyến nghị siết chặt.

#### `/ux-copy` — review + viết lại microcopy

- **Là gì:** Đánh giá mọi chuỗi nhìn thấy được đối chiếu rubric giọng nói và sinh ra một viết-lại trước/sau. Bắt: "form contains errors" (chung chung), "John Doe" (placeholder), copy AI vui mừng tưng bừng, CTA chung chung, empty state chết, lỗi vô dụng.
- **Khi dùng:** Cấu trúc đúng nhưng câu chữ yếu. "Review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "tighten the strings", "the buttons sound generic", "this empty state is dead".
- **Khi bỏ qua:** Vấn đề layout (dùng `/ux-audit` hoặc `/ux-polish`). Vấn đề copy do khả năng truy cập như alt text (dùng `/ux-a11y`). Backend hay hạ tầng.
- **Gọi:** `/ux-copy src/views/checkout.blade.php`.
- **Đầu ra:** Ghi `.ux/last-copy.json` — mảng `strings` gồm `{location, severity, before, after, notes}`, kèm rubric + các locale cần dịch.
- **Nối vào:** `/ux-fix` → áp dụng viết-lại. `/ux-a11y` → kiểm tra lại sau khi sửa copy.

### Fix & polish

#### `/ux-fix` — áp dụng phát hiện thành các commit nguyên tử

- **Là gì:** Đọc báo cáo mới nhất từ `.ux/` (audit, copy, a11y, motion, hoặc polish), xác thực cây làm việc, và áp dụng phát hiện thành các commit nguyên tử qua đúng sub-agent. Xác minh lại bằng cách chạy lại command gốc.
- **Khi dùng:** Sau khi chạy một command lớp audit và review phát hiện. "Fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it".
- **Khi bỏ qua:** Không có báo cáo trước trong `.ux/`. Cây làm việc bẩn và người dùng chưa đồng ý stash/commit. Sửa cần phán xét thiết kế, không phải áp dụng máy móc (dùng `/ux-design` cho redesign).
- **Gọi:** `/ux-fix` (tự phát hiện báo cáo nào để sửa) hoặc `/ux-fix --from=last-a11y.json`.
- **Đầu ra:** Các commit nguyên tử cho mỗi phát hiện. Chạy lại command gốc và cập nhật file `.ux/last-*.json`. In ra một tóm tắt.
- **Nối vào:** `/ux-next` → nhạc trưởng chọn nước cờ kế tiếp.

#### `/ux-polish` — pass mỹ thuật + diệt AI-slop

- **Là gì:** Nhịp khoảng cách, mài sắc phân cấp, phát hiện AI-slop, tính nhất quán token. Đối tác được dẫn dắt bởi LLM của `/ux-lint` — dùng phán xét của bạn cho các quyết định gu thẩm mỹ.
- **Khi dùng:** Cấu trúc đúng nhưng thực thi lỏng lẻo. "Polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste".
- **Khi bỏ qua:** Bề mặt thiếu chức năng cốt lõi (sửa cái đó trước). Cần redesign, không phải polish (dùng `/ux-design`). Vấn đề copy (dùng `/ux-copy`). Vấn đề motion (dùng `/ux-motion`). Vấn đề a11y (dùng `/ux-a11y`).
- **Gọi:** `/ux-polish src/components/Hero.tsx`.
- **Đầu ra:** Code cập nhật + `.ux/last-polish.json` mô tả các thay đổi.
- **Nối vào:** `/ux-lint` → xác minh polish đứng vững. `/ux-a11y` → kiểm tra lại khả năng truy cập.

### Discovery & tự sự

#### `/ux-frame` — khối framing 4 trường

- **Là gì:** Nắm bắt dành-cho-ai, outcome, giả thuyết, và tín hiệu thành công trong một khối framing có cấu trúc. Không có việc thiết kế nào diễn ra — chỉ là thu thập bốn trường biến một yêu cầu mơ hồ thành một brief làm việc. Nhẹ hơn `/ux-discover` (4 trường so với 10).
- **Khi dùng:** Bắt đầu bất kỳ dự án, sprint, hay engagement một-lần nào. Giữa dòng khi một cuộc trò chuyện đã trôi dạt. "Frame this", "what's the brief", "set up the project", "framing".
- **Khi bỏ qua:** Đã framed (kiểm tra `.ux/last-frame.json`). Build component một-lần không có ý nghĩa framing. Backend hay hạ tầng.
- **Gọi:** `/ux-frame "loyalty wallet for MENA Bashiti pilot"`.
- **Đầu ra:** Ghi `.ux/last-frame.json` — `{audience, outcome, hypothesis, success_signal}`.
- **Nối vào:** `/ux-discover` → mở rộng frame thành brief 10 trường. `/ux-design` → sinh dùng frame làm neo.

#### `/ux-research` — lên kế hoạch + tổng hợp nghiên cứu

- **Là gì:** Chế độ kế hoạch: viết script phỏng vấn, khảo sát, bộ sàng tuyển. Chế độ tổng hợp (`--synthesize`): tiêu hóa phỏng vấn, analytics, trang đối thủ, kết quả A/B, ticket hỗ trợ thành khuyến nghị. Điều phối `research-synthesizer`.
- **Khi dùng:** "Plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes".
- **Khi bỏ qua:** Câu trả lời đã biết với độ tin cậy cao. Quyết định có thể đảo ngược, rủi ro thấp. Backend hay hạ tầng.
- **Gọi:** `/ux-research --plan "loyalty wallet adoption in MENA"` hoặc `/ux-research --synthesize interviews/*.md`.
- **Đầu ra:** Ghi `.ux/last-research.json` — kế hoạch nghiên cứu hoặc các chủ đề được tổng hợp + bằng chứng + khuyến nghị.
- **Nối vào:** `/ux-frame` → tích hợp phát hiện vào frame. `/ux-design` → sinh từ phát hiện. `/ux-workshop` → chạy workshop dùng nghiên cứu làm đầu vào.

#### `/ux-workshop` — workshop design thinking 5 giai đoạn

- **Là gì:** Hỗ trợ một workshop discovery / design-thinking đầu cuối. Năm giai đoạn tuần tự (khám phá → bản đồ nhiệt → bản đồ bên liên quan → phác thảo giải pháp → kế hoạch chơi). Có giới hạn thời gian. Artifact cụ thể cho mỗi giai đoạn. Kết thúc bằng một quyết định, không phải "phát hiện thú vị".
- **Khi dùng:** Câu hỏi thật, người tham gia thật, ngân sách thời gian thật. "Run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "kick off the project".
- **Khi bỏ qua:** Brief đã rõ và có phạm vi. Brainstorm một mình (dùng `/ux-design` hoặc `/ux-frame`). Đội đang ở giữa thực thi, không phải discovery.
- **Gọi:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Đầu ra:** Ghi `.ux/last-workshop.json` — kế hoạch chơi + artifact theo giai đoạn.
- **Nối vào:** `/ux-design` → thực thi kế hoạch chơi. `/ux-research` → lấp các khoảng trống workshop làm nổi lên. `/ux-case-study` → xuất bản hành trình.

#### `/ux-case-study` — case study có thể xuất bản (định dạng Wfrah-editorial)

- **Là gì:** Sinh ra một case study dự án ở định dạng editorial đơn sắc tinh khôi — typography Wfrah, đường ngăn nét tóc, mã section đánh số (A)–(G), layout an toàn song ngữ. Một tài liệu, không phải brochure marketing. Đọc từ `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Khi dùng:** Sau khi launch. Sau một mốc rời rạc. "Write a case study", "case study this project", "do the wrap-up doc", "publish this work", "portfolio piece".
- **Khi bỏ qua:** Dự án thiếu dữ liệu để điền các section (A)–(G). Người dùng muốn landing marketing, không phải case study (dùng `/ux-design`).
- **Gọi:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Đầu ra:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Nối vào:** Command tận cùng — thường là kết thúc một dự án.

### Nhạc trưởng

#### `/ux-next` — nhạc trưởng workflow (chỉ đọc)

- **Là gì:** Đọc mọi `.ux/last-*.json` và gọi tên command kế tiếp có đòn bẩy cao nhất. Một nhạc trưởng, không phải thợ xây. Chỉ đọc.
- **Khi dùng:** Giữa các command. "What should I do next", "what's the next move", "decide for me", "where do we go from here".
- **Khi bỏ qua:** Không có báo cáo trước trong `.ux/`. Bạn có một command kế tiếp cụ thể trong đầu.
- **Gọi:** `/ux-next` (không tham số) hoặc `/ux-next --focus=a11y`.
- **Đầu ra:** Stdout — command kế tiếp được khuyến nghị + lý giải.
- **Nối vào:** Bất kỳ command nào nó chọn.

#### `/ux-expert` — móc nối tư vấn

- **Là gì:** Đưa ra thông tin liên hệ của tác giả plugin khi người dùng hỏi về một chuyên gia UX đời thực. Ngắn gọn, thẳng thắn, không marketing.
- **Khi dùng:** "Who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin".
- **Khi bỏ qua:** Người dùng đang hỏi về tính năng plugin, không phải tư vấn.
- **Gọi:** `/ux-expert`.
- **Đầu ra:** Thẻ liên hệ ngắn với LinkedIn / email / repo.

### Đồ thị nối chuỗi command

```
                  ┌──────────────────────┐
                  │  /ux-init            │
                  │  /ux-stats           │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-frame           │  khối framing 4 trường
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-discover        │  thu thập 10 trường (CỔNG CƯỠNG BỨC)
                  └────────────┬─────────┘
                               │ ghi .ux/last-discovery.json
                  ┌────────────▼─────────┐
                  │  /ux-recommend       │  5 tìm kiếm song song -> hệ thống merged
                  └────────────┬─────────┘
                               │ ghi .ux/last-recommendation.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-design     │ │ /ux-component   │ │ /ux-system  │
   │ /ux-dashboard  │ │ /ux-motion      │ │             │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ ghi .ux/last-<surface>.json
            ┌──────────────────┼──────────────────┐
            │                  │                  │
   ┌────────▼───────┐ ┌────────▼────────┐ ┌──────▼──────┐
   │ /ux-lint       │ │ /ux-audit       │ │ /ux-a11y    │
   │ /ux-critique   │ │ /ux-copy        │ │ /ux-motion  │
   └────────┬───────┘ └────────┬────────┘ └──────┬──────┘
            │                  │                  │
            └──────────────────┼──────────────────┘
                               │ ghi .ux/last-<lens>.json
                  ┌────────────▼─────────┐
                  │  /ux-fix             │  áp dụng phát hiện thành commit
                  │  /ux-polish          │
                  └────────────┬─────────┘
                               │
                  ┌────────────▼─────────┐
                  │  /ux-case-study      │  artifact có thể xuất bản
                  └──────────────────────┘

                  ┌──────────────────────┐
                  │  /ux-next            │  nhạc trưởng — chỉ đọc
                  │  /ux-expert          │  móc nối tư vấn
                  └──────────────────────┘
```

---

## 5 sub-agent

Sub-agent là các trình sinh chuyên vai trò được điều phối bởi command. Chúng không bao giờ chạy độc lập — chúng được gọi bởi `/ux-design`, `/ux-component`, `/ux-system`, `/ux-fix`, `/ux-research`, v.v. Mỗi agent có một ranh giới quyền sở hữu được định nghĩa: chúng KHÔNG quyết định brief; chúng thực thi đối chiếu brief.

### `frontend-engineer`

- **Sở hữu:** Code frontend chất lượng production (React, Next.js, Vue, Blade+Alpine, HTML thuần, Astro) với kỷ luật chống AI-slop.
- **Được điều phối bởi:** `/ux-design`, `/ux-component`, `/ux-dashboard`, `/ux-fix`.
- **Đầu vào:** Brief + hướng sáng tạo + token (từ `.ux/last-recommendation.json`).
- **Đầu ra:** Code chạy được, phân biệt được với output AI chung chung. Không gradient tím, không hero căn giữa, không ba card bằng nhau, không Inter ở kích thước display, không "John Doe", không emoji, không mặc định 300ms.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Sở hữu:** Chuyển động trong code frontend production — Framer Motion, GSAP, CSS animation. Thời lượng, easing, biên đạo, fallback reduced-motion, kỷ luật hiệu năng.
- **Được điều phối bởi:** `/ux-design`, `/ux-motion --fix`, `/ux-component`.
- **Đầu vào:** Brief chuyển động + token + 57 preset chuyển động từ `data/motion-presets.json`.
- **Đầu ra:** Chuyển động xứng đáng có chỗ đứng. Luôn được bọc trong fallback `prefers-reduced-motion`. Luôn được thử nghiệm đối chiếu Core Web Vitals.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Sở hữu:** Các chuỗi được ship — thông điệp lỗi, empty state, CTA, loading state, thông điệp thành công, toast, helper text, label form, text button.
- **Được điều phối bởi:** `/ux-copy --fix`, `/ux-design`, `/ux-frame`, `/ux-component`.
- **Đầu vào:** Hồ sơ giọng nói (được đặt tên hoặc dán vào) + các chuỗi của bề mặt.
- **Đầu ra:** Microcopy production được áp dụng nhất quán qua mọi trạng thái của một bề mặt để sản phẩm nghe như một sản phẩm, không phải mười. Cấm: "form contains errors", "John Doe", copy AI vui mừng tưng bừng, CTA chung chung, empty state chết.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Sở hữu:** Tiêu hóa đầu vào nghiên cứu (phỏng vấn, analytics, trang đối thủ, kết quả A/B, ticket hỗ trợ) thành khuyến nghị thiết kế hành động được.
- **Được điều phối bởi:** `/ux-research`, `/ux-workshop`, `/ux-frame`.
- **Đầu vào:** Nghiên cứu thô — transcript, export, URL đối thủ, cụm hỗ trợ.
- **Đầu ra:** Chủ đề, bằng chứng, khuyến nghị. Không bao giờ thiết kế câu trả lời — trao cho nhà thiết kế nền tảng để thiết kế từ đó.
- **Tool:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Sở hữu:** Hệ thống thiết kế đầy đủ — token (màu, typography, không gian, motion, radius, shadow), tài liệu nền tảng, hợp đồng component, cặp dark-mode, lớp theming.
- **Được điều phối bởi:** `/ux-system`, `/ux-component` khi không có hệ thống.
- **Đầu vào:** Brief thương hiệu + `.ux/last-recommendation.json` (phong cách + bảng màu + cặp typography + preset chuyển động).
- **Đầu ra:** Một hệ thống mạch lạc, có chính kiến, sẵn sàng production mà các agent phía sau có thể xây dựng đối chiếu mà không cần quyết định lại nền tảng. Token JSON, foundations MD, hợp đồng component, ánh xạ dark-mode.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### Giao thức điều phối sub-agent

Khi một command điều phối một sub-agent, nó truyền:

1. Brief / khuyến nghị (được load từ `.ux/`).
2. Lát manifest liên quan (ví dụ, `frontend-engineer` nhận phong cách + bảng màu + component đã chọn; `motion-engineer` nhận preset chuyển động đã chọn).
3. 145 rào chắn anti-pattern (luôn được kích hoạt).
4. Một tiêu chí thành công (artifact phải làm gì).

Sub-agent trả về:

1. Artifact (code, tài liệu, hệ thống).
2. Một khối lý giải (vì sao chọn thế này).
3. Một tự kiểm tra đối chiếu rào chắn (quy tắc nào đã xác minh).

Command gọi sau đó tự động chạy `/ux-lint` trước khi tuyên bố hoàn thành.

---

## 11 data manifest

Lớp dữ liệu là bộ não. Mọi command đọc từ nó; bộ máy merge xuyên qua nó; linter quét đối chiếu nó. Mọi file sống dưới `data/` và bọc entry của chúng trong `{_meta, entries}` cho versioning schema.

### `styles.json` — 84 phong cách thiết kế

| Trường | Mô tả |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, v.v. |
| `sample entry` | `swiss-international` — "Grid là luật. Typography làm việc nặng. Trang trí là thất bại." |

Được dùng bởi: `/ux-recommend`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json` — 176 bảng màu

| Trường | Mô tả |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (sáng/tối), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, v.v. |
| `sample entry` | `claude-warm-editorial` — sáng, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Được dùng bởi: `/ux-recommend`, `/ux-system`. Contrast đã xác minh ở AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json` — 70 cặp typography

| Trường | Mô tả |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weight + nguồn + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains` — Cormorant Garamond × Inter × JetBrains Mono |

Mọi family đều có license + URL nguồn. Được dùng bởi `/ux-recommend`, `/ux-system`.

### `components.json` — 148 component

| Trường | Mô tả |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid` — Mega Navigation, Product Grid — anatomy 6 phần, 4 state |

Đây là hào lũy lớn nhất của chúng tôi. Không có plugin UX Claude nào khác ship được manifest component có cấu trúc.

### `industries.json` — 184 quy tắc ngành nghề

| Trường | Mô tả |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, v.v. |
| `sample entry` | `fintech-neobank` — độ tin cậy cao, công bố quy định, UI chính cho số dư/giao dịch, mobile-first sử dụng hàng ngày |

Được dùng bởi `/ux-recommend` làm trục tìm kiếm song song đầu tiên.

### `chart-types.json` — 35 loại biểu đồ

| Trường | Mô tả |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical` — So sánh 4–15 danh mục rời rạc. Vị trí trên trục x ánh xạ danh mục; chiều cao ánh xạ giá trị. |

Được dùng bởi `/ux-dashboard`, `/ux-component` (instance chart).

### `tech-stacks.json` — 25 stack

| Trường | Mô tả |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router` — Next.js 15 (App Router), TS/JS, SSR, RSC, tương thích với Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Các stack khác gồm Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json` — 112 quy luật UX có tên

| Trường | Mô tả |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, v.v. |
| `sample entry` | `hicks-law` — Thời gian quyết định tăng theo log của số lượng lựa chọn được trình bày |

Được dùng bởi `/ux-audit` (chấm điểm 6 lăng kính) và `/ux-critique` (neo gu thẩm mỹ).

### `motion-presets.json` — 57 preset chuyển động

| Trường | Mô tả |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px` — 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Mọi preset đều có biến thể reduced-motion. Code sẵn sàng theo stack cho Framer Motion, GSAP, và CSS thuần.

### `anti-patterns.json` — 145 quy tắc regex

| Trường | Mô tả |
|---|---|
| `entries` | 145 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (type, pattern, flags, scope), `evidence_template`, `fix`, `references` |
| `categories` | A11y (23), Content (15), Layout (13), Typography (10), Color (9), Quality (9), Visual (9), Motion (8), Performance (4) |

Danh sách quy tắc đầy đủ ở [145 quy tắc chống AI-slop](#145-quy-tắc-chống-ai-slop--bộ-linter).

### `brands/*.json` — 160 spec thương hiệu

| Trường | Mô tả |
|---|---|
| `entries` | 160 (cộng với `_index.json` liệt kê tất cả) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Danh sách đầy đủ ở [160 spec DESIGN.md thương hiệu](#160-spec-designmd-thương-hiệu--theo-danh-mục).

---

## 145 quy tắc chống AI-slop — bộ linter

ux-skill ship một linter dựa trên regex xác định. **Không LLM.** **Không API.** **Không mạng.** Chạy trong CI trong ~200ms trên một app Next.js điển hình. Exit khác 0 ở Critical / High khi đặt `--fail-on high`.

Quy tắc được lấy từ `data/anti-patterns.json` (ưu tiên v2) với fallback `references/foundations/anti-patterns.md` (v1 bash). Hai binary được ship: `bin/ux-lint.py` (Python, nhanh, có thể mở rộng) và `bin/ux-lint.sh` (Bash + perl-PCRE, cho môi trường không có Python).

### Quy tắc theo danh mục

#### Typography (3 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| high | `inter-as-display` | Inter được dùng làm font display |
| medium | `hero-text-arbitrary-90px` | Kích thước font hero tùy tiện |
| low | `font-system-only` | Stack font hệ thống không có typeface được chọn |

#### Màu (6 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| high | `purple-to-blue-gradient` | Gradient AI mặc định tím-sang-xanh |
| high | `dark-text-on-dark-card` | Text tương phản thấp trên card |
| medium | `gradient-text-rainbow` | Gradient text nhiều stop |
| medium | `card-glow-purple-shadow` | Shadow phát sáng tím trên card |
| medium | `gradient-mesh-purple-pink` | Hero gradient mesh tím-hồng |
| low | `tailwind-color-named-vague` | Màu Tailwind có tên không có semantic token |

#### Layout (5 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| high | `three-equal-card-grid` | Ba card bằng nhau trên một hàng |
| medium | `centered-everything-hero` | Bố cục hero căn giữa mọi thứ |
| medium | `avatar-stack-overlapping` | Stack avatar chồng lấn chung chung |
| low | `pill-rounded-full-everywhere` | `rounded-full` áp dụng cho mọi thứ |
| low | `nav-equal-hamburger-desktop` | Menu hamburger trên desktop |

#### Nội dung (5 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| high | `lorem-ipsum-leak` | Lorem ipsum trong code ship |
| high | `emoji-in-ui` | Emoji được dùng như element UI |
| high | `icon-emoji-stamp` | Emoji được dùng như icon stamp |
| high | `testimonial-fake-five-stars` | Testimonial năm sao hard-code |
| medium | `fake-name-john-doe` | Tên placeholder chung chung |

#### Chuyển động (3 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| medium | `cta-arrow-rightward-bouncing` | Mũi tên nảy trên CTA |
| low | `timing-300ms-default` | Timing transition mặc định 300ms |
| low | `cubic-bezier-material-only` | Easing mặc định Material khắp nơi |

#### A11y (6 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| high | `inline-svg-no-aria` | SVG không có aria-label hoặc aria-hidden |
| high | `img-no-alt` | Ảnh thiếu thuộc tính alt |
| high | `link-onclick-no-href` | Anchor có onClick nhưng không có href |
| medium | `button-no-type` | Button thiếu thuộc tính type |
| medium | `heading-skip-h1-h3` | Bỏ qua cấp heading |
| medium | `infinite-scroll-no-pagination` | Infinite scroll không có fallback bàn phím |

#### Chất lượng (6 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| high | `console-log-leak` | `console.log` trong code component |
| medium | `inline-style-attribute` | Thuộc tính style inline |
| medium | `any-type-leak` | Kiểu TypeScript `any` |
| medium | `arbitrary-z-index-9999` | Giá trị z-index lười biếng |
| low | `shadcn-default-everywhere` | Khối token shadcn mặc định không sửa |
| low | `todo-fixme-comment` | TODO hoặc FIXME trong code ship |

#### Visual (1 quy tắc)

| Mức độ | ID quy tắc | Tên |
|---|---|---|
| low | `blur-bg-only-decoration` | Backdrop blur không có bề mặt glass |

### Cách dùng linter

**Quét một lần:**

```bash
uxskill lint .
# hoặc
python3 bin/ux-lint.py src/
# hoặc
bash bin/ux-lint.sh src/
```

**Cổng CI (GitHub Actions):**

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

**Đầu ra (mẫu):**

```
─── báo cáo /ux-lint ───
src/components/Hero.tsx:24  [high]   purple-to-blue-gradient
  evidence: bg-gradient-to-br from-purple-500 to-blue-500
  fix: thay bằng gradient primary của bảng màu được khuyến nghị hoặc bỏ gradient

src/components/Pricing.tsx:11  [high] three-equal-card-grid
  evidence: grid grid-cols-3 gap-6 (3 Card con bằng nhau)
  fix: feature một card; kẹp hai bên bằng hai card giảm nhấn mạnh

3 file được quét · 2 high · 0 medium · 0 low · exit 1
Khuyến nghị kế tiếp: /ux-polish --fix (do LLM dẫn dắt, xử lý cả phát hiện lintable lẫn thẩm mỹ)
```

---

## 160 spec DESIGN.md thương hiệu — theo danh mục

Thương hiệu thật. Ngôn ngữ thiết kế thật. Spec DESIGN.md thật — không phải palette chung chung. Bảo plugin "xây một landing theo phong cách Stripe" và nó đọc đúng từ vựng thương hiệu thực: rubric giọng nói, token màu, quy ước motion, nước cờ chữ ký, nước cờ kiêng kỵ.

Mỗi thương hiệu được ship như một JSON có cấu trúc (`data/brands/<slug>.json`) cộng với một tham chiếu văn xuôi (`references/brands/<slug>.md`).

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

### Vì sao điều này quan trọng

8 plugin UX Claude phổ biến khác sinh ra "modern minimal" hoặc "clean dashboard" — các biến thể của cùng một thẩm mỹ mặc định. ux-skill cho phép bạn yêu cầu **sự rõ ràng của Linear**, **sự nghiêm túc của Stripe**, **sự kiềm chế của Apple**, **khối nguyên thạch của Tesla**, **sự thân thiện của Notion**, **kỷ luật gradient của Cursor**, **mật độ nét tóc của Raycast**, **editorial ấm của Claude** — và bộ máy kéo đúng token, giọng nói, quy ước motion, và nước cờ chữ ký từ spec thương hiệu.

---

## Máy chủ MCP — nước cờ bất đối xứng

ux-skill ship một **máy chủ Model Context Protocol**. Chạy `ux-mcp` và bộ máy trở thành một process stdio chạy lâu dài mà bất kỳ host nào hỗ trợ MCP — Claude Desktop, Cursor, Windsurf, agent chung — có thể gọi vào. Mười bốn tool: `ux_recommend`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`. Cùng các handler Python mà slash command dùng; cùng các data manifest; cùng bộ recommender xác định.

**Vì sao đây là nước cờ bất đối xứng:** không một trong tám skill UX Claude hàng đầu (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) nào ship máy chủ MCP. Chúng bị khóa bên trong runtime plugin của Claude Code. ux-skill có thể truy cập từ bất kỳ host nào nói MCP, bao gồm cả các agent chưa bao giờ nghe đến plugin Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp là extra opt-in
ux-mcp                                  # máy chủ stdio JSON-RPC khởi động
```

Trỏ client của bạn đến binary `ux-mcp`. Tài liệu tool đầy đủ, ví dụ JSON, và cấu hình theo client cho Claude Desktop, Cursor, và Windsurf sống tại [docs/mcp.html](docs/mcp.html) và trong `commands/ux-mcp.md`.

---

## Trình cài đặt 17 IDE

`uxskill init` (hoặc `/ux-init` bên trong Claude Code) tự phát hiện IDE bạn đang dùng và ghi đúng artifact. Cùng bộ máy Python. Cùng khuyến nghị. Keo dán khác nhau theo từng IDE.

| IDE / công cụ | Tín hiệu phát hiện | Artifact được cài |
|---|---|---|
| Claude Code | `.claude/` hoặc `CLAUDE.md` | Manifest plugin tại `.claude-plugin/plugin.json` + toàn bộ 22 command + toàn bộ 5 sub-agent |
| Cursor | `.cursor/` hoặc `.cursorrules` | Header prompt `.cursorrules` trỏ về bộ máy |
| Windsurf | `.windsurf/` hoặc `.windsurfrules` | `.windsurfrules` với cùng header prompt |
| GitHub Copilot | `.github/copilot-instructions.md` hoặc `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | Patch `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` hoặc `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

Trong mỗi IDE, cùng các CLI command `uxskill recommend` / `uxskill lint` / `uxskill stats` hoạt động từ terminal. Bộ máy Python là nguồn sự thật; artifact IDE là các header prompt mỏng dẫn vào nó.

---

## Tình huống sử dụng — kịch bản cụ thể

Tám kịch bản thật. Chọn cái gần tình huống của bạn nhất và điều chỉnh lệnh gọi.

### 1. Xây dashboard fintech trong Cursor

Bạn đang ở trong Cursor làm dashboard cho neobank MENA. Bạn cài plugin và chạy discovery, khuyến nghị, rồi sinh dashboard.

```bash
pip install uxskill
uxskill init                                # phát hiện Cursor, ghi .cursorrules
uxskill discover                            # thu thập 10 trường
uxskill recommend \
  --project-type=dashboard \
  --industry=fintech-neobank \
  --tone=clinical --tone=precise \
  --must-have=dark-mode --must-have=a11y-AA --must-have=RTL \
  --forbidden=brutalism --forbidden=purple-gradients \
  --stack=nextjs-15-app-router \
  --region=mena
```

Sau đó trong Cursor, hỏi: *"Generate the dashboard surface using the recommendation in .ux/last-recommendation.json"*. Cursor đọc header `.cursorrules`, load khuyến nghị, điều phối sinh dashboard với ràng buộc rõ ràng.

### 2. Sinh landing theo phong cách Stripe trong Claude Code

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
> [trả về phong cách, bảng màu, cặp typography, preset chuyển động, component, thương hiệu hình mẫu đã chọn]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer sinh trang]

/ux-lint .
> [pass — spec thương hiệu Stripe được tôn trọng]
```

### 3. Audit code hiện có cho AI slop trong CI

Bạn ship một app Next.js hai tuần trước. Bạn muốn một sàn cứng chống lại dấu vân tay AI trên mỗi PR.

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

PR đưa vào gradient tím-sang-xanh, Inter ở 96px, testimonial "John Doe", hoặc emoji-as-icon đều fail CI. Không tốn LLM. ~200ms.

### 4. Polish một bề mặt hiện có "trông như AI tạo"

Bạn thừa kế một app React trông như mọi trang SaaS AI khác. Bạn muốn nó không trông như thế.

```
/ux-critique src/components/Hero.tsx
> [3 điểm thắng, 3 điểm trượt, 1 nước cờ chiến lược — quan điểm thẳng thắn]

/ux-lint src/
> [15 dấu vân tay AI mức high được gắn cờ]

/ux-polish src/components/Hero.tsx
> [pass mỹ thuật được LLM dẫn dắt + diệt AI-slop]

/ux-fix
> [áp dụng phát hiện thành commit nguyên tử, chạy lại linter]
```

Ba command, một bề mặt được polish, commit nguyên tử cho mỗi fix.

### 5. Thiết kế command palette theo phong cách Linear

```
/ux-component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [đọc data/brands/linear.app.json cho token + nước cờ chữ ký]
> [đọc data/components.json cho anatomy + state của command-palette]
> [điều phối frontend-engineer với spec Linear rõ ràng]
```

Component sinh ra dùng đúng token màu, stack typography, quy ước motion, mật độ hairline thực của Linear — không phải "dark UI chung chung".

### 6. Chạy workshop design thinking 90 phút với các bên liên quan

Bạn có một phòng 5 người trong 90 phút. Bạn muốn họ rời đi với một kế hoạch chơi, không phải một cảm hứng.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Plugin hỗ trợ năm giai đoạn (khám phá → bản đồ nhiệt → bản đồ bên liên quan → phác thảo giải pháp → kế hoạch chơi) đầu cuối, có giới hạn thời gian, với artifact cụ thể cho mỗi giai đoạn. Đầu ra là `.ux/last-workshop.json` — kế hoạch chơi, không chỉ "phát hiện thú vị".

### 7. Viết case study có thể xuất bản sau khi launch

Bạn ship ví loyalty. Bạn muốn một tác phẩm portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [đọc .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [sinh case study Wfrah-editorial với các section đánh số (A)-(G), đường ngăn nét tóc, layout an toàn song ngữ]
> [ghi case-studies/bashiti-loyalty.html]
```

Case study là một artifact hoàn thiện, có thể xuất bản — không phải bản nháp. Đơn sắc tinh khôi, typography editorial, sẵn sàng ship lên portfolio của bạn.

### 8. Chạy discovery trong ngữ cảnh không-AI (chỉ thu thập có cấu trúc)

Bạn đang phạm vi hóa một dự án. Bạn chưa cần khuyến nghị — bạn cần một brief có cấu trúc.

```bash
uxskill discover
# thu thập 10 trường, lưu vào .ux/last-discovery.json

cat .ux/last-discovery.json
# {
#   "project_type": "...",
#   "audience": "...",
#   ...
# }
```

Bạn có thể trao JSON cho đội của mình, dán vào tài liệu Notion, hoặc nạp vào một công cụ AI riêng. ux-skill cũng là một công cụ thu thập có cấu trúc, ngoài việc là một bộ máy.

### 9. MASTER.md bền vững — quyết định thiết kế của bạn, trong repo

Sau `/ux-recommend`, lưu trữ phong cách + bảng màu + typography + motion + component + thương hiệu hình mẫu + rào chắn đã chọn dưới dạng một file Markdown người-đọc-được mà đội bạn có thể review, diff, và version-control.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Ghi `.ux/design-system/MASTER.md` (YAML frontmatter + body) và `.ux/design-system/pages/<name>.md` cho mỗi bề mặt được sinh qua `persist save-page`. Idempotent — cùng đầu vào sinh đầu ra giống hệt byte, nên chạy lại trên trạng thái không đổi là no-op trong git.

---

## So sánh với các lựa chọn khác

Bảng tóm tắt ngắn. So sánh đầy đủ từng-bảng tại [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Chiều | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash command | **22** | 1 | 19 | 1 | 1 | nhiều | 1 | 1 | 1 |
| Component | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Preset chuyển động | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Spec thương hiệu | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Quy tắc anti-pattern | **145** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter xác định CI-safe | **có** | không | không | không | không | không | không | không | không |
| IDE hỗ trợ | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Cổng discovery | **10 trường** | ngầm | ngầm | ngầm | ngầm | ngầm | ngầm | ngầm | ngầm |
| Chuỗi state `.ux/` | **có** | không | không | không | không | không | không | không | không |
| Sao (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Đánh giá thẳng thắn

- **ui-ux-pro-max** lớn hơn về độ nhận biết, ship 18 IDE, có tìm kiếm kiểu BM25 trên CSV của họ. Nó không ship manifest component, manifest motion, thư viện thương hiệu, hay linter xác định.
- **open-design** có 19 skill + preview nhưng chỉ hỗ trợ Claude Code và không có lớp anti-slop.
- **hallmark** gần nhất về tinh thần (cũng anti-slop) nhưng là một skill đơn nhất — không bộ máy, không manifest, không command nối chuỗi.
- **material-3-skill** xuất sắc nếu bạn đặc biệt muốn Material Design 3. Chúng tôi không cạnh tranh trên MD3.

Để xem chi tiết đầy đủ theo từng chiều, xem [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Lộ trình

### v2.1 — Hoàn thiện linter (Q3 2026)

- **+17 quy tắc anti-pattern hoãn lại** để đạt tổng 52. Mục tiêu: state hover dark-on-dark, mã hóa state chỉ-bằng-màu, leo z-index dư thừa, breakpoint hardcode trong JS, opacity thay vì state disabled, v.v.
- **`uxskill lint --fix` cho các viết-lại an toàn** của các phát hiện có thể sửa máy móc (button-no-type, img-no-alt chuỗi-rỗng, xóa console-log-leak).
- **Extension VS Code** đưa phát hiện lint nổi lên inline (không cần chạy CI).

### v2.2 — Mở rộng manifest component (Q4 2026)

- **+50 component** để đạt tổng 198. Mới hoàn toàn: combobox với async filter, command-palette với heuristic recent-items, conditional-form-step, biến thể payment-element, date picker nhận biết RTL, phone input riêng MENA, lưới calendar với overlay hijri.
- **Phát code theo từng component** trong 6 stack (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS thuần).
- **Component playground** tại uxskill.laithjunaidy.com/playground — thử bộ máy khuyến nghị + xem preview component trực tiếp.

### v3 — Chợ + khóa chặt (2027)

- **Chợ spec thương hiệu** — xuất bản và khám phá spec thương hiệu cộng đồng. Trả-tiền-để-xuất-bản để tài trợ kiểm duyệt.
- **Quy tắc anti-pattern tùy chỉnh** — dự án có thể định nghĩa quy tắc regex riêng trong `data/anti-patterns.local.json` (đã ship trong v2; v3 thêm khám phá + chia sẻ).
- **`uxskill plan`** — lập kế hoạch trang nhiều-trang đầy đủ từ một brief, không chỉ một bề mặt.
- **Tương đương plugin Figma** — cùng bộ máy khuyến nghị, được đưa lên trong Figma.

---

## Đóng góp

Issue và PR được hoan nghênh. Ba khu vực đòn bẩy cao:

### Thêm một quy tắc anti-pattern

1. Sửa `data/anti-patterns.json` — thêm một entry với `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Thêm một test trong `tests/linter/` — một file kích hoạt quy tắc, một file không.
3. Chạy `uxskill lint tests/linter/should-trigger/<rule>.tsx` — xác nhận nó bắn. Chạy trên `tests/linter/should-not-trigger/<rule>.tsx` — xác nhận nó không bắn.
4. Mở một PR.

### Thêm một spec thương hiệu

1. Tạo `data/brands/<slug>.json` với `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Thêm văn xuôi tương ứng tại `references/brands/<slug>.md`.
3. Đăng ký trong `data/brands/_index.json`.
4. Mở một PR. Spec phải được hỗ trợ bởi tham chiếu nguồn chính (sản phẩm thực của thương hiệu, hệ thống thiết kế công khai, hoặc DESIGN.md nếu họ có công bố).

### Thêm một preset chuyển động

1. Sửa `data/motion-presets.json` — thêm một entry với `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Preset phải có một biến thể reduced-motion. Không ngoại lệ.
3. Mở một PR.

### Quy trình

- Đọc [CONTRIBUTING.md](CONTRIBUTING.md) cho quy trình đầy đủ.
- Đọc [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Quy tắc và spec thương hiệu mới được review về: nền tảng nguồn chính, không over-fit vào một dự án duy nhất, không emoji trong bất kỳ dữ liệu nào, hành vi an toàn RTL khi áp dụng được.

---

## Giấy phép, tác giả, lời cảm ơn

### Giấy phép

MIT. Hãy dùng, fork, xây dựng dựa trên. Nếu nó cứu bạn khỏi việc ship AI slop, hãy gắn sao cho repo — đó là cách rẻ nhất để hỗ trợ.

### Tác giả

**Laith Aljunaidy** — nhà sáng lập đơn nhất của [Dot](https://thedotwallet.com), nền tảng loyalty MENA-first. Xây ux-skill để frontend AI-tạo không trông giống nhau hết.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Trang chủ: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Lời cảm ơn

- Đội ngũ Anthropic vì Claude Code và kiến trúc skill / plugin đã giúp việc này phân phối được.
- Nielsen Norman Group, Laws of UX (lawsofux.com), và cộng đồng nghiên cứu UX có công trình thông báo cho `data/ux-guidelines.json`.
- Mọi thương hiệu được liệt kê trong `data/brands/` — hệ thống thiết kế công khai của họ là nguồn sự thật cho các spec thương hiệu.
- Những người đóng góp v1 ban đầu: một skill Claude một-phát từng là hạt giống cho bộ máy Python v2.
- 8 plugin UX Claude phổ biến mà chúng tôi so sánh — họ nâng cao mức chuẩn; đây là câu trả lời của chúng tôi.

---

**ux-skill** · **v3.0.0-stable** · Được xây để Claude Code, Cursor, Windsurf, và mọi công cụ lập trình AI khác xuất ra frontend không đọc lên như AI tạo.

> Gắn sao repo tại [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Cài qua `pip install uxskill` hoặc `npx uxskill init` · Xem so sánh tại [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
