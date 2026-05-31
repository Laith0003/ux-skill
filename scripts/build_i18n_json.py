"""Build scripts/i18n-strings.json for the v3.0 homepage.

Run: python3 scripts/build_i18n_json.py

Translations target docs/index.html VERBATIM (HTML entities preserved).
Brand names, code, file paths stay in English.
"""
import json
from pathlib import Path
from collections import OrderedDict

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "i18n-strings.json"

LANGS = OrderedDict([
    ("en",    {"name": "English",          "dir": "ltr", "html_lang": "en"}),
    ("zh-CN", {"name": "简体中文",            "dir": "ltr", "html_lang": "zh-CN"}),
    ("zh-TW", {"name": "繁體中文",            "dir": "ltr", "html_lang": "zh-TW"}),
    ("ja",    {"name": "日本語",              "dir": "ltr", "html_lang": "ja"}),
    ("ko",    {"name": "한국어",              "dir": "ltr", "html_lang": "ko"}),
    ("hi",    {"name": "हिन्दी",           "dir": "ltr", "html_lang": "hi"}),
    ("id",    {"name": "Bahasa Indonesia", "dir": "ltr", "html_lang": "id"}),
    ("vi",    {"name": "Tiếng Việt",       "dir": "ltr", "html_lang": "vi"}),
    ("th",    {"name": "ไทย",               "dir": "ltr", "html_lang": "th"}),
    ("ar",    {"name": "العربية",          "dir": "rtl", "html_lang": "ar"}),
    ("es",    {"name": "Español",          "dir": "ltr", "html_lang": "es"}),
    ("fr",    {"name": "Français",         "dir": "ltr", "html_lang": "fr"}),
    ("de",    {"name": "Deutsch",          "dir": "ltr", "html_lang": "de"}),
    ("pt-BR", {"name": "Português",        "dir": "ltr", "html_lang": "pt-BR"}),
    ("ru",    {"name": "Русский",          "dir": "ltr", "html_lang": "ru"}),
    ("tr",    {"name": "Türkçe",           "dir": "ltr", "html_lang": "tr"}),
    ("it",    {"name": "Italiano",         "dir": "ltr", "html_lang": "it"}),
])

LANG_ORDER = list(LANGS.keys())


def k(en, **translations):
    """Build a key dict from en + per-locale translations."""
    out = {"en": en}
    for code in LANG_ORDER[1:]:  # skip en
        out[code] = translations.get(code, en)
    return out


STRINGS = OrderedDict()

# ============ TITLE + META ============
STRINGS["page_title"] = k(
    "uxskill — v3.0 The Brain. 7-axis design synthesizer for AI coding.",
    **{
        "zh-CN": "uxskill — v3.0 The Brain。AI 编程的 7 轴设计合成器。",
        "zh-TW": "uxskill — v3.0 The Brain。AI 編程的 7 軸設計合成器。",
        "ja": "uxskill — v3.0 The Brain。AI コーディングのための 7 軸デザイン合成器。",
        "ko": "uxskill — v3.0 The Brain. AI 코딩을 위한 7축 디자인 신디사이저.",
        "hi": "uxskill — v3.0 The Brain। AI कोडिंग के लिए 7-अक्ष डिज़ाइन सिंथेसाइज़र।",
        "id": "uxskill — v3.0 The Brain. Synthesizer desain 7-aksis untuk coding AI.",
        "vi": "uxskill — v3.0 The Brain. Bộ tổng hợp thiết kế 7 trục cho AI coding.",
        "th": "uxskill — v3.0 The Brain · ตัวสังเคราะห์ดีไซน์ 7 แกนสำหรับ AI coding",
        "ar": "uxskill — v3.0 The Brain · مولّد تصميم سباعي المحاور لأدوات البرمجة بالذكاء الاصطناعي",
        "es": "uxskill — v3.0 The Brain. Sintetizador de diseño de 7 ejes para coding con IA.",
        "fr": "uxskill — v3.0 The Brain. Synthétiseur de design à 7 axes pour le codage IA.",
        "de": "uxskill — v3.0 The Brain. 7-Achsen-Design-Synthesizer für KI-Coding.",
        "pt-BR": "uxskill — v3.0 The Brain. Sintetizador de design de 7 eixos para coding com IA.",
        "ru": "uxskill — v3.0 The Brain. Семиосный дизайн-синтезатор для AI-кодинга.",
        "tr": "uxskill — v3.0 The Brain. AI kodlama için 7 eksenli tasarım sentezleyici.",
        "it": "uxskill — v3.0 The Brain. Sintetizzatore di design a 7 assi per coding con AI.",
    }
)

STRINGS["meta_description"] = k(
    "v3.0.0 stable — The Brain. 1,243 structured entries + 160 brand specs + 152 anti-pattern rules feed a 7-axis synthesizer that compiles a novel design language per brief. The recommender re-ranks from a local decisions ledger you can see. Runs in Claude Code, Cursor, Windsurf, and 14 more IDEs. Offline. Deterministic. No LLM. No telemetry.",
    **{
        "zh-CN": "v3.0.0 正式版 — The Brain。1,243 条结构化数据 + 160 个品牌规范 + 145 条反模式规则,共同驱动 7 轴合成器,为每个简报编译全新的设计语言。推荐器基于本地可见的决策账本重新排序。在 Claude Code、Cursor、Windsurf 等 17 个 IDE 中运行。离线、确定性、无 LLM、无遥测。",
        "zh-TW": "v3.0.0 正式版 — The Brain。1,243 條結構化資料 + 160 個品牌規範 + 145 條反模式規則,共同驅動 7 軸合成器,為每份簡報編譯全新的設計語言。推薦器基於本地可見的決策帳本重新排序。在 Claude Code、Cursor、Windsurf 等 17 個 IDE 中執行。離線、確定性、無 LLM、無遙測。",
        "ja": "v3.0.0 安定版 — The Brain。1,243 件の構造化エントリ + 160 のブランド仕様 + 145 のアンチパターン規則が 7 軸合成器を駆動し、ブリーフごとに新しいデザイン言語を生成。レコメンダーはローカルの決定台帳を参照して再ランク付け。Claude Code、Cursor、Windsurf など 17 IDE で動作。オフライン、決定論的、LLM 不使用、テレメトリなし。",
        "ko": "v3.0.0 안정판 — The Brain. 1,243개의 구조화된 항목 + 160개의 브랜드 사양 + 145개의 안티패턴 규칙이 7축 신디사이저를 구동하여 브리프마다 새로운 디자인 언어를 컴파일. 추천기는 로컬에서 확인 가능한 결정 원장을 기반으로 재순위. Claude Code, Cursor, Windsurf 등 17개 IDE 지원. 오프라인, 결정론적, LLM 미사용, 텔레메트리 없음.",
        "hi": "v3.0.0 स्थिर — The Brain। 1,243 संरचित प्रविष्टियाँ + 160 ब्रांड स्पेक्स + 145 एंटी-पैटर्न नियम 7-अक्ष सिंथेसाइज़र को चलाते हैं जो हर brief के लिए नई डिज़ाइन भाषा कंपाइल करता है। recommender एक स्थानीय decisions ledger से रैंकिंग बदलता है जिसे आप देख सकते हैं। Claude Code, Cursor, Windsurf सहित 17 IDE में चलता है। ऑफ़लाइन, deterministic, कोई LLM नहीं, कोई टेलीमेट्री नहीं।",
        "id": "v3.0.0 stabil — The Brain. 1.182 entri terstruktur + 160 spec brand + 145 aturan anti-pola memberi makan synthesizer 7-aksis yang mengompilasi bahasa desain baru per brief. Recommender me-rank ulang dari decisions ledger lokal yang bisa Anda lihat. Berjalan di Claude Code, Cursor, Windsurf, dan 14 IDE lainnya. Offline. Deterministik. Tanpa LLM. Tanpa telemetri.",
        "vi": "v3.0.0 ổn định — The Brain. 1.182 mục có cấu trúc + 160 spec thương hiệu + 145 quy tắc chống mẫu nuôi một synthesizer 7 trục biên dịch ngôn ngữ thiết kế mới cho mỗi brief. Recommender xếp hạng lại từ decisions ledger cục bộ mà bạn có thể xem. Chạy trong Claude Code, Cursor, Windsurf và 14 IDE khác. Ngoại tuyến. Xác định. Không LLM. Không telemetry.",
        "th": "v3.0.0 stable — The Brain · 1,243 รายการที่มีโครงสร้าง + 160 brand specs + 145 กฎ anti-pattern ป้อนให้ synthesizer 7 แกน คอมไพล์ภาษาออกแบบใหม่ต่อ brief · recommender จัดอันดับใหม่จาก decisions ledger บนเครื่อง · ทำงานใน Claude Code, Cursor, Windsurf และอีก 14 IDE · ออฟไลน์ · deterministic · ไม่มี LLM · ไม่มี telemetry",
        "ar": "v3.0.0 مستقرّة — The Brain · 1,243 إدخالًا منظّمًا + 160 من مواصفات العلامات + 145 قاعدة مضادّة للأنماط تُغذّي مولّدًا سباعي المحاور يَبني لغة تصميم جديدة لكلّ ملخّص · يعيد المُوصِّي ترتيبه استنادًا إلى سجلّ قرارات محلّيّ يمكنك رؤيته · يعمل داخل Claude Code وCursor وWindsurf و14 محرّر أكواد آخر · بلا اتصال، حتميّ، بلا نموذج لغوي ضخم، بلا تتبّع.",
        "es": "v3.0.0 estable — The Brain. 1.182 entradas estructuradas + 160 specs de marca + 145 reglas anti-patrón alimentan un sintetizador de 7 ejes que compila un lenguaje de diseño nuevo por brief. El recomendador rerankea desde un ledger local de decisiones que puedes ver. Corre en Claude Code, Cursor, Windsurf y 14 IDEs más. Offline. Determinístico. Sin LLM. Sin telemetría.",
        "fr": "v3.0.0 stable — The Brain. 1 182 entrées structurées + 160 specs de marque + 145 règles anti-pattern alimentent un synthétiseur à 7 axes qui compile un langage de design inédit par brief. Le recommandeur reclasse via un ledger local de décisions que vous pouvez lire. Tourne dans Claude Code, Cursor, Windsurf et 14 autres IDE. Hors-ligne. Déterministe. Sans LLM. Sans télémétrie.",
        "de": "v3.0.0 stabil — The Brain. 1.182 strukturierte Einträge + 160 Brand-Specs + 145 Anti-Pattern-Regeln speisen einen 7-Achsen-Synthesizer, der pro Brief eine neue Design-Sprache kompiliert. Der Recommender ranked aus einem lokalen Decisions-Ledger neu, das Sie sehen können. Läuft in Claude Code, Cursor, Windsurf und 14 weiteren IDEs. Offline. Deterministisch. Ohne LLM. Ohne Telemetrie.",
        "pt-BR": "v3.0.0 estável — The Brain. 1.182 entradas estruturadas + 160 specs de marca + 145 regras anti-padrão alimentam um sintetizador de 7 eixos que compila uma linguagem de design nova por brief. O recomendador re-ranqueia a partir de um ledger local de decisões que você pode ver. Roda em Claude Code, Cursor, Windsurf e mais 14 IDEs. Offline. Determinístico. Sem LLM. Sem telemetria.",
        "ru": "v3.0.0 stable — The Brain. 1 182 структурированных записи + 160 brand-спецификаций + 152 anti-pattern правил питают семиосный синтезатор, который компилирует новый дизайн-язык под каждый бриф. Рекомендатель пере-ранжирует по локальному журналу решений, который вы можете прочитать. Работает в Claude Code, Cursor, Windsurf и 14 других IDE. Offline. Детерминированно. Без LLM. Без телеметрии.",
        "tr": "v3.0.0 kararlı — The Brain. 1.182 yapılandırılmış giriş + 160 marka spec + 152 anti-pattern kuralı, her brief için yepyeni bir tasarım dili derleyen 7 eksenli bir sentezleyiciyi besler. Önerici, görebileceğiniz yerel decisions ledger'dan yeniden sıralar. Claude Code, Cursor, Windsurf ve 14 IDE'de çalışır. Çevrimdışı. Deterministik. LLM yok. Telemetri yok.",
        "it": "v3.0.0 stabile — The Brain. 1.182 voci strutturate + 160 spec brand + 145 regole anti-pattern alimentano un sintetizzatore a 7 assi che compila un linguaggio di design nuovo per ogni brief. Il recommender ri-classifica da un ledger locale di decisioni che puoi leggere. Funziona in Claude Code, Cursor, Windsurf e altri 14 IDE. Offline. Deterministico. Senza LLM. Senza telemetria.",
    }
)

# ============ NAV ============
STRINGS["nav_brands"] = k("Brands",
    **{"zh-CN":"品牌","zh-TW":"品牌","ja":"ブランド","ko":"브랜드","hi":"ब्रांड",
       "id":"Brand","vi":"Thương hiệu","th":"แบรนด์","ar":"العلامات",
       "es":"Marcas","fr":"Marques","de":"Marken","pt-BR":"Marcas","ru":"Бренды","tr":"Markalar","it":"Brand"})

STRINGS["nav_anti_patterns"] = k("Anti-patterns",
    **{"zh-CN":"反模式","zh-TW":"反模式","ja":"アンチパターン","ko":"안티패턴","hi":"एंटी-पैटर्न",
       "id":"Anti-pola","vi":"Chống mẫu","th":"แอนตี้แพทเทิร์น","ar":"الأنماط المضادّة",
       "es":"Anti-patrones","fr":"Anti-patterns","de":"Anti-Patterns","pt-BR":"Anti-padrões","ru":"Анти-паттерны","tr":"Anti-pattern'lar","it":"Anti-pattern"})

STRINGS["nav_commands"] = k("Commands",
    **{"zh-CN":"命令","zh-TW":"命令","ja":"コマンド","ko":"명령어","hi":"कमांड",
       "id":"Perintah","vi":"Lệnh","th":"คำสั่ง","ar":"الأوامر",
       "es":"Comandos","fr":"Commandes","de":"Befehle","pt-BR":"Comandos","ru":"Команды","tr":"Komutlar","it":"Comandi"})

STRINGS["nav_compare"] = k("Compare",
    **{"zh-CN":"对比","zh-TW":"對比","ja":"比較","ko":"비교","hi":"तुलना",
       "id":"Banding","vi":"So sánh","th":"เปรียบเทียบ","ar":"المقارنة",
       "es":"Comparar","fr":"Comparer","de":"Vergleich","pt-BR":"Comparar","ru":"Сравнить","tr":"Karşılaştır","it":"Confronto"})

STRINGS["nav_blog"] = k("Blog",
    **{"zh-CN":"博客","zh-TW":"部落格","ja":"ブログ","ko":"블로그","hi":"ब्लॉग",
       "id":"Blog","vi":"Blog","th":"บล็อก","ar":"المدوّنة",
       "es":"Blog","fr":"Blog","de":"Blog","pt-BR":"Blog","ru":"Блог","tr":"Blog","it":"Blog"})

STRINGS["nav_faq"] = k("FAQ",
    **{"zh-CN":"常见问题","zh-TW":"常見問題","ja":"FAQ","ko":"자주 묻는 질문","hi":"प्रश्नोत्तर",
       "id":"FAQ","vi":"Hỏi đáp","th":"คำถามที่พบบ่อย","ar":"الأسئلة الشائعة",
       "es":"Preguntas","fr":"FAQ","de":"FAQ","pt-BR":"FAQ","ru":"Вопросы","tr":"SSS","it":"FAQ"})

STRINGS["nav_about"] = k("About",
    **{"zh-CN":"关于","zh-TW":"關於","ja":"概要","ko":"소개","hi":"बारे में",
       "id":"Tentang","vi":"Giới thiệu","th":"เกี่ยวกับ","ar":"عن المشروع",
       "es":"Acerca","fr":"À propos","de":"Über","pt-BR":"Sobre","ru":"О проекте","tr":"Hakkında","it":"Info"})

STRINGS["nav_roadmap"] = k("Roadmap",
    **{"zh-CN":"路线图","zh-TW":"路線圖","ja":"ロードマップ","ko":"로드맵","hi":"रोडमैप",
       "id":"Roadmap","vi":"Lộ trình","th":"แผนงาน","ar":"خارطة الطريق",
       "es":"Hoja de ruta","fr":"Feuille de route","de":"Roadmap","pt-BR":"Roadmap","ru":"Дорожная карта","tr":"Yol haritası","it":"Roadmap"})

STRINGS["nav_star_on_github"] = k("Star on GitHub",
    **{"zh-CN":"在 GitHub 加星","zh-TW":"在 GitHub 加星","ja":"GitHub でスター","ko":"GitHub 스타","hi":"GitHub पर Star करें",
       "id":"Bintangi di GitHub","vi":"Star trên GitHub","th":"Star บน GitHub","ar":"أضف نجمة على GitHub",
       "es":"Dale star en GitHub","fr":"Star sur GitHub","de":"Star auf GitHub","pt-BR":"Dê star no GitHub","ru":"Поставить звезду на GitHub","tr":"GitHub'da yıldız ver","it":"Star su GitHub"})

STRINGS["nav_drawer_lang_label"] = k("Language &middot; 17",
    **{"zh-CN":"语言 &middot; 17","zh-TW":"語言 &middot; 17","ja":"言語 &middot; 17","ko":"언어 &middot; 17","hi":"भाषा &middot; 17",
       "id":"Bahasa &middot; 17","vi":"Ngôn ngữ &middot; 17","th":"ภาษา &middot; 17","ar":"اللغة &middot; 17",
       "es":"Idioma &middot; 17","fr":"Langue &middot; 17","de":"Sprache &middot; 17","pt-BR":"Idioma &middot; 17","ru":"Язык &middot; 17","tr":"Dil &middot; 17","it":"Lingua &middot; 17"})

STRINGS["lang_picker_label"] = k("Language",
    **{"zh-CN":"语言","zh-TW":"語言","ja":"言語","ko":"언어","hi":"भाषा",
       "id":"Bahasa","vi":"Ngôn ngữ","th":"ภาษา","ar":"اللغة",
       "es":"Idioma","fr":"Langue","de":"Sprache","pt-BR":"Idioma","ru":"Язык","tr":"Dil","it":"Lingua"})

# ============ HERO ============
STRINGS["hero_pill_live"] = k("v3.0.0 &middot; THE BRAIN &middot; LIVE",
    **{"zh-CN":"v3.0.0 &middot; THE BRAIN &middot; 上线中","zh-TW":"v3.0.0 &middot; THE BRAIN &middot; 上線中",
       "ja":"v3.0.0 &middot; THE BRAIN &middot; ライブ","ko":"v3.0.0 &middot; THE BRAIN &middot; 라이브",
       "hi":"v3.0.0 &middot; THE BRAIN &middot; लाइव","id":"v3.0.0 &middot; THE BRAIN &middot; LIVE",
       "vi":"v3.0.0 &middot; THE BRAIN &middot; LIVE","th":"v3.0.0 &middot; THE BRAIN &middot; ใช้งานอยู่",
       "ar":"v3.0.0 &middot; THE BRAIN &middot; مباشر","es":"v3.0.0 &middot; THE BRAIN &middot; EN VIVO",
       "fr":"v3.0.0 &middot; THE BRAIN &middot; EN LIGNE","de":"v3.0.0 &middot; THE BRAIN &middot; LIVE",
       "pt-BR":"v3.0.0 &middot; THE BRAIN &middot; AO VIVO","ru":"v3.0.0 &middot; THE BRAIN &middot; В ЭФИРЕ",
       "tr":"v3.0.0 &middot; THE BRAIN &middot; CANLI","it":"v3.0.0 &middot; THE BRAIN &middot; LIVE"})

STRINGS["hero_pill_mit"] = k("MIT &middot; no telemetry &middot; no LLM",
    **{"zh-CN":"MIT &middot; 无遥测 &middot; 无 LLM","zh-TW":"MIT &middot; 無遙測 &middot; 無 LLM",
       "ja":"MIT &middot; テレメトリなし &middot; LLM なし","ko":"MIT &middot; 텔레메트리 없음 &middot; LLM 없음",
       "hi":"MIT &middot; कोई टेलीमेट्री नहीं &middot; कोई LLM नहीं","id":"MIT &middot; tanpa telemetri &middot; tanpa LLM",
       "vi":"MIT &middot; không telemetry &middot; không LLM","th":"MIT &middot; ไม่มี telemetry &middot; ไม่มี LLM",
       "ar":"MIT &middot; بلا تتبّع &middot; بلا نموذج لغوي","es":"MIT &middot; sin telemetría &middot; sin LLM",
       "fr":"MIT &middot; sans télémétrie &middot; sans LLM","de":"MIT &middot; ohne Telemetrie &middot; ohne LLM",
       "pt-BR":"MIT &middot; sem telemetria &middot; sem LLM","ru":"MIT &middot; без телеметрии &middot; без LLM",
       "tr":"MIT &middot; telemetri yok &middot; LLM yok","it":"MIT &middot; senza telemetria &middot; senza LLM"})

# H1 split into three chunks (each line of the h1)
STRINGS["hero_h1_line1"] = k("The brain",
    **{"zh-CN":"这个大脑","zh-TW":"這個大腦","ja":"この頭脳","ko":"두뇌","hi":"वह दिमाग",
       "id":"Otak","vi":"Bộ não","th":"สมอง","ar":"العقل",
       "es":"El cerebro","fr":"Le cerveau","de":"Das Gehirn","pt-BR":"O cérebro","ru":"Мозг","tr":"Beyin","it":"Il cervello"})

STRINGS["hero_h1_line2"] = k("that ships",
    **{"zh-CN":"出品","zh-TW":"出品","ja":"が届ける","ko":"가 출시하는","hi":"जो भेजे",
       "id":"yang menghadirkan","vi":"đem đến","th":"ที่ส่งมอบ","ar":"الذي يُسلِّم",
       "es":"que entrega","fr":"qui livre","de":"das liefert","pt-BR":"que entrega","ru":"который выдаёт","tr":"şunu üreten","it":"che spedisce"})

STRINGS["hero_h1_line3"] = k("design that&nbsp;doesn&rsquo;t look generated.",
    **{"zh-CN":"看不出 AI 生成痕迹的设计。","zh-TW":"看不出 AI 生成痕跡的設計。",
       "ja":"生成物に見えないデザインを。","ko":"AI가 만든 듯 보이지 않는 디자인.",
       "hi":"ऐसा डिज़ाइन जो जेनरेटेड न लगे।","id":"desain yang tidak terlihat dibuat AI.",
       "vi":"thiết kế không trông giống do AI tạo.","th":"ดีไซน์ที่ไม่ดูเหมือน AI สร้าง",
       "ar":"تصميمًا لا يبدو مولَّدًا.","es":"diseño que no parece generado.",
       "fr":"un design qui n&rsquo;a pas l&rsquo;air généré.","de":"Design, das nicht generiert wirkt.",
       "pt-BR":"design que não parece gerado.","ru":"дизайн, который не выглядит сгенерированным.",
       "tr":"yapay üretilmiş gibi durmayan tasarım.","it":"design che non sembra generato."})

# Hero subtitle — full long paragraph. Source has 6 <strong> chunks and runs of plain text.
# We translate the whole thing as ONE key (the build script's replace will substitute the entire block).
STRINGS["hero_sub"] = k(
    "<strong>v3.0 is here.</strong> A 7-axis synthesizer turns any brief into a fresh design language. 160 brand specs become training data, not templates. The recommender re-ranks from a local decisions ledger that learns from your work. Runs in <strong>Claude Code, Cursor, Windsurf</strong> and 14 more IDEs. Same brief always ships the same output. <strong>Offline. Deterministic. No LLM in the engine.</strong>",
    **{
        "zh-CN":"<strong>v3.0 来了。</strong>7 轴合成器把任何 brief 编译成全新的设计语言。160 个品牌规范成为训练数据,而不是模板。推荐器基于本地决策账本重新排序,从你的工作中学习。在 <strong>Claude Code、Cursor、Windsurf</strong> 以及另外 14 个 IDE 中运行。同样的 brief 永远输出同样的结果。<strong>离线。确定性。引擎中没有 LLM。</strong>",
        "zh-TW":"<strong>v3.0 來了。</strong>7 軸合成器把任何 brief 編譯成全新的設計語言。160 個品牌規範成為訓練資料,而不是模板。推薦器基於本地決策帳本重新排序,從你的工作中學習。在 <strong>Claude Code、Cursor、Windsurf</strong> 以及另外 14 個 IDE 中執行。同樣的 brief 永遠輸出同樣的結果。<strong>離線。確定性。引擎中沒有 LLM。</strong>",
        "ja":"<strong>v3.0 が登場。</strong>7 軸合成器が、どんなブリーフでも新しいデザイン言語に変換します。160 のブランド仕様はテンプレートではなくトレーニングデータ。レコメンダーはローカルの決定台帳から再ランク付けし、あなたの仕事から学習します。<strong>Claude Code、Cursor、Windsurf</strong> および他 14 の IDE で動作。同じブリーフは常に同じ出力を生みます。<strong>オフライン。決定論的。エンジンに LLM なし。</strong>",
        "ko":"<strong>v3.0이 도착했습니다.</strong> 7축 신디사이저가 어떤 브리프라도 새로운 디자인 언어로 변환합니다. 160개의 브랜드 사양은 템플릿이 아니라 학습 데이터입니다. 추천기는 로컬 결정 원장에서 재순위를 매기며 당신의 작업에서 배웁니다. <strong>Claude Code, Cursor, Windsurf</strong> 및 14개 IDE에서 작동합니다. 같은 브리프는 항상 같은 결과를 출력합니다. <strong>오프라인. 결정론적. 엔진에 LLM 없음.</strong>",
        "hi":"<strong>v3.0 आ गया है।</strong> 7-अक्ष synthesizer किसी भी brief को नई डिज़ाइन भाषा में बदल देता है। 160 ब्रांड specs अब टेम्पलेट नहीं, ट्रेनिंग डेटा हैं। recommender एक स्थानीय decisions ledger से रैंकिंग बदलता है और आपके काम से सीखता है। <strong>Claude Code, Cursor, Windsurf</strong> और 14 अन्य IDE में चलता है। एक ही brief हमेशा एक ही output देता है। <strong>ऑफ़लाइन। Deterministic। इंजन में कोई LLM नहीं।</strong>",
        "id":"<strong>v3.0 sudah hadir.</strong> Synthesizer 7-aksis mengubah brief apa pun menjadi bahasa desain yang baru. 160 spec brand menjadi data latih, bukan template. Recommender me-rank ulang dari decisions ledger lokal yang belajar dari pekerjaan Anda. Berjalan di <strong>Claude Code, Cursor, Windsurf</strong> dan 14 IDE lainnya. Brief yang sama selalu menghasilkan output yang sama. <strong>Offline. Deterministik. Tanpa LLM di engine.</strong>",
        "vi":"<strong>v3.0 đã có mặt.</strong> Bộ tổng hợp 7 trục biến mọi brief thành một ngôn ngữ thiết kế hoàn toàn mới. 160 spec thương hiệu trở thành dữ liệu huấn luyện, không phải template. Recommender xếp hạng lại từ một decisions ledger cục bộ học từ công việc của bạn. Chạy trong <strong>Claude Code, Cursor, Windsurf</strong> và 14 IDE khác. Cùng một brief luôn cho cùng một output. <strong>Ngoại tuyến. Xác định. Không có LLM trong engine.</strong>",
        "th":"<strong>v3.0 มาแล้ว</strong> synthesizer 7 แกนเปลี่ยน brief ใด ๆ ให้เป็นภาษาดีไซน์ใหม่ · 160 brand specs กลายเป็นข้อมูลฝึก ไม่ใช่เทมเพลต · recommender จัดอันดับใหม่จาก decisions ledger บนเครื่อง ที่เรียนรู้จากงานของคุณ · ทำงานใน <strong>Claude Code, Cursor, Windsurf</strong> และอีก 14 IDE · brief เดียวกันให้ output เดียวกันเสมอ · <strong>ออฟไลน์ · deterministic · ไม่มี LLM ใน engine</strong>",
        "ar":"<strong>v3.0 وصل.</strong> مولّد سباعي المحاور يُحوِّل أيّ ملخّص إلى لغة تصميم جديدة. 160 من مواصفات العلامات تتحوّل إلى بيانات تدريب، لا قوالب. يُعيد المُوصِّي ترتيب نتائجه بناءً على سجلّ قرارات محلّيّ يتعلّم من عملك. يعمل داخل <strong>Claude Code وCursor وWindsurf</strong> و14 محرِّر أكواد آخر. الملخّص نفسه يُنتج المخرج نفسه دائمًا. <strong>بلا اتصال. حتميّ. بلا نموذج لغوي ضخم في المحرّك.</strong>",
        "es":"<strong>v3.0 ya está aquí.</strong> Un sintetizador de 7 ejes convierte cualquier brief en un lenguaje de diseño nuevo. Las 160 specs de marca pasan a ser datos de entrenamiento, no plantillas. El recomendador rerankea desde un ledger local de decisiones que aprende de tu trabajo. Corre en <strong>Claude Code, Cursor, Windsurf</strong> y otros 14 IDEs. Mismo brief, mismo output, siempre. <strong>Offline. Determinístico. Sin LLM en el motor.</strong>",
        "fr":"<strong>v3.0 est là.</strong> Un synthétiseur à 7 axes transforme n&rsquo;importe quel brief en un langage de design inédit. Les 160 specs de marque deviennent des données d&rsquo;entraînement, pas des modèles. Le recommandeur reclasse depuis un ledger local de décisions qui apprend de votre travail. Tourne dans <strong>Claude Code, Cursor, Windsurf</strong> et 14 autres IDE. Même brief, même résultat, à chaque fois. <strong>Hors-ligne. Déterministe. Sans LLM dans le moteur.</strong>",
        "de":"<strong>v3.0 ist da.</strong> Ein 7-Achsen-Synthesizer macht aus jedem Brief eine frische Designsprache. 160 Brand-Specs werden zu Trainingsdaten, nicht zu Vorlagen. Der Recommender ranked aus einem lokalen Decisions-Ledger neu, das von deiner Arbeit lernt. Läuft in <strong>Claude Code, Cursor, Windsurf</strong> und 14 weiteren IDEs. Derselbe Brief liefert immer dasselbe Ergebnis. <strong>Offline. Deterministisch. Kein LLM im Motor.</strong>",
        "pt-BR":"<strong>v3.0 chegou.</strong> Um sintetizador de 7 eixos transforma qualquer brief em uma linguagem de design nova. As 160 specs de marca viram dados de treino, não templates. O recomendador re-ranqueia a partir de um ledger local de decisões que aprende com o seu trabalho. Roda em <strong>Claude Code, Cursor, Windsurf</strong> e mais 14 IDEs. Mesmo brief, mesmo output, sempre. <strong>Offline. Determinístico. Sem LLM no motor.</strong>",
        "ru":"<strong>v3.0 здесь.</strong> Семиосный синтезатор превращает любой бриф в новый дизайн-язык. 160 brand-спецификаций становятся обучающими данными, а не шаблонами. Рекомендатель пере-ранжирует на основе локального журнала решений, который учится на вашей работе. Работает в <strong>Claude Code, Cursor, Windsurf</strong> и 14 других IDE. Один и тот же бриф всегда даёт один и тот же результат. <strong>Offline. Детерминированно. Никакого LLM в движке.</strong>",
        "tr":"<strong>v3.0 yayında.</strong> 7 eksenli bir sentezleyici, herhangi bir brief'i yepyeni bir tasarım diline dönüştürür. 160 marka spec'i artık şablon değil, eğitim verisidir. Önerici, çalışmalarınızdan öğrenen yerel bir decisions ledger'dan yeniden sıralar. <strong>Claude Code, Cursor, Windsurf</strong> ve 14 IDE'de çalışır. Aynı brief her zaman aynı çıktıyı verir. <strong>Çevrimdışı. Deterministik. Motorda LLM yok.</strong>",
        "it":"<strong>v3.0 è qui.</strong> Un sintetizzatore a 7 assi trasforma qualunque brief in un nuovo linguaggio di design. Le 160 spec brand diventano dati di addestramento, non template. Il recommender ri-classifica da un ledger locale di decisioni che impara dal tuo lavoro. Funziona in <strong>Claude Code, Cursor, Windsurf</strong> e altri 14 IDE. Stesso brief, stesso output, sempre. <strong>Offline. Deterministico. Nessun LLM nel motore.</strong>",
    }
)

