"""The Tailwind 4 exporter: a system's semantic roles and its faces in
Tailwind's theme namespaces inside @theme, primitives left out, each mode
an override block the way tokens.css switches it, breakpoints read from the
tokens, and a phone style beside each style that steps down on a phone. It
round trips through the Tailwind importer byte for byte; an imported
Tailwind system is written back in its own names.

Whether a system is the engine's own is read from its ownership record
(the record of the files the engine wrote, the engine's digest in a
stylesheet it wrote, its extension key on a tokens file it wrote), never
from token names. A stylesheet the engine
wrote is rewritten in place; one it did not write is never rewritten: the
additions go in an extension stylesheet beside it, stamped as the
engine's, with its own @theme block."""
import json
from pathlib import Path

import pytest

from engine.existing import is_ux_skill_file, ownership, stamp_digest
from engine.existing.record import RECORD, record_text
from engine.foundations.build import build_system
from engine.foundations.errors import InputError
from engine.foundations.export import dump_dtcg, to_css
from engine.foundations.tokens import Token, TokenSet
from engine.io.css_in import import_css
from engine.io.dtcg_in import import_dtcg, read_dtcg
from engine.io.intake import INTAKE_DIR
from engine.io.report import Source
from engine.io.tailwind_in import import_tailwind_css, read_tailwind
from engine.io.tailwind_out import (
    RESETS, export_tailwind, extension_name, tailwind_extension, tailwind_name, to_tailwind,
    write_tailwind)
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)


def _ours():
    return build_system(NEUTRAL, "#3366FF").tokens


# A folder no record can sit in, so a source read from text is never
# taken as the engine's because of a record where the tests run.
NOWHERE = Path(__file__).resolve().parent / "no-such-folder"


@pytest.fixture(autouse=True)
def _nowhere():
    assert not NOWHERE.exists()


def _import(text, name="theme.css"):
    return import_tailwind_css(text, Source(str(NOWHERE / name), "tailwind", "0" * 64,
                                            len(text)))


def test_roles_take_tailwind_names_in_its_namespaces():
    assert [tailwind_name(r) for r in (
        "color.surface.page", "space.control.gap", "radius.card", "elevation.card",
        "elevation.order.dialog", "border.outline", "border.style.default",
        "motion.reveal.curve", "motion.reveal.duration", "motion.inline-sign",
        "layout.breakpoint.tablet", "layout.container.max", "layout.measure.text",
        "layout.gutter.phone", "layout.columns.phone", "layout.target.min", "type.face.text",
        "type.text.body", "type.strong", "layout.region-gap.phone",
        "layout.hero.padding-block.desktop", "layout.header.padding-block", "type.face.display",
        "type.run.arabic", "type.text.section-title", "type.icon.size.control",
        "imagery.ratio.hero", "imagery.scrim", "radius.media", "type.phone.hero")] == [
        "color-surface-page", "spacing-control-gap", "radius-card", "shadow-card",
        "z-dialog", "border-outline", "border-style-default", "ease-reveal",
        "duration-reveal", "motion-inline-sign", "breakpoint-tablet", "container-max",
        "container-measure-text", "spacing-gutter-phone", "columns-phone",
        "spacing-target-min", "font-text", "text-body", "font-weight-strong",
        "spacing-region-gap-phone", "spacing-hero-padding-block-desktop",
        "spacing-header-padding-block", "font-display", "font-run-arabic",
        "text-section-title", "spacing-icon-control", "aspect-hero", "color-imagery-scrim",
        "radius-media", None]


def test_the_theme_holds_roles_only_with_resolved_values():
    ts = _ours()
    text = to_tailwind(ts, roles=True)
    head = text[:text.index("}")]
    assert head.startswith("@theme {\n" + "".join(f"  {r}: initial;\n" for r in RESETS))
    assert f"  --color-surface-page: {ts.resolve('color.surface.page')};\n" in head
    assert "  --spacing-control-gap: 12px;\n" in head
    assert "  --breakpoint-tablet: 640px;\n" in head
    assert "  --text-body: 1rem;\n" in head
    assert "  --text-body--line-height: 1.55;\n" in head
    assert "  --text-body--font-weight: 400;\n" in head
    assert "  --font-weight-strong: 600;\n" in head
    assert "  --font-display: " in head and "  --aspect-hero: 1.7778;\n" in head
    assert "--color-brand-500" not in text and "var(" not in text
    # @theme holds custom properties only; the base color-scheme follows it.
    assert all(line.startswith("  --") for line in head.splitlines()[1:])
    assert text[len(head):].startswith("}\n\n:root {\n  color-scheme: light;\n}\n")


