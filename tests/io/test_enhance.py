"""Measure before defining: the enhance report reads an imported system,
checks it through the mapping and measures the codebase against it:
unused tokens, raw values a token already holds, values written many ways,
names that lie about how a token is used, and references to tokens the
system lacks. It reports; it never rewrites a file."""
from engine import io
from engine.foundations.tokens import Token, TokenSet
from engine.io.adapter import ROLE_TYPES, AxisMap, Mapping, RoleMap, merge, propose
from engine.io.css_in import import_css
from engine.io.enhance import drift, enhance
from engine.io.report import Imported, ImportReport, Source
from engine.io.scan import scan

SYSTEM = """:root {
  --ink: #1b1d22;
  --paper: #ffffff;
  --blue-500: #3366ff;
  --blue-600: #2952cc;
  --radius-sm: 4px;
  --radius-lg: 12px;
  --text-body: var(--ink);
  --bg-page: var(--paper);
  --primary: var(--blue-500);
  --primary-hover: var(--blue-600);
  --border-subtle: #d0d4da;
}
.dark {
  --text-body: var(--paper);
  --bg-page: var(--ink);
}
"""

APP_CSS = """.page { background: var(--bg-page); color: var(--text-body); }
.btn { background: var(--primary); color: #fff; border-radius: 4px; }
.btn:hover { background: var(--primary-hover); }
.link { color: var(--primary-hover); }
.card { border-radius: 11px; background: var(--text-body); border: 1px solid #FFF; }
.tag { border-radius: .25rem; color: white; outline-color: var(--missing-ring); }
"""


def _system(text=SYSTEM):
    return import_css(text, Source("tokens.css", "css", "ab" * 32, len(text)))


def _project(tmp_path):
    (tmp_path / "app.css").write_text(APP_CSS, encoding="utf-8")
    return tmp_path


MAPPING = Mapping(
    roles={"color.text.default": RoleMap("text-body", "owner"),
           "color.surface.page": RoleMap("bg-page", "owner"),
           "color.action.primary": RoleMap("primary", "name")},
    axes={"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"}, "name")})


def test_drift_finds_unused_tokens_raw_values_and_spellings(tmp_path):
    imported = _system()
    d = drift(imported.tokens, scan([_project(tmp_path)], imported.tokens))
    assert d.unused == ["radius-sm", "radius-lg", "border-subtle"]
    assert d.totals == {"color": (9, 8), "dimension": (2, 0)}
    assert [(r.value, r.tokens, [u.where() for u in r.uses]) for r in d.raw_with_token] == [
        ("#FFFFFF", ["bg-page", "paper"], ["app.css:2", "app.css:5", "app.css:6"]),
        ("4px", ["radius-sm"], ["app.css:2", "app.css:6"])]
    assert [(s.value, s.texts) for s in d.spellings] == [
        ("#FFFFFF", ["#fff", "#FFF", "white"]), ("4px", ["4px", ".25rem"])]
    assert [(f, vals) for f, vals in d.distinct.items()] == [
        ("color", ["#FFFFFF"]), ("radius", ["4px", "11px"]), ("border", ["1px"])]
    assert [(m.value, m.where) for m in d.missing] == [("--missing-ring", "app.css:6")]


def test_names_with_stray_uses_are_named_with_where_they_are_used(tmp_path):
    imported = _system()
    d = drift(imported.tokens, scan([_project(tmp_path)], imported.tokens))
    # Some uses match these names, so they are strays, not lies.
    assert d.lies == []
    assert [(n.token, n.message) for n in d.strays] == [
        ("text-body", "is named for text but is used as a background at app.css:5; 1 of its 2 "
                      "uses match its name"),
        ("primary-hover", "is named for hover but is used outside hover at app.css:4; 1 of its "
                          "2 uses match its name")]