# Hero CTAs
STRINGS["cta_install"] = k("pip install uxskill")  # stays English (code)

STRINGS["cta_source"] = k("Read the source",
    **{"zh-CN":"阅读源码","zh-TW":"閱讀原始碼","ja":"ソースを読む","ko":"소스 읽기","hi":"सोर्स पढ़ें",
       "id":"Baca kode sumber","vi":"Đọc mã nguồn","th":"อ่านโค้ด","ar":"اقرأ المصدر",
       "es":"Ver el código","fr":"Voir la source","de":"Quellcode lesen","pt-BR":"Ver o código","ru":"Читать исходник","tr":"Kaynağı oku","it":"Leggi il codice"})

# Hero stats
STRINGS["hero_stat_entries"] = k("Structured entries",
    **{"zh-CN":"结构化条目","zh-TW":"結構化條目","ja":"構造化エントリ","ko":"구조화된 항목","hi":"संरचित प्रविष्टियाँ",
       "id":"Entri terstruktur","vi":"Mục có cấu trúc","th":"รายการที่มีโครงสร้าง","ar":"إدخالات منظَّمة",
       "es":"Entradas estructuradas","fr":"Entrées structurées","de":"Strukturierte Einträge","pt-BR":"Entradas estruturadas","ru":"Структурированных записей","tr":"Yapılandırılmış giriş","it":"Voci strutturate"})

STRINGS["hero_stat_brand_specs"] = k("Brand DESIGN.md specs",
    **{"zh-CN":"品牌 DESIGN.md 规范","zh-TW":"品牌 DESIGN.md 規範","ja":"ブランド DESIGN.md 仕様","ko":"브랜드 DESIGN.md 사양","hi":"ब्रांड DESIGN.md स्पेक्स",
       "id":"Spec DESIGN.md brand","vi":"Spec DESIGN.md thương hiệu","th":"สเปก DESIGN.md ของแบรนด์","ar":"مواصفات DESIGN.md للعلامات",
       "es":"Specs de marca DESIGN.md","fr":"Specs de marque DESIGN.md","de":"Marken-DESIGN.md-Specs","pt-BR":"Specs de marca DESIGN.md","ru":"Brand DESIGN.md спецификаций","tr":"Marka DESIGN.md spec","it":"Spec brand DESIGN.md"})

STRINGS["hero_stat_rules"] = k("Anti-pattern rules",
    **{"zh-CN":"反模式规则","zh-TW":"反模式規則","ja":"アンチパターン規則","ko":"안티패턴 규칙","hi":"एंटी-पैटर्न नियम",
       "id":"Aturan anti-pola","vi":"Quy tắc chống mẫu","th":"กฎ anti-pattern","ar":"قواعد مضادّة للأنماط",
       "es":"Reglas anti-patrón","fr":"Règles anti-pattern","de":"Anti-Pattern-Regeln","pt-BR":"Regras anti-padrão","ru":"Anti-pattern правил","tr":"Anti-pattern kuralı","it":"Regole anti-pattern"})

STRINGS["hero_stat_ides"] = k("IDE integrations",
    **{"zh-CN":"IDE 集成","zh-TW":"IDE 整合","ja":"IDE 統合","ko":"IDE 통합","hi":"IDE एकीकरण",
       "id":"Integrasi IDE","vi":"Tích hợp IDE","th":"การเชื่อมต่อ IDE","ar":"تكاملات مع المحرِّرات",
       "es":"Integraciones IDE","fr":"Intégrations IDE","de":"IDE-Integrationen","pt-BR":"Integrações IDE","ru":"IDE-интеграций","tr":"IDE entegrasyonu","it":"Integrazioni IDE"})


# ============ 1.5 PROBLEM SECTION ============
STRINGS["problem_eyebrow"] = k("01 &middot; The problem you ship every day",
    **{"zh-CN":"01 &middot; 你每天都在出货的问题","zh-TW":"01 &middot; 你每天都在出貨的問題",
       "ja":"01 &middot; あなたが毎日出荷している問題","ko":"01 &middot; 매일 출시되는 그 문제",
       "hi":"01 &middot; जो समस्या आप हर दिन भेजते हैं","id":"01 &middot; Masalah yang kamu kirim tiap hari",
       "vi":"01 &middot; Vấn đề bạn ship mỗi ngày","th":"01 &middot; ปัญหาที่คุณส่งทุกวัน",
       "ar":"01 &middot; المشكلة التي تُسلِّمها كلّ يوم","es":"01 &middot; El problema que envías cada día",
       "fr":"01 &middot; Le problème que vous livrez chaque jour","de":"01 &middot; Das Problem, das du täglich auslieferst",
       "pt-BR":"01 &middot; O problema que você envia todo dia","ru":"01 &middot; Проблема, которую вы шипите каждый день",
       "tr":"01 &middot; Her gün gönderdiğin sorun","it":"01 &middot; Il problema che spedisci ogni giorno"})

# Problem h2 — translate the WHOLE multi-line block as one key (preserves <br> and <span>)
STRINGS["problem_h2"] = k(
    "You vibe code in Claude Code or Cursor.<br>\n          Your AI ships <span class=\"accent-italic\">slop</span> by default.",
    **{
        "zh-CN":"你在 Claude Code 或 Cursor 里 vibe coding。<br>\n          你的 AI 默认输出 <span class=\"accent-italic\">劣质成品</span>。",
        "zh-TW":"你在 Claude Code 或 Cursor 裡 vibe coding。<br>\n          你的 AI 預設輸出 <span class=\"accent-italic\">劣質成品</span>。",
        "ja":"Claude Code や Cursor で vibe コーディングする。<br>\n          AI はデフォルトで <span class=\"accent-italic\">slop</span> を出荷する。",
        "ko":"Claude Code나 Cursor에서 바이브 코딩한다.<br>\n          AI는 기본적으로 <span class=\"accent-italic\">slop</span>을 출시한다.",
        "hi":"आप Claude Code या Cursor में vibe coding करते हैं।<br>\n          आपका AI डिफ़ॉल्ट से <span class=\"accent-italic\">slop</span> भेजता है।",
        "id":"Kamu vibe coding di Claude Code atau Cursor.<br>\n          AI-mu mengirim <span class=\"accent-italic\">slop</span> sebagai default.",
        "vi":"Bạn vibe code trong Claude Code hay Cursor.<br>\n          AI của bạn mặc định ship <span class=\"accent-italic\">đồ dở</span>.",
        "th":"คุณ vibe code ใน Claude Code หรือ Cursor<br>\n          AI ของคุณส่ง <span class=\"accent-italic\">งานห่วย</span> ตามค่าเริ่มต้น",
        "ar":"تكتب الكود بالحدس داخل Claude Code أو Cursor.<br>\n          والذكاء الاصطناعي يُسلِّم <span class=\"accent-italic\">عملاً رخيصًا</span> افتراضيًّا.",
        "es":"Haces vibe coding en Claude Code o Cursor.<br>\n          Tu IA entrega <span class=\"accent-italic\">slop</span> por defecto.",
        "fr":"Vous vibe codez dans Claude Code ou Cursor.<br>\n          Votre IA livre du <span class=\"accent-italic\">slop</span> par défaut.",
        "de":"Du vibest in Claude Code oder Cursor.<br>\n          Deine KI liefert standardmäßig <span class=\"accent-italic\">Slop</span>.",
        "pt-BR":"Você faz vibe coding no Claude Code ou Cursor.<br>\n          Sua IA entrega <span class=\"accent-italic\">slop</span> por padrão.",
        "ru":"Вы vibe-кодите в Claude Code или Cursor.<br>\n          Ваш AI по умолчанию шипит <span class=\"accent-italic\">slop</span>.",
        "tr":"Claude Code veya Cursor'da vibe coding yapıyorsun.<br>\n          AI'ın varsayılan olarak <span class=\"accent-italic\">slop</span> üretiyor.",
        "it":"Fai vibe coding in Claude Code o Cursor.<br>\n          La tua AI spedisce <span class=\"accent-italic\">slop</span> di default.",
    }
)

# Problem lede — long paragraph
STRINGS["problem_lede"] = k(
    "Ask the model to \"build a fintech landing.\" You get the same five tells inside ten seconds. Purple-to-blue gradients. Three equal cards. Inter at display size. <strong>J&#x6f;hn D&#x6f;e</strong> in the testimonial. Bouncing arrow CTA. Centered hero. 300ms ease-in-out on every transition. The output is technically correct and visually disposable.",
    **{
        "zh-CN":"让模型「写一个金融科技 landing」。十秒内你就能认出同样的五个特征。紫到蓝的渐变。三张等宽卡片。Inter 大字号标题。<strong>J&#x6f;hn D&#x6f;e</strong> 出现在客户证言里。一个弹跳箭头 CTA。居中的 hero。所有过渡都是 300ms ease-in-out。技术上没错,视觉上一次性。",
        "zh-TW":"讓模型「寫一個金融科技 landing」。十秒內你就能認出同樣的五個特徵。紫到藍的漸層。三張等寬卡片。Inter 大字號標題。<strong>J&#x6f;hn D&#x6f;e</strong> 出現在客戶見證裡。一個彈跳箭頭 CTA。置中的 hero。所有過渡都是 300ms ease-in-out。技術上沒錯,視覺上一次性。",
        "ja":"モデルに「フィンテックの LP を作って」と頼んでみる。10 秒以内に同じ 5 つの手癖が出る。紫から青へのグラデーション。等幅 3 カラム。Inter のディスプレイサイズ。<strong>J&#x6f;hn D&#x6f;e</strong> のテスティモニアル。バウンドする矢印 CTA。中央寄せのヒーロー。あらゆるトランジションが 300ms ease-in-out。技術的には正しく、視覚的には使い捨てだ。",
        "ko":"모델에게 \"핀테크 랜딩 만들어줘\"라고 하자. 10초 안에 똑같은 다섯 가지 흔적이 보인다. 보라에서 파랑으로 가는 그라데이션. 동일한 카드 세 개. 디스플레이 사이즈의 Inter. <strong>J&#x6f;hn D&#x6f;e</strong>가 들어간 추천사. 통통 튀는 화살표 CTA. 가운데 정렬된 히어로. 모든 전환은 300ms ease-in-out. 기술적으로는 맞지만 시각적으로는 일회용이다.",
        "hi":"मॉडल से कहो \"एक fintech landing बनाओ।\" दस सेकंड में वही पाँच निशान दिखेंगे। पर्पल-टू-ब्लू ग्रेडिएंट। तीन बराबर कार्ड। Inter डिस्प्ले साइज़ में। testimonial में <strong>J&#x6f;hn D&#x6f;e</strong>। उछलता arrow CTA। केंद्रित hero। हर transition पर 300ms ease-in-out। output तकनीकी रूप से सही है, दृश्य रूप से disposable।",
        "id":"Minta modelnya \"build a fintech landing.\" Dalam sepuluh detik kamu dapatkan lima tanda yang sama. Gradien ungu ke biru. Tiga kartu sama besar. Inter ukuran display. <strong>J&#x6f;hn D&#x6f;e</strong> di testimoni. Tombol panah memantul. Hero rata tengah. 300ms ease-in-out di setiap transisi. Output-nya benar secara teknis tapi sekali pakai secara visual.",
        "vi":"Bảo model \"build a fintech landing.\" Trong mười giây bạn thấy đúng năm dấu hiệu. Gradient tím sang xanh. Ba thẻ bằng nhau. Inter cỡ display. <strong>J&#x6f;hn D&#x6f;e</strong> trong testimonial. Nút mũi tên nảy. Hero căn giữa. 300ms ease-in-out cho mọi transition. Output đúng kỹ thuật nhưng dùng một lần về mặt thị giác.",
        "th":"สั่งโมเดลว่า \"build a fintech landing\" ภายในสิบวินาทีคุณจะเห็นห้าร่องรอยเดิม · ไล่สีจากม่วงไปน้ำเงิน · การ์ดเท่ากันสามใบ · Inter ขนาดดิสเพลย์ · <strong>J&#x6f;hn D&#x6f;e</strong> ใน testimonial · CTA ลูกศรกระดอน · hero จัดกลาง · ทุก transition ใช้ 300ms ease-in-out · output ถูกต้องในเชิงเทคนิคแต่ทิ้งได้ในเชิงภาพ",
        "ar":"اطلب من النموذج «أنشئ صفحة هبوط لشركة فينتك». ستجد خلال عشر ثوانٍ العلامات الخمس نفسها. تدرّج لوني من البنفسجي إلى الأزرق. ثلاث بطاقات متساوية. خط Inter بحجم العنوان. <strong>J&#x6f;hn D&#x6f;e</strong> في شهادة العميل. زرّ نداء يقفز بسهم. هيرو موسَّط. انتقال 300ms ease-in-out في كل عنصر. النتيجة صحيحة تقنيًا، قابلة للاستهلاك بصريًا.",
        "es":"Pídele al modelo \"build a fintech landing.\" En diez segundos tienes los mismos cinco rastros. Gradiente de violeta a azul. Tres tarjetas iguales. Inter en tamaño display. <strong>J&#x6f;hn D&#x6f;e</strong> en el testimonio. CTA con flecha rebotando. Hero centrado. 300ms ease-in-out en cada transición. La salida es correcta técnicamente y desechable visualmente.",
        "fr":"Demandez au modèle « build a fintech landing ». En dix secondes vous retrouvez les cinq mêmes signatures. Dégradé violet vers bleu. Trois cartes égales. Inter taille display. <strong>J&#x6f;hn D&#x6f;e</strong> dans le témoignage. CTA flèche qui rebondit. Hero centré. 300ms ease-in-out sur chaque transition. La sortie est techniquement correcte et visuellement jetable.",
        "de":"Bitte das Modell um „build a fintech landing.\" In zehn Sekunden siehst du dieselben fünf Spuren. Lila-zu-Blau-Verlauf. Drei gleiche Karten. Inter in Display-Größe. <strong>J&#x6f;hn D&#x6f;e</strong> im Testimonial. Hüpfender Pfeil-CTA. Zentrierter Hero. 300ms ease-in-out auf jeder Transition. Das Ergebnis ist technisch korrekt und visuell Wegwerfware.",
        "pt-BR":"Peça ao modelo \"build a fintech landing.\" Em dez segundos você reconhece as mesmas cinco assinaturas. Gradiente roxo-azul. Três cards iguais. Inter em display. <strong>J&#x6f;hn D&#x6f;e</strong> no testimonial. CTA com seta saltitante. Hero centralizado. 300ms ease-in-out em toda transição. A saída é tecnicamente correta e visualmente descartável.",
        "ru":"Попросите модель «build a fintech landing». За десять секунд вы получите те же пять признаков. Градиент из фиолетового в синий. Три одинаковые карточки. Inter в display-размере. <strong>J&#x6f;hn D&#x6f;e</strong> в отзыве. CTA с прыгающей стрелкой. Центрированный hero. 300ms ease-in-out на каждом переходе. Вывод технически верный и визуально одноразовый.",
        "tr":"Modele \"build a fintech landing\" de. On saniye içinde aynı beş izi görürsün. Mordan maviye degrade. Üç eşit kart. Display boyutta Inter. Tanıklıkta <strong>J&#x6f;hn D&#x6f;e</strong>. Zıplayan ok CTA. Ortalanmış hero. Her geçişte 300ms ease-in-out. Çıktı teknik olarak doğru, görsel olarak tek kullanımlık.",
        "it":"Chiedi al modello \"build a fintech landing.\" In dieci secondi ritrovi le stesse cinque firme. Gradiente viola-blu. Tre card uguali. Inter formato display. <strong>J&#x6f;hn D&#x6f;e</strong> nella testimonianza. CTA con freccia che rimbalza. Hero centrato. 300ms ease-in-out su ogni transizione. L&rsquo;output è tecnicamente corretto e visivamente usa-e-getta.",
    }
)

STRINGS["problem_card_fingerprint_tag"] = k("The fingerprint",
    **{"zh-CN":"指纹","zh-TW":"指紋","ja":"指紋","ko":"지문","hi":"फिंगरप्रिंट",
       "id":"Sidik jari","vi":"Dấu vân tay","th":"ลายนิ้วมือ","ar":"البصمة",
       "es":"La huella","fr":"L&rsquo;empreinte","de":"Der Fingerabdruck","pt-BR":"A impressão digital","ru":"Отпечаток","tr":"Parmak izi","it":"L&rsquo;impronta"})

STRINGS["problem_card_fingerprint_head"] = k("Five tells, ten seconds.",
    **{"zh-CN":"五个特征,十秒内识破。","zh-TW":"五個特徵,十秒內識破。","ja":"5 つの手癖、10 秒で見抜ける。",
       "ko":"다섯 가지 흔적, 10초.","hi":"पाँच निशान, दस सेकंड।","id":"Lima tanda, sepuluh detik.",
       "vi":"Năm dấu hiệu, mười giây.","th":"ห้าร่องรอย สิบวินาที","ar":"خمس علامات في عشر ثوانٍ.",
       "es":"Cinco rastros, diez segundos.","fr":"Cinq signes, dix secondes.","de":"Fünf Spuren, zehn Sekunden.",
       "pt-BR":"Cinco rastros, dez segundos.","ru":"Пять признаков, десять секунд.","tr":"Beş iz, on saniye.","it":"Cinque indizi, dieci secondi."})

STRINGS["problem_card_cause_tag"] = k("Why it happens",
    **{"zh-CN":"为什么会这样","zh-TW":"為什麼會這樣","ja":"なぜ起きるか","ko":"왜 그런가","hi":"ऐसा क्यों होता है",
       "id":"Kenapa terjadi","vi":"Vì sao xảy ra","th":"ทำไมถึงเป็นแบบนี้","ar":"لماذا يحدث ذلك",
       "es":"Por qué pasa","fr":"Pourquoi ça arrive","de":"Warum es passiert","pt-BR":"Por que acontece","ru":"Почему так","tr":"Neden olur","it":"Perché succede"})

STRINGS["problem_card_cause_head"] = k("The model improvises.",
    **{"zh-CN":"模型在即兴发挥。","zh-TW":"模型在即興發揮。","ja":"モデルは即興する。","ko":"모델은 즉흥적으로 만든다.","hi":"मॉडल इम्प्रोवाइज़ करता है।",
       "id":"Model berimprovisasi.","vi":"Model ứng tác.","th":"โมเดลกำลังด้นสด","ar":"النموذج يرتجل.",
       "es":"El modelo improvisa.","fr":"Le modèle improvise.","de":"Das Modell improvisiert.",
       "pt-BR":"O modelo improvisa.","ru":"Модель импровизирует.","tr":"Model doğaçlama yapar.","it":"Il modello improvvisa."})

STRINGS["problem_card_cause_body"] = k(
    "The assistant has read every design system on GitHub. It has no idea which one fits your brief. It defaults to the centroid &mdash; the average of every SaaS site it ever ingested. The result reads as generated within seconds. Your domain, your industry, your customers &mdash; none of it influences the output.",
    **{
        "zh-CN":"助手读过 GitHub 上的所有设计系统。它根本不知道哪一个适合你的 brief。它直接落到那个质心 &mdash; 它见过的所有 SaaS 站点的平均值。结果几秒内就显出 AI 的痕迹。你的领域、你的行业、你的客户 &mdash; 通通没有影响到输出。",
        "zh-TW":"助理讀過 GitHub 上的所有設計系統。它根本不知道哪一個適合你的 brief。它直接落到那個質心 &mdash; 它見過的所有 SaaS 網站的平均值。結果幾秒內就顯出 AI 的痕跡。你的領域、你的產業、你的客戶 &mdash; 通通沒有影響到輸出。",
        "ja":"アシスタントは GitHub 上のあらゆるデザインシステムを読んでいる。あなたのブリーフにどれが合うかは分からない。だから重心 &mdash; これまで取り込んだ全 SaaS サイトの平均 &mdash; に落ち着く。結果は数秒で生成物だと分かる。あなたのドメインも、業界も、顧客も、出力に何の影響も与えていない。",
        "ko":"어시스턴트는 GitHub의 모든 디자인 시스템을 읽었다. 어느 것이 당신의 브리프에 맞는지는 모른다. 그래서 중심 &mdash; 그동안 학습한 모든 SaaS 사이트의 평균 &mdash; 으로 떨어진다. 결과는 몇 초 안에 AI 생성물로 읽힌다. 당신의 도메인, 산업, 고객 &mdash; 어느 것도 출력에 영향을 주지 않는다.",
        "hi":"असिस्टेंट ने GitHub पर हर डिज़ाइन सिस्टम पढ़ा है। उसे पता ही नहीं कि कौन सा आपके brief पर फिट होता है। वह default रूप से centroid पर पहुँचता है &mdash; हर SaaS साइट का average जो उसने पढ़ी है। नतीजा कुछ सेकंड में जेनरेटेड दिखता है। आपका domain, आपका industry, आपके customers &mdash; इनमें से कुछ भी output को प्रभावित नहीं करता।",
        "id":"Asisten sudah membaca setiap design system di GitHub. Dia tidak tahu mana yang cocok untuk brief-mu. Default-nya jatuh ke centroid &mdash; rata-rata dari semua situs SaaS yang pernah dia serap. Hasilnya terlihat dihasilkan AI dalam hitungan detik. Domain, industri, pelanggan kamu &mdash; tidak satu pun memengaruhi output.",
        "vi":"Trợ lý đã đọc mọi design system trên GitHub. Nó không biết cái nào hợp brief của bạn. Mặc định nó rơi vào centroid &mdash; trung bình mọi site SaaS từng được nuốt vào. Kết quả nhìn ra là AI tạo chỉ trong vài giây. Lĩnh vực, ngành, khách hàng của bạn &mdash; không cái nào ảnh hưởng đến output.",
        "th":"ผู้ช่วยได้อ่าน design system ทุกตัวบน GitHub แต่มันไม่รู้ว่าตัวไหนเหมาะกับ brief ของคุณ มันจึงตกไปที่จุดศูนย์กลาง &mdash; ค่าเฉลี่ยของทุกเว็บ SaaS ที่เคยกลืนเข้าไป ผลลัพธ์จึงดูเหมือนถูก AI สร้างภายในไม่กี่วินาที โดเมน อุตสาหกรรม ลูกค้าของคุณ &mdash; ไม่มีอะไรมีผลต่อ output เลย",
        "ar":"المساعد قرأ كلّ منظومة تصميم على GitHub. لا فكرة لديه عن المناسب لملخّصك، فيستقرّ على المركز &mdash; متوسّط كلّ موقع SaaS قرأه. تظهر النتيجة كأنّها مولَّدة خلال ثوانٍ. مجالك، صناعتك، عملاؤك &mdash; لا شيء منها يؤثّر في المخرج.",
        "es":"El asistente leyó cada design system de GitHub. No tiene idea de cuál encaja con tu brief. Cae por defecto en el centroide &mdash; el promedio de cada sitio SaaS que ingirió. El resultado se ve generado en segundos. Tu dominio, tu industria, tus clientes &mdash; nada de eso influye en la salida.",
        "fr":"L&rsquo;assistant a lu chaque design system sur GitHub. Il ignore lequel correspond à votre brief. Par défaut il atterrit sur le centroïde &mdash; la moyenne de chaque site SaaS qu&rsquo;il a ingurgité. Le résultat se lit comme généré en quelques secondes. Votre domaine, votre secteur, vos clients &mdash; rien de tout cela n&rsquo;influence la sortie.",
        "de":"Der Assistent hat jedes Designsystem auf GitHub gelesen. Er hat keine Ahnung, welches zu deinem Brief passt. Er landet per Default beim Centroid &mdash; dem Durchschnitt jeder SaaS-Seite, die er je gefressen hat. Das Ergebnis liest sich in Sekunden als generiert. Deine Domain, deine Branche, deine Kunden &mdash; nichts davon beeinflusst die Ausgabe.",
        "pt-BR":"O assistente leu cada design system no GitHub. Ele não tem ideia de qual encaixa no seu brief. Cai por padrão no centroide &mdash; a média de cada site SaaS que ele já ingeriu. O resultado parece gerado em segundos. Seu domínio, seu setor, seus clientes &mdash; nada disso influencia a saída.",
        "ru":"Ассистент прочитал каждую дизайн-систему на GitHub. Он понятия не имеет, какая подходит вашему брифу. По умолчанию он падает в центроид &mdash; усреднение каждого SaaS-сайта, который он когда-либо съел. Результат читается как сгенерированный за секунды. Ваш домен, ваша отрасль, ваши клиенты &mdash; ничто из этого не влияет на вывод.",
        "tr":"Asistan GitHub'daki her design system'i okudu. Brief'ine hangisi uyar, fikri yok. Varsayılan olarak centroide &mdash; yutmuş olduğu her SaaS sitesinin ortalamasına &mdash; düşer. Sonuç saniyeler içinde üretilmiş gibi okunur. Senin alanın, sektörün, müşterilerin &mdash; hiçbiri çıktıyı etkilemez.",
        "it":"L&rsquo;assistente ha letto ogni design system su GitHub. Non ha idea di quale calzi al tuo brief. Di default cade sul centroide &mdash; la media di ogni sito SaaS che ha mai ingerito. Il risultato si legge come generato in pochi secondi. Il tuo dominio, il tuo settore, i tuoi clienti &mdash; nulla di tutto questo influenza l&rsquo;output.",
    }
)

STRINGS["problem_card_cost_tag"] = k("The cost",
    **{"zh-CN":"代价","zh-TW":"代價","ja":"そのコスト","ko":"비용","hi":"कीमत",
       "id":"Biayanya","vi":"Cái giá","th":"ราคา","ar":"الكلفة",
       "es":"El costo","fr":"Le coût","de":"Der Preis","pt-BR":"O custo","ru":"Цена","tr":"Bedeli","it":"Il costo"})

STRINGS["problem_card_cost_head"] = k("Trust erodes on first paint.",
    **{"zh-CN":"信任在第一帧就开始流失。","zh-TW":"信任在第一幀就開始流失。","ja":"信頼は最初のペイントで失われる。",
       "ko":"신뢰는 첫 페인트에서부터 무너진다.","hi":"पहले paint पर ही trust टूटना शुरू।","id":"Kepercayaan luntur di paint pertama.",
       "vi":"Niềm tin mất ngay từ frame đầu.","th":"ความเชื่อใจเริ่มร่วงตั้งแต่ frame แรก","ar":"الثقة تتآكل عند أوّل ظهور.",
       "es":"La confianza se cae en el primer paint.","fr":"La confiance s&rsquo;effrite dès le premier rendu.","de":"Vertrauen bröckelt beim ersten Paint.",
       "pt-BR":"A confiança cai já no primeiro paint.","ru":"Доверие падает на первом рендере.","tr":"Güven ilk paint'te erir.","it":"La fiducia crolla al primo paint."})

