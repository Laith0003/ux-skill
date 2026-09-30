"""extend: add a foundation, roles or contracts to an imported system
without changing a token it has. The result is checked; what blocks it is
named, and a blocked result writes only its report.

A system the engine did not write is never rewritten: the additions go in
an extension file beside it, in its own format and names, stamped and
recorded as the engine's, and a later extension keeps what an earlier one
added. Only the engine's own system, known from the record of the files
it wrote and never from token names, is rewritten in place, through the
intake step."""
import dataclasses
import hashlib
import json
import sys
from pathlib import Path

import pytest

from engine.contracts.library import SEED_DIR
from engine.existing import is_ux_skill_text, stamp_digest
from engine.existing.record import read_record
from engine.foundations.build import build_system
from engine.foundations.color_math import contrast, luminance
from engine.foundations.emit import InputError, brief_audience, unread_lines
from engine.foundations.export import dump_dtcg, from_dtcg
from engine.io.adapter import AxisMap, Mapping, RoleMap, parse_mapping, propose
from engine.io.css_in import import_css, read_css
from engine.io.dtcg_in import import_dtcg, read_dtcg
from engine.io.extend import extend, write_extended
from engine.io.figma_in import import_figma, read_figma
from engine.io.figma_out import READ_SCRIPT
from engine.io.intake import write_with_intake
from engine.io.markdown_in import import_markdown
from engine.io.report import Source
from engine.io.tailwind_in import import_tailwind_css, import_tailwind_json, read_tailwind
from engine.io.tailwind_out import to_tailwind
from engine.synthesizer.axes import AxisValues
from tests.io.test_figma_out import NODE, _run

NEUTRAL = AxisValues(*[0.5] * 7)

# A folder no record can sit in, so a source read from text is never
# taken as the engine's because of a record where the tests run.
NOWHERE = Path(__file__).resolve().parent / "no-such-folder"


@pytest.fixture(autouse=True)
def _nowhere():
    assert not NOWHERE.exists()


FOREIGN = """:root {
  --ink: #1b1d22;
  --paper: #fdfdfb;
  --brand-700: #1f3fa3;
  --text-body: var(--ink);
  --page: var(--paper);
}
.dark {
  --text-body: var(--paper);
  --page: var(--ink);
}
"""
MAPPING = Mapping(roles={"color.text.default": RoleMap("text-body", "owner"),
                         "color.surface.page": RoleMap("page", "owner")},
                  axes={"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"},
                                          "owner")})


def _source(name, fmt, text):
    return Source(str(NOWHERE / name), fmt, "0" * 64, len(text))


def _ours(*names):
    ts = build_system(NEUTRAL, "#3366FF", foundations=names).tokens
    text = dump_dtcg(ts)
    return import_dtcg(text, _source("tokens.json", "dtcg", text))


def _foreign(text=FOREIGN):
    return import_css(text, _source("theme.css", "css", text))


def _rows(ts):
    return [(t.path, t.type, t.value, t.modes, t.layer) for t in ts.tokens()]


def _same(before, after):
    return _rows(before) == _rows(after)[:len(before.tokens())]


# ---------------------------------------------------------------- the engine's own


def test_adding_a_foundation_to_the_engines_own_system_rewrites_it_in_place():
    imported = _ours("color", "border")
    assert imported.owned
    result = extend(imported, propose(imported.tokens), foundations=("motion",))
    assert result.problems == []
    assert _same(imported.tokens, result.tokens)
    assert result.added[0] == "motion.duration.0" and "motion.reveal.duration" in result.added
    assert result.check.passed, result.check.report.summary()
    assert list(result.files) == ["tokens.json", "mapping.json", "extend-report.md"]
    assert result.beside == ["tokens.json"] and result.load == ""
    back = from_dtcg(json.loads(result.files["tokens.json"]))
    assert [t.path for t in back.tokens()] == [t.path for t in result.tokens.tokens()]
    assert "motion.reveal.duration" in parse_mapping(result.files["mapping.json"], "m").roles
    report = result.files["extend-report.md"]
    assert "Extended tokens.json (dtcg), the engine's own system, in place." in report


def test_a_foundation_that_needs_another_brings_only_what_it_points_at():
    imported = _ours("color")
    result = extend(imported, propose(imported.tokens), foundations=("layout",))
    assert result.problems == []
    added_space = [p for p in result.added if p.startswith("space.")]
    assert added_space and all(p.split(".")[1].isdigit() for p in added_space)
    assert any(d.startswith("layout aliases steps of the space scale") for d in result.decisions)


def test_the_engines_own_system_is_rewritten_through_the_intake_step(tmp_path):
    ts = build_system(NEUTRAL, "#3366FF", foundations=("color", "border")).tokens
    seed = tmp_path / "seed.json"
    seed.write_text("{}", encoding="utf-8")
    seeded = Source(str(seed), "dtcg", hashlib.sha256(b"{}").hexdigest(), 2)
    outcome = write_with_intake(tmp_path, {"tokens.json": dump_dtcg(ts)}, seeded)
    assert outcome["status"] == "written"
    imported = read_dtcg(tmp_path / "tokens.json")
    assert imported.owned
    result = extend(imported, propose(imported.tokens), foundations=("motion",))
    refused = write_extended(result, imported)
    assert refused["status"] == "refused" and refused["conflicts"] == ["tokens.json"]
    done = write_extended(result, imported, force=True)
    assert done["status"] == "written", done["message"]
    assert (tmp_path / "tokens.json").read_text(encoding="utf-8") == result.files["tokens.json"]
    backup = tmp_path / done["replaced"]["tokens.json"]
    assert backup.read_text(encoding="utf-8") == dump_dtcg(ts)


def test_the_engines_own_tailwind_theme_is_rewritten_in_place_and_stays_its_own():
    ts = build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens
    text = stamp_digest(to_tailwind(ts, roles=True), css=True)
    imported = import_tailwind_css(text, _source("app.css", "tailwind", text))
    assert imported.owned
    result = extend(imported, propose(imported.tokens), foundations=("radius",))
    assert result.problems == [] and result.beside == ["app.css"]
    again = import_tailwind_css(result.files["app.css"],
                                _source("app.css", "tailwind", result.files["app.css"]))
    assert again.owned and _same(imported.tokens, again.tokens)
    assert again.tokens.get("radius-card").value == "{radius-3}"


def test_the_engines_own_file_is_extended_beside_it_when_the_import_left_an_entry_out():
    doc = json.loads(dump_dtcg(build_system(NEUTRAL, "#3366FF", foundations=("color",)).tokens))
    doc["odd"] = {"$type": "dimension", "$value": "1.5em"}
    text = json.dumps(doc)
    imported = import_dtcg(text, _source("tokens.json", "dtcg", text))
    assert imported.owned and imported.report.not_read
    result = extend(imported, propose(imported.tokens), foundations=("radius",))
    assert result.problems == [] and result.beside == ["tokens-ext.json"]
    assert ("tokens.json is the engine's own, but the import did not read all of it, so it is "
            "not rewritten; the additions are in tokens-ext.json.") in result.decisions