def test_the_report_is_markdown_in_a_fixed_order_and_writes_nothing(tmp_path):
    project = _project(tmp_path)
    before = sorted((p.name, p.stat().st_mtime_ns) for p in project.iterdir())
    imported = _system()
    report = enhance(imported, MAPPING, scan([project], imported.tokens))
    text = report.markdown()
    assert sorted((p.name, p.stat().st_mtime_ns) for p in project.iterdir()) == before
    heads = [line for line in text.splitlines() if line.startswith("## ")]
    assert heads == ["## What was read", "## How it was checked", "## Structure", "## Gate",
                     "## What the code uses", "## For the owner to confirm",
                     "## Decisions made without you"]
    assert f"Mapped 3 of {len(ROLE_TYPES)} " in text
    assert ("- 3 of 11 tokens were not found in the 1 file read: radius-sm, radius-lg, "
            "border-subtle. They are defined in tokens.css; if no code outside the scan uses "
            "them, removing them is your call") in text
    assert "never used" not in text
    assert ("- #FFFFFF is written raw 3 times (app.css:2, app.css:5, app.css:6); the system "
            "holds it as bg-page and paper, so use a token.") in text
    assert "- radius is written as 2 raw values: 4px, 11px." in text
    assert ("- color.action.primary is mapped to primary by name only; confirm it in "
            "mapping.json.") in text
    assert "- scheme is read from scheme by name only; confirm it in mapping.json." in text
    assert "- The system has no reduced-motion mode" in text
    assert "- app.css:6 references --missing-ring, which the system does not have;" in text
    data = report.to_dict()
    assert list(data) == ["source", "import", "mapping", "structure", "gate", "drift",
                          "confirm", "decisions"]
    assert data["drift"]["unused"] == ["radius-sm", "radius-lg", "border-subtle"]


def test_every_code_line_names_where_and_the_fix(tmp_path):
    imported = _system()
    text = enhance(imported, MAPPING, scan([_project(tmp_path)], imported.tokens)).markdown()
    section = text.split("## What the code uses")[1].split("## For the owner")[0]
    lines = [line for line in section.splitlines() if line.startswith("- ")]
    assert lines
    for line in lines:
        if line.startswith(("- color: ", "- dimension: ")):
            continue
        assert any(w in line for w in ("app.css:", "not found")), line
        assert any(w in line for w in ("use a token", "pick one", "move", "rename", "add ",
                                       "remove", "scan")), line


def test_without_a_scan_the_report_says_the_code_was_not_measured():
    imported = _system()
    text = enhance(imported, MAPPING, None).markdown()
    assert ("No code was scanned, so nothing here says which tokens are used; pass the folders "
            "that hold the product's code with --scan.") in text
    assert enhance(imported, MAPPING, None).to_dict()["drift"] is None


def _bullets(text):
    """Each bullet of a markdown text, its wrapped lines joined."""
    out = []
    for line in text.splitlines():
        if line.startswith("  ") and out and not line.startswith("  - "):
            out[-1] += " " + line.strip()
        else:
            out.append(line)
    return out


def test_gate_findings_carry_the_systems_own_names():
    text = SYSTEM.replace("--ink: #1b1d22;", "--ink: #d9dade;")
    report = enhance(_system(text), MAPPING, None)
    gate = report.markdown().split("## Gate")[1].split("## What the code")[0]
    assert max(len(line) for line in gate.splitlines()) <= 160
    lines = [line for line in _bullets(report.markdown())
             if line.startswith("- color.text.default (your text-body) on color.surface.page "
                                "(your bg-page)")]
    assert lines and "(scheme:light,contrast:" not in lines[0]
    assert "1.4.3" in lines[0]
    # The fix is the owner's to make in their own system, not a step of ours.
    assert "Move color.text.default to a step" not in lines[0]
    assert "in your system" in lines[0]
    assert report.to_dict()["gate"]["passed"] is False


def test_an_axis_read_under_other_values_names_them():
    ts = TokenSet({"class-dark": ("off", "on")})
    ts.add(Token("ink", "color", "#1B1D22", modes={"class-dark:on": "#FFFFFF"}))
    ts.add(Token("paper", "color", "#FFFFFF", modes={"class-dark:on": "#1B1D22"}))
    source = Source("tokens.css", "css", "ab" * 32, 10)
    imported = Imported(ts, ImportReport.of(source, ts, 2))
    mapping = Mapping({"color.text.default": RoleMap("ink", "owner"),
                       "color.surface.page": RoleMap("paper", "owner")},
                      {"scheme": AxisMap("class-dark", {"light": "off", "dark": "on"}, "name")})
    text = enhance(imported, mapping).markdown()
    assert ("- scheme is read from class-dark by name only (light is off, dark is on); confirm "
            "it in mapping.json.") in text


def test_an_empty_mapping_never_passes_silently():
    report = enhance(_system(), Mapping(), None)
    text = report.markdown()
    assert f"Mapped 0 of {len(ROLE_TYPES)} roles" in text
    assert "No role is mapped, so the gate had nothing to measure" in text
    assert "gate passed" not in text
    gate = report.to_dict()["gate"]
    assert gate["measured"] is False and gate["passed"] is None