STRINGS["problem_card_cost_body"] = k(
    "Investors flag it. Customers click away. Designers refuse to touch it. You ship faster but the shape of what you shipped is generic. A year of vibe coding leaves a portfolio that all looks the same. The velocity feels free until the brand bill comes due.",
    **{
        "zh-CN":"投资人会指出来。客户会点走。设计师拒绝接手。你出货更快,但你出的东西形状是通用的。一年的 vibe coding 留下一个看起来都一样的作品集。那份速度看起来免费,直到品牌的账单到来。",
        "zh-TW":"投資人會指出來。客戶會點走。設計師拒絕接手。你出貨更快,但你出的東西形狀是通用的。一年的 vibe coding 留下一個看起來都一樣的作品集。那份速度看起來免費,直到品牌的帳單到來。",
        "ja":"投資家は気づく。顧客は離れる。デザイナーは触りたがらない。出荷は早くなったが、出したものの形は汎用的だ。1 年の vibe コーディングは、すべてが似通ったポートフォリオを残す。スピードは無料に見えるが、ブランドの請求書が届くまでの話だ。",
        "ko":"투자자는 알아차린다. 고객은 떠난다. 디자이너는 만지기를 거부한다. 더 빨리 출시하지만 출시한 것의 모양은 일반적이다. 1년의 바이브 코딩이 남기는 건 모두 똑같이 보이는 포트폴리오다. 그 속도는 공짜처럼 느껴진다, 브랜드 청구서가 도착하기 전까지는.",
        "hi":"निवेशक flag करते हैं। ग्राहक click करके चले जाते हैं। डिज़ाइनर इसे छूने से इंकार करते हैं। आप तेज़ ship करते हैं लेकिन जो ship किया उसका आकार generic है। एक साल की vibe coding ऐसा portfolio छोड़ती है जो सब एक जैसा दिखता है। वो speed free लगती है, जब तक brand का बिल नहीं आता।",
        "id":"Investor menandai. Pelanggan klik pergi. Desainer menolak menyentuh. Kamu kirim lebih cepat tapi bentuk yang kamu kirim itu generik. Setahun vibe coding meninggalkan portofolio yang semuanya kelihatan sama. Kecepatan itu terasa gratis sampai tagihan brand datang.",
        "vi":"Nhà đầu tư nhận ra. Khách hàng click bỏ đi. Designer từ chối đụng vào. Bạn ship nhanh hơn nhưng hình dáng thứ bạn ship đều generic. Một năm vibe coding để lại portfolio mà cái nào cũng giống nhau. Tốc độ đó có vẻ miễn phí cho đến khi hoá đơn thương hiệu được trả.",
        "th":"นักลงทุนจับได้ ลูกค้าคลิกออก ดีไซเนอร์ปฏิเสธจะแตะ คุณส่งเร็วขึ้น แต่หน้าตาของสิ่งที่ส่งเป็นแบบทั่วไป หนึ่งปีของ vibe coding ทิ้งพอร์ตที่หน้าตาเหมือนกันหมด ความเร็วดูเหมือนฟรีจนกว่าบิลของแบรนด์จะมาถึง",
        "ar":"المستثمرون يلتقطونها. العملاء يغادرون النقرة. المصمّمون يرفضون لمسها. تُسلّم أسرع، لكنّ شكل ما سلّمته معتاد ومنسوخ. سنة من البرمجة الحدسيّة تترك معرض أعمال كأنّه نسخ مكرَّر. السرعة تبدو مجّانيّة حتى يحلّ موعد فاتورة العلامة.",
        "es":"Los inversores lo detectan. Los clientes hacen clic y se van. Los diseñadores se niegan a tocarlo. Envías más rápido pero la forma de lo que enviaste es genérica. Un año de vibe coding deja un portafolio que parece todo igual. La velocidad se siente gratis hasta que llega la factura de marca.",
        "fr":"Les investisseurs le repèrent. Les clients cliquent ailleurs. Les designers refusent d&rsquo;y toucher. Vous livrez plus vite mais la forme de ce que vous livrez est générique. Un an de vibe coding laisse un portfolio qui se ressemble tout entier. La vitesse paraît gratuite jusqu&rsquo;à ce que la facture de marque arrive.",
        "de":"Investoren merken es. Kunden klicken weg. Designer weigern sich, es anzufassen. Du lieferst schneller, aber die Form dessen, was du geliefert hast, ist generisch. Ein Jahr Vibe Coding hinterlässt ein Portfolio, das überall gleich aussieht. Die Geschwindigkeit fühlt sich kostenlos an, bis die Brand-Rechnung kommt.",
        "pt-BR":"Investidores percebem. Clientes clicam fora. Designers se recusam a tocar. Você envia mais rápido, mas o formato do que enviou é genérico. Um ano de vibe coding deixa um portfólio que parece tudo igual. A velocidade parece grátis até a conta da marca chegar.",
        "ru":"Инвесторы это видят. Клиенты уходят. Дизайнеры отказываются прикасаться. Вы шипите быстрее, но форма того, что вы зашипили, шаблонна. Год vibe-кодинга оставляет портфолио, где всё выглядит одинаково. Скорость кажется бесплатной, пока не приходит счёт за бренд.",
        "tr":"Yatırımcılar fark eder. Müşteriler tıklayıp gider. Tasarımcılar dokunmayı reddeder. Daha hızlı gönderirsin ama gönderdiğin şeyin şekli sıradandır. Bir yıllık vibe coding, hepsi birbirine benzeyen bir portföy bırakır. Hız bedava gibi gelir &mdash; marka faturası gelene dek.",
        "it":"Gli investitori se ne accorgono. I clienti cliccano via. I designer si rifiutano di toccarlo. Spedisci più veloce ma la forma di ciò che hai spedito è generica. Un anno di vibe coding lascia un portfolio che sembra tutto uguale. La velocità sembra gratis finché non arriva la bolletta del brand.",
    }
)

# Problem-card list items
STRINGS["problem_li_gradient"] = k("Purple &rarr; blue 135&deg; gradient",
    **{"zh-CN":"紫 &rarr; 蓝 135&deg; 渐变","zh-TW":"紫 &rarr; 藍 135&deg; 漸層",
       "ja":"紫 &rarr; 青 135&deg; グラデーション","ko":"보라 &rarr; 파랑 135&deg; 그라데이션",
       "hi":"पर्पल &rarr; ब्लू 135&deg; gradient","id":"Gradien ungu &rarr; biru 135&deg;",
       "vi":"Gradient tím &rarr; xanh 135&deg;","th":"ไล่สีม่วง &rarr; น้ำเงิน 135&deg;",
       "ar":"تدرّج بنفسجيّ &rarr; أزرق بزاوية 135&deg;","es":"Gradiente violeta &rarr; azul 135&deg;",
       "fr":"Dégradé violet &rarr; bleu 135&deg;","de":"Lila &rarr; blauer 135&deg;-Verlauf",
       "pt-BR":"Gradiente roxo &rarr; azul 135&deg;","ru":"Градиент фиолетовый &rarr; синий 135&deg;",
       "tr":"Mor &rarr; mavi 135&deg; degrade","it":"Gradiente viola &rarr; blu 135&deg;"})

STRINGS["problem_li_three_cards"] = k("Three equal cards in a row",
    **{"zh-CN":"一排三张等宽卡片","zh-TW":"一排三張等寬卡片","ja":"等幅 3 カラムのカード","ko":"한 줄에 동일한 카드 3개","hi":"एक row में तीन बराबर कार्ड",
       "id":"Tiga kartu sama besar berderet","vi":"Ba thẻ bằng nhau trên một hàng","th":"การ์ดเท่ากันสามใบในแถวเดียว","ar":"ثلاث بطاقات متساوية في صفّ واحد",
       "es":"Tres tarjetas iguales en fila","fr":"Trois cartes égales en ligne","de":"Drei gleiche Karten in einer Reihe",
       "pt-BR":"Três cards iguais em linha","ru":"Три одинаковые карточки в ряд","tr":"Bir sırada üç eşit kart","it":"Tre card uguali in fila"})

STRINGS["problem_li_lorem"] = k("\"L&#x6f;rem ipsum dolor sit amet\"")  # placeholder text stays raw — universal

STRINGS["problem_li_john_doe"] = k("\"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\" testimonial",
    **{"zh-CN":"「J&#x6f;hn D&#x6f;e」/「Jane D&#x6f;e」客户证言","zh-TW":"「J&#x6f;hn D&#x6f;e」/「Jane D&#x6f;e」客戶見證",
       "ja":"「J&#x6f;hn D&#x6f;e」/「Jane D&#x6f;e」のテスティモニアル","ko":"「J&#x6f;hn D&#x6f;e」/「Jane D&#x6f;e」 추천사",
       "hi":"\"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\" testimonial","id":"Testimoni \"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\"",
       "vi":"Testimonial \"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\"","th":"testimonial \"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\"",
       "ar":"شهادة عميل باسم «J&#x6f;hn D&#x6f;e» أو «Jane D&#x6f;e»","es":"Testimonio de \"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\"",
       "fr":"Témoignage de « J&#x6f;hn D&#x6f;e » / « Jane D&#x6f;e »","de":"Testimonial von „J&#x6f;hn D&#x6f;e\" / „Jane D&#x6f;e\"",
       "pt-BR":"Depoimento de \"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\"","ru":"Отзыв «J&#x6f;hn D&#x6f;e» / «Jane D&#x6f;e»",
       "tr":"\"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\" tanıklığı","it":"Testimonianza \"J&#x6f;hn D&#x6f;e\" / \"Jane D&#x6f;e\""})

STRINGS["problem_li_inter_96"] = k("Inter 96px hero, centered",
    **{"zh-CN":"Inter 96px hero,居中","zh-TW":"Inter 96px hero,置中","ja":"Inter 96px のセンター揃え hero","ko":"Inter 96px hero, 가운데 정렬","hi":"Inter 96px hero, केंद्रित",
       "id":"Hero Inter 96px, rata tengah","vi":"Hero Inter 96px, căn giữa","th":"hero Inter 96px จัดกลาง","ar":"عنوان رئيسي Inter 96px موسَّط",
       "es":"Hero Inter 96px, centrado","fr":"Hero Inter 96px, centré","de":"Inter 96px Hero, zentriert",
       "pt-BR":"Hero Inter 96px, centralizado","ru":"Hero Inter 96px, по центру","tr":"Inter 96px hero, ortalanmış","it":"Hero Inter 96px, centrato"})

# Bridge
STRINGS["problem_bridge_text"] = k(
    "What if your AI assistant had a designer's brain wired up next to it &mdash; a brain that <strong>knew which design language fits your brief</strong>, refused the slop fingerprints before commit, and learned from every shipped output?",
    **{
        "zh-CN":"如果你的 AI 助手旁边接了一个设计师的大脑会怎样 &mdash; 一个 <strong>知道哪种设计语言契合你的 brief</strong>、在 commit 前拒绝那些劣质指纹、并从每次出货中学习的大脑?",
        "zh-TW":"如果你的 AI 助手旁邊接了一個設計師的大腦會怎樣 &mdash; 一個 <strong>知道哪種設計語言契合你的 brief</strong>、在 commit 前拒絕那些劣質指紋、並從每次出貨中學習的大腦?",
        "ja":"もし AI アシスタントの隣にデザイナーの頭脳が繋がっていたら &mdash; <strong>あなたのブリーフに合うデザイン言語を知っている</strong> 頭脳が、コミット前に slop の指紋を拒否し、出荷したすべての出力から学習していたら?",
        "ko":"만약 AI 어시스턴트 옆에 디자이너의 두뇌가 연결되어 있다면 &mdash; <strong>당신의 브리프에 맞는 디자인 언어를 아는</strong> 두뇌, 커밋 전에 slop 지문을 거부하고, 출시된 모든 결과물에서 배우는 두뇌라면?",
        "hi":"क्या हो अगर आपके AI assistant के बगल में एक डिज़ाइनर का दिमाग जुड़ा हो &mdash; एक ऐसा दिमाग जो <strong>जानता हो कि कौन सी डिज़ाइन भाषा आपके brief पर फिट होती है</strong>, commit से पहले slop fingerprints को मना कर देता हो, और हर shipped output से सीखता हो?",
        "id":"Bagaimana jika asisten AI-mu punya otak desainer di sebelahnya &mdash; otak yang <strong>tahu bahasa desain mana yang cocok untuk brief-mu</strong>, menolak sidik jari slop sebelum commit, dan belajar dari setiap output yang dikirim?",
        "vi":"Sẽ thế nào nếu trợ lý AI có một bộ não designer được nối bên cạnh &mdash; một bộ não <strong>biết ngôn ngữ thiết kế nào hợp brief của bạn</strong>, từ chối dấu vân tay slop trước khi commit, và học từ mọi output đã ship?",
        "th":"จะเป็นยังไงถ้าผู้ช่วย AI ของคุณมีสมองนักออกแบบต่ออยู่ข้าง ๆ &mdash; สมองที่ <strong>รู้ว่าภาษาดีไซน์แบบไหนเหมาะกับ brief ของคุณ</strong> ปฏิเสธลายนิ้วมือ slop ก่อน commit และเรียนรู้จากทุก output ที่ส่ง?",
        "ar":"تخيّل لو كان بجانب مساعدك الذكيّ عقلٌ مصمِّم &mdash; عقلٌ <strong>يعرف أيّ لغة تصميم تناسب ملخّصك</strong>، ويرفض بصمات الـ slop قبل التثبيت، ويتعلَّم من كلّ مخرج سلَّمته؟",
        "es":"¿Y si tu asistente IA tuviera un cerebro de diseñador conectado al lado &mdash; un cerebro que <strong>supiera qué lenguaje de diseño encaja con tu brief</strong>, rechazara las huellas de slop antes del commit y aprendiera de cada salida enviada?",
        "fr":"Et si votre assistant IA avait un cerveau de designer branché à côté &mdash; un cerveau qui <strong>savait quel langage de design correspond à votre brief</strong>, refusait les empreintes de slop avant commit, et apprenait de chaque sortie livrée ?",
        "de":"Was, wenn dein KI-Assistent neben sich das Gehirn eines Designers hätte &mdash; ein Gehirn, das <strong>weiß, welche Designsprache zu deinem Brief passt</strong>, Slop-Fingerabdrücke vor dem Commit ablehnt und aus jeder ausgelieferten Ausgabe lernt?",
        "pt-BR":"E se seu assistente IA tivesse um cérebro de designer ligado ao lado &mdash; um cérebro que <strong>soubesse qual linguagem de design encaixa no seu brief</strong>, recusasse impressões digitais de slop antes do commit, e aprendesse de cada saída enviada?",
        "ru":"Что если у вашего AI-ассистента рядом был бы мозг дизайнера &mdash; мозг, который <strong>знал бы, какой дизайн-язык подходит вашему брифу</strong>, отказывал бы отпечаткам slop до коммита, и учился бы на каждом отгруженном выводе?",
        "tr":"Peki AI asistanının yanında bir tasarımcı beyni bağlı olsaydı &mdash; <strong>brief'ine hangi tasarım dilinin uyduğunu bilen</strong>, slop parmak izlerini commit'ten önce reddeden ve gönderilen her çıktıdan öğrenen bir beyin olsaydı?",
        "it":"E se il tuo assistente AI avesse un cervello da designer collegato accanto &mdash; un cervello che <strong>sapesse quale linguaggio di design calza al tuo brief</strong>, rifiutasse le impronte di slop prima del commit e imparasse da ogni output spedito?",
    }
)

STRINGS["problem_bridge_cta"] = k("That's v3.0. Keep scrolling.",
    **{"zh-CN":"那就是 v3.0。继续往下滑。","zh-TW":"那就是 v3.0。繼續往下捲。",
       "ja":"それが v3.0 だ。スクロールを続けて。","ko":"그것이 v3.0이다. 계속 스크롤하라.",
       "hi":"वही v3.0 है। scroll करते रहो।","id":"Itu v3.0. Lanjut scroll.",
       "vi":"Đó là v3.0. Cuộn tiếp đi.","th":"นั่นคือ v3.0 · เลื่อนต่อ",
       "ar":"تلك هي v3.0. تابع التمرير.","es":"Eso es v3.0. Sigue desplazándote.",
       "fr":"C&rsquo;est ça, v3.0. Continuez à scroller.","de":"Das ist v3.0. Weiterscrollen.",
       "pt-BR":"Isso é v3.0. Continue rolando.","ru":"Это v3.0. Скроль дальше.",
       "tr":"İşte v3.0. Kaydırmaya devam.","it":"Quello è v3.0. Continua a scrollare."})


# ============ 2. BRAIN ============
STRINGS["brain_eyebrow"] = k("02 &mdash; The architecture",
    **{"zh-CN":"02 &mdash; 架构","zh-TW":"02 &mdash; 架構","ja":"02 &mdash; アーキテクチャ","ko":"02 &mdash; 아키텍처","hi":"02 &mdash; आर्किटेक्चर",
       "id":"02 &mdash; Arsitektur","vi":"02 &mdash; Kiến trúc","th":"02 &mdash; สถาปัตยกรรม","ar":"02 &mdash; البنية المعماريّة",
       "es":"02 &mdash; La arquitectura","fr":"02 &mdash; L&rsquo;architecture","de":"02 &mdash; Die Architektur",
       "pt-BR":"02 &mdash; A arquitetura","ru":"02 &mdash; Архитектура","tr":"02 &mdash; Mimari","it":"02 &mdash; L&rsquo;architettura"})

STRINGS["brain_h2"] = k(
    "Brand specs are training data,<br>\n          <span class=\"accent-italic\">not templates.</span>",
    **{
        "zh-CN":"品牌规范是训练数据,<br>\n          <span class=\"accent-italic\">不是模板。</span>",
        "zh-TW":"品牌規範是訓練資料,<br>\n          <span class=\"accent-italic\">不是模板。</span>",
        "ja":"ブランド仕様はトレーニングデータ、<br>\n          <span class=\"accent-italic\">テンプレートじゃない。</span>",
        "ko":"브랜드 사양은 학습 데이터,<br>\n          <span class=\"accent-italic\">템플릿이 아니다.</span>",
        "hi":"ब्रांड specs ट्रेनिंग डेटा हैं,<br>\n          <span class=\"accent-italic\">टेम्पलेट नहीं।</span>",
        "id":"Spec brand adalah data latih,<br>\n          <span class=\"accent-italic\">bukan template.</span>",
        "vi":"Spec thương hiệu là dữ liệu huấn luyện,<br>\n          <span class=\"accent-italic\">không phải template.</span>",
        "th":"สเปกแบรนด์คือข้อมูลฝึก<br>\n          <span class=\"accent-italic\">ไม่ใช่เทมเพลต</span>",
        "ar":"مواصفات العلامات بيانات تدريب،<br>\n          <span class=\"accent-italic\">لا قوالب.</span>",
        "es":"Las specs de marca son datos de entrenamiento,<br>\n          <span class=\"accent-italic\">no plantillas.</span>",
        "fr":"Les specs de marque sont des données d&rsquo;entraînement,<br>\n          <span class=\"accent-italic\">pas des modèles.</span>",
        "de":"Brand-Specs sind Trainingsdaten,<br>\n          <span class=\"accent-italic\">keine Vorlagen.</span>",
        "pt-BR":"Specs de marca são dados de treino,<br>\n          <span class=\"accent-italic\">não templates.</span>",
        "ru":"Brand-спецификации &mdash; обучающие данные,<br>\n          <span class=\"accent-italic\">не шаблоны.</span>",
        "tr":"Marka spec'leri eğitim verisidir,<br>\n          <span class=\"accent-italic\">şablon değil.</span>",
        "it":"Le spec brand sono dati di addestramento,<br>\n          <span class=\"accent-italic\">non template.</span>",
    }
)

STRINGS["brain_lead"] = k(
    "The catalogue used to be a menu. Pick Stripe, get Stripe-flavored tokens. v3.0 turns that on its head: the 160 brand specs become vocabulary the engine distills from. Output is novel every call.",
    **{
        "zh-CN":"目录以前是菜单。选 Stripe,就拿 Stripe 风味的 tokens。v3.0 把这个翻转过来:160 个品牌规范变成引擎用来萃取的词汇表。每次调用输出都是新的。",
        "zh-TW":"目錄以前是菜單。選 Stripe,就拿 Stripe 風味的 tokens。v3.0 把這個翻轉過來:160 個品牌規範變成引擎用來萃取的詞彙表。每次呼叫輸出都是新的。",
        "ja":"カタログはかつてメニューだった。Stripe を選べば Stripe 風のトークンが出てくる。v3.0 はそれを反転する: 160 のブランド仕様はエンジンが蒸留する語彙になる。出力は呼び出すたびに新しい。",
        "ko":"카탈로그는 한때 메뉴였다. Stripe를 고르면 Stripe 풍 토큰이 나왔다. v3.0은 그걸 뒤집는다: 160개의 브랜드 사양이 엔진이 증류하는 어휘가 된다. 출력은 매 호출마다 새롭다.",
        "hi":"catalogue पहले menu था। Stripe चुनो, Stripe जैसा tokens मिलो। v3.0 इसे उल्टा कर देता है: 160 ब्रांड specs एक vocabulary बन जाते हैं जिससे engine distill करता है। हर call पर output नया।",
        "id":"Dulu katalog itu menu. Pilih Stripe, dapat token rasa Stripe. v3.0 membalik itu: 160 spec brand jadi kosakata yang disuling engine. Output baru setiap panggilan.",
        "vi":"Trước đây catalog là menu. Chọn Stripe, được token kiểu Stripe. v3.0 lật ngược điều đó: 160 spec thương hiệu trở thành vốn từ vựng mà engine chưng cất. Output mới mỗi lần gọi.",
        "th":"แคตตาล็อกเคยเป็นเมนู เลือก Stripe ก็ได้โทเค็นกลิ่น Stripe · v3.0 พลิกเรื่องนี้: 160 brand specs กลายเป็นคลังคำที่ engine สกัดจาก · output ใหม่ทุกครั้งที่เรียก",
        "ar":"كان الكتالوج قائمةً. تختار Stripe فتحصل على رموز بنكهتها. v3.0 يقلب الفكرة: 160 مواصفة علامة تصبح مفردات يستخلصها المحرّك. والمخرج جديد في كلّ استدعاء.",
        "es":"El catálogo era un menú. Eliges Stripe, obtienes tokens sabor Stripe. v3.0 da la vuelta: las 160 specs de marca se vuelven vocabulario del que el motor destila. La salida es nueva cada llamada.",
        "fr":"Le catalogue était un menu. Vous choisissiez Stripe, vous obteniez des tokens à la Stripe. v3.0 inverse la chose : les 160 specs de marque deviennent le vocabulaire que le moteur distille. La sortie est inédite à chaque appel.",
        "de":"Der Katalog war früher ein Menü. Wähl Stripe, bekomm Stripe-artige Tokens. v3.0 dreht das um: Die 160 Brand-Specs werden zum Vokabular, aus dem die Engine destilliert. Die Ausgabe ist bei jedem Aufruf neu.",
        "pt-BR":"O catálogo era um menu. Escolhia Stripe, levava tokens com sabor Stripe. v3.0 inverte isso: as 160 specs de marca viram vocabulário do qual o motor destila. A saída é nova a cada chamada.",
        "ru":"Каталог был меню. Выбрал Stripe &mdash; получил Stripe-вкусные токены. v3.0 переворачивает: 160 brand-спецификаций становятся словарём, из которого движок дистиллирует. Вывод нов каждый вызов.",
        "tr":"Katalog eskiden bir menüydü. Stripe'ı seç, Stripe tatlı token al. v3.0 bunu tersine çevirir: 160 marka spec'i motorun damıttığı bir söz dağarcığına dönüşür. Her çağrıda çıktı yenidir.",
        "it":"Il catalogo era un menu. Sceglievi Stripe, prendevi token con sapore Stripe. v3.0 ribalta la cosa: le 160 spec brand diventano vocabolario da cui il motore distilla. L&rsquo;output è inedito a ogni chiamata.",
    }
)

# Brain quote labels/lines
STRINGS["brain_before_label"] = k("Before v3 &middot; the catalogue picks",
    **{"zh-CN":"v3 之前 &middot; 目录在挑选","zh-TW":"v3 之前 &middot; 目錄在挑選",
       "ja":"v3 以前 &middot; カタログが選ぶ","ko":"v3 이전 &middot; 카탈로그가 고른다","hi":"v3 से पहले &middot; catalogue चुनता है",
       "id":"Sebelum v3 &middot; katalog yang memilih","vi":"Trước v3 &middot; catalog chọn","th":"ก่อน v3 &middot; แคตตาล็อกเลือกให้",
       "ar":"قبل v3 &middot; الكتالوج يختار","es":"Antes de v3 &middot; el catálogo elige",
       "fr":"Avant v3 &middot; le catalogue choisit","de":"Vor v3 &middot; der Katalog wählt",
       "pt-BR":"Antes da v3 &middot; o catálogo escolhe","ru":"До v3 &middot; каталог выбирает",
       "tr":"v3'ten önce &middot; katalog seçer","it":"Prima di v3 &middot; il catalogo sceglie"})

STRINGS["brain_after_label"] = k("After v3 &middot; the brain distills",
    **{"zh-CN":"v3 之后 &middot; 大脑在萃取","zh-TW":"v3 之後 &middot; 大腦在萃取",
       "ja":"v3 以後 &middot; 頭脳が蒸留する","ko":"v3 이후 &middot; 두뇌가 증류한다","hi":"v3 के बाद &middot; दिमाग distill करता है",
       "id":"Setelah v3 &middot; otaknya menyuling","vi":"Sau v3 &middot; bộ não chưng cất","th":"หลัง v3 &middot; สมองสกัด",
       "ar":"بعد v3 &middot; العقل يستخلص","es":"Después de v3 &middot; el cerebro destila",
       "fr":"Après v3 &middot; le cerveau distille","de":"Nach v3 &middot; das Gehirn destilliert",
       "pt-BR":"Depois da v3 &middot; o cérebro destila","ru":"После v3 &middot; мозг дистиллирует",
       "tr":"v3'ten sonra &middot; beyin damıtır","it":"Dopo v3 &middot; il cervello distilla"})

STRINGS["brain_before_line"] = k("Recommender returns a brand specimen.",
    **{"zh-CN":"推荐器返回一个品牌样本。","zh-TW":"推薦器回傳一個品牌樣本。","ja":"レコメンダーはブランドの標本を返す。",
       "ko":"추천기는 브랜드 표본을 반환한다.","hi":"recommender एक ब्रांड specimen लौटाता है।","id":"Recommender mengembalikan spesimen brand.",
       "vi":"Recommender trả về một mẫu thương hiệu.","th":"recommender คืนตัวอย่างแบรนด์","ar":"المُوصِّي يعيد عيّنة علامة.",
       "es":"El recomendador devuelve un espécimen de marca.","fr":"Le recommandeur renvoie un spécimen de marque.",
       "de":"Der Recommender liefert ein Brand-Exemplar.","pt-BR":"O recomendador devolve um espécime de marca.",
       "ru":"Рекомендатель возвращает образец бренда.","tr":"Önerici bir marka örneği döndürür.","it":"Il recommender restituisce un esemplare di brand."})

STRINGS["brain_before_body"] = k(
    "<code>match_brand(brief) &rarr; stripe</code><br>\n            You ship Stripe tokens. Or you fork them. Either way, the system has nothing new to say.",
    **{
        "zh-CN":"<code>match_brand(brief) &rarr; stripe</code><br>\n            你出 Stripe 的 tokens。或者你 fork 一份。无论哪种,系统都没有新东西可说。",
        "zh-TW":"<code>match_brand(brief) &rarr; stripe</code><br>\n            你出 Stripe 的 tokens。或者你 fork 一份。無論哪種,系統都沒有新東西可說。",
        "ja":"<code>match_brand(brief) &rarr; stripe</code><br>\n            あなたは Stripe のトークンを出荷する。あるいはフォークする。どちらにせよ、システムは新しいことを何も言えない。",
        "ko":"<code>match_brand(brief) &rarr; stripe</code><br>\n            당신은 Stripe 토큰을 출시한다. 또는 fork한다. 어느 쪽이든 시스템에 새로 할 말이 없다.",
        "hi":"<code>match_brand(brief) &rarr; stripe</code><br>\n            आप Stripe tokens ship करते हैं। या fork करते हैं। दोनों में, system के पास कहने को कुछ नया नहीं है।",
        "id":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Kamu ship token Stripe. Atau kamu fork. Bagaimanapun, sistem tidak punya hal baru untuk dikatakan.",
        "vi":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Bạn ship token Stripe. Hoặc bạn fork. Dù sao, hệ thống chẳng có gì mới để nói.",
        "th":"<code>match_brand(brief) &rarr; stripe</code><br>\n            คุณส่งโทเค็นของ Stripe หรือ fork ออกมา ไม่ว่าทางไหน ระบบก็ไม่มีอะไรใหม่จะพูด",
        "ar":"<code>match_brand(brief) &rarr; stripe</code><br>\n            تُسلِّم رموز Stripe، أو تُفرّعها. في الحالتين، لا جديد للنظام يقوله.",
        "es":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Envías tokens de Stripe. O los forkeas. Como sea, el sistema no tiene nada nuevo que decir.",
        "fr":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Vous livrez les tokens Stripe. Ou vous les forkez. Dans les deux cas, le système n&rsquo;a rien de neuf à dire.",
        "de":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Du lieferst Stripe-Tokens. Oder forkst sie. So oder so hat das System nichts Neues zu sagen.",
        "pt-BR":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Você envia tokens do Stripe. Ou faz fork. De qualquer jeito, o sistema não tem nada novo a dizer.",
        "ru":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Вы шипите токены Stripe. Или форкаете их. Так или иначе, системе нечего сказать нового.",
        "tr":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Stripe token'larını gönderirsin. Ya da fork edersin. Her iki yolda da sistem yeni bir şey söylemez.",
        "it":"<code>match_brand(brief) &rarr; stripe</code><br>\n            Spedisci i token di Stripe. O li forki. In ogni caso, il sistema non ha nulla di nuovo da dire.",
    }
)

