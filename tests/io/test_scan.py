"""The scanner: every value a codebase actually uses, from CSS, inline
styles in HTML and Blade, JSX style props and Tailwind classes, each with
its file, line, property, state and whether it names a token or writes a
raw value. It reads files and never writes one."""
import json
import os
import time

import pytest

from engine.foundations.errors import InputError
from engine.foundations.tokens import Token, TokenSet
from engine.io.report import Source
from engine.io.scan import MAX_BYTES, SKIP_DIRS, Scan, Usage, canonical, scan
from engine.io.tailwind_in import import_tailwind_css, import_tailwind_json

CSS = """.btn {
  background: var(--color-primary);
  color: #FFF;
  padding: 12px 1rem;
  border-radius: 8px;
  border: 1px solid #d0d4da;
  transition: background 150ms ease-out;
}
.btn:hover { background: var(--color-primary-hover); }
.card { border-radius: .5rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); z-index: 10; }
:root { --local: #fff; }
"""

JSX = """export function Tag({label}) {
  return (
    <span className="bg-surface text-ink hover:bg-[#3366ff] p-4 rounded-[11px]"
          style={{ color: '#ffffff', paddingInline: 12, borderRadius: '0.5rem' }}>
      {label}
    </span>
  );
}
"""

BLADE = """<div class="card" style="color: white; margin-block: 16px">
  <button class="disabled:text-muted" disabled>{{ $label }}</button>
</div>
<style>
  .note { gap: 4px; }
</style>
"""


def _project(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "button.css").write_text(CSS, encoding="utf-8")
    (tmp_path / "src" / "Tag.jsx").write_text(JSX, encoding="utf-8")
    (tmp_path / "views").mkdir()
    (tmp_path / "views" / "card.blade.php").write_text(BLADE, encoding="utf-8")
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "x.css").write_text(".a { color: red; }", encoding="utf-8")
    (tmp_path / "tokens.css").write_text(":root { --color-primary: #36f; }", encoding="utf-8")
    return tmp_path


def _tokens():
    ts = TokenSet({})
    for path, value in (("color-primary", "#3366FF"), ("color-primary-hover", "#2952CC"),
                        ("color-surface", "#FFFFFF"), ("color-ink", "#111111"),
                        ("spacing", {"value": 0.25, "unit": "rem"})):
        kind = "color" if isinstance(value, str) else "dimension"
        ts.add(Token(path, kind, value))
    return ts


def _rows(result):
    return [(u.file, u.line, u.prop, u.family, u.kind, u.value, u.state) for u in result.usages]


def _one(tmp_path, name, text, ts=None):
    (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / name).write_text(text, encoding="utf-8")
    return scan([tmp_path], _tokens() if ts is None else ts)


def test_css_declarations_give_token_and_raw_usages(tmp_path):
    result = scan([_project(tmp_path)], _tokens(), exclude=[tmp_path / "tokens.css"])
    rows = [r for r in _rows(result) if r[0] == "src/button.css"]
    assert rows == [
        ("src/button.css", 2, "background", "color", "token", "color-primary", ""),
        ("src/button.css", 3, "color", "color", "raw", "#FFFFFF", ""),
        ("src/button.css", 4, "padding", "space", "raw", "12px", ""),
        ("src/button.css", 4, "padding", "space", "raw", "16px", ""),
        ("src/button.css", 5, "border-radius", "radius", "raw", "8px", ""),
        ("src/button.css", 6, "border", "border", "raw", "1px", ""),
        ("src/button.css", 6, "border", "color", "raw", "#D0D4DA", ""),
        ("src/button.css", 7, "transition", "duration", "raw", "150ms", ""),
        ("src/button.css", 7, "transition", "motion", "raw", "cubic-bezier(0, 0, 0.58, 1)", ""),
        ("src/button.css", 9, "background", "color", "token", "color-primary-hover", "hover"),
        ("src/button.css", 10, "border-radius", "radius", "raw", "8px", ""),
        ("src/button.css", 10, "box-shadow", "shadow", "raw", "0px 1px 3px 0px #0000001A", ""),
        ("src/button.css", 10, "z-index", "z", "raw", "10", "")]
    written = {u.text for u in result.usages if u.file == "src/button.css" and u.line == 10
               and u.family == "radius"}
    assert written == {".5rem"}


