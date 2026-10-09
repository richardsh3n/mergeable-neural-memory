"""Run the frozen v0.2 writer-supervision diagnostic.

This script reuses the frozen v0.1 model and oracle, but owns a counted copy of
the query-world sampler so rejected attempts are observable without editing v0.1.
"""
from __future__ import annotations

import copy
import gzip
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.merge_memory import (  # noqa: E402
    Episode, LearnedMemory, batch_episodes, canonicalize, load_config,
    pad_facts, possible_answers, reference_answer, seed_everything,
)

HERE = Path(__file__).resolve().parent
CHECKPOINTS = ROOT / "results" / "pilot"


def counted_world(rng: np.random.Generator, config: dict, overlap: float):
    """v0.1 make_query_world law, with retry count returned for audit."""
    cfg = config["dataset"]
    n = int(cfg["n_entities"])
    keys = [(s, r) for s in range(n) for r in range(2)]
    for attempt in range(1, 1001):
        world = rng.integers(n, size=(2, n))
        two_keys = [keys[i] for i in rng.choice(len(keys), 2, replace=False)]
        one_keys = [keys[i] for i in rng.choice(len(keys), 2, replace=False)]
        queries = [(s, r, -1) for s, r in one_keys] + [(s, r, 1-r) for s, r in two_keys]
        paths = [((s, r),) if r2 < 0 else ((s, r), (int(world[r, s]), r2))
                 for s, r, r2 in queries]
        critical = set(edge for path in paths[2:] for edge in path)
        keep = set(edge for path in paths for edge in path)
        missing = set()
        for path in paths:
            if rng.random() < float(config["evaluation"]["missing_probability"]):
                missing.add(path[int(rng.integers(len(path)))])
        flip = int(rng.integers(2))
        a, b = [], []
        for s, r in keys:
            if (s, r) in missing:
                continue
            if (s, r) not in keep and rng.random() > float(cfg["distractor_retention_probability"]):
                continue
            fact = (s, r, int(world[r, s]), 0)
            owner = (r + flip) % 2 if (s, r) in critical else (
                2 if rng.random() < overlap else int(rng.integers(2)))
            if owner in (0, 2):
                a.append(fact)
            if owner in (1, 2):
                b.append(fact)
        if cfg.get("permute_entities_per_episode", True):
            permutation = rng.permutation(n)
            a = [(int(permutation[s]), r, int(permutation[o]), rev) for s, r, o, rev in a]
            b = [(int(permutation[s]), r, int(permutation[o]), rev) for s, r, o, rev in b]
            queries = [(int(permutation[s]), r, r2) for s, r, r2 in queries]
            paths = [tuple((int(permutation[s]), r) for s, r in path) for path in paths]
        reference = canonicalize(a + b)
        answers = [reference_answer(reference, q, n) for q in queries]
        if any(t < n and (len(possible_answers(a, q, n)) < 2 or
                          len(possible_answers(b, q, n)) < 2)
               for q, (t, _) in zip(queries[2:], answers[2:])):
            continue
        rng.shuffle(a)
        rng.shuffle(b)
        episodes = [Episode(list(a), list(b), reference, q, t, m, path,
                             f"overlap_{overlap}")
                    for q, (t, m), path in zip(queries, answers, paths)]
        return episodes, attempt
    raise RuntimeError("Unable to sample an ambiguity-validated world in 1000 attempts.")


def sampler_self_check(config):
    """Compare counted and frozen samplers exactly on fixed seeds/strata."""
    from src.merge_memory import make_query_world
    for overlap in (0.0, 0.25, 0.5):
        for seed in (71, 20261010):
            a = np.random.default_rng(seed)
            b = np.random.default_rng(seed)
            counted, _ = counted_world(a, config, overlap)
            original = make_query_world(b, config, overlap)
            def canonical(episodes):
                return [(e.facts_a, e.facts_b, e.query, e.target, e.intermediate, e.required_edges)
                        for e in episodes]
            assert canonical(counted) == canonical(original), (seed, overlap)


def writer_parameters(model):
    names = ("event_key", "event_value")
    params = [p for name, p in model.named_parameters()
              if name == "slot_keys" or name.startswith(names)]
    for name, p in model.named_parameters():
        p.requires_grad_(name == "slot_keys" or name.startswith(names))
    return params