def test_a_style_that_steps_down_on_a_phone_has_a_phone_style_beside_it():
    ts = _ours()
    text = to_tailwind(ts, roles=True)
    factor = ts.resolve("type.phone.hero")
    size = ts.resolve("type.text.hero")["fontSize"]
    assert size == {"value": 3.375, "unit": "rem"} and factor == 0.568
    assert "  --text-hero-phone: 1.9169rem;\n" in text
    assert "  --text-hero-phone--letter-spacing: -0.62px;\n" in text
    rtl = text[text.index('\n:root[dir="rtl"] {'):]
    assert "  --text-hero-phone: 2.2012rem;\n" in rtl
    assert "--text-body-phone" not in text


def test_modes_switch_the_same_variables_the_way_tokens_css_does():
    ts = _ours()
    text = to_tailwind(ts, roles=True)
    dark = text[text.index('\n:root[data-theme="dark"] {'):]
    assert f"  --color-surface-page: {ts.resolve('color.surface.page', 'scheme:dark')};" in dark
    assert '@media (prefers-color-scheme: dark) {\n  :root:not([data-theme="light"]) {' in text
    assert '\n:root[dir="rtl"] {\n' in text


@pytest.mark.parametrize("scheme", ["system", "light", "dark"])
def test_our_export_round_trips_through_the_importer_byte_for_byte(scheme):
    text = to_tailwind(_ours(), scheme=scheme, roles=True)
    imported = _import(text)
    assert imported.report.not_read == []
    assert imported.resets == RESETS and imported.scheme == scheme
    assert to_tailwind(imported.tokens, imported.forms, imported.resets,
                       scheme=imported.scheme, roles=False) == text
    assert export_tailwind(imported) == text


def test_the_output_is_the_same_bytes_every_time():
    assert to_tailwind(_ours(), roles=True) == to_tailwind(_ours(), roles=True)


def test_an_imported_tailwind_system_is_written_back_in_its_own_names():
    source = """@theme {
  --color-*: initial;
  --color-ink: #1b1d22;
  --color-paper: #fdfdfb;
  --color-surface: var(--color-paper);
  --radius-card: 0.75rem;
}

.dark {
  --color-surface: var(--color-ink);
}
"""
    first = _import(source)
    assert first.resets == ("--color-*",)
    text = to_tailwind(first.tokens, first.forms, first.resets, scheme=first.scheme,
                       roles=False)
    assert text == ("@theme {\n  --color-*: initial;\n  --color-ink: #1B1D22;\n"
                    "  --color-paper: #FDFDFB;\n  --color-surface: var(--color-paper);\n"
                    "  --radius-card: 0.75rem;\n}\n\n:root {\n  color-scheme: light;\n}\n\n"
                    ".dark {\n  color-scheme: dark;\n  --color-surface: var(--color-ink);\n}\n")
    second = _import(text)
    assert [(t.path, t.value, t.modes) for t in second.tokens.tokens()] == [
        (t.path, t.value, t.modes) for t in first.tokens.tokens()]
    assert to_tailwind(second.tokens, second.forms, second.resets,
                       scheme=second.scheme, roles=False) == text


# ------------------------------------------------------------ the dark variant

NIGHT = """@custom-variant dark (&:where(.theme-night, .theme-night *));

@theme {
  --color-ink: #1b1d22;
  --color-paper: #fdfdfb;
  --color-surface: var(--color-paper);
}

.theme-night {
  --color-surface: var(--color-ink);
}
"""


def test_a_custom_dark_variant_is_recorded_and_written_back_as_the_file_has_it():
    first = _import(NIGHT)
    assert first.variant == "@custom-variant dark (&:where(.theme-night, .theme-night *));"
    assert first.forms["scheme"] == (".theme-night", "")
    text = export_tailwind(first)
    assert text.startswith("@custom-variant dark (&:where(.theme-night, .theme-night *));\n\n"
                           "@theme {\n")
    assert ".theme-night {\n  color-scheme: dark;\n  --color-surface: var(--color-ink);\n}\n" \
        in text
    second = _import(text)
    assert second.variant == first.variant
    assert export_tailwind(second) == text