def test_roles_the_owner_left_out_stay_out_and_are_told_apart_from_unmapped_ones():
    mapping = Mapping(
        roles={"color.text.default": RoleMap("text-body", "owner"),
               "color.surface.page": RoleMap(None, "owner"),
               "color.action.primary": RoleMap("primary", "name")},
        axes={"scheme": AxisMap("scheme", {"light": "light", "dark": "dark"}, "owner"),
              "motion": AxisMap(None, {}, "owner")})
    report = enhance(_system(), mapping, None)
    text = report.markdown()
    assert f"Mapped 2 of {len(ROLE_TYPES)} roles" in text
    assert "- Left out by you (1): color.surface.page." in text
    assert "- Axes left out by you (1): motion." in text
    not_mapped = [r for r in ROLE_TYPES if r not in mapping.roles]
    assert f"Not mapped at all ({len(not_mapped)})" in text
    assert "color.surface.page" not in report.to_dict()["mapping"]["not_mapped"]
    assert report.to_dict()["mapping"]["left_out"] == ["color.surface.page"]
    assert report.to_dict()["mapping"]["roles"]["color.surface.page"] is None
    decisions = text.split("## Decisions made without you")[1]
    assert "color.surface.page" not in decisions
    # The owner chose to leave motion out, so it is not asked for again.
    assert "reduced-motion" not in text


def test_a_merged_mapping_keeps_the_owners_null_and_its_notes_are_reported():
    imported = _system()
    existing = Mapping(roles={"color.text.default": RoleMap(None, "owner")})
    merged, notes = merge(propose(imported.tokens), existing)
    assert merged.roles["color.text.default"].token is None
    report = enhance(imported, merged, None, merge_notes=notes)
    decisions = report.markdown().split("## Decisions made without you")[1]
    assert notes and all(f"- {n}." in decisions or f"- {n}" in decisions for n in notes)
    assert report.to_dict()["mapping"]["merge_notes"] == notes
    assert report.to_dict()["mapping"]["roles"]["color.text.default"] is None


def test_what_the_scan_did_not_read_is_carried_into_the_report(tmp_path):
    project = _project(tmp_path)
    (project / "app.min.css").write_text(".a{color:red}", encoding="utf-8")
    imported = _system()
    scanned = scan([project], imported.tokens)
    scanned.unknown_classes.append(("page.html", 1, "text-brand"))
    text = enhance(imported, MAPPING, scanned).markdown()
    assert "- app.min.css is a minified build file; scan its source instead." in text
    assert "- page.html:1 uses the class text-brand, which names no token in the system;" in text


def test_the_report_is_deterministic_and_plain_text(tmp_path):
    imported = _system()
    scanned = scan([_project(tmp_path)], imported.tokens)
    first = enhance(imported, MAPPING, scanned).markdown()
    assert first == enhance(imported, MAPPING, scanned).markdown()
    assert first.isascii()
    dashes = "-" * 2
    assert f" {dashes} " not in first and "\u2014" not in first and "\u2013" not in first


def test_enhance_is_exported_with_merge_and_every_earlier_name():
    for name in ("Drift", "Enhanced", "drift", "enhance", "merge", "propose", "view",
                 "their_names", "scan", "Scan", "Usage", "import_css", "REST_ENDPOINT",
                 "SIZE_SCOPES", "CSS_KEYWORDS", "GamutMapped", "Mapped"):
        assert name in io.__all__ and hasattr(io, name), name


def test_the_owner_is_asked_to_confirm_the_reading_face_and_the_breakpoints():
    ts = TokenSet({})
    ts.add(Token("body", "typography", {
        "fontFamily": ["Plain Serif", "serif"], "fontSize": {"value": 16, "unit": "px"},
        "fontWeight": 400, "letterSpacing": {"value": 0, "unit": "px"}, "lineHeight": 1.5}))
    ts.add(Token("bp-md", "dimension", {"value": 48, "unit": "rem"}))
    source = Source("tokens.json", "dtcg", "ab" * 32, 10)
    imported = Imported(ts, ImportReport.of(source, ts, 2))
    mapping = Mapping({"type.text.body": RoleMap("body", "owner"),
                       "layout.breakpoint.tablet": RoleMap("bp-md", "name")})
    text = enhance(imported, mapping).markdown()
    confirm = text.split("## For the owner to confirm")[1].split("## Decisions")[0]
    assert ("- type.text.body (your body) is set in Plain Serif; confirm it is a face made for "
            "running text, not a display face.") in confirm
    assert "- The breakpoints are layout.breakpoint.tablet 48rem; confirm" in confirm
    assert "- The system has no dark mode in the mapping" in confirm


