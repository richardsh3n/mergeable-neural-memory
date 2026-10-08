import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.theory import exact_merge_table


def test_additive_collision_prevents_exact_union_merge():
    weights = {"a": 1, "b": 2, "c": 3}
    encoder = lambda events: sum(weights[e] for e in events)
    assert encoder({"c"}) == encoder({"a", "b"})
    assert encoder({"c", "a"}) != encoder({"a", "b"})
    with pytest.raises(ValueError):
        exact_merge_table(encoder, weights)


def test_max_is_an_exact_union_homomorphism():
    weights = {"a": 1, "b": 2, "c": 3}
    encoder = lambda events: max([0] + [weights[e] for e in events])
    table = exact_merge_table(encoder, weights)
    for (a, b), value in table.items():
        assert value == max(a, b)


def test_exact_merge_does_not_imply_informative_memory():
    assert exact_merge_table(lambda events: 0, ["a", "b"]) == {(0, 0): 0}
