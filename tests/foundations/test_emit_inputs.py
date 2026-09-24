"""Inputs for `uxskill system build` and `ux_system_build`: brand, axes and
brief. Every error names the input by the caller's label and says the fix."""
import json

import pytest

from engine.foundations.emit import (
    NEUTRAL, NEUTRAL_SOURCE, InputError, brief_axes, choose_axes, parse_axes, parse_brand,
    parse_latin_only, read_brief,
)
from engine.synthesizer.axes import AxisValues, compute_axes


@pytest.mark.parametrize("raw,expected", [
    ("#3366FF", "#3366FF"), ("#3366ff", "#3366FF"), ("3366ff", "#3366FF"),
    ("#36F", "#3366FF"), ("  #3366FF ", "#3366FF"),
])
def test_parse_brand_normalizes(raw, expected):
    assert parse_brand(raw) == expected


@pytest.mark.parametrize("raw", ["blue", "#12345", "#GGGGGG", ""])
def test_parse_brand_names_the_input_and_the_fix(raw):
    with pytest.raises(InputError) as exc:
        parse_brand(raw, label="--brand")
    message = str(exc.value)
    assert message.startswith("--brand ")
    assert "#3366FF" in message


def test_parse_brand_rejects_a_non_string():
    with pytest.raises(InputError, match="^brand is missing"):
        parse_brand(None)


def test_parse_axes_reads_a_string_and_a_list():
    expected = AxisValues(0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7)
    assert parse_axes("0.1,0.2,0.3,0.4,0.5,0.6,0.7") == expected
    assert parse_axes(" 0.1, 0.2 ,0.3,0.4,0.5,0.6,0.7 ") == expected
    assert parse_axes([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]) == expected
    assert parse_axes([0, 1, 0, 1, 0, 1, 0]) == AxisValues(0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0)


@pytest.mark.parametrize("raw,needle", [
    ("0.5,0.5", "--axes has 2 values; pass seven numbers"),
    ("0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5", "--axes has 8 values"),
    ("0.5,0.5,x,0.5,0.5,0.5,0.5", "--axes gives density as 'x'; set it to a number from 0 to 1"),
    ("0.5,0.5,0.5,1.5,0.5,0.5,0.5", "--axes gives geometry as '1.5'"),
    ("0.5,0.5,0.5,0.5,0.5,0.5,nan", "--axes gives type_personality as 'nan'"),
    ([0.5, 0.5, 0.5, 0.5, 0.5, True, 0.5], "--axes gives motion as True"),
    (7, "--axes is 7; pass seven numbers"),
])
def test_parse_axes_names_the_axis_and_the_fix(raw, needle):
    with pytest.raises(InputError) as exc:
        parse_axes(raw, label="--axes")
    assert needle in str(exc.value)


def test_parse_axes_error_lists_the_order():
    with pytest.raises(InputError) as exc:
        parse_axes("1")
    assert "warmth,contrast,density,geometry,formality,motion,type_personality" in str(exc.value)


def test_read_brief_flattens_a_discovery_file(tmp_path):
    f = tmp_path / "last-discovery.json"
    f.write_text(json.dumps({"answers": {"industry": "saas", "tone": "warm, calm"}}),
                 encoding="utf-8")
    assert read_brief(f) == {"industry": "saas", "tone": "warm, calm"}


def test_read_brief_errors_name_the_file_and_the_fix(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(InputError) as exc:
        read_brief(bad, label="--brief")
    assert str(exc.value).startswith(f"--brief {bad} is not valid JSON")
    assert '{"industry": "saas"' in str(exc.value)

    listed = tmp_path / "list.json"
    listed.write_text("[1, 2]", encoding="utf-8")
    with pytest.raises(InputError, match="holds a JSON list, not an object"):
        read_brief(listed, label="--brief")

    with pytest.raises(InputError, match="cannot be read"):
        read_brief(tmp_path / "missing.json", label="--brief")


def test_brief_axes_go_through_the_synthesizer():
    brief = {"industry": "fintech-banking", "tone": ["warm"], "stack": "react"}
    axes, source = brief_axes(brief)
    assert axes == compute_axes({"industry": "fintech-banking", "tone": ["warm"]})
    assert source == "from the brief (industry: fintech-banking; tone: warm)"


def test_brief_axes_read_a_discovery_brief_as_a_flat_one():
    nested = brief_axes({"answers": {"industry": "saas", "tone": ["warm"]}})
    assert nested == brief_axes({"industry": "saas", "tone": ["warm"]})


def test_brief_axes_split_comma_strings():
    axes, source = brief_axes({"tone": "warm, calm"})
    assert axes == compute_axes({"tone": ["warm", "calm"]})
    assert source == "from the brief (tone: warm, calm)"


def test_brief_without_any_field_is_refused():
    with pytest.raises(InputError) as exc:
        brief_axes({"stack": "react"}, label="--brief")
    assert str(exc.value).startswith(
        "--brief has none of industry, tone, audience, must_have, forbidden")
    assert "or pass axes instead" in str(exc.value)


def test_brief_field_of_the_wrong_shape_is_named():
    with pytest.raises(InputError, match='^brief field tone is 3; give a list of words'):
        brief_axes({"tone": 3})
    with pytest.raises(InputError, match="^brief field industry is"):
        brief_axes({"industry": ["saas"]})


def test_choose_axes_sources():
    assert choose_axes(None, None) == (NEUTRAL, NEUTRAL_SOURCE)
    axes, source = choose_axes(None, "0,0,0,0,0,0,0", axes_label="--axes")
    assert axes == AxisValues(0, 0, 0, 0, 0, 0, 0) and source == "set by hand (--axes)"
    axes, source = choose_axes({"industry": "saas"}, None)
    assert source.startswith("from the brief")


def test_choose_axes_refuses_both():
    with pytest.raises(InputError) as exc:
        choose_axes({"industry": "saas"}, "0.5,0.5,0.5,0.5,0.5,0.5,0.5",
                    brief_label="--brief", axes_label="--axes")
    assert str(exc.value).startswith("both --brief and --axes were given; pass one")


# A brief saved by Notepad (UTF-8 with a byte order mark) or by Windows
# PowerShell 5.1 (`echo ... > brief.json` writes UTF-16) reads as usual.
BRIEF = {"industry": "saas", "tone": ["warm"]}


@pytest.mark.parametrize("codec,prefix", [
    ("utf-8", b"\xef\xbb\xbf"), ("utf-16-le", b"\xff\xfe"), ("utf-16-be", b"\xfe\xff"),
])
def test_read_brief_accepts_a_marked_file(tmp_path, codec, prefix):
    f = tmp_path / "brief.json"
    f.write_bytes(prefix + json.dumps(BRIEF).encode(codec))
    assert read_brief(f) == BRIEF


def test_read_brief_that_is_not_utf8_names_the_file_and_the_fix(tmp_path):
    f = tmp_path / "latin1.json"
    f.write_bytes('{"industry": "caf\xe9"}'.encode("latin-1"))
    with pytest.raises(InputError) as exc:
        read_brief(f, label="--brief")
    message = str(exc.value)
    assert message == (f"--brief {f} is not UTF-8 text; save the brief as UTF-8 and pass it "
                       "again")
    for jargon in ("BOM", "codec", "decode", "encoding", "byte"):
        assert jargon not in message


def test_read_brief_names_json_types_not_python_ones(tmp_path):
    for text, word in (("null", "null"), ('"saas"', "string"), ("3", "number"),
                       ("[1]", "list"), ("true", "true or false")):
        f = tmp_path / "b.json"
        f.write_text(text, encoding="utf-8")
        with pytest.raises(InputError) as exc:
            read_brief(f, label="--brief")
        assert f"holds a JSON {word}, not an object" in str(exc.value)
        assert "NoneType" not in str(exc.value)


def test_read_brief_expands_a_home_folder(tmp_path, monkeypatch):
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))
    (tmp_path / "b.json").write_text(json.dumps(BRIEF), encoding="utf-8")
    assert read_brief("~/b.json") == BRIEF