def test_a_hover_token_used_on_hover_in_dark_does_not_lie(tmp_path):
    (tmp_path / "app.css").write_text(
        ".btn:hover { background: var(--primary-hover); }\n"
        ".dark .btn:hover { background: var(--primary-hover); }\n", encoding="utf-8")
    imported = _system()
    d = drift(imported.tokens, scan([tmp_path], imported.tokens))
    assert [u.state for u in scan([tmp_path], imported.tokens).usages] == [
        "hover", "scheme:dark,hover"]
    assert d.lies == [] and d.strays == []


def test_values_the_scan_saw_but_could_not_measure_are_named(tmp_path):
    imported = _system()
    scanned = scan([_project(tmp_path)], imported.tokens)
    # A plain tuple, as an older scanner wrote it: no reason, so a generic fix.
    scanned.not_read = [("Card.tsx", 4, "interpolation", "color: ${ink};\n  padding: 8px;")]
    report = enhance(imported, MAPPING, scanned)
    assert ("- Card.tsx:4 writes color: ${ink}; padding: 8px; (interpolation), which the scan "
            "does not measure; check it by hand") in report.markdown()
    assert report.to_dict()["drift"]["not_read"] == [
        {"where": "Card.tsx:4", "kind": "interpolation",
         "text": "color: ${ink};\n  padding: 8px;", "why": ""}]
    assert report.to_dict()["drift"]["complete"] is False


# ---------------------------------------------------------------- coverage


def test_an_empty_folder_measures_nothing_and_lists_no_token(tmp_path):
    imported = _system()
    report = enhance(imported, MAPPING, scan([tmp_path], imported.tokens))
    section = report.markdown().split("## What the code uses")[1].split("## For the")[0]
    assert "No file was read, so nothing was measured" in section
    assert "radius-sm" not in section and "not found" not in section
    assert report.to_dict()["drift"]["complete"] is False


def test_tokens_used_only_in_a_skipped_file_are_never_advised_away(tmp_path):
    project = _project(tmp_path)
    (project / "vendor.min.css").write_text(".x{border-radius:var(--radius-sm)}",
                                            encoding="utf-8")
    imported = _system()
    report = enhance(imported, MAPPING, scan([project], imported.tokens))
    text = report.markdown()
    assert "Read 1 file. 1 file was not read; each is listed at the end of this section" in text
    assert ("- 3 of 11 tokens were not found in the 1 file read: radius-sm, radius-lg, "
            "border-subtle. They are defined in tokens.css; 1 file was not read (listed below), "
            "so scan those too or confirm by hand before removing any.") in text
    assert "- vendor.min.css is a minified build file; scan its source instead." in text
    assert report.to_dict()["drift"]["complete"] is False


def test_what_the_scanner_could_not_measure_carries_its_reason(tmp_path):
    (tmp_path / "app.css").write_text(".a { margin: calc(100% - 12px); color: var(--ink); }\n",
                                      encoding="utf-8")
    imported = _system()
    scanned = scan([tmp_path], imported.tokens)
    entries = list(getattr(scanned, "not_read", ()))
    assert entries and getattr(entries[0], "why", "")
    text = enhance(imported, MAPPING, scanned).markdown()
    assert f"- app.css:1 was not measured (value): {entries[0].why}" in text
    assert "1 place was not measured" in text
    assert "so scan those too or confirm by hand before removing any" in text


# ---------------------------------------------------------------- names


NAMED = """:root {
  --surface: #ffffff;
  --surface-card: #f4f5f7;
  --on-surface: #1b1d22;
  --on-primary: #ffffff;
  --onSecondary: #ffffff;
  --hover-bg: #e8eaee;
  --weight-regular: 400;
  --z-top: 400;
  --space-4: 16px;
  --radius-lg: 1rem;
}
"""


def _named(tmp_path, css):
    imported = _system(NAMED)
    (tmp_path / "app.css").write_text(css, encoding="utf-8")
    return drift(imported.tokens, scan([tmp_path], imported.tokens))