STRINGS["brain_after_line"] = k("Synthesizer compiles a fresh design language.",
    **{"zh-CN":"合成器编译出全新的设计语言。","zh-TW":"合成器編譯出全新的設計語言。","ja":"合成器が新しいデザイン言語をコンパイルする。",
       "ko":"신디사이저가 새로운 디자인 언어를 컴파일한다.","hi":"synthesizer एक नई डिज़ाइन भाषा कंपाइल करता है।","id":"Synthesizer mengompilasi bahasa desain yang baru.",
       "vi":"Bộ tổng hợp biên dịch một ngôn ngữ thiết kế mới.","th":"synthesizer คอมไพล์ภาษาดีไซน์ใหม่","ar":"المولِّد يبني لغة تصميم جديدة.",
       "es":"El sintetizador compila un lenguaje de diseño nuevo.","fr":"Le synthétiseur compile un langage de design inédit.",
       "de":"Der Synthesizer kompiliert eine frische Designsprache.","pt-BR":"O sintetizador compila uma linguagem de design nova.",
       "ru":"Синтезатор компилирует новый дизайн-язык.","tr":"Sentezleyici yepyeni bir tasarım dili derler.","it":"Il sintetizzatore compila un linguaggio di design inedito."})

STRINGS["brain_after_body"] = k(
    "<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Same brief, same output, every time. Different brief, different system. The catalogue is now the corpus.",
    **{
        "zh-CN":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            同样的 brief,同样的 output,每次都一样。不同的 brief,不同的系统。目录现在变成了语料库。",
        "zh-TW":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            同樣的 brief,同樣的 output,每次都一樣。不同的 brief,不同的系統。目錄現在變成了語料庫。",
        "ja":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            同じブリーフ、同じ出力、毎回。違うブリーフなら違うシステム。カタログはいまや コーパスだ。",
        "ko":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            같은 브리프, 같은 결과, 매번. 다른 브리프, 다른 시스템. 카탈로그는 이제 코퍼스다.",
        "hi":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            एक ही brief, एक ही output, हर बार। अलग brief, अलग system। catalogue अब corpus है।",
        "id":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Brief sama, output sama, setiap kali. Brief berbeda, sistem berbeda. Katalog sekarang adalah korpus.",
        "vi":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Cùng brief, cùng output, mỗi lần. Brief khác, hệ thống khác. Catalog giờ là corpus.",
        "th":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            brief เดียวกัน output เดียวกัน ทุกครั้ง · brief ต่างกัน ระบบต่างกัน · แคตตาล็อกตอนนี้คือ corpus",
        "ar":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            الملخّص نفسه يُنتج المخرج نفسه دائمًا. ملخّص مختلف، نظام مختلف. الكتالوج الآن هو المتن.",
        "es":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Mismo brief, mismo output, cada vez. Brief distinto, sistema distinto. El catálogo ahora es el corpus.",
        "fr":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Même brief, même sortie, à chaque fois. Brief différent, système différent. Le catalogue est désormais le corpus.",
        "de":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Gleicher Brief, gleiches Ergebnis, jedes Mal. Anderer Brief, anderes System. Der Katalog ist jetzt der Korpus.",
        "pt-BR":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Mesmo brief, mesmo output, toda vez. Brief diferente, sistema diferente. O catálogo agora é o corpus.",
        "ru":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Тот же бриф, тот же вывод, каждый раз. Другой бриф &mdash; другая система. Каталог теперь &mdash; это корпус.",
        "tr":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Aynı brief, aynı çıktı, her seferinde. Farklı brief, farklı sistem. Katalog artık derlem.",
        "it":"<code>synthesize(brief) &rarr; novel tokens</code><br>\n            Stesso brief, stesso output, ogni volta. Brief diverso, sistema diverso. Il catalogo è ora il corpus.",
    }
)

# ============ 3. AXES ============
STRINGS["axes_eyebrow"] = k("03 &mdash; The 7 axes",
    **{"zh-CN":"03 &mdash; 七个轴","zh-TW":"03 &mdash; 七個軸","ja":"03 &mdash; 7 つの軸","ko":"03 &mdash; 7개의 축","hi":"03 &mdash; 7 अक्ष",
       "id":"03 &mdash; 7 aksis","vi":"03 &mdash; 7 trục","th":"03 &mdash; 7 แกน","ar":"03 &mdash; المحاور السبعة",
       "es":"03 &mdash; Los 7 ejes","fr":"03 &mdash; Les 7 axes","de":"03 &mdash; Die 7 Achsen",
       "pt-BR":"03 &mdash; Os 7 eixos","ru":"03 &mdash; 7 осей","tr":"03 &mdash; 7 eksen","it":"03 &mdash; I 7 assi"})

STRINGS["axes_h2"] = k(
    "Seven values.<br>\n          One design language.",
    **{
        "zh-CN":"七个数值。<br>\n          一种设计语言。",
        "zh-TW":"七個數值。<br>\n          一種設計語言。",
        "ja":"7 つの値。<br>\n          ひとつのデザイン言語。",
        "ko":"일곱 개의 값.<br>\n          하나의 디자인 언어.",
        "hi":"सात values।<br>\n          एक डिज़ाइन भाषा।",
        "id":"Tujuh nilai.<br>\n          Satu bahasa desain.",
        "vi":"Bảy giá trị.<br>\n          Một ngôn ngữ thiết kế.",
        "th":"เจ็ดค่า<br>\n          ภาษาดีไซน์เดียว",
        "ar":"سبع قيم.<br>\n          لغة تصميم واحدة.",
        "es":"Siete valores.<br>\n          Un lenguaje de diseño.",
        "fr":"Sept valeurs.<br>\n          Un langage de design.",
        "de":"Sieben Werte.<br>\n          Eine Designsprache.",
        "pt-BR":"Sete valores.<br>\n          Uma linguagem de design.",
        "ru":"Семь значений.<br>\n          Один дизайн-язык.",
        "tr":"Yedi değer.<br>\n          Tek tasarım dili.",
        "it":"Sette valori.<br>\n          Un linguaggio di design.",
    }
)

STRINGS["axes_lead"] = k(
    "Briefs map deterministically to seven axis values. Axis values compile to palette, type, spacing, radius, and motion tokens. Same brief always yields the same output.",
    **{
        "zh-CN":"brief 确定性地映射到七个轴值。轴值编译成调色板、字体、间距、圆角和动效 tokens。同样的 brief 永远产生同样的输出。",
        "zh-TW":"brief 確定性地映射到七個軸值。軸值編譯成調色盤、字體、間距、圓角和動效 tokens。同樣的 brief 永遠產生同樣的輸出。",
        "ja":"ブリーフは決定論的に 7 つの軸値にマッピングされる。軸値はパレット、タイポグラフィ、スペーシング、半径、モーションのトークンにコンパイルされる。同じブリーフは常に同じ出力を生む。",
        "ko":"브리프는 결정론적으로 일곱 개의 축 값에 매핑된다. 축 값은 팔레트, 타입, 스페이싱, 반경, 모션 토큰으로 컴파일된다. 같은 브리프는 항상 같은 결과를 낸다.",
        "hi":"briefs deterministically सात axis values पर map होते हैं। axis values palette, type, spacing, radius, और motion tokens में compile होते हैं। एक ही brief हमेशा एक ही output देता है।",
        "id":"Brief dipetakan deterministik ke tujuh nilai aksis. Nilai aksis dikompilasi menjadi token palette, type, spacing, radius, dan motion. Brief sama selalu memberi output sama.",
        "vi":"Brief ánh xạ xác định tới bảy giá trị trục. Giá trị trục biên dịch thành token palette, type, spacing, radius và motion. Cùng brief luôn cho cùng output.",
        "th":"brief แมปแบบ deterministic ไปยังเจ็ดค่าแกน · ค่าแกนคอมไพล์เป็นโทเค็น palette, type, spacing, radius และ motion · brief เดียวกันให้ output เดียวกันเสมอ",
        "ar":"الملخّصات تتعيَّن حتميًّا إلى سبع قيم على المحاور. القيم تُترجَم إلى رموز اللوحة اللونيّة والطباعة والتباعد ونصف القطر والحركة. الملخّص نفسه يعطي المخرج نفسه دائمًا.",
        "es":"Los briefs mapean de forma determinística a siete valores de eje. Los valores compilan a tokens de paleta, tipografía, spacing, radius y motion. Mismo brief, mismo resultado, siempre.",
        "fr":"Les briefs se mappent de façon déterministe à sept valeurs d&rsquo;axe. Les valeurs compilent en tokens de palette, typographie, spacing, radius et motion. Même brief, même sortie, toujours.",
        "de":"Briefs werden deterministisch auf sieben Achsenwerte abgebildet. Achsenwerte kompilieren zu Palette-, Typo-, Spacing-, Radius- und Motion-Tokens. Gleicher Brief liefert immer dasselbe Ergebnis.",
        "pt-BR":"Briefs mapeiam deterministicamente para sete valores de eixo. Os valores compilam em tokens de palette, type, spacing, radius e motion. Mesmo brief, mesmo output, sempre.",
        "ru":"Брифы детерминированно мапятся на семь значений осей. Значения компилируются в токены палитры, типографики, spacing, radius и motion. Один и тот же бриф всегда даёт один и тот же вывод.",
        "tr":"Brief'ler deterministik şekilde yedi eksen değerine eşlenir. Eksen değerleri palette, type, spacing, radius ve motion token'larına derlenir. Aynı brief her zaman aynı çıktıyı verir.",
        "it":"I brief mappano in modo deterministico a sette valori d&rsquo;asse. I valori compilano in token di palette, type, spacing, radius e motion. Stesso brief, stesso output, sempre.",
    }
)

# Axis names + ends
STRINGS["axis_warmth_name"] = k("Warmth",
    **{"zh-CN":"暖度","zh-TW":"暖度","ja":"暖かさ","ko":"따뜻함","hi":"गर्माहट",
       "id":"Kehangatan","vi":"Độ ấm","th":"ความอบอุ่น","ar":"الدفء",
       "es":"Calidez","fr":"Chaleur","de":"Wärme","pt-BR":"Calidez","ru":"Тепло","tr":"Sıcaklık","it":"Calore"})

STRINGS["axis_contrast_name"] = k("Contrast",
    **{"zh-CN":"对比度","zh-TW":"對比度","ja":"コントラスト","ko":"대비","hi":"कंट्रास्ट",
       "id":"Kontras","vi":"Tương phản","th":"คอนทราสต์","ar":"التباين",
       "es":"Contraste","fr":"Contraste","de":"Kontrast","pt-BR":"Contraste","ru":"Контраст","tr":"Kontrast","it":"Contrasto"})

STRINGS["axis_density_name"] = k("Density",
    **{"zh-CN":"密度","zh-TW":"密度","ja":"密度","ko":"밀도","hi":"घनत्व",
       "id":"Densitas","vi":"Mật độ","th":"ความหนาแน่น","ar":"الكثافة",
       "es":"Densidad","fr":"Densité","de":"Dichte","pt-BR":"Densidade","ru":"Плотность","tr":"Yoğunluk","it":"Densità"})

STRINGS["axis_geometry_name"] = k("Geometry",
    **{"zh-CN":"几何形态","zh-TW":"幾何形態","ja":"ジオメトリ","ko":"기하","hi":"ज्यामिति",
       "id":"Geometri","vi":"Hình học","th":"เรขาคณิต","ar":"الهندسة",
       "es":"Geometría","fr":"Géométrie","de":"Geometrie","pt-BR":"Geometria","ru":"Геометрия","tr":"Geometri","it":"Geometria"})

STRINGS["axis_formality_name"] = k("Formality",
    **{"zh-CN":"正式度","zh-TW":"正式度","ja":"フォーマリティ","ko":"격식","hi":"औपचारिकता",
       "id":"Formalitas","vi":"Tính trang trọng","th":"ความเป็นทางการ","ar":"الرسميّة",
       "es":"Formalidad","fr":"Formalité","de":"Formalität","pt-BR":"Formalidade","ru":"Формальность","tr":"Resmiyet","it":"Formalità"})

STRINGS["axis_motion_name"] = k("Motion",
    **{"zh-CN":"动效","zh-TW":"動效","ja":"モーション","ko":"모션","hi":"मोशन",
       "id":"Motion","vi":"Chuyển động","th":"การเคลื่อนไหว","ar":"الحركة",
       "es":"Motion","fr":"Motion","de":"Bewegung","pt-BR":"Motion","ru":"Анимация","tr":"Hareket","it":"Motion"})

STRINGS["axis_type_personality_name"] = k("Type personality",
    **{"zh-CN":"字体性格","zh-TW":"字體性格","ja":"タイプの性格","ko":"타이프 인격","hi":"टाइप व्यक्तित्व",
       "id":"Karakter tipografi","vi":"Cá tính chữ","th":"บุคลิกตัวอักษร","ar":"شخصيّة الخطّ",
       "es":"Personalidad tipográfica","fr":"Personnalité typographique","de":"Type-Persönlichkeit","pt-BR":"Personalidade tipográfica","ru":"Личность шрифта","tr":"Tipo karakteri","it":"Personalità tipografica"})

# Axis ends pairs — using unique strings per axis to avoid collisions
STRINGS["axis_end_cool"] = k("<span>Cool</span><span>Warm</span>",
    **{"zh-CN":"<span>冷</span><span>暖</span>","zh-TW":"<span>冷</span><span>暖</span>",
       "ja":"<span>クール</span><span>ウォーム</span>","ko":"<span>차가움</span><span>따뜻함</span>",
       "hi":"<span>ठंडा</span><span>गर्म</span>","id":"<span>Dingin</span><span>Hangat</span>",
       "vi":"<span>Lạnh</span><span>Ấm</span>","th":"<span>เย็น</span><span>อบอุ่น</span>",
       "ar":"<span>بارد</span><span>دافئ</span>","es":"<span>Frío</span><span>Cálido</span>",
       "fr":"<span>Froid</span><span>Chaud</span>","de":"<span>Kühl</span><span>Warm</span>",
       "pt-BR":"<span>Frio</span><span>Quente</span>","ru":"<span>Холодно</span><span>Тепло</span>",
       "tr":"<span>Soğuk</span><span>Sıcak</span>","it":"<span>Freddo</span><span>Caldo</span>"})

STRINGS["axis_end_quiet"] = k("<span>Quiet</span><span>Loud</span>",
    **{"zh-CN":"<span>安静</span><span>大声</span>","zh-TW":"<span>安靜</span><span>大聲</span>",
       "ja":"<span>静か</span><span>派手</span>","ko":"<span>조용함</span><span>큰소리</span>",
       "hi":"<span>शांत</span><span>तेज़</span>","id":"<span>Tenang</span><span>Lantang</span>",
       "vi":"<span>Yên</span><span>Gắt</span>","th":"<span>เงียบ</span><span>ดัง</span>",
       "ar":"<span>هادئ</span><span>صاخب</span>","es":"<span>Tranquilo</span><span>Fuerte</span>",
       "fr":"<span>Calme</span><span>Fort</span>","de":"<span>Leise</span><span>Laut</span>",
       "pt-BR":"<span>Quieto</span><span>Alto</span>","ru":"<span>Тихо</span><span>Громко</span>",
       "tr":"<span>Sakin</span><span>Yüksek</span>","it":"<span>Quieto</span><span>Forte</span>"})

STRINGS["axis_end_airy"] = k("<span>Airy</span><span>Dense</span>",
    **{"zh-CN":"<span>通透</span><span>密集</span>","zh-TW":"<span>通透</span><span>密集</span>",
       "ja":"<span>軽快</span><span>密集</span>","ko":"<span>여유</span><span>밀집</span>",
       "hi":"<span>हवादार</span><span>घना</span>","id":"<span>Lapang</span><span>Padat</span>",
       "vi":"<span>Thoáng</span><span>Dày</span>","th":"<span>โปร่ง</span><span>หนาแน่น</span>",
       "ar":"<span>منفتح</span><span>كثيف</span>","es":"<span>Aireado</span><span>Denso</span>",
       "fr":"<span>Aéré</span><span>Dense</span>","de":"<span>Luftig</span><span>Dicht</span>",
       "pt-BR":"<span>Arejado</span><span>Denso</span>","ru":"<span>Воздушно</span><span>Плотно</span>",
       "tr":"<span>Ferah</span><span>Yoğun</span>","it":"<span>Arioso</span><span>Denso</span>"})

STRINGS["axis_end_sharp"] = k("<span>Sharp</span><span>Soft</span>",
    **{"zh-CN":"<span>锐利</span><span>柔和</span>","zh-TW":"<span>銳利</span><span>柔和</span>",
       "ja":"<span>シャープ</span><span>ソフト</span>","ko":"<span>예리함</span><span>부드러움</span>",
       "hi":"<span>तीखा</span><span>नरम</span>","id":"<span>Tajam</span><span>Lembut</span>",
       "vi":"<span>Sắc</span><span>Mềm</span>","th":"<span>คม</span><span>นุ่ม</span>",
       "ar":"<span>حادّ</span><span>ناعم</span>","es":"<span>Filoso</span><span>Suave</span>",
       "fr":"<span>Tranchant</span><span>Doux</span>","de":"<span>Scharf</span><span>Weich</span>",
       "pt-BR":"<span>Afiado</span><span>Macio</span>","ru":"<span>Резко</span><span>Мягко</span>",
       "tr":"<span>Keskin</span><span>Yumuşak</span>","it":"<span>Tagliente</span><span>Morbido</span>"})

STRINGS["axis_end_casual"] = k("<span>Casual</span><span>Formal</span>",
    **{"zh-CN":"<span>随性</span><span>正式</span>","zh-TW":"<span>隨性</span><span>正式</span>",
       "ja":"<span>カジュアル</span><span>フォーマル</span>","ko":"<span>캐주얼</span><span>포멀</span>",
       "hi":"<span>कैज़ुअल</span><span>औपचारिक</span>","id":"<span>Santai</span><span>Formal</span>",
       "vi":"<span>Thoải mái</span><span>Trang trọng</span>","th":"<span>ลำลอง</span><span>เป็นทางการ</span>",
       "ar":"<span>عفويّ</span><span>رسميّ</span>","es":"<span>Casual</span><span>Formal</span>",
       "fr":"<span>Décontracté</span><span>Formel</span>","de":"<span>Lässig</span><span>Formell</span>",
       "pt-BR":"<span>Casual</span><span>Formal</span>","ru":"<span>Кэжуал</span><span>Формально</span>",
       "tr":"<span>Gündelik</span><span>Resmi</span>","it":"<span>Casual</span><span>Formale</span>"})

STRINGS["axis_end_still"] = k("<span>Still</span><span>Kinetic</span>",
    **{"zh-CN":"<span>静止</span><span>动感</span>","zh-TW":"<span>靜止</span><span>動感</span>",
       "ja":"<span>静止</span><span>キネティック</span>","ko":"<span>정적</span><span>운동성</span>",
       "hi":"<span>स्थिर</span><span>गतिशील</span>","id":"<span>Diam</span><span>Kinetik</span>",
       "vi":"<span>Tĩnh</span><span>Động</span>","th":"<span>นิ่ง</span><span>เคลื่อนไหว</span>",
       "ar":"<span>ساكن</span><span>متحرّك</span>","es":"<span>Quieto</span><span>Cinético</span>",
       "fr":"<span>Statique</span><span>Cinétique</span>","de":"<span>Statisch</span><span>Kinetisch</span>",
       "pt-BR":"<span>Estático</span><span>Cinético</span>","ru":"<span>Статика</span><span>Кинетика</span>",
       "tr":"<span>Durağan</span><span>Kinetik</span>","it":"<span>Fermo</span><span>Cinetico</span>"})

STRINGS["axis_end_neutral"] = k("<span>Neutral</span><span>Humanist</span>",
    **{"zh-CN":"<span>中性</span><span>人文</span>","zh-TW":"<span>中性</span><span>人文</span>",
       "ja":"<span>ニュートラル</span><span>ヒューマニスト</span>","ko":"<span>중립</span><span>휴머니스트</span>",
       "hi":"<span>तटस्थ</span><span>मानवीय</span>","id":"<span>Netral</span><span>Humanis</span>",
       "vi":"<span>Trung tính</span><span>Humanist</span>","th":"<span>กลาง</span><span>มนุษยนิยม</span>",
       "ar":"<span>محايد</span><span>إنسانيّ</span>","es":"<span>Neutro</span><span>Humanista</span>",
       "fr":"<span>Neutre</span><span>Humaniste</span>","de":"<span>Neutral</span><span>Humanistisch</span>",
       "pt-BR":"<span>Neutro</span><span>Humanista</span>","ru":"<span>Нейтрально</span><span>Гуманист</span>",
       "tr":"<span>Nötr</span><span>Hümanist</span>","it":"<span>Neutro</span><span>Umanista</span>"})

STRINGS["axis_compiles"] = k("compiles to",
    **{"zh-CN":"编译为","zh-TW":"編譯為","ja":"コンパイル先","ko":"컴파일 결과","hi":"compile होता है",
       "id":"dikompilasi ke","vi":"biên dịch thành","th":"คอมไพล์เป็น","ar":"يُترجَم إلى",
       "es":"compila a","fr":"compile vers","de":"kompiliert zu",
       "pt-BR":"compila em","ru":"компилируется в","tr":"şuna derlenir","it":"compila in"})

# ============ 4. MODES ============
STRINGS["modes_eyebrow"] = k("04 &mdash; The three modes",
    **{"zh-CN":"04 &mdash; 三种模式","zh-TW":"04 &mdash; 三種模式","ja":"04 &mdash; 3 つのモード","ko":"04 &mdash; 세 가지 모드","hi":"04 &mdash; तीन modes",
       "id":"04 &mdash; Tiga mode","vi":"04 &mdash; Ba chế độ","th":"04 &mdash; สามโหมด","ar":"04 &mdash; الأنماط الثلاثة",
       "es":"04 &mdash; Los tres modos","fr":"04 &mdash; Les trois modes","de":"04 &mdash; Die drei Modi",
       "pt-BR":"04 &mdash; Os três modos","ru":"04 &mdash; Три режима","tr":"04 &mdash; Üç mod","it":"04 &mdash; I tre modi"})

STRINGS["modes_h2"] = k(
    "Three modes.<br>\n          <span class=\"accent-italic\">Auto-dispatched.</span>",
    **{
        "zh-CN":"三种模式。<br>\n          <span class=\"accent-italic\">自动调度。</span>",
        "zh-TW":"三種模式。<br>\n          <span class=\"accent-italic\">自動調度。</span>",
        "ja":"3 つのモード。<br>\n          <span class=\"accent-italic\">自動ディスパッチ。</span>",
        "ko":"세 가지 모드.<br>\n          <span class=\"accent-italic\">자동 디스패치.</span>",
        "hi":"तीन modes।<br>\n          <span class=\"accent-italic\">अपने आप dispatch।</span>",
        "id":"Tiga mode.<br>\n          <span class=\"accent-italic\">Dispatch otomatis.</span>",
        "vi":"Ba chế độ.<br>\n          <span class=\"accent-italic\">Tự động dispatch.</span>",
        "th":"สามโหมด<br>\n          <span class=\"accent-italic\">ส่งงานอัตโนมัติ</span>",
        "ar":"ثلاثة أنماط.<br>\n          <span class=\"accent-italic\">يُختار النمط تلقائيًّا.</span>",
        "es":"Tres modos.<br>\n          <span class=\"accent-italic\">Despachados solos.</span>",
        "fr":"Trois modes.<br>\n          <span class=\"accent-italic\">Dispatch automatique.</span>",
        "de":"Drei Modi.<br>\n          <span class=\"accent-italic\">Automatisch dispatched.</span>",
        "pt-BR":"Três modos.<br>\n          <span class=\"accent-italic\">Despacho automático.</span>",
        "ru":"Три режима.<br>\n          <span class=\"accent-italic\">Авто-диспатч.</span>",
        "tr":"Üç mod.<br>\n          <span class=\"accent-italic\">Otomatik dispatch.</span>",
        "it":"Tre modi.<br>\n          <span class=\"accent-italic\">Dispatch automatico.</span>",
    }
)

STRINGS["modes_lead"] = k(
    "The synthesizer picks its own mode based on whether you anchored to a named brand. Strict for exact replication, anchor for guided variation, pure for infinity space.",
    **{
        "zh-CN":"合成器根据你是否锚定到某个具名品牌,自己选择模式。Strict 用于精确复刻,Anchor 用于引导式变化,Pure 用于无限空间。",
        "zh-TW":"合成器根據你是否錨定到某個具名品牌,自己選擇模式。Strict 用於精確複刻,Anchor 用於引導式變化,Pure 用於無限空間。",
        "ja":"合成器は、名前のあるブランドにアンカーしているかどうかに基づいて自分でモードを選ぶ。Strict は完全な複製、Anchor はガイド付きバリエーション、Pure は無限空間。",
        "ko":"신디사이저는 명명된 브랜드에 앵커했는지에 따라 스스로 모드를 고른다. Strict는 정확한 복제, Anchor는 가이드된 변형, Pure는 무한 공간.",
        "hi":"synthesizer अपना mode खुद चुनता है, इस आधार पर कि आपने किसी named brand पर anchor किया या नहीं। Strict exact replication के लिए, Anchor guided variation के लिए, Pure infinity space के लिए।",
        "id":"Synthesizer memilih mode-nya sendiri berdasarkan apakah kamu meng-anchor ke brand bernama. Strict untuk replikasi persis, Anchor untuk variasi terarah, Pure untuk ruang tak terbatas.",
        "vi":"Bộ tổng hợp tự chọn chế độ dựa trên việc bạn có anchor vào một brand có tên hay không. Strict cho sao chép chính xác, Anchor cho biến thể có hướng, Pure cho không gian vô tận.",
        "th":"synthesizer เลือกโหมดของตัวเอง โดยดูว่าคุณ anchor กับแบรนด์ที่มีชื่อหรือไม่ · Strict สำหรับลอกแบบเป๊ะ · Anchor สำหรับแปรผันแบบมีทิศ · Pure สำหรับพื้นที่ไม่จำกัด",
        "ar":"يختار المولِّد نمطه تلقائيًّا بناءً على ربطك بعلامة مسمَّاة أو عدمه. Strict للنسخ الدقيق، Anchor للتنويع الموجَّه، Pure للفضاء اللانهائيّ.",
        "es":"El sintetizador elige su modo según si te anclaste a una marca con nombre. Strict para réplica exacta, Anchor para variación guiada, Pure para espacio infinito.",
        "fr":"Le synthétiseur choisit son mode selon que vous êtes ancré ou non à une marque nommée. Strict pour la réplique exacte, Anchor pour la variation guidée, Pure pour l&rsquo;espace infini.",
        "de":"Der Synthesizer wählt seinen Modus selbst, je nachdem, ob du an eine benannte Marke geankert hast. Strict für exakte Replikation, Anchor für geführte Variation, Pure für Infinity Space.",
        "pt-BR":"O sintetizador escolhe o próprio modo conforme você ancorou ou não a uma marca nomeada. Strict para réplica exata, Anchor para variação guiada, Pure para espaço infinito.",
        "ru":"Синтезатор сам выбирает режим в зависимости от того, заякорились ли вы на именованный бренд. Strict для точной репликации, Anchor для направляемой вариации, Pure для бесконечного пространства.",
        "tr":"Sentezleyici, isimlendirilmiş bir markaya bağlanıp bağlanmadığına göre kendi modunu seçer. Strict tam kopya, Anchor yönlendirilmiş varyasyon, Pure sonsuz alan içindir.",
        "it":"Il sintetizzatore sceglie da solo il modo in base a se ti sei ancorato a un brand nominato. Strict per replica esatta, Anchor per variazione guidata, Pure per spazio infinito.",
    }
)

# Mode card 1
STRINGS["mode1_index"] = k("Mode 01 &middot; fastest",
    **{"zh-CN":"模式 01 &middot; 最快","zh-TW":"模式 01 &middot; 最快","ja":"モード 01 &middot; 最速","ko":"모드 01 &middot; 가장 빠름","hi":"Mode 01 &middot; सबसे तेज़",
       "id":"Mode 01 &middot; tercepat","vi":"Chế độ 01 &middot; nhanh nhất","th":"โหมด 01 &middot; เร็วที่สุด","ar":"النمط 01 &middot; الأسرع",
       "es":"Modo 01 &middot; el más rápido","fr":"Mode 01 &middot; le plus rapide","de":"Modus 01 &middot; am schnellsten",
       "pt-BR":"Modo 01 &middot; o mais rápido","ru":"Режим 01 &middot; самый быстрый","tr":"Mod 01 &middot; en hızlısı","it":"Modo 01 &middot; il più veloce"})