def test_a_block_dark_variant_comes_back_verbatim():
    variant = "@custom-variant dark {\n  &:where(.night, .night *) {\n    @slot;\n  }\n}"
    first = _import(variant + "\n\n@theme {\n  --color-ink: #111111;\n}\n\n"
                    ".night {\n  --color-ink: #EEEEEE;\n}\n")
    assert first.variant == variant
    assert export_tailwind(first).startswith(variant + "\n\n@theme {\n")


def test_a_file_without_a_custom_variant_gets_none():
    assert _import("@theme {\n  --color-ink: #111111;\n}\n").variant == ""
    assert "@custom-variant" not in to_tailwind(_ours(), roles=True)


# ------------------------------------------------------------ ownership


FOREIGN_DTCG = {
    "gray": {"$type": "color", "900": {"$value": "#1B1D22"}, "50": {"$value": "#FDFDFB"}},
    "color": {"$type": "color", "brand": {"$value": "#3366FF"},
              "text": {"default": {"$value": "{gray.900}"}}},
    "spacing": {"$type": "dimension", "md": {"$value": {"value": 16, "unit": "px"}}},
}


def _dtcg(doc, name="tokens.json"):
    text = json.dumps(doc) if not isinstance(doc, str) else doc
    return import_dtcg(text, Source(str(NOWHERE / name), "dtcg", "0" * 64, len(text)))


def test_one_engine_style_name_never_makes_a_foreign_system_the_engines():
    imported = _dtcg(FOREIGN_DTCG)
    assert imported.tokens.has("color.text.default")
    assert imported.owned is False
    text = export_tailwind(imported)
    for name in ("--gray-900: #1B1D22;", "--gray-50: #FDFDFB;", "--color-brand: #3366FF;",
                 "--color-text-default: var(--gray-900);", "--spacing-md: 16px;"):
        assert f"  {name}\n" in text
    assert "initial" not in text


def test_a_foreign_system_named_entirely_in_engine_roles_is_still_foreign():
    doc = {"color": {"$type": "color", "surface": {"page": {"$value": "#FFFFFF"}},
                     "text": {"default": {"$value": "#111111"}}}}
    imported = _dtcg(doc)
    assert imported.owned is False
    assert export_tailwind(imported) == ("@theme {\n  --color-surface-page: #FFFFFF;\n"
                                         "  --color-text-default: #111111;\n}\n")


def test_the_engines_tokens_file_is_known_by_its_extension_key_and_exported_in_roles():
    ts = _ours()
    imported = _dtcg(dump_dtcg(ts))
    assert imported.owned is True
    assert export_tailwind(imported) == to_tailwind(ts, roles=True)


def test_a_stylesheet_the_engine_stamped_is_its_own_until_edited():
    text = stamp_digest(to_tailwind(_ours(), roles=True), css=True)
    assert text.startswith("/*\nux-skill-digest: ")
    assert _import(text).owned is True
    assert _import(text + "\n").owned is False
    assert _import(to_tailwind(_ours(), roles=True)).owned is False


def test_a_css_stamp_is_a_comment_ownership_reads(tmp_path):
    f = tmp_path / "theme.css"
    f.write_text(stamp_digest("@theme {\n  --color-ink: #111111;\n}\n", css=True),
                 encoding="utf-8")
    assert ownership(f) == "owned"
    f.write_text(f.read_text(encoding="utf-8").replace("#111111", "#222222"), encoding="utf-8")
    assert ownership(f) == "edited"


def _record(folder, **files):
    (folder / RECORD).parent.mkdir(parents=True, exist_ok=True)
    (folder / RECORD).write_text(record_text(folder, files), encoding="utf-8")


def test_a_stylesheet_the_record_lists_at_its_digest_is_the_engines(tmp_path):
    text = to_tailwind(_ours(), roles=True)
    f, imported = _source(tmp_path, text)
    assert imported.owned is False
    _record(tmp_path, **{"theme.css": text})
    assert read_tailwind(f).owned is True
    f.write_text(text + "\n", encoding="utf-8")
    assert read_tailwind(f).owned is False