def test_a_name_on_a_surface_is_a_foreground(tmp_path):
    d = _named(tmp_path, ".a { color: var(--on-surface); background: var(--surface); }\n"
                         ".b { color: var(--on-primary); fill: var(--onSecondary); }\n")
    assert d.lies == [] and d.strays == []


def test_a_foreground_used_as_a_background_is_a_lie(tmp_path):
    d = _named(tmp_path, ".a { background: var(--on-surface); }\n")
    assert [(x.token, x.message) for x in d.lies] == [
        ("on-surface", "is named for the color on a surface but is used as a background at "
                       "app.css:1; 0 of its 1 uses match its name")]


def test_a_background_used_only_as_text_is_a_lie_and_a_border_use_is_not(tmp_path):
    d = _named(tmp_path, ".a { color: var(--surface-card); }\n"
                         ".b { border-color: var(--surface); }\n")
    assert [x.token for x in d.lies] == ["surface-card"]
    assert "is named for backgrounds but is used for text color at app.css:1" in d.lies[0].message
    assert d.strays == []


def test_the_lie_names_the_word_that_failed(tmp_path):
    d = _named(tmp_path, ".a { background: var(--hover-bg); }\n")
    assert [(x.token, x.message) for x in d.lies] == [
        ("hover-bg", "is named for hover but is used outside hover at app.css:1; 0 of its 1 "
                     "uses match its name")]


def test_raw_values_are_matched_within_their_family(tmp_path):
    d = _named(tmp_path, ".a { z-index: 400; font-weight: 400; padding: 16px; "
                         "border-radius: 1rem; }\n")
    held = {(r.uses[0].family, r.value): r.tokens for r in d.raw_with_token}
    assert held == {("z", "400"): ["z-top"], ("weight", "400"): ["weight-regular"],
                    ("space", "16px"): ["space-4"], ("radius", "16px"): ["radius-lg"]}
    assert d.spellings == []


# ---------------------------------------------------------------- gate


def test_a_set_with_no_mode_prints_no_empty_context():
    ts = TokenSet({})
    ts.add(Token("ink", "color", "#D9DADE"))
    ts.add(Token("paper", "color", "#FFFFFF"))
    imported = Imported(ts, ImportReport.of(Source("tokens.css", "css", "ab" * 32, 10), ts, 2))
    mapping = Mapping({"color.text.default": RoleMap("ink", "owner"),
                       "color.surface.page": RoleMap("paper", "owner")})
    report = enhance(imported, mapping)
    assert report.findings and all(" ()" not in f for f in report.findings)
    # The gate wraps at 160 characters, so the sentence is matched across lines.
    assert "Each finding names our role, then your token in tokens.css." \
        in " ".join(report.markdown().split())


def test_a_clean_gate_names_no_findings_and_a_lone_role_says_no_pair_was_measured():
    text = enhance(_system(), MAPPING).markdown()
    assert "Each finding names" not in text
    lone = Mapping({"color.text.default": RoleMap("text-body", "owner")})
    report = enhance(_system(), lone)
    assert "No contrast pair was measured, since each needs both of its roles mapped" \
        in report.markdown()
    assert report.to_dict()["gate"]["pairs_checked"] == 0


def test_the_not_mapped_list_is_folded_and_complete_in_the_json():
    report = enhance(_system(), MAPPING)
    text = report.markdown()
    how = text.split("## How it was checked")[1].split("## Structure")[0]
    assert max(len(line) for line in how.splitlines()) <= 160
    assert "  - color: 68 of 71, such as color.surface.card, color.surface.sunken and 66 more" \
        in how
    assert len(report.to_dict()["mapping"]["not_mapped"]) == len(ROLE_TYPES) - 3


def test_a_background_name_with_on_in_the_middle_is_still_a_background(tmp_path):
    imported = _system(":root { --bg-on-dark: #111111; --surface-on-inverse: #222222; }\n")
    (tmp_path / "app.css").write_text(".a { background: var(--bg-on-dark); }\n"
                                      ".b { background-color: var(--surface-on-inverse); }\n",
                                      encoding="utf-8")
    d = drift(imported.tokens, scan([tmp_path], imported.tokens))
    assert d.lies == [] and d.strays == []


