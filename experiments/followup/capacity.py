"""Matched-budget capacity and pooling experiments using the original networks."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from functools import partial

import numpy as np
import torch

from src.merge_memory import LearnedMemory, SymmetricMerger, _loss, seed_everything
from .metrics import predict, repeat_state, score, verify_payload
from .packed_table import PackedTable
from .worlds import batch_worlds, draw_world

SHARED_MODES = ("sum_full", "sum_split", "mean_split", "max_split")


def state_for(model, batch, mode):
    pool, source = mode.split("_")
    if source == "full":
        return model.encode(*batch["union"], pool)
    a, b = (model.encode(*facts, "max" if pool == "max" else "sum") for facts in batch["parties"])
    if pool == "max":
        return torch.maximum(a, b)
    return (a + b) / (2 if pool == "mean" else 1)


def optimize(model, loss, optimizer):
    if not bool(torch.isfinite(loss)):
        raise ValueError("Nonfinite training loss")
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0, error_if_nonfinite=True)
    optimizer.step()


def train_backbones(model_config, draw, config, seed, threads):
    seed_everything(seed, threads)
    shared = LearnedMemory(model_config).float()
    models = {name: deepcopy(shared) for name in ("shared", "dedicated_sum", "dedicated_max")}
    optimizers = {name: torch.optim.AdamW(model.parameters(), lr=0.003, weight_decay=0.0001)
                  for name, model in models.items()}
    trace = {name: [] for name in models}
    rng = np.random.default_rng(seed + 305000)
    attempts = Counter()
    for step in range(config["steps"]):
        batch = batch_worlds([draw(rng, 0.30, attempts) for _ in range(config["batch_worlds"])])
        modes = (SHARED_MODES[step % len(SHARED_MODES)], "sum_split", "max_split")
        for (name, model), mode in zip(models.items(), modes):
            state = repeat_state(state_for(model, batch, mode), batch)
            loss = _loss(model, state, batch, 0.30)
            optimize(model, loss, optimizers[name])
            if (step + 1) % 40 == 0 or step + 1 == config["steps"]:
                trace[name].append({"step": step + 1, "loss": float(loss.detach())})
    for model in models.values():
        model.eval()
    return models, trace, dict(attempts)


def train_residuals(model, draw, config, seed):
    torch.manual_seed(seed + 306000)
    base = SymmetricMerger(model.state_dim, model.answer[0].out_features).float()
    mergers = {name: deepcopy(base) for name in ("residual_teacher", "residual_answer_only")}
    opts = {name: torch.optim.AdamW(merger.parameters(), lr=0.002, weight_decay=0.0001)
            for name, merger in mergers.items()}
    rng = np.random.default_rng(seed + 307000)
    attempts = Counter()
    trace = {name: [] for name in mergers}
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    for step in range(config["ablation"]["steps"]):
        batch = batch_worlds([draw(rng, 0.30, attempts) for _ in range(config["batch_worlds"])])
        with torch.no_grad():
            a, b = (model.encode(*facts) for facts in batch["parties"])
            target = model.encode(*batch["union"])
        for name, merger in mergers.items():
            state = merger(a, b)
            loss = _loss(model, repeat_state(state, batch), batch, 0.30)
            if name == "residual_teacher":
                loss = loss + 0.10 * (state - target).square().mean() / target.square().mean().clamp_min(1e-6)
            optimize(merger, loss, opts[name])
            if (step + 1) % 40 == 0 or step + 1 == config["ablation"]["steps"]:
                trace[name].append({"step": step + 1, "loss": float(loss.detach())})
    return mergers, trace, dict(attempts)


@torch.no_grad()
def evaluate_cell(models, mergers, worlds, table, n):
    batch = batch_worlds(worlds)
    rows = {}
    predictions = {}
    plans = {
        "shared": ("sum_split", "max_split", "sum_full", "max_full"),
        "dedicated_sum": ("sum_split", "sum_full"),
        "dedicated_max": ("max_split", "max_full"),
    }
    for name, modes in plans.items():
        model = models[name]
        states = {mode: state_for(model, batch, mode) for mode in modes}
        if "max_split" in states:
            torch.testing.assert_close(states["max_split"], states["max_full"], rtol=1e-5, atol=1e-6)
        for mode, state in states.items():
            verify_payload(state, model)
            predictions[f"{name}/{mode}"] = predict(model, state, batch)
    shared = models["shared"]
    a, b = [shared.encode(*facts) for facts in batch["parties"]]
    for name, merger in mergers.items():
        state = merger(a, b)
        verify_payload(state, shared)
        predictions[name] = predict(shared, state, batch)
    predictions["packed_table"] = torch.tensor([
        table.read(table.merge(*[table.encode(facts) for facts in w.parties]), w.queries)
        for w in worlds
    ])
    predictions["raw_union_oracle"] = torch.tensor([w.targets for w in worlds])
    if table.key_count == table.entities * table.relations:
        torch.testing.assert_close(predictions["packed_table"], predictions["raw_union_oracle"])
    for name, predicted in predictions.items():
        rows[name] = score(predicted, batch, n)
    return rows, {name: predicted.tolist() for name, predicted in predictions.items()}


def capacity(config, pilot, threads, out, emit):
    n = config["n_entities"]
    output = []
    for relations in config["relation_counts"]:
        draw = partial(draw_world, n=n, relations=relations)

        def sample(rng, overlap, attempts):
            return draw(rng, overlap=overlap, attempts=attempts)

        heldout = {}
        corpus = {}
        for ci, overlap in enumerate(config["overlap_levels"]):
            rng = np.random.default_rng(config["evaluation_seed"] + relations * 100 + ci)
            attempts = Counter()
            worlds = [sample(rng, overlap, attempts) for _ in range(config["worlds_per_overlap"])]
            heldout[overlap] = worlds
            union_sizes = [len(w.union) for w in worlds]
            duplicated = [len(set(w.parties[0]) & set(w.parties[1])) for w in worlds]
            corpus[str(overlap)] = {
                "generation": dict(attempts), "mean_union_facts": float(np.mean(union_sizes)),
                "mean_intersection_over_union": float(np.mean(np.array(duplicated) / np.maximum(union_sizes, 1))),
            }
            for i, world in enumerate(worlds):
                emit({"section": "capacity_world", "relations": relations, "overlap": overlap,
                      "id": i, **vars(world)})
        print(f"Capacity relation count {relations}: held-out worlds ready", flush=True)
        for dim in config["state_dims"]:
            model_config = {
                "dataset": {"n_entities": n, "n_relations": relations, "max_revision": 1},
                "architecture": {**pilot["architecture"], "state_dim": dim, "n_slots": config["n_slots"]},
            }
            ablation = config["ablation"]
            ablate = relations == ablation["n_relations"] and dim == ablation["state_dim"]
            for seed in config["fit_seeds"]:
                models, trace, attempts = train_backbones(model_config, sample, config, seed, threads)
                mergers, extra_trace, extra_attempts = (
                    train_residuals(models["shared"], sample, config, seed) if ablate else ({}, {}, {})
                )
                table = PackedTable(n, relations, models["shared"].state_bytes)
                scores = {}
                for overlap, worlds in heldout.items():
                    scores[str(overlap)], predictions = evaluate_cell(models, mergers, worlds, table, n)
                    emit({"section": "capacity_predictions", "relations": relations, "overlap": overlap,
                          "bytes": table.budget, "seed": seed, "predictions_in_world_id_order": predictions})
                model_groups = models | mergers
                output.append({
                    "relations": relations, "seed": seed, "state_dim": dim,
                    "state_bytes": table.budget, "packed_key_count": table.key_count,
                    "parameter_counts": {name: sum(p.numel() for p in model.parameters())
                                         for name, model in model_groups.items()},
                    "corpus": corpus, "scores": scores, "training_trace": trace | extra_trace,
                    "training_generation": attempts, "ablation_generation": extra_attempts,
                })
                torch.save({"config": model_config, "seed": seed,
                            "state_dicts": {name: model.state_dict() for name, model in model_groups.items()}},
                           out / f"capacity-r{relations}-d{dim}-seed{seed}.pt")
                print(f"Completed capacity r={relations}, bytes={table.budget}, seed={seed}", flush=True)
    return output