STRINGS["mode1_ratio"] = k("100% named brand &middot; verbatim",
    **{"zh-CN":"100% 命名品牌 &middot; 原样","zh-TW":"100% 命名品牌 &middot; 原樣","ja":"100% 名指しブランド &middot; そのまま",
       "ko":"100% 지정 브랜드 &middot; 그대로","hi":"100% named brand &middot; जैसा का तैसा","id":"100% brand bernama &middot; verbatim",
       "vi":"100% brand được nêu tên &middot; nguyên văn","th":"100% แบรนด์ที่ระบุชื่อ &middot; ตามต้นฉบับ","ar":"100% علامة مسمَّاة &middot; حرفيًّا",
       "es":"100% marca nombrada &middot; literal","fr":"100% marque nommée &middot; tel quel","de":"100% benannte Marke &middot; wortwörtlich",
       "pt-BR":"100% marca nomeada &middot; literal","ru":"100% именованный бренд &middot; дословно","tr":"%100 isimlendirilmiş marka &middot; aynen","it":"100% brand nominato &middot; letterale"})

STRINGS["mode1_body"] = k(
    "Anchor on a named brand with <code>strict=True</code>. 100% Stripe tokens, no axis adaptation. Fastest path. For when you know exactly what you want and the brief is \"give me Stripe.\"",
    **{
        "zh-CN":"用 <code>strict=True</code> 锚定到一个命名品牌。100% Stripe tokens,不做任何轴适配。最快路径。当你确切知道要什么、brief 就是「给我 Stripe」的时候用。",
        "zh-TW":"用 <code>strict=True</code> 錨定到一個命名品牌。100% Stripe tokens,不做任何軸適配。最快路徑。當你確切知道要什麼、brief 就是「給我 Stripe」的時候用。",
        "ja":"<code>strict=True</code> で名前のあるブランドにアンカー。100% Stripe トークン、軸の適応なし。最速経路。何が欲しいか正確に分かっていて、ブリーフが「Stripe をくれ」のときに。",
        "ko":"<code>strict=True</code>로 명명된 브랜드에 앵커. 100% Stripe 토큰, 축 적응 없음. 가장 빠른 경로. 원하는 걸 정확히 알고 브리프가 \"Stripe 줘\"일 때 쓴다.",
        "hi":"<code>strict=True</code> के साथ एक named brand पर anchor करें। 100% Stripe tokens, कोई axis adaptation नहीं। सबसे तेज़ रास्ता। जब आप ठीक-ठीक जानते हों कि क्या चाहिए और brief है \"मुझे Stripe दो।\"",
        "id":"Anchor ke brand bernama dengan <code>strict=True</code>. 100% token Stripe, tanpa adaptasi aksis. Jalur tercepat. Untuk saat kamu tahu pasti yang kamu mau dan brief-nya \"give me Stripe.\"",
        "vi":"Anchor vào một brand có tên với <code>strict=True</code>. 100% token Stripe, không thích nghi theo trục. Đường nhanh nhất. Khi bạn biết chính xác mình muốn gì và brief là \"give me Stripe.\"",
        "th":"anchor กับแบรนด์ที่มีชื่อด้วย <code>strict=True</code> · 100% โทเค็น Stripe ไม่มีการปรับตามแกน · เส้นทางเร็วที่สุด · ใช้เมื่อคุณรู้แน่ชัดว่าต้องการอะไร และ brief คือ \"give me Stripe\"",
        "ar":"اربط بعلامة مسمَّاة باستخدام <code>strict=True</code>. تحصل على رموز Stripe بنسبة 100% بلا تكييف على المحاور. أسرع مسار. حين تعرف تمامًا ما تريد، والملخّص: «أعطني Stripe.»",
        "es":"Ancla a una marca nombrada con <code>strict=True</code>. 100% tokens Stripe, sin adaptación de ejes. Camino más rápido. Para cuando sabes exactamente qué quieres y el brief es \"give me Stripe.\"",
        "fr":"Ancrez sur une marque nommée avec <code>strict=True</code>. 100% tokens Stripe, sans adaptation d&rsquo;axe. Chemin le plus rapide. Quand vous savez exactement ce que vous voulez et que le brief est « give me Stripe ».",
        "de":"Anker auf eine benannte Marke mit <code>strict=True</code>. 100% Stripe-Tokens, keine Achsen-Anpassung. Schnellster Weg. Für wenn du genau weißt, was du willst, und der Brief lautet „give me Stripe.\"",
        "pt-BR":"Ancore numa marca nomeada com <code>strict=True</code>. 100% tokens Stripe, sem adaptação de eixos. Caminho mais rápido. Para quando você sabe exatamente o que quer e o brief é \"give me Stripe.\"",
        "ru":"Заякорьте на именованный бренд с <code>strict=True</code>. 100% Stripe-токены, без адаптации осей. Самый быстрый путь. Когда вы точно знаете, что хотите, и бриф &mdash; «дай мне Stripe».",
        "tr":"İsimlendirilmiş bir markaya <code>strict=True</code> ile bağlan. %100 Stripe token, eksen uyarlaması yok. En hızlı yol. Tam olarak ne istediğini bildiğin ve brief'in \"give me Stripe\" olduğu zaman.",
        "it":"Ancora a un brand nominato con <code>strict=True</code>. 100% token Stripe, nessun adattamento d&rsquo;asse. Percorso più rapido. Per quando sai esattamente cosa vuoi e il brief è \"give me Stripe.\"",
    }
)

# Mode 2
STRINGS["mode2_index"] = k("Mode 02 &middot; the sweet spot",
    **{"zh-CN":"模式 02 &middot; 甜蜜点","zh-TW":"模式 02 &middot; 甜蜜點","ja":"モード 02 &middot; スイートスポット","ko":"모드 02 &middot; 스위트 스폿","hi":"Mode 02 &middot; sweet spot",
       "id":"Mode 02 &middot; titik manis","vi":"Chế độ 02 &middot; điểm ngọt","th":"โหมด 02 &middot; จุดที่ลงตัว","ar":"النمط 02 &middot; النقطة المثلى",
       "es":"Modo 02 &middot; el punto dulce","fr":"Mode 02 &middot; le sweet spot","de":"Modus 02 &middot; der Sweet Spot",
       "pt-BR":"Modo 02 &middot; o ponto ideal","ru":"Режим 02 &middot; sweet spot","tr":"Mod 02 &middot; tatlı nokta","it":"Modo 02 &middot; il punto dolce"})

STRINGS["mode2_ratio"] = k("70% named &middot; 30% axis adaptation",
    **{"zh-CN":"70% 命名 &middot; 30% 轴适配","zh-TW":"70% 命名 &middot; 30% 軸適配","ja":"70% 名指し &middot; 30% 軸適応",
       "ko":"70% 지정 &middot; 30% 축 적응","hi":"70% named &middot; 30% axis adaptation","id":"70% bernama &middot; 30% adaptasi aksis",
       "vi":"70% được nêu tên &middot; 30% thích nghi theo trục","th":"70% ระบุชื่อ &middot; 30% ปรับตามแกน","ar":"70% علامة مسمَّاة &middot; 30% تكييف على المحاور",
       "es":"70% nombrada &middot; 30% adaptación de ejes","fr":"70% nommée &middot; 30% adaptation d&rsquo;axe","de":"70% benannt &middot; 30% Achsen-Anpassung",
       "pt-BR":"70% nomeada &middot; 30% adaptação de eixos","ru":"70% именованный &middot; 30% адаптации осей","tr":"%70 isimlendirilmiş &middot; %30 eksen uyarlaması","it":"70% nominato &middot; 30% adattamento d&rsquo;asse"})

STRINGS["mode2_body"] = k(
    "Anchor on a named brand, then bend it toward the brief's axis values using four sibling brands as additional vocabulary. The variation that still smells like Stripe but feels like yours.",
    **{
        "zh-CN":"先锚定一个命名品牌,再用四个同族品牌作为额外词汇,把它朝 brief 的轴值弯过去。仍带着 Stripe 味道,但已经像你自己的变体。",
        "zh-TW":"先錨定一個命名品牌,再用四個同族品牌作為額外詞彙,把它朝 brief 的軸值彎過去。仍帶著 Stripe 味道,但已經像你自己的變體。",
        "ja":"名指しブランドにアンカーし、ブリーフの軸値に向けて曲げ、4 つの兄弟ブランドを追加語彙として使う。まだ Stripe の匂いはするが、あなたのものに感じられるバリエーション。",
        "ko":"명명된 브랜드에 앵커한 뒤, 네 개의 형제 브랜드를 추가 어휘로 사용하여 브리프의 축 값 쪽으로 구부린다. 여전히 Stripe 향이 나지만 당신의 것처럼 느껴지는 변형.",
        "hi":"एक named brand पर anchor करें, फिर चार sibling brands को additional vocabulary की तरह इस्तेमाल करते हुए brief के axis values की ओर मोड़ें। ऐसा variation जो अभी भी Stripe जैसा महकता है लेकिन अब आपका लगता है।",
        "id":"Anchor ke brand bernama, lalu bengkokkan ke arah nilai aksis brief menggunakan empat brand serumpun sebagai kosakata tambahan. Variasi yang masih beraroma Stripe tapi terasa milikmu.",
        "vi":"Anchor vào một brand có tên, rồi bẻ nó về phía giá trị trục của brief bằng bốn brand cùng họ làm vốn từ vựng bổ sung. Biến thể vẫn ngửi ra mùi Stripe nhưng đã có vẻ là của bạn.",
        "th":"anchor กับแบรนด์ที่มีชื่อ จากนั้นบิดไปทางค่าของแกนใน brief โดยใช้สี่แบรนด์พี่น้องเป็นคลังคำเพิ่มเติม · ได้ variation ที่ยังกลิ่น Stripe แต่รู้สึกเป็นของคุณ",
        "ar":"اربط بعلامة مسمَّاة، ثم احنها نحو قيم محاور الملخّص باستعمال أربع علامات شقيقة بوصفها مفردات إضافيّة. تنويع لا يزال له طابع Stripe، لكنّه يُحَسّ كأنّه عملك.",
        "es":"Anclas a una marca nombrada y la doblas hacia los valores de eje del brief usando cuatro marcas hermanas como vocabulario extra. La variación que aún huele a Stripe pero se siente tuya.",
        "fr":"Ancrez sur une marque nommée, puis penchez-la vers les valeurs d&rsquo;axe du brief en utilisant quatre marques sœurs comme vocabulaire supplémentaire. La variation qui sent encore Stripe mais qui vous appartient.",
        "de":"Verankere eine benannte Marke und biege sie mit vier Schwestermarken als zusätzlichem Vokabular in Richtung der Achsenwerte des Briefs. Die Variation, die noch nach Stripe riecht, sich aber wie deine anfühlt.",
        "pt-BR":"Ancore numa marca nomeada e a dobre na direção dos valores de eixo do brief usando quatro marcas-irmãs como vocabulário extra. A variação que ainda cheira a Stripe mas parece sua.",
        "ru":"Заякорьте на именованный бренд, затем согните его к значениям осей брифа, используя четыре родственных бренда как дополнительный словарь. Вариация, которая всё ещё пахнет Stripe, но ощущается вашей.",
        "tr":"İsimlendirilmiş bir markaya bağlan, sonra dört kardeş markayı ek söz dağarcığı olarak kullanarak onu brief'in eksen değerlerine doğru bük. Hâlâ Stripe gibi kokan ama seninkine benzeyen varyasyon.",
        "it":"Ancori a un brand nominato, poi lo pieghi verso i valori d&rsquo;asse del brief usando quattro brand fratelli come vocabolario extra. La variazione che sa ancora di Stripe ma sembra tua.",
    }
)

# Mode 3
STRINGS["mode3_index"] = k("Mode 03 &middot; infinity space",
    **{"zh-CN":"模式 03 &middot; 无限空间","zh-TW":"模式 03 &middot; 無限空間","ja":"モード 03 &middot; 無限空間","ko":"모드 03 &middot; 무한 공간","hi":"Mode 03 &middot; infinity space",
       "id":"Mode 03 &middot; ruang tak terbatas","vi":"Chế độ 03 &middot; không gian vô tận","th":"โหมด 03 &middot; พื้นที่ไม่จำกัด","ar":"النمط 03 &middot; فضاء لانهائيّ",
       "es":"Modo 03 &middot; espacio infinito","fr":"Mode 03 &middot; espace infini","de":"Modus 03 &middot; Infinity Space",
       "pt-BR":"Modo 03 &middot; espaço infinito","ru":"Режим 03 &middot; бесконечное пространство","tr":"Mod 03 &middot; sonsuz alan","it":"Modo 03 &middot; spazio infinito"})

STRINGS["mode3_ratio"] = k("0% named &middot; 100% axes",
    **{"zh-CN":"0% 命名 &middot; 100% 轴","zh-TW":"0% 命名 &middot; 100% 軸","ja":"0% 名指し &middot; 100% 軸",
       "ko":"0% 지정 &middot; 100% 축","hi":"0% named &middot; 100% axes","id":"0% bernama &middot; 100% aksis",
       "vi":"0% được nêu tên &middot; 100% trục","th":"0% ระบุชื่อ &middot; 100% แกน","ar":"0% علامة مسمَّاة &middot; 100% محاور",
       "es":"0% nombrada &middot; 100% ejes","fr":"0% nommée &middot; 100% axes","de":"0% benannt &middot; 100% Achsen",
       "pt-BR":"0% nomeada &middot; 100% eixos","ru":"0% именованный &middot; 100% оси","tr":"%0 isimlendirilmiş &middot; %100 eksen","it":"0% nominato &middot; 100% assi"})

STRINGS["mode3_body"] = k(
    "No brand named. The synthesizer picks 8 axis-matching exemplars from the catalogue and distills them into a novel design language. No single brand copied; their shared vocabulary harvested.",
    **{
        "zh-CN":"不指定品牌。合成器从目录中挑选 8 个与轴值匹配的样本,把它们萃取成全新的设计语言。没有复制任何单一品牌;只采集了它们共享的词汇。",
        "zh-TW":"不指定品牌。合成器從目錄中挑選 8 個與軸值匹配的樣本,把它們萃取成全新的設計語言。沒有複製任何單一品牌;只採集了它們共享的詞彙。",
        "ja":"ブランドの指名なし。合成器はカタログから軸に合う 8 つの典型を選び、新しいデザイン言語に蒸留する。単一のブランドを真似ない。共有された語彙だけを収穫する。",
        "ko":"명명된 브랜드 없음. 신디사이저는 카탈로그에서 축에 맞는 8개의 예시를 골라 새로운 디자인 언어로 증류한다. 단일 브랜드를 베끼지 않고 공유된 어휘만 거둔다.",
        "hi":"कोई brand named नहीं। synthesizer catalogue से 8 axis-matching exemplars चुनता है और उन्हें एक नई डिज़ाइन भाषा में distill करता है। कोई single brand copy नहीं; उनकी shared vocabulary harvest होती है।",
        "id":"Tidak ada brand yang disebut. Synthesizer memilih 8 contoh yang cocok dengan aksis dari katalog dan menyulingnya menjadi bahasa desain yang baru. Tidak ada satu brand pun yang ditiru; kosakata bersama mereka yang dipanen.",
        "vi":"Không nêu tên brand nào. Bộ tổng hợp chọn 8 ví dụ khớp trục từ catalog và chưng cất chúng thành một ngôn ngữ thiết kế mới. Không brand đơn lẻ nào bị sao chép; vốn từ vựng chung của họ được thu hoạch.",
        "th":"ไม่ระบุชื่อแบรนด์ · synthesizer หยิบ 8 ตัวอย่างที่แกนตรงกันจากแคตตาล็อก และสกัดเป็นภาษาดีไซน์ใหม่ · ไม่ลอกแบรนด์เดียว เก็บแต่คลังคำร่วม",
        "ar":"دون تسمية أيّ علامة. يختار المولِّد 8 نماذج مطابقة للمحاور من الكتالوج ويستخلصها في لغة تصميم جديدة. لا تقليد لعلامة بعينها؛ بل حصاد لمفرداتها المشتركة.",
        "es":"Sin marca nombrada. El sintetizador elige 8 exemplares que matchean los ejes y los destila en un lenguaje de diseño nuevo. Ninguna marca copiada; se cosecha el vocabulario que comparten.",
        "fr":"Aucune marque nommée. Le synthétiseur choisit 8 exemplaires qui matchent les axes dans le catalogue et les distille en un langage de design inédit. Aucune marque seule copiée ; leur vocabulaire commun moissonné.",
        "de":"Keine Marke benannt. Der Synthesizer wählt 8 achsen-passende Exemplare aus dem Katalog und destilliert sie zu einer frischen Designsprache. Keine einzelne Marke kopiert; ihr gemeinsames Vokabular geerntet.",
        "pt-BR":"Sem marca nomeada. O sintetizador escolhe 8 exemplares que dão match nos eixos e os destila em uma linguagem de design nova. Nenhuma marca única copiada; colhe-se o vocabulário compartilhado.",
        "ru":"Бренд не назван. Синтезатор берёт из каталога 8 примеров, подходящих по осям, и дистиллирует их в новый дизайн-язык. Ни один отдельный бренд не копируется; собирается их общий словарь.",
        "tr":"Marka adı yok. Sentezleyici, katalogdan eksenle eşleşen 8 örnek seçer ve bunları yeni bir tasarım diline damıtır. Tek bir marka kopyalanmaz; ortak söz dağarcıkları hasat edilir.",
        "it":"Nessun brand nominato. Il sintetizzatore sceglie 8 esemplari che matchano gli assi dal catalogo e li distilla in un linguaggio di design inedito. Nessun singolo brand copiato; il loro vocabolario comune raccolto.",
    }
)

# ============ 5. LOOP ============
STRINGS["loop_eyebrow"] = k("05 &mdash; The intelligence loop",
    **{"zh-CN":"05 &mdash; 智能循环","zh-TW":"05 &mdash; 智能循環","ja":"05 &mdash; インテリジェンス・ループ","ko":"05 &mdash; 인텔리전스 루프","hi":"05 &mdash; इंटेलिजेंस loop",
       "id":"05 &mdash; Loop kecerdasan","vi":"05 &mdash; Vòng lặp trí thông minh","th":"05 &mdash; ลูปอัจฉริยะ","ar":"05 &mdash; حلقة الذكاء",
       "es":"05 &mdash; El loop de inteligencia","fr":"05 &mdash; La boucle d&rsquo;intelligence","de":"05 &mdash; Die Intelligence-Loop",
       "pt-BR":"05 &mdash; O loop de inteligência","ru":"05 &mdash; Цикл интеллекта","tr":"05 &mdash; Zeka döngüsü","it":"05 &mdash; Il loop d&rsquo;intelligenza"})

STRINGS["loop_h2"] = k(
    "The brain learns<br>\n          <span class=\"accent-italic\">from itself.</span>",
    **{
        "zh-CN":"大脑从<br>\n          <span class=\"accent-italic\">自己学习。</span>",
        "zh-TW":"大腦從<br>\n          <span class=\"accent-italic\">自己學習。</span>",
        "ja":"頭脳は<br>\n          <span class=\"accent-italic\">自分から学ぶ。</span>",
        "ko":"두뇌는<br>\n          <span class=\"accent-italic\">자기 자신에게서 배운다.</span>",
        "hi":"दिमाग<br>\n          <span class=\"accent-italic\">खुद से सीखता है।</span>",
        "id":"Otaknya belajar<br>\n          <span class=\"accent-italic\">dari dirinya sendiri.</span>",
        "vi":"Bộ não học<br>\n          <span class=\"accent-italic\">từ chính mình.</span>",
        "th":"สมองเรียนรู้<br>\n          <span class=\"accent-italic\">จากตัวมันเอง</span>",
        "ar":"العقل يتعلَّم<br>\n          <span class=\"accent-italic\">من نفسه.</span>",
        "es":"El cerebro aprende<br>\n          <span class=\"accent-italic\">de sí mismo.</span>",
        "fr":"Le cerveau apprend<br>\n          <span class=\"accent-italic\">de lui-même.</span>",
        "de":"Das Gehirn lernt<br>\n          <span class=\"accent-italic\">aus sich selbst.</span>",
        "pt-BR":"O cérebro aprende<br>\n          <span class=\"accent-italic\">consigo mesmo.</span>",
        "ru":"Мозг учится<br>\n          <span class=\"accent-italic\">у самого себя.</span>",
        "tr":"Beyin kendinden<br>\n          <span class=\"accent-italic\">öğrenir.</span>",
        "it":"Il cervello impara<br>\n          <span class=\"accent-italic\">da sé.</span>",
    }
)

STRINGS["loop_lead"] = k(
    "Every call writes to <code>.ux/decisions.jsonl</code>. The recommender re-ranks future candidates by your past wins in the same industry plus UI-type bucket. Cold-start safe. Local only.",
    **{
        "zh-CN":"每次调用都写入 <code>.ux/decisions.jsonl</code>。推荐器根据你在同一行业 + UI 类型 bucket 中过去胜出的记录,重新排序未来的候选。冷启动安全。仅本地。",
        "zh-TW":"每次呼叫都寫入 <code>.ux/decisions.jsonl</code>。推薦器根據你在同一產業 + UI 類型 bucket 中過去勝出的紀錄,重新排序未來的候選。冷啟動安全。僅本地。",
        "ja":"呼び出すたびに <code>.ux/decisions.jsonl</code> に書き込む。レコメンダーは、同じ業界 + UI タイプのバケット内であなたが過去に勝った記録に基づき、未来の候補を再ランク付けする。コールドスタートに安全。ローカルのみ。",
        "ko":"모든 호출이 <code>.ux/decisions.jsonl</code>에 기록된다. 추천기는 같은 산업 + UI 타입 버킷에서 당신의 과거 승리에 따라 미래 후보를 재순위한다. 콜드 스타트 안전. 로컬 전용.",
        "hi":"हर call <code>.ux/decisions.jsonl</code> में लिखता है। recommender उसी industry + UI-type bucket में आपकी पिछली जीत के आधार पर future candidates को re-rank करता है। Cold-start safe। केवल local।",
        "id":"Setiap panggilan menulis ke <code>.ux/decisions.jsonl</code>. Recommender me-rank ulang kandidat masa depan berdasarkan kemenanganmu sebelumnya di bucket industry + UI-type yang sama. Aman cold-start. Lokal saja.",
        "vi":"Mỗi lần gọi ghi vào <code>.ux/decisions.jsonl</code>. Recommender xếp hạng lại các ứng viên tương lai theo những chiến thắng trước đây của bạn trong cùng bucket industry + UI-type. An toàn cold-start. Chỉ local.",
        "th":"ทุก call จะเขียนลงใน <code>.ux/decisions.jsonl</code> · recommender จัดอันดับ candidate ใหม่ตามที่คุณเคยชนะใน bucket industry + UI-type เดียวกัน · cold-start ปลอดภัย · บนเครื่องเท่านั้น",
        "ar":"كلّ استدعاء يُكتب في <code>.ux/decisions.jsonl</code>. يُعيد المُوصِّي ترتيب المرشَّحين المستقبليّين بناءً على نجاحاتك السابقة في نفس مجموعة الصناعة ونوع الواجهة. آمن مع البدء البارد. محلّيّ فقط.",
        "es":"Cada llamada escribe en <code>.ux/decisions.jsonl</code>. El recomendador rerankea los próximos candidatos según tus victorias pasadas en el mismo bucket de industria + tipo de UI. Cold-start seguro. Solo local.",
        "fr":"Chaque appel écrit dans <code>.ux/decisions.jsonl</code>. Le recommandeur reclasse les futurs candidats selon vos victoires passées dans le même bucket industrie + UI-type. Cold-start safe. Local uniquement.",
        "de":"Jeder Aufruf schreibt nach <code>.ux/decisions.jsonl</code>. Der Recommender ranked künftige Kandidaten anhand deiner vergangenen Erfolge im selben Branche- + UI-Type-Bucket neu. Cold-Start-sicher. Nur lokal.",
        "pt-BR":"Cada chamada grava em <code>.ux/decisions.jsonl</code>. O recomendador re-ranqueia futuros candidatos pelas suas vitórias passadas no mesmo bucket de indústria + UI-type. Cold-start seguro. Apenas local.",
        "ru":"Каждый вызов пишет в <code>.ux/decisions.jsonl</code>. Рекомендатель пере-ранжирует будущих кандидатов по вашим прошлым победам в том же bucket индустрии + UI-типа. Cold-start безопасен. Только локально.",
        "tr":"Her çağrı <code>.ux/decisions.jsonl</code> dosyasına yazar. Önerici, aynı sektör + UI-type bucket'ında geçmiş kazanımlarına göre gelecek adayları yeniden sıralar. Cold-start güvenli. Yalnızca yerel.",
        "it":"Ogni chiamata scrive su <code>.ux/decisions.jsonl</code>. Il recommender ri-classifica i candidati futuri in base alle tue vittorie passate nello stesso bucket settore + tipo UI. Cold-start safe. Solo locale.",
    }
)

STRINGS["loop_caption"] = k(
    "<strong>The intelligence loop is now closed.</strong> Only decisions with lint_score &ge; 80 and user_accepted = true count toward future re-ranking. Your install gets sharper for the work you actually ship.",
    **{
        "zh-CN":"<strong>智能循环已经闭合。</strong>只有 lint_score &ge; 80 且 user_accepted = true 的决策才会计入未来重排序。你的安装会随着你真正出货的工作越变越锋利。",
        "zh-TW":"<strong>智能循環已經閉合。</strong>只有 lint_score &ge; 80 且 user_accepted = true 的決策才會計入未來重排序。你的安裝會隨著你真正出貨的工作越變越鋒利。",
        "ja":"<strong>インテリジェンス・ループは閉じた。</strong>未来の再ランク付けに数えられるのは、lint_score &ge; 80 かつ user_accepted = true の決定のみ。あなたが実際に出荷する仕事に対して、インストールは鋭くなっていく。",
        "ko":"<strong>인텔리전스 루프가 이제 닫혔다.</strong> 미래 재순위에는 lint_score &ge; 80이고 user_accepted = true인 결정만 반영된다. 당신이 실제로 출시하는 작업에 맞춰 설치가 더 날카로워진다.",
        "hi":"<strong>intelligence loop अब बंद हो गया है।</strong> केवल वो decisions जिनका lint_score &ge; 80 और user_accepted = true हो, future re-ranking में गिने जाते हैं। आप जो वास्तव में ship करते हैं, उसके लिए आपका install धारदार होता जाता है।",
        "id":"<strong>Loop kecerdasan kini tertutup.</strong> Hanya decisions dengan lint_score &ge; 80 dan user_accepted = true yang dihitung untuk re-ranking ke depan. Install kamu semakin tajam untuk pekerjaan yang benar-benar kamu kirim.",
        "vi":"<strong>Vòng lặp trí thông minh giờ đã khép.</strong> Chỉ những decisions có lint_score &ge; 80 và user_accepted = true mới được tính vào re-ranking trong tương lai. Bản install của bạn sắc bén hơn với công việc bạn thật sự ship.",
        "th":"<strong>ลูปอัจฉริยะปิดวงครบแล้ว</strong> เฉพาะ decisions ที่มี lint_score &ge; 80 และ user_accepted = true เท่านั้นที่นับใน re-ranking ในอนาคต install ของคุณจะคมขึ้นเรื่อย ๆ สำหรับงานที่คุณส่งจริง",
        "ar":"<strong>اكتملت حلقة الذكاء.</strong> ولا تُحسب في إعادة الترتيب المقبلة سوى القرارات التي يكون فيها lint_score &ge; 80 وuser_accepted = true. تثبيتك يصبح أكثر حِدّةً مع العمل الذي تُسلّمه فعلًا.",
        "es":"<strong>El loop de inteligencia ya está cerrado.</strong> Solo cuentan para el re-ranking futuro las decisions con lint_score &ge; 80 y user_accepted = true. Tu instalación se afila con el trabajo que realmente envías.",
        "fr":"<strong>La boucle d&rsquo;intelligence est désormais fermée.</strong> Seules les décisions avec lint_score &ge; 80 et user_accepted = true comptent pour le re-ranking futur. Votre install s&rsquo;affine pour le travail que vous livrez vraiment.",
        "de":"<strong>Die Intelligence-Loop ist jetzt geschlossen.</strong> Nur Entscheidungen mit lint_score &ge; 80 und user_accepted = true zählen fürs künftige Re-Ranking. Deine Installation wird schärfer für die Arbeit, die du tatsächlich auslieferst.",
        "pt-BR":"<strong>O loop de inteligência agora está fechado.</strong> Só decisions com lint_score &ge; 80 e user_accepted = true contam para o re-ranking futuro. Sua instalação fica mais afiada para o trabalho que você de fato envia.",
        "ru":"<strong>Цикл интеллекта теперь замкнут.</strong> В будущем переранжировании учитываются только решения с lint_score &ge; 80 и user_accepted = true. Ваша установка становится острее под ту работу, которую вы реально шипите.",
        "tr":"<strong>Zeka döngüsü artık kapalı.</strong> Gelecek re-ranking'e yalnızca lint_score &ge; 80 ve user_accepted = true olan kararlar sayılır. Kurulumun, gerçekten gönderdiğin işe göre daha keskinleşir.",
        "it":"<strong>Il loop d&rsquo;intelligenza è ora chiuso.</strong> Solo le decisioni con lint_score &ge; 80 e user_accepted = true contano per il re-ranking futuro. La tua install diventa più affilata per il lavoro che effettivamente spedisci.",
    }
)

# ============ 6. DOGFOOD ============
STRINGS["dogfood_eyebrow"] = k("06 &mdash; The dogfood",
    **{"zh-CN":"06 &mdash; 自食其狗粮","zh-TW":"06 &mdash; 自食其狗糧","ja":"06 &mdash; ドッグフーディング","ko":"06 &mdash; 도그푸드","hi":"06 &mdash; डॉगफूड",
       "id":"06 &mdash; Dogfood","vi":"06 &mdash; Dogfood","th":"06 &mdash; กินอาหารหมาตัวเอง","ar":"06 &mdash; طعامنا الخاصّ",
       "es":"06 &mdash; El dogfood","fr":"06 &mdash; Le dogfood","de":"06 &mdash; Das Dogfood",
       "pt-BR":"06 &mdash; O dogfood","ru":"06 &mdash; Догфуд","tr":"06 &mdash; Dogfood","it":"06 &mdash; Il dogfood"})