def test_strays_are_introduced_by_a_sentence_that_says_what_they_are(tmp_path):
    imported = _system()
    text = enhance(imported, MAPPING, scan([_project(tmp_path)], imported.tokens)).markdown()
    lines = text.splitlines()
    first = next(i for i, line in enumerate(lines) if line.startswith("- text-body is named"))
    assert lines[first - 2] == ("These names match some of their uses and not others; each "
                                "line says where a use does not match:")


def test_a_var_to_a_property_the_code_declares_is_not_a_missing_token(tmp_path):
    (tmp_path / "a.css").write_text(".l { --local: var(--only-local); color: var(--local); }\n",
                                    encoding="utf-8")
    (tmp_path / "b.css").write_text(".m { background: var(--local); }\n", encoding="utf-8")
    imported = _system()
    report = enhance(imported, MAPPING, scan([tmp_path], imported.tokens))
    d = report.drift
    assert [m.value for m in d.missing] == ["--only-local"]
    assert d.own == {"--local": ["a.css:1", "b.css:1"]}
    text = report.markdown()
    assert "references --local" not in text
    assert ("- The code declares 1 custom property of its own and references it 2 times: "
            "--local (a.css:1, b.css:1). It is the code's own, not a token the system lacks; if "
            "it holds a value the design keeps, move it into tokens.css as a token.") in text
    assert report.to_dict()["drift"]["own"] == [
        {"name": "--local", "uses": ["a.css:1", "b.css:1"]}]


def test_what_was_not_read_is_not_listed_under_the_strays(tmp_path):
    project = _project(tmp_path)
    (project / "extra.css").write_text(".x { margin: calc(100% - 4px); }\n", encoding="utf-8")
    imported = _system()
    lines = enhance(imported, MAPPING, scan([project], imported.tokens)).markdown().splitlines()
    unread = next(i for i, line in enumerate(lines) if line.startswith("- extra.css:1"))
    strays = next(i for i, line in enumerate(lines) if line.startswith("These names match"))
    assert strays < unread
    assert lines[unread - 2] == "What the scan did not read or measure:"


def test_a_deleted_axis_is_named_once_not_asked_about_again():
    mapping = Mapping(dict(MAPPING.roles), {})
    report = enhance(_system(), mapping)
    text = report.markdown()
    assert "mapping.json leaves out the axis scheme" in " ".join(text.split())
    assert "The system has no dark mode in the mapping" not in text


def test_a_padding_is_not_matched_to_a_text_size(tmp_path):
    imported = _system(":root { --space-4: 16px; --text-base: 16px; --leading-loose: 16px; }\n")
    (tmp_path / "app.css").write_text(".a { padding: 16px; font-size: 16px; }\n",
                                      encoding="utf-8")
    d = drift(imported.tokens, scan([tmp_path], imported.tokens))
    held = {(r.uses[0].family, r.value): r.tokens for r in d.raw_with_token}
    assert held == {("space", "16px"): ["space-4"],
                    ("type-size", "16px"): ["text-base", "leading-loose"]}


def _unresolved_system(ink="{base.ink}"):
    ts = TokenSet({})
    ts.add(Token("mid", "color", "{base.ink}", layer="semantic"))
    ts.add(Token("ink", "color", ink, layer="semantic"))
    ts.add(Token("paper", "color", "#FFFFFF"))
    ts.add(Token("line", "color", "#1B1D22"))
    return Imported(ts, ImportReport.of(Source("tokens.json", "dtcg", "ab" * 32, 10), ts, 4))


def test_a_mapped_role_that_cannot_be_resolved_goes_to_structure_with_its_reason():
    mapping = Mapping({"color.text.default": RoleMap("ink", "owner"),
                       "color.surface.page": RoleMap("paper", "owner")})
    report = enhance(_unresolved_system(), mapping)
    text = report.markdown()
    structure = text.split("## Structure")[1].split("## Gate")[0]
    assert ("- color.text.default (your ink) cannot be resolved: ink aliases base.ink, which is "
            "not defined; define base.ink in tokens.json, or map color.text.default to a "
            "token that resolves in mapping.json.") in structure
    gate = " ".join(text.split("## Gate")[1].split("## What the code")[0].split())
    assert ("No contrast pair was measured, since color.text.default could not be resolved "
            "(see Structure), so the verdict covers the rule checks only:") in gate
    assert "since each needs both of its roles mapped" not in gate
    decisions = text.split("## Decisions made without you")[1]
    assert "cannot be resolved" not in decisions and "(resolving" not in text
    assert report.to_dict()["gate"]["unresolved"] == ["color.text.default"]


