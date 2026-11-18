"""Read-only continuation and delivery challenges on archived neural fits."""
from __future__ import annotations

from collections import Counter
from functools import partial

import numpy as np
import torch

from src.merge_memory import DeepSetsMerger, LearnedMemory, SymmetricMerger, merge_state
from .metrics import (ordered_trees, predict, relative_l2, ridge_predict, score,
                      state_comparison, verify_payload)
from .worlds import batch_worlds, collate_facts, draw_world


def load_fit(root, seed):
    saved = torch.load(root / "results/pilot" / f"checkpoint-seed-{seed}.pt",
                       map_location="cpu", weights_only=True)
    config = saved["config"]
    dims = config["architecture"]
    models = (LearnedMemory(config), SymmetricMerger(dims["state_dim"], dims["hidden_dim"]),
              DeepSetsMerger(dims["state_dim"], dims["hidden_dim"]))
    for model, key in zip(models, ("model", "merger", "deepsets")):
        model.float().eval()
        model.load_state_dict(saved[key])
    return models


def continuation_pairs(rng, n, count):
    for u in range(n):
        for r2 in range(2):
            for _ in range(count):
                s = int(rng.integers(n))
                r1 = 1 - r2
                bridge = (s, r1, u, 0)
                replacement = rng.choice(n, 2, replace=False).tolist()
                objects = rng.integers(n, size=(n, 2))
                facts = [(a, r, int(objects[a, r]), 0) for a in range(n) for r in range(2)
                         if (a, r) != bridge[:2]]
                variants = [[(a, r, new if (a, r) == (u, r2) else b, rev)
                             for a, r, b, rev in facts] for new in replacement]
                yield {"key": (u, r2), "query": (s, r1, r2), "bridge": bridge,
                       "variants": variants, "targets": replacement}


@torch.no_grad()
def continuation(fits, config, emit):
    n = fits[0][1][0].n_entities
    train_count = config["train_pairs_per_key"]
    test_count = config["test_pairs_per_key"]
    train = list(continuation_pairs(np.random.default_rng(config["probe_train_seed"]), n, train_count))
    test = list(continuation_pairs(np.random.default_rng(config["evaluation_seed"]), n, test_count))
    train_facts = collate_facts([facts for pair in train for facts in pair["variants"]])
    test_facts = collate_facts([facts for pair in test for facts in pair["variants"]])
    full_facts = collate_facts([sorted(facts + [pair["bridge"]]) for pair in test
                                for facts in pair["variants"]])
    bridges = collate_facts([[pair["bridge"]] for pair in test for _ in pair["variants"]])
    direct_queries = torch.tensor([(*pair["key"], -1) for pair in test for _ in pair["variants"]])
    joint_queries = torch.tensor([pair["query"] for pair in test for _ in pair["variants"]])
    train_labels = np.array([target for pair in train for target in pair["targets"]])
    targets = torch.tensor([pair["targets"] for pair in test])
    keys = 2 * n
    control_rng = np.random.default_rng(config["control_seed"])
    controls = np.concatenate([control_rng.permutation(group) for group in np.split(train_labels, keys)])
    for i, pair in enumerate(test):
        emit({"section": "continuation_world", "id": i, **pair})

    output = {}
    for seed, (model, _, _) in fits:
        for pool in ("sum", "max"):
            train_state = model.encode(*train_facts, pool)
            local = model.encode(*test_facts, pool)
            bridge_state = model.encode(*bridges, pool)
            merged = local + bridge_state if pool == "sum" else torch.maximum(local, bridge_state)
            replay_state = model.encode(*full_facts, pool)
            for state in (train_state, local, bridge_state, merged, replay_state):
                verify_payload(state, model)
            torch.testing.assert_close(merged, replay_state, rtol=1e-5, atol=1e-6)
            learn_rows = np.split(train_state.flatten(1).numpy(), keys)
            held_rows = np.split(local.flatten(1).numpy(), keys)
            labels = np.split(train_labels, keys)
            shuffled = np.split(controls, keys)

            def probe(probe_labels):
                return torch.from_numpy(np.concatenate([
                    ridge_predict(x, y, test_x, n, config["ridge_penalty"])
                    for x, y, test_x in zip(learn_rows, probe_labels, held_rows)
                ])).reshape(keys * test_count, 2)

            predictions = {
                "probe": probe(labels), "shuffled_probe": probe(shuffled),
                "native_direct": model.read(local, direct_queries).argmax(-1).reshape(-1, 2),
                "native_local": model.read(local, joint_queries).argmax(-1).reshape(-1, 2),
                "native_merged": model.read(merged, joint_queries).argmax(-1).reshape(-1, 2),
                "native_full": model.read(replay_state, joint_queries).argmax(-1).reshape(-1, 2),
            }
            left, right = local[::2], local[1::2]
            same = (left == right).flatten(1).all(dim=1)
            distance = relative_l2(right, left)
            output[f"{seed}/{pool}"] = {
                "pairs": len(test), "exact_collision_pairs": int(same.sum()),
                "collision_accuracy_ceiling_on_this_corpus": 1.0 - int(same.sum()) / (2 * len(test)),
                "median_relative_l2": float(np.median(distance.numpy())),
                "accuracy": {name: float((values == (n if name == "native_local" else targets)).double().mean())
                             for name, values in predictions.items()},
            }
            for i in range(len(test)):
                emit({"section": "continuation_predictions", "seed": seed, "pool": pool, "id": i,
                      "exact_collision": bool(same[i]), "relative_l2": float(distance[i]),
                      "predictions": {name: values[i].tolist() for name, values in predictions.items()}})
    return output


