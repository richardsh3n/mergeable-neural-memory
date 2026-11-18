from collections import Counter

import numpy as np
import pytest
import torch

from experiments.followup.archived import continuation_pairs
from experiments.followup.metrics import ordered_trees, score, verify_payload
from experiments.followup.packed_table import PackedTable
from experiments.followup.run import ROOT, verify_archive
from experiments.followup.worlds import batch_worlds, collate_facts, draw_world
from src.merge_memory import LearnedMemory, possible_answers, reference_answer
from src.run_io import reserve_output


@pytest.fixture(scope="module")
def pilot():
    torch.set_num_threads(1)
    return verify_archive()[0]


@pytest.mark.parametrize("overlap", [0.0, 0.5])
def test_real_third_party_critical_evidence_and_all_trees(pilot, overlap):
    attempts = Counter()
    rng = np.random.default_rng(912)
    worlds = [draw_world(rng, 6, 2, overlap, attempts, 3) for _ in range(20)]
    assert attempts["accepted"] == len(worlds)
    for world in worlds:
        for target, query, path, pair in zip(world.targets, world.queries, world.paths,
                                             [(0, 1), (1, 2), (2, 0)]):
            assert target < 6
            for key, owner in zip(path, pair):
                assert [i for i, party in enumerate(world.parties)
                        if key in {f[:2] for f in party}] == [owner]
                reduced = [fact for i, party in enumerate(world.parties) if i != owner for fact in party]
                assert len(possible_answers(reduced, query, 6)) >= 2
    model = LearnedMemory(pilot).float().eval()
    batch = batch_worlds(worlds)
    with torch.no_grad():
        states = [model.encode(*facts, "max") for facts in batch["parties"]]
        reencode = model.encode(*batch["union"], "max")
        trees = dict(ordered_trees(torch.maximum, states))
        assert len(trees) == 12
        for state in trees.values():
            verify_payload(state, model)
            torch.testing.assert_close(state, reencode, rtol=1e-5, atol=1e-6)
            for delivery in (states[0], state):
                torch.testing.assert_close(torch.maximum(state, delivery), state, rtol=0, atol=0)


def test_counterfactual_changes_only_future_answer():
    pairs = list(continuation_pairs(np.random.default_rng(947), 6, 2))
    assert len(pairs) == 24
    for pair in pairs:
        a, b = pair["variants"]
        assert {f[:2] for f in set(a) ^ set(b)} == {pair["key"]}
        assert all(reference_answer(facts, pair["query"], 6)[0] == 6 for facts in (a, b))
        assert [reference_answer(facts + [pair["bridge"]], pair["query"], 6)[0]
                for facts in (a, b)] == pair["targets"]
        assert len(set(pair["targets"])) == 2


def test_world_macro_averages_queries_before_worlds():
    batch = {"queries_per_world": 2,
             "queries": torch.tensor([[0, 0, 1]] * 4),
             "targets": torch.tensor([0, 6, 0, 1])}
    row = score(torch.tensor([[1, 6], [0, 1]]), batch, 6)
    assert row["known_two_hop_world_macro_accuracy"] == 0.5
    assert row["known_two_hop_queries"] == 3
    assert row["unknown_recall"] == 1.0


def test_packed_table_is_fixed_byte_and_truncates_by_key_only():
    table = PackedTable(12, 8, 32)
    assert table.key_count == 64
    a, b = table.encode([(0, 0, 1, 0), (9, 0, 4, 0)]), table.encode([(1, 7, 3, 0)])
    assert len(a) == len(b) == len(table.merge(a, b)) == 32
    assert table.merge(a, a) == a
    assert table.merge(a, b) == table.merge(b, a)
    assert table.read(table.merge(a, b), [(0, 0, 7), (9, 0, -1)]) == [3, 12]
    with pytest.raises(ValueError, match="Contradictory"):
        table.merge(a, table.encode([(0, 0, 2, 0)]))


def test_actual_dtype_and_empty_histories(pilot):
    model = LearnedMemory(pilot).float()
    facts = collate_facts([[], []])
    for pool in ("sum", "max"):
        state = model.encode(*facts, pool)
        verify_payload(state, model)
        assert not bool(state.any())
        with pytest.raises(ValueError, match="float32"):
            verify_payload(state.double(), model)


def test_output_reservation_keeps_archive_and_existing_runs_safe(tmp_path):
    (tmp_path / "results").mkdir()
    with pytest.raises(ValueError, match="archived"):
        reserve_output(tmp_path / "results" / "pilot", tmp_path)
    target = tmp_path / "fresh"
    assert reserve_output(target, tmp_path) == target
    with pytest.raises(FileExistsError):
        reserve_output(target, tmp_path)
    alias = tmp_path / "alias"
    alias.symlink_to(tmp_path / "results", target_is_directory=True)
    with pytest.raises(ValueError, match="archived"):
        reserve_output(alias / "nested", tmp_path)
    assert not (tmp_path / "results" / "nested").exists()


def test_reproduce_entry_point_protects_frozen_results():
    import subprocess
    import sys

    result = subprocess.run([sys.executable, str(ROOT / "scripts/reproduce_pilot.py"),
                             "--out", str(ROOT / "results/pilot")], capture_output=True, text=True)
    assert result.returncode != 0
    assert "archived results tree" in result.stderr