def test_jsx_classes_and_style_props(tmp_path):
    result = scan([_project(tmp_path)], _tokens(), exclude=[tmp_path / "tokens.css"])
    rows = [r for r in _rows(result) if r[0] == "src/Tag.jsx"]
    assert rows == [
        ("src/Tag.jsx", 3, "bg-surface", "color", "token", "color-surface", ""),
        ("src/Tag.jsx", 3, "text-ink", "color", "token", "color-ink", ""),
        ("src/Tag.jsx", 3, "bg-[#3366ff]", "color", "raw", "#3366FF", "hover"),
        ("src/Tag.jsx", 3, "p-4", "space", "token", "spacing", ""),
        ("src/Tag.jsx", 3, "rounded-[11px]", "radius", "raw", "11px", ""),
        ("src/Tag.jsx", 4, "color", "color", "raw", "#FFFFFF", ""),
        ("src/Tag.jsx", 4, "padding-inline", "space", "raw", "12px", ""),
        ("src/Tag.jsx", 4, "border-radius", "radius", "raw", "8px", "")]


def test_blade_and_html_style_attributes_classes_and_style_blocks(tmp_path):
    result = scan([_project(tmp_path)], _tokens(), exclude=[tmp_path / "tokens.css"])
    rows = [r for r in _rows(result) if r[0] == "views/card.blade.php"]
    assert rows == [
        ("views/card.blade.php", 1, "color", "color", "raw", "#FFFFFF", ""),
        ("views/card.blade.php", 1, "margin-block", "space", "raw", "16px", ""),
        ("views/card.blade.php", 5, "gap", "space", "raw", "4px", "")]
    unknown = [u for u in result.unknown_classes if u[0] == "views/card.blade.php"]
    assert unknown == [("views/card.blade.php", 2, "disabled:text-muted")]


def test_skipped_folders_and_excluded_files_are_not_read(tmp_path):
    result = scan([_project(tmp_path)], _tokens(), exclude=[tmp_path / "tokens.css"])
    assert "node_modules" in SKIP_DIRS
    assert {u.file for u in result.usages} == {"src/button.css", "src/Tag.jsx",
                                              "views/card.blade.php"}
    assert result.files == 3


def test_a_custom_property_defined_in_app_css_is_a_definition_not_a_raw_use(tmp_path):
    result = scan([_project(tmp_path)], _tokens(), exclude=[tmp_path / "tokens.css"])
    assert not any(u.prop == "--local" for u in result.usages)


def test_usage_carries_what_it_needs_for_the_report():
    u = Usage("a.css", 3, "color", "color", "raw", "#FFFFFF", "#fff", "")
    assert u.where() == "a.css:3"


# Beyond the plain case ------------------------------------------------------

def test_canonical_gives_one_text_per_value():
    assert canonical("dimension", {"value": 1, "unit": "rem"}) == "16px"
    assert canonical("duration", {"value": 0.2, "unit": "s"}) == "200ms"
    assert canonical("color", "#3366FF") == "#3366FF"
    assert canonical("number", 1.5) == "1.5"


def test_nested_rules_and_at_rules_are_read_with_their_state(tmp_path):
    scss = """// a line comment: color: #123456;
.panel {
  padding: 8px;
  &:hover { color: #222222; }
  .title { font-size: 18px; }
  @media (min-width: 40rem) {
    padding: 24px;
  }
  @supports (display: grid) { gap: 12px; }
}
@layer components {
  .chip:focus-visible { outline: 2px solid #3366ff; }
  .chip[disabled] { color: #999999; }
}
@keyframes pulse { from { opacity: 1; } to { background-color: #eeeeee; } }
@font-face { font-family: "Local Face"; font-weight: 400; }
"""
    rows = [r[1:] for r in _rows(_one(tmp_path, "panel.scss", scss))]
    assert rows == [
        (3, "padding", "space", "raw", "8px", ""),
        (4, "color", "color", "raw", "#222222", "hover"),
        (5, "font-size", "type-size", "raw", "18px", ""),
        (7, "padding", "space", "raw", "24px", ""),
        (9, "gap", "space", "raw", "12px", ""),
        (12, "outline", "border", "raw", "2px", "focus"),
        (12, "outline", "color", "raw", "#3366FF", "focus"),
        (13, "color", "color", "raw", "#999999", "disabled"),
        (15, "background-color", "color", "raw", "#EEEEEE", "")]


def test_dark_selectors_and_queries_record_the_dark_scheme(tmp_path):
    css = """.dark .card { color: #eeeeee; }
[data-theme="dark"] .card:hover { color: #ffffff; }
@media (prefers-color-scheme: dark) { .card { background: #000000; } }
:root:not(.dark) .card { color: #111111; }
"""
    rows = [(r[1], r[6]) for r in _rows(_one(tmp_path, "a.css", css))]
    assert rows == [(1, "scheme:dark"), (2, "scheme:dark,hover"), (3, "scheme:dark"), (4, "")]