@torch.no_grad()
def three_party(fits, config, emit):
    n = fits[0][1][0].n_entities
    output = {}
    for ci, overlap in enumerate(config["overlap_levels"]):
        rng = np.random.default_rng(config["evaluation_seed"] + ci)
        attempts = Counter()
        worlds = [draw_world(rng, n, 2, overlap, attempts, party_count=3)
                  for _ in range(config["worlds_per_condition"])]
        for i, world in enumerate(worlds):
            emit({"section": "three_party_world", "overlap": overlap, "id": i, **vars(world)})
        batch = batch_worlds(worlds)
        duplicated = collate_facts([w.parties[0] + w.parties[0] for w in worlds])
        methods = {}
        for seed, (model, learned, deepsets) in fits:
            for method in ("learned", "deepsets", "sum", "mean", "max"):
                pool = "max" if method == "max" else "sum"
                merge = partial(merge_state, method, merger=learned, deepsets=deepsets)
                a, b, c = states = [model.encode(*facts, pool) for facts in batch["parties"]]
                reference = model.encode(*batch["union"], pool)
                canonical = merge(merge(a, b), c)
                canonical_pred = predict(model, canonical, batch)
                ab = merge(a, b)
                compare = {
                    "swap_ab": (merge(b, a), ab),
                    "self_a": (merge(a, a), a),
                    "self_b": (merge(b, b), b),
                    "self_c": (merge(c, c), c),
                    "self_merged": (merge(canonical, canonical), canonical),
                    "duplicate_a_events": (merge(merge(model.encode(*duplicated, pool), b), c), canonical),
                }
                for name, state in ordered_trees(merge, states):
                    compare[name] = (state, canonical)
                acc = canonical
                for k in range(1, max(config["redeliveries"]) + 1):
                    acc = merge(acc, a)
                    if k in config["redeliveries"]:
                        compare[f"redeliver_a_{k}"] = (acc, canonical)
                compare["full_reencode"] = (reference, canonical)
                for state in [*states, reference, canonical, ab]:
                    verify_payload(state, model)
                if method == "max":
                    torch.testing.assert_close(canonical, reference, rtol=0, atol=0)
                elif method == "sum" and overlap == 0:
                    torch.testing.assert_close(canonical, reference, rtol=1e-5, atol=1e-6)

                results = {}
                for name, (state, baseline) in compare.items():
                    verify_payload(state, model)
                    predicted = predict(model, state, batch)
                    original = canonical_pred if baseline is canonical else predict(model, baseline, batch)
                    results[name] = {
                        **state_comparison(state, baseline), **score(predicted, batch, n),
                        "answer_agreement_with_comparison_state": float((predicted == original).double().mean()),
                    }
                    emit({"section": "three_party_predictions", "overlap": overlap, "seed": seed,
                          "method": method, "variant": name, "predictions_in_world_id_order": predicted.tolist()})
                methods[f"{seed}/{method}"] = results
        output[str(overlap)] = {"generation": dict(attempts), "methods": methods}
    return output