STRINGS["dogfood_h2"] = k(
    "This page was synthesized<br>\n          <span class=\"accent-italic\">by v3.0 itself.</span>",
    **{
        "zh-CN":"这一页是<br>\n          <span class=\"accent-italic\">v3.0 自己合成的。</span>",
        "zh-TW":"這一頁是<br>\n          <span class=\"accent-italic\">v3.0 自己合成的。</span>",
        "ja":"このページは<br>\n          <span class=\"accent-italic\">v3.0 自身が合成した。</span>",
        "ko":"이 페이지는<br>\n          <span class=\"accent-italic\">v3.0이 직접 합성했다.</span>",
        "hi":"यह page<br>\n          <span class=\"accent-italic\">v3.0 ने खुद synthesize किया है।</span>",
        "id":"Halaman ini disintesis<br>\n          <span class=\"accent-italic\">oleh v3.0 sendiri.</span>",
        "vi":"Trang này được tổng hợp<br>\n          <span class=\"accent-italic\">bởi chính v3.0.</span>",
        "th":"หน้านี้ถูกสังเคราะห์<br>\n          <span class=\"accent-italic\">โดย v3.0 เอง</span>",
        "ar":"هذه الصفحة وُلِّدت<br>\n          <span class=\"accent-italic\">بواسطة v3.0 نفسها.</span>",
        "es":"Esta página fue sintetizada<br>\n          <span class=\"accent-italic\">por v3.0 misma.</span>",
        "fr":"Cette page a été synthétisée<br>\n          <span class=\"accent-italic\">par v3.0 elle-même.</span>",
        "de":"Diese Seite wurde<br>\n          <span class=\"accent-italic\">von v3.0 selbst synthetisiert.</span>",
        "pt-BR":"Esta página foi sintetizada<br>\n          <span class=\"accent-italic\">pelo próprio v3.0.</span>",
        "ru":"Эта страница синтезирована<br>\n          <span class=\"accent-italic\">самим v3.0.</span>",
        "tr":"Bu sayfa<br>\n          <span class=\"accent-italic\">v3.0'ın kendisi tarafından sentezlendi.</span>",
        "it":"Questa pagina è stata sintetizzata<br>\n          <span class=\"accent-italic\">da v3.0 stesso.</span>",
    }
)

STRINGS["dogfood_lead"] = k(
    "We ran the synthesizer on a brief that describes this page. The tokens it emitted power what you are reading right now. The brain ships its own marketing.",
    **{
        "zh-CN":"我们用一个描述这页本身的 brief 跑了合成器。它发出的 tokens 驱动着你现在正在读的一切。大脑自己出自己的市场材料。",
        "zh-TW":"我們用一個描述這頁本身的 brief 跑了合成器。它發出的 tokens 驅動著你現在正在讀的一切。大腦自己出自己的市場材料。",
        "ja":"このページ自体を記述したブリーフで合成器を走らせた。出てきたトークンが、今あなたが読んでいるものを駆動している。頭脳は自分のマーケティングを出荷する。",
        "ko":"이 페이지를 묘사하는 브리프로 신디사이저를 돌렸다. 그것이 내놓은 토큰이 지금 당신이 읽는 것을 구동한다. 두뇌가 자기 마케팅을 출시한다.",
        "hi":"हमने इस page को describe करने वाली एक brief पर synthesizer चलाया। उसने जो tokens दिए, वे अभी आप जो पढ़ रहे हैं उसे चला रहे हैं। दिमाग अपनी marketing खुद ship करता है।",
        "id":"Kami menjalankan synthesizer dengan brief yang mendeskripsikan halaman ini. Token yang dikeluarkan menggerakkan apa yang sedang kamu baca. Otaknya mengirim marketing-nya sendiri.",
        "vi":"Chúng tôi chạy bộ tổng hợp với một brief mô tả chính trang này. Token nó phát ra đang vận hành thứ bạn đang đọc lúc này. Bộ não tự ship marketing của mình.",
        "th":"เราเอา synthesizer ไปรันบน brief ที่อธิบายหน้านี้ · โทเค็นที่มันส่งออกมาขับเคลื่อนสิ่งที่คุณกำลังอ่านอยู่ตอนนี้ · สมองส่งงานการตลาดของตัวเอง",
        "ar":"شغّلنا المولِّد على ملخّص يصف هذه الصفحة. الرموز التي أنتجها هي ما يُحرِّك ما تقرؤه الآن. العقل يُسلِّم تسويقه بنفسه.",
        "es":"Corrimos el sintetizador sobre un brief que describe esta página. Los tokens que emitió impulsan lo que estás leyendo ahora. El cerebro entrega su propio marketing.",
        "fr":"Nous avons fait tourner le synthétiseur sur un brief qui décrit cette page. Les tokens qu&rsquo;il a émis font marcher ce que vous lisez en ce moment. Le cerveau livre son propre marketing.",
        "de":"Wir haben den Synthesizer auf einen Brief losgelassen, der diese Seite beschreibt. Die ausgegebenen Tokens treiben das an, was du gerade liest. Das Gehirn liefert sein eigenes Marketing.",
        "pt-BR":"Rodamos o sintetizador num brief que descreve esta página. Os tokens que ele emitiu movimentam o que você está lendo agora. O cérebro entrega o próprio marketing.",
        "ru":"Мы прогнали синтезатор по брифу, описывающему эту страницу. Выданные им токены питают то, что вы сейчас читаете. Мозг шипит собственный маркетинг.",
        "tr":"Sentezleyiciyi bu sayfayı tanımlayan bir brief üzerinde çalıştırdık. Çıkardığı token'lar şu an okuduğun şeyi yürütüyor. Beyin kendi pazarlamasını gönderiyor.",
        "it":"Abbiamo eseguito il sintetizzatore su un brief che descrive questa pagina. I token che ha emesso muovono ciò che stai leggendo ora. Il cervello spedisce il proprio marketing.",
    }
)

STRINGS["dogfood_label_brief"] = k("The brief",
    **{"zh-CN":"brief","zh-TW":"brief","ja":"ブリーフ","ko":"브리프","hi":"brief",
       "id":"Brief-nya","vi":"Brief","th":"brief","ar":"الملخّص",
       "es":"El brief","fr":"Le brief","de":"Der Brief","pt-BR":"O brief","ru":"Бриф","tr":"Brief","it":"Il brief"})

STRINGS["dogfood_label_mode"] = k("Mode dispatched",
    **{"zh-CN":"调度的模式","zh-TW":"調度的模式","ja":"ディスパッチされたモード","ko":"디스패치된 모드","hi":"dispatched mode",
       "id":"Mode yang dispatch","vi":"Chế độ dispatch","th":"โหมดที่ส่งงาน","ar":"النمط المُختار",
       "es":"Modo despachado","fr":"Mode dispatché","de":"Dispatchter Modus","pt-BR":"Modo despachado","ru":"Выбранный режим","tr":"Dispatch edilen mod","it":"Modo dispatched"})

STRINGS["dogfood_label_axes"] = k("The 7 axis values",
    **{"zh-CN":"七个轴值","zh-TW":"七個軸值","ja":"7 つの軸値","ko":"7개의 축 값","hi":"7 axis values",
       "id":"7 nilai aksis","vi":"7 giá trị trục","th":"ค่า 7 แกน","ar":"قيم المحاور السبعة",
       "es":"Los 7 valores de eje","fr":"Les 7 valeurs d&rsquo;axe","de":"Die 7 Achsenwerte","pt-BR":"Os 7 valores de eixo","ru":"7 значений осей","tr":"7 eksen değeri","it":"I 7 valori d&rsquo;asse"})

STRINGS["dogfood_label_exemplars"] = k("Source exemplars (8)",
    **{"zh-CN":"源样本 (8)","zh-TW":"源樣本 (8)","ja":"ソース典型 (8)","ko":"소스 예시 (8)","hi":"source exemplars (8)",
       "id":"Eksemplar sumber (8)","vi":"Ví dụ nguồn (8)","th":"ตัวอย่างต้นทาง (8)","ar":"النماذج المصدر (8)",
       "es":"Exemplares fuente (8)","fr":"Exemplaires sources (8)","de":"Quell-Exemplare (8)","pt-BR":"Exemplares fonte (8)","ru":"Исходные примеры (8)","tr":"Kaynak örnek (8)","it":"Esemplari sorgente (8)"})

STRINGS["dogfood_label_palette"] = k("Synthesized palette",
    **{"zh-CN":"合成的调色板","zh-TW":"合成的調色盤","ja":"合成パレット","ko":"합성된 팔레트","hi":"synthesized palette",
       "id":"Palette tersintesis","vi":"Palette đã tổng hợp","th":"พาเลตที่สังเคราะห์","ar":"اللوحة اللونيّة المولَّدة",
       "es":"Paleta sintetizada","fr":"Palette synthétisée","de":"Synthetisierte Palette","pt-BR":"Paleta sintetizada","ru":"Синтезированная палитра","tr":"Sentezlenmiş palet","it":"Palette sintetizzata"})

STRINGS["dogfood_label_type_pair"] = k("Synthesized type pair",
    **{"zh-CN":"合成的字体配对","zh-TW":"合成的字體配對","ja":"合成タイプペア","ko":"합성된 타입 페어","hi":"synthesized type pair",
       "id":"Pasangan type tersintesis","vi":"Cặp type đã tổng hợp","th":"คู่ตัวอักษรที่สังเคราะห์","ar":"زوج الخطّ المولَّد",
       "es":"Par tipográfico sintetizado","fr":"Paire typographique synthétisée","de":"Synthetisiertes Type-Paar","pt-BR":"Par tipográfico sintetizado","ru":"Синтезированная пара шрифтов","tr":"Sentezlenmiş tipo çifti","it":"Coppia tipografica sintetizzata"})

STRINGS["dogfood_label_component"] = k("Mini-component &mdash; rendered in the synthesized palette as the brain emitted it",
    **{"zh-CN":"迷你组件 &mdash; 用大脑发出的合成调色板渲染","zh-TW":"迷你元件 &mdash; 用大腦發出的合成調色盤渲染",
       "ja":"ミニコンポーネント &mdash; 頭脳が出した合成パレットでレンダリング","ko":"미니 컴포넌트 &mdash; 두뇌가 내놓은 합성 팔레트로 렌더링",
       "hi":"मिनी-component &mdash; उसी synthesized palette में render जो दिमाग ने दिया","id":"Mini-komponen &mdash; di-render dengan palette tersintesis seperti yang otak keluarkan",
       "vi":"Mini-component &mdash; render bằng palette đã tổng hợp đúng như bộ não phát ra","th":"มินิคอมโพเนนต์ &mdash; เรนเดอร์ในพาเลตที่สมองส่งออกมา",
       "ar":"مكوِّن مصغَّر &mdash; مرسوم باللوحة اللونيّة كما أنتجها العقل","es":"Mini-componente &mdash; renderizado en la paleta sintetizada como la emitió el cerebro",
       "fr":"Mini-composant &mdash; rendu dans la palette synthétisée telle que le cerveau l&rsquo;a émise","de":"Mini-Komponente &mdash; in der synthetisierten Palette gerendert, wie das Gehirn sie ausgegeben hat",
       "pt-BR":"Mini-componente &mdash; renderizado na paleta sintetizada como o cérebro emitiu","ru":"Мини-компонент &mdash; отрисован в синтезированной палитре, как её выдал мозг",
       "tr":"Mini bileşen &mdash; beynin verdiği sentezlenmiş paletle render edildi","it":"Mini-componente &mdash; renderizzato nella palette sintetizzata come il cervello l&rsquo;ha emessa"})

STRINGS["dogfood_card_title"] = k("Card title",
    **{"zh-CN":"卡片标题","zh-TW":"卡片標題","ja":"カードタイトル","ko":"카드 제목","hi":"कार्ड शीर्षक",
       "id":"Judul kartu","vi":"Tiêu đề thẻ","th":"หัวข้อการ์ด","ar":"عنوان البطاقة",
       "es":"Título de la tarjeta","fr":"Titre de la carte","de":"Karten-Titel","pt-BR":"Título do card","ru":"Заголовок карточки","tr":"Kart başlığı","it":"Titolo card"})

STRINGS["dogfood_card_body"] = k(
    "This card uses the literal token values from the synthesize() call: canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Spacing scale 4-8-12-20-32-52-84.",
    **{
        "zh-CN":"这张卡片使用 synthesize() 调用产出的字面 token 值:canvas #424448、ink #c0c2c6、body #9a9ca0、primary #987d86。圆角 7px。间距 4-8-12-20-32-52-84。",
        "zh-TW":"這張卡片使用 synthesize() 呼叫產出的字面 token 值:canvas #424448、ink #c0c2c6、body #9a9ca0、primary #987d86。圓角 7px。間距 4-8-12-20-32-52-84。",
        "ja":"このカードは synthesize() 呼び出しから出た文字どおりのトークン値を使う: canvas #424448、ink #c0c2c6、body #9a9ca0、primary #987d86。半径 7px。スペーシング 4-8-12-20-32-52-84。",
        "ko":"이 카드는 synthesize() 호출에서 나온 그대로의 토큰 값을 사용한다: canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. 반경 7px. 스페이싱 4-8-12-20-32-52-84.",
        "hi":"यह कार्ड synthesize() call से मिले literal token values इस्तेमाल करता है: canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86। Radius 7px। Spacing 4-8-12-20-32-52-84।",
        "id":"Kartu ini memakai nilai token literal dari panggilan synthesize(): canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Skala spacing 4-8-12-20-32-52-84.",
        "vi":"Thẻ này dùng giá trị token nguyên văn từ lời gọi synthesize(): canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Spacing 4-8-12-20-32-52-84.",
        "th":"การ์ดนี้ใช้ค่าโทเค็นตามตัวอักษรจากการเรียก synthesize(): canvas #424448 · ink #c0c2c6 · body #9a9ca0 · primary #987d86 · radius 7px · spacing 4-8-12-20-32-52-84",
        "ar":"تستعمل هذه البطاقة قيم الرموز الحرفيّة الصادرة عن استدعاء synthesize(): canvas #424448، ink #c0c2c6، body #9a9ca0، primary #987d86. نصف القطر 7px. سلّم التباعد 4-8-12-20-32-52-84.",
        "es":"Esta tarjeta usa los valores de token literales de la llamada a synthesize(): canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Escala de spacing 4-8-12-20-32-52-84.",
        "fr":"Cette carte utilise les valeurs de tokens littérales issues de l&rsquo;appel à synthesize() : canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Échelle de spacing 4-8-12-20-32-52-84.",
        "de":"Diese Karte nutzt die wörtlichen Token-Werte aus dem synthesize()-Aufruf: canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Spacing-Skala 4-8-12-20-32-52-84.",
        "pt-BR":"Este card usa os valores literais de token da chamada synthesize(): canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Escala de spacing 4-8-12-20-32-52-84.",
        "ru":"Эта карточка использует буквальные значения токенов из вызова synthesize(): canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Шкала spacing 4-8-12-20-32-52-84.",
        "tr":"Bu kart synthesize() çağrısından çıkan token değerlerini birebir kullanır: canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Spacing ölçeği 4-8-12-20-32-52-84.",
        "it":"Questa card usa i valori token letterali dalla chiamata a synthesize(): canvas #424448, ink #c0c2c6, body #9a9ca0, primary #987d86. Radius 7px. Scala spacing 4-8-12-20-32-52-84.",
    }
)

STRINGS["dogfood_card_btn"] = k("View token output",
    **{"zh-CN":"查看 token 输出","zh-TW":"檢視 token 輸出","ja":"トークン出力を見る","ko":"토큰 출력 보기","hi":"token output देखें",
       "id":"Lihat output token","vi":"Xem output token","th":"ดู output ของโทเค็น","ar":"عرض رموز المخرج",
       "es":"Ver salida de tokens","fr":"Voir la sortie des tokens","de":"Token-Ausgabe ansehen","pt-BR":"Ver saída de tokens","ru":"Посмотреть вывод токенов","tr":"Token çıktısını gör","it":"Vedi output dei token"})

STRINGS["dogfood_caption"] = k(
    "<strong>These are the actual tokens that powered this page.</strong> The brain ships its own marketing. The brief and output are in the HTML source as a comment at the top of the file.",
    **{
        "zh-CN":"<strong>这些就是驱动这一页的实际 tokens。</strong>大脑自己出自己的市场材料。brief 和 output 都在 HTML 源码顶端的注释里。",
        "zh-TW":"<strong>這些就是驅動這一頁的實際 tokens。</strong>大腦自己出自己的市場材料。brief 和 output 都在 HTML 原始碼頂端的註解裡。",
        "ja":"<strong>これがこのページを駆動している実際のトークン。</strong>頭脳は自分のマーケティングを出荷する。ブリーフと出力はファイル先頭のコメントとして HTML ソースにある。",
        "ko":"<strong>이게 이 페이지를 실제로 구동하는 토큰이다.</strong> 두뇌가 자기 마케팅을 출시한다. 브리프와 결과는 파일 상단의 주석으로 HTML 소스에 들어 있다.",
        "hi":"<strong>यही असली tokens हैं जो इस page को चला रहे हैं।</strong> दिमाग अपनी marketing खुद ship करता है। brief और output दोनों HTML source के top पर comment के रूप में हैं।",
        "id":"<strong>Ini adalah token sungguhan yang menggerakkan halaman ini.</strong> Otaknya mengirim marketing-nya sendiri. Brief dan output ada di komentar di bagian atas file HTML.",
        "vi":"<strong>Đây là token thật sự đang vận hành trang này.</strong> Bộ não tự ship marketing. Brief và output nằm trong comment ở đầu file HTML.",
        "th":"<strong>นี่คือโทเค็นจริงที่ขับเคลื่อนหน้านี้</strong> สมองส่งงานการตลาดของตัวเอง brief และ output อยู่ในคอมเมนต์บนสุดของไฟล์ HTML",
        "ar":"<strong>هذه هي الرموز الفعليّة التي تُحرِّك هذه الصفحة.</strong> العقل يُسلِّم تسويقه بنفسه. الملخّص والمخرج موجودان في مصدر HTML بوصفهما تعليقًا في أعلى الملفّ.",
        "es":"<strong>Estos son los tokens reales que impulsan esta página.</strong> El cerebro entrega su propio marketing. El brief y la salida están en el HTML como comentario al inicio del archivo.",
        "fr":"<strong>Ce sont les tokens réels qui font tourner cette page.</strong> Le cerveau livre son propre marketing. Le brief et la sortie figurent dans la source HTML en commentaire au début du fichier.",
        "de":"<strong>Das sind die tatsächlichen Tokens, die diese Seite antreiben.</strong> Das Gehirn liefert sein eigenes Marketing. Brief und Ausgabe stehen als Kommentar oben im HTML-Quelltext.",
        "pt-BR":"<strong>Estes são os tokens reais que movimentam esta página.</strong> O cérebro entrega o próprio marketing. O brief e a saída estão no HTML como comentário no topo do arquivo.",
        "ru":"<strong>Это реальные токены, питающие эту страницу.</strong> Мозг шипит собственный маркетинг. Бриф и вывод лежат в HTML-исходнике комментарием в начале файла.",
        "tr":"<strong>Bu sayfayı çalıştıran gerçek token'lar bunlar.</strong> Beyin kendi pazarlamasını gönderiyor. Brief ve çıktı, HTML kaynağında dosyanın en üstünde bir yorum olarak duruyor.",
        "it":"<strong>Questi sono i token reali che muovono questa pagina.</strong> Il cervello spedisce il proprio marketing. Il brief e l&rsquo;output sono nel sorgente HTML come commento in testa al file.",
    }
)

STRINGS["dogfood_type_body"] = k(
    "Inter for body. Both ship via Google Fonts. The display face here on this page is exactly what came out of the synthesizer.",
    **{
        "zh-CN":"正文用 Inter。两者都通过 Google Fonts 加载。这一页上的展示字体正是合成器输出的那一款。",
        "zh-TW":"內文用 Inter。兩者都透過 Google Fonts 載入。這一頁上的展示字體正是合成器輸出的那一款。",
        "ja":"本文は Inter。両方とも Google Fonts で配信。このページのディスプレイ書体は合成器が出したそのものだ。",
        "ko":"본문은 Inter. 둘 다 Google Fonts로 제공. 이 페이지의 디스플레이 서체는 신디사이저가 내놓은 그대로다.",
        "hi":"body के लिए Inter। दोनों Google Fonts से ship होते हैं। इस page पर display face वही है जो synthesizer से बाहर आया।",
        "id":"Inter untuk body. Keduanya dikirim via Google Fonts. Display face di halaman ini persis seperti yang keluar dari synthesizer.",
        "vi":"Inter cho body. Cả hai phát qua Google Fonts. Display face trên trang này đúng là cái synthesizer xuất ra.",
        "th":"Inter สำหรับ body · ทั้งคู่ส่งผ่าน Google Fonts · ฟอนต์ display บนหน้านี้คือสิ่งที่ synthesizer ส่งออกมาเป๊ะ",
        "ar":"خطّ Inter للنصّ. كلاهما يُحمَّل عبر Google Fonts. خطّ العرض في هذه الصفحة هو بعينه ما خرج من المولِّد.",
        "es":"Inter para body. Ambos vienen vía Google Fonts. La display face en esta página es exactamente la que salió del sintetizador.",
        "fr":"Inter pour le body. Les deux arrivent via Google Fonts. La display face de cette page est exactement celle qui est sortie du synthétiseur.",
        "de":"Inter für Body. Beide kommen über Google Fonts. Die Display-Face auf dieser Seite ist genau die, die der Synthesizer ausgegeben hat.",
        "pt-BR":"Inter para body. Ambas vêm via Google Fonts. A display face desta página é exatamente a que saiu do sintetizador.",
        "ru":"Inter для body. Обе шрифт-семьи поставляются через Google Fonts. Display-шрифт на этой странице &mdash; ровно то, что выдал синтезатор.",
        "tr":"Body için Inter. İkisi de Google Fonts üzerinden geliyor. Bu sayfadaki display face, sentezleyiciden tam olarak çıkan o.",
        "it":"Inter per il body. Entrambi arrivano via Google Fonts. La display face di questa pagina è esattamente quella uscita dal sintetizzatore.",
    }
)

STRINGS["dogfood_type_caption"] = k("JetBrains Mono &middot; for code &middot; ratio 1.333",
    **{"zh-CN":"JetBrains Mono &middot; 用于代码 &middot; 比率 1.333","zh-TW":"JetBrains Mono &middot; 用於程式碼 &middot; 比率 1.333",
       "ja":"JetBrains Mono &middot; コード用 &middot; 比率 1.333","ko":"JetBrains Mono &middot; 코드용 &middot; 비율 1.333",
       "hi":"JetBrains Mono &middot; code के लिए &middot; ratio 1.333","id":"JetBrains Mono &middot; untuk code &middot; rasio 1.333",
       "vi":"JetBrains Mono &middot; cho code &middot; tỷ lệ 1.333","th":"JetBrains Mono &middot; สำหรับโค้ด &middot; อัตราส่วน 1.333",
       "ar":"JetBrains Mono &middot; للكود &middot; نسبة 1.333","es":"JetBrains Mono &middot; para code &middot; ratio 1.333",
       "fr":"JetBrains Mono &middot; pour le code &middot; ratio 1.333","de":"JetBrains Mono &middot; für Code &middot; Ratio 1.333",
       "pt-BR":"JetBrains Mono &middot; para code &middot; ratio 1.333","ru":"JetBrains Mono &middot; для кода &middot; коэффициент 1.333",
       "tr":"JetBrains Mono &middot; kod için &middot; oran 1.333","it":"JetBrains Mono &middot; per il code &middot; ratio 1.333"})

# ============ 7. PILLARS ============
STRINGS["pillars_eyebrow"] = k("07 &mdash; Why this is the floor",
    **{"zh-CN":"07 &mdash; 为什么这就是底线","zh-TW":"07 &mdash; 為什麼這就是底線","ja":"07 &mdash; なぜこれが床となるか","ko":"07 &mdash; 왜 이것이 바닥이 되는가","hi":"07 &mdash; यह floor क्यों है",
       "id":"07 &mdash; Mengapa ini lantai dasarnya","vi":"07 &mdash; Vì sao đây là sàn","th":"07 &mdash; ทำไมนี่คือพื้นมาตรฐาน","ar":"07 &mdash; لماذا هذا هو الحدّ الأدنى",
       "es":"07 &mdash; Por qué esto es el piso","fr":"07 &mdash; Pourquoi c&rsquo;est le plancher","de":"07 &mdash; Warum das die Grundlinie ist",
       "pt-BR":"07 &mdash; Por que isso é o piso","ru":"07 &mdash; Почему это нижний предел","tr":"07 &mdash; Bu neden zemin","it":"07 &mdash; Perché questo è il pavimento"})

STRINGS["pillars_h2"] = k(
    "Three properties.<br>\n          <span class=\"accent-italic\">No competitor has all three.</span>",
    **{
        "zh-CN":"三个属性。<br>\n          <span class=\"accent-italic\">没有竞品同时拥有这三项。</span>",
        "zh-TW":"三個屬性。<br>\n          <span class=\"accent-italic\">沒有競品同時擁有這三項。</span>",
        "ja":"3 つの性質。<br>\n          <span class=\"accent-italic\">3 つすべてを満たす競合はない。</span>",
        "ko":"세 가지 속성.<br>\n          <span class=\"accent-italic\">셋 다 가진 경쟁자는 없다.</span>",
        "hi":"तीन गुण।<br>\n          <span class=\"accent-italic\">कोई competitor तीनों एक साथ नहीं रखता।</span>",
        "id":"Tiga properti.<br>\n          <span class=\"accent-italic\">Tidak ada pesaing yang punya ketiganya.</span>",
        "vi":"Ba thuộc tính.<br>\n          <span class=\"accent-italic\">Không đối thủ nào có đủ cả ba.</span>",
        "th":"สามคุณสมบัติ<br>\n          <span class=\"accent-italic\">ไม่มีคู่แข่งรายไหนมีครบทั้งสาม</span>",
        "ar":"ثلاث خصائص.<br>\n          <span class=\"accent-italic\">لا منافس يجمعها جميعًا.</span>",
        "es":"Tres propiedades.<br>\n          <span class=\"accent-italic\">Ningún competidor las tiene las tres.</span>",
        "fr":"Trois propriétés.<br>\n          <span class=\"accent-italic\">Aucun concurrent ne les a toutes les trois.</span>",
        "de":"Drei Eigenschaften.<br>\n          <span class=\"accent-italic\">Kein Konkurrent hat alle drei.</span>",
        "pt-BR":"Três propriedades.<br>\n          <span class=\"accent-italic\">Nenhum concorrente tem as três.</span>",
        "ru":"Три свойства.<br>\n          <span class=\"accent-italic\">Ни у одного конкурента нет всех трёх.</span>",
        "tr":"Üç özellik.<br>\n          <span class=\"accent-italic\">Üçüne birden sahip rakip yok.</span>",
        "it":"Tre proprietà.<br>\n          <span class=\"accent-italic\">Nessun competitor le ha tutte e tre.</span>",
    }
)

STRINGS["pillar1_title"] = k("Offline.",
    **{"zh-CN":"离线。","zh-TW":"離線。","ja":"オフライン。","ko":"오프라인.","hi":"ऑफ़लाइन।",
       "id":"Offline.","vi":"Ngoại tuyến.","th":"ออฟไลน์","ar":"بلا اتصال.",
       "es":"Offline.","fr":"Hors-ligne.","de":"Offline.","pt-BR":"Offline.","ru":"Offline.","tr":"Çevrimdışı.","it":"Offline."})