# ---------------------------------------------------------------- a foreign stylesheet


def test_a_foreign_stylesheet_is_never_rewritten_its_additions_go_beside_it():
    imported = _foreign()
    result = extend(imported, MAPPING, modes=("density",), foundations=("space",))
    assert result.problems == []
    assert list(result.tokens.axes) == ["scheme", "density"]
    assert list(result.files) == ["theme-ext.css", "mapping.json", "extend-report.md"]
    assert result.beside == ["theme-ext.css"]
    ext = result.files["theme-ext.css"]
    assert is_ux_skill_text(ext)
    assert "--ink" not in ext and "--page" not in ext
    assert ':root[data-density="compact"] {\n  --space-control-gap: var(--space-2);' in ext
    assert "color-scheme" not in ext
    assert result.load.startswith("Load theme-ext.css after theme.css")
    both = import_css(FOREIGN + "\n" + ext, _source("theme.css", "css", FOREIGN))
    assert _rows(both.tokens) == _rows(result.tokens)
    report = result.files["extend-report.md"]
    assert "theme.css is not rewritten" in report
    assert result.load in report


def test_added_tokens_take_the_sources_own_naming():
    result = extend(_foreign(), MAPPING, modes=("density",), foundations=("space",))
    assert "space-control-gap" in result.added and "space.control.gap" not in result.added
    gap = result.tokens.get("space-control-gap")
    assert (gap.value, gap.modes) == ("{space-3}", {"density:compact": "{space-2}"})
    assert result.mapping.roles["space.control.gap"] == RoleMap("space-control-gap", "name")


def test_an_entry_the_import_did_not_read_is_counted_and_kept():
    text = FOREIGN.replace("  --page: var(--paper);\n}",
                           "  --page: var(--paper);\n  --gap-odd: 1.5em;\n}")
    result = extend(_foreign(text), MAPPING, foundations=("radius",))
    assert result.problems == []
    assert "theme.css" not in result.files
    report = result.files["extend-report.md"]
    assert ("theme.css is not rewritten, so the 1 entry the import did not read stays in it "
            "as it is") in report


def test_an_addition_named_like_an_entry_the_import_did_not_read_blocks():
    text = FOREIGN.replace("  --page: var(--paper);\n}",
                           "  --page: var(--paper);\n  --space-4: 1.5em;\n}")
    result = extend(_foreign(text), MAPPING, foundations=("space",))
    assert list(result.files) == ["extend-report.md"]
    assert result.problems[0] == (
        "--space-4 is declared in theme.css, where the import did not read it (1.5em is "
        "relative to the parent's font size, so it has no fixed value; write it in px or "
        "rem); the extension file loads after theme.css and would replace its value, so "
        "write --space-4 in theme.css in a form the import reads, or leave space out")


def test_a_property_the_stylesheet_has_under_another_path_is_compared_as_written():
    text = FOREIGN.replace("  --page: var(--paper);\n}",
                           "  --page: var(--paper);\n  --space-4: 18px;\n}")
    result = extend(_foreign(text), MAPPING, foundations=("space",))
    assert result.problems[0] == (
        "--space-4 is already in theme.css with another value (18px, the space foundation "
        "would write 16px); extend never changes a token the system has, so rename --space-4 "
        "in theme.css or leave space out")


def test_a_dark_first_stylesheet_gets_an_extension_in_its_own_forms():
    text = FOREIGN.replace(".dark {", ':root:not([data-theme="light"]) {')
    imported = _foreign(text)
    assert imported.scheme == "dark"
    result = extend(imported, MAPPING, foundations=("radius",))
    assert result.problems == []
    ext = result.files["theme-ext.css"]
    assert "prefers-color-scheme" not in ext and "color-scheme" not in ext


def test_added_type_is_built_for_the_briefs_audience_and_brings_its_font_files():
    imported = _foreign()
    brief = {"age": "older-adults", "tone": ["calm"], "audience": "many over 60"}
    result = extend(imported, MAPPING, foundations=("type",),
                    audience=brief_audience(brief), unread=unread_lines(brief))
    assert result.problems == []
    assert result.tokens.resolve("type-text-body")["fontSize"] == {"value": 1.125,
                                                                   "unit": "rem"}
    assert list(result.files) == ["theme-ext.css", "fonts.css", "fonts-self-host.css",
                                  "mapping.json", "extend-report.md"]
    assert result.beside == ["theme-ext.css", "fonts.css", "fonts-self-host.css"]
    face = result.tokens.resolve("type-face-text")[0]
    assert f'font-family: "{face} Fallback";' in result.files["fonts.css"]
    assert f'font-family: "{face}";' in result.files["fonts-self-host.css"]
    report = result.files["extend-report.md"]
    assert "- Body text is 18px, targets are at least " in report
    assert "the brief says the readers are older adults" in report
    assert '## Not read from the brief\n\n- audience "many over 60" is plain text' in report


def test_a_role_the_system_already_plays_is_not_added_again():
    result = extend(_foreign(), MAPPING, foundations=("color",))
    assert not any(p in result.added for p in ("color-surface-page", "color-text-default"))
    assert ("color.surface.page and color.text.default are mapped in mapping.json to your page "
            "and text-body, so the foundation did not add its own tokens for them; its tokens "
            "that point at those roles point at yours.") in result.decisions
    assert result.mapping.roles["color.surface.page"] == RoleMap("page", "owner")


def test_imagery_adds_no_art_and_says_how_to_get_it():
    result = extend(_foreign(), MAPPING, foundations=("imagery",))
    assert not any(name.startswith("art/") for name in result.files)
    assert any(d.startswith("No art was written") for d in result.decisions)


# ---------------------------------------------------------------- roles


def test_an_added_role_points_at_the_systems_own_token():
    imported = _foreign()
    light = Mapping(roles=dict(MAPPING.roles), axes={})
    result = extend(imported, light, roles={"color.focus.ring": "brand-700"})
    assert result.problems == []
    token = result.tokens.get("color-focus-ring")
    assert (token.value, token.layer) == ("{brand-700}", "semantic")
    assert result.mapping.roles["color.focus.ring"] == RoleMap("color-focus-ring", "owner")
    assert "--color-focus-ring: var(--brand-700);" in result.files["theme-ext.css"]