def test_a_tokens_file_the_record_lists_at_another_digest_is_foreign(tmp_path):
    text = dump_dtcg(_ours())
    f = tmp_path / "tokens.json"
    f.write_text(text, encoding="utf-8")
    assert read_dtcg(f).owned is True
    _record(tmp_path, **{"tokens.json": text + " "})
    assert read_dtcg(f).owned is False
    _record(tmp_path, **{"tokens.json": text})
    assert read_dtcg(f).owned is True


def test_the_record_never_makes_a_foreign_tokens_file_the_engines_by_its_names(tmp_path):
    f = tmp_path / "tokens.json"
    f.write_text(json.dumps(FOREIGN_DTCG), encoding="utf-8")
    assert read_dtcg(f).owned is False


# ------------------------------------------------------------ opacity


def test_an_opacity_held_from_0_to_100_is_written_from_0_to_1_with_the_unit_noted():
    ts = TokenSet({})
    ts.add(Token("opacity.muted", "number", 60, extensions={"unit": "percent"}))
    ts.add(Token("opacity.plain", "number", 0.5))
    text = to_tailwind(ts, roles=False)
    assert text == ("/*\n * --opacity-muted is written from 0 to 1 (0.6); its source holds it "
                    "from 0 to 100 (60).\n */\n@theme {\n  --opacity-muted: 0.6;\n"
                    "  --opacity-plain: 0.5;\n}\n")
    css = to_css(ts)
    assert "  --opacity-muted: 0.6;\n" in css
    assert " * --opacity-muted is written from 0 to 1 (0.6); its source holds it from 0 to 100 " \
           "(60).\n" in css


def test_an_opacity_note_names_each_mode_value_it_converts():
    ts = TokenSet({"scheme": ("light", "dark")})
    ts.add(Token("opacity.muted", "number", 60, modes={"scheme:dark": 40},
                 extensions={"unit": "percent"}))
    css = to_css(ts)
    assert " * --opacity-muted is written from 0 to 1 (0.6; scheme:dark 0.4); its source holds " \
           "it from 0 to 100 (60; scheme:dark 40).\n" in css
    assert "  --opacity-muted: 0.4;\n" in css


def test_roles_must_be_said_so_a_built_system_is_never_exported_by_accident():
    with pytest.raises(TypeError):
        to_tailwind(_ours())


def test_an_opacity_in_percent_is_not_read_and_the_fix_says_0_to_1():
    imported = import_css(":root {\n  --opacity-muted: 60%;\n}\n",
                          Source(str(NOWHERE / "theme.css"), "css", "0" * 64, 10))
    [item] = imported.report.not_read
    assert item.name == "--opacity-muted"
    assert item.message == ("60% is an opacity in percent; write it as a number from 0 to 1 "
                            "(0.6) so it can be read")


# ------------------------------------------------------------ writing to a source

FOREIGN = """@import "tailwindcss";

@theme {
  --color-*: initial;
  --color-ink: #1b1d22;
  --color-paper: #fdfdfb;
  --color-surface: var(--color-paper);
  --radius-card: 0.75rem;
}

.dark {
  --color-surface: var(--color-ink);
}
"""


def _source(tmp_path, text=FOREIGN, name="theme.css"):
    f = tmp_path / name
    f.write_text(text, encoding="utf-8")
    return f, read_tailwind(f)


def _extended(imported, *tokens):
    ts = TokenSet(imported.tokens.axes)
    for t in imported.tokens.tokens():
        ts.add(Token(t.path, t.type, t.value, modes=dict(t.modes), layer=t.layer))
    for t in tokens:
        ts.add(t)
    return ts


def test_the_extension_is_named_after_the_source():
    assert extension_name("styles/theme.css") == "theme-ext.css"
    assert extension_name("app.tailwind.css") == "app.tailwind-ext.css"