def test_tailwind_variants_read_as_states_and_the_dark_scheme(tmp_path):
    html = ('<a class="dark:bg-ink dark:hover:text-surface group-hover:bg-primary '
            'focus-visible:p-2 active:bg-[#000] md:p-4 !bg-surface">x</a>\n')
    rows = [(r[2], r[4], r[6]) for r in _rows(_one(tmp_path, "a.html", html))]
    assert rows == [("bg-ink", "token", "scheme:dark"),
                    ("text-surface", "token", "scheme:dark,hover"),
                    ("bg-primary", "token", "hover"),
                    ("p-2", "token", "focus"),
                    ("bg-[#000]", "raw", "active"),
                    ("p-4", "token", ""),
                    ("bg-surface", "token", "")]


def test_a_var_to_a_token_the_system_lacks_is_missing(tmp_path):
    result = _one(tmp_path, "a.css", ".a { color: var(--brand-accent, #ff0000); }\n")
    assert _rows(result) == [("a.css", 1, "color", "color", "missing", "--brand-accent", "")]
    assert result.usages[0].text == "var(--brand-accent, #ff0000)"


def test_an_out_of_gamut_color_is_mapped_not_refused(tmp_path):
    result = _one(tmp_path, "a.css", ".a { color: oklch(0.7 0.4 145); }\n")
    [u] = result.usages
    assert (u.family, u.kind, u.text) == ("color", "raw", "oklch(0.7 0.4 145)")
    assert u.value.startswith("#") and len(u.value) == 7


def test_colors_inside_gradients_and_unreadable_shadows_are_still_found(tmp_path):
    css = (".a { background: linear-gradient(90deg, #ff0000, #0000ff 50%); "
           "box-shadow: 0 0 0 3px var(--color-ink), inset 0 1px #00ff00; }\n")
    rows = [(r[2], r[3], r[4], r[5]) for r in _rows(_one(tmp_path, "a.css", css))]
    assert rows == [("background", "color", "raw", "#FF0000"),
                    ("background", "color", "raw", "#0000FF"),
                    ("box-shadow", "color", "token", "color-ink"),
                    ("box-shadow", "color", "raw", "#00FF00")]


def test_apply_and_arbitrary_properties_are_class_uses(tmp_path):
    css = ".btn { @apply bg-primary hover:bg-primary-hover px-[13px]; }\n"
    rows = [(r[2], r[4], r[5], r[6]) for r in _rows(_one(tmp_path, "a.css", css))]
    assert rows == [("bg-primary", "token", "color-primary", ""),
                    ("bg-primary-hover", "token", "color-primary-hover", "hover"),
                    ("px-[13px]", "raw", "13px", "")]
    jsx = ('<i className="[color:#ff0000] bg-[var(--color-ink)] bg-(--color-surface) '
           'text-[length:14px] z-10 duration-150 border" />\n')
    rows = [(r[2], r[3], r[4], r[5]) for r in _rows(_one(tmp_path, "b.jsx", jsx))
            if r[0] == "b.jsx"]
    assert rows == [("color", "color", "raw", "#FF0000"),
                    ("bg-[var(--color-ink)]", "color", "token", "color-ink"),
                    ("bg-(--color-surface)", "color", "token", "color-surface"),
                    ("text-[length:14px]", "type-size", "raw", "14px"),
                    ("z-10", "z", "raw", "10"),
                    ("duration-150", "duration", "raw", "150ms"),
                    ("border", "border", "raw", "1px")]


def test_a_var_in_an_arbitrary_class_takes_its_family_from_the_hint(tmp_path):
    html = ('<p class="text-[var(--muted)] text-[length:var(--step)] text-(length:--step) '
            'border-[var(--line)]">x</p>\n')
    rows = [(r[2], r[3], r[4]) for r in _rows(_one(tmp_path, "a.html", html))]
    assert rows == [("text-[var(--muted)]", "color", "missing"),
                    ("text-[length:var(--step)]", "type-size", "missing"),
                    ("text-(length:--step)", "type-size", "missing"),
                    ("border-[var(--line)]", "color", "missing")]


def test_keyword_utilities_are_not_listed_as_unknown(tmp_path):
    html = ('<p class="text-center border-solid rounded-full bg-transparent flex p mt m-auto '
            'text-lg bg-brand">x</p>\n')
    result = _one(tmp_path, "a.html", html)
    assert [c for _, _, c in result.unknown_classes] == ["text-lg", "bg-brand"]
    assert result.usages == []