def test_an_added_role_that_fails_the_gate_blocks_with_the_systems_names():
    result = extend(_foreign(), MAPPING, roles={"color.focus.ring": "brand-700"})
    assert result.problems == [
        "color.focus.ring on color.surface.page (your page) (scheme:dark) is 1.84:1; "
        "WCAG 1.4.11 needs 3:1. Point --add-role color.focus.ring at another of your tokens, "
        "or leave it out."]
    assert list(result.files) == ["extend-report.md"]
    report = result.files["extend-report.md"]
    assert "## What blocks it" in report
    assert "Nothing was written but this report" in report


def test_a_path_the_system_already_has_blocks_and_only_the_report_is_written():
    doc = {"space": {"4": {"$type": "dimension", "$value": {"value": 18, "unit": "px"}}}}
    text = json.dumps(doc)
    imported = import_dtcg(text, _source("tokens.json", "dtcg", text))
    result = extend(imported, Mapping(), foundations=("space",))
    assert result.problems == [
        "space.4 is already in tokens.json with another value (18px, the space foundation "
        "would write 16px); extend never changes a token the system has, so rename space.4 in "
        "tokens.json or leave space out"]
    assert list(result.files) == ["extend-report.md"]
    assert "## What blocks it" in result.files["extend-report.md"]


# ---------------------------------------------------------------- the check


def test_the_check_says_how_many_roles_were_mapped_per_foundation():
    result = extend(_foreign(), MAPPING, foundations=("radius",))
    report = result.files["extend-report.md"]
    check = report.split("## Check\n\n", 1)[1]
    assert check.startswith("Mapped ")
    assert "| Foundation | Mapped | Left out by you | Not mapped |" in check
    assert "| radius | " in check


def test_nothing_mapped_is_not_measured():
    imported = _foreign()
    result = extend(imported, Mapping(), contracts=())
    report = result.files["extend-report.md"]
    assert "not measured" in report.split("## Check\n\n", 1)[1].split("\n## ", 1)[0]



# A light only system whose text passes AA (5.23:1) but not AAA, and one
# whose text fails AA (2.76:1).
def _light(ink):
    return FOREIGN.replace("--ink: #1b1d22", f"--ink: {ink}").replace(
        ".dark {\n  --text-body: var(--paper);\n  --page: var(--ink);\n}\n", "")


LIGHT = Mapping(roles=dict(MAPPING.roles), axes={})


@pytest.mark.parametrize("add", ["border", "type"])
def test_a_mode_the_additions_bring_never_blames_the_systems_own_tokens(add):
    result = extend(_foreign(_light("#6b6b6b")), LIGHT, modes=("contrast",), foundations=(add,))
    assert result.problems == [] and result.existing == []
    assert result.unmeasured == [
        "color.text.default (your text-body) on color.surface.page (your page) "
        "(contrast:high) is 5.23:1; WCAG 1.4.6 needs 7:1. Change the value of one of them in "
        "your system, or map the role to a token with more contrast."]
    report = result.files["extend-report.md"]
    assert "Your system was never measured in contrast high, a mode the additions bring." \
        in report


@pytest.mark.parametrize("add", ["radius", "border", "type"])
def test_a_finding_the_system_had_stays_apart_whatever_axis_the_additions_bring(add):
    result = extend(_foreign(_light("#9a9a9a")), LIGHT, foundations=(add,))
    assert result.problems == []
    assert len(result.existing) == 1 and "is 2.76:1; WCAG 1.4.3 needs 4.5:1" in \
        result.existing[0]


def test_the_gate_line_says_when_every_failure_was_there_before():
    result = extend(_foreign(_light("#9a9a9a")), LIGHT, foundations=("border",))
    assert result.problems == []
    assert ("Every failing check counted above is one listed under Already in the system; the "
            "additions cause none.") in result.files["extend-report.md"]


def test_a_role_the_owner_kept_out_gets_no_token_from_a_foundation():
    mapping = Mapping(roles={**MAPPING.roles, "color.focus.ring": RoleMap(None, "owner")},
                      axes=dict(MAPPING.axes))
    result = extend(_foreign(), mapping, foundations=("color",))
    assert "color-focus-ring" not in result.added
    assert any(d.startswith('color.focus.ring is kept out in mapping.json with {"token": null, '
                            '"by": "owner"}, so the foundation added no token for it')
               for d in result.decisions)
    assert not any("color.focus.ring " in p for p in result.problems)


def test_an_added_role_that_fails_against_the_owners_fill_names_a_fix_the_owner_can_take():
    # No text reaches 7:1 on the owner's mid-blue fill, so the text the
    # color foundation adds on it cannot pass in high contrast.
    mapping = Mapping(roles={r: m for r, m in OFF_WHITE_MAPPING.roles.items()
                             if r != "color.text.on-action"}, axes={})
    result = extend(_foreign(OFF_WHITE), mapping, modes=("contrast",), foundations=("color",))
    assert result.problems[0] == (
        "color.text.on-action on color.action.primary (your action) (contrast:high) is 4.76:1; "
        "WCAG 1.4.6 needs 7:1. Map color.text.on-action in mapping.json to one of your tokens, "
        "which the color foundation then uses instead of adding its own, or leave color out.")
    assert not any("step further" in p or "Move " in p for p in result.problems)


# ---------------------------------------------------------------- color fits the owner's page


# A light-only system with an off-white page and a mid-blue brand fill.
OFF_WHITE = """:root {
  --ink: #1b1d22;
  --paper: #f7f5f0;
  --blue: #3b6fd4;
  --white: #ffffff;
  --text-body: var(--ink);
  --page: var(--paper);
  --action: var(--blue);
  --on-action: var(--white);
}
"""
OFF_WHITE_MAPPING = Mapping(roles={"color.text.default": RoleMap("text-body", "owner"),
                                   "color.surface.page": RoleMap("page", "owner"),
                                   "color.action.primary": RoleMap("action", "owner"),
                                   "color.text.on-action": RoleMap("on-action", "owner")},
                            axes={})
SURFACES = ("color-surface-tint", "color-surface-band", "color-surface-stripe",
            "color-focus-ring")


def _ratio(result, a, b, mode=""):
    return contrast(result.tokens.resolve(a, mode), result.tokens.resolve(b, mode))


def test_added_color_on_a_light_only_system_passes_against_its_own_page():
    result = extend(_foreign(OFF_WHITE), OFF_WHITE_MAPPING, modes=("contrast",),
                    foundations=("color",))
    assert result.problems == [] and result.existing == [] and result.inherited == []
    assert all(p in result.added for p in SURFACES)
    # The tint stands our floor off the owner's page and no further than it
    # must; the band stands beyond it; the stripe is the owner's page.
    assert 1.1 <= _ratio(result, "color-surface-tint", "page") < 1.12
    assert _ratio(result, "color-surface-band", "page") >= 1.2
    assert result.tokens.get("color-surface-stripe").value == "{page}"
    assert "--color-surface-stripe: var(--page);" in result.files["theme-ext.css"]
    for mode in ("", "contrast:high"):
        need = 4.5 if mode else 3.0
        assert _ratio(result, "color-focus-ring", "page", mode) >= need
        assert _ratio(result, "text-body", "color-surface-band", mode) >= 4.5
    # The owner's own fill and text are never added again.
    assert not any(p in result.added for p in ("color-action-primary", "color-surface-page",
                                               "color-text-default", "color-text-on-action"))
    assert ("color was generated from every axis at 0.5; its brand color is #3B6FD4, read from "
            "your action (color.action.primary).") in result.decisions