def test_a_foreign_stylesheet_is_never_rewritten_its_additions_go_beside_it(tmp_path):
    f, imported = _source(tmp_path)
    before = f.read_bytes()
    ts = _extended(imported, Token("color-accent", "color", "#3366FF",
                                   modes={"scheme:dark": "#99B3FF"}),
                   Token("color-accent-ink", "color", "{color-paper}", layer="semantic"))
    outcome = write_tailwind(ts, imported)
    assert outcome["status"] == "written"
    assert f.read_bytes() == before
    ext = tmp_path / "theme-ext.css"
    assert outcome["file"] == str(ext)
    assert "theme-ext.css" in outcome["written"]
    text = ext.read_text(encoding="utf-8")
    assert is_ux_skill_file(ext)
    body = text[text.index("@theme {"):]
    assert body == ("@theme {\n  --color-accent: #3366FF;\n"
                    "  --color-accent-ink: var(--color-paper);\n}\n\n"
                    ".dark {\n  --color-accent: #99B3FF;\n}\n")
    assert "initial" not in text and "@import" not in text and "color-scheme" not in text
    assert outcome["load"] == (
        f"Load {ext} after {f}: it adds 2 tokens to that theme and changes nothing in it. "
        "Where the source is imported, import theme-ext.css on the line after it, for "
        'example @import "./theme-ext.css";')
    assert outcome["load"] in outcome["message"]
    assert "Load it after theme.css" in text
    # The source was backed up by the intake step, byte for byte.
    backup = tmp_path / outcome["backup"] / "source" / "theme.css"
    assert backup.read_bytes() == before


def test_the_extension_reads_back_in_the_sources_names(tmp_path):
    f, imported = _source(tmp_path)
    ts = _extended(imported, Token("color-accent", "color", "#3366FF",
                                   modes={"scheme:dark": "#99B3FF"}))
    write_tailwind(ts, imported)
    back = read_tailwind(tmp_path / "theme-ext.css")
    assert back.report.not_read == []
    assert [(t.path, t.value, t.modes) for t in back.tokens.tokens()] == [
        ("color-accent", "#3366FF", {"scheme:dark": "#99B3FF"})]


def test_an_extension_the_engine_wrote_is_replaced_with_force_alone(tmp_path):
    f, imported = _source(tmp_path)
    write_tailwind(_extended(imported, Token("color-accent", "color", "#3366FF")), imported)
    again = _extended(imported, Token("color-accent", "color", "#224EDD"))
    refused = write_tailwind(again, imported)
    assert refused["status"] == "refused" and "--force" in refused["message"]
    done = write_tailwind(again, imported, force=True)
    assert done["status"] == "written"
    assert "--color-accent: #224EDD;" in (tmp_path / "theme-ext.css").read_text()
    assert "theme-ext.css" in done["replaced"]


def test_an_extension_edited_by_hand_is_the_owners_and_force_alone_keeps_it(tmp_path):
    f, imported = _source(tmp_path)
    write_tailwind(_extended(imported, Token("color-accent", "color", "#3366FF")), imported)
    ext = tmp_path / "theme-ext.css"
    ext.write_text(ext.read_text(encoding="utf-8") + "/* mine */\n", encoding="utf-8")
    again = _extended(imported, Token("color-accent", "color", "#224EDD"))
    outcome = write_tailwind(again, imported, force=True)
    assert outcome["status"] == "refused"
    assert "--replace-client-files" in outcome["message"]
    assert "/* mine */" in ext.read_text(encoding="utf-8")


def test_an_extension_only_adds_a_changed_token_is_refused_by_name(tmp_path):
    f, imported = _source(tmp_path)
    ts = TokenSet(imported.tokens.axes)
    for t in imported.tokens.tokens():
        value = "#000000" if t.path == "color-ink" else t.value
        ts.add(Token(t.path, t.type, value, modes=dict(t.modes), layer=t.layer))
    with pytest.raises(InputError) as exc:
        write_tailwind(ts, imported)
    assert str(exc.value) == (
        f"--color-ink is #1B1D22 in {f} and #000000 in the system to write; an extension file "
        f"only adds tokens, so change --color-ink in {f} itself, or add a token under a new "
        "name")
    assert not (tmp_path / "theme-ext.css").exists()


UNREAD = FOREIGN.replace("  --radius-card: 0.75rem;\n",
                         "  --radius-card: 0.75rem;\n  --spacing-gutter: 1.5em;\n") + \
    ".btn {\n  --btn-pad: 12px;\n}\n"


@pytest.mark.parametrize("name,path", [("--spacing-gutter", "spacing-gutter"),
                                       ("--btn-pad", "btn-pad")])
