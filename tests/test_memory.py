"""Meaningful pilot checks: invariants, executable labels, and leakage boundaries."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("merge_memory", ROOT / "src" / "merge_memory.py")
memory = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = memory
SPEC.loader.exec_module(memory)


def config():
    return memory.load_config(ROOT / "configs" / "pilot.json")


def test_two_hop_requires_both_parties_and_entity_names_vary():
    cfg = config()
    cfg["dataset"]["two_hop_probability"] = 1.0
    cfg["dataset"]["update_probability"] = 0.0
    cfg["dataset"]["missing_probability"] = 0.0
    rng = np.random.default_rng(17)
    answers = []
    for _ in range(60):
        episode = memory.make_episode(rng, cfg, "disjoint")
        assert memory.reference_answer(episode.facts_a, episode.query, 6)[0] == 6
        assert memory.reference_answer(episode.facts_b, episode.query, 6)[0] == 6
        assert memory.reference_answer(episode.facts_a + episode.facts_b, episode.query, 6)[0] == episode.target
        assert episode.target < 6
        answers.append(episode.target)
    assert len(set(answers)) == 6


def test_revision_overwrites_and_missing_is_unknown():
    facts = [(0, 0, 1, 0), (1, 1, 2, 0), (1, 1, 4, 1)]
    assert memory.reference_answer(facts, (0, 0, 1), 6) == (4, 1)
    assert memory.reference_answer(facts[:1], (0, 0, 1), 6) == (6, 1)
    assert memory.reference_answer([(0, 0, 1, 0), (0, 0, 3, 0)], (0, 0, -1), 6) == (6, 6)
    rng = np.random.default_rng(21)
    for _ in range(40):
        episode = memory.make_episode(rng, config(), "missing")
        assert episode.target == 6


def test_permutation_preserves_answers_under_renaming():
    facts = [(0, 0, 1, 0), (1, 1, 4, 0)]
    permutation = np.array([3, 0, 5, 1, 2, 4])
    transformed = memory.permute_facts(facts, permutation)
    assert memory.reference_answer(transformed, (3, 0, 1), 6) == (2, 0)


def test_empty_identity_fixed_bytes_and_event_order_invariance():
    cfg = config()
    memory.seed_everything(4)
    model = memory.LearnedMemory(cfg).eval()
    batch = memory.make_batch(np.random.default_rng(6), 7, cfg, "overlap")
    state = model.encode(batch["facts_a"], batch["mask_a"])
    reverse = model.encode(batch["facts_a"].flip(1), batch["mask_a"].flip(1))
    torch.testing.assert_close(state, reverse, atol=1e-6, rtol=1e-5)
    zero = model.encode(batch["facts_a"], torch.zeros_like(batch["mask_a"]))
    assert torch.count_nonzero(zero) == 0
    assert state.shape == (7, 12, 24)
    assert state[0].numel() * state.element_size() == model.state_bytes == 1152
    merger = memory.SymmetricMerger(24, 64)
    with torch.no_grad():
        merger.correction[-1].weight.normal_()
        merger.correction[-1].bias.normal_()
    torch.testing.assert_close(merger(state, zero), state, atol=0, rtol=0)
    torch.testing.assert_close(merger(zero, state), state, atol=0, rtol=0)


def test_symmetric_merge_and_max_algebra():
    torch.manual_seed(15)
    a, b, c = (torch.randn(9, 12, 24) for _ in range(3))
    merger = memory.SymmetricMerger(24, 64)
    with torch.no_grad():
        merger.correction[-1].weight.normal_()
    torch.testing.assert_close(merger(a, b), merger(b, a), atol=0, rtol=0)
    torch.testing.assert_close(torch.maximum(a, b), torch.maximum(b, a), atol=0, rtol=0)
    torch.testing.assert_close(torch.maximum(a, a), a, atol=0, rtol=0)
    torch.testing.assert_close(torch.maximum(torch.maximum(a, b), c), torch.maximum(a, torch.maximum(b, c)), atol=0, rtol=0)


def test_additive_disjoint_merge_and_max_overlap_merge_match_reencode():
    cfg = config()
    memory.seed_everything(31)
    model = memory.LearnedMemory(cfg).eval()
    for condition, pool in [("disjoint", "sum"), ("overlap", "max")]:
        batch = memory.make_batch(np.random.default_rng(44), 12, cfg, condition)
        a = model.encode(batch["facts_a"], batch["mask_a"], pool)
        b = model.encode(batch["facts_b"], batch["mask_b"], pool)
        full = model.encode(batch["full_facts"], batch["full_mask"], pool)
        combined = a + b if pool == "sum" else torch.maximum(a, b)
        torch.testing.assert_close(combined, full, atol=1e-6, rtol=1e-5)


def test_model_inference_has_no_label_or_reference_access():
    cfg = config()
    memory.seed_everything(19)
    model = memory.LearnedMemory(cfg).eval()
    merger = memory.SymmetricMerger(24, 64).eval()
    batch = memory.make_batch(np.random.default_rng(23), 5, cfg)
    a = model.encode(batch["facts_a"], batch["mask_a"])
    b = model.encode(batch["facts_b"], batch["mask_b"])
    before = model.read(merger(a, b), batch["queries"])
    batch["targets"].fill_(0)
    batch["intermediate_targets"].fill_(0)
    batch["full_facts"].fill_(0)
    batch["full_mask"].fill_(False)
    after = model.read(merger(a, b), batch["queries"])
    torch.testing.assert_close(before, after, atol=0, rtol=0)
    assert torch.isfinite(before).all()


def test_namespace_control_changes_evidence_but_preserves_original_labels():
    cfg = config()
    # Same random stream creates the same world and query before corruption.
    valid = memory.make_episode(np.random.default_rng(73), cfg, "namespace_mismatch")
    assert memory.reference_answer(valid.reference_facts, valid.query, 6)[0] == valid.target
    assert set(valid.facts_a + valid.facts_b) != set(valid.reference_facts)


def test_training_and_test_world_streams_are_separate_and_repeatable():
    cfg = config()
    train_a = memory.make_batch(np.random.default_rng(101), 10, cfg)
    train_b = memory.make_batch(np.random.default_rng(101), 10, cfg)
    test = memory.make_batch(np.random.default_rng(1000101), 10, cfg)
    assert torch.equal(train_a["facts_a"], train_b["facts_a"])
    assert torch.equal(train_a["targets"], train_b["targets"])
    assert not torch.equal(train_a["facts_a"], test["facts_a"])


def test_local_ambiguity_oracle_detects_constant_relation_exception():
    complete_constant = [(s, 1, 2, 0) for s in range(6)]
    assert memory.possible_answers(complete_constant, (0, 0, 1), 6) == {2}
    assert memory.possible_answers(complete_constant[:-1], (0, 0, 1), 6) == set(range(6))
    assert memory.possible_answers([(0, 0, 1, 0)], (0, 0, 1), 6) == set(range(6))


def test_four_query_world_has_shared_context_and_validated_private_ambiguity():
    cfg = config()
    rng = np.random.default_rng(55)
    known_count, unknown_count = 0, 0
    for _ in range(50):
        world = memory.make_query_world(rng, cfg, 0.5)
        assert len(world) == 4
        assert len({episode.query for episode in world}) == 4
        assert [episode.query[2] < 0 for episode in world] == [True, True, False, False]
        assert all(episode.facts_a == world[0].facts_a for episode in world)
        assert all(episode.facts_b == world[0].facts_b for episode in world)
        for episode in world:
            assert memory.reference_answer(episode.reference_facts, episode.query, 6)[0] == episode.target
            if episode.query[2] >= 0 and episode.target < 6:
                assert len(memory.possible_answers(episode.facts_a, episode.query, 6)) >= 2
                assert len(memory.possible_answers(episode.facts_b, episode.query, 6)) >= 2
                known_count += 1
            unknown_count += episode.target == 6
    assert known_count > 20
    assert unknown_count > 20


def test_deepsets_is_symmetric_same_state_size_and_parameter_count_is_disclosed():
    torch.manual_seed(5)
    candidate = memory.SymmetricMerger(24, 64)
    baseline = memory.DeepSetsMerger(24, 64)
    a, b = torch.randn(3, 12, 24), torch.randn(3, 12, 24)
    torch.testing.assert_close(baseline(a, b), baseline(b, a), atol=0, rtol=0)
    assert baseline(a, b).shape == candidate(a, b).shape == a.shape
    assert sum(p.numel() for p in candidate.parameters()) == 6232
    assert sum(p.numel() for p in baseline.parameters()) == 6320


def test_primary_bootstrap_uses_world_macro_not_query_micro():
    cfg = config()
    rows = []
    for seed in cfg["training"]["seeds"]:
        # World0 has one eligible query and delta1; world1 has two and delta0.
        # Correct worldmacro delta is0.5, whereas querymicro would be1/3.
        for world, main_outcomes in [(0, [True]), (1, [False, False])]:
            for query_id, outcome in enumerate(main_outcomes):
                for method, correct in [("learned", outcome), ("max", False)]:
                    rows.append({"seed": seed, "stratum": "overlap_0.5", "world_id": world,
                                 "query_id": query_id, "method": method, "hops": 2,
                                 "known": True, "correct": correct})
    result = memory.primary_bootstrap(rows, cfg)
    assert result["difference"] == 0.5
    assert all(fit["worlds"] == 2 for fit in result["fits"])


def test_swapped_b_world_rotation_keeps_four_queries_together_and_avoids_self_donors():
    states = torch.arange(3).repeat_interleave(4).view(12, 1, 1).float()
    donors = torch.roll(states, 4, 0)
    assert donors[:, 0, 0].tolist() == [2.0] * 4 + [0.0] * 4 + [1.0] * 4
    assert torch.all(states != donors)


def test_evaluator_prediction_schema_and_control_provenance_without_training():
    cfg = config()
    cfg["evaluation"]["worlds_per_condition"] = 2
    cfg["evaluation"]["batch_size"] = 8
    memory.seed_everything(83)
    model = memory.LearnedMemory(cfg).eval()
    merger = memory.SymmetricMerger(24, 64).eval()
    baseline = memory.DeepSetsMerger(24, 64).eval()
    report, rows = memory.evaluate(model, merger, cfg, 11, True, baseline)
    assert len(rows) == 2 * 4 * 3 * len(cfg["evaluation"]["methods"])
    assert set(report["conditions"]) == set(cfg["evaluation"]["conditions"])
    swapped = [row for row in rows if row["method"] == "swapped_B"]
    assert all(row["donor_world_id"] != row["world_id"] for row in swapped)
    assert all(len(__import__("json").loads(row["probabilities"])) == 7 for row in rows)


def test_merger_loss_backpropagates_without_changing_frozen_backbone():
    cfg = config()
    memory.seed_everything(91)
    model = memory.LearnedMemory(cfg).eval()
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    batch = memory.make_batch(np.random.default_rng(93), 8, cfg)
    a = model.encode(batch["facts_a"], batch["mask_a"])
    b = model.encode(batch["facts_b"], batch["mask_b"])
    for cls in (memory.SymmetricMerger, memory.DeepSetsMerger):
        merger = cls(24, 64)
        loss = memory._loss(model, merger(a, b), batch, 0.3)
        loss.backward()
        assert any(parameter.grad is not None and torch.count_nonzero(parameter.grad) > 0
                   for parameter in merger.parameters())
        assert all(parameter.grad is None for parameter in model.parameters())
