"""A bounded synthetic experiment in learned mergeable neural memory.

Only event tensors enter the neural encoder. The reference world and executable
relational oracle live in the data generator and never enter model inference.
Raw evidence is retained by the evaluator solely for the full-reencode reference.
This is a pilot, not a claim of a novel DeepSets model or a neural CRDT.
"""
from __future__ import annotations

import json
import argparse
import csv
import gzip
import math
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

import numpy as np
import torch
from torch import Tensor, nn
import torch.nn.functional as F


def load_config(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def seed_everything(seed: int, threads: int = 1) -> None:
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(threads)
    torch.use_deterministic_algorithms(True)


def permute_facts(facts: list[tuple[int, int, int, int]], permutation: np.ndarray
                  ) -> list[tuple[int, int, int, int]]:
    """Rename entities only; relations and explicit revision tags are unchanged."""
    return [(int(permutation[s]), r, int(permutation[o]), rev)
            for s, r, o, rev in facts]


def canonicalize(facts: list[tuple[int, int, int, int]]
                 ) -> list[tuple[int, int, int, int]]:
    """Evaluator-only unique latest records; contradictory ties stay unresolved.

    This function is NOT used in LearnedMemory.encode, read, or merge.
    """
    by_key: dict[tuple[int, int], list[tuple[int, int, int, int]]] = {}
    for fact in set(facts):
        by_key.setdefault(fact[:2], []).append(fact)
    output = []
    for records in by_key.values():
        latest = max(record[3] for record in records)
        choices = [record for record in records if record[3] == latest]
        if len({record[2] for record in choices}) == 1:
            output.append(choices[0])
    return sorted(output)


def reference_answer(facts: list[tuple[int, int, int, int]], query: tuple[int, int, int],
                     n_entities: int) -> tuple[int, int]:
    """Executable label oracle, deliberately outside all model methods."""
    mapping = {(s, r): o for s, r, o, _ in canonicalize(facts)}
    subject, relation, next_relation = query
    intermediate = mapping.get((subject, relation), n_entities)
    if next_relation < 0:
        return intermediate, intermediate
    if intermediate == n_entities:
        return n_entities, n_entities
    return mapping.get((intermediate, next_relation), n_entities), intermediate


@dataclass
class Episode:
    facts_a: list[tuple[int, int, int, int]]
    facts_b: list[tuple[int, int, int, int]]
    reference_facts: list[tuple[int, int, int, int]]
    query: tuple[int, int, int]
    target: int
    intermediate: int
    required_edges: tuple[tuple[int, int], ...]
    condition: str


def make_episode(rng: np.random.Generator, config: dict[str, Any],
                 condition: str = "train") -> Episode:
    """Fresh functional relational world, then an independent entity renaming.

    In two-hop known-answer episodes the required edges are exclusive to opposite
    parties. Overlap is sampled on distractors, so neither party is sufficient.
    A namespace mismatch corrupts B's names AFTER assigning the original target.
    """
    cfg = config["dataset"]
    n, relations = int(cfg["n_entities"]), int(cfg["n_relations"])
    if relations != 2:
        raise ValueError("The registered pilot uses exactly two relations.")
    world = rng.integers(n, size=(relations, n))
    records = [(s, r, int(world[r, s]), 0) for r in range(relations) for s in range(n)]
    subject, relation = int(rng.integers(n)), int(rng.integers(relations))
    two_hop = rng.random() < float(cfg["two_hop_probability"])
    if condition in {"missing", "update", "namespace_mismatch"}:
        two_hop = True
    query = (subject, relation, 1 - relation if two_hop else -1)
    first = (subject, relation)
    second = (int(world[relation, subject]), 1 - relation)
    required = (first, second) if two_hop else (first,)
    overlap = float(cfg["overlap_probability"])
    if condition == "disjoint":
        overlap = 0.0
    elif condition == "overlap":
        overlap = 0.75
    # Guarantee random ownership, with two-hop required edges on opposite sides.
    first_owner = int(rng.integers(2))
    facts_a, facts_b = [], []
    for record in records:
        key = record[:2]
        if key not in required and rng.random() > float(cfg.get("distractor_retention_probability", 1.0)):
            continue
        if key == first:
            owner = first_owner
        elif two_hop and key == second:
            owner = 1 - first_owner
        elif rng.random() < overlap:
            owner = 2
        else:
            owner = int(rng.integers(2))
        if owner in {0, 2}:
            facts_a.append(record)
        if owner in {1, 2}:
            facts_b.append(record)

    do_update = condition == "update" or (
        condition == "train" and rng.random() < float(cfg["update_probability"]))
    if do_update:
        # Update the LAST required edge, preserving the prerequisite path.
        update_key = required[-1]
        old = int(world[update_key[1], update_key[0]])
        new = int(rng.integers(n - 1))
        if new >= old:
            new += 1
        update = (update_key[0], update_key[1], new, 1)
        # The revised record belongs to the opposite party from its old version.
        if any(record[:2] == update_key for record in facts_a):
            facts_b.append(update)
        else:
            facts_a.append(update)

    do_missing = condition == "missing" or (
        condition == "train" and rng.random() < float(cfg["missing_probability"]))
    if do_missing:
        missing_key = required[int(rng.integers(len(required)))]
        facts_a = [record for record in facts_a if record[:2] != missing_key]
        facts_b = [record for record in facts_b if record[:2] != missing_key]

    if cfg.get("permute_entities_per_episode", True):
        permutation = rng.permutation(n)
        facts_a, facts_b = permute_facts(facts_a, permutation), permute_facts(facts_b, permutation)
        query = (int(permutation[query[0]]), query[1], query[2])
        required = tuple((int(permutation[s]), r) for s, r in required)
    reference_facts = canonicalize(facts_a + facts_b)
    target, intermediate = reference_answer(reference_facts, query, n)
    if two_hop and target < n and (
        len(possible_answers(facts_a, query, n)) < 2 or len(possible_answers(facts_b, query, n)) < 2
    ):
        return make_episode(rng, config, condition)
    if condition == "namespace_mismatch":
        # A derangement ensures names truly differ; labels stay in original space.
        shift = int(rng.integers(1, n))
        wrong_names = (np.arange(n) + shift) % n
        facts_b = permute_facts(facts_b, wrong_names)
    rng.shuffle(facts_a)
    rng.shuffle(facts_b)
    return Episode(facts_a, facts_b, reference_facts, query, target, intermediate,
                   required, condition)


def possible_answers(facts: list[tuple[int, int, int, int]], query: tuple[int, int, int],
                     n_entities: int) -> set[int]:
    """Evaluator ambiguity oracle under INDEPENDENT, unconstrained mappings.

    Enumerate possible missing-edge values, rather than assuming that a missing
    direct lookup is necessarily unknowable. No bijection constraint is allowed.
    """
    mapping = {(s, r): o for s, r, o, _ in canonicalize(facts)}
    s, r1, r2 = query
    possible_first = [mapping[s, r1]] if (s, r1) in mapping else list(range(n_entities))
    if r2 < 0:
        return set(possible_first)
    output: set[int] = set()
    for middle in possible_first:
        if (middle, r2) in mapping:
            output.add(mapping[middle, r2])
        else:
            output.update(range(n_entities))
    return output


def make_query_world(rng: np.random.Generator, config: dict[str, Any], overlap: float
                     ) -> list[Episode]:
    """Four distinct queries share one world, evidence split, and missing records.

    Exactly two one-hop and two two-hop queries. Critical path records, if present,
    are exclusive and relation-colored to opposite parties. Every known two-hop
    query must leave at least two consistent answers for EACH private party.
    """
    cfg = config["dataset"]
    n = int(cfg["n_entities"])
    for _ in range(1000):
        world = rng.integers(n, size=(2, n))
        keys = [(s, r) for s in range(n) for r in range(2)]
        two_keys = [keys[i] for i in rng.choice(len(keys), 2, replace=False)]
        one_keys = [keys[i] for i in rng.choice(len(keys), 2, replace=False)]
        queries = [(s, r, -1) for s, r in one_keys] + [(s, r, 1 - r) for s, r in two_keys]
        paths = [((s, r),) if r2 < 0 else ((s, r), (int(world[r, s]), r2))
                 for s, r, r2 in queries]
        critical = set(edge for path in paths[2:] for edge in path)
        keep = set(edge for path in paths for edge in path)
        missing: set[tuple[int, int]] = set()
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
            a, b = permute_facts(a, permutation), permute_facts(b, permutation)
            queries = [(int(permutation[s]), r, r2) for s, r, r2 in queries]
            paths = [tuple((int(permutation[s]), r) for s, r in path) for path in paths]
        reference = canonicalize(a + b)
        answers = [reference_answer(reference, query, n) for query in queries]
        if any(target < n and (len(possible_answers(a, query, n)) < 2 or
                               len(possible_answers(b, query, n)) < 2)
               for query, (target, _) in zip(queries[2:], answers[2:])):
            continue
        rng.shuffle(a)
        rng.shuffle(b)
        return [Episode(list(a), list(b), reference, query, target, intermediate,
                        path, f"overlap_{overlap}")
                for query, (target, intermediate), path in zip(queries, answers, paths)]
    raise RuntimeError("Unable to sample an ambiguity-validated world in 1000 attempts.")


def pad_facts(rows: list[list[tuple[int, int, int, int]]], max_facts: int
              ) -> tuple[Tensor, Tensor]:
    facts = torch.zeros((len(rows), max_facts, 4), dtype=torch.long)
    mask = torch.zeros((len(rows), max_facts), dtype=torch.bool)
    for i, row in enumerate(rows):
        if len(row) > max_facts:
            raise ValueError("Fact padding would truncate evidence; increase the registered cap.")
        if row:
            facts[i, :len(row)] = torch.tensor(row, dtype=torch.long)
            mask[i, :len(row)] = True
    return facts, mask


def batch_episodes(episodes: list[Episode], config: dict[str, Any]) -> dict[str, Tensor]:
    cap = int(config["dataset"]["max_facts_per_party"])
    a, am = pad_facts([episode.facts_a for episode in episodes], cap)
    b, bm = pad_facts([episode.facts_b for episode in episodes], cap)
    full, fm = pad_facts([episode.reference_facts for episode in episodes], cap)
    return {
        "facts_a": a, "mask_a": am, "facts_b": b, "mask_b": bm,
        "full_facts": full, "full_mask": fm,
        "queries": torch.tensor([episode.query for episode in episodes], dtype=torch.long),
        "targets": torch.tensor([episode.target for episode in episodes], dtype=torch.long),
        "intermediate_targets": torch.tensor([episode.intermediate for episode in episodes], dtype=torch.long),
    }


def make_batch(rng: np.random.Generator, batch_size: int, config: dict[str, Any],
               condition: str = "train") -> dict[str, Tensor]:
    return batch_episodes([make_episode(rng, config, condition) for _ in range(batch_size)], config)


class LearnedMemory(nn.Module):
    """Shared learned event encoder and recurrent attention reader.

    State is a fixed [slots, dimension] float32 tensor. Every stored coordinate is
    learned; inference performs no key lookup, canonicalization, or graph walk.
    Two reads are an explicit task inductive bias; the intermediate is predicted.
    """
    def __init__(self, config: dict[str, Any]):
        super().__init__()
        data, arch = config["dataset"], config["architecture"]
        self.n_entities = int(data["n_entities"])
        self.n_relations = int(data["n_relations"])
        self.n_slots, self.state_dim = int(arch["n_slots"]), int(arch["state_dim"])
        self.pool_scale = float(arch["pool_scale"])
        e, h, d = int(arch["embedding_dim"]), int(arch["hidden_dim"]), self.state_dim
        self.entities = nn.Embedding(self.n_entities + 1, e)
        self.relations = nn.Embedding(self.n_relations, e)
        self.revisions = nn.Embedding(int(data["max_revision"]) + 1, e)
        self.event_key = nn.Sequential(nn.Linear(3 * e, h), nn.Tanh(), nn.Linear(h, d))
        self.event_value = nn.Sequential(nn.Linear(4 * e, h), nn.ReLU(), nn.Linear(h, d), nn.ReLU())
        self.slot_keys = nn.Parameter(torch.randn(self.n_slots, d) / math.sqrt(d))
        self.state_norm = nn.LayerNorm(d)
        self.read_key = nn.Linear(d, d)
        self.read_value = nn.Linear(d, d)
        self.query_key = nn.Sequential(nn.Linear(2 * e, h), nn.Tanh(), nn.Linear(h, d))
        self.answer = nn.Sequential(nn.Linear(d + 2 * e, h), nn.ReLU(),
                                    nn.Linear(h, self.n_entities + 1))

    @property
    def state_bytes(self) -> int:
        return self.n_slots * self.state_dim * torch.tensor([], dtype=torch.float32).element_size()

    def event_features(self, facts: Tensor) -> Tensor:
        s, r, o, revision = facts.unbind(-1)
        es, er, eo, et = self.entities(s), self.relations(r), self.entities(o), self.revisions(revision)
        key = self.event_key(torch.cat((es, er, et), -1))
        value = self.event_value(torch.cat((es, er, eo, et), -1))
        routing = torch.softmax(torch.einsum("bfd,kd->bfk", key, self.slot_keys) / math.sqrt(self.state_dim), -1)
        return routing.unsqueeze(-1) * value.unsqueeze(-2)

    def encode(self, facts: Tensor, mask: Tensor, pool: str = "sum") -> Tensor:
        features = self.event_features(facts)
        if pool == "sum":
            return (features * mask[:, :, None, None]).sum(1) / self.pool_scale
        if pool == "max":
            state = features.masked_fill(~mask[:, :, None, None], -torch.inf).amax(1)
            return torch.where(mask.any(1)[:, None, None], state, torch.zeros_like(state)) / self.pool_scale
        raise ValueError(f"Unknown pool {pool!r}")

    def _read_once(self, state: Tensor, subject_embedding: Tensor, relation: Tensor) -> Tensor:
        re = self.relations(relation)
        query = self.query_key(torch.cat((subject_embedding, re), -1))
        normalized = self.state_norm(state)
        keys, values = self.read_key(normalized), self.read_value(normalized)
        weights = torch.softmax(torch.einsum("bd,bkd->bk", query, keys) / math.sqrt(self.state_dim), -1)
        readout = torch.einsum("bk,bkd->bd", weights, values)
        return self.answer(torch.cat((readout, subject_embedding, re), -1))

    def read(self, state: Tensor, queries: Tensor, return_intermediate: bool = False
             ) -> Tensor | tuple[Tensor, Tensor]:
        subject, r1, r2 = queries.unbind(-1)
        first_logits = self._read_once(state, self.entities(subject), r1)
        # A differentiable predicted intermediate; no oracle teacher forcing.
        next_subject = torch.softmax(first_logits, -1) @ self.entities.weight
        second_logits = self._read_once(state, next_subject, r2.clamp_min(0))
        logits = torch.where((r2 >= 0)[:, None], second_logits, first_logits)
        return (logits, first_logits) if return_intermediate else logits


class SymmetricMerger(nn.Module):
    """Learned per-slot residual, symmetric with an exact empty-input identity.

    Neither associativity nor idempotence is guaranteed. Training references the
    canonical full-state encoding, but inference only receives two latent states.
    """
    def __init__(self, state_dim: int, hidden_dim: int):
        super().__init__()
        self.correction = nn.Sequential(nn.Linear(3 * state_dim, hidden_dim), nn.Tanh(),
                                        nn.Linear(hidden_dim, state_dim))
        nn.init.zeros_(self.correction[-1].weight)
        nn.init.zeros_(self.correction[-1].bias)

    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        summed = a + b
        features = torch.cat((summed, (a - b).abs(), a * b), -1)
        magnitude_a = a.norm(dim=-1, keepdim=True) / math.sqrt(a.shape[-1])
        magnitude_b = b.norm(dim=-1, keepdim=True) / math.sqrt(b.shape[-1])
        gate = 2 * magnitude_a * magnitude_b / (magnitude_a + magnitude_b + 1e-8)
        return summed + gate * self.correction(features)


class DeepSetsMerger(nn.Module):
    """Strong trained pair baseline: rho(phi(a) + phi(b)), slot by slot."""
    def __init__(self, state_dim: int, hidden_dim: int):
        super().__init__()
        self.phi = nn.Sequential(nn.Linear(state_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, state_dim))
        self.rho = nn.Sequential(nn.Linear(state_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, state_dim))

    def forward(self, a: Tensor, b: Tensor) -> Tensor:
        return self.rho(self.phi(a) + self.phi(b))


def merge_state(method: str, a: Tensor, b: Tensor, merger: SymmetricMerger,
                deepsets: DeepSetsMerger | None = None) -> Tensor:
    if method == "learned":
        return merger(a, b)
    if method == "deepsets":
        if deepsets is None:
            raise ValueError("The trained DeepSets comparator must be provided.")
        return deepsets(a, b)
    if method == "sum":
        return a + b
    if method == "max":
        return torch.maximum(a, b)
    if method == "mean":
        return (a + b) / 2
    if method == "a_only":
        return a
    if method == "b_only":
        return b
    if method == "zero":
        return torch.zeros_like(a)
    raise ValueError(f"Unknown merge method {method!r}")


def _loss(model: LearnedMemory, state: Tensor, batch: dict[str, Tensor], weight: float) -> Tensor:
    logits, first = model.read(state, batch["queries"], return_intermediate=True)
    return F.cross_entropy(logits, batch["targets"]) + weight * F.cross_entropy(first, batch["intermediate_targets"])


def train_shared(config: dict[str, Any], seed: int,
                  progress: Callable[[dict[str, Any]], None] | None = None
                  ) -> tuple[LearnedMemory, list[dict[str, Any]]]:
    """Explicit invocation required. Do not call before preregistration freeze."""
    cfg = config["training"]
    seed_everything(seed, int(cfg["threads"]))
    model = LearnedMemory(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=float(cfg["learning_rate"]),
                                  weight_decay=float(cfg["weight_decay"]))
    rng = np.random.default_rng(seed + 7000)
    history = []
    modes = cfg["shared_pool_training"]
    started = time.perf_counter()
    model.train()
    for step in range(int(cfg["shared_steps"])):
        batch = make_batch(rng, int(cfg["batch_size"]), config)
        mode = modes[step % len(modes)]
        if mode.endswith("full"):
            state = model.encode(batch["full_facts"], batch["full_mask"], mode.split("_")[0])
        else:
            pool = "max" if mode.startswith("max") else "sum"
            a = model.encode(batch["facts_a"], batch["mask_a"], pool)
            b = model.encode(batch["facts_b"], batch["mask_b"], pool)
            if mode.startswith("max"):
                state = torch.maximum(a, b)
            elif mode.startswith("mean"):
                state = (a + b) / 2
            else:
                state = a + b
        optimizer.zero_grad(set_to_none=True)
        loss = _loss(model, state, batch, float(cfg["intermediate_loss_weight"]))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        if (step + 1) % int(cfg["log_every"]) == 0:
            row = {"phase": "shared", "seed": seed, "step": step + 1,
                   "loss": float(loss.detach()), "seconds": time.perf_counter() - started}
            history.append(row)
            if progress:
                progress(row)
    model.eval()
    return model, history


def train_merger(model: LearnedMemory, config: dict[str, Any], seed: int,
                  progress: Callable[[dict[str, Any]], None] | None = None,
                  merger_kind: str = "learned"
                  ) -> tuple[SymmetricMerger | DeepSetsMerger, list[dict[str, Any]]]:
    """Train only merger; all baselines use exactly the frozen shared backbone."""
    cfg = config["training"]
    torch.manual_seed(seed + 13000)
    if merger_kind not in {"learned", "deepsets"}:
        raise ValueError("Registered trained merge kinds are learned and deepsets.")
    merger_class = SymmetricMerger if merger_kind == "learned" else DeepSetsMerger
    merger = merger_class(model.state_dim, int(config["architecture"]["hidden_dim"]))
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    optimizer = torch.optim.AdamW(merger.parameters(), lr=float(cfg["merger_learning_rate"]),
                                  weight_decay=float(cfg["weight_decay"]))
    rng = np.random.default_rng(seed + 17000)
    history, started = [], time.perf_counter()
    model.eval()
    merger.train()
    for step in range(int(cfg["merger_steps"])):
        batch = make_batch(rng, int(cfg["batch_size"]), config)
        with torch.no_grad():
            a = model.encode(batch["facts_a"], batch["mask_a"])
            b = model.encode(batch["facts_b"], batch["mask_b"])
            target_state = model.encode(batch["full_facts"], batch["full_mask"])
        merged = merger(a, b)
        answer_loss = _loss(model, merged, batch, float(cfg["intermediate_loss_weight"]))
        # Scale-invariant relative state error prevents tiny latent vectors from
        # making consistency appear successful while preserving wrong answers.
        state_error = (merged - target_state).square().mean() / target_state.square().mean().clamp_min(1e-6)
        idempotence = (merger(a, a) - a).square().mean() / a.square().mean().clamp_min(1e-6)
        loss = answer_loss + float(cfg["state_consistency_weight"]) * state_error + float(cfg["idempotence_weight"]) * idempotence
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(merger.parameters(), 1.0)
        optimizer.step()
        if (step + 1) % int(cfg["log_every"]) == 0:
            row = {"phase": merger_kind, "seed": seed, "step": step + 1,
                   "loss": float(loss.detach()), "state_relative_mse": float(state_error.detach()),
                   "seconds": time.perf_counter() - started}
            history.append(row)
            if progress:
                progress(row)
    merger.eval()
    return merger, history


def _calibration(confidences: Tensor, correct: Tensor, bins: int) -> float:
    error = 0.0
    for i in range(bins):
        selected = (confidences >= i / bins) & (confidences <= (i + 1) / bins if i + 1 == bins else confidences < (i + 1) / bins)
        if selected.any():
            error += float(selected.float().mean() * (confidences[selected].mean() - correct[selected].float().mean()).abs())
    return error


@torch.no_grad()
def evaluate(model: LearnedMemory, merger: SymmetricMerger, config: dict[str, Any], seed: int
             , return_predictions: bool = False, deepsets: DeepSetsMerger | None = None
             ) -> dict[str, Any] | tuple[dict[str, Any], list[dict[str, Any]]]:
    """Fresh common worlds across methods, distinct test stream for each fit."""
    cfg = config["evaluation"]
    model.eval()
    merger.eval()
    if deepsets is not None:
        deepsets.eval()
    report: dict[str, Any] = {"seed": seed, "state_bytes": model.state_bytes, "conditions": {}}
    predictions: list[dict[str, Any]] = []
    n = int(config["dataset"]["n_entities"])
    for ci, condition in enumerate(cfg["conditions"]):
        rng = np.random.default_rng(seed + int(cfg["seed_offset"]) + ci * 10000)
        overlap = float(cfg["overlap_levels"][ci])
        outputs = {method: {"logits": [], "targets": [], "two_hop": [], "seconds": 0.0,
                            "relative_state_error": [], "commutativity": [], "idempotence": [], "associativity": []}
                   for method in cfg["methods"]}
        remaining = int(cfg["worlds_per_condition"])
        next_world = 0
        while remaining:
            size = min(remaining, max(1, int(cfg["batch_size"]) // int(cfg["queries_per_world"])))
            if "swapped_B" in cfg["methods"] and size < 2:
                raise ValueError("The swapped-B control needs at least two distinct worlds in each evaluation batch.")
            worlds = [make_query_world(rng, config, overlap) for _ in range(size)]
            episodes = [episode for world in worlds for episode in world]
            batch = batch_episodes(episodes, config)
            sum_a = model.encode(batch["facts_a"], batch["mask_a"])
            sum_b = model.encode(batch["facts_b"], batch["mask_b"])
            donor_b = torch.roll(sum_b, int(cfg["queries_per_world"]), 0)
            max_a = model.encode(batch["facts_a"], batch["mask_a"], "max")
            max_b = model.encode(batch["facts_b"], batch["mask_b"], "max")
            full_sum = model.encode(batch["full_facts"], batch["full_mask"])
            full_max = model.encode(batch["full_facts"], batch["full_mask"], "max")
            third = torch.roll(sum_a, 1, 0)  # algebraic probe, not extra query evidence
            for method, out in outputs.items():
                started = time.perf_counter()
                if method == "full_reencode_sum":
                    state = full_sum
                elif method == "full_reencode_max":
                    state = full_max
                elif method == "max":
                    state = torch.maximum(max_a, max_b)
                elif method == "swapped_B":
                    state = merger(sum_a, donor_b)
                else:
                    state = merge_state(method, sum_a, sum_b, merger, deepsets)
                logits = model.read(state, batch["queries"])
                out["seconds"] += time.perf_counter() - started
                out["logits"].append(logits)
                out["targets"].append(batch["targets"])
                out["two_hop"].append(batch["queries"][:, 2] >= 0)
                probabilities = logits.softmax(-1)
                confidence, predicted = probabilities.max(-1)
                for row_index, episode in enumerate(episodes):
                    predictions.append({
                        "seed": seed, "stratum": condition,
                        "world_id": next_world + row_index // int(cfg["queries_per_world"]),
                        "query_id": row_index % int(cfg["queries_per_world"]),
                        "method": method, "subject": episode.query[0], "relation1": episode.query[1],
                        "relation2": episode.query[2], "hops": 2 if episode.query[2] >= 0 else 1,
                        "target": episode.target, "prediction": int(predicted[row_index]),
                        "correct": int(predicted[row_index]) == episode.target,
                        "known": episode.target < n,
                        "confidence": float(confidence[row_index]),
                        "local_possible_answers_a": len(possible_answers(episode.facts_a, episode.query, n)),
                        "local_possible_answers_b": len(possible_answers(episode.facts_b, episode.query, n)),
                        "donor_world_id": (next_world + (row_index // int(cfg["queries_per_world"]) - 1) % size) if method == "swapped_B" else "",
                        "probabilities": json.dumps(probabilities[row_index].tolist(), separators=(",", ":")),
                    })
                reference = full_max if method in {"max", "full_reencode_max"} else full_sum
                out["relative_state_error"].append((state - reference).square().flatten(1).mean(1) / reference.square().flatten(1).mean(1).clamp_min(1e-6))
                if method in {"learned", "deepsets", "sum", "max", "mean"}:
                    pa, pb = (max_a, max_b) if method == "max" else (sum_a, sum_b)
                    pc = torch.roll(pa, 1, 0) if method == "max" else third
                    scale = pa.square().mean().clamp_min(1e-6)
                    out["commutativity"].append(((merge_state(method, pa, pb, merger, deepsets) - merge_state(method, pb, pa, merger, deepsets)).square().mean() / scale).sqrt())
                    out["idempotence"].append(((merge_state(method, pa, pa, merger, deepsets) - pa).square().mean() / scale).sqrt())
                    left = merge_state(method, merge_state(method, pa, pb, merger, deepsets), pc, merger, deepsets)
                    right = merge_state(method, pa, merge_state(method, pb, pc, merger, deepsets), merger, deepsets)
                    out["associativity"].append(((left - right).square().mean() / scale).sqrt())
            remaining -= size
            next_world += size
        summaries = {}
        for method, out in outputs.items():
            logits, targets, hops = torch.cat(out["logits"]), torch.cat(out["targets"]), torch.cat(out["two_hop"])
            probabilities = logits.softmax(-1)
            confidence, predicted = probabilities.max(-1)
            correct = predicted == targets
            known = targets != n
            row = {
                "n": len(targets), "accuracy": float(correct.float().mean()),
                "known_accuracy": float(correct[known].float().mean()) if known.any() else None,
                "two_hop_accuracy": float(correct[hops].float().mean()) if hops.any() else None,
                "one_hop_accuracy": float(correct[~hops].float().mean()) if (~hops).any() else None,
                "unknown_recall": float((predicted[~known] == n).float().mean()) if (~known).any() else None,
                "mean_confidence": float(confidence.mean()),
                "ece": _calibration(confidence, correct, int(cfg["calibration_bins"])),
                "relative_state_mse": float(torch.cat(out["relative_state_error"]).mean()),
                "merge_and_read_seconds": out["seconds"],
                "timing_scope": "merge plus reader only; encoder time excluded, CPU sequential and descriptive",
            }
            for name in ("commutativity", "idempotence", "associativity"):
                row[name + "_relative_rmse"] = float(torch.stack(out[name]).mean()) if out[name] else None
            summaries[method] = row
            primary_rows = [record for record in predictions if record["seed"] == seed and
                            record["stratum"] == condition and record["method"] == method and
                            record["hops"] == 2 and record["known"]]
            by_world: dict[int, list[int]] = {}
            for record in primary_rows:
                by_world.setdefault(record["world_id"], []).append(int(record["correct"]))
            row["known_two_hop_world_macro_accuracy"] = float(np.mean([np.mean(items) for items in by_world.values()])) if by_world else None
            row["known_two_hop_world_count"] = len(by_world)
            row["known_two_hop_query_count"] = len(primary_rows)
        report["conditions"][condition] = summaries
    return (report, predictions) if return_predictions else report


def primary_bootstrap(predictions: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    """Paired world bootstrap within each of three fixed fitted models.

    This conditional interval does NOT estimate variability over training seeds.
    """
    cfg = config["evaluation"]
    main, baseline = cfg["primary_contrast"]
    results, values = [], []
    for seed in config["training"]["seeds"]:
        by_world: dict[int, dict[str, list[int]]] = {}
        for row in predictions:
            if row["seed"] != seed or row["stratum"] != cfg["primary_condition"] or row["hops"] != 2 or not row["known"] or row["method"] not in (main, baseline):
                continue
            by_world.setdefault(row["world_id"], {}).setdefault(row["method"], []).append(int(row["correct"]))
        differences = np.array([np.mean(methods[main]) - np.mean(methods[baseline])
                                for methods in by_world.values()], dtype=np.float64)
        if not len(differences):
            raise ValueError("No known two-hop worlds in the registered primary stratum.")
        values.append(differences)
        results.append({"seed": seed, "worlds": len(differences), "difference": float(differences.mean())})
    rng = np.random.default_rng(int(cfg["bootstrap_seed"]))
    resamples = int(cfg["bootstrap_resamples"])
    boot = np.zeros(resamples)
    for differences in values:
        boot += differences[rng.integers(len(differences), size=(resamples, len(differences)))].mean(1) / len(values)
    lower, upper = np.quantile(boot, [0.025, 0.975])
    return {"main": main, "baseline": baseline, "condition": cfg["primary_condition"],
            "subset": cfg["primary_subset"], "unit": "world; average eligible queries, then equally average fitted models",
            "difference": float(np.mean([v.mean() for v in values])),
            "conditional_95_percent_interval": [float(lower), float(upper)],
            "resamples": resamples, "bootstrap_seed": int(cfg["bootstrap_seed"]), "fits": results,
            "interpretation": "Conditional on these three trained models; not a confidence interval over the population of training seeds."}


def run_pilot(config: dict[str, Any], output_directory: str | Path) -> dict[str, Any]:
    """Called by the authorized root ONLY after preregistration and code freeze."""
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)
    reports, predictions, trace, checkpoints = [], [], [], []
    started = time.perf_counter()
    for seed in config["training"]["seeds"]:
        def progress(row: dict[str, Any]) -> None:
            print(json.dumps(row), flush=True)
        model, shared_trace = train_shared(config, int(seed), progress)
        merger, merger_trace = train_merger(model, config, int(seed), progress)
        deepsets, deepsets_trace = train_merger(model, config, int(seed), progress, "deepsets")
        report, rows = evaluate(model, merger, config, int(seed), return_predictions=True, deepsets=deepsets)
        report["shared_parameter_count"] = sum(parameter.numel() for parameter in model.parameters())
        report["merger_parameter_count"] = sum(parameter.numel() for parameter in merger.parameters())
        report["deepsets_parameter_count"] = sum(parameter.numel() for parameter in deepsets.parameters())
        report["shared_parameter_bytes"] = sum(parameter.numel() * parameter.element_size() for parameter in model.parameters())
        report["merger_parameter_bytes"] = sum(parameter.numel() * parameter.element_size() for parameter in merger.parameters())
        report["deepsets_parameter_bytes"] = sum(parameter.numel() * parameter.element_size() for parameter in deepsets.parameters())
        report["state_float_count"] = model.n_slots * model.state_dim
        checkpoint = output / f"checkpoint-seed-{seed}.pt"
        torch.save({"seed": seed, "model": model.state_dict(), "merger": merger.state_dict(), "deepsets": deepsets.state_dict(),
                    "config": config, "selection_rule": "last configured step, no test selection"}, checkpoint)
        checkpoints.append(checkpoint.name)
        reports.append(report)
        predictions.extend(rows)
        trace.extend(shared_trace + merger_trace + deepsets_trace)
    with gzip.open(output / "predictions.csv.gz", "wt", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)
    with open(output / "training-trace.json", "w", encoding="utf-8") as handle:
        json.dump(trace, handle, indent=2)
    summary = {"config": config, "runs": reports, "primary": primary_bootstrap(predictions, config),
               "elapsed_seconds": time.perf_counter() - started, "prediction_rows": len(predictions),
               "checkpoints": checkpoints,
               "checkpoint_selection": "final configured step only; no validation/test-driven selection",
               "scope": "small learned synthetic neural-memory prototype; no pretrained LLM and no established architectural novelty"}
    with open(output / "metrics.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    train = commands.add_parser("train", help="Run the fixed pilot after preregistration freeze")
    train.add_argument("--config", type=Path, required=True)
    train.add_argument("--out", type=Path, required=True)
    train.add_argument("--threads", type=int, default=None)
    train.add_argument("--preregistration-frozen", action="store_true", help="Affirm the root verified the frozen preregistration/code manifest")
    args = parser.parse_args()
    if not args.preregistration_frozen:
        parser.error("Training requires an already frozen preregistration and source manifest.")
    config = load_config(args.config)
    if args.threads is not None:
        if args.threads != int(config["training"]["threads"]):
            parser.error("Thread override differs from frozen config; change and refreeze before training.")
    summary = run_pilot(config, args.out)
    print(json.dumps({"primary": summary["primary"], "elapsed_seconds": summary["elapsed_seconds"]}), flush=True)


if __name__ == "__main__":
    main()
