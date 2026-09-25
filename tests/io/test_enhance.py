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


def test_names_that_lie_are_named_with_where_they_are_used(tmp_path):
    imported = _system()
    d = drift(imported.tokens, scan([_project(tmp_path)], imported.tokens))
    assert [(n.token, n.message) for n in d.lies] == [
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
    assert "- 3 of 11 tokens are never used: radius-sm, radius-lg, border-subtle." in text
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
        assert any(w in line for w in ("app.css:", "never used")), line
        assert any(w in line for w in ("use a token", "pick one", "move", "rename", "add ",
                                       "remove", "scan")), line


def test_without_a_scan_the_report_says_the_code_was_not_measured():
    imported = _system()
    text = enhance(imported, MAPPING, None).markdown()
    assert ("No code was scanned, so nothing here says which tokens are used; pass the folders "
            "that hold the product's code with --scan.") in text
    assert enhance(imported, MAPPING, None).to_dict()["drift"] is None


def test_gate_findings_carry_the_systems_own_names():
    text = SYSTEM.replace("--ink: #1b1d22;", "--ink: #d9dade;")
    report = enhance(_system(text), MAPPING, None)
    lines = [line for line in report.markdown().splitlines()
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
    assert "- app.min.css was not read: it is a minified build file; scan its source instead." \
        in text
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
    assert d.lies == []


def test_values_the_scan_saw_but_could_not_measure_are_named(tmp_path):
    imported = _system()
    scanned = scan([_project(tmp_path)], imported.tokens)
    scanned.not_read = [("Card.tsx", 4, "CSS-in-JS template", "color: ${ink};\n  padding: 8px;")]
    text = enhance(imported, MAPPING, scanned).markdown()
    assert ("- Card.tsx:4 writes color: ${ink}; padding: 8px; (CSS-in-JS template), which the "
            "scan does not measure, so nothing above counts it; check it by hand") in text
    assert enhance(imported, MAPPING, scanned).to_dict()["drift"]["not_read"] == [
        {"where": "Card.tsx:4", "kind": "CSS-in-JS template",
         "text": "color: ${ink};\n  padding: 8px;"}]