def test_class_expressions_and_bound_styles_in_components(tmp_path):
    jsx = """const a = <div className={cn("p-4", active && 'bg-primary', `text-ink`)} />;
const b = <div
  style={{
    zIndex: 3,
    lineHeight: 1.5,
    "margin-top": 8,
  }} />;
"""
    rows = [(r[1], r[2], r[5]) for r in _rows(_one(tmp_path, "a.tsx", jsx))]
    assert rows == [(1, "p-4", "spacing"), (1, "bg-primary", "color-primary"),
                    (1, "text-ink", "color-ink"), (4, "z-index", "3"),
                    (5, "line-height", "1.5"), (6, "margin-top", "8px")]
    vue = """<template>
  <div :style="{ color: '#ff0000', paddingTop: '4px' }" :class="{ 'bg-surface': on }"></div>
</template>
<style scoped lang="scss">
.x { gap: 2px; } // trailing: gap: 99px;
</style>
"""
    rows = [(r[1], r[2], r[5]) for r in _rows(_one(tmp_path, "b.vue", vue))
            if r[0] == "b.vue"]
    assert rows == [(2, "color", "#FF0000"), (2, "padding-top", "4px"),
                    (2, "bg-surface", "color-surface"), (5, "gap", "2px")]
    svelte = '<div style:color="#00ff00" style="margin: 0 2px"></div>\n'
    rows = [(r[2], r[5]) for r in _rows(_one(tmp_path, "c.svelte", svelte))
            if r[0] == "c.svelte"]
    assert rows == [("color", "#00FF00"), ("margin", "2px")]


def test_multiline_class_attributes_give_each_class_its_own_line(tmp_path):
    html = '<div class="p-4\n  bg-primary\n  text-ink">x</div>\n'
    assert [(r[1], r[2]) for r in _rows(_one(tmp_path, "a.html", html))] == [
        (1, "p-4"), (2, "bg-primary"), (3, "text-ink")]


def test_tailwind_classes_name_tokens_as_the_tailwind_importers_name_them(tmp_path):
    v4 = """@theme {
  --color-ink: #1b1d22;
  --spacing: 0.25rem;
  --radius-card: 0.75rem;
  --text-body: 1rem;
  --font-sans: "Body Sans", sans-serif;
  --font-weight-strong: 650;
  --shadow-raised: 0 1px 2px #0000001a;
  --leading-snug: 1.3;
  --tracking-tight: -0.01rem;
  --ease-snap: cubic-bezier(0.3, 0, 0, 1);
}
"""
    ts4 = import_tailwind_css(v4, Source("app.css", "tailwind", "0" * 64, len(v4))).tokens
    v3 = json.dumps({"colors": {"ink": {"700": "#1b1d22"}}, "spacing": {"4": "1rem"},
                     "borderRadius": {"card": "12px"}, "fontSize": {"body": "16px"},
                     "fontFamily": {"sans": ["Body Sans", "sans-serif"]},
                     "fontWeight": {"strong": "650"}, "boxShadow": {"raised": "0 1px 2px #000"},
                     "lineHeight": {"snug": "1.3"}, "letterSpacing": {"tight": "-0.01rem"},
                     "transitionTimingFunction": {"snap": "cubic-bezier(0.3, 0, 0, 1)"},
                     "transitionDuration": {"150": "150ms"}, "zIndex": {"10": "10"},
                     "borderWidth": {"DEFAULT": "1px"}})
    ts3 = import_tailwind_json(v3, Source("t.json", "tailwind-json", "0" * 64, len(v3))).tokens
    html4 = ('<b class="text-ink p-3 rounded-card text-body font-sans font-strong '
             'shadow-raised leading-snug tracking-tight ease-snap"></b>\n')
    rows = [(r[2], r[3], r[5]) for r in _rows(_one(tmp_path / "v4", "a.html", html4, ts4))]
    assert rows == [("text-ink", "color", "color-ink"), ("p-3", "space", "spacing"),
                    ("rounded-card", "radius", "radius-card"),
                    ("text-body", "type-size", "text-body"), ("font-sans", "font", "font-sans"),
                    ("font-strong", "weight", "font-weight-strong"),
                    ("shadow-raised", "shadow", "shadow-raised"),
                    ("leading-snug", "leading", "leading-snug"),
                    ("tracking-tight", "tracking", "tracking-tight"),
                    ("ease-snap", "motion", "ease-snap")]
    html3 = ('<b class="text-ink-700/50 p-4 rounded-card text-body font-sans font-strong '
             'shadow-raised leading-snug tracking-tight ease-snap duration-150 z-10 border">'
             '</b>\n')
    rows = [(r[2], r[3], r[5]) for r in _rows(_one(tmp_path / "v3", "a.html", html3, ts3))]
    assert rows == [("text-ink-700/50", "color", "colors.ink.700"),
                    ("p-4", "space", "spacing.4"),
                    ("rounded-card", "radius", "borderRadius.card"),
                    ("text-body", "type-size", "fontSize.body"),
                    ("font-sans", "font", "fontFamily.sans"),
                    ("font-strong", "weight", "fontWeight.strong"),
                    ("shadow-raised", "shadow", "boxShadow.raised"),
                    ("leading-snug", "leading", "lineHeight.snug"),
                    ("tracking-tight", "tracking", "letterSpacing.tight"),
                    ("ease-snap", "motion", "transitionTimingFunction.snap"),
                    ("duration-150", "duration", "transitionDuration.150"),
                    ("z-10", "z", "zIndex.10"),
                    ("border", "border", "borderWidth.DEFAULT")]