def test_a_light_only_system_gets_no_dark_additions_and_is_told_so():
    result = extend(_foreign(OFF_WHITE), OFF_WHITE_MAPPING, modes=("contrast",),
                    foundations=("color",))
    ext = result.files["theme-ext.css"]
    assert "scheme" not in result.tokens.axes
    assert "dark" not in ext and "prefers-color-scheme" not in ext
    assert ("Your system has one scheme, light (mapping.json reads no scheme from it), so the "
            "additions hold light values only and add no dark ones. To add them, map scheme in "
            "mapping.json to the switch your dark scheme uses.") in result.decisions
    # The owner's fill can carry white text at 4.5:1 but not 7:1: that is
    # its own finding in a mode the additions bring, not the additions'.
    assert result.unmeasured == [
        "color.text.on-action (your on-action) on color.action.primary (your action) "
        "(contrast:high) is 4.76:1; WCAG 1.4.6 needs 7:1. Change the value of one of them in "
        "your system, or map the role to a token with more contrast."]


def test_a_dark_capable_system_gets_dark_additions_on_its_own_dark_page():
    result = extend(_foreign(), MAPPING, foundations=("color",))
    assert result.problems == []
    dark = "scheme:dark"
    assert result.tokens.resolve("page", dark).lower() == "#1b1d22"
    assert 1.1 <= _ratio(result, "color-surface-tint", "page", dark) < 1.12
    assert _ratio(result, "color-surface-band", "page", dark) >= 1.2
    assert _ratio(result, "color-focus-ring", "page", dark) >= 3.0
    # The stripe points at the owner's page, which switches with the scheme.
    stripe = result.tokens.get("color-surface-stripe")
    assert stripe.value == "{page}" and "scheme:dark" not in stripe.modes
    assert result.tokens.resolve("color-surface-stripe", dark).lower() == "#1b1d22"
    ext = result.files["theme-ext.css"]
    assert ".dark {" in ext and "--color-surface-tint: var(--color-brand-tint-dark);" in ext


def test_a_system_whose_text_fails_keeps_its_finding_and_the_additions_still_pass():
    result = extend(_foreign(_light("#9a9a9a")), LIGHT, foundations=("color",))
    assert result.problems == []
    assert len(result.existing) == 1 and "on color.surface.page (your page)" in \
        result.existing[0] and "is 2.76:1; WCAG 1.4.3 needs 4.5:1" in result.existing[0]
    assert 1.1 <= _ratio(result, "color-surface-tint", "page") < 1.12
    assert _ratio(result, "color-focus-ring", "page") >= 3.0
    assert result.inherited and all(
        m.startswith("color.text.default (your text-body) on ") and m.endswith(
            "color.text.default already fails this on your page, at 2.76:1 there, so the "
            "finding starts with your text-body; change text-body in your system.")
        for m in result.inherited)
    report = result.files["extend-report.md"]
    assert "These pair a color of yours that already fails on your own page" in report
    assert "## What blocks it" not in report
    # Text on art does not take the failing text: it reads over its veil.
    assert result.tokens.resolve("color-text-on-media") != "#9a9a9a"



# ---------------------------------------------------------------- contracts


def test_a_contract_is_bound_through_the_mapping_and_copied():
    imported = _ours("color", "space", "radius", "border", "elevation", "motion", "layout",
                     "type")
    card = SEED_DIR / "card.yaml"
    result = extend(imported, propose(imported.tokens), contracts=(card,))
    assert result.problems == []
    assert result.files["contracts/card.yaml"] == card.read_text(encoding="utf-8")


def test_a_contract_that_binds_a_role_the_system_lacks_is_named():
    card = SEED_DIR / "card.yaml"
    result = extend(_foreign(), MAPPING, contracts=(card,))
    assert result.problems and result.problems[0].startswith("card: ")
    assert "which the token set does not define" in result.problems[0]


# ---------------------------------------------------------------- other formats


def test_a_foreign_tokens_file_gets_an_extension_whose_tokens_alias_its_own():
    doc = {"brand": {"700": {"$type": "color", "$value": "#1f3fa3"}},
           "ink": {"$type": "color", "$value": "#1b1d22"},
           "paper": {"$type": "color", "$value": "#fdfdfb"}}
    text = json.dumps(doc)
    imported = import_dtcg(text, _source("tokens.json", "dtcg", text))
    assert not imported.owned
    mapping = Mapping(roles={"color.text.default": RoleMap("ink"),
                             "color.surface.page": RoleMap("paper")})
    result = extend(imported, mapping, roles={"color.focus.ring": "brand.700"})
    assert result.problems == []
    assert list(result.files) == ["tokens-ext.json", "mapping.json", "extend-report.md"]
    ext = json.loads(result.files["tokens-ext.json"])
    assert list(ext) == ["$extensions", "color"]
    assert ext["color"]["focus"]["ring"]["$value"] == "{brand.700}"
    # The load line names exactly the file the extension points at, and what in it.
    assert ("list tokens-ext.json after it among the token files your tools read, since its "
            "tokens point by name at tokens in tokens.json (brand.700)") in result.load


def test_a_paired_tokens_file_and_its_dark_sibling_are_never_rewritten(tmp_path):
    light = {"ink": {"$type": "color", "$value": "#1b1d22"},
             "paper": {"$type": "color", "$value": "#fdfdfb"},
             "brand": {"$type": "color", "$value": "#1f3fa3"}}
    dark = {"ink": {"$type": "color", "$value": "#fdfdfb"},
            "paper": {"$type": "color", "$value": "#1b1d22"},
            "brand": {"$type": "color", "$value": "#8fa6f0"}}
    (tmp_path / "tokens.json").write_text(json.dumps(light), encoding="utf-8")
    (tmp_path / "tokens.dark.json").write_text(json.dumps(dark), encoding="utf-8")
    imported = read_dtcg(tmp_path / "tokens.json")
    assert imported.report.also_read
    mapping = Mapping(roles={"color.text.default": RoleMap("ink"),
                             "color.surface.page": RoleMap("paper")},
                      axes={"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"})})
    result = extend(imported, mapping, foundations=("radius",))
    assert result.problems == []
    assert "tokens.json" not in result.files and "tokens.dark.json" not in result.files
    assert result.beside == ["tokens-ext.json"]
    before = {p.name: p.read_bytes() for p in tmp_path.iterdir()}
    outcome = write_extended(result, imported)
    assert outcome["status"] == "written", outcome["message"]
    for name, data in before.items():
        assert (tmp_path / name).read_bytes() == data


