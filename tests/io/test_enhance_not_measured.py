"""The gate never says passed when it measured nothing: with no role
mapped, the report says "not measured" and why, in markdown and in JSON
(measured false, passed null), whichever importer read the system."""
import json
from pathlib import Path

import pytest

from engine.io.adapter import FieldMap, Mapping, RoleMap, propose
from engine.io.css_in import read_css
from engine.io.dtcg_in import read_dtcg
from engine.io.enhance import enhance
from engine.io.figma_in import read_figma
from engine.io.markdown_in import read_markdown
from engine.io.tailwind_in import read_tailwind

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"

# Invented systems whose names say no role: a ramp and a radius scale.
SOURCES = {
    "css": ("tokens.css", ":root {\n  --moss-500: #2f7d4f;\n  --radius-sm: 4px;\n}\n"),
    "dtcg": ("tokens.json", json.dumps({
        "moss": {"500": {"$type": "color", "$value": "#2f7d4f"}},
        "radius": {"sm": {"$type": "dimension", "$value": {"value": 4, "unit": "px"}}}})),
    "tailwind": ("app.css", '@import "tailwindcss";\n@theme {\n  --color-moss-500: #2f7d4f;\n'
                            '  --radius-sm: 4px;\n}\n'),
    "tailwind-json": ("theme.json", json.dumps({"colors": {"moss": {"500": "#2f7d4f"}},
                                                "borderRadius": {"sm": "4px"}})),
    "markdown": ("rules.md", "# Tokens\n\n- `moss.500`: #2f7d4f\n- `bend.snug`: 4px\n"),
}
READERS = {"css": read_css, "dtcg": read_dtcg, "tailwind": read_tailwind,
           "tailwind-json": read_tailwind, "markdown": read_markdown}
NOT_MEASURED = ("Not measured: no role is mapped, so the gate had nothing to measure and nothing "
                "here passed; map roles to your tokens in mapping.json to check them.")


@pytest.mark.parametrize("fmt", list(SOURCES))
def test_a_system_whose_names_map_no_role_is_not_measured(tmp_path, fmt):
    name, text = SOURCES[fmt]
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    imported = READERS[fmt](path)
    mapping = propose(imported.tokens)
    assert mapping.roles == {}
    result = enhance(imported, mapping)
    gate = result.to_dict()["gate"]
    assert (gate["measured"], gate["passed"]) == (False, None)
    assert gate["why"] == "no role is mapped"
    markdown = result.markdown()
    assert NOT_MEASURED in markdown
    assert "passed" not in markdown.split("## Gate", 1)[1].split("##", 1)[0].replace(
        "nothing here passed", "")


def test_a_figma_export_with_nothing_mapped_is_not_measured():
    imported = read_figma(FIXTURES / "figma" / "variables.json")
    gate = enhance(imported, Mapping()).to_dict()["gate"]
    assert (gate["measured"], gate["passed"], gate["why"]) == (False, None, "no role is mapped")


def test_mapped_roles_that_could_not_be_checked_are_not_measured_either(tmp_path):
    path = tmp_path / "tokens.css"
    path.write_text(":root {\n  --text-size-lg: 1.125rem;\n}\n", encoding="utf-8")
    imported = read_css(path)
    # One field of the role is mapped; the rest are never guessed, so the
    # role is left out and the gate has nothing.
    mapping = Mapping(roles={"type.text.body": RoleMap.per_field(
        {"fontSize": FieldMap("text-size-lg", "owner")})})
    result = enhance(imported, mapping)
    gate = result.to_dict()["gate"]
    assert (gate["measured"], gate["passed"]) == (False, None)
    assert gate["why"] == "no mapped role could be checked"
    assert ("Not measured: the 1 mapped role could not be checked (see Structure and the "
            "decisions), so the gate had nothing to measure and nothing here passed.") in \
        result.markdown()


def test_mapped_roles_that_gave_no_check_read_as_such():
    from engine.foundations.build import SystemCheck
    from engine.foundations.gate import GateReport
    from engine.io.enhance import Enhanced
    from engine.io.css_in import import_css
    from engine.io.report import Source
    text = ":root { --ink: #111111; }\n"
    imported = import_css(text, Source("t.css", "css", "0" * 64, len(text)))
    mapping = Mapping(roles={"color.text.default": RoleMap("ink", "owner"),
                             "color.surface.page": RoleMap("ink", "owner")})
    check = SystemCheck((), GateReport([], 0, [], 0, []), ("color",))
    result = Enhanced(imported, mapping, check, [], None, [], [], [])
    assert result.why_not_measured() == "no check applied to the mapped roles"
    assert result.markdown().count(
        "Not measured: the 2 mapped roles gave the gate no check to apply (see Structure and the "
        "decisions), so the gate had nothing to measure and nothing here passed.") == 1
