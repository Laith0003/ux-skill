[English](README.md) · **العربية** · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [हिन्दी](README.hi.md) · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

<div dir="rtl">

# ux-skill: محرّك ذكاء التصميم لـ Claude Code وCursor وكل أداة برمجة بالذكاء الاصطناعي

**محرّك لذكاء التصميم يجعل الواجهات التي يولّدها الذكاء الاصطناعي مميّزة بدل أن تكون نمطية.** أضِفه إلى أيّ أداة من 17 أداة للبرمجة بالذكاء الاصطناعي، فلا يعود ناتجك يبدو من صنع الذكاء الاصطناعي. مجاني، برخصة MIT، يعمل دون اتصال، بلا LLM.

```bash
pip install uxskill
```

**[ضع نجمة لـ ux-skill على GitHub](https://github.com/Laith0003/ux-skill)** إن وجدته مفيدًا، فهي أبسط طريقة لدعم المشروع. جديد هنا؟ ابدأ بـ[جولة الـ 60 ثانية](#التثبيت-السريع) أو شاهده حيًّا على [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com).

![قبل: واجهة رئيسية نمطية بصورة من مكتبة صور، وتدرّج بنفسجي باهت، وبلا هوية للعلامة. بعد: صورة حقيقية لموقع بناء تحت طبقة داكنة، وعنوان تحريري بلمسة كهرمانية، ونموذج لطلب عرض سعر داخل الواجهة الرئيسية. الطلب نفسه، ونتيجة مختلفة حين يضع ux-skill القيود.](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*قبل: ركاكة SEO نمطية بصورة من مكتبة صور. بعد: واجهة رئيسية بصورة حقيقية لموقع بناء تحت طبقة داكنة، وعنوان تحريري بلمسة كهرمانية، ونموذج عرض سعر داخلها. أداة البرمجة نفسها، والطلب نفسه، ونتيجة مختلفة حين يضع ux-skill القيود.*

> **الإصدار v4.0، FOUNDATIONS: أمر واحد يبني نظام تصميم كاملًا مفحوصًا وفق WCAG، والعربية والكتابة من اليمين إلى اليسار مدمجتان.** أقوى إضافة لتجربة المستخدم في عالم البرمجة بالذكاء الاصطناعي. نواة استدلال مكتوبة بلغة Python مع مُركِّب حتمي بسبعة محاور، و12 ملفّ بيانات JSON قابلًا للاستعلام (84 أسلوبًا تصميميًا، 176 لوحة ألوان، 70 اقترانًا طباعيًا، 148 مكوّنًا، 184 قطاعًا، 35 نوع رسم بياني، 57 مهيّأة حركة، 112 قانون تجربة مستخدم، 171 قاعدة لكشف الأنماط الضارّة، 25 منظومة تقنية، 160 مواصفة علامة تجارية)، و18 أمرًا من أوامر الشرطة المائلة، و5 وكلاء فرعيين، و25 أداة MCP، ومُدقّق حتمي يقضي على ركاكة الذكاء الاصطناعي. وهي متعدّدة بيئات التطوير: تُثبَّت في Claude Code وCursor وWindsurf وGitHub Copilot وGemini CLI وCodex وKiro وCline وContinue وAider وZed وJetBrains AI وPieces وTabby وTabnine وCodeWhisperer وRoo Cline.

> **اسم العلامة هو `ux-skill`.** اسم الحزمة في PyPI و npm يبقى `uxskill`. ومستودع GitHub موجود على [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill).

**المؤلّف:** [Laith Aljunaidy](https://laithjunaidy.com)، مصمّم ومدير تقني في عمّان · **الموقع:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **قارن مع كل إضافات UX لـ Claude:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0--beta.2-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#مثبّت-17-بيئة-تطوير)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### الجديد في 4.0: الأسس

لون علامتك التجارية يدخل، ونظام تصميم كامل يخرج، وتباينه مفحوص قبل أن يصلك.

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

يتطلّب Python 3.10 أو أحدث. لخادم MCP استخدم `pip install --upgrade 'uxskill[mcp]'`. ومع pipx استخدم `pipx install uxskill` (وفوق إصدار 3.x مثبّت استخدم `pipx upgrade uxskill`). ومع npm استخدم `npx uxskill@latest`. قادم من 3.x؟ [دليل الانتقال](docs/migrating-to-4.md) يربط كل رمز من رموز 3.x بدوره في 4.0.

**تبني منتجًا أو صفحة هبوط؟** تحصل على `tokens.css` لتربطه من صفحتك، و`fonts.css` مع خطوط احتياطية مطابقة في القياسات للخطوط المختارة، و`fonts-self-host.css` الذي يحمّل الخطوط من ملفّاتك أنت، و`tokens.json` للأدوات، ورسومات زخرفية للعلامة في `art/`، و`system-report.md` الذي يشرح بلغة واضحة ما الذي بُني ولماذا، وبأيّ تكوين للصفحة تبدأ. صمّم الأنماط بالأدوار (`var(--color-action-primary)`، `var(--color-text-default)`، `var(--color-surface-page)`)، وبدّل بين الوضع الداكن والتباين العالي والمسافات المضغوطة والكتابة من اليمين إلى اليسار وتقليل الحركة بسمة واحدة على `<html>`. حمّل الخطوط برابط Google Fonts الذي يعطيه التقرير، أو بـ`fonts-self-host.css` ومجلد `fonts/`، واربط `fonts.css` مع أيّ منهما قبل `tokens.css`؛ ولا تعدّل أيًّا من الملفّين. ومع `--brief` يتبع المظهر القطاع والنبرة حين يذكرهما الموجز، وتحدّد الحقول المنظّمة (العمر، اللغات، المخطّط الافتراضي، سياق القراءة) حجم النص ومساحات اللمس وأنظمة الكتابة والمخطّط الذي يُفتح أوّلًا؛ والاكتشاف لا يسأل عن القطاع، لذا يسأل عنه `/ux-system create`. وفي Claude Code يتحقّق `/ux-system create` من الإصدار المثبّت ويشغّل البناء ويشرح التقرير.

**تصمّم نظام تصميم؟** تسعة أسس (اللون، الخط، المسافات، التخطيط، الاستدارة، الحدود، الارتفاع، الحركة، الصور)، يتغيّر كلّ منها تغيّرًا متّصلًا مع المحاور السبعة، مع قيم أوّلية وأدوار دلالية، بصيغة رموز التصميم من W3C (DTCG 2025.10) وبقيم كل وضع. المدخلات نفسها تعطي البايتات نفسها. وعبر MCP يعيد `ux_system_build` التقرير ونتيجة الفحص وحجم كل ملف، ويكتب الملفّات نفسها التي يكتبها الأمر حين يُعطى `out`.

- **بوّابة WCAG.** يُقاس كل زوج ألوان للنص وعناصر التحكم والتركيز في الوضعين الفاتح والداكن، وبالتباين العادي والعالي: WCAG 1.4.3 (النص 4.5:1) و1.4.11 (غير النصي 3:1) في التباين العادي، وWCAG 1.4.6 (النص 7:1) في التباين العالي، إضافة إلى حدّ أدنى خاصّ بنا قدره 4.5:1 في التباين العالي لمعظم الأجزاء غير النصية، لأنّ WCAG لا تحدّد مستوى معزّزًا للعناصر غير النصية. النظام الذي يخفق لا يُكتب، وتوضّح الرسالة ما يجب تغييره.
- **آمن افتراضيًا.** لا يكتب أبدًا فوق ملف مختلف. `--force` يستبدل الملفّات فقط حين تطلب ذلك.
- **العربية.** تحت `dir="rtl"` يتحوّل النص إلى خط عربي بمقاساته وارتفاع سطره الخاصّين؛ وتستخدم المسافات الخصائص المنطقية، وتنعكس الحركة. `--latin-only` يستبعد ذلك.

**نظام تملكه بالفعل.** يقرأ `/ux-system enhance --from` نظامك بأسمائه الأصلية (رموز DTCG، أو خصائص CSS المخصّصة، أو سمة Tailwind، أو ملفّات قواعد markdown، أو تصدير متغيّرات Figma)، ويفحصه عبر البوّابة نفسها، ويقيس ما يفعله كودك به فعلًا؛ دون إعادة كتابة أيّ شيء. ويضيف `/ux-system extend --from` أسسًا أو أدوارًا أو عقودًا دون تغيير أيّ رمز قائم، في ملف امتداد بجانبه، ويكتبه `uxskill system export` بصيغة tokens.css أو سمة Tailwind 4 أو متغيّرات Figma. ويضيف الإصدار 4.2 طبقة الثقة (فحص lint عند كل كتابة، ومراجِع للمسة الأخيرة) والإطلاق. راجع [سجلّ التغييرات](CHANGELOG.md).

**المكوّنات والأقسام.** تحدّد 23 عقدًا للمكوّنات الرموز التي يرتبط بها كل جزء من عنصر التحكم في كل حالة، وكيف تتحرّك كل حالة: تغيّر الحالة ينتقل وفق `motion.state`، والضغط يتحجّم وفق `motion.press.scale` (ويثبت عند تقليل الحركة)، وتنزلق التبويبات والقوائم وعناصر التحكم المقسّمة بمؤشّر واحد. وتسمّي 14 عقدًا للأقسام (الواجهة الرئيسية، الأسعار، الأسئلة الشائعة، التذييل وغيرها) وظيفة كل قسم، والمكوّنات التي تقبلها خاناته، والدليل الذي يحتاجه، وكيف يتراصّ على الهاتف. والصفحات المبنية منها تستخدم الصور الفوتوغرافية؛ أمّا مقتطفات الواجهة فصور إضافية، لا بديل عنها أبدًا.

**مُدقّق يقرأ الصفحة.** 171 قاعدة، كثير منها مع فحص على CSS والترميز بعد تحليلهما، تقرأ نظام الصفحة نفسها: تُوقَّت الحركة وفق منحناها، ويُلزَم ارتفاع سطر عناوين العرض بالحدّ الأدنى للمحرّك، ويجب أن يخرج عنصر التحكم المخفي من ترتيب التنقّل بالمفتاح Tab. ويفتح `uxskill lint --render` كل صفحة في Chromium دون واجهة بعرض سطح المكتب والهاتف ويشغّلها فعلًا: حلقات تركيز لا تظهر أو مقصوصة، وتمرير وضغط يستجيبان متأخّرين، وتركيز يضيع بعد Escape، وضغط ما زال يتحرّك عند تقليل الحركة.

**أوامر أقل.** صارت أوامر الشرطة المائلة الـ 25 الآن 18 أمرًا. يقبل `/ux-discover` الخيارين `--frame` و`--recommend`، ويقبل `/ux-design` الخيارات `--component` و`--dashboard` و`--from-image`، ويكرّر `/ux-polish` الفحص والإصلاح وإعادة الفحص حتى تبلغ النتيجة 90 أو تمرّ ثلاث جولات، ويقبل `/ux-init` الخيار `--stats`. وتبقى الأسماء القديمة السبعة صالحة كأسماء بديلة وتُزال في 4.1؛ راجع [الأسماء البديلة](#الأسماء-البديلة-تُزال-في-41).

**أدلّة لكل نوع من الواجهات.** قواعد صفحات الهبوط ولوحات التحكم والمكوّنات موجودة في `references/surfaces/`، لكلّ منها دليل واحد. يحمّل `/ux-design` دليلًا واحدًا بالضبط بحسب وضعه، فلا يقرأ بناء لوحة التحكم قواعد الواجهة الرئيسية أبدًا.

الاختبارات: **9764 ناجحًا**. دون اتصال. حتمي. لا يُستدعى أيّ LLM أبدًا.

### الجديد في الإصدار v3.1: وفيّ للعلامة، متجاوب، حيّ

- **الوفاء للعلامة إلزامي لا مرجوّ.** يُقرأ اللون الأساسي من بكسلات الشعار (لا من أكثر CSS طلاءً)؛ وتُرفض الخطوط الافتراضية إن لم توافق أسلوب حروف الشعار. وتنتقل العلامة المستخرجة `recommend` -> `synthesize`، و**حدّ أدنى صارم** في `evaluate` يُسقط أيّ ناتج يفقد لون العلامة أو شعارها أو لا يتضمّن صورًا حقيقية. تشغيل بيني في الاتجاهين مع اصطلاح `brand.md` المفتوح (عرض + استيراد).
- **الهاتف أوّلًا، ببوّابة.** أسس حِرفية جديدة (`responsive.md`، `component-behaviors.md`) وبوّابة تراعي التفاف الأسطر، تُخفق عند التمرير الأفقي، أو التفاف عنوان قائمة التنقّل أو الشعار النصّي أو زرّ، أو ترويسة لاصقة مفرطة الارتفاع.
- **طبقة الإبهار.** يستخلص المحرّك 2-3 لحظات مميّزة متناسقة في كل صفحة؛ وقد سقطت مقولة «الإبهار لا يأتي إلا من المستخدم».
- **مُدقّق أدقّ** (152 قاعدة): كشف الصور الإلزامية والعناصر التي تقتصر على أيقونة، وقواعد للرموز المؤقّتة و`100vw`؛ ويُبقى على picsum ذي البذرة ويُحذف العشوائي.

الملاحظات الكاملة في [CHANGELOG.md](CHANGELOG.md).

### الجديد في الإصدار v3

- **مواصفات العلامات التجارية أصبحت بيانات تدريب، لا قوالب.** لم تعد الـ160 مواصفة كتالوجًا يختار منه نظام التوصية، بل أصبحت مفردات يستخلص منها المُركِّب (synthesizer). الناتج جديد في كل استدعاء.
- **مُركِّب من 7 محاور** (warmth، contrast، density، geometry، formality، motion، type_personality). يُسقَط الـbrief حتميًا على قِيم محاور؛ وقِيم المحاور تُترجَم إلى رموز palette + خطوط + spacing + radius + motion جديدة.
- **ثلاثة أوضاع تشغيل تلقائي**: `strict_brand` (علامة واحدة بنسبة 100%)، `brand_anchor` (علامة واحدة بنسبة 70% + 30% مُكيَّفة بالمحاور من علامات شقيقة)، `pure_synthesis` (لا اسم علامة، استخلاص من 8 أمثلة موافقة في المحاور).
- **سجلّ القرارات يُعيد ترتيب نظام التوصية.** ‏`.ux/decisions.jsonl` يُعيد ترتيب المُرشَّحين وفق النصرات السابقة في الحاوية `(industry, ui_type)` نفسها. آمن مع الانطلاق البارد. لا يحتسب إلا القرارات بـ`lint_score >= 80` و`user_accepted = true`.
- **مصفوفة تفاعل المحاور**: حلٌّ صريح للنزاعات بين المحاور المتنافسة (dense + corporate → 4px، airy + corporate → 12px، soft + playful → 18px radius). لا قواعد ارتجالية صامتة بعد الآن.
- **حلقة تلقائية `/ux-evolve`** (في 4.0 هي الحلقة الافتراضية لـ `/ux-polish`): lint → polish → re-lint حتى تصل النتيجة إلى ≥ 90 أو إلى هضبة أو 3 جولات في 4.0 (5 في v3). حدّ الجودة عند 65.
- **3 أدوات MCP جديدة** (15 → 18): `ux_synthesize`، `ux_decisions_query`، `ux_decisions_stats`.
- **لوحة إحصاءات محلية**: `uxskill stats --html` تكتب `.ux/stats.html` تُظهر ما تعلّمه تنصيبك أنت. لا قياسات عن بُعد، ولا جمع عالمي.
- **اجتياز 223 اختبارًا.** بلا اتصال. حتمي. لا استدعاء لأي LLM.

التفاصيل الكاملة في [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain).

### تاريخ النجوم

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ما هو ux-skill

ux-skill هو **محرّك ذكاء تصميم** مخصّص لأدوات البرمجة المعتمدة على الذكاء الاصطناعي. يعمل كحزمة Python (`pip install uxskill`)، وكإضافة لـ Claude Code، وكمثبّت متعدّد يدعم 17 بيئة تطوير. يتلقّى المحرّك موجزًا للمشروع (القطاع، الجمهور، النغمة، المتطلّبات الإلزامية، الممنوعات، المنظومة التقنية، المنطقة)، ويُعيد نظام تصميم متكاملًا موصى به: أسلوب، لوحة ألوان، اقتران طباعي، مهيّآت حركة، مكوّنات، علامات تجارية يُحتذى بها، إلى جانب حواجز الأنماط الضارّة الواجب التزامها. والتوصية حتمية، المُدخل نفسه يُنتج المُخرج نفسه دائمًا.

تجلس هذه الإضافة بينك وبين أداة الذكاء الاصطناعي. حين تطلب من Claude Code أو Cursor أو أيّ مساعد ذكي «أنشئ صفحة هبوط لتطبيق تقنيات مالية»، فإنّ المساعد عادةً ما يرتجل، وتأتي النتيجة مفضوحة كناتج ذكاء اصطناعي خلال خمس ثوانٍ (تدرّجات بنفسجية إلى زرقاء، ثلاث بطاقات متساوية، خط Inter بحجم العرض، «John Doe» في الشهادات، انتقالات افتراضية مدّتها 300ms، واجهة رئيسية في المنتصف، أسهم CTA تقفز). يستبدل ux-skill الارتجال بـ**قيود منظّمة**: تشغّل `/ux-discover` لالتقاط الموجز واختيار النظام، و`/ux-design` لتوليد الكود، و`/ux-lint` للتحقّق قبل الالتزام من أنّه يجتاز قواعد مكافحة ركاكة الذكاء الاصطناعي الحتمية الـ 171.

هذا الملف هو المرجع المُعتمد. كلّ أمر، كلّ وكيل فرعي، كلّ ملفّ بيانات، كلّ مسار تثبيت، كلّ مواصفة علامة تجارية، كلّ تصنيف للأنماط الضارّة، كلّها موثّقة هنا. إن كنت تختار إضافة تصميم لـ Claude Code، أو تُقارن أدوات التصميم الذكي لـ Cursor أو Windsurf أو Codex، فاقرأ هذا الملف من أوّله إلى آخره مع صفحة [compare.html](https://uxskill.laithjunaidy.com/compare.html) جنبًا إلى جنب.

---

## فهرس المحتويات

1. [الدماغ، ما هو الإصدار v3.0](#الدماغ-ما-هو-الإصدار-v30)
2. [التثبيت السريع](#التثبيت-السريع)
3. [الأرقام، مقارنة حيّة مع أفضل 8 مهارات UX لـ Claude](#الأرقام-مقارنة-حيّة-مع-أفضل-8-مهارات-ux-لـ-claude)
4. [البنية، كيف تتشابك القطع](#البنية-كيف-تتشابك-القطع)
5. [أوامر الشرطة المائلة الـ 18، مرجع تفصيلي](#أوامر-الشرطة-المائلة-الـ-18-مرجع-تفصيلي)
6. [الوكلاء الفرعيون الخمسة](#الوكلاء-الفرعيّون-الخمسة)
7. [ملفّات البيانات الـ 11](#ملفّات-البيانات-الـ-11)
8. [قواعد مكافحة ركاكة الذكاء الاصطناعي الـ 171، المُدقّق](#قواعد-مكافحة-ركاكة-الذكاء-الاصطناعي-الـ-171-المُدقّق)
9. [مواصفات DESIGN.md الـ 160 للعلامات، حسب الفئة](#مواصفات-designmd-الـ-160-للعلامات-حسب-الفئة)
10. [خادم MCP، التحرّك غير المتماثل](#خادم-mcp-التحرّك-غير-المتماثل)
11. [مثبّت 17 بيئة تطوير](#مثبّت-17-بيئة-تطوير)
12. [حالات استخدام، سيناريوهات ملموسة](#حالات-استخدام-سيناريوهات-ملموسة)
13. [المقارنة مع البدائل](#المقارنة-مع-البدائل)
14. [خارطة الطريق](#خارطة-الطريق)
15. [المساهمة](#المساهمة)
16. [الترخيص، المؤلّف، الشكر](#الترخيص-المؤلّف-الشكر)

---

## الدماغ: ما هو الإصدار v3.0

الإصدار v3.1.0 هو أكبر تحوّل معماري في تاريخ ux-skill. لم يعد نظام التوصية يختار قوالب من كتالوج، بل يُركِّب المحرّك لغةً تصميميةً جديدةً لكل brief. الـbrief نفسه يُنتج النتيجة نفسها دائمًا (حتمي تمامًا)، لكن كل brief مختلف يحصل على نظامه الجديد الخاص. لم تعد مواصفات العلامات قوالب؛ صارت بيانات تدريب يتعلّم المحرّك منها المفردات. للنظام عينٌ على تاريخه، ويُغلق حلقة التغذية الراجعة محليًا، ولا يستدعي LLM أبدًا.

المُجَمِّع هو **مُركِّب حتمي من 7 محاور**، warmth، contrast، density، geometry، formality، motion، type_personality. يُسقَط كل brief على قِيم محاور؛ وقِيم المحاور تُترجَم إلى رموز palette + خطوط + spacing + radius + motion جديدة. سلالم الطباعة المعيارية تختار نسبتها من contrast (1.200 quiet / 1.250 balanced / 1.333 loud). البَدئيّات الـ7 (stack / cluster / grid / sidebar / cover / frame / split) متجاوبة بحكم التركيب (`auto-fit minmax(min(N, 100%), 1fr)` + container queries). لا يمكن إصدار تخطيط مكسور لأنه ليس قابلًا للتمثيل.

هناك ثلاثة أوضاع تلقائية: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% من رموز Stripe، أسرع مسار)؛ و`brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 30% مُكيَّفة بالمحاور من 4 علامات شقيقة)؛ و`pure_synthesis` (لا اسم علامة → فضاء لا متناهٍ، استخلاص 8 أمثلة موافقة في المحاور إلى لغة تصميم جديدة). تُحَلّ النزاعات بين المحاور بواسطة **مصفوفة تفاعل محاور** موثَّقة، dense + corporate يُجَمَّع إلى 4px (تنتصر density، مدرسة Bloomberg)، airy + corporate إلى 12px (تنتصر formality، فخامة)، soft + playful إلى 18px radius، sharp + corporate إلى 2px. لا قواعد ارتجالية صامتة في التنفيذ.

**سجلّ القرارات** (`.ux/decisions.jsonl`، مخطّط `_v: 1` مُقفَل) يُغلق حلقة التغذية الراجعة. ويُعيد نظام التوصية الآن ترتيب المرشّحين وفق النجاحات السابقة في الحاوية `(industry, ui_type)` نفسها. آمن مع الانطلاق البارد: يتخطّى إعادة الترتيب إن قلّت القرارات السابقة عن 3. لا يحتسب إلا القرارات التي تحقّق `lint_score >= 80` و`user_accepted = true`. ويشغّل `/ux-polish` كذلك lint → polish → re-lint حتى تصل النتيجة إلى ≥ 90 أو إلى هضبة أو 3 جولات، مع حدّ جودة عند 65 يُرفض ما دونه من ناتج ما لم يُستخدم `--force`. والنتيجة: كل تثبيت يزداد ذكاءً من مدوّنته الخاصّة، وكل تشغيل قابل للتكرار بين الأجهزة، ويبقى المحرّك دون اتصال تمامًا.

---

## التثبيت السريع

ثلاثة مسارات للتثبيت. اختر ما يلائم بيئتك.

### المسار 1: متجر إضافات Claude Code (المعتمد)

إن كنت تعمل داخل Claude Code، فالتثبيت يتمّ عبر متجر الإضافات:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

يربط ذلك جميع أوامر الشرطة المائلة الـ 18 (ومعها 7 أسماء قديمة تبقى أسماءً بديلة حتى 4.1) والوكلاء الفرعيين الخمسة بجلستك في Claude Code. بعد التثبيت، شغّل `/ux-init` لإعداد دليل الحالة `.ux/` الخاصّ بالمشروع والتأكّد من أنّ محرّك Python يمكن الوصول إليه.

### المسار 2: pip (شامل)

إن كنت تعمل خارج Claude Code (في Cursor أو Windsurf أو سطر الأوامر أو CI)، ثبّت حزمة Python:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

الحزمة تُعرّض كلًّا من `ux` و`uxskill` كنقطتَي دخول لسطر الأوامر، وهما الملفّ التنفيذي نفسه.

### المسار 3: npx (دون الحاجة إلى إدارة Python يدويًا)

إذا لم ترغب في إدارة Python مباشرة، فإنّ غلاف npx يُقلع كلّ شيء عبر `pipx`:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### التحقّق من التثبيت

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

مجموع التعدادات الاثني عشر 1,262 مُدخلًا. إذا ظهر أيّ تعداد بقيمة 0، فهذا يعني أنّ ملفّ JSON المعنيّ مفقود؛ افتح بلاغًا على [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues).

---

## الأرقام: مقارنة حيّة مع أفضل 8 مهارات UX لـ Claude

تعدادات النجوم تمّ التحقّق منها آخر مرّة عبر `gh api` بتاريخ **2026-05-28**. ux-skill (Laith0003/ux-skill) هو الوافد الأحدث، نحن صغار في الانتشار، عميقون في البنية. والمقارنة أدناه صريحة: أين نخسر، وأين نربح.

| الإضافة | النجوم | البنية | أوامر الشرطة المائلة | مُدقّق آمن للـ CI | مواصفات العلامات | المكوّنات | مهيّآت الحركة | بيئات التطوير المدعومة |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV، مهارة واحدة | 1 | - |، | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 مهارة + معاينة | 19 | - |، | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + ذوق مدعوم بأبحاث | 1 | - |، | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | ملفّ SKILL.md واحد بحجم 62 KB + سكربتات | 1 | - |، | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | مكتبة مهارات موصولة بـ MCP | متعدّد | - |، | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | مهارة بجمالية واحدة | 1 | - |، | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | مهارة تصميم مضادّة للركاكة | 1 | - |، | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | مكوّنات MD3 + تدقيق | 1 | - | (MD3 فقط) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **محرّك Python + 12 ملفّ بيانات + 18 أمرًا + 5 وكلاء فرعيين + مُدقّق CI** | **18** | **171 قاعدة حتمية** | **160** | **148** | **57** | **17** |

### حيث نخسر

- **الانتشار.** لديهم مئات الآلاف من النجوم. ولدينا 14. ضع نجمة لنا، هذه أرخص طريقة للدعم.
- **التعرّف على العلامة.** ui-ux-pro-max و open-design سبقانا بمسافة تُقاس بأشهر، لا بأيّام.
- **صقل التسويق.** يملكون لقطات شاشة ومقاطع توضيحية وصفحات هبوط قابلة للاكتشاف. نحن نملك ملفّ README شاملًا وصفحة هبوط نحيلة.

### حيث نربح

- **مكتبة المكوّنات:** 148 مكوّنًا موثّقًا مع التشريح، والحالات، والـ tokens المستخدَمة، ومواصفات الحركة. لا تُصدر أيّ من الإضافات الثماني الأخرى ملفّ مكوّنات مُهيكلًا.
- **مهيّآت الحركة:** 57 مدخلًا جاهزًا لكلّ منظومة تقنية (Framer Motion، GSAP، CSS) مع بدائل لإيقاف الحركة. لا تُصدر إضافة منها ملفّ حركة.
- **مُدقّق الأنماط الضارّة:** 171 قاعدة حتمية، تعمل ضمن CI، وتنتهي بشيفرة عدم نجاح عند Critical/High. لا تُصدر أيّ إضافة أخرى مُدقّقًا حتميًا.
- **مواصفات العلامات:** 160 ملفّات DESIGN.md حقيقية (Apple، Stripe، Linear، Figma، Tesla، BMW، Notion، Spotify، Airbnb، Vercel، Supabase، Cursor، Raycast، Claude، و96 علامة أخرى). لا تُصدر إضافة منها مكتبة علامات.
- **دعم 17 بيئة تطوير:** المحرّك نفسه، وغراء مختلف لكلّ بيئة.
- **18 أمرًا من أوامر الشرطة المائلة:** اكتشاف، توليد (صفحات، مكوّنات، لوحات تحكّم، من صورة)، تدقيق، lint، حلقة صقل، حلقة إصلاح، دراسة حالة، ورشة، نسخ، حركة، إمكانية وصول، قائد عمليات، موصولة بالكامل.

الجدول الكامل المتوازي على [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## البنية: كيف تتشابك القطع

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

### كيف يعمل المحرّك فعليًّا

1. **المُدخل.** تقدّم موجزًا، إمّا تفاعليًّا عبر `/ux-discover` (10 حقول) أو غير تفاعليّ عبر خيارات تمرّرها إلى `ux recommend`.
2. **5 عمليات بحث متوازية.** يُجري المحرّك خمس عمليات بحث في آن واحد عبر ملفّات البيانات:
   - **القطاع → recommended_styles** (industries.json)
   - **الأسلوب → توافق لوحة الألوان + الخط + الحركة** (styles.json)
   - **النبرة × المتطلّبات الأساسية → مرشّح لوحات الألوان** (palettes.json)
   - **المنظومة التقنية → توافق المكوّنات + مهيّآت الحركة** (tech-stacks.json, motion-presets.json)
   - **المحظورات + المنطقة → الحواجز + قائمة مختصرة بالعلامات النموذجية** (anti-patterns.json, brands/)
3. **الدمج.** يرتّب دامج حتمي المرشّحين، ويحلّ التعارضات (مثلًا: الوضع الداكن الإلزامي يفرض وضع لوحة الألوان)، ويُخرج نظامًا موصى به واحدًا.
4. **المُخرج.** مستند JSON يضمّ الأسلوب المختار ولوحة الألوان والاقتران الطباعي وأفضل 5 مهيّآت حركة وأفضل 12 مكوّنًا وأفضل 5 علامات نموذجية، وجميع حواجز الأنماط الضارّة الـ 171 مفعّلة. مع كتلة تعليل تشرح كل اختيار.
5. **التوليد.** تستهلك الأوامر اللاحقة (`/ux-design` بأوضاعه: الصفحة والمكوّن ولوحة التحكم والصورة، و`/ux-system`) التوصيةَ لتوليد كود فعلي عبر الوكلاء الفرعيين.
6. **التحقّق.** يُعيد `/ux-lint` فحص الكود المولَّد وفق القواعد الـ 171. وينتهي بشيفرة عدم نجاح عند Critical/High داخل CI.

**إضافات الإصدار v3.** يعيد نظام التوصية الآن ترتيب المرشّحين من `engine/decisions/` باستخدام `.ux/decisions.jsonl` (لا يحتسب إلا القرارات التي تحقّق `lint_score >= 80` و`user_accepted = true`؛ آمن مع الانطلاق البارد إن قلّت القرارات السابقة عن 3). ويمكن لمسار التوليد أن يمرّ عبر `engine/synthesizer/`، وهو مُصرِّف حتمي بسبعة محاور يُنتج رموزًا جديدة للوحة الألوان + الخط + المسافات + الاستدارة + الحركة لكل موجز بدل انتقاء قوالب من كتالوج. التفاصيل في [الدماغ، ما هو الإصدار v3.0](#الدماغ-ما-هو-الإصدار-v30).

**Python يفكّر. HTML يعرض. Markdown يربط.**

---

## أوامر الشرطة المائلة الـ 18: مرجع تفصيلي

يأتي كل أمر ملفًّا بصيغة `.md` تحت `commands/` يتضمّن `description` و`allowed-tools` و`triggers` و`when to use` و`when to skip` و`input` و`process` و`output state file`. الأوصاف أدناه مختصرة، والمصدر الكامل هو المواصفة المعتمدة.

تنقسم الأوامر إلى سبع مجموعات: **الإقلاع والمخزون**، و**الاكتشاف والتوصية**، و**التوليد**، و**التدقيق والتحقّق**، و**الإصلاح والصقل**، و**الاكتشاف والسرد**، و**القائد**. وتبقى سبعة أسماء من 3.x صالحة [كأسماء بديلة](#الأسماء-البديلة-تُزال-في-41) حتى 4.1.

### الإقلاع والمخزون

#### `/ux-init`: إقلاع المشروع

- **ماذا:** يكتشف بيئة التطوير التي تستخدمها (`.claude/`، `.cursor/`، `.windsurf/`، إلخ)، ويُثبّت الناتج المناسب، ويتحقّق من إمكانية الوصول إلى محرّك Python، ويطبع لقطة إحصاءات. ويطبع `--stats` اللقطة وحدها: الإصدار + عدد المُدخلات في ملفّات البيانات.
- **متى يُستخدم:** عند أوّل تثبيت في مشروع جديد. بعد استنساخ مشروع يستخدم ux-skill. بعد `pip install --upgrade uxskill`. و`--stats` بعد التثبيت، أو بعد الترقية، أو حين تأتي التوصية باختيارات غريبة وتشكّ في أنّ ملفّات البيانات ناقصة.
- **متى يُتجاوز:** سبق أن شغّلته في هذا المشروع ولم يتغيّر شيء. أمّا `--stats` فلا حاجة لتجاوزه أبدًا: إنّه قراءة تستغرق 50ms.
- **الاستدعاء:** `/ux-init` (دون وسائط)، أو `/ux-init --stats`، أو `uxskill init` / `uxskill stats` من سطر الأوامر. يضيف `--decisions` ملخّص سجلّ القرارات، ويكتب `--html` الملف `.ux/stats.html`.
- **الإخراج:** ناتج خاصّ بكلّ بيئة (انظر [مثبّت 17 بيئة تطوير](#مثبّت-17-بيئة-تطوير)) + دليل `.ux/` + ملخّص يُطبع على الخرج القياسي. ومع `--stats`: JSON على الخرج القياسي (انظر [التحقّق من التثبيت](#التحقّق-من-التثبيت) أعلاه).
- **يربط بـ:** `/ux-discover` تاليًا. و`--stats` للتشخيص فقط.

#### `/ux-mcp`: تشغيل المحرّك خادمَ MCP

- **ماذا:** يشغّل المحرّك خادمًا لـ Model Context Protocol عبر stdio. وتصبح 25 أداة (نظام التوصية، والمُدقّق، والحفظ، والمُركِّب، وسجلّ القرارات، والاستخراج من الصور، وملفّات البيانات، وبناء نظام التصميم واستيراده وتحسينه وتوسيعه وتصديره وفحصه) قابلة للاستدعاء من أيّ مضيف يدعم MCP دون الإضافة.
- **متى يُستخدم:** تعمل في مضيف آخر يدعم MCP وتريد المحرّك نفسه. تشغّل خطّ عمل متعدّد الوكلاء يحتاج مصدرًا واحدًا لقيود التصميم. تريد نظام التوصية أو المُدقّق عمليةً طويلة الأمد داخل CI.
- **متى يُتجاوز:** أنت داخل Claude Code والإضافة مثبّتة؛ فأوامر الشرطة المائلة تصل إلى المحرّك أصلًا. تحتاج إجابة لمرّة واحدة؛ `uxskill recommend` أو `uxskill lint` أبسط.
- **الاستدعاء:** `/ux-mcp`، أو `ux-mcp` من الطرفية بعد `pip install 'uxskill[mcp]'`.
- **الإخراج:** خادم JSON-RPC عبر stdio. انظر [خادم MCP](#خادم-mcp-التحرّك-غير-المتماثل) و`commands/ux-mcp.md` لإعداد كل عميل.
- **يربط بـ:** لا شيء؛ إنّه وسيلة نقل لا خطوة.

### الاكتشاف والتوصية

#### `/ux-discover`: الدالّة الإلزامية (استخراج من 10 حقول، تأطير، توصية)

- **ماذا:** الاستخراج الإلزامي من 10 حقول الذي يمرّ به كل مشروع قبل أيّ أمر توليد. نوع المشروع، الجمهور، الهدف الأساسي، النبرة، المتطلّبات الأساسية، المحظورات، العلامات المرجعية، المنظومة التقنية، المنطقة، مقياس النجاح. **لا ارتجال.** العبارات المحظورة («حديث»، «نظيف») تُجبر المستخدم على التحديد. ثم يشغّل نظام التوصية: تُعيد عمليات البحث المتوازية الخمس لمحرّك Python عبر 12 ملفّ بيانات نظام تصميم واحدًا مدمجًا (القطاع → الأسلوب → لوحة الألوان → الخط → الحركة + المكوّنات + العلامات النموذجية + الحواجز).
- **الأوضاع:** يلتقط `--frame` لمن هو المنتج والنتيجة والفرضية وإشارة النجاح في كتلة تأطير من أربعة حقول، أخفّ من الاستخراج الكامل. ويشغّل `--recommend` نظام التوصية وحده، من موجز محفوظ أو من خيارات لمرّة واحدة.
- **متى يُستخدم:** قبل أيّ `/ux-design` أو `/ux-system`. كلّما تقادم موجز سابق. و`--frame` في بداية مشروع أو دورة عمل أو مهمّة منفردة، أو في منتصف الطريق حين ينحرف الحديث. و`--recommend` عند إعادة توجيه منتج يبدو منهكًا.
- **متى يُتجاوز:** تُصلح علّة (`/ux-fix`). تشغّل تمريرة مُدقّق فقط (`/ux-lint`). الموجز لم يتغيّر منذ الجلسة السابقة.
- **الاستدعاء (Claude Code):** `/ux-discover`، أو `/ux-discover --frame "loyalty wallet for a MENA retail pilot"`، أو `/ux-discover --recommend`.
  **الاستدعاء (سطر الأوامر):**
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
- **الإخراج:** `.ux/last-discovery.json` (موجز الحقول الـ 10)، و`.ux/last-recommendation.json` (الأسلوب المختار، لوحة الألوان، الاقتران الطباعي، أفضل 5 مهيّآت حركة، أفضل 12 مكوّنًا، أفضل 5 علامات نموذجية، جميع حواجز الأنماط الضارّة الـ 171 مفعّلة، مع التعليل)، ومع `--frame` الملف `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`).
- **يربط بـ:** `/ux-design [extra brief]` → كود أمامي مبنيّ على التوصية. `/ux-design --component <name>` → مكوّن واحد متّسق مع القيود المكتشفة. `/ux-system` → نظام تصميم كامل من التوصية. `/ux-lint` → التحقّق من الكود المولَّد.

### التوليد

#### `/ux-design`: توليد سطح جميل ومضادّ للركاكة من موجز

- **ماذا:** يُولّد ناتجًا أماميًّا كاملًا بمستوى إنتاج (صفحة هبوط، موقع تسويقي، هيكل تطبيق) من موجز الاكتشاف + التوصية. يستدعي `frontend-engineer` بتوجيه إبداعي من مراجع مضادّة للركاكة ومن «الترسانة». ويختار الموجز، أو أحد الخيارات، وضعًا من أربعة:
  - **الصفحة** (افتراضي): صفحة كاملة أو واجهة متعدّدة الأقسام. يكتب `.ux/last-design.json`.
  - **`--component [name]`**: مكوّن واحد بمستوى إنتاج (زرّ، نافذة منبثقة، شريط تنقّل، شريط جانبي، بطاقة، جدول، نموذج، رسم بياني). بحالات التفاعل الأربع كلّها، قابل للوصول، وفيّ للعلامة. يبحث عن المكوّن في `.ux/last-recommendation.json` أوّلًا، ثم يستعلم ملفّ البيانات مباشرة. يكتب `.ux/last-component.json`.
  - **`--dashboard`**: انضباط في كثافة البيانات، تخطيط bento، أرقام جدولية بعرض ثابت، أنماط sparkline، تجنّب الإفراط في البطاقات، ألوان حالة دلالية، حركة مقتصدة. ليس موقعًا تسويقيًّا أُلصقت عليه رسوم بيانية. يكتب `.ux/last-dashboard.json`.
  - **`--from-image <path>`**: يقرأ صورة مرجعية للتصميم (PNG/JPG/WebP) برؤية حاسوبية خالصة عبر Pillow (اللوحة الغالبة، قطبية الخلفية، إشارة الخط)، ويطابقها مع ملفّات لوحات الألوان والأساليب، ثم يبني من التوصية الناتجة. ويتوقّف `--extract-only` بعد الاستخراج. يكتب `.ux/last-image-extract.json`.
- **متى يُستخدم:** «صمّم»، «ابنِ لي»، «أنشئ صفحة هبوط»، «اصنع لوحة تحكّم»، «اصنع مكوّنًا»، «ابنِ زرًّا»، «صمّم لوحة الإدارة»، «لوحة المشغّل»، «لوحة مؤشّرات الأداء»، «ابنِه مثل لقطة الشاشة هذه»، أيّ طلب تسليم بصري حرّ الصياغة.
- **متى يُتجاوز:** تريد مراجعة لا بناء (استخدم `/ux-audit` أو `/ux-critique`). عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`، `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`، `/ux-design --dashboard`، `/ux-design --from-image ref.png`.
- **الإخراج:** الكود المولَّد (HTML / Blade / JSX / Vue / Astro)، إضافة إلى ملف الحالة الخاصّ بالوضع.
- **يربط بـ:** `/ux-lint` → التحقّق من الحواجز. `/ux-polish` → صقل تجميلي. `/ux-a11y` → تدقيق إمكانية الوصول. `/ux-copy` → مراجعة النصوص الدقيقة. `/ux-fix` → تطبيق الملاحظات كالتزامات ذرّيّة.

#### `/ux-system`: توليد نظام تصميم انطلاقي كامل

- **ماذا:** يقترح نظام تصميم انطلاقي كامل لمشروع لا يملك واحدًا، tokens (لون، خطّ، فراغ، حركة، نصف قطر، ظلّ)، وثائق أُسس، عقود مكوّنات، إقران الوضع الداكن، مُبدِّل للسمات. يستدعي `design-system-architect`.
- **متى يُستخدم:** «لا نملك نظام تصميم»، «ابنِ لنا نظامًا»، «اقترح tokens»، «ماذا يجب أن تكون سِمتنا»، «أنشئ نظام التصميم».
- **متى يُتجاوز:** المشروع يملك بالفعل نظام تصميم؛ استخدم `/ux-design --component` على النظام القائم بدلًا من ذلك. عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-system create` (محرّك الأسس)، `/ux-system enhance --from <file>` (قياس نظام تملكه بالفعل)، `/ux-system extend --from <file> --add <foundation>` (الإضافة إليه دون تغييره)، أو `/ux-system` (مسار 3.x؛ يُشغّل الاكتشاف أوّلًا إن لم يكن قد سُجّل).
- **الإخراج:** `tokens.json`، `foundations.md`، عقود `components/*.md`، إمكانية إصدار اختياري لـ Tailwind / vanilla / SCSS. يكتب `.ux/last-system.json` لربط السياق.
- **يربط بـ:** `/ux-design --component` → البناء على النظام الجديد. `/ux-design` → توليد واجهة بالرموز الجديدة.

#### `/ux-motion`: معالجة الحركة

- **ماذا:** يُولّد طبقة الحركة لسطح ما، مدد، منحنيات تليين، تصميم تتابعي، بدائل لإيقاف الحركة، انضباط أداء. ويُدقّق أيضًا الحركة القائمة وفق خمسة أبعاد (التوقيت، التليين، المعنى، إيقاف الحركة، الأداء).
- **متى يُستخدم:** «تحقّق من الحركة»، «هل الرسوم جيّدة»، «أصلح الحركة»، «راجع الرسوم»، «تدقيق حركة»، «جولة أداء على الحركة».
- **متى يُتجاوز:** السطح لا يحوي حركة (استخدم `/ux-audit` أو `/ux-polish`). عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-motion path/to/component.tsx` (وضع تدقيق) أو `/ux-motion --generate hero-entry` (وضع توليد).
- **الإخراج:** كود مُحدَّث (في وضع التوليد) أو تقرير `.ux/last-motion.json` (في وضع التدقيق).
- **يربط بـ:** `/ux-fix` → تطبيق ملاحظات الحركة. `/ux-polish` → الإحكام.

### التدقيق والتحقّق

#### `/ux-lint`: مُدقّق حتمي بقواعد regex (بلا LLM، آمن في CI)

- **ماذا:** يشغّل 171 قاعدة على كودك. بلا أيّ استدعاء لنموذج لغوي. ينتهي بشيفرة عدم نجاح عند Critical / High داخل CI. المصدر: `data/anti-patterns.json`. القواعد تُغطّي إمكانية الوصول (45)، المحتوى (35)، التخطيط (18)، الخطوط (16)، الحركة (14)، المرئي (14)، الجودة (12)، الألوان (10)، الأداء (5)، العمق (2).
- **متى يُستخدم:** خطّاف ما قبل الالتزام. بوّابة CI. تمريرة أولى سريعة على قاعدة كود كبيرة قبل دفع كلفة `/ux-audit`. بعد `/ux-design` بأيّ وضع للتحقّق من التوليد.
- **متى يُتجاوز:** تريد حلقة إصلاح (المُدقّق يُبلّغ ولا يُحرّر، اربطه بـ `/ux-polish --fix` أو `/ux-fix`). تريد حكمًا ذوقيًّا (استخدم `/ux-critique`).
- **الاستدعاء (أمر الشرطة المائلة):** `/ux-lint src/`.
- **الاستدعاء (سطر الأوامر):** `uxskill lint .` أو `python3 bin/ux-lint.py .` أو `bash bin/ux-lint.sh --ci --fail-on high`.
- **الاستدعاء (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **الإخراج:** ملاحظات على الخرج القياسي (الموقع، معرّف القاعدة، الخطورة، الدليل). شيفرة الخروج 0 إذا كان نظيفًا، وعدم نجاح عند Critical/High حين يُضبط `--fail-on high`.
- **يربط بـ:** `/ux-polish --fix` → نظير قائم على نموذج لغوي يطبّق نفس الأنماط. `/ux-fix` → تطبيق الملاحظات كالتزامات مرتّبة بالخطورة. `/ux-audit` → جولة استدلال كاملة بست عدسات. `/ux-next` → اترك القائد ليُقرّر.

#### `/ux-audit`: تدقيق تصميمي بست عدسات

- **ماذا:** مراجعة مُنظَّمة ذات وجهة نظر مقابل ستّ عدسات (الوضوح، التراتب، إمكانية الوصول، الصوت، الحركة، الذوق)، تُنتج ملاحظات موسومة بالخطورة. تقرير على طريقة Polaris. يقرأ `.ux/last-frame.json` أوّلًا، الجمهور والنتيجة يُحدّدان خطورة كلّ ملاحظة.
- **متى يُستخدم:** السطح موجود وتريد نقدًا قابلًا للدفاع عنه. «دقّق»، «راجع تجربة المستخدم»، «هل هذا جيّد»، «ما المعطوب»، «فكّك هذا».
- **متى يُتجاوز:** السطح غير موجود بعد (استخدم `/ux-design`). يريد المستخدم عدسة واحدة (استخدم الأمر المختصّ: `/ux-a11y`، `/ux-copy`، `/ux-motion`، `/ux-polish`). يريد المستخدم رأيًا ذوقيًّا (استخدم `/ux-critique`). عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-audit https://example.com/pricing` أو `/ux-audit src/components/Pricing.tsx`.
- **الإخراج:** يكتب `.ux/last-audit.json`، مصفوفة `findings` تحوي `{lens, severity, title, principle, evidence, fix}`، و`severity_counts`، و`dominant_lens`، و`strategic_moves`.
- **يربط بـ:** `/ux-fix` → تطبيق الملاحظات. `/ux-polish` → جولة صقل. `/ux-design` → إن لزمت إعادة تصميم بنيوية.

#### `/ux-a11y`: تدقيق WCAG 2.1 AA + لمسات اللياقة العامّة

- **ماذا:** تدقيق مُنظَّم لـ WCAG 2.1 AA، إضافة إلى لمسات اللياقة التي تنجح في الأدوات المؤتمتة لكنّها تُؤذي المستخدمين الحقيقيين (وضوح التركيز، تخصيص الأخطاء، تفضيلات الحركة، فخاخ لوحة المفاتيح، الاعتماد على اللون).
- **متى يُستخدم:** بوّابة إمكانية الوصول قبل الإطلاق. بعد إعادة التصميم. «تحقّق من إمكانية الوصول»، «تدقيق WCAG»، «هل هذا متاح»، «مراجعة a11y»، «اختبار قارئ شاشة»، «فحص التنقّل بلوحة المفاتيح».
- **متى يُتجاوز:** ليس وجهًا للمستخدم. عمل خلفي أو بنية تحتية. مسوّدات قيد العمل.
- **الاستدعاء:** `/ux-a11y https://example.com` (يُفضَّل رابط حيّ، الأدوات المؤتمتة واختبار لوحة المفاتيح لا يعملان إلّا حيًّا).
- **الإخراج:** يكتب `.ux/last-a11y.json`، مصفوفة `findings` تحوي `{wcag_sc, sc_name, severity, title, evidence, fix, category}`، ومصفوفة `beyond_wcag`، و`severity_counts`.
- **يربط بـ:** `/ux-fix` → تطبيق الملاحظات كالتزامات. `/ux-copy` → إصلاح النصوص البديلة وأخطاء النماذج في إطار جولة نسخ.

#### `/ux-critique`: حكم ذوقي (3 إيجابيات، 3 سلبيات، خطوة استراتيجية واحدة)

- **ماذا:** رأي مصمّم، ليس تدقيقًا مُنظَّمًا ولا درجة خطورة، بل وجهة نظر محكمة وصريحة تُسمّي ما يعمل وما لا يعمل، وتُحدّد الخطوة الاستراتيجية الوحيدة التي ستُحدث أكبر فارق.
- **متى يُستخدم:** «ما رأيك»، «هل هذا جيّد»، «انقد هذا»، «رأي صريح»، «هل المزاج صحيح»، «هل يشبهنا»، «هل نطلق هذا».
- **متى يُتجاوز:** المستخدم يطلب صراحة تدقيقًا مُنظَّمًا (استخدم `/ux-audit`). عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-critique https://example.com`.
- **الإخراج:** يكتب `.ux/last-critique.json`، 3 إيجابيات، 3 سلبيات، خطوة استراتيجية واحدة، إلى جانب نصّ.
- **يربط بـ:** `/ux-design` إذا أوصى الحكم بإعادة تصميم. `/ux-polish` إذا أوصى بالإحكام.

#### `/ux-copy`: مراجعة + إعادة كتابة النصوص الدقيقة

- **ماذا:** يُقيّم كلّ نصّ ظاهر وفق معايير الصوت ويُنتج إعادة كتابة قبل/بعد. يلتقط: «النموذج يحوي أخطاء» (عامّ)، «John Doe» (نائب)، نصوص الذكاء الاصطناعي الاحتفاليّة المرحة، أزرار CTA عامّة، حالات فارغة ميّتة، أخطاء بلا فائدة.
- **متى يُستخدم:** البنية صحيحة لكنّ الكلمات ضعيفة. «راجع النسخة»، «أصلح النصوص الدقيقة»، «رسائل الخطأ سيّئة»، «أعد كتابة هذا»، «أحكِم النصوص»، «أزرار الدعوة تبدو عامّة»، «هذه الحالة الفارغة ميّتة».
- **متى يُتجاوز:** مشكلات تخطيط (استخدم `/ux-audit` أو `/ux-polish`). مشكلات نسخ مرتبطة بإمكانية الوصول كالنصوص البديلة (استخدم `/ux-a11y`). عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-copy src/views/checkout.blade.php`.
- **الإخراج:** يكتب `.ux/last-copy.json`، مصفوفة `strings` تحوي `{location, severity, before, after, notes}`، إضافة إلى معايير ولغات تحتاج ترجمة.
- **يربط بـ:** `/ux-fix` → تطبيق إعادات الكتابة. `/ux-a11y` → إعادة الفحص بعد إصلاحات النسخ.

### الإصلاح والصقل

#### `/ux-fix`: تطبيق الملاحظات بصورة التزامات ذرّيّة

- **ماذا:** يقرأ آخر تقرير من `.ux/` (audit، copy، a11y، motion، أو polish)، ويتحقّق من شجرة العمل، ثم يُطبّق الملاحظات كالتزامات ذرّيّة عبر الوكلاء الفرعيين المناسبين. يُعيد التحقّق بإعادة تشغيل الأمر الأصلي.
- **متى يُستخدم:** بعد تشغيل أمر من فئة التدقيق ومراجعة الملاحظات. «أصلح الملاحظات»، «طبّق الإصلاحات»، «شغّل حلقة الإصلاح»، «رقّع السطح»، «أجرِ التعديلات»، «اذهب وأصلحها».
- **متى يُتجاوز:** لا تقرير سابق في `.ux/`. شجرة العمل مُتّسخة ولم يوافق المستخدم على stash/commit. الإصلاحات تتطلّب حكمًا تصميميًّا لا تطبيقًا ميكانيكيًّا (استخدم `/ux-design` لإعادة التصميم).
- **الاستدعاء:** `/ux-fix` (يكتشف أيّ تقرير يجب إصلاحه تلقائيًّا) أو `/ux-fix --from=last-a11y.json`.
- **الإخراج:** التزامات ذرّيّة لكلّ ملاحظة. يُعيد تشغيل الأمر الأصلي ويُحدّث ملفّ `.ux/last-*.json`. ويطبع ملخّصًا.
- **يربط بـ:** `/ux-next` → يختار القائد الخطوة التالية.

#### `/ux-polish`: حلقة فحص وإصلاح وإعادة فحص + القضاء على ركاكة الذكاء الاصطناعي

- **ماذا:** أوّلًا حلقة حتمية على ملف HTML محلّي: فحص lint، ثم ست تمريرات صقل متساوية الأثر، ثم إعادة الفحص، حتى تبلغ النتيجة 90 أو تثبت أو تمرّ ثلاث جولات (`--rounds` يغيّر السقف). افتراضيًا يبقى ناتج الحلقة في `<file>.evolved.html` ولا يُمسّ الأصل أبدًا. ولا يستبدل الأصلَ إلا `--loop-only` أو `--fix`، بعد التحقّق من نظافة شجرة العمل، ويمنع حدّ الجودة عند 65 أيّ نتيجة راسبة من استبداله ما لم يُستخدم `--force`؛ ومع `--brand-file` يصمد الحدّ الأدنى للوفاء بالعلامة عند كل مخرج. ثم تمريرة الذوق: إيقاع المسافات، شحذ التسلسل البصري، كشف ركاكة الذكاء الاصطناعي، اتّساق الرموز. هو النظير المعتمد على النماذج اللغوية لـ `/ux-lint`، ويعتمد على حكمك في مسائل الذوق. يشغّل `--loop-only` الحلقة وحدها، و`--no-loop` تمريرة الذوق وحدها، ويطبّق `--fix` ملاحظات الذوق.
- **متى يُستخدم:** البنية صحيحة لكن التنفيذ مرتخٍ. «اصقله»، «شدّ هذا»، «أزِل ركاكة الذكاء الاصطناعي»، «اجعله فاخرًا»، «اجعله أقلّ شبهًا بالذكاء الاصطناعي»، «المسافات غير مريحة»، «يبدو عاديًّا»، «يحتاج ذوقًا أكثر»، «حسّنه حتى تتجاوز النتيجة 90»، «اجعله جاهزًا للإطلاق».
- **متى يُتجاوز:** الواجهة تفتقد وظائف أساسية (أصلِحها أوّلًا). تحتاج إعادة تصميم لا صقلًا (استخدم `/ux-design`). مشكلات النصوص (استخدم `/ux-copy`). مشكلات الحركة (استخدم `/ux-motion`). مشكلات إمكانية الوصول (استخدم `/ux-a11y`).
- **الاستدعاء:** `/ux-polish src/components/Hero.tsx`، `/ux-polish out/landing.html --css out/landing.css`، `/ux-polish out/landing.html --loop-only --rounds 5`.
- **الإخراج:** `<file>.evolved.html` من الحلقة (يحلّ محلّ الأصل فقط مع `--loop-only` أو `--fix`)، وكود محدَّث مع `--fix`، و`.ux/last-evolve.json`، وسطر واحد في `.ux/decisions.jsonl`، و`.ux/last-polish.json` الذي يصف ملاحظات الذوق.
- **يربط بـ:** `/ux-lint` → التحقّق من أنّ الصقل صمد. `/ux-a11y` → إعادة فحص إمكانية الوصول.

### الاكتشاف والسرد

#### `/ux-research`: تخطيط بحث + توليف

- **ماذا:** وضع التخطيط: يكتب نصوص مقابلات، استبيانات، فلاتر تجنيد. وضع التوليف (`--synthesize`): يهضم المقابلات والتحليلات ومواقع المنافسين ونتائج A/B وتذاكر الدعم في توصيات. يستدعي `research-synthesizer`.
- **متى يُستخدم:** «خطّط لدراسة بحثيّة»، «أحتاج أسئلة مقابلات»، «صمّم استبيانًا»، «كيف أُجنّد مستخدمين»، «خطّة اختبار مستخدمين»، «دراسة يوميّات»، «اختبار تفضيل»، «fake door»، «smoke test»، «وَلِّف ملاحظات مقابلاتي».
- **متى يُتجاوز:** الجواب معروف بثقة عالية. قرارات قابلة للتراجع بمخاطر منخفضة. عمل خلفي أو بنية تحتية.
- **الاستدعاء:** `/ux-research --plan "loyalty wallet adoption in MENA"` أو `/ux-research --synthesize interviews/*.md`.
- **الإخراج:** يكتب `.ux/last-research.json`، خطّة بحث، أو موضوعات مولَّفة + أدلّة + توصيات.
- **يربط بـ:** `/ux-discover --frame` → دمج النتائج في إطار. `/ux-design` → التوليد من النتائج. `/ux-workshop` → إدارة ورشة بالاعتماد على البحث مُدخلًا.

#### `/ux-workshop`: ورشة تفكير تصميمي من 5 مراحل

- **ماذا:** يُيسّر ورشة اكتشاف / تفكير تصميمي من البداية للنهاية. خمس مراحل متتابعة (استكشاف → خريطة حرارة → خريطة أصحاب مصلحة → رسم حلّ → خطّة لعب). محسوبة بالوقت. مخرجات ملموسة لكلّ مرحلة. تنتهي بقرار، لا بـ«ملاحظات مثيرة للاهتمام».
- **متى يُستخدم:** سؤال حقيقي، مشاركون حقيقيّون، ميزانية وقت حقيقيّة. «أَدِر ورشة»، «يَسِّر اكتشافًا»، «هيا نُجرِ جلسة تفكير تصميمي»، «لديّ أصحاب مصلحة لساعة، ماذا نفعل»، «ابدأ المشروع».
- **متى يُتجاوز:** الموجز واضح ومحدَّد النطاق أصلًا. عصف ذهني فردي (استخدم `/ux-design` أو `/ux-discover --frame`). الفريق في منتصف التنفيذ لا في مرحلة الاكتشاف.
- **الاستدعاء:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`.
- **الإخراج:** يكتب `.ux/last-workshop.json`، خطّة اللعب + مخرجات كلّ مرحلة.
- **يربط بـ:** `/ux-design` → تنفيذ خطّة اللعب. `/ux-research` → سدّ الفجوات التي كشفتها الورشة. `/ux-case-study` → نشر الرحلة.

#### `/ux-case-study`: دراسة حالة قابلة للنشر (شكل تحريري على طريقة Wfrah)

- **ماذا:** يُولّد دراسة حالة للمشروع بصيغة تحريرية أحادية اللون خالصة، بخطوط Wfrah، وفواصل رفيعة، ورموز أقسام مرقّمة من (A) إلى (G)، وتخطيط آمن للمحتوى ثنائي اللغة. مستند لا كتيّب تسويقي. يقرأ من `.ux/last-frame.json` و`.ux/last-workshop.json` و`.ux/last-research.json` و`.ux/last-design.json` و`.ux/last-a11y.json` و`.ux/last-polish.json` و`.ux/last-recommendation.json` و`.ux/last-discovery.json`.
- **متى يُستخدم:** بعد الإطلاق. بعد محطّة مستقلّة. «اكتب دراسة حالة»، «اعمل دراسة حالة على هذا المشروع»، «أنجز وثيقة التغليف»، «انشر هذا العمل»، «قطعة بورتفوليو».
- **متى يُتجاوز:** المشروع يفتقر إلى البيانات اللازمة لملء الأقسام من (A) إلى (G). المستخدم يريد صفحة هبوط تسويقية لا دراسة حالة (استخدم `/ux-design`).
- **الاستدعاء:** `/ux-case-study --format=html --slug=bashiti-loyalty`.
- **الإخراج:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`.
- **يربط بـ:** أمر طرفي، عادةً نهاية المشروع.

### القائد

#### `/ux-next`: قائد سير العمل (قراءة فقط)

- **ماذا:** يقرأ كلّ `.ux/last-*.json` ويُسمّي الأمر التالي الأعلى رافعةً. قائد، لا بنّاء. قراءة فقط.
- **متى يُستخدم:** بين الأوامر. «ماذا أفعل تاليًا»، «ما الخطوة التالية»، «قرّر عنّي»، «إلى أين من هنا».
- **متى يُتجاوز:** لا تقارير سابقة في `.ux/`. تعرف الأمر التالي تحديدًا.
- **الاستدعاء:** `/ux-next` (دون وسائط) أو `/ux-next --focus=a11y`.
- **الإخراج:** خرج قياسي، الأمر التالي الموصى به + المبرّر.
- **يربط بـ:** أيًّا كان الأمر الذي اختاره.

#### `/ux-expert`: صلة استشارية

- **ماذا:** يُظهر معلومات التواصل مع مُنشئ الإضافة حين يطلب المستخدم خبيرًا حقيقيًّا في تجربة المستخدم. وجيز، مباشر، بلا تسويق.
- **متى يُستخدم:** «من بنى هذا»، «أحتاج خبير تجربة مستخدم»، «هل تُقدّم استشارات»، «هل يمكنني توظيف شخص لهذا»، «هل ثمّة إنسان خلف هذه الإضافة».
- **متى يُتجاوز:** المستخدم يسأل عن خصائص الإضافة لا عن الاستشارات.
- **الاستدعاء:** `/ux-expert`.
- **الإخراج:** بطاقة تواصل وجيزة فيها LinkedIn / البريد / المستودع.

### الأسماء البديلة، تُزال في 4.1

دُمجت سبعة أوامر من 3.x في الأوامر الـ 18 أعلاه. وتبقى أسماؤها صالحة لإصدار واحد: يذكر كل اسم بديل المكان الذي انتقل إليه، ثم يشغّل الأمر الجديد بالوسائط نفسها.

| الأمر القديم | الآن | ملاحظات |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | كتلة التأطير نفسها، و`.ux/last-frame.json` نفسه |
| `/ux-recommend` | `/ux-discover --recommend` | أداة MCP `ux_recommend` لم تتغيّر |
| `/ux-stats` | `/ux-init --stats` | لقطة للقراءة فقط |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | يحتفظ الاسم البديل بالسقف القديم البالغ خمس جولات؛ و`/ux-polish` وحده يتوقّف عند ثلاث |
| `/ux-component` | `/ux-design --component` | `.ux/last-component.json` نفسه |
| `/ux-dashboard` | `/ux-design --dashboard` | `.ux/last-dashboard.json` نفسه |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | احذف `--extract-only` للبناء من الصورة |

### مخطّط ربط الأوامر

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

## الوكلاء الفرعيّون الخمسة

الوكلاء الفرعيّون مولّدات متخصّصة بحسب الدور تستدعيها الأوامر. لا يعملون مستقلّين أبدًا، بل تستدعيهم `/ux-design` و`/ux-system` و`/ux-fix` و`/ux-research`، إلخ. لكلّ وكيل حدود مسؤولية محدّدة: لا يُقرّر الموجز، بل يُنفّذه.

### `frontend-engineer`

- **يملك:** كود واجهة أماميّة بمستوى إنتاج (React، Next.js، Vue، Blade+Alpine، HTML نقي، Astro) بانضباط مضادّ لركاكة الذكاء الاصطناعي.
- **يستدعيه:** `/ux-design` (أوضاع الصفحة والمكوّن ولوحة التحكم والصورة)، `/ux-fix`.
- **مُدخلاته:** موجز + توجيه إبداعي + tokens (من `.ux/last-recommendation.json`).
- **مُخرجاته:** كود عامل يتميّز عن الناتج العامّ للذكاء الاصطناعي. بلا تدرّجات بنفسجيّة، بلا سطح رئيسي موسّط، بلا ثلاث بطاقات متساوية، بلا Inter بحجم عرضي، بلا «John Doe»، بلا إيموجي، بلا افتراضات بـ 300 مللي ثانية.
- **الأدوات:** `Read, Write, Edit, Bash, Glob, Grep`.

### `motion-engineer`

- **يملك:** الحركة داخل كود الواجهة الأماميّة الإنتاجي، Framer Motion، GSAP، رسوم CSS. المدد، المنحنيات، التتابع، بدائل إيقاف الحركة، انضباط الأداء.
- **يستدعيه:** `/ux-design` (كل الأوضاع)، `/ux-motion --fix`.
- **مُدخلاته:** موجز حركة + tokens + مهيّآت الحركة الـ 57 من `data/motion-presets.json`.
- **مُخرجاته:** حركة تستحقّ مكانها. ملفوفة دومًا بفروع `prefers-reduced-motion`. مُختبَرة دومًا مقابل Core Web Vitals.
- **الأدوات:** `Read, Write, Edit, Bash, Glob, Grep`.

### `copy-writer`

- **يملك:** النصوص التي تُشحَن، رسائل الأخطاء، الحالات الفارغة، أزرار CTA، حالات التحميل، رسائل النجاح، التنبيهات، النصوص المساعدة، تسميات النماذج، نصوص الأزرار.
- **يستدعيه:** `/ux-copy --fix`، `/ux-design` (كل الأوضاع)، `/ux-discover --frame`.
- **مُدخلاته:** ملفّ تعريف الصوت (مُسمّى أو ملصق) + نصوص السطح.
- **مُخرجاته:** نصوص دقيقة إنتاجيّة مُطبَّقة باتّساق على كلّ حالة في السطح، ليبدو المنتج منتجًا واحدًا لا عشرة. ممنوعات: «النموذج يحوي أخطاء»، «John Doe»، نصوص الذكاء الاصطناعي الاحتفاليّة المرحة، أزرار CTA عامّة، حالات فارغة ميّتة.
- **الأدوات:** `Read, Write, Edit, Bash, Glob, Grep`.

### `research-synthesizer`

- **يملك:** هضم مُدخلات البحث (مقابلات، تحليلات، مواقع المنافسين، نتائج A/B، تذاكر الدعم) إلى توصيات تصميم قابلة للتنفيذ.
- **يستدعيه:** `/ux-research`، `/ux-workshop`، `/ux-discover --frame`.
- **مُدخلاته:** بحث خام، نصوص مقابلات، تصديرات، روابط منافسين، تجميعات دعم.
- **مُخرجاته:** موضوعات، أدلّة، توصيات. لا يُصمّم الجواب أبدًا، يُعطي المصمّم المادّة التي يُصمَّم منها.
- **الأدوات:** `Read, Write, WebFetch, Bash, Glob, Grep`.

### `design-system-architect`

- **يملك:** أنظمة تصميم كاملة، tokens (لون، خطّ، فراغ، حركة، نصف قطر، ظلّ)، وثائق أُسس، عقود مكوّنات، إقران الوضع الداكن، طبقة السمات.
- **يستدعيه:** `/ux-system`، و`/ux-design --component` حين لا يوجد نظام.
- **مُدخلاته:** موجز علامة + `.ux/last-recommendation.json` (أسلوب + لوحة + اقتران طباعي + مهيّآت حركة).
- **مُخرجاته:** نظام متماسك ذو وجهة نظر جاهز للإنتاج يستطيع الوكلاء اللاحقون البناء عليه دون إعادة اتّخاذ القرارات الأساسيّة. tokens بصيغة JSON، أُسس MD، عقود مكوّنات، إقران للوضع الداكن.
- **الأدوات:** `Read, Write, Edit, Bash, Glob, Grep`.

### بروتوكول استدعاء الوكلاء الفرعيّين

حين يستدعي أمرٌ وكيلًا فرعيًّا، يُمرّر إليه:

1. الموجز / التوصية (محمَّل من `.ux/`).
2. الشريحة المعنيّة من الملفّات (مثلًا: `frontend-engineer` يحصل على الأسلوب + لوحة الألوان + المكوّنات المُختارة؛ و`motion-engineer` يحصل على مهيّآت الحركة المُختارة).
3. حواجز الأنماط الضارّة الـ 171 (مُفعّلة دومًا).
4. معيار نجاح (ما يجب أن يفعله الناتج).

يُعيد الوكلاء الفرعيّون:

1. الناتج (كود، وثيقة، نظام).
2. كتلة تبرير (لماذا هذه الاختيارات).
3. فحصًا ذاتيًّا مقابل الحواجز (أيّ القواعد تحقّقوا منها).

يُشغّل الأمر المُستدعي بعد ذلك `/ux-lint` تلقائيًّا قبل إعلان الانتهاء.

---

## ملفّات البيانات الـ 11

طبقة البيانات هي العقل. كلّ أمر يقرأ منها؛ والمحرّك يدمج عبرها؛ والمُدقّق يفحص ضدّها. كلّ الملفّات تعيش تحت `data/` وتُغلَّف مدخلاتها بـ `{_meta, entries}` للمحافظة على إصدارات المخطّط.

### `styles.json`: 84 أسلوبًا تصميميًّا

| الحقل | الوصف |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | بساطة / سويسري، Brutalist، تحريري، Glassmorphism، Neumorphism، Bento، Skeuomorphic، صناعي، Maximalist، AI-Futurist، MENA-modern، Vaporwave، إلخ. |
| `sample entry` | `swiss-international`، «الشبكة قانون. الخطّ يقوم بالحمل الثقيل. الزخرفة فشل.» |

تستخدمه: `/ux-discover`، `/ux-system`، `/ux-design`. المخطّط: [data/SCHEMAS.md](data/SCHEMAS.md).

### `palettes.json`: 176 لوحة ألوان

| الحقل | الوصف |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (فاتح/داكن), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | دافئ، تحريري، magazine، عيادي، مرح، Brutalist، أحادي اللون، Jewel-tone، شرق أوسطي دافئ، dev-tools-dark، إلخ. |
| `sample entry` | `claude-warm-editorial`، فاتح، دافئ/تحريري/magazine، canvas #faf9f5، primary #cc785c |

تستخدمه: `/ux-discover`، `/ux-system`. التباين مُحقَّق وفق AA / AAA. المخطّط: [data/SCHEMAS.md](data/SCHEMAS.md).

### `type-pairs.json`: 70 اقترانًا طباعيًّا

| الحقل | الوصف |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (family + weights + source + license + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`، Cormorant Garamond × Inter × JetBrains Mono |

لكل عائلات الخطوط رخصة + رابط مصدر. تستخدمه `/ux-discover` و`/ux-system`.

### `components.json`: 148 مكوّنًا

| الحقل | الوصف |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | تنقّل، نماذج، عرض بيانات، تغذية راجعة، طبقات فوقيّة، تخطيط، محتوى، تسويق، تجارة إلكترونيّة، توثيق، لوحات تحكّم، رسوم بيانيّة، حالات فارغة، حالات تحميل، حالات أخطاء |
| `sample entry` | `mega-nav-product-grid`، Mega Navigation, Product Grid، تشريح من 6 أجزاء، 4 حالات |

هذا أعمق خندق دفاع لدينا. لا تُقدّم أيّ إضافة UX أخرى لـ Claude ملفّ مكوّنات مُهيكلًا.

### `industries.json`: 184 قاعدة قطاع

| الحقل | الوصف |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | خدمات ماليّة، رعاية صحيّة، تعليم، تجارة إلكترونيّة، SaaS B2B، SaaS B2C، أدوات مطوّرين، إعلام، ألعاب، سفر، عقارات، خاصّة بالشرق الأوسط، إلخ. |
| `sample entry` | `fintech-neobank`، ثقة عالية، إفصاحات تنظيميّة، واجهة رئيسيّة للأرصدة/المعاملات، أولويّة للهاتف للاستخدام اليومي |

يستخدمه نظام التوصية (`/ux-discover`) كأوّل محور بحث متوازٍ.

### `chart-types.json`: 35 نوع رسم بياني

| الحقل | الوصف |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | مقارنة، سلاسل زمنيّة، توزيع، تكوين، علاقة، تدفّق، جغرافي |
| `sample entry` | `bar-vertical`، قارن بين 4 و15 فئة منفصلة. الموقع على المحور x يُمثّل الفئة؛ الارتفاع يُمثّل القيمة. |

يستخدمه `/ux-design --dashboard` و`/ux-design --component` (نسخ الرسوم البيانيّة).

### `tech-stacks.json`: 25 منظومة تقنيّة

| الحقل | الوصف |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | إنتاج، ما قبل الإصدار، تجريبي |
| `sample entry` | `nextjs-15-app-router`، Next.js 15 (App Router)، TS/JS، SSR، RSC، متوافق مع Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css |

من المنظومات الأخرى: Astro، SvelteKit، Remix، Nuxt 3، Solid Start، Qwik، Blade+Alpine، Hotwire، Phoenix LiveView، Hydrogen 2025.

### `ux-guidelines.json`: 112 قانون UX مُسمّى

| الحقل | الوصف |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | كلفة القرار، الانتباه، الذاكرة، التحكّم الحركي، الإدراك البصري، الاجتماعي، العاطفي، النماذج، معالجة الأخطاء، التهيئة، الحالة الفارغة، إلخ. |
| `sample entry` | `hicks-law`، زمن القرار ينمو لوغاريتميًّا مع عدد الخيارات المعروضة |

تستخدمه `/ux-audit` (تقييم بست عدسات) و`/ux-critique` (مرتكز ذوقي).

### `motion-presets.json`: 57 مهيّأة حركة

| الحقل | الوصف |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (بديل لإيقاف الحركة), `when_to_use` |
| `categories` | دخول، خروج، تمرير، تركيز، نقر، تحميل، فارغة، نجاح، خطأ، مرتبطة بالتمرير |
| `sample entry` | `fade-up-12px`، 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

كلّ مهيّأة لها متغيّر لإيقاف الحركة. كود جاهز للمنظومات: Framer Motion، GSAP، CSS الخالص.

### `anti-patterns.json`: 171 قاعدة

| الحقل | الوصف |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`، `name`، `severity` (critical/high/medium/low)، `category`، `detection` (النوع، النمط، الخيارات، النطاق، ولكثير من القواعد فحص `post` على الملف بعد تحليله)، `why`، `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

قائمة القواعد الكاملة في [قواعد مكافحة ركاكة الذكاء الاصطناعي الـ 171](#قواعد-مكافحة-ركاكة-الذكاء-الاصطناعي-الـ-171-المُدقّق).

### `brands/*.json`: 160 مواصفة علامة

| الحقل | الوصف |
|---|---|
| `entries` | 160 (إضافة إلى `_index.json` الذي يسرد الجميع) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | أدوات مطوّرين (36)، استهلاكي / أسلوب حياة / تجزئة (19)، تقنيات ماليّة / عملات مشفّرة (14)، تحريري / إعلام (13)، منصّات AI / ML (12)، إنتاجيّة / تعاون (8)، سيارات (8) |

القائمة الكاملة في [مواصفات DESIGN.md الـ 160 للعلامات](#مواصفات-designmd-الـ-160-للعلامات-حسب-الفئة).

---

## قواعد مكافحة ركاكة الذكاء الاصطناعي الـ 171: المُدقّق

يأتي ux-skill بمُدقّق حتمي: كل قاعدة نمط، وكثير منها يضيف فحصًا على CSS والترميز بعد تحليلهما، فلا يُحتسب التطابق إلا في السياق الذي تسمّيه القاعدة. **بلا LLM.** **بلا API.** **بلا شبكة.** يعمل داخل CI في نحو 200ms على تطبيق Next.js نموذجي. وينتهي بشيفرة عدم نجاح عند ملاحظات Critical / High حين يُضبط `--fail-on high`.

مصدر القواعد هو `data/anti-patterns.json` (v2، المفضّل) مع `references/foundations/anti-patterns.md` بديلًا احتياطيًا (v1، bash). ويُشحن ملفّان تنفيذيان: `bin/ux-lint.py` (Python، سريع، قابل للتوسيع) و`bin/ux-lint.sh` (Bash + perl-PCRE، للبيئات التي تخلو من Python).

### القواعد حسب الفئة

يُولَّد الكتالوج الكامل للقواعد الـ 171، مرتّبةً حسب الفئة ثم حسب الخطورة، من `data/anti-patterns.json` في [README الإنجليزي](README.md#rules-by-category)، وتظهر فيه معرّفات القواعد وأسماؤها كما يطبعها المُدقّق. القواعد تُغطّي A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2).

### استخدام المُدقّق

**فحص مفرد:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
bash bin/ux-lint.sh src/
```

**بوّابة CI (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**خطّاف ما قبل الالتزام:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**الإخراج (نموذج):**

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

## مواصفات DESIGN.md الـ 160 للعلامات: حسب الفئة

علامات حقيقيّة. لغات تصميم حقيقيّة. مواصفات DESIGN.md حقيقيّة، لا لوحات عامّة. تطلب من الإضافة «اصنع صفحة هبوط بأسلوب Stripe» فتقرأ مفردات العلامة الفعليّة: معايير الصوت، tokens الألوان، أعراف الحركة، الحركات المميِّزة، والحركات المضادّة.

تُسلَّم كلّ علامة على هيئة JSON مُهيكَل (`data/brands/<slug>.json`) إضافة إلى مرجع نثري (`references/brands/<slug>.md`).

### أدوات مطوّرين (36)

ClickHouse، Composio، Cursor، Datadog، dbt Labs، Expo، Fivetran، Fly.io، Framer، HashiCorp، Honeycomb، IBM، Lovable، Mintlify، Modal، MongoDB، Neon، Ollama، OpenCode، PostHog، Railway، Raycast، Render، Replicate، Resend، Retool، Sanity، Sentry، Slack، Snowflake، Sourcegraph، Supabase، Superhuman، Vercel، Warp، Webflow

### استهلاكي / أسلوب حياة / تجزئة (19)

Aesop، Airbnb، Allbirds، Apple، Apple Music، Glossier، HP، Hims & Hers، Instagram، Meta، Nike، Patagonia، Pinterest، PlayStation، Shopify، Spotify، Starbucks، TikTok، Uber

### تقنيات ماليّة / عملات مشفّرة (14)

Binance، Brex، Coinbase، Kraken، Mastercard، Mercury، Monzo، N26، Plaid، Ramp، Revolut، Robinhood، Stripe، Wise

### تحريري / إعلام (13)

Bloomberg، Clay، Dezeen، NVIDIA، Pitchfork، Substack، The Atlantic، The Economist، The New York Times، The Verge، The Wall Street Journal، Vodafone، Wired

### منصّات AI / ML (12)

Anthropic، Claude، Cohere، ElevenLabs، MiniMax، Mistral AI، OpenAI، Perplexity، Runway، Together AI، VoltAgent، xAI

### إنتاجيّة / تعاون (8)

Airtable، Cal.com، Figma، Intercom، Linear، Miro، Notion، Zapier

### سيارات (8)

BMW، BMW M، Bugatti، Ferrari، Lamborghini، Renault، SpaceX، Tesla

### لماذا يهمّ هذا

الإضافات الثماني الأخرى الشائعة لـ UX على Claude تُنتج «ميني‌مل عصري» أو «لوحة تحكّم نظيفة»، تنويعات على الجماليّة الافتراضيّة ذاتها. ux-skill يُتيح لك أن تطلب **وضوح Linear**، أو **جدّيّة Stripe**، أو **انضباط Apple**، أو **كتلة Tesla**، أو **دفء Notion**، أو **انضباط تدرّجات Cursor**، أو **كثافة شعريّات Raycast**، أو **تحريريّة Claude الدافئة**، ويسحب المحرّك الـ tokens المناسبة، والصوت، وأعراف الحركة، والحركات المميِّزة من مواصفة العلامة.

---

## خادم MCP: التحرّك غير المتماثل

يُقدّم ux-skill **خادم Model Context Protocol**. تشغّل `ux-mcp` فيتحوّل المحرّك إلى عمليّة stdio طويلة الأمد يقدر أيّ مضيف يدعم MCP (Claude Desktop وCursor وWindsurf والوكلاء العامّون) على الاتّصال بها. 25 أداة: `ux_recommend`، `ux_system_detect`، `ux_lint`، `ux_styles`، `ux_palettes`، `ux_type_pairs`، `ux_components`، `ux_industries`، `ux_motion_presets`، `ux_anti_patterns`، `ux_brands`، `ux_landing_patterns`، `ux_persist_save`، `ux_persist_load`، `ux_stats`، `ux_image_extract`، `ux_synthesize`، `ux_decisions_query`، `ux_decisions_stats`، `ux_system_build`، `ux_system_import`، `ux_system_enhance`، `ux_system_extend`، `ux_system_export`، `ux_contracts_check`. معالجات Python نفسها التي تستخدمها أوامر الشرطة المائلة؛ وملفّات البيانات نفسها؛ ونظام التوصية الحتمي نفسه.

**لماذا هذا تحرّكٌ غير متماثل:** ولا واحدة من أعلى ثماني مهارات UX لـ Claude (ui-ux-pro-max-skill، open-design، taste-skill، huashu-design، stitch، nothing-design، hallmark، material-3) تُصدر خادم MCP. كلّها محبوسة داخل runtime إضافات Claude Code. أمّا ux-skill فيمكن الوصول إليه من أيّ مضيف يتحدّث MCP، بما في ذلك وكلاء لم يسمعوا قطّ بإضافة Claude Code.

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

وجّه عميلك إلى الملفّ التنفيذي `ux-mcp`. توثيق الأدوات الكامل، وأمثلة JSON، وإعدادات كلّ عميل لـ Claude Desktop وCursor وWindsurf موجودة في [docs/mcp.html](docs/mcp.html) وفي `commands/ux-mcp.md`.

---

## مثبّت 17 بيئة تطوير

`uxskill init` (أو `/ux-init` داخل Claude Code) يكتشف تلقائيًّا أيّ بيئة تستخدم ويكتب الناتج الصحيح. نفس محرّك Python. نفس التوصيات. غراء مختلف لكلّ بيئة.

| بيئة التطوير / الأداة | إشارة الاكتشاف | الناتج المثبَّت |
|---|---|---|
| Claude Code | `.claude/` أو `CLAUDE.md` | بيان الإضافة في `.claude-plugin/plugin.json` + الأوامر الـ 18 كلّها (والأسماء البديلة السبعة) + الوكلاء الفرعيون الخمسة كلّهم |
| Cursor | `.cursor/` أو `.cursorrules` | رأس prompt في `.cursorrules` يُشير إلى المحرّك |
| Windsurf | `.windsurf/` أو `.windsurfrules` | `.windsurfrules` بنفس رأس الـ prompt |
| GitHub Copilot | `.github/copilot-instructions.md` أو `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | تعديل على `.continue/config.json` |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` أو `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

في كلّ بيئة، تعمل أوامر `uxskill recommend` / `uxskill lint` / `uxskill stats` من الطرفيّة بنفس الطريقة. محرّك Python هو مصدر الحقيقة؛ ونواتج البيئات هي رؤوس prompt نحيلة تُوجِّه إليه.

---

## حالات استخدام: سيناريوهات ملموسة

ثمانية سيناريوهات حقيقيّة. اختر الأقرب إلى وضعك وكيِّف الاستدعاء.

### 1. بناء لوحة تحكّم لتقنيات ماليّة في Cursor

أنت في Cursor تعمل على لوحة تحكّم لبنك رقمي في الشرق الأوسط. تُثبّت الإضافة وتُشغّل الاكتشاف، ثم التوصية، ثم توليد لوحة التحكّم.

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

ثم في Cursor، اطلب: *«ولّد سطح لوحة التحكّم باستخدام التوصية في .ux/last-recommendation.json»*. يقرأ Cursor رأس `.cursorrules`، ويُحمّل التوصية، ويُشغّل توليد لوحة تحكّم بقيود صريحة.

### 2. توليد صفحة هبوط بأسلوب Stripe في Claude Code

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

### 3. تدقيق كود قائم بحثًا عن ركاكة الذكاء الاصطناعي داخل CI

شحنت تطبيق Next.js قبل أسبوعين. تريد سقفًا صلبًا ضدّ بصمات الذكاء الاصطناعي على كلّ PR.

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

PRs التي تُدخل تدرّجات بنفسجيّة إلى زرقاء، أو Inter بحجم 96 بكسل، أو شهادات «John Doe»، أو إيموجي كأيقونات، تفشل في CI. بلا كلفة LLM. نحو 200 مللي ثانية.

### 4. صقل سطح قائم «يبدو من صنع الذكاء الاصطناعي»

ورثت تطبيق React يبدو مثل أيّ موقع SaaS آخر مُولَّد بالذكاء الاصطناعي. تريد ألّا يبدو هكذا بعد الآن.

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

ثلاثة أوامر، سطح مصقول، التزامات ذرّيّة لكلّ إصلاح.

### 5. تصميم لوحة أوامر بأسلوب Linear

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

المكوّن المُولَّد يستخدم tokens ألوان Linear الحقيقيّة، وكومة الخطوط، وأعراف الحركة، وكثافات الشعريّات، لا «واجهة داكنة عامّة».

### 6. إدارة ورشة تفكير تصميمي مدّتها 90 دقيقة مع أصحاب المصلحة

لديك غرفة فيها 5 أشخاص لمدّة 90 دقيقة. تريدهم أن يخرجوا بخطّة لعب، لا بإحساس عامّ.

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

تُيسّر الإضافة المراحل الخمس (استكشاف → خريطة حرارة → خريطة أصحاب مصلحة → رسم حلّ → خطّة لعب) من البداية للنهاية، محسوبةً بالوقت، بمخرجات ملموسة في كلّ مرحلة. الإخراج هو `.ux/last-workshop.json`، خطّة اللعب، لا مجرّد «ملاحظات مثيرة للاهتمام».

### 7. كتابة دراسة حالة قابلة للنشر بعد الإطلاق

شحنت محفظة الولاء. تريد قطعة بورتفوليو.

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

دراسة الحالة ناتج مُنجَز قابل للنشر، لا مسوّدة. أحاديّ اللون نقي، طباعة تحريريّة، جاهز للشحن إلى بورتفوليوك.

### 8. تشغيل الاكتشاف في سياق غير ذكاء اصطناعي (مجرّد استخراج مُهيكَل)

أنت تُحدّد نطاق مشروع. لا تحتاج توصية بعد، تحتاج موجزًا مُهيكَلًا.

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

يمكنك تسليم الـ JSON لفريقك، أو لصقه في وثيقة Notion، أو تمريره إلى أداة ذكاء اصطناعي منفصلة. ux-skill هو كذلك أداة استخراج مُهيكَل، إلى جانب كونه محرّكًا.

### 9. حفظ MASTER.md: قرارات التصميم في المستودع

بعد `/ux-discover` (أو `/ux-discover --recommend`)، احفظ الأسلوب + لوحة الألوان + الاقتران الطباعي + الحركة + المكوّنات + العلامات النموذجيّة + الحواجز المُختارة بوصفها ملفّ Markdown سهل القراءة يستطيع فريقك مراجعته وعمل diff عليه ووضعه تحت إدارة الإصدارات.

```bash
python3 -m engine.cli.main persist save --project-root .
```

يكتب `.ux/design-system/MASTER.md` (YAML frontmatter + متن) ويكتب `.ux/design-system/pages/<name>.md` لكلّ سطح مولَّد عبر `persist save-page`. مُمتنع التكرار، المُدخل ذاته يُنتج مُخرَجًا متطابقًا بالبايت، فإعادة التشغيل على حالة لم تتغيّر تكون عمليّة بلا أثر في git.

---

## المقارنة مع البدائل

جدول ملخّص. المقارنة الكاملة المتوازية على [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html).

| البُعد | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| أوامر الشرطة المائلة | **18** | 1 | 19 | 1 | 1 | متعدّد | 1 | 1 | 1 |
| المكوّنات | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| مهيّآت الحركة | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| مواصفات العلامات | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| قواعد الأنماط الضارّة | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| مُدقّق حتمي آمن للـ CI | **نعم** | لا | لا | لا | لا | لا | لا | لا | لا |
| بيئات التطوير المدعومة | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| بوّابة اكتشاف | **10 حقول** | ضمنيّة | ضمنيّة | ضمنيّة | ضمنيّة | ضمنيّة | ضمنيّة | ضمنيّة | ضمنيّة |
| سلسلة حالة `.ux/` | **نعم** | لا | لا | لا | لا | لا | لا | لا | لا |
| النجوم (2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### تقييم صريح

- **ui-ux-pro-max** أكبر في الانتشار، يدعم 18 بيئة تطوير، ولديه بحث على طريقة BM25 فوق ملفّ CSV. لا يُصدر ملفّ مكوّنات، ولا ملفّ حركة، ولا مكتبة علامات، ولا مُدقّقًا حتميًّا.
- **open-design** يملك 19 مهارة + معاينة، لكنّه يدعم Claude Code فقط، وبلا طبقة مضادّة للركاكة.
- **hallmark** الأقرب روحًا (مضادّ للركاكة هو الآخر)، لكنّه مهارة واحدة، بلا محرّك، بلا ملفّات، بلا سلسلة أوامر.
- **material-3-skill** ممتاز إن أردت تحديدًا Material Design 3. لا ننافس على MD3.

للتفاصيل الكاملة لكلّ بُعد، انظر [compare.html](https://uxskill.laithjunaidy.com/compare.html).

---

## خارطة الطريق

التالي، دون إصدار محدّد:

- **أنماط Figma**: أنماط تأثيرات للظلال، وأنماط شبكات، وأنماط نصوص مرتبطة بمتغيّرات الحقول، تُكتب في ملف حيّ.
- **ربط المكوّنات**: مكوّن Figma ومتغيّراته مربوطان بمكوّن في الكود وخصائصه، ويبقى الربط قائمًا طوال التسليم.
- **مستورد من موقع حيّ**: قراءة النظام الذي يعرضه موقع منشور فعلًا، إلى جانب مستوردات الملفّات.
- **صفحات توثيق لنظام مبنيّ**: العرض البشري لرموزه وأدواره وعقوده.

ومفتوح أيضًا:

- **`uxskill lint --fix` لإعادة كتابة آمنة** للملاحظات القابلة للإصلاح آليًّا (button-no-type، وimg-no-alt بنصّ فارغ، وإزالة console-log-leak).
- **إضافة VS Code** تعرض ملاحظات الفحص داخل الكود.
- **إخراج كود لكل مكوّن** في ست منظومات (Next.js + React، Vue 3 + Nuxt، SvelteKit، Astro، Blade + Alpine، HTML/CSS خالص).
- **سوق لمواصفات العلامات**: نشر مواصفات العلامات من المجتمع واكتشافها.
- **قواعد أنماط ضارّة مخصّصة**: اكتشاف ومشاركة القواعد التي تعرّفها المشاريع في `data/anti-patterns.local.json`.
- **`uxskill plan`**: تخطيط مواقع متعدّدة الصفحات انطلاقًا من موجز، لا واجهة واحدة فقط.

---

## المساهمة

البلاغات وطلبات السحب مرحَّب بها. ثلاث مناطق ذات رافعة عالية:

### إضافة قاعدة نمط ضارّ

1. عدّل `data/anti-patterns.json`، أضف مدخلًا بحقول `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references`.
2. أضف اختبارًا في `tests/linter/`، ملفّ يُشعل القاعدة، وآخر لا يفعل.
3. شغّل `uxskill lint tests/linter/should-trigger/<rule>.tsx`، تأكّد أنّها تشتعل. شغّل على `tests/linter/should-not-trigger/<rule>.tsx`، تأكّد أنّها لا تشتعل.
4. افتح PR.

### إضافة مواصفة علامة

1. أنشئ `data/brands/<slug>.json` بحقول `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references`.
2. أضف النصّ المرافق في `references/brands/<slug>.md`.
3. سجّلها في `data/brands/_index.json`.
4. افتح PR. يجب أن تستند المواصفة إلى مراجع من المصدر الأوّل (المنتج الفعلي للعلامة، نظام تصميمها العام، أو ملفّ DESIGN.md إن نشرته).

### إضافة مهيّأة حركة

1. عدّل `data/motion-presets.json`، أضف مدخلًا بحقول `id`, `name`, `category`, `tokens`, `stacks` (framer_motion، gsap، css), `accessibility.reduced_motion_fallback`, `when_to_use`.
2. يجب أن تملك المهيّأة متغيّرًا لإيقاف الحركة. بلا استثناءات.
3. افتح PR.

### آليّة العمل

- اقرأ [CONTRIBUTING.md](CONTRIBUTING.md) لمعرفة الآليّة الكاملة.
- اقرأ [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- تُراجَع القواعد ومواصفات العلامات الجديدة من جهة: الاستناد إلى مصدر أوّل، عدم التكيّف الزائد مع مشروع واحد، خلوّ البيانات من أيّ إيموجي، وسلامة السلوك في RTL حين ينطبق.

---

## الترخيص، المؤلّف، الشكر

### الترخيص

MIT. استخدمه، فرّعه، ابنِ فوقه. إن وفّر عليك شحن ركاكة ذكاء اصطناعي، فضع نجمة على المستودع، هذه أرخص طريقة لدعمه.

### المؤلّف

**ليث الجنيدي**: مؤسّس فردي لـ [Dot](https://thedotwallet.com)، منصّة ولاء تنطلق من الشرق الأوسط. أبني ux-skill حتى لا تبدو الواجهات الأماميّة المُولَّدة بالذكاء الاصطناعي كلّها متشابهة.

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- البريد: laith.aljunaidy.laith@gmail.com
- المستودع: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- الموقع: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### شكر

- لفريق Anthropic على Claude Code وعلى بنية المهارات / الإضافات التي جعلت توزيع هذا ممكنًا.
- لمجموعة Nielsen Norman، ولـ Laws of UX (lawsofux.com)، ولمجتمع أبحاث تجربة المستخدم الذي يستند إليه `data/ux-guidelines.json`.
- لكلّ علامة مذكورة في `data/brands/`، أنظمتها التصميميّة العامّة هي مصدر الحقيقة لمواصفاتها.
- لمساهمي v1 الأوائل: مهارة Claude بضربة واحدة كانت بذرة محرّك Python في v2.
- للإضافات الثماني الشائعة التي قارنّا أنفسنا بها، رفعت السقف؛ وهذه إجابتنا.

---

**ux-skill** · **v4.0.0b2** · بُنيت لتُخرج Claude Code وCursor وWindsurf وكلّ أداة برمجة ذكيّة أخرى واجهات أماميّة لا تُقرَأ كأنّها من صنع الذكاء الاصطناعي.

> ضع نجمة للمستودع على [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · ثبّت عبر `pip install uxskill` أو `npx uxskill init` · تصفّح المقارنة على [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html)

</div>
