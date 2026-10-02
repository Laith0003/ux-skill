[English](README.md) · [العربية](README.ar.md) · [简体中文](README.zh.md) · [繁體中文](README.zh-TW.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · **हिन्दी** · [Bahasa Indonesia](README.id.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md) · [Português](README.pt-BR.md) · [Italiano](README.it.md) · [Русский](README.ru.md) · [Türkçe](README.tr.md)

# ux-skill: Claude Code, Cursor और हर दूसरे AI कोडिंग टूल के लिए डिज़ाइन इंटेलिजेंस इंजन

**एक डिज़ाइन इंटेलिजेंस इंजन जो AI से बने UI को घिसा-पिटा नहीं, अलग पहचान वाला बनाता है।** इसे 17 AI कोडिंग टूल में से किसी में भी जोड़िए और आपका आउटपुट AI का बनाया हुआ दिखना बंद हो जाता है। मुफ़्त, MIT, ऑफ़लाइन, कोई LLM नहीं।

```bash
pip install uxskill
```

**[GitHub पर ux-skill को स्टार दें](https://github.com/Laith0003/ux-skill)** अगर यह काम का लगे: प्रोजेक्ट की मदद करने का यही सबसे आसान तरीका है। पहली बार आए हैं? [60 सेकंड के टूर](#त्वरित-इंस्टॉलेशन) से शुरू करें या इसे [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) पर लाइव देखें।

![पहले: स्टॉक फ़ोटो वाला आम-सा हीरो, हल्का बैंगनी ग्रेडिएंट, कोई ब्रांड पहचान नहीं। बाद में: गहरे स्क्रिम के नीचे असली कंस्ट्रक्शन साइट की फ़ोटो, एम्बर एक्सेंट वाली एडिटोरियल हेडलाइन, और हीरो के अंदर कोटेशन माँगने का फ़ॉर्म। वही प्रॉम्प्ट, पर जब पाबंदियाँ ux-skill देता है तो नतीजा अलग।](https://raw.githubusercontent.com/Laith0003/ux-skill/main/docs/blog/skiphire-redesign.png)

*पहले: स्टॉक फ़ोटो वाला आम-सा SEO स्लॉप। बाद में: गहरे स्क्रिम के नीचे असली कंस्ट्रक्शन फ़ोटो वाला हीरो, एम्बर एक्सेंट वाली एडिटोरियल हेडलाइन, हीरो में कोटेशन फ़ॉर्म। वही AI कोडिंग टूल, वही प्रॉम्प्ट, पर जब पाबंदियाँ ux-skill देता है तो नतीजा अलग।*

> **v4.0, FOUNDATIONS: एक कमांड पूरा, WCAG से जाँचा हुआ डिज़ाइन सिस्टम बनाती है, जिसमें अरबी और दाएँ से बाएँ लेखन पहले से शामिल है।** AI कोडिंग के लिए सबसे मज़बूत UX प्लगइन। डिटरमिनिस्टिक 7-अक्ष सिंथेसाइज़र वाला Python रीज़निंग कोर, 12 क्वेरी करने योग्य JSON मैनिफ़ेस्ट (84 स्टाइल, 176 पैलेट, 70 टाइप जोड़ियाँ, 148 कंपोनेंट, 184 इंडस्ट्री, 35 चार्ट प्रकार, 57 मोशन प्रीसेट, 112 UX नियम, 171 एंटी-पैटर्न नियम, 25 टेक स्टैक, 160 ब्रांड स्पेक), 18 स्लैश कमांड, 5 सब-एजेंट, 25 MCP टूल, और एक डिटरमिनिस्टिक एंटी-AI-स्लॉप लिंटर। क्रॉस-IDE: Claude Code, Cursor, Windsurf, GitHub Copilot, Gemini CLI, Codex, Kiro, Cline, Continue, Aider, Zed, JetBrains AI, Pieces, Tabby, Tabnine, CodeWhisperer और Roo Cline में इंस्टॉल होता है।

> **ब्रांड का नाम `ux-skill` है।** PyPI / npm पैकेज का नाम `uxskill` ही रहता है। GitHub रिपॉज़िटरी [`Laith0003/ux-skill`](https://github.com/Laith0003/ux-skill) पर है।

**लेखक:** [Laith Aljunaidy](https://laithjunaidy.com), अम्मान में डिज़ाइनर और CTO · **साइट:** [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com) · **हर Claude UX प्लगइन से तुलना:** [compare.html](https://uxskill.laithjunaidy.com/compare.html) · **GitHub:** [Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) · **PyPI:** [uxskill](https://pypi.org/project/uxskill/) · **npm:** [uxskill](https://www.npmjs.com/package/uxskill)

[![Version](https://img.shields.io/badge/version-4.0.0--beta.2-cc785c.svg)](https://github.com/Laith0003/ux-skill/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![IDEs](https://img.shields.io/badge/IDEs-17-181715)](#17-ide-इंस्टॉलर)
[![README languages](https://img.shields.io/badge/README-17_languages-cc785c.svg)](#)
[![Brands](https://img.shields.io/badge/brand_specs-160-cc785c.svg)](data/brands/_index.json)
[![Components](https://img.shields.io/badge/components-148-cc785c.svg)](data/components.json)
[![Linter](https://img.shields.io/badge/anti--patterns-171-181715.svg)](data/anti-patterns.json)
[![Tests](https://img.shields.io/badge/tests-9764_passing-cc785c.svg)](https://github.com/Laith0003/ux-skill/actions)
[![Motion](https://img.shields.io/badge/motion_presets-57-181715.svg)](data/motion-presets.json)
[![GitHub stars](https://img.shields.io/github/stars/Laith0003/ux-skill?style=social)](https://github.com/Laith0003/ux-skill/stargazers)
[![PyPI downloads](https://img.shields.io/pypi/dm/uxskill.svg)](https://pypi.org/project/uxskill/)
[![Discord](https://img.shields.io/badge/discord-community-cc785c?logo=discord&logoColor=white)](https://discord.gg/uxskill)

### 4.0 में नया: फ़ाउंडेशन

एक ब्रांड रंग दीजिए, पूरा डिज़ाइन सिस्टम पाइए, और उसका कंट्रास्ट आपके हाथ में आने से पहले जाँचा जा चुका होता है।

```bash
pip install --upgrade uxskill
uxskill system build --brand '#3366FF' --brief .ux/last-discovery.json --out design-system
```

Python 3.10 या उससे नया। MCP सर्वर के लिए `pip install --upgrade 'uxskill[mcp]'`। pipx के साथ `pipx install uxskill` (पहले से इंस्टॉल 3.x के ऊपर `pipx upgrade uxskill`)। npm के साथ `npx uxskill@latest`। 3.x से आ रहे हैं? [माइग्रेशन गाइड](docs/migrating-to-4.md) हर 3.x टोकन को 4.0 में उसके रोल से जोड़ती है।

**कोई प्रोडक्ट या लैंडिंग पेज बना रहे हैं?** आपको मिलता है पेज से लिंक करने के लिए `tokens.css`, चुने गए फ़ॉन्ट के लिए मेट्रिक से मेल खाते फ़ॉलबैक के साथ `fonts.css`, फ़ॉन्ट को आपकी अपनी फ़ाइलों से लोड करने वाला `fonts-self-host.css`, टूल के लिए `tokens.json`, `art/` में सजावटी ब्रांड आर्ट, और `system-report.md`, जो सीधे शब्दों में बताता है कि क्या बना, क्यों बना, और किस पेज कंपोज़िशन से शुरुआत करें। रोल के साथ स्टाइल करें (`var(--color-action-primary)`, `var(--color-text-default)`, `var(--color-surface-page)`), और डार्क मोड, हाई कॉन्ट्रास्ट, कॉम्पैक्ट स्पेसिंग, दाएँ से बाएँ या कम मोशन को `<html>` पर एक एट्रिब्यूट से बदलें। फ़ॉन्ट रिपोर्ट में दिए Google Fonts लिंक से लोड करें, या `fonts-self-host.css` और एक `fonts/` फ़ोल्डर से, और दोनों में से किसी के साथ `fonts.css` को `tokens.css` से पहले लिंक करें; इन दोनों फ़ाइलों में बदलाव न करें। `--brief` के साथ, ब्रीफ़ में इंडस्ट्री और टोन दिए हों तो लुक उन्हीं के हिसाब से चलता है, और स्ट्रक्चर्ड फ़ील्ड (उम्र, भाषाएँ, डिफ़ॉल्ट स्कीम, पढ़ने का संदर्भ) टेक्स्ट का आकार, टारगेट, लिपियाँ और कौन-सी स्कीम खुलेगी यह तय करते हैं; डिस्कवरी इंडस्ट्री नहीं पूछती, इसलिए `/ux-system create` पूछता है। Claude Code में `/ux-system create` इंस्टॉल वर्ज़न जाँचता है, बिल्ड चलाता है और रिपोर्ट समझाता है।

**डिज़ाइन सिस्टम डिज़ाइन कर रहे हैं?** नौ फ़ाउंडेशन (रंग, टाइपोग्राफ़ी, स्पेसिंग, लेआउट, रेडियस, बॉर्डर, एलिवेशन, मोशन, इमेजरी), हर एक सात अक्षों के साथ लगातार बदलता है, प्रिमिटिव और सिमैंटिक रोल के साथ, W3C डिज़ाइन टोकन फ़ॉर्मेट (DTCG 2025.10) में और हर मोड के मानों के साथ। वही इनपुट, वही बाइट। MCP पर `ux_system_build` रिपोर्ट, गेट का नतीजा और हर फ़ाइल का आकार लौटाता है, और `out` मिलने पर कमांड वाली ही फ़ाइलें लिखता है।

- **WCAG गेट।** टेक्स्ट, कंट्रोल और फ़ोकस की हर रंग जोड़ी को लाइट और डार्क में, सामान्य और हाई कॉन्ट्रास्ट पर मापा जाता है: सामान्य कॉन्ट्रास्ट पर WCAG 1.4.3 (टेक्स्ट 4.5:1) और 1.4.11 (नॉन-टेक्स्ट 3:1), हाई कॉन्ट्रास्ट पर WCAG 1.4.6 (टेक्स्ट 7:1), और साथ में ज़्यादातर नॉन-टेक्स्ट हिस्सों के लिए हाई कॉन्ट्रास्ट में 4.5:1 की हमारी अपनी न्यूनतम सीमा, क्योंकि WCAG नॉन-टेक्स्ट के लिए कोई उन्नत स्तर तय नहीं करता। जो सिस्टम फ़ेल होता है वह लिखा नहीं जाता; संदेश बताता है कि क्या बदलना है।
- **डिफ़ॉल्ट रूप से सुरक्षित।** यह कभी ऐसी फ़ाइल को ओवरराइट नहीं करता जो अलग हो। `--force` फ़ाइलें तभी बदलता है जब आप कहें।
- **अरबी।** `dir="rtl"` के तहत टेक्स्ट एक अरबी फ़ॉन्ट पर चला जाता है जिसके अपने आकार और लाइन-हाइट हैं; स्पेसिंग लॉजिकल प्रॉपर्टी इस्तेमाल करती है और मोशन उलट जाता है। `--latin-only` इसे बाहर रखता है।

**आपके पास पहले से मौजूद सिस्टम।** `/ux-system enhance --from` उसे उसके अपने नामों में पढ़ता है (DTCG टोकन, CSS कस्टम प्रॉपर्टी, Tailwind थीम, markdown नियम फ़ाइलें या Figma वेरिएबल एक्सपोर्ट), उसी गेट से जाँचता है और मापता है कि आपका कोड उसके साथ असल में क्या करता है; कुछ भी दोबारा नहीं लिखा जाता। `/ux-system extend --from` बिना कोई मौजूदा टोकन बदले फ़ाउंडेशन, रोल या कॉन्ट्रैक्ट जोड़ता है, उसके बगल में एक एक्सटेंशन फ़ाइल में, और `uxskill system export` उसे tokens.css, Tailwind 4 थीम या Figma वेरिएबल के रूप में लिखता है। 4.2 भरोसे की परत (हर राइट पर lint, एक फ़िनिश रिव्यूअर) और लॉन्च जोड़ेगा। [changelog](CHANGELOG.md) देखें।

**कंपोनेंट और सेक्शन।** 23 कंपोनेंट कॉन्ट्रैक्ट बताते हैं कि किसी कंट्रोल का हर हिस्सा हर स्टेट में किन टोकन से बँधता है और हर स्टेट कैसे हिलता है: स्टेट बदलने पर ट्रांज़िशन `motion.state` पर होता है, दबाने पर स्केल `motion.press.scale` पर होता है (और कम मोशन में स्थिर रहता है), और टैब, मेन्यू और सेगमेंटेड कंट्रोल एक ही इंडिकेटर खिसकाते हैं। 14 सेक्शन कॉन्ट्रैक्ट (हीरो, प्राइसिंग, FAQ, फ़ुटर और बाकी) हर सेक्शन का काम, उसके स्लॉट में आने वाले कंपोनेंट, उसे चाहिए सबूत और फ़ोन पर वह कैसे एक के नीचे एक लगता है, यह तय करते हैं। इनसे बने पेज तस्वीरें इस्तेमाल करते हैं; इंटरफ़ेस के टुकड़े अतिरिक्त इमेजरी हैं, कभी विकल्प नहीं।

**पेज पढ़ने वाला लिंटर।** 171 नियम, जिनमें से कई पार्स किए गए CSS और मार्कअप पर अलग जाँच भी करते हैं, पेज के अपने सिस्टम को पढ़ते हैं: मोशन का समय उसके कर्व से निकाला जाता है, डिस्प्ले हेडलाइन की लाइन-हाइट इंजन की न्यूनतम सीमा पर रखी जाती है, और छिपे कंट्रोल को टैब क्रम से बाहर होना चाहिए। `uxskill lint --render` हर पेज को headless Chromium में डेस्कटॉप और फ़ोन की चौड़ाई पर खोलकर चलाता है: ऐसी फ़ोकस रिंग जो दिखती नहीं या कटी हुई है, देर से जवाब देने वाला होवर और प्रेस, Escape के बाद खोया फ़ोकस, और कम मोशन में भी हिलता प्रेस।

**कम कमांड।** 25 स्लैश कमांड अब 18 हैं। `/ux-discover` `--frame` और `--recommend` लेता है, `/ux-design` `--component`, `--dashboard` और `--from-image` लेता है, `/ux-polish` lint, fix, re-lint तब तक दोहराता है जब तक स्कोर 90 न हो जाए या तीन राउंड न हो जाएँ, और `/ux-init` `--stats` लेता है। सात पुराने नाम उपनाम के तौर पर चलते रहते हैं और 4.1 में हट जाएँगे; [उपनाम](#उपनाम-41-में-हटाए-जाएँगे) देखें।

**सरफ़ेस प्लेबुक।** लैंडिंग, डैशबोर्ड और कंपोनेंट के नियम `references/surfaces/` में हैं, हर एक की अपनी प्लेबुक। `/ux-design` अपने मोड के हिसाब से ठीक एक प्लेबुक लोड करता है, इसलिए डैशबोर्ड बिल्ड कभी हीरो के नियम नहीं पढ़ता।

टेस्ट **9764 पास**। ऑफ़लाइन। डिटरमिनिस्टिक। कभी कोई LLM नहीं बुलाया जाता।

### v3.1 में नया: ब्रांड के प्रति सच्चा, रिस्पॉन्सिव, जीवंत

- **ब्रांड के प्रति वफ़ादारी लागू की जाती है, उम्मीद पर नहीं छोड़ी जाती।** प्राइमरी रंग LOGO के पिक्सल से पढ़ा जाता है (सबसे ज़्यादा पेंट हुए CSS से नहीं); डिफ़ॉल्ट फ़ॉन्ट लोगो की अक्षर-शैली से मेल न खाएँ तो खारिज होते हैं। निकाला गया ब्रांड `recommend` -> `synthesize` तक जाता है, और `evaluate` में एक **सख्त न्यूनतम सीमा** हर उस आउटपुट को फ़ेल करती है जो ब्रांड रंग या लोगो खो दे या कोई असली इमेजरी न दे। खुले `brand.md` कन्वेंशन के साथ दोनों दिशाओं में इंटरऑप (रेंडर + इन्जेस्ट)।
- **मोबाइल-फ़र्स्ट, गेट के साथ।** नए क्राफ़्ट फ़ाउंडेशन (`responsive.md`, `component-behaviors.md`) और लाइन-रैप को समझने वाला गेट, जो हॉरिज़ॉन्टल स्क्रॉल, रैप होते नैव, वर्डमार्क या बटन लेबल, या ज़रूरत से ऊँचे स्टिकी हेडर पर फ़ेल होता है।
- **वाह वाली परत।** इंजन हर पेज के लिए 2-3 आपस में तालमेल वाले सिग्नेचर पल निकालता है; "वाह सिर्फ़ यूज़र से आ सकता है" वाली धारणा पलट दी गई है।
- **ज़्यादा तेज़ लिंटर** (152 नियम): ज़रूरी इमेजरी और सिर्फ़-आइकन वाले एलिमेंट की पहचान, प्लेसहोल्डर टोकन और `100vw` के नियम; सीड वाला picsum रखा गया, रैंडम हटाया गया।

पूरे नोट्स [CHANGELOG.md](CHANGELOG.md) में।

### v3 में नया क्या है

- **ब्रांड स्पेक्स अब टेम्पलेट नहीं, ट्रेनिंग डेटा हैं।** 160 ब्रांड स्पेक्स अब वह कैटलॉग नहीं जिसमें से recommender चुनता है, वे वह शब्दावली हैं जिन्हें synthesizer आसवित करता है। हर कॉल पर नया आउटपुट।
- **7-अक्ष synthesizer** (warmth, contrast, density, geometry, formality, motion, type_personality)। ब्रीफ निर्धारक रूप से अक्ष मानों पर मैप होता है; अक्ष मान ताज़ा palette + टाइपोग्राफी + spacing + radius + motion टोकन में कंपाइल होते हैं।
- **तीन स्वचालित-डिस्पैच मोड**: `strict_brand` (एक ब्रांड का 100%), `brand_anchor` (एक ब्रांड का 70% + समान ब्रांडों से अक्ष-अनुकूलित 30%), `pure_synthesis` (कोई ब्रांड नामित नहीं, अक्ष-मिलान वाले 8 उदाहरणों से आसवन)।
- **निर्णय बही recommender को पुनः-रैंक करती है।** `.ux/decisions.jsonl` समान `(industry, ui_type)` बकेट में पिछली जीत के अनुसार उम्मीदवारों को पुनः-रैंक करता है। कोल्ड-स्टार्ट सुरक्षित। केवल `lint_score >= 80` + `user_accepted = true` वाले निर्णय गिने जाते हैं।
- **अक्ष-संपर्क मैट्रिक्स**: प्रतिस्पर्धी अक्षों के बीच स्पष्ट संघर्ष समाधान (dense + corporate → 4px, airy + corporate → 12px, soft + playful → 18px radius)। अब कोई मूक तदर्थ नियम नहीं।
- **`/ux-evolve` स्वचालित लूप** (4.0 में `/ux-polish` का डिफ़ॉल्ट लूप): स्कोर ≥ 90, पठार, या 4.0 में 3 राउंड (v3 में 5) तक lint → polish → re-lint। गुणवत्ता गेट 65 पर।
- **3 नए MCP टूल** (15 → 18): `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`।
- **स्थानीय stats डैशबोर्ड**: `uxskill stats --html` `.ux/stats.html` लिखता है जो दिखाता है कि **आपकी** स्थापना ने क्या सीखा। कोई टेलीमेट्री नहीं, कोई वैश्विक एकत्रीकरण नहीं।
- **223 परीक्षण पास।** ऑफ़लाइन। निर्धारक। LLM कभी नहीं बुलाया।

पूर्ण विवरण [CHANGELOG.md](CHANGELOG.md#300--2026-05-28--the-brain) में।

### स्टार इतिहास

[![Star History Chart](https://api.star-history.com/svg?repos=Laith0003/ux-skill&type=Date)](https://star-history.com/#Laith0003/ux-skill&Date)

---

## ux-skill क्या है

ux-skill AI कोडिंग टूल्स के लिए एक **डिज़ाइन इंटेलिजेंस इंजन** है। यह एक Python पैकेज (`pip install uxskill`), एक Claude Code प्लगइन, और 17-IDE मल्टी-इंस्टॉलर के रूप में चलता है। इंजन एक प्रोजेक्ट ब्रीफ़ (इंडस्ट्री, ऑडियंस, टोन, अनिवार्य तत्व, वर्जित तत्व, स्टैक, क्षेत्र) लेता है और एक पूर्ण अनुशंसित डिज़ाइन सिस्टम लौटाता है: शैली, पैलेट, टाइप पेयर, मोशन प्रीसेट, कंपोनेंट, अध्ययन योग्य ब्रांड उदाहरण, और जो एंटी-पैटर्न रेलिंग्स अनिवार्य हैं। यह अनुशंसा डिटरमिनिस्टिक है, एक ही इनपुट हमेशा एक ही आउटपुट देगा।

प्लगइन आपके और AI कोडिंग टूल के बीच बैठता है। जब आप Claude Code, Cursor, या किसी और AI असिस्टेंट से "एक फ़िनटेक लैंडिंग पेज बनाओ" कहते हैं, तो असिस्टेंट आमतौर पर अपने मन से कुछ भी बना देता है, और नतीजा पाँच सेकंड में AI-जनरेटेड पहचान में आ जाता है (बैंगनी से नीला ग्रेडिएंट, तीन बराबर कार्ड, डिस्प्ले साइज़ पर Inter, टेस्टिमोनियल में "John Doe", 300ms डिफ़ॉल्ट ट्रांज़िशन, बीच में रखा हीरो, उछलते तीर वाले CTA)। ux-skill अंदाज़े की जगह **संरचित पाबंदियाँ** रखता है: आप ब्रीफ़ लेने और सिस्टम चुनने के लिए `/ux-discover`, कोड जेनरेट करने के लिए `/ux-design`, और कमिट से पहले यह जाँचने के लिए कि वह 171 डिटरमिनिस्टिक एंटी-AI-स्लॉप नियमों पर खरा उतरता है, `/ux-lint` चलाते हैं।

यह README कैनोनिकल संदर्भ है। हर कमांड, हर सब-एजेंट, हर डेटा मैनिफ़ेस्ट, हर इंस्टॉल पाथ, हर ब्रांड स्पेक, हर एंटी-पैटर्न श्रेणी, सब यहीं डॉक्यूमेंट किया है। अगर आप एक Claude Code डिज़ाइन प्लगइन ढूँढ रहे हैं या Cursor, Windsurf, या Codex के लिए AI डिज़ाइन टूल्स की तुलना कर रहे हैं, तो इसे ऊपर से नीचे तक पढ़ें और साथ में [compare.html](https://uxskill.laithjunaidy.com/compare.html) भी।

---

## विषय-सूची

1. [द ब्रेन, v3.0 क्या है](#द-ब्रेन-v30-क्या-है)
2. [त्वरित इंस्टॉलेशन](#त्वरित-इंस्टॉलेशन)
3. [संख्याएँ, शीर्ष 8 Claude UX स्किल्स के साथ लाइव तुलना](#संख्याएँ-शीर्ष-8-claude-ux-स्किल्स-के-साथ-लाइव-तुलना)
4. [आर्किटेक्चर, टुकड़े कैसे जुड़ते हैं](#आर्किटेक्चर-टुकड़े-कैसे-जुड़ते-हैं)
5. [18 स्लैश कमांड, विस्तृत संदर्भ](#18-स्लैश-कमांड-विस्तृत-संदर्भ)
6. [5 सब-एजेंट](#5-सब-एजेंट)
7. [11 डेटा मैनिफ़ेस्ट](#11-डेटा-मैनिफ़ेस्ट)
8. [171 एंटी-AI-स्लॉप नियम, लिंटर](#171-एंटी-ai-स्लॉप-नियम-लिंटर)
9. [160 ब्रांड DESIGN.md स्पेक, श्रेणी के अनुसार](#160-ब्रांड-designmd-स्पेक-श्रेणी-के-अनुसार)
10. [MCP सर्वर, असममित चाल](#mcp-सर्वर-असममित-चाल)
11. [17-IDE इंस्टॉलर](#17-ide-इंस्टॉलर)
12. [उपयोग के मामले, ठोस परिदृश्य](#उपयोग-के-मामले-ठोस-परिदृश्य)
13. [विकल्पों की तुलना में](#विकल्पों-की-तुलना-में)
14. [रोडमैप](#रोडमैप)
15. [योगदान](#योगदान)
16. [लाइसेंस, लेखक, आभार](#लाइसेंस-लेखक-आभार)

---

## द ब्रेन: v3.0 क्या है

v3.1.0 ux-skill के इतिहास का सबसे बड़ा वास्तुशिल्प परिवर्तन है। Recommender अब कैटलॉग से टेम्पलेट नहीं चुनता, इंजन प्रत्येक ब्रीफ के लिए ताज़ा डिज़ाइन भाषा का **संश्लेषण** करता है। एक ही ब्रीफ हमेशा एक ही आउटपुट देता है (पूर्णतः निर्धारक), लेकिन हर अलग ब्रीफ को अपना नया सिस्टम मिलता है। ब्रांड स्पेक्स अब टेम्पलेट नहीं हैं; वे प्रशिक्षण डेटा हैं जिनसे इंजन शब्दावली सीखता है। सिस्टम की अपने इतिहास पर नज़र है, फीडबैक लूप को स्थानीय रूप से बंद करता है, और LLM कभी नहीं बुलाता।

संकलक एक **निर्धारक 7-अक्ष synthesizer** है, warmth, contrast, density, geometry, formality, motion, type_personality। हर ब्रीफ अक्ष मानों पर मैप होता है; अक्ष मान ताज़ा palette + टाइपोग्राफी + spacing + radius + motion टोकन में कंपाइल होते हैं। मॉड्यूलर टाइप स्केल contrast से अपना अनुपात चुनते हैं (1.200 quiet / 1.250 balanced / 1.333 loud)। लेआउट प्रिमिटिव निर्माण द्वारा प्रतिक्रियाशील हैं (`auto-fit minmax(min(N, 100%), 1fr)` + container queries)। टूटे लेआउट उत्सर्जित नहीं हो सकते क्योंकि वे प्रतिनिधित्व करने योग्य नहीं हैं।

तीन स्वचालित-डिस्पैच मोड हैं: `strict_brand` (`reference_brands=[stripe] strict=True` → 100% Stripe टोकन, सबसे तेज़ पथ); `brand_anchor` (`reference_brands=[stripe]` → 70% Stripe + 4 समान ब्रांडों से अक्ष-अनुकूलित 30%); और `pure_synthesis` (कोई ब्रांड नामित नहीं → अनंत स्थान, अक्ष-मिलान वाले 8 उदाहरणों से एक नई डिज़ाइन भाषा में आसवन)। प्रतिस्पर्धी अक्षों को एक प्रलेखित **अक्ष-संपर्क मैट्रिक्स** द्वारा हल किया जाता है, dense + corporate 4px पर कंपाइल होता है (density जीतता है, Bloomberg स्कूल), airy + corporate 12px पर (formality जीतता है, लक्ज़री), soft + playful 18px radius पर, sharp + corporate 2px पर। कार्यान्वयन में कोई मूक तदर्थ नियम नहीं।

**निर्णय बही** (`.ux/decisions.jsonl`, schema `_v: 1` लॉक) फीडबैक लूप बंद करती है। Recommender अब समान `(industry, ui_type)` बकेट में पिछली सफलताओं के अनुसार उम्मीदवारों को फिर से रैंक करता है। कोल्ड स्टार्ट में सुरक्षित: 3 से कम पिछले फ़ैसले हों तो री-रैंक छोड़ देता है। सिर्फ़ `lint_score >= 80` AND `user_accepted = true` वाले फ़ैसले गिने जाते हैं। साथ ही `/ux-polish` स्कोर ≥ 90, पठार, या 3 राउंड तक lint → polish → re-lint चलाता है, 65 के गुणवत्ता गेट के साथ, जिसके नीचे का आउटपुट `--force` के बिना ठुकरा दिया जाता है। नतीजा: हर इंस्टॉल अपने कॉर्पस पर समझदार होता जाता है, हर रन मशीनों के बीच दोहराया जा सकता है, और इंजन पूरी तरह ऑफ़लाइन रहता है।

---

## त्वरित इंस्टॉलेशन

तीन इंस्टॉल पाथ। जो आपके माहौल से मेल खाता है उसे चुनें।

### पाथ 1: Claude Code मार्केटप्लेस (कैनोनिकल)

अगर आप Claude Code में काम करते हैं, प्लगइन मार्केटप्लेस के ज़रिए इंस्टॉल करें:

```bash
/plugin marketplace add Laith0003/ux-skill
/plugin install ux@ux-skill
```

यह सभी 18 स्लैश कमांड (साथ में 7 पुराने नाम जो 4.1 तक उपनाम के रूप में रहेंगे) और 5 सब-एजेंट को आपके Claude Code सेशन से जोड़ देता है। इंस्टॉल के बाद, प्रति-प्रोजेक्ट `.ux/` स्टेट डायरेक्टरी सेट करने और यह सत्यापित करने के लिए कि Python इंजन पहुँच योग्य है, `/ux-init` चलाएँ।

### पाथ 2: pip (यूनिवर्सल)

अगर आप Claude Code के बाहर रहते हैं (Cursor, Windsurf, CLI, CI), Python पैकेज इंस्टॉल करें:

```bash
pip install uxskill
uxskill init                       # auto-detects your IDE, installs the right artifact
uxskill stats                      # print manifest counts to verify install
uxskill lint .                     # run the linter against the current directory
```

पैकेज `ux` और `uxskill` दोनों को CLI एंट्री पॉइंट के रूप में उजागर करता है, वे एक ही बाइनरी हैं।

### पाथ 3: npx (Python ज़रूरी नहीं)

अगर आप सीधे Python संभालना नहीं चाहते, npx रैपर `pipx` के ज़रिए सब कुछ बूटस्ट्रैप करता है:

```bash
npx uxskill init                  # downloads pipx + uxskill on first run
npx uxskill recommend --industry=fintech-neobank --tone=warm --stack=nextjs-15-app-router
```

### इंस्टॉल सत्यापित करें

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

बारह गिनतियाँ मिलाकर 1,262 एंट्री होती हैं। अगर कोई गिनती 0 लौटाती है, तो JSON फ़ाइल गुम है; [github.com/Laith0003/ux-skill/issues](https://github.com/Laith0003/ux-skill/issues) पर एक इश्यू खोलें।

---

## संख्याएँ: शीर्ष 8 Claude UX स्किल्स के साथ लाइव तुलना

स्टार की गिनती अंतिम बार `gh api` के ज़रिए **2026-05-28** को सत्यापित की गई। ux-skill (Laith0003/ux-skill) सबसे नया प्रवेशक है, हम जागरूकता पर छोटे हैं, आर्किटेक्चर पर गहरे। नीचे की तुलना ईमानदार है: हम कहाँ हारते हैं, कहाँ जीतते हैं।

| प्लगइन | स्टार | आर्किटेक्चर | स्लैश कमांड | लिंटर (CI-सेफ़) | ब्रांड स्पेक | कंपोनेंट | मोशन प्रीसेट | समर्थित IDE |
|---|---:|---|---:|---|---:|---:|---:|---:|
| nextlevelbuilder/ui-ux-pro-max-skill | **83,958** | Python BM25 + CSV, सिंगल स्किल | 1 | - |, | 0 | 0 | 18 |
| nexu-io/open-design | **54,406** | Node.js + 19 स्किल + प्रीव्यू | 19 | - |, | 0 | 0 | 1 |
| Leonxlnx/taste-skill | **25,202** | Bash + शोध-समर्थित रुचि | 1 | - |, | 0 | 0 | 1 |
| alchaincyf/huashu-design | **15,455** | सिंगल 62 KB SKILL.md + स्क्रिप्ट | 1 | - |, | 0 | 0 | 1 |
| google-labs-code/stitch-skills | **5,762** | MCP-जुड़ी स्किल लाइब्रेरी | multi | - |, | 0 | 0 | 1 |
| dominikmartn/nothing-design-skill | **2,391** | सिंगल-सौंदर्य स्किल | 1 | - |, | 0 | 0 | 1 |
| Nutlope/hallmark | **2,164** | एंटी-स्लॉप डिज़ाइन स्किल | 1 | - |, | 0 | 0 | 1 |
| hamen/material-3-skill | **955** | MD3 कंपोनेंट + ऑडिट | 1 | - | (केवल MD3) | 0 | 0 | 1 |
| **Laith0003/ux-skill (ux-skill)** | **14** | **Python इंजन + 12 मैनिफ़ेस्ट + 18 कमांड + 5 सब-एजेंट + CI लिंटर** | **18** | **171 डिटरमिनिस्टिक नियम** | **160** | **148** | **57** | **17** |

### हम कहाँ हारते हैं

- **जागरूकता।** उनके पास लाखों स्टार हैं। हमारे पास 14 हैं। हमें स्टार करें, यह मदद करने का सबसे सस्ता तरीका है।
- **ब्रांड पहचान।** ui-ux-pro-max और open-design के पास महीनों में मापी जाने वाली बढ़त है, दिनों में नहीं।
- **मार्केटिंग पॉलिश।** उनके पास स्क्रीनशॉट, डेमो वीडियो, और एक खोजने योग्य लैंडिंग पेज है। हमारे पास एक संपूर्ण README और एक पतली लैंडिंग है।

### हम कहाँ जीतते हैं

- **कंपोनेंट लाइब्रेरी:** एनाटॉमी, स्टेट, उपयोग किए गए टोकन, और मोशन स्पेक के साथ 148 डॉक्यूमेंटेड कंपोनेंट। अन्य 8 में से कोई भी एक कंपोनेंट मैनिफ़ेस्ट नहीं भेजता।
- **मोशन प्रीसेट:** रिड्यूस्ड-मोशन फ़ॉलबैक के साथ 57 स्टैक-तैयार एंट्री (Framer Motion, GSAP, CSS)। अन्य में से कोई भी मोशन मैनिफ़ेस्ट नहीं भेजता।
- **एंटी-पैटर्न लिंटर:** 171 डिटरमिनिस्टिक नियम, CI में चलते हैं, Critical/High पर non-zero exit करते हैं। अन्य में से कोई भी डिटरमिनिस्टिक लिंटर नहीं भेजता।
- **ब्रांड स्पेक:** 160 असली DESIGN.md स्पेक (Apple, Stripe, Linear, Figma, Tesla, BMW, Notion, Spotify, Airbnb, Vercel, Supabase, Cursor, Raycast, Claude, और 96 और)। अन्य में से कोई भी ब्रांड लाइब्रेरी नहीं भेजता।
- **17 IDE समर्थित:** एक ही इंजन, प्रति IDE अलग गोंद।
- **18 स्लैश कमांड:** डिस्कवरी, जेनरेशन (पेज, कंपोनेंट, डैशबोर्ड, इमेज से), ऑडिट, लिंट, पॉलिश लूप, फ़िक्स लूप, केस-स्टडी, वर्कशॉप, कॉपी, मोशन, a11y, कंडक्टर, पूरी तरह एकीकृत।

पूरी टेबल-दर-टेबल साथ-साथ तुलना [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) पर।

---

## आर्किटेक्चर: टुकड़े कैसे जुड़ते हैं

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

### इंजन असल में कैसे काम करता है

1. **इनपुट।** आप एक ब्रीफ़ देते हैं, या तो `/ux-discover` (10 फ़ील्ड) से इंटरैक्टिव तरीके से, या `ux recommend` को फ़्लैग देकर बिना इंटरैक्शन के।
2. **5 समानांतर खोजें।** इंजन मैनिफ़ेस्ट पर एक साथ पाँच लुकअप चलाता है:
   - **इंडस्ट्री → recommended_styles** (industries.json)
   - **स्टाइल → पैलेट + टाइप + मोशन संगतता** (styles.json)
   - **टोन × ज़रूरी चीज़ें → पैलेट फ़िल्टर** (palettes.json)
   - **स्टैक → कंपोनेंट संगतता + मोशन प्रीसेट** (tech-stacks.json, motion-presets.json)
   - **वर्जित + क्षेत्र → रेलिंग्स + ब्रांड उदाहरणों की शॉर्टलिस्ट** (anti-patterns.json, brands/)
3. **मर्ज।** एक डिटरमिनिस्टिक मर्जर उम्मीदवारों को रैंक करता है, टकराव सुलझाता है (जैसे ज़रूरी डार्क मोड पैलेट मोड तय कर देता है), और एक ही अनुशंसित सिस्टम देता है।
4. **आउटपुट।** एक JSON दस्तावेज़, जिसमें चुनी गई स्टाइल, पैलेट, टाइप जोड़ी, शीर्ष 5 मोशन प्रीसेट, शीर्ष 12 कंपोनेंट, शीर्ष 5 ब्रांड उदाहरण, और सभी 171 एंटी-पैटर्न रेलिंग्स सक्रिय होती हैं। साथ में हर चुनाव का कारण बताने वाला ब्लॉक।
5. **जेनरेशन।** आगे की कमांड (`/ux-design` अपने पेज, कंपोनेंट, डैशबोर्ड और इमेज मोड में, और `/ux-system`) अनुशंसा का इस्तेमाल करके सब-एजेंट के ज़रिए असली कोड बनाती हैं।
6. **सत्यापन।** `/ux-lint` जेनरेट हुए कोड को 171 नियमों पर फिर से स्कैन करता है। CI में Critical/High पर non-zero exit करता है।

**v3 में जोड़ा गया।** Recommender अब `.ux/decisions.jsonl` का इस्तेमाल करके `engine/decisions/` से उम्मीदवारों को फिर से रैंक करता है (सिर्फ़ `lint_score >= 80` AND `user_accepted = true` वाले फ़ैसले गिनता है; 3 से कम पिछले फ़ैसलों पर कोल्ड स्टार्ट में सुरक्षित)। जेनरेटर का रास्ता `engine/synthesizer/` तक भी जा सकता है, जो एक डिटरमिनिस्टिक 7-अक्ष कंपाइलर है और कैटलॉग से टेम्पलेट चुनने की जगह हर ब्रीफ़ के लिए नए पैलेट + टाइप + स्पेसिंग + रेडियस + मोशन टोकन बनाता है। ब्योरे के लिए [द ब्रेन, v3.0 क्या है](#द-ब्रेन-v30-क्या-है) देखें।

**Python सोचता है। HTML दिखाता है। Markdown जोड़ता है।**

---

## 18 स्लैश कमांड: विस्तृत संदर्भ

हर कमांड `commands/` के तहत एक `.md` फ़ाइल के रूप में आती है, जिसमें `description`, `allowed-tools`, `triggers`, `when to use`, `when to skip`, `input`, `process` और `output state file` होते हैं। नीचे के विवरण संक्षिप्त हैं; पूरा स्रोत ही आधिकारिक स्पेक है।

कमांड सात समूहों में बँटी हैं: **बूटस्ट्रैप और इन्वेंटरी**, **डिस्कवरी और अनुशंसा**, **जेनरेशन**, **ऑडिट और सत्यापन**, **फ़िक्स और पॉलिश**, **डिस्कवरी और कथा**, और **कंडक्टर**। 3.x के सात नाम 4.1 तक [उपनाम](#उपनाम-41-में-हटाए-जाएँगे) के तौर पर चलते रहेंगे।

### बूटस्ट्रैप और इन्वेंटरी

#### `/ux-init`: प्रोजेक्ट को बूटस्ट्रैप करें

- **क्या:** पहचानता है कि आप कौन सा IDE उपयोग कर रहे हैं (`.claude/`, `.cursor/`, `.windsurf/`, आदि), सही आर्टिफ़ैक्ट इंस्टॉल करता है, सत्यापित करता है कि Python इंजन पहुँच योग्य है, स्टैट्स स्नैपशॉट प्रिंट करता है। `--stats` सिर्फ़ स्नैपशॉट प्रिंट करता है: वर्ज़न + डेटा मैनिफ़ेस्ट की एंट्री गिनती।
- **कब उपयोग करें:** नए प्रोजेक्ट में पहली बार इंस्टॉल करते समय। ux-skill उपयोग करने वाले प्रोजेक्ट को क्लोन करने के बाद। `pip install --upgrade uxskill` के बाद। `--stats` इंस्टॉल के बाद, अपग्रेड के बाद, या जब कोई अनुशंसा चौंकाने वाले चुनाव दे और आपको मैनिफ़ेस्ट अधूरे होने का शक हो।
- **कब छोड़ें:** आप पहले से इस प्रोजेक्ट में चला चुके हैं और कुछ नहीं बदला। `--stats` को कभी छोड़ने की ज़रूरत नहीं: यह 50ms की रीड है।
- **आह्वान:** `/ux-init` (कोई आर्ग नहीं), `/ux-init --stats`, या CLI से `uxskill init` / `uxskill stats`। `--decisions` निर्णय बही का सारांश जोड़ता है; `--html` `.ux/stats.html` लिखता है।
- **आउटपुट:** प्रति-IDE आर्टिफ़ैक्ट ([17-IDE इंस्टॉलर](#17-ide-इंस्टॉलर) देखें) + `.ux/` डायरेक्टरी + stdout सारांश। `--stats`: stdout पर JSON (ऊपर [इंस्टॉल सत्यापित करें](#इंस्टॉल-सत्यापित-करें) देखें)।
- **जोड़ता है:** अगला `/ux-discover`। `--stats` सिर्फ़ जाँच के लिए है।

#### `/ux-mcp`: इंजन को MCP सर्वर के रूप में चलाएँ

- **क्या:** इंजन को stdio पर Model Context Protocol सर्वर के रूप में शुरू करता है। 25 टूल (recommender, लिंटर, परसिस्टेंस, सिंथेसाइज़र, निर्णय बही, इमेज एक्सट्रैक्शन, डेटा मैनिफ़ेस्ट, और डिज़ाइन सिस्टम को बनाना, इम्पोर्ट करना, बेहतर करना, बढ़ाना, एक्सपोर्ट करना और जाँचना) प्लगइन के बिना किसी भी MCP-सक्षम होस्ट से बुलाए जा सकते हैं।
- **कब उपयोग करें:** आप किसी दूसरे MCP-सक्षम होस्ट में काम करते हैं और वही इंजन चाहते हैं। आप ऐसी मल्टी-एजेंट पाइपलाइन चलाते हैं जिसे डिज़ाइन पाबंदियों का एक ही स्रोत चाहिए। आप recommender या लिंटर को CI में लंबे समय तक चलने वाली प्रक्रिया के रूप में चाहते हैं।
- **कब छोड़ें:** आप प्लगइन इंस्टॉल किए हुए Claude Code के अंदर हैं; स्लैश कमांड पहले से इंजन तक पहुँचती हैं। आपको एक बार का जवाब चाहिए; `uxskill recommend` या `uxskill lint` ज़्यादा आसान है।
- **आह्वान:** `/ux-mcp`, या `pip install 'uxskill[mcp]'` के बाद शेल से `ux-mcp`।
- **आउटपुट:** एक stdio JSON-RPC सर्वर। हर क्लाइंट के कॉन्फ़िग के लिए [MCP सर्वर](#mcp-सर्वर-असममित-चाल) और `commands/ux-mcp.md` देखें।
- **जोड़ता है:** कुछ नहीं; यह एक ट्रांसपोर्ट है, कोई कदम नहीं।

### डिस्कवरी और अनुशंसा

#### `/ux-discover`: अनिवार्य द्वार (10-फ़ील्ड इनटेक, फ़्रेमिंग, अनुशंसा)

- **क्या:** अनिवार्य 10-फ़ील्ड इनटेक, जिससे हर प्रोजेक्ट किसी भी जेनरेशन कमांड से पहले गुज़रता है। प्रोजेक्ट प्रकार, ऑडियंस, मुख्य लक्ष्य, टोन, ज़रूरी चीज़ें, वर्जित चीज़ें, रेफ़रेंस ब्रांड, स्टैक, क्षेत्र, सफलता का मापदंड। **कोई अंदाज़ा नहीं।** प्रतिबंधित शब्द ("modern", "clean") यूज़र को ठोस बात कहने पर मजबूर करते हैं। फिर recommender चलता है: Python इंजन की 12 मैनिफ़ेस्ट पर 5 समानांतर खोजें एक मिला-जुला डिज़ाइन सिस्टम लौटाती हैं (इंडस्ट्री → स्टाइल → पैलेट → टाइप → मोशन + कंपोनेंट + ब्रांड उदाहरण + रेलिंग्स)।
- **मोड:** `--frame` किसके लिए, नतीजा, परिकल्पना और सफलता संकेत को चार फ़ील्ड वाले फ़्रेमिंग ब्लॉक में दर्ज करता है, जो पूरे इनटेक से हल्का है। `--recommend` सिर्फ़ recommender चलाता है, सहेजे गए ब्रीफ़ या एक बार के फ़्लैग से।
- **कब उपयोग करें:** किसी भी `/ux-design` या `/ux-system` से पहले। जब भी पिछला ब्रीफ़ पुराना पड़ जाए। `--frame` किसी प्रोजेक्ट, स्प्रिंट या एक बार के काम की शुरुआत में, या बीच में जब बातचीत भटक गई हो। `--recommend` जब किसी थके-से दिखते प्रोडक्ट की दिशा बदलनी हो।
- **कब छोड़ें:** आप कोई बग ठीक कर रहे हैं (`/ux-fix`)। आप सिर्फ़ एक लिंटर पास चला रहे हैं (`/ux-lint`)। पिछले सेशन से ब्रीफ़ नहीं बदला।
- **आह्वान (Claude Code):** `/ux-discover`, `/ux-discover --frame "loyalty wallet for a MENA retail pilot"`, या `/ux-discover --recommend`।
  **आह्वान (CLI):**
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
- **आउटपुट:** `.ux/last-discovery.json` (10-फ़ील्ड ब्रीफ़), `.ux/last-recommendation.json` (चुनी गई स्टाइल, पैलेट, टाइप जोड़ी, शीर्ष 5 मोशन प्रीसेट, शीर्ष 12 कंपोनेंट, शीर्ष 5 ब्रांड उदाहरण, सभी 171 एंटी-पैटर्न रेलिंग्स सक्रिय, साथ में कारण), और `--frame` के साथ `.ux/last-frame.json` (`{audience, outcome, hypothesis, success_signal}`)।
- **जोड़ता है:** `/ux-design [extra brief]` → अनुशंसा पर आधारित फ़्रंटएंड कोड। `/ux-design --component <name>` → पता चली पाबंदियों के मुताबिक एक कंपोनेंट। `/ux-system` → अनुशंसा से पूरा डिज़ाइन सिस्टम। `/ux-lint` → जेनरेट हुआ कोड सत्यापित करें।

### जेनरेशन

#### `/ux-design`: ब्रीफ़ से एक सुंदर, एंटी-स्लॉप सर्फ़ेस जेनरेट करें

- **क्या:** डिस्कवरी ब्रीफ़ + अनुशंसा से पूर्ण, उत्पादन-ग्रेड फ़्रंटएंड आर्टिफ़ैक्ट (लैंडिंग, मार्केटिंग साइट, ऐप शेल) जेनरेट करता है। एंटी-स्लॉप और आर्सेनल संदर्भों की रचनात्मक दिशा के साथ `frontend-engineer` को डिस्पैच करता है। ब्रीफ़ या कोई फ़्लैग चार में से एक मोड चुनता है:
  - **पेज** (डिफ़ॉल्ट): पूरा पेज या कई सेक्शन वाला सरफ़ेस। `.ux/last-design.json` लिखता है।
  - **`--component [name]`**: एक अकेला, उत्पादन-ग्रेड कंपोनेंट (बटन, मोडल, नैवबार, साइडबार, कार्ड, टेबल, फ़ॉर्म, चार्ट)। चारों इंटरैक्शन स्टेट, सुलभ, ब्रांड के अनुरूप। कंपोनेंट को पहले `.ux/last-recommendation.json` में ढूँढता है, न मिले तो सीधे मैनिफ़ेस्ट से पूछता है। `.ux/last-component.json` लिखता है।
  - **`--dashboard`**: डेटा घनत्व का अनुशासन, बेंटो लेआउट, टेबुलर मोनोस्पेस अंक, स्पार्कलाइन पैटर्न, कार्ड की भरमार से परहेज़, अर्थपूर्ण स्टेट रंग, संयमित मोशन। ऊपर से चार्ट चिपकाई हुई मार्केटिंग साइट नहीं। `.ux/last-dashboard.json` लिखता है।
  - **`--from-image <path>`**: डिज़ाइन रेफ़रेंस इमेज (PNG/JPG/WebP) को शुद्ध Pillow कंप्यूटर विज़न से पढ़ता है (मुख्य पैलेट, कैनवस की ध्रुवता, टाइप संकेत), उसे पैलेट और स्टाइल मैनिफ़ेस्ट से मिलाता है, और मिली अनुशंसा से बनाता है। `--extract-only` एक्सट्रैक्शन के बाद रुक जाता है। `.ux/last-image-extract.json` लिखता है।
- **कब उपयोग करें:** "Design a", "build me a", "generate a landing page", "create a dashboard", "make a component", "build a button", "design the admin panel", "operator console", "KPI board", "build it like this screenshot", कोई भी फ़्री-फ़ॉर्म दृश्य डिलीवरेबल अनुरोध।
- **कब छोड़ें:** आप समीक्षा चाहते हैं, निर्माण नहीं (`/ux-audit` या `/ux-critique` का उपयोग करें)। बैकएंड या इंफ़्रास्ट्रक्चर कार्य।
- **आह्वान:** `/ux-design generate a fintech landing for a MENA neobank, warm editorial tone, dark-mode AA, no purple gradients`, `/ux-design --component pricing-card-trio --brief="fintech, dark, monospace numbers"`, `/ux-design --dashboard`, `/ux-design --from-image ref.png`।
- **आउटपुट:** जेनरेट हुआ कोड (HTML / Blade / JSX / Vue / Astro), साथ में उस मोड की स्टेट फ़ाइल।
- **जोड़ता है:** `/ux-lint` → रेलिंग्स के विरुद्ध सत्यापित करें। `/ux-polish` → कॉस्मेटिक पास। `/ux-a11y` → सुलभता ऑडिट। `/ux-copy` → माइक्रोकॉपी समीक्षा। `/ux-fix` → निष्कर्षों को परमाणु कमिट के रूप में लागू करें।

#### `/ux-system`: एक पूर्ण स्टार्टर डिज़ाइन सिस्टम जेनरेट करें

- **क्या:** एक ऐसे प्रोजेक्ट के लिए जिसके पास सिस्टम नहीं है, पूर्ण स्टार्टर डिज़ाइन सिस्टम प्रस्तावित करता है, टोकन (रंग, टाइप, स्पेस, मोशन, रेडियस, शैडो), फ़ाउंडेशन डॉक्स, कंपोनेंट कॉन्ट्रैक्ट, डार्क-मोड पेयरिंग, थीम स्विचर। `design-system-architect` को डिस्पैच करता है।
- **कब उपयोग करें:** "We don't have a design system", "build us a system", "propose tokens", "what should our theme be", "set up our DS"।
- **कब छोड़ें:** प्रोजेक्ट के पास पहले से डिज़ाइन सिस्टम है; उसकी जगह मौजूदा सिस्टम पर `/ux-design --component` का उपयोग करें। बैकएंड या इंफ़्रास्ट्रक्चर।
- **आह्वान:** `/ux-system create` (फ़ाउंडेशन इंजन), `/ux-system enhance --from <file>` (आपके पास पहले से मौजूद सिस्टम को मापें), `/ux-system extend --from <file> --add <foundation>` (बिना बदले उसमें जोड़ें), या `/ux-system` (3.x वाला तरीका; अगर फ़ाइल में पहले से डिस्कवरी नहीं है तो पहले डिस्कवरी चलाता है)।
- **आउटपुट:** `tokens.json`, `foundations.md`, `components/*.md` कॉन्ट्रैक्ट, वैकल्पिक Tailwind / vanilla / SCSS एमिट। चेन संदर्भ के लिए `.ux/last-system.json` लिखता है।
- **जोड़ता है:** `/ux-design --component` → नए सिस्टम पर बनाएँ। `/ux-design` → नए टोकन से सरफ़ेस जेनरेट करें।

#### `/ux-motion`: मोशन ट्रीटमेंट

- **क्या:** एक सर्फ़ेस की मोशन परत जेनरेट करता है, अवधि, ईज़िंग, कोरियोग्राफ़ी, रिड्यूस्ड-मोशन फ़ॉलबैक, प्रदर्शन अनुशासन। 5 आयामों (टाइमिंग, ईज़िंग, अर्थ, रिड्यूस्ड-मोशन, प्रदर्शन) के विरुद्ध मौजूदा मोशन का ऑडिट भी करता है।
- **कब उपयोग करें:** "Motion check", "are the animations good", "fix the motion", "review the animations", "motion audit", "performance pass on the motion"।
- **कब छोड़ें:** सर्फ़ेस में कोई मोशन नहीं है (`/ux-audit` या `/ux-polish` का उपयोग करें)। बैकएंड या इंफ़्रास्ट्रक्चर।
- **आह्वान:** `/ux-motion path/to/component.tsx` (ऑडिट मोड) या `/ux-motion --generate hero-entry` (जेनरेशन)।
- **आउटपुट:** अपडेट किया गया कोड (जेनरेशन मोड में) या `.ux/last-motion.json` रिपोर्ट (ऑडिट मोड में)।
- **जोड़ता है:** `/ux-fix` → मोशन निष्कर्ष लागू करें। `/ux-polish` → कसें।

### ऑडिट और सत्यापन

#### `/ux-lint`: डिटरमिनिस्टिक regex-आधारित लिंटर (कोई LLM नहीं, CI-सेफ़)

- **क्या:** आपके कोड के विरुद्ध 171 नियम चलाता है। कोई LLM कॉल नहीं। CI में Critical / High पर non-zero exit करता है। स्रोत: `data/anti-patterns.json`। नियम A11y (45), कंटेंट (35), लेआउट (18), टाइपोग्राफ़ी (16), मोशन (14), दृश्य (14), गुणवत्ता (12), रंग (10), परफ़ॉर्मेंस (5), गहराई (2) को कवर करते हैं।
- **कब उपयोग करें:** प्री-कमिट हुक। CI गेट। `/ux-audit` की लागत चुकाने से पहले बड़े कोडबेस पर तेज़ पहला पास। जेनरेशन सत्यापित करने के लिए किसी भी मोड में `/ux-design` के बाद।
- **कब छोड़ें:** आप एक फ़िक्स लूप चाहते हैं (लिंटर रिपोर्ट करता है, संपादित नहीं करता, `/ux-polish --fix` या `/ux-fix` में चेन करें)। आप रुचि निर्णय चाहते हैं (`/ux-critique` का उपयोग करें)।
- **आह्वान (स्लैश):** `/ux-lint src/`।
- **आह्वान (CLI):** `uxskill lint .` या `python3 bin/ux-lint.py .` या `bash bin/ux-lint.sh --ci --fail-on high`।
- **आह्वान (CI):**
  ```yaml
  - name: ux-lint
    run: bash bin/ux-lint.sh --ci --fail-on high
  ```
- **आउटपुट:** stdout पर निष्कर्ष (स्थान, नियम id, गंभीरता, साक्ष्य)। साफ़ होने पर एग्ज़िट कोड 0, `--fail-on high` सेट होने पर Critical/High पर non-zero।
- **जोड़ता है:** `/ux-polish --fix` → समान पैटर्न पर LLM-चालित समकक्ष। `/ux-fix` → गंभीरता-क्रमबद्ध कमिट के रूप में निष्कर्ष लागू करें। `/ux-audit` → पूर्ण 6-लेंस रीज़निंग पास। `/ux-next` → कंडक्टर को निर्णय लेने दें।

#### `/ux-audit`: 6-लेंस डिज़ाइन ऑडिट

- **क्या:** छह लेंसों (स्पष्टता, पदानुक्रम, सुलभता, आवाज़, मोशन, रुचि) के विरुद्ध एक संरचित, मतपूर्ण समीक्षा, गंभीरता-टैग किए गए निष्कर्ष उत्पन्न करती है। Polaris-शैली की रिपोर्ट। पहले `.ux/last-frame.json` पढ़ता है, ऑडियंस और परिणाम हर निष्कर्ष की गंभीरता को एंकर करते हैं।
- **कब उपयोग करें:** सर्फ़ेस मौजूद है और आप एक रक्षात्मक आलोचना चाहते हैं। "Audit", "review the ux", "is this any good", "what's broken", "tear this apart"।
- **कब छोड़ें:** सर्फ़ेस अभी मौजूद नहीं है (`/ux-design` का उपयोग करें)। उपयोगकर्ता एक लेंस चाहता है (लक्षित कमांड का उपयोग करें: `/ux-a11y`, `/ux-copy`, `/ux-motion`, `/ux-polish`)। उपयोगकर्ता रुचि की राय चाहता है (`/ux-critique` का उपयोग करें)। बैकएंड या इंफ़्रास्ट्रक्चर।
- **आह्वान:** `/ux-audit https://example.com/pricing` या `/ux-audit src/components/Pricing.tsx`।
- **आउटपुट:** `.ux/last-audit.json` लिखता है, `{lens, severity, title, principle, evidence, fix}` की `findings` ऐरे, `severity_counts`, `dominant_lens`, `strategic_moves`।
- **जोड़ता है:** `/ux-fix` → निष्कर्ष लागू करें। `/ux-polish` → कॉस्मेटिक पास। `/ux-design` → अगर संरचनात्मक रीडिज़ाइन की ज़रूरत हो।

#### `/ux-a11y`: WCAG 2.1 AA ऑडिट + सामान्य-शिष्टाचार जाँच

- **क्या:** एक संरचित WCAG 2.1 AA ऑडिट, साथ ही सामान्य-शिष्टाचार जाँच जो स्वचालित उपकरण पास कर लेती हैं लेकिन फिर भी असली उपयोगकर्ताओं को चोट पहुँचाती हैं (फ़ोकस दृश्यता, त्रुटि विशिष्टता, मोशन प्राथमिकताएँ, कीबोर्ड ट्रैप, रंग निर्भरता)।
- **कब उपयोग करें:** शिप से पहले सुलभता गेट। रीडिज़ाइन के बाद। "Accessibility check", "WCAG audit", "is this accessible", "a11y review", "screen reader test", "keyboard nav check"।
- **कब छोड़ें:** उपयोगकर्ता-सामना नहीं। बैकएंड या इंफ़्रास्ट्रक्चर। वर्क-इन-प्रोग्रेस स्केच।
- **आह्वान:** `/ux-a11y https://example.com` (लाइव URL पसंदीदा, स्वचालित उपकरण और कीबोर्ड परीक्षण केवल लाइव काम करते हैं)।
- **आउटपुट:** `.ux/last-a11y.json` लिखता है, `{wcag_sc, sc_name, severity, title, evidence, fix, category}` की `findings` ऐरे, `beyond_wcag` ऐरे, `severity_counts`।
- **जोड़ता है:** `/ux-fix` → निष्कर्षों को कमिट के रूप में लागू करें। `/ux-copy` → कॉपी पास के हिस्से के रूप में alt टेक्स्ट और फ़ॉर्म-एरर वायरिंग ठीक करें।

#### `/ux-critique`: रुचि कॉल (3 जीत, 3 चूक, 1 रणनीतिक चाल)

- **क्या:** एक डिज़ाइनर की राय, कोई संरचित ऑडिट नहीं, कोई गंभीरता स्कोर नहीं, बस एक कसी हुई, मतपूर्ण राय जो नाम लेती है कि क्या काम कर रहा है, क्या नहीं, और एक रणनीतिक चाल जो सबसे ज़्यादा बदलाव लाएगी।
- **कब उपयोग करें:** "What do you think", "is this good", "critique this", "honest take", "is the vibe right", "does this feel like us", "should we ship this"।
- **कब छोड़ें:** उपयोगकर्ता स्पष्ट रूप से एक संरचित ऑडिट चाहता है (`/ux-audit` का उपयोग करें)। बैकएंड या इंफ़्रास्ट्रक्चर।
- **आह्वान:** `/ux-critique https://example.com`।
- **आउटपुट:** `.ux/last-critique.json` लिखता है, 3 जीत, 3 चूक, 1 रणनीतिक चाल, साथ ही गद्य।
- **जोड़ता है:** `/ux-design` अगर राय रीडिज़ाइन की सिफ़ारिश करती है। `/ux-polish` अगर राय कसने की सिफ़ारिश करती है।

#### `/ux-copy`: माइक्रोकॉपी समीक्षा + पुनर्लेखन

- **क्या:** आवाज़ रूब्रिक के विरुद्ध हर दृश्यमान स्ट्रिंग का मूल्यांकन करता है और एक पहले/बाद का पुनर्लेखन उत्पन्न करता है। पकड़ता है: "form contains errors" (सामान्य), "John Doe" (प्लेसहोल्डर), AI-प्रसन्न उत्सवपूर्ण कॉपी, सामान्य CTA, मृत खाली स्थिति, बेकार त्रुटियाँ।
- **कब उपयोग करें:** संरचना सही है लेकिन शब्द कमज़ोर हैं। "Review the copy", "fix the microcopy", "the error messages are bad", "rewrite this", "tighten the strings", "the buttons sound generic", "this empty state is dead"।
- **कब छोड़ें:** लेआउट समस्याएँ (`/ux-audit` या `/ux-polish` का उपयोग करें)। alt टेक्स्ट जैसी सुलभता-चालित कॉपी समस्याएँ (`/ux-a11y` का उपयोग करें)। बैकएंड या इंफ़्रास्ट्रक्चर।
- **आह्वान:** `/ux-copy src/views/checkout.blade.php`।
- **आउटपुट:** `.ux/last-copy.json` लिखता है, `{location, severity, before, after, notes}` की `strings` ऐरे, साथ ही रूब्रिक + अनुवाद की ज़रूरत वाले लोकल।
- **जोड़ता है:** `/ux-fix` → पुनर्लेखन लागू करें। `/ux-a11y` → कॉपी फ़िक्स के बाद पुनः जाँच करें।

### फ़िक्स और पॉलिश

#### `/ux-fix`: निष्कर्षों को परमाणु कमिट के रूप में लागू करें

- **क्या:** `.ux/` से नवीनतम रिपोर्ट (ऑडिट, कॉपी, a11y, मोशन, या पॉलिश) पढ़ता है, वर्किंग ट्री को मान्य करता है, और सही सब-एजेंट के ज़रिए निष्कर्षों को परमाणु कमिट के रूप में लागू करता है। मूल कमांड को पुनः चलाकर पुनः सत्यापित करता है।
- **कब उपयोग करें:** एक ऑडिट-क्लास कमांड चलाने और निष्कर्षों की समीक्षा करने के बाद। "Fix the findings", "apply the fixes", "run the fix loop", "patch the surface", "make the changes", "go fix it"।
- **कब छोड़ें:** `.ux/` में कोई पूर्व रिपोर्ट नहीं। वर्किंग ट्री गंदा है और उपयोगकर्ता ने stash/commit पर सहमति नहीं दी है। फ़िक्स को डिज़ाइन निर्णय की ज़रूरत है, यांत्रिक अनुप्रयोग की नहीं (रीडिज़ाइन के लिए `/ux-design` का उपयोग करें)।
- **आह्वान:** `/ux-fix` (किस रिपोर्ट को फ़िक्स करना है यह स्वतः पहचानता है) या `/ux-fix --from=last-a11y.json`।
- **आउटपुट:** प्रति निष्कर्ष परमाणु कमिट। मूल कमांड को पुनः चलाता है और `.ux/last-*.json` फ़ाइल अपडेट करता है। एक सारांश प्रिंट करता है।
- **जोड़ता है:** `/ux-next` → कंडक्टर अगली चाल चुनता है।

#### `/ux-polish`: lint, fix, re-lint लूप + AI-स्लॉप का सफ़ाया

- **क्या:** पहले एक स्थानीय HTML फ़ाइल पर डिटरमिनिस्टिक लूप: lint, छह idempotent पॉलिश पास, re-lint, जब तक स्कोर 90 न हो, स्कोर ठहर न जाए, या तीन राउंड न हो जाएँ (`--rounds` सीमा बदलता है)। डिफ़ॉल्ट रूप से लूप का आउटपुट `<file>.evolved.html` में रहता है और मूल फ़ाइल को कभी छुआ नहीं जाता। सिर्फ़ `--loop-only` या `--fix` मूल फ़ाइल को बदलते हैं, साफ़ वर्किंग ट्री की जाँच के बाद, और 65 का गुणवत्ता गेट फ़ेल हुए नतीजे को `--force` के बिना उसकी जगह लेने से रोकता है; `--brand-file` के साथ ब्रांड-वफ़ादारी की न्यूनतम सीमा हर निकास पर लागू रहती है। फिर रुचि वाला पास: स्पेसिंग की लय, पदानुक्रम को धार देना, AI-स्लॉप की पहचान, टोकन की एकरूपता। यह `/ux-lint` का LLM-चालित साथी है, जो रुचि के फ़ैसलों में आपकी समझ का इस्तेमाल करता है। `--loop-only` सिर्फ़ लूप चलाता है; `--no-loop` सिर्फ़ रुचि वाला पास; `--fix` रुचि से जुड़े निष्कर्ष लागू करता है।
- **कब उपयोग करें:** संरचना सही है पर अमल ढीला है। "Polish", "tighten this up", "remove the AI-slop", "make it premium", "make this less AI-looking", "the spacing feels off", "this looks generic", "needs more taste", "improve until score 90+", "make it ship-ready"।
- **कब छोड़ें:** सरफ़ेस में मुख्य कार्यक्षमता नहीं है (पहले वह ठीक करें)। पॉलिश नहीं, रीडिज़ाइन चाहिए (`/ux-design` का उपयोग करें)। कॉपी की समस्याएँ (`/ux-copy` का उपयोग करें)। मोशन की समस्याएँ (`/ux-motion` का उपयोग करें)। a11y की समस्याएँ (`/ux-a11y` का उपयोग करें)।
- **आह्वान:** `/ux-polish src/components/Hero.tsx`, `/ux-polish out/landing.html --css out/landing.css`, `/ux-polish out/landing.html --loop-only --rounds 5`।
- **आउटपुट:** लूप से `<file>.evolved.html` (मूल फ़ाइल की जगह सिर्फ़ `--loop-only` या `--fix` में), `--fix` में अपडेट हुआ कोड, `.ux/last-evolve.json`, `.ux/decisions.jsonl` में एक पंक्ति, और रुचि से जुड़े निष्कर्ष बताने वाला `.ux/last-polish.json`।
- **जोड़ता है:** `/ux-lint` → जाँचें कि पॉलिश टिकी रही। `/ux-a11y` → सुलभता फिर से जाँचें।

### डिस्कवरी और कथा

#### `/ux-research`: अनुसंधान योजना + संश्लेषण

- **क्या:** योजना मोड: साक्षात्कार स्क्रिप्ट, सर्वेक्षण, भर्ती स्क्रीनर लिखता है। संश्लेषण मोड (`--synthesize`): साक्षात्कार, एनालिटिक्स, प्रतिस्पर्धी साइट, A/B परिणाम, सपोर्ट टिकट को सिफ़ारिशों में पचाता है। `research-synthesizer` को डिस्पैच करता है।
- **कब उपयोग करें:** "Plan a research study", "I need interview questions", "design a survey", "how do I recruit users", "user testing plan", "diary study", "preference test", "fake door", "smoke test", "synthesize my interview notes"।
- **कब छोड़ें:** उत्तर पहले से उच्च आत्मविश्वास के साथ ज्ञात है। कम-जोखिम वाले प्रतिवर्ती निर्णय। बैकएंड या इंफ़्रास्ट्रक्चर।
- **आह्वान:** `/ux-research --plan "loyalty wallet adoption in MENA"` या `/ux-research --synthesize interviews/*.md`।
- **आउटपुट:** `.ux/last-research.json` लिखता है, अनुसंधान योजना या संश्लेषित विषय + साक्ष्य + सिफ़ारिशें।
- **जोड़ता है:** `/ux-discover --frame` → निष्कर्षों को फ़्रेम में जोड़ें। `/ux-design` → निष्कर्षों से जेनरेट करें। `/ux-workshop` → रिसर्च को इनपुट बनाकर वर्कशॉप चलाएँ।

#### `/ux-workshop`: 5-चरण डिज़ाइन थिंकिंग वर्कशॉप

- **क्या:** एक डिस्कवरी / डिज़ाइन-थिंकिंग वर्कशॉप को शुरू से अंत तक सुगम बनाता है। पाँच क्रमिक चरण (अन्वेषण → हीट मैप → हितधारक मैप → समाधान स्केच → गेम प्लान)। समय-सीमित। प्रति चरण ठोस आर्टिफ़ैक्ट। एक निर्णय के साथ समाप्त होता है, "दिलचस्प निष्कर्ष" के साथ नहीं।
- **कब उपयोग करें:** असली प्रश्न, असली प्रतिभागी, असली समय बजट। "Run a workshop", "facilitate a discovery", "let's do a design thinking session", "I have stakeholders for an hour, what do we do", "kick off the project"।
- **कब छोड़ें:** ब्रीफ़ पहले से साफ़ और सीमित है। अकेले ब्रेनस्टॉर्म (`/ux-design` या `/ux-discover --frame` का उपयोग करें)। टीम डिस्कवरी में नहीं, अमल के बीच में है।
- **आह्वान:** `/ux-workshop "loyalty wallet pivot" --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" --minutes=90`।
- **आउटपुट:** `.ux/last-workshop.json` लिखता है, गेम प्लान + प्रति-चरण आर्टिफ़ैक्ट।
- **जोड़ता है:** `/ux-design` → गेम प्लान निष्पादित करें। `/ux-research` → वर्कशॉप द्वारा उठाए गए अंतरालों को भरें। `/ux-case-study` → यात्रा प्रकाशित करें।

#### `/ux-case-study`: प्रकाशन योग्य केस स्टडी (Wfrah-संपादकीय प्रारूप)

- **क्या:** शुद्ध मोनोक्रोम एडिटोरियल फ़ॉर्मेट में प्रोजेक्ट केस स्टडी बनाता है: Wfrah टाइपोग्राफ़ी, बारीक रेखा वाले विभाजक, (A) से (G) तक क्रमांकित सेक्शन कोड, द्विभाषी के लिए सुरक्षित लेआउट। एक दस्तावेज़, मार्केटिंग ब्रोशर नहीं। `.ux/last-frame.json`, `.ux/last-workshop.json`, `.ux/last-research.json`, `.ux/last-design.json`, `.ux/last-a11y.json`, `.ux/last-polish.json`, `.ux/last-recommendation.json`, `.ux/last-discovery.json` से पढ़ता है।
- **कब उपयोग करें:** लॉन्च के बाद। एक अलग मील के पत्थर के बाद। "Write a case study", "case study this project", "do the wrap-up doc", "publish this work", "portfolio piece"।
- **कब छोड़ें:** प्रोजेक्ट के पास (A) से (G) तक के सेक्शन भरने लायक डेटा नहीं है। यूज़र केस स्टडी नहीं, मार्केटिंग लैंडिंग चाहता है (`/ux-design` का उपयोग करें)।
- **आह्वान:** `/ux-case-study --format=html --slug=bashiti-loyalty`।
- **आउटपुट:** `case-studies/<slug>.<ext>` + `.ux/last-case-study.json`।
- **जोड़ता है:** टर्मिनल कमांड, आमतौर पर प्रोजेक्ट का अंत।

### कंडक्टर

#### `/ux-next`: वर्कफ़्लो कंडक्टर (केवल-पठनीय)

- **क्या:** हर `.ux/last-*.json` पढ़ता है और सबसे ज़्यादा लीवरेज वाले अगले कमांड का नाम लेता है। एक कंडक्टर, बिल्डर नहीं। केवल पठनीय।
- **कब उपयोग करें:** कमांडों के बीच। "What should I do next", "what's the next move", "decide for me", "where do we go from here"।
- **कब छोड़ें:** `.ux/` में कोई पूर्व रिपोर्ट नहीं। आपके मन में एक विशिष्ट अगला कमांड है।
- **आह्वान:** `/ux-next` (कोई आर्ग नहीं) या `/ux-next --focus=a11y`।
- **आउटपुट:** stdout, अनुशंसित अगला कमांड + तर्क।
- **जोड़ता है:** जो भी कमांड वह चुनता है।

#### `/ux-expert`: परामर्श हुक

- **क्या:** जब एक उपयोगकर्ता वास्तविक जीवन के UX विशेषज्ञ के लिए पूछता है तो प्लगइन निर्माता की संपर्क जानकारी सामने लाता है। संक्षिप्त, सीधा, कोई मार्केटिंग नहीं।
- **कब उपयोग करें:** "Who built this", "I need a UX expert", "do you do consulting", "can I hire someone for this", "is there a human behind this plugin"।
- **कब छोड़ें:** उपयोगकर्ता प्लगइन सुविधाओं के बारे में पूछ रहा है, परामर्श के बारे में नहीं।
- **आह्वान:** `/ux-expert`।
- **आउटपुट:** LinkedIn / ईमेल / रेपो के साथ एक संक्षिप्त संपर्क कार्ड।

### उपनाम, 4.1 में हटाए जाएँगे

3.x की सात कमांड ऊपर की 18 में मिला दी गई हैं। उनके नाम एक और रिलीज़ तक चलते हैं: हर उपनाम बताता है कि वह कहाँ चला गया, फिर उन्हीं आर्ग्युमेंट के साथ नई कमांड चलाता है।

| पुरानी कमांड | अब | टिप्पणी |
|---|---|---|
| `/ux-frame` | `/ux-discover --frame` | वही फ़्रेमिंग ब्लॉक, वही `.ux/last-frame.json` |
| `/ux-recommend` | `/ux-discover --recommend` | `ux_recommend` MCP टूल नहीं बदला |
| `/ux-stats` | `/ux-init --stats` | सिर्फ़ पढ़ने वाला स्नैपशॉट |
| `/ux-evolve` | `/ux-polish --loop-only --rounds 5` | उपनाम पुरानी पाँच राउंड की सीमा रखता है; अकेला `/ux-polish` तीन पर रुकता है |
| `/ux-component` | `/ux-design --component` | वही `.ux/last-component.json` |
| `/ux-dashboard` | `/ux-design --dashboard` | वही `.ux/last-dashboard.json` |
| `/ux-image-to-code` | `/ux-design --extract-only --from-image` | इमेज से बनाने के लिए `--extract-only` हटा दें |

### कमांड चेनिंग ग्राफ़

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

## 5 सब-एजेंट

सब-एजेंट कमांड द्वारा डिस्पैच किए गए भूमिका-विशिष्ट जेनरेटर हैं। वे कभी स्वतंत्र रूप से नहीं चलते; उन्हें `/ux-design`, `/ux-system`, `/ux-fix`, `/ux-research`, आदि बुलाते हैं। हर एजेंट की ज़िम्मेदारी की एक तय सीमा है: वे ब्रीफ़ तय नहीं करते; वे उस पर अमल करते हैं।

### `frontend-engineer`

- **स्वामी:** एंटी-AI-स्लॉप अनुशासन के साथ उत्पादन-ग्रेड फ़्रंटएंड कोड (React, Next.js, Vue, Blade+Alpine, vanilla HTML, Astro)।
- **डिस्पैच करने वाला:** `/ux-design` (पेज, कंपोनेंट, डैशबोर्ड और इमेज मोड), `/ux-fix`।
- **इनपुट:** ब्रीफ़ + रचनात्मक दिशा + टोकन (`.ux/last-recommendation.json` से)।
- **आउटपुट:** कार्यशील कोड जो सामान्य AI आउटपुट से अलग पहचाना जा सकता है। कोई पर्पल ग्रेडिएंट नहीं, कोई सेंटर्ड हीरो नहीं, कोई तीन समान कार्ड नहीं, कोई डिस्प्ले साइज़ पर Inter नहीं, कोई "John Doe" नहीं, कोई इमोजी नहीं, कोई 300ms डिफ़ॉल्ट नहीं।
- **टूल:** `Read, Write, Edit, Bash, Glob, Grep`।

### `motion-engineer`

- **स्वामी:** उत्पादन फ़्रंटएंड कोड में मोशन, Framer Motion, GSAP, CSS एनिमेशन। अवधि, ईज़िंग, कोरियोग्राफ़ी, रिड्यूस्ड-मोशन फ़ॉलबैक, प्रदर्शन अनुशासन।
- **डिस्पैच करने वाला:** `/ux-design` (हर मोड), `/ux-motion --fix`।
- **इनपुट:** मोशन ब्रीफ़ + टोकन + `data/motion-presets.json` से 57 मोशन प्रीसेट।
- **आउटपुट:** मोशन जो अपनी जगह कमाता है। हमेशा `prefers-reduced-motion` फ़ॉलबैक में लिपटा। हमेशा Core Web Vitals के विरुद्ध परीक्षित।
- **टूल:** `Read, Write, Edit, Bash, Glob, Grep`।

### `copy-writer`

- **स्वामी:** शिप होने वाली स्ट्रिंग्स, त्रुटि संदेश, खाली स्थिति, CTA, लोडिंग स्थिति, सफलता संदेश, टोस्ट, हेल्पर टेक्स्ट, फ़ॉर्म लेबल, बटन टेक्स्ट।
- **डिस्पैच करने वाला:** `/ux-copy --fix`, `/ux-design` (हर मोड), `/ux-discover --frame`।
- **इनपुट:** आवाज़ प्रोफ़ाइल (नामित या पेस्ट की गई) + सर्फ़ेस की स्ट्रिंग्स।
- **आउटपुट:** उत्पादन माइक्रोकॉपी एक सर्फ़ेस की हर स्थिति में लगातार लागू ताकि उत्पाद एक उत्पाद की तरह लगे, दस की तरह नहीं। प्रतिबंध: "form contains errors", "John Doe", AI-प्रसन्न उत्सवपूर्ण कॉपी, सामान्य CTA, मृत खाली स्थिति।
- **टूल:** `Read, Write, Edit, Bash, Glob, Grep`।

### `research-synthesizer`

- **स्वामी:** अनुसंधान इनपुट (साक्षात्कार, एनालिटिक्स, प्रतिस्पर्धी साइट, A/B परिणाम, सपोर्ट टिकट) को क्रियाशील डिज़ाइन सिफ़ारिशों में पचाना।
- **डिस्पैच करने वाला:** `/ux-research`, `/ux-workshop`, `/ux-discover --frame`।
- **इनपुट:** कच्चा अनुसंधान, ट्रांसक्रिप्ट, एक्सपोर्ट, प्रतिस्पर्धी URL, सपोर्ट क्लस्टर।
- **आउटपुट:** विषय, साक्ष्य, सिफ़ारिशें। कभी उत्तर डिज़ाइन नहीं करता, डिज़ाइनर को डिज़ाइन करने का आधार देता है।
- **टूल:** `Read, Write, WebFetch, Bash, Glob, Grep`।

### `design-system-architect`

- **स्वामी:** पूर्ण डिज़ाइन सिस्टम, टोकन (रंग, टाइप, स्पेस, मोशन, रेडियस, शैडो), फ़ाउंडेशन डॉक्स, कंपोनेंट कॉन्ट्रैक्ट, डार्क-मोड पेयरिंग, थीमिंग परत।
- **डिस्पैच करने वाला:** `/ux-system`, और कोई सिस्टम न हो तो `/ux-design --component`।
- **इनपुट:** ब्रांड ब्रीफ़ + `.ux/last-recommendation.json` (शैली + पैलेट + टाइप पेयर + मोशन प्रीसेट)।
- **आउटपुट:** एक सुसंगत, मतपूर्ण, उत्पादन-तैयार सिस्टम जिसके विरुद्ध डाउनस्ट्रीम एजेंट मूल बातों को पुनः तय किए बिना निर्माण कर सकें। टोकन JSON, फ़ाउंडेशन MD, कंपोनेंट कॉन्ट्रैक्ट, डार्क-मोड मैपिंग।
- **टूल:** `Read, Write, Edit, Bash, Glob, Grep`।

### सब-एजेंट डिस्पैच प्रोटोकॉल

जब एक कमांड एक सब-एजेंट को डिस्पैच करता है, यह पास करता है:

1. ब्रीफ़ / अनुशंसा (`.ux/` से लोड)।
2. प्रासंगिक मैनिफ़ेस्ट स्लाइस (उदाहरण के लिए, `frontend-engineer` को चयनित शैली + पैलेट + कंपोनेंट मिलते हैं; `motion-engineer` को चयनित मोशन प्रीसेट मिलते हैं)।
3. 171 एंटी-पैटर्न रेलिंग्स (हमेशा सक्रिय)।
4. एक सफलता मानदंड (आर्टिफ़ैक्ट को क्या करना चाहिए)।

सब-एजेंट लौटाते हैं:

1. आर्टिफ़ैक्ट (कोड, डॉक, सिस्टम)।
2. एक तर्क ब्लॉक (ये चयन क्यों)।
3. रेलिंग्स के विरुद्ध एक स्व-जाँच (कौन से नियम सत्यापित किए)।

कॉल करने वाला कमांड फिर पूर्ण घोषित करने से पहले स्वचालित रूप से `/ux-lint` चलाता है।

---

## 11 डेटा मैनिफ़ेस्ट

डेटा परत मस्तिष्क है। हर कमांड इससे पढ़ता है; इंजन इसके पार मर्ज करता है; लिंटर इसके विरुद्ध स्कैन करता है। सभी फ़ाइलें `data/` के तहत रहती हैं और स्कीमा संस्करण के लिए अपनी एंट्री को `{_meta, entries}` में लपेटती हैं।

### `styles.json`: 84 डिज़ाइन शैलियाँ

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 84 |
| `keys per entry` | `id`, `name`, `category`, `philosophy`, `when_to_use`, `when_to_skip`, `tokens`, `references`, `compatible_palettes`, `compatible_type_pairs`, `compatible_motion`, `compatible_industries`, `taste_score` |
| `categories` | Minimalist / Swiss, Brutalist, Editorial, Glassmorphism, Neumorphism, Bento, Skeuomorphic, Industrial, Maximalist, AI-Futurist, MENA-modern, Vaporwave, आदि। |
| `sample entry` | `swiss-international`, "ग्रिड कानून है। टाइप भारी काम करता है। सजावट विफलता है।" |

उपयोग द्वारा: `/ux-discover`, `/ux-system`, `/ux-design`। स्कीमा: [data/SCHEMAS.md](data/SCHEMAS.md)।

### `palettes.json`: 176 रंग पैलेट

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 176 |
| `keys per entry` | `id`, `name`, `mode` (हल्का/गहरा), `tone`, `colors` (canvas, surface, ink, body, muted, primary, primary_active, hairline, success, warning, danger, accent), `wcag_contrast_audit`, `compatible_industries` |
| `tones` | warm, editorial, magazine, clinical, playful, brutalist, monochrome, jewel-tone, MENA-warm, dev-tools-dark, आदि। |
| `sample entry` | `claude-warm-editorial`, हल्का, warm/editorial/magazine, canvas #faf9f5, primary #cc785c |

उपयोग द्वारा: `/ux-discover`, `/ux-system`। AA / AAA पर कंट्रास्ट सत्यापित। स्कीमा: [data/SCHEMAS.md](data/SCHEMAS.md)।

### `type-pairs.json`: 70 टाइप पेयरिंग

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 70 |
| `keys per entry` | `id`, `name`, `display` (परिवार + वज़न + स्रोत + लाइसेंस + URL), `body`, `mono`, `compatible_styles`, `taste_score` |
| `sample entry` | `cormorant-inter-jetbrains`, Cormorant Garamond × Inter × JetBrains Mono |

सभी फ़ैमिली के पास लाइसेंस + स्रोत URL है। उपयोग द्वारा: `/ux-discover`, `/ux-system`।

### `components.json`: 148 कंपोनेंट

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 148 |
| `keys per entry` | `id`, `name`, `category`, `purpose`, `anatomy`, `states`, `tokens_used`, `motion`, `accessibility`, `compatible_styles`, `compatible_industries`, `code_skeleton` |
| `categories` | Navigation, Forms, Data Display, Feedback, Overlays, Layout, Content, Marketing, E-commerce, Auth, Dashboard, Charts, Empty States, Loading States, Error States |
| `sample entry` | `mega-nav-product-grid`, Mega Navigation, Product Grid, 6-भाग एनाटॉमी, 4 स्टेट |

यह हमारी सबसे बड़ी खाई है। कोई अन्य Claude UX प्लगइन एक संरचित कंपोनेंट मैनिफ़ेस्ट नहीं भेजता।

### `industries.json`: 184 इंडस्ट्री नियम

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 184 |
| `keys per entry` | `id`, `name`, `category`, `characteristics`, `audience_signals`, `recommended_styles`, `recommended_palettes`, `recommended_type_pairs`, `recommended_motion`, `regulatory_notes`, `regional_notes` |
| `categories` | Financial Services, Healthcare, Education, E-commerce, SaaS B2B, SaaS B2C, Developer Tools, Media, Gaming, Travel, Real Estate, MENA-specific, आदि। |
| `sample entry` | `fintech-neobank`, उच्च विश्वास, नियामक प्रकटीकरण, बैलेंस/लेनदेन प्राथमिक UI, मोबाइल-पहले दैनिक-उपयोग |

Recommender (`/ux-discover`) द्वारा पहली समानांतर खोज अक्ष के रूप में उपयोग।

### `chart-types.json`: 35 चार्ट प्रकार

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 35 |
| `keys per entry` | `id`, `name`, `category`, `when_to_use`, `when_to_skip`, `encoding`, `accessibility`, `data_shape`, `compatible_styles` |
| `categories` | Comparison, Time Series, Distribution, Composition, Relationship, Flow, Geographic |
| `sample entry` | `bar-vertical`, 4 से 15 असतत श्रेणियों की तुलना करें। x-अक्ष पर स्थिति श्रेणी दिखाती है; ऊँचाई मान दिखाती है। |

`/ux-design --dashboard` और `/ux-design --component` (चार्ट इंस्टेंस) द्वारा उपयोग।

### `tech-stacks.json`: 25 स्टैक

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 25 |
| `keys per entry` | `id`, `name`, `category`, `tier`, `languages`, `ssr`, `rsc`, `compatible_styling`, `scaffold_command`, `compatible_motion`, `gotchas` |
| `tiers` | production, prerelease, experimental |
| `sample entry` | `nextjs-15-app-router`, Next.js 15 (App Router), TS/JS, SSR, RSC, Tailwind 4 / CSS Modules / vanilla-extract / styled-components / panda-css के साथ संगत |

अन्य स्टैक में Astro, SvelteKit, Remix, Nuxt 3, Solid Start, Qwik, Blade+Alpine, Hotwire, Phoenix LiveView, Hydrogen 2025 शामिल हैं।

### `ux-guidelines.json`: 112 नामित UX नियम

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 112 |
| `keys per entry` | `id`, `name`, `category`, `source`, `principle`, `application`, `examples`, `caveats`, `related_laws` |
| `categories` | Decision Cost, Attention, Memory, Motor Control, Visual Perception, Social, Emotional, Form, Error Handling, Onboarding, Empty State, आदि। |
| `sample entry` | `hicks-law`, प्रस्तुत विकल्पों की संख्या के साथ निर्णय समय लघुगणक रूप से बढ़ता है |

`/ux-audit` (6-लेंस स्कोरिंग) और `/ux-critique` (रुचि एंकर) द्वारा उपयोग।

### `motion-presets.json`: 57 मोशन प्रीसेट

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 57 |
| `keys per entry` | `id`, `name`, `category`, `tokens` (duration_ms, easing, transform_from/to, opacity_from/to), `stacks` (framer_motion, gsap, css), `accessibility` (रिड्यूस्ड-मोशन फ़ॉलबैक), `when_to_use` |
| `categories` | Entry, Exit, Hover, Focus, Tap, Loading, Empty, Success, Error, Scroll-linked |
| `sample entry` | `fade-up-12px`, 360ms, `cubic-bezier(0.16, 1, 0.3, 1)`, translateY(12px) → 0, opacity 0 → 1 |

हर प्रीसेट में एक रिड्यूस्ड-मोशन वैरिएंट है। Framer Motion, GSAP, और शुद्ध CSS के लिए स्टैक-तैयार कोड।

### `anti-patterns.json`: 171 नियम

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 171 |
| `keys per entry` | `id`, `name`, `severity` (critical/high/medium/low), `category`, `detection` (प्रकार, पैटर्न, फ़्लैग, दायरा, और कई नियमों में पार्स की गई फ़ाइल पर एक `post` जाँच), `why`, `fix` |
| `categories` | A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) |

पूरी नियम सूची [171 एंटी-AI-स्लॉप नियम](#171-एंटी-ai-स्लॉप-नियम-लिंटर) में है।

### `brands/*.json`: 160 ब्रांड स्पेक

| फ़ील्ड | विवरण |
|---|---|
| `entries` | 160 (साथ ही सभी को सूचीबद्ध करने वाला `_index.json`) |
| `keys per entry` | `id`, `name`, `category`, `voice`, `tokens` (color, type, motion), `design_principles`, `signature_moves`, `anti-moves`, `references` |
| `categories` | Developer Tools (36), Consumer / Lifestyle / Retail (19), Fintech / Crypto (14), Editorial / Media (13), AI / ML Platform (12), Productivity / Collaboration (8), Automotive (8) |

पूरी सूची [160 ब्रांड DESIGN.md स्पेक](#160-ब्रांड-designmd-स्पेक-श्रेणी-के-अनुसार) में।

---

## 171 एंटी-AI-स्लॉप नियम: लिंटर

ux-skill एक डिटरमिनिस्टिक लिंटर के साथ आता है: हर नियम एक पैटर्न है, और कई नियम पार्स किए गए CSS और मार्कअप पर अलग जाँच भी जोड़ते हैं, ताकि कोई मेल सिर्फ़ उसी संदर्भ में गिना जाए जिसका नियम नाम लेता है। **कोई LLM नहीं।** **कोई API नहीं।** **कोई नेटवर्क नहीं।** एक सामान्य Next.js ऐप पर CI में ~200ms में चलता है। `--fail-on high` सेट होने पर Critical / High निष्कर्षों पर non-zero exit करता है।

नियम `data/anti-patterns.json` (v2, पसंदीदा) से आते हैं, और `references/foundations/anti-patterns.md` (v1, bash) फ़ॉलबैक है। दो बाइनरी आती हैं: `bin/ux-lint.py` (Python, तेज़, बढ़ाने योग्य) और `bin/ux-lint.sh` (Bash + perl-PCRE, बिना Python वाले वातावरण के लिए)।

### श्रेणी के अनुसार नियम

सभी 171 नियमों का पूरा कैटलॉग, श्रेणी और फिर गंभीरता के क्रम में, `data/anti-patterns.json` से [अंग्रेज़ी README](README.md#rules-by-category) में बनाया जाता है; वहाँ नियमों के ID और नाम वैसे ही हैं जैसे लिंटर उन्हें प्रिंट करता है। नियम A11y (45), Content (35), Layout (18), Typography (16), Motion (14), Visual (14), Quality (12), Color (10), Performance (5), Depth (2) को कवर करते हैं।

### लिंटर उपयोग

**एक-बार स्कैन:**

```bash
uxskill lint .
# or
python3 bin/ux-lint.py src/
# or
bash bin/ux-lint.sh src/
```

**CI गेट (GitHub Actions):**

```yaml
- name: ux-lint
  run: bash bin/ux-lint.sh --ci --fail-on high
```

**प्री-कमिट हुक:**

```bash
# .git/hooks/pre-commit
#!/usr/bin/env bash
bash bin/ux-lint.sh --staged --fail-on high
```

**आउटपुट (नमूना):**

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

## 160 ब्रांड DESIGN.md स्पेक: श्रेणी के अनुसार

असली ब्रांड। असली डिज़ाइन भाषाएँ। असली DESIGN.md स्पेक, सामान्य पैलेट नहीं। प्लगइन को बताएँ "Stripe की शैली में एक लैंडिंग बनाओ" और यह वास्तविक ब्रांड शब्दावली पढ़ता है: आवाज़ रूब्रिक, रंग टोकन, मोशन सम्मेलन, हस्ताक्षर चालें, एंटी-चालें।

हर ब्रांड एक संरचित JSON (`data/brands/<slug>.json`) और एक गद्य संदर्भ (`references/brands/<slug>.md`) के रूप में भेजा जाता है।

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

### यह क्यों मायने रखता है

अन्य 8 लोकप्रिय Claude UX प्लगइन "modern minimal" या "clean dashboard" जेनरेट करते हैं, एक ही डिफ़ॉल्ट सौंदर्य के संस्करण। ux-skill आपको माँगने देता है **Linear की स्पष्टता**, **Stripe की गंभीरता**, **Apple का संयम**, **Tesla का मोनोलिथ**, **Notion की मित्रता**, **Cursor का ग्रेडिएंट अनुशासन**, **Raycast का हेयरलाइन घनत्व**, **Claude का गर्म संपादकीय**, और इंजन ब्रांड स्पेक से सही टोकन, आवाज़, मोशन सम्मेलन, और हस्ताक्षर चालें खींचता है।

---

## MCP सर्वर: असममित चाल

ux-skill एक **Model Context Protocol सर्वर** भेजता है। `ux-mcp` चलाएँ और इंजन लंबे समय तक चलने वाली एक stdio प्रक्रिया बन जाता है, जिसे कोई भी MCP-सक्षम होस्ट (Claude Desktop, Cursor, Windsurf, सामान्य एजेंट) बुला सकता है। 25 टूल: `ux_recommend`, `ux_system_detect`, `ux_lint`, `ux_styles`, `ux_palettes`, `ux_type_pairs`, `ux_components`, `ux_industries`, `ux_motion_presets`, `ux_anti_patterns`, `ux_brands`, `ux_landing_patterns`, `ux_persist_save`, `ux_persist_load`, `ux_stats`, `ux_image_extract`, `ux_synthesize`, `ux_decisions_query`, `ux_decisions_stats`, `ux_system_build`, `ux_system_import`, `ux_system_enhance`, `ux_system_extend`, `ux_system_export`, `ux_contracts_check`। वही Python हैंडलर जो स्लैश कमांड इस्तेमाल करती हैं; वही डेटा मैनिफ़ेस्ट; वही डिटरमिनिस्टिक recommender।

**यह असममित चाल क्यों है:** शीर्ष आठ Claude UX स्किल्स (ui-ux-pro-max-skill, open-design, taste-skill, huashu-design, stitch, nothing-design, hallmark, material-3) में से कोई भी MCP सर्वर नहीं भेजता। वे Claude Code के प्लगइन रनटाइम के अंदर बंद हैं। ux-skill MCP बोलने वाले किसी भी होस्ट से पहुँच योग्य है, उन एजेंटों सहित जिन्होंने कभी Claude Code प्लगइन के बारे में नहीं सुना।

```bash
pip install 'uxskill[mcp]'             # mcp is an opt-in extra
ux-mcp                                  # stdio JSON-RPC server starts
```

अपने क्लाइंट को `ux-mcp` बाइनरी की ओर इंगित करें। पूर्ण टूल डॉक्स, JSON उदाहरण, और Claude Desktop, Cursor, और Windsurf के लिए प्रति-क्लाइंट कॉन्फ़िग [docs/mcp.html](docs/mcp.html) पर और `commands/ux-mcp.md` में रहते हैं।

---

## 17-IDE इंस्टॉलर

`uxskill init` (या Claude Code के अंदर `/ux-init`) स्वतः पता लगाता है कि आप कौन सा IDE उपयोग कर रहे हैं और सही आर्टिफ़ैक्ट लिखता है। एक ही Python इंजन। एक ही अनुशंसाएँ। प्रति IDE अलग गोंद।

| IDE / टूल | पहचान संकेत | इंस्टॉल किया गया आर्टिफ़ैक्ट |
|---|---|---|
| Claude Code | `.claude/` या `CLAUDE.md` | `.claude-plugin/plugin.json` पर प्लगइन मैनिफ़ेस्ट + सभी 18 कमांड (और 7 उपनाम) + सभी 5 सब-एजेंट |
| Cursor | `.cursor/` या `.cursorrules` | `.cursorrules` प्रॉम्प्ट हेडर इंजन की ओर इशारा करते हुए |
| Windsurf | `.windsurf/` या `.windsurfrules` | `.windsurfrules` समान प्रॉम्प्ट हेडर के साथ |
| GitHub Copilot | `.github/copilot-instructions.md` या `.vscode/` | `.github/copilot-instructions.md` |
| Gemini CLI | `GEMINI.md` | `GEMINI.md` |
| Codex | `AGENTS.md` | `AGENTS.md` |
| Kiro | `.kiro/` | `.kiro/instructions.md` |
| Cline | `.cline/` | `.cline/instructions.md` |
| Continue | `.continue/` | `.continue/config.json` पैच |
| Aider | `.aider.conf.yml` | `.aider.conf.yml` + `AIDER.md` |
| Zed | `.zed/` | `.zed/instructions.md` |
| JetBrains AI | `.jetbrains-ai/` या `.idea/` | `.jetbrains-ai/instructions.md` |
| Pieces | `.pieces/` | `.pieces/instructions.md` |
| Tabby | `.tabby/` | `.tabby/instructions.md` |
| Tabnine | `.tabnine/` | `.tabnine/instructions.md` |
| CodeWhisperer | `.aws-codewhisperer/` | `.aws-codewhisperer/instructions.md` |
| Roo Cline | `.roo/` | `.roo/instructions.md` |

हर IDE में, टर्मिनल से वही `uxskill recommend` / `uxskill lint` / `uxskill stats` CLI कमांड काम करते हैं। Python इंजन सत्य का स्रोत है; IDE आर्टिफ़ैक्ट पतले प्रॉम्प्ट-हेडर हैं जो इसमें मार्ग बनाते हैं।

---

## उपयोग के मामले: ठोस परिदृश्य

आठ असली परिदृश्य। अपनी स्थिति के सबसे करीब वाला चुनें और आह्वान को अनुकूलित करें।

### 1. Cursor में फ़िनटेक डैशबोर्ड बनाना

आप एक MENA neobank डैशबोर्ड पर काम कर रहे Cursor में हैं। आप प्लगइन इंस्टॉल करते हैं और डिस्कवरी, अनुशंसा, फिर डैशबोर्ड जेनरेशन चलाते हैं।

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

फिर Cursor में पूछें: *"Generate the dashboard surface using the recommendation in .ux/last-recommendation.json"*। Cursor `.cursorrules` हेडर पढ़ता है, अनुशंसा लोड करता है, स्पष्ट बाधाओं के साथ एक डैशबोर्ड जेनरेशन डिस्पैच करता है।

### 2. Claude Code में Stripe-शैली लैंडिंग जेनरेट करना

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

### 3. CI में AI स्लॉप के लिए मौजूदा कोड का ऑडिट

आपने दो हफ़्ते पहले एक Next.js ऐप शिप किया। आप हर PR पर AI फ़िंगरप्रिंट के विरुद्ध एक कठोर मंज़िल चाहते हैं।

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

PR जो purple-to-blue ग्रेडिएंट, 96px पर Inter, "John Doe" टेस्टीमोनियल, या emoji-as-icons लाते हैं CI में फ़ेल हो जाते हैं। कोई LLM लागत नहीं। ~200ms।

### 4. एक मौजूदा सर्फ़ेस को पॉलिश करना जो "AI-जनरेटेड लगता है"

आपको एक React ऐप विरासत में मिला जो हर दूसरी AI-जनरेटेड SaaS साइट जैसा दिखता है। आप चाहते हैं कि यह वैसा न दिखे।

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

तीन कमांड, एक पॉलिश की हुई सर्फ़ेस, प्रति फ़िक्स परमाणु कमिट।

### 5. Linear-शैली कमांड पैलेट डिज़ाइन करना

```
/ux-design --component command-palette --brief="Linear-style, dark, monospace shortcuts, recent items first"
> [reads data/brands/linear.app.json for tokens + signature moves]
> [reads data/components.json for the command-palette anatomy + states]
> [dispatches frontend-engineer with explicit Linear spec]
```

जेनरेट किया गया कंपोनेंट Linear के वास्तविक रंग टोकन, टाइप स्टैक, मोशन सम्मेलन, हेयरलाइन घनत्व का उपयोग करता है, "सामान्य डार्क UI" नहीं।

### 6. हितधारकों के साथ 90 मिनट का डिज़ाइन थिंकिंग वर्कशॉप चलाना

आपके पास 90 मिनट के लिए 5 लोगों का एक कमरा है। आप चाहते हैं कि वे एक गेम प्लान के साथ चले जाएँ, न कि एक वाइब के साथ।

```
/ux-workshop "loyalty wallet pivot" \
  --participants="2 PMs, 1 designer, 1 eng lead, 1 customer rep" \
  --minutes=90
```

प्लगइन पाँच चरणों (अन्वेषण → हीट मैप → हितधारक मैप → समाधान स्केच → गेम प्लान) को शुरू से अंत तक सुगम बनाता है, समय-सीमित, प्रति-चरण ठोस आर्टिफ़ैक्ट के साथ। आउटपुट `.ux/last-workshop.json` है, गेम प्लान, न कि केवल "दिलचस्प निष्कर्ष"।

### 7. लॉन्च के बाद एक प्रकाशन योग्य केस स्टडी लिखना

आपने लॉयल्टी वॉलेट शिप किया। आप एक पोर्टफ़ोलियो पीस चाहते हैं।

```
/ux-case-study --format=html --slug=bashiti-loyalty
> [reads .ux/last-frame.json, last-workshop.json, last-research.json, last-design.json, last-a11y.json, last-polish.json, last-recommendation.json, last-discovery.json]
> [generates Wfrah-editorial case study with numbered (A)-(G) sections, hairline separators, bilingual-safe layout]
> [writes case-studies/bashiti-loyalty.html]
```

केस स्टडी एक तैयार, प्रकाशन योग्य आर्टिफ़ैक्ट है, ड्राफ़्ट नहीं। शुद्ध मोनोक्रोम, संपादकीय टाइपोग्राफ़ी, आपके पोर्टफ़ोलियो पर शिप करने के लिए तैयार।

### 8. एक गैर-AI संदर्भ में डिस्कवरी चलाना (बस संरचित इनटेक)

आप एक प्रोजेक्ट का दायरा कर रहे हैं। आपको अभी अनुशंसा की ज़रूरत नहीं है, आपको एक संरचित ब्रीफ़ चाहिए।

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

आप JSON को अपनी टीम को सौंप सकते हैं, Notion डॉक में पेस्ट कर सकते हैं, या इसे एक अलग AI टूल में फ़ीड कर सकते हैं। ux-skill एक इंजन होने के अलावा एक संरचित इनटेक टूल भी है।

### 9. MASTER.md दृढ़ता: आपके डिज़ाइन निर्णय, रेपो में

`/ux-discover` (या `/ux-discover --recommend`) के बाद, चुनी गई स्टाइल + पैलेट + टाइप + मोशन + कंपोनेंट + ब्रांड उदाहरण + रेलिंग्स को एक पढ़ने में आसान Markdown फ़ाइल के रूप में सहेजें, जिसकी आपकी टीम समीक्षा कर सके, diff देख सके और वर्ज़न कंट्रोल में रख सके।

```bash
python3 -m engine.cli.main persist save --project-root .
```

`.ux/design-system/MASTER.md` (YAML फ़्रंटमैटर + बॉडी) और `persist save-page` के ज़रिए प्रति जेनरेट की गई सर्फ़ेस `.ux/design-system/pages/<name>.md` लिखता है। बेकार, एक ही इनपुट बाइट-समान आउटपुट देता है, इसलिए अपरिवर्तित स्थिति पर पुनः चलाना git में no-op है।

---

## विकल्पों की तुलना में

संक्षिप्त सारांश तालिका। पूरी टेबल-दर-टेबल तुलना [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) पर है।

| आयाम | ux-skill | ui-ux-pro-max | open-design | taste-skill | huashu-design | stitch-skills | nothing-design | hallmark | material-3 |
|---|---|---|---|---|---|---|---|---|---|
| स्लैश कमांड | **18** | 1 | 19 | 1 | 1 | कई | 1 | 1 | 1 |
| कंपोनेंट | **148** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | (MD3) |
| मोशन प्रीसेट | **57** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ब्रांड स्पेक | **160** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| एंटी-पैटर्न नियम | **171** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| CI-सेफ़ डिटरमिनिस्टिक लिंटर | **हाँ** | नहीं | नहीं | नहीं | नहीं | नहीं | नहीं | नहीं | नहीं |
| समर्थित IDE | **17** | 18 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| डिस्कवरी गेट | **10 फ़ील्ड** | अंतर्निहित | अंतर्निहित | अंतर्निहित | अंतर्निहित | अंतर्निहित | अंतर्निहित | अंतर्निहित | अंतर्निहित |
| `.ux/` स्टेट चेन | **हाँ** | नहीं | नहीं | नहीं | नहीं | नहीं | नहीं | नहीं | नहीं |
| स्टार (2026-05-28) | 14 | 83,958 | 54,406 | 25,202 | 15,455 | 5,762 | 2,391 | 2,164 | 955 |

### ईमानदार आकलन

- **ui-ux-pro-max** जागरूकता पर बड़ा है, 18 IDE भेजता है, अपने CSV पर BM25-शैली खोज है। यह एक कंपोनेंट मैनिफ़ेस्ट, मोशन मैनिफ़ेस्ट, ब्रांड लाइब्रेरी, या डिटरमिनिस्टिक लिंटर नहीं भेजता।
- **open-design** के पास 19 स्किल + प्रीव्यू है लेकिन केवल Claude Code समर्थन और कोई एंटी-स्लॉप परत नहीं।
- **hallmark** भावना में सबसे करीब है (वह भी एंटी-स्लॉप) लेकिन एक एकल स्किल है, कोई इंजन नहीं, कोई मैनिफ़ेस्ट नहीं, कोई जुड़े कमांड नहीं।
- **material-3-skill** उत्कृष्ट है अगर आप विशेष रूप से Material Design 3 चाहते हैं। हम MD3 पर प्रतिस्पर्धा नहीं करते।

प्रति आयाम पूर्ण विवरण के लिए, [compare.html](https://uxskill.laithjunaidy.com/compare.html) देखें।

---

## रोडमैप

आगे, बिना किसी तय रिलीज़ के:

- **Figma स्टाइल**: छाया के लिए इफ़ेक्ट स्टाइल, ग्रिड स्टाइल, और फ़ील्ड वेरिएबल से बँधे टेक्स्ट स्टाइल, एक लाइव फ़ाइल पर लिखे गए।
- **कंपोनेंट मैपिंग**: Figma कंपोनेंट और उसके वेरिएंट को कोड कंपोनेंट और उसके props से जोड़ना, हैंडऑफ़ के दौरान बरकरार।
- **लाइव साइट इम्पोर्टर**: किसी प्रकाशित साइट का असल में रेंडर हुआ सिस्टम पढ़ना, फ़ाइल इम्पोर्टरों के साथ।
- **बने हुए सिस्टम के लिए डॉक्स पेज**: उसके टोकन, रोल और कॉन्ट्रैक्ट का इंसानों के लिए दृश्य।

और भी खुले काम:

- **सुरक्षित रीराइट के लिए `uxskill lint --fix`**: यांत्रिक रूप से ठीक होने वाले निष्कर्षों के लिए (button-no-type, img-no-alt खाली स्ट्रिंग, console-log-leak हटाना)।
- **VS Code एक्सटेंशन** जो लिंट निष्कर्ष इनलाइन दिखाए।
- छह स्टैक में **प्रति-कंपोनेंट कोड आउटपुट** (Next.js + React, Vue 3 + Nuxt, SvelteKit, Astro, Blade + Alpine, वनीला HTML/CSS)।
- **ब्रांड स्पेक मार्केटप्लेस**: कम्युनिटी के ब्रांड स्पेक प्रकाशित करना और खोजना।
- **कस्टम एंटी-पैटर्न नियम**: प्रोजेक्ट `data/anti-patterns.local.json` में जो नियम तय करते हैं, उनकी खोज और साझा करना।
- **`uxskill plan`**: सिर्फ़ एक सरफ़ेस नहीं, एक ब्रीफ़ से कई पेज वाली साइट की योजना।

---

## योगदान

इश्यू और PR का स्वागत है। तीन उच्च-लीवरेज क्षेत्र:

### एक एंटी-पैटर्न नियम जोड़ें

1. `data/anti-patterns.json` संपादित करें, `id`, `name`, `severity`, `category`, `detection.pattern`, `detection.flags`, `detection.scope`, `evidence_template`, `fix`, `references` के साथ एक एंट्री जोड़ें।
2. `tests/linter/` में एक परीक्षण जोड़ें, एक फ़ाइल जो नियम को ट्रिगर करती है, एक जो नहीं करती।
3. `uxskill lint tests/linter/should-trigger/<rule>.tsx` चलाएँ, पुष्टि करें कि यह आग लगाता है। `tests/linter/should-not-trigger/<rule>.tsx` पर चलाएँ, पुष्टि करें कि यह नहीं करता।
4. एक PR खोलें।

### एक ब्रांड स्पेक जोड़ें

1. `id`, `name`, `category`, `voice`, `tokens`, `design_principles`, `signature_moves`, `anti-moves`, `references` के साथ `data/brands/<slug>.json` बनाएँ।
2. संगत गद्य `references/brands/<slug>.md` पर जोड़ें।
3. `data/brands/_index.json` में पंजीकृत करें।
4. एक PR खोलें। स्पेक प्राथमिक-स्रोत संदर्भों द्वारा समर्थित होना चाहिए (ब्रांड का वास्तविक उत्पाद, सार्वजनिक डिज़ाइन सिस्टम, या DESIGN.md अगर वे एक प्रकाशित करते हैं)।

### एक मोशन प्रीसेट जोड़ें

1. `data/motion-presets.json` संपादित करें, `id`, `name`, `category`, `tokens`, `stacks` (framer_motion, gsap, css), `accessibility.reduced_motion_fallback`, `when_to_use` के साथ एक एंट्री जोड़ें।
2. प्रीसेट के पास एक रिड्यूस्ड-मोशन वैरिएंट होना चाहिए। कोई अपवाद नहीं।
3. एक PR खोलें।

### प्रक्रिया

- पूर्ण प्रक्रिया के लिए [CONTRIBUTING.md](CONTRIBUTING.md) पढ़ें।
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) पढ़ें।
- नए नियम और ब्रांड स्पेक की समीक्षा की जाती है: प्राथमिक-स्रोत आधार, एक ही प्रोजेक्ट में ओवरफ़िट नहीं, किसी भी डेटा में कोई इमोजी नहीं, जहाँ लागू हो वहाँ RTL-सुरक्षित व्यवहार।

---

## लाइसेंस, लेखक, आभार

### लाइसेंस

MIT। इसे उपयोग करें, फ़ोर्क करें, इस पर निर्माण करें। अगर यह आपको AI स्लॉप शिप करने से बचाता है, रेपो को स्टार करें, यह इसका समर्थन करने का सबसे सस्ता तरीका है।

### लेखक

**Laith Aljunaidy**: [Dot](https://thedotwallet.com) के एकल संस्थापक, एक MENA-पहले लॉयल्टी प्लेटफ़ॉर्म। ux-skill बना रहे हैं ताकि AI-जनरेटेड फ़्रंटएंड सब एक जैसा न दिखे।

- LinkedIn: [linkedin.com/in/laithaljunaidy](https://www.linkedin.com/in/laithaljunaidy/)
- ईमेल: laith.aljunaidy.laith@gmail.com
- रेपो: [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill)
- साइट: [uxskill.laithjunaidy.com](https://uxskill.laithjunaidy.com)
- PyPI: [pypi.org/project/uxskill](https://pypi.org/project/uxskill/)
- npm: [npmjs.com/package/uxskill](https://www.npmjs.com/package/uxskill)

### आभार

- Anthropic की टीम को Claude Code और skill / plugin आर्किटेक्चर के लिए जिसने इसे वितरण योग्य बनाया।
- Nielsen Norman Group, Laws of UX (lawsofux.com), और UX अनुसंधान समुदाय जिनका काम `data/ux-guidelines.json` को सूचित करता है।
- `data/brands/` में सूचीबद्ध हर ब्रांड, उनकी सार्वजनिक डिज़ाइन प्रणालियाँ ब्रांड स्पेक के लिए सत्य का स्रोत हैं।
- मूल v1 योगदानकर्ता: एक सिंगल-शॉट Claude skill जो v2 Python इंजन के लिए बीज बना।
- 8 लोकप्रिय Claude UX प्लगइन जिनसे हमने तुलना की, उन्होंने मानदंड उठाया; यह हमारा उत्तर है।

---

**ux-skill** · **v4.0.0b2** · इसलिए बनाया गया ताकि Claude Code, Cursor, Windsurf, और हर दूसरा AI कोडिंग टूल फ़्रंटएंड आउटपुट करे जो AI-जनरेटेड के रूप में न पढ़ा जाए।

> [github.com/Laith0003/ux-skill](https://github.com/Laith0003/ux-skill) पर रेपो को स्टार करें · `pip install uxskill` या `npx uxskill init` के ज़रिए इंस्टॉल करें · [uxskill.laithjunaidy.com/compare.html](https://uxskill.laithjunaidy.com/compare.html) पर तुलना देखें