STRINGS["pillar1_body"] = k(
    "Runs on a plane. No API key. No vendor lock-in. The 1,243 entries, 145 rules, 160 brand specs, and the synthesizer all live inside the Python wheel. Air-gapped repos can ship it.",
    **{
        "zh-CN":"在飞机上能跑。无需 API key。无供应商锁定。1,243 条条目、145 条规则、160 个品牌规范和合成器都装在那个 Python wheel 里。隔离网络的 repo 都能 ship。",
        "zh-TW":"在飛機上能跑。無需 API key。無供應商鎖定。1,243 條條目、145 條規則、160 個品牌規範和合成器都裝在那個 Python wheel 裡。隔離網路的 repo 都能 ship。",
        "ja":"飛行機の中でも動く。API キー不要。ベンダーロックインなし。1,243 件のエントリ、145 のルール、160 のブランド仕様、合成器、すべてが Python wheel の中にある。エアギャップ環境のリポジトリでも出荷できる。",
        "ko":"비행기 안에서도 돌아간다. API 키 없음. 벤더 락인 없음. 1,243개 항목, 145개 규칙, 160개 브랜드 사양, 신디사이저 모두 Python wheel 안에 들어 있다. 에어갭 저장소도 출시 가능.",
        "hi":"plane पर चलता है। कोई API key नहीं। कोई vendor lock-in नहीं। 1,243 entries, 145 rules, 160 brand specs, और synthesizer सब Python wheel के अंदर हैं। Air-gapped repos भी इसे ship कर सकते हैं।",
        "id":"Berjalan di pesawat. Tanpa API key. Tanpa vendor lock-in. 1.182 entri, 145 aturan, 160 spec brand, dan synthesizer-nya semua tinggal di dalam Python wheel. Repo air-gapped pun bisa mengirimnya.",
        "vi":"Chạy được trên máy bay. Không API key. Không vendor lock-in. 1.182 mục, 145 quy tắc, 160 spec thương hiệu và bộ tổng hợp đều sống bên trong Python wheel. Repo air-gapped cũng ship được.",
        "th":"รันบนเครื่องบินได้ ไม่ต้องมี API key ไม่ผูกกับเวนเดอร์ · 1,243 entries, 145 rules, 160 brand specs และ synthesizer ทั้งหมดอยู่ใน Python wheel · repo แบบ air-gapped ก็ ship ได้",
        "ar":"يعمل على متن الطائرة. بلا مفتاح API. بلا ارتباط بمورِّد. الإدخالات الـ1,243، والقواعد الـ145، ومواصفات العلامات الـ160، والمولِّد، كلّها داخل حزمة Python wheel. حتى المستودعات المعزولة عن الشبكة تستطيع شحنه.",
        "es":"Corre en un avión. Sin API key. Sin vendor lock-in. Las 1.182 entradas, 145 reglas, 160 specs de marca y el sintetizador viven adentro del wheel de Python. Repos air-gapped pueden enviarlo.",
        "fr":"Tourne dans l&rsquo;avion. Pas de clé API. Pas de vendor lock-in. Les 1 182 entrées, 145 règles, 160 specs de marque et le synthétiseur vivent à l&rsquo;intérieur du wheel Python. Des repos air-gapped peuvent l&rsquo;expédier.",
        "de":"Läuft im Flugzeug. Kein API-Key. Kein Vendor Lock-in. Die 1.182 Einträge, 145 Regeln, 160 Brand-Specs und der Synthesizer leben alle im Python-Wheel. Air-Gapped-Repos können es ausliefern.",
        "pt-BR":"Roda no avião. Sem API key. Sem vendor lock-in. As 1.182 entradas, 145 regras, 160 specs de marca e o sintetizador vivem dentro do wheel Python. Repos air-gapped conseguem enviar.",
        "ru":"Работает в самолёте. Без API-ключа. Без vendor lock-in. 1 182 записи, 145 правил, 160 brand-спецификаций и синтезатор живут внутри Python-wheel. Даже air-gapped репозитории могут его шипить.",
        "tr":"Uçakta çalışır. API anahtarı yok. Vendor lock-in yok. 1.182 giriş, 145 kural, 160 marka spec ve sentezleyici Python wheel'in içinde yaşar. Air-gapped repolar bile gönderebilir.",
        "it":"Gira in aereo. Niente API key. Niente vendor lock-in. Le 1.182 voci, 145 regole, 160 spec brand e il sintetizzatore vivono tutti dentro la wheel Python. Anche repo air-gapped possono spedirlo.",
    }
)

STRINGS["pillar2_title"] = k("Deterministic.",
    **{"zh-CN":"确定性。","zh-TW":"確定性。","ja":"決定論的。","ko":"결정론적.","hi":"Deterministic।",
       "id":"Deterministik.","vi":"Xác định.","th":"Deterministic","ar":"حتميّ.",
       "es":"Determinístico.","fr":"Déterministe.","de":"Deterministisch.","pt-BR":"Determinístico.","ru":"Детерминированно.","tr":"Deterministik.","it":"Deterministico."})

STRINGS["pillar2_body"] = k(
    "Same brief always produces the same tokens. Every sort has an explicit tiebreaker. Reproducible across machines, file systems, Python versions. Diffing two synth runs is meaningful.",
    **{
        "zh-CN":"同样的 brief 永远产生同样的 tokens。每个排序都有显式的 tiebreaker。跨机器、跨文件系统、跨 Python 版本都可复现。对两次 synth 运行做 diff 是有意义的。",
        "zh-TW":"同樣的 brief 永遠產生同樣的 tokens。每個排序都有顯式的 tiebreaker。跨機器、跨檔案系統、跨 Python 版本都可重現。對兩次 synth 執行做 diff 是有意義的。",
        "ja":"同じブリーフは常に同じトークンを生む。すべてのソートに明示的なタイブレーカがある。マシン、ファイルシステム、Python バージョンを跨いで再現可能。2 回の synth 実行の差分は意味を持つ。",
        "ko":"같은 브리프는 항상 같은 토큰을 만든다. 모든 정렬에 명시적 타이브레이커가 있다. 머신, 파일 시스템, Python 버전을 가로질러 재현 가능. 두 synth 실행의 diff는 의미 있다.",
        "hi":"एक ही brief हमेशा एक ही tokens देता है। हर sort में explicit tiebreaker होता है। machines, file systems, Python versions के बीच reproducible है। दो synth runs का diff करना meaningful है।",
        "id":"Brief sama selalu menghasilkan token yang sama. Setiap sort punya tiebreaker eksplisit. Bisa direproduksi di berbagai mesin, file system, versi Python. Diff dua run synth jadi bermakna.",
        "vi":"Cùng brief luôn cho cùng token. Mỗi lần sort đều có tiebreaker rõ ràng. Tái lập được trên máy, file system, phiên bản Python khác nhau. Diff hai lần chạy synth có ý nghĩa.",
        "th":"brief เดียวกันให้โทเค็นเดียวกันเสมอ ทุก sort มี tiebreaker ชัดเจน ทำซ้ำได้ข้ามเครื่อง ระบบไฟล์ และเวอร์ชัน Python · diff สองรันของ synth จึงมีความหมาย",
        "ar":"الملخّص نفسه يعطي الرموز نفسها دائمًا. كلّ ترتيب لديه فاصلٌ صريح للتعادل. قابلٌ للنسخ عبر الأجهزة وأنظمة الملفّات وإصدارات Python. والمقارنة بين تشغيلَي synth ذات معنى.",
        "es":"Mismo brief siempre produce los mismos tokens. Cada sort tiene un tiebreaker explícito. Reproducible entre máquinas, file systems y versiones de Python. Diffear dos corridas de synth tiene sentido.",
        "fr":"Même brief, mêmes tokens, toujours. Chaque tri a un tiebreaker explicite. Reproductible entre machines, file systems et versions de Python. Diffé deux runs de synth a un sens.",
        "de":"Gleicher Brief liefert immer dieselben Tokens. Jede Sortierung hat einen expliziten Tiebreaker. Reproduzierbar über Maschinen, Dateisysteme und Python-Versionen hinweg. Zwei Synth-Läufe zu diffen ist bedeutungsvoll.",
        "pt-BR":"Mesmo brief sempre produz os mesmos tokens. Todo sort tem tiebreaker explícito. Reprodutível entre máquinas, file systems e versões de Python. Diff entre dois runs de synth tem sentido.",
        "ru":"Один и тот же бриф всегда даёт одни и те же токены. Каждая сортировка имеет явный tiebreaker. Воспроизводимо между машинами, файловыми системами и версиями Python. Diff между двумя прогонами synth осмыслен.",
        "tr":"Aynı brief her zaman aynı token'ları üretir. Her sıralamanın açık bir tiebreaker'ı vardır. Makineler, dosya sistemleri ve Python sürümleri arasında tekrarlanabilir. İki synth çalışmasının diff'i anlamlıdır.",
        "it":"Stesso brief produce sempre gli stessi token. Ogni sort ha un tiebreaker esplicito. Riproducibile tra macchine, file system e versioni Python. Fare diff di due run di synth ha senso.",
    }
)

STRINGS["pillar3_title"] = k("Self-learning.",
    **{"zh-CN":"自我学习。","zh-TW":"自我學習。","ja":"自己学習。","ko":"자기 학습.","hi":"स्वयं सीखने वाला।",
       "id":"Belajar sendiri.","vi":"Tự học.","th":"เรียนรู้ตัวเอง","ar":"تعلُّمٌ ذاتيّ.",
       "es":"Auto-aprendizaje.","fr":"Auto-apprenant.","de":"Selbstlernend.","pt-BR":"Auto-aprendizado.","ru":"Самообучение.","tr":"Kendi kendine öğrenir.","it":"Auto-apprendimento."})

STRINGS["pillar3_body"] = k(
    "Every call writes to <code>.ux/decisions.jsonl</code>. The recommender re-ranks future candidates from your past wins. No telemetry. Your install gets sharper for your work, not aggregate slop.",
    **{
        "zh-CN":"每次调用都写入 <code>.ux/decisions.jsonl</code>。推荐器根据你过去的胜出记录,重新排序未来的候选。无遥测。你的安装为你自己的工作变得更锋利,而不是为整体的 slop。",
        "zh-TW":"每次呼叫都寫入 <code>.ux/decisions.jsonl</code>。推薦器根據你過去的勝出紀錄,重新排序未來的候選。無遙測。你的安裝為你自己的工作變得更鋒利,而不是為整體的 slop。",
        "ja":"呼び出すたびに <code>.ux/decisions.jsonl</code> に書き込む。レコメンダーは、あなたの過去の勝利から未来の候補を再ランク付けする。テレメトリなし。インストールはあなたの仕事のために鋭くなり、集約された slop には鋭くならない。",
        "ko":"모든 호출이 <code>.ux/decisions.jsonl</code>에 기록된다. 추천기는 당신의 과거 승리로부터 미래 후보를 재순위한다. 텔레메트리 없음. 당신의 설치는 당신의 작업을 위해 날카로워지며, 집계된 slop을 위해서가 아니다.",
        "hi":"हर call <code>.ux/decisions.jsonl</code> में लिखता है। recommender आपकी पिछली जीत से future candidates को re-rank करता है। कोई टेलीमेट्री नहीं। आपका install आपके काम के लिए धारदार होता है, aggregate slop के लिए नहीं।",
        "id":"Setiap panggilan menulis ke <code>.ux/decisions.jsonl</code>. Recommender me-rank ulang kandidat masa depan dari kemenangan-mu sebelumnya. Tanpa telemetri. Install-mu menajam untuk pekerjaanmu, bukan untuk slop agregat.",
        "vi":"Mỗi lần gọi ghi vào <code>.ux/decisions.jsonl</code>. Recommender xếp hạng lại ứng viên tương lai từ những chiến thắng cũ của bạn. Không telemetry. Bản install của bạn sắc bén cho công việc của bạn, không phải cho slop tổng hợp.",
        "th":"ทุก call เขียนลง <code>.ux/decisions.jsonl</code> · recommender จัดอันดับ candidate ใหม่จากชัยชนะที่ผ่านมาของคุณ · ไม่มี telemetry · install ของคุณคมขึ้นเพื่องานของคุณ ไม่ใช่ slop รวม ๆ",
        "ar":"كلّ استدعاء يُكتب في <code>.ux/decisions.jsonl</code>. يعيد المُوصِّي ترتيب المرشَّحين المستقبليّين بناءً على نجاحاتك السابقة. بلا تتبّع. تثبيتك يصبح أكثر حِدّةً لعملك أنت، لا لـ slop عام.",
        "es":"Cada llamada escribe en <code>.ux/decisions.jsonl</code>. El recomendador rerankea futuros candidatos a partir de tus victorias pasadas. Sin telemetría. Tu instalación se afila para tu trabajo, no para slop agregado.",
        "fr":"Chaque appel écrit dans <code>.ux/decisions.jsonl</code>. Le recommandeur reclasse les futurs candidats à partir de vos victoires passées. Pas de télémétrie. Votre install s&rsquo;affine pour votre travail, pas pour du slop agrégé.",
        "de":"Jeder Aufruf schreibt nach <code>.ux/decisions.jsonl</code>. Der Recommender ranked künftige Kandidaten aus deinen vergangenen Erfolgen neu. Keine Telemetrie. Deine Installation wird schärfer für deine Arbeit, nicht für aggregierten Slop.",
        "pt-BR":"Cada chamada grava em <code>.ux/decisions.jsonl</code>. O recomendador re-ranqueia futuros candidatos a partir das suas vitórias passadas. Sem telemetria. Sua instalação fica mais afiada para o seu trabalho, não para slop agregado.",
        "ru":"Каждый вызов пишет в <code>.ux/decisions.jsonl</code>. Рекомендатель пере-ранжирует будущих кандидатов из ваших прошлых побед. Без телеметрии. Ваша установка становится острее под вашу работу, а не под агрегированный slop.",
        "tr":"Her çağrı <code>.ux/decisions.jsonl</code> dosyasına yazar. Önerici gelecek adayları geçmiş kazanımlarından yeniden sıralar. Telemetri yok. Kurulumun kendi işin için keskinleşir, toplam slop için değil.",
        "it":"Ogni chiamata scrive su <code>.ux/decisions.jsonl</code>. Il recommender ri-classifica i candidati futuri dalle tue vittorie passate. Niente telemetria. La tua install diventa più affilata per il tuo lavoro, non per slop aggregato.",
    }
)

# ============ 8. AUDIENCE ============
STRINGS["audience_eyebrow"] = k("08 &mdash; For vibe coders",
    **{"zh-CN":"08 &mdash; 给 vibe coders","zh-TW":"08 &mdash; 給 vibe coders","ja":"08 &mdash; vibe コーダーへ","ko":"08 &mdash; 바이브 코더에게","hi":"08 &mdash; vibe coders के लिए",
       "id":"08 &mdash; Untuk vibe coder","vi":"08 &mdash; Cho vibe coder","th":"08 &mdash; สำหรับ vibe coder","ar":"08 &mdash; لمبرمجي الحدس",
       "es":"08 &mdash; Para vibe coders","fr":"08 &mdash; Pour les vibe codeurs","de":"08 &mdash; Für Vibe Coder",
       "pt-BR":"08 &mdash; Para vibe coders","ru":"08 &mdash; Для vibe-кодеров","tr":"08 &mdash; Vibe coder'lar için","it":"08 &mdash; Per i vibe coder"})

STRINGS["audience_h2"] = k(
    "If you ship by feel,<br>\n            <span class=\"accent-italic\">the brain is your floor.</span>",
    **{
        "zh-CN":"如果你凭感觉出货,<br>\n            <span class=\"accent-italic\">大脑就是你的底线。</span>",
        "zh-TW":"如果你憑感覺出貨,<br>\n            <span class=\"accent-italic\">大腦就是你的底線。</span>",
        "ja":"感覚で出荷するなら、<br>\n            <span class=\"accent-italic\">頭脳が あなたの床になる。</span>",
        "ko":"감으로 출시한다면,<br>\n            <span class=\"accent-italic\">두뇌가 당신의 바닥이다.</span>",
        "hi":"अगर आप feel से ship करते हैं,<br>\n            <span class=\"accent-italic\">तो दिमाग आपका floor है।</span>",
        "id":"Kalau kamu kirim by feel,<br>\n            <span class=\"accent-italic\">otaknya jadi lantai dasarmu.</span>",
        "vi":"Nếu bạn ship theo cảm tính,<br>\n            <span class=\"accent-italic\">bộ não là sàn của bạn.</span>",
        "th":"ถ้าคุณส่งงานด้วยความรู้สึก<br>\n            <span class=\"accent-italic\">สมองคือพื้นมาตรฐานของคุณ</span>",
        "ar":"إن كنت تُسلّم بالحدس،<br>\n            <span class=\"accent-italic\">فالعقل هو حدّك الأدنى.</span>",
        "es":"Si envías por feeling,<br>\n            <span class=\"accent-italic\">el cerebro es tu piso.</span>",
        "fr":"Si vous livrez au feeling,<br>\n            <span class=\"accent-italic\">le cerveau est votre plancher.</span>",
        "de":"Wenn du nach Gefühl auslieferst,<br>\n            <span class=\"accent-italic\">ist das Gehirn dein Boden.</span>",
        "pt-BR":"Se você envia no feeling,<br>\n            <span class=\"accent-italic\">o cérebro é o seu piso.</span>",
        "ru":"Если вы шипите по ощущениям,<br>\n            <span class=\"accent-italic\">мозг &mdash; ваш пол.</span>",
        "tr":"Eğer hisle gönderiyorsan,<br>\n            <span class=\"accent-italic\">beyin senin zeminindir.</span>",
        "it":"Se spedisci a sensazione,<br>\n            <span class=\"accent-italic\">il cervello è il tuo pavimento.</span>",
    }
)

STRINGS["audience_lead"] = k(
    "You prompt an assistant. It returns code. The CSS is generic. The hierarchy is flat. The palette is the default Tailwind ten. You ship anyway, because the alternative is hand-tuning a thousand tokens.",
    **{
        "zh-CN":"你给助手发 prompt。它返回代码。CSS 是通用的。层级是扁平的。调色板是 Tailwind 默认的那十色。你还是 ship 了,因为另一个选项是手动调一千个 tokens。",
        "zh-TW":"你給助手發 prompt。它回傳程式碼。CSS 是通用的。層級是扁平的。調色盤是 Tailwind 預設的那十色。你還是 ship 了,因為另一個選項是手動調一千個 tokens。",
        "ja":"アシスタントにプロンプトを送る。コードが返ってくる。CSS は汎用。階層はフラット。パレットは Tailwind のデフォルト 10 色。それでも出荷する。代わりは 1,000 個のトークンを手動で調整することだから。",
        "ko":"어시스턴트에게 프롬프트한다. 코드를 돌려준다. CSS는 일반적이다. 위계는 평평하다. 팔레트는 Tailwind 기본 10색이다. 그래도 출시한다. 대안은 천 개의 토큰을 손으로 튜닝하는 것이기 때문이다.",
        "hi":"आप एक assistant को prompt देते हैं। वो code लौटाता है। CSS generic है। hierarchy flat है। palette default Tailwind का दस-रंगी है। फिर भी आप ship कर देते हैं, क्योंकि alternative एक हज़ार tokens hand-tune करना है।",
        "id":"Kamu prompt asisten. Dia mengembalikan code. CSS-nya generik. Hierarki-nya datar. Palette-nya Tailwind default sepuluh warna. Kamu kirim juga, karena alternatifnya adalah menyetel seribu token dengan tangan.",
        "vi":"Bạn prompt một trợ lý. Nó trả về code. CSS generic. Hierarchy phẳng. Palette là mười màu mặc định của Tailwind. Bạn vẫn ship, vì lựa chọn còn lại là tinh chỉnh tay một nghìn token.",
        "th":"คุณ prompt ผู้ช่วย มันคืนโค้ดมา CSS generic ลำดับชั้นแบน palette คือสิบสีดีฟอลต์ของ Tailwind คุณส่งอยู่ดี เพราะทางเลือกอีกทางคือนั่งจูนพันโทเค็นด้วยมือ",
        "ar":"تطلب من مساعد. يعيد لك كودًا. CSS معتاد. التسلسل مسطَّح. اللوحة هي عشر ألوان Tailwind الافتراضيّة. تُسلِّم رغم ذلك، لأنّ البديل أن تضبط ألف رمز يدويًّا.",
        "es":"Promptea a un asistente. Devuelve código. El CSS es genérico. La jerarquía es plana. La paleta es las diez por defecto de Tailwind. Envías igual, porque la alternativa es tunear mil tokens a mano.",
        "fr":"Vous promptez un assistant. Il renvoie du code. Le CSS est générique. La hiérarchie est plate. La palette est le top 10 par défaut de Tailwind. Vous livrez quand même, parce que l&rsquo;alternative est de régler mille tokens à la main.",
        "de":"Du promptest einen Assistenten. Er liefert Code. Das CSS ist generisch. Die Hierarchie ist flach. Die Palette sind die zehn Tailwind-Defaults. Du lieferst trotzdem &mdash; die Alternative wäre, tausend Tokens händisch zu tunen.",
        "pt-BR":"Você prompta um assistente. Ele devolve código. O CSS é genérico. A hierarquia é plana. A paleta são as dez padrão do Tailwind. Você envia mesmo assim, porque a alternativa é tunar mil tokens à mão.",
        "ru":"Вы промптите ассистента. Он возвращает код. CSS общий. Иерархия плоская. Палитра &mdash; десять дефолтных Tailwind. Вы всё равно шипите, потому что альтернатива &mdash; вручную тюнить тысячу токенов.",
        "tr":"Bir asistana prompt verirsin. Kod döndürür. CSS sıradan. Hiyerarşi düz. Palet, Tailwind'in varsayılan onu. Yine de gönderirsin, çünkü alternatif bin token'ı elle ayarlamak.",
        "it":"Promptі un assistente. Restituisce code. Il CSS è generico. La gerarchia è piatta. La palette è le dieci di default di Tailwind. Spedisci comunque, perché l&rsquo;alternativa è tunare mille token a mano.",
    }
)

STRINGS["audience_body"] = k(
    "uxskill sits between you and the assistant. The brief becomes a synthesized design language before code is written. The linter catches the slop before commit. The ledger remembers what worked. You stay vibe; the floor stays high.",
    **{
        "zh-CN":"uxskill 介于你和助手之间。在写代码之前,brief 就变成一套合成的设计语言。linter 在 commit 前抓住 slop。ledger 记得什么有效。你保持 vibe,底线保持高。",
        "zh-TW":"uxskill 介於你和助手之間。在寫程式之前,brief 就變成一套合成的設計語言。linter 在 commit 前抓住 slop。ledger 記得什麼有效。你保持 vibe,底線保持高。",
        "ja":"uxskill はあなたとアシスタントのあいだに座る。コードが書かれる前に、ブリーフは合成されたデザイン言語になる。リンターはコミット前に slop を捕まえる。台帳は何が効いたかを覚える。あなたは vibe のまま、床は高いまま。",
        "ko":"uxskill은 당신과 어시스턴트 사이에 자리한다. 코드가 작성되기 전에 브리프가 합성된 디자인 언어가 된다. 린터가 커밋 전에 slop을 잡는다. 원장은 무엇이 효과 있었는지 기억한다. 당신은 바이브를 유지하고, 바닥은 높게 유지된다.",
        "hi":"uxskill आप और assistant के बीच बैठता है। code लिखे जाने से पहले brief एक synthesized डिज़ाइन भाषा बन जाता है। linter commit से पहले slop पकड़ता है। ledger याद रखता है क्या काम किया। आप vibe में रहते हैं; floor ऊँचा रहता है।",
        "id":"uxskill duduk di antara kamu dan asisten. Brief jadi bahasa desain tersintesis sebelum code ditulis. Linter menangkap slop sebelum commit. Ledger mengingat yang berhasil. Kamu tetap vibe; lantai tetap tinggi.",
        "vi":"uxskill nằm giữa bạn và trợ lý. Brief trở thành ngôn ngữ thiết kế tổng hợp trước khi code được viết. Linter bắt slop trước khi commit. Ledger nhớ cái nào hiệu quả. Bạn vẫn vibe; sàn vẫn cao.",
        "th":"uxskill อยู่ระหว่างคุณกับผู้ช่วย · brief กลายเป็นภาษาดีไซน์ที่สังเคราะห์ก่อนเขียนโค้ด · linter จับ slop ก่อน commit · ledger จำว่าอะไรเวิร์ก · คุณยัง vibe พื้นยังสูง",
        "ar":"يجلس uxskill بينك وبين المساعد. الملخّص يتحوّل إلى لغة تصميم مولَّدة قبل كتابة الكود. الـlinter يلتقط الـslop قبل التثبيت. الـledger يتذكَّر ما نَجح. تبقى أنت في وضع الحدس، ويبقى الحدّ الأدنى عاليًا.",
        "es":"uxskill se sienta entre vos y el asistente. El brief se vuelve un lenguaje de diseño sintetizado antes de que se escriba código. El linter atrapa el slop antes del commit. El ledger recuerda qué funcionó. Vos seguís en vibe; el piso queda alto.",
        "fr":"uxskill s&rsquo;assoit entre vous et l&rsquo;assistant. Le brief devient un langage de design synthétisé avant que le code ne soit écrit. Le linter attrape le slop avant commit. Le ledger se souvient de ce qui a marché. Vous restez en vibe ; le plancher reste haut.",
        "de":"uxskill sitzt zwischen dir und dem Assistenten. Der Brief wird zur synthetisierten Designsprache, bevor Code geschrieben wird. Der Linter erwischt Slop vor dem Commit. Das Ledger merkt sich, was funktioniert hat. Du bleibst Vibe; der Boden bleibt hoch.",
        "pt-BR":"O uxskill senta entre você e o assistente. O brief vira linguagem de design sintetizada antes de qualquer code ser escrito. O linter pega o slop antes do commit. O ledger lembra o que deu certo. Você fica no vibe; o piso fica alto.",
        "ru":"uxskill сидит между вами и ассистентом. Бриф становится синтезированным дизайн-языком до того, как написан код. Линтер ловит slop до коммита. Журнал помнит, что сработало. Вы остаётесь в vibe; пол остаётся высоким.",
        "tr":"uxskill seninle asistan arasında oturur. Brief, kod yazılmadan önce sentezlenmiş bir tasarım dili olur. Linter, commit'ten önce slop'u yakalar. Ledger neyin işe yaradığını hatırlar. Sen vibe'da kalırsın; zemin yüksekte kalır.",
        "it":"uxskill sta tra te e l&rsquo;assistente. Il brief diventa un linguaggio di design sintetizzato prima che venga scritto il code. Il linter prende lo slop prima del commit. Il ledger ricorda cosa ha funzionato. Tu resti in vibe; il pavimento resta alto.",
    }
)

# ============ 9. PROOF ============
STRINGS["proof_eyebrow"] = k("09 &mdash; The catalogue",
    **{"zh-CN":"09 &mdash; 目录","zh-TW":"09 &mdash; 目錄","ja":"09 &mdash; カタログ","ko":"09 &mdash; 카탈로그","hi":"09 &mdash; catalogue",
       "id":"09 &mdash; Katalog","vi":"09 &mdash; Catalog","th":"09 &mdash; แคตตาล็อก","ar":"09 &mdash; الكتالوج",
       "es":"09 &mdash; El catálogo","fr":"09 &mdash; Le catalogue","de":"09 &mdash; Der Katalog",
       "pt-BR":"09 &mdash; O catálogo","ru":"09 &mdash; Каталог","tr":"09 &mdash; Katalog","it":"09 &mdash; Il catalogo"})

STRINGS["proof_h2"] = k(
    "1,243 entries.<br>\n          <span class=\"accent-italic\">Browse the corpus.</span>",
    **{
        "zh-CN":"1,243 条条目。<br>\n          <span class=\"accent-italic\">浏览语料库。</span>",
        "zh-TW":"1,243 條條目。<br>\n          <span class=\"accent-italic\">瀏覽語料庫。</span>",
        "ja":"1,243 件のエントリ。<br>\n          <span class=\"accent-italic\">コーパスを見る。</span>",
        "ko":"1,243개의 항목.<br>\n          <span class=\"accent-italic\">코퍼스 둘러보기.</span>",
        "hi":"1,243 entries।<br>\n          <span class=\"accent-italic\">corpus देखें।</span>",
        "id":"1.182 entri.<br>\n          <span class=\"accent-italic\">Jelajahi korpus.</span>",
        "vi":"1.182 mục.<br>\n          <span class=\"accent-italic\">Duyệt corpus.</span>",
        "th":"1,243 รายการ<br>\n          <span class=\"accent-italic\">เลื่อนดู corpus</span>",
        "ar":"1,243 إدخالًا.<br>\n          <span class=\"accent-italic\">تصفَّح المتن.</span>",
        "es":"1.182 entradas.<br>\n          <span class=\"accent-italic\">Navega el corpus.</span>",
        "fr":"1 182 entrées.<br>\n          <span class=\"accent-italic\">Parcourir le corpus.</span>",
        "de":"1.182 Einträge.<br>\n          <span class=\"accent-italic\">Stöbere im Korpus.</span>",
        "pt-BR":"1.182 entradas.<br>\n          <span class=\"accent-italic\">Navegue pelo corpus.</span>",
        "ru":"1 182 записи.<br>\n          <span class=\"accent-italic\">Пройдитесь по корпусу.</span>",
        "tr":"1.182 giriş.<br>\n          <span class=\"accent-italic\">Derlemde gez.</span>",
        "it":"1.182 voci.<br>\n          <span class=\"accent-italic\">Naviga il corpus.</span>",
    }
)

STRINGS["proof_brands_body"] = k(
    "Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Full palettes, typography, voice. JSON for queries, prose for context.",
    **{
        "zh-CN":"Apple、Stripe、Linear、Vercel、Ferrari、Anthropic。完整调色板、字体、品牌嗓音。JSON 供查询,散文供上下文。",
        "zh-TW":"Apple、Stripe、Linear、Vercel、Ferrari、Anthropic。完整調色盤、字體、品牌嗓音。JSON 供查詢,散文供上下文。",
        "ja":"Apple、Stripe、Linear、Vercel、Ferrari、Anthropic。完全なパレット、タイポグラフィ、ボイス。クエリ用に JSON、文脈用に散文。",
        "ko":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. 전체 팔레트, 타이포그래피, 보이스. 쿼리용 JSON, 컨텍스트용 산문.",
        "hi":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic। पूरी palettes, typography, voice। queries के लिए JSON, context के लिए prose।",
        "id":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Palette, tipografi, dan voice lengkap. JSON untuk query, prosa untuk konteks.",
        "vi":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Đủ palette, typography, voice. JSON cho query, prose cho ngữ cảnh.",
        "th":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic · palette, typography และ voice ครบ · JSON สำหรับ query, prose สำหรับ context",
        "ar":"Apple وStripe وLinear وVercel وFerrari وAnthropic. لوحات ألوان كاملة، وطباعة، وصوت العلامة. JSON للاستعلامات، ونثر للسياق.",
        "es":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Paletas, tipografía y voz completas. JSON para queries, prosa para contexto.",
        "fr":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Palettes, typographies et voix complètes. JSON pour les requêtes, prose pour le contexte.",
        "de":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Vollständige Paletten, Typografie, Voice. JSON für Queries, Prosa für Kontext.",
        "pt-BR":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Paletas, tipografia e voz completas. JSON para queries, prosa para contexto.",
        "ru":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Полные палитры, типографика, voice. JSON для запросов, проза для контекста.",
        "tr":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Tam paletler, tipografi, voice. Sorgular için JSON, bağlam için düzyazı.",
        "it":"Apple, Stripe, Linear, Vercel, Ferrari, Anthropic. Palette, tipografia e voice complete. JSON per le query, prosa per il contesto.",
    }
)