def test_an_unresolved_chain_is_one_clause_per_hop_and_measured_pairs_still_say_it():
    mapping = Mapping({"color.text.default": RoleMap("ink", "owner"),
                       "color.surface.page": RoleMap("paper", "owner"),
                       "color.text.muted": RoleMap("line", "owner")})
    report = enhance(_unresolved_system("{mid}"), mapping)
    text = report.markdown()
    assert ("cannot be resolved: ink aliases mid, mid aliases base.ink, which is not defined; "
            "define base.ink in tokens.json") in text
    gate = " ".join(text.split("## Gate")[1].split("## What the code")[0].split())
    assert report.check.report.checked > 0
    assert ("The pairs and rules that need color.text.default were not measured, since it "
            "could not be resolved (see Structure).") in gate


def test_an_unknown_class_fix_names_the_namespace_and_a_near_token(tmp_path):
    imported = _system(":root { --accent: #3366ff; --spacing-gutter: 1.5em; }\n")
    (tmp_path / "a.html").write_text('<p class="md:flex bg-accent m-gutter bg-brand"></p>\n',
                                     encoding="utf-8")
    text = " ".join(enhance(imported, Mapping(), scan([tmp_path], imported.tokens))
                    .markdown().split())
    assert ("- a.html:1 uses the class bg-accent, which names no token in the color, colors or "
            "backgroundColor namespaces; the system has accent, outside them: rename it "
            "color-accent so the class reads it, or use a class that names a token the system "
            "has.") in text
    assert ("- a.html:1 uses the class m-gutter, which names no token in the spacing "
            "namespace; tokens.css holds --spacing-gutter at tokens.css:1, which was not read "
            "(the import report says how to write it): fix that entry so the class reads "
            "it.") in text
    assert ("- a.html:1 uses the class bg-brand, which names no token in the color, colors or "
            "backgroundColor namespaces; add color-brand to the system, or use a class that "
            "names a token it has.") in text


# ---------------------------------------------------------------- size


def _big_repo(root, files=3000):
    root.mkdir()
    for i in range(files):
        (root / f"page{i}.html").write_text(
            f'<div class="md:flex bg-gray-{100 * (i % 9 + 1)} text-slate-700 p-{i % 12} '
            f'rounded-lg shadow-md bg-brand{i % 40}">\n'
            f'<p style="margin: calc(100% - {i}px); color: var(--nope-{i % 300})">x</p>\n'
            f'<i style="padding: {i % 7}em"></i></div>\n', encoding="utf-8")
    for i in range(100):
        (root / f"vendor{i}.min.css").write_text(".a{color:red}", encoding="utf-8")
    return root


def test_a_big_repo_keeps_the_report_small_and_the_json_complete(tmp_path):
    from engine.foundations import build_system
    from engine.foundations.export import to_css
    from engine.synthesizer.axes import AxisValues
    ts = build_system(AxisValues(*[0.5] * 7), "#3366FF", arabic=False).tokens
    imported = import_css(to_css(ts), Source("tokens.css", "css", "ab" * 32, 1))
    scanned = scan([_big_repo(tmp_path / "repo")], imported.tokens)
    report = enhance(imported, propose(imported.tokens), scanned)
    text = report.markdown()
    assert len(text.encode("utf-8")) < 200_000, len(text)
    data = report.to_dict()
    assert len(data["drift"]["skipped"]) == 100
    assert len(data["drift"]["unknown_classes"]) == len(scanned.unknown_classes) > 3000
    assert len(data["drift"]["not_read"]) == len(scanned.not_read) >= 3000
    assert len(data["drift"]["missing"]) == 3000
    assert len(data["mapping"]["by_name"]) > 100
    # Each folded line says how many and shows a few.
    assert "- 100 files were not read (vendor0.min.css, vendor1.min.css, vendor10.min.css and " \
           "97 more): each is a minified build file; scan its source instead." in text
    assert "- The code references 300 names the system does not have, 3000 times:" in text
    assert " roles are mapped by name only" in text
    decisions = text.split("## Decisions made without you")[1]
    assert ("- 71 color roles are mapped by name only, each to the token of the same name: "
            "color.surface.page, color.surface.card, color.surface.sunken and 68 more; confirm "
            "them in mapping.json.") in decisions
    assert decisions.count(" by name only") < 20
