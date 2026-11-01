"""An imported axis whose base is what :root holds (density: base,
comfortable, compact) is never mapped by name: the owner maps it by hand,
and every step says so. It survives the engine's own DTCG file. Every
stylesheet here is invented."""
import pytest

from engine.foundations.errors import InputError
from engine.foundations.export import dump_dtcg
from engine.io.adapter import AxisMap, Mapping, propose, view
from engine.io.css_in import import_css
from engine.io.dtcg_in import import_dtcg
from engine.io.report import Source

ROOT = ":root {\n  --row: 44px;\n  --gap: 8px;\n}\n"
COMFORTABLE = '[data-density="comfortable"] {\n  --row: 52px;\n  --gap: 10px;\n}\n'
COMPACT = '[data-density="compact"] {\n  --row: 36px;\n  --gap: 6px;\n}\n'


def _css(text):
    return import_css(text, Source("theme.css", "css", "0" * 64, len(text)))


@pytest.mark.parametrize("text, values", [
    (ROOT + COMFORTABLE, ("base", "comfortable")),
    (ROOT + COMFORTABLE + COMPACT, ("base", "comfortable", "compact")),
], ids=["one-mode", "two-modes"])
def test_a_root_based_axis_is_never_mapped_by_name(text, values):
    ts = _css(text).tokens
    assert dict(ts.axes) == {"density": values}
    mapping = propose(ts)
    assert "density" not in mapping.axes
    _, notes = view(ts, mapping)
    listed = " and ".join(values) if len(values) == 2 else "base, comfortable and compact"
    choice = f"<one of {listed}>"
    assert (f"the axis density of the imported system ({listed}) has what :root holds as its "
            "base, not a named value, so it was not mapped and is not checked; to check it, "
            f'write in the mapping "density": {{"from": "density", "values": {{"comfortable": '
            f'"{choice}", "compact": "{choice}"}}, "by": "owner"}}') in notes


def test_the_owners_mapping_of_a_root_based_axis_is_read():
    ts = _css(ROOT + COMFORTABLE + COMPACT).tokens
    mapping = Mapping({}, {"density": AxisMap("density", {"comfortable": "base",
                                                          "compact": "compact"})})
    _, notes = view(ts, mapping)
    assert not any("has what :root holds as its base" in n for n in notes)


def test_a_value_the_axis_lacks_is_refused_with_every_value_named():
    ts = _css(ROOT + COMFORTABLE + COMPACT).tokens
    mapping = Mapping({}, {"density": AxisMap("density", {"comfortable": "base",
                                                          "compact": "tight"})})
    with pytest.raises(InputError, match="density has the values base, comfortable and "
                                         "compact; use those"):
        view(ts, mapping)


def test_the_engines_own_dtcg_of_a_root_based_axis_reads_back():
    ts = _css(ROOT + COMFORTABLE + COMPACT).tokens
    text = dump_dtcg(ts)
    back = import_dtcg(text, Source("tokens.json", "dtcg", "0" * 64, len(text)))
    assert dict(back.tokens.axes) == {"density": ("base", "comfortable", "compact")}
    assert back.tokens.resolve("row", "density:compact") == {"value": 36, "unit": "px"}


def test_one_named_value_is_worded_as_one_mode():
    imported = _css(ROOT + COMFORTABLE)
    [note] = imported.report.notes
    assert note.message.endswith("with :root as its base and comfortable as its mode")
    assert ("Modes: density (the values set with no mode are the base; mode comfortable)."
            in imported.report.markdown())