def local_targets(episodes, field, n):
    result = []
    for ep in episodes:
        facts = ep.facts_a if field == "a" else ep.facts_b
        answer, middle = reference_answer(facts, ep.query, n)
        result.append((answer, middle))
    return result


def train_arm(seed, arm, config):
    seed_everything(910000 + seed, 1)
    ckpt = torch.load(CHECKPOINTS / f"checkpoint-seed-{seed}.pt", map_location="cpu", weights_only=True)
    model = LearnedMemory(ckpt["config"])
    model.load_state_dict(ckpt["model"])
    initial = {k: v.detach().clone() for k, v in model.state_dict().items()}
    parameters = writer_parameters(model)
    optim = torch.optim.AdamW(parameters, lr=config["learning_rate"],
                              weight_decay=config["weight_decay"])
    data_rng = np.random.default_rng(config["training_seed_offset"] + seed * 10000)
    step_hashes, step_attempts, trace = [], [], []
    model.train()
    started = time.time()
    for step in range(config["steps"]):
        worlds, attempts = [], []
        for _ in range(config["worlds_per_training_step"]):
            world, count = counted_world(data_rng, ckpt["config"], config["training_overlap"])
            worlds.append(world)
            attempts.append(count)
        episodes = [ep for world in worlds for ep in world]
        digest_payload = [[ep.facts_a, ep.facts_b, ep.query, ep.target, ep.intermediate]
                          for ep in episodes]
        step_hashes.append(hashlib.sha256(json.dumps(digest_payload, separators=(",", ":")).encode()).hexdigest())
        step_attempts.append(sum(attempts))
        batch = batch_episodes(episodes, ckpt["config"])
        n = model.n_entities
        targets_a = local_targets(episodes, "a", n)
        targets_b = local_targets(episodes, "b", n)
        ta = torch.tensor([x[0] for x in targets_a]); ma = torch.tensor([x[1] for x in targets_a])
        tb = torch.tensor([x[0] for x in targets_b]); mb = torch.tensor([x[1] for x in targets_b])
        state_a = model.encode(batch["facts_a"], batch["mask_a"], "max")
        state_b = model.encode(batch["facts_b"], batch["mask_b"], "max")
        union_state = torch.maximum(state_a, state_b)
        logits_a, first_a = model.read(state_a, batch["queries"], return_intermediate=True)
        logits_b, first_b = model.read(state_b, batch["queries"], return_intermediate=True)
        logits_u, first_u = model.read(union_state, batch["queries"], return_intermediate=True)
        local_loss = (F.cross_entropy(logits_a, ta) + .3 * F.cross_entropy(first_a, ma) +
                      F.cross_entropy(logits_b, tb) + .3 * F.cross_entropy(first_b, mb)) / 2
        union_loss = (F.cross_entropy(logits_u, batch["targets"]) +
                      .3 * F.cross_entropy(first_u, batch["intermediate_targets"]))
        loss = local_loss if arm == "local" else .5 * local_loss + .5 * union_loss
        optim.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.0)
        optim.step()
        if (step + 1) % config["log_every"] == 0:
            rec = {"seed": seed, "arm": arm, "step": step + 1,
                   "local_loss": float(local_loss.detach()), "union_loss": float(union_loss.detach()),
                   "elapsed_seconds": time.time() - started}
            trace.append(rec)
            print(json.dumps(rec), flush=True)
    model.eval()
    final = model.state_dict()
    frozen_equal = all(torch.equal(initial[k], final[k]) for k in initial if not (
        k == "slot_keys" or k.startswith("event_key") or k.startswith("event_value")))
    assert frozen_equal, "A reader or shared embedding changed despite freeze."
    path = HERE / f"writer-{arm}-seed-{seed}.pt"
    torch.save({"model": final, "seed": seed, "arm": arm, "parent": ckpt["selection_rule"],
                "state_bytes": model.state_bytes}, path)
    return model, trace, step_hashes, step_attempts