# A brief word the synthesizer does not know moves no axis. The source line
# says which words were read and which were ignored, and a brief where no
# word was read is refused instead of silently building the neutral system.
from engine.synthesizer.axes import FORBIDDEN_CLAMPS, INDUSTRY_SEEDS, TONE_NUDGES  # noqa: E402


def test_unrecognized_words_are_named_in_the_source():
    axes, source = brief_axes({"industry": "saas", "tone": "warm, luxurious",
                               "audience": "small business owners"})
    assert axes == compute_axes({"industry": "saas", "tone": ["warm", "luxurious"],
                                 "audience": ["small business owners"]})
    assert source == ("from the brief (industry: saas; tone: warm); not recognized and "
                      "ignored: luxurious (tone), small business owners (audience)")


def test_an_industry_read_as_a_nearby_one_says_so():
    axes, source = brief_axes({"industry": "fintech"})
    assert axes == compute_axes({"industry": "fintech-payments"})
    assert source == "from the brief (industry: fintech, read as fintech-payments)"


def test_a_brief_that_leaves_every_axis_neutral_says_so():
    axes, source = brief_axes({"forbidden": ["loud"]})
    assert axes == NEUTRAL
    assert source == "from the brief (forbidden: loud), which leaves every axis at 0.5"


@pytest.mark.parametrize("brief,unknown,vocabulary", [
    ({"industry": "bakery"}, "bakery (industry)", INDUSTRY_SEEDS),
    ({"tone": "luxurious"}, "luxurious (tone)", TONE_NUDGES),
    ({"audience": "small business owners"}, "small business owners (audience)", TONE_NUDGES),
    ({"must_have": "dark mode"}, "dark mode (must_have)", TONE_NUDGES),
    ({"forbidden": ["neon"]}, "neon (forbidden)", FORBIDDEN_CLAMPS),
])
def test_a_brief_with_no_recognized_word_is_refused(brief, unknown, vocabulary):
    with pytest.raises(InputError) as exc:
        choose_axes(brief, None, brief_label="--brief", axes_label="--axes")
    message = str(exc.value)
    assert message.startswith("--brief has no word the engine recognizes, so it would build "
                              "the same system as no brief. Not recognized: " + unknown + ".")
    assert "Use at least one accepted word, or pass --axes instead." in message
    for word in vocabulary:
        assert word in message


def test_the_refusal_lists_a_shared_vocabulary_once():
    with pytest.raises(InputError) as exc:
        brief_axes({"industry": "bakery", "tone": "luxurious", "audience": "owners"})
    message = str(exc.value)
    assert "tone and audience accept: " in message and "industry accepts: " in message
    assert message.count("playful") == 1


def test_parse_axes_drops_the_sign_of_zero():
    axes = parse_axes("-0,0,0,0,0,0,0")
    assert axes.to_dict()["warmth"] == 0.0 and str(axes.warmth) == "0.0"


def test_latin_only_reads_only_true_or_false():
    assert parse_latin_only(None) is False
    assert parse_latin_only(False) is False and parse_latin_only(True) is True
    for junk in ("maybe", "true", 1, 0, [True]):
        with pytest.raises(InputError) as exc:
            parse_latin_only(junk, "latin_only")
        assert str(exc.value).startswith(f"latin_only is {junk!r}; pass true to leave out")
        assert "or false (the default) to keep them" in str(exc.value)