def test_a_tailwind_theme_gets_an_extension_with_its_own_theme_block():
    text = ('@import "tailwindcss";\n\n@theme {\n  --color-ink: #1b1d22;\n'
            '  --color-paper: #fdfdfb;\n}\n')
    imported = import_tailwind_css(text, _source("app.css", "tailwind", text))
    mapping = Mapping(roles={"color.text.default": RoleMap("color-ink"),
                             "color.surface.page": RoleMap("color-paper")})
    result = extend(imported, mapping, foundations=("radius",))
    assert result.problems == []
    ext = result.files["app-ext.css"]
    assert "@theme {" in ext and "@import" not in ext and "--color-ink" not in ext
    assert "--radius-card: var(--radius-" in ext


def test_markdown_and_a_tailwind_3_theme_get_an_extension_tokens_file():
    md = "| Token | Value |\n|---|---|\n| `ink` | #1b1d22 |\n| `paper` | #fdfdfb |\n"
    imported = import_markdown([("colors.md", md)], _source("colors.md", "markdown", md))
    mapping = Mapping(roles={"color.text.default": RoleMap("ink"),
                             "color.surface.page": RoleMap("paper")})
    result = extend(imported, mapping, roles={"color.focus.ring": "ink"})
    assert result.problems == []
    ext = json.loads(result.files["tokens-ext.json"])
    assert ext["color"]["focus"]["ring"]["$value"] == {
        "colorSpace": "srgb", "components": [0.105882, 0.113725, 0.133333], "hex": "#1B1D22"}
    theme = json.dumps({"colors": {"ink": "#1b1d22", "paper": "#fdfdfb"}})
    imported = import_tailwind_json(theme, _source("theme.json", "tailwind-json", theme))
    mapping = Mapping(roles={"color.text.default": RoleMap("colors.ink"),
                             "color.surface.page": RoleMap("colors.paper")})
    result = extend(imported, mapping, foundations=("radius",))
    assert result.problems == [] and "tokens-ext.json" in result.files


def _figma_export():
    return {"variableCollections": {"c1": {
        "id": "c1", "name": "Colors", "defaultModeId": "m1",
        "modes": [{"modeId": "m1", "name": "Light"}, {"modeId": "m2", "name": "Dark"}],
        "variableIds": ["v1", "v2"]}},
        "variables": {
            "v1": {"id": "v1", "name": "ink", "variableCollectionId": "c1",
                   "resolvedType": "COLOR", "scopes": ["ALL_SCOPES"],
                   "valuesByMode": {"m1": {"r": 0.1, "g": 0.1, "b": 0.12, "a": 1},
                                    "m2": {"r": 0.99, "g": 0.99, "b": 0.98, "a": 1}}},
            "v2": {"id": "v2", "name": "paper", "variableCollectionId": "c1",
                   "resolvedType": "COLOR", "scopes": ["ALL_SCOPES"],
                   "valuesByMode": {"m1": {"r": 0.99, "g": 0.99, "b": 0.98, "a": 1},
                                    "m2": {"r": 0.1, "g": 0.1, "b": 0.12, "a": 1}}}}}


FIGMA_MAPPING = Mapping(roles={"color.text.default": RoleMap("ink"),
                               "color.surface.page": RoleMap("paper")},
                        axes={"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"})})


# A light-only system whose text passes AA by a little (4.63:1) and whose
# muted text sits under 5:1 (4.98:1), on an off-white page.
NEAR_AA = """:root {
  --paper: #faf7f0;
  --grey: #707070;
  --soft-grey: #6b6b6b;
  --bg: var(--paper);
  --fg: var(--grey);
  --fg-muted: var(--soft-grey);
}
"""
NEAR_AA_MAPPING = Mapping(roles={"color.surface.page": RoleMap("bg", "owner"),
                                 "color.text.default": RoleMap("fg", "owner"),
                                 "color.text.muted": RoleMap("fg-muted", "owner")}, axes={})
TEXT_SURFACES = ("color-surface-tint", "color-surface-band", "color-surface-sunken",
                 "color-surface-selected") + tuple(
    f"color-status-{s}-soft" for s in ("danger", "warning", "success", "info"))


def test_owner_text_that_passes_by_a_little_keeps_its_minimum_on_every_added_surface():
    result = extend(_foreign(NEAR_AA), NEAR_AA_MAPPING, modes=("contrast",), foundations=("color",))
    assert result.problems == []
    for surface in TEXT_SURFACES:
        assert surface in result.added
        for mode in ("", "contrast:high"):
            for text in ("fg", "fg-muted"):
                assert _ratio(result, text, surface, mode) >= 4.5, (surface, mode, text)
            # Nearer the page than the engine's own step, never past it.
            assert result.tokens.resolve(surface, mode) != result.tokens.resolve("bg")
    line = next(d for d in result.decisions if d.startswith("Your text wins over our own "
                                                              "distance floors: "))
    assert "color.surface.band stands " in line and "under our 1.2:1 floor" in line
    assert "color.text.default (your fg)" in line and "color.surface.page (your bg)" in line
    # The band still sits beyond the tint.
    assert _ratio(result, "color-surface-band", "bg") > _ratio(result, "color-surface-tint", "bg")


@pytest.mark.parametrize("page", ["#ececec", "#e3e8ef", "#f0e6d2"])
def test_the_sunken_surface_recedes_from_the_owners_page(page):
    text = OFF_WHITE.replace("--paper: #f7f5f0", f"--paper: {page}")
    result = extend(_foreign(text), OFF_WHITE_MAPPING, foundations=("color",))
    assert result.problems == []
    sunken = result.tokens.resolve("color-surface-sunken")
    assert luminance(sunken) < luminance(page)
    assert 1.08 <= contrast(sunken, page) <= 1.15


DARK_ONLY = """:root {
  --fg: #f2f2f2;
  --bg: #111317;
}
"""
DARK_ONLY_MAPPING = Mapping(roles={"color.text.default": RoleMap("fg", "owner"),
                                   "color.surface.page": RoleMap("bg", "owner")}, axes={})


def test_a_dark_only_system_adding_elevation_gets_dark_shadows_and_is_told_dark():
    result = extend(_foreign(DARK_ONLY), DARK_ONLY_MAPPING, foundations=("elevation",))
    assert result.problems == []
    dark = build_system(NEUTRAL, "#3366FF", foundations=("elevation",)).tokens
    card = result.tokens.get("elevation-card")
    assert not card.modes
    assert result.tokens.resolve("elevation-card") == dark.resolve("elevation.card", "scheme:dark")
    assert any(d.startswith("Your system has one scheme, dark ") for d in result.decisions)
    ext = result.files["theme-ext.css"]
    assert "shadow-light" not in ext