def make_test_data(config, source_config):
    all_worlds = []
    counts = {}
    for si, overlap in enumerate(config["overlaps"]):
        rng = np.random.default_rng(config["test_seed"] + si * 10000)
        worlds, attempts = [], []
        for wid in range(config["worlds_per_stratum"]):
            eps, n_attempts = counted_world(rng, source_config, overlap)
            worlds.append(eps)
            attempts.append(n_attempts)
        all_worlds.append(worlds)
        counts[str(overlap)] = {"accepted_worlds": len(worlds), "attempted_worlds": int(sum(attempts)),
                                "rejections": int(sum(attempts) - len(attempts)),
                                "attempts_per_world_max": int(max(attempts))}
    serial = []
    for si, worlds in enumerate(all_worlds):
        for wid, eps in enumerate(worlds):
            for qi, ep in enumerate(eps):
                local_a, local_a_mid = reference_answer(ep.facts_a, ep.query,
                                                        int(source_config["dataset"]["n_entities"]))
                local_b, local_b_mid = reference_answer(ep.facts_b, ep.query,
                                                        int(source_config["dataset"]["n_entities"]))
                serial.append({"stratum": si, "world_id": wid, "query_id": qi,
                               "facts_a": ep.facts_a, "facts_b": ep.facts_b,
                               "union_facts": ep.reference_facts, "query": ep.query,
                               "target": ep.target, "intermediate": ep.intermediate,
                               "local_a_target": local_a, "local_a_intermediate": local_a_mid,
                               "local_b_target": local_b, "local_b_intermediate": local_b_mid,
                               "required_edges": ep.required_edges})
    with gzip.open(HERE / "heldout-corpus.json.gz", "wt", encoding="utf-8") as f:
        json.dump(serial, f, separators=(",", ":"))
    return all_worlds, counts


@torch.no_grad()
def eval_arm(model, worlds, overlap_values):
    rows = []
    for si, worlds_in_stratum in enumerate(worlds):
        b_states = []
        for prior_eps in worlds_in_stratum:
            prior_batch = batch_episodes(prior_eps, model_config)
            b_states.append(model.encode(prior_batch["facts_b"], prior_batch["mask_b"], "max"))
        for wid, episodes in enumerate(worlds_in_stratum):
            batch = batch_episodes(episodes, model_config)
            sa = model.encode(batch["facts_a"], batch["mask_a"], "max")
            sb = model.encode(batch["facts_b"], batch["mask_b"], "max")
            donor_b = b_states[(wid - 1) % len(b_states)]
            su = torch.maximum(sa, sb)
            duplicate_a = torch.maximum(sa, sa)
            swapped_b = torch.maximum(sa, donor_b)
            sf = model.encode(batch["full_facts"], batch["full_mask"], "max")
            assert torch.equal(su, sf), "MAXSET split/union equivalence failed."
            partitions = [[], [], []]
            # One world has four queries but only one evidence set; partition it once.
            for i, fact in enumerate(sorted(episodes[0].reference_facts)):
                partitions[i % 3].append(fact)
            part_batches = [pad_facts([partitions[i]] * len(episodes),
                                      int(model_config["dataset"]["max_facts_per_party"]))
                            for i in range(3)]
            part_states = [model.encode(facts, mask, "max") for facts, mask in part_batches]
            three_left = torch.maximum(torch.maximum(part_states[0], part_states[1]), part_states[2])
            three_right = torch.maximum(part_states[0], torch.maximum(part_states[1], part_states[2]))
            assert torch.equal(three_left, three_right) and torch.equal(three_left, sf)
            a_labels = local_targets(episodes, "a", model.n_entities)
            b_labels = local_targets(episodes, "b", model.n_entities)
            for method, state in (("union", su), ("a_only", sa), ("b_only", sb),
                                  ("full_reencode", sf), ("zero", torch.zeros_like(su)),
                                  ("duplicate_a", duplicate_a), ("swapped_b", swapped_b),
                                  ("three_party_left", three_left), ("three_party_right", three_right)):
                logits = model.read(state, batch["queries"])
                pred = logits.argmax(-1).cpu().tolist()
                for qi, (ep, guess) in enumerate(zip(episodes, pred)):
                    if method == "a_only":
                        target, _ = a_labels[qi]
                        basis = "a"
                    elif method == "b_only":
                        target, _ = b_labels[qi]
                        basis = "b"
                    else:
                        target, basis = ep.target, "union"
                    row = {"stratum": si, "overlap": overlap_values[si], "world_id": wid,
                                 "query_id": qi, "method": method, "hops": 1 if ep.query[2] < 0 else 2,
                                 "target": int(target), "prediction": int(guess), "label_basis": basis,
                                 "known": target < model.n_entities,
                                 "correct": int(guess == target),
                                 "probabilities": logits[qi].softmax(-1).cpu().tolist()}
                    if method in ("a_only", "b_only"):
                        row["union_target"] = int(ep.target)
                        row["union_known"] = bool(ep.target < model.n_entities)
                        row["union_correct"] = int(guess == ep.target)
                    rows.append(row)
    return rows


