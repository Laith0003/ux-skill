"""The loop finder the importers share."""
from engine.io.graph import cycles


def test_each_node_on_a_loop_gets_its_loop_and_nothing_else_does():
    refs = {"a": ["b"], "b": ["c"], "c": ["a"], "d": ["a"], "e": ["e"], "f": []}
    loops = cycles(list(refs), lambda n: refs[n])
    assert loops == {"a": ["a", "b", "c", "a"], "b": ["b", "c", "a", "b"],
                     "c": ["c", "a", "b", "c"], "e": ["e", "e"]}


def test_the_dtcg_importer_uses_the_shared_finder():
    import engine.io.dtcg_in

    assert engine.io.dtcg_in.cycles is cycles and not hasattr(engine.io.dtcg_in, "_cycles")
