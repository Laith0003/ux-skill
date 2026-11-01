"""The Stageshow exporter: a system's roles as a Stageshow look, so a
product illustration made with the Stageshow kit wears the page's own
system. Each look token takes the role it stands for, in light and in dark;
the tokens the kit tunes to an illustration's scale (shadows, density, the
placeholder inks) stay the kit's. The look is unlayered, so it wins over
the kit's own themes, which sit in a cascade layer."""
import re

import pytest

from engine.foundations.build import build_system
from engine.foundations.errors import InputError
from engine.foundations.export import dump_dtcg, to_css
from engine.foundations.tokens import Token, TokenSet
from engine.io.commands import TARGETS, run_export
from engine.io.stageshow_out import KIT_OWNED, LOOK, LOOK_CLASS, to_stageshow
from engine.synthesizer.axes import AxisValues

NEUTRAL = AxisValues(*[0.5] * 7)
DARK = "scheme:dark"


def _ours():
    return build_system(NEUTRAL, "#3366FF").tokens


def _blocks(text):
    """The declarations of the light block and the dark block, by token."""
    out = {}
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", text):
        out[selector.strip()] = dict(re.findall(r"(--ss-[a-z0-9-]+):\s*([^;]+);", body))
    return out[f".{LOOK_CLASS} .ss-stage"], out[f'.{LOOK_CLASS} .ss-stage[data-theme="dark"]']


def test_every_look_token_takes_its_role_in_light_and_dark():
    ts = _ours()
    light, dark = _blocks(to_stageshow(ts))
    assert set(light) == set(dark) == {prop for prop, _ in LOOK}
    for prop, role in LOOK:
        if ts.get(role).type == "color":
            assert light[prop] == ts.resolve(role), prop
            assert dark[prop] == ts.resolve(role, DARK), prop


def test_the_surfaces_text_and_accent_follow_the_system():
    ts = _ours()
    light, dark = _blocks(to_stageshow(ts))
    assert light["--ss-canvas"] == ts.resolve("color.surface.page")
    assert dark["--ss-canvas"] == ts.resolve("color.surface.page", DARK)
    assert light["--ss-text-strong"] == ts.resolve("color.text.default")
    assert light["--ss-accent"] == ts.resolve("color.action.primary")
    assert light["--ss-danger-soft"] == ts.resolve("color.status.danger.soft")


def test_the_faces_and_radii_come_from_the_system():
    light, _ = _blocks(to_stageshow(_ours()))
    assert light["--ss-font"].startswith('"Noto Sans"')
    assert "Plex Mono" in light["--ss-mono"]
    assert light["--ss-radius-md"] == "7px"
    assert light["--ss-radius-window"] == "14px"


def test_what_the_kit_tunes_to_an_illustration_stays_the_kits():
    text = to_stageshow(_ours())
    for prop in KIT_OWNED:
        assert prop not in text, prop
    assert not any(prop in KIT_OWNED for prop, _ in LOOK)


def test_the_look_is_unlayered_so_it_wins_over_the_kits_themes():
    text = to_stageshow(_ours())
    assert "@layer" not in text
    assert f'className="{LOOK_CLASS}"' in text, "the file says how to use it"


def test_a_system_without_the_roles_names_each_missing_one_and_the_fix():
    ts = TokenSet()
    ts.add(Token("brand.blue", "color", "#3366FF"))
    with pytest.raises(InputError) as err:
        to_stageshow(ts)
    message = str(err.value)
    assert "color.surface.page" in message and "color.action.primary" in message
    assert "system build" in message


def test_export_writes_the_look_file(tmp_path):
    assert "stageshow" in TARGETS
    src = tmp_path / "tokens.json"
    src.write_text(dump_dtcg(_ours()), encoding="utf-8")
    result = run_export(src, to="stageshow", include_files=True)
    assert [f["name"] for f in result["files"]] == ["stageshow-look.css"]
    assert "--ss-accent:" in result["texts"]["stageshow-look.css"]


def test_a_stylesheet_ux_skill_wrote_exports_the_same_look(tmp_path):
    """Its roles come back with flat names (color-surface-page); the look
    finds each role by the CSS property it becomes."""
    ts = _ours()
    css = tmp_path / "tokens.css"
    css.write_text(to_css(ts), encoding="utf-8")
    result = run_export(css, to="stageshow", include_files=True)
    assert _blocks(result["texts"]["stageshow-look.css"]) == _blocks(to_stageshow(ts))


def test_the_look_rides_on_the_wrapper_the_stage_takes_its_class_on():
    """The kit puts a Stage's className on its .ss-fit wrapper, around the
    .ss-stage element, so the look selects the stage inside the class."""
    text = to_stageshow(_ours())
    assert f".{LOOK_CLASS} .ss-stage {{" in text
    assert f"class=\"{LOOK_CLASS}\"" not in text and f'className="{LOOK_CLASS}"' in text


def test_the_refusal_names_the_callers_own_fields():
    ts = TokenSet()
    ts.add(Token("brand.blue", "color", "#3366FF"))
    with pytest.raises(InputError) as err:
        to_stageshow(ts, labels={"to": "to", "build": "ux_system_build"})
    assert str(err.value).startswith("to stageshow reads") and "ux_system_build" in str(err.value)


def test_entries_the_import_left_out_are_listed_at_the_top(tmp_path):
    src = tmp_path / "theme.css"
    src.write_text(to_css(_ours()) + "\n.card { --card-glow: 0 0 4px red; }\n", encoding="utf-8")
    look = run_export(src, to="stageshow", include_files=True)["texts"]["stageshow-look.css"]
    assert "1 entry was not read" in look and "--card-glow" in look
    assert look.index("--card-glow") < look.index(".ux-look .ss-stage {")


def test_a_scheme_is_refused_since_the_stage_picks_its_own(tmp_path):
    src = tmp_path / "tokens.json"
    src.write_text(dump_dtcg(_ours()), encoding="utf-8")
    with pytest.raises(InputError) as err:
        run_export(src, to="stageshow", scheme="dark")
    assert str(err.value).startswith("--scheme does not apply to --to stageshow")
    assert 'theme="dark"' in str(err.value)