def summarize(rows, config):
    by_arm = {}
    for arm in ("local", "future"):
        chosen = [r for r in rows if r["arm"] == arm]
        by_arm[arm] = {}
        for si, overlap in enumerate(config["overlaps"]):
            group = [r for r in chosen if r["stratum"] == si]
            for method in ("union", "a_only", "b_only", "full_reencode"):
                mg = [r for r in group if r["method"] == method]
                for subset, filt in (("all", lambda r: True), ("known", lambda r: r["known"]),
                                     ("unknown", lambda r: not r["known"]),
                                     ("known_two_hop", lambda r: r["known"] and r["hops"] == 2)):
                    vals = [r["correct"] for r in mg if filt(r)]
                    by_arm[arm][f"overlap_{overlap}_{method}_{subset}"] = float(np.mean(vals)) if vals else None
            for method in ("a_only", "b_only"):
                vals = [r["union_correct"] for r in group if r["method"] == method and r["union_known"]]
                by_arm[arm][f"overlap_{overlap}_{method}_union_label_known"] = float(np.mean(vals)) if vals else None
    def world_effect(arm):
        maps = {}
        for r in rows:
            if r["arm"] == arm and r["method"] == "union" and r["stratum"] == 2 and r["known"] and r["hops"] == 2:
                maps.setdefault(r["world_id"], []).append(r["correct"])
        return np.array([np.mean(maps[k]) for k in sorted(maps)], dtype=float)
    loc, fut = world_effect("local"), world_effect("future")
    assert len(loc) == len(fut) > 0
    diffs = fut - loc
    rng = np.random.default_rng(config["bootstrap_seed"])
    boots = np.empty(config["bootstrap_resamples"])
    for i in range(len(boots)):
        idx = rng.integers(0, len(diffs), size=len(diffs))
        boots[i] = float(np.mean(diffs[idx]))
    ci = np.quantile(boots, [.025, .975]).tolist()
    fits = []
    for seed in config["seeds"]:
        a = world_effects_by_seed[seed]
        fits.append({"seed": seed, "local": float(a[0].mean()), "future": float(a[1].mean()),
                     "difference": float((a[1]-a[0]).mean())})
    delta = float(diffs.mean())
    inherited = [r for r in rows if r["arm"] == "inherited"]
    def acc(arm, si, method, selector=lambda r: True):
        vals = [r["correct"] for r in rows if r["arm"] == arm and r["stratum"] == si and
                r["method"] == method and selector(r)]
        return float(np.mean(vals)) if vals else None
    future_union = acc("future", 2, "union", lambda r: r["known"] and r["hops"] == 2)
    base_union = acc("inherited", 2, "union", lambda r: r["known"] and r["hops"] == 2)
    future_private = np.mean([acc("future", 2, method, lambda r: r["known"])
                              for method in ("a_only", "b_only")])
    base_private = np.mean([acc("inherited", 2, method, lambda r: r["known"])
                            for method in ("a_only", "b_only")])
    gates = {
        "gain_at_least_2pp": delta * 100 >= config["minimum_gain_pp"],
        "conditional_ci_lower_above_zero": ci[0] > 0,
        "all_three_fit_effects_positive": all(f["difference"] > 0 for f in fits),
        "future_union_within_2pp_of_inherited": future_union >= base_union - config["maximum_union_drop_pp"] / 100,
        "future_union_at_least_90pct": future_union >= config["minimum_reference_accuracy"],
        "future_private_local_within_5pp_of_inherited": future_private >= base_private - config["maximum_local_drop_pp"] / 100,
        "every_future_full_reencode_at_least_90pct": all(
            np.mean([r["correct"] for r in rows if r["seed"] == seed and r["arm"] == "future" and
                     r["stratum"] == 2 and r["method"] == "full_reencode" and r["known"] and r["hops"] == 2])
            >= config["minimum_reference_accuracy"] for seed in config["seeds"]),
    }
    gate = all(gates.values())
    return {"primary": {"contrast": "future minus local", "overlap": config["primary_overlap"],
                         "subset": "known_two_hop", "difference": delta,
                         "conditional_95_percent_interval": ci, "resamples": len(boots),
                         "world_count": len(diffs), "fits": fits,
                         "supported": bool(ci[0] > 0), "all_progress_gates": gates,
                         "progress_gate_passed": bool(gate),
                         "reference_values": {"future_union_accuracy": future_union,
                                              "inherited_union_accuracy": base_union,
                                              "future_private_local_accuracy": float(future_private),
                                              "inherited_private_local_accuracy": float(base_private)}},
            "descriptive_accuracy": by_arm}