def test_a_light_only_system_writes_no_dark_shadow_steps():
    result = extend(_foreign(OFF_WHITE), OFF_WHITE_MAPPING, foundations=("elevation",))
    assert result.problems == []
    assert "shadow-dark" not in result.files["theme-ext.css"]


def test_the_default_brand_color_is_named_as_the_engines_default():
    result = extend(_foreign(DARK_ONLY), DARK_ONLY_MAPPING, foundations=("color",))
    assert ("color was generated from every axis at 0.5; its brand color is #3366FF, the "
            "engine's default, since mapping.json maps no color.action.primary and no color's "
            "name says primary or brand; map it there, or pass the brand color.") \
        in result.decisions


def test_colors_that_cannot_be_read_are_said_and_the_engines_page_is_used(monkeypatch):
    extend_module = sys.modules["engine.io.extend"]

    def broken(*args, **kwargs):
        raise InputError("page reads nothing; fix it")

    monkeypatch.setattr(extend_module, "view", broken)
    result = extend(_foreign(OFF_WHITE), OFF_WHITE_MAPPING, foundations=("color",))
    assert ("The colors mapping.json sends to your tokens could not be read (page reads "
            "nothing; fix it), so the added colors were generated around the engine's own page "
            "and text, not yours; fix that entry in mapping.json to have them fit your page.") \
        in result.decisions


def test_added_color_points_at_the_owners_page_in_a_figma_or_tokens_file(tmp_path):
    (tmp_path / "variables.json").write_text(json.dumps(_figma_export()), encoding="utf-8")
    figma = extend(read_figma(tmp_path / "variables.json"), FIGMA_MAPPING,
                   foundations=("color",))
    assert figma.problems == []
    assert figma.tokens.get("color.surface.stripe").value == "{paper}"
    doc = {"ink": {"$type": "color", "$value": "#1b1d22"},
           "paper": {"$type": "color", "$value": "#f4f1ea"},
           "text": {"$type": "color", "$value": "{ink}"},
           "page": {"$type": "color", "$value": "{paper}"}}
    text = json.dumps(doc)
    tokens = extend(import_dtcg(text, _source("tokens.json", "dtcg", text)),
                    Mapping(roles={"color.text.default": RoleMap("text"),
                                   "color.surface.page": RoleMap("page")}),
                    foundations=("color",))
    assert tokens.problems == []
    ext = json.loads(tokens.files["tokens-ext.json"])
    assert ext["color"]["surface"]["stripe"]["$value"] == "{page}"
    assert 1.1 <= contrast(tokens.tokens.resolve("color.surface.tint"), "#f4f1ea") < 1.12


def test_a_foreign_figma_export_gets_an_extension_script(tmp_path):
    (tmp_path / "variables.json").write_text(json.dumps(_figma_export()), encoding="utf-8")
    imported = read_figma(tmp_path / "variables.json")
    result = extend(imported, FIGMA_MAPPING, foundations=("radius",))
    assert result.problems == []
    assert result.beside == ["variables-ext.json", "variables-ext.js"]
    assert result.load.startswith("Run variables-ext.js in the Figma file")


# ---------------------------------------------------------------- a later extension