def test_binary_large_and_minified_files_are_skipped_and_reported(tmp_path):
    (tmp_path / "logo.css").write_bytes(b"\x89PNG\x00\x00binary")
    (tmp_path / "huge.css").write_text(".a { color: #fff; }\n" * (MAX_BYTES // 10),
                                       encoding="utf-8")
    (tmp_path / "vendor.min.css").write_text(".a{color:#fff}", encoding="utf-8")
    (tmp_path / "latin.css").write_bytes(b".a { content: '\xe9'; }")
    (tmp_path / "ok.css").write_text(".a { color: #fff; }\n", encoding="utf-8")
    result = scan([tmp_path], _tokens())
    assert result.files == 1
    assert [s[0] for s in result.skipped] == ["huge.css", "latin.css", "logo.css",
                                              "vendor.min.css"]
    reasons = dict(result.skipped)
    assert "larger than" in reasons["huge.css"]
    assert "binary" in reasons["logo.css"]
    assert "UTF-8" in reasons["latin.css"] and "save it as UTF-8" in reasons["latin.css"]
    assert "minified" in reasons["vendor.min.css"]


def test_a_stylesheet_that_does_not_parse_is_reported_and_the_rest_is_read(tmp_path):
    (tmp_path / "a.css").write_text(".a {\n  color: #fff;\n.b { gap: 2px; }\n",
                                    encoding="utf-8")
    (tmp_path / "b.css").write_text(".b { gap: 2px; }\n", encoding="utf-8")
    result = scan([tmp_path], _tokens())
    assert [u.file for u in result.usages] == ["b.css"]
    [(file, why)] = result.skipped
    assert file == "a.css"
    assert "line 1" in why and "add the missing }" in why


def test_a_root_that_does_not_exist_names_the_path_and_the_fix(tmp_path):
    with pytest.raises(InputError) as err:
        scan([tmp_path / "nowhere"], _tokens())
    message = str(err.value)
    assert "nowhere" in message and "pass" in message


def test_a_file_root_is_read_and_hidden_folders_are_not(tmp_path):
    (tmp_path / ".cache").mkdir()
    (tmp_path / ".cache" / "a.css").write_text(".a { gap: 1px; }", encoding="utf-8")
    (tmp_path / "one.css").write_text(".a { gap: 3px; }", encoding="utf-8")
    assert [u.file for u in scan([tmp_path], _tokens()).usages] == ["one.css"]
    assert [u.file for u in scan([tmp_path / "one.css"], _tokens()).usages] == ["one.css"]


def test_the_scanner_writes_nothing(tmp_path):
    _project(tmp_path)

    def state():
        return sorted((p, os.stat(os.path.join(p, n)).st_mtime_ns)
                      for p, _, names in os.walk(tmp_path) for n in names)
    before = state()
    scan([tmp_path], _tokens())
    assert state() == before


def test_the_same_tree_scans_the_same_way(tmp_path):
    _project(tmp_path)
    first, second = scan([tmp_path], _tokens()), scan([tmp_path], _tokens())
    assert first == second
    assert isinstance(first, Scan)


def test_a_few_thousand_small_files_scan_in_a_few_seconds(tmp_path):
    for d in range(30):
        folder = tmp_path / f"pkg{d}"
        folder.mkdir()
        for i in range(100):
            (folder / f"c{i}.css").write_text(CSS, encoding="utf-8") if i % 2 else \
                (folder / f"C{i}.jsx").write_text(JSX, encoding="utf-8")
    start = time.perf_counter()
    result = scan([tmp_path], _tokens())
    elapsed = time.perf_counter() - start
    assert result.files == 3000
    assert elapsed < 5, f"3000 files took {elapsed:.1f}s"