STRINGS["proof_brands_link"] = k("Browse brands &middot;",
    **{"zh-CN":"浏览品牌 &middot;","zh-TW":"瀏覽品牌 &middot;","ja":"ブランドを見る &middot;","ko":"브랜드 보기 &middot;","hi":"brands देखें &middot;",
       "id":"Jelajahi brand &middot;","vi":"Duyệt brand &middot;","th":"ดูแบรนด์ &middot;","ar":"تصفَّح العلامات &middot;",
       "es":"Ver marcas &middot;","fr":"Parcourir les marques &middot;","de":"Marken durchstöbern &middot;",
       "pt-BR":"Ver marcas &middot;","ru":"Смотреть бренды &middot;","tr":"Markaları gör &middot;","it":"Sfoglia i brand &middot;"})

STRINGS["proof_rules_body"] = k(
    "Deterministic regex. Sub-50ms scan on 10K lines. Catches placeholder text, default Tailwind palettes, A11y skips, marketing buzzwords.",
    **{
        "zh-CN":"确定性正则。一万行扫描小于 50ms。抓占位文本、Tailwind 默认调色板、A11y 跳过、营销 buzzword。",
        "zh-TW":"確定性正則。一萬行掃描小於 50ms。抓佔位文字、Tailwind 預設調色盤、A11y 跳過、行銷 buzzword。",
        "ja":"決定論的な正規表現。1 万行を 50ms 未満でスキャン。プレースホルダ文字、Tailwind デフォルトパレット、A11y のスキップ、マーケティングのバズワードを検出。",
        "ko":"결정론적 정규표현식. 1만 줄을 50ms 미만으로 스캔. 플레이스홀더 텍스트, Tailwind 기본 팔레트, A11y 건너뜀, 마케팅 버즈워드를 잡는다.",
        "hi":"Deterministic regex। 10K lines पर 50ms से कम का scan। placeholder text, default Tailwind palettes, A11y skips, marketing buzzwords पकड़ता है।",
        "id":"Regex deterministik. Scan di bawah 50ms untuk 10K baris. Menangkap placeholder text, palette Tailwind default, A11y yang dilewat, buzzword marketing.",
        "vi":"Regex xác định. Quét dưới 50ms cho 10K dòng. Bắt placeholder text, palette Tailwind mặc định, A11y bị bỏ, buzzword marketing.",
        "th":"regex แบบ deterministic · สแกน 10K บรรทัดต่ำกว่า 50ms · จับ placeholder text, palette Tailwind ดีฟอลต์, A11y ที่ข้าม, buzzword การตลาด",
        "ar":"تعابير منتظمة حتميّة. مسح أقلّ من 50ms لـ10K أسطر. يلتقط نصوصًا مؤقّتة، ولوحات Tailwind الافتراضيّة، وتجاوزات A11y، ومصطلحات تسويقيّة فارغة.",
        "es":"Regex determinístico. Escaneo en menos de 50ms sobre 10K líneas. Atrapa placeholder text, paletas Tailwind por defecto, skips de A11y, buzzwords de marketing.",
        "fr":"Regex déterministe. Scan sous 50ms sur 10K lignes. Attrape les placeholder text, les palettes Tailwind par défaut, les skips A11y, les buzzwords marketing.",
        "de":"Deterministisches Regex. Scan unter 50ms auf 10K Zeilen. Erwischt Platzhalter-Text, Default-Tailwind-Paletten, A11y-Skips, Marketing-Buzzwords.",
        "pt-BR":"Regex determinístico. Scan abaixo de 50ms em 10K linhas. Pega placeholder text, paletas Tailwind padrão, A11y skips, buzzwords de marketing.",
        "ru":"Детерминированный regex. Сканирование менее 50ms на 10K строк. Ловит placeholder-текст, дефолтные Tailwind палитры, A11y skips, маркетинговые buzzwords.",
        "tr":"Deterministik regex. 10K satırda 50ms altı tarama. Placeholder text'i, varsayılan Tailwind paletlerini, A11y atlamalarını, pazarlama buzzword'lerini yakalar.",
        "it":"Regex deterministico. Scan sotto i 50ms su 10K righe. Becca placeholder text, palette Tailwind di default, A11y skip, buzzword di marketing.",
    }
)

STRINGS["proof_rules_link"] = k("Browse rules &middot;",
    **{"zh-CN":"浏览规则 &middot;","zh-TW":"瀏覽規則 &middot;","ja":"ルールを見る &middot;","ko":"규칙 보기 &middot;","hi":"rules देखें &middot;",
       "id":"Jelajahi aturan &middot;","vi":"Duyệt rules &middot;","th":"ดูกฎ &middot;","ar":"تصفَّح القواعد &middot;",
       "es":"Ver reglas &middot;","fr":"Parcourir les règles &middot;","de":"Regeln durchstöbern &middot;",
       "pt-BR":"Ver regras &middot;","ru":"Смотреть правила &middot;","tr":"Kuralları gör &middot;","it":"Sfoglia le regole &middot;"})

STRINGS["proof_launch_head"] = k("Read the launch post",
    **{"zh-CN":"读发布博文","zh-TW":"讀發布部落格文","ja":"ローンチ投稿を読む","ko":"런치 포스트 읽기","hi":"launch post पढ़ें",
       "id":"Baca post peluncuran","vi":"Đọc bài launch","th":"อ่านโพสต์เปิดตัว","ar":"اقرأ تدوينة الإطلاق",
       "es":"Leer el post de lanzamiento","fr":"Lire le post de lancement","de":"Launch-Post lesen","pt-BR":"Ler o post de lançamento","ru":"Читать пост запуска","tr":"Lansman yazısını oku","it":"Leggi il post di lancio"})

STRINGS["proof_launch_body"] = k(
    "The full architecture writeup. Why brand specs became training data. Why the synthesizer is deterministic. Why the ledger closes the loop.",
    **{
        "zh-CN":"完整的架构说明。为什么品牌规范变成了训练数据。为什么合成器是确定性的。为什么 ledger 把循环闭合。",
        "zh-TW":"完整的架構說明。為什麼品牌規範變成了訓練資料。為什麼合成器是確定性的。為什麼 ledger 把循環閉合。",
        "ja":"アーキテクチャの完全解説。なぜブランド仕様がトレーニングデータになったか。なぜ合成器が決定論的か。なぜ台帳がループを閉じるか。",
        "ko":"전체 아키텍처 글. 왜 브랜드 사양이 학습 데이터가 되었나. 왜 신디사이저가 결정론적인가. 왜 원장이 루프를 닫는가.",
        "hi":"पूरा architecture writeup। क्यों brand specs training data बने। क्यों synthesizer deterministic है। क्यों ledger loop को बंद करता है।",
        "id":"Writeup arsitektur lengkap. Kenapa spec brand jadi data latih. Kenapa synthesizer deterministik. Kenapa ledger menutup loop-nya.",
        "vi":"Bài viết kiến trúc đầy đủ. Vì sao spec thương hiệu trở thành dữ liệu huấn luyện. Vì sao bộ tổng hợp xác định. Vì sao ledger đóng vòng lặp.",
        "th":"คำอธิบายสถาปัตยกรรมแบบครบ · ทำไม brand specs จึงกลายเป็นข้อมูลฝึก · ทำไม synthesizer ถึง deterministic · ทำไม ledger ปิดวง",
        "ar":"شرح البنية المعماريّة كاملًا. لماذا تحوّلت مواصفات العلامات إلى بيانات تدريب. لماذا المولِّد حتميّ. لماذا يُغلِق الـledger الحلقة.",
        "es":"El writeup completo de arquitectura. Por qué las specs de marca pasaron a ser datos de entrenamiento. Por qué el sintetizador es determinístico. Por qué el ledger cierra el loop.",
        "fr":"Le writeup complet de l&rsquo;architecture. Pourquoi les specs de marque sont devenues des données d&rsquo;entraînement. Pourquoi le synthétiseur est déterministe. Pourquoi le ledger ferme la boucle.",
        "de":"Das komplette Architektur-Writeup. Warum Brand-Specs zu Trainingsdaten wurden. Warum der Synthesizer deterministisch ist. Warum das Ledger den Loop schließt.",
        "pt-BR":"O writeup completo da arquitetura. Por que specs de marca viraram dados de treino. Por que o sintetizador é determinístico. Por que o ledger fecha o loop.",
        "ru":"Полный разбор архитектуры. Почему brand-спецификации стали обучающими данными. Почему синтезатор детерминирован. Почему ledger замыкает цикл.",
        "tr":"Tam mimari yazısı. Marka spec'lerinin neden eğitim verisi olduğu. Sentezleyicinin neden deterministik olduğu. Ledger'ın döngüyü neden kapattığı.",
        "it":"Il writeup completo dell&rsquo;architettura. Perché le spec brand sono diventate dati di addestramento. Perché il sintetizzatore è deterministico. Perché il ledger chiude il loop.",
    }
)

STRINGS["proof_launch_link"] = k("Read the launch &middot;",
    **{"zh-CN":"阅读发布 &middot;","zh-TW":"閱讀發布 &middot;","ja":"ローンチを読む &middot;","ko":"런치 읽기 &middot;","hi":"launch पढ़ें &middot;",
       "id":"Baca peluncuran &middot;","vi":"Đọc launch &middot;","th":"อ่านการเปิดตัว &middot;","ar":"اقرأ الإطلاق &middot;",
       "es":"Leer el lanzamiento &middot;","fr":"Lire le lancement &middot;","de":"Launch lesen &middot;",
       "pt-BR":"Ler o lançamento &middot;","ru":"Читать о запуске &middot;","tr":"Lansmanı oku &middot;","it":"Leggi il lancio &middot;"})

# Proof card heads (already have hero_stat_brand_specs and hero_stat_rules — those will catch
# "Brand DESIGN.md specs" and "Anti-pattern rules" here too via the global replace. Good.)

# ============ 10. FINAL CTA ============
STRINGS["final_h2"] = k("Install in 60 seconds.",
    **{"zh-CN":"60 秒内安装。","zh-TW":"60 秒內安裝。","ja":"60 秒でインストール。","ko":"60초 만에 설치.","hi":"60 सेकंड में install करें।",
       "id":"Instal dalam 60 detik.","vi":"Cài đặt trong 60 giây.","th":"ติดตั้งใน 60 วินาที","ar":"التثبيت في 60 ثانية.",
       "es":"Instalá en 60 segundos.","fr":"Installez en 60 secondes.","de":"In 60 Sekunden installiert.",
       "pt-BR":"Instale em 60 segundos.","ru":"Установка за 60 секунд.","tr":"60 saniyede kur.","it":"Installa in 60 secondi."})

STRINGS["final_lead"] = k(
    "Pick the runtime that fits where you live. The Python wheel is the engine; the npm wrapper invokes it from Node hosts; the Claude marketplace installs the slash commands and sub-agents directly.",
    **{
        "zh-CN":"挑一个适合你常住环境的 runtime。Python wheel 是引擎;npm wrapper 从 Node 宿主调用它;Claude marketplace 直接安装 slash commands 和 sub-agents。",
        "zh-TW":"挑一個適合你常住環境的 runtime。Python wheel 是引擎;npm wrapper 從 Node 宿主呼叫它;Claude marketplace 直接安裝 slash commands 和 sub-agents。",
        "ja":"住んでいる環境に合うランタイムを選ぼう。Python wheel がエンジン。npm ラッパーは Node ホストから呼び出す。Claude marketplace はスラッシュコマンドとサブエージェントを直接インストールする。",
        "ko":"당신이 사는 환경에 맞는 런타임을 골라라. Python wheel이 엔진이고, npm 래퍼는 Node 호스트에서 그것을 호출하며, Claude 마켓플레이스는 슬래시 명령어와 서브에이전트를 바로 설치한다.",
        "hi":"वो runtime चुनें जो आपके maहौल पर fit बैठे। Python wheel engine है; npm wrapper Node hosts से उसे invoke करता है; Claude marketplace slash commands और sub-agents directly install करता है।",
        "id":"Pilih runtime yang cocok dengan tempatmu kerja. Python wheel adalah engine-nya; npm wrapper memanggilnya dari host Node; Claude marketplace memasang slash command dan sub-agent langsung.",
        "vi":"Chọn runtime hợp với chỗ bạn sống. Python wheel là engine; npm wrapper gọi nó từ host Node; Claude marketplace cài slash command và sub-agent trực tiếp.",
        "th":"เลือก runtime ที่เข้ากับที่ที่คุณอยู่ · Python wheel คือ engine · npm wrapper เรียกมันจาก host แบบ Node · Claude marketplace ติดตั้ง slash command และ sub-agent ตรง ๆ",
        "ar":"اختر بيئة التشغيل التي تناسب مكان عيشك. حزمة Python wheel هي المحرّك؛ غلاف npm يستدعيها من مضيفي Node؛ سوق Claude يثبِّت الأوامر القاطعة والوكلاء الفرعيّين مباشرة.",
        "es":"Elegí el runtime que va con donde vivís. El wheel Python es el motor; el wrapper npm lo invoca desde hosts Node; el marketplace de Claude instala los slash commands y sub-agents directo.",
        "fr":"Choisissez le runtime qui correspond à votre environnement. Le wheel Python est le moteur ; le wrapper npm l&rsquo;invoque depuis des hôtes Node ; la marketplace Claude installe directement les slash commands et sub-agents.",
        "de":"Wähle die Runtime, die zu deiner Umgebung passt. Das Python-Wheel ist der Motor; der npm-Wrapper ruft es aus Node-Hosts auf; der Claude-Marketplace installiert Slash-Commands und Sub-Agents direkt.",
        "pt-BR":"Escolha o runtime que combina com onde você vive. O wheel Python é o motor; o wrapper npm invoca a partir de hosts Node; o marketplace do Claude instala slash commands e sub-agents direto.",
        "ru":"Выберите runtime, который подходит вашей среде. Python-wheel &mdash; это движок; npm-обёртка вызывает его из Node-хостов; маркетплейс Claude напрямую ставит slash-команды и саб-агентов.",
        "tr":"Yaşadığın yere uygun runtime'ı seç. Python wheel motordur; npm wrapper onu Node host'lardan çağırır; Claude marketplace slash komutlarını ve sub-agent'ları doğrudan kurar.",
        "it":"Scegli il runtime adatto a dove vivi. Il wheel Python è il motore; il wrapper npm lo invoca da host Node; il marketplace di Claude installa slash command e sub-agent direttamente.",
    }
)

STRINGS["final_copy"] = k("Copy",
    **{"zh-CN":"复制","zh-TW":"複製","ja":"コピー","ko":"복사","hi":"कॉपी",
       "id":"Salin","vi":"Sao chép","th":"คัดลอก","ar":"نسخ",
       "es":"Copiar","fr":"Copier","de":"Kopieren","pt-BR":"Copiar","ru":"Копировать","tr":"Kopyala","it":"Copia"})

STRINGS["final_sub"] = k(
    "Open source &middot; MIT &middot; No telemetry &middot; No LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star on GitHub</a>",
    **{
        "zh-CN":"开源 &middot; MIT &middot; 无遥测 &middot; 无 LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">在 GitHub 加星</a>",
        "zh-TW":"開源 &middot; MIT &middot; 無遙測 &middot; 無 LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">在 GitHub 加星</a>",
        "ja":"オープンソース &middot; MIT &middot; テレメトリなし &middot; LLM なし &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">GitHub でスター</a>",
        "ko":"오픈 소스 &middot; MIT &middot; 텔레메트리 없음 &middot; LLM 없음 &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">GitHub 스타</a>",
        "hi":"Open source &middot; MIT &middot; कोई टेलीमेट्री नहीं &middot; कोई LLM नहीं &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">GitHub पर Star करें</a>",
        "id":"Open source &middot; MIT &middot; Tanpa telemetri &middot; Tanpa LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Bintangi di GitHub</a>",
        "vi":"Mã nguồn mở &middot; MIT &middot; Không telemetry &middot; Không LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star trên GitHub</a>",
        "th":"โอเพนซอร์ส &middot; MIT &middot; ไม่มี telemetry &middot; ไม่มี LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star บน GitHub</a>",
        "ar":"مفتوح المصدر &middot; MIT &middot; بلا تتبّع &middot; بلا نموذج لغوي &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">أضف نجمة على GitHub</a>",
        "es":"Open source &middot; MIT &middot; Sin telemetría &middot; Sin LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star en GitHub</a>",
        "fr":"Open source &middot; MIT &middot; Sans télémétrie &middot; Sans LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star sur GitHub</a>",
        "de":"Open Source &middot; MIT &middot; Ohne Telemetrie &middot; Ohne LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star auf GitHub</a>",
        "pt-BR":"Open source &middot; MIT &middot; Sem telemetria &middot; Sem LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Dê star no GitHub</a>",
        "ru":"Open source &middot; MIT &middot; Без телеметрии &middot; Без LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Поставить звезду на GitHub</a>",
        "tr":"Açık kaynak &middot; MIT &middot; Telemetri yok &middot; LLM yok &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">GitHub'da yıldız ver</a>",
        "it":"Open source &middot; MIT &middot; Senza telemetria &middot; Senza LLM &middot; <a href=\"https://github.com/Laith0003/ux-skill\" rel=\"noopener\">Star su GitHub</a>",
    }
)

# ============ FOOTER ============
STRINGS["footer_caption"] = k(
    "Design intelligence for AI coding. Built so every model session ships work that doesn't look generated.",
    **{
        "zh-CN":"AI 编程的设计智能。让每一次模型会话交付的作品都不像 AI 生成。",
        "zh-TW":"AI 編程的設計智能。讓每一次模型工作階段所交付的成品都不像 AI 生成。",
        "ja":"AI コーディングのためのデザインインテリジェンス。すべてのモデル・セッションが、生成物に見えない仕事を出荷するために。",
        "ko":"AI 코딩을 위한 디자인 인텔리전스. 모든 모델 세션이 AI가 만든 듯 보이지 않는 작업을 출시하도록 설계됨.",
        "hi":"AI coding के लिए डिज़ाइन इंटेलिजेंस। हर मॉडल सेशन ऐसा काम भेजे जो जेनरेटेड न दिखे।",
        "id":"Design intelligence untuk AI coding. Dibangun supaya setiap sesi model mengirim pekerjaan yang tidak terlihat dibuat AI.",
        "vi":"Design intelligence cho AI coding. Được tạo để mọi phiên model ship công việc không trông giống do AI tạo.",
        "th":"ดีไซน์อัจฉริยะสำหรับ AI coding · ทำขึ้นเพื่อให้ทุกเซสชันของโมเดลส่งงานที่ไม่ดูเหมือนถูก AI สร้าง",
        "ar":"ذكاء تصميم لأدوات البرمجة بالذكاء الاصطناعي. مصمَّم لكي تُسلِّم كلّ جلسةٍ للنموذج عملًا لا يبدو مولَّدًا.",
        "es":"Inteligencia de diseño para coding con IA. Hecho para que cada sesión de modelo envíe trabajo que no parezca generado.",
        "fr":"L&rsquo;intelligence du design pour le codage par IA. Conçu pour que chaque session du modèle livre un travail qui ne semble pas généré.",
        "de":"Design-Intelligence für KI-Coding. Gebaut, damit jede Modell-Session Arbeit liefert, die nicht generiert aussieht.",
        "pt-BR":"Inteligência de design para coding com IA. Construído para que cada sessão do modelo envie trabalho que não parece gerado.",
        "ru":"Дизайн-интеллект для AI-кодинга. Сделан так, чтобы каждая сессия модели шипила работу, не похожую на сгенерированную.",
        "tr":"AI kodlama için tasarım zekâsı. Her model oturumunun, üretilmiş gibi durmayan iş gönderebilmesi için yapıldı.",
        "it":"Intelligenza di design per coding con AI. Costruito perché ogni sessione del modello spedisca lavoro che non sembri generato.",
    }
)

STRINGS["footer_col_plugin"] = k("The plugin",
    **{"zh-CN":"插件","zh-TW":"外掛","ja":"プラグイン","ko":"플러그인","hi":"plugin",
       "id":"Plugin-nya","vi":"Plugin","th":"ปลั๊กอิน","ar":"الإضافة",
       "es":"El plugin","fr":"Le plugin","de":"Das Plugin","pt-BR":"O plugin","ru":"Плагин","tr":"Eklenti","it":"Il plugin"})

STRINGS["footer_col_reading"] = k("Reading",
    **{"zh-CN":"阅读","zh-TW":"閱讀","ja":"読みもの","ko":"읽을거리","hi":"पढ़ने के लिए",
       "id":"Bacaan","vi":"Đọc","th":"อ่าน","ar":"للقراءة",
       "es":"Lecturas","fr":"À lire","de":"Lesestoff","pt-BR":"Leitura","ru":"Чтение","tr":"Okuma","it":"Letture"})

STRINGS["footer_col_get_it"] = k("Get it",
    **{"zh-CN":"获取","zh-TW":"取得","ja":"入手","ko":"받기","hi":"पाएँ",
       "id":"Dapatkan","vi":"Lấy về","th":"รับมา","ar":"احصل عليه",
       "es":"Conseguilo","fr":"Récupérer","de":"Holen","pt-BR":"Pegue","ru":"Получить","tr":"Edin","it":"Prendilo"})

STRINGS["footer_link_brand_specs"] = k("Brand specs &middot; 160",
    **{"zh-CN":"品牌规范 &middot; 160","zh-TW":"品牌規範 &middot; 160","ja":"ブランド仕様 &middot; 160","ko":"브랜드 사양 &middot; 160","hi":"ब्रांड specs &middot; 160",
       "id":"Spec brand &middot; 160","vi":"Spec thương hiệu &middot; 160","th":"สเปกแบรนด์ &middot; 160","ar":"مواصفات العلامات &middot; 160",
       "es":"Specs de marca &middot; 160","fr":"Specs de marque &middot; 160","de":"Brand-Specs &middot; 160",
       "pt-BR":"Specs de marca &middot; 160","ru":"Brand specs &middot; 160","tr":"Marka spec'leri &middot; 160","it":"Spec brand &middot; 160"})

STRINGS["footer_link_anti_patterns"] = k("Anti-patterns &middot; 145",
    **{"zh-CN":"反模式 &middot; 145","zh-TW":"反模式 &middot; 145","ja":"アンチパターン &middot; 145","ko":"안티패턴 &middot; 145","hi":"एंटी-पैटर्न &middot; 145",
       "id":"Anti-pola &middot; 145","vi":"Chống mẫu &middot; 145","th":"แอนตี้แพทเทิร์น &middot; 145","ar":"الأنماط المضادّة &middot; 145",
       "es":"Anti-patrones &middot; 145","fr":"Anti-patterns &middot; 145","de":"Anti-Patterns &middot; 145",
       "pt-BR":"Anti-padrões &middot; 145","ru":"Анти-паттерны &middot; 145","tr":"Anti-pattern'lar &middot; 145","it":"Anti-pattern &middot; 145"})

STRINGS["footer_link_slash_commands"] = k("Slash commands &middot; 23",
    **{"zh-CN":"斜杠命令 &middot; 23","zh-TW":"斜線命令 &middot; 23","ja":"スラッシュコマンド &middot; 23","ko":"슬래시 명령어 &middot; 23","hi":"slash commands &middot; 23",
       "id":"Slash command &middot; 23","vi":"Slash command &middot; 23","th":"slash command &middot; 23","ar":"أوامر بشرطة مائلة &middot; 23",
       "es":"Slash commands &middot; 23","fr":"Slash commands &middot; 23","de":"Slash-Commands &middot; 23",
       "pt-BR":"Slash commands &middot; 23","ru":"Slash-команды &middot; 23","tr":"Slash komutları &middot; 23","it":"Slash command &middot; 23"})

STRINGS["footer_link_mcp_server"] = k("MCP server &middot; 18 tools",
    **{"zh-CN":"MCP 服务器 &middot; 18 个工具","zh-TW":"MCP 伺服器 &middot; 18 個工具","ja":"MCP サーバー &middot; 18 ツール","ko":"MCP 서버 &middot; 18개 도구","hi":"MCP server &middot; 18 tools",
       "id":"Server MCP &middot; 18 tool","vi":"MCP server &middot; 18 tool","th":"เซิร์ฟเวอร์ MCP &middot; 18 เครื่องมือ","ar":"خادم MCP &middot; 18 أداة",
       "es":"Servidor MCP &middot; 18 herramientas","fr":"Serveur MCP &middot; 18 outils","de":"MCP-Server &middot; 18 Tools",
       "pt-BR":"Servidor MCP &middot; 18 ferramentas","ru":"MCP-сервер &middot; 18 инструментов","tr":"MCP sunucusu &middot; 18 araç","it":"Server MCP &middot; 18 strumenti"})

STRINGS["footer_link_launch_post"] = k("v3.0 The Brain &middot; launch",
    **{"zh-CN":"v3.0 The Brain &middot; 发布","zh-TW":"v3.0 The Brain &middot; 發布","ja":"v3.0 The Brain &middot; ローンチ","ko":"v3.0 The Brain &middot; 런치","hi":"v3.0 The Brain &middot; launch",
       "id":"v3.0 The Brain &middot; peluncuran","vi":"v3.0 The Brain &middot; launch","th":"v3.0 The Brain &middot; เปิดตัว","ar":"v3.0 The Brain &middot; الإطلاق",
       "es":"v3.0 The Brain &middot; lanzamiento","fr":"v3.0 The Brain &middot; lancement","de":"v3.0 The Brain &middot; Launch",
       "pt-BR":"v3.0 The Brain &middot; lançamento","ru":"v3.0 The Brain &middot; запуск","tr":"v3.0 The Brain &middot; lansman","it":"v3.0 The Brain &middot; lancio"})

STRINGS["footer_link_all_posts"] = k("All posts",
    **{"zh-CN":"全部文章","zh-TW":"全部文章","ja":"全投稿","ko":"전체 글","hi":"सभी posts",
       "id":"Semua post","vi":"Tất cả bài","th":"โพสต์ทั้งหมด","ar":"جميع التدوينات",
       "es":"Todos los posts","fr":"Tous les posts","de":"Alle Beiträge",
       "pt-BR":"Todos os posts","ru":"Все посты","tr":"Tüm yazılar","it":"Tutti i post"})

STRINGS["footer_link_github_source"] = k("GitHub source",
    **{"zh-CN":"GitHub 源码","zh-TW":"GitHub 原始碼","ja":"GitHub ソース","ko":"GitHub 소스","hi":"GitHub source",
       "id":"Source di GitHub","vi":"Mã nguồn GitHub","th":"ซอร์สบน GitHub","ar":"المصدر على GitHub",
       "es":"Código en GitHub","fr":"Source GitHub","de":"GitHub-Quelle","pt-BR":"Código no GitHub","ru":"Исходник на GitHub","tr":"GitHub kaynağı","it":"Sorgente GitHub"})

STRINGS["footer_bottom_license"] = k("MIT licensed &middot; No telemetry &middot; No account",
    **{"zh-CN":"MIT 许可 &middot; 无遥测 &middot; 无账号","zh-TW":"MIT 授權 &middot; 無遙測 &middot; 無帳號",
       "ja":"MIT ライセンス &middot; テレメトリなし &middot; アカウントなし","ko":"MIT 라이선스 &middot; 텔레메트리 없음 &middot; 계정 없음",
       "hi":"MIT licensed &middot; कोई टेलीमेट्री नहीं &middot; कोई account नहीं","id":"Lisensi MIT &middot; Tanpa telemetri &middot; Tanpa akun",
       "vi":"MIT licensed &middot; Không telemetry &middot; Không tài khoản","th":"ใช้สัญญาอนุญาต MIT &middot; ไม่มี telemetry &middot; ไม่มีบัญชี",
       "ar":"مرخَّص MIT &middot; بلا تتبّع &middot; بلا حساب","es":"Licencia MIT &middot; Sin telemetría &middot; Sin cuenta",
       "fr":"Licence MIT &middot; Sans télémétrie &middot; Sans compte","de":"MIT-Lizenz &middot; Ohne Telemetrie &middot; Ohne Account",
       "pt-BR":"Licença MIT &middot; Sem telemetria &middot; Sem conta","ru":"Лицензия MIT &middot; Без телеметрии &middot; Без аккаунта",
       "tr":"MIT lisansı &middot; Telemetri yok &middot; Hesap yok","it":"Licenza MIT &middot; Senza telemetria &middot; Senza account"})


# ============ WRITE ============
def main():
    data = {
        "_meta": {
            "version": "2.0",
            "base": "docs/index.html",
            "note": "Strings keyed by stable English text (HTML entity-preserving). Each translation is a flat dict; missing keys fall back to English. Code, brand names, file paths, stat numbers, and terminal text STAY in English on every language version.",
            "generated_by": "scripts/build_i18n_json.py",
        },
        "languages": LANGS,
        "strings": STRINGS,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {len(STRINGS)} keys across {len(LANGS)} languages.")


if __name__ == "__main__":
    main()