if __name__ == "__main__":
    config = load_config(HERE / "config.json")
    model_config = load_config(ROOT / "configs" / "pilot.json")
    sampler_self_check(model_config)
    print("SAMPLER_SELF_CHECK=PASS", flush=True)
    worlds, generation_counts = make_test_data(config, model_config)
    all_rows, all_trace, hash_archive, attempt_archive = [], [], {}, {}
    world_effects_by_seed = {}
    for seed in config["seeds"]:
        paired = {}
        for arm in ("local", "future"):
            model, trace, hashes, attempts = train_arm(seed, arm, config)
            paired[arm] = (hashes, attempts)
            hash_archive[f"{seed}-{arm}"] = hashes
            attempt_archive[f"{seed}-{arm}"] = {"worlds": config["steps"] * config["worlds_per_training_step"],
                "attempted_worlds": int(sum(attempts)), "rejections": int(sum(attempts)-len(attempts)),
                "step_hashes_sha256": hashlib.sha256("".join(hashes).encode()).hexdigest()}
            per_fit = eval_arm(model, worlds, config["overlaps"])
            for row in per_fit:
                row["seed"], row["arm"] = seed, arm
            all_rows += per_fit
            all_trace += trace
            if arm == "local":
                baseline = copy.deepcopy(model)
        assert paired["local"] == paired["future"], "Paired training stream differs between arms."
        # The inherited checkpoint is evaluated on exactly the same held-out worlds.
        ck = torch.load(CHECKPOINTS / f"checkpoint-seed-{seed}.pt", map_location="cpu", weights_only=True)
        reference = LearnedMemory(ck["config"]); reference.load_state_dict(ck["model"]); reference.eval()
        ref_rows = eval_arm(reference, worlds, config["overlaps"])
        for row in ref_rows:
            row["seed"], row["arm"] = seed, "inherited"
        all_rows += ref_rows
        world_effects_by_seed[seed] = []
        for arm in ("local", "future"):
            m = [r for r in all_rows if r["seed"] == seed and r["arm"] == arm and r["method"] == "union" and r["stratum"] == 2 and r["known"] and r["hops"] == 2]
            by_world = {}
            for r in m: by_world.setdefault(r["world_id"], []).append(r["correct"])
            world_effects_by_seed[seed].append(np.array([np.mean(by_world[k]) for k in sorted(by_world)]))
    with gzip.open(HERE / "predictions.jsonl.gz", "wt", encoding="utf-8") as f:
        for row in all_rows: f.write(json.dumps(row, separators=(",", ":")) + "\n")
    (HERE / "training-trace.json").write_text(json.dumps(all_trace, indent=2))
    (HERE / "training-audit.json").write_text(json.dumps({"step_hashes": hash_archive,
        "attempt_counts": attempt_archive, "heldout_generation": generation_counts,
        "sampler_source_check": "exact match against frozen v0.1 sampler on 6 seeded fixtures"}, indent=2))
    summary = summarize(all_rows, config)
    summary["config"] = config
    summary["scope"] = "Synthetic mechanism diagnostic; no pretrained LLM or architectural novelty claim."
    (HERE / "results.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["primary"], indent=2), flush=True)