def test_an_addition_named_like_an_entry_the_import_did_not_read_is_refused(tmp_path, name,
                                                                          path):
    f, imported = _source(tmp_path, UNREAD)
    assert name in [i.name for i in imported.report.not_read]
    assert not imported.tokens.has(path)
    ts = _extended(imported, Token(path, "dimension", {"value": 24, "unit": "px"}))
    with pytest.raises(InputError) as exc:
        write_tailwind(ts, imported)
    assert str(exc.value).startswith(f"{name} is declared in {f}, where the import did not "
                                     "read it (")
    assert str(exc.value).endswith(
        f"); an extension file loaded after {f} would replace its value, so rename the "
        f"addition, or map it to {name} and write {name} in {f} in a form the import reads")
    assert not (tmp_path / "theme-ext.css").exists()


def test_an_addition_beside_entries_the_import_did_not_read_changes_none_of_them(tmp_path):
    f, imported = _source(tmp_path, UNREAD)
    outcome = write_tailwind(_extended(imported, Token("spacing-gutter-wide", "dimension",
                                                       {"value": 24, "unit": "px"})), imported)
    assert outcome["status"] == "written"
    assert "changes nothing in it" in outcome["load"]
    text = (tmp_path / "theme-ext.css").read_text(encoding="utf-8")
    assert "--spacing-gutter:" not in text and "--btn-pad" not in text


def test_nothing_to_add_writes_nothing(tmp_path):
    f, imported = _source(tmp_path)
    outcome = write_tailwind(_extended(imported), imported)
    assert outcome["status"] == "unchanged"
    assert outcome["message"] == (f"{f} already holds every token of the system to write, so "
                                  "no extension file was written.")
    assert not (tmp_path / "theme-ext.css").exists()
    assert tailwind_extension(imported, _extended(imported)) == ""


def test_the_engines_own_stylesheet_is_rewritten_in_place_through_intake(tmp_path):
    first = _import(to_tailwind(_ours(), roles=True))
    f = tmp_path / "theme.css"
    f.write_text(stamp_digest(export_tailwind(first), css=True), encoding="utf-8")
    imported = read_tailwind(f)
    assert imported.owned is True
    ts = _extended(imported, Token("color-extra", "color", "#123456"))
    refused = write_tailwind(ts, imported)
    assert refused["status"] == "refused"
    outcome = write_tailwind(ts, imported, force=True)
    assert outcome["status"] == "written"
    assert outcome["file"] == str(f)
    assert outcome["load"] == ""
    assert not (tmp_path / "theme-ext.css").exists()
    assert is_ux_skill_file(f)
    text = f.read_text(encoding="utf-8")
    assert "  --color-extra: #123456;\n" in text
    assert list(outcome["replaced"]) == ["theme.css"]
    assert (tmp_path / INTAKE_DIR).is_dir()


def test_an_engine_stylesheet_edited_by_hand_is_foreign_and_gets_an_extension(tmp_path):
    text = stamp_digest("@theme {\n  --color-ink: #111111;\n}\n", css=True)
    f, imported = _source(tmp_path, text.replace("#111111", "#222222"))
    assert imported.owned is False
    outcome = write_tailwind(_extended(imported, Token("color-accent", "color", "#3366FF")),
                             imported)
    assert outcome["file"] == str(tmp_path / "theme-ext.css")


def test_a_source_that_is_not_a_tailwind_stylesheet_is_refused_by_name(tmp_path):
    f = tmp_path / "tokens.json"
    f.write_text(json.dumps(FOREIGN_DTCG), encoding="utf-8")
    imported = import_dtcg(f.read_text(), Source(str(f), "dtcg", "0" * 64, 1))
    with pytest.raises(InputError) as exc:
        write_tailwind(imported.tokens, imported)
    assert str(exc.value) == (
        f"{f} is a dtcg source, not a Tailwind stylesheet, so no Tailwind file is written "
        "beside it; pass the Tailwind stylesheet (.css) the system lives in, or export the "
        "system to a new folder")


def test_the_package_keeps_its_names_and_adds_the_exporter():
    import engine.io as io
    for name in ("read_any", "write_css", "merge", "write_with_intake", "import_css",
                 "RESETS", "tailwind_name", "to_tailwind", "export_tailwind",
                 "tailwind_extension", "write_tailwind", "extension_name"):
        assert name in io.__all__ and hasattr(io, name)