def test_a_later_extension_keeps_what_an_earlier_one_added(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    first = extend(read_css(tmp_path / "theme.css"), MAPPING, foundations=("radius",))
    assert write_extended(first, read_css(tmp_path / "theme.css"))["status"] == "written"
    mapping = parse_mapping(first.files["mapping.json"], "mapping.json")
    imported = read_css(tmp_path / "theme.css")
    second = extend(imported, mapping, foundations=("motion",))
    assert second.problems == []
    ext = second.files["theme-ext.css"]
    assert "--radius-card:" in ext and "--motion-reveal-duration:" in ext
    assert "motion-reveal-duration" in second.added
    assert "radius-card" not in second.added
    report = second.files["extend-report.md"]
    assert "theme-ext.css, written by an earlier extension, holds" in report
    assert write_extended(second, imported)["status"] == "refused"
    done = write_extended(second, imported, force=True)
    assert done["status"] == "written", done["message"]
    assert (tmp_path / "theme.css").read_text(encoding="utf-8") == FOREIGN
    assert "theme-ext.css" in read_record(tmp_path)


def test_a_later_stylesheet_extension_blocks_where_the_source_now_sets_its_name(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    first = extend(read_css(tmp_path / "theme.css"), MAPPING, foundations=("radius",))
    assert write_extended(first, read_css(tmp_path / "theme.css"))["status"] == "written"
    (tmp_path / "theme.css").write_text(
        FOREIGN.replace("  --page: var(--paper);\n}", "  --page: var(--paper);\n"
                        "  --radius-card: 2px;\n}"), encoding="utf-8")
    mapping = parse_mapping(first.files["mapping.json"], "mapping.json")
    again = extend(read_css(tmp_path / "theme.css"), mapping, foundations=("motion",))
    assert again.problems[0] == (
        "--radius-card is in theme.css and in theme-ext.css, written by an earlier extension, "
        "with other values, so theme-ext.css replaces the value theme.css sets; remove "
        "--radius-card from theme-ext.css, or from theme.css")
    assert list(again.files) == ["extend-report.md"]


TAILWIND = ('@import "tailwindcss";\n\n@theme {\n  --color-ink: #1b1d22;\n'
            '  --color-paper: #fdfdfb;\n}\n')
TW_MAPPING = Mapping(roles={"color.text.default": RoleMap("color-ink"),
                            "color.surface.page": RoleMap("color-paper")})


def test_a_later_tailwind_extension_keeps_the_first_and_sees_a_changed_source(tmp_path):
    (tmp_path / "app.css").write_text(TAILWIND, encoding="utf-8")
    first = extend(read_tailwind(tmp_path / "app.css"), TW_MAPPING, foundations=("radius",))
    assert write_extended(first, read_tailwind(tmp_path / "app.css"))["status"] == "written"
    mapping = parse_mapping(first.files["mapping.json"], "mapping.json")
    second = extend(read_tailwind(tmp_path / "app.css"), mapping, foundations=("motion",))
    assert second.problems == []
    ext = second.files["app-ext.css"]
    assert ext.count("@theme {") == 2 and "--radius-card:" in ext
    assert "--motion-reveal-duration:" in ext and "@import" not in ext
    (tmp_path / "app.css").write_text(
        TAILWIND.replace("}\n", "  --radius-card: 2px;\n}\n"), encoding="utf-8")
    third = extend(read_tailwind(tmp_path / "app.css"), mapping, foundations=("motion",))
    assert third.problems[0].startswith("--radius-card is in app.css and in app-ext.css, "
                                        "written by an earlier extension, with other values")


@pytest.mark.parametrize("fname,text,reader,mapping,value", [
    ("theme.css", FOREIGN, read_css, MAPPING, "calc(1px + 1px)"),
    ("app.css", TAILWIND, read_tailwind, TW_MAPPING, "clamp(1px, 2vw, 3px)"),
])
def test_a_mapped_name_the_source_now_sets_unread_names_the_value_and_the_fix(
        tmp_path, fname, text, reader, mapping, value):
    (tmp_path / fname).write_text(text, encoding="utf-8")
    first = extend(reader(tmp_path / fname), mapping, foundations=("radius",))
    assert write_extended(first, reader(tmp_path / fname))["status"] == "written"
    own = parse_mapping(first.files["mapping.json"], "mapping.json")
    (tmp_path / fname).write_text(text.replace("}\n", f"  --radius-card: {value};\n}}\n", 1),
                                  encoding="utf-8")
    again = extend(reader(tmp_path / fname), own, foundations=("motion",))
    ext = fname.replace(".css", "-ext.css")
    assert again.problems == [
        f"--radius-card is declared in {fname} as a value the import could not read ({value} "
        f"is computed by the browser; write the value it computes to), and in {ext}, written "
        f"by an earlier extension, which loads after {fname} and replaces it; mapping.json "
        f"sends radius.card to it, so write --radius-card in {fname} in a form the import "
        "reads, or map radius.card to another of your tokens in mapping.json"]
    assert list(again.files) == ["extend-report.md"]


def test_a_mapped_name_declared_unread_blocks_on_a_first_run_too():
    text = FOREIGN.replace("  --page: var(--paper);\n}", "  --page: var(--paper);\n"
                           "  --ring: calc(1px + 1px);\n}")
    mapping = Mapping(roles={**MAPPING.roles, "border.focus-ring.width": RoleMap("ring")},
                      axes=dict(MAPPING.axes))
    result = extend(_foreign(text), mapping, foundations=("radius",))
    assert result.problems == [
        "--ring is declared in theme.css as a value the import could not read (calc(1px + 1px) "
        "is computed by the browser; write the value it computes to); mapping.json sends "
        "border.focus-ring.width to it, so write --ring in theme.css in a form the import reads, "
        "or map border.focus-ring.width to another of your tokens in mapping.json"]


def test_a_figma_second_run_before_the_owner_exports_again_keeps_the_mapping(tmp_path):
    (tmp_path / "variables.json").write_text(json.dumps(_figma_export()), encoding="utf-8")
    first = extend(read_figma(tmp_path / "variables.json"), FIGMA_MAPPING,
                   foundations=("radius",))
    assert write_extended(first, read_figma(tmp_path / "variables.json"))["status"] == "written"
    own = parse_mapping(first.files["mapping.json"], "mapping.json")
    assert own.roles["radius.card"] == RoleMap("radius.card", "name")
    second = extend(read_figma(tmp_path / "variables.json"), own, foundations=("motion",))
    assert second.problems == []
    assert second.tokens.has("radius.card")
    payload = json.loads(second.files["variables-ext.json"])
    names = [v["name"] for c in payload["collections"] for v in c["variables"]]
    assert names.index("radius/card") < names.index("motion/reveal/duration")
    assert "| radius | 9 of 9 |" in second.files["extend-report.md"]


def test_a_later_extension_that_would_change_an_earlier_addition_blocks(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    light = Mapping(roles=dict(MAPPING.roles), axes={})
    first = extend(read_css(tmp_path / "theme.css"), light,
                   roles={"color.focus.ring": "brand-700"})
    assert first.problems == []
    write_extended(first, read_css(tmp_path / "theme.css"))
    mapping = Mapping(roles=dict(MAPPING.roles), axes={})
    second = extend(read_css(tmp_path / "theme.css"), mapping,
                    roles={"color.focus.ring": "ink"})
    assert second.problems == [
        "--color-focus-ring is already in theme-ext.css, written by an earlier extension, as "
        "var(--brand-700); extend never changes a token the system has, so edit "
        "theme-ext.css itself, or point color.focus.ring at brand-700"]


def test_an_earlier_tokens_extension_that_now_disagrees_with_the_source_blocks(tmp_path):
    doc = {"ink": {"$type": "color", "$value": "#1b1d22"},
           "paper": {"$type": "color", "$value": "#fdfdfb"}}
    (tmp_path / "tokens.json").write_text(json.dumps(doc), encoding="utf-8")
    mapping = Mapping(roles={"color.text.default": RoleMap("ink"),
                             "color.surface.page": RoleMap("paper")})
    first = extend(read_dtcg(tmp_path / "tokens.json"), mapping, foundations=("radius",))
    assert write_extended(first, read_dtcg(tmp_path / "tokens.json"))["status"] == "written"
    doc["radius"] = {"card": {"$type": "dimension", "$value": {"value": 2, "unit": "px"}}}
    (tmp_path / "tokens.json").write_text(json.dumps(doc), encoding="utf-8")
    again = extend(read_dtcg(tmp_path / "tokens.json"), mapping, foundations=("motion",))
    assert again.problems[0] == (
        "radius.card is in tokens.json and in tokens-ext.json, written by an earlier "
        "extension, with other values, so tokens-ext.json replaces the value tokens.json "
        "sets; remove radius.card from tokens-ext.json, or from tokens.json")


# ---------------------------------------------------------------- writing


def test_a_blocked_result_writes_only_its_report(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    imported = read_css(tmp_path / "theme.css")
    result = extend(imported, MAPPING, roles={"color.focus.ring": "brand-700"})
    assert result.problems
    outcome = write_extended(result, imported, out=tmp_path / "out")
    assert outcome["status"] == "written"
    assert sorted(p.name for p in (tmp_path / "out").iterdir()) == [
        ".uxskill", "extend-report.md"]
    assert sorted(p.name for p in tmp_path.iterdir()) == ["out", "theme.css"]


def test_the_report_and_mapping_can_go_to_another_folder(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    imported = read_css(tmp_path / "theme.css")
    result = extend(imported, MAPPING, foundations=("radius",))
    outcome = write_extended(result, imported, out=tmp_path / "intake")
    assert outcome["status"] == "written", outcome["message"]
    assert (tmp_path / "theme-ext.css").is_file()
    assert sorted(p.name for p in (tmp_path / "intake").iterdir()) == [
        ".uxskill", "extend-report.md", "mapping.json"]
    assert (tmp_path / "theme.css").read_text(encoding="utf-8") == FOREIGN


def test_two_folders_are_written_both_or_neither(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    intake = tmp_path / "intake"
    intake.mkdir()
    (intake / "mapping.json").write_text('{"version": 1, "roles": {}}\n', encoding="utf-8")
    imported = read_css(tmp_path / "theme.css")
    result = extend(imported, MAPPING, foundations=("radius",))
    outcome = write_extended(result, imported, out=intake)
    assert outcome["status"] == "refused"
    assert "Wrote" not in outcome["message"]
    assert not (tmp_path / "theme-ext.css").exists()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["intake", "theme.css"]
    assert sorted(p.name for p in intake.iterdir()) == ["mapping.json"]


@pytest.mark.skipif(NODE is None, reason="node is not installed")
def test_a_second_figma_script_applies_what_both_runs_add(tmp_path):
    (tmp_path / "variables.json").write_text(json.dumps(_figma_export()), encoding="utf-8")
    first = extend(read_figma(tmp_path / "variables.json"), FIGMA_MAPPING,
                   foundations=("radius",))
    write_extended(first, read_figma(tmp_path / "variables.json"))
    own = parse_mapping(first.files["mapping.json"], "mapping.json")
    second = extend(read_figma(tmp_path / "variables.json"), own, foundations=("motion",))
    got = _run(tmp_path, _figma_export(), second.files["variables-ext.js"], READ_SCRIPT)
    result, read = got["out"]
    assert result["conflicts"] == []
    back = import_figma(read, Source("read.json", "figma", "0" * 64, len(read))).tokens
    assert back.resolve("radius.card") == first.tokens.resolve("radius.card")
    assert back.has("motion.reveal.duration") and back.get("ink").value == \
        read_figma(tmp_path / "variables.json").tokens.get("ink").value


def test_every_refusal_is_given_at_once(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    (tmp_path / "theme-ext.css").write_text("/* mine */\n", encoding="utf-8")
    intake = tmp_path / "intake"
    intake.mkdir()
    (intake / "mapping.json").write_text('{"version": 1, "roles": {}}\n', encoding="utf-8")
    imported = read_css(tmp_path / "theme.css")
    result = extend(imported, MAPPING, foundations=("radius",))
    outcome = write_extended(result, imported, out=intake)
    assert outcome["status"] == "refused"
    assert outcome["conflicts"] == [str(tmp_path / "theme-ext.css"), str(intake / "mapping.json")]
    assert "theme-ext.css" in outcome["message"] and "mapping.json" in outcome["message"]


def test_a_second_folder_that_fails_puts_the_first_back(tmp_path, monkeypatch):
    import sys
    module = sys.modules["engine.io.extend"]
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    imported = read_css(tmp_path / "theme.css")
    result = extend(imported, MAPPING, foundations=("radius",))
    real = module.write_with_intake

    def failing(folder, files, sources, **kw):
        if "mapping.json" in files and not kw.get("plan_only"):
            return {"status": "error", "written": [], "unchanged": [], "conflicts": [],
                    "message": "Nothing was written: the disk is full.", "backup": "",
                    "replaced": {}}
        return real(folder, files, sources, **kw)

    monkeypatch.setattr(module, "write_with_intake", failing)
    outcome = write_extended(result, imported, out=tmp_path / "intake")
    assert outcome["status"] == "error"
    assert outcome["message"] == (
        "Nothing was written: the disk is full. What was written in "
        f"{tmp_path} was put back as it was, so nothing changed.")
    assert sorted(p.name for p in tmp_path.iterdir()) == ["theme.css"]


def test_a_font_file_the_owner_has_is_named_in_the_refusal(tmp_path):
    (tmp_path / "theme.css").write_text(FOREIGN, encoding="utf-8")
    (tmp_path / "fonts.css").write_text("/* mine */\n", encoding="utf-8")
    imported = read_css(tmp_path / "theme.css")
    result = extend(imported, MAPPING, foundations=("type",))
    outcome = write_extended(result, imported, force=True)
    assert outcome["status"] == "refused"
    assert outcome["message"].endswith(
        "fonts.css is one of the font files the added faces load through, written beside the "
        "system as a build writes them; move your own file of that name, or pass "
        "--replace-client-files as well as --force to replace it after a backup.")


def test_a_figma_export_the_engine_wrote_still_gets_a_script_to_run(tmp_path):
    export = _figma_export()
    (tmp_path / "variables.json").write_text(json.dumps(export), encoding="utf-8")
    imported = dataclasses.replace(read_figma(tmp_path / "variables.json"), owned=True)
    result = extend(imported, FIGMA_MAPPING, foundations=("radius",))
    assert result.beside == ["variables-ext.json", "variables-ext.js"]
    assert result.load.startswith("Run variables-ext.js")


def test_the_same_extension_gives_the_same_bytes():
    a = extend(_foreign(), MAPPING, foundations=("space", "motion"))
    b = extend(_foreign(), MAPPING, foundations=("space", "motion"))
    assert a.files == b.files


# ---------------------------------------------------------------- bad input


@pytest.mark.parametrize("kwargs,message", [
    ({"foundations": ("colour",)}, "--add names colour, which is not a foundation; use color, "
                                   "space, radius, border, elevation, motion, layout, type or "
                                   "imagery"),
    ({"roles": {"color.text.main": "ink"}}, "--add-role names color.text.main, which is not a "
                                            "role the engine checks; use one of its roles, for "
                                            "example color.text.default"),
    ({"roles": {"color.focus.ring": "missing"}}, "--add-role points color.focus.ring at missing, "
                                                 "which the system does not have; name one of "
                                                 "its tokens"),
    ({"roles": {"space.control.gap": "ink"}}, "--add-role points space.control.gap at ink, a "
                                              "color, but the role needs a dimension; name a "
                                              "dimension token"),
    ({"roles": {"color.text.default": "ink"}}, "--add-role names color.text.default, which the "
                                               "mapping already sends to text-body; edit "
                                               "mapping.json to repoint it"),
])
def test_bad_additions_name_the_input_and_the_fix(kwargs, message):
    with pytest.raises(InputError) as exc:
        extend(_foreign(), MAPPING, **kwargs)
    assert str(exc.value) == message


def test_a_role_the_owner_kept_out_is_named_as_kept_out():
    mapping = Mapping(roles={**MAPPING.roles, "color.focus.ring": RoleMap(None, "owner")},
                      axes=dict(MAPPING.axes))
    with pytest.raises(InputError) as exc:
        extend(_foreign(), mapping, roles={"color.focus.ring": "brand-700"})
    assert str(exc.value) == (
        '--add-role names color.focus.ring, which mapping.json keeps out of the check with '
        '{"token": null, "by": "owner"}; remove that entry from mapping.json to add it')


def test_extend_does_not_load_the_writer():
    import subprocess
    import sys
    code = ("import sys, engine.io.extend; "
            "print('engine.foundations.emit' in sys.modules)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                         check=True, cwd=Path(__file__).resolve().parents[2])
    assert out.stdout.strip() == "False"
