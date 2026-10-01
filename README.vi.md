[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · **Tiếng Việt** · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: bộ máy trí tuệ thiết kế cho Claude Code, Cursor và mọi công cụ lập trình AI khác

**Một bộ máy trí tuệ thiết kế giúp UI do AI tạo ra có bản sắc thay vì rập khuôn.** Gắn nó vào bất kỳ công cụ nào trong 17 công cụ lập trình AI và sản phẩm của bạn thôi trông như do AI làm. Miễn phí, MIT, ngoại tuyến, không LLM.

```bash
pip install uxskill
```

**[Gắn sao cho ux-skill trên GitHub](https://github.com/Laith0003/ux-skill)** nếu nó hữu ích: đó là cách đơn giản nhất để giúp dự án. Mới đến? Bắt đầu với [tour 60 giây](#cài-đặt-nhanh) hoặc xem trực tiếp tại [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![Trước: hero ảnh stock rập khuôn, gradient tím nhạt, không có bản sắc thương hiệu. Sau: ảnh công trường thật dưới lớp phủ tối, tiêu đề kiểu biên tập với điểm nhấn màu hổ phách, và form yêu cầu báo giá đặt ngay trong hero. Cùng một prompt, kết quả khác khi ux-skill cung cấp các ràng buộc.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*Trước: SEO slop rập khuôn với ảnh stock. Sau: hero ảnh công trường thật dưới lớp phủ tối, tiêu đề kiểu biên tập với điểm nhấn màu hổ phách, form báo giá ngay trong hero. Cùng công cụ lập trình AI, cùng prompt, kết quả khác khi ux-skill cung cấp các ràng buộc.*

> **v4.0, FOUNDATIONS: một lệnh dựng nên hệ thống thiết kế hoàn chỉnh, được kiểm tra theo WCAG, tích hợp sẵn tiếng Ả Rập và chiều viết phải sang trái.** Plugin UX mạnh nhất cho lập trình bằng AI. Một lõi suy luận Python với bộ tổng hợp 7 trục xác định, 12 manifest JSON truy vấn được (84 phong cách, 176 bảng màu, 70 cặp chữ, 148 component, 184 ngành, 35 loại biểu đồ, 57 preset chuyển động, 112 định luật UX, 171 quy tắc anti-pattern, 25 tech stack, 160 đặc tả thương hiệu), 18 slash command, 5 sub-agent, 25 tool MCP và một linter chống AI-slop xác định. Đa IDE: cài vào Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer và Roo Cline.

> **Tên thương hiệu là `ux-skill`.** Tên gói trên PyPI / npm vẫn là `uxskill`. Repo GitHub nằm tại [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**Tác giả:** [Laith Aljunaidy](https://laithjunaidy.com), nhà thiết kế và CTO tại Amman · **Trang:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **So sánh với mọi plugin UX cho Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#trình-cài-đặt-17-ide)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### Mới trong 4.0: các nền tảng

Một màu thương hiệu vào, một hệ thống thiết kế ra, với độ tương phản đã được kiểm tra trước khi đến tay bạn.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 trở lên. Với máy chủ MCP, `pip install --upgrade 'uxskill[mcp]'`. Với pipx, `pipx install uxskill` (cài đè lên bản 3.x đã có, `pipx upgrade uxskill`). Với npm, `npx uxskill@latest`. Đang dùng 3.x? [Hướng dẫn chuyển đổi](docs/migrating-to-4.md) ánh xạ mọi token 3.x sang vai trò của nó trong 4.0.

**Đang xây sản phẩm hay landing page?** Bạn nhận được `tokens.css` để liên kết từ trang, `fonts.css` với font dự phòng khớp số đo cho các kiểu chữ đã chọn, `fonts-self-host.css` tải kiểu chữ từ chính tệp của bạn, `tokens.json` cho công cụ, hình ảnh trang trí thương hiệu trong `art/`, và `system-report.md`, nói bằng lời đơn giản những gì đã được dựng, vì sao, và nên bắt đầu từ bố cục trang nào. Tạo kiểu bằng các vai trò (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`), và bật tắt chế độ tối, tương phản cao, khoảng cách gọn, phải sang trái hay giảm chuyển động bằng một thuộc tính trên `<html>`. Tải kiểu chữ bằng liên kết Google Fonts mà báo cáo đưa ra, hoặc bằng `fonts-self-host.css` cùng thư mục `fonts/`, và liên kết `fonts.css` với cách nào cũng được, trước `tokens.css`; đừng sửa tệp nào trong hai tệp đó. Với `--brief`, diện mạo đi theo ngành và giọng điệu khi brief nêu chúng, còn các trường có cấu trúc (độ tuổi, ngôn ngữ, chế độ mặc định, bối cảnh đọc) quyết định cỡ chữ, vùng chạm, hệ chữ và chế độ nào mở ra trước; discovery không hỏi ngành, nên `/ux-system create` sẽ hỏi. Trong Claude Code, `/ux-system create` kiểm tra phiên bản đã cài, chạy build và giải thích báo cáo.

**Đang thiết kế một hệ thống thiết kế?** Chín nền tảng (màu, chữ, khoảng cách, bố cục, bo góc, viền, độ nổi, chuyển động, hình ảnh), mỗi nền tảng thay đổi liên tục theo bảy trục, với primitive và vai trò ngữ nghĩa, theo định dạng W3C design tokens (DTCG 2025.10) kèm giá trị của mọi chế độ. Cùng đầu vào, cùng từng byte. Qua MCP, `ux_system_build` trả về báo cáo, kết quả kiểm tra và kích thước từng tệp, và ghi đúng các tệp như lệnh khi được truyền `out`.

- **Cổng WCAG.** Mọi cặp màu cho chữ, điều khiển và focus đều được đo ở chế độ sáng và tối, ở tương phản chuẩn và cao: WCAG 1.4.3 (chữ 4.5:1) và 1.4.11 (phi văn bản 3:1) ở tương phản chuẩn, WCAG 1.4.6 (chữ 7:1) ở tương phản cao, cộng thêm ngưỡng sàn 4.5:1 ở tương phản cao cho phần lớn thành phần phi văn bản do chúng tôi tự đặt, vì WCAG không quy định mức nâng cao cho phi văn bản. Hệ thống không đạt sẽ không được ghi ra; thông báo cho biết cần sửa gì.
- **An toàn mặc định.** Không bao giờ ghi đè một tệp đã khác đi. `--force` chỉ thay tệp khi bạn yêu cầu.
- **Tiếng Ả Rập.** Dưới `dir="rtl"` chữ chuyển sang phông Ả Rập với cỡ chữ và chiều cao dòng riêng; khoảng cách dùng thuộc tính logic và chuyển động được lật gương. `--latin-only` bỏ phần này.

**Một hệ thống bạn đã có.** `/ux-system enhance --from` đọc nó theo đúng tên gọi của nó (token DTCG, thuộc tính tùy biến CSS, theme Tailwind, tệp quy tắc markdown hoặc bản xuất biến Figma), kiểm tra qua cùng cổng đó và đo xem code của bạn thực sự dùng nó ra sao; không có gì bị viết lại. `/ux-system extend --from` thêm nền tảng, vai trò hay hợp đồng mà không đổi token nào đang có, trong một tệp mở rộng đặt cạnh, và `uxskill system export` ghi nó ra thành tokens.css, theme Tailwind 4 hoặc biến Figma. Bản 4.2 bổ sung lớp tin cậy (lint mỗi lần ghi, một bước rà soát hoàn thiện) và đợt ra mắt. Xem [changelog](CHANGELOG.md).

**Component và section.** 23 hợp đồng component nêu rõ mỗi phần của một điều khiển gắn với token nào ở từng trạng thái và mỗi trạng thái chuyển động ra sao: đổi trạng thái thì chuyển tiếp theo `motion.state`, nhấn thì co giãn theo `motion.press.scale` (và đứng yên khi giảm chuyển động), còn tab, menu và segmented control trượt một chỉ báo duy nhất. 14 hợp đồng section (hero, bảng giá, FAQ, footer và các phần còn lại) nêu nhiệm vụ của từng section, các component mà slot của nó nhận, bằng chứng nó cần và cách nó xếp chồng trên điện thoại. Các trang dựng từ chúng dùng ảnh chụp; mảnh giao diện chỉ là hình ảnh bổ sung, không bao giờ thay thế.

**Một linter đọc cả trang.** 171 quy tắc, nhiều quy tắc có thêm bước kiểm tra trên CSS và markup đã phân tích, đọc chính hệ thống của trang: chuyển động được canh thời gian theo đường cong của nó, chiều cao dòng của tiêu đề display được giữ ở ngưỡng sàn của bộ máy, và một điều khiển bị ẩn phải rời khỏi thứ tự tab. `uxskill lint --render` mở từng trang trong Chromium headless ở bề rộng desktop và điện thoại rồi thao tác thật: vòng focus không hiện hoặc bị cắt, hover và nhấn phản hồi chậm, focus bị mất sau Escape, và cú nhấn vẫn chuyển động khi đã giảm chuyển động.

**Ít lệnh hơn.** 25 slash command còn 18. `/ux-discover` nhận `--frame` và `--recommend`, `/ux-design` nhận `--component`, `--dashboard` và `--from-image`, `/ux-polish` lặp lint, fix, re-lint cho đến khi điểm đạt 90 hoặc qua ba vòng, và `/ux-init` nhận `--stats`. Bảy tên cũ vẫn chạy như alias và sẽ bị bỏ ở 4.1; xem [các alias](#alias-bị-bỏ-ở-41).

**Playbook theo bề mặt.** Quy tắc cho landing, dashboard và component nằm trong `references/surfaces/`, mỗi loại một playbook. `/ux-design` nạp đúng một playbook, chọn theo chế độ của nó, nên build dashboard không bao giờ đọc quy tắc hero.

Test: **9764 đạt**. Ngoại tuyến. Xác định. Không bao giờ gọi LLM.

### Mới trong v3.1: đúng thương hiệu, responsive, sống động

- **Độ trung thành thương hiệu được cưỡng chế, không phải trông chờ.** Màu chủ đạo được đọc từ điểm ảnh của LOGO (không phải từ CSS được tô nhiều nhất); font mặc định bị loại để theo kiểu chữ của logo. Thương hiệu trích xuất đi theo `recommend` -> `synthesize`, và một **ngưỡng sàn cứng** trong `evaluate` đánh TRƯỢT mọi đầu ra làm mất màu hoặc logo thương hiệu hay không có hình ảnh thật. Tương thích hai chiều với quy ước mở `brand.md` (render + nhập).
- **Mobile-first, có cổng kiểm tra.** Các nền tảng tay nghề mới (`responsive.md`, `component-behaviors.md`) cùng một cổng nhận biết xuống dòng, đánh trượt khi có cuộn ngang, nhãn nav, wordmark hay nút bị xuống dòng, hoặc header sticky quá cao.
- **Lớp wow.** Bộ máy tạo ra 2-3 khoảnh khắc đặc trưng phối hợp trên mỗi trang; học thuyết "wow chỉ có thể đến từ người dùng" bị đảo ngược.
- **Linter sắc hơn** (152 quy tắc): phát hiện hình ảnh bắt buộc và phần tử chỉ có icon, quy tắc token placeholder và `100vw`; picsum có seed được giữ, loại ngẫu nhiên bị gỡ.

Ghi chú đầy đủ trong [CHANGELOG.md](CHANGELOG.md).

### Có gì mới trong v3

- **Brand specs trở thành dữ liệu huấn luyện, không phải template.** 160 brand specs không còn là catalog mà recommender chọn từ, chúng là vốn từ mà synthesizer chưng cất. Output mới ở mỗi lần gọi.
- **Synthesizer 7 trục** (warmth, contrast, density, geometry, formality, motion, type_personality). Brief được ánh xạ tất định sang giá trị trục; giá trị trục được biên dịch thành palette + typography + spacing + radius + motion token tươi.
- **Ba chế độ tự động phân phối**: `strict_brand` (100% một thương hiệu), `brand_anchor` (70% một thương hiệu + 30% thích ứng theo trục từ thương hiệu anh em), `pure_synthesis` (không thương hiệu nào được nêu, chưng cất từ 8 ví dụ khớp trục).
- **Sổ cái quyết định xếp hạng lại recommender.** `.ux/decisions.jsonl` xếp hạng lại ứng viên theo chiến thắng quá khứ trong cùng bucket `(industry, ui_type)`. An toàn cold-start. Chỉ đếm các quyết định có `lint_score >= 80` + `user_accepted = true`.
- **Ma trận tương tác trục**: giải quyết xung đột rõ ràng giữa các trục cạnh tranh (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius). Không còn quy tắc tùy biến im lặng.
- **Vòng lặp tự động `/ux-evolve`** (ở 4.0, là vòng lặp mặc định của `/ux-polish`): lint → polish → re-lint cho đến khi điểm ≥ 90, chững lại, hoặc 3 vòng ở 4.0 (5 ở v3). Quality gate ở 65.
- **3 công cụ MCP mới** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`.
- **Bảng điều khiển stats cục bộ**: `uxskill stats --html` ghi `.ux/stats.html` cho biết cài đặt **của bạn** đã học được gì. Không telemetry, không tổng hợp toàn cục.
- **223 test đậu.** Offline. Tất định. Không bao giờ gọi LLM.

Chi tiết đầy đủ trong [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### Lịch sử sao

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill là gì

ux-skill là một **bộ máy trí tuệ thiết kế** dành cho các công cụ lập trình AI. Nó chạy như một gói Python (`pip install uxskill`), như một plugin của Claude Code, và như một trình cài đặt đa-IDE cho 17 môi trường. Bộ máy nhận vào một brief dự án (ngành nghề, đối tượng, tone, yêu-cầu-bắt-buộc, điều-cấm-kỵ, stack, khu vực) và trả về một hệ thống thiết kế được khuyến nghị đầy đủ: phong cách, bảng màu, cặp typography, preset chuyển động, component, các thương hiệu hình mẫu để nghiên cứu và những rào chắn anti-pattern phải tuân thủ. Khuyến nghị mang tính xác định, cùng một đầu vào luôn tạo ra cùng một đầu ra.

Plugin nằm giữa bạn và công cụ lập trình AI. Khi bạn yêu cầu Claude Code, Cursor hay bất kỳ trợ lý AI nào "xây một landing page fintech", trợ lý thường ứng tác, và kết quả lộ ra là do AI tạo ra trong vòng năm giây (gradient từ tím sang xanh, ba thẻ bằng nhau, Inter ở kích thước display, "John Doe" trong testimonial, transition mặc định 300ms, hero căn giữa, mũi tên CTA nảy lên xuống). ux-skill thay thế việc ứng tác bằng **những ràng buộc có cấu trúc**: bạn chạy `/ux-discover` để nắm bắt brief và chọn hệ thống, `/ux-design` để sinh mã, và `/ux-lint` để xác minh code vượt qua 171 quy tắc chống AI-slop xác định trước khi commit.

README này là tài liệu tham chiếu chính thức. Mọi command, mọi sub-agent, mọi data manifest, mọi đường cài đặt, mọi spec thương hiệu, mọi danh mục anti-pattern, tất cả đều được tài liệu hóa ở đây. Nếu bạn đang tìm một plugin thiết kế cho Claude Code hoặc so sánh các công cụ thiết kế AI cho Cursor, Windsurf hay Codex, hãy đọc tài liệu này từ đầu đến cuối song song với [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Mục lục

1. [Bộ não, v3.0 là gì](#bộ-não-v30-là-gì)
2. [Cài đặt nhanh](#cài-đặt-nhanh)
3. [Những con số, so sánh trực tiếp với 8 skill UX hàng đầu cho Claude](#những-con-số-so-sánh-trực-tiếp-với-8-skill-ux-hàng-đầu-cho-claude)
4. [Kiến trúc, các mảnh ghép khớp với nhau thế nào](#kiến-trúc-các-mảnh-ghép-khớp-với-nhau-thế-nào)
5. [18 slash command, tham chiếu chi tiết](#18-slash-command-tham-chiếu-chi-tiết)
6. [5 sub-agent](#5-sub-agent)
7. [11 data manifest](#11-data-manifest)
8. [171 quy tắc chống AI-slop, bộ linter](#171-quy-tắc-chống-ai-slop-bộ-linter)
9. [160 spec DESIGN.md thương hiệu, theo danh mục](#160-spec-designmd-thương-hiệu-theo-danh-mục)
10. [Máy chủ MCP, nước cờ bất đối xứng](#máy-chủ-mcp-nước-cờ-bất-đối-xứng)
11. [Trình cài đặt 17 IDE](#trình-cài-đặt-17-ide)
12. [Tình huống sử dụng, kịch bản cụ thể](#tình-huống-sử-dụng-kịch-bản-cụ-thể)
13. [So sánh với các lựa chọn khác](#so-sánh-với-các-lựa-chọn-khác)
14. [Lộ trình](#lộ-trình)
15. [Đóng góp](#đóng-góp)
16. [Giấy phép, tác giả, lời cảm ơn](#giấy-phép-tác-giả-lời-cảm-ơn)

---

## Bộ não: v3.0 là gì

v3.1.0 là sự dịch chuyển kiến trúc lớn nhất trong lịch sử ux-skill. Recommender không còn chọn template từ catalog, engine **tổng hợp** một ngôn ngữ thiết kế tươi cho mỗi brief. Cùng một brief luôn cho ra cùng một output (hoàn toàn tất định), nhưng mỗi brief khác nhau nhận được hệ thống mới của riêng nó. Brand specs không còn là template; chúng là dữ liệu huấn luyện mà engine học vốn từ. Hệ thống có mắt nhìn vào lịch sử của chính nó, đóng vòng phản hồi cục bộ, và không bao giờ gọi LLM.

Compiler là **synthesizer tất định 7 trục**, warmth, contrast, density, geometry, formality, motion, type_personality. Mỗi brief ánh xạ sang giá trị trục; giá trị trục biên dịch thành palette + typography + spacing + radius + motion token tươi. Thang typography mô-đun chọn tỷ lệ từ contrast (1.200 quiet / 1.250 balanced / 1.333 loud). Layout primitive đáp ứng theo cấu trúc (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). Layout hỏng không thể phát ra vì chúng không thể biểu diễn.

Có ba chế độ tự động phân phối: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% token Stripe, đường nhanh nhất); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% thích ứng theo trục từ 4 thương hiệu anh em); và `pure_synthesis` (không thương hiệu nào được nêu → không gian vô hạn, chưng cất 8 ví dụ khớp trục thành ngôn ngữ thiết kế mới). Các trục cạnh tranh được giải quyết bằng **ma trận tương tác trục** đã tài liệu hóa, dense + corporate biên dịch thành 4px (density thắng, trường phái Bloomberg), airy + corporate thành 12px (formality thắng, sang trọng), soft + playful thành 18px radius, sharp + corporate thành 2px. Không quy tắc tùy biến im lặng trong triển khai.

**Sổ cái quyết định** (`.ux/decisions.jsonl`, schema `_v: 1` khóa) đóng vòng phản hồi. Recommender giờ xếp hạng lại ứng viên theo chiến thắng quá khứ trong cùng bucket `(industry, ui_type)`. An toàn khi khởi động nguội: bỏ qua bước xếp hạng lại khi có dưới 3 quyết định trước đó. Chỉ đếm các quyết định có `lint_score >= 80` VÀ `user_accepted = true`. Thêm vào đó `/ux-polish` chạy lint → polish → re-lint cho đến khi điểm ≥ 90, chững lại, hoặc 3 vòng, với quality gate ở 65 mà dưới đó output bị từ chối nếu không có `--force`. Kết quả: mỗi cài đặt thông minh hơn trên corpus của chính mình, mỗi lần chạy tái lập được giữa các máy, và engine vẫn hoàn toàn offline.

---

## Cài đặt nhanh

Ba đường cài đặt. Chọn đường phù hợp với môi trường của bạn.

### Đường 1: chợ Claude Code (chính thống)

Nếu bạn làm việc trong Claude Code, cài qua chợ plugin:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

Điều đó kết nối toàn bộ 18 slash command (cộng 7 tên cũ được giữ làm alias đến 4.1) và 5 sub-agent vào phiên Claude Code của bạn. Sau khi cài, chạy `/ux-init` để thiết lập thư mục state `.ux/` cho dự án và xác minh rằng bộ máy Python có thể truy cập được.

### Đường 2: pip (đa năng)

Nếu bạn làm việc ngoài Claude Code (Cursor, Windsurf, CLI, CI), cài gói Python:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

Gói cung cấp cả `ux` và `uxskill` làm entry point CLI, chúng là cùng một binary.

### Đường 3: npx (không cần Python)

Nếu bạn không muốn quản lý Python trực tiếp, wrapper npx tự bootstrap mọi thứ qua `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### Xác minh cài đặt

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

Mười hai số đếm cộng lại thành 1.262 mục. Nếu bất kỳ số đếm nào trả về 0, file JSON đang thiếu: mở một issue tại [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## Những con số: so sánh trực tiếp với 8 skill UX hàng đầu cho Claude

Số sao được xác minh lần cuối qua `gh api` vào **2026-05-28**. ux-skill (Laith0003/ux-skill) là người mới nhất gia nhập, chúng tôi nhỏ về độ nhận biết, sâu về kiến trúc. Bảng so sánh dưới đây thành thật: chỗ chúng tôi thua, chỗ chúng tôi thắng.

| Plugin | Sao | Kiến trúc | Slash command | Linter (CI-safe) | Spec thương hiệu | Component | Preset chuyển động | IDE hỗ trợ |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83.958** | Python BM25 + CSV, một skill duy nhất | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54.406** | Node.js + 19 skill + preview | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25.202** | Bash + gu thẩm mỹ dựa trên nghiên cứu | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15.455** | Một SKILL.md 62 KB + script | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5.762** | Thư viện skill nối với MCP | nhiều | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2.391** | Skill thẩm mỹ đơn nhất | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2.164** | Skill thiết kế anti-slop | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | Component MD3 + audit | 1 | - | (chỉ MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Bộ máy Python + 12 manifest + 18 command + 5 sub-agent + linter CI** | **18** | **171 quy tắc xác định** | **160** | **148** | **57** | **17** |

### Chỗ chúng tôi thua

- **Độ nhận biết.** Họ có hàng trăm nghìn sao. Chúng tôi có 14. Hãy gắn sao cho repo, đó là cách rẻ nhất để giúp.
- **Nhận diện thương hiệu.** ui-ux-pro-max và open-design có một lợi thế đi trước được đo bằng tháng, không phải ngày.
- **Bóng bẩy marketing.** Họ có screenshot, video demo, và một landing page dễ khám phá. Chúng tôi có một README đầy đủ và một landing mỏng.

### Chỗ chúng tôi thắng

- **Thư viện component:** 148 component được tài liệu hóa với anatomy, state, token sử dụng, và spec chuyển động. Không có cái nào trong 8 plugin kia ship được manifest component.
- **Preset chuyển động:** 57 entry sẵn sàng theo stack (Framer Motion, GSAP, CSS) với fallback reduced-motion. Không có ai trong số còn lại ship manifest chuyển động.
- **Linter anti-pattern:** 171 quy tắc xác định, chạy trong CI, exit khác 0 ở mức Critical/High. Không có ai trong số còn lại ship một linter xác định.
- **Spec thương hiệu:** 160 spec DESIGN.md thật (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude, và 96 thương hiệu khác). Không có ai trong số còn lại ship một thư viện thương hiệu.
- **17 IDE được hỗ trợ:** cùng một bộ máy, keo dán khác nhau cho mỗi IDE.
- **18 slash command:** discovery, generation (trang, component, dashboard, từ một hình ảnh), audit, lint, vòng lặp polish, vòng lặp fix, case study, workshop, copy, motion, a11y, conductor, tích hợp đầy đủ.

Bảng so sánh đầy đủ cạnh nhau tại [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Kiến trúc: các mảnh ghép khớp với nhau thế nào

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

### Bộ máy thực sự hoạt động thế nào

1. **Đầu vào.** Bạn cung cấp một brief, hoặc tương tác qua `/ux-discover` (10 trường), hoặc không tương tác qua các flag của `ux recommend`.
2. **5 tìm kiếm song song.** Bộ máy chạy đồng thời năm truy vấn trên các manifest:
   - **Ngành → recommended_styles** (industries.json)
   - **Phong cách → tương thích bảng màu + chữ + chuyển động** (styles.json)
   - **Giọng điệu × bắt buộc → bộ lọc bảng màu** (palettes.json)
   - **Stack → tương thích component + preset chuyển động** (tech-stacks.json, motion-presets.json)
   - **Cấm + khu vực → rào chắn + danh sách rút gọn thương hiệu hình mẫu** (anti-patterns.json, brands/)
3. **Hợp nhất.** Một bộ hợp nhất xác định xếp hạng ứng viên, giải quyết xung đột (ví dụ chế độ tối bắt buộc quyết định chế độ bảng màu) và xuất ra một hệ thống khuyến nghị duy nhất.
4. **Đầu ra.** Một tài liệu JSON gồm phong cách đã chọn, bảng màu, cặp chữ, 5 preset chuyển động hàng đầu, 12 component hàng đầu, 5 thương hiệu hình mẫu hàng đầu, và toàn bộ 171 rào chắn anti-pattern đang bật. Kèm một khối lý giải cho từng lựa chọn.
5. **Sinh mã.** Các lệnh phía sau (`/ux-design` ở các chế độ trang, component, dashboard và hình ảnh, cùng `/ux-system`) dùng khuyến nghị để sinh code thật qua các sub-agent.
6. **Xác minh.** `/ux-lint` quét lại code đã sinh theo 171 quy tắc. Exit khác 0 ở Critical/High trong CI.

**Bổ sung của v3.** Recommender giờ xếp hạng lại ứng viên từ `engine/decisions/` dựa trên `.ux/decisions.jsonl` (chỉ đếm quyết định có `lint_score >= 80` VÀ `user_accepted = true`; an toàn khi khởi động nguội dưới 3 quyết định trước đó). Luồng sinh mã có thể chuyển sang `engine/synthesizer/`, một trình biên dịch 7 trục xác định tạo token bảng màu + chữ + khoảng cách + bo góc + chuyển động mới cho từng brief thay vì chọn template từ danh mục. Chi tiết tại [Bộ não, v3.0 là gì](#bộ-não-v30-là-gì).

**Python suy nghĩ. HTML hiển thị. Markdown nối chuỗi.**

---

## 18 slash command: tham chiếu chi tiết

Mỗi lệnh được ship dưới dạng một tệp `.md` trong `commands/` với `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` và `output state file`. Mô tả dưới đây đã được rút gọn; mã nguồn đầy đủ mới là đặc tả chuẩn.

Các lệnh được chia thành bảy nhóm: **khởi tạo & kiểm kê**, **discovery & khuyến nghị**, **sinh mã**, **kiểm tra & xác minh**, **sửa & đánh bóng**, **discovery & tường thuật**, và **điều phối**. Bảy tên từ 3.x vẫn chạy như [alias](#alias-bị-bỏ-ở-41) cho đến 4.1.

### Khởi động & kiểm kê

#### `/ux-init`: khởi động dự án

- **Là gì:** Phát hiện IDE bạn đang dùng (`.claude/`, `.cursor/`, `.windsurf/`, v.v.), cài đúng artifact, xác minh bộ máy Python có thể truy cập được, in ra ảnh chụp số liệu. `--stats` chỉ in ảnh chụp: phiên bản + số mục trong các manifest dữ liệu.
- **Khi dùng:** Lần đầu cài trong một dự án mới. Sau khi clone một dự án dùng ux-skill. Sau `pip install --upgrade uxskill`. `--stats` sau khi cài, sau khi nâng cấp, hoặc khi một khuyến nghị đưa ra lựa chọn bất ngờ và bạn nghi manifest chưa đầy đủ.
- **Khi bỏ qua:** Bạn đã chạy trong dự án này và không có gì thay đổi. `--stats` không bao giờ cần bỏ qua: chỉ là một lần đọc 50ms.
- **Gọi:** `/ux-init` (không tham số), `/ux-init --stats`, hoặc `uxskill init` / `uxskill stats` từ CLI. `--decisions` thêm phần tóm tắt sổ cái quyết định; `--html` ghi ra `.ux/stats.html`.
- **Đầu ra:** Artifact theo IDE (xem [Trình cài đặt 17 IDE](#trình-cài-đặt-17-ide)) + thư mục `.ux/` + tóm tắt qua stdout. `--stats`: JSON ra stdout (xem [Xác minh cài đặt](#xác-minh-cài-đặt) ở trên).
- **Nối vào:** `/ux-discover` kế tiếp. `--stats` chỉ để chẩn đoán.

#### `/ux-mcp`: chạy bộ máy như một máy chủ MCP

- **Là gì:** Khởi động bộ máy như một máy chủ Model Context Protocol qua stdio. 25 tool (recommender, linter, lưu trữ, bộ tổng hợp, sổ cái quyết định, trích xuất từ hình ảnh, các manifest dữ liệu, cùng việc dựng, nhập, cải thiện, mở rộng, xuất và kiểm tra một hệ thống thiết kế) có thể được gọi từ bất kỳ host nào hỗ trợ MCP, không cần plugin.
- **Khi dùng:** Bạn làm việc trong một host khác hỗ trợ MCP và muốn cùng bộ máy. Bạn chạy pipeline nhiều agent cần một nguồn ràng buộc thiết kế duy nhất. Bạn muốn recommender hoặc linter là một tiến trình chạy lâu dài trong CI.
- **Khi bỏ qua:** Bạn đang ở trong Claude Code với plugin đã cài; slash command đã chạm tới bộ máy. Bạn cần câu trả lời một lần; `uxskill recommend` hoặc `uxskill lint` đơn giản hơn.
- **Gọi:** `/ux-mcp`, hoặc `ux-mcp` từ shell sau `pip install 'uxskill[mcp]'`.
- **Đầu ra:** Một máy chủ JSON-RPC qua stdio. Xem [Máy chủ MCP](#máy-chủ-mcp-nước-cờ-bất-đối-xứng) và `commands/ux-mcp.md` để cấu hình cho từng client.
- **Nối vào:** Không gì cả; đây là lớp truyền tải, không phải một bước.

### Discovery & khuyến nghị

#### `/ux-discover`: hàm cưỡng chế (intake 10 trường, framing, khuyến nghị)

- **Là gì:** Bản intake 10 trường bắt buộc mà mọi dự án phải qua trước bất kỳ lệnh sinh mã nào. Loại dự án, đối tượng, mục tiêu chính, giọng điệu, yêu cầu bắt buộc, điều cấm, thương hiệu tham chiếu, stack, khu vực, chỉ số thành công. **Không ứng tác.** Các cụm từ bị cấm ("modern", "clean") buộc người dùng phải cụ thể. Sau đó chạy recommender: 5 tìm kiếm song song của bộ máy Python trên 12 manifest trả về một hệ thống thiết kế hợp nhất (Ngành → Phong cách → Bảng màu → Chữ → Chuyển động + Component + Thương hiệu hình mẫu + Rào chắn).
- **Chế độ:** `--frame` ghi nhận cho ai, kết quả, giả thuyết và tín hiệu thành công trong một khối framing bốn trường, nhẹ hơn bản intake đầy đủ. `--recommend` chỉ chạy recommender, từ brief đã lưu hoặc từ flag một lần.
- **Khi dùng:** Trước bất kỳ `/ux-design` hay `/ux-system` nào. Bất cứ khi nào brief trước đã cũ. `--frame` khi bắt đầu dự án, sprint hay một việc lẻ, hoặc giữa chừng khi cuộc trao đổi đã lạc hướng. `--recommend` khi định vị lại một sản phẩm trông đã mệt mỏi.
- **Khi bỏ qua:** Bạn đang sửa bug (`/ux-fix`). Bạn chỉ chạy một lượt linter (`/ux-lint`). Brief không đổi so với phiên trước.
- **Gọi (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"`, hoặc `/ux-discover --recommend`.
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
- **Đầu ra:** `.ux/last-discovery.json` (brief 10 trường), `.ux/last-recommendation.json` (phong cách đã chọn, bảng màu, cặp chữ, 5 preset chuyển động hàng đầu, 12 component hàng đầu, 5 thương hiệu hình mẫu hàng đầu, toàn bộ 171 rào chắn anti-pattern đang bật, kèm lý giải), và với `--frame`, `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **Nối vào:** `/ux-design [extra brief]` → code frontend bám sát khuyến nghị. `/ux-design --component <name>` → một component khớp với các ràng buộc đã tìm ra. `/ux-system` → hệ thống thiết kế đầy đủ từ khuyến nghị. `/ux-lint` → xác minh code đã sinh.

### Sinh code

#### `/ux-design`: sinh một bề mặt đẹp, chống slop từ một brief

- **Là gì:** Sinh một artifact frontend hoàn chỉnh, chất lượng production (landing, marketing site, app shell) từ brief discovery + khuyến nghị. Điều phối `frontend-engineer` với hướng sáng tạo từ tham chiếu anti-slop và kho vũ khí. Brief, hoặc một flag, chọn một trong bốn chế độ:
  - **trang** (mặc định): một trang đầy đủ hoặc một bề mặt nhiều section. Ghi `.ux/last-design.json`.
  - **`--component [name]`**: một component đơn lẻ chất lượng production (button, modal, navbar, sidebar, card, bảng, form, biểu đồ). Đủ bốn trạng thái tương tác, dễ tiếp cận, đúng thương hiệu. Tìm component trong `.ux/last-recommendation.json` trước, nếu không có thì truy vấn thẳng manifest. Ghi `.ux/last-component.json`.
  - **`--dashboard`**: kỷ luật mật độ dữ liệu, layout bento, số monospace dạng bảng, mẫu sparkline, chống lạm dụng card, màu trạng thái có nghĩa, chuyển động tiết chế. Không phải trang marketing dán chart lên. Ghi `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: đọc một ảnh tham chiếu thiết kế (PNG/JPG/WebP) bằng thị giác máy tính thuần Pillow (bảng màu chủ đạo, cực tính nền, tín hiệu chữ), đối chiếu với các manifest bảng màu và phong cách, rồi dựng từ khuyến nghị thu được. `--extract-only` dừng sau bước trích xuất. Ghi `.ux/last-image-extract.json`.
- **Khi dùng:** "Design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "build a button", "design the admin panel", "operator console", "KPI board", "build it like this screenshot", bất kỳ yêu cầu sản phẩm hình ảnh tự do nào.
- **Khi bỏ qua:** Bạn muốn review, không phải build (dùng `/ux-audit` hoặc `/ux-critique`). Việc backend hay hạ tầng.
- **Gọi:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`.
- **Đầu ra:** Code được sinh (HTML / Blade / JSX / Vue / Astro), cộng tệp trạng thái của chế độ đó.
- **Nối vào:** `/ux-lint` → xác minh đối chiếu rào chắn. `/ux-polish` → pass mỹ thuật. `/ux-a11y` → audit khả năng truy cập. `/ux-copy` → review microcopy. `/ux-fix` → áp dụng phát hiện thành các commit nguyên tử.

#### `/ux-system`: sinh một hệ thống thiết kế khởi đầu đầy đủ

- **Là gì:** Đề xuất một hệ thống thiết kế khởi đầu đầy đủ cho dự án chưa có, token (màu, typography, không gian, motion, radius, shadow), tài liệu nền tảng, hợp đồng component, cặp dark-mode, công tắc theme. Điều phối `design-system-architect`.
- **Khi dùng:** "We don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS".
- **Khi bỏ qua:** Dự án đã có hệ thống thiết kế; thay vào đó hãy dùng `/ux-design --component` trên hệ thống hiện có. Backend hay hạ tầng.
- **Gọi:** `/ux-system create` (bộ máy nền tảng), `/ux-system enhance --from <file>` (đo một hệ thống bạn đã có), `/ux-system extend --from <file> --add <foundation>` (bổ sung mà không thay đổi nó), hoặc `/ux-system` (luồng của 3.x; chạy discovery trước nếu chưa có sẵn file).
- **Đầu ra:** `tokens.json`, `foundations.md`, các hợp đồng `components/*.md`, phát Tailwind / vanilla / SCSS tùy chọn. Ghi `.ux/last-system.json` cho ngữ cảnh chuỗi.
- **Nối vào:** `/ux-design --component` → dựng trên hệ thống mới. `/ux-design` → sinh một bề mặt dùng token mới.

#### `/ux-motion`: xử lý chuyển động

- **Là gì:** Sinh lớp chuyển động của một bề mặt, thời lượng, easing, biên đạo, fallback reduced-motion, kỷ luật hiệu năng. Cũng audit chuyển động hiện có đối chiếu 5 chiều (timing, easing, ý nghĩa, reduced-motion, hiệu năng).
- **Khi dùng:** "Motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "performance pass on the motion".
- **Khi bỏ qua:** Bề mặt không có chuyển động (dùng `/ux-audit` hoặc `/ux-polish`). Backend hay hạ tầng.
- **Gọi:** `/ux-motion path/to/component.tsx` (chế độ audit) hoặc `/ux-motion --generate hero-entry` (sinh).
- **Đầu ra:** Code cập nhật (ở chế độ sinh) hoặc báo cáo `.ux/last-motion.json` (ở chế độ audit).
- **Nối vào:** `/ux-fix` → áp dụng phát hiện motion. `/ux-polish` → siết chặt.

### Audit & xác minh

#### `/ux-lint`: linter dựa trên regex xác định (không LLM, CI-safe)

- **Là gì:** Chạy 171 quy tắc trên code của bạn. Không gọi LLM. Exit khác 0 ở Critical / High trong CI. Nguồn: `data/anti-patterns.json`. Quy tắc bao trùm A11y (45), Nội dung (35), Layout (18), Typography (16), Motion (14), Visual (14), Chất lượng (12), Màu (10), Hiệu năng (5), Chiều sâu (2).
- **Khi dùng:** Pre-commit hook. Cổng CI. Pass đầu nhanh trên codebase lớn trước khi trả giá `/ux-audit`. Sau `/ux-design` ở bất kỳ chế độ nào để xác minh việc sinh.
- **Khi bỏ qua:** Bạn muốn vòng lặp fix (linter báo cáo, không sửa, nối vào `/ux-polish --fix` hoặc `/ux-fix`). Bạn muốn phán xét gu thẩm mỹ (dùng `/ux-critique`).
- **Gọi (slash):** `/ux-lint src/`.
- **Gọi (CLI):** `uxskill lint .` hoặc `python3 bin/ux-lint.py .` hoặc `bash bin/ux-lint.sh --ci --fail-on high`.
- **Gọi (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **Đầu ra:** Phát hiện ra stdout (vị trí, id quy tắc, mức độ, bằng chứng). Exit code 0 nếu sạch, khác 0 ở Critical/High khi đặt `--fail-on high`.
- **Nối vào:** `/ux-polish --fix` → đối tác được dẫn dắt bởi LLM trên cùng mẫu. `/ux-fix` → áp dụng phát hiện thành commit, sắp xếp theo mức độ. `/ux-audit` → pass suy luận 6 lăng kính đầy đủ. `/ux-next` → để nhạc trưởng quyết định.

#### `/ux-audit`: audit thiết kế 6 lăng kính

- **Là gì:** Một review có cấu trúc, có chính kiến đối chiếu sáu lăng kính (rõ ràng, phân cấp, khả năng truy cập, giọng nói, motion, gu thẩm mỹ), sinh ra phát hiện được gắn nhãn mức độ. Báo cáo phong cách Polaris. Đọc `.ux/last-frame.json` trước, đối tượng và outcome neo mức độ của mỗi phát hiện.
- **Khi dùng:** Bề mặt tồn tại và bạn muốn một phê bình có thể bảo vệ được. "Audit", "review the ux", "is this any good", "what's broken", "tear this apart".
- **Khi bỏ qua:** Bề mặt chưa tồn tại (dùng `/ux-design`). Người dùng muốn một lăng kính (dùng command nhắm mục tiêu: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`). Người dùng muốn ý kiến gu thẩm mỹ (dùng `/ux-critique`). Backend hay hạ tầng.
- **Gọi:** `/ux-audit https://example.com/pricing` hoặc `/ux-audit src/components/Pricing.tsx`.
- **Đầu ra:** Ghi `.ux/last-audit.json`, mảng `findings` gồm `{lens, severity, title, principle, evidence, fix}`, `severity_counts`, `dominant_lens`, `strategic_moves`.
- **Nối vào:** `/ux-fix` → áp dụng phát hiện. `/ux-polish` → pass mỹ thuật. `/ux-design` → nếu cần redesign cấu trúc.

#### `/ux-a11y`: audit WCAG 2.1 AA + các kiểm tra lịch sự thông thường

- **Là gì:** Một audit WCAG 2.1 AA có cấu trúc, cộng với các kiểm tra lịch sự thông thường mà công cụ tự động vượt qua nhưng vẫn làm tổn thương người dùng thật (khả năng nhìn thấy focus, độ cụ thể của lỗi, ưu tiên chuyển động, bẫy bàn phím, phụ thuộc màu sắc).
- **Khi dùng:** Cổng khả năng truy cập trước khi ship. Sau một redesign. "Accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check".
- **Khi bỏ qua:** Không hướng người dùng. Backend hay hạ tầng. Phác thảo work-in-progress.
- **Gọi:** `/ux-a11y https://example.com` (ưu tiên URL trực tiếp, công cụ tự động và kiểm tra bàn phím chỉ hoạt động khi live).
- **Đầu ra:** Ghi `.ux/last-a11y.json`, mảng `findings` gồm `{wcag_sc, sc_name, severity, title, evidence, fix, category}`, mảng `beyond_wcag`, `severity_counts`.
- **Nối vào:** `/ux-fix` → áp dụng phát hiện thành commit. `/ux-copy` → sửa alt text và đấu nối lỗi form như một phần của pass copy.

#### `/ux-critique`: gọi gu thẩm mỹ (3 điểm thắng, 3 điểm trượt, 1 nước cờ chiến lược)

- **Là gì:** Ý kiến của một nhà thiết kế, không phải audit có cấu trúc, không phải điểm mức độ, chỉ là một quan điểm chặt chẽ có chính kiến gọi tên cái gì đang ổn, cái gì không, và một nước cờ chiến lược sẽ thay đổi nhiều nhất.
- **Khi dùng:** "What do you think", "is this good", "critique this", "honest take", "is the vibe right", "does this feel like us", "should we ship this".
- **Khi bỏ qua:** Người dùng muốn rõ ràng một audit có cấu trúc (dùng `/ux-audit`). Backend hay hạ tầng.
- **Gọi:** `/ux-critique https://example.com`.
- **Đầu ra:** Ghi `.ux/last-critique.json`, 3 điểm thắng, 3 điểm trượt, 1 nước cờ chiến lược, kèm văn xuôi.
- **Nối vào:** `/ux-design` nếu quan điểm khuyến nghị redesign. `/ux-polish` nếu quan điểm khuyến nghị siết chặt.

#### `/ux-copy`: review + viết lại microcopy

- **Là gì:** Đánh giá mọi chuỗi nhìn thấy được đối chiếu rubric giọng nói và sinh ra một viết-lại trước/sau. Bắt: "form contains errors" (chung chung), "John Doe" (placeholder), copy AI vui mừng tưng bừng, CTA chung chung, empty state chết, lỗi vô dụng.
- **Khi dùng:** Cấu trúc đúng nhưng câu chữ yếu. "Review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "tighten the strings", "the buttons sound generic", "this empty state is dead".
- **Khi bỏ qua:** Vấn đề layout (dùng `/ux-audit` hoặc `/ux-polish`). Vấn đề copy do khả năng truy cập như alt text (dùng `/ux-a11y`). Backend hay hạ tầng.
- **Gọi:** `/ux-copy src/views/checkout.blade.php`.
- **Đầu ra:** Ghi `.ux/last-copy.json`, mảng `strings` gồm `{location, severity, before, after, notes}`, kèm rubric + các locale cần dịch.
- **Nối vào:** `/ux-fix` → áp dụng viết-lại. `/ux-a11y` → kiểm tra lại sau khi sửa copy.

### Fix & polish

#### `/ux-fix`: áp dụng phát hiện thành các commit nguyên tử

- **Là gì:** Đọc báo cáo mới nhất từ `.ux/` (audit, copy, a11y, motion, hoặc polish), xác thực cây làm việc, và áp dụng phát hiện thành các commit nguyên tử qua đúng sub-agent. Xác minh lại bằng cách chạy lại command gốc.
- **Khi dùng:** Sau khi chạy một command lớp audit và review phát hiện. "Fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it".
- **Khi bỏ qua:** Không có báo cáo trước trong `.ux/`. Cây làm việc bẩn và người dùng chưa đồng ý stash/commit. Sửa cần phán xét thiết kế, không phải áp dụng máy móc (dùng `/ux-design` cho redesign).
- **Gọi:** `/ux-fix` (tự phát hiện báo cáo nào để sửa) hoặc `/ux-fix --from=last-a11y.json`.
- **Đầu ra:** Các commit nguyên tử cho mỗi phát hiện. Chạy lại command gốc và cập nhật file `.ux/last-*.json`. In ra một tóm tắt.
- **Nối vào:** `/ux-next` → nhạc trưởng chọn nước cờ kế tiếp.

#### `/ux-polish`: vòng lặp lint, fix, re-lint + diệt AI-slop

- **Là gì:** Trước tiên là một vòng lặp xác định trên tệp HTML cục bộ: lint, áp sáu lượt polish idempotent, re-lint, cho đến khi điểm đạt 90, chững lại, hoặc qua ba vòng (`--rounds` đổi giới hạn). Mặc định kết quả vòng lặp nằm ở `<file>.evolved.html` và tệp gốc không bao giờ bị động đến. Chỉ `--loop-only` hoặc `--fix` mới thay tệp gốc, sau khi kiểm tra working tree sạch, và quality gate ở 65 ngăn một kết quả không đạt thay thế nó nếu không có `--force`; với `--brand-file`, ngưỡng sàn trung thành thương hiệu được giữ ở mọi lối ra. Sau đó là lượt gu thẩm mỹ: nhịp khoảng cách, phân cấp sắc nét hơn, phát hiện AI-slop, tính nhất quán token. Phiên bản dẫn dắt bởi LLM tương ứng với `/ux-lint`, dùng phán đoán của bạn cho các quyết định về gu. `--loop-only` chỉ chạy vòng lặp; `--no-loop` chỉ chạy lượt gu; `--fix` áp dụng các phát hiện về gu.
- **Khi dùng:** Cấu trúc đúng nhưng thực thi lỏng lẻo. "Polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste", "improve until score 90+", "make it ship-ready".
- **Khi bỏ qua:** Bề mặt còn thiếu chức năng cốt lõi (sửa cái đó trước). Cần thiết kế lại, không phải đánh bóng (dùng `/ux-design`). Vấn đề về chữ nghĩa (dùng `/ux-copy`). Vấn đề chuyển động (dùng `/ux-motion`). Vấn đề a11y (dùng `/ux-a11y`).
- **Gọi:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`.
- **Đầu ra:** `<file>.evolved.html` từ vòng lặp (chỉ thay tệp gốc khi có `--loop-only` hoặc `--fix`), code đã cập nhật khi có `--fix`, `.ux/last-evolve.json`, một dòng trong `.ux/decisions.jsonl`, và `.ux/last-polish.json` mô tả các phát hiện về gu.
- **Nối vào:** `/ux-lint` → xác minh phần đánh bóng còn giữ. `/ux-a11y` → kiểm tra lại khả năng tiếp cận.

### Discovery & tự sự

#### `/ux-research`: lên kế hoạch + tổng hợp nghiên cứu

- **Là gì:** Chế độ kế hoạch: viết script phỏng vấn, khảo sát, bộ sàng tuyển. Chế độ tổng hợp (`--synthesize`): tiêu hóa phỏng vấn, analytics, trang đối thủ, kết quả A/B, ticket hỗ trợ thành khuyến nghị. Điều phối `research-synthesizer`.
- **Khi dùng:** "Plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes".
- **Khi bỏ qua:** Câu trả lời đã biết với độ tin cậy cao. Quyết định có thể đảo ngược, rủi ro thấp. Backend hay hạ tầng.
- **Gọi:** `/ux-research --plan "loyalty wallet adoption in MENA"` hoặc `/ux-research --synthesize interviews/*.md`.
- **Đầu ra:** Ghi `.ux/last-research.json`, kế hoạch nghiên cứu hoặc các chủ đề được tổng hợp + bằng chứng + khuyến nghị.
- **Nối vào:** `/ux-discover --frame` → đưa phát hiện vào một frame. `/ux-design` → sinh từ phát hiện. `/ux-workshop` → chạy workshop với nghiên cứu làm đầu vào.

#### `/ux-workshop`: workshop design thinking 5 giai đoạn

- **Là gì:** Hỗ trợ một workshop discovery / design-thinking đầu cuối. Năm giai đoạn tuần tự (khám phá → bản đồ nhiệt → bản đồ bên liên quan → phác thảo giải pháp → kế hoạch chơi). Có giới hạn thời gian. Artifact cụ thể cho mỗi giai đoạn. Kết thúc bằng một quyết định, không phải "phát hiện thú vị".
- **Khi dùng:** Câu hỏi thật, người tham gia thật, ngân sách thời gian thật. "Run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "kick off the project".
- **Khi bỏ qua:** Brief đã rõ ràng và có phạm vi. Brainstorm một mình (dùng `/ux-design` hoặc `/ux-discover --frame`). Đội đang giữa giai đoạn thực thi, không phải discovery.
- **Gọi:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **Đầu ra:** Ghi `.ux/last-workshop.json`, kế hoạch chơi + artifact theo giai đoạn.
- **Nối vào:** `/ux-design` → thực thi kế hoạch chơi. `/ux-research` → lấp các khoảng trống workshop làm nổi lên. `/ux-case-study` → xuất bản hành trình.

#### `/ux-case-study`: case study có thể xuất bản (định dạng Wfrah-editorial)

- **Là gì:** Sinh case study dự án theo định dạng biên tập đơn sắc thuần, chữ Wfrah, đường phân cách mảnh, mã section đánh số từ (A) đến (G), layout an toàn cho song ngữ. Một tài liệu, không phải brochure marketing. Đọc từ `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json`.
- **Khi dùng:** Sau khi launch. Sau một mốc rời rạc. "Write a case study", "case study this project", "do the wrap-up doc", "publish this work", "portfolio piece".
- **Khi bỏ qua:** Dự án thiếu dữ liệu để điền các section từ (A) đến (G). Người dùng muốn landing marketing, không phải case study (dùng `/ux-design`).
- **Gọi:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **Đầu ra:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **Nối vào:** Command tận cùng, thường là kết thúc một dự án.

### Nhạc trưởng

#### `/ux-next`: nhạc trưởng workflow (chỉ đọc)

- **Là gì:** Đọc mọi `.ux/last-*.json` và gọi tên command kế tiếp có đòn bẩy cao nhất. Một nhạc trưởng, không phải thợ xây. Chỉ đọc.
- **Khi dùng:** Giữa các command. "What should I do next", "what's the next move", "decide for me", "where do we go from here".
- **Khi bỏ qua:** Không có báo cáo trước trong `.ux/`. Bạn có một command kế tiếp cụ thể trong đầu.
- **Gọi:** `/ux-next` (không tham số) hoặc `/ux-next --focus=a11y`.
- **Đầu ra:** Stdout, command kế tiếp được khuyến nghị + lý giải.
- **Nối vào:** Bất kỳ command nào nó chọn.

#### `/ux-expert`: móc nối tư vấn

- **Là gì:** Đưa ra thông tin liên hệ của tác giả plugin khi người dùng hỏi về một chuyên gia UX đời thực. Ngắn gọn, thẳng thắn, không marketing.
- **Khi dùng:** "Who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin".
- **Khi bỏ qua:** Người dùng đang hỏi về tính năng plugin, không phải tư vấn.
- **Gọi:** `/ux-expert`.
- **Đầu ra:** Thẻ liên hệ ngắn với LinkedIn / email / repo.

### Alias, bị bỏ ở 4.1

Bảy lệnh của 3.x đã gộp vào 18 lệnh ở trên. Tên của chúng vẫn chạy thêm một bản phát hành: mỗi alias cho biết nó đã chuyển đi đâu, rồi chạy lệnh mới với cùng tham số.

| Lệnh cũ | Hiện tại | Ghi chú |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | Cùng khối framing, cùng `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | Tool MCP `ux_recommend` không đổi |
| `/ux-stats` | `/ux-init --stats` | Ảnh chụp chỉ đọc |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | Alias giữ giới hạn cũ năm vòng; riêng `/ux-polish` dừng ở ba |
| `/ux-component` | `/ux-design --component` | Cùng `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | Cùng `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | Bỏ `--extract-only` để dựng từ hình ảnh |

### Đồ thị nối chuỗi command

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

Sub-agent là các trình sinh chuyên vai trò được điều phối bởi command. Chúng không bao giờ chạy độc lập: chúng được gọi bởi `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research`, v.v. Mỗi agent có một phạm vi trách nhiệm rõ ràng: chúng KHÔNG quyết định brief; chúng thực thi theo brief.

### `frontend-engineer`

- **Sở hữu:** Code frontend chất lượng production (React, Next.js, Vue, Blade+Alpine, HTML thuần, Astro) với kỷ luật chống AI-slop.
- **Được điều phối bởi:** `/ux-design` (các chế độ trang, component, dashboard và hình ảnh), `/ux-fix`.
- **Đầu vào:** Brief + hướng sáng tạo + token (từ `.ux/last-recommendation.json`).
- **Đầu ra:** Code chạy được, phân biệt được với output AI chung chung. Không gradient tím, không hero căn giữa, không ba card bằng nhau, không Inter ở kích thước display, không "John Doe", không emoji, không mặc định 300ms.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **Sở hữu:** Chuyển động trong code frontend production, Framer Motion, GSAP, CSS animation. Thời lượng, easing, biên đạo, fallback reduced-motion, kỷ luật hiệu năng.
- **Được điều phối bởi:** `/ux-design` (mọi chế độ), `/ux-motion --fix`.
- **Đầu vào:** Brief chuyển động + token + 57 preset chuyển động từ `data/motion-presets.json`.
- **Đầu ra:** Chuyển động xứng đáng có chỗ đứng. Luôn được bọc trong fallback `prefers-reduced-motion`. Luôn được thử nghiệm đối chiếu Core Web Vitals.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **Sở hữu:** Các chuỗi được ship, thông điệp lỗi, empty state, CTA, loading state, thông điệp thành công, toast, helper text, label form, text button.
- **Được điều phối bởi:** `/ux-copy --fix`, `/ux-design` (mọi chế độ), `/ux-discover --frame`.
- **Đầu vào:** Hồ sơ giọng nói (được đặt tên hoặc dán vào) + các chuỗi của bề mặt.
- **Đầu ra:** Microcopy production được áp dụng nhất quán qua mọi trạng thái của một bề mặt để sản phẩm nghe như một sản phẩm, không phải mười. Cấm: "form contains errors", "John Doe", copy AI vui mừng tưng bừng, CTA chung chung, empty state chết.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **Sở hữu:** Tiêu hóa đầu vào nghiên cứu (phỏng vấn, analytics, trang đối thủ, kết quả A/B, ticket hỗ trợ) thành khuyến nghị thiết kế hành động được.
- **Được điều phối bởi:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`.
- **Đầu vào:** Nghiên cứu thô, transcript, export, URL đối thủ, cụm hỗ trợ.
- **Đầu ra:** Chủ đề, bằng chứng, khuyến nghị. Không bao giờ thiết kế câu trả lời, trao cho nhà thiết kế nền tảng để thiết kế từ đó.
- **Tool:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **Sở hữu:** Hệ thống thiết kế đầy đủ, token (màu, typography, không gian, motion, radius, shadow), tài liệu nền tảng, hợp đồng component, cặp dark-mode, lớp theming.
- **Được điều phối bởi:** `/ux-system`, `/ux-design --component` khi chưa có hệ thống.
- **Đầu vào:** Brief thương hiệu + `.ux/last-recommendation.json` (phong cách + bảng màu + cặp typography + preset chuyển động).
- **Đầu ra:** Một hệ thống mạch lạc, có chính kiến, sẵn sàng production mà các agent phía sau có thể xây dựng đối chiếu mà không cần quyết định lại nền tảng. Token JSON, foundations MD, hợp đồng component, ánh xạ dark-mode.
- **Tool:** `Read, Write, Edit, Bash, Glob, Grep`.

### Giao thức điều phối sub-agent

Khi một command điều phối một sub-agent, nó truyền:

1. Brief / khuyến nghị (được load từ `.ux/`).
2. Lát manifest liên quan (ví dụ, `frontend-engineer` nhận phong cách + bảng màu + component đã chọn; `motion-engineer` nhận preset chuyển động đã chọn).
3. 171 rào chắn anti-pattern (luôn được kích hoạt).
4. Một tiêu chí thành công (artifact phải làm gì).

Sub-agent trả về:

1. Artifact (code, tài liệu, hệ thống).
2. Một khối lý giải (vì sao chọn thế này).
3. Một tự kiểm tra đối chiếu rào chắn (quy tắc nào đã xác minh).

Command gọi sau đó tự động chạy `/ux-lint` trước khi tuyên bố hoàn thành.

---

## 11 data manifest

Lớp dữ liệu là bộ não. Mọi command đọc từ nó; bộ máy merge xuyên qua nó; linter quét đối chiếu nó. Mọi file sống dưới `data/` và bọc entry của chúng trong `{_meta, entries}` cho versioning schema.

### `styles.json`: 84 phong cách thiết kế

| Trường | Mô tả |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, v.v. |
| `sample entry` | `swiss-international`, "Grid là luật. Typography làm việc nặng. Trang trí là thất bại." |

Được dùng bởi: `/ux-discover`, `/ux-system`, `/ux-design`. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 bảng màu

| Trường | Mô tả |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (sáng/tối), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, v.v. |
| `sample entry` | `claude-warm-editorial`, sáng, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

Được dùng bởi: `/ux-discover`, `/ux-system`. Contrast đã xác minh ở AA / AAA. Schema: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 cặp typography

| Trường | Mô tả |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weight + nguồn + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

Mọi family đều có giấy phép + URL nguồn. Được dùng bởi `/ux-discover`, `/ux-system`.

### `components.json`: 148 component

| Trường | Mô tả |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, anatomy 6 phần, 4 state |

Đây là hào lũy lớn nhất của chúng tôi. Không có plugin UX Claude nào khác ship được manifest component có cấu trúc.

### `industries.json`: 184 quy tắc ngành nghề

| Trường | Mô tả |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, v.v. |
| `sample entry` | `fintech-neobank`, độ tin cậy cao, công bố quy định, UI chính cho số dư/giao dịch, mobile-first sử dụng hàng ngày |

Được recommender (`/ux-discover`) dùng làm trục tìm kiếm song song đầu tiên.

### `chart-types.json`: 35 loại biểu đồ

| Trường | Mô tả |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, so sánh từ 4 đến 15 danh mục rời rạc. Vị trí trên trục x biểu thị danh mục; chiều cao biểu thị giá trị. |

Được dùng bởi `/ux-design --dashboard` và `/ux-design --component` (instance chart).

### `tech-stacks.json`: 25 stack

| Trường | Mô tả |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, tương thích với Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

Các stack khác gồm Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025.

### `ux-guidelines.json`: 112 quy luật UX có tên

| Trường | Mô tả |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, v.v. |
| `sample entry` | `hicks-law`, Thời gian quyết định tăng theo log của số lượng lựa chọn được trình bày |

Được dùng bởi `/ux-audit` (chấm điểm 6 lăng kính) và `/ux-critique` (neo gu thẩm mỹ).

### `motion-presets.json`: 57 preset chuyển động

| Trường | Mô tả |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (fallback reduced-motion), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

Mọi preset đều có biến thể reduced-motion. Code sẵn sàng theo stack cho Framer Motion, GSAP, và CSS thuần.

### `anti-patterns.json`: 171 quy tắc

| Trường | Mô tả |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (loại, mẫu, flag, phạm vi, và với nhiều quy tắc là một bước kiểm tra `post` trên tệp đã phân tích), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

Danh sách quy tắc đầy đủ nằm ở [171 quy tắc chống AI-slop](#171-quy-tắc-chống-ai-slop-bộ-linter).

### `brands/*.json`: 160 spec thương hiệu

| Trường | Mô tả |
|---|---|
| `entries` | 160 (cộng với `_index.json` liệt kê tất cả) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

Danh sách đầy đủ ở [160 spec DESIGN.md thương hiệu](#160-spec-designmd-thương-hiệu-theo-danh-mục).

---

## 171 quy tắc chống AI-slop: bộ linter

ux-skill ship một linter xác định: mỗi quy tắc là một mẫu, và nhiều quy tắc thêm bước kiểm tra trên CSS và markup đã phân tích, nên một kết quả khớp chỉ được tính trong ngữ cảnh mà quy tắc nêu ra. **Không LLM.** **Không API.** **Không mạng.** Chạy trong CI mất ~200ms với một ứng dụng Next.js điển hình. Exit khác 0 với phát hiện Critical / High khi đặt `--fail-on high`.

Quy tắc lấy từ `data/anti-patterns.json` (v2, ưu tiên) với dự phòng `references/foundations/anti-patterns.md` (v1, bash). Hai binary được ship: `bin/ux-lint.py` (Python, nhanh, mở rộng được) và `bin/ux-lint.sh` (Bash + perl-PCRE, cho môi trường không có Python).

### Quy tắc theo danh mục

Danh mục đầy đủ của 171 quy tắc, theo nhóm rồi theo mức độ, được sinh từ `data/anti-patterns.json` vào [README tiếng Anh](README.md#rules-by-category); ở đó ID và tên quy tắc giữ nguyên như linter in ra. Quy tắc bao trùm A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### Cách dùng linter

**Quét một lần:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
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

## 160 spec DESIGN.md thương hiệu: theo danh mục

Thương hiệu thật. Ngôn ngữ thiết kế thật. Spec DESIGN.md thật, không phải palette chung chung. Bảo plugin "xây một landing theo phong cách Stripe" và nó đọc đúng từ vựng thương hiệu thực: rubric giọng nói, token màu, quy ước motion, nước cờ chữ ký, nước cờ kiêng kỵ.

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

8 plugin UX Claude phổ biến khác sinh ra "modern minimal" hoặc "clean dashboard", các biến thể của cùng một thẩm mỹ mặc định. ux-skill cho phép bạn yêu cầu **sự rõ ràng của Linear**, **sự nghiêm túc của Stripe**, **sự kiềm chế của Apple**, **khối nguyên thạch của Tesla**, **sự thân thiện của Notion**, **kỷ luật gradient của Cursor**, **mật độ nét tóc của Raycast**, **editorial ấm của Claude**, và bộ máy kéo đúng token, giọng nói, quy ước motion, và nước cờ chữ ký từ spec thương hiệu.

---

## Máy chủ MCP: nước cờ bất đối xứng

ux-skill ship một **máy chủ Model Context Protocol**. Chạy `ux-mcp` và bộ máy trở thành một tiến trình stdio chạy lâu dài mà bất kỳ host nào hỗ trợ MCP (Claude Desktop, Cursor, Windsurf, agent chung) đều có thể gọi vào. 25 tool: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`. Cùng các handler Python mà slash command dùng; cùng các data manifest; cùng bộ recommender xác định.

**Vì sao đây là nước cờ bất đối xứng:** không một trong tám skill UX Claude hàng đầu (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) nào ship máy chủ MCP. Chúng bị khóa bên trong runtime plugin của Claude Code. ux-skill có thể truy cập từ bất kỳ host nào nói MCP, bao gồm cả các agent chưa bao giờ nghe đến plugin Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

Trỏ client của bạn đến binary `ux-mcp`. Tài liệu tool đầy đủ, ví dụ JSON, và cấu hình theo client cho Claude Desktop, Cursor, và Windsurf sống tại [docs/mcp.html](docs/mcp.html) và trong `commands/ux-mcp.md`.

---

## Trình cài đặt 17 IDE

`uxskill init` (hoặc `/ux-init` bên trong Claude Code) tự phát hiện IDE bạn đang dùng và ghi đúng artifact. Cùng bộ máy Python. Cùng khuyến nghị. Keo dán khác nhau theo từng IDE.

| IDE / công cụ | Tín hiệu phát hiện | Artifact được cài |
|---|---|---|
| Claude Code | `.claude/` hoặc `CLAUDE.md` | Manifest plugin tại `.claude-plugin/plugin.json` + toàn bộ 18 command (và 7 alias) + toàn bộ 5 sub-agent |
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

## Tình huống sử dụng: kịch bản cụ thể

Tám kịch bản thật. Chọn cái gần tình huống của bạn nhất và điều chỉnh lệnh gọi.

### 1. Xây dashboard fintech trong Cursor

Bạn đang ở trong Cursor làm dashboard cho neobank MENA. Bạn cài plugin và chạy discovery, khuyến nghị, rồi sinh dashboard.

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

/ux-discover --recommend
> [returns picked style, palette, type pair, motion presets, components, brand exemplars]

/ux-design "generate the landing using the Stripe brand spec as exemplar"
> [frontend-engineer generates the page]

/ux-lint .
> [passes, Stripe brand spec was respected]
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
> [3 wins, 3 misses, 1 strategic move, the take is honest]

/ux-lint src/
> [15 high-severity AI fingerprints flagged]

/ux-polish src/components/Hero.tsx
> [LLM-driven cosmetic pass + AI-slop kill]

/ux-fix
> [applies findings as atomic commits, re-runs the linter]
```

Ba command, một bề mặt được polish, commit nguyên tử cho mỗi fix.

### 5. Thiết kế command palette theo phong cách Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

Component sinh ra dùng đúng token màu, stack typography, quy ước motion, mật độ hairline thực của Linear, không phải "dark UI chung chung".

### 6. Chạy workshop design thinking 90 phút với các bên liên quan

Bạn có một phòng 5 người trong 90 phút. Bạn muốn họ rời đi với một kế hoạch chơi, không phải một cảm hứng.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

Plugin hỗ trợ năm giai đoạn (khám phá → bản đồ nhiệt → bản đồ bên liên quan → phác thảo giải pháp → kế hoạch chơi) đầu cuối, có giới hạn thời gian, với artifact cụ thể cho mỗi giai đoạn. Đầu ra là `.ux/last-workshop.json`, kế hoạch chơi, không chỉ "phát hiện thú vị".

### 7. Viết case study có thể xuất bản sau khi launch

Bạn ship ví loyalty. Bạn muốn một tác phẩm portfolio.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

Case study là một artifact hoàn thiện, có thể xuất bản, không phải bản nháp. Đơn sắc tinh khôi, typography editorial, sẵn sàng ship lên portfolio của bạn.

### 8. Chạy discovery trong ngữ cảnh không-AI (chỉ thu thập có cấu trúc)

Bạn đang phạm vi hóa một dự án. Bạn chưa cần khuyến nghị, bạn cần một brief có cấu trúc.

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

Bạn có thể trao JSON cho đội của mình, dán vào tài liệu Notion, hoặc nạp vào một công cụ AI riêng. ux-skill cũng là một công cụ thu thập có cấu trúc, ngoài việc là một bộ máy.

### 9. MASTER.md bền vững: quyết định thiết kế của bạn, trong repo

Sau `/ux-discover` (hoặc `/ux-discover --recommend`), lưu phong cách + bảng màu + chữ + chuyển động + component + thương hiệu hình mẫu + rào chắn đã chọn thành một tệp Markdown dễ đọc mà đội bạn có thể review, diff và quản lý phiên bản.

```bash
python3 -m engine.cli.main persist save --project-root .
```

Ghi `.ux/design-system/MASTER.md` (YAML frontmatter + body) và `.ux/design-system/pages/<name>.md` cho mỗi bề mặt được sinh qua `persist save-page`. Idempotent, cùng đầu vào sinh đầu ra giống hệt byte, nên chạy lại trên trạng thái không đổi là no-op trong git.

---

## So sánh với các lựa chọn khác

Bảng tóm tắt ngắn. So sánh đầy đủ từng-bảng tại [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| Chiều | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| Slash command | **18** | 1 | 19 | 1 | 1 | multi | 1 | 1 | 1 |
| Component | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| Preset chuyển động | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Spec thương hiệu | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Quy tắc anti-pattern | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Linter xác định CI-safe | **có** | không | không | không | không | không | không | không | không |
| IDE hỗ trợ | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Cổng discovery | **10 trường** | ngầm | ngầm | ngầm | ngầm | ngầm | ngầm | ngầm | ngầm |
| Chuỗi state `.ux/` | **có** | không | không | không | không | không | không | không | không |
| Sao (2026-05-28) | 14 | 83.958 | 54.406 | 25.202 | 15.455 | 5.762 | 2.391 | 2.164 | 955 |

### Đánh giá thẳng thắn

- **ui-ux-pro-max** lớn hơn về độ nhận biết, ship 18 IDE, có tìm kiếm kiểu BM25 trên CSV của họ. Nó không ship manifest component, manifest motion, thư viện thương hiệu, hay linter xác định.
- **open-design** có 19 skill + preview nhưng chỉ hỗ trợ Claude Code và không có lớp anti-slop.
- **hallmark** gần nhất về tinh thần (cũng anti-slop) nhưng là một skill đơn nhất, không bộ máy, không manifest, không command nối chuỗi.
- **material-3-skill** xuất sắc nếu bạn đặc biệt muốn Material Design 3. Chúng tôi không cạnh tranh trên MD3.

Để xem chi tiết đầy đủ theo từng chiều, xem [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## Lộ trình

Tiếp theo, không gắn với bản phát hành cố định:

- **Style Figma**: effect style cho đổ bóng, grid style và text style gắn với biến của trường, ghi lên một tệp đang mở.
- **Ánh xạ component**: một component Figma và các biến thể của nó được nối với một component trong code và props của nó, giữ nguyên qua bước bàn giao.
- **Trình nhập từ site đang chạy**: đọc hệ thống mà một site đã xuất bản thực sự render, bên cạnh các trình nhập từ tệp.
- **Trang tài liệu cho một hệ thống đã dựng**: góc nhìn cho con người về token, vai trò và hợp đồng của nó.

Vẫn còn mở:

- **`uxskill lint --fix` cho các lần viết lại an toàn** đối với phát hiện sửa được một cách máy móc (button-no-type, img-no-alt chuỗi rỗng, gỡ console-log-leak).
- **Tiện ích VS Code** hiển thị phát hiện lint ngay trong code.
- **Sinh code theo component** cho sáu stack (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, HTML/CSS thuần).
- **Chợ đặc tả thương hiệu**: đăng và khám phá đặc tả thương hiệu của cộng đồng.
- **Quy tắc anti-pattern tùy chỉnh**: khám phá và chia sẻ các quy tắc mà dự án định nghĩa trong `data/anti-patterns.local.json`.
- **`uxskill plan`**: lập kế hoạch site nhiều trang từ một brief, không chỉ một bề mặt.

---

## Đóng góp

Issue và PR được hoan nghênh. Ba khu vực đòn bẩy cao:

### Thêm một quy tắc anti-pattern

1. Sửa `data/anti-patterns.json`, thêm một entry với `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. Thêm một test trong `tests/linter/`, một file kích hoạt quy tắc, một file không.
3. Chạy `uxskill lint tests/linter/should-trigger/<rule>.tsx`, xác nhận nó bắn. Chạy trên `tests/linter/should-not-trigger/<rule>.tsx`, xác nhận nó không bắn.
4. Mở một PR.

### Thêm một spec thương hiệu

1. Tạo `data/brands/<slug>.json` với `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. Thêm văn xuôi tương ứng tại `references/brands/<slug>.md`.
3. Đăng ký trong `data/brands/_index.json`.
4. Mở một PR. Spec phải được hỗ trợ bởi tham chiếu nguồn chính (sản phẩm thực của thương hiệu, hệ thống thiết kế công khai, hoặc DESIGN.md nếu họ có công bố).

### Thêm một preset chuyển động

1. Sửa `data/motion-presets.json`, thêm một entry với `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. Preset phải có một biến thể reduced-motion. Không ngoại lệ.
3. Mở một PR.

### Quy trình

- Đọc [CONTRIBUTING.md](CONTRIBUTING.md) cho quy trình đầy đủ.
- Đọc [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Quy tắc và spec thương hiệu mới được review về: nền tảng nguồn chính, không over-fit vào một dự án duy nhất, không emoji trong bất kỳ dữ liệu nào, hành vi an toàn RTL khi áp dụng được.

---

## Giấy phép, tác giả, lời cảm ơn

### Giấy phép

MIT. Hãy dùng, fork, xây dựng dựa trên. Nếu nó cứu bạn khỏi việc ship AI slop, hãy gắn sao cho repo, đó là cách rẻ nhất để hỗ trợ.

### Tác giả

**Laith Aljunaidy**: nhà sáng lập đơn nhất của [Dot](https://thedotwallet.com), nền tảng loyalty MENA-first. Xây ux-skill để frontend AI-tạo không trông giống nhau hết.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- Email: laith.aljunaidy.laith@gmail.com
- Repo: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- Trang chủ: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### Lời cảm ơn

- Đội ngũ Anthropic vì Claude Code và kiến trúc skill / plugin đã giúp việc này phân phối được.
- Nielsen Norman Group, Laws of UX (lawsofux.com), và cộng đồng nghiên cứu UX có công trình thông báo cho `data/ux-guidelines.json`.
- Mọi thương hiệu được liệt kê trong `data/brands/`, hệ thống thiết kế công khai của họ là nguồn sự thật cho các spec thương hiệu.
- Những người đóng góp v1 ban đầu: một skill Claude một-phát từng là hạt giống cho bộ máy Python v2.
- 8 plugin UX Claude phổ biến mà chúng tôi so sánh, họ nâng cao mức chuẩn; đây là câu trả lời của chúng tôi.

---

**ux-skill** · **v4.0.0** · Được xây để Claude Code, Cursor, Windsurf, và mọi công cụ lập trình AI khác xuất ra frontend không đọc lên như AI tạo.

> Gắn sao repo tại [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · Cài qua `pip install uxskill` hoặc `npx uxskill init` · Xem so sánh tại [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)
